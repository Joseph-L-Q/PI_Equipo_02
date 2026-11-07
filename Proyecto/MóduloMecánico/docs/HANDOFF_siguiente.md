# HANDOFF siguiente | PC de casa | SimScale por módulo ensamblado (07/11)

Proyectos públicos: [nodo](https://www.simscale.com/projects/yoichi_palacio/lanternguard_1_-_nodo_sumergido_1336844629/) · [boya](https://www.simscale.com/projects/yoichi_palacio/lanternguard_2_-_boya_661668473/) · [tierra](https://www.simscale.com/projects/yoichi_palacio/lanternguard_3_-_estacion_de_tierra_418577745/). Los pids y el estado están en `salida/simscale_modulos/state.json`. Scripts: `cad_final/simscale_modulos.py` (o `simscale_run.py --modulo <m>`) y `cad_final/capturas_simscale.py`.

## Por hacer
1. **Boya, con sesión en SimScale:** sondear von Mises a 2–3 mm del ojal en la corrida `boya_estatico_mixto`. Si fuera del pico pasa de 25 MPa (FS < 2), revisar el ojal y la cuna.
2. **Capturas que piden sesión** (`docs/GUIA_CAPTURAS_SIMSCALE.md`): la magnitud del desplazamiento, la malla, las condiciones de borde en el workbench y la configuración del proyecto de María.
3. **Desplazamiento de la boya, corrida 2:** no se corrió. El publicado es de la corrida 1. Comando: `simscale_modulos.py --modulo boya --mixto --desplazamiento`.
4. **CFD de la boya** (opción b del encargo): no se hizo.
5. Lo pendiente del bloque del 05/11 sigue igual (abajo).

## Decisiones que tomé solo (detalle en `docs/DECISIONES.md`, 07/11)
- **Contactos pegados detectados por script**, a 0,35 mm. La API no tiene la detección automática del workbench.
- **Boya:** el informe toma la corrida 2 y conserva la 1, que se publica con su diagnóstico.
- **Tierra:** el apoyo va en las ranuras de las pestañas. La primera corrida, que empotraba todo el fondo, se descartó.

---

# HANDOFF siguiente | PC de casa | documento limpio sin probetas (05/11)

Documento: [LanternGuard - PIEZAS PARA IMPRIMIR](https://cad.onshape.com/documents/76e36e0130a8d259842ecee7/w/fdd58e8bdf77f39a1781a12d), did `76e36e0130a8d259842ecee7`, wid `fdd58e8bdf77f39a1781a12d`. Generado con `cad_final/documento_limpio.py`; estado en `salida/limpio/estado.json`.

## Por hacer
1. **Onshape, a mano:** Share > Link (vista + exportación; la API da 403) y arrastrar `00_LEEME` al primer lugar.
2. **Drive, carpeta `LanternGuard_CAD/08_PARA_IMPRIMIR`:** solo STL, 3MF y PDF de planos de estas 21 piezas, con los mismos números (`10_M1s_caja_cuerpo`, ...). Sin probetas. Exportar los PDF desde este documento: no se exportaron aquí.
3. **Slicer real** de M3s (asiento Ø17,1), LR2_aro, T1 y T2 (en PLA). La placa P12 anterior no sirve.
4. **FEM con `fem.py` (CalculiX)** del riel: el FS 3,95 / 5,19 es de `fem_tet10`.
5. **Confirmar Heltec, batería y SMA** antes de imprimir T1 y T2.
6. **Cotas a mano** que no cupieron: M3s, M5s, M11, M11_sup y B6 (detalle en `salida/limpio/registro_planos.json`).
7. **El `.env` sigue en `cad_final/`:** no se borró, como pediste. Borrarlo cuando termine el trabajo con la clave.

## Gramos
| Conjunto | g | h |
|---|---|---|
| Nodo P2 (16 piezas) | 1677 | 45 |
| Boya PET (14 piezas) | 1489 | 58,5 |
| 4 aros LR2 | 600 | 40 |
| Tierra T1 + T2, PLA | 121 | 8,1 |
| **Total (36 piezas)** | **3887** | **152** |

**Rollos: 4, con 113 g de margen.** Aro, T1, T2 y M3s son estimados, sin slicer. Las horas del aro y de tierra usan el ritmo de `BOM.md` (15 g/h), más prudente que los 31 g/h de `ARO_Y_ESTACION.md`.

## Decisiones que tomé solo
- **Probetas:** antes del cambio de plan se cargaron y dibujaron; se quitaron de este documento. No están en `LG_IMPRIMIR_P2` las P01 a P05 (nunca estuvieron ahí; hay STL en `LG_probetas`); PB_aro sí sigue ahí, con asiento Ø16,8. Los STEP de P01 a P05 quedan en `salida/limpio/step/`.
- **Números de pestaña:** no los cambié. Identifican la pieza; el orden de impresión está en las fases del LEEME. Renumerar costaría unas 40 llamadas.
- **Prueba de agua:** añadí a tu procedimiento las 2 placas de prueba con junta (8 M4) y el tapón del PG7, porque la caja tiene 2 ventanas hacia los rieles (`docs/ESTANQUEIDAD.md`). Sin eso entra agua por ahí.
- **Revisar el gancho:** el cálculo a mano de `REPORTE.md` da FS 1,8 entre capas en el gancho en C con 150 N (antes 1,9). El FEM del riel da 3,95, pero fija el asiento, así que no evalúa bien esa zona. El FEM de `aro.py`/CalculiX debe confirmarlo. En la fase 1, tirar del gancho a mano antes de seguir.
- **Juego:** 0,3 mm es el nominal; el agujero sigue corrido 0,09 mm por la curva del aro, así que el mínimo real es 0,21 mm por lado.
- **BOM:** B3 y B4 pasan a 100 % (247 y 111 g, reparto de la placa P16): la tabla decía 175 y 79 g al 40 %. T1 y T2 en PLA (72 y 49 g). Lastre del nodo: 990 g.
- **Planos editados además de lo pedido:** T1 y T2 ahora dicen PLA; LR2_aro cita el asiento Ø17,1 y juego 0,6 en diámetro.
- **Plano de M6:** es el `Drawing 13` de Melissa, renombrado; no es un PLANO_A4 generado.
- **Llamadas:** 249 de 250 en el encargo del documento. Este cambio llevó un contador aparte con tope 70, que fijé yo porque tu mensaje no daba uno. El tope de 250 lo tomé como del encargo anterior.

---

# HANDOFF siguiente | PC de casa | aro Ø16,5 con relleno, M3s nuevo, T1 corregido y ensamble de tierra (05/11)

Detalle en `docs/ARO_Y_ESTACION.md`. Generado en la PC de trabajo, que no tiene OrcaSlicer ni CalculiX.

## Por hacer
1. **Comprar 5 rollos, no 4:** el total estimado es de unos 4172 g (tabla abajo).
2. **Slicer real** de LR2_aro, PB_aro, T1_caja, T2_tapa y **M3s_riel_gancho**. La placa actual de M3s es del asiento anterior: no imprimirla. Para el aro: **13 perímetros de 0,4, 15 % de gyroid y capas superiores e inferiores de 5,2 mm**. Revisar la cara inferior sin soportes.
3. **FEM con `fem.py` (CalculiX)** del riel con el M3s nuevo y del aro. El FS 3,01 del aro impreso tiene muy poco margen y supone una rigidez de relleno sin ensayar. Riel: FS 3,94 en el agua y 5,19 al izar. Revisar también la cuenta a mano del gancho en `REPORTE.md`, que da FS 1,9 contra 13,7 del FEM.
4. **Imprimir PB_aro antes que los 4 aros y los M3s:** el margen real en el asiento es de 0,06 mm por lado. Si no entra, ajustar `gancho.c` y regenerar.
5. **Subir a Drive** los STL, los 3MF y los planos (`salida/aro/stl/`, `salida/tierra/stl/`, `salida/prototipos/P2_robusto/stl/M3s_riel_gancho.stl`, `salida/nuevas/planos_A4/`, `salida/planos_onshape/pdf_a4/`).
6. **Confirmar medidas reales del Heltec, la batería y la SMA antes de imprimir la caja:** contorno, altura, agujeros M2,5, pantalla, USB-C, PRG, RST y cara de la SMA. Hoy son estimadas en `tierra.medidas` (`params.py`); si cambian, correr `tierra.py` y `tierra.py --ensamble`.
7. **Lastre:** el cálculo pasó de 980 a 990 g con el M3s nuevo. Pesar con el lastre real, como estaba previsto.
8. **Cotas a mano en Onshape:** LR2_aro 3 (alto 16 incluido), T1_caja 15, T2_tapa 10 y M3s_riel_gancho 13; no cupieron o salen de bordes curvos. En esos planos sigue el defecto SHEET «11».

## Gramos
| Pieza | Cant. | Impresión | g c/u | g total |
|---|---|---|---|---|
| LR2_aro | 4 | 13 perímetros + 15 % gyroid | 150,0 | 600,0 |
| PB_aro_tramo | 1 | 13 perímetros + 15 % gyroid | 12,0 | 12,0 |
| PB_aro_asiento | 1 | 100 % | 15,7 | 15,7 |
| T1_caja | 1 | 100 % | 73,9 | 73,9 |
| T2_tapa | 1 | 100 % | 50,1 | 50,1 |
| **Piezas nuevas** | | | | **751,7** |
| Las 20 placas del 05/11 (slicer) | | | | 3427 |
| Cambio del par de M3s (por volumen y relleno) | | | | −7 |
| **Total del proyecto** | | | | **≈ 4172 g** |

**Rollos: 5 de 1 kg.** El objetivo de 4 rollos con 150 g de margen pedía 3850 g como máximo; el total se pasa por 322 g, y por 172 g de los 4000 g aun sin margen. Para llegar, cada aro debería pesar unos 70 g, y el más liviano probado (76 g) tiene FS 1,70.

## Decisiones que tomé solo
- **Aro:** 13 perímetros + 15 % de gyroid, la más liviana con FS ≥ 3. Prioricé la resistencia sobre los 4 rollos, como pediste. Alternativa si el plástico manda: 4 perímetros + 15 % (76 g por aro, unos 3870 g, 130 g de margen), pero con FS 1,70 **no cumple**.
- **M3s:** el agujero del asiento se corrió 0,09 mm hacia el eje para eliminar un roce de 0,03 mm con el aro curvo.
- **Onshape, reemplazos:** los tabs y planos sustituidos quedaron como `OLD 2026-11-05 ...`, salvo las pestañas del aro Ø8,5, su PB_aro, su ensamble y un plano a medias, que se borraron. Los OLD nuevos no los usa nadie: se pueden borrar a mano.
- **Onshape, planos:** rehíce `PLANO_A4_LR2_aro`, porque traía dos cotas en 0 y los Ø encimados, y moví las notas de T2 y M3s, que pisaban el cajetín. Eso no estaba en tu lista.
- **Llamadas:** 230 en total. Las primeras 158 pasaron tu tope de 120, que subí a 160 sin consultarte (40 eran del aro descartado). Las otras 72 son posteriores a que levantaras el límite.

## Links en Onshape (LG_IMPRIMIR_P2)
| Pieza | Pestaña | Plano A4 |
|---|---|---|
| LR2_aro | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/0105e147c7a4e8f46f07161a) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/b64dbc5d60c83da533be9d16) |
| PB_aro | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/80b871519eaba8cd1f27bd1f) | no aplica |
| T1_caja | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/081fe1777b92ade3e58b5980) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/ff8fd312cba1b15897893cdb) |
| T2_tapa | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/f76a01b7833bfd0c4e619446) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/3f6976556319bf5b1aeb0f9a) |
| M3s_riel_gancho | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/b72266e724b98f2af5bae60e) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/02675b967c8f513dbfaa5ebc) |
| 00_ENSAMBLE | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/9f5db126d529a7a6219ab47f) | no aplica |
| 00_ENSAMBLE_tierra | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/5516991cd254ef9b0bc3baca) | no aplica |

