# Reporte de verificación (generado por `build.py`)

No editar a mano: se regenera. Valores en mm, cm³, g y MPa.

## 1. Piezas: sólido cerrado e imprimible

Cama supuesta 220 × 220 × 250 mm. Voladizo = caras con normal hacia abajo a más de 45° de la vertical, fuera de la cama, en la orientación de impresión indicada.

| Pieza | Archivo | Material | Cant. | Sólido válido | Estanco (STL) | Cuerpos | Volumen cm³ | Masa g (100 % relleno) | Caja en orientación de impresión | Cabe en la cama | Voladizo mm² |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | `P1_caja_central_cuerpo` | PETG | 1 | sí | sí | 1 | 238.3 | 303 | 162 × 94 × 60 | sí | 570 |
| P2 | `P2_caja_central_tapa` | PETG | 1 | sí | sí | 1 | 118.9 | 151 | 160 × 94 × 64 | sí | 1847 |
| P3 | `P3_brazo` | PETG | 2 | sí | sí | 1 | 63.9 | 81 | 42 × 34 × 192 | sí | 930 |
| P4 | `P4revB_capsula_cuerpo` | PETG | 2 | sí | sí | 1 | 48.4 | 61 | 64 × 64 × 48 | sí | 1101 |
| P5 | `P5_capsula_tapa` | PETG | 2 | sí | sí | 1 | 23.4 | 30 | 64 × 64 × 33 | sí | 699 |
| P6 | `P6_bisel_ventana` | PETG | 2 | sí | sí | 1 | 2.3 | 3 | 42 × 42 × 2 | sí | 0 |
| P7 | `P7_ventana` | acrílico 3 mm (comprado, cortado) | 2 | sí | sí | 1 | 2.1 | 3 | 3 × 30 × 30 | sí | 54 |
| P8 | `P8_marco_malla_prueba` | PETG | 1 | sí | sí | 1 | 71.4 | 91 | 200 × 200 × 6 | sí | 0 |

## 2. Espesores mínimos que quedan bajo cada corte

Mínimo aceptado: 1.2 mm (3 perímetros de boquilla 0.4).

| Zona | Espesor mm | ¿≥ mínimo? |
|---|---|---|
| Hombro de la ventana (pared frontal − asiento) | 2.80 | sí |
| Tapa cápsula bajo la ranura del O-ring | 3.50 | sí |
| Tapa caja bajo la ranura del O-ring | 4.50 | sí |
| Ranura ↔ agujero de tornillo (cápsula) | 1.25 | sí |
| Ranura ↔ cavidad (cápsula) | 2.95 | sí |
| Ranura ↔ agujero de tornillo (caja, lado corto) | 1.75 | sí |
| Ranura ↔ cavidad (caja, lado corto) | 3.45 | sí |
| Fondo del inserto M3 ↔ cavidad (almohadilla del brazo) | 9.00 | sí |
| Agujero piloto M2 del bisel ↔ cavidad | 2.00 | sí |
| Pared de brazo | 3.00 | sí |
| Barra de malla de prueba | 2.00 | sí |

## 3. Encaje de componentes e interferencias

| Par | Volumen de interferencia mm³ | Holgura mínima mm | Resultado |
|---|---|---|---|
| esp32_devkit_wroom32u ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| esp32_devkit_wroom32u ↔ caja (tapa) | 0.00 | 36.00 | OK |
| microsd_module ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| microsd_module ↔ caja (tapa) | 0.00 | 37.00 | OK |
| max485_module ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| max485_module ↔ caja (tapa) | 0.00 | 37.00 | OK |
| jsn_sr04t_board ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| jsn_sr04t_board ↔ caja (tapa) | 0.00 | 39.00 | OK |
| jsn_sr04t_probe ↔ caja (cuerpo) | 0.00 | 0.20 | OK |
| jsn_sr04t_probe ↔ caja (tapa) | 0.00 | 38.00 | OK |
| contratuerca PG7 (+X) ↔ esp32_devkit_wroom32u | 0.00 | 72.04 | OK |
| contratuerca PG7 (+X) ↔ microsd_module | 0.00 | 82.12 | OK |
| contratuerca PG7 (+X) ↔ max485_module | 0.00 | 12.72 | OK |
| contratuerca PG7 (+X) ↔ jsn_sr04t_board | 0.00 | 5.50 | OK |
| contratuerca PG7 (+X) ↔ jsn_sr04t_probe | 0.00 | 48.46 | OK |
| contratuerca PG7 (−X) ↔ esp32_devkit_wroom32u | 0.00 | 2.50 | OK |
| contratuerca PG7 (−X) ↔ microsd_module | 0.00 | 4.40 | OK |
| contratuerca PG7 (−X) ↔ max485_module | 0.00 | 81.01 | OK |
| contratuerca PG7 (−X) ↔ jsn_sr04t_board | 0.00 | 83.18 | OK |
| contratuerca PG7 (−X) ↔ jsn_sr04t_probe | 0.00 | 48.46 | OK |
| cámara ↔ cápsula (cuerpo) | 0.00 | 1.00 | OK |
| cámara ↔ cápsula (tapa) | 0.00 | 16.00 | OK |
| ventana ↔ cápsula (cuerpo) | 0.00 | 0.00 | OK |

