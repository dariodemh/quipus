# Rejilla de categorías de Incahuasi (método Kober/Ventris)

Carpeta: `analisis/ds/n_rejilla/`. Semilla fija 20261018. Todos los scripts leen solo
`analisis/datos/*.csv` y las salidas de `13`, `14` y `19`; no escriben fuera de esta carpeta.

## 0. Resumen

1. **El grafo de equivalencias no produce categorías grandes, y eso es informativo.** Con 144
   aristas verificadas por aritmética o alineamiento (45 celdas UR278↔UR270 colgante, 45
   celdas↔subsidiaria, 28 copias UR255↔UR267A, 23 cabeceras del mismo registro, 3 componentes A),
   se forman 95 componentes no triviales (47 de 2 cuerdas y 48 de 3). **Ninguna categoría abstracta emerge como
   componente conexa**: lo que se repite entre libros no es una cuerda (los valores son cifras
   únicas de un registro) sino una **posición**. El método de Kober/Ventris aplicado a quipus tiene
   que trabajar con ranuras, no con "palabras" que reaparecen.
2. **El color no codifica la columna; codifica la fila y el nivel.** En UR278, 23/28 filas son
   monocromas (nulo 0,01/28; p = 0,0002) y la información mutua columna–color es 0,015 bits frente
   a 0,020 del nulo (p = 0,77). En UR270 el colgante es blanco y la subsidiaria no en 61/62 pares
   (p = 1,4·10⁻¹⁷). La "columna 3" de UR278 no tiene el mismo color que su contraparte de UR270:
   UR270 es casi todo blanco y UR278 colorea la fila entera.
3. **La posición sí codifica la categoría, y el orden de las 9 partes se conserva.** En los 5
   registros que están a la vez en UR270 y UR278, la permutación identidad es la mejor de las 9!
   en 5/5 casos, con 39/45 celdas iguales ±1 (p por fila entre 2,8·10⁻⁶ y 3,3·10⁻⁵; combinado
   7,4·10⁻²⁶, con la cautela de que las filas no son independientes).
4. **La firma relativa de las 9 partes es estable.** Efecto de columna: Friedman χ² = 90,6,
   p = 3,5·10⁻¹⁶, W de Kendall = 0,44 (26 filas completas); la varianza de las medias por columna
   es 9,2 veces la del nulo (p = 0,0002). Las partes 1 y 2 son las mayores en 18/28 filas
   (esperado 6,2; p = 2,2·10⁻⁶) y las partes 8 y 9 las menores en 16/28 (p = 6,5·10⁻⁵). No es un
   artefacto de ordenar de mayor a menor: 0/28 filas están ordenadas así.
5. **Negativos que importan.** El color **no** se conserva en la única copia incaica alineable:
   UR255–UR267A coincide en color en 4/28 cuerdas (nulo 4,8; p = 1,0) y en unión en 0/28 (UR255
   es R, UR267A es V). El color es, por tanto, una convención del libro/registrador, no una
   propiedad de la categoría. Además, la cuota no ocupa la 2.ª posición en el libro maestro UR269
   (2/65, p = 0,93), y la firma no es perfectamente invariante de escala (ρ de la proporción con el
   total del registro hasta ±0,42, sin superar BH).

## 1. Pregunta y marco

El objetivo es construir un **diccionario interno de categorías** del archivo de Incahuasi sin
suponer significados: primero la estructura (qué cuerdas registran lo mismo), después el
significado. La unidad de categoría no es la cuerda suelta sino la **ranura** (posición dentro del
registro) y el **rol aritmético** (cabecera, cuota, parte A, parte B, columna).

Preguntas concretas:

- ¿Qué relaciones verificadas permiten afirmar que dos cuerdas registran la misma categoría?
- ¿Los atributos (color, posición, nivel, unión, torsión, magnitud) se conservan entre quipus?
- ¿El color o la posición marcan la categoría, y de qué forma?
- ¿Se conserva el orden de las 9 partes? ¿Hay una parte siempre mayor o menor?

## 2. Datos y método

### 2.1 Datos

- `analisis/datos/cuerdas.csv`, restringido a los 52 quipus con `procedencia = Incahuasi`
  (23 JC del Sector B y 29 UR del depósito). 0 con `nudos` vacío se trata como ausente.
