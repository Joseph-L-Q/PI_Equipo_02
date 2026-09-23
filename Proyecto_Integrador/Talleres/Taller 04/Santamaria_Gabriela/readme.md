# Taller 4: Redes Neuronales: CNN, Keras y Perceptrón

## Introducción

En este taller se trabajaron tres métodos relacionados con redes neuronales: las Redes Neuronales Convolucionales (CNN), el framework Keras y el Perceptrón.

Cada método permite resolver diferentes tipos de problemas. Las CNN son utilizadas principalmente para trabajar con imágenes, Keras facilita la creación y entrenamiento de modelos de aprendizaje profundo, mientras que el Perceptrón permite comprender los conceptos básicos de una red neuronal.

Durante el desarrollo del taller se realizaron diferentes pruebas con estos métodos, analizando cómo aprenden a partir de los datos, cómo evaluar sus resultados y qué técnica sería más adecuada para aplicarla en un proyecto real.

---

# 1. Redes Neuronales Convolucionales (CNN)

Las Redes Neuronales Convolucionales (CNN, *Convolutional Neural Networks*) son modelos de aprendizaje profundo utilizados principalmente para analizar imágenes.

Su principal característica es que pueden aprender automáticamente características visuales importantes de una imagen, como bordes, texturas y formas, sin necesidad de definir manualmente cada característica que debe buscar el modelo. <a href="#ref1">[1]</a>

En una CNN, la imagen pasa por diferentes capas que permiten extraer información progresivamente. Las primeras capas suelen identificar características simples, mientras que las capas posteriores combinan esta información para reconocer patrones más complejos.

---

## Implementación de una CNN utilizando PyTorch

Durante el taller se implementó una CNN utilizando PyTorch <a href="#ref1">[1]</a>, utilizando el dataset **TrashNet** <a href="#ref2">[2]</a>.

El objetivo del modelo fue realizar una clasificación binaria utilizando imágenes de residuos, específicamente:

- Vidrio.
- Plástico.

Para ello, las imágenes fueron organizadas en conjuntos de:

- Entrenamiento.
- Validación.
- Prueba.

Esta separación permitió entrenar el modelo y posteriormente evaluar su comportamiento utilizando imágenes que no fueron utilizadas durante el aprendizaje.

---

## Datos utilizados para el entrenamiento

<img width="452" height="662" alt="image" src="https://github.com/user-attachments/assets/4a69109c-6d63-4550-899d-ca8c76cbcee8" />

<img width="1007" height="680" alt="image" src="https://github.com/user-attachments/assets/d4d7d84a-545d-43f9-93d9-1ad208feb016" />


> **Fig. 1. Ejemplos de imágenes utilizadas del dataset TrashNet.**

Las imágenes mostradas corresponden a los datos utilizados para entrenar la red neuronal. A partir de estas muestras, la CNN aprende características visuales que permiten diferenciar entre las categorías vidrio y plástico.

---

# Construcción y entrenamiento del modelo

Para construir la CNN se utilizaron diferentes capas encargadas de extraer características de las imágenes y realizar la clasificación final.

Durante el entrenamiento, la red neuronal ajusta sus parámetros internos con el objetivo de reducir el error entre la predicción realizada y la categoría real de cada imagen.

Para evaluar el desempeño del modelo se utilizaron diferentes métricas:

- Accuracy.
- ROC-AUC.
- Precision.
- Recall.
- F1-score.
- Matriz de confusión.

Estas métricas permiten analizar no solamente la cantidad de predicciones correctas, sino también conocer qué tan bien el modelo diferencia las categorías evaluadas.

---

## Proceso de entrenamiento del modelo CNN

<img width="1112" height="660" alt="image" src="https://github.com/user-attachments/assets/49e97ad8-e22d-419f-974c-9bc7da1207e8" />


> **Fig. 2. Proceso de entrenamiento del modelo CNN durante las diferentes épocas.**

Durante esta etapa el modelo aprende progresivamente las características presentes en las imágenes. La información obtenida durante el entrenamiento permite ajustar los pesos internos de la red para mejorar la clasificación.

---

# Resultados obtenidos con la CNN

Luego del entrenamiento, el modelo logró aprender características visuales que permitieron diferenciar las categorías evaluadas.

Los resultados obtenidos fueron:

- **Accuracy aproximado: 63.27%**
- **ROC-AUC aproximado: 0.67 - 0.69**

