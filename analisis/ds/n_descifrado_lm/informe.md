# Desciframiento por tanteo controlado de quipus no numéricos

**Equipo:** `n_descifrado_lm` · **Fecha:** 18 de octubre de 2026 · **Semilla:** 20261018
**Datos:** `analisis/datos/cuerdas.csv` (57 818 filas, deduplicadas a 57 809); OKR `khipu.db` no modificado.
**Candidatos:** UR179, UR180, UR178, UR050, UR054, UR052, AS076, JC012, UR203, UR215. **Controles numéricos:** UR278 y UR266 (Incahuasi).
**Scripts:** `01_corpus.py`, `01b_aymara.py`, `lm_utils.py`, `decipher.py`, `02_secuencias.py`, `03_descifrado.py`, `04_positivo.py`, `04b_potencia.py`, `05_langstats.py`, `06_analisis.py`, `07_estabilidad.py`, `08_busqueda_intensa.py`.
**Salidas:** `resultados.csv`, `resultados_consolidados.csv`, `resultados_aymara.csv`, `langstats.csv`, `control_positivo.csv`, `potencia.csv`, `alfabetos.csv`, `estabilidad.csv`, `busqueda_intensa.csv`, `corpus/`.

---

## 1. Pregunta

¿Algún quipu no numérico —o alguno de sus alfabetos candidatos de signo por cuerda— admite una asignación signo → sílaba que se parezca a lengua quechua/aymara **más de lo que permiten los controles negativos**, con la misma potencia de búsqueda y corrección por comparaciones múltiples?

El encargo exige explícitamente no presentar ninguna "lectura" que no supere los controles. El diseño, por tanto, se organizó alrededor de tres trampas conocidas:

1. **El inventario.** Un silabario quechua tiene ~60–120 sílabas. Si el alfabeto del quipu tiene 5 signos, no puede escribir lengua, y ninguna optimización lo arregla.
2. **La búsqueda libre siempre mejora.** Elegir la asignación que maximiza la verosimilitud hace que *cualquier* secuencia con estructura de orden (banding, decimalidad, tally) parezca "lengua" frente a un nulo que solo baraja. El nulo correcto no es el barajado, sino **lengua real con el mismo alfabeto y la misma marginal**.
3. **Identificabilidad.** Con n cuerdas y V signos, si n/V es pequeño, la clave no es identificable ni aunque la secuencia sea lengua de verdad. Eso hay que medirlo, no suponerlo.

---

## 2. Método

### 2.1 Alfabetos candidatos (definidos *a priori*)

Un alfabeto asigna un signo a cada cuerda; la secuencia son las cuerdas de nivel 0 en orden `orden` (izquierda→derecha, el orden de lectura del KFG). Se definieron siete antes de mirar ninguna verosimilitud:

| Alfabeto | Signo por cuerda | V en los 12 quipus |
|---|---|---|
| A1 color | color canónico: componentes básicos ordenados, sin rangos de posición | 1–16 |
| A2 color+torsión | color ∥ S/Z/U | 1–16 |
| A3 color+unión | color ∥ R/V/T/U | 1–16 |
| A4 color+fibra | color ∥ canuto ∥ terminación (la fibra no está en `cuerdas.csv`) | 1–29 |
| A5 nudo | nº de nudos + patrón de tipos (`4SSSS`) | 2–46 |
| A6 color+nudo | color ∥ patrón de nudos | 2–80 |
| A6-micro | cada nudo como signo (tipo+nº+dirección), `\|` entre cuerdas | 4–25 |

El inventario se midió también en **toda la clase limpia de 56 quipus** de `n_no_numericos` (§3.1).

### 2.2 Corpus y modelo de lengua

- **Quechua colonial (primario):** texto quechua del manuscrito de Huarochirí (ed. Arguedas, c. 1600), separado de la traducción española por densidad de palabras-función y ausencia de vocales acentuadas. **16 264 sílabas, 592 tipos.**
- **Aymara (auxiliar):** 615 líneas de la Wikipedia aymara filtradas por funcionales. **24 167 sílabas, 920 tipos.**
- **Quechua moderno (robustez):** Wikipedia quechua, 119 573 sílabas.

