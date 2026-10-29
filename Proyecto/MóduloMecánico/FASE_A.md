# Fase A | Layout de la caja central (28/10/2026)

Rama local `cad/version-final`. Código nuevo en `cad_final/`; `cad/` no se tocó.

- Correr: `cd cad_final` y `python fase_a.py` (Python 3.12, CadQuery 2.8, pyvista 0.49). Tarda unos 40 s.
- Tabla completa `parámetro | anterior | nuevo | razón | origen | estado`: `cad_final/reporte_fase_a.md` (se genera desde `params.py`; no editar a mano).
- Renders: `salida/faseA/faseA_bandeja_iso.png`, `faseA_caja_abierta_iso.png`, `faseA_caja_superior.png`, `faseA_caja_bajo.png`.

## 1. Archivos

| Archivo | Qué hace |
|---|---|
| `cad_final/params.py` | Fuente única. Cada valor con `origen` y `estado`, más el valor anterior. Secciones COMUN / NODO / BOYA |
| `cad_final/layout.py` | Coloca los módulos y las zonas libres en números, sin CAD, y **deriva la cavidad**. Revisa que ningún cuerpo choque con nada |
| `cad_final/caja_central.py` | M1 y M2 preliminares, M11 bandeja (der/izq), módulos dummy, contratuercas, riel de referencia |
| `cad_final/checks.py`, `render.py` | Copiados de `cad/build.py` y `cad/vistas.py`. No se importan, porque `cad/` tiene otro `params.py` |
| `cad_final/fase_a.py` | Ejecuta todo, calcula masa, aire, empuje y lastre, y escribe el reporte y los renders |

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
