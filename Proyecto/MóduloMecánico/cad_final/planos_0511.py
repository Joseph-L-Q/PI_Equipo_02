"""04/11/2026 (night) batch, block 2.1: replace the Part Studios of LG_IMPRIMIR_P2 with the current STEP, put the
positioned assembly in 00_ENSAMBLE, draw as many A4 sheets as the API budget allows and merge the v5 PDF.

    python planos_0511.py --subir            # retire (rename in place) + lean upload of every changed piece
    python planos_0511.py --ensamble         # 00_ENSAMBLE: node + buoy pieces, no REF_ bodies
    python planos_0511.py --dibujar M1s_caja_cuerpo,M3s_riel_gancho   # old drawing -> OLD, new PLANO_A4_<code>
    python planos_0511.py --cambios          # CAMBIOS pdf into LG_00_LEER_PRIMERO (1 call)
    python planos_0511.py --unir             # PLANOS_A4_LanternGuard_v5.pdf (cover + every current piece)
    python planos_0511.py --cuenta

Budget: every API call goes through a guard that stops at STOP billed calls of the year (2420). Lean upload: the
history copy of planos_0411 (2 extra calls per tab) is skipped, the OLD tab stays in the document itself, and the
listing, parts and properties calls are made only for the pieces that get a drawing.
"""
import argparse
import json
import sys
from pathlib import Path
import time

import onshape_push as OP
import onshape_sync as OS
import planos_onshape as P

FECHA = "2026-11-04"
STOP = 2420
STATE = P.OUT / "estado_0511.json"
P2S = P.P2 / "step"
BOYA_S = P.BOYA / "step"
M3F = ("M3f_marco_bolsillo", P2S / "M3f_marco_bolsillo.step", None, 2)
NODE_CHANGED = ["M1s_caja_cuerpo", "M2_caja_tapa", "M3s_riel_gancho", "M3t_tapa_bolsillo", "M3f_marco_bolsillo",
                "M4_capsula_cuerpo", "M5s_capsula_tapa_pie", "M11_bandeja", "M11_bandeja_sup"]
BUOY_CHANGED = ["B1_casco", "B2_cubierta_lisa", "B2_cubierta_mastil", "B3_caja", "B4_tapa", "B5_cuna_base",
                "B5_cuna_cuello", "B6_correa"]
UPLOAD = NODE_CHANGED + BUOY_CHANGED          # M6_capsula_bisel: the STEP only changed its OCC stamp
PRIORITY = ["M1s_caja_cuerpo", "M3s_riel_gancho", "M3f_marco_bolsillo", "M2_caja_tapa", "M4_capsula_cuerpo", "B1_casco",
            "B2_cubierta_lisa", "B2_cubierta_mastil", "B5_cuna_base", "B5_cuna_cuello", "B3_caja", "B4_tapa",
            "M5s_capsula_tapa_pie", "M11_bandeja", "M11_bandeja_sup", "M3t_tapa_bolsillo", "B6_correa", "M6_capsula_bisel"]


def setup():
    """Registers M3f in the piece lists of planos_onshape, lifts its quota guards and wraps the client call."""
    if not any(p[0] == "M3f_marco_bolsillo" for p in P.PIECES):
        P.PIECES.append((M3F[0], M3F[1], P.P2 / "stl" / "M3f_marco_bolsillo.stl", M3F[3]))
        i = P.A4_ORDER.index("M3t_tapa_bolsillo") + 1
        P.A4_ORDER.insert(i, "M3f_marco_bolsillo")
    P.LIMIT_A4 = STOP
    P.LIMIT = STOP
    P.use_format("equipo")
    orig = OS.Client.call

    def guarded(self, method, path, body=None, content_type="application/json"):
        if OS.year_total() >= STOP:
            raise SystemExit(f"presupuesto: {OS.year_total()} llamadas facturadas (tope {STOP}); paro")
        return orig(self, method, path, body, content_type)
    OS.Client.call = guarded


def st():
    return OS.read_json(STATE, {})


def put(s):
    OS.write_json(STATE, s)


def rename(c, did, wid, eid, pid, name):
    c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{eid}", {"properties": [{"propertyId": pid, "value": name}]})


