# Auditoría del *Code of the Quipu Databook* (Ascher y Ascher, 1988) frente al Khipu Field Guide

**Equipo:** `ds/n_databook` · **Fecha:** 18 de octubre de 2026
**Fuentes:** OCR Tesseract de `analisis/fuentes_txt/databook/as*.txt` (206 archivos, AS10–AS215) y `analisis/datos/cuerdas.csv` (KFG).
**Entregables:** `databook_rows.csv`, `discrepancias.csv`, `notas_ascher.csv`, `databook_vs_kfg.csv`, `quipus_conteos.csv`, `controles_nulos.csv` y los scripts de esta carpeta.

---

## 1. Pregunta

¿Qué tan fiel es el Khipu Field Guide (KFG) a la fuente que dice transcribir —el *Databook* de Ascher y Ascher (1988)— en valor, color y largo? ¿Dónde, cómo y cuánto divergen? ¿Los valores del KFG son siempre transcripción, o a veces reconstrucción? ¿Qué afirmaciones numéricas hicieron los Ascher que podamos contrastar después?

No se audita aquí si los quipus "significan" algo: se audita la **cadena de transmisión de datos**, un paso previo obligatorio para cualquier análisis computacional.

---

## 2. Material y unidad de análisis

- 206 archivos OCR, uno por número AS (AS10–AS215).
- 14 953 filas de tabla extraídas; 211 segmentos-quipu (seis archivos contienen varios quipus: AS26A/B, AS33A–G, AS35A–D, AS101 I/II, AS124, AS207A–C).
- 210 quipus del Databook con al menos una cuerda de nivel 0.
- Unidad de análisis: **el quipu**. Los contrastes de concordancia se agregan por quipu o se acompañan de un nulo que permuta dentro de cada quipu.

**Advertencia de circularidad:** el KFG se construyó, al menos en parte, a partir de este mismo Databook. Por tanto, una concordancia alta mide **fidelidad de transcripción**, no verificación independiente de los números. Esta advertencia gobierna toda la interpretación.

---

## 3. Método

### 3.1 Parser

`parse_databook.py` procesa cada línea de tabla con estrategia de derecha a izquierda:

1. **Subsidiarias** al final (`1:10.0`, `3:20.0-20.5`, `missing`).
2. **Valor**: expresión final del tipo `4`, `4+4`, `16+T`, `12(?)`. Las sumas explícitas se suman (188 filas); `?` se marca como valor incierto (217 filas).
3. **Color**: primer token válido tras el largo, validado contra el vocabulario de colores del KFG (evita leer como color ruido tipo `yy`, `ll`).
4. **Largo**: último decimal fuera de paréntesis, con tolerancia a `¢`, `b`, `o`, `,`.
5. **Nudos**: texto entre la etiqueta y el largo, normalizando errores típicos: `35(3.5)→3s(3.5)`, `38(3.0)→3s(3.0)`, `Tl→T1`, `1sl→1s1`, `4us1→4s1`, `)34L(→);4L(`.
6. **Sin columna de valor** (AS87, AS95, AS104): la fila se conserva con `valor=NaN` para no perder color, largo y conteo.

La etiqueta de cuerda se normaliza a `p1`, `p1s1`, `t1`, `t2s1`. La numeración se repara cuando el OCR duplica o invierte números (p. ej. AS010: un `1` que en realidad es la cuerda 15).

### 3.2 Identificación de quipus

El id se toma del **encabezado** (`QUIPU AS26A`, `AS101--PART II`, `AS207 A`), no del nombre del archivo:

| Archivo | Id KFG |
|---|---|
| as26 | AS026A (y AS026B en el mismo archivo) |
| as35 | AS35A–AS35D |
| as101 | AS101_Part_1 / AS101_Part_2 |
| as207 | AS207A / AS207B / AS207C |

Esto evita el error de mapear todo `AS101` a una sola parte y duplicar filas.

### 3.3 Alineación con KFG

Para cada quipu se alinean las secuencias completas (colgantes y subsidiarias, en orden físico) con un Needleman–Wunsch cuya puntuación combina:

- valor (coincidencia exacta 1.5; ±1 → 1.0),
- largo (≤0.11 cm → 1.5; ≤0.6 → 1.0),
- color (conjunto de componentes igual → 1.0; intersección → 0.5),
- mismo nivel (bonus 0.6; penalización −0.8 si difiere),
- mismo número de colgante (bonus 0.8, solo nivel 0).

Solo se conservan pares con **mismo nivel y score ≥ 3** para los contrastes de valor. Resultado: 6 955 pares alineados, 6 215 comparables, 129 quipus.

### 3.4 Decodificación de nudos

`decoder.py` implementa la lectura Ascher con posición: los nudos simples valen 10 si están en la mitad superior de la cuerda o si hay otro racimo debajo; los largos valen su número de vueltas; las figuras de ocho valen 1. Marca como **ambiguos** los casos de un solo nudo simple en la zona media y los racimos con más de 9 nudos.

### 3.5 Clasificación de discrepancias de valor

Para cada par con `valor_db ≠ valor_kfg`:

| Clase | Definición operativa |
|---|---|
| `a_ocr` | El número impreso difiere por dígitos insertados/perdidos (subsecuencia o factor 10/100), no explicable por posición decimal. |
| `b_error_kfg` | Los nudos del Databook sostienen el valor del Databook y los nudos del KFG (presentes) no sostienen el valor del KFG. |
| `c_error_databook` | Los nudos del KFG sostienen su valor y los nudos del Databook no sostienen el valor impreso. |
| `d_convencion_x10` | Ambas fuentes son coherentes con sus nudos, pero difieren en una decena/centena (convención posicional). |
| `d_valor_dudoso` | El Databook imprime `?` (valor incierto) y el KFG lo resuelve. |
| `d_kfg_sin_nudos` | El KFG no registra nudos (valor 0 por defecto) y el Databook sí. |
| `d_otras` | Nudos ambiguos, valores no concluyentes o discrepancias de fuente. |

### 3.6 Notas de los Ascher

`notas.py` segmenta la sección *Observations* en ítems numerados (incluye ítems `a)`, `(1)`, `*1.`), limpia encabezados de página y clasifica cada ítem por palabras clave (suma, igualdad, conteo, construcción/color, valor). Genera una fila por afirmación.

---

## 4. Resultados

### 4.1 Cobertura del parser

| Métrica | Valor |
|---|---|
| Archivos procesados | 206 |
| Filas extraídas | **14 953** |
| Quipus/segmentos con filas | 211 |
| Quipus del Databook con nivel 0 | **210** |
| Colgantes (nivel 0) | 12 157 |
| Subsidiarias nivel 1 / 2 / 3 | 2 435 / 251 / 110 |
| Filas con valor legible | 13 369 (89.4 %) |
| Filas sin valor (columna ausente) | 1 584 (10.6 %) |
| Valores marcados `?` | 217 (1.6 % de las filas con valor) |
| Valores expresados como suma (`4+4`) | 188 (1.4 %) |

**Cobertura frente a la descripción del cordón principal:** mediana **96.2 %** de los colgantes descritos (P25 = 85.7 %; 10 de 189 quipus por debajo del 70 %). Frente al propio KFG, en los 131 quipus comunes recuperamos **7 002 de 8 042 cuerdas (87.1 %)** y **5 935 de 6 457 colgantes (91.9 %)**. No hay una fracción única porque el OCR destruye tablas completas en algunos quipus y porque el KFG contiene cuerdas fantasma que el Databook no tiene.

**Control interno del parser:** en 86.1 % de las filas con valor, el valor impreso coincide exactamente con la decodificación de sus propios nudos; si se ignora la posición decimal (7 vs 70), coincide el 89.4 %. Los desacuerdos restantes son, en su mayoría, valores `?` o nudos con OCR corrupto.

**Quipus problemáticos (no utilizables para valor):** AS014, AS036, AS037, AS081, AS129 (tabla con valores ausentes o `?`), AS087, AS095 y AS104 (columna de valor no legible). AS022 y AS190 no tienen tabla (solo prosa/observaciones). Los quipus con tabla rota siguen siendo utilizables para color y largo.

