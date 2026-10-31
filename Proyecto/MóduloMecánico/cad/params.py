"""LanternGuard mechanical module: every dimension lives here (mm, g, MPa).

Source tags in comments:
  [doc]  taken from team documents (file noted)
  [ds]   component datasheet value (confidence noted)
  [sup]  SUPUESTO: our assumption, with the reason
Change a value here and re-run build.py; nothing else hardcodes dimensions.
"""

# ---------------------------------------------------------------- global
PRINT_BED = (220.0, 220.0, 250.0)   # [sup] common FDM bed (Ender-3 / Prusa class)
MIN_WALL = 1.2                      # [sup] 3 perimeters x 0.4 mm nozzle
CLEARANCE = 1.0                     # [sup] min gap component <-> wall
PETG_DENSITY = 1.27                 # g/cm3 [doc] 03_INVENTARIO_CAD.md (rho 1270 kg/m3)
PETG_YIELD = 45.0                   # MPa   [doc] tentative value used in T01
SEAWATER_DENSITY = 1.025            # g/cm3 [sup] standard seawater at 35 g/L
DESIGN_DEPTH_M = 15.0               # m     [doc] rev.3 list, row "Uso"
DESIGN_PRESSURE = 0.15              # MPa   ~ rho g h = 1025*9.81*15 = 0.151 MPa

# --------------------------------------------------- electronics (envelopes, L x W x H)
COMPONENTS = {
    # name: (L, W, H, mass_g, source)
    "esp32_devkit_wroom32u": (52.0, 28.0, 13.0, 10.0, "[ds] 30-pin DevKit, clones vary +-3 mm (media)"),
    "microsd_module":        (42.0, 24.0, 12.0, 4.0, "[ds] SPI microSD breakout (media)"),
    "max485_module":         (44.0, 14.0, 12.0, 3.0, "[ds] MAX485 TTL breakout (media)"),
    "jsn_sr04t_board":       (41.0, 28.5, 10.0, 6.0, "[ds] JSN-SR04T v2/v3 driver board (media)"),
    "arducam_mega_5mp":      (33.0, 33.0, 25.0, 20.0, "[ds] Arducam Mega 5MP SPI, board 33x33, lens height 20-25 (media/baja)"),
}
JSN_PROBE_DIA = 23.5      # [ds] transducer housing diameter (media); 03_INVENTARIO assumed 22
JSN_PROBE_LEN = 20.0      # [ds] housing length above the mounting face (baja)
CABLE_MASS_G = 40.0       # [sup] wiring + glands inside the sealed volumes

# --------------------------------------------------- seals and fasteners
ORING_CORD = 2.0          # [doc] O-ring 22 x 2 (CONTEXTO_SESION_CHAT §4): 2 mm cross-section
GROOVE_DEPTH = 1.5        # 25 % squeeze on a 2.0 mm cord (face seal, static)
GROOVE_WIDTH = 2.6        # ~1.3 x cord, room for 25 % squeeze spread
M3_CLEAR = 3.4
M4_CLEAR = 4.2            # [doc] hinge hole 4.2 for M4 (CONTEXTO_SESION_CHAT §4)
M3_INSERT_HOLE = 4.0      # [sup] M3 heat-set insert, 5.7 mm long
M3_INSERT_DEPTH = 6.0
M2_PILOT = 1.8            # self-tapping M2 for the window bezel
PG7_HOLE = 12.6           # [doc] PG7 thread 12.5 mm; nut inside
PG7_NUT_AF = 15.0         # [ds] PG7 locknut across flats (baja) -> needs ~19 mm flat inside
PG9_HOLE = 15.4           # [ds] PG9 thread 15.2 mm (media)
PG9_NUT_AF = 20.0         # [ds] PG9 locknut across flats (media)
NUT_T = 5.0               # [ds] gland locknut thickness (media)
CAP_GLAND_X = 10.0        # PG7 centre from the capsule rear opening (bottom wall)
LID_GLAND_Y = 18.0        # PG9 offset from the handle on the box lid

