# Verificación a mano (generado por `verificacion.py`)

Carga de manipulación: 150 N en una cápsula; gancho: 75 N. PETG: E 1700 MPa, ν 0.38, σy 45 MPa macizo (a lo largo de las capas) y 22 MPa entre capas. Todos estimados. FS = σ admisible / σ calculada; se dan las dos columnas y se dice cuál aplica según la orientación de impresión.

## 1. Secciones del riel (cortes del CAD)

Corte de 0.05 mm del sólido real; I respecto del eje horizontal que pasa por el centroide; Z = I / c.

| Sección | A mm² | I mm⁴ | c mm | Z mm³ |
|---|---|---|---|---|
| ext_medio | 412 | 46051 | 15.3 | 3018 |
| punta_ranura_salida | 380 | 43882 | 15.4 | 2853 |
| union_hembra | 361 | 157248 | 32.2 | 4883 |
| union_macho | 229 | 6716 | 9.6 | 697 |

## 2. Riel con 150 N en la cápsula

Carga en el eje de la bisagra con el carro a ras de la punta (palanca máxima). La caída del eje bajo el riel no suma momento con carga vertical. El tramo se imprime acostado: la flexión va a lo largo de las capas (aplica 45).

**Caso A, nodo colgado del asa:** voladizo desde la caja. Momento en la unión central/extensión (|x| = 70) M = F·(x_carga − 70); en la sección llena σ = M/Z; en la media madera σ = M/Z_mitad. Flecha de la punta δ = F·L³/(3·E·I) con la sección llena (las uniones la aumentan).

**Caso B, nodo apoyado en los ganchos:** voladizo más allá del gancho, M = F·(x_carga − D/2).

| Aro | Ext. | Punta mm | x carga mm | A: M N·mm | A: σ llena MPa | A: σ media madera MPa | A: FS 45 / 22 (media madera) | A: flecha mm | B: M N·mm | B: σ MPa | B: FS 45 / 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ø100 | 0 | 115 | 127.5 | 8625 | 3.0 | 12.4 | 3.6 / 1.8 | 0.1 | 11625 | 4.1 | 11.0 / 5.4 |
| Ø200 | 1 | 215 | 227.5 | 23625 | 8.3 | 33.9 | 1.3 / 0.6 | 2.5 | 19125 | 6.7 | 6.7 / 3.3 |
| Ø300 | 1 | 215 | 227.5 | 23625 | 8.3 | 33.9 | 1.3 / 0.6 | 2.5 | 11625 | 4.1 | 11.0 / 5.4 |
| Ø500 | 2 | 315 | 327.5 | 38625 | 13.5 | 55.4 | 0.8 / 0.4 | 10.9 | 11625 | 4.1 | 11.0 / 5.4 |

Con la punta (C18) el carro entra a ras de la punta en todos los aros; la fila usa esa posición (palanca máxima).

## 3. Unión de tramos (media madera + llave en cola de milano + 2 M4 verticales)

Momento más cargado: caso A, M = 38625 N·mm. Par de fuerzas con brazo igual a la media altura de la media madera (z = 15): la mitad de arriba se apoya en el hombro y abajo aparece una tracción T = M / 15 = **2575 N** que tiende a separar las mitades a lo largo del riel. La toman los 2 M4 en corte simple y la llave en aplastamiento; se dan los dos por separado (ambos son conservadores porque comparten).

- M4 solos, corte: τ = T / (2·12.6 mm²) = **102 MPa** en el acero (A2-70: fluencia del orden de 450 MPa, corte del orden de 0.6 de eso, dato de catálogo por confirmar).
- M4 solos, aplastamiento del PETG: σ = T / (2·d·h) con d = 4.0 y h = 15 (media altura) = **21.5 MPa** → FS 2.1 (45, carga en el plano de las capas, tramo acostado) / 1.0 (22).
- Llave sola (8 × 11 × 4), aplastamiento en su cara de 8 × 4: σ = 80.5 MPa → FS 0.6 / 0.3; corte en su base 11 × 8: τ = 29.3 MPa.
- Flexión en la media madera: σ = M / Z_mitad = 55.4 MPa → FS 0.8 / 0.4.

### 3b. La unión según el largo del riel

