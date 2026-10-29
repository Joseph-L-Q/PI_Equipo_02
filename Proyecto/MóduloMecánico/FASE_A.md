# Fase A | Layout de la caja central (28/10/2026, revisada el mismo día)

> **Lee primero la §7 (revisión).** Las secciones 2 a 6 son la primera versión y quedan como historia: D1, D7, C12 y C13 ya los resolviste y sus cifras cambiaron.

Rama local `cad/version-final`. Código nuevo en `cad_final/`; `cad/` no se tocó.

- Correr: `cd cad_final` y `python fase_a.py` (Python 3.12, CadQuery 2.8, pyvista 0.49). Tarda unos 40 s.
- Tabla completa `parámetro | anterior | nuevo | razón | origen | estado`: `cad_final/reporte_fase_a.md` (se genera desde `params.py`; no editar a mano).
- Renders: `salida/faseA/faseA_bandeja_iso.png`, `faseA_caja_abierta_iso.png`, `faseA_caja_superior.png`, `faseA_caja_bajo.png`, `faseA_camara_corte.png` y `faseA_variante_2pisos_iso.png`.

## 1. Archivos

| Archivo | Qué hace |
|---|---|
| `cad_final/params.py` | Fuente única. Cada valor con `origen` y `estado`, más el valor anterior. Secciones COMUN / NODO / BOYA |
| `cad_final/layout.py` | Coloca los módulos y las zonas libres en números, sin CAD, y **deriva la cavidad**. Revisa que ningún cuerpo choque con nada |
| `cad_final/caja_central.py` | M1 y M2 preliminares, M11 bandeja (der/izq), módulos dummy, contratuercas, riel de referencia |
| `cad_final/checks.py`, `render.py` | Copiados de `cad/build.py` y `cad/vistas.py`. No se importan, porque `cad/` tiene otro `params.py` |
| `cad_final/camara.py` | Tramo central como cámara de cables: alto derivado, chequeo del recorrido del Cat5e, bolsillos y pletinas (revisión) |
| `cad_final/fase_a.py` | Ejecuta todo: compara 1 y 2 pisos, calcula masa, aire, empuje y pletinas por aro, y escribe el reporte y los renders |

`caja.py` y `calc_fase0.py` (Fase 0) quedan como estaban.

## 2. Cambios principales (resumen de la tabla)

| Parámetro | Anterior | Nuevo | Razón | Estado |
|---|---|---|---|---|
| Profundidad | 15 m | 1 m (0.0101 MPa) | Prueba real | confirmado |
| Electrónica | WROOM + MAX485 + JSN-SR04T | DevKitC-1 + XY-017 + microSD + MPU-6050 + 2 HW-517 | Decisión del equipo | medidas estimadas |
| Agujero del JSN en el fondo | sí | eliminado | Ultrasónico descartado | confirmado |
| Pared / fondo / tapa | 5 / 6 / 6 | 4 / 4 / 5 | A 1 m la presión no manda; la tapa queda en 5 por la ranura de 1.5 | tapa por verificar |
| Brida | 9 × 6 | 10 × 8 | Insertos térmicos M3 en la brida (antes tuercas) | por verificar |
| Tornillos de la tapa | 6 (paso 76) | 12 (paso ≤ 65) | Compresión pareja de la junta | por verificar |
| Cavidad | 132 × 66 × 54 | **184.6 × 108 × 46** (derivada) | Layout con las holguras de 15 / 10 / 20 mm | derivado |
| Caja exterior | 142 × 76 × 60 | **192.6 × 116 × 50**; con brida y tapa **212.6 × 136 × 55** | Entra en la cama de 220 con 7 mm de margen | derivado |
| Pasacables | 2 × PG7 en las paredes laterales + PG9 en la tapa | 2 × PG7 en el **fondo** (x = ±18.66) + 1 × PG7 umbilical en la tapa (−20, 16) | Los cables bajan al riel | por verificar |
| Unión con el riel | brida de 4 M3 por brazo | 4 insertos M4 **ciegos** desde abajo (±51.5, ±6) | No perforan el sello | por verificar |
| Cámara | 33 × 33 × 25 | 33 × 33 × 17 | Fabricante | confirmado |

