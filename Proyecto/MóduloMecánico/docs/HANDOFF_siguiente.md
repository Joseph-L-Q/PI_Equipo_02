# HANDOFF siguiente | LanternGuard CAD | cierre del encargo del 04/11 noche

Rama `cad/version-final`, con push a `origin` (equipo) y `personal` (respaldo privado).
Leer primero:
- `docs/ENTREGA_2026-11-05.md` (o el PDF), que resume todo;
- `docs/PENDIENTES.md`;
- `../../docs/DECISIONES.md`.

## Hecho en el encargo (5 bloques)
- [x] **1. Correcciones del laboratorio:**
  - mínimo 5 mm en elementos esbeltos, revisado en el build (`esbelto.py` + `esbelto_nodo.py`, 32 elementos, 0 bajo 5);
  - chaflanes de 45° en la base;
  - boya en mitades con lengüeta, pasadores y tornillos A2;
  - nodo sin soportes (M1s 22,3 → 0,5 %; M3s 12,2 % como excepción) y pieza nueva M3f;
  - FS entre capas ≥ 3,35 en el nodo y lastre de 980 g;
  - 20 placas, **3132 g (más de 3 kg)**, 97,5 h, S/ 188.
- [x] **2. Onshape:**
  - 17 pestañas reemplazadas y `00_ENSAMBLE` con 32 sólidos (igual que el STEP);
  - 12 `PLANO_A4` hechos en Onshape y 5 en local, por la cuota: **quedan ~89 llamadas en 2026**;
  - `PLANOS_A4_LanternGuard_v5.pdf`, `STL_por_pieza/` con LEEME y lo viejo copiado en `OLD/`;
  - `MARGENES` y `COTAS_A_MANO` (md + pdf).
- [x] **3. SimScale:**
  - las 8 corridas en los proyectos A y B, pero las descargas dan 403, así que las imágenes son del FEM local marcado;
  - el golpe lateral sobre el panel NO cumple;
  - `REPORTE_SIMSCALE_LanternGuard.pdf` y `CARGAS_CONJUNTO.pdf` en Drive `06_SimScale`.
- [x] **4. Visor:**
  - `docs/visor/` (index.html + datos.json + modelo.glb) y `LanternGuard_visor.html` de un solo archivo (3,7 MB);
  - en Drive `07_Documentos/visor/`;
  - el hosting no estaba disponible: no hay CLI de Hostinger y el MCP no conectó.
- [x] **5. Entrega:** `ENTREGA_2026-11-05` (md + pdf), `BITACORA.xlsx` y `BOM.md` con los herrajes de la boya PET y de M3f.

## Los 5 pasos siguientes
1. **Imprimir y probar las probetas** (P01–P05). Después, la prueba de la junta P03 con el cordón NBR Ø2 comprado, de 30 min a 1 m (`ESTANQUEIDAD.pdf`).
2. **Medir el cable plano real y el aro de la linterna** antes de imprimir los rieles (P12). El canal deja 22 × 18 mm.
3. **Decidir el golpe lateral sobre el panel** (bajar el panel, columnas más gruesas o tirantes) y la estabilidad de la boya con una botella perdida (GM 38 < 40). Luego correr `simscale_run.py --grupo B`.
4. **Onshape a mano:**
  - borrar las pestañas «OLD 2026-11-04 …»;
  - corregir SHEET a «1 of 1»;
  - completar `COTAS_A_MANO.md`;
  - con cuota nueva, `planos_0511.py --dibujar M5s_capsula_tapa_pie,...` para los 5 planos locales.
5. **Drive a mano:** borrar los originales viejos que ya están en `OLD/` (lista en `PENDIENTES.md`) y crear un `client_id` propio de rclone antes de que Google retire el compartido.

## Cómo regenerar (desde `cad_final/` con `..\.venv\Scripts\python.exe`)
| Qué | Comando |
|---|---|
| Nodo P2 (CAD, slicer, FEM, cama, espesores) | `build.py --prototipo P2_robusto` |
| Boya | `boya_pet.py` |
| Placas | `imprimir_hoy.py`, luego `placas.py ../salida/imprimir_hoy/plan_placas.json` |
| Soportes por pieza | `soportes.py ../salida/imprimir_hoy ../salida/soportes_despues.json`; comparar con `--comparar` |
| Guía y estanqueidad | `guia_piezas.py` |
| Márgenes | `margenes.py` |
| BOM y bitácora | `bitacora.py` |
| SimScale | `simscale_run.py --todo`, o `--grupo A/B`; `--resultados` rehace las imágenes y el reporte sin gastar |
| Visor | `visor.py` (llama a `visor_datos.py`); prueba con `python visor_prueba.py` |
| Planos | `planos_0511.py` (ver docstring) |
