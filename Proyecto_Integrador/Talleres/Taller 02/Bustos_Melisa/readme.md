# Placa PCB para Módulo de Proximidad Ultrasónica con ESP32-S3

Este apartado contiene los esquemáticos y archivos de fabricación de mi placa PCB individual, diseñada para integrar de forma segura un microcontrolador **ESP32-S3** con instrumentación de sensado de distancia.

## ¿Qué sensor utilicé y cuál es su función?

El componente central para la adquisición de datos en este diseño es:

**Sensor Ultrasónico Impermeable (JSN-SR04T):** Un módulo de proximidad de grado industrial ideal para medir distancias en entornos exigentes. Para su correcta implementación, la placa integra un **divisor de voltaje** (conformado por resistencias de 1kΩ y 2kΩ) en la línea de datos. Esta etapa de acondicionamiento es crítica, ya que adapta el pulso de retorno (`ECHO`) de 5V del sensor a los 3.3V que maneja el ESP32-S3, protegiendo al microcontrolador de posibles daños.

El objetivo principal de esta PCB es proporcionar un soporte de hardware altamente confiable. Al trasladar el ESP32, las conexiones del sensor y la etapa de protección a pistas de cobre, se mitigan los problemas de ruido eléctrico, variaciones de tensión y los falsos contactos típicos de los montajes temporales en protoboard.

## ¿Por qué lo hice y cuál es su importancia?

Esta placa fue desarrollada para mi proyecto universitario **LanternGuard** con el propósito de pasar de un prototipo básico a una implementación técnica mucho más compacta y ordenada.

Para facilitar la lectura del esquemático y su posterior ensamblaje, la arquitectura del circuito se ha estructurado en los siguientes bloques:

* **Módulo de Procesamiento:** La unidad central de control y lógica, gobernada por el microcontrolador ESP32-S3.
* **Módulo de Alimentación:** Interfaz de entrada mediante borneras de conexión segura para energizar el circuito de forma estable.
* **Módulo de Proximidad y Acondicionamiento:** Los puertos dedicados para el sensor JSN-SR04T, junto con la red de resistencias (1kΩ y 2kΩ) que garantizan la integridad de las señales.
* **Fijación Mecánica:** Agujeros de montaje estratégicamente distribuidos para asegurar la placa a la estructura del proyecto.

## Imágenes del Diseño

**1. Esquemático**

<img width="2362" height="1751" alt="SCH_Schematic1_Bustos_Melisa" src="https://github.com/user-attachments/assets/a7b8124e-ec6d-4810-a8ad-2bf8c6061470" />

**2. Diseño de la PCB (2D)**

<img width="2160" height="2653" alt="PCB_PCB1_2026-09-04" src="https://github.com/user-attachments/assets/3c5527c8-1d34-4e50-a8e8-bda29d3ab72e" />

**3. Vista 3D**

<img width="2160" height="1974" alt="3D_PCB1_2026-09-04" src="https://github.com/user-attachments/assets/7b28b192-e8d5-4a1d-bd14-a2b5d6115b16" />

<img width="2160" height="1719" alt="3D_PCB1_2026-09-040" src="https://github.com/user-attachments/assets/e6e844b2-5b63-4dd9-8977-976cab03613a" />

<img width="2160" height="1668" alt="3D_PCB1_2026-09-041" src="https://github.com/user-attachments/assets/65f15314-e857-4227-b108-33f4743b9dc3" />

<img width="2160" height="2662" alt="3D_PCB1_2026-09-042" src="https://github.com/user-attachments/assets/28bdd78d-8dd4-490b-b020-1345e83b05f0" />
