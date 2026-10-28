# CM009 — Lectura profunda de un solo quipu (región Puruchuco)

Autor: equipo `k_CM009`. Fecha: 2026-10-17. Scripts en esta misma carpeta (`01_…`–`06_…`).

---

## 0. Pregunta

¿Qué estructura y qué aritmética interna tiene el quipu **CM009** y cuál es la lectura más
probable de su contenido (censo, tributo, depósito, calendario, otro), con controles
estadísticos explícitos?

---

## 1. Datos: advertencia de procedencia (crítico para interpretar todo lo demás)

**CM009 no está en los datos preparados del proyecto.** Comprobado:

- `analisis/datos/cuerdas.csv` (57 818 filas, 651 quipus): los prefijos presentes son
  `UR, AS, HP, QU, KH, MM, JC`. **No hay ninguna fila `CM…`.**
- `analisis/datos/quipus.csv` y `analisis/datos/grupos.csv`: tampoco contienen `CM009`.
- Las tablas de verdad del KFG (`data/external/data-science-khipu-article/data/ascher_sum_relations/*.csv`,
  650 quipus) y el volcado `KFG_DB.SQL` (26 MB) **tampoco** contienen `CM009`.
- `data/local_only/KhipuAnalysis/RobynDatabase.db` (KFG anterior) no lo tiene.

La **única** fuente en el repo con CM009 a nivel de cuerda es
`data/external/khipu-computational-toolkit/legacy/data/processed/cord_hierarchy.csv`
(export de la base KFG `khipu_database.db`, 709 quipus, 62 746 cuerdas; fecha 2026-02-26).
De ahí reconstruí CM009: **65 cuerdas**. La K-CAT lo etiqueta como región
**"Purucucho"** (sic) = **Puruchuco**, geo_zone "Central Coast", cluster "Simple".

Consecuencias metodológicas:
1. **No tengo `grupo`** (los grupos de colgantes del KFG). La columna `grupo`/`grupos.csv` es
   inaccesible para CM009. La agrupación que propongo abajo es **inferida del patrón de color**,
   no del campo oficial.
2. CM009 **no** forma parte de los 21–24 quipus de Puruchuco catalogados en el OKR
   (UR060–UR082, UR165 = KH0297–KH0319, KH0404). No pude resolver su número de museo.
   **No afirmo** que sea uno de los "grupo de Puruchuco" de Urton & Brezine (2005).
3. La direccionalidad de nudo llega como **U (desconocida)** en todas las cuerdas: KFG no la
   registró, así que no se puede analizar S/Z para este quipu.

Estas limitaciones están reflejadas en el nivel de evidencia.

---

## 2. Método

1. Reconstrucción cuerda a cuerda desde `cord_hierarchy.csv` (script `01_estructura.py`).
2. Estructura: niveles, subsidiarias, unión, torsión, colores, largos, valores, y parseo de la
   cadena de nudos (`nTIPO(pos,dir),valor`).
3. Aritmética interna: suma de subsidiarias, cuerdas superiores, sumas de grupos, y búsqueda
   exhaustiva de **sumas contiguas** (≥2 sumandos) y **acumulados** que igualen otra cuerda
   (`02_aritmetica.py`).
4. Periodicidad de color, de valor y de patrón de nudos (`03_periodicidad.py`, `04_periodos_holm.py`).
5. **Todos** los patrones se contrastan con nulos de **permutación, 1000 réplicas, semilla numpy 0**.
   Para el patrón de valor uso un nulo que **preserva el color** (baraja valores dentro de cada
   clase de color), que es el control honesto cuando el color ya es periódico.
6. Corrección de comparaciones múltiples: **Holm**, en dos familias (patrones globales y escaneo
   de periodos).
7. Prohibido: leer archivos grandes completos; sólo consultas y salidas ≤40 líneas.

---

## 3. Estructura reconstruida (resultados con cifras)

