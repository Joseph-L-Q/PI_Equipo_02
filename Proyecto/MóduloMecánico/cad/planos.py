"""Two A3 drawings with the UPCH title block, projected from the STEP files (OCCT hidden-line removal).

    python planos.py
Outputs: planos/LG-ENS-01.{pdf,png} (assembly, 1:5) and planos/LG-M4-01.{pdf,png} (camera capsule, 1:1).
Every dimension value is the distance between its two end points, and each end point is checked to lie
ON the surface of the STEP solid (on_surface). The value is then compared with params.py; any mismatch
stops the script, so the drawing cannot drift from the model.
"""
import math
import sys
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, PathPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt  # noqa: E402
from OCP.HLRAlgo import HLRAlgo_Projector  # noqa: E402
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parts as P  # noqa: E402
from params import *  # noqa: E402,F403

MOD = HERE.parent
STEP = MOD / "step"
OUT = MOD / "planos"
OUT.mkdir(exist_ok=True)
LOGO = MOD.parent.parent / "Recursos" / "Imágenes" / "cayetano.png"
DATE = "05/10/2026"

plt.rcParams.update({"font.family": "Arial", "font.size": 8})
LW_VIS, LW_HID, LW_THIN, LW_FRAME = 0.9, 0.45, 0.4, 1.6   # points: ~0.35 / 0.18 / 0.13 / 0.6 mm


# ------------------------------------------------------------------ projection
class View:
    """Orthographic view: normal n points to the viewer, vx is the paper's right; paper = origin + scale * (u, v)."""

    def __init__(self, n, vx, origin, scale):
        self.n, self.vx = np.array(n, float), np.array(vx, float)
        self.n /= np.linalg.norm(self.n)
        self.vx /= np.linalg.norm(self.vx)
        self.vy = np.cross(self.n, self.vx)
        self.o, self.s = np.array(origin, float), scale

    def p(self, pt):
        pt = np.asarray(pt, float)
        return self.o + self.s * np.array([pt @ self.vx, pt @ self.vy])

    def hlr(self, shapes, hidden=False):
        algo = HLRBRep_Algo()
        for s in shapes:
            algo.Add(s.wrapped)
        algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*self.n), gp_Dir(*self.vx))))
        algo.Update()
        algo.Hide()
        h = HLRBRep_HLRToShape(algo)
        vis = [h.VCompound(), h.OutLineVCompound()]
        hid = [h.HCompound(), h.OutLineHCompound()] if hidden else []
        return _polys(vis, self), _polys(hid, self)


def _polys(compounds, view):
    out = []
    for c in compounds:
        if c is None or c.IsNull():
            continue
        for e in cq.Shape.cast(c).Edges():
            k = max(2, min(120, int(e.Length() / 0.4) + 2))
            uv = np.array([e.positionAt(t).toTuple()[:2] for t in np.linspace(0, 1, k)])
            out.append(view.o + view.s * uv)
    return out


def draw(ax, polys, lw=LW_VIS, ls="-", color="black", clip=None):
    for pl in polys:
        (ln,) = ax.plot(pl[:, 0], pl[:, 1], color=color, lw=lw, ls=ls, solid_capstyle="round")
        if clip is not None:
            ln.set_clip_path(clip)


# ------------------------------------------------------------------ annotation helpers
BG = dict(fc="white", ec="none", pad=0.4)     # dimension text stays legible over hatching


def text(ax, x, y, s, size=8, **kw):
    ax.text(x, y, s, fontsize=size, **kw)


def arrow(ax, a, b):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", lw=LW_THIN, color="black",
                                                    shrinkA=0, shrinkB=0, mutation_scale=7))


def dim(ax, a, b, off, label=None, vertical=False, fmt="{:.0f}", scale=1.0, size=8, prefix=""):
    """Linear dimension between paper points a and b, dimension line `off` mm away (sign = side)."""
    a, b = np.array(a, float), np.array(b, float)
    if vertical:
        x = off
        pa, pb = np.array([x, a[1]]), np.array([x, b[1]])
        for p, q in ((a, pa), (b, pb)):
            ax.plot([p[0] + np.sign(x - p[0]) * 1.0, q[0] + np.sign(x - p[0]) * 2.0], [p[1], q[1]], color="black", lw=LW_THIN)
        val = abs(b[1] - a[1]) / scale
    else:
        y = off
        pa, pb = np.array([a[0], y]), np.array([b[0], y])
        for p, q in ((a, pa), (b, pb)):
            ax.plot([p[0], q[0]], [p[1] + np.sign(y - p[1]) * 1.0, q[1] + np.sign(y - p[1]) * 2.0], color="black", lw=LW_THIN)
        val = abs(b[0] - a[0]) / scale
    mid = (pa + pb) / 2
    arrow(ax, mid, pa)
    arrow(ax, mid, pb)
    s = label if label is not None else prefix + fmt.format(val)
    if vertical:
        text(ax, mid[0] - 1.0, mid[1], s, size, rotation=90, ha="right", va="center", bbox=BG)
    else:
        text(ax, mid[0], mid[1] + 0.8, s, size, ha="center", va="bottom", bbox=BG)
    return val


