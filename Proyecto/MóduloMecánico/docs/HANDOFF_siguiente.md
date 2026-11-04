# HANDOFF siguiente | LanternGuard CAD | 04/11/2026, cierre 11:50

Rama `cad/version-final`, con push a `origin` (equipo) y a `personal` (respaldo privado `IchiSieben/LanternGuard-CAD-backup`).
Leer primero:
- `docs/ENTREGA_2026-11-04.md` (o el PDF), que resume todo para el equipo;
- `docs/PENDIENTES.md`;
- `docs/DECISIONES.md`, en la raíz del repo.

## Hecho el 04/11 (cola completa)
- **Bloque 0:** respaldo privado y `RETOMAR_EN_OTRA_PC.md`, con la clave de SimScale y el SDK desde git. La rama `cad/celosia-v2` congela el concepto anterior.
- **Bloque 1, márgenes y boya:**
  - cama útil de 230 con chequeo (`cama.py` corre en `build.py`) y `MARGENES.md`;
  - B1, B2 y B5 en mitades, topes bajos en vez de varillas de 2,4 mm, postes de Ø10 con collar.
- **Bloque 1-FINAL, riel cerrado (commit 2534d00):**
  - un solo volumen seco y `riel.tipo = "cerrado" | "celosia"`;
  - riel de 36 × 30 con canal de 24 × 18;
  - juntas planas Ø2 en las uniones riel–caja y riel–silla, con 4 M4 y 4 M3 a ≤ 40 mm;
  - pase del cable de 8 × 22 con borde R10, y sin PG7 entre caja y cápsula;
  - ventana M7 con anillo plano de silicona y silicona marina;
  - bandeja M11 corregida (postes pasantes con M3 × 38, sin la ventana en ocho);
  - perfil Orca estanco (`impresion.estanca`);
  - FS entre capas: riel 3,18, izado 5,47, pie 3,80;
  - lastre de 1050 g.
- **Bloque 2, nombres:** lo vigente va sin sufijo, lo reemplazado está en LG_HISTORICO como «OLD 2026-11-04 …» y la pestaña CAMBIOS dice qué Drawing a mano de Melissa quedó desactualizado.
- **Bloque 3, SimScale por API** (`cad_final/simscale_run.py`):
  - proyectos A «LanternGuard nodo sumergido» y B «LanternGuard boya»;
  - la cubierta B2 fallaba con la ola de 200 N, así que las barras pasaron de 4 a 8 mm y ahora da FS 3,0;
  - `docs/REPORTE_SIMSCALE_LanternGuard.pdf` está en Drive `06_SimScale`.
- **Bloque 4, visor 3D:** `docs/visor/index.html` (se regenera con `cad_final/visor.py`) en Drive `07_Documentos/visor/`.
- **Bloque 5, cierre:** `docs/ENTREGA_2026-11-04.md` y PDF en Drive `07_Documentos`.
- **Planos:**
  - 15 `PLANO_A4_<pieza>` nuevos en LG_IMPRIMIR_P2, en formato del equipo (`cad_final/planos_0411.py`);
  - `04_Planos/PLANOS_A4_LanternGuard_v4.pdf` y `04_Planos/STL_por_pieza/`.
- **Placas:** 19, con **2846 g y 96,1 h** (más de 2,7 kg). Están en Drive `02_Imprimir_primero_probetas/imprimir_hoy_04nov_riel_cerrado/`.

## Siguiente (en orden)
1. **Manual en Onshape:**
   - borrar las pestañas «OLD …» de LG_IMPRIMIR_P2, porque la API no puede borrar;
   - en los planos nuevos, cambiar SHEET de «11» a «1 of 1»;
   - completar las cotas de `salida/planos_onshape/COTAS_A_MANO_A4_v4.md`;
   - en B1 hay textos de cota que se pisan.
2. **Antes de imprimir el nodo:**
   - medir el cable plano real (el canal deja 22 mm planos × 18 de alto y el pase mide 8 × 22);
   - comprar cordón NBR Ø2 y lámina de silicona de 1 mm;
   - imprimir la probeta de junta P03 y hacer la prueba de `ESTANQUEIDAD.md`.
3. **Decidir si el golpe lateral de 200 N sobre el panel solar es un requisito.** Si lo es, rehacer las columnas del panel o ponerle tirantes.
4. **Pesar el granel del lastre comprado**; el rango válido es de 870 a 1220 g.
5. **P3 y P4 (monocasco)** siguen con el riel anterior. Hacer esto solo si se presenta P4 impreso.

## Cómo regenerar
Todo se corre desde `cad_final/` con `..\.venv\Scripts\python.exe`.

| Qué | Comando |
|---|---|
| Nodo P2 (CAD, slicer, FEM, ficha y cama) | `build.py --prototipo P2_robusto` |
| Boya | `boya_pet.py` |
| Placas | `imprimir_hoy.py`, luego `placas.py ../salida/imprimir_hoy/plan_placas.json` |
| Guía de piezas y estanqueidad | `guia_piezas.py` |
| Visor 3D | `visor.py` |
| Márgenes | `margenes.py` |
| BOM | `bitacora.py` |
| SimScale | `simscale_run.py --pieza X`; informe con `--informe` (pisa las ediciones a mano del reporte) |
| Planos A4 | `planos_0411.py --dibujar <codigos>` y luego `--unir` |
