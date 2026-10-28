# Monografía del archivo de Leymebamba (Laguna de los Cóndores): quipus UR001–UR022

## 0. Pregunta

¿Qué es y qué registra el conjunto de quipus UR001–UR022 (Laguna de los Cóndores / Leymebamba, okr KH0237–KH0258)? En concreto: (1) ¿cómo se describe el conjunto (tamaños, estructuras, colores, valores, sumas, cuerdas superiores, torsión, direcciones de nudo)?; (2) ¿hay relaciones *entre* estos quipus (secuencias de valores, totales que reaparecen, estructuras o patrones de color idénticos)?; (3) ¿se puede reconstruir una jerarquía de quipus de detalle y de resumen?; (4) ¿qué dice la literatura de este sitio y qué se registraba aquí?

## 1. Datos y método

- **Datos (ya preparados):** `analisis/datos/cuerdas.csv` (57 818 cuerdas; 5 167 pertenecen a UR001–UR022), `quipus.csv`, `grupos.csv` (KFG). Contraste puntual con `data/external/open-khipu-repository/data/khipu.db` (OKR/KDB) y con `data/external/data-science-khipu-article/data/ascher_sum_relations/` (relaciones de suma de KFG).
- **Unidad de análisis:** el **quipu** (22 unidades). Cuando el estadístico es a nivel de cuerda, el nulo se calcula barajando **dentro de cada quipu**, de modo que cada quipu conserva su número y su multiconjunto de valores.
- **Valor 0 con `nudos` vacío = ausente** (no se cuenta como cero). Se documentan aparte los **ceros reales** (valor 0 *con* cadena de nudos).
- **Nulos explícitos** (semilla 0, 500 permutaciones salvo donde se indique): (a) secuencias de valores → barajar valores dentro de cada quipu; (b) totales que reaparecen → **permutar los valores entre quipus** (dentro de un quipu el total es invariante al barajado, así que ese nulo no sirve para totales); (c) patrones de color → barajar colores dentro de cada quipu; (d) firmas de grupos → permutar etiquetas de grupo dentro de cada quipu.
- **Corrección de comparaciones múltiples:** Holm sobre la familia de tests declarada en cada bloque.
- **Etiquetas de evidencia:** bien apoyado / apoyado con datos / propuesto / especulativo.
- Scripts reproducibles en esta carpeta: `01_describe.py`, `02_structure.py`, `03_between.py`, `03b_distintivos.py`, `04_sums_hierarchy.py`, `05_trio.py`.

## 2. Descripción del conjunto

**Tamaño y contexto.** 22 quipus, okr KH0237–KH0258, Centro Mallqui (Leymebamba, Chachapoyas/Amazonas). Es el subconjunto "estudiable" del archivo de 32 quipus recuperados en 1996 (Urton 2005). **No hay nombres duplicados del mismo objeto dentro de esta serie**: `orig_inv_num` = UR001–UR022 únicos y `DUPLICATE_FLAG=0` en la KDB para todos. Total: **5 167 cuerdas**, de las que **3 348 son colgantes** (nivel 0), 1 625 subsidiarias (nivel 1), 186 de nivel 2, 7 de nivel 3 y 1 de nivel 4 (profundidad máxima en UR003).

**Tabla por quipu** (`suma valores` = suma decimal de *todas* las cuerdas con valor; `sumas internas` = cuerdas-madre que igualan la suma de sus hijas; `R/V/T` = unión recto/verso/cuerda superior):

