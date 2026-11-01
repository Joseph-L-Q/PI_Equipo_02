# Correcciones 01/11/2026: chaflán en la base de los soportes

**Observación de la jefa de práctica (Ing. María Rejas):** "En las piezas B2_cubierta, B3_caja, B5_cuna y M1s se sugiere
colocar un chaflán en la base de los soportes con el suelo, ya que reduce la concentración de esfuerzos y aumenta la
resistencia de la unión."

**Qué se hizo:**
- **Parámetro nuevo** en `cad_final/params.py`: `chaflan.base_soportes = 1.5` mm a 45°. Se prueba primero
  `chaflan.base_soportes_max = 2.0` en cada unión. Si choca con algo, baja a 1,5 → 1,0 → 0,5. Con `0` se vuelve a la
  versión anterior.
- **Construcción:** el chaflán es un sólido que se suma en la base de cada soporte (`cad_final/chaflan.py`):
  - un cono en los postes;
  - un prisma en nervios, paredes y orejas;
  - una franja a 45° en el perímetro interior del piso.

  Cada chaflán se recorta a su placa, así que no sobresale del borde. Los agujeros quedan libres y el asiento de cada
  cabeza M3 (Ø7) también.
- **Verificación** (`cad_final/correccion_chaflan.py`): cada pieza se cruzó contra los componentes, las botellas, las
  contratuercas PG7, el lastre en el máximo de su rango y las piezas vecinas. Se compararon v1 y v2, y **el chaflán no
  agrega ninguna interferencia**. El B-rep es válido en las 4 piezas y la orientación de impresión es la misma.

## Por pieza

### B2_cubierta (boya): impresa sin girar, sin soportes antes y después

| Dónde | Chaflán | Nota |
|---|---|---|
| 4 pilares Ø10 bajo las orejas de la caja, sobre las barras | 2 × 45° | Caben 2 justos en la barra de 14 |
| 4 columnas Ø12 del panel, sobre las barras transversales | 2 × 45° a lo largo de la barra, 1 × 45° hacia los bordes | La barra mide 14: el cono se recorta al borde |
| Mástil de antena Ø14, sobre la barra del extremo | 2 × 45° a lo largo de la barra | El mástil ocupa todo el ancho de la barra |

Los 8 asientos de cabeza M3 de la cubierta quedan libres. La caja B3 apoya 6 mm más arriba, así que no toca el chaflán.

### B3_caja (caja seca de la boya): impresa sin girar, sin soportes antes y después

| Dónde | Chaflán | Nota |
|---|---|---|
| Piso con paredes interiores, todo el perímetro | 2 × 45° | El RTC apoya en el piso a 3 mm de la pared: le queda 1 mm de aire |
| 4 standoffs Ø9 del portabaterías | 2 × 45° | El portabaterías apoya 6 mm más arriba |
| 4 postes Ø8 de la bandeja | 2 × 45° | — |
| 4 orejas con la pared exterior (sobre los pilares) | 2 × 45° | El asiento de la cabeza M3 de cada oreja queda libre |

Las tres contratuercas PG7 están a más de 20 mm del piso y no tocan el chaflán.

### B5_cuna (×2): impresa sin girar, con soportes antes y después (el voladizo no cambia)

| Dónde | Chaflán | Nota |
|---|---|---|
| 5 costillas sobre el patín | **1 × 45°** | La botella apoya a 1,5 mm del patín: es el más grande que deja aire (0,5 mm) |
| Pared lateral sobre las 4 lengüetas de unión al casco | 2 × 45° | No toca el casco B1 (verificado en el ensamble) |
| 2 postes de correa Ø8 que nacen de las lengüetas | 2 × 45° | — |

Los postes de correa del otro lado y las paredes nacen directo de la cama, sin placa. Ahí no hay unión con un piso, así
que no llevan chaflán.

### M1s_caja_cuerpo (nodo P2): impresa sin girar, con soportes antes y después (como ya estaba)

| Dónde | Chaflán | Nota |
|---|---|---|
| Piso con paredes interiores, perímetro | 2 × 45° | — |
| Piso con paredes extremas, junto a las 2 contratuercas PG7 | **sin chaflán** | La tuerca queda a 1 mm del piso y se ajusta con llave. Se deja libre una franja de ±10,7 mm por 11 mm desde la pared |
| 4 bosses Ø8 de la bandeja | 2 × 45° | La bandeja apoya 8 mm más arriba |
| Paredes de los 2 bolsillos de lastre con el techo (por dentro) | **1 × 45°** | Con el lastre en el máximo del rango (654 g por bolsillo, 29,05 de 30 mm), 1,5 lo tocaba. Con 1,0 queda libre |

El voladizo bajó de 15 115 a 14 515 mm² porque el techo de los bolsillos ahora tiene un borde a 45°. Con el lastre
nominal (575 g por bolsillo, 25,6 mm) sobran 4,4 mm.

