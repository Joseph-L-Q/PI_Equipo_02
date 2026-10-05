# Decisiones tomadas sin el grupo (sesión nocturna 4–5 oct 2026)

Las tomó Claude en modo autónomo y queda pendiente que el grupo las confirme. El detalle está en `Proyecto/MóduloMecánico/README.md` (decisiones A/B y supuestos) y en `docs/estado-2026-10-04.md` (supuestos para confirmar). Casi todas se revierten cambiando una línea de `Proyecto/MóduloMecánico/cad/params.py` y corriendo `python build.py`.

| Fecha | Tarea | Qué se eligió | Por qué | Qué se descartó | Cómo revertir |
|---|---|---|---|---|---|
| 2026-10-04 | CAD cápsula | Cavidad de 38 × 38 × 50 (M4 = P4 rev. B) | La P4 del T01 (46 × 34 × 22) no aloja la cámara de 33 × 33 con su lente, y la tuerca PG7 necesita fondo | Mantener la P4 original | Cambiar `CAP_CAV_*` en `params.py` |
| 2026-10-04 | CAD bisagra | Eje detrás de la cápsula, en la tapa trasera y fuera del sello | Con el eje arriba, la cápsula chocaba con el brazo a 90° | Eje arriba como en la P4 | Mover la lengüeta en `capsule_lid` (`parts.py`) |
| 2026-10-04 | CAD bisagra | 36 dientes (10°) y trabajo a 40° | Una posición fija cada 10° es fácil de reproducir con guantes | Fricción continua | `HINGE_TEETH` y `CAM_TILT_DEG` (múltiplo de 10) |
| 2026-10-04 | CAD ventana | Disco plano | Barato, fácil de sellar y reemplazable | Domo que pide la rev. 3 | Solo cambia el asiento: `WIN_*` |
| 2026-10-04 | CAD montaje | Apoyo sobre el aro de una linterna de Ø500 mm, brazos de 190 mm | La rev. 3 dice que va sobre el aro; Ø0.5 m sale de la ref. [1] | Sujeción al cabo (`Entregable1`) | `LANTERN_RING_D`, `ARM_LEN` |
| 2026-10-04 | CAD nombres | Piezas M1 a M8, con una tabla de equivalencia a P1 a P5 del T01 | Evitar confusión con la numeración del equipo | Reusar P1 a P8 | Renombrar los `stem` en `build.py` |
| 2026-10-04 | Material | PETG con E = 1700 MPa y σy = 45 MPa (valores del T01) | Son los que ya usa la Pieza 4; ninguna versión cita fuente | Los de Antezana (2.1 GPa, 50 MPa) | `PETG_YIELD` en `params.py` y E en `build.py` |
| 2026-10-04 | Pendiente | El paso libre para el cabo **no se resolvió** | Necesita una decisión de grupo: desplazar la caja, ranura en U o tubo sellado | — | — |

Nada se subió a GitHub: los commits están solo en la rama local `yoichi/diseno-mecanico`.

## Sesión del 5 oct 2026 (vistas, planos, PPT de entrega)

| Fecha | Tarea | Qué se eligió | Por qué | Qué se descartó | Cómo revertir |
|---|---|---|---|---|---|
| 2026-10-05 | Planos | Proyección HLR de OpenCASCADE + lámina dibujada con matplotlib (`cad/planos.py`) | FreeCAD no está instalado y la ruta OCP no necesita instalar nada; cada cota se comprueba sobre la superficie del STEP y contra `params.py` | FreeCAD TechDraw headless; plano en Onshape (necesita a Yoichi) | Hacer los planos en Onshape y reemplazar los PNG/PDF de `planos/` |
| 2026-10-05 | Planos | Lámina 2 con vista desde la ventana además de frontal, superior y corte, y un detalle B 4:1 de la ranura | La ranura de la junta (2.6 × 1.5) no se lee a 1:1 | Solo 3 vistas | Borrar `side`/detalle en `sheet_capsule()` |
| 2026-10-05 | Planos | Globo 8 (M8) en un detalle aparte a 1:10 | M8 es del banco de prueba, no está en `ENSAMBLE_modulo` | Omitir M8 del plano | Quitar el bloque "M8" en `sheet_assembly()` |
| 2026-10-05 | Vistas | Colores tipo Onshape: rojo #C0392B (M1, M4), negro (M3), gris claro (M2, M5, M6), acrílico translúcido (M7) | Pedido explícito; los colores del STEP tienen la tapa casi blanca, que se pierde en fondo blanco | Colores exactos del STEP | `COLOR` en `cad/vistas.py` |
| 2026-10-05 | PPT | "abrazaderas" → "correa de velcro" también en la diapo 9 (además de 6 y 17) | El prompt decía diapos 5 y 17, pero la palabra estaba en 6, 9 y 17; se dejó coherente en todas | Cambiar solo 2 diapos | `REPLACE` en `parcial/tools/build_entrega.py` |
| 2026-10-05 | PPT | Video reinsertado con PowerPoint por COM (XML nativo), autoplay "con la anterior" como primer efecto | Diagnóstico: FINAL en disco sí tiene el video (media1.mp4 H.264 12 s, relaciones, autoplay y póster correctos; PowerPoint lo exporta con su póster). El texto de instrucción ("VIDEO (12 s) ... insertar_video.py") es el marcador `Video hueco texto` de la **v3**: lo más probable es que se abriera la v3 o un FINAL anterior a la inserción. Se reinsertó con COM para que el XML sea el nativo de PowerPoint | Dejar el video de python-pptx | `insertar_video.py` (versión anterior) |
| 2026-10-05 | Taller 03.1 | Estación de Davenport, Iowa (AQS 191630015, POC 3), 360 días de 2023 | Una sola estación con el año casi completo (≥ 330 días), como pedía la consigna | Otras estaciones con menos días | Cambiar el filtro de estación en `Regresion_PM25_Palacios.ipynb` y reejecutar |
| 2026-10-05 | Taller 03.1 | Columna CBSA vacía en el CSV | El archivo masivo de la EPA no trae el código numérico; no se inventó | Rellenarla a mano | Completar desde la tabla CBSA de la EPA |
| 2026-10-05 | Taller 04 | TrashNet vidrio/plástico a 144 × 192 en CPU (~10 min) | Sin GPU; con el tamaño original pasaba de 20 min | Imagen completa | Cambiar el tamaño en el notebook y reejecutar |
| 2026-10-05 | Taller 05 | Act. 05 (LED desde la web) documentada con Ubidots | La consigna no fija plataforma | Arduino Cloud o ThingSpeak | Editar la sección Act. 05 del readme y el sketch |
