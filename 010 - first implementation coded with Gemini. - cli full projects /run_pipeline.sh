#!/bin/bash
set -e

# Configuration
VENV_DIR=".venv"
PYTHON="$VENV_DIR/bin/python"
SCRIPT_DIR="src"
PROCESS_SCRIPT="$SCRIPT_DIR/process_model.py"

# Check arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_stl_path>"
    exit 1
fi

INPUT_STL="$1"
BASENAME=$(basename "$INPUT_STL" .stl)
DIRNAME=$(dirname "$INPUT_STL")
OUTPUT_3MF="$DIRNAME/${BASENAME}_colored.3mf"

# Check environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR. Please set it up first."
    exit 1
fi

# Step 1: Image Generation (Skipped)
echo "------------------------------------------------"
echo "Step 1: Creative Concepting"
echo "------------------------------------------------"
echo "Skipping AI image generation (API Key required)."
# TODO: Add generate_image call here when key is available.

# Step 2: 3D Processing
echo "------------------------------------------------"
echo "Step 2: 3D Processing & Colorization"
echo "------------------------------------------------"
echo "Processing $INPUT_STL -> $OUTPUT_3MF"

"$PYTHON" "$PROCESS_SCRIPT" "$INPUT_STL" "$OUTPUT_3MF"

echo "------------------------------------------------"
echo "Pipeline Complete!"
echo "Output saved to: $OUTPUT_3MF"
echo "------------------------------------------------"
