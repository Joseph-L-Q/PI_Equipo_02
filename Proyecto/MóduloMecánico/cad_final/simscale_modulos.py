"""SimScale by ASSEMBLED MODULE (docs/ENCARGO_SIMSCALE_2026-11-07.md): one upload per module, linear static, bonded contacts.

    python simscale_run.py --modulo nodo|boya|tierra [--fineness 4] [--rehacer]      (or python simscale_modulos.py ...)
    python simscale_modulos.py --listar nodo        picks + contacts + connectivity, no API call

Geometry = the assembly STEP delivered for printing (salida/limpio/step/00_ENSAMBLE_*.step, checked by verificar_entrega.py),
without the reference bodies (REF_linterna*, ref_botella*) and without the LR2 rings (not in the node list of the brief; the
support is the hook seat, the ring itself is a separate print verified in docs/ARO_Y_ESTACION.md).

Contacts: "bonded automatic" like the reference project. The API has no auto-detection, so it is done here the same way the
workbench does it: every pair of faces of two different solids closer than CONTACT_TOL becomes a bonded pair (master = faces of
the first solid, slave = faces of the second), position tolerance CONTACT_TOL. The solid graph must come out connected.
"""
import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cadquery as cq                                            # noqa: E402
from OCP.BRepExtrema import BRepExtrema_DistShapeShape            # noqa: E402

import simscale_run as R                                         # noqa: E402
import verificar_entrega as V                                     # noqa: E402

BASE_SPEC = R.build_spec          # the single-piece spec; run_simscale gets a wrapper of it

MOD = HERE.parent
OUT = MOD / "salida" / "simscale_modulos"
STATE = OUT / "state.json"
CONTACT_TOL = 0.35          # mm: bonded if two faces of different solids are closer than this (0.3 mm print clearances included)
PROJ_TOL = 1.0              # mm: SimScale position tolerance of each bonded pair (0.35 left "empty contact node list" on B2-B3 of the buoy)
G = 9.81

MATS = {"PETG": dict(E=2.1e9, nu=0.38, rho=1270.0, allow=50.0), "PLA": dict(E=3.5e9, nu=0.36, rho=1240.0, allow=40.0)}
MODULES = {
    "nodo": dict(project="LanternGuard 1 - Nodo sumergido", asm="00_ENSAMBLE_nodo", mat="PETG",
                 desc="LanternGuard submerged node, full printed assembly (closed rail, hooks D17.1, capsules, box, lid, trays, ballast frames), "
                      "PETG, linear static, bonded contacts. Support: hook seats on the ring. Loads: self weight + 990 g ballast as point mass, "
                      "150 N on one capsule, 1.5 m/s current as pressure."),
    "boya": dict(project="LanternGuard 2 - Boya", asm="00_ENSAMBLE_boya", mat="PETG", strict=True,
                 desc="LanternGuard buoy, full printed assembly (hull halves, deck halves with panel columns, dry box, lid, bottle cradles, straps), "
                      "PETG, linear static, bonded contacts. Support: mooring eyes. Loads: self weight, electronics/panel/antenna as point masses, "
                      "200 N wave on the deck, 200 N lateral hit on the panel, 300 N line pull reacted at the mooring."),
    "tierra": dict(project="LanternGuard 3 - Estacion de tierra", asm="00_ENSAMBLE_tierra", mat="PLA",
                   desc="LanternGuard ground station T1 box + T2 lid, PLA, linear static, bonded contacts. Fixed at the mounting tabs; "
                        "50 N on the lid, 30 N lateral on the SMA antenna connector."),
}


def keep(name):
    n = name.lower()
    return not (n.startswith("ref") or n.startswith("lr2_aro"))


# ------------------------------------------------------------------------------------------------ geometry
def load_module(mod):
    """[(name, cq.Solid)] of the printed solids, and the flat face table: info[i] = face_info + 'solid' index."""
    sol = [(n, cq.Solid(bake(s))) for n, v, s in V.named_solids(V.LIMPIO / f"{MODULES[mod]['asm']}.step") if keep(n)]
    faces, info = [], []
    for k, (n, s) in enumerate(sol):
        for f in s.Faces():
            d = R.face_info(f)
            d["solid"] = k
            faces.append(f)
            info.append(d)
    return sol, faces, info


