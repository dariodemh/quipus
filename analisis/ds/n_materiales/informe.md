# Materiales como evidencia de producción: ¿quién hacía qué registros?

**Equipo:** `n_materiales` · **Fecha:** 18-10-2026 · **Semilla:** 20261018
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `quipus.csv`, OKR `khipu.db` (54 403 cuerdas, 612 quipus), e informes previos `t_canutos_fibra`, `k_UR262`, `t_mitades`, `13_sistema_incahuasi`, `14_copias`.
**Scripts:** `01_firma.py` → `08_resumen.py` (esta carpeta), en ese orden: `python 01_firma.py; python 02_pureza.py; ...; python 08_resumen.py`. Todos los p-valores son empíricos con semilla fija.

---

## 1. Pregunta

¿Los rasgos **no numéricos** de manufactura (torsión, dirección de nudo por tipo, fibra, terminación, unión al cordón, grosor, paleta) permiten identificar **manos, talleres o lotes de producción**? En concreto:

1. ¿Hay una firma de manufactura por quipu y por grupo?
2. ¿Forman los quipus grupos discretos (talleres/manos) que sobrevivan a un nulo?
3. ¿Los quipus aritméticamente relacionados de Incahuasi (UR273A/B, UR266, UR275, UR270, UR278, UR269) comparten mano? ¿Y las copias?
4. ¿Cambia la firma dentro de un quipu (añadidos, reparaciones)?
5. Control obligatorio: ¿cuánto de la "firma" es en realidad **quién transcribió** los datos?

**Advertencia conceptual que ordena todo el informe:** una firma de manufactura puede identificar un **lote de producción** (una sesión, un taller, una tradición local) pero no a una **persona**. "Misma mano" exige que la variación entre individuos sea mayor que la variación entre objetos del mismo individuo, y eso no es observable sin una agrupación externa validada. Todo lo que sigue distingue explícitamente ambos niveles.

---

## 2. Método

### 2.1 Construcción de la firma (`01_firma.py`)

Por quipu (unidad de análisis = quipu, nunca cuerda):

| Rasgo | Operacionalización | Cobertura |
|---|---|---|
| Torsión | `pS_tors` = S/(S+Z) en cuerdas con dato | 515/651 quipus (≥5 cuerdas) |
| Dirección de nudo | `pS_nd_simple`, `pS_nd_largo`, `pS_nd_ocho` parseando `nudos` | 465/651 (≥1 nudo simple) |
| Unión al cordón | `pR` = R/(R+V+T) | 462/651 |
| Terminación | `pK`, `pB`, `pU` sobre cuerdas con dato | 651/651 |
| Paleta | entropía normalizada de familias de color, colores/cuerda, `pW`, `pAB`, `pMB` | 651/651 |
| Fibra | fracción CL (camélido) en OKR | 313/651 |
| Grosor | media y CV por quipu en OKR | 593/651 |
| Canutos | fracción de cuerdas envueltas | solo 8 quipus con detalle OKR |

La dirección de nudo se calcula **por tipo** porque el tipo impone la dirección: en el corpus, los nudos simples son 72 % Z y los largos 54 % S (`02_pureza.py`). Mezclar tipos sin condicionar produce un artefacto mecánico.

### 2.2 Nulos

- **Pureza interna:** se barajan las etiquetas de cuerda **entre quipus** conservando tamaños; así el nulo reproduce la composición marginal del corpus. 4 000 permutaciones.
- **Independencia de ejes:** χ² con nulo de permutación (10 000) + BH sobre las 6 parejas.
- **Firma idéntica:** nulo que baraja cada eje de forma independiente entre quipus (preserva marginales, destruye la coherencia multivariada); 5 000 réplicas.
- **Clustering:** KMeans sobre 4 ejes one-hot + 6 rasgos continuos estandarizados → PCA; silueta observada frente a 300 nulos de barajado independiente de rasgos. Bootstrap de cuerdas dentro de cada quipu (100) y de quipus al 80 % (200), con ARI.
- **Dentro del quipu:** número de rachas del valor minoritario (2 000 permutaciones) y cambio de régimen por máximo TV con 500 permutaciones; BH por rasgo.
- **Pares (Incahuasi, copias):** distancia de firma media frente a subconjuntos aleatorios del **mismo sitio** y, en el control decisivo, del **mismo sector**.

