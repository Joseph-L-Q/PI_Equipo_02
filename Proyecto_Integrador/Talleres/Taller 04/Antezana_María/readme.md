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
  <img width="1267" height="390" alt="image" src="https://github.com/user-attachments/assets/4544030b-6bf1-4599-bd2c-b2db30f8e0fd" />
  <br>
  <em><b>Figura 1.</b> Impresión de la arquitectura SimpleCNN detallando los bloques de convolución (Conv2d), activación (ReLU), reducción (MaxPool2d, AdaptiveAvgPool2d) y la capa lineal final (Linear).</em>
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

**Interpretación:** la matriz de confusión permite calcular la exactitud directamente: de los 149 casos de prueba, el modelo acertó en 81 (37 vidrios y 44 plásticos correctamente clasificados), lo que da una exactitud de 54.36 % (81/149). Sin embargo, también se equivocó bastante: confundió 39 vidrios con plástico y 29 plásticos con vidrio, es decir, casi la mitad de los errores van en cada dirección, sin que el modelo tienda claramente a favorecer una clase sobre otra. Complementando esto, el ROC-AUC de 0.62 (calculado a partir de las probabilidades de salida, no de la matriz) confirma que el modelo apenas logra separar ambas clases: un valor de 0.5 significaría una separación aleatoria, y 0.62 está bastante cerca de eso. En conjunto, ambos resultados muestran que el modelo entrenado desde cero, con solo 687 imágenes de entrenamiento y sin ayuda externa, tiene una capacidad de generalización bastante limitada frente a datos completamente nuevos.

#### 1.2.4. Data augmentation y Transfer Learning

Después probamos **data augmentation**, que consiste en generar pequeñas variaciones de las imágenes originales (rotaciones y desplazamientos leves) para que el modelo aprenda de formas distintas de una misma imagen [1]. Con esta técnica, la exactitud en prueba subió de 54.36 % a 59.06 %, una mejora ligera pero visible.

<p align="center">
  <img width="1062" height="540" alt="image" src="https://github.com/user-attachments/assets/e59c7e7d-9257-4731-b386-d5ba0a323e37" />
  <br>
  <em><b>Figura 5.</b> Entrenamiento del modelo con data augmentation (6 épocas) y comparación de la exactitud y ROC-AUC en prueba, con y sin augmentation.</em>
</p>

**Interpretación:** al comparar ambos modelos sobre el conjunto de prueba, el uso de data augmentation elevó la exactitud de 54.36 % a 59.06 % y el ROC-AUC de 0.6204 a 0.6222. Aunque la mejora es pequeña en términos absolutos, es consistente en ambas métricas, lo que sugiere que generar variaciones artificiales de las imágenes (pequeñas rotaciones y desplazamientos) sí ayuda al modelo a generalizar un poco mejor frente a datos que no vio durante el entrenamiento. Sin embargo, el ROC-AUC de 0.62 sigue estando lejos de un buen desempeño, lo que indica que el aumento de datos por sí solo no es suficiente para resolver las limitaciones de una CNN entrenada desde cero con pocas imágenes (687 en total). Esto refuerza la idea de que, para este tipo de problemas con datasets pequeños, sería necesario complementar el augmentation con otras estrategias, como el transfer learning que se aplica más adelante.

Luego aplicamos **transfer learning**, que consiste en reutilizar un modelo que ya fue entrenado previamente con una gran cantidad de imágenes, y adaptarlo a un problema nuevo [6]. Se usó una red **ResNet18** [7] preentrenada: primero entrenamos solamente la última capa (dejando las demás congeladas), y después hice *fine-tuning*, descongelando las últimas capas para que se ajustaran mejor a las imágenes de vidrio y plástico.

<p align="center">
  <img width="1270" height="401" alt="image" src="https://github.com/user-attachments/assets/2df88b45-9966-4f77-857e-375625f8722a" />
  <br>
  <em><b>Figura 6.</b> Entrenamiento del modelo con transfer learning (Etapa 1): ajuste de la última capa (fc) de ResNet18, manteniendo el resto de la red congelada.</em>
</p>