def bake(s):
    """The solid with its assembly placement written into the geometry (no TopLoc_Location left), so XCAF can name its faces."""
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
    from OCP.TopLoc import TopLoc_Location
    loc = s.Location()
    if loc.IsIdentity():
        return s
    return BRepBuilderAPI_Transform(s.Located(TopLoc_Location()), loc.Transformation(), True).Shape()


def _bb_gap(a, b):
    return max(a[0] - b[3], b[0] - a[3], a[1] - b[4], b[1] - a[4], a[2] - b[5], b[2] - a[5], 0.0)


def face_to_face(fa, fb, ia, ib, tol):
    """Strict pair test: two planes facing each other (antiparallel normals), or two cylinders with parallel axes and radii within tol.
    Drops the pairs that only touch along an edge (a pillar side against a floor), which leave SimScale with an empty contact node list."""
    if ia["type"] == "PLANE" and ib["type"] == "PLANE":
        return sum(a * b for a, b in zip(ia["n"], ib["n"])) < -0.99
    if ia["type"] == "CYLINDER" and ib["type"] == "CYLINDER":
        ca, cb = fa._geomAdaptor().Cylinder(), fb._geomAdaptor().Cylinder()
        da, db = ca.Axis().Direction(), cb.Axis().Direction()
        par = abs(da.X() * db.X() + da.Y() * db.Y() + da.Z() * db.Z()) > 0.999
        return par and abs(ca.Radius() - cb.Radius()) <= tol
    return False


def contacts(sol, faces, info, tol=CONTACT_TOL, strict=False):
    """{(i, j): (faces of i, faces of j)} for every pair of solids that touch within tol (strict: face to face only, see face_to_face;
    then the first list is the master = the larger area, the second the slave)."""
    sbb = []
    for n, s in sol:
        b = s.BoundingBox()
        sbb.append((b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax))
    by_solid = {}
    for i, d in enumerate(info):
        by_solid.setdefault(d["solid"], []).append(i)
    res = {}
    for a in range(len(sol)):
        for b in range(a + 1, len(sol)):
            if _bb_gap(sbb[a], sbb[b]) > tol:
                continue
            fa = [i for i in by_solid[a] if _bb_gap(info[i]["bb"], sbb[b]) <= tol]
            fb = [j for j in by_solid[b] if _bb_gap(info[j]["bb"], sbb[a]) <= tol]
            ma, mb = set(), set()
            for i in fa:
                for j in fb:
                    if _bb_gap(info[i]["bb"], info[j]["bb"]) > tol:
                        continue
                    dd = BRepExtrema_DistShapeShape(faces[i].wrapped, faces[j].wrapped)
                    if dd.IsDone() and dd.Value() <= tol and (not strict or face_to_face(faces[i], faces[j], info[i], info[j], tol)):
                        ma.add(i)
                        mb.add(j)
            if ma:
                A, B = sorted(ma), sorted(mb)
                if strict and sum(info[i]["area"] for i in A) < sum(info[j]["area"] for j in B):
                    A, B = B, A
                res[(a, b)] = (A, B)
    return res


def components(n, pairs):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in pairs:
        parent[find(a)] = find(b)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def exterior_faces(sol, faces, info, direction, cos_min=0.5):
    """Faces whose outward normal points into `direction` (cos >= cos_min) and whose centre sees free space along it
    (a ray from the centre, offset 0.05 mm, hits no solid of the module): the wetted, upstream faces."""
    from OCP.gp import gp_Lin, gp_Pnt, gp_Dir
    from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
    ints = []
    for n, s in sol:
        it = IntCurvesFace_ShapeIntersector()
        it.Load(s.wrapped, 1e-6)
        ints.append(it)
    dx, dy, dz = direction
    out = []
    for i, f in enumerate(faces):
        try:
            c = f.Center()
            nv = f.normalAt(c)
        except Exception:      # noqa: BLE001
            continue
        if nv.x * dx + nv.y * dy + nv.z * dz < cos_min:
            continue
        p = gp_Pnt(c.x + 0.05 * dx, c.y + 0.05 * dy, c.z + 0.05 * dz)
        line = gp_Lin(p, gp_Dir(dx, dy, dz))
        blocked = False
        for it in ints:
            it.Perform(line, 0.0, 1e5)
            if it.IsDone() and it.NbPnt() > 0:
                blocked = True
                break
        if not blocked:
            out.append(i)
    return out


