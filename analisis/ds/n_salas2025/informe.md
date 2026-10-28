# Salas García (2025), *La interpretación lingüística de los quipus*: lectura crítica y pruebas en el corpus KFG

**Autor del informe:** equipo `n_salas2025`
**Fecha:** 18 de octubre de 2026
**Archivos:** `claims.csv` (30 afirmaciones), `clasificadores.csv` (21 clasificadores/series), `pruebas_salas.py`, `robustez.py`, `pruebas_extra.py`, `pares_neto.py`, `hacer_tablas.py`, `resultados.csv`, `resumen.json`, `robustez.json`, `extras.json`, `pares_neto.json`.

---

## 1. Pregunta

¿Qué afirma Salas García sobre los quipus y la cuenta, qué parte de eso es una hipótesis lingüística defendible y qué parte se puede someter a prueba con el corpus KFG/OKR? En particular:

1. Si los clasificadores de pares *luc* y *felæp* describían registros reales, ¿hay un exceso de valores pares en algún grupo de quipus (por procedencia costera norte/yunga o por color)?
2. Si *chiæng* y *palæc* clasificaban centenas, ¿hay un exceso de valores múltiplos de 100 o de 10, y se asocian a color o procedencia?
3. ¿Los quipus de procedencia costera norte/yunga difieren de los demás en estructura numérica?
4. ¿Hay alguna otra predicción medible (orden ordinal, prelación, disposición espacial, calendario, confesión) que el corpus permita evaluar?

---

## 2. Qué dice el libro (síntesis operativa)

Salas parte de un hecho que él mismo subraya: **no se han hallado quipus en la zona donde se habló el mochica** (línea 1637). Su argumento no es arqueológico sino léxico: el sistema de clasificadores numerales del mochica, documentado por Carrera (1644) y Middendorf (1892), habría conservado fósiles semánticos de aquello que los quipus contaban. La estructura es decimal y los clasificadores están fusionados con las bases:

| Clasificador | Valor | Qué cuenta según Salas | Fuente principal |
|---|---:|---|---|
| *luc* | par (2) | frutas, hortalizas, huevos, cosas redondas, platos/mates | Carrera 1644: 188; Middendorf 1892: 129 |
| *felæp* | par (2) | aves, potos, platos, objetos grandes | Carrera 1644: 188; Middendorf 1892: 129 |
| *çiæcɥ* | 10 | diez absoluto, no combinatorio | Carrera 1644: 183 |
| *ssop* | 10 | cuerda: días/tiempo, ordinales, conjuntos ordenados, oraciones, confesión, monedas, pueblos en el espacio | Carrera 1644: 183, 258; Middendorf 1892: 68 |
| *pong* | 10 | piedra: humanos, animados, forma, categoría residual; también monedas | Carrera 1644: 182-186; Middendorf 1892: 68 |
| *cæss* | 10 | tiempo; parentesco, uso femenino, hilos | Carrera 1644: 206; Larco 1939: 74 |
| *cɥoquixll* | 10 | choclo/maíz: mazorcas, frutos y vegetales | Carrera 1644; Middendorf 1892 |
| *chiæng* | 100 | centenas de ciertas frutas (calabazas, camotes, ajíes) | Carrera 1644: 186; Middendorf 1892: 130 |
| *palæc* | 100 | lo que no cuenta *chiæng*; por oposición, animados | Carrera 1644: 109, 185 |
| *cunô* | 1000 | millar; préstamo quechua | Carrera 1644: 185 |

La tesis central es que **el clasificador dice qué se cuenta**, no que el color o la posición codifiquen significados léxicos. Para el quipu, *ssop* 'cuerda' permite inferir que la cuerda era el ordinal y el nudo el cardinal; de ahí el tiempo, los ordinales, los conjuntos ordenados, la confesión, las monedas y la disposición espacial de pueblos (cap. 7). El color aparece una sola vez como marcador de "trechos": Martos (1606) dice que los indios "señalando a trechos con hilos azules, verdes, amarillos y colorados" daban cuenta de su historia (línea 9335). **No hay en el libro una hipótesis de que el color sea un clasificador semántico estable.**