Corrección múltiple: BH-FDR por familia de pruebas; se indica cuando aplica. p mínimo reportable = 1/(B+1) (0,00025 con 4 000).

---

## 3. Resultados

### 3.1 El quipu es una unidad de manufactura: cada rasgo es casi constante dentro del objeto

Solo se cuentan valores **conocidos**: U/Unknown/? no son categorías de manufactura y se excluyen (incluirlos inflaría artificialmente la pureza de los quipus mal catalogados).

| Rasgo | Quipus | Pureza observada | Pureza nula | p | % quipus 100 % puros |
|---|---|---|---|---|---|
| Torsión (S/Z) | 501 | **0,995** | 0,930 | <0,00025 | **93,4 %** |
| Dirección nudo simple | 309 | **0,961** | 0,713 | <0,00025 | 70,2 % |
| Dirección nudo largo | 375 | **0,964** | 0,572 | <0,00025 | 74,7 % |
| Unión R/V | 431 | **0,909** | 0,570 | <0,00025 | 60,8 % |
| Terminación | 630 | **0,779** | 0,655 | <0,00025 | 11,6 % |
| Color | 631 | **0,563** | 0,379 | <0,00025 | 7,3 % |

Lectura: la torsión y la dirección de nudo son **constantes de objeto**, no variables de cuerda. Un quipu se hace de una sola vez, con un solo lote de hilado. Esto replica a Ascher (2005) con el corpus completo y con nulo explícito.

La pureza de la unión R/V (0,909 frente a 0,570) es alta pero **no es manufactura**: es un código de disposición (ver §3.6). La terminación y el color son los únicos rasgos con variación interna sustantiva.

### 3.2 La firma es un código corto y sus ejes son independientes

Los cuatro ejes discretos (torsión, dirección de nudo simple, unión, terminación) son **estadísticamente independientes**:

| Par | p | q (BH) |
|---|---|---|
| torsión × dir. nudo | 0,015 | 0,091 |
| torsión × unión | 0,094 | 0,281 |
| torsión × terminación | 0,637 | 0,764 |
| dir. nudo × unión | 0,193 | 0,386 |
| dir. nudo × terminación | 0,494 | 0,742 |
| unión × terminación | 0,895 | 0,895 |

Ninguna sobrevive a BH. Consecuencia cuantitativa: entre los 387 quipus con los cuatro ejes, **el 15,4 % de los pares comparte firma idéntica**. El valor esperado si los ejes fueran independientes con sus marginales es **15,6 %** (nulo, sd 0,0033; p = 0,59).

**Esto es el resultado negativo central:** una firma idéntica en los cuatro ejes no es evidencia de nada, porque ocurre exactamente a la tasa que predicen las marginales. Hay 19 de las 24 combinaciones posibles y las tres más frecuentes concentran el 61 % de los quipus.

### 3.3 ¿Talleres o manos? El clustering no los encuentra

- KMeans, k* = 5, silueta 0,227; nulo 0,185 ± 0,017 → **p = 0,030**. En la familia de 3 pruebas de estructura (silueta, vecino próximo, firma idéntica) el q de BH es 0,045: sobrevive por poco, pero la magnitud del efecto es pequeña.
- Distancia media al vecino más próximo: 0,0485 observada vs 0,0596 nula, **p = 0,0033**. Hay un exceso real de parejas parecidas, pero pequeño.
- Bootstrap: ARI = 0,63 ± 0,07 (cuerdas) y 0,80 ± 0,11 (quipus). Los clusters son reproducibles *dado el algoritmo*.
- **Pero los clusters no son de manufactura:** ARI entre cluster y cada eje = 0,017 (torsión), −0,014 (nudo), 0,027 (unión), 0,034 (terminación). Los clusters están definidos por **paleta y tamaño**: el cluster 0 (n = 26) tiene entropía de color 0,885 y 9,5 colgantes; el 1 (n = 46) es 65 % AB; el 2 (n = 46) es 81 % blanco; el 4 (n = 203) es el grupo grande y heterogéneo.
- Los clusters **cortan transversalmente las colecciones**: ARI con museo = 0,00; con región = −0,03; con prefijo = −0,02. No son un artefacto de transcripción, pero tampoco son "manos".
- El clustering jerárquico sobre distancia de Gower **no admite un corte equilibrado**: con k = 2 produce [1, 361]; con k = 5, [1, 2, 22, 106, 231]. Es encadenamiento típico de datos mixtos, no estructura discreta.

