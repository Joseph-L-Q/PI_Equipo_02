
# Clasificación de cable, esponja y Sigma Face mediante Edge Impulse y la XIAO ESP32S3 Sense

## 1. Introducción

Tiny Machine Learning (TinyML) es ejecutar modelos de aprendizaje automático en dispositivos pequeños, como los microcontroladores. La placa hace la predicción por sí misma, sin enviar cada imagen a una computadora.

El jueves 15 de octubre de 2026 volvimos a trabajar con la placa **XIAO ESP32S3 Sense** de Seeed Studio, que trae un procesador ESP32-S3 y una cámara [1]. En el taller anterior entrenamos el modelo dentro de SenseCraft AI [2]. Esta vez lo entrenamos en **Edge Impulse**, una plataforma en línea donde se cargan los datos, se entrena la red neuronal y se exporta el modelo para distintas placas [3], [4]. Seeed Studio documenta este mismo flujo para la XIAO ESP32S3 Sense [5].

Seguimos la guía de clase [6]. Configuramos Arduino IDE (Integrated Development Environment, entorno de desarrollo integrado), tomamos nuestras propias fotos con la cámara de la placa, entrenamos el modelo en Edge Impulse y lo evaluamos con dos pruebas estadísticas. Después lo ejecutamos en la placa desde Arduino IDE y, al final, en SenseCraft AI.

Elegimos tres clases: **Cable**, **Esponja** y **Sigma Face**. Las dos primeras son objetos del laboratorio. La tercera es el rostro de Joseph haciendo el gesto "Sigma Face". Capturamos **50 imágenes por clase**, **150 en total**.

Estuvimos los cinco integrantes del equipo:

- **Joseph Lombardi Quispe** creó el proyecto en Edge Impulse y posó para la clase Sigma Face.
- **Melissa Bustos** y **María Antezana** participaron en la captura del conjunto de datos y en las pruebas.
- **Yoichi Palacios Tanaka** se encargó de la parte final: la prueba en el monitor serie de Arduino IDE y la visualización en SenseCraft AI.
- **Gabriela Santamaría** tomó la mayoría de las fotos y capturas de pantalla de este documento.

## 2. Objetivos

### 2.1. Objetivo general

Entrenar en Edge Impulse un clasificador de imágenes de tres clases (Cable, Esponja y Sigma Face) con fotos tomadas por la propia XIAO ESP32S3 Sense, evaluarlo y ejecutarlo en la placa.

### 2.2. Objetivos específicos

- Configurar Arduino IDE y la cámara de la placa con el ejemplo CameraWebServer.
- Capturar 50 imágenes por clase y etiquetarlas en Edge Impulse.
- Entrenar un modelo de 96x96 píxeles por transferencia de aprendizaje.
- Evaluarlo con dos pruebas estadísticas: Live classification y Model testing.
- Exportarlo como librería de Arduino, adaptar los pines de la cámara y leer sus predicciones en el monitor serie.
- Probarlo en SenseCraft AI y comparar los resultados con el taller anterior.

## 3. Materiales y herramientas

### 3.1. Materiales utilizados

<p align="center">
  <strong>Tabla 1.</strong> <em>Materiales y herramientas utilizados durante el laboratorio.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>N.º</th>
      <th>Material o herramienta</th>
      <th>Función</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">1</td>
      <td>XIAO ESP32S3 Sense</td>
      <td>Placa con la que capturamos las imágenes y ejecutamos el modelo.</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td>Cámara de la XIAO ESP32S3 Sense</td>
      <td>Tomó las fotos del conjunto de datos y las imágenes de prueba.</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td>Cable USB (Universal Serial Bus) tipo C a USB tipo A</td>
      <td>El cable que pidió el profesor: punta tipo C para la placa y USB para la laptop. Alimenta y programa la placa.</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td>Laptop</td>
      <td>Para programar la placa y entrar a Edge Impulse y SenseCraft AI.</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td>Arduino IDE 2.3.10</td>
      <td>Para cargar CameraWebServer y el ejemplo de inferencia, y para leer el monitor serie.</td>
    </tr>
    <tr>
      <td align="center">6</td>
      <td>Paquete de placas ESP32 de Espressif Systems</td>
      <td>Permite programar la XIAO ESP32S3 desde Arduino IDE. Usamos la versión estable recomendada por la guía.</td>
    </tr>
    <tr>
      <td align="center">7</td>
      <td>Ejemplo CameraWebServer y página <code>captura_xiao_etiqueta_personalizada.html</code></td>
      <td>Transmiten la imagen de la cámara por la red y descargan lotes de fotos etiquetadas en un archivo ZIP.</td>
    </tr>
    <tr>
      <td align="center">8</td>
      <td>Edge Impulse</td>
      <td>Para cargar los datos, diseñar el impulse, entrenar, probar y exportar el modelo.</td>
    </tr>
    <tr>
      <td align="center">9</td>
      <td>SenseCraft AI</td>
      <td>Para ejecutar el modelo en la placa y ver sus predicciones.</td>
    </tr>
    <tr>
      <td align="center">10</td>
      <td>Cable delgado, esponja y rostro con el gesto Sigma Face</td>
      <td>Lo que reconoce el modelo: una clase cada uno.</td>
    </tr>
    <tr>
      <td align="center">11</td>
      <td>GitHub</td>
      <td>Repositorio donde guardamos los archivos y esta documentación.</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia.</em>
</p>

### 3.2. Características de la placa XIAO ESP32S3 Sense

La XIAO ESP32S3 Sense tiene un procesador ESP32-S3 de doble núcleo de hasta 240 MHz, 8 MB de PSRAM (Pseudo Static Random Access Memory, memoria de acceso aleatorio pseudoestática), 8 MB de memoria Flash, Wi-Fi, Bluetooth LE (Low Energy, de bajo consumo) y un módulo de cámara [1].

Lo que más usamos fue la cámara: con ella armamos el conjunto de datos y probamos el modelo. La PSRAM también importó. La guía pide activarla porque el modelo necesita memoria extra para procesar las imágenes y, sin ella, aparecen errores por falta de memoria [6].

## 4. Desarrollo del taller

### 4.1. Lo que pidió el profesor en la pizarra

