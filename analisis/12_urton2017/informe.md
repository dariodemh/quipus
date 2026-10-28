# 12 · Urton (2017), *Inka History in Knots*: lecturas concretas frente a los datos KFG

Rol: historiador andino y analista de datos. Entrada: texto plano del libro (`analisis/fuentes_txt/InkaHistoryinKnotsReadingKhipusas.txt`, capítulos 3-12, tablas y apéndices; el cap. 1-2 y 13 no traen lecturas de quipus concretos). Salida: `lecturas.csv` (23 lecturas, con museo, número KDB/KH, qué registraría, cifras citadas, documento colonial y seguridad que le da el propio Urton), scripts `a_…j_*.py` con su salida `.out`, y este informe. Semilla fija 12017 en todos los nulos.

## 0. Cómo leer los resultados (límite importante)

KFG y OKR provienen de la misma base de datos (KDB de Harvard) que Urton usó. Que una cifra coincida con KFG comprueba que el libro transcribe bien la base y que la estructura descrita está en la base. **No es una verificación independiente del objeto ni de la interpretación.** Lo que sí se puede poner a prueba es (a) si la estructura/aritmética citada existe, (b) si supera un nulo explícito, y (c) si la interpretación (calendario, censo, tributo) es distinguible de lo que daría el azar o una explicación aburrida. Cuando no hay nulo posible lo digo.

Vocabulario de veredictos: **confirmada** (cifras y estructura existen y superan el nulo), **compatible** (existen pero el dato no discrimina la interpretación frente al azar), **no reproducida** (la cifra o la estructura no aparece en KFG o no supera el nulo), **refutada** (KFG contradice la afirmación).

Correspondencia de IDs: UR## de Urton = `UR###` de KFG (p. ej. UR6 = UR006 = KH0242). Dos marcadores sin valor (M1, M2) del libro aparecen en KFG como colgantes p35 y p56 de UR028; hay que desplazar la numeración.

## 1. Hallazgo principal: UR006 sí reproduce la estructura de Urton (corrige SINTESIS)

SINTESIS (05) dice que UR006 «no reproduce el calendario» porque KFG da 571 colgantes (Urton: 762) y 24 grupos de 20-22. La causa es de lectura de datos: **KFG codifica los «loop pendants» como subsidiarias de la cuerda-lazo** (25 cuerdas sin largo con 8-9 subsidiarias cada una; 285 subs de nivel 1). Contando las subsidiarias de los lazos (`a_ur006.py`):

- 24 conjuntos regulares de 20-22 colgantes (grupos KFG 2, 5, 7, … 56) + 24 lazos de 8-9 (el 25.º lazo, p24, es el «top string»): **729 cuerdas por los 24 pares (Urton: 730)**; año 1 = 361 (362), año 2 = 368 (368); semestres 179, 182, 185, 183 (Urton 179, 183, 185, 183). Los 24 tamaños de par difieren de los de Urton en una sola cuerda (par 8: 30 vs 31).
- Valores (Tabla 4.3): las 48 sumas por par (colgantes/lazo) coinciden exactamente en **45 de 48** (año 1: 23/24; año 2: 22/24 con mi transcripción, ambigua, de la tabla en PDF). Las cuerdas fuera de los pares suman **80 = 31+23+26** (exacto). Total KFG 3 037 (Urton 3 042); año 1 hasta el par 12: 2 058 (2 059); año 2: 979 (983). La Tabla 4.4 completa (564 valores) coincide con KFG en 544 valores y en el orden (LCS 530/549 frente a 306 con orden permutado; `j_tabla44.py`).
- Nulo (permutar los valores de UR006 y recalcular las 48 sumas): 0,56 coincidencias esperadas, máximo 5 en 1 000 permutaciones; observadas 45.

