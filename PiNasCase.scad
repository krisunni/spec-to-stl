//////////////////////////////
// KRYPTON NAS ENCLOSURE
// Premium Multi-Color 3D Printable Case
// Theme: DC Comics Krypton / Fortress of Solitude
//////////////////////////////
//
// TWO CREATIVE VERSIONS:
// ======================
// VERSION 1: "FORTRESS SPIRE" - Vertical tower with chimney cooling
//            + Removable magnetic side panel for easy component access
// VERSION 2: "CRYSTAL SHARD" - Angular wedge with convection channels
//
// Scroll to bottom to select which version to render
// Use fortress_spire_assembled() to preview with panel mounted
//
// MULTI-COLOR PRINTING GUIDE:
// ===========================
// Filament 1 (Main Body):    Ice Gray / Crystal White  -> color("ghostwhite")
// Filament 2 (Accents):      Deep Blue (Krypton Blue)  -> color("dodgerblue")
// Filament 3 (Text/Logos):   Superman Red              -> color("crimson")
// Filament 4 (Details):      Silver/Black              -> color("silver"), color("black")
//

//////////////////////////////
// GLOBAL PARAMETERS
//////////////////////////////

// Printer tolerances
tolerance = 0.25;
snap_clearance = 0.35;

// Wall & structure
wall = 2.8;
floor = 3.0;
fillet_res = 24;

// Screw parameters
screw_d = 2.6;
screw_head_d = 5.2;
post_d = 8;

// Fan (40mm)
fan_size = 40;
fan_screw_spacing = 32;
fan_screw_d = 3.2;

// ===== COMPONENT DIMENSIONS =====

// Raspberry Pi 5
pi_x = 85;
pi_y = 56;
pi_z = 1.6;
pi_standoff = 8;
pi_hole_x = 58;
pi_hole_y = 49;
pi_hole_offset = 3.5;

// AI HAT
ai_hat_z = 25;
ai_clearance = 30;

// UGREEN M.2 SSD: 125 x 41 x 14 mm
ssd_x = 125;
ssd_y = 41;
ssd_z = 14;

// UGREEN USB-C Ethernet: 62 x 25 x 15 mm
eth_x = 62;
eth_y = 25;
eth_z = 15;

// Text
text_depth = 2;
text_font = "Orbitron:style=Bold";

// Kryptonian styling
glyph_size = 8;
glyph_depth = 2;

//////////////////////////////
// UTILITY MODULES
//////////////////////////////

module screw_post(h) {
    difference() {
        cylinder(h=h, d=post_d, $fn=fillet_res);
        translate([0, 0, -0.1])
            cylinder(h=h+0.2, d=screw_d, $fn=fillet_res);
    }
}

module krypton_glyph(size=glyph_size, depth=glyph_depth) {
    linear_extrude(height=depth)
    polygon([[size/2,0], [size,size/2], [size/2,size], [0,size/2]]);
}

module hex_grid(width, height, hex_size=8, spacing=3, depth=10) {
    hex_h = hex_size * sin(60);
    cols = floor(width / (hex_size + spacing));
    rows = floor(height / (hex_h + spacing));

    for(row = [0:rows-1])
    for(col = [0:cols-1]) {
        offset_x = (row % 2) * (hex_size + spacing) / 2;
        translate([col * (hex_size + spacing) + offset_x + hex_size/2,
                   row * (hex_h + spacing) + hex_h/2, 0])
            cylinder(d=hex_size, h=depth, $fn=6);
    }
}

module crystal_vent_slot(length, width, depth) {
    linear_extrude(height=depth)
    polygon([
        [width*0.15, 0], [width*0.85, 0],
        [width, length*0.25], [width, length*0.75],
        [width*0.85, length], [width*0.15, length],
        [0, length*0.75], [0, length*0.25]
    ]);
}

module arrow_vent(length, width, depth) {
    linear_extrude(height=depth)
    polygon([
        [width/2, 0],
        [width, length*0.3],
        [width*0.7, length*0.3],
        [width*0.7, length],
        [width*0.3, length],
        [width*0.3, length*0.3],
        [0, length*0.3]
    ]);
}

//////////////////////////////
//
// VERSION 1: FORTRESS SPIRE
// Vertical tower design with natural chimney effect
// Cool air enters bottom, hot air exits top
//
// Component stack (bottom to top):
// - SSD (generates some heat, at bottom for intake)
// - Ethernet adapter (minimal heat)
// - Raspberry Pi 5 + AI HAT (main heat source, middle)
// - Fan exhaust at top (optional, passive works too)
//
//////////////////////////////

// Spire dimensions
spire_base_x = 140;
spire_base_y = 100;
spire_height = 160;
spire_taper = 0.85;  // Top is 85% of base size

