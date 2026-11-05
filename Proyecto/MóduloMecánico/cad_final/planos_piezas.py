"""Simple drawing per piece (A4, PNG + PDF) projected from its STEP with OCCT hidden-line removal.

    python planos_piezas.py [M1 M3p ...]      (or: python build.py --planos)   -> ../planos/cad_final/<code>.{png,pdf}
    python planos_piezas.py --carpeta ../salida/prototipos/P4_estetico --prefijo P4 [--titulo "P4 estetico"]
        -> ../planos/cad_final/P4/<code>.{png,pdf}: one sheet per STEP of the folder's step/ (name, infill and print
           orientation from its resultados.json; quantity from its slicer.json "cant", else the pair rule)
    python planos_piezas.py --unir [--portada portada.pdf] P1 P4 BP   -> ../planos/PLANOS_LanternGuard.pdf

Three first-angle views (front, top, side) with the overall dimensions measured on the projected outline, plus the
table of important dimensions from piezas.py (value, params.py name, estado). The projection helpers follow
../cad/planos.py, which is not imported because it loads the old cad/ params at import time.
"""
import json
import logging
import sys
import textwrap
from types import SimpleNamespace
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt  # noqa: E402
from OCP.HLRAlgo import HLRAlgo_Projector  # noqa: E402
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape  # noqa: E402

import params as P  # noqa: E402
import piezas as Z  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "planos" / "cad_final"
SCALES = (5.0, 2.0, 1.0, 0.5, 0.2, 0.1)
LW_VIS, LW_THIN = 0.7, 0.35
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # the font list has per-OS fallbacks
plt.rcParams.update({"font.family": ["Arial", "Liberation Sans", "DejaVu Sans"], "font.size": 7})

# view name -> (normal toward the viewer, paper right); first angle: top view below the front, the view from the
# left (-X) on the right of the front
VIEWS = {"frente": ((0, -1, 0), (1, 0, 0)), "planta": ((0, 0, 1), (1, 0, 0)), "lado": ((-1, 0, 0), (0, -1, 0))}
ISO = ((1, -1, 1), (1, 1, 0))       # isometric from front-right-top, drawn under the side view
ORIENT_TXT = {"sin girar": "como en el modelo", "X180": "X180 (dada vuelta)", "X+90": "X+90 (de costado)",
              "X-90": "X-90 (de costado)", "Y+90": "Y+90 (de canto)", "Y-90": "Y-90 (de canto)"}
PAIRS = ("M3", "M4", "M5", "M6", "M7", "M9", "M10", "M13", "M14")   # one per rail side (folder mode, no "cant")


def project(shape, n, vx):
    algo = HLRBRep_Algo()
    algo.Add(shape.wrapped)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*n), gp_Dir(*vx))))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)
    out = []
    for c in (h.VCompound(), h.OutLineVCompound(), h.Rg1LineVCompound()):
        if c is None or c.IsNull():
            continue
        for e in cq.Shape.cast(c).Edges():
            k = max(2, min(120, int(e.Length() / 0.4) + 2))
            out.append(np.array([e.positionAt(t).toTuple()[:2] for t in np.linspace(0, 1, k)]))
    return out


def extent(polys):
    a = np.vstack(polys)
    return a.min(axis=0), a.max(axis=0)


def dim(ax, a, b, off, vertical=False):
    """Linear dimension between paper points a and b, line at x = off (vertical) or y = off (horizontal)."""
    a, b = np.array(a, float), np.array(b, float)
    if vertical:
        pa, pb = np.array([off, a[1]]), np.array([off, b[1]])
    else:
        pa, pb = np.array([a[0], off]), np.array([b[0], off])
    for p, q in ((a, pa), (b, pb)):
        ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=LW_THIN)
    ax.annotate("", xy=pa, xytext=pb, arrowprops=dict(arrowstyle="<|-|>", lw=LW_THIN, color="black", mutation_scale=6,
                                                       shrinkA=0, shrinkB=0))
    return pa, pb


def load(pz):
    if pz.step.exists():
        return cq.importers.importStep(str(pz.step)).val()
    if pz.code == "PB8":
        import probetas
        return probetas.pb8()["PB8_inserto_M4"].val()
    raise FileNotFoundError(pz.step)


