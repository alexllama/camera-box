"""Phase 4 - aperture stop sliders.

Each stop is a flat slider that drops into the stop slot from the top and rests
on the cavity floor, exactly like the screen frame. No tape, no loose discs: the
slot holds it, the slot's bottom puts the hole on the axis, and a pull tab above
the light cone lets you lift it out with two fingers.

Outline: 85.5 wide, so the 3.15 mm end pads sit 1.75 mm into both walls and fill
the 2.5 mm slot (2.3 thick). The cone is blocked by a 0.9 mm thick Ø58 web with
the aperture in it; the web only has to be opaque, so the part is light. Above
the cone sits a pull tab carrying one dot per slider, so you can count the dots
to sort them once they are out of their labelled bags.

The stop has its own slot at z = 17, just behind the plate: a stop works by
cutting the cone *at* the lens, and gets weaker the further back it sits. With
the screen at z = 70 the lever is 53 mm, so N = 53 / hole. The same part also
fits any focus slot (25, 29, ...), where the lever is shorter and the stop
correspondingly weaker - handy for seeing that effect, but the stop slot is the
honest position.

Printed flat, six on one plate, nothing needs support.

Run:  exec(open('/home/alex/Work/camera-box/scripts/build_4_stops.py').read(), globals())
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

DOC_NAME = "camera_stops"
V = App.Vector
W2 = STOP_W / 2.0
SLIDER_H = STOP_TAB_TOP - STOP_Y0                # 78.9 overall, tab included
Z_PLACE = STOP_SLOT_Z - STOP_PAD_T / 2.0         # 15.85: slider front face in the slot

# the sliders have to clear the plate's spigot and stay out of the focus slots
assert STOP_PAD_T < SLOT_W, "stop pad is thicker than the slot"
assert 0 < W2 - INNER_W / 2 <= SLOT_DEPTH, "stop pads must reach into both slots"
assert STOP_PAD_W > W2 - INNER_W / 2, "pads must be wider than they are engaged"


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def make_stop(hole_d, index):
    """One slider: front (lens-side) face at z = 0, aperture on the local axis."""
    web = Part.makeCylinder(STOP_WEB_D / 2.0, STOP_WEB_T, V(0, 0, 0), V(0, 0, 1))
    # bar out to the pads, so the disc cannot flap about on its own
    web = web.fuse(box(-W2, W2, -STOP_BAR_HALF_H, STOP_BAR_HALF_H, 0, STOP_WEB_T))
    # pull tab, above the cone, so it cannot leak light onto the sheet
    web = web.fuse(box(-STOP_TAB_W / 2, STOP_TAB_W / 2,
                       STOP_TAB_Y0, STOP_TAB_TOP, 0, STOP_WEB_T))
    # index dots in the tab: slider i carries i dots, so the set stays sorted
    for k in range(index):
        dx = (k - (index - 1) / 2.0) * STOP_INDEX_PITCH
        web = web.cut(Part.makeCylinder(STOP_INDEX_D / 2.0, STOP_WEB_T + 2.0,
                                        V(dx, STOP_INDEX_Y, -1.0), V(0, 0, 1)))
    # thick pads that ride in the side slots down to the cavity floor
    for sx in (-1, 1):
        x_out = sx * W2
        x_in = sx * (W2 - STOP_PAD_W)
        web = web.fuse(box(min(x_in, x_out), max(x_in, x_out),
                           STOP_Y0, STOP_Y1, 0, STOP_PAD_T))
    # the aperture itself
    web = web.cut(Part.makeCylinder(hole_d / 2.0, STOP_PAD_T + 2.0,
                                    V(0, 0, -1.0), V(0, 0, 1)))
    return web.removeSplitter()


# ------------------------------------------------------------------ the sliders
stops = []
for i, hole in enumerate(STOP_HOLES, start=1):
    shape = make_stop(hole, i)
    stops.append((i, hole, shape))
    bb = shape.BoundBox
    print(f"  Stop_{i} (hole {hole:.1f}, {i} dot{'s' if i > 1 else ''}): "
          f"vol={shape.Volume:,.0f} mm3  "
          f"faces={len(shape.Faces)}  solids={len(shape.Solids)}  "
          f"bbox {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f}")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)

cols = STOP_LAYOUT_COLS
rows = (len(stops) + cols - 1) // cols
pitch_x = STOP_W + STOP_LAYOUT_GAP
pitch_y = SLIDER_H + STOP_LAYOUT_GAP
x0 = -(cols - 1) * pitch_x / 2.0
y0 = (rows - 1) * pitch_y / 2.0

objs = {}
for i, hole, shape in stops:
    k = i - 1
    col, row = k % cols, k // cols
    obj = doc.addObject("Part::Feature", f"Stop_{i}_d{hole:g}")
    obj.Shape = shape
    obj.Placement.Base = V(x0 + col * pitch_x, y0 - row * pitch_y, 0)
    if getattr(obj, "ViewObject", None):
        obj.ViewObject.ShapeColor = (0.2, 0.2, 0.2)
    objs[i] = obj
doc.recompute()

print(f"  laid out on the bed: {cols} columns x {rows} rows, "
      f"{pitch_x:.1f} x {pitch_y:.1f} mm pitch")
b = Part.makeCompound([o.Shape for o in doc.Objects]).BoundBox
print(f"  batch footprint: {b.XLength:.0f} x {b.YLength:.0f} mm "
      f"(A1 bed is 256 x 256)")
if b.XLength > 250 or b.YLength > 250:
    raise RuntimeError("batch does not fit the bed - reduce STOP_HOLES or the gap")

fcstd = os.path.join(PARTS, "camera_stops.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

# --------------------------------------------------------------------- export
for i, hole, shape in stops:
    idx = objs[i]
    keep = idx.Placement.Base
    idx.Placement.Base = V(0, 0, 0)          # individual files sit on the origin
    stem = f"stop_{i}_d{hole:g}mm"
    for ext in ("stl", "3mf"):
        Mesh.export([idx], os.path.join(EXPORTS, f"{stem}.{ext}"))
    idx.Placement.Base = keep
Mesh.export(list(doc.Objects), os.path.join(EXPORTS, "aperture_stops.3mf"))
Mesh.export(list(doc.Objects), os.path.join(EXPORTS, "aperture_stops.stl"))
print("exports written to", EXPORTS)

# ------------------------------------------------------------------ self-check
print("\n--- geometry check ---")
checks = []


def chk(label, shape, x, y, z, want):
    got = shape.isInside(V(x, y, z), 1e-6, True)
    checks.append((label, got == want, got, want))


for i, hole, shape in stops:
    rh = hole / 2.0
    chk(f"stop {i}: hole open", shape, 0, 0, STOP_WEB_T / 2, False)
    chk(f"stop {i}: web solid right of hole", shape, rh + 1.0, 0, STOP_WEB_T / 2, True)
    chk(f"stop {i}: web solid below hole", shape, 0, -(rh + 1.0), STOP_WEB_T / 2, True)
    chk(f"stop {i}: web solid at the cone edge", shape, 0, -26.0, STOP_WEB_T / 2, True)
    chk(f"stop {i}: nothing beyond the web disc", shape, 10.0, 30.5, STOP_WEB_T / 2, False)
    chk(f"stop {i}: left pad full thickness", shape, -(W2 - 0.5), 0, STOP_PAD_T - 0.1, True)
    chk(f"stop {i}: right pad full thickness", shape, W2 - 0.5, 0, STOP_PAD_T - 0.1, True)
    chk(f"stop {i}: pad is not a plate", shape, W2 - 0.5, 0, STOP_PAD_T + 0.2, False)
    chk(f"stop {i}: pad reaches the floor", shape, W2 - 0.5, STOP_Y0 + 0.4, 1.0, True)
    chk(f"stop {i}: pad stops short of the ledge", shape, W2 - 0.5, STOP_Y1 + 0.5, 1.0, False)
    chk(f"stop {i}: pull tab", shape, 0, STOP_TAB_TOP - 1.0, STOP_WEB_T / 2, True)
    chk(f"stop {i}: tab is narrow", shape, 8.0, STOP_TAB_TOP - 1.0, STOP_WEB_T / 2, False)
    chk(f"stop {i}: tab solid under the dots", shape, 0, 31.0, STOP_WEB_T / 2, True)
    for k in range(i):
        dx = (k - (i - 1) / 2.0) * STOP_INDEX_PITCH
        chk(f"stop {i}: index dot {k + 1}/{i}", shape, dx, STOP_INDEX_Y,
            STOP_WEB_T / 2, False)

bad = 0
for label, ok, got, want in checks:
    if not ok:
        print(f"  [BAD] {label}: inside={got} (want {want})")
    bad += 0 if ok else 1
print(f"{len(checks) - bad}/{len(checks)} checks passed")

# ------------------------------------------------------------ fit in the body
print("\n--- fit in the front body ---")
front = App.openDocument(os.path.join(PARTS, "camera_front_body.FCStd"))
body = [s.Shape for s in front.Objects]
screen = App.openDocument(os.path.join(PARTS, "camera_screen.FCStd"))
body += [s.Shape for s in screen.Objects]
lids = App.openDocument(os.path.join(PARTS, "camera_lids.FCStd"))
body += [s.Shape for s in lids.Objects]

for i, hole, shape in stops:
    s = shape.copy()
    s.translate(V(0, 0, Z_PLACE))
    worst = 0.0
    for other in body:
        o = s.common(other).Volume
        worst = max(worst, o)
    print(f"  [{'ok ' if worst < 0.05 else 'BAD'}] stop {i}: slide-in volume "
          f"{Z_PLACE:.2f}..{Z_PLACE + STOP_PAD_T:.2f} in the {STOP_SLOT_Z:.0f} slot, "
          f"worst overlap {worst:.3f} mm3")
    bad += 0 if worst < 0.05 else 1

for d in (front, screen, lids):
    App.closeDocument(d.Name)

# ---------------------------------------------------------------- the numbers
print("\n--- what the set covers ---")
print("  stop  hole  f/# at z=%.0f  f/# in slot 25  depth of focus  Airy disc"
      % STOP_SLOT_Z)
print("               (screen at %.0f)                 (+- at 0.1 mm)" % STOP_SCREEN_Z)
for i, hole, shape in stops:
    lever = STOP_SCREEN_Z - STOP_SLOT_Z
    n = lever / hole
    n25 = (STOP_SCREEN_Z - 25.0) / hole
    dof = 0.1 * n
    airy = 2.44 * 0.00055 * n * 1000.0            # micrometres at the film plane
    print(f"  {i:>4}  {hole:4.1f}  f/{n:<10.1f}  f/{n25:<11.1f}  "
          f"+-{dof:4.2f} mm      {airy:3.0f} um")
print("  (no slider: the bare Ø59 bore is the wide-open reference)")

print("\nRESULT:", "all good" if bad == 0 else f"{bad} PROBLEM(S)")