**Interpretación:** en esta primera etapa solo se entrenó la capa final (`fc`) de ResNet18, dejando congeladas todas las demás capas preentrenadas. Aun así, el modelo mejoró de forma constante en las 4 épocas: la exactitud de validación pasó de 61.22 % a 70.75 %, y el ROC-AUC subió de 0.758 a 0.849. Esto confirma la idea central del transfer learning: como ResNet18 ya fue entrenada previamente con millones de imágenes, la red ya "sabe" reconocer bordes, texturas y formas generales, por lo que solo fue necesario ajustar la última capa para adaptar ese conocimiento a la tarea específica de distinguir vidrio de plástico, sin necesidad de aprender todo desde cero.

<p align="center">
  <img width="1270" height="610" alt="image" src="https://github.com/user-attachments/assets/d767f5d3-9066-44a2-b9e0-70da9197289e" />
  <br>
  <em><b>Figura 7.</b> Descongelamiento de las capas `layer4` y `fc`, y entrenamiento con fine-tuning (Etapa 2) de ResNet18.</em>
</p>

**Interpretación:** en esta segunda etapa se descongelaron las capas de `layer4` además de `fc` (17 parámetros entrenables en total), permitiendo que la parte más profunda de la red se ajustara también a las características particulares de las imágenes de vidrio y plástico. El resultado fue una mejora considerable: la exactitud de validación subió de 78.91 % a 87.76 %, y el ROC-AUC alcanzó 0.963 en la última época. Esto muestra que el fine-tuning aporta un salto de calidad importante frente a solo entrenar la última capa, ya que le da a la red la flexibilidad de refinar sus filtros más profundos para el problema específico, en lugar de depender únicamente de las características genéricas aprendidas originalmente.

<p align="center">
  <img width="1600" height="333" alt="image" src="https://github.com/user-attachments/assets/3d02f3a3-29cf-4d8d-81be-b73f32a799d3" />
  <br>
  <em><b>Figura 8.</b> Evaluación en el conjunto de prueba del modelo con transfer learning (reporte de clasificación y matriz de confusión) y comparación global de los tres modelos entrenados.</em>
</p>

**Interpretación:** el modelo con transfer learning obtuvo una exactitud de 88.59 % y un ROC-AUC de 0.9605 en el conjunto de prueba, con un desempeño equilibrado entre ambas clases (precision y recall por encima de 0.84 tanto para vidrio como para plástico). Al comparar los tres modelos entrenados a lo largo del taller, se observa una mejora progresiva clara: la CNN entrenada desde cero apenas superaba el azar (acc=0.5436, auc=0.6204), el data augmentation aportó una mejora leve (acc=0.5906, auc=0.6222), y el transfer learning con fine-tuning dio un salto notable en ambas métricas (acc=0.8859, auc=0.9605). Esto confirma que, para un dataset pequeño como el de este ejercicio (solo 687 imágenes de entrenamiento), reutilizar el conocimiento de una red preentrenada resulta mucho más efectivo que intentar aprender todas las características desde cero, incluso aplicando técnicas de aumento de datos.


#### 1.2.5. Interpretabilidad con Grad-CAM

Para entender en qué se estaba fijando el modelo, se usó **Grad-CAM**, una técnica que genera un mapa de calor sobre la imagen, señalando las zonas que más influyeron en la predicción [8].

<p align="center">
  <img width="1120" height="393" alt="image" src="https://github.com/user-attachments/assets/557ffae0-811b-48e6-bacd-6fccf2b63487" />
  <br>
  <em><b>Figura 9.</b> Mapa de calor generado mediante Grad-CAM sobre una imagen de prueba, superpuesto a la imagen original.</em>
</p>

**Interpretación:** las zonas más claras del mapa de calor indican mayor influencia en la decisión del modelo, mientras que las zonas oscuras tuvieron poco peso. Esta herramienta es valiosa porque no basta con que un modelo tenga buena exactitud; también hay que verificar que esté "mirando" las partes correctas de la imagen y no elementos irrelevantes del fondo.

Finalmente, guardamos los tres modelos entrenados (CNN desde cero, CNN con augmentation y ResNet con transfer learning) para poder reutilizarlos después sin tener que volver a entrenarlos desde el inicio.

---

## 2. Método Keras

**Keras** es un framework de alto nivel que permite construir y entrenar redes neuronales de forma más sencilla que programarlas completamente desde cero [9]. En este taller fue usado para resolver un problema de **clasificación binaria**: identificar si una reseña de película es positiva o negativa, usando el dataset **IMDB** [10].

### 2.1. Arquitectura y componentes utilizados

Para este modelo se utilizó:

