"""Fase D: ensambles del nodo sobre la linterna de referencia, un caso por aro.

python ensambles.py build            -> construye cada pieza una vez y la guarda como BREP en salida/ensambles/_cache
python ensambles.py case <caso>      -> interferencias, barrido de bisagra, apice minimo, renders y STEP de un caso
python ensambles.py report           -> une los JSON de los casos en reporte_ensambles.md
Casos: 100, 100e1 (variante con 1 extension por lado), 200, 300, 500.
Marco comun: el de la caja (fondo exterior z = 0); el fondo del riel queda en z_rail.
"""
import json
import math
import sys
import time
from itertools import combinations
from pathlib import Path

import cadquery as cq
import numpy as np

import camara
import caja_central as CC
import capsula
import gancho
import layout
import riel
from params import (CAM_TILT_DEG, CARRIAGE_L, CARRIAGE_TRAVEL, CORD_CLEAR, HOOK_DROP, INTERF_TOL, LANTERN_APEX_H,
                    LANTERN_CORD_AZ, LANTERN_CORD_D, LANTERN_NET_K, LANTERN_NET_T, LANTERN_ROD_D,
                    PLATE_POCKET_LAYERS, RAIL_CENTRAL_L, RAIL_EXT_L, RAIL_EXT_PER_RING, RING_DIAMETERS, SWEEP_S,
                    SWEEP_TILT_STEP)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "ensambles"
CACHE = OUT / "_cache"
LAP = riel.LAP
Z0, Z1 = cq.Vector(0, 0, 0), cq.Vector(0, 0, 1)
CASES = {"100": (100.0, None), "100e1": (100.0, 1), "200": (200.0, None), "300": (300.0, None), "500": (500.0, None)}
S_NOM = CARRIAGE_TRAVEL
TILTS = [int(t) for t in np.arange(0, 90 + 1e-9, SWEEP_TILT_STEP)]


# ------------------------------------------------------------------ pieces (built once, cached as BREP)
def build_pieces():
    lay = layout.build(floors=1)
    c = camara.dims(lay)
    ch = camara.chamber_solid(lay, PLATE_POCKET_LAYERS)
    pc = {"caja": CC.box_body(lay).val(), "tapa": CC.box_lid(lay).val(), "riel_central": riel.central(lay, c).val(),
          "riel_ext": riel.ext(c).val(), "riel_punta": riel.punta(c).val(), "gancho": gancho.gancho().val(), "carro": capsula.carriage().val(),
          "carro_perilla_libre": capsula.knob_free().val(), "cap_M4": capsula.capsule_body().val(),
          "cap_M5": capsula.capsule_lid().val(), "cap_M6": capsula.bezel().val(), "cap_M7": capsula.window_disc().val(),
          "casquillo": gancho.bushings()[f"M13_casquillo_D{int(LANTERN_ROD_D)}"].val()}
    for k, v in CC.trays(lay).items():
        pc[f"bandeja_{k}"] = v.val()
    for k, v in ch.items():
        if k.startswith("tapa_bolsillo"):
            pc[k] = v.val()
    for i, pl in enumerate(camara.plates_solid(lay, PLATE_POCKET_LAYERS)):
        pc[f"pletina_{i}"] = pl.val() if hasattr(pl, "val") else pl
    return pc, c


def cache_pieces():
    CACHE.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    pc, c = build_pieces()
    for k, v in pc.items():
        v.exportBrep(str(CACHE / f"{k}.brep"))
    (CACHE / "dims.json").write_text(json.dumps({"z_rail": c.z_rail, "x_joint": c.x_joint}))
    print("pieces cached:", len(pc), f"{time.time() - t0:.0f}s", "z_rail", c.z_rail, "x_joint", c.x_joint)


def load_pieces():
    pc = {p.stem: cq.Shape.importBrep(str(p)) for p in CACHE.glob("*.brep")}
    d = json.loads((CACHE / "dims.json").read_text())
    return pc, d["z_rail"], d["x_joint"]