| Rasgo | Valor |
|---|---|
| Cuerdas totales | **65**, todas colgantes (nivel 0) |
| Subsidiarias / cuerdas superiores | **0 / 0** |
| Unión (attachment) | **"Unknown" en las 65** (KFG no registró R/V/T) |
| Torsión | **U en las 65** (desconocida) |
| Largo | **45 cm en las 65** (uniforme) |
| Colores | W=17, AB=16, GG=16, W:KB=16 (4 colores Ascher) |
| Valor total | **3486** (media 53.6) |
| Cuerdas sin nudos | **15 (23 %)**: p4,p5,p7,p8,p9,p13,p27,p29,p33,p47,p48,p49,p53,p57,p61 |
| Tipos de nudo | L (largo) 32, S (simple) 22, E (figura de 8) 16 |
| Dirección de nudo | **U en los 70 racimos** (no analizable) |

**Patrón de color (estricto).** La secuencia de colores es
`W,GG,W,AB,W:KB` (p1–p5) y desde p6 repite **exactamente** el ciclo de 4
`W,AB,GG,W:KB` hasta p65. Es decir, **61 de 65 cuerdas** siguen un ciclo de color de periodo 4
perfecto. El acuerdo a lag 4 es 0.934 (p=0.001; corrección Holm abajo).

**Estructura de "registros".** El ciclo de color de 4 define **15 registros** de 4 cuerdas
`[W, AB, GG, W:KB]` (p6–p65), precedidos por una **cabecera irregular de 5 cuerdas** (p1–p5:
W,GG,W,AB,W:KB = 1,1,1,0,0). 15×4 + 5 = 65.

| reg | W | AB | GG | W:KB | | reg | W | AB | GG | W:KB |
|----:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | 4 | 0 | 0 | 0 | | 9 | 57 | 5 | 6 | 2 |
| 2 | 8 | 2 | 1 | 0 | | 10 | **1236** | 46 | 59 | 10 |
| 3 | 8 | 1 | 3 | 1 | | 11 | 1 | 0 | 0 | 0 |
| 4 | 56 | 5 | 4 | 1 | | 12 | 3 | 1 | 1 | 0 |
| 5 | **1213** | 43 | 60 | 17 | | 13 | 6 | 1 | 3 | 0 |
| 6 | 2 | 0 | 1 | 0 | | 14 | 33 | 3 | 2 | 0 |
| 7 | 8 | 1 | 1 | 0 | | 15 | **459** | 44 | 39 | 13 |
| 8 | 8 | 1 | 3 | 1 | | | | | | |

**Las cuerdas blancas (W) son fronteras de registro**: aparecen cada 4 cuerdas desde p6 (W=17 en
total). Esto es exactamente el rol que **Medrano & Khosla (2024)** proponen para los cordeles
colgantes blancos: marcadores de límite de grupos. **Coincide**, pero es una convención
*propuesta* por ellos, no un hecho establecido.

**Tres super-grupos de 5 registros.** Los registros 1–5, 6–10 y 11–15 tienen la **misma forma**:
el registro 3 ≈ 8 (idénticos: `[8|1,3,1]`), 4 ≈ 9 (`[56|5,4,1]` vs `[57|5,6,2]`), 5 ≈ 10
(`[1213|43,60,17]` vs `[1236|46,59,10]`), y 5 ≈ 10 ≈ 15 (`[459|44,39,13]`). Es decir, el
quipu se lee como **3 bloques de 5 registros** (20 cuerdas cada uno), cada bloque con la
misma plantilla y valores distintos.

**Los cuatro campos correlacionan.** Sobre los 15 registros, Spearman:
W–AB = 0.95, W–GG = 0.88, W–W:KB = 0.83, AB–GG = 0.86 (n=15, **p<0.001** en todos). Las cuatro
categorías suben y bajan juntas → un único "tamaño" por registro desglosado en 4 columnas.

---

## 4. Aritmética interna y controles

