# UR231 / KH0468 — Lectura profunda de un quipu de Ica/Pisco

**Autor:** equipo DS · **Fecha:** 2026-10-18 · **Carpeta:** `analisis/ds/k_UR231/`
**Scripts reproducibles:** `01_estructura.py` … `08_plantilla.py` (semilla 0 en todos los nulos).

---

## 1. Pregunta

¿Qué es UR231? ¿Cómo está construido, qué aritmética contiene y qué tipo de registro
(censo, tributo, depósito, calendario u otro) es el más probable? ¿Qué filas y columnas
tendría? ¿Qué no encaja y qué parte podría ser información no numérica?

## 2. Datos y método

- **Fuente primaria:** `analisis/datos/cuerdas.csv` (KFG), `grupos.csv`, `quipus.csv`.
  **Verificación independiente:** OKR `khipu.db`, `KHIPU_ID = 1000541` (`KH0468`), que
  tiene exactamente **954 cuerdas, 1:1 con KFG**. Los valores KFG se recalcularon desde
  la cadena `nudos` en las 227 cuerdas con nudos: **0 discrepancias**, y todos los nudos
  simples tienen ≤9 unidades y posiciones monótonas (control de calidad, `01`).
- **Unidad de análisis:** el quipu. Al ser un estudio de caso, todos los controles son
  **permutaciones dentro del quipu**, no inferencia poblacional.
- **Nulo principal:** se barajan los **226 valores de colgante** entre las 864 posiciones
  de colgante, conservando la estructura de grupos, los colores y los 638 ceros
  (= cuerdas sin nudos, valores ausentes, no ceros reales). 1000–2000 permutaciones,
  semilla 0. Para las sumas intra-grupo se usó además un **nulo intra-grupo** (barajar
  los valores dentro de cada grupo), que es el control correcto porque los valores de un
  mismo grupo comparten magnitud.
- **Corrección múltiple:** Holm sobre el conjunto de tests principales (§4.5).
- **Literatura:** búsqueda por `UR231`, `KH0468`, `VA16135`, `Ica/Pisco` en `docs/fichas/`
  y `docs/estado_del_arte.md`; se leyeron las fichas `repo-kfg` y `2005-Urton-khipu-archives`.

## 3. Estructura

### 3.1 Cifras globales (todas demostradas sobre los datos)

| Variable | Valor |
|---|---|
| Cuerdas totales | **954** = **864 colgantes + 90 subsidiarias** |
| Cordón principal | 304 cm (2.º más largo de 651 quipus) |
| Percentil en nº de cuerdas | 99,5 del corpus |
| Grupos de colgantes | **80** (percentil 98,2 del corpus) |
| Colgantes por grupo | moda **11** (59 grupos), 10 (9), 12 (8), 8 (2), 7 (1), 6 (1) |
| Cuerdas con nudos | **227** (226 colgantes + 1 subsidiaria); **727 sin nudos (76,2 %)** |
| Valor total | **26 251** |
| Grupos con algún valor | **30 / 80** |
| Colores distintos | **64**; 73/80 grupos son monocromos |
| Unión de colgantes | **862 V, 0 R, 2 ?**; subsidiarias: 89 U, 1 V |
| Torsión | 952 S, 2 sin dato |
| Nudos | **1 780**: 849 S, 911 L, 20 E; dirección **1 779 Z, 1 U** |
| Terminaciones | 779 K, 164 B, 9 R, 2 sin dato |
| Cuerdas superiores (union T) | **0** |

**Lectura inmediata:** es un quipu **excepcionalmente grande, muy regular en grupos de 11
colgantes, monocromo por grupo y mayoritariamente vacío**. El 76,2 % de cuerdas sin nudos
está en el percentil 96,5 del corpus, pero no es único (AS069 78 %, UR1057 69 %): hay un
"género" de quipus grandes y poco anudados, no es solo daño.

### 3.2 La plantilla 6 × 14 (el hallazgo estructural central)

La nota de catalogación del OKR ya dice que el quipu está organizado en **"sets of 14 cord
groupings (each composed of ca. 11 pendants)"** y que es la unión de dos fragmentos
(VA16135a + VA16135b). Los datos confirman esa plantilla y la precisan:

