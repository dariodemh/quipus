# Información física en los quipus: espaciado entre grupos, posición de los racimos y largo de las cuerdas

**Autor:** equipo `t_espaciado` · **Fecha:** 18/10/2026 · **Semilla:** 20261017
**Datos:** KFG (`analisis/datos/cuerdas.csv`, `grupos.csv`, `quipus.csv`) y relaciones de suma KFG (`data/external/data-science-khipu-article/data/ascher_sum_relations/`).

---

## 1. Pregunta

¿Llevan información el **espaciado entre grupos** de colgantes (`pos_cm`, `espacio_cm`), la **posición vertical de los racimos de nudos** (cm desde el inicio de la cuerda) y el **largo de las cuerdas**?

Dos preguntas concretas:

1. ¿Los grupos separados por espacios mayores marcan **secciones con aritmética distinta** (otra escala de valores, otras sumas, otras series)?
2. ¿El largo de las cuerdas se relaciona con el **valor** o con el **color** *dentro* del quipu?

La unidad de análisis es el **quipu**. Todos los tests de cuerda usan permutaciones dentro de quipu (o dentro de grupo), nunca comparaciones entre cuerdas de quipus distintos.

---

## 2. Datos y método

### 2.1 Corpus y parsing

- 57.818 cuerdas, 651 quipus, 8.117 grupos de colgantes.
- 40.162 cuerdas tienen nudos; 64.416 racimos de nudos parseados de la columna `nudos` (`nTIPO(pos,dir),aporte`). El parseo recupera el 99,9% de los racimos; los 68 fragmentos mal formados son celdas vacías o sin valor.
- Se excluyen para los análisis físicos: 1.523 cuerdas con `largo = 0`, 87 con `pos_max > largo + 0,01` (posición inconsistente) y 9 pares `(kfg, cuerda)` duplicados. Quedan 40.050 cuerdas con posición válida.
- `valor = 0` con `nudos` vacío se trata como ausente (no cero), según el brief.

### 2.2 Variables físicas

- **Gap entre grupos**: `espacio_cm` es el espacio anotado entre el último colgante de un grupo y el primero del siguiente. KFG solo lo registra para grupos con ≥2 colgantes; para grupos de 1 colgante se aproxima con `pos_next − pos_cm` (el ancho del grupo es ~0). Para el análisis de sensibilidad se usa también `gap_dpos = pos_next − pos_cm` en todos los casos (incluye el ancho del grupo).
- **Posición de racimos**: cm desde el inicio (unión al cordón principal) hasta cada racimo. Se derivan: `pos_min` (primer racimo), `pos_max` (último), `cola = largo − pos_max` (tramo libre inferior), `lead = pos_min` (tramo libre superior), `span = pos_max − pos_min` (banda anudada).
- **Largo**: `largo` en cm.

### 2.3 Nulos y corrección

- **Permutación dentro de quipu**: para cada test se calcula el estadístico observado y 2.000–5.000 réplicas permutando la variable explicativa dentro de cada quipu (o dentro de cada grupo, para el color). El p empírico es `(1 + #{nulo ≥ obs})/(B+1)`; cuando la hipótesis es de asociación positiva se reporta la cola correspondiente y, para los resultados negativos, el p a dos colas.
- **Corrección múltiple**: Holm dentro de cada familia pre-especificada (A: discontinuidad entre grupos; B: aislamiento de estructuras aritméticas; C: cruce de sumas; largo: valor; largo: color). Se indica el p ajustado. Los resultados principales de A y C sobreviven también a Holm sobre las 19 pruebas de espaciado (p_adj ≈ 0,01).
- **Control de la explicación aburrida**: se controla por número de racimos, nivel jerárquico, posición dentro del grupo, tipo de unión y terminación; se compara el efecto del gap anotado con el de la distancia entre inicios (`gap_dpos`); se excluyen gaps extremos (>10 cm); se prueba con mediana además de media.

### 2.4 Muestras de los tests principales

