
# Clasificación de lentes y celulares mediante SenseCraft AI y activación de LED con GPIO

## 1. Introducción

Tiny Machine Learning (TinyML) es una tecnología que permite implementar modelos de aprendizaje automático en dispositivos pequeños, como los microcontroladores. Su aplicación hace posible que estos dispositivos procesen información obtenida de sus sensores y realicen tareas de reconocimiento sin depender constantemente de una computadora para ejecutar el modelo [1].

En este taller continuamos trabajando con la placa **XIAO ESP32S3 Sense**, desarrollada por Seeed Studio. Este dispositivo incorpora un procesador ESP32-S3, un módulo de cámara para capturar imágenes y conexiones GPIO que permiten controlar componentes electrónicos. Estas características facilitan el desarrollo de aplicaciones que relacionan el reconocimiento de imágenes con acciones físicas [2].

Para realizar la práctica utilizamos **SenseCraft AI**, una plataforma que permite crear, entrenar y ejecutar modelos de inteligencia artificial. Mediante sus herramientas podemos organizar fotografías en diferentes categorías y utilizarlas para enseñar a un modelo a distinguir los objetos representados en ellas [3].

A diferencia de la primera actividad, en la que empleamos un modelo previamente entrenado para reconocer personas, en esta ocasión desarrollamos nuestro propio modelo de clasificación. Seleccionamos dos objetos de uso cotidiano, **lentes y celulares**, con el propósito de comprobar si el sistema podía diferenciarlos mediante las imágenes capturadas por la cámara de la placa.

Para el entrenamiento recopilamos **81 imágenes de lentes y 81 imágenes de celulares**, reuniendo un total de 162 fotografías. Posteriormente, realizamos pruebas de reconocimiento con la participación de **María Antezana, Melisa Bustos y Gabriela Santamaría**, quienes evaluaron ambas categorías y registraron los porcentajes de confianza mostrados por SenseCraft AI.

Finalmente, configuramos la salida GPIO para que el LED se encendiera cuando el modelo reconociera la categoría Lentes con una confianza superior al 60 %. De esta manera, la actividad comprendió desde la preparación de los datos y el entrenamiento del modelo hasta la evaluación de sus resultados y la comprobación de una respuesta física del dispositivo.

## 2. Objetivos

### 2.1. Objetivo general

Desarrollar y evaluar un modelo de clasificación de imágenes mediante SenseCraft AI y la placa XIAO ESP32S3 Sense, utilizando fotografías de lentes y celulares para comprobar su reconocimiento y configurar la activación de un LED mediante GPIO.

### 2.2. Objetivos específicos

- Recopilar y organizar imágenes de lentes y celulares para construir el conjunto de datos utilizado durante el entrenamiento.
- Crear y entrenar un modelo de clasificación de imágenes mediante SenseCraft AI.
- Realizar pruebas individuales de reconocimiento con las tres integrantes del equipo y registrar los porcentajes de confianza obtenidos.
- Analizar los resultados considerando el umbral inicial de confianza del 43 %.
- Configurar la salida GPIO para encender el LED cuando la categoría Lentes presente una confianza superior al 60 %.
- Comprobar el funcionamiento del LED y documentar las evidencias de cada participante.
- Almacenar los archivos del proyecto y presentar el procedimiento desarrollado mediante GitHub.

## 3. Materiales y herramientas

### 3.1. Materiales utilizados

Para desarrollar el laboratorio utilizamos la placa XIAO ESP32S3 Sense, una laptop y los objetos seleccionados para el reconocimiento. También empleamos SenseCraft AI para crear y entrenar el modelo, observar sus resultados y configurar la salida GPIO.

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
      <td>Placa utilizada para ejecutar el modelo y controlar la salida GPIO.</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td>Cámara de la XIAO ESP32S3 Sense</td>
      <td>Permite capturar las imágenes utilizadas durante el entrenamiento y las pruebas.</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td>Cable USB</td>
      <td>Permite conectar la placa con la laptop.</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td>Laptop</td>
      <td>Se utilizó para acceder a SenseCraft AI y observar los resultados del modelo.</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td>SenseCraft AI</td>
      <td>Plataforma utilizada para crear, entrenar, probar y configurar el modelo.</td>
    </tr>
    <tr>
      <td align="center">6</td>
      <td>Lentes y celular</td>
      <td>Objetos seleccionados para establecer las dos categorías de clasificación.</td>
    </tr>
    <tr>
      <td align="center">7</td>
      <td>LED de la placa</td>
      <td>Indicador utilizado para comprobar la activación mediante GPIO.</td>
    </tr>
    <tr>
      <td align="center">8</td>
      <td>GitHub</td>
      <td>Repositorio utilizado para almacenar los archivos y documentar el proyecto.</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia.</em>
</p>

### 3.2. Características de la placa XIAO ESP32S3 Sense

La XIAO ESP32S3 Sense es una placa de tamaño reducido diseñada para desarrollar proyectos relacionados con inteligencia artificial, sensores y sistemas electrónicos.

Cuenta con un procesador ESP32-S3 de doble núcleo, capaz de trabajar hasta 240 MHz, además de 8 MB de memoria PSRAM y 8 MB de memoria Flash. También dispone de conectividad Wi-Fi, Bluetooth LE, cámara y conexiones GPIO [2].

Para nuestra práctica, las características más importantes fueron la cámara y las conexiones GPIO. La primera permitió recopilar imágenes y realizar las pruebas de reconocimiento, mientras que la segunda se utilizó para controlar el encendido del LED.

La combinación de ambas funciones nos permitió trabajar con dos tipos de resultados: la clasificación visualizada en SenseCraft AI y la respuesta física del dispositivo cuando se cumplía una condición determinada.

## 4. Desarrollo del taller

### 4.1. Paso 1: Creación del modelo de inteligencia artificial

Primero ingresamos a la plataforma **SenseCraft AI** para crear un nuevo modelo de inteligencia artificial.

Dentro de las opciones disponibles seleccionamos **Image Classification Detection**, correspondiente a la actividad de clasificación de imágenes. Mediante esta herramienta podemos entrenar un modelo utilizando fotografías organizadas en categorías previamente definidas [3].

Para nuestro proyecto establecimos dos categorías:

- **Lentes:** fotografías del par de lentes utilizado durante el laboratorio.
- **Celular:** fotografías del dispositivo móvil seleccionado para el entrenamiento.

