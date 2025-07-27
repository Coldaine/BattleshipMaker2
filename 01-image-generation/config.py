"""
Configuration for cloud-based image generation pipeline
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class GenerationConfig:
    """Configuration for image generation parameters"""
    
    # Model settings
    model_name: str = "gemini-2.5-pro"
    api_key: Optional[str] = None
    
    # Image settings
    width: int = 1024
    height: int = 1024
    quality: str = "high"  # high, medium, low
    
    # Generation settings
    num_images: int = 1
    temperature: float = 0.7
    top_p: float = 0.9
    
    # Output settings
    output_dir: str = "generated_images"
    prefix: str = "bismarck"
    
    # Camera pose settings
    camera_distances: Optional[List[float]] = None
    camera_heights: Optional[List[float]] = None
    camera_angles: Optional[List[float]] = None
    
    # Prompt settings
    style_prompt: str = "photorealistic, high detail, naval architecture"
    negative_prompt: str = "cartoon, anime, low quality, blurry"
    
    def __post_init__(self):
        if self.camera_distances is None:
            self.camera_distances = [50, 100, 150, 200, 300]  # meters
        if self.camera_heights is None:
            self.camera_heights = [10, 25, 50, 75, 100]  # meters
        if self.camera_angles is None:
            self.camera_angles = [0, 45, 90, 135, 180, 225, 270, 315]  # degrees

class ImageGenerationConfig:
    """Main configuration class for image generation pipeline"""
    
    def __init__(self):
        self.base_config = GenerationConfig()
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories"""
        dirs = [
            "generated_images",
            "generated_images/test",
            "generated_images/production",
            "generated_images/validation",
            "prompts",
            "metadata"
        ]
        
        for dir_name in dirs:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
    
    def get_api_key(self) -> str:
        """Get API key from environment or config"""
        api_key = os.getenv("GOOGLE_API_KEY") or self.base_config.api_key
        if not api_key:
            raise ValueError("Google API key not found. Set GOOGLE_API_KEY environment variable.")
        return api_key
    
    def get_output_path(self, batch_name: str = "test") -> Path:
        """Get output path for a specific batch"""
        return Path(self.base_config.output_dir) / batch_name
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary"""
        return {
            "model": self.base_config.model_name,
            "dimensions": [self.base_config.width, self.base_config.height],
            "quality": self.base_config.quality,
            "style": self.base_config.style_prompt,
            "negative": self.base_config.negative_prompt,
            "camera_settings": {
                "distances": self.base_config.camera_distances,
                "heights": self.base_config.camera_heights,
                "angles": self.base_config.camera_angles
            }
        }

# Global config instance
config = ImageGenerationConfig()