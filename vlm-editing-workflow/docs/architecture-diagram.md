# Technical Architecture Diagram

## Current vs. Proposed Architecture

```mermaid
graph TB
    subgraph "CURRENT PIPELINE (Robust)"
        A[Image Input] --> B[VLM Analysis]
        B --> C[Structured tool_calls JSON]
        C --> D[Blender bpy API]
        D --> E[Mesh Operations]
        E --> F[3D Output]
    end

    subgraph "FLAWED PROPOSAL (Critiqued)"
        G[Image Input] --> H[VLM Analysis] 
        H --> I[Natural Language suggested_action]
        I --> J[NLP Parser - BRITTLE]
        J --> K[Blender Operations]
        K --> L[Output]
    end

    subgraph "CORRECTED ARCHITECTURE (Recommended)"
        M[Image Input] --> N[Future Spatial 3D-LLM]
        N --> O[Structured 3D Volume JSON]
        O --> P[Volume Selection Engine]
        P --> Q[Enhanced Tool Calls]
        Q --> R[Blender bpy API]
        R --> S[Mesh Operations]
        S --> T[3D Output]
    end
```

## Phase-by-Phase Implementation Flow

```mermaid
graph LR
    subgraph "Phase 1: Foundation"
        P1A[Analyze Current Pipeline] --> P1B[Design JSON Schema]
        P1B --> P1C[Build Volume Selection]  
        P1C --> P1D[Test Framework]
    end

    subgraph "Phase 2: 3DGS Integration"
        P2A[Photo Input] --> P2B[3DGS Training]
        P2B --> P2C[Splat to Mesh]
        P2C --> P2D[Existing Pipeline]
    end

    subgraph "Phase 3: Enhanced Tools"
        P3A[Volume-based Selection] --> P3B[New Tool Library]
        P3B --> P3C[Spatial Validation]
    end

    P1D --> P2A
    P2D --> P3A
```

## JSON Schema Evolution

### Before (Flawed)
```json
{
  "suggested_action": "Reshape the volume in the upper-left; apply 'Armored Steel Plate' texture."
}
```

### After (Corrected)
```json
{
  "tool_calls": [
    {
      "function_name": "extrude_faces_in_volume",
      "parameters": {
        "volume_identifier": {
          "type": "box",
          "center_xyz": [15.7, -3.2, 8.5],
          "dimensions_xyz": [4.5, 2.1, 3.0],
          "rotation_quaternion_wxyz": [0.966, 0.0, 0.259, 0.0]
        },
        "extrude_vector": [0.0, 0.0, 0.5]
      }
    },
    {
      "function_name": "apply_material_to_volume", 
      "parameters": {
        "volume_identifier": {
          "type": "box",
          "center_xyz": [15.7, -3.2, 8.5],
          "dimensions_xyz": [4.5, 2.1, 3.0]
        },
        "material_name": "Armored_Steel_Plate"
      }
    }
  ]
}
```

## Integration Strategy: Path A vs Path B

```mermaid
graph TB
    subgraph "Path A: Feasible (Immediate)"
        PA1[Multi-view Photos] --> PA2[3DGS Training]
        PA2 --> PA3[High-quality Splats]
        PA3 --> PA4[Mesh Conversion]
        PA4 --> PA5[Existing Mesh Pipeline]
        PA5 --> PA6[Refined 3D Model]
    end

    subgraph "Path B: Research Track (Long-term)"
        PB1[3DGS Scene] --> PB2[Direct Splat Editing]
        PB2 --> PB3[Splat-native Tools]
        PB3 --> PB4[Real-time Manipulation]
    end

    subgraph "Technical Challenges"
        TC1[Mesh vs Splat Divide]
        TC2[Point Cloud Topology]
        TC3[Real-time Constraints]
    end

    PA4 -.-> TC1
    PB2 -.-> TC2
    PB4 -.-> TC3
```

## Critical Fix: Volume-based Selection

```mermaid
graph LR
    subgraph "3D Volume Definition"
        VD1[center_xyz: 15.7, -3.2, 8.5]
        VD2[dimensions_xyz: 4.5, 2.1, 3.0] 
        VD3[rotation_quaternion_wxyz]
    end

    subgraph "Selection Algorithm"
        SA1[Transform to Local Space]
        SA2[Point-in-Box Test]
        SA3[Return Selected Vertices]
    end

    subgraph "Tool Execution"
        TE1[extrude_faces_in_volume]
        TE2[scale_vertices_in_volume]
        TE3[apply_material_to_volume]
    end

    VD1 --> SA1
    VD2 --> SA1  
    VD3 --> SA1
    SA1 --> SA2
    SA2 --> SA3
    SA3 --> TE1
    SA3 --> TE2
    SA3 --> TE3
```

## Risk Mitigation Architecture

```mermaid
graph TB
    subgraph "Input Validation"
        IV1[JSON Schema Validation]
        IV2[Coordinate Range Check]
        IV3[Volume Bounds Verification]
    end

    subgraph "Processing Safety"
        PS1[Spatial Index Optimization]
        PS2[Error Recovery]
        PS3[Fallback Mechanisms]
    end

    subgraph "Output Verification"
        OV1[Geometric Integrity Check]
        OV2[Performance Monitoring]
        OV3[Quality Metrics]
    end

    IV1 --> PS1
    IV2 --> PS2
    IV3 --> PS3
    PS1 --> OV1
    PS2 --> OV2
    PS3 --> OV3