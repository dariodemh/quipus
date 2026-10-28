# Monografía del archivo de norte de Chile: Lluta Valley, Arica y Playa Miller

*Carpeta:* `analisis/ds/a_chile/` · *Datos:* `analisis/datos/{cuerdas,quipus,grupos}.csv` (Khipu Field Guide, 651 quipus) + relaciones de Ascher de KFG (`data-science-khipu-article`) + OKR.

## 1. Pregunta

¿Qué es el archivo de quipus del extremo norte de Chile (Lluta Valley, Arica, Playa Miller #6)? Se pide: (1) describir el conjunto quipu a quipu; (2) buscar relaciones **entre** estos quipus con nulo explícito; (3) reconstruir, si existe, una jerarquía detalle/resumen; (4) contrastar con la literatura del sitio y proponer qué se registraba.

## 2. Método

- **Selección.** 10 objetos con `procedencia` ∈ {Lluta Valley, Mollepampa/Playa Miller, Playa Miller #6, Arica}: `AS069, KH0083, KH0267, UR058A, UR084, UR130, UR131A, UR131B, UR131C, UR132`.
- **Nombres duplicados.** Se comprobó en `okr-kh-numbers.csv` que ningún objeto aparece dos veces en la lista: `AS069=KH0082`; `KH0083=AS070=UR035`; `UR058A=KH0294`; `UR084=KH0320`; `UR130=KH0369`; `UR131A/B/C=KH0370/0371/0372` (un solo lote de museo, nº 21163); `UR132=KH0373`; `KH0267=UR034`. Los diez `kfg` y los diez `okr` son únicos: no hay alias contados como objetos distintos. En particular, `AS070` no figura como objeto aparte en KFG: solo existe como alias de `KH0083`.
- **Caveat.** `AS071` (=KH0084) fue excavado junto a AS069‑AS070 (Dauelsberg 1965) pero su `procedencia` viene como “Unknown”, así que queda fuera del conjunto estricto por la regla 6 (no usar museo como origen). Es un compañero probable de Lluta que conviene rastrear.
- **Unidad de análisis: el quipu** (regla 1 del BRIEF). Las comparaciones entre quipus usan la secuencia de colgantes; los controles permutan **dentro de cada quipu**.
- **Nulo (regla 2).** Barajado de los valores de las cuerdas dentro de cada quipu, conservando el multiconjunto de valores y el patrón de posiciones ausentes: 500 iteraciones, semilla 0 (`numpy.default_rng(0)`).
- **Corrección múltiple (regla 3).** Holm sobre los 45 pares (o 90 pares ordenados) según el test.
- **Valores 0 sin nudos = ausentes** (regla 6); no se cuentan como ceros reales.
- Scripts reproducibles en esta carpeta: `01b_tabla.py`, `02_relaciones.py`, `03_sumas_estructura.py`, `04_totales_color.py`, `05_trio_jerarquia.py`, `06_base_rates.py`.

## 3. Resultados

### 3.1 Tabla por quipu (KFG)

| kfg (=KH) | procedencia | cuerdas | colgantes | subsid. | prof. | grupos | col. Ascher | color dominante | rango val. | mediana | torsión | R/V | quipos de nudo S/Z | sumas Ascher (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AS069 (KH0082) | Lluta Valley | 1831 | 1650 | 181 | 2 | 432 | 245 | W | 1–585 | 14 | U | 0/0 | S:251 L:280 E:74 (dir. U) | pp 200, ip 140, color 263, sub 47 |
| KH0083 (KH0083=AS070=UR035) | Mollepampa / Playa Miller | 585 | 88 | 497 | 5 | 60 | 167 | W, AB, MG, DB | 1–748 | 22,5 | S | 87/0 | S:484 Z:69 E:79 | pp 3, ip 2, color 1, sub 9, isub 6 |
| KH0267 | Playa Miller #6 | 22 | 7 | 15 | 2 | 6 | 6 | W:LK, PR, MG | 1–4 | 3 | S | 0/7 | S:19 Z:3 | — |
| UR058A (KH0294) | Playa Miller #6 | 275 | 58 | 217 | 3 | 9 | 27 | W:KB, AB, MG | 1–7 | 1 | S | 58/0 | S:148 Z:83 E:86 | csb 2 |
| UR084 (KH0320) | Playa Miller #6 | 23 | 6 | 17 | 2 | 6 | 11 | W:KB, MB:KB | 1–5 | 1 | S | 0/0 | S:15 Z:2 | — |
| UR130 (KH0369) | Playa Miller #6 | 126 | 59 | 67 | 2 | 7 | 23 | W, AB, KB | 6–108 | 25 | S | 52/1 | S:98 Z:9 | pp 12, color 6 |
| UR131A (KH0370) | Lluta Valley | 89 | 56 | 33 | 2 | 9 | 6 | **AB (94 %)** | 2–748 | 20,5 | S | 22/41 | S:117 E:6 | pp 5, ip 1, color 4 |
| UR131B (KH0371) | Lluta Valley | 105 | 66 | 39 | 2 | 12 | 5 | **AB (93 %)** | 1–1152 | 14 | S | 30/36 | S:124 Z:1 | pp 7, sub 5 |
| UR131C (KH0372) | Lluta Valley | 100 | 59 | 41 | 2 | 10 | 4 | **AB (90 %)** | 1–766 | 26 | S | 26/37 | S:116 E:12 | pp 14, color 10, isub 1 |
| UR132 (KH0373) | Playa Miller #6 | 57 | 9 | 48 | 1 | 1 | 16 | LK, PR, W-KB | 6–25 | 10 | S | 0/0 | S:30 Z:13 E:16 | pp 2 |

Cifras clave (detalle en `tabla_descriptiva.csv`):

- **Tamaños muy dispares:** de 22 cuerdas (KH0267) a 1831 (AS069). Dos quipus grandes (AS069, KH0083) concentran 2416 de las 3213 cuerdas del conjunto.
- **Cuerdas superiores (cordón "T"): CERO** en los 10 quipus. Las sumas del conjunto son todas internas (colgante‑colgante, indexadas, subsidiaria‑colgante, banda). Contexto: solo 26/651 quipus del corpus tienen algún cordón T (154 cuerdas), así que la ausencia aquí es lo normal (consistente con Medrano & Khosla 2024: los top cords registran una minoría de sumas).
- **Unión R/V:** AS069 y los tres fragmentos pequeños (KH0267, UR084) no tienen R/V (unión U/desconocida); el resto es mayoritariamente **R (recto)**, salvo el trío UR131A/B/C donde domina **V (verso)** (UR131A 41 V vs 22 R; UR131B 36 V vs 30 R; UR131C 37 V vs 26 R).
- **Torsión:** siempre S salvo AS069 (U). **Dirección de nudo:** S dominante; Z aparece sobre todo en UR058A (83 Z de 231 nudos) y KH0083 (69 Z).
- **Colores:** dos regímenes. (a) Un grupo **blanco‑dominante** (AS069, KH0083, UR130, UR058A, UR084) y con acentos de marrón (KB/MB/AB) o púrpura (LK/PR); (b) el **trío UR131A/B/C, dominado por AB (marrón claro): 90–94 %** de sus cuerdas. KH0267 y UR132 son púrpura/magenta (PR, MG, LK). AS069 (245) y KH0083 (167) son extremos en número de colores (mediana del corpus = 7, p90 = 25).

### 3.2 Relaciones entre los quipus

**a) Secuencias de valores compartidas (colgantes).** Para cada par se contaron sub‑secuencias contiguas coincidentes (longitudes 2–5) y la corrida máxima. El par con más coincidencias en bruto es **AS069–KH0083** (1066 ventanas de longitud 4), seguido de AS069–UR131B (974) y AS069–UR130 (974). **Pero el nulo genera tantas o más:** AS069 tiene 1650 colgantes con solo 83 valores distintos y mediana 14, de modo que barajando aparecen corridas máximas de longitud 12 por puro azar. P‑valores empíricos (H):

| par | L4 | Lmax | p(Lmax) | Lmax nulo (media) |
|---|---|---|---|---|
| AS069–KH0083 | 1066 | 12 | 1,00 | 12,0 |
| AS069–UR131B | 974 | 11 | 0,46 | 9,5 |
| AS069–UR130 | 974 | 12 | 0,45 | 9,7 |
| KH0083–UR130 | 47 | 9 | 0,11 | 7,4 |

**Ningún par sobrevive a Holm** (p(L4) más bajo en bruto = 0,004 para AS069–KH0083 → 0,18 corregido; p(Lmax) ≥ 0,46 en los pares grandes). Los “parecidos” de secuencia se explican por el **multiconjunto de valores pequeños y el tamaño del quipu**, no por contenido compartido.

**b) Totales de un quipu presentes en otro.** Se tomaron las sumas de grupo (nivel colgante) más el total de cada quipu A y se contó cuántas coinciden con valores de cuerda de B; el nulo baraja los valores de A (cambia las sumas de grupo, conserva el multiconjunto). Resultado: **0 de 90 pares significativos tras Holm** (`05_trio_jerarquia.py`). Coincidencias aisladas como KH0083→UR131A {15, 21, 73, 258} no superan la tasa base.

**c) Estructuras de grupo idénticas.** Se compararon los vectores “nº de cuerdas por grupo”. Ningún par alcanza parecido alto: la mejor LCS normalizada es **0,33** (UR131B–UR131C, UR130–UR131B, KH0267–UR084). **No hay dos quipus con la misma estructura de grupos.** AS069 sí tiene una estructura interna llamativa: 432 grupos que alternan tamaño 1 (189) y 6–7 (170), con 153 pares adyacentes 1↔7 (seriación/banding muy marcada).

