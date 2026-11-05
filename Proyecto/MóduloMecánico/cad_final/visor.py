r"""Interactive 3D manual of LanternGuard (node + buoy): geometry half.

Regenerate everything with ONE command (from cad_final):

    ..\.venv\Scripts\python.exe visor.py && ..\.venv\Scripts\python.exe visor_datos.py
    (visor.py already calls visor_datos at the end; the second call only matters when the CAD did not change and
     you just want to refresh slicer / FEM / simulation data: it takes ~3 s because it does not read the STEP files)

visor.py  : reads the two STEP assemblies, tessellates the pieces and writes
            docs/visor/modelo.glb       one mesh per piece named with its code (B1_casco_a/_b, M3s_riel_gancho_der, ...),
                                        seals as SELLO_nn meshes (red), bottles / lantern / electronics as REF_* (gray ghosts)
            salida/_tmp/visor_geometria.json   sidecar for visor_datos.py: explosion offsets, bounding boxes, hole positions
                                        of every feature placed in the assembly frame (piece STEP -> assembly by a 48-matrix
                                        best-fit search; pieces that do not fit within 1 mm get no markers)
visor_datos.py : docs/visor/datos.json, index.html and LanternGuard_visor.html (single file, GLB + JSON embedded).
"""
import itertools
import json
import math
import re
import sys
import time
import unicodedata
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
LOCAL_JSON = MOD / "salida" / "nuevas" / "local.json"        # ensamble.niveles: z of the 4 ring centres (read only)
ARO_STEP = MOD / "salida" / "aro" / "step" / "LR2_aro.step"
BENCH_PIECES = [("PB_aro", "linterna", MOD / "salida" / "aro" / "step" / "PB_aro.step", -260.0),
                ("T1_caja", "tierra", MOD / "salida" / "tierra" / "step" / "T1_caja.step", -100.0),
                ("T2_tapa", "tierra", MOD / "salida" / "tierra" / "step" / "T2_tapa.step", 60.0)]   # name, group, STEP, x of the centre (mm)
BENCH_Y, BENCH_Z = -300.0, -244.34                           # mm: beside the node (y < node), resting on its lowest level
NODE_STEPS = MOD / "salida" / "prototipos" / "P2_robusto" / "step"     # one STEP per piece (frame of guia_piezas / rasgos.json)
BUOY_STEPS = MOD / "salida" / "boya_pet" / "step"
SIDECAR = MOD / "salida" / "_tmp" / "visor_geometria.json"
ALIGN_TOL = 1.0                          # mm: mean distance (piece STEP vs assembly body) accepted for placing hole markers

BUOY_SHIFT = (620.0, 0.0, 300.0)        # mm, buoy origin in the node frame (beside the node, not at true distance)
DROP = {"REF_boya", "REF_umbilical", "REF_aro_superior"}     # node placeholders replaced by the real buoy, a drawn umbilical and the real ring LR2_aro_1
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
def ren(nm):
    """STEP body name -> public mesh name: halves _a/_b, every reference body REF_*."""
    nm = re.sub(r"_mitad_1$", "_a", nm)
    nm = re.sub(r"_mitad_2$", "_b", nm)
    if nm.startswith("ref_"):
        nm = "REF_" + nm[4:]
    if nm.startswith("lastre"):
        nm = "REF_" + nm
    return nm


def base_key(name):
    """Instance name -> guide / slicer key (drops side and half suffixes)."""
    n = re.sub(r"_(izq|der)$", "", name)
    n = re.sub(r"^(B1_casco)_[ab]$", r"\1", n)
    n = re.sub(r"^(B5_cuna)_[DI]_(base|cuello)$", r"\1_\2", n)
    n = re.sub(r"^(B6_correa)_[DI]\d+$", r"\1", n)
    n = re.sub(r"^(LR2_aro)_\d+$", r"\1", n)
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
    m = re.search(r"^B1_casco_([ab])$", name)
    return f"mitad {m.group(1).upper()}" if m else ""


