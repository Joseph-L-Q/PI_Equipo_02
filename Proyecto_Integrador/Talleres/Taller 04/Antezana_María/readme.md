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

* **Capa Convolucional (`Conv2D`):** Aplica un conjunto de filtros (*kernels*) sobre la imagen para extraer mapas de características (*feature maps*) [2].

$$(I * K)(i, j) = \sum_{m} \sum_{n} I(i - m, j - n) \cdot K(m, n)$$

* **Función de Activación (`ReLU`):** Introduce no linealidad al sistema mediante la función $f(x) = \max(0, x)$, permitiendo a la red aprender representaciones complejas [2].
* **Capa de Submuestreo (`MaxPool2D`):** Reduce la dimensión espacial de los mapas de características reteniendo las señales más relevantes, lo que disminuye la carga computacional y previene el sobreajuste [2].
* **Capas Densas (`Fully-Connected`):** Reciben las características aplanadas (*flattened*) y realizan la clasificación final [2].

<p align="center">
  <img src="---" alt="Diagrama de arquitectura CNN" width="85%"/>
  <br>
  <em><b>Figura 1.</b> Flujo de procesamiento en una red convolucional: Convolución, ReLU, MaxPooling y Capas Densas.</em>
</p>

* **¿Qué representa este gráfico?**: Muestra el flujo completo de información dentro de una CNN, desde la imagen de entrada ($150 \times 150 \times 3$), pasando por capas alternadas de convolución (`Conv2D`) y agregación (`MaxPooling2D`), hasta las capas completamente conectadas (`Dense`) que entregan la probabilidad de clasificación.
* **¿Por qué se utiliza en el análisis?**: Permite visualizar cómo la red reduce progresivamente la dimensión espacial de las imágenes mientras incrementa la profundidad de los mapas de características (*feature maps*), pasando de detectar bordes simples a identificar estructuras complejas.


### 1.2 Resultados y resúmen del taller

Para la práctica de clasificación de residuos en el dataset *TrashNet* (vidrio vs. plástico) [3], se implementó una CNN desde cero en PyTorch [4].

1. **Entrenamiento desde cero:** El modelo alcanzó una exactitud (*accuracy*) del **63.27%** y un área bajo la curva (ROC-AUC) de **0.68**, demostrando capacidad de aprendizaje inicial pero con margen de mejora [3], [4].
2. **Data Augmentation:** Se aplicaron transformaciones geométricas (rotaciones y desplazamientos) para aumentar la diversidad del conjunto de entrenamiento y reducir el sobreajuste [2].
3. **Transfer Learning y Fine-Tuning:** Se adaptó la arquitectura **ResNet18** preentrenada [5], descongelando capas superiores para ajustar los pesos al dominio de residuos, logrando un incremento significativo en la precisión y convergencia más rápida [3], [5].

<p align="center">
  <img src="--" alt="Curvas de entrenamiento CNN vs Transfer Learning" width="80%"/>
  <br>
  <em><b>Figura 2.</b> Comparativa de curvas de pérdida y exactitud entre la CNN base y Transfer Learning con ResNet18.</em>
</p>

### 1.3 Interpretabilidad mediante Grad-CAM

Con el objetivo de auditar las decisiones del modelo, se implementó la técnica **Grad-CAM** (*Gradient-weighted Class Activation Mapping*) [6]. Esta herramienta genera mapas de calor visuales que destacan las regiones de la imagen que mayor peso tuvieron en la predicción final [6].

<p align="center">
  <img src="---" alt="Visualización Grad-CAM" width="60%"/>
  <br>
  <em><b>Figura 3.</b> Mapa de calor Grad-CAM indicando las zonas de interés analizadas por la red convolucional.</em>
</p>

---

## 2. Método Keras

**Keras** es una API de redes neuronales de alto nivel escrita en Python, capaz de ejecutarse sobre frameworks como TensorFlow [7]. Permite un prototipado intuitivo mediante la construcción de modelos secuenciales o funcionales [7].

### 2.1 Construcción del modelo y sobreajuste

En el taller se abordó un problema de clasificación de texto y sentimiento utilizando el dataset **IMDB** [8]. Los datos fueron codificados mediante *one-hot encoding* e ingresados a una red densa (*Multilayer Perceptron*) con capas ocultas activadas por `ReLU` y una salida con activación `Sigmoid` [7], [8].