Al empezar la clase, el profesor escribió en la pizarra el material que debíamos llevar y cómo organizar la entrega (Figuras 1 y 2). El material era un cable con una punta tipo C y la otra USB. La entrega es una carpeta `TinyML-Edge Impulse` con el readme, `Data.zip` y `Modelo.zip`. El readme debía llevar imágenes de cinco partes: el proyecto, el dataset (imágenes y etiqueta), dos pruebas estadísticas, las pruebas de Edge Impulse (paso 6) y las pruebas en SenseCraft.

<p align="center">
  <img src="imagenes/01_pizarra_completa.jpg" alt="Pizarra completa con el material pedido y la estructura de la carpeta TinyML-Edge Impulse" width="800" />
  <br />
  <strong>Figura 1.</strong> <em>Pizarra del profesor con el material y la estructura de la entrega.</em>
</p>

<p align="center">
  <img src="imagenes/02_pizarra_detalle.jpg" alt="Detalle de la pizarra con la carpeta TinyML-Edge Impulse, el readme, Data.zip y Modelo.zip" width="800" />
  <br />
  <strong>Figura 2.</strong> <em>Detalle de la pizarra: carpeta, archivos y primeras secciones del readme.</em>
</p>

La Tabla 2 muestra dónde quedó cada punto de la pizarra en este documento.

<p align="center">
  <strong>Tabla 2.</strong> <em>Puntos de la pizarra y su ubicación en este documento.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Punto de la pizarra</th>
      <th>Contenido</th>
      <th>Ubicación</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Proyecto</td>
      <td>Creación del proyecto en Edge Impulse.</td>
      <td align="center">4.5</td>
    </tr>
    <tr>
      <td>Dataset (imágenes y etiqueta)</td>
      <td>Captura de las imágenes, carga y etiquetado en Edge Impulse.</td>
      <td align="center">4.4 y 4.6</td>
    </tr>
    <tr>
      <td>Pruebas estadísticas (2)</td>
      <td>Live classification y Model testing en Edge Impulse.</td>
      <td align="center">4.9</td>
    </tr>
    <tr>
      <td>Edge Impulse: Pruebas (paso 6)</td>
      <td>Modelo ejecutándose en la placa, leído en el monitor serie.</td>
      <td align="center">4.12</td>
    </tr>
    <tr>
      <td>SenseCraft: Pruebas</td>
      <td>Modelo ejecutándose en SenseCraft AI.</td>
      <td align="center">4.13</td>
    </tr>
    <tr>
      <td>Data.zip y Modelo.zip</td>
      <td>Imágenes capturadas y librería exportada.</td>
      <td align="center">7</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la pizarra del profesor (Figura 1).</em>
</p>

### 4.2. Configuración de Arduino IDE

Primero preparamos Arduino IDE para programar la XIAO ESP32S3 [6]:

1. En **Archivo >> Preferencias** agregamos esta dirección en el campo de URL (Uniform Resource Locator, dirección web) adicionales del administrador de placas:
   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_dev_index.json`
2. En **Herramientas >> Placa >> Administrador de placas** instalamos el paquete **ESP32 de Espressif Systems**, en la versión estable recomendada por la guía. Las versiones con *alpha* en el nombre no funcionan bien con la XIAO y Edge Impulse [6].
3. En **Herramientas >> Placa** elegimos **XIAO_ESP32S3** y, en **Herramientas >> Puerto**, el puerto de la placa.
4. En **Herramientas >> PSRAM** elegimos **OPI PSRAM**, la PSRAM con interfaz octal (OPI, *Octal Peripheral Interface*), para tener la memoria extra que piden la cámara y el modelo [6].

### 4.3. Cámara con CameraWebServer

Para tomar nuestras fotos usamos el ejemplo **Archivo >> Ejemplos >> ESP32 >> Camera >> CameraWebServer** [6]. En `board_config.h` activamos el modelo de cámara de nuestra placa:

```cpp
#define CAMERA_MODEL_XIAO_ESP32S3 // Has PSRAM
```

En el archivo principal pusimos el nombre y la contraseña del Wi-Fi del laboratorio. Lo demás quedó con sus valores por defecto. Esas credenciales no van en este documento.

Subimos el programa y el monitor serie mostró la dirección IP (Internet Protocol) de la cámara. Al abrirla en el navegador iniciamos la transmisión con **Start Stream**. Si a la misma dirección se le añade `/capture`, se obtiene una foto fija [6].

La guía avisa de dos errores comunes. Si Arduino IDE no reconoce el puerto, hay que desconectar la placa, revisar que esté bien armada y volver a conectarla. Si no se conecta al Wi-Fi, hay que revisar el nombre y la contraseña escritos en el código [6].

### 4.4. Captura del conjunto de datos (dataset: imágenes y etiqueta)

Con la cámara transmitiendo abrimos la página **captura_xiao_etiqueta_personalizada.html** que nos dieron en clase. En ella se escribe la IP de la cámara, la etiqueta, cuántas fotos tomar y cada cuánto tiempo. Dejamos el intervalo por defecto de la página de captura. Al terminar, la página descarga un ZIP con una carpeta que lleva el nombre de la etiqueta [6].

Melissa y María participaron en la captura junto con el resto del equipo. Hicimos una ronda por clase y salieron tres archivos: `Cable_images_50.zip`, `Esponja_images_50.zip` y `Sigma face_images_50.zip`.

- **Cable:** un cable negro delgado sobre la base de corte verde del laboratorio.
- **Esponja:** una esponja gris oscura sobre la misma base de corte.
- **Sigma Face:** el rostro de Joseph haciendo siempre el mismo gesto, con el laboratorio de fondo.

Revisamos los archivos: cada clase tiene **50 imágenes** y todas miden **320x240 píxeles**, en formato JPEG (Joint Photographic Experts Group).

<p align="center">
  <strong>Tabla 3.</strong> <em>Distribución de las imágenes capturadas.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Clase</th>
      <th>Cantidad de imágenes</th>
      <th>Resolución</th>
      <th>Distribución porcentual</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cable</td>
      <td align="center">50</td>
      <td align="center">320x240</td>
      <td align="center">33,3 %</td>
    </tr>
    <tr>
      <td>Esponja</td>
      <td align="center">50</td>
      <td align="center">320x240</td>
      <td align="center">33,3 %</td>
    </tr>
    <tr>
      <td>Sigma Face</td>
      <td align="center">50</td>
      <td align="center">320x240</td>
      <td align="center">33,3 %</td>
    </tr>
    <tr>
      <td><strong>Total</strong></td>
      <td align="center"><strong>150</strong></td>
      <td align="center">-</td>
      <td align="center"><strong>100 %</strong></td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de los archivos capturados con la XIAO ESP32S3 Sense.</em>
</p>

Antes de pasar a Edge Impulse descomprimimos los tres archivos, cerramos el monitor serie y detuvimos la transmisión, como pide la guía [6]. Las 150 imágenes están en [Data.zip](Data.zip), en las carpetas `Cable/`, `Esponja/` y `Sigma Face/`.

### 4.5. Proyecto en Edge Impulse

Joseph creó una cuenta en Edge Impulse y un proyecto nuevo [6]. El proyecto se llama **Joseph_Lombardi-project-1** y lleva una etiqueta del Grupo 2 de Proyecto Integrador (Figura 3). Todo lo que sigue en Edge Impulse (carga, entrenamiento, pruebas y exportación) lo hicimos en ese proyecto.

<p align="center">
  <img src="imagenes/03_ei_proyecto.jpg" alt="Panel principal del proyecto Joseph_Lombardi-project-1 en Edge Impulse" width="800" />
  <br />
  <strong>Figura 3.</strong> <em>Panel principal del proyecto Joseph_Lombardi-project-1 en Edge Impulse.</em>
</p>

### 4.6. Carga y etiquetado de las imágenes

Como ya teníamos las fotos, elegimos añadir datos existentes [6]. Para cada clase seleccionamos sus 50 imágenes, dejamos la partición en **Automatically split between training and test** y escribimos la etiqueta a mano en **Enter label** [6], [3].

<p align="center">
  <img src="imagenes/04_ei_carpetas_dataset.jpg" alt="Carpetas de las tres clases en la ventana de selección de archivos" width="800" />
  <br />
  <strong>Figura 4.</strong> <em>Carpetas descomprimidas de las tres clases: Sigma face_images_50, Cable_images_50 y Esponja_images_50.</em>
</p>

<p align="center">
  <img src="imagenes/05_ei_seleccion_imagenes.jpg" alt="Selección de las imágenes de la clase Sigma Face" width="800" />
  <br />
  <strong>Figura 5.</strong> <em>Selección de las imágenes de la clase Sigma Face en la ventana de carga de Edge Impulse.</em>
</p>

<p align="center">
  <img src="imagenes/06_ei_etiqueta_sigma_face.jpg" alt="Configuración de la carga con 50 archivos y la etiqueta Sigma Face" width="800" />
  <br />
  <strong>Figura 6.</strong> <em>Carga de 50 archivos con partición automática y la etiqueta Sigma Face escrita a mano.</em>
</p>

Edge Impulse muestra un registro de cada carga. En la Figura 7 termina la de Sigma Face: 50 archivos subidos y ninguno fallido.

<p align="center">
  <img src="imagenes/07_ei_carga_completa.jpg" alt="Registro de carga de la clase Sigma Face con 50 archivos subidos y 0 fallidos" width="800" />
  <br />
  <strong>Figura 7.</strong> <em>Registro de carga de la clase Sigma Face: 50 archivos subidos y 0 fallidos.</em>
</p>

Hicimos lo mismo con Cable y Esponja. Al final, **Data acquisition** mostró **150 elementos** con una partición de **79 % / 21 %**: **119 imágenes de entrenamiento** y **31 de prueba** (Figura 8).

<p align="center">
  <img src="imagenes/08_ei_dataset.jpg" alt="Sección Data acquisition con 150 elementos y partición 79 por ciento y 21 por ciento" width="800" />
  <br />
  <strong>Figura 8.</strong> <em>Conjunto de datos en Edge Impulse: 150 elementos, 119 de entrenamiento y 31 de prueba.</em>
</p>

<p align="center">
  <strong>Tabla 4.</strong> <em>Partición del conjunto de datos en Edge Impulse.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Conjunto</th>
      <th>Cantidad de imágenes</th>
      <th>Porcentaje</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Entrenamiento (Training)</td>
      <td align="center">119</td>
      <td align="center">79 %</td>
    </tr>
    <tr>
      <td>Prueba (Test)</td>
      <td align="center">31</td>
      <td align="center">21 %</td>
    </tr>
    <tr>
      <td><strong>Total</strong></td>
      <td align="center"><strong>150</strong></td>
      <td align="center"><strong>100 %</strong></td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la sección Data acquisition de Edge Impulse.</em>
</p>

Un detalle que nos sirvió más adelante: las 31 imágenes de prueba salieron de las mismas sesiones de captura. No se usan para entrenar, pero muestran los mismos objetos, con el mismo fondo y la misma luz.

### 4.7. Diseño del impulse

En Edge Impulse, un *impulse* es la cadena que recibe los datos, los procesa y se los pasa a un bloque de aprendizaje. Lo armamos en **Impulse design >> Create impulse** con tres partes [6]:

- **Image data:** valores por defecto. Las imágenes se reducen a **96x96 píxeles** antes de entrar al modelo.
- **Processing block: Image.** Normaliza las imágenes. Ahí se elige RGB (rojo, verde y azul) o escala de grises y se pulsa **Generate features** [6].
- **Learning block: Transfer Learning (Images).** El bloque *Classification* aprende patrones a partir de las características de los datos de entrada. Transfer learning, en cambio, parte de una red ya entrenada y la ajusta a nuestras imágenes. Por eso funciona con pocas fotos, como las nuestras [6], [7].

La capa de entrada recibe **27 648 características** (Figura 9). Eso es 96 x 96 x 3: trabajamos en RGB.

### 4.8. Entrenamiento por transferencia de aprendizaje

En **Impulse design >> Transfer learning** revisamos los parámetros y pulsamos **Save & train** [6]. El número de ciclos de entrenamiento se mantuvo en el valor por defecto. La Tabla 5 resume lo que se ve en la captura.

<p align="center">
  <strong>Tabla 5.</strong> <em>Parámetros de entrenamiento utilizados en Edge Impulse.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Parámetro</th>
      <th>Valor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Número de ciclos de entrenamiento</td>
      <td align="center">Valor por defecto (no lo modificamos)</td>
    </tr>
    <tr>
      <td>Tasa de aprendizaje (learning rate)</td>
      <td align="center">0,0005</td>
    </tr>
    <tr>
      <td>Procesador de entrenamiento</td>
      <td align="center">GPU (Graphics Processing Unit, unidad de procesamiento gráfico)</td>
    </tr>
    <tr>
      <td>Aumento de datos (data augmentation)</td>
      <td align="center">Desactivado</td>
    </tr>
    <tr>
      <td>Arquitectura</td>
      <td align="center">MobileNetV2 96x96 0.35 (capa final de 16 neuronas, dropout 0,1)</td>
    </tr>
    <tr>
      <td>Capa de entrada</td>
      <td align="center">27 648 características</td>
    </tr>
    <tr>
      <td>Capa de salida</td>
      <td align="center">3 clases</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la sección Transfer learning de Edge Impulse.</em>
</p>

El *dropout* apaga al azar una parte de las neuronas durante el entrenamiento. Sirve para que el modelo no memorice las imágenes.

Al terminar, Edge Impulse mostró el desempeño sobre el **conjunto de validación**, una parte de las imágenes de entrenamiento que la plataforma aparta para evaluar el modelo mientras aprende. Con la versión **Quantized (int8)**, cuyos pesos se guardan como enteros de 8 bits, obtuvimos una exactitud (*accuracy*) de **91,7 %** y una pérdida (*loss*) de **0,16** (Figura 9).

<p align="center">
  <img src="imagenes/09_ei_transfer_learning.jpg" alt="Parámetros de entrenamiento, arquitectura MobileNetV2 y desempeño de validación con 91,7 por ciento de exactitud" width="800" />
  <br />
  <strong>Figura 9.</strong> <em>Parámetros de entrenamiento, arquitectura MobileNetV2 y desempeño sobre el conjunto de validación (Quantized int8).</em>
</p>

La Tabla 6 tiene la matriz de confusión. La puntuación F1 junta dos cosas: la precisión (de las imágenes que el modelo puso en una clase, cuántas eran de esa clase) y la exhaustividad o *recall* (de las imágenes de una clase, cuántas reconoció). La curva ROC (*Receiver Operating Characteristic*, característica operativa del receptor) mide qué tan bien separa el modelo las clases. Un área de 1,00 es una separación completa en las imágenes evaluadas.

<p align="center">
  <strong>Tabla 6.</strong> <em>Matriz de confusión y métricas sobre el conjunto de validación (Quantized int8).</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Clase real \ Clase predicha</th>
      <th>Cable</th>
      <th>Esponja</th>
      <th>Sigma Face</th>
      <th>F1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cable</td>
      <td align="center"><strong>100 %</strong></td>
      <td align="center">0 %</td>
      <td align="center">0 %</td>
      <td align="center">0,94</td>
    </tr>
    <tr>
      <td>Esponja</td>
      <td align="center">12,5 %</td>
      <td align="center"><strong>87,5 %</strong></td>
      <td align="center">0 %</td>
      <td align="center">0,88</td>
    </tr>
    <tr>
      <td>Sigma Face</td>
      <td align="center">0 %</td>
      <td align="center">12,5 %</td>
      <td align="center"><strong>87,5 %</strong></td>
      <td align="center">0,93</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la sección Transfer learning de Edge Impulse. Exactitud: 91,7 %; pérdida: 0,16; área bajo la curva ROC: 1,00; precisión, exhaustividad y F1 ponderados: 0,92.</em>
</p>

En el **Data explorer** (Figura 10) cada punto es una imagen. Las tres clases forman grupos separados y solo unos pocos puntos salen marcados como incorrectos.

En la misma pantalla, Edge Impulse estima el rendimiento en el dispositivo con su compilador EON Compiler (modo *RAM optimized*): **754 ms** de inferencia, **228,0 K** de RAM (Random Access Memory, memoria de acceso aleatorio) y **546,0 K** de Flash. Ojo: esa estimación es para el dispositivo objetivo del proyecto, un **Cortex-M4F a 80 MHz** (Figura 3), no para la XIAO. Además, nuestra librería no usa el compilador EON (`EI_CLASSIFIER_COMPILED 0` en `model_metadata.h` de [Modelo.zip](Modelo.zip)). La tomamos solo como referencia.

<p align="center">
  <img src="imagenes/10_ei_data_explorer.jpg" alt="Data explorer con tres grupos de puntos y estimación de rendimiento en el dispositivo" width="600" />
  <br />
  <strong>Figura 10.</strong> <em>Data explorer de las muestras clasificadas y estimación de rendimiento para el objetivo Cortex-M4F a 80 MHz.</em>
</p>

### 4.9. Pruebas estadísticas (2)

La pizarra pedía dos pruebas estadísticas. En Edge Impulse las hicimos con **Live classification** y **Model testing**.

#### 4.9.1. Prueba estadística 1: Live classification

En **Live classification** se elige una muestra del conjunto de prueba y se pulsa **Load sample** para clasificarla sola [6], [8]. Probamos una imagen por clase con la versión **Unoptimized (float32)**, la versión sin cuantizar, con pesos en números decimales de 32 bits.

<p align="center">
  <img src="imagenes/11_ei_live_cable.jpg" alt="Live classification de la muestra Cable_039 clasificada como Cable con 1,00" width="800" />
  <br />
  <strong>Figura 11.</strong> <em>Live classification de la muestra Cable_039: Cable 1,00.</em>
</p>

<p align="center">
  <img src="imagenes/12_ei_live_esponja.jpg" alt="Live classification de la muestra Esponja_048 clasificada como Esponja con 1,00" width="800" />
  <br />
  <strong>Figura 12.</strong> <em>Live classification de la muestra Esponja_048: Esponja 1,00.</em>
</p>

<p align="center">
  <strong>Tabla 7.</strong> <em>Resultados de Live classification (Unoptimized float32).</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Muestra</th>
      <th>Etiqueta real</th>
      <th>Cable</th>
      <th>Esponja</th>
      <th>Sigma Face</th>
      <th>Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cable_039</td>
      <td align="center">Cable</td>
      <td align="center">1,00</td>
      <td align="center">0</td>
      <td align="center">0</td>
      <td align="center">Correcto</td>
    </tr>
    <tr>
      <td>Esponja_048</td>
      <td align="center">Esponja</td>
      <td align="center">0</td>
      <td align="center">1,00</td>
      <td align="center">0</td>
      <td align="center">Correcto</td>
    </tr>
    <tr>
      <td>Sigma face_040</td>
      <td align="center">Sigma Face</td>
      <td align="center">0</td>
      <td align="center">0</td>
      <td align="center">1,00</td>
      <td align="center">Correcto</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la sección Live classification de Edge Impulse. La captura de Sigma face_040 no la incluimos como figura.</em>
</p>

Las tres muestras salieron correctas, con 1,00. Pero es una imagen por clase: sirve para ver que el modelo funciona, no para medir qué tan bien funciona.

#### 4.9.2. Prueba estadística 2: Model testing

**Model testing** clasifica de una vez todo el conjunto de prueba con el botón **Classify all** [6], [9]. Con la versión **Unoptimized (float32)** obtuvimos **96,77 %** de exactitud sobre las 31 imágenes de prueba: 30 correctas.

<p align="center">
  <img src="imagenes/13_ei_model_testing.jpg" alt="Model testing con exactitud de 96,77 por ciento" width="800" />
  <br />
  <strong>Figura 13.</strong> <em>Resultado de Model testing sobre el conjunto de prueba: exactitud de 96,77 %.</em>
</p>

<p align="center">
  <img src="imagenes/14_ei_model_testing_matriz.jpg" alt="Matriz de confusión de Model testing y Feature explorer con una muestra de Esponja incorrecta" width="800" />
  <br />
  <strong>Figura 14.</strong> <em>Matriz de confusión de Model testing y Feature explorer, donde se marca una muestra de Esponja clasificada incorrectamente.</em>
</p>

<p align="center">
  <strong>Tabla 8.</strong> <em>Matriz de confusión y métricas de Model testing (Unoptimized float32).</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Clase real \ Clase predicha</th>
      <th>Cable</th>
      <th>Esponja</th>
      <th>Sigma Face</th>
      <th>Incierto</th>
      <th>F1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cable</td>
      <td align="center"><strong>100 %</strong></td>
      <td align="center">0 %</td>
      <td align="center">0 %</td>
      <td align="center">0 %</td>
      <td align="center">0,95</td>
    </tr>
    <tr>
      <td>Esponja</td>
      <td align="center">9,1 %</td>
      <td align="center"><strong>90,9 %</strong></td>
      <td align="center">0 %</td>
      <td align="center">0 %</td>
      <td align="center">0,95</td>
    </tr>
    <tr>
      <td>Sigma Face</td>
      <td align="center">0 %</td>
      <td align="center">0 %</td>
      <td align="center"><strong>100 %</strong></td>
      <td align="center">0 %</td>
      <td align="center">1,00</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la sección Model testing de Edge Impulse. Exactitud: 96,77 %; área bajo la curva ROC: 1,00; precisión, exhaustividad y F1 ponderados: 0,97.</em>
</p>

El único error fue una esponja que el modelo tomó por cable. En la validación también hubo una esponja confundida con cable. No lo tomamos como un patrón confirmado, porque las dos evaluaciones usan versiones distintas del modelo e imágenes distintas.

### 4.10. Exportación del modelo (Deployment)

En **Deployment** elegimos **Arduino library**, con TensorFlow Lite como motor de inferencia, y la versión **Quantized (int8)**. Según la guía, la versión int8 es más rápida y ocupa menos RAM y Flash, con la misma precisión reportada [6]. Al pulsar **Build**, Edge Impulse generó la librería.

El archivo descargado, `ei-joseph_lombardi-project-1-arduino-1.0.1-impulse-#1.zip`, está sin cambios en esta carpeta como [Modelo.zip](Modelo.zip). Dentro está la librería `Joseph_Lombardi-project-1_inferencing`, con las etiquetas Cable, Esponja y Sigma Face.