- Hay **cuatro grupos de fibra vegetal** (no algodón) en los grupos **36, 50, 64 y 78**,
  exactamente a **14 grupos de distancia** (p exacta ≈ **2,4 × 10⁻⁵**; ver §5.3).
- Tomando como referencia el grupo **0D** y el de **12 cuerdas** (que en C–F ocupan las
  ranuras 5–6), los seis conjuntos quedan:

```
Ranura:  1      2           3           4          5          6          7       8          9   10 11 12    13     14
A (0)    MB     YB:GG 5/164 0D 10/558  B 12/5766  KB         MB 7/461   B       B          B/KB bandado
B (9)    B      YB 1/10     B:MB        AB:MB 1/34 W:0D 5/20  AB:MB      0D 10/165 AB 12/2695 MB:CB YB 10/423 YB HB W:B HB
C (23)   YB:MB  MB:KB 1/32  AB:G0 5/86  AB:MB     0D 10/207  AB 12/3416 CB      MB 6/242   B   B  MB MB    MB     HB [V]
D (37)   MB:KB  PR 1/41     AB:GG 5/51  AB:PR     0D 10/179  B 12/3082  CB      MB 10/469  B   B  MB YB:MB B      HB [V]
E (51)   AB:MB  YB:MB 1/34  W:G 4/61    AB:MB     0D 10/186  AB 12/3054 CB      HB 10/408  AB  GB HB YB:MB HB     HB [V]
F (65)   AB:MB  YB:MB       W:G 5/143   W:KB      0D 10/199  YB 12/3500 AB:KB   MB 10/538  B   MB RD MB    PR 7/13 MB [V]
```

(`n/suma` = número de cuerdas con valor / suma; `[V]` = fibra vegetal. Los conjuntos se
delimitan por los terminadores 8, 22, 36, 50, 64 y 78: A es un fragmento de 9 grupos;
B–F tienen 14 grupos cada uno.)

**Lo que la tabla muestra:**

1. En los cuatro conjuntos alineados (C–F), las ranuras **5, 6 y 8** están ocupadas por los
   mismos tipos de grupo:
   - ranura 5: grupo **0D**, **10 valores** (165–207; A = 558);
   - ranura 6: grupo de **12 cuerdas, 12 valores** (2 695–3 500; A = 5 766);
   - ranura 8: grupo de **10 valores** (242–538).
2. Las ranuras 2 y 3 llevan grupos pequeños (1 valor ≈ 30–40; 4–5 valores ≈ 20–143).
3. La ranura 14 es el **terminador**: fibra vegetal en C–F; en A y B el terminador es textil
   (B/KB bandado en 8; HB en 22). El par 0D/12 está en 5–6 en C–F, en **7–8 en B** y en
   **3–4 en A**: los dos primeros conjuntos se desvían ±2 respecto de la plantilla. La causa
   (pérdida de grupos vs. diseño distinto del primer tramo) no se puede decidir con un solo
   quipu; los grupos cortos 33, 34, 38 y 43 muestran que sí hubo pérdida de cuerdas.
4. El quipu es, por tanto, **seis copias de una tabla de 14 ranuras**, con los extremos
   truncados.

### 3.3 Colores, subsidiarias y nudos

- **Color:** cada grupo es prácticamente monocromo (73/80); los pocos grupos con varias
  cadenas de color son los "bandados" (p. ej. grupo 8: `B(0–13)/KB(13–27.5)`), donde el
  color cambia a lo largo de la cuerda, no entre cuerdas. El color es, por tanto, una
  **etiqueta de grupo/columna**, no un valor por cuerda.
- **Subsidiarias:** 90 en 11 grupos. **89 de 90 están sin nudos**; la única con valor es
  `p764s1 = 14` (padre `p764 = 169`). Seis grupos (17, 21, 29, 48, 57, 62) tienen
  **11 colgantes + 11 subsidiarias**, todas vacías: es una **segunda fila de la misma
  tabla**, no una jerarquía numérica.