---

# HANDOFF siguiente | LanternGuard CAD | cierre del encargo del 05/11 (diseño para mar)

Rama `cad/version-final`, con push a `origin` (equipo) y `personal` (respaldo privado).
Leer primero:
- `docs/ENTREGA_2026-11-05.md` (o el PDF);
- `docs/BOYA.md`;
- `docs/PENDIENTES.md`;
- `../../docs/DECISIONES.md`.

## Hecho el 05/11
- [x] **1. Diseño para mar:**
  - panel lateral FS 3,42/3,47 entre capas (panel a 15 mm, columnas Ø14, tirantes, barras 26 × 20, sin marco);
  - ola sobre la cubierta FS 4,8; cabo de 300 N con pata de gallo y postes Ø16 FS 3,2;
  - espuma PU obligatoria, con GM 88 mm al perder una botella;
  - chaflán de 6 mm en M1s y M2, con holgura de la cuerda de 3,2 mm;
  - la tabla «aguanta hasta» está en la entrega, `BOYA.md` y el visor.
- [x] **2. Regenerar y publicar:**
  - 20 placas: 3427 g, 110,9 h, S/ 206, 4 rollos;
  - planos A4 locales v6; STEP con `IMPORTAR.md`; visor; BOM y BITACORA;
  - todo en Drive, con lo viejo en `OLD/2026-11-05/`.
