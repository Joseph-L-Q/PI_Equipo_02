# Retomar LanternGuard CAD en otra PC

## 1. Clonar
Hay dos remotos con el mismo historial:
- `origin`, el del equipo: https://github.com/Joseph-L-Q/PI_Equipo_02 (público).
- `personal`, un respaldo privado de Yoichi: https://github.com/IchiSieben/LanternGuard-CAD-backup. Tiene todas las ramas y tags.

```powershell
git clone https://github.com/Joseph-L-Q/PI_Equipo_02.git
cd PI_Equipo_02
git remote add personal https://github.com/IchiSieben/LanternGuard-CAD-backup.git   # opcional
git checkout cad/version-final
cd "Proyecto/MóduloMecánico"
```

## 2. Python y venv (Python 3.12)
```powershell
winget install -e --id Python.Python.3.12
powershell -ExecutionPolicy Bypass -File .\setup_laptop.ps1
```
El script hace tres cosas:
1. crea `.venv\`;
2. instala `requirements.txt` (CadQuery 2.8, Gmsh 4.13, trimesh, pyvista, etc.);
3. corre `python cad_final/build.py --rapido`.

En Mac se usa `setup_mac.sh`. Después se trabaja con `.venv\Scripts\python.exe cad_final/build.py ...`.

## 3. Herramientas externas

| Herramienta | Para qué | Dónde la busca el código | Variable para otra ruta |
|---|---|---|---|
| OrcaSlicer **nightly** portable | Laminar los 3MF: gramos y horas | `~/Downloads/OrcaSlicer_Windows_x64_nightly_portable/` | `ORCA_EXE` |
| CalculiX 2.22 (`ccx_static.exe`) | Análisis FEM del riel y del pie | `~/Downloads/calculix_2.22/calculix_2.22_4win/ccx_static.exe` | `CCX_EXE` |
| Gmsh | Mallado del FEM | Se instala con pip (`gmsh==4.13.1`) | (no tiene) |
| rclone | Subir a Drive | En el PATH | (no tiene) |
| Microsoft Edge | Pasar los MD a PDF (entrega, guías) | Ruta estándar de Windows | `EDGE_EXE` |

- Orca nightly: https://github.com/SoftFever/OrcaSlicer/releases (tag `nightly-builds`). Los perfiles P1P, PETG y 0.20 mm están en `cad_final/orca/`.
- CalculiX para Windows: https://www.calculix.de (o el paquete `calculix_2.22_4win`).
- rclone: `winget install Rclone.Rclone`.

## 4. Lo que se recrea a mano (no está en git ni en Drive)

**`cad_final/.env`** (lo ignora `.gitignore`). Lleva estas dos variables:
```
ONSHAPE_ACCESS_KEY=...
ONSHAPE_SECRET_KEY=...
```
- Se generan en Onshape: *My account → Developer → API keys*, con permisos de lectura y escritura.
- Las usan `onshape_sync.py`, `onshape_push.py` y `planos_onshape.py`.
- Guárdalo en UTF-8 sin BOM.

**Remoto de rclone `lgdrive:`.** Se crea con `rclone config`:
- `type = drive`;
- `scope = drive`;
- `root_folder_id = 1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO` (la carpeta LanternGuard_CAD);
- se autoriza con la cuenta de Google que tenga acceso a esa carpeta.

Conviene crear un `client_id` propio porque el compartido de rclone se retira en 2026: https://rclone.org/drive/#making-your-own-client-id

**SimScale.** No usa claves: los pasos son manuales (`SIMSCALE.md`). Los STEP están en Drive `06_SimScale`.

Ninguna clave va al repo, a Drive ni a un chat.

## 5. Dónde está cada cosa en Drive
Carpeta **LanternGuard_CAD** (id `1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO`): https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO

| Carpeta | Qué tiene |
|---|---|
| `01_Onshape_importar` | STEP de cada prototipo para importar en Onshape |
| `02_Imprimir_primero_probetas` | 3MF y STL listos para imprimir, por tanda (`imprimir_hoy_*`) |
| `03_Piezas_STL_preliminar_NO_IMPRIMIR` | STL viejos, solo de referencia |
| `04_Planos` | PDF de planos: `A4_formato_equipo/`, `pdf/`, `png/` y `STL_por_pieza/` |
| `05_Renders_y_capturas` | Renders (por ejemplo `skin/`) |
| `06_SimScale` | STEP simplificados y casos FEM |
| `07_Documentos` | `LANTERNGUARD_ENTREGA.pdf`, `ESTADO.md`, BITACORA.xlsx, BOM.md, `GUIA_PIEZAS_LanternGuard.pdf` |

**Reglas para Drive:**
- Solo se sube con `rclone copy`; nunca `sync` ni `delete`.
- Las versiones anteriores se renombran `zz_v2_...` y no se borran.

## 6. Comprobar que todo funciona
```powershell
.venv\Scripts\python.exe cad_final/build.py --rapido                 # CAD + checks (incluye cama 230 x 230)
.venv\Scripts\python.exe cad_final/build.py --prototipo P2_robusto   # prototipo completo
rclone lsd lgdrive:                                                  # deben salir las 7 carpetas
```

Para saber en qué se quedó el trabajo, lee en este orden:
1. `docs/ESTADO.md`;
2. `docs/HANDOFF_siguiente.md`;
3. `docs/DECISIONES.md`, en la raíz del repo.