Elegimos estos objetos porque presentan características visuales diferentes y podíamos utilizarlos directamente durante las pruebas. Nuestro propósito no era reconocer marcas o modelos específicos, sino conseguir que el sistema diferenciara las dos categorías.

Esta organización fue necesaria porque cada fotografía debía asociarse con el objeto correspondiente. De esa manera, el modelo dispondría de ejemplos identificados que le permitirían aprender a reconocer las características visuales de cada clase.

### 4.2. Paso 2: Recopilación de imágenes para el entrenamiento

Después de crear las categorías, comenzamos a recopilar las fotografías necesarias para entrenar el modelo.

Para ello, conectamos la XIAO ESP32S3 Sense a la laptop mediante un cable USB y utilizamos su cámara para registrar las imágenes de los objetos seleccionados.

Durante esta etapa capturamos **81 imágenes de lentes y 81 imágenes de celulares**, obteniendo un total de **162 fotografías**.

<p align="center">
  <strong>Tabla 2.</strong> <em>Distribución de las imágenes utilizadas para el entrenamiento.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Categoría</th>
      <th>Cantidad de imágenes</th>
      <th>Distribución porcentual</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Lentes</td>
      <td align="center">81</td>
      <td align="center">50 %</td>
    </tr>
    <tr>
      <td>Celular</td>
      <td align="center">81</td>
      <td align="center">50 %</td>
    </tr>
    <tr>
      <td><strong>Total</strong></td>
      <td align="center"><strong>162</strong></td>
      <td align="center"><strong>100 %</strong></td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir del registro realizado en SenseCraft AI.</em>
</p>

<img width="1919" height="1026" alt="Cantidad de imágenes recopiladas para las categorías Lentes y Celular" src="https://github.com/user-attachments/assets/628d6847-b9ae-486a-bfa1-3c35c543b4f7" />

<p align="center">
  <strong>Figura 1.</strong> <em>Recopilación de 81 imágenes para cada categoría: Lentes y Celular.</em>
</p>

Como se observa en la tabla y en la captura, ambas categorías cuentan con la misma cantidad de imágenes. Esto permitió mantener una distribución equilibrada en número de fotografías, aunque no garantiza por sí solo que el modelo reconozca ambas clases con la misma precisión.

Es importante señalar que utilizamos **un solo par de lentes y un celular**, cuyas fotografías fueron capturadas principalmente desde uno o dos ángulos. Si bien reunimos la cantidad de imágenes prevista para el taller, la variedad de objetos y perspectivas fue limitada.

La documentación de Seeed Studio recomienda utilizar imágenes con diferentes posiciones, ángulos, fondos e iluminación para mejorar la capacidad de reconocimiento de un modelo frente a nuevas condiciones [3]. Por ello, la variedad de fotografías constituye un aspecto que podríamos mejorar en futuros entrenamientos.

Durante esta etapa participaron María Antezana, Melisa Bustos y Gabriela Santamaría. A continuación, se presentan las evidencias individuales de la recopilación de imágenes.

#### 4.2.1. Participación de María Antezana

María Antezana participó en la captura de fotografías utilizando los objetos seleccionados frente a la cámara de la XIAO ESP32S3 Sense.

Durante el procedimiento verificamos que las imágenes se registraran en las categorías correspondientes, con el propósito de organizar correctamente los datos antes de iniciar el entrenamiento.

<img width="1600" height="1200" alt="María Antezana recopilando imágenes" src="URL_IMAGEN_01" />

<p align="center">
  <strong>Figura 2.</strong> <em>María Antezana participando en la recopilación de imágenes para el entrenamiento del modelo.</em>
</p>

#### 4.2.2. Participación de Melisa Bustos

Melisa Bustos también colaboró en el registro de fotografías mediante SenseCraft AI.

En esta actividad utilizamos la cámara y la laptop para continuar recopilando los datos necesarios, manteniendo separadas las imágenes de lentes y celulares.

<img width="1600" height="1200" alt="Melisa Bustos recopilando imágenes" src="URL_IMAGEN_02" />

<p align="center">
  <strong>Figura 3.</strong> <em>Melisa Bustos realizando la captura de fotografías mediante la XIAO ESP32S3 Sense.</em>
</p>

#### 4.2.3. Participación de Gabriela Santamaría

Gabriela Santamaría participó en el mismo procedimiento, colaborando con la recopilación de las imágenes de entrenamiento.

Al completar esta etapa, contamos con 81 fotografías por categoría, las cuales quedaron preparadas para continuar con la creación del modelo.

<img width="1600" height="1200" alt="Gabriela Santamaría recopilando imágenes" src="URL_IMAGEN_03" />

<p align="center">
  <strong>Figura 4.</strong> <em>Gabriela Santamaría participando en el registro de imágenes para el modelo de clasificación.</em>
</p>

### 4.3. Paso 3: Descarga y almacenamiento de los datos

Una vez completada la recopilación de fotografías, descargamos el conjunto de datos en un archivo comprimido con formato **.zip**.

Este archivo reúne las imágenes utilizadas durante la práctica y permite conservarlas organizadas según sus respectivas categorías.

El almacenamiento de estos datos resulta importante porque mantiene un registro de la información empleada para desarrollar el modelo. Asimismo, permite revisar posteriormente las fotografías y comprobar cómo se preparó el conjunto de entrenamiento.

Es necesario diferenciar este archivo del modelo entrenado. Mientras que el `.zip` contiene las imágenes recopiladas, el modelo es el resultado del proceso de aprendizaje realizado por SenseCraft AI.

Por lo tanto, ambos archivos cumplen funciones distintas dentro del proyecto y deben conservarse como parte de su documentación.

### 4.4. Paso 4: Entrenamiento del modelo

Con las imágenes organizadas, continuamos con el entrenamiento mediante SenseCraft AI.

Para realizarlo, utilizamos las 162 fotografías correspondientes a las categorías Lentes y Celular. Durante este proceso, el sistema analiza las imágenes proporcionadas para aprender a distinguir patrones visuales asociados con cada objeto.

Esto significa que no le indicamos manualmente todas las características que diferencian unos lentes de un celular. En cambio, proporcionamos ejemplos previamente identificados para que el modelo aprendiera a relacionar las imágenes con sus categorías.

De acuerdo con la documentación oficial de Seeed Studio, una vez recopiladas las imágenes y definidas las clases, SenseCraft AI permite iniciar el entrenamiento. Al finalizar, el modelo puede desplegarse en un dispositivo compatible para realizar pruebas de reconocimiento [3].

