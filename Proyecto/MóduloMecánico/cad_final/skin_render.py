"""Presentation renders of the SKIN on its node: perspective camera, soft lights, ambient occlusion, no B-rep edges
(render.py stays the Onshape-style technical one).

    python skin_render.py [P2_robusto] [concha]

Reads the node assembly (ensamble_simple_D200.step, solids named by skin.by_volume) and salida/skin/<proto>/<tema>/
SKIN_<tema>.step. Writes render_iso.png, render_frente.png and render_detalle.png next to the skin.
"""
import sys

import numpy as np
import pyvista as pv
import cadquery as cq

import skin as S

SIZE = (2400, 1600)
SKIN_RGB = "#8c9196"           # PETG grey (the print colour)
NODE_RGB = "#e9e6df"           # the node in a warm off-white so the grey skin reads on top of it
BG = ("#f4f6f8", "#c9d1d9")    # gradient, top to bottom
SHOW = ("M1s_caja_cuerpo", "M2_caja_tapa", "M3s_riel_gancho", "M3t_tapa_bolsillo", "M4_capsula_cuerpo",
        "M5s_capsula_tapa_pie", "M6_capsula_bisel", "REF_M7_capsula_ventana")


def mesh(shape, tol=0.04):
    verts, tris = shape.tessellate(tol, 0.12)
    pts = np.array([v.toTuple() for v in verts])
    return pv.PolyData(pts, np.hstack([np.full((len(tris), 1), 3), np.array(tris)]).ravel())


def shot(meshes, out, eye, focus, view_up=(0, 0, 1), angle=26.0):
    pl = pv.Plotter(off_screen=True, window_size=SIZE, lighting="none")
    pl.set_background(BG[0], top=BG[0])
    pl.set_background(BG[1], top=BG[0])
    for m, rgb, kw in meshes:
        pl.add_mesh(m, color=rgb, smooth_shading=True, split_sharp_edges=True, feature_angle=35, **kw)
    key = pv.Light(position=(400, -700, 900), focal_point=focus, intensity=0.85, light_type="scene light")
    key.positional = False
    fill = pv.Light(position=(-700, -200, 300), focal_point=focus, intensity=0.35, light_type="scene light")
    rim = pv.Light(position=(-200, 800, 500), focal_point=focus, intensity=0.45, light_type="scene light")
    head = pv.Light(intensity=0.18, light_type="headlight")
    for lt in (key, fill, rim, head):
        pl.add_light(lt)
    pl.enable_anti_aliasing("ssaa")
    try:
        pl.enable_ssao(radius=6.0, bias=0.3, kernel_size=128, blur=True)
    except Exception:                                   # older VTK: no SSAO, the lights alone still read
        pass
    pl.camera.position, pl.camera.focal_point, pl.camera.up = eye, focus, view_up
    pl.camera.view_angle = angle
    pl.renderer.ResetCameraClippingRange()
    pl.screenshot(str(out))
    pl.close()
    print("written", out)


def main(proto="P2_robusto", theme="concha"):
    parts = S.by_volume(proto)
    out = S.MOD / "salida" / "skin" / proto / theme
    skin = cq.importers.importStep(str(out / f"SKIN_{theme}.step")).val()
    sk = dict(specular=0.35, specular_power=28, ambient=0.12, diffuse=0.85)
    nd = dict(specular=0.15, specular_power=10, ambient=0.16, diffuse=0.85)
    node = [(mesh(v), NODE_RGB, nd) for k, v in parts.items() if k.startswith(SHOW)]
    items = node + [(mesh(skin, 0.02), SKIN_RGB, sk)]
    b = skin.BoundingBox()
    top = b.zmax
    allb = cq.Compound.makeCompound([v for k, v in parts.items() if k.startswith(SHOW)]).BoundingBox()
    mid = ((allb.xmin + allb.xmax) / 2, (allb.ymin + allb.ymax) / 2, (allb.zmin + allb.zmax) / 2)
    r = max(allb.xlen, allb.ylen, allb.zlen)
    shot(items, out / "render_iso.png", eye=(mid[0] - 1.6 * r, mid[1] - 1.7 * r, mid[2] + 1.7 * r), focus=mid, angle=18.0)
    shot(items, out / "render_frente.png", eye=(mid[0], mid[1] - 2.4 * r, mid[2] + 1.25 * r), focus=mid, angle=19.0)
    # detail: the shell fan, low and close, from the front-right, framed on the front half of the lid
    hx, hy = 0.0, -20.0
    shot(items, out / "render_detalle.png", eye=(hx + 95, hy - 150, top + 85), focus=(hx - 5, hy - 18, top - 3),
         angle=30.0)


if __name__ == "__main__":
    main(*sys.argv[1:])