### 4.2 Concordancia global con KFG

| Dimensión | Pares | Coincidencia | Nulo (permutación intra-quipu) | p |
|---|---:|---:|---:|---:|
| Valor | 5 890 | **94.7 %** | 30.5 % | 0.001 |
| Color (conjunto de componentes) | 6 215 | **92.2 %** | 42.9 % | 0.001 |
| Largo (±0.5 cm) | 6 215 | **99.9 %** | 10.5 % | 0.001 |

Los p-valores son empíricos (1 000 permutaciones, semilla 42); el mínimo alcanzable es 0.000999. Corrección de Holm para tres pruebas: **p_Holm = 0.003** en las tres. El nulo permuta las cuerdas del KFG **dentro de cada quipu**, preservando el tamaño y la composición de valores/colores/largos de cada quipu; por tanto el acuerdo observado no se explica por azar ni por la heterogeneidad entre quipus.

**Pero:** este test demuestra que el emparejamiento es correcto, no que los valores sean verdaderos. Dada la genealogía común Databook → KFG, el 94.7 % es un techo de fidelidad de transcripción, no una validación externa.

### 4.3 Discrepancias de valor

**311 discrepancias** sobre 6 215 pares comparables (**5.0 %**). Distribución:

| Clase | n | % de discrepancias | Lectura |
|---|---:|---:|---|
| `d_kfg_sin_nudos` | **128** | 41.2 % | KFG perdió los nudos y puso valor 0 |
| `d_valor_dudoso` | **70** | 22.5 % | El Databook marcó `?`; KFG resolvió |
| `c_error_databook` | **45** | 14.5 % | Nudos KFG coherentes; valor impreso del Databook no |
| `d_convencion_x10` | **31** | 10.0 % | Difieren solo en decena/centena |
| `d_otras` | **23** | 7.4 % | Nudos ambiguos o fuente distinta |
| `a_ocr` | **14** | 4.5 % | Dígitos insertados/perdidos |
| `b_error_kfg` | **0** | 0 % | Sin caso claro de error aritmético del KFG con nudos presentes |

Casos ilustrativos:

- **AS010 (KFG 27 cuerdas vs Databook 25).** KFG inserta dos cuerdas fantasma: `p15` (largo 0, valor 0, sin nudos) y `p26` (largo 0, valor 10, nudo `1S(0.0,U)`). El Databook no las tiene. Es el ejemplo más limpio de fila inventada/desplazada en KFG.
- **AS011 p13.** Databook imprime valor 2 con `--` (sin nudos); KFG pone 0. Discrepancia de fuente, no de OCR.
- **AS101_Part_2.** 21 de 21 cuerdas difieren exactamente en ×10 (Databook 3, 7, 9…; KFG 30, 70, 90…), con largos y colores idénticos. No es OCR: es una **convención posicional distinta** aplicada sistemáticamente a todo el quipu.
- **AS170 p9.** Databook 643, nudos `6L(20.0);3L(24.0)` = 9, KFG 9. El valor impreso del Databook está corrompido; el KFG reconstruye bien.
- **AS081.** El Databook dice literalmente: *“No numerical interpretation is possible as the knot clusters do not conform to the base ten positional system.”* KFG, sin embargo, le asigna valores decimales (10, 5, 0, 7, 9, 0, 3, 8). Es una contradicción directa entre fuente y base derivada.
- **AS129.** Valores del tipo `1113`, `1748`, `1475` (concatenación de valores de racimos, no suma posicional) pasan intactos al KFG. El KFG no los corrige ni los marca como no decimales.

**Concentración:** 60 quipus tienen al menos una discrepancia; los cinco primeros (AS050 98, AS101_Part_2 24, AS069 12, AS013 10, AS101_Part_1 9) suman el **49 %**. La mediana de la tasa por quipu (quipus con ≥10 pares) es **1.5 %**, y **39 de 92 quipus no tienen ninguna discrepancia de valor**. El 5 % global está dominado por un puñado de especímenes, sobre todo AS050 (56 cuerdas sin nudos en KFG + 37 valores `?`).

