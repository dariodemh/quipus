# lit_5 — Extracción y verificación de afirmaciones de la literatura

**Fecha:** 18 de octubre de 2026 · **Carpeta:** `analisis/ds/lit_5/`
**Semilla:** 20261017 · **Datos:** `analisis/datos/*.csv` (KFG preparado) y `data/external/open-khipu-repository/data/khipu.db` (OKR).

---

## 1. Pregunta

¿Qué afirmaciones concretas sobre la estructura o el significado de los quipus, publicadas en las nueve fichas asignadas, son realmente contrastables con los datos del repo, y cuáles se sostienen al comprobarlas?

El objetivo no es descifrar ni resumir la literatura, sino separar tres cosas que las fichas mezclan: (a) descripciones del corpus, (b) inferencias estructurales con control estadístico y (c) lecturas semánticas. Solo las dos primeras pueden auditarse con datos.

## 2. Método

1. **Lectura completa de las 9 fichas** (son cortas: 15–32 líneas cada una): Sivan 2026, Thompson 2026, Zenil & Uthamacumaran 2026, K-CAT, KFG, Khipu-ML, KhipuAnalysis, OKR y rv-repro.
2. **Extracción de 50 afirmaciones** a `afirmaciones.csv`, con fuente, afirmación, quipus implicados, cifras, cómo comprobarla y si es comprobable con los datos del repo (23 «sí», 21 «parcial», 6 «no»).
3. **Verificación de las 6 afirmaciones más importantes** que eran comprobables, priorizando las que tienen cifras cerradas y las que sostienen conclusiones fuertes:
   - conteos del corpus (OKR, KFG, K-CAT, Zenil);
   - réplica de Santa Valley (Khipu-ML);
   - asimetría de *handedness* (KFG);
   - cuerdas STRING y `knot_value_type` (Sivan);
   - restricción padre = Σ hijos (K-CAT);
   - color y magnitud del valor (K-CAT).
4. **Reglas aplicadas:** unidad de análisis = quipu; valores 0 sin nudos tratados como ausentes; nulo explícito por permutación dentro de cada quipu cuando hay inferencia; p-valor empírico; Holm cuando hay familia de pruebas; se reportan también los negativos.
5. Todos los scripts son reproducibles y están en esta carpeta (`02`–`08`); cada uno guarda su salida en `res_*.json`.

**Advertencia de independencia:** el corpus preparado (`cuerdas.csv`) deriva del KFG, la misma fuente que usa K-CAT. Verificar a K-CAT contra `cuerdas.csv` no es una replicación independiente: es una auditoría de consistencia interna. El OKR sí es una transcripción parcialmente independiente (otra base, otros curadores), y por eso la réplica de Santa Valley vale más como control.

## 3. Extracción: qué hay y qué es comprobable

| Fuente | Afirmaciones | «sí» | «parcial» | «no» | Tipo dominante |
|---|---:|---:|---:|---:|---|
| K-CAT | 10 | 6 | 4 | 0 | descriptores de corpus y patrones |
| Sivan | 8 | 1 | 4 | 3 | desciframiento silábico |
| KFG | 6 | 4 | 2 | 0 | sumas Ascher y handedness |
| rv-repro | 6 | 2 | 2 | 2 | entropía R/V y LLM |
| Zenil | 5 | 2 | 3 | 0 | topología/ML estructural |
| Thompson | 5 | 4 | 1 | 0 | curación de datos |
| Khipu-ML | 5 | 2 | 3 | 0 | clustering y réplica R/V |
| OKR | 3 | 2 | 0 | 1 | inventario |
| KhipuAnalysis | 2 | 0 | 2 | 0 | EDA / cobertura |
| **Total** | **50** | **23** | **21** | **6** | |

Patrón general: las afirmaciones **descriptivas** (conteos, proporciones, patrones de suma) son las más comprobables y las que mejor se reproducen. Las afirmaciones **semánticas** (Sivan; tipos de documento; categorías de tributo del LLM de rv-repro) no son comprobables con los datos del repo: requieren diccionarios, código no publicado o documentos externos. Las afirmaciones **estructurales con ML** (Zenil, Khipu-ML) son parcialmente comprobables: sus conjuntos de datos se pueden reconstruir, pero sus pipelines no.