En nuestro caso, completamos este procedimiento y continuamos con la evaluación para comprobar cómo respondía el sistema al presentar nuevamente los objetos frente a la cámara.

### 4.5. Paso 5: Preparación y ejecución del modelo

Después del entrenamiento, preparamos el modelo para utilizarlo con la placa XIAO ESP32S3 Sense.

Mediante las opciones de SenseCraft AI realizamos el procedimiento correspondiente para ejecutar el modelo y acceder a la vista previa de resultados.

Desde esta sección podíamos observar las imágenes capturadas por la cámara y las clasificaciones mostradas en la laptop.

Durante esta primera evaluación todavía no habíamos configurado GPIO para encender el LED. Nuestro propósito era comprobar el reconocimiento de ambas categorías y registrar los porcentajes de confianza obtenidos.

### 4.6. Paso 6: Configuración inicial del umbral de confianza

Antes de comenzar las pruebas observamos que el parámetro **Confidence Threshold** se encontraba configurado en **43 %**.

Este valor se mantuvo durante las evaluaciones de lentes y celulares, ya que no realizamos modificaciones en la configuración inicial del reconocimiento.

El umbral de confianza establece un valor de referencia que permite determinar qué predicciones cumplen con el nivel mínimo establecido por el sistema.

Sin embargo, debemos diferenciar este parámetro del porcentaje obtenido al analizar cada imagen.

**Umbral de confianza (Confidence Threshold):** corresponde al valor establecido en la configuración del modelo. Durante nuestras pruebas fue del **43 %**.

**Confianza obtenida:** es el porcentaje que el modelo asigna a una categoría cuando procesa una imagen.

Por ejemplo, si presentamos unos lentes y el modelo muestra una confianza del 90 %, significa que asignó esa puntuación a la categoría Lentes. Esto no modifica el umbral inicial, que continúa siendo del 43 %.

Además, una confianza del 90 % no significa que el modelo tenga una precisión general del 90 %. Para determinar su desempeño sería necesario comprobar cuántas clasificaciones realiza correctamente al evaluar un conjunto más amplio de imágenes.

Esta distinción fue importante para interpretar los resultados y evitar confundir los valores establecidos en SenseCraft AI con los porcentajes generados durante el reconocimiento.

### 4.7. Paso 7: Pruebas de reconocimiento de lentes

Después de comprobar que el modelo estaba preparado, comenzamos las pruebas utilizando el par de lentes seleccionado para la actividad.

Cada integrante presentó el objeto frente a la cámara de la XIAO ESP32S3 Sense mientras observábamos la clasificación y el porcentaje de confianza mostrado en SenseCraft AI.

El propósito era verificar si el modelo reconocía correctamente los lentes, manteniendo el umbral inicial del 43 %.

#### 4.7.1. Prueba de reconocimiento de lentes con María Antezana

María Antezana realizó la primera prueba colocando los lentes frente a la cámara del dispositivo.

Durante el procedimiento observamos cómo el modelo procesaba la imagen y comprobamos si la clasificación correspondía al objeto presentado.

<img width="1600" height="1200" alt="María Antezana probando el reconocimiento de lentes" src="URL_IMAGEN_04" />

<p align="center">
  <strong>Figura 5.</strong> <em>María Antezana realizando la prueba de reconocimiento de lentes mediante la XIAO ESP32S3 Sense.</em>
</p>

**Resultado obtenido**

Durante esta prueba, el modelo reconoció la categoría **Lentes con una confianza del 100 %**, superando el umbral inicial del 43 %.

El resultado indica que el sistema asignó su máxima puntuación de confianza a dicha categoría en la imagen analizada.

<img width="1600" height="855" alt="Resultado del reconocimiento de lentes de María Antezana" src="URL_IMAGEN_05" />

<p align="center">
  <strong>Figura 6.</strong> <em>Resultado del reconocimiento de lentes durante la prueba de María Antezana, con una confianza del 100 %.</em>
</p>

#### 4.7.2. Prueba de reconocimiento de lentes con Melisa Bustos

Posteriormente, Melisa Bustos realizó la misma evaluación utilizando los lentes y la cámara de la placa.

Mantuvimos el modelo entrenado y su configuración inicial para comprobar si el reconocimiento se repetía correctamente durante una nueva captura.

<img width="1600" height="1200" alt="Melisa Bustos probando el reconocimiento de lentes" src="URL_IMAGEN_06" />

<p align="center">
  <strong>Figura 7.</strong> <em>Melisa Bustos comprobando el reconocimiento de lentes mediante el modelo de clasificación.</em>
</p>

**Resultado obtenido**

En la prueba de Melisa también se registró una confianza del **100 %** para la categoría Lentes.

Este resultado coincidió con el obtenido anteriormente por María, mostrando que el modelo mantuvo la misma puntuación de confianza durante ambas evaluaciones.

<img width="1600" height="855" alt="Resultado del reconocimiento de lentes de Melisa Bustos" src="URL_IMAGEN_07" />

<p align="center">
  <strong>Figura 8.</strong> <em>Resultado del reconocimiento de lentes durante la prueba de Melisa Bustos, con una confianza del 100 %.</em>
</p>

#### 4.7.3. Prueba de reconocimiento de lentes con Gabriela Santamaría

Finalmente, Gabriela Santamaría presentó los lentes frente a la cámara para completar la evaluación de esta categoría.

El procedimiento se realizó sin modificar los parámetros del modelo, lo que permitió comparar directamente su respuesta con las pruebas anteriores.

<img width="1600" height="1200" alt="Gabriela Santamaría probando el reconocimiento de lentes" src="URL_IMAGEN_08" />

<p align="center">
  <strong>Figura 9.</strong> <em>Gabriela Santamaría realizando la prueba de reconocimiento de lentes mediante SenseCraft AI.</em>
</p>

**Resultado obtenido**

Durante la prueba de Gabriela, SenseCraft AI mostró nuevamente una confianza del **100 %** para Lentes.

Con este resultado completamos las tres evaluaciones individuales, obteniendo la misma clasificación y porcentaje de confianza en todos los casos.

<img width="1600" height="855" alt="Resultado del reconocimiento de lentes de Gabriela Santamaría" src="URL_IMAGEN_09" />

