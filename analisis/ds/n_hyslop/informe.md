# Inkawasi (Hyslop 1985): sectores, almacenes y las 9 partes de los quipus

**Equipo:** n_hyslop · **Fecha:** 2026-10-18 · **Semilla:** 20261018
**Fuentes primarias:** Hyslop 1985, *Inkawasi: The New Cuzco* (texto completo en `analisis/fuentes_txt/Hyslop1985_Inkawasi.txt`, leído por tramos); Urton & Chu 2015, *Accounting in the King's Storehouse* + Apéndice I; Urton 2017, cap. 9; LeVine (ed.) 1992; `analisis/SINTESIS.md`; `analisis/ds/n_rejilla/`; `analisis/ds/n_almacenes/`.
**Salidas:** `sectores.csv`, `quipus_ua.csv`, `capacidad_escenarios.csv`, `logistica_mita.csv`, `logistica.csv`, `control_multiplos.csv`, `control_cortes.csv`, `salida_01.txt`–`salida_03.txt`, scripts `01_sectores.py`, `02_pruebas.py`, `03_logistica.py`.

---

## 1. Pregunta

¿La arquitectura de Inkawasi —y en particular la organización de sus depósitos— ofrece un modelo de 9 partes, de mitades o de cuartos que pueda corresponder a las 9 columnas de UR278/UR270? ¿Dónde estaba exactamente la kallanka U.A. 4 de los 14 quipus cubiertos de maní? ¿Qué productos, duración de ocupación y población implica el sitio, y cómo contrasta con los escenarios de 54–5.600 mitayos de `n_almacenes`?

## 2. Método

1. **Lectura dirigida, no masiva.** Se usó `grep -n` sobre Hyslop para localizar Sector A, los sectores B–H, el capítulo 4 (diseño simbólico) y los pasajes de población/ocupación; se leyeron tramos de ≤80 líneas. No se imprimió el libro completo.
2. **Dos escalas separadas.** (a) El sitio: conteos de cuartos, medidas, volumen y división simbólica. (b) El libro: perfil de las 9 columnas de UR278 (`n_rejilla/rejilla.csv`, 28 registros). No se mezclan: un conteo arquitectónico no es una prueba de un patrón de cuerdas.
3. **Nulo explícito en cada prueba de correspondencia.** T1 (4+5), T3 (gradiente) y T1b (cortes) permutan etiquetas de columna *dentro de cada registro* de UR278, preservando el total de la fila y la estructura de los 28 registros. T2 (3×3) es una F anidada sobre log-proporciones que compara el modelo de 3 bloques con el de 9 columnas libres. Es una prueba interna al libro, no una prueba poblacional entre quipus; UR270 se usa solo como réplica descriptiva (6 filas completas, 5 de 7 registros repetidos, no independiente).
4. **Corrección múltiple.** Holm para T1–T3 (4+5, 3×3, gradiente). Holm separado para los 8 puntos de corte contiguos. Se declara cuando algo no sobrevive.
5. **Control de apofenia.** Se contaron 13 conteos arquitectónicos independientes y se preguntó cuántos son múltiplos de 9, 7, 5, 6, etc., comparando con un nulo binomial y Monte Carlo uniforme 1–250. Es un control de escepticismo, no una prueba de intención.
6. **Etiquetas:** demostrado / apoyado con datos / propuesto / especulativo. La aritmética de capacidad se marca como cálculo con supuestos, no como test.

## 3. Sectores, cuartos y volumen

La tabla completa está en `sectores.csv`; aquí va lo esencial.