Estos resultados muestran que la CNN pudo identificar patrones en las imágenes; sin embargo, el desempeño todavía puede mejorar utilizando técnicas adicionales como *data augmentation* y *transfer learning*. :contentReference[oaicite:2]{index=2}

---

## Evaluación del modelo

<img width="740" height="647" alt="image" src="https://github.com/user-attachments/assets/0ffc5bc2-c81f-483a-a08b-25886acfbdd9" />


> **Fig. 3. Resultados obtenidos durante la evaluación del modelo CNN.**

Las métricas permiten observar el comportamiento del modelo durante el entrenamiento y validación. La reducción de la pérdida indica que la red aprende características de los datos, mientras que las métricas de evaluación permiten analizar su desempeño con imágenes nuevas.

---

## Matriz de confusión

<img width="410" height="492" alt="image" src="https://github.com/user-attachments/assets/3ce36747-e537-4961-b17f-21e235616b63" />


> **Fig. 4. Matriz de confusión obtenida durante la evaluación del modelo CNN.**

La matriz de confusión permite observar los aciertos y errores realizados por el modelo al clasificar las imágenes. Esto ayuda a identificar qué categorías presentan mayor dificultad durante la predicción.

---

# Data Augmentation y Transfer Learning

Después de entrenar una CNN desde cero, se probaron diferentes técnicas para mejorar el desempeño del modelo. Estas técnicas fueron **Data Augmentation** y **Transfer Learning**, las cuales permiten mejorar la capacidad de aprendizaje cuando se cuenta con una cantidad limitada de datos.

---

# Data Augmentation

El aumento de datos (*Data Augmentation*) es una técnica que permite generar nuevas variaciones de las imágenes originales mediante pequeñas transformaciones.

El objetivo de esta técnica es aumentar la cantidad de ejemplos disponibles para el modelo y ayudar a que pueda aprender características más variadas de las imágenes.

Durante la práctica se aplicaron transformaciones sobre las imágenes, como:

- Rotaciones.
- Desplazamientos.
- Variaciones controladas de las imágenes originales.

Estas modificaciones permiten que la red neuronal no memorice únicamente las imágenes utilizadas durante el entrenamiento, sino que aprenda características más generales.

Sin embargo, es importante aplicar transformaciones que tengan sentido para el problema. Una transformación incorrecta podría generar imágenes que no representen situaciones reales y afectar el aprendizaje del modelo.

---

## Aplicación de Data Augmentation

<img width="867" height="157" alt="image" src="https://github.com/user-attachments/assets/1d69f269-8815-4274-ba5d-e76b4911a929" />


> **Fig. 5. Comparación rápida mediante Data Augmentation.**

Las imágenes modificadas permiten aumentar la variedad del conjunto de entrenamiento. Esto ayuda al modelo a mejorar su capacidad para reconocer patrones visuales bajo diferentes condiciones.

---

# Transfer Learning

El Transfer Learning consiste en utilizar un modelo que ya fue entrenado previamente con una gran cantidad de imágenes y adaptarlo a un nuevo problema.

En lugar de entrenar una red neuronal completamente desde cero, se aprovechan los conocimientos aprendidos por un modelo existente y se ajustan sus capas finales para una nueva tarea.

Durante el taller se utilizó esta técnica para comparar el desempeño de una CNN creada desde cero con un modelo previamente entrenado.

Esta estrategia resulta importante porque permite obtener mejores resultados cuando no se dispone de una gran cantidad de datos propios.

---

## Fine-tuning

Después de utilizar Transfer Learning, se realizó un proceso de *fine-tuning*.

Esta técnica consiste en descongelar algunas capas del modelo previamente entrenado para permitir que puedan adaptarse mejor al nuevo conjunto de imágenes.

El proceso realizado fue:

1. Utilizar un modelo previamente entrenado.
2. Entrenar inicialmente las capas finales.
3. Descongelar algunas capas superiores.
4. Ajustar nuevamente el modelo con las nuevas imágenes.

Esto permite que la red conserve características generales aprendidas previamente y, al mismo tiempo, pueda especializarse en el nuevo problema.

---

## Comparación con la CNN desde cero

A partir de las pruebas realizadas, se pudo observar que Transfer Learning permite aprovechar mejor la información aprendida previamente por el modelo.

Mientras que una CNN entrenada desde cero necesita una mayor cantidad de datos para aprender características visuales, un modelo preentrenado puede adaptarse más rápidamente a una nueva clasificación.

Por esta razón, para proyectos donde inicialmente existen pocos datos disponibles, Transfer Learning representa una alternativa importante.

---

# Grad-CAM

