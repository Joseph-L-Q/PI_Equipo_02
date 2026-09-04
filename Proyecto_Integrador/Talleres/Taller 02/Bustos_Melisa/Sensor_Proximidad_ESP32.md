# Placa PCB para Sensor de Proximidad con ESP32

Este apartado contiene los archivos de fabricación y el diseño de nuestra placa PCB, elaborada para integrar un microcontrolador ESP32-S3 con un módulo de sensores. 

## ¿Qué sensor utilicé y para qué sirve?

El componente central para las mediciones es el **JSN-SR04T**, un sensor de proximidad ultrasónico de grado industrial. 

El propósito de esta placa es servir como una base física sólida y robusta. Al integrar el sensor y la batería directamente al ESP32 a través de pistas ruteadas, eliminamos por completo la inestabilidad, los falsos contactos y el clásico desorden de cables sueltos que solemos tener al usar un protoboard.

## ¿Por qué lo hicé y cuál es su importancia?

Desarrollé esta placa como parte de mi proyecto universitario para tener un circuito más ordenado, seguro y fácil de manejar. 

Para que la arquitectura del diseño sea clara, la dividí en tres partes clave:

* **Módulo de Procesamiento:** El cerebro del sistema, comandado por nuestro ESP32.
* **Módulo de Alimentación:** Conectores de energía mecánicamente seguros para la batería.
* **Módulo de Proximidad:** La interfaz directa para la conexión con el entorno.

## Imágenes del Diseño

**1. Esquemático**

<img width="2362" height="1751" alt="Esquemático_Bustos_Melisa" src="https://github.com/user-attachments/assets/0cc9d4dc-f0ac-47e3-bbc1-c5e1cfeaf505" />

**2. Diseño de la PCB (2D)**

<img width="2160" height="2652" alt="PCB_PCB1_2026-09-03" src="https://github.com/user-attachments/assets/db24daa2-b1e2-4976-8c91-85a381065bd7" />

**3. Vista 3D**

<img width="2160" height="1968" alt="3D_PCB1_2026-09-030" src="https://github.com/user-attachments/assets/3527fbfa-2e5a-4b5d-8c95-27d64b3bad1a" />

<img width="2160" height="1724" alt="3D_PCB1_2026-09-031" src="https://github.com/user-attachments/assets/074f2272-58a0-4aa6-aaf7-d56d77b62e92" />

<img width="2160" height="1828" alt="3D_PCB1_2026-09-032" src="https://github.com/user-attachments/assets/93bc072d-0a97-46b8-bda5-64ad2efb0d9c" />

<img width="2160" height="1565" alt="3D_PCB1_2026-09-033" src="https://github.com/user-attachments/assets/bdbb22c5-aa4d-48fd-bd78-3a0980914632" />