| Sector | Función | Cuartos de almacén | Medidas / disposición | Volumen |
|---|---|---|---|---|
| **A (Qolqawasi)** | Almacén estatal; recepción, conteo y depósito | **202–250 bins cuadrados + 36 cámaras rectangulares** | 110 × 110 m; bins de 3,5–4,5 m de lado y ~2 m de alto; una sola entrada (NO); plataforma central | **6.400 m³** (bins cuadrados); hasta ~11.600 si se suman las 36 cámaras |
| A1 | Kallankas + secaderos: recepción y contabilidad inicial | 4 kallankas (U.A. 1, 2, 4, 5) + 2 secaderos (U.A. 7, 8) | 2 kallankas + 1 secadero por lado del corredor U.A. 3; secaderos con 30 paneles de 3×39 cuadros de 23 cm = 3.510 cuadros | no computado |
| A2 | Cámaras grandes (¿almacén o secado/conteo?) | **36 = 4 × 9** | **18 por lado; 9 exteriores más cortas y 9 interiores más largas**; 2 filas de 9 por lado del eje | 0–5.184 (si son almacén) |
| A3 | Bins pequeños de almacén | **209** (Hyslop: 202–250) | 3,5–4,5 m de lado; 3 lados (O, S, E); filas múltiples | 5.120–8.464; **6.400 con el bin medio (3,9 × 3,9 × 2,0 m)** |
| B | Residencia de élite; posible templo de Wiracocha | 0 | 200 × 100 m; ≥120 cuartos; 4–5 compuestos | 0 |
| C | Ceremonial: plaza trapezoidal, posible Templo del Sol, entierro, corrales | 0 | 110 × 100 m; ~25 cuartos; 11 recintos de 7–13 m; plaza con 20 columnas | 0 |
| D | Residencia de baja condición y cocina | 0 | 200 m; ~120 cuartos; muros ≤40 cm | 0 |
| E1 | Complejo administrativo/ceremonial; posible almacén diversificado | 96 (no confirmado) | 100 m de ancho; 7 filas de cubículos; columnas cada 3,2 m | desconocido |
| **E2** | Cuartos ceremoniales/administrativos | **9 = 4 + 5** | Estructura cuadrada de 4 cuartos + rectangular de 5; pasillo alineado con el ushnu | 0 |
| F1 | Residencia de estatus intermedio; almacén ocasional | 0 | 120 m de ancho; 14 unidades de 3–4 cuartos = 42–56 cuartos; 3 niveles | 0 |
| G | Almacén | **≥63** (+5 al O de C) | 100 × 200 m; cuartos cuadrados sin puertas en filas | 1.544–2.552 (estimación propia) |
| H | Puesto de observación | 0 | 35 × 40 m; ~7 cuartos | 0 |
| **Total** | A + G (+E1 posible) | **265–313**; 308 en el punto medio | — | **7.944–16.200** según escenarios |

**Consistencia interna.** Sumando los puntos medios (A 245, B 120, C 25, D 120, E 105, F 49, G 63, H 7) salen **734 cuartos**, de los cuales A+G = **308 = 42 %**. El rango con los extremos es 39–45 %. Esto cae dentro de la estimación de Hyslop de que **entre un tercio y la mitad** de los cuartos del sitio eran almacén (Hyslop 1985:31). Es un control de coherencia, no una prueba independiente: los conteos salen de la misma descripción.

### 3.1 El dato que corrige a `n_almacenes`: 6.400 m³ no es la suma de 36 cámaras + 209 colcas de 2 × 2 m

Hyslop calcula **6.400 m³ “dentro de los *square storage bins*”** (1985:99). El texto no da la fórmula. Hay dos lecturas geométricamente compatibles:

- **(a) 209 bins × 30,6 m³ = 6.400 m³.** Es la lectura literal: los *square bins* son A3 (209), de 3,5–4,5 m de lado y ~2 m de alto. Un bin medio de 3,9 × 3,9 × 2,0 m da exactamente 30,4 m³.
- **(b) 245 unidades × 26,1 m³ = 6.400 m³.** Incluye las 36 cámaras rectangulares, con un bin medio algo menor (3,6 × 3,6 × 2,0 m).

`n_almacenes` eligió una tercera descomposición: 36 cámaras de 112–148 m³ + 209 colcas de **2 × 2 m** con 1,3–1,8 m de carga (5,2–7,2 m³). Esa descomposición **no es compatible con Hyslop**: 2 × 2 m = 4 m², mientras que 3,5–4,5 m de lado = 12,25–20,25 m². Las colcas pequeñas tienen **3,4–7,8 veces el volumen** que les supuso `n_almacenes`. Con las dimensiones de Hyslop, las 209 colcas solas ocupan **5.120–8.464 m³**, y **6.400 m³ cae dentro de ese rango** (209 × 30,6 = 6.400). Es decir, consumen todo el 6.400. Las 36 cámaras grandes tienen que estar **fuera** de ese cálculo (o no ser almacén). No pueden sumarse dentro de él.

**Ambigüedad que no puedo resolver con el texto:** Hyslop cuenta 202–250 “square structures” y, aparte, ≥30 “rectangular enclosures”; Urton & Chu cuentan 209 *small square* + 36 *large rectangular* = 245. Si los 36 estuvieran incluidos en los 202–250, el total de A sería 202–250, no 238–286; pero entonces los 209 bins “pequeños” tendrían que ser mucho menores que los 3,5–4,5 m que Hyslop describe, que es justo lo que no está documentado. La separación 209 + 36 es la de Urton & Chu; el 6.400 sigue siendo un piso y el argumento principal no cambia, pero el total de A queda entre 202 y 286 unidades según esa lectura. Además, las medidas de Hyslop parecen de planta y posiblemente exteriores; si se descuenta el muro, el volumen por bin baja, pero no hasta los 5–7 m³ que supuso `n_almacenes`.

Consecuencia: **6.400 m³ es un suelo, no un valor central**. Los escenarios quedan así (`capacidad_escenarios.csv`):