// Side panel parameters (for easy access)
panel_inset = 2;
panel_lip = 4;
panel_magnet_d = 6;    // 6mm diameter magnets
panel_magnet_depth = 2;
panel_snap_size = 3;

module spire_shell() {
    // Tapered tower shape - wider at base, narrower at top
    hull() {
        // Base
        translate([wall, wall, 0])
            cube([spire_base_x - 2*wall, spire_base_y - 2*wall, 0.1]);

        // Top (tapered)
        top_x = spire_base_x * spire_taper;
        top_y = spire_base_y * spire_taper;
        offset_x = (spire_base_x - top_x) / 2;
        offset_y = (spire_base_y - top_y) / 2;
        translate([offset_x + wall, offset_y + wall, spire_height])
            cube([top_x - 2*wall, top_y - 2*wall, 0.1]);
    }
}

module spire_side_panel_cutout() {
    // Cutout for removable side access panel
    // Use linear_extrude of a 2D trapezoid for clean geometry

    panel_margin = 20;
    panel_bottom = 15;
    panel_top = 35;

    top_x = spire_base_x * spire_taper;
    offset_x = (spire_base_x - top_x) / 2;

    // Calculate corner positions
    bx1 = panel_margin;                          // bottom left x
    bx2 = spire_base_x - panel_margin;           // bottom right x
    tx1 = offset_x + panel_margin;               // top left x
    tx2 = spire_base_x - offset_x - panel_margin; // top right x
    bz = panel_bottom;                           // bottom z
    tz = spire_height - panel_top;               // top z

    // Extrude trapezoid shape through the wall (y direction)
    translate([0, -1, 0])
    rotate([-90, 0, 0])
    linear_extrude(height = wall * 3)
    polygon(points = [
        [bx1, bz],
        [bx2, bz],
        [tx2, tz],
        [tx1, tz]
    ]);
}

module spire_panel_magnet_holes() {
    // Magnet holes disabled - panel uses friction fit with snap lip
    // Magnets only in panel, attracted to steel plate or just friction
}

module spire_side_panel() {
    // Removable side panel - press fit with lip
    panel_margin = 20;
    panel_bottom = 15;
    panel_top = 35;
    top_x = spire_base_x * spire_taper;
    offset_x = (spire_base_x - top_x) / 2;

    // Panel sized to fit opening with small gap
    panel_w_bot = spire_base_x - 2*panel_margin - 0.5;
    panel_w_top = top_x - 2*panel_margin - 0.5;
    panel_h = spire_height - panel_top - panel_bottom - 0.5;
    panel_thick = wall;

    color("ghostwhite")
    difference() {
        union() {
            // Main panel (tapered trapezoid)
            hull() {
                cube([panel_w_bot, panel_thick, 2]);
                translate([(panel_w_bot - panel_w_top)/2, 0, panel_h - 2])
                    cube([panel_w_top, panel_thick, 2]);
            }

            // Inner lip for retention (sits inside opening)
            hull() {
                translate([3, panel_thick - 0.1, 3])
                    cube([panel_w_bot - 6, 3, 2]);
                translate([(panel_w_bot - panel_w_top)/2 + 3, panel_thick - 0.1, panel_h - 5])
                    cube([panel_w_top - 6, 3, 2]);
            }
        }

        // Ventilation slots
        for(i = [0:4]) {
            z_pos = 18 + i * 20;
            if(z_pos < panel_h - 12) {
                ratio = z_pos / panel_h;
                w_at_z = panel_w_bot - (panel_w_bot - panel_w_top) * ratio;
                x_off = (panel_w_bot - w_at_z) / 2;

                translate([x_off + 12, -0.1, z_pos])
                    cube([10, panel_thick + 4, 5]);
                translate([panel_w_bot - x_off - 22, -0.1, z_pos])
                    cube([10, panel_thick + 4, 5]);
            }
        }

        // Finger grip at top
        translate([panel_w_bot/2 - 12, -0.1, panel_h - 5])
            cube([24, panel_thick/2 + 0.1, 7]);
    }

    // Edge accent stripe
    color("dodgerblue")
    translate([6, -0.6, 6])
    hull() {
        cube([panel_w_bot - 12, 0.6, 2]);
        translate([(panel_w_bot - panel_w_top)/2, 0, panel_h - 12])
            cube([panel_w_top - 12, 0.6, 2]);
    }

    // DC-style rectangle frame around K
    color("dodgerblue")
    translate([panel_w_bot/2 - 20, -1, panel_h/2 - 22])
    rotate([90, 0, 0])
    linear_extrude(1)
    difference() {
        square([40, 44]);
        translate([2.5, 2.5]) square([35, 39]);
    }

