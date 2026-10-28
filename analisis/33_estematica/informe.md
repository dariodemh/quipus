# 33 · Estemática: primer árbol de copias de todo el corpus

Fecha: 2026-10-18. Semilla: 20261033. Diseño congelado y adendas: `diseno.md`. Estemas por familia: `estemas.md` (texto) y `estemas_auto.md` (salida automática). Pares: `pares_copia.csv`.

## Cómo reproducirlo

Orden de ejecución (≈ 25 min con 20 núcleos):

1. `python comun.py --demo`: autocomprobación de la medida.
2. `python 01_barrido.py`: barrido; `--mitad E` corre la fase de exploración.
3. `python 02_pares.py todo`
4. `python 05_orden_libre.py`
5. `python 03_familias.py`
6. `python 06_candidatas_lector.py`
7. `python 04_potencia.py`

`03_familias.py` también corre su autocomprobación de la aritmética interna. Los datos de entrada se leen sin modificarlos: `datos/`, OKR en modo `ro`, `04`, `09`, `17` y `28`.

## 0. Resumen

1. **Barrido completo, sin prefiltro con pérdidas.** Entraron 201 930 pares (636 quipus con ≥ 3 cuerdas anudadas). La medida suma bloques locales disjuntos, en cualquier orden y sentido; prueba las escalas ×1, ×10, ×1/10, ×2 y ×1/2, con huecos y tolerancia de ±1 nudo. El nulo permuta rachas, con Monte Carlo secuencial: 9 → 99 → 999 permutaciones y cola de Gumbel.
   - **24 pares con q < 0,05; 20 con Holm < 0,05.**
   - El nulo es conservador: 1 532 pares con p < 0,01 frente a 2 019 esperados.
2. **Los controles positivos se recuperan con el barrido salvo las «versiones» de Incahuasi.**
   - Con q < 0,05: UR053B~C (puesto 5), UR064~UR068 (6), UR1107=UR237 (10, detectado como **inverso**), UR066~UR067 (16) y UR255~UR267A (22; q = 0,005, Holm 0,11).
   - Fuera: UR256~UR267B (puesto 558, p = 0,004) y UR266~UR275 (puesto 28, q = 0,28). Comparten cabeceras, no tramos.
   - La prueba sin orden (post hoc) los recupera: q_comb = 1e-7 y 7e-9.
   - De los 25 pares de 04 se recuperan 23. Los 2 que faltan son los «débiles» de 04.
3. **Copias nuevas frente a todo el proyecto: dos, ambas post hoc y del mismo tipo: «extracto de un campo».**
   - **UR1104 (AS104) reproduce en orden las cabeceras de los 9 primeros registros de UR234.** Ambos están en Berlín. La única variante (3102/3012) es el mismo nudo leído en otra posición decimal. UR1104 conserva una cabecera que UR234 ha perdido. Nivel: **apoyado (post hoc)**.
   - **UR108 (Lima) reproduce la cuerda 9 de las 6 secciones grandes de UR231 (Berlín)**, 5 de 6 exactas. Nivel: **propuesto (post hoc)**.
   - Ninguna está en la literatura (grep de `fuentes_txt` y `fichas`; búsqueda web en Khipu Field Guide sin resultados).
   - El barrido congelado no da ninguna copia «de tramo» nueva respecto de 04. Coincide con 30_frontera.
4. **La copia es un rasgo del archivo, no un accidente.**
   - Tasa dentro del mismo sitio frente a sitios distintos: 10/6 820 frente a 6/72 980 (OR 17,9; p = 1e-7). De los 6 cruces, 5 son etiquetas compatibles o nombres de coleccionista.
   - Donde el archivo sobrevive casi entero, entre el 14 y el 20 % de los quipus tiene copia: Incahuasi 8/52 contando los post hoc, Puruchuco 4/≈20, Leymebamba 3/22.
   - En el corpus en conjunto, 35/636 (5,5 %). Es una cota inferior: la potencia exige unas 15–20 cuerdas copiadas.
5. **Tipología.**
   - (a) Duplicado del mismo nivel guardado aparte: Puruchuco II y III; Incahuasi, canasta frente a corredor.
   - (b) Copia parcial o por tramos, a veces fragmentada en varias piezas: UR1175 → UR233 + UR232; UR212 → tres fragmentos de Basilea.
   - (c) Versión con otro desglose: UR266/UR275, UR256/UR267B, y UR1175/UR233 sin capa de subsidiarias.
   - (d) **Extracto de un campo** (nuevo): UR234 → UR1104 y UR231 → UR108.