| Escenario | m³ | Supuesto |
|---|---:|---|
| S1: solo A, lectura literal de Hyslop | **6.400** | 6.400 para los *square bins* |
| S2: A3 geométrico | **5.120–8.464** | 209 bins de 3,5–4,5 m × 2 m |
| S3: A3 + A2 si A2 es almacén | **9.332–13.648** | 36 cámaras de 15 × 6 m × 1,3–1,6 m |
| S4: sitio A + G, con A2 almacén | **10.876–16.200** | S3 + 63 cuartos de G |
| S5: sitio A + G, sin A2 | **7.944–8.952** | 6.400 + G |
| **Central** | **≈8.300–13.000** | A3 6.400 + G ~1.900; + A2 ~4.700 |

El rango de `n_almacenes` (5.000–14.000 m³) no es absurdo, pero su **6.400 central es el piso de A**, y su techo de 14.000 no es el techo real (16.200 si A2 y G cuentan). La consecuencia para la unidad: la cota inferior de masa unitaria de `n_almacenes` (3,4–10,4 kg) baja a **≈2,6–8,0 kg con 8.300 m³**, **≈2,0–6,1 kg con 10.900 m³** y **≈1,3–4,1 kg con 16.200 m³** (en todo el rango, 1,3–8,0 kg). Las raciones de 0,7 kg/día siguen por debajo, pero ya no por un factor 10, sino por **2–11**. La conclusión principal de `n_almacenes` —la unidad es un **volumen** (saco de 30–55 L), no una masa fija— no se ve afectada; es más, el grid de 23 × 23 cm y los paneles de 3 × 39 cuadros apuntan a una unidad volumétrica/área estandarizada.

**Nivel:** la incompatibilidad geométrica de la descomposición de `n_almacenes` es **demostrado** (aritmética con las medidas de Hyslop). Que el total real sea 8.300–13.000 es **propuesto** (depende de si A2 y G son almacén). Que 6.400 sea el piso de A es **apoyado con datos**.

## 4. ¿Hay un Inkawasi de 9 partes?

### 4.1 Lo que Hyslop dice del diseño simbólico

Hyslop propone un sitio dividido en **dos mitades (hanan/hurin)** y **cuatro suyus**, no en nueve:

- “The plan... shows Inkawasi divided into four parts... The broad solid line divides the Hanan division from the Hurin division... The double line... creates four parts or suyu: Anti Suyu... Qolla Suyu... Kunti Suyu... Chincha Suyu” (1985:45–46).
- El sistema de ceques de Cuzco, que Hyslop usa como modelo, tiene “divisions into parts of **two, four, three, and nine**” (1985:52). Pero el **9 no se aplica al plano del sitio**: los tres suyus distintos de Kunti Suyu tienen “nine lines in groups of three”; **Kunti Suyu tiene 2 divisiones de 7 líneas = 14 unidades**, y Hyslop identifica Sector F Zone 1 con esas **14 unidades arquitectónicas**, no con 9 (1985:53–54).
- Hyslop es explícito sobre la flexibilidad: los incas “manipulated the concepts of bi-, tri-, and quadripartition” y “this scheme is only one way of comprehending Inkawasi's symbolic design” (1985:46). Es una advertencia contra leer cualquier número como intención.

**Las alineaciones astronómicas no añaden un 9.** El corredor central de Sector A y su plataforma tienen una orientación de **155°08'** y apuntan al paso más bajo del horizonte, donde Hyslop sitúa el ascenso de la Vía Láctea y de las constelaciones llama/yutu; la misma orientación se prolonga en los muros de los bins y en Sector B (1985:62–63). El edificio principal de E se alinea con el ocaso cenital; la plaza trapezoidal de C con el ascenso de las Pléyades (67°53'); el corredor de F con 154°30'. Son ejes de una línea, no una retícula de 9. El corredor de 155°08' es el eje central de Sector A; la pila de 7 quipus apareció en el corredor norte **U.A. 3**, que corta ese eje en ángulo recto. El archivo está en la zona de recepción norte, no en un sector 9.

**Nivel:** la división en 2 + 4 y la asignación de 14 unidades a Kunti Suyu son **demostrado** (texto explícito). Que el sitio *no* tenga una división en 9 es **apoyado con datos** (Hyslop no la propone y su modelo la excluye).

### 4.2 Los 9 que sí existen en la arquitectura

| 9 potencial | Dónde | Comentario |
|---|---|---|
| **36 = 4 × 9** | A2: 36 cámaras rectangulares | 18 por lado = 2 × 9; 9 exteriores cortas + 9 interiores largas |
| **18 = 2 × 9** | A2, por lado del eje | 2 filas de 9; la fila de 9 es la unidad repetida |
| **9 = 4 + 5** | E2: 4 cuartos + 5 cuartos | Pasillo alineado con el ushnu; Hyslop: “suggests some symbolic content” |
| **63 = 7 × 9** | G: ≥63 cuartos | 7 filas de 9, o 9 de 7; el texto no da filas |
| **3 × 3 = 9** | Ceques de Cuzco: 3 suyus × 9 líneas en grupos de 3 | Modelo textual, **no** aplicado al plano de Inkawasi |
| 209 | A3 | **11 × 19**, no múltiplo de 9 |
| 245 | Total A | **5 × 7²**, no múltiplo de 9 |
| 96 | E1 | **3 × 32**, no múltiplo de 9 |
| 30 | “Rectangular enclosures” de A | **3 × 10**, no múltiplo de 9; Hyslop duda que sean almacén |
| 14 | F1 (Kunti Suyu) | **2 × 7**, no 9 |

