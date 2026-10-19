# 22_formularios: ¿hay «formularios con clave de reparto» en todo el corpus?

**Pregunta.** El modelo de «formulario local» dice que los números son universales y que color y posición marcan categorías con una clave propia de cada archivo. ¿Se ve fuera de Incahuasi y de UR053?

**Respuesta corta.**

- **Sí, hay formularios** dentro de los quipus: 37 % de los que tienen ≥ 30 cuerdas.
- **Sí, se replican dentro de archivos**: 20 conjuntos de quipus distintos confirman en la mitad de confirmación.
- **No aparece la misma clave de color en archivos sin relación.** El criterio congelado de refutación no se cumple.
- **Pero la «clave local demostrada» solo se sostiene en 4 archivos pequeños**, de 2 a 5 quipus cada uno. Dos de ellos son pares que no son independientes (copias o mitades).

## Archivos

| archivo | qué es |
|---|---|
| `diseno.md` | diseño congelado antes de correr el corpus |
| `detector.py` | nivel quipu: candidatos, estadísticos, nulos 1–3 y controles negativos. Salidas: `quipus_detector.csv`, `salida_detector.txt` |
| `archivos.py` | archivos, exploración→confirmación, especificidad, copias y sumas, refutación y tasa. Salidas: `formularios.csv`, `refutacion_pares.csv`, `salida_archivos.txt` |

Se corre desde la raíz: `python analisis/22_formularios/detector.py` y luego `python analisis/22_formularios/archivos.py`.

**Nota de formato.** En `quipus_detector.csv` las claves de motivo usan `-` como separador. Eso es ambiguo con colores mezclados como `W-MB`: el CSV se escribió antes de la desviación 3. En `formularios.csv` y `refutacion_pares.csv` el separador es `|`.

## Desviaciones del diseño (declaradas)

1. **Color ausente (`nan`, 356 colgantes).** Ahora rompe los motivos: no puede definir una categoría. Antes de corregirlo aparecía como color «nan» en motivos falsos (p. ej. `nan-W`).
2. **p del quipu: de paramétrico a permutación**, como preveía el §3 del diseño.
   - El p paramétrico (ANOVA + Bonferroni dentro del quipu) **falló el control negativo**. En el corpus barajado N3 dio 1–5 detecciones BH y hasta 3 Holm, todas degeneradas: 3 bloques idénticos como `[0,1],[0,1],[0,1]`, con residuo cero y F infinito.
   - p_q pasa a ser un **min-p por permutación** del nulo 3: barajar los valores entre los colgantes de nivel 0 con colores y grupos fijos, y repetir la búsqueda completa. Así queda corregida la búsqueda sobre todos los candidatos.
   - Se usan 199 réplicas, que se amplían hasta 10 199 si p ≤ 0,02. Por eso **el p mínimo es 9,8·10⁻⁵ y el Holm mínimo es 0,037** (376 quipus). Holm < 0,05 equivale aquí a «tocó el piso».
   - El nulo 1 usa el mismo esquema, con un máximo de 1 999 réplicas.
3. **Separador de motivos.** Pasa de `-` a `|`, porque hay colores con guion. Es un error de código sin efecto estadístico (la deduplicación es por cuerdas).
4. **Suplemento post hoc: Incahuasi P9.** No entró en la confirmación por el tope congelado de 3 tipos por familia: P3, P4 y P6 tenían p_E menor. Se probó aparte y se marca como post hoc.
5. **Controles negativos con 2 réplicas por tipo**, no 3.

## 1. Nivel quipu

**Candidatos y nulos.**
- 376 de 651 quipus tienen al menos un candidato válido; en total hay 6 989 candidatos.
- La familia P (posicional) son grupos de k colgantes. Las familias C son motivos de color contiguos dentro del grupo, en resolución fina y gruesa.
- El estadístico es el efecto de posición tras quitar la escala del bloque (ANOVA de dos vías sobre log1p).
- Nulos:
  - **nulo 3:** valores barajados dentro del quipu; da p_q;
  - **nulo 1:** colores barajados dentro del quipu; necesario para llamar «cromático» a un formulario;
  - **nulo 2:** valores barajados entre bloques, columna por columna; prueba si el bloque funciona como registro, es decir, si hay coescala.