- `analisis/13_sistema_incahuasi/`: `grafo_cuerdas.csv`, `libro_consolidado.csv`,
  `ur270_ur278.csv`, `ur278_tabla.csv`. (`componentes_filas.csv` se inspeccionó, pero sus
  emparejamientos por índice de registro entre UR273A y UR274A resultaron en gran parte espurios
  —808 frente a 700, 272 frente a 280— y **no se usaron**; en su lugar se usan las notas de suma
  verificada de `grafo_cuerdas.csv`.)
- `analisis/14_copias/filas_alineadas.csv` (alineamiento Smith-Waterman de copias).
- `analisis/18_equipo_rojo/informe.md`: se usan solo las relaciones que el equipo rojo deja como
  **sobreviven** o **apoyadas**. En la práctica: la celda UR270→UR278 (sobrevive), la suma A+B de
  la afirmación 1a (sobrevive con p = 0,015 corregido; la 1b se debilita y no se usa), la copia
  UR255–UR267A (validada por 14) y las cabeceras UR266/UR275/UR269 (apoyadas). **No** se usa la
  posición de las filas de UR269 como prueba (el equipo rojo la retira) ni la numerología de
  cuotas.
- `analisis/19_prediccion/loo_consenso.csv` e `inventario_redundancia.csv`: se usan para medir
  cuántas vías independientes sostienen cada celda de la rejilla (§3.6), no para predecir.

### 2.2 Grafo de equivalencias (`01_grafo.py`)

Nodos = cuerdas. Aristas = "misma categoría", solo cuando hay una relación verificada:

| Tipo | n | Criterio |
|---|---:|---|
| `celda_P` | 45 | la celda k de una fila de UR278 es el colgante k del grupo correspondiente de UR270 (5 filas × 9 columnas; 39/45 celdas ±1) |
| `celda_S` | 45 | esa misma celda es la 1.ª subsidiaria del colgante k de UR270 |
| `copia` | 28 | UR255↔UR267A, alineamiento de `14_copias` (27 exactas + 1 ±1 nudo) |
| `cabecera` | 23 | cabeceras del mismo registro en UR266/UR275/UR269, LCS exacta sobre la lista ordenada |
| `componente_A` | 3 | dos cuerdas A que, con la **misma** cuerda B y el **mismo** total, son el mismo componente en dos copias (notas de 13) |

Componentes conexas: **95 componentes con ≥2 cuerdas** (47 de 2 cuerdas y 48 de 3; una de ellas
con tres aristas), tamaño máximo 3. Es decir, el grafo empareja **registros**, no categorías.

**Por qué.** Una cuerda de quipu lleva una cifra que pertenece a un registro concreto (un periodo,
un depósito). Dos cuerdas de libros distintos solo son "la misma" si son el mismo registro. La
categoría que se repite no es la cifra sino la **ranura**: "la columna 3", "la parte A", "la
cabecera". Por eso el diccionario se construye en dos niveles: (i) componentes de cuerdas
(registros equivalentes) y (ii) clases de ranura (columna, rol). El segundo nivel es el que se
puede comparar entre quipus y con listas coloniales.

### 2.3 Consistencia de atributos (`01_grafo.py`)

Para cada tipo de arista y cada atributo (color exacto, familia de color, unión, torsión) se cuenta
cuántas aristas emparejan el mismo valor. **Nulo:** se permuta el atributo dentro de cada quipu
**y dentro de cada nivel** (conserva el estilo del libro y la composición por nivel; 5 000
réplicas). p empírico unilateral = (1 + n.º nulos ≥ observado)/(B+1). BH sobre las 20 pruebas.

### 2.4 Color (`04_color.py`)

- **A)** UR278: n.º de filas monocromas frente a un nulo que baraja los colores de todo el quipu
  (conserva la composición global).
- **B)** UR270: en cada par colgante/subsidiaria con colores distintos, ¿el colgante es el blanco?
  Nulo = intercambio dentro del par (binomial exacta).
- **C)** UR278: información mutua columna–color frente a permutar colores dentro de la fila.
- **D)** Copia UR255–UR267A: color, unión y torsión idénticos frente a permutar el color de B.

### 2.5 Las 9 partes (`02_columnas.py`, `03_rejilla.py`)