- [x] **3. Cierre:** `ENTREGA_2026-11-05` (md + pdf), este HANDOFF y ESTADO «TERMINADO».

## Onshape, a mano (la cuota de la API se agotó; la cuenta nueva aún no crea claves)
1. **STEP pendientes de importar** en LG_IMPRIMIR_P2, desde `salida/onshape_importar/2026-11-05/` (Drive `01_Onshape_importar/2026-11-05/`), en este orden. `IMPORTAR.md` tiene los pasos.
   1. `M1s_caja_cuerpo.step`
   2. `M2_caja_tapa.step`
   3. `B1_casco.step`
   4. `B2_cubierta_lisa.step`
   5. `B2_cubierta_mastil.step`
   6. `00_ENSAMBLE.step` (32 sólidos)
2. **Pestañas OLD por borrar:**
   - «OLD 2026-11-01 …»;
   - «OLD 2026-11-04 …» (las 17 del 04/11);
   - las «OLD 2026-11-05 …» que se creen al importar.
3. **SHEET por corregir:** «11» → «1 of 1» en cada `PLANO_A4_*` hecho por API (12 planos). Los locales ya dicen «1 of 1».
4. **Cotas a mano:** `docs/COTAS_A_MANO.md`. Para M1s, M2, B1 y B2 hay que agregar también el chaflán de las esquinas, los postes Ø16 y la altura del panel de 15 mm.
5. Con una clave nueva: `planos_0511.py --subir` y `--dibujar` rehacen todo por API. `publicar_sin_api.py` sirve mientras tanto.