**Lo que el texto no permite contar.** Solo A2 permite contar por fila: 18 cámaras por lado = 2 filas de 9 (9 exteriores cortas + 9 interiores largas). Hyslop **no publica el número de filas por lado de A3** (solo dice “rows” en tres lados) ni el número de filas de G (solo “at least 63” en dos montículos). Cualquier “9 por fila” en A3 o G es una conjetura, no un dato. La única fila de 9 documentada es la de A2, y su noveno elemento no es una división social ni un sector: es una cámara de almacén.

**El control de ubicuidad.** Si se toman 13 conteos independientes (4 kallankas, 2 secaderos, 18 cámaras/lado, 209 bins, 96 cubículos, 9 cuartos E2, 63 G, 30 recintos, 14 unidades F, 7 H, 25 C, 120 B, 120 D), **3 son múltiplos de 9** (18, 9, 63), frente a **1,44 esperados**; p binomial = **0,169**, p Monte Carlo = **0,158** (`control_multiplos.csv`). No hay exceso. Más aún: los múltiplos de **6** dan p = 0,051 (18, 96, 30, 120, 120) y los de **12** p = 0,088 (96, 120, 120), mejores que el 9. El 5 da p = 0,253. Es decir: con este método, **el 9 no es el número más “especial” del sitio**; el 6/12 lo es más. Es exactamente lo que se espera de un edificio con muchos conteos redondos.

**Nivel:** que 36, 18 y 63 sean múltiplos de 9 es **demostrado** (aritmética). Que eso indique una intención simbólica de 9 partes es **especulativo** y el control lo debilita (p = 0,17).

### 4.3 Las pruebas contra las correspondencias concretas

Se probó el perfil de las 9 columnas de UR278 (26 filas completas de `13_sistema_incahuasi/ur278_tabla.csv`; medias c1…c9 = 0,1348, 0,1398, 0,0968, 0,1073, 0,1164, 0,1294, 0,1070, 0,0798, 0,0888; la firma de `firma_9_partes.csv`, calculada con 27–28 filas por columna, difiere en ≤0,004) contra las tres lecturas arquitectónicas posibles:

| Prueba | Estadístico | p sin corregir | p Holm | Veredicto |
|---|---|---:|---:|---|
| **T1: 4 + 5** (E2: c1–c4 vs c5–c9) | diferencia = 0,0154 | 0,270 | 0,270 | **no** |
| **T2: 3 × 3** (bloques contiguos c1–c3, c4–c6, c7–c9) | F = 6,78; R² 9 libres = 0,307 vs 3 bloques = 0,167 | **< 10⁻⁵** | **< 10⁻⁵** | **rechazado** |
| **T3: gradiente** (una fila de 9 depósitos que decrece) | ρ Spearman = −0,733 | 0,031 | **0,061** | **no sobrevive** |
| **T1b: escaneo de los 8 cortes contiguos** | 8 pruebas; el mejor p = 0,015 (corte tras c7) | — | **0,118** | **ninguno** |
| T1c: réplica en UR270 (6 filas) | diferencia 4+5 = 0,0263 | 0,177 | — | misma dirección, no significativa |

**Lectura.** El 4+5 de E2 es solo uno de los ocho cortes posibles y no se distingue (p = 0,27). El 3×3 contiguo —la lectura que sugiere “nueve líneas en grupos de tres”— **se rechaza con fuerza**: explica la mitad de la varianza que las 9 columnas libres (R² 0,167 vs 0,307; F = 6,78, p < 10⁻⁵). El gradiente es sugestivo (las columnas finales son menores), pero no significativo tras Holm (p = 0,031; Holm 0,061) y está roto por c6, que es la tercera columna más grande. Un escaneo de todos los cortes no encuentra ninguno (Holm mínimo 0,118).

**Exploratorio, no prueba:** la mejor partición posible en 3 bloques de 3 (de las 280) sube el R² solo a 0,271 (vs 0,307 de las 9 libres) y **no es contigua**: agrupa (c1, c2, c6), (c4, c5, c7) y (c3, c8, c9). Es decir, agrupa las **tres columnas más grandes** (c1, c2, c6); es un efecto de magnitud, no de tríadas de ceques. No se usa como evidencia.

**Nivel:** que las 9 columnas no se reduzcan a 4+5 ni a un gradiente monótono es **apoyado con datos** (no significativos tras Holm); que el 3×3 contiguo no las explique es **apoyado con datos** (p < 10⁻⁵, solo para tríadas contiguas). Que el 9 sea una categoría interna del libro, no un mapa del sitio, es **propuesto**.