def cyl_d(f):
    return 2 * f._geomAdaptor().Cylinder().Radius()


def cyl_axis(f):
    d = f._geomAdaptor().Cylinder().Axis().Direction()
    return (d.X(), d.Y(), d.Z())


def of_solid(info, sol, prefix):
    ks = {k for k, (n, s) in enumerate(sol) if n.startswith(prefix)}
    return lambda f: f["solid"] in ks


def area(info, idx):
    return sum(info[i]["area"] for i in idx)


# ------------------------------------------------------------------------------------------------ cases
def case_nodo(sol, faces, info):
    import params as P
    seat_d = 2 * (P.RING_SECTION / 2 + 0.3)                            # 17.1
    seats = [i for i, f in enumerate(info) if of_solid(info, sol, "M3s")(f) and f["type"] == "CYLINDER"
             and abs(cyl_d(faces[i]) - seat_d) < 0.05]
    # ballast: 990 g resting on the two pocket lids (inner face, +Z, z = -30)
    lids = [i for i, f in enumerate(info) if of_solid(info, sol, "M3t")(f) and R.planar(f, nz=1) and f["area"] > 1000]
    # 150 N on one capsule: the front (bezel M6 + window seat) of the +X capsule, straight down
    bezel = [i for i, f in enumerate(info) if of_solid(info, sol, "M6_capsula_bisel_der")(f)]
    # current 1.5 m/s along -X (as in the old FEM): pressure on the faces that face +X and see free water
    wet = exterior_faces(sol, faces, info, (1.0, 0.0, 0.0))
    q = 0.5 * 1025.0 * 1.5 ** 2
    ball_kg = 0.990
    loads = [dict(kind="mass", label=f"lastre {ball_kg * 1000:.0f} g como masa puntual, mitad en cada tapa de bolsillo", idx=lids, mass_kg=ball_kg),
             dict(kind="force", label="150 N hacia abajo sobre el frente (bisel) de la capsula +X", idx=bezel, force_N=(0.0, 0.0, -150.0)),
             dict(kind="pressure", label=f"corriente 1,5 m/s: {q:.0f} Pa sobre las caras mojadas que miran a la corriente (+X)", idx=wet, pressure_pa=q)]
    return dict(name="nodo_estatico", titulo="Nodo sumergido completo: peso + lastre 990 g + 150 N en una capsula + corriente 1,5 m/s",
                fixed=[("asiento Ø17,1 de los 2 ganchos (colgados del aro)", seats)], loads=loads, gravity=True,
                notes=[f"Presion dinamica 0,5·1025·1,5² = {q:.0f} Pa (Cd = 1) sobre {len(wet)} caras, {area(info, wet) / 100:.0f} cm², fuerza ≈ {q * area(info, wet) * 1e-6:.1f} N en -X.",
                       "El asiento del gancho se fija entero (como el FEM viejo y el modelo de Maria): el aro no se modela."])