Durante el entrenamiento se identificó un fenómeno claro de **sobreajuste (*overfitting*)**, donde la pérdida de entrenamiento disminuía continuamente mientras que la pérdida de validación comenzaba a aumentar a partir de la cuarta época [2], [7].

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Curva de pérdida Keras con sobreajuste" width="75%"/>
  <br>
  <em><b>Figura 4.</b> Evaluación del sobreajuste mediante el seguimiento de la pérdida en entrenamiento y validación.</em>
</p>

### 2.2 Estrategias de mitigación

Para mitigar el sobreajuste y mejorar la capacidad de generalización del modelo se aplicaron dos técnicas principales [2]:

* **Dropout:** Desactivación aleatoria del 50% de las neuronas durante cada paso de entrenamiento para evitar co-adaptaciones complejas [2].
* **Regularización L2 (Weight Decay):** Penalización de pesos elevados en la función de costo para mantener una estructura de red más simple [2].

---

## 3. Método Perceptrón

El **Perceptrón** representa la forma más elemental de una red neuronal directa (*feedforward*), diseñada por Frank Rosenblatt en 1958 [9]. Consiste en una sola neurona que realiza una combinación lineal de sus entradas ponderadas por pesos y aplica una función de activación de paso o escalón [9].

$$\hat{y} = f\left( \sum_{i=1}^{n} w_i x_i + b \right)$$

### 3.1 Funciones de activación y separabilidad lineal

Se evaluó la respuesta de la neurona utilizando distintas funciones de activación, tales como la función escalón unitario y la tangente hiperbólica (`tanh`) [2], [9].

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Funciones de activación en el Perceptrón" width="70%"/>
  <br>
  <em><b>Figura 5.</b> Comportamiento de la salida del perceptrón bajo funciones de activación escalón y tangente hiperbólica.</em>
</p>

### 3.2 La limitación del problema XOR

Al probar el perceptrón con compuertas lógicas simples, se comprobó experimentalmente que un solo perceptrón puede resolver problemas **linealmente separables** como `AND` u `OR` [9]. Sin embargo, es **incapaz de resolver la función lógica `XOR`**, debido a que no existe una única línea recta que pueda dividir las clases en el plano hiperplano [2], [9]. Esta limitación histórica motivó el desarrollo del Perceptrón Multicapa (MLP) y el algoritmo de retropropagación (*backpropagation*) [2].

<p align="center">
  <img src="URL_DE_TU_IMAGEN" alt="Fronteras de decisión AND OR XOR" width="85%"/>
  <br>
  <em><b>Figura 6.</b> Fronteras de decisión para compuertas lógicas: separabilidad lineal (AND, OR) frente a no separabilidad (XOR).</em>
</p>

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

[1] I. Goodfellow, Y. Bengio, y A. Courville, *Deep Learning*. Cambridge, MA, USA: MIT Press, 2016.

[2] A. Géron, *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*, 2nd ed. Sebastopol, CA, USA: O'Reilly Media, 2019.

[3] G. Thung y M. Yang, "Classification of Trash for Recyclability Status," *CS229 Project Report*, Stanford University, Stanford, CA, USA, 2016.

[4] A. Paszke *et al.*, "PyTorch: An Imperative Style, High-Performance Deep Learning Library," en *Advances in Neural Information Processing Systems 32 (NeurIPS)*, 2019, pp. 8024–8035.

[5] K. He, X. Zhang, S. Ren, y J. Sun, "Deep Residual Learning for Image Recognition," en *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, Las Vegas, NV, USA, 2016, pp. 770–778.

[6] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, y D. Batra, "Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization," en *Proc. IEEE International Conference on Computer Vision (ICCV)*, Venice, Italy, 2017, pp. 618–626.

[7] F. Chollet, *Deep Learning with Python*, 2nd ed. Shelter Island, NY, USA: Manning Publications, 2021.

[8] A. L. Maas, R. E. Daly, P. T. Pham, D. Huang, A. Y. Ng, y C. Potts, "Learning Word Vectors for Sentiment Analysis," en *Proc. 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies*, Portland, OR, USA, 2011, pp. 142–150.

[9] F. Rosenblatt, "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain," *Psychological Review*, vol. 65, no. 6, pp. 386–408, 1958.

