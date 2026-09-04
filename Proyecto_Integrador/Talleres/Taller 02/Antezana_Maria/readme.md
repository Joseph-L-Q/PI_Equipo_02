# Placa PCB para Módulo de Sensado (Humedad) con ESP32-S3

Este apartado contiene los archivos de fabricación y el diseño de mi placa PCB individual, elaborada para integrar un microcontrolador **ESP32-S3** con el módulo de sensado para el proyecto **LanternGuard**. 

## ¿Qué sensor utilicé y para qué sirve?

El componente principal implementado en el diseño es:

* **Sensor de Humedad y Temperatura (DHT22 / AM2302):** Encargado de monitorear los niveles de condensación y humedad en el gabinete estanco para prevenir fallas y determinar el accionamiento del sistema de ventilación/desempañado. Incluye su respectiva resistencia de *pull-up* ($10\text{ k}\Omega$) entre la línea de alimentación $3.3\text{V}$ y el pin de datos `SDA` para garantizar la estabilidad de la lectura.

El propósito de esta placa es servir como una base física sólida y ordenada. Al integrar el sensor y la resistencia de acondicionamiento directamente al ESP32-S3 mediante pistas ruteadas en la PCB, eliminamos la inestabilidad, los falsos contactos y el desorden de cables de un protoboard.

## ¿Por qué lo hice y cuál es su importancia?

Desarrollé esta placa como parte de mi proyecto universitario para tener un circuito más ordenado, seguro y eficiente dentro de la arquitectura de **LanternGuard**. 

Para que la distribución del diseño sea clara, la dividí en tres secciones principales:

* **Módulo de Control:** El cerebro del sistema, comandado por nuestro microcontrolador ESP32-S3.
* **Módulo de Sensado:** La interfaz dedicada para la adquisición de datos del sensor DHT22.
* **Módulo de Resistencia:** La etapa de acondicionamiento de señal con la resistencia de $10\text{ k}\Omega$ integrada.

## Imágenes del Diseño

**1. Esquemático**

<img width="80%" alt="Esquemático_Antezana_Maria" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/SCH_Schematic1_1-P1_Antezana_sensores.png" />

**2. Diseño de la PCB (2D)**

<img width="80%" alt="PCB_Antezana_Maria" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/2D_Sensores_Antezana.png" />

**3. Vista 3D**

<img width="80%" alt="Vista3D_Antezana_Maria" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/3D_Sensores_Antezana.png" />
<img width="80%" alt="Vista3D_Antezana_Maria" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/3D_sensore_Ante.png" />

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber necesarios para la fabricación de la placa PCB se encuentra disponible en: [`Gerber_Maria_2026-09-04.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Proyecto_Integrador/Talleres/Taller%2002/Antezana_Maria/Gerber_PCB1_Antezana_Sensores.zip).
