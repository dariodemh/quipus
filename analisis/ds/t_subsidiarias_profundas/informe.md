# Árboles de subsidiarias profundos (nivel ≥ 3, hasta 15)

**Equipo:** análisis estructural de subsidiarias · **Fecha:** 2026-10-17
**Datos:** `analisis/datos/cuerdas.csv` (KFG; 57 818 cuerdas, 651 quipus)
**Scripts:** `01_estructura.py`, `03_sumas.py`, `04_nulo_ramificacion.py`,
`05_extremos.py`, `06_contexto.py`, `07_confusores.py`, `08_control_okr.py`,
`09_formas_tipos.py`, `10_resumen.py` (todos en esta carpeta).
**Salidas:** `arboles.csv`, `forma_arboles.csv`, `forma_quipus.csv`, `sumas_por_quipu.csv`,
`sumas_stats.json`, `resumen_quipus.csv`, `control_okr.csv`, `extremos.txt`, `casos10.csv`.

---

## 1. Pregunta

¿En qué quipus aparecen estructuras de subsidiarias de nivel ≥ 3 (hasta el nivel 15 que
existe en el corpus)? ¿Son sumas jerárquicas, listas de detalle, u otra cosa (genealogías,
desgloses, cadenas de copia)? ¿Su forma se distingue de la que produce una ramificación
aleatoria? Se describen los 10 casos más extremos cuerda por cuerda.

## 2. Método

**Unidad de análisis.** El quipu. Cuando se prueba a nivel de cuerda o de árbol, se usan
permutaciones dentro de cada quipu o se agrega por quipu; nunca se comparan cuerdas de
quipus distintos como si fueran independientes.

**Construcción del árbol.** Cada cuerda colgante (nivel 0) con todos sus descendientes por
el campo `padre`. Un árbol es "profundo" si su altura ≥ 3, es decir, si contiene al menos
una cuerda de nivel ≥ 3. No se impuso ningún filtro de tamaño ni de valores.

**Valores.** `valor = 0` con `nudos` vacío se trata como ausente (NaN), no como cero. Esto
es importante: en los niveles profundos hay muchas cuerdas sin nudos, y contarlas como
ceros inflaría artificialmente las sumas triviales.