| quipu | cuerdas | colg. | subsid. | nivel | grupos | val min-max | suma valores | sumas internas | color dominante | R/V/T |
|---|---|---|---|---|---|---|---|---|---|---|
| UR001 | 572 | 407 | 165 | 2 | 48 | 1-8308 | 93145 | 8 | AB (115/407) | 255/206/0 |
| UR002 | 116 | 72 | 44 | 2 | 10 | 1-8817 | 38975 | 0 | MB (15/72) | 23/46/0 |
| UR003 | 758 | 281 | 477 | 4 | 15 | 0-11 | 893 | 29 | AB (83/281) | 55/220/0 |
| UR004 | 573 | 482 | 91 | 2 | 73 | 1-2230 | 12304 | 5 | MB (279/482) | 213/246/0 |
| UR005 | 62 | 49 | 13 | 1 | 4 | 2-135 | 1531 | 0 | W (37/49) | 28/19/0 |
| UR006 | 874 | 571 | 303 | 2 | 63 | 0-521 | 3037 | 10 | MB (344/571) | 339/412/9 |
| UR007 | 80 | 45 | 35 | 2 | 16 | 1-10 | 74 | 2 | MB (21/45) | 4/41/0 |
| UR008 | 6 | 6 | 0 | 0 | 2 | 5-200 | 502 | 0 | W (6/6) | 0/6/0 |
| UR009 | 164 | 149 | 15 | 1 | 21 | 1-61 | 414 | 4 | MB (86/149) | 94/46/0 |
| UR010 | 176 | 159 | 17 | 1 | 30 | 1-153 | 2997 | 0 | W (63/159) | 63/91/0 |
| UR011 | 343 | 176 | 167 | 2 | 24 | 1-15746 | 261452 | 2 | W:MB (34/176) | 92/83/0 |
| UR012 | 126 | 50 | 76 | 2 | 12 | 0-1059 | 3158 | 1 | W (8/50) | 33/29/0 |
| UR013 | 59 | 24 | 35 | 2 | 7 | 0-90 | 647 | 0 | AB (11/24) | 8/14/0 |
| UR014 | 44 | 23 | 21 | 1 | 10 | 1-155 | 606 | 0 | W (15/23) | 14/6/0 |
| UR015 | 88 | 65 | 23 | 2 | 11 | 1-2565 | 29578 | 0 | W (14/65) | 17/45/0 |
| UR016 | 442 | 222 | 220 | 2 | 7 | 0-99 | 2965 | 7 | AB (211/222) | 220/0/0 |
| UR017 | 122 | 97 | 25 | 1 | 27 | 1-211 | 1355 | 15 | AB (38/97) | 54/32/0 |
| UR018 | 38 | 31 | 7 | 1 | 8 | 1-9018 | 27563 | 0 | AB (12/31) | 15/12/0 |
| UR019 | 18 | 13 | 5 | 1 | 4 | 1-28 | 100 | 0 | AB (4/13) | 4/8/0 |
| UR020 | 30 | 24 | 6 | 1 | 9 | 2-5004 | 25965 | 0 | W (6/24) | 13/9/0 |
| UR021 | 162 | 136 | 26 | 1 | 23 | 1-61 | 498 | 12 | MB (58/136) | 31/111/0 |
| UR022 | 314 | 266 | 48 | 1 | 31 | 1-572 | 6705 | 1 | W (252/266) | 159/102/0 |

**Rasgos transversales.**

- **Tamaños muy dispares:** de UR008 (6 cuerdas) a UR006 (874). Grandes (>400): UR006, UR003, UR004, UR001, UR016. Pequeños (<50): UR008, UR019, UR020, UR018, UR014.
- **Profundidad jerárquica baja:** casi todos tienen nivel máximo 1–2; UR003 llega a 4 (único).
- **Valores:** rango 1–15 746 (máximo en UR011). Valores pequeños dominan; varios quipus tienen un valor "grande" aislado (UR001 8308, UR002 8817, UR018 9018, UR020 5004, UR011 15 746) que convive con muchos 1–10.
- **Ceros reales** (0 *con* nudos, p. ej. `0L(7.0,U)`, `0E(...)`): solo 8 cuerdas, en UR003, UR006, UR012, UR013 y UR016. Frente a **1 565 cuerdas ausentes** (0 sin nudos): el uso del cero explícito es raro y localizado.
- **Sumas internas:** todas las cuerdas-madre que igualan la suma de sus hijas (verificación propia) suman 96 casos, pero **muchos son triviales** (una hija única de valor 1). Las relaciones de suma de KFG (más informativas) están en 19 de los 22 quipus; **UR007, UR008 y UR019 no aparecen** en ese archivo (dato ausente, no "sin sumas"). Más ricos en sumas: UR004 (549 relaciones), UR022 (302), UR016 (231), UR006 (222), UR010 (214).
- **Cuerdas superiores (unión T):** solo **UR006, 9 cuerdas**, todas hijas de `p24` (una cuerda sin nudos, valor 0) con valores 0,1,1,2,1,0,1,15,10. No forman una suma clásica de cuerda superior.
- **Unión R/V:** en el agregado R=1 734, V=1 784, U=1 581, T=9. Hay quipus **marcadamente a una sola mano**: UR016 = 220 R / 0 V (recto puro); UR003 = 220 V / 55 R y UR021 = 111 V / 31 R (verso dominante); UR007 = 41 V / 4 R. Esto apunta a fabricación diferenciada por quipu.
- **Torsión:** abrumadoramente **S** (5 013 S, 1 Z, 100 U). No hay señal de torsión Z sistemática.
- **Terminación:** dominante K (3 760 cuerdas).
- **Colores de colgantes:** MB 972, AB 680, W 631, KB 171, GG 100; combinaciones barber-pole W:MB 83, AB:MB 68, W:AB 63. **Advertencia de conservación:** UR022 es el "Washed Khipu" de la KDB; su blancura extrema (252/266) es con alta probabilidad **post-deposicional**, no registral.

