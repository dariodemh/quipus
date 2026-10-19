# Incahuasi (Inkawasi): tríos `[x, c, x−c]`, pares atados y lectura contable

Carpeta: `analisis/09_incahuasi/`. Todos los scripts son reproducibles (semillas fijas) y leen `analisis/datos/*.csv`. Convenciones del brief: la unidad es el quipu; valor 0 sin nudos = cuerda ausente; BH-FDR o Holm indicados; con B = 2000 permutaciones el p mínimo es 1/2001 (q mínimo BH ≈ 0,02), así que "q = 0,024" significa "ninguna permutación igualó lo observado".

## 0. Resumen

1. **Demostrado.** La regularidad "primera cuerda del grupo = constante c + resto" es específica de 8 quipus de Incahuasi del Sector A (UR255, 256, 266, 267A, 267B, 269, 274B, 275). En el resto del corpus (643 quipus) no aparece ningún trío no trivial con constante (los "hallazgos" fuera de Incahuasi son rachas de 10/100/200 repetidos o un trío solapado contado 3 veces). Los 23 quipus JC (Sector B) no la muestran.
2. **Demostrado.** `c` es una constante por quipu (15, 15, 10, 10, 47, 47) y no depende de `x`; en UR269 depende de la **fila** dentro de bloques de 5 (47, 46, 46, 44, 25; R² = 0,39, p = 0,0015), no del valor de `x` dentro de la fila.
3. **Demostrado (búsqueda ciega en 21 321 pares del corpus).** Existen **tres** parejas de quipus que comparten `x`: UR255–UR267A, UR256–UR267B y **UR266–UR275** (esta última no figura en la ficha de Urton y Chu, que solo habla de "dos conjuntos"; no he podido comprobar el texto completo). Alineación cuerda a cuerda: 24, 21 y 25 valores idénticos frente a 5,8, 5,6 y 3,9 esperados (p ≈ 0,003, el mínimo posible).
4. **Apoyado con datos.** En cada pareja el orden de `c` y `n = x−c` está invertido (UR267A/UR267B: `[x, c, n]`; UR255/UR256: `[x, n, c]`; UR275 `[x, c, …, n]`) y la unión R/V también (3/3 parejas opuestas; con p = 0,5 por pareja esto es descriptivo, p ≈ 0,13).
5. **Apoyado con datos.** El color distingue a `x` (blanco W en UR267A 15/15, UR267B 11/13, UR269 14/15, UR275 6/7; Holm p < 0,05 en 3 quipus), pero **no** distingue `c` de `n` (Holm p ≥ 0,35). No hay una terna de colores bruto/deducción/neto general; UR255 y UR256 son casi monocromos (AB). Las cuerdas jaspeadas (`:`) están sobrerrepresentadas al final del registro en UR267A, 267B, 269, 275 y 255.
6. **Interpretación.** Sobreviven solo las lecturas de "deducción fija por registro" (tara, cuota, ración para el depósito). Quedan descartadas con datos: proporcional (diezmo, merma %), saldo encadenado y salida variable. Con estos datos **no se puede separar** tara de tributo de ración. Cualquier asignación a un producto es especulativa.

## 1. Lo que dice la literatura (verificado)

La ficha `2015-Urton_inkawasi.md` contiene solo el resumen de Urton y Chu (2015): no dice nada sobre el 15. La interpretación está en la tesis de Clindaniel (2019), que leí del PDF local (`papers/local_only`, pp. 66–67 y 91–96), citando Urton y Chu 2015:522:

- Hay "fixed values" repetidos en muchos quipus del Sector A (excavación 2013-14). Se interpretan como algo parecido a **impuestos sobre los bienes que entraban al depósito**: cantidad a apartar para el sostén de la instalación y su personal.
- UR267A, cuerdas 1–3: 106, 15, 91 = "106−15=91". UR255 es el quipu "emparejado" con las operaciones invertidas (cuerdas 67–69: 70, 55, 15; "70−55=15", el valor fijo es el resultado). Se propone que sirvió para verificar los cálculos de UR267A.
- Clindaniel (prueba de concepto): en UR267A W = suma/crédito, AB = resta/débito, AB:MB (jaspeado) = resultado; en UR255 AB = suma, MB = resta, AB:MB = resultado. Los colores solo se usarían para establecer la secuencia ("efecto de inclusión"). Él mismo dice no haber hallado otros quipus con ese sistema.
- Productos: ají, maní y frijol negro hallados con los quipus (asociación de contexto, **propuesta**). El maíz que menciona el encargo no aparece en el resumen que tengo. Los datos de contexto de excavación no están en el OKR (`estado_del_arte.md` §2.5), así que **ningún quipu puede asignarse a un producto con estos datos**.