    // Large "K" inside rectangle
    color("crimson")
    translate([panel_w_bot/2, -text_depth + 0.3, panel_h/2])
    rotate([90, 0, 0])
    linear_extrude(text_depth)
        text("K", size=28, font=text_font, halign="center", valign="center");

    // "ACCESS" below
    color("crimson")
    translate([panel_w_bot/2, -text_depth + 0.3, panel_h/2 - 32])
    rotate([90, 0, 0])
    linear_extrude(text_depth)
        text("ACCESS", size=5, font=text_font, halign="center");
}

module spire_interior() {
    // Hollow interior following taper
    hull() {
        translate([wall*2, wall*2, floor])
            cube([spire_base_x - 4*wall, spire_base_y - 4*wall, 0.1]);

        top_x = spire_base_x * spire_taper;
        top_y = spire_base_y * spire_taper;
        offset_x = (spire_base_x - top_x) / 2;
        offset_y = (spire_base_y - top_y) / 2;
        translate([offset_x + wall*2, offset_y + wall*2, spire_height - wall])
            cube([top_x - 4*wall, top_y - 4*wall, 0.1]);
    }
}

module spire_base_vents() {
    // Bottom intake vents - cool air enters here
    // No front vents - that's where access panel goes

    // Rear bottom vents
    translate([20, spire_base_y - wall - 0.5, 10])
    rotate([-90, 0, 0])
        hex_grid(spire_base_x - 40, 25, 6, 2, wall + 1);

    // Left side bottom vents
    translate([-0.5, 20, 10])
    rotate([0, 90, 0])
    rotate([0, 0, 90])
        hex_grid(spire_base_y - 40, 25, 6, 2, wall + 1);

    // Right side bottom vents
    translate([spire_base_x - wall - 0.5, 20, 10])
    rotate([0, 90, 0])
    rotate([0, 0, 90])
        hex_grid(spire_base_y - 40, 25, 6, 2, wall + 1);
}

module spire_exhaust_vents() {
    // Top exhaust - hot air exits here (chimney effect)

    top_x = spire_base_x * spire_taper;
    top_y = spire_base_y * spire_taper;
    offset_x = (spire_base_x - top_x) / 2;
    offset_y = (spire_base_y - top_y) / 2;

    // Large top opening for convection
    translate([spire_base_x/2, spire_base_y/2, spire_height - wall - 0.5])
        cylinder(d=fan_size + 10, h=wall + 1, $fn=fillet_res);

    // Rear exhaust vents near top (not front - that's the panel)
    for(i = [0:3]) {
        translate([offset_x + 15 + i*20, spire_base_y - offset_y - wall - 0.5, spire_height - 40])
        rotate([-90, 0, 0])
            crystal_vent_slot(25, 8, wall + 1);
    }
}

module spire_io_cutouts() {
    // Pi 5 port cutouts on LEFT wall (x=0)
    // Match Pi mount position
    pi_z_level = floor + ssd_z + 15 + eth_z + 15;
    pi_y_pos = (spire_base_y - pi_y - 10) / 2 + 5;  // Pi board Y + offset for mount
    port_z = pi_z_level + 3 + pi_standoff + 1;      // Mount base + standoff + clearance

    // === RASPBERRY PI 5 PORTS (Left wall, x=0) ===
    // Pi 5 port layout (from front to back of board):
    // USB-C power, HDMI0, HDMI1, Audio, (gap), USB2x2, Ethernet

    // USB-C Power port
    translate([-1, pi_y_pos + 5, port_z])
        cube([wall + 2, 11, 7]);

    // Micro HDMI 0
    translate([-1, pi_y_pos + 20, port_z])
        cube([wall + 2, 9, 5]);

    // Micro HDMI 1
    translate([-1, pi_y_pos + 32, port_z])
        cube([wall + 2, 9, 5]);

    // 3.5mm Audio jack
    translate([-1, pi_y_pos + 45, port_z + 2])
        rotate([0, 90, 0])
            cylinder(d=7, h=wall + 2, $fn=fillet_res);

    // 2x USB 3.0 ports (stacked)
    translate([-1, pi_y_pos + pi_y - 22, port_z - 1])
        cube([wall + 2, 15, 16]);

    // Gigabit Ethernet port
    translate([-1, pi_y_pos + pi_y - 5, port_z - 1])
        cube([wall + 2, 16, 14]);

    // === SSD USB cable exit (Right wall) ===
    translate([spire_base_x - wall - 1, wall*2 + 10, floor + 5])
        cube([wall + 2, 15, 10]);

