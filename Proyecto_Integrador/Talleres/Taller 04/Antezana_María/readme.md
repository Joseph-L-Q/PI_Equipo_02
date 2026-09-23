# Taller 4: Clasificación de Imágenes mediante Redes Neuronales Artificiales

---

## Introducción

Las Redes Neuronales Artificiales (RNA) son modelos de aprendizaje automático inspirados en la estructura biológica del cerebro humano, diseñados para reconocer patrones complejos, clasificar información y tomar decisiones a partir de datos no estructurados como imágenes o texto [1]. En este taller exploramos tres enfoques clave dentro del aprendizaje profundo: el **Perceptrón**, como la unidad fundamental de procesamiento; **Keras**, un framework de alto nivel para prototipado rápido de redes densas; y las **Redes Neuronales Convolucionales (CNN)**, especializadas en el procesamiento y extracción de características en visión computacional [1], [2].

Como estudiante de ingeniería industrial que busca optimización de procesos, estas herramientas permiten automatizar tareas de inspección visual, control de calidad y predicción, reemplazando la evaluación manual con sistemas más precisos, sostenibles y eficientes.

Orientándonos más a nuestro proyecto acerca del monitoreo de biofouling y evaluación del estado de las conchas de abanico (*Argopecten purpuratus*), el análisis de imágenes en **Lanterguard** puede realizarse mediante redes neuronales, esto permitiría optimizar la toma de decisiones, reduciendo la mortalidad de los cultivos y mejorando la eficiencia operativa.

---

## 1. Método CNN (Convolutional Neural Networks)

Las Redes Neuronales Convolucionales (CNN) son una arquitectura de aprendizaje profundo diseñada específicamente para trabajar con datos estructurados en forma de rejilla, como las imágenes [2]. A diferencia de las redes totalmente conectadas, las CNN reducen la complejidad operacional mediante operaciones de convolución que detectan patrones locales (bordes, texturas y formas) independientemente de su posición en la imagen. 

### 1.1 Componentes principales

Una CNN se arma combinando distintos tipos de capas que van transformando la imagen paso a paso:

* **Convolución (Conv2D):** aplica filtros pequeños llamados *kernels* que recorren la imagen para obtener mapas de características. Las primeras capas aprenden rasgos simples (bordes), mientras que las capas más profundas aprenden formas más complejas [2].

$$(I * K)(i, j) = \sum_{m} \sum_{n} I(i - m, j - n) \cdot K(m, n)$$

* **Activación (ReLU):** introduce no linealidad en el modelo. Su funcionamiento es sencillo: si el valor es negativo lo convierte en 0, y si es positivo lo deja igual. Esto le permite a la red aprender relaciones que no son simplemente rectas [3].
* **Pooling (MaxPool):** reduce el tamaño de la información obtenida en cada mapa de características, quedándose con lo más relevante. Esto ayuda a que el modelo generalice mejor y a que el costo computacional no se dispare [1].
* **Capas fully-connected (densas):** son las capas finales que toman toda la información ya procesada y la usan para dar la clasificación de salida.

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Diagrama de arquitectura de una CNN" width="80%"/>
  <br>
  <em><b>Figura 1.</b> Diagrama de la arquitectura de una CNN, mostrando el flujo de una imagen a través de las capas de convolución, activación, pooling y capas densas.</em>
</p>

### 1.2. Resultados y resumen del taller

Antes de entrenar cualquier modelo, primero se preparó el entorno de trabajo. Para este taller se usó **PyTorch**, ya que permite construir y entrenar redes neuronales con bastante control sobre cada capa [4]:

    packages = [
        "torch", "torchvision", "numpy",
        "matplotlib", "scikit-learn", "tqdm", "pillow"
    ]

Para trabajar con imágenes se utilizó el dataset **TrashNet** [5], que contiene fotografías de distintos tipos de residuos. Para este ejercicio solo se usaron dos clases: vidrio (0) y plástico (1), en escala de grises, divididas en conjuntos de entrenamiento, validación y prueba mediante `trash_dataset.py`. Antes de poder usar las imágenes en la red, fue necesario convertirlas de formato `.jpg` a tensores, que es la estructura numérica que PyTorch necesita para poder procesar la información:

    transform_basic = T.Compose([
        T.ToTensor()  # Convierte la imagen en un tensor
    ])