En el capítulo 10 Salas es escéptico de los "quipus narrativos": una anomalía numérica es indicio, no prueba, de narración; los números pueden generar relatos sin ser un código fonético (líneas 9542-9557, 9771-9813). Esto es relevante para evaluar el libro: no promete un desciframiento, ofrece una tipología de lo contable.

---

## 3. Datos y método

- **Corpus:** 651 quipus, 57 818 cuerdas en `cuerdas.csv`; 40 162 cuerdas con nudos registrados y valor ≥ 0 en 641 quipus. Se excluyen las cuerdas sin nudos (valor 0 = ausente, no cero real).
- **Color:** se eliminaron los rangos en cm con `re.sub(r'\([^)]*\)','',s)`; se usó el color base antes de `:`, `/` o `-`.
- **Unidad de análisis:** el quipu. Las pruebas a nivel de cuerda usan **permutaciones dentro de cada quipu**; las de procedencia permutan etiquetas entre quipus. Semilla fija `20251018` (y `777`, `99`, `4242` en robustez).
- **Nulo de paridad:** la paridad decimal no es 50 %. En el corpus, la unidad 0 es el 17,45 % de las cuerdas y la proporción empírica de valores pares es **52,88 %**. Cualquier prueba que asuma 50 % sobreestima los pares en ~2,9 puntos. Por eso se usa (a) la distribución empírica de dígitos y (b) un análisis "neto" que excluye las unidades 0, que son notación decimal y no pares.
- **Nulo de "redondez":** se permutan independientemente las decenas y las unidades dentro de cada quipu para probar si los múltiplos de 100 exceden lo esperado por los márgenes de cada posición.
- **Corrección múltiple:** 84 pruebas principales; se aplicaron Holm y Benjamini-Hochberg sobre todas. Las pruebas exploratorias adicionales (paridad neta, rachas, colores dirigidos) se reportan aparte y no se mezclan con las 84.
- **Procedencia:** nunca se usó el museo como lugar de origen. Se definió *costa norte/yunga* como La Libertad, Lambayeque, Piura y Tumbes; *costa norcentral* como Santa, Huacho y Huaura (proxy, no yunga).

**Limitaciones.** KFG es una decodificación moderna; el "valor" depende de las convenciones de Ascher/Urton y de la ausencia de racimos de unidades. No hay metadatos de qué se contaba en cada cuerda. Las procedencias son de museo/colección y 286 quipus son desconocidos.

---

## 4. Resultados

### 4.1 Cobertura: no hay muestra yunga

De los 651 quipus, **365 tienen procedencia identificable** y **0** proceden de La Libertad, Lambayeque, Piura o Tumbes. Hay 14 en la costa norcentral (6 de Santa, 7 de Huacho y 1 de Huaura) y 286 desconocidos. Es decir, **la predicción central de Salas (ausencia de quipus mochicas) se cumple en el corpus, pero no se puede contrastar la predicción alternativa (que los quipus yungas tuvieran estructura distinta), porque no hay muestra.** La ausencia es además débil como dato histórico: refleja qué se conservó y qué se catalogó, no necesariamente qué existió.

### 4.2 Pares (*luc*, *felæp*)

**Nivel global.** El 52,88 % de las 40 162 cuerdas válidas tiene unidad par. La distribución de unidades no es uniforme (χ² = 10 535,6; gl = 9; p < 1e-300): 1 es el dígito más frecuente (19,28 %), seguido de 0 (17,45 %) y 2 (14,36 %). La paridad "de fondo" no es 50 %, y hay un exceso de unidades 0 y 1.

**Paridad neta.** Excluyendo las unidades 0 (33 153 cuerdas), la proporción de pares es **42,92 %**, frente al 44,44 % teórico de dígitos 1-9 uniformes. No hay un exceso global; hay un leve déficit.

