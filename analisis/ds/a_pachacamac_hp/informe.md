# Monografía del archivo de Pachacamac, serie HP (HP001–HP032)

**Equipo:** `analisis/ds/a_pachacamac_hp/`
**Datos:** `analisis/datos/cuerdas.csv`, `quipus.csv`, `grupos.csv` (Khipu Field Guide) +
`data/external/open-khipu-repository/data/okr-kh-numbers.csv`.
**Reglas:** unidad de análisis = quipu; nulo explícito; semilla 0; corrección múltiple;
resultados negativos; etiquetas de evidencia.

---

## 0. Pregunta

¿Qué es y qué registra el archivo de quipus del Museo de Sitio de Pachacamac,
serie HP001–HP032? En concreto:
1. Describir el conjunto (estructura, color, valores, sumas, uniones, torsión, dirección de nudo).
2. Buscar relaciones **entre** los quipus del archivo (valores/estructuras/colores compartidos) con nulo.
3. Reconstruir la jerarquía del archivo (quipus de detalle vs. de resumen).
4. Contrastar con la literatura del sitio y proponer qué se registraba.

---

## 1. Descripción del conjunto

Hay **32 quipus** (HP001–HP032) atribuidos al **Museo de Sitio de Pachacamac**
(`procedencia` = Pachacamac o Cieneguilla-Valle de Lurín para HP015/HP016; `museo` =
Museo de Sitio de Pachacamac en los 32). **Total: 1 202 cuerdas** (986 colgantes de nivel 0,
204 subsidiarias de nivel 1, 11 de nivel 2, 1 de nivel 3).

Tabla completa en `tabla_por_quipu.csv` (generada por `01_describe.py`). Resumen:

| kfg | cuerdas | grupos | sub | nudos | sin nudos | val min | val max | Σval | T | R | V |
|------|--------|-------|-----|-------|-----------|---------|---------|-------|---|---|---|
| HP001 | 14 | 6 | 0 | 14 | 0 | 1385 | 2973 | 28045 | 0 | 0 | 14 |
| HP002 | 31 | 2 | 1 | 30 | 1 | 20 | 5340 | 29080 | 0 | 30 | 0 |
| HP003 | 96 | 14 | 16 | 66 | 30 | 1 | 355 | 5023 | 0 | 80 | 0 |
| HP004 | 51 | 10 | 38 | 40 | 11 | 1 | 302 | 1344 | 0 | 0 | 17 |
| HP005 | 27 | 5 | 6 | 22 | 5 | 1 | 608 | 1177 | 0 | 22 | 0 |
| HP006 | 13 | 2 | 5 | 10 | 3 | 3 | 568 | 1941 | 0 | 0 | 8 |
| HP007 | 27 | 6 | 3 | 17 | 10 | 10 | 1743 | 6718 | 0 | 24 | 0 |
| HP008 | 18 | 1 | 6 | 16 | 2 | 1 | 433 | 2690 | 0 | 12 | 0 |
| HP009 | 13 | 1 | 8 | 11 | 2 | 1 | 243 | 367 | 0 | 4 | 5 |
| HP010 | 27 | 3 | 0 | 25 | 2 | 610 | 11540 | 63409 | 0 | 27 | 0 |
| HP011 | 43 | 3 | 15 | 35 | 8 | 2 | 2000 | 14856 | 0 | 43 | 0 |
| HP012 | 57 | 9 | 6 | 31 | 26 | 1 | 200 | 3496 | 0 | 57 | 0 |
| HP013 | 15 | 2 | 3 | 8 | 7 | 1 | 90 | 414 | 0 | 0 | 13 |
| HP014 | 64 | 16 | 5 | 44 | 20 | 1 | 272 | 1107 | 0 | 61 | 0 |
| HP015 | 9 | 3 | 0 | 3 | 6 | 14 | 24 | 55 | 0 | 2 | 7 |
| HP016 | 12 | 1 | 8 | 9 | 3 | 2 | 7 | 33 | 0 | 3 | 0 |
| HP017 | 136 | 19 | 36 | 107 | 29 | 1 | 155 | 4386 | 0 | 0 | 102 |
| HP018 | 35 | 9 | 7 | 24 | 11 | 1 | 88 | 434 | 0 | 27 | 0 |
| HP019 | 22 | 4 | 0 | 10 | 12 | 1 | 6 | 31 | 0 | 22 | 0 |
| HP020 | 29 | 5 | 3 | 24 | 5 | 1 | 12 | 91 | 0 | 0 | 26 |
| HP021 | 9 | 1 | 1 | 9 | 0 | 1 | 3236 | 3501 | 0 | 0 | 8 |
| HP022 | 18 | 2 | 0 | 18 | 0 | 1 | 83 | 314 | 0 | 18 | 0 |
| HP023 | 31 | 4 | 11 | 23 | 8 | 2 | 400 | 1271 | 0 | 20 | 0 |
| HP024 | 7 | 2 | 3 | 6 | 1 | 3 | 460 | 1277 | 0 | 0 | 4 |
| HP025 | 55 | 12 | 0 | 0 | 55 | – | – | – | 0 | 55 | 0 |
| HP026 | 17 | 4 | 0 | 0 | 17 | – | – | – | 0 | 17 | 0 |
| HP027 | 76 | 6 | 23 | 65 | 11 | 66 | 39263 | 198386 | 0 | 55 | 0 |
| HP028 | 10 | 1 | 0 | 0 | 10 | – | – | – | 0 | 10 | 0 |
| HP029 | 67 | 13 | 4 | 45 | 22 | 4 | 2963 | 16404 | 0 | 0 | 62 |
| HP030 | 110 | 12 | 3 | 103 | 7 | 100 | 2783 | 52916 | 0 | 108 | 0 |
| HP031 | 48 | 6 | 5 | 42 | 6 | 1 | 8 | 76 | 0 | 43 | 0 |
| HP032 | 15 | 4 | 0 | 10 | 5 | 3 | 72 | 149 | 0 | 0 | 15 |