También se configuraron los `DataLoaders`, que se encargan de organizar las imágenes en lotes (*batches*) y de mezclarlas, y definí el `device`, para que el entrenamiento se ejecute en GPU si está disponible. La GPU es un procesador especializado que puede hacer muchas operaciones en paralelo, lo cual resulta clave para entrenar redes neuronales como las CNN de forma más rápida.

Con el entorno y los datos listos, se pasó a la parte de entrenamiento y evaluación, que es donde realmente se puede ver qué tanto aprende el modelo.

#### 1.2.1. Verificación visual del dataset

Antes de entrenar, se realizó una revisión visual de algunos ejemplos de cada clase para confirmar que las imágenes y sus etiquetas estaban correctamente cargadas.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5c03f40c-669b-40ed-a78c-8e0f87d8d23f" width="80%"/>
  <br>
  <em><b>Figura 2.</b> Ejemplos de imágenes de las clases vidrio (0) y plástico (1) del dataset TrashNet, en escala de grises.</em>
</p>

**Interpretación:** las imágenes muestran texturas y formas claramente distintas entre ambos materiales, lo cual en teoría le da a la CNN suficiente información visual para diferenciarlas.

#### 1.2.2. Entrenamiento de la CNN desde cero

Se construyó una CNN básica combinando bloques de convolución, ReLU y pooling, y un clasificador final. Para evaluar el modelo usamos varias métricas: *accuracy* (porcentaje de aciertos), ROC-AUC (qué tan bien separa las dos clases), matriz de confusión y las métricas de *precision*, *recall* y F1-score, que son útiles cuando una clase tiene más ejemplos que otra [1].

<p align="center">
  <img src="https://github.com/user-attachments/assets/ccf2684e-91da-4eae-a1c0-39a6310862f1" width="80%"/>
  <br>
  <em><b>Figura 3.</b> Pérdida de entrenamiento y métricas de validación (Accuracy y ROC-AUC) de la CNN entrenada desde cero.</em>
</p>

**Interpretación:** a partir de la época 4 el modelo empieza a mejorar su clasificación hasta alcanzar una exactitud de validación de 63.27 % y un ROC-AUC entre 0.67 y 0.69. Esto muestra que sí hubo aprendizaje, pero de forma moderada: la pérdida baja poco a poco, sin embargo, la mejora no es muy grande. Esto me hizo entender que entrenar una red no garantiza automáticamente un buen resultado, y que hay que evaluar con cuidado antes de sacar conclusiones.

#### 1.2.3. Evaluación en el conjunto de prueba

<p align="center">
  <img src="https://github.com/user-attachments/assets/603571ff-3822-4053-a1a0-a28590f6083e" width="70%"/>
  <br>
  <em><b>Figura 4.</b> Matriz de confusión de la CNN entrenada desde cero sobre el conjunto de prueba.</em>
</p>

**Interpretación:** en el conjunto de prueba, la exactitud bajó a 54.36 % y el ROC-AUC a 0.62, valores más bajos que en validación. Esto indica que el modelo entrenado desde cero, con pocas imágenes y sin ayuda externa, tiene una capacidad de generalización limitada frente a datos completamente nuevos.

#### 1.2.4. Data augmentation y Transfer Learning

Después probamos **data augmentation**, que consiste en generar pequeñas variaciones de las imágenes originales (rotaciones y desplazamientos leves) para que el modelo aprenda de formas distintas de una misma imagen [1]. Con esta técnica, la exactitud en prueba subió de 54.36 % a 59.06 %, una mejora ligera pero visible.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5cb3631e-ca55-4f49-b49f-cdb81acc5ada" width="70%"/>
  <br>
  <em><b>Figura 5.</b> --- </em>
</p>

**Interpretación:** ---

Luego aplicamos **transfer learning**, que consiste en reutilizar un modelo que ya fue entrenado previamente con una gran cantidad de imágenes, y adaptarlo a un problema nuevo [6]. Se usó una red **ResNet18** [7] preentrenada: primero entrenamos solamente la última capa (dejando las demás congeladas), y después hice *fine-tuning*, descongelando las últimas capas para que se ajustaran mejor a las imágenes de vidrio y plástico.

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Resultados del modelo con transfer learning" width="80%"/>
  <br>
  <em><b>Figura 6.</b> Métricas de validación y evaluación en prueba del modelo con transfer learning y fine-tuning (ResNet18).</em>
</p>

