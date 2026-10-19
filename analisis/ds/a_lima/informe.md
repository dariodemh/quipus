# Monografía del archivo de quipus de la costa central de Lima

**Equipo:** `analisis/ds/a_lima`
**Fecha:** 2026-10-17
**Datos:** `analisis/datos/{cuerdas,quipus,grupos}.csv` (Khipu Field Guide, 651 quipus) + `data/external/data-science-khipu-article` (sumas Ascher) + `docs/fichas`, `docs/estado_del_arte.md`.
**Scripts:** `01_cohorte.py` … `13_posicional_bh.py` (misma carpeta). Todos reproducibles, semilla 0.

---

## 0. Pregunta y método

**Pregunta.** ¿Qué caracteriza al conjunto de quipus de la costa central de Lima (Armatambo, Huaquerones, near Lima, Chancay, Huacho, Chuquitanta, Marquez)? ¿Hay relaciones internas que permitan reconstruir un archivo (quipus de detalle vs. de resumen) y proponer qué se registraba?

**Cohorte.** Quipus de `quipus.csv` cuya `procedencia` contiene `Armatambo|Huaquerones|near Lima|Chancay|Huacho|Chuquitanta|Marquez` → **63 quipus, 3 284 cuerdas**. Se añadió una etiqueta normalizada `sitio` (agrupa variantes: "Armatambo, Lima" = Armatambo; "Huando" = Chancay; "Huaura Valley, near Lima" = near Lima; "Costa Central, Huacho"/"Huacho?" = Huacho). Reparto: Huaquerones 19, Armatambo 14, Huacho 7, Chancay 7, Marquez 6, near Lima 6, Chuquitanta 4.

**Unidad de análisis:** el quipu (regla 1). Los contrastes intra-quipu usan permutaciones **dentro** de cada quipu.

**Control de "dos nombres del mismo objeto".** Los 63 quipus tienen **63 números OKR distintos**: no hay un objeto contado dos veces. `UR1124` y `UR1124_Detail_1` son el mismo objeto físico (cuerpo + detalle fotográfico): `UR1124_Detail_1` se excluye de los contrastes entre quipus (quedan 62 quipus, 1 891 pares).

**Nulos.** Nulo principal: barajar los valores (o colores) **dentro de cada quipu**, 500 iteraciones, semilla 0 (preserva el vocabulario de valores de cada quipu, rompe el orden). Donde el estadístico es invariante a la permutación (pertenencia a conjuntos) se usa un **nulo de pool** (reasignación global de valores conservando nº de cuerdas por quipu) y se dice explícitamente. Corrección múltiple: **BH-FDR**. Nivel de evidencia etiquetado en cada conclusión.

---

## 1. Descripción del conjunto

| Sitio | n quipus | n cuerdas | con suma (Ascher) | unión R/V (R:V) | torsión (S:Z) | color dominante |
|---|---|---|---|---|---|---|
| Armatambo | 14 | 649 | 11/14 | 297 : 343 | 37 : 611 | W, AB, MB, KB |
| Huaquerones | 19 | 702 | 12/19 | 447 : 225 | 689 : 6 | W, AB, MB, RL |
| Huacho | 7 | 955 | 7/7 | 250 : 591 | 950 : 0 | W, AB, YB, MB |
| Chancay | 7 | 184 | 3/7 | 57 : 91 | 181 : 0 | W, AB, MB |
| Marquez | 6 | 210 | 5/6 | 0 : 0 | 142 : 0 | **YB, W, LB, DB** |
| near Lima | 6 | 306 | 4/6 | 0 : 169 | 251 : 1 | W, AB, MB |
| Chuquitanta | 4 | 278 | 3/4 | 39 : 112 | 120 : 154 | W, AB, MB |
| **Total** | **63** | **3 284** | **45/63** | 1 090 : 1 531 (+6 T) | 2 370 : 772 | W, AB, MB |

Tamaño: media 52,1 cuerdas/quipu (σ 59,1), mediana 32, rango 3–306 (`MM001`, Huacho?); 2 897 cuerdas de nivel 0, 350 de nivel 1, 34 de nivel 2, 3 de nivel 3. Proporción de cuerdas con valor > 0: 0,67–0,96 (Armatambo 0,75; Huaquerones 0,67).