**d) Patrones de color.** Las coincidencias de color están dominadas por largas corridas de blanco (W), presentes en todos los quipus blanco‑dominantes; por eso muchos pares alcanzan corridas de 9 sin significado. El único patrón “propio” es el del **trío UR131A/B/C: los tres son AB‑dominantes** (90–94 %), contra una mediana del corpus del 5 % (p95 = 57 %). Solo **16 de 651** quipus del corpus superan el 80 % de AB, y los tres fragmentos del trío están entre ellos (P ≈ (16/651)³ ≈ 1,5·10⁻⁵ bajo un modelo uniforme).

### 3.3 Jerarquía detalle/resumen

- **No se detecta una jerarquía entre quipus** (ningún “resumen” cuyo total coincida con valores de otro; ningún par con estructura de grupos igual). Las jerarquías que existen son **internas** a cada quipu (padre→subsidiarias): p. ej. AS069 registra 200 sumas colgante‑colgante y 47 subsidiaria‑colgante, con cadenas de hasta 28 sumandos; KH0083 tiene 6 sumas subsidiaria indexadas sobre 5 niveles de profundidad (prof. 5, el máximo del conjunto).
- **Dos “familias” internas por procedencia**, no una jerarquía global:
  - **Lluta** (AS069 + trío UR131A/B/C): magnitudes altas (log₁₀ máx = 2,77–3,06), proportion de subsidiarias normal (0,11–0,69) y, en el trío, color AB y unión verso.
  - **Playa Miller / Arica** (KH0083, KH0267, UR058A, UR084, UR130, UR132): **muy ricas en subsidiarias** (ver 3.4).