## 3. Relaciones entre quipus (con nulos)

Todas las pruebas usan el quipu como unidad y nulos de permutación con semilla 0.

**(a) Subsecuencias contiguas de valores compartidas** (`03_between.py`). Estadístico = coincidencias de n-gramas entre pares de quipus (pares contados con multiplicidad).

| L | observado | nulo (500) | p | Holm |
|---|---|---|---|---|
| 3 | 265 | 156.2 ± 18.6 | 0.0020 | 0.014 |
| 4 | 57 | 30.0 ± 8.8 | 0.0060 | 0.030 |
| 5 | 12 | 4.7 ± 2.9 | 0.0299 | 0.120 |

Hay **exceso** de coincidencias a L=3–4. Pero el detalle muestra que **el exceso está dominado por patrones triviales** de enteros pequeños ubicuos: `(1,1,1)`, `(1,1,3)`, `(1,3,2)`, `(2,1,1)`… Al exigir patrones **distintivos** (`03b_distintivos.py`, valores ≥5 y ≥10, mismo nulo):

| test | observado | nulo | p | Holm |
|---|---|---|---|---|
| L=3, máx≥5 | 74 | 40.4 ± 8.6 | 0.0020 | 0.010 |
| L=4, máx≥5 | 7 | 5.0 ± 2.9 | 0.2355 | 0.463 |
| **L=3, máx≥10** | 14 | 10.7 ± 4.5 | **0.2315** | **0.463** |

El patrón distintivo (L=3 con un valor ≥10) **no supera el nulo**. La "señal" de L=3 se debe a que los quipus reales tienen **rachas locales de valores pequeños repetidos** (muchos 1) más que los barajados, lo que infla coincidencias genéricas. Conclusión: **no hay evidencia de secuencias de valores compartidas entre quipus distintos**.

**(b) Totales de un quipu que reaparecen en otro** (`03_between.py`). Nulo: permutar valores entre quipus (preserva tamaños y el conjunto global de valores). Observado **9/462** pares; nulo **5.4 ± 5.6**; **p=0.24** (Holm 0.71). **Negativo.** Las coincidencias concretas son triviales (p. ej. total(UR007)=52 reaparece en 5 quipus grandes cuyo rango de valores incluye 52; total(UR003)=263 en UR011, etc.).

**(c) Patrones de color idénticos** (`03_between.py`, `03b`). A L=8 el test ingenuo es significativo (obs 71 vs nulo 27.6, p=0.002), **pero todos los 8-gramas compartidos son de 2 colores**: son bordes de bloques monocromos (`W W W W W W W AB`, `MB MB MB MB MB MB MB AB`…). Al exigir **≥3 colores distintos** solo quedan 2 pares, y con **≥4 colores, cero**. A L=4 el observado incluso está *por debajo* del nulo (505 vs 558). Conclusión: el "patrón de color compartido" es un **artefacto de longitud de los bloques de color**, no una correspondencia entre quipus.

**(d) Estructuras de grupos idénticas** (`02_structure.py`, `03_between.py`). Ningún par de quipus comparte la **misma secuencia de tamaños de grupo** (obs=0). Negativo. Sí hay **regularidad interna** llamativa: UR011 tiene 14 grupos consecutivos de exactamente 5 cuerdas; UR006 tiene 23 grupos de 21–22; UR022 tiene casi todos sus grupos de 7–10; UR016 tiene grupos de 101 y 75. Esa regularidad es *intra*-quipu (probablemente andamiaje decimal), no un rasgo compartido entre quipus.

