"""SimScale by API: linear static FEM of the LanternGuard pieces (free community plan).

    python simscale_run.py --pieza B3_caja            one piece
    python simscale_run.py --grupo B                  all pieces of a group (A = submerged node, B = buoy)
    python simscale_run.py --todo                     everything
    python simscale_run.py --resultados               images + docs/resultados/resultados.json, no SimScale run (see resultados_bloque3.py)
    python simscale_run.py --informe                  docs/REPORTE_SIMSCALE_LanternGuard.md/.pdf from docs/resultados/resultados.json
    python simscale_run.py --listar B3_caja           print the face inventory and the picked faces, do not touch the API
    python simscale_run.py --pieza B3_caja --solo-preparar   name faces + check picks + capture BCs, no API call at all
    options: --fineness 5 (SimScale automatic mesh, 1 coarse .. 10 fine), --rehacer (ignore the saved ids and re-create)

Run from cad_final/. The key is SIMSCALE_API_KEY in cad_final/.env (never printed, never written anywhere else).

How it works, per piece:
 1. The STEP is read with cadquery and every face is NAMED "LGF####" (its index in the cadquery face list) by writing a
    new STEP through XCAF (OCP). SimScale keeps that name as the face attribute SDL/TYSA_UNAME, so the geometry
    mapping API gives the SimScale entity id (B1_TE..) of every face I pick by position/normal. The pick is verified
    (count and area of the faces of each support and load) and saved in salida/simscale/<piece>.json.
 2. Project (A "LanternGuard nodo sumergido" / B "LanternGuard boya", re-used by name), geometry import, mesh
    (Simmetrix automatic, second order), linear static analysis, run, wait, download, captures.
 3. The results (von Mises max, displacement max) are read from the downloaded solution fields with PyVista.

Material PETG of the task: E 2.1 GPa, nu 0.38, rho 1270 kg/m3, allowable 50 MPa (FS = 50 / sigma_max). Units: STEP in mm,
SimScale in SI. Flotation and stability are analytical (docs/BOYA.md), not FEM.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time
import zipfile
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")      # params.py reads it at import (fem.geometry() needs it)

import numpy as np                                      # noqa: E402
import requests                                         # noqa: E402

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
OUT = MOD / "salida" / "simscale"
STEP_A = MOD / "salida" / "prototipos" / "P2_robusto" / "step"
STEP_B = MOD / "salida" / "boya_pet" / "step"
FEM_JSON = MOD / "salida" / "prototipos" / "P2_robusto" / "fem" / "fem.json"

E_PA, NU, RHO, SIGMA_ALLOW = 2.1e9, 0.38, 1270.0, 50.0     # PETG of the task
G = 9.81
RHO_SEA, V_CURRENT = 1025.0, 1.5
Q_DYN = 0.5 * RHO_SEA * V_CURRENT ** 2                     # 1153 Pa
HANDLING_N = 150.0
WAVE_N = 200.0
PROJECTS = {"A": "LanternGuard nodo sumergido", "B": "LanternGuard boya"}


# ------------------------------------------------------------------------------------------------ faces
def face_info(f):
    bb = f.BoundingBox()
    c = f.Center()
    d = dict(bb=(bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax), c=(c.x, c.y, c.z), area=f.Area(), type=f.geomType(), n=None)
    if d["type"] == "PLANE":
        n = f.normalAt()
        d["n"] = (n.x, n.y, n.z)
    return d


def load_faces(step):
    import cadquery as cq
    sh = cq.importers.importStep(str(step)).val()
    return sh, sh.Faces()


def imprint(sh, circles):
    """Split the planar faces under each circle (x, y, z, r; normal +Z) so a support can be picked as its own face (OCC splitter)."""
    import cadquery as cq
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Splitter
    from OCP.TopTools import TopTools_ListOfShape
    args, tools = TopTools_ListOfShape(), TopTools_ListOfShape()
    args.Append(sh.wrapped)
    for x, y, z, r in circles:
        tools.Append(cq.Face.makeFromWires(cq.Wire.makeCircle(r, cq.Vector(x, y, z), cq.Vector(0, 0, 1))).wrapped)
    sp = BRepAlgoAPI_Splitter()
    sp.SetArguments(args)
    sp.SetTools(tools)
    sp.Build()
    out = cq.Shape.cast(sp.Shape())
    if out.ShapeType() != "Solid" or not out.isValid() or abs(out.Volume() - sh.Volume()) > 1e-3 * sh.Volume():
        raise RuntimeError("imprint broke the solid")
    return out


def holes_xy(info, d, zlo, zhi, tol=0.25):
    """Centres (x, y) of the vertical cylindrical holes of diameter d whose bbox lies between zlo and zhi."""
    return [((f["bb"][0] + f["bb"][3]) / 2, (f["bb"][1] + f["bb"][4]) / 2) for f in info
            if f["type"] == "CYLINDER" and abs((f["bb"][3] - f["bb"][0]) - d) < tol and abs((f["bb"][4] - f["bb"][1]) - d) < tol
            and f["bb"][2] >= zlo - 0.05 and f["bb"][5] <= zhi + 0.05]


def prep_b3(info):
    import params as P
    zmin = min(f["bb"][2] for f in info)
    return [(x, y, zmin, 5.0) for x, y in holes_xy(info, P.M3_CLEAR, zmin, zmin + P.PET_EAR[2])]       # footprint of the D10 pillars


def prep_b2(info):
    import params as P
    zmin = min(f["bb"][2] for f in info)
    return [(x, y, zmin, 5.0) for x, y in holes_xy(info, P.M3_CLEAR, zmin, zmin + P.PET_COVER_T)]       # footprint of the D10 hull bosses


def name_step(sh, faces, out):
    """Write `out` = the same solid with face i named LGF{i:04d} (survives the SimScale import as SDL/TYSA_UNAME)."""
    from OCP.Interface import Interface_Static
    from OCP.STEPCAFControl import STEPCAFControl_Writer
    from OCP.STEPControl import STEPControl_AsIs
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.TDataStd import TDataStd_Name
    from OCP.TDocStd import TDocStd_Document
    from OCP.XCAFApp import XCAFApp_Application
    from OCP.XCAFDoc import XCAFDoc_DocumentTool
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF"))
    app.NewDocument(TCollection_ExtendedString("MDTV-XCAF"), doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    lab = st.AddShape(sh.wrapped)
    for i, f in enumerate(faces):
        sl = st.AddSubShape(lab, f.wrapped)
        if sl.IsNull():
            raise RuntimeError(f"face {i} could not be named")
        TDataStd_Name.Set_s(sl, TCollection_ExtendedString(f"LGF{i:04d}"))
    w = STEPCAFControl_Writer()
    Interface_Static.SetIVal_s("write.stepcaf.subshapes.name", 1)
    w.SetNameMode(True)
    w.Transfer(doc, STEPControl_AsIs)
    out.parent.mkdir(parents=True, exist_ok=True)
    w.Write(str(out))


def pick(info, test):
    return [i for i, f in enumerate(info) if test(f)]


def planar(f, nz=None, ny=None, nx=None, tol=1e-3):
    n = f["n"]
    if n is None:
        return False
    return all(v is None or abs(n[k] - v) < tol for k, v in enumerate((nx, ny, nz)))


def near_xy(f, x, y, tol):
    return math.hypot((f["bb"][0] + f["bb"][3]) / 2 - x, (f["bb"][1] + f["bb"][4]) / 2 - y) < tol


def total_area(info, idx):
    return sum(info[i]["area"] for i in idx)


# ------------------------------------------------------------------------------------------------ cases
# A case = dict(name, fixed=[(label, idx)], loads=[dict(kind, label, idx, force_N, point_mm, mass...)], gravity, notes)
def _fx(info, test, label):
    idx = pick(info, test)
    return (label, idx)


def case_b3(info, step):
    """B3_caja, the dry electronics box: bolted by its 4 ears (M3) to the pillars of the deck."""
    zmin = min(f["bb"][2] for f in info)
    zmax = max(f["bb"][5] for f in info)
    ears = pick(info, lambda f: planar(f, nz=-1) and abs(f["bb"][2] - zmin) < 0.05 and f["area"] < 200)   # imprinted D10 pillar footprints
    floor = pick(info, lambda f: planar(f, nz=1) and abs(f["bb"][2] - (zmin + 2.4)) < 0.05 and f["area"] > 3000)
    rim = pick(info, lambda f: planar(f, nz=1) and abs(f["bb"][5] - zmax) < 0.05)
    side = sorted(pick(info, lambda f: planar(f, ny=1) and f["area"] > 800), key=lambda i: -info[i]["bb"][4])[:1]
    import params as P
    bm = P.BUOY_MASS
    elec_g = P.BUOY_CELLS * bm["celda_18650"] + bm["portabaterias"] + bm["pcb_heltec"] + bm["waveshare"] + bm["rtc"] + bm["cables_fusible"] \
        + bm["prensaestopas"] * 1.5 + bm["tornilleria"]
    lid_g = 57.2     # B4 lid printed mass (docs/BOYA.md), it rests on the flange rim
    return dict(name="caja_peso_y_ola",
                titulo="Caja seca: peso de la electronica y de la tapa + golpe de ola de 200 N de costado",
                fixed=[("4 orejas: huella de los pilares D10 bajo la oreja (atornilladas)", ears)],
                loads=[dict(kind="force", label="peso de la electronica sobre el piso", idx=floor, force_N=(0, 0, -elec_g * 1e-3 * G)),
                       dict(kind="force", label="peso de la tapa B4 sobre el borde", idx=rim, force_N=(0, 0, -lid_g * 1e-3 * G)),
                       dict(kind="force", label="golpe de ola 200 N contra la pared +Y", idx=side, force_N=(0, WAVE_N, 0))],
                gravity=True,
                notes=[f"Electronica {elec_g:.0f} g (parametros del modelo, sin panel ni antena) y tapa {lid_g} g, 1 g de gravedad.",
                       "La ola de 200 N se aplica entera contra una pared larga: caso exagerado (la caja va bajo el panel)."])


def case_b2(info, step, variant="vertical"):
    """B2 deck half: bolted to the hull bosses (M3 clearance holes in the bars), loaded by the box pillars and panel columns."""
    import params as P
    zmin = min(f["bb"][2] for f in info)
    bm = P.BUOY_MASS
    # pillars, panel columns and the mast: small planar +Z faces, told apart by their diameter
    bar_top = zmin + P.PET_COVER_T
    dia = lambda f: f["bb"][3] - f["bb"][0]          # noqa: E731
    top_of = lambda D, z: pick(info, lambda f: planar(f, nz=1) and abs(dia(f) - D) < 0.3 and abs(f["bb"][5] - z) < 0.5)   # noqa: E731
    pil_tops = top_of(P.PET_PILLAR[0], bar_top + P.PET_PILLAR[1])
    col_tops = pick(info, lambda f: planar(f, nz=1) and abs(dia(f) - P.PET_COLUMN_D) < 0.3 and f["bb"][5] > bar_top + 30)
    mast = pick(info, lambda f: planar(f, nz=1) and abs(dia(f) - P.PET_MAST[0]) < 0.3 and f["bb"][5] > bar_top + 100)
    # supports: imprinted D10 footprints of the hull bosses under the M3 holes of the bars
    holes = pick(info, lambda f: planar(f, nz=-1) and abs(f["bb"][2] - zmin) < 0.05 and f["area"] < 200)
    box_total = 171.0 + 57.2 + P.BUOY_CELLS * bm["celda_18650"] + bm["portabaterias"] + bm["pcb_heltec"] + bm["waveshare"] + bm["rtc"] \
        + bm["cables_fusible"] + bm["prensaestopas"] * 1.5 + bm["tornilleria"]     # B3 + B4 + contents (g)
    f_pil = box_total * 1e-3 * G / 4.0
    f_col = bm["panel"] * 1e-3 * G / 4.0
    loads = []
    if pil_tops:
        loads.append(dict(kind="force", label="peso de la caja (1/4 por pilar)", idx=pil_tops, force_N=(0, 0, -f_pil * len(pil_tops))))
    lateral = variant == "lateral"
    if col_tops:
        loads.append(dict(kind="force", label="peso del panel" + (" + golpe de ola 200 N (en +Y) sobre las columnas" if lateral else " (1/4 por columna)"), idx=col_tops,
                          force_N=(0, WAVE_N if lateral else 0, -f_col * len(col_tops))))
    if mast:
        loads.append(dict(kind="force", label="antena", idx=mast, force_N=(0, 0, -bm["antena"] * 1e-3 * G)))
    if not lateral:
        bars = pick(info, lambda f: planar(f, nz=1) and abs(f["bb"][5] - bar_top) < 0.05 and f["area"] > 300)
        loads.append(dict(kind="force", label="golpe de ola vertical de 200 N sobre las barras", idx=bars, force_N=(0, 0, -WAVE_N)))
    notes = [f"Caja completa {box_total:.0f} g repartida en 4 pilares (cada mitad carga 2); panel {bm['panel']} g en 4 columnas (cada mitad carga 2)."]
    if lateral:
        notes.append("Variante lateral: la ola de 200 N golpea el panel (hace de vela) y baja por sus columnas; cada media cubierta recibe los 200 N enteros "
                     "en sus 2 columnas (exagerado: en la boya completa se reparten entre las dos mitades).")
    else:
        notes.append("Golpe de ola vertical: 200 N hacia abajo sobre la cara de arriba de las barras de esa mitad (cada mitad recibe los 200 N enteros: "
                     "exagerado, en la boya completa se reparten).")
    return dict(name="cubierta_ola_lateral" if lateral else "cubierta_ola_vertical",
                titulo="Media cubierta: peso de la caja y del panel + golpe de ola de 200 N " + ("lateral sobre el panel" if lateral else "vertical sobre las barras"),
                fixed=[("huella de los 4 bosses D10 del casco bajo los agujeros M3", holes)], loads=loads, gravity=True, notes=notes)


def front_force_geometry():
    """Positions from fem.geometry() (same as the local FEM) and the drag on the capsule."""
    import fem
    import capsula as CP
    g = fem.geometry()
    cd = CP.cap_dims()
    return g, cd


def case_a(piece, info, step):
    """Group A: same supports and loads as cad_final/fem.py (+ the current as a drag force on the capsule front)."""
    import fem
    import params as P
    import simple as SM
    g, cd = front_force_geometry()
    rx, rz = g["ring"]
    ri = P.RING_SECTION / 2 + P.SIMPLE_HOOK_C[0]

    def seat(f):
        bb = f["bb"]
        c = ((bb[0] + bb[3]) / 2, (bb[2] + bb[5]) / 2)
        return abs(c[0] - rx) < ri + 1.0 and abs(c[1] - rz) < ri + 1.0 and (bb[5] - bb[2]) <= 2 * ri + 1.0 and (bb[3] - bb[0]) <= 2 * ri + 1.0

    def saddle(f):
        bb = f["bb"]
        if g["pts"]:
            c = ((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2)
            return (any(math.dist(c, p) < 1.0 for p in g["pts"]) and bb[3] - bb[0] <= P.M3_INSERT_HOLE + 0.5
                    and bb[4] - bb[1] <= P.M3_INSERT_HOLE + 0.5 and bb[5] - bb[2] > 0.5)
        c = ((bb[0] + bb[3]) / 2, (bb[2] + bb[5]) / 2)
        return any(abs(c[0] - x) < P.M4_CLEAR and abs(c[1] - g["bz"]) < P.M4_CLEAR for x in g["bx"]) and (bb[3] - bb[0]) <= P.M4_CLEAR + 0.5

    def lid_holes(f):
        bb = f["bb"]
        c = ((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2, (bb[2] + bb[5]) / 2)
        return any(math.dist(c, p) < P.CAP_LID_T for p in g["lid_pts"]) and max(bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]) <= 8.0

    front = g["front"]
    r_cap = cd[1] / 2 if len(cd) > 1 else 40.0
    a_front = math.pi * r_cap ** 2 * 1e-6          # m2
    drag = Q_DYN * a_front * 1.0                   # Cd = 1 (blunt), N
    drag_note = (f"Corriente de {V_CURRENT} m/s: presion dinamica 0.5*{RHO_SEA:g}*{V_CURRENT}^2 = {Q_DYN:.0f} Pa sobre el frente de la capsula "
                 f"(area {a_front * 1e4:.1f} cm2, Cd = 1) = {drag:.2f} N, en -X (la corriente empuja la capsula hacia atras), aplicada en el frente.")
    grav = (0, 0, -HANDLING_N)
    f_remote = (-drag, 0, -HANDLING_N)
    if piece == "M3s_riel_gancho":
        return dict(name="riel_agua", titulo="Riel con gancho colgado del anillo: capsula con 150 N hacia abajo + corriente de 1.5 m/s",
                    fixed=[("asiento de la C del gancho (colgado del anillo)", pick(info, seat))],
                    loads=[dict(kind="remote", label="150 N + arrastre en el frente de la capsula, por un cuerpo rigido a la silla", idx=pick(info, saddle),
                                force_N=f_remote, point_mm=front)], gravity=False, notes=[drag_note])
    if piece == "M5s_capsula_tapa_pie":
        return dict(name="pie", titulo="Tapa de capsula con pie: silla fija, 150 N + corriente en el frente de la capsula",
                    fixed=[("agujeros de la silla (insertos M3 de la tapa del pie)", pick(info, saddle))],
                    loads=[dict(kind="remote", label="150 N + arrastre en el frente, por un cuerpo rigido a los 4 M3 de la tapa", idx=pick(info, lid_holes),
                                force_N=f_remote, point_mm=front)], gravity=False, notes=[drag_note])
    if piece == "M1s_caja_cuerpo":
        # Lifting case (decision, not in fem.py): the node hangs from the 20 M3 inserts of the lid flange (the handle is on the lid) while the
        # rail half is bolted to the +X end pad (4 M4 inserts) and carries the capsule: 150 N + drag at the capsule front through a rigid body.
        lid = pick(info, lambda f: f["type"] == "CYLINDER" and (f["bb"][3] - f["bb"][0]) < 6.2 and abs((f["bb"][4] - f["bb"][1]) - (f["bb"][3] - f["bb"][0])) < 0.1
                   and f["bb"][5] > 76.5 and f["bb"][2] > 68.5)
        pad = pick(info, lambda f: f["type"] == "CYLINDER" and abs((f["bb"][3] - f["bb"][0]) - 8.5) < 0.2 and abs((f["bb"][4] - f["bb"][1]) - P.M4_INSERT_HOLE) < 0.2
                   and f["bb"][3] > g["x_flange"] - 0.1 and f["bb"][0] > 0)
        return dict(name="izado", titulo="Caja: colgada de los insertos M3 de la tapa, el riel con la capsula tira del cojin +X (150 N + corriente)",
                    fixed=[("agujeros M3 de la brida de la tapa (16)", lid)],
                    loads=[dict(kind="remote", label="150 N + arrastre en el frente de la capsula, por un cuerpo rigido a los 4 M4 del cojin +X", idx=pad,
                                force_N=f_remote, point_mm=front)], gravity=True, notes=[drag_note,
                    "Caso propio (el FEM local no tiene la caja): la caja cuelga de la tapa como al izar por el asa; los insertos M3 de la tapa se toman "
                    "como apoyos fijos y el riel con la capsula tira de los 4 M4 del cojin."])
    raise KeyError(piece)


PIECES = {
    "B3_caja": dict(grupo="B", step=STEP_B / "B3_caja.step", case=case_b3, prep=prep_b3),
    "B2_cubierta_lisa": dict(grupo="B", step=STEP_B / "B2_cubierta_lisa.step", case=case_b2, prep=prep_b2),
    "B2_cubierta_mastil": dict(grupo="B", step=STEP_B / "B2_cubierta_mastil.step", case=case_b2, prep=prep_b2),
    "B2_cubierta_lisa_lateral": dict(grupo="B", step=STEP_B / "B2_cubierta_lisa.step", case=lambda i, s: case_b2(i, s, "lateral"), prep=prep_b2),
    "B2_cubierta_mastil_lateral": dict(grupo="B", step=STEP_B / "B2_cubierta_mastil.step", case=lambda i, s: case_b2(i, s, "lateral"), prep=prep_b2),
    "M3s_riel_gancho": dict(grupo="A", step=STEP_A / "M3s_riel_gancho.step", case=lambda i, s: case_a("M3s_riel_gancho", i, s)),
    "M5s_capsula_tapa_pie": dict(grupo="A", step=STEP_A / "M5s_capsula_tapa_pie.step", case=lambda i, s: case_a("M5s_capsula_tapa_pie", i, s)),
    "M1s_caja_cuerpo": dict(grupo="A", step=STEP_A / "M1s_caja_cuerpo.step", case=lambda i, s: case_a("M1s_caja_cuerpo", i, s)),
}


def prepare(piece):
    """STEP -> (solid with the supports imprinted, faces, info, case). Face i of `faces` is the one named LGF{i:04d}."""
    p = PIECES[piece]
    sh, faces = load_faces(p["step"])
    info = [face_info(f) for f in faces]
    if p.get("prep"):
        circles = p["prep"](info)
        if circles:
            sh = imprint(sh, circles)
            faces = sh.Faces()
            info = [face_info(f) for f in faces]
    return sh, faces, info, p["case"](info, p["step"])


# ------------------------------------------------------------------------------------------------ SimScale
def client():
    from dotenv import dotenv_values
    import simscale_sdk as sim
    key = dotenv_values(HERE / ".env").get("SIMSCALE_API_KEY")
    if not key:
        raise SystemExit("SIMSCALE_API_KEY missing in cad_final/.env")
    cfg = sim.Configuration()
    cfg.api_key = {"X-API-KEY": key}
    return sim.ApiClient(cfg)


def api_err(e):
    """Only the status code and the reason, never headers."""
    st = getattr(e, "status", "?")
    body = " ".join((getattr(e, "body", "") or "").split())[:1500]
    return f"HTTP {st} {getattr(e, 'reason', '')} {body}"


def get_project(api, group):
    import simscale_sdk as sim
    name = PROJECTS[group]
    P = sim.ProjectsApi(api)
    page = 1
    while True:
        r = P.get_projects(limit=100, page=page)
        for p in r.embedded:
            if p.name == name:
                return p.project_id
        if len(r.embedded) < 100:
            break
        page += 1
    desc = {"A": "LanternGuard submerged node (PETG): rail, capsule foot and box, linear static FEM, loads of docs/REPORTE_SIMSCALE_LanternGuard.md",
            "B": "LanternGuard buoy (PETG bottles buoy): electronics box and deck, linear static FEM"}[group]
    return P.create_project(sim.Project(name=name, description=desc, measurement_system="SI")).project_id


def wait(fn, ok=("FINISHED",), bad=("FAILED", "CANCELED"), every=6, limit=3600, label=""):
    t0 = time.time()
    last = None
    while True:
        o = fn()
        s = str(o.status)
        if s != last:
            print(f"   {label}: {s}" + (f" {o.progress:.0%}" if getattr(o, 'progress', None) else ""), flush=True)
            last = s
        if s in ok:
            return o
        if s in bad:
            raise RuntimeError(f"{label} ended {s}")
        if time.time() - t0 > limit:
            raise TimeoutError(label)
        time.sleep(every)


def import_geometry(api, pid, piece, named_step, src_step):
    import simscale_sdk as sim
    digest = hashlib.sha1(src_step.read_bytes() + named_step.stat().st_size.to_bytes(8, "little")).hexdigest()[:8]
    gname = f"{piece}_{digest}"
    G_ = sim.GeometriesApi(api)
    for g in G_.get_geometries(pid, limit=100).embedded:
        if g.name == gname:
            return g.geometry_id, gname
    st = sim.StorageApi(api).create_storage()
    r = requests.put(st.url, data=named_step.read_bytes(), headers={"Content-Type": "application/octet-stream"}, timeout=300)
    print(f"   upload status {r.status_code}")
    r.raise_for_status()
    imp = sim.GeometryImportsApi(api).import_geometry(pid, sim.GeometryImportRequest(
        name=gname, location=sim.GeometryImportRequestLocation(storage_id=st.storage_id), format="STEP", input_unit="mm",
        options=sim.GeometryImportRequestOptions(facet_split=False, sewing=False, improve=False, optimize_for_lbm_solver=False)))
    done = wait(lambda: sim.GeometryImportsApi(api).get_geometry_import(pid, imp.geometry_import_id), label="geometry import", every=3)
    return done.geometry_id, gname


def mappings(api, pid, gid, cls):
    import simscale_sdk as sim
    out, page = [], 1
    while True:
        r = sim.GeometriesApi(api).get_geometry_mappings(pid, gid, _class=cls, limit=1000, page=page)
        out += r.embedded
        if len(r.embedded) < 1000:
            return out
        page += 1


def face_entities(api, pid, gid, n_faces):
    """{face index: [SimScale entity names]} from the LGF attribute; asserts every face is there exactly once."""
    res = {}
    for e in mappings(api, pid, gid, "face"):
        for o in e.originate_from:
            for a in o.attribute_list or []:
                if a.attribute == "SDL/TYSA_UNAME" and str(a.value).startswith("LGF"):
                    res.setdefault(int(a.value[3:]), []).append(e.name)
    missing = [i for i in range(n_faces) if i not in res]
    if missing:
        raise RuntimeError(f"{len(missing)} faces lost their name in the import (e.g. {missing[:5]}): the pick would not be reliable")
    return res


def comp(v):
    import simscale_sdk as sim
    k = lambda x: sim.ConstantFunction(type="CONSTANT", value=float(x))  # noqa: E731
    return sim.ComponentVectorFunction(type="COMPONENT", x=k(v[0]), y=k(v[1]), z=k(v[2]))


def build_spec(case, ent, body_names):
    import simscale_sdk as sim
    const = lambda v: sim.ConstantFunction(type="CONSTANT", value=v)  # noqa: E731
    ref = lambda idx: sim.TopologicalReference(entities=sorted({e for i in idx for e in ent[i]}), sets=[])  # noqa: E731
    bcs = []
    for n, (label, idx) in enumerate(case["fixed"]):
        bcs.append(sim.FixedSupportBC(type="FIXED_SUPPORT", name=f"Fixed support {n + 1}", topological_reference=ref(idx)))
    for n, ld in enumerate(case["loads"]):
        if ld["kind"] == "remote":
            bcs.append(sim.RemoteForceLoadBC(
                type="REMOTE_FORCE_LOAD", name=f"Remote force {n + 1}",
                force=sim.DimensionalVectorFunctionForce(value=comp(ld["force_N"]), unit="N"),
                remote_point=sim.DimensionalVectorLength(value=sim.DecimalVector(*[x * 1e-3 for x in ld["point_mm"]]), unit="m"),
                deformation_behavior="UNDEFORMABLE", enable_search_radius=False, topological_reference=ref(ld["idx"])))
        else:
            bcs.append(sim.ForceLoadBC(
                type="FORCE_LOAD", name=f"Force {n + 1}",
                force=sim.DimensionalVectorFunctionForce(value=comp(ld["force_N"]), unit="N"),
                topological_reference=ref(ld["idx"])))
    mat = sim.SolidMaterial(
        name="PETG", material_behavior=sim.LinearElasticMaterialBehavior(
            type="LINEAR_ELASTIC", directional_dependency=sim.IsotropicDirectionalDependency(
                type="ISOTROPIC", youngs_modulus=sim.DimensionalFunctionPressure(value=const(E_PA), unit="Pa"), poissons_ratio=const(NU))),
        density=sim.DimensionalFunctionDensity(value=const(RHO), unit="kg/m³"),
        topological_reference=sim.TopologicalReference(entities=body_names, sets=[]))
    model = sim.SolidModel(magnitude=sim.DimensionalFunctionAcceleration(value=const(G if case["gravity"] else 0.0), unit="m/s²"),
                           e=sim.DimensionalVectorLength(value=sim.DecimalVector(0, 0, -1), unit="m"))
    return sim.StaticAnalysis(
        type="STATIC_ANALYSIS", non_linear_analysis=False,
        connection_groups=[sim.Contact(type="CONTACT", node_merging_bonded=False, connections=[])], connectors=[],
        element_technology=sim.SolidElementTechnology(element_technology3_d=sim.ElementTechnology(definition_method=sim.AutomaticElementDefinitionMethod(type="AUTOMATIC"))),
        model=model, materials=[mat], initial_conditions=sim.SolidInitialConditions(), boundary_conditions=bcs,
        numerics=sim.SolidNumerics(solver=sim.ChronosSolver(
            type="CHRONOS", convergence_threshold=1.0e-6, max_iterations=1000, non_convergence_action="SWITCH_TO_DIRECT_SOLVER",
            advanced_settings=sim.AdvancedChronosSettings(force_fsai=False, smoother="FSAI_LIGHT", prolongation="ENERGY_MINIMIZATION", improve_test_space=False,
                                                          preconditioner_recycling=1, restart_gmres=50, distributed_matrix_storage=True, num_of_threads=0,
                                                          verbosity=0, write_coords_and_matrix=0)), remote_point_stiffness_multiplier=0),
        simulation_control=sim.SolidSimulationControl(
            pseudo_time_stepping=sim.SingleStepPseudoTimeStepping(type="SINGLE_STEP", static_timesteps=sim.DimensionalTime(value=0, unit="s")),
            processors=sim.ComputingCore(num_of_processors=-1, num_of_computing_processors=-1, domain_decomposition=sim.AutomaticDomainDecomposition(type="AUTOMATIC"),
                                         num_of_threads=1, partition_mesh=False),
            max_run_time=sim.DimensionalTime(value=3600, unit="s")),
        result_control=sim.SolidResultControl(
            solution_fields=[sim.DisplacementResultControlItem(type="DISPLACEMENT", name="Displacement", displacement_type=sim.GlobalDisplacementType(type="GLOBAL")),
                             sim.StressResultControlItem(type="STRESS", name="Cauchy stress", stress_type=sim.GlobalCauchyStressType(type="CAUCHY")),
                             sim.StressResultControlItem(type="STRESS", name="Von Mises stress", stress_type=sim.GlobalVonMisesStressType(type="VON_MISES")),
                             sim.StrainResultControlItem(type="STRAIN", name="Total strain", strain_type=sim.GlobalTotalStrainType(type="TOTAL"))],
            edge_calculation=[], area_calculation=[], volume_calculation=[], point_data=[]),
        mesh_order="SECOND")


STATE_FILE = OUT / "state.json"


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=1), encoding="utf-8")


def run_simscale(piece, case, ent, gid, pid, api, fineness, state, rehacer):
    import simscale_sdk as sim
    key = f"{piece}/{case['name']}"
    S = state.setdefault(key, {})
    if rehacer or S.get("gid") != gid:
        S.clear()
    S["gid"] = gid
    bodies = [e.name for e in mappings(api, pid, gid, "region")]      # the solid(s): class "region"
    SM_ = sim.SimulationsApi(api)
    M = sim.MeshOperationsApi(api)
    # simulation first (a structural mesh needs the simulation id), without mesh; the mesh id is added afterwards
    if not S.get("sim_id"):
        spec = sim.SimulationSpec(name=f"{piece}: {case['name']}", geometry_id=gid, model=build_spec(case, ent, bodies))
        S["sim_id"] = SM_.create_simulation(pid, spec).simulation_id
        save_state(state)
    if not S.get("mesh_op"):
        algo = sim.SimmetrixMeshingSolid(
            type="SIMMETRIX_MESHING_SOLID", sizing=sim.AutomaticMeshSizingSimmetrix(type="AUTOMATIC_V9", fineness=fineness, curvature=sim.AutomaticCurvature(type="AUTOMATIC_CURVATURE")),
            refinements=[], automatic_sweep_parameters=sim.AutomaticSweepOff(type="AUTOMATIC_SWEEP_MESHING_OFF"), num_of_processors=-1,
            max_meshing_run_time=sim.DimensionalTime(value=18000, unit="s"))
        S["mesh_op"] = M.create_mesh_operation(pid, sim.MeshOperation(name=f"Mesh {piece} f{fineness:g}", geometry_id=gid, model=algo)).mesh_operation_id
        save_state(state)
        try:
            est = M.estimate_mesh_operation(pid, S["mesh_op"])
            S["mesh_estimate"] = est.to_dict()
            print("   mesh estimate:", str(S["mesh_estimate"])[:260])
        except Exception as e:       # noqa: BLE001
            print("   estimate failed:", api_err(e))
    if not S.get("mesh_id"):
        cur = M.get_mesh_operation(pid, S["mesh_op"])
        if str(cur.status) not in ("RUNNING", "FINISHED", "QUEUED"):
            M.start_mesh_operation(pid, S["mesh_op"], simulation_id=S["sim_id"])
        done = wait(lambda: M.get_mesh_operation(pid, S["mesh_op"]), label="mesh", every=8)
        S["mesh_id"] = done.mesh_id
        save_state(state)
    spec = SM_.get_simulation(pid, S["sim_id"])       # always push the current setup + mesh (re-runs after a setup fix)
    spec.mesh_id = S["mesh_id"]
    spec.model = build_spec(case, ent, bodies)
    SM_.update_simulation(pid, S["sim_id"], spec)
    chk = SM_.check_simulation_setup(pid, S["sim_id"])
    sev = str(getattr(chk, "severity", ""))
    msgs = [str(getattr(e, "message", e)) for e in (chk.entries or [])]
    print("   setup check:", sev, msgs[:4])
    S["check"] = dict(severity=sev, entries=msgs[:10])
    if sev == "ERROR":
        raise RuntimeError("simulation setup has errors: " + "; ".join(msgs[:3]))
    R = sim.SimulationRunsApi(api)
    if not S.get("run_id"):
        run = R.create_simulation_run(pid, S["sim_id"], sim.SimulationRun(name=f"Run {time.strftime('%Y-%m-%d %H:%M')}"))
        S["run_id"] = run.run_id
        save_state(state)
        try:
            est = SM_.estimate_simulation_setup(pid, S["sim_id"])
            S["run_estimate"] = est.to_dict() if hasattr(est, "to_dict") else str(est)
            print("   run estimate:", str(S["run_estimate"])[:300])
        except Exception as e:       # noqa: BLE001
            print("   run estimate failed:", api_err(e))
        R.start_simulation_run(pid, S["sim_id"], S["run_id"])
    done = wait(lambda: R.get_simulation_run(pid, S["sim_id"], S["run_id"]), label="run", every=8)
    S["duration"] = str(done.duration)
    S["compute"] = done.compute_resource.to_dict() if done.compute_resource else None
    return S


def links(pid, sim_id, run_id, results):
    base = f"https://www.simscale.com/workbench/?pid={pid}"
    d = dict(proyecto=base, simulacion=f"{base}&mi=spec:{sim_id}%2Cservice:SIMULATION%2Cstrategy:1")
    for r in results:
        url = getattr(r, "workbench_url", None)
        if url and "VON" in str(getattr(r, "category", "")).upper() or (url and "von" in str(url).lower()):
            d["resultado"] = url
    return d


def fetch_results(api, pid, state_entry, out_dir):
    """Download the solution fields of the run; returns the list of result items."""
    import simscale_sdk as sim
    R = sim.SimulationRunsApi(api)
    res = R.get_simulation_run_results(pid, state_entry["sim_id"], state_entry["run_id"], limit=100)
    return res.embedded


def face_mesh(f, tol=0.2):
    import pyvista as pv
    v, tri = f.tessellate(tol, 0.3)
    if not tri:
        return None
    pts = np.array([(p.x, p.y, p.z) for p in v])
    cells = np.hstack([[3, *t_] for t_ in tri])
    return pv.PolyData(pts, cells)


def render_bc(faces, case, path, piece):
    """Capture of the boundary conditions: the part in grey, supports in blue, loads in red/orange with an arrow."""
    import pyvista as pv
    pl = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    pl.set_background("white")
    meshes = [m for m in (face_mesh(f) for f in faces) if m is not None]
    pl.add_mesh(meshes[0].merge(meshes[1:]) if len(meshes) > 1 else meshes[0], color="#c9ccd1", opacity=0.55, show_edges=False)
    legend = []

    def paint(idx, color):
        ms = [m for m in (face_mesh(faces[i], 0.05) for i in idx) if m is not None]
        if ms:
            pl.add_mesh(ms[0].merge(ms[1:]) if len(ms) > 1 else ms[0], color=color, show_edges=False)
    for label, idx in case["fixed"]:
        paint(idx, "#1f5fbf")
        legend.append([f"APOYO: {label}", "#1f5fbf"])
    palette = ["#d62728", "#ff7f0e", "#9467bd", "#8c564b"]
    allpts = np.vstack([m.points for m in meshes])
    diag = float(np.linalg.norm(allpts.max(0) - allpts.min(0)))
    for n, ld in enumerate(case["loads"]):
        col = palette[n % len(palette)]
        paint(ld["idx"], col)
        legend.append([f"CARGA: {ld['label']} ({', '.join(f'{v:.1f}' for v in ld['force_N'])} N)", col])
        fv = np.array(ld["force_N"], float)
        if np.linalg.norm(fv) > 0:
            ctr = np.mean([faces[i].Center().toTuple() for i in ld["idx"]], axis=0) if ld["kind"] != "remote" else np.array(ld["point_mm"], float)
            d = fv / np.linalg.norm(fv)
            pl.add_mesh(pv.Arrow(start=ctr - d * diag * 0.22, direction=d, scale=diag * 0.22, tip_length=0.3, tip_radius=0.08, shaft_radius=0.03), color=col)
    pl.add_legend(legend, bcolor="white", size=(0.62, 0.18), loc="upper left")
    pl.add_text(f"{piece}: condiciones de borde", font_size=11, color="black", position="lower_left")
    pl.view_isometric()
    pl.screenshot(str(path))
    pl.close()


def collect(api, pid, S, piece, case):
    """Export the solution as VTK, download it, read the maxima with PyVista and render von Mises / displacement / mesh."""
    import pyvista as pv
    import simscale_sdk as sim
    items = fetch_results(api, pid, S, OUT)
    sol = next((r for r in items if r.type == "SOLUTION_FIELD"), None)
    if sol is None:
        raise RuntimeError("the run has no solution field")
    d = OUT / "_res" / f"{piece}_{S['run_id'][:8]}"      # one folder per run: a re-run never reads an old result
    if not list(d.glob("**/*.vtu")):
        E = sim.SimulationResultExportsApi(api)
        x = E.create_export(pid, sim.CreateExportRequest(result_id=sol.result_id, format="VTK"))
        for _ in range(200):
            g = E.get_export(pid, x.export_id)
            print(f"   export: {g.status}", flush=True)
            if g.status in ("DONE", "FINISHED", "SUCCESS", "COMPLETED") and g.url:
                break
            if g.status in ("FAILED", "ERROR"):
                raise RuntimeError(f"VTK export failed {g.error_code}")
            time.sleep(5)
        r = requests.get(g.url, timeout=900)
        print(f"   download {r.status_code} {len(r.content) // 1024} KB", flush=True)
        r.raise_for_status()
        d.mkdir(parents=True, exist_ok=True)
        zf = d / "res.zip"
        zf.write_bytes(r.content)
        with zipfile.ZipFile(zf) as z:
            z.extractall(d)
        zf.unlink()
    vtu = sorted(d.glob("**/*.vtu"))[0]
    m = pv.read(str(vtu))
    m = m.combine() if hasattr(m, "combine") else m
    vm = np.asarray(m["von Mises stress"], float) / 1e6                   # Pa -> MPa
    u = np.linalg.norm(np.asarray(m["displacement"], float), axis=1) * 1e3  # m -> mm
    m["vm_MPa"], m["u_mm"] = vm, u
    smax, p995 = float(vm.max()), float(np.percentile(vm, 99.5))
    pos = np.asarray(m.points)
    where = (pos[int(vm.argmax())] * 1e3).round(1).tolist()
    stats = dict(nodos=int(m.n_points), celdas=int(m.n_cells), sigma_max_MPa=smax, sigma_p995_MPa=p995, sigma_max_en_mm=where,
                 FS=SIGMA_ALLOW / smax, FS_p995=SIGMA_ALLOW / p995, u_max_mm=float(u.max()))
    surf = m.extract_surface()
    shots = {}
    for name, arr, title, cmap, clim in (("vonmises", "vm_MPa", f"von Mises (MPa), max {smax:.2f}", "turbo", [0, smax]),
                                         ("desplazamiento", "u_mm", f"desplazamiento (mm), max {stats['u_max_mm']:.3f}", "viridis", [0, stats["u_max_mm"]])):
        pl = pv.Plotter(off_screen=True, window_size=(1600, 1000))
        pl.set_background("white")
        pl.add_mesh(surf, scalars=arr, cmap=cmap, clim=clim, scalar_bar_args=dict(title=title, color="black"))
        pl.add_text(f"{piece}: {title}", font_size=11, color="black")
        pl.view_isometric()
        f = OUT / f"{piece}_{name}.png"
        pl.screenshot(str(f))
        pl.close()
        shots[name] = f.name
    pl = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    pl.set_background("white")
    pl.add_mesh(surf, color="#dfe3e8", show_edges=True, edge_color="#555555", line_width=0.4)
    pl.add_text(f"{piece}: malla de SimScale ({stats['celdas']} celdas, segundo orden)", font_size=11, color="black")
    pl.view_isometric()
    f = OUT / f"{piece}_malla.png"
    pl.screenshot(str(f))
    pl.close()
    shots["malla"] = f.name
    return dict(resultado=stats, capturas=shots, enlace_resultado=sol.workbench_url,
                enlace_proyecto=f"https://www.simscale.com/workbench/?pid={pid}",
                enlace_simulacion=f"https://www.simscale.com/workbench/?pid={pid}&mi=spec:{S['sim_id']}%2Cservice:SIMULATION%2Cstrategy:1")


def expand_remote(case, faces):
    """The API has no way to give the remote force its point ("There is no Point assigned"), so each remote load becomes one force load per hole,
    statically equivalent to the force F at the point P: same resultant and same moment about the hole centroid (minimum-norm split, xz plane)."""
    out = []
    for ld in case["loads"]:
        if ld["kind"] != "remote":
            out.append(ld)
            continue
        groups = {}
        for i in ld["idx"]:
            c = faces[i].Center()
            groups.setdefault((round(c.x * 2) / 2, round(c.y * 2) / 2, round(c.z * 2) / 2), []).append(i)
        cs = np.array([np.mean([faces[i].Center().toTuple() for i in ix], axis=0) for ix in groups.values()])
        cen = cs.mean(0)
        r = cs - cen
        P_ = np.array(ld["point_mm"], float) - cen
        F = np.array(ld["force_N"], float)
        m_y = P_[2] * F[0] - P_[0] * F[2]          # moment about y of F at P, taken at the centroid of the holes (N mm)
        n = len(cs)
        # unknown f = [Fx_1..n, Fz_1..n]: sum Fx = F0, sum Fz = F2, sum(rz Fx - rx Fz) = m_y
        A = np.vstack([np.r_[np.ones(n), np.zeros(n)], np.r_[np.zeros(n), np.ones(n)], np.r_[r[:, 2], -r[:, 0]]])
        f = np.linalg.lstsq(A, np.array([F[0], F[2], m_y]), rcond=None)[0]
        if np.linalg.norm(A @ f - [F[0], F[2], m_y]) > 1e-6 * (1 + abs(m_y)):
            raise RuntimeError("the holes cannot carry the moment of the remote force (they are aligned)")
        for k, ix in enumerate(groups.values()):
            out.append(dict(kind="force", label=f"{ld['label']} (agujero {k + 1} de {n})", idx=ix, force_N=(float(f[k]), 0.0, float(f[n + k]))))
    case = dict(case)
    case["loads_equivalentes"] = out
    return case


def process(piece, a, api_holder, state):
    """One piece end to end. Returns the result dict that is saved as salida/simscale/<piece>.json."""
    sh, faces, info, case = prepare(piece)
    pick_report = dict(fijos=[dict(label=l, caras=len(ix), area_mm2=round(total_area(info, ix), 1)) for l, ix in case["fixed"]],
                       cargas=[dict(label=ld["label"], caras=len(ld["idx"]), area_mm2=round(total_area(info, ld["idx"]), 1), fuerza_N=[round(v, 3) for v in ld["force_N"]])
                               for ld in case["loads"]])
    for r in pick_report["fijos"] + pick_report["cargas"]:
        if r["caras"] == 0:
            raise RuntimeError(f"{piece}: no faces found for '{r['label']}'")
    print(f"== {piece}: {case['name']}  faces {len(faces)}", json.dumps(pick_report, ensure_ascii=False))
    named = OUT / "_named" / f"{piece}.step"
    name_step(sh, faces, named)
    res = dict(pieza=piece, grupo=PIECES[piece]["grupo"], caso=case["name"], titulo=case["titulo"], notas=case["notes"], seleccion=pick_report,
               material=dict(E_MPa=E_PA / 1e6, nu=NU, rho=RHO, sigma_adm_MPa=SIGMA_ALLOW), fineness=a.fineness)
    (OUT / f"{piece}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    render_bc(faces, case, OUT / f"{piece}_condiciones.png", piece)
    if a.solo_preparar:
        return res
    if "api" not in api_holder:
        api_holder["api"] = client()
    api = api_holder["api"]
    pid = get_project(api, PIECES[piece]["grupo"])
    gid, gname = import_geometry(api, pid, piece, named, PIECES[piece]["step"])
    ent = face_entities(api, pid, gid, len(faces))
    dup = [i for i, v in ent.items() if len(v) != 1]
    print(f"   geometry {gname}: {len(ent)} faces mapped, {len(dup)} split by the import")
    res.update(project_id=pid, geometry_id=gid)
    S = run_simscale(piece, expand_remote(case, faces) | {"loads": expand_remote(case, faces)["loads_equivalentes"]}, ent, gid, pid, api, a.fineness, state, a.rehacer)
    res.update(sim_id=S["sim_id"], run_id=S["run_id"], mesh_id=S["mesh_id"], check=S.get("check"), duracion=S.get("duration"), compute=S.get("compute"))
    res.update(collect(api, pid, S, piece, case))
    (OUT / f"{piece}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return res


LOCAL = {"M3s_riel_gancho": "riel_agua", "M5s_capsula_tapa_pie": "pie"}      # SimScale piece -> case of the local CalculiX (fem.json)
ORDEN = ["M3s_riel_gancho", "M5s_capsula_tapa_pie", "M1s_caja_cuerpo", "B3_caja", "B2_cubierta_lisa", "B2_cubierta_mastil",
         "B2_cubierta_lisa_lateral", "B2_cubierta_mastil_lateral"]


CORRECCION_8MM = '### Corrección del mismo día: cubierta de la boya con barras de 8 mm\n\nCon barras de 4 mm la cubierta no aguantaba la ola (tabla de arriba). Por eso **las barras de B2 pasaron de 4 a 8 mm** (`boya_pet.cubierta_espesor`). La boya sigue estable: calado 41,6 mm, francobordo 83,9 mm, GM 101/710 mm, 1014 g impresos.\n\nLa simulación con la cubierta nueva **corrió en SimScale** (proyecto B), pero el plan gratuito no dejó descargar el resultado: devolvió el error 403 «export-source-locked». Por eso se verificó en la computadora con CalculiX, usando el mismo golpe de 200 N sobre las barras y la cubierta sujeta en sus agujeros M3. Antes se comprobó que el cálculo local da lo mismo que SimScale con la cubierta vieja:\n\n| Media cubierta | Barras | σ p99.5 (MPa) | FS = 50/σ p99.5 | σ pico (MPa) | Flecha (mm) | Fuente |\n|---|---|---|---|---|---|---|\n| B2 lisa | 4 mm | 58,6 | 0,85 | 120 | 35,5 | local (SimScale: 58,6 y 34,5: coincide) |\n| B2 lisa | **8 mm** | **16,4** | **3,0** | 38,7 | **5,2** | local |\n| B2 mástil | **8 mm** | **16,3** | **3,1** | 34,1 | **5,3** | local |\n\nLa cubierta de 8 mm **cumple** el golpe vertical de 200 N con FS 3 (sin contar los picos de los bordes de los agujeros), aunque cada mitad recibe los 200 N enteros, lo que es exagerado. Queda pendiente el golpe **lateral** sobre el panel solar, que hace de vela: lo resisten las 4 columnas Ø12 del panel, no las barras. Ver `docs/PENDIENTES.md`.\n\n**Cómo leer «σ máx.» y «σ p99.5».** «σ máx.» es el valor de un solo punto de la malla, en el borde de un agujero o en el lugar donde se aplica la carga. Ese pico sale de cómo se modela, no de la pieza. Por eso el cálculo local usa el percentil 99,5, que ignora el 0,5 % de puntos más altos. Con ese criterio, el riel da FS 11, el pie de la cápsula FS 6,8 y la caja M1s FS 6,5 frente a 50 MPa. Además, el cálculo local verifica la resistencia **entre capas**, que es la mitad: 22 MPa. Ahí el riel da FS 3,2 y el pie FS 3,8.\n'
# History of the 4 -> 8 mm change of the B2 bars (04/11), kept here so --informe does not lose it; the numbers are historical, never regenerated.


def informe():
    """docs/REPORTE_SIMSCALE_LanternGuard.md from docs/resultados/resultados.json (+ the per-piece JSON of salida/simscale), Spanish, plain language."""
    res_f = MOD / "docs" / "resultados" / "resultados.json"
    if not res_f.exists():
        raise SystemExit("run resultados_bloque3.py (or --resultados) first: docs/resultados/resultados.json is missing")
    R = json.loads(res_f.read_text(encoding="utf-8"))
    rows, secs = [], []
    for k in ORDEN:
        e = R.get(k)
        if not e:
            continue
        jf = OUT / f"{k}.json"
        d = json.loads(jf.read_text(encoding="utf-8")) if jf.exists() else {}
        ok = e["fs_p995"] >= 1 and e["fs_capas"] >= 1
        verdict = "cumple" if (ok and e["fs"] >= 1) else ("cumple sin picos" if ok else "NO cumple")
        ss = f"{e['sigma_simscale']:.1f} / {e['umax_simscale_mm']:.2f}" if e.get("sigma_simscale") is not None else "no hay"
        rows.append(f"| {k} | {e['titulo']} | **{e['fuente']}** | {e['sigma_max']:.1f} | {e['fs']:.2f} | {e['sigma_p995']:.1f} | {e['fs_capas']:.2f} | {e['umax_mm']:.2f} | "
                    f"{e['sigma_local']:.1f} / {e['umax_local_mm']:.2f} | {ss} | **{verdict}** | [abrir]({e['link']}) |")
        sel = ""
        if d.get("seleccion"):
            sel = "\n".join(f"- Apoyo fijo: {x['label']} → {x['caras']} caras, {x['area_mm2']} mm²" for x in d["seleccion"]["fijos"])
            sel += "\n" + "\n".join(f"- Carga: {x['label']} → {x['caras']} caras, {x['area_mm2']} mm², fuerza {x['fuerza_N']} N" for x in d["seleccion"]["cargas"])
        img = lambda s: f"![{k} {s}](resultados/{k}/{s}.png)"      # noqa: E731
        why = f" Motivo: {e['motivo_fuente']}." if e.get("motivo_fuente") else ""
        secs.append(f"### {k}\n\n{e['titulo']}.\n\n" + "\n".join(f"- {n}" for n in e["notas"]) + f"\n\n**Caras elegidas (verificadas por conteo y área):**\n\n{sel}\n\n"
                    f"**Resultado ({e['fuente']}):** σ máxima {e['sigma_max']:.2f} MPa (FS {e['fs']:.2f}); σ sin el 0.5 % de picos {e['sigma_p995']:.2f} MPa "
                    f"(FS {e['fs_p995']:.2f} en el plano de las capas con 50 MPa; FS **entre capas** {e['fs_capas']:.2f} con 22 MPa); desplazamiento máximo {e['umax_mm']:.2f} mm; "
                    f"malla de {e['malla']['celdas']} elementos.{why}\n\n"
                    f"[Proyecto en SimScale]({e['link_proyecto']}) · [Simulación]({e['link_simulacion']}) · [Resultado]({e['link']})\n\n"
                    f"Escalas fijas en todas las imágenes: esfuerzo 0 a 50 MPa y desplazamiento 0 a 6 mm (magenta = pasa del tope).\n\n"
                    f"{img('condiciones')}\n\n{img('vonmises')}\n\n{img('desplazamiento')}\n\n{img('malla')}\n")
    lat = R.get("B2_cubierta_mastil_lateral") or R.get("B2_cubierta_lisa_lateral")
    lat_txt = ""
    if lat:
        half = lat["sigma_p995"] / 2
        lat_txt = (f"- **Golpe lateral de 200 N sobre el panel (cubierta de 8 mm): {'cumple' if lat['cumple'] else 'NO cumple'}.** σ sin picos {lat['sigma_p995']:.1f} MPa (FS {lat['fs_p995']:.2f} en el plano, "
                   f"{lat['fs_capas']:.2f} entre capas), desplazamiento {lat['umax_mm']:.0f} mm. Los 200 N entran enteros por las 2 columnas de una sola mitad (exagerado). Si se reparten entre las dos "
                   f"mitades (100 N cada una; el esfuerzo es proporcional a la carga) queda σ ≈ {half:.0f} MPa: FS {SIGMA_ALLOW / half:.1f} en el plano pero {22.0 / half:.2f} entre capas, "
                   "es decir, **las columnas Ø12 no cumplirían entre capas** aun con el reparto. La flecha de decenas de mm también muestra que la cubierta se dobla mucho.")
    head = f"""# LanternGuard: simulación con SimScale (cálculo por API)