* **Capas densas (Dense):** dos capas ocultas de 16 neuronas cada una, con activación **ReLU**, y una capa de salida de 1 neurona con activación **sigmoide**, que entrega un valor entre 0 y 1 interpretado como la probabilidad de que la reseña sea positiva [1].
* **Función de pérdida (binary_crossentropy):** mide qué tan lejos están las predicciones del valor real en un problema de dos clases [1].
* **One-hot encoding:** como el texto no se le puede dar directamente a la red, cada reseña se transforma en un vector de 10,000 posiciones, donde cada posición indica si una palabra específica del vocabulario está presente (1) o ausente (0).

### 2.2. Resultados y resumen del taller

El dataset IMDB [10] ya viene con cada reseña representada como una secuencia de números, donde cada número corresponde a una palabra según un diccionario (`word_index`) que Keras proporciona. Después de revisar cómo se veía una reseña en este formato, aplicamos la función de one-hot encoding para convertir todas las reseñas de entrenamiento y prueba en vectores que la red pudiera procesar, y finalmente armamos el modelo con las capas descritas en el punto 2.1.

#### 2.2.1. Entrenamiento del modelo base y sobreajuste

<p align="center">
<img width="776" height="762" alt="image" src="https://github.com/user-attachments/assets/df5493d4-7f54-4c41-8d4c-d5a37a3ea170" width="70%"/>
  <br>
  <em><b>Figura 10.</b> Curva de pérdida del conjunto de entrenamiento y del conjunto de validación del modelo base de Keras.</em>
</p>

**Interpretación:** la pérdida de entrenamiento sigue bajando, pero la de validación deja de mejorar y hasta empieza a subir después de cierta época. Esta señal se conoce como **sobreajuste (overfitting)**: el modelo empieza a "memorizar" las reseñas de entrenamiento en vez de aprender patrones que funcionen también con reseñas nuevas [1]. En el conjunto de prueba, el modelo obtuvo una pérdida de aproximadamente 0.6 y una exactitud de 86.1 %.

#### 2.2.2. Comparación con un modelo más pequeño

<p align="center">
  <img width="783" height="758" alt="image" src="https://github.com/user-attachments/assets/57225205-80fb-41a5-abc3-b0767fa4b42e" width="70%"/>
  <br>
  <em><b>Figura 11.</b> Comparación de la pérdida de validación entre el modelo original y un modelo con menos neuronas.</em>
</p>

**Interpretación:** al reducir el tamaño de la red (menos neuronas), el sobreajuste sigue apareciendo, pero de forma más leve y más lenta. Esto ayudó a entender que el tamaño de una red no es "mientras más grande, mejor": una red demasiado grande para un problema simple puede aprender de más y perder capacidad de generalizar.

#### 2.2.3. Regularización L2

Para intentar reducir el sobreajuste, se aplicó **regularización L2**, que penaliza a la red cuando los pesos se vuelven demasiado grandes, evitando que dependa demasiado de combinaciones muy específicas de los datos de entrenamiento [1].

<p align="center">
  <img width="780" height="762" alt="image" src="https://github.com/user-attachments/assets/229abe54-be71-411a-b37f-0e935c6bf1bb" width="70%"/>
  <br>
  <em><b>Figura 12.</b> Curvas de pérdida de entrenamiento y validación aplicando regularización L2, comparadas con el modelo original.</em>
</p>

**Interpretación:** con regularización, el sobreajuste se retrasa un poco, aunque no desaparece del todo. Igual me sirvió para confirmar que la regularización sí modifica cómo aprende el modelo, incluso si en algunas épocas el error se ve un poco más alto que antes.

#### 2.2.4. Dropout

También probamos **Dropout**, una técnica que durante el entrenamiento apaga aleatoriamente un porcentaje de las neuronas (en este caso, 50 %), obligando a la red a no depender siempre de las mismas neuronas para aprender [11]:

    # Desactiva de forma aleatoria aprox. 50% de las neuronas
    model4.add(layers.Dropout(0.5))

<p align="center">
  <img width="786" height="766" alt="image" src="https://github.com/user-attachments/assets/d40aeaa7-df23-420d-a8c0-32ddb779063a" width="70%"/>
  <br>
  <em><b>Figura 13.</b> Curva de pérdida de validación aplicando Dropout, comparada con el modelo original.</em>
</p>

**Interpretación:** con Dropout, el modelo tarda más en empezar a sobreajustarse en comparación con el modelo original, lo que confirma que esta técnica realmente ayuda a que la red generalice mejor.

