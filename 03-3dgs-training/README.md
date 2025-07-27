# 3D Gaussian Splatting Training Pipeline

## 🎯 Purpose
Train high-quality 3D Gaussian Splatting models from prepared synthetic multi-view datasets of battleships.

## 📥 Inputs
- Prepared dataset from Stage 2 (COLMAP format)
- Camera poses and intrinsics
- 200-500 multi-view images

## 📤 Outputs
- Trained `.ply` file with gaussian splats (3-8M splats)
- Training metrics and convergence graphs
- Checkpoint files for resume capability
- Quality assessment report

## 🔧 Training Pipeline

### 1. Environment Setup

```bash
# Clone 3DGS repository
git clone https://github.com/graphdeco-inria/gaussian-splatting.git
cd gaussian-splatting

# Install dependencies
pip install -r requirements.txt
pip install submodules/diff-gaussian-rasterization
pip install submodules/simple-knn
```

### 2. Hardware Configuration

**Local Setup: RTX 3090 + 5090**
```python
# Optimal settings for available VRAM
CONFIG = {
    "3090": {
        "max_images": 100,      # Limit concurrent images
        "resolution_scale": 0.5, # Start with half resolution
        "densification_interval": 500,
        "max_splats": 5_000_000
    },
    "5090": {
        "max_images": 200,      # Full dataset
        "resolution_scale": 1.0, # Full resolution
        "densification_interval": 300,
        "max_splats": 8_000_000
    }
}
```

### 3. Training Configuration

```python
# train_bismarck.py
import os
import torch
from arguments import ModelParams, PipelineParams, OptimizationParams

def get_bismarck_config():
    parser = ArgumentParser(description="Bismarck training params")
    
    # Model parameters
    model = ModelParams(parser)
    model.sh_degree = 3  # Spherical harmonics degree
    
    # Pipeline parameters  
    pipeline = PipelineParams(parser)
    pipeline.convert_SHs_python = False
    pipeline.compute_cov3D_python = False
    
    # Optimization parameters
    opt = OptimizationParams(parser)
    opt.iterations = 30000  # Can extend to 50000 for quality
    opt.position_lr_init = 0.00016
    opt.position_lr_final = 0.0000016
    opt.position_lr_delay_mult = 0.01
    opt.position_lr_max_steps = 30000
    opt.feature_lr = 0.0025
    opt.opacity_lr = 0.05
    opt.scaling_lr = 0.005
    opt.rotation_lr = 0.001
    
    # Densification
    opt.densify_from_iter = 500
    opt.densify_until_iter = 15000
    opt.densify_grad_threshold = 0.0002
    opt.densification_interval = 100
    opt.opacity_reset_interval = 3000
    
    return model, pipeline, opt
```

### 4. Training Execution

```bash
# Basic training command
python train.py \
    -s data/bismarck_dataset \
    -m output/bismarck_splats \
    --eval \
    --iterations 30000

# With custom config
python train.py \
    -s data/bismarck_dataset \
    -m output/bismarck_splats \
    --eval \
    --sh_degree 3 \
    --images_resolution 2 \
    --resolution 2048 \
    --iterations 50000 \
    --checkpoint_iterations 5000 \
    --save_iterations 5000 10000 20000 30000 50000
```

### 5. Multi-GPU Strategy

For 3090 + 5090 setup:
```python
def distributed_training():
    # Use 5090 for main training
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # 5090
    
    # Use 3090 for validation renders
    # Run separate process for evaluation
```

### 6. Training Monitoring

```python
class TrainingMonitor:
    def __init__(self, log_dir):
        self.writer = SummaryWriter(log_dir)
        
    def log_metrics(self, iteration, metrics):
        self.writer.add_scalar('Loss/L1', metrics['l1_loss'], iteration)
        self.writer.add_scalar('Loss/SSIM', metrics['ssim_loss'], iteration)
        self.writer.add_scalar('PSNR', metrics['psnr'], iteration)
        self.writer.add_scalar('Num_Splats', metrics['num_gaussians'], iteration)
        
    def log_images(self, iteration, renders, ground_truth):
        self.writer.add_images('Renders', renders, iteration)
        self.writer.add_images('Ground_Truth', ground_truth, iteration)
        self.writer.add_images('Difference', 
                              torch.abs(renders - ground_truth), 
                              iteration)
```