| Hipótesis | Resultado | Contraste |
|---|---|---|
| colgante = suma de subsidiarias | **N/A** (no hay subsidiarias) | — |
| cuerda superior = suma de grupo | **N/A** (no hay cuerdas superiores) | — |
| W = AB+GG+W:KB (registro = suma) | **0 / 15** registros | — |
| W:KB = AB+GG | 2 / 15 (azar) | — |
| alguna cuerda = suma de un tramo contiguo (≥2) | 409 coincidencias | **p = 0.33** (no significativo) |
| acumulado P_i = cuerda posterior | 35 (todas triviales, valor 1) | — |
| valores repetidos | 50 cuerdas con valor no único | **p = 1.00** |

**Conclusión aritmética:** con el nulo pedido por el BRIEF (barajar valores dentro del quipu,
1000×, semilla 0), CM009 **no** muestra ninguna aritmética interna por encima del azar
(p = 0.33). Esto es coherente con que el KFG (verdad de referencia de sumas de Ascher) y el
propio detector de la K-CAT **no registran ninguna relación de suma para CM009** (comprobado:
0 filas en `ascher_sum_relations/*` y en `phase10_summation_groups.csv`). Las 409 "coincidencias"
contiguas son el **artefacto esperado** de un quipu con muchos valores pequeños (1 aparece 16×,
0/ausente 15×, 3 aparece 5×): con 65 números pequeños, las sumas de tramos igualan otra cuerda
por puro azar. **La explicación aburrida gana.**

---

## 5. Periodicidad y nulos (con corrección múltiple)

**Familia A — patrones globales (Holm, m=6):**

| Test | obs | p | p_Holm | |
|---|---:|---:|---:|---|
| color, lag 4 (periodicidad de color) | 0.934 | 0.001 | **0.006** | SIG |
| valor, lag 20 (nulo **preserva color**) | 0.400 | 0.001 | **0.006** | SIG |
| patrón de tipos de nudo, lag 20 | 0.622 | 0.001 | **0.006** | SIG |
| sumas contiguas | 409 | 0.332 | 0.663 | ns |
| valores repetidos | 50 | 1.000 | 1.000 | ns |
| valor, lag 4 (nulo preserva color) | 0.213 | 0.125 | 0.375 | ns |

**Familia B — escaneo de periodos del valor con nulo que preserva color (Holm, m=7):**
sólo **L=20** sobrevive (p=0.001 → **p_Holm=0.007**). L=4 (p=0.10), 8, 12, 16, 24 y 40 (p=0.06)
**no** son significativos.

**Lectura de los controles.** La periodicidad de *color* a lag 4 es trivialmente cierta. Lo
importante es que la **periodicidad de valor a lag 20 sobrevive al nulo que preserva el color**:
es decir, no se explica por "valores del mismo color tienden a repetirse". El 40 % de las
posiciones repiten su valor exacto a distancia 20, y el patrón de nudos repite al 62 % —frente a
~0.12–0.16 esperado al azar—. Por tanto existe una **plantilla de 20 cuerdas repetida 3 veces**.
Como el lag 20 = 5 ciclos de color, la plantilla son **5 registros de 4 cuerdas**.

---

## 6. Lectura propuesta

**Tipo de registro: lista cuantitativa administrativa de tipo censo/tributo** (propuesto;
la estructura es lo apoyado; el "qué se cuenta" es especulativo).

**Filas y columnas.**

- **Filas = 15 unidades/registros**, agrupadas en **3 bloques de 5**. Cada fila empieza con una
  cuerda **blanca (W)** que la delimita (patrón Medrano & Khosla).
- **Columnas = 4 campos** por fila: W (cuerda blanca, cabecera/límite con su propio valor),
  **AB, GG, W:KB**. Los cuatro campos **correlacionan fuertemente** (ρ 0.83–0.95), por lo que
  parecen un tamaño desglosado en 4 categorías, **no** una suma (W ≠ AB+GG+W:KB).
- Los tres valores W "grandes" (1213, 1236, 459) en los registros 5, 10 y 15 son las filas
  "de totales" de cada bloque de 5: el registro 5 de cada bloque lleva la magnitud mayor.
  **No** son sumas de nada interno (0/15 verificaciones exactas).