REF_ES = {
    "REF_M7_capsula_ventana": "Ventana de acrílico de la cápsula (comprada)", "REF_aro_superior": "Aro superior de la linterna (referencia)",
    "REF_linterna_malla": "Malla de la linterna (referencia)", "REF_linterna_piso": "Piso de la linterna (referencia)",
    "REF_cuerda": "Cuerda de la linterna (referencia)", "REF_cabo": "Cabo de amarre (referencia)",
    "REF_estructura_punto_fijo": "Estructura del punto fijo (referencia)", "REF_umbilical": "Cable umbilical (dibujo)",
    "REF_lastre": "Lastre: tuercas y arandelas M8 a granel",
    "REF_batt": "Portabaterías con 3 celdas 18650 (referencia)", "REF_pcb": "Placa electrónica (referencia)",
    "REF_ws": "Módulo Waveshare (referencia)", "REF_rtc": "Reloj RTC (referencia)", "REF_panel": "Panel solar 170 × 170 (referencia)",
    "REF_botella": "Botella PET de flotación (referencia)",
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
    "LR2_aro": "Asiento en C de los ganchos M3s, con la base plana hacia la boca de la C; las cuerdas de la linterna cuelgan de cada aro (uno por piso).",
    "PB_aro": "Es una probeta: reproduce un tramo del aro LR2 y el asiento real de M3s. No se monta en el nodo.",
    "T1_caja": "Tapa T2 (4 M3 inox A4 a insertos, con cordón NBR Ø2), Heltec en 4 postes M2,5, SMA de mamparo con junta y tapón de silicona en el puerto USB-C.",
    "T2_tapa": "Caja T1 (4 M3 inox A4 con cordón NBR Ø2) y acrílico de la ventana OLED pegado con sellador.",
}

EST_TIERRA = "Las medidas del Heltec y de la batería son estimadas: confírmalas antes de imprimir."
AVISOS = {"LR2_aro": "Diseñado para 2 kg por piso + 150 N de manipulación; FS entre capas ≥ 3.",
          "PB_aro": "Imprímela y pruébala en el asiento de la probeta antes de imprimir los 4 aros LR2.",
          "T1_caja": EST_TIERRA, "T2_tapa": EST_TIERRA}
AVISO_PASO = {"Aros de la linterna": AVISOS["LR2_aro"], "Probeta del aro": AVISOS["PB_aro"],
              "Caja de la estación de tierra": EST_TIERRA, "Tapa de la estación de tierra": EST_TIERRA}



def material_of(name, kind):
    if kind == "impresa":
        return "PETG (impresa 3D, Bambu P1P)"
    if name.startswith("REF_lastre"):
        return "Acero: tuercas y arandelas M8 a granel"
    if "ventana" in name:
        return "Acrílico (comprado)"
    if name.startswith("REF_botella"):
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
        if name.startswith("REF_lastre"):
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
    if group in ("linterna", "tierra"):
        return (0, 0, 60) if name.startswith("T2_") else (0, 0, 0)
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
    if n in ("REF_batt", "REF_pcb", "REF_ws", "REF_rtc"):
        return (0, 0, 245)
    if n == "REF_panel":
        return (0, 0, 380)
    if n.startswith("REF_botella"):
        return (0, sgn(cy) * 70, 20)
    v = np.array([cx, cy, cz], float)
    nv = np.linalg.norm(v)
    return tuple((v / nv * 100) if nv > 1 else (0, 0, 100))


