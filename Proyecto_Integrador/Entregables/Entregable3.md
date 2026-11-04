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

---

#### Boceto 2 - Solución preliminar 2

El segundo boceto representa una alternativa conceptual de LanternGuard basada en la Solución 2 de la matriz morfológica. Conserva la organización general del sistema mediante una boya de superficie y un módulo sumergido conectado por cable umbilical, pero plantea diferentes componentes electrónicos, materiales y mecanismos de adquisición, procesamiento y comunicación.

**Descripción técnica y funcional:**

* **Estrategia de muestreo:** Muestreo por umbral, basado en la activación del sistema ante un evento previamente definido. La condición de activación y sus parámetros deberán establecerse y validarse posteriormente.

* **Boya de superficie (nodo boya):**
  * **Alimentación:** Batería Li-Po de 10 000 mAh y módulo BMS para protección y gestión de la batería.
  * **Control y procesamiento:** Raspberry Pi Zero 2 W, considerada para supervisar las funciones de la boya y realizar procesamiento local de la información.
  * **Telemetría:** Módulo LoRa SX1276 para transmitir mensajes breves y metadatos hacia una estación receptora terrestre.
  * **Comunicación interna:** Enlace RS-485 mediante cable umbilical con el módulo sumergido.
  * **Visualización:** Dashboard web para consultar los resultados del monitoreo.

* **Barra y módulo sumergido (nodo sumergido):**
  * **Control:** Microcontrolador ESP32-WROOM-32U alojado en un compartimento electrónico protegido.
  * **Registro de movimiento:** Sensor inercial MPU-6050 para obtener información de aceleración y movimiento durante las inspecciones.
  * **Almacenamiento:** Memoria Flash W25Q128 como alternativa de almacenamiento electrónico, cuya capacidad disponible y suficiencia deberán evaluarse.
  * **Estructura y protección:** Carcasa fabricable mediante impresión 3D en ABS, con recubrimiento de resina epóxica como alternativa de protección superficial.
  * **Comunicación:** Transferencia de información hacia la boya mediante RS-485.

* **Cápsulas de cámara:**
  * **Captura:** Dos cámaras Arducam Mega de 5 MP con lente M12, orientadas hacia diferentes regiones de las mallas.
  * **Iluminación:** Módulos LED infrarrojos para apoyar la adquisición de imágenes, cuya compatibilidad con las cámaras deberá verificarse.
  * **Protección óptica:** Ventanas de vidrio templado marino y sellado mediante juntas O-ring.
  * **Tratamiento superficial:** Film hidrofóbico PET como alternativa para reducir la acumulación de agua y suciedad sobre las ventanas ópticas, pendiente de evaluación en condiciones submarinas.

* **Procesamiento y comunicación:**
  * **Procesamiento local:** Se contempla utilizar la Raspberry Pi Zero 2 W para desarrollar procedimientos de análisis de imágenes orientados a estimar la cobertura visible y el volumen de bioincrustación.
  * **Transmisión inalámbrica:** LoRa se utilizaría para mensajes breves y metadatos, mientras que las fotografías completas requerirían un procedimiento de transferencia local.
  * **Notificación:** Dashboard web para visualizar indicadores, registros e historial de inspecciones.

Esta alternativa utiliza componentes y materiales distintos de los seleccionados para el diseño principal de LanternGuard. Su representación permite comparar las posibilidades técnicas de la Solución 2 frente a las demás alternativas de la matriz morfológica.

<p align="center"><strong><em>Figura 2. Boceto de la Solución preliminar 2 del sistema LanternGuard.</em></strong></p>

<p align="center">
  <img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/b66c5076-6e49-4c28-863a-85913905350e" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se presenta la alternativa de diseño correspondiente a la Solución 2 de la matriz morfológica, considerando sus componentes electrónicos, materiales estructurales y funciones propuestas. Las características de procesamiento, comunicación y protección óptica deberán evaluarse y validarse durante etapas posteriores.</em></p>

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
