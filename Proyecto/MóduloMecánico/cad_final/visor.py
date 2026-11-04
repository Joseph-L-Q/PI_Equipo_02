"""Interactive 3D viewer of LanternGuard (node + buoy).

Run from cad_final:  ..\\.venv\\Scripts\\python.exe visor.py
Writes  docs/visor/lanternguard.glb  and  docs/visor/index.html  (the GLB is embedded in the page as base64,
the guide data as JSON, so the page opens offline from disk or Drive; only three.js comes from cdnjs).

Everything is read at run time (STEP assemblies, slicer.json, rasgos.json, GUIA_PIEZAS.md, ESTANQUEIDAD.md), so
a re-run picks up a regenerated node or an updated seal list.
"""
import base64
import json
import math
import re
import sys
import time
from pathlib import Path

import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
OUT = MOD / "docs" / "visor"
NODE_STEP = MOD / "salida" / "prototipos" / "P2_robusto" / "ensamble_simple_D200.step"
BUOY_STEP = MOD / "salida" / "boya_pet" / "ENSAMBLE_boya_pet.step"
NODE_SLICER = MOD / "salida" / "prototipos" / "P2_robusto" / "slicer.json"
BUOY_SLICER = MOD / "salida" / "boya_pet" / "slicer.json"
RASGOS = MOD / "salida" / "guia_piezas" / "rasgos.json"
SELLOS_JSON = MOD / "salida" / "guia_piezas" / "sellos.json"
GUIA_MD = MOD / "docs" / "GUIA_PIEZAS.md"
ESTANQ_MD = MOD / "docs" / "ESTANQUEIDAD.md"
TEMPLATE = HERE / "visor_template.html"

BUOY_SHIFT = (620.0, 0.0, 300.0)        # mm, buoy origin in the node frame (beside the node, not at true distance)
DROP = {"REF_boya", "REF_umbilical"}     # node placeholders replaced by the real buoy and a drawn umbilical
TRI_BUDGET_PRINTED = 30000
TRI_BUDGET_REF = 6000


# ----------------------------------------------------------------------------- STEP reading (named bodies)
def read_named_step(path):
    """Return [(name, cq.Shape)] with the assembly placement applied."""
    import cadquery as cq
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.STEPCAFControl import STEPCAFControl_Reader
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.TDF import TDF_Label, TDF_LabelSequence
    from OCP.TDataStd import TDataStd_Name
    from OCP.TDocStd import TDocStd_Document
    from OCP.XCAFDoc import XCAFDoc_DocumentTool

    doc = TDocStd_Document(TCollection_ExtendedString("x"))
    rd = STEPCAFControl_Reader()
    rd.SetNameMode(True)
    if rd.ReadFile(str(path)) != IFSelect_RetDone:
        raise RuntimeError(f"cannot read {path}")
    rd.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())

    def name_of(lab):
        a = TDataStd_Name()
        return a.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), a) else ""

    out = []

    def walk(lab):
        if st.IsAssembly_s(lab):
            comps = TDF_LabelSequence()
            st.GetComponents_s(lab, comps)
            for i in range(1, comps.Length() + 1):
                c = comps.Value(i)
                ref = TDF_Label()
                nm = name_of(c)
                if st.GetReferredShape_s(c, ref):
                    nm = nm or name_of(ref)
                    if st.IsAssembly_s(ref):
                        walk(ref)
                    else:
                        out.append((nm, cq.Shape.cast(st.GetShape_s(c))))
        else:
            out.append((name_of(lab), cq.Shape.cast(st.GetShape_s(lab))))

    free = TDF_LabelSequence()
    st.GetFreeShapes(free)
    for i in range(1, free.Length() + 1):
        walk(free.Value(i))
    return out


def tessellate(shape, budget):
    """Triangle mesh in mm; tolerance grows until the triangle budget is met."""
    bb = shape.BoundingBox()
    diag = math.sqrt(bb.xlen ** 2 + bb.ylen ** 2 + bb.zlen ** 2)
    tol = max(0.15, diag * 0.0008)
    for _ in range(8):
        v, f = shape.tessellate(tol, 0.4)
        if len(f) <= budget:
            break
        tol *= 1.6
    m = trimesh.Trimesh(np.array([[p.x, p.y, p.z] for p in v]), np.array(f), process=False)
    m.merge_vertices()
    m.update_faces(m.nondegenerate_faces())
    return m


