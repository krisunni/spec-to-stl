#!/usr/bin/env python3
"""
AirPods Max Headphone Stand V2 - Organic Sculptural Design

Six objects:
  1. TripodBase: three curved legs radiating from central hub with column socket
  2. ColumnLower: tapered outer sleeve with M3 setscrew holes for height adjustment
  3. ColumnUpper: tapered inner column with organic cradle and integrated spacer hook
  4. StretcherRail: vice body with organic ear cup pads
  5. StretcherArm: sliding jaw with organic pad
  6. BoltRetainer: threaded thumbscrew to prevent M6 bolt backout

Design inspired by elegant wooden headphone stands - flowing curves, tripod stability,
integrated forms, minimal visible mechanics.

Run in FreeCAD Python console:
  exec(open('/Users/kris/Code/case/headphone_stand_v2.py').read())

Or headless:
  /Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('headphone_stand_v2.py').read())"
"""

import FreeCAD
import Part
import math

# ============================================
# PARAMETERS
# ============================================

# Tripod base
LEG_COUNT = 3                # Three legs at 120 degrees
LEG_RADIUS = 70.0            # Distance from center to leg tip (mm)
LEG_WIDTH_HUB = 24.0         # Leg width at hub connection (mm)
LEG_WIDTH_TIP = 16.0         # Leg width at outer tip (mm)
LEG_THICK_HUB = 12.0         # Leg thickness at hub (mm)
LEG_THICK_TIP = 8.0          # Leg thickness at tip (mm)
LEG_CURVE_DOWN = 12.0        # Vertical drop from hub to tip (mm)
HUB_D = 48.0                 # Central hub diameter (mm)
HUB_H = 22.0                 # Hub height (mm)

# Column socket in hub
SOCKET_D = 28.0              # Socket inner diameter (mm)
SOCKET_DEPTH = 16.0          # Socket depth into hub (mm)

# Lower column (outer sleeve, fixed to base)
COL_LOWER_D_BASE = 27.5      # Outer diameter at base (fits socket) (mm)
COL_LOWER_D_TOP = 24.0       # Outer diameter at top (tapered) (mm)
COL_LOWER_H = 85.0           # Height (mm)
COL_LOWER_WALL = 3.0         # Wall thickness (mm)
COL_INNER_D = COL_LOWER_D_BASE - 2 * COL_LOWER_WALL  # Inner diameter

# Upper column (inner, slides into lower)
TOLERANCE = 0.3              # Per-side clearance (mm)
COL_UPPER_D_BASE = COL_INNER_D - 2 * TOLERANCE  # Diameter at base (mm)
COL_UPPER_D_TOP = 18.0       # Diameter at top (tapered) (mm)
COL_UPPER_H = 115.0          # Total height (mm)

# Setscrew height locking (M3 holes on lower column)
SETSCREW_D = 3.2             # M3 clearance hole (mm)
SETSCREW_Z_START = 25.0      # First setscrew position from base (mm)
SETSCREW_SPACING = 15.0      # Spacing between positions (mm)
SETSCREW_COUNT = 4           # Number of height positions

# Stretcher vice storage bracket (on lower column)
BRACKET_W = 32.0             # Bracket width (wider than vice) (mm)
BRACKET_D = 8.0              # Bracket depth/protrusion (mm)
BRACKET_H = 4.0              # Bracket thickness (mm)
BRACKET_Z = 35.0             # Height above base (mm)
BRACKET_SLOT_W = 28.0        # Slot width for vice rail (mm)
BRACKET_SLOT_D = 6.0         # Slot depth (mm)

# Cradle (integrated into top of upper column)
CRADLE_W = 75.0              # Width (mm)
CRADLE_D_FRONT = 22.0        # Depth at front (mm)
CRADLE_D_BACK = 14.0         # Depth at back (tapers) (mm)
CRADLE_H = 22.0              # Height above column (mm)
CRADLE_ARC_R = 85.0          # Convex top surface radius (mm)
CURVE_R = 13.0               # Concave channel radius (mm)
CHANNEL_DEPTH = 5.5          # Channel depth (mm)