# ------------------------------------------------------------------ placement
def put(shape, x0, side, dz):
    """Shape in a +X frame -> world: translate to (x0, 0, dz), and the -X side is the same part turned 180 deg about Z."""
    s = shape.moved(cq.Location(cq.Vector(x0, 0, dz)))
    return s.rotate(Z0, Z1, 180) if side < 0 else s


def tip_x(n, xj):
    assert abs(xj - riel.X_JOINT) < 1e-9
    return riel.tip_x(n)


def comp(shapes):
    return cq.Compound.makeCompound(list(shapes))


def capsule_carriage_frame(pc, tilt):
    return [capsula.place_capsule(pc[k], tilt) for k in ("cap_M4", "cap_M5", "cap_M6", "cap_M7")]


def hook_set(pc, D, z_rail, side):
    lat, kn = gancho.placed_parts()
    L = gancho.hook_layout()
    free = cq.Solid.makeCylinder(L["free_d"] / 2, -gancho.FL_T - L["jaw_top_abs"], cq.Vector(L["xk"], 0, L["jaw_top_abs"]), Z1)
    b = pc["casquillo"].moved(cq.Location(cq.Vector(0, 0, -HOOK_DROP)))
    sg = "+X" if side > 0 else "-X"
    x0, dz = D / 2, z_rail
    return {f"M9 gancho {sg}": (put(pc["gancho"], x0, side, dz), "gancho"),
            f"M14 pestillo {sg}": (put(lat, x0, side, dz), "gancho"),
            f"M12 perilla {sg}": (put(kn, x0, side, dz), "gancho"),
            f"M13 casquillo {sg}": (put(b, x0, side, dz), "gancho"),
            f"cilindro libre perilla gancho {sg}": (put(free, x0, side, dz), "gancho_libre")}


def node_parts(pc, z_rail, xj, D, n, s, tilt):
    """name -> (shape, group) in the box frame; carriage at s, capsule at tilt."""
    out = {"M1 caja": (pc["caja"], "caja"), "M2 tapa": (pc["tapa"], "caja"),
           "M3 riel central": (pc["riel_central"], "riel")}
    for k, v in pc.items():
        if k.startswith("bandeja_"):
            out["M11 " + k] = (v, "caja")
        elif k.startswith("tapa_bolsillo"):
            out[k] = (v, "riel")
        elif k.startswith("pletina_"):
            out["lastre " + k] = (v, "lastre")
    for side in (1, -1):
        sg = "+X" if side > 0 else "-X"
        for k, (name, x0) in enumerate(riel.placements(n)):
            label = f"M3 riel ext {sg} {k + 1}" if name == "ext" else f"M3 riel punta {sg}"
            out[label] = (put(pc[f"riel_{name}"], x0, side, 0), "riel")
        out.update(hook_set(pc, D, z_rail, side))
        xo = tip_x(n, xj) - s
        out[f"M10 carro {sg}"] = (put(pc["carro"], xo, side, z_rail), "carro")
        out[f"cilindro libre perilla carro {sg}"] = (put(pc["carro_perilla_libre"], xo, side, z_rail), "carro_libre")
        out[f"capsula M4-M7 {sg}"] = (put(comp(capsule_carriage_frame(pc, tilt)), xo, side, z_rail), "capsula")
    return out


def lantern(D, z_rod, apex_h):
    R = D / 2
    ring = cq.Solid.makeTorus(R, LANTERN_ROD_D / 2, cq.Vector(0, 0, z_rod), Z1)
    cords = cords_at(D, z_rod, apex_h)
    h = LANTERN_NET_K * D
    net = cq.Solid.makeCylinder(R, h, cq.Vector(0, 0, z_rod - h), Z1).cut(
        cq.Solid.makeCylinder(R - LANTERN_NET_T, h + 2, cq.Vector(0, 0, z_rod - h - 1), Z1))
    return ring, cords, net


def cords_at(D, z_rod, apex_h, extra_r=0.0):
    out = []
    for a in LANTERN_CORD_AZ:
        p = cq.Vector(D / 2 * math.cos(math.radians(a)), D / 2 * math.sin(math.radians(a)), z_rod)
        q = cq.Vector(0, 0, z_rod + apex_h)
        v = q - p
        out.append(cq.Solid.makeCylinder(LANTERN_CORD_D / 2 + extra_r, v.Length, p, v))
    return out


