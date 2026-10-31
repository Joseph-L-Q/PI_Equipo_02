# HANDOFF siguiente | LanternGuard CAD | después del 30/10/2026 (noche)

Rama `cad/version-final` (PR #10 a main), todo con push. Leer primero `docs/LANTERNGUARD_ENTREGA.pdf` (resumen, tablas,
links) y `docs/ESTADO.md`. Decisiones de la noche: `docs/DECISIONES.md` (raíz del repo). Bloques 0 a G del
HANDOFF_2026-10-30_v2 terminados; REPORTE_CAD §11 tiene el detalle.

## Estado
- Nodo: P2 robusto para la piscina, P4 estético para presentar. Correcciones 1 a 4 aplicadas.
- Boya: 4 × 1 L en cruz + espuma PU (863 g, 32 h). Se vuelve a 500 ml con `flotacion.botella = "500ml"`.
- Impresión: 17 placas cortadas (2469 g, 84.7 h). 3MF en Drive `02_Imprimir_primero_probetas/imprimir_hoy_30oct_v2/`.
- Onshape: abrir `LG_00_LEER_PRIMERO`; en P3, P4 y sistema usar la pestaña `ENSAMBLE_v2_completo`.

## Los 5 siguientes pasos
1. **Imprimir el grupo 1 (probetas P01 a P05, 207 g, 7.9 h)** y anotar resultados: holgura que entra justa (PB7), inserto
   M4 (PB8), cierre de la junta (PB6), PB10 sobre la varilla real del aro, PB9 con una botella real de 1 L.
2. **Medir** `aro.seccion` (calibrador sobre la varilla), el KIT A con la ESP32 puesta, el PG7 y la densidad a granel de
   las tuercas M8 (pesar un vaso lleno). Cargar en `params.py` y correr `python cad_final/build.py --prototipo P2_robusto`.
3. **Decidir con el equipo**: ángulo de cápsula 30° o 70° (P11 espera esto), límite de peso (nodo ≤ 3 kg y boya aparte),
   botella 1 L o 500 ml, y qué hacer con la cuerda a 2.9 mm de la brida (opciones a, b, c en `docs/PROTOTIPOS.md`).
4. Con las probetas bien: imprimir el grupo 2 (nodo P2 sin medidas pendientes, 1125 g, 34.9 h) y después P12 (rieles).
   Volver a cortar con `python cad_final/imprimir_hoy.py` y `python cad_final/placas.py ../salida/imprimir_hoy/plan_placas.json`
   si cambió alguna medida.
5. Pendientes chicos: arreglar `cad_final/variantes.py` (firmas viejas); mover a mano en Onshape los 2 documentos viejos
   a `LanternGuard/_historico` y arrastrar las pestañas de ensamble al primer lugar; crear un `client_id` propio de
   rclone (el compartido se retira en 2026); poner precios en la hoja HARDWARE de BITACORA.xlsx.