| Test | Unidad | n |
|---|---|---|
| Pares de grupos consecutivos con gap | par | 5.397 (548 quipus; 342 con ≥4 pares) |
| Sección por el gap más grande (≥2 cm) | quipu | 78 |
| Grupos con estructura aritmética KFG | grupo | 871 (224 quipus) |
| Relaciones cluster-cluster | relación | 292 (107 quipus) |
| Relaciones pendant-pendant con span>0 | relación | 2.768 (311 quipus) |
| Largo ~ valor | quipu | 548 |
| Largo ~ color (color simple) | quipu / grupo | 221 / 414 |

---

## 3. Resultados

### 3.1 Espaciado entre grupos

**Descriptivos.** Hay 7.466 pares consecutivos con gap anotado (5.397 con ambas medias de valor disponibles). El gap es pequeño: mediana 0,5 cm (IQR 0,3–1,0; p90 = 2,0 cm; p95 = 3,5 cm; máximo 272 cm). Solo el 14,3% de los pares supera 2 cm y el 3,5% supera 5 cm. Los gaps grandes **no** son “cuerdas separadoras”: tras un gap >5 cm hay un 17% de grupos de 1 colgante, frente a 35% tras un gap ≤0,75 cm. Son tramos vacíos del cordón principal entre grupos sustanciales.

**A. ¿Los gaps grandes separan grupos más distintos?** Sí, pero el efecto es pequeño y graduado.

| Δ entre grupos adyacentes | Spearman(gap, Δ) intra-quipu | p (2 colas) | Holm | Grande vs pequeño (q75) | p | Holm |
|---|---:|---:|---:|---:|---:|---:|
| log valor medio | 0,074 | 0,0005 | **0,003** | +0,262 log | 0,0005 | **0,0025** |
| nº de dígitos (racimos) | 0,071 | 0,0005 | **0,003** | +0,154 | 0,0005 | **0,0025** |
| nº medio de racimos | 0,073 | 0,001 | **0,003** | +0,108 | 0,0005 | **0,0025** |
| largo medio | 0,075 | 0,001 | **0,003** | +1,87 cm | 0,0005 | **0,0025** |
| nº de cuerdas del grupo | 0,030 | 0,146 | 1,0 | — | — | — |
| entropía de color | 0,025 | 0,217 | 1,0 | +0,048 | 0,0035 | **0,017** |

- El 59% de los quipus muestra la asociación positiva para valor; el 59% para largo.
- El efecto es **graduado**: el Δ de valor estandarizado pasa de −0,04 (gaps 0–0,5 cm) a +0,24 (gaps >5 cm).
- No hay efecto sobre el **tamaño del grupo** (nº de cuerdas), lo que descarta que el resultado sea solo “grupos grandes vs pequeños”.
- El efecto es específico del **espacio anotado**: con `gap_dpos` (distancia entre inicios, que incluye el ancho del grupo) el efecto desaparece (ρ = 0,017; p = 0,19). Esto es coherente con que lo relevante sea el hueco vacío y no el ancho del grupo, pero también advierte de un posible sesgo de anotación de KFG.
- **Robustez clave:** al restringir a pares con gap **directamente anotado** (grupo anterior con ≥2 colgantes; n = 263 quipus), el efecto sobre el **valor** baja a ρ = 0,043 (p = 0,035) y no sobrevive a Holm; el efecto sobre el **largo** se mantiene (ρ = 0,076; p = 0,0013). La parte más sólida del hallazgo es, por tanto, que los gaps separan **módulos físicos de distinto largo**, no necesariamente escalas de valor.

**Test de sección (más exigente).** Para cada quipu con ≥6 grupos y un gap ≥2 cm se parte por el gap más grande y se compara la media de valor antes vs después; el nulo parte en un límite de grupo aleatorio del mismo quipu (5.000 réplicas). En 78 quipus:

| Feature | \|Δ\| observado | \|Δ\| nulo | z medio | p (media z) | % quipus p<0,05 |
|---|---:|---:|---:|---:|---:|
| log valor medio | 0,831 | 0,756 | 0,24 | 0,019 | 0% |
| nº racimos medio | 0,366 | 0,341 | 0,14 | 0,105 | 0% |
| largo medio (cm) | 5,51 | 4,74 | 0,31 | 0,003 | 2,6% |

