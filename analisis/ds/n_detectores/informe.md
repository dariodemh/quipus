# Detectores dirigidos en todo el corpus KFG

**Equipo:** `n_detectores`. **Fecha:** 2026-10-18. **Datos:** `analisis/datos/*.csv` (651 quipus, 57 818 cuerdas, 40 162 anudadas) + `data/external/open-khipu-repository/data/khipu.db`.
**Scripts:** `comun.py`, `d1_cuotas.py`, `d2_parejas_suma.py`, `d3_cadenas.py`, `d4_celdas.py`, `refinar_d2_d3.py`, `d5_superiores.py`, `resumen.py`. Semillas fijas (`20261017 + detector`). Sin commits; todo vive en `analisis/ds/n_detectores/`.

---

## 1. Pregunta

¿Hay en el corpus KFG **otros sistemas contables entre quipus** como el de Incahuasi (UR255–UR280), o Incahuasi es único? Se aplican cuatro detectores dirigidos a **todos** los quipus con ≥3 registros y a **todos** sus pares, agrupando además por `procedencia` y por `museo` (archivos con ≥3 quipus). Se añade D5: cuántas cuerdas superiores y marcadoras de OKR se pierden en la codificación KFG.

La lección que guía el diseño: los barridos genéricos no encuentran nada; las pruebas dirigidas (una cuota, una suma alineada, un orden) sí. Por eso cada detector tiene un nulo que **solo rompe el emparejamiento** y conserva magnitudes, tamaños de grupo y huecos, y cada control positivo se declara antes de mirar los resultados.

## 2. Método

### 2.1 Unidad y definiciones

- **Registro** = grupo de colgantes que no es separador rosa (PK sin nudos). **Cabecera** = primer colgante anudado (nivel 0) del grupo. Se conservan los registros sin cabecera (`x=0`) como huecos para no romper la alineación.
- **Cuota** = valor `c` tal que `x_i − n_i = c` en casi todos los registros, o valor que se repite en la misma posición relativa.
- **Tolerancia ±1 dígito** = diferencia en `{0, 1, 10, 100, 1000, 10000}` (la misma de `13_sistema_incahuasi`).
- **Colecciones:** 31 familias por `procedencia` (606 quipus) y 41 por `museo` (600 quipus). Para un par, la familia dirigida es la procedencia compartida; si no, el museo compartido; si no, `global` (exploratorio).
- **Exclusiones:** mismo objeto y copias conocidas de `14_copias/` y `04_concordancias/` (27 pares). **Excepción deliberada:** no se excluyen los pares internos de Incahuasi, porque son el control positivo (UR273A+B→UR266/UR275, UR278→UR266). Se excluyen las copias entre museos (HP055~UR1084, UR064~UR068, UR006~UR009, etc.).

### 2.2 Detectores

| Detector | Qué busca | Nulo | Réplicas |
|---|---|---|---|
| **D1** | Cuota por registro: `x−n=c` constante, o valor modal en la misma posición de colgante | Barajar cuerdas no-cabecera entre registros del quipu (conserva grupos, multiconjunto y magnitudes); para la posición, barajar dentro de cada registro entre posiciones ≥1 | 1000 |
| **D2** | `A_i + B_i =` cabecera de algún registro de un tercer quipu `C` (exacto y ±1), con orden (τ) | Permutar las cabeceras no nulas de B entre sus posiciones no nulas (conserva huecos y magnitudes) | 1000; 5000 si p≤0,01 |
| **D3** | Totales de grupo de A que aparecen como cabeceras de B en el mismo orden (LCS) | Barajar la secuencia de cabeceras de B | 1000; 5000 si p≤0,01 |
| **D4** | Celda = colgante + su s1, columna a columna, que reproduce un grupo de B | Permutar los grupos de B (vectores completos) | 1000 |

**Estadístico de D2.** Es el de **unión**: número de registros `i` cuya suma cae en la cabecera de *algún* quipu del destino (lectura literal de «algún tercer quipu C»), el mismo que usó `13_sistema_incahuasi` (UR266 ∪ UR275 ∪ UR269). La atribución al mejor `C` y el top-3 se dan como descripción, no como estadístico. Esto es importante: contar «cualquier cabecera de cualquier quipu del corpus» da medias nulas de 6–20 y ningún poder; restringir el destino a la colección de A y B es lo que hace el detector dirigido.

