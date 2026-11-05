r"""Data half of the interactive 3D manual: docs/visor/datos.json + the two HTML files.

Regenerate everything with ONE command (from cad_final):

    ..\.venv\Scripts\python.exe visor.py && ..\.venv\Scripts\python.exe visor_datos.py

(visor.py already runs this file at its end. Run only `visor_datos.py` when the CAD did not change and you just
want fresh slicer / FEM / simulation numbers: it reads the sidecar salida/_tmp/visor_geometria.json written by visor.py
and takes about 5 s.)

Outputs, all in docs/visor/:
  datos.json                 everything the viewer shows except the geometry (pieces, seals, steps, print plan, tests, results)
  modelo.glb                 written by visor.py
  index.html                 three.js viewer that fetches datos.json + modelo.glb (serve the folder, e.g. python -m http.server)
  LanternGuard_visor.html    same viewer with GLB, JSON and result images embedded: opens with a double click (file://)

Sources, read at run time so a re-run follows the CAD: params.py (watertight print profile), guia_piezas.py (seal list, via
salida/guia_piezas/sellos.json and rasgos.json, GUIA_PIEZAS.md), ESTANQUEIDAD.md (sections 5-7), slicer.json of the node and the
buoy (grams, hours), salida/imprimir_hoy (plan_placas.json, lista.json), bitacora.hardware (screws, cord, PG7, silicone),
docs/resultados/resultados.json + images (simulation; missing -> "pendiente").
"""
import base64
import html
import json
import re
import sys
import time
from pathlib import Path

import visor as V

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
OUT = MOD / "docs" / "visor"
SAL = MOD / "salida"
TEMPLATE = HERE / "visor_template.html"
RESULT_DIR = MOD / "docs" / "resultados"
PRECIO_KG = 60.0            # soles per kg of PETG (owner's figure of ENTREGA_2026-11-04; params.py still says 90, see DECISIONES.md)
EMBED_LIMIT_MB = 15.0
OPEN_COST = "S/"

# ----------------------------------------------------------------------------- small helpers


def rj(p):
    return json.loads(Path(p).read_text(encoding="utf-8")) if Path(p).exists() else None


