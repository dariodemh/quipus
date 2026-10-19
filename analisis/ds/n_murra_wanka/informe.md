# El quipu wanka de Hatun Xauxa (1561): estructura, proporcionalidad y comparación con Incahuasi

*Equipo `n_murra_wanka`. Fuente principal: John V. Murra, «The Ethno-Categories of a Regional Khipu», Andean Past Special Publication 13 (2024), texto en `analisis/fuentes_txt/Murra2024_EthnoCategories.txt` (artículo pp. 13–29; cuadro reconstructivo pp. 31–50). Datos derivados en esta carpeta; scripts `01`–`06`; semilla 20261018.*

---

## 1. Pregunta

1. ¿Cuál es la **estructura** del registro que los khipukamayuq de Hatun Xauxa leyeron en 1561: cuántas categorías, en qué orden, con qué ejes (evento/año, saya, entregado/saqueado), con o sin totales?
2. ¿Se sostiene la regla de que los bienes se movilizaban «en proporción directa a la población de cada saya»?
3. ¿En qué se parece y en qué se diferencia este registro del sistema de Incahuasi (UR278: 28 registros × 9 partes)?
4. Si el quipu se hubiera conservado, ¿qué forma de cuerdas tendría, y hay algún quipu del corpus con esa forma?

## 2. Método y una advertencia sobre la fuente

Leí el artículo por tramos (pp. 13–29 en inglés y español, notas editoriales pp. 31–37, cuadro pp. 38–50). El cuadro reconstructivo se imprime en seis páginas (dos clústeres por página) y el OCR **pierde las coordenadas de columna**: cada celda queda en un renglón distinto, de modo que se conserva el *orden* de los valores de cada fila pero no a qué cuerda pertenece cada uno cuando la fila tiene celdas vacías. No hay PDF local ni acceso al PDF original (el repositorio de la Universidad de Maine está detrás de una prueba de navegador y la revista ya no sirve el PDF). Por eso:

- **No inventé la asignación valor→columna.** Guardo la secuencia de valores por evento y por par de clústeres (`wanka_celdas.csv`), y trabajo con cantidades **invariantes a esa asignación**: el total de la fila de un macro-grupo, el número de cuerdas con dato y el número total de cantidades.
- `wanka.csv` (pedido) tiene una fila por cantidad impresa: `saya, anio, evento, i_evento, categoria, orden_en_grupo, cantidad, unidad, columna`. La columna `columna` vale `desconocida` en todas las filas: es honesto, no un descuido. `categorias_wanka.csv` da las 43 cuerdas con su etiqueta, unidad y flujo.
- Unidad de análisis: **el evento** (19), no la cantidad (361). Los nulos permutan eventos dentro de cada macro-grupo, preservando las marginales. 20 000 permutaciones; Holm sobre 5 pruebas.

## 3. Estructura del registro

### 3.1 Arquitectura

| Rasgo | Valor | Fuente |
|---|---|---|
| Cuerdas colgantes | **43**, de un solo cordón principal | nota editorial, p. 31 |
| Clústeres / categorías | **12** (I–XII) | nota editorial, p. 31 |
| Cuerdas por categoría | 2, 3, 3, 6, 6, 4, 3, 5, 4, 2, 2, 3 | cuadro |
| Eje temporal | **19 eventos** (a–q, con `ch` y `ll`) en orden histórico estricto, 1533–1548 | Murra, p. 16 |
| Años explícitos | solo **8 de 19** (1533, 1533–34, 1537, 1538, 1539, 1541, 1542, 1548); el resto se ubica por secuencia | cuadro |
| Flujos | **27 cuerdas «entregado» + 9 «rancheado/saqueado» + 7 «a la salida»** | cuadro |
| Subtotales o totales | **ninguno** (ni fila ni columna de total; «total» solo aparece en el texto de Lechtman) | cuadro |
| Eje saya | **ninguno**: el cuadro es solo de Hatun Xauxa | encabezado del cuadro |
| Celdas con cantidad | **361** de 817 posibles (44,2 %) | `wanka_celdas.csv` |