# --------------------------------------------------- camera capsule: P4 rev. B
# Original P4 (T01): 52 x 40 x 28 outer, cavity 46 x 34 x 22 -> cannot hold a 33x33 board
# plus a 20-25 mm lens. Rev. B keeps the window, ears and hinge, and enlarges the cavity.
CAP_CAV_W = 38.0          # board 33 + 2.5 per side
CAP_CAV_H = 38.0
CAP_CAV_L = 50.0          # lens 25 + board 2 + cable bend + PG7 locknut zone behind the board
CAP_WALL = 4.0            # side walls
CAP_FRONT = 6.0           # doc proposed 5 (03_INVENTARIO_CAD §5); 6 leaves a 2.8 mm window shoulder
CAP_FLANGE = 9.0          # flange width around the rear opening
CAP_FLANGE_T = 6.0
CAP_LID_T = 5.0
WIN_DIA = 30.0            # [sup] flat acrylic disc; doc had 25.4 -> 30 gives FOV margin for wide lens
WIN_T = 3.0               # [doc] acrylic 3 mm
WIN_SEAT_DEPTH = 3.2      # recess from the outside; water pressure pushes the disc onto the shoulder
LENS_APERTURE = 22.0      # clear aperture behind the window
BEZEL_OD = 42.0
BEZEL_T = 2.5
BEZEL_SCREWS = 3          # M2 self-tapping into the front wall

# --------------------------------------------------- toothed hinge
# [doc] CONTEXTO_SESION_CHAT §4: disc 24 mm, 36 teeth (10 deg), tooth 1.2 mm,
# fork of two 5 mm ears with an 8.4 mm gap, range 0-90 deg, axis outside the seal.
HINGE_DISC_D = 24.0
HINGE_TEETH = 36
HINGE_TOOTH_H = 1.2
HINGE_TEETH_RIN = 7.0       # teeth ring 7-12 mm; M4 hole 4.2 stays clear
HINGE_EAR_T = 5.0
HINGE_GAP = 8.4
TONGUE_CORE = HINGE_GAP - 2 * HINGE_TOOTH_H   # 6.0 mm, teeth on both faces mesh into the fork
TONGUE_LEN = 16.0         # hinge axis to lid outer face (tongue sits on the lid, outside the seal)
CAM_TILT_DEG = 40.0       # [sup] working tilt "inclinadas hacia abajo"; must be a multiple of 10 (tooth pitch)

# --------------------------------------------------- central electronics box
BOX_CAV_L = 132.0         # devkit 52 + probe 26 + MAX485 44 + gaps (layout in parts.py)
BOX_CAV_W = 66.0          # devkit row 28 + JSN board row 28.5 + gaps
BOX_CAV_H = 54.0          # boards 18 + PG7 locknut above them + room under the lid
BOX_WALL = 5.0            # Roark check: side wall 132 x 54 at 0.15 MPa
BOX_FLOOR = 6.0
BOX_FLANGE = 9.0
BOX_FLANGE_T = 6.0
BOX_LID_T = 6.0           # Roark check in checks.py (5 mm deflects ~1.5 mm)
ARM_PAD = 34.0            # square pad on each end wall for the arm (solid, outside the seal)
GLAND_Z = 28.0            # PG7 centre height above the cavity floor: locknut clears the boards
ARM_PAD_T = 10.0
HANDLE_H = 42.0           # [doc] rev.3 Ergonomia: asa + punto de anclaje, usable with gloves
HANDLE_GRIP = 90.0        # glove width ~ 90 mm [sup]

# --------------------------------------------------- arms (hollow, flooded cable conduits)
ARM_W = 30.0              # [doc] 03_INVENTARIO_CAD §5: arms 30 x 25
ARM_H = 25.0
ARM_WALL = 3.0
ARM_LEN = 190.0           # standing print height 190 + 52 fork = 242 <= 250 bed; saddles land on a 500 mm ring
ARM_FLANGE_T = 5.0
FORK_REACH = 52.0         # tube end -> rounded ear tip         # ears beyond the tube end; sized so the capsule clears the arm at 0-90 deg
RING_ROD_D = 12.0         # [sup] lantern top ring rod diameter (not in docs)
LANTERN_RING_D = 500.0    # [doc] lantern outer diameter 0.5 m (ref [1], rev.3 Geometria); ring rod assumed
STRAP_SLOT = (26.0, 4.0)  # velcro / hose-clamp strap, gloved install <= 5 min

# --------------------------------------------------- lab test mesh frame
FRAME_OUT = 200.0
FRAME_BAR = 14.0
FRAME_T = 6.0
MESH_OPENING = 20.0       # [doc] lantern mesh opening 15-32 mm (03_INVENTARIO / FONDEPES)
MESH_BAR = 2.0
MESH_T = 2.0
TEST_DISTANCE = 150.0     # [sup] camera window to mesh plane in the lab tank