**Justificación literaria.**
- **Urton & Brezine (2005, Puruchuco)**: el archivo de Puruchuco "ejemplifica cómo se
  sintetizaban, manipulaban y transferían datos de **censo y tributo** entre niveles contables".
  Es el marco que hace plausible una lista administrativa en Puruchuco —pero el trabajo es
  **sólo resumen**, muestra pequeña y **sin controles**; no identifica CM009.
- **Medrano & Khosla (2024)**: (i) el 74 % de 650 quipus tienen fórmulas de suma de Ascher
  —CM009 **no** está entre ellos—; (ii) los **cordeles blancos** se proponen como **marcadores
  de límite** de grupos. En CM009 el blanco aparece cada 4 cuerdas → encaja con "límite de
  registro". Nivel de la convención en la ficha: **propuesto**.
- **Clindaniel (2019)**: la **seriación/banding** del color se relaciona con la **magnitud**
  (logística p<0.01). CM009 tiene color estrictamente seriado (periodo 4) y magnitud alta
  (media 53.6), en la dirección predicha.
- **Medrano & Urton / FitzPatrick / Thompson (valle del Santa, Arica)**: refuerzan que los
  quipus administrativos inka se organizan como listas cuantitativas repetitivas; n pequeño en
  todos esos casos.

Ninguna fuente menciona CM009; la lectura es una **inferencia por estructura y procedencia**,
no una lectura directa.

---

## 7. Lo que no encaja (anomalías e información no numérica)

1. **Cabecera irregular p1–p5**: colores W,GG,W,AB,W:KB y valores 1,1,1,0,0 rompen el ciclo.
   Puede ser un **encabezado/etiqueta de sujeto** (título del registro) o simplemente el
   arranque físico del quipu.
2. **Registros 1, 6 y 11** (los primeros de cada bloque de 5) tienen **sólo la cuerda W con
   nudos**; AB, GG y W:KB están **vacías**. Patrón sistemático, no aleatorio: los "primeros
   de bloque" funcionarían como sub-cabeceras.
3. **15 cuerdas sin nudos (23 %)**. En el BRIEF, valor 0 sin nudos = **ausente**, no cero real.
   Posiciones dentro del registro: casi todas son AB/GG/W:KB de registros pequeños, más la
   cabecera. Unas 0 reales no existen aquí.
4. **Todos los nudos son de dirección U** (70/70) y **todas las uniones "Unknown"**: KFG no
   registró S/Z ni R/V/T. No es que "no haya dirección": es que **falta el dato**. Cualquier
   lectura que dependa de S/Z o de R/V en CM009 es **imposible** con estos datos.
5. **Los tres valores W grandes** (1213, 1236, 459) no encajan con el resto (≤60): son 3
   outliers en progresión de lag 20. Podrían ser **totales** o **cantidades de otra unidad**, o
   incluso **no numéricos** (p. ej. un identificador con nudos en varias posiciones). No hay
   forma de decidirlo con un solo quipu.
6. **Nudos E (figura de 8)**: 16, repartidos en los campos de valor 1. En la literatura (Sivan
   2026) el E a veces se lee como marca de modo/no-numérica; aquí siempre acompaña al valor 1,
   lo que **no** apoya esa lectura (aquí E ≈ 1).

---

## 8. Resultados negativos (reportados explícitamente)

- **No hay jerarquía de cuerdas**: 0 subsidiarias, 0 cuerdas superiores, 0 grupos con suma
  detectada (KFG y K-CAT coinciden).
- **No hay aritmética interna** significativa (sumas contiguas p=0.33; valores repetidos p=1.0;
  W≠suma de sus 3 hermanos en 0/15).
- **El lag 4 del valor NO es significativo** una vez que el nulo preserva el color (p=0.125):
  la similitud de valores a distancia 4 era sólo el eco del color.
- **Periodos 8/12/16/24/40**: no significativos.
- **No se puede analizar** dirección de nudo (S/Z), unión R/V, ni grupos oficiales: datos
  ausentes para este quipu.

---