Mismo caso A con la punta del riel en cada configuración: la decidida el 29/10 (C18), la mínima que deja armar gancho + carro (R + 64) y la anterior.

| Aro | Configuración | Punta mm | M en la unión N·mm | σ media madera MPa | FS 45 / 22 |
|---|---|---|---|---|---|
| Ø100 | decisión 29/10 (paso 100 + punta) | 115 | 8625 | 12.4 | 3.6 / 1.8 |
| Ø100 | mínima para armar | 114 | 8475 | 12.2 | 3.7 / 1.8 |
| Ø100 | anterior (extensiones solapadas, sin punta) | 70 | 1875 | 2.7 | 16.7 / 8.2 |
| Ø200 | decisión 29/10 (paso 100 + punta) | 215 | 23625 | 33.9 | 1.3 / 0.6 |
| Ø200 | mínima para armar | 164 | 15975 | 22.9 | 2.0 / 1.0 |
| Ø200 | anterior (extensiones solapadas, sin punta) | 155 | 14625 | 21.0 | 2.1 / 1.0 |
| Ø300 | decisión 29/10 (paso 100 + punta) | 215 | 23625 | 33.9 | 1.3 / 0.6 |
| Ø300 | mínima para armar | 214 | 23475 | 33.7 | 1.3 / 0.7 |
| Ø300 | anterior (extensiones solapadas, sin punta) | 155 | 14625 | 21.0 | 2.1 / 1.0 |
| Ø500 | decisión 29/10 (paso 100 + punta) | 315 | 38625 | 55.4 | 0.8 / 0.4 |
| Ø500 | mínima para armar | 314 | 38475 | 55.2 | 0.8 / 0.4 |
| Ø500 | anterior (extensiones solapadas, sin punta) | 240 | 27375 | 39.2 | 1.1 / 0.6 |

### 3c. Con la varilla M8 tensada (decisión 29/10, C19), M = 38625 N·mm

La varilla pasa por agujeros de Ø8.5 en todos los tramos, con su eje a z = 14.05 sobre el fondo del riel (bajo el Cat5e, sobre el canal de tuercas), y se aprieta a unos 500 N con tuerca y arandela ancha en las dos puntas. Las caras de PETG de la unión sólo pueden empujar: cuando el momento abre la unión, la tracción la toma la varilla y la compresión la cara de tope de la media madera. Es un par de fuerzas, como una viga de hormigón pretensado por tramos. Los 2 M4 y la llave siguen ahí y ayudan; no se cuentan.

- **Caso A (150 N hacia abajo, como el resto de la verificación):** compresión abajo. Conservador, sólo la pared del fondo (102 mm², centro a z = 2.0): brazo 12.05, varilla T = M / brazo = **3205 N**, PETG σ = T / A = **31.5 MPa** → FS 1.4 (45; los tramos se imprimen acostados o boca abajo y la compresión va a lo largo de las capas).
- Rotura con bloque uniforme a 45 MPa (el bloque más favorable llega a z = 13.5, 192 mm²): M_u = 78565 N·mm → **FS 2.0** contra el momento de diseño. Sin la varilla eran 0.8.
- **Caso inverso (150 N hacia arriba, por ejemplo levantar el nodo por una cápsula):** compresión en la pared de arriba (120 mm²), brazo 13.95: T = 2769 N, PETG 23.1 MPa → FS 2.0.
- **Varilla:** área resistente 36.6 mm². Con la mayor tracción (3205 N): σ = 88 MPa → FS 7.3 en grado 8.8 (640 MPa) y 2.7 en 4.6 (240 MPa). Grado `8.8` estimado: confirmar el comprado.
- **Arandela DIN 9021** (Ø24) contra la pared de la punta (5 de espesor): área útil 353 mm² (sin la boca del canal de tuercas) → 9.1 MPa → FS 4.9. Corte de la pared en el contorno del conducto (4 × 22 × 5): 7.3 MPa.
- **Rigidez:** varilla de 651 mm (Ø500), k = E·A/L = 11244 N/mm. De 500 a 3205 N se estira 0.24 mm: la unión se abre menos de eso a la altura de la varilla. El PETG apretado fluye con los días: reapretar la tuerca después de la primera semana en el agua.
- Todo es estimado (PETG, grado del acero, precarga) y la unión real además tiene holguras: la prueba a flexión de la unión con la varilla sigue siendo la que manda.

