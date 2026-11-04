# Bocetos de las soluciones preliminares - Lanterguard

En esta sección se presentan las propuestas conceptuales y los bocetos de ingeniería para las tres alternativas de solución preliminares del proyecto **Lanterguard** (sistema de inspección y monitoreo de *biofouling* en cultivos de concha de abanico). 

Cada alternativa integra una boya de superficie, un umbilical de comunicación/alimentación y una barra principal sumergida con dos cápsulas ópticas laterales ajustables para inspeccionar los distintos niveles de la linterna de cultivo.

---

#### Boceto 1 - Solución preliminar 1

El primer boceto representa la configuración conceptual de LanternGuard correspondiente a la Solución 1 de la matriz morfológica. Se muestra la integración de una boya de superficie con un módulo sumergido instalado sobre una linterna de cultivo de concha de abanico (*Argopecten purpuratus*), así como los principales componentes electrónicos, estructurales y de comunicación considerados en la propuesta.

**Descripción técnica y funcional:**

* **Estrategia de muestreo:**
  * Inspecciones periódicas programadas cada 15 días, con una duración aproximada de cinco minutos para la adquisición de información.
  * Uso previsto de temporización y modos de bajo consumo energético (*deep sleep*) entre inspecciones.

* **Boya de superficie (nodo boya):**
  * **Alimentación:** Panel solar, baterías recargables de ion-litio 18650 y circuitos de regulación y gestión energética. Se contempla el regulador LM2596 para acondicionamiento de tensión; la configuración definitiva de carga solar deberá completarse.
  * **Control y comunicación:** Placa Heltec WiFi LoRa 32 V3, que integra un microcontrolador ESP32-S3 y un transceptor LoRa SX1262.
  * **Programación:** Reloj de tiempo real DS3231 para coordinar las inspecciones.
  * **Control de alimentación:** Interruptor de encendido y apagado.
  * **Comunicación con el módulo sumergido:** Enlace cableado RS-485 mediante transceptores MAX3485 y cable umbilical.
  * **Telemetría:** Transmisión de mensajes breves, estados y metadatos de inspección mediante LoRa hacia una estación receptora terrestre.

* **Barra y módulo sumergido (nodo sumergido):**
  * **Control:** Microcontrolador ESP32-S3-DevKitC-1-N16R8, ubicado dentro de un compartimento electrónico protegido.
  * **Registro de movimiento:** Acelerómetro triaxial LIS3DH para obtener información complementaria sobre el movimiento y la inclinación del módulo.
  * **Almacenamiento:** Módulo microSD mediante interfaz SPI para almacenar las fotografías y los registros obtenidos durante las inspecciones.
  * **Comunicación interna:** Cable umbilical RS-485 para la transferencia de información entre el módulo sumergido y la boya.
  * **Estructura:** Barra de soporte y piezas estructurales fabricables mediante impresión 3D con material PETG.
  * **Protección:** Compartimento electrónico estanco y medidas de protección frente al ambiente marino.

* **Cápsulas de cámara:**
  * **Captura de imágenes:** Dos cámaras Arducam Mega de 5 MP con enfoque automático, orientadas hacia diferentes regiones de las mallas.
  * **Posicionamiento:** Soportes de cámara que permiten establecer las orientaciones de captura previstas en el diseño.
  * **Iluminación:** Aros LED de luz blanca para favorecer la adquisición de fotografías submarinas.
  * **Protección óptica:** Ventanas transparentes de acrílico y elementos de sellado mediante juntas O-ring.
  * **Protección superficial:** Aplicación propuesta de un tratamiento antifouling y de un recubrimiento transparente hidrofóbico para reducir la adherencia de organismos y favorecer las condiciones de las ventanas ópticas. Su eficacia deberá evaluarse posteriormente.

* **Comunicación, procesamiento y visualización:**
  * **Recepción terrestre:** Estación receptora basada en Heltec WiFi LoRa 32 V3 para recibir los mensajes transmitidos desde la boya.
  * **Fotografías completas:** Almacenamiento y recuperación mediante una transferencia local posterior, cuyo procedimiento específico aún debe definirse.
  * **Procesamiento de imágenes:** Servicio de procesamiento destinado a estimar el porcentaje de cobertura visible de bioincrustación y desarrollar un algoritmo propio para estimar el volumen acumulado en las regiones analizadas.
  * **Notificación al usuario:** Aplicativo LanternGuard para visualizar fotografías, resultados e historial de inspecciones, sin limitar su uso exclusivamente a dispositivos móviles.

La Solución preliminar 1 constituye la alternativa seleccionada por el equipo como base para el diseño conceptual de LanternGuard. Su configuración permite integrar las funciones de adquisición de imágenes submarinas, registro de movimiento, alimentación, protección estructural y comunicación, orientadas al monitoreo periódico de la bioincrustación.

<p align="center"><strong><em>Figura 1. Boceto de la Solución preliminar 1 del sistema LanternGuard.</em></strong></p>

<p align="center">
 <img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/a5e23aaf-b8f5-4b65-97db-a3880adfd248" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se presenta la vista general de LanternGuard y los detalles conceptuales de la boya de superficie, el módulo sumergido y la cápsula de cámara. El boceto corresponde a la Solución 1 de la matriz morfológica y considera los componentes y materiales seleccionados por el equipo. Las funciones de estimación volumétrica, gestión energética y recuperación local de fotografías requieren desarrollo o validación posterior.</em></p>


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