## 2. Tarea 1: reconstrucción de tríos (`01_trios.py`, `01b_otros.py`, `04_cierre_primera.py`, `08_tabla_incahuasi.py`)

**Definición.** Ventana = 3 cuerdas de nivel 0 presentes (valor > 0) consecutivas dentro de un grupo. Patrones por posición de la suma: S1 (`[x, c, x−c]` y `[x, x−c, c]`), S2 (`[c, x, x−c]`), S3 (`[c, x−c, x]`). Tolerancia 0 y ±1. "No trivial" = partes distintas, parte menor ≥ 5, suma ≥ 30 (descarta `[20,10,10]`).

**Nulos** (por quipu, B = 2000, semilla 1000+i). N1: barajar los valores presentes del quipu entre posiciones (conserva grupos y la repetición de c). N2 (el más estricto): en quipus con ≥ 4 grupos de exactamente 3 cuerdas, barajar **cada columna** entre grupos: conserva los marginales de x, c y x−c y rompe solo el emparejamiento por fila.

**Resultados en 651 quipus** (`trios_por_quipu.csv`, `salida_01_trios.txt`):

| Prueba | testables | p<0,05 (esp.) | q<0,05 | quipus con q<0,05 |
|---|---|---|---|---|
| tol 0, N1 | 483 | 47 (24) | 12 | 9 Incahuasi (JC010, UR255, 256, 260, 267A, 267B, 269, 270, 275) + MM001, UR113, UR230 |
| tol 0, N2 columnas | 48 | 8 (2,4) | 6 | **UR255, 256, 267A, 267B, 269, 275** |
| tol 1, N1 | 505 | 78 (25) | 37 | 11 Incahuasi y 26 de otras procedencias (efecto de valores pequeños) |
| tol 1, N2 | 54 | 12 (2,7) | 6 | los mismos 6 |

Tras el filtro "no trivial" (`trios_no_triviales.csv`) solo quedan los 6 con ≥ 7 aciertos; fuera de Incahuasi el máximo es 3 (AS036, UR218, UR1136, UR049) y ninguno tiene q < 0,05. Explicaciones aburridas verificadas: MM001 son rachas de `10 10 10` (24 de 26 aciertos usan c = 10 con partes iguales); UR113 y UR260, valores de 1–2; UR270, rachas de 100/200; UR218, un único trío (22, 36, 14) contado 3 veces por solapamiento de ventanas.

**Generalización** (`04_cierre_primera.py`): grupo "cierra" si su primera cuerda presente = suma del resto de cuerdas de nivel 0 (≥ 3 presentes). Con tol 0: 9 quipus con q<0,05, **8 son Incahuasi** (UR255 9 grupos, 256 7, 266 2, 267A 15, 267B 12, 269 15, 274B 2, 275 10) y uno es UR1152 (Ica). Con tol 1–2 aparecen además AS207C, HP011, UR188, UR004, UR1057 (excesos pequeños, no examinados). UR275 y UR266 muestran que el trío es un caso mínimo del registro general `x = c + deducciones + neto`: en UR275, 3317 = 47 + 114 + 498 + 370 + 2287 + 1 (cierre con tolerancia 1).

**Corrección a lo heredado.** "15 de 15 grupos" no es exacto. UR267A tiene 29 grupos (26 registros) y 15 cierran exactamente. UR255 cierra 9–10 de 24 registros. UR256 cierra 7 de 23 y UR267B 12–13 de 26. Lo que sí es casi universal es la presencia de `c`: aparece en 23/24 registros de UR255, 25/26 de UR267A, 20/22 de UR256, 25/25 de UR267B, 22/27 de UR266 y 24/25 de UR275. Tampoco es cierto que `c` sea constante en UR266/269/275 ("46–47"): en UR275 y UR266 es 47 (con 40 y 44 aislados); en UR269 varía por fila (§5).

**Tabla por quipu** (tríos exactos no triviales; `tabla_por_quipu.csv`, `tabla_incahuasi.csv` para los 52):

