"""Render the README images from the actual STL meshes.

Uses VTK offscreen rendering, so no GUI or external renderer is needed.

Outputs:
    renders/exploded.png   exploded assembly of the current build
    renders/parts.png      sheet of the printed parts in the current build

Run:
    python3 scripts/render_readme.py
"""

import os
import tempfile

from PIL import Image, ImageDraw, ImageFont
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingOpenGL2 import vtkEGLRenderWindow
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkWindowToImageFilter,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPORTS = os.path.join(ROOT, "exports")
RENDERS = os.path.join(ROOT, "renders")
os.makedirs(RENDERS, exist_ok=True)

FONT_REG = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

# Only parts in the current build. Legacy carrier, old 59.05 mm plate and the
# test parts are deliberately excluded.
PARTS = [
    ("camera_front_plate_lens67p73.stl", "Front plate 67.73", (0.17, 0.19, 0.22)),
    ("camera_front_tube.stl", "Front tube", (0.42, 0.46, 0.51)),
    ("camera_rear_body.stl", "Rear body", (0.48, 0.52, 0.56)),
    ("camera_front_lid.stl", "Front lid", (0.72, 0.75, 0.78)),
    ("camera_rear_lid.stl", "Rear lid", (0.65, 0.69, 0.73)),
    ("sheet_frame_front.stl", "Screen frame front", (0.80, 0.75, 0.66)),
    ("sheet_frame_back.stl", "Screen frame back", (0.74, 0.69, 0.60)),
    ("stop_1_d10mm.stl", "Stop d10", (0.86, 0.47, 0.22)),
    ("stop_2_d7mm.stl", "Stop d7", (0.86, 0.47, 0.22)),
    ("stop_3_d5mm.stl", "Stop d5", (0.86, 0.47, 0.22)),
    ("stop_4_d3.6mm.stl", "Stop d3.6", (0.86, 0.47, 0.22)),
    ("stop_5_d2.5mm.stl", "Stop d2.5", (0.86, 0.47, 0.22)),
    ("stop_6_d1.8mm.stl", "Stop d1.8", (0.86, 0.47, 0.22)),
    ("camera_phone_cap.stl", "Phone cap", (0.25, 0.36, 0.47)),
]

# Exploded-view placement: optical axis is z, so spread parts along z and
# lift the two long lids clear in +y.
EXPLODE = {
    "camera_front_plate_lens67p73.stl": (0, 0, 0),
    "stop_1_d10mm.stl": (0, 0, 75),
    "sheet_frame_front.stl": (0, 0, 85),
    "sheet_frame_back.stl": (0, 0, 95),
    "camera_front_tube.stl": (0, 0, 105),
    "camera_front_lid.stl": (0, 62, 0),
    "camera_rear_body.stl": (0, 0, 220),
    "camera_rear_lid.stl": (0, 62, 115),
    "camera_phone_cap.stl": (0, 0, 355),
}


def make_actor(path, color, opacity=1.0):
    reader = vtkSTLReader()
    reader.SetFileName(path)
    reader.Update()
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    prop = actor.GetProperty()
    prop.SetColor(*color)
    prop.SetAmbient(0.32)
    prop.SetDiffuse(0.68)
    prop.SetSpecular(0.10)
    prop.SetSpecularPower(18)
    if opacity < 1.0:
        prop.SetOpacity(opacity)
    return actor


def make_lights(renderer, cx, cy, cz, span):
    renderer.SetAutomaticLightCreation(False)
    key = vtkLight()
    key.SetLightTypeToSceneLight()
    key.SetPosition(cx - span, cy - 1.2 * span, cz + 1.6 * span)
    key.SetFocalPoint(cx, cy, cz)
    key.SetIntensity(0.78)
    key.SetColor(1.0, 1.0, 1.0)
    fill = vtkLight()
    fill.SetLightTypeToSceneLight()
    fill.SetPosition(cx + 1.2 * span, cy + 0.8 * span, cz + 0.5 * span)
    fill.SetFocalPoint(cx, cy, cz)
    fill.SetIntensity(0.34)
    fill.SetColor(0.89, 0.93, 1.0)
    renderer.AddLight(key)
    renderer.AddLight(fill)


