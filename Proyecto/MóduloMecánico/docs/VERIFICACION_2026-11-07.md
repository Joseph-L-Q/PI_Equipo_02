# Verificación 07/11/2026: repo, documento de Onshape entregado y Drive

Paso 0 de `docs/ENCARGO_SIMSCALE_2026-11-07.md`, hecho antes de subir nada a SimScale.

**Resultado: no hay diferencias de geometría.** El repo y el documento de Onshape entregado coinciden pieza por pieza. En Drive había un solo archivo viejo: el STL de M3s, del 04/11, con el asiento anterior. Además faltaban LR2_aro, T1 y T2. Ya se subieron (detalle abajo). Se puede simular.

## 1. Repo

| Dato | Valor |
|---|---|
| Rama | `cad/version-final` |
| Commit local = `origin` | `7ef7793` (05/11 19:57). Es el documento limpio (`2519cfb`) más una nota del plano de M3s |
| `personal` | `a4ef4bc`, atrasado. Se empuja al cerrar |
| Cambios de código desde `2519cfb` | ninguno: `7ef7793` solo toca documentos |

Comprobado sobre los STEP del repo con `cad_final/verificar_entrega.py`:

| Hecho pedido | Resultado |
|---|---|
| M3s con asiento Ø17,1 | **sí**: el M3s tiene un cilindro de Ø17,1 |
| LR2_aro Ø16,5 con 13 perímetros | **sí**: `aro.seccion` = 16,5 y `aro.impreso.perimetros` = 13. El alto es 16,0 por la base aplanada de 0,5 |
| Riel cerrado | **sí**: 2 mitades M3s (der e izq) en el ensamble del nodo |
| B1, B2 y B5 en mitades | **sí**: B1 ×2, B2 lisa + mástil, B5 ×4 (base y cuello, D e I) |
| M1s y M2 con chaflán de 6 mm | **sí**: 4 caras a 45° de cateto 6 en cada una (`caja.chaflan_esquina` = 6) |
| Cubiertas B2 con barras de 26 × 20 | **sí**: `boya_pet.barra_cruz` = (26, 20, 113) |
| T1 y T2 de tierra | **sí** |

## 2. Documento entregado en Onshape

