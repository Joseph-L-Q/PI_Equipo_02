# Taller 04: Redes Neuronales: CNN, Keras y Perceptrón

En este trabajo revisamos tres formas de construir redes neuronales que probamos en clase: una CNN para clasificar imágenes, un modelo hecho con Keras para clasificar texto, y un perceptrón armado desde cero. Por cada una explicamos qué es, qué funciones usamos, qué resultados dio y por qué sirve. Al final contamos cómo usaríamos estas herramientas en nuestro proyecto de monitoreo submarino de conchas de abanico.

---

## 1. CNN (Red Neuronal Convolucional)

### ¿Qué es y para qué sirve

Una CNN es una red pensada para trabajar con imágenes. En lugar de mirar cada pixel por separado, recorre la imagen con pequeños filtros (kernels) que van detectando patrones: bordes, texturas, formas. Con varias capas apiladas, las primeras detectan cosas simples (líneas, bordes) y las últimas detectan formas más completas (un objeto entero). Por eso es la herramienta estándar cuando el problema depende de reconocer algo visualmente, como diferenciar dos tipos de residuos en una foto, algo que fue justamente nuestro ejercicio: separar vidrio de plástico usando el dataset TrashNet.

Esta idea de usar filtros que se deslizan sobre la imagen para reconocer patrones visuales fue formalizada por LeCun et al. en 1998, cuando mostraron que las CNN superaban a otras técnicas en el reconocimiento de dígitos escritos a mano [1].

### Piezas clave que usamos

- **Conv2D**: aplica los filtros y genera "mapas de características". Cada filtro aprende a detectar algo distinto.
- **ReLU**: es la función de activación. Su regla es simple: si el valor es negativo lo convierte en 0, si es positivo lo deja igual. Esto le da a la red la capacidad de aprender relaciones que no son lineales.
- **MaxPool2D**: reduce el tamaño de la imagen quedándose con lo más relevante de cada zona, lo que ayuda a que el modelo generalice y no se sature de cálculos.
- **AdaptiveAvgPool2D**: al final de los bloques convolucionales, resume cada mapa de características en un solo valor promedio, sin importar el tamaño original de la imagen.
- **Flatten + Linear (capa densa)**: "aplana" lo que queda de la parte convolucional y lo conecta con una capa totalmente conectada, que es la que finalmente decide entre vidrio y plástico.

<p align="center">
  <img width="857" height="717" alt="image" src="https://github.com/user-attachments/assets/4ad68d8d-feea-43b7-998a-64e1d04f7fbc" />
</p>
<p align="center"><em>Figura 1. Código de la arquitectura de la CNN entrenada desde cero (bloques Conv2D, ReLU, MaxPool2D, AdaptiveAvgPool2D y la capa densa final).</em></p>

### Lo que hicimos paso a paso

1. Cargamos el dataset TrashNet, con fotos en escala de grises de vidrio (0) y plástico (1).
2. Miramos ejemplos del dataset para asegurarnos de que las etiquetas tenían sentido.

<p align="center">
  <img width="787" height="736" alt="image" src="https://github.com/user-attachments/assets/f409f8f8-edfe-47d2-84ab-c41c9d86cc24" /
</p>
<p align="center"><em>Figura 2. Código usado para mostrar ejemplos del dataset TrashNet.</em></p>

<p align="center">
  <img width="989" height="661" alt="figura03_dataset_ejemplos" src="https://github.com/user-attachments/assets/446940b0-6873-4d96-b39b-918bc4ff7c1f" />
</p>
<p align="center"><em>Figura 3. Ejemplos del dataset TrashNet (vidrio y plástico).</em></p>

Acá se nota que las fotos de vidrio son botellas y frascos, y las de plástico son botellas y envases transparentes. Visualmente se parecen bastante entre sí, lo que ya nos avisa que el problema no iba a ser trivial para el modelo.

3. Entrenamos una CNN simple desde cero durante 8 épocas.

<p align="center">
  <img width="1066" height="370" alt="image" src="https://github.com/user-attachments/assets/2f5db870-0ac7-4ad8-a85a-8a3930ad22c3" />
</p>
<p align="center"><em>Figura 4. Código usado para graficar la pérdida y las métricas de validación durante el entrenamiento.</em></p>

<p align="center">
  <img width="864" height="395" alt="figura05_perdida_entrenamiento" src="https://github.com/user-attachments/assets/7560c4dd-ca4c-49e6-b330-146af6781427" />