**Tabla por quipu:** `tabla_quipus.csv` (n cuerdas, niveles, nº grupos, tamaños de grupo, colores top, rango de valores, nº de cuerdas 0-sin-nudo, S/Z, R/V/T, direcciones de nudo, estructura del PC). **Sumas por quipu:** `sumas_quipus.csv`.

### 1.1 Torsión, unión R/V y dirección de nudo

- **Torsión del cordón.** Separa los sitios de forma casi total: **Armatambo es el único sitio con torsión Z dominante** (611 Z vs 37 S); Huacho, Chancay, Marquez, near Lima y Huaquerones son S (Chuquitanta es mixto, por arrastre de `KH0001`). Este es el resultado más nítido del conjunto.
- **Torsión ↔ unión (R/V): NO hay asociación.** Contingencia seguro(S)/Z × R/V: S→R 788/V 1 116; Z→R 299/V 414; **χ² p = 0,83**. La idea de que S↔verso y Z↔recto "casi perfecta" **no se sostiene** en este conjunto (es un control que refuta una expectativa razonable). La unión R vs V sí es un rasgo **de quipu** completo: p. ej. UR060 (108 R/0 V) frente a UR061 (0 R/41 V).
- **Dirección de nudo** (S/Z en la cadena `nudos`), nudos individuales: S 3 853 / Z 8 179. Por sitio, la fracción S es muy variable: near Lima 0,86; Chancay 0,62; Armatambo 0,47; Huacho 0,42; Huaquerones 0,13; Chuquitanta 0,04; Marquez 0,001. Al separar por tipo: los nudos **simples** son Z-dominantes en casi todos los sitios (Marquez 0,00 S; Huaquerones 0,08; Armatambo 0,20) salvo **near Lima (0,93 S)**; los nudos **largos** son S-dominantes en Armatambo (0,62), Huacho (0,62), near Lima (0,88) y Z-dominantes en Huaquerones (0,02) y Marquez (0,00). La variación sitio-dirección es real pero está confundida con la tradición de torsión local.

### 1.2 Sumas, cuerdas superiores y valores

- **Sumas internas.** 45/63 quipus (71 %) tienen ≥1 relación de suma Ascher; totales agregados: 557 colgante-colgante (`pendant-pendant`), 167 colgante-colgante-con-color, 117 con índice, 84 subsidiaria-colgante, 13 grupo-grupo, 17 bandas de suma, 13 clusters decrecientes. Un detector propio (cord = suma de un bloque consecutivo contiguo del mismo grupo) halla **809 relaciones en 38 quipus**: la aritmética de sumas es un rasgo **general y transversal**, no distintivo de un sitio. Huacho es el sitio más "sumatorio" (7/7 quipus, 404 relaciones; `MM001` 164).
- **Cuerdas superiores (`union=T`): solo 6 en todo el conjunto** — 4 en `HP047` (Armatambo) y 2 en `UR186` (Chancay/Huando). Coincide con Medrano y Khosla (2024): los *top cords* son minoría.
- **Colores.** Blanco (W) domina en todos los sitios; **Marquez es el sitio menos "blanco"** (YB es su color más frecuente, seguido de W/LB/DB). `UR060` mezcla RL (rojo) y `MM001` PG/GG (verde): la mayoría usa la tríada W/AB/MB.

---

## 2. Relaciones ENTRE los quipus (con controles)

Seis contrastes de par (62 quipus, 1 891 pares), nulo por barajado intra-quipu (500 iter, semilla 0) y BH-FDR:

| Test | Estadístico | Observado | Nulo | p / q |
|---|---|---|---|---|
| 1 | bigramas de valor compartidos (total) | 3 523 | 3 790 ± 114 | z = −2,3; **0/1 891 pares con q < 0,05** |
| 1b | íd., barajando dentro de grupos (robustez) | 3 523 | 3 639 ± 107 | z = −1,1; p = 0,86 |
| 2 | total(A) ∈ valores(B) | 149 | 80 ± 36 | p = 0,050 (nulo de pool) |
| 3 | multiconjunto de tamaños de grupo idéntico | 1 par | 4,1 ± 2,2 | p = 0,99 |
| 4 | bigramas de color compartidos | 4 784 | 5 448 ± 139 | z = −4,8; p = 1,00 |
| 5 | total(A) = suma de un grupo de B | 46 | 26 ± 9 | p = 0,028 (nulo de pool) |

**Interpretación.**