**Heterogeneidad entre quipus.** La fracción de pares por quipu está muy sobredispersa: en los 487 quipus con ≥10 cuerdas netas, la desviación estándar de los z es 1,86 (p(χ²) = 1,5e-132), y **24 quipus siguen siendo significativos tras BH**. Algunos ejemplos:

| Quipu | n netas | pares | tasa | valores dominantes | procedencia |
|---|---:|---:|---:|---|---|
| UR037 | 150 | 133 | 88,7 % | 107 doses, 17 cuatros | Unknown |
| MM019 | 211 | 157 | 74,4 % | 103 doses, 27 seises | Unknown |
| UR216 | 61 | 52 | 85,2 % | 31 cuarentayochos, 16 veinticuatro | Pachacamac |
| AS036 | 30 | 29 | 96,7 % | 4, 6, 8 | Maranga, Huaca 1 |
| UR1084 | 208 | 134 | 64,4 % | 22, 32, 12, 33 | Unknown |
| HP055 | 121 | 84 | 69,4 % | 22, 33, 222, 12 | unknown |

En el otro extremo hay quipus con **déficit** de pares porque casi todas sus cuerdas valen 1: UR087 (24,3 % pares; 309 cuerdas netas), UR1057 (19,4 %), AS071 (17,8 %), UR003 (28,7 %). Es decir, el corpus es bimodal: registros de "unos" y registros de "doses/cuatros". **Hay quipus que parecen contar pares, pero son casos individuales, no un grupo de procedencia ni de color.**

**Color.** Ningún color muestra un exceso de paridad neta tras corrección: el mejor es RB (395 cuerdas, 44,3 % vs 39,9 % nulo; p = 0,027; BH = 0,43). Los aparentes efectos de color en la paridad bruta (KB, LB, HB) desaparecen al excluir las unidades 0. **No hay apoyo para que el color marque "pares".**

**Repetición adyacente.** Hay 2 533 pares de cuerdas consecutivas con el mismo valor >1, frente a 1 661 esperados por permutación (z = 27,4; p = 0,0003). Pero las rachas de longitud 3 también exceden (214 vs 148; ratio 1,44) más que las de longitud 2 (ratio 1,19). El fenómeno es **agrupamiento general de valores repetidos**, no una firma específica de pares. Además, los valores repetidos más frecuentes son 2 (204 casos), 4 (143), 3 (116) y 10 (111): mezcla de conteo de pares y de decenas.

**Nivel de evidencia:** *apoyado con datos* que existen registros que cuentan en pares o con valores pares dominantes (UR037, MM019, AS036, UR216); *propuesto* que eso corresponda a *luc*/*felæp*; *no apoyado* que sea un rasgo yunga o de un color.

### 4.3 Decenas y centenas (*ssop*, *pong*, *chiæng*, *palæc*)

**El "exceso" de múltiplos de 10 es notacional.** 7 009 cuerdas (17,45 %) terminan en 0. Pero solo **65 cuerdas (0,16 %)** tienen un nudo 0 explícito; en las demás, el 0 de unidad es **ausencia de racimo**, no un cero contado. Un valor 120 se registra como `1S,100;2S,20` sin racimo de unidades. Por tanto, "múltiplo de 10" no es evidencia de un clasificador de decenas: es la representación posicional decimal.

**Múltiplos de 100.** Hay 776 cuerdas con valor ≥100 y dos ceros finales (1,93 %), frente a 434,5 esperadas si las posiciones de decenas y unidades fueran independientes (ratio 1,79; p = 0,0005). El exceso es real como descriptivo: las cantidades "redondas" de cien son más frecuentes de lo que predicen los márgenes. Pero (a) es exactamente lo que produce una contabilidad decimal con cantidades redondas, y (b) **no se asocia de forma robusta a color ni a procedencia**. El único color con señal, DB, debe el 77 % de su exceso a un solo quipu (UR1109: 45 de 92 cuerdas DB son múltiplos de 100; aporte 13,4 de 17,4). KB y unidades 0: el 55 % del exceso viene de tres quipus (UR122, AS066, UR270). Son casos, no clases.

**Grupos de tamaño 10.** Hay 215 grupos de exactamente 10 cuerdas, frente a 166 esperados por composición aleatoria (z = 3,85; p = 0,0001). Pero el control negativo inmediato lo desmonta: hay **256 grupos de 9** y 175 de 11; el tamaño 10 no es un pico local (215 vs 215,5 del promedio de sus vecinos). El "efecto" es un artefacto del nulo de composición uniforme, no una firma de los diez mandamientos ni de la decena.

**Nivel de evidencia:** *bien apoyado en el corpus* que los ceros de unidad son ausencia de racimo; *no apoyado* que *chiæng*/*palæc* dejen una huella detectable en forma de centenas exactas o grupos de 10.

