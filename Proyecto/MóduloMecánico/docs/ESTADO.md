# Estado de la sesión LanternGuard CAD (PC de casa, 30/10/2026)

Última actualización: **20:25**. Terminados: bloque 0, bloque A (primera pasada) y P0 del bloque B. En curso: P1 a P4 (bloque B) y la boya PET (bloque C), en paralelo.
Rama `cad/version-final` en https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

| Bloque | Estado | Resultado |
|---|---|---|
| 0 Herramientas | listo 19:30 | ver abajo |
| A Onshape | primera pasada lista 20:20 | Claves escriben. Documentos `LG_probetas` y `LG_P0_original` creados; los de P1 a P4, boya y sistema se suben cuando estén. Links en `docs/LINKS.md` |
| B Prototipos P0 a P4 | P0 listo; P1 a P4 en curso | P0 simple V1: 1248 g, 45.1 h, 112 soles; P0 modular: 1285 g, 55.1 h, 116 soles (estimado). Fichas en `salida/prototipos/P0_original/` |
| C Boya con botellas PET | en curso (rama `cad/boya-pet`) | |
| D Planos 2D | pendiente | |
| E Lista de impresión y capturas | pendiente | |
| F Documento para el equipo | pendiente | |
| G Cierre | pendiente | |

## Bloque 0: qué hay en esta PC

| Herramienta | Estado | Prueba |
|---|---|---|
| OrcaSlicer nightly 2.5.0-dev portable | sí, `Downloads/OrcaSlicer_Windows_x64_nightly_portable/` (la ruta que ya usa `slicer.py`; no se movió a `OrcaSlicer_nightly/`) | `--slicer` cortó las 10 piezas del nodo hoy (1358 g, 47.0 h); `--export-3mf` probado en M6: el 3MF trae `Metadata/plate_1.png` y `top_1.png` |
| Perfiles Orca | sí, `cad_final/orca/` (3 JSON planos, commit 20ea93d) | |
| CalculiX 2.22 + Gmsh 4.13.1 | sí (`Downloads/calculix_2.22/`, Gmsh en el venv) | `--fem` TODO BIEN hoy: riel 8.39 MPa FS 5.36/2.62, pie 8.92 MPa FS 5.04/2.47 |
| Onshape (`cad_final/.env`) | sí, claves cargadas a las 19:20 | `GET /users/sessioninfo` responde 200. La escritura se prueba en el bloque A |
| rclone `lgdrive:` | sí, apunta a LanternGuard_CAD | lista las 7 carpetas |
| Python `.venv` 3.12.10 | sí | `--rapido` TODO BIEN en 70 s |

## Dónde está cada cosa
- Este archivo y los nuevos (`PENDIENTES.md`, `LINKS.md`, `PROTOTIPOS.md`, `BOYA.md`...): `Proyecto/MóduloMecánico/docs/`.
- Decisiones tomadas sin Yoichi: `docs/DECISIONES.md` en la **raíz del repo** (ya existía).
- Drive: carpeta LanternGuard_CAD, este archivo en `07_Documentos/ESTADO.md`.

## Links
- Onshape LG_probetas: https://cad.onshape.com/documents/dfcea0e1fd7d960062f6631e/w/7030967448e32d98d4462131
- Onshape LG_P0_original: https://cad.onshape.com/documents/95702b685c4703a1812f1cd5/w/22e05e9a953df1fd6ec5ee2a
- Todos: `docs/LINKS.md`
