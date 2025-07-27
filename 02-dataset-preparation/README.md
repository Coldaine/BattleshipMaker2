# Dataset Preparation Pipeline

## 🎯 Purpose
Transform synthetic multi-view images into a properly formatted dataset for 3D Gaussian Splatting training, including camera pose estimation and validation.

## 📥 Inputs
- 200-500 synthetic images from Stage 1
- Technical drawing reference data
- Camera angle metadata from generation

## 📤 Outputs
- COLMAP-compatible dataset structure
- Camera intrinsics/extrinsics files
- Validated image set ready for 3DGS
- Quality metrics report

## 🔧 Pipeline Steps

### 1. Dataset Organization
```
bismarck_dataset/
├── images/
│   ├── view_000.jpg
│   ├── view_001.jpg
│   └── ...
├── sparse/
│   └── 0/
│       ├── cameras.bin
│       ├── images.bin
│       └── points3D.bin
└── metadata.json
```

### 2. Camera Pose Estimation

#### Option A: Synthetic Poses (Recommended)
Since we control the generation process, we can use known camera positions:

```python
def create_synthetic_poses(num_views=200):
    poses = []
    
    # Main ring at deck level
    for i in range(144):  # Every 2.5 degrees
        angle = np.radians(i * 2.5)
        distance = 300  # meters from ship center
        height = 20     # meters above water
        
        pose = {
            'position': [
                distance * np.cos(angle),
                distance * np.sin(angle),
                height
            ],
            'look_at': [0, 0, 15],  # Ship center
            'up': [0, 0, 1]
        }
        poses.append(pose)
    
    # Elevated views
    # ... additional poses
    
    return poses
```

#### Option B: COLMAP Estimation
For cases where synthetic poses fail:

```bash
# Feature extraction
colmap feature_extractor \
    --database_path database.db \
    --image_path images/

# Feature matching
colmap exhaustive_matcher \
    --database_path database.db

# Sparse reconstruction
colmap mapper \
    --database_path database.db \
    --image_path images/ \
    --output_path sparse/
```

### 3. Validation Pipeline

#### A. Coverage Validation
```python
def validate_coverage(poses):
    """Ensure no large gaps in viewing angles"""
    angles = [get_azimuth(p) for p in poses]
    gaps = []
    
    for i in range(len(angles)-1):
        gap = angles[i+1] - angles[i]
        if gap > 15:  # degrees
            gaps.append((angles[i], angles[i+1]))
    
    return len(gaps) == 0, gaps
```

#### B. Scale Consistency
```python
def validate_scale_consistency(images, reference_length=251.0):
    """Check ship length consistency across views
    Bismarck length: 251 meters
    """
    lengths = []
    
    for img_path in images:
        ship_pixels = detect_ship_length(img_path)
        focal_length = get_focal_length(img_path)
        distance = get_camera_distance(img_path)
        
        # Calculate real-world length
        length = (ship_pixels * distance) / focal_length
        lengths.append(length)
    
    variance = np.std(lengths) / np.mean(lengths)
    return variance < 0.05  # 5% tolerance
```

#### C. Image Quality Checks
```python
def validate_image_quality(image_path):
    checks = {
        'resolution': check_resolution(image_path, min_size=1024),
        'sharpness': check_sharpness(image_path, threshold=0.7),
        'exposure': check_exposure(image_path),
        'ship_visible': check_ship_detection(image_path)
    }
    return all(checks.values()), checks
```

### 4. Dataset Augmentation (Optional)

For better 3DGS training:
- Add slight noise to perfect synthetic images
- Vary exposure/contrast slightly
- Add realistic atmospheric effects

```python
def augment_for_realism(image):
    # Add subtle noise
    noise = np.random.normal(0, 2, image.shape)
    image = np.clip(image + noise, 0, 255)
    
    # Slight exposure variation
    exposure = np.random.uniform(0.95, 1.05)
    image = np.clip(image * exposure, 0, 255)
    
    return image.astype(np.uint8)
```

### 5. Export Formats

#### COLMAP Format (Primary)
```python
def export_colmap_format(dataset_path, poses, intrinsics):
    # Create COLMAP binary files
    write_cameras_binary(poses, intrinsics)
    write_images_binary(image_list, poses)
    write_points3D_binary([])  # Empty for synthetic
```

#### NeRF Format (Alternative)
```python
def export_nerf_format(dataset_path, poses):
    transforms = {
        "camera_angle_x": FOV,
        "frames": []
    }
    
    for i, pose in enumerate(poses):
        transforms["frames"].append({
            "file_path": f"./images/view_{i:03d}",
            "transform_matrix": pose.tolist()
        })
    
    with open("transforms_train.json", "w") as f:
        json.dump(transforms, f, indent=2)
```

## 🧪 Validation Checklist

- [ ] All images have consistent resolution
- [ ] Camera poses cover 360° with no large gaps
- [ ] Ship scale consistent across views (±5%)
- [ ] Technical drawing proportions maintained
- [ ] No duplicate or near-duplicate views
- [ ] Lighting consistency across dataset
- [ ] File naming convention correct
- [ ] Metadata complete and accurate

## 🛠️ Tools Required

- **COLMAP**: Camera pose estimation
- **OpenCV**: Image processing and validation
- **NumPy**: Numerical operations
- **Pillow**: Image I/O
- **Custom Scripts**: Validation and formatting

## ⚠️ Common Issues

### Problem: COLMAP fails to find poses
**Solution**: Use synthetic poses with known camera positions

### Problem: Scale drift across views  
**Solution**: Add scale constraints using technical drawings

### Problem: Inconsistent lighting
**Solution**: Normalize images or regenerate with fixed lighting

## 📊 Quality Metrics

Target metrics for dataset:
- **Coverage**: <10° maximum gap between views
- **Consistency**: <5% scale variation
- **Quality**: >95% images pass all checks
- **Completeness**: 200+ validated views

## 🚀 Next Steps

Once dataset is prepared and validated:
1. Copy to 03-3dgs-training workspace
2. Verify GPU memory for image resolution
3. Begin 3DGS training process