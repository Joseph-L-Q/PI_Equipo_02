"""Safety margins per printed piece (block 1 of 04/11): bbox in print orientation vs the usable bed, measured minimum wall,
and the most slender vertical element (height / thickness) before -> after. Writes docs/MARGENES.md and salida/margenes.json.

    python margenes.py [--antes <git ref>]      (from cad_final/; default ref 1fc425c = before the 04/11 changes)

Wall thickness is measured on the STL: from N surface samples a ray is cast inwards (minus the face normal) and the
distance to the opposite face is the local thickness. The 1st percentile is reported (the absolute minimum is dominated
by chamfer tips and hole edges, which are not walls). The slender element is declared per piece from the CAD
(params + boya_pet), because a mesh does not say what a "post" is.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import trimesh

import params as P

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
SAL = MOD / "salida"
N = 3000


def wall(stl, n=N, seed=1):
    m = trimesh.load(stl)
    pts, fi = trimesh.sample.sample_surface(m, n, seed=seed)
    nr = m.face_normals[fi]
    org = pts - nr * 1e-3
    loc, ray, _ = m.ray.intersects_location(org, -nr, multiple_hits=False)
    if len(ray) == 0:
        return None, None
    d = np.linalg.norm(loc - org[ray], axis=1)
    d = d[d > 0.05]
    return float(np.percentile(d, 1)), float(np.percentile(d, 5))


def bbox(stl, orient):
    from checks import mesh_checks
    o = {"sin girar": None, "X180": ("X", 180), "X+90": ("X", 90), "Y+90": ("Y", 90)}.get(orient)
    return mesh_checks(str(stl), (*P.BED_USE, P.PRINT_BED[2]), o)["bbox"]


# most slender vertical element per piece: (description before, h, t before, description after, h, t after)
def slender():
    import boya_pet as B
    d = B.dims(P.FLOT_BOTTLE, P.FLOT_COUNT)
    zs = d["wall"] + P.PET_STOP_H
    up_h = d["z_top"] - d["zc"]                              # old uprights of the mid ribs, between slot and channel
    up_t = d["Wb"] / 2 - d["slot_w"] / 2
    post_free = d["z_top"] - zs
    strap_free = d["z_top"] - d["wall_h"]
    col_h = d["z_panel0"] - d["z_cover_top"]
    return {
        "B1_casco": (f"varilla de costilla intermedia {up_t:.1f} x 3 mm (lado canal)", up_h, up_t,
                     f"poste M3 Ø{P.PET_POST_B1:g} libre sobre la silla, con collar", post_free, P.PET_POST_B1),
        "B5_cuna": (f"varilla de costilla intermedia {up_t:.1f} x 3 mm", up_h, up_t,
                    f"poste de correa Ø{P.PET_POST_D:g} (libre sobre la pared)", strap_free, P.PET_POST_D),
        "B2_cubierta": (f"columna del panel Ø{P.PET_COLUMN_D:g}", col_h, P.PET_COLUMN_D,
                        f"columna del panel Ø{P.PET_COLUMN_D:g}, con chaflán", col_h, P.PET_COLUMN_D),
    }


def esbeltos(stem):
    """Slender elements of the enforced registry (esbelto.py + esbelto_nodo.py) that belong to this piece: [(name, t, ok)]."""
    import esbelto as E
    code = stem.split("_")[0]
    out = []
    for n, t in E.registro() + E._nodo():
        first = n.replace("nodo: ", "").split(" ")[0].split("/")
        if code in first:
            out.append((n.replace("nodo: ", ""), t, t >= P.SLENDER_T_MIN - 1e-9))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--antes", default="1fc425c")
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="margenes_"))
    sets = []
    boya = json.loads((SAL / "boya_pet" / "slicer.json").read_text(encoding="utf-8"))
    for stem, info in boya.items():
        sets.append(("boya", stem, SAL / "boya_pet" / "stl" / f"{stem}.stl", info["orientacion"]))
    p2 = json.loads((SAL / "prototipos" / "P2_robusto" / "resultados.json").read_text(encoding="utf-8"))["piezas"]
    for stem, info in p2.items():
        sets.append(("nodo P2", stem, SAL / "prototipos" / "P2_robusto" / "stl" / f"{stem}.stl", info["orient"]))
    old_boya = {"B1_casco": "B1_casco", "B2_cubierta_lisa": "B2_cubierta", "B2_cubierta_mastil": "B2_cubierta",
                "B5_cuna_base": "B5_cuna", "B5_cuna_cuello": "B5_cuna"}
    sl = slender()
    rows = []
    for grp, stem, stl, orient in sets:
        bb = bbox(stl, orient)
        w1, w5 = wall(stl)
        prev = None
        if grp == "boya":
            ostem = old_boya.get(stem, stem)
            rel = f"Proyecto/MóduloMecánico/salida/boya_pet/stl/{ostem}.stl"
            dst = tmp / f"{ostem}.stl"
            if not dst.exists():
                blob = subprocess.run(["git", "show", f"{a.antes}:{rel}"], cwd=MOD, capture_output=True).stdout
                dst.write_bytes(blob)
            if dst.stat().st_size:
                ob = json.loads(subprocess.run(["git", "show", f"{a.antes}:Proyecto/MóduloMecánico/salida/boya_pet/slicer.json"], cwd=MOD,
                                               capture_output=True).stdout)
                prev = dict(bbox=bbox(dst, ob[ostem]["orientacion"]), wall=wall(dst)[0])
        key = next((k for k in sl if stem.startswith(k)), None)
        rows.append(dict(grupo=grp, pieza=stem, bbox=[round(v, 1) for v in bb], cabe=bb[0] <= P.BED_USE[0] and bb[1] <= P.BED_USE[1],
                         pared_p1=round(w1, 2) if w1 else None, pared_p5=round(w5, 2) if w5 else None, antes=prev,
                         esbelto=sl.get(key), esb=esbeltos(stem)))
        print(f"{stem:22s} bbox {bb[0]:6.1f} x {bb[1]:6.1f}  pared p1 {w1:5.2f}", flush=True)
    (SAL / "margenes.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    write_md(rows)


NOTES = {   # piece -> what the measured minimum is and what is done about it
    "B1_casco": "2.4 = paredes laterales con ventanas y patín (no estructurales; excepción declarada). Costillas 3 → 4 → 5 mm; varillas de 2.4 × 3 mm eliminadas (topes bajos); brida de unión 5 + 5, columnas de 16, pin Ø5, lengüeta y ranura en las columnas; chaflán de 45° × 3 en la base de postes y costillas.",
    "B2_cubierta_lisa": "Barras de 14 × 8 mm; 4 lengüetas verticales en la barra de la costura; orejas de la caja de 5; pilares Ø10.",
    "B2_cubierta_mastil": "Pared del mástil 3 → 5 (Ø18 / Ø8); mismas barras, pilares y columnas que el lado liso.",
    "B3_caja": "Postes de la bandeja Ø8 → Ø9: el anillo alrededor del inserto Ø4 pasa de 2.0 a 2.5 (la malla facetada lo mide 2.2). Paredes de 2.4 = placas apoyadas en sus 4 bordes.",
    "B4_tapa": "Tapa de 6.5 mm: quedan 5 bajo la ranura de la junta (antes 2.5).",
    "B5_cuna_base": "2.4 = paredes laterales (no estructurales). Postes de correa Ø8 → Ø10; lengüeta vertical en vez de pin; lengüetas de 12 × 14.",
    "B5_cuna_cuello": "Igual que el lado base.",
    "B6_correa": "Correa de 14 × 5 (antes 14 × 4).",
    "M1s_caja_cuerpo": "Paredes y fondo de 5. Sin soportes: el piso es plano porque los bolsillos de lastre pasaron al marco M3f (4 orejas M3 de 20 × 14 × 12); ventana con techo a 45°. Ventana 24 × 18 al canal del riel en cada extremo (sin PG7).",
    "M3s_riel_gancho": "Riel cerrado 36 × 30, paredes 6, sin ventanas; pared del gancho 5; 2 costillas de apoyo de 6 bajo el riel y techo del canal a 45° (sin soportes casi todo: 12.2 % aceptado). FS entre capas 2.72 → 3.18 (alma del gancho 20 → 26). El 1.9 medido es el labio de 1.5 entre la ranura de la junta y el canal (1.6 de alto), no una pared.",
    "M4_capsula_cuerpo": "Pared de 5, brida de 6, falda a 45° bajo la brida. 1.2 = tubo separador de luz del aro LED (óptico, no estructural). No se puede engrosar sin cambiar el aro: "
                         "el agujero Ø19 del aro limita el diámetro exterior del tubo. Se ajusta cuando se mida el aro comprado (`aro_led.agujero`).",
    "M5s_capsula_tapa_pie": "Silla de 10 con 4 insertos M3 y junta; tapa 5 → 6. FS entre capas 2.47 → 3.80. El 1.5 medido es el labio entre la ranura de la junta y el pase del cable (1.6 de alto), no una pared.",
    "M2_caja_tapa": "Tapa sin girar y sin soportes; asa de 60 con ventana de techo a 45° y ojo en gota.",
    "M3f_marco_bolsillo": "Marco del bolsillo de lastre (×2), fuera del sello, atornillado a las 4 orejas de M1s; paredes de 5.",
    "M3t_tapa_bolsillo": "Placa de 5 que cierra el marco M3f (fuera del sello).",
    "M6_capsula_bisel": "2.25 en el borde del bisel (no estructural).",
    "M11_bandeja_sup": "Bandeja de 3 sin postes propios.",
    "M11_bandeja": "2.3 en la bandeja (no estructural, dentro de la caja). Postes pasantes para el M3 × 38; sin la ventana en ocho.",
}


def write_md(rows):
    L = ["# MÁRGENES DE SEGURIDAD (04/11/2026)", "",
         f"Reglas: ninguna pieza pasa de **{P.BED_USE[0]:g} × {P.BED_USE[1]:g} mm** en X o Y en su orientación de impresión "
         f"(`impresora.cama_util`; `build.py` falla si alguna se pasa, con `cama.py`). Pared mínima **{P.WALL_MIN_NS:g} mm** en lo no "
         f"estructural. **{P.SLENDER_T_MIN:g} mm** mínimo en todo elemento vertical esbelto (alto/espesor > {P.SLENDER_RATIO:g}) o "
         f"cargado, con chaflán en la base. FS objetivo **≥ {P.FS_TARGET_Z:g} entre capas** en lo estructural.", "",
         "Pared medida en el STL: percentil 1 del espesor local, con 3000 rayos hacia adentro. El mínimo absoluto lo dan "
         "las puntas de chaflán y los bordes de agujero, que no son paredes. Antes = commit `1fc425c` (antes de los cambios del 04/11).", "",
         "## Boya PET 4 × 1 L", "",
         "| Pieza | Caja X × Y (mm) | Cabe en 230 | Pared p1 antes → después | Elemento más esbelto: antes → después (alto/espesor) | Nota |",
         "|---|---|---|---|---|---|"]
    for r in rows:
        if r["grupo"] != "boya":
            continue
        a = r["antes"] or {}
        bb0 = f"{a['bbox'][0]:.0f} × {a['bbox'][1]:.0f} → " if a.get("bbox") else ""
        w0 = f"{a['wall']:.2f} → " if a.get("wall") else ""
        e = r["esbelto"]
        es = f"{e[0]} ({e[1] / e[2]:.1f}) → {e[3]} ({e[4] / e[5]:.1f})" if e else "—"
        L.append(f"| {r['pieza']} | {bb0}{r['bbox'][0]:.0f} × {r['bbox'][1]:.0f} | {'sí' if r['cabe'] else '**NO**'} | {w0}{r['pared_p1']:.2f} | "
                 f"{es} | {NOTES.get(r['pieza'], '')} |")
    L += ["", "## Nodo P2 robusto (riel cerrado, 04/11)", "",
          "| Pieza | Caja X × Y (mm) | Cabe en 230 | Pared p1 | Nota |", "|---|---|---|---|---|"]
    for r in rows:
        if r["grupo"] == "boya":
            continue
        L.append(f"| {r['pieza']} | {r['bbox'][0]:.0f} × {r['bbox'][1]:.0f} | {'sí' if r['cabe'] else '**NO**'} | {r['pared_p1']:.2f} | "
                 f"{NOTES.get(r['pieza'], '')} |")
    L += ["", 'Aire entre cuerdas y caja (05/11): las 4 cuerdas suben a 45° junto a las esquinas de la brida de la tapa. Con paredes de 5 mm la brida creció a 149 × 148 y el aire bajó a 1.5 mm (antes 2.9). Se cortó un chaflán de 6 mm en las 4 esquinas de la brida de M1s y de la tapa M2 (`caja.chaflan_esquina`, solo P2): ahora las cuerdas pasan a 3.2 mm (3.24, 3.24, 3.24, 3.24). Las dos piezas tienen el mismo contorno, por eso había que cortar las dos. Los 4 tornillos de esquina se corrieron 5.9 mm sobre el borde para dejar 5 mm de material junto al inserto; la ranura de la junta no se toca (queda a 10 mm del chaflán). Sigue por debajo de los 10 mm que se piden a brazos y cápsulas: es un aviso, no una falla.']
    L += ["", "## Elementos esbeltos por pieza (registro con control, `esbelto.py` + `esbelto_nodo.py`)", "",
          f"Cada elemento declarado debe medir al menos **{P.SLENDER_T_MIN:g} mm**; si no, `esbelto.py` sale con error y `build.py` / `boya_pet.py` no construyen. "
          "Espesor = lado fino (pared, costilla, oreja, barra) o diámetro (poste, columna).", "",
          "| Pieza | Elemento | Espesor (mm) | ¿Cumple? |", "|---|---|---|---|"]
    for r in rows:
        for n, t, ok in r.get("esb") or []:
            L.append(f"| {r['pieza']} | {n} | {t:.1f} | {'sí' if ok else '**NO**'} |")
        if not r.get("esb"):
            L.append(f"| {r['pieza']} | — (sin elementos esbeltos declarados) | — | — |")
    import esbelto as E
    L += ["", "Excepciones declaradas (más finas que el mínimo, con su motivo):", ""]
    L += [f"- {n}: **{t:g} mm**. {why}" for n, t, why in E.EXCEPCIONES]
    L += ["", "## Fuera de la cama útil", "",
          "- `M1m_caja_riel` de P3 y P4 (monocasco: caja y riel en una pieza) mide 250 mm. No se imprime ahora (la piscina usa P2). "
          "P3/P4 siguen con el riel anterior: si P4 se presenta impreso, hay que llevarle el riel cerrado y partirlo.", "",
          "## FS entre capas (FEM local, CalculiX)", "",
          "| Pieza | FS a lo largo | FS entre capas | Objetivo ≥ 3 |", "|---|---|---|---|",
          "| M3s riel cerrado (agua 150 N) | 6.50 | 3.18 | **sí** (antes, en celosía: 5.56 / 2.72) |",
          "| M3s riel cerrado (izado 150 N) | 11.19 | 5.47 | **sí** |",
          "| M5s pie de la tapa de cápsula | 7.77 | 3.80 | **sí** (antes 5.04 / 2.47) |",
          "| Boya (B1 a B6) | — | — | sin FEM local: cargas bajas (flotación); el análisis de SimScale de B2 y B3 va en el bloque 3 |", "",
          "El 04/11 se aplicó la corrección de concepto: riel cerrado y un solo volumen seco. Todo lo estructural del nodo P2 "
          "cumple FS ≥ 3 entre capas (FEM local con CalculiX, `salida/prototipos/P2_robusto/fem/fem.json`)."]
    (MOD / "docs" / "MARGENES.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
