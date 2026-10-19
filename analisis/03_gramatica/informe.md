# 03_gramatica: ¿los quipus se comportan como tablas o como texto?

**Respuesta corta.** Estadísticamente, los quipus se comportan como **registros de datos**. Ningún subconjunto pasa una prueba de "texto" que no se explique igual de bien por números, bandeado de color o artefactos de codificación. Hay tres tipos de estructura: (1) **bandeado**, es decir, corridas de cuerdas iguales y autorrepetición mayor que el azar, algo que el texto natural no tiene; (2) **columnas dentro de los grupos explícitos** en cerca de la mitad de los quipus que tienen grupos repetidos; (3) **convenciones de formato compartidas dentro de un mismo archivo**, que viven en la secuencia de colores y no en los patrones de nudos. El único subconjunto anómalo son 26 quipus "STRING" con mayoría de cuerdas no decimales (UR039, UR050–055, AS014, UR203...). Es heterogéneo, tiene poca diversidad de color y su "canal silábico" se parece poco al quechua: tiene 4,5 veces menos efecto de posición y 2,4 veces menos diversidad léxica, y sus secuencias de vueltas tienden a ser decrecientes, lo cual es más propio de números.

Scripts (Python 3.13, semilla fija `SEMILLA = 20261017` + desplazamiento por tarea), en `analisis/03_gramatica/`:
`comun.py` (carga, tokens, teoría de la información y referencias; `python comun.py` corre autocomprobaciones), `t1_entropia.py`, `t1b_perfil.py`, `t2_tabla.py`, `t3_ngramas.py`, `t4_direccion.py` y `t5_textuales.py`. Las salidas están en `resultados/`. El orden de ejecución es t1, t1b, t2, t3, t4 y t5 (t5 lee las salidas de t1 y t2). Tiempo total: unos 45 min.

## Datos, tokens y referencias

- Secuencia = **colgantes (nivel 0) en orden**, por quipu. Unidad de análisis = quipu. Los quipus con menos de 10 colgantes (t1) o menos de 12 (t2) quedan fuera.
- Tokens: **color** (código Ascher sin rangos en cm); **patrón** (tipos de nudo y lugar decimal, sin dígitos; p. ej. `S2.S1.L0`, `-` = sin nudos); **tupla** (color|patrón|unión|torsión); **magnitud** (nº de dígitos; 0 = sin nudos, ausente y no cero).
- Cuerda "no decimal" (`anom_dec`): más de un racimo largo u ocho, un largo u ocho que no es el último, o lugares no decrecientes. Afecta a 3.320 de 40.160 cuerdas anudadas (8,3 %). Es más estricta que la definición STRING de Sivan.
- Referencia lingüística (d): **Declaración Universal de Derechos Humanos** en quechua boliviano y en español (corpus `udhr` de NLTK, en `ref/`), silabeada por reglas (C)(C)V(C) con dígrafos quechuas (3.399 y 3.413 sílabas). También se usan letras del quechua. Se toman ventanas aleatorias **de la misma longitud que cada quipu**. Limitación: es un solo texto, jurídico y moderno.
- Sitio: procedencia arqueológica gruesa (nunca museo). Las colecciones privadas y "Unknown" cuentan como desconocidas (268 de 651).

## 1. Entropía, entropía condicional, IM por desfase, Zipf y Heaps (`t1_*`)

Por documento se calculan H0, ΔH_k = H_k(nulo) − H_k(obs) para k = 1–3 (en fracción de H0), el exceso de información mutua I(X_t; X_{t+d}) para d = 1–20 (z frente a 200 barajados), la autorrepetición (P(x_t = x_{t−1}) frente al barajado), Zipf y Heaps. Nulos: (a) barajado dentro del quipu; (b) barajado del orden de los grupos; (c) tabla sintética emparejada (misma longitud y frecuencias, k = tamaño modal de grupo, fidelidad 0,5–0,9); (d) ventanas de texto.

Medianas por clase (543 quipus; `t1_resumen.csv`, `t1b_resumen.txt`):