Además del entrenamiento del modelo, se trabajó una técnica de interpretación llamada **Grad-CAM** (*Gradient-weighted Class Activation Mapping*).

Esta técnica permite visualizar las zonas de una imagen que tuvieron mayor influencia en la decisión tomada por la red neuronal.

A diferencia de una predicción tradicional, donde solamente se obtiene una clase final, Grad-CAM permite observar qué partes de la imagen fueron consideradas importantes por el modelo.

---

## Interpretación de Grad-CAM

<img width="847" height="315" alt="image" src="https://github.com/user-attachments/assets/bcbd4af1-f357-4ea6-af88-4311a90d846d" />


> **Fig. 6. Mapa de calor generado mediante Grad-CAM para interpretar la predicción del modelo.**

El mapa de calor permite observar las regiones de la imagen donde la CNN concentró mayor atención. Las zonas con mayor intensidad representan las áreas que tuvieron mayor influencia durante la clasificación.

Esta herramienta es importante porque permite verificar si el modelo está tomando decisiones utilizando información adecuada de la imagen y no elementos externos como el fondo.

---
# 2. Implementación utilizando Keras

Keras es un framework de alto nivel utilizado para construir, entrenar y evaluar modelos de aprendizaje profundo.

A diferencia de una arquitectura específica como CNN o Perceptrón, Keras funciona como una herramienta que facilita la creación de redes neuronales mediante una estructura más sencilla y organizada.

Durante el desarrollo del taller se utilizó Keras para implementar un modelo de clasificación utilizando el dataset **IMDB**, donde el objetivo fue analizar reseñas de películas y clasificarlas según el sentimiento expresado en el texto.

El modelo buscó determinar si una reseña correspondía a una opinión positiva o negativa mediante el aprendizaje de patrones presentes en los datos.

---
## Preparación del dataset IMDB

Para entrenar el modelo se utilizó el dataset IMDB, el cual contiene reseñas de películas etiquetadas según dos categorías:

- Opinión positiva.
- Opinión negativa.

Antes de ingresar los datos al modelo fue necesario realizar un proceso de preparación, debido a que las redes neuronales no trabajan directamente con texto.

Por ello, las reseñas fueron transformadas en una representación numérica que pueda ser procesada por la red neuronal.

---
## Construcción de la red neuronal utilizando Keras

Para desarrollar el modelo se utilizaron diferentes capas neuronales encargadas de procesar la información de entrada y generar una clasificación final.

La estructura del modelo permitió que la red aprenda relaciones entre las palabras presentes en las reseñas y pueda identificar patrones asociados con sentimientos positivos o negativos.

El flujo general del modelo fue:

Entrada de texto
↓
Procesamiento numérico
↓
Capas neuronales
↓
Clasificación positiva o negativa 

---

## Entrenamiento del modelo

Durante el entrenamiento, el modelo ajustó sus parámetros internos utilizando los datos proporcionados.

El objetivo fue minimizar el error entre la predicción realizada por la red neuronal y la categoría real de cada reseña.

Para evaluar el comportamiento del modelo se analizaron métricas de desempeño obtenidas durante las etapas de entrenamiento y validación.

<img width="535" height="517" alt="image" src="https://github.com/user-attachments/assets/c448551d-98d9-4558-a13b-9d18e299d847" />


> **Fig. 7. Evolución del entrenamiento del modelo desarrollado con Keras.**

La gráfica permite observar el comportamiento del modelo durante las épocas de entrenamiento. La diferencia entre los resultados de entrenamiento y validación ayuda a identificar si existe sobreajuste (*overfitting*) durante el aprendizaje.

---

## Análisis del sobreajuste

Durante el entrenamiento de una red neuronal es posible que el modelo aprenda demasiado los datos utilizados para entrenar y tenga dificultades para trabajar con datos nuevos.

Este comportamiento se conoce como sobreajuste (*overfitting*).

Para reducir este problema pueden aplicarse diferentes estrategias como:

- Aumentar la cantidad de datos.
- Utilizar técnicas de regularización.
- Aplicar Dropout.
- Ajustar la complejidad del modelo.

 ---

  ## Aprendizaje obtenido

El desarrollo de este modelo permitió comprender cómo utilizar un framework especializado para construir redes neuronales de una manera más sencilla.

Keras facilita la implementación de diferentes modelos, permitiendo realizar pruebas rápidas y analizar el comportamiento de una red neuronal durante su entrenamiento.

---
# 3. Perceptrón