    // === External Ethernet adapter cable (Right wall) ===
    translate([spire_base_x - wall - 1, spire_base_y - 45, floor + ssd_z + 18])
        cube([wall + 2, 15, 10]);

    // === Power cable entry (bottom rear) ===
    translate([20, spire_base_y - wall - 1, 2])
        cube([25, wall + 2, 6]);
}

module spire_main_case() {
    color("ghostwhite")
    difference() {
        spire_shell();
        spire_interior();
        spire_base_vents();
        spire_exhaust_vents();
        spire_io_cutouts();
        spire_side_panel_cutout();  // Removable access panel opening
    }
}

// Internal mounting shelves for spire
module spire_ssd_shelf() {
    // Bottom level - SSD mount
    color("dodgerblue")
    translate([wall*2, wall*2, floor])
    difference() {
        union() {
            cube([ssd_x + 10, ssd_y + 10, 3]);
            // Retention walls
            translate([0, 0, 3]) cube([5, ssd_y + 10, ssd_z]);
            translate([ssd_x + 5, 0, 3]) cube([5, ssd_y + 10, ssd_z]);
        }
        translate([5, 5, 3]) cube([ssd_x, ssd_y, ssd_z + 5]);
        // Vent holes in shelf
        for(i = [0:3])
            translate([20 + i*25, ssd_y/2 + 5, -0.1])
                cylinder(d=8, h=4, $fn=6);
    }
}

module spire_eth_shelf() {
    // Second level - Ethernet adapter
    color("dodgerblue")
    translate([spire_base_x - eth_x - wall*3 - 10, wall*2, floor + ssd_z + 15])
    difference() {
        union() {
            cube([eth_x + 10, eth_y + 10, 3]);
            translate([0, 0, 3]) cube([5, eth_y + 10, eth_z]);
            translate([eth_x + 5, 0, 3]) cube([5, eth_y + 10, eth_z]);
        }
        translate([5, 5, 3]) cube([eth_x, eth_y, eth_z + 5]);
    }
}

module spire_pi_mount() {
    // Third level - Pi + AI HAT (main heat source)
    // Pi positioned with port edge near left wall for I/O access
    pi_z_level = floor + ssd_z + 15 + eth_z + 15;

    // Position Pi so ports face left wall (x=0)
    // Pi ports overhang PCB by ~2mm, wall inner surface at x=wall
    pi_x_pos = wall + 2;  // Small gap for port clearance
    pi_y_pos = (spire_base_y - pi_y - 10) / 2;

    color("silver")
    translate([pi_x_pos, pi_y_pos, pi_z_level])
    union() {
        // Platform with airflow holes
        difference() {
            cube([pi_x + 10, pi_y + 10, 3]);
            for(x = [15, 45, 75])
            for(y = [15, 35, 55])
                translate([x, y, -0.1]) cylinder(d=8, h=4, $fn=6);
        }

        // Standoffs
        translate([pi_hole_offset + 5, pi_hole_offset + 5, 3]) screw_post(pi_standoff);
        translate([pi_hole_offset + pi_hole_x + 5, pi_hole_offset + 5, 3]) screw_post(pi_standoff);
        translate([pi_hole_offset + 5, pi_hole_offset + pi_hole_y + 5, 3]) screw_post(pi_standoff);
        translate([pi_hole_offset + pi_hole_x + 5, pi_hole_offset + pi_hole_y + 5, 3]) screw_post(pi_standoff);
    }
}

module spire_heat_baffles() {
    // Internal baffles to guide airflow upward
    color("silver")
    union() {
        // Angled baffle behind Pi directing heat up
        pi_z_level = floor + ssd_z + 15 + eth_z + 15;
        translate([wall*2, spire_base_y - wall*3, pi_z_level])
        rotate([15, 0, 0])
            cube([spire_base_x - wall*4, 2, 40]);
    }
}

module spire_accent_strips() {
    color("dodgerblue")
    union() {
        // Vertical edge accents following taper
        for(corner = [[wall, wall], [spire_base_x - wall - 4, wall],
                      [wall, spire_base_y - wall - 4], [spire_base_x - wall - 4, spire_base_y - wall - 4]]) {
            hull() {
                translate([corner[0], corner[1], 5])
                    cube([4, 4, 0.1]);

                top_x = spire_base_x * spire_taper;
                top_y = spire_base_y * spire_taper;
                offset_x = (spire_base_x - top_x) / 2;
                offset_y = (spire_base_y - top_y) / 2;

                new_x = corner[0] < spire_base_x/2 ? offset_x + wall : spire_base_x - offset_x - wall - 4;
                new_y = corner[1] < spire_base_y/2 ? offset_y + wall : spire_base_y - offset_y - wall - 4;

                translate([new_x, new_y, spire_height - 10])
                    cube([4, 4, 0.1]);
            }
        }
    }
}