### 4.4 Estructura por procedencia (costa norte/yunga)

No hay quipus yungas. Como proxy se compararon los 14 quipus de la costa norcentral (6 de Santa) con el resto:

- Los 14 quipus norcentrales tienen **más cuerdas** (diferencia en log1p = 1,14; p = 0,0003; Holm = 0,025); el subgrupo de Santa (6 quipus) tiene mediana 106 vs 31 (Mann-Whitney p = 0,0027).
- No difieren en paridad, proporción de unidades 0, múltiplos de 100, valor medio, valor máximo ni proporción de subsidiarias (todos p > 0,4).
- El efecto de tamaño está dominado por 6 quipus de Santa, todos grandes (50-321 cuerdas). Es compatible con un sesgo de colección/museo y con n = 6; no se puede separar "región" de "colección".

**Nivel de evidencia:** *apoyado con datos* solo para el tamaño; *no concluyente* para estructura numérica; *no testeable* para yunga.

### 4.5 Color y posición como clasificadores

**Color y límites de grupo.** Hay un efecto consistente: en los límites entre grupos de colgantes, la probabilidad de que cambie el color es **47,4 %**, frente a **38,4 %** dentro de los grupos (diferencia +9,0 puntos; p = 0,00033; Holm = 0,027). En el análisis robusto por quipu (435 quipus con ambos tipos de pares), la diferencia media es **+12,8 puntos** (p = 0,0002; 59,5 % de los quipus con diferencia positiva). Los grupos de KFG se definen por espaciamiento físico (`grupos.csv`, `espacio_cm`), no por color, lo que reduce la circularidad del test. Es el hallazgo sustantivo más sólido de esta ronda: **el color cambia más en las fronteras de grupo que dentro de ellos**, lo que apoya la idea de que el color marca secciones/trechos, tal como sugiere Martos (1606). No apoya que un color concreto signifique una clase de objeto.

**Posición y ordinalidad.** Si la cuerda es el ordinal y el nudo el cardinal, la posición no debería predecir la magnitud. Los datos son compatibles con esa independencia: correlación intragrupo posición-valor r = **-0,009** (p = 0,001, pero efecto despreciable); Spearman medio por quipu = **-0,071**; la distribución es ancha y bimodal (41 % con |ρ| > 0,3, en ambos signos). No hay una tendencia monotónica global. La "prelación" (lo más importante primero) tampoco aparece: r = **-0,012** (p = 0,0005, efecto nulo). **La posición no codifica magnitud de forma estable.**

**Nivel de evidencia:** *apoyado con datos* que el color marca límites de grupo; *propuesto* que la posición sea un ordinal; *no apoyado* que el color o la posición sean clasificadores semánticos de tipo "qué se cuenta".

### 4.6 Otras predicciones: calendario, confesión, "cuerda = día"

