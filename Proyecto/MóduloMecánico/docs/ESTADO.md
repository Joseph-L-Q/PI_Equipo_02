# Estado LanternGuard CAD | documento limpio, sin probetas, juego del aro 0,3 mm por lado (05/11) | **TERMINADO, con 2 pasos a mano**

**Total a imprimir: 3887 g, unas 152 h, 36 piezas.** 4 rollos de 1 kg alcanzan con 113 g de margen, 37 g menos que los 150 g pedidos. No alcanza para repetir una pieza grande.

Documento: [LanternGuard - PIEZAS PARA IMPRIMIR](https://cad.onshape.com/documents/76e36e0130a8d259842ecee7/w/fdd58e8bdf77f39a1781a12d) (did `76e36e0130a8d259842ecee7`, wid `fdd58e8bdf77f39a1781a12d`). El original `LG_IMPRIMIR_P2` no se escribió, y sigue con las probetas y el M3s de asiento Ø16,8.

| Verificación | Resultado | Pedido |
|---|---|---|
| Asiento de M3s | Ø17,1 (aro Ø16,5): 0,3 mm nominal por lado; 0,21 mm reales por la curva del aro | 0,3 por lado |
| FEM riel en el agua, 150 N | FS entre capas 3,95, flecha 1,36 mm (`fem_tet10`, sin CalculiX) | ≥ 3 |
| FEM riel al izar, 150 N | FS entre capas 5,19, flecha 0,21 mm | ≥ 3 |
| Choques | aro-gancho 0 mm³; `simple.py`: 0 interferencias, sin fallas | sin choque |
| Otras piezas del nodo | solo cambió el volumen de M3s | sin cambios |
| Ensambles | nodo 20 + 4 REF, boya 14 + 4 REF, tierra 2 | suma de la BOM |
| Documento | 21 piezas, 21 planos, 3 ensambles, 00_LEEME; 0 referencias rotas, 0 faltantes | sin rotas ni faltantes |

**Pasos a mano en Onshape:**
1. Activar Share > Link con vista y exportación: la API rechaza la clave con un 403.
2. Arrastrar `00_LEEME` al primer lugar: la API no reordena pestañas.

Quedan 24 pestañas `.step`: si se borran, el Part Studio queda en error y con 0 partes (probado).

---

# Estado LanternGuard CAD | aro Ø16,5 con relleno, M3s nuevo, estación de tierra (05/11) | **TERMINADO**

**El proyecto necesita 5 rollos, no 4:** unos 4172 g estimados. Con FS ≥ 3, cada aro pesa 150 g (13 perímetros + 15 % de gyroid), y los 4 rollos pedían unos 70 g.

| Verificación | Resultado | Pedido |
|---|---|---|
| Aro impreso, 2 kg + 150 N, pico de flexión | FS entre capas **3,01** (macizo 3,16) | ≥ 3 |
| Riel M3s en el agua / al izar | FS entre capas **3,94** / 5,19 | ≥ 3 |
| Choque aro-gancho y con la cápsula | ninguno; margen del asiento 0,06 mm por lado | sin choque |
| Aire cuerda-caja | 7,5 mm | ≥ 3 |
| Cama | aro Ø216,5; M3s 140,5 | ≤ 230 |
| Ensamble de tierra | 30 sólidos sin choques; 30 partes en Onshape | sin choques |

Todos los FS salen de `fem_tet10.py` (sin CalculiX en esta PC). La rigidez del gyroid está estimada, sin ensayo.

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

Revisión final del documento: 125 pestañas, sin referencias rotas ni nombres duplicados. Llamadas: 230. El `.env` se borró al terminar. Lo pendiente está en `HANDOFF_siguiente.md` y el detalle en `ARO_Y_ESTACION.md`.

---

# Estado LanternGuard CAD | aros, estación de tierra y planos nuevos (05/11) | **SUPERADO por el bloque de arriba**

**El aro LR2 de 8,5 mm NO cumple:** FS entre capas 0,54 (0,48 en el pico de flexión) con 2 kg + 150 N. No se cambió el diámetro. Propuesta sin aplicar: aro Ø16,5 y asiento Ø16,8. Detalle, supuestos y lista de verificación en `docs/ARO_Y_ESTACION.md`.

| Bloque | Estado |
|---|---|
| LR2_aro y PB_aro | STEP y STL en `salida/aro/`. `aro.seccion` 8,5 real, holgura 0,15: M3s no cambia. No subidos a Onshape ni a Drive |
| T1_caja y T2_tapa | STEP y STL en `salida/tierra/`, 124 g. Medidas del Heltec y la batería sin confirmar. No subidos a Onshape ni a Drive |

## Planos nuevos en LG_IMPRIMIR_P2
Los 5 `PLANO_A4_*` apuntan a las pestañas vigentes. Se borraron los 5 planos viejos y sus OLD (Part Studio y `.step`). Quedan 28 OLD, todas usadas por los «Drawing N» de Melissa, que no se tocaron. Sin referencias rotas. 97 llamadas.

| Pieza | Plano | Cotas por API | Cotas a mano |
|---|---|---|---|
| M1s_caja_cuerpo | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/740f34822d2dbb305df48f48) | 18 | 17 |
| M2_caja_tapa | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/0c80d12f9d8423d7505f19cd) | 10 | 3 |
| B1_casco | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/a00a08da6785d3533161a858) | 20 | 13 |
| B2_cubierta_lisa | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/25e0e3db18a41e920aa0e0c9) | 16 | 9 |
| B2_cubierta_mastil | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/3a048c8e2da45fc76052dda2) | 17 | 19 |