**Sumas jerárquicas.** Se probó `valor(padre) = Σ valor(hijos)` con tolerancia 1e-6, solo
en nodos con ≥ 2 hijos y todos los valores presentes. Se probaron además: (a) padre = suma
de un subconjunto propio de hijos de tamaño ≥ 2 (excluyendo el caso trivial "un hijo copia
el valor del padre"); (b) un hijo = suma de los demás hermanos (solo con ≥ 3 hijos);
(c) padre = suma de todas las hojas de su subárbol. El nulo es una permutación de los
valores observados dentro de cada quipu (preserva el patrón de valores ausentes, la
estructura del árbol y la multiplicidad de valores); 2 000 permutaciones para el test
principal y 500–1 000 para los alternativos, semilla fija.

**Forma frente a ramificación aleatoria.** Dos nulos:
- **Nulo A (conservador):** se conserva exactamente la secuencia de grados de salida
  (número de hijos de cada nodo) y se aleatoriza a qué nodo cuelga cada hijo. Conserva n,
  el número de hijos y la "forma de grados"; solo cambia el emparejamiento.
- **Nulo B:** árbol recursivo aleatorio (cada nodo nuevo se cuelga de un nodo previo
  uniforme). Conserva solo n.
Se comparan altura máxima y número de cuerdas en nivel ≥ 3. El test válido a nivel de
quipu es Poisson-binomial: para cada árbol con n ≥ 4 se estima P(altura ≥ 3 | sus grados)
con 200–400 simulaciones y se compara el número observado de árboles profundos con el
esperado. Corrección por comparaciones múltiples: Benjamini–Hochberg (BH-FDR).

**Controles de calidad.** Contraste KFG vs OKR (khipu.db) para los 46 quipus; comparación
de conteos por nivel. Modelos logístico y de Poisson para tamaño y procedencia.

## 3. Resultados

### 3.1. Cobertura y concentración

- **397 cuerdas** del corpus están en nivel ≥ 3 (0,69 % de 57 818); el máximo es el nivel
  15. La distribución por nivel es: 296 en nivel 3, 40 en 4, 15 en 5, y una cola de 1–9
  cuerdas por nivel hasta 15 (el nivel 15 tiene 8 cuerdas, todas de HP038).
- Esas 397 cuerdas pertenecen a **46 de los 651 quipus (7,1 %)**. Forman **153 árboles
  profundos** (altura ≥ 3), que suman **1 409 cuerdas (2,4 % del corpus)**; 0,37 % de los
  41 714 colgantes.
- Alturas: 121 árboles de altura 3, 27 de altura 4, 4 de altura 5 y **1 de altura 15**
  (HP038).
- La distribución está muy concentrada: los cinco quipus con más cuerdas en árboles
  profundos (KH0083 447, UR262 134, UR280 128, UR058B 71, HP038 66) reúnen 846/1 409 =
  **60 %**. KH0083 solo aporta 40 árboles y 447 cuerdas (76 % de sus propias cuerdas).

**Tabla 1. Quipus con más estructura profunda** (lista completa de los 46 en
`resumen_quipus.csv`).

| Quipu | Árboles | Cuerdas en árboles | Altura máx. | Cuerdas totales en nivel ≥3 | % de sus cuerdas | Procedencia | OKR |
|---|---:|---:|---:|---:|---:|---|---|
| KH0083 | 40 | 447 | 5 | 108 | 76,4 | Mollepampa | corrobora |
| UR262 | 20 | 134 | 5 | 54 | 27,3 | Incahuasi | ausente |
| UR280 | 13 | 128 | 4 | 20 | 52,0 | Incahuasi | ausente |
| UR058B | 4 | 71 | 3 | 10 | 27,7 | Unknown | ausente |
| HP038 | 1 | 66 | **15** | 63 | 25,7 | Unknown (MNAAHP) | ausente |
| UR003 | 6 | 54 | 4 | 8 | 7,1 | Leymebamba | ausente |
| KH0197 | 5 | 52 | 4 | 29 | 34,9 | Unknown (Berlín) | **discrepa** |
| UR096 | 1 | 39 | 3 | 2 | 68,4 | Unknown | ausente |
| UR058A | 3 | 33 | 3 | 3 | 12,0 | Unknown | ausente |
| UR270 | 5 | 32 | 4 | 11 | 8,4 | Incahuasi | ausente |
| UR165 | 4 | 30 | 3 | 6 | 13,3 | La Molina | ausente |
| UR271 | 5 | 25 | 3 | 10 | 27,2 | Incahuasi | ausente |

Lista completa de los 46 (árboles/cuerdas): KH0083 (40/447), UR262 (20/134), UR280
(13/128), UR058B (4/71), HP038 (1/66), UR003 (6/54), KH0197 (5/52), UR096 (1/39), UR058A
(3/33), UR270 (5/32), UR165 (4/30), UR271 (5/25), JC010 (3/18), AS071 (1/18), MM019
(2/17), UR1175 (4/17), UR097 (1/16), UR253 (1/15), UR267B (1/14), UR146 (1/14), UR049
(3/13), UR215 (2/11), UR272 (2/10), HP054 (1/9), HP004 (1/9), HP045 (1/8), UR216 (1/8),
UR193 (2/8), KH0001 (2/8), AS029 (1/8), AS172 (1/6), UR094 (1/6), UR1095 (1/5), UR268
(1/5), UR277 (1/5), JC023 (1/5), HP046_B (1/5), KH0057 (1/5), UR034 (1/5), UR113 (1/5),
UR266 (1/5), AS036 (1/4), AS042 (1/4), JC011 (1/4), UR1040 (1/4), UR120 (1/4).

**El tamaño manda.** Los quipus con estructura profunda tienen mediana de 172 cuerdas
frente a 39 en el resto (Mann–Whitney p = 2,5 × 10⁻¹⁴). Un logit `profundo ~ ln(cuerdas)`
da **OR = 2,18 por cada duplicación del tamaño** (p = 6,7 × 10⁻¹²). Es la explicación
aburrida principal: cuanto más grande el quipu, más oportunidades de que una cadena de
subsidiarias llegue al nivel 3.

**Incahuasi.** Tras ajustar por tamaño, los quipus de Incahuasi siguen teniendo más
estructura profunda: 12/52 (23,1 %) frente a 34/599 (5,7 %); OR ajustada 4,88
(IC 95 % 2,14–11,13), p = 0,0002; dentro de los quipus de ≥ 100 cuerdas, 10/19 (52,6 %)
frente a 21/141 (14,9 %), Fisher OR = 6,35, p = 0,0005. **Pero** Incahuasi también tiene
una intensidad de registro algo mayor (1,26 cuerdas por colgante y 21,6 % de colgantes con
subsidiarias, frente a 1,12–1,16 y 11,7–15,1 % en los demás grupos). No se puede separar
"práctica antigua" de "convención de excavación/registro" con estos datos.

### 3.2. ¿Sumas jerárquicas? No en los árboles profundos

**Control positivo (el test funciona).** En todo el corpus, entre los 1 389 nodos
padre-hijo comparables (≥ 2 hijos, todos con valor), **57 cumplen exactamente**
`padre = Σ hijos` (4,10 %), frente a **24,7 esperados** por el nulo de permutación
(1,78 %); p = 0,0005. El exceso es real y está concentrado: **UR113** aporta 15/52
(28,8 %; binomial p = 1,4 × 10⁻¹⁴; BH = 3,1 × 10⁻¹²) y **UR169** 4/20 (p = 3,9 × 10⁻⁴;
BH = 0,043). De 221 quipus con algún test, solo esos 2 sobreviven a BH. Es decir, la suma
jerárquica padre = hijos existe, pero es un fenómeno localizado, no una propiedad general.

**En los árboles profundos no aparece.** Solo **1 de 73** nodos comparables cumple la suma
exacta (1,4 %), frente a 0,87 esperados por el nulo; **p = 0,60**. El único caso es
HP004 `p1s3 = 44 = 20 + 24`, que está en el nivel 1 del árbol, no en los niveles hondos.
Restringiendo a nivel ≥ 3: **0/26** (nulo 0,0; p = 1,0). De los 153 árboles, 95 no tienen
ningún nodo comparable (cadenas sin ramificación con valores), así que el test se apoya en
58 árboles.

**Otras relaciones tampoco.** Padre = subconjunto propio de ≥ 2 hijos: 2/25 (8,0 %) frente
a 1,54 esperados (6,2 %), p = 0,46; a nivel de quipu, 2 quipus con ≥ 1 acierto frente a
1,43 esperados, p = 0,43. Un hijo = suma de los demás: 1/73 frente a 0,34, p = 0,30.
Padre = suma de todas las hojas del subárbol: 25/485 (5,2 %) frente a 6,7 esperados
(1,4 %), p = 0,005 en el conjunto, **pero 24 de los 25 casos son colgantes de nivel 0**
(en árboles poco profundos, sobre todo pares de dos hojas); dentro de los árboles profundos
es **1/119 (0,8 %)**, indistinguible del azar.

**Conclusión de esta sección:** los árboles profundos **no son sumas jerárquicas**. La
suma padre = hijos es un fenómeno de los niveles 0–1 de ciertos quipus (UR113, UR169),
no de las estructuras profundas.

### 3.3. ¿Listas de detalle? Parcialmente, y con un matiz importante

**Los valores existen en todos los niveles.** En los árboles profundos, la fracción de
cuerdas con valor es 71,9 % en nivel 0, 63,9 % en 1, 71,2 % en 2, 77,7 % en 3, 82,5 % en 4
y 60 % en 5. No son cuerdas vacías: los niveles hondos registran números.

**Las cuerdas se acortan con la profundidad** (mediana 37 cm en nivel 0, 33,5 en 1, 31 en
2, 28,5 en 3, 26,5 en 4, 25 en 5), consistente con un escalonamiento físico de ataduras.

**Pero la relación de magnitud cambia con la profundidad.** En todo el corpus, la fracción
de aristas en que el hijo es menor que la madre es 74,2 % en nivel 1 (razón mediana 0,28),
60,1 % en nivel 2 (0,51) y 56,6 % en nivel ≥ 3 (0,67). En los árboles profundos, 57,6 % de
las aristas con valores tienen hijo < madre (razón mediana 0,66), frente a 46,3 % del nulo
(p = 0,002). Es decir: **en el nivel 1 la subsidiaria es claramente una parte pequeña del
total; en los niveles 3–5 el valor es casi del mismo orden que el de la madre**. Eso es más
compatible con "continuación/etiqueta" que con "desglose aritmético".

**Duplicación de valores.** El 12,9 % de las aristas internas de los árboles profundos
tiene el mismo valor en madre e hijo, frente a 7,6 % del nulo (p = 0,001). La tasa sube con
la profundidad: 7,7 % en nivel 1, 16,0 % en nivel 2, 17,5 % en nivel 3. En 16 de 127
árboles con aristas comparables, ≥ 50 % de las aristas son duplicaciones; **UR271 tiene
5/5 árboles al 100 %** (cadenas 220→220→220→220, 200→200→…, 150→150→…). Es un fenómeno
distinto de la suma: la misma cantidad se repite hacia abajo.

**Color.** En los 259 nodos con ≥ 2 hijos coloreados, la fracción media de colores
distintos es 0,658, frente a 0,684 del nulo de permutación de colores dentro del quipu;
**no hay exceso de diversidad** (p = 0,99; de hecho es ligeramente menor). La probabilidad
de que madre e hijo compartan la familia de color es 44,6 %, frente a 38,9 % del nulo
(p = 0,002): hay una leve tendencia a que la subsidiaria herede el color de la madre, pero
no una "codificación por color" fuerte de las ramas.

**Tipología de forma** (regla explícita en `09_formas_tipos.py`):

| Tipo | n | Cuerdas medias | Altura media | n en nivel ≥3 (media) | Cadena |
|---|---:|---:|---:|---:|---:|
| Cadena con ramas | 88 (57,5 %) | 6,9 | 3,0 | 1,4 | 0,71 |
| Cadena larga | 31 (20,3 %) | 12,6 | 4,5 | 6,4 | 0,58 |
| Árbol ramificado | 27 (17,6 %) | 10,1 | 3,0 | 2,3 | 0,30 |
| Abanico ancho | 7 (4,6 %) | 19,7 | 3,0 | 2,4 | 0,41 |

El árbol profundo modal **no es una jerarquía equilibrada: es una espina** (muchos nodos
con un solo hijo) con ramificaciones laterales. Eso explica por qué hay tantos niveles con
pocas cuerdas.

### 3.4. Forma frente a nulos de ramificación aleatoria

- **Nulo A (grados conservados):** la altura media observada de los 153 árboles profundos
  es 3,31; la del nulo A es 2,28. La diferencia es modesta y solo el **1 %** de los árboles
  individuales tiene p < 0,05 (HP038 p = 0,0025; UR262/p80 p = 0,042). Excluyendo HP038,
  la altura media observada baja a 3,23 y el nulo A sigue en 2,28.
- **Nulo B (árbol recursivo aleatorio):** la altura media del nulo B es 3,23, casi
  idéntica a la observada (3,31; 3,21 sin HP038). Es decir, **la profundidad típica de
  estos árboles no es extraordinaria**: un árbol aleatorio del mismo tamaño también llega a
  nivel 3. Lo extraordinario es la *cantidad* de árboles profundos y unos pocos casos
  concretos.
- **Test válido por quipu:** se observan **153 árboles profundos** donde el nulo A predice
  **78,0**. Siete quipus sobreviven a BH: UR262 (20 vs 5,8; p = 7,1 × 10⁻¹⁰; BH =
  3,2 × 10⁻⁸), KH0083 (40 vs 24,3; p = 1,0 × 10⁻⁸; BH = 2,3 × 10⁻⁷), UR270 (5 vs 1,1;
  p = 4,3 × 10⁻⁴; BH = 0,0066), UR271 (5 vs 1,1; p = 5,7 × 10⁻⁴; BH = 0,0066), UR280
  (13 vs 7,1; p = 0,0019; BH = 0,018), KH0197 (5 vs 1,9; p = 0,0067; BH = 0,045),
  UR1175 (4 vs 1,2; p = 0,0068; BH = 0,045). El resto (39 quipus) no se distingue del
  nulo.
- **HP038 es el único caso individual extremo**: 15 niveles, 66 cuerdas, p = 0,0025
  frente a ambos nulos (nulo A: altura media 1,71, percentil 95 = 6; nulo B: 7,53,
  percentil 95 = 10).

**Lectura:** la ramificación aleatoria explica la forma de casi todos los árboles; lo que
no explica es que haya 153 en vez de 78, y sobre todo HP038. La señal está en la
**concentración** (pocos quipus con muchas estructuras), no en una profundidad
individualmente imposible.

### 3.5. Los 10 casos más extremos, cuerda por cuerda

Criterio de selección: mayor número de cuerdas en nivel ≥ 3, desempate por número de
cuerdas del árbol, **una estructura por quipu** (para no repetir los 40 árboles de KH0083).
El detalle completo, con colores, largos, uniones y nudos, está en `extremos.txt`.

**1. HP038 / p8 — 66 cuerdas, altura 15, 63 en nivel ≥ 3 (el caso único).**
`p8(1) → s1(∅) → s1(∅) → [8 hijos, el 8.º continúa] → s1(∅) → [8 hijos, el 8.º continúa]
→ …` hasta el nivel 15. En cada nivel hay una "madre" solitaria seguida de un abanico de
8 cuerdas blancas (9 en el nivel 9); la cadena sigue siempre por la última. Las 7 madres de la cadena tienen
largos **exactamente iguales** a los colgantes p2–p8 del mismo quipu (40, 42, 38, 39, 8,
28, 29 cm, en ese orden) y colores que coinciden en 5/7 (los otros 2 son variantes de
marrón: MB/BG). Los valores son casi todos ausentes; donde hay, son 1, 2, 3, 10. **No es
una suma ni un desglose: es una copia recursiva de la secuencia de colgantes**, metida
dentro del 8.º hijo del 8.º hijo… Es el único árbol con p < 0,01 frente a ambos nulos.
No está en OKR. La explicación aburrida —duplicación en la transcripción de KFG— es
posible; la estructura está en el xlsx original, no solo en el CSV.

**2. KH0083 / p17 — 19 cuerdas, altura 4, 10 en nivel ≥ 3.**
`p17(15) → s1(55) → s1(∅) → {s1(∅) → 44; s2(563)}; s2(∅) → {s1(140), s2(4), s3(∅) → 5,
s4(10), s5(8)}; s3(18)`. El nivel 3 tiene 8 cuerdas con **8 colores distintos**; los
valores son heterogéneos (44, 563, 140, 4, 10, 8, 5, 18, 3) y no suman. Es el prototipo de
"desglose por categorías": ramas con colores propios y conteos independientes, sin total
en la madre. 15 colores distintos en 19 cuerdas.

**3. UR267B / p52 — 14 cuerdas, altura 4, 7 en nivel ≥ 3.**
`p52(∅) → s1(1) → {s1(∅), s2(4), s3(1), s4(1) → s1(1), s5(1) → s1(1) → s1(∅), s2(5),
s3(∅), s4(5), s5(∅)}`. Casi todos los valores son 1, 4 o 5; 62 % de las aristas internas
duplican el valor de la madre. Es una cadena de conteo de unidades, no una suma.

**4. KH0197 / p3 — 10 cuerdas, altura 4, 6 en nivel ≥ 3.**
`p3(533) → s1(9) → s1(10) → {s1(2) → s1(2), s2(10), s3(1), s4(1), s5(1)}; s2(6)`. Una
plantilla muy parecida (misma forma 1→1→1→5→1, con 5 hijos de colores W, YB, RL, GL y una
variante de marrón) se repite en p3, p5, p7, p9 y p11, con valores distintos. **Pero OKR
solo registra 35 cuerdas para KH0197 (niveles 1–2) frente a 149 en KFG (nivel 4); el quipu
figura como incompleto (COMPLETE = 0).** Este caso no está corroborado y podría ser una
transcripción/duplicación de KFG.

**5. UR262 / p80 — 10 cuerdas, altura 5, 6 en nivel ≥ 3.**
`p80(224) → s1(2211) → {s1(56), s2(40) → s1(98) → s1(40) → {s1(∅), s2(53), s3(20),
s4(11)}}`. Números grandes (2211 = 2000 + 200 + 10 + 1), todos distintos, ningún total.
Es uno de los cuatro árboles de altura 5 del corpus y el único de Incahuasi; es también el
único árbol de UR262 con p < 0,05 frente al nulo A (p = 0,042).

**6. UR280 / p7 — 16 cuerdas, altura 4, 5 en nivel ≥ 3.**
`p7(188) → {s1(∅), s2(12) → s1(14) → {s1(22), s2(5), s3(36), s4(3) → s1(2)}, s3(164) →
s1(3), s4(63) → s1(2), s5(20) → s1(72), s6(∅)}`. La madre 188 no es la suma de sus hijos
(12 + 164 + 63 + 20 = 259); el hijo 12 tampoco es la suma de 22 + 5 + 36 + 3. Los valores
del nivel 3 (22, 5, 36, 3) son del mismo orden que el padre 14: no hay reducción
aritmética.

**7. AS071 / p16 — 18 cuerdas, altura 3, 4 en nivel ≥ 3.**
`p16(11) → {s1(4), s2(1) → s1(∅) → {4 hijos de 1}, s2(1), s3(3), s3(1) → {s1(1), s2(1)},
s4(1), s5(4), s6(4), s7(1), s8(2)}`. Abanico ancho: 8 hijos en nivel 1, con 8 colores
distintos; el nivel 3 son cuatro cuerdas de valor 1. Es el caso más "plano" de la lista.

**8. UR058B / p7 — 15 cuerdas, altura 3, 4 en nivel ≥ 3.**
`p7(21) → {s1(∅) → s1(1) → {s1(2), s2(30), s3(10)}, s2(1), s3(70) → s1(20), s4(60),
s5(∅) → s1(1) → s1(1), s6(20), s7(40)}`. Los hijos de nivel 1 son 1, 70, 60, 20, 40: no
suman 21; el nivel 3 vuelve a valores pequeños (2, 30, 10).

**9. UR146 / p37 — 14 cuerdas, altura 3, 4 en nivel ≥ 3.**
`p37(∅) → s1(∅) → {s1(∅) → s1(∅), s2(3) → s1(∅), s3(5) → s1(∅), s4(10) → s1(∅),
s5(12), s6(∅), s7(∅), s8(3)}`. Las cuatro cuerdas de nivel 3 miden 1,5–4,5 cm y están
vacías: son **cáscaras estructurales**, no datos. Este es el caso que mejor ilustra el
polo "artefacto de atadura": la profundidad existe, pero no codifica nada numérico.

**10. UR270 / p101 — 9 cuerdas, altura 4, 4 en nivel ≥ 3.**
`p101(∅) → s1(93) → {s1(12), s2(∅), s3(8) → {s1(13), s2(∅), s3(31) → s1(63)}}`. Los
valores **crecen hacia abajo**: 8 → 13/31 → 63. Es el patrón inverso al de una suma
jerárquica (el nivel 4 es 63, el nivel 2 es 8); no hay ningún total.

**Caso especial (fuera del top 10 por tamaño): UR271 / p1–p5 — cinco árboles idénticos.**
Cada uno es `p(220) → s1(220) → s1(220) → {s1(220), s2(220)}` (y análogos con 200 y 150).
El mismo número se repite en todos los niveles y en las dos hojas; 100 % de duplicación.
No es una suma: es una **cadena de réplica**. Es el mejor contraejemplo a "todo árbol
profundo es un desglose".

### 3.6. Controles, resultados negativos y explicaciones aburridas

**Controles que pasaron:**
- El test de suma detecta el fenómeno donde existe: UR113 (15/52, BH = 3 × 10⁻¹²) y
  UR169 (4/20, BH = 0,043). Que en los árboles profundos dé 1/73 no es falta de potencia
  del test, es ausencia del fenómeno.
- El nulo de grados conservados es conservador: mantiene el número de hijos de cada nodo y
  el tamaño; aun así, el 1 % de los árboles individuales y 7 quipus se salen.
- El nulo de color permuta colores dentro del quipu, preservando la paleta local; el
  resultado (sin exceso de diversidad) no es un artefacto de comparar quipus distintos.

**Resultados negativos:**
- **No hay suma jerárquica en los niveles profundos:** 0/26 en nivel ≥ 3; 1/73 en todo el
  árbol (y ese 1 está en nivel 1).
- **No hay suma de subconjuntos ni de hermanos:** 2/25 y 1/73, ambos compatibles con el
  nulo (p = 0,46 y 0,30); a nivel de quipu, p = 0,43.
- **No hay exceso de diversidad de color entre hermanos:** 0,658 vs 0,684 (p = 0,99).
- **La profundidad típica no es extraordinaria:** el nulo recursivo aleatorio produce 3,23
  niveles de media, casi lo mismo que los 3,31 observados.
- **No hay señal de "genealogía" propiamente dicha:** no hay etiquetas ni valores
  cualitativos; todos los niveles tienen números o están vacíos. Lo que se observa es
  compatible con desgloses numéricos y cadenas de attachment, no con nombres.
- **42 de los 46 quipus no están en OKR**, así que la estructura profunda no se puede
  verificar con una segunda transcripción.
- **KH0197 discrepa:** KFG 149 cuerdas/nivel 4 vs OKR 35/nivel 1. Es el único caso con
  desacuerdo fuerte entre fuentes; sus 5 árboles profundos (y la plantilla repetida
  p3/p5/p7/p9/p11) deben tratarse como no verificados.

**Otras explicaciones aburridas consideradas:**
- *Tamaño del quipu:* explica gran parte (OR 2,18 por duplicación), pero no todo (Incahuasi
  OR 4,9 ajustada).
- *Intensidad de registro:* Incahuasi tiene más cuerdas por colgante y más colgantes con
  subsidiarias; no se puede descartar que parte del exceso sea convención de registro.
- *Ceros ausentes:* tratados como NaN; si se contaran como ceros, aparecerían muchas
  "sumas" triviales. El resultado negativo se mantiene con el tratamiento correcto.
- *Copia de la secuencia en HP038:* los largos idénticos a p2–p8 (7/7) son demasiado
  exactos para ser casualidad; o el quipu es recursivo de verdad, o la base lo copió. No
  se puede decidir sin la foto/el registro físico.

## 4. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| 397 cuerdas en nivel ≥ 3, en 46/651 quipus, 153 árboles, 1 409 cuerdas | **Bien apoyado** (conteo directo) |
| HP038 tiene una cadena de 15 niveles cuya secuencia de largos copia p2–p8 (7/7 exactos) | **Bien apoyado** (dato KFG) / **propuesto** (que sea intencional o artefacto) |
| En los árboles profundos no hay suma padre = Σ hijos (0/26 en nivel ≥ 3; 1/73 global) | **Bien apoyado** para estos datos; **apoyado** como afirmación sobre el corpus (95 árboles sin nodo comparable) |
| La suma padre = hijos existe en el corpus pero localizada (UR113, UR169) | **Apoyado con datos** (nulo, BH) |
| Los árboles profundos son mayoritariamente espinas con ramas, no jerarquías equilibradas | **Apoyado con datos** (tipología y grados) |
| Hay más árboles profundos de los esperados por ramificación aleatoria (153 vs 78; 7 quipus BH) | **Apoyado con datos** (nulo A, Poisson-binomial) |
| La profundidad típica no es extrema; solo HP038 lo es | **Apoyado con datos** |
| Los valores se duplican hacia abajo más de lo esperado (12,9 % vs 7,6 %) | **Apoyado con datos** |
| Incahuasi tiene más estructura profunda tras ajustar por tamaño | **Apoyado con datos**, con la reserva de intensidad de registro |
| Los árboles profundos son "desgloses parciales" (categorías con conteos independientes), no sumas | **Propuesto** (la parte negativa está bien apoyada; la positiva es interpretativa) |
| UR271 son "cadenas de réplica" | **Propuesto** (patrón claro, 5/5, pero sin corroboración externa) |
| KH0197 es una duplicación/transcripción de KFG | **Propuesto** (discrepancia OKR fuerte, pero OKR está incompleto) |
| Que los árboles profundos tengan significado genealógico, ritual o calendárico | **Especulativo** (no hay evidencia estructural que lo distinga) |

## 5. Limitaciones

1. **Una sola transcripción para 42/46 quipus.** KFG es la única fuente de la estructura
   fina; OKR solo cubre 4. No se puede separar "estructura antigua" de "convención de
   transcripción" en la mayoría.
2. **Los valores ausentes son masivos en los niveles hondos.** El test de suma se apoya en
   58 árboles con al menos un nodo comparable; los otros 95 no aportan información
   aritmética.
3. **No hay semántica.** Sabemos que hay números y colores, pero no qué cuentan. La
   etiqueta "desglose" es una descripción estructural, no una traducción.
4. **La procedencia "Incahuasi" agrupa un proyecto de excavación**, no una cultura; el
   efecto de procedencia puede ser un efecto de registro.
5. **HP038 puede ser un artefacto de la base.** Sus largos idénticos a p2–p8 son la señal
   más fuerte; haría falta la foto o el registro físico para decidir.

## 6. Para el coordinador

- **Los árboles profundos son raros y están concentrados:** 397 cuerdas en nivel ≥ 3
  (0,69 %), 153 árboles en 46/651 quipus (7,1 %), 1 409 cuerdas (2,4 %). Cinco quipus
  reúnen el 60 %; KH0083 solo tiene 40 árboles y 447 cuerdas.
- **No son sumas jerárquicas.** Solo 1/73 nodos comparables cumple padre = Σ hijos
  (0/26 en nivel ≥ 3); el único caso está en nivel 1. El control positivo funciona:
  UR113 tiene 15/52 sumas exactas (BH = 3 × 10⁻¹²) y UR169 4/20. La suma existe en el
  corpus, pero no en las estructuras profundas.
- **Son sobre todo "espinas" con ramas:** 88/153 son cadenas con ramas y 31 cadenas
  largas; solo 27 son árboles ramificados y 7 abanicos. El árbol profundo modal tiene
  muchos nodos de un solo hijo, no una jerarquía equilibrada.
- **La profundidad típica no es extraordinaria:** 3,31 niveles observados vs 2,28 del nulo
  que conserva los grados y 3,23 del árbol recursivo aleatorio. Lo anómalo es la
  *cantidad*: 153 vs 78 esperados, con 7 quipus significativos tras BH (UR262, KH0083,
  UR270, UR271, UR280, KH0197, UR1175).
- **HP038 es el único caso individual extremo:** 15 niveles, 66 cuerdas, y una cadena
  cuyos largos copian exactamente los colgantes p2–p8 (40, 42, 38, 39, 8, 28, 29 cm;
  7/7). Es o una estructura recursiva real o una duplicación de la base; no está en OKR.
  Recomiendo verificar la foto/el registro físico antes de interpretarlo.
- **Hay un patrón de réplica, no de suma:** 12,9 % de las aristas internas repiten el
  valor de la madre (nulo 7,6 %, p = 0,001), y sube con la profundidad (17,5 % en nivel 3).
  UR271 tiene 5/5 árboles con el mismo número repetido en todos los niveles (220, 200,
  150). Es un fenómeno distinto que merece una ficha propia.
- **El color no codifica las ramas como se esperaba:** la diversidad de color entre
  hermanos no supera el azar (0,658 vs 0,684; p = 0,99); solo hay un leve exceso de
  herencia madre-hijo (44,6 % vs 38,9 %; p = 0,002).
- **Cuidado con la base:** 42/46 quipus no están en OKR; KH0197 discrepa fuertemente
  (149 cuerdas/nivel 4 en KFG vs 35/nivel 1 en OKR, quipu incompleto). Los 5 árboles de
  KH0197 y su plantilla repetida no están verificados.
- **El tamaño explica mucho, no todo:** OR 2,18 por duplicación de cuerdas; aun así
  Incahuasi sigue con OR 4,9 ajustada, pero también tiene más intensidad de registro
  (21,6 % de colgantes con subsidiarias vs 12,5 %). No se puede separar práctica de
  convención con estos datos.
- **Siguiente ronda recomendada:** (1) verificar HP038 y KH0197 contra foto/OKR/otra
  transcripción; (2) analizar los abanicos de 8 cuerdas de HP038 y las plantillas de
  KH0197 como posible convención de registro; (3) probar si los árboles profundos de
  UR262/UR280 son desgloses de categorías (color/tipo) usando los nudos y no solo el
  valor; (4) buscar el mismo patrón de "réplica" en quipus sin estructura profunda.