La *Doctrina Christiana* de 1584 se descargó (`corpus/doctrina1584.txt`, 249 KB), pero su OCR está a dos columnas intercaladas quechua/aymara y no se puede separar sin alineación manual; se descartó y se documenta. El aymara es, por tanto, un corpus auxiliar moderno, no colonial.

Silabificación ortográfica CV(C) con dígrafos (`ch`, `ll`, `rr`, `sh`) y `hu`/`qu` como onset. Modelo **bigrama de sílabas sobre el flujo continuo**, vocabulario K = 120 sílabas más frecuentes, suavizado add-0,1. K = 120 mantiene el problema comparable a un silabario real y garantiza V ≤ K.

### 2.3 Búsqueda

Para cada (quipu, alfabeto) se busca la **función inyectiva** signo → sílaba que maximiza

  logL = Σ_t log P(f(s_t) | f(s_{t−1}))

por recocido simulado (4 reinicios × 2 500 iteraciones; movimientos de intercambio y de reasignación a sílaba libre). Se reporta **logL por signo**. Los controles usan el mismo presupuesto.

### 2.4 Controles

1. **Nulo de barajado:** 60 permutaciones de la misma secuencia (preserva la marginal, destruye el orden); p empírico = fracción con logL ≥ observado.
2. **Calibración de lengua (el control decisivo):** 20 réplicas de **texto quechua real comprimido a V clases con la misma distribución marginal de signos que el quipu**. Si la secuencia fuera lengua con ese alfabeto, ¿qué verosimilitud produciría? Un desciframiento genuino debe caer **dentro** de esa distribución (0,05 < p < 0,95), no por encima.
3. **Quipus numéricos de Incahuasi (UR278, UR266)** leídos con los mismos alfabetos.
4. **Secuencias aleatorias** con la misma distribución (equivalentes al barajado) y **secuencias rígidas** (periódicas) como referencia.
5. **Control positivo:** texto quechua real cifrado con clave aleatoria (biyectiva y many-to-one), misma búsqueda; se mide la fracción de la clave recuperada.
6. **Corrección múltiple:** BH-FDR por familia sobre las 84 configuraciones y sobre las 60 secuencias únicas (A1/A2/A3 suelen coincidir cuando la torsión o la unión son constantes).

### 2.5 Estadísticos sin asignación

Entropía condicional H(siguiente|anterior) en bits con corrección de Miller-Madow, entropía normalizada, pendiente de Zipf y tasa de repetición adyacente, comparadas con 200 barajados y 200 réplicas de lengua real **con la misma marginal y la misma longitud** (`05_langstats.py`). La comparación a igual n es esencial: el estimador de H está muy sesgado hacia abajo con n pequeño y no se puede comparar un quipu de 18 cuerdas con un corpus de 16 000 sílabas.

---

## 3. Resultados

### 3.1 El inventario es demasiado pequeño para un silabario (resultado a priori)

En la clase limpia de 56 quipus no numéricos (54 con ≥ 8 cuerdas analizables), el alfabeto de color por quipu tiene **mediana V = 5 y máximo V = 19**; con el color exacto (sin canonicalizar), mediana 5 y **máximo 39**. **Ningún quipu de la clase alcanza V ≥ 40**, y menos aún las 60–120 sílabas de un silabario quechua.

En los 12 quipus analizados, V mediano por alfabeto va de 3 (color) a 10 (A6-micro); solo **4 de 84** configuraciones alcanzan V ≥ 40 (UR203 A5 = 46 y A6 = 80; UR215 A6 = 45; UR266 A6 = 46).

**Consecuencia lógica:** en 80 de 84 configuraciones el alfabeto **no puede representar un silabario**. Cualquier "lectura" sería un código de 2–20 símbolos, no una escritura silábica.

### 3.2 Verosimilitud: el nulo de barajado mide rigidez, no lengua

| Alfabeto | V mediana | logL/signo obs | nulo barajado | lengua calibrada |
|---|---:|---:|---:|---:|
| A1 color | 3 | −2,39 | −2,52 | −2,51 |
| A5 nudo | 7,5 | −2,83 | −2,91 | −2,89 |
| A6 color+nudo | 9,5 | −3,04 | −3,16 | −3,10 |
| A6 micro | 10 | −3,08 | −3,23 | −3,19 |

