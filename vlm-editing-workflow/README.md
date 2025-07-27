# VLM-Editing Workflow (Archived)

This folder contains the original vision for a VLM-driven 3D editing pipeline where:

1. A Vision Language Model (VLM) analyzes 3D scenes
2. Outputs structured JSON commands with precise 3D coordinates
3. Commands execute in Blender to modify geometry

## Key Components

- **src/**: Volume selection and tool execution code
- **schema/**: JSON schema for structured tool calls
- **tests/**: Test pipeline for validating commands
- **docs/**: Original architecture and implementation plans

## Status

This workflow is currently **archived** as we focus on the more immediate goal of synthetic image → 3DGS reconstruction for battleships. The VLM editing approach remains a potential future enhancement once we have:

1. Proven the 3DGS reconstruction pipeline
2. Developed a library of high-quality 3D models
3. Access to spatial-aware VLMs that can output precise 3D coordinates

The core innovation of volume-based selection (selecting geometry within 3D boxes/spheres) could still be valuable for the splat refinement phase of our current pipeline.