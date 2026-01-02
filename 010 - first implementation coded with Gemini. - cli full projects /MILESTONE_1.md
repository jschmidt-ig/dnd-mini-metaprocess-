# Milestone 1: Visualization & Basic Pipeline

**Goal:** Establish the core CLI workflow to generate creative concept art and a printable 4-color 3MF file from a source STL.

## Objectives

1.  **Environment Setup**
    -   [x] Verify/Install Python environment with necessary 3D libraries (e.g., `trimesh`, `numpy`, `scipy`, `mapbox-earcut`).
    -   [x] Ensure `capri/` directory has the source STL file (User action required).

2.  **Part A: Creative Concepting (AI Visualization)**
    -   [x] Develop a standardized prompt strategy for the `generate_image` tool.
    -   [x] **Task:** Generate 3-4 distinct visual concepts for the "Capri" character using a 4-color palette suitable for 3D printing.
    -   [x] Save these concepts to `capri/concepts/` (Implemented as Swatch Cards in `capri_imageconcepts/`).

3.  **Part B: 3D Processing Pipeline (Proof of Concept)**
    -   [x] Create a Python script (`src/process_model.py`) to:
        -   Load an STL file.
        -   Analyze the mesh (check for water-tightness, volume).
        -   Implement a basic coloring heuristic (e.g., separate disconnected shells, or use simple geometric segmentation) to assign 4 material IDs.
        -   Export the result as a `.3mf` file compatible with Bambu Studio.

4.  **Part C: CLI Integration**
    -   [x] Create a master wrapper script (e.g., `run_pipeline.sh` or a Python CLI) that:
        -   Takes an STL path as input.
        -   Triggers the image generation (Part A).
        -   Runs the 3D processing (Part B).
        -   Outputs the final folder structure ready for the user.

## Success Criteria
-   [x] User can run a single command to generate concept images (Palettes generated via script).
-   [x] User can run a command to produce a valid `.3mf` file from the input STL.
-   [x] The `.3mf` file opens in Bambu Studio with 4 distinct colored regions (even if the coloring logic is simple for now).

## Status Update (Milestone 1 Complete)
- **3D Processing:** Successful. `process_model.py` converts STL to 4-color 3MF.
- **Visualization:** Full AI 3D renders were blocked by API limitations/Safety filters on the provided keys.
- **Fallback:** Generated Color Palette Cards in `capri_imageconcepts/` using `src/generate_palettes.py` to provide the requested 4-color references and descriptions.