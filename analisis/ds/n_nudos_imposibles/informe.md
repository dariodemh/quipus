# Nudos imposibles en decimal: vueltas de 10–20 y unidades fuera de lugar

**Carpeta:** `analisis/ds/n_nudos_imposibles/`
**Semilla:** 20261018 · **Fecha:** 2026-10-18
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `quipus.csv`, `grupos.csv`; OKR en solo lectura (`data/external/open-khipu-repository/data/khipu.db`). No se creó ni modificó ningún `khipu.db`.

---

## 1. Pregunta

¿Los quipus con nudos largos de 10–20 vueltas (imposibles en la lectura decimal, que admite 2–9) y las cuerdas con varias unidades o con la unidad fuera del final son:

1. **otra notación numérica** (unaria/aditiva, otra base, n vueltas = n unidades),
2. **errores de transcripción**, o
3. **candidatos no numéricos**?

La pregunta se prueba con (a) una auditoría KFG–OKR de las vueltas reales, (b) la estructura de los quipus afectados y (c) una prueba de **sumas internas** (madre = suma de hijas; cabeza de grupo = suma del resto) bajo lecturas alternativas, con nulo por permutación y corrección múltiple.

---

## 2. Resumen ejecutivo

- **La premisa heredada contiene un error de convención.** En el campo `nudos` de KFG, el número antes de `L` **no es el número de vueltas**: es el **valor del racimo**. Un `200L` es un nudo largo de **2 vueltas** en posición de centenas, no un nudo de 200 vueltas. OKR lo confirma: `NUM_TURNS = 2`, `knot_value_type = 200`.
- De las **362 cuerdas** con `nL ≥ 10` en KFG, **171 (47,2 %)** son valor posicional ordinario (vueltas reales 2–9), **144 (39,8 %)** tienen vueltas reales ≥10 y **47 (13,0 %)** no tienen match OKR. Las 144 reales están en **14 quipus**, no en 39.
- **AS090_N2 queda descartado como candidato:** sus 56 cuerdas con `nL ≥ 10` son todas valor posicional (vueltas 2–3; valores 100–3000). Es un quipu decimal de altos valores, no un quipu anómalo.
- El candidato más fuerte es **UR1095** (32 cuerdas con 10–15 vueltas reales), seguido de **UR193** (29) y **KH0001** (29), **UR055** (18), **UR1087** (13) y **UR203** (8).
- **6 de los 14 quipus** con vueltas reales tienen notas explícitas de no decimalidad o nudos espirales: «No numerical interpretation is possible… do not conform to the base ten positional system» (UR1095, UR1087), «spiral knots» (UR193, UR203), «no observable pattern… assign no numerical values» (AS014). KH0001 documenta una **convención aditiva propia** y AS078 una nota de valores 0–10 en un solo racimo. No son errores de transcripción: el fenómeno está documentado en la fuente.
- **Ninguna lectura alternativa hace cerrar las sumas internas.** Lectura del transcriptor (H): 6/326 cierres (1,8 %); decimal estricta (D): 2/319; unaria (U): 10/319; mod 10: 1/319; «L≥10 como n unidades» (LU): 15/319; bases 5, 8, 12, 16 y 20: 1–2/319. Todos los p > 0,22 y todos los p Holm = 1,0. Las sumas de grupo cierran **0/72**.
- **No hay enriquecimiento de cabezas de grupo** (Fisher combinado p = 0,99) ni posiciones fijas (p = 0,77). Las cuerdas anómalas sí están **enriquecidas en el color modal del quipu** (KH0001 p = 0,0007; UR193 p = 0,0013; UR1095 p = 0,0147; Holm < 0,01 para los dos primeros), pero no hay un color exclusivo: es el color mayoritario del quipu, no un código.
- **Veredicto:** otra notación (aditiva/no decimal) o candidato no numérico, **no** error de transcripción. El contenido semántico sigue siendo especulativo. Nivel global: **apoyado con datos** para la anomalía y para el fracaso de las sumas; **bien apoyado** para la convención KFG/OKR.

---

## 3. Método

### 3.1 Parseo y definiciones

