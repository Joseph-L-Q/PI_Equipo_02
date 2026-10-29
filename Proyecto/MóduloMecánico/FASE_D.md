# Fase D: ensambles

`cad_final/ensambles.py` arma el nodo completo para Ø100, Ø200, Ø300 y Ø500 (más una variante de Ø100 con 1 extensión)
con la linterna de referencia: aro de varilla Ø8, 4 cuerdas Ø4 a 45, 135, 225 y 315° que suben a un ápice sobre el eje, y
una red esquemática (cáscara cilíndrica de 1 mm). Reporte completo: `cad_final/reporte_ensambles.md`. Renders en
`salida/ensambles/` (`ensamble_D{aro}_iso.png` y `_lado.png`). Los STEP de ensamble (8 MB cada uno) no van al repo:
se regeneran con `python ensambles.py`.

## Resultado principal: con las piezas actuales el nodo no se puede armar en ningún aro

El carro y la cápsula tienen que ir **más allá del gancho**: la manga del carro no puede compartir la ranura T con la
brida del gancho, y la cápsula cuelga 34 bajo el riel, a la altura de la mandíbula. `largo_riel.py` lo mide a lo largo
del riel, sin CAD:

- la brida del gancho termina 3 mm afuera del centro de la varilla; la manga del carro (60) arranca 1 mm después;
- por eso la punta del riel tiene que llegar a **R + 64** como mínimo (carro a ras de la punta), y a R + 164 para usar
  todo el recorrido de ±50.

| Aro | Punta necesaria mm | Punta actual mm (extensiones solapadas 15) | Falta mm | Con extensiones a paso 100 | Menor n que alcanza (solapadas / paso 100) |
|---|---|---|---|---|---|
| Ø100 | 114 | 70 (0 ext.) | 44 | 70, falta 44 | 1 / 1 |
| Ø200 | 164 | 155 (1 ext.) | 9 | 170, sobra 6 | 2 / 1 |
| Ø300 | 214 | 155 (1 ext.) | 59 | 170, falta 44 | 2 / 2 |
| Ø500 | 314 | 240 (2 ext.) | 74 | 270, falta 44 | 3 / 3 |

**Esto es una contradicción en la especificación, y la decide el equipo.** La tabla del prompt (0 / 1 / 2 extensiones →
230 / 430 / 630) pone la punta en 115, 215 y 315: justo R + 65 del aro mayor de cada rango, lo que pide el gancho + el
carro. Pero con un tramo central de 140 y extensiones de 100 no se llega a esos largos de ninguna forma: solapando la
unión salen 140 / 310 / 480, y sin solapar 140 / 340 / 540. A la base le faltan 90 (45 por lado).
**¿El tramo central mide 140 o el riel de Ø100 mide 230? Las dos cosas no pueden ser.**

Salidas posibles, ninguna aplicada (los parámetros `riel.paso_extension` y `riel.regla_extensiones` están preparados
con el valor actual por defecto):

1. Una **pieza de punta** de 45 + 15 de unión por lado (60, entra en la cama) y extensiones a paso 100: da exactamente la
   tabla del equipo con 0 / 1 / 2 extensiones.
2. Extensiones a paso 100 (lengüeta macho fuera del cuerpo, pieza de 115) y una extensión más en Ø100, Ø300 y Ø500.
3. Regla automática con las extensiones actuales: 1 / 2 / 2 / 3 extensiones por lado.

En las tres, el riel más largo carga más la unión (ver `FASE_E.md` §3b): en Ø500 la media madera macho queda con
FS 0.8 a 45 MPa con 150 N en la cápsula. La decisión de largo y la de reforzar la unión son una sola.

## Otros hallazgos

- **Ganchos contra la caja en Ø100** (lo pedía el prompt): los ganchos a ±50 quedan bajo la caja y no tocan M1 ni M2.
- **Orientación del gancho:** brida y perilla hacia la caja, mandíbula hacia afuera. Es la que deja libre el riel desde
  R + 3 para el carro.
- **Cuerdas de la linterna:** en Ø100 y Ø200 no hay ápice que funcione, porque la caja (159.6 × 126) es más ancha que el
  aro y las cuerdas a 45° la atraviesan (en Ø200 la esquina de la caja queda a 7.7 mm del eje de la cuerda). En Ø300 el
  ápice tiene que estar a 535 mm o más sobre el aro, en Ø500 a 273 mm o más. Es una propiedad de la linterna de prueba con
  esta caja, no del riel.
- **Gancho y casquillo contra la red** (56 a 96 mm³ en Ø300 y Ø500): la red esquemática es una pared de 1 mm justo en el
  radio de la varilla. Es un artefacto del modelo salvo que la red real cuelgue por dentro de la varilla.
- **Barrido de la bisagra:** con el riel actual choca en casi todas las posiciones, por la misma falta de largo. Se
  rehace cuando se decida el largo.

## Decisiones tomadas sin consulta

| # | Qué | Por qué | Descartado | Cómo revertir |
|---|---|---|---|---|
| D29 | Gancho con la brida y la perilla hacia la caja | Deja libre el riel desde R + 3 para el carro | Perilla hacia afuera | `ensambles.hook_set` |
| D30 | El lado −X se arma girando 180° sobre Z (como `riel.py`), no reflejando | La ranura de salida del cable queda del lado correcto | Espejo | `ensambles.put` |
| D31 | No se cambian `RAIL_CENTRAL_L`, `RAIL_EXT_L` ni `RAIL_EXT_PER_RING` | Son valores del equipo y la contradicción es suya | Elegir una de las tres salidas | `riel.paso_extension`, `riel.regla_extensiones` |
| D32 | Linterna de referencia con valores estimados: varilla Ø8, cuerdas Ø4, ápice 400, red de alto = D | No hay medidas; se reporta el ápice mínimo en vez de suponer uno | | bloque `# ensambles (Fase D)` de `params.py` |
| D33 | Los STEP de ensamble quedan fuera del repo | 42 MB; se regeneran con el script | Subirlos | `.gitignore` |

## Cierre

- **Qué cambió:** hay ensambles de los cuatro aros con la linterna de referencia, y `largo_riel.py` mide cuánto riel
  falta en cada uno.
- **Qué chequeos pasaron:** los ganchos no tocan la caja en Ø100, la caja con el riel y las pletinas no chocan entre sí, y
  el carro con la cápsula no choca contra su propio tramo.
- **Qué quedó pendiente:** **la decisión del largo del riel** (falta de 9 a 74 mm según el aro), que arrastra la unión de
  tramos (Fase E) y el barrido de la bisagra; el ápice de las cuerdas en Ø100 y Ø200.
