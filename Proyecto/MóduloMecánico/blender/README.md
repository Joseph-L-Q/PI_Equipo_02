# Animación del módulo (Blender)

| Archivo | Qué hace |
|---|---|
| `animacion.py` | v1: 12 s, giro 180° + despiece en bloque + bisagra. |
| `animacion_v2.py` | v2: 20 s, 1920x1080, 30 fps. Despiece pieza por pieza con etiquetas, título final. |
| `render_v2.sh` | Render en la Mac (tmux `pi-video`): secuencia PNG reanudable, vigilante de 2 min (máx. 3 reinicios), MP4 H.264 + GIF. |

Entrada: `../stl/ensamble_piezas/` (STL por instancia + `manifest.json`, generados por `cad/build.py`).
Salida: `Recursos/Imágenes/LG_mec_animacion_v2.mp4` y `.gif`.

```bash
# en la Mac, desde ~/PI_CAD/sin_push (blender/ y stl/ copiados ahí)
tmux new -d -s pi-video "bash ~/PI_CAD/sin_push/blender/render_v2.sh"
# revisar cuadros sueltos antes de renderizar todo:
Blender -b -P blender/animacion_v2.py -- --in stl/ensamble_piezas --png check --res 960x540 --samples 16 --only 1,300,600
```

## Guion v2

| Tiempo | Qué pasa |
|---|---|
| 0–4 s | El conjunto armado gira 120° (de −98° a 22°). |
| 4–10 s | Despiece en orden de montaje inverso: M2 sube, M6 y M7 salen por el eje óptico, M5 atrás y arriba (libra el brazo), M4 se separa, M3 se aleja de la caja. Cada pieza entra con su etiqueta 3D y su fila en la leyenda. |
| 10–13 s | Pausa explosionada con giro lento. |
| 13–18 s | Montaje en orden; las etiquetas salen cuando cada pieza vuelve. |
| 18–20 s | La cápsula derecha gira 0°→40° en su bisagra; título "LanternGuard · Módulo sumergido". |

## Decisiones (05/10/2026)

- **Rojo**: se usa el `COLOUR_RGB` del STEP (0.85, 0.20, 0.18 → `#D9332E`), como pide el guion, en vez del `#C0392B` aproximado. El `#C0392B` queda como color de acento del texto. Para cambiarlo: `MATS["red"]`.
- **Negro de los brazos y gris de las tapas**: del guion, no del STEP (el STEP trae gris oscuro 0.25 y casi blanco 0.95).
- **"Hacia adelante / atrás"** se interpreta en el marco de la cápsula: adelante = lado de la ventana (eje óptico hacia afuera). M5 sale hacia atrás y además hacia arriba, porque recto hacia atrás chocaría con el brazo. Offsets en `STEPS`.
- **Ángulo del despiece**: 22° y no de frente (0°): de frente las ventanas y biseles se ven de canto. El giro sigue siendo de 120°.
- **Etiquetas**: código corto 3D junto a cada pieza (solo en el lado derecho, para no amontonar) + leyenda 2D con el nombre completo a la izquierda.
- **Fondo**: ciclorama (piso curvo que sube a pared) gris claro con 4 luces de área (clave, relleno, contra, cenital): da el degradado y la sombra de contacto sin línea de horizonte. AO = "fast GI" de Eevee Next (Blender 5.2 ya no tiene el ajuste GTAO clásico).
- **GIF**: los 20 s completos a 2,5× = 8 s, 15 fps, 720 px de ancho.