- **No hay secuencias de valores compartidas entre quipus.** El exceso es **negativo** (los pares reales comparten *menos* bigramas que el azar), tb. al barajar sólo dentro de grupos. Ninguno de los 1 891 pares es significativo tras BH. La coincidencia "más llamativa" por bigramas es KH0227×UR283 (obs 31) con p = 0,18 y q = 1,0.
- **Coincidencias de totales/sumas de grupo:** ligeramente por encima del azar (p ≈ 0,03–0,05), pero **enteramente explicadas por enteros pequeños** (los "totales" más repetidos son 6, 10, 30, 16, 11, 42). Es el riesgo que Urton (2005) reconoce: con valores decimales pequeños, las coincidencias son baratas. **No es un hallazgo.**
- **Estructuras de grupos idénticas:** 1 par (UR065×UR286, ambos [6]) frente a 4,1 esperados → **negativo**.
- **Enriquecimiento por sitio (controlado por tamaño).** El estadístico crudo "bigramas dentro del sitio" parecía señalar a Huacho (obs 6,95 vs nulo 1,77; p = 0,010), pero es un **artefacto de tamaño** (los 7 quipus de Huacho son grandes). Al restar a cada par su propio nulo y permutar etiquetas de sitio, **ningún sitio** presenta exceso: Armatambo −0,21 (p 0,69), Huaquerones −0,31 (p 0,84), Huacho −2,08 (p 1,0), etc.; todos q ≈ 1,0.
- **Test global del máximo (control de selección post-hoc).** El par con más coincidencias posicionales de nivel 0 es **UR060×UR074 (17)** y con más bigramas KH0227×UR283 (31). Pero el **máximo nulo** entre todos los pares es 21,5 ± 2,7 (posicional) y 33,0 ± 2,5 (bigramas): **el mejor par real no supera lo que el azar produce en 1 891 pares** (p = 0,97 y 0,84). BH sobre las coincidencias posicionales: **0/1 891 pares con q < 0,05** (mínimo p = 0,002 → q = 1,0).

### 2.1 Candidato a cuenta duplicada: UR066 y UR067 (Huaquerones)

Único par con una firma *cualitativa* llamativa (no sólo orden de bigramas):

- Ambos tienen **32 cuerdas de nivel 0** y casi el mismo total (3 335 vs 3 485).
- **16 coincidencias posicionales** con valores > 0 (nulo intra-quipu 0,99; p = 0,0002).
- **Racha contigua idéntica de 14 posiciones** (índices 16–29: 19,4,3,0,22,3,9,2,156,13,12,…,2904,133,…,40).
- Comparten el valor **2904**, que **no aparece en ningún otro** de los 63 quipus (y 1212/1236 sólo aparecen en el vecino internamente duplicado `UR064`).

Es el patrón clásico de "cuentas duplicadas" de Urton y Brezine (2005) para Puruchuco. **Pero** el par se eligió *a posteriori* y, corregido por comparaciones múltiples (BH sobre los 1 891 pares), **q = 1,0**. Conclusión honesta: **apoyado con datos como el mejor candidato del conjunto, no demostrado**; requiere una prueba pre-registrada (p. ej. emparejarlo por número de museo o contexto antes de mirar valores).

---

## 3. Jerarquía detalle/resumen

- **Dentro de cada quipu** sí hay estructura de resumen: sumas colgante-colgante (557 en 45 quipus), 13 sumas grupo-grupo y 17 bandas de suma. `UR186` (Chancay/Huando) destaca: 3 clusters con cuerdas superiores sumatorias, 20 sumas colgante-colgante, 14 grupos con bandas.
- **`HP047` (Armatambo) es el mejor candidato a quipu de resumen**: 4 cuerdas superiores (`union=T`), 1 cluster de suma por cuerda superior (con doble suma), 3 clusters con bandas y 4 seriados. La primera cuerda (p1 = 2643) supera en magnitud a sus grupos (≈316, 742, 264, 592) y no la reproducen sus vecinos: la firma de "total" arriba es plausible pero **no verificable** con los datos abiertos.
- **No existe jerarquía numérica entre quipus.** Ningún total de un quipu equivale sistemáticamente a una suma de grupo de otro más allá del azar (§2). Los únicos "resúmenes" detectables son **intra-quipu**.
- `UR1124` vs `UR1124_Detail_1` (Marquez): el "detalle" tiene valores mucho mayores (hasta 4 800) que el cuerpo (máx 366) y una subsidiaria; **no** es un resumen del cuerpo, es re-documentación de una porción del mismo objeto.

