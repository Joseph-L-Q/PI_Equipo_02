"""Engine of guia_piezas.py: STEP loading, hole detection, off-screen rendering with numbered markers, A4 sheets.

Frames: every piece is read in the frame of its STEP file (the same one salida/boya_pet and salida/prototipos use).
"""
import math
import textwrap

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pyvista as pv  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402
from OCP.BRepAdaptor import BRepAdaptor_Surface  # noqa: E402

pv.OFF_SCREEN = True

CATS = {
    "union": ("#1f5fbf", "tornillo / unión"),
    "cable": ("#e07b00", "cable"),
    "sello": ("#c0272d", "sello / agua"),
    "forma": ("#2e8b57", "forma / ahorro de material"),
    "ajuste": ("#7d3cb5", "alineación / ajuste"),
    "mont": ("#555555", "montaje de piezas internas"),
}
VW, VH = 1500, 1150


# ----------------------------------------------------------------------------- geometry
def load(path):
    shp = cq.importers.importStep(str(path))
    sol = shp.val()
    v, t = sol.tessellate(0.12, 0.3)
    V = np.array([x.toTuple() for x in v])
    F = np.hstack([[3, *x] for x in t])
    return shp, sol, pv.PolyData(V, F).clean(tolerance=1e-5)


def _axis_letter(a):
    for i, ch in enumerate("xyz"):
        if abs(a[i]) > 0.995:
            return ch
    return "d"


def hole_instances(shp, sol):
    """Concave (hole-like) cylinder faces, merged per coaxial line and axial segment -> list of dicts."""
    raw = []
    for fc in shp.faces().vals():
        if fc.geomType() != "CYLINDER":
            continue
        cy = BRepAdaptor_Surface(fc.wrapped).Cylinder()
        r = cy.Radius()
        ax = cy.Axis()
        d, loc = ax.Direction(), ax.Location()
        a = np.array([d.X(), d.Y(), d.Z()])
        a = a * (1.0 if a[int(np.argmax(abs(a)))] > 0 else -1.0)
        p0 = np.array([loc.X(), loc.Y(), loc.Z()])
        verts = np.array([v.toTuple() for v in fc.Vertices()])
        rad = verts[0] - p0
        rad -= a * np.dot(rad, a)
        if np.linalg.norm(rad) < 1e-6:
            continue
        ru = rad / np.linalg.norm(rad)
        s = (verts - p0) @ a
        bb = fc.BoundingBox()
        bc = np.array([bb.center.x, bb.center.y, bb.center.z])
        probe = p0 + a * np.dot(bc - p0, a) + ru * r - ru * 0.4
        if sol.isInside(cq.Vector(*probe)):
            continue                                              # material on the axis side: a post / a convex face
        raw.append(dict(D=round(2 * r, 2), a=a, p0=p0, s0=float(s.min()), s1=float(s.max())))
    groups = []
    for h in raw:
        for g in groups:
            if abs(g["D"] - h["D"]) < 0.01 and abs(abs(g["a"] @ h["a"]) - 1) < 1e-3:
                dp = h["p0"] - g["p0"]
                dp -= g["a"] * np.dot(dp, g["a"])
                if np.linalg.norm(dp) < 0.3:
                    sh = float(np.dot(h["p0"] - g["p0"], g["a"]))
                    g["segs"].append((h["s0"] + sh, h["s1"] + sh))
                    break
        else:
            groups.append(dict(D=h["D"], a=h["a"], p0=h["p0"], segs=[(h["s0"], h["s1"])]))
    out = []
    for g in groups:
        segs = sorted(g["segs"])
        merged = [list(segs[0])]
        for a0, a1 in segs[1:]:
            if a0 <= merged[-1][1] + 0.6:
                merged[-1][1] = max(merged[-1][1], a1)
            else:
                merged.append([a0, a1])
        for a0, a1 in merged:
            mid = (a0 + a1) / 2
            out.append(dict(D=g["D"], a=g["a"], ax=_axis_letter(g["a"]), ctr=g["p0"] + g["a"] * mid, len=a1 - a0))
    out.sort(key=lambda h: (h["D"], h["ax"], round(h["ctr"][0]), round(h["ctr"][1]), round(h["ctr"][2])))
    return out


def match(h, spec):
    """spec: D (value or (lo,hi)), ax, x/y/z ranges (lo,hi) on the centre, len (lo,hi), ax_in (set of letters)."""
    D = spec.get("D")
    if D is not None:
        lo, hi = (D - 0.06, D + 0.06) if np.isscalar(D) else D
        if not lo <= h["D"] <= hi:
            return False
    if "ax" in spec and h["ax"] not in spec["ax"]:
        return False
    for i, k in enumerate("xyz"):
        if k in spec and not spec[k][0] <= h["ctr"][i] <= spec[k][1]:
            return False
    if "len" in spec and not spec["len"][0] <= h["len"] <= spec["len"][1]:
        return False
    return True


# ----------------------------------------------------------------------------- rendering
def basis(az, el):
    a, e = math.radians(az), math.radians(el)
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    up0 = np.array([0.0, 0.0, 1.0]) if abs(el) < 80 else np.array([0.0, 1.0, 0.0]) * (1 if el > 0 else -1)
    right = np.cross(up0, d)
    right /= np.linalg.norm(right)
    up = np.cross(d, right)
    return d, right, up


class View:
    """One parallel-projection view: image, depth buffer and the 3D -> pixel map."""

    def __init__(self, mesh, az, el, zoom_box=None):
        self.d, self.right, self.up = basis(az, el)
        pts = mesh.points if zoom_box is None else zoom_box
        pr, pu = pts @ self.right, pts @ self.up
        self.cx = (pr.min() + pr.max()) / 2
        self.cy = (pu.min() + pu.max()) / 2
        wr, wu = pr.max() - pr.min(), pu.max() - pu.min()
        self.S = max(wu / 2, wr / 2 * VH / VW) * 1.07                      # half height in mm
        self.k = (VH / 2) / self.S                                         # px per mm
        c3 = self.right * self.cx + self.up * self.cy
        R = float(np.linalg.norm(mesh.bounds[1::2]) + np.linalg.norm(mesh.bounds[0::2])) * 2
        self.cam = c3 + self.d * R
        p = pv.Plotter(off_screen=True, window_size=(VW, VH))
        p.set_background("white")
        p.add_mesh(mesh, color="#cfd6df", smooth_shading=False, specular=0.15, ambient=0.35, diffuse=0.75)
        p.add_mesh(mesh.extract_feature_edges(35, boundary_edges=False, non_manifold_edges=False), color="#4a5560", line_width=1.0)
        p.enable_parallel_projection()
        p.camera_position = [tuple(self.cam), tuple(c3), tuple(self.up)]
        p.camera.parallel_scale = self.S
        p.camera.clipping_range = (R * 0.2, R * 3)
        self.img = p.screenshot(return_img=True)
        dep = p.get_image_depth(fill_value=np.nan)
        p.close()
        self.depth = -dep

    def px(self, P):
        P = np.asarray(P, float)
        return np.array([VW / 2 + ((P @ self.right) - self.cx) * self.k, VH / 2 - ((P @ self.up) - self.cy) * self.k])

    def depth_of(self, P):
        return float(np.dot(self.cam - np.asarray(P, float), self.d))

    def visible(self, P, tol):
        x, y = self.px(P)
        xi, yi = int(round(x)), int(round(y))
        if not (0 <= xi < VW and 0 <= yi < VH):
            return False
        win = self.depth[max(0, yi - 1):yi + 2, max(0, xi - 1):xi + 2]
        best = np.nan if np.all(np.isnan(win)) else np.nanmin(win)
        if np.isnan(best):
            return True
        return self.depth_of(P) <= best + tol