### 4.11. Modelo en Arduino IDE

Con la librería descargada seguimos la guía para ejecutar el modelo en la placa [6], [4]:

1. En **Programa >> Incluir Librería >> Añadir biblioteca .ZIP** elegimos el ZIP del modelo.
2. Abrimos **Archivo >> Ejemplos >> Joseph_Lombardi-project-1_inferencing >> esp32 >> esp32_camera**.
3. Borramos el bloque de pines que va desde `#define CAMERA_MODEL_ESP_EYE // Has PSRAM` hasta el primer `#endif`, porque es de otra cámara. En su lugar pegamos los pines de la XIAO ESP32S3 Sense. GPIO significa *General Purpose Input/Output* (entradas y salidas de propósito general); cada línea dice a qué terminal de la placa va un pin de la cámara [6], [10]:

```cpp
#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     10
#define SIOD_GPIO_NUM     40
#define SIOC_GPIO_NUM     39

#define Y9_GPIO_NUM       48
#define Y8_GPIO_NUM       11
#define Y7_GPIO_NUM       12
#define Y6_GPIO_NUM       14
#define Y5_GPIO_NUM       16
#define Y4_GPIO_NUM       18
#define Y3_GPIO_NUM       17
#define Y2_GPIO_NUM       15
#define VSYNC_GPIO_NUM    38
#define HREF_GPIO_NUM     47
#define PCLK_GPIO_NUM     13
```