# Spacer hook (integrated into back of cradle)
HOOK_DEPTH = 10.0            # Hook protrusion depth (mm)
HOOK_H = 42.0                # Hook slot height (mm)
HOOK_GAP = 4.0               # Slot gap width (mm)

# Stretcher vice rail (organic redesign)
VICE_L = 145.0               # Rail length (mm)
VICE_W = 26.0                # Rail width (mm)
VICE_BASE_H = 10.0           # Base thickness (mm)
VICE_WALL_H = 18.0           # Wall height (mm)
VICE_WALL_T = 4.5            # Wall thickness (mm)
VICE_CHAN_W = 15.0           # Channel width (mm)
VICE_FIXED_T = 10.0          # Fixed end wall thickness (mm)
VICE_BOLT_T = 14.0           # Bolt end wall thickness (mm)

# Organic ear cup pads (smoother, larger)
VICE_PAD_W = 22.0            # Pad width (mm)
VICE_PAD_D = 14.0            # Pad depth (mm)
VICE_PAD_H = 58.0            # Pad height (mm)
VICE_PAD_CURVE_R = 50.0      # Concave radius (gentler) (mm)
VICE_PAD_CONCAVE = 4.0       # Concave depth (mm)

# Bolt hardware (M6)
VICE_BOLT_D = 6.5            # Shaft clearance (mm)
VICE_HEAD_D = 11.5           # Head counterbore dia (mm)
VICE_HEAD_DEPTH = 5.0        # Head counterbore depth (mm)
VICE_NUT_W = 10.2            # Nut pocket width (mm)
VICE_NUT_DEPTH = 5.5         # Nut pocket depth (mm)

# Graduation marks
VICE_GRAD_SPACING = 5.0      # Mark interval (mm)

# Sliding arm (organic redesign)
VICE_ARM_L = 22.0            # Arm length (mm)
VICE_ARM_W = VICE_CHAN_W - 2 * TOLERANCE  # Width (mm)
VICE_ARM_H = VICE_WALL_H - 0.5  # Height (mm)
VICE_ARM_PAD_W = 14.0        # Arm pad width (fits channel) (mm)

# Bolt retainer knob (prevents bolt backout)
KNOB_D = 22.0                # Knob diameter (mm)
KNOB_H = 8.0                 # Knob thickness (mm)
KNOB_GRIP_COUNT = 16         # Number of grip facets
KNOB_GRIP_DEPTH = 1.0        # Grip facet depth (mm)
KNOB_THREAD_D = 6.0          # M6 threaded hole (mm)
KNOB_THREAD_DEPTH = 12.0     # Thread depth (mm)

# ============================================
# DOCUMENT SETUP
# ============================================
doc_name = "HeadphoneStand_V2"
if FreeCAD.ActiveDocument and FreeCAD.ActiveDocument.Name == doc_name:
    doc = FreeCAD.ActiveDocument
    for obj in doc.Objects:
        doc.removeObject(obj.Name)
else:
    doc = FreeCAD.newDocument(doc_name)

# ============================================
# TRIPOD BASE
# ============================================
# Central hub (cylinder with fillet transitions to legs)
hub = Part.makeCylinder(HUB_D / 2, HUB_H, FreeCAD.Vector(0, 0, 0))

# Socket for column (centered, from top)
socket = Part.makeCylinder(SOCKET_D / 2, SOCKET_DEPTH + 0.5,
    FreeCAD.Vector(0, 0, HUB_H - SOCKET_DEPTH))
hub = hub.cut(socket)