Orden de las 12 categorías (constante en las 19 filas): **(I)** personas (varones, mujeres) → **(II)** camélidos (ovejas/llamas, carneros para comida, saqueados) → **(III)** textiles (vestidos/lana/cumbi, frazadas, vestidos saqueados) → **(IV)** cultivos (maíz, quinua, papas; y sus versiones saqueadas) → **(V)** fibras de cabuya (sandalias, soga, aderezos de caballo) → **(VI)** cerámica (cántaros/ollas/tinajas, vasijas pequeñas/mates) → **(VII)** aves (gallinas de Castilla, huevos, perdices) → **(VIII)** vegetales no cultivados (leña, astillas, carbón, hierba, paja) → **(IX)** bebida y productos de valle (chicha, fruta, sal, pescado) → **(X)** personas «a la salida» (cargadores, yanaconas) → **(XI)** camélidos «a la salida» → **(XII)** alimentos para el camino (maíz, quinua, papas).

Dos observaciones estructurales que el cuadro permite y que conviene retener:

- **El orden no es una lista de productos, es una jerarquía de reinos**: seres vivos → cosas (textiles → cultivos → fibra → cerámica) → un intruso colonial (aves, añadido en 1537) → vegetales silvestres → valle/sierra → lo que sale con la gente. Murra lo dice explícitamente (pp. 17–19) y propone que el clúster VII fue **intercalado** después de 1532 al final de la macrocategoría III–VI.
- **Hay dos criterios de clivaje dentro de cada categoría**: el flujo (entregado vs rancheado) y el momento (durante vs «a la salida»). Ambos son *sub-ejes*, no categorías nuevas.

### 3.2 Años, no décadas

El registro **no es anual**: es una lista de 19 acontecimientos datados cuando el acontecimiento importa (entrada de Pizarro 1533, Alvarado 1537, sitio de Lima 1538, Mercadillo 1539, Mazuelas 1541, Vaca de Castro 1542, Gasca 1548). Los años intermedios se deducen por la secuencia, no se anotan. Murra subraya que los 19 eventos se leyeron «en estricto orden histórico» y que eso ya es información que excede la aritmética.

### 3.3 Un defecto de la fuente: filas duplicadas

Los eventos **`ll` y `m` son idénticos** en 3 de las 6 páginas del cuadro (p. 40: `210;300;15;25;123`; p. 41: `22;450;31;50;2933;30541;3214`; p. 42: `1041;612;60;80` + un `86` adicional). El propio cuadro lo advierte («† Scribal error? Error by the khipukamayoq?»). Esto importa: (a) confirma que la transcripción es fiel al original, no una reconstrucción libre; (b) **invalida tratar las 19 filas como observaciones independientes**; (c) sugiere que el khipu tenía un registro repetido o que el escribano copió un renglón.

## 4. La regla «en proporción directa a la población de cada saya»

### 4.1 No es verificable con esta fuente (resultado principal)

La afirmación que cita LeVine (1992:264–265) —«from 1533 to 1537 the Lurinwanka and Hatunxauxa provincial divisions (saya) repeatedly mobilized certain classes of goods in direct proportion to the relative populations of the two saya»— **no se puede contrastar con Murra (2024)**:

- El cuadro es **solo de Hatun Xauxa** (encabezado: «khipu deposition by the lords of Hatun Xauxa»). No hay una sola cifra de Lurin Wanka ni de la tercera fratría.
- No hay población por saya en el artículo. La única cifra demográfica es **~27 000 unidades domésticas para toda la etnia wanka en 1532** (Vega 1582, citado en p. 24), sin desagregación.
- Murra dice expresamente que la estructura social de **«las tres fratrías wanka»** aún no se conoce y que el papel del 266/133 «todavía no hemos descifrado» (pp. 16, 24). Es decir: el propio autor del análisis declara que la variable independiente (población relativa de cada saya) es desconocida.
- La regla tampoco aparece formulada en el artículo: es una **glosa de LeVine**, no un resultado de Murra. En el texto de Murra la palabra «saya» no aparece ni una vez.

