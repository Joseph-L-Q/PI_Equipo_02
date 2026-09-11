# Diseño de la Pieza 3 en Onshape

Se diseñó este componente, correspondiente a la carcasa de la cámara del sistema de monitoreo submarino. La pieza cuenta con una estructura tipo caja con una tapa superior para proteger los componentes internos frente a las condiciones del entorno marino. Asimismo, presenta una perforación lateral destinada al paso de conexiones y fue diseñada considerando su integración con los demás componentes del sistema.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza3_Onshape_Santamaria.png" alt="Modelo CAD 3D de la Pieza 3" width="100%"/>
  <br>
  <em>Figura 5. Vista general del modelado 3D de la carcasa de la cámara en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo en Onshape](https://cad.onshape.com/documents/abaf97f135b791090d5654a3/w/1b2e7b3ab154f4d4ad8ff047/e/2992f9c7802c3002f6d76ee6)

---

# Simulación de Esfuerzos Mecánicos de la Pieza 3 en SimScale

Se analizó el comportamiento estructural de la pieza asignando material PETG ($\rho = 1270 \text{ kg/m}^3$, $E = 2.1 \text{ GPa}$, $\nu = 0.38$). Mediante un análisis estático, se consideraron las condiciones de operación a las que estaría sometida la carcasa de la cámara dentro del entorno submarino.

Para la simulación se establecieron las siguientes condiciones de carga:

- **Sujeción fija:** aplicada en las zonas de unión de la carcasa, representando los puntos donde la pieza se encuentra asegurada al sistema.
- **Presión externa uniforme:** de $50\,000 \text{ Pa}$ ($0.5 \text{ bar}$) aplicada sobre las caras exteriores expuestas, representando la presión generada por el entorno marino.
- **Gravedad:** se consideró una aceleración gravitacional de $9.81 \text{ m/s}^2$ en dirección vertical hacia abajo (**eje -Y del sistema de coordenadas**), con el objetivo de incluir el efecto del peso propio de la carcasa durante las condiciones de operación.

Los resultados de la simulación permiten evaluar la resistencia mecánica de la carcasa mediante el esfuerzo equivalente de Von Mises, verificando que la pieza soporta adecuadamente las cargas aplicadas durante las condiciones previstas de funcionamiento.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza3_SimScale_Santamaria.png" alt="Simulación de Esfuerzos de la Pieza 3" width="100%"/>
  <br>
  <em>Figura 6. Mapa de resultados de la simulación estructural en SimScale para la carcasa de la cámara.</em>
</p>

* **Enlace a la simulación en SimScale:** [Ver simulación interactiva en SimScale](https://www.simscale.com/workbench/?pid=3625990943939288531)

---