Fecha: {time.strftime('%d/%m/%Y')}. Este documento se explica solo: no hace falta abrir el repositorio.

## Qué se hizo

Se calculó cuánto se deforma y cuánto esfuerzo soporta cada pieza impresa del nodo sumergido (grupo A) y de la boya (grupo B) bajo las cargas de uso, con el programa
SimScale (plan gratuito, por su API) y, cuando SimScale no entrega el resultado o todavía no corrió la geometría actual, con CalculiX en la computadora **con el mismo caso**
(mismas caras, mismas fuerzas, mismo material). Son dos proyectos separados: **«{PROJECTS['A']}»** y **«{PROJECTS['B']}»**. Todo lo hace `cad_final/simscale_run.py`
(`python simscale_run.py --pieza NOMBRE`; el informe con `--informe`) y `cad_final/resultados_bloque3.py` (imágenes y `docs/resultados/resultados.json`).

- **Material (PETG):** E = 2.1 GPa, ν = 0.38, densidad 1270 kg/m³. Esfuerzo admisible 50 MPa en el plano de las capas (el cálculo local de la versión simple usaba 45) y 22 MPa **entre capas**.
- **FS = 50 / σ máxima** (cuántas veces cabe la carga hasta el límite). **FS entre capas = 22 / σ p99.5.** σ p99.5 es el esfuerzo sin el 0.5 % de puntos más altos: los picos
  en el borde de un apoyo o de un agujero cargado son un efecto del modelo («pellizca» la pieza), por eso la regla del proyecto juzga con el p99.5. «Cumple» = FS ≥ 1 con p99.5 en ambos sentidos.
