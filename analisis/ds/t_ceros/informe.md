# Ceros posicionales y alineación de las posiciones decimales en los quipus del KFG

**Equipo:** ceros posicionales (`analisis/ds/t_ceros/`)
**Fecha:** 18 de octubre de 2026
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus del Khipu Field Guide).

---

## 1. Pregunta

1. ¿Se pueden detectar en la columna `nudos` las cuerdas en las que falta una posición decimal intermedia (p. ej. 305: centenas y unidades sin decenas)?
2. ¿La distancia en cm entre racimos ocupa el espacio de la posición faltante, es decir, el cero se codifica como una banda vacía?
3. ¿Alineaban los quipucamayoc las posiciones decimales entre cuerdas, como columnas? ¿Qué tan consistente es esa alineación por quipu?
4. ¿Hay quipus sin alineación, que puedan corresponder a otro tipo de registro?

---

## 2. Datos y método

### 2.1 Corpus y unidad de análisis

- 651 quipus, 57 818 cuerdas. 638 quipus y 40 064 cuerdas tienen al menos un racimo con valor decimal.
- **Unidad de análisis:** el quipu (no la cuerda) para todos los p-valores. Los contrastes de alineación usan solo cuerdas de **nivel 0** (colgantes del cordón principal), porque las subsidiarias se anclan a alturas distintas de su madre y no comparten el mismo origen vertical. Los análisis por grupo usan los grupos de colgantes (`grupo`) dentro de cada quipu.
- Se excluyen las cuerdas sin nudos: `valor = 0` con `nudos` vacío se trata como ausente, no como cero real (regla del BRIEF).

### 2.2 Parser y definiciones

Cada racimo se parsea como `nTIPO(pos_cm,dirección),valor`. El exponente decimal se obtiene contando los ceros finales de `valor` (40 → 1, 300 → 2, 5 → 0), no con `log10` (un `log10` redondeado clasifica mal 6–9 y 40–90; se corrigió durante el análisis). En 99,94 % de las cuerdas con racimos, `cuerda.valor` coincide exactamente con la suma de las contribuciones de `nudos`; las 23 excepciones son el quipu UR044, cuyos racimos no traen valor explícito. Esto valida el uso de `valor` como suma de contribuciones, pero **no** valida que esa suma sea un numeral decimal (ver §3.6).

Categorías de cuerda con ≥2 racimos:

| Categoría | Definición | Cuerdas (todos los niveles) |
|---|---|---:|
| `una` | un solo racimo con valor | 23 155 |
| `reg` | exponentes únicos y estrictamente decrecientes con la posición | 13 832 |
| `dup` | algún exponente repetido (dos o más racimos en la misma posición decimal) | 2 916 |
| `inv` | exponentes únicos pero con orden vertical invertido | 161 |

- **Cero posicional interno:** cuerda `reg` en la que falta un exponente entre el mínimo y el máximo (p. ej. exponentes {2,0}: falta 1).
- **Ancho de banda del quipu (`w`):** mediana de las distancias entre racimos consecutivos con Δexponente = 1 en el mismo quipu.
- **Ratio del hueco:** `Δpos / (Δexponente × w)`. Si el cero ocupa exactamente una banda, el ratio vale 1.
- **Dispersión de banda:** MAD (mediana de desviaciones absolutas) de las posiciones de los racimos del mismo exponente entre cuerdas. Se normaliza por el espaciado entre bandas: `rel = MAD / espaciado`.
- **Alineación local:** la misma dispersión calculada dentro de cada `grupo` de colgantes.

### 2.3 Modelos nulos

| Nulo | Qué preserva | Qué destruye | Uso |
|---|---|---|---|
| **N1 `startperm`** (primario) | el patrón interno de cada cuerda (n.º de racimos y distancias), y la distribución observada de alturas de inicio de bloque del quipu | la correspondencia entre una cuerda concreta y su altura | alineación de bandas a nivel de quipu |
| **N2 `jitter ±2 cm`** (sensibilidad) | el patrón interno y la altura aproximada | las filas precisas | alineación fina |
| **N3 `free`** (sensibilidad, solo como cota superior) | el patrón interno | toda la colocación vertical | no se usa para conclusiones |
| **N4 grupos barajados** | tamaños de grupo y patrón interno | la asignación de cuerdas a grupos | ¿la alineación es local al grupo? |
| **N5 posición aleatoria en el hueco** | el hueco de la cuerda | la posición de la banda faltante | localización del cero |

- 99 réplicas para N1/N2 (p mínimo 0,01), 199 para N3/N5, 499 para N4.
- Semillas fijas: 20261017, 20261018, 20261019, 20261020, 20261021.
- Corrección de comparaciones múltiples: **Benjamini–Hochberg (BH-FDR)** por familia de pruebas; se indica el número de pruebas y el q-valor. Para las pruebas únicas (escalamiento del hueco, gradiente por posición) se aplica Holm a las 2–3 pruebas de la familia.
- Los p-valores empíricos tienen resolución limitada (p. ej. 0,01 con 99 réplicas). Cuando el q-valor no puede alcanzar 0,05 por resolución, se reporta el **tamaño de efecto** y no se fuerza una dicotomía.

---

## 3. Resultados

### 3.1 ¿Cuántos ceros posicionales hay?

