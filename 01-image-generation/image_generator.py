
import os
import json
import time
import logging
from pathlib import Path
from itertools import product
from PIL import Image, ImageDraw, ImageFont

from config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageGenerator:
    """Generates images based on systematic prompts and camera poses."""

    def __init__(self):
        self.config = config
        self.model_name = self.config.get('generation_model.name')
        self.output_base_dir = Path(self.config.get('output_settings.base_dir'))

    def _create_placeholder_image(self, text, path):
        """Creates a placeholder image with text, simulating a real API call."""
        try:
            img = Image.new('RGB', (self.config.get('image_settings.width'), self.config.get('image_settings.height')), color = '#333')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 15)
            except IOError:
                font = ImageFont.load_default()
            draw.text((10, 10), text, fill=(255, 255, 255), font=font)
            img.save(path)
            logging.info(f"Successfully created placeholder image: {path}")
            return True
        except Exception as e:
            logging.error(f"Failed to create placeholder image at {path}: {e}")
            return False

    def _generate_prompt(self, camera_distance, camera_height, camera_angle):
        """Generates a detailed, structured prompt for image generation."""
        style = self.config.get('prompt_engineering.style')
        negative = self.config.get('prompt_engineering.negative')
        return (
            f"A photorealistic image of the German battleship Bismarck. "
            f"Style: {style}. Negative keywords: {negative}. "
            f"Camera: distance={camera_distance}m, height={camera_height}m, angle={camera_angle}deg."
        )

    def generate_image(self, prompt, metadata, output_path):
        """Simulates generating a single image and saving it with metadata."""
        image_path = output_path.with_suffix('.png')
        metadata_path = output_path.with_suffix('.json')

        # Simulate API call and save image
        success = self._create_placeholder_image(prompt, image_path)
        if not success:
            return False

        # Save metadata
        try:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            logging.info(f"Successfully saved metadata: {metadata_path}")
            return True
        except IOError as e:
            logging.error(f"Failed to save metadata at {metadata_path}: {e}")
            return False

    def run_batch_generation(self, batch_name, num_images):
        """Generates a batch of images with systematic camera poses."""
        batch_dir = self.output_base_dir / batch_name
        batch_dir.mkdir(parents=True, exist_ok=True)

        distances = self.config.get('camera_poses.distances')
        heights = self.config.get('camera_poses.heights')
        angles = self.config.get('camera_poses.angles')

        # Create all possible camera pose combinations
        all_poses = list(product(distances, heights, angles))
        poses_to_generate = all_poses[:num_images]

        logging.info(f"Starting batch '{batch_name}' to generate {len(poses_to_generate)} images.")

        for i, (dist, h, angle) in enumerate(poses_to_generate):
            prompt = self._generate_prompt(dist, h, angle)
            output_prefix = f"{self.config.get('output_settings.prefix')}_{i:04d}"
            output_path = batch_dir / output_prefix

            metadata = {
                "batch_name": batch_name,
                "image_index": i,
                "model_name": self.model_name,
                "timestamp": time.time(),
                "prompt": prompt,
                "camera_settings": {"distance": dist, "height": h, "angle": angle}
            }

            self.generate_image(prompt, metadata, output_path)

        logging.info(f"Batch '{batch_name}' complete.")
