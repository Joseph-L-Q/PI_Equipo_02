# Estado de la sesión LanternGuard CAD (PC de casa, 30/10/2026)

Última actualización: **21:21** según el reloj de la PC (el 21:25 anterior era estimado; handoff en `docs/HANDOFF_noche.md`). Terminados: 0, A, B, D. En curso: C segunda vuelta (boya con 4 botellas de 500 ml)
y E (falta la parte de la boya). Siguen F (documento para el equipo) y G (cierre).
Rama `cad/version-final`: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

| Bloque | Estado | Resultado |
|---|---|---|
| 0 Herramientas | listo | Orca nightly, CalculiX, Gmsh, rclone y claves de Onshape funcionan en esta PC |
| A Onshape | listo; correcciones 3 y 4 hechas en P0, siguen P1 a P4 y la boya | 8 documentos `LG_*` en la carpeta LanternGuard. **P0: pestañas nuevas `ENSAMBLE_v2` (simple V1, 53 partes) y `ENSAMBLE_modular_v2` (47), todas con nombre y REF_ en lo que no se imprime, geometría igual.** Verificación de los ENSAMBLE viejos: P1, P2 y boya coinciden; a P3 y P4 les falta `M1m_caja_con_riel` (se arregla con su ENSAMBLE_v2). Links en `docs/LINKS.md` |
| B Prototipos | listo | Tabla y recomendación en `docs/PROTOTIPOS.md`; fichas en `salida/prototipos/` |
| C Boya PET | listo (2.ª vuelta, de1a2e3) | **Recomendada: 4 × 1 L en cruz** (casco + 2 cunas + 4 correas): 863 g, 32.0 h, S/ 77.7; calado 39.5 mm, francobordo 82 mm, GM 112 / 762 mm. Si pierde una botella vuelca sin espuma; con la espuma PU estimada queda estable a 6 a 12°. No cumple 700 g ni 25 h. 4 × 500 ml (720 g, 26.8 h) vuelca sin una botella. Onshape: `LG_boya_PET_v2`. Detalle: `docs/BOYA.md` |
| D Planos | boya lista; P2 y P4 esperan las correcciones | Boya 4 × 1 L: 6 láminas nuevas en `planos/cad_final/BP/` (B5 cuna y B6 correa nuevas; soportes corregidos en B1 y B5). El PDF único se une al final con P2 y P4 |
| E Lista de impresión | boya lista; nodo P2 espera las correcciones | Boya en 5 placas sin fallas: casco (213.6 g, 7.4 h), cubierta (119.0 g, 5.8 h), caja y tapa (227.8 g, 7.4 h), cuna impresa 2 veces (282.0 g, 10.0 h), 4 correas (20.1 g, 0.9 h). **Total 862.5 g, 31.1 h.** P14 y P15 ya no fallan (`"fijo": true`) |
| F Documento para el equipo | pendiente | |
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