### 4.4 El negativo espacial más importante

Los **dos únicos libros de 9 partes identificados en Incahuasi** (UR270 y UR278) se encontraron **los dos en la kallanka U.A. 4**, dentro del grupo de 14 quipus cubiertos de maní. **No** se encontraron en E2 (los 9 cuartos 4+5) ni en las filas de 9 cámaras de A2. La probabilidad de que ambos caigan en la misma estructura por azar, con los tamaños observados (15, 7, 5, 2), es **0,337**; de que ambos caigan justo en U.A.4, **0,259**. No es significativo, pero el hecho descriptivo es claro: **el formato de 9 partes está concentrado en un solo archivo, no repartido por el sitio**.

Esto refuta la versión fuerte de “las 9 partes = 9 sectores/9 depósitos del sitio”. La versión débil —“las 9 partes son una categoría contable interna, usada por un mismo equipo de contadores”— es compatible con todo lo anterior y es la que queda en pie.

## 5. La kallanka U.A. 4 y los 14 quipus del maní

### 5.1 Qué dice cada fuente

- **Urton & Chu 2015:519, 521:** “14 samples were found in the southwest corner of kallanka **U.A. 4** covered with peanuts”; “Both are from a group of 14 khipus found in kallanka **U.A. 4** covered with peanuts” (UR266 y UR268). Es la fuente que pide la tarea.
- **Apéndice I de 2015:** lista 15 quipus en U.A. 4: los 14 del maní (UR266, 268, 269, 270, 272, 273A, 273B, 274A, 274B, 275, 276, 277, 278, 279) **más UR271**, con frijol negro, en la misma sala. U.A. 2 tiene 5 (UR262–265, 280); U.A. 7 tiene 2 (UR267A/B); el corredor tiene 7 (UR255–261).
- **Urton 2017:** la narrativa dice **U.A. 05** dos veces (p. 159 y p. 162: “catorce muestras... en la esquina suroeste de la kallanka U.A. 05”), pero el apéndice y otro pasaje de la misma obra (p. 163) dicen **U.A. 04** (“in the corner of excavation unit U.A. 04”). Es la inconsistencia que ya había marcado `n_almacenes` (N4). El peso de la evidencia —2015 artículo + 2015 apéndice + apéndice de 2017— favorece **U.A. 4**; el “05” parece un desliz sistemático de la narrativa de 2017. **Nivel: apoyado con datos, no demostrado**, porque no hay acceso a las notas de campo de Chu.

### 5.2 Cuál es, en el plano de Hyslop

U.A. 4 es **una de las cuatro kallankas de Subsector A1**, en el extremo norte de Sector A/Qolqawasi, flanqueando el corredor norte U.A. 3, cerca de la única entrada noroeste y al lado de un secadero (U.A. 7 u 8). Su esquina suroeste es la que contenía el maní y los 14 quipus.

Hyslop **no usa el término “kallanka” ni numera U.A.**; su descripción del norte de Sector A habla de “several small rectangular structures... next to the only entrance” y de “at least 30 large rectangular enclosures” entre la plataforma y las filas de bins, que él interpreta como zonas de **preparación, secado, clasificación y/o conteo**, no como salas techadas (1985:99–101). La correspondencia U.A. 4 ↔ una estructura concreta de Hyslop es, por tanto, **posicional**, no nominal. **No se puede decidir del texto si U.A. 4 es la kallanka del lado este o del oeste**; haría falta la Figura 3 de Urton & Chu o el plano de Chu. **Nivel: propuesto / abierto.**

### 5.3 Por qué importa: el archivo de U.A. 4 es coherente

| U.A. | Quipus | Cuerdas | Contenido |
|---|---:|---:|---|
| U.A. 2 | 5 | 651 | UR262–265, 280; contra el muro sur/este |
| **U.A. 4** | **15** | **1.839** | los 14 del maní + UR271 (frijol); **incluye UR270 y UR278, los dos libros de 9 partes** |
| U.A. 7 | 2 | 182 | UR267A/B, en cesta con ají |
| Corredor (U.A. 3) | 7 | 303 | UR255–261, pila bajo muro caído |
| **Total** | **29** | **2.975** | 34 recuperados; 29 estudiados |

Los 14 del maní suman **1.807 cuerdas = 60,7 %** de las 2.975 estudiadas. Incluyen el libro maestro UR278 (297 cuerdas, 9 partes), el segundo libro de 9 partes UR270 (158), las copias UR266/UR275, el libro de 208 UR268, y UR269 (273). Es un **archivo de una sola oficina/evento**, no una muestra dispersa. El tamaño medio (129,1 cuerdas) es mayor que el resto (77,9), pero la diferencia **no es significativa** (p permutación = 0,089); no se usa como prueba.

Urton (2017:157–159) describe el flujo: caravanas → corredor norte → kallankas (contabilidad inicial) → secaderos con grid → contabilidad final → cámaras del sur. Eso sitúa los 14 quipus en la **zona de recepción y conteo**, no en las cámaras de depósito. Es consistente con que el libro de 9 partes registre **flujos que entran**, no el stock de un bin concreto.

