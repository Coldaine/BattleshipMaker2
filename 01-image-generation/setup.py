#!/usr/bin/env python3
"""
Setup script for cloud-based image generation pipeline
"""

import os
import subprocess
import sys

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_directories():
    """Create necessary directories"""
    dirs = [
        "generated_images",
        "generated_images/test",
        "generated_images/production",
        "prompts",
        "metadata"
    ]
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("Directories created successfully")

def create_env_template():
    """Create .env template for API keys"""
    env_content = """# Google API Key for Gemini
GOOGLE_API_KEY=your_api_key_here

# Optional: OpenAI API Key for DALL-E
OPENAI_API_KEY=your_openai_key_here

# Optional: Stability AI API Key
STABILITY_API_KEY=your_stability_key_here
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    print("Created .env.template file")

def main():
    """Main setup function"""
    print("Setting up cloud-based image generation pipeline...")
    
    try:
        install_dependencies()
        setup_directories()
        create_env_template()
        print("\nSetup complete! Next steps:")
        print("1. Copy .env.template to .env and add your API keys")
        print("2. Run: python main.py --batch-name test_batch --num-images 25")
        print("3. Check generated_images/ for your dataset")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()