<p align="center">
  <strong>Figura 10.</strong> <em>Resultado del reconocimiento de lentes durante la prueba de Gabriela Santamaría, con una confianza del 100 %.</em>
</p>

### 4.8. Paso 8: Comparación de los resultados de reconocimiento de lentes

Después de realizar las pruebas individuales, organizamos los resultados para comparar la respuesta del modelo durante el reconocimiento de lentes.

En las tres evaluaciones mantuvimos el umbral inicial del **43 %**, sin modificar los parámetros del sistema.

<p align="center">
  <strong>Tabla 3.</strong> <em>Comparación de los resultados de reconocimiento de lentes.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Participante</th>
      <th>Categoría</th>
      <th>Umbral configurado</th>
      <th>Confianza obtenida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>María Antezana</td>
      <td align="center">Lentes</td>
      <td align="center">43 %</td>
      <td align="center">100 %</td>
    </tr>
    <tr>
      <td>Melisa Bustos</td>
      <td align="center">Lentes</td>
      <td align="center">43 %</td>
      <td align="center">100 %</td>
    </tr>
    <tr>
      <td>Gabriela Santamaría</td>
      <td align="center">Lentes</td>
      <td align="center">43 %</td>
      <td align="center">100 %</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de las pruebas realizadas en SenseCraft AI.</em>
</p>

Como se observa en la tabla, durante las evaluaciones de **María, Melisa y Gabriela**, el modelo obtuvo una confianza del **100 %** para la categoría Lentes. En los tres casos reconoció correctamente el objeto y superó el umbral configurado del 43 %.

La coincidencia de estos resultados muestra un comportamiento favorable del modelo durante las pruebas documentadas, ya que mantuvo la máxima puntuación de confianza sin necesidad de modificar su configuración.

No obstante, debemos considerar que las tres evaluaciones se realizaron con el mismo par de lentes utilizado durante el entrenamiento. Además, las imágenes recopiladas presentaban una variedad limitada de perspectivas. Estas condiciones podrían favorecer el reconocimiento de un objeto con características visuales similares a las aprendidas, aunque no realizamos pruebas específicas para determinar su influencia.

Por lo tanto, el **100 % corresponde a la confianza registrada en las tres imágenes evaluadas y no a una precisión general del modelo**. Para comprobar si mantiene ese desempeño sería necesario utilizar otros tipos de lentes, diferentes posiciones y fotografías que no hayan formado parte del entrenamiento.

### 4.9. Paso 9: Pruebas de reconocimiento de celulares

Después de completar el reconocimiento de lentes, continuamos con la categoría Celular.

En esta etapa utilizamos el dispositivo móvil seleccionado durante el entrenamiento y realizamos nuevamente pruebas individuales con María, Melisa y Gabriela.

Mantuvimos el mismo modelo y el umbral del **43 %**, con el propósito de evaluar ambas categorías bajo una configuración equivalente.

#### 4.9.1. Prueba de reconocimiento de celulares con María Antezana

María Antezana realizó la primera evaluación presentando el celular frente a la cámara de la XIAO ESP32S3 Sense.

Durante la prueba observamos la clasificación mostrada en SenseCraft AI para comprobar si el sistema diferenciaba el celular de los lentes utilizados anteriormente.

<img width="1600" height="1200" alt="María Antezana probando el reconocimiento de celulares" src="URL_IMAGEN_10" />

<p align="center">
  <strong>Figura 11.</strong> <em>María Antezana realizando la prueba de reconocimiento de celulares mediante la XIAO ESP32S3 Sense.</em>
</p>

**Resultado obtenido**

El modelo reconoció la categoría **Celular con una confianza del 88 %**, superando el umbral inicial del 43 %.

Aunque este porcentaje fue menor que el registrado en las pruebas con lentes, la clasificación correspondió correctamente al objeto presentado.

<img width="1600" height="855" alt="Resultado del reconocimiento de celulares de María Antezana" src="URL_IMAGEN_11" />

<p align="center">
  <strong>Figura 12.</strong> <em>Resultado del reconocimiento de celulares durante la prueba de María Antezana, con una confianza del 88 %.</em>
</p>

#### 4.9.2. Prueba de reconocimiento de celulares con Melisa Bustos

Posteriormente, Melisa Bustos realizó la evaluación utilizando el mismo celular frente a la cámara.

El procedimiento permitió registrar otra clasificación sin realizar cambios en el modelo ni en su umbral de confianza.

<img width="1600" height="1200" alt="Melisa Bustos probando el reconocimiento de celulares" src="URL_IMAGEN_12" />

<p align="center">
  <strong>Figura 13.</strong> <em>Melisa Bustos realizando la prueba de reconocimiento de celulares mediante SenseCraft AI.</em>
</p>

**Resultado obtenido**

Durante esta prueba, el modelo identificó el celular con una confianza del **77 %**.

Este valor fue inferior al 88 % obtenido por María, pero también superó el umbral del 43 % y correspondió a la categoría correcta.

La diferencia permitió observar que, aun utilizando el mismo objeto y manteniendo la configuración, el modelo podía presentar distintos niveles de confianza entre una captura y otra.

<img width="1600" height="855" alt="Resultado del reconocimiento de celulares de Melisa Bustos" src="URL_IMAGEN_13" />

<p align="center">
  <strong>Figura 14.</strong> <em>Resultado del reconocimiento de celulares durante la prueba de Melisa Bustos, con una confianza del 77 %.</em>
</p>

#### 4.9.3. Prueba de reconocimiento de celulares con Gabriela Santamaría

Finalmente, Gabriela Santamaría realizó la prueba para completar el reconocimiento individual de celulares.

Al presentar el objeto frente a la cámara, observamos la respuesta de SenseCraft AI y registramos el porcentaje correspondiente.

<img width="1600" height="1200" alt="Gabriela Santamaría probando el reconocimiento de celulares" src="URL_IMAGEN_14" />

<p align="center">
  <strong>Figura 15.</strong> <em>Gabriela Santamaría realizando la prueba de reconocimiento de celulares con el modelo desarrollado.</em>
</p>

**Resultado obtenido**

El sistema reconoció la categoría **Celular con una confianza del 90 %**, siendo el porcentaje más alto de las tres pruebas realizadas con este objeto.

Este resultado también superó el umbral inicial y completó el registro necesario para comparar las respuestas del modelo.

<img width="1600" height="855" alt="Resultado del reconocimiento de celulares de Gabriela Santamaría" src="URL_IMAGEN_15" />