---

## 4. Verificaciones

### 4.1 Conteos del corpus: exactos en el OKR, inflados en K-CAT

| Fuente | Afirmación | Medido en el repo | Veredicto |
|---|---|---|---|
| OKR | 619 quipus, 54.403 cuerdas, 110.677 nudos, 633 principales | 619 / 54.403 / 110.677 / 633 | **exacto** |
| OKR | 702 números KH; 83 sin fila en la base | 702; 83 | **exacto** |
| KFG | 650 quipus, 55.720 cuerdas, 116.246 nudos | 651 xlsx; `cuerdas.csv` 651 / 57.818; `khipu_summary.csv` 650 filas | **casi exacto** (difiere el conteo de cuerdas) |
| KFG | 14 (2%) quipus sin nudos | 10 (1,5%) | **parcial** |
| K-CAT | 709 quipus, 62.746 cuerdas | la fuente tiene **651 xlsx** y 650 filas de resumen | **no reproducible desde esta release; +9%** |
| K-CAT | 69,7% cuerdas con valor>0 | 69,35% | **exacto** |
| K-CAT | 98,2% quipus con ≥1 valor | 98,31% | **exacto** |
| K-CAT | L:S = 1,05 | 1,049 | **exacto** |
| K-CAT | 80,3% pendants sin subsidiarias | 80,7% | **exacto** |
| K-CAT | 72,6% quipus con ≥1 patrón de suma | 74,5% (484/650) | **apoyado, no exacto** |
| K-CAT | PPS 57,8% de los quipus / 7.018 relaciones | 65,7% (427/650) / 8.088 cuerdas de suma | **parcial** (difiere el denominador) |
| K-CAT | handedness PPS 45,7/54,3 | 45,82/54,18 | **exacto** |
| Zenil | 532 quipus / 15.558 cuerdas elegibles | 534 / 15.853 (+0,4% / +1,9%) | **casi exacto** |
| Zenil | 8.959 enlaces padre-hijo | 9.021 si ambos extremos tienen nudos; 15.302 sin ese filtro | **parcial** (depende de la definición) |

**Lectura.** El OKR se reproduce al dígito. Los descriptores de K-CAT sobre `cuerdas.csv` se reproducen con una precisión notable (69,35 vs 69,7; 98,31 vs 98,2; 1,049 vs 1,05; 80,7 vs 80,3), lo que sugiere que su pipeline de decodificación es correcto. Pero su cifra de corpus (709/62.746) no sale de la release del KFG: hay 651 archivos y 650 filas. Eso no invalida sus proporciones, pero sí su marco de «todo el corpus»: están contando algo distinto (posiblemente duplicados o versiones), y cualquier tasa calculada sobre 709 hereda ese error de denominador.

Estas filas son **conteos descriptivos, no tests**: no llevan nulo ni p-valor. El control aquí es la doble fuente (OKR frente a KFG) y la reproducibilidad al dígito o la discrepancia sistemática.

El conjunto elegible de Zenil se reconstruye casi exactamente (15.853 vs 15.558 cuerdas; 534 vs 532 quipus), lo que es un control positivo de que su definición de «≥2 grupos de nudos en posiciones positivas» está bien especificada. El conteo de enlaces no coincide con una definición ingenua, pero sí al restringir a enlaces con nudos en ambos extremos (9.021 vs 8.959, +0,7%): su n=8.959 es plausible.

### 4.2 Santa Valley: replicación exacta, 6/6

Khipu-ML afirma que en KH0323–KH0328 cinco de seis quipus son R o V puros, que KH0326 es el único mixto (40 R / 69 V) y que el agregado es 49/51. Conté `ATTACHMENT_TYPE` por `KHIPU_ID` en `khipu.db`:

| KH | R | V | U | Khipu-ML |
|---|---:|---:|---:|---|
| KH0323 | 310 | 0 | 61 | 310/0 ✓ |
| KH0324 | 0 | 54 | 48 | 0/54 ✓ |
| KH0325 | 0 | 207 | 81 | 0/207 ✓ |
| KH0326 | 40 | 69 | 22 | 40/69 ✓ |
| KH0327 | 0 | 93 | 32 | 0/93 ✓ |
| KH0328 | 56 | 0 | 5 | 56/0 ✓ |
| **Total** | **406** | **423** | **249** | **49/51 ✓ (48,97%)** |