En las 13 832 cuerdas `reg` (todos los niveles), **726 cuerdas (5,25 %) tienen al menos un cero interno**, con **747 posiciones cero** en total, distribuidas en **168 quipus**.

Restringido a nivel 0 (la base de los análisis de alineación): 11 471 cuerdas `reg`, **658 con cero (5,74 %)**, **679 posiciones cero**, **163 quipus**. Entre las cuerdas `reg` de nivel 0 con **3 o más dígitos** (4 670), **658 (14,1 %)** tienen al menos un cero interno.

- Distribución por quipu (nivel 0): mediana 2 ceros, p75 = 6, p90 ≈ 10, máximo 37 (UR001), 34 (UR268), 23 (UR1109), 20 (UR020).
- Posición faltante: decenas 495, centenas 161, millares 22, decenas de millar 1. Es lo esperable: el cero interno más frecuente es el de las decenas.
- Ejemplos: 101, 104, 204, 305, 601, 1001, 1078.

**Ceros finales (no internos).** 5 344 cuerdas de un solo racimo tienen un valor múltiplo de 10 (23 % de las 23 155 cuerdas de un racimo); 2 368 son potencias exactas de 10 (10, 100, 1 000…). En esos casos el cero se codifica por el **final de la cuerda** (no hay racimos debajo), no por un hueco intermedio. Es un modo complementario de cero posicional y no se mezcla con el conteo anterior.

**Frecuencia de ceros internos frente a dígitos aleatorios.** Entre las cuerdas `reg` de nivel 0 con 3, 4 y 5 dígitos, la fracción con al menos un cero interno es 11,4 %, 21,8 % y 30,5 %, frente a 10 %, 19 % y 27,1 % si los dígitos internos fueran uniformes 0–9. Los ceros son compatibles con un dígito más, con una leve sobrerrepresentación de 1–3 puntos. Esto es **descriptivo**, no una prueba de que el cero se codifique espacialmente: los dígitos de un registro real no tienen por qué ser uniformes (ver §4.1).

### 3.2 El hueco mide una banda: el cero ocupa la posición que falta

Para 659 huecos de nivel 0 con ancho de banda disponible en su quipu:

| Métrica | Valor |
|---|---:|
| Ratio `Δpos/(Δe·w)` mediana | **0,958** |
| IQR | 0,83 – 1,05 |
| Dentro de 0,8–1,2 | **68,9 %** |
| Cuerdas con Δe=2 y Δe=1 en la misma cuerda | 201 |
| Ratio mismo-cord (Δe=2) mediana | **1,89** (IQR 1,57–2,18) |
| Contraste vs ratio = 1 (sin banda extra) | Wilcoxon, **p = 5,8 × 10⁻³³** |
| Contraste vs ratio = 2 (dos bandas) | Wilcoxon, p = 6,7 × 10⁻⁴ (mediana algo menor que 2) |
| Quipus con ≥3 huecos | 77 |
| CV del ratio dentro del quipu (mediana) | **0,113** |

El patrón es muy regular: **un lugar saltado ocupa aproximadamente el espacio de una banda**, y dentro de un mismo quipu el ratio tiene un CV de ~11 %. El ratio es incluso **más regular que los anchos de banda normales** de la misma cuerda (en los 75 quipus con ≥3 huecos y ≥3 anchos: CV mediano 0,10 vs 0,19; Wilcoxon p = 7,1 × 10⁻⁹; 80 % con CV_cero < CV_banda). Para Δe=3 (20 casos) el hueco se comprime: ratio 0,79 (IQR 0,68–0,87), es decir, unos 2,4 anchos de banda para 3 lugares; el escalamiento es monótono pero no perfectamente lineal.

**Ejemplos con Δe=2 (un cero intermedio):**

| Quipu | Cuerda | Valor | Racimos (cm) | Hueco | `w` del quipu | Ratio |
|---|---|---|---:|---:|---:|---:|
| AS029 | p49 | 204 | 2S 7,0 → 4L 20,0 | 13,0 | 6,5 | **2,00** |
| MM001 | p111 | 204 | 2S 10,0 → 4L 25,0 | 15,0 | 7,5 | **2,00** |
| AS115 | p14 | 205 | 2S 6,0 → 5L 24,5 | 18,5 | 9,0 | **2,06** |
| UR085 | p26 | 205 | 2S 19,0 → 5L 36,0 | 17,0 | 9,0 | **1,89** |
| AS133 | p8 | 305 | 3S 6,0 → 5L 24,5 | 18,5 | 14,0 | 1,32 |

El último caso (AS133) muestra que no todos los huecos son exactamente dos bandas: hay quipus con anchos de banda heterogéneos o con errores de medición. En conjunto, sin embargo, la mediana es 0,96 y el 69 % cae en 0,8–1,2.

**Nivel de evidencia:** *apoyado con datos* para “el hueco ocupa una banda”. **Salvedad de circularidad:** los valores de `nudos` son lecturas expertas (Ascher/Urton/KFG), y una de las convenciones documentadas asigna el valor “por posición del nudo” (Thompson 2026). Si el anotador usó el hueco para decidir que había un lugar saltado, esta prueba es una **verificación de coherencia interna**, no un descubrimiento independiente. La prueba realmente independiente es la alineación física de bandas entre cuerdas (§3.3–3.5), que usa solo posiciones.

### 3.3 ¿Se alinean las posiciones decimales entre cuerdas?

