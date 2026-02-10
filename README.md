<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-blue?style=flat-square" alt="Version 2.0.0">
  <img src="https://img.shields.io/badge/FreeCAD-Python-green?style=flat-square" alt="FreeCAD Python">
  <img src="https://img.shields.io/badge/output-STL%20%7C%203MF-orange?style=flat-square" alt="STL + 3MF">
  <img src="https://img.shields.io/badge/dashboard-Three.js-purple?style=flat-square" alt="Three.js Dashboard">
  <img src="https://img.shields.io/badge/print-PETG%20%7C%20PLA-red?style=flat-square" alt="PETG + PLA">
</p>

# Krypton NAS - Fortress Spire

A 3D printable Raspberry Pi 5 NAS enclosure inspired by the Fortress of Solitude from DC Comics -- designed entirely through spec-driven development with AI assistance.

---

## The Story

I'm a software engineer, not a CAD designer. I wanted a custom NAS case for my Raspberry Pi 5 but had zero experience with parametric 3D modeling. Instead of spending weeks learning FreeCAD from scratch, I applied the same spec-driven development patterns I use for software:

1. **Write the spec first** -- dimensions, constraints, component interfaces
2. **Let AI fill the knowledge gaps** -- FreeCAD Python API, 3D geometry, print tolerances
3. **Iterate with structured state** -- track components, features, and tasks in machine-readable JSON
4. **Ship real artifacts** -- printable STL files, not just documentation

The result: a fully parametric, 8-component enclosure with themed decorative panels, passive thermal management, and snap-in component mounts -- all generated from a single Python script and exported via a spec-driven pipeline.

---

## What's In This Repo

### The Product

A tapered tower enclosure (140x100mm base, 160mm tall) housing:
- Raspberry Pi 5 on M2.5 standoffs
- UGREEN M.2 NVMe SSD in snap-in rails
- UGREEN USB-C Ethernet adapter in a U-cradle
- 4 removable magnetic panels with themed patterns

### The Process

This repo is also a reference implementation of **spec-driven development applied to non-software work**:

```
.state/              Machine-readable project state (JSON)
  spec.json          Single source of truth: colors, dimensions, components, BOM
  system.json        Project metadata and version
  components.json    8 printable parts with specs
  features.json      8 features with phase tracking
  tasks.json         10 tasks with priorities
  changelog.json     Version history
  workflows.json     Design and manufacturing workflows
  glossary.json      Krypton NAS terminology
pipeline/            Spec-driven build pipeline
  export_3mf.py      Multi-color 3MF + individual STL export
  build.sh           One-command pipeline runner
dashboard/           Interactive HTML dashboards (no build step)
  spec-viewer.html   Three.js 3D spec sheet with exploded view
stl/                 Print-ready STL files for all components
```

---

## Quick Start

### View the Dashboard

```bash
./serve.sh
# Open http://localhost:8080/dashboard/
```

7 pages: Overview, Components, Features, Tasks, Changelog, Glossary, and **Spec Sheet** (interactive 3D viewer with exploded view and component selector).

### Generate the 3D Model + Export

```bash
# One-command pipeline: generates model, assigns colors, exports 3MF + STLs
./pipeline/build.sh

# Or run FreeCAD directly for model generation only
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('krypton_nas_panels.py').read())"
```

The pipeline reads `.state/spec.json` for color mappings and component definitions, runs the FreeCAD script headless, and exports:
- `output/KryptonNAS_multicolor.3mf` -- multi-color 3MF with per-body colors
- `stl/*.stl` -- individual component STLs for single-color printing

### Print It

1. Open individual STLs from `stl/` in your slicer (or use the multi-color 3MF)
2. `MainShell.stl` -- print opening-up, no supports needed
3. `MainShell_Integrated.stl` -- alternative with SSD/Ethernet/Pi5 mounts fused in
4. Print each panel flat, pattern face up
5. Press-fit 48 magnets (6mm x 2mm) into recesses (24 shell + 24 panels)
6. Snap in SSD, Ethernet adapter, screw in Pi 5

---

## Components