# ---------------------------------------------------------------- 1. Part Studios
def subir(c, ctx):
    R = P.reg()
    did, wid = R["documento"]["did"], R["documento"]["wid"]
    s = st()
    steps = {c_: stp for c_, stp, _, _ in P.PIECES}
    by_name = {n: i for i, n in ctx["elements"].items()}
    for code in UPLOAD:
        rec = s.setdefault(code, {})
        if rec.get("subido"):
            continue
        old, oldblob = by_name.get(code), by_name.get(code + ".step")
        if old and "retirado" not in rec:
            new = f"OLD {FECHA} {code} (geometría anterior)"
            rename(c, did, wid, old, ctx["name_pid"], new)
            if oldblob:
                rename(c, did, wid, oldblob, ctx["name_pid"], new + ".step")
            rec["retirado"] = {"estudio": old, "blob": oldblob, "nombre": new}
            put(s)
        body, ctype = OS.multipart({"encodedFilename": f"{code}.step", "translate": "true", "storeInDocument": "true",
                                    "importWithinDocument": "true", "yAxisIsUp": "false", "flattenAssemblies": "false"}, steps[code])
        r = c.call("POST", f"/blobelements/d/{did}/w/{wid}", body, ctype)
        t = c.wait_translation(r["translationId"])
        if t.get("requestState") != "DONE":
            rec["fallo"] = f"{t.get('requestState')}: {t.get('failureReason')}"
            put(s)
            print(code, "FALLO", rec["fallo"])
            continue
        rec.update(subido=True, blob=r["id"], estudio=t["resultElementIds"][0])
        rec.pop("fallo", None)
        put(s)
        print("subido", code, rec["estudio"], "año:", OS.year_total())


# ---------------------------------------------------------------- 2. assembly
BUOY_DX = 700.0      # mm: the buoy is moved in +X next to the node (node x -215..215, buoy x -248..248)


def build_assembly(dst):
    """Node (ensamble_simple_D200) + buoy (ENSAMBLE_boya_pet) in one STEP, without REF_/ref_ bodies. Both keep their own
    frames; the buoy is moved BUOY_DX in +X (REF_boya of the node is only a 210x140x76 box, not a mooring frame).
    Returns the list of (name, solids). Names come from the XCAF labels of the sources."""
    import cadquery as cq
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.STEPCAFControl import STEPCAFControl_Reader
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.TDataStd import TDataStd_Name
    from OCP.TDF import TDF_LabelSequence, TDF_Label
    from OCP.TDocStd import TDocStd_Document
    from OCP.TopLoc import TopLoc_Location
    from OCP.XCAFApp import XCAFApp_Application
    from OCP.XCAFDoc import XCAFDoc_DocumentTool

    def name_of(lab):
        a = TDataStd_Name()
        return a.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), a) else ""

    def leaves(stool, lab, loc, out):
        if stool.IsAssembly_s(lab):
            comps = TDF_LabelSequence()
            stool.GetComponents_s(lab, comps)
            for i in range(1, comps.Length() + 1):
                cl = comps.Value(i)
                ref = TDF_Label()
                stool.GetReferredShape_s(cl, ref)
                leaves(stool, ref, loc.Multiplied(stool.GetLocation_s(cl)), out)
        else:
            out.append((name_of(lab), stool.GetShape_s(lab).Moved(loc)))

    items = []
    for path, dx in ((P.P2 / "ensamble_simple_D200.step", 0.0), (P.BOYA / "ENSAMBLE_boya_pet.step", BUOY_DX)):
        app = XCAFApp_Application.GetApplication_s()
        doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF"))
        app.NewDocument(TCollection_ExtendedString("MDTV-XCAF"), doc)
        rd = STEPCAFControl_Reader()
        rd.SetNameMode(True)
        if rd.ReadFile(str(path)) != IFSelect_RetDone or not rd.Transfer(doc):
            raise RuntimeError(f"no leo {path}")
        stool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
        roots = TDF_LabelSequence()
        stool.GetFreeShapes(roots)
        got = []
        for i in range(1, roots.Length() + 1):
            leaves(stool, roots.Value(i), TopLoc_Location(), got)
        for nm, sh in got:
            if nm.lower().startswith("ref_"):
                continue
            items.append((nm, cq.Shape.cast(sh).moved(cq.Location(cq.Vector(dx, 0, 0)))))
    if dst is not None:
        asm = cq.Assembly(name="LG_ensamble")
        for nm, sh in items:
            asm.add(sh, name=nm)
        asm.export(str(dst))
    return items