**Conclusión §3:** el archivo de Lima no muestra un sistema de quipus de detalle/summary encadenados entre sí. La capacidad de resumen existe **dentro** del quipu (top cords + sumas), no **entre** quipus.

---

## 4. Contraste con la literatura

- **Locke (1912, 1928).** El conjunto AMNH de la expedición Bandelier (nº B-87xx) procede de Huando, Chancay, **Chuquitanta** y "Media Lima" (= nuestro *near Lima*), y Locke usó esos quipus para establecer que las **cuerdas superiores suman los colgantes**. Coincide con nuestra cohorte (Chancay/Chuquitanta/near Lima son AMNH o Berlín) y con §3: las cuerdas superiores existen pero son escasas (6). Ver **`docs/fichas/1912-Locke-peruvian-knot-record.md`, `1928-Locke-supplementary-notes.md`**.
- **Urton y Brezine (2005); Urton (2005); Brezine y Villacorta (2020).** El archivo de **Puruchuco** (21–23 quipus, UR060–UR082, hallados en una olla) es **el mismo que nuestra procedencia "Huaquerones"** (región Puruchuco, museo de Puruchuco). Es el caso canónico de "relaciones numéricas entre quipus de un archivo". Nuestro reanálisis con nulo y BH **no reproduce** relaciones significativas entre esos quipus salvo el candidato UR066/UR067; esto **sintoniza con la propia advertencia de Urton (2005)** ("la identificación de matches no usa criterio estadístico… ¿qué probabilidad hay de coincidencias por azar con valores pequeños?"). Ver **`docs/fichas/2005-Urton_puruchuco.md`, `2005-Urton-khipu-archives.md`**.
- **Clindaniel (2019).** Reporta que la dirección de nudo Z domina globalmente **salvo en Armatambo**, donde se invierte. Nuestro resultado afín y más limpio: **Armatambo es el único sitio con torsión de cordón Z** (611 Z vs 37 S), frente a la torsión S de Chancay/Huacho/Marquez/near Lima/Huaquerones. Matizamos: para **nudos simples** Armatambo es 0,20 S (Z-dominante), así que la "inversión" de Armatambo se expresa en la **torsión**, no en la dirección de nudo simple. Ver **`docs/fichas/2019-Clindaniel_grammar-inka-khipu.md`**.
- **Medrano y Khosla (2024).** Los *top cords* registran una **minoría** de las sumas: consistente (6 cuerdas T, 4 en un solo quipu, frente a 557 sumas colgante-colgante).
- **Thompson (2024).** Extiende el "grupo contable de Puruchuco" a pares de Arica (n = 2). Refuerza que las relaciones entre quipus se han documentado con **muestras mínimas y sin nulo**, justo lo que aquí controlamos.

**Qué se registraba aquí (propuesta).** El material de la costa central de Lima es **numérico y administrativo** (censo/tributo, cuentas con sumas y bandas de color), coherente con un aparato estatal/ychsma en torno a los centros de Pachacámac–Armatambo–Puruchuco–Huacho–Chancay. La aritmética es interna al quipu; no hay evidencia de un archivo de quipus encadenados (resumen de resúmenes) en estos 63 objetos. La excepción tentadora —UR066/UR067— sugiere **copias ajustadas de una misma cuenta** en Puruchuco, pero no sobrevive a la corrección múltiple.

---

## 5. Resultados negativos (explícitos)

1. **Sin secuencias de valores compartidas** entre ningún par (0/1 891 con q<0,05; exceso incluso negativo).
2. **Sin patrones de color compartidos** (bigramas de color por debajo del azar, p=1,00).
3. **Sin estructuras de grupo idénticas** más allá del azar (1 vs 4,1).
4. **Sin enriquecimiento por sitio** una vez controlado el tamaño (todos q≈1,0); el aparente efecto Huacho era artefacto de tamaño.
5. **Torsión ↔ unión R/V sin asociación** (χ² p=0,83) — refuta una expectativa común.
6. **Sin jerarquía numérica entre quipus** (totales/sumas cruzadas no superan el azar; nulo de pool).
7. **El mejor par por similitud no supera el máximo nulo** (test global del máximo).
8. **UR066/UR067**: candidato fuerte per-pair (p=0,0002) que **no sobrevive a BH** (q=1,0).