**Conclusión:** hay tipos de paleta reproducibles, pero **no hay evidencia de talleres/manos discretos** en los rasgos de manufactura. La estructura que se detecta es un gradiente dominado por color y tamaño, no grupos separados.

### 3.4 Fibra y grosor: la cobertura la decide el transcriptor, no el objeto

- **Fibra:** CN 28 951 cuerdas, CL 1 373 (2,5 %), sin dato 21 799 (40 %). La cobertura por quipu es **bimodal**: 47 % de los quipus tienen 0 % de cuerdas con fibra y 44 % tienen 100 %. No hay término medio: es un régimen de registro, no una propiedad física.
- La cobertura depende del transcriptor de OKR: `leah` 2 %, `tania` 20 %, `katie` 24 %, `gurton` 63 %, `cbrezine` 98 %, `julia` 100 %, `jclindaniel` 99,8 %.
- **Grosor:** 47 816 de 53 257 cuerdas (89,8 %) tienen grosor exactamente 0, y la tasa de ceros va del 74 % (`gurton`) al 100 % (`julia`, `jclindaniel`, `chandra`). `TWIST_ANGLE` es 0 en el 99,87 % de las cuerdas. **No es una medición utilizable.**
- **Canutos:** el OKR solo tiene detalle para 8 quipus (236 canutos); el resto es presencia/ausencia. Se remite a `t_canutos_fibra`: 179/650 quipus (27,5 %) con al menos un canuto, distribución bimodal.

Esto no invalida los análisis de fibra de `t_canutos_fibra` (que ya advirtió el sesgo), pero **impide usar fibra o grosor como firma de mano**: la variable "tiene dato de fibra" es en gran medida la variable "quién lo transcribió".

### 3.5 Incahuasi: los quipus relacionados comparten el *baseline del sector*, no una mano

Los 48 quipus del archivo de Incahuasi se dividen en dos bloques perfectos:

| Sector | Torsión S | Torsión Z | n |
|---|---|---|---|
| JC (Sector B) | 0 | 22 | 22 |
| UR (depósito/qolqawasi) | 26 | 0 | 26 |

Fisher exacto **p = 3,7 × 10⁻¹⁴**. La torsión dentro de Incahuasi **no separa manos: separa sectores**. Una vez fijado el sector, la torsión es constante y tiene poder discriminante cero (control en §4).

Los 7 quipus del sistema aritmético (UR266, UR269, UR270, UR273A, UR273B, UR275, UR278) son todos del sector UR, todos S, todos con nudo simple Z (0–0,8 % S), casi todos terminación K.

- Distancia de firma media de los 7: **0,274**; nulo de 7 quipus al azar de todo Incahuasi: 0,430; **p = 0,029**.
- Parece un "efecto de mano". **No lo es.** Restringiendo el nulo al sector UR (26 quipus), la distancia observada es 0,274 frente a 0,301 nula, **p = 0,29**; sin el eje unión, 0,175 vs 0,234, **p = 0,12**; solo torsión, **p = 1,00**. El efecto desaparece por completo.
- La razón del falso positivo es simple: los 7 están entre los más grandes del depósito, y en Incahuasi los grandes son S (mediana de colgantes: S = 107,5; Z = 11,0). La probabilidad de que los 7 sean S usando la tasa S de **su estrato de tamaño** es 0,20, no 0,009.

**Nivel: bien apoyado (negativo).** El sistema aritmético no muestra una firma de manufactura propia; comparte el baseline del depósito UR. No hay evidencia de que el "libro consolidado" (UR267A/B) haya sido hecho por otra mano que los parciales: UR267A/B no difieren de UR273, UR275 o UR278 en torsión, dirección de nudo ni terminación.

### 3.6 El hallazgo positivo: la unión R/V **codifica la parte**, no la mano

Dos parejas del sistema son la misma obra en dos volúmenes (A + B = consolidado, según `13_sistema_incahuasi`) y tienen la unión **opuesta y perfecta**:

| Pareja | Parte A | Parte B |
|---|---|---|
| UR273A / UR273B | pR = **0,000** (83/83 V) | pR = **0,991** (113/114 R) |
| UR267A / UR267B | pR = **0,000** (82/82 V) | pR = **1,000** (103/103 R) |