Las cotas a mano no cupieron o salen de bordes curvos. Falta corregir SHEET «11» → «1 of 1» si estos planos heredan ese defecto. No se exportó PDF por API: el vigente sigue siendo `PLANOS_A4_LanternGuard_v6.pdf`.

---

# Estado LanternGuard CAD | limpieza de pestañas OLD en LG_IMPRIMIR_P2 (05/11) | **TERMINADO**

De 91 pestañas OLD se borraron 53 y quedaron 38 (19 Part Studios y sus 19 `.step`). Después de la limpieza, los 28 Drawings no tienen referencias rotas.

**Criterio:** una OLD queda si la usa un Drawing que sigue en el documento. Su `.step` queda con ella porque el Part Studio importado depende de él (`dependsOnBlob`). Los Drawings `OLD … PLANO_A4_*` se borraron porque ninguno los referencia, y con ellos lo que solo ellos usaban. Lo borrado se puede restaurar desde el historial del documento.

## Quedaron (cada una con su `.step`, con el mismo nombre y `.step` al final)

| Drawing que la usa | Nombre actual | Nombre anterior |
|---|---|---|
| Drawing 1 B1_casco | OLD (usado por Drawing 1) B1_casco | OLD 2026-11-04 B1_casco (partida en mitades) |
| Drawing 2 B2_cubierta | OLD (usado por Drawing 2) B2_cubierta | OLD 2026-11-04 B2_cubierta (partida en mitades) |
| Drawing 3 B3_caja | OLD (usado por Drawing 3) B3_caja | OLD 2026-11-04 B3_caja (postes Ø9 y cama útil 230) |
| Drawing 4 B4_tapa | OLD (usado por Drawing 4) B4_tapa | OLD 2026-11-04 B4_tapa (geometría anterior) |
| Drawing 5 B5_cuna | OLD (usado por Drawing 5) B5_cuna | OLD 2026-11-04 B5_cuna (partida en mitades) |
| Drawing 6 B6_correa | OLD (usado por Drawing 6) B6_correa | OLD 2026-11-04 B6_correa (cama útil 230) |
| Drawing 14 M11 | OLD (usado por Drawing 14) M11_bandeja | OLD 2026-11-04 M11_bandeja (riel cerrado estanco) |
| Drawing 15 M11 | OLD (usado por Drawing 15) M11_bandeja_sup | OLD 2026-11-04 M11_bandeja_sup (riel cerrado estanco) |
| Drawing 7 M1s_caja_cuerpo | OLD (usado por Drawing 7) M1s_caja_cuerpo | OLD 2026-11-04 M1s_caja_cuerpo (riel cerrado estanco) |
| Drawing 8 M2 | OLD (usado por Drawing 8) M2_caja_tapa | OLD 2026-11-04 M2_caja_tapa (geometría anterior) |
| Drawing 9 M3s | OLD (usado por Drawing 9) M3s_riel_gancho | OLD 2026-11-04 M3s_riel_gancho (riel cerrado estanco) |
| Drawing 10 M3t | OLD (usado por Drawing 10) M3t_tapa_bolsillo | OLD 2026-11-04 M3t_tapa_bolsillo (geometría anterior) |
| Drawing 11 M4 | OLD (usado por Drawing 11) M4_capsula_cuerpo | OLD 2026-11-04 M4_capsula_cuerpo (riel cerrado estanco) |
| Drawing 12 M5 | OLD (usado por Drawing 12) M5s_capsula_tapa_pie | OLD 2026-11-04 M5s_capsula_tapa_pie (riel cerrado estanco) |
| PLANO_A4_B1_casco | OLD (usado por PLANO_A4_B1_casco) B1_casco | OLD 2026-11-05 B1_casco |
| PLANO_A4_B2_cubierta_lisa | OLD (usado por PLANO_A4_B2_cubierta_lisa) B2_cubierta_lisa | OLD 2026-11-05 B2_cubierta_lisa |
| PLANO_A4_B2_cubierta_mastil | OLD (usado por PLANO_A4_B2_cubierta_mastil) B2_cubierta_mastil | OLD 2026-11-05 B2_cubierta_mastil |
| PLANO_A4_M1s_caja_cuerpo | OLD (usado por PLANO_A4_M1s_caja_cuerpo) M1s_caja_cuerpo | OLD 2026-11-05 M1s_caja_cuerpo |
| PLANO_A4_M2_caja_tapa | OLD (usado por PLANO_A4_M2_caja_tapa) M2_caja_tapa | OLD 2026-11-05 M2_caja_tapa |

