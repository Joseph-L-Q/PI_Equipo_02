# Importar a Onshape a mano (2026-11-05)

La cuota de la API de Onshape se agotó, así que estas piezas no se subieron solas. Hay que importarlas a mano en el
documento **LG_IMPRIMIR_P2**: https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff

Las piezas que no están en esta lista no cambiaron y no se tocan.

## Orden

1. Abrir el documento LG_IMPRIMIR_P2.
2. Para cada fila de la tabla, en orden:
   1. Clic derecho en la pestaña `<pieza>` → **Rename** → `OLD 2026-11-05 <pieza> (<motivo corto>)`. No se borra.
   2. Botón **+** (abajo a la izquierda) → **Import…** → elegir el archivo `.step` de esta carpeta.
   3. Cuando termine de traducir, renombrar la pestaña nueva a `<pieza>`, sin sufijo.
   4. Si la pieza tiene plano `PLANO_A4_<pieza>`, abrirlo y apuntar la vista a la pestaña nueva (o hacer un plano nuevo con el
      formato del equipo). Los planos de Melissa ("Drawing …") no se tocan.
3. Al final, el ensamble: renombrar `00_ENSAMBLE` a `OLD 2026-11-05 00_ENSAMBLE`, importar `00_ENSAMBLE.step` y renombrar la
   pestaña nueva a `00_ENSAMBLE`. Debe tener **32 sólidos** (sin cuerpos REF_).
4. Mover las pestañas `OLD …` a LG_HISTORICO si se quiere limpiar (o borrarlas a mano).

## Piezas

| Orden | Archivo | Reemplaza a | Qué cambió | Volumen |
|---|---|---|---|---|
| 1 | `M1s_caja_cuerpo.step` | Part Studio `M1s_caja_cuerpo` | chaflán de 6 mm en las 4 esquinas de la brida (holgura de la cuerda); tornillos de esquina corridos 5,9 mm | 367.5 cm³ (antes 368.0) |
| 2 | `M2_caja_tapa.step` | Part Studio `M2_caja_tapa` | chaflán de 6 mm en las 4 esquinas en planta (holgura de la cuerda); tornillos de esquina corridos 5,9 mm | 160.2 cm³ (antes 160.4) |
| 3 | `B1_casco.step` | Part Studio `B1_casco` | postes de la cubierta Ø16 y parches de amarre de 34 x 14 para la pata de gallo (cabo de 300 N) | 202.0 cm³ (antes 157.4) |
| 4 | `B2_cubierta_lisa.step` | Part Studio `B2_cubierta_lisa` | panel a 15 mm, columnas Ø14, 4 tirantes, marco bajo el panel y barras de 20 x 20 (golpe lateral de 200 N) | 326.6 cm³ (antes 121.8) |
| 5 | `B2_cubierta_mastil.step` | Part Studio `B2_cubierta_mastil` | igual que B2 lisa, más el mástil de la antena | 351.6 cm³ (antes 150.4) |
| 6 | `00_ENSAMBLE.step` | Assembly / Part Studio `00_ENSAMBLE` | conjunto con las piezas de arriba | 32 sólidos |

Los planos A4 de estas piezas ya están hechos en local con el formato del equipo, en
`04_Planos/PLANOS_A4_LanternGuard_v6.pdf` (Drive).
