# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"Krypton NAS" - 3D printable Raspberry Pi 5 NAS enclosure with DC Comics Krypton/Fortress of Solitude theme. Tapered tower design with passive thermal management, removable magnetic panels, and tool-free component mounting. Two implementations: FreeCAD Python (primary) and OpenSCAD (original).

## Running the Scripts

```bash
# Generate 3D model (headless)
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('krypton_nas_panels.py').read())"

# In FreeCAD Python console (interactive)
exec(open('/Users/kris/Code/case/krypton_nas_panels.py').read())

# Multi-color 3MF + STL export pipeline
./pipeline/build.sh

# Dashboard
./serve.sh [port]  # default 8080, then open http://localhost:8080/dashboard/
```

**Important:** FreeCAD's Python console defaults to ASCII encoding. All `.py` files must be pure ASCII (no Unicode arrows, symbols, etc.) or the `exec(open(...).read())` pattern will fail.

## FreeCAD Python Architecture (krypton_nas_panels.py)

### Coordinate System
- Standard XYZ, Z-up. X=width (140mm), Y=depth (100mm), Z=height (160mm)
- Taper: top is 85% of base dimensions (119x85mm at z=160)
- `get_taper_at_height(z)` computes scale factor at any height

### Geometry Approach
- **Tapered shapes:** `Part.makeLoft([base_wire, top_wire], True)` - wires MUST be closed (repeat first point)
- **Subtractive features:** `shape.cut(geometry)` for all openings, recesses, cutouts
- **Document pattern:** Creates/reuses doc named `KryptonNAS_AllPanels`, adds `Part::Feature` objects

### 8 Objects Created

| Object | Z Position | Purpose |
|--------|------------|---------|
| `MainShell` | 0-160mm | Case body with panel openings + 24 magnet recesses |
| `SSD_ClampMount` | z=3mm | Snap-in rails for UGREEN M.2 (125x41x14mm) |
| `Ethernet_ClampMount` | z=35mm | U-cradle for UGREEN USB-C (62x25x15mm) |
| `Pi5_Mount` | z=65mm | 4 corner posts, M2.5 holes, board at z=73mm |
| `FrontPanel_CrystalBurst` | 15-135mm | Radial diamond pattern |
| `RearPanel_FortressGate` | 15-135mm | Hex matrix + crystal slot vents + RJ45 cutout |
| `LeftPanel_ShieldArray` | 15-135mm | Shield tessellation + USB-C/HDMI/Ethernet cutouts |
| `RightPanel_CrystalWave` | 15-135mm | Wave pattern + USB 3.0/SSD cable exits |

### Key Dimensions (all parametric, in mm)

| Parameter | Value | | Parameter | Value |
|-----------|-------|-|-----------|-------|
| Base | 140 x 100 | | Wall | 2.8 |
| Height | 160 | | Taper | 85% |
| Panel thickness | 2.5 | | Panel gap | 0.3 (tolerance) |
| Magnets | 6mm dia x 2mm | | Recess depth | 1.5mm (press-fit) |
| Pi 5 board | 85 x 56 | | Pi 5 holes | M2.5, 58x49mm spacing |
| SSD enclosure | 125 x 41 x 14 | | Ethernet adapter | 62 x 25 x 15 |

### FreeCAD API Patterns

- Loft wires must close: `pts = [p1, p2, p3, p4, p1]`
- Cylinder rotation for magnet recesses: front/rear rotate around X-axis (90deg), left/right around Y-axis
- Always call `doc.recompute()` after batch additions
- Boolean cuts need valid intersection; add 0.1mm epsilon to cut depths if failures occur

## Spec-Driven Pipeline

### Master Spec (`/.state/spec.json`)
Single source of truth for the entire project: color palette (6 Krypton-themed colors), parametric dimensions, component-to-color mappings, hardware BOM, print settings, and assembly instructions. All dashboard pages and the export pipeline read from this file.

### Multi-Color 3MF Export (`pipeline/export_3mf.py`)
FreeCAD headless script that:
1. Loads `.state/spec.json` for color mappings
2. Runs `krypton_nas_panels.py` to generate 8 objects
3. Assigns `ViewObject.ShapeColor` per object from spec palette
4. Exports single multi-color 3MF to `output/KryptonNAS_multicolor.3mf`
5. Exports individual STLs to `stl/`

Run: `./pipeline/build.sh`

### Web-Based Spec Viewer (`dashboard/spec-viewer.html`)
Three.js interactive spec sheet replacing TechDraw. Features:
- 3 orthographic viewports (front, right, top) + 1 perspective isometric with orbit controls
- `STLLoader` loads models, `MeshPhongMaterial` with colors from spec.json
- `EdgesGeometry` wireframe overlay for technical drawing look
- Color palette legend, engineering data cards, hardware BOM, print settings
- CDN via ES module importmap (three@0.170.0) - no build tools required

## State-Driven Development

Machine-readable state in `.state/`:

| File | Purpose |
|------|---------|
| `spec.json` | Single source of truth: colors, parameters, components, hardware BOM, assembly |
| `system.json` | Version, status, environment, architecture |
| `components.json` | 8 components with specs, color refs, print settings |
| `features.json` | Features with phase tracking (8 features) |
| `tasks.json` | Tasks with priorities (includes open bug: HDMI port cutouts on left panel) |
| `changelog.json` | Version history (v2.0 in-progress, v1.0 released) |
| `workflows.json` | Design workflows (includes multi-color 3MF export) |

**After any change:** update changelog, component/feature status, and task status in `.state/*.json` files alongside the code changes.

### State Relationships
- `tasks[].relatedFeature` references `features[].id`
- `tasks[].component` references `components[].id`
- `changelog[].changes[].component` references `components[].id`
- `features[].documentation` links to `/features/*.md`
- `features[].implementationPlan` links to `/implementation-plans/*.md`

## Known Issues

- **HDMI cutouts (bug):** Dual micro-HDMI port cutouts on `LeftPanel_ShieldArray` not rendering correctly. Boolean cut may have incorrect geometry/positioning.

## STL Export

- `MainShell.stl` - bare shell (no mounts), prints opening-up (no supports)
- `MainShell_Integrated.stl` - shell with all internal mounts fused (single-print option)
- `SSD_ClampMount.stl`, `Ethernet_ClampMount.stl`, `Pi5_Mount.stl` - individual mounts
- Panels print flat with pattern facing up
- Run `./pipeline/build.sh` to regenerate all STLs + multi-color 3MF

## OpenSCAD (PiNasCase.scad)

Original design with two variants. Switch at bottom of file:
```openscad
fortress_spire();            // Version 1 - vertical tower
// crystal_shard();           // Version 2 - angular wedge
```
Preview: F5. Full render: F6. Export: File > Export > STL.