<p align="center">
  <strong>Figura 16.</strong> <em>Resultado del reconocimiento de celulares durante la prueba de Gabriela Santamaría, con una confianza del 90 %.</em>
</p>

### 4.10. Paso 10: Comparación de los resultados de reconocimiento de celulares

Una vez concluidas las pruebas, organizamos los porcentajes registrados para identificar las diferencias observadas entre las evaluaciones.

<p align="center">
  <strong>Tabla 4.</strong> <em>Comparación de los resultados de reconocimiento de celulares.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Participante</th>
      <th>Categoría</th>
      <th>Umbral configurado</th>
      <th>Confianza obtenida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>María Antezana</td>
      <td align="center">Celular</td>
      <td align="center">43 %</td>
      <td align="center">88 %</td>
    </tr>
    <tr>
      <td>Melisa Bustos</td>
      <td align="center">Celular</td>
      <td align="center">43 %</td>
      <td align="center">77 %</td>
    </tr>
    <tr>
      <td>Gabriela Santamaría</td>
      <td align="center">Celular</td>
      <td align="center">43 %</td>
      <td align="center">90 %</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de las pruebas realizadas en SenseCraft AI.</em>
</p>

Los resultados muestran que **María obtuvo una confianza del 88 %, Melisa del 77 % y Gabriela del 90 %**. En los tres casos, el modelo reconoció correctamente el celular y superó el umbral establecido.

A diferencia de las pruebas con lentes, en esta categoría observamos variaciones entre los porcentajes. Gabriela registró el valor más alto, mientras que Melisa obtuvo el menor, con una diferencia de **13 puntos porcentuales** entre ambas evaluaciones.

El promedio de confianza de las tres pruebas fue del **85 %**. Este valor resume las puntuaciones obtenidas, pero no representa una medida de la precisión general del modelo.

La variación observada indica que el sistema no asignó exactamente la misma confianza al celular en todas las capturas. Esto podría estar relacionado con diferencias en la posición del objeto, el encuadre o la iluminación. Sin embargo, no realizamos pruebas controladas que permitan establecer cuál de estos factores influyó en los resultados.

En consecuencia, podemos afirmar que el modelo reconoció correctamente el celular durante las tres evaluaciones, aunque con porcentajes distintos. Para conocer mejor su comportamiento sería necesario repetir las pruebas con otros dispositivos y condiciones de captura.

### 4.11. Paso 11: Análisis general de los porcentajes de confianza

Al comparar las dos categorías, observamos una diferencia en el comportamiento del modelo.

En las pruebas con lentes, las tres integrantes obtuvieron una confianza del **100 %**. En cambio, durante el reconocimiento de celulares se registraron porcentajes de **88 %, 77 % y 90 %**.

Estos resultados muestran que el modelo fue consistente en sus puntuaciones para los lentes, mientras que presentó cierta variación al evaluar el celular. A pesar de ello, las seis clasificaciones documentadas correspondieron a los objetos presentados y superaron el umbral inicial del 43 %.

Es importante señalar que haber obtenido seis clasificaciones correctas no significa que el modelo tenga una precisión general del 100 %. Las evaluaciones se realizaron utilizando únicamente dos objetos físicos, que también habían sido empleados durante el entrenamiento.

Por esta razón, las pruebas permiten comprobar el funcionamiento del modelo en las condiciones del laboratorio, pero no determinan cómo respondería frente a otros lentes, celulares o imágenes diferentes.

Esta interpretación también nos ayudó a comprender que la confianza de una clasificación debe analizarse junto con el objeto reconocido, el umbral configurado y las condiciones en las que se realizó la prueba.

### 4.12. Paso 12: Configuración de GPIO para encender el LED

Después de completar las pruebas de reconocimiento, continuamos con la configuración de la salida **GPIO**.

GPIO significa *General Purpose Input/Output*, que en español corresponde a entradas y salidas de propósito general. Estas conexiones permiten que un dispositivo reciba señales o controle componentes electrónicos.

En nuestro laboratorio utilizamos esta función para encender el LED cuando el modelo reconociera unos lentes con una confianza superior al porcentaje establecido.

Para realizar la configuración ingresamos a la sección:

**Output → GPIO**

La documentación oficial de Seeed Studio explica que SenseCraft AI permite establecer condiciones mediante parámetros como **Object, Condition, Confidence, GPIO, Default Status y Active Status**, los cuales determinan qué reconocimiento debe producirse y cómo responderá la salida electrónica [4].

#### 4.12.1. Parámetros utilizados durante la configuración

Establecimos que el LED se encendiera cuando el modelo reconociera la categoría **Lentes** con una confianza **mayor al 60 %**.

<p align="center">
  <strong>Tabla 5.</strong> <em>Parámetros utilizados para configurar la activación del LED mediante GPIO.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Parámetro</th>
      <th>Valor seleccionado</th>
      <th>Función</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Object</td>
      <td align="center">Lentes</td>
      <td>Indica la categoría que debe reconocer el modelo para activar la salida.</td>
    </tr>
    <tr>
      <td>GPIO</td>
      <td align="center">LED</td>
      <td>Selecciona el indicador que deseamos controlar.</td>
    </tr>
    <tr>
      <td>Condition</td>
      <td align="center">Greater than</td>
      <td>Establece que la confianza debe ser mayor al porcentaje indicado.</td>
    </tr>
    <tr>
      <td>Confidence</td>
      <td align="center">60 %</td>
      <td>Determina el valor que debe superarse para activar el LED.</td>
    </tr>
    <tr>
      <td>Default Status</td>
      <td align="center">LED apagado</td>
      <td>Mantiene la salida en su estado inicial cuando no se cumple la condición.</td>
    </tr>
    <tr>
      <td>Active Status</td>
      <td align="center">LED encendido</td>
      <td>Activa el indicador cuando se cumple la condición configurada.</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Fuente: Elaboración propia a partir de la configuración realizada en SenseCraft AI.</em>
</p>

#### 4.12.2. Fundamentación de los parámetros seleccionados

**Object: Lentes**

Seleccionamos esta categoría porque queríamos que la activación del LED dependiera específicamente del reconocimiento de los lentes.

Aunque nuestro modelo estaba entrenado para diferenciar lentes y celulares, en esta etapa necesitábamos elegir cuál de las categorías funcionaría como condición de activación.

**GPIO: LED**

