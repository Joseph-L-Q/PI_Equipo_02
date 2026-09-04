## 2.3. Joseph Lombardi

### Placa PCB para módulo de sensado de humedad y proximidad con ESP32-S3

Este apartado presenta el diseño y los archivos de fabricación de la placa PCB individual elaborada por **Joseph Lombardi**. La placa integra un microcontrolador **ESP32-S3**, un sensor **DHT11** y un sensor ultrasónico **HC-SR04** para el proyecto **LanternGuard**.

#### ¿Qué sensores utilicé y para qué sirven?

Los componentes principales utilizados son:

- **Sensor DHT11:** Permite medir la humedad y la temperatura dentro del sistema. Su línea de datos utiliza una resistencia *pull-up* de **10 kΩ**, conectada a **3.3 V**, para mantener estable la comunicación con el ESP32-S3.

- **Sensor ultrasónico HC-SR04:** Permite medir la distancia o proximidad de un objeto mediante ondas ultrasónicas. Este sensor funciona con una alimentación de **5 V**.

- **Divisor de voltaje:** Se utilizaron resistencias de **1 kΩ** y **2 kΩ** en la salida `ECHO` del HC-SR04. Este divisor reduce la señal de aproximadamente **5 V** a un nivel cercano a **3.3 V**, protegiendo la entrada del ESP32-S3.

La placa permite integrar los sensores y sus resistencias directamente con el microcontrolador mediante pistas ruteadas, evitando falsos contactos y el desorden generado por las conexiones en un protoboard.

#### ¿Por qué lo hice y cuál es su importancia?

Esta placa fue desarrollada como parte del proyecto universitario **LanternGuard**, con el propósito de obtener un circuito más ordenado, estable y seguro.

El diseño se divide en las siguientes secciones:

- **Módulo de control:** Formado por el microcontrolador ESP32-S3, encargado de recibir y procesar los datos de los sensores.
- **Módulo de humedad y temperatura:** Formado por el sensor DHT11 y su resistencia *pull-up* de **10 kΩ**.
- **Módulo de proximidad:** Formado por el sensor HC-SR04 y el divisor de voltaje compuesto por las resistencias de **1 kΩ** y **2 kΩ**.

El desarrollo de la PCB facilita la instalación de los componentes, reduce posibles errores de conexión y permite obtener una solución más compacta para su integración en la estructura final del proyecto.

#### Imágenes del diseño

**1. Esquemático**

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/dfa8ef5cfb81be3a7e531df7f3f92018af223741/Recursos/Im%C3%A1genes/esquematicoJoseph2.png" alt="Esquemático electrónico de Joseph Lombardi" width="80%">
  <br>
  <em><b>Figura 1.</b> Esquemático electrónico desarrollado por Joseph Lombardi.</em>
</p>

**2. Diseño de la PCB en 2D**

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/6d02315b309bb98c942aa9f847840294ac2baf20/Recursos/Im%C3%A1genes/placaJoseph2.png" alt="Diseño PCB 2D de Joseph Lombardi" width="80%">
  <br>
  <em><b>Figura 2.</b> Distribución y ruteado de los componentes en la placa PCB.</em>
</p>

**3. Vista 3D**

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/6d02315b309bb98c942aa9f847840294ac2baf20/Recursos/Im%C3%A1genes/placa3dSuperiorJoseph.png" alt="Vista 3D de la PCB de Joseph Lombardi" width="80%">
  <br>
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/6d02315b309bb98c942aa9f847840294ac2baf20/Recursos/Im%C3%A1genes/placa3dInferiorJoseph.png" alt="Vista 3D de la PCB de Joseph Lombardi" width="80%">
  <br>
  <em><b>Figura 3.</b> Representación tridimensional de la placa PCB diseñada.</em>
</p>

> **Nota de archivos Gerber:** El archivo comprimido con los Gerber necesarios para fabricar la placa PCB se encuentra disponible en: [`Gerber_Joseph_Lombardi.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/dfa8ef5cfb81be3a7e531df7f3f92018af223741/Recursos/Im%C3%A1genes/Gerber_Joseph_Corregido_PCB1_2026-09-04.zip).

---