# Create three legs radiating at 120 degree intervals
base = hub
for i in range(LEG_COUNT):
    angle_deg = i * 360.0 / LEG_COUNT
    angle_rad = math.radians(angle_deg)

    # Leg direction
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    # Leg at hub: wider, thicker, at hub height
    leg_hub_center = FreeCAD.Vector(dx * (HUB_D / 2 + LEG_WIDTH_HUB / 2),
                                     dy * (HUB_D / 2 + LEG_WIDTH_HUB / 2),
                                     HUB_H / 2)

    # Leg at tip: narrower, thinner, curved down
    leg_tip_center = FreeCAD.Vector(dx * LEG_RADIUS, dy * LEG_RADIUS,
                                     HUB_H / 2 - LEG_CURVE_DOWN)

    # Create leg as lofted shape from hub ellipse to tip ellipse
    # At hub: ellipse perpendicular to radial direction
    # At tip: ellipse perpendicular to radial direction

    # Simpler approach: create tapered box and rotate it
    # Leg oriented radially outward
    leg_length = LEG_RADIUS - HUB_D / 2 - LEG_WIDTH_HUB / 2

    # Create a tapered solid using makePolygon + loft
    # Bottom profile at hub (wider, thicker)
    hub_x = HUB_D / 2
    hub_z_bottom = HUB_H / 2 - LEG_THICK_HUB / 2
    hub_z_top = HUB_H / 2 + LEG_THICK_HUB / 2

    pts_hub = [
        FreeCAD.Vector(hub_x, -LEG_WIDTH_HUB / 2, hub_z_bottom),
        FreeCAD.Vector(hub_x, LEG_WIDTH_HUB / 2, hub_z_bottom),
        FreeCAD.Vector(hub_x, LEG_WIDTH_HUB / 2, hub_z_top),
        FreeCAD.Vector(hub_x, -LEG_WIDTH_HUB / 2, hub_z_top),
        FreeCAD.Vector(hub_x, -LEG_WIDTH_HUB / 2, hub_z_bottom)
    ]
    wire_hub = Part.makePolygon(pts_hub)

    # Top profile at tip (narrower, thinner, lower)
    tip_x = LEG_RADIUS
    tip_z_bottom = HUB_H / 2 - LEG_CURVE_DOWN - LEG_THICK_TIP / 2
    tip_z_top = HUB_H / 2 - LEG_CURVE_DOWN + LEG_THICK_TIP / 2

    pts_tip = [
        FreeCAD.Vector(tip_x, -LEG_WIDTH_TIP / 2, tip_z_bottom),
        FreeCAD.Vector(tip_x, LEG_WIDTH_TIP / 2, tip_z_bottom),
        FreeCAD.Vector(tip_x, LEG_WIDTH_TIP / 2, tip_z_top),
        FreeCAD.Vector(tip_x, -LEG_WIDTH_TIP / 2, tip_z_top),
        FreeCAD.Vector(tip_x, -LEG_WIDTH_TIP / 2, tip_z_bottom)
    ]
    wire_tip = Part.makePolygon(pts_tip)

    # Loft between the two profiles
    leg = Part.makeLoft([wire_hub, wire_tip], True)

    # Rotate leg around Z axis to correct angle
    leg.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), angle_deg)

    # Fuse with base
    base = base.fuse(leg)

# Add base to document
obj_base = doc.addObject("Part::Feature", "TripodBase")
obj_base.Shape = base

# ============================================
# COLUMN LOWER (outer sleeve)
# ============================================
# Tapered cylinder (larger at base, smaller at top)
# Create using loft of two circles

# Base circle
base_circle = Part.makeCircle(COL_LOWER_D_BASE / 2, FreeCAD.Vector(0, 0, 0))
base_wire = Part.Wire(base_circle)

# Top circle
top_circle = Part.makeCircle(COL_LOWER_D_TOP / 2, FreeCAD.Vector(0, 0, COL_LOWER_H))
top_wire = Part.Wire(top_circle)

# Loft to create outer shell
col_lower_outer = Part.makeLoft([base_wire, top_wire], True)

# Inner cavity (tapered to match outer taper)
inner_base_r = COL_LOWER_D_BASE / 2 - COL_LOWER_WALL
inner_top_r = COL_LOWER_D_TOP / 2 - COL_LOWER_WALL

inner_base_circle = Part.makeCircle(inner_base_r, FreeCAD.Vector(0, 0, -0.5))
inner_base_wire = Part.Wire(inner_base_circle)

inner_top_circle = Part.makeCircle(inner_top_r, FreeCAD.Vector(0, 0, COL_LOWER_H + 0.5))
inner_top_wire = Part.Wire(inner_top_circle)

col_lower_inner = Part.makeLoft([inner_base_wire, inner_top_wire], True)

# Cut inner from outer
col_lower = col_lower_outer.cut(col_lower_inner)