- **Nudos:** estructura decimal canónica (centenas ~4 cm, decenas ~10,5 cm, unidades
  ~19 cm). Reparto: **61 cuerdas con 3 racimos, 131 con 2 y 35 con 1**; en las de un solo
  racimo la posición es la única pista de la escala (de ahí la duda sobre `p115`, §6).
  20 nudos en ocho (valor 1) y un único nudo con dirección U (`p26`). No hay valores de
  4 cifras; máximo **898**.

## 4. Aritmética interna y controles

### 4.1 Lo que reporta KFG (y por qué no es evidencia)

KFG (`ascher_sum_relations/pendant_pendant_sum.csv`) atribuye a UR231 **186 "sumas
pendant-pendant"** (89 izquierdas / 97 derechas; suma media 169) y **13 sumas por color**,
**12 indexed**. Es la cifra que cita Medrano y Khosla (2024) para su reconstrucción.

Al descomponer las 186 relaciones (`04`, `05`):

| Composición de las 186 | n |
|---|---|
| Todos los sumandos en un solo grupo | **94** |
| Atraviesan ≥2 grupos | 92 |
| Incluyen cuerdas sin nudos (cero) como sumandos | **94** |
| En un solo grupo y con 2–5 sumandos no nulos | 83 |
| Ventana de >20 cuerdas | 56 |
| Ventana máxima | **129 cuerdas** (14 grupos) |
| La cuerda suma está dentro del bloque de sumandos | 15 |

El algoritmo de KFG enumera **toda ventana contigua** y busca **cualquier** cuerda del
quipu con ese valor. Con 638 posiciones vacías, cualquier valor rodeado de ceros es "suma"
de decenas de ventanas; y las ventanas largas cruzan grupos sin relación. Es un problema de
**comparaciones múltiples no controlado**, no aritmética.

### 4.2 Réplica estricta (con nulos)

Se reimplementó la fórmula Ascher con la regla del brief (0 sin nudos = ausente, **todos
los sumandos deben tener valor >0**), ventanas contiguas de 2–5 cuerdas:

| Test | Observado | Nulo (media) | p | Nulo usado |
|---|---|---|---|---|
| Suma **adyacente** (cuerda inmediatamente a izq. o der. de la ventana), mismo grupo | **1** | 2,78 | **0,95** | intra-grupo, 1000 perm. |
| Suma en **cualquier posición** del mismo grupo | **11** | 9,73 | **0,38** | intra-grupo, 1000 perm. |
| Tipo KFG, ventanas de 2–6 cuerdas, cualquier posición | 1 471 | 1 061,7 | 0,003 | global, 1000 perm. |

La única suma adyacente es `p425 = 13 = 5 + 8` (grupo 39). No hay exceso de aritmética:
**1 y 11 coinciden con el azar**. El test "global" da p = 0,003 pero es engañoso: **175 de
las 227 cuerdas con valor** tienen alguna coincidencia de ventana corta en algún lugar del
quipu; con ~126 valores distintos y cientos de ventanas, eso es la tasa base, no diseño.

**Conclusión (demostrada, negativa):** UR231 **no contiene aritmética Ascher verificable**.
Las 186 relaciones de KFG son un artefacto del método; la afirmación de reconstrucción
basada en ellas queda debilitada (aunque la reconstrucción puede sostenerse por la
plantilla de color, §5.2).

### 4.3 Totales de grupo, repeticiones y razones

| Test | Observado | Nulo | p | Lectura |
|---|---|---|---|---|
| Total de un grupo = suma de un tramo contiguo de otros grupos | 8 | 16,4 | 0,73 | todos triviales (34 = 34); **no hay jerarquía de totales** |
| Vector de 11 valores de un grupo = suma de un tramo de grupos | **0** | — | — | no hay agregación vectorial |
| Valores repetidos en >1 grupo (35 de 126) | 35 | 35,9 | 0,99 | repetición = azar |
| Razón total ranura 6 / ranura 5, conjuntos B–F | 16,3–17,6 | — | — | CV 3,2 %, pero es consecuencia del perfil compartido (§5.1), no una suma |

### 4.4 Lo que no se puede testear

