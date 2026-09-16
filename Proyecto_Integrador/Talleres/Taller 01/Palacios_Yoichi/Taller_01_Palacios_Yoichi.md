# Diseño de la Pieza 4 en Onshape

Se diseñó este componente, el cual corresponde al módulo de cámara estándar del sistema, complementario al módulo de cámara gran angular de la Pieza 3. Se trata de una cápsula de 52 × 40 × 28 mm, con pared de 3 mm y una cavidad interior de 46 × 34 × 22 mm destinada a alojar la cámara. En la cara frontal cuenta con un asiento circular de Ø25 mm × 3 mm de profundidad para la ventana de acrílico y una apertura pasante de Ø20 mm para el lente. En la parte posterior incluye dos orejas de bisagra con perforación pasante de Ø4.2 mm para el perno M4 que une la cápsula al extremo de la barra estructural y permite el ajuste del ángulo de la cámara. El material de referencia es PETG impreso en 3D (tentativo).

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza_4_Onshape_Palacios.png" alt="Modelo CAD 3D de la Pieza 4" width="100%"/>
  <br>
  <em>Figura 7. Vista general del modelado 3D del módulo de cámara estándar en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo en Onshape](https://cad.onshape.com/documents/1204ec5c40a452e7a628bc6e/w/7f62edade57aa1332627dee5/e/4ab849edff8b72e1d308ae19)

---

# Simulación de Esfuerzos Mecánicos de la Pieza 4 en SimScale

Se realizó un análisis estático estructural de la cápsula. Se asignó material PETG ($E = 1700 \text{ MPa}$, $\nu = 0.38$, $\rho = 1270 \text{ kg/m}^3$; valores tentativos), una sujeción fija en las orejas de la bisagra, que constituyen la zona real de sujeción de la pieza, y una presión de $2500 \text{ Pa}$ sobre la cara frontal (caso de carga tentativo, equivalente a $\approx 5 \text{ N}$). El esfuerzo máximo de Von Mises resultó $\approx 1.02 \text{ MPa}$, concentrado en la zona de la bisagra por ser la sección delgada donde se reacciona la carga, valor muy por debajo del límite de fluencia del PETG ($45 \text{ MPa}$, tentativo), con amplio margen de seguridad.

#### Componentes del modelo analizado:
* **Cuerpo de la cápsula:** volumen principal de $52 \times 40 \times 28 \text{ mm}$ con pared de $3 \text{ mm}$, que aloja la cámara.
* **Ventana acrílica:** disco de $\varnothing 25 \text{ mm}$ asentado en la cara frontal sobre la apertura pasante de $\varnothing 20 \text{ mm}$ del lente.
* **Orejas de bisagra:** par de salientes posteriores con perforación pasante de $\varnothing 4.2 \text{ mm}$ para el perno M4, zona de sujeción a la barra estructural.

#### Configuración de Materiales y Fuerzas aplicadas:
* **Material Asignado:** PETG (Polietileno Tereftalato de Glicol), con densidad $\rho = 1270 \text{ kg/m}^3$, módulo de Elasticidad $E = 1700 \text{ MPa}$, coeficiente de Poisson $\nu = 0.38$ y límite elástico $\sigma_y = 45 \text{ MPa}$ *(tentativo)*. Fuente del datasheet del filamento: `[FUENTE PETG]`.
* **Sujeción fija (*Fixed Support*):** aplicada sobre las caras internas de las perforaciones de las orejas de bisagra, que es la zona real por la que la cápsula se une al extremo de la barra estructural mediante el perno M4.
* **Caso de carga 1 (*Pressure 1*, simulado en el Run 1):** presión uniforme de $2500 \text{ Pa}$ sobre la cara frontal, que modela el contacto de manipulación del operario sobre la ventana durante la instalación y el ajuste del ángulo. Sobre la cara útil de $46 \times 34 \text{ mm}$ equivale a $\approx 4 \text{ N}$.
* **Caso de carga 2 (tracción manual e izado, pendiente de correr como Run 2):** tracción de $150 \text{ N}$ aplicada en las orejas de bisagra con la misma sujeción, según la fila *Fuerzas* de la Lista de Exigencias, que exige resistencia a la tracción manual e izado mayor a $150 \text{ N}$. Es un caso distinto del anterior: el caso 1 representa contacto sobre la ventana y el caso 2 el izado por el cabo de suspensión.
* **Aceleración de Gravedad ($g$):** configurada globalmente en el árbol del proyecto (*Model*) con un valor de $9.81 \text{ m/s}^2$ orientada en dirección vertical hacia abajo (**eje `[EJE]`** del sistema de coordenadas), con el fin de considerar el peso propio de la pieza durante su operación. Como la bisagra permite ajustar el ángulo de la cámara, la orientación de instalación no es fija: se adopta la condición más desfavorable para las orejas de bisagra, es decir, la cápsula girada hacia abajo, con el centro de masa más alejado del eje del perno.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza_4_SimScale_Palacios.png" alt="Simulación de Esfuerzos de la Pieza 4" width="100%"/>
  <br>
  <em>Figura 8. Distribución de esfuerzos de Von Mises sobre el módulo de cámara en SimScale.</em>
</p>

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller1_Palacios_Malla.png" alt="Malla de elementos finitos de la Pieza 4" width="100%"/>
  <br>
  <em>Figura 9. Malla de elementos finitos generada sobre la cápsula en SimScale.</em>
</p>

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller1_Palacios_Condiciones.png" alt="Condiciones de borde de la Pieza 4" width="100%"/>
  <br>
  <em>Figura 10. Condiciones de borde: sujeción fija en las orejas de bisagra y presión sobre la cara frontal.</em>
</p>

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller1_Palacios_Desplazamiento.png" alt="Desplazamiento de la Pieza 4" width="100%"/>
  <br>
  <em>Figura 11. Distribución de desplazamientos de la cápsula bajo el caso de carga 1.</em>
</p>

#### Resultados obtenidos:

| Magnitud | Caso 1 (presión $2500 \text{ Pa}$, Run 1) | Caso 2 (tracción $150 \text{ N}$, Run 2) |
|---|---|---|
| Esfuerzo máximo de Von Mises | $\approx 1.02 \text{ MPa}$ | `[VON MISES CASO 2]` |
| Desplazamiento máximo | `[DESPLAZAMIENTO MÁX]` | `[DESPLAZAMIENTO CASO 2]` |
| Factor de seguridad ($\sigma_y / \sigma_{max}$) | $\approx 44$ | `[FS CASO 2]` |

> **Nota:** el factor de seguridad de $45 / 1.02 \approx 44$ debe leerse como **cota superior**. Corresponde únicamente al caso de carga 1 y todavía no incorpora el peso propio por gravedad ni el caso de carga 2 de tracción e izado, que es el gobernante según la Lista de Exigencias. El valor definitivo se fija tras correr el Run 2.

* **Enlace a la simulación en SimScale:** [Ver simulación interactiva en SimScale](https://www.simscale.com/workbench/?pid=3299755565309640234&mi=spec:3e3994b8-5e2c-4c4c-9b08-0920f9426825%2Cservice:SIMULATION%2Cstrategy:1)

---
