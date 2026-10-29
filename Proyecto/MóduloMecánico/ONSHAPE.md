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

## La primera vez (documento nuevo)

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