module spire_text() {
    // Rear side text (opposite from access panel)
    color("crimson")
    translate([spire_base_x/2, spire_base_y + 0.5, spire_height/2])
    rotate([90, 0, 180])
    linear_extrude(text_depth)
        text("FORTRESS", size=10, font=text_font, halign="center");

    color("crimson")
    translate([spire_base_x/2, spire_base_y + 0.5, spire_height/2 - 16])
    rotate([90, 0, 180])
    linear_extrude(text_depth)
        text("SPIRE", size=8, font=text_font, halign="center");

    // Port labels on left side (near Pi ports)
    pi_z_level = floor + ssd_z + 15 + eth_z + 15;
    pi_y_pos = (spire_base_y - pi_y - 10) / 2 + 5;
    port_z = pi_z_level + 3 + pi_standoff + 1;

    color("silver") {
        // PWR label
        translate([-0.3, pi_y_pos + 8, port_z + 9])
        rotate([90, 0, -90])
        linear_extrude(0.8)
            text("PWR", size=3.5, font=text_font);

        // HDMI label
        translate([-0.3, pi_y_pos + 24, port_z + 7])
        rotate([90, 0, -90])
        linear_extrude(0.8)
            text("HDMI", size=3.5, font=text_font);

        // USB label
        translate([-0.3, pi_y_pos + pi_y - 20, port_z + 17])
        rotate([90, 0, -90])
        linear_extrude(0.8)
            text("USB", size=3.5, font=text_font);

        // ETH label
        translate([-0.3, pi_y_pos + pi_y - 2, port_z + 15])
        rotate([90, 0, -90])
        linear_extrude(0.8)
            text("ETH", size=3.5, font=text_font);
    }
}

module spire_glyphs() {
    color("silver")
    union() {
        // Vertical glyph column on front
        for(i = [0:5])
            translate([spire_base_x - 15, -glyph_depth + 0.5, 20 + i*22])
            rotate([90, 0, 0])
                krypton_glyph();

        // Vertical glyph column on back
        for(i = [0:5])
            translate([15, spire_base_y - 0.5, 20 + i*22])
            rotate([-90, 0, 0])
                krypton_glyph();
    }
}

module spire_lid() {
    top_x = spire_base_x * spire_taper;
    top_y = spire_base_y * spire_taper;

    color("ghostwhite")
    difference() {
        union() {
            // Peaked lid like crystal tip
            hull() {
                translate([5, 5, 0]) cube([top_x - 10, top_y - 10, 3]);
                translate([top_x/2 - 10, top_y/2 - 10, 25]) cube([20, 20, 0.1]);
            }

            // Inner lip
            translate([wall + tolerance, wall + tolerance, -8])
                cube([top_x - 2*wall - 2*tolerance, top_y - 2*wall - 2*tolerance, 8]);
        }

        // Central exhaust chimney
        translate([top_x/2, top_y/2, -9])
            cylinder(d=fan_size, h=30, $fn=fillet_res);

        // Additional exhaust holes
        for(a = [0:45:359])
            translate([top_x/2 + cos(a)*25, top_y/2 + sin(a)*25, -0.1])
                cylinder(d=10, h=10, $fn=6);
    }

    // Lid accents
    color("dodgerblue")
    difference() {
        hull() {
            translate([10, 10, 3]) cube([top_x - 20, top_y - 20, 0.1]);
            translate([top_x/2 - 8, top_y/2 - 8, 20]) cube([16, 16, 0.1]);
        }
        hull() {
            translate([15, 15, 2.9]) cube([top_x - 30, top_y - 30, 0.1]);
            translate([top_x/2 - 5, top_y/2 - 5, 21]) cube([10, 10, 0.1]);
        }
        translate([top_x/2, top_y/2, -1])
            cylinder(d=fan_size + 5, h=30, $fn=fillet_res);
    }

    // Lid text - flat on the sloped surface
    color("crimson")
    translate([top_x/2, 15, 2])
    linear_extrude(text_depth)
        text("KRYPTON", size=8, font=text_font, halign="center");
}

// Complete Spire Assembly
module fortress_spire() {
    spire_main_case();
    spire_ssd_shelf();
    spire_eth_shelf();
    spire_pi_mount();
    // spire_heat_baffles();  // Optional
    spire_accent_strips();
    spire_text();
    spire_glyphs();

    // Lid positioned beside for printing
    translate([spire_base_x + 20, 0, 0])
        spire_lid();

    // Side access panel positioned beside for printing
    // (magnetically attaches to front of case)
    translate([spire_base_x + 20, spire_base_y + 20, 0])
        spire_side_panel();
}