# ------------------------------------------------------------------ boolean helpers
def bbox(sh):
    b = sh.BoundingBox()
    return (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


def bb_hit(a, b, tol=0.0):
    return (a[0] <= b[1] + tol and b[0] <= a[1] + tol and a[2] <= b[3] + tol and b[2] <= a[3] + tol
            and a[4] <= b[5] + tol and b[4] <= a[5] + tol)


def common(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception as e:  # noqa: BLE001
        print("   boolean failed:", e, flush=True)
        return float("nan")


def tess_mesh(shapes, tol=0.2):
    import trimesh
    ms = []
    for sh in shapes:
        v, t = sh.tessellate(tol, 0.3)
        if len(t):
            ms.append(trimesh.Trimesh(np.array([p.toTuple() for p in v]), np.array(t), process=False))
    return trimesh.util.concatenate(ms)


def surface_points(shapes, spacing=0.5):
    m = tess_mesh(shapes)
    n = int(min(2_000_000, max(50_000, m.area / spacing ** 2)))
    pts = np.vstack([m.sample(n), m.vertices])
    return pts


def min_apex(D, z_rod, node_shapes):
    """Smallest apex height for which every cord axis stays >= radius + CORD_CLEAR from every node surface, with the
    apex itself CORD_CLEAR above the highest node point (the lantern hangs from it, the node sits below).
    Scan upward from that floor on a grid (first clear value), then bisect between the last blocked and the first clear."""
    from scipy.spatial import cKDTree
    pts_all = surface_points(node_shapes, 0.7)
    tree = cKDTree(pts_all)
    need = LANTERN_CORD_D / 2 + CORD_CLEAR + 0.7            # 0.7 = surface sampling margin
    R = D / 2
    h_floor = float(pts_all[:, 2].max() - z_rod + CORD_CLEAR)

    def dist(H):
        d = np.inf
        for a in LANTERN_CORD_AZ:
            p = np.array([R * math.cos(math.radians(a)), R * math.sin(math.radians(a)), z_rod])
            q = np.array([0, 0, z_rod + H])
            n = int(max(20, np.linalg.norm(q - p) / 2.0))
            pts = p + (q - p) * np.linspace(0, 1, n)[:, None]
            d = min(d, tree.query(pts)[0].min())
        return d

    grid = np.concatenate([[h_floor], h_floor * np.geomspace(1.0, 3000.0 / h_floor, 40)[1:]])
    res = [(float(H), dist(H)) for H in grid]
    d_far = res[-1][1]
    ok = [k for k, (H, d) in enumerate(res) if d >= need]
    if not ok:
        return dict(min_H=None, h_floor=h_floor, d_at_max=float(d_far), non_monotone=False,
                    note="ninguna altura entre el techo del nodo y 3000 mm deja 10 mm de aire")
    i = ok[0]
    lo, hi = (res[i - 1][0] if i else h_floor), res[i][0]
    if i:
        for _ in range(20):
            mid = (lo + hi) / 2
            if dist(mid) >= need:
                hi = mid
            else:
                lo = mid
    non_mono = any(d < need for H, d in res[i:])
    return dict(min_H=float(hi), h_floor=h_floor, d_at_max=float(d_far), non_monotone=bool(non_mono),
                note="hay alturas mayores que vuelven a fallar" if non_mono else "")


# ------------------------------------------------------------------ one case
def run_case(case):
    D, n_over = CASES[case]
    n = RAIL_EXT_PER_RING[D] if n_over is None else n_over
    pc, z_rail, xj = load_pieces()
    z_rod = z_rail - HOOK_DROP
    tip = tip_x(n, xj)
    t0 = time.time()
    res = dict(case=case, D=D, n_ext=n, tip=tip, rail_L=2 * tip, z_rail=z_rail, z_rod=z_rod, s_nom=S_NOM,
               tilt_nom=CAM_TILT_DEG)

    nodes = node_parts(pc, z_rail, xj, D, n, S_NOM, CAM_TILT_DEG)
    ring, cords, net = lantern(D, z_rod, LANTERN_APEX_H)
    bbs = {k: bbox(v[0]) for k, v in nodes.items()}
    allb = [b for k, b in bbs.items() if "libre" not in k]
    res["bbox"] = dict(x=(min(b[0] for b in allb), max(b[1] for b in allb)), y=(min(b[2] for b in allb), max(b[3] for b in allb)),
                       z=(min(b[4] for b in allb), max(b[5] for b in allb)))

    # node pairs
    skip_same = {"caja", "riel", "lastre", "carro", "carro_libre", "capsula"}
    pairs = []
    names = list(nodes)
    for a, b in combinations(names, 2):
        ga, gb = nodes[a][1], nodes[b][1]
        if ga == gb and ga in skip_same:
            continue
        if ga == gb == "gancho" and a.split()[-1] == b.split()[-1]:
            continue
        if {ga, gb} == {"gancho", "gancho_libre"} and a.split()[-1] == b.split()[-1]:
            continue
        if {ga, gb} <= {"gancho_libre", "carro_libre"}:
            continue
        if not bb_hit(bbs[a], bbs[b]):
            continue
        v = common(nodes[a][0], nodes[b][0])
        pairs.append((a, b, v))
    res["pairs"] = [p for p in pairs if not (p[2] <= INTERF_TOL)]
    res["pairs_checked"] = len(pairs)
    print(case, "pares nodo", len(pairs), "con interferencia", len(res["pairs"]), f"{time.time() - t0:.0f}s", flush=True)

    # node vs lantern
    lant = {"aro": ring, "red": net}
    for i, c in enumerate(cords):
        lant[f"cuerda {int(LANTERN_CORD_AZ[i])}"] = c
    lb = {k: bbox(v) for k, v in lant.items()}
    lrows = []
    for a, (sh, g) in nodes.items():
        for ln, ls in lant.items():
            if bb_hit(bbs[a], lb[ln]):
                v = common(sh, ls)
                if not (v <= INTERF_TOL):
                    lrows.append((a, ln, v))
    res["lantern"] = lrows
    print(case, "nodo vs linterna", len(lrows), f"{time.time() - t0:.0f}s", flush=True)

    # carriage (and its free knob cylinder) against the rest, for the three carriage positions
    others = {k: v for k, v in nodes.items() if v[1] in ("caja", "riel", "lastre", "gancho", "gancho_libre")}
    ob = {k: bbs[k] for k in others}
    car_s = {}
    for s in SWEEP_S:
        xo = tip - s
        for side in (1, -1):
            sg = "+X" if side > 0 else "-X"
            for nm, key, g in (("M10 carro", "carro", "carro"), ("cilindro libre perilla carro", "carro_perilla_libre", "carro_libre")):
                sh = put(pc[key], xo, side, z_rail)
                b = bbox(sh)
                for on, (osh, og) in others.items():
                    if g == "carro_libre" and og == "gancho_libre":
                        continue
                    if bb_hit(b, ob[on]):
                        v = common(sh, osh)
                        if not (v <= INTERF_TOL):
                            car_s.setdefault(f"{nm} {sg} | {on}", {})[str(int(s))] = v
    res["carro_s"] = car_s
    print(case, "carro vs resto por s", len(car_s), f"{time.time() - t0:.0f}s", flush=True)

    # hinge sweep, +X side (the node and the lantern are symmetric in X)
    static = {k: v for k, v in nodes.items() if v[1] in ("caja", "riel", "lastre", "gancho", "gancho_libre")}
    static.update({"aro": (ring, "l"), "red": (net, "l")})
    for i, c in enumerate(cords):
        static[f"cuerda {int(LANTERN_CORD_AZ[i])}"] = (c, "l")
    sb = {k: bbox(v[0]) for k, v in static.items()}
    sweep = {}
    for s in SWEEP_S:
        xo = tip - s
        car = put(pc["carro"], xo, 1, z_rail)
        cb = bbox(car)
        for t in TILTS:
            cap = put(comp(capsule_carriage_frame(pc, t)), xo, 1, z_rail)
            cpb = bbox(cap)
            hits = {}
            for on, (osh, og) in static.items():
                if bb_hit(cpb, sb[on]):
                    v = common(cap, osh)
                    if not (v <= INTERF_TOL):
                        hits[on] = v
            if bb_hit(cpb, cb):
                v = common(cap, car)
                if not (v <= INTERF_TOL):
                    hits["M10 carro +X"] = v
            sweep[f"{int(s)}|{t}"] = hits
        print(case, "barrido s", s, f"{time.time() - t0:.0f}s", flush=True)
    res["sweep"] = sweep

    # minimum apex height
    solids = [v[0] for k, v in nodes.items() if v[1] not in ("gancho_libre", "carro_libre")]
    res["apex"] = min_apex(D, z_rod, solids)
    print(case, "apice minimo", res["apex"], f"{time.time() - t0:.0f}s", flush=True)

    # renders and STEP
    from render import render
    items = [(v[0], col, op, True, None) for k, v in nodes.items() if v[1] not in ("gancho_libre", "carro_libre")
             for col, op in [({"caja": "#5b8fb9", "riel": "#3a9d7a", "lastre": "#777777", "gancho": "#c9a227",
                               "carro": "#e07b39", "capsula": "#3a7ca5"}[v[1]], 1.0 if v[1] != "caja" else 0.55)]]
    items += [(ring, "#8a8a8a", 0.8, False, None), (net, "#b9d6e8", 0.25, False, None)] + [(c, "#c0504d", 0.9, False, None) for c in cords]
    for view, tag in (("iso", "iso"), ("frontal", "lado")):
        render(items, OUT / f"ensamble_D{case}_{tag}.png", view, f"Ensamble D{case}: {n} ext/lado, carro s={int(S_NOM)}, tilt {int(CAM_TILT_DEG)}")
    comp([v[0] for v in nodes.values() if v[1] not in ("gancho_libre", "carro_libre")] + [ring, net] + cords).exportStep(
        str(OUT / f"ensamble_D{case}.step"))
    res["seconds"] = time.time() - t0
    (OUT / f"_res_{case}.json").write_text(json.dumps(res, indent=1, default=float))
    print(case, "listo", f"{res['seconds']:.0f}s", flush=True)


# ------------------------------------------------------------------ report
def report():
    L = ["# Ensambles (Fase D)", "",
         "Nodo completo sobre la linterna de referencia (esquematica: aro Ø8 en el plano horizontal a la altura del centro de la varilla, "
         "4 cuerdas Ø4 a 45/135/225/315 grados, red cilindro de 1 mm de espesor y alto D). Todos los valores de la linterna son "
         "`estimado / por_verificar` (ver `params.py`, bloque `# ensambles (Fase D)`). Umbral de interferencia: volumen comun > 0.01 mm3.",
         "Posicion nominal: carro con s = 50 (punta del riel 50 mm pasada la manga), capsula a 40 grados. "
         "El lado -X es la misma pieza girada 180 grados sobre Z (como `riel.py`). El barrido de bisagra se calcula en el lado +X.", ""]
    data = {c: json.loads((OUT / f"_res_{c}.json").read_text()) for c in CASES if (OUT / f"_res_{c}.json").exists()}
    L += ["## Resumen", "", "| Caso | Ext/lado | Largo del riel | Bbox X | Bbox Y | Bbox Z | Pares con interferencia | Nodo vs linterna | Apice minimo (10 mm) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for c, r in data.items():
        a = r["apex"]
        ap = f"{a['min_H']:.0f} mm" if a["min_H"] else "no existe"
        b = r["bbox"]
        L.append(f"| D{c} | {r['n_ext']} | {r['rail_L']:.0f} | {b['x'][0]:.0f} a {b['x'][1]:.0f} | {b['y'][0]:.0f} a {b['y'][1]:.0f} | "
                 f"{b['z'][0]:.0f} a {b['z'][1]:.0f} | {len(r['pairs'])} | {len(r['lantern'])} | {ap} |")
    for c, r in data.items():
        title = {"100e1": "Ø100 con 1 extension por lado (variante)", "100": "Ø100 (sin extensiones, RAIL_EXT_PER_RING = 0)"}.get(c, f"Ø{c}")
        L += ["", f"## {title}", "",
              f"Largo ensamblado del riel: {r['rail_L']:.1f} mm (punta a punta, x = ±{r['tip']:.1f}). Centro de la varilla a z = {r['z_rod']:.2f}, fondo del riel z = {r['z_rail']:.2f}.",
              "", "### Interferencias entre piezas del nodo (nominal)", ""]
        if r["pairs"]:
            L += ["| Pieza A | Pieza B | mm3 |", "|---|---|---|"] + [f"| {a} | {b} | {v:.2f} |" for a, b, v in sorted(r["pairs"], key=lambda x: -x[2])]
        else:
            L.append("Ninguna.")
        L += ["", "### Carro y cilindro libre de su perilla contra el resto, segun s", ""]
        if r["carro_s"]:
            L += ["| Par | s=0 | s=50 | s=100 |", "|---|---|---|---|"]
            for k, d in sorted(r["carro_s"].items()):
                L.append(f"| {k} | " + " | ".join(f"{d.get(str(int(s)), 0):.2f}" for s in SWEEP_S) + " |")
        else:
            L.append("Ninguna.")
        L += ["", "### Nodo contra la linterna (apice 400)", ""]
        if r["lantern"]:
            L += ["| Pieza | Linterna | mm3 |", "|---|---|---|"] + [f"| {a} | {b} | {v:.2f} |" for a, b, v in sorted(r["lantern"], key=lambda x: -x[2])]
        else:
            L.append("Ninguna.")
        L += ["", "### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)", ""]
        L += ["| s | Tilts libres | Tilts con choque | Choques (peor tilt) |", "|---|---|---|---|"]
        for s in SWEEP_S:
            free = [t for t in TILTS if not r["sweep"][f"{int(s)}|{t}"]]
            bad = [t for t in TILTS if r["sweep"][f"{int(s)}|{t}"]]
            targets = {}
            for t in bad:
                for k, v in r["sweep"][f"{int(s)}|{t}"].items():
                    if v > targets.get(k, (0, 0))[0]:
                        targets[k] = (v, t)
            txt = "; ".join(f"{k} {v:.1f} mm3 (tilt {t})" for k, (v, t) in sorted(targets.items(), key=lambda x: -x[1][0])) or "ninguno"
            L.append(f"| {int(s)} | {free if free else 'ninguno'} | {bad if bad else 'ninguno'} | {txt} |")
        a = r["apex"]
        L += ["", "### Apice minimo de las cuerdas", ""]
        if a["min_H"]:
            L.append(f"Altura minima del apice sobre el aro para 10 mm de aire entre cuerda y cualquier pieza del nodo: **{a['min_H']:.0f} mm** "
                     f"(piso: {a['h_floor']:.0f} mm = techo del nodo + 10). {a.get('note', '')}")
        else:
            L.append(f"No existe: {a.get('note', '')}. Aire con las cuerdas casi verticales (apice a 3000 mm, caso mas favorable): {a['d_at_max'] - LANTERN_CORD_D / 2:.1f} mm entre la superficie de la cuerda y el nodo (piso de altura {a['h_floor']:.0f} mm).")
    (HERE / "reporte_ensambles.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("reporte escrito")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "build":
        cache_pieces()
    elif cmd == "case":
        run_case(sys.argv[2])
    elif cmd == "apex":
        c = sys.argv[2]
        D, n_over = CASES[c]
        n = RAIL_EXT_PER_RING[D] if n_over is None else n_over
        pc, z_rail, xj = load_pieces()
        nodes = node_parts(pc, z_rail, xj, D, n, S_NOM, CAM_TILT_DEG)
        f = OUT / f"_res_{c}.json"
        r = json.loads(f.read_text())
        r["apex"] = min_apex(D, z_rail - HOOK_DROP, [v[0] for v in nodes.values() if v[1] not in ("gancho_libre", "carro_libre")])
        f.write_text(json.dumps(r, indent=1, default=float))
        print(c, r["apex"])
    elif cmd == "report":
        report()