Qué queda en pie y qué no del calendario: la **estructura** (24 pares casi regulares de ≈30 cuerdas, dos bloques de 12) es real y única en el corpus (ningún otro quipu tiene 24 pares 21+9; HP038, UR113 y KH0049 tienen lazos pero no esa regularidad). Pero la **lectura calendárica** no es discriminable: remuestreando los 24 tamaños de par con reemplazo, el total cae a ±1 de 730 en el 40 % de los casos (media 729,0); la media de par es 30,4, no 29,5 (mes sinódico); un solo par mide 29. «365» sale de promediar dos años de 362 y 368, un objetivo con holgura. Etiqueta: **estructura bien apoyada; calendario propuesto (compatible, no falsable con estos datos)**. La nota de 05 sobre calendario (ningún quipu con 328/354/360/365/730 colgantes) sigue siendo cierta para colgantes, pero UR006 contado con lazos da 729 cuerdas en los pares.

## 2. Resultados por lectura

### 2.1 Atarco: UR028, UR029, UR023 (caps. 3 y 10) — `b_atarco.py`, `i_censo.py`
- **UR028**: 74 colgantes y 15 subsidiarias (✓). Cuerda 1 = 102 = Σ(cuerdas 2-4 con sus subsidiarias: 29, 14, 13, 10, 12, 24) (✓ exacto). Secciones de 30/20/20 cuerdas separadas por M1 y M2 (✓). Sumas de los conjuntos de 5 cuerdas: pares (MB) 14, 10, 24 (= subsidiarias de 2-4, ✓ las tres); impares (AB) 25, 13, 14 frente a los 29, 13, 14 que cita Urton (✓ en 2 de 3; el conjunto 5-29 da 25: la cuerda 25 tiene un nudo de tipo desconocido valorado 0 en KFG, y Urton parece haberle dado 4). Total 5-74 = 100 (104 si se cuentan las 4 subsidiarias KB de valor 1 que Urton dice que valen 0). Reparto AB/MB de los colgantes 5-74: 52/48 (Urton 54/48).
- Nulo: permutando los 70 valores de los colgantes 5-74, 5 de las 6 sumas de conjunto de Urton se reproducen con media 0,32 aciertos y P(≥5) = 0 en 5 000; que 2-4 sumen 102 con sus subsidiarias: 0 de 20 000.
- Veredicto aritmética: **confirmada** (con una discrepancia de 4 en un conjunto). La interpretación (6 ayllus, 102 = una pachaca, AB = hanan encompassing hurin) **no se puede someter a nulo**: es **propuesta**. Es consistente con 08/10 («fila + cuerda total suelta»).
- **UR029**: 35 colgantes, todos con ≥1 subsidiaria (39 subs), 7 grupos de 5, primer colgante 7 (✓). Total KFG 125 (123); colgantes sin nudos [5, 21, 28, 35] (Urton añade el 6; KFG da 2 a p6, lo que explica la diferencia de 2). Solo 4 quipus de 441 tienen todos sus colgantes con subsidiaria (UR029, UR057, UR216, UR271).
- **Criterio «censo-like» (UR029, UR023 y 50-60 quipus)**: ≥90 % de los valores en 1-7 y más 1-4 que 5-7 lo cumplen 35 de 482 quipus con ≥15 cuerdas con valor (7 %), entre ellos UR023, UR029, AS017, AS169, UR003, UR1097. UR028 no lo cumple por la subsidiaria de valor alto (89 %). El chi-cuadrado de Brezine no es replicable (los exemplares solo están en figuras); con un exemplar aproximado (22/28/20/14/8/5/3 %) pasa p>0,05 el 32 % de 262 quipus: la prueba es poco selectiva con n pequeño. Veredicto UR029/UR023: **compatible** (el patrón numérico existe; no discrimina «censo» de «cualquier registro de cantidades pequeñas»). La lectura cuerda=tributario, subsidiaria=dependiente es **especulativa** (Urton la califica «highly speculative»).