El Perceptrón es uno de los modelos más simples dentro de las redes neuronales artificiales y permite comprender los conceptos básicos de aprendizaje automático.

Este modelo recibe valores de entrada, les asigna diferentes pesos y, mediante una función de activación, genera una salida que permite realizar una clasificación.

Aunque actualmente existen modelos mucho más complejos, el Perceptrón es importante porque representa uno de los primeros acercamientos al funcionamiento de una red neuronal.

---

## Funcionamiento del Perceptrón

El funcionamiento del Perceptrón se basa en realizar una combinación entre las entradas y los pesos asignados.

El proceso general es:

Datos de entrada
↓
Multiplicación por pesos
↓
Suma de valores
↓
Función de activación
↓
Salida del modelo


Durante el entrenamiento, el modelo ajusta sus pesos con el objetivo de reducir los errores entre la salida obtenida y la salida esperada.

---

# Implementación del Perceptrón

Durante el desarrollo del taller se implementó un Perceptrón para analizar problemas de clasificación utilizando compuertas lógicas.

Se evaluaron los siguientes casos:

- AND.
- OR.
- XOR.

Estos ejemplos permiten comprender las capacidades y limitaciones de un Perceptrón simple.

---

# Clasificación de compuertas lógicas AND y OR

Las compuertas AND y OR pueden resolverse utilizando un Perceptrón debido a que sus datos pueden separarse mediante una frontera lineal.

Esto significa que existe una línea que permite dividir correctamente las diferentes clases.

---

<img width="442" height="436" alt="image" src="https://github.com/user-attachments/assets/498bd0b8-7341-4a4e-bdf7-40c36d46359b" />



> **Fig. 8. Clasificación realizada por el Perceptrón para las compuertas AND y OR.**

Los resultados muestran que el Perceptrón puede resolver problemas donde existe una separación lineal entre las categorías. En estos casos, el modelo logra encontrar una combinación adecuada de pesos para realizar la clasificación.

---

# Limitación del Perceptrón: Caso XOR

La compuerta XOR representa una limitación importante del Perceptrón simple.

A diferencia de AND y OR, los datos de XOR no pueden separarse utilizando una única línea, por lo que un Perceptrón básico no puede resolver correctamente este problema.

Para solucionar este tipo de problemas es necesario utilizar redes neuronales con más capas, conocidas como redes multicapa.

---

<img width="432" height="440" alt="image" src="https://github.com/user-attachments/assets/b54b914a-3566-4a70-ab1f-7012bf4f658b" />


> **Fig. 9. Limitación del Perceptrón simple mediante la compuerta XOR.**

El caso XOR demuestra que un Perceptrón de una sola capa tiene limitaciones para resolver problemas donde las clases no presentan una separación lineal.

---

# Ventajas y limitaciones del Perceptrón

## Ventajas

- Es un modelo sencillo de comprender.
- Permite conocer los fundamentos de una red neuronal.
- Tiene bajo costo computacional.

## Limitaciones

- Solo funciona correctamente con problemas linealmente separables.
- No puede extraer características complejas.
- No es adecuado para trabajar directamente con imágenes.

---
# 4. Comparación y selección del método para LanternGuard

Después de analizar los tres métodos trabajados durante el taller: CNN, Keras y Perceptrón, se realizó una comparación considerando las características del proyecto LanternGuard.

El objetivo del proyecto es desarrollar un sistema capaz de detectar niveles de bioincrustación en linternas utilizadas para el cultivo de concha de abanico mediante el análisis de imágenes.

Por esta razón, se evaluó qué método presenta mejores características para trabajar con información visual.

---

# Comparación de los métodos estudiados

| Método | Características principales | Posible aplicación en LanternGuard |
|---|---|---|
| CNN | Red neuronal especializada en procesamiento de imágenes. Permite aprender características visuales como formas, texturas y patrones. | Puede utilizarse para analizar imágenes de las linternas y detectar diferentes niveles de bioincrustación. |
| Keras | Framework que facilita la creación, entrenamiento y evaluación de modelos de aprendizaje profundo. | Puede utilizarse como herramienta para implementar y entrenar la red neuronal del proyecto. |
| Perceptrón | Modelo neuronal básico utilizado para problemas sencillos de clasificación. Presenta limitaciones cuando los datos no son separables linealmente. | No sería adecuado para analizar imágenes debido a la complejidad de la información visual. |

---

# Método seleccionado para LanternGuard

Después de analizar las características de cada método, se considera que una **Red Neuronal Convolucional (CNN)** sería la alternativa más adecuada para implementar en LanternGuard.