Se parseó `nudos` con la expresión `(\d+)([A-Z]+)\(([-\d.]+),([A-Za-z?]+)\)(?:,(-?\d+))?`, que admite los casos sin valor final (p. ej. `UR044`). Cada racimo conserva tipo, número `n`, posición en cm, dirección y valor aportado.

Definiciones operativas:

| Etiqueta | Definición |
|---|---|
| **Marcada (broad)** | `nL ≥ 10` **o** más de un racimo `L/E` **o** un único `L/E` que no es el último racimo. Reproduce la lógica de `20_categorias/nudos_fuera_de_regla.csv`. |
| **L10** | Algún racimo `L/E` con `n ≥ 10` en KFG. |
| **Vueltas reales** | En OKR, `NUM_TURNS ≥ 10` para un nudo `L`. |
| **Valor posicional** | `nL ≥ 10` en KFG pero `NUM_TURNS` 2–9 y `knot_value_type ≥ 10` en OKR. |
| **Multiunidad real** | ≥ 2 racimos `L/E` en el mismo lugar de unidades cuya suma de dígitos es > 9. |
| **Unidad en decenas** | Un `L/E` en lugar 10, 100… (variante posicional, no imposible). |
| **Multiunidad ≤ 9** | Varios `L/E` en unidades que suman ≤ 9 (dígito compuesto legítimo). |

### 3.2 La convención KFG: `nL` es valor, no vueltas

En KFG, para `S` el número es el **conteo de nudos**; para `L` y `E` es el **valor del racimo**. Ejemplos:

- `200L(5.5,U),200` (AS090_N2 p6) → OKR: un nudo largo de **2 vueltas**, `knot_value_type = 200`.
- `20L(14.0,U),20` (AS004 p2) → por la convención KFG, nudo largo de **2 vueltas** en decenas (AS004 no está en OKR; inferido de que `n` es múltiplo de 10 y el valor es 20).
- `10L(14.5,Z),10` (UR193 p6s5) → nudo largo de **10 vueltas**; aquí `n` sí coincide con vueltas porque está en unidades.

Por eso `nL ≥ 10` **no** implica 10 vueltas. La comprobación empírica: en 513 racimos `L` de cuerdas L10 emparejadas con OKR, `KFG n == OKR knot_value_type` en **476/513 (92,8 %)** y `KFG n == NUM_TURNS` en **337/513 (65,7 %)**. Las discrepancias (36/513, 7,0 %) son casos como UR018 p10 (`4000` vs `1000`) o UR032 p37 (`200` vs `100`), compatibles con errores puntuales de factor 2/4, no con un patrón.

### 3.3 Lecturas alternativas

Para cada cuerda emparejada con OKR se reconstruyeron los dígitos físicos: vueltas para `L`, número de nudos para `S/E`, valor para `SP/EE/LL/BL`. Se evaluaron:

| Lectura | Regla |
|---|---|
| **H** | Valor KFG = suma de contribuciones por racimo (S en su lugar decimal; L/E como unidades aditivas). Es la lectura del transcriptor. |
| **D** | Decimal ordinal estricta: dígito físico × 10^(racimos debajo). |
| **U** | Unaria pura: suma de dígitos físicos, posición ignorada. |
| **M** | Mod 10: dígito = vueltas mod 10, lugar ordinal. |
| **LU** | H, pero los `L` de ≥10 vueltas se leen como `n` unidades (lugar 1). |
| **B5, B8, B12, B16, B20** | Base b ordinal, para probar «base distinta». B20 permite dígitos 10–15. |

### 3.4 Sumas internas, nulo y corrección

Relaciones probadas:

- **Madre = suma de hijas directas** (`padre` en KFG).
- **Cabeza de grupo = suma del resto del grupo** (primer colgante del grupo según `orden`).

Solo se usaron cuerdas **con nudos**: la convención `valor = 0` con `nudos` vacío es ausencia, no cero. Esto es crítico: sin este filtro aparecían «cierres» triviales 0 = 0 (AS207A, UR1095 p142) que desaparecen al exigir cuerdas válidas.

Nulo: se permutaron los valores de las madres (o cabezas) **dentro de cada quipu**, preservando la estructura de hijas y el número de relaciones. 5 000 permutaciones; semilla 20261018. p empírico = `(1 + #{nulo ≥ observado}) / (1 + B)`. Se aplicó **Holm y BH** sobre las 20 pruebas lectura × tipo de relación (más las pruebas de multiunidad y base).

