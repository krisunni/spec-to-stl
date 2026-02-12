#!/usr/bin/env python3
"""
AirPods Max Headband Spacer - Graduated Wedge

A tapered block that slides between the mesh canopy and the steel frame
at the top of the headband. Inserting it further spreads the frame arms
apart, reducing clamping force. Continuously adjustable with graduation
notches for repeatable positioning.

Run in FreeCAD Python console:
  exec(open('/Users/kris/Code/case/headband_spacer.py').read())

Or headless:
  /Applications/FreeCAD.app/Contents/MacOS/FreeCAD -c "exec(open('headband_spacer.py').read())"
"""

import FreeCAD
import Part
import math

# ============================================
# PARAMETERS
# ============================================
LENGTH = 80.0          # Along headband direction (mm)
WIDTH_NARROW = 37.0    # Narrow end - matches natural frame gap (mm)
WIDTH_WIDE = 47.0      # Wide end - max +10mm stretch (mm)
THICKNESS = 8.0        # Fits in gap between mesh and frame (mm)

GROOVE_WIDTH = 5.0     # Channel for frame rail (mm)
GROOVE_DEPTH = 2.0     # Holds spacer laterally (mm)

NOTCH_SPACING = 16.0   # Distance between graduation marks (mm)
NOTCH_COUNT = 4        # Number of graduation notches
NOTCH_WIDTH = 1.0      # V-notch opening width (mm)
NOTCH_DEPTH = 1.0      # V-notch depth into top face (mm)

CHAMFER = 1.0          # Leading edge chamfer for insertion (mm)

# ============================================
# DOCUMENT SETUP
# ============================================
doc_name = "HeadbandSpacer"
if FreeCAD.ActiveDocument and FreeCAD.ActiveDocument.Name == doc_name:
    doc = FreeCAD.ActiveDocument
    for obj in doc.Objects:
        doc.removeObject(obj.Name)
else:
    doc = FreeCAD.newDocument(doc_name)

# ============================================
# WEDGE BODY - Loft between narrow and wide rectangles
# ============================================
# Narrow end at y=0, wide end at y=LENGTH
# Body centered on X, sitting on Z=0

def make_rect_wire(width, thickness, y_pos):
    """Create a closed rectangular wire at a given Y position, centered on X."""
    hw = width / 2.0
    pts = [
        FreeCAD.Vector(-hw, y_pos, 0),
        FreeCAD.Vector( hw, y_pos, 0),
        FreeCAD.Vector( hw, y_pos, thickness),
        FreeCAD.Vector(-hw, y_pos, thickness),
        FreeCAD.Vector(-hw, y_pos, 0),  # close the wire
    ]
    wire = Part.makePolygon(pts)
    return wire

narrow_wire = make_rect_wire(WIDTH_NARROW, THICKNESS, 0)
wide_wire = make_rect_wire(WIDTH_WIDE, THICKNESS, LENGTH)

wedge = Part.makeLoft([narrow_wire, wide_wire], True)

# ============================================
# FRAME RAIL GROOVES
# ============================================
# Two channels along the top face (Z=THICKNESS), one at each side edge.
# Each groove runs the full length and is inset from the outer edge.
# The groove sits at the outer edge of the top face so the frame rail
# slots into it from the side.

def make_groove(x_center, y_start, y_end, width, depth, z_top):
    """Create a groove box for cutting."""
    hw = width / 2.0
    # Groove cut from top face downward
    pts_bottom = [
        FreeCAD.Vector(x_center - hw, y_start, z_top - depth),
        FreeCAD.Vector(x_center + hw, y_start, z_top - depth),
        FreeCAD.Vector(x_center + hw, y_start, z_top + 0.1),
        FreeCAD.Vector(x_center - hw, y_start, z_top + 0.1),
        FreeCAD.Vector(x_center - hw, y_start, z_top - depth),
    ]
    pts_top = [
        FreeCAD.Vector(x_center - hw, y_end, z_top - depth),
        FreeCAD.Vector(x_center + hw, y_end, z_top - depth),
        FreeCAD.Vector(x_center + hw, y_end, z_top + 0.1),
        FreeCAD.Vector(x_center - hw, y_end, z_top + 0.1),
        FreeCAD.Vector(x_center - hw, y_end, z_top - depth),
    ]
    wire_b = Part.makePolygon(pts_bottom)
    wire_t = Part.makePolygon(pts_top)
    return Part.makeLoft([wire_b, wire_t], True)

# The grooves need to follow the taper of the wedge. At y=0 the width is
# WIDTH_NARROW, at y=LENGTH it is WIDTH_WIDE. The groove center at each
# Y position tracks the edge of the wedge at that Y.
# We approximate with a loft between groove cross-sections at each end.