## Borradas (53)

**Drawings (15):**
- OLD 2026-11-04 PLANO_A4_B1_casco (geometría anterior)
- OLD 2026-11-04 PLANO_A4_B2_cubierta_lisa (barras de 4 mm, FS 0.4 con la ola)
- OLD 2026-11-04 PLANO_A4_B2_cubierta_lisa (geometría anterior)
- OLD 2026-11-04 PLANO_A4_B2_cubierta_mastil (barras de 4 mm, FS 0.4 con la ola)
- OLD 2026-11-04 PLANO_A4_B2_cubierta_mastil (geometría anterior)
- OLD 2026-11-04 PLANO_A4_B3_caja (geometría anterior)
- OLD 2026-11-04 PLANO_A4_B5_cuna_base (geometría anterior)
- OLD 2026-11-04 PLANO_A4_B5_cuna_cuello (geometría anterior)
- OLD 2026-11-04 PLANO_A4_B6_correa (geometría anterior; vigente: plano local en el PDF v5)
- OLD 2026-11-04 PLANO_A4_M11_bandeja (geometría anterior; vigente: plano local en el PDF v5)
- OLD 2026-11-04 PLANO_A4_M11_bandeja_sup (geometría anterior; vigente: plano local en el PDF v5)
- OLD 2026-11-04 PLANO_A4_M1s_caja_cuerpo (geometría anterior)
- OLD 2026-11-04 PLANO_A4_M3s_riel_gancho (geometría anterior)
- OLD 2026-11-04 PLANO_A4_M4_capsula_cuerpo (geometría anterior)
- OLD 2026-11-04 PLANO_A4_M5s_capsula_tapa_pie (geometría anterior; vigente: plano local en el PDF v5)

