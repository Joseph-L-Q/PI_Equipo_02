"""Local FEM of the simple version (free tools): Gmsh mesh + CalculiX, for the rail half with its hook and the capsule
foot, with the load cases of simple.py §5 (150 N of handling on a capsule). PETG of params.py (estimated, isotropic:
the layers are not modelled, so the FS is given against the in-layer and the between-layer strength).

    python fem.py            (from cad_final/; or: python build.py --fem)
Cases:
  riel_agua    M3s, the C seat of the hook fixed (in the water the node hangs on the ring), 150 N down at the front of
               the capsule, carried by a rigid body to the 2 M4 holes of the saddle.
  riel_izado   M3s, the face of the flange on the box pad fixed (lifting by the handle), the same load.
  pie          M5s, the 2 M4 holes of the saddle fixed, 150 N down at the front of the capsule carried by a rigid body
               to the 4 M3 holes of the lid.
The maximum stress is taken as the 99.5th percentile of the von Mises stress at the integration points (the fixed
faces and the rigid bodies give local peaks that are a modelling artefact); the absolute maximum is also given.
Outputs: salida/simple/fem/ (fem.json, one PNG per case; .inp/.dat/.frd ignored by git). CCX_EXE overrides the solver.
No result here says anything about watertightness.
"""
import json
import math
import os
import subprocess
import time
from pathlib import Path

import numpy as np

import params as P
import simple as SM

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "simple" / "fem"
STEP = HERE.parent / "salida" / "simple" / "step"
CCX = Path(os.environ.get("CCX_EXE", Path.home() / "Downloads" / "calculix_2.22" / "calculix_2.22_4win" / "ccx_static.exe"))
GMSH_TO_CCX_TET10 = [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]


def geometry():
    """Positions of the load and support features from simple.py (same as the CAD)."""
    import capsula as CP
    import layout
    lay = layout.build(P.SIMPLE_ESP32_BASE, floors=P.SIMPLE_FLOORS)
    cp = {"M4": CP.capsule_body(), "M6": CP.bezel(), "M7": CP.window_disc(), "lid": CP.lid_plate()}
    ax, az, foot = SM.capsule_pose(lay, cp)
    xf = CP.cap_dims()[6]
    front = (ax + SM.cap_pt(xf, 0)[0], 0.0, az + SM.cap_pt(xf, 0)[1])
    lid_pts = [(ax + SM.cap_pt(CP.cap_dims()[4] + P.CAP_LID_T / 2, z)[0], y, az + SM.cap_pt(CP.cap_dims()[4] + P.CAP_LID_T / 2, z)[1])
               for y, z in CP.cap_screw_pts()]
    return dict(x_flange=SM.x_flange(lay), bx=foot["bx"], bz=foot["bz"], ring=(SM.R_RING, SM.Z_RAIL - P.HOOK_DROP),
                front=front, lid_pts=lid_pts)


def mesh(step, size):
    """Second-order tetra mesh of a STEP: (nodes {tag: xyz}, tets [10 tags], surface tag -> node tags, gmsh surfaces bbox)."""
    import gmsh
    gmsh.initialize()
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
    et, en = gmsh.model.mesh.getElementsByType(11)
    tets = en.astype(int).reshape(-1, 10)
    surf = {}
    for dim, tag in gmsh.model.getEntities(2):
        nt, _, _ = gmsh.model.mesh.getNodes(dim, tag, includeBoundary=True)
        surf[tag] = (set(nt.astype(int)), gmsh.model.getBoundingBox(dim, tag))
    gmsh.finalize()
    return nodes, tets, surf


def pick(surf, test):
    out = set()
    for tag, (nt, bb) in surf.items():
        if test(bb):
            out |= nt
    return out


def near(bb, x=None, z=None, tol=3.0):
    xc, zc = (bb[0] + bb[3]) / 2, (bb[2] + bb[5]) / 2
    return (x is None or abs(xc - x) < tol) and (z is None or abs(zc - z) < tol)