6. **Dirección de copia: casi siempre indecidible, y lo digo.**
   - Con dos testigos, Lachmann solo orienta con criterios externos. La aritmética interna cierra en muy pocas variantes.
   - El único nudo de estema por encima de un par se sostiene en errores conjuntivos y viene de 13/ds: UR278 → α → {UR266, UR275}, con ±1 en unidades compartidos.
   - 30_frontera aporta otro conjuntivo: 15652/15649, en KH0049 y en UR122.

## 1. Diseño y cambios (detalle en `diseno.md`)

- **Medida (congelada antes de ver datos).**
  - Puntuación log-odds de 04: exacta, ±1 nudo, discordancia. Las frecuencias se calculan sobre la composición del par, así que valores comunes y ceros pesan casi nada.
  - Suma de hasta 5 bloques Smith-Waterman disjuntos. Cada bloque puede ir directo o invertido. Los tramos de A y de B se retiran tras usarse.
  - Máximo sobre las 5 escalas.
- **Exploración/confirmación.** Quipus divididos en E (319) y C (317), estratificados por procedencia. En E se hicieron dos cambios, documentados en las adendas:
  1. **El prefiltro por huella** (multiconjunto de valores ≥ 10) perdía 7 de los 25 pares de 04: los de valores pequeños, como Leymebamba. Se sustituyó por Monte Carlo secuencial sobre todos los pares, sin pérdida.
  2. **El nulo por nivel daba 84 «copias» solo en E–E.** Eran quipus eje (HP034, UR1114) con rachas 1-1-1 o 2-2-2. Se pasó al **nulo de rachas** y a τ = 20 bits. Los controles se mantienen entre 1e-7 y 1e-91. 30_frontera llegó a la misma conclusión por su lado: el nulo de permutación total imita copias.
- **Calibración E/C de la versión final.** Los pares apoyados o bien apoyados se reparten 8 en E–E, 3 en C–C y 12 en E–C. Lo esperado por número de pares es 5,75, 5,75 y 11,5. No hay sesgo de la fase de exploración.
- **Post hoc, y marcado así en todas las salidas.**
  - `05_orden_libre.py` (valores ≥ 100 compartidos frente a reemplazo por quipus de otra procedencia, más el orden de esos valores). Se añadió porque el barrido no veía las versiones de Incahuasi.
  - `06_candidatas_lector.py`.

## 2. Resultados por par (`pares_copia.csv`)

| nivel | n | pares |
|---|---|---|
| bien apoyado (Holm < 0,05 y equipo rojo o publicado) | 15 | HP055~UR1084, KH0049~UR122, UR1175~UR233, UR1175~UR232, UR006~UR009, UR006~UR021, UR009~UR021, UR053B~C, UR064~UR068, UR066~UR067, MM015~UR212, MM016~UR212, UR1114~UR1123, UR1118~UR218, QU002~UR137 |
| mismo objeto (bien apoyado) | 3 | UR1107=UR237 (inverso), KH0033=UR044, AS125=UR247 |
| apoyado | 2 | AS159~AS173, UR255~UR267A |
| apoyado (post hoc) | 3 | UR266~UR275, UR256~UR267B, **UR1104~UR234 (nuevo)** |
| propuesto | 5 | AS128~QU013 (falla diversidad), MM008~UR212, MM016~UR1131, UR004~UR037 y UR113~UR260 (estos dos, artefactos) |
| propuesto (post hoc) | 2 | **UR108~UR231 (nuevo)**, UR273B~UR274B |
| especulativo | 218 | p < 1e-3 sin q; incluye UR1034→UR1145 |

**Escala.** Ningún par con escala ≠ 1 sobrevive al equipo rojo. Los dos que la usan (UR004~UR037 ×½ y UR113~UR260 ×10) se apoyan en 2 o 3 valores distintos.

**Inversión.** La inversión sí es real:
- UR1107=UR237 (mismo objeto);
- MM015 y MM016 frente a UR212;
- UR009 frente a UR006 y UR021.

**Reordenamiento.** UR006~UR009: 2 bloques en orden cambiado.