STEPS = [
    ("nodo", "Caja del nodo", "Empieza por la caja seca M1s: es el cuerpo del nodo y todo lo demás se atornilla a ella.", [r"^M1s"]),
    ("nodo", "Lastre en los bolsillos", "Mete las tuercas y arandelas M8 en los dos bolsillos de abajo y ciérralos con las tapas M3t (2 tornillos cada una). Entra agua: es normal.", [r"^REF_lastre", r"^M3t"]),
    ("nodo", "Bandejas de la electrónica", "Atornilla la bandeja inferior y la superior a los 4 postes del piso de la caja (zona seca).", [r"^M11"]),
    ("nodo", "Tapa con asa", "Pon el cordón de goma Ø2 en la ranura de la tapa M2 y apriétala con 12 tornillos M3. El umbilical sale por su prensaestopas.", [r"^M2_"]),
    ("nodo", "Rieles con gancho", "Cada riel M3s se atornilla a un costado de la caja con 4 tornillos M4. El gancho en C cuelga del aro de la linterna.", [r"^M3s"]),
    ("linterna", "Probeta del aro", "Antes de imprimir los 4 aros, imprime la probeta PB_aro y comprueba que el aro entra en el asiento con el plano hacia la boca.", [r"^PB_aro"]),
    ("linterna", "Aros de la linterna", "Cada aro LR2 entra en el asiento en C de los ganchos M3s con la base plana hacia la boca de la C. Va un aro por piso, a los niveles del ensamble.", [r"^LR2_aro"]),
    ("nodo", "Cápsulas de cámara", "En la punta de cada riel va la cápsula: cuerpo M4, tapa con pie M5s, bisel M6 y ventana de acrílico.", [r"^M4_", r"^M5s", r"^M6_", r"^REF_M7"]),
    ("nodo", "Linterna, aro y cuerdas", "Piezas de referencia: el aro, la malla, los pisos y las cuerdas donde cuelga el nodo.", [r"^REF_aro", r"^REF_linterna", r"^REF_cuerda", r"^REF_cabo", r"^REF_estructura"]),
    ("boya", "Casco de la boya", "Une las dos mitades del casco B1 (6 tornillos M3 y un pin de alineación).", [r"^B1_"]),
    ("boya", "Cunas y botellas", "Atornilla las cunas B5 al casco y apoya las cuatro botellas PET selladas: son las que hacen flotar la boya.", [r"^B5_", r"^REF_botella"]),
    ("boya", "Correas", "Las correas B6 abrazan las botellas desde arriba para que no se salgan.", [r"^B6_"]),
    ("boya", "Cubierta", "Las dos mitades de la cubierta B2 se atornillan a los postes del casco (4 M3 cada una).", [r"^B2_"]),
    ("boya", "Caja seca y electrónica", "Dentro de la caja B3 van las baterías, la placa, el módulo Waveshare y el reloj. Se fija a la cubierta por sus orejas.", [r"^B3_", r"^REF_batt", r"^REF_pcb", r"^REF_ws", r"^REF_rtc"]),
    ("boya", "Tapa de la caja seca", "Cordón O-ring Ø2 en la ranura y tornillos M3 a los insertos de la brida de B3.", [r"^B4_"]),
    ("boya", "Panel solar", "El panel de 170 × 170 se atornilla a las cuatro columnas de la cubierta.", [r"^REF_panel"]),
    ("tierra", "Caja de la estación de tierra", "Funde los insertos M2,5 en los 4 postes y los M3 en las esquinas. El Heltec va sobre los postes, la SMA de mamparo en el agujero de +X y el tapón de silicona en el puerto de −X. Se monta con el USB-C hacia abajo.", [r"^T1_"]),
    ("tierra", "Tapa de la estación de tierra", "Pon el cordón NBR Ø2 en la ranura de T1, pega el acrílico en la ventana OLED y cierra con 4 tornillos M3 inox A4.", [r"^T2_"]),
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




# ----------------------------------------------------------------------------- piece STEP -> assembly placement
def _mats48():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3))
            for i, p in enumerate(perm):
                M[i, p] = sg[i]
            out.append(M)
    return out


R48 = _mats48()


def align(piece_mesh, inst_mesh):
    """Best of the 48 axis-aligned (mirrors included) placements of a piece STEP onto its assembly body.
    Returns (mean distance mm, M 3x3, t) with  world = M @ p + t."""
    from scipy.spatial import cKDTree
    tree = cKDTree(inst_mesh.vertices)
    pv = piece_mesh.vertices
    sample = pv[np.random.RandomState(0).choice(len(pv), min(1500, len(pv)), replace=False)]
    ic = (inst_mesh.bounds[0] + inst_mesh.bounds[1]) / 2
    pc = (piece_mesh.bounds[0] + piece_mesh.bounds[1]) / 2
    best = None
    for M in R48:
        d = tree.query((sample - pc) @ M.T + ic)[0].mean()
        if best is None or d < best[0]:
            best = (d, M)
    d, M = best
    return float(d), M, ic - M @ pc


def g3(p):
    """world mm Z-up -> glTF metres Y-up (the frame of modelo.glb and of the viewer)."""
    return [round(float(p[0]) * 0.001, 5), round(float(p[2]) * 0.001, 5), round(float(-p[1]) * 0.001, 5)]


# ----------------------------------------------------------------------------- seal geometry
def tube(pts, radius, closed=True, sections=6):
    """Cylinder segments through a polyline (the same trick as the umbilical)."""
    pts = [np.array(p, float) for p in pts]
    if closed:
        pts = pts + [pts[0]]
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        d = b - a
        L = float(np.linalg.norm(d))
        if L < 1e-6:
            continue
        cyl = trimesh.creation.cylinder(radius=radius, height=L, sections=sections)
        z = np.array([0, 0, 1.0])
        axis = np.cross(z, d / L)
        ang = math.acos(max(-1, min(1, float(z @ (d / L)))))
        T = trimesh.transformations.rotation_matrix(ang, axis) if np.linalg.norm(axis) > 1e-9 else np.eye(4)
        T[:3, 3] = (a + b) / 2
        cyl.apply_transform(T)
        segs.append(cyl)
    return trimesh.util.concatenate(segs)