Controles estructurales: color y cabeza de grupo por permutación dentro de quipu (10 000 permutaciones, unidad = quipu); posición relativa y rango del racimo por Mann–Whitney por quipu y combinación de Fisher; corrección Holm por familia.

---

## 4. Resultados

### 4.1 Inventario: 3 098 cuerdas marcadas, pero muchas no son «imposibles»

Se marcaron **3 098 cuerdas en 278 quipus** (5,4 % de las 57 818; 7,7 % de las 40 160 con nudos). El desglose muestra que la etiqueta «imposible» es heterogénea:

| Categoría | Cuerdas | Quipus |
|---|---:|---:|
| `L/E` con `n ≥ 10` (KFG) | 362 | 64 |
| — vueltas reales ≥ 10 | **144** | **14** |
| — valor posicional (vueltas 2–9) | 171 | 39 |
| — ambiguo (sin OKR) | 47 | 15 |
| Multiunidad real (suma > 9) | 915 | 76 |
| Unidad en decenas/centenas | 74 | 16 |
| Multiunidad que suma ≤ 9 (válida) | 1 042 | 181 |
| Ambiguo | 446 | 74 |
| Sin OKR | 149 | 46 |
| Otro | 248 | 49 |
| **Total marcado** | **3 098** | **278** |

*Las categorías se solapan:* una misma cuerda puede ser L10 y multiunidad, y las categorías de posición solo se calculan para las 2 990 cuerdas con posición marcada (108 cuerdas L10 no tienen posición marcada). Por eso la suma de filas supera 3 098.

De las 2 990 cuerdas con «posición imposible», solo **915** tienen una suma de unidades > 9 demostrable; **1 042** son en realidad dígitos compuestos válidos (suma ≤ 9); **74** son `E/L` en decenas/centenas (variante posicional); el resto es ambiguo o no tiene OKR. La cifra de «3 000 cuerdas que rompen la regla decimal» **sobreestima** el fenómeno.

**Réplica del hallazgo previo.** Con `10 ≤ nL ≤ 20` se reproducen exactamente las **198 cuerdas en 39 quipus** de `n_narrative_threads`. Pero de esas 198: **143** tienen vueltas reales, **36** son valor posicional y **19** son ambiguas. El conteo era correcto; la interpretación «10–20 vueltas» solo vale para el 72 %.

### 4.2 Los 14 quipus con vueltas reales ≥ 10

| Quipu | OKR | Museo | Procedencia | n cuerdas | n reales | n multiunidad | frac. marcada | canutos | fibra | Nota del transcriptor |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **UR1095** | KH0108 | Museum für Völkerkunde, Múnich | Pachacámac | 212 | **32** | 12 | 0,590 | 0 | s/d | «No numerical interpretation is possible…» |
| **UR193** | KH0431 | Ethnologisches Museum, Berlín | Pachacámac | 226 | **29** | 88 | 0,743 | 0 | CN | «spiral knots» |
| **KH0001** | KH0001 | AMNH, Nueva York | Chuquitanta | 154 | **29** | 35 | 0,766 | 0 | s/d | convención aditiva propia |
| **UR055** | KH0289 | Museo Oro, Lima | s/d | 180 | **18** | 155 | 0,961 | 42 | H | solo número de museo |
| **UR1087** | KH0100 | Museum für Völkerkunde, Múnich | Perú | 97 | **13** | 9 | 0,526 | 0 | CN | «No numerical interpretation…» |
| **UR203** | KH0441 | Ethnologisches Museum, Berlín | s/d | 167 | **8** | 6 | 0,575 | 0 | CN | «spiral knots» |
| **AS014** | KH0015 | British Museum | s/d | 75 | **5** | 22 | 0,773 | 0 | s/d | «no observable pattern…» |
| UR051 | KH0281 | Banco Central de Reserva, Lima | s/d | 98 | 3 | 25 | 0,776 | 0 | CN | — |
| UR052 | KH0282 | Museo Central BCR, Lima | s/d | 96 | 2 | 75 | 0,938 | 25 | CL | canutos |
| UR165 | KH0404 | Puruchuco Museum | La Molina | 225 | 1 | 2 | 0,049 | 0 | CN | — |
| UR171 | KH0410 | AMNH, Nueva York | s/d | 40 | 1 | 1 | 0,175 | 0 | s/d | — |
| UR157 | KH0397 | Museo Regional de Ica | Tambo Colorado | 10 | 1 | 0 | 0,200 | 0 | CN | — |
| AS078 | KH0091 | Musée du Quai Branly | Hacienda Copara, Nazca | 27 | 1 | 0 | 0,037 | 0 | s/d | valores 0–10 |
| UR191 | KH0429 | Musée du Quai Branly | Huaca Pérez, Lima | 28 | 1 | 0 | 0,036 | 0 | CN | — |

