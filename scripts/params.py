"""Shared parameters for the modular box camera.

Units: millimetres. All values are nominal.

Coordinate system
-----------------
  x : left/right (width), centred on the optical axis
  y : down/up (height), y = -45 bottom, y = +45 top
  z : optical axis, z = 0 at the outer face of the front plate
      (the mounting face the lens ring sits against)

So a "distance behind the lens face" is just a z value.
"""

# ---- outer envelope -------------------------------------------------------
OUT_W = 90.0          # outer width  (x)
OUT_H = 90.0          # outer height (y), lid fitted
WALL = 4.0            # solid wall thickness

INNER_W = OUT_W - 2 * WALL          # 82
INNER_H = OUT_H - 2 * WALL          # 82 (usable cavity, lid occupies top 4)

# ---- front plate ----------------------------------------------------------
PLATE_T = 5.0         # flange thickness (z = 0 .. 5)
PLATE_SPIGOT = 8.0    # spigot length that presses into the tube
FIT = 0.15            # slip-fit clearance per side
BORE_D = 59.05        # through hole for the lens ring
APERTURE_RECESS_D = 64.0   # optional stop disc, dropped in behind the glass
APERTURE_RECESS_DEPTH = 0.8

# ---- tube (front body) ----------------------------------------------------
TUBE_LEN = 105.0      # z = PLATE_T .. PLATE_T + TUBE_LEN  -> 110 total
FRONT_TOTAL = PLATE_T + TUBE_LEN            # 110

# ---- top lid seat (flush drop-in lid, Phase 2) ---------------------------
LID_T = 4.0
LID_REBATE_W = 2.5    # step cut into the outside of the top rim
LID_LEDGE_Y = OUT_H / 2 - LID_T             # 41 : lid underside rests here

# ---- focus slots (screen frame lives in one pair) ------------------------
SLOT_PITCH = 4.0
SLOT_W = 2.5          # -> web = 1.5 mm
SLOT_DEPTH = 2.0      # rebate must stay wider than this so the frame drops in
SLOT_FIRST_Z = 25.0   # first slot centre behind the lens face
# The screen frame must stay in front of the rear body's spigot (front face at
# z = 98): slot 97 puts the frame's rear face at 98.15 and clashes by 0.15 mm,
# so the usable series stops at 93.
SLOT_COUNT = 18       # 25 .. 93
SLOT_LAST_Z = SLOT_FIRST_Z + (SLOT_COUNT - 1) * SLOT_PITCH     # 93
SLOT_TOP_Y = LID_LEDGE_Y                     # slots stop under the lid ledge

# ---- rear body (Phase 1B) -------------------------------------------------
REAR_LEN = 110.0      # z = 110 .. 220
REAR_FACE_Z = PLATE_T + TUBE_LEN + REAR_LEN        # 220 : rear wall outer face
REAR_WALL_T = 8.0     # solid rear wall, carries the camera aperture
REAR_SPIGOT = 12.0    # laps into the front tube
REAR_SPIGOT_WALL = 2.0
REAR_SPIGOT_FACE_Z = PLATE_T + TUBE_LEN - REAR_SPIGOT          # 98 : spigot front face

# camera aperture + foam light seal on the rear wall's outer face
CAM_APERTURE_D = 22.0
CAM_CHAMFER_D = 26.0        # flare on the inner face, acts as a light baffle
FOAM_RING_OD = 34.0         # closed-cell foam ring, pressed by the phone
FOAM_RING_ID = 24.0
FOAM_RECESS_D = 0.6         # shallow locating step for the foam ring

# ---- carrier fixing points (blind holes in the rear wall) -----------------
# x, y positions in the rear wall's outer face; all sit inside the free
# top/left strips, clear of the foam ring.
CARRIER_HOLES = [(-38.4, -30.0), (-38.4, 6.0), (8.0, 25.5), (38.0, 25.5)]
PILOT_DEPTH = 6.0           # rear wall is 8 mm, so 2 mm stays light-tight

# ---- phone (Samsung S24 Ultra, measured in its case) ---------------------
CASE_L = 165.0        # long edge (ruler)
CASE_W = 82.5         # short edge, case body only (calipers)
CASE_W_BTN = 82.9     # including the volume buttons
CASE_T = 11.5         # typical thickness
CASE_T_CAM = 12.47    # over the camera bump
CASE_T_KICK = 12.99   # over the kickstand near the base
BTN_PROUD = CASE_W_BTN - CASE_W            # 0.4

LENS_FROM_SIDE = 17.6     # lens centre -> case side under the buttons
LENS_FROM_TOP = 34.33     # lens centre -> case end opposite the charger

# Landscape, buttons up, lens on the optical axis (x = y = 0):
PHONE_X0 = -LENS_FROM_TOP                  # -34.33
PHONE_X1 = PHONE_X0 + CASE_L               # +130.67
PHONE_Y1 = LENS_FROM_SIDE                  # +17.6  (case side, under buttons)
PHONE_Y0 = PHONE_Y1 - CASE_W               # -64.90
BUTTON_Y = PHONE_Y1 + BTN_PROUD            # +18.0  (button tips)

