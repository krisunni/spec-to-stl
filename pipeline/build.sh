#!/bin/bash
# Multi-Project Build Pipeline
# Generates models, assigns colors, exports 3MF + STLs for all projects
#
# Usage: ./pipeline/build.sh

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FREECAD="/Applications/FreeCAD.app/Contents/MacOS/FreeCAD"

echo "========================================"
echo "  Spec-to-STL Build Pipeline"
echo "========================================"
echo ""

# Check FreeCAD
if [ ! -f "$FREECAD" ]; then
    echo "ERROR: FreeCAD not found at $FREECAD"
    echo "Install FreeCAD or update the path in this script."
    exit 1
fi

# Check spec.json
if [ ! -f "$DIR/.state/spec.json" ]; then
    echo "ERROR: .state/spec.json not found"
    exit 1
fi

echo "Project: $DIR"
echo "FreeCAD: $FREECAD"
echo ""

# Create STL subdirectories
mkdir -p "$DIR/stl/krypton-nas"
mkdir -p "$DIR/stl/headband-spacer"
mkdir -p "$DIR/stl/headphone-stand"
mkdir -p "$DIR/output"

# Run the export pipeline
cd "$DIR"
"$FREECAD" -c "exec(open('pipeline/export_3mf.py').read())"

echo ""
echo "Output files:"
echo "  3MF:  output/*.3mf"
echo "  STLs: stl/krypton-nas/*.stl"
echo "  STLs: stl/headband-spacer/*.stl"
echo "  STLs: stl/headphone-stand/*.stl"
echo ""
echo "Done."