**Conclusión:** la regla es, en el mejor de los casos, una hipótesis de la literatura secundaria, y con los datos publicados **no es contrastable**. Etiqueta: *demostrado* que la fuente no permite el contraste; *especulativo* el contenido de la regla.

### 4.2 Lo que sí se puede probar: un factor de escala por evento

Aunque no haya sayas, el registro sí tiene un eje «tamaño del acontecimiento». Si la movilización fuera «proporcional» (una canasta fija escalada por el número de personas atendidas), todas las categorías deberían moverse juntas y el vector de cantidades de cada evento debería ser un múltiplo escalar de un vector común. Eso sí es testeable con totales por macro-grupo:

| Prueba | Estadístico | Nulo (20 000 permutaciones) | p | Holm |
|---|---|---|---|---|
| T1a co-movimiento de magnitudes (log₁₀ total por macro-grupo) | ρ de Spearman medio = **+0,573** | IC95 [−0,198; +0,233] | <5·10⁻⁵ | 2·10⁻⁴ |
| T1b co-movimiento del n.º de cuerdas con dato | ρ medio = **+0,320** | IC95 [−0,104; +0,134] | 1·10⁻⁴ | 2·10⁻⁴ |
| T2 estructura de rango 1 (PC1 de la matriz 19×6 estandarizada) | **62,0 %** de varianza | máx. nulo 95 % = 39,9 % | <5·10⁻⁵ | 2·10⁻⁴ |

Las 6 macro-categorías **co-mueven**: cuando un evento es grande, es grande en todas (ρ=0,57). La matriz evento×categoría es compatible con un modelo de **un solo factor de escala** (62 % de la varianza en PC1, frente a 40 % que produce el nulo). Además, dentro de cada macro-grupo, los eventos con más cuerdas con dato son también los de mayor magnitud (ρ positivo en **6/6**, significativo en 5/6; `06_checks.py`).

Esto es *compatible* con la lógica «canasta fija × escala», pero la escala no es la población de la saya: es el tamaño del acontecimiento (número de españoles, campaña, saqueo). Y el ajuste no es perfecto: PC1 deja 38 % de varianza idiosincrásica (cada categoría tiene su historia: el maíz de las campañas, la leña de los campamentos).

### 4.3 Tendencia temporal

| Prueba | Resultado |
|---|---|
| ρ(evento, magnitud) por macro-grupo | negativa en **6/6**; sign test p = 0,031 (Holm 0,031) |
| ρ(evento, n.º de cuerdas con dato) | **−0,01**, p = 0,95 (sin tendencia) |
| Concentración | evento `a` (1533) = **43,2 %** de la suma bruta; `a`+`b`+`c`+`ch`+`d`+`e` (1533–34) = **56,5 %**; Gasca (1548) = 3,8 % |

Lectura: las cantidades **decaen** con el tiempo (consistente con el agotamiento de los depósitos), pero la **amplitud del registro no se estrecha**: se siguen usando las mismas 12 categorías hasta 1548, con cifras menores. Esto **modera** la lectura de Murra de que las cuerdas de lo saqueado «reciben poca atención» después del primer contacto: lo que baja es el volumen, no el número de categorías registradas.

### 4.4 El contraste que falta (diseño)

Para probar la regla haría falta una matriz **saya × categoría × año** (Hatun Xauxa y Lurin Wanka, 12 categorías, 8 años datados ≈ 96 celdas) y la población relativa de cada saya. El contraste correcto no es «¿hay más de Hatun Xauxa?» (siempre lo habrá, si es la saya mayor), sino:

1. **Estabilidad de la razón:** para cada categoría y año, r\[t] = cantidad(Lurin)/cantidad(Hatun). La regla predice r\[t] = P(Lurin)/P(Hatun) = constante. Se testea con un modelo log-lineal `log(cantidad) ~ saya + categoría + año` y se examina la interacción saya×categoría: la regla exige interacción nula. Con 96 celdas y ~12 categorías, la potencia para detectar desviaciones del 50 % es razonable.
2. **Contraste de proporciones:** bondad de ajuste de las 12 proporciones observadas contra las proporciones poblacionales (χ² o G-test con corrección de continuidad), por año, con BH-FDR sobre los 8 años.
3. **Nulo:** permutar la etiqueta de saya dentro de cada categoría-año (preservando totales) daría la distribución de r bajo «no hay efecto saya»; el nulo relevante para la regla es distinto: simular cantidades multinomiales con probabilidades = población relativa y ver si el CV observado de r cae dentro.

Nada de esto es posible con Murra (2024). Queda como especificación para cuando se digitalice Espinoza Soriano (1971–72) o la visita de 1558–61.

### 4.5 Redondeo

19,7 % de las 361 cantidades son múltiplos de 10 (IC95 binomial [15,7; 24,1]; bootstrap por evento [14,3; 25,5]), frente al 10 % esperado si los valores fueran arbitrarios (p = 3·10⁻⁸; Holm 1,6·10⁻⁷). En las 234 celdas de las 26 filas completas de UR278 solo el 7,3 % son múltiplos de 10. El redondeo wanka es plausiblemente **del escribano** (unidades europeas: hanegas, libras, cargas) más que del khipu; no lo uso como evidencia de cuotas administrativas.

## 5. Comparación cuantitativa con Incahuasi (UR278)

| Dimensión | Wanka 1561 | Incahuasi UR278 | Comentario |
|---|---|---|---|
| Categorías | **12** (taxonómicas: personas, camélidos, textiles…) | **1** ítem (no identificado) partido en **9** partes | Ejes distintos |
| Partes paralelas | **19 eventos** | **28 registros** (filas) | Wanka = tiempo; Incahuasi = unidades administrativas |
| Cuerdas | 43 declaradas / **361 cantidades** | **28 × 9 = 252** cuerdas (249 celdas con dato) | |
| CV entre partes | **1,96** (entre los 6 macro-grupos, dentro del evento) | **0,187** (perfil medio entre las 9 columnas); 0,304 dentro de fila | Wanka es 10× más desigual: son cosas distintas, no cuotas |
| max/min | — (unidades heterogéneas) | **2,62** por fila | Wanka no comparable |
| Estabilidad de proporciones | PC1 = 62 % (un factor de escala) | perfil estable; Friedman χ² = 90,6, p = 3,5·10⁻¹⁶ | Ambas tienen estructura, pero de signo distinto |
| Variabilidad entre registros | CV temporal 1,46–2,66 por categoría | CV de totales de fila = 0,37 | Incahuasi es uniforme; Wanka es disperso |
| Magnitudes | mediana 233; máximo 321 354; **35 valores ≥10⁴** | celdas ~100–450; totales de fila 875–4 273 | Wanka exige cuerdas de 5–6 posiciones |
| Cuotas | **no hay**: proporciones libres y distintas por categoría | 9 partes casi iguales (perfil 8,0–14,0 %; media 11,1 %) | Incahuasi = reparto; Wanka = rúbrica |
| Orden | constante (declarado) | identidad = mejor de 9! en los 5 pares UR270–UR278 (1/362 880) | **Único rasgo realmente compartido** |
| Totales / subtotales | **ausentes** | **presentes**: la cabecera de cada grupo es la suma de sus 9 cuerdas (UR275/UR266) | Diferencia jerárquica clave |
| Unidades | heterogéneas y europeas | homogéneas | |
| Co-movimiento entre columnas | ρ = 0,57 | ρ = 0,63 | En ambos lo produce el tamaño del registro/fila; no distingue |

**Interpretación.** Incahuasi y el registro wanka comparten solo dos cosas: (a) **un orden de columnas que se conserva** y (b) **una arquitectura de grupos de cuerdas con un fan de colgantes**. Todo lo demás es opuesto: Incahuasi es una **partición administrativa de partes casi iguales** (CV 0,19) de un mismo ítem, replicada en 28 registros y **con totales de cabecera**; el wanka es una **taxonomía de bienes distintos** (CV 1,96), replicada en 19 eventos, **sin totales**, con unidades y magnitudes heterogéneas. El primero se parece a una hoja de cálculo con celdas equivalentes; el segundo, a un libro de cuentas por rúbricas y fechas.

