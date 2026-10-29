"""MEDIDAS.md for the team, written from params.py and the exported STL (never by hand).

    python medidas.py      (or: python build.py --medidas)   -> ../MEDIDAS.md

Plain Spanish for readers who do not program: what to measure first, what each ring needs, and one section per piece
with its size, how it is printed and where each important value comes from.
"""
from pathlib import Path

import trimesh

import fase_a as FA
import layout as LY
import params as P
import piezas as Z
import riel

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
OUT = MOD / "MEDIDAS.md"
PLANOS = "planos/cad_final"

ORIGEN = {"medido": "medido", "fabricante": "dato del fabricante", "equipo": "decisión del equipo", "estimado": "estimado"}
ESTADO = {"confirmado": "confirmado", "por_verificar": "**por confirmar**"}

# what to measure first: (param key, what, tool, why it matters); the order is the priority
POR_CONFIRMAR = [
    ("comp.esp32_devkitc1", "Largo, ancho y alto (con pines) de la ESP32-S3 DevKitC-1", "calibrador",
     "fija el tamaño de la bandeja y de la caja"),
    ("pg7.contratuerca_AF", "Entrecaras de la contratuerca del prensaestopas PG7", "calibrador",
     "fija el lugar de los PG7 y el largo de la caja"),
    ("pg7.domo", "Diámetro y largo del prensaestopas PG7 por fuera (cuerpo + domo)", "calibrador",
     "fija el alto de la cámara de cables bajo la caja"),
    ("petg.densidad", "Densidad real del PETG: pesar una probeta y dividir por su volumen del slicer", "balanza + slicer",
     "cambia el peso en el agua y la cantidad de pletinas"),
    ("impresion.holgura", "Holgura que ajusta sin juego en el peine PB7", "probeta PB7", "todos los encajes"),
    ("impresion.comp_agujero", "Cuánto se achican los agujeros en la impresora (peine PB7)", "probeta PB7",
     "agujeros de tornillos, insertos y varilla"),
    ("riel.ranura_T", "Que la tuerca M4 entre y deslice en la ranura T (probeta PB2)", "probeta PB2 + tuerca real",
     "ganchos y carros se aprietan ahí"),
    ("m4.inserto_agujero", "Fuerza de arranque del inserto M4 (probeta PB8); el fondo pide 274 N", "probeta PB8 + dinamómetro",
     "el riel cuelga de esos 4 insertos"),
    ("aro.varilla_D", "Diámetro de la varilla del aro de la linterna real", "calibrador",
     "elige el casquillo M13 que se imprime"),
    ("gancho.caida", "Distancia del fondo del riel al centro de la varilla del aro, con el aro real", "regla o calibrador",
     "alto del gancho"),
    ("ensamble.linterna_peso_agua_N", "Peso de la linterna (aro, red y carga) dentro del agua", "dinamómetro en un balde",
     "carga del asa en Ø100 y Ø200"),
    ("lastre.pletina", "Ancho y espesor de la pletina de inox comprada", "calibrador", "tamaño del bolsillo del lastre"),
    ("riel.varilla_masas", "Peso de la varilla M8 (por metro), la tuerca y la arandela", "balanza", "lastre del nodo"),
    ("riel.varilla_grado", "Grado de la varilla M8 (8.8 o 4.6, viene marcado o en la factura)", "a la vista",
     "resistencia de la unión del riel"),
    ("riel.varilla_arandela", "Diámetro exterior y espesor de la arandela ancha M8", "calibrador", "apoyo en la punta del riel"),
    ("camara.lente_D", "Diámetro del porta-lente de la Arducam Mega", "calibrador", "frente de la cápsula"),
    ("aro_led.envolvente", "Diámetro exterior y espesor del anillo LED", "calibrador", "ventana y apertura de la cápsula"),
    ("aro_led.agujero", "Diámetro interior del anillo LED", "calibrador", "tubo separador entre LED y lente"),
    ("cable.cat5e_D", "Diámetro del Cat5e de exterior", "calibrador", "conducto del riel y prensaestopas"),
    ("camara.cable_incluido", "Largo del cable que trae la cámara", "cinta métrica", "si alcanza o hay que alargar (prueba SPI)"),
    ("boya.panel", "Medidas del panel solar", "calibrador", "largueros de la boya"),
    ("boya.masas", "Peso de cada componente de la boya, sobre todo el panel y las baterías", "balanza",
     "francobordo: con unos 40 g más en el panel baja de 50 mm"),
    ("masa.capsula_contenido", "Peso de la cámara + LED + cable + PG7 de una cápsula", "balanza", "peso en el agua"),
    ("masa.otras_piezas", "Peso de ganchos, carros, perillas y tornillería del riel ya impresos", "balanza", "peso en el agua"),
    ("impresora.cama", "Tamaño de la cama de la impresora que se use", "manual de la impresora", "si cada pieza entra"),
    ("umbilical", "Diámetro y largo del cable umbilical", "calibrador + cinta métrica", "prensaestopas y boya"),
    ("pestillo.resalte", "Que el pestillo haga clic sin trabarse (probeta PB4 sobre PB1)", "probeta + guante", "cierre del gancho"),
    ("casquillo.interferencia", "Que el casquillo entre a presión en el gancho (probeta PB1)", "probeta", "casquillo firme"),
]