[LanternGuard - PIEZAS PARA IMPRIMIR](https://cad.onshape.com/documents/76e36e0130a8d259842ecee7/w/fdd58e8bdf77f39a1781a12d), de Melissa. Se abrió sin iniciar sesión con Playwright: el documento ya es público (`ANONYMOUS_ACCESS`). Las pestañas se leyeron con la sesión anónima de la página, sin la API de la cuenta personal.

| Dato | Valor |
|---|---|
| Pestañas | **70**: 24 Part Studios, 21 planos, 24 `.step` y `00_LEEME.pdf`. Igual a las 70 que se registraron al crearlo (`salida/limpio/estado.json`) |
| Ensambles | `00_ENSAMBLE_nodo`, `00_ENSAMBLE_boya` y `00_ENSAMBLE_tierra`, con sus `.step` |
| Última modificación del workspace | 05/11 19:59 (−05:00), 2 minutos después del commit `7ef7793`. Es el fin de aquella sesión. **Nadie lo modificó después** |
| Blobs de los ensambles y del M3s | mismos ids que los registrados: nodo `4d0227bc…`, boya `0f8e8745…`, tierra `378bad62…`, M3s `708f241f…` |

Las propiedades de masa no se pueden leer sin iniciar sesión (401). Por eso la geometría se comparó por los blobs: siguen siendo exactamente los STEP que se subieron, y esos STEP están en el repo (`salida/limpio/step/`).

## 3. Pieza por pieza

Volumen de cada sólido del STEP de ensamble subido a Onshape, comparado con el STEP por pieza del repo (tolerancia 0,1 %).

| Pieza | Ensamble | Repo: volumen (mm³) | Onshape: blob del ensamble | Drive: STL en `04_Planos/STL_por_pieza` | Diferencia |
|---|---|---|---|---|---|
| M1s_caja_cuerpo | nodo | 367 482 | igual | 05/11 (orientado) | ninguna |
| M2_caja_tapa | nodo | 160 231 | igual | 05/11 (orientado) | ninguna |
| M11_bandeja | nodo | 43 659 | igual | 05/11 | ninguna |
| M11_bandeja_sup | nodo | 39 211 | igual | 05/11 | ninguna |
| M3t_tapa_bolsillo ×2 | nodo | 35 555 | igual | 05/11 | ninguna |
| M3f_marco_bolsillo ×2 | nodo | 62 499 | igual | 05/11 | ninguna |
| **M3s_riel_gancho ×2** | nodo | **168 136** | igual | **era del 04/11 (170 829 mm³, asiento viejo)** | **solo Drive: reemplazado hoy** |
| M4_capsula_cuerpo ×2 | nodo | 64 566 | igual | 05/11 | ninguna |
| M5s_capsula_tapa_pie ×2 | nodo | 80 070 | igual | 05/11 | ninguna |
| M6_capsula_bisel ×2 | nodo | 1 890 | igual | 05/11 | ninguna |
| **LR2_aro ×4** | nodo | 133 158 | igual | **faltaba** | **solo Drive: subido hoy** |
| B1_casco (2 mitades) | boya | 201 997 c/u | igual | 05/11 | ninguna |
| B2_cubierta_lisa | boya | 326 592 | igual | 05/11 | ninguna |
| B2_cubierta_mastil | boya | 351 615 | igual | 05/11 | ninguna |
| B3_caja | boya | 187 723 | igual | 05/11 | ninguna |
| B4_tapa | boya | 114 896 | igual | 05/11 | ninguna |
| B5_cuna_base ×2 | boya | 81 751 | igual | 05/11 | ninguna |
| B5_cuna_cuello ×2 | boya | 85 628 | igual | 05/11 | ninguna |
| B6_correa ×4 | boya | 7 315 | igual | 05/11 | ninguna |
| **T1_caja** | tierra | 58 181 | igual | **faltaba** | **solo Drive: subido hoy** |
| **T2_tapa** | tierra | 39 471 | igual | **faltaba** | **solo Drive: subido hoy** |

Los ensambles traen además cuerpos de referencia, que no se imprimen: la linterna (malla y 3 pisos) en el nodo y las 4 botellas en la boya. La ventana de acrílico M7 no está en el ensamble del nodo. Detalle en `salida/verificacion/verificacion_0711.json`.

## 4. Drive (`lgdrive:`)

| Carpeta | Estado |
|---|---|
| `04_Planos/PLANOS_A4_LanternGuard_v6.pdf` | es el último. **No incluye** el M3s de Ø17,1 ni LR2_aro, T1 y T2. Esos van en PDF sueltos (abajo) |
| `04_Planos/STL_por_pieza` + `LEEME.txt` | 18 STL vigentes. Son los mismos archivos que `salida/imprimir_hoy/`, salvo M3s, que estaba viejo |
| `02_Imprimir_primero_probetas/imprimir_hoy_2026-11-05/` | existe. En el encargo figura como `02_Imprimir`. La placa de M3s que trae es del asiento viejo: no imprimirla (ya figuraba en el HANDOFF) |
| `08_PARA_IMPRIMIR` | **no existe**. Sigue pendiente (punto 2 del HANDOFF): hay que exportar los PDF desde Onshape |

**Subido hoy, solo con `rclone copy`.** Antes de reemplazar M3s, lo viejo se copió a `OLD/2026-11-07/`.
- `04_Planos/STL_por_pieza/`: `M3s_riel_gancho.stl` (Ø17,1), `LR2_aro.stl`, `T1_caja.stl` y `T2_tapa.stl`. Están en la orientación del CAD, no en la de impresión: girarlos en el slicer.
- `04_Planos/A4_formato_equipo/`: `PLANO_A4_M3s_riel_gancho.pdf` (el del documento limpio, Ø17,1) y `PLANO_A4_LR2_aro`, `PLANO_A4_T1_caja` y `PLANO_A4_T2_tapa`, cada uno en versión Onshape y `_local`.
- **Aviso:** los PDF de LR2_aro, T1 y T2 son del 05/11 18:53, de antes de las notas que se agregaron en Onshape: el plano de LR2 cita ahora el asiento Ø17,1 y T1 y T2 dicen PLA. La geometría es la misma. La versión final de esas notas está en el documento de Onshape.