# Left groove (negative X side)
def make_tapered_groove(side_sign):
    """Create a groove that follows the tapered edge.
    side_sign: -1 for left, +1 for right."""
    # At narrow end (y=0): edge is at side_sign * WIDTH_NARROW/2
    # Groove is inset by GROOVE_WIDTH/2 from edge
    narrow_edge = side_sign * WIDTH_NARROW / 2.0
    narrow_center = narrow_edge - side_sign * GROOVE_WIDTH / 2.0

    # At wide end (y=LENGTH): edge is at side_sign * WIDTH_WIDE/2
    wide_edge = side_sign * WIDTH_WIDE / 2.0
    wide_center = wide_edge - side_sign * GROOVE_WIDTH / 2.0

    ghw = GROOVE_WIDTH / 2.0
    z_top = THICKNESS

    pts_narrow = [
        FreeCAD.Vector(narrow_center - ghw, -0.1, z_top - GROOVE_DEPTH),
        FreeCAD.Vector(narrow_center + ghw, -0.1, z_top - GROOVE_DEPTH),
        FreeCAD.Vector(narrow_center + ghw, -0.1, z_top + 0.1),
        FreeCAD.Vector(narrow_center - ghw, -0.1, z_top + 0.1),
        FreeCAD.Vector(narrow_center - ghw, -0.1, z_top - GROOVE_DEPTH),
    ]
    pts_wide = [
        FreeCAD.Vector(wide_center - ghw, LENGTH + 0.1, z_top - GROOVE_DEPTH),
        FreeCAD.Vector(wide_center + ghw, LENGTH + 0.1, z_top - GROOVE_DEPTH),
        FreeCAD.Vector(wide_center + ghw, LENGTH + 0.1, z_top + 0.1),
        FreeCAD.Vector(wide_center - ghw, LENGTH + 0.1, z_top + 0.1),
        FreeCAD.Vector(wide_center - ghw, LENGTH + 0.1, z_top - GROOVE_DEPTH),
    ]
    wire_n = Part.makePolygon(pts_narrow)
    wire_w = Part.makePolygon(pts_wide)
    return Part.makeLoft([wire_n, wire_w], True)

groove_left = make_tapered_groove(-1)
groove_right = make_tapered_groove(1)

shape = wedge.cut(groove_left)
shape = shape.cut(groove_right)

# ============================================
# GRADUATION NOTCHES
# ============================================
# V-shaped cuts across the top face at regular intervals.
# Each notch is a triangular prism running across the full width.
# First notch at NOTCH_SPACING from narrow end, then every NOTCH_SPACING.

for i in range(NOTCH_COUNT):
    y_pos = NOTCH_SPACING * (i + 1)
    if y_pos > LENGTH:
        break

    # Width at this Y position (linear interpolation)
    t = y_pos / LENGTH
    w_at_y = WIDTH_NARROW + t * (WIDTH_WIDE - WIDTH_NARROW)
    hw = w_at_y / 2.0 + 1.0  # extend past edges to ensure full cut

    z_top = THICKNESS
    half_nw = NOTCH_WIDTH / 2.0

    # V-notch: triangle cross-section, extruded across width
    # Points form a triangular prism along X axis
    v1 = FreeCAD.Vector(-hw, y_pos - half_nw, z_top + 0.1)
    v2 = FreeCAD.Vector(-hw, y_pos + half_nw, z_top + 0.1)
    v3 = FreeCAD.Vector(-hw, y_pos, z_top - NOTCH_DEPTH)

    v4 = FreeCAD.Vector(hw, y_pos - half_nw, z_top + 0.1)
    v5 = FreeCAD.Vector(hw, y_pos + half_nw, z_top + 0.1)
    v6 = FreeCAD.Vector(hw, y_pos, z_top - NOTCH_DEPTH)

    # Build triangular prism from faces
    tri1 = Part.Face(Part.makePolygon([v1, v2, v3, v1]))
    tri2 = Part.Face(Part.makePolygon([v4, v5, v6, v4]))
    rect1 = Part.Face(Part.makePolygon([v1, v4, v6, v3, v1]))
    rect2 = Part.Face(Part.makePolygon([v2, v5, v6, v3, v2]))
    rect3 = Part.Face(Part.makePolygon([v1, v4, v5, v2, v1]))

    notch_shell = Part.Shell([tri1, tri2, rect1, rect2, rect3])
    notch_solid = Part.Solid(notch_shell)

    shape = shape.cut(notch_solid)