| Quipu | tríos | c (frecuencia) | x (lista) |
|---|---|---|---|
| UR255 | 10 | 15 (10) | 34, 66, 70, 110, 124, 127, 141, 148, 187, 201 |
| UR256 | 7 | 10 (7) | 153, 329, 357, 394, 518, 535, 603 |
| UR267A | 15 | 15 (15) | 34, 44, 70, 106, 110, 124, 127, 141, 149, 157, 187, 201, 206, 215, 238 |
| UR267B | 13 | 10 (13) | 121, 284, 321, 328, 329, 394, 518, 535, 543, 601, 603, 613, 660 |
| UR269 | 15 | 46 (7), 47 (4), 25 (2), 44, 20 | 270, 522, 662, 1130, 1505, 1665, 1827, 2214, 2236, 2362, 2399, 2518, 2561, 2675, 2797 |
| UR275 | 7 | 47 (7) | 1505, 1653, 1737, 1780, 1891, 1907, 2247 |
| UR266 | 1 (+ registros con ítems) | 47 | 1765 (los demás tienen cuerdas intermedias; ver pareja con UR275) |
| UR274B | 2 | 17 | 1300, 1402 |

Otros 44 quipus de Incahuasi: 0 tríos no triviales con constante (UR262: 3 con c distintas; JC010, JC013, UR268, UR270, UR273B, UR274A: 1–2 aciertos aislados, no significativos tras BH).

Variantes: en estos quipus S2 y S3 no aparecen tras el filtro. Todo es S1, con `c` en posición 2 (UR267A 14/15, UR267B 12/13, UR275 7/7) o en posición 3 (UR255 8/10, UR256 7/7, UR269 14/15). La tolerancia ±1 añade casos (UR269 18, UR267B 14) sin cambiar nada.

## 3. Tarea 2: qué distingue a x, c y n (`02_roles.py`, `02b_roles_cn.py`)

Roles por valor: x = cuerda suma, c = parte menor, n = parte mayor. Nulo: permutar los roles **dentro de cada trío** (conserva las tres cuerdas; B = 5000). Holm sobre 54 pruebas (`roles_pruebas.csv`) y 12 contrastes de color (`roles_color_contrastes.csv`).

| Atributo | Resultado |
|---|---|
| Unión R/V | **Constante dentro del quipu** (no distingue roles). Cambia entre quipus: UR255 R, UR267A V, UR256 V, UR267B R, UR266 V, UR275 R (90 % R), UR269 V. Las 3 parejas son opuestas. En las otras 2 parejas significativas del corpus con unión uniforme (KH0049–UR122, UR1104–UR234) son iguales (V–V). |
| Torsión | S en todo (constante). |
| Color: x vs {c,n} | W en UR267A (15/15), UR269 (14/15), UR275 (6/7): Holm p = 0,016; 0,002; 0,011. UR267B (11/13 W) no es distinguible porque c y n también son W. UR255/UR256: x = AB como todo. |
| Color: c vs n | No distinguible (Holm 0,35–1). Por quipu: UR267A c = W (11) o AB (4), n = AB (9), W (4), AB:MB (2). UR269 c = MB/NB/AB, n = NB (11/15). UR275 c = NB y n = NB. UR255/256 todo AB. |
| ¿c siempre del mismo color? | Dentro de cada quipu casi (UR267B 13/13 W, UR255 10/10 AB, UR256 7/7 AB, UR275 7/7 NB), no en UR267A ni UR269, y **no entre quipus** (W, AB, NB, MB). |
| Tipo y dirección de nudos | Los p crudos son pequeños pero son una consecuencia mecánica del valor (15 = 1 simple de decenas + 5 largos; x lleva centenas). Sin información independiente. Dirección: simples Z y largos S en UR267A/269/275; Z en todo UR255 (esquema de Clindaniel). Es constante por quipu. |
| Largo | Sin diferencias robustas (x más largo en UR267A, p crudo 0,014; Holm 0,38). |
| Jaspeadas (`:`) | Al final del registro (grupos ≥ 3 cuerdas): UR267A 7/23 (esp. 2,1; p < 0,001), UR267B 6/25 (1,9; p = 0,002), UR269 8/41 (2,2; p < 0,001), UR275 16/25 (4,2; p < 0,001), UR255 2/13 (0,4; p = 0,04). Cero en UR256/UR266. Compatible con "jaspeado = resultado" de Clindaniel, pero en UR267A 16 de 23 finales no son jaspeados: los colores marcan el resultado al inicio y luego dejan de hacerlo. |