def solids_of(sh):
    from OCP.TopAbs import TopAbs_SOLID
    from OCP.TopExp import TopExp_Explorer
    e, n = TopExp_Explorer(sh, TopAbs_SOLID), 0
    while e.More():
        n += 1
        e.Next()
    return n


def dibujar(c, ctx, codes):
    by = {cd: (stp, q) for cd, stp, q in P.a4_pieces()}
    s = st()
    for code in codes:
        R = P.reg()
        did, wid = R["documento"]["did"], R["documento"]["wid"]
        rec = R.get("piezas", {}).get(code, {})
        if rec.get("hecho_0511") and rec.get("a4", {}).get("pdf"):
            continue
        sr = s.get(code, {})
        if not sr.get("estudio"):
            print(code, "sin Part Studio nuevo: no dibujo")
            continue
        if not rec.get("inicio_0511"):
            old_eid = next((i for i, n in ctx["elements"].items() if n == f"PLANO_A4_{code}"), None)
            if old_eid:
                new = f"OLD {FECHA} PLANO_A4_{code} (geometría anterior)"
                rename(c, did, wid, old_eid, ctx["name_pid"], new)
                ctx["elements"][old_eid] = new
            R.setdefault("antes_0511", {})[code] = rec
            R.setdefault("piezas", {})[code] = {"partstudio": sr["estudio"], "pestana": code, "inicio_0511": time.strftime("%Y-%m-%dT%H:%M"),
                                                "dibujo_anterior": old_eid}
            P.save(R)
        stp, q = by[code]
        try:
            P.piece_a4(code, stp, q, c, ctx)
        except (OS.OnshapeError, KeyError, IndexError, StopIteration) as e:
            print(code, "FALLO:", str(e)[:300])
            continue
        R = P.reg()
        R["piezas"][code]["hecho_0511"] = True
        P.save(R)


def ensamble(c, ctx):
    R = P.reg()
    did, wid = R["documento"]["did"], R["documento"]["wid"]
    s = st()
    if s.get("ensamble", {}).get("verificado"):
        return
    dst = P.OUT / "00_ENSAMBLE.step"
    items = build_assembly(dst)
    from checks import fix_step_stamp
    fix_step_stamp(dst)
    names, local = OP.step_parts(dst)
    rec = s.setdefault("ensamble", {"solidos_step": local, "piezas": [n for n, _ in items]})
    if "estudio" not in rec:
        for eid, nm in ctx["elements"].items():
            if nm in ("00_ENSAMBLE", "00_ENSAMBLE.step"):
                rename(c, did, wid, eid, ctx["name_pid"], f"OLD {FECHA} {nm} (ensamble anterior)")
        body, ctype = OS.multipart({"encodedFilename": "00_ENSAMBLE.step", "translate": "true", "storeInDocument": "true",
                                    "importWithinDocument": "true", "yAxisIsUp": "false", "flattenAssemblies": "true"}, dst)
        r = c.call("POST", f"/blobelements/d/{did}/w/{wid}", body, ctype)
        t = c.wait_translation(r["translationId"])
        rec.update(blob=r["id"], estado=t.get("requestState"), resultado=t.get("resultElementIds"), fallo=t.get("failureReason"))
        put(s)
        if t.get("requestState") != "DONE":
            print("ENSAMBLE FALLO", rec)
            return
        rec["estudio"] = t["resultElementIds"][0]
        put(s)
    parts = c.call("GET", f"/parts/d/{did}/w/{wid}/e/{rec['estudio']}")
    rec["solidos_onshape"] = len(parts)
    rec["nombres_onshape"] = [p.get("name") for p in parts]
    rec["verificado"] = True
    put(s)
    print("00_ENSAMBLE: Onshape", len(parts), "partes; STEP", local, "solidos")


LOCAL = ["M5s_capsula_tapa_pie", "M11_bandeja", "M11_bandeja_sup", "M3t_tapa_bolsillo", "B6_correa"]
LOCAL_DIR = P.OUT / "pdf_a4_local"
M6_OLD = P.OUT_A4 / "PLANO_A4_M6_capsula_bisel.pdf"          # STEP only changed its OCC stamp: the 31/10 sheet still holds