La diferencia existe pero es **mucho menor de lo que sugiere el test de pares**: las secciones separadas por el gap más grande no tienen medias de valor dramáticamente distintas. El 0% de quipus con p<0,05 individual (frente al 5% esperado por azar) indica que el gap más grande no es un corte especialmente extremo dentro de cada quipu.

**B. ¿Las estructuras aritméticas están aisladas por gaps?** **No.**

- 871 grupos (224 quipus) tienen alguna estructura KFG: 140 series decrecientes, 149 bandas de suma, 605 grupos en sumas cluster-cluster.
- Los grupos con estructura aritmética **no** tienen gaps mayores ni antes ni después:

| Comparación | Diferencia (cm) | p (una cola positiva) | Holm |
|---|---:|---:|---:|
| gap después | −0,36 | 0,96 | 1,0 |
| gap antes | −0,09 | 0,66 | 1,0 |
| máximo de ambos | −0,21 | 0,83 | 1,0 |
| suma de ambos | −0,20 | 0,78 | 1,0 |
| controlando tamaño del grupo | +0,07 | 0,31 | 1,0 |

*(p a dos colas para el gap posterior ≈ 0,08; la dirección es negativa, es decir, los grupos aritméticos están algo menos aislados, no más.)*

Si algo, los grupos aritméticos están **menos** aislados (gaps algo menores), no más. No hay apoyo a que el espaciado delimite “bloques de suma”.

**C. ¿Las sumas cruzan gaps grandes?** Resultado mixto y, en el caso favorable, probablemente artefacto de localidad.

- **Cluster-cluster sums** (292 relaciones, 107 quipus): cruzan 0,462 gaps ≥2 cm de media; ventanas aleatorias del mismo span y quipu cruzan 0,481 (p = 0,29; Holm = 1,0). Con ≥5 cm: 0,072 vs 0,066 (p = 0,75). **No evitan** los gaps grandes.
- **Pendant-pendant sums** (2.768 relaciones, 311 quipus): 0,191 vs 0,221 gaps ≥2 cm (p = 0,0003; Holm = 0,0013); con ≥5 cm, 0,025 vs 0,043 (p = 0,0003). Hay una evitación pequeña, pero las relaciones de suma ocurren en zonas densas (grupos grandes y vecinos), donde los gaps grandes son raros por construcción; el nulo de ventana aleatoria no conserva esa localidad. **No lo considero evidencia de fronteras aritméticas** sin un nulo que preserve la posición.

**Balance de 3.1.** Los gaps grandes marcan **cambios locales de escala** entre grupos adyacentes, sobre todo en el **largo de las cuerdas** (ρ = 0,076 con gaps directamente anotados) y, más débilmente, en el valor/nº de dígitos (ρ ≈ 0,04–0,07; el valor pierde significación al usar solo gaps anotados). No delimitan secciones coherentes con aritmética distinta ni aíslan las estructuras de suma. El efecto de escala es pequeño (Δ ≈ 0,26 unidades logarítmicas en el test de cuartiles, ~30% en media geométrica) y sensible a cómo se mide el gap.

---

### 3.2 Posición de los racimos de nudos

**Sanidad.** 40.162 cuerdas con nudos; 64.416 racimos. Solo 87 cuerdas (0,22%) tienen `pos_max > largo`; 1.523 tienen `largo = 0`. Las posiciones son cm con precisión de 0,5 cm en la mayoría de los casos.

**Orden vertical.** En las 16.960 cuerdas con ≥2 racimos, el 92,0% tiene aportes **descendentes** de arriba abajo (el racimo superior vale más). El 8,0% (1.359 cuerdas) presenta alguna inversión. Pero:

- 424 de los 447 quipus con ≥5 cuerdas multi-racimo son mayoritariamente descendentes; solo 8 son mayoritariamente ascendentes, 10 iguales y 5 mixtos.
- Las inversiones se concentran: 792 de las 1.359 cuerdas con inversión (58%) están en solo 10 quipus (AS014, KH0001, UR193, UR055, UR052, UR050, UR203…), y 28 quipus tienen >30% de cuerdas invertidas.
- Muchas “inversiones” no son cambios de orden decimal sino **varios racimos en el mismo orden**: p. ej. AS014 p1 = `2S(5),20; 2L(12),2; 6L(21),6; 3L(36),3` → 31, donde los tres racimos inferiores son unidades. El orden vertical no es el que decodifica KFG: el aporte de cada racimo ya viene dado y la suma no depende de la posición.
- Verificación directa: en las 40.092 cuerdas con todos los racimos parseados, `valor` coincide con la **suma de los aportes** en el 100% (tolerancia 10⁻⁶; 99,99% en cuerdas con ≥2 racimos). La posición vertical no entra en la suma. Cualquier información de la posición sería, por tanto, **adicional** al valor, no parte de él.

