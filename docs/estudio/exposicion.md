# Exposición: mi parte (bocetos → diseño 3D), 5 minutos

Según el reparto de `00_PLAN_PARCIAL.md`, me tocan los bocetos y el modelo 3D, que en la rúbrica valen 1 + 5 de 20 puntos. Son las diapos 12 a 17 del PPT v2.

**Antes del martes**, poner en los huecos del PPT:
- `LG_mec_ensamble_iso.png` en la diapo 15;
- `LG_mec_banco_prueba.png` en la 17.

Están en `Recursos/Imágenes/` y ya tienen la proporción de cada hueco. En la 16 van los planos de Onshape, que se hacen a mano el lunes.

## Guion

| Tiempo | Diapo / imagen | Qué digo |
|---|---|---|
| 0:00 a 0:40 | 12 Boceto seleccionado (vista general, luego detalles) | "Este es el concepto que ganó en la matriz: una barra que se apoya sobre el aro de la linterna. En el centro va la caja con el ESP32, el sensor de distancia y la microSD; en cada punta, una cápsula con su cámara. Un umbilical baja datos y energía desde la boya. A la derecha están los tres detalles: la caja de la boya, la barra y la cápsula." |
| 0:40 a 1:10 | 13 Alternativas | "Las otras dos rutas de la matriz: Ethernet hasta tierra con Portenta y Wi-Fi con Raspberry. Las descartamos porque bajo el agua no hay radio y el cable a tierra es caro y pesado." |
| 1:10 a 2:10 | 14 Piezas (y `LG_mec_P4revB_capsula_cuerpo.png`) | "Pasamos del boceto a piezas. Cada medida sale de un componente real: la cámara tiene 33 × 33 mm y su lente 25, así que la cavidad mide 38 × 38 × 42. Mi pieza original, la P4, era muy chica para la cámara, así que hice la P4 rev. B. Todo el diseño está en un solo archivo de parámetros en milímetros: si cambiamos una placa, cambia una línea." |
| 2:10 a 3:10 | 15 Ensamble (`LG_mec_ensamble_iso.png`) | "El ensamble: caja central con tapa sellada por junta tórica y asa para guantes con ojo de anclaje; dos brazos huecos por donde pasa el cable; y la bisagra dentada de 36 dientes, que fija la cámara cada 10°. Trabajamos a 40°. La bisagra está detrás de la cápsula y fuera del sello: así gira de 0 a 90° sin chocar con el brazo. Lo comprobamos en el CAD." |
| 3:10 a 4:00 | 16 Planos | "Planos con cajetín UPCH: el de conjunto con la lista de piezas y el de la cápsula con un corte por la junta. La junta es un cordón de 2 mm en una ranura de 1.5 mm de profundidad: 25 % de compresión." |
| 4:00 a 5:00 | 17 Interacción (`LG_mec_banco_prueba.png`) + pasos 1 a 4 | "Así se usa: se sube la línea, se apoya la barra sobre el aro, se ajusta con una correa en menos de 5 minutos y la cámara mira la malla. En el laboratorio lo probamos con este marco de malla de 20 mm a 150 mm de la cámara. Lo que falta validar: estanqueidad real en balde y tanque, y el lastre, porque con el aire sellado el equipo flota." |

Si sobra tiempo, cerrar con: "Verificamos lo que se puede calcular. Lo que no está probado lo dejamos escrito como pendiente."

## 10 preguntas difíciles del jurado

1. **¿Por qué PETG y no PLA o ABS?**
   PETG absorbe poca agua, resiste mejor la intemperie que el PLA y se imprime más fácil que el ABS, sin olor ni deformación. La lista de exigencias lo fija en la fila Fabricación.
2. **¿Resiste 15 m de profundidad?**
   A 15 m la presión es ρgh = 1025 × 9.81 × 15 ≈ 0.15 MPa. Con la fórmula de placa plana de Roark, el panel más cargado (la tapa de la caja, 132 × 66 mm con 6 mm de espesor) llega a unos 11 MPa: factor de seguridad de 4 frente a 45 MPa. **Es un cálculo, no un ensayo.** El FDM es más débil entre capas, por eso falta probarlo.
3. **Las simulaciones de SimScale usan 50 kPa. ¿No contradice los 15 m?**
   Sí: 50 kPa son unos 5 m. Es una inconsistencia que ya identificamos. La corregimos con el cálculo a 0.15 MPa y falta repetir la simulación con esa carga (el Run 2).
4. **¿Es estanco?**
   No lo afirmamos. Está diseñado para serlo: sello de cara con junta tórica al 25 % de compresión y prensaestopas en cada cable. El PETG impreso puede filtrar entre capas, así que lo imprimimos al 100 % con capa de sellado y lo probamos en balde con papel indicador antes del tanque.
5. **¿Cuánto pesa y flota?**
   Pesa unos 0.97 kg en aire (la exigencia es ≤ 3 kg). Con 592 cm³ de aire sellado flota con unos 0.3 kgf hacia arriba. Para cumplir el peso aparente de 0.2 a 0.5 kgf hacen falta unos 0.5 a 0.8 kg de lastre de acero inoxidable bajo la caja. Lo ajustamos midiendo en agua.
6. **¿Por qué la bisagra va detrás de la cápsula y no arriba, como en la P4 original?**
   Con el eje arriba, al inclinar la cámara hacia abajo el cuerpo gira hacia atrás y choca con el brazo. Habría necesitado orejas de unos 90 mm, muy flexibles. Con el eje detrás, a la altura del centro, gira de 0 a 90° con al menos 8.5 mm de holgura.
7. **¿Por qué una ventana plana si la lista de exigencias pide un domo?**
   El domo corrige la refracción, pero es caro y difícil de sellar en un prototipo. El plano es barato y reemplazable. Es una decisión abierta que tenemos que cerrar como grupo; el cambio en el CAD es solo el asiento de la ventana.
8. **¿Cómo pasa el cable sin que entre agua?**
   El brazo va inundado y solo guía el cable. El sello está en los prensaestopas: PG7 en la caja y en cada cápsula, PG9 en la tapa para el umbilical.
9. **¿Cómo se relaciona esto con los requerimientos (trazabilidad)?**
   Cada exigencia baja a una pieza:
   - Montaje ≤ 5 min con guantes: apoyos con correa y perno con tuerca mariposa.
   - Ergonomía: asa y ojo de anclaje.
   - Fabricación PETG con juntas: tapas con ranura.
   - Uso a 15 m: espesores verificados con Roark.
   - Función principal (capturar la malla): dos cápsulas a 40°.
10. **¿Por qué el prototipo es tan corto si la linterna mide 0.5 m de diámetro?**
    Es a escala de laboratorio: cada pieza tiene que entrar en una impresora de 220 mm. El largo es un parámetro (`ARM_LEN`); para campo se alarga el brazo o se usa un tubo comercial.

**Pregunta trampa posible:** "¿De dónde sale 132 kg?". No sale de ninguna fuente. El estudio de Samanco [1] da 68 a 73 kg de biofouling por linterna en 2 a 3 meses, y esa es la cifra correcta.