// Preview: Show panel in mounted position
module fortress_spire_assembled() {
    spire_main_case();
    spire_ssd_shelf();
    spire_eth_shelf();
    spire_pi_mount();
    spire_accent_strips();
    spire_text();
    spire_glyphs();

    // Lid in mounted position
    top_x = spire_base_x * spire_taper;
    top_y = spire_base_y * spire_taper;
    offset_x = (spire_base_x - top_x) / 2;
    offset_y = (spire_base_y - top_y) / 2;
    translate([offset_x, offset_y, spire_height - 8])
        spire_lid();

    // Side panel in mounted position (front face)
    translate([20 + 0.5, 0.5, 15 + 0.5])
        spire_side_panel();
}


//////////////////////////////
//
// VERSION 2: CRYSTAL SHARD
// Angular wedge design with convection-driven cooling
// Dramatic crystalline aesthetic with functional thermals
//
// The angled surfaces naturally promote convection:
// - Hot air rises along the sloped ceiling
// - Cool air drawn in through lower vents
// - Components arranged along thermal gradient
//
//////////////////////////////

// Shard dimensions
shard_length = 200;
shard_width = 100;
shard_height_front = 45;   // Low front
shard_height_rear = 95;    // Tall rear (hot air exits here)
shard_angle = atan((shard_height_rear - shard_height_front) / shard_length);

module shard_profile() {
    // 2D profile of the shard cross-section
    polygon([
        [0, 0],
        [shard_length, 0],
        [shard_length, shard_height_rear],
        [shard_length * 0.7, shard_height_rear + 15],  // Crystal peak
        [0, shard_height_front]
    ]);
}

module shard_shell() {
    // Main angular body
    linear_extrude(height=shard_width)
    offset(r=2)
    offset(r=-2)
        shard_profile();
}

module shard_interior() {
    translate([wall, 0, wall])
    linear_extrude(height=shard_width - 2*wall)
    offset(r=-wall)
        shard_profile();
}

module shard_front_vents() {
    // Cool air intake at low front
    for(i = [0:4]) {
        translate([15 + i*20, shard_height_front - 15, -0.5])
        rotate([-90, 0, 0])
        rotate([0, 0, -shard_angle])
            crystal_vent_slot(12, 8, wall + 1);
    }

    // Bottom front intake
    for(i = [0:5]) {
        translate([10 + i*18, -0.5, 15 + i*3])
            cube([8, wall + 1, 15]);
    }
}

module shard_rear_vents() {
    // Hot air exhaust at tall rear (chimney exit)
    // Large vent area for maximum exhaust

    // Top rear crystal vents
    for(i = [0:4]) {
        translate([shard_length - 15, shard_height_rear - 10 - i*15, wall + 10 + i*8])
        rotate([0, -90, 0])
            crystal_vent_slot(20, 10, wall + 1);
    }

    // Peak exhaust
    translate([shard_length * 0.7 - 15, shard_height_rear + 5, shard_width/2 - 20])
    rotate([0, 35, 0])
        cube([30, 15, 40]);
}

module shard_side_vents() {
    // Side ventilation following the angle

    // Left side (z=0)
    for(i = [0:6]) {
        z_pos = 5;
        x_pos = 20 + i*25;
        y_pos = shard_height_front + (x_pos / shard_length) * (shard_height_rear - shard_height_front) - 25;

        translate([x_pos, y_pos, -0.5])
        rotate([-shard_angle, 0, 0])
            arrow_vent(18, 10, wall + 1);
    }

    // Right side (z=shard_width)
    for(i = [0:6]) {
        x_pos = 20 + i*25;
        y_pos = shard_height_front + (x_pos / shard_length) * (shard_height_rear - shard_height_front) - 25;

        translate([x_pos, y_pos, shard_width - wall - 0.5])
        rotate([-shard_angle, 0, 0])
            arrow_vent(18, 10, wall + 1);
    }
}

module shard_io_cutouts() {
    // Pi I/O on left side
    translate([20, floor + pi_standoff + 3, -0.5])
        cube([50, 22, wall + 1]);

    // SSD USB on right rear
    translate([shard_length - 30, floor + 5, shard_width - wall - 0.5])
        cube([25, 15, wall + 1]);

    // Ethernet on right side
    translate([shard_length - eth_x - 30, floor + ssd_z + 20, shard_width - wall - 0.5])
        cube([20, 15, wall + 1]);
}

module shard_main_case() {
    color("ghostwhite")
    rotate([90, 0, 0])
    translate([0, 0, -shard_width])
    difference() {
        shard_shell();
        shard_interior();
        shard_front_vents();
        shard_rear_vents();
        shard_side_vents();
        shard_io_cutouts();
    }
}