## 6. Cómo se vería el quipu wanka en cuerdas

### 6.1 El problema aritmético: 43 cuerdas no pueden contener 361 números

La nota editorial afirma que el quipu eran **43 cuerdas colgando de un solo cordón** y que Lechtman construyó con sus estudiantes las **primeras 6 categorías = 24 cuerdas** para **un solo evento** (1533). De ahí:

- 1 cuerda = 1 número (sintaxis estándar del khipu). 43 cuerdas = 43 números. (El conteo de 361 incluye unos pocos números escritos dentro de una misma celda —«In chains 532», «354 measures», «86 for Guadocheri»— y una lectura alternativa marcada con asterisco, 13 045; el orden de magnitud no cambia.)
- El cuadro contiene **361 números** = 8,4 × 43. Para las primeras 6 categorías y los 19 eventos harían falta ~24 × 19 ≈ **456 cuerdas**; para todo el cuadro, entre **361 y 817**.
- Por tanto, la reconstrucción de 43 cuerdas **no puede ser literal** si el quipu registraba los 19 eventos. Caben dos lecturas: (a) las 43 cuerdas guardaban **totales acumulados** por categoría y las 19 filas son la descomposición analística que el khipukamayuq podía narrar; o (b) el quipu físico tenía **≥361 cuerdas** (una por celda), organizadas en 12 grupos.
- La lectura (a) explica por qué el cuadro no tiene totales (los totales *eran* las cuerdas) y por qué el orden histórico se leía en voz alta. La lectura (b) explica la estructura del cuadro como matriz.

### 6.2 Predicción de forma (si se conservó)

Bajo (b), el quipu wanka sería:

- **12 grupos** de color, en el orden I–XII, cada grupo = una categoría (probablemente un color/familia por grupo, como en UR278, donde 23/28 filas son monocromas).
- **Uno o dos colgantes por evento dentro de cada grupo** (~19–38 por grupo), es decir, un «abanico» de ~19 cuerdas por grupo; total **361–817 cuerdas**, uno de los mayores del corpus (percentil >96 %).
- **Dos sub-series por categoría**: entregado vs rancheado, distinguibles por torsión (Z/S), dirección de fijación (recto/verso) o color; y una **cola final** (grupos X–XII) para lo que «sale» con la gente.
- Mayoría de valores de **4 dígitos** (35 de 361 valores son ≥10⁴; 3 son ≥10⁵), lo que exige cuerdas con 5–6 posiciones de nudos, raras en el corpus.

### 6.3 Búsqueda en el corpus

`05_corpus.py` calcula para los 651 quipus: n.º de cuerdas, n.º de grupos, mediana de colgantes por grupo, fracción de cuerdas numéricas, homogeneidad cromática de los grupos y n.º de colores. Filtré por la forma predicha (10–14 grupos, 180–500 cuerdas, 12–26 colgantes por grupo, ≥55 % numéricas):

- **0 de 651 quipus cumplen la forma predicha** (esperado por independencia: 0,6).
- **No hay ningún quipu con procedencia «Mantaro», «Jauja» o «Xauxa»** en el corpus (0 de 651; 235 son «Unknown»). La premisa geográfica de la búsqueda no se puede cumplir.
- El más parecido es **UR093** (procedencia desconocida, Museo Temple Radicati): **12 grupos**, mediana de **18 colgantes/grupo** (21, 3, 14, 18, 20, 39, 16, 18, 24, 16, 15, 19), 1227 cuerdas, pero solo **27,5 % numéricas** (una de cada cuatro cuerdas), 42 colores y nivel máximo 2. Es 2,5× más grande que el máximo predicho y casi no tiene valores: no es el quipu wanka, pero es el único con su «esqueleto» de 12 grupos y ~18 cuerdas por grupo.
- Otros candidatos con 11–13 grupos y ≥150 cuerdas: QU012 (13 grupos, 281 cuerdas, 76 % numéricas), AS026B (13 grupos de exactamente 10 cuerdas, 260), UR058B (12 grupos, 256), UR203 (12 grupos, 167), UR207 (11 grupos, 164). Ninguno tiene el fan de ~19 ni la escala de valores.
- Solo **23/651 (3,5 %)** tienen ≥361 cuerdas (la mediana del corpus es 43 cuerdas): aun en el escenario (b), el quipu wanka estaría en el 3,5 % superior por tamaño.

