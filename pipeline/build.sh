#!/bin/bash
# Krypton NAS - One-Command Build Pipeline
# Generates model, assigns colors, exports 3MF + STLs
#
# Usage: ./pipeline/build.sh

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FREECAD="/Applications/FreeCAD.app/Contents/MacOS/FreeCAD"

echo "========================================"
echo "  Krypton NAS Build Pipeline"
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

# Run the export pipeline
cd "$DIR"
"$FREECAD" -c "exec(open('pipeline/export_3mf.py').read())"

echo ""
echo "Output files:"
echo "  3MF: output/KryptonNAS_multicolor.3mf"
echo "  STLs: stl/*.stl"
echo ""
echo "Done."