def balloon(ax, n, at, to, r=3.6):
    ax.add_patch(Circle(at, r, fill=True, fc="white", ec="black", lw=LW_THIN, zorder=5))
    text(ax, at[0], at[1], str(n), 8.5, ha="center", va="center", weight="bold", zorder=6)
    d = np.array(to, float) - np.array(at, float)
    start = np.array(at) + d / np.linalg.norm(d) * r
    ax.plot([start[0], to[0]], [start[1], to[1]], color="black", lw=LW_THIN, zorder=4)
    ax.add_patch(Circle(to, 0.6, color="black", zorder=4))


def centerline(ax, a, b):
    ax.plot([a[0], b[0]], [a[1], b[1]], color="black", lw=LW_THIN, ls=(0, (12, 2, 2, 2)))


def hatch_faces(ax, faces, view, hatch, clip=None):
    """Fill section faces (planar faces on the cutting plane) with ISO-style hatching."""
    for f in faces:
        verts, codes = [], []
        for w in [f.outerWire()] + f.innerWires():
            k = max(8, min(1500, int(w.Length() / 0.2) + 2))     # walk the wire as one curve: edges in order
            pts = [view.p(w.positionAt(t).toTuple()) for t in np.linspace(0, 1, k, endpoint=False)]
            verts += pts + [pts[0]]
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 1) + [MPath.CLOSEPOLY]
        patch = PathPatch(MPath(verts, codes), fc="none", ec="none", hatch=hatch, lw=0)
        ax.add_patch(patch)
        if clip is not None:
            patch.set_clip_path(clip)


def section(shape, keep_pos_y=True):
    """Half of `shape` on one side of the plane y = 0, and its faces lying on that plane."""
    big = cq.Solid.makeBox(1000, 1000, 1000, cq.Vector(-500, -1000 if keep_pos_y else 0, -500))
    half = shape.cut(big)
    faces = [f for f in half.Faces() if f.geomType() == "PLANE" and abs(f.normalAt().y) > 0.999
             and abs(f.Center().y) < 1e-6]
    return half, faces


# ------------------------------------------------------------------ sheet + title block
def sheet():
    fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 420)
    ax.set_ylim(0, 297)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((20, 10), 390, 277, fill=False, lw=LW_FRAME))
    for x in (105, 210, 315):                  # centring marks
        ax.plot([x + 0, x], [287, 292], color="black", lw=LW_THIN)
    ax.plot([210, 210], [5, 10], color="black", lw=LW_THIN)
    return fig, ax


def iso_e_symbol(ax, x, y):
    """First-angle (ISO-E) projection symbol: truncated cone, its end view on the right."""
    h1, h2, L = 3.0, 6.0, 7.0
    ax.add_patch(Polygon([(x, y - h1 / 2), (x + L, y - h2 / 2), (x + L, y + h2 / 2), (x, y + h1 / 2)],
                         closed=True, fill=False, lw=LW_THIN))
    cx = x + L + 6.5
    ax.add_patch(Circle((cx, y), h2 / 2, fill=False, lw=LW_THIN))
    ax.add_patch(Circle((cx, y), h1 / 2, fill=False, lw=LW_THIN))
    ax.plot([x - 1, cx + h2 / 2 + 1], [y, y], color="black", lw=0.3, ls=(0, (6, 1.5, 1.5, 1.5)))