# ---- lids (Phase 2) ------------------------------------------------------
LID_CLR = 0.15                     # side clearance inside the 87 mm rebate
LID_XH = INNER_W / 2 + LID_REBATE_W - LID_CLR      # 43.35 -> 86.7 wide
LID_Y0 = LID_LEDGE_Y + 0.05        # 41.05 : underside, rests on the ledge
LID_Y1 = OUT_H / 2 - 0.05          # 44.95 : top surface, just below flush
LID_SPLIT_Y = (LID_Y0 + LID_Y1) / 2.0              # 43.00 : lap plane
LID_LAP = 10.0                     # mutual overlap either side of the seam
LID_SEAM_Z = FRONT_TOTAL           # 110
LID_CHAMFER = 0.8                  # fingernail V-groove along the top edges

# front plate cap/skirt: keeps the plate from falling off and helps retain the lid
PLATE_SKIRT_H = 8.0            # goes back along the outside of the tube (prints with flange on bed)
PLATE_SKIRT_T = 1.2            # wall thickness of the cap
PLATE_SKIRT_CLR = 0.15         # 0.15 per side -> OUT_W + 0.3 ID, friction fit
PLATE_SKIRT_LEAD = 0.5         # chamfer on the skirt's rear edge

# ridge on the underside, drops into the cavity as a light baffle
LID_FLANGE_W = 2.0
LID_FLANGE_T = 1.5
LID_FLANGE_CLR = 0.2
LID_FLANGE_X0 = INNER_W / 2 - LID_FLANGE_CLR - LID_FLANGE_W    # 38.8
LID_FLANGE_X1 = INNER_W / 2 - LID_FLANGE_CLR                   # 40.8
LID_FRONT_FLANGE_Z = (PLATE_T + PLATE_SPIGOT + 0.5, 97.0)      # clears both spigots
LID_REAR_FLANGE_Z = (115.0, REAR_FACE_Z - REAR_WALL_T - 1.0)   # 115 .. 211

# ---- focusing screen frame (Phase 3) -------------------------------------
# Slides down into one pair of focus slots, so only its outer 1.75 mm is thin
# enough for the 2.5 mm slot; the sheet sits in a pocket, which lets the two
# halves close on each other and keeps the rim light-tight.
FRAME_W = 2 * (INNER_W / 2 + SLOT_DEPTH) - 0.5      # 85.5 : 1.75 mm into each slot
FRAME_Y0 = -OUT_H / 2 + WALL + 0.1                  # -40.9 : rests on the cavity floor
FRAME_Y1 = LID_LEDGE_Y - 3.0                        # +38.0 : clear of the lid ridge
FRAME_HALF_T = 1.15                                 # 2.30 total -> 0.20 in the slot
FRAME_APERTURE = 60.0                               # square window, centred on the axis
FRAME_POCKET_W = 76.0
FRAME_POCKET_H = 66.0
FRAME_POCKET_D = 0.45                               # sheet up to 0.5 mm thick
FRAME_PIN_D = 2.5
FRAME_PIN_H = 1.1
FRAME_SOCKET_D = 2.45                               # light press fit
FRAME_PINS = [(-30.0, 34.5), (30.0, 34.5), (-30.0, -37.0), (30.0, -37.0)]
FRAME_TEST_SLOT = SLOT_FIRST_Z + 6 * SLOT_PITCH     # 49 : middle slot, for checks

# ---- carrier -------------------------------------------------------------
CARRIER_DEPTH = 16.0
CARRIER_Z0 = REAR_FACE_Z
CARRIER_Z1 = CARRIER_Z0 + CARRIER_DEPTH            # 236
RAIL = 8.0                # rail width around the opening
CARRIER_CLR = 0.2         # clearance phone <-> stops

OPEN_X0 = PHONE_X0 - CARRIER_CLR           # -34.53 : fixed x stop
OPEN_Y0 = PHONE_Y0 - CARRIER_CLR           # -65.10 : bottom fence (phone rests)
OPEN_Y1 = BUTTON_Y + 3.0                   # +21.0  : clear of the buttons
JAW_X0 = PHONE_X1 + CARRIER_CLR            # +130.87 : sliding jaw front face
JAW_T = 3.0
JAW_TRAVEL = 3.0                           # retraction needed to clear the lip
OPEN_X1 = JAW_X0 + JAW_T + JAW_TRAVEL      # +136.87 : right rail inner face

CARRIER_X0 = OPEN_X0 - RAIL                # -42.53
CARRIER_X1 = OPEN_X1 + 12.0                # +148.87 : right rail is 12 mm wide
CARRIER_Y0 = OPEN_Y0 - RAIL                # -73.10
CARRIER_Y1 = OPEN_Y1 + RAIL                # +29.00

