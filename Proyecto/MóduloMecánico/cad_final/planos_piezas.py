"""Simple drawing per piece (A4, PNG + PDF) projected from its STEP with OCCT hidden-line removal.

    python planos_piezas.py [M1 M3p ...]      (or: python build.py --planos)   -> ../planos/cad_final/<code>.{png,pdf}

Three first-angle views (front, top, side) with the overall dimensions measured on the projected outline, plus the
table of important dimensions from piezas.py (value, params.py name, estado). The projection helpers follow
../cad/planos.py, which is not imported because it loads the old cad/ params at import time.
"""
import logging
import sys
import textwrap
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


def sheet(pz, shape):
    fig = plt.figure(figsize=(297 / 25.4, 210 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 297)
    ax.set_ylim(0, 210)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((8, 8), 281, 194, fill=False, lw=1.2))
    raw = {k: project(shape, n, vx) for k, (n, vx) in VIEWS.items()}
    ext = {k: extent(v) for k, v in raw.items()}
    size = {k: e[1] - e[0] for k, e in ext.items()}
    # drawing area: x 16..185, y 16..194; front top-left, top below it, side to the right of the front
    w_need = size["frente"][0] + size["lado"][0]
    h_need = size["frente"][1] + size["planta"][1]
    s = next((sc for sc in SCALES if w_need * sc <= 125 and h_need * sc <= 140), SCALES[-1])
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
    ax.text(x0, 93, "* por confirmar (estimado o del fabricante)", fontsize=5.8, va="top", color="#444")
    # notes for the new design
    y = 87
    ax.text(x0, y, "Notas", fontsize=7, weight="bold", va="top")
    y -= 4.2
    for i, t in enumerate(notes(pz), 1):
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
    qt = f"{q[0]} por nodo" if len(set(q)) == 1 else "según el aro (ver MEDIDAS.md)"
    ax.text(tx + 2, ty + 15, f"Escala {('%g:1' % s) if s >= 1 else ('1:%g' % (1 / s))} (A4)   Cantidad: {qt}", fontsize=6.3, va="center")
    ax.text(tx + 2, ty + 5, "LanternGuard · Equipo 02 · desde el modelo (cad_final); revisión = commit de git", fontsize=5.6,
            va="center")
    ax.text(16, 12, "Proyección ISO-E (primer diedro). Medidas generales leídas del modelo. NO LISTO PARA IMPRIMIR "
            "mientras haya cotas por confirmar.", fontsize=5.8, color="#444")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{pz.code}.pdf", metadata={"CreationDate": None})  # same model, same bytes
    fig.savefig(OUT / f"{pz.code}.png", dpi=150, facecolor="white")
    plt.close(fig)
    return s


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
    raise SystemExit(main(sys.argv[1:]))