El observado supera al barajado en **35/84** configuraciones (q < 0,05; 25/60 secuencias únicas tras BH). Pero el mismo estadístico es **máximo en los quipus numéricos**: UR278 A1-color da z = **+14,4** frente a su nulo, UR255 A6-micro z = +9,9 y UR266 A6-micro z = +7,3. Es decir, la prueba de permutación detecta que las secuencias de cuerdas tienen orden (banding, seriación, decimalidad), **no** que sean lengua. Un quipu numérico "descifra" mejor que cualquier candidato no numérico: el máximo de los candidatos es z = +4,9 (UR050 A6-micro).

**Comparación directa con la referencia numérica** (18 quipus decimales, 6 de Incahuasi + 12 aleatorios; `referencia_numerica.csv`). `p_vs_numerico` = fracción de quipus numéricos con exceso sobre el barajado ≥ el del candidato, mismo alfabeto. La mediana en los candidatos es **0,72** y **ningún candidato baja de 0,056**: ninguno es siquiera tan rígido como los numéricos, y ninguno se separa de ellos en la dirección de la lengua.

### 3.3 Calibración contra lengua real

Posición de cada configuración en la distribución de lengua real con la misma marginal:

| Lado | n configs |
|---|---:|
| Por encima del rango de lengua (más rígido que lengua) | 33 |
| Dentro del rango de lengua | 40 |
| Por debajo (menos estructura que lengua) | 11 |

Estar "dentro" no es evidencia positiva: es no ser distinguible de lengua en una muestra minúscula. El criterio conjunto —(i) estructura de orden significativa frente al barajado, (ii) verosimilitud dentro del rango de lengua, (iii) V ≥ 40— lo cumplen **0 de 84 con el modelo quechua colonial**. Con modelos alternativos pasan **2/84 (aymara) y 3/84 (quechua moderno)**: en ambos, UR203 A5-nudo; además UR215 A6-color+nudo (aymara) y UR203 A6-color+nudo + el numérico UR266 A6-color+nudo (quechua moderno). Ninguno de ellos tiene asignación estable (§3.6), así que son no-rechazos, no desciframientos. Sin la condición V ≥ 40, solo 2 configuraciones pasan (i)+(ii): JC012 A6-micro (V = 4) y el numérico UR278 A6-micro (V = 21).

**Un resultado metodológico central:** la distribución de lengua calibrada y la de barajados son casi indistinguibles. La diferencia estandarizada media es **d = 0,17** (máx. 1,75; solo 5/84 con d > 1). Es decir, **a estas longitudes el método no separa lengua de ruido**: ambas alcanzan casi el mismo techo de verosimilitud porque el optimizador tiene libertad sobrada para encajar cualquier secuencia en los bigramas más probables. Cualquier p-valor de este método con n < 300 y V > 10 es, por construcción, poco informativo.

### 3.4 Entropía condicional: por debajo de la lengua en todos los casos no degenerados

H(siguiente|anterior) de las secuencias de quipu, comparada con lengua real de la misma marginal y longitud:

| Alfabeto | H quipu | H lengua calibrada | z vs barajado |
|---|---:|---:|---:|
| A1 color | 0,81 | 1,17 | −13,0 |
| A5 nudo | 1,67 | 1,75 | −2,6 |
| A6 color+nudo | 1,51 | 1,79 | −4,8 |
| A6 micro | 1,81 | 2,18 | −16,1 |

En las 58 configuraciones con V ≥ 4, **el 93 % tiene H menor que la lengua calibrada** (mediana de la razón H/H_lengua = 0,85; en los quipus numéricos = 0,77) y el 93 % cae por debajo del percentil 0,5 de la distribución de lengua. Las excepciones son casos de n muy pequeño (AS076 A5, n = 15, percentil 0,875), donde el estimador tiene un error enorme. Las configuraciones con percentil 1,0 son V = 1–2 con marginal casi constante (p. ej. UR050, repetición adyacente 0,99), donde la "coincidencia" es trivial.

**Lectura:** las secuencias de cuerdas son *más predecibles* que la lengua al mismo tamaño de alfabeto. Es la firma de un código rígido (banding, decimalidad, tally), no de un texto.

### 3.5 Potencia del método: qué se puede y qué no se puede concluir