</p>
<p align="center"><em>Figura 5. Pérdida de entrenamiento (CNN desde cero).</em></p>

<p align="center">
  <img width="855" height="395" alt="figura06_metricas_validacion" src="https://github.com/user-attachments/assets/9b9437ff-a449-49da-8bb5-28421c127441" />
</p>
<p align="center"><em>Figura 6. Métricas de validación (CNN desde cero).</em></p>

La pérdida baja, pero muy poco. El ROC-AUC sí mejora (llega cerca de 0.70), lo que indica que el modelo va encontrando alguna diferencia entre las clases. Sin embargo, el accuracy se queda pegado alrededor del 50%, y hacia el final incluso baja. Esto se confirma con la matriz de confusión en el set de prueba:

<p align="center">
  <img width="1093" height="302" alt="image" src="https://github.com/user-attachments/assets/c0de8cef-5858-42b5-83bb-594d99e4c652" />
</p>
<p align="center"><em>Figura 7. Código usado para graficar la matriz de confusión.</em></p>

<p align="center">
  <img width="364" height="341" alt="figura08_matriz_confusion" src="https://github.com/user-attachments/assets/bbceb026-6120-469a-bd46-58e97c2ce8ac" />
</p>
<p align="center"><em>Figura 8. Matriz de confusión CNN desde cero.</em></p>
<!-- Captura de pantalla: salida (gráfico) de la celda de la Figura 7 -->

El modelo predijo casi siempre la clase 0 (vidrio), acertando por pura casualidad en la mitad de los casos. En la práctica, esto significa que la red desde cero, con solo 8 épocas y pocos datos, no alcanzó a aprender rasgos realmente útiles: aprendió un atajo (predecir siempre lo mismo) en vez de aprender a distinguir.

4. Probamos con **data augmentation** (rotaciones y traslaciones pequeñas) para darle más variedad de ejemplos al modelo sin necesidad de más fotos reales.
5. Probamos **transfer learning**: en vez de entrenar una red desde cero, usamos ResNet18, un modelo ya entrenado en millones de imágenes (ImageNet), y solo ajustamos su última capa a nuestro problema. Esta idea de reutilizar redes profundas ya entrenadas, en vez de partir de cero, viene de arquitecturas como ResNet, que introdujeron las conexiones residuales para poder entrenar redes mucho más profundas sin que se degrade el aprendizaje [2].

<p align="center">
  <img width="1287" height="375" alt="image" src="https://github.com/user-attachments/assets/02b20f4e-6662-44da-8b2c-6f91ee2b61dc" />
</p>
<p align="center"><em>Figura 9. Código para construir el modelo con transfer learning a partir de ResNet18.</em></p>

Con transfer learning, el aprendizaje mejoró notoriamente: el modelo empezó a distinguir mejor entre vidrio y plástico, algo que no lográbamos entrenando desde cero. Luego hicimos **fine-tuning**, descongelando las últimas capas de ResNet18 para que se ajustaran mejor a nuestras imágenes específicas.

6. Por último, usamos **Grad-CAM** para entender en qué parte de la imagen se fijaba el modelo al momento de predecir. Esta técnica genera un mapa de calor sobre la imagen original, señalando las zonas que más influyeron en la decisión [3].

<p align="center">
  <img width="963" height="667" alt="image" src="https://github.com/user-attachments/assets/060faa07-1b4b-4b29-9e1f-4b00fe49a11e" />
</p>
<p align="center"><em>Figura 10. Código usado para generar el mapa de calor de Grad-CAM sobre una imagen de prueba.</em></p>

<p align="center">
  <img width="990" height="356" alt="figura11_gradcam" src="https://github.com/user-attachments/assets/7fbf0201-9af3-437d-986e-c15593bc0cc8" />
</p>
<p align="center"><em>Figura 11. Grad-CAM sobre una imagen del set de prueba.</em></p>

Las zonas amarillas son las que más pesaron en la predicción, y las moradas las que casi no importaron. En este caso, el modelo se fijó en el centro de la botella, que tiene sentido porque ahí está la textura y forma del vidrio.

### Lo que aprendimos

- Entrenar una CNN desde cero con pocos datos y pocas épocas no siempre funciona: el modelo puede "hacer trampa" prediciendo siempre la misma clase.
- El transfer learning es una herramienta poderosa cuando no tenemos muchos datos propios, porque aprovechamos todo lo que un modelo grande ya aprendió antes.
- Grad-CAM nos ayuda a confiar (o desconfiar) de un modelo, porque muestra si realmente está mirando lo que debería mirar y no algo irrelevante del fondo de la imagen.