**Controles positivos (obligatorios): los 5 detectados.**

| quipu | tipo | candidato | bloques | cuotas | p_q | q_BH | nulo 1 |
|---|---|---|---|---|---|---|---|
| UR053A | cromático | W–RL–AB | 14 | 0,65 / 0,19 / 0,16 | ≤1·10⁻⁴ | 5·10⁻⁴ | 5·10⁻⁴ |
| UR053C | cromático | A–W–R (grueso) | 20 | 0,14 / 0,61 / 0,25 | ≤1·10⁻⁴ | 5·10⁻⁴ | 5·10⁻⁴ |
| UR053D | cromático | W–R–A–W–R | 12 | 0,44 / 0,09 / 0,12 / 0,28 / 0,08 | ≤1·10⁻⁴ | 5·10⁻⁴ | 5·10⁻⁴ |
| UR278 | posicional | P9 | 26 | 0,14 / 0,14 / 0,10 / 0,11 / 0,11 / 0,13 / 0,11 / 0,08 / 0,09 | 0,002 | 0,007 | — |
| UR270 | posicional | P9 | 7 | 0,15 / 0,15 / 0,10 / 0,12 / 0,09 / 0,16 / 0,10 / 0,04 / 0,08 | 0,013 | 0,032 | — |

Además, UR053E es cromático: W–R, 0,77 / 0,23, con 35 bloques. UR053B no llega (q = 0,045, pero nulo 1 = 0,11), porque su AB es subsidiaria.

**Coescala dentro del quipu.**
- **Incahuasi** coescala (UR278: nulo 2 p = 0,002). Sus filas son registros.
- **UR053A y UR053C no coescalan.** En UR053C, W y R incluso se compensan. El reparto 4:1:1 de UR053 es estable **entre** quipus, no fila a fila. Esto confirma lo que el coordinador vio (CV de la parte W de 0,11 a 0,31).

**Controles negativos (corpus barajados, pipeline completo):** ver §1b. N3 da 0 detecciones; N1 da 3–5 cromáticos falsos.

**Resultado en todo el corpus** (q_BH < 0,05 sobre p_q de permutación, n = 376).

| | todos los quipus | quipus con ≥ 30 cuerdas (n = 410) |
|---|---|---|
| Q, cualquiera | 162 | **150 = 36,6 %** [31,9; 41,5] |
| Q posicional | 89 | 81 = 19,8 % |
| Q cromático (pasa nulo 1) | 73 | 69 = 16,8 % |
| Q+ (además, el bloque coescala: nulo 2) | 87 | 83 = 20,2 % |
| Holm < 0,05 (piso) | 79 | 76 = 18,5 % |

- **Banderas entre los Q de ≥ 30 cuerdas:**
  - «total + partes»: 12;
  - «lista ordenada»: 9;
  - «filas casi idénticas»: 9.

  Son pocas: la mayoría de los formularios no se explica por totales, listas ordenadas ni copias internas.
- **Tamaño del formulario:** k va de 2 a 12, con moda 3–6.
- **Réplica de otras rondas:** los 8 «bloques de perfil repetido» de n_plantillas salen todos Q: UR1131, UR1175, UR1144, UR1149, UR1099, AS178, AS048 y UR172. También UR1140, la ficha de Nazca.

### 1b. Controles negativos

Se corrió el pipeline completo (p por permutación, nulo 1 y BH) sobre corpus barajados. Fueron 2 réplicas de cada tipo y no 3 como decía el diseño, por tiempo de cómputo (desviación 5).

| corpus barajado | Q cromático | Q posicional | Holm < 0,05 | referencia: p paramétrico, q_BH < 0,05 |
|---|---|---|---|---|
| N3 (valores barajados en el quipu), rep 0 | 0 | 0 | 0 | 2 |
| N3, rep 1 | 0 | 0 | 0 | 4 |
| N1 (colores barajados en el quipu), rep 0 | 3 | 102* | 42* | 119 |
| N1, rep 1 | 5 | 104* | 44* | 124 |

