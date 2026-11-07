"""Whole-system load diagram: ISO render of buoy + umbilical + node (+ lantern, references) with the force arrows at scale and a numbered load path.

    python cargas_conjunto.py            -> docs/CARGAS_CONJUNTO.md + docs/CARGAS_CONJUNTO.pdf (+ docs/cargas_conjunto_general.png)

Geometry: salida/boya_pet/ENSAMBLE_boya_pet.step (buoy, its own frame, keel z = 0) and salida/prototipos/P2_robusto/ensamble_simple_D200.step
(node P2 with the 200 mm lantern ring), the node hung `CABO` mm under the keel as in sistema.json (cabo_largo). Both are read-only inputs.
Forces: weights from salida/boya_pet/resultados.json and P2_robusto/resultados.json, current as in simscale_run.py (1153 Pa on the capsule front),
wave 200 N and handling 150 N as in the SimScale cases. Arrow length = force x SCALE mm per N (arrows under MIN_ARROW mm are drawn at MIN_ARROW and flagged).
"""
import json
import math
import os
import sys
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")

import numpy as np                                      # noqa: E402

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
DOCS = MOD / "docs"
BUOY_STEP = MOD / "salida" / "boya_pet" / "ENSAMBLE_boya_pet.step"
NODE_STEP = MOD / "salida" / "prototipos" / "P2_robusto" / "ensamble_simple_D200.step"
CABO = 560.0
SCALE = 2.0          # mm of arrow per N
MIN_ARROW = 22.0
G = 9.81


def meshes(step, tol=0.6):
    import cadquery as cq
    import pyvista as pv
    sh = cq.importers.importStep(str(step)).val()
    out = []
    for s in sh.Solids():
        v, tri = s.tessellate(tol, 0.4)
        if tri:
            out.append(pv.PolyData(np.array([(p.x, p.y, p.z) for p in v]), np.hstack([[3, *t] for t in tri])))
    return out, sh.BoundingBox()


def numbers():
    import capsula as CP
    import fem
    b = json.loads((MOD / "salida" / "boya_pet" / "resultados.json").read_text(encoding="utf-8"))
    n = json.loads((MOD / "salida" / "prototipos" / "P2_robusto" / "resultados.json").read_text(encoding="utf-8"))
    cd = CP.cap_dims()
    r = cd[1] / 2
    area = math.pi * r * r * 1e-6
    q = 0.5 * 1025.0 * 1.5 ** 2
    return dict(w_buoy=b["masa_g"] * 1e-3 * G, buoyancy_max=b["empuje_botellas_g"] * 1e-3 * G, calado=b["hidro"]["calado"],
                w_node_water=n["peso"]["100"]["aparente_g"] * 1e-3 * G, drag=q * area, area_cm2=area * 1e4, q=q, front=fem.geometry()["front"])


def arrow(pv, start, d, force, color):
    d = np.asarray(d, float) / np.linalg.norm(d)
    length = max(force * SCALE, MIN_ARROW)
    return pv.Arrow(start=np.asarray(start, float), direction=d, scale=length, tip_length=min(0.35, 18.0 / length), tip_radius=min(0.09, 6.0 / length), shaft_radius=min(0.035, 2.2 / length)), \
        np.asarray(start, float) + d * length