- **UR278:** 28 filas × 9 columnas (`ur278_tabla.csv`, filas con ≥7 columnas; 26 completas).
- **UR270:** 7 grupos con exactamente 9 colgantes; celda = colgante + 1.ª subsidiaria.
- Proporción = celda / total de la fila. Firma = media por columna; IC 95 % bootstrap
  remuestreando filas (5 000).
- **Efecto de columna:** Friedman sobre las 26 filas completas + W de Kendall. Nulo de la
  varianza de las medias por columna: permutar columnas dentro de cada fila (5 000).
- **Estabilidad del patrón:** Spearman medio entre todos los pares de filas; nulo permutando
  dentro de fila (500).
- **Orden entre quipus:** en los 5 pares UR270–UR278 se comparan las 9! permutaciones; se cuenta
  cuántas celdas coinciden ±1 y se ve si la identidad es óptima.
- **Mayor/menor:** n.º de filas en que la columna k es el máximo (o el mínimo), frente a una
  binomial con p = 1/9 (o 2/9 para el par 1–2).
- **Control aburrido:** ¿están las filas ordenadas de mayor a menor?

## 3. Resultados

### 3.1 Qué atributos se conservan entre quipus

| Tipo | Atributo | n | Aciertos | Esperado nulo | Razón | p | q (BH) |
|---|---|---:|---:|---:|---:|---:|---:|
| cabecera | color | 23 | 15 | 4,77 | 3,15 | 0,0002 | **0,0020** |
| cabecera | familia de color | 23 | 15 | 4,82 | 3,11 | 0,0002 | **0,0020** |
| componente_A | color | 3 | 3 | 0,60 | 4,98 | 0,0054 | 0,031 |
| componente_A | familia | 3 | 3 | 0,58 | 5,19 | 0,0062 | 0,031 |
| celda_P | color | 45 | 33 | 32,09 | 1,03 | 0,41 | 1 |
| copia | color | 28 | 4 | 6,41 | 0,62 | 0,95 | 1 |
| cabecera | unión | 23 | 5 | 5,62 | 0,89 | 0,84 | 1 |
| celda_S | color | 45 | 0 | 3,89 | 0,00 | 1 | 1 |
| celda_P | unión | 45 | 0 | 0,28 | 0,00 | 1 | 1 |

Lectura:

- **Cabeceras:** el mismo total registrado en dos libros lleva el mismo color (blanco) 15/23 veces,
  tres veces más de lo esperado. Es el único atributo que se conserva claramente entre quipus, y
  es un atributo de **rol**, no de columna.
- **Celdas UR270–UR278:** el color coincide 33/45, pero el esperado es 32,1. No hay señal: UR270
  es blanco en el 97 % de los colgantes y cualquier libro blanco "acierta".
- **Copias:** 4/28 frente a 6,4 esperadas con el nulo estratificado (4,8 con el nulo simple de
  §3.2; p ≈ 1 en ambos). El color **no** se conserva. La unión se invierte sistemáticamente
  (0/28) y la torsión es constante (S en ambos), así que no informa.
- **Torsión:** es S en todos los libros considerados; cualquier prueba da p = 1. No es un atributo
  de categoría.
- **componente_A:** 3/3 con el mismo color. Es sugerente pero n = 3 y los tres pares son blancos;
  no se eleva a hallazgo.

### 3.2 El color marca la fila y el nivel, no la columna

| Prueba | Observado | Nulo | p |
|---|---:|---:|---:|
| A. UR278, filas monocromas | 23/28 | 0,01/28 | 0,0002 |
| B. UR270, colgante blanco en pares de color distinto | 61/62 | 31/62 (0,5) | 1,4·10⁻¹⁷ |
| C. UR278, MI(columna, color) | 0,015 bits | 0,020 bits | 0,77 |
| D. UR255–UR267A, color idéntico | 4/28 | 4,82/28 | 1,00 |
| D. UR255–UR267A, unión idéntica | 0/28 | — | — |

- En UR278 el color es de la **fila**: 23/28 filas tienen un solo color; las 5 restantes tienen 2
  (una cuerda de otro color). El color modal por fila es AB 12, W 10, NB 5, MB 1. Es decir, el
  color distingue **registros o grupos de registros**, no columnas.
- En UR270 el color es del **nivel**: colgante W (61/63) y subsidiaria NB/KB o mezcla (55/76).
  El par colgante/subsidiaria es un contraste de rol perfecto (61/62).