**Conclusión:** la posición vertical es **ordinal y redundante** con los valores de los racimos; no añade una lectura numérica independiente. El 8% de excepciones es un problema de registro/convención concentrado en pocos quipus, no un segundo código.

**Disposición física.** En cuerdas con ≥2 racimos (medianas): 24% de la cuerda libre arriba, 28% de banda anudada, 43% libre abajo. Los nudos ocupan una banda intermedia, con más cola que cabeza.

**Huecos entre racimos.** El hueco entre racimos consecutivos es grande: mediana 7,5 cm (IQR 4,5–13,0), el 20% del largo de la cuerda. Escala con el largo (r = 0,35) pero no con el número de racimos (r = −0,02). En cuerdas de 3 racimos, el primer hueco (7,0 cm) y el segundo (7,5 cm) son casi iguales; solo el 40,5% tiene el primero mayor (Wilcoxon p = 1,9×10⁻¹¹, pero la diferencia es 0,5 cm). **No hay puntuación decimal**: el espaciado no marca la frontera entre centenas, decenas y unidades.

**¿Hay información en el hueco?** En cuerdas de 2 racimos, la fracción de cuerda ocupada por el hueco correlaciona débilmente con el valor (ρ medio ≈ 0,18; 72% de los quipus positivo). Es un efecto pequeño, redundante con los nudos y compatible con el tamaño físico de los racimos; no lo interpreto como codificación.

---

### 3.3 Largo de las cuerdas y valor

**Dentro del quipu no hay relación positiva; si algo, una relación negativa trivial.**

| Test (548 quipus, ≥8 cuerdas y ≥4 valores) | ρ medio | p (2 colas) | Holm | % quipus positivo |
|---|---:|---:|---:|---:|
| Spearman largo ~ valor | −0,022 | 0,009 | **0,027** | 45% |
| Mismo nº de racimos (estratos quipu × n_clusters) | −0,086 | 0,001 | **0,004** | 38% |
| Mismo grupo (estratos quipu × grupo) | −0,042 | 0,001 | **0,004** | 45% |
| Cola ~ valor, mismo nº de racimos | −0,010 | 0,237 | 0,237 | 49% |

- El efecto es **estadísticamente detectable pero trivial**: como máximo, un cambio de 0,09 en la correlación de rangos; la dirección es negativa (valores mayores en cuerdas algo más cortas), no la esperada si el largo codificara magnitud.
- La cola (tramo libre inferior), que es la parte del largo no ocupada por nudos, **no** se relaciona con el valor una vez controlado el número de racimos (ρ = −0,01; p = 0,24). Es el test más limpio y es negativo.
- La correlación residual de −0,16 que aparece al residualizar el largo sobre nº de racimos y nivel es un **artefacto de supresión**: al parcializar una variable (nº de racimos) que correlaciona con el valor pero poco con el largo, se induce una correlación negativa. Por eso el test principal es el estratificado por nº de racimos, no el residual.
- **Entre quipus** sí hay correlación: media de log largo ~ media de log valor, r = 0,34 (566 quipus). Es una correlación ecológica: los quipus con cuerdas más largas tienden a tener valores mayores y más racimos (r = 0,33 con el nº medio de racimos). No autoriza a inferir que el largo de una cuerda codifique su valor.

**Conclusión:** el largo no codifica el valor dentro del quipu. La relación entre quipus es un efecto de escala/estilo del espécimen.

---

### 3.4 Largo de las cuerdas y color

**Asociación robusta y de tamaño moderado, pero localizada en los extremos libres, no en la zona anudada.**