# ============================================
# LEADING EDGE CHAMFER
# ============================================
# Chamfer the narrow end (y=0) edges for easy insertion.
# Cut a triangular prism off the leading edge on both Z faces.

hw_narrow = WIDTH_NARROW / 2.0 + 0.1

# Bottom leading chamfer (Z=0 face, y=0 edge)
c1 = FreeCAD.Vector(-hw_narrow, -0.1, -0.1)
c2 = FreeCAD.Vector(-hw_narrow, CHAMFER, -0.1)
c3 = FreeCAD.Vector(-hw_narrow, -0.1, CHAMFER)

c4 = FreeCAD.Vector(hw_narrow, -0.1, -0.1)
c5 = FreeCAD.Vector(hw_narrow, CHAMFER, -0.1)
c6 = FreeCAD.Vector(hw_narrow, -0.1, CHAMFER)

tri_b1 = Part.Face(Part.makePolygon([c1, c2, c3, c1]))
tri_b2 = Part.Face(Part.makePolygon([c4, c5, c6, c4]))
rect_b1 = Part.Face(Part.makePolygon([c1, c4, c5, c2, c1]))
rect_b2 = Part.Face(Part.makePolygon([c1, c4, c6, c3, c1]))
rect_b3 = Part.Face(Part.makePolygon([c2, c5, c6, c3, c2]))

chamfer_bottom_shell = Part.Shell([tri_b1, tri_b2, rect_b1, rect_b2, rect_b3])
chamfer_bottom = Part.Solid(chamfer_bottom_shell)
shape = shape.cut(chamfer_bottom)

# Top leading chamfer (Z=THICKNESS face, y=0 edge)
z_t = THICKNESS
c1t = FreeCAD.Vector(-hw_narrow, -0.1, z_t + 0.1)
c2t = FreeCAD.Vector(-hw_narrow, CHAMFER, z_t + 0.1)
c3t = FreeCAD.Vector(-hw_narrow, -0.1, z_t - CHAMFER)

c4t = FreeCAD.Vector(hw_narrow, -0.1, z_t + 0.1)
c5t = FreeCAD.Vector(hw_narrow, CHAMFER, z_t + 0.1)
c6t = FreeCAD.Vector(hw_narrow, -0.1, z_t - CHAMFER)

tri_t1 = Part.Face(Part.makePolygon([c1t, c2t, c3t, c1t]))
tri_t2 = Part.Face(Part.makePolygon([c4t, c5t, c6t, c4t]))
rect_t1 = Part.Face(Part.makePolygon([c1t, c4t, c5t, c2t, c1t]))
rect_t2 = Part.Face(Part.makePolygon([c1t, c4t, c6t, c3t, c1t]))
rect_t3 = Part.Face(Part.makePolygon([c2t, c5t, c6t, c3t, c2t]))

chamfer_top_shell = Part.Shell([tri_t1, tri_t2, rect_t1, rect_t2, rect_t3])
chamfer_top = Part.Solid(chamfer_top_shell)
shape = shape.cut(chamfer_top)

# ============================================
# ADD TO DOCUMENT
# ============================================
obj = doc.addObject("Part::Feature", "HeadbandSpacer")
obj.Shape = shape
doc.recompute()

# ============================================
# CONSOLE OUTPUT
# ============================================
bb = shape.BoundBox
print("")
print("=" * 50)
print("  AirPods Max Headband Spacer")
print("=" * 50)
print("")
print("  Dimensions:")
print("    Length:       %.1f mm" % bb.YLength)
print("    Narrow end:   %.1f mm (zero stretch)" % WIDTH_NARROW)
print("    Wide end:     %.1f mm (+%.1f mm stretch)" % (WIDTH_WIDE, WIDTH_WIDE - WIDTH_NARROW))
print("    Thickness:    %.1f mm" % THICKNESS)
print("")
print("  Graduation notches (from narrow end):")
for i in range(NOTCH_COUNT):
    y = NOTCH_SPACING * (i + 1)
    stretch = (WIDTH_WIDE - WIDTH_NARROW) * (y / LENGTH)
    print("    Notch %d: %dmm = +%.1fmm stretch" % (i + 1, int(y), stretch))
print("")
print("  Print settings:")
print("    Orientation:  flat (wide face on bed)")
print("    Supports:     none")
print("    Layer height: 0.16mm")
print("    Infill:       100% solid")
print("    Material:     PLA or TPU (TPU adds grip)")
print("")
print("  Usage:")
print("    1. Slide narrow end under mesh canopy")
print("    2. Push further to increase spread")
print("    3. Align notch with frame edge for repeatable fit")
print("")
print("=" * 50)