**Tamaño de las diferencias:** 214 de 311 (69 %) están dentro de ±10; 29 superan ±100. La media (−19.6) está arrastrada por outliers; la mediana es +1.

### 4.4 Color y largo

- **Color exacto: 92.2 %** (93.1 % si se ignora el componente blanco `W`). Las diferencias no son mayoritariamente OCR:
  - `B → AB` (38 casos),
  - Databook sin color → KFG `PK` (24) o `W` (23),
  - `WW → W` (20, ruido de OCR),
  - `BY → YB` (15, inversión de código),
  - `BB → B` (13),
  - `W → KB:W` (11, el KFG añade el color dominante).
  
  Conclusión: el color del KFG no es una copia literal; a veces añade un componente (W, KB) o reinterpreta el código. No debe usarse como verdad absoluta sin normalizar.

- **Largo: 99.9 % dentro de ±0.5 cm** (diferencia media 0.01 cm). Solo 4 cuerdas difieren más de 1 cm: AS027 p10s1 (3 vs 9), AS050 p166 (25.5 vs 23.5), AS069 p4 (34 vs 39.5), AS168 p7 (24 vs 54). El largo es, con diferencia, el campo mejor transcrito.

### 4.5 Quipus ausentes y conteos de cuerdas

- **80 quipus del Databook no están en KFG** (AS30–AS208: AS030–AS034, AS038, AS040, AS046–AS047, AS049, AS051–AS058, AS067–AS068, AS070, AS084, AS086, AS088, AS091, AS095–AS100, AS102–AS109, AS113–AS114, AS116–AS121, AS123–AS124, AS126–AS127, AS130–AS131, AS135–AS136, AS138, AS140–AS141, AS143–AS152, AS154, AS161–AS163, AS165–AS167, AS175–AS176, AS179–AS181, AS208). Es el 38 % del Databook y una parte sustancial del corpus AS.
- **14 ids KFG AS sin Databook comparable:** AS001–AS009 (fuera del rango AS10–AS215 del Databook), AS063B, AS065B, AS182B, AS215F (partes que el Databook no transcribe por separado) y AS195 (el Databook trae tabla, pero su jerarquía de subsidiarias —`1slsl`, `1ls3`…— rompe el parser: solo se recuperan 2 de 7 filas).
- **130 quipus comparables.**
- **AS063 y AS065:** el KFG tiene 9 y 5 cuerdas frente a 33 y 10 descritas. No es pérdida de datos: el KFG separa AS063/AS063B y AS065/AS065B; el Databook los presenta juntos.
- **Cuerdas con largo 0 en KFG: 62**, de las cuales **14 tienen valor > 0** (p. ej. AS010 p26 = 10, AS042 p1 = 124, AS069 p1649 = 10, AS071 p235s1 = 1). Un largo 0 con valor positivo es un artefacto de dato, no una cuerda real de longitud cero.
- **5 quipus tienen valores en KFG pero ningún valor legible en el Databook:** AS014 (75 cuerdas con valor), AS036 (65), AS037 (42), AS081 (6 de 8) y AS129 (14). En estos casos el KFG **no transcribe: reconstruye**. Es el hallazgo más importante para el uso de la base.

### 4.6 Notas y afirmaciones de los Ascher

- **812 ítems** de observación en **195 quipus**.
- 756 contienen números; **134** contienen una relación aritmética explícita; **116** usan vocabulario de suma/igualdad (“sum of”, “equals”, “total”, “twice”, “half”).
- La tabla `notas_ascher.csv` tiene columnas `quipu, item, texto, tipo, tiene_numeros, numeros`, lista para contrastar con nuestros hallazgos.

Ejemplos:

| Quipu | Afirmación de los Ascher |
|---|---|
| AS010 | “The value of top cord 1 plus the value of its subsidiary equals 51. The total value of the first 7 pendants is 51 and the total value of the next 7 pendants is 51.” |
| AS016 | “Pendant cord 1 is the sum of the values on the remaining 6 pendants.” |
| AS019 | “The value of pendant 9 is the sum of the values of pendants 6 and 7.” |
| AS028 | “Group 5 can be a sum group…” |
| AS033 | Varias relaciones de suma entre AS33E/G y otros quipus. |