#### 2.2.5. Predicción de ejemplo

Finalmente, hicicmos una predicción de prueba con el modelo entrenado. Para la reseña del índice 10, el modelo devolvió una probabilidad de 99.4 % de que la reseña fuera positiva, lo cual coincide con el resultado real de esa reseña.

---

## 3. Método Perceptrón

El **Perceptrón** es el modelo más simple de una red neuronal. Fue propuesto originalmente como un modelo capaz de aprender a partir de ejemplos, combinando distintas entradas mediante pesos para producir una salida [12]. Aunque es un modelo muy básico, entenderlo ayuda a comprender cómo funcionan por dentro modelos mucho más complejos, como las CNN vistas en el punto 1.

### 3.1. Funcionamiento y funciones de activación

El perceptrón recibe varias entradas, las multiplica por sus respectivos pesos, les suma un sesgo (*bias*) y pasa ese resultado por una **función de activación**, que decide la salida final. En el taller probamos dos funciones de activación distintas:

* **Función escalón:** devuelve 0 o 1, dependiendo de si la suma ponderada es negativa o positiva.
* **Función tanh:** transforma el resultado en un valor continuo entre -1 y 1.

Para relacionarlo con un contexto industrial, probamos el perceptrón con un ejemplo de detección de sobrecalentamiento en un equipo, usando como entradas la temperatura y la vibración registradas por sensores. Dependiendo de los pesos y el sesgo asignados, el perceptrón decide si activar o no una alerta.

### 3.2. Resultados y resumen del taller

Además del ejemplo anterior, probamos el perceptrón con las compuertas lógicas AND, OR y XOR, para observar qué tipo de problemas puede resolver un solo perceptrón.

#### 3.2.1. Compuertas AND y OR

<p align="center">
  <img width="1381" height="816" alt="image" src="https://github.com/user-attachments/assets/6ba51e85-af5e-4905-9067-ceffa5fe8073" />
  <br>
  <em><b>Figura 14.</b> Fronteras de decisión del perceptrón para las compuertas lógicas AND y OR.</em>
</p>

**Interpretación:** el código probó el perceptrón con distintas combinaciones de pesos para las cuatro entradas posibles: (0,0), (0,1), (1,0) y (1,1). Con los pesos [0.4, 0.4] y bias -0.5, el perceptrón se comportó como una compuerta **AND**: la salida fue 0 en (0,0), (0,1) y (1,0), y solo dio 1 cuando ambas entradas eran 1, es decir, (1,1). Esto tiene sentido matemático, ya que la suma ponderada (0.4×1 + 0.4×1 - 0.5 = 0.3) es la única combinación donde el resultado supera el umbral de 0 necesario para activar la función escalón. Por otro lado, con los pesos [2, 1] y bias -0.5, el perceptrón se comportó como una compuerta **OR**: la salida fue 0 únicamente en (0,0), y 1 en las otras tres combinaciones, bastando con que una sola entrada fuera 1 para que la suma ponderada superara el umbral. Al graficar estas dos compuertas, tanto AND como OR se pueden resolver con una sola línea recta que separa los puntos donde la salida es 0 de los puntos donde la salida es 1. Esto confirma que un solo perceptrón puede resolver problemas que son **linealmente separables**, y que el resultado de la clasificación depende directamente de los pesos y el bias elegidos, no solo de las entradas.


#### 3.2.2. El problema XOR y su limitación

La compuerta XOR da como salida 1 solo cuando las dos entradas son diferentes. Al intentar resolverla con un solo perceptrón, no es posible encontrar una única línea recta que separe correctamente los casos [13].

<p align="center">
  <img width="482" height="477" alt="image" src="https://github.com/user-attachments/assets/7e6af943-21ca-40fe-a9fd-55dd549b597d" width="80%"/>
  <br>
  <em><b>Figura 15.</b> Fronteras de decisión de dos neuronas trabajando en conjunto para resolver el problema XOR.</em>
</p>

**Interpretación:** un solo perceptrón no puede resolver XOR porque sus puntos no se pueden separar con una única frontera lineal [13]. Sin embargo, al combinar dos perceptrones junto con una capa de salida, sí es posible resolverlo. Esto me ayudó a entender por qué las redes neuronales necesitan varias capas para poder resolver problemas más complejos, y cómo esa misma idea es la base de arquitecturas más avanzadas como las CNN.

