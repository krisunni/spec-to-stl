# Component: Main Shell

## Overview

| Property | Value |
|----------|-------|
| **ID** | main-shell |
| **Version** | 1.0.0 |
| **Status** | operational |
| **Type** | enclosure |
| **STL** | stl/MainShell_Integrated.stl |

Tapered case body with panel openings, magnet recesses, and all internal component mounts fused into a single printable object.

## Features

- Lofted tapered geometry (140x100mm base, 85% taper at top)
- Panel openings on all 4 sides with alignment lips
- 24 magnet recesses (6 per side, 6mm x 2mm)
- Integrated SSD, Ethernet, and Pi5 mounts (no floating geometry)

## Dimensions

| Parameter | Value |
|-----------|-------|
| Base footprint | 140 x 100 mm |
| Height | 160 mm |
| Top footprint | 119 x 85 mm (85% taper) |
| Wall thickness | 2.8 mm |
| Floor thickness | 3.0 mm |

## Internal Mounts

### SSD Clamp Mount (z=3mm)
- Rail-style mount for UGREEN M.2 NVMe enclosure (125x41x14mm)
- 4 snap-in retention clips
- Tool-free installation

### Ethernet Clamp Mount (z=35mm)
- U-cradle for UGREEN USB-C Ethernet adapter (62x25x15mm)
- Retention clips for secure hold
- Cable routing clearance

### Pi 5 Mount (z=65mm)
- 4 corner posts matching Pi 5 hole pattern (85x56mm)
- M2.5 threaded screw holes
- Board surface at z=73mm (8mm standoff)
- Airflow platform with ventilation slots

## Print Settings

| Setting | Recommended |
|---------|-------------|
| **Orientation** | Opening facing up |
| **Layer height** | 0.2mm |
| **Supports** | None needed |
| **Infill** | 15-20% |
| **Material** | PLA or PETG |
| **STL file** | MainShell_Integrated.stl |

## Generation

```bash
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('krypton_nas_panels.py').read())"
```

Key functions: `create_main_shell()` (line 632), `create_panel_opening()`, `add_magnet_recesses()`

## Related

- Panels: `/components/decorative-panels.md`
- Mounts: `/components/internal-mounts.md`
- Architecture: `/architecture/overview.md`