### 2.2 UR006 y sus «fuentes» UR009, UR021 (cap. 4) — `a_ur006.py`
- **UR021 ↔ UR006 meses 13-16** (4 pares): subsecuencia común de valores ≥5 = 20 (mismo bloque) frente a 5-13 en los otros bloques; nulo (permutar UR021 y tomar el mejor bloque): media 13,0, p95 15, 0 de 300 igualaron o superaron. **Confirmada**.
- **UR009**: no discrimina un bloque (mejor bloque meses 12-15, LCS 13, p = 0,39 frente al máximo de permutaciones). Pero la subsecuencia **20-61-20 aparece solo en UR006, UR009 y UR021 de los 651 quipus**: relación real, aunque en UR009 el solape es un fragmento (~7 valores), no los 4 meses. **Compatible/parcial** (para UR009).
- **3 000 tributarios**: el total 3 037 (2 957 dentro de los pares) está a 1,2 % de 3 000; en quipus con totales de 1 500-6 000, el 6,7 % está a esa distancia de un múltiplo de 1 000. Urton construye «3 002» como promedio de 3 042 y 2 962 (los dos totales, con y sin 80 cuerdas), la cifra documental 3 000 es redondeada y no hay un segundo ancla. **Compatible, débil (post hoc)**.
- **Guaman**: no verificable; Urton mismo lo declara improbable. **Especulativo**.

### 2.3 UR011, ¿colapso demográfico? (cap. 11) — `c_ur011.py`
- Los 15 pares de la Tabla 11.2 coinciden **15/15** con KFG. Pares gemelos: mediana |ln razón| 0,11 frente a 0,80 si se permutan los 30 valores entre pares (0 de 10 000 ≤); coincide con 10 (columnas gemelas de UR011).
- Descenso: Spearman medias vs orden −0,81 (p = 3e-4), −78,8 % (Urton: 80 %). Pero no es «constante y precipitado»: es una **meseta de ~15 600 a ~8 900 (pares 1-9), un salto de −75 % entre los pares 9 y 10 y otra meseta de 1 460-3 300** (dos mesetas explican R² 0,87 en logaritmo; una recta, 0,69). La serie de tributarios de Schjellerup baja de 16 309 (1559) a 10 699 (1583): descenso gradual. El 3,8 % de los quipus con ≥12 grupos tiene rho ≤ −0,8 (6/158); cualquier serie monótona decreciente correlaciona alto con la curva de tributarios (mediana 0,93 con máximos de grupo ordenados de otros quipus), de modo que el ajuste no discrimina. **Estructura de pares: confirmada. Lectura «tributarios en caída 1570-1625»: compatible, no discriminada** (el escalón brusco es un dato en contra de la lectura de descenso paulatino).

### 2.4 Puruchuco (cap. 5) — `d_puruchuco.py`
- **UR068 → UR067 / UR066** (nivel II suma a nivel III): sumando las tres secciones de 20 cuerdas de UR068 (cuerdas 14-33, 34-53, 54-73) frente a UR067 (cuerdas 13-32): 16/20 exactas (18/20 con UR066). Las discrepancias son **justo las de Urton**: 2 904 vs 2 908 y 161 vs 162; las otras dos son cuerdas rotas de UR067 (valor 0), como él dice. De las 12 columnas con suma ≥5 coinciden 8; en 5 000 permutaciones por sección el máximo es 2 (media 0,11). **Confirmada**.
- **UR066≈UR067** (27/32 posiciones iguales; 9 de 11 valores ≥5; LCS 9/10 frente a 4,1) y **UR064≈UR068** (LCS 16 de 22/23 frente a 7,3; 1 212/1 213, 1 236, 459, 43, 64): **confirmadas** (coincide con las copias que 04 ya listaba).
- **UR063 → UR068 sección central**: alineando las 6 secciones por la cuerda grande de cada una (127, 229, 148, 367, 157, 219), la suma de columna da 1 247 (UR068: 1 236), 46 (46 exacto), 44 (59), 8 (10); 5 de 20 columnas exactas (2 de 9 con valor ≥5) y P = 0,007 frente a permutar UR063, pero la alineación es post hoc. Totales: UR063 = 1 439; sección central de UR068 = 1 447. UR073 (incompleto, total 1 147) comparte solo 148 y 229 con UR063 (LCS 8, nulo máx 8). **Compatible, parcial** (el libro admite que este nivel es «ruidoso»).
- **Segmento introductorio («Puruchuco»)**: «exactamente 3 cuerdas de valor 1 y ninguna otra entre las 12 primeras» ocurre en **4 de 441 quipus: UR064, UR066, UR067, UR068, solo ellos**. Pero la posición exacta 1-7-9 sólo está en UR066; UR064 y UR068 tienen 1-8-10 y UR067 1-5-9. Firma compartida y exclusiva: **confirmada**; «precisamente el mismo arreglo en niveles II y III»: **refutada en las posiciones**; lectura toponímica «Puruchuco»: **propuesta** (no verificable).

