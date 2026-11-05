# HANDOFF siguiente | LanternGuard CAD | encargo del 04/11 (noche)

Rama `cad/version-final`. Push a `origin` (equipo) y `personal` (respaldo privado) por bloque.
El encargo completo está en el chat del 04/11 noche; esta es la cola íntegra. [x] = hecho.
Leer también `docs/ESTADO.md`, `docs/PENDIENTES.md`, `../../docs/DECISIONES.md`.

Línea base de soportes: `salida/_soportes_antes/` = copia de los 24 STL de `salida/imprimir_hoy/` ANTES de tocar la geometría.
Cuota Onshape al empezar: 2112 de 2500 llamadas del año (quedan ~388).

## BLOQUE 1. Correcciones del laboratorio
- [ ] 1.1 Mínimo 5 mm en todo elemento vertical/esbelto (topes y nervios del casco, postes del panel, barras, costillas, lengüetas). `margen.esbelto_min` 4 → 5 y check en margenes.py que FALLE el build. Chaflán 45° en la base.
- [ ] 1.2 B1/B2/B5 en mitades ≤ 230 con lengüeta + pasadores + tornillos A2; mitades en visor y planos.
- [ ] 1.3 M1s sin soportes (chaflán 45° bajo voladizos, agujeros horizontales en gota, puentes ≤ 10). Medir soporte en Orca antes/después; dividir con junta sellada solo si sigue > 15 %. Tabla % soporte por pieza antes/después (todas); soportes árbol donde queden.
- [ ] 1.4 Riel cerrado: canal 22 × 18, FS ≥ 3 entre capas (riel, pie, izado); lastre; sellos al día.
- [ ] 1.5 Regenerar STL, 3MF por placa (≤ 230), slicer (g, h, costo por pieza y total), FEM. Si total > 3 kg → primera línea del resumen.

## BLOQUE 2. Publicar piezas y planos
- [ ] 2.1 Onshape LG_IMPRIMIR_P2: piezas vigentes con código, 00_ENSAMBLE nodo + boya (sin REF_), conteo de sólidos vs STEP; PLANO_A4_<pieza> de todas las vigentes, con cota del chaflán; CAMBIOS en LG_00_LEER_PRIMERO. No tocar los Drawings de Melissa.
- [ ] 2.2 Drive 04_Planos: PLANOS_A4_LanternGuard_v5.pdf (portada con índice, cantidades y cotas a mano); STL_por_pieza/ con LEEME.txt y lo viejo copiado a OLD/ (rclone solo copia: los originales viejos quedan listados para borrar a mano). 02_Imprimir: imprimir_hoy_<fecha>/.
- [ ] 2.3 docs/MARGENES.md (bbox, pared mínima, esbeltez) y COTAS_A_MANO.md.

## BLOQUE 3. SimScale con imágenes
- [ ] Proyecto A "LanternGuard nodo sumergido": M3s, M5s, M1s; 150 N en el gancho + corriente 1,5 m/s. Proyecto B "LanternGuard boya": B3, B2 mitades, mástil del panel; peso + ola 200 N + golpe lateral sobre el panel (cumple sí/no). Geometría del bloque 1.
- [ ] 4 imágenes por pieza: von Mises, desplazamiento, malla, condiciones de borde. Cadena: API + PyVista → Playwright → FEM local marcado "FEM local (SimScale no exportó)".
- [ ] Tabla: σmax, FS = 50/σmax, desplazamiento, FS entre capas, local vs SimScale.
- [ ] docs/CARGAS_CONJUNTO.pdf (ISO con flechas a escala y camino de carga numerado).
- [ ] REPORTE_SIMSCALE_LanternGuard.pdf a Drive 06_SimScale con links.

## BLOQUE 4. Manual interactivo 3D
- [ ] cad_final/visor_datos.py → docs/visor/datos.json; index.html (three.js fijo, cdnjs) + modelo.glb (malla por pieza con código, sellos en rojo, REF_ gris translúcido) + versión de un archivo (GLB base64 si < 15 MB).
- [ ] Pestañas PIEZAS, JUNTAS, ENSAMBLE (animado, explotar/armar), IMPRESIÓN, PRUEBAS, RESULTADOS; clic en pieza → panel; claro/oscuro; celular; < 5 s.
- [ ] Hosting: sin hostinger CLI y con el MCP caído → Drive 07_Documentos/visor/.

## BLOQUE 5. Entrega
- [ ] docs/ENTREGA_2026-11-05.md + PDF; respuesta de 5 líneas para la profesora.
- [ ] BITACORA.xlsx y BOM.md (tornillos, cordón NBR, lámina de silicona, PG7, insertos).
- [ ] HANDOFF_siguiente.md con los 5 siguientes pasos; ESTADO.md "TERMINADO" con hora; resumen de 15 líneas.
