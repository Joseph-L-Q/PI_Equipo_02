# Llevar el CAD a Onshape

El modelo de verdad está en `cad_final/params.py` y los scripts de `cad_final/`. Onshape recibe **copias** en STEP: lo
que se cambie a mano en Onshape no vuelve a `params.py`. Si una medida cambia, se cambia en `params.py`, se regenera y
se actualiza Onshape con el STEP nuevo.

> No se pudo probar desde aquí (el documento compartido es de solo lectura). Los nombres de menú son los de la
> interfaz en inglés de Onshape; si no coinciden, busca la opción equivalente.

## Qué archivos subir

| Qué | Dónde está | Nota |
|---|---|---|
| Piezas del nodo | `salida/preliminar/step/` | M1 a M14, una pieza por archivo. M3 son cuatro: `M3_riel_central`, `M3_riel_ext`, `M3_riel_punta`, `M3_tapa_bolsillo` |
| Piezas de la boya | `salida/boya/step/` | B1 a B6 |
| Ensamble completo por aro | `salida/ensambles/ensamble_D100.step` (y D200, D300, D500) | **No están en el repo** (pesan 42 MB). Se generan con `python cad_final/build.py --todo` |

## Por la API (sin navegador): `cad_final/onshape_sync.py`

Documento actual: **LanternGuard CAD final**, su link está en `cad_final/onshape_config.json`. El mapa
pieza → pestaña de Onshape está en `cad_final/onshape_map.json`. Los dos van al repo.

### Claves (una vez por computador)

1. En Onshape: avatar arriba a la derecha → **My account → Developer → API keys → Create new API key**. Las cuentas
   individuales tienen como máximo 2 claves activas.
2. Marca los permisos **Read** y **Write**. Marca también **Delete** si quieres que el script pueda borrar pestañas; la
   clave del 29/10 no lo tiene y el borrado da 403.
3. Copia las dos claves en `Proyecto/MóduloMecánico/.env` (está en `.gitignore`, nunca se sube):

   ```
   ONSHAPE_ACCESS_KEY=...
   ONSHAPE_SECRET_KEY=...
   ```

   La secreta se ve una sola vez. Si se pierde, borra la clave y crea otra.

### Límite de llamadas

El plan Student tiene **2 500 llamadas por año**. Solo cuentan las respuestas buenas (2xx y 3xx), y al llegar al
límite Onshape responde 402. El script anota cada llamada en `cad_final/onshape_calls.log` (local, fuera del repo; cada
computador lleva su cuenta) y no sube nada si el cálculo pasa el límite. `--cuenta` muestra lo gastado.

| Qué | Llamadas |
|---|---|
| `--init` (documento nuevo) | 1 |
| Pieza nueva (subir + traducir; consulta el estado cada 5 s) | 2 a 3 |
| `--actualizar` una pieza que cambió | 1 |
| Pieza que no cambió | 0 (se salta; `--forzar` la sube igual) |
| Primera carga de las 27 piezas (29/10) | 55, con las pruebas: 61 en total |

### Comandos (desde `Proyecto/MóduloMecánico`, con el `.venv`)

```
python cad_final/onshape_sync.py --init "LanternGuard CAD final"     # solo si no hay onshape_config.json
python cad_final/onshape_sync.py --subir salida/preliminar/step salida/boya/step
python cad_final/onshape_sync.py --actualizar M9                     # M3 = las cuatro del riel
python cad_final/onshape_sync.py --ensamble 200                      # salida/ensambles/ensamble_D200.step, aplanado
python cad_final/onshape_sync.py --cuenta
```

Cualquiera de esos comandos acepta `--dry-run`, que dice qué haría y cuántas llamadas gastaría, sin llamar.

### Subir una versión nueva sin tocar las anteriores: `onshape_push.py` (versión simple)

```
python cad_final/onshape_push.py salida/simple/ensamble_simple_D200.step --nombre simple_D200_V1
python cad_final/build.py --rapido --onshape        # regenera y sube el ensamble simple como simple_D200_vN
```

- Siempre crea pestañas **nuevas**: si ya hay una con ese nombre usa `_v2`, `_v3`... Nunca borra ni reemplaza.
- Sube el STEP con traducción, espera a que termine (consulta cada 5 s) e imprime el link de cada pestaña nueva. Gasta
  4 llamadas por archivo. `--plano` aplana el ensamble.