**Interpretación:** el cambio fue enorme. La exactitud en prueba pasó de 54.36 % (CNN desde cero) a 88.59 %, y el ROC-AUC subió de 0.62 a 0.96. Esto permitió comprobar en la práctica por qué el transfer learning es tan útil cuando no se cuenta con muchas imágenes propias: en vez de aprender todo desde cero, el modelo aprovecha lo que ya "sabe ver" de millones de imágenes previas y solo se ajusta al nuevo problema.

#### 1.2.5. Interpretabilidad con Grad-CAM

Para entender en qué se estaba fijando el modelo, utilicé **Grad-CAM**, una técnica que genera un mapa de calor sobre la imagen, señalando las zonas que más influyeron en la predicción [8].

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Mapa de calor Grad-CAM" width="80%"/>
  <br>
  <em><b>Figura 7.</b> Mapa de calor generado mediante Grad-CAM sobre una imagen de prueba, superpuesto a la imagen original.</em>
</p>

**Interpretación:** las zonas más claras del mapa de calor indican mayor influencia en la decisión del modelo, mientras que las zonas oscuras tuvieron poco peso. Esta herramienta es valiosa porque no basta con que un modelo tenga buena exactitud; también hay que verificar que esté "mirando" las partes correctas de la imagen y no elementos irrelevantes del fondo.

Finalmente, guardé los tres modelos entrenados (CNN desde cero, CNN con augmentation y ResNet con transfer learning) para poder reutilizarlos después sin tener que volver a entrenarlos desde el inicio.

---

## 2. Método Keras

**Keras** es un framework de alto nivel que permite construir y entrenar redes neuronales de forma más sencilla que programarlas completamente desde cero [9]. En este taller lo utilicé para resolver un problema de **clasificación binaria**: identificar si una reseña de película es positiva o negativa, usando el dataset **IMDB** [10].

### 2.1. Arquitectura y componentes utilizados

Para este modelo usé:

* **Capas densas (Dense):** dos capas ocultas de 16 neuronas cada una, con activación **ReLU**, y una capa de salida de 1 neurona con activación **sigmoide**, que entrega un valor entre 0 y 1 interpretado como la probabilidad de que la reseña sea positiva [1].
* **Función de pérdida (binary_crossentropy):** mide qué tan lejos están las predicciones del valor real en un problema de dos clases [1].
* **One-hot encoding:** como el texto no se le puede dar directamente a la red, cada reseña se transforma en un vector de 10,000 posiciones, donde cada posición indica si una palabra específica del vocabulario está presente (1) o ausente (0).

### 2.2. Resultados y resumen del taller

El dataset IMDB [10] ya viene con cada reseña representada como una secuencia de números, donde cada número corresponde a una palabra según un diccionario (`word_index`) que Keras proporciona. Después de revisar cómo se veía una reseña en este formato, apliqué la función de one-hot encoding para convertir todas las reseñas de entrenamiento y prueba en vectores que la red pudiera procesar, y finalmente armé el modelo con las capas descritas en el punto 2.1.

#### 2.2.1. Entrenamiento del modelo base y sobreajuste

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Curva de pérdida de entrenamiento y validación" width="70%"/>
  <br>
  <em><b>Figura 8.</b> Curva de pérdida del conjunto de entrenamiento y del conjunto de validación del modelo base de Keras.</em>
</p>

**Interpretación:** la pérdida de entrenamiento sigue bajando, pero la de validación deja de mejorar y hasta empieza a subir después de cierta época. Esta señal se conoce como **sobreajuste (overfitting)**: el modelo empieza a "memorizar" las reseñas de entrenamiento en vez de aprender patrones que funcionen también con reseñas nuevas [1]. En el conjunto de prueba, el modelo obtuvo una pérdida de aproximadamente 0.6 y una exactitud de 86.1 %.

#### 2.2.2. Comparación con un modelo más pequeño

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Comparación entre modelo original y modelo más pequeño" width="70%"/>
  <br>
  <em><b>Figura 9.</b> Comparación de la pérdida de validación entre el modelo original y un modelo con menos neuronas.</em>
</p>

**Interpretación:** al reducir el tamaño de la red (menos neuronas), el sobreajuste sigue apareciendo, pero de forma más leve y más lenta. Esto me ayudó a entender que el tamaño de una red no es "mientras más grande, mejor": una red demasiado grande para un problema simple puede aprender de más y perder capacidad de generalizar.

#### 2.2.3. Regularización L2

