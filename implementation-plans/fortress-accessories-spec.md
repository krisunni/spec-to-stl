# Krypton NAS Aesthetic Accessories Plan

## Project Codename: **FORTRESS COLLECTION**

> *"The crystals... they contain the total knowledge of Krypton."* — Jor-El

A suite of desk accessories designed to complement the Krypton NAS case, transforming your workspace into a miniature Fortress of Solitude.

---

## Brand Identity

### Product Line: **House of El Desktop Series**

| Component | DC Theme Name | Inspiration |
|-----------|---------------|-------------|
| Main Case | **Krypton Spire** | The tapered crystal towers of Krypton |
| Base Platform | **Argo Pedestal** | Argo City, the domed Kryptonian city |
| LED Ring | **Rao's Halo** | Rao, Krypton's red sun |
| Crystal Accents | **Sunstone Shards** | Sunstone crystals that built the Fortress |
| Cable Manager | **Phantom Zone Conduit** | The interdimensional prison |
| Status Badge | **House Crest** | The iconic "S" shield (El family crest) |
| USB Hub Dock | **Kandor Station** | The bottled city of Kandor |
| Ventilation Top | **Fortress Crown** | The Fortress spire apex |

---

## Component Specifications

### 1. Argo Pedestal (Base Platform)

**Purpose:** Elevate the Krypton Spire, add visual weight, hide cables

```
Dimensions:
  - Base: 180 x 140 x 25mm (outer)
  - Top recess: 142 x 102mm (case sits inside lip)
  - Elevation: 22mm lift

Features:
  - Crystal facet pattern on sides (matches spire aesthetic)
  - Cable channel: 25mm wide rear exit slot
  - Anti-slip: 4x rubber feet (10mm dia)
  - Optional: Recessed cavity for LED strip (Rao's Halo integration)

Material: PLA/PETG, recommended ice blue or silver
```

**Pattern Style:** Angled facets mimicking crystalline growth, 30° chamfers

---

### 2. Rao's Halo (LED Accent Ring)

**Purpose:** Ambient underglow, status indication via RGB

```
Dimensions:
  - Ring OD: 160mm
  - Ring ID: 130mm
  - Height: 8mm
  - LED channel: 10mm wide x 5mm deep

Fits: WS2812B LED strip (60 LED/m) or 5V LED ring

Features:
  - Snap-fit into Argo Pedestal
  - Diffuser slots (frosted acrylic insert)
  - 3-wire exit port for Pi GPIO control

Modes (software-defined):
  - Solid red: "Red Sun" - System idle
  - Pulsing blue: "Krypton Pulse" - Disk activity
  - White sweep: "Fortress Awakening" - Boot sequence
```

---

### 3. Sunstone Shards (Crystal Accent Set)

**Purpose:** Decorative crystals that frame the case

```
Set includes (6 pieces):

  Shard Alpha (x2):
    - 15 x 10 x 60mm tall
    - 5-sided crystal profile
    - Magnetic base (6mm magnet)

  Shard Beta (x2):
    - 12 x 8 x 45mm tall
    - Angled 15° lean
    - Flat base (adhesive)

  Shard Gamma (x2):
    - 20 x 12 x 35mm
    - Cluster formation (3 crystals fused)
    - Weighted base

Placement: Flanking front corners of pedestal

Material: Clear/translucent PETG for light diffusion
Optional: Hollow for LED tea light insertion
```

---

### 4. Phantom Zone Conduit (Cable Manager)

**Purpose:** Route cables from rear of case to desk edge

```
Dimensions:
  - Length: 200mm (adjustable segments)
  - Channel: 30mm wide x 20mm tall (interior)
  - Wall: 2mm

Design:
  - Segmented spine (5 x 40mm sections)
  - Living hinge connections (flex ±30°)
  - Crystal-slot pattern vents (matches rear panel)
  - End caps with 25mm cable exit holes

Mounting: Adhesive strip channel on underside

Capacity:
  - 1x Ethernet cable
  - 1x USB-C power
  - 2x HDMI (micro to full adapter cables)
```

---

### 5. House Crest (Status Badge)

**Purpose:** Front-facing emblem with optional NFC/LED

```
Dimensions:
  - Shield shape: 40mm wide x 50mm tall x 5mm thick
  - Bezel depth: 2mm

Design Options:

  A) Basic Crest:
     - Raised "S" shield (Superman/House of El)
     - Friction-fit into front panel slot

  B) Illuminated Crest:
     - Hollow back for 5mm LED
     - Translucent face layer
     - 2-wire to Pi GPIO

  C) NFC Crest:
     - Cavity for NTAG215 chip
     - Tap to wake / smart home trigger

Attachment: Magnetic (uses existing front panel magnet positions)
```