| Component | STL | Color | Description |
|-----------|-----|-------|-------------|
| Main Shell | `MainShell.stl` | ![#C8E6F0](https://img.shields.io/badge/-Krypton%20Ice-C8E6F0?style=flat-square) | Hollow case body with panel openings + magnet recesses |
| Front Panel | `FrontPanel_CrystalBurst.stl` | ![#4A9BD9](https://img.shields.io/badge/-Crystal%20Blue-4A9BD9?style=flat-square) | Radial diamond pattern |
| Rear Panel | `RearPanel_FortressGate.stl` | ![#4A9BD9](https://img.shields.io/badge/-Crystal%20Blue-4A9BD9?style=flat-square) | Hex grid + crystal vents + RJ45 cutout |
| Left Panel | `LeftPanel_ShieldArray.stl` | ![#D4A848](https://img.shields.io/badge/-Sunstone%20Gold-D4A848?style=flat-square) | Shield pattern + Pi I/O ports |
| Right Panel | `RightPanel_CrystalWave.stl` | ![#C84040](https://img.shields.io/badge/-Rao%20Red-C84040?style=flat-square) | Wave pattern + cable exits |
| SSD Mount | `SSD_ClampMount.stl` | ![#A8B8C8](https://img.shields.io/badge/-Fortress%20Silver-A8B8C8?style=flat-square) | Snap-in rails at z=3mm |
| Ethernet Mount | `Ethernet_ClampMount.stl` | ![#A8B8C8](https://img.shields.io/badge/-Fortress%20Silver-A8B8C8?style=flat-square) | U-cradle at z=35mm |
| Pi 5 Mount | `Pi5_Mount.stl` | ![#A8B8C8](https://img.shields.io/badge/-Fortress%20Silver-A8B8C8?style=flat-square) | M2.5 standoffs at z=65mm |

Also available: `MainShell_Integrated.stl` (shell + all 3 mounts fused for single-piece printing).

---

## Color Palette

<table>
  <tr>
    <td><img src="https://img.shields.io/badge/%20%20%20%20%20%20%20%20-C8E6F0?style=for-the-badge" alt="swatch"></td>
    <td><strong>Krypton Ice</strong><br><code>#C8E6F0</code></td>
    <td>Main shell body</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/%20%20%20%20%20%20%20%20-A8B8C8?style=for-the-badge" alt="swatch"></td>
    <td><strong>Fortress Silver</strong><br><code>#A8B8C8</code></td>
    <td>Internal mounts</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/%20%20%20%20%20%20%20%20-4A9BD9?style=for-the-badge" alt="swatch"></td>
    <td><strong>Crystal Blue</strong><br><code>#4A9BD9</code></td>
    <td>Front and rear panels</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/%20%20%20%20%20%20%20%20-D4A848?style=for-the-badge" alt="swatch"></td>
    <td><strong>Sunstone Gold</strong><br><code>#D4A848</code></td>
    <td>Left panel (port side)</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/%20%20%20%20%20%20%20%20-C84040?style=for-the-badge" alt="swatch"></td>
    <td><strong>Rao Red</strong><br><code>#C84040</code></td>
    <td>Right panel (cable side)</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/%20%20%20%20%20%20%20%20-7B5EA7?style=for-the-badge" alt="swatch"></td>
    <td><strong>Phantom Purple</strong><br><code>#7B5EA7</code></td>
    <td>Accent features</td>
  </tr>
</table>

---

## Hardware BOM

| Item | Qty | Spec |
|------|-----|------|
| Neodymium magnets | 48 | 6mm dia x 2mm (24 shell + 24 panels) |
| M2.5 x 6mm screws | 4 | Phillips pan head, Pi 5 mounting |
| Raspberry Pi 5 | 1 | Any RAM variant, 85 x 56mm |
| UGREEN M.2 SSD enclosure | 1 | USB-C, 125 x 41 x 14mm |
| UGREEN USB-C Ethernet | 1 | Gigabit, 62 x 25 x 15mm |
| USB-C power supply | 1 | 5V 5A (27W PD) |
| USB 3.0 cable | 1 | USB-A to USB-C, short |
| Ethernet cable | 1 | Cat5e/Cat6, short |

---

## Spec-Driven Development

### How It Works

All project state lives in `.state/*.json` files with `.state/spec.json` as the single source of truth for the build pipeline. Interactive dashboards in `dashboard/` render directly from this JSON -- no build step, no framework, just vanilla HTML + fetch.

The spec viewer (`dashboard/spec-viewer.html`) loads STL models directly in the browser using Three.js, with an exploded view showing all 8 components with their themed colors.

### Why It Works for Non-Software

Spec-driven development isn't just for code. The same patterns that make software projects navigable for AI assistants work for:

- **Hardware design** -- components, tolerances, interfaces
- **Manufacturing** -- print settings, material specs, assembly steps
- **Creative work** -- design language, color palettes, thematic consistency

The key insight: if you can express your domain knowledge as structured specifications, AI can bridge the gap between your intent and the specialized tools needed to realize it.

---

## What's Next

The **Fortress Accessories Collection** adds 7 desk accessories:
Argo Pedestal, Rao's Halo LED ring, Sunstone Shards, Phantom Zone cable manager, House Crest badge, Kandor Station USB hub, and Fortress Crown top cap.

Track progress: `./serve.sh` then open the Features dashboard.

## Known Issues

- **HDMI cutouts**: Dual micro-HDMI port cutouts on `LeftPanel_ShieldArray` not rendering correctly. Boolean cut may have incorrect geometry/positioning.

---

## Trademark Notice

This is an independent fan project. It is not produced, endorsed, supported, or affiliated with DC Comics, Warner Bros. Discovery, or any of their subsidiaries or affiliates.

DC, DC Comics, Superman, Krypton, Fortress of Solitude, Phantom Zone, and all related characters, names, and indicia are trademarks of and copyright DC Comics and/or Warner Bros. Discovery. All rights reserved.

Raspberry Pi is a trademark of Raspberry Pi Ltd. UGREEN is a trademark of Ugreen Group Limited. FreeCAD is a trademark of the FreeCAD community. All other trademarks are the property of their respective owners.

This project uses these names solely to describe the thematic inspiration and hardware compatibility of the design. No ownership or affiliation is claimed or implied.

## License

Open source. Print it, mod it, make it yours.
