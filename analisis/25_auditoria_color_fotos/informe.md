# Auditoría visual del color: base de datos frente a fotos

Alcance: 14 quipus con foto y filas en `analisis/datos/cuerdas.csv` (AS010, 011, 012, 015, 017, 018, 020, 025, 069, 071, 212, 213, 214, 215). Las fotos de AS026, 031-034, 038, 070, 124, 136 y 140 existen, pero esos ids no tienen filas en `cuerdas.csv` y no se pudieron comparar. Resultados fila por fila en `auditoria.csv` (49 observaciones; no incluye imágenes).

## Método y límites

- Las fotos son diapositivas antiguas de 800 px, con dominante azul, amarilla o verde según la toma. No hay carta de color. Solo es fiable comparar tonos entre cuerdas de la misma foto, no tonos absolutos.
- Emparejé por bloques, no por cuerda, con tres criterios: (a) el número y orden de cuerdas por grupo; (b) cuerdas con rasgos únicos (la banda roja de AS018, el cordón tricolor de AS012, el bloque de 4 cuerdas pálidas sueltas de AS215); (c) contrastes claro/oscuro dentro del abanico. En ninguna foto pude fijar con seguridad cuál extremo es la cuerda 1, así que cada bloque tiene incertidumbre de ±1 grupo. Un emparejamiento cuerda a cuerda no es defendible.
- Para el color de la base usé la tabla `ascher_color_dc` de OKR. **Aviso:** en esa tabla `B` es «moderate yellowish brown», `G` es «grayish olive green», `LB` es «deep yellowish brown» (oscuro), `DB` es «deep brown» y `BG` es azul grisáceo. En esta base las letras B y G no significan azul ni verde, y la L de `LB` no significa «claro». Las fotos confirman que `B` es marrón (AS020, AS212).
- Juicio visual de un solo observador; no medí píxeles (un intento de segmentación automática dio ruido por fondos y reglas, y lo descarté).
- Escala del acuerdo: `si`, `parcial`, `no`, `no_verificable`. Los porcentajes excluyen `no_verificable`.

## Resultados

| Dimensión | si | parcial | no | no verificable | Acuerdo |
|---|---|---|---|---|---|
| Categoría gruesa (blanco, marrón, colorido) | 21 | 3 | 0 | 2 | 21/24 = 88% estricto; 24/24 si se cuenta el parcial |
| Fino (AB, MB, DB, B, LB, BB…) | 1 | 3 | 1 | 3 | 1/5 = 20% estricto; 4/5 = 80% con parcial |
| Fronteras de cambio de color | 6 | 0 | 0 | 0 | 6/6 (a escala de bloque) |
| Compuestos (torsión o tramos) | 2 | 2 | 1 | 2 (+2 rasgos no registrados) | 2/5 estricto |

**Grueso.** Blanco frente a marrón coincide casi siempre. Lo que la base llama `W` es en realidad crudo o gris-beige, a veces con motas (AS012 g2, AS025). Los tres `parcial` son colores oscuros no marrones: `G` y `YG` en AS012 y AS015 aparecen casi negro-azulados. Puede ser el sesgo azul de la diapositiva o un tono realmente distinto, y no se puede decidir con estas fotos. Del lado colorido, el rojo de AS018 sí se ve. El rosa `PK` de AS012 y los `GY`/`G`/`PK` de AS212 no se distinguen.

**Fino.** El único acuerdo pleno es el orden `LB` < `BB` en AS213, donde las subsidiarias `BB` se ven más oscuras. `AB`, `YB` y `B` no se pueden separar entre sí. En AS215 la base dice `DB` (marrón profundo), pero no se ve ninguna cuerda oscura: el hilo oscuro torcido con blanco (`W:DB`) se lee como marrón medio. Con n=5 verificable la estimación es muy imprecisa (el intervalo de Wilson al 95% para 1/5 va de aproximadamente 4% a 62%). Lo sólido es que la foto **no puede confirmar** los tonos de marrón, no que la base esté mal.

**Fronteras.** Las 6 coincidieron: oscuro a pálido en AS012 (g1→g2, g4→g5) y el corte a unos 7 cm de `MB/W`, el paso W→LB en AS213 (p9/p10), la banda en AS018 y el bloque de 4 `W` sueltos de AS215. Es poco exigente porque son cambios marcados y se comparan por bloque.