Se analizaron 486 quipus de nivel 0 con ≥5 cuerdas, ≥8 racimos y ≥2 bandas decimales.

**Dispersión de la misma banda entre cuerdas** (MAD observada vs nulo N1 `startperm`):

| Métrica | Observado | Nulo N1 (mediana) |
|---|---:|---:|
| MAD de banda (mediana, cm) | **0,91** | 2,23 |
| Fracción de racimos a ≤1 cm de la mediana de su banda | **0,64** | 0,38 |
| Ratio observado/nulo (mediana) | **0,49** (IQR 0,30–0,75) | — |

- **BH-FDR:** 244/486 quipus con q < 0,05 (50,2 %). Entre los quipus con **≥3 bandas**, 190/267 (71,2 %). Con el nulo N2 (`jitter ±2 cm`), 219/486 (45,1 %) y 137/267 (51,3 %). Los dos nulos acotan el efecto.
- **Tamaño de efecto (independiente de la potencia):** el ratio observado/nulo es < 0,8 en **77 %** de los 486 quipus (85 % con 3 bandas, 92 % con 4 bandas, 100 % con 5–6).
- El efecto no es un artefacto del tamaño: entre quipus con ≥3 bandas y ≥20 cuerdas, 80,5 % son significativos y la mediana del ratio es 0,41; en quipus pequeños con 3 bandas, 34–40 % son significativos pero el ratio mediano sigue siendo 0,43–0,46. La significación crece con el tamaño (potencia), el **tamaño de efecto no**.
- La variabilidad del largo de las cuerdas **no explica** la alineación: correlación entre ratio y CV del largo de las cuerdas ≈ 0,00 (p = 0,99). Los quipus con cuerdas más largas tienden a estar algo *mejor* alineados (rho = −0,17, p = 1,1 × 10⁻⁴), no peor.

**El gradiente por posición decimal.** La dispersión disminuye cuanto más alta es la posición:

| Exponente | Bandas (quipu × posición) | Racimos por banda (mediana) | MAD mediana (cm) | p75 (cm) |
|---:|---:|---:|---:|---:|
| 0 (unidades) | 528 | 22 | **1,00** | 1,50 |
| 1 (decenas) | 480 | 16 | **0,75** | 1,00 |
| 2 (centenas) | 242 | 12 | **0,50** | 1,00 |
| 3 (millares) | 83 | 9 | **0,50** | 0,62 |
| 4 (decenas de millar) | 12 | 6,5 | **0,00** | 0,31 |

Contrastes pareados dentro del quipu: unidades > decenas (Wilcoxon p = 2,6 × 10⁻¹⁹) y decenas > centenas (p = 1,4 × 10⁻¹⁷); Holm a 2 pruebas sigue < 10⁻¹⁶. Las unidades son más variables porque allí están los nudos largos y en figura de ocho; pero el gradiente persiste **dentro de los nudos simples**: para racimos tipo S, MAD mediana 0,75 (decenas), 0,50 (centenas), 0,50 (millares), 0,00 (decenas de millar).

**¿La alineación es solo de los nudos largos?** No. Restringiendo a racimos tipo S (los que codifican decenas/centenas/millares), la dispersión relativa mediana es 0,143, prácticamente igual que la de todos los racimos (0,150); la correlación entre ambas es 0,86 y en 59 % de los quipus la S es igual o mejor. La alineación no se explica porque los nudos largos de las unidades estén todos a la misma altura.

![Bandas decimales y tamaño del hueco](fig_alineacion.png)

*Figura. (A) UR1120: escalera decimal compartida; (B) AS008: bandas globales anchas pero grupos internos alineados; (C) UR1095: bandas desordenadas; (D) distribución del ratio del hueco (nivel 0, n = 658 huecos con ratio < 3; mediana 0,96).*

**Ejemplo de quipu alineado (UR1120, 32 cuerdas, 122 racimos):**

| Posición | Mediana (cm) | MAD (cm) | n |
|---|---:|---:|---:|
| unidades | 35,5 | 1,0 | 27 |
| decenas | 27,5 | 0,5 | 30 |
| centenas | 18,75 | 0,5 | 30 |
| millares | 11,5 | 0,5 | 25 |
| decenas de millar | 5,0 | 0,5 | 10 |

Las bandas están separadas ~7–8 cm y cada una tiene una dispersión de 0,5–1 cm: es una escalera decimal compartida por las 32 cuerdas.

### 3.4 La alineación es local a los grupos de colgantes

La dispersión de banda **dentro de cada grupo** es mucho menor que la del quipu completo:

- 1 295 grupos de ≥5 cuerdas en 342 quipus: `rel_g` mediana **0,062** (IQR 0,037–0,103); 92 % de los grupos tiene `rel_g ≤ 0,2`.
- En los 263 quipus con ≥2 grupos analizables, la dispersión media por grupo es menor que la del quipu completo en **86,3 %** de los casos (mediana 0,074 vs 0,154).
- Frente a un nulo que **baraja las etiquetas de grupo** preservando tamaños (499 réplicas), 124/263 quipus (47 %) tienen q < 0,05; la mediana del ratio grupo/nulo es 0,61. Es decir, los grupos reales son unidades de alineación más allá de la mera partición aleatoria, aunque el efecto no es universal.
- **12 de los 21 quipus con mala alineación global** (`rel > 0,5`) tienen, sin embargo, `rel_g < 0,2`: su escalera es local, no única para todo el quipu.