Elegimos el LED para observar una respuesta física del dispositivo. A diferencia de las pruebas anteriores, donde únicamente visualizábamos los resultados en la laptop, esta configuración nos permitió comprobar el efecto del reconocimiento sobre una salida electrónica.

**Condition: Greater than**

Seleccionamos *Greater than*, que significa "mayor que", porque necesitábamos establecer una comparación entre la confianza obtenida y el valor requerido para encender el LED.

Esta opción indica que el porcentaje debe superar el límite configurado y no simplemente igualarlo [4].

**Confidence: 60 %**

Establecimos una confianza del **60 %** como condición de activación.

Este valor es superior al umbral inicial del 43 % utilizado durante las pruebas de reconocimiento. Lo seleccionamos para que el encendido del LED dependiera de un nivel de confianza más exigente.

Por ejemplo, si el modelo identificaba unos lentes con una confianza del 85 %, el LED debía encenderse porque el resultado superaba el 60 %.

En cambio, si obtenía una confianza del 55 %, el indicador permanecería apagado al no cumplirse la condición.

**Default Status: LED apagado**

Configuramos este estado para mantener el LED apagado cuando el reconocimiento no alcanzara el porcentaje establecido.

**Active Status: LED encendido**

Seleccionamos este estado para que el indicador se encendiera cuando el sistema reconociera la categoría Lentes con una confianza superior al 60 %.

De esta manera, relacionamos el resultado de la clasificación con el funcionamiento de un componente electrónico.

#### 4.12.3. Diferencia entre el umbral inicial y la configuración GPIO

Durante el laboratorio utilizamos dos valores de confianza con funciones distintas.

El primero fue el **43 %**, correspondiente al umbral inicial del modelo. Este parámetro se mantuvo durante las pruebas de reconocimiento de lentes y celulares.

Posteriormente, configuramos GPIO con una condición **mayor al 60 %**, aplicable específicamente a la categoría Lentes.

Por lo tanto, un reconocimiento podía cumplir el umbral inicial del modelo sin alcanzar necesariamente el porcentaje requerido para encender el LED.

Esta diferencia permitió comprender que la clasificación de un objeto y la activación de una salida electrónica pueden depender de condiciones diferentes.

#### 4.12.4. Evidencia de la configuración GPIO

En la siguiente captura se presentan los parámetros utilizados para controlar el LED mediante SenseCraft AI.

Se observa la selección de la categoría Lentes, la condición Greater than y el porcentaje de confianza establecido en 60 %.

<img width="1600" height="855" alt="Configuración de GPIO en SenseCraft AI" src="URL_IMAGEN_16" />

<p align="center">
  <strong>Figura 17.</strong> <em>Configuración GPIO en SenseCraft AI, donde se establece el reconocimiento de Lentes con una confianza mayor al 60 % para activar el LED.</em>
</p>

### 4.13. Paso 13: Comprensión de la condición de activación

Después de configurar GPIO, analizamos cómo debía responder el LED según los resultados del reconocimiento.

La condición establecida fue la siguiente:

**Si el modelo reconoce Lentes con una confianza mayor al 60 %, el LED se enciende.**

**Si la confianza de Lentes no supera el 60 %, el LED permanece apagado.**

Para explicar este funcionamiento, presentamos algunos ejemplos:

<p align="center">
  <strong>Tabla 6.</strong> <em>Ejemplos del funcionamiento esperado del LED según la confianza del reconocimiento.</em>
</p>

<div align="center">
<table>
  <thead>
    <tr>
      <th>Confianza de Lentes</th>
      <th>¿Supera el 60 %?</th>
      <th>Estado esperado del LED</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">90 %</td>
      <td align="center">Sí</td>
      <td align="center">Encendido</td>
    </tr>
    <tr>
      <td align="center">75 %</td>
      <td align="center">Sí</td>
      <td align="center">Encendido</td>
    </tr>
    <tr>
      <td align="center">60 %</td>
      <td align="center">No</td>
      <td align="center">Apagado</td>
    </tr>
    <tr>
      <td align="center">45 %</td>
      <td align="center">No</td>
      <td align="center">Apagado</td>
    </tr>
  </tbody>
</table>
</div>

<p align="center">
  <em>Nota: Los porcentajes presentados son ejemplos para explicar la condición de activación y no corresponden a mediciones adicionales del laboratorio.</em>
</p>

Como se observa, la condición Greater than requiere que la confianza sea estrictamente superior al 60 %. Por ello, un resultado igual a ese porcentaje no sería suficiente para encender el LED.

Asimismo, debemos recordar que la categoría seleccionada fue Lentes. Esto significa que la activación depende de la confianza asociada con dicho objeto y no de cualquier clasificación mostrada por el sistema.

Con esta configuración comprendimos cómo establecer condiciones para controlar componentes electrónicos a partir de los resultados obtenidos mediante inteligencia artificial.

### 4.14. Paso 14: Pruebas de activación del LED mediante GPIO

Una vez terminada la configuración, realizamos las pruebas para comprobar si el LED respondía correctamente al reconocimiento de lentes.

En esta etapa participaron María Antezana, Melisa Bustos y Gabriela Santamaría, quienes utilizaron la misma placa y mantuvieron los parámetros establecidos.

A diferencia de las evaluaciones anteriores, ahora buscábamos comprobar que una clasificación con una confianza superior al 60 % produjera el encendido del LED.

Para documentar el procedimiento, cada integrante registró una fotografía durante la prueba y otra con un acercamiento al dispositivo, donde se aprecia la luz encendida.

#### 4.14.1. Prueba de activación del LED con María Antezana

María Antezana realizó la primera prueba colocando los lentes frente a la cámara de la XIAO ESP32S3 Sense.

Mientras el modelo analizaba la imagen, observamos la respuesta del dispositivo para verificar si se cumplía la condición establecida en GPIO.

Durante la evaluación comprobamos que el LED se encendía cuando la confianza de reconocimiento superaba el 60 %.

<img width="1600" height="1200" alt="María Antezana realizando la prueba de activación del LED" src="URL_IMAGEN_17" />

<p align="center">
  <strong>Figura 18.</strong> <em>María Antezana realizando la prueba de reconocimiento de lentes con la configuración GPIO activada.</em>
</p>

Para registrar la respuesta de la placa, tomamos una segunda fotografía con un acercamiento al LED.

En esta evidencia se aprecia la luz encendida, lo que permite comprobar visualmente el funcionamiento de la salida durante la prueba de María.