### 2.5 Pachacamac (cap. 6) — `e_pachacamac.py`
- Apéndice (91 totales): coinciden con KFG 79 de 89 presentes (UR115 y UR126 no están en KFG; 10 difieren, de 2 unidades a 600; las mayores en términos relativos son HP009 497 vs 367 y UR218 8 282 vs 8 810). Estadísticos del corpus: 169 grupos de 5 cuerdas (✓ exacto), 145/107/79/74/71 de 3/1/4/2/6 (Urton 144/116/79/80/74), 66,3 % con subsidiarias (67 %), media de totales 15 693 (15 610); la mediana (1 344 frente a 1 486) no coincide. **Descriptivo: confirmado.**
- Seis pares «closely matching» (Tabla 6.1): mismo número de colgantes en 5 de 6 (el sexto 77/86), totales a ≤10 % en 4/6 (UR226/UR230: 12 019 vs 830), pero **correlación posicional de valores ≈ 0** (Spearman −0,24 a 0,24, todos p>0,08), color casi nunca igual y sin subsecuencia común por encima del nulo (el mejor caso, UR1096/UR196: LCS 16 frente a 14,2, p = 0,09). Que tres pares tengan a la vez igual número de colgantes y total a ±10 % ocurre solo 3 veces entre 3 655 pares de Pachacamac (se esperaban ≈1,5). **No reproducida** como «valores que coinciden»; queda la regularidad de recuento de cuerdas (propuesta).

### 2.6 Par «ceque» UR053B/UR053C (cap. 8) — `f_ur053.py`
Desde la cuerda 11 de UR053C y la 1 de UR053B (desfase 10): 35 de 51 valores idénticos y 39 cercanos (nulo permutado: 2,4, máximo 8; máximo sobre 25 desfases: media 5,1, máx. 10; p = 2e-4). Uniones: UR053C todo V, UR053B todo R (✓ opuestas), terna de color W/RL/AB periódica en 98 % de UR053B (✓). **Estructura del par: confirmada.** La lectura ceque (collana/payan/cayao, horario/antihorario) **no admite nulo: especulativa** (Urton: «without wishing to claim»).

