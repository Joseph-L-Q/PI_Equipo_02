# Cambios rápidos

Todas las medidas viven en un solo archivo: `cad_final/params.py`. Nada se cambia en los STL, los STEP ni Onshape a
mano: se cambia el número en `params.py` y se regenera.

## Qué versión se regenera

`version` en `params.py`: `"simple"` (por defecto, el prototipo en el aro Ø200: `cad_final/simple.py`, salida en
`salida/simple/` y números en `cad_final/reporte_simple.md`) o `"modular"` (riel por tramos de Ø100 a Ø500). Con
`simple`, `build.py --rapido` tarda menos de 1.5 min y no toca las piezas de la modular. En la simple se cambian sobre
todo `capsula.angulo`, `aro.seccion`, `lastre.pletinas`, `separador.*`, `apice.altura` y `linterna.*`.

## Cómo cambiar una medida

1. Abre `cad_final/params.py` (con cualquier editor de texto; VS Code o el Bloc de notas sirven).
2. Busca el nombre de la medida. Los nombres están en `MEDIDAS.md`, al lado de cada valor (por ejemplo `caja.fondo`).
3. Cada línea se ve así:

   ```python
   BOX_FLOOR = p("caja.fondo", 4.0, "estimado", "por_verificar", "razón ...")
   ```

   - Cambia **solo el número** (4.0).
   - Si lo mediste: cambia `"estimado"` por `"medido"` y `"por_verificar"` por `"confirmado"`.
   - En la razón, anota con qué lo mediste y la fecha (por ejemplo `"calibrador, 3 piezas, 05/11"`).
4. Regenera (desde la carpeta `Proyecto/MóduloMecánico`, con el entorno de `setup_laptop.ps1`):

   | Qué cambiaste | Comando | Tarda |
   |---|---|---|
   | Cualquier cosa, para ver si sigue todo bien | `python cad_final/build.py --rapido` | ~1.5 min |
   | Una medida de pieza que se imprime | `python cad_final/build.py` | ~6 min |
   | El largo del riel, el aro o algo que puede chocar | `python cad_final/build.py --todo` | ~18 min, usa todos los núcleos |
   | Solo quieres actualizar `MEDIDAS.md` | `python cad_final/build.py --medidas` | ~15 s |
   | Solo los planos | `python cad_final/build.py --planos` | ~40 s |

   En Windows, si no activaste el entorno, usa `.venv\Scripts\python.exe` en lugar de `python`.
5. Mira la última línea: `TODO BIEN` o `HUBO FALLAS`. Si falla, el detalle está en `salida/_logs_build/<paso>.log`.
   Lo normal es que una medida nueva haga chocar dos piezas: el log dice cuáles.
6. Actualiza Onshape con los STEP nuevos (detalle en `ONSHAPE.md`):

   ```
   python cad_final/onshape_sync.py --actualizar M9 --dry-run   # qué subiría y cuántas llamadas gasta
   python cad_final/onshape_sync.py --actualizar M9             # sube el STEP nuevo de M9 al documento
   ```

   - `M3` sube las cuatro piezas del riel. Si el STEP no cambió, no gasta llamadas.
   - Después, **a mano en Onshape**: clic derecho en la pestaña del Part Studio de esa pieza → **Update...** y eliges el
     mismo STEP. La API no tiene ese paso; sin él el Part Studio sigue con la forma vieja.

## Los cambios más comunes

| Quiero... | Nombre en `params.py` | Qué se mueve |
|---|---|---|
| Ajustar holguras después de imprimir el peine (PB7) | `impresion.holgura`, `impresion.comp_agujero` | Todos los encajes |
| Poner la medida real de la varilla del aro | `aro.varilla_D` | Casquillo M13 que se usa |
| Cambiar el ángulo de las cámaras | `bisagra.inclinacion` | Ensambles; la bisagra tiene 36 dientes (pasos de 10 grados) |
| Usar otro largo de riel para un aro | `riel.extensiones` | Piezas por aro, lastre, cables, ensambles |
| Cambiar el grado de la varilla M8 (8.8 o 4.6) | `riel.varilla_grado` | Solo el cálculo de la unión (`reporte_verificacion.md` §3c) |
| Poner el peso real de la linterna en el agua | `ensamble.linterna_peso_agua_N` | Cálculo del asa (`reporte_verificacion.md` §6b) |
| Medidas del prensaestopas PG7 | `pg7.agujero`, `pg7.contratuerca_AF`, `pg7.domo` | Caja, cápsula y el alto de la cámara de cables |
| Espesor del fondo de la caja | `caja.fondo` | Caja M1 y la probeta PB8 (tiene el mismo espesor) |
| Densidad real del PETG (la que dice el slicer) | `petg.densidad` | Pesos y lastre |
| Masas reales (pesadas en balanza) | `masa.*`, `boya.masas` | Lastre y flotación |

## Qué no tocar

- `riel.paso_extension` y `riel.regla_extensiones`: son decisiones del equipo (C18). Si se cambian, hay que revisar el
  largo de todo el riel y volver a correr `--todo`.
- La carpeta `cad/`: es el diseño anterior, queda como referencia y no se regenera.
- Los archivos `reporte_*.md`, `MEDIDAS.md` y los planos se escriben solos: si los editas a mano, se pierden en el
  próximo build.