---

## 4. Análisis de los Métodos para uso en LanternGuard

Nuestro proyecto, **LanternGuard**, es un dispositivo que monitorea el biofouling (la capa de algas y organismos que se adhiere a las linternas donde crecen las conchas de abanico). El dispositivo usa un sensor de proximidad para calcular el volumen de biofouling y dos cámaras ubicadas en los extremos de las linternas para fotografiar esa acumulación. El prototipo solo mide y toma las fotos; el cálculo del volumen y el procesamiento de imágenes se harían en la nube, y los resultados llegarían a un aplicativo que muestra el volumen de biofouling, el porcentaje de batería y las fotos tomadas.

El problema de fondo es que el biofouling compite con las conchas de abanico por los nutrientes: mientras más biofouling se pega a las linternas, menos nutrientes y oxígeno les quedan a las conchas, y su crecimiento se vuelve más lento. Además, sin un monitoreo constante, las empresas acuícolas gastan de más en mantenimiento, enviando personal a limpiar las linternas incluso cuando todavía no es necesario. Nuestro dispositivo busca resolver esto avisando solo cuándo hace falta limpiar.

### 4.1. Comparación de las tres metodologías estudiadas

| Criterio | Perceptrón | Keras (capas densas) | CNN |
|---|---|---|---|
| Tratamiento de imágenes | No apto: no conserva la estructura 2D de una foto | Deficiente: requiere aplanar la imagen, perdiendo la relación espacial entre píxeles vecinos [2] | Adecuado: extrae patrones visuales conservando la posición relativa de los píxeles [2] |
| Complejidad de parámetros | Muy baja | Alta si se aplana una imagen completa | Optimizada mediante filtros compartidos y *pooling* [1] |
| Sensibilidad a variaciones de posición/luz | Alta | Alta | Baja, gracias a las capas de convolución y *pooling* [2] |
| Rol en LanternGuard | Útil solo para la decisión final (aviso o no aviso) | Útil como herramienta para construir y entrenar el modelo, no para leer la imagen directamente | Método principal para analizar las fotos de biofouling |

### 4.2. CNN: leer las fotos de las cámaras

Las dos cámaras ubicadas en los extremos de las linternas tomarían fotos periódicas de la malla. Una CNN sería la encargada de convertir cada foto en un nivel de suciedad, exactamente como en nuestro ejercicio separamos vidrio de plástico por su forma y textura, solo que aquí el patrón a reconocer sería la cantidad de algas y organismos adheridos a la malla.

* **Conv2D, ReLU y MaxPool2D** funcionarían igual que en nuestro ejercicio: los primeros filtros aprenderían a detectar texturas simples (malla limpia versus malla con algas), y los filtros de capas más profundas irían reconociendo parches de biofouling más completos, con su forma y densidad [2].
* **AdaptiveAvgPool2D y la capa Linear final** resumirían toda esa información en una sola predicción. A diferencia de nuestro ejercicio (donde la salida era binaria: vidrio o plástico), aquí la capa final probablemente tendría varias salidas con activación *softmax*, una por cada nivel de biofouling, en vez de una sola neurona.
* **Transfer learning** sería casi obligatorio en nuestro caso: como no vamos a tener miles de fotos submarinas propias, partiríamos de un modelo ya entrenado en clasificación de imágenes (como ResNet18, usado en el ejercicio, o una versión más liviana como MobileNet [14], pensando en que el procesamiento correría en la nube y conviene que sea económico) y solo reentrenaríamos la última capa con nuestras propias fotos [6].
* **Data augmentation** también sería clave, quizás más que en el ejercicio: con pocas fotos reales, generar variaciones (rotaciones, cambios de brillo que simulen distinta turbidez del agua o distinta iluminación según la profundidad) ayudaría a que el modelo no memorice las pocas fotos que sí tenemos.
* **Grad-CAM** tendría un rol importante de confianza: nos permitiría comprobar que el modelo realmente se está fijando en la malla y el biofouling, y no en elementos irrelevantes de la foto, como peces o partículas flotando en el agua [8], algo especialmente importante porque de esta predicción depende avisar (o no) a un acuicultor para que vaya a limpiar.

Los niveles de bioincrustación se organizarían en categorías operativas, por ejemplo:

* **Normal:** linterna con poca o ninguna presencia de biofouling.
* **Advertencia:** presencia moderada de organismos adheridos que requiere seguimiento.
* **Crítico:** alta presencia de biofouling que podría afectar el cultivo, requiriendo limpieza inmediata.

