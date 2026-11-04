"""04/11/2026 batch: retire the replaced tabs of LG_IMPRIMIR_P2 to LG_HISTORICO and draw the new pieces (A4, team format).

    python planos_0411.py --retirar boya|nodo      # copy the Part Studio to LG_HISTORICO, rename old tabs "OLD ..."
    python planos_0411.py --dibujar boya|nodo|<code,code>
    python planos_0411.py --melissa                 # export her drawings of the unchanged pieces
    python planos_0411.py --unir                    # merge v4

Batched version of onshape_historico.retire: one listing, constant Name property id, no organize, no DELETE (403):
copy of the Part Studio (1 call) + rename of the copy (1) + rename of the original and its .step blob in place (1 each).
"""
import argparse
import json
import sys
import time

import onshape_sync as OS
import planos_onshape as P

FECHA = "2026-11-04"
BUOY = ["B1_casco", "B2_cubierta_lisa", "B2_cubierta_mastil", "B3_caja", "B4_tapa", "B5_cuna_base", "B5_cuna_cuello", "B6_correa"]
BUOY_NEW = [c for c in BUOY if c != "B4_tapa"]                          # B4 did not change
NODE = ["M1s_caja_cuerpo", "M3s_riel_gancho", "M5s_capsula_tapa_pie", "M11_bandeja", "M11_bandeja_sup", "M4_capsula_cuerpo"]
# tab to retire -> reason
RETIRE = {"boya": {"B1_casco": "partida en mitades", "B2_cubierta": "partida en mitades", "B5_cuna": "partida en mitades",
                   "B3_caja": "postes Ø9 y cama útil 230", "B6_correa": "cama útil 230"},
          "nodo": {k: "riel cerrado estanco" for k in NODE}}
STATE = P.OUT / "retirados_0411.json"
UNCHANGED = {code: (P.OUT_A4 / f"PLANO_A4_{code}.pdf", "plano A4 del 31/10") for code in ("B4_tapa", "M2_caja_tapa", "M3t_tapa_bolsillo", "M6_capsula_bisel")}
UNCHANGED["SKIN_concha"] = (P.OUT_A4 / "PLANO_A4_SKIN_concha_v1.pdf", "plano A4 del 31/10")


def retire(c, ctx, which):
    R = P.reg()
    did, wid = R["documento"]["did"], R["documento"]["wid"]
    hist = OS.read_json(P.OP.DOCS, {})["LG_HISTORICO"]
    st = OS.read_json(STATE, {})
    for tab, motivo in RETIRE[which].items():
        if tab in st:
            continue
        by_name = {n: i for i, n in ctx["elements"].items()}
        studio, blob = by_name.get(tab), by_name.get(tab + ".step")
        rec = {"motivo": motivo, "estudio": studio, "blob": blob}
        new = f"OLD {FECHA} {tab} ({motivo})"
        if studio:
            r = c.call("POST", f"/elements/copyelement/{hist['did']}/workspace/{hist['wid']}",
                       {"documentIdSource": did, "workspaceIdSource": wid, "elementIdSource": studio, "isWorkspace": True})
            neid = r.get("id") or r.get("elementId")
            c.call("POST", f"/metadata/d/{hist['did']}/w/{hist['wid']}/e/{neid}", {"properties": [{"propertyId": ctx["name_pid"], "value": new}]})
            rec["copia_en_historico"] = neid
            c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{studio}", {"properties": [{"propertyId": ctx["name_pid"], "value": new}]})
            ctx["elements"][studio] = new
        if blob:
            c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{blob}", {"properties": [{"propertyId": ctx["name_pid"], "value": new + ".step"}]})
            ctx["elements"][blob] = new + ".step"
        rec["nuevo_nombre"] = new
        st[tab] = rec
        OS.write_json(STATE, st)
        print("retirado", tab, "->", new)


def reset_rec(code):
    """The registry entry of a piece whose tabs were retired starts again (the old one is kept under 'antes')."""
    R = P.reg()
    old = R.setdefault("piezas", {}).pop(code, None)
    old2 = R["piezas"].pop(code + "_v2", None)
    if old or old2:
        R.setdefault("antes_0411", {})[code] = {"base": old, "v2": old2}
    save = P.save
    save(R)


def draw(c, ctx, codes):
    by = {cd: (st, q) for cd, st, q in P.a4_pieces()}
    for code in codes:
        R = P.reg()
        rec = R.get("piezas", {}).get(code, {})
        if rec.get("a4", {}).get("pdf") and rec.get("hecho_0411"):
            continue
        if not rec.get("hecho_0411") and "inicio_0411" not in rec:
            reset_rec(code)
            R = P.reg()
            R.setdefault("piezas", {})[code] = {"inicio_0411": time.strftime("%Y-%m-%dT%H:%M")}
            P.save(R)
        step, q = by[code]
        try:
            a4 = P.piece_a4(code, step, q, c, ctx)
        except (OS.OnshapeError, KeyError, IndexError, StopIteration) as e:
            print(code, "FALLO:", str(e)[:300])
            continue
        R = P.reg()
        R["piezas"][code]["hecho_0411"] = True
        P.save(R)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--retirar")
    ap.add_argument("--dibujar")
    ap.add_argument("--unir", action="store_true")
    a = ap.parse_args()
    P.use_format("equipo")
    c = P.client() if (a.retirar or a.dibujar) else None
    ctx = P.a4_context(c) if (a.retirar or a.dibujar) else None
    if a.retirar:
        retire(c, ctx, a.retirar)
    if a.dibujar:
        codes = {"boya": BUOY_NEW, "nodo": NODE}.get(a.dibujar) or a.dibujar.split(",")
        draw(c, ctx, codes)
    if a.unir:
        P.merge_a4(UNCHANGED, "v4")


if __name__ == "__main__":
    sys.exit(main())