Control positivo con texto quechua real y clave biyectiva aleatoria, **al presupuesto usado en los quipus** (4 reinicios × 2 500 iteraciones):

| n | V | precisión de la clave (media) | z vs barajado |
|---:|---:|---:|---:|
| 30 | 21–25 | 0,03 | 0,3 |
| 60 | 35–45 | 0,02 | 1,1 |
| 100 | 41–60 | 0,04 | 1,0 |
| 164 | 62–77 | 0,02 | 1,0 |
| 298 | 69–104 | 0,04 | 1,9 |

(El NMI por token es trivialmente 1 porque el cifrado es biyectivo y la partición se conserva; por eso se reporta la precisión de la clave. Detalle en `control_positivo.csv`.)

Con ese presupuesto el método **no recupera la clave ni cuando la secuencia es literalmente lengua quechua cifrada**. Pero un presupuesto 5–10× mayor sí la recupera (`04b_potencia.py`, texto generado por el modelo restringido a V sílabas):

| V | n | tokens/signo | precisión (20×15 000, 3 réplicas) |
|---:|---:|---:|---:|
| 5 | 500 | 100 | 0,33 (1 de 3) |
| 10 | 1 000 | 100 | 0,97 |
| 20 | 1 000 | 50 | 0,48 |

**Interpretación honesta:** el método es válido —recupera el 97 % con V = 10 y n = 1 000— pero **necesita un orden de magnitud más de datos que los quipus**. Además, con V = 5 falla 2 de 3 veces aunque la clave existe: en esos fallos, el mapeo recuperado tiene **mayor** verosimilitud que la clave verdadera (−1397 vs −1423), es decir, el modelo de lengua actúa como un prior imperfecto y el óptimo de verosimilitud no es la clave. Esto refuerza que una "lectura" óptima no puede interpretarse sin validación externa. Los quipus tienen n/V entre 1,4 y 82 (mediana 9,1; p10–p90 = 3–53); incluso los mayores (UR203: 113 cuerdas, V = 46–80) están en el régimen donde una clave verdadera apenas se insinúa. Por tanto, el resultado negativo **no prueba que no haya lengua**: prueba que no es identificable con estos datos y este método. Lo que sí es concluyente es el tamaño del inventario y la rigidez de las secuencias.

Con búsqueda intensiva (20 × 15 000) en los mejores candidatos (`busqueda_intensa.csv`), UR203 A5 y A6-micro y UR215 A6-color+nudo pasan a ser significativos frente al barajado (p = 0,000, logL/s ≈ −3,4 vs −3,6), pero siguen sin superar el criterio conjunto: su H condicional es menor que la de lengua y su asignación no es estable (§3.6).

### 3.6 Estabilidad: el acuerdo entre mitades es exactamente el del azar

Desciframiento independiente de las dos mitades del mismo quipu, mismo método (`estabilidad.csv`). El azar relevante es 1/V (el óptimo usa del orden de V sílabas), no 1/K:

| Quipu | Alfabeto | Signos comunes | Acuerdo | Azar 1/V |
|---|---|---:|---:|---:|
| UR203 | A5 nudo | 14 | 0,07 | 0,071 |
| UR203 | A6 color+nudo | 9 | 0,11 | 0,111 |
| UR215 | A6 color+nudo | 7 | 0,00 | 0,143 |
| UR050 | A6 micro | 11 | 0,09 | 0,091 |
| AS076 | A5 nudo | 2 | 0,50 | 0,500 |
| UR179 | A5 nudo | 5 | 0,20 | 0,200 |
| UR052 | A5 nudo | 6 | 0,00 | 0,167 |
| UR278 | A5 nudo | 8 | 0,00 | 0,125 |

En **6 de 8 casos el acuerdo es exactamente 1/V** y en los otros 2 está por debajo. Las dos mitades producen asignaciones estadísticamente independientes: no hay ninguna lectura reproducible.

### 3.7 Robustez al modelo de lengua