4. También borramos el bloque `#if defined(CAMERA_MODEL_ESP_EYE)` que pone los pines 13 y 14 como `INPUT_PULLUP`, porque también es de la otra cámara [6].
5. Verificamos, subimos el código y abrimos el monitor serie.

La guía dice que, si sale un error por falta de espacio, hay que aumentar `arena_size` en el archivo de la carpeta `tflite-model` de la librería [6]. En nuestro caso no fue necesario modificar la memoria del modelo.

### 4.12. Edge Impulse: pruebas en el monitor serie

En la pizarra esta parte aparece como "Edge Impulse: Pruebas (paso 6)". Es el paso 6 de la parte "Modelo en Arduino IDE" de la guía [6]. Yoichi cargó el programa y abrió el monitor serie, y fuimos poniendo cada objeto frente a la cámara. Cada bloque del monitor muestra el tiempo de DSP (*Digital Signal Processing*, procesamiento digital de la señal), el tiempo de clasificación y la puntuación de cada clase.

<p align="center">
  <img src="imagenes/15_arduino_prueba.jpg" alt="Integrante del equipo sosteniendo la placa en su carcasa azul, conectada a la laptop con Arduino IDE abierto" width="420" />
  <br />
  <strong>Figura 15.</strong> <em>Prueba en Arduino IDE: la placa conectada a la laptop, con uno de los objetos del dataset frente a la cámara.</em>