def notes(pz):
    """Sheet notes for the new design, every number from params.py (the cad/ notes for 15 m do not apply)."""
    n = ["Cotas en mm. Tolerancias generales según ISO 2768-m.",
         "Tornillería M3/M4 de acero inoxidable A4 (AISI 316); la varilla M8 según riel.varilla_grado."]
    if pz.code in ("M1", "M2", "M4", "M5"):
        kpa = P.SEAWATER_DENSITY * 9.81 * P.DESIGN_DEPTH_M          # g/cm3 * m/s2 * m = kPa
        comp = (P.ORING_CORD - P.GROOVE_DEPTH) / P.ORING_CORD * 100
        n += [f"Junta tórica: cordón Ø{P.ORING_CORD:g} en ranura {P.GROOVE_WIDTH:g} × {P.GROOVE_DEPTH:g} "
              f"(compresión {comp:.0f} %).",
              f"Pared diseñada a {P.DESIGN_DEPTH_M:g} m ({kpa:.0f} kPa); manda la manipulación con "
              f"{P.HANDLING_LOAD_N:g} N."]
    if pz.code in ("M5", "M10"):
        n.append(f"Bisagra de {P.HINGE_TEETH} dientes: de 0° a 90° en pasos de {360 / P.HINGE_TEETH:g}°.")
    if pz.code == "M2":
        n.append(f"Asa y ojal Ø{P.HANDLE_EYE[1]:g} verificados a {P.HANDLING_LOAD_N + P.LANTERN_WATER_N:g} N "
                 f"({P.HANDLING_LOAD_N:g} N + {P.LANTERN_WATER_N:g} N de la linterna); grillete o argolla inox M6 en el ojal.")
    return n


def mass_max_g(pz, shape):
    """Solid (100 %) mass: the upper bound for any infill."""
    m = pz.material.lower()
    rho = P.ACRYLIC_DENSITY if "acr" in m else P.PETG_DENSITY if "petg" in m else None
    return None if rho is None else shape.Volume() / 1000.0 * rho


