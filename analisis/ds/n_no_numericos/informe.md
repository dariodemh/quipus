# Quipus no numéricos como clase propia: anomalía decimal, estructura y candidatos

**Equipo:** `n_no_numericos` · **Fecha:** 18 de octubre de 2026 · **Semilla:** 20261018
**Datos:** `analisis/datos/cuerdas.csv` (57 818 filas; 57 809 tras deduplicar), `quipus.csv`, `grupos.csv`; OKR `khipu.db` (619 quipus); KFG `khipu_summary.csv`.
**Scripts (en esta carpeta, ejecutables en orden):** `00_dedup.py`, `02_indice.py`, `04_estructura.py`, `05_nulo.py`, `06_clase.py`, `07_caracterizar.py`, `08_colorgram.py`, `09_tipomi.py`, `10_direccion.py`, `11_nulo_corpus.py`, `12_clase_final.py`, `13_controles.py`, `14_negativos.py`, `15_top10.py`, `16_consolidar.py`, `17_okr_top10.py`, `18_sensibilidad_nulo.py`.
**Salidas principales:** `quipus_clase.csv` (maestro por quipu), `cuerdas_anom.csv`, `nulo_corpus.csv`, `nulo_resumen.csv`, `top10.csv`.

---

## 1. Pregunta

¿Existe una clase de quipus que rompe la gramática decimal —o que la cumple con patrones no contables— y que por eso sea candidata a registro no estadístico (narrativa, nombres, calendarios, etiquetas)? ¿Se puede identificar con un índice reproducible, separando anomalía real de error de transcripción? ¿Qué estructura no aritmética tiene esa clase? ¿Qué quipus concretos deberían leerse primero?

---

## 2. Método

### 2.1 Corpus y limpieza

- 651 quipus, 57 809 cuerdas tras eliminar 9 filas duplicadas de `UR196` y `MM007_AN002` (dos filas para la misma cuerda, una con nudos y otra vacía). Sin esta limpieza, las filas vacías generaban “ceros imposibles” espurios y duplicaban cuerdas en los cruces.
- 64 464 racimos de nudos parseados; 40 158 cuerdas con nudos y 17 651 sin nudos. `valor = 0` con `nudos` vacío = ausente (regla del BRIEF).
- Unidad de inferencia: **el quipu**. Los contrastes de cuerda usan permutaciones dentro de quipu o se agregan por quipu.

### 2.2 Parser y corrección de la premisa

Cada racimo se parsea como `nTIPO(pos,dir),valor`. La clave es que **el exponente decimal se obtiene de los ceros finales del valor aportado**, no del número `n`:

- `3S(7.5),30` → 3 nudos simples en decenas (exponente 1).
- `9L(9.0),9` → 9 vueltas en unidades (exponente 0).
- `30L(5.5),30` → 3 vueltas en decenas (exponente 1), no 30 vueltas.
- `100E(2.5),100` → 1 figura de ocho en centenas (exponente 2).

Esto obliga a corregir dos supuestos de la tarea:

1. **“Nudos largos o de ocho fuera de unidades” no es, por sí solo, una anomalía.** Hay 341 racimos L/E con exponente >0 (0,9 % de los L/E). Son nudos posicionales válidos: el KFG lo documenta explícitamente para AS027 (“Figure eight knots or long knots are used in all positions. No single knots occur”) y el OKR registra E con `knot_value_type` 10/100. Solo 86 racimos L/E tienen **más de 9 vueltas** en la misma posición, y esos sí son morfológicamente raros.
2. **“Nudos simples en unidades” es una convención menor, no una ruptura.** Hay 221 racimos S con exponente 0 (0,34 % de los racimos), concentrados en AS (108) y UR (93). En varios quipus el nudo simple se usa para “1” en unidades (AS054, AS026B). No es un marcador de clase: solo 2 quipus de la clase tienen una tasa ≥0,2.

Por tanto, el índice se construye sobre lo que **sí** rompe la posición decimal: varios racimos en el mismo orden, inversiones de orden y cuerdas que son pura secuencia de un solo orden.

### 2.3 Índice de anomalía decimal

Por quipu se calculan:

| Índice | Definición | Qué mide |
|---|---|---|
| **Q** | fracción de cuerdas multi-racimo con **un solo exponente** | secuencia pura (tally/unary), no numeral posicional |
| **D** | fracción de cuerdas multi-racimo con **exponente repetido** | varios racimos en la misma posición (unidades duplicadas, “nether knots”) |
| **I** | inversiones / pares adyacentes (el exponente **aumenta** hacia abajo) | orden decimal roto |
| **R** | `Rdiff` = color rico en cuerdas sin nudo − color rico en cuerdas con nudo | ¿las cuerdas vacías llevan color/estructura? |
| **Z** | cuerdas con nudos y valor 0, o racimos de tipo desconocido (`0U`) | ceros imposibles / nudos no clasificados |
| **C** | S en unidades + L/E con >9 vueltas + E con valor no potencia de 10 | anomalías de convención (se reportan aparte) |

Un quipu es **ND** (no decimal estructural) si tiene ≥5 cuerdas multi-racimo y cumple, con q < 0,05 frente al nulo de corpus, al menos una de: Q ≥ 0,50; D ≥ 0,50; I ≥ 0,10. Es **NC** si tiene ≥5 cuerdas sin nudo y ≥5 con nudo, `Rdiff ≥ 0,3` y q < 0,05. Es **NU** si Z ≥ 0,10 y ≥8 cuerdas.

### 2.4 Nulos y corrección múltiple

- **Nulo intra-quipu (el pedido en la tarea):** se barajan los tipos de nudo entre los racimos del quipu, preservando valores, posiciones y tamaños de cuerda. Sirve para preguntar si la *colocación* de los tipos es anómala **dada la composición del propio quipu**.
- **Nulo de corpus (el que se usa para la clase):** para cada quipu se muestrean secuencias de exponentes de igual longitud desde el resto del corpus (dejando fuera al propio quipu), 4 999 réplicas. Pregunta: ¿este quipu se parece a un quipu decimal típico? Es el nulo adecuado para Q/D/I porque el nulo intra-quipu **no puede** detectar una composición pura de unidades: si todas las cuerdas son de unidades, barajar dentro del quipu deja Q = 1.
- **Nulo de color:** se permutan las etiquetas de “color rico” entre cuerdas del quipu (2 000 réplicas), preservando qué cuerdas no tienen nudo.
- **Corrección:** BH-FDR por familia (Q, D, I, Rdiff, tests de caracterización). Los p-valores empíricos tienen resolución 1/5 000 ≈ 0,0002.

### 2.5 Errores de transcripción

Se marcan y excluyen de la clase primaria: `UR090`, `UR235`, `UR144`, `UR193`, `UR190`, `KH0058`, `HP054`, `HP038`, `HP004`, `AS072`, `AS050`, `AS101_Part_1/2`, `AS069`, `AS013`, `AS014` (valores reconstruidos por KFG), `AS036`, `AS037`, `AS081`, `AS129`; además, cualquier quipu con tasa de discrepancia KFG–OKR > 5 %. Cinco quipus de la clase quedan marcados: **UR193, UR144, HP054, AS014, AS081**; la clase limpia baja de 61 a 56.

---

## 3. Resultados

### 3.1 Qué es y qué no es una anomalía decimal

| Fenómeno | Conteo | Lectura |
|---|---:|---|
| L/E con exponente >0 | 341 racimos (0,9 % de L/E) | **Válido**: nudo posicional; no es anomalía |
| L/E con >9 vueltas en la misma posición | 86 racimos en 14 quipus | Morfología rara; posible nudo “especial” o error |
| S en unidades (exponente 0) | 221 racimos en 48 quipus | Convención menor (S = 1); concentrada en AS |
| Exponente repetido en la cuerda | 2 961 cuerdas, 7 311 racimos, 261 quipus | Núcleo del fenómeno “nether knots”/unidades múltiples |
| Cuerda con un solo exponente (multi-racimo) | 1 864 cuerdas | Secuencia pura (tally/unary) |
| Inversión de orden | 532 cuerdas, 548 pares, 69 quipus | Orden decimal roto |
| Nudos con valor 0 / tipo desconocido | 63 cuerdas en 31 quipus; 25 en UR179/180 | 25 son nudos “no-axis”; el resto son aislados |
| Cuerdas sin nudo con color rico | 4 349 de 17 651 | Posible etiqueta/color, pero común |

**Conclusión de esta sección:** la premisa “L/E fuera de unidades = no numérico” no se sostiene. El verdadero eje es **la repetición de orden** (varios nudos del mismo orden) y **la secuencia pura** (cuerdas con un solo orden).

