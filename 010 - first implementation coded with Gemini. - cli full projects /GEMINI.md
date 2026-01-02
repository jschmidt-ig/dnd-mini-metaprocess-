# AI 3D D&D Colorizer

This project aims to use AI to automate the process of colorizing 3D STL models for printing on a Bambu Labs X1C with a 4-color AMS system.

## Project Goals

1.  **Creative Concepting:** Generate multiple high-quality preview images showing how a 3D model (STL) could look when painted with 4 colors.
2.  **3D Colorization:** Automatically generate a 3MF file from an STL, assigning colors to different parts of the mesh based on the creative concept.
3.  **Process Automation:** Minimize manual effort in complex 3D software (like Blender or CAD tools) by using CLI-based tools or AI-driven automation.

## Technical Context

-   **Printer:** Bambu Labs X1C
-   **System:** 4-color AMS (Automated Material System)
-   **Nozzles:** 0.2mm and 0.4mm
-   **OS:** macOS (darwin)
-   **Primary Inputs:** STL files (located in project subdirectories like `./capri`).
-   **Primary Outputs:** 
    -   Rendered previews (images).
    -   Color-mapped 3MF files compatible with Bambu Studio.

## Workflow

1.  **Input:** Locate the target STL file (e.g., `capri/model.stl`).
2.  **Visualization:** Use AI image generation tools (like `generate_image`) to create conceptual renders of the model with 4 distinct colors.
3.  **Analysis & Segmentation:** (To be implemented) Analyze the STL mesh to identify logical parts for coloring.
4.  **Generation:** Create a `.3mf` file that contains the original geometry but with 4-color assignments suitable for the Bambu AMS.
5.  **Verification:** Provide the 3MF and previews to the user for loading into Bambu Studio.

## AI Agent Instructions

-   **Image Generation:** Use the `generate_image` tool to create previews. Focus on "miniature painting style" and "4-color palette" in prompts.
-   **3D Tools:** Prefer CLI tools like `trimesh` (Python), `OpenSCAD`, or `Blender` (headless) for mesh manipulation and 3MF generation.
-   **Bambu Compatibility:** Ensure 3MF files are structured specifically for Bambu Studio's AMS mapping.
-   **Exploration:** If a step requires a new tool, proactively search for and install macOS-compatible CLI utilities.