def stl_info(pz):
    m = trimesh.load(str(pz.stl), force="mesh")
    ext = m.bounds[1] - m.bounds[0]
    V, A = abs(m.volume) / 1000.0, m.area / 100.0          # cm3, cm2
    if pz.material.startswith("acr"):
        g = V * P.ACRYLIC_DENSITY
        txt = f"{g:.0f} g"
    elif pz.infill.startswith("100") or pz.infill == "no se imprime":
        g = V * P.PETG_DENSITY
        txt = f"{g:.0f} g"
    else:
        shell = min(V, A * P.SHELL_T / 10.0)
        g40 = P.PETG_DENSITY * (shell + 0.4 * (V - shell))
        txt = f"{g40:.0f} g al 40 % ({V * P.PETG_DENSITY:.0f} g al 100 %)"
    return ext, txt


def qty_txt(pz):
    q = [pz.n(D) for D in P.RING_DIAMETERS]
    if pz.code == "PB8":
        return "3 (aparte, para la prueba)"
    if len(set(q)) == 1:
        return f"{q[0]} por nodo"
    return ", ".join(f"Ø{D:g}: {n}" for D, n in zip(P.RING_DIAMETERS, q))


def configs():
    lay = LY.build(floors=1)
    an = FA.analyse_box(lay)
    rows = FA.balance(an, P.INFILL_CASES[0])["rows"]
    return lay, rows