### Por qué es importante

Las CNN son la base de casi todo lo que hoy funciona con imágenes: cámaras de seguridad, diagnóstico médico por imágenes, autos autónomos, control de calidad en fábricas. Entender cómo se arma una y por qué a veces falla (como nos pasó con el modelo desde cero) es tan importante como saber usarla cuando funciona bien.

---

## 2. Clasificación binaria con Keras

### ¿Qué es y para qué sirve

Keras es una librería que permite armar y entrenar redes neuronales sin tener que programar cada operación matemática a mano. Uno arma la red por capas, como si fuera un molde, y Keras se encarga de todo el cálculo de gradientes y ajustes de pesos por detrás. Es ideal para ir directo al diseño del modelo sin perder tiempo en detalles de bajo nivel.

En nuestro ejercicio usamos Keras para un problema de texto: clasificar reseñas de películas del dataset IMDB como positivas o negativas.

### Funciones clave que usamos

- **Sequential**: es el "molde" donde vamos apilando las capas de la red, una tras otra, en orden.
- **Dense**: una capa donde cada neurona está conectada con todas las de la capa anterior. Es la capa más básica de una red.
- **activation='relu'**: la misma función de activación que vimos en la CNN, para las capas ocultas.
- **activation='sigmoid'**: convierte la salida en un número entre 0 y 1, perfecto para decir "probabilidad de que sea positiva".
- **compile**: define cómo se va a entrenar el modelo (optimizador, función de pérdida, métrica).
- **fit**: entrena el modelo con los datos.
- **Dropout** y **regularizers.l2**: técnicas para evitar que el modelo memorice de más los datos de entrenamiento.

<p align="center">
  <img width="1305" height="376" alt="image" src="https://github.com/user-attachments/assets/54d95d69-34cb-4ae3-bfff-5424edfd83d9" />
</p>
<p align="center"><em>Figura 12. Código para crear y compilar el modelo base (capas Dense + compile).</em></p>

### Lo que hicimos paso a paso

1. Descargamos el dataset de IMDB, que ya viene con las reseñas convertidas en secuencias de números (cada número representa una palabra).
2. Usamos el diccionario de palabras de Keras para poder leer una reseña real y entender qué estábamos clasificando.
3. Convertimos cada reseña en un vector de ceros y unos (one-hot encoding): un 1 si la palabra aparece en la reseña, un 0 si no.

<p align="center">
  <img width="1195" height="252" alt="image" src="https://github.com/user-attachments/assets/52e022cd-67f3-4001-8d67-44d7010650c8" />
</p>
<p align="center"><em>Figura 13. Código de la función de one-hot encoding usada para vectorizar las reseñas.</em></p>

4. Armamos el modelo base (2 capas ocultas de 16 neuronas) y lo entrenamos 20 épocas.

<p align="center">
  <img width="1211" height="380" alt="image" src="https://github.com/user-attachments/assets/635b9f5f-b186-472c-887f-70c44ac3717b" />
</p>
<p align="center"><em>Figura 14. Código para graficar la pérdida del modelo base.</em></p>

<p align="center">
  <img width="826" height="813" alt="figura15_perdida_base" src="https://github.com/user-attachments/assets/2d494a05-1336-4032-a96f-094eeefcc291" />
</p>
<p align="center"><em>Figura 15. Pérdida del modelo base.</em></p>

La curva azul (entrenamiento) baja todo el tiempo, pero la naranja (validación) baja al principio y después empieza a subir. Esto es sobreajuste: el modelo está memorizando las reseñas de entrenamiento en vez de aprender patrones generales, y por eso funciona cada vez peor con datos que no ha visto. Al evaluarlo en el set de prueba, dio un 86.1% de exactitud, con un nivel de error de 0.6.

5. Probamos un modelo más chico (4 neuronas en vez de 16) para ver si el sobreajuste cambiaba.

<p align="center">
  <img width="1296" height="403" alt="image" src="https://github.com/user-attachments/assets/622eecc2-e5b1-4933-9efb-7c66d1084737" />
</p>
<p align="center"><em>Figura 16. Código para comparar la validación del modelo original contra el modelo más pequeño.</em></p>