### 2.7 Incahuasi (cap. 9) — `g_incahuasi.py`, `incahuasi_sets.csv`
- **UR268 (valor fijo 208, 19 cuerdas)**: 20 conjuntos con primera cuerda = suma del resto: error relativo mediano 8,5 % frente a 43 % si se permutan las primeras cuerdas entre conjuntos (p = 5e-4); 7 conjuntos a ≤1 % (sólo 1 exacto), 9 a ≤3 %: «las sumas no siempre cuadran», como dice Urton. **Confirmada, aproximada**.
- **UR275 (valor fijo 47)**: 24 conjuntos, 9 exactos y 16 a ≤1 %, error mediano 0,1 % (nulo 27 %, p = 5e-4); 7 tripletas (X, 47, X−47) en las cuerdas 78-102. **Confirmada**.
- **UR266/UR275**: 20 valores >1 000 idénticos en común (Urton: 18 de 43 + 8 cercanos); 102 pares a ≤3 %; 1 070+1 217 = 2 287 ✓; 1 653+1 606 = 3 259 ✓. Los dos son (con UR269, que tiene 8 cuerdas de 47 que Urton no menciona) los únicos con 47. **Copia: confirmada** (SINTESIS, 04). La lectura crédito/débito es **propuesta** (no distinguible de deducción fija, 09). Nota: 04 encontró además que los 33 totales de UR278 son cabeceras de UR266; Urton solo ve la copia UR266≈UR275, así que su par «credito/débito» omite que UR266 también resume a UR278 (jerarquía).
- **UR255/UR267A (15) y UR256/UR267B (10)**: tripletas X,c,Y: 14 (UR267A) y 12 (UR267B); X,Y,c: 8 (UR255) y 7 (UR256); sólo 0-1 del tipo contrario. Error 152−10=143 en UR267B y 153−143=10 en UR256: **idénticos en KFG**. Uniones: UR267A V / UR255 R; UR267B R / UR256 V (opuestas en ambos pares, coherente con 09). **Confirmada**; la exclusividad de 15 y 10 a cada pareja **no se cumple** (10 aparece 12 veces en UR264, 14 en JC010; 15, 7 veces en UR264). Valores fijos 30 (UR274A, 17 cuerdas) y 17 (UR274B, 12): ✓ presentes. UR273B «miles similares a UR266/UR275»: 0 valores >1 000 idénticos; «similar» no se puede probar.
- Interpretación tasa/cuota: **propuesta** (09 ya la deja como «deducción fija»).

### 2.8 Santa y el «Rosetta khipu» (cap. 12) — `h_santa.py`, `santa_grupos_posiciones.csv`
(Se reutiliza la reconstrucción en 133 grupos de 05, que coincide con 48/9/34/17/15/10.) El Apéndice B de Urton reproduce el KFG: los 9 primeros grupos de UR091 coinciden con KFG grupo por grupo.
- Sumas por posición KFG: 369, 1 507, 439, 4 871, 615, 616 (Urton: 359+rotas = 367/8, 1 512, 434, 4 876, 611, 616; diferencias de 4-5 en cinco columnas). La suma 367 de la posición 1 sólo se obtiene sacando el grupo de unión desconocida (05: p ≈ 0,005-0,018 con nulo de objetivo arbitrario). **Apoyado débilmente, post hoc**; el contraste de 05 sobre los 133 y 132 (P(mejor error ≤3) = 0,36-0,94) sigue en pie.
- **Posición 4 mayor del grupo** en el 88 % de los grupos (Urton: «always»): **no es regla estricta**.
- **Posición 1 determina el tamaño del resto**: dentro de cada quipu, ρ(p1, suma 2-6) = −0,16 a 0,14 (p >0,48; p1 casi constante por quipu); entre quipus ρ = 1,0 con n = 6 (p exacto 0,003): efecto de escala entre rollos, coherente con el «tamaño de fila» de 10, no una regla por grupo. **No reproducida** dentro del quipu.
- **Emparejamiento por rango** pachaca-quipu (ρ = 1; Σ|dif| = 22): con composiciones uniformes de 133 en 6 partes se alcanza Σ|dif| ≤ 22 el 25 % de las veces. **No excepcional**.
- **Posición 5/6 = población (5×132 = 660 vs 611/616, −7 %)**: la probabilidad de que alguna de las 6 columnas quede a ≤7 % de un objetivo log-uniforme 100-5 000 es 0,17. **Compatible, no discriminante** (Urton mismo admite que no distingue entre 5 y 6).
- Lo que Urton llama «problemas»: 133 vs 132 grupos, nombres y colores no resueltos. **Rosetta: no reproducida como equivalencia fila a fila; compatible a nivel del total** (consistente con la tabla de 05).

## 3. Tabla final