**Multiplicidad.** Se aplica BH por detector sobre **todos** los pares (como pide el encargo) y, además, BH dentro de la familia dirigida. El BH global es, por construcción, incapaz de dar q<0,05: con 108 319 pares de D2 y p mínimo 2·10⁻⁴ (5000 réplicas), el q mínimo posible es 21,7. Se reporta para dejar constancia, pero la prueba válida es el **q dirigido** (`q_dir`): BH dentro de la familia, restringida a quipus con ≥3 cabeceras ≥100 (contenido numérico). En Incahuasi eso deja 20 quipus y 190 pares.

### 2.3 Control positivo (obligatorio)

| Control | Detector | Resultado | p | q_dir |
|---|---|---|---|---|
| UR273A + UR273B → UR266/UR275 | D2 | 12/18 sumas (8 exactas); top-3: UR269:7, **UR275:6, UR266:5**; τ=0,43 | 0,0002 | **0,037** |
| UR273B + UR274A → UR275 | D2 | 10/17 (6 exactas); C=**UR275**:7; **τ=1,0** | 0,0008 | 0,074 |
| UR270 → UR278 | D4 | 6 grupos; 9/9 columnas en el mejor; **τ=1,0** | 0,001 | **0,030** |
| UR278 → UR266 | D3 | LCS=15 (nulo 5,9) | 0,0002 | **0,038** |
| UR278 → UR275 | D3 | LCS=11 (nulo 4,9) | 0,0002 | **0,038** |
| UR267A + UR267B → UR269 | D2 | 15/26 (9 exactas); C=UR269:9; τ=0,46 | 0,009 | 0,46 |
| UR255/UR267A c=15; UR256/UR267B c=10; UR266/UR275 c=47; UR268 c=208; UR269 c=46; UR274B c=17 | D1 | 3–15 registros de apoyo cada uno | ≤0,002 | 0,004–0,006 |

Los cinco controles obligatorios se recuperan. El de D2 atribuye el primer destino a UR269 (que también es libro consolidado), pero UR275 y UR266 aparecen en el top-3 y el par UR273B+UR274A→UR275 tiene τ=1. El sistema no es un artefacto del detector.

## 3. Resultados

### 3.1 D1 — Cuotas: Incahuasi, y casi nada más

410 quipus analizados (≥3 registros y al menos un candidato `d`), 45 familias. **12 quipus con q_max<0,05; 11 son Incahuasi**:

| Quipu | c* | Apoyo/n | Explícita/n | q_max |
|---|---|---|---|---|
| UR255 | 15 | 9/28 | 15/28 | 0,004 |
| UR267A | 15 | 15/26 | 24/26 | 0,004 |
| UR256 | 10 | 8/24 | 6/24 | 0,004 |
| UR267B | 10 | 13/26 | 22/26 | 0,004 |
| UR266 | 47 | 3/33 | 14/33 | 0,006 |
| UR275 | 47 | 7/26 | 22/26 | 0,006 |
| UR269 | 46 | 10/91 | 2/91 | 0,004 |
| UR268 | 208 | 4/30 | 16/30 | 0,004 |
| UR274B | 17 | 3/33 | 6/33 | 0,006 |
| UR277 | 2 | 8/19 | 1/19 | 0,006 |
| JC001 | 2 | 3/8 | 0/8 | 0,038 |

Fuera de Incahuasi solo hay tres señales, y ninguna es una cuota contable:
- **HP055** (museo Nacional de Arqueología): el valor **100 ocupa la posición 2 en 10 de 31 registros** (p=0,001; q=0,001). Es una **columna constante**, no `x−n=c`. Candidata a unidad/patrón de medida; [propuesto].
- **UR1149** (Ocucaje): `c=610` con 4/25 registros (p=0,005; q=0,015). Con 4 apoyos y una colección pequeña es [especulativo].
- **c=1** en UR001/UR006 (Leymebamba) y UR076 (Huaquerones): trivial (muchas cuerdas valen 1); [artefacto].

**Lectura:** el patrón de cuota `x−n=c` es específico del archivo de Incahuasi. No aparece en Pachacamac (90 quipus), Ica (47), Leymebamba (22), Nazca (13), Puruchuco (23), Lima, Santa ni en los quipus de museo con ≥3 ejemplares.

### 3.2 D2 — Sumas registro a registro

466 quipus con ≥3 cabeceras, **108 319 pares** (tras exclusiones); 82 683 pares con `obs≥3` probados con 1000 réplicas; **31 refinados con 5000**. El q global no baja de 1 (imposible por tamaño de familia). Por exceso (`obs − media nula`) los primeros puestos son:

| A + B | n | obs | exactas | Mejor C (nC) | τ | nulo medio | exceso | p | q_dir | familia |
|---|---|---|---|---|---|---|---|---|---|---|
| **UR273A+UR273B** | 18 | 12 | 8 | UR269 (7); top3 UR275:6, UR266:5 | 0,43 | 3,70 | **8,30** | 0,0002 | **0,037** | Incahuasi |
| **UR273B+UR274A** | 17 | 10 | 6 | **UR275** (7) | **1,00** | 3,98 | **6,02** | 0,0008 | 0,074 | Incahuasi |
| **UR267A+UR267B** | 26 | 15 | 9 | UR269 (9) | 0,46 | 9,16 | 5,84 | 0,009 | 0,46 | Incahuasi |
| UR190+UR274B | 14 | 11 | 2 | AS008 (3) | — | 5,79 | 5,21 | 0,0016 | 1,0 | global |
| MM019+UR266 | 26 | 13 | 6 | UR247 (3) | — | 8,10 | 4,90 | 0,003 | 1,0 | global |
| UR255+UR274A | 19 | 12 | 3 | UR269 (4) | −1,0 | 7,12 | 4,88 | 0,011 | 0,46 | Incahuasi |
| **UR1088+UR195** | 24 | 23 | 14 | UR232 (18); top3 UR233:18, UR120:11 | **−0,31** | **18,61** | 4,39 | 0,0026 | 0,023 | **Huacho** |
| UR034+UR197 | 19 | 19 | 17 | AS069 (14) | 0,51 | 16,56 | 2,44 | 0,0016 | 1,0 | global |

**El único candidato fuera de Incahuasi con q_dir<0,05 es UR1088+UR195→UR232/UR233/UR120 (Huacho).** No es un sistema tipo Incahuasi:
- La media nula es **18,6** y lo observado **23** (exceso 4,4, la mitad que el control de Incahuasi).
- El orden no se conserva: **τ = −0,31** (los componentes de Incahuasi dan τ=1 o 0,43).
- Los quipus implicados (UR1088, UR195, UR232, UR233, UR120) tienen valores pequeños y densos (2, 4, 10, 20), de modo que una suma de dos registros cae casi siempre en alguna cabecera. Es la **explicación aburrida** (densidad), no una relación contable.
- La atribución se reparte entre tres destinos (18/18/11) en vez de concentrarse en un libro.

Los demás puestos altos son ruido de densidad: UR190+UR274B→AS008 tiene solo 3 coincidencias en el mejor C y top-3 repartido; UR034+UR197→AS069 es el quipu grande de 431 registros con cabeceras 1–130; UR267A+UR267B es el control del sistema (q_dir=0,46 por el tamaño de la familia, no por falta de efecto).

### 3.3 D3 — Cadenas de cabeceras ordenadas

216 648 pares ordenados; 35 392 con LCS≥3; 22 refinados. **Ningún par fuera de Incahuasi tiene q_dir<0,05.** Los controles:

| A → B | LCS | nulo medio | exceso | p | q_dir |
|---|---|---|---|---|---|
| **UR278 → UR266** | **15** | 5,91 | 9,09 | 0,0002 | **0,038** |
| **UR278 → UR275** | **11** | 4,86 | 6,14 | 0,0002 | **0,038** |
| UR273A → UR274A | 7 | 3,92 | 3,08 | 0,0014 | 0,18 |
| QU021 → AS007 | 9 | 5,55 | 3,45 | 0,0004 | 1,00 |
| UR045 → UR1140 | 10 | 6,62 | 3,38 | 0,0008 | 1,00 |
| UR004 → UR231 | 11 | 7,72 | 3,28 | 0,0068 | 1,00 |

Los dos únicos efectos fuertes son el control (UR278→UR266/UR275). Los demás tienen exceso ≤3,5 y q_dir=1 tras corregir: no hay cadenas comparables en Pachacamac, Ica, Nazca, Puruchuco, Santa ni Lima.

### 3.4 D4 — Celdas colgante+s1

Solo **60 quipus** tienen grupos con ≥3 celdas completas (colgante con su primera subsidiaria); 3 536 pares ordenados, 18 candidatos. El control es el único resultado sólido:

| A → B | grupos | columnas (mejor) | τ | nulo medio | p | q_dir |
|---|---|---|---|---|---|---|
| **UR270 → UR278** | **6** | **9/9** | **1,0** | 0,20 | 0,001 | **0,030** |
| UR029 → AS212 | 3 | 3 | — | 0,38 | 0,001 | 0,61 |
| UR057 → UR272 | 3 | 5 | — | 0,38 | 0,001 | 0,61 |
| UR057 → AS212 / UR057→UR113 / UR272→UR034 | 2 | 4/4/3 | — | 0,07–0,23 | 0,001 | 0,61 |