def locales(codes):
    import planos_piezas as PP
    by = {cd: (stp, q) for cd, stp, q in P.a4_pieces()}
    s = st()
    for code in codes:
        if s.get("local", {}).get(code):
            continue
        stp, q = by[code]
        pdf, sc, notes = PP.sheet_equipo(code, stp, q, LOCAL_DIR, FECHA, P.chamfer_for(code))
        s.setdefault("local", {})[code] = {"pdf": str(pdf.relative_to(P.MOD)), "escala": sc, "notas": notes}
        put(s)
        print("local", code, sc)


def cotas_a_mano():
    """{piece: text} from docs/COTAS_A_MANO.md (the other agent's list; the v4 file if it is missing)."""
    import re
    f = P.MOD / "docs" / "COTAS_A_MANO.md"
    if not f.exists():
        f = P.OUT / "COTAS_A_MANO_A4_v4.md"
    out, cur = {}, []
    for ln in f.read_text(encoding="utf-8").splitlines():
        if ln.startswith("#"):
            cur = re.findall(r"\b(?:[BM]\d+[a-z]?_[A-Za-z0-9_]+|SKIN_concha)\b", ln.split(":")[0]) if ln.startswith("###") else []
            for cd in cur:
                out.setdefault(cd, [])
        elif cur and ln.startswith("- "):
            for cd in cur:
                out[cd].append(re.sub(r"\*\*", "", ln[2:]))
    return {k: " · ".join(v) for k, v in out.items()}, f.name


def unir(tag="v5", override=None):
    """override: {code: (pdf, origen, escala)} wins over every other source (used by publicar_sin_api.py for v6)."""
    import html
    import subprocess
    import tempfile
    from pypdf import PdfReader, PdfWriter
    from entrega_pdf import EDGE
    R = P.reg()
    s = st()
    mano, fuente = cotas_a_mano()
    rows, files = [], []
    for code, stp, q in P.a4_pieces():
        if code.startswith("SKIN"):
            continue
        rec = R.get("piezas", {}).get(code, {})
        a4 = rec.get("a4", {})
        if override and code in override:
            f, origen, esc = override[code]
        elif rec.get("hecho_0511") and a4.get("pdf"):
            f, origen, esc = P.MOD / a4["pdf"], "Onshape (nuevo 04/11)", {"2:5": "1:2,5"}.get(a4.get("escala"), a4.get("escala", "-"))
        elif s.get("local", {}).get(code):
            l = s["local"][code]
            f, origen, esc = P.MOD / l["pdf"], "Local (cuota API)", l["escala"]
        elif code == "M6_capsula_bisel" and M6_OLD.exists():
            f, origen, esc = M6_OLD, "Onshape (plano del 31/10, sin cambios)", "1:1"
        else:
            f, origen, esc = None, "no generado", "-"
        ok = f is not None and Path(f).exists()
        if ok:
            files.append(f)
        txt = mano.get(code, "ver COTAS_A_MANO")
        txt = (txt[:330] + "…") if len(txt) > 330 else txt
        rows.append(f"<tr><td class=c>{len(files) + 1 if ok else '-'}</td><td><b>{html.escape(code)}</b></td><td class=c>{q}</td>"
                    f"<td>{html.escape(origen)}</td><td class=c>{esc}</td><td>{html.escape(txt)}</td></tr>")
    page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@page {{ size: A4 landscape; margin: 8mm; }}
