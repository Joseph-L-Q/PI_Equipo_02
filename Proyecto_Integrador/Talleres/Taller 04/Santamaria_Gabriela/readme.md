# Taller 4: Redes Neuronales: CNN, Keras y Perceptrón

En esta sesión aprendí a utilizar y entender tres formas de trabajar con redes neuronales: las Redes Neuronales Convolucionales (CNN) utilizando PyTorch  <a href="#ref2">[1]</a>, el framework Keras  <a href="#ref2">[4]</a> y el Perceptrón como la unidad más básica de una red neuronal. Cada uno tiene una forma diferente de trabajar, pero en conjunto me ayudaron a entender cómo una red neuronal puede aprender a partir de datos y cómo elegir una técnica dependiendo del problema.

---

## 1. CNN (Convolutional Neural Networks)

Las CNN son un tipo de red neuronal especialmente utilizada para trabajar con imágenes. En lugar de analizar cada píxel de manera independiente, utilizan filtros pequeños llamados *kernels* que recorren la imagen y buscan patrones en zonas cercanas, como bordes, texturas y formas.

### ¿Por qué sirve?

Las CNN son adecuadas cuando el problema consiste en reconocer patrones visuales en imágenes. En el taller trabajé este tipo de red utilizando PyTorch <a href="#ref2">[1]</a> y GPU. La GPU permite realizar muchas operaciones en paralelo, lo que facilita el entrenamiento de modelos que requieren una gran cantidad de cálculos.

### Partes principales

* **Convolución (Conv2D):** aplica filtros sobre la imagen para obtener mapas de características. Las primeras capas pueden detectar características sencillas, mientras que las capas posteriores pueden aprender patrones más complejos.

* **Activación (ReLU):** permite que la red aprenda relaciones no lineales. Su funcionamiento es sencillo: los valores negativos se convierten en 0 y los positivos se mantienen.

* **Pooling (MaxPool):** reduce el tamaño de la información obtenida, manteniendo las características más importantes. Esto ayuda a disminuir la cantidad de operaciones que debe realizar la red.

* **Capas fully-connected (densas):** reciben la información procesada por las capas anteriores y la utilizan para obtener la clasificación final.

> **Fig. 1.** Diagrama de la arquitectura de una CNN mostrando el flujo de una imagen a través de las capas de convolución, activación, pooling y capas densas.

Para practicar utilicé el dataset **TrashNet** <a href="#ref2">[2]</a> , que contiene imágenes de diferentes tipos de residuos. En el ejercicio trabajado se utilizaron imágenes de vidrio y plástico, clasificadas como 0 y 1, y divididas en conjuntos de entrenamiento, validación y prueba.

Primero construí una CNN básica desde cero, utilizando bloques de convolución, ReLU y pooling, y finalmente un clasificador. Para evaluar el modelo utilicé diferentes métricas, como *accuracy*, ROC-AUC, matriz de confusión, *precision*, *recall* y F1-score.

A partir de la época 4, el modelo empezó a mejorar su clasificación hasta alcanzar una exactitud de **63.27%** y un ROC-AUC entre **0.67 y 0.69**. Esto muestra que el modelo sí logró aprender características de las imágenes, aunque su desempeño todavía fue moderado. Por eso, no basta con construir una red neuronal, sino que también es necesario evaluar sus resultados y probar diferentes alternativas para mejorarla.

### Data augmentation y Transfer Learning

Después probé **data augmentation**, realizando pequeñas rotaciones y desplazamientos de las imágenes. Esta técnica permite generar variaciones de los datos disponibles y puede ayudar al modelo a aprender de diferentes formas de una misma imagen. También se debe tener cuidado con transformaciones que no tengan sentido para el problema, como algunos giros horizontales o verticales.

