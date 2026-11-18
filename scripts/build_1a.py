"""Phase 1A - front body: front plate + slotted tube.

Run inside FreeCAD (GUI) so Mesh export is available:
    exec(open('/home/alex/Work/camera-box/scripts/build_1a.py').read(), globals())
"""

import os

import FreeCAD as App
import Mesh
import Part

HERE = "/home/alex/Work/camera-box/scripts"
exec(open(os.path.join(HERE, "params.py")).read(), globals())

PARTS = os.path.join(os.path.dirname(HERE), "parts")
EXPORTS = os.path.join(os.path.dirname(HERE), "exports")
os.makedirs(PARTS, exist_ok=True)
os.makedirs(EXPORTS, exist_ok=True)

DOC_NAME = "camera_front_body"
V = App.Vector


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl(dia, z0, z1, x=0.0, y=0.0):
    return Part.makeCylinder(dia / 2.0, z1 - z0, V(x, y, z0), V(0, 0, 1))


def finish(shape, name):
    shape = shape.removeSplitter()
    print(f"  {name}: vol={shape.Volume:,.0f} mm3  faces={len(shape.Faces)}")
    return shape


# ---------------------------------------------------------------- front plate
spigot_half = INNER_W / 2 - FIT                     # 40.85
plate = box(-OUT_W / 2, OUT_W / 2, -OUT_H / 2, OUT_H / 2, 0, PLATE_T)
plate = plate.fuse(box(-spigot_half, spigot_half, -spigot_half, spigot_half,
                       PLATE_T, PLATE_T + PLATE_SPIGOT))
plate = plate.cut(cyl(BORE_D, -1, PLATE_T + PLATE_SPIGOT + 1))
# optional aperture-stop disc pocket, behind the glass, on the spigot end face
plate = plate.cut(cyl(APERTURE_RECESS_D,
                      PLATE_T + PLATE_SPIGOT - APERTURE_RECESS_DEPTH,
                      PLATE_T + PLATE_SPIGOT))

# outer cap/skirt: slides over the front of the tube so the plate can't fall
# off or tilt; also helps retain the front lid (which sits inside the collar)
# goes BACK along the outside of the tube (into +z) so it can print with the
# flange on the bed, spigot up
skirt_od = OUT_W + 2 * PLATE_SKIRT_CLR + 2 * PLATE_SKIRT_T
skirt_id = OUT_W + 2 * PLATE_SKIRT_CLR
tube_z0 = PLATE_T  # 5.0
# full collar: outer box minus inner cavity plus corners? Or just a frame.
# easier: start from a thick box and hollow it out, keeping all four walls
skirt = box(-skirt_od / 2, skirt_od / 2, -skirt_od / 2, skirt_od / 2,
            0, tube_z0 + PLATE_SKIRT_H)
hole = box(-skirt_id / 2, skirt_id / 2, -skirt_id / 2, skirt_id / 2,
           -1, tube_z0 + PLATE_SKIRT_H + 1)
skirt = skirt.cut(hole)
# lead-in chamfer on the rear edge of the skirt, so it goes on square
skirt_edges = [e for e in skirt.Edges
               if abs(e.BoundBox.ZMin) > tube_z0 + PLATE_SKIRT_H - 1e-6 and e.Length > 80.0]
if skirt_edges:
    skirt = skirt.makeChamfer(PLATE_SKIRT_LEAD, skirt_edges)
plate = plate.fuse(skirt)
plate = finish(plate, "FrontPlate")

# ------------------------------------------------------------------- the tube
Z0 = PLATE_T
Z1 = PLATE_T + TUBE_LEN

tube = box(-OUT_W / 2, OUT_W / 2, -OUT_H / 2, OUT_H / 2, Z0, Z1)

# open top + cavity (over-cut past the top so the roof is fully removed)
tube = tube.cut(box(-INNER_W / 2, INNER_W / 2,
                    -OUT_H / 2 + WALL, OUT_H / 2 + 1,
                    Z0 - 1, Z1 + 1))
