# 13 · El sistema contable del archivo de Incahuasi (Inkawasi)

Carpeta: `analisis/13_sistema_incahuasi/`. Scripts reproducibles con semilla fija; leen `analisis/datos/*.csv` y reutilizan `analisis/09_incahuasi/comun.py` (sin modificar nada fuera de esta carpeta). Convenciones del brief: valor 0 sin nudos = cuerda ausente; nulos explícitos; BH-FDR u Holm indicados en cada caso; con B réplicas el p mínimo es 1/(B+1).

## 0. Resumen

El archivo no es un conjunto de parejas sueltas. Es **un solo sistema de libros encadenados**, y casi todas sus piezas aparecen ahora unidas por aritmética exacta y en orden.

1. **Bien apoyado. Las "parejas atadas" son dos componentes de un mismo registro y se suman.** El registro i de UR273A más el registro i de UR273B da la cabecera de un registro de UR266, UR275 o UR269: 8 de 18 sumas son exactas, frente a 1,3 esperadas (p = 1·10⁻⁴; Holm 0,002; control con el resto del archivo: 0 coincidencias). Lo mismo ocurre con UR267A + UR267B, cuyas sumas dan los registros de UR269 con cuota 25 (3 de 6 exactas frente a 0,19 esperadas, Holm 0,005; 5 de 6 con ±1). Ejemplos: 453 + 1200 = 1653, 448 + 1289 = 1737, 808 + 2142 = 2950, 672 + 1575 = 2247, 215 + 613 = 828, 127 + 535 = 662 y 201 + 321 = 522.
2. **Bien apoyado. La cuota del registro consolidado es la suma de las cuotas de sus componentes.** 30 (UR274A) + 17 (UR274B/UR273B) = **47** (UR266/UR275/UR269), y 15 (UR267A/UR255) + 10 (UR267B/UR256) = **25** (UR269). Los registros consolidados que son sumas A+B llevan precisamente esa cuota (`salida_09_cuotas.txt`). La relación 47 = 30 + 17 no la notaron Urton ni los informes 04 y 09.
3. **Bien apoyado. UR270 es el detalle de esos componentes.** Sus colgantes blancos suman la parte B y sus primeras subsidiarias NB suman la parte A, en la misma fila de UR273B/UR273A (3 grupos exactos frente a 0,17 esperados; Holm 0,006). Además, **cada celda de UR278 es colgante + subsidiaria de UR270, columna a columna**: en 5 de 12 grupos coinciden entre 6 y 9 de las 9 columnas (±1), frente a 0,003 esperados (p = 0,0002 con dos nulos). Con solo los colgantes, ninguna fila coincide. Por ejemplo, UR270 g0 da 237 295 138 198 201 153 106 138 187, y UR278 g21 dice 238 295 138 198 201 153 106 138 187.
4. **Bien apoyado (heredado de 04 y ampliado).** Los totales de las filas de UR278 son las cabeceras de UR266 y UR275, en orden (τ = 1 con 15 y 9 pares). Así, una misma cifra se alcanza por dos caminos independientes: sumando 9 columnas (UR270 → UR278 → UR266/UR275) o sumando 2 componentes (UR270 → UR273A/B → UR266/UR275/UR269). Es un control cruzado de tipo "doble entrada".
5. **Apoyado con datos. UR269 es un libro maestro con bloques de 5 filas.** Las cabeceras que son suma de UR273A+B ocupan la **1.ª fila** de su bloque: 4 de 4 exactas y 6 de 6 contando ±1 (P al azar = 1·10⁻³ y 5·10⁻⁵). Las que son suma de UR267A+B ocupan la **última**: 4 de 5 exactas y 7 de 8 con ±1. Las cuotas modales por fila son 47, 46, 46, 44 y 25. Lectura: cada bloque es un periodo, y en él cada uno de 5 flujos aporta un registro. Se han identificado 2 de los 5 flujos; los otros 3 (cuotas 46, 46 y 44) no están en el archivo conservado.
6. **Verificaciones pedidas.** La cuota 17 aparece solo en UR273B y UR274B (más una vez suelta en UR267B). "Cabecera seguida de 47" se da solo en UR266 (17 de 26 registros), UR275 (24 de 25) y UR269 (8, con variantes 46 y 44). La cuota 208 aparece solo en UR268 (19 de 29), y la búsqueda ciega de la constante de cada quipu encuentra c significativa en 10 quipus, todos UR del depósito (Qolqawasi: corredor y kallankas). La constante de UR274A sale 44 en la búsqueda aritmética, pero la cuerda explícita es 30 (15 de 15). **Negativo:** ningún quipu JC (Sector B) se enlaza con nada.
7. **Niveles superiores: negativo o especulativo.** Ningún total de grupo de UR266 aparece en otro quipu (§2.8). Que UR268 (cuota 208) resuma los bloques de UR269 es solo una coincidencia sugerente: 47 + 46 + 46 + 44 + 25 = 208 (P ≈ 0,03 por azar), y las sumas de bloque caen en el rango de UR268 (7400–12 000), pero ninguna coincide exactamente.

## 1. Método y scripts

