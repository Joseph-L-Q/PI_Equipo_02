"""Block 3 results pipeline: images + resultados.json for every piece, SimScale first, local CalculiX as the fallback.

    python resultados_bloque3.py                       every piece (needs no new SimScale run)
    python resultados_bloque3.py --pieza B2_cubierta_mastil_lateral --pieza B3_caja
    python resultados_bloque3.py --malla 3.0           local mesh size (mm, default 3)
    python resultados_bloque3.py --sin-api             do not even read the SimScale geometry names (everything local)

Source rule (decided, see ../../docs/DECISIONES.md): a piece is "SimScale" only if
  1. salida/simscale/<piece>.json has a `resultado` and its run_id is the one in state.json for that piece/case, and
  2. the geometry that run used is the geometry of the CURRENT STEP (name `<piece>_<sha1 of step + named step size>` read from the project), and
  3. the VTK of that exact run is on disk (salida/simscale/_res/<piece>_<run8>, or the legacy folder <piece> when run8 is not there and the
     maxima recomputed from the VTK match the JSON).
Anything else is "FEM local": the SAME case (same faces, same per-hole forces, same PETG) solved with Gmsh + CalculiX C3D10.

Outputs (paths are read by the viewer, keep them):
  docs/resultados/<piece>/{vonmises,desplazamiento,malla,condiciones}.png
  docs/resultados/resultados.json
Color scales are FIXED for every piece: von Mises 0..50 MPa (the allowable; above it the colour saturates to magenta),
displacement 0..6 mm (above it, magenta). The title of each image gives the true maximum.
FS conventions: fs = 50 / sigma_max (absolute maximum), fs_capas = 22 / sigma_p995 (between layers), fs_plano = 45 / sigma_p995 (in the layer plane);
sigma_p995 is the 99.5th percentile (the absolute maximum is dominated by the supports / load patches, a modelling artefact).
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")

import numpy as np                                      # noqa: E402

import simscale_run as SR                               # noqa: E402

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
DOCS_RES = MOD / "docs" / "resultados"
LOCAL = SR.OUT / "_local"
CLIM_VM = (0.0, 50.0)
CLIM_U = (0.0, 6.0)
SY_PLANO, SY_CAPAS = 45.0, 22.0                          # MPa, params.PETG_YIELD / PETG_YIELD_Z (fem.py convention)
STAMP_403 = "FEM local (SimScale no exportó)"
STAMP_NEW = "FEM local (SimScale aún no corre esta geometría)"
PID = {"A": "770997415227428031", "B": "5890288887472164333"}
GMSH_TO_CCX_TET10 = [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]       # also the VTK_QUADRATIC_TETRA order


# ------------------------------------------------------------------------------------------------ local FEM
def _ccx():
    import fem
    return fem.CCX


def mesh_with_faces(sh, faces, size, work):
    """Gmsh second-order mesh of the (imprinted) solid. Returns nodes {tag: xyz}, tets (n,10), face_tris {cq face index: [(6 node tags)]}.
    gmsh surfaces are matched to the cadquery faces by centre of mass + area (the STEP is written and read back, ordering is not trusted)."""
    import gmsh
    step = work / "geom.step"
    sh.exportStep(str(step))
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("m")
        gmsh.model.occ.importShapes(str(step))
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMax", size)
        gmsh.option.setNumber("Mesh.MeshSizeMin", size / 3)
        gmsh.option.setNumber("Mesh.ElementOrder", 2)
        gmsh.option.setNumber("Mesh.SecondOrderLinear", 1)
        gmsh.model.mesh.generate(3)
        tags, xyz, _ = gmsh.model.mesh.getNodes()
        nodes = dict(zip(tags.astype(int), xyz.reshape(-1, 3)))
        _, en = gmsh.model.mesh.getElementsByType(11)
        tets = en.astype(int).reshape(-1, 10)
        gs = []
        for dim, tag in gmsh.model.getEntities(2):
            c = gmsh.model.occ.getCenterOfMass(dim, tag)
            a = gmsh.model.occ.getMass(dim, tag)
            _, _, nt = gmsh.model.mesh.getElements(dim, tag)
            tri = np.concatenate([np.asarray(x, int).reshape(-1, 6) for x in nt]) if len(nt) else np.zeros((0, 6), int)
            gs.append((np.array(c), a, tri))
    finally:
        gmsh.finalize()
    cq_c = np.array([f.Center().toTuple() for f in faces])
    cq_a = np.array([f.Area() for f in faces])
    face_tris, used = {}, set()
    for i in range(len(faces)):
        best, bd = None, 1e9
        for j, (c, a, _) in enumerate(gs):
            if j in used:
                continue
            d = np.linalg.norm(c - cq_c[i]) + abs(a - cq_a[i]) / max(cq_a[i], 1e-6) * 5
            if d < bd:
                best, bd = j, d
        if best is not None and bd < 0.2:
            used.add(best)
            face_tris[i] = gs[best][2]
    return nodes, tets, face_tris


def load_nodal(nodes, tris, force):
    """Consistent nodal forces of a total force spread uniformly over triangles T6: corners 0, mid-sides area/3 each."""
    out = {}
    areas = []
    for t in tris:
        p = [nodes[int(k)] for k in t[:3]]
        areas.append(0.5 * np.linalg.norm(np.cross(p[1] - p[0], p[2] - p[0])))
    tot = sum(areas)
    for t, a in zip(tris, areas):
        for k in t[3:]:
            out[int(k)] = out.get(int(k), 0.0) + np.asarray(force, float) * (a / tot / 3.0)
    return out


def write_inp(path, nodes, tets, fixed, forces, gravity):
    L = ["*HEADING", "LanternGuard resultados_bloque3", "*NODE"]
    L += [f"{k},{v[0]:.6f},{v[1]:.6f},{v[2]:.6f}" for k, v in nodes.items()]
    L += ["*ELEMENT,TYPE=C3D10,ELSET=EALL"]
    L += [f"{i + 1}," + ",".join(str(t[j]) for j in GMSH_TO_CCX_TET10) for i, t in enumerate(tets)]
    ids = sorted(fixed)
    L.append("*NSET,NSET=FIX")
    L.extend(",".join(str(n) for n in ids[i:i + 12]) for i in range(0, len(ids), 12))
    L.append("*NSET,NSET=NALL")
    allk = sorted(nodes)
    L.extend(",".join(str(n) for n in allk[i:i + 12]) for i in range(0, len(allk), 12))
    L += ["*MATERIAL,NAME=PETG", "*ELASTIC", f"{SR.E_PA / 1e6:g},{SR.NU:g}", "*DENSITY", f"{SR.RHO * 1e-12:.6e}",
          "*SOLID SECTION,ELSET=EALL,MATERIAL=PETG", "*STEP", "*STATIC", "*BOUNDARY", "FIX,1,3,0.0"]
    if gravity:
        L += ["*DLOAD", f"EALL,GRAV,{SR.G * 1e3:.4f},0,0,-1"]
    L += ["*CLOAD"]
    for k in sorted(forces):
        for c in range(3):
            if abs(forces[k][c]) > 1e-12:
                L.append(f"{k},{c + 1},{forces[k][c]:.8f}")
    L += ["*NODE PRINT,NSET=NALL", "U", "*EL PRINT,ELSET=EALL", "S", "*END STEP"]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def solve_local(piece, size, force=False):
    """Local CalculiX solve of the SimScale case of `piece`. Returns dict(stats, grid (pyvista, point+cell data), sh, faces, case)."""
    import pyvista as pv
    import fem
    sh, faces, info, case = SR.prepare(piece)
    case_eq = SR.expand_remote(case, faces)
    loads = case_eq["loads_equivalentes"]
    work = LOCAL / piece
    work.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    nodes, tets, ftris = mesh_with_faces(sh, faces, size, work)
    need = {i for _, ix in case["fixed"] for i in ix} | {i for ld in loads for i in ld["idx"]}
    missing = sorted(need - set(ftris))
    if missing:
        raise RuntimeError(f"{piece}: {len(missing)} support/load faces could not be matched to the gmsh surfaces {missing[:5]}")
    fixed = set()
    for _, ix in case["fixed"]:
        for i in ix:
            fixed |= {int(k) for t in ftris[i] for k in t}
    forces = {}
    for ld in loads:
        tris = np.concatenate([ftris[i] for i in ld["idx"]])
        for k, v in load_nodal(nodes, tris, ld["force_N"]).items():
            forces[k] = forces.get(k, 0.0) + v
    tot = np.sum(list(forces.values()), axis=0)
    want = np.sum([np.array(ld["force_N"], float) for ld in loads], axis=0)
    if np.linalg.norm(tot - want) > 1e-6 * (1 + np.linalg.norm(want)):
        raise RuntimeError(f"{piece}: nodal forces {tot} differ from the case {want}")
    inp = work / "caso.inp"
    write_inp(inp, nodes, tets, fixed, forces, case["gravity"])
    r = subprocess.run([str(_ccx()), "-i", "caso"], cwd=work, capture_output=True, text=True, timeout=3600)
    dat = work / "caso.dat"
    if r.returncode != 0 or not dat.exists():
        raise RuntimeError(f"ccx rc={r.returncode}: {(r.stdout + r.stderr)[-400:]}")
    U, S = fem.read_dat(dat)
    keys = list(nodes)
    idx = {k: i for i, k in enumerate(keys)}
    pts = np.array([nodes[k] for k in keys])
    cells = np.hstack([[10] + [idx[int(x)] for x in t[GMSH_TO_CCX_TET10]] for t in tets])
    grid = pv.UnstructuredGrid(cells, np.full(len(tets), 24, np.uint8), pts)
    grid.cell_data["vm_MPa"] = np.array([S.get(i + 1, 0.0) for i in range(len(tets))])
    grid.point_data["u_mm"] = np.array([U.get(k, 0.0) for k in keys])
    vm = grid.cell_data["vm_MPa"]
    p995 = float(np.percentile(vm, 99.5))
    c = grid.cell_centers().points
    stats = dict(nodos=int(len(keys)), celdas=int(len(tets)), sigma_max_MPa=float(vm.max()), sigma_p995_MPa=p995,
                 sigma_max_en_mm=c[int(vm.argmax())].round(1).tolist(), u_max_mm=float(grid.point_data["u_mm"].max()),
                 malla_mm=size, segundos=round(time.time() - t0, 1), solver="CalculiX 2.22 C3D10, Gmsh")
    (work / "stats.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    return dict(stats=stats, grid=grid, sh=sh, faces=faces, case=case)


# ------------------------------------------------------------------------------------------------ SimScale side
def load_state():
    f = SR.OUT / "state.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def case_key(piece, state):
    """state.json key `<piece>/<case name>` of the current case of the piece (case name from the code)."""
    sh, faces, info, case = SR.prepare(piece)
    return f"{piece}/{case['name']}", case


def geometry_is_current(api, piece, group, gid, named_now, src_step):
    """True when the SimScale geometry `gid` carries the name of the digest of the CURRENT step."""
    import simscale_sdk as sim
    digest = hashlib.sha1(src_step.read_bytes() + named_now.stat().st_size.to_bytes(8, "little")).hexdigest()[:8]
    gname = f"{piece}_{digest}"
    pid = PID[group]
    for g in sim.GeometriesApi(api).get_geometries(pid, limit=100).embedded:
        if g.geometry_id == gid:
            return g.name == gname, g.name, gname
    return False, None, gname


def vtu_for(piece, run_id):
    for d in (SR.OUT / "_res" / f"{piece}_{run_id[:8]}", SR.OUT / "_res" / piece):
        v = sorted(d.glob("**/*.vtu"))
        if v:
            return v[0]
    return None


def read_simscale(vtu, expect):
    """(pyvista grid with vm_MPa / u_mm point data, stats); None when the maxima do not match the JSON of the run."""
    import pyvista as pv
    m = pv.read(str(vtu))
    m = m.combine() if hasattr(m, "combine") else m
    vm = np.asarray(m["von Mises stress"], float) / 1e6
    u = np.linalg.norm(np.asarray(m["displacement"], float), axis=1) * 1e3
    m.point_data["vm_MPa"], m.point_data["u_mm"] = vm, u
    stats = dict(nodos=int(m.n_points), celdas=int(m.n_cells), sigma_max_MPa=float(vm.max()), sigma_p995_MPa=float(np.percentile(vm, 99.5)),
                 sigma_max_en_mm=(np.asarray(m.points)[int(vm.argmax())] * 1e3).round(1).tolist(), u_max_mm=float(u.max()))
    if expect and abs(stats["sigma_max_MPa"] - expect["sigma_max_MPa"]) > 0.02 * expect["sigma_max_MPa"]:
        return None
    return m, stats


# ------------------------------------------------------------------------------------------------ images
def _shot(surf, scalars, clim, cmap, title, stamp, path, edges=False, color=None, bar_title=None):
    import pyvista as pv
    pl = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    pl.set_background("white")
    if scalars:
        pl.add_mesh(surf, scalars=scalars, cmap=cmap, clim=list(clim), above_color="magenta", below_color="#00004d",
                    scalar_bar_args=dict(title=bar_title, color="black", n_labels=6, fmt="%.1f", vertical=True, height=0.6, position_y=0.2, position_x=0.9))
    else:
        pl.add_mesh(surf, color=color, show_edges=True, edge_color="#555555", line_width=0.4)
    pl.add_text(title, font_size=11, color="black", position="upper_left")
    if stamp:
        pl.add_text(stamp, font_size=12, color="#b00020", position="lower_left")
    pl.view_isometric()
    pl.screenshot(str(path))
    pl.close()


def render_set(piece, grid, stats, stamp, faces, case, out):
    """The 4 PNGs of a piece into `out`."""
    out.mkdir(parents=True, exist_ok=True)
    surf = grid.extract_surface()
    if "vm_MPa" in grid.cell_data and "vm_MPa" not in grid.point_data:      # local FEM: element values -> smooth nodal values for the picture
        surf = grid.cell_data_to_point_data().extract_surface()
    _shot(surf, "vm_MPa", CLIM_VM, "turbo", f"{piece}: von Mises, máx {stats['sigma_max_MPa']:.1f} MPa (p99.5 {stats['sigma_p995_MPa']:.1f}); escala fija 0-50 MPa, magenta = pasa de 50",
          stamp, out / "vonmises.png", bar_title="von Mises (MPa)")
    _shot(surf, "u_mm", CLIM_U, "viridis", f"{piece}: desplazamiento máx {stats['u_max_mm']:.2f} mm; escala fija 0-6 mm, magenta = pasa de 6",
          stamp, out / "desplazamiento.png", bar_title="desplazamiento (mm)")
    _shot(surf, None, None, None, f"{piece}: malla ({stats['celdas']} tetraedros de segundo orden)", stamp, out / "malla.png", color="#dfe3e8")
    SR.render_bc(faces, case, out / "condiciones.png", piece)
    return {k: f"resultados/{piece}/{k}.png" for k in ("vonmises", "desplazamiento", "malla", "condiciones")}


# ------------------------------------------------------------------------------------------------ driver
def run_piece(piece, size, api, state, no_api=False):
    key, case = case_key(piece, state)
    S = state.get(key, {})
    jf = SR.OUT / f"{piece}.json"
    js = json.loads(jf.read_text(encoding="utf-8")) if jf.exists() else {}
    grp = SR.PIECES[piece]["grupo"]
    local = solve_local(piece, size)
    faces, case_o = local["faces"], local["case"]
    ss, why = None, ""
    if not S.get("run_id"):
        why = "sin corrida en SimScale"
    elif not js.get("resultado") or js.get("run_id") != S["run_id"]:
        why = "la corrida existe pero SimScale no devolvió el resultado (403 export-source-locked)"
    elif no_api or api is None:
        why = "no se pudo verificar la geometría contra SimScale"
    else:
        named = SR.OUT / "_named" / f"{piece}.step"
        sh, fcs, info, c2 = SR.prepare(piece)
        SR.name_step(sh, fcs, named)
        ok, g_old, g_now = geometry_is_current(api, piece, grp, S["gid"], named, SR.PIECES[piece]["step"])
        if not ok:
            why = f"SimScale corrió otra geometría ({g_old}); la actual es {g_now}"
        else:
            v = vtu_for(piece, S["run_id"])
            r = read_simscale(v, js["resultado"]) if v else None
            if r is None:
                why = "no está el VTK de esa corrida en disco"
            else:
                ss = r
    pid = PID[grp]
    link_sim = f"https://www.simscale.com/workbench/?pid={pid}&mi=spec:{S['sim_id']}%2Cservice:SIMULATION%2Cstrategy:1" if S.get("sim_id") else f"https://www.simscale.com/workbench/?pid={pid}"
    st_loc = local["stats"]
    if ss:
        grid, st = ss
        fuente, stamp = "SimScale", None
        link = js.get("enlace_resultado") or link_sim
    else:
        grid, st = local["grid"], st_loc
        fuente = "FEM local"
        stamp = STAMP_403 if "403" in why else STAMP_NEW
        link = link_sim
    imgs = render_set(piece, grid, st, stamp, faces, case_o, DOCS_RES / piece)
    sm, p995 = st["sigma_max_MPa"], st["sigma_p995_MPa"]
    ent = dict(pieza=piece, caso=case["name"], titulo=case["titulo"], grupo=grp, fuente=fuente, motivo_fuente=("" if ss else why),
               sigma_max=round(sm, 2), sigma_p995=round(p995, 2), fs=round(SR.SIGMA_ALLOW / sm, 3), fs_p995=round(SR.SIGMA_ALLOW / p995, 2),
               fs_capas=round(SY_CAPAS / p995, 2), fs_plano=round(SY_PLANO / p995, 2), umax_mm=round(st["u_max_mm"], 3),
               sigma_local=round(st_loc["sigma_max_MPa"], 2), sigma_local_p995=round(st_loc["sigma_p995_MPa"], 2), umax_local_mm=round(st_loc["u_max_mm"], 3),
               sigma_simscale=(round(ss[1]["sigma_max_MPa"], 2) if ss else None), sigma_simscale_p995=(round(ss[1]["sigma_p995_MPa"], 2) if ss else None),
               umax_simscale_mm=(round(ss[1]["u_max_mm"], 3) if ss else None),
               cumple=bool(SR.SIGMA_ALLOW / p995 >= 1 and SY_CAPAS / p995 >= 1), cumple_pico=bool(SR.SIGMA_ALLOW / sm >= 1),
               link=link, link_proyecto=f"https://www.simscale.com/workbench/?pid={pid}", link_simulacion=link_sim,
               malla=dict(celdas=st["celdas"], nodos=st["nodos"]), imagenes=imgs, notas=case["notes"])
    print(f"{piece:28s} {fuente:9s} smax {sm:7.1f} p995 {p995:6.1f} FS {ent['fs']:.2f} capas {ent['fs_capas']:.2f} u {st['u_max_mm']:.2f} mm | local {st_loc['sigma_max_MPa']:.1f}/{st_loc['sigma_p995_MPa']:.1f}"
          f" | {st_loc['celdas']} cells {st_loc['segundos']} s | {why}", flush=True)
    return ent


def update(names, size, no_api):
    """Images + resultados.json entries for `names` (other entries of the file are kept)."""
    state = load_state()
    api = None
    if not no_api:
        try:
            api = SR.client()
        except SystemExit as e:
            print("no API:", e)
    DOCS_RES.mkdir(parents=True, exist_ok=True)
    jf = DOCS_RES / "resultados.json"
    allr = json.loads(jf.read_text(encoding="utf-8")) if jf.exists() else {}
    rc = 0
    for k in names:
        try:
            allr[k] = run_piece(k, size, api, state, no_api)
        except Exception as e:       # noqa: BLE001
            rc = 1
            print(f"FAILED {k}: {type(e).__name__}: {SR.api_err(e) if hasattr(e, 'status') else e}")
    jf.write_text(json.dumps(allr, indent=1, ensure_ascii=False), encoding="utf-8")
    (DOCS_RES / "meta.json").write_text(json.dumps(dict(
        generado=time.strftime("%Y-%m-%d %H:%M"), escala_vonmises_MPa=list(CLIM_VM), escala_desplazamiento_mm=list(CLIM_U),
        convenciones="fs = 50/sigma_max; fs_capas = 22/sigma_p995 (entre capas); fs_plano = 45/sigma_p995; cumple = fs_p995>=1 y fs_capas>=1",
        material=dict(E_MPa=SR.E_PA / 1e6, nu=SR.NU, rho=SR.RHO, sigma_adm_MPa=SR.SIGMA_ALLOW)), indent=1, ensure_ascii=False), encoding="utf-8")
    print("written", jf)
    return rc


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pieza", action="append", default=[])
    ap.add_argument("--malla", type=float, default=3.0)
    ap.add_argument("--sin-api", action="store_true")
    a = ap.parse_args()
    return update(a.pieza or list(SR.ORDEN), a.malla, a.sin_api)


if __name__ == "__main__":
    sys.exit(main())
