# Placa PCB para Nodo Sumergido de Inspección Visual con ESP32

Este apartado contiene el diseño y los archivos de fabricación de mi placa PCB individual, elaborada para integrar un microcontrolador **ESP32** con el conjunto de cámaras y sensores del **nodo sumergido** del proyecto **LanternGuard**. Es la placa que va dentro de la cápsula estanca y la que concentra la captura de imágenes de la malla de la linterna, el registro local y el enlace hacia la boya de superficie.

## ¿Qué sensores utilicé y para qué sirven?

Los componentes principales utilizados son:

- **Dos cámaras Arducam Mega (SPI):** capturan las imágenes RGB de la malla de la linterna. Comparten el bus SPI del ESP32 y se seleccionan una a la vez mediante líneas *chip select* independientes. Dos cámaras permiten cubrir el ancho de la malla en una sola pasada y contrastar ambas capturas.
- **Módulo microSD (SPI):** guarda localmente cada captura y su marca de tiempo. Es el respaldo que permite recuperar la serie de imágenes aunque el enlace con la boya falle durante una inmersión.
- **Sensor de temperatura DS18B20 (1-Wire):** mide la temperatura del agua. Es un dato de contexto necesario para interpretar la tasa de acumulación de biofouling.
- **Acelerómetro y giroscopio MPU6050 (I2C):** registra la inclinación y el movimiento del nodo. Sirve para descartar capturas tomadas mientras el módulo oscilaba por efecto de la corriente.
- **Sensor de turbidez (analógico):** mide la claridad del agua en el momento de la captura. Una turbidez alta invalida la comparación de área libre entre capturas consecutivas.
- **Transceptor MAX485 (RS-485):** convierte el puerto serie del ESP32 al estándar RS-485 para el enlace por cable umbilical hacia la boya de superficie. RS-485 es diferencial, por lo que tolera la longitud del cable y el ruido eléctrico mucho mejor que un UART directo.

### Asignación de pines del ESP32

| Módulo | Interfaz | Pines del ESP32 |
|---|---|---|
| Bus SPI compartido | SPI | SCK **GPIO 18**, MISO **GPIO 19**, MOSI **GPIO 23** |
| Cámara Arducam Mega 1 | SPI (CS) | **GPIO 5** |
| Cámara Arducam Mega 2 | SPI (CS) | **GPIO 4** |
| Módulo microSD | SPI (CS) | **GPIO 13** |
| Sensor DS18B20 | 1-Wire | **GPIO 25** |
| MPU6050 | I2C | SDA **GPIO 21**, SCL **GPIO 22** |
| Sensor de turbidez | ADC1 | **GPIO 34** (solo entrada) |
| MAX485 | UART / RS-485 | `[PINES MAX485]` |

## ¿Por qué lo hice y cuál es su importancia?

Esta placa fue desarrollada como parte del proyecto universitario **LanternGuard**, con el propósito de reunir en un solo circuito ordenado todo lo que debe entrar en una cápsula estanca de tamaño limitado.

El diseño se divide en las siguientes secciones:

- **Módulo de control:** el microcontrolador ESP32, encargado de secuenciar la captura, leer los sensores y administrar el enlace de datos.
- **Módulo de visión:** las dos cámaras Arducam Mega sobre el bus SPI compartido, con líneas *chip select* separadas para evitar conflictos en el bus.
- **Módulo de almacenamiento:** la microSD, también sobre el mismo bus SPI, con su propia línea de selección.
- **Módulo de sensado ambiental:** DS18B20, MPU6050 y sensor de turbidez, cada uno en su interfaz correspondiente.
- **Módulo de comunicación:** el MAX485 y el conector del cable umbilical hacia la boya.

Compartir un único bus SPI entre las dos cámaras y la microSD reduce el número de pistas y libera pines del ESP32, que es la restricción real en este diseño. El ruteo en PCB, en lugar de cableado sobre protoboard, es además un requisito práctico: dentro de una cápsula sumergida no hay espacio ni tolerancia para falsos contactos.

## Imágenes del Diseño

**1. Esquemático**

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller2_Palacios_Esquematico.png" alt="Esquemático electrónico de Yoichi Palacios" width="80%">
  <br>
  <em><b>Figura 1.</b> Esquemático electrónico del nodo sumergido desarrollado por Yoichi Palacios.</em>
</p>

> **Nota de esquemático en pdf:** El esquemático en pdf se encuentra disponible en: [`SCH_Schematic1_Palacios_Yoichi.pdf`](./SCH_Schematic1_Palacios_Yoichi.pdf).

**2. Diseño de la PCB en 2D**

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller2_Palacios_PCB_2D.png" alt="Diseño PCB 2D de Yoichi Palacios" width="80%">
  <br>
  <em><b>Figura 2.</b> Distribución y ruteado de los componentes en la placa PCB.</em>
</p>

**3. Vista 3D**

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller2_Palacios_PCB_3D.png" alt="Vista 3D de la PCB de Yoichi Palacios" width="80%">
  <br>
  <em><b>Figura 3.</b> Representación tridimensional de la placa PCB diseñada.</em>
</p>

> **Nota de archivos Gerber:** El archivo comprimido con los Gerber necesarios para fabricar la placa PCB se encuentra disponible en: [`Gerber_PCB1_Palacios_Yoichi.zip`](./Gerber_PCB1_Palacios_Yoichi.zip).

---

## Checklist de entrega

- [ ] Exportar esquemático a PDF
- [ ] Exportar Gerber a .zip
- [ ] Capturas: esquemático, PCB 2D, vista 3D
- [ ] Imagen/logo en capa TopSilkLayer, no en cobre
- [ ] Agujeros de montaje (4 esquinas, $\varnothing 3.2 \text{ mm}$ para M3)
- [ ] Enlace público al proyecto EasyEDA: `[ENLACE EASYEDA]`
- [ ] Completar los pines del MAX485 en la tabla de asignación: `[PINES MAX485]`