**Part Studios (17):**
- OLD 2026-11-04 00_ENSAMBLE (ensamble anterior)
- OLD 2026-11-04 B1_casco (geometría anterior)
- OLD 2026-11-04 B2_cubierta_lisa (barras de 4 mm, FS 0.4 con la ola)
- OLD 2026-11-04 B2_cubierta_lisa (geometría anterior)
- OLD 2026-11-04 B2_cubierta_mastil (barras de 4 mm, FS 0.4 con la ola)
- OLD 2026-11-04 B2_cubierta_mastil (geometría anterior)
- OLD 2026-11-04 B3_caja (geometría anterior)
- OLD 2026-11-04 B5_cuna_base (geometría anterior)
- OLD 2026-11-04 B5_cuna_cuello (geometría anterior)
- OLD 2026-11-04 B6_correa (geometría anterior)
- OLD 2026-11-04 M11_bandeja (geometría anterior)
- OLD 2026-11-04 M11_bandeja_sup (geometría anterior)
- OLD 2026-11-04 M1s_caja_cuerpo (geometría anterior)
- OLD 2026-11-04 M3s_riel_gancho (geometría anterior)
- OLD 2026-11-04 M4_capsula_cuerpo (geometría anterior)
- OLD 2026-11-04 M5s_capsula_tapa_pie (geometría anterior)
- OLD 2026-11-05 00_ENSAMBLE

**STEP (21):**
- OLD 2026-11-01 B2_cubierta (sin chaflan)
- OLD 2026-11-01 B3_caja (sin chaflan)
- OLD 2026-11-01 B5_cuna (sin chaflan)
- OLD 2026-11-01 M1s_caja_cuerpo (sin chaflan)
- OLD 2026-11-04 00_ENSAMBLE.step (ensamble anterior)
- OLD 2026-11-04 B1_casco (geometría anterior).step
- OLD 2026-11-04 B2_cubierta_lisa (barras de 4 mm, FS 0.4 con la ola).step
- OLD 2026-11-04 B2_cubierta_lisa (geometría anterior).step
- OLD 2026-11-04 B2_cubierta_mastil (barras de 4 mm, FS 0.4 con la ola).step
- OLD 2026-11-04 B2_cubierta_mastil (geometría anterior).step
- OLD 2026-11-04 B3_caja (geometría anterior).step
- OLD 2026-11-04 B5_cuna_base (geometría anterior).step
- OLD 2026-11-04 B5_cuna_cuello (geometría anterior).step
- OLD 2026-11-04 B6_correa (geometría anterior).step
- OLD 2026-11-04 M11_bandeja (geometría anterior).step
- OLD 2026-11-04 M11_bandeja_sup (geometría anterior).step
- OLD 2026-11-04 M1s_caja_cuerpo (geometría anterior).step
- OLD 2026-11-04 M3s_riel_gancho (geometría anterior).step
- OLD 2026-11-04 M4_capsula_cuerpo (geometría anterior).step
- OLD 2026-11-04 M5s_capsula_tapa_pie (geometría anterior).step
- OLD 2026-11-05 00_ENSAMBLE.step

---

# Estado LanternGuard CAD | subida a Onshape del 05/11 | **TERMINADO: 6 piezas subidas y verificadas**

Subidas por API a LG_IMPRIMIR_P2 con la clave de Melissa, en el orden de `IMPORTAR.md`: https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff

| Pieza | Partes en Onshape | Sólidos en el STEP | Pestaña |
|---|---|---|---|
| M1s_caja_cuerpo | 1 | 1 | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/44a95b160abfe866f19bf95e) |
| M2_caja_tapa | 1 | 1 | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/55f19eb539b3a82a029f39c1) |
| B1_casco | 1 | 1 | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/ff2a57f172f6f9814e18550a) |
| B2_cubierta_lisa | 1 | 1 | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/ed6cb3efba6bf7742ef61ce8) |
| B2_cubierta_mastil | 1 | 1 | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/b1fba20195398ad4baf6847b) |
| 00_ENSAMBLE | 32 | 32 | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/53a25ac22b33b97a8c87e645) |

