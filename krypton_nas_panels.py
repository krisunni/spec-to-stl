#!/usr/bin/env python3
"""
Krypton NAS - Fortress Spire Case with All Removable Panels
Creative 3D-printable design with magnetic attachments

Run this script in FreeCAD's Python console or via:
  freecad -c krypton_nas_panels.py

All four sides have removable magnetic panels with unique DC/Krypton-inspired patterns:
- Front: Crystal Burst pattern
- Rear: Fortress Gate / Hex Matrix pattern
- Left: Shield Array pattern (with Pi port cutouts)
- Right: Crystal Wave pattern (with cable exits)
"""

import FreeCAD
import Part
import math

# ============================================
# PARAMETERS
# ============================================
spire_base_x = 140  # Width at base (mm)
spire_base_y = 100  # Depth at base (mm)
spire_height = 160  # Total height (mm)
spire_taper = 0.85  # Top is 85% of base

wall = 2.8          # Wall thickness
floor_h = 3.0       # Floor thickness
tolerance = 0.3     # Panel gap tolerance

# Calculate top dimensions
top_x = spire_base_x * spire_taper  # 119mm
top_y = spire_base_y * spire_taper  # 85mm

# Panel parameters
panel_thick = 2.5   # Panel body thickness
lip_width = 5.0     # Lip around panel
lip_depth = 2.5     # Lip extends into case

# Magnet parameters
magnet_d = 6.0      # 6mm diameter
magnet_h = 2.0      # 2mm thick
magnet_recess = 1.5 # Depth in both frame and panel

# Panel opening dimensions
panel_margin = 15   # Margin from edges
panel_bottom = 15   # Start height from floor
panel_top_margin = 25  # Distance from top
panel_height = spire_height - panel_bottom - panel_top_margin  # ~120mm

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_taper_at_height(z):
    """Calculate taper factor at given height"""
    t = z / spire_height
    return 1.0 - t * (1.0 - spire_taper)

def get_x_at_height(z):
    """Get X dimension at height z"""
    taper = get_taper_at_height(z)
    return spire_base_x * taper

def get_y_at_height(z):
    """Get Y dimension at height z"""
    taper = get_taper_at_height(z)
    return spire_base_y * taper

def get_offset_at_height(z):
    """Get XY offset at height z due to taper"""
    current_x = get_x_at_height(z)
    current_y = get_y_at_height(z)
    offset_x = (spire_base_x - current_x) / 2
    offset_y = (spire_base_y - current_y) / 2
    return offset_x, offset_y

def create_tapered_box(base_x, base_y, height, taper):
    """Create a tapered box using loft"""
    top_x = base_x * taper
    top_y = base_y * taper

    # Base rectangle
    base_pts = [
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(base_x, 0, 0),
        FreeCAD.Vector(base_x, base_y, 0),
        FreeCAD.Vector(0, base_y, 0),
        FreeCAD.Vector(0, 0, 0)
    ]
    base_wire = Part.makePolygon(base_pts)

    # Top rectangle (centered)
    offset_x = (base_x - top_x) / 2
    offset_y = (base_y - top_y) / 2
    top_pts = [
        FreeCAD.Vector(offset_x, offset_y, height),
        FreeCAD.Vector(offset_x + top_x, offset_y, height),
        FreeCAD.Vector(offset_x + top_x, offset_y + top_y, height),
        FreeCAD.Vector(offset_x, offset_y + top_y, height),
        FreeCAD.Vector(offset_x, offset_y, height)
    ]
    top_wire = Part.makePolygon(top_pts)

    loft = Part.makeLoft([base_wire, top_wire], True)
    return loft

