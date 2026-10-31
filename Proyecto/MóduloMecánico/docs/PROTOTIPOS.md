# Prototipos del nodo P0 a P4 (bloque B, 30/10)

Comparacion de los cinco puntos de partida y los cuatro prototipos nuevos sobre el aro de prueba Ø200. Todo sale del mismo codigo
(`cad_final/simple.py`, banderas de `params.proto.perfiles`); cada prototipo tiene su carpeta con ficha, STEP, STL, renders, G-code (no versionado),
`slicer.json` y `fem/fem.json`: `salida/prototipos/<P1_minimo|P2_robusto|P3_monocasco|P4_estetico>/` (ver `FICHA.md` de cada una).

## Como se regenera

```
python cad_final/build.py --prototipo P1_minimo        # ciclo completo: CAD, slicer, FEM y ficha (~2 a 3 min)
python cad_final/build.py --prototipo P3_monocasco --fem   # un solo paso (--rapido, --slicer, --fem)
LG_VERSION=P2_robusto python cad_final/simple.py       # mismo efecto sin build.py; LG_VERSION pisa params.version
```

`params.version = "simple"` sigue siendo el nodo V2 de referencia y escribe donde siempre (`salida/simple/`); `"modular"` no cambia. Los prototipos no tocan la bitacora,
MEDIDAS.md ni `salida/simscale/`. `P1_minimo` pisa al importar unos pocos valores de `params.py` (`proto.sobreescrituras`).

## Tabla

Masa, horas y costo = gramos y horas de OrcaSlicer (P1P, PETG, 0.2 mm) por pieza x cantidad, sin pletinas ni tornilleria, ventanas de acrilico ni linterna; costo a S/ 90 el kg (`costo.petg_soles_kg`,
estimado). FS = FEM local con 150 N en una capsula (percentil 99.5 de von Mises, PETG isotropico estimado), a lo largo de las capas / entre capas. "Riel" = riel con el asiento del gancho fijo (caso `riel_agua`),
"pie" = pie de la capsula. El peso aparente es en agua de mar, bandeja al 40 %.

| | P0 simple V1 | P0 modular | V2 (ref.) | P1 minimo | P2 robusto | P3 monocasco | P4 estetico |
|---|---|---|---|---|---|---|---|
| Masa impresa g | 1248 | 1285 (estimado) | 1358 | **1302** | 1381 | 1335 | 1332 |
| Horas | 45.1 | 55.1 (estimado) | 47.0 | **45.2** | 47.3 | 45.7 | 45.8 |
| Costo S/ | 112 | 116 | 122.3 | **117.2** | 124.3 | 120.1 | 119.9 |
| FS riel | 6.9 / 3.4 (a mano) | 1.3 / 0.6 union (a mano) | 5.4 / 2.6 | 3.9 / **1.9** | 5.6 / 2.7 | 4.8 / 2.3 | 4.7 / 2.3 |
| FS pie | 2.5 / 1.2 (a mano) | sin FEM | 5.0 / 2.5 | 5.4 / 2.6 | 5.0 / 2.5 | 5.5 / 2.7 | 5.5 / 2.7 |
| Piezas impresas por nodo | 17 | 28 | 14 | 14 | 14 | 14 | 14 |
| Sellos estancos | 7 | ver ficha P0 | 9 | 9 | 9 | 9 | 9 |
| Juntas atornilladas (no estancas) | ver ficha P0 | ver ficha P0 | 4 | 4 | 4 | 4 | 4 |
| Peso en aire g | 2079 | 2048 | 2462 | 2415 | 2678 | 2475 | 2471 |
| Peso aparente g (ventana 200 a 500) | +265 | +225 | +205 | +277 | +373 | +238 | +238 |
| Caja exterior mm | 139.6 x 106 x 50 | ver ficha P0 | 127 x 126 x 77 | 119 x 128 x 77 | 127 x 126 x 77 | 127 x 126 x 77 | 127 x 126 x 77 |

Las columnas P0 vienen de `salida/prototipos/P0_original/simple_V1/FICHA.md` y `modular/FICHA.md`; sus FS son calculos a mano (el FEM local llego con la V2) y su metodo de contar sellos no incluye los PG7
de las capsulas, por eso 7 contra 9. Detalles de P0 en esas fichas.

Sellos de P1 a P4 (9): tapa de la caja, 2 tapas de capsula, 2 ventanas, 2 PG7 de la caja, 2 PG7 de capsula. Juntas atornilladas (4): V2, P1, P2 = 2 bridas riel-caja + 2 pies M4; P3 y P4 = 2 uniones de extremo + 2 abrazaderas M4;
no cuentan las tapas del bolsillo ni los tornillos de las tapas. **Ningun prototipo reduce el numero de sellos**: la union riel-caja y las del riel van dentro del conducto inundado y no son estancas.

## Que es cada uno y que se aprendio

