# Lo que aprendí sobre las CNN

En la primera parte del notebook aprendí qué es una **CNN** o red neuronal convolucional. Este tipo de red se usa para analizar imágenes. Sus filtros recorren los píxeles y van detectando características como bordes, formas y texturas. También vimos que **ReLU** ayuda a la red a aprender relaciones más complejas y que **MaxPool** reduce el tamaño de la información que se está procesando.

![Esquema de la CNN que aparece al inicio del notebook](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20161807.png)

Para ponerlo en práctica usamos imágenes de **vidrio y plástico** del conjunto de datos TrashNet. Primero se cargaron las imágenes en escala de grises y se dividieron en tres grupos: **entrenamiento**, para que la red aprenda; **validación**, para revisar cómo va aprendiendo; y **prueba**, para evaluar el resultado final con imágenes que no usó durante el entrenamiento.

![Ejemplos de imágenes de vidrio y plástico mostradas en el notebook](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162024.png)

Después construimos una CNN desde cero y la entrenamos durante ocho épocas. Una época significa que el modelo pasó una vez por los datos de entrenamiento. Revisamos la **pérdida**, que indica el error del modelo, y la **exactitud**, que indica cuántas imágenes clasificó correctamente. La pérdida de entrenamiento fue bajando y la exactitud de validación llegó a **63,27 %**, pero en el conjunto de prueba obtuvo **55,03 %**. Entendí que mejorar durante el entrenamiento no siempre significa que el modelo vaya a funcionar igual de bien con imágenes nuevas.

![Gráfica de pérdida de entrenamiento de la CNN](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162411.png)

![Gráfica de exactitud y ROC-AUC de validación](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162417.png)

También revisamos una **matriz de confusión**. Esta nos deja ver los aciertos y errores por separado: cuántas imágenes de vidrio se clasificaron como vidrio, cuántas se confundieron con plástico y lo mismo para las imágenes de plástico. Así entendí mejor los resultados, porque una sola cifra de exactitud no muestra en qué clase se equivoca el modelo.

![Matriz de confusión de la CNN entrenada desde cero](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162426.png)

Luego probamos el **aumento de datos** (*data augmentation*). Consistió en aplicar pequeñas rotaciones y desplazamientos a las imágenes de entrenamiento para que la red viera más variaciones. La exactitud en prueba subió un poco, de **55,03 % a 56,38 %**. En este caso ayudó, aunque la mejora fue pequeña.

La mejora más grande llegó cuando usamos **ResNet18**. Esta red ya había sido entrenada con muchas imágenes, así que aprovechamos lo que había aprendido y adaptamos sus últimas capas para distinguir vidrio de plástico. Primero entrenamos la capa final y después ajustamos también una de sus últimas partes. Con este modelo obtuvimos **86,58 % de exactitud** en prueba. Aprendí que usar una red preentrenada puede dar mejores resultados cuando tenemos una cantidad limitada de imágenes.

Por último, usamos **Grad-CAM** para generar un mapa de calor sobre una imagen. Las zonas más resaltadas muestran qué partes influyeron más en la predicción de ResNet18. Esto sirve para observar en qué se fijó el modelo, aunque el mapa por sí solo no asegura que haya clasificado bien. Al final también guardamos los modelos para poder recuperarlos sin entrenarlos otra vez.

![Imagen original, mapa Grad-CAM y superposición](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/ce2cf0d0b135a149e0c698f04cf2ff8137af02b1/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162820.png)