module shard_pi_mount() {
    // Pi mounted in the lower front section (cooler zone)
    color("silver")
    translate([15, wall + 5, floor])
    union() {
        difference() {
            cube([pi_x + 10, pi_y + 10, 3]);
            for(x = [20, 50, 80])
            for(y = [15, 35, 55])
                translate([x, y, -0.1]) cylinder(d=6, h=4, $fn=6);
        }

        translate([pi_hole_offset + 5, pi_hole_offset + 5, 3]) screw_post(pi_standoff);
        translate([pi_hole_offset + pi_hole_x + 5, pi_hole_offset + 5, 3]) screw_post(pi_standoff);
        translate([pi_hole_offset + 5, pi_hole_offset + pi_hole_y + 5, 3]) screw_post(pi_standoff);
        translate([pi_hole_offset + pi_hole_x + 5, pi_hole_offset + pi_hole_y + 5, 3]) screw_post(pi_standoff);
    }
}

module shard_ssd_mount() {
    // SSD in rear tall section (heat rises away)
    color("dodgerblue")
    translate([shard_length - ssd_x - 20, shard_width - ssd_y - wall - 10, floor])
    difference() {
        union() {
            cube([ssd_x + 8, ssd_y + 8, 4]);
            translate([0, 0, 4]) cube([4, ssd_y + 8, ssd_z]);
            translate([ssd_x + 4, 0, 4]) cube([4, ssd_y + 8, ssd_z]);
        }
        translate([4, 4, 4]) cube([ssd_x, ssd_y, ssd_z + 5]);
        for(i = [0:3])
            translate([15 + i*28, ssd_y/2 + 4, -0.1]) cylinder(d=8, h=5, $fn=6);
    }
}

module shard_eth_mount() {
    // Ethernet beside SSD
    color("dodgerblue")
    translate([shard_length - ssd_x - eth_x - 35, shard_width - eth_y - wall - 10, floor])
    difference() {
        union() {
            cube([eth_x + 8, eth_y + 8, 4]);
            translate([0, 0, 4]) cube([4, eth_y + 8, eth_z]);
            translate([eth_x + 4, 0, 4]) cube([4, eth_y + 8, eth_z]);
        }
        translate([4, 4, 4]) cube([eth_x, eth_y, eth_z + 5]);
    }
}

module shard_thermal_ramp() {
    // Internal ramp to guide hot air toward rear exhaust
    color("silver", 0.5)
    translate([pi_x + 30, wall, floor + pi_standoff + 25])
    rotate([0, shard_angle + 5, 0])
        cube([80, shard_width - 2*wall, 2]);
}

module shard_accent_edges() {
    color("dodgerblue")
    union() {
        // Angular accent along top edge
        translate([0, 0, 0])
        rotate([90, 0, 0])
        translate([0, 0, -shard_width])
        linear_extrude(height=shard_width)
        polygon([
            [5, shard_height_front - 3],
            [shard_length - 5, shard_height_rear - 3],
            [shard_length * 0.7 - 5, shard_height_rear + 12],
            [shard_length * 0.7 - 8, shard_height_rear + 10],
            [shard_length - 8, shard_height_rear - 5],
            [8, shard_height_front - 5]
        ]);

        // Bottom edge accent
        translate([5, -wall - 0.5, 3])
            cube([shard_length - 10, 2, 4]);
    }
}

module shard_text() {
    color("crimson")
    union() {
        // Angled text following roof line
        translate([shard_length/2, shard_width + 0.5, shard_height_front + (shard_height_rear - shard_height_front)/2])
        rotate([90, -shard_angle, 0])
        linear_extrude(text_depth)
            text("CRYSTAL SHARD", size=10, font=text_font, halign="center");

        // Side text
        translate([shard_length/3, -0.5, shard_width/2])
        rotate([90, 0, 0])
        rotate([0, 0, 90])
        linear_extrude(text_depth)
            text("KRYPTON NAS", size=12, font=text_font, halign="center");

        // Rear text
        translate([shard_length + 0.5, (shard_height_rear + shard_height_front)/2, shard_width/2])
        rotate([0, -90, 0])
        rotate([0, 0, 90])
        linear_extrude(text_depth)
            text("K", size=25, font=text_font, halign="center");
    }
}

module shard_glyphs() {
    color("silver")
    union() {
        // Glyphs along angled top surface
        for(i = [0:7]) {
            x_pos = 25 + i*20;
            y_pos = shard_height_front + (x_pos / shard_length) * (shard_height_rear - shard_height_front) - 2;

            translate([x_pos, shard_width + 0.5, y_pos])
            rotate([90, 0, 0])
                krypton_glyph(6, glyph_depth);
        }