**Equipo rojo de las nuevas** (§7 del diseño y `estemas.md` §7):
- *Valores comunes.* Los 9 valores de UR1104 están entre 1 407 y 3 419. Ningún otro quipu del corpus contiene más de 1 de ellos. De los 5 de UR108, solo UR231 tiene más de 2.
- *Listas cortas.* UR108 tiene 7 cuerdas. Por eso el orden solo aporta 1/60 y el par queda en propuesto. UR1104 tiene 9 de 9 en orden.
- *Ceros.* No intervienen.
- *Duplicado de base de datos.* Los largos, la posición de los nudos, su dirección y los colores difieren. UR1104/UR234 los transcribieron investigadores distintos: Ascher y Urton.
- *Mismo objeto con otra sigla.* UR1104 tiene el alias UR224 (Khipu Field Guide), no UR234. Los números de inventario son distintos: VA42527 y VA66837.

## 3. Crítica de familias (`estemas.md`, `familias.csv`, `direccion.csv`, `variantes.csv`)

- **16 familias de copia y 3 de mismo objeto.** Solo dos tienen 3 testigos:
  - **Leymebamba.** Hay 4 columnas con variantes en los tres testigos. UR009 es singular 2 veces; una es una transposición entre subsidiarias. UR021 es singular 1 vez. El conjuntivo UR009 = UR021 ≠ UR006 aparece 1 vez, con ±1 nudo. Árbol: **estrella sin resolver** alrededor de UR006. Particiones incompatibles: 0.
  - **UR1175.** UR233 y UR232 no se solapan (comparten el inventario VA63038): son **un testigo en dos piezas**. Lo mismo vale para Basilea: MM008, MM015 y MM016, inventario IVc.366.03, copian tramos disjuntos de UR212.
- **Contaminación (propuesta).** MM016 contiene además 5 cuerdas idénticas a UR1131. Sería la única red del corpus.
- **Dirección.** Ningún par llega a los 2 criterios exigidos. Con 1 criterio quedan:
  - **omisión de capa:** UR1175 ⇢ UR233/232;
  - **omisión sistemática de las cuerdas «222»:** HP055 ⇢ UR1084;
  - **extracto de sección más el error conjuntivo de 30:** KH0049 ⇢ UR122, o fuente común;
  - **corrección aritmética:** UR256 tiene 153, que cierra [x, c, x − c], donde UR267B tiene 143. Con un solo criterio no orienta.
- **Errores conjuntivos que sí estructuran el estema.**
  - UR266 y UR275 comparten todos los ±1 de unidades frente a UR278. Hay un libro perdido α entre UR278 y los dos libros (13/ds; coordinador).
  - KH0049 y UR122 comparten 15652/15649 (30_frontera).
  - Puruchuco: las dos divergencias 2904/2908 y 161/162 aparecen en UR066 y en UR067 (14).
- **Separativos frente a ruido.** El ruido del mismo objeto leído dos veces es del 3 al 12 % de lecturas distintas. Las copias quedan en ese rango o algo por encima. Eso concuerda con 14: las copias conservan el valor al nivel del ruido de lectura.

## 4. Cruces: museo, sitio y transcriptor

- **Cruzan institución: 5 pares, 4 familias.**
  - Lima → París: HP055/UR1084.
  - Lima → Gotemburgo: KH0049/UR122.
  - Basilea → Berlín: MM/UR212.
  - Dallas → Miami: QU002/UR137.
  - A estos se suma UR108/UR231 (Lima → Berlín, post hoc).
  - Lo más probable es dispersión moderna de lotes de un mismo sitio, no envío antiguo a distancia.
- **Sitios conocidos distintos: 6 pares.**
  - KH0049 «Costa Sur» frente a UR122 «Nazca»: compatibles.
  - UR1114 «Entre Ica y Pisco» frente a UR1123 «Ica»: compatibles.
  - MM015/016 «Eduard Gaffron»: es un coleccionista, no un sitio.
  - **UR1175 Pachacamac frente a UR233/UR232 Huacho:** el único cruce real posible. A unos 150 km.
- **Serie de investigador.** 9 de 20 pares cruzan serie (AS/HP/KH/MM/QU frente a UR). 7 cruzan capturista OKR (`cord.CREATED_BY`). Una copia leída por dos investigadores no puede ser un artefacto de su forma de numerar.
- **KFG frente a OKR: la misma lectura.** El multiconjunto de valores de KFG está en OKR al 99,86 % de media, con mínimo 94,8 % en los 37 miembros de familias. KFG no es una lectura independiente.
- **Lecturas independientes reales.** Solo están en los duplicados del mismo objeto leídos por dos investigadores: UR1107/UR237, AS125/UR247 y KH0033/UR044. Discrepan en el 3 al 12 % de las lecturas, que es el ruido de base.

