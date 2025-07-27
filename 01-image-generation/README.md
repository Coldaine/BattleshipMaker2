# Image Generation Pipeline - Technical Drawing Integration

## 🎯 Objective
Create consistent multi-view synthetic images of the Bismarck battleship using AI image generation constrained by historical technical drawings for dimensional accuracy.

## 📐 Technical Drawing Resources

### Essential Bismarck References
1. **Anatomy of the Ship: The Battleship Bismarck** (Jack Brower)
   - Complete technical drawings
   - Cross-sections every 10 meters
   - Detailed superstructure plans

2. **Kagero Super Drawings 3D**
   - 3D reconstructions with measurements
   - Detail closeups of complex areas

3. **Original Blueprints** (Bundesarchiv)
   - Construction drawings from Blohm & Voss
   - As-built modifications

### Drawing Types Needed
- **General Arrangements**: Overall layout
- **Lines Plans**: Hull shape definition  
- **Armor Diagrams**: Thickness and angles
- **Machinery Spaces**: Internal structure
- **Weapons Layout**: Turret and gun positions

## 📊 Model Comparison Matrix

### **1. DALL-E 3 (OpenAI)**
**Pros:**
- Excellent prompt following
- Good geometric understanding
- API access for automation
- Consistent style within batches

**Cons:**
- Limited control over camera angles
- No fine-tuning capability
- Cost per image
- May struggle with exact view consistency

**Best For:** Initial prototyping, reference generation

### **2. Midjourney v6**
**Pros:**
- Highest photorealistic quality
- Good historical accuracy
- Strong community with naval enthusiasts
- --cref (character reference) for consistency

**Cons:**
- Discord-based, harder to automate
- Limited camera control
- Expensive for hundreds of images
- Manual process

**Best For:** High-quality reference images, hero shots

### **3. Flux (Black Forest Labs)**
**Pros:**
- Open weights available
- Good prompt adherence
- Can run locally on 5090
- ControlNet compatible

**Cons:**
- Newer, less proven for consistency
- May need prompt engineering
- Local compute time

**Best For:** Bulk generation with control

### **4. Stable Diffusion XL + ControlNet**
**Pros:**
- Complete local control
- ControlNet for precise camera angles
- Can use depth/normal maps for consistency
- Free after setup
- Custom LoRA training possible

**Cons:**
- Requires technical setup
- May need custom training
- Quality varies with checkpoint

**Best For:** Full pipeline control

## 🔧 Proposed Hybrid Approach

### **Phase 1: Reference Collection**
1. **Midjourney**: Generate 10-20 high-quality Bismarck references
   - Different angles but same lighting/style
   - Use --cref for consistency
   - Focus on historical accuracy

2. **Historical References**: Collect real Bismarck photos/blueprints
   - Side profiles
   - Deck plans
   - Detail shots

### **Phase 2: Consistency Testing**
Test each model's ability to maintain consistency:

```python
# Consistency test prompts
test_angles = [
    (0, 15),    # Front quarter
    (45, 15),   # Side quarter
    (90, 15),   # Pure side
    (180, 15),  # Rear
]

consistency_prompt = """
Battleship Bismarck, German WW2, 1941 configuration,
aerial view at {azimuth} degrees azimuth, {elevation} degrees elevation,
consistent lighting, overcast sky, gray ocean,
photorealistic, historical accuracy
"""
```

### **Phase 3: Production Pipeline**