Bisagra: la lengüeta de la tapa engrana con las orejas del brazo. Se comprueba el cuerpo de la cápsula contra el brazo en todo el rango; los dientes de la tapa contra los del brazo se reportan aparte porque se tocan por diseño (flanco con flanco).

| Ángulo | Cuerpo cápsula ↔ brazo mm³ | Holgura mm | Tapa (sin dientes) ↔ brazo mm³ |
|---|---|---|---|
| 0° | 0.00 | 12.97 | 0.00 |
| 10° | 0.00 | 12.97 | 0.00 |
| 20° | 0.00 | 12.97 | 0.00 |
| 30° | 0.00 | 12.97 | 0.00 |
| 40° | 0.00 | 12.97 | 0.00 |
| 50° | 0.00 | 12.97 | 0.00 |
| 60° | 0.00 | 12.97 | 0.00 |
| 70° | 0.00 | 12.97 | 0.00 |
| 80° | 0.00 | 11.48 | 0.00 |
| 90° | 0.00 | 8.50 | 0.00 |

Dientes engranados a 40° (ángulo de trabajo): solape 0.00 mm³ (≈ 0 = flancos en contacto, sin juego ni choque).

## 4. Peso y flotabilidad (exigencia: peso aparente de 0.2 a 0.5 kgf; ≤ 3 kg en aire)

| Concepto | Valor |
|---|---|
| PETG impreso (sin el marco de prueba), 100 % relleno | 804 g |
| Ventanas de acrílico | 5 g |
| Electrónica (datasheets, ver params.py) | 63 g |
| Cables y prensaestopas (supuesto) | 40 g |
| Tornillería (supuesto) | 60 g |
| **Masa total en aire** | **972 g** (cumple ≤ 3 kg) |
| Aire sellado (caja 470 + 2 cápsulas × 61) | 592 cm³ |
| Volumen desplazado | 1237 cm³ |
| Empuje en agua de mar (1.025 g/cm³) | 1268 g |
| **Peso aparente** | **-295 g** (flota) |
| Lastre para entrar en 0.2 a 0.5 kgf | 495 a 795 g de peso aparente (acero inoxidable: ×1.15 en aire, ≈ 570 a 915 g) |

El relleno real < 100 % baja la masa y deja aire atrapado en las paredes: el peso aparente real será más negativo. Medir en balde y ajustar el lastre.

## 5. Presión a 15 m (0.15 MPa): placa plana, estimación de Roark

Fórmula: σ = β·q·b²/t², y = α·q·b⁴/(E·t³). Roark, *Formulas for Stress and Strain*, 7.ª ed., tabla 11.4 caso 1a (bordes simplemente apoyados, más conservador que empotrado). σy PETG = 45.0 MPa, E = 1700 MPa (valores tentativos del T01).

| Panel | a × b mm | t mm | β | σ MPa | FS = σy/σ | Flecha mm |
|---|---|---|---|---|---|---|
| Tapa de la caja | 132 × 66 | 6 | 0.610 | 11.1 | 4.1 | 0.86 |
| Fondo de la caja | 132 × 66 | 6 | 0.610 | 11.1 | 4.1 | 0.86 |
| Pared lateral de la caja | 132 × 54 | 5 | 0.656 | 11.5 | 3.9 | 0.73 |
| Pared extrema de la caja | 66 × 54 | 5 | 0.385 | 6.7 | 6.7 | 0.38 |
| Pared de la cápsula | 42 × 38 | 4 | 0.334 | 4.5 | 9.9 | 0.15 |
| Tapa de la cápsula | 38 × 38 | 5 | 0.287 | 2.5 | 18.1 | 0.07 |

FDM es anisótropo: entre capas la resistencia puede caer a la mitad o menos. Con FS ≥ 2.5 en todas las placas el margen sigue siendo positivo, pero **no está probado**: falta el ensayo en cámara de presión o a profundidad. Las simulaciones SimScale del equipo usaron 50 kPa (≈ 5 m), un tercio de esta carga.

## 6. Junta tórica (sello de cara, estático)

Cordón Ø2.0 mm en ranura de 2.6 × 1.5 mm: compresión 25 % (rango habitual 15 a 30 % para sello estático), llenado de ranura 81 % (< 90 %). Calculado, **no probado**.
