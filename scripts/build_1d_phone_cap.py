"""Rear phone cap - a sliding C-channel that replaces the bolt-on carrier.

The collar grips the outside of the rear body (friction, no glue). Two long
rails hold the phone by its screen-side edge and both long sides; the phone
slides in along x (from the right in normal use) and friction holds it with
whichever lens is over the Ø22 aperture. Both ends are open for full travel.

Print as modelled (z up), no supports.

Run:  exec(open('/home/alex/Work/camera-box/scripts/build_1d_phone_cap.py').read(), globals())
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

DOC_NAME = "camera_phone_cap"
V = App.Vector


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def finish(shape, name):
    shape = shape.removeSplitter()
    print(f"  {name}: vol={shape.Volume:,.0f} mm3  faces={len(shape.Faces)}  "
          f"solids={len(shape.Solids)}")
    return shape


# ---- channel cross-section -------------------------------------------------
y_bottom_in = PHONE_Y0 - PHONE_RAIL_CLR      # -65.05
y_top_in = BUTTON_Y + PHONE_RAIL_CLR         # 18.15, clears the +0.4 buttons
y_bottom_out = y_bottom_in - PHONE_RAIL_T    # -68.55
y_top_out = y_top_in + PHONE_RAIL_T          # 21.65
z_rail0 = REAR_FACE_Z                        # 220
z_rail1 = LIP_Z1                             # 235.4

# ---- collar around the rear body -----------------------------------------
cap_od = OUT_W + 2 * PHONE_CAP_CLR + 2 * PHONE_CAP_T   # 94.4
cap_id = OUT_W + 2 * PHONE_CAP_CLR                     # 90.4
collar = box(-cap_od / 2, cap_od / 2, -cap_od / 2, cap_od / 2,
             REAR_FACE_Z - PHONE_CAP_SKIRT_H, REAR_FACE_Z)
collar = collar.cut(box(-cap_id / 2, cap_id / 2, -cap_id / 2, cap_id / 2,
                        REAR_FACE_Z - PHONE_CAP_SKIRT_H - 1, REAR_FACE_Z + 1))
# lead-in on the forward edge
edges = [e for e in collar.Edges
         if abs(e.BoundBox.ZMin - (REAR_FACE_Z - PHONE_CAP_SKIRT_H)) < 1e-6
         and e.Length > 80.0]
if edges:
    collar = collar.makeChamfer(PLATE_SKIRT_LEAD, edges)

cap = collar

# ---- webs tying the rails to the collar -----------------------------------
# bottom web sits outside the body footprint, so it can drop below z = 220
bottom_web = box(PHONE_CONN_X0, PHONE_CONN_X1, y_bottom_out, -cap_id / 2,
                 REAR_FACE_Z - 2.0, REAR_FACE_Z + 1.5)
# top web stays above the body face; y = 18.15..47.2 never covers the foam ring
top_web = box(PHONE_CONN_X0, PHONE_CONN_X1, y_top_in, cap_od / 2,
              REAR_FACE_Z, REAR_FACE_Z + 1.5)
cap = cap.fuse(bottom_web).fuse(top_web)

# ---- the two rails and their screen-side lips ------------------------------
bottom_rail = box(PHONE_RAIL_X0, PHONE_RAIL_X1, y_bottom_out, y_bottom_in,
                  z_rail0, z_rail1)
top_rail = box(PHONE_RAIL_X0, PHONE_RAIL_X1, y_top_in, y_top_out,
               z_rail0, z_rail1)

# lips overlap the rails by 0.1 mm so the fuse is clean; 0.2 mm above the screen
bottom_lip = box(PHONE_RAIL_X0, PHONE_RAIL_X1, y_bottom_in - 0.1,
                 y_bottom_in + PHONE_LIP_W, LIP_Z0, LIP_Z1)
top_lip = box(PHONE_RAIL_X0, PHONE_RAIL_X1, y_top_in - PHONE_LIP_W,
              y_top_in + 0.1, LIP_Z0, LIP_Z1)

for s in (bottom_rail, top_rail, bottom_lip, top_lip):
    cap = cap.fuse(s)

# index tick at x = 0 on the top lip: main-lens reference
tick = box(-0.4, 0.4, y_top_in - PHONE_LIP_W + 0.2, y_top_in - 0.2,
           LIP_Z1 - 0.5, LIP_Z1 + 1)
cap = cap.cut(tick)

cap = finish(cap, "PhoneCap")

if len(cap.Solids) != 1:
    raise RuntimeError(f"phone cap is {len(cap.Solids)} solids, expected 1")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
obj = doc.addObject("Part::Feature", "PhoneCap")
obj.Shape = cap
if getattr(obj, "ViewObject", None):
    obj.ViewObject.ShapeColor = (0.13, 0.13, 0.13)
doc.recompute()

fcstd = os.path.join(PARTS, "camera_phone_cap.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

for ext in ("stl", "3mf"):
    Mesh.export([obj], os.path.join(EXPORTS, f"camera_phone_cap.{ext}"))
print("exports written to", EXPORTS)

# ------------------------------------------------------------------ self-check
print("\n--- geometry check ---")
checks = []


def chk(label, x, y, z, want):
    got = cap.isInside(V(x, y, z), 1e-6, True)
    checks.append((label, got == want, got, want))


chk("collar wall solid", 46.0, 0.0, 214.0, True)
chk("collar cavity open", 44.0, 0.0, 214.0, False)
chk("bottom rail solid", 0.0, -67.0, 228.0, True)
chk("top rail solid", 0.0, 19.5, 228.0, True)
chk("channel open", 0.0, 0.0, 228.0, False)
chk("bottom lip solid", 0.0, -64.5, 234.4, True)
chk("top lip solid", 0.0, 17.5, 234.4, True)
chk("screen clearance", 0.0, 0.0, 233.4, False)
chk("foam ring clear", 0.0, 0.0, 220.5, False)
chk("index tick cut", 0.0, 17.5, 235.2, False)
chk("rail beyond body", 120.0, -67.0, 228.0, True)

# the phone must fit through the whole travel range
bad_pts = 0
total = 0
for dx in (-25.0, 0.0, 25.0, 45.0):
    for xi in range(33):
        x = PHONE_X0 + dx + (xi + 0.5) * (CASE_L / 33.0)
        for yi in range(17):
            y = PHONE_Y0 + (yi + 0.5) * (CASE_W / 17.0)
            for z in (221.8, 227.0, 233.1):
                total += 1
                if cap.isInside(V(x, y, z), 1e-6, True):
                    bad_pts += 1
checks.append((f"phone volume free at 4 stops ({total} pts)", bad_pts == 0,
               bad_pts, 0))

bad = 0
for label, ok, got, want in checks:
    if not ok:
        print(f"  [BAD] {label}: inside={got} (want {want})")
    bad += 0 if ok else 1
print(f"{len(checks) - bad}/{len(checks)} checks passed")

# ---- no interference with the rest of the camera ---------------------------
print("\n--- fit with the existing body ---")
for path in ("camera_rear_body.FCStd", "camera_lids.FCStd"):
    d = App.openDocument(os.path.join(PARTS, path))
    for o in d.Objects:
        vol = cap.common(o.Shape).Volume
        print(f"  [{'ok ' if vol < 0.05 else 'BAD'}] {path}:{o.Name} "
              f"overlap {vol:.3f} mm3")
        bad += 0 if vol < 0.05 else 1
    App.closeDocument(d.Name)

b = cap.BoundBox
print(f"\nPhoneCap: X {b.XMin:.2f}..{b.XMax:.2f}  Y {b.YMin:.2f}..{b.YMax:.2f}  "
      f"Z {b.ZMin:.2f}..{b.ZMax:.2f}")
print(f"phone channel Y {y_bottom_in:.2f}..{y_top_in:.2f}, "
      f"X {PHONE_RAIL_X0:.0f}..{PHONE_RAIL_X1:.0f}")
print("RESULT:", "all good" if bad == 0 else f"{bad} PROBLEM(S)")