<p align="center">
  <img width="835" height="813" alt="figura17_comparacion_modelo_pequeno" src="https://github.com/user-attachments/assets/97d3b892-cad3-4347-a2ab-57015f39e21c" />
</p>
<p align="center"><em>Figura 17. Comparación con modelo más pequeño.</em></p>

Con menos neuronas, el modelo tiene menos "capacidad" para memorizar, así que el sobreajuste llega más tarde y es menos pronunciado. Esto confirma que el tamaño del modelo influye directamente en qué tan fácil se sobreajusta.

6. Probamos regularización L2, que penaliza los pesos muy grandes para que el modelo no dependa demasiado de unas pocas conexiones.

<p align="center">
  <img width="1502" height="407" alt="image" src="https://github.com/user-attachments/assets/7334f2fd-4898-4f87-bdc2-81389fc6e12b" />
</p>
<p align="center"><em>Figura 18. Código del modelo con regularización L2 (kernel_regularizer).</em></p>

<p align="center">
  <img width="1312" height="436" alt="image" src="https://github.com/user-attachments/assets/43b45f02-d2da-48b0-9dbb-93d42a07556d" />
</p>
<p align="center"><em>Figura 19. Código para graficar la comparación con regularización.</em></p>

<p align="center">
  <img width="826" height="813" alt="figura20_regularizacion" src="https://github.com/user-attachments/assets/bb559097-4019-47d1-8a3f-9be09a9d96a1" />
</p>
<p align="center"><em>Figura 20. Regularización L2.</em></p>

7. Probamos Dropout, que apaga aleatoriamente la mitad de las neuronas en cada paso de entrenamiento. Esto obliga a la red a no depender de neuronas específicas y a aprender de formas distintas de combinarlas [4].

<p align="center">
  <img width="1352" height="435" alt="image" src="https://github.com/user-attachments/assets/c47794ea-de53-4133-8fbf-af416f6f9638" />
</p>
<p align="center"><em>Figura 21. Código del modelo con capas de Dropout.</em></p>

<p align="center">
  <img width="1330" height="401" alt="image" src="https://github.com/user-attachments/assets/4aebafa4-bb1c-4678-a2f5-7bf5682fe62e" />
</p>
<p align="center"><em>Figura 22. Código para graficar la comparación con Dropout.</em></p>

<p align="center">
  <img width="835" height="813" alt="figura23_dropout" src="https://github.com/user-attachments/assets/255e396d-6303-42d5-afb5-f26318a64842" />
</p>
<p align="center"><em>Figura 23. Dropout.</em></p>

8. Finalmente, usamos el modelo para predecir reseñas nuevas. Por ejemplo, la reseña número 10 dio un valor de 99.4%, es decir, el modelo está casi seguro de que es una reseña positiva.

### Lo que aprendimos

- El sobreajuste es uno de los problemas más comunes al entrenar redes, y se nota claramente cuando la curva de validación empieza a subir mientras la de entrenamiento sigue bajando.
- Hay varias formas de pelear contra el sobreajuste: achicar el modelo, regularizar los pesos, o usar dropout. Ninguna es mágica, pero todas ayudan.
- Keras permite iterar rápido: armar, entrenar y comparar varios modelos en poco tiempo, lo que es clave para poder probar estas soluciones una por una.

### Por qué es importante

Keras (parte de TensorFlow) es una de las herramientas más usadas en la industria porque baja la barrera de entrada: no hace falta ser experto en el detalle matemático para construir modelos funcionales. Además, entender el sobreajuste es fundamental en cualquier proyecto real, porque un modelo que funciona perfecto en los datos de entrenamiento pero falla con datos nuevos, en la práctica, no sirve de nada.

---

## 🟣 Perceptrón

### ¿Qué es y para qué sirve

El perceptrón es el modelo más simple de red neuronal: una sola neurona que recibe varias entradas, las multiplica por unos pesos, suma todo (más un sesgo o "bias"), y aplica una función de activación para decidir una salida. Fue propuesto por Frank Rosenblatt en 1958 como un modelo simplificado de cómo el cerebro podría almacenar y organizar información [5]. Es la base conceptual de todo lo que vimos antes: una CNN o un modelo de Keras, en el fondo, son muchos perceptrones conectados entre sí en capas.

### Funciones clave que usamos