### 3.2 La clase: 61 quipus (56 limpios)

- **61/651 = 9,4 %** de los quipus; **56/651 = 8,6 %** tras excluir los confundidos con transcripción.
- Composición: **ND 54** (35 por Q, 51 por D, 10 por I; solapamientos), **NC 6**, **NU 3**.
- Subtipos exclusivos sobre los 61 (antes de excluir): `seq+dup` 34, `dup` 8, `dup+inv` 7, `inv` 3, `NC` 4, `NU` 3, `seq+dup+NC` 1, `dup+NC` 1. En la clase limpia (56) quedan `seq+dup` 32, `dup` 8, `dup+inv` 5, `inv` 3, `NC` 4, `NU` 2, `seq+dup+NC` 1, `dup+NC` 1.
- **15 quipus son “tally puro”**: ≥95 % de sus racimos están en unidades (AS076, HP019, HP020, JC012, UR050, UR054, UR052, UR003, UR112, UR051, UR110, UR007, UR055, AS077, UR178).
- **39 ND conservan un “esqueleto” decimal** (algún exponente >0) y añaden unidades extra. Es compatible con **nether knots/tallies añadidos a un registro decimal**, no necesariamente con un registro no decimal.
- La lista completa, con subtipo y flags, está en `quipus_clase.csv` (`clase_limpia == 1`).

**Nulo de corpus (test principal).** En los quipus ND con Q/D/I altos, Q observado = 1,00 frente a un nulo de 0,10–0,19; I = 0,39 frente a 0,02; D = 1,00 frente a 0,13–0,45. Los candidatos ND principales dan p = 0,0005 (q = 0,002–0,011 tras BH). La sensibilidad excluyendo las propias secuencias del quipu (`18_sensibilidad_nulo.py`) reproduce p = 0,0005 para UR178, UR050, UR054, UR052, KH0001, UR177, UR203 y UR215.

**Nulo intra-quipu (test pedido).** Solo **4 de 54** quipus ND son significativos con este nulo. Los quipus de secuencia pura dan p ≈ 1 (UR178, UR050, UR054), exactamente porque su composición ya es de unidades. Esto no es un fallo del test: es la demostración de que **el nulo intra-quipu condiciona sobre la composición y por eso no puede detectar la no-decimalidad composicional**. El nulo de corpus es el que responde a la pregunta.

### 3.3 Tres regímenes dentro de la clase (no excluyentes)

1. **Tally puro / secuencia unaria** (15 quipus). Cuerdas con 2–5 nudos idénticos (p. ej. AS076: `2L,2L,2L`; JC012: `1E,1E`; UR178: cuatro `1S`). Valores pequeños y repetidos. Es el grupo más claramente no posicional.
2. **Decimal + nudos inferiores** (39 quipus). Conservan decenas/centenas pero acumulan unidades repetidas o invertidas (KH0001, UR177, UR203, UR215, UR1095). Puede ser un tally añadido, no un lenguaje distinto.
3. **Morfología rara** (UR179/180 no-axis; UR203/UR215 spiral; UR193 spiral, marcado por transcripción). Nudos que no se dejan leer como S/L/E estándar. Es el grupo más prometedor para una lectura de signos, pero también el más difícil de separar de “nudo dañado”.

### 3.4 Caracterización frente al resto

Clase limpia (n = 56) vs resto limpio (n = 575). Medianas o proporciones; q de BH.

| Variable | Clase | Resto | p / q |
|---|---:|---:|---:|
| cuerdas (mediana) | 78,5 | 41 | q = 0,010 |
| racimos (mediana) | 82,5 | 42 | q = 0,0003 |
| cuerdas multi-racimo | 14,5 | 9 | q = 0,0002 |
| cuerdas con nudo | 50,5 | 29 | q = 0,006 |
| **canutos (presencia)** | **67,9 %** | **22,4 %** | **q < 0,001** |
| **fibra de camélido (CL)** | **16,1 %** | **1,7 %** | **q < 0,001** |
| cuerdas superiores (`union=T`) | 0 % | 4,35 % | p = 0,155 (NS) |
| fracción de subsidiarias | 2,3 % | 12,5 % | p = 0,15 (NS) |
| algún subsidiario | 53,6 % | 67,4 % | p = 0,053 (borde) |
| color rico (≥2 componentes) | 18,3 % | 20,0 % | p = 0,45 (NS) |
| n.º de colores distintos | 5 | 7 | p = 0,36 (NS) |
| colores exactos distintos en el quipu | 7,8 | 10,9 | **p = 0,019 (menor en clase)** |
| banded | 73,2 % | 71,8 % | p = 0,88 (NS) |
| seriated | 75,0 % | 81,6 % | p = 0,28 (NS) |
| Benford match | 0,747 | 0,744 | p = 0,92 (NS) |
| MI(valor; color) | 0,52 | 0,87 | **p < 0,001 (menor en clase)** |
| mediana de la fracción de cuerdas multi-racimo con nudos idénticos (mismo tipo y valor) | 11,6 % | 0 % | **p < 0,001** |
| mediana de la fracción de cuerdas multi-racimo con un solo tipo de nudo | 42,6 % | 3,3 % | **p < 0,001** |

