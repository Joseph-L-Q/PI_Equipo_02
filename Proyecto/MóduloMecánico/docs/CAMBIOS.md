# CAMBIOS: LanternGuard CAD

Hay una línea por fecha, con qué cambió y por qué. Lo vigente no lleva sufijo. Lo reemplazado está en el documento de Onshape
**LG_HISTORICO** como "OLD <fecha> <pieza> (<motivo>)" y en la rama `cad/celosia-v2` de git.

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 2026-10-29 | Hay 4 prototipos del nodo: P1 mínimo, P2 robusto, P3 monocasco y P4 estético. Linterna con aro y 4 cuerdas. | Comparar peso, horas y FS antes de imprimir. P2 queda para la piscina y P4 para presentar. |
| 2026-10-30 | La boya pasa a 4 botellas de 1 L en cruz con espuma PU (B1 a B6). | Con 2 botellas, la boya volcaba al perder una. La cruz da GM 112 / 762 mm y francobordo de 82 mm. |
| 2026-10-31 | Concha estética SKIN_concha sobre la caja de P2 (34,9 g). | Apariencia para la presentación sin tocar la pieza estructural. |
| 2026-11-01 | Chaflán de 45° en la base de los soportes de B2, B3, B5 y M1s. | Observación de la jefa de práctica: evita que los soportes se quiebren en la unión con la base. |
| 2026-11-02 | Melissa rehízo a mano los planos A4 de LG_IMPRIMIR_P2 ("Drawing 1 B1_casco" … "Drawing 16 SKIN"). | Formato del equipo y notas corregidas a mano. |
| 2026-11-04 | Nueva convención de nombres: lo vigente va sin `_v2`, `_v3` ni `zz_`, y lo viejo pasa a LG_HISTORICO. La rama `cad/celosia-v2` congela el concepto actual (riel en celosía y caja con PG7). | Que nadie imprima una versión vieja por confusión de nombres, y que el concepto anterior se pueda recuperar entero antes de la corrección de concepto. |
| 2026-11-04 | **B1_casco** pasa a dos mitades iguales (se imprimen 2). El "Drawing 1 B1_casco" de Melissa muestra la pieza entera y quedó desactualizado. | La pieza entera no cabía en la cama útil de 230 mm. Reemplaza: `PLANO_A4_B1_casco`. |
| 2026-11-04 | **B2_cubierta** pasa a dos piezas: `B2_cubierta_lisa` y `B2_cubierta_mastil`. "Drawing 2 B2_cubierta" quedó desactualizado. | Cama útil de 230 mm. Reemplazan: `PLANO_A4_B2_cubierta_lisa` y `PLANO_A4_B2_cubierta_mastil`. |
| 2026-11-04 | **B5_cuna** pasa a dos piezas: `B5_cuna_base` y `B5_cuna_cuello` (2 de cada una). "Drawing 5 B5_cuna" quedó desactualizado. | Cama útil de 230 mm. Reemplazan: `PLANO_A4_B5_cuna_base` y `PLANO_A4_B5_cuna_cuello`. |
| 2026-11-04 | **B3_caja** cambió: postes de la bandeja Ø9 (antes Ø8). "Drawing 3 B3_caja" quedó desactualizado. | Más material alrededor del inserto. Reemplaza: `PLANO_A4_B3_caja`. |
| 2026-11-04 | **B6_correa** mide 14 × 106 mm (antes 104). "Drawing 6 B6_correa" quedó desactualizado. | Cama útil y márgenes. Reemplaza: `PLANO_A4_B6_correa`. |
| 2026-11-04 | **M1s_caja_cuerpo** cambió con el riel cerrado y estanco. "Drawing 7 M1s_caja_cuerpo" quedó desactualizado. | Corrección de concepto 3a. Reemplaza: `PLANO_A4_M1s_caja_cuerpo`. |
| 2026-11-04 | **M3s_riel_gancho** cambió (riel cerrado, alma de 26 mm). "Drawing 9 M3s" quedó desactualizado. | Corrección de concepto 3a. Reemplaza: `PLANO_A4_M3s_riel_gancho`. |
| 2026-11-04 | **M4_capsula_cuerpo** cambió (sin agujero PG7, asiento de ventana de 3,8 mm). "Drawing 11 M4" quedó desactualizado. | Corrección de concepto 3a. Reemplaza: `PLANO_A4_M4_capsula_cuerpo`. |
| 2026-11-04 | **M5s_capsula_tapa_pie** cambió (silla y tapa de la cápsula). "Drawing 12 M5" quedó desactualizado. | Corrección de concepto 3a. Reemplaza: `PLANO_A4_M5s_capsula_tapa_pie`. |
| 2026-11-04 | **M11_bandeja** y **M11_bandeja_sup** cambiaron (poste separador pasante). "Drawing 14 M11" y "Drawing 15 M11" quedaron desactualizados (los dos dicen solo "M11"). | Corrección de concepto 3a. Reemplazan: `PLANO_A4_M11_bandeja` y `PLANO_A4_M11_bandeja_sup`. |
| 2026-11-04 | Los dibujos de Melissa que siguen vigentes: Drawing 4 (B4), 8 (M2), 10 (M3t), 13 (M6) y 16 (SKIN). | Esas piezas no cambiaron. |