def sheet(pz, shape, out=OUT):
    fig = plt.figure(figsize=(297 / 25.4, 210 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 297)
    ax.set_ylim(0, 210)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((8, 8), 281, 194, fill=False, lw=1.2))
    raw = {k: project(shape, n, vx) for k, (n, vx) in VIEWS.items()}
    iso = project(shape, *ISO)
    ext = {k: extent(v) for k, v in raw.items()}
    size = {k: e[1] - e[0] for k, e in ext.items()}
    # drawing area: x 16..185, y 16..194; front top-left, top below it, side to the right of the front
    w_need = size["frente"][0] + size["lado"][0]
    h_need = size["frente"][1] + size["planta"][1]
    side_iso = not pz.keys                      # folder mode: no table, so the isometric takes the right column
    wmax, hmax = (160, 150) if side_iso else (125, 140)
    s = next((sc for sc in SCALES if w_need * sc <= wmax and h_need * sc <= hmax), SCALES[-1])
    gap = 22
    fx0 = 26
    fy0 = 194 - 18 - size["frente"][1] * s
    origin = {"frente": (fx0, fy0), "planta": (fx0, fy0 - gap - size["planta"][1] * s),
              "lado": (fx0 + size["frente"][0] * s + gap, fy0)}
    paper = {}
    for k, polys in raw.items():
        o = np.array(origin[k]) - ext[k][0] * s
        paper[k] = [o + s * pl for pl in polys]
        for pl in paper[k]:
            ax.plot(pl[:, 0], pl[:, 1], color="black", lw=LW_VIS, solid_capstyle="round")
        lo, hi = extent(paper[k])
        ax.text((lo[0] + hi[0]) / 2, lo[1] - 4.5 if k != "planta" else lo[1] - 4.5, k.upper(), ha="center", va="top",
                fontsize=6.5, color="#444")
    # isometric: right column in folder mode, else under the side view; at the sheet scale if it fits
    ilo, ihi = extent(iso)
    isz = ihi - ilo
    if side_iso:
        box = (192, 104, 93, 72)                  # x0, y0, w, h on paper
    else:
        lo_l = extent(paper["lado"])[0]
        box = (lo_l[0], 26, 185 - lo_l[0], lo_l[1] - 36)
    si = min(s * 2, box[2] / max(isz[0], 1e-6), box[3] / max(isz[1], 1e-6))
    io = np.array([box[0] + (box[2] - isz[0] * si) / 2, box[1] + box[3] - isz[1] * si]) - ilo * si
    for pl in iso:
        q = io + si * pl
        ax.plot(q[:, 0], q[:, 1], color="#333", lw=LW_THIN, solid_capstyle="round")
    ax.text(box[0] + box[2] / 2, box[1] + box[3] - isz[1] * si - 2, "ISOMÉTRICA (sin escala)", ha="center", va="top",
            fontsize=6.5, color="#444")
    # overall dimensions (true size = paper / s)
    lo, hi = extent(paper["frente"])
    pa, pb = dim(ax, (lo[0], hi[1]), (hi[0], hi[1]), hi[1] + 7)
    ax.text((pa[0] + pb[0]) / 2, pa[1] + 0.8, f"{size['frente'][0]:.1f}", ha="center", va="bottom", fontsize=7)
    pa, pb = dim(ax, (lo[0], lo[1]), (lo[0], hi[1]), lo[0] - 7, vertical=True)
    ax.text(pa[0] - 0.8, (pa[1] + pb[1]) / 2, f"{size['frente'][1]:.1f}", ha="right", va="center", rotation=90, fontsize=7)
    lo, hi = extent(paper["planta"])
    pa, pb = dim(ax, (lo[0], lo[1]), (lo[0], hi[1]), lo[0] - 7, vertical=True)
    ax.text(pa[0] - 0.8, (pa[1] + pb[1]) / 2, f"{size['planta'][1]:.1f}", ha="right", va="center", rotation=90, fontsize=7)
    # important dimensions table
    x0, y = 192, 194
    if side_iso:
        bb = shape.BoundingBox()
        ax.text(x0, y, "Medidas generales del modelo (mm)", fontsize=8, weight="bold", va="top")
        ax.text(x0, y - 6, f"{bb.xlen:.1f} × {bb.ylen:.1f} × {bb.zlen:.1f}  (X × Y × Z del CAD)", fontsize=6.5, va="top")
    else:
        ax.text(x0, y, "Cotas importantes (mm)", fontsize=8, weight="bold", va="top")
    y -= 6
    reg = P.REGISTRO
    for label, k, idx in pz.keys:
        st = "" if reg[k].estado == "confirmado" else " *"
        ax.text(x0, y, f"{label}: {Z.fmt(Z.value(k, idx))}{st}", fontsize=6.2, va="top")
        ax.text(x0 + 3, y - 3.2, k + (f" ({idx})" if isinstance(idx, str) else (f" [{idx + 1}]" if idx is not None else "")),
                fontsize=5.2, va="top", color="#555", family="monospace")
        y -= 7.4
        if y < 100:
            ax.text(x0, y, "... (sigue en MEDIDAS.md)", fontsize=6, va="top")
            break
    if not side_iso:
        ax.text(x0, 93, "* por confirmar (estimado o del fabricante)", fontsize=5.8, va="top", color="#444")
    # notes for the new design
    y = 87
    ax.text(x0, y, "Notas", fontsize=7, weight="bold", va="top")
    y -= 4.2
    for i, t in enumerate(getattr(pz, "extra_notes", None) or notes(pz), 1):
        for j, line in enumerate(textwrap.wrap(t, 72)):
            ax.text(x0 + (0 if j == 0 else 3), y, (f"{i}. " if j == 0 else "") + line, fontsize=5.5, va="top")
            y -= 3.1
    assert y > 53, f"{pz.code}: notes overflow into the title block"
    # title block
    tx, ty, tw, th = 192, 10, 95, 42
    ax.add_patch(Rectangle((tx, ty), tw, th, fill=False, lw=0.9))
    for yy in (ty + 30, ty + 20, ty + 10):
        ax.plot([tx, tx + tw], [yy, yy], color="black", lw=LW_THIN)
    ax.text(tx + 2, ty + 36, f"{pz.code} · {pz.name}", fontsize=8.5, weight="bold", va="center")
    mm = mass_max_g(pz, shape)
    ax.text(tx + 2, ty + 25, f"Material: {pz.material}   Relleno: {pz.infill.split(',')[0]}   "
            f"Masa máx. g: {'—' if mm is None else f'{mm:.0f}'}", fontsize=6.3, va="center")
    q = [pz.n(D) for D in P.RING_DIAMETERS]
    qt = getattr(pz, "qty_txt", None) or (f"{q[0]} por nodo" if len(set(q)) == 1 else "según el aro (ver MEDIDAS.md)")
    ax.text(tx + 2, ty + 15, f"Escala {('%g:1' % s) if s >= 1 else ('1:%g' % (1 / s))} (A4)   Cantidad: {qt}", fontsize=6.3, va="center")
    ax.text(tx + 2, ty + 5, "LanternGuard · Equipo 02 · desde el modelo (cad_final); revisión = commit de git", fontsize=5.6,
            va="center")
    ax.text(16, 12, "Proyección ISO-E (primer diedro). Medidas generales leídas del modelo. NO LISTO PARA IMPRIMIR "
            "mientras haya cotas por confirmar.", fontsize=5.8, color="#444")
    if getattr(pz, "orient_txt", None):
        ax.text(16, 16, f"Orientación de impresión: {pz.orient_txt}", fontsize=6.3)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{pz.code}.pdf", metadata={"CreationDate": None})  # same model, same bytes
    fig.savefig(out / f"{pz.code}.png", dpi=150, facecolor="white")
    plt.close(fig)
    return s