| Lectura de Urton | ¿Cifras coinciden? | ¿Estructura existe? | ¿Supera nulo? | Veredicto |
|---|---|---|---|---|
| L01 UR028: 102 = Σ 2-4 con subs; conjuntos 5 (pares/impares) | sí (5/6 sumas; impar A 25 vs 29) | sí (74+15, 30/20/20) | sí (p<2e-4) | **confirmada** (aritmética); AB=hanan **propuesta** |
| L02 UR029 censo | casi (125 vs 123; vacíos 4 vs 5) | sí (35 con subs, 7×5; 1 de 4 quipus) | n/a (criterio 7 % de quipus) | **compatible** |
| L03 50-60 quipus censales | sin lista | criterio cumplido por 35/482 | chi² no replicable | **compatible/no reproducida** |
| L04 UR006: 24 pares 21+9, 730, 362/368 | sí (729; 361/368; semestres) | sí (únicos en el corpus) | sí (estructura) | **confirmada** (estructura) |
| L04b UR006 como calendario bienal | 729 vs 730 | — | no (P≈0,40 por azar de tamaños) | **compatible** (propuesto) |
| L05 UR006: Tabla 4.3, 3 042, 80 fuera | sí (45/48; 3 037) | sí | sí (0,56 esperadas vs 45) | **confirmada** (cifras) |
| L05b 3 002 ≈ 3 000 tributarios | 3 037 / 2 957 | — | no (6,7 % a esa distancia; post hoc) | **compatible, débil** |
| L06 UR021 = fuente de meses 13-16 | sí | sí (LCS 20) | sí (0/300) | **confirmada** |
| L06 UR009 idem | parcial (fragmento 20-61-20) | parcial | no por bloque (p=0,39); triple única en 3/651 | **compatible/parcial** |
| L07 UR006 = quipu de Guaman | — | — | n/a | **especulativa** |
| L08 UR011 15 pares | sí 15/15 | sí | sí (p<1e-4) | **confirmada** (estructura) |
| L08b UR011 = colapso demográfico | cifras sí | descenso en escalón | no discrimina (ρ −0,81; curva monótona) | **compatible** |
| L09 UR063 → UR068 central | parcial (46 y 1 247 vs 1 236; 5/20) | alineación ambigua | p=0,007 (post hoc) | **compatible, parcial** |
| L10 UR068 → UR067/066 | sí (16/20; 18/20; 2904/2908 y 161/162) | sí | sí (0/5 000) | **confirmada** |
| L11 UR064≈UR068, UR066≈UR067 | sí | sí | sí (LCS 16 vs 7; 9 vs 4) | **confirmada** |
| L11b intro 12 cuerdas, 3 nudos en 1-7-9 | no (1-8-10; 1-5-9) | firma 3×valor 1: 4/441 | — | firma **confirmada**; posiciones **refutadas** |
| L12 seis pares Pachacamac | cuerdas 5/6; totales 4/6; UR218 8 282 vs 8 810 | no hay valores en común | no (ρ≈0) | **no reproducida** |
| L13 corpus Pachacamac | 79/89 totales; 169 grupos de 5 | sí | n/a | **confirmada** (descriptivo) |
| L14 UR053B/C ceque | sí (35/51 exactas) | sí (V vs R; W/RL/AB) | sí (p=2e-4) | **confirmada** (par); ceque **especulativa** |
| L15 UR268 suma con 208 | sí (aprox., 1 exacta) | sí (20 conjuntos) | sí (5e-4) | **confirmada** |
| L16 UR275 con 47, X-47 | sí (9 exactas, 16 ≤1 %) | sí | sí (5e-4) | **confirmada** |
| L17 UR266≈UR275, solo ellos con 47 | sí (20 exactos >1 000) | sí | sí (04: q=1e-8) | **confirmada** (copia); «solo ellos con 47»: UR269 también (8) |
| L18 UR255/267A, UR256/267B, paradigmas | sí (incl. 152→153) | sí (X,c,Y vs X,Y,c) | sí (09: p≈0,003) | **confirmada**; «exclusivos» 15 y 10: **refutada** |
| L19 UR274A 30, UR274B 17; UR273B | sí | sí | n/a | **confirmada**; «UR273B miles similares»: **no reproducida** |
| L20 Santa 133 grupos = 132 tributarios | 133 sí | sí (6 quipus de seisenas) | no (05: P 0,36-0,94) | **compatible** |
| L21 posición 1 = 367 pesos | 369/367 con exclusión | sí | p≈0,005-0,018 post hoc | **apoyado débil** |
| L22 posición 1 determina las demás | 5 columnas ±5 | no dentro del quipu | entre quipus ρ=1 (n=6) | **no reproducida** (por grupo); escala entre quipus |
| L22b pos. 5/6 = población | 611/616 vs 660 | — | P=0,17 | **compatible, no discrimina** |