**(e) Test dirigido a las relaciones que cita la literatura** (`05_trio.py`). Urton (2005) afirma que UR6, UR9 y UR21 son cuentas duplicadas y que UR9/UR21 replican un segmento de UR6. Probamos la subsecuencia contigua de valores más larga (L*) por par y su significancia bajo barajado dentro de cada quipu:

| par | L* | p (crudo) | p (Holm) |
|---|---|---|---|
| UR006-UR009 | 5 (`1,1,1,1,1`) | 0.42 | 1.0 |
| **UR006-UR021** | **7** | **0.088** | **1.0** |
| UR009-UR021 | 5 (`1,1,1,1,1`) | 0.60 | 1.0 |
| UR004-UR006 | 5 (`1,3,1,1,1`) | 0.25 | 1.0 |
| UR012-UR013 (familia CMA-628) | 2 (`2,14`) | 0.15 | 1.0 |
| UR005-UR010 (familia CMA-480) | 2 (`16,15`) | 0.75 | 1.0 |

**Ningún par es significativo** tras Holm. Ni el trío de Urton ni las parejas de la misma familia de colección muestran secuencias compartidas más allá del azar. Resultado **negativo** para "cuentas duplicadas" a nivel de valores decodificados.

## 4. Jerarquía del archivo

- **A nivel de datos:** no encontramos ningún enlace de resumen → detalle (total de un quipu como valor de otro: p=0.24; secuencias compartidas: no significativo; estructuras de grupo idénticas: 0). Las sumas detectadas son **internas** a cada quipu (colgante-colgante, madre-hijas), coherentes con agregación local, pero **no** con consolidación de un quipu en otro.
- **Agrupación física por colección** (números de inventario de la KDB, útiles como proxy de lote/tumba): CMA-628 = UR002, UR011, UR012, UR013, UR014, UR015 (LC1-257 A–F); CMA-480 = UR005, UR007, UR008, UR010, UR017, UR018, UR019, UR020 (LC1-109.1–.6, 109A/B); además CMA-419 (UR003), CMA-847 (UR004), CMA-850 (UR009), CMA-373 (UR016), INC-498 (UR021), INC-109 (UR022), INC/LDC-108 (UR001). Dentro de cada familia **no** hay firmas de grupo ni secuencias compartidas, así que el parentesco de lote **no** se traduce en parentesco numérico.
- **UR006 como candidato a "resumen"** (es el *Calendar Khipu*): es el único con cuerdas superiores (T), el mayor del archivo y el más citado. Pero ver §5: los datos de KFG/OKR **no reproducen** la estructura publicada por Urton (762 colgantes en 24 conjuntos de 29–31), lo que obliga a cautela.

Nivel de evidencia de la jerarquía: **propuesto/negativo en los datos disponibles**; no hay jerarquía de resumen-detalle demostrable dentro de UR001–UR022.

## 5. Contraste con la literatura del sitio