## 4. Insertos M4 del fondo de la caja (caso A)

El momento del riel entra a la caja por los 4 M4 de la brida de la cámara en (±40, ±20). Pivote en la línea de tornillos del lado opuesto (conservador): T_par = F·(x_carga + 40) / 80, la mitad por inserto.

| Aro | x carga mm | Tracción por inserto N |
|---|---|---|
| Ø100 | 127.5 | **157** |
| Ø200 | 227.5 | **251** |
| Ø300 | 227.5 | **251** |
| Ø500 | 327.5 | **345** |

**Exigencia:** cada inserto térmico M4 del fondo debe aguantar al menos 345 N de arranque en PETG (más el factor de seguridad que el equipo quiera). No hay dato de capacidad del inserto: hay que probarlo o tomarlo del fabricante.

## 5. Gancho con 75 N

Varilla en x = 0; alma de 12 × 12 de x = −12 a 0 (excentricidad e = 6); M4 de la perilla en x = -30.0; extremo de la brida en x = -47.0. La brida sólo puede empujar contra el fondo del riel, así que el apoyo está en el extremo del lado de la perilla y el perno toma la suma.

- Alma: σ = F/A + F·e/Z = 75/144 + 75·6/288 = **2.1 MPa** → FS 21.6 (45: el gancho se imprime de costado y la carga va en el plano de las capas).
- Reacción en el extremo de la brida R = F·24.0/17.0 = 106 N; perno M4 = F + R = **181 N**.
- Brida en el perno: M = 1800 N·mm, Z = (30 − 4.2)·6²/6 = 155 mm³, σ = **11.6 MPa** → FS 3.9 / 1.9.
- Tuerca M4 contra los labios de la ranura T (apoyo de 1.2 por lado × 7): σ = 10.8 MPa → FS 4.2 / 2.0 (tramo acostado: el labio trabaja en el plano de las capas, aplica 45).
- Asiento recto: flecha de la curva del aro sobre 12 de contacto, f = c²/(8R): Ø100 0.36 mm, Ø200 0.18 mm, Ø300 0.12 mm, Ø500 0.07 mm. El prompt pedía este cálculo: el asiento recto sirve.

## 6. Asa y tapa con 150 N de izado

- Barra del asa como viga simplemente apoyada de 90 (conservador), sección 12 × 10: M = F·L/4 = 3375 N·mm, σ = **16.9 MPa** → FS 2.7 (la tapa se imprime con el asa arriba: la barra flexa en el plano de las capas).
- Patas del asa: tracción a través de las capas, F/2 sobre 12 × 12: 0.52 MPa → FS 42 (22).
- 10 tornillos M3 con inserto en la brida: si sólo los tornillos llevan el izado, **15.0 N por inserto**, más la reacción de la junta tórica comprimida (sin dato: depende de la dureza del cordón).

## 7. Bisagra dentada

- Peso de la cápsula con contenido en aire: 128 g, centro a 43 del eje → par T = 54 N·mm (en el agua casi neutra: desplaza 128 cm³).
- Dientes: 36, alto 1.2, radio medio 9.5, semipaso 0.83 → flanco α = 55.4°. Par para saltar un diente con precarga axial N, dos caras: T = 2·N·r_m·tan(α + φ), con μ = 0.3 (estimado, φ = 16.7°): T = 58.7·N.
- Contra el peso propio: N ≥ 0.9 N. Contra 150 N en el frente (palanca 65): N ≥ **166 N**, que un M4 da con un par de apriete de unos 0.13 N·m (T = 0.2·d·N, coeficiente típico).
- Aplastamiento del M4 con 150 N: en las orejas 2 × 4 × 5 → 3.8 MPa; en la lengua 4 × 6.0 → 6.2 MPa. FS > 4 aun entre capas.

## 8. Presión a 1 m (0.0101 MPa), placas de Roark

σ = β·q·b²/t², y = α·q·b⁴/(E·t³) (Roark, 7.ª ed., tabla 11.4 caso 1a, bordes simplemente apoyados; coeficientes copiados de `cad/build.py`). La presión empuja hacia adentro: la tapa se apoya en la brida y la junta; los tornillos no la cargan.