| Script | Qué hace | Nulo |
|---|---|---|
| `00_volcado.py` | Vuelca los 52 quipus grupo a grupo (`volcado_archivo.txt`; formato `valor_color`, `[sN:valor_color]` = subsidiaria). | — |
| `01_enlaces_valores.py` | LCS en orden entre los 378 pares de quipus con ≥3 valores ≥100; tolerante (±1 dígito) y robusta (exacta, sin múltiplos de 100). | Cada valor de B se sustituye por uno de los 40 más cercanos en escala log del resto del archivo (preserva magnitud y orden de magnitudes); BH. |
| `02_agregados.py` (+ `02b_control_magnitud.py`) | Búsqueda exhaustiva de totales: grupo, grupo con subsidiarias, subsidiarias de grupo, colgante+subsidiarias, subsidiarias de un colgante, columna, color por grupo, color por quipu, bloque y total. Cada total se busca en todas las cuerdas de los 52 quipus. | Permutar valores dentro de cada nivel en A (conserva magnitudes, tamaños de grupo y huecos), con refinamiento a 21 000 réplicas; BH sobre las 13 260 pruebas. 02b: nulo de magnitud en B. |
| `03_constantes.py` | (a) Descubre la cuota c de cada quipu por la aritmética x − n = c, aunque la cuerda c esté en blanco. (b) Verifica 10/15/17/20/25/30/40/44/46/47/208 en todo el archivo. | Barajar entre registros las cuerdas que no son cabecera; BH. |
| `04_componentes.py` | Sumas A+B registro a registro; UR270 P/S frente a UR273/UR274; prueba dirigida en las filas de UR269 con cuota 25 o 47. | Barajar B entre registros (rompe solo el emparejamiento); en UR270, permutar dentro de nivel o barajar S entre grupos; Holm. |
| `05_ur278_tabla.py` | UR278 como tabla de 28 filas × 9 columnas: efecto de fila, de columna, columnas gemelas y CV. | Permutar columnas entre filas o dentro de fila. |
| `06_grafo.py` | Grafo a nivel de cuerda (`grafo_cuerdas.csv`, 637 aristas) y libro consolidado con fuentes (`libro_consolidado.csv`). | (Reúne lo probado.) |
| `07_ur270_ur278.py` | Celdas de UR278 frente a colgante + subsidiaria de UR270, columna a columna. | Nulo 1: permutar las 9 sumas dentro de cada grupo. Nulo 2: permutar subsidiarias entre colgantes. Control: solo colgantes. |
| `08_orden.py` | τ de Kendall entre la posición del registro de origen y la del destino; posición en el bloque de UR269. | Permutar las posiciones de destino; BH. |
| `09_cuotas.py` | Relaciones entre cuotas: numerología frente a estructura. | Cuotas log-uniformes en [10, 250]. |
| `10_jaspeadas.py` | Color por rol (x, c, n, partidas) en 222 registros. | Permutar colores dentro de cada registro. |

**Definición de registro.** Un registro es un grupo de colgantes que no es separador rosa (PK). Su cabecera es el primer colgante anudado. En UR273A/B y UR274A/B los separadores rosas están en las mismas posiciones, y eso permite alinear "registro i con registro i".

## 2. Resultados

### 2.1 Enlaces entre quipus por cifras compartidas en orden (`01`, `salida_01_enlaces.txt`)

En la versión robusta (exacta, sin números redondos) hay 7 pares con q < 0,05 de 378:

| Par | LCS robusta | nulo media / máx | q |
|---|---|---|---|
| UR255–UR267A | 20 | 3,6 / 9 | 0,013 |
| UR256–UR267B | 20 | 2,3 / 7 | 0,013 |
| UR266–UR275 | 25 | 2,9 / 8 | 0,013 |
| **UR273B–UR274B** (nuevo) | 4 (tolerante 10) | 0,0 / 0 | 0,013 |
| **UR273A–UR274A** (nuevo) | 4 (tolerante 6) | 0,5 / 3 | 0,013 |
| **UR269–UR275** (nuevo) | 7 | 2,8 / 7 | 0,043 |
| UR257–UR278 | 1 | 0 / 0 | artefacto: una sola coincidencia de un valor sin vecinos de magnitud |

Tres pares que solo salen con tolerancia (JC007–UR268, UR271–UR274B y UR269–UR274B) son **artefactos de números redondos**: 5000 frente a 4000/6000, o 1300/1000 frente a 1200/2000. Desaparecen en la versión robusta. Las dos parejas nuevas tienen la misma estructura que las de Urton y Chu: quipus con la misma disposición de registros (separadores rosas en los grupos 10, 14, 16, 23 y 27 en UR273A y UR273B), con la cuota explícita en un miembro (30 en UR274A en 15 de 15 registros; 17 en UR274B) y la cabecera sola, con cuerdas en blanco, en el otro (UR273A/B).

**Negativo.** Ningún par que incluya un quipu JC pasa el FDR. Los 23 quipus del Sector B no se enlazan con el Sector A ni entre sí.

### 2.2 Los componentes A y B se suman en el libro consolidado (`04`, `componentes_*.csv`)