- En la copia UR255–UR267A el color es del **libro**: UR255 es casi monocromo AB (84/89) y UR267A es
  W/AB (51 W, 22 AB). La copia conserva la cifra y la torsión, pero no el color ni la unión.
- **Conclusión:** el color no es un marcador de la categoría "columna k". Marca (i) el registro o
  grupo en los libros de detalle, (ii) el nivel/rol dentro del registro, (iii) el estilo del libro.
  Es un atributo **jerárquico y local**, no un lexema.

### 3.3 La posición sí: las 9 partes y su orden

**Estructura.** UR278 tiene 28 registros con 9 columnas; UR270 tiene 7 grupos con 9 colgantes y sus
subsidiarias. La celda de UR278 es el colgante + la 1.ª subsidiaria de UR270: 39/45 celdas coinciden
±1 en la **misma posición ordinal**. En cada uno de los 5 pares, la permutación identidad es la
mejor de las 9! (única en 2 de 5; en los otros 3 hay entre 1 y 11 permutaciones empatadas):

| UR270 | UR278 | Celdas ±1 | p(permutación ≥ identidad) |
|---:|---:|---:|---:|
| 0 | 21 | 9/9 | 5,5·10⁻⁶ |
| 4 | 25 | 9/9 | 2,8·10⁻⁶ |
| 5 | 26 | 7/8 | 5,5·10⁻⁶ |
| 8 | 27 | 8/9 | 2,8·10⁻⁶ |
| 9 | 28 | 6/9 | 3,3·10⁻⁵ |

Producto = 7,4·10⁻²⁶ (las filas comparten registros, así que tómese como cota optimista; por fila
el p máximo es 3,3·10⁻⁵). **El orden de las 9 partes se conserva entre los dos libros.** No hay
permutación, desplazamiento ni reordenamiento por tamaño.

**Efecto de columna y firma.**

- Friedman (26 filas completas): χ² = 90,6, p = 3,5·10⁻¹⁶, W = 0,44.
- Varianza de las medias por columna: 0,00043 frente a 0,00005 del nulo (9,2×), p = 0,0002.
- Spearman medio entre pares de filas: 0,411 (nulo 0,000), p = 0,002.
- 0/28 filas están ordenadas de mayor a menor; 57 % de los pares adyacentes son descendentes (casi
  la mitad, como se espera de un orden no monótono).

### 3.4 Firma de las 9 partes

`firma_9_partes.csv` (proporción media del total del registro, IC 95 % bootstrap por filas,
n = 28 en UR278 y 7 en UR270):

| Parte | Proporción UR278 | IC 95 % | UR270 | Rango medio | Máx. | Mín. |
|---|---:|---|---:|---:|---:|---:|
| c1 | 0,135 | 0,125–0,145 | 0,143 | 2,8 | 9 | 0 |
| c2 | 0,140 | 0,128–0,152 | 0,163 | 2,6 | 9 | 2 |
| c3 | 0,096 | 0,087–0,105 | 0,103 | 6,3 | 1 | 6 |
| c4 | 0,107 | 0,102–0,113 | 0,118 | 5,1 | 0 | 0 |
| c5 | 0,116 | 0,107–0,127 | 0,093 | 4,4 | 4 | 0 |
| c6 | 0,132 | 0,119–0,147 | 0,150 | 3,7 | 4 | 0 |
| c7 | 0,111 | 0,099–0,123 | 0,090 | 5,2 | 1 | 4 |
| c8 | 0,083 | 0,072–0,093 | 0,063 | 7,4 | 0 | 7 |
| c9 | 0,090 | 0,082–0,097 | 0,084 | 7,2 | 0 | 9 |

Firma: **c2 ≈ c1 > c6 > c5 > c7 > c4 > c3 > c9 > c8**. Es decir, las dos primeras posiciones
concentran el 27,6 % del total (2/9 = 22,2 % si fuera uniforme), y las dos últimas el 17,2 %.

- **¿Una parte siempre mayor?** c1 o c2 es el máximo en 18/28 filas (esperado 6,2; p = 2,2·10⁻⁶).
  En UR270 el máximo está repartido: c2 3, c6 3, c1 1. Luego "c1/c2 mayor" es fuerte en UR278 y
  solo parcial en UR270.