**Lo anterior:** cada pieza quedó renombrada `OLD 2026-11-05 <pieza>` (Part Studio y `.step`). No se borró nada.

**Pendiente a mano:**
- Los `PLANO_A4_*` de estas piezas siguen apuntando a la geometría anterior: hay que apuntar cada vista a la pestaña nueva (`IMPORTAR.md`). Los planos vigentes están en `PLANOS_A4_LanternGuard_v6.pdf`.
- Corregir SHEET «11» → «1 of 1» y las cotas a mano (`HANDOFF_siguiente.md`).

---

# Estado LanternGuard CAD | encargo del 05/11 (diseño para mar) | **TERMINADO: 05:32**

Modo sin API de Onshape: las piezas cambiadas quedan como STEP con `IMPORTAR.md` para subirlas a mano.

| Bloque | Estado |
|---|---|
| 1 Diseño para mar | Hecho. Panel lateral 200 N: FS 3,02 entre capas (era 0,41). Ola sobre la cubierta: FS 3,7. Cabo 300 N con pata de gallo de dos ramales: FS 3,2. Espuma PU obligatoria: con una botella perdida GM 85/506 mm (era 38). Holgura cuerda-caja 3,2 mm con chaflán de 6 mm en M1s y M2 |
| 2 Regenerar y publicar | Hecho. 20 placas sin fallas: 3427 g, 110,9 h, S/ 206 (4 rollos de 1 kg). Cubiertas B2 sin soportes (0,1 y 0,4 %). 5 STEP + `00_ENSAMBLE` (32 sólidos) con `IMPORTAR.md` en Drive `01_Onshape_importar/2026-11-05/`. `PLANOS_A4_LanternGuard_v6.pdf` en `04_Planos`. STL por pieza, visor, BITACORA, BOM, BOYA.pdf, reporte de SimScale y CARGAS_CONJUNTO subidos; lo viejo en `OLD/2026-11-05/` |
| 3 Cierre | Hecho. `ENTREGA_2026-11-05.pdf` actualizado, `HANDOFF_siguiente.md` con los STEP por importar, las pestañas OLD, SHEET y cotas a mano |

**Links:** Drive https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO · Onshape https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff · Rama https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

**Problemas abiertos:**
- Si la espuma llena solo la mitad de los huecos, la boya vuelca al perder una botella. Control al armar: pesar la lata antes y después (≥ 55 g de espuma).
- Con una botella perdida la boya escora 11° (criterio propio 10°).
- Onshape: hay que importar a mano 5 STEP y el ensamble (`IMPORTAR.md`).
- La boya impresa pesa 1385 g (antes 1105 g) y tarda 59,7 h.

---

# Estado LanternGuard CAD | encargo del 04/11 noche | **TERMINADO: 22:54**

**Aviso: el total impreso pasa de 3 kg. Son 3132 g en 20 placas (probetas 243 g, nodo P2 1682 g, boya 1207 g), 97,5 h, S/ 188 a S/ 60/kg.**

| Bloque | Estado |
|---|---|
| 1 Correcciones del laboratorio | Hecho. Mínimo 5 mm en elementos esbeltos, revisado en el build, con chaflán de 45°. Boya en mitades con lengüeta, pasadores y tornillos A2. Nodo sin soportes: M1s 22,3 → 0,5 %, M2 1,8 %, M4 1,6 %, M3s 12,2 % (excepción). M3f es nueva. Lastre 980 g |
| 2 Publicar piezas y planos | Hecho. 17 piezas en Onshape, `00_ENSAMBLE` con 32 sólidos (igual que el STEP), 12 planos en Onshape y 5 en local por la cuota. PDF v5, `STL_por_pieza` y `OLD/` en Drive `04_Planos` |
| 3 SimScale | Hecho. 8 corridas en A y B; las descargas dan 403, así que las imágenes son del FEM local, marcado. Nodo con FS entre capas ≥ 3,35. **El golpe lateral sobre el panel no cumple** |
| 4 Visor 3D | Hecho. Drive `07_Documentos/visor/LanternGuard_visor.html` (doble clic). Sin hosting: no hay CLI ni conexión |
| 5 Entrega | Hecho. `ENTREGA_2026-11-05.pdf`, `BITACORA.xlsx` y `BOM.md` en `07_Documentos` |