La razón principal es que el proyecto trabaja con imágenes obtenidas mediante cámaras, donde la información importante se encuentra en características visuales como:

- Cambios de textura.
- Formas de los organismos adheridos.
- Distribución de la bioincrustación sobre la superficie de la linterna.

Una CNN tiene la capacidad de aprender automáticamente estos patrones y utilizarlos para realizar una clasificación.

---

# Propuesta de clasificación para LanternGuard

El modelo podría entrenarse para clasificar diferentes niveles de bioincrustación, por ejemplo:

| Categoría | Descripción |
|---|---|
| Normal | Linterna con poca o ninguna presencia de bioincrustación. |
| Advertencia | Presencia moderada de organismos adheridos que requiere seguimiento. |
| Crítico | Alta presencia de bioincrustación que podría afectar el cultivo. |

Esta clasificación permitiría generar información útil para apoyar la toma de decisiones del acuicultor.

---

# Uso de Transfer Learning en LanternGuard

Una de las principales dificultades al desarrollar el proyecto sería la cantidad inicial de imágenes disponibles para entrenar el modelo.

Crear una CNN desde cero requiere una gran cantidad de datos para obtener buenos resultados. Por esta razón, una alternativa sería utilizar **Transfer Learning**.

Esta técnica permitiría utilizar un modelo previamente entrenado con una gran cantidad de imágenes y adaptarlo posteriormente utilizando imágenes propias obtenidas de las linternas de cultivo.

Entre sus ventajas se encuentran:

- Menor tiempo de entrenamiento.
- Mejor aprovechamiento de datos limitados.
- Mayor capacidad de adaptación al nuevo problema.

---

# Propuesta general del sistema LanternGuard

El funcionamiento planteado para el sistema sería:
┌─────────────────────────┐
│ 📷 Captura de imagen    │
│ Cámara en linterna      │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 🖼 Preprocesamiento     │
│ Ajuste tamaño           │
│ Normalización           │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 🧠 CNN + Transfer       │
│ Learning                │
│ Extracción patrones     │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 🔍 Análisis visual      │
│ Texturas y formas       │
│ Bioincrustación         │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 📊 Clasificación        │
│ Normal                  │
│ Advertencia             │
│ Crítico                 │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 👨‍🌾 Resultado para      │
│ acuicultor              │
└─────────────────────────┘

> **Fig. 10. Flujo general de funcionamiento propuesto para el sistema LanternGuard.**

El diagrama representa el flujo planteado para el sistema LanternGuard. Primero se realiza la captura de imágenes de las linternas mediante cámaras, posteriormente la imagen pasa por una etapa de preprocesamiento para mejorar la calidad de los datos. Luego, el modelo CNN con Transfer Learning analiza las características visuales y finalmente clasifica el nivel de bioincrustación para generar información útil al acuicultor.

---

# Conclusiones

A partir del análisis realizado durante el taller se pudo comprender que cada método estudiado tiene diferentes aplicaciones dependiendo del tipo de problema.

El Perceptrón permitió comprender los fundamentos básicos del funcionamiento de una red neuronal, pero presenta limitaciones para problemas complejos debido a que solo trabaja adecuadamente con datos separables linealmente.

Keras facilitó la construcción y entrenamiento de modelos neuronales, funcionando como una herramienta de apoyo para implementar diferentes arquitecturas de aprendizaje profundo.

Finalmente, las Redes Neuronales Convolucionales presentan características adecuadas para LanternGuard debido a su capacidad para analizar imágenes y aprender patrones visuales.

Por ello, la propuesta planteada para el proyecto sería utilizar una **CNN implementada mediante un framework como Keras o PyTorch, complementada con Transfer Learning y Grad-CAM**, con el objetivo de detectar e interpretar niveles de bioincrustación en linternas de cultivo de concha de abanico.

---

# Referencias

<a id="ref1"></a>

[1] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, A. Desmaison, A. Kopf, E. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang y S. Chintala.

"PyTorch: An Imperative Style, High-Performance Deep Learning Library."

Advances in Neural Information Processing Systems 32 (NeurIPS), 2019.


<a id="ref2"></a>

[2] G. Thung y M. Yang.

"Classification of Trash for Recyclability Status."

CS229 Project Report, Stanford University, 2016.


<a id="ref3"></a>

[3] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh y D. Batra.

"Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization."

IEEE International Conference on Computer Vision (ICCV), 2017.


<a id="ref4"></a>

[4] F. Chollet.

"Keras."

2015.

https://keras.io/