Conclusión: **no existe** una terna fija color-bruto/deducción/neto. Lo robusto es solo "el bruto es la cuerda blanca" en 4 de 6 quipus, y jaspeado al final en 5. La lectura W/AB/AB:MB de Clindaniel es válida para el inicio de UR267A y no se generaliza (**propuesto**).

## 4. Tarea 3: relaciones entre quipus (`03_pares.py`, `06_pares_detalle.py`, `09_ur255_blancos.py`)

**Búsqueda ciega** (`pares_corpus.csv`): para cada par de quipus con ≥ 8 valores distintos ≥ 50, los valores comunes frente a lo esperado por independencia (frecuencias del corpus; cola de Poisson; Bonferroni sobre 21 321 pares). De 3313 pares con ≥ 5 valores comunes, 8 pasan Bonferroni. De ellos **tres son Incahuasi**: UR256–UR267B (29 comunes, esp. 8,4, p_bonf = 0,0004), UR255–UR267A (22; esp. 5,2; 0,0009) y **UR266–UR275** (26; esp. 7,6; 0,003). Los otros pasan por Pachacamac (AS125–UR247, UR1118–UR218, UR1104–UR234) y KH0049–UR122 (Costa Sur/Nazca): fuera de este encargo. Ningún otro quipu de Incahuasi se empareja con UR269.

**Alineación cuerda a cuerda** (programación dinámica; `alineacion_pares.csv`; nulo: barajar la secuencia B y realinear, 300 réplicas, el p mínimo es 0,0033):

| Pareja | c | alineados idénticos (no c) | nulo media / máx | ±1 | otros ≤ 15 | > 15 |
|---|---|---|---|---|---|---|
| UR255–UR267A | 15 | 24 (22 ≥ 30) | 5,8 / 11 | 2 | 4 | 1 |
| UR256–UR267B | 10 | 21 (20 ≥ 30) | 5,6 / 12 | 1 | 1 | 26 |
| UR266–UR275 | 47 | 25 | 3,9 / 8 | 1 | 1 | 21 |

Qué dicen:

- **UR255–UR267A** (la mejor): los mismos 22 `x` en el mismo orden (106, 206, 238, 85, 160, 114, 141, 187, 95, 215, 157, …). Diferencias: 161/160, 134/133, 16/15 (±1) y 112/100, 92/82, 66/77, 51/63, 25/44 (5 discrepancias de 5–19). UR267A trae el neto en 23/26 registros y UR255 solo en 10/23 (ver abajo). Las cuerdas de UR267A se agrupan igual que las de UR255 salvo que UR255 intercala una cuerda sin nudos (de largo normal, mediana 35 cm; 17 de 24 miden ≥ 20 cm) donde UR267A tiene el neto.
- **Orden espejo.** UR255 (c, n) = `[x, n, c]`, UR267A `[x, c, n]`; igual UR256 vs UR267B. Las parejas se distinguen por el orden y la unión R/V opuesta. Consistente con "emparejado con operaciones invertidas" de Urton y Chu (cálculo de verificación); **no** demuestra el sentido de la inversión.
- **UR255 deja el neto en blanco en la primera mitad.** Registros con x y c: grupos < 16: neto presente en 2 de 13; grupos ≥ 16: 10 de 10 (Fisher p = 7·10⁻⁵; UR267A 11/13 vs 11/12, p = 1). **El corte en el grupo 16 se eligió mirando los datos** (exploratorio; el p está inflado). El 0 de 10 vs 11 de 13 es nítido. Las cuerdas en blanco son cuerdas completas sin nudos, no muñones.
- **UR256–UR267B:** coinciden `x` y `c` (14–20 registros), pero las cuerdas de detalle difieren mucho (26 alineamientos con diferencia > 15). Aparecen desplazamientos de c: UR256 623 vs UR267B 613 y 270 vs 260 (diferencia = c), y en el registro 601 se ve `601 = 580 + 10 + 11` (UR256) frente a `601 = 10 + 591` y `591 = 580 + 11` (UR267B): la misma cuenta con dos cortes distintos del mismo cálculo (descomposición `x = c + d + n`, con una segunda deducción variable d = 11).
- **UR266–UR275:** mismas x (3317, 2089, 1842, 1876, 3249, 2229, 3320, 4273, 2633, 3096, 2950, 2275, 1278, …) y mismo c = 47. UR275 añade partidas y la cuerda neta jaspeada final (W:MB): 1842 = 47 + 342 + 11 + 1442.
- **Prueba de complementariedad** (`06_pares_detalle.py`, `pares_descomposicion.csv`): ¿se resuelve `x = c + subconjunto (≤ 3 cuerdas)` solo al unir los dos quipus? Resultado **negativo/débil**: UR255–UR267A 0 de 22 (nulo 0,04), UR256–UR267B 2 de 20 (nulo 1,6; p = 0,46), UR266–UR275 2 de 25 (nulo 0,2; p = 0,02). No demuestro "detalle vs resumen" ni "copias" más allá de la igualdad de `x`.
- `x` de un quipu en otros quipus de Incahuasi fuera de las tres parejas: no hay (la búsqueda ciega no encuentra más).