- **Cuerda superior = suma de grupo:** hay **0 cuerdas con union T** (KFG y OKR). Test
  imposible; resultado negativo estructural.
- **Colgante = suma de subsidiarias:** 89/90 subsidiarias vacías; la única con valor
  (169 vs 14) no suma. En los seis grupos 11+11 la igualdad 0 = 0 es **trivial**, no
  evidencia.

### 4.5 Corrección de Holm (tests principales)

| Test | p | Holm |
|---|---|---|
| Grupos de fibra vegetal en progresión de 14 | 2,4 × 10⁻⁵ | significativo |
| Periodicidad de color a lag 14 (16/66) | 0,0005 | significativo |
| Perfiles de los seis grupos de 12 (r = 0,915) | 0,001 | significativo |
| Sumas intra-grupo (11) | 0,38 | n.s. |
| Totales de grupo (8) | 0,73 | n.s. |
| Sumas adyacentes (1) | 0,95 | n.s. |
| Valores repetidos (35) | 0,99 | n.s. |

Los tres primeros sobreviven Holm (α = 0,05). El de lag 14, además, resiste una corrección
por los 79 lags posibles (0,0005 × 79 ≈ 0,04) y **no es post hoc**: la nota del OKR ya
afirma "sets of 14". El de fibra vegetal sí es post hoc en la elección de d = 14, pero
d = 14 está fijado por la documentación y por el test de color.

## 5. Patrones no aritméticos

### 5.1 Los seis grupos de 12 comparten un perfil de 11 columnas

Los totales por columna (11 primeras cuerdas) de los seis grupos de 12 (el "Total" excluye
la 12.ª cuerda, que es 14–48; el total completo del grupo está en §3.2):

| Grupo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 327 | 426 | 332 | 319 | 402 | 353 | 898 | 789 | 582 | 759 | 531 | 5 718 |
| 16 | 157 | 174 | 204 | 154 | 203 | 141 | 411 | 321 | 275 | 405 | 236 | 2 681 |
| 28 | 284 | 234 | 268 | 184 | 314 | 175 | 539 | 373 | 286 | 461 | 271 | 3 389 |
| 42 | 235 | 223 | 218 | 145 | 213 | 137 | 543 | 372 | 270 | 443 | 264 | 3 063 |
| 56 | 174 | 191 | 256 | 185 | 302 | 168 | 476 | 365 | 278 | 381 | 263 | 3 039 |
| 70 | 169 | 162 | 148 | 165 | 186 | 176 | 523 | 538 | 390 | 606 | 414 | 3 477 |

- Correlación de Pearson media entre pares: **r = 0,915** (nulo permutando dentro de cada
  fila: r ≈ 0,00; p = **0,001**).
- Spearman medio: **0,83**; el orden de magnitud de las columnas es casi idéntico en los
  seis (la columna 6 es la menor en 4/6; las columnas 7 y 10 son las mayores).
- El **valor 12.º es el más pequeño de su grupo en 6/6** (48, 14, 27, 19, 15, 23), mientras
  los otros 11 son 137–898: la columna 12 es otra cosa (¿un residuo, un contador, una
  unidad distinta?).

Esto es lo que cabría esperar de **seis mediciones de las mismas 11 categorías** en seis
unidades distintas (o seis periodos), no de seis listas independientes.

### 5.2 Periodicidad de color a 14 grupos

- Coincidencias exactas de color entre el grupo *g* y *g+14*: **16/66** (24 %), frente a un
  nulo de **3,83** (5,8 %): **p = 0,0005**. El lag 14 es el **primero de 79 lags**; el
  segundo es 28 (11 coincidencias, armónico).
- Restringido a los conjuntos C–F (g = 27…65): **14 coincidencias** frente a 2,26 del nulo
  (p = 0,0005).
- Robustez: agrupando los colores en familias (todos los marrones juntos), **43/66** frente
  a 30,4 del nulo (p = 0,0005). El patrón no depende de la notación fina de color.
- En los conjuntos C–F la correspondencia es casi perfecta en las ranuras 5, 6, 7, y en
  varias de las 9–13 (p. ej. g27–g41–g55–g69 son todos `0D`; g29–g43–g57 son todos `CB`;
  g36–g50–g64 son `HB` + fibra vegetal).