| Prueba | Sumas halladas (exactas) | Nulo media / máx | p | Holm |
|---|---|---|---|---|
| UR273A + UR273B → UR266 ∪ UR275 ∪ UR269 | **8 de 18** | 1,27 / 6 | 1·10⁻⁴ | 0,0018 |
| idem, control (resto del archivo) | 0 | 0,29 | 1 | — |
| UR274A + UR273B → consolidado | **7 de 18** | 1,58 / 7 | 6·10⁻⁴ | 0,0078 |
| UR269, registros con cuota 25: cabecera = UR267A + UR267B | **3 de 6** (5 con ±1) | 0,19 / 3 | 3·10⁻⁴ | 0,0051 |
| UR269, registros con cuota 47: cabecera = UR273A + UR273B | **3 de 8** (5 con ±1) | 0,33 / 3 | 6·10⁻⁴ | 0,0078 |
| UR267A + UR267B → consolidado (sin dirigir) | 6 | 2,6 / 10 | 0,036 | 0,33 |
| UR255 + UR256, UR274A + UR274B, cruces | 1–6 | ≈ nulo | 0,03–0,87 | ≥ 0,3 |

Las copias UR255/UR256 y UR274B no se alinean registro a registro con su par (tienen otra disposición de grupos), así que no sirven para esta prueba. UR274A sí se alinea con UR273B, y **rellena los huecos de UR273A**: donde UR273A está en blanco, 391 (UR274A) + 887 = 1278 (UR266/UR275), 891 + 1129 = 2020 (UR275 g13 y UR269 g69) y 772 + 1334 = 2106 (UR266 g24, UR275 g15). UR274A funciona, pues, como copia y complemento de UR273A.

Sumas exactas, con su destino (`grafo_cuerdas.csv`):

| Registro | Parte A (cuota 30) | Parte B (cuota 17) | A + B | Destino (cuota 47) |
|---|---|---|---|---|
| 3 | 808 (273A) | 2142 | 2950 | UR266 g19, UR275 g10, = total de UR278 g14 |
| 5 | 391 (274A) | 887 | 1278 | UR266 g21, UR275 g12, = total de UR278 g16 |
| 6/7 | 891 (274A) | 1129 | 2020 | UR275 g13, UR269 g69 (UR266 y UR278 dicen 2114/2115; UR266 cuelga 94 = la diferencia) |
| 8 | 772 (274A) | 1334 | 2106 | UR266 g24, UR275 g15 (UR278 g19 = 2105) |
| 9 | 453 | 1200 | 1653 | UR266 g25, UR275 g16, UR269 g5 (UR278 g21 = 1654) |
| 11 | 448 | 1289 | 1737 | UR266 g26, UR275 g17, UR269 g11 |
| 12 | 502 | 1325 | 1827 | UR269 g17 (UR275 g18 = 1825) |
| 13 | 448 | 1332 | 1780 | UR275 g19, UR269 g23 |
| 17 | 672 | 1575 | 2247 | UR275 g21 |
| 18 | 509 | 1256 | 1765 | UR266 g33 |
| 19 | 325 | 1181 | 1506 | UR266 g34 / UR275 g23 / UR269 g49 = 1505 (±1) |

| Registro | Parte A (UR267A, cuota 15) | Parte B (UR267B, cuota 10) | A + B | UR269 (cuota 25) |
|---|---|---|---|---|
| 11 | 215 | 613 | 828 | g21: 828, 803 (= 828 − 25) |
| 14 | 141 | 601 | 742 | g41: 742 |
| 15 | 127 | 535 | 662 | g47: 662, 637, 25 |
| 16 | 110 | 603 | 713 | g53: 712, 687 (±1) |
| 18 | 201 | 321 | 522 | g65: 522, 497, 25 |
| 21 | 63 | 329 | 392 | g81: 392 |

El orden se conserva: UR267A+B → UR269 τ = 1 con 5 pares exactos (p = 0,009); UR273A+B → UR275 τ = 1 (p = 0,007); UR274A+UR273B → UR275 τ = 1 (p = 0,0012). Hacia UR266 el τ es solo 0,2, porque una coincidencia espuria (1506 = UR266 g2, que es el total de UR278 g1) rompe la serie.

### 2.3 UR270, el detalle de los componentes, y UR278 (`04`, `07`)

- **Colgantes y subsidiarias de UR270 → UR273B/UR273A.** P (suma de los colgantes blancos de un grupo) aparece exactamente como cabecera de UR273B/UR274B en 6 de 18 grupos, frente a 0,55 esperados (Holm 0,007). S (suma de las primeras subsidiarias) **no** aparece por sí sola de forma significativa en UR273A/UR274A (1 exacta; 8 con ±1 frente a 6). En cambio, la prueba conjunta (P = B_i exacto y S = A_i ±1 en la **misma fila**) da 3 frente a 0,17 (p = 4·10⁻⁴; Holm 0,006): g0 1200/453 → fila 9; g8 1575/673 → fila 17 (672); g9 1256/510 → fila 18 (509). P + S aparece en el libro consolidado (1653, 2248 ≈ 2247, 1766 ≈ 1765, 1940 ≈ UR266 1939), pero por sí solo no supera el nulo (3 exactas, p = 0,07–0,16).
- **Celdas de UR278 = colgante + subsidiaria de UR270** (`ur270_ur278.csv`):

| UR270 | UR278 | Columnas que coinciden (±1) |
|---|---|---|
| g0 | g21 | 9/9 |
| g4 | g25 | 9/9 (302 frente a 301) |
| g5 | g26 | 7/9 (una en blanco) |
| g8 | g27 | 8/9 (246 frente a 290) |
| g9 | g28 | 6/9 |
| g10 | g29 | 5/9 |