**Lectura:** la clase es **más grande, más plana, con muchos nudos del mismo tipo/valor, valores pequeños y repetidos**, y **sin cuerdas superiores**. El color no es más rico; al contrario, el vocabulario exacto de color es menor. La asociación valor–color es más débil (esperable si los valores son degenerados).

### 3.5 Correlatos materiales: canutos y fibra

- **Canutos:** 67,9 % de la clase vs 22,4 % del resto (OR = 7,30; q < 0,001). En logit controlando log(tamaño) y prefijo, el efecto sigue: coeficiente 2,06 (OR ≈ 7,9; p < 0,001). Estratificado por museo, OR de Mantel–Haenszel = **9,4**. Sobrevive dentro de AS (58 % vs 18 %), HP (60 % vs 10 %), UR (79 % vs 24 %) y en todos los cuartiles de tamaño.
- **Fibra de camélido:** 16,1 % vs 1,7 % (OR = 10,8; q < 0,001). En UR, controlando tamaño, OR ≈ 15,4 (p < 0,001); estratificado por museo, MH OR = 6,9. Pero las celdas son pequeñas y el camélido está concentrado en unas pocas colecciones (Soldi, Banco Central, Temple Radicati, Ica). **Nivel: propuesto, confundido con colección.**
- **Canutos + camélido** apuntan a un **género material** distinto: quipus de fibra animal, con envolturas de cordón principal, cuerdas largas y nudos repetidos. Es el hallazgo positivo más robusto fuera del propio índice.

### 3.6 Estructura no aritmética: color, entropía, tipo/orden, dirección

**a) N-gramas de color como “palabras”.** Sobre cuerdas de nivel 0 ordenadas dentro de cada grupo, con símbolos (color grueso, torsión):

| Métrica | Clase | Resto | p |
|---|---:|---:|---:|
| repetición de bigramas | 0,906 | 0,881 | 0,95 |
| repetición de trigramas | 0,794 | 0,755 | 0,88 |
| entropía condicional normalizada | 0,61 | 0,55 | 0,16 |
| quipus con p_cond < 0,05 | 55,3 % | 48,7 % | 0,44 |
| MI(patrón de tipos; color) | 0,354 | 0,372 | 0,57 |
| MI(valor; color) | 0,555 | 0,962 | < 0,001 |

No hay un “lexicón” de color en la clase. La repetición de bigramas es altísima en **todo** el corpus (banding/seriation), no un rasgo de la clase. Hay un resultado nominal frágil: tras BH, 14,9 % de la clase vs 3,8 % del resto tienen bigramas de color significativamente repetidos (OR = 4,4; p = 0,005), pero la repetición bruta **no** es mayor y el efecto lo arrastran unos pocos quipus con bandas; no lo interpretamos como palabras.

**b) Tipo/orden de nudo más allá del valor.** El MI entre el patrón de tipos y el color, controlando por valor, no distingue a la clase (0,354 vs 0,372; p = 0,57). El tipo/orden no lleva información de color más allá del valor. La única diferencia es que en la clase el valor predice menos el color (0,555 vs 0,962), coherente con valores degenerados.

**c) Dirección S/Z (Urton 2003).** En 398 quipus con ≥20 nudos con dirección: fracción S en la clase 0,345 vs 0,23 en el resto (p = 0,21); entropía de dirección 0,236 vs 0,351 (p = 0,83). No hay un código binario de dirección específico de la clase. UR178 sí tiene una secuencia S,S,S,Z en sus primeras cuerdas, pero son solo 9 nudos con dirección; es una pista local, no un patrón de clase.