### 5.3 Los cuatro grupos de fibra vegetal

36, 50, 64, 78: diferencias **14, 14, 14**. Si los cuatro se eligieran al azar entre 80,
la probabilidad de formar una progresión aritmética de razón 14 es 38 / C(80,4) ≈
**2,4 × 10⁻⁵** (y ≈ 3 × 10⁻⁴ si se permiten las 13 razones posibles). Es el ancla material
(independiente del color) de la plantilla de 14.

### 5.4 Un posible par de cuentas paralelas: g18 y g58

Los grupos 18 (YB) y 58 (HB) tienen 10 valores cada uno:

```
g18: 22  23  34  33  43  10  16  45  55  142   (total 423)
g58: 20  34  35  41  45  11  15  46  56  105   (total 408)
```

r = **0,974**; **7/10** valores difieren en ≤2; diferencia media 6,5. Es el par con más
coincidencias entre los grupos de 10 valores; los pares de grupos 0D tienen diferencias
medias parecidas (2,6–4,4) pero sobre valores de 8–30 (escala 10 veces menor). La lectura
"cuenta duplicada/paralela" es **propuesta** (los colores difieren y no hay documento
externo); la similitud es **apoyada con datos**.

### 5.5 Otras regularidades

- La ranura 5 tiene **siempre 10 valores y la 11.ª cuerda vacía** (6/6).
- La ranura 6 tiene **siempre 12 cuerdas y 12 valores** (6/6).
- La ranura 8 tiene 6–10 valores, con media por cuerda 40–66 (C tiene solo 6 valores: 4
  cuerdas dañadas).
- El conjunto A es ~2–3× mayor que B–F en las ranuras 5 y 6 (558 vs 165–207; 5 766 vs
  2 695–3 500). No es la suma de los otros cinco (la suma de B–F es 936 y 15 747).

## 6. Anomalías y qué no encaja

1. **`p115` (grupo 10, valor 10):** un único nudo simple a **41,5 cm** del cordón (cuerda
   de 51,5 cm). La posición decimal normal de las decenas es ~10,5 cm; a 41,5 cm el nudo
   está en el extremo. Puede ser un 1 (unidad) mal posicionado o un nudo terminal, no un
   10. Es la lectura numérica más frágil del quipu.
2. **`p26` (grupo 2, valor 70):** el nudo de unidades tiene dirección **U** (el único de
   1 780). Dato incompleto, no anomalía de diseño.
3. **`p626` y `p781`:** union `?` y largo 0; conservan nudos (11 y 12). Falta el registro
   de unión/longitud.
4. **`p61` (grupo 5, 65):** "broken and retied recently"; valor potencialmente alterado.
5. **Cuerdas sin nudos: 727/954 (76,2 %).** No es solo daño: muchas tienen longitud normal
   (38–40 cm) y color cuidado. Es un quipu **mayoritariamente no anudado**.
6. **Grupos dañados:** 33 (8 cuerdas), 34 (7), 38 (8), 43 (6); en 34, 43 y 76 el largo
   medio es 0 (cuerdas rotas). Los cuatro grupos cortos caen en la ventana **33–43**, justo
   alrededor de la unión propuesta tras el clúster 39: consistente con la rotura, no con
   un diseño.
7. **Terminaciones R:** 9 cuerdas con terminación `R` (código no documentado en las
   fichas), todas vacías; sin impacto numérico.
8. **El 100 % verso no es señal:** 332/651 quipus del corpus tienen 0 cuerdas R; todas
   verso es frecuente. No se puede leer como "una sola mitad" hanan/hurin (la hipótesis
   R/V de Medrano y Urton 2018 no es aplicable aquí: no hay contraste).
9. **La fila de subsidiarias vacía** (11+11 en seis grupos) no tiene función numérica
   detectable; o es una segunda fila de la tabla, o un espacio reservado.

## 7. Lectura propuesta

**Tipo de registro: tabla administrativa de 6 unidades × 14 categorías × 11 subcategorías**
(no calendario, no "quipu narrativo").

