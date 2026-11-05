"""05/11/2026 batch, block 2, NO Onshape API (quota spent). Finds the pieces whose geometry changed since the 04/11
upload to Onshape, leaves their STEP + the assembly STEP for a manual import, draws their A4 sheets locally (team format)
and merges PLANOS_A4_LanternGuard_v6.pdf.

    python publicar_sin_api.py --cambiadas                   # list changed pieces (volume / bbox / solids vs 04/11)
    python publicar_sin_api.py --importar                    # salida/onshape_importar/2026-11-05/ + IMPORTAR.md
    python publicar_sin_api.py --planos                      # local A4 sheets of the changed pieces + v6 PDF

Baseline: salida/step_hash_2026-11-04.json (volume, bbox and solid count of every STEP as uploaded on 04/11, written
before any 05/11 change). A STEP whose only change is the OCC time stamp is NOT a change.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

import onshape_sync as OS
import planos_0511 as Q
import planos_onshape as P


def _no_api(*a, **k):
    raise SystemExit("publicar_sin_api: la API de Onshape está prohibida en este encargo")


OS.Client.call = _no_api

FECHA = "2026-11-05"
BASE = P.MOD / "salida" / "step_hash_2026-11-04.json"
IMP = P.MOD / "salida" / "onshape_importar" / FECHA
LOCAL6 = P.OUT / "pdf_a4_local_0511b"
DOC = "LG_IMPRIMIR_P2"
# why each piece changed (filled from the 05/11 block-1 results; default text otherwise)
MOTIVO = {}
MOTIVO_FILE = P.MOD / "salida" / "motivos_2026-11-05.json"


def pieces():
    P.use_format("equipo")
    if not any(p[0] == "M3f_marco_bolsillo" for p in P.PIECES):
        P.PIECES.append((Q.M3F[0], Q.M3F[1], P.P2 / "stl" / "M3f_marco_bolsillo.stl", Q.M3F[3]))
        P.A4_ORDER.insert(P.A4_ORDER.index("M3t_tapa_bolsillo") + 1, "M3f_marco_bolsillo")
    return {c: (Path(stp), q) for c, stp, _, q in P.PIECES}


def cambiadas():
    import cadquery as cq
    base = json.loads(BASE.read_text(encoding="utf-8"))
    out = []
    for code, (stp, q) in pieces().items():
        b = base.get(code)
        if not stp.exists():
            continue
        s = cq.importers.importStep(str(stp)).val()
        bb = s.BoundingBox()
        vol, dims, n = s.Volume(), (bb.xlen, bb.ylen, bb.zlen), len(s.Solids())
        if b is None:
            out.append((code, "pieza nueva", None, vol))
            continue
        dv = (vol - b["vol"]) / b["vol"]
        dd = max(abs(x - y) for x, y in zip(dims, b["bb"]))
        if abs(dv) > 1e-4 or dd > 0.02 or n != b["n"]:
            out.append((code, f"volumen {100 * dv:+.2f} %, caja envolvente {dd:.2f} mm", b["vol"], vol))
    return out


def motivos():
    return json.loads(MOTIVO_FILE.read_text(encoding="utf-8")) if MOTIVO_FILE.exists() else {}


def importar(ch):
    IMP.mkdir(parents=True, exist_ok=True)
    by = pieces()
    mot = motivos()
    R = P.reg()
    url = R["documento"]["url"]
    rows = []
    for i, (code, delta, v0, v1) in enumerate(ch, 1):
        stp = by[code][0]
        shutil.copy2(stp, IMP / f"{code}.step")
        m = mot.get(code, delta)
        rows.append(f"| {i} | `{code}.step` | Part Studio `{code}` | {m} | {v1 / 1000:.1f} cm³ (antes {v0 / 1000:.1f}) |"
                    if v0 else f"| {i} | `{code}.step` | (nueva) Part Studio `{code}` | {m} | {v1 / 1000:.1f} cm³ |")
    asm = IMP / "00_ENSAMBLE.step"
    items = Q.build_assembly(asm)
    n_sol = sum(Q.solids_of(sh.wrapped) for _, sh in items)
    md = f"""# Importar a Onshape a mano ({FECHA})

La cuota de la API de Onshape se agotó, así que estas piezas no se subieron solas. Hay que importarlas a mano en el
documento **{DOC}**: {url}

Las piezas que no están en esta lista no cambiaron y no se tocan.

## Orden

1. Abrir el documento {DOC}.
2. Para cada fila de la tabla, en orden:
   1. Clic derecho en la pestaña `<pieza>` → **Rename** → `OLD {FECHA} <pieza> (<motivo corto>)`. No se borra.
   2. Botón **+** (abajo a la izquierda) → **Import…** → elegir el archivo `.step` de esta carpeta.
   3. Cuando termine de traducir, renombrar la pestaña nueva a `<pieza>`, sin sufijo.
   4. Si la pieza tiene plano `PLANO_A4_<pieza>`, abrirlo y apuntar la vista a la pestaña nueva (o hacer un plano nuevo con el
      formato del equipo). Los planos de Melissa ("Drawing …") no se tocan.
3. Al final, el ensamble: renombrar `00_ENSAMBLE` a `OLD {FECHA} 00_ENSAMBLE`, importar `00_ENSAMBLE.step` y renombrar la
   pestaña nueva a `00_ENSAMBLE`. Debe tener **{n_sol} sólidos** (sin cuerpos REF_).
4. Mover las pestañas `OLD …` a LG_HISTORICO si se quiere limpiar (o borrarlas a mano).

## Piezas

| Orden | Archivo | Reemplaza a | Qué cambió | Volumen |
|---|---|---|---|---|
{chr(10).join(rows)}
| {len(rows) + 1} | `00_ENSAMBLE.step` | Assembly / Part Studio `00_ENSAMBLE` | conjunto con las piezas de arriba | {n_sol} sólidos |

Los planos A4 de estas piezas ya están hechos en local con el formato del equipo, en
`04_Planos/PLANOS_A4_LanternGuard_v6.pdf` (Drive).
"""
    (IMP / "IMPORTAR.md").write_text(md, encoding="utf-8")
    print(IMP, len(rows), "piezas +", n_sol, "sólidos en el ensamble")


def planos(ch):
    import planos_piezas as PP
    LOCAL6.mkdir(parents=True, exist_ok=True)
    by = pieces()
    over = {}
    for code, *_ in ch:
        stp, q = by[code]
        pdf, sc, notes = PP.sheet_equipo(code, stp, q, LOCAL6, FECHA, P.chamfer_for(code))
        over[code] = (pdf, "Local (05/11, pieza cambiada)", sc)
        print("plano", code, sc)
    return Q.unir("v6", over)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cambiadas", action="store_true")
    ap.add_argument("--importar", action="store_true")
    ap.add_argument("--planos", action="store_true")
    a = ap.parse_args()
    ch = cambiadas()
    for c in ch:
        print(c[0], "|", c[1])
    if a.importar:
        importar(ch)
    if a.planos:
        planos(ch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