## Gramos, horas y costo (OrcaSlicer, PETG; costo a S/ 60/kg)

| Pieza | Cant. | g antes → después | h antes → después | S/ antes → después | Soportes |
|---|---|---|---|---|---|
| B2_cubierta | 1 | 119,0 → 119,2 (+0,2) | 5,80 → 5,84 (+0,04) | 7,14 → 7,15 | no / no |
| B3_caja | 1 | 171,0 → 171,7 (+0,7) | 5,46 → 5,53 (+0,07) | 10,26 → 10,30 | no / no |
| B5_cuna | 2 | 141,0 → 141,2 (+0,2) c/u | 5,01 → 5,03 (+0,02) c/u | 8,46 → 8,47 c/u | sí / sí |
| M1s_caja_cuerpo | 1 | 509,2 → 509,3 (+0,1) | 16,13 → 16,06 (−0,07) | 30,55 → 30,56 | sí / sí |
| **Total (con cantidades)** | | **1081,2 → 1082,6 (+1,4)** | **37,41 → 37,49 (+0,08, ~5 min)** | **64,87 → 64,96** | |

- **3MF listos para imprimir** (G-code dentro), uno por pieza, en `salida/correccion_chaflan/3mf/`. Suman 1082,8 g y
  37,5 h; B5 se imprime 2 veces.
- **Cifras del slicer:** salen de cortar cada pieza sola (`slicer.json`), con el mismo perfil antes y después.
- **Peso de los prototipos:** el nodo P2 sube +0,1 g y la boya +1,3 g. Ninguno cambia el lastre.

## FEM

- **Se volvió a correr** el FEM de P2 (Gmsh + CalculiX).
  - Riel con el nodo en el agua: **FS 5,56; 2,72 entre capas**.
  - Izado: FS 8,48; 4,15 entre capas.
  - Pie de la cápsula: **FS 5,04; 2,47 entre capas**.
- **Mismos valores que antes:** el riel M3s y el pie M5s no cambian con esta corrección.
- **M1s y la boya no tienen FEM.** El chaflán solo puede bajar la tensión en esas uniones, porque saca la esquina viva.

## Onshape y Drive

- **Onshape LG_IMPRIMIR_P2:**
  - Pestañas nuevas `B2_cubierta_v2`, `B3_caja_v2`, `B5_cuna_v2` y `M1s_caja_cuerpo_v2`.
  - Planos `PLANO_A4_<pieza>_v2` en el mismo formato A4 del equipo. Cada uno lleva la cota del chaflán y una nota con
    los tamaños por unión:
    - B2 y B3: "Chaflán 2x45°" de canto, en el frente y la lateral.
    - M1s: "Chaflán 2x45°" en la vista superior, sobre la franja del piso. Adentro de la caja, de canto no se ve.
    - B5: "Chaflán 1x45°" en la vista superior, sobre las costillas del patín.
  - Los Part Studio anteriores se renombraron `zz_v1_<pieza>` y no se borraron.
  - Los planos A4 v1 (`PLANO_A4_<pieza>`) ya no estaban en el documento: alguien del equipo los sacó junto con los A3
    y los reemplazó por los "Drawing 2 … 16" hechos a mano. Las copias en PDF siguen en Drive
    (`04_Planos/A4_formato_equipo/`).
  - **Ojo con los Drawings a mano:** "Drawing 2 B2_cubierta", "3 B3_caja", "5 B5_cuna" y "7 M1s" siguen apuntando al
    Part Studio v1, ahora `zz_v1_…`, es decir, a la pieza sin chaflán. Para actualizarlos, en cada vista: botón derecho
    → cambiar la referencia al Part Studio `_v2`.
  - El primer intento de los 4 planos v2 tenía la cota del chaflán cruzada sobre otra vista. Se rehicieron, y el
    intento quedó como `zz_A4_prueba1_<pieza>_v2`, sin borrar.
- **Drive** `04_Planos/A4_formato_equipo/correccion_chaflan/`: los 4 PDF y los 4 STL nuevos, más los 3MF en `3mf/`.
  https://drive.google.com/open?id=17fAHg0FpzQXGBqcPaqawMURLoB9X9TVK
- **Drive** `04_Planos/PLANOS_A4_LanternGuard_v3.pdf`, con las 4 piezas reemplazadas.
  https://drive.google.com/open?id=1YJ--prr1EcfMIFeJOVHmHnyuDqIGMd1D
- **Onshape LG_IMPRIMIR_P2:** https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff

## Cómo repetirlo

```
python cad_final/boya_pet.py
.venv/Scripts/python cad_final/build.py --prototipo P2_robusto
python cad_final/correccion_chaflan.py --antes <carpeta con boya_pet/ y P2_robusto/ de la versión anterior>
python cad_final/planos_onshape.py --formato equipo --v2 todas --unir
```

- **Directorio:** los comandos se corren desde `cad_final/`.
- **Python:** el FEM necesita el del `.venv`, porque `gmsh` solo está instalado ahí.