- El trío **UR131A/B/C** comparte lote de museo (21163), procedencia (Lluta), color (AB) y **totales casi idénticos** (6713, 6691, 6345; ±6 %). Esto los señala como un conjunto producido/guardado como unidad, no un detalle de otro quipu.

### 3.4 Contrastes cuantificados contra el corpus (tasas base)

- **Subsidiarias por colgante.** Playa Miller/Arica: KH0083 = 5,65; UR132 = 5,33; UR058A = 3,74; UR084 = 2,83; KH0267 = 2,14 (UR130 = 1,14). Tasa base del corpus (ratio ≥ 2) = **4,6 %**. **5 de 6** quipus de Playa Miller superan 2 → p binomial ≈ **1,2·10⁻⁶**. Los percentiles de esos cinco van del **96 al 99**. Lluta, en cambio, es normal (AS069 = 0,11, percentil 46; trío 0,59–0,69, percentiles 76–80).
- **Magnitud (log₁₀ del máximo colgante).** Lluta: 2,77–3,06; Playa Miller “pequeños”: 0,60–0,85 (KH0267, UR058A, UR084) y 1,40 (UR132); KH0083 = 2,87 y UR130 = 2,03. La divergencia de magnitud dentro de Playa Miller es amplia.
- **Nº de colores.** AS069 (245) y KH0083 (167) son outliers extremos (mediana corpus 7).