# ----------------------------------------------------------------------------- sheets
def _place_markers(items_px, rad=21):
    """items_px: list of (n, anchor_xy). Returns list of (n, anchor, circle_xy) avoiding overlaps."""
    placed = []
    taken = []
    offs = [(0, 0)] + [(rad * 1.9 * math.cos(t), rad * 1.9 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    offs += [(rad * 3.3 * math.cos(t), rad * 3.3 * math.sin(t)) for t in np.linspace(0.2, 2 * math.pi + 0.2, 16, endpoint=False)]
    for n, (ax_, ay_) in items_px:
        for ox, oy in offs:
            c = (ax_ + ox, ay_ + oy)
            if all(math.hypot(c[0] - t[0], c[1] - t[1]) > rad * 2.05 for t in taken):
                break
        taken.append(c)
        placed.append((n, (ax_, ay_), c))
    return placed


def fit_text(items, width_in, height_in, fs_max=8.0, fs_min=5.8):
    """(head, body lines) per item with the biggest font that fits."""
    fs = fs_max
    while True:
        cpl = max(30, int(width_in * 72 / (0.505 * fs)) - 5)
        blocks = []
        for it in items:
            head = it["tipo"] + (f"  ·  Ø{it['diam']}" if it.get("diam") and f"Ø{it['diam'].replace('.0', '')}" not in it["tipo"] else "") + (f"  ·  ×{len(it['puntos'])}" if len(it["puntos"]) > 1 else "")
            blocks.append((head, textwrap.wrap(it["texto"], cpl)))
        lh = fs * 1.27 / 72
        need = sum((1 + len(b[1])) * lh + 0.06 for b in blocks)
        if need <= height_in or fs <= fs_min:
            return fs, blocks, lh, need
        fs -= 0.2


def draw_sheet(fig_path_png, fig_path_pdf, pieza, items, views, header, page_note=None):
    """items: list of dict(n,tipo,cat,diam,texto,puntos,tol,vis). views: list of View. Returns the figure (saved)."""
    fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
    fig.patch.set_facecolor("white")
    fig.text(0.025, 0.955, header["titulo"], fontsize=17, fontweight="bold", va="center")
    for li, ln in enumerate(textwrap.wrap(header["sub"], 175)):
        fig.text(0.025, 0.920 - li * 0.021, ln, fontsize=8.4, va="center", color="#333333")
    fig.text(0.025, 0.018, "LanternGuard · guía de piezas · " + header["pie"], fontsize=6.5, color="#777777")
    fig.text(0.975, 0.018, header["pagina"], fontsize=6.5, color="#777777", ha="right")
    nv = len(views)
    area = (0.02, 0.05, 0.57, 0.84)
    hh = area[3] / nv
    for vi, v in enumerate(views):
        ax = fig.add_axes([area[0], area[1] + area[3] - hh * (vi + 1), area[2], hh - 0.005])
        ax.imshow(v.img, extent=(0, VW, VH, 0), interpolation="bilinear")
        ax.set_xlim(0, VW)
        ax.set_ylim(VH, 0)
        ax.axis("off")
        if nv > 1:
            ax.text(8, 30, f"Vista {'AB'[vi]}", fontsize=8, color="#666666", va="top")
        to_place = []
        for it in items:
            vis_pts = it["vis"].get(vi, [])
            col = CATS[it["cat"]][0]
            for q in vis_pts[1:]:
                x, y = v.px(q)
                ax.plot([x], [y], "o", ms=5, color=col, mec="white", mew=0.5, zorder=5)
            if vis_pts:
                to_place.append((it["n"], tuple(v.px(vis_pts[0]))))
                far = [q for q in vis_pts[1:] if np.linalg.norm(v.px(q) - v.px(vis_pts[0])) > 320]
                if far and len(vis_pts) > 2:
                    to_place.append((it["n"], tuple(v.px(far[0]))))
        for n, anc, c in _place_markers(to_place):
            col = CATS[items[n - 1]["cat"]][0]
            if math.hypot(c[0] - anc[0], c[1] - anc[1]) > 1:
                ax.plot([anc[0], c[0]], [anc[1], c[1]], "-", color=col, lw=0.9, zorder=6)
            ax.plot([anc[0]], [anc[1]], "o", ms=5, color=col, mec="white", mew=0.5, zorder=7)
            ax.add_patch(Circle(c, 20, fc=col, ec="white", lw=1.1, zorder=8))
            ax.text(c[0], c[1] + 0.5, str(n), color="white", fontsize=9 if n < 10 else 8, fontweight="bold", ha="center", va="center", zorder=9)
    # legend
    lx, ly, lw_, lh_ = 0.600, 0.05, 0.39, 0.84
    fs, blocks, lh, _need = fit_text(items, lw_ * 11.69 - 0.32, lh_ * 8.27 - 0.1)
    y = ly + lh_
    for it, (head, lines) in zip(items, blocks):
        col = CATS[it["cat"]][0]
        yy = y - 0.003
        fig.patches.append(matplotlib.patches.Ellipse((lx + 0.0105, yy - 0.0095), 0.0185, 0.0185 * 11.69 / 8.27, transform=fig.transFigure, fc=col, ec="none"))
        fig.text(lx + 0.0105, yy - 0.0095, str(it["n"]), color="white", fontsize=min(fs, 7.2), fontweight="bold", ha="center", va="center")
        fig.text(lx + 0.026, yy - 0.5 * lh / 8.27, head, fontsize=fs, va="center", fontweight="bold", color=col)
        for li, line in enumerate(lines):
            fig.text(lx + 0.026, yy - (li + 1.5) * lh / 8.27, line, fontsize=fs, va="center")
        y -= (1 + len(lines)) * lh / 8.27 + 0.06 / 8.27
    # category key
    kx = 0.025
    for k, (c, name) in CATS.items():
        if any(i["cat"] == k for i in items):
            fig.patches.append(matplotlib.patches.Ellipse((kx + 0.004, 0.047), 0.008, 0.008 * 11.69 / 8.27, transform=fig.transFigure, fc=c, ec="none"))
            fig.text(kx + 0.011, 0.047, name, fontsize=6.5, va="center", color="#333333")
            kx += 0.012 + 0.0062 * len(name)
    if fig_path_png:
        fig.savefig(fig_path_png, dpi=150)
    if fig_path_pdf:
        fig.savefig(fig_path_pdf)
    return fig


# ============================================================================= content
import argparse  # noqa: E402
import datetime  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOYA = ROOT / "salida" / "boya_pet" / "step"
NODO = ROOT / "salida" / "prototipos" / "P2_robusto" / "step"
OUT = ROOT / "salida" / "guia_piezas"
DOCS = ROOT / "docs"


def A(cat, tipo, texto, spec, diam=None, key=None, tol=0.0):
    """Item whose anchors are detected holes (spec: dict or list of dicts, see match())."""
    return dict(auto=True, cat=cat, tipo=tipo, texto=texto, spec=spec if isinstance(spec, list) else [spec], diam=diam, key=key, tol=tol)


def M(cat, tipo, texto, puntos, diam=None, key=None, tol=3.0):
    """Item with hand-written 3D anchors (shapes, windows, grooves)."""
    return dict(auto=False, cat=cat, tipo=tipo, texto=texto, puntos=[tuple(map(float, p)) for p in puntos], diam=diam, key=key, tol=tol)


def IGN(spec):
    """Detected cylinders that are not features (inner fillets)."""
    return dict(ignore=True, spec=spec if isinstance(spec, list) else [spec])


NOTA_CONCEPTO = " Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente."
H_DX = (0.5, 3.0)

PIEZAS = []

# ----------------------------------------------------------------------------- boya (PET bottle buoy)
PIEZAS += [
    dict(id="B1_casco", grupo="Boya", step=BOYA / "B1_casco.step", titulo="B1 · Casco (una mitad)",
         sub="Estructura que sostiene las botellas PET. Se imprime 2 veces: la segunda mitad es esta misma pieza girada 180° (x = 0 es la unión). Ejes: x a lo largo de las botellas, z arriba.",
         views=[(215, 33), (38, 38)],
         items=[
             A("union", "Tornillos de unión de las mitades", "Paso M3 (Ø3.4) en x = 0. Seis M3×20 inox con tuerca cruzan las dos bridas de 4 + 4 mm: 4 en las columnas del canal (y = ±19) y 2 en las almohadillas bajas de las paredes (y = ±107).",
               dict(D=3.4, ax="x", x=(-6, 2)), key="union"),
             M("ajuste", "Pin Ø4 de alineación", "Pin impreso Ø4 en x = 0 (y = +19, z = 28) que entra en el alojamiento de la otra mitad. Garantiza que las dos mitades coinciden antes de apretar los M3.",
               [(2.0, 19.0, 28.0)], diam="4.0", key="pin", tol=4),
             A("ajuste", "Alojamiento del pin", "Agujero Ø4.4 (pin 4 + holgura 0.2) en y = −19: recibe el pin de la otra mitad.",
               dict(D=4.4, ax="x"), key="aloj"),
             A("union", "Pasos M3 hacia las cunas", "Cuatro pasos M3 (Ø3.4) en la costilla del extremo. Los tornillos vienen de las bahías del casco y se enroscan en los insertos de las lengüetas de las cunas B5.",
               dict(D=3.4, ax="x", x=(-130, -120)), key="cunas"),
             A("union", "Insertos M3 de los postes", "Inserto térmico M3 (Ø4.0 × 6) en la punta de cada poste: reciben los 4 tornillos M3 con que se atornilla la cubierta B2 (cada mitad de B2 va a sus propios 4 postes).",
               dict(D=4.0, ax="z"), key="insertos"),
             M("forma", "Poste Ø10", "Cuatro postes Ø10 que nacen del piso y suben hasta el inserto. Pasaron de Ø8 a Ø10 el 04/11; los del medio llevan un collar a 45° donde salen de la silla baja.",
               [(-123, 23, 70), (-123, -23, 70), (-63.5, 23, 70), (-63.5, -23, 70)], diam="10", key="postes", tol=7),
             A("cable", "Ojal de amarre", "Agujero Ø10.5 en el parche de la quilla. Hay uno por mitad (x = ±21): el cabo de amarre va en pata de gallo, con dos ramales a un nudo. Es independiente del umbilical.",
               dict(D=10.5, ax="z"), key="ojal", tol=3),
             M("cable", "Canal central", "Hueco de 50 mm entre las dos bahías (y = ±25), sin costillas. Por aquí baja el cable umbilical y caben el domo del PG7 y la contratuerca de la caja B3.",
               [(-95, 0, 2.5), (-30, 0, 2.5)], key="canal", tol=1000),
             A("forma", "Silla baja de la botella", "Ranura en U Ø83 (botella Ø80 + 1.5 de holgura). Desde el 04/11 las costillas intermedias son sillas bajas (≤ 15 mm sobre el patín) y no varillas de 2.4×3. Lo que sujeta la botella hacia arriba son las barras de B2 y las correas.",
               dict(D=83, ax="x"), key="silla"),
             A("forma", "Ranura del cuello", "Ranura Ø32 en la costilla del extremo (bahía y = −69): por ella asoma el cuello de la botella, unos 21 mm fuera del casco.",
               dict(D=32, ax="x"), key="cuello"),
             M("forma", "Rombo de aligeramiento", "Ventana en rombo en la costilla del extremo de la base de la botella (bahía y = +69). Ahorra material y, con caras a 45°, se imprime sin puentes.",
               [(-125.0, 68.9, 43.9)], key="rombo", tol=6),
             M("forma", "Ventanas hexagonales", "Cuatro ventanas hexagonales en la pared exterior (2 por bahía visible). Aligeran la pared y sirven para inyectar la espuma de poliuretano que da reserva de flotación.",
               [(-94.25, 112.8, 27), (-31.75, 112.8, 27), (-94.25, -112.8, 27), (-31.75, -112.8, 27)], key="hex", tol=4),
             M("forma", "Patín bajo la botella", "Piso de 2.4 mm y 24 mm de ancho bajo cada botella: es lo único que toca la botella por abajo. El resto del fondo queda abierto para que escurra el agua.",
               [(-95, 68.9, 2.4), (-95, -68.9, 2.4)], key="patin", tol=3),
             M("forma", "Chaflán 45° en la base de los soportes", "Chaflanes de 45° donde costillas y postes nacen del patín: evitan voladizos y soportes de impresión (corrección de la jefa de práctica).",
               [(-63.5, 80, 4), (-63.5, -80, 4), (-63.5, 23, 17.4), (-63.5, -23, 17.4)], key="chaflan", tol=5),
         ]),
    dict(id="B2_cubierta_lisa", grupo="Boya", step=BOYA / "B2_cubierta_lisa.step", titulo="B2 · Cubierta, lado liso",
         sub="Marco de barras que cierra el casco por arriba y sostiene la caja B3 y el panel solar. Cada mitad es un marco cerrado atornillado a sus propios 4 postes. Esta es la que no lleva mástil.",
         views=[(215, 35)],
         items=[
             A("union", "Pasos M3 al casco", "Cuatro pasos M3 (Ø3.4) en las barras: los tornillos entran a los insertos de los postes de B1 ([[B1_casco:insertos]]).",
               dict(D=3.4, ax="z"), key="pasos"),
             A("union", "Pilares con inserto M3", "Dos pilares Ø10 × 6 bajo las orejas de la caja. Inserto M3 (Ø4.0): recibe el tornillo que atraviesa la oreja de B3.",
               dict(D=4.0, ax="z", z=(80, 120)), key="pilares"),
             A("union", "Columnas del panel con inserto M3", "Dos columnas Ø12 que suben 107 mm. Inserto M3 (Ø4.0) en la punta: el panel solar de 170×170 se atornilla a las cuatro columnas (2 por mitad), 25 mm sobre la tapa.",
               dict(D=4.0, ax="z", z=(150, 210)), key="columnas"),
             M("forma", "Barras de 14 × 4 mm", "Barras que cruzan sobre las botellas: no las dejan salir hacia arriba. Los huecos entre barras son por donde se inyecta la espuma. La barra de x = 0 es nueva: cierra el marco de cada mitad.",
               [(-63.5, 0, 89.4), (-4, -40, 89.4), (-30, 68.9, 89.4)], key="barras", tol=3),
             M("forma", "Pie a 45° de pilares y columnas", "Chaflán de 45° en la base de pilares y columnas sobre las barras (chaflán de la base de soportes): imprime sin soporte.",
               [(-69, 51.4, 90.5), (-69, -51.4, 90.5), (-70, 68.9, 91), (-70, -68.9, 91)], key="pie45", tol=5),
         ]),
    dict(id="B2_cubierta_mastil", grupo="Boya", step=BOYA / "B2_cubierta_mastil.step", titulo="B2 · Cubierta, lado mástil",
         sub="La otra mitad de la cubierta, con el mástil de la antena. Mismos pilares y columnas que el lado liso; la caja y el panel atornillados encima amarran las dos mitades.",
         views=[(35, 35), (215, 30)],
         items=[
             A("union", "Pasos M3 al casco", "Cuatro pasos M3 (Ø3.4): tornillos hacia los insertos de los postes de B1.",
               dict(D=3.4, ax="z"), key="pasos"),
             A("union", "Pilares con inserto M3", "Dos pilares Ø10 bajo las orejas de la caja: inserto M3 (Ø4.0) para el tornillo de la oreja de B3.",
               dict(D=4.0, ax="z", z=(80, 120)), key="pilares"),
             A("union", "Columnas del panel con inserto M3", "Dos columnas Ø12 con inserto M3 (Ø4.0) en la punta para el panel solar.",
               dict(D=4.0, ax="z", z=(150, 210)), key="columnas"),
             A("cable", "Hueco del mástil Ø8", "Mástil Ø14 con hueco interior Ø8 desde z = 95 hasta la punta. Por dentro sube el pigtail de la antena (un cable corto con el conector de antena).",
               dict(D=8.0, ax="z"), key="mastil", tol=2),
             A("cable", "Puerto del pigtail Ø7", "Agujero Ø7 en el mástil hacia la caja: por aquí sale el pigtail y va a un PG7 de la cara +X de B3 ([[B3_caja:pg7_pig]]).",
               dict(D=7.0, ax="x"), key="puerto", tol=4),
             M("forma", "Barras y barra de costura", "Marco de barras de 14 × 4 mm; la barra en x = 0 cierra este marco. Igual que en el lado liso: retiene las botellas y deja huecos para la espuma.",
               [(63.5, 0, 89.4), (4, -40, 89.4), (30, 68.9, 89.4)], key="barras", tol=3),
             M("forma", "Pie a 45° de pilares y columnas", "Chaflán de 45° en la base de pilares, columnas y mástil (chaflán de la base de soportes).",
               [(69, 51.4, 90.5), (69, -51.4, 90.5), (70, 68.9, 91), (70, -68.9, 91)], key="pie45", tol=5),
         ]),
    dict(id="B3_caja", grupo="Boya", step=BOYA / "B3_caja.step", titulo="B3 · Caja seca",
         sub="Caja hermética de la electrónica de la boya (PCB, Waveshare, portabaterías 3×18650, RTC). Paredes de 2.4 mm con brida de 10 × 7 mm. Se cierra con la tapa B4.",
         views=[(215, 30), (35, 38)],
         items=[
             IGN(dict(D=6.0, ax="z", len=(30, 100))),
             A("union", "Pasos M3 de las orejas", "Cuatro orejas de 14×14×4 mm en las esquinas. Un M3 por oreja entra al inserto del pilar de B2 ([[B2_cubierta_lisa:pilares]]): así la caja queda fija a la cubierta.",
               dict(D=3.4, ax="z"), key="orejas"),
             A("sello", "Insertos M3 de la brida", "Diez insertos térmicos M3 (Ø4.0 × 6) en la brida de 7 mm. Los tornillos de la tapa B4 los aprietan. Son ciegos (no atraviesan) y quedan afuera del cordón.",
               dict(D=4.0, ax="z", z=(160, 175)), key="ins_brida"),
             A("mont", "Standoffs del portabaterías", "Cuatro standoffs Ø9 con inserto M3: sostienen el portabaterías 3×18650 separado del piso.",
               dict(D=4.0, ax="z", z=(95, 110)), key="standoff"),
             A("mont", "Postes de la bandeja", "Cuatro postes Ø9 con inserto M3 en la punta: sostienen la bandeja donde van la PCB y el Waveshare.",
               dict(D=4.0, ax="z", z=(125, 145)), key="postes"),
             A("cable", "PG7 del umbilical", "Agujero Ø12.6 en la pared −X (z = 30 mm sobre el piso interior). Entra el cable umbilical que baja al nodo; la contratuerca va por dentro y el prensaestopas aprieta el cable. Sella el paso.",
               dict(D=12.6, ax="x", x=(-100, 0)), key="pg7_umb", tol=3),
             A("cable", "PG7 del cable solar", "Agujero Ø12.6 en la pared +X (y = −25): entra el cable del panel solar.",
               dict(D=12.6, ax="x", x=(0, 100), y=(-40, 0)), key="pg7_solar", tol=3),
             A("cable", "PG7 del pigtail de antena", "Agujero Ø12.6 en la pared +X (y = +25): entra el pigtail que viene del mástil de B2 ([[B2_cubierta_mastil:puerto]]).",
               dict(D=12.6, ax="x", x=(0, 100), y=(0, 40)), key="pg7_pig", tol=3),
             M("sello", "Brida plana con chaflán 45°", "Brida de 10 mm de ancho y 7 de espesor. Su cara superior, plana, es donde aprieta el cordón de la tapa (ver [[B4_tapa:groove]]). Abajo lleva un chaflán de 45° para imprimir sin soportes.",
               [(0, -53, 169.8), (-70, 0, 169.8)], key="brida", tol=3),
         ]),
    dict(id="B4_tapa", grupo="Boya", step=BOYA / "B4_tapa.step", titulo="B4 · Tapa de la caja seca",
         sub="Tapa plana de 4 mm de B3. Se imprime con la ranura hacia arriba (girada 180°). Aquí está el sello que mantiene seca la electrónica.",
         views=[(215, 30), (215, -40)],
         items=[
             IGN(dict(D=16.0, ax="z")),
             A("union", "Pasos M3 de la tapa", "Diez pasos M3 (Ø3.4): los tornillos entran a los diez insertos de la brida de B3 ([[B3_caja:ins_brida]]) y comprimen el cordón.",
               dict(D=3.4, ax="z"), key="pasos"),
             M("sello", "Ranura del cordón O-ring", "Ranura rectangular de 2.6 mm de ancho × 1.5 de hondo en la cara inferior, 2.8 mm afuera de la pared. Lleva un cordón de goma Ø2 mm (25 % de compresión) que aprieta contra la brida plana de B3.",
               [(0, 47.2, 169.8), (0, -47.2, 169.8), (76.2, 0, 169.8), (-76.2, 0, 169.8)], key="groove", tol=3),
         ]),
    dict(id="B5_cuna_base", grupo="Boya", step=BOYA / "B5_cuna_base.step", titulo="B5 · Cuna, lado base",
         sub="Cuna que sostiene una botella a lo largo de Y en cada extremo del casco. Mitad del lado de la base de la botella; se imprime 2 veces (una por cuna). Aquí x = 0 es la unión con el lado cuello.",
         views=[(215, 33), (38, 38)],
         items=[
             A("union", "Pasos M3 de unión de las mitades", "Dos pasos M3 (Ø3.4) en almohadillas bajas en x = 0: un M3 por lado une esta mitad con la del cuello (brida 4 + 4 mm).",
               dict(D=3.4, ax="x"), key="union"),
             A("union", "Insertos M3 de las lengüetas", "Inserto M3 (Ø4.0 × 6, eje en Y) en cada lengüeta de 12 × 14 mm que sale hacia el casco. El tornillo entra desde la bahía de B1, cruza la costilla del extremo ([[B1_casco:cunas]]) y rosca aquí.",
               dict(D=4.0, ax="y"), key="lenguetas"),
             A("union", "Insertos M3 de los postes de correa", "Dos postes Ø10 (corridos 1 mm afuera para no tocar la botella) con inserto M3: reciben los tornillos de la correa B6.",
               dict(D=4.0, ax="z"), key="postes"),
             A("forma", "Silla baja de la botella", "Ranuras en U Ø83 en la costilla del medio y en la de la unión: guían la botella; las correas B6 la sujetan hacia arriba.",
               dict(D=83, ax="x"), key="silla"),
             M("forma", "Rombo de aligeramiento", "Ventana en rombo en la costilla del extremo de la base de la botella (cerrada: la base de la botella la toca). Ahorra material y se imprime sin puentes.",
               [(-125.0, 0, 43.9)], key="rombo", tol=6),
             M("forma", "Ventanas hexagonales", "Cuatro ventanas hexagonales (2 por pared): aligeran y dejan inyectar espuma de poliuretano.",
               [(-94.25, 43.9, 27), (-31.75, 43.9, 27), (-94.25, -43.9, 27), (-31.75, -43.9, 27)], key="hex", tol=4),
             M("forma", "Chaflán 45° en la base de los soportes", "Chaflanes de 45° en la unión de costillas, lengüetas y postes con el patín: sin voladizos ni soportes.",
               [(-63.5, 12, 4), (-63.5, -12, 4), (-46.9, 50, 7)], key="chaflan", tol=6),
         ]),
    dict(id="B5_cuna_cuello", grupo="Boya", step=BOYA / "B5_cuna_cuello.step", titulo="B5 · Cuna, lado cuello",
         sub="La otra mitad de la cuna, la que recibe el cuello de la botella. Se imprime 2 veces. Mismas uniones que el lado base.",
         views=[(35, 33), (215, 38)],
         items=[
             A("union", "Pasos M3 de unión de las mitades", "Dos pasos M3 (Ø3.4) en x = 0: unen esta mitad con la del lado base.",
               dict(D=3.4, ax="x"), key="union"),
             A("union", "Insertos M3 de las lengüetas", "Inserto M3 (Ø4.0, eje en Y) en cada lengüeta: reciben los tornillos que vienen del casco B1.",
               dict(D=4.0, ax="y"), key="lenguetas"),
             A("union", "Insertos M3 de los postes de correa", "Dos postes Ø10 con inserto M3 (Ø4.0) para la correa B6.",
               dict(D=4.0, ax="z"), key="postes"),
             A("forma", "Silla baja de la botella", "Ranuras en U Ø83 que guían la botella.",
               dict(D=83, ax="x"), key="silla"),
             A("forma", "Ranura del cuello", "Ranura Ø32 en la costilla del extremo: por aquí asoma el cuello de la botella.",
               dict(D=32, ax="x"), key="cuello"),
             M("forma", "Ventanas hexagonales", "Cuatro ventanas hexagonales (2 por pared): aligeran y dejan inyectar espuma.",
               [(94.25, 43.9, 27), (31.75, 43.9, 27), (94.25, -43.9, 27), (31.75, -43.9, 27)], key="hex", tol=4),
             M("forma", "Chaflán 45° en la base de los soportes", "Chaflanes de 45° en la unión de costillas, lengüetas y postes con el patín.",
               [(63.5, 12, 4), (63.5, -12, 4), (46.9, 50, 7)], key="chaflan", tol=6),
         ]),
    dict(id="B6_correa", grupo="Boya", step=BOYA / "B6_correa.step", titulo="B6 · Correa",
         sub="Cierra cada cuna sobre la botella. Se imprimen 4 (2 por cuna). Va plana sobre la cama.",
         views=[(30, 40)],
         items=[
             A("union", "Pasos M3 en los extremos", "Dos agujeros M3 (Ø3.4) a 92 mm entre centros: se atornillan a los insertos de los postes de la cuna ([[B5_cuna_base:postes]]).",
               dict(D=3.4, ax="z"), key="pasos"),
             M("forma", "Banda plana de 14 × 4 mm", "Banda que pasa por encima de la botella y la sujeta hacia arriba contra la silla baja de la cuna.",
               [(0, 0, 4)], key="banda", tol=2),
         ]),
]

# ----------------------------------------------------------------------------- nodo P2_robusto
PIEZAS += [
    dict(id="M1s_caja_cuerpo", grupo="Nodo P2", step=NODO / "M1s_caja_cuerpo.step", titulo="M1s · Caja del nodo (cuerpo)",
         sub="Caja seca del nodo (127 × 126 × 77 mm exteriores). En los dos extremos lleva el cojín donde se atornilla cada riel; abajo, los bolsillos de lastre. Se cierra con la tapa M2. x a lo largo de los rieles, z arriba.",
         views=[(60, 30), (215, -35)],
         items=[
             IGN(dict(D=6.0, ax="z", len=(30, 100))),
             M("forma", "Cojín cuadrado de la pared (el \"agujero cuadrado\" del costado)", "En cada pared de extremo hay un cojín rectangular (casi cuadrado) de 10 mm de espesor y 50 mm de ancho. No es un agujero cuadrado: es una placa en relieve con un agujero redondo ([[M1s_caja_cuerpo:bore]]) y 4 tornillos ([[M1s_caja_cuerpo:m4]]). Da un asiento plano a la brida del riel y refuerza la pared donde se rosca. Hay uno por extremo (×2)." + NOTA_CONCEPTO,
               [(73.6, -21, 30.5), (-73.6, 21, 30.5)], key="cojin", tol=3),
             A("cable", "Agujero redondo Ø30 del cojín", "Ventana de acceso de 30 mm en el cojín. Deja entrar el domo del PG7 (que asoma hacia afuera) y una llave para apretar la contratuerca. Por aquí el cable sale de la caja hacia el conducto del riel ([[M3s_riel_gancho:dome]])." + NOTA_CONCEPTO,
               dict(D=30, ax="x"), key="bore", tol=2),
             A("union", "Insertos M4 del cojín", "Cuatro insertos térmicos M4 (Ø5.6 × 8.5) por cojín, en cuadro de 40 × 20 mm. Son los 4 tornillos que se ven al costado: los M4 de la brida del riel ([[M3s_riel_gancho:m4]]) entran aquí. Ciegos: no perforan la pared de la caja." + NOTA_CONCEPTO,
               dict(D=5.6, ax="x"), key="m4", tol=2),
             A("cable", "PG7 de la pared (cámara)", "Agujero Ø12.6 para el prensaestopas PG7 en el fondo del Ø30. Por él pasa el cable Cat5e de la cámara (un cable por cápsula: imagen SPI y anillo LED) hacia el interior seco. La contratuerca va dentro (9 mm). Es el sello del cable." + NOTA_CONCEPTO,
               dict(D=12.6, ax="x"), key="pg7", tol=14),
             A("sello", "Insertos M3 de la brida", "Doce insertos térmicos M3 (Ø4.0 × 6) en la brida: los 12 tornillos de la tapa M2 los aprietan y comprimen el cordón O-ring. Ciegos y fuera del cordón.",
               dict(D=4.0, ax="z", z=(60, 80)), key="ins_brida", tol=2),
             M("sello", "Brida plana: asiento del cordón", "La cara superior de la brida es plana: contra ella aprieta el cordón de goma Ø2 que va en la ranura de la tapa M2 (ver [[M2_caja_tapa:groove]]).",
               [(0, -69, 77), (0, 69, 77)], key="brida", tol=3),
             M("forma", "Falda a 45° bajo la brida", "El paso del cuerpo a la brida es un chaflán a 45°: se imprime sin soportes.",
               [(0, -68, 66), (-68, 0, 66)], key="falda", tol=5),
             A("mont", "Insertos M3 de los bosses de la bandeja", "Cuatro bosses Ø8 sobre el piso con inserto M3: atornillan la bandeja M11 (en el interior seco). Cada boss, igual que las paredes interiores, nace del piso con un chaflán de 45° (chaflán de la base de soportes).",
               dict(D=4.0, ax="z", z=(5, 15)), key="bosses", tol=3),
             A("union", "Insertos M3 de los bolsillos", "Cuatro insertos M3 (Ø4.0) en el fondo de los bolsillos (2 por bolsillo): ahí se atornillan los M3 avellanados de la tapa M3t.",
               dict(D=4.0, ax="z", z=(-40, -10)), key="ins_m3t", tol=3),
             M("forma", "Bolsillos de lastre", "Dos cajones de 100 × 50 × 30 mm bajo el piso (uno por lado), abiertos por abajo y fuera del sello. Llevan las tuercas y arandelas M8 a granel (575 g por bolsillo, 1150 g en total) y se cierran con M3t. Entra agua: es lo normal.",
               [(0, 29.5, -14), (0, -29.5, -14)], key="bolsillos", tol=6),
         ]),
    dict(id="M2_caja_tapa", grupo="Nodo P2", step=NODO / "M2_caja_tapa.step", titulo="M2 · Tapa de la caja con asa",
         sub="Cierra la caja M1s. Lleva el asa para cargar con guante, el ojo de anclaje del cabo y el PG7 del umbilical. Se imprime girada (Y+90). Aquí z crece hacia arriba (asa arriba).",
         views=[(40, 35), (40, -40)],
         items=[
             IGN(dict(D=6.0, ax="y")),
             A("union", "Pasos M3 de la tapa", "Doce pasos M3 (Ø3.4): los tornillos entran a los doce insertos de la brida de M1s ([[M1s_caja_cuerpo:ins_brida]]) y aprietan el cordón.",
               dict(D=3.4, ax="z"), key="pasos"),
             A("sello", "Ranura del cordón O-ring (4 esquinas)", "Ranura rectangular de 2.6 × 1.5 mm en la cara inferior, a mitad de camino entre la cavidad y la línea de tornillos. Cordón de goma Ø2. Se marcan las 4 esquinas redondeadas (R6); la ranura sigue el contorno.",
               dict(D=12, ax="z"), key="groove", tol=2),
             A("cable", "PG7 del umbilical", "Agujero Ø12.6 en la tapa: entra el cable umbilical que sube a la boya (cable flojo, con curva). Prensaestopas con contratuerca por dentro; es un sello del nodo.",
               dict(D=12.6, ax="z"), key="pg7", tol=2),
             A("union", "Ojo de anclaje Ø10", "Ojo Ø10 en lo alto del asa, con eje en Y: aquí se amarra el cabo que sube a la linterna / línea larga.",
               dict(D=10, ax="y"), key="ojo", tol=3),
             M("forma", "Asa en arco", "Asa de 12 mm de grosor con apertura para guante. El techo de la ventana va a 45° para imprimir sin soportes.",
               [(-25, 6, 122), (-47, 6, 92)], key="asa", tol=5),
         ]),
    dict(id="M3s_riel_gancho", grupo="Nodo P2", step=NODO / "M3s_riel_gancho.step", titulo="M3s · Riel con gancho (una mitad)",
         sub="Riel hueco de 30 × 30 mm (celosía) que sale de la caja y lleva la cápsula de cámara. Una mitad por lado; la otra es la misma pieza girada 180° sobre z. El gancho en C cuelga el nodo del aro de la linterna.",
         views=[(35, 28), (215, 25)],
         items=[
             IGN(dict(D=20.8, ax="y")),
             A("union", "Pasos M4 de la brida", "Cuatro pasos M4 (Ø4.2) en la brida de 25 mm de ancho: los 4 tornillos M4 que atan el riel al cojín de la caja ([[M1s_caja_cuerpo:m4]]). Unión no estanca." + NOTA_CONCEPTO,
               dict(D=4.2, ax="x", x=(60, 90)), key="m4", tol=3),
             A("cable", "Ventana Ø21 de la brida", "Ventana de 21 mm. Mirando el riel desde el lado de la caja es el agujero redondo grande que se ve en la brida, junto a la celosía. Deja pasar el domo del PG7 de la caja (que asoma por el Ø30 del cojín). De aquí el Cat5e sale del PG7 hacia el interior del conducto." + NOTA_CONCEPTO,
               dict(D=21, ax="x"), key="dome", tol=3),
             M("cable", "Conducto hueco por dentro", "El riel es un tubo hueco: 10 mm libres entre paredes de 5 mm. Por dentro corre el Cat5e de la cámara (varilla M8 de lastre aparte). Va inundado: no sella; el sello son los PG7." + NOTA_CONCEPTO,
               [(135, 0, 13.7)], key="conducto", tol=1000),
             M("forma", "Celosía de triángulos (ahorro de material)", "Ventanas triangulares (celosía Warren de 65°, barras de 3 mm) en las dos paredes. Quitan material y peso. No son pasos de cable: el cable va por dentro y se ve a través de ellas.",
               [(97, 15, 13.7), (115, 15, 13.7), (133, 15, 13.7), (97, -15, 13.7), (115, -15, 13.7), (133, -15, 13.7)], key="celosia", tol=3),
             A("cable", "Agujero redondo Ø8 de la punta", "Es el agujero redondo que se ve en el extremo del riel (pared de 5 mm). Es la entrada del cable de la cámara al riel: el Cat5e sale del PG7 de la cápsula ([[M4_capsula_cuerpo:pg7]]), hace un bucle y entra por aquí, corre por el conducto ([[M3s_riel_gancho:conducto]], se ve por la celosía), pasa la ventana Ø21 ([[M3s_riel_gancho:dome]]) y llega al PG7 del cojín de la caja ([[M1s_caja_cuerpo:pg7]])." + NOTA_CONCEPTO,
               dict(D=8, ax="x"), key="punta", tol=3),
             A("union", "M4 de la silla de la cápsula", "Dos tornillos M4 (a x = 170 y 200) cruzan el riel de lado a lado: se ven 4 pasos Ø4.2, uno por pared. Aprietan las mejillas de la silla de M5s contra el riel. NO son pasos de cable.",
               dict(D=4.2, ax="y"), key="silla", tol=3),
             A("union", "Asiento en C del gancho", "C abierta de Ø8.8 (varilla del aro Ø8 + 0.4 de holgura): el nodo cae sobre la varilla del aro de la linterna. Una correa de 25 × 3 pasa por la ranura del alma.",
               dict(D=8.8, ax="y"), key="gancho", tol=3),
         ]),
    dict(id="M3t_tapa_bolsillo", grupo="Nodo P2", step=NODO / "M3t_tapa_bolsillo.step", titulo="M3t · Tapa del bolsillo de lastre",
         sub="Placa de 3 mm que cierra por abajo cada bolsillo de lastre de la caja. Se imprimen 2 (una por bolsillo). Plana en la cama.",
         views=[(30, -40)],
         items=[
             A("union", "Pasos M3 avellanados", "Dos pasos M3 (Ø3.4) con avellanado: la cabeza queda al ras del fondo. Los M3 de 8 mm entran a los insertos del fondo del bolsillo ([[M1s_caja_cuerpo:ins_m3t]]).",
               dict(D=3.4, ax="z"), key="pasos", tol=2),
             M("forma", "Placa de cierre", "Placa de 107 × 35 × 3 mm que retiene el lastre a granel. No es estanca: el bolsillo está fuera del sello.",
               [(0, 29, -31.5)], key="placa", tol=3),
         ]),
    dict(id="M4_capsula_cuerpo", grupo="Nodo P2", step=NODO / "M4_capsula_cuerpo.step", titulo="M4 · Cápsula de cámara (cuerpo)",
         sub="Caja estanca de la cámara Arducam Mega 5 MP, con anillo LED y ventana de acrílico. Brida de 4 mm que se cierra con la tapa M5s. Hay una por lado (×2). x es el eje óptico (adelante = +x).",
         views=[(35, 25), (215, 25)],
         items=[
             IGN(dict(D=4.0, ax="x", len=(30, 50))),
             A("union", "Pasos M3 de la brida", "Cuatro pasos M3 (Ø3.4) en las esquinas de la brida: M3 con tuerca unen la tapa M5s y aprietan el cordón O-ring Ø2 ([[M5s_capsula_tapa_pie:groove]]).",
               dict(D=3.4, ax="x"), key="pasos"),
             A("cable", "PG7 de la cápsula", "Agujero Ø12.6 en la pared inferior, a 10 mm de la apertura trasera. Entra el Cat5e de esta cámara (imagen SPI y anillo LED); este es el otro extremo del cable del riel ([[M3s_riel_gancho:punta]]). Sello del cable; hay 23 mm atrás para el bucle y la contratuerca.",
               dict(D=12.6, ax="z"), key="pg7", tol=3),
             A("sello", "Asiento de la ventana Ø30.4", "Rebaje frontal para el disco de acrílico M7 (Ø30 × 3). El bisel M6 lo mantiene en su lugar. A confirmar: el CAD solo define el asiento; el sellador o junta de la ventana no está especificado.",
               dict(D=30.4, ax="x"), key="asiento", tol=3),
             M("forma", "Apertura anular del LED con 3 radios", "Anillo de luz Ø26 alrededor del lente: deja salir la luz del anillo LED (Ø30 × 3, pegado a la cara interior). Tres radios de 2 mm sujetan el tubo opaco que impide que el LED ilumine el lente por dentro.",
               [(65, 0, -11)], key="anillo", tol=3),
             A("forma", "Orificio del lente Ø16.4", "Agujero central: por aquí mira el porta-lente Ø16 de la cámara. Lo rodea un tubo separador opaco (pared 1.2).",
               dict(D=16.4, ax="x"), key="lente", tol=3),
             A("union", "Pilotos M2 del bisel", "Tres agujeros ciegos Ø1.8 × 4 mm: tornillos M2 autorroscantes del bisel M6.",
               dict(D=1.8, ax="x"), key="pilotos", tol=2),
             M("mont", "Cavidad 38 × 38 × 38", "Aloja la cámara (33 × 33 × 17), el anillo LED y, detrás, 23 mm de zona libre para el bucle del cable y la contratuerca del PG7.",
               [(45, 0, 0)], key="cavidad", tol=1000),
         ]),
    dict(id="M5s_capsula_tapa_pie", grupo="Nodo P2", step=NODO / "M5s_capsula_tapa_pie.step", titulo="M5s · Tapa de la cápsula con pie",
         sub="Cierra la cápsula M4 y la fija al riel: placa de tapa inclinada 30°, alma y silla en U que abraza el riel. Se imprime ×2. El STEP está en la pose del ensamble (x a lo largo del riel).",
         views=[(40, 25), (215, 35)],
         items=[
             A("union", "Pasos M3 de la tapa", "Cuatro pasos M3 (Ø3.4) en las esquinas de la placa: M3 con tuerca contra M4 ([[M4_capsula_cuerpo:pasos]]). Apretados, comprimen el cordón.",
               dict(D=3.4, ax="d"), key="pasos"),
             A("sello", "Ranura del cordón O-ring (4 esquinas)", "Ranura rectangular de 2.6 × 1.5 mm en la cara interior de la placa, entre la cavidad y los M3. Cordón de goma Ø2. Se marcan sus 4 esquinas (R4).",
               dict(D=10.6, ax="d"), key="groove", tol=3),
             A("union", "M4 de la silla", "Dos M4 (a x = 170 y 200) cruzan las dos mejillas (4 pasos Ø4.2) y el riel por dentro ([[M3s_riel_gancho:silla]]). Sujetan la cápsula al riel.",
               dict(D=4.2, ax="y"), key="silla", tol=3),
             M("forma", "Silla en U sobre el riel", "Dos mejillas y una placa bajo el riel: abrazan el conducto (holgura 0.3 por lado).",
               [(185, 20.3, 22), (185, -20.3, 22)], key="silla_u", tol=4),
             M("forma", "Alma triangular", "Alma en V que lleva el peso de la cápsula al riel; se imprime sin soportes locales. FEM local: factor de seguridad 5.0 (150 N).",
               [(183, 0, -10)], key="alma", tol=1000),
         ]),
    dict(id="M6_capsula_bisel", grupo="Nodo P2", step=NODO / "M6_capsula_bisel.step", titulo="M6 · Bisel de la cápsula",
         sub="Anillo de 2.5 mm que sostiene la ventana de acrílico contra el frente de M4. Pequeño: se imprime ×2 al 40 %.",
         views=[(35, 25)],
         items=[
             A("union", "Pasos de los M2", "Tres agujeros Ø2.4 a 120°: pasan los M2 autorroscantes que se enroscan en los pilotos Ø1.8 de M4 ([[M4_capsula_cuerpo:pilotos]]).",
               dict(D=2.4, ax="x"), key="pasos", tol=2),
             A("sello", "Abertura Ø28", "Abertura de 28 mm: deja ver el lente y el LED a través del acrílico (Ø30). La corona de 1 mm que queda sobre el borde de la ventana la retiene.",
               dict(D=28, ax="x"), key="abertura", tol=2),
         ]),
    dict(id="M11_bandeja", grupo="Nodo P2", step=NODO / "M11_bandeja.step", titulo="M11 · Bandeja inferior",
         sub="Bandeja de 3 mm dentro de la caja seca: sostiene los módulos electrónicos. Se atornilla a los 4 bosses de M1s y lleva 4 postes que reciben la bandeja superior.",
         views=[(40, 40), (40, -40)],
         items=[
             A("union", "Pasos M3 sobre los bosses", "Cuatro pasos M3 (Ø3.4) en las esquinas de la placa, justo bajo los postes: deberían recibir los M3 hacia los insertos de los bosses de M1s ([[M1s_caja_cuerpo:bosses]]). A confirmar: en el STEP el poste es sólido de z = 16 a 36, así que el paso queda tapado y el tornillo no tiene por dónde entrar. Revisar en el CAD.",
               dict(D=3.4, ax="z", z=(10, 20)), key="bosses", tol=2),
             A("mont", "Postes de la bandeja superior", "Cuatro postes con paso M3 (Ø3.4): la bandeja superior M11_sup se atornilla encima.",
               dict(D=3.4, ax="z", z=(30, 45)), key="postes", tol=2),
             A("cable", "Ventana doble Ø27 (en ocho)", "Dos círculos de 27 mm que se juntan. Herencia de la caja anterior con PG7 en el piso (radio de acceso para la llave); hoy solo deja pasar cables hacia el fondo. A confirmar: no tiene función estructural.",
               dict(D=27.32, ax="z"), key="ocho", tol=3),
             M("forma", "Muescas de los extremos", "Muescas en los bordes de la bandeja sobre las contratuercas de los PG7 de las paredes de extremo (+2 mm alrededor de sus esquinas).",
               [(58, 0, 13.5), (-58, 0, 13.5)], key="muescas", tol=4),
         ]),
    dict(id="M11_bandeja_sup", grupo="Nodo P2", step=NODO / "M11_bandeja_sup.step", titulo="M11 · Bandeja superior",
         sub="Segundo piso de la caja seca. Placa de 3 mm que se apoya en los 4 postes de la bandeja inferior.",
         views=[(40, 40)],
         items=[
             A("union", "Pasos M3 de los postes", "Cuatro pasos M3 (Ø3.4): los M3 bajan a los postes de la bandeja inferior ([[M11_bandeja:postes]]).",
               dict(D=3.4, ax="z"), key="postes", tol=2),
         ]),
]

# ----------------------------------------------------------------------------- seals of the current concept
COD = {"B2_cubierta_lisa": "B2 lisa", "B2_cubierta_mastil": "B2 mástil", "B5_cuna_base": "B5 base", "B5_cuna_cuello": "B5 cuello",
       "M11_bandeja": "M11 inferior", "M11_bandeja_sup": "M11 superior"}


def cod(pid):
    return COD.get(pid, pid.split("_")[0])


SELLOS = [
    dict(sello="Tapa B4 sobre la caja seca B3", piezas=["B3_caja", "B4_tapa"], tipo="cordón O-ring Ø2 en ranura",
         protege="La electrónica de la boya: PCB, Waveshare, portabaterías 3×18650 y RTC.",
         refs=[("B4_tapa", "groove"), ("B4_tapa", "pasos"), ("B3_caja", "brida")]),
    dict(sello="PG7 del umbilical en B3 (pared −X)", piezas=["B3_caja"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca",
         protege="El paso del cable umbilical (boya ↔ nodo) hacia la caja seca.", refs=[("B3_caja", "pg7_umb")]),
    dict(sello="PG7 del cable solar en B3 (pared +X)", piezas=["B3_caja"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca",
         protege="El paso del cable del panel solar hacia la caja seca.", refs=[("B3_caja", "pg7_solar")]),
    dict(sello="PG7 del pigtail de antena en B3 (pared +X)", piezas=["B3_caja", "B2_cubierta_mastil"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca",
         protege="El paso del pigtail de la antena hacia la caja seca. El mástil de B2 solo guía el cable: no sella.", refs=[("B3_caja", "pg7_pig"), ("B2_cubierta_mastil", "puerto")]),
    dict(sello="Insertos M3 de la brida de B3", piezas=["B3_caja"], tipo="inserto térmico ciego (no atraviesa la brida)",
         protege="La brida no queda perforada y los tornillos quedan fuera del cordón: el agua no tiene camino por los tornillos.", refs=[("B3_caja", "ins_brida")]),
    dict(sello="Botellas PET selladas (flotación)", piezas=["B1_casco", "B5_cuna_base", "B5_cuna_cuello"], tipo="tapón de rosca de fábrica (botella comprada)",
         protege="El aire que flota la boya. El casco impreso NO es estanco: solo sostiene las botellas.", refs=[("B1_casco", "silla"), ("B1_casco", "cuello"), ("B5_cuna_cuello", "cuello")]),
    dict(sello="Tapa M2 sobre la caja M1s", piezas=["M1s_caja_cuerpo", "M2_caja_tapa"], tipo="cordón O-ring Ø2 en ranura",
         protege="La electrónica del nodo (bandejas M11) en la caja seca.", refs=[("M2_caja_tapa", "groove"), ("M2_caja_tapa", "pasos"), ("M1s_caja_cuerpo", "brida")]),
    dict(sello="PG7 de cada cámara en las paredes de extremo de M1s (×2)", piezas=["M1s_caja_cuerpo", "M3s_riel_gancho"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca",
         protege="El paso del Cat5e de cada cámara a la caja seca. El conducto del riel va inundado: el sello es el PG7, no el riel.", refs=[("M1s_caja_cuerpo", "pg7"), ("M3s_riel_gancho", "dome")]),
    dict(sello="PG7 del umbilical en la tapa M2", piezas=["M2_caja_tapa"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca",
         protege="El paso del umbilical hacia la caja seca del nodo.", refs=[("M2_caja_tapa", "pg7")]),
    dict(sello="Insertos M3 de la brida de M1s y M4 del cojín", piezas=["M1s_caja_cuerpo"], tipo="inserto térmico ciego",
         protege="No perforan la caja: los 12 M3 de la tapa quedan fuera del cordón y los 8 M4 del cojín no pasan la pared.", refs=[("M1s_caja_cuerpo", "ins_brida"), ("M1s_caja_cuerpo", "m4")]),
    dict(sello="Tapa M5s sobre la cápsula M4 (×2 cápsulas)", piezas=["M4_capsula_cuerpo", "M5s_capsula_tapa_pie"], tipo="cordón O-ring Ø2 en ranura",
         protege="La cámara Arducam y el anillo LED dentro de cada cápsula.", refs=[("M5s_capsula_tapa_pie", "groove"), ("M5s_capsula_tapa_pie", "pasos"), ("M4_capsula_cuerpo", "pasos")]),
    dict(sello="PG7 de cada cápsula en M4 (×2)", piezas=["M4_capsula_cuerpo"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca",
         protege="El paso del Cat5e hacia el interior de la cápsula (cámara y LED).", refs=[("M4_capsula_cuerpo", "pg7")]),
    dict(sello="Ventana de acrílico M7 en el frente de M4 (×2)", piezas=["M4_capsula_cuerpo", "M6_capsula_bisel"], tipo="asiento Ø30.4 con sellador (a definir)",
         protege="El frente de la cápsula: la ventana deja pasar la luz y no el agua. A confirmar: el CAD solo define el asiento y el bisel M6 con 3 M2; no hay sellador especificado.", refs=[("M4_capsula_cuerpo", "asiento"), ("M6_capsula_bisel", "abertura"), ("M6_capsula_bisel", "pasos")]),
]
NO_ESTANCO = [
    "Conducto del riel M3s: va inundado a propósito (el Cat5e tiene chaqueta exterior y entra por PG7 a la caja y a la cápsula).",
    "Unión riel ↔ caja (4 M4) y pie M5s ↔ riel (2 M4): atornilladas, no estancas.",
    "Bolsillos de lastre de M1s y sus tapas M3t: fuera del sello, entra agua.",
    "Casco B1, cunas B5, correas B6 y cubierta B2 de la boya: estructura abierta; flotan las botellas.",
]


# ----------------------------------------------------------------------------- build
def build_items(p, debug=False):
    """Detect holes, apply the item list. Returns (items, instances, unmatched)."""
    shp, sol, mesh = load(p["step"])
    inst = hole_instances(shp, sol)
    used = set()
    items = []
    spec_items = p["items"]
    if debug:
        spec_items = [A("union", "candidato", f"candidato {i}", dict(D=h["D"], ax=h["ax"], x=(h["ctr"][0] - .3, h["ctr"][0] + .3), y=(h["ctr"][1] - .3, h["ctr"][1] + .3), z=(h["ctr"][2] - .3, h["ctr"][2] + .3))) for i, h in enumerate(inst)]
    for it in spec_items:
        hit = [i for i, h in enumerate(inst) if i not in used and any(match(h, s) for s in it["spec"])] if (it.get("auto") or it.get("ignore")) else []
        used.update(hit)
        if it.get("ignore"):
            continue
        n = len(items) + 1
        if it["auto"]:
            hs = [inst[i] for i in hit]
            if not hs:
                print(f"  AVISO {p['id']}: '{it['tipo']}' no encontró agujeros")
                continue
            diam = "/".join(sorted({(f"{h['D']:.1f}" if h["D"] < 10 else f"{h['D']:g}") for h in hs}))
            items.append(dict(n=n, cat=it["cat"], tipo=it["tipo"], diam=diam, texto=it["texto"], key=it["key"], tol=it["tol"], holes=hs,
                              puntos=[tuple(np.round(h["ctr"], 1)) for h in hs]))
        else:
            items.append(dict(n=n, cat=it["cat"], tipo=it["tipo"], diam=it["diam"], texto=it["texto"], key=it["key"], tol=it["tol"], holes=None, puntos=it["puntos"]))
    left = [inst[i] for i in range(len(inst)) if i not in used]
    return items, mesh, left


def anchors_for(it, v):
    """3D points of an item to draw in view v, with a depth test."""
    out = []
    if it["holes"] is not None:
        for h in it["holes"]:
            sgn = 1.0 if float(np.dot(h["a"], v.d)) >= 0 else -1.0
            P = h["ctr"] + h["a"] * sgn * h["len"] / 2
            if it["tol"] >= 1000 or v.visible(P, 1.6 + it["tol"]):
                out.append(P)
    else:
        for P in it["puntos"]:
            if it["tol"] >= 1000 or v.visible(P, it["tol"]):
                out.append(np.array(P))
    return out


def resolve_refs(text, cur, numbers):
    def rep(m):
        pid, key = m.group(1), m.group(2)
        n = numbers.get((pid, key))
        if n is None:
            raise KeyError(f"referencia {pid}:{key} sin resolver")
        return f"N° {n}" if pid == cur else f"N° {n} de {cod(pid)}"
    import re
    return re.sub(r"\[\[([A-Za-z0-9_]+):([A-Za-z0-9_]+)\]\]", rep, text)


def cover_figure(piezas, pages):
    fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
    fig.text(0.05, 0.92, "LanternGuard · Guía de piezas", fontsize=26, fontweight="bold")
    fig.text(0.05, 0.875, "Qué es cada agujero y cada forma de las piezas impresas de la boya y del nodo de cámaras (prototipo P2).", fontsize=11, color="#333333")
    fig.text(0.05, 0.83, "Cómo leer la guía", fontsize=14, fontweight="bold")
    lines = [
        "• Cada hoja es una pieza. El dibujo muestra la pieza en 3D con círculos numerados; la lista de la derecha dice qué es cada número.",
        "• Un mismo número con varios puntos (×n) es el mismo tipo de agujero repetido; se numera una sola vez.",
        "• Los colores agrupan: azul = tornillo o unión · naranja = por donde pasa un cable · rojo = sello (agua) · verde = forma o ahorro de material ·",
        "   morado = alineación · gris = montaje de piezas internas.",
        "• Ø = diámetro en mm. M3 de paso = Ø3.4 (el tornillo pasa libre) · inserto M3 = Ø4.0 (inserto térmico, se funde con soldador) ·",
        "   M4 de paso = Ø4.2 · inserto M4 = Ø5.6 · piloto M2 = Ø1.8 · prensaestopas PG7 = Ø12.6 · cordón O-ring = Ø2 en ranura de 2.6 × 1.5.",
        "• Si una hoja tiene dos vistas (A y B), algunos rasgos solo se ven desde la otra cara. Los puntos pequeños sin número son repeticiones del mismo rasgo.",
        "• Las referencias \"N° 3 de B1\" remiten a la hoja y número de esa pieza.",
        "• Las piezas \"×2\" o \"×4\" se imprimen varias veces. Las piezas simétricas (mitades) son la misma pieza girada.",
    ]
    for i, l in enumerate(lines):
        fig.text(0.05, 0.795 - i * 0.034, l, fontsize=8.8)
    fig.text(0.05, 0.47, "Piezas", fontsize=14, fontweight="bold")
    y = 0.435
    for grp in ("Boya", "Nodo P2"):
        fig.text(0.05, y, "Boya con botellas PET" if grp == "Boya" else "Nodo de cámaras P2_robusto", fontsize=9.5, fontweight="bold", color="#1f5fbf")
        y -= 0.026
        for p in [q for q in piezas if q["grupo"] == grp]:
            fig.text(0.06, y, f"{p['titulo']}", fontsize=8.3)
            fig.text(0.40, y, f"pág. {pages[p['id']]}", fontsize=8.3, color="#555555")
            y -= 0.0205
        y -= 0.01
    fig.text(0.55, 0.47, "Estado", fontsize=14, fontweight="bold")
    est = ["Concepto vigente antes de la corrección 3a: los rasgos que dependen del", "riel y del cable (M1s, M3s) cambian con la corrección de concepto", "(riel cerrado estanco, cable por dentro): pendiente.", "",
           "Lista de sellos: docs/ESTANQUEIDAD.md.", "Texto de esta guía: docs/GUIA_PIEZAS.md.", f"Generada el {datetime.date.today().isoformat()} con cad_final/guia_piezas.py."]
    for i, l in enumerate(est):
        fig.text(0.55, 0.435 - i * 0.026, l, fontsize=8.8)
    return fig


def md_piece(p, items):
    out = [f"## {p['titulo']}", "", p["sub"], "", f"![{p['id']}](../salida/guia_piezas/{p['id']}.png)", ""]
    for it in items:
        d = f" Ø{it['diam']}" if it["diam"] else ""
        k = f" ×{len(it['puntos'])}" if len(it["puntos"]) > 1 else ""
        out.append(f"{it['n']}. **{it['tipo']}**{d}{k} _({CATS[it['cat']][1]})_. {it['texto']}")
    out.append("")
    return out


def main():
    ap = argparse.ArgumentParser(description="Guía de piezas: PNG/PDF por pieza, PDF único, MD, JSON y ESTANQUEIDAD.md")
    ap.add_argument("--solo", help="id de una pieza (solo su PNG/PDF)")
    ap.add_argument("--debug", help="id de una pieza: numera todos los agujeros detectados (PNG en el directorio temporal del sistema)")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    import matplotlib.backends.backend_pdf as bpdf
    todo = [p for p in PIEZAS if not a.solo or p["id"] == a.solo]
    if a.debug:
        p = next(q for q in PIEZAS if q["id"] == a.debug)
        items, mesh, left = build_items(p, debug=True)
        for it in items:
            h = it["holes"][0]
            print(f"{it['n']-1:3d} D={h['D']:<5g} {h['ax']} ctr=({h['ctr'][0]:.1f},{h['ctr'][1]:.1f},{h['ctr'][2]:.1f}) len={h['len']:.1f}")
        import tempfile
        views = [View(mesh, *vw) for vw in p["views"]]
        for it in items:
            it["vis"] = {vi: anchors_for(it, v) for vi, v in enumerate(views)}
            it["texto"] = ""
        tmp = Path(tempfile.gettempdir()) / f"guia_debug_{p['id']}.png"
        draw_sheet(str(tmp), None, p["id"], items, views, dict(titulo=p["titulo"], sub="debug", pie="", pagina=""))
        print("debug ->", tmp)
        return
    built = {}
    for p in PIEZAS:
        print("detectando", p["id"])
        items, mesh, left = build_items(p)
        built[p["id"]] = (items, mesh)
        for h in left:
            print(f"  SIN CLASIFICAR {p['id']}: D={h['D']:g} {h['ax']} ctr=({h['ctr'][0]:.1f},{h['ctr'][1]:.1f},{h['ctr'][2]:.1f}) len={h['len']:.1f}")
    numbers = {(pid, it["key"]): it["n"] for pid, (items, _m) in built.items() for it in items if it["key"]}
    for p in PIEZAS:
        for it in built[p["id"]][0]:
            it["texto"] = resolve_refs(it["texto"], p["id"], numbers)
    pages = {p["id"]: i + 2 for i, p in enumerate(PIEZAS)}
    npag = len(PIEZAS) + 1
    pp = None if a.solo else bpdf.PdfPages(str(DOCS / "GUIA_PIEZAS_LanternGuard.pdf"))
    if pp:
        cf = cover_figure(PIEZAS, pages)
        cf.text(0.975, 0.018, f"1 / {npag}", fontsize=6.5, color="#777777", ha="right")
        pp.savefig(cf)
        plt.close(cf)
    rasgos = {}
    for p in todo:
        items, mesh = built[p["id"]]
        print("dibujando", p["id"], len(items), "rasgos")
        views = [View(mesh, *vw) for vw in p["views"]]
        for it in items:
            it["vis"] = {vi: anchors_for(it, v) for vi, v in enumerate(views)}
            if not any(it["vis"].values()):
                print(f"  AVISO {p['id']} N° {it['n']} '{it['tipo']}': no se ve en ninguna vista")
                it["vis"][0] = [np.array(q) for q in it["puntos"]]
        hdr = dict(titulo=p["titulo"], sub=p["sub"], pie=datetime.date.today().isoformat(), pagina=f"{pages[p['id']]} / {npag}")
        fig = draw_sheet(str(OUT / f"{p['id']}.png"), str(OUT / f"{p['id']}.pdf"), p["id"], items, views, hdr)
        if pp:
            pp.savefig(fig)
        plt.close(fig)
        rasgos[p["id"]] = [dict(n=it["n"], tipo=it["tipo"], diam=it["diam"], texto=it["texto"], punto=[float(x) for x in it["puntos"][0]],
                                puntos=[[float(x) for x in q] for q in it["puntos"]], categoria=it["cat"]) for it in items]
    if pp:
        pp.close()
    if a.solo:
        print("listo (solo)")
        return
    (OUT / "rasgos.json").write_text(json.dumps(rasgos, ensure_ascii=False, indent=1), encoding="utf-8")
    # seals
    sellos = []
    for i, s in enumerate(SELLOS, 1):
        donde = [f"{cod(pid)} N° {numbers[(pid, key)]}" for pid, key in s["refs"]]
        sellos.append(dict(n=i, sello=s["sello"], piezas=s["piezas"], tipo=s["tipo"], protege=s["protege"], donde=donde))
    (OUT / "sellos.json").write_text(json.dumps(sellos, ensure_ascii=False, indent=1), encoding="utf-8")
    md = ["# Estanqueidad: sellos del concepto vigente", "",
          "> **Concepto vigente antes de la corrección 3a; se actualiza cuando llegue.**", "",
          "Lista de lo que mantiene seco cada volumen. Los números de la última columna son los de `GUIA_PIEZAS_LanternGuard.pdf` / `GUIA_PIEZAS.md`. Se genera con `cad_final/guia_piezas.py`; datos en `salida/guia_piezas/sellos.json`.", "",
          "| N° | Sello | Piezas | Tipo | Qué protege | Dónde lo ves en la guía |", "|---|---|---|---|---|---|"]
    for s in sellos:
        md.append(f"| {s['n']} | {s['sello']} | {', '.join(cod(x) for x in s['piezas'])} | {s['tipo']} | {s['protege']} | {'; '.join(s['donde'])} |")
    md += ["", "## Lo que NO es estanco a propósito", ""] + [f"- {x}" for x in NO_ESTANCO]
    md += ["", "## Pendiente", "", "- Sellador o junta de la ventana M7: no está especificado en el CAD.",
           "- Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): el conducto del riel y los PG7 de M1s/M3s se rehacen.", ""]
    (DOCS / "ESTANQUEIDAD.md").write_text("\n".join(md), encoding="utf-8")
    g = ["# Guía de piezas LanternGuard", "", "> Texto de `GUIA_PIEZAS_LanternGuard.pdf`. Los números coinciden con los de los PNG de `salida/guia_piezas/`.",
         "> Concepto vigente antes de la corrección 3a (lo del riel y del cable en M1s y M3s cambia con ella).", "",
         "Colores en los PNG: azul = tornillo / unión · naranja = cable · rojo = sello · verde = forma / ahorro de material · morado = alineación · gris = montaje interno.",
         "Medidas: M3 de paso Ø3.4 · inserto M3 Ø4.0 · M4 de paso Ø4.2 · inserto M4 Ø5.6 · piloto M2 Ø1.8 · PG7 Ø12.6 · cordón O-ring Ø2 en ranura de 2.6 × 1.5.",
         "Regenerar: `cd cad_final && ..\\.venv\\Scripts\\python.exe guia_piezas.py`.", ""]
    for grp, ttl in (("Boya", "Boya con botellas PET"), ("Nodo P2", "Nodo de cámaras P2_robusto")):
        g += [f"# {ttl}", ""]
        for p in [q for q in PIEZAS if q["grupo"] == grp]:
            g += md_piece(p, built[p["id"]][0])
    (DOCS / "GUIA_PIEZAS.md").write_text("\n".join(g), encoding="utf-8")
    print(f"listo: {npag} páginas")


if __name__ == "__main__":
    main()