Ejemplos:

| Quipu | Cuerdas | Bandas | `rel` del quipu | `rel_g` mediana | Interpretación |
|---|---:|---:|---:|---:|---|
| AS008 | 175 | 4 | 0,64 | **0,11** | bandas globales anchas, grupos muy alineados |
| UR022 | 153 | 3 | 0,65 | **0,06** | ídem |
| QU019 | 166 | 3 | 0,80 | **0,05** | ídem |
| UR1175 | 185 | 3 | 0,54 | **0,04** | ídem |
| UR1120 | 32 | 5 | 0,07 | 0,07 | alineación global y local |
| UR1095 | 92 | 3 | 4,08 | 1,51 | sin alineación ni global ni local |

**Interpretación:** el quipucamayoc no usaba una única cuadrícula para todo el quipu; alineaba las posiciones dentro de cada grupo (y a veces dentro de secciones), y distintos grupos podían usar offsets o escalas distintas. Por eso un test a nivel de quipu subestima la alineación real. **Nivel de evidencia:** *apoyado con datos* para la estructura local; *propuesto* para la lectura de que los grupos son las “columnas” de un registro tabular.

### 3.5 ¿El cero cae en la columna correcta?

Para 555 huecos de nivel 0 que tienen al menos otro racimo del mismo exponente en su grupo, se comparó la posición interpolada del hueco (`p_hat`, interpolación lineal entre los dos racimos vecinos) con la mediana de la banda del exponente faltante en las **otras cuerdas del mismo grupo**:

| Métrica | Valor |
|---|---:|
| Distancia mediana `|p_hat − banda_grupo|` | **0,75 cm** |
| ≤1 cm | **59,5 %** |
| ≤1,5 cm | **73,0 %** |
| Huecos sin banda del mismo exponente en su grupo | 124/679 (18,3 %) |

La localización depende de la alineación del grupo, como predice la hipótesis:

| Alineación del grupo (`rel_g`) | n huecos | Distancia mediana | ≤1 cm | ≤1,5 cm |
|---|---:|---:|---:|---:|
| ≤0,10 (muy alineado) | 284 | **0,75 cm** | **67,6 %** | 81,7 % |
| 0,10–0,20 | 84 | 1,50 cm | 38,1 % | 59,5 % |
| >0,20 (poco alineado) | 39 | **3,50 cm** | **17,9 %** | 33,3 % |

- Spearman entre `rel_g` y la distancia al hueco: **rho = 0,31, p = 1,7 × 10⁻¹⁰**.
- Mann–Whitney grupos muy alineados vs poco alineados: **p = 4,4 × 10⁻¹⁰**; diferencia de medianas −2,75 cm (bootstrap IC 95 % −3,75 a −1,00).
- A nivel de quipu completo (mediana de la banda en otras cuerdas, no del grupo; n = 690 huecos): distancia mediana 1,25 cm, 47,5 % ≤1 cm; en 98,5 % de los huecos la banda verdadera está más cerca que las bandas adyacentes (mediana de la distancia a la banda adyacente: 9,0 cm).

**Lectura:** cuando las bandas están alineadas, el hueco de un cero coincide con la columna del exponente faltante; cuando no lo están, el hueco no se puede localizar en una columna. Esto es exactamente lo que se esperaría si el cero se representara como una **celda vacía de una tabla decimal**. **Nivel de evidencia:** *apoyado con datos* (con la salvedad de que la etiqueta del exponente viene del registro experto).

### 3.6 Quipus sin alineación y posibles “otros registros”

#### (a) Cuerdas con más de un racimo en la misma posición decimal

2 916 cuerdas (todos los niveles; 2 253 de nivel 0) tienen exponentes repetidos. De ellas, **2 041 son solo de unidades** (varios nudos largos en la misma posición 10⁰). Afectan a **229/572 quipus (40 %)** con cuerdas multirracimo; **151/572 (26,4 %)** tienen al menos una cuerda con unidades duplicadas. Es del mismo orden que el >20 % de “nether knots” reportado por Hyland (2024) para el OKR, aunque la definición no es idéntica.

Estas cuerdas no son numerales decimales: el valor de `cuerda.valor` es la **suma** de varios racimos del mismo orden. Ejemplos:

- UR050: 164 cuerdas, 501 racimos, **todos tipo L y todos de unidades**; valores 5–22; cuerdas de 70–100 cm.
- UR054: 312 racimos, 311 L de unidades.
- UR052: 312 racimos, 312 L, 309 de unidades.
- UR112: 76 cuerdas, 115 L de unidades.
- UR039 (el quipu de calibración de Sivan 2026): 212 racimos, 169 L de unidades y 42 S de decenas; pureza 0,83.

#### (b) Quipus dominados por un patrón de “secuencia”

Defino **pureza** de una cuerda como la fracción de sus racimos que caen en su exponente modal. Un quipu es “de secuencia” si pureza ≥ 0,8 y tiene ≥5 cuerdas multirracimo. Hay **28 quipus** así (4,3 % del corpus), entre ellos UR050, UR054, UR052, UR055, UR051, UR110, UR112, UR144, UR193, UR039, HP019/HP020, JC012, MM019. AS014 es un caso mixto (pureza 0,76) con el mismo patrón de fondo.