- **Filas:** los **6 conjuntos** (A–F), cada uno de hasta 14 grupos (C–F completos). Por su
  tamaño y por la literatura de archivo para Ica/Pisco (Urton 2005: pares/duplicados en la
  colección de Berlín; AS159/AS173, AS114/AS123), lo más probable es que sean **6 unidades
  administrativas** (ayllus/parcialidades, o 6 revisiones de una misma unidad), no 6 años.
- **Columnas:** las **14 ranuras** de cada conjunto, identificadas por color y por una
  posición fija; cada ranura contiene **11 colgantes** (subcolumnas). Solo **5 ranuras**
  están cuantificadas: 2 (1 valor), 3 (4–5), 5 (10), 6 (12), 8 (10).
- **Contenido:** la ranura 5 suma ~180 por conjunto (165–207; A = 558); la ranura 6,
  ~3 000 (2 695–3 500; A = 5 766); la ranura 8, ~400 (242–538). La razón 6/5 es 16,3–17,6
  en B–F (CV 3,2 %), compatible con **un mismo colectivo medido en dos unidades** (p. ej.
  personas y bienes), pero **no demostrable** sin referente.
- **Lo que NO es:** no hay suma de colgantes, ni suma de grupos, ni cuerdas superiores, ni
  agregación vectorial. Es un **registro de valores yuxtapuestos**, no una hoja de cálculo
  que cuadre.

**Nivel de evidencia:** la plantilla 6×14 y los perfiles son **apoyados con datos**
(p = 0,001, Holm); la lectura "censo/tributo/depósito" es **propuesta**; la asignación de
filas a ayllus y de columnas a categorías concretas es **especulativa**.

**Contraste con la literatura.** Urton (2005) describe la colección de Berlín (Ica/Pisco)
como un archivo con **cuentas duplicadas/concordantes**; UR231 encaja en ese género por
tamaño, por la unión de dos fragmentos y por el par g18/g58. La nota del OKR ya dice
"sets of 14"; este análisis la cuantifica (14 grupos, 4 terminadores vegetales, color
periódico) y añade que **la aritmética invocada para la reconstrucción no se sostiene**.
Medrano y Khosla (2024) usan las 186 sumas como verosimilitud de la unión; aquí se muestra
que esas 186 son compatibles con azar, así que la unión debe defenderse por la plantilla de
color/fibra, no por las sumas.

## 8. Resultados negativos (explícitos)

1. **No hay sumas Ascher:** 1 adyacente (p = 0,95) y 11 intra-grupo (p = 0,38).
2. **No hay cuerdas superiores** (union T = 0): imposible testear "grupo = suma".
3. **No hay suma de subsidiarias:** 89/90 vacías; la única no cuadra.
4. **No hay jerarquía de totales:** 8 coincidencias triviales (p = 0,73); 0 coincidencias
   vectoriales.
5. **No hay exceso de valores repetidos:** 35 vs 35,9 (p = 0,99).
6. **No hay señal R/V:** 0 R, pero el 51 % del corpus también tiene 0 R.
7. **No hay dirección de nudo variable:** 1 779 Z y 1 U; el eje S/Z no informa.
8. **No hay estructura calendárica** detectable: 14 ranuras × 11 no se ajusta a meses,
   días ni años; los valores no son fechas ni múltiplos de 20/365.
9. **El "perfil compartido" no implica suma:** las columnas de la ranura 5 y de la ranura
   6 tienen perfiles distintos (r entre perfiles ≈ 0), así que no son la misma magnitud
   medida dos veces.

## 9. Tabla de niveles de evidencia