Esto coincide con la estructura interna: la unión R/V está **bloqueada a lo largo del quipu** (120 quipus mixtos; 77 con rachas significativamente agrupadas tras BH; rachas observadas 9,3 vs 20,9 esperadas; p < 0,0005 en cada uno) y con pureza por grupo 0,880 frente a 0,850 nula (86/462 quipus con q < 0,05). No marca la primera cuerda del grupo (R = 51,9 % en posición 1 vs 50,3 % en el resto).

**Interpretación (apoyada con datos, no bien apoyada):** R/V es un **código binario de disposición/partición** —probablemente la dicotomía hanan/hurín o parte A/B que propusieron Medrano y Urton (2018)— y **no un rasgo de manufactura**. Usarlo como "firma de mano" es inválido: dos partes de la misma obra, hechas para sumarse, llevan unión opuesta por diseño. Esto también explica por qué la unión "pura" es tan alta (0,909): un quipu bien hecho usa un solo código de unión en toda su extensión.

### 3.7 Copias: no comparten firma de manufactura

De `14_copias` se evaluaron **14 parejas de copia no redundantes** (se excluyen pares que comparten objeto, para no violar independencia; 9 de ellas tienen los cuatro ejes comparables):

- Firma idéntica en los 4 ejes: **1/9 (11 %)**, frente al 15 % del corpus. Con n = 9 la diferencia no es significativa: el resultado correcto es que **no hay exceso**, no que haya un déficit bien apoyado.
- Torsión coincide 13/13 (trivial: el 93 % de las cuerdas con dato del corpus es S).
- Dirección de nudo 9/13; terminación **13/14**; **unión 3/9** (P(X≤3 | Bin(9, 0,5)) = 0,25).
- El único par con firma idéntica es UR064/UR068.

**Nivel: apoyado con datos.** Las copias reproducen **contenido** (valores y, en parte, color: `14_copias` encontró color conservado por encima del azar, p = 7 × 10⁻⁵), pero **no reproducen la manufactura**. Eso es lo esperable si un escriba copia de un modelo sin tener el original delante: copia la información, no el objeto. No hay evidencia de que las copias las hiciera la misma mano; hay evidencia de que **no** comparten el gesto técnico. La coincidencia de terminación (13/14) es real pero poco informativa: la terminación K domina el corpus (79 % de los quipus) y las copias son casi todas K.

### 3.8 Dentro del quipu: bloques de unión y terminación, torsión sin cambios

| Rasgo | Quipus mixtos evaluables | Con rachas agrupadas (q < 0,05) | Rachas obs. | Rachas esp. |
|---|---|---|---|---|
| Unión R/V | 120 | **77** | 9,3 | 20,9 |
| Terminación | 314 | 27 | 11,8 | 13,7 |
| Torsión | 10 | 4 | 9,2 | 14,0 |

Cambio de régimen por máximo TV en colgantes: unión 74/211 con q < 0,05 (TV 0,425 vs 0,225 nula); terminación 34/409; **torsión 0/86**.

La firma **por grupo** confirma el mismo reparto: pureza ponderada dentro de grupo frente a nulo intra-quipu → color 0,637 vs 0,596 (148/460 quipus con q < 0,05), unión 0,880 vs 0,850 (86/462), terminación 0,814 vs 0,792 (70/460), **torsión 0,994 vs 0,992 (0/460)**. Es decir: el color y la unión se organizan por grupos de colgantes (son códigos de disposición); la torsión no se organiza por nada porque es constante en todo el objeto.

- La **torsión nunca cambia** dentro de un quipu (0/86 tras BH). No hay evidencia de cuerdas añadidas con otro hilado.
- La **unión y la terminación sí se segmentan**, pero en bloques que coinciden con la disposición del registro, no con reparaciones.
- **Notas de reparación/empalme/añadido:** 134 cuerdas en 52 quipus. No se asocian a mayor mezcla de torsión; el efecto va en dirección **contraria** (Mann-Whitney p = 0,087; los quipus con nota están *menos* mezclados). Las "reparaciones" anotadas por los catalogadores no dejan huella detectable en la firma.

**Nivel: bien apoyado (descriptivo) para la torsión; apoyado con datos para la segmentación de unión/terminación.**

### 3.9 Respuesta directa a "¿quién hacía qué registros?"

Con estos datos, **no se puede asignar registros a personas**. Lo que sí se puede afirmar:

- Cada quipu es el producto de **un lote de producción** (torsión y dirección de nudo constantes). Ese lote pudo ser una persona o un taller; el dato no distingue.
- La variación de manufactura que existe entre quipus va por **colección/sector/tradición** (Incahuasi JC vs UR; Armatambo vs resto; quipus grandes vs pequeños), no por individuos dentro de una misma colección.
- El único "quién" directamente observable en la base es **quién transcribió** el quipu al OKR/KFG (fibras, grosores, colores), y ese quién contamina varias variables.
- El reparto de trabajo que sugiere la cultura material es, como mucho, **entre tradiciones locales de hilado** (S vs Z), no entre escribas identificables.

---

## 4. Controles

1. **Nulo de pureza entre quipus** (conserva tamaños y marginal). Sin él, la pureza del 99 % sería trivial.
2. **Nulo de independencia de rasgos** para el clustering y para la firma idéntica. Es el control que mata la interpretación "misma firma = misma mano".
3. **Control de tamaño:** en Incahuasi la torsión correlaciona con el número de colgantes (S: mediana 107,5; Z: 11,0). El "los 7 son todos S" pasa de p = 0,009 a p = 0,20 al condicionar por estrato de tamaño.
4. **Control de sector:** el nulo de los 7 relacionados restringido a UR elimina el efecto (p = 0,29).
5. **Control de transcriptor:** `CREATED_BY` de OKR. 37 de los 49 quipus con torsión Z los transcribió `jclindaniel` (los 22 JC de Incahuasi y los 14 del Museo Nacional/Pueblo Libre, es decir Armatambo). La fibra se registra en el 2 %–100 % de las cuerdas según quién transcribió. El grosor es 0 en el 74 %–100 % según quién transcribió. **Cualquier "efecto de fibra/grosor" no controlado por transcriptor es sospechoso.**
6. **Control de prefijo:** AS/UR/JC/HP/KH no explicó los clusters (ARI ≈ 0), pero sí estructura la torsión (JC = Z en Incahuasi; AS/UR en el resto).
7. **No redundancia en copias:** se deduplicaron las parejas que comparten objeto (de 19 a 14), porque el mismo quipu en dos pares infla la significación.
8. **BH-FDR** por familia en todas las tablas de pruebas múltiples.

---

## 5. Resultados negativos (explícitos)

1. **No hay talleres/manos discretos.** Silueta 0,227 vs 0,185 nula (p = 0,030; q = 0,045 en su familia), pero los clusters están definidos por color y tamaño, no por manufactura, y no hay corte jerárquico equilibrado. El exceso de parejas parecidas es real pero pequeño (vecino próximo 0,0485 vs 0,0596; p = 0,0033).
2. **La firma idéntica no identifica nada:** 15,4 % observado vs 15,6 % esperado por marginales independientes (p = 0,59).
3. **La fibra no es usable como firma:** cobertura 0 %/100 % por quipu, decidida por el transcriptor.
4. **El grosor no es usable:** 89,8 % de ceros; `TWIST_ANGLE` 99,87 % de ceros.
5. **Los quipus relacionados de Incahuasi no comparten una mano detectable:** el efecto bruto (p = 0,029) desaparece al controlar por sector (p = 0,29). El libro consolidado no difiere de los parciales.
6. **Las copias no comparten manufactura:** 1/9 comparables con firma idéntica (11 %), sin exceso sobre el 15 % base (n = 9: no significativo).
7. **Las reparaciones anotadas no dejan huella** en la heterogeneidad de torsión (p = 0,087, dirección contraria).
8. **La torsión no cambia dentro del quipu** (0/86 cambios de régimen tras BH).

