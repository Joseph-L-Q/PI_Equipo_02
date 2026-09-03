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

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza_4_SimScale_Palacios.png" alt="Simulación de Esfuerzos de la Pieza 4" width="100%"/>
  <br>
  <em>Figura 8. Distribución de esfuerzos de Von Mises sobre el módulo de cámara en SimScale.</em>
</p>

* **Enlace a la simulación en SimScale:** [Ver simulación interactiva en SimScale](https://www.simscale.com/workbench/?pid=3299755565309640234&mi=spec:3e3994b8-5e2c-4c4c-9b08-0920f9426825%2Cservice:SIMULATION%2Cstrategy:1)

---