## 6. Productos, ocupación, población y soldados

### 6.1 Productos

Hyslop: el valle de Lunahuaná “is not a zone capable of great agricultural production”; los almacenes se llenaron con bienes **producidos o manufacturados fuera**; no hay evidencia de producción especializada (1985:31). Urton & Chu recuperaron en el complejo: mazorcas de maíz, semillas de lúcuma, vainas de frijol, vértebras de pescado, fragmentos de moluscos y camarones; además, maní, ají y frijol negro cubriendo quipus. Es una firma **mixta costa/sierra**, coherente con un depósito de aprovisionamiento militar, no con un centro productor local.

**Cuidado:** el maní y el ají son “montones” que cubren los quipus, no el stock excavado. No se puede dividir kilos entre unidades anotadas (negativo N3 de `n_almacenes`). Que los quipus “se usaran para contar maní” es **especulativo**, aunque es la hipótesis más natural para el grupo de 14.

### 6.2 Ocupación

Hyslop: “the archaeological hints... that the site was used only briefly” (1985:33); puertas selladas en E1; poca cerámica Inka; ausencia de áreas de producción; abandono tras la guerra contra Huarco. LeVine/Snead: “Large but only briefly occupied... constructed as a base of operations for military campaigns... subsequently abandoned in favor of the coastal site of Cerro Azul” (1992:78–79). **Nivel: apoyado con datos.**

### 6.3 Población y soldados

- **Población base:** Hyslop propone **~1.000** personas (1985:30) y luego **1.000–2.000** (“A base population of one or two thousand... probably swelled by many thousands when an army was in residence”; cap. 5, “Housing Capacity”). No hay cuarteles para un ejército: “Inkawasi has no architecture which demonstrates it could have housed an army... the armies camped outside” (1985:30). Los residentes se reparten: élite en B, mita/retainers de baja condición en D, intermedios en F; no hay evidencia de mitmaq.
- **Densidad:** 240 cuartos residenciales claros (B 120 + D 120) para 1.000–2.000 personas = **4,2–8,3 personas por cuarto**; si se suman los 49 de F, 3,5–6,9. Es densidad de **barracones/retainers sin familia**, no de hogares. Coherente con la rotación de mit'a.
- **Almacenaje per cápita:** 6.400 m³ / 1.000–2.000 hab = **3.200–6.400 m³ por 1.000**, frente a **605–780 m³/1.000** en Pumpu, Huánuco Pampa y Xauxa (LeVine 1992, tabla 4-4). Es **4,1–10,6 veces** la norma de un centro administrativo de altura; con la capacidad corregida (10.900–16.200), **7–27 veces**. Esto es el argumento más fuerte de que Inkawasi es un **depósito de aprovisionamiento**, no una ciudad.
- **¿Cuántos soldados?** Con 6.400 m³ y densidades 0,4–0,7 t/m³, el depósito guarda **2.560–4.480 t**. A 0,7–1,5 kg/persona/día son **1,7–6,4 millones de personas-día**: 20.000 hombres durante **85–320 días**; 10.000 durante **171–640 días**. Con la capacidad corregida (16.200 m³), 20.000 hombres durante **216–810 días**. Es compatible con los “many thousands” de Hyslop y con una campaña de meses, no con una guarnición permanente de ese tamaño. **Nivel: propuesto** (depende de densidad y ración).

### 6.4 Contraste con los escenarios de mitayos de `n_almacenes`

Con el escenario de costal de 25 kg (el que usa su informe), los trabajadores totales por libro de 9 partes son:

| Producto | p5 | mediana | p95 |
|---|---:|---:|---:|
| papa/chuño | 52 | 90 | 173 |
| maíz | 107 | 208 | 453 |
| frijol | 212 | 395 | 813 |
| maní | 399 | 755 | **1.572** |
| ají | 1.294 | 2.527 | **5.588** |

La población del sitio (1.000–2.000) cubre sin problema los escenarios de chuño/maíz y buena parte de frijol/maní; el escenario de ají (1.300–5.600) exige **0,65–5,6 veces** la población base **por libro** (según se tome 1.000 o 2.000), es decir, mit'a rotativa de fuera. No hay contradicción: Hyslop dice que el ejército acampaba fuera y que la población se inflaba “by many thousands”. Pero tampoco hay confirmación independiente. El hecho de que los 14 quipus estén cubiertos de **maní** apunta al escenario de **400–1.600 trabajadores**, que es el más compatible con la población local; tómese como **propuesto/especulativo**, porque el maní es un marcador, no una prueba del producto contado.

Lo que **no** apoyan los datos: que las 9 columnas sean “9 cuadrillas” de un sector del sitio. El sitio tiene **8 sectores (A–H)**, no 9, y Hyslop no describe una división social en 9. Las 9 columnas pueden ser 9 grupos de trabajo, 9 productos, 9 periodos o 9 categorías administrativas; la arquitectura no decide cuál.

