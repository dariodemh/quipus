# UR113 (KH0349) — Lectura profunda de un quipu

**Procedencia:** Nazca (Museo de la Cultura del Mundo, Gotemburgo; nº 1931.37.0001; apodo «Valhalla»).
**Cordón principal:** 135 cm, color `AB-AB-BG-KB`.
**Tamaño:** 866 cuerdas, **332 colgantes**, **534 subsidiarias** (505 de nivel 1, 28 de nivel 2, 1 de nivel 3), 31 grupos.
**Scripts:** `01_estructura.py`, `02_aritmetica.py`, `03_calidad_nudos.py`, `04_corpus.py`, `05_color_nulos.py`, `06_localiza.py`, `07_bateria.py`, `08_decrecientes.py`, `09_color_lags.py`. Todos con semilla 0.

---

## 1. Pregunta

¿Qué estructura y qué aritmética internas tiene UR113, y qué tipo de registro es (censo, tributo, depósito, calendario, otro)? ¿Qué serían sus filas y columnas? ¿Qué no encaja?

## 2. Método y límites

- Unidad de análisis: **el quipu** para las comparaciones con el corpus; para las pruebas internas, **permutaciones dentro del quipu** (y dentro del grupo cuando la prueba es por grupo), nunca comparaciones entre cuerdas tratadas como independientes.
- Nulo explícito en cada prueba: se baraja el vector de valores (o de colores) conservando la estructura (qué cuerdas tienen subsidiarias, tamaños de grupo, multiconjunto de valores). 500–2000 remuestreos, semilla 0.
- Corrección de comparaciones múltiples: **Benjamini–Hochberg (FDR)** en las pruebas por grupo; se indica cuando una prueba es única y no requiere corrección.
- Filtro **anti-trivial**: se excluyen sumas de un solo sumando, sumas que sólo funcionan por ceros y objetivos < 3. Este filtro es decisivo (ver §4.2) y es la principal diferencia con los detectores automáticos del KFG.
- **Límite grave de los datos:** KFG y OKR son **la misma lectura** (866 cuerdas y 891 racimos de nudos en ambas fuentes; 1311 nudos sueltos en OKR; el registro procede de una única digitalización de 2005). No hay segunda lectura independiente, así que ningún resultado aritmético puede separar «aritmética real» de «error sistemático de transcripción». Además, el KFG anota que **los colgantes 1–24 (grupos 0–2) se montaron sobre tela y se cosieron al revés**, y que la fijación se leyó «a la inversa»: el `union` R/V de esos grupos no es fiable.
- No uso el museo como lugar de origen: la procedencia declarada es Nazca y no hay contexto arqueológico.

## 3. Estructura reconstruida

### 3.1 Esqueleto

| Nivel | Cuerdas | Qué son |
|---|---|---|
| 0 | 332 | colgantes (filas del registro) |
| 1 | 505 | subsidiarias de colgante |
| 2 | 28 | subsidiarias de subsidiaria |
| 3 | 1 | `p323s2s1s1` (138) |
| **total** | **866** | |

- **Grupos:** 31 (índices 0–30), entre 1 y 20 colgantes; mediana 12. Ocupan de 1 a 127 cm del cordón principal.
- **Jerarquía:** 167 colgantes tienen hijas (69 con 1, 14 con 2, 17 con 3, 16 con 4, 23 con 5, 7 con 6, 9 con 7, 7 con 8, 4 con 9, 1 con 10). Las 505 subsidiarias de nivel 1 cuelgan de esos 167 colgantes: **1,61 subsidiarias por colgante**, percentil 96 entre los quipus de ≥50 colgantes y **2.º del corpus en número absoluto de subsidiarias** (sólo UR093 tiene más).
- **Unión:** R = 330, V = 3 (`p4`, `p5`, `p133`), U = 533. **No hay ninguna unión T: el quipu no tiene cuerdas superiores.** Es un dato negativo importante: no hay totales explícitos de grupo.
- **Torsión:** S = 858, U = 8. **Terminación:** K = 796, B = 57, R = 7, sin dato = 6.
- **Colores:** 56 códigos distintos en el quipu; 24 en los colgantes. Dominantes: W 95, RB 83, AB 30, G0 18, KB 15, YB 12, W:KB 12, W:RB 12.
- **Valores:** suma de colgantes **9 146**; suma de todas las cuerdas 13 113. Colgante típico: mediana 8, media 27,5, máximo 620. 110 colgantes de 1 dígito, 132 de 2, 26 de 3.