Los seis conteos coinciden **exactamente**, el único quipu mixto es KH0326 y el agregado da 48,97% R / 51,03% V. Es la verificación más limpia de todo el lote. Lo que esto demuestra es la **estructura R/V**, no la contabilidad: la propia autora advierte que no reproduce el total de 367 pesos. Nivel: **demostrado** (para el patrón estructural y los conteos); la interpretación hanan/hurin sigue siendo **apoyada con datos** por Medrano & Urton, no demostrada aquí.

### 4.3 Handedness: 54/46 se sostiene; 63% y subsidiary no

Leí los cuatro CSV de `ascher_sum_relations` y agregué por quipu. La unidad es el quipu; el test principal es de signos (¿hay más quipus con exceso de sumas derechas que de izquierdas?), con bootstrap de quipus y un nulo que reparte las sumas de cada quipu con p=0,5.

| Relación | R% medido | L / R | KFG declara | p signos | Holm (4 tests) | IC95% bootstrap |
|---|---:|---|---:|---:|---:|---|
| pendant-pendant | **54,18** | 3.706 / 4.382 | 54/46 [4382/3706] | 1,26e-6 | 5,0e-6 | [52,8; 55,6] |
| color | **56,47** | 1.316 / 1.707 | 56/44 [1707/1316] | 5,55e-6 | 1,7e-5 | [52,9; 59,8] |
| indexed | **57,27** | 1.000 / 1.340 | 57/43 [2712/2034] | 6,16e-6 | 1,2e-5 | [53,8; 60,7] |
| subsidiary | 60,37 | 65 / 99 | 57/43 [439/328] | **0,871** | 0,871 | [46,5; 71,6] |

- **PPS, color e indexed se sostienen.** Las proporciones coinciden al segundo decimal y el exceso de sumas derechas es consistente en quipus (233 vs 139; 152 vs 82; 138 vs 72). El nulo intra-quipu para PPS da p=0,0002 (N=5.000). El efecto es real pero modesto: 54,2% frente a 50%, *odds ratio* ≈ 1,18.
- **Cuidado con los conteos absolutos de la ficha.** En indexed la proporción 57/43 coincide, pero los totales de la ficha (2.712/2.034) no salen de estos CSV (1.000/1.340); probablemente cuenta cuerdas sumando o usa otra versión. En subsidiary los totales son incompatibles (ficha 439/328; CSV 65/99): misma dirección, pero 60/40 y con n=164. La ficha y el corpus preparado no son intercambiables al nivel de conteos.
- **Subsidiary no se sostiene** con n=164 sumas: 60,4% pero 20 quipus a favor y 18 en contra (p=0,87). La cifra 57/43 de la ficha probablemente suma conteos de cuerdas, no de quipus, y con n pequeño es frágil.
- **El «63% de los khipus presenta ambos sentidos» no se reproduce.** Con la unión de las cuatro relaciones obtengo 361/724 = 49,9%; sobre 650 = 55,5%; restringido a quipus con alguna suma = 74,6%. Ninguna definición da 63%. La afirmación depende de un denominador que la ficha no explicita; queda **no apoyada**.

Nivel: **apoyado con datos** para la asimetría PPS/color/indexed; **no apoyado** para subsidiary y para el 63%.

### 4.4 Sivan: la cuenta STRING se sostiene; el 99,8% no

**a) Cuerdas STRING.** Sivan define STRING como las cuerdas incompatibles con la lectura decimal (más de un nudo largo o más de un nudo en ocho) y afirma 1.992/37.206 = 5,35%. Conté en `knot` por `CORD_ID`:

- cuerdas con algún nudo: **37.206** (coincide exacto);
- con >1 L/LL o >1 E/EE: **1.963 = 5,28%** (1.721 con >1 L, 254 con >1 E, 12 con ambos).

