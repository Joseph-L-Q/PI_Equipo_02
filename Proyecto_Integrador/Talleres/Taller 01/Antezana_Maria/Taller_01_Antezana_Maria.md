# Diseño de la Pieza 5 en Onshape

Se diseñó la **tapa superior de acceso** a la pieza principal (pieza 1 y 2). Esta pieza cuenta con una geometría plana con bordes ajustados para un encaje sellado (*press-fit*) y una manija central ergonómica para facilitar la apertura y el mantenimiento en campo por parte del operario.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/pieza%205_OneShape_Antezana.png" alt="Modelo CAD 3D de la Tapa" width="100%"/>
  <br>
  <em>Figura 1. Vista del modelado 3D de la tapa en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo interactivo en Onshape](https://cad.onshape.com/documents/92c43fa99b5db15195bb939b/w/b8fcf09428ae9fe8132781fd/e/07d8c02eb93c5e076a980b94?renderMode=0&uiState=6a90e4f97b02dbf7abc36dcd)

---

# Simulación de Esfuerzos Mecánicos de la Pieza 5 en SimScale

Se realizó un Análisis Estructural Estático (*Static Structural Analysis*) en SimScale para validar la resistencia mecánica de la tapa frente a la presión hidrostática del agua de mar, los efectos del peso propio durante la inmersión y las corrientes marinas. Se configuró una sujeción fija (*Fixed Support*) en los 4 bordes laterales que encajan en la estructura de la pieza central y una carga de presión uniforme (*Pressure Load*) de $50\,000 \text{ Pa}$ ($50 \text{ kPa} / 0.5 \text{ bar}$) sobre la cara exterior. La simulación arrojó un esfuerzo máximo de Von Mises de $5.157 \times 10^5 \text{ Pa}$ ($0.516 \text{ MPa}$), el cual es significativamente menor al límite elástico del PETG ($50 \text{ MPa}$). Esto confirma un factor de seguridad elevado, garantizando que la tapa no sufrirá deformaciones plásticas ni fallas mecánicas bajo las condiciones de trabajo estipuladas.

#### Configuración de Materiales y Fuerzas aplicadas:
* **Material Asignado:** PETG (Polietileno Tereftalato de Glicol), con densidad $\rho = 1270 \text{ kg/m}^3$, módulo de Elasticidad $E = 2.1 \text{ GPa}$, coeficiente de Poisson $\nu = 0.38$ y límite elástico $\sigma_y = 50 \text{ MPa}$.
* **Presión Hidrostática (*Pressure 2*):** Carga uniforme de $50\,000 \text{ Pa}$ ($50 \text{ kPa} / 0.5 \text{ bar}$) aplicada sobre la cara exterior expuesta al medio marino.
* **Aceleración de Gravedad ($g$):** Configurada globalmente en el árbol del proyecto (*Model*) con un valor de $9.81 \text{ m/s}^2$ orientada en dirección vertical hacia abajo (**eje $-Z$** del sistema de coordenadas, **e_z = -1** en la configuración de SimScale), con el fin de considerar el peso propio de la pieza durante su operación.

<p align="center">
  <img src="---" alt="Simulación de Esfuerzos Von Mises" width="100%"/>
  <br>
  <em>Figura 2. Mapa de distribución de esfuerzos de Von Mises en la Pieza 5 mediante SimScale.</em>
</p>

* **Enlace a la Simulación Interactiva en SimScale:** [Ver simulación interactiva en SimScale](https://www.simscale.com/workbench/?pid=8438599269814585137&rru=d7d0d725-1333-4844-920a-74b9c6da085f&ci=ac29b1a3-ab57-41ae-adaf-43ad37a850cd&mt=SIMULATION_RESULT&ct=SOLUTION_FIELD)
