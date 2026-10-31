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