\* En N1 la estructura posicional queda intacta a propósito, porque solo se barajan los colores. Por eso los Q posicionales son esperables ahí, no son falsos positivos.

- **Lo que cuenta en N1 son las detecciones cromáticas falsas: 3–5**, frente a 73 en los datos reales. Implica una FDR empírica de ~5–7 % entre los cromáticos.
- **N3 da 0 detecciones:** el p por permutación está bien calibrado, y el paramétrico no.

## 2. Nivel archivo: exploración → confirmación

**Archivos y partición.**
- Hay 148 archivos que cubren 519 de 651 quipus:
  - 23 por conjunto de prefijo;
  - 38 por procedencia;
  - 87 por museo con inventario consecutivo.
- La partición se hizo con semilla 20261018 y quedó así:
  - UR053B, D y E en exploración; UR053A y C en confirmación;
  - UR278 en exploración; UR270 en confirmación.

**Resultados.**
- 200 tipos pasaron de exploración a confirmación (p_E < 0,001, como máximo 3 por archivo y familia).
- **138 son «no confirmables»:** el tipo no aparece en ningún quipu de confirmación del mismo archivo. Es la limitación más grande: la mayoría de los archivos tiene 2–3 quipus.
- De los 62 confirmables, **41 confirman con BH** (31 con Holm). Quitando duplicados (el mismo par de quipus contado como conjunto, procedencia y museo) quedan **27 formularios en 20 conjuntos de quipus distintos**.
- **Especificidad:** solo 10 filas son **locales**, es decir, la concordancia en el archivo supera la de fuera (Mann-Whitney < 0,05). Corresponden a **4 archivos**. Las demás quedan «indeterminadas»: hay pocos quipus de fuera con el mismo tipo, o fuera también hay algo de concordancia.

### Formularios de archivo confirmados (sin duplicados)