En orden (τ = 1). Estadístico "grupos con ≥6 columnas": 5, frente a 0,003 (nulo 1) y 0,005 (nulo 2), p = 0,0002 en ambos. **Control: solo colgantes, 0 grupos.** La celda de UR278 es, pues, la suma de la parte B (colgante) y la parte A (subsidiaria) de la misma unidad.

### 2.4 UR278 por dentro (`05`): 33 filas × 9 columnas

- 28 filas con ≥7 colgantes (33 grupos con ≥2, como en 04). Hay un efecto de fila fuerte: ρ medio entre columnas de 0,63 (nulo 0,00; p = 0,0002), y el CV dentro de fila es 0,28 frente a 0,43 (p = 0,0005). Las filas son "unidades con tamaño".
- Hay un efecto de columna (Friedman 90,6 frente a 8; p = 0,0002). Las columnas 1 y 2 son siempre las mayores (rango medio 2,6) y las columnas 8, 9 y 3 las menores (la 9 es la mínima de la fila en 9 de 26 filas, la 8 en 7). Las columnas son categorías estables.
- Columnas gemelas (|ci − cj| ≤ 1): 71 frente a 70,9. **Negativo**: las repeticiones (415 415, 342 342) se explican porque las filas son casi constantes, no porque haya columnas duplicadas.
- **Las filas son registros sucesivos del mismo flujo (cuota 47).** Las filas 11–19 de UR278 corresponden a los registros 0–8 de UR273 (4273 ≈ 4263, 2950, 1278 y 2106 exactas o ±1) y las filas 21–29 a los registros 9–19 (por la vía de UR270). Las filas 0–10 son anteriores a lo que conservan UR273 y UR274.

Respuesta a la pregunta 2: **sí, UR278 resume un quipu de detalle (UR270)**, pero solo para su segundo tramo; el detalle del primer tramo no se conserva. Las 33 filas son **33 registros sucesivos** de un único flujo con cuota 47 [apoyado], cada uno repartido en 9 subunidades estables [bien apoyado como estructura]. Que las 9 columnas sean depósitos, días o grupos de trabajo es [especulativo]. Ver §4.

### 2.5 Cuotas: dónde están y cómo se relacionan (`03`, `09`)

Descubrimiento ciego de c (x − n = c, aunque la cuerda c esté en blanco; nulo: barajar cuerdas entre registros):

| Quipu | Registros | c* | Apoyo (nulo) | q |
|---|---|---|---|---|
| UR267B / UR256 | 25 / 21 | 10 | 13 (1,2) / 8 (1,1) | 0,0009 |
| UR267A / UR255 | 18 / 16 | 15 | 12 (1,5) / 6 (1,2) | 0,0009 |
| UR275 / UR266 | 25 / 26 | 47 | 7 (1,0) / 3 (1,0) | 0,0009 |
| UR269 | 58 | 46 (y 47, 44, 25 en la verificación) | 10 (1,2) | 0,0009 |
| **UR268** | 29 | **208** | 4 (1,0) | 0,0009 |
| **UR274B** | 19 | **17** | 3 (1,1) | 0,002 |
| UR274A | 15 | 44 (la cuerda explícita es 30: 15/15, q < 0,05) | 2 (0,9) | 0,026 |
| UR278, UR270, UR262, UR273B | — | ninguna | — | ≥ 0,35 |

Verificación (`constantes_verificacion.csv`; nº de registros con neto x − C / con C justo después de la cabecera; * = q < 0,05):
- **17**: UR274B 3*/10 y UR273B 0/3. En ningún otro quipu.
- **"Cabecera + 47"**: UR275 7*/24*, UR266 3*/17 y UR269 4*/8. En los demás, como mucho 1/1.
- **30**: solo UR274A (0/15*).
- **208**: solo UR268 (4*/19*).
- **10** y **15**: solo en sus parejas.
- **"Total = x + 17"** (04): se confirma en UR274B, donde x es el total P de un grupo de UR270: 1402 = 1385 + 17 (UR270 g5), 1300 = 1283 + 17 (g6) y 1332 = 1315 + 17 (g4; la cuerda dice 10). No aparece en otro sitio.

**Relaciones entre cuotas.**
- **Estructural, bien apoyada:** cuota del consolidado = cuota de A + cuota de B. Así, 30 + 17 = 47 y 15 + 10 = 25. En los registros consolidados que son sumas A+B exactas, la cuota explícita o implícita es 47 (14 casos) o 25 (3 casos); solo hay 2 registros de 47 con 40 (UR275 g10, UR269 g23).
- **Numerología pura, débil:** entre {10, 15, 17, 30, 47, 208} hay 2 relaciones de suma (17 + 30 = 47 y 15 + 15 = 30). Con cuotas al azar, P(≥2) = 0,038; añadiendo 25, P(≥3) = 0,012. Sin la estructura no significaría nada.
- **Especulativo:** 47 + 46 + 46 + 44 + 25 = 208, la cuota de UR268. Si se suman 5 cuotas de UR269 al azar, P(= 208) = 0,026.
- **Negativo:** no hay relación de producto ni de proporción. La cuota no es proporcional al bruto (ya lo mostró 09) y 10, 15, 17 y 30 no son múltiplos de una unidad común.

