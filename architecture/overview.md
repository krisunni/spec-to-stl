# Architecture Overview

## System Architecture

Krypton NAS is a 3D printable enclosure system for Raspberry Pi 5 NAS builds. The architecture spans two design tools (FreeCAD Python and OpenSCAD) producing 8 printable components that assemble into a complete Fortress of Solitude-themed case.

## Design Pipeline

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Parametric      │     │   3D Model       │     │   3D Print       │
│   Python Script   │────▶│   (FreeCAD)      │────▶│   (STL → Slicer) │
│                   │     │                  │     │                  │
│ krypton_nas_      │     │ KryptonNAS_      │     │ stl/*.stl        │
│ panels.py         │     │ Complete.FCStd   │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

## Component Stack (Bottom to Top)

```
z=160mm ┌─────────────────────────────┐
        │        Exhaust Space         │  ← Hot air exits through
        │                              │    panel vents & top
z=73mm  │  ┌───────────────────────┐  │
        │  │   Raspberry Pi 5      │  │  ← Board on 4 corner posts
z=65mm  │  │   (85 x 56 mm)       │  │    M2.5 screws
        │  └───────────────────────┘  │
        │                              │
z=35mm  │  ┌───────────────────────┐  │
        │  │   Ethernet Adapter    │  │  ← U-cradle with snap clips
        │  │   (62 x 25 x 15 mm)  │  │    UGREEN USB-C adapter
        │  └───────────────────────┘  │
        │                              │
z=3mm   │  ┌───────────────────────┐  │
        │  │   M.2 SSD Enclosure   │  │  ← Rail mount with 4 clips
        │  │   (125 x 41 x 14 mm) │  │    UGREEN NVMe enclosure
z=0mm   └──┴───────────────────────┴──┘
           140 x 100 mm base (85% taper)
```

## Panel System

```
            ┌─────────┐
            │  Top    │  (open for exhaust)
            │         │
     ┌──────┤         ├──────┐
     │ Left │         │Right │
     │Shield│  Main   │Wave  │
     │Array │  Shell  │      │
     │      │         │      │
     │ Pi   │         │Cable │
     │ I/O  │         │exits │
     ├──────┤         ├──────┤
     │Front │         │ Rear │
     │Burst │         │ Gate │
     └──────┴─────────┴──────┘

Each panel: 2.5mm thick, 5mm lip overlap
Attachment: 6x neodymium magnets per side (24 total)
Magnet spec: 6mm diameter x 2mm thick, 1.5mm recess
```

## File Architecture

```
krypton_nas_panels.py
├── Parameters (lines 20-50)
│   └── All dimensions configurable
├── Helpers (lines 52-295)
│   ├── get_taper_at_height()   ← Core taper calculation
│   ├── create_tapered_box()    ← Lofted geometry
│   ├── create_diamond()        ← Crystal shape primitive
│   ├── create_hexagon()        ← Hex prism primitive
│   ├── create_shield_shape()   ← Pentagon shield
│   └── create_crystal_slot()   ← Octagonal vent
├── Mounts (lines 324-627)
│   ├── create_ssd_clamp_mount()
│   ├── create_ethernet_clamp_mount()
│   └── create_pi5_mount()
├── Shell (lines 632-870)
│   ├── create_main_shell()
│   ├── create_panel_opening()
│   └── add_magnet_recesses()
├── Panels (lines 877-1326)
│   ├── create_front_panel_crystal_burst()
│   ├── create_rear_panel_fortress_gate()
│   ├── create_left_panel_shield_array()
│   └── create_right_panel_crystal_wave()
└── Build (lines 1331-1422)
    └── Creates 8 FreeCAD objects
```

## Thermal Design

The tapered spire creates a natural chimney effect:

1. Cool air enters through lower panel vents
2. Heat from Pi 5 and SSD rises naturally
3. Component stacking places heat sources at optimal heights
4. Hot air exits through upper panel vents and open top
5. No fans required - fully passive cooling

## Related Documents

- [Component: Main Shell](/components/main-shell.md)
- [Component: Decorative Panels](/components/decorative-panels.md)
- [Feature: Passive Thermal Management](/features/passive-thermal-management.md)
- [Feature: Removable Magnetic Panels](/features/removable-magnetic-panels.md)
