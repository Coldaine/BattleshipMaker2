# Image Generation Prompt Engine

This tool generates a systematic set of prompts and metadata for creating a consistent image dataset of the Bismarck battleship. The output is designed to be used with a text-to-image generation model to create images suitable for 3D Gaussian Splatting (3DGS) training.

**Note:** This script *does not* generate images directly. It creates the structured prompts and camera pose metadata required for a separate image generation process.

## Features

-   **Systematic Prompt Generation**: Creates detailed prompts for consistent ship appearance across all images.
-   **Configurable Camera Poses**: Generates prompts for a 360° view of the subject with configurable distances, heights, and angles.
-   **Metadata Tracking**: Saves a JSON file for each generated prompt, containing the exact parameters used.
-   **Batch Processing**: CLI support for generating a specified number of prompts in a named batch.
-   **Dataset Validation**: A simple validation tool to check the diversity and coverage of camera poses in a generated batch.

## How It Works

The pipeline operates in two main stages:

1.  **Prompt Generation**: The `main.py` script is executed, which uses the `BismarckImageGenerator` class to generate a batch of text prompts and corresponding metadata files. These are saved in the `generated_images/` directory under a specified batch name.
2.  **Image Generation (Manual Step)**: The generated prompts must then be used with a separate text-to-image model (e.g., Midjourney, Stable Diffusion, or a future Gemini model with image generation capabilities) to produce the actual images.

## Setup and Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: A `setup.py` script is included for convenience, which runs this command.*

2.  **Configure API Keys**:
    This project is configured to use Google Gemini for future integration, but no API key is required for the current prompt-generation functionality. A `.env.template` is provided for forward-compatibility.

## Usage

### Generating a Batch of Prompts

To generate a new set of prompts, run `main.py` with the desired batch name and number of images.

```bash
python main.py --batch-name <your_batch_name> --num-images <number_of_prompts>
```

**Example:**

```bash
# Generate 50 prompts for a batch named "production_run_01"
python main.py --batch-name production_run_01 --num-images 50
```

The output will be saved in `generated_images/production_run_01/`.

### Validating a Dataset

The validation tool checks if a generated batch has sufficient variety in its camera poses for 3DGS training.

```bash
python main.py --validate-only --output-dir <path_to_batch>
```

**Example:**

```bash
# Validate the batch generated in the previous step
python main.py --validate-only --output-dir generated_images/production_run_01
```

## Configuration

The core parameters for prompt generation can be modified in `config.py`:

-   `camera_distances`: A list of camera distances from the ship (in meters).
-   `camera_heights`: A list of camera heights above the water (in meters).
-   `camera_angles`: A list of camera angles around the ship (in degrees).
-   `style_prompt`: The base art style description.
-   `negative_prompt`: Terms to exclude from the generation.