## 5. Tarea 4: hipótesis, predicciones y comprobación (`05_hipotesis.py`, `salida_10_cobertura_c.txt`)

| Hipótesis | Predicción distinta | Comprobación | Veredicto |
|---|---|---|---|
| **A. Tara/cuota fija por registro** (bruto − tara = neto; tributo fijo; ración para el depósito) | c constante dentro del quipu; c/x decrece con x; neto siempre positivo | CV(c) = 0 en UR255, 256, 267A, 267B, 275. c/x: UR267A 6–44 %; UR267B 1,5–8 %; UR275 2–3 % | **Compatible** (demostrado que c es fija) |
| **B. Proporcional** (diezmo 10 %, merma %, impuesto ad valorem) | c ∝ x; c/x constante | c/x varía de 6 % a 44 % en UR267A (con 10 % tendríamos c de 3 a 24). Si c = round(r·x) la SD de c sería 8,5 (UR255), 4,7 (256), 9,1 (267A), 4,5 (267B), 6,3 (275); observada **0**. UR269 dentro de fila: SD de c predicha 9,1/4,6/3,4/12,1/26,5, observada 2,9/3,4/2,4/6,7/11,7; Spearman c–x intrafila 0,11 (p = 0,24) | **Descartada** (demostrado en 5 quipus). Tampoco el diezmo (1/10 ya negativo en `01_aritmetica`). |
| **C. Entrada–salida–saldo encadenado** (el saldo de un registro es la entrada del siguiente) | n_i reaparece como x_(i+1) | 0 encadenamientos adyacentes en los 6 quipus (nulo ≈ 0); 0 n reaparecen como x en el mismo quipu (1 en UR267B) | **Descartada** (en forma de saldo arrastrado) |
| **D. Salida variable** (cada registro con su propia salida) | c variaría libremente | c idéntica en 5 quipus; solo UR269 varía | **Descartada** para 5; UR269 ver E |
| **E. Deducción por categoría** (tara/cuota según tipo de producto o de contenedor) | c fija por categoría y quipu distinto = categoría distinta | UR269, bloques de 5 filas separadas por cuerdas sin valor: c = 47, 46, 46, 44, 25; R² de c explicado por fila = 0,39 frente a 0,09 del nulo (barajar c entre registros, B = 10 000), p = 0,0015. c distinta entre parejas (15, 10, 47) | **Apoyado con datos** (UR269 y entre quipus); la correspondencia con productos es especulativa |
| **F. Saldo negativo imposible** | x > c siempre | Cierto (x/c mínimo 2,07 en UR267A, 13 en UR269…), pero no discrimina: es lo que daría cualquier hipótesis con x grande | No informativo |
| **G. Dos deducciones** (c fija + otra variable) | registros `x = c + d + n` | UR256/267B: 601 = 580 + 10 + 11; UR275: 3317 = 47 + 114 + 498 + 370 + 2287; cierre por primera cuerda en 8 quipus con q<0,05 | **Apoyado con datos** |

Veredicto: lo que queda es "cada registro = cantidad recibida **x**, menos una deducción fija **c** (constante por quipu o por categoría), menos eventuales partidas variables, igual al resto **n**". Esto cuadra con la lectura de Urton y Chu (c = valor fijo restado) y con la verificación cruzada en parejas. **No** distingue tara de tributo de ración de depósito: los tres predicen lo mismo en estos datos. La "tasa de 15" no tiene aquí ningún comportamiento especial: 15 es solo el valor de c en la pareja UR255/UR267A (10 en la otra, 47 en la tercera). La pareja con los x pequeños (34–238) tiene la c relativamente más grande. La escala de c no es proporcional a la de x entre parejas (c/x típica aprox.: 14 %, 3 %, 2 %). Con un producto por quipu no puedo compararlo con "cacahuete, ají, frijol" porque no hay asignación quipu-producto en los datos.