### 3.2 Dos regímenes de grupo

Los 31 grupos no son homogéneos; se separan en dos familias nítidas:

| Régimen | Grupos | Rasgos |
|---|---|---|
| **A. Monocromo, sin desglose** | 2, 3, 10, 14, 15, 18, 19, 24, 26, 27, 29, 30 | todos los colgantes del mismo color; 0–5 subsidiarias; valores redondos o muy pequeños; **13 de 31 grupos (no todos monocromos) tienen ≥50 % de un solo valor**; 5 de ellos (0, 5, 14, 22 y 30) tienen un único valor no nulo |
| **B. Policromo, con desglose** | 4, 6, 8, 12, 13, 16, 20 | 4–6 colores; 3–8 subsidiarias por colgante; valores pequeños (4–70) que en parte **suman exactamente** |

Ejemplos:
- **Grupo 3** (18 colgantes, todos W, 4 subsidiarias): `220, 220, 220, 220, 220, 200, 200, 200, 200, 210, 11, 10, 10, 10, 620, 0, 0, 0`. Diez lotes de 200–220 más un resto y un 620 (=600+20). Total 2 771.
- **Grupo 6** (17 colgantes, 89 subsidiarias): `8, 5, 7, 11, 9, 12, 8, 7, 11, 12, 11, 9, 12, 15, 14, 10, 0`. Cada colgante lleva 4–7 subsidiarias de valor 1–4.
- **Grupo 4** (20 colgantes, 78 subsidiarias): `222, 218, 171, 179, 173, 135, 165, 88, 158, 17, 78, 143, 74, 98, 68, 67, 0, 0, 0, 0`. Aquí las subsidiarias **no** suman el colgante (error medio absoluto 74).

### 3.3 El final de los grupos: cuerdas sin nudo

143 cuerdas (16,5 %) no tienen ningún nudo; 64 son colgantes. La proporción es **normal en el corpus** (mediana 17,9 %; percentil 46), así que no es una anomalía de este quipu. Pero su distribución sí es llamativa: varias series **terminan en un bloque de 3–4 colgantes en blanco** (grupos 0, 3, 4, 5, 22, 26). No he encontrado una explicación mejor que «espacio dejado al final del bloque»; no hay evidencia de que sean ceros contables.

## 4. Aritmética interna

### 4.1 Colgante = suma de sus subsidiarias (la prueba fuerte)

Excluyendo madres con una sola hija y valores 0 (triviales): **17 de 95 colgantes con ≥2 hijas** cumplen la igualdad exacta (17,9 %). Nulo (barajar los valores de todas las subsidiarias, 500 permutaciones): media 1,67, máximo 8. **p = 0,002** (10× exceso).

Casos: `p71` 8 = 2+1+1+4; `p76` 12 = 1+1+1+3+2+1+3; `p190` 40 = 4+3+33; `p195` 30 = 4+4+1+0+21; `p196` 12 = 3+3+6; `p229` 60 = 13+47; `p230` 70 = 13+2+55.

Por grupo (nulo dentro del grupo, 2000 permutaciones, BH sobre 15 grupos):

| Grupo | Madres | Exactas | Esperado | p | q (BH) |
|---|---|---|---|---|---|
| 16 | 17 | 5 | 0,69 | 0,0005 | **0,0037** |
| 12 | 12 | 3 | 0,12 | 0,0005 | **0,0037** |
| 6 | 17 | 6 | 1,51 | 0,0025 | **0,0125** |
| 20 | 18 | 2 | 0,44 | 0,073 | 0,27 |
| resto | — | 0–2 | — | >0,15 | n.s. |

**Lectura:** hay una jerarquía aritmética real, pero **localizada en tres grupos** (6, 12, 16) y marginal en el 20. En los grupos 3, 4, 28 y 30 las subsidiarias **no** son un desglose del colgante (error medio 58–140).