<img width="1600" height="1200" alt="LED encendido durante la prueba de María Antezana" src="URL_IMAGEN_18" />

<p align="center">
  <strong>Figura 19.</strong> <em>Evidencia del LED encendido durante la prueba de reconocimiento de lentes realizada por María Antezana.</em>
</p>

#### 4.14.2. Prueba de activación del LED con Melisa Bustos

Posteriormente, Melisa Bustos realizó la misma evaluación utilizando el par de lentes y la cámara del dispositivo.

Mantuvimos la categoría Lentes y la condición Greater than con una confianza del 60 %, sin modificar los parámetros establecidos anteriormente.

Durante la prueba observamos nuevamente el encendido del LED al cumplirse la condición de reconocimiento.

<img width="1600" height="1200" alt="Melisa Bustos realizando la prueba de activación del LED" src="URL_IMAGEN_19" />

<p align="center">
  <strong>Figura 20.</strong> <em>Melisa Bustos comprobando el funcionamiento del reconocimiento de lentes con la salida GPIO configurada.</em>
</p>

Asimismo, registramos una fotografía más cercana para mostrar el estado del LED durante esta evaluación.

La imagen permite identificar la respuesta física de la placa, complementando la evidencia del procedimiento realizado por Melisa.

<img width="1600" height="1200" alt="LED encendido durante la prueba de Melisa Bustos" src="URL_IMAGEN_20" />

<p align="center">
  <strong>Figura 21.</strong> <em>Evidencia del LED encendido durante la prueba de reconocimiento de lentes realizada por Melisa Bustos.</em>
</p>

#### 4.14.3. Prueba de activación del LED con Gabriela Santamaría

Finalmente, Gabriela Santamaría realizó la prueba para completar la comprobación de GPIO con las tres integrantes.

Al colocar los lentes frente a la cámara, verificamos la respuesta del modelo y observamos el encendido del LED cuando se cumplía la condición configurada.

Esta evaluación permitió repetir el procedimiento utilizando los mismos parámetros, sin necesidad de realizar modificaciones adicionales.

<p align="center">
  
  <img width="1600" height="1206" alt="image" src="https://github.com/user-attachments/assets/97cc0b94-d3ad-4aea-a985-b2fa8729fbe7" />

  <strong>Figura 22.</strong> <em>Gabriela Santamaría realizando la prueba de activación del LED mediante GPIO y el reconocimiento de lentes.</em>
</p>

Al igual que en las evaluaciones anteriores, registramos una segunda fotografía enfocando la placa para mostrar con mayor claridad el LED encendido.

Con esta evidencia completamos la documentación individual de las pruebas de activación.

<p align="center">
  
  <img width="1600" height="1214" alt="image" src="https://github.com/user-attachments/assets/7963662e-90fa-4d4e-aea0-909414617d11" />

  <strong>Figura 23.</strong> <em>Evidencia del LED encendido durante la prueba de reconocimiento de lentes realizada por Gabriela Santamaría.</em>
</p>

Las pruebas realizadas por las tres integrantes permitieron comprobar que la configuración GPIO respondía al reconocimiento de lentes bajo las condiciones establecidas.

Además de las clasificaciones visualizadas en SenseCraft AI, pudimos observar una respuesta física del dispositivo, lo que demuestra la relación entre el procesamiento de imágenes y el control de una salida electrónica.

## 5. Resultados y análisis

### 5.1. Resultados del entrenamiento

Durante el laboratorio desarrollamos un modelo de clasificación de imágenes utilizando SenseCraft AI y la placa XIAO ESP32S3 Sense.

Para el entrenamiento recopilamos 162 fotografías, distribuidas equitativamente entre las categorías Lentes y Celular. Esta organización permitió proporcionar al modelo la misma cantidad de ejemplos para cada clase.

Una vez finalizado el entrenamiento, conseguimos ejecutar el modelo y realizar las evaluaciones correspondientes.

Sin embargo, es importante considerar que **las 81 imágenes de cada categoría no representaban 81 objetos diferentes**, sino fotografías de un mismo par de lentes y un mismo celular, capturadas desde un número reducido de perspectivas.

Por ello, aunque el entrenamiento permitió realizar las pruebas previstas, la variedad del conjunto de datos fue limitada. Este aspecto debe tenerse en cuenta al interpretar los resultados, ya que un modelo puede responder favorablemente ante imágenes similares a las utilizadas durante su aprendizaje sin mantener necesariamente ese desempeño frente a objetos nuevos.

### 5.2. Resultados del reconocimiento de lentes

Durante las evaluaciones realizadas por María Antezana, Melisa Bustos y Gabriela Santamaría, el modelo reconoció correctamente la categoría Lentes con una confianza del **100 % en los tres casos**.

Estos resultados superaron el umbral inicial del 43 % y mostraron que el sistema podía identificar el objeto durante las pruebas documentadas sin modificar su configuración.

La coincidencia de los porcentajes indica que el modelo mantuvo su máxima puntuación de confianza en las tres imágenes analizadas. No obstante, debido a que se utilizó el mismo par de lentes empleado durante el entrenamiento, los resultados deben interpretarse dentro de las condiciones específicas del laboratorio.

Por lo tanto, las pruebas fueron satisfactorias para esta categoría, pero no permiten asegurar que el modelo reconozca con la misma confianza otros tipos de lentes.

### 5.3. Resultados del reconocimiento de celulares

En las pruebas correspondientes a la categoría Celular registramos porcentajes de **88 % para María, 77 % para Melisa y 90 % para Gabriela**.

Las tres clasificaciones fueron correctas y superaron el umbral del 43 %. Sin embargo, a diferencia de los lentes, el sistema mostró variaciones en sus puntuaciones.

La confianza promedio fue del **85 %**, con una diferencia de 13 puntos porcentuales entre el resultado más alto y el más bajo.

Aunque no podemos determinar qué produjo estas diferencias, los resultados muestran que la confianza del modelo puede cambiar entre capturas de un mismo objeto.

Al comparar ambas categorías, los lentes presentaron puntuaciones más altas y uniformes que el celular en las pruebas realizadas. Sin embargo, esto no demuestra que el modelo reconozca mejor todos los lentes que todos los celulares, puesto que únicamente evaluamos un objeto de cada categoría.

Para establecer una comparación más representativa sería necesario realizar nuevas pruebas con diferentes modelos de celulares y tipos de lentes.

### 5.4. Resultados de la configuración GPIO