def create_diamond(cx, cy, cz, size, depth, direction='z'):
    """Create a diamond/crystal shape"""
    half = size / 2

    if direction == 'z':
        points = [
            FreeCAD.Vector(cx, cy + half, cz),
            FreeCAD.Vector(cx + half, cy, cz),
            FreeCAD.Vector(cx, cy - half, cz),
            FreeCAD.Vector(cx - half, cy, cz),
            FreeCAD.Vector(cx, cy + half, cz),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.extrude(FreeCAD.Vector(0, 0, depth))
    elif direction == '-z':
        points = [
            FreeCAD.Vector(cx, cy + half, cz),
            FreeCAD.Vector(cx + half, cy, cz),
            FreeCAD.Vector(cx, cy - half, cz),
            FreeCAD.Vector(cx - half, cy, cz),
            FreeCAD.Vector(cx, cy + half, cz),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.extrude(FreeCAD.Vector(0, 0, -depth))
    elif direction == 'y':
        points = [
            FreeCAD.Vector(cx, cy, cz + half),
            FreeCAD.Vector(cx + half, cy, cz),
            FreeCAD.Vector(cx, cy, cz - half),
            FreeCAD.Vector(cx - half, cy, cz),
            FreeCAD.Vector(cx, cy, cz + half),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.extrude(FreeCAD.Vector(0, depth, 0))
    elif direction == '-y':
        points = [
            FreeCAD.Vector(cx, cy, cz + half),
            FreeCAD.Vector(cx + half, cy, cz),
            FreeCAD.Vector(cx, cy, cz - half),
            FreeCAD.Vector(cx - half, cy, cz),
            FreeCAD.Vector(cx, cy, cz + half),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.extrude(FreeCAD.Vector(0, -depth, 0))
    elif direction == 'x':
        points = [
            FreeCAD.Vector(cx, cy, cz + half),
            FreeCAD.Vector(cx, cy + half, cz),
            FreeCAD.Vector(cx, cy, cz - half),
            FreeCAD.Vector(cx, cy - half, cz),
            FreeCAD.Vector(cx, cy, cz + half),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.extrude(FreeCAD.Vector(depth, 0, 0))
    else:  # '-x'
        points = [
            FreeCAD.Vector(cx, cy, cz + half),
            FreeCAD.Vector(cx, cy + half, cz),
            FreeCAD.Vector(cx, cy, cz - half),
            FreeCAD.Vector(cx, cy - half, cz),
            FreeCAD.Vector(cx, cy, cz + half),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        return face.extrude(FreeCAD.Vector(-depth, 0, 0))

def create_hexagon(cx, cy, cz, size, depth, direction='z'):
    """Create a hexagonal prism"""
    points = []
    for i in range(7):
        angle = math.pi / 6 + i * math.pi / 3
        if direction in ['z', '-z']:
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            points.append(FreeCAD.Vector(x, y, cz))
        elif direction in ['y', '-y']:
            x = cx + size * math.cos(angle)
            z = cz + size * math.sin(angle)
            points.append(FreeCAD.Vector(x, cy, z))
        else:  # x directions
            y = cy + size * math.cos(angle)
            z = cz + size * math.sin(angle)
            points.append(FreeCAD.Vector(cx, y, z))

    wire = Part.makePolygon(points)
    face = Part.Face(wire)

    if direction == 'z':
        return face.extrude(FreeCAD.Vector(0, 0, depth))
    elif direction == '-z':
        return face.extrude(FreeCAD.Vector(0, 0, -depth))
    elif direction == 'y':
        return face.extrude(FreeCAD.Vector(0, depth, 0))
    elif direction == '-y':
        return face.extrude(FreeCAD.Vector(0, -depth, 0))
    elif direction == 'x':
        return face.extrude(FreeCAD.Vector(depth, 0, 0))
    else:
        return face.extrude(FreeCAD.Vector(-depth, 0, 0))

def create_shield_shape(cx, cy, cz, size, depth, direction='y'):
    """Create a Superman-inspired shield/pentagon shape"""
    # Pentagon-like shield (pointed at bottom)
    h = size
    w = size * 0.8

    if direction in ['y', '-y']:
        points = [
            FreeCAD.Vector(cx, cy, cz + h * 0.5),        # Top center
            FreeCAD.Vector(cx + w/2, cy, cz + h * 0.3),  # Top right
            FreeCAD.Vector(cx + w/2, cy, cz - h * 0.2),  # Mid right
            FreeCAD.Vector(cx, cy, cz - h * 0.5),        # Bottom point
            FreeCAD.Vector(cx - w/2, cy, cz - h * 0.2),  # Mid left
            FreeCAD.Vector(cx - w/2, cy, cz + h * 0.3),  # Top left
            FreeCAD.Vector(cx, cy, cz + h * 0.5),        # Close
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        if direction == 'y':
            return face.extrude(FreeCAD.Vector(0, depth, 0))
        else:
            return face.extrude(FreeCAD.Vector(0, -depth, 0))
    else:  # x directions
        points = [
            FreeCAD.Vector(cx, cy, cz + h * 0.5),
            FreeCAD.Vector(cx, cy + w/2, cz + h * 0.3),
            FreeCAD.Vector(cx, cy + w/2, cz - h * 0.2),
            FreeCAD.Vector(cx, cy, cz - h * 0.5),
            FreeCAD.Vector(cx, cy - w/2, cz - h * 0.2),
            FreeCAD.Vector(cx, cy - w/2, cz + h * 0.3),
            FreeCAD.Vector(cx, cy, cz + h * 0.5),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        if direction == 'x':
            return face.extrude(FreeCAD.Vector(depth, 0, 0))
        else:
            return face.extrude(FreeCAD.Vector(-depth, 0, 0))

def create_crystal_slot(cx, cy, cz, width, height, depth, direction='y'):
    """Create a crystal-shaped vent slot (octagonal)"""
    w = width / 2
    h = height / 2
    corner = min(w, h) * 0.3

    if direction in ['y', '-y']:
        points = [
            FreeCAD.Vector(cx - w + corner, cy, cz + h),
            FreeCAD.Vector(cx + w - corner, cy, cz + h),
            FreeCAD.Vector(cx + w, cy, cz + h - corner),
            FreeCAD.Vector(cx + w, cy, cz - h + corner),
            FreeCAD.Vector(cx + w - corner, cy, cz - h),
            FreeCAD.Vector(cx - w + corner, cy, cz - h),
            FreeCAD.Vector(cx - w, cy, cz - h + corner),
            FreeCAD.Vector(cx - w, cy, cz + h - corner),
            FreeCAD.Vector(cx - w + corner, cy, cz + h),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        if direction == 'y':
            return face.extrude(FreeCAD.Vector(0, depth, 0))
        else:
            return face.extrude(FreeCAD.Vector(0, -depth, 0))
    else:
        points = [
            FreeCAD.Vector(cx, cy - w + corner, cz + h),
            FreeCAD.Vector(cx, cy + w - corner, cz + h),
            FreeCAD.Vector(cx, cy + w, cz + h - corner),
            FreeCAD.Vector(cx, cy + w, cz - h + corner),
            FreeCAD.Vector(cx, cy + w - corner, cz - h),
            FreeCAD.Vector(cx, cy - w + corner, cz - h),
            FreeCAD.Vector(cx, cy - w, cz - h + corner),
            FreeCAD.Vector(cx, cy - w, cz + h - corner),
            FreeCAD.Vector(cx, cy - w + corner, cz + h),
        ]
        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        if direction == 'x':
            return face.extrude(FreeCAD.Vector(depth, 0, 0))
        else:
            return face.extrude(FreeCAD.Vector(-depth, 0, 0))

# ============================================
# COMPONENT DIMENSIONS
# ============================================
# Raspberry Pi 5
pi5_width = 85.0         # X dimension
pi5_depth = 56.0         # Y dimension
pi5_hole_spacing_x = 58.0  # Between mounting holes (X)
pi5_hole_spacing_y = 49.0  # Between mounting holes (Y)
pi5_hole_d = 2.7         # M2.5 hole diameter
pi5_standoff_h = 8.0     # Standoff height
pi5_standoff_d = 6.0     # Standoff outer diameter

# UGREEN M.2 SSD Enclosure
ssd_length = 125.0       # X dimension
ssd_width = 41.0         # Y dimension
ssd_height = 14.0        # Z dimension (thickness)
ssd_clamp_grip = 3.0     # How much clamp grips the SSD

# UGREEN USB-C Ethernet Adapter
eth_length = 62.0        # X dimension
eth_width = 25.0         # Y dimension
eth_height = 15.0        # Z dimension
eth_clamp_grip = 3.0     # How much clamp grips the adapter

# ============================================
# INTERNAL MOUNT STRUCTURES
# ============================================

def create_pi5_mount(base_z):
    """
    Create Raspberry Pi 5 mounting structure with 4 screw posts.
    Pi oriented with USB-C/HDMI edge facing LEFT panel (X=0) for port access.
    USB/Ethernet edge faces RIGHT.
    """
    inner_x = spire_base_x - 2 * wall
    inner_y = spire_base_y - 2 * wall

    # Position Pi with port edge near left wall
    # Pi 5 ports: USB-C power + 2x HDMI on one 85mm edge
    # Leave 8mm clearance from inner wall for port connectors
    pi_offset_x = wall + 8  # Near left wall with clearance for connectors
    pi_offset_y = wall + (inner_y - pi5_depth) / 2  # Centered in Y

    mount_parts = []

    # Calculate the 4 corner hole positions (Pi 5 uses corner mounting)
    hole_positions = [
        (pi_offset_x + (pi5_width - pi5_hole_spacing_x) / 2,
         pi_offset_y + (pi5_depth - pi5_hole_spacing_y) / 2),
        (pi_offset_x + (pi5_width + pi5_hole_spacing_x) / 2,
         pi_offset_y + (pi5_depth - pi5_hole_spacing_y) / 2),
        (pi_offset_x + (pi5_width - pi5_hole_spacing_x) / 2,
         pi_offset_y + (pi5_depth + pi5_hole_spacing_y) / 2),
        (pi_offset_x + (pi5_width + pi5_hole_spacing_x) / 2,
         pi_offset_y + (pi5_depth + pi5_hole_spacing_y) / 2),
    ]

    # Create 4 standoff posts
    for (hx, hy) in hole_positions:
        # Outer standoff cylinder
        standoff = Part.makeCylinder(pi5_standoff_d / 2, pi5_standoff_h)
        standoff.translate(FreeCAD.Vector(hx, hy, base_z))

        # Inner screw hole
        hole = Part.makeCylinder(pi5_hole_d / 2, pi5_standoff_h + 1)
        hole.translate(FreeCAD.Vector(hx, hy, base_z - 0.5))

        standoff = standoff.cut(hole)
        mount_parts.append(standoff)

    # Create base platform connecting the posts
    platform_margin = 5.0
    platform = Part.makeBox(
        pi5_width + platform_margin * 2,
        pi5_depth + platform_margin * 2,
        2.0  # Platform thickness
    )
    platform.translate(FreeCAD.Vector(
        pi_offset_x - platform_margin,
        pi_offset_y - platform_margin,
        base_z
    ))

    # Cut center opening for airflow
    airflow_cut = Part.makeBox(
        pi5_width - 20,
        pi5_depth - 20,
        5
    )
    airflow_cut.translate(FreeCAD.Vector(
        pi_offset_x + 10,
        pi_offset_y + 10,
        base_z - 1
    ))
    platform = platform.cut(airflow_cut)

    mount_parts.append(platform)

    # Fuse all parts
    result = mount_parts[0]
    for part in mount_parts[1:]:
        result = result.fuse(part)

    return result

def create_ssd_clamp_mount(base_z):
    """
    Create SSD clamp mount with snap-in rails (no screws).
    Uses friction-fit clips that grip the sides of the SSD enclosure.
    """
    # Center the SSD in the case
    inner_x = spire_base_x - 2 * wall
    inner_y = spire_base_y - 2 * wall

    ssd_offset_x = wall + (inner_x - ssd_length) / 2
    ssd_offset_y = wall + (inner_y - ssd_width) / 2

    mount_parts = []

    # Base rails (two parallel rails along the length)
    rail_height = 5.0
    rail_width = 8.0

    # Left rail
    left_rail = Part.makeBox(ssd_length + 10, rail_width, rail_height)
    left_rail.translate(FreeCAD.Vector(
        ssd_offset_x - 5,
        ssd_offset_y - rail_width,
        base_z
    ))
    mount_parts.append(left_rail)

    # Right rail
    right_rail = Part.makeBox(ssd_length + 10, rail_width, rail_height)
    right_rail.translate(FreeCAD.Vector(
        ssd_offset_x - 5,
        ssd_offset_y + ssd_width,
        base_z
    ))
    mount_parts.append(right_rail)

    # Snap-in clips (4 clips, 2 on each side)
    clip_width = 15.0
    clip_height = ssd_height + ssd_clamp_grip
    clip_thickness = 2.5
    clip_overhang = 4.0  # How much the clip extends over the SSD

    clip_positions = [
        # Left side clips
        (ssd_offset_x + 20, ssd_offset_y - clip_thickness, 'left'),
        (ssd_offset_x + ssd_length - 35, ssd_offset_y - clip_thickness, 'left'),
        # Right side clips
        (ssd_offset_x + 20, ssd_offset_y + ssd_width, 'right'),
        (ssd_offset_x + ssd_length - 35, ssd_offset_y + ssd_width, 'right'),
    ]

    for (cx, cy, side) in clip_positions:
        # Vertical part of clip
        clip_vert = Part.makeBox(clip_width, clip_thickness, clip_height)
        clip_vert.translate(FreeCAD.Vector(cx, cy, base_z + rail_height))

        # Horizontal overhang (the part that holds the SSD)
        clip_horiz = Part.makeBox(clip_width, clip_overhang, clip_thickness)
        if side == 'left':
            clip_horiz.translate(FreeCAD.Vector(
                cx,
                cy + clip_thickness,
                base_z + rail_height + clip_height - clip_thickness
            ))
        else:
            clip_horiz.translate(FreeCAD.Vector(
                cx,
                cy - clip_overhang + clip_thickness,
                base_z + rail_height + clip_height - clip_thickness
            ))

        # Angled entry ramp (for snap-in)
        # Create a small chamfer on the clip tip
        ramp_pts = []
        if side == 'left':
            ramp_pts = [
                FreeCAD.Vector(cx, cy + clip_thickness, base_z + rail_height + clip_height - clip_thickness),
                FreeCAD.Vector(cx + clip_width, cy + clip_thickness, base_z + rail_height + clip_height - clip_thickness),
                FreeCAD.Vector(cx + clip_width, cy + clip_thickness + clip_overhang, base_z + rail_height + clip_height),
                FreeCAD.Vector(cx, cy + clip_thickness + clip_overhang, base_z + rail_height + clip_height),
                FreeCAD.Vector(cx, cy + clip_thickness, base_z + rail_height + clip_height - clip_thickness),
            ]
        else:
            ramp_pts = [
                FreeCAD.Vector(cx, cy, base_z + rail_height + clip_height - clip_thickness),
                FreeCAD.Vector(cx + clip_width, cy, base_z + rail_height + clip_height - clip_thickness),
                FreeCAD.Vector(cx + clip_width, cy - clip_overhang + clip_thickness, base_z + rail_height + clip_height),
                FreeCAD.Vector(cx, cy - clip_overhang + clip_thickness, base_z + rail_height + clip_height),
                FreeCAD.Vector(cx, cy, base_z + rail_height + clip_height - clip_thickness),
            ]

        mount_parts.append(clip_vert)
        mount_parts.append(clip_horiz)

    # End stops to prevent SSD from sliding out
    stop_width = 5.0
    stop_height = 8.0

    # Front stop
    front_stop = Part.makeBox(stop_width, ssd_width + 2 * rail_width, stop_height)
    front_stop.translate(FreeCAD.Vector(
        ssd_offset_x - 5,
        ssd_offset_y - rail_width,
        base_z
    ))
    mount_parts.append(front_stop)

    # Rear stop
    rear_stop = Part.makeBox(stop_width, ssd_width + 2 * rail_width, stop_height)
    rear_stop.translate(FreeCAD.Vector(
        ssd_offset_x + ssd_length,
        ssd_offset_y - rail_width,
        base_z
    ))
    mount_parts.append(rear_stop)

    # Fuse all parts
    result = mount_parts[0]
    for part in mount_parts[1:]:
        result = result.fuse(part)

    return result

def create_ethernet_clamp_mount(base_z):
    """
    Create Ethernet adapter clamp mount with snap-in clips (no screws).
    Positioned with RJ45 port facing REAR panel for cable access.
    USB-C end faces front (connects to Pi internally).
    """
    inner_x = spire_base_x - 2 * wall
    inner_y = spire_base_y - 2 * wall

    # Position ethernet adapter with RJ45 port near rear wall
    # eth_length is along X axis, port is at high-X end facing rear
    eth_offset_x = wall + (inner_x - eth_length) / 2  # Centered in X
    eth_offset_y = wall + inner_y - eth_width - 10    # Near rear wall

    mount_parts = []

    # Base cradle (U-shaped)
    cradle_wall = 3.0
    cradle_height = 5.0

    # Bottom
    cradle_bottom = Part.makeBox(eth_length + 10, eth_width + cradle_wall * 2, cradle_height)
    cradle_bottom.translate(FreeCAD.Vector(
        eth_offset_x - 5,
        eth_offset_y - cradle_wall,
        base_z
    ))
    mount_parts.append(cradle_bottom)

    # Side walls of cradle
    left_wall = Part.makeBox(eth_length + 10, cradle_wall, eth_height + 3)
    left_wall.translate(FreeCAD.Vector(
        eth_offset_x - 5,
        eth_offset_y - cradle_wall,
        base_z + cradle_height
    ))
    mount_parts.append(left_wall)

    right_wall = Part.makeBox(eth_length + 10, cradle_wall, eth_height + 3)
    right_wall.translate(FreeCAD.Vector(
        eth_offset_x - 5,
        eth_offset_y + eth_width,
        base_z + cradle_height
    ))
    mount_parts.append(right_wall)

    # Retention clips (2 clips on top that snap over the adapter)
    clip_width = 12.0
    clip_overhang = 5.0
    clip_thickness = 2.0

    for i, cx in enumerate([eth_offset_x + 10, eth_offset_x + eth_length - 22]):
        # Left clip arm
        left_arm = Part.makeBox(clip_width, clip_thickness, eth_height + 5)
        left_arm.translate(FreeCAD.Vector(
            cx,
            eth_offset_y - cradle_wall - clip_thickness,
            base_z + cradle_height
        ))
        mount_parts.append(left_arm)

        # Left clip overhang
        left_over = Part.makeBox(clip_width, clip_overhang, clip_thickness)
        left_over.translate(FreeCAD.Vector(
            cx,
            eth_offset_y - cradle_wall,
            base_z + cradle_height + eth_height + 5 - clip_thickness
        ))
        mount_parts.append(left_over)

        # Right clip arm
        right_arm = Part.makeBox(clip_width, clip_thickness, eth_height + 5)
        right_arm.translate(FreeCAD.Vector(
            cx,
            eth_offset_y + eth_width + cradle_wall,
            base_z + cradle_height
        ))
        mount_parts.append(right_arm)

        # Right clip overhang
        right_over = Part.makeBox(clip_width, clip_overhang, clip_thickness)
        right_over.translate(FreeCAD.Vector(
            cx,
            eth_offset_y + eth_width + cradle_wall - clip_overhang,
            base_z + cradle_height + eth_height + 5 - clip_thickness
        ))
        mount_parts.append(right_over)

    # End stops
    front_stop = Part.makeBox(5, eth_width + cradle_wall * 2, eth_height)
    front_stop.translate(FreeCAD.Vector(
        eth_offset_x - 5,
        eth_offset_y - cradle_wall,
        base_z + cradle_height
    ))
    mount_parts.append(front_stop)

    # Fuse all parts
    result = mount_parts[0]
    for part in mount_parts[1:]:
        result = result.fuse(part)

    return result

# ============================================
# CREATE MAIN SHELL
# ============================================

def create_main_shell():
    """Create the main case shell with all panel openings"""

    # Outer shell
    outer = create_tapered_box(spire_base_x, spire_base_y, spire_height, spire_taper)

    # Inner cavity
    inner_offset = wall
    inner_base_x = spire_base_x - 2 * wall
    inner_base_y = spire_base_y - 2 * wall

    inner_base_pts = [
        FreeCAD.Vector(inner_offset, inner_offset, floor_h),
        FreeCAD.Vector(inner_offset + inner_base_x, inner_offset, floor_h),
        FreeCAD.Vector(inner_offset + inner_base_x, inner_offset + inner_base_y, floor_h),
        FreeCAD.Vector(inner_offset, inner_offset + inner_base_y, floor_h),
        FreeCAD.Vector(inner_offset, inner_offset, floor_h)
    ]
    inner_base_wire = Part.makePolygon(inner_base_pts)

    inner_top_x = inner_base_x * spire_taper
    inner_top_y = inner_base_y * spire_taper
    top_offset_x = (spire_base_x - top_x) / 2 + wall
    top_offset_y = (spire_base_y - top_y) / 2 + wall

    inner_top_pts = [
        FreeCAD.Vector(top_offset_x, top_offset_y, spire_height - wall),
        FreeCAD.Vector(top_offset_x + inner_top_x, top_offset_y, spire_height - wall),
        FreeCAD.Vector(top_offset_x + inner_top_x, top_offset_y + inner_top_y, spire_height - wall),
        FreeCAD.Vector(top_offset_x, top_offset_y + inner_top_y, spire_height - wall),
        FreeCAD.Vector(top_offset_x, top_offset_y, spire_height - wall)
    ]
    inner_top_wire = Part.makePolygon(inner_top_pts)

    inner_loft = Part.makeLoft([inner_base_wire, inner_top_wire], True)
    shell = outer.cut(inner_loft)

    return shell

def create_panel_opening(shell, side, margin=15):
    """Cut a panel opening in the shell for a given side"""

    z_bottom = panel_bottom
    z_top = spire_height - panel_top_margin

    # Get dimensions at bottom and top of opening
    off_b_x, off_b_y = get_offset_at_height(z_bottom)
    off_t_x, off_t_y = get_offset_at_height(z_top)

    x_b = get_x_at_height(z_bottom)
    y_b = get_y_at_height(z_bottom)
    x_t = get_x_at_height(z_top)
    y_t = get_y_at_height(z_top)

    if side == 'front':
        # Front panel (Y=0 face)
        bottom_pts = [
            FreeCAD.Vector(off_b_x + margin, -1, z_bottom),
            FreeCAD.Vector(off_b_x + x_b - margin, -1, z_bottom),
            FreeCAD.Vector(off_b_x + x_b - margin, wall + 2, z_bottom),
            FreeCAD.Vector(off_b_x + margin, wall + 2, z_bottom),
            FreeCAD.Vector(off_b_x + margin, -1, z_bottom),
        ]
        top_pts = [
            FreeCAD.Vector(off_t_x + margin, -1, z_top),
            FreeCAD.Vector(off_t_x + x_t - margin, -1, z_top),
            FreeCAD.Vector(off_t_x + x_t - margin, wall + 2, z_top),
            FreeCAD.Vector(off_t_x + margin, wall + 2, z_top),
            FreeCAD.Vector(off_t_x + margin, -1, z_top),
        ]
    elif side == 'rear':
        # Rear panel (Y=max face)
        bottom_pts = [
            FreeCAD.Vector(off_b_x + margin, spire_base_y - wall - 2, z_bottom),
            FreeCAD.Vector(off_b_x + x_b - margin, spire_base_y - wall - 2, z_bottom),
            FreeCAD.Vector(off_b_x + x_b - margin, spire_base_y + 1, z_bottom),
            FreeCAD.Vector(off_b_x + margin, spire_base_y + 1, z_bottom),
            FreeCAD.Vector(off_b_x + margin, spire_base_y - wall - 2, z_bottom),
        ]
        top_pts = [
            FreeCAD.Vector(off_t_x + margin, off_t_y + y_t - wall - 2, z_top),
            FreeCAD.Vector(off_t_x + x_t - margin, off_t_y + y_t - wall - 2, z_top),
            FreeCAD.Vector(off_t_x + x_t - margin, off_t_y + y_t + 1, z_top),
            FreeCAD.Vector(off_t_x + margin, off_t_y + y_t + 1, z_top),
            FreeCAD.Vector(off_t_x + margin, off_t_y + y_t - wall - 2, z_top),
        ]
    elif side == 'left':
        # Left panel (X=0 face)
        bottom_pts = [
            FreeCAD.Vector(-1, off_b_y + margin, z_bottom),
            FreeCAD.Vector(-1, off_b_y + y_b - margin, z_bottom),
            FreeCAD.Vector(wall + 2, off_b_y + y_b - margin, z_bottom),
            FreeCAD.Vector(wall + 2, off_b_y + margin, z_bottom),
            FreeCAD.Vector(-1, off_b_y + margin, z_bottom),
        ]
        top_pts = [
            FreeCAD.Vector(-1, off_t_y + margin, z_top),
            FreeCAD.Vector(-1, off_t_y + y_t - margin, z_top),
            FreeCAD.Vector(wall + 2, off_t_y + y_t - margin, z_top),
            FreeCAD.Vector(wall + 2, off_t_y + margin, z_top),
            FreeCAD.Vector(-1, off_t_y + margin, z_top),
        ]
    else:  # right
        # Right panel (X=max face)
        bottom_pts = [
            FreeCAD.Vector(spire_base_x - wall - 2, off_b_y + margin, z_bottom),
            FreeCAD.Vector(spire_base_x - wall - 2, off_b_y + y_b - margin, z_bottom),
            FreeCAD.Vector(spire_base_x + 1, off_b_y + y_b - margin, z_bottom),
            FreeCAD.Vector(spire_base_x + 1, off_b_y + margin, z_bottom),
            FreeCAD.Vector(spire_base_x - wall - 2, off_b_y + margin, z_bottom),
        ]
        top_pts = [
            FreeCAD.Vector(off_t_x + x_t - wall - 2, off_t_y + margin, z_top),
            FreeCAD.Vector(off_t_x + x_t - wall - 2, off_t_y + y_t - margin, z_top),
            FreeCAD.Vector(off_t_x + x_t + 1, off_t_y + y_t - margin, z_top),
            FreeCAD.Vector(off_t_x + x_t + 1, off_t_y + margin, z_top),
            FreeCAD.Vector(off_t_x + x_t - wall - 2, off_t_y + margin, z_top),
        ]

    bottom_wire = Part.makePolygon(bottom_pts)
    top_wire = Part.makePolygon(top_pts)

    try:
        opening = Part.makeLoft([bottom_wire, top_wire], True)
        return shell.cut(opening)
    except:
        # Fallback to simple box
        box = Part.makeBox(200, 200, z_top - z_bottom)
        return shell

def add_magnet_recesses(shell, side):
    """Add 6 magnet recesses around panel opening"""

    z_bottom = panel_bottom
    z_top = spire_height - panel_top_margin
    z_mid = (z_bottom + z_top) / 2

    magnet_positions = []

    # Calculate positions based on side
    if side == 'front':
        # Front face (Y near 0)
        off_b_x, _ = get_offset_at_height(z_bottom)
        off_t_x, _ = get_offset_at_height(z_top)
        off_m_x, _ = get_offset_at_height(z_mid)

        x_b = get_x_at_height(z_bottom)
        x_t = get_x_at_height(z_top)
        x_m = get_x_at_height(z_mid)

        # Left edge (2 magnets)
        magnet_positions.append((off_b_x + panel_margin + 8, wall/2, z_bottom + 20))
        magnet_positions.append((off_m_x + panel_margin + 8, wall/2, z_mid))
        # Right edge (2 magnets)
        magnet_positions.append((off_b_x + x_b - panel_margin - 8, wall/2, z_bottom + 20))
        magnet_positions.append((off_m_x + x_m - panel_margin - 8, wall/2, z_mid))
        # Top edge (2 magnets)
        magnet_positions.append((off_t_x + x_t/2 - 15, wall/2, z_top - 10))
        magnet_positions.append((off_t_x + x_t/2 + 15, wall/2, z_top - 10))

        direction = 'y'

    elif side == 'rear':
        off_b_x, off_b_y = get_offset_at_height(z_bottom)
        off_t_x, off_t_y = get_offset_at_height(z_top)
        off_m_x, off_m_y = get_offset_at_height(z_mid)

        x_b = get_x_at_height(z_bottom)
        x_t = get_x_at_height(z_top)
        x_m = get_x_at_height(z_mid)
        y_b = get_y_at_height(z_bottom)

        magnet_positions.append((off_b_x + panel_margin + 8, spire_base_y - wall/2, z_bottom + 20))
        magnet_positions.append((off_m_x + panel_margin + 8, off_m_y + get_y_at_height(z_mid) - wall/2, z_mid))
        magnet_positions.append((off_b_x + x_b - panel_margin - 8, spire_base_y - wall/2, z_bottom + 20))
        magnet_positions.append((off_m_x + x_m - panel_margin - 8, off_m_y + get_y_at_height(z_mid) - wall/2, z_mid))
        magnet_positions.append((off_t_x + x_t/2 - 15, off_t_y + get_y_at_height(z_top) - wall/2, z_top - 10))
        magnet_positions.append((off_t_x + x_t/2 + 15, off_t_y + get_y_at_height(z_top) - wall/2, z_top - 10))

        direction = '-y'

    elif side == 'left':
        _, off_b_y = get_offset_at_height(z_bottom)
        _, off_t_y = get_offset_at_height(z_top)
        _, off_m_y = get_offset_at_height(z_mid)

        y_b = get_y_at_height(z_bottom)
        y_t = get_y_at_height(z_top)
        y_m = get_y_at_height(z_mid)

        magnet_positions.append((wall/2, off_b_y + panel_margin + 8, z_bottom + 20))
        magnet_positions.append((wall/2, off_m_y + panel_margin + 8, z_mid))
        magnet_positions.append((wall/2, off_b_y + y_b - panel_margin - 8, z_bottom + 20))
        magnet_positions.append((wall/2, off_m_y + y_m - panel_margin - 8, z_mid))
        magnet_positions.append((wall/2, off_t_y + y_t/2 - 10, z_top - 10))
        magnet_positions.append((wall/2, off_t_y + y_t/2 + 10, z_top - 10))

        direction = 'x'

    else:  # right
        off_b_x, off_b_y = get_offset_at_height(z_bottom)
        off_t_x, off_t_y = get_offset_at_height(z_top)
        off_m_x, off_m_y = get_offset_at_height(z_mid)

        x_b = get_x_at_height(z_bottom)
        x_t = get_x_at_height(z_top)
        x_m = get_x_at_height(z_mid)
        y_b = get_y_at_height(z_bottom)
        y_t = get_y_at_height(z_top)
        y_m = get_y_at_height(z_mid)

        magnet_positions.append((spire_base_x - wall/2, off_b_y + panel_margin + 8, z_bottom + 20))
        magnet_positions.append((off_m_x + x_m - wall/2, off_m_y + panel_margin + 8, z_mid))
        magnet_positions.append((spire_base_x - wall/2, off_b_y + y_b - panel_margin - 8, z_bottom + 20))
        magnet_positions.append((off_m_x + x_m - wall/2, off_m_y + y_m - panel_margin - 8, z_mid))
        magnet_positions.append((off_t_x + x_t - wall/2, off_t_y + y_t/2 - 10, z_top - 10))
        magnet_positions.append((off_t_x + x_t - wall/2, off_t_y + y_t/2 + 10, z_top - 10))

        direction = '-x'

    # Create magnet recesses
    for pos in magnet_positions:
        cyl = Part.makeCylinder(magnet_d/2, magnet_recess + 1)

        if direction == 'y':
            cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
            cyl.translate(FreeCAD.Vector(pos[0], pos[1] - magnet_recess, pos[2]))
        elif direction == '-y':
            cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
            cyl.translate(FreeCAD.Vector(pos[0], pos[1] + 1, pos[2]))
        elif direction == 'x':
            cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
            cyl.translate(FreeCAD.Vector(pos[0] - magnet_recess, pos[1], pos[2]))
        else:  # -x
            cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -90)
            cyl.translate(FreeCAD.Vector(pos[0] + 1, pos[1], pos[2]))

        shell = shell.cut(cyl)

    return shell

# ============================================
# CREATE PANELS WITH PATTERNS
# ============================================

def create_front_panel_crystal_burst():
    """Create front panel with Crystal Burst pattern"""

    z_bottom = panel_bottom
    z_top = spire_height - panel_top_margin
    panel_h = z_top - z_bottom

    off_b_x, _ = get_offset_at_height(z_bottom)
    off_t_x, _ = get_offset_at_height(z_top)
    x_b = get_x_at_height(z_bottom)
    x_t = get_x_at_height(z_top)

    # Panel base shape (trapezoid)
    margin = panel_margin + tolerance
    bottom_pts = [
        FreeCAD.Vector(off_b_x + margin, 0, z_bottom),
        FreeCAD.Vector(off_b_x + x_b - margin, 0, z_bottom),
        FreeCAD.Vector(off_b_x + x_b - margin, panel_thick, z_bottom),
        FreeCAD.Vector(off_b_x + margin, panel_thick, z_bottom),
        FreeCAD.Vector(off_b_x + margin, 0, z_bottom),
    ]
    top_pts = [
        FreeCAD.Vector(off_t_x + margin, 0, z_top),
        FreeCAD.Vector(off_t_x + x_t - margin, 0, z_top),
        FreeCAD.Vector(off_t_x + x_t - margin, panel_thick, z_top),
        FreeCAD.Vector(off_t_x + margin, panel_thick, z_top),
        FreeCAD.Vector(off_t_x + margin, 0, z_top),
    ]

    bottom_wire = Part.makePolygon(bottom_pts)
    top_wire = Part.makePolygon(top_pts)
    panel = Part.makeLoft([bottom_wire, top_wire], True)

    # Center of panel
    cx = spire_base_x / 2
    cz = (z_bottom + z_top) / 2

    # Crystal Burst pattern - central large diamond
    central_diamond = create_diamond(cx, -1, cz, 25, panel_thick + 3, 'y')
    panel = panel.cut(central_diamond)

    # Radiating smaller diamonds in rings
    ring_radii = [25, 40, 55]
    diamond_sizes = [12, 10, 8]
    counts = [6, 8, 10]

    for ring_idx, (radius, size, count) in enumerate(zip(ring_radii, diamond_sizes, counts)):
        for i in range(count):
            angle = (i * 2 * math.pi / count) + (ring_idx * math.pi / count / 2)
            dx = radius * math.cos(angle)
            dz = radius * math.sin(angle)

            # Check if within panel bounds
            test_x = cx + dx
            test_z = cz + dz

            if test_z > z_bottom + 10 and test_z < z_top - 10:
                # Adjust x for taper at this height
                taper = get_taper_at_height(test_z)
                off_x, _ = get_offset_at_height(test_z)
                local_x = get_x_at_height(test_z)

                if test_x > off_x + margin + 10 and test_x < off_x + local_x - margin - 10:
                    diamond = create_diamond(test_x, -1, test_z, size, panel_thick + 3, 'y')
                    panel = panel.cut(diamond)

    # Add magnet recesses to panel (matching frame positions)
    magnet_positions = [
        (off_b_x + panel_margin + 8, z_bottom + 20),
        ((off_b_x + off_t_x)/2 + panel_margin + 8, cz),
        (off_b_x + x_b - panel_margin - 8, z_bottom + 20),
        ((off_b_x + off_t_x)/2 + x_b*0.95 - panel_margin - 8, cz),
        (off_t_x + x_t/2 - 15, z_top - 10),
        (off_t_x + x_t/2 + 15, z_top - 10),
    ]

    for pos in magnet_positions:
        cyl = Part.makeCylinder(magnet_d/2, magnet_recess + 0.5)
        cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
        cyl.translate(FreeCAD.Vector(pos[0], panel_thick - magnet_recess, pos[1]))
        panel = panel.cut(cyl)

    return panel

def create_rear_panel_fortress_gate():
    """Create rear panel with Fortress Gate / Hex Matrix pattern"""

    z_bottom = panel_bottom
    z_top = spire_height - panel_top_margin
    panel_h = z_top - z_bottom

    off_b_x, off_b_y = get_offset_at_height(z_bottom)
    off_t_x, off_t_y = get_offset_at_height(z_top)
    x_b = get_x_at_height(z_bottom)
    x_t = get_x_at_height(z_top)
    y_b = get_y_at_height(z_bottom)
    y_t = get_y_at_height(z_top)

    margin = panel_margin + tolerance

    # Panel base
    bottom_pts = [
        FreeCAD.Vector(off_b_x + margin, spire_base_y - panel_thick, z_bottom),
        FreeCAD.Vector(off_b_x + x_b - margin, spire_base_y - panel_thick, z_bottom),
        FreeCAD.Vector(off_b_x + x_b - margin, spire_base_y, z_bottom),
        FreeCAD.Vector(off_b_x + margin, spire_base_y, z_bottom),
        FreeCAD.Vector(off_b_x + margin, spire_base_y - panel_thick, z_bottom),
    ]
    top_pts = [
        FreeCAD.Vector(off_t_x + margin, off_t_y + y_t - panel_thick, z_top),
        FreeCAD.Vector(off_t_x + x_t - margin, off_t_y + y_t - panel_thick, z_top),
        FreeCAD.Vector(off_t_x + x_t - margin, off_t_y + y_t, z_top),
        FreeCAD.Vector(off_t_x + margin, off_t_y + y_t, z_top),
        FreeCAD.Vector(off_t_x + margin, off_t_y + y_t - panel_thick, z_top),
    ]

    bottom_wire = Part.makePolygon(bottom_pts)
    top_wire = Part.makePolygon(top_pts)
    panel = Part.makeLoft([bottom_wire, top_wire], True)

    cx = spire_base_x / 2
    cz = (z_bottom + z_top) / 2

    # Top section: Crystal slot vents for exhaust
    for i in range(5):
        slot_x = cx - 40 + i * 20
        slot_z = z_top - 25
        slot = create_crystal_slot(slot_x, spire_base_y + 1, slot_z, 12, 20, panel_thick + 3, '-y')
        panel = panel.cut(slot)

    # Middle section: Hexagonal grid (variable size)
    hex_sizes = [8, 7, 6, 5]
    for row in range(4):
        z_pos = cz - 15 + row * 18
        hex_size = hex_sizes[row % len(hex_sizes)]
        num_hexes = 5 + row % 2

        for i in range(num_hexes):
            hx = cx - 35 + i * 15 + (row % 2) * 7.5

            # Check bounds
            taper = get_taper_at_height(z_pos)
            off_x, off_y = get_offset_at_height(z_pos)
            local_x = get_x_at_height(z_pos)

            if hx > off_x + margin + 8 and hx < off_x + local_x - margin - 8:
                hex_shape = create_hexagon(hx, spire_base_y + 1, z_pos, hex_size, panel_thick + 3, '-y')
                panel = panel.cut(hex_shape)

    # Bottom section: Large diamond vents
    for i in range(3):
        dx = cx - 30 + i * 30
        dz = z_bottom + 25
        diamond = create_diamond(dx, spire_base_y + 1, dz, 15, panel_thick + 3, '-y')
        panel = panel.cut(diamond)

    # ===========================================
    # USB-C ETHERNET ADAPTER RJ45 PORT CUTOUT
    # ===========================================
    # Ethernet adapter positioned with RJ45 facing rear
    # Calculate adapter position (must match create_ethernet_clamp_mount)
    inner_x_local = spire_base_x - 2 * wall
    inner_y_local = spire_base_y - 2 * wall
    eth_offset_x = wall + (inner_x_local - eth_length) / 2

    # Ethernet mount Z position
    ssd_mount_height = 5 + ssd_height + ssd_clamp_grip + 5
    eth_base_z = floor_h + ssd_mount_height + 5
    # RJ45 port is at center height of adapter
    eth_port_z = eth_base_z + 5 + eth_height / 2

    # RJ45 port cutout (centered on adapter X position, at rear Y)
    # RJ45 is typically 16mm wide x 13mm tall
    rj45_cutout = Part.makeBox(18, panel_thick + 3, 14)
    rj45_cutout.translate(FreeCAD.Vector(
        eth_offset_x + eth_length / 2 - 9,  # Centered on adapter
        spire_base_y - panel_thick - 1,
        eth_port_z - 7
    ))
    panel = panel.cut(rj45_cutout)

    # Add magnet recesses
    magnet_positions = [
        (off_b_x + panel_margin + 8, z_bottom + 20),
        ((off_b_x + off_t_x)/2 + panel_margin + 8, cz),
        (off_b_x + x_b - panel_margin - 8, z_bottom + 20),
        ((off_b_x + off_t_x)/2 + x_b*0.95 - panel_margin - 8, cz),
        (off_t_x + x_t/2 - 15, z_top - 10),
        (off_t_x + x_t/2 + 15, z_top - 10),
    ]

    for pos in magnet_positions:
        cyl = Part.makeCylinder(magnet_d/2, magnet_recess + 0.5)
        cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
        cyl.translate(FreeCAD.Vector(pos[0], spire_base_y - panel_thick, pos[1]))
        panel = panel.cut(cyl)

    return panel

def create_left_panel_shield_array():
    """Create left panel with Shield Array pattern and port cutouts"""

    z_bottom = panel_bottom
    z_top = spire_height - panel_top_margin
    panel_h = z_top - z_bottom

    _, off_b_y = get_offset_at_height(z_bottom)
    _, off_t_y = get_offset_at_height(z_top)
    y_b = get_y_at_height(z_bottom)
    y_t = get_y_at_height(z_top)

    margin = panel_margin + tolerance

    # Panel base
    bottom_pts = [
        FreeCAD.Vector(0, off_b_y + margin, z_bottom),
        FreeCAD.Vector(0, off_b_y + y_b - margin, z_bottom),
        FreeCAD.Vector(panel_thick, off_b_y + y_b - margin, z_bottom),
        FreeCAD.Vector(panel_thick, off_b_y + margin, z_bottom),
        FreeCAD.Vector(0, off_b_y + margin, z_bottom),
    ]
    top_pts = [
        FreeCAD.Vector(0, off_t_y + margin, z_top),
        FreeCAD.Vector(0, off_t_y + y_t - margin, z_top),
        FreeCAD.Vector(panel_thick, off_t_y + y_t - margin, z_top),
        FreeCAD.Vector(panel_thick, off_t_y + margin, z_top),
        FreeCAD.Vector(0, off_t_y + margin, z_top),
    ]

    bottom_wire = Part.makePolygon(bottom_pts)
    top_wire = Part.makePolygon(top_pts)
    panel = Part.makeLoft([bottom_wire, top_wire], True)

    cy = spire_base_y / 2
    cz = (z_bottom + z_top) / 2

    # Shield pattern tessellation
    shield_size = 15
    rows = 4
    cols = 3

    for row in range(rows):
        for col in range(cols):
            sz = z_bottom + 25 + row * 28
            sy = cy - 20 + col * 20 + (row % 2) * 10

            # Check bounds
            _, off_y = get_offset_at_height(sz)
            local_y = get_y_at_height(sz)

            if sy > off_y + margin + 8 and sy < off_y + local_y - margin - 8:
                if sz > z_bottom + 15 and sz < z_top - 15:
                    shield = create_shield_shape(-1, sy, sz, shield_size, panel_thick + 3, 'x')
                    panel = panel.cut(shield)

    # Port cutouts for Raspberry Pi 5
    # Pi is positioned with USB-C/HDMI edge facing left (X=0)
    # Calculate actual positions based on Pi mount location

    # Pi mount position (must match create_pi5_mount)
    inner_y_local = spire_base_y - 2 * wall
    pi_offset_y = wall + (inner_y_local - pi5_depth) / 2

    # Pi board Z position (mount base + standoff height)
    # pi5_base_z is calculated in build_model, approximate here
    ssd_mount_height = 5 + ssd_height + ssd_clamp_grip + 5
    eth_mount_height = 5 + eth_height + 5
    pi_board_z = floor_h + ssd_mount_height + 5 + eth_mount_height + 5 + pi5_standoff_h

    # Pi 5 port positions from board edge (USB-C/HDMI edge):
    # USB-C power: 7.5mm from corner, 3.5mm tall
    # Micro HDMI 0: 22mm from corner, 3mm tall
    # Micro HDMI 1: 35mm from corner, 3mm tall
    # All ports are ~1mm above board bottom surface

    port_z_base = pi_board_z + 1  # Ports start 1mm above board

    # USB-C power port (for power supply)
    usbc_y = pi_offset_y + 7.5
    usbc_cutout = Part.makeBox(panel_thick + 3, 9, 4)
    usbc_cutout.translate(FreeCAD.Vector(-1, usbc_y - 4.5, port_z_base))
    panel = panel.cut(usbc_cutout)

    # Micro HDMI port 0
    hdmi0_y = pi_offset_y + 22
    hdmi0_cutout = Part.makeBox(panel_thick + 3, 8, 4)
    hdmi0_cutout.translate(FreeCAD.Vector(-1, hdmi0_y - 4, port_z_base))
    panel = panel.cut(hdmi0_cutout)

    # Micro HDMI port 1
    hdmi1_y = pi_offset_y + 35
    hdmi1_cutout = Part.makeBox(panel_thick + 3, 8, 4)
    hdmi1_cutout.translate(FreeCAD.Vector(-1, hdmi1_y - 4, port_z_base))
    panel = panel.cut(hdmi1_cutout)

    # Add magnet recesses
    magnet_positions = [
        (off_b_y + panel_margin + 8, z_bottom + 20),
        ((off_b_y + off_t_y)/2 + panel_margin + 8, cz),
        (off_b_y + y_b - panel_margin - 8, z_bottom + 20),
        ((off_b_y + off_t_y)/2 + y_b*0.95 - panel_margin - 8, cz),
        (off_t_y + y_t/2 - 10, z_top - 10),
        (off_t_y + y_t/2 + 10, z_top - 10),
    ]

    for pos in magnet_positions:
        cyl = Part.makeCylinder(magnet_d/2, magnet_recess + 0.5)
        cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90)
        cyl.translate(FreeCAD.Vector(panel_thick - magnet_recess, pos[0], pos[1]))
        panel = panel.cut(cyl)

    return panel

def create_right_panel_crystal_wave():
    """Create right panel with Crystal Wave pattern and cable exits"""

    z_bottom = panel_bottom
    z_top = spire_height - panel_top_margin
    panel_h = z_top - z_bottom

    off_b_x, off_b_y = get_offset_at_height(z_bottom)
    off_t_x, off_t_y = get_offset_at_height(z_top)
    x_b = get_x_at_height(z_bottom)
    x_t = get_x_at_height(z_top)
    y_b = get_y_at_height(z_bottom)
    y_t = get_y_at_height(z_top)

    margin = panel_margin + tolerance

    # Panel base
    bottom_pts = [
        FreeCAD.Vector(spire_base_x - panel_thick, off_b_y + margin, z_bottom),
        FreeCAD.Vector(spire_base_x - panel_thick, off_b_y + y_b - margin, z_bottom),
        FreeCAD.Vector(spire_base_x, off_b_y + y_b - margin, z_bottom),
        FreeCAD.Vector(spire_base_x, off_b_y + margin, z_bottom),
        FreeCAD.Vector(spire_base_x - panel_thick, off_b_y + margin, z_bottom),
    ]
    top_pts = [
        FreeCAD.Vector(off_t_x + x_t - panel_thick, off_t_y + margin, z_top),
        FreeCAD.Vector(off_t_x + x_t - panel_thick, off_t_y + y_t - margin, z_top),
        FreeCAD.Vector(off_t_x + x_t, off_t_y + y_t - margin, z_top),
        FreeCAD.Vector(off_t_x + x_t, off_t_y + margin, z_top),
        FreeCAD.Vector(off_t_x + x_t - panel_thick, off_t_y + margin, z_top),
    ]

    bottom_wire = Part.makePolygon(bottom_pts)
    top_wire = Part.makePolygon(top_pts)
    panel = Part.makeLoft([bottom_wire, top_wire], True)

    cy = spire_base_y / 2
    cz = (z_bottom + z_top) / 2

    # Crystal Wave pattern - sinusoidal lines with diamond nodes
    num_waves = 5
    points_per_wave = 8

    for wave_idx in range(num_waves):
        wave_z = z_bottom + 20 + wave_idx * 22

        if wave_z < z_top - 20:
            # Create wave with diamonds at peaks
            for i in range(points_per_wave):
                t = i / (points_per_wave - 1)

                _, off_y = get_offset_at_height(wave_z)
                local_y = get_y_at_height(wave_z)

                wave_y = off_y + margin + 10 + t * (local_y - 2*margin - 20)
                wave_offset = 8 * math.sin(t * 2 * math.pi)

                # Place diamond at wave peaks/troughs
                if i % 2 == 0:
                    diamond_size = 8 if abs(wave_offset) > 5 else 6
                    diamond = create_diamond(spire_base_x + 1, wave_y, wave_z + wave_offset,
                                           diamond_size, panel_thick + 3, '-x')
                    panel = panel.cut(diamond)

    # Horizontal crystal slots connecting waves
    for i in range(4):
        slot_z = z_bottom + 30 + i * 25
        if slot_z < z_top - 25:
            _, off_y = get_offset_at_height(slot_z)
            local_y = get_y_at_height(slot_z)
            slot_y = cy

            slot = create_crystal_slot(spire_base_x + 1, slot_y, slot_z,
                                      local_y - 2*margin - 30, 8, panel_thick + 3, '-x')
            panel = panel.cut(slot)

    # ===========================================
    # Pi 5 PORT CUTOUTS (USB/Ethernet edge faces RIGHT)
    # ===========================================
    # Pi is positioned with its USB-C/HDMI edge at left, so USB/ETH edge is at right
    # Pi mount position
    inner_y_local = spire_base_y - 2 * wall
    pi_offset_y = wall + (inner_y_local - pi5_depth) / 2

    # Calculate Pi board Z position
    ssd_mount_height = 5 + ssd_height + ssd_clamp_grip + 5
    eth_mount_height = 5 + eth_height + 5
    pi_board_z = floor_h + ssd_mount_height + 5 + eth_mount_height + 5 + pi5_standoff_h

    port_z_base = pi_board_z + 1  # Ports start 1mm above board

    # Pi 5 port positions from USB/Ethernet edge (measured from corner):
    # USB 3.0 port 0: ~9mm from corner, 7mm wide, 16mm tall (stacked)
    # USB 3.0 port 1: ~9mm from corner (same stack)
    # Ethernet RJ45: ~32mm from corner, 16mm wide, 13.5mm tall

    # USB 3.0 ports (stacked, one cutout)
    usb_y = pi_offset_y + pi5_depth - 9 - 7  # From opposite corner
    usb_cutout = Part.makeBox(panel_thick + 3, 16, 17)
    usb_cutout.translate(FreeCAD.Vector(spire_base_x - panel_thick - 1, usb_y - 8, port_z_base))
    panel = panel.cut(usb_cutout)

    # Ethernet RJ45 port
    eth_rj45_y = pi_offset_y + pi5_depth - 32 - 8
    eth_rj45_cutout = Part.makeBox(panel_thick + 3, 17, 14)
    eth_rj45_cutout.translate(FreeCAD.Vector(spire_base_x - panel_thick - 1, eth_rj45_y - 8, port_z_base))
    panel = panel.cut(eth_rj45_cutout)

    # ===========================================
    # CABLE EXIT HOLES (for internal connections)
    # ===========================================
    # SSD USB cable exit (SSD is at bottom, centered)
    ssd_z = floor_h + 5 + ssd_height / 2  # Middle of SSD
    ssd_exit = create_crystal_slot(spire_base_x + 1, cy, ssd_z, 20, 10, panel_thick + 3, '-x')
    panel = panel.cut(ssd_exit)

    # USB-C Ethernet adapter internal cable routing (not external - it's internal)
    # The adapter connects to Pi via USB-C internally, RJ45 faces rear panel

    # Add magnet recesses
    magnet_positions = [
        (off_b_y + panel_margin + 8, z_bottom + 20),
        ((off_b_y + off_t_y)/2 + panel_margin + 8, cz),
        (off_b_y + y_b - panel_margin - 8, z_bottom + 20),
        ((off_b_y + off_t_y)/2 + y_b*0.95 - panel_margin - 8, cz),
        (off_t_y + y_t/2 - 10, z_top - 10),
        (off_t_y + y_t/2 + 10, z_top - 10),
    ]

    for pos in magnet_positions:
        cyl = Part.makeCylinder(magnet_d/2, magnet_recess + 0.5)
        cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), -90)
        cyl.translate(FreeCAD.Vector(spire_base_x - panel_thick, pos[0], pos[1]))
        panel = panel.cut(cyl)

    return panel

# ============================================
# MAIN - BUILD THE COMPLETE MODEL
# ============================================

def build_model():
    """Build the complete Krypton NAS case with all removable panels and internal mounts"""

    # Create or get document
    if FreeCAD.ActiveDocument:
        doc = FreeCAD.ActiveDocument
    else:
        doc = FreeCAD.newDocument("KryptonNAS_AllPanels")

    print("Creating main shell...")
    shell = create_main_shell()

    print("Cutting panel openings...")
    for side in ['front', 'rear', 'left', 'right']:
        shell = create_panel_opening(shell, side)
        shell = add_magnet_recesses(shell, side)

    # ============================================
    # CREATE INTERNAL MOUNTS
    # ============================================
    # Stack order (bottom to top): SSD -> Ethernet -> Pi 5

    # Z positions for component stacking
    ssd_base_z = floor_h  # SSD at bottom (3mm from floor)
    ssd_mount_total_height = 5 + ssd_height + ssd_clamp_grip + 5  # rail + SSD + clip clearance

    eth_base_z = ssd_base_z + ssd_mount_total_height + 5  # Ethernet above SSD with 5mm gap
    eth_mount_total_height = 5 + eth_height + 5  # cradle + adapter + clearance

    pi5_base_z = eth_base_z + eth_mount_total_height + 5  # Pi 5 above Ethernet with 5mm gap

    print("Creating SSD clamp mount...")
    ssd_mount = create_ssd_clamp_mount(ssd_base_z)
    ssd_mount_obj = doc.addObject("Part::Feature", "SSD_ClampMount")
    ssd_mount_obj.Shape = ssd_mount

    print("Creating Ethernet clamp mount...")
    eth_mount = create_ethernet_clamp_mount(eth_base_z)
    eth_mount_obj = doc.addObject("Part::Feature", "Ethernet_ClampMount")
    eth_mount_obj.Shape = eth_mount

    print("Creating Pi 5 mount...")
    pi5_mount = create_pi5_mount(pi5_base_z)
    pi5_mount_obj = doc.addObject("Part::Feature", "Pi5_Mount")
    pi5_mount_obj.Shape = pi5_mount

    # Add shell to document (after mounts for proper layer ordering)
    shell_obj = doc.addObject("Part::Feature", "MainShell")
    shell_obj.Shape = shell

    print("Creating front panel (Crystal Burst)...")
    front_panel = create_front_panel_crystal_burst()
    front_obj = doc.addObject("Part::Feature", "FrontPanel_CrystalBurst")
    front_obj.Shape = front_panel

    print("Creating rear panel (Fortress Gate)...")
    rear_panel = create_rear_panel_fortress_gate()
    rear_obj = doc.addObject("Part::Feature", "RearPanel_FortressGate")
    rear_obj.Shape = rear_panel

    print("Creating left panel (Shield Array)...")
    left_panel = create_left_panel_shield_array()
    left_obj = doc.addObject("Part::Feature", "LeftPanel_ShieldArray")
    left_obj.Shape = left_panel

    print("Creating right panel (Crystal Wave)...")
    right_panel = create_right_panel_crystal_wave()
    right_obj = doc.addObject("Part::Feature", "RightPanel_CrystalWave")
    right_obj.Shape = right_panel

    doc.recompute()

    # Print mount positions for reference
    print("\n" + "="*50)
    print("Model complete! 8 objects created:")
    print("="*50)
    print("\nINTERNAL MOUNTS:")
    print(f"  - SSD_ClampMount (z={ssd_base_z}mm) - snap-in rails with 4 clips")
    print(f"  - Ethernet_ClampMount (z={eth_base_z}mm) - U-cradle with retention clips")
    print(f"  - Pi5_Mount (z={pi5_base_z}mm) - 4 corner posts with M2.5 holes")
    print("\nSHELL AND PANELS:")
    print("  - MainShell (with all panel openings and magnet recesses)")
    print("  - FrontPanel_CrystalBurst")
    print("  - RearPanel_FortressGate")
    print("  - LeftPanel_ShieldArray (with Pi port cutouts)")
    print("  - RightPanel_CrystalWave (with cable exits)")
    print("\nMOUNT NOTES:")
    print("  - SSD: Slide in from top, clips snap over edges (125x41x14mm)")
    print("  - Ethernet: Drop in and press down, clips snap over top (62x25x15mm)")
    print("  - Pi 5: Mount with M2.5 screws through 4 corner posts")

    return doc

# Run if executed directly
if __name__ == "__main__":
    build_model()
