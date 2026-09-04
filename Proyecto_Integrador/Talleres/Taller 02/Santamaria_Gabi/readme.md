# Placa PCB para Sensor de Humedad/Temperatura con ESP32

Este apartado contiene los archivos de fabricación y el diseño de mi placa PCB, elaborada para integrar un microcontrolador **ESP32-S3-DEV-KIT-N8R8** con un módulo de sensores.

## ¿Qué sensor utilicé y para qué sirve?

El componente central para las mediciones es el **DHT22 (AM2302)**, un sensor digital de humedad y temperatura de uso común en proyectos de monitoreo ambiental.

El propósito de esta placa es servir como una base física sólida y robusta. Al integrar el sensor directamente al ESP32-S3-DEV-KIT-N8R8 a través de pistas ruteadas (incluyendo la resistencia pull-up necesaria para la comunicación de datos), eliminamos por completo la inestabilidad, los falsos contactos y el clásico desorden de cables sueltos que solemos tener al usar un protoboard.

## ¿Por qué lo hice y cuál es su importancia?

Desarrollé esta placa como parte de mi proyecto universitario para detectar incrustaciones en las linternas de conchas de abanico, buscando tener un circuito más ordenado, seguro y fácil de manejar.

Para que la arquitectura del diseño sea clara, la dividí en dos partes:

* **Módulo de Procesamiento:** El cerebro del sistema, comandado por nuestro ESP32-S3-DEV-KIT-N8R8.
* **Módulo de Sensor de Humedad/Temperatura:** La interfaz directa para la medición de las condiciones ambientales, junto con su resistencia pull-up.

## Imágenes del Diseño

**1. Esquemático**

<img width="1497" height="1062" alt="Captura de pantalla 2026-09-03 232957" src="https://github.com/user-attachments/assets/ce33615d-ceda-4bee-bf70-4105aea1083b" />

**2. Diseño de la PCB (2D)**

<img width="422" height="377" alt="Captura de pantalla 2026-09-03 232456" src="https://github.com/user-attachments/assets/dcf4c3ae-288a-4f94-beba-46b31883acc7" />


**3. Vista 3D**

<img width="1238" height="727" alt="Captura de pantalla 2026-09-03 232648" src="https://github.com/user-attachments/assets/f3229288-1f05-4d5c-82ee-bf10f61904d5" />