### 2.6 UR269, un libro maestro en bloques de 5 (`08`)

Bloques separados por cuerdas rosas.
- Las cabeceras que son suma de UR273A+B están en la **fila 1** del bloque. Con sumas exactas, 4 de 4 (g5, g11, g17, g23; P al azar = 1/750 ≈ 1·10⁻³). Contando ±1, 6 de 6 (+ g49, g61; P = 5·10⁻⁵).
- Las que son suma de UR267A+B están en la **última fila**. Con sumas exactas, 4 de 5 (g21, g47, g65, g81; P de esas 4 = 1/450). La quinta, g41, es la 4.ª de un bloque de 9 que parece doble, sin separador. Contando ±1, 7 de 8 (+ g53, g77; g100 es una coincidencia con un neto, 1618 ≈ 1617, y no cuenta). Las cuotas por fila (09) son 47, 46, 46, 44 y 25. Los registros de cada flujo avanzan con los bloques: UR273, registros 9, 11, 12, 13, 15, 19 y 21–22 en los bloques 1–9; UR267, registros 11, 14–15, 16, 18 y 21 en los bloques 3, 6, 7, 9 y 12.

### 2.7 Color y jaspeadas (`10`)

En 222 registros con cuota, la **cabecera es blanca** en el 73 % (nulo 31 %; p = 0,0002). Se cumple por separado en UR266, UR267A, UR267B, UR268, UR269, UR274A, UR274B y UR275 (UR255 y UR256 son AB monocromos). La cuota nunca es jaspeada (2 % frente a 8 %).

**El neto jaspeado no es general.** Destaca solo en UR275 (56 % frente a 14 %; p = 0,0002). En el conjunto sube al 17 % (nulo 6 %), y en UR269 y UR268 lo jaspeado son las **partidas intermedias** (35 % y 40 % frente a 25 % y 28 %; p ≈ 0,002). En UR270 la parte A (subsidiarias) es NB o W:NB y la parte B (colgantes) es W.

Lectura: el color marca el **rol** "bruto" (blanco) de forma general y otros roles de forma local. Que el jaspeado señale el resultado (Clindaniel) solo vale para UR275 y el comienzo de UR267A.

### 2.8 Búsqueda exhaustiva de totales (`02`)

**Familia completa.** Son 13 260 pruebas: 52 quipus A × 10 tipos de agregado × 52 quipus B; reciben nulo las 1360 que tienen ≥2 coincidencias, y las que quedan en p ≤ 0,005 reciben 21 000 réplicas. **Ninguna llega a q < 0,05 en la familia completa.** Las seis mejores tocan el p mínimo (4,8·10⁻⁵) y se quedan en q = 0,105: con m = 13 260, una prueba exhaustiva de este tamaño no puede certificar relaciones de 4 a 12 coincidencias. Por eso las relaciones de §2.2–2.3 se prueban como hipótesis dirigidas, con su propia familia y Holm. Control adicional en `02b_control_magnitud.py`: nulo del lado B que preserva la magnitud (`agregados_control_magnitud.csv`).

| A → B (tipo) | Exactas | Nulo A / p | Nulo B (magnitud) / p | Lectura |
|---|---|---|---|---|
| UR278 → UR266 (G, total de grupo) | 12 | 0,7 / 5·10⁻⁵ | 1,7 / 2·10⁻⁴ | relación conocida (04) |
| UR278 → UR275 (G) | 7 | 0,8 / 5·10⁻⁵ | 2,6 / 0,004 | ídem |
| UR270 → UR274B / UR273B (G) | 5 / 4 | 0,4 / 1·10⁻⁴; 0,2 / 2·10⁻⁴ | 1,5 / 0,004; 1,2 / 0,008 | parte B (§2.3) |
| UR270 → UR278 (PS, colgante + subsidiarias) | 53 de 82 | 38 / 4·10⁻⁴ | 34 / 2·10⁻⁴ | celdas de UR278 (§2.3; 07 lo prueba por columna) |
| UR269 → UR269, UR275 → UR275 (CG, total por color) | 8; 7 | 1 / 5·10⁻⁵ | 0,8–2,4 / 2·10⁻⁴ | **trivial**: neto y cuota del mismo color suman la cabecera (x = n + c) |
| UR255 → UR270 (G) | 11 | 4,7 / 0,001 | 7,2 / 0,019 | **artefacto de densidad**: los totales x + 15 caen en la franja 100–250, saturada de valores en UR270 |
| UR260 → UR270 (PS) | 6 | 1,8 / 5·10⁻⁴ | 3,9 / 2·10⁻⁴ | candidato débil: 6 valores de 101 a 192 en colgantes blancos de UR270 (100, 150 redondos) |
| JC013 → UR278 (PS) | 2 | 0,1 / 0,001 | 0,9 / 2·10⁻⁴ | solo 2 valores (120, 144): no interpretable |