La diferencia es de 29 cuerdas (1,5% relativo), atribuible a la versión del OKR o a incluir LL/EE. **Se sostiene.** Es un hecho descriptivo útil: el 95% de las cuerdas anudadas es compatible con una lectura decimal; el «canal silábico» se propone sobre el 5% restante.

**b) `knot_value_type = NUM_TURNS × PLACE_VALUE` en 586/588 (99,8%).** Esta afirmación no se sostiene tal como está escrita:

- la tabla `knot` del OKR **no tiene columna `PLACE_VALUE`**;
- para los nudos L, `knot_value_type` es igual a `NUM_TURNS` en **21.588/21.907 = 98,54%** (no 99,8%);
- restringido a cuerdas STRING, la coincidencia cae a **4.069/4.257 = 95,58%**, no 99,8%;
- el valor de `knot_value_type` en L toma valores 2–9, es decir, es el dígito de vueltas, no un producto por el lugar. El lugar lo aporta el cluster/posición.

Si Sivan definió su propio `PLACE_VALUE` como 1, la fórmula es tautológica; si no, es falsa en el 100% de los casos porque el campo no existe. Esto confirma la crítica de la ficha: comprobar esa relación contra el OKR **no valida la lectura silábica**, solo confirma una convención ya incorporada en la base. Nivel de la afirmación: **rechazada en su forma publicada**.

### 4.5 Padre = suma de hijos: minoría real, pero el 6,6%/0,35 depende de contar ausentes como cero

K-CAT afirma que la restricción se cumple solo en 6,6% de los grupos padre-hijo, con razón mediana 0,35 y 39,4% de grupos triviales. Construí los grupos padre→hijos directos desde `cuerdas.csv` y probé definiciones explícitas (el repo de K-CAT no publica la suya):

| Definición | Grupos | Igualdad exacta | Mediana hijo/padre |
|---|---:|---:|---:|
| **D1** hijos con valor; sin nudos = ausente (regla del brief) | 6.344 | **9,06%** | **0,50** |
| **D1b** todos los grupos; hijos sin valor = suma 0 | 7.484 | **7,72%** | **0,357** |
| **D2** solo grupos con ≥2 hijos con valor | 1.800 | **4,00%** | **0,733** |
| D3 estilo K-CAT (sin nudos = 0) | 9.426 | 9,07% (no trivial) | 0,50 |

- El **9,06%** de D1 es la estimación correcta bajo la regla 6 del brief. La igualdad exacta ocurre **más de lo esperado por azar**: el nulo que baraja los valores de los hijos dentro de cada quipu da p=0,0005 (N=2.000); tras Holm para D1/D2, p=0,001 y p=0,0005. Pero sigue siendo una **minoría**: ~9 de cada 10 grupos no cumplen la suma.
- El **7,72% y la mediana 0,357** de D1b reproducen casi exactamente el 6,6% y 0,35 de K-CAT. El patrón es consistente con que K-CAT esté incluyendo grupos **sin ningún hijo con valor** y contándolos como suma 0: eso viola la regla 6 (0 sin nudos = ausente) y arrastra la mediana hacia abajo. Con el tratamiento correcto, la mediana es 0,50, no 0,35.
- El **39,4% de grupos triviales** no se reproduce con ninguna definición obvia: obtengo 15,3% si se exige padre con valor, y 32,8% si además se cuentan los padres ausentes como cero. Su definición debe de incluir otros casos (probablemente grupos sin hijos registrados).
- Con ≥2 hijos la igualdad cae al 4,0% y la mediana sube a 0,73: **el 87,5% de los «aciertos» del 9% son grupos de un solo hijo** que repite el valor del padre (11,1% de esos casos), un patrón que puede ser copia/registro y no suma.

Nivel: **apoyado con datos** que la suma padre=hijos es una minoría (4–9%) y que ocurre más que el azar; **parcial/rechazada como cifra exacta** la versión 6,6%/0,35, que es un artefacto de definición.

### 4.6 Color: el p-valor gigante se reproduce; el efecto es pequeño

**a) Prevalencia del blanco.** K-CAT dice 27,5% de las *entradas* de color y 77,7% de los quipus. En `cuerdas.csv` (una fila por cuerda, no por entrada):