Se repitió el análisis completo de las 84 configuraciones con el modelo aymara (`resultados_aymara.csv`) y con el quechua moderno (`resultados_quechua_wiki.csv`). La correlación de rangos de logL/signo con el modelo colonial es **ρ = 0,95** en ambos casos (p de barajado: ρ = 0,64 y 0,80). La diferencia lengua–barajado media es d = 0,28 (aymara) y 0,72 (quechua moderno), frente a 0,17 (colonial): cuanto mejor es el modelo, algo más separa lengua de ruido, pero sigue siendo poca. Las conclusiones no dependen del corpus: el problema es el tamaño de los datos y de los alfabetos, no la elección de la lengua.

---

## 4. Controles, amenazas y explicaciones aburridas

1. **El nulo de barajado no es el nulo de "lengua".** Preserva solo la marginal; cualquier rigidez lo supera. Por eso el resultado principal se apoya en la calibración contra lengua real con marginal pareada y en la entropía condicional, no en el p de barajado.
2. **La calibración tiene su límite:** comprimir lengua real a V clases preserva la estructura bigrama pero no es "texto real con V símbolos". Por eso se añadió el control positivo biyectivo, que confirma la falta de potencia.
3. **El modelo de lengua es colonial y pequeño** (16 000 sílabas). Se replicó con aymara y con quechua moderno; los rankings son casi idénticos (ρ = 0,95).
4. **La silabificación ortográfica es tosca:** no distingue aspiradas/glotalizadas ni la fonología colonial. Un modelo más fino cambiaría valores absolutos, no el tamaño del inventario ni la falta de potencia.
5. **Transcripción:** los candidatos están en OKR y su composición coincide con KFG (informe `n_no_numericos`), pero ambos comparten en parte el mismo registro de campo.
6. **No circularidad:** los alfabetos usan atributos de cuerda (color, torsión, unión, nudos), no el valor decimal ni el índice de anomalía que definió la clase.
7. **Múltiples comparaciones y redundancia:** 84 configuraciones, muchas idénticas (A1/A2/A3 cuando torsión y unión son constantes). Se corrigió por BH sobre las 84 y sobre las 60 únicas; ninguna conclusión positiva sobrevive.
8. **Presupuesto de búsqueda:** el negativo principal (0/84) se obtuvo con 4×2 500. Con 20×15 000 algunos candidatos pasan el test de barajado, pero no el conjunto (inventario, entropía, estabilidad). Se reporta para no exagerar el negativo.

---

## 5. Resultados negativos (explícitos)

1. **Ningún quipu ni alfabeto pasa el criterio conjunto** (orden significativo + verosimilitud dentro del rango de lengua + V ≥ 40) **con el modelo primario: 0/84**. Con modelos alternativos pasan 2–3/84 (UR203, UR215 y el numérico UR266), pero ninguno tiene asignación estable entre mitades: son no-rechazos, no lecturas.
2. **El inventario es 1–2 órdenes de magnitud menor que un silabario:** mediana V = 5 (color) en la clase de 56; máximo 39 con color exacto; ningún quipu de la clase llega a 40.
3. **El test de barajado da positivo en 35/84, pero también —y más fuerte— en los quipus numéricos** (UR278 z = +14,4; UR255 z = +9,9). Ningún candidato es tan rígido como ellos (`p_vs_numerico` ≥ 0,056; mediana 0,72). No es evidencia de lengua.
4. **La entropía condicional de los quipus es menor que la de lengua** en el 93 % de las configuraciones con V ≥ 4 (razón mediana H/H_lengua = 0,85; 0,77 en los numéricos). Son más rígidos, no más lingüísticos.
5. **La calibración de lengua y el barajado son casi indistinguibles** (d = 0,17): el método no separa lengua de ruido a estas longitudes.
6. **El control positivo no recupera la clave al presupuesto usado** (precisión 0,02–0,04; máx. 0,17). Con 10× más búsqueda la recupera en buena medida (97 % con V = 10, n = 1 000; ~50 % con V = 20), lo que demuestra que el método es válido pero los datos son insuficientes.
7. **No hay asignación estable entre mitades** (acuerdo = 1/V en 6/8 casos).
8. **UR203/UR215, los de mayor inventario, no muestran una estructura compatible con lengua:** su H condicional es menor que la calibrada y su asignación split-half es independiente.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| El inventario de signos por cuerda de la clase no numérica es 1–19 colores (mediana 5) y nunca ≥ 40 | **Demostrado** (conteo directo, independiente del modelo) |
| Ningún quipu/alfabeto supera el criterio conjunto de desciframiento con el modelo primario | **Demostrado** para este método y este corpus (0/84); 2–3/84 con modelos alternativos, sin estabilidad |
| Las secuencias de cuerdas son más rígidas que la lengua (H condicional menor) | **Apoyado con datos** (z = −2,6 a −53; 200 réplicas) |
| El estadístico de barajado mide rigidez y no lengua | **Apoyado con datos** (los numéricos son los más extremos) |
| El método no identifica una clave a n ≤ 300 con V ≈ 20–80 | **Apoyado con datos** (control positivo y curva de potencia) |
| Los quipus no numéricos son tally/etiqueta y no narrativa | **Propuesto** (consistente con este informe y con `n_no_numericos`; no probado aquí) |
| Algún quipu contenga un texto silábico que este método no puede recuperar | **Especulativo / no refutado** — es la limitación principal |

