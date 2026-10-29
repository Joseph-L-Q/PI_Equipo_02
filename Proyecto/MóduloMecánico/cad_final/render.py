"""Onshape-style off-screen renders (shaded with black B-rep edges), adapted from cad/vistas.py.

render(items, out, view): items = [(cq Shape or Workplane, colour, opacity, draw_edges, label or None)].
"""
import numpy as np
import pyvista as pv

SIZE = (1920, 1080)
DIRS = {"iso": (1, -1, 1), "iso_alto": (0.9, -1.1, 1.6), "iso_bajo": (0.7, -1, -1.9), "superior": (0, 0, 1), "frontal": (0, -1, 0),
        "lateral": (1, 0, 0)}


def _shape(obj):
    return obj.val() if hasattr(obj, "val") else obj


def to_mesh(shape):
    verts, tris = shape.tessellate(0.05, 0.15)
    pts = np.array([v.toTuple() for v in verts])
    faces = np.hstack([np.full((len(tris), 1), 3), np.array(tris)]).ravel()
    return pv.PolyData(pts, faces)


def to_edges(shape):
    """Every B-rep edge as a polyline: what Onshape draws in 'shaded with edges'."""
    pts, lines, n = [], [], 0
    for e in shape.Edges():
        k = max(2, min(80, int(e.Length() / 1.5) + 2))
        pts.extend(e.positionAt(t).toTuple() for t in np.linspace(0, 1, k))
        lines.append([k] + list(range(n, n + k)))
        n += k
    return pv.PolyData(np.array(pts), lines=np.hstack(lines))


def render(items, out, view="iso", title=None):
    pl = pv.Plotter(off_screen=True, window_size=SIZE)
    pl.set_background("white")
    pl.enable_anti_aliasing("ssaa")
    all_pts, lab_pts, lab_txt = [], [], []
    for obj, color, opacity, edges, label in items:
        shp = _shape(obj)
        mesh = to_mesh(shp)
        all_pts.append(mesh.points)
        pl.add_mesh(mesh, color=color, smooth_shading=True, split_sharp_edges=True, opacity=opacity,
                    specular=0.25, specular_power=20, ambient=0.18, diffuse=0.8)
        if edges:
            pl.add_mesh(to_edges(shp), color="black", line_width=1.4 if opacity > 0.6 else 0.8,
                        opacity=1.0 if opacity > 0.6 else 0.5)
        if label:
            bb = shp.BoundingBox()
            lab_pts.append((bb.center.x, bb.center.y, bb.zmax))
            lab_txt.append(label)
    if lab_pts:
        pl.add_point_labels(np.array(lab_pts), lab_txt, font_size=20, text_color="black", point_size=1,
                            shape_color="white", shape_opacity=0.85, margin=3, always_visible=True,
                            show_points=False)
    if title:
        pl.add_text(title, position="upper_left", font_size=14, color="black")
    pl.enable_parallel_projection()
    d = np.array(DIRS[view], float)
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
    pl.camera.parallel_scale = 1.1 * max((v.max() - v.min()) / 2, (u.max() - u.min()) / 2 / aspect)
    pl.renderer.ResetCameraClippingRange()
    pl.screenshot(str(out))
    pl.close()
    print("written", out)