---

### 6. Kandor Station (USB Hub Dock)

**Purpose:** Front-accessible USB ports with Kryptonian styling

```
Dimensions:
  - Body: 80 x 50 x 30mm
  - Dome top (Kandor bottle reference)

Features:
  - 4x USB-A 3.0 ports (front-facing)
  - Internal USB hub PCB (generic 4-port)
  - Single USB-C upstream cable to Pi
  - Crystal facet side panels

Placement: Adjacent to case on pedestal or standalone

Design notes:
  - Dome is decorative lid (removable)
  - Hex pattern vents match rear panel
  - LED ring around base (optional, matches Rao's Halo)
```

---

### 7. Fortress Crown (Ventilation Top Cap)

**Purpose:** Replace solid top with decorative ventilation piece

```
Dimensions:
  - Fits existing top opening: ~119 x 85mm (tapered)
  - Height: 20-40mm (extends above case)

Design Options:

  A) Crystal Spire Cap:
     - Central crystal column (25mm dia)
     - Ring of smaller crystals (6x)
     - Open lattice for airflow

  B) Fortress Dome:
     - Geodesic dome pattern
     - Triangle vents (60% open area)
     - Frosted for LED diffusion from below

  C) Sentinel Tower:
     - Kryptonian robot head silhouette
     - Eye slots for status LEDs
     - 40mm tall extension

Attachment: Friction fit or magnetic (add 4x magnets to top rim)
```

---

## Integration Matrix

| Accessory | Standalone | Requires Pedestal | Pi GPIO | Magnets |
|-----------|------------|-------------------|---------|---------|
| Argo Pedestal | Yes | — | Optional | No |
| Rao's Halo | No | Yes | Yes (3-wire) | No |
| Sunstone Shards | Yes | Optional | No | Yes (x2) |
| Phantom Conduit | Yes | No | No | No |
| House Crest | No | No | Optional | Yes |
| Kandor Station | Yes | Optional | No (USB) | No |
| Fortress Crown | No | No | Optional | Yes |

---

## Recommended Configurations

### **Minimalist Setup** (3 pieces)
- Argo Pedestal
- House Crest (Basic)
- Phantom Zone Conduit

### **Illuminated Setup** (5 pieces)
- Argo Pedestal + Rao's Halo
- House Crest (Illuminated)
- Sunstone Shards (x2 Alpha)
- Fortress Crown (Dome)

### **Full Fortress** (All pieces)
- Complete accessory suite
- Coordinated LED control via Pi GPIO
- Cable-free front presentation

---

## Technical Compatibility

```
Base Case Reference: KryptonNAS_Complete.FCStd
Script: krypton_nas_panels.py

Key Dimensions to Match:
  - Case base footprint: 140 x 100mm
  - Case top footprint: 119 x 85mm
  - Case height: 160mm
  - Wall thickness: 2.8mm
  - Magnet size: 6mm dia x 2mm
  - Panel margin: 15mm from edges
```

---

## File Naming Convention

```
krypton_argo_pedestal.py      # Base platform
krypton_rao_halo.py           # LED ring
krypton_sunstone_shards.py    # Crystal accents
krypton_phantom_conduit.py    # Cable manager
krypton_house_crest.py        # Status badge
krypton_kandor_station.py     # USB hub
krypton_fortress_crown.py     # Top cap variants
```

---

## Print Recommendations

| Part | Layer Height | Infill | Supports | Material |
|------|--------------|--------|----------|----------|
| Argo Pedestal | 0.2mm | 20% | No | PLA/PETG |
| Rao's Halo | 0.16mm | 100% | No | White PLA |
| Sunstone Shards | 0.12mm | 15% | Yes | Clear PETG |
| Phantom Conduit | 0.2mm | 15% | No | PLA |
| House Crest | 0.12mm | 100% | No | Dual-color |
| Kandor Station | 0.2mm | 25% | Minimal | PLA/PETG |
| Fortress Crown | 0.16mm | 20% | Yes | Clear/White |

---

## Color Palette

| Name | Hex | Use |
|------|-----|-----|
| Krypton Ice | #B8D4E3 | Primary shell color |
| Fortress Silver | #C0C0C0 | Metallic accents |
| Rao Red | #8B0000 | LED idle state |
| Crystal Blue | #4169E1 | LED active state |
| Sunstone Gold | #FFD700 | Accent highlights |
| Phantom Purple | #4B0082 | Optional alternate |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-02-02 | Initial design plan |

---

*"In the name of Rao, let this knowledge endure."*