Luego utilicé **transfer learning**, que consiste en aprovechar un modelo que ya fue entrenado previamente con una gran cantidad de imágenes y adaptarlo a un nuevo problema. Primero entrené la última capa del modelo y posteriormente realicé *fine-tuning*, descongelando algunas de las últimas capas para que pudieran adaptarse al nuevo conjunto de datos.

En comparación con la CNN construida desde cero, el uso de transfer learning y *fine-tuning* permitió mejorar la capacidad del modelo para diferenciar entre vidrio y plástico.

> **Fig. 2.** Curvas de entrenamiento y métricas del modelo CNN desde cero y del modelo utilizando transfer learning y fine-tuning.

Esta parte es importante para mi proyecto porque **LanternGuard** probablemente no tendrá al inicio una gran cantidad de fotografías propias de linternas con diferentes niveles de bioincrustación. Por eso, una alternativa sería utilizar un modelo previamente entrenado y adaptarlo con fotografías propias del proyecto.

### Grad-CAM

También trabajé con una técnica de interpretabilidad llamada **Grad-CAM**, utilizando una versión simplificada de ResNet18 <a href="#ref2">[3]</a>. Esta técnica genera un mapa de calor sobre la imagen para mostrar las zonas que tuvieron mayor influencia en la decisión del modelo.

Las zonas con mayor intensidad indican que tuvieron una mayor influencia en la predicción, mientras que las zonas con menor intensidad tuvieron una menor influencia. Esto permite observar si el modelo realmente está prestando atención a las partes importantes de la imagen.

> **Fig. 3.** Mapa de calor generado mediante Grad-CAM, mostrando las regiones de la imagen que tuvieron mayor influencia en la predicción del modelo.

Para LanternGuard, esta herramienta podría ser útil para comprobar que la CNN está enfocándose en las zonas donde realmente aparece la bioincrustación de la linterna y no en elementos externos de la fotografía.

Finalmente, guardé el modelo entrenado para poder utilizarlo posteriormente sin necesidad de realizar nuevamente todo el entrenamiento.

---

## 2. Keras

Keras  <a href="#ref2">[4]</a>  es un framework que permite construir y entrenar redes neuronales de una manera más sencilla. En comparación con programar una red desde cero utilizando PyTorch, Keras facilita la definición de las capas, el entrenamiento y la evaluación del modelo.

### ¿Por qué sirve?

Keras permite realizar pruebas de diferentes modelos de manera más rápida y directa, por lo que puede ser práctico cuando se quiere desarrollar una aplicación que utilice redes neuronales sin tener que programar todos los componentes desde cero.

En el taller utilicé Keras para trabajar un problema de **clasificación binaria** utilizando el dataset **IMDB**  <a href="#ref2">[5]</a> , que contiene reseñas de películas que deben clasificarse como positivas o negativas.

Primero descargué los datos y utilicé el diccionario de palabras proporcionado por el dataset. Después apliqué **one-hot encoding** para transformar la información textual en una representación que pudiera ser procesada por la red neuronal. Finalmente, construí un modelo con dos capas ocultas de 16 neuronas y una capa de salida con una neurona.

> **Fig. 4.** Curva de pérdida del conjunto de entrenamiento y del conjunto de validación del modelo de Keras, donde se observa la aparición del sobreajuste.

Al analizar los resultados observé que el error de validación dejaba de disminuir mientras el modelo continuaba aprendiendo los datos de entrenamiento. Esto es una señal de **sobreajuste (*overfitting*)**, porque el modelo puede aprender demasiado los datos utilizados durante el entrenamiento y tener dificultades para trabajar con datos nuevos.

El modelo terminó con un error de aproximadamente **0.6** y una exactitud de **86.1%**.

Después comparé el modelo con uno más pequeño. El sobreajuste continuó apareciendo, pero fue menos fuerte. Esto me permitió entender que el tamaño y la configuración de una red pueden influir en su capacidad para generalizar.

Para reducir el sobreajuste utilicé:

* **Regularización:** ayuda a evitar que el modelo dependa demasiado de los datos de entrenamiento.

* **Dropout:** durante el entrenamiento se desactivan aleatoriamente algunas neuronas. En este caso se utilizó un *dropout* del 50%, haciendo que la red no dependa siempre de las mismas neuronas.

Finalmente, realicé una predicción de ejemplo con el modelo entrenado. Para el índice 10, el modelo obtuvo una probabilidad de **99.4%** de que la reseña perteneciera a la clase positiva.

---

## 3. Perceptrón

El **Perceptrón** es uno de los modelos más simples de una red neuronal. Recibe diferentes entradas, las combina utilizando pesos y genera una salida que representa una predicción.

### ¿Por qué sirve?

Aunque es un modelo sencillo, entender su funcionamiento ayuda a comprender cómo se construyen redes neuronales más complejas. También permite entender por qué algunos problemas necesitan varias capas para poder ser resueltos.

La **función de activación** transforma el resultado obtenido después de combinar las entradas y sus pesos. Por ejemplo, la función escalón puede producir una salida de 0 o 1, mientras que la función *tanh* transforma el resultado a un valor entre -1 y 1.

> **Fig. 5.** Comparación de la salida del perceptrón utilizando diferentes funciones de activación: función escalón y tanh.

Durante el taller probé el perceptrón utilizando compuertas lógicas:

* **AND:** la salida es 1 solamente cuando las dos entradas son 1.

* **OR:** la salida es 1 cuando al menos una de las entradas es 1.

* **XOR:** la salida es 1 cuando las dos entradas son diferentes.

Al observar las fronteras de decisión, pude comprobar que AND y OR pueden ser representadas mediante una sola frontera lineal. En cambio, XOR presenta una distribución que no puede separarse correctamente utilizando una sola línea.

> **Fig. 6.** Fronteras de decisión de las compuertas AND, OR y el intento de resolver XOR utilizando un solo perceptrón.

La conclusión principal fue que **un solo perceptrón no puede resolver el problema XOR**, porque sus puntos no pueden separarse mediante una única frontera lineal. Sin embargo, utilizando más de un perceptrón y una capa de salida sí es posible resolverlo.

Esto me ayudó a entender por qué las redes neuronales pueden necesitar varias capas para resolver problemas más complejos y cómo se relaciona esta idea con las CNN estudiadas anteriormente.

---

## 4. Aplicación de lo aprendido al proyecto LanternGuard

Mi proyecto se llama **LanternGuard** y busca desarrollar un sistema que permita detectar la presencia y nivel de bioincrustación en las linternas utilizadas para el cultivo de concha de abanico. Para ello, el sistema combina un **sensor de proximidad** con una **cámara** que toma fotografías de las linternas.

El sensor de proximidad puede ayudar a detectar la presencia o cercanía de la linterna respecto al sistema de medición, mientras que la cámara proporciona la información visual que será analizada mediante inteligencia artificial.

Para la parte de análisis de imágenes utilizaría una **CNN**, debido a que el objetivo es reconocer patrones visuales relacionados con la presencia de bioincrustación. La experiencia realizada con TrashNet  <a href="#ref2">[2]</a> me permitió entender cómo una CNN puede aprender características de una imagen y utilizarlas para realizar una clasificación.

En LanternGuard, las fotografías podrían organizarse según diferentes niveles de bioincrustación, por ejemplo:

* **0:** sin bioincrustación.
* **1:** nivel bajo.
* **2:** nivel medio.
* **3:** nivel alto.

Estos niveles tendrían que definirse mediante un criterio de evaluación para que las fotografías puedan ser clasificadas de manera consistente. De esta forma, el proyecto no se limitaría solamente a decir si una linterna está limpia o sucia, sino que buscaría identificar diferentes niveles de bioincrustación.