</p>

<p align="center">
  <img src="imagenes/16_arduino_monitor_serie_equipo.jpg" alt="Integrantes del equipo durante la prueba, con el monitor serie abierto y la esponja del dataset sobre el tapete de corte" width="420" />
  <br />
  <strong>Figura 16.</strong> <em>El equipo durante la prueba, con el monitor serie abierto. Sobre el tapete de corte se ve la esponja del dataset.</em>
</p>

<p align="center">
  <img src="imagenes/17_monitor_serie_cable.jpg" alt="Monitor serie con predicciones de Cable entre 0,89 y 0,96" width="800" />
  <br />
  <strong>Figura 17.</strong> <em>Monitor serie con el cable frente a la cámara.</em>
</p>

<p align="center">
  <img src="imagenes/18_monitor_serie_esponja.jpg" alt="Monitor serie con predicciones de Esponja entre 0,83 y 0,89" width="800" />
  <br />
  <strong>Figura 18.</strong> <em>Monitor serie con la esponja frente a la cámara.</em>
</p>

<p align="center">
  <img src="imagenes/19_monitor_serie_sigma_face.jpg" alt="Monitor serie con predicciones de Sigma Face entre 0,59 y 0,82 en los bloques completos" width="800" />
  <br />
  <strong>Figura 19.</strong> <em>Monitor serie con el gesto Sigma Face frente a la cámara.</em>
</p>

<p align="center">
  <strong>Tabla 9.</strong> <em>Puntuación de la clase correcta en el monitor serie.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Objeto presentado</th>
      <th>Bloques completos</th>
      <th>Puntuación mínima</th>
      <th>Puntuación máxima</th>
      <th>Promedio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cable</td>
      <td align="center">7</td>
      <td align="center">0,89062</td>
      <td align="center">0,95703</td>
      <td align="center">0,9185</td>
    </tr>
    <tr>
      <td>Esponja</td>
      <td align="center">7</td>
      <td align="center">0,83203</td>
      <td align="center">0,89453</td>
      <td align="center">0,8622</td>
    </tr>
    <tr>
      <td>Sigma Face</td>
      <td align="center">7</td>
      <td align="center">0,58594</td>
      <td align="center">0,81641</td>
      <td align="center">0,7277</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de los bloques completos visibles en las Figuras 17, 18 y 19.</em>
</p>

**Lo que observamos**

En todos los bloques, la clase con mayor puntuación fue la del objeto que teníamos delante. En todas las cabeceras visibles el monitor marcó **4 ms de DSP** y **182 ms de clasificación**.

Sigma Face fue la clase más baja y la que más subía y bajaba. Arriba en la Figura 19 incluso aparece un 0,53516, de un bloque que no se ve completo.

### 4.13. SenseCraft: pruebas

Yoichi se encargó de esta parte. Volvimos al **Dashboard** de Edge Impulse y descargamos el bloque **Transfer learning model** en formato **TensorFlow Lite (int8 quantized)** [6]. En **SenseCraft AI >> Espacio de trabajo >> Subir modelo** le pusimos un nombre, elegimos el archivo y agregamos los objetos en el mismo orden de las etiquetas del modelo: Cable, Esponja y Sigma Face [6], [11].

Con el modelo cargado, la **Vista previa** muestra la imagen de la cámara con una barra de confianza por clase, y el **Registro del dispositivo** muestra los tiempos de cada inferencia.

<p align="center">
  <img src="imagenes/20_sensecraft_prueba_cable.jpg" alt="Prueba del cable en SenseCraft AI con la XIAO ESP32S3 Sense apuntando a la base de corte" width="420" />
  <br />
  <strong>Figura 20.</strong> <em>Prueba de la clase Cable en SenseCraft AI.</em>
</p>

<p align="center">
  <img src="imagenes/21_sensecraft_prueba_esponja.jpg" alt="Prueba de la esponja en SenseCraft AI" width="420" />
  <br />
  <strong>Figura 21.</strong> <em>Prueba de la clase Esponja en SenseCraft AI.</em>
</p>

<p align="center">
  <img src="imagenes/22_sensecraft_prueba_sigma_face.jpg" alt="Prueba del gesto Sigma Face en SenseCraft AI con la placa orientada hacia el rostro de un integrante" width="420" />
  <br />
  <strong>Figura 22.</strong> <em>Prueba de la clase Sigma Face, con la placa orientada hacia el rostro de uno de los integrantes.</em>
</p>

<p align="center">
  <img src="imagenes/23_sensecraft_cable.jpg" alt="Vista previa de SenseCraft AI con Cable al 90 por ciento" width="800" />
  <br />
  <strong>Figura 23.</strong> <em>Vista previa de SenseCraft AI con el cable: Cable 90 %.</em>
</p>

<p align="center">
  <img src="imagenes/24_sensecraft_esponja.jpg" alt="Vista previa de SenseCraft AI con Esponja al 83 por ciento" width="800" />
  <br />
  <strong>Figura 24.</strong> <em>Vista previa de SenseCraft AI con la esponja: Esponja 83 %.</em>
</p>

<p align="center">
  <img src="imagenes/25_sensecraft_sigma_face.jpg" alt="Vista previa de SenseCraft AI con Sigma Face al 79 por ciento" width="800" />
  <br />
  <strong>Figura 25.</strong> <em>Vista previa de SenseCraft AI con el gesto Sigma Face: Sigma Face 79 %.</em>
</p>

**Lo que observamos**

En las tres capturas la clase correcta tuvo la mayor confianza y las otras dos quedaron en 0 %.

## 5. Resultados y análisis

### 5.1. Conjunto de datos

Tuvimos **150 imágenes**, **50 por clase**, de **320x240 píxeles**. Edge Impulse separó **119 para entrenamiento y 31 para prueba** y las redujo a **96x96 píxeles** en RGB.

Las clases están equilibradas en cantidad, pero cada una es un solo objeto (un cable, una esponja y un rostro) fotografiado sobre el mismo fondo y desde pocos ángulos. Eso no garantiza que el modelo reconozca otros cables, otras esponjas u otros rostros.

