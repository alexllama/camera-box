"""Front plate for a 67.73 mm diameter lens (friction fit).

Print with the spigot up, flange on the bed. Keep the cap/skirt on to hold it
to the tube. The shroud is long enough to slide over the tube for fine focus
tuning, with thick walls for rigidity.

Run:
    exec(open('/home/alex/Work/camera-box/scripts/build_1a_plate_lens67p73.py').read(), globals())
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

DOC_NAME = "camera_front_plate_lens67p73"
V = App.Vector

# ---- fit for 67.73 mm lens barrel -----------------------------------------
LENS_OD = 67.73
FIT = -0.08
BORE_CUT = LENS_OD + FIT

assert BORE_CUT > 0

# ---- shroud for sliding focus tuning --------------------------------------
SHROUD_LEN = 60.0           # length of each side of the shroud
SHROUD_T = 2.0              # thicker walls as requested
SHROUD_CLR = 0.20           # clearance to tube OD for sliding fit (tune if needed)

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

# Bore for the new lens
plate = plate.cut(cyl(BORE_CUT, -1, PLATE_T + PLATE_SPIGOT + 1))
try:
    bore_edges = [e for e in plate.Edges
                  if abs(e.BoundBox.ZMin) < 1e-6 and e.Length > (BORE_CUT * 3.14159 - 2.0)]
    if bore_edges:
        plate = plate.makeChamfer(0.5, bore_edges)
except Exception:
    pass

# optional aperture-stop disc pocket, behind the glass, on the spigot end face
plate = plate.cut(cyl(APERTURE_RECESS_D,
                      PLATE_T + PLATE_SPIGOT - APERTURE_RECESS_DEPTH,
                      PLATE_T + PLATE_SPIGOT))

# outer shroud: long enough to slide over the tube for fine focus tuning
shroud_od = OUT_W + 2 * SHROUD_CLR + 2 * SHROUD_T
shroud_id = OUT_W + 2 * SHROUD_CLR
tube_z0 = PLATE_T
shroud_z1 = tube_z0 + SHROUD_LEN
shroud = box(-shroud_od / 2, shroud_od / 2, -shroud_od / 2, shroud_od / 2,
            0, shroud_z1)
hole = box(-shroud_id / 2, shroud_id / 2, -shroud_id / 2, shroud_id / 2,
           -1, shroud_z1 + 1)
shroud = shroud.cut(hole)
# lead-in chamfer on the rear edge of the shroud
shroud_edges = [e for e in shroud.Edges
                if abs(e.BoundBox.ZMin) > shroud_z1 - 1e-6 and e.Length > 80.0]
if shroud_edges:
    shroud = shroud.makeChamfer(0.5, shroud_edges)
plate = plate.fuse(shroud)
plate = finish(plate, "FrontPlate_Lens67p73")

# -------------------------------------------------------------------- document
if DOC_NAME in [d.Name for d in App.listDocuments().values()]:
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)
obj = doc.addObject("Part::Feature", "FrontPlate_Lens67p73")
obj.Shape = plate
if getattr(obj, "ViewObject", None):
    obj.ViewObject.ShapeColor = (0.13, 0.13, 0.13)
doc.recompute()

fcstd = os.path.join(PARTS, "camera_front_plate_lens67p73.FCStd")
doc.saveAs(fcstd)
print("saved", fcstd)

# --------------------------------------------------------------------- export
for ext in ("stl", "3mf"):
    path = os.path.join(EXPORTS, f"camera_front_plate_lens67p73.{ext}")
    Mesh.export([obj], path)
print("exports written to", EXPORTS)

bb = plate.BoundBox
print(f"Lens OD {LENS_OD:.2f} -> bore cut {BORE_CUT:.3f} (interference {FIT:+.3f} mm)")
print(f"Shroud OD {shroud_od:.2f} ID {shroud_id:.2f} H {SHROUD_LEN:.0f} T {SHROUD_T:.0f}")
print(f"bbox {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f}")