No son “quipus sin nudos” ni quipus rotos: son quipus con cuerdas que contienen **series de nudos del mismo orden** (p. ej. 4L, 5L, 5L a 15, 30 y 55 cm), no un numeral de varias posiciones. El `valor` suma esos racimos, pero esa suma no es una lectura decimal del objeto. **Nivel de evidencia:** *apoyado con datos* para el patrón; *propuesto* para la interpretación como “otro tipo de registro” (tally, secuencia, lista, o nudos inferiores).

#### (c) Quipus con bandas presentes pero mal alineadas

31 quipus tienen `rel_g > 0,3` o, sin datos de grupo, `rel_q > 0,4`. Los casos con más cuerdas: KH0001 (96), UR1095 (89), UR203 (87), UR1087 (67), UR213 (57), AS014 (42), UR183 (25), UR059 (24), UR215 (22), UR291A (21), KH0032 (18), UR177 (18), AS037 (16), AS036 (15), UR1146 (16). Algunos son de secuencia; otros muestran las bandas **desordenadas** (UR1095: unidades 15,8 cm, decenas 18,0 cm, centenas 17,8 cm), lo que sugiere error de medición, inversión de la cuerda o un registro no decimal.

#### (d) Clasificación descriptiva

Con umbrales explícitos (no son una prueba):

| Clase | n | Criterio |
|---|---:|---|
| alineado | 298 | ratio obs/nulo ≤ 0,8 |
| alineación local solamente | 24 | `rel_q > 0,4` y `rel_g ≤ 0,15` |
| débil | 39 | resto con datos suficientes |
| sin alineación local | 31 | `rel_g > 0,3` (o sin grupo y `rel_q > 0,4`) |
| secuencia no decimal | 28 | pureza ≥ 0,8 y ≥5 cuerdas multirracimo |
| pocos datos | ~230 | <5 cuerdas multirracimo; no clasificable |

---

## 4. Controles, resultados negativos y amenazas

### 4.1 Circularidad de la asignación de valor

Es la amenaza principal. La columna `nudos` no es una medición cruda: es una **lectura** que asigna a cada racimo su valor decimal. Thompson (2026) documenta que los Ascher asignan valor “por posición del nudo” y Urton “por tipo de nudo”; el KFG mezcla ambas tradiciones. Si el anotador decidió que había un lugar saltado porque el hueco era grande, el resultado de §3.2 es una comprobación de coherencia, no una prueba independiente.

Por eso el argumento se apoya en tres capas:

1. **Geometría del hueco** (§3.2): el hueco escala con Δe y es regular dentro del quipu. Aun si la etiqueta se asignó por el hueco, la regularidad cuantitativa (ratio 0,96; CV 0,11) es un hecho del registro.
2. **Alineación física de bandas** (§3.3–3.4): usa posiciones en cm de cuerdas distintas; no depende de que el hueco se haya usado para etiquetar. El hecho de que las bandas del mismo exponente estén más juntas que el nulo es una propiedad física.
3. **Localización del hueco en la columna del grupo** (§3.5): el hueco coincide con la banda que otras cuerdas del mismo grupo tienen a esa altura.

Ninguna de las tres capas demuestra por sí sola que el quipucamayoc “codificara el cero”; en conjunto, la lectura es consistente y queda **apoyada con datos**, no bien apoyada.

Tampoco podemos estimar la tasa de ceros **no** codificados: si un escriba omitía el hueco, el valor se leería como 35 en lugar de 305 y no quedaría rastro en la base. Los 747 ceros enumerados son, por construcción, solo aquellos que tienen huella espacial (un hueco entre racimos).

### 4.2 Sensibilidad a las notas de revisión de valor

La columna `alt` está vacía, pero **63 cuerdas `reg` de nivel 0 tienen notas del tipo `Alt.Value`, `value changed` o `Originally`**. De ellas, **42 (66,7 %) tienen un cero interno**, frente al 5,4 % de las demás (Fisher OR = 35,0; p = 1,8 × 10⁻³⁷). El patrón típico es una revisión que **promueve el racimo más alto un lugar** sin añadir el racimo intermedio:

- UR011 p84: `1S(7,5)=100; 5L(24)=5` → valor 105; nota “value changed. Originally 15”.
- UR015 p15: `300U(4,5)=300; 9L(19,5)=9` → 309; “value changed; was 39”.
- QU022 p4: `1S(5,5)=100; 4L(8)=4` → 104; “Alt.Value: 14”.
- MM019 p1: `2S(3,5)=200; 1E(37)=1` → 201; “Alt.Value: 21”.

La revisión puede ser correcta (el nudo era realmente de centenas y el cero es real) o puede ser un artefacto (el valor se cambió sin cambiar los nudos). También puede reflejar un cambio de criterio de lectura (posición vs tipo de nudo; Thompson 2026). Las notas no permiten decidir. La revisión se concentra en pocos quipus: UR011 (14 cuerdas, 15 ceros), UR020 (10, 14), UR018 (6, 6), QU022 (3, 3), UR015 (3, 3), UR002 (2, 2). Esos quipus están **bien alineados** (ratio obs/nulo 0,37–0,67), lo que sugiere que la relectura pudo apoyarse en las bandas físicas; no se puede separar la corrección del sesgo.