### 5.2. Pruebas estadísticas en Edge Impulse

<p align="center">
  <strong>Tabla 10.</strong> <em>Resumen de las evaluaciones realizadas en Edge Impulse.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Evaluación</th>
      <th>Versión del modelo</th>
      <th>Datos evaluados</th>
      <th>Exactitud</th>
      <th>F1 ponderado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Entrenamiento (validación)</td>
      <td align="center">Quantized (int8)</td>
      <td align="center">Conjunto de validación</td>
      <td align="center">91,7 %</td>
      <td align="center">0,92</td>
    </tr>
    <tr>
      <td>Live classification</td>
      <td align="center">Unoptimized (float32)</td>
      <td align="center">3 muestras, una por clase</td>
      <td align="center">3 de 3 correctas</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Model testing</td>
      <td align="center">Unoptimized (float32)</td>
      <td align="center">31 imágenes de prueba</td>
      <td align="center">96,77 %</td>
      <td align="center">0,97</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de las Figuras 9, 11 a 14 y la Tabla 7.</em>
</p>

Hay que leer estas cifras con dos cuidados. La validación usó el modelo int8 y las dos pruebas el float32, así que no comparan exactamente el mismo modelo. Y las imágenes de prueba vienen de las mismas sesiones que las de entrenamiento: el 96,77 % dice que el modelo distingue bien estas tres escenas, no que funcione igual con objetos o fondos nuevos.

### 5.3. Confianza por clase en el dispositivo

<p align="center">
  <strong>Tabla 11.</strong> <em>Confianza de la clase correcta en el dispositivo.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Clase</th>
      <th>SenseCraft AI</th>
      <th>Monitor serie (mínimo a máximo)</th>
      <th>Monitor serie (promedio)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cable</td>
      <td align="center">90 %</td>
      <td align="center">89,1 % a 95,7 %</td>
      <td align="center">91,9 %</td>
    </tr>
    <tr>
      <td>Esponja</td>
      <td align="center">83 %</td>
      <td align="center">83,2 % a 89,5 %</td>
      <td align="center">86,2 %</td>
    </tr>
    <tr>
      <td>Sigma Face</td>
      <td align="center">79 %</td>
      <td align="center">58,6 % a 81,6 %</td>
      <td align="center">72,8 %</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de las Figuras 17 a 19 y 23 a 25. Los valores del monitor serie corresponden a los 7 bloques completos de la Tabla 9.</em>
</p>

En las dos herramientas el orden fue el mismo: **Cable** primero, luego **Esponja** y al final **Sigma Face**. En SenseCraft AI cada valor es una sola captura, no un promedio.

En la placa la confianza fue menor que el 1,00 de Live classification. Tiene sentido: en la placa el modelo ve imágenes nuevas tomadas en vivo y corre la versión int8, mientras que Live classification usó imágenes guardadas y la versión float32. No hicimos pruebas para separar cuánto pesa cada cosa.

Sigma Face fue la clase con menos confianza y más variación. Un rostro cambia de posición, distancia y luz mucho más que un objeto quieto sobre la mesa, y su fondo es el laboratorio, mientras que el cable y la esponja comparten la base de corte. Tampoco comprobamos cuál de estos factores influyó más.

### 5.4. Tiempos de preprocesamiento e inferencia

<p align="center">
  <strong>Tabla 12.</strong> <em>Tiempos registrados y estimados.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Fuente</th>
      <th>Preprocesamiento</th>
      <th>Inferencia</th>
      <th>Postprocesamiento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SenseCraft AI, Registro del dispositivo (16 registros)</td>
      <td align="center">87 a 97 ms (promedio 94,9 ms)</td>
      <td align="center">188 a 192 ms (promedio 189,7 ms)</td>
      <td align="center">0 ms</td>
    </tr>
    <tr>
      <td>Arduino IDE, monitor serie</td>
      <td align="center">DSP: 4 ms</td>
      <td align="center">Clasificación: 182 ms</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Edge Impulse, estimación para Cortex-M4F a 80 MHz</td>
      <td align="center">-</td>
      <td align="center">754 ms</td>
      <td align="center">-</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de las Figuras 10, 17 a 19 y 23 a 25.</em>
</p>

La inferencia tardó cerca de **190 ms** en SenseCraft AI y **182 ms** en el monitor serie: valores parecidos. El preprocesamiento, en cambio, fue muy distinto (4 ms frente a unos 95 ms). Son programas diferentes y seguramente cada uno mide etapas distintas, así que no los comparamos directamente.

Los tiempos reales en la placa fueron mucho menores que los 754 ms que estimó Edge Impulse. Esa estimación es para un Cortex-M4F a 80 MHz con el compilador EON; el ESP32-S3 de la XIAO llega a 240 MHz [1].

### 5.5. Comparación con el taller anterior

En el taller anterior entrenamos en SenseCraft AI un modelo de dos clases, Lentes y Celular [2].

<p align="center">
  <strong>Tabla 13.</strong> <em>Comparación entre el taller de SenseCraft AI y el taller de Edge Impulse.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Aspecto</th>
      <th>Taller anterior (SenseCraft AI)</th>
      <th>Este taller (Edge Impulse)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Clases</td>
      <td align="center">2 (Lentes y Celular)</td>
      <td align="center">3 (Cable, Esponja y Sigma Face)</td>
    </tr>
    <tr>
      <td>Imágenes</td>
      <td align="center">162 (81 por clase)</td>
      <td align="center">150 (50 por clase)</td>
    </tr>
    <tr>
      <td>Plataforma de entrenamiento</td>
      <td align="center">SenseCraft AI</td>
      <td align="center">Edge Impulse, transferencia de aprendizaje con MobileNetV2</td>
    </tr>
    <tr>
      <td>Evaluación en la plataforma</td>
      <td align="center">No registrada</td>
      <td align="center">Validación 91,7 % y Model testing 96,77 %</td>
    </tr>
    <tr>
      <td>Ejecución en la placa</td>
      <td align="center">SenseCraft AI</td>
      <td align="center">Arduino IDE (monitor serie) y SenseCraft AI</td>
    </tr>
    <tr>
      <td>Confianza en SenseCraft AI</td>
      <td align="center">Lentes: 100 % en 3 pruebas. Celular: 88 %, 77 % y 90 %</td>
      <td align="center">Cable: 90 %. Esponja: 83 %. Sigma Face: 79 % (una captura por clase)</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la documentación del taller anterior [2] y de los resultados de este taller.</em>
