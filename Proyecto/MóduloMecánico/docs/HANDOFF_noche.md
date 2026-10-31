# HANDOFF noche 30/10/2026 (~21:25) | LanternGuard CAD, PC de casa

Rama `cad/version-final`, todo empujado salvo lo que se indica. Plan base: HANDOFF_2026-10-30_v2.md §4. Decisiones:
`docs/DECISIONES.md` (raíz del repo). Links: `docs/LINKS.md`. Estado: `docs/ESTADO.md` (también en Drive 07_Documentos).

## Estado por bloque
| Bloque | Estado | Commits |
|---|---|---|
| 0 Herramientas | listo (Orca nightly, CalculiX, Gmsh, rclone `lgdrive:`, claves Onshape que escriben) | 57584be |
| A Onshape | listo: 8 docs `LG_*` en la carpeta LanternGuard (bf32e5647856cd2677198b89) con descripción (`onshape_push.py`: `--carpeta`, `organize()`). Faltan: LG_00_LEER_PRIMERO, ENSAMBLE_v2 y nombres REF_ (corrección 3 y 4) | e553f57, b6e44d5 |
| B Prototipos | listo: P0 (V1 y modular), P1..P4, `docs/PROTOTIPOS.md`; recomendación P2 robusto (piscina) y P4 estético (presentar) | e553f57, 1463c4c |
| C Boya PET | 1.ª vuelta (2 × 1 L) unida (778c790), descartada por Yoichi. 2.ª vuelta (4 × 500 ml) **en curso** | 2bc5de6, 778c790 |
| D Planos | listo para P2, P4 y boya 2 × 1 L: `planos/PLANOS_LanternGuard.pdf` (25 págs.) | c2b27d8 |
| E Impresión | nodo P2 listo: `salida/imprimir_hoy/` (21 STL, `plan_placas.json`), 14 placas cortadas, 3MF en Drive `02_Imprimir_primero_probetas/imprimir_hoy_30oct_noche/`, capturas en `salida/capturas_slicer/`. Placas de la boya: falta (P14/P15 fallaron por la zona excluida; usar `"fijo": true`) | b6e44d5 |
| F Entrega | pendiente. Listo el conversor `cad_final/entrega_pdf.py` (md → PDF con Edge headless) | |
| G Cierre | pendiente | |

## Quedó a medias (subagentes lanzados)
- **Boya, 2.ª vuelta:** subagente en el árbol principal; toca solo `boya_pet.py`, el bloque `flotacion.*`/`boya_pet.*`
  de `params.py`, `salida/boya_pet/`, `docs/BOYA.md`; commitea sin push. **Cómo retomarla si no terminó:** mirar
  `git log` y `git status` de esos archivos; si no hay commit `cad(bloqueC): segunda vuelta...`, relanzar con el pedido
  de Yoichi: 4 botellas de 500 ml en las esquinas del casco (254 × 226), francobordo, GM en los dos ejes ≥ 40 mm, caso
  con 3 botellas flotando derecha, comparar con 2 × 1 L en `docs/BOYA.md` y recomendar una.
- **Correcciones (abajo), ya lanzadas:** subagente en un worktree (`.claude/worktrees/...`), rama `cad/tanda3`, que
  hace push de esa rama y no la une. Al terminar: `git merge origin/cad/tanda3` en `cad/version-final` (el conflicto
  esperable es `params.py`: conservar los dos bloques).

## Correcciones de Yoichi (copiadas textual)
1. Quita el separador LR1 y el ápice de todos los prototipos y del sistema (parámetro separador.usar = False, sin borrar el código). La linterna de prueba se modela simple: aro superior Ø200 + 4 cuerdas que suben rectas desde el aro hasta un punto de amarre, + cabo al long line. El nodo se engancha al aro superior y queda girado para que los brazos salgan a 45° entre cuerdas; verifica holgura cuerda-brazo ≥ 10 mm. Sin aro guía.

2. Lastre: reemplaza las pilas de pletinas por UN bolsillo por lado para tuercas/arandelas M8 inox a granel (o bolsas de perdigones), con tapa atornillada. Calcula cuántos gramos hacen falta por prototipo para quedar entre 0.2 y 0.5 kgf aparente hacia abajo y ponlo en la FICHA. Antes de agregar lastre, intenta bajar el aire encerrado achicando la caja (P1 y P3). En el ensamble el lastre va como un solo cuerpo por bolsillo llamado "lastre_izq"/"lastre_der", no 10 pletinas.

3. Onshape: el STEP de ENSAMBLE de LG_P3_monocasco se importó con errores y faltan piezas del brazo. Revisa todos los ENSAMBLE subidos: compara el número de sólidos del STEP local con las partes que reporta Onshape (GET partstudios/.../parts). Si no coinciden, repara (ShapeFix / unir caras) o sube el ensamble como un STEP por pieza ya posicionado en la misma pestaña. Usa una pestaña nueva ENSAMBLE_v2, no borres la anterior.

4. Renombra en Onshape los cuerpos de referencia para que se entiendan: "REF_linterna_malla", "REF_aro_superior", "REF_cuerda_1..4", "REF_cabo", "REF_umbilical". Todo lo que se imprime con su código (M1_caja...). Lo que no se imprime lleva el prefijo REF_.

Anota cada cambio en docs/ESTADO.md y en la FICHA de cada prototipo.

## Orden de trabajo
(a) Cerrar la boya 4 × 500 ml (esperar o retomar el subagente; push; `LG_boya_PET_v2` en Onshape).
(b) Aplicar las 4 correcciones a P0..P4 y al sistema (unir `cad/tanda3`; luego Onshape: ENSAMBLE_v2 por documento,
    comparar sólidos de `ensamble_solidos.json` con `GET /parts/d/{did}/w/{wid}`, nombres REF_). P0 es referencia sin
    tocar la geometría: solo su ensamble en Onshape (ENSAMBLE_v2 con nombres) si hace falta.
(c) Rehacer D y E solo para lo que cambió: `planos_piezas.py --carpeta ... --prefijo P2|P4|BP` (borrar la carpeta del
    prefijo antes), `portada_planos.py` + `--unir --portada ../planos/cad_final/_portada.pdf P2 P4 BP`;
    `imprimir_hoy.py` (actualizar BUOY/PLATES si cambian piezas; LR1 sale de la lista) + `placas.py plan_placas.json`.
(d) F: `docs/LANTERNGUARD_ENTREGA.md` + `entrega_pdf.py`, LG_00_LEER_PRIMERO, subir a Drive 07_Documentos (PDF,
    PLANOS, BITACORA, BOM, renders, capturas). G: REPORTE_CAD §11, `docs/HANDOFF_siguiente.md`, ESTADO "TERMINADO",
    resumen de 15 líneas con links.

## Reglas que siguen vigentes
Claves en `cad_final/.env` (gitignored), nunca impresas. Drive solo con `rclone copy`. Commits con explicit paths y
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. No borrar en Onshape ni en Drive; pestañas y documentos
nuevos con sufijo de versión. Orca: rutas Windows desde Python; Orca deja `00000.log` en el cwd.
