"""Phase 2 - two flush top lids.

camera_front_lid : z = 5 .. 110  (upper half) / .. 115 (lower half, 10 mm lap)
camera_rear_lid  : z = 105 .. 220 (upper half) / 115 .. 220 (lower half)

Each lid is a 86.7 x 3.9 plate sitting in the 87 x 4 rebate, with a 2 x 1.5 mm
ridge on the underside that drops into the cavity as a light baffle, and an
0.8 mm chamfer along the two top edges as a fingernail groove.

Run:  exec(open('/home/alex/Work/camera-box/scripts/build_2_lids.py').read(), globals())
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

DOC_NAME = "camera_lids"
V = App.Vector

Z_SEAM = LID_SEAM_Z
Z_UP = Z_SEAM - LID_LAP / 2.0      # 105 : upper-half joint
Z_LO = Z_SEAM + LID_LAP / 2.0      # 115 : lower-half joint


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def wedge(x_outer, size, z0, z1):
    """45 deg chamfer cutter for the top outer edge at x_outer (+ or -).

    The cut plane passes exactly through (x_outer - size, LID_Y1) and
    (x_outer, LID_Y1 - size); the triangle is extended outward so it
    clears the corner on all sides.
    """
    s = 1.0 if x_outer > 0 else -1.0
    pts = [(x_outer - s * (size + 2.0), LID_Y1 + 2.0),
           (x_outer + s * 2.0, LID_Y1 + 2.0),
           (x_outer + s * 2.0, LID_Y1 - size - 2.0)]
    poly = [V(x, y, z0) for x, y in pts]
    poly.append(poly[0])
    return Part.Face(Part.makePolygon(poly)).extrude(V(0, 0, z1 - z0))


def lid(upper_z0, upper_z1, lower_z0, lower_z1, flange_z, chamfer_z):
    shape = box(-LID_XH, LID_XH, LID_SPLIT_Y, LID_Y1, upper_z0, upper_z1)
    shape = shape.fuse(box(-LID_XH, LID_XH, LID_Y0, LID_SPLIT_Y, lower_z0, lower_z1))
    for sx in (-1, 1):
        x0 = min(sx * LID_FLANGE_X0, sx * LID_FLANGE_X1)
        x1 = max(sx * LID_FLANGE_X0, sx * LID_FLANGE_X1)
        shape = shape.fuse(box(x0, x1, LID_Y0 - LID_FLANGE_T, LID_Y0,
                               flange_z[0], flange_z[1]))
        shape = shape.cut(wedge(sx * LID_XH, LID_CHAMFER, chamfer_z[0], chamfer_z[1]))
    return shape.removeSplitter()


front = lid(PLATE_T, Z_UP, PLATE_T, Z_LO,
            LID_FRONT_FLANGE_Z, (PLATE_T, Z_UP))
rear = lid(Z_UP, REAR_FACE_Z, Z_LO, REAR_FACE_Z,
           LID_REAR_FLANGE_Z, (Z_UP, REAR_FACE_Z))

print(f"  FrontLid: vol={front.Volume:,.0f} mm3  faces={len(front.Faces)}  "
      f"solids={len(front.Solids)}")
print(f"  RearLid : vol={rear.Volume:,.0f} mm3  faces={len(rear.Faces)}  "
      f"solids={len(rear.Solids)}")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
objs = []
for shape, name in ((front, "FrontLid"), (rear, "RearLid")):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    if getattr(o, "ViewObject", None):
        o.ViewObject.ShapeColor = (0.13, 0.13, 0.13)
    objs.append(o)
doc.recompute()

fcstd = os.path.join(PARTS, "camera_lids.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

for o in objs:
    stem = "camera_front_lid" if o.Name == "FrontLid" else "camera_rear_lid"
    for ext in ("stl", "3mf"):
        Mesh.export([o], os.path.join(EXPORTS, f"{stem}.{ext}"))
Mesh.export(objs, os.path.join(EXPORTS, "camera_lids.3mf"))
print("exports written to", EXPORTS)

# ------------------------------------------------------------------ self-check
print("\n--- geometry check ---")
checks = []


def chk(label, shape, x, y, z, want):
    got = shape.isInside(V(x, y, z), 1e-6, True)
    checks.append((label, got == want, got, want))


chk("front lid upper", front, 0, 44.0, 50, True)
chk("front lid lower", front, 0, 42.0, 50, True)
chk("front lid tail kept", front, 0, 42.0, 112, True)
chk("front lid tail upper gone", front, 0, 44.0, 112, False)
chk("front lid stops at plate", front, 0, 43.0, 4.5, False)
chk("front lid ends at 115", front, 0, 42.0, 116, False)
chk("rear lid nose upper", rear, 0, 44.0, 112, True)
chk("rear lid nose lower gone", rear, 0, 42.0, 112, False)
chk("rear lid full at 200", rear, 0, 42.0, 200, True)
chk("rear lid starts at 105", rear, 0, 44.0, 104, False)
chk("rear lid ends flush", rear, 0, 42.0, 220.5, False)
chk("front flange", front, 39.8, 40.0, 50, True)
chk("front flange absent at tail", front, 39.8, 40.0, 112, False)
chk("rear flange", rear, -39.8, 40.0, 160, True)
chk("rear flange stops at wall", rear, -39.8, 40.0, 213, False)
chk("chamfer removed", front, LID_XH - 0.1, LID_Y1 - 0.1, 50, False)
chk("inner edge intact", front, LID_XH - 1.2, LID_Y1 - 0.1, 50, True)

bad = 0
for label, ok, got, want in checks:
    print(f"  [{'ok ' if ok else 'BAD'}] {label:<26} inside={got} (want {want})")
    bad += 0 if ok else 1
print(f"{len(checks) - bad}/{len(checks)} checks passed")

# --- interference with the bodies and with each other ----------------------
print("\n--- interference ---")
d1 = App.openDocument(os.path.join(PARTS, "camera_front_body.FCStd"))
tube = d1.getObject("FrontTube").Shape
plate = d1.getObject("FrontPlate").Shape
d2 = App.openDocument(os.path.join(PARTS, "camera_rear_body.FCStd"))
rear_body = d2.getObject("RearBody").Shape

for label, a, b in (("front lid / plate", front, plate),
                    ("front lid / tube", front, tube),
                    ("front lid / rear body", front, rear_body),
                    ("rear lid / rear body", rear, rear_body),
                    ("front lid / rear lid", front, rear)):
    vol = a.common(b).Volume
    print(f"  [{'ok ' if vol < 1.0 else 'BAD'}] {label:<24} overlap={vol:.2f} mm3")
    bad += 0 if vol < 1.0 else 1

for d in (d1, d2):
    App.closeDocument(d.Name)

for label, shape in (("FrontLid", front), ("RearLid", rear)):
    b = shape.BoundBox
    print(f"{label}: X {b.XMin:.2f}..{b.XMax:.2f}  Y {b.YMin:.2f}..{b.YMax:.2f}  "
          f"Z {b.ZMin:.2f}..{b.ZMax:.2f}  len {b.ZLength:.1f}")
print("seam: upper joint z=105, lower joint z=115, lap 10 mm")
print("RESULT:", "all good" if bad == 0 else f"{bad} PROBLEM(S)")
