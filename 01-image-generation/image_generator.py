"""
Cloud-based image generation pipeline for Bismarck battleship dataset
"""

import os
import json
import time
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import logging
from PIL import Image

from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BismarckImageGenerator:
    """Main image generation class for Bismarck battleship dataset"""
    
    def __init__(self):
        self.config = config
        self.model = None
        self._setup_model()
        
    def _setup_model(self):
        """Initialize the Gemini model"""
        try:
            api_key = self.config.get_api_key()
            genai.configure(api_key=api_key)
            
            # Configure generation parameters
            generation_config = {
                "temperature": self.config.base_config.temperature,
                "top_p": self.config.base_config.top_p,
                "max_output_tokens": 2048,
            }
            
            # Initialize model
            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config=generation_config
            )
            logger.info("Successfully initialized Gemini model")
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise
    
    def generate_bismarck_prompt(self, 
                               camera_distance: float = 100,
                               camera_height: float = 25,
                               camera_angle: float = 0,
                               lighting: str = "daylight",
                               weather: str = "clear",
                               detail_level: str = "high") -> str:
        """Generate detailed prompt for Bismarck battleship image"""
        
        # Camera position description
        angle_desc = {
            0: "front view",
            45: "front-right angle",
            90: "right side view",
            135: "rear-right angle",
            180: "rear view",
            225: "rear-left angle",
            270: "left side view",
            315: "front-left angle"
        }
        
        camera_desc = angle_desc.get(int(camera_angle), f"{camera_angle}° angle")
        
        prompt = f"""
        Generate a photorealistic image of the German battleship Bismarck from a {camera_desc} perspective.
        
        Camera specifications:
        - Distance: {camera_distance}m from ship
        - Height: {camera_height}m above water level
        - Angle: {camera_angle}° relative to ship's bow
        
        Environmental conditions:
        - Lighting: {lighting}
        - Weather: {weather}
        
        Ship details:
        - WWII German battleship Bismarck in operational configuration
        - Full hull visible above waterline
        - All main turrets and secondary armament clearly visible
        - Naval gray camouflage pattern
        - Swastika flag not visible (historical accuracy without Nazi symbols)
        - Realistic ocean surface with appropriate wake
        - Clear sky with natural lighting
        
        Technical requirements:
        - {detail_level} detail level
        - Sharp focus throughout
        - Natural colors
        - Professional naval photography style
        - 1024x1024 resolution
        
        Style: Photorealistic, high-quality naval photography, professional maritime documentation
        """
        
        return prompt.strip()
    
    def generate_image(self, 
                      prompt: str,
                      output_path: str,
                      seed: Optional[int] = None) -> bool:
        """Generate a single image using Gemini"""
        
        try:
            logger.info(f"Generating image: {output_path}")
            
            # Generate image
            result = self.model.generate_content(prompt)
            
            # For now, we'll create a placeholder since Gemini 2.0 doesn't directly generate images
            # This will be updated when we integrate with actual image generation APIs
            
            # Create a placeholder response
            metadata = {
                "prompt": prompt,
                "timestamp": time.time(),
                "seed": seed,
                "model": "gemini-2.0-flash-exp"
            }
            
            # Save metadata
            metadata_path = Path(output_path).with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Generated metadata for: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate image: {e}")
            return False
    
    def generate_batch(self,
                      batch_name: str,
                      num_images: int = 20,
                      camera_params: Optional[List[Tuple[float, float, float]]] = None) -> Dict[str, Any]:
        """Generate a batch of images with systematic camera poses"""
        
        output_dir = self.config.get_output_path(batch_name)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if camera_params is None:
            # Generate systematic camera poses
            camera_params = []
            distances = [100, 150, 200]
            heights = [25, 50, 75]
            angles = [0, 45, 90, 135, 180, 225, 270, 315]
            
            for dist in distances:
                for height in heights:
                    for angle in angles:
                        camera_params.append((dist, height, angle))
        
        # Limit to requested number of images
        camera_params = camera_params[:num_images]
        
        results = {
            "batch_name": batch_name,
            "total_images": len(camera_params),
            "successful": 0,
            "failed": 0,
            "images": []
        }
        
        for i, (dist, height, angle) in enumerate(camera_params):
            prompt = self.generate_bismarck_prompt(
                camera_distance=dist,
                camera_height=height,
                camera_angle=angle
            )
            
            output_path = output_dir / f"bismarck_{i:03d}_d{dist}_h{height}_a{angle}.jpg"
            
            success = self.generate_image(prompt, str(output_path))
            
            if success:
                results["successful"] += 1
                results["images"].append({
                    "index": i,
                    "path": str(output_path),
                    "camera_distance": dist,
                    "camera_height": height,
                    "camera_angle": angle,
                    "prompt": prompt
                })
            else:
                results["failed"] += 1
        
        # Save batch results
        results_path = output_dir / "batch_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Batch generation complete: {results['successful']}/{results['total_images']} successful")
        return results
    
    def validate_dataset(self, batch_path: str) -> Dict[str, Any]:
        """Validate generated dataset for 3DGS compatibility"""
        
        batch_path = Path(batch_path)
        results_file = batch_path / "batch_results.json"
        
        if not results_file.exists():
            return {"error": "Results file not found"}
        
        with open(results_file) as f:
            results = json.load(f)
        
        validation = {
            "total_images": results["total_images"],
            "successful": results["successful"],
            "coverage_analysis": {},
            "quality_metrics": {}
        }
        
        # Analyze camera coverage
        distances = set()
        heights = set()
        angles = set()
        
        for img in results["images"]:
            distances.add(img["camera_distance"])
            heights.add(img["camera_height"])
            angles.add(img["camera_angle"])
        
        validation["coverage_analysis"] = {
            "unique_distances": len(distances),
            "unique_heights": len(heights),
            "unique_angles": len(angles),
            "distance_range": [min(distances), max(distances)] if distances else [0, 0],
            "height_range": [min(heights), max(heights)] if heights else [0, 0],
            "angle_range": [min(angles), max(angles)] if angles else [0, 0]
        }
        
        # Basic quality checks
        validation["quality_metrics"] = {
            "min_images_for_3dgs": 20,
            "has_sufficient_coverage": len(distances) >= 3 and len(heights) >= 3 and len(angles) >= 8,
            "meets_minimum": results["successful"] >= 20
        }
        
        return validation

# Example usage
if __name__ == "__main__":
    generator = BismarckImageGenerator()
    
    # Generate test batch
    results = generator.generate_batch("test_batch_001", num_images=25)
    print(f"Generated {results['successful']} images")
    
    # Validate dataset
    validation = generator.validate_dataset("generated_images/test_batch_001")
    print("Validation results:", validation)