- **Suma ponderada + bias**: multiplica cada entrada por su peso, suma todo y le agrega el sesgo. Es el cálculo central del perceptrón.
- **Función escalón**: devuelve 1 si la suma ponderada es mayor o igual a 0, y 0 si es negativa. Es una decisión binaria, tipo "sí o no".
- **Función tanh**: transforma cualquier valor en un número entre -1 y 1, dando una salida más suave y gradual en vez de una decisión tajante.

<p align="center">
  <img width="1178" height="575" alt="image" src="https://github.com/user-attachments/assets/8cc4c612-2393-49e1-a321-dc1d2ff047ac" />
</p>
<p align="center"><em>Figura 24. Código de la función escalón, la función tanh y la función del perceptrón.</em></p>

### Lo que hicimos paso a paso

1. Simulamos un caso de sobrecalentamiento de un equipo industrial usando temperatura y vibración como entradas, con pesos y bias definidos a mano.
2. Comparamos la salida usando la función escalón contra la función tanh: la escalón dio una alerta clara (0 o 1), mientras que tanh dio un valor intermedio que también se puede interpretar como nivel de riesgo.
3. Armamos compuertas lógicas (AND, OR) ajustando los pesos y el bias del perceptrón, y probamos qué pasa con XOR.

<p align="center">
  <img width="991" height="677" alt="image" src="https://github.com/user-attachments/assets/90fd7de5-c41d-4c01-873e-e0e2473f50e2" />
</p>
<p align="center"><em>Figura 25. Código para graficar las fronteras de decisión de AND y OR.</em></p>

<p align="center">
  <img width="503" height="505" alt="figura26_and_or" src="https://github.com/user-attachments/assets/44dffb89-6b1b-46cd-98ae-fc90f091b3b0" />
</p>
<p align="center"><em>Figura 26. Fronteras de decisión AND y OR.</em></p>

Cada línea es la "frontera de decisión" de un perceptrón: todo lo que queda de un lado se clasifica como 1, y del otro lado como 0. Con AND, la línea separa el punto (1,1) del resto. Con OR, la línea separa el punto (0,0) del resto.

4. Con XOR (que da 1 solo cuando las entradas son distintas) nos encontramos con el límite real del perceptrón simple:

<p align="center">
  <img width="956" height="742" alt="image" src="https://github.com/user-attachments/assets/c0f855cd-c4ca-49e4-90d8-83797d3752df" />
</p>
<p align="center"><em>Figura 27. Código para graficar el intento de resolver XOR con un solo perceptrón.</em></p>

<p align="center">
  <img width="503" height="505" alt="figura28_xor" src="https://github.com/user-attachments/assets/902fea8a-c60a-4ce1-b49e-dbf9c898cf42" />
</p>
<p align="center"><em>Figura 28. Intento de XOR.</em></p>

No existe una sola línea recta que logre separar los círculos blancos (XOR = 0) de los puntos azules (XOR = 1). Un perceptrón solo no puede resolver XOR, porque XOR no es "separable linealmente". Este fue justamente uno de los límites que señalaron Minsky y Papert en 1969, y lo que frenó por años el desarrollo de las redes neuronales, hasta que se demostró que apilando varios perceptrones en capas (justo lo que hace una red neuronal moderna) sí se puede resolver [6].

### Lo que aprendimos

- Un perceptrón es, literalmente, una suma ponderada más una función de activación. Todo lo demás (CNN, Keras) es una versión más grande y sofisticada de esta misma idea.
- Los pesos y el bias son los que definen el comportamiento del perceptrón: cambiándolos, la misma estructura puede comportarse como AND, como OR, o como cualquier otra regla lineal.
- Un solo perceptrón tiene límites claros: no puede resolver problemas que no se pueden separar con una línea recta, como XOR. Para eso se necesitan varias capas.

### Por qué es importante

Entender el perceptrón es entender la base de todo. Antes de usar una librería como Keras o PyTorch, conviene saber qué está pasando en el fondo: una suma ponderada, un umbral, una decisión. Además, ver con nuestros propios ojos por qué falla en XOR ayuda a entender por qué las redes reales necesitan varias capas para resolver problemas más complejos.

---

## Cómo aplicaríamos esto en nuestro proyecto