**d) Repetición dentro de la cuerda.** La clase tiene más cuerdas formadas por nudos idénticos (mismo tipo y valor): 11,6 % vs 0 % de mediana; y más cuerdas con un solo tipo de nudo: 42,6 % vs 3,3 %. Esto es la firma estructural del **tally/unary**, y es el resultado no aritmético más sólido de la clase.

**e) Contraste explícito con las tres propuestas.**

| Propuesta | Predicción para una clase no numérica | Resultado en esta clase | Nivel |
|---|---|---|---|
| **Urton (2003), código binario** | Torsión, dirección de nudo y ply usados como bits, con secuencias no aleatorias | La dirección S/Z no distingue a la clase (fracción S 0,345 vs 0,23; p = 0,21; entropía 0,236 vs 0,351; p = 0,83). Hay pistas locales (UR178 S,S,S,Z; UR050 80 % S), pero no un código de clase | **No apoyado** como firma de clase; **especulativo** para casos individuales |
| **Hyland (2017), Collata** | Color/fibra/ply como sílabas; muchas combinaciones por colgante; nudos solo terminales | El vocabulario exacto de color es **menor** (7,8 vs 10,9; p = 0,019); no hay n-gramas de color más repetidos (0,906 vs 0,881; p = 0,95); el tipo/orden no lleva color (MI 0,354 vs 0,372). La fibra de camélido sí se asocia (16 % vs 1,7 %), pero como **material**, no como sílaba | **No apoyado** para color/sílaba; **propuesto** solo para el eje fibra/material |
| **Clindaniel (2019)** | S/Z marcado, combinaciones de color y banding/seriation relacionados con magnitud; gramática no numérica distinta | Banded 73,2 % vs 71,8 % (p = 0,88); seriated 75,0 % vs 81,6 % (p = 0,28); dirección sin diferencia. No aparece una gramática de signos distinta, pero sí un eje **unario** (nudos idénticos) que Clindaniel no modeló | **No apoyado** para la gramática de signos; **nuevo** el eje unario |

En conjunto, las tres propuestas predicen una **riqueza de signos** (color, dirección, banding) que esta clase **no** tiene. Lo que sí tiene es **repetición unaria** y **materialidad** (canutos, fibra animal). Es un resultado negativo fuerte para la hipótesis “narrativa/silográfica” y positivo para “tally/etiqueta”.

### 3.7 Los 10 quipus más prometedores

Criterios: (i) anomalía estructural o morfológica confirmada en OKR; (ii) no confundido con error de transcripción; (iii) tamaño legible; (iv) estructura interna que permita una hipótesis falsable. La tabla completa está en `top10.csv`.

| # | Quipu | Cuerdas | Qué tiene | Por qué leerlo primero |
|---:|---|---:|---|---|
| 1 | **UR179** | 18 | 54 nudos de tipo vacío/valor 0; 3 colores; AMNH, Cajamarquilla | KFG dice “no-axis knots”; OKR registra 54 nudos sin tipo. Es el caso más limpio de nudos que existen pero no se dejan leer en decimal. Probar si el número/posición/dirección de nudos forma una secuencia binaria o un tally. |
| 2 | **UR180** | 12 | 30 nudos vacíos + 7 E=1; dos bloques de color (W:NB:DG / W:AB:DG) | Mismo sitio y morfología que UR179, pero mezcla E=1 y no-axis; los bloques de color permiten testear si el color separa secciones. |
| 3 | **UR178** | 14 | 57 nudos S=1, 4–5 por cuerda, todas valen 4/5; S/Z en las primeras cuerdas | Secuencia unaria pura, sin posiciones decimales; el patrón 4/5 y la dirección S/Z son una hipótesis de calendario o código binario. Confirmado en OKR (57 S). |
| 4 | **UR050** | 164 | 501 nudos L de 4–8 vueltas, todos unidades; 163 canutos; 100 % camélido; 80 % S | El tally más grande y mejor documentado; permite testear si los valores L forman series/runs y si los canutos marcan sus cortes. |
| 5 | **UR054** | 115 | 312 L unidades; 113 canutos; 100 % camélido | Réplica de UR050 en la misma colección privada (Soldi); sirve para separar “género” de “objeto único”. |
| 6 | **UR052** | 96 | 320 L unidades; 92 canutos; 60 % camélido; otro museo (Banco Central) | Réplica de UR050/54 en otra colección; si el patrón se repite, es un género, no un espécimen. |
| 7 | **AS076** | 16 | 32 racimos, en su mayoría L2 repetidos; 8 canutos; Musée de l’Homme | Tally puro de “2s” (`2L,2L,2L`), el ejemplo más legible de conteo unario; los canutos permiten ver si separan grupos de 2. |
| 8 | **JC012** | 30 | 35 E=1 y L2, todos unidades; Incahuasi | Tally puro de “1s” (`1E,1E`), procedencia inca controlada (Incahuasi); ideal para comparar con los quipus incas “normales” del mismo sitio. |
| 9 | **UR203** | 167 | 135 multi; D=0,75, I=0,31; 49 SP (“spiral”), 93 E, 2 BL; nota KFG “spiral knots like UR193” | Quipu grande con morfología espiral y orden invertido; testear si SP/EE/BL marcan valores no decimales o una secuencia aparte. |
| 10 | **UR215** | 268 | 42 multi; D=0,48, I=0,32; 28 SP; segundo espiral grande | Réplica de UR203 para el mismo tipo de nudo espiral; permite ver si el patrón se repite en otro objeto. |