## 4. Controles

- **Nulo de permutación** (barajado intra‑quipu de valores, 500 iter, semilla 0) para secuencias (a), totales de grupo (b) y patrón de color (d).
- **Corrección de Holm** sobre 45 pares (secuencias, color) y 90 pares ordenados (totales). Ningún test entre quipus queda significativo tras la corrección.
- **Tasa base del corpus** (los 651 quipus) usada como control poblacional para subsidiarias, magnitud y color, en lugar de comparar solo dentro del grupo.
- **Deduplicación de nombres** vía `okr-kh-numbers.csv`.

## 5. Resultados negativos

1. **No hay cuerdas superiores ni sumas de top cord** en el archivo de Chile (0/10 quipus).
2. **No hay secuencias de valores compartidas** entre quipus que sobrevivan al nulo: los “parecidos” son artefacto del tamaño y de valores pequeños repetidos.
3. **No hay relaciones de total** (suma de un quipu que aparezca como valor en otro) significativas.
4. **No hay estructuras de grupos idénticas** (LCS normalizada máxima 0,33).
5. **No hay jerarquía detalle/resumen entre quipus**; la jerarquía es interna a cada objeto.
6. Los patrones de color compartidos (largas corridas) se deben al blanco ubicuo, salvo el caso ya señalado del trío AB.

## 6. Nivel de evidencia