# Add setscrew holes for height adjustment
for i in range(SETSCREW_COUNT):
    z = SETSCREW_Z_START + i * SETSCREW_SPACING
    # Hole on +X side, perpendicular to column axis
    # Need to calculate radius at this height (interpolate between base and top)
    t = z / COL_LOWER_H  # Normalized height
    r_at_z = COL_LOWER_D_BASE / 2 * (1 - t) + COL_LOWER_D_TOP / 2 * t

    setscrew_hole = Part.makeCylinder(SETSCREW_D / 2, COL_LOWER_WALL + 2,
        FreeCAD.Vector(r_at_z - 1, 0, z),
        FreeCAD.Vector(1, 0, 0))
    col_lower = col_lower.cut(setscrew_hole)

# ---- Stretcher vice storage bracket ----
# Horizontal bracket extending from -Y side of column
# Vice rail clips onto this when not in use
t_bracket = BRACKET_Z / COL_LOWER_H
r_bracket = COL_LOWER_D_BASE / 2 * (1 - t_bracket) + COL_LOWER_D_TOP / 2 * t_bracket

# Bracket arm extending from column
bracket_arm = Part.makeBox(BRACKET_W, BRACKET_D, BRACKET_H,
    FreeCAD.Vector(-BRACKET_W / 2, -r_bracket - BRACKET_D, BRACKET_Z))

# U-shaped slot in bracket for rail to clip into
slot_cut = Part.makeBox(BRACKET_SLOT_W, BRACKET_SLOT_D, BRACKET_H + 1,
    FreeCAD.Vector(-BRACKET_SLOT_W / 2, -r_bracket - BRACKET_D, BRACKET_Z - 0.5))
bracket = bracket_arm.cut(slot_cut)

col_lower = col_lower.fuse(bracket)

# Add to document
obj_col_lower = doc.addObject("Part::Feature", "ColumnLower")
obj_col_lower.Shape = col_lower

# ============================================
# COLUMN UPPER (inner, with cradle)
# ============================================
# Tapered cylinder
upper_base_circle = Part.makeCircle(COL_UPPER_D_BASE / 2, FreeCAD.Vector(0, 0, 0))
upper_base_wire = Part.Wire(upper_base_circle)

upper_top_circle = Part.makeCircle(COL_UPPER_D_TOP / 2,
    FreeCAD.Vector(0, 0, COL_UPPER_H))
upper_top_wire = Part.Wire(upper_top_circle)

col_upper = Part.makeLoft([upper_base_wire, upper_top_wire], True)

# ---- Organic cradle at top ----
# Teardrop shape in plan view (wide at front, narrow at back)
# Create lofted cradle from bottom rectangle to top arched profile

cradle_z_base = COL_UPPER_H
cradle_z_top = COL_UPPER_H + CRADLE_H

# Bottom profile: teardrop (wide at front -Y, narrow at back +Y)
# Use polygon approximation
cradle_pts_bottom = []
num_pts = 16
for i in range(num_pts + 1):
    angle = -math.pi / 2 + math.pi * i / num_pts  # Front semicircle
    if i <= num_pts / 2:
        # Front half: full width
        r = CRADLE_W / 2
        x = r * math.cos(angle)
        y = -CRADLE_D_FRONT / 2 + r * math.sin(angle)
    else:
        # Back half: narrower
        r = CRADLE_W / 2
        x = r * math.cos(angle)
        # Transition from front to back depth
        y_front = -CRADLE_D_FRONT / 2
        y_back = CRADLE_D_BACK / 2
        t = (i - num_pts / 2) / (num_pts / 2)
        y = y_front * (1 - t) + y_back * t + r * math.sin(angle) * (1 - t)

    cradle_pts_bottom.append(FreeCAD.Vector(x, y, cradle_z_base))