La lista completa de los 278 quipus marcados, con procedencia, museo, n cuerdas, fracción marcada, canutos, fibra, nota y veredicto, está en **`nudos_imposibles.csv`**. La tabla por cuerda (3 098 filas) está en **`cuerdas_nudos_imposibles.csv`**.

### 4.3 Estructura de los seis principales

**UR1095 (KH0108), 32 cuerdas reales.** El caso más puro: **9 cuerdas tienen un solo racimo `X`** (un nudo de 10–15 vueltas y nada más); 17 tienen 2 racimos, 4 tienen 3 y 2 tienen 4. El 53 % coocurre con `S`; solo el 6 % con un `L` normal (2–9). Todas son de color **B (marrón)**, el color modal del quipu (31/32; p = 0,0147; Holm 0,088). No son cabezas de grupo (0/20). Posición mediana 14,0 cm, relativa 0,34. La nota es explícita: no hay interpretación numérica posible; 23 órdenes de racimos distintos y 32 racimos de 10–15 nudos. **Es un candidato no numérico o una notación de conteo, no un decimal.**

**UR193 (KH0431), 29 cuerdas reales.** 28 de 29 tienen **3 racimos**; el `X` está en la posición central en 20/29. El 52 % coocurre con `S` y el 66 % con un `L` normal: el nudo de 10–13 vueltas está **incrustado entre nudos decimales normales**, no aislado. Color blanco (18/29, p = 0,0013; Holm 0,0091). Cabezas de grupo 2/10 frente a 2/87 (p = 0,0498 sin corregir; Holm 0,647: no significativo). Posición mediana 17,0 cm, relativa 0,42. Además, 88 cuerdas tienen multiunidad real (varios `L` en unidades que suman > 9). La nota «spiral knots» describe dos tipos de nudo espiral, con y sin eje. **Otra notación (espiral/aditiva), no un decimal ordinario.**

**KH0001, 29 cuerdas reales.** 25/29 tienen 3 racimos; el `X` está en el centro en 13/29. El 86 % coocurre con `S` y el 62 % con `L` normal. Color blanco (27/29, p = 0,0007; Holm 0,0056). Cabeza de grupo 1/23 (p = 0,68). Posición mediana 14,5 cm, relativa 0,42. La nota es una **convención de lectura propia**: «All single knots read as value 10; long knots valued 10 and higher are placed within parentheses; values of multiple knots in same position are joined inside brackets». Es un sistema **numérico no decimal/aditivo**, no un error.

**UR055 (KH0289), 18 cuerdas reales.** Estructura radicalmente distinta: **180 grupos de un solo colgante** (no hay grupos con ≥2), 42 canutos, fibra H (pelo), y las 18 cuerdas reales son de color LK (el color dominante del quipu). El 94 % tiene un `L` normal además del `X`; solo el 6 % tiene `S`. Posición mediana 49 cm, relativa 0,54. No hay nota relevante. 155 cuerdas tienen multiunidad real. **Candidato a notación aditiva/tally** (varios nudos largos de 4–6 vueltas sumados), no a decimal.

**UR1087 (KH0100), 13 cuerdas reales.** 2–3 racimos, 31 % con `S`, 54 % con `L` normal, blancas, no cabezas (0/11). Posición mediana 16,5 cm, relativa 0,34. Nota: «No numerical interpretation is possible… 19 different knots… 13 knots which contain 10, 11, 12, or 13 knots». **No numérico / otra notación.**