**Alternativas inmediatas:** UR055 (698 L, 173 canutos; el tally más grande), UR003 y UR007 (Leymebamba, tally puro), HP019/HP020 (Pachacamac, tally puro), UR282/UR289 (Armatambo, tally puro con canutos), UR223/UR1109 (sin nudos con color rico), KH0001 y UR177 (decimal + nudos inferiores, Chuquitanta).

---

## 4. Controles y amenazas

1. **Nulo explícito y p empírico:** nulo de corpus con 4 999 réplicas por quipu; p mínimo 0,0005; BH por familia. La sensibilidad excluyendo las propias secuencias del quipu reproduce p = 0,0005 en los candidatos ND probados (UR178, UR050, UR054, UR052, KH0001, UR177, UR203, UR215 y UR055).
2. **El nulo intra-quipu no basta:** solo 4/54 ND son significativos con él; los tally puros dan p ≈ 1. Se reporta como limitación metodológica, no como evidencia en contra.
3. **Transcripción:** 5 quipus de la clase marcados y excluidos (UR193, UR144, HP054, AS014, AS081). Los 10 candidatos están en OKR y su composición de tipos coincide (UR179: 54 vacíos; UR178: 57 S; UR050: 501 L; UR203: 49 SP, etc.). Aun así, KFG y OKR comparten en parte el mismo registro de campo: la concordancia es una cota inferior de la calidad, no una validación independiente.
4. **Duplicados:** UR196 y MM007_AN002 tenían filas repetidas; se deduplicó. Sin ello, UR196 aportaba 14 “ceros imposibles” falsos.
5. **Circularidad:** Q, D e I definen la clase; las cifras de “valores pequeños/repetidos” son en parte consecuencia de la definición. No las usamos como evidencia independiente. El color, la dirección, el MI tipo–color, los canutos y la fibra sí son independientes del índice.
6. **Confusión material:** los canutos sobreviven a tamaño, prefijo y museo; la fibra de camélido no sobrevive igual de bien (MH OR 6,9, celdas pequeñas). No usar el museo como lugar de origen.
7. **Morfología vs daño:** sin imágenes no se puede distinguir un nudo “no-axis” o “espiral” de un nudo dañado o mal transcrito. La nota del KFG y la coincidencia con OKR ayudan, pero no cierran la pregunta.
8. **Sesgo del corpus:** 651 quipus no son una muestra aleatoria; sobrerrepresentan UR y procedencia desconocida. Las conclusiones por sitio son exploratorias.
9. **Partes de un mismo objeto:** AS207B y AS207C (partes de AS207) y AS026B (parte de AS026) se cuentan como quipus separados porque el KFG los registra así; si se agrupan, la clase baja en 1–2 casos. No cambia ninguna conclusión, pero el conteo de 61 no debe tomarse como 61 objetos físicos independientes.

---

## 5. Resultados negativos (explícitos)