- **P1 minimo.** Celosia triangular en las paredes del conducto (6 ventanas por mitad), pared 3.5, gancho snap-fit, caja de 119 x 128 con holguras de 3 mm y zonas USB/microSD recortadas (estimadas), capsula con
  cavidad de 36 en vez de 38. **Ahorra 56 g (4 %) y 1.8 h respecto de V2, pero su FS entre capas del riel es 1.9, bajo el 2 que se usa de criterio.** Ademas la fuerza de insercion y la fatiga del snap no estan calculadas: requiere probeta.
- **P2 robusto.** V2 con la celosia (6 ventanas por mitad) y pared 5. Para entrar en la ventana de peso aparente hubo que ir a 6 pletinas por bolsillo (bolsillo de capacidad 6, `capacidad` y `pletinas` en el perfil), por eso
  pesa mas en aire (2678 g) y en el agua (+373 g, dentro de 200 a 500). Es el mas fuerte (5.6 / 2.7).
- **P3 monocasco.** Caja y los dos tramos de riel con sus ganchos en una sola pieza de 250 x 146 x 118 (cabe en la cama de 256), corte en |x| = 125; los extremos con pie y tapa de capsula en una pieza (M5m), unidos con la brida de 4 M4 del patron
  existente; ganchos de abrazadera con tornillo. Sin insertos M4 en los cojines de la caja. Ahorra solo 23 g (1.7 %) frente a V2: la celosia solo cabe en los tramos libres y el 100 % de relleno de M1m (caja sellada) arrastra los tramos de riel,
  que en V2 iban al 40 %. M1m son 661 g y 23 h en una sola impresion con soportes (22 600 mm2 de voladizo): si falla, se pierde mucho.
- **P4 estetico.** Parte de P3 (mejor FS entre capas con peso bajo entre los que cumplen FS >= 2). Radio de 3 mm en las aristas largas del conducto del riel, en el borde superior de la tapa y bajo la brida de la caja,
  logo "LanternGuard" en relieve de 0.6 mm sobre la tapa. Material: **-0.2 %** respecto de P3 (los redondeos quitan lo que el logo pone), muy por debajo del tope de +15 %.

## Lo que no salio como se pedia

- **Celosia.** Las paredes laterales solo se pueden aligerar en los tramos libres (fuera de brida, silla de la capsula, punta): 6 ventanas por mitad en P1 y P2, 2 + 1 en P3 y P4. El ahorro de masa por la celosia es de pocos gramos;
  la mayor parte del ahorro de P1 viene de la caja y la capsula mas pequenas.
- **Redondeos de P4.** Las esquinas verticales de la caja y las aristas largas de la capsula ya son redondeadas en el diseno base, asi que el fileteado de esquinas no aplica. Un redondeo de 3 mm en el borde frontal de la capsula y en la tapa M5 parte
  el cuerpo en varias piezas en el asiento del bisel (probado, se descarto); el perfil de la capsula queda como en V2. "Lineas continuas entre caja y riel" no se implemento (no hay loft): solo coinciden los radios.
- **Logo.** OCCT marca el texto (curvas B-spline) en la verificacion de operaciones booleanas; la tapa M2 de P4 se acepta con B-rep valido, estanca y de un solo cuerpo, y esa unica verificacion exonerada queda anotada en `simple.py`. Falta ver el logo impreso.
- **Mosqueton.** Documentado en `ENGANCHES.md`, no construido.
- **Snap (P1):** sin probeta. **Abrazadera (P3, P4):** la red de la linterna de prueba pasa por la media luna y ese chequeo se omite para M9c.
- Todo FS es del FEM local con PETG isotropico estimado: no hay ensayo, y no dice nada de estanqueidad.

## Recomendacion (cerrada)

- **Para las pruebas en piscina: P2_robusto.** Es el unico con FS >= 2.5 en todos los casos entre capas, usa piezas pequenas (riesgo de impresion bajo, sin una pieza de 23 h), conserva el gancho en C con ranura para la correa de 25 mm y el
  peso aparente (+373 g) esta dentro de la ventana. Cuesta 23 g y 0.3 h mas que V2 (+1.7 %) y 56 g mas que P1.
- **Para presentar: P4_estetico.** Menos uniones (sin insertos M4 en la caja ni rieles atornillados a ella), tapa con logo y bordes redondeados, FS minimo 2.3, y masa y horas casi iguales a V2.
  Antes de mostrarla impresa hay que ver el logo y probar que M1m sale entera.
- Descartados: P1 (FS entre capas 1.9 y snap sin probeta) y P3 (P4 es P3 con acabado y mismo costo).
- Efecto de elegir otra cosa: P1 en vez de P2 ahorra S/ 7 y 2 h, pero baja el FS entre capas del riel de 2.7 a 1.9; P3 en vez de P2 ahorra S/ 4 y 1.6 h, pero concentra 23 h en una sola pieza.

## Parametros nuevos (todos en `params.py`, estimados salvo indicacion)

`proto.perfiles` (banderas por version), `proto.sobreescrituras` (P1), `proto.celosia`, `proto.snap`, `proto.abrazadera`, `proto.corte_x`, `proto.redondeos`, `proto.logo`, `costo.petg_soles_kg` (90, estimado).
Se estiman y hay que confirmar: `aro.seccion` (8 mm), las holguras de la caja y la capsula de P1, los radios y la apertura del snap, el PETG.