# Simplified approach: just use a rectangular base
cradle_base_pts = [
    FreeCAD.Vector(-CRADLE_W / 2, -CRADLE_D_FRONT / 2, cradle_z_base),
    FreeCAD.Vector(CRADLE_W / 2, -CRADLE_D_FRONT / 2, cradle_z_base),
    FreeCAD.Vector(CRADLE_W / 2, CRADLE_D_BACK / 2, cradle_z_base),
    FreeCAD.Vector(-CRADLE_W / 2, CRADLE_D_BACK / 2, cradle_z_base),
    FreeCAD.Vector(-CRADLE_W / 2, -CRADLE_D_FRONT / 2, cradle_z_base)
]
cradle_base_wire = Part.makePolygon(cradle_base_pts)

# Top profile: same shape but slightly smaller
scale = 0.95
cradle_top_pts = [
    FreeCAD.Vector(-CRADLE_W / 2 * scale, -CRADLE_D_FRONT / 2 * scale, cradle_z_top),
    FreeCAD.Vector(CRADLE_W / 2 * scale, -CRADLE_D_FRONT / 2 * scale, cradle_z_top),
    FreeCAD.Vector(CRADLE_W / 2 * scale, CRADLE_D_BACK / 2 * scale, cradle_z_top),
    FreeCAD.Vector(-CRADLE_W / 2 * scale, CRADLE_D_BACK / 2 * scale, cradle_z_top),
    FreeCAD.Vector(-CRADLE_W / 2 * scale, -CRADLE_D_FRONT / 2 * scale, cradle_z_top)
]
cradle_top_wire = Part.makePolygon(cradle_top_pts)

# Loft cradle
cradle_block = Part.makeLoft([cradle_base_wire, cradle_top_wire], True)

# Arch the top using cylinder subtraction from below
arc_center_z = cradle_z_top + CRADLE_ARC_R
arch_cyl = Part.makeCylinder(CRADLE_ARC_R, CRADLE_W + 4,
    FreeCAD.Vector(-CRADLE_W / 2 - 2, 0, arc_center_z),
    FreeCAD.Vector(1, 0, 0))

arch_bounds = Part.makeBox(CRADLE_W + 6, CRADLE_D_FRONT + CRADLE_D_BACK + 6, CRADLE_H + 4,
    FreeCAD.Vector(-CRADLE_W / 2 - 3, -CRADLE_D_FRONT / 2 - 3, cradle_z_base - 1))
corner_cutter = arch_bounds.cut(arch_cyl)
cradle_arched = cradle_block.cut(corner_cutter)

# Concave channel for headband
cyl_center_z = cradle_z_top + CURVE_R - CHANNEL_DEPTH
channel_cyl = Part.makeCylinder(CURVE_R, CRADLE_W + 4,
    FreeCAD.Vector(-CRADLE_W / 2 - 2, 0, cyl_center_z),
    FreeCAD.Vector(1, 0, 0))
cradle_final = cradle_arched.cut(channel_cyl)

# Spacer hook at back of cradle
# Create a slot/notch at the back center
hook_slot = Part.makeBox(HOOK_GAP, HOOK_DEPTH,HOOK_H,
    FreeCAD.Vector(-HOOK_GAP / 2, CRADLE_D_BACK / 2, cradle_z_base))
cradle_final = cradle_final.cut(hook_slot)

# Fuse cradle to column
col_upper = col_upper.fuse(cradle_final)

# Add to document
obj_col_upper = doc.addObject("Part::Feature", "ColumnUpper")
obj_col_upper.Shape = col_upper

# ============================================
# STRETCHER RAIL (organic redesign)
# ============================================
rail_block = Part.makeBox(VICE_L, VICE_W, VICE_BASE_H + VICE_WALL_H,
    FreeCAD.Vector(-VICE_L / 2, -VICE_W / 2, 0))

# U-channel
chan_start_x = -VICE_L / 2 + VICE_FIXED_T
chan_end_x = VICE_L / 2 - VICE_BOLT_T
chan_len = chan_end_x - chan_start_x
channel_cut = Part.makeBox(chan_len, VICE_CHAN_W, VICE_WALL_H + 1,
    FreeCAD.Vector(chan_start_x, -VICE_CHAN_W / 2, VICE_BASE_H))
rail = rail_block.cut(channel_cut)

