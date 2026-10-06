# Bocetos de las soluciones preliminares - Lanterguard

En esta sección se presentan las propuestas conceptuales y los bocetos de ingeniería para las tres alternativas de solución preliminares del proyecto **Lanterguard** (sistema de inspección y monitoreo de *biofouling* en cultivos de concha de abanico). 

Cada alternativa integra una boya de superficie, un umbilical de comunicación/alimentación y una barra principal sumergida con dos cápsulas ópticas laterales ajustables para inspeccionar los distintos niveles de la linterna de cultivo.

---

## Boceto 1 - Solución preliminar 1

<img width="1600" height="900" alt="Boceto1" src="https://github.com/user-attachments/assets/0d9b4e1a-0169-4118-acb3-a0fc3bf56ed8" />

### Descripción técnica y funcional:
* **Estrategia de Muestreo:** Muestreo periódico mediante *Timer* en modo de bajo consumo (*deep sleep*).
* **Boya de Superficie (Nodo Boya):**
  * **Alimentación:** Panel solar con banco de baterías Li-ion 18650 y regulador buck LM2596.
  * **Procesamiento y Control:** Microcontrolador ESP32-S3.
  * **Interfaz e Indicadores:** Interruptor basculante iluminado.
  * **Telemetría:** Módulo inalámbrico LoRa SX1276 con antena externa de larga distancia hacia un *Gateway* LoRa en tierra.
  * **Notificación al usuario:** Aplicación móvil dedicada (App móvil).
* **Barra y Módulo Sumergido (Nodo Sumergido):**
  * **Procesamiento:** Microcontrolador ESP32-WROOM-32U en caja estanca central.
  * **Sensores de Proximidad y Almacenamiento:** Sensor ultrasónico impermeabilizado JSN-SR04T y módulo MicroSD (SPI) para respaldo local.
  * **Comunicación Interna:** Cable umbilical industrial RS-485 entre la boya y el nodo sumergido.
  * **Estructura y Protección:** Carcasa de PTFE (Teflón) con recubrimiento de spray *antifouling* marino y limpieza de ventana mediante limpiaparabrisas / nanorrecubrimiento transparente.
* **Cápsulas de Cámara:**
  * **Captura de Imagen:** Dos cámaras Arducam Mega 5MP (Auto-Focus / Lente M12) montadas en bisagras dentadas para ajuste fino de ángulo por pasos.
  * **Iluminación y Sellado:** Anillo de luz LED SMD blanca alrededor de la lente, ventana protectora de acrílico transparente y sellado mediante junta *O-ring*.

---

## Boceto 2 - Solución preliminar 2

<img width="1600" height="900" alt="Boceto2" src="https://github.com/user-attachments/assets/e2a411e4-cf8b-418c-8029-81a71b572165" />

### Descripción técnica y funcional:
* **Estrategia de Muestreo:** Muestreo por umbral (activación por eventos de detección).
* **Boya de Superficie (Nodo Boya):**
  * **Alimentación:** Batería Li-Po de 10,000 mAh gestionada por un módulo BMS (Protección y balanceo).
  * **Procesamiento y Control:** Microcontrolador ESP32-WROOM-32U.
  * **Interfaz e Indicadores:** Pulsador con anillo LED integrado.
  * **Telemetría:** Módulo Ethernet W5500 con transmisión por cable Ethernet directo hacia una estación en tierra (router).
  * **Notificación al usuario:** Dashboard web interactivo.
* **Barra y Módulo Sumergido (Nodo Sumergido):**
  * **Procesamiento:** Placa de alto rendimiento Arduino Portenta H7 en caja estanca central.
  * **Sensores de Proximidad y Almacenamiento:** Sensor ToF Láser VL53L1X para medición precisa de distancia y memoria EEPROM AT24C256.
  * **Comunicación Interna:** Cable umbilical industrial RS-485.
  * **Estructura y Protección:** Carcasa de polietileno de alta densidad (HDPE) mecanizada con recubrimiento de resina epóxica *antifouling* y film hidrofóbico PET para limpieza óptica.
* **Cápsulas de Cámara:**
  * **Captura de Imagen:** Dos cámaras Arducam Mega 5MP (M02) ajustables mediante bisagra dentada.
  * **Iluminación y Sellado:** Tira LED COB integrada para iluminación uniforme, ventana de vidrio templado marino con spray repelente de agua y sellado hermético por *O-ring*.

---

## Boceto 3 - Solución preliminar 3

<img width="1600" height="900" alt="Boceto3" src="https://github.com/user-attachments/assets/8a7d94de-7a4d-4929-a2ab-c47256afb406" />

### Descripción técnica y funcional:
* **Estrategia de Muestreo:** Muestreo adaptativo basado en algoritmos de control.
* **Boya de Superficie (Nodo Boya):**
  * **Alimentación:** Panel solar con controlador de carga solar dedicado y batería de gel plomo-ácido de 12V.
  * **Procesamiento y Control:** Monoplaca Raspberry Pi Zero 2 W.
  * **Interfaz e Indicadores:** Pantalla OLED de 0.96" para monitoreo de estado en la boya (ej.: voltaje de batería).
  * **Telemetría:** Antena Wi-Fi SMA de 2.4 GHz para comunicación directa a router Wi-Fi en tierra.
  * **Notificación al usuario:** Bot de automatización en WhatsApp.
* **Barra y Módulo Sumergido (Nodo Sumergido):**
  * **Procesamiento:** Monoplaca Raspberry Pi Zero 2 W alojada en el nodo sumergido.
  * **Sensores de Proximidad y Almacenamiento:** Sensor ultrasónico UART A02YYUW y memoria Flash externa W25Q128.
  * **Comunicación Interna:** Cable umbilical industrial RS-485.
  * **Estructura y Protección:** Carcasa de PTFE mecanizada cubierta con lámina adhesiva de cobre como barrera *antifouling* y ventana con film hidrofóbico PET.
* **Cápsulas de Cámara:**
  * **Captura de Imagen:** Dos cámaras Arducam Mega 3MP (M02) montadas sobre soporte articulado con bisagra dentada.
  * **Iluminación y Sellado:** Módulo de iluminación LED infrarrojo (IR) para baja perturbación de la biomasa, ventana de policarbonato transparente con film hidrofóbico y sellado mediante junta *O-ring*.