def case_boya(sol, faces, info):
    import params as P
    bm = P.BUOY_MASS
    eyes = [i for i, f in enumerate(info) if of_solid(info, sol, "B1")(f) and f["type"] == "CYLINDER" and f["bb"][2] < 0.5
            and f["bb"][5] < P.PET_EYE[1] + 0.5 and abs((f["bb"][3] - f["bb"][0]) - P.PET_EYE[2]) < 0.3]
    b3 = of_solid(info, sol, "B3")
    z3 = min(info[i]["bb"][2] for i in range(len(info)) if b3(info[i]))
    floor = [i for i, f in enumerate(info) if b3(f) and R.planar(f, nz=1) and abs(f["bb"][2] - (z3 + 2.4)) < 0.05 and f["area"] > 3000]
    b2 = of_solid(info, sol, "B2")
    dia = lambda f: f["bb"][3] - f["bb"][0]          # noqa: E731
    zb = min(info[i]["bb"][2] for i in range(len(info)) if b2(info[i]))
    bar_top = zb + P.PET_COVER_T
    pil_top = zb + max(P.PET_COVER_T, P.PET_XBAR[1]) + P.PET_PILLAR[1]
    col_tops = [i for i, f in enumerate(info) if b2(f) and R.planar(f, nz=1) and abs(dia(f) - P.PET_COLUMN_D) < 0.3 and f["bb"][5] > bar_top + 30]
    mast = [i for i, f in enumerate(info) if b2(f) and R.planar(f, nz=1) and abs(dia(f) - P.PET_MAST[0]) < 0.3 and f["bb"][5] > bar_top + 100]
    bars = [i for i, f in enumerate(info) if b2(f) and R.planar(f, nz=1) and bar_top - 0.05 < f["bb"][5] < pil_top + 0.05 and f["area"] > 300
            and abs(dia(f) - P.PET_PILLAR[0]) > 0.3]
    elec_g = P.BUOY_CELLS * bm["celda_18650"] + bm["portabaterias"] + bm["pcb_heltec"] + bm["waveshare"] + bm["rtc"] + bm["cables_fusible"] \
        + bm["prensaestopas"] * 1.5 + bm["tornilleria"]
    # bottle seats: faces of the printed parts that touch a bottle (the bottles push the buoy against the line)
    allsol = [(n, cq.Solid(s)) for n, v, s in V.named_solids(V.LIMPIO / f"{MODULES['boya']['asm']}.step") if n.lower().startswith("ref_botella")]
    seats = []
    for i, f in enumerate(info):
        for n, s in allsol:
            b = s.BoundingBox()
            if _bb_gap(f["bb"], (b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax)) > 1.0:
                continue
            dd = BRepExtrema_DistShapeShape(faces[i].wrapped, s.wrapped)
            if dd.IsDone() and dd.Value() <= 1.0:
                seats.append(i)
                break
    c45 = 300.0 * math.sqrt(0.5)
    loads = [dict(kind="mass", label=f"electronica {elec_g:.0f} g como masa puntual sobre el piso de B3", idx=floor, mass_kg=elec_g * 1e-3),
             dict(kind="mass", label=f"panel solar {bm['panel']} g como masa puntual sobre las 4 columnas", idx=col_tops, mass_kg=bm["panel"] * 1e-3),
             dict(kind="mass", label=f"antena {bm['antena']} g sobre el mastil", idx=mast, mass_kg=bm["antena"] * 1e-3),
             dict(kind="force", label="ola 200 N vertical sobre la cara de arriba de las barras de la cubierta", idx=bars, force_N=(0.0, 0.0, -200.0)),
             dict(kind="force", label="golpe lateral 200 N (+Y) sobre el panel, por sus 4 columnas", idx=col_tops, force_N=(0.0, 200.0, 0.0)),
             dict(kind="force", label="tiro del cabo 300 N a 45°: las botellas empujan la boya contra el amarre (reaccion en los ojales)", idx=seats,
                  force_N=(-c45, 0.0, c45))]
    if not mast:
        loads = [ld for ld in loads if ld["idx"]]
    return dict(name="boya_estatico", titulo="Boya completa: peso + panel + electronica, ola 200 N, golpe lateral 200 N, cabo 300 N; apoyo en el amarre",
                fixed=[("agujeros de los ojales de amarre de las 2 mitades de B1 (pata de gallo)", eyes)], loads=loads, gravity=True,
                notes=["Supuesto del apoyo: la boya queda fija en el amarre y el cabo de 300 N a 45° es la reaccion. La fuerza que lo equilibra entra por "
                       f"donde las botellas apoyan en el casco y las cunas ({len(seats)} caras): empuje y arrastre de las botellas.",
                       "Las 4 cargas actuan juntas (caso envolvente, exagerado)."])