### 4.2 Colgante = suma de una corrida contigua de colgantes previos (patrón Ascher)

Con el filtro anti-trivial: **8 casos de 218 cuerdas testables** (3,7 %); nulo 4,34 (máx. 11), **p = 0,09 → no significativo**. De esos 8, siete son corridas monocromas (`p133` 20 = 10+10; `p309` 4 = 2+2; `p329` 11 = 6+5; `p141` 110 = 20+20+10+60; y tres casos de 1+1+1, 2+1, 1+0+3). El «p = 0,005» de la versión monocroma es post-hoc sobre los mismos 8 casos y no lo considero evidencia.

**Contraste metodológico decisivo.** El KFG atribuye a UR113 **135 colgantes que son «suma de colgantes previos»** (`pendant_pendant_sum_relation.csv`, 41 % de los 332). Al reproducirlo, esas 135 filas son todas exactas, pero el detector busca **cualquier subconjunto** de hasta 66 colgantes previos (`num_summands` llega a 66). Repetí ese mismo detector: encuentra **124**; al barajar los valores **sigue encontrando 91,4 de media** (mín. 80, máx. 103). Es decir, **~74 % de las «sumas» del KFG son alcanzables por azar** con búsqueda de subconjuntos. El número del KFG no es evidencia de nada; la señal honesta es la de §4.1.

### 4.3 Totales de grupo y agregación

- **No hay cuerdas superiores** (T = 0), luego no hay totales de grupo registrados en el artefacto.
- Suma de colgantes = 9 146; no es un número redondo ni coincide con ningún valor del quipu.
- **No hay bipartición en mitades iguales:** el corte más cercano a la mitad (4 573) se desvía en 810 unidades (9 %); no hay ningún corte con desviación < 5 %.
- **Totales de grupo repetidos:** sólo dos pares (`g0 = g30 = 150`; `g15 = g25 = 35`). Nulo: 0,69 pares de media, **p = 0,15 → no significativo**. La simetría 150/150 entre el primer y el último grupo es sugestiva pero **no supera el azar**.
- Sumas de grupos consecutivos que igualan otro grupo: 2 casos, ambos triviales (22–24 = 51 = g7; 25–26 = 35 = g15).
- Razones constantes entre totales de grupo (×1,5, ×2, ×2,5, ×4, ×5): todas involucran números pequeños (7, 14, 20, 35, 100) y no hay ninguna serie; **negativo**.

### 4.4 Orden decreciente dentro de los grupos (hallazgo principal)

Dentro de cada grupo, los colgantes están **ordenados de mayor a menor** con mucha más frecuencia de la esperada. Test por grupo: Spearman entre posición y valor, nulo = permutar los valores **dentro de ese grupo** (conserva el multiconjunto; prueba sólo el orden).

- **10 de 23 grupos testables** con ρ ≤ −0,60 (grupos 1, 2, 3, 4, 9, 11, 13, 16, 17, 21). Nulo del quipu completo (permutación dentro de grupo, 1000 réplicas): **1,06 grupos de media, máximo 5, p = 0,001**.
- BH sobre los 23 grupos: **9 grupos con q < 0,05** (ρ de −0,59 a −0,94).
- Contexto de corpus (486 quipus con ≥3 grupos testables): UR113 tiene **43,5 % de grupos decrecientes** frente a una mediana del corpus de 0 % (media 14,7 %). En la tabla del propio KFG (`ascher_decreasing_cluster`), UR113 tiene **5 clusters decrecientes** frente a una media de 0,22 y un máximo de 6 en todo el corpus: **percentil 99,4**.
- **Control de la explicación aburrida:** ¿están ordenados por longitud física y no por valor? No. Correlación valor–largo en los colgantes = −0,09; en los grupos decrecientes el largo tiende a *crecer* (ρ = +0,4 a +0,6) mientras el valor decrece. El orden es numérico, no físico.
- Aviso: SINTESIS.md registra un negativo previo («exceso del primer colgante = orden decreciente, desaparece con control»). Mi prueba no es ésa: no mira el primer colgante sino la monotonicidad de todo el grupo, y el nulo conserva el multiconjunto de valores; por eso sobrevive.