| clase | ΔH1/H0 | autorrep. (obs/azar) | % con autorrep. < 1 | % periódico* | Zipf (por doc.) | Heaps β |
|---|---|---|---|---|---|---|
| quipu, color | 0,23 | 1,19 | 33 % | 21 % | 1,35 | 0,44 |
| quipu, patrón | 0,06 | 1,28 | 23 % | 24 % | 1,49 | 0,46 |
| quipu, tupla | 0,08 | 1,72 | 29 % | 12 % | 0,90 | 0,73 |
| tabla sintética (color) | 0,08 | 0,85 | 74 % | 60 % | 1,62 | 0,31 |
| texto quechua (sílabas) | 0,02 | ≈0 | 86 % | 2 % | 0,43 | 0,90 |
| texto quechua (letras) | 0,07 | 0,25 | 95 % | 4 % | 0,83 | 0,66 |
| quipu barajado (azar) | 0,00 | 1,00 | 52 % | 9 % | — | — |

\*periódico = el máximo z de IM en desfases mayores que 1 supera 3 y supera al del desfase 1.

- La dependencia de desfase 1 es significativa (p_a < 0,05) en el 70 % de los quipus por color, el 44 % por patrón y el 62 % por tupla, frente al 43–59 % del texto y al 4–6 % del azar. **Ambos tienen orden**, así que esto no distingue texto de tabla.
- El rasgo que separa es la **autorrepetición**. Los quipus repiten la misma cuerda contigua más de lo esperado (bandeado). El texto la evita: casi ninguna sílaba se repite contigua, y en letras la tasa es 0,25 de la esperada. En quipus de 100 o más colgantes solo el 19–28 % tiene autorrepetición menor que 1.
- El barajado de grupos (b) apenas cambia ΔH1 (mediana de ΔH1_b ≈ 0,01): la estructura de desfase 1 está **dentro de los grupos**. Lo mismo pasa con el texto al barajar palabras, así que no discrimina.
- **Zipf no sirve para diagnosticar.** A escala de corpus, el exponente de la tupla color|patrón|unión|torsión es 0,86, igual que el β = 0,851 que Sivan presenta como "lingüístico", y el quechua silabeado da 1,27. Zipf depende de cómo se define el token. **Demostrado** (como contraejemplo).
- Clasificador (regresión logística entrenada solo con referencias: texto, tabla, bandeado, azar; exactitud CV-5 = 0,71–0,82). **No es robusto**: la proporción de quipus "texto" pasa del 6 % (color, con rasgo de autorrepetición) al 20 % sin él, y en tupla del 19,5 % al 54 %. Al quitar la autorrepetición, "texto" se vuelve la clase de "estructura débil sin periodicidad", que se solapa con el azar en secuencias cortas. Los quipus que "parecen texto" son casi todos pequeños (n = 10–46). **Resultado negativo**: con estas métricas de secuencia, texto y "estructura débil" no se separan en documentos cortos.

**Conclusión T1** (*apoyado con datos*): los quipus caen entre "bandeado" y "tabla", no junto al texto. La firma del texto (antirrepetición, vocabulario que crece con Heaps β ≈ 0,9) no aparece en el corpus.

## 2. Estructura de tabla (`t2_*`)

Dos pruebas por quipu, para color y para magnitud:
- **B, grupos explícitos**: en los grupos del tamaño más frecuente (2 o más, al menos 3 grupos), ¿la posición dentro del grupo predice la variable? El nulo permuta dentro de cada grupo, de modo que conserva la composición de cada fila y, con ella, el bandeado. P = 2000.
- **A, periodo implícito**: k = 2–15, con el mismo nulo intrafila y combinación de Simes.

Primero se calibró el método. La versión inicial con nulo de barajado global daba un **26 % de falsos positivos en texto**, porque la dependencia local infla la varianza. Por eso se adoptó el nulo intrafila y se añadieron referencias emparejadas por quipu (sustituto de Markov de orden 1 del propio quipu y ventana de texto con los mismos grupos).

| prueba | quipus | Markov-1 | texto | tabla fid. 0,3 / 0,6 |
|---|---|---|---|---|
| B grupos, color, p < 0,05 | **51,4 %** (n = 290) | 11,1 % | 5,3 % | 46 % / 79 % |
| B grupos, magnitud, p < 0,05 | **45,7 %** (n = 289) | 3,8 % | — | — |
| A implícito, color, p < 0,05 | 29,7 % | 15,1 % | 12,2 % | 31 % / 70 % |
| A implícito, magnitud, p < 0,05 | 18,8 % | 5,9 % | — | — |