def case_tierra(sol, faces, info):
    t1 = of_solid(info, sol, "T1")
    t2 = of_solid(info, sol, "T2")
    lid_y = max(abs(info[i]["bb"][1]) for i in range(len(info)) if t2(info[i])) + 0.05
    # the bottom of T1 is ONE face with the tabs (fixing it would fix the whole box): the support is the wall of the screw slots
    in_tab = lambda f: (f["bb"][1] > lid_y or f["bb"][4] < -lid_y) and f["bb"][5] < 8.0 and max(abs(f["bb"][1]), abs(f["bb"][4])) < 58.0   # noqa: E731
    tabs = [i for i, f in enumerate(info) if t1(f) and in_tab(f) and (f["type"] == "CYLINDER" or (f["n"] is not None and abs(f["n"][2]) < 1e-3))]
    top = [i for i, f in enumerate(info) if t2(f) and R.planar(f, nz=1) and f["area"] > 1000]
    sma = [i for i, f in enumerate(info) if t1(f) and f["type"] == "CYLINDER" and 6.0 < cyl_d(faces[i]) < 7.0
           and abs(cyl_axis(faces[i])[2]) < 0.1]
    ax = cyl_axis(faces[sma[0]]) if sma else (1, 0, 0)
    lat = (-ax[1], ax[0], 0.0)                                                     # horizontal, perpendicular to the SMA axis
    return dict(name="tierra_estatico", titulo="Estacion de tierra T1 + T2 (PLA): 50 N sobre la tapa, 30 N lateral en la antena; fija en las pestañas",
                fixed=[("paredes de las ranuras de tornillo de las pestañas de T1", tabs)],
                loads=[dict(kind="force", label="50 N sobre la tapa T2", idx=top, force_N=(0.0, 0.0, -50.0)),
                       dict(kind="force", label="30 N lateral sobre el agujero del conector SMA (palanca de la antena)", idx=sma,
                            force_N=tuple(30.0 * c for c in lat))],
                gravity=True, notes=["PLA: E 3,5 GPa, ν 0,36, ρ 1240 kg/m³, σ admisible 40 MPa."])


CASES = {"nodo": case_nodo, "boya": case_boya, "tierra": case_tierra}


# ------------------------------------------------------------------------------------------------ STEP with named faces and bodies
def name_step(sol, faces, out):
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
    k = 0
    for n, s in sol:
        lab = st.AddShape(s.wrapped, False)
        TDataStd_Name.Set_s(lab, TCollection_ExtendedString(n))
        for f in s.Faces():
            sl = st.AddSubShape(lab, f.wrapped)
            if sl.IsNull():
                raise RuntimeError(f"face {k} of {n} could not be named")
            TDataStd_Name.Set_s(sl, TCollection_ExtendedString(f"LGF{k:05d}"))
            k += 1
    assert k == len(faces)
    w = STEPCAFControl_Writer()
    Interface_Static.SetIVal_s("write.stepcaf.subshapes.name", 1)
    w.SetNameMode(True)
    w.Transfer(doc, STEPControl_AsIs)
    out.parent.mkdir(parents=True, exist_ok=True)
    w.Write(str(out))


def face_entities(api, pid, gid, n_faces):
    res = {}
    for e in R.mappings(api, pid, gid, "face"):
        for o in e.originate_from:
            for a in o.attribute_list or []:
                if a.attribute == "SDL/TYSA_UNAME" and str(a.value).startswith("LGF"):
                    res.setdefault(int(a.value[3:]), []).append(e.name)
    missing = [i for i in range(n_faces) if i not in res]
    if missing:
        raise RuntimeError(f"{len(missing)} faces lost their name in the import (e.g. {missing[:5]})")
    return res


def region_names(api, pid, gid):
    """[(entity, body name)] of the solids (class region)."""
    out = []
    for e in R.mappings(api, pid, gid, "region"):
        nm = None
        for o in e.originate_from:
            nm = nm or getattr(o, "body", None)
            for a in o.attribute_list or []:
                if a.attribute in ("SDL/TYSA_NAME", "SDL/TYSA_UNAME") and not str(a.value).startswith("LGF"):
                    nm = nm or str(a.value)
        out.append((e.name, nm))
    return out