## 5. Color

- **Grupos monocromos: 12 de 31** (11 de los 30 grupos con ≥2 cuerdas; el otro es el grupo 30, de una sola cuerda). Nulo barajando colores entre colgantes (tamaños de grupo fijos): 1,1 de media (máx. 3), **p = 0,001**. El color marca bloques, no es decorativo.
- **Concentración del valor modal por grupo:** suma de los conteos del valor más repetido en grupos de ≥4 cuerdas = 84; nulo 54,1 (máx. 65), **p = 0,001**. Hay «cantidades estándar» repetidas dentro del bloque (p. ej. los cinco 220 y los cuatro 200 del grupo 3).
- **Orden de color dentro de la lista de subsidiarias:** consistencia de un orden global inferido (pares de colores que aparecen juntos en una misma madre) = 0,775; nulo permutando el orden dentro de cada madre = 0,630 (máx. 0,674), **p = 0,005** (200 réplicas). Efecto real pero modesto: hay una tendencia a un orden canónico de colores (W/AB al principio, KB al final), no una regla estricta.
- **Color y magnitud:** Kruskal–Wallis del valor de las subsidiarias por color (7 colores con n ≥ 15): H = 32,1; nulo 6,05; p = 0,0005. Pero está confundido con la posición: el color «grande» (W, W-KB) es el que suele ocupar el lugar del desglose principal. **No lo uso como prueba semántica.**
- **Estructura de franjas:** la autocorrelación de color es fuerte en los lags 1 y 2 (0,69 y 0,61 de coincidencias frente a 0,46 y 0,45 del nulo intra-grupo; p = 0,003 en ambos) y desaparece en el lag 3 (0,47 vs 0,43; p = 0,08) y en el 4. Es **agrupamiento en franjas cortas de 2–3 cuerdas**, no periodicidad de alternancia regular.
- **Negativos de color:** (a) las subsidiarias **no** evitan el color de su madre (8,5 % de coincidencia observada frente a 9,5 % esperada por los márgenes); (b) **no** se cumple «un color distinto por subsidiaria» (diferencia observada −0,35 frente a −0,49 del nulo; p = 1,0); (c) no hay periodicidad de color en lags ≥3 más allá de las franjas cortas.

## 6. Propuesta de lectura

**Tipo de registro: cuenta administrativa jerárquica, con listas ordenadas por magnitud y subtotales locales. No es un calendario.**

- **Descartado (con datos):** calendario. No hay 30/31/365 elementos, ni periodicidad numérica, ni ciclos; los tamaños de grupo son 1–20 y los valores 0–620. Tampoco hay bipartición en mitades (§4.3), que es el patrón de UR28 (Nazca; totales repetidos de 102 en sus agrupaciones).
- **Descartado (con datos):** depósito/inventario de lotes homogéneos. Sólo el grupo 3 tiene cantidades redondas tipo lote (200/220); el resto son cantidades irregulares.
- **Mejor ajuste: padrón/censo o evaluación de tributo** — una lista de contribuyentes (o de unidades domésticas) agrupada en 31 bloques, **ordenada de mayor a menor dentro de cada bloque**, con el desglose de algunas filas en categorías de color y con subtotales exactos en tres bloques. Los valores 5–15 del grupo 6 (con 4–7 subsidiarias de 1–4 cada una) son compatibles con **tamaños de unidad doméstica desglosados por categoría**; los 200–220 del grupo 3, con **lotes o pachacas**.
- **Filas:** los 332 colgantes = 332 entradas (unidades domésticas, contribuyentes o lotes).
- **Columnas:** (1) bloque/grupo; (2) **posición = rango** (el valor decrece); (3) **color del colgante** = categoría o marca de bloque; (4) **valor** = cantidad; (5) **lista de subsidiarias** = desglose variable de (color, cantidad), no una tabla de columnas fijas.
- **Escala (especulativo):** 332 entradas en 31 bloques de ~12 es un tamaño plausible para un padrón de unidades domésticas de una parcialidad; los diez lotes de 200–220 del grupo 3 darían ~2 100 unidades, compatible con una *pachaca* grande o con un fondo de depósito. No hay forma de decidirlo con estos datos: el quipu no trae unidades ni etiquetas.