### 4.3. Keras: armar y entrenar el modelo

En el taller usamos Keras para un problema de texto, pero la misma lógica de "armar la red por capas y dejar que Keras haga los cálculos" aplicaría igual de bien para entrenar la CNN de la sección anterior, ya que Keras también permite construir capas convolucionales [9].

* **Sequential** seguiría siendo el molde donde apilaríamos las capas Conv2D, ReLU, MaxPool2D y la capa final.
* **compile** definiría cómo se entrena el modelo: en vez del `binary_crossentropy` que usamos con IMDB, aquí usaríamos `categorical_crossentropy`, ya que tendríamos varias clases (niveles de biofouling) en vez de dos.
* **fit**, junto con un `validation_split`, entrenaría el modelo y nos permitiría ver si aparece sobreajuste, igual que vimos con las reseñas de IMDB.
* **Dropout** y `regularizers.l2` serían casi indispensables desde el principio: con pocas fotos reales de campo, el riesgo de sobreajuste sería alto, muy similar a lo que vimos con el modelo de IMDB cuando la curva de validación empezaba a subir [11].
* Además, agregaríamos **EarlyStopping**, una función de Keras que detiene el entrenamiento automáticamente cuando la pérdida de validación deja de mejorar. Con un dataset chico, esto evitaría seguir entrenando de más y ayudaría a quedarnos con la versión del modelo que mejor generaliza.

### 4.4. Perceptrón: la lógica final de alerta

Una vez que el sistema tiene el volumen de biofouling que mide el sensor de proximidad y el nivel de suciedad que predice la CNN en las fotos, necesita tomar una decisión simple: ¿aviso o no aviso al acuicultor? Esa decisión final sería un perceptrón [12], con entradas muy concretas:

* $x_1$: el volumen de biofouling medido por el sensor de proximidad (normalizado, por ejemplo de 0 a 1).
* $x_2$: el nivel de suciedad que predice la CNN a partir de las fotos (convertido a número, por ejemplo 0 = bajo, 1 = medio, 2 = alto).
* $x_3$: el tiempo transcurrido desde la última limpieza registrada.

Con esto, la suma ponderada sería $w_1x_1 + w_2x_2 + w_3x_3 + b$, y la función escalón decidiría el resultado final: si la suma supera cierto umbral, el sistema genera la alerta de "linterna sucia, hay que limpiar"; si no, devuelve "todo bien, no hace falta ir". Es la misma lógica que usamos para detectar sobrecalentamiento en el ejemplo del equipo industrial, solo que aplicada a las conchas de abanico. Al principio, los pesos $w_1$, $w_2$ y $w_3$ probablemente se fijarían a mano, en conversación con los propios acuicultores (por ejemplo, dándole más peso al volumen medido por el sensor que al tiempo transcurrido). Más adelante, cuando se tengan suficientes casos reales de "aquí sí hacía falta limpiar" y "aquí no", esos pesos se podrían ajustar entrenando el perceptrón con esos datos, en vez de definirlos manualmente.

### 4.5. Por qué todo esto correría en la nube

Como el dispositivo solo se encarga de medir (con el sensor de proximidad) y tomar fotos (con las cámaras), tiene sentido que todo el procesamiento pesado —correr la CNN sobre las fotos y calcular el volumen— se haga en la nube y no dentro del dispositivo. Esto evita que el equipo gaste batería procesando imágenes bajo el agua, algo importante porque solo cuenta con pilas y un panel solar. El dispositivo enviaría los datos crudos (la lectura del sensor y las fotos) a través de sus antenas de radio, la nube correría los modelos entrenados con Keras y devolvería tanto el nivel de biofouling como la decisión final del perceptrón, ya lista para mostrarse en el aplicativo. El entrenamiento de los modelos (la parte que sí exige mucho cálculo) se haría aparte, de forma periódica, cada vez que se junte suficiente información nueva; en la nube, durante el uso normal, solo correría la inferencia, que es mucho más liviana.

---

## 5. Borrador de Implementación para LanternGuard

---

## 6. Conclusiones

---

## 7. Referencias Bibliográficas

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

[14] A. G. Howard *et al.*, "MobileNets: Efficient convolutional neural networks for mobile vision applications," *arXiv preprint arXiv:1704.04861*, 2017.