**Sensibilidad:** excluyendo las 42 cuerdas con nota de revisión, quedan **616 cuerdas con cero y 632 posiciones** (frente a 658/679). El ratio del hueco apenas cambia: mediana **0,962** (vs 0,958), 71,6 % dentro de 0,8–1,2 (vs 68,9 %). El resultado geométrico es robusto; lo que cambia es el **conteo exacto** de ceros (≈7 % del total queda en duda). También hay casos en la dirección opuesta: MM002 p38 (`3S=30; 2S=2` → 32, “Alt.Value: 320”) donde la lectura alternativa *crearía* un hueco que la lectura elegida no tiene. Las notas de rotura/reparación no explican los huecos: solo 4 de las 56 cuerdas con esa nota tienen uno (7,1 % vs 5,4 % de las demás); la terminación rota/cortada/ravellada tampoco (13,4 % vs 13,8 %).

**Nivel de evidencia:** *apoyado con datos* para la asociación revisión–hueco; *no resuelto* si la revisión corrige un cero real o lo inventa. Es una limitación importante para cualquier análisis que use `valor` como numeral.

### 4.3 Las filas no son una cuadrícula rígida de 0,5 cm

Prueba libre de etiquetas: fracción de racimos cuya altura exacta (redondeada a 0,5 cm) aparece en otra cuerda. Observado 0,79 vs nulo 0,71 (desplazamientos discretos de 0,5 cm, ±2 cm); exceso mediano 4,5 puntos porcentuales; 74 % de los quipus con observado > nulo, pero **solo 127/562 p < 0,05 y 0/562 q < 0,05** (BH). Es decir, las coincidencias exactas son mucho más débiles que la alineación estadística de bandas. La alineación es real pero **no es una cuadrícula perfecta**: hay ruido de medición, variación entre cuerdas y distintos offsets por grupo.

### 4.4 La alineación no es universal

- 29 % de los quipus con ≥3 bandas no alcanzan q < 0,05 frente al nulo conservador; ~12 % tienen ratio > 0,8 (peor o igual que el nulo).
- 41 % de los huecos quedan a >1 cm de la banda mediana de su grupo; 18 % no tienen ninguna banda del mismo exponente en su grupo.
- 231 quipus no son clasificables por tener <5 cuerdas multirracimo. La alineación podría estar presente pero no es medible con esta resolución.

### 4.5 No hay un patrón claro por procedencia ni por investigador

- Tasa de q < 0,05 por prefijo: AS 36 %, HP 50 %, JC 50 %, KH 54 %, MM 47 %, QU 65 %, UR 54 %; chi² = 10,6, gl 6, **p = 0,10**. No se rechaza la homogeneidad; no hay evidencia de que la alineación sea un artefacto de un solo transcriptor.
- La procedencia conocida se asocia a mayor significación (63/99 vs 181/387; Fisher p = 0,003), pero los quipus con procedencia conocida son también **más grandes** (mediana 48 vs 19,5 cuerdas) y tienen más bandas (3 vs 2). Es un confundido por tamaño/potencia, no una prueba de geografía. No usar el museo como origen (regla del BRIEF).

### 4.6 Otras limitaciones

- Solo se analizan cuerdas de nivel 0 para la alineación. Las subsidiarias se anclan a alturas distintas; una reconstrucción 3D con la posición de anclaje (columna `Position` del xlsx, no incluida en `cuerdas.csv`) permitiría testear su alineación.
- Las posiciones son distancias a lo largo de cada cuerda, no coordenadas 3D; la curvatura del cordón principal y la orientación del quipu no se modelan.
- Los análisis por grupo usan grupos con ≥5 cuerdas y ≥8 racimos; aun así, `rel_g` es inestable cuando el grupo tiene solo 2 bandas o un espaciado <2 cm (el denominador es pequeño). La clasificación por clases es orientativa, no una partición definitiva.
- Las posiciones están redondeadas a 0,5 cm. No podemos separar por completo la alineación del objeto de una posible plantilla o redondeo del transcriptor; la verificación con imágenes (§6.7) es la única que lo resolvería.
- El parser descarta 23 segmentos vacíos/malformados y 42 racimos sin valor explícito (64 490 segmentos totales; <0,1 %). 50 cuerdas de nivel 0 tienen `largo = 0` o faltante (0,18 %); sus posiciones se usan igual.
- El corpus KFG no es una muestra aleatoria; 651 quipus, con sobrerrepresentación de UR y de procedencia desconocida.
- `alt` está vacío en todo el corpus: no hay lecturas alternativas para comparar.
- No se verifica contra imágenes ni contra el OKR cuerda a cuerda en esta tarea; los valores y posiciones se toman de `cuerdas.csv`.
- Los p-valores empíricos con 99 réplicas tienen resolución 0,01; los conteos BH son aproximados en el límite.

---

## 5. Nivel de evidencia