def _c(v, nd=1):
    """Number with decimal comma, no trailing zeros ("12,5", "10")."""
    return f"{v:.{nd}f}".rstrip("0").rstrip(".").replace(".", ",") if nd else f"{round(v)}"


def sheet_equipo(code, step, qty, out, date="2026-11-04", chamfer=None, material="PETG"):
    """Local drawing in the team's format (same as planos_onshape --formato equipo): ISO A4 landscape, first angle, mm with
    decimal comma, ISO title block (TITLE / LANTERNGUARD / DRAWN / DATE / MATERIAL / SCALE / SHEET) at x 124..287, y 10..49
    of a 10 mm frame. Front, top, left side and isometric views; overall dimensions of each view, hole list and chamfer
    note. Marked 'Plano generado en local (cuota de la API de Onshape)'. Returns (pdf path, scale text, notes list)."""
    shape = cq.importers.importStep(str(step)).val()
    fig = plt.figure(figsize=(297 / 25.4, 210 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 297)
    ax.set_ylim(0, 210)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((10, 10), 277, 190, fill=False, lw=1.0))
    raw = {k: project(shape, n, vx) for k, (n, vx) in VIEWS.items()}
    iso = project(shape, *ISO)
    ext = {k: extent(v) for k, v in raw.items()}
    sz = {k: e[1] - e[0] for k, e in ext.items()}
    std = (2.0, 1.0, 0.5, 0.4, 1 / 3, 0.25, 0.2, 0.125, 0.1)
    s = next((sc for sc in std if sz["frente"][0] * sc <= 98 and sz["frente"][1] * sc + sz["planta"][1] * sc <= 104
              and sz["lado"][0] * sc <= 128 and sz["lado"][1] * sc <= 80), std[-1])
    # left column: front above, top below; right: side on top, isometric under it, above the title block
    fx0, fy_top = 26.0, 192.0
    fy0 = fy_top - 8 - sz["frente"][1] * s
    origin = {"frente": (fx0, fy0), "planta": (fx0, fy0 - 32 - sz["planta"][1] * s),
              "lado": (146.0, fy_top - 8 - sz["lado"][1] * s)}
    paper = {}
    for k, polys in raw.items():
        o = np.array(origin[k]) - ext[k][0] * s
        paper[k] = [o + s * pl for pl in polys]
        for pl in paper[k]:
            ax.plot(pl[:, 0], pl[:, 1], color="black", lw=LW_VIS, solid_capstyle="round")
        lo, hi = extent(paper[k])
        ax.text((lo[0] + hi[0]) / 2, lo[1] - 9.5, {"frente": "FRONTAL", "planta": "SUPERIOR", "lado": "LATERAL"}[k], ha="center",
                va="top", fontsize=6.5, color="#444")

    def hdim(k, off, label):
        lo, hi = extent(paper[k])
        pa, pb = dim(ax, (lo[0], hi[1]), (hi[0], hi[1]), hi[1] + off)
        ax.text((pa[0] + pb[0]) / 2, pa[1] + 0.8, label, ha="center", va="bottom", fontsize=7)

    def vdim(k, off, label):
        lo, hi = extent(paper[k])
        pa, pb = dim(ax, (lo[0], lo[1]), (lo[0], hi[1]), lo[0] - off, vertical=True)
        ax.text(pa[0] - 0.8, (pa[1] + pb[1]) / 2, label, ha="right", va="center", rotation=90, fontsize=7)
    hdim("frente", 6, _c(sz["frente"][0]))
    vdim("frente", 6, _c(sz["frente"][1]))
    hdim("planta", 6, _c(sz["planta"][0]))
    vdim("planta", 6, _c(sz["planta"][1]))
    hdim("lado", 6, _c(sz["lado"][0]))
    vdim("lado", 6, _c(sz["lado"][1]))
    # isometric in the free area under the side view
    lo_l, hi_l = extent(paper["lado"])
    ilo, ihi = extent(iso)
    isz = ihi - ilo
    box = (125.0, 78.0, 160.0, max(10.0, lo_l[1] - 22 - 78.0))
    si = min(s * 2, box[2] / max(isz[0], 1e-6), box[3] / max(isz[1], 1e-6))
    io = np.array([box[0] + (box[2] - isz[0] * si) / 2, box[1] + box[3] - isz[1] * si]) - ilo * si
    for pl in iso:
        q = io + si * pl
        ax.plot(q[:, 0], q[:, 1], color="#333", lw=LW_THIN, solid_capstyle="round")
    ax.text(box[0] + box[2] / 2, box[1] + box[3] - isz[1] * si - 2, "ISOMÉTRICA (sin escala)", ha="center", va="top",
            fontsize=6.5, color="#444")
    # hole list (concave full cylinders), chamfer note
    notes = []
    try:
        import planos_onshape as PO
        hs = PO.holes(step)
        groups = {}
        for _, _, r in hs:
            groups[round(2 * r, 2)] = groups.get(round(2 * r, 2), 0) + 1
        if groups:
            notes.append("Agujeros: " + "; ".join(f"{n}x Ø{_c(d, 2)}" for d, n in sorted(groups.items())))
    except Exception as e:  # noqa: BLE001
        notes.append(f"(lista de agujeros no disponible: {str(e)[:40]})")
    if chamfer:
        notes += chamfer["lineas"][1:] and ["Chaflán 45°: " + "; ".join(chamfer["lineas"][1:])]
    notes.append("Espesores, separación de nervios y posición de agujeros: ver cotas a mano (COTAS_A_MANO).")
    y = 50.0 + 4 * (len(notes) + 1)
    # title block: the standard layout of the Onshape A4 sheet of the team
    tx0, ty0, tx1, ty1 = 124.0, 10.0, 287.0, 49.0
    ax.add_patch(Rectangle((tx0, ty0), tx1 - tx0, ty1 - ty0, fill=False, lw=1.0))
    for yy in (ty0 + 13, ty0 + 26):
        ax.plot([tx0, tx1], [yy, yy], color="black", lw=LW_THIN)
    for xx in (tx0 + 54, tx0 + 108):
        ax.plot([xx, xx], [ty0, ty0 + 26], color="black", lw=LW_THIN)
    ax.plot([tx0 + 81, tx0 + 81], [ty0 + 26, ty1], color="black", lw=LW_THIN)

    def cell(x, yb, label, value, size=8):
        ax.text(x + 1.5, yb + 11.3, label, fontsize=4.5, color="#555", va="top")
        ax.text(x + 1.5, yb + 5.0, value, fontsize=size, va="center")
    cell(tx0, ty0 + 26, "TITLE", code, 9)
    cell(tx0 + 81, ty0 + 26, "COMPANY", "LANTERNGUARD", 8)
    cell(tx0, ty0 + 13, "DRAWN", "Equipo 02 UPCH")
    cell(tx0 + 54, ty0 + 13, "DATE", date)
    cell(tx0 + 108, ty0 + 13, "MATERIAL", material)
    sc = f"{_c(s)}:1" if s >= 1 else f"1:{_c(1 / s)}"
    cell(tx0, ty0, "SCALE", sc)
    cell(tx0 + 54, ty0, "SHEET", "1 of 1")
    cell(tx0 + 108, ty0, "QTY", f"{qty}")
    ax.text(tx0 + 2, ty1 + 3.2, f"Cantidad: {qty}   ·   Material: {material}   ·   Cotas en mm   ·   Proyección: primer diedro (ISO)",
            fontsize=5.8, va="bottom")
    ax.text(tx0 + 2, ty1 + 7.2, "Plano generado en local (cuota de la API de Onshape)", fontsize=6.3, weight="bold",
            va="bottom", color="#a00000")
    for i, t in enumerate(notes):
        ax.text(tx0 + 2, ty1 + 11.5 + 3.6 * (len(notes) - 1 - i), t, fontsize=5.6, va="bottom")
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / f"PLANO_A4_{code}_local.pdf"
    fig.savefig(pdf, metadata={"CreationDate": None})
    fig.savefig(out / f"PLANO_A4_{code}_local.png", dpi=110, facecolor="white")
    plt.close(fig)
    return pdf, sc, notes