### Rasgos del conjunto

- **Torsión: S en las 1 197 cuerdas con dato** (5 sin dato). NO hay Z ni U. Uniforme.
- **Unión al cordón principal: 0 cuerdas superiores (union T).** R = 740, V = 281,
  U/Unknown/? = 181. Es decir, **ningún quipu HP usa unión T**: el archivo no conserva
  cuerdas superiores → no hay "cuenta de cuenta" dentro de cuerdas; las sumas, si existen,
  son horizontales (una colgante = Σ subsidiarias, o grupo = grupo).
- **Terminación:** K (nudo/ojal terminal?) 760, B 367, U 70, sin dato 5.
- **Dirección de los racimos de nudo:** Z = 1 660 vs S = 59 vs U = 3. Igual que el patrón
  general del KDB (Clindaniel 2019): **Z domina**.
- **Tipos de racimo:** S simple 998, L largo 549, E figura de ocho 175 (nudos "no decimales"
  tipo STRING son escasos).
- **Colores** (80 códigos distintos; base más frecuente): W blanco 648, MB marrón medio 186,
  AB marrón claro 147, KB marrón oscuro 81, RM/RB rojos 83, GG 15. Predomina el **blanco con
  mezclas blanco-marrón** (W%MB, W%AB, W:MB): paleta monocroma con pares claro/oscuro.
- **Valores** (867 cuerdas con nudo): mediana 66, máx 39 263 (HP027); solo **20,8 %**
  múltiplos de 10 y 5,3 % terminan en 5 → mezcla de números "coherentes" (1, 2, 100) y
  valores atípicos (HP001: 1385–2973; HP010: ≥610; HP021: 3236; HP027: hasta 39 263).
- **Quipus vacíos (sin nudos):** HP025 (55 cuerdas), HP026 (17), HP028 (10). Son cuerdas
  presentes pero sin nudos → probablemente "vacíos de datos" o marcadores de posición.

> **Nivel de evidencia:** descripción = **bien apoyado** (lectura directa de los datos) para
> torsión, unión, dirección y conteos; **apoyado con datos** para la lectura funcional de
> los quipus vacíos.

### 1.1 Dos pares de quipus son el MISMO objeto físico

`okr-kh-numbers.csv` asigna a **HP001 y HP002** el mismo número de registro
**RN 43366** (MSP 1385A y MSP 1385B) y a **HP029 y HP030** el mismo **RN 43406**
(MSP 1425A y MSP 1425B). Es decir, el archivo tiene **30 objetos físicos distintos**,
no 32: HP001+HP002 y HP029+HP030 son dos mitades (A/B) de sendos quipus partidos.
Esto importa para la pregunta 2: cualquier "relación" HP001–HP002 o HP029–HP030 es
trivial (son el mismo objeto) y **no debe contarse como hallazgo**. Los totales no
coinciden exactamente (HP001 Σ=28 045 vs. HP002 Σ=29 080; HP029 Σ=16 404 vs.
HP030 Σ=52 916), así que no son "mitad y mitad" aritméticas.
**Nivel: bien apoyado** (número de registro compartido).

---

## 2. Relaciones entre los quipus (con nulo de permutación)

Método: 496 pares; se barajan los valores (o los colores) **dentro de cada quipu**
500 veces, semilla 0, y se recalcula la métrica. Se comparan 6 métricas y se corrige
por comparaciones múltiples con **BH-FDR**.