También sería necesario generar un conjunto de fotografías propias, tomando imágenes de linternas con diferentes condiciones de bioincrustación y organizándolas según el nivel establecido. Estas imágenes podrían utilizarse para entrenar, validar y probar el modelo.

Si al inicio se cuenta con pocas fotografías propias, se podría utilizar **transfer learning**, aprovechando un modelo previamente entrenado y adaptándolo a las imágenes de LanternGuard. Esto permitiría comparar el desempeño de un modelo entrenado desde cero con uno que utiliza conocimientos aprendidos previamente.

Para implementar la CNN, **Keras** podría facilitar la construcción y entrenamiento del modelo, mientras que **PyTorch** me permitió comprender de manera más detallada cómo se construyen y entrenan las redes neuronales.

Finalmente, **Grad-CAM** podría utilizarse como una herramienta de apoyo para revisar las predicciones del modelo. En este proyecto sería importante verificar que la red esté observando las zonas de la linterna donde realmente se encuentra la bioincrustación y no otros elementos presentes en la fotografía.

El **Perceptrón** no sería utilizado directamente para analizar las fotografías, debido a que es un modelo mucho más simple y no está diseñado para aprovechar la información espacial de una imagen. Sin embargo, su estudio fue importante para comprender cómo las entradas, los pesos, las funciones de activación y las capas forman parte de redes neuronales más complejas.

---

## 5. Conclusiones del taller

A partir del taller comprendí que las redes neuronales pueden utilizarse de diferentes maneras dependiendo del tipo de información que se quiera analizar.

Las **CNN** permiten trabajar con imágenes y aprender patrones visuales mediante diferentes capas. La práctica también mostró que construir una CNN desde cero no garantiza un buen resultado, por lo que es necesario evaluar el modelo y probar técnicas como *data augmentation*, transfer learning y *fine-tuning*.

Con **Keras** aprendí que es posible construir y entrenar redes neuronales de una manera más sencilla. Además, el ejercicio permitió comprender el problema del sobreajuste y algunas formas de reducirlo, como la regularización y el dropout.

El **Perceptrón** permitió comprender las bases de una red neuronal y observar que un solo modelo puede ser insuficiente para resolver problemas que no pueden separarse linealmente.

Finalmente, relacionar estos conocimientos con **LanternGuard** me permitió identificar que una CNN podría utilizarse para analizar las fotografías de las linternas y reconocer diferentes niveles de bioincrustación. También comprendí que el modelo debe ser evaluado con datos propios y que herramientas como transfer learning y Grad-CAM pueden ser útiles durante el desarrollo del proyecto.

---

## Referencias

<a id="ref1"></a>

[1] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, A. Desmaison, A. Kopf, E. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang, J. Bai y S. Chintala, “PyTorch: An Imperative Style, High-Performance Deep Learning Library,” en *Advances in Neural Information Processing Systems 32 (NeurIPS)*, 2019, pp. 8024–8035.

<a id="ref2"></a>


[2] G. Thung y M. Yang, “Classification of Trash for Recyclability Status,” *CS229 Project Report*, Stanford University, Stanford, CA, USA, 2016. [En línea]. Disponible en: https://cs229.stanford.edu/proj2016/report/ThungYang-ClassificationOfTrashForRecyclabilityStatus-report.pdf

<a id="ref3"></a>

[3] K. He, X. Zhang, S. Ren y J. Sun, “Deep Residual Learning for Image Recognition,” en *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, Las Vegas, NV, USA, 2016, pp. 770–778, doi: 10.1109/CVPR.2016.90.

<a id="ref4"></a>

[4] F. Chollet et al., “Keras,” 2015. [En línea]. Disponible en: https://keras.io


<a id="ref5"></a>

[5] A. L. Maas, R. E. Daly, P. T. Pham, D. Huang, A. Y. Ng y C. Potts, “Learning Word Vectors for Sentiment Analysis,” en *Proc. 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies*, Portland, OR, USA, 2011, pp. 142–150.