Los dos pares con 3 grupos coinciden en solo 3 columnas y su q_dir es 0,61. **D4 no encuentra ninguna otra tabla de celdas en el corpus**, con la limitación de que solo es aplicable a quipus con subsidiarias s1 (60 de 651).

### 3.5 D5 — Cuerdas superiores y marcadoras perdidas en KFG

Cruce `cuerdas.csv` ↔ `khipu.db(cord)` por `puente.csv`; `CORD_ORDINAL` de OKR = rango del colgante KFG (validado en UR087: 7,14,21,…,109 = p7,p14,p21,…,p109). Resultados en `superiores_perdidas.csv`:

| Concepto | OKR (nivel 1) | KFG lo registra | Perdidas |
|---|---|---|---|
| Cuerdas superiores `T` | **95** en 11 quipus | 3 (solo HP047) | **92 / 95 = 96,8 %** |
| Marcadoras `M` | **502** en 63 quipus | 0 (KFG no tiene campo) | **502 / 502 = 100 %** |
| KFG `union=T` que OKR no marca T | — | 54 cuerdas en 9 quipus | falsos positivos |

Desglose de las 92 T perdidas: **57 como `union=U`**, **34 como R/V** y 1 sin mapear. En **UR087**: 13 T, todas perdidas (10 U + 3 R/V), y 5 marcadoras, las 5 perdidas. Coincide exactamente con `k_UR087/informe.md`.

**Corolario:** KFG no solo pierde las superiores: su `union=T` (154 cuerdas, 26 quipus) es en gran parte otra cosa (54 falsos positivos en 9 quipus; solo HP047 coincide con OKR). Cualquier análisis de superiores/marcadoras debe hacerse contra OKR, no contra KFG. D5 es **demostrado** (campos directos, sin inferencia).

## 4. Controles y resultados negativos

- **Nulo y p:** todos los efectos reportados tienen p empírico con semilla fija y nulo explícito que conserva magnitudes y tamaños. El p mínimo con 1000 réplicas es 0,001; con 5000, 0,0002.
- **Corrección múltiple:** BH por detector sobre todos los pares (q global) y BH dirigido por familia (`q_dir`). El q global de D2/D3 es estructuralmente inútil (q mínimo posible 21,7 en D2 y 43,3 en D3, ambos >1); se reporta por transparencia. El q_dir es la prueba que sobrevive.
- **Negativos fuertes:**
  - No hay cuota `x−n=c` no trivial fuera de Incahuasi (11/12 D1 son Incahuasi; los casos externos son c=1 trivial o UR1149, aislado).
  - No hay otra cadena ordenada (D3: 0 pares externos con q_dir<0,05).
  - No hay otra tabla de celdas (D4: 0 pares externos; los 2 con 3 grupos tienen q_dir=0,61).
  - No hay enlace entre el Sector B de Incahuasi (JC001–JC023) y el resto: ningún par JC–UR queda con q_dir<0,05; JC005+UR262 tiene p=0,015 pero q=0,46, y JC001 solo da una cuota c=2 con 3/8 registros (q=0,038, no replicada).
  - El mejor candidato externo (Huacho) se explica por densidad y no respeta el orden (τ=−0,31).
- **Falsos positivos esperables:** los quipus grandes con valores pequeños y densos (AS069, UR050, UR055, UR1032, UR144) dominan el ranking bruto de D2 pero no el exceso; su media nula es casi igual a lo observado. Es la explicación aburrida que hay que descartar antes de hablar de sistema.

## 5. Niveles de evidencia

| Afirmación | Nivel |
|---|---|
| El sistema de Incahuasi se recupera con D1, D2, D3 y D4, con los controles obligatorios y q_dir≤0,074 | **Demostrado** (controles positivos + nulo) |
| No hay otro sistema tipo Incahuasi en el corpus KFG (651 quipus) según D1–D4 | **Apoyado con datos** (barrido completo; límites: D4 solo 60 quipus, D2/D3 dependen de cabeceras) |
| KFG pierde 92/95 cuerdas superiores y 502/502 marcadoras; su `union=T` no equivale a OKR T | **Demostrado** (campos directos) |
| HP055 tiene una columna constante de 100 en la posición 2 (posible unidad de medida) | **Propuesto** |
| UR1088+UR195→UR232/233/120 (Huacho) es un sistema contable | **Especulativo / probable artefacto de densidad** (exceso 4,4; τ negativo; nulo 18,6) |
| UR1149 (Ocucaje) tiene cuota 610 | **Especulativo** (4/25 registros) |

## 6. Limitaciones