Otros hechos del archivo: los registros por quipu son ~24–26 en las tres parejas (23, 24, 24, 25, 25, 26); UR267A agrupa los registros en 4 bloques de 3, 6, 10 y 7 separados por 3 cordones rosa (PK) sin nudos.

## 6. Tarea 5: lectura de UR267A, registro a registro (`07_traduccion_UR267A.py`)

Notación: x (color) / c (color) / n (color). **[D]** = demostrado por la aritmética; **[S]** = supuesto interpretativo.

> *«UR267A es una lista de 26 registros, en 4 bloques (3, 6, 10 y 7 registros) separados por tres cordones rosa sin nudos [D]. Cada registro abre con una cuerda blanca que lleva una cantidad (el bruto), sigue casi siempre una cuerda con el valor 15 y termina con una cuerda que lleva la diferencia [D en 15 registros; en el resto, ver abajo]. [S] Leído como un almacén: llegó 106 (W); se apartó la cuota fija de 15 (AB); quedan 91 (AB:MB, jaspeado = resultado) [Clindaniel, propuesto]. [S] Lo que se aparta (15) sería lo destinado al sostén del depósito y su personal [Urton y Chu, propuesto].»*

Registros (colores en el orden x / c / n; `∅` = cuerda sin nudos o ausente):

| Grupo | x / c / n | Estado | Contraparte en UR255 |
|---|---|---|---|
| 0 | 106 W / 15 AB / 91 AB:MB | cierra [D] | mismo registro (x=106, 15; neto en blanco) |
| 1 | 112 W / 15 W / ∅ AB:MB (muñón de 1,5 cm) | sin neto (esperado 97) | no hallada |
| 2 | 161 W / 15 W / 140 AB:MB | no cierra (Δ = 6; UR255 trae 160) | 160 |
| — | (rosa) | separador | |
| 4 | 206 / 15 / 191 AB:MB | cierra | mismo x |
| 5 | 238 / 15 / 223 W | cierra | mismo x |
| 6 | 85 / 15 / ∅ AB:MB (muñón de 4,5 cm) | sin neto (esperado 70) | mismo x |
| 7 | 160 / 15 / 239 AB:MB | no cierra (Δ = −94; 239 ≈ 238+1) | mismo x |
| 8 | 114 / 15 / 84 AB:MB | no cierra (84 = 114 − 2·15) | mismo x |
| 9 | 141 W / **16** AB / 120 AB:MB | no cierra (Δ = 5; c = 16) | 141 |
| — | (rosa) | separador | |
| 11 | 187 / 15 / 80 AB:MB | no cierra (80 = 95 − 15 es el neto del registro 12) | 187 |
| 12 | 95 / 15 / 17 AB (+ subsidiaria 50) | no cierra | 95 |
| 13 | 215 / 15 / 200 AB | cierra | mismo x |
| 14 | 157 / 15 AB / 142 AB | cierra | mismo x |
| 15 | 187 / 15 / 172 AB | cierra (UR255 también: 172 jaspeado) | 187, 172 |
| 16 | 141 / 15 / 126 | cierra | UR255: [141, 126, 15] |
| 17 | 127 / 15 / 112 | cierra | UR255: [127, 112, 15] |
| 18 | 110 / 15 / 95 | cierra | UR255: [110, 95, 15] |
| 19 | 149 / 15 / 134 | cierra | UR255: [148, 133, 15] (±1) |
| 20 | 201 / 15 / 186 | cierra | UR255: [201, 186, 15] |
| — | (rosa) | separador | |
| 22 | 70 W / 15 W / 55 W | cierra (UR255: 70, 55, 15 = el caso de Clindaniel) | [70, 55, 15] |
| 23 | 82 / 15 / 77 | no cierra (Δ = −10; ¿67?) | 92 / 15 (neto ∅) |
| 24 | 63 W / 15 AB / 40 AB | no cierra (Δ = 8) | [66, 51, 15] |
| 25 | 34 / 15 AB / 19 W | cierra | [34, ∅, 15, 19] |
| 26 | 44 / 15 / 29 | cierra | (UR255: 25, 10, 29, 14) |
| 27 | 124 W / 109 AB / 15 AB | cierra, con 15 en tercer lugar | [124, 109, 15] |
| 28 | 31 W / 15 AB / ∅ | sin neto (esperado 16) | no hallada |