## 5. ¿Rasgo del sistema o algo raro? Géneros del atlas (E → C)

| género | copiados / n | lectura |
|---|---|---|
| ARC (archivo jerárquico) | 10/21 | Replica en C (Holm 5e-5), pero es **circular**: el atlas define ARC en parte por las copias |
| CAL (calendario) | 3/3 | **Circular**: UR009 y UR021 entran en CAL por ser copias |
| FOR (formulario) | 9/101 (8,9 %) | OR ≈ 1,9 en E (p = 0,24) y 1,8 en C (p = 0,42): **no replica** |
| SIN | 7/286 (2,4 %) | Menos copias en E (p = 0,02); en C, p = 0,06, Holm 0,09: no replica |
| TAB, SEG, PAD, NAZ | 2/55, 2/76, 1/9, 1/6 | Al nivel de la base |
| **TAL, ASG, SUM, NON** | **0/28, 0/28, 0/14, 0/9** | No se copian |

**Lectura (apoyado para «archivo»; propuesto para el resto).**
- La copia sigue a los **archivos**, no a un género de contenido. Se copia dentro de un depósito: duplicado de nivel, respaldo en otro edificio, extracto de un campo para otro nivel.
- Los tally (TAL), las asignaciones (ASG) y los registros de suma interna (SUM) no muestran copias.
- **Ni la copia como respaldo ni el envío a otro nivel son raros.** Los dos aparecen en todos los archivos que sobreviven casi completos: Incahuasi, Puruchuco y Leymebamba.
  - El «envío a otro nivel» tiene dos firmas: los totales que suben (UR278 → libro) y ahora los **extractos de un campo** (UR234 → UR1104, UR231 → UR108).
  - Fuera de los archivos, la baja tasa se explica por dispersión y potencia, no por ausencia.

## 6. Potencia (`potencia.csv`, `salida_04.txt`)

Copia sembrada de L cuerdas en quipus reales, con 10 % de errores de ±1 nudo y 10 % de omisiones. Proporción de copias que alcanzan Holm < 0,05 sobre 201 930 pares, con 30 réplicas por celda:

| L | inversa | reordenada en 2 bloques | escala ×10 |
|---|---|---|---|
| 5 | 0 | 0 | 0 |
| 8 | 0,17 | 0,03 | 0,13 |
| 12 | 0,63 | 0,17 | 0,43 |
| 20 | 0,97 | 0,67 | 0,67 |

- **Efecto mínimo detectable al 80 %:**
  - copia directa o inversa: unas 15 cuerdas;
  - reordenada o a escala: más de 20.
- Las copias de menos de 10 cuerdas (AS159/AS173, UR1118/UR218) solo se ven si sus valores son raros.
- Las versiones con cabeceras compartidas y desglose distinto no se ven con el barrido; necesitan la prueba sin orden.
- La tasa de copia del §0.4 es una **cota inferior**.

## 7. Niveles de evidencia

- **Bien apoyado.**
  - La copia es un fenómeno de archivo: mismo sitio frente a sitios distintos, OR 18, p = 1e-7.
  - 10 de los 15 pares con Holm < 0,05, los que están en un mismo museo.
  - La inversión real en Basilea y en Leymebamba.
  - El nulo de permutación por cuerda es insuficiente; hace falta conservar las rachas (independiente de 30).
  - KFG y OKR son la misma lectura.
- **Apoyado.**
  - Los otros 5 pares con Holm < 0,05, que están en museos distintos (HP055/UR1084, KH0049/UR122, MM015/UR212, MM016/UR212, QU002/UR137). La estadística es tan fuerte como en los demás, pero falta verificar en los objetos que sean piezas distintas y de qué procedencia. En `pares_copia.csv` figuran como «apoyado (entre museos)»; criterio de `04_concordancias`, corregido el 27/10/2026.
  - Tipología a–c.
  - UR1104 extrae las cabeceras de UR234 (post hoc).
  - Un testigo en dos piezas: UR232 + UR233, y Basilea.
  - Ancestro perdido α de UR266/UR275 (conjuntivos de 13/ds).
- **Propuesto.**
  - UR108 extrae el campo 9 de UR231, lo que apoya la unión de los fragmentos VA16135a y b.
  - Contaminación en MM016 (UR212 + UR1131).
  - KH0049 ⇢ UR122.
  - HP055 ⇢ UR1084.
  - UR1175 ⇢ β.