| Métrica | obs | nulo media ± sd | p (1-col.) | BH-FDR |
|---|---|---|---|---|
| A. Valores alineados en la misma posición ordinal | 132 | 108,7 ± 10,3 | 0,020 | **0,12** |
| B. Σ de un grupo de A = valor de otro quipu B | 304 | 295,7 ± 26,9 | 0,357 | 0,43 |
| B2. Cuerda contigua (ventana≤12) = otra cuerda (interno) | 1223 | 1169 ± 41,3 | 0,108 | 0,32 |
| C. Estructura de grupos idéntica (vector cuerdas/grupo) | 0 pares | – (exacto) | – | – |
| D. Colores base alineados por posición | 3660 | 3731,8 ± 70,5 | 0,852 | 0,85 |
| Seriación de valores dentro de grupo | 16/166 | 12,9 ± 3,1 | 0,208 | 0,42 |
| Banding de color (adyacentes iguales) | 239/1170 | 230,1 ± 10,6 | 0,216 | 0,43 |

**Ninguna métrica sobrevive a la corrección BH-FDR** (el p ajustado más bajo es 0,12).
Es decir: **no hay evidencia de que los quipus HP compartan secuencias de valores,
sumas cruzadas, estructuras de grupo ni patrones de color más allá del azar.**
La única señal marginal (métrica A) es un **artefacto**: al exigir valores ≥2/≥10/≥100,
los pares alineados caen de 81 a 19 y a 8; de las 8 coincidencias posicionales de
HP014–HP031, **7 son el valor 1** (HP031 tiene 34 de sus 48 cuerdas con el valor 1).
Con valores informativos la señal desaparece.
**Nivel: bien apoyado (negativo).**

### 2.1 Jerarquía de archivo (detalle vs. resumen)

- **Dentro de cada quipu:** hay **0 cuerdas superiores** (union T) en todo el archivo,
  así que no existe la estructura "cuerda resumen del grupo". `cuerda = Σ subsidiarias
  directas` solo se cumple en **3 casos triviales** (una sola subsidiaria; HP005 p16=1,
  HP014 p18=2, HP020 p11=2). Las sumas de ventanas contiguas (B2) no superan el nulo.
- **Entre quipus:** los "totales" de un quipu que cuadran con sumas de 2–4 totales de
  otros son **coincidencias combinatorias**, no jerarquía: p. ej. HP003 Σ=5023 =
  HP005+HP019+HP021+HP022, y HP029 Σ=16404 = HP004+HP011+HP015+HP032. Con 32 totales y
  C(32,3)+C(32,4) ≈ 40 000 combinaciones, los cuadres exactos son esperables; **el nulo
  por permutación no sirve aquí** porque barajar dentro del quipu no cambia el total.
- **Conclusión:** **no se reconstruye una jerarquía de archivo** (no hay quipus de
  "resumen" que agreguen sistemáticamente a otros). El archivo es un conjunto de
  registros independientes. **Nivel: apoyado con datos (negativo).**

---

## 3. Qué se registraba aquí: indicios internos

- **Dos registros de escala distinta.** Por mediana de valor: un grupo de "números
  grandes" (HP001 1878, HP010 1301, HP027 366, HP030 266, HP002 230, HP011 140) frente a
  una mayoría de "números pequeños" (mediana ≤ 30, con muchos 1–10). HP001 (14 cuerdas,
  todas entre 1385 y 2973) es un caso extremo de registro de magnitudes altas.
- **Quipus sin nudos** (HP025, HP026, HP028) y una alta tasa global de cuerdas sin nudo
  (335/1202 ≈ 28 %, coherente con el ~30 % del corpus).
- **Sin seriación ni banding significativos**; el patrón seriado de HP017 (90,32,56,…)
  no se generaliza al archivo.
- **Colores monocromos** (blanco dominante + pares marrón claro/medio): paleta
  compatible con "categorías por color" más que con un código multicolor.

---

## 4. Contraste con la literatura del sitio

- La **serie HP = catálogo de Héctor Pereyra**, autor de *Quipus del Museo del Sitio
  Pachacamac* (citado en `docs/fichas/repo-khipuanalysis.md` y
  `2025-Thompson-ascher-corrections.md`); el museo tiene **32 objetos KH, los 32 con
  datos** (`docs/estado_del_arte.md`, tabla de instituciones), exactamente HP001–HP032.
- **Urton (2017, *Inka History in Knots*)** trata *archivos* de Pachacamac (valle de
  Lurín) junto a Puruchuco, Chachapoyas e Inkawasi como **registros de censo y tributo**
  de los quipucamayoc (`docs/fichas/2017-Urton-inka-history-knots.md`). Esto respalda
  leer el archivo HP como **contabilidad administrativa / población** más que como
  calendario.
- **Clindaniel (2019)** confirma que en Pachacamac (n=91, incluye UR/AS/HP) **domina la
  dirección Z** y que los patrones de color del KDB reproducen combinaciones de los
  "wrapped sticks" (Monte Carlo p<0,01). Nuestro dato (Z=1660 vs S=59 en HP001–032) es
  **consistente** con ese control independiente → **apoyado con datos**.
