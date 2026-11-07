"""Step 0 of docs/ENCARGO_SIMSCALE_2026-11-07.md: the geometry to simulate is the one delivered for printing.

    python verificar_entrega.py            -> salida/verificacion/verificacion_0711.json (printed summary)

Reads the 3 assembly STEPs uploaded to "LanternGuard - PIEZAS PARA IMPRIMIR" (salida/limpio/step/00_ENSAMBLE_*.step),
names every solid (XCAF), computes its volume, and compares it with the per-piece STEP of the repo (same name, volume
within 0.1 %). Then checks the design facts the brief lists (seat 17.1, ring 16.5, closed rail, halves, chamfer 6,
deck bars 26 x 20, T1/T2). No network.
"""
import json
import math
import os
import sys
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")
HERE = Path(__file__).resolve().parent
MOD = HERE.parent
sys.path.insert(0, str(HERE))

from OCP.STEPCAFControl import STEPCAFControl_Reader            # noqa: E402
from OCP.TDocStd import TDocStd_Document                        # noqa: E402
from OCP.TCollection import TCollection_ExtendedString          # noqa: E402
from OCP.XCAFDoc import XCAFDoc_DocumentTool                    # noqa: E402
from OCP.TDF import TDF_LabelSequence                           # noqa: E402
from OCP.TDataStd import TDataStd_Name                          # noqa: E402
from OCP.TopAbs import TopAbs_SOLID                             # noqa: E402
from OCP.TopExp import TopExp_Explorer                          # noqa: E402
from OCP.GProp import GProp_GProps                              # noqa: E402
from OCP.BRepGProp import BRepGProp                             # noqa: E402
import cadquery as cq                                           # noqa: E402

LIMPIO = MOD / "salida" / "limpio" / "step"
OUT = MOD / "salida" / "verificacion"
P2 = MOD / "salida" / "prototipos" / "P2_robusto" / "step"
BOYA = MOD / "salida" / "boya_pet" / "step"
ARO = MOD / "salida" / "aro" / "step"
TIERRA = MOD / "salida" / "tierra" / "step"


def vol(shape):
    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, g)
    return g.Mass()


def named_solids(path):
    """[(name, volume_mm3, shape)] of every solid in an assembly STEP, name = its PRODUCT label."""
    doc = TDocStd_Document(TCollection_ExtendedString("doc"))
    r = STEPCAFControl_Reader()
    r.SetNameMode(True)
    if r.ReadFile(str(path)) != 1:
        raise RuntimeError(f"cannot read {path}")
    r.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    labels = TDF_LabelSequence()
    st.GetFreeShapes(labels)
    out = []

    def walk(lab, loc_shape=None):
        shape = st.GetShape_s(lab)
        name_attr = TDataStd_Name()
        name = name_attr.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), name_attr) else "?"
        if st.IsAssembly_s(lab):
            comps = TDF_LabelSequence()
            st.GetComponents_s(lab, comps)
            for i in range(1, comps.Length() + 1):
                walk(comps.Value(i))
            return
        if st.IsReference_s(lab):
            ref = lab.__class__()
            st.GetReferredShape_s(lab, ref)
            nm = TDataStd_Name()
            if ref.FindAttribute(TDataStd_Name.GetID_s(), nm):
                name = nm.Get().ToExtString()
            shape = st.GetShape_s(lab)
        ex = TopExp_Explorer(shape, TopAbs_SOLID)
        while ex.More():
            s = ex.Current()
            out.append((name, vol(s), s))
            ex.Next()

    for i in range(1, labels.Length() + 1):
        walk(labels.Value(i))
    return out


def piece_volume(path):
    sh = cq.importers.importStep(str(path))
    return sum(s.Volume() for s in sh.solids().vals()), sh


SOURCE = {  # assembly solid name (prefix) -> per-piece STEP of the repo
    "LR2_aro": ARO / "LR2_aro.step", "M11_bandeja_sup": P2 / "M11_bandeja_sup.step", "M11_bandeja": P2 / "M11_bandeja.step",
    "M1s_caja_cuerpo": P2 / "M1s_caja_cuerpo.step", "M2_caja_tapa": P2 / "M2_caja_tapa.step",
    "M3f_marco_bolsillo": P2 / "M3f_marco_bolsillo.step", "M3s_riel_gancho": P2 / "M3s_riel_gancho.step",
    "M3t_tapa_bolsillo": P2 / "M3t_tapa_bolsillo.step", "M4_capsula_cuerpo": P2 / "M4_capsula_cuerpo.step",
    "M5s_capsula_tapa_pie": P2 / "M5s_capsula_tapa_pie.step", "M6_capsula_bisel": P2 / "M6_capsula_bisel.step",
    "B1_casco": BOYA / "B1_casco.step", "B2_cubierta_lisa": BOYA / "B2_cubierta_lisa.step",
    "B2_cubierta_mastil": BOYA / "B2_cubierta_mastil.step", "B3_caja": BOYA / "B3_caja.step", "B4_tapa": BOYA / "B4_tapa.step",
    "B5_cuna": None, "B6_correa": BOYA / "B6_correa.step", "T1_caja": TIERRA / "T1_caja.step", "T2_tapa": TIERRA / "T2_tapa.step",
}


