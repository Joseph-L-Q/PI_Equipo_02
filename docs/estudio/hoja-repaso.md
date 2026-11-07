# Hoja de repaso (1 página): examen mar 6/10/2026

**[V]** = dato verificado. **[S]** = supuesto. Fuentes y páginas: ver `preguntas-examen.md`.

## Definiciones clave

| Término | Definición corta |
|---|---|
| Mecatrónica | Mecánica + electrónica + TI integradas de forma sinérgica |
| Sistema mecatrónico | Sistema base + sensores + actores + procesamiento; flujos de material, energía e información |
| Micro-ciclo | Situación/meta -> análisis y síntesis -> evaluación -> decisión -> planificar o aprender |
| V-model | 2004: requisitos -> diseño del sistema -> diseño por dominio -> integración -> aseguramiento -> producto. 2020: tres franjas (núcleo, requisitos continuos, modelado y análisis); secuencia lógica, no temporal |
| Verificación / validación | ¿Se construyó bien? (contra la especificación) / ¿Es el producto correcto? (contra la necesidad del usuario). Métodos: análisis, inspección, demostración, ensayo |
| Integración | Distribuida (cables), modular (interfaces), espacial (una carcasa) |
| Lista de exigencias | E = exigencia, D = deseo; categorías: función, geometría, cinemática, fuerzas, energía, materia, señales, control |
| Caja negra / matriz morfológica | Función global con entradas y salidas, sin la solución / subfunciones x alternativas; N = m1 x m2 x ... x mn |
| Overfitting / transfer learning | Memoriza el entrenamiento y falla con datos nuevos / red preentrenada: congelar, entrenar la última capa, ajuste fino |
| Broker MQTT | Recibe, filtra por topic, distribuye, gestiona conexiones, seguridad y QoS (0 máximo una vez, 1 al menos una, 2 exactamente una) |

## Fórmulas

- Presión hidrostática: p = ρ·g·h. Con ρ ≈ 1025 kg/m³, g = 9.81 y h = 15 m: ≈ 151 kPa ≈ 0.15 MPa. A 5 m: ≈ 50 kPa.
- Factor de seguridad = resistencia / esfuerzo máximo (debe ser mayor que 1).
- ADC de 12 bits a 3.3 V: V = ADC x 3.3 / 4095.
- Regresión: ŷ = b0 + b1·x. MAE = (1/n)Σ|y - ŷ|. RMSE = √MSE. R² = 1 - SS_res/SS_tot.
- Perceptrón: y = f(Σ wᵢxᵢ + b). Sigmoide = 1/(1 + e⁻ᶻ). ReLU = max(0, x). Softmax = e^zⱼ / Σe^zₖ.
- Descenso del gradiente: x_nuevo = x_viejo - α·f'(x_viejo). MSE = (1/n)Σ(y - ŷ)². Entropía cruzada = -Σ p(x)·log q(x).
- Clasificación: precisión = VP/(VP+FP). Recall = VP/(VP+FN). F = 2PR/(P+R).
- % malla libre [S] = área de malla visible / área en la imagen de malla limpia x 100.

## Números del proyecto

| Dato | Valor |
|---|---|
| Biofouling por linterna | 68 a 73 kg en 2 a 3 meses (Loayza y Tresierra 2014) [V] |
| Recambio a 30 días | -64.6 % biofouling, +10.8 % supervivencia (Loayza-Aguilar 2025) [V] |
| Exportaciones 2025 | > US$ 188 millones FOB (Gestión 2026, Sanipes) [V] |
| Evaluación manual | ≈ 30 min por 100 puntos (First 2021) [V] |
| Faster R-CNN | mAP 93.14 % (Zhu 2025) [V] |
| Profundidad | 0 a 15 m (≈ 0.15 MPa); salinidad 35 g/L |
| Tracción / peso | > 150 N; 0.2 a 0.5 kgf aparente en agua; ≤ 3 kg en aire |
| Montaje / costo | ≤ 5 min con guantes; ≤ S/ 1200 |
| Potencia | Activa 2 a 5 W; reposo < 0.15 W |
| Error deseado | MAE < 15 % frente a un especialista |
| Bisagra | 0 a 90°, 36 dientes |
| ODS | 14 (14.b), 12 (12.2), 9 (9.5) |

**No usar:** 132 kg (no existe en la fuente); referencias README [3] y [4] (no existen).

## Arquitectura (Solución 1)

- Barra sobre el aro superior. Caja central: ESP32-WROOM-32U, JSN-SR04T, microSD, MAX485. Dos cápsulas con Arducam Mega 5 MP (SPI).
- RS-485 -> caja en boya: ESP32-S3, LoRa SX1276, 18650, LM2596, panel solar -> app.
- Procesamiento fuera de la placa (Python/OpenCV). Control: lazo abierto con decisión asistida.
- Por qué: no hay radio bajo el agua, LoRa es de largo alcance y bajo consumo, y es lo más barato y liviano.
- Alternativas: Sol. 2 Portenta H7 + Ethernet; Sol. 3 Raspberry Pi Zero 2 W + Wi-Fi + WhatsApp.

## Inconsistencias a explicar y buses

Comunicaciones distintas entre documentos (Wi-Fi, acústica, RS-485 + LoRa) | SimScale a 50 kPa (≈ 5 m) vs exigencia de 15 m (≈ 150 kPa) | cilindro 220 x 130 viejo en `main`.

**Buses:** SPI (MOSI, MISO, SCK, CS; rápido) | I2C (SDA, SCL; direcciones) | UART (TX, RX) | RS-485 (par diferencial, largo alcance). MQTT: puerto 1883 sin cifrar, 8883 con TLS.
