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
CABLE_RUTA = ("Camino completo, todo en seco: dentro de la caja M1s → ventana de la pared de extremo → canal del riel M3s → "
              "curva de radio 10 → abertura bajo el riel → conducto de M5s → ranura de la tapa de la cápsula → cámara.")
PIEZAS += [
    dict(id="M1s_caja_cuerpo", grupo="Nodo P2", step=NODO / "M1s_caja_cuerpo.step", titulo="M1s · Caja del nodo (cuerpo)",
         sub="Caja seca del nodo (127 × 126 × 77 mm). La caja, los dos rieles y las dos cápsulas forman UN solo volumen seco: el cable plano de cada cámara va por dentro, sin prensaestopas. "
             "Cada extremo tiene una ventana al canal del riel. Abajo, los bolsillos de lastre. La cierra la tapa M2. x a lo largo de los rieles, z arriba.",
         views=[(60, 30), (215, -35)],
         items=[
             IGN(dict(D=2.0, ax="x")),
             IGN(dict(D=6.0, ax="z", len=(30, 100))),
             M("cable", "Recorrido del cable (resumen)", "El cable plano de cada cámara NO sale de la caja por un prensaestopas. " + CABLE_RUTA + " "
               "Aquí empieza: el cable sale de la electrónica, llega a la ventana ([[M1s_caja_cuerpo:ventana]]) y entra al riel ([[M3s_riel_gancho:canal]]). Ya no hay PG7 entre la caja y la cápsula; el único PG7 que queda en el nodo es el del umbilical, en la tapa M2.",
               [(0, 0, 40)], key="ruta", tol=1000),
             M("forma", "Cojín rectangular de la pared", "En cada pared de extremo hay una placa en relieve de 10 mm de espesor y 50 mm de ancho. Da un asiento plano a la brida del riel y refuerza la pared donde se rosca. "
               "Lleva la ventana ([[M1s_caja_cuerpo:ventana]]) y 4 insertos ciegos ([[M1s_caja_cuerpo:m4]]). Hay uno por extremo (×2). Antes tenía un agujero redondo Ø30 y un PG7: ya no.",
               [(73.6, -21, 30.5), (-73.6, 21, 30.5)], key="cojin", tol=3),
             M("cable", "Ventana redondeada de 24 × 18 al riel", "Ventana rectangular con esquinas redondeadas (R1) que atraviesa la pared y el cojín: la caja queda abierta al canal del riel, sin tapa ni cable de por medio. El cable plano pasa por aquí. "
               "Se sella con el cordón de goma plano de la brida del riel ([[M3s_riel_gancho:oring]]), que rodea la ventana. Una por extremo (×2).",
               [(73.5, 0, 13.7), (-73.5, 0, 13.7)], key="ventana", tol=3),
             A("union", "Insertos M4 del cojín", "Cuatro insertos térmicos M4 (Ø5.6 × 8.5) por cojín, en cuadro de 40 × 20 mm, alrededor de la ventana. Reciben los 4 tornillos M4 de la brida del riel ([[M3s_riel_gancho:m4]]) y aprietan el cordón plano. Ciegos: no perforan la pared.",
               dict(D=5.6, ax="x"), key="m4", tol=2),
             A("sello", "Insertos M3 de la brida", "Doce insertos térmicos M3 (Ø4.0 × 6) en la brida: los 12 tornillos de la tapa M2 los aprietan y comprimen el cordón O-ring. Ciegos y fuera del cordón.",
               dict(D=4.0, ax="z", z=(60, 80)), key="ins_brida", tol=2),
             M("sello", "Brida plana: asiento del cordón", "La cara superior de la brida es plana: contra ella aprieta el cordón de goma Ø2 que va en la ranura de la tapa M2 (ver [[M2_caja_tapa:groove]]).",
               [(0, -69, 77), (0, 69, 77)], key="brida", tol=3),
             M("forma", "Falda a 45° bajo la brida", "El paso del cuerpo a la brida es un chaflán a 45°: se imprime sin soportes.",
               [(0, -68, 66), (-68, 0, 66)], key="falda", tol=5),
             A("mont", "Insertos M3 de los bosses de la bandeja", "Cuatro bosses Ø8 sobre el piso con inserto M3 (ciego). Un solo tornillo M3 × 38 de acero inoxidable por boss atraviesa la bandeja superior, el poste y la bandeja inferior y se enrosca aquí ([[M11_bandeja:postes]]). Cada boss nace del piso con un chaflán de 45°.",
               dict(D=4.0, ax="z", z=(5, 15)), key="bosses", tol=3),
             A("union", "Insertos M3 de los bolsillos", "Cuatro insertos M3 (Ø4.0) en el fondo de los bolsillos (2 por bolsillo): ahí se atornillan los M3 avellanados de la tapa M3t.",
               dict(D=4.0, ax="z", z=(-40, -10)), key="ins_m3t", tol=3),
             M("forma", "Bolsillos de lastre", "Dos cajones de 100 × 50 × 30 mm bajo el piso (uno por lado), abiertos por abajo y fuera del sello. Llevan las tuercas y arandelas M8 a granel (575 g por bolsillo, 1150 g en total) y se cierran con M3t. Entra agua: es lo normal.",
               [(0, 29.5, -14), (0, -29.5, -14)], key="bolsillos", tol=6),
         ]),
    dict(id="M2_caja_tapa", grupo="Nodo P2", step=NODO / "M2_caja_tapa.step", titulo="M2 · Tapa de la caja con asa",
         sub="Cierra la caja M1s. Lleva el asa para cargar con guante, el ojo de anclaje del cabo y el PG7 del umbilical, que es el único prensaestopas que queda en el nodo. Se imprime girada (Y+90). Aquí z crece hacia arriba (asa arriba).",
         views=[(40, 35), (40, -40)],
         items=[
             IGN(dict(D=6.0, ax="y")),
             A("union", "Pasos M3 de la tapa", "Doce pasos M3 (Ø3.4): los tornillos entran a los doce insertos de la brida de M1s ([[M1s_caja_cuerpo:ins_brida]]) y aprietan el cordón.",
               dict(D=3.4, ax="z"), key="pasos"),
             A("sello", "Ranura del cordón O-ring (4 esquinas)", "Ranura rectangular de 2.6 × 1.5 mm en la cara inferior, a mitad de camino entre la cavidad y la línea de tornillos. Cordón de goma Ø2. Se marcan las 4 esquinas redondeadas (R6); la ranura sigue el contorno.",
               dict(D=12, ax="z"), key="groove", tol=2),
             A("cable", "PG7 del umbilical", "Agujero Ø12.6 en la tapa: entra el cable umbilical que sube a la boya (cable flojo, con curva). Prensaestopas con contratuerca por dentro. Es el único PG7 del nodo.",
               dict(D=12.6, ax="z"), key="pg7", tol=2),
             A("union", "Ojo de anclaje Ø10", "Ojo Ø10 en lo alto del asa, con eje en Y: aquí se amarra el cabo que sube a la linterna / línea larga.",
               dict(D=10, ax="y"), key="ojo", tol=3),
             M("forma", "Asa en arco", "Asa de 12 mm de grosor con apertura para guante. El techo de la ventana va a 45° para imprimir sin soportes.",
               [(-25, 6, 122), (-47, 6, 92)], key="asa", tol=5),
         ]),
    dict(id="M3s_riel_gancho", grupo="Nodo P2", step=NODO / "M3s_riel_gancho.step", titulo="M3s · Riel cerrado con gancho (una mitad)",
         sub="Ahora es una caja cerrada y seca de 36 × 30 mm que sale de la caja M1s y lleva el cable plano hasta la cápsula; ya no es una celosía abierta. Una mitad por lado; la otra es la misma pieza girada 180° sobre z. "
             "El gancho en C, fundido al riel, cuelga el nodo del aro de la linterna.",
         views=[(215, 25), (35, -35)],
         items=[
             IGN(dict(D=2.0, ax="x", len=(100, 130))),
             IGN(dict(D=20.8, ax="y")),
             M("cable", "Recorrido del cable (resumen)", "El cable plano de la cámara va por dentro del riel, seco. " + CABLE_RUTA + " "
               "Ya no hay prensaestopas PG7 en el riel ni en la caja: el cable pasa de una pieza a otra por aberturas selladas con cordón plano. Puntos marcados: boca del canal en la brida, canal, y abertura bajo el riel.",
               [(73.5, 0, 13.7), (140, 0, 13.7), (185, 0, -4.3)], key="ruta", tol=1000),
             M("cable", "Canal interior seco 24 × 18", "El riel es un tubo cerrado de 36 × 30 mm de afuera. Por dentro, un canal de 24 × 18 mm con esquinas redondeadas (R1) y un piso plano de 22 mm donde se apoya el cable plano. Paredes de 6 mm, sin ventanas. Es parte del volumen seco: el agua no entra.",
               [(140, 0, 13.7)], key="canal", tol=1000),
             M("forma", "Punta cerrada", "El extremo del riel está cerrado con pared de 6 mm (antes tenía un agujero Ø8 para el cable): el cable no sale por aquí, baja por la abertura de abajo ([[M3s_riel_gancho:abertura]]).",
               [(213, 0, 13.7)], key="punta", tol=5),
             A("sello", "Ranura del cordón plano (4 esquinas)", "Ranura en la cara de la brida (la que mira a la caja), alrededor de la boca del canal: 2.6 mm de ancho × 1.6 de hondo. Lleva un cordón de goma Ø2 en forma de marco (NBR, se comprime 20 %). Al apretar los 4 M4 contra el cojín de la caja, el cordón sella la unión riel ↔ caja ([[M1s_caja_cuerpo:ventana]]). Se marcan las 4 esquinas redondeadas; la ranura sigue el contorno.",
               dict(D=10.2, ax="x"), key="oring", tol=3),
             A("union", "Pasos M4 de la brida", "Cuatro pasos M4 (Ø4.2) en la brida de 25 mm de ancho: los 4 tornillos M4 que atan el riel al cojín de la caja ([[M1s_caja_cuerpo:m4]]) y comprimen el cordón plano ([[M3s_riel_gancho:oring]]).",
               dict(D=4.2, ax="x", x=(60, 90)), key="m4", tol=3),
             M("cable", "Abertura de 8 × 22 hacia la cápsula", "Abertura rectangular de 8 × 22 mm en el piso del riel, cerca de la punta: por aquí el cable plano baja del canal hacia la cápsula. El borde de entrada está redondeado (radio 10) para que el cable no se doble de golpe. Rodeada por el cordón plano de M5s ([[M5s_capsula_tapa_pie:oring_riel]]).",
               [(185, 0, -7.3)], key="abertura", tol=3),
             M("forma", "Almohadilla de 6 mm bajo el riel", "Placa de 50 × 50 × 6 mm bajo el riel, cerca de la punta. Es el asiento plano de la silla de M5s. Sus alas (7 mm a cada lado del riel) llevan los pasos M3 ([[M3s_riel_gancho:pad_m3]]): los tornillos quedan FUERA del canal, no lo perforan.",
               [(185, -25, -4.3)], key="almohadilla", tol=4),
             A("union", "Pasos M3 de la almohadilla", "Cuatro pasos M3 (Ø3.4) en las alas de la almohadilla, en cuadro de 34 × 40 mm: tornillos M3 que bajan a los 4 insertos ciegos de la silla de M5s ([[M5s_capsula_tapa_pie:inserts]]).",
               dict(D=3.4, ax="z"), key="pad_m3", tol=3),
             A("forma", "Rebajes Ø6.5 para las cabezas", "Cuatro rebajes redondos Ø6.5 junto a cada paso M3: dejan hueco para la cabeza del tornillo y la llave.",
               dict(D=6.5, ax="z"), key="rebajes", tol=3),
             A("union", "Asiento en C del gancho", "C abierta de Ø8.8 (varilla del aro Ø8 + 0.4 de holgura): el nodo cae sobre la varilla del aro de la linterna. El alma del gancho (26 mm de ancho) está fundida al riel y lleva una ranura para una correa de 25 × 3.",
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
         sub="Caja seca de la cámara Arducam Mega 5 MP, con anillo LED y ventana de acrílico. Ya no tiene prensaestopas: el cable plano entra por una ranura de la tapa M5s. Brida de 4 mm que se cierra con la tapa M5s. Hay una por lado (×2). x es el eje óptico (adelante = +x).",
         views=[(35, 25), (215, 25)],
         items=[
             IGN(dict(D=4.0, ax="x", len=(30, 50))),
             A("union", "Pasos M3 de la brida", "Cuatro pasos M3 (Ø3.4) en las esquinas de la brida: M3 con tuerca unen la tapa M5s y aprietan el cordón O-ring Ø2 ([[M5s_capsula_tapa_pie:groove]]).",
               dict(D=3.4, ax="x"), key="pasos"),
             A("sello", "Asiento de la ventana Ø30.4 (3.8 de hondo)", "Rebaje frontal para el disco de acrílico M7 (Ø30 × 3). Ahora es más hondo (3.8 mm, antes 3.2) para alojar también la junta plana de silicona de 1 mm (Ø30 × Ø26.5) que va debajo del disco. El bisel M6 comprime la junta un 20 % y un cordón de silicona marina alrededor del borde del disco termina el sello.",
               dict(D=30.4, ax="x"), key="asiento", tol=3),
             M("forma", "Apertura anular del LED con 3 radios", "Anillo de luz Ø26 alrededor del lente: deja salir la luz del anillo LED (Ø30 × 3, pegado a la cara interior). Tres radios de 2 mm sujetan el tubo opaco que impide que el LED ilumine el lente por dentro.",
               [(65, 0, -11)], key="anillo", tol=3),
             A("forma", "Orificio del lente Ø16.4", "Agujero central: por aquí mira el porta-lente Ø16 de la cámara. Lo rodea un tubo separador opaco (pared 1.2).",
               dict(D=16.4, ax="x"), key="lente", tol=3),
             A("union", "Pilotos M2 del bisel", "Tres agujeros ciegos Ø1.8 × 4 mm: tornillos M2 autorroscantes del bisel M6.",
               dict(D=1.8, ax="x"), key="pilotos", tol=2),
             M("mont", "Cavidad 38 × 38 × 38 (seca)", "Aloja la cámara (33 × 33 × 17), el anillo LED y, detrás, una zona libre para el bucle del cable plano. El cable llega por la ranura de la tapa M5s ([[M5s_capsula_tapa_pie:ranura]]); ya no hay agujero ni PG7 en la pared de la cápsula. Es parte del volumen seco.",
               [(45, 0, 0)], key="cavidad", tol=1000),
         ]),
    dict(id="M5s_capsula_tapa_pie", grupo="Nodo P2", step=NODO / "M5s_capsula_tapa_pie.step", titulo="M5s · Tapa de la cápsula con pie",
         sub="Cierra la cápsula M4, la fija bajo el riel y lleva el cable plano desde el riel hasta la cámara por un conducto interior. Placa de silla de 10 mm bajo el riel, alma de 30 mm de ancho con el conducto, y tapa inclinada 30° con una ranura para el cable. "
             "Se imprime ×2. El STEP está en la pose del ensamble (x a lo largo del riel).",
         views=[(40, 25), (215, 35)],
         items=[
             M("cable", "Recorrido del cable (resumen)", "Aquí termina el recorrido del cable plano: " + CABLE_RUTA + " "
               "En esta pieza: abertura de la placa ([[M5s_capsula_tapa_pie:abertura]]) → conducto del alma ([[M5s_capsula_tapa_pie:conducto]]) → ranura de la tapa ([[M5s_capsula_tapa_pie:ranura]]) → cápsula.",
               [(185, 0, -7.3), (180, 0, -25), (173.7, 0, -48.3)], key="ruta", tol=1000),
             A("sello", "Ranura del cordón plano (4 esquinas)", "Ranura de 2.6 × 1.6 mm en la cara de arriba de la placa, alrededor de la abertura del cable. Lleva un cordón de goma Ø2 en forma de marco (se comprime 20 %): sella la unión con la almohadilla del riel ([[M3s_riel_gancho:almohadilla]]). Se marcan las 4 esquinas.",
               dict(D=10.2, ax="z"), key="oring_riel", tol=3),
             M("cable", "Abertura de 8 × 22 de la placa", "Abertura rectangular en la placa de silla, justo bajo la del riel ([[M3s_riel_gancho:abertura]]): el cable plano entra aquí desde el canal.",
               [(185, 0, -7.3)], key="abertura", tol=3),
             A("union", "Insertos M3 ciegos de la placa", "Cuatro insertos térmicos M3 (Ø4.0 × 6), ciegos, en cuadro de 34 × 40 mm: reciben los M3 que bajan de la almohadilla del riel ([[M3s_riel_gancho:pad_m3]]). Al ser ciegos no atraviesan la placa. Ya no hay M4 horizontales ni mejillas laterales.",
               dict(D=4.0, ax="z"), key="inserts", tol=3),
             M("cable", "Conducto interior del alma", "El alma (30 mm de ancho) es hueca: por dentro corre un conducto de 22 mm de ancho que lleva el cable plano desde la abertura de la placa hasta la tapa, sin curvas cerradas. Es parte del volumen seco.",
               [(180, 0, -25)], key="conducto", tol=1000),
             M("cable", "Ranura de 8 × 22 de la tapa", "Ranura rectangular en la tapa (que ahora tiene 6 mm de espesor): el cable plano sale del conducto y entra a la cápsula por aquí, hacia la cámara. Sustituye al antiguo PG7 de la cápsula.",
               [(173.7, 0, -48.3)], key="ranura", tol=3),
             A("union", "Pasos M3 de la tapa", "Cuatro pasos M3 (Ø3.4) en las esquinas de la placa: M3 con tuerca contra M4 ([[M4_capsula_cuerpo:pasos]]). Apretados, comprimen el cordón.",
               dict(D=3.4, ax="d"), key="pasos"),
             A("sello", "Ranura del cordón O-ring de la tapa (4 esquinas)", "Ranura rectangular de 2.6 × 1.5 mm en la cara interior de la tapa, entre la cavidad y los M3. Cordón de goma Ø2. Se marcan sus 4 esquinas (R4).",
               dict(D=10.6, ax="d"), key="groove", tol=3),
             M("forma", "Alma triangular", "Alma que lleva el peso de la cápsula al riel; se imprime sin soportes locales. El análisis de resistencia (FEM) se repite con esta forma nueva.",
               [(180, -15, -30)], key="alma", tol=1000),
         ]),
    dict(id="M6_capsula_bisel", grupo="Nodo P2", step=NODO / "M6_capsula_bisel.step", titulo="M6 · Bisel de la cápsula",
         sub="Anillo de 2.5 mm que sostiene la ventana de acrílico contra el frente de M4 y comprime la junta plana de silicona. Pequeño: se imprime ×2 al 40 %.",
         views=[(35, 25)],
         items=[
             A("union", "Pasos de los M2", "Tres agujeros Ø2.4 a 120°: pasan los M2 autorroscantes que se enroscan en los pilotos Ø1.8 de M4 ([[M4_capsula_cuerpo:pilotos]]). Al apretarlos, el bisel comprime un 20 % la junta de silicona.",
               dict(D=2.4, ax="x"), key="pasos", tol=2),
             A("sello", "Abertura Ø28", "Abertura de 28 mm: deja ver el lente y el LED a través del acrílico (Ø30). La corona de 1 mm que queda sobre el borde de la ventana la retiene contra la junta plana de silicona de 1 mm (Ø30 × Ø26.5); un cordón de silicona marina alrededor del borde del disco completa el sello.",
               dict(D=28, ax="x"), key="abertura", tol=2),
         ]),
    dict(id="M11_bandeja", grupo="Nodo P2", step=NODO / "M11_bandeja.step", titulo="M11 · Bandeja inferior",
         sub="Bandeja de 3 mm dentro de la caja seca: sostiene los módulos electrónicos. Lleva 4 postes que además son separadores: un solo tornillo M3 × 38 inoxidable por esquina atraviesa la bandeja superior, el poste y esta bandeja y se enrosca en el inserto de M1s.",
         views=[(40, 40), (40, -40)],
         items=[
             A("union", "Postes con paso M3 pasante (separador)", "Cuatro postes huecos con paso M3 (Ø3.4) de lado a lado, 30 mm de largo contando la placa. Un tornillo M3 × 38 de acero inoxidable entra por la bandeja superior, baja por el poste, cruza esta bandeja y se enrosca en el inserto del boss de M1s ([[M1s_caja_cuerpo:bosses]]). Así un solo tornillo fija las dos bandejas a la caja.",
               dict(D=3.4, ax="z", z=(20, 35)), key="postes", tol=2),
             M("forma", "Placa lisa de 3 mm", "La ventana en forma de ocho ya no existe: servía para llegar a prensaestopas en el piso, que esta caja no tiene. Tampoco hay muescas en los extremos, porque ya no hay contratuercas de PG7 en las paredes.",
               [(0, 0, 13.5)], key="placa", tol=3),
         ]),
    dict(id="M11_bandeja_sup", grupo="Nodo P2", step=NODO / "M11_bandeja_sup.step", titulo="M11 · Bandeja superior",
         sub="Segundo piso de la caja seca. Placa de 3 mm que se apoya en los 4 postes de la bandeja inferior; el mismo tornillo M3 × 38 de cada esquina las une a las dos con la caja.",
         views=[(40, 40)],
         items=[
             A("union", "Pasos M3 de los postes", "Cuatro pasos M3 (Ø3.4): por cada uno entra la cabeza de un tornillo M3 × 38 inoxidable que baja por el poste de la bandeja inferior ([[M11_bandeja:postes]]) hasta el inserto de M1s.",
               dict(D=3.4, ax="z"), key="postes", tol=2),
         ]),
]

# ----------------------------------------------------------------------------- seals of the current concept
COD = {"B2_cubierta_lisa": "B2 lisa", "B2_cubierta_mastil": "B2 mástil", "B5_cuna_base": "B5 base", "B5_cuna_cuello": "B5 cuello",
       "M11_bandeja": "M11 inferior", "M11_bandeja_sup": "M11 superior"}


def cod(pid):
    return COD.get(pid, pid.split("_")[0])


SELLOS = [
    # ---- nodo P2_robusto: caja + 2 rieles + 2 cápsulas = un solo volumen seco
    dict(sello="Tapa M2 sobre la caja M1s", piezas=["M1s_caja_cuerpo", "M2_caja_tapa"], tipo="cordón O-ring Ø2 en ranura", zona="nodo",
         protege="La electrónica del nodo (bandejas M11) y todo el volumen seco, que desde la caja se extiende por los rieles hasta las cápsulas.",
         refs=[("M2_caja_tapa", "groove"), ("M2_caja_tapa", "pasos"), ("M1s_caja_cuerpo", "brida")], cant="×1"),
    dict(sello="Riel M3s ↔ caja M1s: cordón plano (×2)", piezas=["M3s_riel_gancho", "M1s_caja_cuerpo"], tipo="cordón de goma Ø2 NBR en ranura plana, 20 % de compresión (ranura 1.6 × 2.6 mm)", zona="nodo",
         protege="La unión entre la caja y cada riel, alrededor de la ventana por donde pasa el cable.",
         refs=[("M3s_riel_gancho", "oring"), ("M3s_riel_gancho", "m4"), ("M1s_caja_cuerpo", "ventana"), ("M1s_caja_cuerpo", "m4")], cant="×2"),
    dict(sello="Almohadilla del riel M3s ↔ silla de M5s: cordón plano (×2)", piezas=["M3s_riel_gancho", "M5s_capsula_tapa_pie"], tipo="cordón de goma Ø2 NBR en ranura plana, 20 % de compresión", zona="nodo",
         protege="La unión entre el riel y la tapa de la cápsula, alrededor de la abertura de 8 × 22 mm por donde baja el cable.",
         refs=[("M5s_capsula_tapa_pie", "oring_riel"), ("M3s_riel_gancho", "abertura"), ("M3s_riel_gancho", "pad_m3"), ("M5s_capsula_tapa_pie", "inserts")], cant="×2"),
    dict(sello="Tapa M5s sobre la cápsula M4 (×2)", piezas=["M4_capsula_cuerpo", "M5s_capsula_tapa_pie"], tipo="cordón O-ring Ø2 en ranura", zona="nodo",
         protege="La cámara Arducam y el anillo LED dentro de cada cápsula. El cable plano entra por la ranura de esta tapa, que queda dentro del sello.",
         refs=[("M5s_capsula_tapa_pie", "groove"), ("M5s_capsula_tapa_pie", "pasos"), ("M4_capsula_cuerpo", "pasos")], cant="×2"),
    dict(sello="Ventana de acrílico M7: junta plana + silicona (×2)", piezas=["M4_capsula_cuerpo", "M6_capsula_bisel"], tipo="junta plana de silicona de 1 mm (Ø30 × Ø26.5) comprimida 20 % por el bisel M6 + cordón de silicona marina en el borde", zona="nodo",
         protege="El frente de cada cápsula: la ventana deja pasar la luz y no el agua.",
         refs=[("M4_capsula_cuerpo", "asiento"), ("M6_capsula_bisel", "abertura"), ("M6_capsula_bisel", "pasos")], cant="×2"),
    dict(sello="PG7 del umbilical en la tapa M2", piezas=["M2_caja_tapa"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca", zona="nodo",
         protege="El paso del cable umbilical hacia la caja seca. Es el único prensaestopas que queda en el nodo.", refs=[("M2_caja_tapa", "pg7")], cant="×1"),
    dict(sello="Insertos ciegos que no perforan paredes", piezas=["M1s_caja_cuerpo", "M5s_capsula_tapa_pie", "M3s_riel_gancho"], tipo="inserto térmico ciego (no atraviesa)", zona="nodo",
         protege="Los 12 M3 de la brida de M1s, los 8 M4 de los cojines y los 4 M3 de cada silla de M5s se enroscan en insertos ciegos: ningún tornillo abre un camino al interior. Los 4 M3 de la almohadilla del riel pasan por las alas, fuera del canal.",
         refs=[("M1s_caja_cuerpo", "ins_brida"), ("M1s_caja_cuerpo", "m4"), ("M5s_capsula_tapa_pie", "inserts"), ("M3s_riel_gancho", "pad_m3")], cant=""),
    # ---- boya
    dict(sello="Tapa B4 sobre la caja seca B3", piezas=["B3_caja", "B4_tapa"], tipo="cordón O-ring Ø2 en ranura", zona="boya",
         protege="La electrónica de la boya: PCB, Waveshare, portabaterías 3×18650 y RTC.",
         refs=[("B4_tapa", "groove"), ("B4_tapa", "pasos"), ("B3_caja", "brida")], cant="×1"),
    dict(sello="PG7 del umbilical en B3 (pared −X)", piezas=["B3_caja"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca", zona="boya",
         protege="El paso del cable umbilical (boya ↔ nodo) hacia la caja seca.", refs=[("B3_caja", "pg7_umb")], cant="×1"),
    dict(sello="PG7 del cable solar en B3 (pared +X)", piezas=["B3_caja"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca", zona="boya",
         protege="El paso del cable del panel solar hacia la caja seca.", refs=[("B3_caja", "pg7_solar")], cant="×1"),
    dict(sello="PG7 del pigtail de antena en B3 (pared +X)", piezas=["B3_caja", "B2_cubierta_mastil"], tipo="prensaestopas PG7 (Ø12.6) con contratuerca", zona="boya",
         protege="El paso del pigtail de la antena hacia la caja seca. El mástil de B2 solo guía el cable: no sella.", refs=[("B3_caja", "pg7_pig"), ("B2_cubierta_mastil", "puerto")], cant="×1"),
    dict(sello="Insertos M3 de la brida de B3", piezas=["B3_caja"], tipo="inserto térmico ciego (no atraviesa la brida)", zona="boya",
         protege="La brida no queda perforada y los tornillos quedan fuera del cordón: el agua no tiene camino por los tornillos.", refs=[("B3_caja", "ins_brida")], cant=""),
    dict(sello="Botellas PET selladas (flotación)", piezas=["B1_casco", "B5_cuna_base", "B5_cuna_cuello"], tipo="tapón de rosca de fábrica (botella comprada)", zona="boya",
         protege="El aire que flota la boya. El casco impreso NO es estanco: solo sostiene las botellas.", refs=[("B1_casco", "silla"), ("B1_casco", "cuello"), ("B5_cuna_cuello", "cuello")], cant=""),
]
NO_ESTANCO = [
    "Bolsillos de lastre de M1s y sus tapas M3t: están fuera del sello y se llenan de agua. Es lo normal; el lastre son tuercas y arandelas a granel.",
    "Gancho en C de M3s y su correa: están por fuera del riel, mojados siempre.",
    "Las 4 alas de la almohadilla del riel (con los M3 que bajan a M5s): quedan fuera del canal. El agua puede tocarlas sin entrar.",
    "Casco B1, cunas B5, correas B6 y cubierta B2 de la boya: estructura abierta; flotan las botellas PET (cerradas de fábrica).",
    "Mástil de B2 (solo guía el cable del pigtail): no sella; el sello está en el PG7 de B3.",
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
    est = ["Concepto vigente (04/11/2026): caja, rieles y cápsulas son un", "solo volumen seco; el cable plano de cada cámara va por", "dentro y el único PG7 del nodo es el del umbilical.", "",
           "Sellos y pruebas de agua: docs/ESTANQUEIDAD.md.", "Texto de esta guía: docs/GUIA_PIEZAS.md.", f"Generada el {datetime.date.today().isoformat()} con cad_final/guia_piezas.py."]
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


def seal_figure(path):
    """ESTANQUEIDAD figure: the node assembly (grey, see-through), the dry volume in BLUE, each seal of the node numbered in RED.
    The assembly is read from the real STEP (ensamble_simple_D200.step); the dry volume is rebuilt from the design dimensions."""
    import params as P
    asm = ROOT / "salida" / "prototipos" / "P2_robusto" / "ensamble_simple_D200.step"
    names = [s["nombre"] for s in json.loads((ROOT / "salida" / "prototipos" / "P2_robusto" / "ensamble_solidos.json").read_text(encoding="utf-8"))["solidos"]]
    solids = dict(zip(names, cq.importers.importStep(str(asm)).val().Solids()))

    def mesh_of(sol):
        v, t = sol.tessellate(0.2, 0.4)
        return pv.PolyData(np.array([x.toTuple() for x in v]), np.hstack([[3, *x] for x in t])).clean(tolerance=1e-5)

    keep = ["M1s_caja_cuerpo", "M2_caja_tapa"] + [f"{k}_{s}" for s in ("der", "izq") for k in ("M3s_riel_gancho", "M5s_capsula_tapa_pie", "M4_capsula_cuerpo", "M6_capsula_bisel")]
    grey = [mesh_of(solids[k]) for k in keep]

    # capsule frame -> assembly (+X side): same rotation as simple.cap_rot, translation found by matching the real M4
    m4 = cq.importers.importStep(str(NODO / "M4_capsula_cuerpo.step")).val()

    def rot(s):
        s = s.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), P.SIMPLE_CAP_TILT)
        return s.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180) if P.SIMPLE_CAP_AZ == "adentro" else s
    bb0, bb1 = rot(m4).BoundingBox(), solids["M4_capsula_cuerpo_der"].BoundingBox()
    tr = np.array([bb1.xmin - bb0.xmin, bb1.ymin - bb0.ymin, bb1.zmin - bb0.zmin])

    def tf(p):                                                     # point of the capsule frame -> assembly
        th = math.radians(P.SIMPLE_CAP_TILT)
        x, y, z = p
        xr, zr = x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th)
        if P.SIMPLE_CAP_AZ == "adentro":
            xr, y = -xr, -y
        return np.array([xr, y, zr]) + tr

    def mir(p):
        return np.array([-p[0], -p[1], p[2]])

    def box(x0, x1, y0, y1, z0, z1):
        return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0)).val()

    blue = [box(-59.5, 59.5, -59, 59, 5, 77.2)]
    ch = box(59, 209, -12, 12, 4.7, 22.7)
    blue += [ch, ch.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180)]
    t_ = np.array([0.5, -0.866])
    n_ = np.array([0.866, 0.5])
    c_ = np.array([176.3, -46.8])
    pts = [(181, 4.7), (189, 4.7), (181, -17.3), (189, -17.3)] + [tuple(c_ + s * 4 * t_ + k * 3 * n_) for s in (-1, 1) for k in (-1, 1)]
    from scipy.spatial import ConvexHull
    hull = ConvexHull(np.array(pts))
    poly = [tuple(map(float, pts[i])) for i in hull.vertices]
    duct = cq.Workplane("XZ").workplane(offset=-11).polyline(poly).close().extrude(22).val()
    blue += [duct, duct.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180)]
    cav = box(22, 61, -19, 19, -19, 19)                           # capsule cavity, capsule frame
    cav = rot(cav).translate(cq.Vector(*tr))
    blue += [cav, cav.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180)]
    blue_m = [mesh_of(b) for b in blue]

    # seals of the node: number -> 3D anchors
    pg7 = [h for h in hole_instances(cq.Workplane().add(solids["M2_caja_tapa"]), solids["M2_caja_tapa"]) if abs(h["D"] - 12.6) < 0.1 and h["ax"] == "z"]
    pg7_pt = (pg7[0]["ctr"] + np.array([0, 0, pg7[0]["len"] / 2])) if pg7 else np.array([0.0, 0.0, 110.0])
    sx = lambda *ps: [np.array(p, float) for p in ps]
    anchors = {
        1: sx((0, -64, 77)),
        2: sx((73.5, 0, 25.5), (-73.5, 0, 25.5)),
        3: sx((185, -16, -7.3), (-185, 16, -7.3)),
        4: [tf((24, -27.5, 0)), mir(tf((24, -27.5, 0)))],
        5: [tf((67, 0, 14)), mir(tf((67, 0, 14)))],
        6: [pg7_pt],
        7: sx((68.5, 68, 77), (73.5, 20, 23.7)),
    }
    labels = {1: "Tapa M2 sobre la caja M1s", 2: "Cordón plano riel ↔ caja (×2)", 3: "Cordón plano riel ↔ silla M5s (×2)", 4: "Tapa M5s sobre la cápsula M4 (×2)",
              5: "Ventana M7: junta de silicona + silicona marina (×2)", 6: "PG7 del umbilical en la tapa M2", 7: "Insertos ciegos (no perforan paredes)"}

    allm = [m for m in grey] + blue_m
    allpts = np.vstack([m.points for m in allm])

    def render(az, el, box_=None, W=1400, H=900):
        d, right, up = basis(az, el)
        pts_ = allpts if box_ is None else box_
        pr, pu = pts_ @ right, pts_ @ up
        cx, cy = (pr.min() + pr.max()) / 2, (pu.min() + pu.max()) / 2
        S = max((pu.max() - pu.min()) / 2, (pr.max() - pr.min()) / 2 * H / W) * 1.12
        k = (H / 2) / S
        c3 = right * cx + up * cy
        R = float(np.linalg.norm(allpts.max(0) - allpts.min(0))) * 2
        pl = pv.Plotter(off_screen=True, window_size=(W, H))
        pl.set_background("white")
        for m in grey:
            pl.add_mesh(m, color="#b9c0c9", opacity=0.20, smooth_shading=False)
            pl.add_mesh(m.extract_feature_edges(35, boundary_edges=False, non_manifold_edges=False), color="#6b7580", line_width=0.7)
        for m in blue_m:
            pl.add_mesh(m, color="#1f6fe0", opacity=0.55, smooth_shading=False)
        pl.enable_parallel_projection()
        pl.camera_position = [tuple(c3 + d * R), tuple(c3), tuple(up)]
        pl.camera.parallel_scale = S
        pl.camera.clipping_range = (R * 0.2, R * 3)
        img = pl.screenshot(return_img=True)
        pl.close()
        return img, (lambda P_: np.array([W / 2 + ((np.asarray(P_, float) @ right) - cx) * k, H / 2 - ((np.asarray(P_, float) @ up) - cy) * k]))

    views = [(35, 24, None, 1400, 900), (30, 22, np.array([[x, y, z] for x in (85, 215) for y in (-40, 40) for z in (-95, 30)], float), 1000, 1000)]
    fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
    fig.text(0.03, 0.95, "Nodo P2_robusto: el volumen seco (azul) y sus sellos (rojo)", fontsize=15, fontweight="bold")
    fig.text(0.03, 0.918, "Todo lo azul es un solo espacio seco: la caja, los dos rieles, el conducto bajo cada riel y las dos cápsulas. Cada número rojo es un lugar donde un sello impide que entre el agua.", fontsize=8.2, color="#333333")
    rects = [(0.02, 0.36, 0.57, 0.53), (0.61, 0.36, 0.37, 0.53)]
    for (az, el, bx, W_, H_), rc in zip(views, rects):
        img, px = render(az, el, bx, W_, H_)
        ax = fig.add_axes(rc)
        ax.imshow(img, extent=(0, W_, H_, 0))
        ax.set_xlim(0, W_)
        ax.set_ylim(H_, 0)
        ax.axis("off")
        items_px = [(n, tuple(px(p))) for n, ps in anchors.items() for p in ps if 0 < px(p)[0] < W_ and 0 < px(p)[1] < H_]
        for n, anc, c in _place_markers(items_px, rad=26):
            if math.hypot(c[0] - anc[0], c[1] - anc[1]) > 1:
                ax.plot([anc[0], c[0]], [anc[1], c[1]], "-", color="#c0272d", lw=1.1, zorder=6)
            ax.plot([anc[0]], [anc[1]], "o", ms=5, color="#c0272d", mec="white", mew=0.6, zorder=7)
            ax.add_patch(Circle(c, 25, fc="#c0272d", ec="white", lw=1.2, zorder=8))
            ax.text(c[0], c[1] + 1, str(n), color="white", fontsize=10, fontweight="bold", ha="center", va="center", zorder=9)
    y = 0.31
    for n, lab in labels.items():
        fig.patches.append(matplotlib.patches.Ellipse((0.04, y), 0.016, 0.016 * 11.69 / 8.27, transform=fig.transFigure, fc="#c0272d", ec="none"))
        fig.text(0.04, y, str(n), color="white", fontsize=7.5, fontweight="bold", ha="center", va="center")
        fig.text(0.055, y, lab, fontsize=9, va="center")
        y -= 0.034
    fig.patches.append(matplotlib.patches.Rectangle((0.55, 0.296), 0.02, 0.022, transform=fig.transFigure, fc="#1f6fe0", ec="none", alpha=0.6))
    fig.text(0.58, 0.307, "Volumen seco (el cable plano de la cámara viaja por aquí)", fontsize=9, va="center")
    fig.text(0.55, 0.265, "Izquierda: el nodo completo. Derecha: ampliación de un extremo (riel, conducto y cápsula).", fontsize=8, color="#555555")
    fig.text(0.55, 0.238, "Los sellos de la boya (B3 y B4) no salen aquí: están en la tabla.", fontsize=8, color="#555555")
    fig.text(0.03, 0.018, "LanternGuard · estanqueidad · " + datetime.date.today().isoformat(), fontsize=6.5, color="#777777")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print("figura de sellos ->", path)