**Conclusión:** el corpus KFG **no contiene** un quipu con la forma predicha. Dado que el quipu wanka se presentó en Lima en 1561 y no se conoce su paradero, el resultado negativo es informativo: o se perdió, o el registro se materializó como **una serie de quipus pequeños** (uno por evento o por año, ~43 cuerdas cada uno), no como un quipu único de 361+ cuerdas. Esta segunda posibilidad es la que mejor concilia «43 cuerdas» con «361 números» y es testeable en el futuro buscando **conjuntos** de quipus de ~43 cuerdas y 12 grupos.

## 7. Controles y límites

- **Nulo explícito** en todas las pruebas: permutación de eventos dentro de cada macro-grupo (T1, T2), preservando marginales; 20 000 réplicas; semilla 20261018.
- **Corrección múltiple:** Holm sobre 5 pruebas (T1a, T1b, T2, T3, T6). Las cinco siguen siendo significativas.
- **Pseudorreplicación:** la unidad es el evento (19), no las 361 cantidades. El bootstrap de T6 se hace **por evento**, no por celda.
- **Duplicación `ll`≡`m`:** al eliminar la fila `m`, el co-movimiento baja a ρ = 0,38 (p = 2·10⁻⁴) y PC1 a 57 % (sigue por encima del nulo, 40 %). La conclusión no depende del duplicado, pero el tamaño del efecto sí se infla si se incluye.
- **Límite mayor:** la pérdida de coordenadas de columna impide cualquier prueba a nivel de categoría fina (p. ej., maíz vs quinua, entregado vs rancheado). Todo lo que se afirma arriba es a nivel de macro-grupo (6) o de evento (19).
- **Sumas brutas:** sumar hanegas, cargas, pares y personas no tiene sentido físico. Los totales se usan solo como **índice de volumen relativo** dentro de una misma macro-categoría y evento, nunca como magnitud absoluta.
- **Procedencia:** no se usa el museo como lugar de origen (regla del brief). UR093 es «Unknown».

## 8. Resultados negativos

1. **La regla de proporcionalidad por saya no es contrastable** con Murra (2024): el cuadro es de una sola saya y no hay población desagregada. La afirmación de LeVine no está respaldada por la tabla que dice resumir.
2. **No hay totales ni subtotales** en el registro wanka (a diferencia de Incahuasi): no se puede verificar la aritmética interna del quipu.
3. **Ningún quipu del corpus** tiene la forma predicha (0/651) ni procede del Mantaro/Jauja.
4. **La amplitud del registro no decae** con el tiempo (ρ = −0,01): la hipótesis de que las cuerdas de lo saqueado «se abandonan» tras 1533 no se sostiene; lo que decae es el volumen.
5. **La razón saqueado/entregado no es constante** ni siquiera en el evento mejor documentado (1533): va de 1,7 (maíz) a 105 (vestidos), un factor 60. No hay una «tasa de saqueo» única.
6. **El redondeo decimal** (19,7 %) impide usar las cantidades como reflejo directo de nudos: al menos una parte del redondeo es del escribano.