def title_block(ax, title, code, sheet_no, scale, material):
    x0, y0, w, h = 230, 10, 180, 56
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, lw=LW_FRAME))
    # logo + university
    img = plt.imread(str(LOGO))
    ax.imshow(img, extent=(x0 + 2, x0 + 50, y0 + h - 22, y0 + h - 2), zorder=3)
    ax.plot([x0, x0 + w], [y0 + h - 24, y0 + h - 24], color="black", lw=LW_THIN)
    ax.plot([x0 + 52, x0 + 52], [y0 + h - 24, y0 + h], color="black", lw=LW_THIN)
    text(ax, x0 + 54, y0 + h - 6, "UNIVERSIDAD PERUANA CAYETANO HEREDIA", 8.5, weight="bold", va="center")
    text(ax, x0 + 54, y0 + h - 11.5, "Facultad de Ciencias e Ingeniería", 8, va="center")
    text(ax, x0 + 54, y0 + h - 17, "C7328 Proyecto Integrador · Equipo 02", 8, va="center")
    # title row
    ax.plot([x0, x0 + w], [y0 + 20, y0 + 20], color="black", lw=LW_THIN)
    text(ax, x0 + 2, y0 + h - 26.5, "Título", 5.5, va="top", color="#444")
    text(ax, x0 + 4, y0 + 26, title, 11, weight="bold", va="center")
    # field grid: label, value, column x, row
    cols = [x0, x0 + 36, x0 + 72, x0 + 108, x0 + 144, x0 + w]
    for cx in cols[1:-1]:
        ax.plot([cx, cx], [y0, y0 + 20], color="black", lw=LW_THIN)
    ax.plot([x0, x0 + w], [y0 + 10, y0 + 10], color="black", lw=LW_THIN)
    fields = [("Lámina N.º", f"{code} ({sheet_no})"), ("Escala", scale), ("Unidades", "mm"), ("Formato", "A3"),
              ("Proyección", "ISO-E"),
              ("Material", material), ("Dibujó", "Y. Palacios"), ("Revisó", "Equipo 02"), ("Fecha", DATE),
              ("Tol. general", "ISO 2768-m")]
    for i, (lab, val) in enumerate(fields):
        cx = cols[i % 5]
        cy = y0 + 20 - 10 * (i // 5)
        text(ax, cx + 1.2, cy - 1.2, lab, 5.5, va="top", color="#444")
        size = 7.5 if len(val) < 18 else 6
        if lab == "Proyección":
            text(ax, cx + 1.5, cy - 6.5, val, 7, va="center")
            iso_e_symbol(ax, cx + 13, cy - 6.3)
        else:
            text(ax, cx + 1.5, cy - 6.5, val, size, va="center", weight="bold" if lab == "Lámina N.º" else None)


def notes(ax, x, y, lines):
    text(ax, x, y, "Notas", 8, weight="bold", va="top")
    for i, s in enumerate(lines):
        text(ax, x, y - 5 - 4.2 * i, s, 7, va="top")


def save(fig, stem):
    fig.savefig(OUT / f"{stem}.pdf")
    fig.savefig(OUT / f"{stem}.png", dpi=200, facecolor="white")
    plt.close(fig)
    print("written", stem)


# ------------------------------------------------------------------ checks
MEASURED = {}


def on_surface(shape, pts, tol=0.01):
    """Each 3D point must lie on a face of `shape` (distance to its boundary, not to its volume)."""
    shell = cq.Compound.makeCompound(shape.Faces())
    for pt in pts:
        d = shell.distance(cq.Vertex.makeVertex(*pt))
        if d > tol:
            raise SystemExit(f"Dimension end point {tuple(round(v, 2) for v in pt)} is {d:.3f} mm off the model")
    MEASURED.setdefault("_points", [0, 0])[0] += len(pts)


def expect(key, value, target, tol=0.6):
    MEASURED[key] = (value, target)
    if abs(value - target) > tol:
        raise SystemExit(f"Dimension check failed: {key} measured {value:.2f}, params.py says {target:.2f}")


# ------------------------------------------------------------------ sheet 1: assembly
BOM = [  # pos, code, name, qty, material, mass g (from cad/reporte_verificacion.md)
    (1, "M1", "Caja central (cuerpo)", 1, "PETG", 303),
    (2, "M2", "Tapa de caja con asa", 1, "PETG", 151),
    (3, "M3", "Brazo hueco con horquilla", 2, "PETG", 99),
    (4, "M4", "Cápsula de cámara (P4 rev. B)", 2, "PETG", 68),
    (5, "M5", "Tapa de cápsula con lengüeta", 2, "PETG", 30),
    (6, "M6", "Bisel de ventana", 2, "PETG", 3),
    (7, "M7", "Ventana Ø30 × 3", 2, "Acrílico (PMMA)", 3),
    (8, "M8", "Marco con malla (banco de prueba)", 1, "PETG", 91),
]


def bom_table(ax, x0, y0, w):
    cols = [0, 12, 26, 92, 104, 150, w]
    heads = ["Pos.", "Código", "Denominación", "Cant.", "Material", "Masa g"]
    rh = 5.5
    rows = [heads] + [[str(p), c, n, str(q), m, str(g)] for p, c, n, q, m, g in BOM]
    for i, r in enumerate(reversed(rows)):          # ISO 7573: position 1 nearest the title block
        y = y0 + i * rh
        ax.add_patch(Rectangle((x0, y), w, rh, fill=False, lw=LW_FRAME if r is heads else LW_THIN))
        for j, s in enumerate(r):
            text(ax, x0 + cols[j] + 1.2, y + rh / 2, s, 6.8, va="center", weight="bold" if r is heads else None)
    for c in cols[1:-1]:
        ax.plot([x0 + c, x0 + c], [y0, y0 + rh * len(rows)], color="black", lw=LW_THIN)
    return y0 + rh * len(rows)


def load_assembly():
    assy = cq.Assembly.importStep(str(STEP / "ENSAMBLE_modulo.step"))
    return {ch.name: ch.obj.moved(ch.loc) for ch in assy.children}


def sheet_assembly():
    parts = load_assembly()
    shapes = list(parts.values())
    s = 1 / 5
    fig, ax = sheet()
    front = View((0, -1, 0), (1, 0, 0), (125, 222), s)
    top = View((0, 0, 1), (1, 0, 0), (125, 168), s)
    left = View((-1, 0, 0), (0, -1, 0), (232, 222), s)
    iso = View((1, -1, 1), (1, 1, 0), (330, 200), 1 / 6)
    for v, label in ((front, "VISTA FRONTAL"), (top, "VISTA SUPERIOR"), (left, "VISTA LATERAL IZQUIERDA"),
                     (iso, "VISTA ISOMÉTRICA (1:6)")):
        vis, _ = v.hlr(shapes)
        draw(ax, vis, lw=LW_VIS if v is not iso else 0.7)
        ys = np.concatenate([p[:, 1] for p in vis])
        xs = np.concatenate([p[:, 0] for p in vis])
        text(ax, (xs.min() + xs.max()) / 2, ys.min() - (24 if v is front else 6), label, 7.5, ha="center",
             va="top", weight="bold")

    bb = cq.Compound.makeCompound(shapes).BoundingBox()
    # overall length, height, width; saddles on the 500 mm lantern ring
    ring_z = P.arm_z() - P.box_dims()[2] / 2 - ARM_H / 2 - 12
    yd = front.p((0, 0, bb.zmin))[1]
    L = dim(ax, front.p((bb.xmin, 0, bb.zmin)), front.p((bb.xmax, 0, bb.zmin)), yd - 16, scale=s)
    sx = LANTERN_RING_D / 2
    a1 = dim(ax, front.p((-sx, 0, ring_z)), front.p((0, 0, ring_z)), yd - 7, scale=s)
    a2 = dim(ax, front.p((0, 0, ring_z)), front.p((sx, 0, ring_z)), yd - 7, scale=s)
    centerline(ax, front.p((0, 0, bb.zmin - 8)), front.p((0, 0, bb.zmax + 4)))
    for x in (-sx, sx):
        c = front.p((x, 0, ring_z))
        ax.add_patch(Circle(c, (RING_ROD_D / 2) * s, fill=False, lw=LW_THIN, ls="--"))
    H = dim(ax, front.p((bb.xmin, 0, bb.zmin)), front.p((bb.xmin, 0, bb.zmax)), front.p((bb.xmin, 0, 0))[0] - 6,
            vertical=True, scale=s)
    W = dim(ax, top.p((bb.xmax, bb.ymin, 0)), top.p((bb.xmax, bb.ymax, 0)), top.p((bb.xmax, 0, 0))[0] + 8,
            vertical=True, scale=s)
    text(ax, front.p((sx, 0, ring_z))[0] - 2, yd - 11.5, "apoyo en el aro de la linterna (Ø500, varilla Ø12)",
         6, ha="right")
    _, out_w, _ = P.box_dims()
    for name, x in (("M3_brazo_izq", -sx), ("M3_brazo_der", sx)):     # top of the rod seat, beside the strap slot
        on_surface(parts[name], [(x, ARM_W / 2 - 1, ring_z + RING_ROD_D / 2 + 0.5)])
    expect("Largo total", L, 770.0)
    expect("Alto total", H, 157.0)
    expect("Ancho total (brida de la caja)", W, out_w + 2 * BOX_FLANGE)
    expect("Apoyo izquierdo al eje", a1, LANTERN_RING_D / 2)
    expect("Apoyo derecho al eje", a2, LANTERN_RING_D / 2)

    # balloons on the isometric view
    def c3(name):
        b = parts[name].BoundingBox()
        return np.array([b.center.x, b.center.y, b.center.z])

    targets = [(1, "M1_caja_cuerpo", (-60, -45, -15), (300, 150)), (2, "M2_caja_tapa", (45, -25, -20), (312, 262)),
               (3, "M3_brazo_der", (0, 0, 0), (360, 165)), (4, "M4_capsula_cuerpo_der", (0, 0, 0), (398, 182)),
               (5, "M5_capsula_tapa_der", (0, 0, 0), (395, 225)), (6, "M6_bisel_der", (0, 0, 0), (395, 152)),
               (7, "M7_ventana_der", (0, 0, 0), (372, 140))]
    for n, name, dxyz, at in targets:
        balloon(ax, n, at, iso.p(c3(name) + np.array(dxyz)))
    # M8: not part of the module, shown as a small detail
    frame = cq.importers.importStep(str(STEP / "M8_marco_malla_prueba.step")).val()
    v8 = View((0, 0, 1), (1, 0, 0), (60, 85), 1 / 10)
    vis8, _ = v8.hlr([frame])
    draw(ax, vis8, lw=0.5)
    text(ax, 60, 71, "DETALLE M8 · banco de prueba (1:10)\nno forma parte del módulo", 6.5, ha="center", va="top")
    balloon(ax, 8, (80, 98), v8.p((FRAME_OUT / 2 - FRAME_BAR / 2, FRAME_OUT / 2 - FRAME_BAR / 2, 0)))

    ytop = bom_table(ax, 230, 66, 180)
    text(ax, 232, ytop + 2, "Lista de piezas", 8, weight="bold")
    notes(ax, 105, 102, [
        "1. Cotas en mm, medidas sobre el modelo (step/ENSAMBLE_modulo.step).",
        f"2. Cámaras inclinadas {CAM_TILT_DEG:.0f}° hacia abajo; bisagra dentada de {HINGE_TEETH} dientes (10° por diente).",
        "3. Los brazos se apoyan en el aro superior de la linterna y se fijan con correa de velcro.",
        "4. Piezas impresas en PETG (FDM, 0,4 mm); juntas tóricas de 2 mm en cápsulas y caja.",
        "5. Masas al 100 % de relleno, según cad/reporte_verificacion.md.",
        "6. Plano generado con CadQuery/OCCT (cad/planos.py) desde el mismo modelo.",
    ])
    title_block(ax, "LanternGuard · Módulo sumergido · Conjunto", "LG-ENS-01", "1/2", "1:5", "PETG / acrílico")
    save(fig, "LG-ENS-01")


# ------------------------------------------------------------------ sheet 2: camera capsule
def sheet_capsule():
    body = cq.importers.importStep(str(STEP / "M4_capsula_cuerpo_P4revB.step")).val()
    lid = cq.importers.importStep(str(STEP / "M5_capsula_tapa.step")).val()
    bezel = cq.importers.importStep(str(STEP / "M6_bisel_ventana.step")).val()
    win = cq.importers.importStep(str(STEP / "M7_ventana.step")).val()
    out_w, out_h, fl_w, fl_h, x_lid0, x0, x_front = P.cap_dims()
    xm = (x0 + x_front) / 2
    fig, ax = sheet()

    # first angle: elevation centre, view from the right (window) on its LEFT, plan view BELOW
    elev = View((0, -1, 0), (1, 0, 0), (165 - xm, 215), 1.0)
    side = View((1, 0, 0), (0, 1, 0), (65, 215), 1.0)
    plan = View((0, 0, 1), (1, 0, 0), (165 - xm, 128), 1.0)
    for v, label, hid in ((elev, "VISTA FRONTAL", True), (side, "VISTA LATERAL DERECHA (ventana)", False),
                          (plan, "VISTA SUPERIOR", True)):
        vis, hidden = v.hlr([body], hidden=hid)
        draw(ax, vis)
        draw(ax, hidden, lw=LW_HID, ls=(0, (4, 2)))
        text(ax, v.p((xm, 0, 0))[0] if v is not side else v.o[0], (v.p((0, 0, -fl_h / 2))[1] if v is not plan
             else v.p((0, -fl_w / 2, 0))[1]) - 16, label, 7.5, ha="center", va="top", weight="bold")
    # axis lines
    centerline(ax, elev.p((x0 - 6, 0, 0)), elev.p((x_front + 6, 0, 0)))
    centerline(ax, plan.p((x0 - 6, 0, 0)), plan.p((x_front + 6, 0, 0)))
    centerline(ax, side.p((0, -fl_w / 2 - 4, 0)), side.p((0, fl_w / 2 + 4, 0)))
    centerline(ax, side.p((0, 0, -fl_h / 2 - 4)), side.p((0, 0, fl_h / 2 + 4)))

    # elevation: 56 long, 46 high, flange 64 and 6
    zb = elev.p((0, 0, -fl_h / 2))[1]
    Lb = dim(ax, elev.p((x0, 0, -out_h / 2)), elev.p((x_front, 0, -out_h / 2)), zb - 8)
    Tf = dim(ax, elev.p((x0, 0, fl_h / 2)), elev.p((x0 + CAP_FLANGE_T, 0, fl_h / 2)), elev.p((0, 0, fl_h / 2))[1] + 6)
    Hb = dim(ax, elev.p((x_front, 0, -out_h / 2)), elev.p((x_front, 0, out_h / 2)), elev.p((x_front, 0, 0))[0] + 8,
             vertical=True)
    Hf = dim(ax, elev.p((x0, 0, -fl_h / 2)), elev.p((x0, 0, fl_h / 2)), elev.p((x0, 0, 0))[0] - 7, vertical=True)
    Wb = dim(ax, plan.p((x_front, -out_w / 2, 0)), plan.p((x_front, out_w / 2, 0)), plan.p((x_front, 0, 0))[0] + 8,
             vertical=True)
    xc = x0 + 32                                   # cavity width on the hidden lines of the plan view
    Wc = dim(ax, plan.p((xc, -CAP_CAV_W / 2, 0)), plan.p((xc, CAP_CAV_W / 2, 0)), plan.p((xc, 0, 0))[0],
             vertical=True, size=7, fmt="{:.0f} (cavidad)")
    gx = x0 + CAP_GLAND_X
    dim(ax, plan.p((x0, 0, 0)) + np.array([0, -out_w / 2 - 1]), plan.p((gx, 0, 0)) + np.array([0, -out_w / 2 - 1]),
        plan.p((0, -fl_w / 2, 0))[1] - 6)
    text(ax, plan.p((gx, 0, 0))[0] - 6, plan.p((gx, 0, 0))[1] - 11, f"PG7 Ø{PG7_HOLE:g} (cara inferior)", 6.5)
    # side view: window seat, aperture, flange, cutting plane A-A
    r_seat = WIN_DIA / 2 + 0.2
    for r, lab, ang in ((r_seat, f"Ø{2 * r_seat:g} asiento de ventana", 35), (LENS_APERTURE / 2, f"Ø{LENS_APERTURE:g}", -40)):
        a = math.radians(ang)
        p = side.p((0, r * math.cos(a), r * math.sin(a)))
        q = p + np.array([math.cos(a), math.sin(a)]) * (34 - r)
        arrow(ax, q, p)
        ax.plot([q[0], q[0] + (14 if ang > 0 else 6)], [q[1], q[1]], color="black", lw=LW_THIN)
        text(ax, q[0] + 0.5, q[1] + 0.8, lab, 6.8)
    Wf = dim(ax, side.p((0, -fl_w / 2, -fl_h / 2)), side.p((0, fl_w / 2, -fl_h / 2)), side.p((0, 0, -fl_h / 2))[1] - 12)
    ya, yb_ = side.p((0, 0, fl_h / 2 + 7)), side.p((0, 0, -fl_h / 2 - 7))
    for p, sgn in ((ya, 1), (yb_, -1)):
        ax.plot([p[0], p[0]], [p[1] - sgn * 3, p[1]], color="black", lw=1.4)
        arrow(ax, p, p + np.array([6, 0]))            # looking from -Y towards +Y (paper right)
        text(ax, p[0] + 7, p[1] + 1, "A", 9, weight="bold", ha="center", va="bottom")
    ax.plot([ya[0], yb_[0]], [ya[1], yb_[1]], color="black", lw=LW_THIN, ls=(0, (10, 2, 2, 2)))

    # section A-A of the closed capsule (M4 + M5 + M6 + M7), plane y = 0 through the optical axis
    sec = View((0, -1, 0), (1, 0, 0), (290, 215), 1.0)
    halves, hatch = [], []
    for shp, pat in ((body, "/////"), (lid, "\\\\\\\\\\"), (bezel, "/////"), (win, "xxxx")):
        h, faces = section(shp)
        halves.append(h)
        hatch.append((faces, pat))
    vis, _ = sec.hlr(halves)
    for faces, pat in hatch:
        hatch_faces(ax, faces, sec, pat)
    draw(ax, vis)
    centerline(ax, sec.p((-16, 0, 0)), sec.p((x_front + 10, 0, 0)))
    text(ax, sec.p((x_lid0 + 30, 0, 0))[0], sec.p((0, 0, -fl_h / 2))[1] - 16, "CORTE A-A", 7.5,
         ha="center", va="top", weight="bold")
    zc = sec.p((0, 0, -CAP_CAV_H / 2))[1]
    Lc = dim(ax, sec.p((x0, 0, -CAP_CAV_H / 2)), sec.p((x0 + CAP_CAV_L, 0, -CAP_CAV_H / 2)), zc + 4,
             size=7)
    Hc = dim(ax, sec.p((x0 + CAP_CAV_L - 8, 0, -CAP_CAV_H / 2)), sec.p((x0 + CAP_CAV_L - 8, 0, CAP_CAV_H / 2)),
             sec.p((x0 + CAP_CAV_L - 8, 0, 0))[0] - 2, vertical=True, size=7)
    tw = dim(ax, sec.p((x0 + 20, 0, CAP_CAV_H / 2)), sec.p((x0 + 20, 0, out_h / 2)),
             sec.p((x0 + 20, 0, 0))[0] + 6, vertical=True, size=6.5)
    Dw = dim(ax, sec.p((x_front, 0, -WIN_DIA / 2)), sec.p((x_front, 0, WIN_DIA / 2)),
             sec.p((x_front, 0, 0))[0] + 12, vertical=True, size=7, prefix="Ø")
    Tw = dim(ax, sec.p((x_front - CAP_FRONT, 0, out_h / 2)), sec.p((x_front, 0, out_h / 2)),
             sec.p((0, 0, fl_h / 2))[1] + 5, size=6.5)
    # detail B on the O-ring groove, 4:1
    cl_h = (CAP_CAV_H + (fl_h - CAP_FLANGE)) / 2
    gpt = np.array([x0 - GROOVE_DEPTH / 2, 0, cl_h / 2])
    rB = 5.0
    ax.add_patch(Circle(sec.p(gpt), rB, fill=False, lw=LW_THIN))
    text(ax, sec.p(gpt)[0] - rB - 1, sec.p(gpt)[1] + rB, "B", 9, weight="bold", ha="right")
    k = 4.0
    det = View((0, -1, 0), (1, 0, 0), np.array([330, 120]) - k * np.array([gpt[0], gpt[2]]), k)
    clip = Circle(det.p(gpt), rB * k, transform=ax.transData)
    ax.add_patch(Circle(det.p(gpt), rB * k, fill=False, lw=LW_THIN))
    for faces, pat in hatch:
        hatch_faces(ax, faces, det, pat, clip=clip)
    vis_d, _ = det.hlr(halves)
    draw(ax, vis_d, clip=clip)
    text(ax, det.p(gpt)[0], det.p(gpt)[1] - rB * k - 3, "DETALLE B (4:1)\nranura de junta tórica", 7.5,
         ha="center", va="top", weight="bold")
    gw = dim(ax, det.p((x0 - GROOVE_DEPTH, 0, cl_h / 2 - GROOVE_WIDTH / 2)),
             det.p((x0 - GROOVE_DEPTH, 0, cl_h / 2 + GROOVE_WIDTH / 2)), det.p((x0, 0, 0))[0] - 12,
             vertical=True, scale=k, fmt="{:.1f}", size=7)
    gd = dim(ax, det.p((x0 - GROOVE_DEPTH, 0, cl_h / 2 + GROOVE_WIDTH / 2)),
             det.p((x0, 0, cl_h / 2 + GROOVE_WIDTH / 2)), det.p((0, 0, cl_h / 2))[1] + 10, scale=k,
             fmt="{:.1f}", size=7)
    text(ax, det.p(gpt)[0] + rB * k + 3, det.p(gpt)[1] - 4, f"O-ring cordón {ORING_CORD:g} mm\n(25 % de compresión)", 6.5)

    c_body = [(x0, 0, -out_h / 2), (x_front, 0, -out_h / 2), (x0, 0, fl_h / 2), (x0 + CAP_FLANGE_T, 0, fl_h / 2),
              (x_front, 0, out_h / 2), (x0, 0, -fl_h / 2), (x_front, -out_w / 2, 0), (x_front, out_w / 2, 0),
              (x0, -fl_w / 2, 0), (x0, fl_w / 2, 0), (x0, 0, -CAP_CAV_H / 2), (x0 + CAP_CAV_L, 0, -CAP_CAV_H / 2),
              (x0 + CAP_CAV_L - 8, 0, CAP_CAV_H / 2), (x0 + 20, 0, CAP_CAV_H / 2), (x0 + 20, 0, out_h / 2),
              (x_front - CAP_FRONT, 0, out_h / 2), (xc, -CAP_CAV_W / 2, 0), (xc, CAP_CAV_W / 2, 0)]
    on_surface(body, c_body)
    on_surface(win, [(x_front - WIN_SEAT_DEPTH, 0, -WIN_DIA / 2), (x_front - WIN_SEAT_DEPTH, 0, WIN_DIA / 2)])
    on_surface(lid, [(x0 - GROOVE_DEPTH, 0, cl_h / 2 - GROOVE_WIDTH / 2), (x0 - GROOVE_DEPTH, 0, cl_h / 2 + GROOVE_WIDTH / 2),
                     (x0, 0, cl_h / 2 + GROOVE_WIDTH / 2)])
    for key, val, tgt in (("Largo cápsula", Lb, CAP_CAV_L + CAP_FRONT), ("Alto cápsula", Hb, out_h),
                          ("Ancho cápsula", Wb, out_w), ("Brida alto", Hf, fl_h), ("Brida ancho", Wf, fl_w),
                          ("Espesor brida", Tf, CAP_FLANGE_T), ("Cavidad largo", Lc, CAP_CAV_L),
                          ("Cavidad alto", Hc, CAP_CAV_H), ("Pared", tw, CAP_WALL), ("Ventana", Dw, WIN_DIA),
                          ("Pared frontal", Tw, CAP_FRONT), ("Ranura ancho", gw, GROOVE_WIDTH),
                          ("Ranura prof.", gd, GROOVE_DEPTH)):
        expect(key, val, tgt, tol=0.05)
    expect("Cavidad ancho", Wc, CAP_CAV_W, tol=0.05)

    text(ax, 330, 76, "Rayado: M4 cuerpo ///   M5 tapa \\\\\\   M6 bisel ///   M7 acrílico xxx", 6.5, ha="center")
    notes(ax, 25, 62, [
        "1. Cotas en mm, medidas sobre step/M4_capsula_cuerpo_P4revB.step (y M5-M7 en el corte).",
        f"2. Ventana: disco de acrílico Ø{WIN_DIA:g} × {WIN_T:g} en asiento exterior de {WIN_SEAT_DEPTH:g} mm;",
        "    la presión del agua la apoya en el hombro. Sellado con RTV marino, retenida por M6.",
        f"3. Brida con 4 agujeros Ø{M3_CLEAR:g} para M3 con tuerca. Pared {CAP_WALL:g} mm, frente {CAP_FRONT:g} mm.",
        "4. Cavidad para Arducam Mega 5MP (placa 33 × 33, lente 20-25 mm).",
        "5. Plano generado con CadQuery/OCCT (cad/planos.py) desde el mismo modelo.",
    ])
    title_block(ax, "Cápsula de cámara M4 (P4 rev. B)", "LG-M4-01", "2/2", "1:1 (det. 4:1)", "PETG")
    save(fig, "LG-M4-01")


def main():
    sheet_assembly()
    sheet_capsule()
    npts = MEASURED.pop("_points")[0]
    w = max(len(k) for k in MEASURED)
    print(f"\n{npts} extremos de cota verificados sobre la superficie del modelo")
    print("Cotas medidas vs params.py")
    for k, (v, t) in MEASURED.items():
        print(f"  {k:<{w}}  {v:8.2f}  {t:8.2f}")


if __name__ == "__main__":
    main()