| Test | Unidades | ε² observado | ε² nulo | p | Holm |
|---|---:|---:|---:|---:|---:|
| color ~ log largo, dentro de quipu | 221 quipus | 0,108 | 0,000 | 0,001 | **0,005** |
| color ~ log largo, solo nivel 0 | 219 quipus | 0,098 | −0,001 | 0,001 | **0,005** |
| color ~ log largo, dentro de grupo | 414 grupos | 0,164 | −0,003 | 0,001 | **0,005** |
| color ~ log largo, nivel 0, dentro de grupo | 263 grupos | 0,087 | −0,003 | 0,001 | **0,005** |
| color ~ largo residual (nº racimos + nivel), grupo | 414 grupos | 0,188 | −0,002 | 0,001 | **0,005** |
| **control positivo:** color ~ valor, dentro de grupo | 414 grupos | 0,135 | −0,018 | 0,001 | **0,005** |
| color ~ **span** (banda anudada), grupo | 378 grupos | **0,006** | −0,081 | — | — |

*Nota:* ε² de Kruskal-Wallis tiene sesgo negativo en grupos pequeños y con empates; por eso todos los efectos se comparan con el **nulo permutado** (columna “ε² nulo”), no con 0. Un observado ≈ nulo (como el span, 0,006 vs −0,081) indica ausencia de asociación.

- El color se asocia al largo incluso dentro del mismo grupo, del mismo nivel, y tras controlar el número de racimos. El control positivo (color ~ valor) también da señal, lo que indica que el método detecta la codificación por color conocida.
- **Dirección:** las cuerdas blancas tienen un log-largo +0,076 respecto del resto (≈8% más largas; 782 grupos; Wilcoxon p = 2×10⁻⁵); las marrones oscuras son más cortas: KB log-dif −0,186 (≈−17%), GG −0,183 (≈−17%), CB −0,203 (≈−18%) (dentro de grupo, vs resto).
- **Dónde está la diferencia:** el color se asocia al **lead** (ε² = 0,134) y a la **cola** (ε² = 0,120), pero **no** al span de los nudos (ε² = 0,006). Es decir, las cuerdas de distinto color difieren en cuánto cordón libre queda arriba y abajo, no en cómo se distribuyen los nudos. Esto es más compatible con un **convenio de corte/amarre o con el grosor/fibra** que con una codificación numérica.
- **Controles:** el efecto sobrevive a controlar la posición dentro del grupo (ε² residual = 0,177), el tipo de unión y terminación (ε² residual = 0,203), y a excluir el blanco (ε² = 0,166 entre colores no blancos). También sobrevive dentro de uniones R (0,132) y V (0,084).
- **Confusión residual:** el color se asocia fuertemente al tipo de unión (ε² = 0,191) y a la terminación (ε² = 0,165), y a la posición en el grupo (ε² = 0,106). Aunque el efecto del largo sobrevive a esos controles, no podemos descartar que color, grosor y fibra sean facetas del mismo rasgo físico (no hay grosor/fibra por cuerda en KFG: el campo `Thickness` está a 0 en los 30 quipus inspeccionados).

---

## 4. Controles, resultados negativos y explicaciones alternativas

**Negativos claros:**

1. **No hay secciones aritméticas delimitadas por gaps.** Las estructuras KFG (sumas, bandas, series decrecientes) no están más aisladas; los cluster-cluster sums no evitan gaps grandes. El único positivo (pendant-pendant) es pequeño y compatible con localidad.
2. **No hay puntuación decimal en el espaciado de racimos.** El primer y el segundo hueco son casi iguales; el espaciado solo escala con el largo.
3. **No hay relación positiva largo ~ valor** dentro del quipu; la relación es nula/negativa trivial. La cola no se relaciona con el valor.
4. **No hay efecto del color sobre el span de los nudos**; el color afecta solo a los extremos libres.
5. **No hay “cuerdas separadoras”**: los gaps grandes van seguidos de grupos normales, no de colgantes únicos.
6. **El tamaño del grupo no explica** la discontinuidad de valor entre grupos (Δ nº de cuerdas no significativo).

**Explicaciones aburridas que sobreviven:**