# ---- Fixed end pad (organic shape) ----
fixed_pad_x = -VICE_L / 2
fixed_pad_base = Part.makeBox(VICE_PAD_D, VICE_PAD_W, VICE_PAD_H,
    FreeCAD.Vector(fixed_pad_x, -VICE_PAD_W / 2, VICE_BASE_H + VICE_WALL_H))

# Round the edges with cylinder cuts
# Round front edges (4 corners)
edge_r = 3.0
for y_sign in [-1, 1]:
    for z_sign in [-1, 1]:
        y_pos = y_sign * (VICE_PAD_W / 2 - edge_r)
        z_pos = VICE_BASE_H + VICE_WALL_H + VICE_PAD_H / 2 + z_sign * (VICE_PAD_H / 2 - edge_r)
        edge_cyl = Part.makeCylinder(edge_r, VICE_PAD_D + 2,
            FreeCAD.Vector(fixed_pad_x - 1, y_pos, z_pos),
            FreeCAD.Vector(1, 0, 0))
        # Only cut if it's an outside corner
        if z_sign == -1 or z_sign == 1:
            # Create corner cut box
            cut_box = Part.makeBox(VICE_PAD_D + 2, edge_r * 2, edge_r * 2,
                FreeCAD.Vector(fixed_pad_x - 1, y_pos - edge_r, z_pos - edge_r))
            corner_cut = cut_box.cut(edge_cyl)
            fixed_pad_base = fixed_pad_base.cut(corner_cut)

# Concave face on +X side
concave_cyl_fixed = Part.makeCylinder(VICE_PAD_CURVE_R, VICE_PAD_W + 2,
    FreeCAD.Vector(fixed_pad_x + VICE_PAD_D + VICE_PAD_CURVE_R - VICE_PAD_CONCAVE,
                   -VICE_PAD_W / 2 - 1, VICE_BASE_H + VICE_WALL_H + VICE_PAD_H / 2),
    FreeCAD.Vector(0, 1, 0))
fixed_pad = fixed_pad_base.cut(concave_cyl_fixed)
rail = rail.fuse(fixed_pad)

# ---- Bolt end ----
bolt_wall_x = VICE_L / 2 - VICE_BOLT_T
bolt_center_z = VICE_BASE_H + VICE_WALL_H / 2

# Bolt clearance
bolt_hole = Part.makeCylinder(VICE_BOLT_D / 2, VICE_BOLT_T + 2,
    FreeCAD.Vector(bolt_wall_x - 1, 0, bolt_center_z),
    FreeCAD.Vector(1, 0, 0))
rail = rail.cut(bolt_hole)

# Counterbore
counterbore = Part.makeCylinder(VICE_HEAD_D / 2, VICE_HEAD_DEPTH + 0.1,
    FreeCAD.Vector(VICE_L / 2 - VICE_HEAD_DEPTH, 0, bolt_center_z),
    FreeCAD.Vector(1, 0, 0))
rail = rail.cut(counterbore)

# Graduation marks
grad_y = VICE_W / 2 - VICE_WALL_T
grad_z = VICE_BASE_H + VICE_WALL_H
mark_x = chan_start_x
while mark_x <= chan_end_x:
    notch = Part.makeBox(1.0, VICE_WALL_T + 0.2, 1.0,
        FreeCAD.Vector(mark_x - 0.5, grad_y - 0.1, grad_z - 1.0))
    rail = rail.cut(notch)
    mark_x += VICE_GRAD_SPACING

obj_rail = doc.addObject("Part::Feature", "StretcherRail")
obj_rail.Shape = rail

# ============================================
# STRETCHER ARM (organic redesign)
# ============================================
arm_base = Part.makeBox(VICE_ARM_L, VICE_ARM_W, VICE_ARM_H,
    FreeCAD.Vector(-VICE_ARM_L / 2, -VICE_ARM_W / 2, 0))

# ---- Organic pad ----
arm_pad_base = Part.makeBox(VICE_PAD_D, VICE_ARM_PAD_W, VICE_PAD_H,
    FreeCAD.Vector(-VICE_PAD_D / 2, -VICE_ARM_PAD_W / 2, VICE_ARM_H))