- **Contexto (apoyado con datos):** 32 quipus hallados en 1996 con ~220 fardos en media docena de *chullpas* bajo un alero sobre la **Laguna de los Cóndores**, cerca de **Leymebamba** (Chachapoyas, Amazonas); materiales desde Chachapoya preinca (ca. 800–1450 d.C.) hasta inca y colonial temprano. De los 32, **22 estudiables** — exactamente nuestra serie (Urton 2001, 2005).
- **UR6 = calendario + censo (propuesto):** Urton (2001, 2005) interpreta UR6 como **calendario bienal + censo de contribuyentes**; 762 colgantes, 730 organizados en **24 conjuntos de 29–31 cuerdas** (= 2 años de 365 días), total de nudos corregido a 2 962; **10 conjuntos numéricos de tres términos** propuestos como "etiquetas de identidad"; si son etiquetas, el censo baja a 2 114. **UR9 y UR21 replicarían un segmento de cuatro meses de UR6 (~1/6)**. UR6 contendría el famoso *Calendar Khipu* (nickname confirmado en la KDB).
- **Contraste con nuestros datos (resultado negativo / discrepancia):** en KFG **y** en OKR/KDB, UR006 tiene **874 cuerdas** (571 colgantes), repartidas en grupos de 20–22, **no** de 29–31; su suma decimal de colgantes es 1 050. **No encontramos** ninguno de los conjuntos de tres términos citados (20-61-20, 11-35-20, 30-65-20, 10-30-10) en los valores decodificados de UR006. Es decir, KFG y OKR coinciden entre sí, pero **no** reproducen la estructura publicada por Urton. Esto puede deberse a diferencias de codificación/segmentación o a revisión de lecturas; en cualquier caso, la hipótesis calendárica **no es verificable** con los datos decimales disponibles, y el "match" UR6/UR9/UR21 no aparece en los valores (p crudo 0.088, Holm 1.0).
- **UR19 (Saez-Rodriguez 2014):** describe UR19 (CMA480/LC1-109.3) con **13 colgantes + 5 subsidiarias**, cordón principal de 26 cm, algodón Z-spin/S-ply blanco. Nuestros datos coinciden exactamente (13 colgantes, 5 subsidiarias, 18 cuerdas, pc 26 cm ⇒ **la codificación es fiable** para este ejemplar). Su lectura astronómica (π≈3.14, distancia Tierra-Luna) es el **contraejemplo metodológico** citado por el propio estado del arte: n=1, sin nulo ni control de multiplicidad, selección post hoc de divisores. No la reproducimos como hallazgo.
- **Datación (Cherkinsky 2014):** 5 muestras de Laguna de los Cóndores; 4 caen entre 1479–1538 y 1531–69 d.C. (inca tardío / colonial temprano), 1 atípica descartada. Es decir, el archivo es **tardío**, no Chachapoya clásico.
- **Sesgo de muestra (Clindaniel 2019; estado del arte):** esta es la **única colección serrana** de quipus; cualquier generalización al "imperio" está sesgada.

## 6. Qué se registraba aquí (propuesta)

La evidencia disponible es compatible con **varios registros contables independientes de pequeña escala** (valores 1–100 en su mayoría, con agregación interna colgante→subsidiaria), procedentes de **al menos dos contextos funerarios (lotes CMA-628 y CMA-480)**, sin un quipu-resumen detectable dentro de la serie. No se observa consolidación arithmetic entre quipus. La excepción candidata —UR006 como calendario/censo y sus presuntos duplicados UR9/UR21— **es una propuesta de la literatura que nuestros datos no confirman ni refutan del todo**: la discrepancia estructural KFG/OKR vs. Urton impide zanjarla. Nivel: **propuesto** para "registros contables locales (¿censo/tributo) agrupados por lote funerario"; **especulativo** para contenidos concretos (ayllus, meses, mitayos).

## 7. Nivel de evidencia (resumen)

| Afirmación | Nivel |
|---|---|
| UR001–UR022 = subconjunto estudiable del archivo de 32 quipus de Laguna de los Cóndores; sin duplicados de catálogo | **bien apoyado** (metadatos KDB/OKR) |
| Rasgos constructivos: torsión S dominante, terminación K, unión R/V ~50/50 con quipus "a una mano" (UR016 R, UR003/UR021 V) | **bien apoyado** (datos de cuerdas) |
| Ceros reales escasos y localizados (8 cuerdas) frente a 1 565 ausentes | **bien apoyado** |
| Colores MB/AB/W dominantes; W de UR022 probablemente post-deposicional (lavado) | **apoyado con datos** |
| Sumas internas presentes (agregación local) | **bien apoyado** (verificación propia + KFG) |
| **No** hay secuencias de valores compartidas entre quipus distintos (patrones distintivos superan el nulo) | **apoyado con datos** (negativo) |
| **No** hay totales de un quipu que reaparezcan en otro por encima del azar | **apoyado con datos** (negativo) |
| **No** hay patrones de color ni firmas de grupo idénticos entre quipus (color = artefacto de bloques) | **apoyado con datos** (negativo) |
| **No** se reproduce el match UR6/UR9/UR21 de Urton (2005) en los valores decodificados | **apoyado con datos** (negativo, con reserva por discrepancia de codificación) |
| UR006 = calendario + censo; UR9/UR21 subordinados | **propuesto** (Urton), no verificado aquí |
| Conjuntos de tres términos = etiquetas de identidad | **especulativo** (Urton 2005 lo admite) |
| UR19 registra π y distancias lunares | **especulativo** (Saez-Rodriguez 2014) |

## 8. Resultados negativos (explícitos)