def infill_txt(r):
    return "no se imprime (acrílico)" if r is None else f"{round(r * 100)} %" if isinstance(r, (int, float)) else str(r)


def folder_pieces(folder, prefix, title=None):
    """Pieza-like entries for sheet() from a prototype folder: step/<stem>.step + resultados.json (+ slicer.json)."""
    folder = Path(folder)
    res = json.loads((folder / "resultados.json").read_text(encoding="utf-8"))["piezas"]
    sl = folder / "slicer.json"
    sl = json.loads(sl.read_text(encoding="utf-8")) if sl.exists() else {}
    heads = [k.split("_")[0] for k in res]
    out = []
    for stem, info in res.items():
        step = folder / "step" / f"{stem}.step"
        if not step.exists():
            continue
        head = stem.split("_")[0]
        qty = sl.get(stem, {}).get("cant") or info.get("cant") or info.get("qty") or (2 if head.rstrip("stbe").startswith(PAIRS) else 1)
        pct = sl.get(stem, {}).get("relleno_pct")
        r = info.get("relleno", pct / 100 if pct else 0.4)      # old folders keep the infill only in slicer.json
        g = sl.get(stem, {}).get("g")
        extra = [f"{title or prefix}: pieza {stem}.", "Cotas en mm. Tolerancias generales según ISO 2768-m.",
                 f"Impresión: P1P, PETG, 0.20 mm, 3 paredes, giroide {infill_txt(r)}, "
                 f"{'con' if info.get('soportes', sl.get(stem, {}).get('soportes')) else 'sin'} soportes."]
        if g:
            extra.append(f"Slicer (OrcaSlicer): {g:.1f} g y {sl[stem].get('h', 0):.2f} h por pieza.")
        extra.append("Para imprimir se usa el STL o el 3MF, no este plano: el plano sirve para verificar y para el informe.")
        out.append(SimpleNamespace(code=f"{prefix}_{head if heads.count(head) == 1 else stem}", stem=stem, name=info.get("nombre", stem), step=step,
                                   material="Acrílico" if r is None else "PETG", infill=infill_txt(r), keys=[],
                                   n=lambda D, q=qty: q, qty_txt=f"{qty} por {'boya' if 'boya' in folder.name else 'nodo'}", extra_notes=extra,
                                   orient_txt=ORIENT_TXT.get(info.get("orient"), info.get("orient"))))
    return out