- Fracción tabular estimada, (r − r0)/(1 − r0): **45–49 %** de los quipus con grupos repetidos (color) y 44 % (magnitud). Por periodo implícito, 14–20 %. Con BH, **175 de 299 quipus con grupos repetidos (58,5 %)** tienen columnas significativas (q < 0,05) en color o magnitud. Sobre los 518 quipus de 12 o más colgantes, 215 (41,5 %) muestran alguna estructura de columnas con q < 0,05 en alguna prueba. Es una cota inferior, porque muchos quipus no tienen grupos repetidos o tienen un solo color.
- Entre los quipus con periodo implícito significativo, las **columnas son más homogéneas que las filas en el 82 %**. El tamaño modal de las filas significativas tiene mediana 6 (rango intercuartil 4–8).
- **Nivel**: *demostrado* que existe estructura de columnas dentro de los grupos en cerca de la mitad de los quipus con grupos, con controles de dependencia local y texto. Que esas columnas sean "categorías de registro" es *propuesto*: puede ser, por ejemplo, una cuerda inicial de otro color que marca el grupo, que sigue siendo una columna.

## 3. "Frases" compartidas (`t3_*`)

Se buscaron n-gramas (n = 2–4) de color|patrón presentes en 3 o más quipus. Hay 2.224 candidatos y cuatro nulos dentro del quipu (P = 400): A barajado libre, R barajado de corridas (conserva el bandeado), **Cfijo** (secuencia de colores intacta y patrones barajados) y **Pfijo** (patrones intactos y colores barajados). BH sobre los candidatos.

- Bigramas: hay **menos** compartidos que en el nulo (1.128 frente a 1.360), porque el bandeado reduce los bigramas distintos. Trigramas y tetragramas: más que en el nulo A y en R (4-gramas: 424 frente a 144 y 283; p = 0,0025).
- 369 n-gramas no homogéneos superan R (q < 0,05) y 482 superan Pfijo. **Ninguno supera Cfijo**, ni de uno en uno (0 con q < 0,05) ni en total (4-gramas 424 frente a 433, p = 0,76). Es decir, **todo el exceso de "frases" compartidas se explica por la secuencia de colores**. El orden de los patrones de nudos no añade vocabulario compartido entre quipus (*apoyado con datos*, resultado negativo importante para cualquier hipótesis léxica sobre los nudos).
- Concentración por sitio: la pureza media de sitio de los n-gramas significativos es 0,496, frente a 0,439 si se permutan las etiquetas de sitio (p = 0,012). El efecto es modesto. Hay 15 n-gramas confinados a un solo sitio: **Santa (UR087–UR091, el conjunto ya emparejado de Medrano y Urton)**, **Leymebamba** (`MB|- > MB|E0 > MB|L0` en 7 quipus) e **Incahuasi** (`PK|- > W|S3.S2.S1.L0` en UR266, UR268, UR269 y UR273B: cuerda rosada vacía seguida de una blanca con un valor grande, que parece una cabecera). *Apoyado con datos*: hay **convenciones de formato de archivo** (formularios), no vocabulario panandino. Explicación aburrida posible: un mismo escriba o copias del mismo documento.

## 4. Dirección S/Z y torsión (`t4_*`)

Las etiquetas se definen por cuerda y por separado según el tipo de nudo, porque los tipos difieren: **dirLE** es la dirección del racimo de unidades (estratificada por L o E), **dirS** la de los simples y **tor** la torsión. Se usan quipus mixtos (minoría de 3 o más, 10 o más cuerdas). Permutaciones dentro del quipu con P = 2000. Estadístico de corpus = suma de z con permutaciones conjuntas. Holm sobre las 30 pruebas.