| archivo (quipus) | formulario: posiciones y cuotas medias | quipus con el tipo / Q | escala máx/mín | p_C · Holm | especificidad | copias / sumas |
|---|---|---|---|---|---|---|
| **UR053A–E** (Banco Central; conjunto = museo consecutivo) | **W \| R (grueso): W/R por quipu A 0,76 · B 0,66 · C 0,70 · D 0,80 · E 0,77**. También W\|RL\|AB\|W\|RL: E 0,44/0,09/0,10/0,29/0,08 frente a C 0,40/0,09/0,08/0,32/0,10 | 5 / 4 | **70×** | 5·10⁻⁵ · 0,003 | **local** (p = 0,042) | UR053B~C copia (14_copias); sin sumas |
| **UR267A/B** (Incahuasi, mitades A/B) | P3: 0,54/0,09/0,37 frente a 0,46/0,12/0,42; W\|W\|A: 0,57/0,06/0,36 frente a 0,51/0,17/0,33 | 2 / 2 | 3× | 5·10⁻⁵ · 0,003 | local (0,029) | UR255~UR267A copia; las mitades A/B son una misma obra (n_narrative_threads) |
| **UR131A–C** (Lluta, Arica; conjunto) | P7: 0,69/0,27/0,02/0/0,01/0/0,01 frente a 0,67/0,26/0,04/0/0/0,02/0,02 | 1 (solo B tiene ≥ 3 bloques) / 1 | — | 5·10⁻⁵ · 0,003 | local (0,003) | — |
| **UR141 + UR149** (museo consecutivo; UR149 de Ocucaje) | P8: 0,01/0,22/0,05/0,11/0,28/0,10/0,16/0,07 frente a 0,00/0,39/0,04/0,03/0,43/0,04/0,04/0,03 | 2 / 2 | 1,6× | 5·10⁻⁵ · 0,003 | local (0,025) | — |
| **Incahuasi** (procedencia) | P3: E 0,55/0,18/0,27 frente a C 0,47/0,36/0,16. P4: 0,53/0,16/0,09/0,21 frente a 0,41/0,21/0,23/0,15. W\|NB\|AB: 0,89/0,01/0,10 frente a 0,64/0,24/0,12 | P3: 12 / 11 | 2 100× | 1,5·10⁻⁴ · 0,006 | indeterminado (0,063) | UR255~UR267A copia; 13_sistema: UR270→UR278 (124 relaciones de suma), UR255→UR270 (64), UR267A→UR270 (31), … |
| Incahuasi P9 (**post hoc**) | E (UR278) 0,14/0,14/0,10/0,11/0,11/0,13/0,11/0,08/0,09 frente a C (UR270, JC009) 0,13/0,11/0,08/0,17/0,10/0,13/0,09/0,09/0,11 | — | — | p_C = 0,022 | — | ídem |
| **Santa** (UR087, UR090, UR092) | W×6 + R(+R+R) (grueso): UR092 0,04/0,25/0,03/0,29/0,08/0,06/0,05/0,20 frente a UR087 0,04/0,04/0,01/0,37/0,02/0,04/0,04/0,44 | 2–3 / 1 | 1–12× | 3,5·10⁻⁴ · 0,015 | indeterminado | — |
| UR195 + UR198 (museo consecutivo; Nazca) | P4: 0,05/0,07/0,81/0,07 frente a 0,16/0,12/0,50/0,22 | 2 / 2 | 1× | 4,5·10⁻⁴ · 0,018 | indeterminado | — |
| UR045 + UR048 (museo consecutivo) | P4: 0,17/0,07/0,70/0,07 frente a 0,15/0,15/0,51/0,19 | 2 / 2 | 1× | 5·10⁻⁵ · 0,003 | indeterminado | — |
| UR242/244/246 (museo consecutivo; Ica) | P8: la 4.ª o la 5.ª posición es la mayor (0,42 frente a 0,37) | 3 / 3 | 9,5× | 5·10⁻⁵ · 0,003 | indeterminado | — |
| Ica (UR229, UR1166) | P11: la 1.ª es la mayor (0,31 frente a 0,47) | 2 / 2 | 3,5× | 1·10⁻⁴ · 0,004 | indeterminado | — |
| Pachacamac (procedencia) | P6: 0,17/0,22/0,43/0,07/0,05/0,06 frente a 0,16/0,30/0,11/0,14/0,24/0,05 | 6 / 5 | 105× | 0,005 · 0,13 | indeterminado | AS125~UR247 mismo objeto; UR1118~UR218 copia |
| Pachacamac K\|M (UR199, HP017) | 0,00 / 1,00: la K siempre vacía; **marcador vacío, trivial** | 2 / 2 | 1× | 0,031 · 0,69 | indeterminado | — |

Todas las filas, incluidas las no confirmadas y las no confirmables, están en `formularios.csv`.

**Lectura.**

- **UR053A–E es el mejor caso del modelo.**
  - La razón W:R se mantiene entre 0,66 y 0,80 en 5 quipus cuya escala varía 70 veces.
  - Se predijo desde 3 quipus de exploración y se confirmó en los otros 2 (Holm 0,003).
  - Es específica del archivo: fuera de él, los quipus con W\|R no concuerdan (concordancia −0,003 frente a 0,59).
  - El trío completo W\|R\|A no entró en la confirmación por el tope de 3 tipos: lo desplazaron W\|R y los motivos de 5 posiciones, que lo contienen.
