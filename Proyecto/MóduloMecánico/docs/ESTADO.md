# Estado de la sesión LanternGuard CAD (PC de casa, 30/10/2026)

Última actualización: **21:25** (handoff en `docs/HANDOFF_noche.md`). Terminados: 0, A, B, D. En curso: C segunda vuelta (boya con 4 botellas de 500 ml)
y E (falta la parte de la boya). Siguen F (documento para el equipo) y G (cierre).
Rama `cad/version-final`: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

| Bloque | Estado | Resultado |
|---|---|---|
| 0 Herramientas | listo | Orca nightly, CalculiX, Gmsh, rclone y claves de Onshape funcionan en esta PC |
| A Onshape | listo (falta LG_00_LEER_PRIMERO, va con F) | 8 documentos `LG_*` dentro de la carpeta LanternGuard, con descripción. Links en `docs/LINKS.md` |
| B Prototipos | listo | Tabla y recomendación en `docs/PROTOTIPOS.md`; fichas en `salida/prototipos/` |
| C Boya PET | 1.ª vuelta lista; 2.ª vuelta en curso | 2 × 1 L: 624 g, 20.9 h, pero GM 16 mm y vuelca si pierde una botella. Se prueba 4 × 500 ml en las esquinas |
| D Planos | listo | `planos/PLANOS_LanternGuard.pdf` (25 páginas: P2, P4 y boya 2 × 1 L; la boya se rehace con la 2.ª vuelta) |
| E Lista de impresión | nodo listo; boya pendiente de la 2.ª vuelta | 21 STL en `salida/imprimir_hoy/`, 16 placas (3MF en Drive), capturas en `salida/capturas_slicer/` |
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