## 9. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| 12 categorías, 43 cuerdas, 19 eventos, orden constante, sin totales, sin eje saya | **Demostrado** (fuente primaria) |
| La regla de proporcionalidad por saya no es verificable con esta fuente | **Demostrado** |
| 43 cuerdas no pueden contener 361 números; el quipu físico requeriría 361–817 cuerdas o totales acumulados | **Demostrado** (aritmética) / **apoyado con datos** para la inferencia física |
| Existe un factor de escala por evento (co-movimiento + rango 1) | **Apoyado con datos** (p < 5·10⁻⁵, Holm) |
| Las cantidades decaen con el tiempo y la amplitud no | **Apoyado con datos** (sign test p = 0,031; ρ riqueza ≈ 0) |
| Wanka = taxonomía dispersa vs Incahuasi = partición igualitaria | **Apoyado con datos** (CV 1,96 vs 0,19) |
| Arquitectura de 12 grupos × ~19 cuerdas | **Propuesto** |
| Que el quipu wanka fuera un quipu único de 361+ cuerdas | **Propuesto** (alternativa: serie de quipus) |
| La regla de proporcionalidad como ley andina | **Especulativo** |

## 10. Para el coordinador

- **El «quipu de 43 cuerdas» no puede ser literal.** El cuadro tiene 361 números (44 % de una matriz 19×43); con una cuerda por número harían falta 361–817 cuerdas. La reconstrucción de 43 cuerdas solo funciona si cada cuerda era un **total acumulado** por categoría y los 19 eventos eran la narración. Es la contradicción estructural más importante del artículo y afecta a cualquier uso del «quipu wanka» como caso de estudio.
- **La regla «proporcional a la población de cada saya» no está en Murra y no es contrastable con Murra.** El cuadro es solo de Hatun Xauxa; no hay cifras de Lurin Wanka; la única demografía es ~27 000 unidades domésticas para toda la etnia; Murra dice que la estructura de las tres fratrías es desconocida. La frase es de LeVine (1992), no un resultado. No debe citarse como hallazgo.
- **Lo que sí muestra el registro:** un **factor de escala por evento**. Las 6 macro-categorías co-mueven (ρ = 0,57; p < 5·10⁻⁵), la matriz es casi de rango 1 (PC1 = 62 % vs 40 % del nulo) y los eventos grandes son grandes en todo. Eso es «proporcionalidad» en el sentido débil de canasta fija escalada, no en el sentido de cuotas por saya.
- **La estructura wanka es lo opuesto a Incahuasi.** 12 categorías taxonómicas × 19 eventos, sin totales, CV entre categorías 1,96; frente a 28 registros × 9 partes casi iguales, con totales de cabecera, CV 0,19. El único rasgo compartido es el **orden de columnas conservado** (en los 5 pares UR270–UR278, la identidad es la mejor de 9! = 1/362 880).
- **Predicción física:** 12 grupos de color, ~19 cuerdas por grupo (361–817 cuerdas), dos sub-series (entregado/rancheado) y valores de 4–6 dígitos. Sería uno de los mayores quipus conocidos (percentil >96 %).
- **Búsqueda en el corpus: 0/651 coincidencias.** No hay ningún quipu del Mantaro/Jauja/Xauxa en el KFG (0 de 651; 235 «Unknown»). El más parecido es **UR093** (12 grupos, mediana 18 cuerdas/grupo, 1227 cuerdas, solo 27,5 % numéricas): comparte el esqueleto, no la sustancia.
- **Hipótesis alternativa que concilia todo:** el registro se materializó como una **serie de quipus pequeños** (~43 cuerdas, uno por evento o año). Es testeable buscando conjuntos de quipus de ~43 cuerdas con 12 grupos y valores que sumen los totales del cuadro.
- **Corrección de fecha:** el cuadro termina en **1548** (Gasca), no en 1554; la declaración es de 1561. Los años explícitos son 8 de 19; el resto se ubica por secuencia.
- **Cautela con la fuente:** el OCR pierde las columnas y las filas `ll` y `m` están duplicadas en 3/6 páginas. Cualquier trabajo futuro sobre esta tabla debe partir del PDF, no del texto.
- **Siguiente paso recomendado:** conseguir el PDF o la transcripción de Espinoza Soriano (1971–72) para (a) recuperar la asignación celda-columna y (b) verificar si existe la declaración de Lurin Wanka con cifras comparables. Sin eso, la pregunta 2 queda cerrada como «no testeable», no como «cierta».