- **Incahuasi se confirma por procedencia (P3, P4, W\|NB\|AB) y P9 se replica post hoc (p = 0,022), pero la especificidad no se demuestra:** P3 tiene p_local = 0,063, y los formularios de 3–4 posiciones con la primera mayor son comunes en todo el corpus (10_tablas: «1.ª columna mayor»). Aun así, Incahuasi es el único archivo con **formulario + sumas entre quipus** (13_sistema), es decir, un sistema.
- **UR267A/B y UR131A–C confirman, pero no son registros independientes**: mitades de una misma obra o un juego atado.
- **UR141/UR149 es un hallazgo nuevo**: un formulario P8 con las posiciones 2 y 5 dominantes, en dos quipus de Berlín con inventario consecutivo. Pero hay solo 3 bloques en confirmación. **Propuesto/apoyado.**
- **Santa:** el bloque de 6 blancas + rojas concuerda entre UR092 y UR087, en línea con el «grupo de 6 cuerdas por tributario» de Medrano y Urton. Pero solo hay 3–4 bloques, y las cuotas difieren en la posición 2 (0,25 frente a 0,04). **Propuesto.**

## 3. Copias y sumas

- **Copias** (tomadas de `14_copias/pares_resumen.csv`):
  - UR053B~UR053C, en el formulario W\|R;
  - UR255~UR267A y AS125~UR247, el mismo objeto;
  - UR1118~UR218, en el archivo de Pachacamac.
- **Sumas entre quipus:** solo las hay registradas en Incahuasi (13_sistema). Ningún otro archivo confirmado tiene sumas conocidas entre sus quipus.
- **Con la excepción de Incahuasi, los formularios de archivo son registros paralelos con la misma clave, no consolidaciones.**

## 4. La predicción que refutaría el modelo

- **Universo.** Motivos de color finos con p_col < 0,05 en el quipu. Hay 392 pares de quipus que comparten un motivo idéntico y son del mismo archivo o no relacionados. Los pares de procedencia desconocida no entran en ninguna de las dos clases.
- **Umbral d\*.** d\* = 0,434 es la distancia de Aitchison máxima entre UR053A, C y D en W\|R\|A.

| pares | k | n | con d ≤ d\* | esperado (posiciones permutadas) | p |
|---|---|---|---|---|---|
| mismo archivo | 2 | 68 | 31 | 17,1 | 0,0005 |
| mismo archivo | ≥ 3 | 100 | **25 (25 %)** | 6,7 | 0,0005 |
| no relacionados (procedencias distintas) | 2 | 151 | 25 | 18,7 | 0,02 |
| no relacionados | ≥ 3 | 73 | **4 (5,5 %)** | 1,3 | 0,018 |
| no relacionados **estrictos** (sin palabra común en la procedencia y museo distinto) | ≥ 3 | 45 | 1 | 0,4 | **0,33** |

- **El criterio congelado de refutación no se cumple.** Ningún par cumple las condiciones individuales: k ≥ 3, los dos Q, p_col < 0,01 en el motivo y d ≤ d\*.
  - Los 4 pares no relacionados con k ≥ 3 cercanos son **3 motivos de un mismo par**, HP033 (Ullujaya, Ocucaje, Ica) ~ KH0049 («Costa Sur»).
  - Los dos están en el Museo Nacional (MNAAHP) y son de la costa sur, así que la «no relación» es dudosa. HP033 tiene valores de 1 a 16 y p_col de 0,02 a 0,04.
  - El cuarto par es HP033~UR272, con d = 0,433, justo en el umbral.
  - Con la definición estricta, el exceso desaparece (1 frente a 0,4; p = 0,33).
- **Dentro de archivo, los pares con el mismo motivo tienen el mismo reparto 4,5 veces más a menudo que entre archivos** (25 % frente a 5,5 %; Fisher OR = 5,75, p = 0,0007). Es la firma de una clave local.
- **Un resto débil (k = 2).** En los pares no relacionados con dos colores (sobre todo W\|AB y W\|MB), la razón va en el mismo sentido en el 59 % (p = 0,034). Es compatible con la regularidad conocida «la 1.ª columna, a menudo blanca, es la mayor» (10_tablas). Es una tendencia de marcado, no un léxico: no fija proporciones. Por diseño no refuta, pero **conviene decirlo**: el blanco tiende a ir con lo mayor en varios sitios.

## 5. Tasa y comparación con los géneros coloniales

**Quipus con ≥ 30 cuerdas (n = 410).**