- **Fuente de cada resultado:** «SimScale» solo si la corrida existe, se pudo descargar y corrió **la geometría actual**; si no, «FEM local». Local y SimScale coinciden en las piezas
  que tienen los dos (desplazamientos dentro de 3 %).
- **Escalas de color fijas** en todas las imágenes (esfuerzo 0 a 50 MPa; desplazamiento 0 a 6 mm), para poder comparar piezas a simple vista.
- **La flotación y la estabilidad de la boya NO son de este cálculo:** son analíticas y están en `docs/BOYA.md`. El diagrama de cargas del conjunto está en `docs/CARGAS_CONJUNTO.pdf`.

## Resultados

| Pieza | Caso | Fuente | σ máx. (MPa) | FS = 50/σ máx. | σ p99.5 (MPa) | FS entre capas (22/σ p99.5) | Desplaz. (mm) | Local: σ máx. / desplaz. | SimScale: σ máx. / desplaz. | Veredicto | Enlace |
|---|---|---|---|---|---|---|---|---|---|---|---|
"""
    mid = """

Lectura: «cumple» = FS ≥ 1 con σ máx. y con σ p99.5 en los dos sentidos; «cumple sin picos» = pasa con p99.5 pero el pico puntual supera 50 MPa (criterio propio, no normativo).
Los enlaces abren la simulación en SimScale (proyecto público del plan gratuito).