| Placa | a × b mm | t mm | β | σ MPa | FS 45 / 22 | flecha mm |
|---|---|---|---|---|---|---|
| Tapa de la caja (campo de 5; bajo la ranura quedan 3.5) | 132 × 98 | 5 | 0.431 | 1.67 | 27 / 13 | 0.317 |
| Fondo de la caja | 132 × 98 | 4 | 0.431 | 2.60 | 17 / 8 | 0.619 |
| Pared larga | 132 × 46 | 4 | 0.699 | 0.93 | 48 / 24 | 0.054 |
| Pared corta | 98 × 46 | 4 | 0.624 | 0.83 | 54 / 27 | 0.047 |
| Pared de la cápsula | 38 × 38 | 4 | 0.287 | 0.26 | 173 / 84 | 0.009 |

Ventana de acrílico, placa circular simplemente apoyada en el hombro (radio libre 13, t 3, ν 0.37 típico): σ = 3(3+ν)·q·a²/(8t²) = **0.24 MPa**, frente a un acrílico típico de decenas de MPa (dato de material estimado, no medido).

## 9. Flotabilidad y estabilidad

Los números de flotabilidad son los de `fase_a.py`. En esta fase se corrigió su cálculo de estabilidad: el acero de las pletinas no sumaba a la masa total y las cápsulas iban a la altura del riel (ahora van con el eje bajo el riel, a 0 y a 90°).

Exigencias: peso aparente de +0.2 a +0.5 kgf, total en aire ≤ 3 kg.

| Relleno bandeja | Aro | Nodo sin acero g | Desplaza cm³ | Aparente sin acero g | Pletinas por lado | Aparente final g | En ventana | Total en aire g | ≤ 3 kg |
|---|---|---|---|---|---|---|---|---|---|
| 40 % | Ø100 | 1469 | 1626 | -198 | 3 | **+318** | sí | 2062 | sí |
| 40 % | Ø200 | 1647 | 1724 | -120 | 2 | **+224** | sí | 2042 | sí |
| 40 % | Ø300 | 1647 | 1724 | -120 | 2 | **+224** | sí | 2042 | sí |
| 40 % | Ø500 | 1825 | 1822 | -42 | 2 | **+301** | sí | 2220 | sí |
| 100 % | Ø100 | 1473 | 1626 | -194 | 3 | **+322** | sí | 2066 | sí |
| 100 % | Ø200 | 1651 | 1724 | -116 | 2 | **+228** | sí | 2046 | sí |
| 100 % | Ø300 | 1651 | 1724 | -116 | 2 | **+228** | sí | 2046 | sí |
| 100 % | Ø500 | 1829 | 1822 | -38 | 2 | **+305** | sí | 2224 | sí |

Totalmente sumergido no hay plano de flotación ni metacentro: el par adrizante al inclinarse un ángulo θ es B·BG·sen θ, con B el empuje y BG la distancia vertical del centro de masa (G) bajo el centro de empuje (B). BG > 0 quiere decir que no se voltea; el número que importa es BG. Las placas de acero ya están en G y en B.

| Aro | Inclinación de las cápsulas | z G mm | z B mm | BG mm | B N | Par adrizante a 10° N·mm |
|---|---|---|---|---|---|---|
| Ø100 | 0° | -34.8 | -12.7 | **22.1** | 17.1 | 66 |
| Ø100 | 90° | -40.1 | -19.2 | **21.0** | 17.1 | 62 |
| Ø200 | 0° | -34.6 | -14.4 | **20.2** | 17.8 | 63 |
| Ø200 | 90° | -40.0 | -20.6 | **19.4** | 17.8 | 60 |
| Ø300 | 0° | -34.6 | -14.4 | **20.2** | 17.8 | 63 |
| Ø300 | 90° | -40.0 | -20.6 | **19.4** | 17.8 | 60 |
| Ø500 | 0° | -36.3 | -16.5 | **19.7** | 18.8 | 64 |
| Ø500 | 90° | -41.2 | -22.4 | **18.8** | 18.8 | 62 |

Las cápsulas son casi neutras (128 g contra 128 cm³), así que bajarlas mueve G y B casi igual. El margen lo dan las pletinas bajo el riel contra el aire de la caja arriba.