Para intentar reducir el sobreajuste, apliqué **regularización L2**, que penaliza a la red cuando los pesos se vuelven demasiado grandes, evitando que dependa demasiado de combinaciones muy específicas de los datos de entrenamiento [1].

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Curvas con regularización L2" width="70%"/>
  <br>
  <em><b>Figura 10.</b> Curvas de pérdida de entrenamiento y validación aplicando regularización L2, comparadas con el modelo original.</em>
</p>

**Interpretación:** con regularización, el sobreajuste se retrasa un poco, aunque no desaparece del todo. Igual me sirvió para confirmar que la regularización sí modifica cómo aprende el modelo, incluso si en algunas épocas el error se ve un poco más alto que antes.

#### 2.2.4. Dropout

También probé **Dropout**, una técnica que durante el entrenamiento apaga aleatoriamente un porcentaje de las neuronas (en este caso, 50 %), obligando a la red a no depender siempre de las mismas neuronas para aprender [11]:

    # Desactiva de forma aleatoria aprox. 50% de las neuronas
    model4.add(layers.Dropout(0.5))

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Curvas con Dropout" width="70%"/>
  <br>
  <em><b>Figura 11.</b> Curva de pérdida de validación aplicando Dropout, comparada con el modelo original.</em>
</p>

**Interpretación:** con Dropout, el modelo tarda más en empezar a sobreajustarse en comparación con el modelo original, lo que confirma que esta técnica realmente ayuda a que la red generalice mejor.

#### 2.2.5. Predicción de ejemplo

Finalmente, hice una predicción de prueba con el modelo entrenado. Para la reseña del índice 10, el modelo devolvió una probabilidad de 99.4 % de que la reseña fuera positiva, lo cual coincide con el resultado real de esa reseña.

---

## 3. Método Perceptrón

El **Perceptrón** es el modelo más simple de una red neuronal. Fue propuesto originalmente como un modelo capaz de aprender a partir de ejemplos, combinando distintas entradas mediante pesos para producir una salida [12]. Aunque es un modelo muy básico, entenderlo ayuda a comprender cómo funcionan por dentro modelos mucho más complejos, como las CNN vistas en el punto 1.

### 3.1. Funcionamiento y funciones de activación

El perceptrón recibe varias entradas, las multiplica por sus respectivos pesos, les suma un sesgo (*bias*) y pasa ese resultado por una **función de activación**, que decide la salida final. En el taller probé dos funciones de activación distintas:

* **Función escalón:** devuelve 0 o 1, dependiendo de si la suma ponderada es negativa o positiva.
* **Función tanh:** transforma el resultado en un valor continuo entre -1 y 1.

Para relacionarlo con un contexto industrial, probé el perceptrón con un ejemplo de detección de sobrecalentamiento en un equipo, usando como entradas la temperatura y la vibración registradas por sensores. Dependiendo de los pesos y el sesgo asignados, el perceptrón decide si activar o no una alerta.

### 3.2. Resultados y resumen del taller

Además del ejemplo anterior, probé el perceptrón con las compuertas lógicas AND, OR y XOR, para observar qué tipo de problemas puede resolver un solo perceptrón.

#### 3.2.1. Compuertas AND y OR

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Fronteras de decisión AND y OR" width="60%"/>
  <br>
  <em><b>Figura 12.</b> Fronteras de decisión del perceptrón para las compuertas lógicas AND y OR.</em>
</p>

**Interpretación:** tanto AND (salida 1 solo si ambas entradas son 1) como OR (salida 1 si al menos una entrada es 1) se pueden resolver con una sola línea recta que separa los puntos donde la salida es 0 de los puntos donde la salida es 1. Esto confirma que un solo perceptrón puede resolver problemas que son **linealmente separables**.

#### 3.2.2. El problema XOR y su limitación

La compuerta XOR da como salida 1 solo cuando las dos entradas son diferentes. Al intentar resolverla con un solo perceptrón, no es posible encontrar una única línea recta que separe correctamente los casos [13].

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Solución de XOR con dos neuronas" width="60%"/>
  <br>
  <em><b>Figura 13.</b> Fronteras de decisión de dos neuronas trabajando en conjunto para resolver el problema XOR.</em>
</p>

**Interpretación:** un solo perceptrón no puede resolver XOR porque sus puntos no se pueden separar con una única frontera lineal [13]. Sin embargo, al combinar dos perceptrones junto con una capa de salida, sí es posible resolverlo. Esto me ayudó a entender por qué las redes neuronales necesitan varias capas para poder resolver problemas más complejos, y cómo esa misma idea es la base de arquitecturas más avanzadas como las CNN.

---

## 4. Análisis de los Métodos para uso en LanternGuard