def umbilical_mesh(p0, p1):
    """Orange cable drawn from the node lid up and across to the buoy box (decoration, not a printed part)."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    mid = (p0 + p1) / 2
    ctrl = [p0, p0 + [0, 0, 70], p0 + [40, 0, 140], mid + [0, 0, 130], p1 + [-150, 0, 80], p1 + [-40, 0, 10], p1]
    pts = []
    for t in np.linspace(0, 1, 40):                       # Bezier of degree 6
        n = len(ctrl) - 1
        pts.append(sum(math.comb(n, i) * (1 - t) ** (n - i) * t ** i * c for i, c in enumerate(ctrl)))
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        d = b - a
        L = float(np.linalg.norm(d))
        if L < 1e-6:
            continue
        cyl = trimesh.creation.cylinder(radius=3.0, height=L, sections=8)
        z = np.array([0, 0, 1.0])
        axis = np.cross(z, d / L)
        ang = math.acos(max(-1, min(1, float(z @ (d / L)))))
        T = trimesh.transformations.rotation_matrix(ang, axis) if np.linalg.norm(axis) > 1e-9 else np.eye(4)
        T[:3, 3] = (a + b) / 2
        cyl.apply_transform(T)
        segs.append(cyl)
    return trimesh.util.concatenate(segs)


def zup_to_gltf(m):
    """mm Z-up -> metres Y-up (x, z, -y)."""
    v = m.vertices
    m.vertices = np.column_stack([v[:, 0], v[:, 2], -v[:, 1]]) * 0.001
    m.fix_normals()
    return m


# ----------------------------------------------------------------------------- text sources
def read_json(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def parse_guia(md):
    """{key: {titulo, funcion, items}} using the image alt text ![key](...) of each section."""
    out = {}
    if not md.exists():
        return out
    txt = md.read_text(encoding="utf-8")
    for sec in re.split(r"\n(?=## )", txt):
        m = re.match(r"## (.+)", sec)
        im = re.search(r"!\[([^\]]+)\]", sec)
        if not (m and im):
            continue
        body = sec[m.end():]
        pre = body.split("![")[0].strip()
        items = re.findall(r"^\d+\. \*\*(.+?)\*\*(.*)$", body, re.M)
        titulo = m.group(1).split("·", 1)[-1].strip()
        out[im.group(1)] = dict(titulo=titulo, funcion=pre, items=items)
    return out


def parse_estanq(md, sellos_json):
    """Seal table + 'no estanco' + pending bullets, read from ESTANQUEIDAD.md (falls back to sellos.json)."""
    seals, no_est, pend = [], [], []
    if md.exists():
        txt = md.read_text(encoding="utf-8")
        for ln in txt.splitlines():
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(c) >= 5 and c[0].isdigit():
                seals.append(dict(n=int(c[0]), sello=c[1], piezas=c[2], tipo=c[3], protege=c[4], donde=c[5] if len(c) > 5 else ""))
        sec = None
        for ln in txt.splitlines():
            if ln.startswith("## "):
                sec = "no" if "NO es estanco" in ln else "pend" if ln.lower().startswith("## pendiente") else None
            elif ln.startswith("- ") and sec:
                (no_est if sec == "no" else pend).append(re.sub(r"[`*]", "", ln[2:]).strip())
    if not seals:
        for s in sellos_json or []:
            seals.append(dict(n=s["n"], sello=s["sello"], piezas=", ".join(s["piezas"]), tipo=s["tipo"], protege=s["protege"], donde="; ".join(s["donde"])))
    return seals, no_est, pend


# ----------------------------------------------------------------------------- name resolution
def base_key(name):
    """Instance name -> guide / slicer key (drops side and half suffixes)."""
    n = re.sub(r"_(izq|der)$", "", name)
    n = re.sub(r"_mitad_\d+$", "", n)
    n = re.sub(r"^(B5_cuna)_[DI]_(base|cuello)$", r"\1_\2", n)
    n = re.sub(r"^(B6_correa)_[DI]\d+$", r"\1", n)
    return n


def lookup(d, key):
    if key in d:
        return key
    cands = [k for k in d if key.startswith(k) or k.startswith(key)]
    return max(cands, key=len) if cands else None


def side_of(name):
    if name.endswith("_izq") or re.search(r"_I(_|\d|$)", name):
        return "lado izquierdo"
    if name.endswith("_der") or re.search(r"_D(_|\d|$)", name):
        return "lado derecho"
    m = re.search(r"_mitad_(\d)$", name)
    return f"mitad {m.group(1)}" if m else ""


REF_ES = {
    "REF_M7_capsula_ventana": "Ventana de acrílico de la cápsula (comprada)", "REF_aro_superior": "Aro superior de la linterna (referencia)",
    "REF_linterna_malla": "Malla de la linterna (referencia)", "REF_linterna_piso": "Piso de la linterna (referencia)",
    "REF_cuerda": "Cuerda de la linterna (referencia)", "REF_cabo": "Cabo de amarre (referencia)",
    "REF_estructura_punto_fijo": "Estructura del punto fijo (referencia)", "REF_umbilical": "Cable umbilical (dibujo)",
    "lastre_": "Lastre: tuercas y arandelas M8 a granel",
    "ref_batt": "Portabaterías con 3 celdas 18650 (referencia)", "ref_pcb": "Placa electrónica (referencia)",
    "ref_ws": "Módulo Waveshare (referencia)", "ref_rtc": "Reloj RTC (referencia)", "ref_panel": "Panel solar 170 × 170 (referencia)",
    "ref_botella": "Botella PET de flotación (referencia)",
}

JOINS = {
    "M1s_caja_cuerpo": "Tapa M2 (12 M3 y cordón O-ring), un riel M3s por lado, tapas de lastre M3t, bandejas M11.",
    "M2_caja_tapa": "Caja M1s (12 M3 con cordón O-ring); el cabo de la linterna se amarra en su ojo.",
    "M3s_riel_gancho": "Caja M1s (brida con 4 M4), cápsula M4/M5s (2 M4 a la silla) y el aro de la linterna (gancho en C).",
    "M3t_tapa_bolsillo": "Caja M1s, por abajo (2 M3 avellanados a los insertos del bolsillo).",
    "M4_capsula_cuerpo": "Tapa con pie M5s (cordón O-ring), bisel M6 con 3 M2 y ventana de acrílico.",
    "M5s_capsula_tapa_pie": "Cápsula M4 (tornillos y cordón O-ring) y riel M3s (2 M4 por la silla).",
    "M6_capsula_bisel": "Cápsula M4 (3 M2): sujeta la ventana de acrílico.",
    "M11_bandeja": "Bosses de la caja M1s (4 M3); la bandeja superior se apila encima.",
    "M11_bandeja_sup": "Bandeja inferior M11.",
    "B1_casco": "La otra mitad del casco (6 M3 y pin), cubierta B2 (4 M3 por mitad) y cunas B5 (4 M3).",
    "B2_cubierta_lisa": "Postes del casco B1 (4 M3), caja B3 (orejas, 2 M3) y panel solar (2 columnas).",
    "B2_cubierta_mastil": "Postes del casco B1 (4 M3), caja B3 (orejas, 2 M3), panel solar y antena en el mástil.",
    "B3_caja": "Cubierta B2 (2 orejas con M3) y tapa B4 (cordón O-ring con tornillos M3 a insertos).",
    "B4_tapa": "Caja seca B3 (cordón O-ring y tornillos M3).",
    "B5_cuna_base": "Casco B1 (M3 a las lengüetas) y la botella PET por el lado de la base.",
    "B5_cuna_cuello": "Casco B1 (M3 a las lengüetas) y la botella PET por el lado del cuello.",
    "B6_correa": "Casco B1 y botella: la correa abraza la botella desde arriba.",
}


def material_of(name, kind):
    if kind == "impresa":
        return "PETG (impresa 3D, Bambu P1P)"
    if name.startswith("lastre"):
        return "Acero: tuercas y arandelas M8 a granel"
    if "ventana" in name:
        return "Acrílico (comprado)"
    if name.startswith("ref_botella"):
        return "PET (botella comprada)"
    return "No se imprime: pieza comprada o dibujo de referencia"


# ----------------------------------------------------------------------------- explosion offsets and steps
def sgn(v):
    return 1.0 if v >= 0 else -1.0


def offset_for(name, c, group, gc):
    """Explosion vector (mm, Z-up) from the piece centre c (world, mm)."""
    x, y, z = c
    if group == "nodo":
        s = sgn(x)
        if name.startswith("M2_"):
            return (0, 0, 170)
        if name.startswith("M11_bandeja_sup"):
            return (0, 0, 100)
        if name.startswith("M11_bandeja"):
            return (0, 0, 55)
        if name.startswith("M3t"):
            return (0, 0, -120)
        if name.startswith("lastre"):
            return (0, 0, -70)
        if name.startswith("M3s"):
            return (s * 90, 0, 0)
        if name.startswith("M5s"):
            return (s * 150, 0, -35)
        if name.startswith("M4_"):
            return (s * 90, 0, -90)
        if name.startswith("M6_"):
            return (s * 40, 0, -90)
        if "M7" in name:
            return (s * 55, 0, -90)
        return (0, 0, 0)
    ox, oy, oz = gc
    cx, cy, cz = x - ox, y - oy, z - oz
    n = name
    if n.startswith("B1_"):
        return (sgn(cx) * 80, 0, -50)
    if n.startswith("B2_"):
        return (sgn(cx) * 80, 0, 110)
    if n.startswith("B3_"):
        return (0, 0, 200)
    if n.startswith("B4_"):
        return (0, 0, 290)
    if n.startswith("B5_"):
        return (0, sgn(cy) * 120, -60)
    if n.startswith("B6_"):
        return (0, sgn(cy) * 40, 70)
    if n in ("ref_batt", "ref_pcb", "ref_ws", "ref_rtc"):
        return (0, 0, 245)
    if n == "ref_panel":
        return (0, 0, 380)
    if n.startswith("ref_botella"):
        return (0, sgn(cy) * 70, 20)
    v = np.array([cx, cy, cz], float)
    nv = np.linalg.norm(v)
    return tuple((v / nv * 100) if nv > 1 else (0, 0, 100))


STEPS = [
    ("nodo", "Caja del nodo", "Empieza por la caja seca M1s: es el cuerpo del nodo y todo lo demás se atornilla a ella.", [r"^M1s"]),
    ("nodo", "Lastre en los bolsillos", "Mete las tuercas y arandelas M8 en los dos bolsillos de abajo y ciérralos con las tapas M3t (2 tornillos cada una). Entra agua: es normal.", [r"^lastre", r"^M3t"]),
    ("nodo", "Bandejas de la electrónica", "Atornilla la bandeja inferior y la superior a los 4 postes del piso de la caja (zona seca).", [r"^M11"]),
    ("nodo", "Tapa con asa", "Pon el cordón de goma Ø2 en la ranura de la tapa M2 y apriétala con 12 tornillos M3. El umbilical sale por su prensaestopas.", [r"^M2_"]),
    ("nodo", "Rieles con gancho", "Cada riel M3s se atornilla a un costado de la caja con 4 tornillos M4. El gancho en C cuelga del aro de la linterna.", [r"^M3s"]),
    ("nodo", "Cápsulas de cámara", "En la punta de cada riel va la cápsula: cuerpo M4, tapa con pie M5s, bisel M6 y ventana de acrílico.", [r"^M4_", r"^M5s", r"^M6_", r"^REF_M7"]),
    ("nodo", "Linterna, aro y cuerdas", "Piezas de referencia: el aro, la malla, los pisos y las cuerdas donde cuelga el nodo.", [r"^REF_aro", r"^REF_linterna", r"^REF_cuerda", r"^REF_cabo", r"^REF_estructura"]),
    ("boya", "Casco de la boya", "Une las dos mitades del casco B1 (6 tornillos M3 y un pin de alineación).", [r"^B1_"]),
    ("boya", "Cunas y botellas", "Atornilla las cunas B5 al casco y apoya las cuatro botellas PET selladas: son las que hacen flotar la boya.", [r"^B5_", r"^ref_botella"]),
    ("boya", "Correas", "Las correas B6 abrazan las botellas desde arriba para que no se salgan.", [r"^B6_"]),
    ("boya", "Cubierta", "Las dos mitades de la cubierta B2 se atornillan a los postes del casco (4 M3 cada una).", [r"^B2_"]),
    ("boya", "Caja seca y electrónica", "Dentro de la caja B3 van las baterías, la placa, el módulo Waveshare y el reloj. Se fija a la cubierta por sus orejas.", [r"^B3_", r"^ref_batt", r"^ref_pcb", r"^ref_ws", r"^ref_rtc"]),
    ("boya", "Tapa de la caja seca", "Cordón O-ring Ø2 en la ranura y tornillos M3 a los insertos de la brida de B3.", [r"^B4_"]),
    ("boya", "Panel solar", "El panel de 170 × 170 se atornilla a las cuatro columnas de la cubierta.", [r"^ref_panel"]),
    ("nodo", "Cable umbilical", "Une la tapa del nodo con la caja seca de la boya. Va flojo, con curva, para que el oleaje no lo tense.", [r"^REF_umbilical"]),
]


def seal_parts(seal, names):
    """Part instance names touched by a seal row (tokens B3, M1s, 'B5 base', 'B2 mástil'...)."""
    hit = set()
    toks = [t.strip() for t in re.split(r"[,;]", seal["piezas"]) if t.strip()]
    for t in toks:
        code = re.match(r"([BM]\d+[a-z]?)", t)
        if not code:
            continue
        code = code.group(1)
        rest = t[len(code):].strip().lower()
        for n in names:
            if re.match(code + r"(_|$)", n) is None:
                continue
            if rest in ("base", "cuello", "lisa") and rest not in n:
                continue
            if rest in ("mástil", "mastil") and "mastil" not in n:
                continue
            hit.add(n)
    return sorted(hit)


# ----------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    scene = trimesh.Scene()
    parts = {}
    node = read_named_step(NODE_STEP)
    buoy = read_named_step(BUOY_STEP)
    print(f"node: {len(node)} bodies ({NODE_STEP.name}, {time.strftime('%d/%m %H:%M', time.localtime(NODE_STEP.stat().st_mtime))}); buoy: {len(buoy)} bodies", flush=True)

    meshes = {}
    for group, items, shift in (("nodo", node, (0, 0, 0)), ("boya", buoy, BUOY_SHIFT)):
        for nm, sh in items:
            if nm in DROP:
                continue
            printed = bool(re.match(r"^[BM]\d+", nm))
            m = tessellate(sh, TRI_BUDGET_PRINTED if printed else TRI_BUDGET_REF)
            m.apply_translation(shift)
            meshes[nm] = (group, "impresa" if printed else "ref", m)

    # drawn umbilical: node lid top -> buoy box side
    b3 = next((m for n, (g, k, m) in meshes.items() if n.startswith("B3_")), None)
    lid = next((m for n, (g, k, m) in meshes.items() if n.startswith("M2_")), None)
    if b3 is not None and lid is not None:
        top = lid.bounds[1][2]
        bb = b3.bounds
        meshes["REF_umbilical"] = ("nodo", "ref", umbilical_mesh((0, 0, top), (bb[0][0], (bb[0][1] + bb[1][1]) / 2, (bb[0][2] + bb[1][2]) / 2)))

    # buoy group centre (for radial rules)
    bm = [m.bounds for n, (g, k, m) in meshes.items() if g == "boya"]
    gc = tuple((np.min([b[0] for b in bm], 0) + np.max([b[1] for b in bm], 0)) / 2) if bm else (0, 0, 0)

    guia = parse_guia(GUIA_MD)
    rasgos = read_json(RASGOS)
    sl = {**read_json(NODE_SLICER), **read_json(BUOY_SLICER)}
    seals, no_est, pend = parse_estanq(ESTANQ_MD, read_json(SELLOS_JSON))
    names = list(meshes)

    for nm, (group, kind, m) in meshes.items():
        c = (m.bounds[0] + m.bounds[1]) / 2
        off = offset_for(nm, c, group, gc)
        key = base_key(nm)
        gk = lookup(guia, key)
        rk = lookup(rasgos, key)
        sk = lookup(sl, key)
        ref_es = next((v for k, v in REF_ES.items() if nm.startswith(k)), None)
        titulo = (guia[gk]["titulo"] if gk and kind == "impresa" else ref_es) or nm.replace("_", " ")
        side = side_of(nm)
        info = dict(group=group, kind=kind, code=key if kind == "impresa" else nm,
                    titulo=titulo + (f" ({side})" if side else ""),
                    funcion=guia[gk]["funcion"] if gk and kind == "impresa" else (ref_es or "Pieza de referencia."),
                    material=material_of(nm, kind), offset=[off[0], off[2], -off[1]],
                    centro=[float(c[0]), float(c[2]), float(-c[1])])
        if sk and kind == "impresa":
            s = sl[sk]
            info.update(g=round(float(s["g"]), 1), h=round(float(s["h"]), 2), qty=s.get("qty"), relleno=s.get("relleno_pct"),
                        soportes=s.get("soportes"))
        elif nm.startswith("lastre"):
            info.update(g=575.0, h=None)
        j = JOINS.get(key)
        if j:
            info["une"] = j
        rs = rasgos.get(rk, []) if rk and kind == "impresa" else []
        info["rasgos"] = [dict(n=r["n"], tipo=r["tipo"], diam=r.get("diam"), texto=r["texto"], cat=r.get("categoria"), cant=len(r.get("puntos") or [1])) for r in rs]
        info["tornillos"] = [f"{r['tipo']}{' Ø' + str(r['diam']) if r.get('diam') else ''} ×{len(r.get('puntos') or [1])}"
                             for r in rs if r.get("categoria") == "union"]
        if not rs and kind == "impresa":
            info["rasgos_nota"] = "Esta pieza todavía no tiene ficha de agujeros en la guía."
        info["sellos"] = [s["n"] for s in seals if nm in seal_parts(s, names)]
        parts[nm] = info
        scene.add_geometry(zup_to_gltf(m.copy()), node_name=nm, geom_name=nm)

    # steps (regex over instance names); leftovers go to a last step
    steps, used = [], set()
    for grp, tit, txt, pats in STEPS:
        ps = [n for n in names if any(re.search(p, n) for p in pats) and n not in used]
        if ps:
            used.update(ps)
            steps.append(dict(titulo=tit, texto=txt, partes=ps, grupo=grp))
    rest = [n for n in names if n not in used]
    if rest:
        steps.append(dict(titulo="Otras piezas", texto="Piezas nuevas que todavía no tienen paso propio en el visor.", partes=rest, grupo="nodo"))
    for i, s in enumerate(steps):
        for n in s["partes"]:
            parts[n]["paso"] = i

    seal_out = [dict(s, partes=seal_parts(s, names)) for s in seals]

    glb = scene.export(file_type="glb", include_normals=False)
    (OUT / "lanternguard.glb").write_bytes(glb)
    stamp = lambda p: f"{p.name} ({time.strftime('%d/%m %H:%M', time.localtime(p.stat().st_mtime))})"   # noqa: E731
    data = dict(partes=parts, pasos=steps, sellos=seal_out, no_estanco=no_est, pendiente=pend,
                generado=time.strftime("%d/%m/%Y %H:%M"), fuentes=dict(nodo=stamp(NODE_STEP), boya=stamp(BUOY_STEP)))
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    html = html.replace("__GLB_B64__", base64.b64encode(glb).decode("ascii"))
    (OUT / "index.html").write_text(html, encoding="utf-8")
    tri = sum(len(m.faces) for _, _, m in meshes.values())
    print(f"{len(parts)} parts, {tri} triangles, glb {len(glb) / 1e6:.2f} MB, html {(OUT / 'index.html').stat().st_size / 1e6:.2f} MB, "
          f"{len(steps)} steps, {len(seals)} seals, {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