- **Calendario de 730 cuerdas.** El corpus no contiene un quipu con 24 grupos de 29-31 cuerdas. UR003 tiene 758 cuerdas, pero solo 15 grupos y ningún grupo de 29-31. El quipu-calendario CMA-625/LC1-254 de Urton no se puede identificar en KFG con esta segmentación. **No verificable.**
- **"Cuerda = día".** De 126 quipus con ≥100 cuerdas, la fracción media de valores 1 es 14,6 % (mediana 8,8 %); **ninguno** supera el 80 % de unos. Hay excepciones (AS071 75,2 %, UR1032 71,4 %, UR1057 66,3 %, UR003 58,8 %), pero no es un patrón general. **No apoyado** como modelo universal; compatible con casos concretos.
- **Confesión (9-10 hilos).** No se puede identificar sin contexto; el tamaño 10 no muestra pico local. **No testeable con estos metadatos.**
- **Disposición espacial de pueblos (Chucuito).** Requiere identificar pueblos en cuerdas; KFG no los tiene. **No testeable.**

### 4.7 Tabla de supervivientes y veredicto

De 84 pruebas principales, 8 pasan Holm y 9 pasan BH. Tras el escrutinio:

| Prueba | p | Holm | Efecto | Veredicto |
|---|---:|---:|---|---|
| `grupo_tamano10` | 0,00012 | 0,0098 | 215 vs 166 | **Artefacto**: 9 es más frecuente (256); sin pico local |
| `estructura_santa_n` | 0,0003 | 0,0249 | +1,14 log cuerdas | **Débil**: 14 quipus (6 de Santa), sesgo de colección |
| `color_limite_grupo` | 0,00033 | 0,0273 | +9,0 pp | **Robusto**: se replica por quipu (+12,8 pp) |
| `pares_adyacentes` | 0,00033 | 0,0273 | 2 533 vs 1 661 | **Inespecífico**: las rachas de 3 exceden más |
| `color_u0|KB` | 0,0005 | 0,0400 | +3,3 pp | **Frágil**: 55 % del exceso en 3 quipus |
| `color_c100|DB` | 0,0005 | 0,0400 | +2,9 pp | **Un solo quipu** (UR1109, 77 %) |
| `mult100_independencia` | 0,0005 | 0,0400 | ratio 1,79 | **Notacional/redondez**; sin asociación robusta |
| `prelacion_grupos` | 0,0005 | 0,0400 | r = -0,012 | **Efecto nulo** pese al p |

**Conclusión de la tabla:** solo el efecto color-límite de grupo sobrevive como hallazgo sustantivo. Los demás p pequeños son artefactos de nulos mal especificados, casos únicos o efectos triviales por n grande.

---

## 5. Resultados negativos (explícitos)

1. **No hay quipus yungas** en el corpus: 0 de 365 con procedencia identificable.
2. **No hay exceso de pares asociado a color** tras excluir los múltiplos de 10 y corregir por múltiples comparaciones.
3. **No hay exceso de pares asociado a la costa norcentral** (proxy): diferencia de +1,9 pp, p = 0,36.
4. **No hay exceso de múltiplos de 100 asociado de forma robusta a color o procedencia**; DB es un solo quipu.
5. **No hay grupos de 10** más frecuentes que sus vecinos 9 y 11.
6. **No hay estructura de calendario 24×30** en KFG.
7. **No hay apoyo para "una cuerda = un día"** como patrón general.
8. **No hay orden monotónico** entre posición y valor, ni prelación estable.
9. **No hay diferencia numérica** entre costa norcentral y resto, salvo tamaño.
10. **No hay evidencia de que el color codifique clases semánticas**; solo marca límites de sección.

---

## 6. Evaluación crítica del libro

### 6.1 Lo sólido (bien apoyado / apoyado con datos)

