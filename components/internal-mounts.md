# Component: Internal Mounts

## Overview

3 internal component mounts integrated into the MainShell. All use snap-in or screw-based retention for secure, tool-minimal installation.

## SSD Clamp Mount

| Property | Value |
|----------|-------|
| **ID** | ssd-mount |
| **Position** | z = 3mm (base level) |
| **Target** | UGREEN M.2 NVMe enclosure |
| **Target dimensions** | 125 x 41 x 14 mm |
| **Retention** | 4 snap-in clips |
| **STL** | stl/SSD_ClampMount.stl |

Rail-style mount with flexible retention clips that deflect during insertion and spring back to hold the SSD enclosure. No tools required.

## Ethernet Clamp Mount

| Property | Value |
|----------|-------|
| **ID** | ethernet-mount |
| **Position** | z = 35mm |
| **Target** | UGREEN USB-C Ethernet adapter |
| **Target dimensions** | 62 x 25 x 15 mm |
| **Retention** | U-cradle + clips |
| **STL** | stl/Ethernet_ClampMount.stl |

U-shaped cradle profile with retention clips. Cable routing clearance for USB-C cable to Pi 5.

## Raspberry Pi 5 Mount

| Property | Value |
|----------|-------|
| **ID** | pi5-mount |
| **Position** | z = 65mm (board at z=73mm) |
| **Target** | Raspberry Pi 5 |
| **Target dimensions** | 85 x 56 mm |
| **Retention** | 4x M2.5 screws |
| **STL** | stl/Pi5_Mount.stl |

4 corner mounting posts matching the Pi 5 hole pattern with M2.5 threaded holes. 8mm standoff provides airflow underneath the board. Ventilation slots in the platform.

## Hardware Required

| Item | Quantity | Specification |
|------|----------|---------------|
| M2.5 screws | 4 | For Pi 5 mounting |
| Neodymium magnets | 24 | 6mm dia x 2mm thick |

SSD and Ethernet mounts use snap-in retention (no hardware needed).

## Related

- Shell: `/components/main-shell.md`
- Feature: `/features/snap-in-component-mounts.md`