def source_of(name):
    if name.startswith("B5_cuna"):
        return BOYA / ("B5_cuna_cuello.step" if "cuello" in name else "B5_cuna_base.step")
    for k in sorted(SOURCE, key=len, reverse=True):
        if name.startswith(k) and SOURCE[k]:
            return SOURCE[k]
    return None


def cyl_diams(shape):
    ds = set()
    for f in cq.Shape.cast(shape).Faces():
        if f.geomType() == "CYLINDER":
            ds.add(round(2 * f._geomAdaptor().Cylinder().Radius(), 2))
    return sorted(ds)


def chamfer_faces(shape, leg):
    """Vertical planar faces at 45 degrees in plan whose width is leg*sqrt(2) (the plan chamfer of the corners)."""
    n = 0
    for f in cq.Shape.cast(shape).Faces():
        if f.geomType() != "PLANE":
            continue
        nv = f.normalAt()
        if abs(nv.z) > 1e-3 or abs(abs(nv.x) - abs(nv.y)) > 1e-3:
            continue
        bb = f.BoundingBox()
        w = math.hypot(bb.xlen, bb.ylen)
        if abs(w - leg * math.sqrt(2)) < 0.3:
            n += 1
    return n


def main():
    import params as P
    OUT.mkdir(parents=True, exist_ok=True)
    rep = {"ensambles": {}, "piezas": {}, "hechos": {}}
    pv_cache = {}
    for asm in ("00_ENSAMBLE_nodo", "00_ENSAMBLE_boya", "00_ENSAMBLE_tierra"):
        sol = named_solids(LIMPIO / f"{asm}.step")
        rows = []
        for name, v, s in sol:
            src = source_of(name)
            if src is None:
                rows.append(dict(nombre=name, vol_mm3=round(v, 1), fuente=None, ref=name.upper().startswith("REF")))
                continue
            if src not in pv_cache:
                pv_cache[src] = piece_volume(src)
            pv = pv_cache[src][0]
            n_src = len(pv_cache[src][1].solids().vals())
            per = pv / n_src
            ok = min(abs(v - per), abs(v - pv)) / max(v, 1e-9) < 1e-3
            rows.append(dict(nombre=name, vol_mm3=round(v, 1), fuente=str(src.relative_to(MOD)).replace("\\", "/"),
                             vol_fuente_mm3=round(per if abs(v - per) < abs(v - pv) else pv, 1), igual=ok))
        rep["ensambles"][asm] = rows
        print(asm, len(sol), "solids;", sum(1 for r in rows if r.get("igual")), "equal to repo piece;",
              [r["nombre"] for r in rows if r.get("igual") is False])

    m3s = cq.importers.importStep(str(P2 / "M3s_riel_gancho.step"))
    d3 = cyl_diams(m3s.val().wrapped)
    aro_bb = cq.importers.importStep(str(ARO / "LR2_aro.step")).val().BoundingBox()
    m1 = cq.importers.importStep(str(P2 / "M1s_caja_cuerpo.step")).val().wrapped
    m2 = cq.importers.importStep(str(P2 / "M2_caja_tapa.step")).val().wrapped
    boya_names = [r["nombre"] for r in rep["ensambles"]["00_ENSAMBLE_boya"]]
    H = rep["hechos"]
    H["M3s_asiento_17.1"] = dict(ok=17.1 in d3, diametros_cilindros=d3)
    H["LR2_aro_seccion_16.5"] = dict(ok=abs(P.RING_SECTION - 16.5) < 1e-6 and abs(aro_bb.zlen - 16.5) < 0.6,
                                     params=P.RING_SECTION, alto_bbox=round(aro_bb.zlen, 2), perimetros=P.AROS["perimetros"],
                                     ok_perimetros=P.AROS["perimetros"] == 13)
    H["M1s_M2_chaflan_6"] = dict(ok=chamfer_faces(m1, 6.0) >= 4 and chamfer_faces(m2, 6.0) >= 4,
                                 caras_M1s=chamfer_faces(m1, 6.0), caras_M2=chamfer_faces(m2, 6.0), params=P.BOX_CORNER_CH)
    H["B2_barras_26x20"] = dict(ok=tuple(P.PET_XBAR[:2]) == (26.0, 20.0), params=list(P.PET_XBAR))
    H["mitades_B1_B5"] = dict(ok=sum(n.startswith("B1_casco") for n in boya_names) == 2 and sum(n.startswith("B5_cuna") for n in boya_names) == 4,
                              B1=sum(n.startswith("B1_casco") for n in boya_names), B5=sum(n.startswith("B5_cuna") for n in boya_names),
                              B2=sum(n.startswith("B2_cubierta") for n in boya_names))
    H["riel_cerrado_M3s_x2"] = dict(ok=sum(r["nombre"].startswith("M3s") for r in rep["ensambles"]["00_ENSAMBLE_nodo"]) == 2)
    H["T1_T2"] = dict(ok=len(rep["ensambles"]["00_ENSAMBLE_tierra"]) == 2)
    for k, v in H.items():
        print(f"{k:24s} {'OK' if v['ok'] else 'DIFIERE'}  {json.dumps({a: b for a, b in v.items() if a != 'ok'}, ensure_ascii=False)}")
    (OUT / "verificacion_0711.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