body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 7pt; color: #1b1b1b; }}
h1 {{ font-size: 16pt; margin: 0; }} .sub {{ font-size: 8.5pt; color: #444; margin: 2pt 0 6pt; }}
table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid #bbb; padding: 1.5pt 3pt; vertical-align: top; }}
th {{ background: #e8eef3; text-align: left; }} .c {{ text-align: center; }} tr {{ page-break-inside: avoid; }}
</style></head><body>
<h1>LANTERNGUARD · planos de fabricación {tag} (formato del equipo)</h1>
<div class="sub">Equipo 02 UPCH · PETG · ISO A4 horizontal, primer diedro, cotas en mm · {time.strftime('%d/%m/%Y')} · hoja 1 = esta portada ·
Onshape LG_IMPRIMIR_P2: {html.escape(R['documento']['url'])} · Los planos «Local» se generaron desde el STEP con el script del repo
(cuota de la API de Onshape agotada); los de Onshape se pueden completar a mano. Lista de cotas a mano: <b>docs/{html.escape(fuente)}</b>.</div>
<table><tr><th>Hoja</th><th>Pieza</th><th>Cant.</th><th>Origen</th><th>Escala</th>
<th>Cotas que faltan a mano (de {html.escape(fuente)})</th></tr>{''.join(rows)}</table>
</body></html>"""
    tmp = Path(tempfile.mkdtemp(prefix=f"portada_{tag}_"))
    (tmp / "p.html").write_text(page, encoding="utf-8")
    cover = P.OUT / f"portada_A4_{tag}.pdf"
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={tmp / 'perfil'}", "--no-pdf-header-footer",
                    f"--print-to-pdf={cover}", (tmp / "p.html").as_uri()], capture_output=True, timeout=180)
    w = PdfWriter()
    for f in [cover] + files:
        for pg in PdfReader(str(f)).pages:
            w.add_page(pg)
    out = P.OUT / f"PLANOS_A4_LanternGuard_{tag}.pdf"
    with open(out, "wb") as fh:
        w.write(fh)
    print(out, len(w.pages), "páginas;", len(files), "planos;", "portada:", len(PdfReader(str(cover)).pages), "pág.")
    return out


def cambios(c):
    """docs/CAMBIOS.md -> docs/CAMBIOS.pdf, and the PDF replaces the file of the CAMBIOS tab of LG_00_LEER_PRIMERO in place
    (blob update, translate=false): 2 calls (tab listing + upload)."""
    import entrega_pdf
    entrega_pdf.main(P.MOD / "docs" / "CAMBIOS.md")
    doc = OS.read_json(OP.DOCS, {})["LG_00_LEER_PRIMERO"]
    els = c.call("GET", f"/documents/d/{doc['did']}/w/{doc['wid']}/elements")
    tab = [e for e in els if "CAMBIOS" in e["name"].upper() and e.get("elementType") == "BLOB"]
    print("pestañas CAMBIOS:", [(e["name"], e["id"]) for e in tab])
    if len(tab) != 1:
        print("no hay exactamente una pestaña CAMBIOS: no subo (queda en PENDIENTES)")
        return
    pdf = P.MOD / "docs" / "CAMBIOS.pdf"
    body, ctype = OS.multipart({"encodedFilename": tab[0]["name"] if tab[0]["name"].lower().endswith(".pdf") else "CAMBIOS.pdf",
                                "translate": "false", "storeInDocument": "true"}, pdf)
    c.call("POST", f"/blobelements/d/{doc['did']}/w/{doc['wid']}/e/{tab[0]['id']}", body, ctype)
    s = st()
    s["cambios_tab"] = {"id": tab[0]["id"], "nombre": tab[0]["name"], "actualizada": True}
    put(s)
    print("CAMBIOS actualizada")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subir", action="store_true")
    ap.add_argument("--ensamble", action="store_true")
    ap.add_argument("--dibujar")
    ap.add_argument("--cambios", action="store_true")
    ap.add_argument("--unir", action="store_true")
    ap.add_argument("--locales", action="store_true")
    ap.add_argument("--cuenta", action="store_true")
    a = ap.parse_args()
    setup()
    if a.cuenta:
        print(OS.year_total())
        return 0
    n0 = OS.year_total()
    c = P.client() if (a.subir or a.dibujar or a.ensamble or a.cambios) else None
    ctx = P.a4_context(c) if (a.subir or a.dibujar or a.ensamble) else None
    if a.subir:
        subir(c, ctx)
    if a.ensamble:
        ensamble(c, ctx)
    if a.dibujar:
        dibujar(c, ctx, PRIORITY if a.dibujar == "todo" else a.dibujar.split(","))
    if a.cambios:
        cambios(c)
    if a.locales:
        locales(LOCAL)
    if a.unir:
        unir()
    print("llamadas facturadas:", n0, "->", OS.year_total())


if __name__ == "__main__":
    sys.exit(main())