## Cargas y apoyos (supuestos, en lenguaje simple)

- **Nodo sumergido (A):** 150 N hacia abajo en el frente de la cápsula (manipulación), más la corriente de 1.5 m/s: presión 0.5 · 1025 · 1.5² = 1153 Pa sobre el frente
  de la cápsula (área de su sección, Cd = 1), convertida en una fuerza en −X en el mismo punto, porque estas piezas no incluyen el cuerpo de la cápsula.
- **Ajuste obligado:** la API de SimScale no deja asignar el punto de una «fuerza remota» («There is no Point assigned»). En su lugar, los 150 N se reparten en una fuerza
  por cada agujero de unión con la misma fuerza total y el mismo momento que daría el cuerpo rígido (reparto de mínima norma). El cálculo local usa **ese mismo reparto**.
- **Caja del nodo (M1s):** caso propio: la caja cuelga de los agujeros M3 de la brida de la tapa (como al izar por el asa) y el riel con la cápsula tira de los 4 M4 del cojín +X.
- **Boya (B):** peso de la electrónica y del panel solar (350 g), de la tapa y de la antena, más un golpe de ola de 200 N. En la caja, los 200 N empujan de lado una pared larga.
  En cada media cubierta hay dos casos: golpe vertical de 200 N sobre las barras, y golpe lateral de 200 N sobre el panel (que baja por sus columnas). Cada mitad recibe los 200 N enteros (exagerado a propósito).