**Nivel de evidencia:**
- Estructura de 31 grupos, 332 colgantes, 534 subsidiarias, sin cuerdas superiores: **bien apoyado** (lectura directa).
- Suma exacta colgante = subsidiarias en 17 filas (p = 0,002; 3 grupos con q < 0,05): **apoyado con datos**.
- Orden decreciente dentro de grupos (p = 0,001; percentil 99 del corpus): **apoyado con datos**.
- Bloques monocromos y cantidades estándar repetidas (p = 0,001): **apoyado con datos**.
- «Lista de contribuyentes ordenada por magnitud» (censo/tributo): **propuesto**.
- Identificación de los colores con categorías concretas (sexo, edad, ayllu, hanan/urin): **especulativo**.

## 7. Lo que no encaja

1. **Grupo 4** es el caso más raro: 20 colgantes, 78 subsidiarias, valores 67–222, y las subsidiarias **no** reconstruyen el colgante (error medio 74). Si el resto del quipu usa «colgante = total», el grupo 4 usa otra convención (¿el colgante es una etiqueta y las subsidiarias las cantidades?).
2. **Profundidad 3:** `p323s2s1s1` = 138 (100+30+8), hija de `p323s2s1` = 178 (100+70+8). Es la única cuerda de nivel 3 y tiene valores de 3 dígitos, algo que no aparece en el resto de las subsidiarias (máx. 178). Parece una fila mal anidada o un desglose de un desglose.
3. **`p39` = 620** (600+20, racimo de 6 nudos en el lugar de las centenas): es el único valor > 300 y rompe la escala del grupo 3 (200–220). Podría ser 220+200+200 = 620 (suma de tres colgantes del mismo grupo), pero no es contiguo.
4. **Tres uniones V** (`p4`, `p5`, `p133`) frente a 330 R. `p4` y `p5` no tienen nudos; `p133` vale 20. Con sólo 3 casos no se puede probar nada, y además los grupos 0–2 están re-montados y su unión se leyó al revés (nota KFG).
5. **8 cuerdas con torsión U**, de las cuales **6 tienen largo 0 y terminación B** (`p50s4`, `p51s5`, `p107s4`, `p199s5`, `p240s6`, `p243s5`): son muñones/roturas, no cuerdas legibles.
6. **36 racimos se apartan de la convención dominante** (4,0 % de 891): 14 nudos simples en S, 11 figuras de ocho en S, 7 nudos largos en Z y 4 del tipo indeterminado. Entre los 865 racimos con tipo definido (E, L, S) son 32 (3,7 %). La dirección está determinada por el tipo de nudo (L→S, E→Z, S→Z) en el 96,4 % de los casos: **no hay un código binario independiente en la dirección**, y las excepciones son compatibles con errores de lectura.
7. **Anomalías físicas anotadas por el KFG:** `p33` con un lazo tipo dogal entre 16,5 y 17,5 cm; `p69` hallado suelto en el fardo, sin fijación; `p88` parcheado en dos puntos; `p22` y `p163s8` cosidos con hilo moderno; `p292–295` frágiles y reconstruidos. Todas degradan la confianza en esas filas.
8. **Información no numérica.** Los candidatos son: el color (56 códigos, con bloques monocromos y un orden canónico débil), la unión R/V (3 V), el lazo de `p33` y los 143 blancos. El color es el único canal con estructura estadística propia; **no hay evidencia** de que los nudos codifiquen algo distinto de números decimales.

## 8. Resultados negativos (explícitos)

- **No hay cuerdas superiores** (T = 0): ningún total de grupo registrado.
- **No hay suma de colgantes contiguos** más allá del azar (p = 0,09 con filtro anti-trivial).
- **Las 135 «sumas» del KFG son un artefacto** de búsqueda de subconjuntos (91,4 de media en datos barajados).
- **No hay bipartición en mitades** (desviación mínima 810 unidades, 9 %).
- **No hay totales de grupo repetidos** significativos (p = 0,15), ni razones constantes, ni progresión.
- **No hay calendario**: ni 30/31/365, ni periodicidad numérica, ni grupos de tamaño regular.
- **No hay código en la dirección del nudo**: está determinada por el tipo (96,4 %).
- **UR113 no es copia de otro quipu**: la concordancia con UR271 es débil y el par UR113→UR264 es un artefacto (informes 04 y 14); no se sostiene.
- **El color de la subsidiaria no se opone ni se alinea con el de la madre** (8,5 % vs 9,5 % esperado).

