#!/usr/bin/env python3
"""
Krypton NAS - Multi-Color 3MF Export Pipeline

Generates the FreeCAD model, assigns per-body colors from spec.json,
and exports a single multi-color 3MF plus individual STLs.

Run via FreeCAD headless:
  /Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('pipeline/export_3mf.py').read())"
"""

import json
import os
import sys
import time

# Resolve paths relative to project root (one level up from pipeline/)
script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
if os.path.basename(script_dir) == 'pipeline':
    project_root = os.path.dirname(script_dir)
else:
    project_root = script_dir

spec_path = os.path.join(project_root, '.state', 'spec.json')
model_script = os.path.join(project_root, 'krypton_nas_panels.py')
output_dir = os.path.join(project_root, 'output')
stl_dir = os.path.join(project_root, 'stl')

ts = str(int(time.time()))
print("")
print("=" * 60)
print("  KRYPTON NAS - MULTI-COLOR 3MF EXPORT")
print("  Build " + ts)
print("=" * 60)

# --------------------------------------------------
# 1. Load spec.json
# --------------------------------------------------
print("\n[1/5] Loading spec.json ...")
with open(spec_path, 'r') as f:
    spec = json.load(f)

colors = spec['colors']
components = spec['components']
print("  Loaded " + str(len(components)) + " components, " + str(len(colors)) + " colors")

# --------------------------------------------------
# 2. Generate model by running krypton_nas_panels.py
# --------------------------------------------------
print("\n[2/5] Generating FreeCAD model ...")
exec(open(model_script).read())

import FreeCAD
import Import
import Mesh
import Part

doc = FreeCAD.ActiveDocument
if doc is None:
    print("  ERROR: No active document after model generation")
    sys.exit(1)

print("  Document: " + doc.Name)
print("  Objects: " + str(len(doc.Objects)))

# --------------------------------------------------
# 3. Assign colors per component from spec
# --------------------------------------------------
print("\n[3/5] Assigning colors ...")

def hex_to_rgb_tuple(hex_str):
    """Convert '#RRGGBB' to (R/255, G/255, B/255, 0.0) tuple for FreeCAD."""
    h = hex_str.lstrip('#')
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return (r, g, b, 0.0)

colored_objects = []
for comp in components:
    obj_name = comp['freecad_object']
    color_name = comp['color']
    obj = doc.getObject(obj_name)
    if obj is None:
        print("  WARNING: Object '" + obj_name + "' not found, skipping")
        continue
    if color_name not in colors:
        print("  WARNING: Color '" + color_name + "' not in palette, skipping")
        continue

    color_hex = colors[color_name]['hex']
    rgb = hex_to_rgb_tuple(color_hex)

    if hasattr(obj, 'ViewObject') and obj.ViewObject is not None:
        obj.ViewObject.ShapeColor = rgb
        print("  " + obj_name + " -> " + color_name + " (" + color_hex + ")")
    else:
        print("  " + obj_name + " -> " + color_name + " (no ViewObject, color metadata only)")

    colored_objects.append(obj)

doc.recompute()

# --------------------------------------------------
# 4. Export multi-color 3MF
# --------------------------------------------------
print("\n[4/5] Exporting multi-color 3MF ...")
os.makedirs(output_dir, exist_ok=True)

threemf_path = os.path.join(output_dir, 'KryptonNAS_multicolor.3mf')
try:
    Import.export(colored_objects, threemf_path)
    size_kb = os.path.getsize(threemf_path) / 1024.0
    print("  Exported: " + threemf_path)
    print("  Size: " + str(round(size_kb, 1)) + " KB")
except Exception as e:
    print("  ERROR exporting 3MF: " + str(e))
    print("  Trying fallback with Mesh export ...")
    # Fallback: export as mesh-based 3MF
    try:
        meshes = []
        for obj in colored_objects:
            if hasattr(obj, 'Shape'):
                mesh = Mesh.Mesh(obj.Shape.tessellate(0.1))
                meshes.append(mesh)
        if meshes:
            combined = meshes[0]
            for m in meshes[1:]:
                combined.addMesh(m)
            combined.write(threemf_path)
            print("  Fallback export succeeded: " + threemf_path)
    except Exception as e2:
        print("  Fallback also failed: " + str(e2))

# --------------------------------------------------
# 5. Export individual STLs
# --------------------------------------------------
print("\n[5/5] Exporting individual STLs ...")
os.makedirs(stl_dir, exist_ok=True)

for comp in components:
    obj_name = comp['freecad_object']
    stl_filename = os.path.basename(comp['stl'])
    stl_path = os.path.join(stl_dir, stl_filename)

    obj = doc.getObject(obj_name)
    if obj is None or not hasattr(obj, 'Shape'):
        print("  SKIP: " + obj_name + " (no shape)")
        continue

    try:
        mesh = Mesh.Mesh(obj.Shape.tessellate(0.1))
        mesh.write(stl_path)
        size_kb = os.path.getsize(stl_path) / 1024.0
        print("  " + stl_filename + " (" + str(round(size_kb, 1)) + " KB)")
    except Exception as e:
        print("  ERROR: " + stl_filename + " - " + str(e))

# Also export integrated shell (shell + mounts fused)
print("\n  Exporting MainShell_Integrated.stl ...")
shell = doc.getObject('MainShell')
ssd = doc.getObject('SSD_ClampMount')
eth = doc.getObject('Ethernet_ClampMount')
pi5 = doc.getObject('Pi5_Mount')

if shell and ssd and eth and pi5:
    try:
        fused = shell.Shape.fuse([ssd.Shape, eth.Shape, pi5.Shape])
        mesh = Mesh.Mesh(fused.tessellate(0.1))
        integrated_path = os.path.join(stl_dir, 'MainShell_Integrated.stl')
        mesh.write(integrated_path)
        size_kb = os.path.getsize(integrated_path) / 1024.0
        print("  MainShell_Integrated.stl (" + str(round(size_kb, 1)) + " KB)")
    except Exception as e:
        print("  ERROR fusing shell: " + str(e))

print("\n" + "=" * 60)
print("  BUILD COMPLETE")
print("=" * 60)