- **Apoyos de la boya:** la caja va atornillada por sus 4 orejas a los pilares de la cubierta (se fija la huella de Ø10 de cada pilar); cada media cubierta, a los 4 postes del casco (huella de Ø10 de cada poste).
- **Cómo se eligieron las caras:** cada cara del STEP se «bautiza» (LGF0000, LGF0001…) y SimScale conserva ese nombre; los apoyos y cargas se escogen por posición y orientación y se comprueba conteo y área.
  Las cargas del cálculo local se reparten de forma consistente sobre los triángulos de esas mismas caras.

""" + CORRECCION_8MM + """
## Piezas

"""
    tail = """
## Qué dicen los resultados

""" + "\n".join(f"- **{k}** ({R[k]['fuente']}): FS {R[k]['fs']:.2f} (pico), {R[k]['fs_p995']:.1f} sin picos, {R[k]['fs_capas']:.2f} entre capas, {R[k]['umax_mm']:.2f} mm." for k in ORDEN if k in R) + f"""
{lat_txt}

## Límites y avisos

- Las corridas de SimScale de la cubierta con barras de 8 mm terminaron bien pero el plan gratuito devolvió 403 «export-source-locked» al descargar el resultado; por eso esas piezas salen con FEM local.
  No se usaron capturas del visor web de SimScale: la clave de la API no inicia sesión en la página y no hay una sesión abierta.