def merge(prefixes, cover=None, out=None):
    """One PDF: the cover (if any) and the sheets of planos/cad_final/<prefix>/, prefix by prefix."""
    from pypdf import PdfReader, PdfWriter
    out = Path(out or OUT.parent / "PLANOS_LanternGuard.pdf")
    w = PdfWriter()
    if cover:
        w.append(PdfReader(str(cover)))
    for pre in prefixes:
        for f in sorted((OUT / pre).glob("*.pdf")):
            w.append(PdfReader(str(f)))
    with open(out, "wb") as fh:
        w.write(fh)
    return out


def main_folder(folder, prefix, title=None):
    fails = []
    for pz in folder_pieces(folder, prefix, title):
        try:
            s = sheet(pz, cq.importers.importStep(str(pz.step)).val(), OUT / prefix)
            print("plano", pz.code, "escala", s)
        except Exception as e:  # noqa: BLE001
            fails.append(f"{pz.code}: {e}")
            print("FALLA", pz.code, e)
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


def main(codes=None):
    fails = []
    for pz in Z.PIEZAS:
        if codes and pz.code not in codes:
            continue
        try:
            s = sheet(pz, load(pz))
            print("plano", pz.code, "escala", s)
        except Exception as e:  # noqa: BLE001
            fails.append(f"{pz.code}: {e}")
            print("FALLA", pz.code, e)
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--carpeta" in a:
        kw = {k: a[a.index(f"--{k}") + 1] for k in ("carpeta", "prefijo", "titulo") if f"--{k}" in a}
        raise SystemExit(main_folder(kw["carpeta"], kw["prefijo"], kw.get("titulo")))
    if a[:1] == ["--unir"]:
        cover = a[a.index("--portada") + 1] if "--portada" in a else None
        print("written", merge([x for x in a[1:] if x not in ("--portada", cover)], cover))
        raise SystemExit(0)
    raise SystemExit(main(a))