**UR203 (KH0441), 8 cuerdas reales.** 1–4 racimos, 62 % con `S`, **0 % con `L` normal**: aquí el nudo de 10–12 vueltas no convive con un `L` decimal, sino con `S` y `E`. Color blanco, cabezas 1/5 (p = 0,35). Nota: «spiral knots… like those described for UR193». **Otra notación (espiral).**

**Control negativo: AS090_N2 (KH0103).** 56 cuerdas con `nL ≥ 10`, pero **0 con vueltas reales ≥ 10**: todas son `100E/200L/300L…` con 2–3 vueltas y valores posicionales 100–3000. 58 cuerdas, 8 grupos, color blanco, valores 223, 322, etc. Es un **quipu decimal de altos valores**, no un quipu anómalo. Su inclusión como candidato en `n_narrative_threads` es un artefacto de leer `nL` como vueltas.

### 4.4 Lecturas alternativas y sumas internas

La prueba decisiva: ¿alguna lectura hace que la madre sea la suma de las hijas, o la cabeza la suma del grupo? Resultados con cuerdas válidas (sin vacías), 14 quipus con vueltas reales, nulo de 5 000 permutaciones dentro de quipu:

| Lectura | Relación | n | Cierran | Tasa | Nulo (medio) | p | Holm |
|---|---|---:|---:|---:|---:|---:|---:|
| **H** (transcriptor) | madre | 326 | 6 | 0,0184 | 7,64 | 0,782 | 1,0 |
| **D** (decimal) | madre | 319 | 2 | 0,0063 | 2,38 | 0,698 | 1,0 |
| **U** (unaria) | madre | 319 | 10 | 0,0313 | 18,73 | 0,994 | 1,0 |
| **M** (mod 10) | madre | 319 | 1 | 0,0031 | 2,52 | 0,918 | 1,0 |
| **LU** (L≥10 = n unidades) | madre | 319 | 15 | 0,0470 | 12,03 | 0,228 | 1,0 |
| **B5** | madre | 319 | 2 | 0,0063 | 3,27 | 0,840 | 1,0 |
| **B8** | madre | 319 | 1 | 0,0031 | 2,47 | 0,917 | 1,0 |
| **B12** | madre | 319 | 1 | 0,0031 | 2,09 | 0,877 | 1,0 |
| **B16** | madre | 319 | 1 | 0,0031 | 2,07 | 0,882 | 1,0 |
| **B20** | madre | 319 | 1 | 0,0031 | 2,08 | 0,876 | 1,0 |
| **H** | grupo | 72 | 0 | 0,0000 | 0,65 | 1,0 | 1,0 |
| **D/U/M/LU/bases** | grupo | 72 | 0 | 0,0000 | ≤0,69 | 1,0 | 1,0 |

Lectura de la tabla:

- **La lectura del transcriptor (H) no cierra mejor que el azar**: 6 cierres observados frente a 7,64 esperados; p = 0,78.
- **La decimal estricta (D) es peor**: 2/319.
- **La unaria pura (U) tiene menos cierres que el nulo** (10 vs 18,73; p = 0,99): los valores no se comportan como meras sumas de vueltas.
- **LU es la única que supera el nulo** (15 vs 12,03), pero p = 0,23 y Holm = 1,0. No es evidencia; es la variante que más se acerca, y sigue sin cerrar el 95 % de las relaciones.
- **Ninguna base distinta (5, 8, 12, 16, 20) mejora**; B20, que permitiría dígitos 10–15, da 1/319.
- **Las sumas de grupo cierran 0/72** en todas las lecturas. No hay una sola cabeza de grupo que sea la suma de su grupo entre cuerdas válidas.

Prueba complementaria en los quipus con **multiunidad real** (≥ 5 cuerdas; 19 quipus, incluidos UR050, UR054, UR055, UR052, UR193): H madre 6/291 (2,1 %) vs nulo 7,21, p = 0,74; grupo 0/77, p = 1,0. Tampoco hay sumas.

**Base de comparación:** en una muestra de 120 quipus grandes, H madre cierra 69/1 351 (5,1 %) frente a 65,31 esperados, p = 0,33; grupo 0/301. Es decir, **las sumas internas exactas son raras en todo el corpus** (≈5 %), y los quipus anómalos están por debajo de esa base, no por encima.

