"""Test ring for a 67.73 mm lens barrel.

Print this by itself to check the friction fit before printing the full faceplate.
Measure the barrel with calipers (the smooth part that goes into the spigot),
and tweak FIT if needed.

Suggested order:
    FIT = -0.10  # start (tight but pressable)
    FIT = -0.08  # if too tight to press in by hand
    FIT = -0.12  # if too loose / wobbles

Run:
    exec(open('/home/alex/Work/camera-box/scripts/test_lens_ring.py').read(), globals())
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

DOC_NAME = "lens_ring_test_67p73"
V = App.Vector

LENS_OD = 67.73
FIT = -0.08        # interference: negative = bore smaller than barrel
BORE_CUT = LENS_OD + FIT
RING_OD = 76.0
RING_H = 8.0

assert BORE_CUT > 0, "BORE_CUT must be positive"

def cyl(dia, h, z0, x=0.0, y=0.0):
    return Part.makeCylinder(dia / 2.0, h, V(x, y, z0), V(0, 0, 1))


ring = cyl(RING_OD, RING_H, 0)
ring = ring.cut(cyl(BORE_CUT, RING_H + 2.0, -1.0))
# lead-in on the bottom face so it presses in straight
try:
    edges = [e for e in ring.Edges
             if abs(e.BoundBox.ZMin) < 1e-6 and e.Length > (BORE_CUT * 3.14159 - 2.0)]
    if edges:
        ring = ring.makeChamfer(0.6, edges)
except Exception:
    pass

ring = ring.removeSplitter()

if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
obj = doc.addObject("Part::Feature", "LensRingTest_67p73")
obj.Shape = ring
if getattr(obj, "ViewObject", None):
    obj.ViewObject.ShapeColor = (0.15, 0.15, 0.15)
doc.recompute()

fcstd = os.path.join(PARTS, "lens_ring_test_67p73.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

for ext in ("stl", "3mf"):
    path = os.path.join(EXPORTS, f"lens_ring_test_67p73.{ext}")
    Mesh.export([obj], path)
print("exports written to", EXPORTS)
print(f"Lens OD {LENS_OD:.2f} -> bore {BORE_CUT:.3f} (FIT {FIT:+.3f})  ring OD {RING_OD:.0f} x H {RING_H:.0f}")
