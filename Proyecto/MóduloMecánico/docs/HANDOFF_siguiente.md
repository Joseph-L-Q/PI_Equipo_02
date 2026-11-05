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