Advertencia: AS033 agrupa AS33A–G en un solo id porque el KFG no tiene esas partes; sus 30 ítems deben separarse antes de usarse.

---

## 5. Controles

1. **Nulo de permutación intra-quipu** (1 000 permutaciones, semilla 42): descrito en 4.2. El acuerdo observado supera a todas las permutaciones en las tres dimensiones (p = 0.001; Holm = 0.003).
2. **Control de alineación:** solo se comparan pares con el mismo nivel (95.5 % de los pares alineados) y score ≥3; los pares dudosos se excluyen. Sin este filtro, el acuerdo de valor baja al 84 % (mezcla de filas mal alineadas).
3. **Control de decodificación:** 86.1 % de las filas con valor coinciden con la decodificación independiente de sus nudos (89.4 % ignorando la decena). Esto detecta líneas mal parseadas y valores impresos corruptos.
4. **Control de circularidad:** se midió por separado la coherencia interna del KFG (95.7 % de las cuerdas con nudos y decodificación no ambigua tienen valor = decodificación). El KFG es internamente coherente; el problema no es su aritmética, sino la pérdida de nudos y la invención de valores en 5 quipus.

No se aplicó corrección múltiple a los conteos descriptivos (no son pruebas de hipótesis); sí a las tres pruebas de concordancia.

---

## 6. Resultados negativos

- **No se encontró ningún caso claro de error aritmético del KFG con nudos presentes** (`b_error_kfg = 0`). Cuando el KFG tiene nudos, su valor coincide con su lectura en 95.7 % de los casos no ambiguos.
- **La concordancia no es un artefacto de alineación:** el nulo intra-quipu da 30.5 % para valor y 10.5 % para largo.
- **El largo no es un problema:** 99.9 % dentro de 0.5 cm. Cualquier análisis que dependa de longitud puede usar KFG con confianza.
- **El color no es una copia literal:** 7.8 % de diferencias, muchas por convención (B/AB, W/KB:W), no por OCR. No es un error grave, pero impide tratar el color KFG como verdad absoluta.
- **La tasa global de discrepancia (5 %) sobreestima el problema típico:** la mediana por quipu es 1.5 % y 39/92 quipus no tienen ninguna.
- **AS081 prueba que el KFG no respeta las propias advertencias del Databook:** no es un caso aislado de OCR, sino una decisión de codificación.

---

## 7. Nivel de evidencia

| Hallazgo | Nivel |
|---|---|
| El parser recupera 14 953 filas y ~96 % de los colgantes descritos | **Demostrado** (medición directa) |
| Valor 94.7 %, color 92.2 %, largo 99.9 % de concordancia | **Demostrado** como fidelidad de transcripción (no como verdad) |
| 311 discrepancias y su clasificación | **Apoyado con datos** (depende del decoder y de la alineación; se verificaron a mano varios casos, entre ellos AS010, AS011, AS101 y AS170) |
| 128 cuerdas con nudos perdidos en KFG | **Apoyado con datos** (el KFG tiene `nudos` vacío y valor 0) |
| 5 quipus con valores reconstruidos por KFG | **Demostrado** (valores KFG presentes; valores Databook ausentes/`?`) |
| AS081: KFG impone lectura decimal contra la nota de los Ascher | **Demostrado** (cita textual + valores KFG) |
| Atribuir cada error a Tesseract vs. a la edición impresa | **Especulativo** (no tenemos el PDF original ni la edición de 1988 a la vista) |
| Que las 45 `c_error_databook` sean erratas de la edición y no del OCR | **Propuesto** (patrón consistente, pero sin verificación física) |

---

## 8. Limitaciones