def rounded_loop(corners):
    """Four groove corners (any order) -> closed polyline with rounded corners (Chaikin, 3 passes)."""
    c = np.array(corners, float)
    ctr = c.mean(0)
    u, s, vt = np.linalg.svd(c - ctr)
    e1, e2 = vt[0], vt[1]
    order = np.argsort(np.arctan2((c - ctr) @ e2, (c - ctr) @ e1))
    pts = c[order]
    for _ in range(3):
        n = len(pts)
        new = []
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            new += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        pts = np.array(new)
    return pts


def ring(center, axis, R, r):
    """Torus of major radius R and tube radius r around `axis` (unit) at `center`."""
    t = trimesh.creation.torus(major_radius=R, minor_radius=r, major_sections=32, minor_sections=8)
    z = np.array([0, 0, 1.0])
    ax = np.cross(z, axis)
    ang = math.acos(max(-1, min(1, float(z @ axis))))
    T = trimesh.transformations.rotation_matrix(ang, ax) if np.linalg.norm(ax) > 1e-9 else np.eye(4)
    T[:3, 3] = center
    t.apply_transform(T)
    return t


def sphere(c, r):
    s = trimesh.creation.icosphere(subdivisions=1, radius=r)
    s.apply_translation(c)
    return s


SEAL_R = 1.7           # mm, drawn cord radius (real cord is 1.0): slightly fat so that it reads in the viewer


def code_to_key(code, keys):
    """'M2' / 'B5 base' / 'B2 mástil' (as written in sellos.json 'donde') -> piece key."""
    tok = code.strip().split()
    pre = tok[0]
    rest = " ".join(tok[1:]).lower().replace("á", "a")
    for k in keys:
        if k.startswith(pre + "_"):
            if rest and rest not in k:
                continue
            return k
    return None


def build_seals(seals, inst, meshes, rasgos):
    """{seal n: {host instance: mesh}}. `inst` = {name: dict(key, M, t, ok)}. One mesh per host so that in the
    exploded view each ring travels with the piece that carries its groove."""
    out = {}
    by_key = {}
    for nm, d in inst.items():
        by_key.setdefault(d["key"], []).append(nm)

    for s in seals:
        n = s["n"]
        parts = {}                                    # host -> [meshes]
        low = (s["sello"] + " " + s["tipo"]).lower()
        refs = []
        for dd in s.get("donde", []):
            m = re.match(r"(.+?) N° (\d+)", dd)
            if m:
                k = code_to_key(m.group(1), list(rasgos))
                if k:
                    refs.append((k, int(m.group(2))))
        for k, num in refs:
            rs = rasgos.get(k, [])
            if not 0 < num <= len(rs):
                continue
            r = rs[num - 1]
            for nm in by_key.get(k, []):
                d = inst[nm]
                if not d["ok"]:
                    continue
                pts = [d["M"] @ np.array(p, float) + d["t"] for p in r["puntos"]]
                if "pg7" in low and "PG7" in r["tipo"]:
                    bb = meshes[nm][2].bounds
                    c = np.array(pts[0])
                    faces = [(abs(c[i] - bb[j][i]), i) for i in range(3) for j in range(2)]
                    ax = np.zeros(3)
                    ax[min(faces)[1]] = 1
                    parts.setdefault(nm, []).append(ring(c, ax, 6.3, SEAL_R))
                elif len(pts) == 4 and "Ranura" in r["tipo"]:
                    parts.setdefault(nm, []).append(tube(rounded_loop(pts), SEAL_R))
                elif "inserto" in low and "Inserto" in r["tipo"]:
                    parts.setdefault(nm, []).extend(sphere(p, 2.6) for p in pts)
        if "ventana" in low:
            for nm, (g, kind, m) in meshes.items():
                if nm.startswith("REF_M7"):
                    ext = m.bounds[1] - m.bounds[0]
                    ax = np.zeros(3)
                    ax[int(np.argmin(ext))] = 1
                    c = (m.bounds[0] + m.bounds[1]) / 2
                    c = c + ax * (ext[int(np.argmin(ext))] / 2)
                    parts.setdefault(nm, []).append(ring(c, ax, 14.0, SEAL_R))
        if "tapón" in low or "tapon" in low:
            cunas = [m.bounds.mean(0) for nm, (g, kind, m) in meshes.items() if nm.startswith("B5_cuna") and nm.endswith("cuello")]
            for nm, (g, kind, m) in meshes.items():
                if nm.startswith("REF_botella") and cunas:
                    ext = m.bounds[1] - m.bounds[0]
                    a = int(np.argmax(ext))
                    c = m.bounds.mean(0)
                    cn = min(cunas, key=lambda q: np.linalg.norm(q - c))
                    sg = 1.0 if cn[a] >= c[a] else -1.0
                    ax = np.zeros(3)
                    ax[a] = 1
                    cc = c.copy()
                    cc[a] = c[a] + sg * (ext[a] / 2 - 12)
                    parts.setdefault(nm, []).append(ring(cc, ax, 13.0, SEAL_R))
        out[n] = {h: trimesh.util.concatenate(ms) for h, ms in parts.items()}
    return out