**Negativos de la búsqueda exhaustiva:**
- Ningún total (de grupo, color, columna, bloque o quipu) de **UR266**, UR269, UR275, UR268 ni UR273A/B aparece en otro quipu más de lo esperado. Lo mejor es UR266 CG → UR273B, con 2 coincidencias (p = 0,016).
- Ningún agregado del archivo reproduce las cifras de **UR257** (p ≥ 0,02 con 2 coincidencias).
- **UR268** solo recibe 2 totales de bloque de UR274A (p = 0,006; q = 1).
- Los **totales por color** no forman un nivel propio, salvo la reformulación trivial x = c + n.
- Los quipus JC no participan en nada.

Respuesta a la pregunta 2: **no hay un nivel por encima de UR266 en lo conservado.**

### 2.9 ¿Hay un nivel por encima?

- **UR266 → ?**: no. Ningún total de UR266 (de grupo, color, columna o bloque) aparece en otro quipu (§2.8).
- **UR269 → UR268 (cuota 208)**: las sumas de los bloques de UR269 (7384–12 158) caen en el rango de las cabeceras de UR268 (7135–15 039). Dos quedan cerca (9335 frente a 9332; 10 379 frente a 10 385), pero no hay ninguna coincidencia exacta y el orden no se mantiene. Con la coincidencia 47 + 46 + 46 + 44 + 25 = 208, queda como **especulativo**: UR268 sería el nivel de periodo y UR269 el desglose por flujos. Para probarlo harían falta los bloques que faltan.
- **UR257** (98 718, 74 065, 44 385...): ningún total del archivo lo reproduce (§2.8). **Negativo.**
- Las subsidiarias grandes de UR266 (1070, 473, 1151, 2069, 832, 2500, 3300, 685, 167; colores 0G/0B) cuelgan de la cuerda en blanco que sigue al 47. Urton (2017: 168) señala 1070 + 1217 = 2287, el neto de UR275 g0. Fuera de ese caso no he encontrado su regla. **Sin resolver.**

## 3. Literatura (grep en `analisis/fuentes_txt` y `docs/fichas`)

**Urton 2017, cap. 9 "Accounting in the King's Storehouse", pp. 154–177** (`fuentes_txt/InkaHistoryinKnotsReadingKhipusas.txt`, líneas 1629–2440):

- **Contexto.** Inkawasi está a 28 km aguas arriba en el valle de Cañete. Fue base militar de la campaña contra los Huarco y el "Nuevo Cuzco" de Cieza. El depósito, Qolqawasi, tiene 6 estructuras al norte (4 kallankas, U.A. 01/02/04/05, y 2 "espacios de clasificación", U.A. 07/08), 36 grandes cámaras centrales y 209 colcas pequeñas; unos 6400 m³. En el suelo de U.A. 07 hay cuadrículas de 23 × 23 cm, impresas con cuerdas, en paneles de 3 × 39 (≈30 paneles, unos 3510 cuadros). Se interpretan como unidades estándar de clasificación.
- **Hallazgos.** 34 quipus (Chu, 2013–2014); Urton describe 29.
  - Corredor norte (sector C, subsector 5): una pila de 7 quipus, UR255–UR261, con UR255 y UR256 atados.
  - U.A. 07: UR267A y UR267B atados, en un cesto cubierto de **ají**.
  - Kallanka U.A. 04: **14 quipus bajo maní**. Son UR266, 268, 269, 270, 272, 273A, 273B, 274A, 274B, 275, 276, 277, 278 y 279. El texto dice U.A. 05 y el apéndice U.A. 04: hay una incoherencia.
  - UR271, bajo **frijol negro**, en la misma kallanka.
  - UR262–265 y UR280, en la kallanka U.A. 02.
  - UR273A/B comparten la U.E. 14 y UR274A/B la U.E. 15.
- **Lo que dijo Urton.**
  - "Internal summing" (cabecera = suma del resto).
  - "Fixed values" 208, 47, 15 y 10, leídos como "something like a tax, or levy... for the support and maintenance of the site". En el apéndice anota también "fixed value 30" (UR274A) y "17" (UR274B), pero no las relaciona.
  - UR266 y UR275 son "the only two that contain... 47". Es falso: UR269 lo tiene en 8 registros y con variantes 46 y 44.
  - La pareja UR266–UR275 es un "closely matching" (18 de 43 valores >1000 idénticos). Propone una contabilidad casi de doble entrada (créditos frente a débitos).
  - Las parejas atadas UR255–UR256 y UR267A–UR267B se emparejan en cruz, con "paradigmas aritméticos recíprocos" (X/c/Y frente a X/Y/c), y menciona el error 152 − 10 = 143 corregido en UR256.
  - Atar quipus serviría "perhaps to aggregate into the same large account the enumeration of different products".
  - Sobre UR273B: "numbers similar to thousands numbers on matching pair UR266 and UR275".
  - Explica el cambio de cuota 208 → 47 por la magnitud o el "estatus" del campo de origen.
- **Lo que este informe añade o corrige.**
  1. La agregación de quipus atados no es solo física, es **aritmética**: A + B = registro consolidado, y cuota A + cuota B = cuota consolidada (15 + 10 = 25; 30 + 17 = 47). Urton intuyó el "same large account"; aquí queda bien apoyado.
  2. UR273B no se "parece" a UR266/UR275: es **un sumando** de sus cifras.
  3. La diferencia entre 208, 47, 25, 17, 15 y 10 no tiene que deberse al producto ni al estatus del campo. Responde al **nivel de agregación**: componente (10, 15, 17, 30), flujo (25, 47) y quizá periodo (208; especulativo).
  4. La pareja UR266–UR275 no necesita la lectura créditos/débitos. Ambas copian los mismos registros brutos del mismo flujo, uno en versión resumida (UR266) y otro con el desglose de deducciones y neto (UR275).
  5. La hipótesis de "un producto por montón" se complica. UR269, bajo maní, consolida registros cuyos componentes (UR267A/B) estaban bajo ají en otra sala.
