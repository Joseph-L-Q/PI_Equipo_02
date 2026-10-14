# README 2 | Creación de un modelo de clasificación de lentes y celulares con SenseCraft AI

**Taller:** TinyML con XIAO ESP32S3 Sense — Entrenamiento de un modelo de clasificación de imágenes y activación de un LED mediante GPIO  
**Plataforma:** SenseCraft AI  
**Dispositivo:** XIAO ESP32S3 Sense  
**Participantes de las pruebas:** María Antezana, Melisa Bustos y Gabriela Santamaría

## 1. Introducción

Tiny Machine Learning (TinyML) permite utilizar modelos de aprendizaje automático en dispositivos pequeños, como los microcontroladores. Durante el laboratorio trabajamos con la placa **XIAO ESP32S3 Sense**, que incorpora una cámara y dispone de conexiones de entrada y salida para interactuar con componentes electrónicos [1](#ref1), [2](#ref2).

En esta segunda actividad utilizamos **SenseCraft AI** para crear un modelo propio de clasificación de imágenes. A diferencia del primer README, en el que probamos un modelo ya disponible, esta vez recopilamos nuestros datos, entrenamos el modelo y evaluamos su funcionamiento. La plataforma permite desarrollar este tipo de modelos a partir de imágenes organizadas por categorías [3](#ref3).

Elegimos **lentes** y **celulares**, dos objetos cotidianos que podíamos colocar frente a la cámara. Después del entrenamiento, realizamos pruebas de reconocimiento y configuramos una salida **GPIO** para relacionar el resultado de la clasificación con el encendido de un LED. Las evidencias de la actividad corresponden a las pruebas realizadas por María Antezana, Melisa Bustos y Gabriela Santamaría.

## 2. Objetivos

### 2.1. Objetivo general

Crear y probar un modelo de inteligencia artificial capaz de diferenciar lentes y celulares mediante SenseCraft AI y la placa XIAO ESP32S3 Sense, y comprobar la activación de un LED a través de GPIO.

### 2.2. Objetivos específicos

- Recopilar y organizar imágenes de lentes y celulares para entrenar el modelo.
- Entrenar un modelo de clasificación con las dos categorías seleccionadas.
- Realizar pruebas con ambos objetos y registrar las clasificaciones obtenidas.
- Interpretar los porcentajes de confianza mostrados por SenseCraft AI.
- Configurar una condición de salida GPIO y verificar el encendido del LED.
- Documentar el procedimiento, las evidencias y los archivos del proyecto en GitHub.

## 3. Materiales y herramientas

La XIAO ESP32S3 Sense cuenta con un microcontrolador ESP32-S3, una cámara y opciones de conexión que permiten realizar prácticas de reconocimiento de imágenes [2](#ref2). Para esta actividad empleamos los siguientes recursos:

<p align="center"><strong>Tabla 1.</strong> Materiales y herramientas utilizados durante el laboratorio.</p>

<div align="center">
<table>
  <thead>
    <tr><th>Material o herramienta</th><th>Uso en la práctica</th></tr>
  </thead>
  <tbody>
    <tr><td>XIAO ESP32S3 Sense</td><td>Dispositivo utilizado para realizar las pruebas del modelo y controlar la salida GPIO.</td></tr>
    <tr><td>Cámara del dispositivo</td><td>Captura de imágenes de lentes y celulares.</td></tr>
    <tr><td>Computadora y cable USB</td><td>Conexión del dispositivo y acceso a la plataforma.</td></tr>
    <tr><td>SenseCraft AI</td><td>Creación, entrenamiento, vista previa y configuración del modelo.</td></tr>
    <tr><td>Lentes y celulares</td><td>Objetos elegidos para las dos categorías de clasificación.</td></tr>
    <tr><td>LED utilizado durante la práctica</td><td>Indicador visual de la respuesta configurada mediante GPIO.</td></tr>
    <tr><td>GitHub</td><td>Almacenamiento y presentación del conjunto de datos, el modelo y las evidencias.</td></tr>
  </tbody>
</table>
</div>

<p align="center"><em>Fuente: Elaboración propia a partir de los materiales utilizados en el taller.</em></p>

## 4. Desarrollo del taller

### 4.1. Creación del modelo y selección de las categorías

Primero ingresamos a SenseCraft AI y elegimos la opción de crear un modelo de **clasificación de imágenes**. Este tipo de modelo analiza una imagen y le asigna una categoría según lo aprendido durante el entrenamiento [3](#ref3).

Creamos dos categorías: **Lentes** y **Celular**. Esta separación fue importante porque permitió indicar a qué objeto correspondía cada imagen antes de iniciar el entrenamiento. Nuestro propósito no era identificar la marca de los productos, sino distinguir entre los dos tipos de objetos seleccionados.

### 4.2. Captura y organización de las imágenes

Después de establecer las categorías, utilizamos la cámara para registrar imágenes de los objetos. Reunimos **81 fotografías de lentes** y **81 fotografías de celulares**, para un total de **162 imágenes**.

<p align="center"><strong>Tabla 2.</strong> Distribución de las imágenes utilizadas para el entrenamiento.</p>

<div align="center">
<table>
  <thead><tr><th>Categoría</th><th>Cantidad de imágenes</th></tr></thead>
  <tbody>
    <tr><td>Lentes</td><td align="center">81</td></tr>
    <tr><td>Celular</td><td align="center">81</td></tr>
    <tr><td><strong>Total</strong></td><td align="center"><strong>162</strong></td></tr>
  </tbody>
</table>
</div>

<p align="center"><em>Fuente: Registro de imágenes realizado por el equipo durante el laboratorio.</em></p>

Mantuvimos la misma cantidad de imágenes en ambas categorías para que el conjunto de datos estuviera equilibrado en número. La documentación de SenseCraft AI también recomienda incluir imágenes variadas en cuanto a ángulos, iluminación y fondos, ya que esto puede ayudar al modelo a reconocer los objetos en condiciones distintas a las del entrenamiento [3](#ref3).

Durante la recopilación participaron las tres integrantes del equipo. A continuación, se presentan las evidencias de esta etapa en el orden acordado.

#### 4.2.1. María Antezana

María participó en la captura de imágenes de los objetos seleccionados, utilizando la cámara del dispositivo y la computadora para registrar los datos de entrenamiento.

<p align="center"><img width="900" alt="María Antezana durante la captura de imágenes" src="URL_IMAGEN_01" /></p>

<p align="center"><strong>Figura 1.</strong> <em>María Antezana participando en la recopilación de imágenes para el entrenamiento del modelo.</em></p>

#### 4.2.2. Melisa Bustos

Melisa colaboró en el mismo proceso, colocando los objetos frente a la cámara y registrando imágenes para las categorías definidas.

<p align="center"><img width="900" alt="Melisa Bustos durante la captura de imágenes" src="URL_IMAGEN_02" /></p>

<p align="center"><strong>Figura 2.</strong> <em>Melisa Bustos realizando la captura de imágenes con la XIAO ESP32S3 Sense.</em></p>

#### 4.2.3. Gabriela Santamaría

Gabriela también participó en la captura de imágenes, contribuyendo a completar el conjunto de datos que utilizaríamos en el entrenamiento.

<p align="center"><img width="900" alt="Gabriela Santamaría durante la captura de imágenes" src="URL_IMAGEN_03" /></p>

<p align="center"><strong>Figura 3.</strong> <em>Gabriela Santamaría participando en el registro de imágenes para las categorías del modelo.</em></p>

### 4.3. Descarga del conjunto de datos y entrenamiento

Una vez terminada la recopilación, descargamos las imágenes en un archivo comprimido **`.zip`** y lo incorporamos al repositorio del grupo. Este archivo permite conservar los datos con los que trabajamos y deja un registro de las dos categorías utilizadas.

Luego iniciamos el entrenamiento desde SenseCraft AI. En esta etapa, la plataforma procesó las imágenes clasificadas para generar un modelo que pudiera diferenciar lentes y celulares. De acuerdo con la guía oficial, el entrenamiento comienza después de recopilar y organizar las imágenes de las clases que se desean reconocer [3](#ref3).

Al finalizar, continuamos con la preparación del modelo para utilizarlo con la XIAO ESP32S3 Sense y realizar las pruebas mediante su cámara. La plataforma permite desplegar el modelo entrenado en un dispositivo compatible y comprobar las predicciones desde la vista previa [3](#ref3).

### 4.4. Pruebas de reconocimiento

Para evaluar el modelo, colocamos nuevamente los objetos frente a la cámara y observamos la clasificación presentada en SenseCraft AI. Realizamos las pruebas con ambas categorías y guardamos capturas de los resultados.

#### 4.4.1. Prueba con lentes

Primero presentamos los **lentes** frente a la cámara para observar si el modelo les asignaba la categoría correspondiente. Durante la prueba, verificamos el resultado mostrado en pantalla y registramos la evidencia fotográfica.

<p align="center"><img width="900" alt="Prueba física de reconocimiento de lentes" src="URL_IMAGEN_04" /></p>

<p align="center"><strong>Figura 4.</strong> <em>Prueba de reconocimiento de lentes mediante la cámara de la XIAO ESP32S3 Sense.</em></p>

La captura de SenseCraft AI permite observar qué categoría indicó el modelo y con qué porcentaje de confianza respondió a esa imagen.

<p align="center"><img width="1600" alt="Resultado del reconocimiento de lentes en SenseCraft AI" src="URL_IMAGEN_05" /></p>

<p align="center"><strong>Figura 5.</strong> <em>Resultado de la clasificación de lentes y porcentaje de confianza mostrado en SenseCraft AI.</em></p>

#### 4.4.2. Prueba con celulares

Después repetimos el procedimiento con un **celular**, manteniendo el modelo entrenado con las dos categorías. Buscamos comprobar si podía distinguir este objeto de los lentes utilizando la misma cámara.

<p align="center"><img width="900" alt="Prueba física de reconocimiento de celular" src="URL_IMAGEN_06" /></p>

<p align="center"><strong>Figura 6.</strong> <em>Prueba de reconocimiento de un celular utilizando el modelo entrenado.</em></p>

También registramos la pantalla con el resultado del modelo para compararlo con la prueba anterior.

<p align="center"><img width="1600" alt="Resultado del reconocimiento de celular en SenseCraft AI" src="URL_IMAGEN_07" /></p>

<p align="center"><strong>Figura 7.</strong> <em>Resultado de la clasificación de celular y porcentaje de confianza mostrado en SenseCraft AI.</em></p>

### 4.5. Lectura de los porcentajes de confianza

En la vista previa, SenseCraft AI muestra las predicciones del modelo y permite revisar sus puntuaciones de confianza. También dispone de ajustes para definir qué nivel de confianza se requiere antes de considerar una detección como válida [4](#ref4).

Es importante diferenciar **la confianza obtenida** del **umbral configurado**: la primera es un resultado que calcula el modelo al analizar una imagen; el segundo es un valor que establecemos para decidir cuándo aceptar o utilizar ese resultado. Por ello, un porcentaje mostrado durante una prueba no demuestra, por sí solo, la precisión general del modelo.

<p align="center"><strong>Tabla 3.</strong> Registro de los resultados observados en SenseCraft AI.</p>

<div align="center">
<table>
  <thead><tr><th>Objeto presentado</th><th>Categoría esperada</th><th>Confianza mostrada</th></tr></thead>
  <tbody>
    <tr><td>Lentes</td><td>Lentes</td><td align="center"><strong>[COMPLETAR SEGÚN CAPTURA]</strong></td></tr>
    <tr><td>Celular</td><td>Celular</td><td align="center"><strong>[COMPLETAR SEGÚN CAPTURA]</strong></td></tr>
  </tbody>
</table>
</div>

<p align="center"><em>Fuente: Elaboración propia a partir de las capturas de resultados de las figuras 5 y 7.</em></p>

Estos campos se completarán con los porcentajes exactos de las capturas. No se incluyen valores estimados porque el propósito del registro es presentar lo observado durante la práctica.

### 4.6. Configuración de la salida GPIO

Luego de probar el reconocimiento, ingresamos a la opción **Output → GPIO** de SenseCraft AI. Esta función permite establecer condiciones para que una salida de la placa cambie de estado según el resultado del modelo. La guía de Seeed Studio describe opciones como *Object*, *Condition*, *Confidence*, *GPIO*, *Default Status* y *Active Status* [5](#ref5).

En nuestra actividad configuramos el sistema para observar el **encendido del LED** cuando se cumpliera la condición de reconocimiento. Durante la práctica registramos dos valores de referencia: **80 %** y **60 %**.

<p align="center"><strong>Tabla 4.</strong> Registro de la configuración utilizada durante la prueba GPIO.</p>

<div align="center">
<table>
  <thead><tr><th>Elemento</th><th>Configuración o función</th></tr></thead>
  <tbody>
    <tr><td>Object</td><td><strong>[CONFIRMAR EN LA CAPTURA: Lentes o Celular]</strong>. Define qué categoría activa la condición.</td></tr>
    <tr><td>Valor de reconocimiento</td><td><strong>80 %</strong>. Valor anotado durante la práctica; <strong>[CONFIRMAR NOMBRE EXACTO DEL AJUSTE]</strong>.</td></tr>
    <tr><td>Confidence (condición GPIO)</td><td><strong>60 %</strong>, de acuerdo con el registro del equipo; verificar su ubicación en la captura.</td></tr>
    <tr><td>Condition</td><td><strong>[CONFIRMAR: Greater than / mayor que]</strong>. Establece la comparación que activa la salida.</td></tr>
    <tr><td>GPIO</td><td>Salida utilizada para controlar el LED durante la prueba.</td></tr>
    <tr><td>Default Status / Active Status</td><td>Estados definidos para mantener el LED apagado o encenderlo según la condición.</td></tr>
  </tbody>
</table>
</div>

<p align="center"><em>Fuente: Registro del equipo y campos de configuración descritos en la documentación de Seeed Studio [5](#ref5).</em></p>

El **80 %** y el **60 %** no deben confundirse con los porcentajes obtenidos en las pruebas de lentes y celulares. Son valores que anotamos durante la configuración. Antes de cerrar el registro, debemos comprobar en la captura a qué campo de la plataforma corresponde cada uno, porque los ajustes de reconocimiento y los de activación GPIO pueden ser independientes [4](#ref4), [5](#ref5).

El propósito de la configuración fue sencillo: **cuando el modelo reconociera la categoría seleccionada y se cumpliera la condición establecida, el LED debía encenderse**. De esta forma, el resultado de la clasificación se utilizó para producir una respuesta visible en el dispositivo.

### 4.7. Verificación del encendido del LED

Finalmente, realizamos una prueba con la salida GPIO configurada. Para ello, utilizamos nuevamente los objetos de la práctica y observamos la respuesta del dispositivo. Durante esta etapa registramos el **LED encendido**, por lo que tomamos dos fotografías desde distintas distancias.

#### 4.7.1. Vista general de la prueba

La primera fotografía muestra a las integrantes del equipo durante la comprobación del funcionamiento de la placa. Esta evidencia permite observar la disposición del dispositivo y la participación del grupo.

<p align="center"><img width="900" alt="María Antezana, Melisa Bustos y Gabriela Santamaría durante la prueba GPIO" src="URL_IMAGEN_08" /></p>

<p align="center"><strong>Figura 8.</strong> <em>María Antezana, Melisa Bustos y Gabriela Santamaría durante la prueba de reconocimiento y activación del LED.</em></p>

#### 4.7.2. Detalle del LED encendido

En la segunda fotografía acercamos la cámara al dispositivo para que la luz encendida pudiera apreciarse con mayor claridad. Esta imagen constituye la evidencia directa de la respuesta física obtenida durante el laboratorio.

<p align="center"><img width="900" alt="Primer plano del LED encendido en el dispositivo" src="URL_IMAGEN_09" /></p>

<p align="center"><strong>Figura 9.</strong> <em>Primer plano del LED encendido durante la prueba de la salida GPIO.</em></p>

## 5. Resultados y análisis

### 5.1. Creación y evaluación del modelo

El principal resultado de la primera etapa fue el desarrollo de un modelo propio con **dos categorías y 162 imágenes de entrenamiento**. A diferencia de utilizar un modelo ya preparado, esta actividad nos permitió intervenir en la recopilación de datos y en el entrenamiento.

Las pruebas con lentes y celulares permitieron observar las predicciones del modelo en la vista previa. Los porcentajes registrados en las figuras 5 y 7 servirán para describir con precisión cómo respondió ante cada objeto, sin atribuirle una exactitud general a partir de solo dos capturas.

### 5.2. Respuesta de la salida GPIO

En la segunda etapa comprobamos que el reconocimiento podía relacionarse con una acción física. El encendido del LED, registrado en las figuras 8 y 9, mostró la respuesta del dispositivo durante la prueba con la configuración realizada.

Este comportamiento coincide con el uso de GPIO que describe Seeed Studio: cambiar el estado de una salida cuando el modelo cumple una condición definida en la plataforma [5](#ref5).

### 5.3. Alcance y aspectos por mejorar

Aunque el modelo fue entrenado con la misma cantidad de imágenes por categoría, las pruebas documentadas no permiten asegurar que vaya a reconocer correctamente cualquier lente o celular. Su respuesta podría cambiar al utilizar objetos distintos o modificar las condiciones de luz, distancia, orientación y fondo. La documentación oficial recomienda contar con imágenes variadas para mejorar la capacidad de reconocer nuevos ejemplos [3](#ref3).

Para una evaluación posterior sería útil ampliar la variedad de objetos, probar imágenes que no se utilizaron para entrenar y registrar tanto los aciertos como las clasificaciones incorrectas. Asimismo, convendría revisar la respuesta del LED cuando la condición de activación no se cumpla, además de documentar su encendido.

## 6. Conclusiones

1. **Creamos un modelo de clasificación propio** en SenseCraft AI utilizando 81 imágenes de lentes y 81 de celulares. El proceso nos permitió conocer las etapas de preparación de datos, entrenamiento y prueba.
2. **Realizamos pruebas con ambas categorías** y registramos las predicciones mostradas por la plataforma. Esto nos ayudó a distinguir entre los resultados de confianza del modelo y los umbrales que se configuran para utilizar dichos resultados.
3. **Comprobamos el encendido del LED mediante GPIO**, relacionando el reconocimiento de imágenes con una respuesta física de la XIAO ESP32S3 Sense.
4. **Documentamos la participación del equipo** y las principales etapas del laboratorio con fotografías y capturas. Estas evidencias permiten comprender el procedimiento seguido y verificar los resultados observados.
5. **Identificamos la necesidad de realizar pruebas adicionales** con otros objetos y condiciones para evaluar mejor el comportamiento del modelo antes de utilizarlo en una aplicación más amplia.

## 7. Archivos y evidencias del repositorio

Para que el README 2 quede acompañado de sus entregables, el repositorio debe contar con los siguientes archivos:

- **Conjunto de datos `.zip`:** contiene las imágenes recopiladas durante el laboratorio. **Subido al repositorio**, según el registro del equipo.
- **Archivo del modelo entrenado:** debe guardarse y subirse al repositorio, conforme a lo solicitado en la actividad. **[VERIFICAR QUE YA ESTÉ SUBIDO]**.
- **Evidencias fotográficas:** fotografías de las participantes durante la captura de datos, las pruebas de reconocimiento y la activación del LED.
- **Capturas de resultados:** imágenes de SenseCraft AI que muestran el reconocimiento de lentes y celulares, con sus porcentajes de confianza.
- **README 2:** documentación del procedimiento, los resultados y las referencias utilizadas.

## 8. Referencias bibliográficas

<a id="ref1"></a>

[1] Universidad Peruana Cayetano Heredia, *TinyML con XIAO ESP32S3 Sense: Laboratorio con SenseCraft*, material de clase, Perú, 2026.

<a id="ref2"></a>

[2] Seeed Studio, “Getting Started with Seeed Studio XIAO ESP32-S3 Series,” *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/. [Consultado: 13-oct-2026].

<a id="ref3"></a>

[3] Seeed Studio, “Train an Image Classification Model with SenseCraft AI,” *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/sensecraft-ai/tutorials/sensecraft-ai-training-classification/. [Consultado: 13-oct-2026].

<a id="ref4"></a>

[4] Seeed Studio, “SenseCraft AI: Train and Deploy Edge AI Models,” *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/sensecraft-ai/overview/. [Consultado: 13-oct-2026].

<a id="ref5"></a>

[5] Seeed Studio, “Configuring Model Output and GPIO on SenseCraft AI for XIAO ESP32S3 Sense,” *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/sensecraft-ai/tutorials/sensecraft-ai-output-gpio-xiao/. [Consultado: 13-oct-2026].
