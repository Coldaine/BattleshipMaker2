#!/usr/bin/env python3
"""
Main entry point for cloud-based image generation pipeline
"""

import argparse
import json
import sys
from pathlib import Path

from image_generator import BismarckImageGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate Bismarck battleship images for 3DGS training")
    parser.add_argument("--batch-name", default="test_batch", help="Name for this batch")
    parser.add_argument("--num-images", type=int, default=25, help="Number of images to generate")
    parser.add_argument("--validate-only", action="store_true", help="Only validate existing dataset")
    parser.add_argument("--output-dir", default="generated_images", help="Output directory")
    
    args = parser.parse_args()
    
    generator = BismarckImageGenerator()
    
    if args.validate_only:
        # Validate existing dataset
        validation = generator.validate_dataset(args.output_dir)
        print("Validation Results:")
        print(json.dumps(validation, indent=2))
    else:
        # Generate new batch
        print(f"Generating {args.num_images} images for batch: {args.batch_name}")
        results = generator.generate_batch(args.batch_name, args.num_images)
        print(f"Generated {results['successful']}/{results['total_images']} images")
        
        # Validate the new dataset
        validation = generator.validate_dataset(f"{args.output_dir}/{args.batch_name}")
        print("Dataset validation complete")

if __name__ == "__main__":
    main()