- **¿Una parte siempre menor?** c8 o c9 es el mínimo en 16/28 (p = 6,5·10⁻⁵); en UR270 c8 es el
  mínimo en 5/7. La parte 8 es la más estable como "la menor".
- La correlación entre la firma de UR278 y la de UR270 es ρ = 0,85 (p = 0,004), pero 5 de los 7
  registros de UR270 son los mismos que los de UR278: no es una réplica independiente.
- **No invariante de escala:** la proporción de c1 y c2 baja con el total de la fila (ρ = −0,38 y
  −0,39) y la de c7 sube (ρ = +0,42; p sin corregir 0,025). Con 9 pruebas, ninguna supera BH
  (q ≈ 0,11–0,15). Se reporta como negativo débil.

### 3.5 La rejilla y el diccionario

- `rejilla.csv` (ancha): 35 registros (28 de UR278 + 7 de UR270) × 9 partes, con `cuota`, `total`,
  `color_registro`, `color_subsidiaria` y el identificador del par UR270↔UR278.
- `rejilla_larga.csv`: 441 filas, una por (registro, parte, componente P/S/celda), con valor,
  proporción, color, nivel, unión, torsión y largo.
- `diccionario_categorias.csv`: 7 categorías con su marcador y su nivel de evidencia.

| Categoría | Marcador | Atributos | Evidencia |
|---|---|---|---|
| cabecera (total bruto) | posición 1 + blanco | W 92/120 (77 %), nulo 29/120, p = 0,0003; nivel 0 | bien apoyado (estructura) / apoyado (color) |
| cuota c | posición 2; constante del libro | UR275 24/25 (p = 0,0002), UR266 12/25 (p = 0,001); color del libro (NB en UR275, YB/HB en UR266); UR269 2/65 (p = 0,93) | apoyado (posición); color = estilo |
| parte A (subsidiaria) | nivel 1; NB/KB o mezcla | UR270: 55/76; cuota 30/15 | bien apoyado (aritmética) / apoyado (color) |
| parte B (colgante) | nivel 0; blanco | UR270: 61/63 W; unión V; cuota 17/10 | bien apoyado (aritmética) / apoyado (color) |
| columna k (k = 1..9) | posición ordinal 1..9 | 39/45 celdas ±1; color de fila (MI p = 0,77); firma estable | bien apoyado (estructura y orden) |
| celda compuesta P+S | aritmética | 39/45 celdas ±1; en UR278 una sola cuerda | bien apoyado |
| neto n = x − c | siguiente a la cuota; a menudo ausente | sin color/posición propios | propuesto |

**Magnitud típica por categoría.** Cabecera: mediana 2 000 (rango 100–4 273; n = 120). Parte A:
mediana 450–453. Parte B: mediana 1 328–1 334 (es la parte grande del registro partido). Cuota: 47
en UR266/UR275, 46 en UR269, y 30/17/15/10/25/208 en sus libros locales. Columnas: mediana 139–298
en UR278 y 130–295 en UR270; c1, c2 y c6 rondan 290–300 y c8 ronda 130–139. La jerarquía de
magnitudes (cabecera ≫ parte B ≫ parte A ≈ columna) es coherente con la de roles, no con la de
columnas.

La prueba de posición de la cuota es un nulo de barajado dentro de cada grupo: en UR275 la cuota
cae en la 2.ª posición 24/25 veces (p = 0,0002) y en UR266 12/25 (p = 0,001). En UR269, el libro
maestro, solo 2/65 (p = 0,93): **la disposición "cabecera, cuota, partidas" es local a los libros
de componentes, no universal.**

### 3.6 Redundancia de la rejilla (`19_prediccion`)

El inventario de redundancia clasifica cada cuerda por las reglas que la sostienen. Para las 45
celdas de UR278 (5 filas × 9 columnas):

- 44/45 tienen una predicción por la regla `celda270`; 35/44 son exactas y 4 más caen ±1 (39/45,
  como en §3.3). La restante no tiene predicción.
- **Ninguna celda tiene dos vías independientes** (`n_vias_indep = 1` en las 44). La identidad
  columna a columna es, pues, una sola relación aritmética, no una doble entrada.