**Compuestos y jaspeados.**
- Coincide: el cordón fino tricolor `W:MB:YG` de AS012 se ve en las macros. En AS70, aunque ese id no tiene filas, abundan las cuerdas torcidas claro/oscuro («barber pole»), coherentes con el uso masivo de `:` en AS069 y AS071. La base sí registra la torsión bicolor.
- Discrepancia: en AS018 los tramos rojos (`W/RM/W`, 2.5-3 cm) son un **hilo rojo enrollado** sobre una pendiente blanca, no el color de la pendiente. La base lo trata como cambio de color de la cuerda. En macros (AS18_1, AS18_2) hay seis o más bandas rojas.
- Resto: en la mayoría de las cuerdas `W:B` y `W:RG` no pude confirmar la torsión por resolución (n/v).

## Rasgos visibles que la base no registra

- El **cordón principal** no tiene color en `cuerdas.csv`. En AS011 es una trenza gruesa de hilos gris-verdosos, tostado, marrón y casi negro, es decir hilos de varios colores torcidos (AS11_2).
- AS012: hilo azul oscuro enrollado en la unión de pendientes, y nudos grandes gris-beige sobre el cordón principal.
- Nudos anómalos: nudos largos o múltiples en cuerdas de AS11 y AS212, y un lazo en cordón en AS025.
- Fibra: las cuerdas pálidas de AS212, AS20 y AS25 tienen superficie vellosa (aspecto de fibra animal o camélido en macros); no se puede separar de algodón crudo con esta resolución. El color `W` mezcla probablemente algodón blanco, fibra de camélido crema y gris natural.
- AS213 y AS214: las fotos sobre fondo negro o liso muestran cuerdas anaranjado-doradas que la base reparte entre `LB` y `BB`; la diferencia depende del contraste.

## Conclusión sobre la confiabilidad

- **Análisis grueso (pálido, marrón, colorido): confiable.** 88% estricto (21/24), con la salvedad de que el pálido es crudo/gris-beige, no blanco.
- **Análisis fino (tonos de marrón AB, MB, DB, B, LB…): no verificable con estas fotos** (1 de 5 pleno, 3 de 8 comparaciones sin dato). No hay evidencia de que sea fiable ni de que no lo sea. El caso AS215 sugiere que `DB` puede estar sobrevalorado cuando hay un hilo oscuro torcido con otro claro. Cualquier uso de la distinción entre tonos de marrón debe tratarse como ordinal, no absoluto, y pedir contraste con los agrupamientos reales de la base (no con la foto).
- **Compuestos:** el código `:` es realista; la codificación de tramos `/` puede confundir un hilo de atadura con el color de la cuerda (AS018).
- Fiabilidad de este ejercicio: n pequeño (49 observaciones en 14 quipus, 24 en grueso y 5 en fino), emparejamiento por bloque y diapositivas con dominante de color.

## Para el coordinador

- El color grueso (pálido/marrón/colorido) se puede usar: 21 de 24 bloques coinciden (88%), y los otros 3 son tonos oscuros ambiguos, no errores pálido/marrón.
- Los tonos de marrón (AB/MB/DB/B/LB/BB) no se pueden validar con estas diapositivas (solo 5 comparaciones verificables, 1 plena). No afirmar fiabilidad ni inconsistencia; tratar el tono fino como ordinal y declarar la incertidumbre.
- Cuidado con la nomenclatura: en esta base `B` y `G` son marrón y verde oliva, `BG` es azul, `LB` es marrón oscuro profundo y `AB` es el marrón más claro. Mi lectura difiere de la glosa del encargo (B azul, G verde), que debería corregirse.
- `W` incluye crudo y gris-beige con motas: no equivale a blanco puro.
- Los códigos `/` (tramos) pueden ser hilos atados y no el color de la cuerda (AS018: hilo rojo enrollado en pendiente blanca). Revisar otros `W/R...`; una consulta sobre tramos cortos de color intenso es candidata.
- Faltan colores del cordón principal y de objetos atados en `cuerdas.csv`; en AS011 y AS012 hay hilos multicolores y envolturas visibles.
- Las fotos de AS026, 031-034, 038, 070, 124, 136 y 140 no pudieron compararse porque no hay filas en `cuerdas.csv`; por tanto el alcance es 14 quipus, no los 24 con foto.
- Las fotos no se copiaron al repo; los temporales de trabajo se borraron.
