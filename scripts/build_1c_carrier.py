"""Phase 1B accessory - phone carrier.

Frame bolts to the rear wall (4 x M3 into blind pilots) and holds the phone
landscape, buttons up, lens on the optical axis.  A sliding jaw at the right
end is pushed by an M5 screw running in a standard nut pocket; a band may be
used instead (buttonholes in the top/bottom rails + notches in the jaw).

Run:  exec(open('/home/alex/Work/camera-box/scripts/build_1c_carrier.py').read(), globals())
"""

import math
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

DOC_NAME = "camera_carrier"
V = App.Vector


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl_z(dia, z0, z1, x=0.0, y=0.0):
    return Part.makeCylinder(dia / 2.0, z1 - z0, V(x, y, z0), V(0, 0, 1))


def cyl_x(dia, x0, x1, y=0.0, z=0.0):
    return Part.makeCylinder(dia / 2.0, x1 - x0, V(x0, y, z), V(1, 0, 0))


def hex_x(af, x0, length, y, z):
    """Hexagonal prism with axis along x, AF across flats."""
    r = af / 2.0 / math.cos(math.radians(30))
    pts = [V(x0, y + r * math.cos(math.radians(30 + 60 * k)),
             z + r * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
    pts.append(pts[0])
    return Part.Face(Part.makePolygon(pts)).extrude(V(length, 0, 0))


def finish(shape, name):
    shape = shape.removeSplitter()
    print(f"  {name}: vol={shape.Volume:,.0f} mm3  faces={len(shape.Faces)}  "
          f"solids={len(shape.Solids)}")
    return shape


# ================================================================== the frame
frame = box(CARRIER_X0, CARRIER_X1, CARRIER_Y0, CARRIER_Y1, CARRIER_Z0, CARRIER_Z1)
frame = frame.cut(box(OPEN_X0, OPEN_X1, OPEN_Y0, OPEN_Y1,
                      CARRIER_Z0 - 1, CARRIER_Z1 + 1))

# fixed x-stop lip: 2.2 mm over the phone's front face, at the left end
frame = frame.fuse(box(OPEN_X0 - 1.0, OPEN_X0 + LIP_W,
                       PHONE_Y0 + 0.2, BUTTON_Y - 0.2,
                       LIP_Z0, LIP_Z1))

# four M3 countersunk fixing holes
for hx, hy in CARRIER_HOLES:
    frame = frame.cut(cyl_z(CARRIER_SCREW_BORE, CARRIER_Z0 - 1, CARRIER_Z1 + 1, hx, hy))
    frame = frame.cut(Part.makeCone(CARRIER_CSK_D / 2.0, CARRIER_SCREW_BORE / 2.0,
                                    (CARRIER_CSK_D - CARRIER_SCREW_BORE) / 2.0,
                                    V(hx, hy, CARRIER_Z1), V(0, 0, -1)))

# M5 pusher: clearance bore + hex nut pocket on the outer face
frame = frame.cut(cyl_x(PUSHER_BORE, OPEN_X1 - 1, CARRIER_X1 + 1, PUSHER_Y, PUSHER_Z))
frame = frame.cut(hex_x(NUT_AF, CARRIER_X1 - NUT_H, NUT_H + 1, PUSHER_Y, PUSHER_Z))

# band anchor buttonholes in the top and bottom rails
for y0, y1 in ((CARRIER_Y1 - 10, CARRIER_Y1 + 1),
               (CARRIER_Y0 - 1, CARRIER_Y0 + 10)):
    frame = frame.cut(box(BAND_HOLE_X - BAND_HOLE_W / 2, BAND_HOLE_X + BAND_HOLE_W / 2,
                          y0, y1,
                          PUSHER_Z - BAND_HOLE_H / 2, PUSHER_Z + BAND_HOLE_H / 2))

frame = finish(frame, "CarrierFrame")

# ==================================================================== the jaw
jaw = box(JAW_X0, JAW_X0 + JAW_T, PHONE_Y0 + 0.2, BUTTON_Y - 0.2, JAW_Z0, JAW_Z1)
jaw = jaw.fuse(box(JAW_X0 - LIP_W, JAW_X0 + JAW_T,
                   PHONE_Y0 + 0.2, BUTTON_Y - 0.2, LIP_Z0, LIP_Z1))

# socket for the pusher screw tip, so the jaw hangs on it and cannot be lost
jaw = jaw.cut(cyl_x(5.2, JAW_X0 + 0.5, JAW_X0 + JAW_T + 1, PUSHER_Y, PUSHER_Z))

# band notches in the jaw's top and bottom edges
for yc in (BUTTON_Y - 0.2 - 2.65, PHONE_Y0 + 0.2 + 2.65):
    jaw = jaw.cut(box(JAW_X0 - 1.0, JAW_X0 + JAW_T - 0.9,
                      yc - 2.65, yc + 2.65,
                      PUSHER_Z - BAND_HOLE_H / 2 - 0.5, PUSHER_Z + BAND_HOLE_H / 2 + 0.5))

jaw = finish(jaw, "CarrierJaw")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
objs = []
for shape, name in ((frame, "CarrierFrame"), (jaw, "CarrierJaw")):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    if getattr(o, "ViewObject", None):
        o.ViewObject.ShapeColor = (0.13, 0.13, 0.13)
    objs.append(o)
doc.recompute()

fcstd = os.path.join(PARTS, "camera_carrier.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

for o in objs:
    stem = "camera_carrier_frame" if o.Name == "CarrierFrame" else "camera_carrier_jaw"
    for ext in ("stl", "3mf"):
        Mesh.export([o], os.path.join(EXPORTS, f"{stem}.{ext}"))
Mesh.export(objs, os.path.join(EXPORTS, "camera_carrier.3mf"))
print("exports written to", EXPORTS)

# ------------------------------------------------------------------ self-check
print("\n--- geometry check ---")
checks = []


def chk(label, shape, x, y, z, want):
    got = shape.isInside(V(x, y, z), 1e-6, True)
    checks.append((label, got == want, got, want))


chk("top rail solid", frame, 0, 25.5, 228, True)
chk("left rail solid", frame, -38.4, 0, 228, True)
chk("bottom rail solid", frame, 60, -69, 228, True)
chk("right rail solid", frame, 145, 0, 228, True)
chk("opening clear", frame, 0, 0, 228, False)
chk("left stop lip", frame, OPEN_X0 + 1.0, 0, LIP_Z0 + 1.0, True)
chk("no lip above phone", frame, OPEN_X0 + 1.0, 20.9, LIP_Z0 + 1.0, False)
chk("screw bore void", frame, -38.4, -30, 224, False)
chk("csk void", frame, -38.4, -30, 235.5, False)
chk("screw thread wall", frame, -38.4 + 3.0, -30, 226.5, True)
chk("pusher bore void", frame, 140, PUSHER_Y, PUSHER_Z, False)
chk("nut pocket void", frame, 146.5, PUSHER_Y + 3.6, PUSHER_Z, False)
chk("rail above pocket", frame, 146.5, PUSHER_Y + 3.6, PUSHER_Z + 5.6, True)
chk("band hole top void", frame, BAND_HOLE_X, 25, PUSHER_Z, False)
chk("band hole bottom void", frame, BAND_HOLE_X, -69, PUSHER_Z, False)

chk("jaw body solid", jaw, JAW_X0 + 1.5, 0, 227, True)
chk("jaw lip solid", jaw, JAW_X0 - 1.0, 0, LIP_Z0 + 1.0, True)
chk("jaw socket void", jaw, JAW_X0 + 1.5, PUSHER_Y, PUSHER_Z, False)
chk("jaw band notch void", jaw, JAW_X0 + 1.0, 15.0, PUSHER_Z, False)
chk("jaw above notch solid", jaw, JAW_X0 + 1.0, 16.0, 222.0, True)

bad = 0
for label, ok, got, want in checks:
    print(f"  [{'ok ' if ok else 'BAD'}] {label:<24} inside={got} (want {want})")
    bad += 0 if ok else 1
print(f"{len(checks) - bad}/{len(checks)} checks passed")

b = frame.BoundBox
print(f"CarrierFrame: X {b.XMin:.2f}..{b.XMax:.2f}  Y {b.YMin:.2f}..{b.YMax:.2f}  "
      f"Z {b.ZMin:.2f}..{b.ZMax:.2f}")
b = jaw.BoundBox
print(f"CarrierJaw:   X {b.XMin:.2f}..{b.XMax:.2f}  Y {b.YMin:.2f}..{b.YMax:.2f}  "
      f"Z {b.ZMin:.2f}..{b.ZMax:.2f}")
print(f"phone:        X {PHONE_X0:.2f}..{PHONE_X1:.2f}  Y {PHONE_Y0:.2f}..{PHONE_Y1:.2f}  "
      f"front z={PHONE_FRONT_Z:.2f}")