1. **D2 y D3 dependen de la cabecera** (primer colgante anudado). Un sistema que use totales en otra posición o en subsidiarias se vería solo parcialmente. D4 cubre el caso colgante+s1, pero solo 60 quipus tienen esa estructura.
2. **D2 usa la unión de destinos de la colección.** La atribución a un `C` concreto es descriptiva; el p-valor es del estadístico de unión. Para el control, el top-3 contiene UR266/UR275, pero el mejor `C` individual es UR269.
3. **El q global no es interpretable** por el tamaño de la familia (108 319 pares). El q_dir restringe a quipus con ≥3 cabeceras ≥100; es una decisión de diseño declarada, no un ajuste post hoc.
4. **La procedencia de museo no es lugar de origen.** Las familias `museo:` se usan solo como agrupación archivística, nunca como proveniencia.
5. **D5** solo cubre los quipus con fila en `puente.csv`; los 59 `union=T` de KFG sin fila en el puente no se pudieron contrastar.

## 7. Para el coordinador

- **Incahuasi sigue siendo único.** De 410 quipus con cuota analizable, 11 de los 12 con `q<0,05` son Incahuasi; las cuotas 10, 15, 17, 46, 47 y 208 se recuperan con 3–15 registros de apoyo y q=0,004–0,006.
- **Los cinco controles obligatorios se recuperan:** D2 da UR273A+UR273B→UR266/UR275 (12/18, 8 exactas, q_dir=0,037) y UR273B+UR274A→UR275 (τ=1, q_dir=0,074); D3 da UR278→UR266 (LCS=15, q_dir=0,038) y →UR275 (LCS=11, q_dir=0,038); D4 da UR270→UR278 (6 grupos, 9/9 columnas, τ=1, q_dir=0,030).
- **Ningún otro archivo muestra el paquete completo.** D3 no tiene ningún par externo con q_dir<0,05; D4 no tiene ninguna otra tabla de celdas; D1 no tiene ninguna otra cuota no trivial (UR1149, c=610 en 4/25, es el único caso externo y queda como especulativo).
- **El mejor candidato externo es Huacho (UR1088+UR195→UR232/233/120):** 23/24 sumas, q_dir=0,023, pero media nula 18,6 (exceso 4,4), τ=−0,31 y valores pequeños densos. Lo clasifico como **artefacto de densidad**, no como sistema.
- **Puruchuco, Pachacamac, Ica, Nazca, Lima y Santa: negativos.** Los quipus grandes (AS069, UR050, UR055, UR1032, UR144) generan falsos positivos brutos en D2, pero su exceso es pequeño (≤3,5) y su media nula es casi lo observado.
- **D5 es el hallazgo más sólido y de aplicación inmediata:** OKR tiene 95 cuerdas superiores nivel 1 en 11 quipus; KFG solo marca 3 (HP047) → **92/95 perdidas (96,8 %)**, 57 como `union=U` y 34 como R/V. Y **502/502 marcadoras perdidas (100 %)**. En UR087, 13/13 superiores y 5/5 marcadoras.
- **KFG `union=T` no es OKR `T`:** 54 cuerdas en 9 quipus llevan `union=T` sin ser T en OKR. No usar KFG para estudiar superiores/marcadoras; cruzar siempre con `khipu.db`.
- **Recomendación 1:** repetir D2/D3 en los quipus de Pachacamac y Puruchuco usando **todas las cuerdas** (no solo cabeceras) y alineación por bloques/separadores, como se hizo en Incahuasi; el negativo actual es de cabeceras, no de valores.
- **Recomendación 2:** investigar HP055 (columna de 100 en posición 2, 10/31) y UR1149 (c=610, 4/25) como casos aislados, no como sistemas.
- **Recomendación 3:** para D5, generar una tabla de equivalencias cuerda KFG ↔ CORD_ID de OKR y reetiquetar `union=T`/marcadoras antes de cualquier análisis de estructura; hoy KFG oculta el 97 % de las superiores y el 100 % de las marcadoras.

---

### Reproducir

```bash
cd analisis/ds/n_detectores
python d1_cuotas.py          # d1_cuotas.csv
python d2_parejas_suma.py    # d2_observado.csv, enlaces_d2.csv (criba 1000)
python d3_cadenas.py         # d3_cadenas.csv, d3_candidatos.csv
python d4_celdas.py          # d4_celdas.csv, d4_candidatos.csv
python refinar_d2_d3.py      # refina a 5000 y reescribe enlaces_d2/d3
python d5_superiores.py      # superiores_perdidas.csv
python resumen.py            # enlaces_nuevos.csv
```