def render_png(actors, width, height, path, azimuth="iso", margin=1.08):
    renderer = vtkRenderer()
    renderer.SetGradientBackground(True)
    renderer.SetBackground(0.97, 0.98, 0.99)
    renderer.SetBackground2(0.84, 0.87, 0.91)

    for actor in actors:
        renderer.AddActor(actor)

    bounds = [float("inf"), float("-inf")] * 3
    for actor in actors:
        b = actor.GetBounds()
        for i in range(3):
            bounds[2 * i] = min(bounds[2 * i], b[2 * i])
            bounds[2 * i + 1] = max(bounds[2 * i + 1], b[2 * i + 1])
    cx = (bounds[0] + bounds[1]) / 2
    cy = (bounds[2] + bounds[3]) / 2
    cz = (bounds[4] + bounds[5]) / 2
    span = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
    make_lights(renderer, cx, cy, cz, span)

    camera = vtkCamera()
    camera.SetFocalPoint(cx, cy, cz)
    if azimuth == "iso":
        camera.SetPosition(cx + 1.0 * span, cy - 1.25 * span, cz + 0.85 * span)
    elif azimuth == "low":
        camera.SetPosition(cx + 1.15 * span, cy - 1.0 * span, cz + 0.55 * span)
    camera.SetViewUp(0, 0, 1)
    camera.ParallelProjectionOn()
    renderer.SetActiveCamera(camera)

    # The default X window renders but its pixel readback segfaults here;
    # EGL offscreen readback works and needs no display.
    window = vtkEGLRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetSize(width, height)
    window.AddRenderer(renderer)
    renderer.ResetCamera()
    camera.SetParallelScale(camera.GetParallelScale() * margin)
    window.Render()

    capture = vtkWindowToImageFilter()
    capture.SetInput(window)
    capture.SetInputBufferTypeToRGB()
    capture.ReadFrontBufferOff()
    capture.Update()
    writer = vtkPNGWriter()
    writer.SetFileName(path)
    writer.SetInputConnection(capture.GetOutputPort())
    writer.Write()
    window.Finalize()


def render_exploded():
    actors = []
    for filename, _label, color in PARTS:
        actor = make_actor(os.path.join(EXPORTS, filename), color)
        if filename in EXPLODE:
            actor.SetPosition(*EXPLODE[filename])
        actors.append(actor)

    out = os.path.join(RENDERS, "exploded.png")
    render_png(actors, 1200, 1700, out, azimuth="iso", margin=0.65)
    print("wrote", out)


def render_parts_sheet():
    cell_w, cell_h = 380, 310
    cols = 4
    rows = (len(PARTS) + cols - 1) // cols
    header = 86
    canvas_h = header + rows * cell_h + 16
    canvas = Image.new("RGB", (cols * cell_w + 16, canvas_h), (245, 247, 249))
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(FONT_BOLD, 28)
    sub_font = ImageFont.truetype(FONT_REG, 16)
    name_font = ImageFont.truetype(FONT_BOLD, 17)
    file_font = ImageFont.truetype(FONT_REG, 12)
    draw.text((20, 16), "Printed parts - current build", font=title_font,
              fill=(31, 36, 43))
    draw.text((22, 54), "Rendered from exports/*.stl - sizes differ, not to scale",
              font=sub_font, fill=(97, 107, 120))

    for idx, (filename, label, color) in enumerate(PARTS):
        col, row = idx % cols, idx // cols
        x0 = 8 + col * cell_w
        y0 = header + row * cell_h

        actor = make_actor(os.path.join(EXPORTS, filename), color)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            render_png([actor], cell_w - 12, cell_h - 64, tmp_path,
                       azimuth="iso", margin=1.14)
            img = Image.open(tmp_path).convert("RGB")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        canvas.paste(img, (x0 + 6, y0 + 4))
        draw.rectangle((x0 + 6, y0 + 4, x0 + cell_w - 6, y0 + cell_h - 60),
                       outline=(212, 217, 224), width=1)
        draw.text((x0 + 14, y0 + cell_h - 54), label, font=name_font,
                  fill=(36, 41, 48))
        draw.text((x0 + 14, y0 + cell_h - 31), filename, font=file_font,
                  fill=(107, 117, 128))

    out = os.path.join(RENDERS, "parts.png")
    canvas.save(out)
    print("wrote", out)


if __name__ == "__main__":
    render_exploded()
    render_parts_sheet()
