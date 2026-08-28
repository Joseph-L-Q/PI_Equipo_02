---

## Diseño de la Pieza 6 en Onshape

Se diseñó este componente como parte de la estructura interna del sistema. La pieza cuenta con una geometría tipo caja y presenta soportes internos elevados, cuya función es sostener y mantener en posición los componentes que serán colocados en su interior. Estos soportes permiten distribuir el peso de los elementos instalados y evitar que se encuentren directamente apoyados sobre la base de la carcasa.

El modelo fue desarrollado en Onshape considerando las dimensiones necesarias para su integración con las demás piezas del sistema y dejando el espacio adecuado para la colocación de los componentes internos.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza%206_Onshape_Lombardi.png" alt="Modelo CAD 3D de la Pieza 6" width="100%"/>
  <br>
  <em>Figura 11. Vista general del modelado 3D de la Pieza 6 en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** https://cad.onshape.com/documents/dd5b7649926b850f58e3a0cd/w/3415aad3ec89db9e80203726/e/ca9610162541ef929950109f?renderMode=0&uiState=6a91154ceb1494b0c65417ee

---

## Simulación de Esfuerzos Mecánicos de la Pieza 6 en SimScale

Para evaluar la resistencia de la pieza se realizó una simulación estructural estática en SimScale utilizando PETG como material. Se estableció una sujeción fija (*Fixed Support*) en la zona de apoyo de la estructura y se aplicó una carga sobre los soportes internos para representar el peso que podrían ejercer los componentes colocados sobre ellos.

Para la simulación se utilizó una carga de referencia de aproximadamente $10 \text{ N}$, permitiendo observar cómo se distribuyen los esfuerzos a través de los soportes y del resto de la estructura.

Los resultados fueron evaluados mediante el esfuerzo equivalente de Von Mises. En el mapa de colores se observa que la mayor parte de la pieza permanece en tonalidades azules y celestes, correspondientes a esfuerzos relativamente bajos, mientras que las zonas amarillas y rojas representan puntos donde el esfuerzo se concentra principalmente alrededor de los soportes y sus uniones con la estructura.

El esfuerzo máximo obtenido en la simulación fue aproximadamente de $2.129 \times 10^6 \text{ Pa}$ ($2.13 \text{ MPa}$). Este valor es considerablemente menor al límite elástico aproximado del PETG, de alrededor de $50 \text{ MPa}$, por lo que bajo las condiciones evaluadas la pieza puede soportar la carga aplicada sin presentar una falla estructural.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza%206_SimScale_Lombardi.png" alt="Simulación estructural de la Pieza 6" width="100%"/>
  <br>
  <em>Figura 12. Distribución de esfuerzos de Von Mises obtenida en la simulación estructural de la Pieza 6 en SimScale.</em>
</p>


---