- **Urton y Chu 2015** (`docs/fichas/2015-Urton_inkawasi.md`): solo tenemos el resumen. Habla de "dos conjuntos de muestras emparejadas y atadas" y de unidades contables estandarizadas (las cuadrículas).
- **Clindaniel 2019** (ficha): lectura W/AB/AB:MB = suma/resta/resultado en UR267A y UR255, como prueba de concepto. Aquí se confirma que "blanco = bruto" es general (§2.7), pero no que "jaspeado = resultado".
- `QuipuYTocapu.txt` no menciona Inkawasi. Solo habla en general de las colcas y de los quipucamayoc de depósito (Astuhuamán, Caxas).

## 4. Diagrama del flujo de cifras

```
                              NIVEL 0: UNIDADES (9 por registro; cada una con parte B y parte A)
  UR270  (bajo maní, U.E.13)   grupo = registro;  9 colgantes W = parte B  +  9 subsidiarias NB = parte A
     │                      │                                   │
     │ columna a columna    │ Σ colgantes (P)                   │ Σ subsidiarias s1 (S)
     │ P_j + S_j            ▼                                   ▼
     │              NIVEL 1: COMPONENTES (por registro)
     │              UR273B ══copia══ UR274B    cuota 17      UR273A ══copia/complemento══ UR274A   cuota 30
     │              (cabecera B; 17 explícito en 274B)        (cabecera A; 30 explícito en 274A)
     ▼                      │  B_i                                   │  A_i
  UR278 (U.E.16)            └───────────────┬───────────────────────┘
  33 filas × 9 columnas                     │  A_i + B_i     (cuota 30 + 17 = 47)
  celda = B + A de la unidad                ▼
     │ Σ fila           NIVEL 2: LIBRO DEL FLUJO "47"   (bruto x  −  47  −  partidas  =  neto)
     └───────────────▶ UR266 (U.E.12; resumido) ══copia══ UR275 (U.E.19; con partidas y neto jaspeado)
                        filas 0-19 desde UR278, filas 16-24 desde A+B; misma secuencia de registros
                                            │ (registros 9-22 del flujo)
                                            ▼
  UR267A (ají, U.A.07) cuota 15 ══copia══ UR255 (corredor; atado a UR256)
       +                                     A_i + B_i (cuota 15 + 10 = 25)
  UR267B (ají, U.A.07) cuota 10 ══copia══ UR256 (corredor)        │
                                                                   ▼
                        NIVEL 3: LIBRO MAESTRO UR269 (maní, U.E.11)
                        bloques de 5 filas = periodos;  fila 1 = flujo "47" (UR273/274)
                        filas 2-4 = flujos con cuota 46, 46, 44 (fuentes NO conservadas)
                        fila 5 = flujo "25" (UR267A/B)
                                            │  ¿Σ bloque? (47+46+46+44+25 = 208)   [especulativo]
                                            ▼
                        NIVEL 4?: UR268 (maní, U.E.18), cuota 208, cabeceras 7 135-15 039
  Sin enlace: UR257 (cifras de decenas de miles), UR262-265, UR271, UR272, UR276, UR277, UR279, UR280, JC001-JC023
```

Rutas de verificación: el bruto de un registro del flujo 47 se alcanza (i) por columnas (UR270 → UR278 → UR266/UR275) y (ii) por componentes (UR270 → UR273A/B → suma → UR266/UR275/UR269). Además, cada componente y cada libro existen por duplicado, con su copia (255/267A, 256/267B, 273A/274A, 273B/274B y 266/275), y en cada copia la cuota se coloca en otra posición (09).

## 5. Traducción en prosa