1. **L/E fuera de unidades no es anomalía:** 341 racimos (0,9 %) y documentados como convención posicional válida (AS027). La premisa de la tarea no se sostiene.
2. **S en unidades no define la clase:** 221 racimos (0,34 %), concentrados en AS; solo 2 quipus de la clase con tasa ≥0,2.
3. **E con valor no potencia de 10** es raro (53 racimos en 23 quipus) y probablemente transcripción/erratas, no un código.
4. **Ceros imposibles:** 63 cuerdas en 31 quipus; 25 son los no-axis de UR179/180 y el resto son aislados (≤4 por quipu). No hay un patrón de “cero” como signo.
5. **No hay lexicón de color:** la repetición de bigramas es 0,906 vs 0,881 (p = 0,95); la entropía condicional no baja (p = 0,16); el vocabulario exacto de color es **menor** en la clase (7,8 vs 10,9; p = 0,019). La hipótesis de Hyland (color/fibra como sílabas) no se apoya en esta clase.
6. **El tipo/orden de nudo no lleva información de color más allá del valor:** MI 0,354 vs 0,372 (p = 0,57).
7. **No hay código binario de dirección específico:** fracción S 0,345 vs 0,23 (p = 0,21); entropía 0,236 vs 0,351 (p = 0,83). Urton 2003 no se confirma como rasgo de esta clase.
8. **No hay cuerdas superiores:** 0/56 en la clase vs 4,35 % del resto (p = 0,155); ninguna estructura de suma superior.
9. **No hay diferencia en banded/seriated:** 73,2 % vs 71,8 % y 75,0 % vs 81,6 % (NS). El patrón de color de Clindaniel no separa la clase.
10. **No hay diferencia de Benford:** 0,747 vs 0,744 (p = 0,92).
11. **No hay heterogeneidad global por procedencia:** chi² p = 0,32. Solo dos clusters pequeños y post hoc: Cajamarquilla 3/4 (Fisher p = 0,0029) y Chuquitanta 2/4 (p = 0,046). Son sugerentes, pero con n = 4 por sitio y elegidos después de mirar los datos; no los tratamos como confirmados.
12. **El nulo intra-quipu no detecta la no-decimalidad composicional:** 4/54; es una limitación del nulo, no una prueba de que la clase sea decimal.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Existe una clase estructural de 61 quipus (9,4 %) con exceso de racimos del mismo orden / secuencias puras | **Apoyado con datos** (definición explícita; depende del índice) |
| 15 quipus son “tally puro” (≥95 % de racimos en unidades) | **Demostrado** (conteo); la lectura como tally unario es **propuesto** |
| 39 ND conservan un esqueleto decimal y añaden unidades | **Apoyado con datos**; compatible con nether knots/tallies, no con no-decimalidad pura |
| Los canutos se asocian a la clase (OR 7,3; MH 9,4) | **Apoyado con datos** (robusto a tamaño, prefijo y museo; registro de canutos incompleto) |
| La fibra de camélido se asocia a la clase | **Propuesto** (OR alto pero celdas pequeñas y confusión con colección) |
| La clase no tiene un lexicón de color (vocabulario igual o menor) | **Apoyado con datos (negativo)** |
| El tipo/orden de nudo no lleva color más allá del valor | **Sin evidencia** (MI 0,354 vs 0,372; p = 0,57) |
| No hay código binario de dirección específico | **Sin evidencia** (fracción S 0,345 vs 0,23; p = 0,21) |
| No hay cuerdas superiores en la clase | **Sugerente (negativo)**; 0/56, p = 0,155 |
| UR179/UR180 son “no-axis knots” y UR203/UR215 “spiral knots” | **Apoyado con datos** para la existencia (KFG + OKR); **propuesto** para su significado |
| Los clusters Cajamarquilla y Chuquitanta | **Propuesto** (n = 4 en cada sitio; post hoc) |
| La clase es narrativa/silográfica al estilo Collata | **Especulativo / no apoyado** |
| La clase es un género de tally/etiqueta, no un registro estadístico | **Propuesto** (la explicación más parsimoniosa) |

---

## 7. Ideas para la siguiente ronda