- **Especulativo.**
  - Toda dirección de copia.
  - El estema de Leymebamba.
  - UR1034 → UR1145: 5 totales exactos en orden, p = 4e-4 nominal; 4 de ellos son menores que 20.

UR004 → UR091, la otra candidata del lector, sale **negativa**: 10 totales con ±1 nudo frente a 9,6 esperados (p = 0,51). El barrido da p = 0,7.

## 8. Límites

- La selección es por valor. Toda copia que reescriba los valores es invisible.
- El color no se usó para detectar. Entre transcriptores no es comparable (24, 26).
- La prueba sin orden y las dos copias nuevas son posteriores al diseño. Su q es sobre la familia post hoc (2 957 pares con ≥ 3 valores compartidos), no sobre los 201 930.
- `cierra()` solo prueba sumas contiguas y de subsidiarias. Una aritmética más rica (columnas, cuotas) orientaría más aristas.
- La lista de «publicadas» se verificó leyendo pasajes: Urton 2005, Urton y Brezine 2005, Urton y Chu 2015, Urton 2017. La co-mención por sí sola no cuenta como publicación.

## Para el coordinador

- El barrido congelado (201 930 pares; multibloque, inversión, escala, huecos y ±1 nudo; nulo de rachas) da **24 pares con q < 0,05 y 20 con Holm**. Recupera 23 de los 25 de 04 y 5 de 7 controles. Los 2 que pierde, UR256/UR267B y UR266/UR275, los recupera la prueba sin orden (post hoc, q ≤ 1e-7).
- **Nuevo y fuerte (post hoc): UR1104 (AS104) es un extracto de las cabeceras de UR234.**
  - 9 cabeceras en orden, con una variante de posición decimal (3102/3012).
  - Conserva la cabecera hoy rota de UR234 (2016).
  - Ambos están en Berlín y los transcribieron investigadores distintos. Nivel: apoyado.
- **Nuevo (post hoc, propuesto): UR108 (Lima) copia la cuerda 9 de las 6 secciones de UR231 (Berlín), 5 de 6 exactas.** Si se confirma, apoya la unión de los fragmentos VA16135a y b de KFG. Es lo más útil para verificar en museo.
- **La copia es un rasgo de archivo, no rara.** Mismo sitio frente a sitios distintos, OR 18 (p = 1e-7). Afecta al 14–20 % de los quipus de los archivos casi completos y al 5,5 % del corpus (cota inferior; potencia del 80 % solo desde unas 15 cuerdas). No se copian TAL, ASG ni SUM. FOR no replica. ARC y CAL son circulares.
- **Tipos:** duplicado del mismo nivel guardado aparte; copia por tramos repartida en varias piezas (UR232+UR233; los fragmentos de Basilea, dos de ellos invertidos); versión con otro desglose; extracto de un campo (nuevo). Contaminación propuesta: MM016 = UR212 + UR1131.
- **La dirección es casi siempre indecidible** con dos testigos. Ningún par reúne 2 criterios. Los únicos nudos de estema firmes salen de errores conjuntivos: α entre UR278 y UR266/UR275 (±1 compartidos) y 15652/15649 en KH0049 y UR122. Leymebamba queda en estrella.
- **Candidatas del lector:** UR004 → UR091, negativa (p = 0,5). UR1034 → UR1145, especulativa (p = 4e-4 nominal; totales pequeños; q de 04 = 0,15).
- **Método:** el nulo que permuta cuerda a cuerda fabrica copias a partir de rachas. Lo mostramos 33 y 30 por separado. Toda búsqueda entre quipus debe usar un nulo de rachas o de tramos.
- **KFG = OKR** (99,9 % del multiconjunto de valores). Las únicas lecturas independientes son los 3 duplicados del mismo objeto, con un ruido de lectura del 3 al 12 %.

Fuentes web consultadas solo para comprobar si las relaciones estaban publicadas (no lo están): [Khipu Field Guide, UR108](https://khipufieldguide.com/catalog/UR108.html), [KH0468 (UR231)](https://www.khipufieldguide.com/catalog/KH0468.html), [KH0118 (UR1104, AS104, UR224)](https://www.khipufieldguide.com/catalog/KH0118.html) y [KH0471 (UR234)](https://www.khipufieldguide.com/catalog/KH0471.html).