- El enlace de cada proyecto es el que usa el sitio para proyectos compartidos (`workbench/?pid=...`). El plan gratuito deja los proyectos públicos (contienen solo geometría y resultados de estas piezas);
  desde el script no se puede comprobar el acceso sin iniciar sesión, conviene abrirlo una vez en una ventana privada.
- No se simuló estanqueidad, fatiga ni el efecto de las capas de impresión (material isótropo; las capas solo entran en el FS entre capas). Los STEP son los de `salida/prototipos/P2_robusto/step` y `salida/boya_pet/step` del momento de la corrida.
- El FEM local usa el máximo por elemento (puntos de integración) y no el valor nodal de SimScale; el p99.5 de los dos es comparable, el máximo puntual puede diferir.
- Los resultados dependen de las cargas supuestas arriba: si el equipo fija otras (por ejemplo la ola real), se corre de nuevo con el script.
"""
    out = MOD / "docs" / "REPORTE_SIMSCALE_LanternGuard.md"
    out.write_text(head + "\n".join(rows) + mid + "\n".join(secs) + tail, encoding="utf-8")
    print("written", out)
    try:
        import entrega_pdf
        entrega_pdf.main(out)
    except Exception as e:       # noqa: BLE001
        print("PDF failed:", e)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pieza", action="append", default=[])
    ap.add_argument("--grupo", choices=["A", "B"])
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--listar", metavar="PIEZA")
    ap.add_argument("--solo-preparar", action="store_true")
    ap.add_argument("--fineness", type=float, default=5.0)
    ap.add_argument("--rehacer", action="store_true")
    ap.add_argument("--informe", action="store_true", help="write docs/REPORTE_SIMSCALE_LanternGuard.md/.pdf from docs/resultados/resultados.json")
    ap.add_argument("--resultados", action="store_true", help="images + docs/resultados/resultados.json for the chosen pieces (default all) with NO SimScale run: SimScale where it has the current geometry, local FEM otherwise")
    ap.add_argument("--malla", type=float, default=3.0, help="local FEM mesh size in mm (resultados)")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.informe:
        informe()
        return 0
    if a.resultados:
        import resultados_bloque3 as RB
        return RB.update(list(a.pieza) or list(ORDEN), a.malla, False)
    if a.listar:
        sh, faces, info, case = prepare(a.listar)
        for lbl, idx in case["fixed"]:
            print("FIJO", lbl, len(idx), f"{total_area(info, idx):.1f} mm2", [round(info[i]['c'][0]) for i in idx][:8])
        for ld in case["loads"]:
            print("CARGA", ld["label"], len(ld["idx"]), f"{total_area(info, ld['idx']):.1f} mm2", ld["force_N"])
        return 0
    names = list(a.pieza)
    if a.grupo:
        names += [k for k, v in PIECES.items() if v["grupo"] == a.grupo]
    if a.todo:
        names = list(PIECES)
    for k in names:
        if k not in PIECES:
            raise SystemExit(f"unknown piece {k}: {list(PIECES)}")
    print("pieces:", names)
    state_f = OUT / "state.json"
    state = json.loads(state_f.read_text(encoding="utf-8")) if state_f.exists() else {}
    holder, rc = {}, 0
    for k in names:
        try:
            process(k, a, holder, state)
        except Exception as e:       # noqa: BLE001
            rc = 1
            print(f"FAILED {k}: {type(e).__name__}: {api_err(e) if hasattr(e, 'status') else e}")
        finally:
            state_f.write_text(json.dumps(state, indent=1), encoding="utf-8")
    if names and not a.solo_preparar:        # images (docs/resultados/<piece>/*.png) + resultados.json, then the report
        import resultados_bloque3 as RB
        rc = RB.update(names, a.malla, False) or rc
        informe()
    return rc


if __name__ == "__main__":
    sys.exit(main())