> En Inkawasi, los quipucamayoc del depósito llevaban **registros sucesivos** de lo que entraba [apoyado: series ordenadas que se repiten en el mismo orden en 6 quipus]. Cada registro de un flujo se tomaba en **9 subunidades** fijas, cuyo tamaño relativo se mantenía de un registro a otro (las dos primeras siempre mayores, la 8.ª y la 9.ª menores) [bien apoyado como estructura: UR278 y UR270; qué eran es especulativo: ¿9 depósitos, 9 cuadrillas, 9 cargas?]. En cada subunidad se separaban **dos partes, A y B**, una pequeña (~25 %) y otra grande (~75 %) [bien apoyado: colgante B y subsidiaria A en UR270; su naturaleza, especulativa: ¿dos procedencias o dos mitades?].
>
> Las partes se asentaban en dos quipus distintos y **cada parte pagaba su propia cuota fija por registro**: 30 la parte A y 17 la parte B en el flujo que aquí llamo "47"; 15 y 10 en el flujo "25" [bien apoyado: cuotas constantes por quipu; 09 ya descartó que fueran proporcionales]. De cada quipu de componente se hacía **una copia**, con la cuota en otra posición del registro [bien apoyado], que a veces completaba lo que faltaba en el original (UR274A rellena UR273A) [apoyado].
>
> Después se **sumaban las dos partes** y se pasaban a un libro del flujo con la cuota también sumada (30 + 17 = 47; 15 + 10 = 25) [bien apoyado]. El total de cada registro se obtenía también sumando sus 9 subunidades, y ambas vías daban la misma cifra [bien apoyado en los registros conservados]. El libro del flujo se llevaba por duplicado. Una versión abreviada (UR266) asentaba el bruto y la cuota 47. Otra (UR275) asentaba el bruto, la cuota, varias partidas variables y el **resto**, que a menudo va en jaspeado [bien apoyado: aritmética; apoyado: color]. Cuando dos vías no coincidían, la diferencia quedaba anotada en una subsidiaria (2114 = 2020 + 94) [propuesto, un caso].
>
> Por último, un **libro maestro (UR269)** reunía por periodos (bloques de 5 filas) un registro de cada uno de cinco flujos, con sus cuotas: 47, 46, 46, 44 y 25 [apoyado: posición en el bloque, p ≈ 10⁻⁵–10⁻⁶; los flujos 46, 46 y 44 se infieren de sus cuotas y sus quipus no se conservan]. Quizá un quipu aún mayor (UR268, cuota 208 = 47 + 46 + 46 + 44 + 25) totalizaba cada periodo [especulativo].
>
> La cuota fija sería lo apartado por registro para el sostén del depósito y su personal [propuesto, lectura de Urton; nada en las cifras distingue tasa, ración o merma]. Que el flujo "47" sea maní y el "25" ají [especulativo]: los quipus aparecieron bajo esos productos, pero el libro maestro (bajo maní) mezcla ambos flujos.

## 6. Resultados negativos

- Sector B (JC001–JC023): ningún enlace, ninguna cuota y ningún total compartido.
- UR257, UR262–265, UR271, UR272, UR276, UR277, UR279 y UR280 no se enlazan con el sistema; la búsqueda exhaustiva de §2.8 solo deja un candidato débil, UR260 → UR270.
- Ningún total de UR266, UR269, UR275 o UR268 aparece en otro quipu: no hay un nivel superior conservado.
- Columnas gemelas en UR278: negativo.
- UR255 + UR256 y UR274A + UR274B registro a registro: no se alinean (otra disposición de grupos).
- La suma S de UR270 sola no aparece en UR273A/UR274A más de lo esperado (la parte A se recupera solo en la prueba conjunta por fila).
- UR269 → UR268: sin coincidencias exactas.
- El neto jaspeado no es una regla general.
- La numerología de las cuotas, sin la estructura, es débil (p = 0,01–0,04).
- Artefactos descartados: números redondos con tolerancia ±1 dígito (JC007–UR268, UR271–UR274B, UR269–UR274B) y el par UR257–UR278 (un solo valor).

## 7. Niveles de evidencia

- **Bien apoyado:**
  - A + B = consolidado (UR273A+B, UR274A+UR273B; UR267A+B en las filas con cuota 25 de UR269).
  - Cuota consolidada = suma de cuotas (47 = 30 + 17; 25 = 15 + 10).
  - UR270 P = B y S = A en la misma fila.
  - Celdas de UR278 = colgante + subsidiaria de UR270.
  - UR278 → UR266/UR275 en orden (04).
  - Cinco parejas de copia (dos nuevas).
  - Cuotas 17 y 208 por la aritmética.
  - Cabecera blanca.
  - Efectos de fila y columna en UR278.
- **Apoyado con datos:** UR269 en bloques de 5 flujos (posiciones), UR274A como complemento de UR273A, filas de UR278 = registros sucesivos del flujo 47, jaspeado del neto en UR275.
- **Propuesto:** cuota = deducción para el depósito (Urton), doble vía columnas/componentes como control, subsidiaria de UR266 como diferencia de conciliación, existencia de 3 flujos más (cuotas 46, 46 y 44) cuyos quipus se perdieron o no se registraron (Urton estudió 29 de 34).
- **Especulativo:** UR268 = nivel de periodo (208); identidad de las 9 columnas y de las partes A/B; flujo 47 = maní y flujo 25 = ají.

## 8. Siguiente ronda

1. **Predicción comprobable.** Si existen los quipus de los flujos con cuota 46, 46 y 44, serán parejas A/B cuyas cuotas sumen 46 o 44, y sus sumas darán las filas 2–4 de los bloques de UR269. Hay que buscarlos entre los 5 quipus de Inkawasi que Urton no estudió y en las fotos o registros de campo de Chu.
2. Revisar en el objeto las discrepancias de una cifra: UR278 g12 2533 frente a 2633, g27 246 frente a 290, y UR270 g9 s1 frente a UR278 g28. Así se distingue un error de lectura de un ajuste del quipucamayoc.
3. Reconstruir el primer tramo del flujo 47 (filas 0–10 de UR278): ¿existía un UR270 "anterior"?
4. Probar UR268 = Σ bloques de UR269 con una definición de bloque independiente de los separadores rosas (p. ej., por las cuotas 47…25).
5. Explicar las subsidiarias 0G/0B de UR266 (1070, 473, 1151...) a partir de las partidas de UR275 y de las columnas de UR278.