## 7. Controles, resultados negativos y nivel de evidencia

### 7.1 Controles

- **Nulo de permutación dentro de fila** en T1–T3: preserva el total de cada registro y la estructura de 28 registros; 20.000 permutaciones, semilla 20261018. Es el nulo correcto para “¿el perfil de columnas se puede reducir a este corte?”.
- **Holm** para T1–T3 y **Holm separado** para los 8 cortes. Se reportan p sin corregir y corregidos.
- **Control de apofenia** (múltiplos de k) con nulo binomial y Monte Carlo uniforme 1–250. Se reportan ambos; coinciden.
- **Chequeo de independencia:** no se usan los 28 registros como si fueran 28 quipus; la prueba es interna a UR278. UR270 se usa solo como réplica descriptiva y se advierte que 5 de sus 7 registros están repetidos.
- **Chequeo de fuente:** se contrastaron las tres menciones de U.A. 4/5 (2015 artículo, 2015 apéndice, 2017 narrativa/apéndice) y se reporta la inconsistencia.

### 7.2 Resultados negativos

1. **No hay un plano de 9 partes.** Hyslop divide el sitio en 2 mitades y 4 suyus; Kunti Suyu tiene 14 unidades. El 9 aparece en la gramática de los ceques (3 suyus × 9 líneas en grupos de 3), no en el plano de Inkawasi.
2. **No hay asociación espacial entre el 9 y los quipus de 9 partes.** UR270 y UR278 están en U.A. 4 (kallanka), no en E2 (9 cuartos) ni en A2 (9+9 cámaras). P(misma estructura) = 0,337; P(ambos en U.A.4) = 0,259.
3. **Ningún corte de las 9 columnas sobrevive.** 4+5 p = 0,27; 3×3 rechazado (p < 10⁻⁵; R² 0,167 vs 0,307); gradiente p = 0,031 pero Holm 0,061; los 8 cortes contiguos, Holm ≥ 0,118.
4. **El 9 no es un número especial del sitio.** 3 de 13 conteos son múltiplos de 9 (p = 0,17); los múltiplos de 6 dan p = 0,051 y los de 12 p = 0,088. 209 = 11×19, 245 = 5×7², 96 = 3×32.
5. **El grupo de 14 no es significativamente mayor** que el resto (p = 0,089), aunque concentra el 60,7 % de las cuerdas.
6. **No se puede identificar el producto contado** a partir del maní/ají/frijol: son montones que cubren los quipus, no el stock. No hay calibración masa↔unidad.
7. **No se puede fijar el lado de U.A. 4** (este u oeste) sin la Figura 3/plano de Chu.
8. **No se puede resolver si 6.400 incluye A2** con el texto disponible; hay dos lecturas geométricamente válidas y la fórmula de Hyslop no se publica.

### 7.3 Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Sector A es un almacén de 110 × 110 m con 202–250 bins de 3,5–4,5 m y 6.400 m³ | **demostrado** |
| A2 tiene 36 cámaras = 18 por lado = 9 exteriores + 9 interiores | **demostrado** (Urton & Chu 2015) |
| 6.400 m³ es consistente con 209 bins de ~30,6 m³ y es un **piso**, no la suma de 36 cámaras + 209 colcas de 2×2 m | **apoyado con datos** (geometría) |
| El total del sitio es 8.300–13.000 m³ (central) y hasta 16.200 | **propuesto** |
| El sitio se divide en 2 mitades + 4 suyus, no en 9 | **demostrado** (Hyslop) |
| E2 tiene 9 cuartos = 4+5, alineados con el ushnu | **demostrado** (Hyslop); intención simbólica: **propuesto** |
| Las 9 columnas no corresponden a 4+5 ni a un gradiente; el 3×3 contiguo se rechaza | **apoyado con datos** (4+5 p = 0,27; gradiente Holm 0,061; 3×3 p < 10⁻⁵) |
| UR270 y UR278, los dos libros de 9 partes, están en U.A. 4 | **apoyado con datos** (2015 + apéndice; 2017 inconsistente) |
| U.A. 4 es una kallanka del norte de A1, junto al corredor U.A. 3 | **propuesto** (posicional; falta plano) |
| El archivo de U.A. 4 es una oficina/evento coherente | **propuesto** (composición y flujo) |
| Población 1.000–2.000; ejército “many thousands” fuera | **propuesto** (Hyslop lo llama “guess”) |
| Ocupación breve | **apoyado con datos** |
| Almacenaje per cápita 4–27× la norma de altura | **apoyado con datos** (aritmética; población es estimada) |
| 20.000 hombres durante 3–10 meses con 6.400 m³ | **propuesto** (densidad/ración supuestas) |
| El maní indica el producto contado | **especulativo** |
| Las 9 partes son 9 categorías/grupos/periodos internos | **propuesto** (no decidible con arquitectura) |