Después de evaluar el reconocimiento, configuramos GPIO para activar el LED cuando el modelo identificara la categoría Lentes con una confianza superior al 60 %.

Las pruebas realizadas por las tres integrantes permitieron observar el encendido de la luz al cumplirse la condición establecida. Este resultado se documentó mediante fotografías individuales y acercamientos al dispositivo.

La actividad permitió comprobar que la información obtenida mediante el reconocimiento de imágenes podía utilizarse para controlar una salida electrónica.

También distinguimos el umbral inicial del **43 %**, empleado durante las pruebas de clasificación, del **60 %** establecido para activar GPIO. Esta diferencia resulta importante porque permite configurar una condición específica para el encendido del LED, independiente del valor utilizado inicialmente para visualizar los reconocimientos.

De esta manera, conseguimos relacionar el funcionamiento del modelo de inteligencia artificial con una acción observable en la placa.

### 5.5. Limitaciones de las pruebas y propuestas de mejora

Aunque los resultados fueron favorables durante el laboratorio, identificamos algunas limitaciones relacionadas principalmente con las imágenes de entrenamiento y el alcance de las pruebas.

En primer lugar, **utilizamos únicamente un par de lentes y un celular**. Si bien recopilamos 81 imágenes por categoría, todas correspondían a los mismos objetos físicos. Esto redujo la variedad de características que el modelo pudo aprender, por lo que no podemos asegurar que reconozca correctamente otros diseños de lentes o diferentes modelos de celulares.

Asimismo, **las fotografías fueron capturadas principalmente desde uno o dos ángulos**, sin una variación amplia en las posiciones de los objetos. Esta característica limita la posibilidad de evaluar cómo respondería el modelo ante imágenes tomadas desde perspectivas diferentes.

Otra limitación fue que las pruebas se realizaron utilizando los mismos objetos empleados durante el entrenamiento. Por esta razón, los porcentajes registrados permiten describir el funcionamiento observado, pero no constituyen una evaluación suficiente de la capacidad del modelo para reconocer objetos nuevos.

Para mejorar el proyecto, sería recomendable ampliar el conjunto de datos incorporando lentes de diferentes formas, tamaños y colores, así como celulares de distintas marcas y diseños. También convendría tomar fotografías desde varios ángulos, modificar las distancias respecto a la cámara y trabajar con diferentes condiciones de iluminación.

Finalmente, sería importante reservar algunas imágenes nuevas exclusivamente para las pruebas, sin utilizarlas durante el entrenamiento. De esta manera, podríamos evaluar con mayor claridad si el modelo reconoce las características generales de cada categoría y no solamente las imágenes similares a las que ya había procesado.

Estas mejoras permitirían realizar una evaluación más completa, identificar posibles errores de clasificación y conocer mejor las condiciones en las que el modelo mantiene un reconocimiento adecuado.

## 6. Conclusiones

1. Durante el taller desarrollamos un modelo de clasificación de imágenes mediante SenseCraft AI y la placa XIAO ESP32S3 Sense. Para ello, recopilamos 162 fotografías distribuidas en dos categorías, lo que nos permitió conocer el procedimiento de preparación de datos, entrenamiento y ejecución de un modelo propio de inteligencia artificial.

2. Las pruebas realizadas por María Antezana, Melisa Bustos y Gabriela Santamaría permitieron comprobar el reconocimiento de lentes y celulares. En la categoría Lentes obtuvimos una confianza del 100 % en las tres evaluaciones, mientras que para Celular registramos valores de 88 %, 77 % y 90 %. Estos resultados mostraron que el modelo podía clasificar correctamente ambos objetos durante las pruebas realizadas.

3. Al interpretar los resultados comprendimos la diferencia entre el umbral de confianza, establecido inicialmente en 43 %, y los porcentajes generados durante cada clasificación. Asimismo, identificamos que una confianza elevada no representa necesariamente la precisión general del modelo, especialmente cuando las pruebas se realizan con los mismos objetos utilizados durante el entrenamiento.

4. Mediante la configuración GPIO logramos activar el LED al reconocer la categoría Lentes con una confianza superior al 60 %. Las pruebas individuales permitieron observar esta respuesta física y comprobar cómo los resultados del modelo podían utilizarse para controlar un componente electrónico.

5. Finalmente, reconocimos que la variedad de imágenes es un aspecto importante para mejorar el funcionamiento del modelo. Debido a que utilizamos un solo objeto por categoría y fotografías tomadas desde pocos ángulos, consideramos necesario ampliar los datos y realizar pruebas con objetos nuevos para evaluar mejor su capacidad de reconocimiento.


## 7. Archivos del proyecto

Como parte de la documentación del laboratorio, nuestro repositorio de GitHub contiene los archivos utilizados durante el desarrollo del modelo de clasificación. Para facilitar su revisión, se incluyen los siguientes enlaces de acceso directo:

- **[Conjunto de datos (.zip)](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Proyecto_Integrador/Talleres/TinyML-Sensecraft/classification_dataset.zip):** contiene las 162 imágenes recopiladas para el entrenamiento, distribuidas en las categorías Lentes y Celular.

- **[Modelo entrenado](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Proyecto_Integrador/Talleres/TinyML-Sensecraft/classification_dataset.zip):** archivo correspondiente al modelo de clasificación de lentes y celulares desarrollado mediante SenseCraft AI.

Estos archivos permiten conservar los datos y resultados del proyecto, así como facilitar su consulta y revisión.

## 8. Referencias bibliográficas

<a id="ref1"></a>

[1] Universidad Peruana Cayetano Heredia, *TinyML con XIAO ESP32S3 Sense: Laboratorio con SenseCraft*, material de clase, Lima, Perú, 2026.

<a id="ref2"></a>

[2] Seeed Studio, "Getting Started with Seeed Studio XIAO ESP32-S3 Series," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/. [Accedido: 13-oct-2026].

<a id="ref3"></a>

[3] Seeed Studio, "Train an Image Classification Model with SenseCraft AI," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/sensecraft-ai/tutorials/sensecraft-ai-training-classification/. [Accedido: 13-oct-2026].

<a id="ref4"></a>

[4] Seeed Studio, "Configuring Model Output and GPIO on SenseCraft AI for XIAO ESP32S3 Sense," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/sensecraft-ai/tutorials/sensecraft-ai-output-gpio-xiao/. [Accedido: 13-oct-2026].