1. **OCR muy desigual.** AS014, AS036, AS037, AS081, AS087, AS095, AS104 y AS129 tienen tablas rotas o columnas ausentes; sus valores no se comparan.
2. **Alineación ambigua en cuerdas vacías.** Las cuerdas con valor 0 y largo 0.5 son indistinguibles; el DP puede desplazar el emparejamiento. Se mitigó con el bonus de nivel y el filtro de score, pero no se elimina.
3. **Decodificador Ascher incompleto.** La posición exacta (centenas/decenas/unidades) no siempre se puede inferir de la posición sobre la cuerda; los casos ambiguos se marcan y no se usan para acusar a ninguna fuente.
4. **KFG no es independiente.** El acuerdo mide fidelidad, no verdad. Para validar los valores haría falta el PDF del Databook o examen físico.
5. **AS033, AS035, AS101, AS207 y AS026** contienen varios quipus por archivo; sus observaciones y conteos se agrupan y deben tratarse con cuidado.
6. **No se usó la corrección de Thompson (2025)** ni la edición impresa; los errores que aquí llamamos “del Databook” podrían ser del OCR de 2026, no de 1988.

---

## 9. Para el coordinador

- **El parser funciona:** 14 953 filas, 210 quipus, cobertura mediana del 96 % de los colgantes descritos; 13 369 filas con valor. Los scripts son reproducibles (`parse_databook.py`, `decoder.py`, `crossmatch.py`, `analizar.py`).
- **La transcripción KFG es excelente en lo grueso:** valor 94.7 % (n = 5 890), color 92.2 %, largo 99.9 % (±0.5 cm). El nulo intra-quipu da 30.5 %, 42.9 % y 10.5 % (p = 0.001; Holm = 0.003). Pero el KFG deriva del Databook: esto mide fidelidad, no verdad.
- **El 5 % de discrepancias de valor (311 casos) no es homogéneo:** 128 son cuerdas que el KFG dejó sin nudos (valor 0), 70 son valores que el Databook marcó `?`, 45 son valores impresos del Databook que sus propios nudos no sostienen, 31 son convenciones ×10 y solo 14 son OCR evidente. **No hay ningún error aritmético claro del KFG cuando sus nudos están presentes.**
- **Los errores se concentran:** 60 quipus afectados, top-5 = 49 % (AS050 98, AS101_Part_2 24, AS069 12, AS013 10, AS101_Part_1 9). La mediana por quipu es 1.5 % y 39/92 quipus con ≥10 pares no tienen ninguna discrepancia.
- **Hallazgo crítico:** el KFG no siempre transcribe. En AS014, AS036, AS037, AS081 y AS129 hay valores KFG sin valores legibles en el Databook. En **AS081** el Databook dice “no numerical interpretation is possible” y el KFG le asigna 10, 5, 0, 7, 9, 0, 3, 8. En **AS129** copia valores concatenados (`1113`, `1748`…) como si fueran decimales.
- **Cuerdas fantasma:** 62 cuerdas KFG tienen largo 0, 14 con valor >0 (AS010 p26 = 10, AS042 p1 = 124, AS069 p1649 = 10). AS010 tiene 27 cuerdas en KFG frente a 25 en el Databook.
- **Cobertura del corpus:** 80 quipus del Databook (38 %) no están en KFG; 14 ids KFG AS no tienen Databook comparable (9 son AS001–009, fuera del rango; 4 son partes; AS195 es un fallo de parseo de subsidiarias). Cualquier análisis “de corpus” con KFG está perdiendo un tercio del Databook.
- **Color:** 92.2 % exacto; las diferencias son sobre todo códigos (B/AB, BB/B) y componentes añadidos (W, KB:W), no OCR. Normalizar antes de usar color como variable.
- **Notas listas:** 812 afirmaciones de 195 quipus, 116 con sumas/igualdades, en `notas_ascher.csv` (quipu → texto → tipo). Sirven para contrastar las relaciones de suma con nuestros hallazgos.
- **Recomendación:** usar el Databook como fuente primaria de valor y largo; usar KFG para nudos y estructura, pero marcar como “reconstruido” todo valor de AS014/036/037/081/129 y excluir AS081/AS129 de cualquier análisis decimal. Antes de la siguiente ronda, auditar a mano AS050, AS101_Part_2, AS069 y AS013, que concentran la mitad de los problemas.