def write_inp(path, nodes, tets, fixed, rigid, ref_xyz, load):
    n_ref = max(nodes) + 1
    n_rot = n_ref + 1
    L = ["*HEADING", "LanternGuard fem.py", "*NODE"]
    L += [f"{k},{v[0]:.6f},{v[1]:.6f},{v[2]:.6f}" for k, v in nodes.items()]
    L += [f"{n_ref},{ref_xyz[0]:.6f},{ref_xyz[1]:.6f},{ref_xyz[2]:.6f}", f"{n_rot},{ref_xyz[0]:.6f},{ref_xyz[1]:.6f},{ref_xyz[2]:.6f}"]
    L += ["*ELEMENT,TYPE=C3D10,ELSET=EALL"]
    L += [f"{i + 1}," + ",".join(str(t[j]) for j in GMSH_TO_CCX_TET10) for i, t in enumerate(tets)]

    def nset(name, ids):
        ids = sorted(ids)
        L.append(f"*NSET,NSET={name}")
        L.extend(",".join(str(n) for n in ids[i:i + 12]) for i in range(0, len(ids), 12))
    nset("FIX", fixed)
    nset("RIG", rigid - fixed)
    nset("NALL", nodes.keys())
    L += ["*MATERIAL,NAME=PETG", "*ELASTIC", f"{P.PETG_E},{P.PETG_NU}", "*SOLID SECTION,ELSET=EALL,MATERIAL=PETG",
          f"*RIGID BODY,NSET=RIG,REF NODE={n_ref},ROT NODE={n_rot}",
          "*STEP", "*STATIC", "*BOUNDARY", "FIX,1,3,0.0", "*CLOAD"]
    L += [f"{n_ref},{i + 1},{f:.6f}" for i, f in enumerate(load) if f]
    L += ["*NODE PRINT,NSET=NALL", "U", "*EL PRINT,ELSET=EALL", "S", "*NODE FILE", "U", "*EL FILE", "S", "*END STEP"]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def read_dat(path):
    """(|U| per node, von Mises per element max over its integration points) from the .dat of CalculiX."""
    U, S = {}, {}
    mode = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("displacements"):
            mode = "u"
            continue
        if s.startswith("stresses"):
            mode = "s"
            continue
        parts = s.split()
        if not parts or not parts[0].lstrip("-").isdigit():
            continue
        try:
            vals = [float(v) for v in parts]
        except ValueError:
            continue
        if mode == "u" and len(vals) == 4:
            U[int(vals[0])] = math.sqrt(vals[1] ** 2 + vals[2] ** 2 + vals[3] ** 2)
        elif mode == "s" and len(vals) == 8:
            sx, sy, sz, txy, txz, tyz = vals[2:]
            vm = math.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (txy ** 2 + txz ** 2 + tyz ** 2))
            e = int(vals[0])
            S[e] = max(S.get(e, 0.0), vm)
    return U, S


def png(path, nodes, tets, S, title):
    import pyvista as pv
    ids = {k: i for i, k in enumerate(nodes)}
    pts = np.array(list(nodes.values()))
    cells = np.hstack([[4, ids[t[0]], ids[t[1]], ids[t[2]], ids[t[3]]] for t in tets])
    grid = pv.UnstructuredGrid(cells, np.full(len(tets), 10, np.uint8), pts)
    grid.cell_data["von Mises MPa"] = np.array([S.get(i + 1, 0.0) for i in range(len(tets))])
    pl = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    pl.set_background("white")
    clim = [0, float(np.percentile(grid.cell_data["von Mises MPa"], 99.5))]
    pl.add_mesh(grid, scalars="von Mises MPa", cmap="turbo", clim=clim, show_edges=False)
    pl.add_text(title, font_size=12, color="black")
    pl.view_isometric()
    pl.screenshot(str(path))
    pl.close()