def md_inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def md_blocks(txt):
    """Tiny markdown -> list of blocks {t: h3|p|ol|ul|table, html/items/rows}. Enough for ESTANQUEIDAD.md."""
    out, lines, i = [], txt.splitlines(), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
        elif ln.startswith("###"):
            out.append(dict(t="h3", html=md_inline(ln.lstrip("# ").strip())))
            i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                c = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", x) for x in c):
                    rows.append([md_inline(x) for x in c])
                i += 1
            out.append(dict(t="table", rows=rows))
        elif re.match(r"\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                items.append(md_inline(re.sub(r"^\d+\. ", "", lines[i])))
                i += 1
            out.append(dict(t="ol", items=items))
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(md_inline(lines[i][2:]))
                i += 1
            out.append(dict(t="ul", items=items))
        else:
            out.append(dict(t="p", html=md_inline(ln)))
            i += 1
    return out


def md_section(txt, start_pat, end_pat=r"^## "):
    """Text between a heading matching start_pat and the next '## ' heading."""
    ls = txt.splitlines()
    a = next((i for i, l in enumerate(ls) if re.match(start_pat, l)), None)
    if a is None:
        return ""
    b = next((i for i in range(a + 1, len(ls)) if re.match(end_pat, ls[i])), len(ls))
    return "\n".join(ls[a + 1:b])


# ----------------------------------------------------------------------------- print data
ORIENT_ES = {
    "sin girar": "Como sale del modelo: la cara plana de abajo queda sobre la cama.",
    "ya orientada": "El archivo ya viene girado para imprimir; no la gire.",
}


def orient_text(o):
    if not o:
        return ""
    if o in ORIENT_ES:
        return ORIENT_ES[o]
    m = re.fullmatch(r"([XYZ])([+-]?\d+)", o)
    if m:
        ang = int(m.group(2))
        return f"Gírela {abs(ang)}° sobre el eje {m.group(1)} antes de ponerla en la cama (el archivo de la placa ya viene girado)."
    return o


PROBETAS_ES = {
    "PB7_peine_holguras": ("Peine de holguras", "Cuatro agujeros con juego distinto (0.2, 0.3, 0.4 y 0.5 mm). El pin que entra justo, sin bailar, fija la holgura que se usará en todas las piezas que encajan."),
    "PB7_pines": ("Pines del peine", "Los cuatro pines que se prueban en el peine; vienen unidos por una tira fina que hay que cortar antes."),
    "PB8_inserto_M4": ("Probeta del inserto M4", "Tres placas con un inserto roscado M4. Se tira de un perno hasta que el inserto se salga: dice cuánta fuerza aguanta de verdad."),
    "PB6_junta_base": ("Probeta de junta: base", "Caja plana de 60 × 60 con insertos M3 en las cuatro esquinas. Con su tapa y el cordón de goma es la prueba más barata de que la junta no deja pasar agua."),
    "PB6_junta_tapa": ("Probeta de junta: tapa", "Tapa con la misma ranura del cordón (2.6 × 1.5 mm) que usan las cajas. Sirve para ver si el cordón se aplasta bien y no se sale."),
    "PB10_gancho_tramo": ("Tramo del gancho", "Un tramo del gancho en C del riel, para probar cuánto aguanta antes de imprimir los rieles enteros."),
    "PB9_bahia_botella": ("Bahía de la botella", "Un trozo del casco con la bahía donde va la botella PET: se prueba que la botella entra y queda firme."),
}

TIPS_ESTANCA = [
    "Use el perfil de impresión estanco en estas piezas: 4 perímetros, 5 capas arriba y 5 abajo, relleno 100 %. Así las paredes y las zonas de junta quedan macizas.",
    "Seque el filamento antes de imprimir (varias horas a unos 60 °C). El PETG húmedo hace burbujas y burbujas son huecos por donde pasa el agua.",
    "No cambie de rollo ni de temperatura a la mitad de una pieza estanca; imprímala de una sola vez, sin pausas.",
    "No toque la cama ni el aire de la impresora durante las primeras capas: son las que quedan contra el agua.",
    "Al terminar, mire cada pieza contra una luz fuerte: si se ve luz a través de una pared, hay un hueco y se reimprime.",
    "Opcional: una capa de epoxi por dentro cierra poros pequeños. Hágalo solo si la prueba de agua falló, y cambie una sola cosa a la vez.",
]
TIPS_GENERALES = [
    "Una placa se imprime con un solo relleno y un solo ajuste de soportes; por eso las piezas están agrupadas por placas.",
    "Si una placa no cabe en la cama de la Bambu P1P (256 × 256 mm), no la fuerce: avise y se parte en dos.",
    "Quite los soportes con cuidado, sobre todo en roscas, ranuras de cordón y paredes finas.",
]

PRINT_GROUPS = {
    1: ("Probetas", "Primero, antes que nada: sirven para ajustar holguras, probar insertos y probar la junta. Con su resultado se corrigen las piezas finales."),
    2: ("Piezas que ya se pueden imprimir", "No dependen de ninguna medida pendiente: bisel, bandejas, tapas de bolsillo, cápsulas, tapa y caja del nodo."),
    3: ("Rieles (después de medir el aro)", "Los rieles se cuelgan del aro de la linterna: hay que medir el aro real antes de imprimirlos."),
    4: ("Boya", "Casco, cubiertas, caja seca con su tapa, cunas y correas."),
    5: ("Skin (la cubierta decorativa)", "Pendiente: todavía no está en el plan de impresión."),
}


def piece_key_from_file(fname, keys):
    m = re.match(r"^\d+_(.+?)_x(\d+)\.stl$", fname)
    if not m:
        return None, 1
    stem, qty = m.group(1), int(m.group(2))
    if stem in keys:
        return stem, qty
    code = re.match(r"([BM]\d+[a-z]?)_", stem)
    if code:
        c = [k for k in keys if k.startswith(code.group(1) + "_")]
        if len(c) == 1:
            return c[0], qty
        c2 = [k for k in c if k.endswith(stem.split("_", 1)[1]) or stem.split("_", 1)[1] in k]
        if len(c2) == 1:
            return c2[0], qty
    return None, qty


# ----------------------------------------------------------------------------- seals: commercial part / install / test
SEAL_KINDS = [
    ("pg7", lambda s: "prensaestopas" in s,
     dict(parte="Prensaestopas PG7 con contratuerca (agujero de Ø12.6 mm)",
          instalar=["Pase el cable por la tuerca de presión y por la goma del prensaestopas, antes de apretar nada.",
                    "Meta el cuerpo del prensaestopas por el agujero de la pieza, con su junta del lado de la pared, y ponga la contratuerca por dentro.",
                    "Apriete la contratuerca a mano y luego un cuarto de vuelta con llave. No lo apriete de más: el PETG se aplasta.",
                    "Apriete la tuerca de presión sobre el cable hasta que la goma lo abrace. Tire suave del cable: no debe deslizar."],
          probar=["Con el cable ya puesto, sumerja la pieza 30 minutos con papel seco dentro. Papel seco = sello bueno.",
                  "Si hay gotas junto al cable, revise que la goma sea para el grosor del cable (Ø5.5 mm)."])),
    ("ventana", lambda s: "ventana" in s,
     dict(parte="Anillo plano de silicona de 1 mm (Ø30 × Ø26.5) + silicona marina (cartucho de 70 mm, p. ej. Sikaflex-291i) + disco de acrílico Ø30 × 3",
          instalar=["Limpie y seque el asiento de la ventana en la cápsula.",
                    "Ponga el anillo de silicona en el asiento y encima el disco de acrílico.",
                    "Coloque el bisel M6 y apriete sus 3 tornillos M2 en cruz, de a poco: el anillo se comprime un 20 %.",
                    "Pase un cordón fino de silicona marina por el borde de la ventana y deje curar el tiempo que diga el cartucho."],
          probar=["Pruebe la cápsula sola (subconjunto A de la pestaña Pruebas): papel seco detrás de la ventana tras 30 minutos a 0.5 m.",
                  "Es un sello nuevo: esta prueba es la que confirma que el anillo y la silicona bastan."])),
    ("cordon_plano", lambda s: "plana" in s and "cordón" in s,
     dict(parte="Cordón de goma NBR de Ø2 mm, cortado a medida (unos 420 mm para los 4 sellos planos, con 10 % de sobra)",
          instalar=["Limpie la ranura: sin rebabas ni polvo.",
                    "Corte el cordón con un poco de sobra y colóquelo sin torcerlo ni estirarlo, siguiendo las esquinas redondeadas.",
                    "Debe asomar un poco sobre la ranura. Junte las puntas a tope en un lado recto, no en una esquina.",
                    "Apriete los tornillos en cruz y de a poco: primero medio apriete en todos, después el apriete final. El cordón se aplasta un 20 %."],
          probar=["Antes de sumergir, revise que el cordón no se plegó en las esquinas.",
                  "Pruebe el riel con su silla (subconjunto C) y luego el nodo completo (subconjunto D): 30 minutos y, si sale seco, 24 horas."])),
    ("oring", lambda s: "o-ring" in s or "oring" in s,
     dict(parte="Cordón de goma NBR de Ø2 mm en ranura de 2.6 × 1.5 mm, cortado a medida (no hace falta un O-ring cerrado)",
          instalar=["Limpie la ranura: sin rebabas ni polvo.",
                    "Coloque el cordón sin torcerlo; debe asomar un poco por encima de la ranura. Junte las puntas a tope.",
                    "Ponga la tapa y apriete los tornillos M3 en cruz, de a poco (medio apriete en todos y luego el final).",
                    "Pase una tira de papel por el camino del cable para ver que nada se haya atascado."],
          probar=["Papel de cocina seco adentro, nunca electrónica. Sumerja 30 minutos a 0.5 m, saque, seque por fuera y abra.",
                  "Si está seco, repita 24 horas. Si está mojado, la mancha señala el sello que falló."])),
    ("insertos", lambda s: "inserto" in s,
     dict(parte="Insertos roscados de latón M3 (Ø4.0 × 6) y M4 (Ø5.6), ciegos: no atraviesan la pared",
          instalar=["Caliente el soldador con punta para insertos (unos 230 °C para PETG).",
                    "Apoye el inserto en su agujero, recto, y presione sin golpear hasta que quede al ras de la superficie.",
                    "Déjelo enfriar sin tocarlo. Pruebe el tornillo a mano: debe entrar sin esfuerzo y sin que el inserto gire."],
          probar=["Imprima la probeta del inserto M4 (P02) y tire de un perno hasta que se salga: debe aguantar lo que pide la caja (unos 274 N por inserto).",
                  "Como son ciegos, no hay camino de agua por el tornillo: se comprueba mirando que ningún agujero atraviese la pared."])),
    ("botella", lambda s: "tapón" in s or "tapon" in s or "botella" in s,
     dict(parte="Botellas PET de gaseosa cerradas de fábrica, con su tapón de rosca (compradas)",
          instalar=["Use botellas limpias, secas y sin golpes, cerradas a mano hasta el tope.",
                    "Apóyelas en las cunas B5 y sujételas con las correas B6. No las abra después de la prueba."],
          probar=["Sumerja las botellas 24 horas con un peso encima: no deben soltar burbujas ni arrugarse.",
                  "Una botella aplastada o con burbujas en el tapón tiene fuga: se cambia, no se repara."])),
]


def seal_texts(s):
    low = (s["sello"] + " " + s["tipo"]).lower()
    for _, test, d in SEAL_KINDS:
        if test(low):
            return d
    return dict(parte="Ver la tabla de ESTANQUEIDAD.md", instalar=[], probar=[])


# ----------------------------------------------------------------------------- main
def piece_types(sl_node, sl_boya, lista):
    """{key: dict(g, h, qty, relleno, soportes, orient, paredes, estanca...)} from the two slicer.json (+ lista.json for orientation)."""
    tipos = {}
    for src, group in ((sl_node, "nodo"), (sl_boya, "boya")):
        for k, v in (src or {}).items():
            tipos[k] = dict(grupo=group, g=v.get("g"), h=v.get("h"), qty=v.get("qty"), relleno=v.get("relleno_pct"),
                            soportes=v.get("soportes"), orient=v.get("orientacion"))
    keys = list(tipos)
    for e in lista or []:
        k, qty = piece_key_from_file(e["archivo"], keys)
        if k:
            t = tipos[k]
            t["qty"] = t.get("qty") or qty
            t["orient"] = e.get("orient") or t.get("orient")
            t["paredes"] = e.get("paredes")
            t["estanca"] = e.get("estanca")
            if t.get("g") is None:
                t["g"], t["h"] = e.get("g"), e.get("h")
    return tipos


def main():
    t0 = time.time()
    geo = rj(V.SIDECAR)
    if not geo:
        sys.exit("falta " + str(V.SIDECAR) + ": corra primero  python visor.py")
    OUT.mkdir(parents=True, exist_ok=True)
    G = geo["piezas"]

    guia = V.parse_guia(V.GUIA_MD)
    rasgos = V.read_json(V.RASGOS)
    sellos_src = V.read_json(V.SELLOS_JSON)
    sellos_src = sellos_src if isinstance(sellos_src, list) else []
    seals_md, no_est, pend = V.parse_estanq(V.ESTANQ_MD, sellos_src)
    est_txt = V.ESTANQ_MD.read_text(encoding="utf-8") if V.ESTANQ_MD.exists() else ""
    sl_node, sl_boya = V.read_json(V.NODE_SLICER), V.read_json(V.BUOY_SLICER)
    lista = rj(SAL / "imprimir_hoy" / "lista.json") or []
    plan = rj(SAL / "imprimir_hoy" / "plan_placas.json") or {"placas": []}
    tipos = piece_types(sl_node, sl_boya, lista)

    # print profile for the watertight parts (read-only import of params)
    perfil = dict(perimetros=4, capas_arriba=5, capas_abajo=5, relleno=100, piezas=["M1s", "M2", "M3s", "M4", "M5s", "B3", "B4"])
    try:
        import params as PRM
        sp = PRM.SEAL_PRINT
        perfil = dict(perimetros=sp["perimetros"], capas_arriba=sp["capas_arriba"], capas_abajo=sp["capas_abajo"],
                      relleno=round(sp["relleno"] * 100), piezas=list(sp["piezas"]))
    except Exception as e:                          # noqa: BLE001
        print("params.SEAL_PRINT no disponible, perfil por defecto:", e)
    orca = sorted(p.stem.replace(".process", "").replace(".filament", "").replace(".machine", "") for p in (HERE / "orca").glob("*.json"))

    # ---- per-instance pieces
    names = list(G)
    count = {}
    for n, e in G.items():
        if e["kind"] == "impresa":
            count[e["key"]] = count.get(e["key"], 0) + 1
    piezas = {}
    for nm, e in G.items():
        kind, key = e["kind"], e["key"]
        if kind == "sello":
            s = next((x for x in sellos_src if x["n"] == e["n"]), {})
            piezas[nm] = dict(group=e["group"], kind="sello", code=nm, titulo=f"Sello {e['n']}: {s.get('sello', '')}", n=e["n"],
                              funcion=s.get("protege", ""), material="Cordón de goma / prensaestopas / silicona (comprado)",
                              offset=e["offset"], centro=e["centro"], host=e["host"], bbox=e["bbox"])
            continue
        gk = V.lookup(guia, key)
        ref_es = next((v for k, v in V.REF_ES.items() if nm.startswith(k)), None)
        side = V.side_of(nm)
        titulo = (guia[gk]["titulo"] if gk and kind == "impresa" else ref_es) or nm.replace("_", " ")
        info = dict(group=e["group"], kind=kind, code=key if kind == "impresa" else nm, titulo=titulo + (f" ({side})" if side else ""),
                    funcion=guia[gk]["funcion"] if gk and kind == "impresa" else (ref_es or "Pieza de referencia."),
                    material=V.material_of(nm, kind), offset=e["offset"], centro=e["centro"], bbox=e["bbox"])
        if kind == "impresa":
            t = tipos.get(V.lookup(tipos, key) or "", {})
            g, h = t.get("g"), t.get("h")
            qty = count.get(key, 1)
            info.update(g=None if g is None else round(float(g), 1), h=None if h is None else round(float(h), 2), qty=qty,
                        costo=None if g is None else round(float(g) * PRECIO_KG / 1000, 2),
                        relleno=t.get("relleno"), soportes=t.get("soportes"), paredes=t.get("paredes"), estanca=t.get("estanca"),
                        orient=orient_text(t.get("orient")))
            if V.JOINS.get(key):
                info["une"] = V.JOINS[key]
            rk = V.lookup(rasgos, key)
            rs = rasgos.get(rk, []) if rk else []
            pts = e.get("rasgos_pts", {})
            info["rasgos"] = [dict(n=r["n"], tipo=r["tipo"], diam=r.get("diam"), texto=r["texto"], cat=r.get("categoria"),
                                   cant=len(r.get("puntos") or [1]), pts=pts.get(str(r["n"]))) for r in rs]
            info["tornillos"] = [f"{r['tipo']}{' Ø' + str(r['diam']) if r.get('diam') else ''} ×{len(r.get('puntos') or [1])}"
                                 for r in rs if r.get("categoria") == "union"]
            info["insertos"] = [f"{r['tipo']} ×{len(r.get('puntos') or [1])}" for r in rs if "nserto" in r["tipo"]]
            info["marcas3d"] = bool(pts)
            if not rs:
                info["rasgos_nota"] = "Esta pieza todavía no tiene ficha de agujeros en la guía."
        elif nm.startswith("REF_lastre"):
            info.update(g=575.0, costo=None, nota_g="Peso del lastre de un bolsillo (tuercas y arandelas M8 a granel).")
        piezas[nm] = info

    # ---- seals
    seals = []
    for s in sellos_src:
        meshes = [k for k, v in piezas.items() if v["kind"] == "sello" and v.get("n") == s["n"]]
        txt = seal_texts(s)
        inst = sorted({n for n in names if G[n]["kind"] == "impresa" and any(n.startswith(p.split("_")[0] + "_") and V.base_key(n) == p for p in s["piezas"])})
        seals.append(dict(n=s["n"], sello=s["sello"], tipo=s["tipo"], protege=s["protege"], donde=s.get("donde", []), zona=s.get("zona"),
                          cant=s.get("cant", ""), partes=inst, mallas=meshes, comercial=txt["parte"], instalar=txt["instalar"],
                          probar=txt["probar"]))
    for p in piezas.values():
        if p["kind"] == "impresa":
            p["sellos"] = [s["n"] for s in seals if p.get("code") in [V.base_key(x) for x in s["partes"]]]
    for n, p in piezas.items():
        if p["kind"] != "impresa":
            p.setdefault("sellos", [])

    # ---- assembly steps
    steps, used = [], set()
    solid = [n for n in names if G[n]["kind"] != "sello"]
    for grp, tit, txt, pats in V.STEPS:
        ps = [n for n in solid if any(re.search(p, n) for p in pats) and n not in used]
        if ps:
            used.update(ps)
            steps.append(dict(titulo=tit, texto=txt, partes=ps, grupo=grp))
    rest = [n for n in solid if n not in used]
    if rest:
        steps.append(dict(titulo="Otras piezas", texto="Piezas nuevas que todavía no tienen paso propio en el visor.", partes=rest, grupo="nodo"))
    for i, st in enumerate(steps):
        sel = [n for n, p in piezas.items() if p["kind"] == "sello" and p["host"] in st["partes"]]
        st["sellos"] = sel
        crew, tor = [], []
        for n in st["partes"]:
            for r in piezas[n].get("rasgos", []):
                if r["cat"] == "union":
                    tor.append(dict(pieza=n, n=r["n"], tipo=r["tipo"], diam=r.get("diam"), cant=r["cant"], tiene3d=bool(r.get("pts"))))
        st["tornillos"] = tor
        for n in st["partes"] + sel:
            piezas[n]["paso"] = i

    # ---- hardware lists
    herraje = dict(nodo=[], boya=[])
    try:
        import bitacora as B
        res = rj(B.SAL / "simple" / "resultados.json")
        rb = rj(B.SAL / "simple" / "boya" / "resultados_boya.json")
        for grp, item, med, cant in B.hardware(res, rb):
            if grp == "nodo simple":
                herraje["nodo"].append(dict(item=item, medida=med, cant=cant))
    except Exception as e:                          # noqa: BLE001
        print("bitacora.hardware no disponible:", e)
        herraje["nodo_nota"] = "Lista de compra del nodo no disponible en esta corrida."
    agg, seen = {}, set()
    for n, p in piezas.items():
        if p["kind"] == "impresa" and p["group"] == "boya" and p["code"] not in seen:     # once per piece type
            seen.add(p["code"])
            for r in p["rasgos"]:
                if r["cat"] == "union" or "nserto" in r["tipo"]:
                    agg[(p["code"], r["tipo"])] = r["cant"]
    herraje["boya"] = [dict(item=f"{c} · {t}", medida="por pieza", cant=q) for (c, t), q in sorted(agg.items())]
    herraje["boya"] += [dict(item="Cordón de goma NBR Ø2 para la tapa B4", medida="según el perímetro de la brida", cant=1),
                        dict(item="Prensaestopas PG7 con contratuerca (umbilical, cable solar, antena)", medida="PG7", cant=3),
                        dict(item="Botellas PET cerradas (flotación)", medida="4 × 500 ml", cant=4)]

    # ---- print plan
    grupos = {}
    keys = list(tipos)
    for pl in plan.get("placas", []):
        gnum = pl.get("grupo", 2)
        items, gsum, hsum = [], 0.0, 0.0
        for path, qty in pl["piezas"]:
            fn = Path(path).name
            k, q = piece_key_from_file(fn, keys)
            stem = re.sub(r"^\d+_|_x\d+\.stl$", "", fn)
            t = tipos.get(k, {}) if k else {}
            li = next((x for x in lista if x["archivo"] == fn), {})
            g, h = (t.get("g") if t.get("g") is not None else li.get("g")), (t.get("h") if t.get("h") is not None else li.get("h"))
            pr = PROBETAS_ES.get(stem)
            items.append(dict(archivo=fn, codigo=k or stem, nombre=pr[0] if pr else (piezas.get(next((n for n in names if G[n].get("key") == k), ""), {}).get("titulo", stem) if k else stem),
                              nota=pr[1] if pr else "", cant=qty, g=g, h=h, orient=orient_text(li.get("orient") or t.get("orient")),
                              pendiente=g is None))
            if g is not None:
                gsum += g * qty
                hsum += (h or 0) * qty
        grupos.setdefault(gnum, []).append(dict(
            nombre=pl["nombre"], relleno=pl["relleno"], soportes=pl["soportes"], paredes=pl["paredes"], estanca=pl.get("estanca", False),
            piezas=items, g=round(gsum, 1), h=round(hsum, 2), costo=round(gsum * PRECIO_KG / 1000, 2),
            incompleta=any(i["pendiente"] for i in items)))
    impresion_grupos = []
    for gnum in sorted(set(grupos) | set(PRINT_GROUPS)):
        ttl, nota = PRINT_GROUPS.get(gnum, (f"Grupo {gnum}", ""))
        pls = grupos.get(gnum, [])
        impresion_grupos.append(dict(n=gnum, titulo=ttl, nota=nota, placas=pls, pendiente=not pls,
                                     g=round(sum(p["g"] for p in pls), 1), h=round(sum(p["h"] for p in pls), 1),
                                     costo=round(sum(p["costo"] for p in pls), 2)))
    # totals by group over the 3D pieces (qty x unit)
    tot = {"nodo": dict(g=0.0, h=0.0), "boya": dict(g=0.0, h=0.0)}
    for n, p in piezas.items():
        if p["kind"] == "impresa" and p.get("g") is not None:
            tot[p["group"]]["g"] += p["g"]
            tot[p["group"]]["h"] += p.get("h") or 0
    for v in tot.values():
        v["g"], v["h"] = round(v["g"]), round(v["h"], 1)
        v["costo"] = round(v["g"] * PRECIO_KG / 1000, 2)

    # ---- tests (ESTANQUEIDAD.md section 6 + the extras)
    sec6 = md_section(est_txt, r"^## 6\.")
    sec5 = md_section(est_txt, r"^## 5\.")
    sec7 = md_section(est_txt, r"^## 7\.")
    pruebas = dict(
        antes=[dict(t="p", html="Se prueba de lo pequeño a lo grande. Cada nivel solo se hace si el anterior salió <b>seco</b>."),
               dict(t="ol", items=[
                   "<b>Probeta de junta P03 (PB6).</b> Imprímala primero, con el perfil estanco. Ponga el cordón de Ø2 en la ranura, cierre con los 4 M3 y sumérjala 30 minutos a 1 m con papel seco dentro. Es la prueba más barata: si ella falla, ninguna caja va a aguantar.",
                   "<b>Cada volumen por separado</b> (cápsula, caja con tapa, riel con su silla): 30 minutos y luego 24 horas a 0.5 m, como dice la guía de abajo.",
                   "<b>El nodo completo</b> (caja + 2 rieles + 2 cápsulas) sin electrónica, y después la piscina con peso durante 2 horas.",
                   "Solo si todo está seco se monta la electrónica real."])],
        guia=md_blocks(sec6),
        imprimir=md_blocks(sec5),
        pendiente=md_blocks(sec7),
        comparar=[dict(t="p", html="Para saber si un cambio mejoró algo (otro filamento, otra temperatura, 4 o 5 perímetros), compare <b>dos impresiones de la misma probeta P03</b> haciendo cambiar <b>una sola cosa</b>."),
                  dict(t="ol", items=[
                      "Imprima las dos con el mismo rollo, la misma cama y el mismo día; marque cada una con un número.",
                      "Pese las dos: la más liviana tiene menos relleno real o más huecos.",
                      "Mírelas contra una luz fuerte: anote en cuál se ve luz a través de la pared.",
                      "Hágales la misma prueba de agua (misma profundidad, mismo tiempo, papel nuevo) y fotografíe el papel de cada una.",
                      "Anote fecha, qué cambió y el resultado. Quédese con la que salió seca; si salen iguales, con la más barata."])],
        mirar=[dict(t="ul", items=[
            "<b>Capas:</b> que no haya rendijas entre capas ni zonas con capas «sueltas» o con hilos. Una rendija entre capas es un camino para el agua.",
            "<b>Puentes y voladizos:</b> las partes que se imprimen en el aire (techos de las ranuras, agujeros horizontales) suelen quedar caídas o con huecos; ahí se fugan primero.",
            "<b>Roscas e insertos:</b> que el tornillo entre sin forzar, que el inserto no gire y que no haya burbujas alrededor.",
            "<b>Ranuras del cordón:</b> fondo liso, sin hilos ni rebabas; ancho y hondo como en el modelo (2.6 × 1.5 mm).",
            "<b>Esquinas:</b> sin separación de capas; un tornillo muy apretado en una esquina puede abrirla.",
            "<b>Contraluz:</b> pase una luz fuerte por detrás de cada pared; si se ve luz, hay un hueco y se reimprime."])])

    # ---- simulation results
    resultados = dict(disponible=False, casos=[], nota="Todavía no hay resultados de simulación publicados (docs/resultados/resultados.json).")
    rr = rj(RESULT_DIR / "resultados.json")
    meta = rj(RESULT_DIR / "meta.json") or {}
    if rr:
        casos = []
        for k, v in rr.items():
            imgs = {i: copy_image(RESULT_DIR / k / f"{i}.png", f"img/{k}_{i}.jpg") for i in ("vonmises", "desplazamiento", "condiciones", "malla")
                    if (RESULT_DIR / k / f"{i}.png").exists()}
            casos.append(dict(id=k, pieza=v.get("pieza", k), caso=v.get("caso"), titulo=v.get("titulo"), fuente=v.get("fuente"),
                              motivo=v.get("motivo_fuente"), sigma_max=v.get("sigma_max"), sigma_p995=v.get("sigma_p995"), fs=v.get("fs"),
                              fs_p995=v.get("fs_p995"), fs_capas=v.get("fs_capas"), fs_plano=v.get("fs_plano"), umax_mm=v.get("umax_mm"),
                              cumple=v.get("cumple"), link=v.get("link"), notas=v.get("notas", []), imagenes=imgs,
                              celdas=(v.get("malla") or {}).get("celdas")))
        casos.sort(key=lambda c: c["id"])
        resultados = dict(disponible=True, casos=casos, generado=meta.get("generado"), escalas=dict(vonmises=meta.get("escala_vonmises_MPa"),
                          desplazamiento=meta.get("escala_desplazamiento_mm")), convenciones=meta.get("convenciones"),
                          material=meta.get("material"))
    else:
        fem = rj(SAL / "prototipos" / "P2_robusto" / "fem" / "fem.json")
        if fem:
            casos = [dict(id=k, pieza=k, caso=k, titulo=f"Cálculo local (CalculiX): {k}", fuente="FEM local", fs=round(v["fs"], 2),
                          fs_capas=round(v["fs_capas"], 2), sigma_max=round(v["smax_abs"], 1), umax_mm=round(v["umax"], 2),
                          cumple=v["fs"] >= 1 and v["fs_capas"] >= 1, imagenes={}, notas=[], link=None) for k, v in fem["casos"].items()]
            resultados = dict(disponible=True, casos=casos, nota="Solo el cálculo local del nodo; faltan las simulaciones completas.")
    for p in piezas.values():
        if p["kind"] == "impresa":
            cs = [c for c in resultados["casos"] if c["pieza"] == p["code"] or c["id"].startswith(p["code"])]
            p["resultados"] = [c["id"] for c in cs]

    datos = dict(version=1, generado=geo.get("generado"), generado_datos=time.strftime("%d/%m/%Y %H:%M"), fuentes=geo.get("fuentes"),
                 precio_kg=PRECIO_KG, piezas=piezas, sellos=seals, sellos_sin_3d=geo.get("sellos_sin_3d", []),
                 no_estanco=no_est, pendiente=pend, pasos=steps, herraje=herraje, totales=tot,
                 impresion=dict(grupos=impresion_grupos, perfil_estanco=perfil, perfiles_orca=orca, tips_estanca=TIPS_ESTANCA,
                                tips_generales=TIPS_GENERALES, probetas=PROBETAS_ES and {k: dict(nombre=v[0], texto=v[1]) for k, v in PROBETAS_ES.items()}),
                 pruebas=pruebas, resultados=resultados)
    (OUT / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    write_html(datos)
    print(f"datos.json {(OUT / 'datos.json').stat().st_size / 1e3:.0f} kB · {len(piezas)} meshes · {len(seals)} sellos · {len(steps)} pasos · "
          f"{len(resultados['casos'])} casos de simulación · {time.time() - t0:.0f}s", flush=True)


def copy_image(src, rel, maxpx=900, q=78):
    """Recompress a simulation PNG to a JPEG inside docs/visor/img so the viewer folder is self-contained. Returns the relative path."""
    from PIL import Image
    dst = OUT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or dst.stat().st_mtime < Path(src).stat().st_mtime:
        im = Image.open(src).convert("RGB")
        im.thumbnail((maxpx, maxpx))
        im.save(dst, "JPEG", quality=q, optimize=True)
    return rel


def jpeg_data_uri(path):
    return "data:image/jpeg;base64," + base64.b64encode(Path(path).read_bytes()).decode("ascii")


THREE_URL = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
THREE_TAG = '<script src="' + THREE_URL + '" id="three-cdn"></script>'


def three_source():
    """three.js r128 text (cached in salida/_tmp) so the single-file version also works offline; None if it cannot be had."""
    cache = SAL / "_tmp" / "three.r128.min.js"
    if not cache.exists():
        try:
            import urllib.request
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(urllib.request.urlopen(THREE_URL, timeout=30).read())
        except Exception as e:                      # noqa: BLE001
            print("no se pudo bajar three.js, el archivo único lo pedirá a cdnjs:", e)
            return None
    return cache.read_text(encoding="utf-8").replace("</script", "<" + chr(92) + "/script")


def write_html(datos):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    three = three_source()
    glb = (OUT / "modelo.glb").read_bytes()
    idx = tpl.replace("/*__MODE__*/null", '"fetch"').replace("/*__DATA__*/null", "null").replace("__GLB_B64__", "")
    (OUT / "index.html").write_text(idx, encoding="utf-8")

    emb = json.loads(json.dumps(datos))                      # deep copy
    nimg = 0
    for c in emb["resultados"]["casos"]:
        for k, rel in list(c["imagenes"].items()):
            c["imagenes"][k] = jpeg_data_uri(OUT / rel)
            nimg += 1
    dj = json.dumps(emb, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    single = tpl.replace("/*__MODE__*/null", '"embedded"').replace("/*__DATA__*/null", dj).replace("__GLB_B64__", base64.b64encode(glb).decode("ascii"))
    if three:
        single = single.replace(THREE_TAG, "<script>" + three + "</script>")
    mb = len(single.encode("utf-8")) / 1e6
    if mb > EMBED_LIMIT_MB:                                  # too big: drop the images, keep the page openable
        for c in emb["resultados"]["casos"]:
            c["imagenes"] = {}
        dj = json.dumps(emb, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        single = tpl.replace("/*__MODE__*/null", '"embedded"').replace("/*__DATA__*/null", dj).replace("__GLB_B64__", base64.b64encode(glb).decode("ascii"))
        if three:
            single = single.replace(THREE_TAG, "<script>" + three + "</script>")
        mb = len(single.encode("utf-8")) / 1e6
        print(f"AVISO: con imágenes pasaba de {EMBED_LIMIT_MB} MB; el archivo único va sin imágenes de simulación")
    (OUT / "LanternGuard_visor.html").write_text(single, encoding="utf-8")
    old = OUT / "lanternguard.glb"
    if old.exists():
        old.unlink()
    print(f"index.html {(OUT / 'index.html').stat().st_size / 1e3:.0f} kB · LanternGuard_visor.html {mb:.2f} MB ({nimg} imágenes embebidas) · modelo.glb {len(glb) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