- **Saez-Rodríguez (2013, VA 42527, de Pachacamac)** propone un calendario lunar de maíz,
  pero su ficha lo marca **especulativo** (n=1, regresión de 7 puntos, selección post
  hoc de divisores). Nuestro archivo **no aporta** el patrón calendárico esperado
  (ni seriación ni banding significativos), lo que **debilita** esa lectura como
  generalización al archivo.
- **FitzPatrick / Medrano** (valle del Santa) y la contabilidad jerárquica de
  **Puruchuco (Urton 2005/2017)** sí documentan quipus con cuerdas superiores y sumas;
  el archivo HP **carece por completo** de union T, por lo que **no replica** ese género
  de "cuenta de cuentas".

**Propuesta (nivel: propuesto, no bien apoyado):** el archivo HP001–HP032 es una
**serie de registros administrativos independientes** (probable censo/tributo o listas
de cantidades) sin estructura jerárquica conservada; la ausencia de cuerdas superiores
y de relaciones cruzadas sugiere que **la jerarquía (si la hubo) se perdió o residía en
el cordón principal/organización física**, no en las cuerdas. La escala bimodal
(registros de unidades pequeñas vs. un puñado de magnitudes altas) es compatible con
"listas de detalles" frente a "consolidados de un solo nivel".

---

## 5. Resultados negativos (explícitos)

1. **0 cuerdas superiores (union T)** en los 32 quipus — no hay jerarquía vertical interna.
2. **Ninguna relación entre quipus sobrevive BH-FDR** (valores, sumas, estructura de
   grupos, color).
3. **Estructuras de grupo idénticas: 0 pares.**
4. **Sin seriación (p=0,21) ni banding de color (p=0,22)** por encima del nulo.
5. La señal de "valores alineados" es artefacto del valor 1.
6. **Torsión uniforme S (1197/1197)**: no hay variación de torsión que explotar.

---

## 6. Para el coordinador

- **El archivo HP = 30 objetos físicos, no 32**: HP001+HP002 comparten RN 43366 (MSP 1385
  A/B) y HP029+HP030 comparten RN 43406 (MSP 1425 A/B). Cualquier relación entre esos
  pares es trivial; que el resto de equipos lo excluyan antes de "descubrir" un hallazgo.
- **Es la serie de Pereyra en el Museo de Sitio de Pachacamac** (32 objetos KH, los 32
  con datos según la tabla institucional del estado del arte); unidad = quipu, 1202 cuerdas.
- **Hallazgo negativo principal: no hay relaciones entre quipus.** 6 métricas (valores
  alineados, sumas de grupo cruzadas, sumas contiguas internas, estructura de grupos,
  color alineado, seriación/banding) → el p ajustado más bajo es **BH-FDR = 0,12**. Es un
  conjunto de registros independientes, no un archivo jerárquico.
- **Sin cuerdas superiores (union T=0) y sin sumas internas reales** (solo 3 casos
  triviales de 1 subsidiaria): **no replica** el género "cuenta de cuentas" de Puruchuco.
  La jerarquía de detalle/resumen **no está en las cuerdas**.
- **Control independiente que sí valida:** dirección de nudo **Z=1660 vs S=59**, torsión
  **S=100 %**, coherente con Clindaniel (2019) para Pachacamac. Los patrones de color
  (blanco dominante + pares AB/MB) son compatibles con los "wrapped sticks".
- **Dos registros de escala**: mayoría con valores 1–30 y un grupo de magnitudes altas
  (HP001 ~1900, HP010 ~1300, HP027 hasta 39 263). Sugiere mezcla de "detalle" y
  "consolidado" de un solo nivel.
- **Lectura propuesta (nivel: propuesto):** registros administrativos de censo/tributo
  (como propone Urton 2017 para Pachacamac), **no** un calendario (la hipótesis
  calendárica de Saez-Rodríguez es especulativa y no reaparece aquí).
- **Recomendación siguiente ronda:** (a) cruzar HP con el OKR/KDB para confirmar que no
  hay duplicados HP↔UR/AS (la tabla KH ya muestra el puente); (b) buscar información NO
  en los valores sino en el **cordón principal** (pc_largo, pc_color, pc_estructura) y en
  la **posición física** de los grupos, donde puede residir la jerarquía perdida;
  (c) tratar HP001+HP002 y HP029+HP030 como objetos únicos al comparar con otros archivos.

*Scripts reproducibles: `01_describe.py`, `02_stats.py`, `03_relations.py`, `04_diag.py`,
`05_sums.py`, `06_features.py`. Tablas: `tabla_por_quipu.csv`, `pares.csv`. Semilla 0.*