def main():
    import pyvista as pv
    N = numbers()
    bm, bb = meshes(BUOY_STEP)
    nm, nb = meshes(NODE_STEP)
    dz = -CABO - nb.zmax                                  # node top CABO mm under the keel
    nm = [m.translate((0, 0, dz), inplace=False) for m in nm]
    pl = pv.Plotter(off_screen=True, window_size=(1500, 2000))
    pl.set_background("white")
    for m in bm:
        pl.add_mesh(m, color="#8fb996", opacity=0.6)
    for m in nm:
        pl.add_mesh(m, color="#8aa0b8", opacity=0.9)
    zw = N["calado"]
    pl.add_mesh(pv.Plane(center=(0, 0, zw), direction=(0, 0, 1), i_size=900, j_size=900), color="#4aa3df", opacity=0.18)
    cx = 0.0
    # references: cabo C1 and umbilical U1
    pl.add_mesh(pv.Line((0, 0, 0), (0, 0, -CABO)), color="#333333", line_width=4)
    t = np.linspace(0, 1, 40)
    umb = np.c_[60 + 140 * np.sin(math.pi * t), -40 - 60 * t, 20 - (CABO + 120) * t]
    pl.add_mesh(pv.Spline(umb, 80).tube(radius=3.5), color="#e07b00")
    labels, pts = [], []
    # force arrows (name, start, direction, N, color, number)
    front = np.array(N["front"], float) + np.array([0, 0, dz])
    zt = bb.zmax
    arrows = [
        (1, "Golpe de ola sobre el panel", (0, -150, zt - 25), (0, 1, 0), 200.0, "#d62728"),
        (2, "Peso de la boya", (0, -200, 140.0), (0, 0, -1), N["w_buoy"], "#7f4f24"),
        (3, "Empuje de las botellas", (300, 0, 0.0), (0, 0, 1), N["w_buoy"] + N["w_node_water"], "#1f77b4"),
        (4, "Tirón del cabo (peso del nodo en el agua)", (-300, 0, 0.0), (0, 0, -1), N["w_node_water"], "#9467bd"),
        (5, "Corriente de 1.5 m/s sobre la cápsula", tuple(front + np.array([60, 0, 0])), (-1, 0, 0), N["drag"], "#ff7f0e"),
        (6, "Izado a mano 150 N (caso de diseño de la cápsula)", tuple(front + np.array([0, 0, 190])), (0, 0, -1), 150.0, "#2ca02c"),
    ]
    flagged = []
    for num, name, s0, d, f, col in arrows:
        a, tip = arrow(pv, s0, d, f, col)
        pl.add_mesh(a, color=col)
        if f * SCALE < MIN_ARROW:
            flagged.append(num)
        labels.append(str(num))
        pts.append(tip + np.array([0, 0, 18]))
    pl.add_point_labels(np.array(pts), labels, font_size=34, text_color="black", shape="rounded_rect", shape_color="white", shape_opacity=1.0,
                        always_visible=True, point_size=0, show_points=False)
    shots = {}
    for tag, focus, dist, size in (("general", (0, 0, -620), 3700, (1500, 2000)), ("boya", (0, 0, 120), 760, (1500, 1200)),
                                   ("nodo", tuple(front + np.array([-120, 0, 60])), 900, (1500, 1200))):
        pl.window_size = size
        f = np.array(focus, float)
        pl.camera_position = [tuple(f + dist * np.array([1, -1, 0.7]) / np.linalg.norm([1, -1, 0.7])), tuple(f), (0, 0, 1)]
        pl.reset_camera_clipping_range()
        pl.render()
        f_png = DOCS / f"cargas_conjunto_{tag}.png"
        pl.screenshot(str(f_png))
        shots[tag] = f_png.name
    pl.close()
    rows = "\n".join(f"| {n_} | {nm_} | {f:.1f} N | {d} |" for n_, nm_, _, d, f, _ in
                     [(a[0], a[1], a[2], {(0, 1, 0): "horizontal, +Y", (0, 0, -1): "hacia abajo", (0, 0, 1): "hacia arriba", (-1, 0, 0): "horizontal, −X"}[a[3]], a[4], a[5]) for a in arrows])
    md = f"""# Cargas sobre el conjunto boya + nodo sumergido

Fecha: {__import__('time').strftime('%d/%m/%Y')}. Hecho por `cad_final/cargas_conjunto.py` con las piezas actuales (boya y nodo P2). Las flechas están a escala: **2 mm de flecha = 1 N** (la misma escala en las tres vistas)
(las que serían menores de {MIN_ARROW:.0f} mm se dibujan de {MIN_ARROW:.0f} mm para que se vean: {', '.join(str(i) for i in flagged) or 'ninguna'}; su valor real está en la tabla).
Verde = boya, azul = nodo sumergido con la linterna, línea negra = cabo, tubo naranja = umbilical (son referencias, no se calculan). Las flechas 2, 3 y 4 se dibujan al costado de la boya para que se vean; en la realidad actúan en el centro. El plano azul es la superficie del agua.

![Vista general](cargas_conjunto_general.png)

![Boya, vista cercana](cargas_conjunto_boya.png)

![Nodo, vista cercana](cargas_conjunto_nodo.png)

| N.º | Carga | Valor | Dirección |
|---|---|---|---|
{rows}

## Camino de la carga (qué pieza la lleva y por dónde pasa)

1. **Golpe de ola (1).** Pega en el panel solar, que hace de vela. Del panel pasa a las **4 columnas Ø12** de la cubierta, de ahí a las **barras de la cubierta** y a los **4 tornillos M3** que la unen al casco. Es la carga más peligrosa de la boya: en `docs/resultados` está el cálculo (cubierta, caso «lateral»).
2. **Peso de la boya (2)** ({N['w_buoy']:.1f} N, {N['w_buoy'] / G * 1000:.0f} g con la electrónica). La caja seca lo apoya en 4 pilares de la cubierta; la cubierta lo pasa por los 4 tornillos M3 al casco.
3. **Empuje de las botellas (3).** El agua empuja las botellas hacia arriba con la misma fuerza del peso de la boya más lo que cuelga del cabo ({N['w_buoy'] + N['w_node_water']:.1f} N, calado {N['calado']:.0f} mm). Las botellas lo pasan a las costillas del casco. Si se hundiera del todo, el empuje máximo disponible es {N['buoyancy_max']:.0f} N.
4. **Tirón del cabo (4).** El nodo pesa unos {N['w_node_water'] / G * 1000:.0f} g dentro del agua (lastre ajustado a 0.2–0.5 kgf). Ese peso baja por el cabo y tira del **parche de amarre del fondo del casco** (quilla).
5. **Corriente (5).** Con 1.5 m/s la presión es {N['q']:.0f} Pa sobre el frente de la cápsula ({N['area_cm2']:.0f} cm²): **{N['drag']:.1f} N** hacia atrás. Pasa de la tapa de la cápsula al **pie en silla**, de ahí al **riel con gancho** y, por la C del gancho, al **aro** del que cuelga todo. La carga inclina un poco el cabo (no se dibuja).
6. **Izado a mano (6).** Es el caso de diseño de la cápsula y el riel: 150 N hacia abajo en el frente de la cápsula, mucho mayor que cualquier carga del agua. Se calcula en SimScale para el riel (M3s), el pie (M5s) y la caja (M1s).

La flotación y la estabilidad de la boya son analíticas (`docs/BOYA.md`); esto solo muestra de dónde viene cada carga que se usó en las simulaciones.
"""
    out = DOCS / "CARGAS_CONJUNTO.md"
    out.write_text(md, encoding="utf-8")
    import entrega_pdf
    entrega_pdf.main(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