- Lo que sí tiene doble vía es el **total de la fila**: la regla `fila278` (suma de las 9 columnas)
  y la suma de las celdas `celda270` llegan a la misma cabecera de UR266/UR275. Es decir, la
  rejilla está verificada por arriba (total) y por abajo (celdas), pero cada celda individual
  descansa en una sola regla.
- En UR270, las 45 cuerdas de las 5 filas tampoco tienen una segunda vía (`n_vias_indep = 1`).

Esto no debilita el orden de las 9 partes (que se apoya en 39 coincidencias ±1 y en la optimalidad
de la identidad), pero sí obliga a presentar la firma como **una estructura de un libro verificada
contra otro**, no como un hecho doblemente contabilizado.

## 4. Controles, resultados negativos y explicaciones aburridas

1. **Nulo de color dentro de quipu y nivel** en las 20 pruebas de consistencia; BH. Solo las
   cabeceras superan q < 0,05 con un tamaño razonable.
2. **El color no marca la columna** (MI 0,015 vs 0,020; p = 0,77). La explicación aburrida
   (el color es del grupo/registro) se confirma: 23/28 filas monocromas.
3. **La copia incaica no conserva color ni unión** (4/28 y 0/28). Esto contradice la impresión de
   que "las copias conservan el color": en Incahuasi el color es una elección del libro. (14 encuentra
   conservación de color en el conjunto de familias del mismo registrador, Fisher p = 7·10⁻⁵, pero
   esta familia concreta no la muestra: 14,3 % frente a 17,2 % del nulo, p = 1,0.)
4. **No hay componente grande**: 95 componentes de 2–3 cuerdas. La categoría no es una cuerda que
   reaparece; es una ranura. Sin este paso, cualquier "diccionario" de cuerdas sería una lista de
   registros.
5. **La firma no es perfectamente estable en UR270 para el máximo** (c2 3, c6 3, c1 1). El mínimo
   (c8) sí se replica (5/7).
6. **No invariancia de escala** de las proporciones (|ρ| hasta 0,42), no significativa tras BH.
7. **UR269 no coloca la cuota en la 2.ª posición** (2/65). La estructura de 9 columnas y la de
   libro maestro son dos formatos distintos; no se deben mezclar.
8. **La torsión es constante (S)** en todos los libros del sistema: no discrimina categorías.
9. **La unión R/V es del libro** (UR255 R vs UR267A V; UR278 R vs UR270 V): no es un atributo de
   la categoría.
10. **`componente_A` 3/3** se reporta como sugerente, no como hallazgo: n = 3 y los tres pares son
    blancos.
11. **El color de la fila se asocia al tamaño, no a la forma.** En UR278, las filas AB tienen
    mediana 2 229 y las W 1 816 (Mann-Whitney p = 0,036), pero ninguna de las 9 proporciones
    difiere entre AB y W (p mínimo 0,066; 9 pruebas, ninguna significativa tras BH). La firma de
    las 9 partes no es un artefacto del color.

## 5. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| La celda de UR278 es colgante + 1.ª subsidiaria de UR270, columna a columna | **bien apoyado** (13/07; 39/45 ±1; el equipo rojo lo deja sobrevivir) |
| Las 9 partes están en el mismo orden en UR270 y UR278 | **bien apoyado** (identidad óptima 5/5; p ≤ 3,3·10⁻⁵ por fila) |
| Hay un efecto de columna estable (las 9 partes no son intercambiables) | **bien apoyado** (Friedman p = 3,5·10⁻¹⁶; var p = 0,0002) |
| La firma relativa es c2 ≈ c1 > c6 > … > c8 | **apoyado con datos** (28 filas; IC; réplica parcial en UR270) |
| El color marca la fila/registro en UR278 | **bien apoyado** (23/28 vs 0,01; p = 0,0002) |
| El color marca el nivel/rol en UR270 | **bien apoyado** (61/62; p = 1,4·10⁻¹⁷) |
| El color no marca la columna | **apoyado con datos** (MI p = 0,77; unión/torsión constantes) |
| La cabecera es blanca | **apoyado con datos** (92/120 vs 29/120; p = 0,0003) |
| La cuota va en 2.ª posición en UR266/UR275 | **apoyado con datos** (24/25 y 12/25; p ≤ 0,001) |
| Las 9 partes son depósitos, días, parcialidades o grupos de trabajo | **especulativo** |
| La firma se puede comparar con listas coloniales de parcialidades | **propuesto** (es la siguiente prueba, no un resultado) |