## 9. Niveles de evidencia (resumen)

| Afirmación | Nivel |
|---|---|
| 31 grupos, 332 colgantes, 534 subsidiarias, sin T, torsión S | bien apoyado |
| Decimal posicional y dirección determinada por tipo de nudo | bien apoyado |
| 17 colgantes = suma exacta de sus subsidiarias (p = 0,002; 3 grupos q < 0,05) | apoyado con datos |
| 10/23 grupos ordenados de mayor a menor (p = 0,001; percentil 99,4 del corpus) | apoyado con datos |
| 12/31 grupos monocromos y cantidades estándar repetidas (p = 0,001) | apoyado con datos |
| Dos regímenes de grupo (monocromo/sin desglose vs policromo/con desglose) | apoyado con datos |
| Es un padrón/censo o evaluación de tributo con filas ordenadas por magnitud | propuesto |
| Los colores son categorías (sexo/edad/ayllu) y los grupos son ayllus o mitades | especulativo |

## 10. Para el coordinador

- **UR113 es el 5.º quipu más grande del corpus** (866 cuerdas), 11.º en colgantes (332) y **2.º en subsidiarias (534)**: es un registro de agregación, no una lista corta.
- **Tiene aritmética interna real pero escasa y localizada:** 17 de 95 colgantes con ≥2 hijas son la suma exacta de su desglose (17,9 % frente a 1,7 esperado; p = 0,002), concentrados en los grupos 6, 12 y 16 (q BH = 0,004; 0,004; 0,013).
- **El hallazgo más fuerte y nuevo es el orden:** 10 de 23 grupos están ordenados de mayor a menor (ρ ≤ −0,6; p = 0,001; 9 grupos con q < 0,05). Es el **percentil 99,4 del corpus** en clusters decrecientes del KFG (5 frente a media 0,22). No lo explica la longitud de las cuerdas (ρ valor–largo = −0,09).
- **Cuidado con el KFG:** sus «135 colgantes que son suma de otros» son un artefacto de búsqueda de subconjuntos (el detector sigue encontrando 91 de media con los valores barajados). No citar esa cifra.
- **No hay cuerdas superiores ni totales de grupo** (T = 0) y **no hay bipartición en mitades** (el mejor corte se desvía un 9 %): no replica el esquema de totales repetidos de UR28 (Nazca), así que la lectura «seis ayllus en dos mitades» no se puede trasladar.
- **Sí hay estructura de bloques:** 12 de 31 grupos son monocromos (p = 0,001) y 13 grupos tienen ≥50 % de un mismo valor (p = 0,001); el color marca bloques, no decora.
- **Dos regímenes:** grupos monocromos con valores redondos y sin desglose (3, 10, 27…) frente a grupos policromos con 4–8 subsidiarias por colgante y valores pequeños (6, 8, 12, 16, 20). El grupo 4 es la excepción: tiene desglose pero **no** suma (error medio 74).
- **Lectura más probable (propuesto):** padrón/censo o evaluación de tributo; filas = 332 unidades domésticas/contribuyentes; columnas = bloque, rango (valor decreciente), color (categoría) y desglose variable. **No es calendario** ni inventario de lotes homogéneos.
- **Siguiente ronda recomendada:** (1) buscar el patrón «grupo ordenado + subtotal exacto» en los otros quipus grandes con muchas subsidiarias (UR093, KH0083, UR262, UR003) con el mismo nulo, para ver si es un género; (2) comprobar si los grupos decrecientes de UR113 tienen equivalentes en quipus de la misma procedencia (Nazca: UR028, UR119, UR166); (3) auditar el grupo 4 y la cuerda de nivel 3 contra las fotos del museo, porque son los dos puntos donde la lectura actual puede estar mal.