---

## 6. Nivel de evidencia

| Hallazgo | Nivel |
|---|---|
| Armatambo es el único sitio con torsión Z (resto S) | **Apoyado con datos** (n=14, separación casi total) |
| Armatambo con unión R-dominante y near Lima con V pura | **Apoyado con datos** (descriptivo) |
| Arqueología aritmética interna (45/63 con sumas; 809 sumas internas) | **Apoyado con datos** (conteo robusto, coincide con KFG) |
| Cuerdas superiores escasas (6) | **Demostrado** (dato directo) |
| Sin relaciones entre quipus tras nulo y BH | **Demostrado** (resultado negativo controlado) |
| Torsión ↔ unión sin asociación | **Demostrado** en este conjunto (χ² p=0,83) |
| UR066/UR067 = cuenta duplicada | **Apoyado con datos / propuesto** (no pasa BH; selección post-hoc) |
| HP047 = quipu de resumen encabezado por un total | **Propuesto** (firma compatible, no verificable) |
| Qué se registraba (censo/tributo administrativo) | **Propuesto / especulativo** |

---

## 7. Para el coordinador

- **Cohorte bien definida:** 63 quipus, 3 284 cuerdas; 63 OKR distintos (sin objetos contados dos veces); `UR1124_Detail_1` excluido por ser el mismo objeto. Sitios: Huaquerones 19, Armatambo 14, Huacho 7, Chancay 7, Marquez 6, near Lima 6, Chuquitanta 4.
- **Resultado negativo central (demostrado):** con nulo intra-quipu (500×, semilla 0) y BH-FDR **no hay relaciones significativas entre los quipus de Lima** — ni secuencias de valores, ni patrones de color, ni estructuras de grupo, ni enriquecimiento por sitio. El test global del máximo confirma que el mejor par real (17 coincidencias) está **por debajo** de lo que produce el azar entre 1 891 pares (21,5).
- **El único candidato con firma sustantiva es UR066×UR067** (Huaquerones/Puruchuco): 32 cuerdas cada uno, 16 coincidencias posicionales (p=0,0002), racha idéntica de 14 valores y comparten el valor 2904, único en el conjunto. **No sobrevive a múltiples comparaciones (q=1,0)**; recomiendo una prueba **pre-registrada** (emparejar por nº de museo antes de mirar valores), junto con UR064 (dos bloques internos de ~1 200).
- **Armatambo es el outlier del conjunto (apoyado con datos):** única procedencia con **torsión de cordón Z** (611 Z vs 37 S) y unión R-dominante; replica y precisa a Clindaniel (2019), que ya señalaba a Armatambo como excepción. Los demás sitios son S/verso.
- **La aritmética de sumas es interna, no un archivo encadenado:** 45/63 quipus con sumas Ascher (968 relaciones) y 809 sumas internas detectadas en 38 quipus; **pero** ningún total de un quipu reaparece como suma de grupo de otro más allá del azar. No hay jerarquía detalle↔resumen entre objetos.
- **Medrano y Khosla (2024) se confirman:** sólo 6 cuerdas superiores (`union=T`) en todo el conjunto (4 en `HP047`, 2 en `UR186`), frente a 557 sumas colgante-colgante. `HP047` es el mejor candidato a quipu de resumen (posible total en la 1.ª cuerda).
- **Se refuta una expectativa razonable:** torsión ↔ unión R/V **no** se asocian (χ² p=0,83). Cualquier interpretación R/V-S/Z como código debe probarse, no asumirse.
- **Triangulación literaria:** nuestra "Huaquerones" es el **grupo de Puruchuco** (Urton y Brezine 2005; Clindaniel UR060–UR082) y buena parte del conjunto es el material **AMNH Bandelier** de Locke (1912/1928: Huando, Chancay, Chuquitanta, Media Lima). Conclusión de contenido: **registro numérico administrativo (censo/tributo)**, sin evidencia de archivo encadenado — **propuesto**.
- **Recomendación siguiente ronda:** (1) tabla puente museo↔KFG↔OKR para pre-registrar emparejamientos y re-probar UR066/UR067 y UR064; (2) jerarquía intra-quipu en `HP047`/`UR186` (verificar top cords como totales) contra los reportes N/C de Locke; (3) replicar la inversión de Armatambo a nivel de **torsión** en todo el OKR (n=619) para ver si es un marcador local ychsma.