- Uniformidad: torsión uniforme en el 93,8 % de 439 quipus (S = 92 %, como Ascher); dirS uniforme en el 74,7 % (S = 26 %); dirLE uniforme solo en el 40 % (S = 46 %). En la misma cuerda, el largo u ocho es más a menudo S que los simples en 118 quipus, y lo contrario en 62 (Wilcoxon p = 2,5·10⁻⁸; en el 24,7 % de las cuerdas difieren). Esto **replica a Clindaniel** (simples Z, largos más S) con el quipu como unidad. Los ochos (E) son mayoritariamente Z (3.133 frente a 1.237).
- **Marcador de inicio de grupo: negativo** (dirLE p = 0,61; dirS p = 0,44; tor p = 0,35; Holm = 1).
- **Bloques y homogeneidad por grupo: fuerte** (dirLE: Z = 175, Holm 0,015, 26 quipus con q < 0,05; dirS: 15; tor: 5 de 8). La dirección se mantiene por grupos.
- ¿Sigue al color o a la magnitud de la cuerda? Al condicionar al grupo (permutando solo dentro del grupo), dirLE~color se reduce a p = 0,024 (Holm 0,16) y dirLE~magnitud a p = 0,065 (Holm 0,39). La dirección **sigue al grupo, no a la cuerda**. Para dirS, color|grupo se mantiene (Holm 0,015, pero solo 2 quipus con q < 0,05).
- **Oposición de mitades**: "mitad|grupos", con un nulo que baraja el orden de los grupos, es significativa en dirLE (Holm 0,015) y dirS (Holm 0,015). Por quipu solo hay 3 y 2 casos con q < 0,05, así que es un efecto débil y difuso de "secciones" más largas que un grupo. En torsión no aparece (p = 0,40).
- No se puede contrastar torsión × dirección: solo hay 16 quipus con ambas variables mezcladas.
- **Nivel**: *demostrado* que la dirección se organiza por grupos y bloques; *rechazado* (resultado negativo) que marque el inicio de grupo; *apoyado con datos, débil* que haya secciones mayores que un grupo. La interpretación funcional (sección temática u "oposición de mitades" frente a sesión o mano de anudado) es **especulativa**. La explicación aburrida, que cada grupo lo anudara una persona o en una sesión distinta, predice exactamente este patrón y no se puede descartar con estos datos.

## 5. Candidatos más "textuales" (`t5_*`)

La puntuación es el rango medio de: fracción de cuerdas no decimales; parte de la dependencia que está en el desfase 1 y no en un periodo; ausencia de bandeado; poco efecto de columnas (tamaño del efecto, no p); pocas relaciones de suma de Ascher (KFG) por cuerda; y riqueza de patrones. Se calcula sobre 298 quipus con 30 o más colgantes y al menos 50 % anudados, **corregida por log(n)**: la primera versión, con n ≥ 20 y valores p, tenía ρ = −0,52 con n, es decir, premiaba lo pequeño. Tras la corrección, ρ con n = 0,01. Con la fracción de cuerdas rotas la correlación es ρ = 0,14 (p = 0,019): **leve contaminación por daño**. Con la proporción de rasgos desconocidos no hay correlación (|ρ| < 0,08).

Top 20 (`t5_top20.csv`; ⚠ = rotas por encima del P75 = 28,7 %, o dirección desconocida en más del 50 %): AS090_N2 (⚠ dir U), **UR050** (⚠ 48 % rotas), UR268, UR1087, **UR203**, AS028 (⚠ dir U), UR153 (⚠ 90 % rotas), UR240 (⚠), HP051_A, UR038, **AS014** (⚠ dir U), UR1106, UR278, UR015, UR007, UR005, UR270, UR255, UR274A (⚠) y UR060.

Lectura crítica:
- La lista es **heterogénea y frágil**: depende de pesos arbitrarios. Incluye quipus de Incahuasi (UR255, UR268, UR270, UR278) que son contabilidad de almacén conocida (Urton y Chu; Clindaniel). Solo los que combinan una fracción no decimal alta con poca tabularidad son candidatos con sentido: **AS090_N2, UR050, UR203, AS014, UR1087, HP051_A**, y fuera del top KH0001, UR039, UR051–UR055 y UR193.
- **26 quipus con 50 % o más de cuerdas no decimales** (y 10 o más anudadas): solo 2 de 25 evaluables tienen columnas, frente a 213 de 493 del resto (Fisher OR = 0,11, p = 2,6·10⁻⁴), y eso pese a ser mayores (n mediana 72 frente a 45). **Factor de confusión**: tienen pocos colores (mediana 3; UR050, UR054 y UR039 tienen 2) y casi nunca grupos repetidos, así que la potencia de la prueba de columnas es baja. Su procedencia está concentrada en desconocida (15), Pachacamac (4) y Lima (3).
- Hay **artefactos de codificación** entre los "no decimales": AS019 registra `400L(6.5,U),400`, es decir, la cifra de centenas como un "largo" de 400 vueltas. Es una convención de transcripción, no un nudo real. Hay que auditar antes de leer.
- **Prueba directa del "canal silábico" de Sivan** (2.700 cuerdas con 2 o más racimos largo/ocho, 258 quipus). El orden de los racimos dentro de la cuerda importa (I(token; inicio/medio/final) frente a barajado intra-cuerda, p = 0,0005), pero el exceso es 0,021·H0, frente a **0,093·H0 en palabras quechuas**: 4,5 veces menor. La razón tipos/ocurrencias de las "palabras" es 0,24 frente a 0,56 en quechua (más repetición, vocabulario de solo 50 "sílabas"). El 69 % de las cuerdas tiene vueltas **no crecientes** hacia abajo, frente al 51 % si se barajan. Ese orden descendente es una regularidad de tipo numérico o de procedimiento, no fonotáctica. **Nivel: apoyado con datos que hay estructura posicional; especulativo, y no apoyado por estas pruebas, que sea texto.**

