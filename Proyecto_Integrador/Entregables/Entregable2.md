# LanternGuard 🦪
> **Sistema de monitoreo de biofouling en linternas de cultivo de conchas de abanico**

---

## Descripción del Proyecto
LanternGuard es un sistema de monitoreo diseñado para medir el porcentaje de biofouling en las linternas utilizadas en el cultivo de conchas de abanico (acuicultura). El proyecto se divide en dos partes principales: un **nodo sumergido** (cámaras, sensor de proximidad y microcontrolador) y una **boya en la superficie** (panel solar, batería, módulo de comunicación y segundo microcontrolador) que envía los datos a la nube y al aplicativo para el usuario.

---

## 1. Caja Negra (Entradas y Salidas del Sistema)

La Caja Negra muestra las entradas y salidas principales que interactúan con nuestro sistema.

<img width="1774" height="1459" alt="Caja negra" src="https://github.com/user-attachments/assets/aa16bae0-18bc-41ab-9df6-a7357741ddef" />

---

## 2. Estructura de Funciones

Es el diagrama de bloques que muestra cómo funciona el sistema internamente dividiéndose por módulos.

<img width="2320" height="2228" alt="Esquema de funciones" src="https://github.com/user-attachments/assets/d86bfbf1-6cd5-4dec-93f4-336dca374436" />

### Módulos del Sistema:
* **Módulo Mecánico:** Encargado de la hermeticidad de la carcasa bajo el agua, la barrera contra el biofouling y el soporte físico de los componentes.
* **Módulo Eléctrico:** Recibe la energía solar, regula la carga, la almacena en la batería y la distribuye a los sensores, actuadores y comunicación.
* **Módulo de Sensores:** Toma de imágenes con las cámaras y medición con el sensor de proximidad.
* **Módulo de Actuadores:** Enciende la luz para tomar las fotos.
* **Módulo de Control y Procesamiento:** Administra los tiempos de encendido/apagado, sincroniza los datos e identifica la información.
* **Módulo de Comunicación:** Envía las fotos y los datos del sistema hacia la nube para mostrarlos en el aplicativo.

---

## 3. Matriz Morfológica

Presenta las diferentes alternativas de componentes y materiales evaluados para cumplir con cada función del diagrama.

<img width="1580" height="3002" alt="Matriz Morfológica" src="https://github.com/user-attachments/assets/62fb1dd2-454a-4b45-a9f3-21780d3b00ca" />

---

## 📊 4. Evaluación de Soluciones

Ponderación y selección de la mejor combinación de componentes según criterios de resistencia al agua, energía, costos y viabilidad del proyecto.

<img width="1246" height="682" alt="1" src="https://github.com/user-attachments/assets/46d0367f-82ab-41b9-9ce4-30720b1b7281" />

<img width="1868" height="531" alt="2" src="https://github.com/user-attachments/assets/108bd2bd-2179-44af-a89e-84733749e683" />

<img width="1862" height="761" alt="3" src="https://github.com/user-attachments/assets/40b9d48e-1723-4217-a347-e5e51f6d2bfe" />

---
