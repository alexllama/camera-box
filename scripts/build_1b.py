"""Phase 1B - rear body: spigot, tube, lid rebate, rear wall, camera aperture.

Run inside FreeCAD (GUI):
    exec(open('/home/alex/Work/camera-box/scripts/build_1b.py').read(), globals())
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

DOC_NAME = "camera_rear_body"
V = App.Vector


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl(dia, z0, z1, x=0.0, y=0.0):
    return Part.makeCylinder(dia / 2.0, z1 - z0, V(x, y, z0), V(0, 0, 1))


def finish(shape, name):
    shape = shape.removeSplitter()
    print(f"  {name}: vol={shape.Volume:,.0f} mm3  faces={len(shape.Faces)}")
    return shape


Z0 = PLATE_T + TUBE_LEN          # 110 : rear body front face
Z1 = Z0 + REAR_LEN               # 220 : rear wall outer face
ZW = Z1 - REAR_WALL_T            # 212 : rear wall inner face

# ------------------------------------------------------------------- the tube
rear = box(-OUT_W / 2, OUT_W / 2, -OUT_H / 2, OUT_H / 2, Z0, Z1)

# spigot size, and the shoulder it grows out of
sp = INNER_W / 2 - FIT                 # 40.85 : spigot outer half-width
sw = sp - REAR_SPIGOT_WALL             # 38.85 : spigot inner half-width

# cavity, open top.  The front 2 mm keeps a 2.15 mm inward shoulder so the
# spigot ring has material to attach to (a ring inside an 82 mm cavity would
# otherwise float).
rear = rear.cut(box(-sw, sw, -OUT_H / 2 + WALL, OUT_H / 2 + 1, Z0 - 1, Z0 + 2.5))
rear = rear.cut(box(-INNER_W / 2, INNER_W / 2,
                    -OUT_H / 2 + WALL, OUT_H / 2 + 1,
                    Z0 + 2.0, ZW))
# keep that shoulder out of the lid seat
rear = rear.cut(box(-INNER_W / 2, INNER_W / 2,
                    OUT_H / 2 - LID_T, OUT_H / 2 + 1, Z0 - 1, Z0 + 2.5))

# flush lid rebate: full 87 mm width so the lid can also pass over the 8 mm
# rear wall, leaving one continuous top surface (over the cavity this is the
# same cut the open top already made)
rear = rear.cut(box(-INNER_W / 2 - LID_REBATE_W, INNER_W / 2 + LID_REBATE_W,
                    OUT_H / 2 - LID_T, OUT_H / 2 + 1,
                    Z0 - 1, Z1 + 1))

# spigot: laps 12 mm into the front tube, 0.15 mm clearance
rear = rear.fuse(box(-sp, sp, -sp, sp, Z0 - REAR_SPIGOT, Z0 + 1.5)
                 .cut(box(-sw, sw, -sw, sw, Z0 - REAR_SPIGOT - 1, Z0 + 2.5)))

# camera aperture, flared on the inside as a light baffle
rear = rear.cut(cyl(CAM_APERTURE_D, ZW - 1, Z1 + 1))
rear = rear.cut(Part.makeCone(CAM_CHAMFER_D / 2.0, CAM_APERTURE_D / 2.0,
                              2.0, V(0, 0, ZW), V(0, 0, 1)))

# shallow locating step for the foam seal ring
rear = rear.cut(cyl(FOAM_RING_OD, Z1 - FOAM_RECESS_D, Z1 + 1))

# four blind pilot holes for the phone carrier (M3 x 6 mm -> 2 mm stays solid)
for hx, hy in CARRIER_HOLES:
    rear = rear.cut(cyl(PILOT_D, Z1 - PILOT_DEPTH, Z1 + 1, hx, hy))

rear = finish(rear, "RearBody")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
obj = doc.addObject("Part::Feature", "RearBody")
obj.Shape = rear
if getattr(obj, "ViewObject", None):
    obj.ViewObject.ShapeColor = (0.13, 0.13, 0.13)
doc.recompute()

fcstd = os.path.join(PARTS, "camera_rear_body.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

for ext in ("stl", "3mf"):
    Mesh.export([obj], os.path.join(EXPORTS, f"camera_rear_body.{ext}"))
print("exports written to", EXPORTS)

bb = rear.BoundBox
print(f"RearBody: X {bb.XLength:.2f}  Y {bb.YLength:.2f}  Z {bb.ZLength:.2f}  "
      f"z {bb.ZMin:.2f}..{bb.ZMax:.2f}  solids={len(rear.Solids)}")

print("carrier pilot holes (open at z=217, still solid at z=213):")
for hx, hy in CARRIER_HOLES:
    print(f"  ({hx:+6.1f},{hy:+6.1f})  open={not rear.isInside(V(hx, hy, 217), 1e-6, True)}"
          f"  plugged={rear.isInside(V(hx, hy, 213), 1e-6, True)}")
