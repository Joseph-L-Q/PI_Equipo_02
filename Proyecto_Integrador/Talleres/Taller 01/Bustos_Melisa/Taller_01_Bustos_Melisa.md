# Diseño de la Pieza 1 en Onshape

Se diseñó este componente, el cual corresponde a una de las mitades de la pieza central de la estructura. Cuenta con una perforación circular destinada al paso y conexión de los cables hacia la pieza 3 (una de las cajas de las cámaras). Asimismo, incluye una cavidad rebajada que representa la mitad del compartimento donde se estarán el microcontrolador ESP32 y las baterías. La pieza está diseñada para unirse mediante encaje directo con la pieza 2.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza1_Onshape_Bustos.png" alt="Modelo CAD 3D de la Pieza 1" width="100%"/>
  <br>
  <em>Figura 1. Vista general del modelado 3D de la carcasa principal en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo en Onshape](https://cad.onshape.com/documents/823093ea5158517335111a07/w/534bbd9bcc4404bff8c5c0c9/e/e0badff72f909b6f093e9bcc)

---

# Simulación de Esfuerzos Mecánicos de la Pieza 1 en SimScale

Se analizó el comportamiento de la pieza asignando material PETG ($\rho = 1270 \text{ kg/m}^3$, $E = 2.1 \text{ GPa}$, $\nu = 0.38$). Mediante un análisis estático, se aplicó una sujeción fija en la cara posterior de unión y una presión hidrostática externa de $50\,000 \text{ Pa}$ ($0.5 \text{ bar}$) sobre las 5 caras exteriores. Los resultados de la simulación muestran que el esfuerzo máximo de Von Mises alcanza un valor pico de $2.129 \times 10^6 \text{ Pa}$ ($2.13 \text{ MPa}$), concentrándose principalmente en la zona interna de la cavidad. Este valor se encuentra muy por debajo del límite elástico del PETG ($50 \text{ MPa}$), lo que confirma que la estructura soporta adecuadamente las cargas del entorno marino sin riesgo de deformaciones plásticas ni fallas.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza1_Simscale_Bustos.png" alt="Simulación de Esfuerzos de la Pieza 1" width="100%"/>
  <br>
  <em>Figura 2. Mapa de resultados de la simulación estructural en SimScale para la carcasa.</em>
</p>

* **Enlace a la simulación en SimScale:** [Ver proyecto en SimScale](https://www.simscale.com/workbench/?pid=3635885982911573950&rru=f8fc2047-d041-48a8-847e-e0277bf55f11&ci=23f6dcd0-09fd-4092-b64b-868768afe6a9&mt=SIMULATION_RESULT&ct=SOLUTION_FIELD)

---