## Resultados negativos (resumen)

1. Las métricas de secuencia (entropía condicional, IM) no separan "texto" de "estructura débil" en documentos cortos. El clasificador cambia de 6 % a 54 % "texto" según los rasgos.
2. Ningún n-grama de color+patrón se comparte entre quipus más allá de lo que explica la secuencia de colores. No hay vocabulario de patrones de nudos.
3. La dirección de nudo no marca el inicio de grupo. Tampoco sigue al color ni a la magnitud de la cuerda una vez condicionada al grupo (dirLE).
4. El nulo de barajado global da falsos positivos de "tabla" en texto (26 %). Hubo que cambiar de prueba, y queda documentado.
5. Zipf ≈ 0,85 aparece con tuplas de rasgos físicos: no es evidencia lingüística.

## Niveles de evidencia

| afirmación | nivel |
|---|---|
| Los quipus tienen bandeado (autorrepetición mayor que el azar) y no la antirrepetición del texto | apoyado con datos |
| Columnas dentro de grupos en cerca del 50 % de los quipus con grupos (≈ 41 % del corpus de 12 o más colgantes con alguna prueba) | demostrado (estructura) / propuesto (función) |
| Zipf no diagnostica lengua | demostrado (contraejemplo) |
| Formatos de archivo compartidos (Santa, Leymebamba, Incahuasi) en la secuencia de colores | apoyado con datos |
| Sin vocabulario compartido de patrones de nudos | apoyado con datos (negativo) |
| Dirección de nudo homogénea por grupo; no marca inicio; secciones débiles | demostrado / negativo / apoyado débil |
| Interpretación de la dirección como "mitades" o "signo" | especulativo |
| Subconjunto STRING menos tabular | apoyado con datos, confundido por baja diversidad de color |
| STRING = texto silábico | especulativo; las pruebas aquí no lo apoyan |

## Limitaciones

Hay un solo texto de referencia, corto, jurídico y moderno, con un silabeo por reglas aproximado. Las secuencias se calculan solo sobre colgantes: las subsidiarias quedan para la siguiente ronda. Las entropías plug-in tienen sesgo en n pequeño, aunque se controlan con los nulos de la misma longitud. Toda la base es KFG y no se cruzó con OKR. La prueba de columnas exige variación de color o magnitud y grupos repetidos. La puntuación de textualidad tiene pesos arbitrarios.

## Siguiente ronda

1. **Auditar las 3.320 cuerdas no decimales** contra el OKR y las fichas originales para separar convenciones de transcripción (tipo AS019) de nudos reales. Después, repetir T5 solo con las genuinas.
2. En los quipus STRING (UR039, UR050–055, KH0001, UR193, UR203), probar **hipótesis numéricas alternativas**: listas de dígitos sueltos, calendarios, conteos ordenados. Por ejemplo, comprobar si las secuencias descendentes de vueltas cumplen sumas entre cuerdas, usando nulos que conserven la composición por cuerda.
3. Probar si las **columnas** detectadas coinciden con las relaciones de suma de Ascher (¿la columna j de cada grupo es suma de otras?) y con los marcadores blancos de Medrano y Khosla.
4. Comprobar la hipótesis de la "sesión de anudado" para la dirección: ¿los cambios de dirección coinciden con cambios en la posición en cm de los racimos (otra "mano")?
5. Repetir T1 con un corpus quechua más largo y variado (por ejemplo, textos coloniales normalizados) y con secuencias que incluyan subsidiarias.
