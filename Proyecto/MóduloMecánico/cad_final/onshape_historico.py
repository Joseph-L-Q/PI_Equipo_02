"""Naming convention (2026-11-04): the current tab has no suffix (B1_casco, PLANO_A4_B1_casco); what it replaces is
copied to the document LG_HISTORICO as "OLD <date> <piece> (<reason>)" and deleted from the working document.

    python onshape_historico.py --doc LG_IMPRIMIR_P2 --tab B2_cubierta.step --fecha 2026-11-01 --motivo "sin chaflan"
    python onshape_historico.py --renombrar LG_IMPRIMIR_P2 B2_cubierta_v2 B2_cubierta
    python onshape_historico.py --listar LG_IMPRIMIR_P2

Copy: POST /elements/copyelement/{did}/workspace/{wid} (copyElementFromSourceDocument). If the API refuses the copy,
the tab is renamed "OLD ..." in place and left for a manual move (printed, and returned as "a_mano").
Rename: POST /metadata/d/{did}/w/{wid}/e/{eid} with the Name property. Deletion: DELETE /elements/d/{did}/w/{wid}/e/{eid}
(Onshape keeps it in the document history, so it can be restored from there).
"""
import argparse

import onshape_push as PU
import onshape_sync as OS

HIST = "LG_HISTORICO"


def elements(c, doc):
    d = OS.read_json(PU.DOCS, {})[doc]
    return d, {e["name"]: e for e in PU.tabs(c, d["did"], d["wid"])}


def name_pid(c, d, eid):
    m = c.call("GET", f"/metadata/d/{d['did']}/w/{d['wid']}/e/{eid}")
    return next(p["propertyId"] for p in m["properties"] if p.get("name") == "Name")


def rename(c, doc, old, new):
    d, el = elements(c, doc)
    eid = el[old]["id"]
    c.call("POST", f"/metadata/d/{d['did']}/w/{d['wid']}/e/{eid}", {"properties": [{"propertyId": name_pid(c, d, eid), "value": new}]})
    return eid


def historico(c):
    d = PU.ensure_document(c, HIST)
    PU.organize(c, HIST, "Pestañas reemplazadas: 'OLD <fecha> <pieza> (<motivo>)'. Lo vigente está en LG_IMPRIMIR_P2 sin sufijo.")
    return d


def retire(c, doc, tab, fecha, motivo, delete=True):
    """Copies tab to LG_HISTORICO as OLD ..., then deletes it from doc. Returns (new_name, 'copiado'|'a_mano')."""
    src, el = elements(c, doc)
    e = el[tab]
    piece = tab.rsplit(".", 1)[0] if tab.lower().endswith((".step", ".stp")) else tab
    new = f"OLD {fecha} {piece} ({motivo})"
    h = historico(c)
    try:
        r = c.call("POST", f"/elements/copyelement/{h['did']}/workspace/{h['wid']}",
                   {"documentIdSource": src["did"], "workspaceIdSource": src["wid"], "elementIdSource": e["id"], "isWorkspace": True})
        eid = r.get("id") or r.get("elementId")
        c.call("POST", f"/metadata/d/{h['did']}/w/{h['wid']}/e/{eid}", {"properties": [{"propertyId": name_pid(c, h, eid), "value": new}]})
    except OS.OnshapeError as err:
        print(f"  la API no copió {tab} ({str(err)[:120]}): se renombra en {doc} para moverla a mano")
        rename(c, doc, tab, new)
        return new, "a_mano"
    if delete:
        try:
            c.call("DELETE", f"/elements/d/{src['did']}/w/{src['wid']}/e/{e['id']}")
        except OS.OnshapeError as err:          # the API key has no delete scope (403): rename in place, delete by hand
            print(f"  copiado, pero la API no borra en {doc} ({str(err)[:60]}): queda como '{new}' para borrarla a mano")
            rename(c, doc, tab, new)
            return new, "copiado_borrar_a_mano"
    return new, "copiado"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc")
    ap.add_argument("--tab")
    ap.add_argument("--fecha")
    ap.add_argument("--motivo")
    ap.add_argument("--renombrar", nargs=3, metavar=("DOC", "VIEJO", "NUEVO"))
    ap.add_argument("--listar")
    a = ap.parse_args()
    c = OS.Client()
    if a.listar:
        for n, e in elements(c, a.listar)[1].items():
            print(e["elementType"][:10], n, e["id"])
    elif a.renombrar:
        print(rename(c, *a.renombrar))
    else:
        print(retire(c, a.doc, a.tab, a.fecha, a.motivo))


if __name__ == "__main__":
    main()
