# Estado de la sesión LanternGuard CAD (PC de casa, 30/10/2026)

Última actualización: **21:52** según el reloj de la PC (el 21:25 anterior era estimado; handoff en `docs/HANDOFF_noche.md`). Terminados: 0, A, B, D. En curso: C segunda vuelta (boya con 4 botellas de 500 ml)
y E (falta la parte de la boya). Siguen F (documento para el equipo) y G (cierre).
Rama `cad/version-final`: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

| Bloque | Estado | Resultado |
|---|---|---|
| 0 Herramientas | listo | Orca nightly, CalculiX, Gmsh, rclone y claves de Onshape funcionan en esta PC |
| A Onshape | listo, con las correcciones 3 y 4 | 9 documentos `LG_*` (nuevo: `LG_boya_PET_v2`). Pestañas ENSAMBLE nuevas con nombres (piezas con su código, REF_ en lo que no se imprime) y verificadas contra el STEP: P0 V1 53 = 53, P0 modular 47 = 47, P1 y P2 31 = 31, P3 y P4 31 = 31 y sistema 36 = 36 (en `ENSAMBLE_v2_completo`: M1m y el umbilical solo entran con `allowFaultyParts`), boya 19 = 19. Links en `docs/LINKS.md` |
| B Prototipos | listo, con las correcciones 1 y 2 (tanda 3, 683ade1) | Linterna sin separador ni ápice (aro + 4 cuerdas a un nudo + cabo), brazos a 45° entre cuerdas con aire ≥ 10 mm a brazo y cápsula; lastre a granel en un bolsillo por lado (`lastre_izq`/`lastre_der`, 1020 a 1150 g para 0.35 kgf); cajas de P1, P3 y P4 más chicas. P2: 1400 g, 46.7 h, S/ 126.0, FS 5.6 / 2.7. P4: 1352 g, 46.0 h, S/ 121.7, FS 4.7 / 2.3. Recomendación igual: P2 piscina, P4 presentar |
| C Boya PET | listo (2.ª vuelta, de1a2e3) | **Recomendada: 4 × 1 L en cruz** (casco + 2 cunas + 4 correas): 863 g, 32.0 h, S/ 77.7; calado 39.5 mm, francobordo 82 mm, GM 112 / 762 mm. Si pierde una botella vuelca sin espuma; con la espuma PU estimada queda estable a 6 a 12°. No cumple 700 g ni 25 h. 4 × 500 ml (720 g, 26.8 h) vuelca sin una botella. Onshape: `LG_boya_PET_v2`. Detalle: `docs/BOYA.md` |
| D Planos | listo | `planos/PLANOS_LanternGuard.pdf`, 27 páginas: portada, P2 (10), P4 (10) y boya 4 × 1 L (6), con las correcciones de la tanda 3. En Drive `07_Documentos` |
| E Lista de impresión | listo | 17 placas sin fallas, **2469 g y 84.7 h**: probetas 207 g / 7.9 h, nodo P2 sin medidas pendientes 1125 g / 34.9 h, rieles (esperan `aro.seccion`) 274 g / 10.4 h, boya 863 g / 31.5 h. LR1 salió de la lista. 3MF y STL en Drive `02_Imprimir_primero_probetas/imprimir_hoy_30oct_v2/` |
| F Documento para el equipo | listo | **`docs/LANTERNGUARD_ENTREGA.pdf`** (7 páginas) en Drive `07_Documentos` y en Onshape `LG_00_LEER_PRIMERO`, junto con PLANOS, BITACORA.xlsx y BOM.md (con P2, P4 y la boya PET) |
| G Cierre | pendiente | |

## Recomendación (bloque B)
- **Pruebas en piscina: P2 robusto.** 14 piezas, 1381 g, 47.3 h, 124 soles. FS riel 5.6 / 2.7 entre capas, pie 5.0 / 2.5.
- **Presentar: P4 estético.** Caja y riel en una pieza, redondeos, logo. 1332 g, 45.8 h, 120 soles. FS 4.7 / 2.3.
- Descartados: P1 mínimo (FS entre capas 1.9) y P3 monocasco (P4 es P3 con acabado).

## Qué imprimir primero (P2, placas ya cortadas)
1. Probetas: PB7 holguras, PB8 inserto M4, PB6 junta, PB10 tramo de riel con el gancho (sobre la varilla real),
   PB9 bahía de botella (con una botella real). 5 placas, 214 g, 7.9 h.
2. Sin medidas pendientes: bisel y bandejas, tapas del bolsillo, cápsulas, tapa de la caja, caja (17 h), tapas de
   cápsula con pie (condicional al ángulo de 30°). 6 placas, 1106 g, 35.5 h.
3. Espera `aro.seccion`: rieles con gancho y separador LR1. 2 placas, 311 g, 12.0 h.
4. Boya: después de la 2.ª vuelta.

## Links
- Onshape LG_P2_robusto: https://cad.onshape.com/documents/999b4e78fb31ffdeaf864392/w/5004d17b81ec1ab1c916dc78
- Onshape LG_P4_estetico: https://cad.onshape.com/documents/d8e4b0f024f7efcb8f94ed99/w/fabae97231abb068b21c50e6
- Drive LanternGuard_CAD: https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO
- Todos: `docs/LINKS.md`. Decisiones: `docs/DECISIONES.md` en la raíz del repo. Bloqueos: `docs/PENDIENTES.md`.