### 4.5 KFG frente a OKR y notas del transcriptor

- **Cobertura:** 321/362 cuerdas L10 emparejadas con OKR; 41 quedan sin match (AS004 21, QU007 6, QU011 3, QU009 2, QU013 2, y 6 casos sueltos). Las no emparejadas son, en su mayoría, valor posicional probable (AS004 es un quipu decimal de altos valores), pero se codifican como «ambiguo».
- **Acuerdo:** 476/513 racimos `L` con `KFG n == OKR knot_value_type` (92,8 %); 337/513 con `KFG n == NUM_TURNS` (65,7 %); 36/513 (7,0 %) no coinciden con ninguno. Ejemplos de discrepancia: UR018 p10 (KFG 4000, OKR 1000), UR032 p37 (200 vs 100), AS156 p19 (20 vs 10). Son errores puntuales de factor 2/4, no un patrón sistemático.
- **No hay un patrón de error de transcripción que explique el fenómeno.** Al contrario: KFG y OKR coinciden en las 144 cuerdas con vueltas reales; las notas del transcriptor describen el fenómeno como una propiedad del objeto.
- **Notas textuales** (OKR, `khipu_main.NOTES`):
  - UR1095: «No numerical interpretation is possible as the knot clusters do not conform to the base ten positional system. Twenty-three different knot cluster orders are found on the pendants… there are 32 knot clusters which contain 10-15 knots.»
  - UR1087: «No numerical interpretation is possible… Nineteen different knots or figure eight knots followed by single knots… there are 13 knots which contain 10, 11, 12, or 13 knots.»
  - UR193: «We have identified an unusual pair of knots on UR193. These are termed “spiral knots” with and without axis.»
  - UR203: «“spiral knots” are knots like those described for UR193. There are two types: Spiral knot with axis, spiral knot without axis.»
  - AS014: «The placement of knot groupings follows no observable pattern. Therefore, we assign no numerical values to the knots.»
  - KH0001: «All single knots read as value 10. Long knots valued 10 and higher are placed within parentheses. Values of multiple knots in same position are joined inside brackets.»
  - AS078: «Each pendant on the quipu contains only one knot cluster (either long knots or a figure eight knot). The values, however, range from 0 to 10.»

### 4.6 Controles estructurales

| Control | Resultado | p / corrección |
|---|---|---|
| **Color modal** (¿las cuerdas reales están en el color mayoritario?) | KH0001 27/29 vs 79/125; UR193 18/29 vs 61/197; UR1095 31/32 vs 145/180 | Permutación dentro de quipu: KH0001 p = 0,0007 (Holm 0,0056); UR193 p = 0,0013 (Holm 0,0091); UR1095 p = 0,0147 (Holm 0,088). Fisher combinado p = 0,00014 (exploratorio). |
| **Cabeza de grupo** (grupos ≥ 2) | UR193 2/10 vs 2/87; KH0001 1/23 vs 3/73; resto 0 | Permutación: UR193 p = 0,0498 (Holm 0,647); combinado Fisher p = 0,993. **Sin efecto.** |
| **Posición relativa** (L≥10 vs L 2–9, mismo quipu) | Medianas 0,33–0,54; diferencias pequeñas | Mann–Whitney por quipu; Fisher combinado p = 0,769; Wilcoxon de medianas p = 0,359. **Sin efecto.** |
| **Rango del racimo** (0 = arriba) | Genuinos mediana 0,50 (IQR 0,00–0,77); normales 0,50 (0,00–1,00) | Mann–Whitney p = 0,162. **Sin efecto.** |
| **Coocurrencia** | UR1095 53 % con S, 6 % con L normal; UR193 52 % / 66 %; KH0001 86 % / 62 %; UR055 6 % / 94 %; UR1087 31 % / 54 %; UR203 62 % / 0 % | Descriptivo. El nudo de 10+ vueltas suele estar **incrustado** entre nudos normales, no aislado. |

Interpretación: las cuerdas anómalas **no** son cabezas de grupo, **no** ocupan una posición fija y **no** tienen un color exclusivo. El único efecto robusto es que están en el **color modal** del quipu, lo que probablemente refleja que pertenecen al cuerpo principal y no a las subsidiarias de color variado; no es un código de color.