## 4. Negativos y avisos
- **Corrección a SINTESIS**: «UR006 no reproduce el calendario» se debe a no contar las subsidiarias de las cuerdas-lazo. Estructura y sumas sí se reproducen; lo que sigue sin demostrarse es la interpretación calendárica y la de tributarios.
- Pares de Pachacamac (Tabla 6.1), emblema en 1-7-9 de Puruchuco, «posición 1 determina el resto» y exclusividad de los valores fijos 15/10/47: no sobreviven tal como se enuncian.
- Distancias de ±1-5 entre Urton y KFG (UR028, UR029, Santa, Tabla 4.3, Pachacamac) son del orden de errores de lectura de cuerdas; no explican nada.
- Ninguna lectura concreta se «traduce» a un sentido (qué se contó) con seguridad: lo que se confirma es aritmética de registro (sumas, copias, jerarquía), la misma conclusión de 04, 08, 09 y 10.

## 5. Niveles de evidencia
- **Bien apoyado**: estructura 24 pares de UR006 y sumas de la Tabla 4.3; UR021 como segmento de UR006; 15 pares gemelos de UR011; UR068 → UR067/UR066 (con las dos divergencias que cita Urton); copias UR064/UR068 y UR066/UR067; firma de 3 nudos exclusiva de 4 quipus de Puruchuco; par UR053B/C; sumas internas UR268/UR275, copias UR266/UR275 y paradigmas recíprocos de Incahuasi; UR028 cuerda 1 = Σ y conjuntos pares.
- **Apoyado con datos**: UR009 parcial (triple 20-61-20 única); suma de posición 1 del Santa ≈ 367 (post hoc, débil).
- **Propuesto**: calendario bienal de UR006; 3 000 tributarios; moieties por color/impar-par (UR028); tasa de depósito en Incahuasi; crédito/débito UR266/UR275.
- **Especulativo**: UR006 = quipu de Guaman; ceque en UR053B/C; UR011 como demografía; UR029 cuerda=tributario; «Puruchuco» como emblema toponímico; hanan/hurin y pachacas del Santa.

## 6. Siguiente ronda
1. Comprobar con el Apéndice A de Urton (orden de nombres del padrón) si el orden de los 133 grupos del Santa sigue el orden de las pachacas por posición del grupo (hipótesis falsable que 05 también pedía).
2. Buscar en KFG la estructura «par + lazo» fuera de UR006 con subsidiarias (HP038, UR113 son candidatos pero no regulares) y repetir la prueba de pares con un nulo de tamaños en HP038.
3. Para UR011: probar si el escalón entre los pares 9 y 10 coincide con otra variable (color, unión) y si las 4-6 cuerdas «bajas» antes de cada par suman o restan al par (columnas de ajuste).
4. UR063/UR073 con las secciones reales de Brezine (no una alineación por cuerda grande) para cerrar la jerarquía de Puruchuco con 04 (UR063 vs UR073/UR078).
5. Reintegrar L02/L03 en un benchmark: ¿cuántos de los 35 quipus «censo-like» tienen estructura de columnas (03) frente a los demás?