# ------------------------------------------------------------------------------------------------ spec
def make_spec_builder(mod, case, pairs, mat, only_disp=False):
    """Returns build_spec(case, ent, bodies) for simscale_run.run_simscale: the single-piece spec plus contacts, masses, pressures."""
    import simscale_sdk as sim
    m = MATS[mat]

    def build(case_, ent, bodies):
        R.E_PA, R.NU, R.RHO = m["E"], m["nu"], m["rho"]
        base_loads = [ld for ld in case_["loads"] if ld["kind"] in ("force", "remote")]
        spec = BASE_SPEC(dict(case_, loads=base_loads), ent, bodies)
        spec.materials[0].name = mat
        ref = lambda idx: sim.TopologicalReference(entities=sorted({e for i in idx for e in ent[i]}), sets=[])  # noqa: E731
        const = lambda v: sim.ConstantFunction(type="CONSTANT", value=v)   # noqa: E731
        for n, ld in enumerate(case_["loads"]):
            if ld["kind"] == "mass":
                spec.boundary_conditions.append(sim.PointMassBC(
                    type="POINT_MASS", name=f"Point mass {n + 1}", mass=sim.DimensionalMass(value=ld["mass_kg"], unit="kg"),
                    external_point=sim.DimensionalVectorLength(value=sim.DecimalVector(*[c * 1e-3 for c in centroid(case_, ld)]), unit="m"),
                    deformation_behavior="DEFORMABLE", enable_search_radius=False, topological_reference=ref(ld["idx"])))
            elif ld["kind"] == "pressure":
                spec.boundary_conditions.append(sim.PressureBC(
                    type="PRESSURE", name=f"Pressure {n + 1}", pressure=sim.DimensionalFunctionPressure(value=const(ld["pressure_pa"]), unit="Pa"),
                    topological_reference=ref(ld["idx"])))
        conns = []
        for (a, b), (fa, fb) in sorted(pairs.items()):
            conns.append(sim.BondedContact(type="BONDED_CONTACT", name=f"Bonded {a}-{b}", enable_heat_transfer=None,
                                           position_tolerance=sim.SetValuePositionTolerance(type="SET_VALUE", tolerance=sim.DimensionalLength(value=PROJ_TOL * 1e-3, unit="m")),
                                           master_topological_reference=ref(fa), slave_topological_reference=ref(fb)))
        spec.connection_groups = [sim.Contact(type="CONTACT", node_merging_bonded=True, connections=conns)]
        if only_disp:      # the public viewer publishes one field per run: this run keeps only the displacement
            spec.result_control.solution_fields = [f for f in spec.result_control.solution_fields if f.type == "DISPLACEMENT"]
        return spec
    return build


_CENTROIDS = {}


def centroid(case, ld):
    return _CENTROIDS[ld["label"]]


# ------------------------------------------------------------------------------------------------ main
def prepare(mod, mixto=False):
    """mixto: full (0.35 mm) bonded contacts everywhere, strict face-to-face only between B2 and B3, the pair SimScale could not project
    (the all-strict boya kept only ~311 mm2 of each cradle on the hull and peaked at a contact singularity: docs/DECISIONES.md)."""
    sol, faces, info = load_module(mod)
    t0 = time.time()
    if mixto:
        pairs = contacts(sol, faces, info, strict=False)
        st = contacts(sol, faces, info, strict=True)
        for (a, b) in list(pairs):
            na, nb = sol[a][0][:2], sol[b][0][:2]
            if {na, nb} == {"B2", "B3"}:
                pairs[(a, b)] = st[(a, b)]
    else:
        pairs = contacts(sol, faces, info, strict=MODULES[mod].get("strict", False))
    comps = components(len(sol), list(pairs))
    case = CASES[mod](sol, faces, info)
    for ld in case["loads"]:
        if ld["kind"] == "mass":
            a = area(info, ld["idx"])
            c = [sum(faces[i].Center().toTuple()[k] * info[i]["area"] for i in ld["idx"]) / a for k in range(3)]
            _CENTROIDS[ld["label"]] = c
    print(f"{mod}: {len(sol)} solids, {len(faces)} faces, {len(pairs)} bonded pairs ({time.time() - t0:.0f} s), {len(comps)} connected group(s)")
    for g in comps:
        print("   group:", [sol[k][0] for k in g])
    for lab, idx in case["fixed"]:
        print(f"   FIXED {lab}: {len(idx)} faces, {area(info, idx):.0f} mm2, solids {sorted({sol[info[i]['solid']][0] for i in idx})}")
    for ld in case["loads"]:
        print(f"   {ld['kind'].upper():8s} {ld['label']}: {len(ld['idx'])} faces, {area(info, ld['idx']):.0f} mm2, solids {sorted({sol[info[i]['solid']][0] for i in ld['idx']})}")
    return sol, faces, info, pairs, comps, case


