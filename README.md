<p align="center">
  <img src="https://img.shields.io/badge/version-3.0.0-blue?style=flat-square" alt="Version 3.0.0">
  <img src="https://img.shields.io/badge/FreeCAD-Python-green?style=flat-square" alt="FreeCAD Python">
  <img src="https://img.shields.io/badge/output-STL%20%7C%203MF-orange?style=flat-square" alt="STL + 3MF">
  <img src="https://img.shields.io/badge/dashboard-Three.js-purple?style=flat-square" alt="Three.js Dashboard">
  <img src="https://img.shields.io/badge/print-PLA%20%7C%20PETG%20%7C%20TPU-red?style=flat-square" alt="PLA + PETG + TPU">
</p>

# Spec-to-STL

A collection of 3D-printable designs built entirely through spec-driven development with AI assistance. JSON specs define every dimension, color, and constraint. FreeCAD Python scripts generate parametric geometry. A headless pipeline exports print-ready files.

---

## Projects

### Krypton NAS - Fortress Spire

A Raspberry Pi 5 NAS enclosure inspired by the Fortress of Solitude from DC Comics. Tapered tower design (140x100mm base, 160mm tall) with passive thermal management, removable magnetic panels, and tool-free component mounting. 8 components, 6 colors, 48 magnets.

- **Script:** `krypton_nas_panels.py`
- **STLs:** `stl/krypton-nas/`
- **Components:** Main Shell, 4 decorative panels, SSD mount, Ethernet mount, Pi 5 mount

### AirPods Max Headband Spacer

A graduated wedge spacer that slides between the AirPods Max mesh canopy and steel frame to reduce clamping force for glasses wearers. Tapers from 37mm to 47mm over 80mm, with frame rail grooves and graduation notches for repeatable adjustment.

- **Script:** `headband_spacer.py`
- **STLs:** `stl/headband-spacer/`
- **Components:** Single solid wedge with grooves and notches

### AirPods Max Headphone Stand

A two-piece telescoping headphone stand with adjustable height. Square tube base (130x90mm) with 5 locking slots, slider column with curved headband cradle, and a spacer holder shelf. Height range: 61-161mm in 15mm steps.

- **Script:** `headphone_stand.py`
- **STLs:** `stl/headphone-stand/`
- **Components:** Stand Base, Stand Slider

---

## Quick Start

### View the Dashboard

```bash
./serve.sh
# Open http://localhost:8080/dashboard/
```

The dashboard has project cards linking to the interactive 3D spec viewer with project switcher tabs.

### Generate All Models + Export

```bash
# One-command pipeline: generates all projects, assigns colors, exports 3MF + STLs
./pipeline/build.sh

# Or run individual scripts in FreeCAD
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('krypton_nas_panels.py').read())"
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('headband_spacer.py').read())"
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('headphone_stand.py').read())"
```

The pipeline reads `.state/spec.json` for all project definitions and exports:
- `output/KryptonNAS_multicolor.3mf` -- multi-color 3MF with per-body colors
- `stl/krypton-nas/*.stl` -- Krypton NAS component STLs
- `stl/headband-spacer/*.stl` -- Headband spacer STL
- `stl/headphone-stand/*.stl` -- Headphone stand STLs (base + slider)

---

## Repository Structure

```
.state/              Machine-readable project state (JSON)
  spec.json          Single source of truth: multi-project specs, colors, components
  system.json        Project metadata and version
  components.json    All components across projects
  features.json      Features with phase tracking
  tasks.json         Tasks with priorities
  changelog.json     Version history
pipeline/            Spec-driven build pipeline
  export_3mf.py      Multi-project 3MF + STL export
  build.sh           One-command pipeline runner
dashboard/           Interactive HTML dashboards (no build step)
  index.html         Landing page with project cards
  spec-viewer.html   Three.js 3D viewer with project switcher
stl/                 Print-ready STL files organized by project
  krypton-nas/       Krypton NAS enclosure STLs (9 files)
  headband-spacer/   Headband spacer STL (1 file)
  headphone-stand/   Headphone stand STLs (2 files)
```

---

## Spec-Driven Development

All project state lives in `.state/*.json` files with `.state/spec.json` as the single source of truth. The spec file uses a multi-project `projects` array where each project defines its own colors, parameters, components, hardware BOM, and assembly instructions.

The spec viewer (`dashboard/spec-viewer.html`) loads STL models in the browser using Three.js, with project tabs to switch between designs, exploded views for multi-component projects, and per-component isolation views.

---

## Trademark Notice

DC, DC Comics, Superman, Krypton, Fortress of Solitude, Phantom Zone, and all related characters, names, and indicia are trademarks of and copyright DC Comics and/or Warner Bros. Discovery. Raspberry Pi is a trademark of Raspberry Pi Ltd. AirPods Max is a trademark of Apple Inc. All other trademarks are the property of their respective owners.

This project uses these names solely to describe the thematic inspiration and hardware compatibility of the designs. No ownership or affiliation is claimed or implied.

## License

Open source. Print it, mod it, make it yours.