- Los gaps grandes son **tramos vacíos del cordón principal**, probablemente por montaje, rotura o separación de módulos de registro; su asociación con el largo y la escala de valor puede reflejar que los quipus se confeccionaron por partes o que el anotador separó visualmente bloques distintos.
- El largo está determinado por la **posición de los nudos y la cola libre** (R² largo ~ pos_max = 0,52; la cola es ~30% de la varianza entre quipus). La cola es un rasgo del fabricante/espécimen, no del valor.
- Las diferencias de largo por color se localizan en los extremos libres y podrían deberse a **grosor/fibra** (las cuerdas marrón oscuro podrían ser de camélido, más gruesas y cortadas más cortas) o a convenciones de corte. KFG no trae grosor utilizable.

**Sesgos de datos:**

- `espacio_cm` solo existe para grupos de ≥2 colgantes (30,8% de NaN, casi todos grupos de 1). La imputación con `pos_next − pos_cm` para esos casos es aproximada. El resultado de A es sensible a esta operacionalización: con `gap_dpos` desaparece, y el efecto sobre el valor se debilita al restringir a gaps directamente anotados (el efecto sobre el largo se mantiene).
- KFG no es una muestra aleatoria; los quipus de museo pueden estar montados con orientaciones y longitudes alteradas. Las 87 cuerdas con `pos_max > largo` y los 28 quipus con >30% de inversiones sugieren errores de medición o montaje.
- El color KFG mezcla color y material; no hay variable de fibra/grosor por cuerda.

---

## 5. Nivel de evidencia

| Afirmación | Nivel | Comentario |
|---|---|---|
| El espaciado anotado entre grupos es pequeño (mediana 0,5 cm) y los gaps grandes son raros | **Demostrado (descriptivo)** | 7.466 pares; p90 = 2 cm |
| Los gaps grandes se asocian a diferencias locales de **largo** (robusto) y, más débilmente, de valor/nº de dígitos entre grupos adyacentes | **Apoyado con datos** | largo ρ = 0,076 con gaps anotados; valor ρ = 0,043 y pierde Holm; desaparece con `gap_dpos` |
| Los gaps grandes **no** delimitan secciones con aritmética distinta ni aíslan las sumas | **Apoyado con datos (negativo)** | 871 grupos, 292+2.768 relaciones; tamaños de efecto ≈ 0 |
| La posición vertical de los racimos no añade información numérica independiente | **Apoyado con datos** | `valor` = suma de aportes en 100% de 40.092 cuerdas; 92% orden descendente; 8% excepciones en 28 quipus |
| El espaciado entre racimos no marca fronteras decimales | **Apoyado con datos (negativo)** | g1 ≈ g2 (7,0 vs 7,5 cm) |
| El largo no codifica el valor dentro del quipu | **Apoyado con datos (negativo)** | ρ ≤ 0,09 en valor absoluto; cola ~ valor p = 0,24 |
| El largo se asocia al color dentro del quipu/grupo | **Apoyado con datos** | ε² = 0,09–0,19; robusto a nivel, posición, unión y terminación |
| Esa asociación color-largo es un convenio de corte/fibra y no información semántica | **Propuesto** | se localiza en lead/cola, no en el span; sin datos de grosor/fibra |
| Los gaps grandes reflejan módulos de registro o montaje | **Especulativo** | plausible, no testeable con KFG |
| El color o el largo “significan” categorías/valores | **Especulativo** | no hay evidencia independiente en estos datos |

---

## 6. Limitaciones

1. **Medición**: las posiciones y largos son de KFG, con precisión de 0,5 cm y errores documentados; no son mediciones de laboratorio.
2. **Espaciado**: `espacio_cm` es una anotación, no una medida automática; su dependencia del número de colgantes obliga a imputar y puede introducir sesgo.
3. **Color**: los códigos KFG no separan pigmento de material; el efecto color-largo podría ser un efecto de fibra/grosor.
4. **Relaciones de suma**: las de KFG son detecciones con tolerancia y heurísticas; los spans en grupos pueden no coincidir exactamente con la estructura física.
5. **Poder**: para las estructuras aritméticas (871 grupos) el test excluye un efecto positivo mayor que ~0,35 cm, pero no permite afirmar equivalencia para efectos menores; la estimación puntual es incluso negativa (dos colas ≈ 0,08 para el gap posterior).
6. **No independencia**: aunque se permuta dentro de quipu, los quipus comparten museo/región y convenciones de registro; los p-valores no incorporan esa estructura.

