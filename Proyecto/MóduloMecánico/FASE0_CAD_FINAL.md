# Fase 0 | CAD final LanternGuard | inventario y diagnóstico (28/10/2026)

Sin cambios de geometría. Fuente: `Proyecto/MóduloMecánico/cad/` en `Documents\Portfolio\laptop\PI_Equipo_02` (rama local `yoichi/diseno-mecanico`).

## 1. Qué hay realmente

| Qué | Estado |
|---|---|
| Herramienta | **CadQuery** (no build123d, como dice el handoff). `params.py` (medidas), `parts.py` (piezas), `build.py` (export + chequeos + reporte), `planos.py`, `vistas.py` |
| Salidas | `step/` (M1…M8 + `ENSAMBLE_modulo.step` + banco de prueba), `stl/` y `stl/ensamble_piezas/` (der/izq + `manifest.json`), `planos/` (LG-ENS-01, LG-M4-01) |
| Chequeos ya automatizados | sólido válido (BRepCheck + BOPAlgo), STL cerrado, cama, voladizos, espesores bajo cortes, interferencias, barrido de la bisagra 0–90°, flotabilidad, Roark a 0.15 MPa |
| Git | Repo con rama local. Desde aquí no tengo terminal en tu PC: no puedo crear la rama `cad/version-final`. Propuesta: trabajo en `cad_final/` al lado de `cad/` (el original no se toca) y tú haces el commit, o me das los comandos para pegar |
| Onshape | `M1_caja_cuerpo`…`M7_ventana_der`. El brazo izquierdo es la misma forma que el derecho girada 180° (instancia compartida) |

## 2. Medidas actuales (las del script, no las del handoff)

| Parámetro | Valor en el script | Handoff dice | Origen / estado |
|---|---:|---:|---|
| Caja central exterior | 142 × 76 × 60 (+ pestaña 9) | 180 × 130 × 80 | script; cavidad 132 × 66 × 54 pensada para ESP32-WROOM + MAX485 + JSN-SR04T |
| Pared caja / tapa / fondo | 5 / 6 / 6 | 4 | script (Roark a 15 m) |
| Cápsula exterior | 46 × 46 × 61 (+ pestaña, 64 × 64) | 70 × 70 × 55 | script; cavidad 38 × 38 × 50 |
| Ventana | acrílico Ø30 × 3 | — | supuesto |
| Brazo | 30 × 25, pared 3, **190 mm** + horquilla 52 | 100 por lado | script; impreso **de pie** (242 de alto) |
| Pivote de la bisagra | x = ±310.5 desde el centro | — | calculado |
| Apoyo sobre el aro | x = ±250 (aro Ø500), varilla Ø12 | sección 8 | ambos **estimados** |
| Bisagra | 36 dientes (10°), M4, tilt 40° | — | script |
| Junta | cordón Ø2, ranura 2.6 × 1.5 (25 %) | — | calculado, no probado |
| Prensaestopas | PG7 brazos/cápsulas, PG9 umbilical en la tapa | — | script |
| Masa en aire | 1022 g | ≤ 3 kg | cumple |
| Peso aparente | **−310 g (flota)** | +0.2 a +0.5 kgf | falta lastre 0.6–0.9 kg |
| Profundidad de diseño | 15 m (0.15 MPa) | 1 m | cambiar a 1 m (C2) |

## 3. Conflictos