def run_case(name, step, g, size, fixed_test, rigid_test):
    t0 = time.time()
    nodes, tets, surf = mesh(step, size)
    fixed = pick(surf, fixed_test)
    rigid = pick(surf, rigid_test)
    if not fixed or not rigid:
        return dict(error=f"no encontre las caras (fijas {len(fixed)}, carga {len(rigid)})")
    inp = OUT / f"{name}.inp"
    write_inp(inp, nodes, tets, fixed, rigid, g["front"], (0.0, 0.0, -P.HANDLING_LOAD_N))
    r = subprocess.run([str(CCX), "-i", name], cwd=OUT, capture_output=True, text=True, timeout=3600)
    dat = OUT / f"{name}.dat"
    if r.returncode != 0 or not dat.exists():
        return dict(error=f"ccx rc={r.returncode}: {(r.stdout + r.stderr)[-300:]}")
    U, S = read_dat(dat)
    vm = np.array(list(S.values()))
    s995 = float(np.percentile(vm, 99.5))
    png(OUT / f"{name}.png", nodes, tets, S, f"{name}: von Mises (escala hasta el percentil 99.5 = {s995:.1f} MPa)")
    return dict(nodos=len(nodes), elementos=len(tets), umax=max(U.values()), smax=s995, smax_abs=float(vm.max()),
                fs=P.PETG_YIELD / s995, fs_capas=P.PETG_YIELD_Z / s995, segundos=time.time() - t0)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not CCX.exists():
        raise SystemExit(f"no encuentro CalculiX en {CCX} (CCX_EXE)")
    g = geometry()
    size = P.FEM_MESH
    rx, rz = g["ring"]
    ri = P.RING_SECTION / 2 + P.SIMPLE_HOOK_C[0]
    seat = lambda bb: near(bb, x=rx, z=rz, tol=ri + 1.0) and (bb[5] - bb[2]) <= 2 * ri + 1.0 and (bb[3] - bb[0]) <= 2 * ri + 1.0  # noqa: E731
    flange = lambda bb: abs(bb[0] - g["x_flange"]) < 0.05 and abs(bb[3] - g["x_flange"]) < 0.05  # noqa: E731
    saddle = lambda bb: any(near(bb, x=x, z=g["bz"], tol=P.M4_CLEAR) for x in g["bx"]) and (bb[3] - bb[0]) <= P.M4_CLEAR + 0.5  # noqa: E731

    def lid_holes(bb):
        c = ((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2, (bb[2] + bb[5]) / 2)
        return any(math.dist(c, p) < P.CAP_LID_T for p in g["lid_pts"]) and max(bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]) <= 8.0
    cases = {"riel_agua": (STEP / "M3s_riel_gancho.step", seat, saddle),
             "riel_izado": (STEP / "M3s_riel_gancho.step", flange, saddle),
             "pie": (STEP / "M5s_capsula_tapa_pie.step", saddle, lid_holes)}
    res = {}
    for name, (step, fx, rg) in cases.items():
        res[name] = run_case(name, step, g, size, fx, rg)
        print(name, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in res[name].items()}, flush=True)
    data = dict(material=dict(E=P.PETG_E, nu=P.PETG_NU, sy=P.PETG_YIELD, sy_capas=P.PETG_YIELD_Z), malla_mm=size,
                carga_N=P.HANDLING_LOAD_N, solver=str(CCX.name), casos={k: v for k, v in res.items() if "error" not in v},
                errores={k: v["error"] for k, v in res.items() if "error" in v})
    (OUT / "fem.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    simscale_md(g, data)
    return 1 if data["errores"] else 0


def simscale_md(g, data):
    """salida/simscale/: the STEP of the two simple pieces and SIMSCALE.md with the manual steps of the same cases."""
    import shutil
    sim = HERE.parent / "salida" / "simscale"
    sim.mkdir(parents=True, exist_ok=True)
    shutil.copy2(STEP / "M3s_riel_gancho.step", sim / "simple_M3s_riel_gancho.step")
    shutil.copy2(STEP / "M5s_capsula_tapa_pie.step", sim / "simple_M5s_capsula_tapa_pie.step")
    fx, fy, fz = g["front"]
    rx, rz = g["ring"]
    c = data["casos"]

    def row(k):
        v = c.get(k)
        return (f"{v['umax']:.2f} mm, {v['smax']:.1f} MPa (p99.5), FS {v['fs']:.1f} / {v['fs_capas']:.1f}" if v else "sin resultado")
    L = ["# SimScale, version simple (pasos manuales; el plan gratuito no tiene API)", "",
         "Generado por `cad_final/fem.py`. Mismos casos que el FEM local (Gmsh + CalculiX, `salida/simple/fem/fem.json`), "
         "para comparar. Unidades mm, N, MPa. No se afirma estanqueidad por simulacion.", "",
         "| Archivo | Pieza |", "|---|---|",
         "| `simple_M3s_riel_gancho.step` | Mitad del riel con el gancho en C (la otra mitad es la misma, girada) |",
         "| `simple_M5s_capsula_tapa_pie.step` | Tapa de la capsula con el pie en silla |", "",
         "## Pasos comunes", "",
         "1. SimScale → New Project → Import CAD → elegir el STEP, unidad **mm**.",
         "2. Create Simulation → **Static**. Analysis type lineal, pequenos desplazamientos.",
         f"3. Materials → New → nombre PETG, Linear elastic isotropic: E = {P.PETG_E:g} MPa, ν = {P.PETG_NU:g}, "
         f"densidad {P.PETG_DENSITY * 1000:g} kg/m³ (todo estimado, `params.py`). Asignar a todo el volumen.",
         f"4. Mesh → Standard, **second order**, tamano maximo {P.FEM_MESH:g} mm (o fineness 7).",
         "5. Result control → von Mises y desplazamiento total.", "",
         "## Casos", "",
         f"Carga en los tres: **Remote force** de {P.HANDLING_LOAD_N:g} N en −Z aplicada en el punto (x, y, z) = "
         f"({fx:.1f}, {fy:.1f}, {fz:.1f}) mm (frente de la capsula), comportamiento **deformable**, sobre las caras indicadas.", "",
         "| Caso | STEP | Fijo (Fixed support) | Caras de la remote force | FEM local |", "|---|---|---|---|---|",
         f"| riel_agua | M3s | Cara interior de la C del gancho (cilindro de radio {P.RING_SECTION / 2 + P.SIMPLE_HOOK_C[0]:g} centrado en x = {rx:.1f}, z = {rz:.1f}) | "
         f"Los 2 agujeros M4 de la silla (cilindros a x = {g['bx'][0]:.1f} y {g['bx'][1]:.1f}, z = {g['bz']:.1f}) | {row('riel_agua')} |",
         f"| riel_izado | M3s | Cara plana de la brida contra el cojin de la caja (x = {g['x_flange']:.1f}) | Los 2 agujeros M4 de la silla | {row('riel_izado')} |",
         f"| pie | M5s | Los 2 agujeros M4 de la silla | Los 4 agujeros M3 de la tapa | {row('pie')} |", "",
         f"FS = {P.PETG_YIELD:g} MPa (a lo largo de las capas) / σ y {P.PETG_YIELD_Z:g} MPa (entre capas) / σ, con σ el percentil "
         "99.5 de von Mises: los picos en las caras fijas y en los agujeros de la remote force son efecto del modelo. Si "
         "SimScale da valores mas de 20 % distintos, revisar que la remote force sea deformable y las caras sean las mismas."]
    (sim / "SIMSCALE.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