## 3. Resultado

| | sin_base (por defecto) | kit_a (alternativa) |
|---|---|---|
| Caja con brida | 212.6 × 136 × 55, **cabe** | 286.6 × 147 × 52, **no cabe** en 220 |
| Bandejas | 2 × 89.3 × 104 (≤ 150) | 2 × 126.3 × 115 |
| Choques cuerpo ↔ zona | 0 | 0 |

Chequeos: M1, M2 y las dos M11 pasan BRepCheck, BOPAlgo, 1 sólido y sin astillas. Interferencia de cada módulo con M1 y con la bandeja: 0.00 mm³.

**Aire, empuje y lastre (solo la caja):** aire sellado 797 cm³, volumen desplazado 1400 cm³, empuje 1435 g. La caja pesa 594 g (relleno 40 %) a 770 g (100 %) y queda con **−841 a −665 g: flota**.

**Nodo completo, PRELIMINAR** (riel calculado por sección, cápsulas de la P4 rev. B vieja, 200 g de ganchos/carros/perillas sin modelar): peso aparente entre −609 y −917 g. Para quedar en +0.2 a +0.5 kgf hacen falta **930 a 1630 g de acero inoxidable**. Total en aire: **2.30 a 2.85 kg**, cumple ≤ 3 kg pero con poco margen. Los dos bolsillos (207 cm³) admiten unos 817 g en tuercas o 1470 g en barra: **con tuercas no alcanza**.

Cómo leer el rango: el 40 % es el caso más boyante solo si los huecos del relleno quedan sellados. Si se inundan durante los días de prueba, el peso aparente se acerca a la fila del 100 % y sobra lastre. Por eso el lastre tiene que ser ajustable (pesar el nodo en el agua y quitar o agregar).

Estabilidad aproximada de la caja con el lastre en los bolsillos: centro de masa z = 8.2 y centro de empuje z = 25.5, así que no se voltea. El cálculo completo es la Fase E.

## 4. Decisiones tomadas sin consultarte (el `docs/DECISIONES.md` del repo queda fuera de esta carpeta, así que van aquí)