| | n | fracción |
|---|---|---|
| formulario detectable (Q) | 150 | **36,6 %** |
| formulario cromático (Q cromático) | 69 | 16,8 % |
| formulario de registros (Q+) | 83 | 20,2 % |
| miembro de un formulario de archivo confirmado (BH) | 44 | 10,7 % |
| miembro de un formulario de archivo **local** | 12 | 2,9 % |

**Medrano (72 transcripciones, `11_rosetta`).**

| género | n | % | forma |
|---|---|---|---|
| pnum (tributo, servicios, bienes entregados) | 29 | 40 % | «categoría + número» por rubros; es lo que produciría un formulario si los rubros se repiten por unidad |
| summ (títulos y visitas) | 32 | 44 % | un número por pueblo: una lista sin bloque de k posiciones, que no generaría formulario |
| elicit | 8 | 11 % | |
| pnar | 3 | 4 % | |

El padrón del Santa (un grupo de 6 cuerdas por tributario) sí es un formulario.

- La **cota superior colonial**, de ~40 % de géneros con forma de formulario, es del mismo orden que el 37 % de Q.
- La fracción con **clave compartida y confirmada en un archivo** (11 %, o 3 % local) es mucho menor. Eso se debe en buena parte al diseño: la mayoría de los archivos tiene 2–3 quipus y 138 de 200 tipos no son confirmables.
- **Límite de la comparación:**
  - 26 de las 29 pnum son posteriores a la conquista;
  - el corpus es mayoritariamente prehispánico y costero;
  - la tesis no trae las listas completas.

  Es una comparación de órdenes de magnitud y nada más (**especulativo**).

## Para el coordinador

- **[demostrado, con salvedad]** El detector congelado recupera los 5 controles positivos: UR053A, C y D cromáticos (q = 5·10⁻⁴, nulo 1 = 5·10⁻⁴) y UR278/UR270 posicionales P9 (q = 0,007 y 0,032). Salvedad: el p paramétrico falló el control negativo con bloques degenerados, así que se usa min-p por permutación (desviación declarada). Con eso, los corpus barajados dan 0 detecciones (N3) y 3–5 cromáticos falsos (N1), frente a 73 reales. El Holm mínimo alcanzable es 0,037.
- **[apoyado]** En el 36,6 % de los quipus con ≥ 30 cuerdas (150 de 410) hay un formulario detectable: posición o color que guarda cuotas estables entre bloques una vez quitada la escala. En el 16,8 % la clave es el color (pasa el nulo de colores barajados), y en el 20,2 % los bloques además coescalan, como registros. Banderas triviales (total+partes, lista ordenada, filas idénticas): ≤ 12 cada una.
- **[demostrado]** UR053A–E: W:R = 0,66–0,80 en 5 quipus que varían 70 veces en escala. Predicho desde B, D y E, se confirma en A y C (Holm 0,003) y es específico del archivo (p_local = 0,042; fuera, concordancia ≈ 0). No coescala fila a fila dentro del quipu: la clave es de archivo, no de registro.
- **[apoyado]** Incahuasi: P3 y W\|NB\|AB se confirman entre mitades (Holm 0,006 y 0,038); P4 solo con BH (Holm 0,051). El P9 se replica solo post hoc (p = 0,022), porque el tope congelado lo dejó fuera. La especificidad no se demuestra (p = 0,063): los formularios cortos con la 1.ª posición mayor son comunes. Incahuasi sigue siendo el único archivo con formulario y sumas entre quipus.
- **[apoyado/propuesto]** 20 conjuntos de quipus distintos confirman un formulario de archivo con BH. Solo 4 son locales demostrados: UR053A–E, UR267A/B, UR131A–C y UR141+UR149, y los dos del medio no son registros independientes. Nuevos para mirar: UR141/UR149 (P8 con las posiciones 2 y 5 dominantes, Berlín) y el bloque W×6+R del Santa (UR087/UR092; 3–4 bloques). Este último podría ser el «grupo por tributario» de Medrano y Urton.
- **[demostrado como negativo de la refutación]** No aparece la misma secuencia de colores con el mismo reparto en archivos sin relación: 0 pares cumplen el criterio congelado. El único acercamiento, HP033~KH0049 (3 motivos), es dudoso: los dos están en el MNAAHP y son de la costa sur. Con la definición estricta, 1 frente a 0,4 esperado (p = 0,33). Dentro de archivo, el mismo motivo tiene el mismo reparto en el 25 % de los pares; entre archivos, en el 5,5 % (OR = 5,75, p = 0,0007). Es la firma de una clave local. **Revisado en «Control por transcriptor»:** el contraste se mantiene con el investigador fijo (MH OR 5,5), pero sin UR053 baja a no significativo; queda en «apoyado».
- **[apoyado, débil]** El resto compartido es una tendencia, no un léxico: en pares de dos colores de sitios distintos, el blanco va con el valor mayor en el 59 % (p = 0,034), en línea con «la 1.ª columna, a menudo blanca, es la mayor». El modelo debe admitir este marcado débil de lo principal.
- **[especulativo]** La tasa de formularios (37 %) es del mismo orden que la fracción colonial de géneros «categoría + número por rubros» (pnum, 40 % de Medrano). Las transcripciones son posteriores a la conquista y el corpus no, así que no es una prueba.
- **Limitaciones:**
  - 138 de 200 tipos explorados no son confirmables, porque el tipo no aparece en la otra mitad del archivo; los archivos son pequeños;
  - los «archivos» por procedencia (Pachacamac, 90 quipus) son sitios y no archivos;
  - solo se usan colgantes: los formularios con subsidiarias quedan fuera (UR053B);
  - motivos contiguos sin huecos;
  - la especificidad tiene poca potencia cuando fuera hay < 5 quipus con el tipo.