**Technical Drawing-Constrained Generation**
```python
class BismarckViewGenerator:
    def __init__(self):
        self.base_model = "SDXL_military_vehicles_checkpoint"
        self.controlnets = [
            "depth_controlnet_v11",
            "canny_controlnet_v11",
            "lineart_controlnet_v11"
        ]
        self.technical_drawings = self.load_drawings()
        
    def generate_view_ring(self, angle):
        # 1. Render depth map from 3D proxy at angle
        depth_map = self.render_proxy_depth(angle)
        
        # 2. Project technical drawing to current view
        line_art = self.project_drawing_to_view(angle)
        
        # 3. Multi-ControlNet generation
        controls = {
            "depth": depth_map,
            "canny": line_art,
            "reference": self.reference_style
        }
        
        # 4. Generate with dimensional constraints
        image = self.generate_with_controls(controls)
        
        # 5. Validate proportions
        if not self.validate_proportions(image, angle):
            return self.regenerate_with_adjustments(angle)
            
        return image
```

**Option B: Flux API + Post-Selection**
```python
class FluxBismarckGenerator:
    def generate_with_oversampling(self):
        # Generate 3x needed views
        # Use CLIP similarity to select most consistent set
        # LLM-based quality filtering
```

## 📐 Camera Configuration for 3DGS

### **Optimal View Distribution**
```python
def generate_camera_positions():
    views = []
    
    # Ring at deck level
    for azimuth in range(0, 360, 5):  # 72 views
        views.append({"azimuth": azimuth, "elevation": 0})
    
    # Elevated rings
    for elevation in [15, 30, 45]:
        for azimuth in range(0, 360, 10):  # 36 views each
            views.append({"azimuth": azimuth, "elevation": elevation})
    
    # Top-down views
    for azimuth in range(0, 360, 30):  # 12 views
        views.append({"azimuth": azimuth, "elevation": 75})
    
    return views  # Total: ~200 views
```

## 🧪 Consistency Evaluation Metrics

### **1. Geometric Consistency**
- Ship length/beam ratio constant
- Turret positions match
- Superstructure alignment

### **2. Appearance Consistency**
- Lighting direction
- Color palette (gray hull, deck color)
- Detail level

### **3. 3DGS Compatibility**
- No missing angles
- Overlapping coverage
- Consistent scale

## 🚀 Technical Drawing Integration Workflow

### Step 1: Collect Technical Drawings
**Sources**:
- Naval archive blueprints
- Jane's Fighting Ships diagrams
- Anatomy of the Ship series
- Model builder reference books

**Required Views**:
1. **Profile (Side)**: Full length elevation
2. **Plan (Top)**: Deck arrangements
3. **Sections**: Cross-sections at key points
4. **Details**: Turret configurations, bridge structure

### Step 2: Process Drawings for ControlNet
```python
def process_technical_drawing(image_path):
    # 1. Load and clean drawing
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Extract clean lines
    edges = cv2.Canny(gray, 50, 150)
    
    # 3. Optional: Thin lines for cleaner input
    kernel = np.ones((2,2), np.uint8)
    thinned = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    return thinned
```

### Step 3: Multi-Layer ControlNet Setup
```yaml
ControlNet Configuration:
  Layer 1 - Depth:
    source: 3D_proxy_render
    weight: 0.7
    control_mode: depth
    
  Layer 2 - LineArt:
    source: technical_drawing
    weight: 0.9
    control_mode: canny
    
  Layer 3 - Composition:
    source: reference_photo
    weight: 0.3
    control_mode: reference
```

### Step 4: Generate Test Views
1. **Canonical views first** (matching technical drawings)
2. **Interpolated angles** (between canonical views)
3. **Validate proportions** against blueprints

## 💡 Key Decisions Needed

1. **Quality vs Speed**: Do we prioritize perfect consistency (SDXL+ControlNet) or faster iteration (Flux/DALL-E)?

2. **Automation Level**: Full automation with APIs or semi-manual with quality control?

3. **Training Custom Model**: Worth training a Bismarck-specific LoRA/Dreambooth model?

4. **Backup Plans**: What if first approach fails? Should we prepare multiple pipelines?

## 📝 Next Steps

1. Set up ComfyUI with military vehicle checkpoints
2. Create basic 3D proxy of Bismarck for depth maps
3. Run consistency tests with 20-view sample
4. Decide on production approach based on results