Nuestro proyecto integrador, **LanternGuard**, busca automatizar el monitoreo y cuantificación del nivel de bioincrustación (*biofouling*) en linternas de cultivo de concha de abanico (*Argopecten purpuratus*). El sistema integra sensores de proximidad para el posicionamiento y módulos de captura de imagen en campo.

### 4.1 Selección de la técnica ideal: CNN con Transfer Learning

Tras analizar las metodologías del taller, se determinó que el método ideal para **LanternGuard** es una **Red Neuronal Convolucional (CNN) optimizada con Transfer Learning (ResNet18 / MobileNet)** [2], [5].

* **¿Por qué no un Perceptrón simple o Red Densa?** El Perceptrón no conserva la estructura espacial 2D de las imágenes y requeriría aplanar los píxeles, perdiendo la relación de vecindad entre organismo e infraestructura [2], [9].
* **¿Por qué Keras o PyTorch con CNN?** Las CNN extraen automáticamente patrones visuales complejos como textura, color y densidad de organismos adheridos (p. ej., balanos, algas o ascidias) [2].
* **¿Por qué Transfer Learning?** En entornos acuícolas reales, la recolección de miles de imágenes etiquetadas es costosa. Iniciar con un modelo preentrenado permite lograr alta precisión con un dataset local reducido [2], [5].

### 4.2 Integración propuesta para la categorización del biofouling

Se plantea un esquema de clasificación multiclase según la severidad de la incrustación:

* **Clase 0 (Limpio):** Linterna sin adherencias (0% - 5% cobertura).
* **Clase 1 (Bajo):** Cobertura incipiente (5% - 25%).
* **Clase 2 (Medio):** Incrustación moderada (25% - 50%).
* **Clase 3 (Alto):** Obstrucción crítica (> 50%), requiriendo mantenimiento inmediato.

Además, la incorporación de **Grad-CAM** en LanternGuard resulta fundamental para validación operativa, asegurando que el modelo enfoque sus predicciones en las mallas de la linterna y no en reflexiones de luz o sombras de la embarcación [6].

---

## 5. Borrador de Implementación para LanternGuard

---

## 6. Referencias Bibliográficas

[1] I. Goodfellow, Y. Bengio, and A. Courville, *Deep Learning*. Cambridge, MA, USA: MIT Press, 2016.

[2] Y. LeCun, Y. Bengio, and G. Hinton, "Deep learning," *Nature*, vol. 521, no. 7553, pp. 436-444, May 2015.

[3] V. Nair and G. E. Hinton, "Rectified linear units improve restricted Boltzmann machines," in *Proc. 27th Int. Conf. Machine Learning (ICML)*, Haifa, Israel, 2010, pp. 807-814.

[4] A. Paszke *et al.*, "PyTorch: An imperative style, high-performance deep learning library," in *Advances in Neural Information Processing Systems 32 (NeurIPS)*, 2019, pp. 8024-8035.

[5] G. Thung and M. Yang, "Classification of trash for recyclability status," *CS229 Project Report*, Stanford University, Stanford, CA, USA, 2016.

[6] S. J. Pan and Q. Yang, "A survey on transfer learning," *IEEE Transactions on Knowledge and Data Engineering*, vol. 22, no. 10, pp. 1345-1359, Oct. 2010.

[7] K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR)*, Las Vegas, NV, USA, 2016, pp. 770-778.

[8] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, "Grad-CAM: Visual explanations from deep networks via gradient-based localization," in *Proc. IEEE Int. Conf. Computer Vision (ICCV)*, Venice, Italy, 2017, pp. 618-626.

[9] F. Chollet *et al.*, "Keras," 2015. [Online]. Available: https://keras.io

[10] A. L. Maas, R. E. Daly, P. T. Pham, D. Huang, A. Y. Ng, and C. Potts, "Learning word vectors for sentiment analysis," in *Proc. 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies*, Portland, OR, USA, 2011, pp. 142-150.

[11] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, "Dropout: A simple way to prevent neural networks from overfitting," *Journal of Machine Learning Research*, vol. 15, no. 1, pp. 1929-1958, 2014.

[12] F. Rosenblatt, "The perceptron: A probabilistic model for information storage and organization in the brain," *Psychological Review*, vol. 65, no. 6, pp. 386-408, 1958.

[13] M. Minsky and S. Papert, *Perceptrons: An Introduction to Computational Geometry*. Cambridge, MA, USA: MIT Press, 1969.