**Links:**
- Drive: https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO
- Onshape: https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff
- SimScale A: https://www.simscale.com/workbench/?pid=770997415227428031
- SimScale B: https://www.simscale.com/workbench/?pid=5890288887472164333
- Rama: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

**Problemas:**
- El golpe lateral sobre el panel falla (FS 0,41 entre capas).
- La boya con una botella perdida queda con GM 38 (objetivo 40).
- La holgura entre la cuerda y la caja es de 1,5 mm.
- Quedan unas 89 llamadas de Onshape en el año.
- SimScale bloquea las descargas (403).
- Hay que limpiar a mano lo viejo en Onshape y en Drive (`PENDIENTES.md`).

---

# Estado de la sesión LanternGuard CAD (PC de casa, 30/10/2026)

**TERMINADO: 21:52 (reloj de la PC).** Bloques 0 a G listos y con push. Documento para el equipo:
**`docs/LANTERNGUARD_ENTREGA.pdf`** (Drive `07_Documentos` y Onshape `LG_00_LEER_PRIMERO`). Siguiente sesión:
`docs/HANDOFF_siguiente.md`.
Rama `cad/version-final`: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

| Bloque | Estado | Resultado |
|---|---|---|
| 0 Herramientas | listo | Orca nightly, CalculiX, Gmsh, rclone y claves de Onshape funcionan en esta PC |
| A Onshape | listo, con las correcciones 3 y 4 | 10 documentos `LG_*` (nuevos: `LG_00_LEER_PRIMERO` y `LG_boya_PET_v2`). Pestañas ENSAMBLE nuevas con nombres (piezas con su código, REF_ en lo que no se imprime) y verificadas contra el STEP: P0 V1 53 = 53, P0 modular 47 = 47, P1 y P2 31 = 31, P3 y P4 31 = 31 y sistema 36 = 36 (en `ENSAMBLE_v2_completo`: M1m y el umbilical solo entran con `allowFaultyParts`), boya 19 = 19. Links en `docs/LINKS.md` |
| B Prototipos | listo, con las correcciones 1 y 2 (tanda 3, 683ade1) | Linterna sin separador ni ápice (aro + 4 cuerdas a un nudo + cabo), brazos a 45° entre cuerdas con aire ≥ 10 mm a brazo y cápsula; lastre a granel en un bolsillo por lado (`lastre_izq`/`lastre_der`, 1020 a 1150 g para 0.35 kgf); cajas de P1, P3 y P4 más chicas. P2: 1400 g, 46.7 h, S/ 126.0, FS 5.6 / 2.7. P4: 1352 g, 46.0 h, S/ 121.7, FS 4.7 / 2.3. Recomendación igual: P2 piscina, P4 presentar |
| C Boya PET | listo (2.ª vuelta, de1a2e3) | **Recomendada: 4 × 1 L en cruz** (casco + 2 cunas + 4 correas): 863 g, 32.0 h, S/ 77.7; calado 39.5 mm, francobordo 82 mm, GM 112 / 762 mm. Si pierde una botella vuelca sin espuma; con la espuma PU estimada queda estable a 6 a 12°. No cumple 700 g ni 25 h. 4 × 500 ml (720 g, 26.8 h) vuelca sin una botella. Onshape: `LG_boya_PET_v2`. Detalle: `docs/BOYA.md` |
| D Planos | listo | `planos/PLANOS_LanternGuard.pdf`, 27 páginas: portada, P2 (10), P4 (10) y boya 4 × 1 L (6), con las correcciones de la tanda 3. En Drive `07_Documentos` |
| E Lista de impresión | listo | 17 placas sin fallas, **2469 g y 84.7 h**: probetas 207 g / 7.9 h, nodo P2 sin medidas pendientes 1125 g / 34.9 h, rieles (esperan `aro.seccion`) 274 g / 10.4 h, boya 863 g / 31.5 h. LR1 salió de la lista. 3MF y STL en Drive `02_Imprimir_primero_probetas/imprimir_hoy_30oct_v2/` |
| F Documento para el equipo | listo | **`docs/LANTERNGUARD_ENTREGA.pdf`** (7 páginas) en Drive `07_Documentos` y en Onshape `LG_00_LEER_PRIMERO`, junto con PLANOS, BITACORA.xlsx y BOM.md (con P2, P4 y la boya PET) |
| G Cierre | listo | REPORTE_CAD §11, `docs/HANDOFF_siguiente.md` con los 5 siguientes pasos |

