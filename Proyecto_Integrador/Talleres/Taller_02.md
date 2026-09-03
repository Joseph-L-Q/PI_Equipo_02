# Taller 02: Diseño del Esquema Electrónico en EasyEDA

## 1. Descripción del Trabajo
En este taller se realizó la introducción al diseño de esquemáticos electrónicos y a la creación de PCB en EasyEDA mediante un circuito de prueba individual (indicador LED con resistencia de protección y conector de alimentación H1). Asimismo, se establecieron las bases del esquema electrónico para el proyecto **LanternGuard**, configurando líneas de alimentación y módulos de sensado. Cada integrante generó su respectivo esquema y archivo Gerber para exportación.

---

## 2. Esquemáticos del Circuito de Prueba

### 2.1. María Antezana

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Esquem%C3%A1tico_prueba_Antezana.png" alt="Esquema Electrónico - María Antezana" width="80%">
  <br>
  <em><b>Figura 1.</b> Esquemático del circuito de prueba en EasyEDA elaborado por María Antezana.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Maria_2026-09-01.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Gerber_PCB1_2026-09-01.zip).

---

### 2.2. Melissa Bustos

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Esquem%C3%A1tico_Prueba_Melisa.png" alt="Esquema Electrónico - Melissa" width="80%">
  <br>
  <em><b>Figura 2.</b> Esquemático del circuito de prueba en EasyEDA elaborado por Melissa.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Melisa_2026-09-01.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Gerber_Prueba_Melisa_2026-09-01.zip).

---

### 2.3. Joseph Lombardi

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/ab9084373628f2e3de4e49a7390c74c93baff3af/Recursos/Im%C3%A1genes/Prueba_Joseph.png" alt="Esquema Electrónico - Joseph" width="80%">
  <br>
  <em><b>Figura 2.</b> Esquemático del circuito de prueba en EasyEDA elaborado por Joseph.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Joseph_2026-09-01.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/ab9084373628f2e3de4e49a7390c74c93baff3af/Recursos/Im%C3%A1genes/Gerber_Joseph_2026-09-01.zip).

---

### 2.4. Yoichi Palacios

<p align="center">
  <img src="../Recursos/esquema_electronico_integrante4.png" alt="Esquema Electrónico - Integrante 4" width="80%">
  <br>
  <em><b>Figura 4.</b> Esquemático del circuito de prueba en EasyEDA elaborado por [Nombre Integrante 4].</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Integrante4_2026-09-01.zip`](../Recursos/Gerber_Integrante4_2026-09-01.zip).

---

### 2.5. Gabriela Santamaria

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Esquem%C3%A1tico_Prueba_Santamaria.png" alt="Esquema Electrónico - Gabriela Santamaria" width="80%">
  <br>
  <em><b>Figura 5.</b> Esquemático del circuito de prueba en EasyEDA elaborado por Gabriela Santamaria.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Santamaria_PCB1_2026-09-01.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Gerber_Santamaria_PCB1_2026-09-01.zip).
---

## 3. Bases del esquemático para LanternGuard

Para la integración con el microcontrolador ESP32 en el módulo de control, se contemplan las siguientes entradas de sensado:

* **Sensor de Humedad Interna:** Encargado de monitorear el nivel de condensación en el gabinete estanco para activar el ventilador de ventilación.
* **Sensor de Proximidad:** Utilizado para detectar la presencia/distancia óptima de la malla previa a la captura fotográfica.


### 3.1. María Antezana

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Esquem%C3%A1tico_sensores_Antezana.png" alt="Esquema Electrónico - María Antezana" width="80%">
  <br>
  <em><b>Figura 6.</b> Esquemático del módulo de sensores de Lantern Guard en EasyEDA elaborado por María Antezana.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Maria_2026-09-01.zip`](...).

---

### 3.2. Melissa Bustos

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Esquem%C3%A1tico_Sensor_Melisa.png" alt="Esquema Electrónico - Melissa" width="80%">
  <br>
  <em><b>Figura 7.</b> Esquemático del módulo de sensores de Lantern Guard en EasyEDA elaborado por Melissa.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Melisa_2026-09-02.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Gerber_Sensor_Melisa_2026-09-02.zip).

---

### 2.3. Joseph Lombardi

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/ab9084373628f2e3de4e49a7390c74c93baff3af/Recursos/Im%C3%A1genes/Prueba_Joseph.png" alt="Esquema Electrónico - Joseph" width="80%">
  <br>
  <em><b>Figura 2.</b> Esquemático del circuito de prueba en EasyEDA elaborado por Joseph.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Joseph_2026-09-01.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/ab9084373628f2e3de4e49a7390c74c93baff3af/Recursos/Im%C3%A1genes/Gerber_Joseph_2026-09-01.zip).

---

### 3.4. Yoichi Palacios

<p align="center">
  <img src="../Recursos/esquema_electronico_integrante4.png" alt="Esquema Electrónico - Integrante 4" width="80%">
  <br>
  <em><b>Figura 9.</b> Esquemático del módulo de sensores de Lantern Guard en EasyEDA elaborado por [Nombre Integrante 4].</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en: [`Gerber_Integrante4_2026-09-01.zip`](../Recursos/Gerber_Integrante4_2026-09-01.zip).

---

### 3.5. Gabriela Santamaria

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Esquem%C3%A1tico_sensor_Santamaria.png" alt="Esquema Electrónico - Gabriela Santamaria" width="80%">
  <br>
  <em><b>Figura 10.</b> Esquemático del módulo de sensores de Lantern Guard en EasyEDA elaborado por Gabriela Santamaria.</em>
</p>

> **Nota de Archivos Gerber:** El archivo comprimido con los Gerber de este circuito se encuentra disponible en:  [`Gerber_Santamaria_Sensor_PCB1_2026-09-02.zip`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Gerber_Santamaria_Sensor_PCB1_2026-09-02.zip).
---