| Afirmación | Nivel | Comentario |
|---|---|---|
| Existen cuerdas con un cero posicional interno y se pueden enumerar (726 cuerdas, 747 ceros, 168 quipus; nivel 0: 658/679/163) | **Apoyado con datos** (descriptivo) | Conteo reproducible, pero depende de la lectura de `nudos` |
| El hueco de un cero ocupa ~una banda: ratio 0,96; mismo-cord 1,89; CV por quipu 0,11; p = 5,8 × 10⁻³³ vs 1 | **Apoyado con datos** | Fuerte, con salvedad de circularidad (§4.1) |
| Las bandas del mismo exponente se alinean entre cuerdas más de lo esperado por un nulo que preserva el patrón interno y la distribución de inicios | **Apoyado con datos** | 50 % q < 0,05 global; 71 % con ≥3 bandas; tamaño de efecto ratio 0,49 |
| La alineación es local a los grupos de colgantes, no una única cuadrícula del quipu | **Apoyado con datos** | 86 % de los quipus con grupos: `rel_g` < `rel_q`; 12/21 quipus globalmente anchos son localmente tight |
| El cero cae en la columna del exponente faltante cuando el grupo está alineado | **Apoyado con datos** | 68 % ≤1 cm en grupos tight vs 18 % en loose; rho = 0,31, p = 1,7 × 10⁻¹⁰ |
| Las posiciones altas (centenas/millares) se alinean más que las unidades | **Apoyado con datos** | MAD 1,0 → 0,75 → 0,5 cm; p pareado ~10⁻¹⁷ |
| Hay ~28 quipus con un régimen de “secuencia” (varios nudos del mismo orden), no numerales decimales | **Apoyado con datos** para el patrón; **propuesto** para la interpretación | UR050, UR054, UR052, UR112, UR039; AS014 es un caso mixto |
| Los nudos inferiores/unidades duplicadas son comunes (26 % de los quipus con cuerdas multirracimo) | **Apoyado con datos** | Consistente con Hyland 2024 (>20 % en OKR), definición no idéntica |
| ≈7 % de las posiciones cero podrían ser artefactos de revisión de valor, no ceros físicos | **No resuelto** | 42 cuerdas / 47 posiciones (6,9 %) con notas “value changed/Alt.Value”; el `alt` está vacío |
| La alineación es una cuadrícula exacta de 0,5 cm | **Refutado / negativo** | Exceso de coincidencias exactas pequeño; 0/562 q < 0,05 |
| La alineación se explica por el largo de las cuerdas | **Refutado / negativo** | rho ≈ 0 con el CV del largo |
| La alineación varía por investigador o procedencia | **No apoyado** | chi² por prefijo p = 0,10; procedencia confundida con tamaño |
| El quipucamayoc “usaba columnas decimales” conscientemente | **Propuesto** | Consistente con Locke 1928 (“columnas de 1000's/100's/10's/1's”) y con los datos, pero no bien apoyado |

---

## 6. Ideas para la siguiente ronda

1. **Reconstruir la coordenada vertical global** de todas las cuerdas (nivel 0 y subsidiarias) usando la columna `Position` de los xlsx (posición de anclaje de cada subsidiaria en su madre). Testear si la alineación local se extiende a todo el árbol cuando se suma el offset de anclaje.
2. **Validar los ceros con aritmética independiente**: en quipus con cuerdas superiores o sumas Ascher, comprobar si el valor 305 (con cero) entra en la suma como 305 y no como 35. Eso rompería la circularidad de la lectura.
3. **Comparar con el OKR**: extraer `knot_cluster.START_POS` y `knot_value_type` para los mismos KH y repetir el análisis de bandas; si las posiciones son mediciones independientes, la alineación física se puede replicar sin la lectura KFG.
4. **Modelar la elección de banda** con un modelo jerárquico (banda dentro de grupo dentro de quipu) para separar la varianza de medición de la varianza de colocación.
5. **Estudiar los 28 quipus de secuencia**: ¿son un registro de conteo, una lista de cantidades, o nudos inferiores? Comparar con la tipología de Hyland y con los quipus de Pachacamac/Armatambo.
6. **Analizar la dirección y el tipo de nudo** en los huecos: si el cero se marca con un nudo especial o con un espacio, y si los quipus con más ceros son los de valores más largos.
7. **Reconstruir la columna `alt` desde las notas** (`Alt.Value`, `value changed`, `Originally`) y auditar las revisiones de UR011, UR020, UR018, QU022 y UR015: sin eso, ~7 % de los ceros queda en duda.
8. **Testear la hipótesis de la “columna” con imágenes**: en 2–3 quipus bien conservados, verificar si las bandas de 0,5 cm son reales o si la alineación es solo un efecto de redondeo del registro.

---

## 7. Para el coordinador

