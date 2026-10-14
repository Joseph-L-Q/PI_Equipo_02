
# Clasificación de personas y activación mediante GPIO utilizando SenseCraft AI

## 1. Introducción

Tiny Machine Learning (TinyML) es una tecnología que permite utilizar modelos de inteligencia artificial en dispositivos pequeños, como los microcontroladores. Esto hace posible que estos dispositivos procesen información y realicen tareas de reconocimiento sin depender constantemente de una computadora o de Internet [ [1] ](#ref1).

En este taller trabajamos con la placa **XIAO ESP32S3 Sense**, desarrollada por Seeed Studio. Esta placa cuenta con un microcontrolador ESP32-S3 y un módulo de cámara que permite capturar imágenes. También dispone de conexiones GPIO que podemos utilizar para controlar componentes electrónicos, como un LED [ [2] ](#ref2).

Para realizar la práctica utilizamos **SenseCraft AI**, una plataforma que nos permite seleccionar modelos de inteligencia artificial, instalarlos en dispositivos compatibles y observar sus resultados [ [3] ](#ref3).

En nuestro caso seleccionamos el modelo **Person Classification**, que sirve para identificar si en una imagen aparece una persona o no. Para comprobar su funcionamiento realizamos pruebas con nuestros compañeros Joseph Lombardi y Yoichi Palacios, quienes se colocaron frente a la cámara mientras observábamos los resultados en la computadora.

Después de comprobar que el modelo podía reconocer personas, utilizamos la opción **GPIO** para configurar el encendido de un LED. Establecimos que el LED se encendiera cuando la confianza del reconocimiento de una persona fuera mayor al 60 %.

De esta manera, el taller nos permitió comprender cómo podemos utilizar un modelo de inteligencia artificial para reconocer personas mediante una cámara y, al mismo tiempo, controlar una salida física de la placa.

## 2. Objetivos

### 2.1. Objetivo general

Utilizar el modelo Person Classification en la placa XIAO ESP32S3 Sense mediante SenseCraft AI, realizando pruebas de reconocimiento de personas y configurando el encendido de un LED mediante GPIO.

### 2.2. Objetivos específicos

- Conocer el funcionamiento básico de TinyML y de la placa XIAO ESP32S3 Sense.
- Seleccionar e instalar el modelo Person Classification mediante SenseCraft AI.
- Realizar pruebas de reconocimiento de personas utilizando la cámara.
- Observar e interpretar los porcentajes de confianza que muestra el modelo.
- Configurar la salida GPIO para encender un LED cuando la confianza de detección sea mayor al 60 %.
- Comprobar el funcionamiento del LED mediante las pruebas realizadas con nuestros compañeros.

## 3. Materiales y herramientas

### 3.1. Materiales utilizados

Para desarrollar el taller utilizamos los siguientes materiales y herramientas:

**Tabla 1. Materiales y herramientas utilizados en el laboratorio**

| N.º | Material o herramienta | Función |
|:---:|---|---|
| 1 | XIAO ESP32S3 Sense | Placa utilizada para ejecutar el modelo y controlar el LED. |
| 2 | Cámara de la XIAO ESP32S3 Sense | Permite capturar las imágenes de las personas. |
| 3 | Cable USB | Permite conectar la placa con la computadora. |
| 4 | Computadora | Se utilizó para acceder a SenseCraft AI y observar los resultados. |
| 5 | SenseCraft AI | Plataforma utilizada para seleccionar y configurar el modelo. |
| 6 | Person Classification | Modelo de inteligencia artificial utilizado para reconocer personas. |
| 7 | LED de la placa | Indicador que se enciende cuando se cumple la condición configurada. |

*Fuente: Elaboración propia.*

### 3.2. Características de la placa

La XIAO ESP32S3 Sense es una placa pequeña que permite desarrollar proyectos relacionados con inteligencia artificial, sensores y sistemas electrónicos. Una de sus ventajas es que cuenta con una cámara que podemos utilizar para realizar pruebas de reconocimiento de imágenes [ [2] ](#ref2).

**Tabla 2. Características principales de la XIAO ESP32S3 Sense**

| Característica | Descripción |
|---|---|
| Microcontrolador | ESP32-S3 |
| Procesador | Doble núcleo, hasta 240 MHz |
| Memoria PSRAM | 8 MB |
| Memoria Flash | 8 MB |
| Conectividad | Wi-Fi y Bluetooth LE |
| Cámara | Módulo compatible con XIAO ESP32S3 Sense |
| GPIO | Permite controlar entradas y salidas |
| Conexión | USB |

*Fuente: Material del taller [ [1] ](#ref1) y documentación de Seeed Studio [ [2] ](#ref2).*

En nuestro laboratorio utilizamos principalmente la cámara para reconocer personas y la salida GPIO para encender el LED.

## 4. Desarrollo del taller

### 4.1. Paso 1: Selección del modelo Person Classification

Primero ingresamos a la plataforma SenseCraft AI para buscar el modelo que íbamos a utilizar durante el taller.

Dentro de la plataforma encontramos diferentes modelos de inteligencia artificial y seleccionamos **Person Classification**, porque nuestro objetivo era comprobar si la cámara podía reconocer cuando una persona se encontraba frente a ella.

Este modelo trabaja con dos categorías:

**Tabla 3. Categorías del modelo Person Classification**

| Categoría | Significado |
|---|---|
| Person | Indica que el modelo reconoce la presencia de una persona. |
| Not a person | Indica que el modelo no reconoce una persona en la imagen. |

*Fuente: Modelo Person Classification utilizado en SenseCraft AI.*

Es importante mencionar que este modelo no identifica el nombre de las personas. Lo que hace es analizar la imagen y determinar si encuentra una persona.

Por ese motivo, durante el taller utilizamos a nuestros compañeros para comprobar si el modelo los clasificaba correctamente como personas.

Después de seleccionar el modelo, continuamos con el procedimiento de instalación en la placa.

<img width="1600" height="855" alt="image" src="https://github.com/user-attachments/assets/a4779d9a-ddb6-4d07-93d2-a8d3c3106413" />

*Figura 1. Selección del modelo Person Classification en SenseCraft AI para realizar las pruebas de reconocimiento de personas.*

### 4.2. Paso 2: Conexión de la placa XIAO ESP32S3 Sense

Después de seleccionar el modelo, conectamos la placa XIAO ESP32S3 Sense a la computadora utilizando un cable USB.

Realizamos este procedimiento porque necesitábamos que la computadora reconociera el dispositivo y poder cargar el modelo seleccionado.

Durante este paso seguimos las instrucciones que aparecían en SenseCraft AI para preparar la placa.

En una de las pantallas apareció el mensaje:

**"Please flash the model to the device first".**

Este mensaje nos indicaba que primero debíamos instalar el modelo en la placa antes de comenzar las pruebas.

Una vez realizado el procedimiento de preparación, continuamos con la ejecución del modelo y la utilización de la cámara.


<img width="1600" height="861" alt="image" src="https://github.com/user-attachments/assets/d283b017-b8bb-4c0b-aa53-aabdee270124" />

*Figura 2. Pantalla de SenseCraft AI durante la preparación de la XIAO ESP32S3 Sense, donde se indica que debemos cargar el modelo en el dispositivo.*

### 4.3. Paso 3: Inicio de la cámara y ejecución del modelo

Una vez que tuvimos preparado el modelo, ingresamos a la opción **Preview** de SenseCraft AI.

Esta opción nos permitió observar en la computadora lo que estaba capturando la cámara de la placa.

Durante esta parte comprobamos que la cámara funcionara y que el modelo pudiera procesar las imágenes.

El procedimiento que realizaba el sistema era el siguiente:

1. La cámara capturaba una imagen.
2. El modelo analizaba la imagen.
3. SenseCraft AI mostraba si correspondía a Person o Not a person.
4. Observábamos el porcentaje de confianza de la clasificación.

También encontramos una sección llamada **Device Logger**, donde aparecían registros del procesamiento del modelo.

En esta sección se mostraban tiempos de preprocesamiento e inferencia. Comprendimos que el preprocesamiento es la preparación de la imagen y que la inferencia es el momento en que el modelo analiza la imagen para obtener un resultado.

Estos procesos forman parte del funcionamiento de los modelos de TinyML [ [1] ](#ref1).

<img width="1600" height="857" alt="image" src="https://github.com/user-attachments/assets/9421e0f5-4ac8-4cd0-9de4-74cac2eb11c7" />

*Figura 3. Visualización de la cámara mediante SenseCraft AI y registros de procesamiento mostrados en Device Logger.*

### 4.4. Paso 4: Primera prueba de reconocimiento de personas

Después de comprobar que la cámara funcionaba, comenzamos a realizar las pruebas con nuestros compañeros.

En esta primera parte solamente queríamos verificar que el modelo pudiera identificar la presencia de una persona. Todavía no estábamos utilizando la configuración GPIO para encender el LED.

Para realizar las pruebas participaron nuestros compañeros **Joseph Lombardi Quispe y Yoichi Palacios Tanaka**.

Cada uno se colocó frente a la cámara mientras observábamos en la computadora la respuesta del modelo.

#### 4.4.1. Prueba con Joseph Lombardi

Primero, Joseph Lombardi se colocó frente a la cámara de la XIAO ESP32S3 Sense.

Mientras la cámara lo enfocaba, observamos la pantalla de SenseCraft AI para comprobar cómo respondía el modelo.

Lo que buscábamos era que el modelo reconociera la presencia de nuestro compañero y mostrara la categoría **Person**.

Esta prueba nos permitió observar directamente cómo se realiza el reconocimiento de una persona utilizando una cámara y un modelo de inteligencia artificial.

<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/8076e6f7-7451-4c89-adfd-63c16d762759" />

*Figura 4. Joseph Lombardi realizando la primera prueba de reconocimiento frente a la cámara de la XIAO ESP32S3 Sense.*

#### 4.4.2. Prueba con Yoichi Palacios

Después realizamos la misma prueba con Yoichi Palacios.

En este caso, nuestro compañero se colocó frente a la cámara para comprobar si el modelo también podía reconocer la presencia de otra persona.

Mantuvimos el mismo modelo y observamos los resultados que aparecían en SenseCraft AI.

La finalidad era repetir la prueba con un participante diferente y verificar el funcionamiento del reconocimiento.

<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/5bf2df1e-3f2a-4788-9e86-7c0a6f385272" />

*Figura 5. Yoichi Palacios realizando la prueba de reconocimiento mediante el modelo Person Classification.*

**Tabla 4. Resumen de las pruebas realizadas**

| Participante | Actividad | Objetivo |
|---|---|---|
| Joseph Lombardi | Se colocó frente a la cámara. | Comprobar que el modelo detectara una persona. |
| Yoichi Palacios | Repitió la prueba de reconocimiento. | Verificar el funcionamiento con otra persona. |

*Fuente: Elaboración propia.*


### 4.5. Paso 5: Observación y comparación de los porcentajes de confianza

Después de realizar las pruebas con nuestros compañeros Joseph Lombardi y Yoichi Palacios Tanaka, observamos los porcentajes de confianza que aparecían en SenseCraft AI.

Durante esta primera etapa utilizamos el modelo **Person Classification**, manteniendo la misma configuración para ambos compañeros.

Antes de realizar las pruebas, observamos que el parámetro **Confidence Threshold** estaba configurado en **50 %**. Este valor se mantuvo durante ambas pruebas, ya que no realizamos ninguna modificación en la configuración del modelo.

Este umbral sirve como referencia mínima de confianza para las detecciones. Sin embargo, no significa que todas las imágenes deban obtener exactamente un 50 %, porque el modelo calcula un porcentaje diferente según la imagen que analiza.

Al realizar las pruebas, obtuvimos los siguientes resultados:

**Tabla 5. Comparación de los resultados de reconocimiento de personas**

| Participante | Clasificación | Umbral configurado | Confianza obtenida |
|---|---|---:|---:|
| Joseph Lombardi | Person | 50 % | 100 % |
| Yoichi Palacios Tanaka | Person | 50 % | 89 % |

*Fuente: Elaboración propia a partir de las pruebas realizadas en SenseCraft AI durante el taller.*

Como podemos observar, el modelo reconoció a nuestros dos compañeros como personas, aunque los porcentajes de confianza fueron diferentes.

En el caso de **Joseph Lombardi**, obtuvimos un **100 % de confianza**, lo que significa que el modelo mostró su máxima puntuación para la categoría Person en la imagen analizada.

Por otro lado, **Yoichi Palacios Tanaka** obtuvo un **89 % de confianza**. Aunque este resultado fue menor, también superó el umbral del 50 % y el modelo lo clasificó como persona.

Esto nos permitió comprender que, aun utilizando el mismo modelo y sin cambiar su configuración, los porcentajes de confianza pueden variar dependiendo de la imagen capturada.

Esta diferencia podría estar relacionada con la iluminación, la posición de los participantes frente a la cámara o las características de cada imagen. Sin embargo, no realizamos pruebas específicas para determinar qué factor produjo la diferencia.

#### 4.5.1. Resultado de reconocimiento de Joseph Lombardi

En la siguiente captura podemos observar el resultado obtenido durante la prueba con Joseph Lombardi.

El modelo mostró una confianza del **100 %** para la categoría Person, superando el umbral del 50 % que se encontraba configurado.

<img width="1600" height="847" alt="image" src="https://github.com/user-attachments/assets/59631cc6-debe-4e79-a64f-5efbd474143e" />

*Figura 6. Resultado del reconocimiento de Joseph Lombardi mediante SenseCraft AI, con un 100 % de confianza para la categoría Person.*

#### 4.5.2. Resultado de reconocimiento de Yoichi Palacios Tanaka

Después realizamos la prueba con Yoichi Palacios Tanaka, manteniendo el mismo modelo y la configuración inicial.

En esta ocasión, el modelo mostró una confianza del **89 %** para la categoría Person.

Aunque fue un porcentaje diferente al de la primera prueba, también superó el umbral establecido y permitió reconocer a nuestro compañero como persona.

<img width="1600" height="847" alt="image" src="https://github.com/user-attachments/assets/ec6688e4-7460-49b4-b1d6-22bd1b06dac4" />

*Figura 7. Resultado del reconocimiento de Yoichi Palacios Tanaka mediante SenseCraft AI, con un 89 % de confianza para la categoría Person.*

#### 4.5.3. ¿Qué aprendimos de los resultados?

Con estas pruebas comprendimos que el porcentaje de confianza puede cambiar entre una imagen y otra, incluso cuando utilizamos el mismo modelo y mantenemos la misma configuración.

También aprendimos a diferenciar el **umbral de confianza**, que en esta primera etapa fue del 50 %, de la **confianza obtenida en cada reconocimiento**, que fue del 100 % y 89 %.

Finalmente, después de comprobar el reconocimiento de personas, pasamos a la segunda etapa del taller, donde utilizamos la opción **GPIO**.

En esta nueva etapa configuramos un umbral del **60 %**, para que el LED se encendiera cuando el modelo reconociera una persona con una confianza superior a dicho valor.


### 4.6. Paso 6: Configuración de GPIO para encender el LED

Después de comprobar que el modelo podía reconocer personas, pasamos a la segunda parte del taller, donde utilizamos **GPIO**.

GPIO significa *General Purpose Input/Output*, que en español se refiere a entradas y salidas de propósito general.

Estas conexiones permiten que una placa pueda recibir información o controlar componentes electrónicos [ [2] ](#ref2).

En nuestro caso, utilizamos esta función para encender el LED cuando la cámara reconociera una persona.

Para hacerlo, ingresamos a la opción:

**Output → GPIO**

Dentro de esta sección configuramos los siguientes parámetros:

**Tabla 6. Parámetros utilizados en la configuración GPIO**

| Parámetro | Valor seleccionado | ¿Para qué sirve? |
|---|---|---|
| Object | Person | Indica que queremos detectar una persona. |
| GPIO | LED | Selecciona el LED que vamos a controlar. |
| Condition | Greater than | Indica que el valor debe ser mayor al establecido. |
| Confidence | 60 | Establece el porcentaje de confianza necesario. |
| Default Status | LED off | Mantiene el LED apagado cuando no se cumple la condición. |
| Active Status | LED on | Enciende el LED cuando se cumple la condición. |

*Fuente: Configuración realizada durante el taller en SenseCraft AI.*

#### ¿Por qué seleccionamos estos valores?

**Object: Person**

Seleccionamos Person porque nuestro objetivo era que el LED respondiera cuando el modelo reconociera una persona frente a la cámara.

**GPIO: LED**

Elegimos LED porque queríamos observar una respuesta física del dispositivo. Así, además de ver la clasificación en la computadora, podíamos comprobar el funcionamiento mediante una luz.

**Condition: Greater than**

Seleccionamos Greater than, que significa "mayor que", porque necesitábamos establecer una condición para activar el LED.

**Confidence: 60**

Colocamos el valor de 60 para indicar que el modelo debía reconocer una persona con una confianza superior al 60 %.

Por ejemplo, si el modelo mostraba una confianza del 80 %, el LED debía encenderse porque ese valor supera el límite configurado.

**Default Status: LED off**

Seleccionamos esta opción para que el LED estuviera apagado cuando no se cumpliera la condición.

**Active Status: LED on**

Elegimos esta opción para que el LED se encendiera cuando el modelo detectara una persona y superara el porcentaje establecido.

De esta manera, logramos relacionar el resultado del reconocimiento con una acción física de la placa.

<img width="1600" height="856" alt="image" src="https://github.com/user-attachments/assets/c379c7c6-bbaa-4a18-b723-db9c0b1dc5b7" />


*Figura 8. Configuración de GPIO en SenseCraft AI, donde seleccionamos Person, LED y un porcentaje de confianza mayor al 60 %.*

### 4.7. Paso 7: Comprensión de la condición de activación

Después de realizar la configuración, analizamos cómo debía funcionar el LED.

La condición que establecimos fue la siguiente:

**Si la confianza de Person es mayor al 60 %, el LED se enciende.**

**Si la confianza no supera el 60 %, el LED permanece apagado.**

Para comprenderlo mejor, podemos observar algunos ejemplos:

**Tabla 7. Ejemplos del funcionamiento esperado del LED**

| Confianza de Person | ¿Supera el 60 %? | Estado esperado del LED |
|---|---|---|
| 100 % | Sí | Encendido |
| 80 % | Sí | Encendido |
| 60 % | No | Apagado |
| 40 % | No | Apagado |

*Nota: Los valores de 80 %, 60 % y 40 % son ejemplos para explicar la condición. No corresponden a mediciones adicionales del laboratorio.*

Esta parte fue importante porque nos permitió entender que el LED no se encendía simplemente por conectar la placa, sino porque debía cumplirse la condición que habíamos configurado.

También comprendimos que el resultado de un modelo de inteligencia artificial puede utilizarse para controlar una acción en un dispositivo electrónico.

### 4.8. Paso 8: Prueba del LED con Joseph Lombardi

Una vez que terminamos de configurar el GPIO, volvimos a realizar pruebas con nuestros compañeros.

Esta vez no solamente queríamos que el modelo reconociera una persona, sino que también encendiera el LED cuando se cumpliera la condición establecida.

Primero realizamos la prueba con Joseph Lombardi.

Nuestro compañero se colocó frente a la cámara y observamos la respuesta del modelo en SenseCraft AI.

Cuando el modelo identificó a la persona con una confianza superior al 60 %, pudimos observar que el LED se encendía.

Para registrar lo ocurrido tomamos dos fotografías.

En la primera fotografía se muestra a nuestro compañero realizando la prueba mientras utilizábamos la computadora para observar el funcionamiento del modelo.

<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/9bb9326e-4167-4c0d-89ac-5de928ca341b" />

*Figura 9. Joseph Lombardi realizando la prueba de reconocimiento con la configuración GPIO activada.*

En la segunda fotografía enfocamos directamente el dispositivo para mostrar que el LED se encontraba encendido.

Esta imagen nos sirvió como evidencia de que la configuración estaba funcionando y que la placa respondía al reconocimiento de una persona.

<img width="1600" height="1202" alt="image" src="https://github.com/user-attachments/assets/1976b2cb-20a6-4c49-b9ec-526cb03a9e47" />

*Figura 10. Evidencia del LED encendido durante la prueba de reconocimiento de Joseph Lombardi.*

### 4.9. Paso 9: Prueba del LED con Yoichi Palacios

Después de terminar la prueba con Joseph Lombardi, repetimos el procedimiento con Yoichi Palacios.

Mantuvimos la configuración GPIO que habíamos establecido anteriormente, es decir, Person con una confianza mayor al 60 %.

Yoichi se colocó frente a la cámara y observamos cómo respondía el modelo.

Al reconocer su presencia y cumplirse la condición, el LED se encendió.

Con esta segunda prueba pudimos comprobar que la configuración también funcionaba con otro participante y que no era necesario modificar los valores para repetir el procedimiento.

De igual manera, registramos dos fotografías.

En la primera se observa a nuestro compañero realizando la prueba frente a la cámara.

<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/916a5f0b-f587-485b-9362-aae7b5ad642d" />


*Figura 11. Yoichi Palacios realizando la prueba de reconocimiento con la configuración GPIO.*

En la segunda fotografía se muestra el LED encendido, lo que permitió registrar la respuesta física del dispositivo.

<img width="1600" height="1206" alt="image" src="https://github.com/user-attachments/assets/3fe710a8-b80a-4b86-a06f-835d1f614351" />


*Figura 12. Evidencia del LED encendido durante la prueba de reconocimiento de Yoichi Palacios.*

### 4.10. Paso 10: Registro final de la práctica

Al finalizar las pruebas, reunimos las capturas de pantalla y las fotografías obtenidas durante el laboratorio.

Estas evidencias nos permitieron mostrar cada parte del procedimiento: desde la selección del modelo hasta las pruebas de reconocimiento y el encendido del LED.

De esta manera, pudimos documentar el trabajo realizado y explicar los resultados observados.

![Figura 12. Evidencia complementaria](imagenes/figura-12-evidencia-adicional.jpg)

*Figura 12. Evidencia complementaria del desarrollo del taller utilizando SenseCraft AI y la placa XIAO ESP32S3 Sense.*

## 5. Resultados y análisis

### 5.1. Resultados obtenidos

Durante el taller conseguimos realizar las actividades relacionadas con la clasificación de personas y la activación del LED.

Para presentar de manera más ordenada lo que hicimos, elaboramos el siguiente resumen.

**Tabla 8. Resumen de los resultados del laboratorio**

| Etapa | Actividad realizada | Resultado observado |
|---|---|---|
| 1 | Selección del modelo | Seleccionamos Person Classification. |
| 2 | Conexión del dispositivo | Preparamos la placa XIAO ESP32S3 Sense. |
| 3 | Inicio de la cámara | Pudimos visualizar las imágenes en SenseCraft AI. |
| 4 | Prueba con Joseph Lombardi | Realizamos el reconocimiento de una persona. |
| 5 | Prueba con Yoichi Palacios | Repetimos el reconocimiento con otro compañero. |
| 6 | Resultados de confianza | Obtuvimos una captura con 100 % para Person. |
| 7 | Configuración GPIO | Establecimos una confianza mayor al 60 %. |
| 8 | Prueba del LED con Joseph | Observamos que el LED se encendió. |
| 9 | Prueba del LED con Yoichi | Comprobamos nuevamente el encendido del LED. |

*Fuente: Elaboración propia a partir de las pruebas realizadas durante el taller.*

### 5.2. Análisis del reconocimiento de personas

En la primera parte del laboratorio comprobamos que el modelo Person Classification podía utilizar la cámara para identificar la presencia de nuestros compañeros.

Uno de los resultados más importantes fue observar una confianza del 100 % para la categoría Person en una de las capturas.

Esto nos ayudó a comprender cómo el modelo analiza una imagen y presenta un resultado mediante porcentajes.

También entendimos que estos porcentajes corresponden a la confianza del modelo y que no necesariamente indican que siempre reconocerá correctamente todas las imágenes.

### 5.3. Análisis de la activación del LED

En la segunda parte aprendimos a utilizar los resultados del modelo para controlar una salida GPIO.

Al configurar el LED para que se encendiera cuando la confianza de Person fuera mayor al 60 %, pudimos observar cómo una clasificación realizada por inteligencia artificial producía una respuesta física.

Durante las pruebas con Joseph y Yoichi observamos el encendido del LED, lo que nos permitió comprobar el funcionamiento de la configuración.

Esta fue una de las partes más interesantes del taller, porque no solamente vimos un resultado en la computadora, sino también una acción realizada por la placa.

### 5.4. Limitaciones de las pruebas

Durante el laboratorio solamente realizamos pruebas de reconocimiento con personas.

Aunque el modelo también incluye la categoría Not a person, no realizamos pruebas utilizando perros u otros objetos.

Por este motivo, no podemos asegurar cómo habría respondido el sistema frente a esos casos, ya que no los comprobamos durante la práctica.

Además, nuestras pruebas se realizaron con dos participantes, por lo que sería interesante realizar nuevas pruebas con más personas y diferentes condiciones de iluminación.

## 6. Conclusiones

1. Durante el taller aprendimos a utilizar la plataforma SenseCraft AI y la placa XIAO ESP32S3 Sense para ejecutar un modelo de inteligencia artificial. Esto nos permitió conocer de manera práctica cómo funciona TinyML y cómo puede utilizarse para reconocer personas mediante una cámara.

2. Al realizar las pruebas con nuestros compañeros Joseph Lombardi y Yoichi Palacios, pudimos observar cómo el modelo Person Classification analizaba las imágenes. En una de las capturas obtuvimos un 100 % de confianza para la categoría Person, lo que nos permitió comprender mejor los resultados mostrados por la plataforma.

3. También aprendimos a configurar GPIO para controlar el LED de la placa. Para ello, establecimos que el LED se encendiera cuando la confianza de reconocimiento de una persona fuera mayor al 60 %, comprendiendo cómo se utilizan las condiciones para activar una salida.

4. Durante las pruebas con ambos compañeros observamos que el LED se encendía cuando se cumplía la condición configurada. Esto nos permitió comprobar que el reconocimiento realizado por el modelo podía utilizarse para controlar un componente electrónico.

5. Finalmente, el taller nos ayudó a comprender mejor la relación entre inteligencia artificial y electrónica. Consideramos que esta experiencia fue útil porque pudimos aplicar lo aprendido mediante pruebas reales y observar directamente los resultados obtenidos.

## 7. Referencias bibliográficas

<a id="ref1"></a>

[1] Universidad Peruana Cayetano Heredia, *TinyML con XIAO ESP32S3 Sense: Laboratorio con SenseCraft*, material de clase, Lima, Perú, 2026.

<a id="ref2"></a>

[2] Seeed Studio, "XIAO ESP32S3 Sense," *Seeed Studio Wiki*. [En línea]. Disponible en: https://wiki.seeedstudio.com/XIAO_ESP32S3_Sense/. [Accedido: 13-oct-2026].

<a id="ref3"></a>

[3] Seeed Studio, "SenseCraft AI," *SenseCraft*. [En línea]. Disponible en: https://sensecraft.seeed.cc/. [Accedido: 13-oct-2026].