- W exacto: **12.537/57.385 = 21,85%** de las cuerdas con color;
- alguna cuerda que contiene W: **22.137 = 38,58%**;
- quipus con W exacto: **460/651 = 70,7%**;
- quipus con alguna W: **534/651 = 82,0%**.

El 27,5% cae entre 21,9% y 38,6%, y el 77,7% entre 70,7% y 82,0%: son plausibles si se cuentan **entradas** de color (varias por cuerda) en lugar de cuerdas. No es reproducible con `cuerdas.csv` sin la tabla de colores del KFG. **Parcial.**

**b) Color y magnitud del valor.** Reproduje el test a nivel de cuerda: Kruskal-Wallis con 39 colores (n≥30), **H=1.449,8, p=7,5e-280**, frente a H=1.419, p=3,6e-267 de K-CAT. La diferencia es trivial y confirma que el pipeline de K-CAT es correcto. Pero el tamaño del efecto es **ε² ≈ 1.450/39.782 ≈ 0,036**: el color explica ~3,6% de la varianza del log-valor. El p-valor astronómico es consecuencia de tratar 39.782 cuerdas de 637 quipus como independientes.

Al agregar por quipu (394 quipus con ≥3 cuerdas blancas y ≥3 no blancas):

- mediana de la diferencia W − no W = **+0,077 log10** (≈ 1,19× en valor), es decir, las cuerdas blancas valen **ligeramente más**, no menos;
- 216 quipus con W>no W frente a 141 con W<no W; test de signos p=8,5e-5;
- nulo que baraja color dentro de cada quipu: p=0,001 (N=1.000).

La asociación **sobrevive** a la agregación por quipu, pero es pequeña y de signo contrario a la lectura «colores bandados por encima de W» si se compara W contra todo lo demás. Holm para las dos pruebas de la misma hipótesis (signos y permutación) deja p=1,7e-4 y p=0,001, así que el efecto no desaparece; lo que no sobrevive es su **tamaño**. Nivel: **apoyado con datos** que hay asociación débil; **rechazada** la lectura del p=3,6e-267 como prueba de un efecto fuerte.

### 4.7 Thompson: los quipus del Peabody no están en el corpus preparado

- **AS030, AS031, AS032 y AS033A–G no existen en `cuerdas.csv`** (651 khipus). En el OKR sí están, como KH0032–KH0041. Es un hueco de cobertura relevante: los conjuntos del Peabody (siete números de acceso, uno de ellos el anillo de siete quipus) quedan fuera de todos los análisis hechos sobre el KFG preparado, y K-CAT (que dice usar 709) tampoco los estaría incluyendo si su fuente es la misma release.
- La lectura citada de **AS033A p1 = 1S(5,0,Z),10 + 2L(14,0,Z),2 = 12** no coincide con el OKR: KH0035 cord 1 tiene **dos nudos S en el mismo cluster, ambos valor 10**, no un S más dos L. Puede ser que el OKR no haya incorporado la corrección de la visita de 2026, o que la numeración p1 no sea la misma. **No verificable / discrepante.**
- **29 quipus del OKR no tienen fila de metadatos** en `quipus.csv` (p. ej. KH0099, KH0114, KH0589–KH0592). Cualquier análisis que cruce OKR con `quipus.csv` pierde esos 29 sin avisar.

Nivel: la ficha es **curación de datos**, no una hipótesis; sus cifras no son auditables con el corpus preparado porque los objetos no están. En el OKR sí están los objetos, pero la lectura citada de p1 no coincide, así que la corrección no puede confirmarse con esta versión. El hallazgo negativo es de **cobertura**, no de interpretación.

---

## 5. Resultados negativos (explícitos)