- **Bien apoyado** (censo directo de los datos): composición, tamaños, rangos de valores, ausencia de top cords, unión R/V, torsión, direcciones de nudo, y la deduplicación de nombres.
- **Apoyado con datos:** (a) el archivo de **Lluta** (magnitud alta, trío AB+verso, totales casi idénticos, lote 21163) frente al de **Playa Miller/Arica** (muy rico en subsidiarias, 5/6 ≥ 2, p ≈ 1,2·10⁻⁶; blanco‑dominante); (b) la riqueza en sumas internas de AS069 (200 pp + 140 ip + 263 color), coherente con la fórmula de Ascher (Medrano & Khosla 2024).
- **Propuesto:** que el archivo de Playa Miller/Arica registra magnitudes pequeñas (KH0267 1–4, UR058A 1–7) con abundante desagregación en subsidiarias (¿recuentos/atributos fraccionados?), y que el archivo de Lluta registra agregados de mayor escala (rango hasta ~750–1150). El dato radiocarbónico (Cherkinsky 2014) sitúa KH0083 (=AS070=UR035, Playa Miller #6) en **1559–79 d. C.**, es decir, ya en contacto colonial.
- **Especulativo:** el “significado” concreto (qué se contaba). No hay evidencia en los datos de este archivo que permita fijar un referente; solo se puede afirmar el **estilo local** (subsidiarias masivas y números pequeños vs. agregados grandes).

## 7. Contraste con la literatura del sitio

- **Cherkinsky et al. (2014, ficha `2014-Cherkinsky-khipu-radiocarbon.md`):** fecha UR35/AS70 = **KH0083** (Playa Miller #6, Arica) en 365 ± 29 BP → **1559–79 d. C.** Es el ancla cronológica de este archivo: el material de Arica/Playa Miller es tardío (Inka tardío / contacto).
- **Clindaniel (2019, ficha `2019-Clindaniel_grammar-inka-khipu.md`):** los **6 quipus del norte de Chile** actúan como *outliers*: con todos los khipus el término “procedencia” (PCA de lat/lon) es significativo (p < 0,05) para predecir seriación vs banding, pero **al excluir esos 6 quipus solo la magnitud queda significativa**. Es decir, la literatura ya registró que **este archivo es anómalo dentro del corpus inka** — coincide con nuestra “familia” chilena distintiva (subsidiarias masivas, AB, V).
- **Medrano & Khosla (2024, ficha `2024-Medrano_data-science-khipu.md`):** las fórmulas de Ascher caracterizan ≥ 74 % de 650 quipus y los **top cords son minoritarios**. Nuestro archivo encaja: 8/10 quipus tienen alguna relación de Ascher, y **0/10 tienen top cords** (las sumas son internas).
- **Ascher & Ascher (1981, ficha `1981-Ascher-code-quipu.md`):** el quipu como aritmética decimal y “sumas categóricas”. AS069 es precisamente un caso de sumas internas masivas, del tipo analizado caso a caso por los Ascher (el KFG remite a notas de Ascher & Ascher 1987: 490‑491 sobre AS069‑071, excavados por Percy Dauelsberg en 1965, Lluta).

## 8. Para el coordinador

- **Conjunto:** 10 objetos únicos del extremo norte de Chile (Lluta Valley, Mollepampa/Playa Miller #6, Arica); ninguno es alias repetido (verificado en `okr-kh-numbers.csv`). Dos grandes (AS069 1831 cuerdas; KH0083 585) y ocho pequeños (22–275).
- **Cero cuerdas superiores / cero sumas de top cord.** Todas las sumas son internas; AS069 es sumamente aritmético (200 sumas colgante‑colgante + 140 indexadas + 263 de color).
- **Ninguna relación entre quipus sobrevive a los controles:** las secuencias compartidas, los totales y las estructuras de grupo se explican por el nulo (barajado intra‑quipu, 500 it., semilla 0) y por la tasa base del corpus. Corrido con corrección Holm: 0/45 pares (secuencias/color) y 0/90 pares (totales).
- **Hallazgo fuerte y con control:** el sub‑archivo de **Playa Miller/Arica es extremadamente rico en subsidiarias** (5/6 quipus con ratio ≥ 2; tasa base 4,6 %; p binomial ≈ 1,2·10⁻⁶; percentiles 96–99). El de **Lluta es normal** en subsidiarias pero de **magnitud alta**.
- **El trío UR131A/B/C** (lote 21163, Lluta) comparte color **AB 90–94 %** (solo 16/651 quipus del corpus lo alcanzan), unión **verso** y **totales casi idénticos** (6713/6691/6345). Es un conjunto coherente, no un “resumen” de otro quipu.
- **No hay jerarquía detalle/resumen entre quipus.** La jerarquía es interna (padre→subsidiarias), especialmente profunda en KH0083 (prof. 5).
- **Cronología:** KH0083 = AS070 = UR035 está datado por ¹⁴C en **1559–79 d. C.** (Cherkinsky 2014) → material tardío/colonial; refuerza que este archivo es una práctica local del Horizonte Tardío‑contacto, no una anécdota.
- **La literatura ya marca este archivo como anómalo:** Clindaniel (2019) encuentra que excluir los 6 quipus del norte de Chile **elimina** el efecto de procedencia en el corpus → nuestra “familia chilena” (subsidiarias masivas + estilo de color) es un patrón real, no artefacto nuestro.
- **Recomendaciones:** (i) replicar el ratio de subsidiarias con la definición de profundidad del OKR y en subconjuntos por museo, para descartar sesgo de catalogación (KH0083 y UR132 son los extremos); (ii) probar si los “números pequeños + muchas subsidiarias” de Playa Miller codifican fracciones/atributos por objeto (a testar contra un nulo de composición); (iii) buscar más quipus de Lluta (**AS071=KH0084**, 404 cuerdas, valores ≤ 11, hoy con procedencia “Unknown”, y afines) para cerrar el conjunto del lote AS069‑071 y el 21163; (iv) verificar in situ la posible unidad física de UR131A/B/C (¿un solo objeto fragmentado o tres registros gemelos?).