**Limitaciones.** (a) La firma se reduce a 4 ejes gruesos porque el KFG no registra número de cabos (ply) ni grosor utilizable; el OKR sí tiene `TWIST`, pero no distingue ply. (b) Solo 387 quipus tienen los 4 ejes y 362 entran en el clustering; dentro de Incahuasi, el sector UR tiene 26 quipus, que es el mínimo para plantear un test de 2–3 manos. (c) "Misma mano" no es observable sin una agrupación externa validada (mismo hallazgo, misma tumba, misma fecha); la firma solo puede refutar, no confirmar, una atribución de autor.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Cada rasgo de manufactura es constante dentro del quipu (torsión 99,5 % de pureza; 93,4 % de quipus 100 % puros) | **Bien apoyado (descriptivo)** |
| Los cuatro ejes discretos son independientes y la firma idéntica ocurre a la tasa de las marginales | **Bien apoyado (descriptivo)** |
| La unión R/V está bloqueada y marca la parte A vs B en las dos parejas del sistema de Incahuasi (UR273A/B, UR267A/B) | **Bien apoyado (descriptivo);** su lectura como hanan/hurín es **apoyada con datos** |
| La torsión separa sectores/colecciones (JC vs UR en Incahuasi, p = 3,7 × 10⁻¹⁴), no individuos | **Bien apoyado (descriptivo)** |
| Fibra y grosor no son utilizables como firma por sesgo de registro | **Bien apoyado (descriptivo)** |
| No hay talleres/manos discretos detectables en la firma | **Apoyado con datos** |
| Las copias no comparten manufactura | **Apoyado con datos** |
| El sistema aritmético de Incahuasi comparte baseline de sector, no mano | **Apoyado con datos** (negativo) |
| La torsión S/Z marca tradiciones regionales/étnicas de hilado | **Propuesto** |
| UR262 es "un solo taller/mano" (k_UR262) | **Propuesto**: demuestra un solo *lote* (490 cuerdas 100 % S), no una persona; el 93,4 % de los quipus del corpus son igual de puros |

---

## 7. Para el coordinador

- **La manufactura no identifica manos, identifica lotes.** Cada quipu es internamente homogéneo (torsión 99,5 % pura; 93,4 % con un solo valor en todas sus cuerdas) y esa homogeneidad es la norma del corpus, no una excepción: no se puede inferir "un solo artesano" de un objeto uniforme.
- **La firma de 4 ejes no tiene poder identificador.** Los ejes son independientes y el 15,4 % de los pares del corpus comparte firma idéntica, exactamente lo que predicen las marginales (15,6 %; p = 0,59). Dos quipus con la misma firma no son más que dos quipus sacados de la misma urna.
- **El clustering produce tipos de paleta, no talleres.** k = 5 con silueta 0,227 frente a 0,185 nula (p = 0,030; q = 0,045, justo en el límite); los clusters se definen por color y tamaño (ARI con los ejes ≈ 0) y cortan transversalmente museos y regiones (ARI ≈ 0). No hay grupos discretos.
- **El mejor hallazgo es negativo y limpio en Incahuasi.** Los 7 quipus del sistema aritmético parecen compartir firma (p = 0,029), pero el efecto desaparece al comparar solo dentro del sector UR (p = 0,29): comparten el baseline del depósito, no una mano. El libro consolidado UR267A/B no difiere de los parciales.
- **Hallazgo positivo inesperado:** la unión R/V es un **código**, no manufactura. UR273A es 100 % V y UR273B 99 % R; UR267A es 100 % V y UR267B 100 % R. Las dos mitades de la misma obra llevan unión opuesta por diseño. Esto respalda la hipótesis R/V = partición (Medrano-Urton) y **invalida la unión como firma de mano**.
- **Las copias se copiaron, no se recrearon con la misma mano:** 1/9 comparables con firma idéntica (11 %, por debajo del 15 % base); la unión coincide solo 3/9. Copian contenido y parte del color, no el gesto técnico. Es consistente con escribas distintos trabajando de un modelo.
- **Aviso de datos:** fibra (40 % sin dato, cobertura 0/100 % por quipu) y grosor (89,8 % de ceros) están decididos por el transcriptor (`leah` 2 % vs `julia` 100 % de fibra). No usar ninguna de las dos como variable de objeto sin controlar `CREATED_BY`.
- **Dentro del quipu** la torsión nunca cambia (0/86 cambios significativos): no hay cuerdas añadidas con otro hilado. La unión y la terminación sí se segmentan en bloques (unión: 77/120 quipus), pero eso es disposición, no reparación; las notas de reparación no se asocian a heterogeneidad (p = 0,087).
- **Recomendación:** para buscar "manos" hay que salir de los rasgos de manufactura y usar **combinaciones de contenido + color + geometría** dentro de una misma colección con n grande (Incahuasi UR tiene 26 quipus, suficiente para un test de 2–3 manos; el corpus entero no). Y hay que separar siempre el efecto sector/colección del efecto individuo.
- **No repetir** el error de leer "100 % S" como "una mano": en Incahuasi eso solo identifica el depósito UR, y en el corpus identifica grandes quipus y la tradición Armatambo/Pueblo Libre.