Balance: 15 registros cierran exactamente [D]; 3 no tienen cuerda neta; 8 no cierran. Entre los 8, 5 parecen errores de un dígito o de agrupación (grupos 2, 9, 11, 23, 24) y 1 admite una lectura aritmética distinta (84 = 114 − 2·15) [S]. No distingo errores de lectura del KFG de otras reglas de cálculo. El registro 27 invierte el orden (c en tercer lugar), como lo hace siempre UR255. Qué es **supuesto**: que x sea "lo entregado" y no un total ya mezclado, que 15 sea una tasa y no una unidad, el sentido de los colores y la lectura como depósito.

## 7. Resultados negativos

- Sin tríos no triviales con constante fuera de Incahuasi; ninguno en los 23 quipus JC.
- Sin código de color bruto/deducción/neto general; c y n no se distinguen por color, largo, torsión ni nudos.
- Sin encadenamiento de saldos; sin proporcionalidad; el 10 % de diezmo no se sostiene.
- La unión R/V opuesta en 3/3 parejas no es significativa (p ≈ 0,125 con p = 0,5 por pareja).
- La complementariedad "A ∪ B resuelve lo que A y B no resuelven" no se sostiene salvo UR266–UR275 (p = 0,02, sin corrección).
- Las variantes S2 y S3 no se presentan en Incahuasi más allá de lo trivial.

## 8. Niveles de evidencia

- **Demostrado:** el patrón `primera cuerda = c + resto` en 8 quipus del Sector A, y solo ahí (frente a N1/N2, 651 quipus); c constante por quipu; c no proporcional a x; tres parejas de quipus con x comunes; UR267A: 15 registros cierran.
- **Apoyado con datos:** c por categoría de fila en UR269; orden y unión invertidos en las parejas; x = cuerda blanca en 3-4 quipus; jaspeado al final del registro; UR255 con el neto en blanco en la primera mitad (corte post hoc); registros `x = c + d + n` en UR256/267B/275.
- **Propuesto:** c = tara/cuota/ración del depósito; pares como verificación cruzada; "jaspeado = resultado".
- **Especulativo:** ligar un valor de c a un producto concreto; cualquier lectura de x como cantidad de grano, ají, maní o frijol; la lectura de UR266–UR275 como pareja (nueva aquí, sin contrastar con la literatura).

## 9. Siguiente ronda

1. Revisar los 8 registros no cerrados de UR267A y los de UR255 con los xlsx originales y la ficha física (¿errores de lectura? ¿decalaje de grupos?).
2. Reconstruir el grafo completo de UR266–UR275 con subsidiarias (x = c + partidas + neto) y contrastarlo con UR269.
3. Contexto de excavación de Urton y Chu (posición de cada quipu respecto de los productos): sin él no se puede probar la hipótesis de producto.
4. Buscar el segundo emparejamiento posible de UR269 (¿en el material no incluido en el KFG?) y estudiar los bloques de 5 filas (¿5 categorías?).
5. Revisar los excesos de cierre con tol 1–2 en AS207C, HP011, UR188, UR004, UR1057, UR1152.

## Archivos

Scripts: `comun.py`, `01_trios.py`, `01b_otros.py`, `02_roles.py`, `02b_roles_cn.py`, `03_pares.py`, `04_cierre_primera.py`, `05_hipotesis.py`, `06_pares_detalle.py`, `07_traduccion_UR267A.py`, `08_tabla_incahuasi.py`, `09_ur255_blancos.py`. Salidas: `salida_*.txt`, `trios_por_quipu.csv`, `trios_detalle.csv`, `trios_no_triviales.csv`, `tabla_incahuasi.csv`, `tabla_por_quipu.csv`, `roles_*.csv`, `pares_corpus.csv`, `alineacion_*.csv`, `pares_descomposicion.csv`, `pares_union.csv`, `cierre_primera_por_quipu.csv`, `resultado_jaspeadas.csv`, `ur269_filas.csv`, `traduccion_UR267A.csv`.