## 6. Limitaciones

- **Una sola rejilla de 9 partes.** Solo UR278 y UR270 tienen 9 columnas; los demás libros tienen
  1–5 cuerdas por registro. La firma se estima con 28 filas de un mismo libro (y 7 de otro que
  repite 5 registros). No hay réplica independiente de la firma.
- **Los 5 pares UR270–UR278 no son 5 experimentos independientes**: son 5 registros de un mismo
  par de libros. El producto de p es una cota optimista.
- **El alineamiento de copias selecciona por valor**, así que la conservación de cifras no es
  independiente; color y unión sí lo son (no intervinieron en la búsqueda).
- **La muestra de copias incaicas es 1** (UR255–UR267A). No se puede generalizar "las copias no
  conservan el color" a todo el corpus; sí se puede afirmar para este par.
- **KFG y OKR comparten la fuente Urton/Chu**, de modo que las 39/45 celdas no son dos lecturas
  independientes, sino dos quipus físicos distintos leídos por el mismo equipo.
- El "valor" es el decimal decodificado por KFG; un error de un nudo en una celda no cambia la
  conclusión (por eso se usa ±1).

## 7. Para el coordinador

- **La rejilla de 9 partes existe y está ordenada.** UR270 y UR278 registran las mismas 9 partes en
  el mismo orden: 39/45 celdas ±1 y la identidad es la mejor de las 9! en 5/5 registros
  (p ≤ 3,3·10⁻⁵ por fila). Es la evidencia más fuerte de esta ronda.
- **El color no sirve para alinear categorías.** No marca la columna (MI p = 0,77), marca la fila
  en UR278 (23/28 monocromas, p = 0,0002) y el nivel en UR270 (61/62, p = 1,4·10⁻¹⁷). En la copia
  UR255–UR267A el color ni siquiera se conserva (4/28, p = 1,0).
- **La posición y la cuota sí son marcadores.** Cabecera en 1.ª posición (blanca 92/120, 77 %),
  cuota en 2.ª posición en UR275 (24/25) y UR266 (12/25), pero **no** en UR269 (2/65): hay dos
  formatos de libro y no se deben mezclar.
- **Firma relativa:** c2 ≈ c1 (27,6 % del total) > c6 > c5 > c7 > c4 > c3 > c9 > c8 (17,2 %).
  c1/c2 es el máximo en 18/28 filas (p = 2,2·10⁻⁶); c8/c9 el mínimo en 16/28 (p = 6,5·10⁻⁵). La
  parte 8 es la más estable como "la menor" (5/7 en UR270).
- **La firma no es perfectamente invariante de escala**: las proporciones de c1/c2 bajan con el
  total (ρ ≈ −0,39) y c7 sube (ρ = +0,42), sin superar BH. Al comparar con listas coloniales hay
  que usar proporciones, no valores absolutos, y tolerar esa deriva.
- **No hay categorías como componentes conexas.** El grafo da 95 componentes de 2–3 cuerdas: lo
  que se repite es la ranura, no la cifra. El "diccionario" debe ser de posiciones y roles, no de
  cuerdas.
- **Advertencia para la comparación colonial:** las 9 partes solo están atestiguadas en un libro
  (28 registros) y su orden se verifica contra un segundo quipu que repite 5 de esos registros. La
  firma es una hipótesis estructural bien medida, no una réplica independiente.
- **Siguiente paso recomendado:** buscar en el archivo algún quipu con 9 columnas y cuota distinta
  de 47 (o con 5/6/7 columnas) para ver si la firma se conserva al cambiar el número de partes;
  y comparar la firma c1..c9 con las listas de parcialidades de los documentos coloniales de
  Lunahuaná/Cañete, probando permutaciones de las 9 etiquetas.
- **Scripts:** `01_grafo.py`, `02_columnas.py`, `03_rejilla.py`, `04_color.py`, `05_redundancia.py`,
  `comun_rejilla.py`; salidas `grafo_aristas.csv`, `grafo_componentes.csv`,
  `consistencia_atributos.csv`, `orden_9_partes.csv`, `pruebas_columnas.csv`,
  `firma_9_partes.csv`, `rejilla.csv`, `rejilla_larga.csv`, `diccionario_categorias.csv`,
  `estilo_quipu.csv`.