## Control por transcriptor

Lo pidió el coordinador tras `24_color_formato`. El detalle está en `transcriptor.md`; el script es `transcriptor.py`.

- **La confusión existía.**
  - Dentro de archivo, el 90 % de los pares con el mismo motivo comparten investigador.
  - Entre archivos sin relación, solo el 48 %.
- **Definiciones.**
  - El transcriptor relevante es el **investigador**, con la regla de 24 (AS y UR ≥ 1000 = Ascher; UR = Urton; JC = Clindaniel).
  - `cord.CREATED_BY` es quien digitalizó, no quien nombró los colores. Se informa como control secundario.
- **Con el investigador fijo, el contraste dentro frente a entre se mantiene:**
  - k ≥ 3: 25 de 96 frente a 0 de 35 (p = 0,0002);
  - k = 2: 48 % frente a 18 % (p = 0,0003);
  - Mantel-Haenszel OR = 5,5;
  - solo Urton: p = 0,037 (k ≥ 3) y 0,0007 (k = 2).
- **Pero depende de UR053A–E.** Sin sus pares: 22 % frente a 0 % (p = 0,135) y 31 % frente a 19 % (p = 0,22). La dirección se mantiene, ya sin significación. Rebaja la «firma de clave local» del §4 de **demostrado** a **apoyado, sostenido sobre todo por UR053**.
- **No aparece ninguna clave compartida que el vocabulario ocultara:**
  - 0 de 35 pares sin relación con k ≥ 3 y el mismo investigador están cerca (potencia ≥ 0,9 para una tasa del 25 %);
  - 0 pares cumplen el criterio de refutación.
  - El exceso débil con k = 2 (W\|MB, MB\|AB) baja a p = 0,084.
  - HP033~KH0049, el único acercamiento, junta a dos investigadores distintos (HP y KH) con la misma digitalizadora y el mismo museo.
- **Potencia:**
  - **solo Urton tiene n**: 147 pares dentro y 81 entre;
  - Ascher tiene 3 pares dentro, porque sus quipus son casi todos de procedencia desconocida;
  - Clindaniel no tiene ninguno.

  Para Ascher, el negativo entre archivos (0 de 21 con k ≥ 3) es informativo; el contraste dentro frente a entre, no.