1. **Auditoría de imágenes** de UR179, UR180, UR178, AS076, JC012, UR203 y UR215: confirmar si los nudos “vacíos/espiral” son morfologías reales o daño; es la única forma de romper la ambigüedad.
2. **Test de unario vs decimal** en los 15 tally puros: ¿el número de nudos por cuerda se distribuye como un conteo (Poisson/binomial) o como un código? ¿Los runs de nudos idénticos tienen longitudes con significado (2, 4, 5)?
3. **Canutos como marcadores de sección:** cruzar los canutos (posición, color, número) con los grupos y los runs de nudos en UR050/54/52/55 y AS076; t_canutos_fibra ya mostró que los canutos delimitan grupos y llevan color propio.
4. **Espiral/no-axis:** estudiar los 3 quipus con SP (UR193, UR203, UR215) y los 2 no-axis (UR179/180) como un subcorpus morfológico; buscar si SP/EE/BL reemplazan a S/L/E en posiciones específicas.
5. **Repetición de tipo dentro de la cuerda** como variable de género: `sametipo` (42,6 % vs 3,3 %) es un discriminador fuerte y barato; usarlo en futuros modelos de clasificación.
6. **Control de colección/fibra:** conseguir la fibra por cuerda de más quipus (hoy solo 297) para separar el efecto material del efecto género.
7. **Replicar el nulo de corpus** con un modelo jerárquico (quipu → grupo → cuerda) para no depender de un pool global.
8. **No usar el nulo intra-quipu para clases composicionales:** reportar siempre el nulo de corpus o un modelo generativo que permita composiciones puras.

---

## 8. Para el coordinador

- **La clase existe, pero no es una sola cosa.** 61 quipus (9,4 %) rompen la gramática decimal; 56 quedan tras excluir 5 confundidos con transcripción. Dentro hay **15 tally puros** (≥95 % de racimos en unidades), **39 decimales con unidades extra** (compatibles con nether knots/tallies) y **6 sin nudos con color rico**; son categorías que se solapan, no una partición.
- **Corrección importante de la premisa:** los nudos largos o de ocho “fuera de unidades” **no** son anomalía; son nudos posicionales válidos (341 racimos, documentados en AS027 y en OKR). El eje real es la **repetición de orden** y la **secuencia pura**, no el tipo de nudo.
- **El hallazgo material más robusto son los canutos:** 68 % en la clase vs 22 % en el resto (OR 7,3; q < 0,001; OR 9,4 estratificado por museo). La fibra de camélido también (16 % vs 1,7 %; OR 10,8) pero está confundida con colección. La clase se asocia a un **género material** (canutos robustos; fibra animal sugerente), no a un color más rico.
- **No hay evidencia de un lenguaje de color.** La repetición de bigramas de color es altísima en todo el corpus (0,91 vs 0,88; p = 0,95), la entropía condicional no baja y el vocabulario exacto de color es **menor** en la clase (7,8 vs 10,9; p = 0,019). Hyland (Collata) no se replica en esta clase.
- **Tampoco hay código binario de dirección ni información de tipo/orden más allá del valor:** MI(tipo; color) 0,354 vs 0,372 (p = 0,57); fracción S 0,345 vs 0,23 (p = 0,21). Urton 2003 y Clindaniel 2019 no se confirman como firma de esta clase.
- **La estructura no aritmética que sí aparece es el unario:** mediana de la fracción de cuerdas con nudos idénticos 11,6 % vs 0 %; mediana de la fracción con un solo tipo de nudo 42,6 % vs 3,3 %. Es un patrón de **tally/secuencia**, no de narrativa.
- **Los 3 quipus de Cajamarquilla son la prioridad:** UR179 y UR180 tienen nudos “no-axis” (KFG) que OKR registra como 54 y 30 nudos sin tipo; UR178 es una secuencia de 57 nudos S=1. Es un conjunto local coherente (AMNH, Cajamarquilla) y el mejor candidato a lectura de signos.
- **Los 10 candidatos concretos:** UR179, UR180, UR178, UR050, UR054, UR052, AS076, JC012, UR203, UR215. UR179/UR180 son morfología no-axis; UR178 y los cinco siguientes son tally puro (con canutos en UR050/54/52 y AS076); los dos últimos son nudos espirales. Alternativas: UR055, UR003, UR007, HP019/HP020, UR282/UR289, UR223/UR1109.
- **No sobreinterpretar:** 39 de los 54 ND conservan un esqueleto decimal; sus unidades extra pueden ser nether knots/tallies añadidos, no un lenguaje distinto. Sin imágenes no se puede separar “nudo especial” de “nudo dañado”. La lectura narrativa sigue siendo **especulativa**; la lectura como **tally/etiqueta** es la más parsimoniosa y es la que recomiendo testear primero.
- **Siguiente paso barato y decisivo:** auditar imágenes de UR179/180/178 y AS076/JC012, y cruzar los canutos con los runs de nudos en UR050/54/52/55. Eso convertiría la clase de “prometedora” en “demostrada” (o la refutaría) sin necesidad de nuevos datos.