1. **Sin secuencias de valores compartidas** entre quipus distintos una vez descartados los patrones triviales de 1s (L=3 con valor ≥10: p=0.23).
2. **Sin totales compartidos**: 9/462 coincidencias vs 5.4 esperadas (p=0.24).
3. **Sin patrones de color compartidos**: los 8-gramas compartidos son fronteras de bloques monocromos; con ≥4 colores, cero.
4. **Sin firmas de grupo idénticas**: 0 pares.
5. **Sin jerarquía resumen-detalle** detectable entre quipus.
6. **Discrepancia KFG/OKR vs. Urton (2005)** en el tamaño y la estructura de UR006.
7. UR007, UR008 y UR019 **no tienen datos de suma** en la fuente KFG (dato ausente, no ausencia de sumas).

## 9. Para el coordinador

- **Qué es:** 22 quipus, 5 167 cuerdas, okr KH0237–KH0258, Museo Centro Mallqui (Leymebamba). Es el subconjunto estudiable del archivo de 32 quipus de Laguna de los Cóndores hallado en 1996; **sin duplicados de catálogo** dentro de la serie (verificado en KDB: `orig_inv_num`/`DUPLICATE_FLAG`).
- **Archivo heterogéneo:** de 6 cuerdas (UR008) a 874 (UR006). Profundidad jerárquica baja (nivel ≤2 salvo UR003 = 4). Valores 1–15 746; **cero explícito rarísimo** (8 cuerdas) frente a 1 565 cuerdas ausentes.
- **Marcas de fabricación fuertes:** torsión S casi universal (5 013/5 167); unión **R/V ~50/50** en el agregado pero **"a una mano" por quipu** (UR016 = 220 R / 0 V; UR003 = 220 V / 55 R; UR021 = 111 V / 31 R). Colores MB/AB/W dominantes; el blanco extremo de UR022 es del "Washed Khipu", probablemente post-deposicional — no usarlo como color registral.
- **Negativo central (con control):** **no hay relaciones numéricas ni de color entre quipus**. Secuencias de valores distintivas (L=3, valor ≥10): p=0.23; totales compartidos: 9/462 vs 5.4, p=0.24; firmas de grupo idénticas: 0. Todo bajo nulo de permutación (semilla 0, 500) y Holm. La aparente señal a L=3 es un artefacto de rachas de 1s; la de color, de bloques monocromos.
- **El trío de Urton no se replica:** UR6/UR9/UR21 ("cuentas duplicadas") no muestran subsecuencia compartida significativa (mejor caso UR006-UR021 L*=7, p crudo 0.088, Holm 1.0). **Negativo apoyado con datos.**
- **Jerarquía:** no se puede reconstruir una relación resumen-detalle. Las sumas son **internas** a cada quipu. El único quipu "de resumen" citado (UR006, *Calendar Khipu*, con las 9 únicas cuerdas superiores del archivo) es candidato por literatura, no por aritmética.
- **Discrepancia de datos importante:** KFG y OKR coinciden en UR006 = **874 cuerdas / 571 colgantes / grupos 20–22**, pero Urton (2005) publica **762 colgantes en 24 conjuntos de 29–31** y suma de nudos 2 962; **no hallamos** sus 10 "conjuntos de tres términos". Recomiendo auditoría KFG↔KDB↔publicación para UR006 antes de dar por buena cualquier lectura calendárica.
- **Validación positiva:** UR19 reproduce exactamente la ficha de Saez-Rodriguez (13 colgantes + 5 subsidiarias, pc 26 cm) → la codificación es fiable; su lectura astronómica (π, Luna) es **especulativa** (n=1, sin controles).
- **Contexto:** datación tardía (4/5 muestras 1479–1569 d.C.); archivo de contexto funerario, **única colección serrana**, con fuerte sesgo geográfico. Propuesta: **registros contables locales de censo/tributo**, agrupados por lote funerario (CMA-628, CMA-480), sin consolidador detectable.
- **Siguiente ronda recomendada:** (1) auditoría de los datos UR006; (2) buscar la jerarquía no a nivel de valores sino de **estructura decimal** (bandas de color, grupos seriados) con nulos propios; (3) contrastar las "etiquetas de tres términos" en la KDB cruda; (4) replicar el negativo en otros archivos (Puruchuco, Inkawasi) para ver si la ausencia de *matching* es un sesgo de la codificación decimal.