1. **Subsidiary handedness 57/43**: no se sostiene a nivel de quipu (60,4%, 20 vs 18 quipus, p=0,87).
2. **«63% de los khipus con ambos sentidos»**: no se reproduce bajo ninguna definición razonable (49,9% / 55,5% / 74,6% según denominador).
3. **Sivan, `knot_value_type = NUM_TURNS × PLACE_VALUE` 99,8%**: el campo `PLACE_VALUE` no existe; la coincidencia con `NUM_TURNS` es 98,5% global y 95,6% en STRING; la fórmula, tal como se publica, es falsa o tautológica.
4. **K-CAT, 709 quipus / 62.746 cuerdas**: no reproducibles desde esta release del KFG (651 xlsx, 650 filas); +9% sobre el total real del corpus preparado.
5. **K-CAT, padre=Σhijos 6,6% y mediana 0,35**: solo se aproxima si se cuentan los hijos ausentes como cero; con la regla correcta es 9,06% y 0,50. El 39,4% de grupos triviales no se reproduce (15,3–32,8%).
6. **K-CAT, color p=3,6e-267 como efecto fuerte**: se reproduce el p, pero ε²≈3,6% y a nivel de quipu la diferencia es +0,08 dex (≈1,2×), no un salto de orden de magnitud.
7. **Thompson, AS033A p1=12**: el OKR muestra dos nudos S de valor 10; no coincide.
8. **Zenil, 8.959 enlaces**: no sale con una definición ingenua (15.302); sí al exigir nudos en ambos extremos (9.021), pero la definición exacta no es reproducible sin su código.

## 6. Nivel de evidencia de cada conclusión

| Conclusión | Nivel |
|---|---|
| Los conteos del OKR (619/54.403/110.677/633; 702 KH/83) son exactos | **demostrado** |
| La réplica R/V de Santa Valley (6/6 conteos, KH0326 único mixto, 49/51) es exacta | **demostrado** |
| La asimetría PPS 54/46 y color 56/44 existe y es consistente por quipu | **apoyado con datos** (p≈1e-6, Holm; efecto modesto) |
| El 5,3% de cuerdas STRING es correcto | **apoyado con datos** (1.963/37.206) |
| La suma padre=hijos es una minoría (4–9%) pero ocurre más que el azar | **apoyado con datos** (nulo p=0,0005; Holm) |
| El color se asocia débilmente con la magnitud del valor | **apoyado con datos** (ε²≈3,6%; +0,08 dex por quipu) |
| El 6,6%/0,35 de K-CAT es una definición que cuenta ausentes como cero | **propuesto** (la imitación reproduce 7,72%/0,357; su código no está disponible) |
| La asimetría subsidiary 57/43 | **no apoyado** |
| El 63% de khipus con ambos sentidos | **no apoyado** |
| El 99,8% de Sivan | **rechazado en su forma publicada** |
| Los 709 quipus de K-CAT | **no reproducible** desde esta release (651 xlsx; +9%) |
| Los ocho tipos de documento de Sivan | **especulativo** (sin criterio operacional ni validación externa) |
| El silabario de 13 símbolos y la cobertura del 92,3% | **especulativo** (optimización sobre un quipu, sin código ni nulo de cobertura) |
| La lectura semántica de los quipus en general | **no demostrada** (coinciden OKR, K-CAT y Zenil) |

## 7. Limitaciones

- **Definiciones propias.** K-CAT no publica el código de su restricción padre-hijo; mis D1/D1b/D2 son reconstrucciones razonables, no su definición exacta. Lo mismo vale para el «63%» de KFG: sin su script no puedo saber qué denominador usa.
- **Dependencia de la transcripción.** Todos los conteos heredan errores del KFG/OKR. La ficha de Thompson documenta correcciones que el corpus preparado no incorpora (los quipus del Peabody ni siquiera están).
- **Color.** `cuerdas.csv` da un código por cuerda, no las entradas múltiples de la tabla de colores del KFG; por eso el 27,5%/77,7% solo puede juzgarse como «parcial».
- **Los nulos son conservadores en una dirección y liberales en otra.** Barajar valores dentro del quipu preserva la composición de cada quipu, pero no preserva la posición (decenas/unidades) ni el tamaño relativo de padres e hijos; por eso el nulo de sumas puede subestimar la estructura. En color, barajar etiquetas dentro del quipu ignora la posición de la cuerda, que es un confusor conocido.
- **No hay acceso a los pipelines** de Sivan, Zenil, K-CAT ni rv-repro. Las afirmaciones marcadas «no» o «parcial» no son falsas por eso: son **no auditables** con lo disponible.
- **No usé procedencia de museo como origen** en ningún análisis; `quipus.csv` mezcla «Unknown» con regiones y no lo traté como variable geográfica.