---

## 7. Para el coordinador

- **Espaciado:** los gaps entre grupos son pequeños (mediana 0,5 cm) y los grandes (>2 cm) son el 14% de los pares. Separan grupos con **largo de cuerda** algo distinto (ρ = 0,076 con gaps anotados; +1,9 cm en el test de cuartiles) y, más débilmente, con distinto valor/nº de dígitos (ρ ≈ 0,04–0,07; el valor pierde significación al usar solo gaps anotados). El efecto desaparece si se mide la distancia entre inicios en vez del hueco vacío.
- **No hay “secciones aritméticas”:** los grupos con sumas/bandas/series decrecientes **no** están más aislados por gaps (diferencias ≈ 0, todas NS), y las sumas cluster-cluster no evitan los gaps grandes (0,46 vs 0,48; p = 0,29). El único positivo (pendant-pendant, 0,19 vs 0,22) es un artefacto probable de localidad.
- **Los gaps grandes no son cuerdas separadoras:** van seguidos de grupos normales (17% de 1 colgante, menos que tras gaps pequeños).
- **Posición de nudos:** el 92% de las cuerdas multi-racimo tiene los valores descendiendo de arriba abajo, pero el 8% de excepciones se concentra en 28 quipus (AS014, KH0001, UR193…), muchas veces por varios racimos en el mismo orden decimal. KFG no usa la posición para decodificar: la posición es **ordinal y redundante**, no un segundo canal.
- **El espaciado entre racimos no marca decimales:** el primer y el segundo hueco miden 7,0 y 7,5 cm (40% con el primero mayor); solo escala con el largo de la cuerda (r = 0,35). Los nudos ocupan una banda intermedia (24% libre arriba, 28% anudado, 43% libre abajo).
- **Largo ~ valor:** dentro del quipu la correlación es ≈ 0 (ρ = −0,02 cruda; −0,09 controlando nº de racimos; 38–45% de quipus positivo). La cola libre no se relaciona con el valor (p = 0,24). La correlación +0,34 entre quipus es ecológica, no individual.
- **Largo ~ color:** asociación robusta dentro de quipu y de grupo (ε² = 0,09–0,19; Holm < 0,01). Blancas: log-dif +0,076 (≈8% más largas); KB/GG/CB: log-dif −0,19 a −0,20 (≈17–18% más cortas). Pero el efecto está en el **lead y la cola**, no en el span anudado (ε² = 0,006): parece un convenio de corte/amarre o un efecto de fibra/grosor, no una codificación numérica.
- **Recomendación 1:** no usar el largo ni el espaciado como variables de valor en modelos de desciframiento; sí usarlos como **covariables de estilo/espécimen** (especialmente la cola y el color).
- **Recomendación 2:** antes de interpretar los 28 quipus “invertidos”, auditar la orientación de montaje (¿posiciones medidas desde el extremo libre?) y separar los que tienen varios racimos en el mismo orden de los que realmente invierten decenas/unidades.
- **Recomendación 3:** para cerrar la pregunta de secciones, repetir el test de sumas con un nulo que preserve la **localidad** (misma ventana de grupos, no una ventana aleatoria del quipu) y con las relaciones de suma de OKR, no solo las heurísticas de KFG.

---

### Archivos

- `prep.py` — parsing de nudos, derivadas y grupos.
- `explorar_nudos.py`, `explorar_grupos.py` — descriptivos.
- `analisis_espaciado.py` — tests A/B/C de espaciado.
- `robust_espaciado.py` — sensibilidad del test A.
- `secciones.py` — test de sección por el gap máximo.
- `analisis_largo.py` — tests de largo ~ valor y largo ~ color.
- `diag_color_pos.py` — controles de posición/componentes del efecto color.
- `log_espaciado.txt`, `log_largo.txt` — salidas completas.
- `pvalues_espaciado.csv`, `pvalues_largo.csv` — p-valores para Holm.
