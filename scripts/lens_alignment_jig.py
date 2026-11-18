"""Lens alignment jig for the 67.73 mm lens plate.

Slide this into the 67.73 mm faceplate's bore from the front (or drop it in with
the plate off the tube) so the lens barrel rests against the front edge of the
jig. That way the lens is square and fully seated to the same depth every time.

Print with the disc face on the bed, no supports.

Run:
    exec(open('/home/alex/Work/camera-box/scripts/lens_alignment_jig.py').read(), globals())
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

DOC_NAME = "lens_alignment_jig_67p73"
V = App.Vector

LENS_OD = 67.73
FIT = -0.08
BORE_CUT = LENS_OD + FIT
JIG_OD = 67.55
JIG_T = 3.0
RIM_W = 8.0
HANDLE_D = 24.0
HANDLE_H = 4.0

def cyl(dia, h, z0, x=0.0, y=0.0):
    return Part.makeCylinder(dia / 2.0, h, V(x, y, z0), V(0, 0, 1))


jig = cyl(JIG_OD, JIG_T, 0)
jig = jig.fuse(cyl(JIG_OD + 2 * RIM_W, JIG_T, 0))
# finger handle
jig = jig.fuse(cyl(HANDLE_D, HANDLE_H, JIG_T, 0, 0))
# center hole for visibility/less material
jig = jig.cut(cyl(30.0, JIG_T + HANDLE_H + 2.0, -1.0))

# chamfer the bore edge of the disc so the lens doesn't hang up
try:
    edges = [e for e in jig.Edges
             if abs(e.BoundBox.ZMin) < 1e-6 and e.Length > (JIG_OD * 3.14159 - 2.0)]
    if edges:
        jig = jig.makeChamfer(0.4, edges)
except Exception:
    pass

jig = jig.removeSplitter()

if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
obj = doc.addObject("Part::Feature", "LensAlignmentJig_67p73")
obj.Shape = jig
if getattr(obj, "ViewObject", None):
    obj.ViewObject.ShapeColor = (0.8, 0.4, 0.0)
doc.recompute()

fcstd = os.path.join(PARTS, "lens_alignment_jig_67p73.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

for ext in ("stl", "3mf"):
    path = os.path.join(EXPORTS, f"lens_alignment_jig_67p73.{ext}")
    Mesh.export([obj], path)
print("exports written to", EXPORTS)
print(f"Jig OD {JIG_OD:.2f} (fits in bore {BORE_CUT:.3f})  rim {JIG_OD + 2 * RIM_W:.1f}  H {JIG_T + HANDLE_H:.1f}")