</p>

Con una clase más y menos fotos por clase, el modelo acertó las tres clases en la placa. Sus confianzas en SenseCraft AI (79 % a 90 %) se parecen a las del celular en el taller anterior (77 % a 90 %) y quedan por debajo del 100 % de los lentes. Como esta vez tomamos una sola captura por clase y la vez anterior tres, la comparación es solo orientativa.

Lo que más cambió fue la forma de evaluar. Edge Impulse nos dio un conjunto de prueba y una matriz de confusión, algo que en el taller anterior no registramos. Y pudimos correr el mismo modelo de dos maneras: como librería de Arduino y en SenseCraft AI.

### 5.6. Limitaciones y mejoras

- **Un solo objeto por clase.** Un cable, una esponja y un rostro. El modelo pudo aprender esos objetos en particular, no "cable" o "esponja" en general.
- **Mismo fondo y pocos ángulos.** Un cambio de fondo, distancia o luz podría cambiar la clasificación.
- **Prueba sin imágenes realmente nuevas.** Las 31 imágenes de prueba salieron de las mismas sesiones que las de entrenamiento.
- **Pocas pruebas en la placa.** Una captura por clase en SenseCraft AI y siete bloques por clase en el monitor serie.
- **Sin aumento de datos.** Entrenamos con *data augmentation* desactivado.

Para la próxima: fotografiar varios objetos por clase con fondos y luces distintos, capturar el conjunto de prueba en otra sesión, activar el aumento de datos y repetir las pruebas en la placa para sacar promedios.

## 6. Conclusiones

1. Con 150 fotos propias y transferencia de aprendizaje, el modelo acertó 30 de las 31 imágenes de Model testing (96,77 %). El único error fue una esponja tomada por cable.

2. En la placa el modelo reconoció las tres clases, tanto en el monitor serie como en SenseCraft AI. El orden de confianza se repitió en las dos herramientas: Cable (90 % en SenseCraft AI), Esponja (83 %) y Sigma Face (79 %).

3. Sigma Face fue la clase más difícil. En el monitor serie bajó hasta 0,59 en los bloques completos. Un rostro se mueve y cambia de fondo mucho más que un objeto sobre la mesa.

4. Aprendimos a no mezclar cifras. La validación usó el modelo int8 y las pruebas el float32, y los 754 ms que estimó Edge Impulse eran para otro microcontrolador: en la XIAO medimos unos 190 ms.

5. Un 96,77 % con imágenes de las mismas sesiones no asegura que el modelo funcione con otros cables, esponjas o rostros. Para medir eso necesitamos datos más variados y un conjunto de prueba capturado aparte.

## 7. Archivos del proyecto

- **[Conjunto de datos (Data.zip)](Data.zip):** las 150 imágenes capturadas con la XIAO ESP32S3 Sense, de 320x240 píxeles, en las carpetas `Cable/`, `Esponja/` y `Sigma Face/` (50 por clase).

- **[Modelo (Modelo.zip)](Modelo.zip):** librería de Arduino exportada desde Edge Impulse (`Joseph_Lombardi-project-1_inferencing`, versión 1.0.1, modelo cuantizado int8). Se instala en Arduino IDE con **Programa >> Incluir Librería >> Añadir biblioteca .ZIP**.

- **[Imágenes del taller](imagenes/):** fotos de la pizarra y del laboratorio, y capturas de pantalla usadas como figuras en este documento.

## 8. Referencias bibliográficas

<a id="ref1"></a>

[1] Seeed Studio, "Getting Started with Seeed Studio XIAO ESP32-S3 Series," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/. [Accedido: 16-oct-2026].

<a id="ref2"></a>

[2] Equipo 02, "Clasificación de lentes y celulares mediante SenseCraft AI y activación de LED con GPIO," repositorio PI_Equipo_02, Proyecto Integrador, Universidad Peruana Cayetano Heredia, 2026. Disponible en: [../TinyML-Sensecraft/readme2.md](../TinyML-Sensecraft/readme2.md).

<a id="ref3"></a>

[3] Edge Impulse, "Data acquisition," *Edge Impulse Documentation*. [En línea]. Disponible en: https://docs.edgeimpulse.com/studio/projects/data-acquisition. [Accedido: 16-oct-2026].

<a id="ref4"></a>

[4] Edge Impulse, "Run Arduino library (IDE 2.0)," *Edge Impulse Documentation*. [En línea]. Disponible en: https://docs.edgeimpulse.com/hardware/deployments/run-arduino-2-0. [Accedido: 16-oct-2026].

<a id="ref5"></a>

[5] Seeed Studio, "XIAO ESP32S3-Sense Image Classification," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/tinyml_course_Image_classification_project/. [Accedido: 16-oct-2026].

<a id="ref6"></a>

[6] Universidad Peruana Cayetano Heredia, *TinyML con XIAO ESP32S3 Sense: Laboratorio con Edge Impulse*, material de clase, Lima, Perú, 2026.

<a id="ref7"></a>

[7] Edge Impulse, "Transfer learning (images)," *Edge Impulse Documentation*. [En línea]. Disponible en: https://docs.edgeimpulse.com/studio/projects/learning-blocks/blocks/transfer-learning-images. [Accedido: 16-oct-2026].

<a id="ref8"></a>

[8] Edge Impulse, "Live classification," *Edge Impulse Documentation*. [En línea]. Disponible en: https://docs.edgeimpulse.com/studio/projects/live-classification. [Accedido: 16-oct-2026].

<a id="ref9"></a>

[9] Edge Impulse, "Model testing," *Edge Impulse Documentation*. [En línea]. Disponible en: https://docs.edgeimpulse.com/studio/projects/model-testing. [Accedido: 16-oct-2026].

<a id="ref10"></a>

[10] Seeed Studio, "Camera Usage in Seeed Studio XIAO ESP32S3 Sense," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/. [Accedido: 16-oct-2026].

<a id="ref11"></a>

[11] Seeed Studio, "Using a model for XIAO ESP32S3 Sense," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/sensecraft-ai/tutorials/sensecraft-ai-pretrained-models-for-xiao/. [Accedido: 16-oct-2026].