---

## 5. Resultados negativos

1. **No hay sumas internas** bajo ninguna lectura probada: H 6/326, D 2/319, U 10/319, M 1/319, LU 15/319, bases 1–2/319; todos p > 0,22 y Holm = 1,0. Grupos: 0/72.
2. **No hay enriquecimiento de cabezas de grupo** (p = 0,99 combinado). El único caso nominal (UR193, p = 0,0498) desaparece con Holm (0,647).
3. **No hay posiciones fijas** ni rango preferente (p = 0,77 y 0,16).
4. **No hay evidencia de base 20** ni de otra base: B20 da 1/319 cierres.
5. **No hay un patrón de error de transcripción**: KFG y OKR coinciden en el 92,8 % de los racimos L; las 36 discrepancias son puntuales.
6. **AS090_N2 no es anómalo**: 56/56 L10 son valor posicional; 0 vueltas reales.
7. **La etiqueta «3 000 cuerdas imposibles» sobreestima**: 1 042 son multiunidad ≤ 9 (válidas) y 74 son unidades en decenas/centenas (variante).
8. **La lectura unaria pura no funciona**: tiene menos cierres que el nulo (10 vs 18,7), no más.

---

## 6. Veredicto por quipu

| Quipu | Vueltas reales | Multiunidad | Nota | Veredicto | Evidencia |
|---|---:|---:|---|---|---|
| **UR1095** | 32 | 12 | «No numerical interpretation…» | **No numérico / otra notación** | Apoyado con datos |
| **UR193** | 29 | 88 | «spiral knots» | **Otra notación (espiral/aditiva)** | Apoyado con datos |
| **KH0001** | 29 | 35 | convención aditiva | **Numérico no decimal** | Apoyado con datos |
| **UR055** | 18 | 155 | — | **Aditivo/tally** | Propuesto |
| **UR1087** | 13 | 9 | «No numerical interpretation…» | **No numérico / otra notación** | Apoyado con datos |
| **UR203** | 8 | 6 | «spiral knots» | **Otra notación (espiral)** | Propuesto |
| **AS014** | 5 | 22 | «no observable pattern…» | **No numérico** | Apoyado con datos |
| **UR051** | 3 | 25 | — | **Candidato no numérico** | Propuesto |
| **UR052** | 2 | 75 | canutos | **Multiunidad aditiva** | Propuesto |
| **UR165, UR171, UR157, AS078, UR191** | 1 cada uno | 0–2 | — | **Caso aislado** (error puntual o variante menor) | Especulativo |
| **AS090_N2** | 0 | 0 | — | **Decimal de altos valores** | Bien apoyado |
| **AS004** | 0 (sin OKR) | — | — | **Ambiguo sin OKR; probable decimal de altos valores** | Apoyado (indirecto) |

**Regla de decisión:** ≥ 3 cuerdas con vueltas reales y nota explícita → otra notación/no numérico; ≥ 5 cuerdas con multiunidad real sin L10 → multiunidad aditiva; 1–2 cuerdas → caso aislado; 0 reales con valores posicionales → decimal normal.

---

## 7. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| En KFG, `nL` es el valor del racimo, no el número de vueltas; 171/321 L10 son valor posicional; AS090_N2 es decimal | **Bien apoyado** (OKR `NUM_TURNS` y `knot_value_type`) |
| Hay 144 cuerdas en 14 quipus con vueltas reales de 10–16 | **Bien apoyado** (KFG y OKR coinciden) |
| Esos quipus no son decimales posicionales; usan notación aditiva/espiral/no numérica | **Apoyado con datos** (6/14 notas de no decimalidad/espirales + KH0001; estructura; ausencia de sumas) |
| Ninguna lectura alternativa hace cerrar las sumas internas | **Apoyado con datos** (negativo; 24 pruebas, Holm 1,0) |
| Los nudos de 10–16 vueltas son una categoría semántica distinta (no solo números) | **Propuesto** |
| Base 20 u otra base | **Especulativo** (probado, sin apoyo) |
| Los casos aislados de 1–2 cuerdas son errores de transcripción | **Especulativo** |

---

## 8. Limitaciones