        // Side glyphs
        for(i = [0:4]) {
            translate([shard_length - 20, -glyph_depth + 0.5, 15 + i*18])
            rotate([90, 0, 0])
                krypton_glyph();
        }
    }
}

module shard_lid() {
    // Angled lid matching the profile
    lid_length = shard_length - 10;
    lid_width = shard_width - wall*2 - tolerance*2;

    color("ghostwhite")
    translate([0, 0, 0])
    rotate([90, 0, 0])
    difference() {
        linear_extrude(height=lid_width) {
            polygon([
                [5, shard_height_front - 5],
                [lid_length, shard_height_rear - 8],
                [shard_length * 0.7 - 5, shard_height_rear + 10],
                [5, shard_height_front + 5]
            ]);
        }

        // Inner cutout for lip
        translate([0, 0, 3])
        linear_extrude(height=lid_width - 6) {
            offset(r=-3)
            polygon([
                [5, shard_height_front - 5],
                [lid_length, shard_height_rear - 8],
                [shard_length * 0.7 - 5, shard_height_rear + 10],
                [5, shard_height_front + 5]
            ]);
        }

        // Exhaust vents in lid
        for(i = [0:5]) {
            x_pos = 30 + i*25;
            y_pos = shard_height_front + (x_pos / shard_length) * (shard_height_rear - shard_height_front);
            translate([x_pos, y_pos - 3, -0.5])
                cylinder(d=12, h=lid_width + 1, $fn=6);
        }
    }

    // Lid accent
    color("dodgerblue")
    translate([0, lid_width + 2, 0])
    rotate([90, 0, 0])
    linear_extrude(height=2) {
        difference() {
            polygon([
                [10, shard_height_front - 2],
                [lid_length - 5, shard_height_rear - 5],
                [shard_length * 0.7 - 8, shard_height_rear + 7],
                [10, shard_height_front + 2]
            ]);
            offset(r=-5)
            polygon([
                [10, shard_height_front - 2],
                [lid_length - 5, shard_height_rear - 5],
                [shard_length * 0.7 - 8, shard_height_rear + 7],
                [10, shard_height_front + 2]
            ]);
        }
    }

    // Lid text
    color("crimson")
    translate([shard_length/2, lid_width/2, shard_height_front + 20])
    rotate([0, -shard_angle - 5, 0])
    linear_extrude(text_depth)
        text("KRYPTON", size=14, font=text_font, halign="center");
}

// Complete Shard Assembly
module crystal_shard() {
    shard_main_case();
    shard_pi_mount();
    shard_ssd_mount();
    shard_eth_mount();
    // shard_thermal_ramp();  // Optional internal baffle
    shard_accent_edges();
    shard_text();
    shard_glyphs();

    // Lid positioned beside for printing
    translate([shard_length + 30, 0, 0])
        shard_lid();
}


//////////////////////////////
// RENDER SELECTION
//////////////////////////////
//
// Uncomment ONE of the following to render:
//

// VERSION 1: Fortress Spire (vertical tower) - parts laid out for printing
fortress_spire();

// VERSION 1 ASSEMBLED: Preview with panel and lid mounted
// fortress_spire_assembled();

// VERSION 2: Crystal Shard (angular wedge)
// crystal_shard();


//////////////////////////////
// THERMAL DESIGN NOTES
//////////////////////////////
//
// FORTRESS SPIRE:
// - Chimney effect: cool air enters base vents, hot air exits top
// - Components stacked by heat output (coolest at bottom)
// - Tapered shape accelerates rising air
// - Pi + AI HAT in middle where airflow is strongest
// - Peaked lid creates low-pressure zone for exhaust
// - REMOVABLE SIDE PANEL: Magnetic attachment with 6x 6mm magnets
//   - Full-height access to all components without unstacking
//   - Crystal vents in panel maintain airflow when closed
//   - Finger notch at top for easy removal
//
// CRYSTAL SHARD:
// - Convection slope: angled ceiling guides hot air to rear
// - Low front = intake zone (cool)
// - Tall rear = exhaust zone (hot air naturally rises here)
// - Arrow vents on sides indicate airflow direction
// - Thermal gradient from front to back
//
// Both designs work WITHOUT a fan for quiet operation.
// Add 40mm fan at exhaust point for active cooling if needed.
//

//////////////////////////////
// PRINT SETTINGS
//////////////////////////////
//
// Layer height: 0.2mm
// Infill: 15-20%
// Supports: Required for overhangs
//
// SPIRE: Print upright, supports for shelves
// SHARD: Print on side (flat bottom edge down)
//