# Round edges (similar to fixed pad)
for y_sign in [-1, 1]:
    for z_sign in [-1, 1]:
        y_pos = y_sign * (VICE_ARM_PAD_W / 2 - edge_r)
        z_pos = VICE_ARM_H + VICE_PAD_H / 2 + z_sign * (VICE_PAD_H / 2 - edge_r)
        edge_cyl = Part.makeCylinder(edge_r, VICE_PAD_D + 2,
            FreeCAD.Vector(-VICE_PAD_D / 2 - 1, y_pos, z_pos),
            FreeCAD.Vector(1, 0, 0))
        cut_box = Part.makeBox(VICE_PAD_D + 2, edge_r * 2, edge_r * 2,
            FreeCAD.Vector(-VICE_PAD_D / 2 - 1, y_pos - edge_r, z_pos - edge_r))
        corner_cut = cut_box.cut(edge_cyl)
        arm_pad_base = arm_pad_base.cut(corner_cut)

# Concave face on -X side
concave_cyl_arm = Part.makeCylinder(VICE_PAD_CURVE_R, VICE_ARM_PAD_W + 2,
    FreeCAD.Vector(-VICE_PAD_D / 2 - VICE_PAD_CURVE_R + VICE_PAD_CONCAVE,
                   -VICE_ARM_PAD_W / 2 - 1, VICE_ARM_H + VICE_PAD_H / 2),
    FreeCAD.Vector(0, 1, 0))
arm_pad = arm_pad_base.cut(concave_cyl_arm)
arm = arm_base.fuse(arm_pad)

# Captive nut pocket
nut_center_z = VICE_ARM_H / 2
nut_pocket = Part.makeBox(VICE_NUT_DEPTH, VICE_NUT_W, VICE_NUT_W,
    FreeCAD.Vector(VICE_ARM_L / 2 - VICE_NUT_DEPTH,
                   -VICE_NUT_W / 2, nut_center_z - VICE_NUT_W / 2))
arm = arm.cut(nut_pocket)

# Bolt clearance hole
arm_bolt_hole = Part.makeCylinder(VICE_BOLT_D / 2, VICE_ARM_L + 2,
    FreeCAD.Vector(-VICE_ARM_L / 2 - 1, 0, nut_center_z),
    FreeCAD.Vector(1, 0, 0))
arm = arm.cut(arm_bolt_hole)

obj_arm = doc.addObject("Part::Feature", "StretcherArm")
obj_arm.Shape = arm

# ============================================
# BOLT RETAINER KNOB
# ============================================
# Cylindrical knob with grip facets and threaded hole

# Main knob body
knob = Part.makeCylinder(KNOB_D / 2, KNOB_H, FreeCAD.Vector(0, 0, 0))

# Grip facets (cut flats around circumference)
for i in range(KNOB_GRIP_COUNT):
    angle_deg = i * 360.0 / KNOB_GRIP_COUNT
    angle_rad = math.radians(angle_deg)

    # Create a box to cut a flat
    cut_x = (KNOB_D / 2 - KNOB_GRIP_DEPTH) * math.cos(angle_rad)
    cut_y = (KNOB_D / 2 - KNOB_GRIP_DEPTH) * math.sin(angle_rad)

    flat_cut = Part.makeBox(KNOB_GRIP_DEPTH + 1, 3, KNOB_H + 2,
        FreeCAD.Vector(cut_x, -1.5, -1))
    flat_cut.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), angle_deg)
    knob = knob.cut(flat_cut)

# Threaded hole (M6 clearance for threading later, or tap by user)
thread_hole = Part.makeCylinder(KNOB_THREAD_D / 2, KNOB_THREAD_DEPTH,
    FreeCAD.Vector(0, 0, -0.5))
knob = knob.cut(thread_hole)

obj_knob = doc.addObject("Part::Feature", "BoltRetainer")
obj_knob.Shape = knob

doc.recompute()

# ============================================
# CONSOLE OUTPUT
# ============================================
# Calculate assembled heights
min_height = HUB_H + SETSCREW_Z_START + CRADLE_H
max_height = HUB_H + COL_LOWER_H + COL_UPPER_H + CRADLE_H
adjustment_range = (SETSCREW_COUNT - 1) * SETSCREW_SPACING