# flush lid rebate: 2 mm x 4 mm step on the outside of the top rim
for sx in (-1, 1):
    x_in = sx * INNER_W / 2
    x_out = sx * (INNER_W / 2 + LID_REBATE_W)
    tube = tube.cut(box(min(x_in, x_out), max(x_in, x_out),
                        OUT_H / 2 - LID_T, OUT_H / 2 + 1,
                        Z0 - 1, Z1 + 1))

# focus slots: vertical pockets in both side walls, frame drops in from the top
for i in range(SLOT_COUNT):
    zc = SLOT_FIRST_Z + i * SLOT_PITCH
    for sx in (-1, 1):
        x_in = sx * INNER_W / 2
        x_out = sx * (INNER_W / 2 + SLOT_DEPTH)
        tube = tube.cut(box(min(x_in, x_out), max(x_in, x_out),
                            -OUT_H / 2 + WALL, SLOT_TOP_Y + 1,
                            zc - SLOT_W / 2, zc + SLOT_W / 2))

# dedicated stop slot: the aperture stop wants to be close to the lens, so it
# gets its own slot just behind the plate instead of borrowing a focus slot
for sx in (-1, 1):
    x_in = sx * INNER_W / 2
    x_out = sx * (INNER_W / 2 + SLOT_DEPTH)
    tube = tube.cut(box(min(x_in, x_out), max(x_in, x_out),
                        -OUT_H / 2 + WALL, SLOT_TOP_Y + 1,
                        STOP_SLOT_Z - SLOT_W / 2, STOP_SLOT_Z + SLOT_W / 2))

tube = finish(tube, "FrontTube")

# the stop slider must clear the plate's spigot, and the slot must not be so
# close to the first focus slot that the web between them gets thin
spigot_face = PLATE_T + PLATE_SPIGOT
stop_front = STOP_SLOT_Z - STOP_PAD_T / 2
print(f"  stop slot {STOP_SLOT_Z:.0f} ({STOP_SLOT_Z - SLOT_W / 2:.2f}..{STOP_SLOT_Z + SLOT_W / 2:.2f}),"
      f" slider {stop_front:.2f}..{STOP_SLOT_Z + STOP_PAD_T / 2:.2f},"
      f" clearance to spigot face {stop_front - spigot_face:.2f} mm")
if stop_front - spigot_face < 0.5:
    raise RuntimeError("stop slider clashes with the plate spigot")
print(f"  web to first focus slot: {(SLOT_FIRST_Z - SLOT_W / 2) - (STOP_SLOT_Z + SLOT_W / 2):.2f} mm")

# the rearmost slot must leave the screen frame clear of the rear body's spigot
frame_rear = SLOT_LAST_Z + FRAME_HALF_T
clear = REAR_SPIGOT_FACE_Z - frame_rear
print(f"  slots {SLOT_FIRST_Z:.0f}..{SLOT_LAST_Z:.0f} ({SLOT_COUNT}) at {SLOT_PITCH:.0f} mm pitch")
print(f"  last frame position: rear face {frame_rear:.2f}, spigot face "
      f"{REAR_SPIGOT_FACE_Z:.1f}, clearance {clear:.2f} mm")
if clear < 0.5:
    raise RuntimeError(f"rearmost slot {SLOT_LAST_Z} clashes with the rear spigot "
                       f"({clear:.2f} mm clearance) - reduce SLOT_COUNT")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)

for shape, name in ((plate, "FrontPlate"), (tube, "FrontTube")):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if getattr(obj, "ViewObject", None):
        obj.ViewObject.ShapeColor = (0.13, 0.13, 0.13)
doc.recompute()

fcstd = os.path.join(PARTS, "camera_front_body.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

# --------------------------------------------------------------------- export
for obj in doc.Objects:
    for ext in ("stl", "3mf"):
        path = os.path.join(EXPORTS, f"camera_front_{obj.Name.lower().replace('front','')}.{ext}")
        Mesh.export([obj], path)
Mesh.export(list(doc.Objects), os.path.join(EXPORTS, "camera_front_body.3mf"))
print("exports written to", EXPORTS)

# ------------------------------------------------------------------- sanity
for obj in doc.Objects:
    bb = obj.Shape.BoundBox
    print(f"{obj.Name}: X {bb.XLength:.2f}  Y {bb.YLength:.2f}  Z {bb.ZLength:.2f}"
          f"  solids={len(obj.Shape.Solids)}")