# depth of the phone: set by the retainer lips, foam compressed by that gap
FOAM_T = 3.0              # closed-cell foam, sits in the 0.6 mm recess
FOAM_GAP = 1.7            # compressed thickness = phone back off the wall face
PHONE_BACK_Z = CARRIER_Z0 + FOAM_GAP       # 221.70
PHONE_FRONT_Z = PHONE_BACK_Z + CASE_T      # 233.20
LIP_T = 2.0
LIP_W = 2.2               # how far the lip reaches over the phone's face
LIP_Z0 = PHONE_FRONT_Z + 0.2               # 233.40
LIP_Z1 = LIP_Z0 + LIP_T                    # 235.40
JAW_Z0 = 221.5
JAW_Z1 = LIP_Z0                            # jaw never stands proud of the lips

# M5 pusher in the right rail
PUSHER_Y = (PHONE_Y0 + PHONE_Y1) / 2.0     # -23.65
PUSHER_Z = 228.0
PUSHER_BORE = 5.5
NUT_AF = 8.4              # M5 hex nut pocket, 8 mm across flats + clearance
NUT_H = 4.8
NUT_FROM_Z = CARRIER_X1   # pocket opens on the outer face

# fixing screws (M3 countersunk into the carrier, thread-forming in the wall)
CARRIER_SCREW_BORE = 3.2
CARRIER_CSK_D = 6.2

# band-retention provision: buttonhole at the left end of the top/bottom rails
BAND_HOLE_X = -38.0
BAND_HOLE_W = 3.5
BAND_HOLE_H = 2.0

# ---- rear phone cap: sliding C-channel, open at both ends ------------------
# Phone slides in along x (from the right in normal use) and friction holds it
# wherever the chosen lens is over the aperture. The cap collar grips the rear
# body; the rails hold the phone by its screen-side edge and both long sides.
PHONE_RAIL_T = 3.5             # rail wall, thicker than the old 2 mm shroud
PHONE_RAIL_CLR = 0.15          # per side, snug sliding fit on the cased phone
PHONE_RAIL_X0 = -60.0
PHONE_RAIL_X1 = 180.0          # 240 mm long: about 75 mm of lens travel
PHONE_CONN_X0 = -50.0          # web under the rails, only around the collar
PHONE_CONN_X1 = 50.0
PHONE_CAP_SKIRT_H = 12.0       # cap collar down the outside of the rear body
PHONE_CAP_T = 2.0
PHONE_CAP_CLR = 0.20           # per side over the 90 mm rear body
PHONE_LIP_W = 2.2              # lip over the phone's screen-side edge

# ---- aperture stop sliders (Phase 4) -------------------------------------
# Each stop is a flat slider that drops into a slot from the top and rests on
# the cavity floor, exactly like the screen frame - no tape, no loose discs.
# It has its own slot just behind the plate: a stop works by cutting the light
# cone *at* the lens, so it gets weaker (less depth of field) the further back
# it sits.  Same geometry also fits any focus slot, with that caveat.
STOP_SLOT_Z = 17.0         # 2.85 mm behind the plate's spigot face (13.0)
STOP_W = FRAME_W                              # 85.5 : same 1.75 mm slot engagement
STOP_Y0 = FRAME_Y0                            # -40.9 : rests on the cavity floor
STOP_Y1 = 29.0             # top of the web disc: covers the cone (r <= 27.4)
STOP_WEB_D = 58.0          # disc that blocks the cone, radius 29
STOP_WEB_T = 0.9           # thin: it only has to be opaque
STOP_PAD_W = 3.15          # thick end pads that fill the slot
STOP_PAD_T = 2.3           # slot is 2.5 -> 0.1 mm play, same as the frame
STOP_BAR_HALF_H = 10.0     # web bar joining the disc to the pads
STOP_TAB_W = 14.0          # pull tab, above the cone so it cannot leak light
STOP_TAB_Y0 = 25.0         # tab starts inside the web disc, so it fuses cleanly
STOP_TAB_TOP = 38.0        # clear of the lid ridge, like the screen frame
STOP_INDEX_D = 1.6         # index dots in the tab: count them to tell sliders apart
STOP_INDEX_PITCH = 2.2
STOP_INDEX_Y = 34.5
STOP_LAYOUT_COLS = 2
STOP_LAYOUT_GAP = 3.0

STOP_NOMINAL_F = 64.0      # measured focal length, only for reference
STOP_SCREEN_Z = 70.0       # nominal film plane, for the f-number table
# hole diameters; with the stop at STOP_SLOT_Z, N = (STOP_SCREEN_Z - STOP_SLOT_Z) / hole
STOP_HOLES = [10.0, 7.0, 5.0, 3.6, 2.5, 1.8]

# ---- process --------------------------------------------------------------
SLIP = FIT            # sliding fits
PRESS = 0.25          # interference for pins
PILOT_D = 2.7         # M3 thread-forming pilot in PLA