---

## 7. Para el coordinador

- **No hay ninguna lectura, y el negativo está bien acotado:** 0 de 84 combinaciones (12 quipus × 7 alfabetos) pasa el criterio conjunto con el modelo primario. Con modelos alternativos pasan 2–3 (UR203 A5/A6, UR215 A6 y el numérico UR266), pero ninguna tiene asignación estable: son no-rechazos, no lecturas. No se presenta ninguna "traducción".
- **El hallazgo más contundente es a priori y no depende de ningún modelo:** el alfabeto de color por quipu de la clase no numérica tiene mediana 5 y máximo 19 signos (máximo 39 con color exacto). Un silabario quechua necesita 60–120. La mayoría de estos quipus **no puede** ser escritura silábica.
- **La prueba de barajado es una trampa:** da p < 0,05 en 35/84 configuraciones, pero el máximo lo alcanza el quipu numérico UR278 (z = +14,4) y UR255 (z = +9,9); el mejor candidato solo llega a z = +4,9 y ninguno es tan rígido como los numéricos (`p_vs_numerico` ≥ 0,056). Mide rigidez (banding, decimalidad), no lengua. Cualquier informe que se apoye solo en "logL supera al azar" se está autoengañando.
- **La calibración correcta (lengua real con la misma distribución de signos) sitúa a 33/84 configuraciones por encima del rango de lengua** —más deterministas que un texto— y a 40 dentro, pero "dentro" es indistinguibilidad con n minúscula: la diferencia media entre lengua calibrada y barajado es d = 0,17, casi nula. El test no separa lengua de ruido a estas longitudes.
- **La entropía condicional confirma la rigidez:** en el 93 % de las configuraciones con V ≥ 4, los quipus tienen H menor que la lengua de la misma longitud y marginal (razón mediana 0,85; 0,77 en los numéricos). No son textos: son códigos.
- **El control positivo marca el límite de lo concluyente:** al presupuesto usado, un cifrado verdadero de texto quechua no se recupera (precisión 0,02–0,04). Con 10× más búsqueda se recupera el 97 % con V = 10 y n = 1 000, pero solo ~50 % con V = 20 y a veces el óptimo de verosimilitud no es la clave verdadera. Por tanto no se puede afirmar "no hay lengua"; solo "no es identificable con estos datos".
- **UR203 y UR215, los de mayor inventario (45–80 signos), no muestran una lectura estable:** el acuerdo entre mitades es exactamente el del azar (1/V). Su aparente compatibilidad con lengua es indistinguibilidad de ruido.
- **Recomendación 1 (barata y decisiva):** no invertir más en desciframiento sustitutivo con n < 300. El siguiente paso con posibilidades reales es concatenar secuencias del mismo género (por grupo/posición/colección) hasta n > 1 000, o modelar la jerarquía madre–subsidiaria como gramática en vez de como secuencia plana.
- **Recomendación 2:** si se insiste en lo silábico, el único objeto con inventario suficiente es UR203/UR215; hay que auditar primero si sus 45–80 "signos" son morfologías reales o variantes de daño/transcripción.
- **Recomendación 3:** el resultado positivo de `n_no_numericos` (tally/unario, canutos, fibra animal) es el marco más plausible; este informe lo refuerza al mostrar que las secuencias son más rígidas que la lengua y que su alfabeto es demasiado pequeño para escribir.