- **El sistema de clasificadores mochicas está bien documentado** en Carrera (1644) y Middendorf (1892): *luc*/*felæp* = pares, *chiæng*/*palæc* = centenas, *ssop*/*pong*/*cæss*/*cɥoquixll* = decenas. Esto es dato lingüístico, no especulación.
- **La etimología y la semántica de los clasificadores** (*luc* < 'pie', *felæp* < 'sentado', *cɥoquixll* < quechua 'choclo', *cunô* < quechua 'mil') son defendibles y citan fuentes primarias.
- **Salas es honesto sobre el límite arqueológico**: no hay quipus mochicas, y el vínculo es inferencial.
- **El color como marcador de trechos** tiene apoyo documental (Martos 1606) y, en nuestro corpus, un efecto estadístico robusto de +9 a +13 pp en los límites de grupo. Es la parte de su teoría que mejor se sostiene, aunque el libro no la desarrolla como hipótesis central.
- **El escepticismo sobre los quipus narrativos** es metodológicamente sano: una anomalía no prueba narración.

### 6.2 Lo propuesto (inferencia razonable, no bien apoyada)

- **La transferencia de los clasificadores mochicas a los quipus**: es una analogía semántica plausible, pero no hay un corpus yunga que la confirme. El propio Salas lo dice.
- **La cuerda como ordinal y el nudo como cardinal**: es coherente con la iconicidad y con la independencia posición-valor que encontramos, pero no se sigue de los datos.
- **El orden espacial de pueblos** (Chucuito) está documentado en la visita, pero no se puede probar en KFG.
- **El calendario de 730 días** es una interpretación de Urton para un quipu concreto; Salas la usa como ancla, no la demuestra.

### 6.3 Lo especulativo

- **Que *ssop* 'cuerda' haya derivado del uso de los quipus** (o sea un calco de *caitu*): etimología verosímil, sin prueba independiente.
- **La estructura de los quipus de confesión** (9-10 hilos, subsidiarias, nudos que cuentan pecados): reconstrucción plausible a partir de catecismos, pero sin identificación de un quipu real.
- **La narración a partir de números**: es una posibilidad lógica, no un hallazgo; el propio autor la presenta como propuesta.
- **Que los clasificadores de decena hayan penetrado por contacto inca**: hay préstamos léxicos, pero la cronología y la dirección no se pueden fijar con estos datos.
- **Cualquier intento de mapear *luc*/*felæp* a colores o posiciones concretas**: el libro no lo hace y nuestros datos no lo apoyan.

### 6.4 Aporte a la hipótesis "color/posición como clasificador"

El libro **no propone** que el color sea un clasificador semántico. Su aporte es distinto:

1. **Refuerza que el clasificador es "qué se cuenta"**, no "cómo se pinta". Esto desplaza la pregunta desde "¿qué significa el rojo?" hacia "¿qué se contaba en esta cuerda?".
2. **Sugiere que la posición es ordinal**, no magnitud: la cuerda indica el lugar en una serie (mandamiento, pueblo, día), y el nudo la cantidad. Nuestros datos son compatibles (r ≈ 0), pero no lo prueban.
3. **El color como marcador de secciones** es la versión débil y defendible: no codifica clases de objetos, pero segmenta el discurso. El efecto de límites de grupo es el único hallazgo robusto de esta ronda.
4. **La ausencia de quipus yungas** es un resultado negativo importante: la hipótesis de una influencia mochica directa sobre los quipus serranos no se puede testear con este corpus; solo se puede testear la huella léxica.

**Veredicto global:** el libro es una obra de lingüística histórica y semántica, no un desciframiento. Su valor está en el inventario de clasificadores y en la disciplina de distinguir fuente, inferencia y especulación. Su debilidad es que casi todas las predicciones numéricas fuertes (pares, centenas, calendario, confesión) no dejan una huella separable de las convenciones decimales y de la heterogeneidad de los registros. Lo que sí deja huella es el uso del color para marcar secciones.

### 6.5 Resumen de niveles de evidencia