- Claves en `cad_final/.env` (o `Proyecto/MóduloMecánico/.env`), nunca en el repo.
- Hoy los ensambles se exportan como un compuesto de sólidos: Onshape los convierte en **un Part Studio con todas las
  piezas**, sin pestaña de Assembly. Para tener un Assembly con mates hay que exportar el STEP con árbol de ensamble
  (pendiente).

Subidos el 29/10: `LR1_separador`, `simple_D200_V1` (cápsula a 30°), `simple_D200_V2_45grados` y
`simple_D200_V3_sin_correa` (los STEP de V2 y V3 salen de `cad_final/variantes.py`, en `salida/variantes/`).
Después: `nodo_simple_V2` (caja baja, KIT A, cámaras hacia la malla), `boya_simple_V1`, `boya_referencia_V1` (maqueta
del ejemplo del equipo) y `sistema_simple_V1` (nodo + boya + U1 + C1). Los STEP de estos ya llevan las piezas con nombre
(M*, B*, LR*, U1, C1); Onshape igual crea un solo Part Studio. El Part Studio huérfano de M7 sigue ahí: la clave no tiene
permiso de borrar (403), se borra a mano.

### Lo que la API no hace: el "Update..."

Probado el 29/10 con M7:

- Volver a subir el STEP **con** traducción crea un **segundo** Part Studio. El primero queda igual y los ensambles
  siguen apuntando a él.
- Subirlo **sin** traducción reemplaza el archivo, pero el Part Studio tampoco se actualiza solo.
- La API (especificación OpenAPI v17) no tiene un endpoint equivalente al menú **Update...**.

Por eso `--actualizar` solo reemplaza el STEP dentro del documento (1 llamada, sin Part Studio duplicado). Después hay
que hacer esto a mano en Onshape:

1. Clic derecho en la pestaña del **Part Studio** de la pieza (mismo nombre que el STEP) → **Update...**.
2. Elige el STEP nuevo: `salida/preliminar/step/<pieza>.step` o `salida/boya/step/<pieza>.step`.
3. Si una unión de un ensamble queda en rojo, vuelve a crearla (ver abajo).

La pieza nueva (`crear`) sí queda lista sola: STEP y Part Studio traducido, en milímetros, con Z hacia arriba
(`yAxisIsUp=false`).

## La primera vez (documento nuevo, a mano)

1. **Create → Document**, nombre *LanternGuard nodo (cad_final)*.
2. Pestaña inferior **+ → Import**, elige los STEP de `salida/preliminar/step/`. Unidades: **milímetros**.
3. Crea un **Assembly** e **Insert** cada pieza. Cantidades por aro: tabla del §2 de `MEDIDAS.md`.
4. Uniones (*mates*), solo las que hacen falta para mirar el conjunto:
   - **Fastened**: caja M1 con tapa M2; caja con el tramo central del riel; tramos del riel entre sí.
   - **Slider**: carro M10 sobre el riel (recorrido en `carro.recorrido` de `params.py`). Ojo: en Ø100, Ø300 y Ø500
     el carro solo puede ir a ras de la punta (conflicto C20 en `REPORTE_CAD.md`); el recorrido de ±50 solo existe en Ø200.
   - **Revolute**: cápsula M4 + M5 en el carro, eje de la bisagra, de 0 a 90 grados.
5. Para comparar, importa también `ensamble_D200.step`: es la posición de referencia (carro a ras de la punta, cápsula
   a 40 grados).

## Cuando cambia una medida (documento que ya existe)

1. Cambia el valor en `cad_final/params.py` y regenera (`CAMBIOS_RAPIDOS.md` dice qué comando).
2. En Onshape, clic derecho sobre la pestaña del STEP importado → **Update...** y elige el archivo nuevo con el mismo
   nombre. Onshape reemplaza la geometría y trata de mantener las uniones.
3. Si una unión queda en rojo, la cara que usaba cambió de forma: borra esa unión y vuelve a crearla. Es normal cuando
   cambia la cantidad de caras (por ejemplo, al agregar la varilla M8 o el tabique del riel).
4. Si cambia el riel (largo, puntas, extensiones), conviene **volver a importar** el ensamble del aro en lugar de
   actualizar pieza por pieza.

## Ojo

- El documento viejo de Onshape tiene el brazo `M3_brazo` (en rojo, C11). Ese brazo ya no existe: el riel nuevo son
  cuatro piezas. Hay que importar de nuevo, no actualizar.
- Los planos que se usan para imprimir y medir salen del modelo, en `planos/cad_final/` (uno por pieza, PNG y PDF). El
  editor de planos de Onshape sirve para la presentación, pero sus cotas no se comprobaron contra `params.py`.
