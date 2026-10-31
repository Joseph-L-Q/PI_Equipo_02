"""FICHA.md of a prototype (P1..P4) and its row in salida/prototipos/resumen.json, from what simple.py, slicer.py and fem.py wrote.

    python prototipos.py            (from cad_final/; LG_VERSION or params.version picks the prototype; build.py --prototipo does all)
Never invents a number: a case without a FEM run prints "sin FEM", a piece without slicer data prints "sin slicer".
Mass, hours and cost are the sliced ones (slicer.json) times the quantity of each printed piece; the bought acrylic windows (M7) and
the test-lantern separator (LR1) are not counted. Cost = grams x params.costo.petg_soles_kg.
"""
import json
from pathlib import Path

import params as P

HERE = Path(__file__).resolve().parent
SAL = HERE.parent / "salida"
VER = SAL / P.SALIDA_REL


def load(name):
    f = VER / name
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def summarize(ver_dir=None):
    res, sl, fem = load("resultados.json"), load("slicer.json"), load("fem/fem.json")
    qty = res["cantidades"]
    printed = {k: q for k, q in qty.items() if not k.startswith("M7")}
    row = dict(version=P.VERSION, piezas=sum(printed.values()), tipos=len(printed),
               sellos=sum(res["sellos"].values()), juntas=sum(res["juntas_atornilladas"].values()),
               aire_g=res["peso"]["40"]["aire_g"], aparente_g=res["peso"]["40"]["aparente_g"],
               aparente100_g=res["peso"]["100"]["aparente_g"], caja=res["caja"]["exterior"],
               fs_mano=res["fs"])
    if sl and all(k in sl for k in printed):
        row["masa_g"] = sum(q * sl[k]["g"] for k, q in printed.items())
        row["horas"] = sum(q * sl[k]["h"] for k, q in printed.items())
        row["costo_soles"] = row["masa_g"] / 1000 * P.PETG_PRICE
    c = (fem or {}).get("casos", {})
    row["fem"] = {k: dict(fs=v["fs"], fs_capas=v["fs_capas"], umax=v["umax"], smax=v["smax"]) for k, v in c.items()}
    return res, sl, fem, row


def fmt(v, f="{:.1f}", none="sin dato"):
    return none if v is None else f.format(v)


