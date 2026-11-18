"""Phase 3 - two-piece focusing-screen frame.

sheet_frame_front : plate + 0.45 mm sheet pocket + 4 press-fit pins
sheet_frame_back  : plate + 4 matched sockets

Both halves are built at the z of one focus slot (49 mm) so the export can be
checked straight against the body; the slot you actually use is your choice.

Run:  exec(open('/home/alex/Work/camera-box/scripts/build_3_screen.py').read(), globals())
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

DOC_NAME = "camera_screen"
V = App.Vector

ZX = FRAME_TEST_SLOT
Z_MID = ZX                          # interface plane, at the slot centre
AP = FRAME_APERTURE / 2.0


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl_z(dia, z0, z1, x=0.0, y=0.0):
    return Part.makeCylinder(dia / 2.0, z1 - z0, V(x, y, z0), V(0, 0, 1))


def plate(name, z0, z1):
    s = box(-FRAME_W / 2, FRAME_W / 2, FRAME_Y0, FRAME_Y1, z0, z1)
    s = s.cut(box(-AP, AP, -AP, AP, z0 - 1, z1 + 1))
    print(f"  {name} blank: vol={s.Volume:,.0f} mm3")
    return s


# ------------------------------------------------------------------ front half
front = plate("front", Z_MID - FRAME_HALF_T, Z_MID)
# sheet pocket, opens toward the back half
front = front.cut(box(-FRAME_POCKET_W / 2, FRAME_POCKET_W / 2,
                      -FRAME_POCKET_H / 2, FRAME_POCKET_H / 2,
                      Z_MID - FRAME_POCKET_D, Z_MID + 1))
# pins
for px, py in FRAME_PINS:
    front = front.fuse(cyl_z(FRAME_PIN_D, Z_MID, Z_MID + FRAME_PIN_H, px, py))
front = front.removeSplitter()

# ------------------------------------------------------------------- back half
back = plate("back", Z_MID, Z_MID + FRAME_HALF_T)
for px, py in FRAME_PINS:
    back = back.cut(cyl_z(FRAME_SOCKET_D, Z_MID - 1,
                          Z_MID + FRAME_HALF_T + 1, px, py))
back = back.removeSplitter()

for label, s in (("SheetFrameFront", front), ("SheetFrameBack", back)):
    print(f"  {label}: vol={s.Volume:,.0f} mm3  faces={len(s.Faces)}  solids={len(s.Solids)}")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
objs = []
for shape, name in ((front, "SheetFrameFront"), (back, "SheetFrameBack")):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    if getattr(o, "ViewObject", None):
        o.ViewObject.ShapeColor = (0.85, 0.85, 0.8)
    objs.append(o)
doc.recompute()

fcstd = os.path.join(PARTS, "camera_screen.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

for o in objs:
    stem = "sheet_frame_front" if o.Name == "SheetFrameFront" else "sheet_frame_back"
    for ext in ("stl", "3mf"):
        Mesh.export([o], os.path.join(EXPORTS, f"{stem}.{ext}"))
Mesh.export(objs, os.path.join(EXPORTS, "camera_screen.3mf"))
print("exports written to", EXPORTS)

# ------------------------------------------------------------------ self-check
print("\n--- geometry check ---")
checks = []


def chk(label, shape, x, y, z, want):
    got = shape.isInside(V(x, y, z), 1e-6, True)
    checks.append((label, got == want, got, want))


chk("aperture open (front)", front, 0, 0, Z_MID - 0.5, False)
chk("aperture open (back)", back, 0, 0, Z_MID + 0.5, False)
chk("rim solid", front, 35, 0, Z_MID - 0.5, True)
chk("pocket void", front, 0, 32, Z_MID - 0.1, False)
chk("pocket floor", front, 0, 32, Z_MID - FRAME_HALF_T + 0.2, True)
chk("front face flat", front, 0, 32, Z_MID - FRAME_HALF_T + 0.01, True)
chk("pin present", front, -30, 34.5, Z_MID + 0.8, True)
chk("socket void", back, -30, 34.5, Z_MID + 0.8, False)
chk("back beside socket", back, -30 + 2.0, 34.5, Z_MID + 0.5, True)
chk("back shell", back, 35, 0, Z_MID + 0.5, True)
chk("frame below lid ledge", front, 0, 37.5, Z_MID - 0.5, True)
chk("frame top ends at 38", front, 0, 38.5, Z_MID - 0.5, False)

bad = 0
for label, ok, got, want in checks:
    print(f"  [{'ok ' if ok else 'BAD'}] {label:<24} inside={got} (want {want})")
    bad += 0 if ok else 1
print(f"{len(checks) - bad}/{len(checks)} checks passed")

# -------------------------------------------------- slot engagement + clashes
print("\n--- fit in the front tube ---")
d1 = App.openDocument(os.path.join(PARTS, "camera_front_body.FCStd"))
tube = d1.getObject("FrontTube").Shape
d3 = App.openDocument(os.path.join(PARTS, "camera_lids.FCStd"))
lid_f = d3.getObject("FrontLid").Shape

stack = front.fuse(back)
for label, a, b in (("screen stack / tube", stack, tube),
                    ("screen stack / front lid", stack, lid_f),
                    ("front / back halves", front, back)):
    vol = a.common(b).Volume
    print(f"  [{'ok ' if vol < 1.0 else 'BAD'}] {label:<24} overlap={vol:.2f} mm3")
    bad += 0 if vol < 1.0 else 1

inside_slot = not tube.isInside(V(FRAME_W / 2 - 0.2, 0, ZX), 1e-6, True)
web = tube.isInside(V(FRAME_W / 2 - 0.2, 0, ZX - 2.0), 1e-6, True)
print(f"  [{'ok ' if inside_slot else 'BAD'}] edge sits in the slot void at z={ZX}")
print(f"  [{'ok ' if web else 'BAD'}] wall is solid 2 mm away at z={ZX - 2.0} (slot web)")
bad += (0 if inside_slot else 1) + (0 if web else 1)

for d in (d1, d3):
    App.closeDocument(d.Name)

for label, s in (("front", front), ("back", back)):
    b = s.BoundBox
    print(f"{label}: X {b.XMin:.2f}..{b.XMax:.2f}  Y {b.YMin:.2f}..{b.YMax:.2f}  "
          f"Z {b.ZMin:.2f}..{b.ZMax:.2f}  t={b.ZLength:.2f}")
print("RESULT:", "all good" if bad == 0 else f"{bad} PROBLEM(S)")