## 9. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| CM009: 65 colgantes, sin subsidiarias ni cuerdas superiores, largo 45, 4 colores | **bien apoyado** (dato directo) |
| Color en periodo 4 estricto desde p6 (acuerdo 0.934, p_Holm=0.006) | **apoyado con datos** |
| Plantilla de 20 cuerdas repetida 3× en valor y nudos (p_Holm=0.006, sobrevive nulo color-preservado) | **apoyado con datos** |
| Estructura = 15 registros `[W,AB,GG,W:KB]` + cabecera de 5, en 3 bloques de 5 | **apoyado con datos / propuesto** (la partición en 4 depende de mi lectura del color; no tengo `grupo`) |
| Los 4 campos correlacionan (una magnitud desglosada, no suma) | **apoyado con datos** |
| Lectura como censo/tributo (lista administrativa cuantitativa) | **propuesto** |
| Significado concreto de W (total / etiqueta / contador) | **especulativo** |
| CM009 pertenece al "grupo de Puruchuco" de Urton & Brezine | **especulativo / no verificado** |

---

## 10. Para el coordinador

- **CM009 no existe en `analisis/datos/*.csv`** (ni `cuerdas`, ni `quipus`, ni `grupos`), ni en
  el volcado `KFG_DB.SQL`, ni en la verdad de sumas del KFG. Sólo está en el export K-CAT
  `legacy/…/cord_hierarchy.csv` (base KFG de 709 quipus). **Hay que decidir si se incorpora o se
  excluye**; si el resto del equipo asume que CM009 está en los datos preparados, es un error de
  base. No pude resolver su número de museo ni confirmar que sea uno de los 21 de Urton.
- CM009 es un quipu **plano**: 65 colgantes, **0 subsidiarias y 0 cuerdas superiores**, largo 45
  uniforme, **unión y dirección de nudo no registradas** (U). No sirve para probar jerarquía
  contable; sirve para estructura de lista.
- **Hallazgo principal (apoyado):** la secuencia de **color es estrictamente periódica de
  periodo 4** (`W,AB,GG,W:KB`) y el **valor y el patrón de nudos son periódicos de periodo 20**
  (3 repeticiones). El lag 20 **sobrevive a un nulo que preserva el color** (p_Holm=0.006): no es
  un artefacto del color. 40 % de posiciones repiten valor exacto a distancia 20.
- **Sin aritmética interna.** Sumas contiguas p=0.33, repetidos p=1.0, W≠AB+GG+W:KB (0/15). Las
  409 coincidencias son azar de valores pequeños. KFG y K-CAT coinciden en que CM009 no tiene
  sumas. **Cuidado con "hallar" sumas aquí.**
- **Estructura propuesta (apoyado/propuesto):** 15 registros de 4 cuerdas `[W(blanca), AB, GG,
  W:KB]` + cabecera de 5; los registros forman **3 bloques de 5** con la misma plantilla. El
  blanco delimita cada registro, coincidiendo con Medrano & Khosla (2024, **propuesto**).
- Los 4 campos por registro **correlacionan ρ 0.83–0.95**: una magnitud única desglosada en 4
  columnas (no una suma). Consistente con una **lista administrativa** (censo/tributo) de
  Puruchuco (Urton & Brezine 2005), pero la lectura semántica es **propuesto**, no bien apoyado.
- **Anomalías:** cabecera p1–p5 irregular; registros 1/6/11 sólo con la cuerda blanca;
  3 valores W gigantes (1213, 1236, 459) en progresión lag-20 que no encajan; 23 % de cuerdas
  sin nudos (ausentes, no ceros). El E (figura de 8) siempre vale 1.
- **Recomendaciones:** (1) crear la tabla puente que traiga CM009 (y los ~58 quipus KFG que
  faltan) a `analisis/datos/`; (2) conseguir `grupo`/posición física real para validar mi
  partición de 4; (3) con `grupo` oficial, re-testear si el blanco marca límites de grupo en
  todo el corpus KFG (no sólo aquí); (4) buscar en los otros 709 KFG quipus el mismo patrón
  color-periodo-4 + valor-periodo-20 (¿es un género de quipu?); (5) buscar el registro
  fotográfico de CM009 para confirmar colores (Milillo et al. 2023: el color observado puede
  estar alterado).