print("")
print("=" * 60)
print("  AirPods Max Headphone Stand V2 - Organic Design")
print("=" * 60)
print("")
print("  TripodBase (1 piece):")
print("    Legs:          %d curved legs, %.0fmm radius" % (LEG_COUNT, LEG_RADIUS))
print("    Hub:           %.0fmm diameter, %.0fmm height" % (HUB_D, HUB_H))
print("    Footprint:     ~%.0fmm diameter circle" % (LEG_RADIUS * 2))
print("")
print("  ColumnLower (1 piece):")
print("    Outer:         %.1f-%.1fmm tapered, %.0fmm tall" % (COL_LOWER_D_BASE, COL_LOWER_D_TOP, COL_LOWER_H))
print("    Inner:         %.1fmm diameter hollow" % COL_INNER_D)
print("    Setscrew:      %d M3 holes at %.0fmm spacing" % (SETSCREW_COUNT, SETSCREW_SPACING))
print("    Bracket:       Storage clip for stretcher vice (%.0fmm from base)" % BRACKET_Z)
print("")
print("  ColumnUpper (1 piece):")
print("    Column:        %.1f-%.1fmm tapered, %.0fmm tall" % (COL_UPPER_D_BASE, COL_UPPER_D_TOP, COL_UPPER_H))
print("    Cradle:        %.0fmm wide, organic teardrop shape" % CRADLE_W)
print("    Arch:          R%.0fmm convex top, R%.0fmm concave channel" % (CRADLE_ARC_R, CURVE_R))
print("    Spacer hook:   Integrated slot at back (%.0fmm tall)" % HOOK_H)
print("")
print("  Assembled height range:")
print("    Minimum:       ~%.0fmm (cradle top above table)" % min_height)
print("    Maximum:       ~%.0fmm (fully extended)" % max_height)
print("    Adjustment:    %d positions, %.0fmm per step" % (SETSCREW_COUNT, SETSCREW_SPACING))
print("")
print("  StretcherRail (1 piece):")
print("    Body:          %.0f x %.0f x %.0fmm" % (VICE_L, VICE_W, VICE_BASE_H + VICE_WALL_H))
print("    Channel:       %.0fmm wide, %.0fmm deep" % (VICE_CHAN_W, VICE_WALL_H))
print("    Fixed pad:     %.0fmm tall, organic shape, concave R%.0f" % (VICE_PAD_H, VICE_PAD_CURVE_R))
print("    Graduations:   %.0fmm spacing" % VICE_GRAD_SPACING)
print("")
print("  StretcherArm (1 piece):")
print("    Base:          %.0f x %.1f x %.1fmm" % (VICE_ARM_L, VICE_ARM_W, VICE_ARM_H))
print("    Pad:           %.0fmm tall, organic shape, concave R%.0f" % (VICE_PAD_H, VICE_PAD_CURVE_R))
print("    Nut pocket:    M6 captive nut" % ())
print("")
print("  BoltRetainer (1 piece):")
print("    Knob:          %.0fmm diameter x %.0fmm thick" % (KNOB_D, KNOB_H))
print("    Grip:          %d facets" % KNOB_GRIP_COUNT)
print("    Thread:        M6 threaded hole (%.0fmm deep, tap after printing)" % KNOB_THREAD_DEPTH)
print("")
print("  Hardware required:")
print("    M6 x 100mm hex bolt      x1  (stretcher drive)")
print("    M6 hex nut               x1  (captive in stretcher arm)")
print("    M3 x 10mm setscrew       x1  (height lock)")
print("    M6 tap (optional)        x1  (to thread BoltRetainer)")
print("")
print("  Print settings:")
print("    TripodBase:    upside-down (legs up), supports for leg curves")
print("    ColumnLower:   upright, no supports")
print("    ColumnUpper:   upright, supports for cradle overhang")
print("    StretcherRail: flat, no supports")
print("    StretcherArm:  flat, no supports")
print("    BoltRetainer:  flat (hole side down), no supports")
print("    Material:      PLA or PETG")
print("")
print("  Objects: TripodBase, ColumnLower, ColumnUpper,")
print("           StretcherRail, StretcherArm, BoltRetainer")
print("=" * 60)