- Solo 14 quipus tienen ≥ 1 cuerda con vueltas reales; 7 tienen ≥ 5. El tamaño es pequeño para inferencias por quipu.
- 41/362 cuerdas L10 no tienen match OKR; su clasificación es «ambiguo».
- El campo `nudos` de KFG mezcla convenciones (`S` = conteo, `L/E` = valor), lo que hace muy fácil leer «vueltas» donde hay «valor». Cualquier análisis futuro debe usar OKR `NUM_TURNS` o reconstruir el valor por racimo.
- La prueba de sumas usa igualdad exacta; no se probaron tolerancias ni «suma de un subconjunto» de hijas. Sin embargo, la tasa base (5,1 %) y la ausencia de cierres de grupo (0/72) sugieren que una tolerancia no cambiaría el veredicto.
- La definición de «cabeza de grupo» es una convención (primer colgante del grupo). Otras relaciones (cuerda superior, suma de subsidiarias de segundo orden) no se probaron. Además, la relación `padre` no implica suma en todos los quipus: el test madre = suma de hijas es una **criba**, no una prueba de que no exista ninguna suma en el quipu.
- Procedencia de museo ≠ lugar de origen; no se usó como origen.
- No se inspeccionaron las fotos de alta resolución de los nudos espirales; la interpretación física de «10–16 vueltas» se basa en OKR.

---

## 9. Para el coordinador

- **Corregir la premisa antes de seguir:** en KFG el número antes de `L` es el **valor**, no las vueltas. De 362 cuerdas con `nL ≥ 10`, **171 son decimal ordinario** (vueltas 2–9) y solo **144 tienen vueltas reales ≥ 10**, en **14 quipus**. La cifra «198 cuerdas / 39 quipus» se reproduce, pero solo 143 son vueltas reales; 36 son valor posicional y 19 ambiguas.
- **AS090_N2 queda descartado:** sus 56 `nL ≥ 10` son valores posicionales (2–3 vueltas; 100–3000). **UR1095** debe ocupar su lugar como candidato principal (32 cuerdas reales; nota «no numerical interpretation is possible»).
- **Los 14 quipus con vueltas reales:** UR1095 (32), UR193 (29), KH0001 (29), UR055 (18), UR1087 (13), UR203 (8), AS014 (5), UR051 (3), UR052 (2), y cinco casos aislados de 1.
- **No son errores de transcripción:** KFG y OKR coinciden en el 92,8 % de los racimos `L`; 6/14 quipus tienen notas explícitas de no decimalidad o nudos espirales, y KH0001 documenta una convención aditiva propia. El fenómeno está documentado en la fuente, no es un artefacto de digitalización.
- **Ninguna lectura alternativa cierra las sumas:** H 6/326, D 2/319, U 10/319, LU 15/319, bases 5–20 1–2/319; todos p > 0,22 y Holm = 1,0. Las sumas de grupo cierran **0/72**. La hipótesis «n vueltas = n unidades» no se valida por sumas internas.
- **Estructura:** no son cabezas de grupo (p = 0,99), no tienen posición fija (p = 0,77) y no tienen color exclusivo; sí están en el color modal del quipu (KH0001 y UR193, Holm < 0,01). El nudo de 10+ vueltas suele estar **incrustado** entre `S` y `L` normales, sobre todo en UR193 y KH0001.
- **Veredicto:** otra notación numérica (aditiva/espiral) o candidato no numérico, **no** error. UR1095, UR1087 y AS014 son los candidatos no numéricos más claros; KH0001 es un sistema numérico no decimal; UR055/UR050/UR054 son aditivos/tally.
- **Clase separada que merece su propia ronda:** 915 cuerdas en 76 quipus con **múltiples unidades que suman > 9** (UR050 162, UR055 155, UR054 109, UR193 88, UR052 75). Es un fenómeno aditivo distinto del nudo de 10+ vueltas; no debe mezclarse con él.
- **Siguiente ronda recomendada:** (1) inspección de fotos de alta resolución de UR1095/UR193/KH0001 para contar vueltas y distinguir «spiral with/without axis»; (2) prueba de sumas con tolerancia y de «suma de subconjunto»; (3) análisis de color y grupo a nivel de racimo, no de cuerda; (4) no volver a usar `nL` como vueltas en ningún análisis.