| # | Estado real |
|---|---|
| C1 | Conjunto mide **770 mm** de largo frente a 220 de la Lista. Es inevitable si se apoya en un aro de Ø500: hay que reescribir la fila Geometría |
| C2 | Script diseñado a 15 m. A 1 m la presión es **0.010 MPa (15 veces menos)**: la tapa de la caja trabaja a 0.74 MPa. A 1 m la presión deja de mandar; manda la manipulación (150 N) |
| C3 | Sin cambio: Waveshare hace la carga, sin esquema de la placa fabricada |
| C4 | **El script todavía tiene la electrónica vieja** (ESP32-WROOM, MAX485, JSN-SR04T con agujero en el fondo). Con KIT A (80 × 70 estimado) **no entra**: la cavidad mide 66 de ancho. La caja tiene que crecer |
| C5 | El agujero del JSN-SR04T en el fondo se elimina (ultrasónico descartado). ToF no se modela |
| **C6** | **No está "al límite": está bloqueado.** Con brazos de 190 el recorrido a la cámara más lejana sale **≈ 410–450 mm** (ESP32 al centro o a un extremo) frente a 300 incluidos. El estimado de 290 del handoff era con brazos de 100 |
| C7 | DS3231: reservar 40 × 25 × 15 en la boya |
| C8 | Sin cambio: estanqueidad solo por prueba 24 h / 72 h / 7 días |
| C9 | Usar solo la placa 70 × 73.5 |
| **C10 (nuevo)** | **El brazo se imprime de pie**, así que al flexionar trabaja **entre capas**. Con 150 N en la cápsula: σ = 18.5 MPa en la raíz; con la mitad de resistencia entre capas, **FS ≈ 1.2**. Hay que imprimirlo acostado (en diagonal cabe: 242 < 311) o reforzarlo |
| C11 (nuevo) | Rojo de M3 en Onshape: hipótesis, Parasolid marca falla en la unión dientes/oreja (arista mínima 0.39 mm, cara 0.73 mm²) o por la instancia compartida der/izq. Se puede probar exportando M3_der y M3_izq como sólidos separados y quitando astillas |

## 4. Cálculo a mano (primera pasada)

| Caso | Valor | Comentario |
|---|---|---|
| Brazo 30 × 25 × 3: I = 25 344 mm⁴, W = 2 028 mm³ | | |
| 150 N en la cápsula, momento en la raíz (brazo en voladizo de 250 mm) | 37 N·m → 18.5 MPa | FS 2.4 macizo, **1.2 entre capas** → caso que gobierna |
| 150 N en la cápsula, apoyado en el aro | 12 N·m → 6.0 MPa | FS 3.8 entre capas |
| Izado por el asa (2 patas 12 × 12) | 0.5 MPa | sobrado |
| Aplastamiento del M4 en las orejas | 3.75 MPa | sobrado |
| Corriente 0.5 m/s sobre una cápsula | 0.46 N | despreciable |
| Presión a 1 m sobre la tapa | 0.74 MPa | despreciable |

Conclusión: a 1 m lo crítico no es el agua sino **la raíz del brazo, la unión brazo-caja (4 insertos M3) y la orientación de impresión**. Eso es lo que hay que reforzar y luego verificar en SimScale.

## 5. Archivos y parámetros que tocaría (Fases 1–6)

- `params.py`: `DESIGN_DEPTH_M = 1`, presión 0.0101; `COMPONENTS` nuevo (KIT A, 2 HW-517, XY-017, microSD, MPU-6050) con origen/estado; `LANTERN_RING_D` y `RING_ROD_D` a lo medido; `BOX_CAV_*` desde el layout; `PRINT_BED` a la impresora real; brazo con raíz reforzada (cartelas, pared 4) y orientación acostada.
- `parts.py`: `box_body` sin agujero JSN, con standoffs para KIT A y MPU-6050 rígido; asiento del aro curvo (radio R) + snap en C + ranura de correa 25 mm; `ring_pos` con `x = √(R² − e²)`; probetas nuevas (gancho y junta).
- `build.py`: chequeo de recorrido de cable, caso de 150 N, export separado der/izq de M3.
- `boya.py` (nuevo, B1…Bn) y `REPORTE_CAD.md`.

## 6. Plan de SimScale (después del cálculo a mano, para no gastar cuota)

1. M3 brazo: fijo en la brida de la raíz, 150 N vertical en el agujero del pivote. Comparar con 18.5 MPa a mano.
2. Unión brazo-caja: M1 fijo en la tapa/pestaña, 37 N·m en la almohadilla (o el brazo completo con contacto).
3. Gancho al aro: 75 N por gancho (150 N repartidos) sobre el asiento curvo.
4. Tapa de la caja con izado de 150 N por el asa.
Material PETG manual: E 1700 MPa, ν 0.38, ρ 1270, σy 45 (σ entre capas 22).

## 7. Lo que hace falta para seguir

1. **Decisión C6** (bloqueante para la Fase 4).
2. Medidas: aro (Ø y sección), cable Arducam, KIT A, aro LED, impresora.
3. OK para pasar a la Fase 1.