Nuestro proyecto es un vigilante submarino que monitorea el biofouling (la capa de algas y organismos que se pega en las linternas donde crecen las conchas de abanico). El dispositivo usa un sensor de proximidad para calcular el volumen de biofouling pegado a las linternas, y dos cámaras ubicadas en los extremos de las linternas para monitorear también, con fotos, la cantidad de biofouling. El dispositivo solo mide y toma las fotos; el cálculo del volumen y el procesamiento se harían en la nube. Los resultados llegan a un aplicativo que muestra el volumen de biofouling, el porcentaje de batería (el dispositivo se alimenta con pilas y un panel solar) y las fotos tomadas.

El problema de fondo es que el biofouling compite con las conchas de abanico por los nutrientes: mientras más biofouling se pega a las linternas, menos nutrientes y oxígeno les quedan a las conchas, y su crecimiento se vuelve más lento. Además, sin un monitoreo constante, las empresas acuícolas gastan de más en mantenimiento, mandando gente a limpiar las linternas incluso cuando todavía no es necesario. Nuestro dispositivo resuelve esto avisando solo cuándo hace falta limpiar.

Estas tres técnicas encajan en distintos puntos del sistema:

**CNN, para leer las fotos de las cámaras.** Las dos cámaras en los extremos de las linternas toman fotos que muestran qué tan cubierta está la malla de biofouling. Una CNN puede procesar esas fotos y clasificar el nivel de suciedad (bajo, medio, alto), igual que en nuestro ejercicio separamos vidrio de plástico por su forma y textura. Como no vamos a tener miles de fotos submarinas propias para entrenar un modelo desde cero, la idea de transfer learning es clave: podríamos partir de un modelo ya entrenado en tareas de clasificación de imágenes y ajustarlo con las fotos que sí logremos recolectar en el mar.

**Keras, para armar y entrenar el modelo rápido.** En vez de programar cada capa a mano, usaríamos Keras para construir el modelo que clasifica el nivel de biofouling en las fotos, entrenarlo con los datos que vayamos juntando, y ajustarlo con dropout o regularización si notamos que memoriza de más (algo muy probable si tenemos pocas fotos reales de campo, igual que nos pasó con el modelo de IMDB).

**Perceptrón, para la lógica final de alerta.** Una vez que el sistema tiene el volumen de biofouling que mide el sensor de proximidad y el nivel de suciedad que detecta la CNN en las fotos, necesita decidir algo simple: ¿aviso o no aviso al acuicultor? Esa decisión final es, en el fondo, un perceptrón: se combinan variables (volumen de biofouling, nivel de suciedad en las fotos, tiempo desde la última limpieza) con ciertos pesos, se compara contra un umbral, y se genera una alerta de "linterna sucia, hay que limpiar" o "todo bien, no hace falta ir". Es la misma lógica que usamos para detectar sobrecalentamiento en el ejemplo del equipo industrial, solo que aplicada a las conchas de abanico.

Como el dispositivo solo se encarga de medir y tomar fotos, y todo el cálculo pesado (volumen, clasificación de imágenes) se haría en la nube, tiene sentido correr ahí mismo los modelos de CNN entrenados con Keras: así el dispositivo no gasta batería procesando imágenes bajo el agua, solo envía los datos crudos, y la nube devuelve el resultado ya listo para mostrarse en el aplicativo. El perceptrón final, al ser un cálculo simple, también podría correr en la nube junto con el resto.

En resumen, usaríamos las tres técnicas juntas: la CNN (armada y entrenada con Keras) para interpretar las fotos de las cámaras y convertirlas en un nivel de suciedad, y una capa final tipo perceptrón para combinar ese nivel con la lectura del sensor de proximidad y transformarlo en una alerta clara y accionable para el acuicultor.

---

## Referencias

[1] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, "Gradient-based learning applied to document recognition," *Proc. IEEE*, vol. 86, no. 11, pp. 2278–2324, Nov. 1998.

[2] K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016, pp. 770–778.

[3] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, "Grad-CAM: Visual explanations from deep networks via gradient-based localization," in *Proc. IEEE Int. Conf. Comput. Vis. (ICCV)*, 2017, pp. 618–626.

[4] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, "Dropout: A simple way to prevent neural networks from overfitting," *J. Mach. Learn. Res.*, vol. 15, no. 56, pp. 1929–1958, 2014.

[5] F. Rosenblatt, "The perceptron: A probabilistic model for information storage and organization in the brain," *Psychol. Rev.*, vol. 65, no. 6, pp. 386–408, 1958.

[6] M. Minsky and S. Papert, *Perceptrons: An Introduction to Computational Geometry*. Cambridge, MA, USA: MIT Press, 1969.