## 01/11/2026: corrección de la jefa de práctica (chaflán en la base de los soportes)
- **Qué se cambió:** B2_cubierta, B3_caja, B5_cuna y M1s_caja_cuerpo llevan chaflán a 45° en la base de los soportes:
  - 2 mm donde entra;
  - 1 mm en las costillas de B5 sobre el patín y en el techo de los bolsillos de M1s;
  - nada junto a las contratuercas PG7 de M1s.

  Parámetro `chaflan.base_soportes`.
- **Impresión:** +1,4 g y +5 min en total. Ninguna pieza pasa a necesitar soportes.
- **FEM:** FS sin cambio (riel 5,56 / 2,72, pie 5,04 / 2,47).
- **Onshape:** pestañas `*_v2` y `PLANO_A4_*_v2`.
- **Drive:** `04_Planos/PLANOS_A4_LanternGuard_v3.pdf`.
- **Detalle:** `docs/CORRECCIONES_2026-11-01.md`.

## Recomendación
- **Piscina: nodo P2 robusto.** 1400 g, 46.7 h, S/ 126.0. FS riel 5.6 / 2.7 entre capas, pie 5.0 / 2.5. Lastre 1150 g de tuercas M8.
- **Presentar: nodo P4 estético.** 1352 g, 46.0 h, S/ 121.7. FS 4.7 / 2.3.
- **Boya: 4 botellas de 1 L en cruz + espuma PU.** 863 g, 32.0 h, S/ 77.7. Sin espuma vuelca si pierde una botella.

## Qué imprimir primero
1. Probetas P01 a P05: 207 g, 7.9 h (PB10 sobre la varilla real del aro, PB9 con una botella real de 1 L).
2. Nodo P2 sin medidas pendientes (P06 a P11): 1125 g, 34.9 h. P11 solo si el ángulo queda en 30°.
3. Rieles con gancho (P12): 274 g, 10.4 h, después de medir `aro.seccion`.
4. Boya (P14 a P18): 863 g, 31.5 h; la cuna (P17) se imprime 2 veces.

## Links
- Documento para el equipo (Drive 07_Documentos): https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO
- Onshape LG_00_LEER_PRIMERO: https://cad.onshape.com/documents/b9bce32f5ed7658b40f45777/w/5b938b69e9a7352f33c5075c
- Onshape LG_P2_robusto: https://cad.onshape.com/documents/999b4e78fb31ffdeaf864392/w/5004d17b81ec1ab1c916dc78
- Onshape LG_P4_estetico: https://cad.onshape.com/documents/d8e4b0f024f7efcb8f94ed99/w/fabae97231abb068b21c50e6
- Onshape LG_boya_PET_v2: https://cad.onshape.com/documents/f4e8ac814316f253d53d94e0/w/a972a01f232336138e011bc2
- PR #10: https://github.com/Joseph-L-Q/PI_Equipo_02/pull/10
- Todos: `docs/LINKS.md`. Decisiones: `docs/DECISIONES.md` (raíz del repo). Bloqueos: `docs/PENDIENTES.md`.