- **Sí hay ceros posicionales y son frecuentes:** 726 cuerdas (5,25 % de las cuerdas decimales regulares) con 747 ceros internos, en 168 quipus; nivel 0: 658 cuerdas, 679 ceros, 163 quipus. El cero más común es el de las decenas (495 casos), luego centenas (161).
- **Cuidado con las revisiones de valor:** 63 cuerdas tienen notas “Alt.Value/value changed/Originally” y 42 de ellas (66,7 %) tienen un cero interno; las revisiones suelen promover el nudo más alto un lugar (15 → 105) y pueden crear el hueco. Excluyéndolas quedan 616 cuerdas / 632 ceros (≈7 % menos), pero el ratio del hueco casi no cambia (0,962 vs 0,958). El `alt` está vacío: la ambigüedad no está resuelta.
- **El hueco mide una banda:** el ratio `Δpos/(Δe·w)` tiene mediana **0,96** (IQR 0,83–1,05); cuando se compara dentro de la misma cuerda, el hueco de un cero es **1,89×** el ancho de banda (p = 5,8 × 10⁻³³). El CV del ratio dentro de un quipu es **0,11**: el cero se comporta como una celda vacía regular.
- **Las posiciones decimales se alinean entre cuerdas, pero no en todos los quipus:** la MAD de la misma banda es **0,91 cm** frente a **2,23 cm** del nulo; 50 % de los 486 quipus son significativos (71 % de los que tienen ≥3 bandas), y el tamaño de efecto es < 0,8 en el 77 %. No es una cuadrícula exacta de 0,5 cm (ese test no sobrevive a BH).
- **La alineación es local a los grupos de colgantes:** la dispersión dentro del grupo es **0,062** (6 % del espaciado) frente a **0,154** del quipu completo; en 86 % de los quipus el grupo es más tight que el quipu, y 47 % supera un nulo de particiones aleatorias del mismo tamaño (mediana del ratio 0,61). 12 de los 21 quipus “desalineados” a nivel global están bien alineados por grupos. **El quipu no es la unidad natural de alineación; el grupo sí.**
- **Los ceros caen en la columna correcta cuando el grupo está alineado:** en grupos con `rel_g ≤ 0,1`, el 68 % de los huecos está a ≤1 cm de la banda del exponente faltante (82 % a ≤1,5 cm); en grupos poco alineados, solo el 18 %. Spearman 0,31 (p = 1,7 × 10⁻¹⁰). Es la evidencia más directa de “celda vacía en una tabla decimal”.
- **El patrón no es universal:** 29 % de los quipus con ≥3 bandas no superan el nulo conservador; 41 % de los huecos están a >1 cm de la banda de su grupo; 231 quipus no son clasificables por tener pocas cuerdas multirracimo. No hay señal por investigador (p = 0,10) ni por región (confundida con tamaño).
- **Hay un grupo de ~28 quipus que no son numerales decimales:** cuerdas con series de nudos del mismo orden (UR050: 501 nudos largos, todos de unidades; UR054, UR052, UR112, UR039; AS014 es el caso mixto más claro). En ellos `valor` es una suma, no un número posicional. Cualquier análisis de sumas/aritmética debería excluirlos o tratarlos aparte.
- **Los nudos de unidades duplicados son comunes:** 151/572 quipus (26,4 %) tienen al menos una cuerda con varias unidades; es del orden del >20 % de “nether knots” de Hyland (2024). La base no permite distinguir si son nudos inferiores, secuencias o errores.
- **Recomendación prioritaria:** repetir el análisis con coordenadas verticales globales (incluyendo subsidiarias y el punto de anclaje) y validar los ceros contra sumas independientes (cuerdas superiores/Ascher). Sin eso, la lectura “el cero es una banda vacía” queda **apoyada con datos**, no bien apoyada, por la circularidad de la asignación de valor en `nudos`. Para la siguiente ronda, no usar el quipu como unidad de alineación: usar **grupo × posición decimal** y reportar siempre el tamaño de efecto (ratio obs/nulo) además del p-valor, porque la significación depende fuertemente del número de cuerdas y de bandas.

---

## 8. Reproducibilidad

Scripts en `analisis/ds/t_ceros/`:

| Script | Qué hace |
|---|---|
| `parse_quipus.py` | parser de `nudos`, exponente decimal, contribuciones |
| `explorar.py` | carga y primeras distribuciones |
| `alineacion.py` | primer test de filas y nulo de desplazamiento |
| `bandas2.py` | test principal de alineación con nulos N1/N2 (genera `bandas_quipu2.csv`) |
| `grupos_bandas.py` | dispersión de bandas por grupo (genera `grupos_bandas.csv`) |
| `grupos_alineacion.py` | nulo de grupos con startperm (genera `grupos_bandas_null.csv`) |
| `grupos_vs_quipu.py` | test grupo vs quipu con grupos barajados (genera `grupos_vs_quipu.csv`) |
| `filas_exactas.py` | test libre de etiquetas de coincidencias exactas (genera `filas_exactas.csv`) |
| `ceros_localizacion.py` | localización del hueco en la banda del grupo y del quipu (genera `ceros_grupo.csv`, `ceros_localizacion.csv`) |
| `integrar.py` | une cuerdas, quipus y ceros (genera `quipus_alineacion.csv`, `ceros_detalle.csv`) |
| `clasificar.py` | clasificación descriptiva (genera `clasificacion.csv`) |
| `figura.py` | figura resumen (genera `fig_alineacion.png`) |
| `resumen_cifras.py` | cifras canónicas (genera `cifras.json`) |

Los CSV intermedios (`bandas_quipu2.csv`, `grupos_bandas.csv`, `grupos_vs_quipu.csv`, `filas_exactas.csv`, `clasificacion.csv`, `ceros_detalle.csv`, `ceros_grupo.csv`, `ceros_localizacion.csv`, `quipus_alineacion.csv`, `cuerdas_anotadas.csv`) y `cifras.json` quedan en la misma carpeta.

**Semillas:** 20261017 (alineación), 20261018 (bandas), 20261019 (grupos), 20261020 (grupos vs quipu), 20261021 (filas exactas).

**Referencias citadas:** Locke (1928) para las columnas de 1000's/100's/10's/1's; Ascher y Ascher (1981) para la notación posicional; Hyland (2024) para los *nether knots*; Thompson (2026) para la diferencia de criterio Ascher/Urton en la asignación de valor; Medrano y Khosla (2024) y el KFG para la base de datos.
