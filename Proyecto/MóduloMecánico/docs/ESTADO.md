# Estado de la sesión LanternGuard CAD (PC de casa, 30/10/2026)

Última actualización: **19:30**, bloque **0** terminado. Siguiente: bloque A (Onshape) y B (prototipos).
Rama `cad/version-final` en https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final

| Bloque | Estado | Resultado |
|---|---|---|
| 0 Herramientas | listo 19:30 | ver abajo |
| A Onshape | pendiente | |
| B Prototipos P0 a P4 | pendiente | |
| C Boya con botellas PET | pendiente | |
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