| Hallazgo | Nivel |
|---|---|
| El sistema de clasificadores mochicas (valores y semántica) está documentado en Carrera/Middendorf | **Bien apoyado** (filológico) |
| No hay quipus yungas en el corpus: 0 de 365 con procedencia identificable | **Bien apoyado en el corpus** (no histórico) |
| Los ceros de unidad son ausencia de racimo, no ceros contados (solo 65 nudos 0 explícitos) | **Bien apoyado en el corpus** |
| El color cambia más en los límites de grupo (+9 pp; +12,8 pp por quipu) | **Apoyado con datos** |
| Existen quipus que registran valores pares dominantes (UR037, MM019, AS036) | **Apoyado con datos** |
| No hay asociación entre pares y color o procedencia yunga/norcentral | **Bien apoyado en el corpus** (negativo) |
| La cuerda es ordinal y el nudo cardinal | **Propuesto** (compatible con r ≈ 0) |
| Los clasificadores mochicas se transfieren a los quipus | **Propuesto** (analogía sin corpus yunga) |
| *Ssop* deriva del uso de quipus / es calco de *caitu* | **Especulativo** |
| El quipu de confesión tiene 9-10 hilos y nudos que cuentan pecados | **Especulativo** |
| La narración a partir de números | **Especulativo** (posibilidad lógica) |
| El calendario de 730 días | **Propuesto** para un quipu concreto; no verificado en KFG |

---

## 7. Para el coordinador

- **No hay muestra yunga:** 0 de 365 quipus con procedencia identificable son de La Libertad, Lambayeque, Piura o Tumbes. La predicción de Salas (ausencia de quipus mochicas) se cumple, pero no se puede comparar estructura yunga vs resto; el proxy norcentral son solo 14 quipus (6 de Santa).
- **La paridad no es 50 %:** el 52,88 % de las cuerdas válidas tiene unidad par; 0 y 1 son los dígitos más frecuentes (17,45 % y 19,28 %). Excluyendo unidades 0, la paridad neta es 42,92 %, no hay exceso global.
- **Sí existen quipus que cuentan en pares, pero son casos:** UR037 (107 doses; 88,7 % pares), MM019 (103 doses; 74,4 %), AS036 (29/30 pares), UR216 (85,2 %). No se asocian a color ni a procedencia; el color no muestra exceso de pares tras corrección (mejor p = 0,027, BH = 0,43).
- **Los múltiplos de 10 son notación, no clasificador:** solo 65 cuerdas (0,16 %) tienen un nudo 0 explícito; el resto de los "ceros" son ausencia de racimo. Los múltiplos de 100 exceden 1,79× lo esperado por independencia, pero es redondez decimal y no se asocia robustamente a color/procedencia (DB depende de un solo quipu, UR1109).
- **El grupo de 10 es un artefacto:** 215 grupos de 10 vs 166 esperados, pero hay 256 de 9 y 175 de 11; no hay pico local. No sirve como evidencia de los diez mandamientos.
- **El hallazgo robusto es el color como límite de sección:** 47,4 % de cambios de color en fronteras de grupo vs 38,4 % dentro (+9,0 pp; Holm = 0,027), y +12,8 pp en el análisis por quipu (p = 0,0002; 59,5 % de quipus positivos). Apoya "color = trechos", no "color = clase semántica".
- **La posición no codifica magnitud:** r = -0,009; Spearman medio -0,071; sin prelación estable (r = -0,012). Es compatible con cuerda-ordinal/nudo-cardinal, pero no lo demuestra.
- **El calendario y "cuerda = día" no se sostienen en KFG:** no hay quipu con 24 grupos de 29-31; de 126 quipus grandes, ninguno tiene >80 % de unos (media 14,6 %).
- **Para la siguiente ronda:** (1) estudiar los quipus de "doses" (UR037, MM019, AS036) contra sus colores y grupos, para ver si el par se marca localmente; (2) buscar colecciones yungas o procedencias finas; (3) replicar el efecto color-límite en OKR con segmentación independiente; (4) probar si los quipus de 9-10 grupos existen en contextos coloniales; (5) no usar la paridad bruta como prueba de pares: siempre excluir unidades 0.
