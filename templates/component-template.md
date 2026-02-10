# Component: {Component Name}

## Overview

| Property | Value |
|----------|-------|
| **ID** | {component-id} |
| **Version** | {version} |
| **Status** | {operational\|pending\|error} |
| **Type** | {enclosure\|panel\|mount\|accessory} |
| **STL** | stl/{FileName}.stl |

{Brief description of what this component is}

## Features

- Feature 1
- Feature 2

## Dimensions

| Parameter | Value |
|-----------|-------|
| Width | {X} mm |
| Height | {Y} mm |
| Depth | {Z} mm |

## Print Settings

| Setting | Recommended |
|---------|-------------|
| **Orientation** | {description} |
| **Layer height** | 0.2mm |
| **Supports** | None / Required |
| **Infill** | {percentage} |
| **Material** | PLA or PETG |

## Generation

```bash
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('{script}.py').read())"
```

## Related

- Related components and features