def estanqueidad_md(sellos):
    """ESTANQUEIDAD.md: plain-language text for the student team (Spanish)."""
    L = ["# Estanqueidad del nodo y de la boya", "",
         f"Versión del {datetime.date.today().isoformat()} · concepto vigente: **un solo volumen seco** en el nodo (caja + rieles + cápsulas), con el cable plano de las cámaras por dentro. "
         "Los números de la tabla se pueden buscar en la guía de piezas (`GUIA_PIEZAS_LanternGuard.pdf`).", "",
         "## 1. La idea en dos frases", "",
         "Antes, cada cámara tenía su propio cable que salía de la caja por un prensaestopas (PG7), corría por un riel abierto lleno de agua y entraba a la cápsula por otro PG7. "
         "Eran cuatro pasos de cable que podían gotear.", "",
         "Ahora la caja, los dos rieles y las dos cápsulas son **un solo espacio seco**: el cable plano de la cámara viaja por dentro, protegido, y las piezas se unen con cordones de goma planos. "
         "El único prensaestopas que queda en el nodo es el del cable umbilical, en la tapa M2.", "",
         "## 2. El dibujo", "",
         "En azul, el espacio que debe quedar seco. En rojo y numerado, cada sello. Los números son los de la tabla de abajo.", "",
         "![Volumen seco y sellos del nodo](../salida/guia_piezas/estanqueidad_nodo.png)", "",
         "El camino del cable de una cámara, siempre en seco: dentro de la caja → ventana de la pared de extremo → canal del riel → curva suave (radio 10 mm) → abertura bajo el riel → conducto de la pieza M5s → ranura de la tapa de la cápsula → cámara.", "",
         "## 3. Tabla de sellos", "",
         "Hay **{}** sellos en el nodo (números 1 a 7) y **{}** en la boya (números 8 a {}). Los de la boya no cambiaron.".format(
             sum(1 for s in sellos if s["zona"] == "nodo"), sum(1 for s in sellos if s["zona"] == "boya"), len(sellos)), "",
         "| N° | Sello | Cuántos | Cómo sella | Qué protege | Dónde verlo en la guía |", "|---|---|---|---|---|---|"]
    for s in sellos:
        L.append(f"| {s['n']} | {s['sello']} | {s['cant']} | {s['tipo']} | {s['protege']} | {'; '.join(s['donde'])} |")
    L += ["", "Notas de la tabla:", "",
          "- **Cordón plano** = un cordón de goma NBR de Ø2 mm puesto en una ranura con forma de marco (1.6 mm de hondo × 2.6 mm de ancho). Al apretar los tornillos se aplasta un 20 % y llena la rendija. No se pega ni se estira: se coloca sin torcer.",
          "- **Insertos ciegos**: tuercas de latón que se funden dentro del plástico sin atravesarlo. Como no hay agujero de lado a lado, el agua no tiene camino por el tornillo. La excepción son los 4 tornillos de la almohadilla del riel (M3s), que pasan por las alas, fuera del canal.", "",
          "## 4. Lo que NO es estanco, a propósito", ""] + [f"- {x}" for x in NO_ESTANCO]
    L += ["", "Todo lo demás del nodo (caja, riel, conducto, cápsulas) sí debe quedar seco.", "",
          "## 5. Impresión de las piezas estancas", "",
          "Las piezas que forman el volumen seco (M1s, M2, M3s, M4, M5s y, en la boya, B3 y B4) se imprimen con el perfil estanco: **4 perímetros, 5 capas arriba y 5 abajo, 100 % de relleno**. "
          "Opcional: una capa de epoxi por dentro. Antes de armar, mire cada pieza contra una luz fuerte: si se ve luz a través de una pared, hay un hueco y esa pieza se reimprime.", "",
          "## 6. Cómo probar que no entra agua", "",
          "Regla general: **nunca ponga electrónica en una prueba de agua**. Dentro va papel de cocina seco: si al abrir está seco, el sello aguantó; si tiene manchas, ahí entró agua.", "",
          "### Paso 1. Montaje en seco (sin agua)", "",
          "1. Limpie las ranuras (sin rebabas ni polvo) y coloque cada cordón sin torcerlo: debe asomar un poco por encima de la ranura.",
          "2. Arme todo el nodo con los tornillos, apretando en cruz y de a poco (primero medio apriete en todos, luego el apriete final).",
          "3. Pase por todo el camino del cable una tira de papel del mismo ancho que el cable plano (22 mm): debe entrar por la ventana de la caja y salir por la ranura de la tapa de la cápsula sin atascarse ni doblarse en ángulo.",
          "4. Anote qué tornillos quedaron más flojos o más duros: son los primeros sospechosos si algo gotea.", "",
          "### Paso 2. Baño de cada subconjunto vacío", "",
          "Pruebe de lo pequeño a lo grande. En cada prueba: papel de cocina seco adentro, lastre para que se hunda (una piedra o pesas atadas por fuera), y un balde u otro recipiente donde quepa a 0.5 m de profundidad.", "",
          "| Subconjunto | Cómo prepararlo | Qué mirar al abrir |", "|---|---|---|",
          "| A. Una cápsula completa (M4 + M5s + M6 + M7 con su junta y silicona) | Cierre la abertura de la placa de M5s con una placa plana de prueba y su cordón (o con una tapa de acrílico). | Papel seco en la cámara; ninguna gota tras la ventana. |",
          "| B. Caja M1s con tapa M2 | Tape las dos ventanas de las paredes con placas planas de prueba y ponga el PG7 con el cable umbilical (o un tapón). | Papel seco en las bandejas; ninguna gota en la tapa. |",
          "| C. Un riel M3s con su silla M5s | Cierre la boca del riel contra una placa plana de prueba y la ranura de la tapa de M5s con cinta de buena calidad. | Papel seco dentro del canal y del conducto. |",
          "| D. Nodo completo (caja + 2 rieles + 2 cápsulas) | El nodo armado como irá en el agua, sin electrónica. | Papel seco en la caja, en los dos canales y en las dos cápsulas. |", "",
          "Pasos de cada prueba:", "",
          "1. Sumerja 30 minutos a 0.5 m. Saque, seque por fuera con un paño y abra sobre una mesa. Mire el papel.",
          "2. Si está seco, ponga papel nuevo y repita, esta vez **24 horas**.",
          "3. Al terminar, saque una foto del papel y anote la fecha, el subconjunto y el resultado.",
          "4. Pase al siguiente subconjunto solo si el anterior salió seco las 24 horas.", "",
          "### Paso 3. Piscina con peso, antes de la electrónica", "",
          "1. Arme el nodo completo con papel dentro y un peso de prueba que iguale la masa de la electrónica.",
          "2. Cuélguelo del aro como irá en la linterna y bájelo a la profundidad de trabajo prevista.",
          "3. Déjelo 2 horas. Saque, seque y revise el papel de la caja, de los dos rieles y de las dos cápsulas.",
          "4. Solo si todo está seco, se pasa a montar la electrónica real.", "",
          "### Si entra agua", "",
          "1. No arme de nuevo enseguida. Abra, saque el papel y mire **dónde** está mojado: la mancha apunta al sello que falló (la tabla de la sección 3 dice qué piezas lo forman).",
          "2. Causas más comunes: cordón torcido o pellizcado; un tornillo flojo en una esquina; ranura con rebaba o con polvo; pared impresa con huecos (se ve a contraluz); silicona de la ventana con un hueco.",
          "3. Corrija **una sola cosa** a la vez (por ejemplo, cordón nuevo, o una capa de epoxi, o rehacer la pieza) y repita la prueba completa de ese subconjunto, empezando de nuevo por los 30 minutos.",
          "4. Si falla dos veces en el mismo sello, anote la pieza y avise: puede ser un problema de diseño y no de armado.", "",
          "## 7. Por confirmar en las pruebas", "",
          "- La junta plana de silicona de la ventana (Ø30 × Ø26.5 × 1 mm) y el cordón de silicona marina son nuevos: la prueba de la cápsula (A) es la que confirma que bastan.",
          "- El cordón plano en forma de marco de la brida del riel y el de la silla de M5s tienen esquinas redondeadas: revise que el cordón no se pliegue en las esquinas al apretar.",
          "- Tornillo de las bandejas (M11): M3 × 38 inox (o M3 × 40 recortado 2 mm). Atraviesa 33 mm (bandeja 3 + poste 27 + bandeja 3) y entra 5 mm en el inserto de 6 mm sin tocar el fondo. Verificar con las piezas impresas."]
    return L


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
        sellos.append(dict(n=i, sello=s["sello"], piezas=s["piezas"], tipo=s["tipo"], protege=s["protege"], donde=donde, zona=s["zona"], cant=s["cant"]))
    (OUT / "sellos.json").write_text(json.dumps(sellos, ensure_ascii=False, indent=1), encoding="utf-8")
    seal_figure(str(OUT / "estanqueidad_nodo.png"))
    md = estanqueidad_md(sellos)
    (DOCS / "ESTANQUEIDAD.md").write_text("\n".join(md), encoding="utf-8")
    g = ["# Guía de piezas LanternGuard", "", "> Texto de `GUIA_PIEZAS_LanternGuard.pdf`. Los números coinciden con los de los PNG de `salida/guia_piezas/`.",
         "> Concepto vigente (04/11/2026): caja, rieles y cápsulas son un solo volumen seco; el cable plano va por dentro y el único PG7 del nodo es el del umbilical.", "",
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
