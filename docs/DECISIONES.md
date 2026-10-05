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