## 8. Para el coordinador

- **De 50 afirmaciones extraídas, 23 son comprobables con los datos del repo, 21 parciales y 6 no.** Las descriptivas se reproducen; las semánticas no son auditables. El `afirmaciones.csv` es la lista de trabajo para la siguiente ronda.
- **La réplica más limpia es Santa Valley:** los seis conteos R/V de Khipu-ML coinciden exactamente (KH0323 310/0 … KH0326 40/69 … KH0328 56/0; agregado 48,97% R), y KH0326 es el único mixto. Eso valida el patrón estructural R/V, no la contabilidad de 367 pesos.
- **El OKR se reproduce al dígito** (619/54.403/110.677/633; 702 KH, 83 ausentes). En cambio, **los 709 quipus de K-CAT no salen de esta release**: hay 651 xlsx y 650 filas. Sus proporciones son buenas, su denominador no.
- **El handedness 54/46 de KFG se sostiene** (54,18%, IC 52,8–55,6, p=1,3e-6 por quipus, Holm 5e-6). Pero **subsidiary 57/43 no** (p=0,87) y **el 63% de khipus con ambos sentidos no se reproduce** (49,9–74,6% según denominador). No usar esas dos cifras.
- **Sivan acierta en lo descriptivo y falla en lo probatorio:** las cuerdas STRING son 1.963/37.206 = 5,28% (él dice 5,35%), pero su 99,8% es falso en la forma publicada: `PLACE_VALUE` no existe en el OKR, `knot_value_type` es el dígito de vueltas (98,5% global, 95,6% en STRING). La ecuación es tautológica o errónea; no valida el silabario.
- **La suma padre=hijos es real pero minoritaria:** 9,06% de los grupos con la regla correcta (4,0% si se exigen ≥2 hijos), muy por encima del nulo (p=0,0005; Holm 0,001). El 6,6%/0,35 de K-CAT solo se aproxima contando hijos ausentes como cero (7,72%/0,357), lo que viola la regla 6 del brief.
- **El color tiene señal, pero no la que sugiere el p-valor:** el KW a nivel de cuerda se reproduce (H=1.450, p=7,5e-280, ε²≈3,6%), y a nivel de quipu sobrevive (394 quipus, +0,077 dex, p=0,001). Es un efecto de ~1,2×, no de orden de magnitud; además las cuerdas blancas valen **más**, no menos.
- **Hueco de cobertura importante:** los conjuntos del Peabody (AS030–AS033G; 10 registros KH0032–KH0041, incluido el anillo de siete quipus) **no están en `cuerdas.csv`**, y 29 quipus del OKR no tienen metadatos en `quipus.csv`. Cualquier conclusión de corpus los ignora.
- **Recomendación para la siguiente ronda:** (1) pedir a K-CAT su definición exacta de grupo padre-hijo y reejecutar con la regla de ausentes; (2) incorporar los quipus del Peabody al corpus preparado; (3) reimplementar el test de entropía R/V de rv-repro con cohorte propia y semilla fija; (4) no invertir más en el silabario de Sivan hasta que publique código y diccionarios, y en su lugar probar su nulo de cobertura (asignaciones aleatorias + morfología) sobre las 1.963 cuerdas STRING.

---

### Archivos

- `afirmaciones.csv` — 50 afirmaciones extraídas.
- `comun.py` — carga de datos y utilidades.
- `01_extraer_afirmaciones.py` — genera `afirmaciones.csv`.
- `02_verificar_corpus.py` — conteos OKR/KFG/K-CAT/Zenil.
- `03_handedness.py` — asimetría L/R, tests de signos, bootstrap, nulo.
- `04_verificar_sivan.py` — cuerdas STRING y `knot_value_type`.
- `05_santa_rv.py` — réplica R/V de Santa Valley.
- `06_verificar_sumas.py` — padre=Σhijos, definiciones y nulo.
- `07_verificar_color.py` — prevalencia de W y color×valor.
- `08_thompson_cobertura.py` — quipus del Peabody y cobertura de identificadores.
- `res_*.json` — salidas numéricas de cada script.

*No se hicieron commits. Todos los archivos están dentro de `analisis/ds/lit_5/`.*