### 7. Quality Checkpoints

```python
def evaluate_checkpoint(model_path, test_views):
    metrics = {
        'psnr': [],
        'ssim': [],
        'lpips': []
    }
    
    for view in test_views:
        rendered = render_gaussian_splats(model_path, view)
        gt = load_ground_truth(view)
        
        metrics['psnr'].append(calculate_psnr(rendered, gt))
        metrics['ssim'].append(calculate_ssim(rendered, gt))
        metrics['lpips'].append(calculate_lpips(rendered, gt))
    
    return {
        'psnr': np.mean(metrics['psnr']),
        'ssim': np.mean(metrics['ssim']),
        'lpips': np.mean(metrics['lpips'])
    }
```

## 🎚️ Hyperparameter Tuning

### Key Parameters to Adjust

1. **Learning Rates**
   - Position LR: Controls splat movement
   - Scaling LR: Controls splat size
   - Opacity LR: Controls transparency

2. **Densification**
   - Gradient threshold: When to split/clone splats
   - Interval: How often to densify
   - Until iteration: When to stop adding splats

3. **Pruning**
   - Opacity threshold: Remove transparent splats
   - Scale threshold: Remove huge splats
   - View-space threshold: Remove off-screen splats

### Bismarck-Specific Settings

```python
# For ship with fine details (rigging, guns)
DETAIL_CONFIG = {
    "densify_grad_threshold": 0.0001,  # Lower = more splats
    "prune_opacity_threshold": 0.005,   # Lower = keep more
    "max_splat_size": 0.1,              # Prevent giant splats
    "position_lr_init": 0.00008         # Slower = more stable
}
```

## 🧪 Validation Process

### During Training
- Monitor loss convergence
- Check splat count growth
- Validate on held-out views
- Watch for overfitting

### Post-Training
1. **Visual Inspection**
   - Render from novel viewpoints
   - Check for floaters/artifacts
   - Verify detail preservation

2. **Quantitative Metrics**
   - PSNR > 28 dB
   - SSIM > 0.90
   - LPIPS < 0.1

3. **Technical Drawing Validation**
   - Measure ship dimensions in renders
   - Compare to blueprint specifications
   - Ensure proportional accuracy

## ⚠️ Common Issues

### Problem: Out of Memory
```python
# Solutions:
# 1. Reduce batch size
opt.batch_size = 1

# 2. Lower resolution initially
opt.resolution_scale = 0.5

# 3. Limit splat count
opt.max_gaussians = 3_000_000
```

### Problem: Poor Convergence
```python
# Solutions:
# 1. Adjust learning rates
opt.position_lr_init *= 0.5

# 2. Extend training
opt.iterations = 50000

# 3. Better initialization
opt.random_init = False
```

### Problem: Floating Artifacts
```python
# Solutions:
# 1. Aggressive pruning
opt.prune_big_splats = True
opt.max_splat_size = 0.05

# 2. Opacity regularization
opt.opacity_reg = 0.01
```

## 📊 Expected Results

### Training Timeline (3090/5090)
- 0-5k iterations: Basic shape emerges
- 5k-15k: Details develop, densification active
- 15k-25k: Refinement, quality improvement
- 25k-30k+: Final polish, convergence

### Quality Targets
- **Splat Count**: 3-8M (memory dependent)
- **Training Time**: 6-12 hours
- **Final PSNR**: >28 dB
- **Final SSIM**: >0.90

## 🚀 Next Steps

After successful training:
1. Save final `.ply` file
2. Generate quality metrics report
3. Create preview renders
4. Move to splat refinement stage