# ----------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    SIDECAR.parent.mkdir(parents=True, exist_ok=True)
    import cadquery as cq
    scene = trimesh.Scene()
    node = read_named_step(NODE_STEP)
    buoy = read_named_step(BUOY_STEP)
    print(f"node: {len(node)} bodies ({NODE_STEP.name}, {time.strftime('%d/%m %H:%M', time.localtime(NODE_STEP.stat().st_mtime))}); buoy: {len(buoy)} bodies", flush=True)

    meshes = {}
    for group, items, shift in (("nodo", node, (0, 0, 0)), ("boya", buoy, BUOY_SHIFT)):
        for nm0, sh in items:
            nm = ren(nm0)
            if nm in DROP:
                continue
            printed = bool(re.match(r"^[BM]\d+", nm))
            m = tessellate(sh, TRI_BUDGET_PRINTED if printed else TRI_BUDGET_REF)
            m.apply_translation(shift)
            meshes[nm] = (group, "impresa" if printed else "ref", m)

    # new pieces: 4 rings at the assembly levels (node axis x = y = 0, flat down) and the bench pieces beside the model
    placed = {}
    niveles = read_json(LOCAL_JSON).get("ensamble", {}).get("niveles", [])
    if niveles:
        ring = tessellate(cq.importers.importStep(str(ARO_STEP)).val(), TRI_BUDGET_PRINTED)
        for i, z in enumerate(niveles, 1):
            t = np.array([0.0, 0.0, float(z)])
            m = ring.copy()
            m.apply_translation(t)
            meshes[f"LR2_aro_{i}"] = ("linterna", "impresa", m)
            placed[f"LR2_aro_{i}"] = t
    else:
        print(f"  AVISO: {LOCAL_JSON.name} sin ensamble.niveles: no se colocan los aros LR2")
    for nm, group, f, x in BENCH_PIECES:
        m = tessellate(cq.importers.importStep(str(f)).val(), TRI_BUDGET_PRINTED)
        c, lo = (m.bounds[0] + m.bounds[1]) / 2, m.bounds[0][2]
        t = np.array([x - c[0], BENCH_Y - c[1], BENCH_Z - lo])
        m.apply_translation(t)
        meshes[nm] = (group, "impresa", m)
        placed[nm] = t

    # drawn umbilical: node lid top -> buoy box side
    b3 = next((m for n, (g, k, m) in meshes.items() if n.startswith("B3_")), None)
    lid = next((m for n, (g, k, m) in meshes.items() if n.startswith("M2_")), None)
    if b3 is not None and lid is not None:
        top = lid.bounds[1][2]
        bb = b3.bounds
        meshes["REF_umbilical"] = ("nodo", "ref", umbilical_mesh((0, 0, top), (bb[0][0], (bb[0][1] + bb[1][1]) / 2, (bb[0][2] + bb[1][2]) / 2)))

    # piece STEP -> assembly placement (for hole markers and seal rings)
    rasgos = read_json(RASGOS)
    inst, cache = {}, {}
    for nm, (group, kind, m) in meshes.items():
        if kind != "impresa":
            continue
        key = base_key(nm)
        if nm in placed:
            inst[nm] = dict(key=key, M=np.eye(3), t=placed[nm], ok=True, d=0.0)
            continue
        f = (NODE_STEPS if group == "nodo" else BUOY_STEPS) / f"{key}.step"
        ok, d, M, t = False, None, np.eye(3), np.zeros(3)
        if f.exists():
            if key not in cache:
                cache[key] = tessellate(cq.importers.importStep(str(f)).val(), TRI_BUDGET_PRINTED)
            d, M, t = align(cache[key], m)
            ok = d <= ALIGN_TOL
        print(f"  placement {nm:28s} {'ok ' if ok else 'NO '} {'' if d is None else f'{d:.2f} mm'}", flush=True)
        inst[nm] = dict(key=key, M=M, t=t, ok=ok, d=d)

    sellos = read_json(SELLOS_JSON)
    seal_meshes = build_seals(sellos if isinstance(sellos, list) else [], inst, meshes, rasgos)

    # buoy group centre (for radial rules)
    bm = [m.bounds for n, (g, k, m) in meshes.items() if g == "boya"]
    gc = tuple((np.min([b[0] for b in bm], 0) + np.max([b[1] for b in bm], 0)) / 2) if bm else (0, 0, 0)

    geo, sin3d = {}, []
    for nm, (group, kind, m) in meshes.items():
        c = (m.bounds[0] + m.bounds[1]) / 2
        off = offset_for(nm, c, group, gc)
        e = dict(group=group, kind=kind, key=base_key(nm) if kind == "impresa" else nm,
                 centro=g3(c), offset=[round(off[0] * 0.001, 5), round(off[2] * 0.001, 5), round(-off[1] * 0.001, 5)],
                 bbox=[g3(m.bounds[0]), g3(m.bounds[1])])
        if kind == "impresa":
            d = inst[nm]
            e["colocacion"] = dict(ok=d["ok"], error_mm=None if d["d"] is None else round(d["d"], 2))
            if d["ok"]:
                rs = rasgos.get(d["key"], [])
                e["rasgos_pts"] = {str(r["n"]): [g3(d["M"] @ np.array(p, float) + d["t"]) for p in r["puntos"]] for r in rs}
        geo[nm] = e
        mm = m.copy()
        if kind == "ref" and nm != "REF_umbilical":
            mm.visual.face_colors = [150, 160, 170, 110]
        scene.add_geometry(zup_to_gltf(mm), node_name=nm, geom_name=nm)

    for n, hosts in sorted(seal_meshes.items()):
        s = next(x for x in sellos if x["n"] == n)
        slug = re.sub(r"[^A-Za-z0-9]+", "_", unicodedata.normalize("NFKD", s["sello"]).encode("ascii", "ignore").decode()).strip("_")[:32]
        if not hosts:
            print(f"  seal {n}: no 3D geometry (list only)")
            sin3d.append(n)
            continue
        for host, m in sorted(hosts.items()):
            nm = f"SELLO_{n:02d}_{slug}" + (f"__{host}" if len(hosts) > 1 else "")
            c = (m.bounds[0] + m.bounds[1]) / 2
            geo[nm] = dict(group=geo[host]["group"], kind="sello", key=nm, n=n, host=host,
                           centro=g3(c), offset=geo[host]["offset"], bbox=[g3(m.bounds[0]), g3(m.bounds[1])])
            mm = m.copy()
            mm.visual.face_colors = [214, 40, 40, 255]
            scene.add_geometry(zup_to_gltf(mm), node_name=nm, geom_name=nm)

    glb = scene.export(file_type="glb", include_normals=False)
    (OUT / "modelo.glb").write_bytes(glb)
    stamp = lambda p: f"{p.name} ({time.strftime('%d/%m %H:%M', time.localtime(p.stat().st_mtime))})"   # noqa: E731
    SIDECAR.write_text(json.dumps(dict(piezas=geo, sellos_sin_3d=sin3d, fuentes=dict(nodo=stamp(NODE_STEP), boya=stamp(BUOY_STEP)),
                                       generado=time.strftime("%d/%m/%Y %H:%M")), ensure_ascii=False), encoding="utf-8")
    tri = sum(len(m.faces) for _, _, m in meshes.values())
    print(f"{len(geo)} meshes ({sum(1 for v in geo.values() if v.get('kind') == 'sello')} seal meshes), {tri} triangles, "
          f"glb {len(glb) / 1e6:.2f} MB, {time.time() - t0:.0f}s", flush=True)
    if "--sin-datos" not in sys.argv:
        import visor_datos
        visor_datos.main()


if __name__ == "__main__":
    sys.exit(main())