## 8. Para el coordinador

- **Inkawasi no es un sitio de 9 partes.** Hyslop lo divide en 2 mitades (hanan/hurin) y 4 suyus; Kunti Suyu/Sector F tiene 14 unidades. El único 9 explícito es E2: 4 cuartos + 5 cuartos, con pasillo alineado al ushnu. No hay plantilla arquitectónica de 9 que copiar.
- **Los dos libros de 9 partes (UR270 y UR278) están juntos en U.A. 4**, una kallanka del extremo norte de Sector A/Qolqawasi, en el grupo de 14 quipus cubiertos de maní; **no** están en los 9 cuartos de E2 ni en las filas de 9 cámaras de A2. El 9 es interno al archivo, no un mapa del sitio.
- **Ninguna correspondencia numérica sobrevive.** 4+5 p = 0,27; 3×3 rechazado (p < 10⁻⁵; R² 0,167 vs 0,307); gradiente p = 0,031 pero Holm 0,061; los 8 cortes contiguos, Holm ≥ 0,118. El 9 tampoco es especial: 3/13 conteos múltiplos de 9 (p = 0,17), mientras el 6 da p = 0,051 y el 12 p = 0,088.
- **Corrección importante a `n_almacenes`:** su descomposición 36 cámaras de 112–148 m³ + 209 colcas de 2×2 m no cabe en Hyslop, que da bins de 3,5–4,5 m. Las 209 colcas solas ocupan 5.120–8.464 m³ y 6.400 cae dentro de ese rango. **6.400 es el piso de A, no un central del sitio**: el total plausible es 8.300–13.000 m³ y hasta 16.200 con A2+G. La cota inferior de masa unitaria baja de 3,4–10,4 kg a **1,3–8,0 kg** según el escenario (2,6–8,0 con 8.300 m³; 1,3–4,1 con 16.200); las raciones de 0,7 kg siguen por debajo, pero ya no por un orden de magnitud. La conclusión “la unidad es un volumen (30–55 L)” se mantiene.
- **U.A. 4:** usar **U.A. 4**, no 05. Lo dicen el artículo de 2015 (p. 519, 521) y su apéndice (15 quipus en U.A. 4, incluido UR271); la narrativa de Urton 2017 dice “05” dos veces, pero su propio apéndice y otro pasaje dicen “04”. Es un desliz de la narrativa de 2017, no un cambio de ubicación. **No** se puede fijar si es la kallanka este u oeste sin la Figura 3/plano de Chu.
- **El archivo de U.A. 4 es coherente:** 14 quipus, 1.807 cuerdas = 60,7 % de las 2.975 estudiadas; incluye UR278 (297 cuerdas), UR270 (158), las copias UR266/275 y UR269 (273). Es una oficina/evento, no una muestra dispersa. El flujo descrito por Urton (caravanas → kallankas → secaderos → cámaras) sitúa estos quipus en la **recepción y conteo**, no en el depósito.
- **Población y soldados:** 1.000–2.000 residentes; ejército “many thousands” acampado fuera; sin cuarteles. El almacenaje per cápita es 4–27× la norma de Pumpu/Huánuco/Xauxa, lo que confirma el papel de **depósito de aprovisionamiento**. Con 6.400 m³, 20.000 hombres podrían comer 3–10 meses (0,7–1,5 kg/día); con la capacidad corregida, más. Es una estimación, no una prueba.
- **Mitayos:** 52–173 (chuño), 107–453 (maíz), 212–813 (frijol), 399–1.572 (maní), 1.294–5.588 (ají) por libro de 9 partes. La población local cubre los escenarios bajos/medios; el ají exige mit'a externa. El maní de los 14 quipus apunta a 400–1.600, pero el maní es un marcador, no una prueba del producto contado.
- **Qué pediría a la siguiente ronda:** (1) la Figura 3 o el plano de Chu para fijar el lado de U.A. 4 y las dimensiones de A2; (2) decidir si 6.400 incluye A2 (la fórmula de Hyslop no está publicada); (3) probar las 9 columnas contra **9 categorías de producto, 9 grupos contribuyentes o 9 periodos**, no contra 9 sectores arquitectónicos; (4) usar el grid de 23×23 cm para calibrar el volumen unitario; (5) contrastar la inconsistencia U.A. 4/5 con las notas de campo de Chu.

---

### Reproducibilidad

```
python analisis/ds/n_hyslop/01_sectores.py   # sectores.csv, quipus_ua.csv, capacidad_escenarios.csv
python analisis/ds/n_hyslop/02_pruebas.py    # control_multiplos.csv, control_cortes.csv, T1-T6
python analisis/ds/n_hyslop/03_logistica.py  # logistica_mita.csv, logistica.csv
```

Todo usa semilla 20261018. Los CSV y los `salida_*.txt` están en `analisis/ds/n_hyslop/`. No se modificó nada fuera de esta carpeta.