def main():
    if P.VERSION not in P.PROTOTYPES:
        raise SystemExit(f"prototipos.py: version '{P.VERSION}' no es un prototipo ({', '.join(P.PROTOTYPES)})")
    res, sl, fem, row = summarize()
    cfg = P.CFG
    qty = res["cantidades"]
    fc = row["fem"]
    L = [f"# Ficha {P.VERSION}", "",
         "Generada por `cad_final/prototipos.py` desde `resultados.json`, `slicer.json` y `fem/fem.json` de esta carpeta. No editar a mano.", "",
         "## Que es", "",
         f"Nodo del aro de prueba Ø{P.SIMPLE_RING_D:g} (version simple V2 como base) con estas diferencias: riel **{cfg['riel']}**, pared del conducto "
         f"**{cfg['pared']:g} mm**, gancho **{cfg['gancho']}**, {'caja y riel en una sola pieza (monocasco)' if cfg['monocasco'] else 'caja y rieles separados'}, "
         f"{'con redondeos y logo' if cfg['estetico'] else 'sin acabado estetico'}, caja **{cfg['caja']}**, capsula **{cfg['capsula']}**. "
         f"Caja exterior {' x '.join(f'{v:.0f}' for v in res['caja']['exterior'])} mm. Ventanas de celosia: {res.get('celosia_ventanas') or 'ninguna'}. "
         f"Redondeos aplicados (radio mm, 0 = fallo): {res.get('redondeos') or 'ninguno'}.", "",
         "## Piezas impresas", "",
         "| Pieza | Cant. | g c/u (slicer) | h c/u | Orientacion | Soportes | Relleno |", "|---|---|---|---|---|---|---|"]
    for k, q in qty.items():
        p = res["piezas"].get(k, {})
        s = (sl or {}).get(k)
        if k.startswith("M7"):
            L.append(f"| {p.get('nombre', k)} | {q} | comprada | - | - | - | acrilico |")
            continue
        L.append(f"| {p.get('nombre', k)} | {q} | {fmt(s and s['g'])} | {fmt(s and s['h'], '{:.2f}')} | {p.get('orient', '-')} | "
                 f"{'si' if p.get('soportes') else 'no'} | {p.get('relleno')} |")
    L += ["", f"Piezas impresas por nodo: **{row['piezas']}** de {row['tipos']} tipos, mas 2 ventanas de acrilico.", ""]
    if "masa_g" in row:
        L += [f"Masa impresa del nodo (slicer, sin pletinas ni tornilleria): **{row['masa_g']:.0f} g**; tiempo **{row['horas']:.1f} h**; "
              f"filamento **S/ {row['costo_soles']:.2f}** (a S/ {P.PETG_PRICE:g} el kg, estimado).", ""]
    else:
        L += ["Masa, horas y costo: **sin slicer** (correr `build.py --prototipo " + P.VERSION + " --slicer`).", ""]
    L += ["## Sellos y juntas", "",
          f"- Sellos estancos: **{row['sellos']}** ({', '.join(f'{k} {v}' for k, v in res['sellos'].items())}).",
          f"- Juntas atornilladas no estancas (conducto inundado): **{row['juntas']}** ({', '.join(f'{k} {v}' for k, v in res['juntas_atornilladas'].items())}); "
          "ademas de las tapas del bolsillo del lastre (2 M3t) y los tornillos de las tapas.", "",
          "## Peso", "",
          f"- En aire: **{row['aire_g']:.0f} g** (bandeja al 40 %), con {res['pletinas']['por_bolsillo']} pletinas por bolsillo.",
          f"- Aparente en agua de mar: **{row['aparente_g']:+.0f} g** (40 %) / {row['aparente100_g']:+.0f} g (100 %); ventana exigida "
          f"{P.BALLAST_TARGET_KGF[0] * 1000:.0f} a {P.BALLAST_TARGET_KGF[1] * 1000:.0f} g.", "",
          "## Factores de seguridad (150 N de manipulacion en una capsula)", ""]
    if fc:
        L += ["FEM local (Gmsh + CalculiX, PETG isotropico estimado, esfuerzo = percentil 99.5 de von Mises; FS a lo largo de las capas / entre capas):", "",
              "| Caso | Desplazamiento mm | Esfuerzo MPa | FS | FS entre capas |", "|---|---|---|---|---|"]
        for k, v in fc.items():
            L.append(f"| {k} | {v['umax']:.2f} | {v['smax']:.1f} | {v['fs']:.1f} | {v['fs_capas']:.1f} |")
        miss = [k for k in ("riel_agua", "riel_izado", "pie") if k not in fc]
        if miss:
            L.append(f"\nSin FEM: {', '.join(miss)}.")
    else:
        L.append("**Sin FEM** (correr `build.py --prototipo " + P.VERSION + " --fem`).")
    fm = res["fs"]
    L += ["", f"Calculo a mano (simple.py, conservador, no es FEM): riel {fm['riel']:.1f} / {fm['riel_capas']:.1f}, pie {fm['pie']:.1f} / {fm['pie_capas']:.1f}, "
          f"gancho {fm['gancho']:.1f} / {fm['gancho_capas']:.1f} (a lo largo / entre capas)."
          + (" En P3/P4 el pie va fundido a la tapa: el calculo a mano del pie (aplastamiento de los M4) no aplica; vale el FEM." if cfg["monocasco"] else ""), "",
          "## Archivos", "",
          "- `ensamble_simple_D200.step` (nodo + linterna de prueba), `stl/` y `step/` por pieza, `ensamble_simple_iso.png` y `ensamble_simple_lado.png` "
          "(vista frontal), `nodo_simple_iso.png`, `nodo_simple_corte.png`, `REPORTE.md` (chequeos), `slicer.json`, `fem/fem.json` y sus PNG.", "",
          "## Pendiente", "",
          "- Todo lo estimado de `params.py` sigue por verificar (diametro real de la varilla del aro, cargas, PETG real); ver `docs/PROTOTIPOS.md`.",
          "- Ninguna cifra de este prototipo esta probada en agua: el FEM es de un material isotropico estimado y no dice nada de estanqueidad."]
    if cfg["gancho"] == "snap":
        L.append("- Gancho snap-fit: la fuerza de insercion y la fatiga del brazo no estan calculadas; imprimir una probeta del gancho sobre la varilla real antes del nodo.")
    if cfg["gancho"] == "abrazadera":
        L.append("- Abrazadera: la red de la linterna de prueba pasa por la media luna M9c; no se verifico contra la red real.")
    (VER / "FICHA.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sumf = SAL / "prototipos" / "resumen.json"
    allr = json.loads(sumf.read_text(encoding="utf-8")) if sumf.exists() else {}
    allr[P.VERSION] = row
    sumf.write_text(json.dumps(allr, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print("FICHA", VER / "FICHA.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
