# SimScale, version simple (pasos manuales; el plan gratuito no tiene API)

Generado por `cad_final/fem.py`. Mismos casos que el FEM local (Gmsh + CalculiX, `salida/simple/fem/fem.json`), para comparar. Unidades mm, N, MPa. No se afirma estanqueidad por simulacion.

| Archivo | Pieza |
|---|---|
| `simple_M3s_riel_gancho.step` | Mitad del riel con el gancho en C (la otra mitad es la misma, girada) |
| `simple_M5s_capsula_tapa_pie.step` | Tapa de la capsula con el pie en silla |

## Pasos comunes

1. SimScale → New Project → Import CAD → elegir el STEP, unidad **mm**.
2. Create Simulation → **Static**. Analysis type lineal, pequenos desplazamientos.
3. Materials → New → nombre PETG, Linear elastic isotropic: E = 1700 MPa, ν = 0.38, densidad 1270 kg/m³ (todo estimado, `params.py`). Asignar a todo el volumen.
4. Mesh → Standard, **second order**, tamano maximo 2.5 mm (o fineness 7).
5. Result control → von Mises y desplazamiento total.

## Casos

Carga en los tres: **Remote force** de 150 N en −Z aplicada en el punto (x, y, z) = (132.7, 0.0, -61.6) mm (frente de la capsula), comportamiento **deformable**, sobre las caras indicadas.

| Caso | STEP | Fijo (Fixed support) | Caras de la remote force | FEM local |
|---|---|---|---|---|
| riel_agua | M3s | Cara interior de la C del gancho (cilindro de radio 4.4 centrado en x = 100.0, z = -41.3) | Los 2 agujeros M4 de la silla (cilindros a x = 170.0 y 200.0, z = 18.7) | 2.51 mm, 8.4 MPa (p99.5), FS 5.4 / 2.6 |
| riel_izado | M3s | Cara plana de la brida contra el cojin de la caja (x = 73.5) | Los 2 agujeros M4 de la silla | 0.25 mm, 4.1 MPa (p99.5), FS 10.9 / 5.3 |
| pie | M5s | Los 2 agujeros M4 de la silla | Los 4 agujeros M3 de la tapa | 0.48 mm, 8.9 MPa (p99.5), FS 5.0 / 2.5 |

FS = 45 MPa (a lo largo de las capas) / σ y 22 MPa (entre capas) / σ, con σ el percentil 99.5 de von Mises: los picos en las caras fijas y en los agujeros de la remote force son efecto del modelo. Si SimScale da valores mas de 20 % distintos, revisar que la remote force sea deformable y las caras sean las mismas.
