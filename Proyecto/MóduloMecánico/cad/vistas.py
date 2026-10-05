"""Onshape-style views ("shaded with edges") of step/ENSAMBLE_modulo.step.

    python vistas.py
Outputs: Recursos/Imágenes/LG_mec_vista_{iso,frontal,superior,lateral}.png and LG_mec_explosionada.png
(1920 x 1080, white background, black B-rep edges). Reads the STEP written by build.py, so the views
always show the same model as the CAD files.
"""
import math
from pathlib import Path

import cadquery as cq
import numpy as np
import pyvista as pv

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
IMG = MOD.parent.parent / "Recursos" / "Imágenes"
STEP = MOD / "step" / "ENSAMBLE_modulo.step"
SIZE = (1920, 1080)

# Onshape-like palette: red body parts, matte black arms, light grey lids and bezels, clear acrylic
COLOR = {"M1": "#C0392B", "M4": "#C0392B", "M3": "#2B2B2E", "M2": "#C9CCD1", "M5": "#C9CCD1",
         "M6": "#C9CCD1", "M7": "#A9D3F0"}
LABEL = {"M1": "M1 Caja central", "M2": "M2 Tapa con asa", "M3": "M3 Brazo", "M4": "M4 Cápsula",
         "M5": "M5 Tapa de cápsula", "M6": "M6 Bisel", "M7": "M7 Ventana acrílica"}
TILT = math.radians(40.0)


def load_parts():
    """[(instance name, part id, located Shape)] from the assembly STEP."""
    assy = cq.Assembly.importStep(str(STEP))
    return [(ch.name, ch.name[:2], ch.obj.moved(ch.loc)) for ch in assy.children]


def explode_offset(name, pid):
    """Static exploded layout: lid up, arms out, capsule parts along their optical axis."""
    if pid == "M1":
        return np.zeros(3)
    if pid == "M2":
        return np.array([0, 0, 90.0])
    s = 1.0 if name.endswith("der") else -1.0
    base = np.array([s * 80.0, 0, 0])
    axis = np.array([s * math.cos(TILT), 0, -math.sin(TILT)])
    along = {"M3": None, "M5": 0.0, "M4": 45.0, "M7": 110.0, "M6": 165.0}[pid]
    return base if along is None else base + along * axis


def to_mesh(shape, shift):
    verts, tris = shape.tessellate(0.05, 0.15)
    pts = np.array([v.toTuple() for v in verts]) + shift
    faces = np.hstack([np.full((len(tris), 1), 3), np.array(tris)]).ravel()
    return pv.PolyData(pts, faces)


def to_edges(shape, shift):
    """Every B-rep edge as a polyline: what Onshape draws in 'shaded with edges'."""
    pts, lines, n = [], [], 0
    for e in shape.Edges():
        L = e.Length()
        k = max(2, min(80, int(L / 1.5) + 2))
        p = [e.positionAt(t).toTuple() for t in np.linspace(0, 1, k)]
        pts.extend(p)
        lines.append([k] + list(range(n, n + k)))
        n += k
    return pv.PolyData(np.array(pts) + shift, lines=np.hstack(lines))


def render(parts, out, view, exploded=False, labels=False):
    pl = pv.Plotter(off_screen=True, window_size=SIZE)
    pl.set_background("white")
    pl.enable_anti_aliasing("ssaa")
    label_pts, label_txt, all_pts = [], [], []
    for name, pid, shp in parts:
        shift = explode_offset(name, pid) if exploded else np.zeros(3)
        glass = pid == "M7"
        mesh = to_mesh(shp, shift)
        all_pts.append(mesh.points)
        pl.add_mesh(mesh, color=COLOR[pid], smooth_shading=True, split_sharp_edges=True,
                    opacity=0.45 if glass else 1.0, specular=0.25, specular_power=20, ambient=0.18, diffuse=0.8)
        pl.add_mesh(to_edges(shp, shift), color="black", line_width=1.6 if not glass else 1.0)
        if labels and not name.endswith("izq"):          # one label per part, on the right-hand instance
            bb = shp.BoundingBox()
            label_pts.append(np.array([bb.center.x, bb.center.y, bb.zmax]) + shift)
            label_txt.append(LABEL[pid])
    if label_pts:
        pl.add_point_labels(np.array(label_pts), label_txt, font_size=22, text_color="black", point_size=1,
                            shape_color="white", shape_opacity=0.85, margin=4, always_visible=True,
                            show_points=False)
    # orthographic camera framed on the projected extents (8 % margin), like Onshape's "zoom to fit"
    pl.enable_parallel_projection()
    dirs = {"iso": (1, -1, 1), "iso_bajo": (1.3, -1, 0.45), "frontal": (0, -1, 0), "superior": (0, 0, 1), "lateral": (1, 0, 0)}
    d = np.array(dirs[view], float)
    d /= np.linalg.norm(d)
    up = np.array((0, 1, 0) if view == "superior" else (0, 0, 1), float)
    right = np.cross(up, d)
    right /= np.linalg.norm(right)
    up = np.cross(d, right)
    pts = np.vstack(all_pts)
    u, v = pts @ right, pts @ up
    centre = right * (u.min() + u.max()) / 2 + up * (v.min() + v.max()) / 2
    pl.camera_position = [tuple(centre + d * 3000), tuple(centre), tuple(up)]
    aspect = SIZE[0] / SIZE[1]
    pl.camera.parallel_scale = 1.08 * max((v.max() - v.min()) / 2, (u.max() - u.min()) / 2 / aspect)
    pl.renderer.ResetCameraClippingRange()
    pl.screenshot(str(out))
    pl.close()
    print("written", out.name)


def main():
    parts = load_parts()
    for v in ("iso", "frontal", "superior", "lateral"):
        render(parts, IMG / f"LG_mec_vista_{v}.png", v)
    # lower viewpoint so the windows, which face down and outwards, are seen from the front
    render(parts, IMG / "LG_mec_explosionada.png", "iso_bajo", exploded=True, labels=True)


if __name__ == "__main__":
    main()
