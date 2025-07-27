# VLM-Editing Workflow (Archived)

> **Note: This project is archived and not in active development.** The concepts and code within are from an exploratory phase and are not currently maintained.

This folder contains the original vision for a VLM-driven 3D editing pipeline where:

1. A Vision Language Model (VLM) analyzes 3D scenes
2. Outputs structured JSON commands with precise 3D coordinates
3. Commands execute in Blender to modify geometry

## Key Components

- **src/**: Volume selection and tool execution code
- **schema/**: JSON schema for structured tool calls
- **tests/**: Test pipeline for validating commands
- **docs/**: Original architecture and implementation plans

## Archived Status & Rationale

This workflow is currently **archived** as we focus on the more immediate goal of synthetic image → 3DGS reconstruction for battleships. The VLM editing approach remains a potential future enhancement once we have:

1. Proven the 3DGS reconstruction pipeline
2. Developed a library of high-quality 3D models
3. Access to spatial-aware VLMs that can output precise 3D coordinates

The core innovation of volume-based selection (selecting geometry within 3D boxes/spheres) could still be valuable for the splat refinement phase of our current pipeline.

## Future Vision & Potential Features

Should this project be revived, a production-ready implementation would need to address several key areas. The following is a conceptual roadmap of features that would be required to build a robust system:

-   **Comprehensive Blender API:** A deeper and more abstract API layer for complex scene manipulations, including material/shader editing, lighting adjustments (adding/removing lights, changing properties), and camera controls.
-   **Procedural Generation:** Support for procedural scene generation based on high-level VLM commands (e.g., "create a forest scene," "build a modern cityscape").
-   **Robust Workflow Automation:**
    -   **Error Handling:** Implement comprehensive error handling and transaction-like rollbacks for failed Blender operations.
    -   **Batch Processing:** Add support for processing multiple scenes or command lists sequentially.
    -   **Performance Monitoring:** Integrate tools to monitor and log performance metrics for Blender operations and rendering.
-   **Developer & User Experience:**
    -   **Plugin System:** Create a plugin architecture to allow for custom tools, selection methods, and VLM integrations.
    -   **Testing Framework:** Develop an automated testing suite specifically for the Blender control modules to validate scene changes.
    -   **Configuration & Monitoring UI:** A user-friendly interface for configuring VLM endpoints, managing job queues, and monitoring workflow execution.
-   **Advanced Capabilities:**
    -   **Real-time Preview:** A mechanism for efficient data streaming between the VLM and Blender to enable near real-time visualization of proposed changes.
    -   **Version Control:** Integration with systems like Git LFS for versioning Blender scene files (`.blend`) and tracking changes programmatically.