| Afirmación | Nivel |
|---|---|
| 954 cuerdas = 864 colgantes + 90 subsidiarias; 227 con nudos; 30/80 grupos con datos | **Demostrado** |
| Plantilla de 6 conjuntos × 14 ranuras, con ranuras 5/6/8 fijas | **Apoyado con datos** (p = 0,001; 4/4 conjuntos alineados C–F) |
| Periodicidad de color a 14 grupos | **Apoyado con datos** (p = 0,0005; resiste Holm y Bonferroni por 79 lags) |
| 4 grupos de fibra vegetal a 14 de distancia | **Apoyado con datos** (p ≈ 2,4 × 10⁻⁵; post hoc en d, pero d documentado) |
| Los seis grupos de 12 comparten 11 columnas (r = 0,915) | **Apoyado con datos** (p = 0,001) |
| No hay aritmética Ascher verificable | **Demostrado** (negativo; p = 0,38–0,95) |
| Las 186 sumas de KFG son artefacto | **Demostrado** (composición + nulos) |
| g18/g58 = cuentas paralelas/duplicadas | **Apoyado con datos** (similitud) / **propuesto** (interpretación) |
| Tipo de registro: tabla administrativa (censo/tributo/depósito) | **Propuesto** |
| Filas = 6 ayllus/parcialidades; columnas = 14 categorías; 11 subcategorías | **Especulativo** |
| El color es etiqueta de categoría, no valor numérico | **Propuesto** (monocromía por grupo + periodo) |

## 10. Para el coordinador

- **UR231 no es un quipu aritmético.** Las 186 "sumas pendant-pendant" que reporta KFG y
  que se citan para su reconstrucción se desmontan: 94 incluyen ceros, 56 usan ventanas de
  >20 cuerdas y la mitad cruzan grupos. Con la regla del brief (0 = ausente) quedan **1
  suma adyacente (p = 0,95)** y **11 intra-grupo (p = 0,38)**: azar puro.
- **Lo que sí tiene estructura es la plantilla:** 80 grupos ≈ **6 conjuntos de 14 ranuras**
  (la nota del OKR ya lo decía), con **cuatro grupos de fibra vegetal exactamente a 14 de
  distancia** (p ≈ 2,4 × 10⁻⁵) y **periodicidad de color a lag 14** (16/66 vs 3,8; p =
  0,0005). Es el hallazgo más sólido y el mejor argumento para la unión de los fragmentos.
- **Las ranuras 5, 6 y 8 están fijas en los cuatro conjuntos alineados (C–F):** 0D con 10
  valores
  (~180), grupo de 12 con 12 valores (~3 000) y grupo de 10 valores (~400). Los seis
  grupos de 12 comparten un perfil de 11 columnas (r = 0,915, p = 0,001): es compatible
  con **seis mediciones de las mismas 11 categorías**, no con seis listas independientes.
- **La 12.ª cuerda de esos grupos es siempre la más pequeña** (14–48 frente a 137–898):
  hay una columna "residual" que no es del mismo tipo que las otras 11. Merece mirada
  propia en la siguiente ronda.
- **Posible cuenta duplicada:** g18 y g58 (10 valores) tienen r = 0,974 y 7/10 diferencias
  ≤2. Encaja con el género de "cuentas concordantes" de Urton (2005) para la colección de
  Berlín; habría que buscar la cuenta concordante en el archivo de Berlín.
- **El 76 % de cuerdas no tiene nudos** (percentil 96,5), pero no es solo daño: muchas
  tienen longitud normal. Es un quipu **mayoritariamente de etiquetas de color**, no de
  números. Eso limita cualquier lectura numérica global.
- **El 100 % verso no informa:** 332/651 quipus del corpus también tienen 0 R; no se puede
  usar como marcador de mitad. La hipótesis R/V de Medrano–Urton 2018 no es testeable aquí.
- **Anomalías a revisar:** `p115` (nudo a 41,5 cm, valor 10 dudoso), `p26` (nudo U),
  `p626`/`p781` (unión `?`, largo 0), `p61` (roto y reatado). Los grupos 33, 34, 38 y 43
  (6–8 cuerdas) se concentran alrededor de la unión tras el clúster 39: la rotura es real.
- **Recomendación:** (a) no usar las 186 sumas como evidencia de reconstrucción; (b)
  contrastar la plantilla 6×14 contra los otros quipus grandes de Ica/Pisco (UR1109,
  UR1113, UR1114) y contra AS069; (c) buscar un referente documental (visita/revisita) para
  las ranuras 5/6/8; (d) revisar `p115` en el museo antes de fijar su valor.