def render_bc(mod, path):
    """Local render (pyvista, 1920 x 1080, ISO) of the supports and loads picked for the SimScale run of the module."""
    sol, faces, info, pairs, comps, case = prepare(mod)
    show = dict(case, loads=[])
    for ld in case["loads"]:
        d = dict(ld)
        if ld["kind"] == "mass":
            d["force_N"] = (0.0, 0.0, -ld["mass_kg"] * G)
            d["label"] = ld["label"]
        elif ld["kind"] == "pressure":
            d["force_N"] = (-ld["pressure_pa"] * area(info, ld["idx"]) * 1e-6, 0.0, 0.0)
        show["loads"].append(d)
    import pyvista as pv
    orig = pv.Plotter.__init__

    def big(self, *a, **k):
        k["window_size"] = (1920, 1080)
        orig(self, *a, **k)
    pv.Plotter.__init__ = big
    try:
        R.render_bc(faces, show, path, MODULES[mod]["project"])
    finally:
        pv.Plotter.__init__ = orig


def get_project(api, mod):
    import simscale_sdk as sim
    name = MODULES[mod]["project"]
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
    return P.create_project(sim.Project(name=name, description=MODULES[mod]["desc"], measurement_system="SI")).project_id


def run(mod, fineness, rehacer, only_disp=False, mixto=False):
    sol, faces, info, pairs, comps, case = prepare(mod, mixto)
    if mixto:
        case = dict(case, name=case["name"] + "_mixto")
    base_key = f"modulo_{mod}/{case['name']}"
    if only_disp:
        case = dict(case, name=case["name"] + "_desplazamiento")
    if len(comps) != 1:
        raise SystemExit(f"{mod}: the bonded graph has {len(comps)} groups, a free body would make the solve singular")
    for lab, idx in case["fixed"]:
        if not idx:
            raise SystemExit(f"empty support {lab}")
    for ld in case["loads"]:
        if not ld["idx"]:
            raise SystemExit(f"empty load {ld['label']}")
    named = OUT / "_named" / f"{mod}.step"
    name_step(sol, faces, named)
    api = R.client()
    pid = get_project(api, mod)
    print("   project", pid)
    gid, gname = R.import_geometry(api, pid, f"modulo_{mod}", named, V.LIMPIO / f"{MODULES[mod]['asm']}.step")
    ent = face_entities(api, pid, gid, len(faces))
    regs = region_names(api, pid, gid)
    print(f"   geometry {gname}: {len(ent)} faces mapped, {len(regs)} regions")
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    R.STATE_FILE = STATE
    R.build_spec = make_spec_builder(mod, case, pairs, MODULES[mod]["mat"], only_disp)
    if only_disp:      # same geometry and mesh as the von Mises run
        B = state.get(base_key, {})
        if B.get("gid") != gid or not B.get("mesh_id"):
            raise SystemExit(f"run the von Mises case of {mod} first")
        D = state.setdefault(f"modulo_{mod}/{case['name']}", {})
        if rehacer or D.get("gid") != gid:
            D.clear()
        D.update(gid=gid, mesh_op=B["mesh_op"], mesh_id=B["mesh_id"], mesh_estimate=B.get("mesh_estimate"))
        rehacer = False
    S = R.run_simscale(f"modulo_{mod}", case, ent, gid, pid, api, fineness, state, rehacer)
    S["pid"] = pid
    S["regions"] = regs
    S["case"] = dict(titulo=case["titulo"], fixed=[(lab, len(idx)) for lab, idx in case["fixed"]],
                     loads=[dict(kind=ld["kind"], label=ld["label"], faces=len(ld["idx"])) for ld in case["loads"]], notes=case["notes"])
    R.save_state(state)
    print("   done", S.get("duration"), S.get("compute"))
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modulo", choices=list(MODULES))
    ap.add_argument("--listar", choices=list(MODULES))
    ap.add_argument("--bc", choices=list(MODULES), help="local render of supports and loads")
    ap.add_argument("--fineness", type=float, default=4)
    ap.add_argument("--rehacer", action="store_true")
    ap.add_argument("--desplazamiento", action="store_true", help="second run, same mesh, only the displacement field")
    ap.add_argument("--mixto", action="store_true", help="full contacts, strict only B2-B3 (new case name, keeps the earlier run)")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.bc:
        d = OUT / "capturas" / a.bc
        d.mkdir(parents=True, exist_ok=True)
        render_bc(a.bc, d / "condiciones_borde_local.png")
    elif a.listar:
        prepare(a.listar)
    elif a.modulo:
        run(a.modulo, a.fineness, a.rehacer, a.desplazamiento, a.mixto)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