def main():
    lay, rows = configs()
    reg = P.REGISTRO
    n_ver = sum(1 for x in reg.values() if x.estado != "confirmado")
    r = ["# Medidas del nodo LanternGuard y de la boya", "",
         "> Este archivo lo escribe el programa `cad_final/medidas.py` a partir de `cad_final/params.py`. **No lo edites a "
         "mano**: si una medida cambia, se cambia en `params.py` y se vuelve a generar (`python cad_final/build.py --medidas`).", "",
         "**Cómo leer las tablas.** Cada medida dice de dónde sale (*origen*) y si ya se comprobó (*estado*):", "",
         "- **medido**: lo medimos con la pieza real en la mano.",
         "- **dato del fabricante**: viene de la hoja de datos o del anuncio; hay que confirmarlo con la pieza comprada.",
         "- **decisión del equipo**: lo decidimos nosotros (por ejemplo, el largo del riel).",
         "- **estimado**: es una suposición o una propuesta de diseño; se confirma midiendo o con una probeta.", "",
         f"Hoy hay {len(reg)} medidas en `params.py`: {sum(1 for x in reg.values() if x.origen == 'medido')} medidas a mano y "
         f"{n_ver} por confirmar. Las piezas de `salida/preliminar/` y `salida/boya/` **no están listas para imprimir** hasta que "
         "se confirmen las medidas de la tabla 1. Lo único listo para imprimir son las probetas de `salida/probetas/`.", ""]

    # 1. what to measure
    r += ["## 1. Medidas por confirmar, de la más importante a la menos", "",
          "| # | Qué hay que medir | Con qué | Valor que usa hoy el modelo | Nombre en params.py | Origen | Por qué importa |",
          "|---|---|---|---|---|---|---|"]
    for i, (k, what, tool, why) in enumerate(POR_CONFIRMAR, 1):
        x = reg[k]
        r.append(f"| {i} | {what} | {tool} | {Z.fmt(x.value)} | `{k}` | {ORIGEN[x.origen]} | {why} |")
    listed = {k for k, *_ in POR_CONFIRMAR}
    rest = [x for x in reg.values() if x.estado != "confirmado" and x.key not in listed]
    r += ["", f"Además hay {len(rest)} valores de diseño propuestos (formas, holguras, espesores) que se confirman con las "
          "probetas y la prueba en el agua. Están en las secciones de cada pieza y todos juntos en "
          "`cad_final/reporte_parametros.md` §2.", ""]

    # 2. configurations
    r += ["## 2. Qué se arma para cada aro", "",
          "| Aro | Largo del riel | Extensiones por lado | Varilla M8 | Pletinas de inox por lado | Peso en el aire | "
          "Peso dentro del agua (hacia abajo) |", "|---|---|---|---|---|---|---|"]
    for row in rows:
        n = row["n"]
        r.append(f"| Ø{row['D']:g} | {row['L']:.0f} mm | {n} | {riel.rod_length(n):.0f} mm, con 2 tuercas y 2 arandelas | "
                 f"{row['layers']} | {row['total'] / 1000:.2f} kg | {row['app']:.0f} g |")
    r += ["", f"El peso dentro del agua tiene que quedar entre {P.BALLAST_TARGET_KGF[0] * 1000:.0f} y "
          f"{P.BALLAST_TARGET_KGF[1] * 1000:.0f} g y el peso en el aire bajo {P.AIR_MASS_MAX_KG:g} kg. Bandeja al 40 %.", "",
          "Piezas por nodo según el aro:", "",
          "| Pieza | " + " | ".join(f"Ø{D:g}" for D in P.RING_DIAMETERS) + " |", "|---|" + "---|" * len(P.RING_DIAMETERS)]
    for pz in Z.PIEZAS:
        if pz.folder != Z.PRE:
            continue
        r.append(f"| {pz.code} {pz.name} | " + " | ".join(str(pz.n(D)) for D in P.RING_DIAMETERS) + " |")
    r.append("| Pletinas de inox " + Z.fmt(P.PLATE_BAR) + f" × {P.PLATE_L:g} | "
             + " | ".join(str(P.PLATE_SIDES * row["layers"]) for row in rows) + " |")
    r += ["", "La boya es una sola para todos los aros (sección 3, piezas B).", ""]

    # 3. pieces
    r += ["## 3. Piezas", "",
          "Para cada pieza: el plano (generado desde el modelo, en `planos/cad_final/`), las medidas generales tal como está "
          "dibujada (largo × ancho × alto) y las medidas importantes con su nombre en `params.py`.", ""]
    for pz in Z.PIEZAS:
        ext, mass = stl_info(pz)
        r += [f"### {pz.code} · {pz.name}", "", f"![{pz.code}]({PLANOS}/{pz.code}.png)", "",
              f"- **Para qué sirve:** {pz.what}.",
              f"- **Medidas generales:** {ext[0]:.1f} × {ext[1]:.1f} × {ext[2]:.1f} mm.",
              f"- **Material:** {pz.material}. **Relleno:** {pz.infill}. **Cómo se imprime:** {pz.orient}.",
              f"- **Cantidad:** {qty_txt(pz)}. **Masa:** {mass}.",
              f"- **Archivos:** `{pz.stl.relative_to(MOD).as_posix()}`" + (f", `{pz.step.relative_to(MOD).as_posix()}`" if pz.step.exists() else "") + "."]
        if pz.note:
            r.append(f"- **Ojo:** {pz.note}")
        r += ["", "| Medida | Valor (mm) | Nombre en params.py | Origen | Estado |", "|---|---|---|---|---|"]
        for label, k, idx in pz.keys:
            x = reg[k]
            name = f"`{k}`" + (f" ({idx})" if isinstance(idx, str) else (f" [{idx + 1}.º valor]" if idx is not None else ""))
            r.append(f"| {label} | {Z.fmt(Z.value(k, idx))} | {name} | {ORIGEN[x.origen]} | {ESTADO[x.estado]} |")
        r.append("")
    r += ["## 4. Tornillería y compras que fija el modelo", "",
          "| Qué | Medida | Nombre en params.py | Estado |", "|---|---|---|---|"]
    for label, k in (("Tuerca M4 (ranura T)", "m4.tuerca"), ("Cabeza Allen M4", "m4.cabeza"), ("Tuerca M3", "m3.tuerca"),
                     ("Inserto térmico M3: agujero", "m3.inserto_agujero"), ("Tornillo M3 avellanado (tapa del bolsillo)", "m3.cabeza_avellanada"), ("Inserto térmico M4: agujero", "m4.inserto_agujero"),
                     ("Varilla roscada M8 (datos)", "riel.varilla_M8_datos"), ("Arandela ancha M8 DIN 9021", "riel.varilla_arandela"),
                     ("Tuerca M8", "riel.varilla_tuerca"), ("Cordón de junta tórica", "junta.cordon"),
                     ("Pletina de inox", "lastre.pletina"), ("Cat5e", "cable.cat5e_D")):
        x = reg[k]
        r.append(f"| {label} | {Z.fmt(x.value)} | `{k}` | {ESTADO[x.estado]} |")
    r.append("")
    OUT.write_text("\n".join(r), encoding="utf-8")
    print("written", OUT, len(r), "lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