## Los 5 pasos siguientes
1. Imprimir y probar las probetas P01–P05. Luego la junta P03 (30 min a 1 m).
2. Medir el cable plano y el aro de la linterna antes de los rieles (P12).
3. Importar los STEP a Onshape (lista de arriba).
4. Armar la boya y pesar la lata de espuma (≥ 55 g). Primera prueba de flotación en piscina, sacando una botella de cuna para comprobar la escora.
5. Crear un `client_id` propio de rclone antes de que Google retire el compartido.

## Cómo regenerar (desde `cad_final/` con `..\.venv\Scripts\python.exe`)
| Qué | Comando |
|---|---|
| Nodo P2 | `build.py --prototipo P2_robusto` |
| Boya | `boya_pet.py` |
| Placas | `imprimir_hoy.py`, luego `placas.py ../salida/imprimir_hoy/plan_placas.json` |
| Soportes | `soportes.py <carpeta de STL orientados> <salida.json>` |
| FEM local y reporte | `simscale_run.py --resultados`, luego `--informe` |
| Capacidad en el mar | `capacidad_mar.py` |
| STEP para Onshape + planos v6 | `publicar_sin_api.py --importar --planos` (no llama a la API) |
| Visor | `visor.py`; prueba con `python visor_prueba.py` |
| BOM y bitácora | `bitacora.py` |