| # | Qué se eligió | Por qué | Qué se descartó | Cómo revertirlo |
|---|---|---|---|---|
| D1 | "20 mm alrededor de cada contratuerca" leído **literal**: radio = esquina de la tuerca (8.66) + 20, y también 20 entre las dos tuercas | Es lo que dice el prompt v2 | La lectura de `caja.py` (una franja de 20 en total) | `holgura.contratuerca` en `params.py`. Ojo: con 10 o 5 el layout actual choca y **hay que reordenar las bandas**. No lo calculé, así que no doy un tamaño |
| D2 | Las zonas de cable y de acceso pueden solaparse entre sí; los cuerpos no pueden solaparse con nada | Los cables son flexibles y el acceso es ocasional. Sin esto la caja no entra en la cama | Que todas las zonas fueran excluyentes | Regla `conflicts()` en `layout.py` |
| D3 | Bandeja **partida** en `M11_bandeja_der` (ESP32, MPU-6050, HW-517 #2) y `M11_bandeja_izq` (microSD, XY-017, HW-517 #1). Ningún módulo queda partido | Entera mide 180: rompe la regla de 150 | Una sola bandeja | `bandeja.partir = False` |
| D4 | Umbilical en la **tapa**, en (−20, 16), dentro de la zona libre central | Sube a la boya. Queda fuera del asa (y = ±6) y de la zona de cables del MPU | En una pared lateral | `caja.pg7_umbilical_xy` |
| D5 | ESP32 con los pines hacia abajo, sobre una cuna de 15 mm (dupont por debajo) y USB hacia +Y con 35 mm libres | Acceso al USB sin sacar la bandeja | Pines hacia arriba (la placa iría al revés) | Posición en `layout.build()` |
| D6 | Unión con el riel por 4 insertos M4 ciegos en refuerzos interiores de 6 mm | El sello no se perfora | Pernos pasantes con junta | `caja.base_m4`, `caja.base_m4_boss` |
| D7 | Bolsillos de lastre integrados en M1, abiertos por abajo, de 20 de profundidad, a los costados del riel | El prompt los pide en la base, fuera del sello | Lastre dentro de la caja | `lastre.*` |

## 5. Conflictos y pendientes nuevos

| # | Qué pasa | Propuesta |
|---|---|---|
| **C12 (nuevo, Fase C)** | El domo del PG7 del fondo baja unos 15 a 20 mm dentro del riel, y el hueco del riel mide 22. El Cat5e (Ø5.5) necesita un radio de curvatura de unos 22 mm. **No puede doblar 90° dentro del riel** | Montar el PG7 al revés (domo dentro de la caja, en la zona libre, y contratuerca dentro del riel), o una ventana alargada con rampa en el tramo central. Se decide en la Fase C |
| **C13 (nuevo)** | El nodo flota: hacen falta 0.93 a 1.63 kg de lastre. Con tuercas, los bolsillos no alcanzan | Barra o pletina de inox (1470 g de capacidad), bolsillos de 28 de profundidad (el riel mide 30) o relleno al 100 %. Las tres cosas se suman |
| C4 (actualizado) | Con KIT A la caja mide 286.6 con brida: no cabe | Queda como alternativa paramétrica y desactivada |
| C14 (nuevo, Fase C) | Impreso de pie, los bolsillos dejan el fondo puenteando 32 mm sobre la zona del riel | Rampa a 45° en las caras interiores de los bolsillos, o bolsillos atornillados aparte |
| C15 (nuevo, Fase D) | En el aro de Ø100 las 4 cuerdas suben desde un radio de 50, dentro de la huella de la caja (±96 × ±58) | Revisar en el ensamble de Ø100 |
| Nota | El prompt da largos de 230 / 430 / 630; los tramos del riel suman 140 / 340 / 540. Supongo que la diferencia (45 por lado) son los carros | Confirmar en la Fase C |
| Nota | Las cabezas de los M4 de la base quedan dentro del riel; se aprietan con una llave allen por la ranura en T | Fase C |

Siguen estimados y sin medir: DevKitC-1, XY-017, HW-517, microSD, MPU-6050 (alto con pines), contratuerca PG7, cable Cat5e, impresora y densidad del PETG.

## 6. Cierre de la fase

- **Qué cambió:** `params.py` es la fuente única (con origen, estado y valor anterior). La caja sale del layout: 192.6 × 116 × 50 (212.6 × 136 × 55 con brida), con 2 bandejas, 3 PG7, 4 M4 ciegos y bolsillos de lastre.
- **Qué chequeos pasaron:** BRepCheck, BOPAlgo y astillas en M1, M2 y las dos M11; 0 choques en el layout; 0 mm³ de interferencia; cama de 220 y regla de 150 cumplidas.
- **Qué quedó pendiente:** C12 (curva del cable en el riel), C13 (lastre de 0.9 a 1.6 kg), D1 (lectura de los 20 mm) y todas las medidas reales.

## 7. Revisión del 28/10 (tus cambios a D1, C12 y C13)

### 7.1 Lo que pediste y cómo quedó

| Pedido | Cómo quedó |
|---|---|
| D1: 5 mm alrededor de cada contratuerca; se aprietan con la caja vacía | `holgura.contratuerca = 5`. Como se aprietan antes de meter la bandeja, la zona de la llave va solo del fondo a la cara de la bandeja. Arriba de la bandeja queda una columna libre de 15 mm para el cable que sube (radio 13.66), y la bandeja lleva un agujero de ese radio sobre cada contratuerca |
| Comparar 1 y 2 pisos y quedarse con el de menor aire | **1 piso: 484 cm³; 2 pisos: 485 cm³.** Es un empate: 1 cm³ está por debajo de lo que el modelo puede distinguir. Gana 1 piso por la regla, y además es 30 mm más bajo, lleva una sola bandeja y baja el centro de masa. 2 pisos queda a un switch (`caja.pisos = 2`) |
| C13: M1, M2, M4, M5 y tramos al 100 % con 5 perímetros; pletina de inox bajo el tramo central | `impresion.relleno_sellado = 1.0` y `impresion.perimetros_sellado = 5`. Pletina de inox de 25 × 5 × 100 (99 g): **4 por lado** (3 en Ø500), en dos bolsillos paramétricos fuera del sello. Se eliminan los bolsillos de la caja (D7): `lastre.bolsillos_caja = False` |
| C12: el tramo central como cámara de unos 50 mm con rampa al conducto de 22; R ≥ 25; PG7 normal con el domo en la cámara | `camara.py`. Alto interior **53.4** (derivado). El cable baja del domo, dobla 90° con R25 y queda sobre los nervios de la ranura T, ya a la altura del conducto. La rampa a 45° llega al conducto antes de la unión. Holgura mínima del cable al techo: 12.9 mm |

### 7.2 Números nuevos (1 piso, sin KIT A)

| | Antes (§3) | Ahora |
|---|---|---|
| Cavidad | 184.6 × 108 × 46 | **131.6 × 98 × 46** |
| Caja con brida y tapa | 212.6 × 136 × 55 | **159.6 × 126 × 55** (cabe en la cama con 60 mm de margen) |
| Bandeja | 2 piezas de 89.3 × 104 | **1 pieza de 127.6 × 94** |
| Aire sellado | 797 cm³ | **484 cm³** |
| Desplaza la caja | 1400 cm³ (empuje 1435 g) | **935 cm³ (empuje 958 g)** |
| Caja en aire | 594 a 770 g | **573 g** (M1 y M2 al 100 %) |
| Peso aparente de la caja sola | −841 a −665 g | **−385 g** (flota) |
| Peso aparente del nodo sin lastre | −609 a −917 g | **−338 g (Ø100) a −297 g (Ø500)** |
| Lastre | 930 a 1630 g, no cabía | **8 pletinas (790 g), 4 por lado, de Ø100 a Ø300; 6 (593 g) en Ø500** |
| Peso aparente final | | **+349 g (Ø100), +370 g (Ø200 y Ø300), +218 g (Ø500)**, dentro de 0.2 a 0.5 kgf |
| Total en aire | 2.30 a 2.85 kg | **2.08 a 2.19 kg** (≤ 3) |
| Estabilidad | | Centro de masa 6.7 mm (Ø100) y 9.0 mm (Ø500) bajo el de empuje: no se voltea, pero con poco margen |
| Con KIT A | no cabía (286.6) | Ahora **cabe**: 159.6 × 170 × 67 (1 piso) |

El relleno de la bandeja (40 % o 100 %) cambia el total en solo 4 g. La incertidumbre que queda son las masas estimadas de la electrónica y de las piezas sin modelar (200 g).

Cada pletina hunde 86 g y se ponen de a dos (172 g por par). Como la ventana mide 300 g, siempre hay una cantidad de pares que cae adentro. Si el nodo real pesa distinto en el agua, se ajusta quitando o agregando un par.

### 7.3 Decisiones nuevas tomadas sin consultarte

| # | Qué se eligió | Por qué | Qué se descartó | Cómo revertirlo |
|---|---|---|---|---|
| D8 | 1 piso | Menor aire (484 contra 485, empate), más bajo, una sola bandeja | 2 pisos (caja de 136 × 102 × 85) | `caja.pisos = 2` |
| D9 | La ESP32 va **sobre** los prensaestopas, en su cuna de 15 mm. Las repisas de la cuna quedan fuera de las columnas de cable | Sin la zona de llave sobre la bandeja, ese hueco queda libre, y los cables suben directo a los dupont de abajo de la placa | Bandas alrededor de los prensaestopas (la caja vieja) | Posición en `layout.build()` |
| D10 | La zona de llave del PG7 va solo del fondo a la bandeja, con una columna de cable de 15 mm sobre la bandeja | Tu dato: se aprietan con la caja vacía | Zona de llave hasta la tapa | `layout.build()` |
| D11 | Umbilical en la tapa, en (−53.2, 17.5) | Es el lugar libre más cercano al preferido, fuera de la franja del asa (\|y\| ≥ 17.5). Si no hubiera lugar, iría a la pared −X | Tapa en (−20, 16): ahí la contratuerca chocaba con la ESP32 | `caja.pg7_umbilical` = `tapa` / `pared` |
| D12 | Cámara **abierta arriba** en \|x\| ≤ 27.6: el fondo de la caja hace de techo y los domos entran por ahí. Alto interior derivado de 53.4, no de 50 | Domo PG7 de 22 (estimado) + R25 + medio cable + nervio de la ranura T. Con 50 el cable no llega sobre los nervios | Alto fijo de 50 | `riel.camara_*`, `pg7.domo` |
| D13 | Los 4 M4 de la caja al riel pasan a la **brida de la cámara**, en (±40, ±20). La cabeza queda fuera de la cámara y se aprietan desde abajo | Dentro de una cámara de 53 de alto la llave no llega | Insertos en (±51.5, ±6) | `caja.base_m4` |
| D14 | Pletinas **a los costados de la cámara, al nivel del fondo del riel**, con la tapa atornillada al ras del fondo. No debajo del riel | La ranura T del fondo tiene que quedar libre en todo el tramo central, porque en Ø100 los ganchos van a ±50, dentro del tramo. Colgadas justo bajo la caja, el centro de masa quedaba 11 mm **sobre** el de empuje | Bajo el riel (tapa la ranura T); colgadas de la brida; pletinas de 130 (el bolsillo invadía la unión y la extensión no entraba de costado: ahora miden 100 y el bolsillo llega a \|x\| = 53.5) | `lastre.pletina_nivel` = `abajo` / `brida`; `lastre.pletina_largo` |
| D15 | Unión de tramos (Fase B): media madera de 15, llave en cola de milano vista de lado (entra deslizando de costado) y 2 M4 verticales **dentro de las paredes**, que en la unión se engrosan a 10 | Los M4 no cruzan el conducto. Cada lado del riel lleva un solo Cat5e (5.5), así que un conducto de 10 en la unión alcanza | Tornillos que cruzan el conducto | `riel.union_*` |

### 7.4 Conflictos y pendientes

| # | Qué pasa | Propuesta |
|---|---|---|
| C12, C13, C14 | Resueltos por la revisión. C14 desaparece junto con los bolsillos de la caja | |
| C16 (nuevo) | El alto de la cámara sale del largo del domo del PG7 (22, **estimado**). Si el real mide 25, la cámara crece 3 mm | Medir el prensaestopas comprado antes de cerrar la Fase C |
| C17 (nuevo) | El fondo del riel queda 57.4 mm bajo el fondo de la caja (antes 30). El nodo es más alto, pero la estabilidad mejora | Fase D: revisar ganchos y cuerdas con la nueva altura |
| C15 (sigue) | En Ø100 las cuerdas suben desde el radio 50, dentro de la huella de la caja (cuerpo ±69.8 × ±53) y cerca de los bolsillos (\|y\| hasta 44) | Fase D |
| Nota | El margen de estabilidad es de 6.7 a 9 mm | Fase E, con momentos y metacentro |

### 7.5 Cierre de la revisión

> **Actualizado en la Fase C** con la cápsula real (93.1 g y 127.8 cm³ por unidad, antes 104 y 154): 3 pletinas por lado en todos los aros, peso aparente final de +208 (Ø100), +228 (Ø200 y Ø300) y +249 g (Ø500), total en aire de 1.86 a 2.07 kg, centro de masa 8.9 (Ø100) y 9.8 mm (Ø500) bajo el de empuje. Detalle en `FASE_C.md`.

- **Qué cambió:** la caja se achicó a 159.6 × 126 × 55, con una sola bandeja, y el aire sellado bajó de 797 a 484 cm³. El tramo central es ahora una cámara de 53.4 de alto. El lastre son pletinas de inox de 25 × 5 × 100: 4 por lado (3 en Ø500). El nodo queda entre +218 y +370 g en el agua y entre 2.08 y 2.19 kg en el aire.
- **Qué chequeos pasaron:** M1, M2, M11, la cámara y las tapas de los bolsillos pasan BRepCheck y BOPAlgo. El layout tiene 0 choques en 1 y en 2 pisos, y todas las interferencias dan 0 mm³. El recorrido del Cat5e con R25 cumple los 6 chequeos, y el centro de masa queda debajo del de empuje.
- **Qué quedó pendiente:** medir el domo del PG7 (C16), la estabilidad completa (Fase E), las cuerdas en Ø100 (C15) y todas las medidas de la electrónica.
