# Predicción del equipo 13: ¿existen los flujos 46, 46 y 44 de UR269?

Carpeta: `analisis/ds/n_incahuasi_46_44/`. Scripts reproducibles `00`–`06`, semilla fija.
No se ha modificado nada fuera de esta carpeta. Datos: `analisis/datos/cuerdas.csv` y
`quipus.csv`; se reutiliza (solo lectura) el cargador de `09_incahuasi/comun.py`.

## 0. Pregunta

El libro maestro **UR269** tiene bloques de 5 filas con cuotas (valor constante que se
resta de la cabecera para dar el neto) **47, 46, 46, 44, 25**. Los flujos 47
(UR273A+UR273B, cuotas 30+17) y 25 (UR267A+UR267B, 15+10) están identificados por el
equipo 13. La predicción a probar es:

> Los flujos con cuota 46, 46 y 44 provendrían de parejas de quipus cuyas cuotas sumen
> 46 o 44, y las cabeceras sumadas **registro a registro** darían las filas 2–4 de los
> bloques de UR269.

Se prueba en tres frentes:

1. ¿Hay en **todo el corpus** (651 quipus KFG) quipus con cuota constante por grupo?
   ¿Hay parejas cuyas cuotas sumen 46 o 44? Para cada pareja candidata, ¿A_i + B_i
   reproduce las filas 2–4 (exacto y ±1), con nulo barajando B y corrección múltiple?
2. ¿Es **UR268** (cuota 208 = 47+46+46+44+25) la suma de los bloques de UR269, con
   definiciones de bloque alternativas (separadores rosas, patrón de cuotas, ventanas
   deslizantes de 5), nulo y corrección?
3. ¿Es alguna fila 2–4 de UR269 la **suma de dos o tres registros** de cualquier quipu
   del archivo de Incahuasi (UR255–UR280, UR267A/B, UR273A/B, UR274A/B, JC001–JC023)?

## 1. Método

- **Unidad de análisis: el quipu.** Las permutaciones son dentro de cada quipu
  (barajando cuerdas o el orden de los registros), nunca entre quipus.
- **Registro** = grupo con cabecera (primer colgante presente de nivel 0, valor ≥ 100).
  La definición **estricta** del equipo 13 exige además ≥1 cuerda anudada más; la
  **laxa** no, y se usa para el barrido de parejas porque recupera quipus fragmentarios
  que la estricta descarta (UR273A pasa de 1 a 21 registros, UR273B de 6 a 21). Sin la
  laxa, un componente real como UR273A ni siquiera entraría en el barrido.
- **Cuota** d: valor tal que muchas cabeceras x tienen en su grupo una cuerda de valor
  x−d (el neto). Es la definición operativa de `13_sistema_incahuasi/03_constantes.py`,
  la única que permite buscar cuotas en 651 quipus sin leerlos a mano.
- **Nulo de cuota:** barajar las cuerdas no cabecera entre registros del mismo quipu
  (conserva x, tamaños de grupo y multiconjunto de valores); estadístico = máximo apoyo
  sobre d ∈ {2,…,60} ∪ {208}; 2000 réplicas; BH-FDR sobre los 62 quipus con ≥5 registros.
- **Nulo de suma A+B:** barajar el **orden de los registros de B** (A queda fijo).
  Conserva la distribución marginal de las sumas y la estructura de cada componente,
  pero rompe la alineación registro a registro. 2000 réplicas; BH-FDR por familia.
- **Nulo global del barrido:** para que la búsqueda de 10 153 parejas tenga una prueba
  válida se usa el **estadístico máximo** (máximo de coincidencias sobre todas las
  parejas), que ya incorpora la multiplicidad; 100 réplicas globales.
- **Nulo de magnitud** en los casos dudosos: se conservan las sumas y se sortean los
  objetivos de la distribución empírica de cabeceras de UR269. Es el control de
  "¿esto es solo densidad de números redondos?".
- Correcciones **BH-FDR** (Holm donde se indica). Con B réplicas el p mínimo es 1/(B+1).
  Valores 0 sin nudos = cuerdas ausentes (no ceros).

## 2. Resultados

### 2.1 Objetivos: las filas 2–4 de UR269 (`00_objetivos.py`)

La reconstrucción de bloques por cuerdas rosas (PK), reparando los registros que la
digitalización partió en dos grupos (p. ej. g56 = 2468, 2422 + g57 = 46), da 15 bloques
de tamaños `[5,5,5,5,4,8,5,4,5,5,5,2,4,2,4]`. El bloque de 8 filas es el bloque doble
que ya señaló el equipo 13. Se usan dos conjuntos de objetivos:

- **A (posición):** filas 2–4 de los 8 bloques de exactamente 5 filas → **24 filas**.
- **B (cuota):** todos los registros con cuota explícita 46 o 44 y cabecera ≥ 100 →
  **24 filas** (incluye bloques irregulares; 15 coinciden con A).

Ambos se guardan en `ur269_objetivos.csv` y se analizan en paralelo; las conclusiones no
dependen de la definición.

### 2.2 Inventario de cuotas del corpus y parejas 46/44 (`01_cuotas_corpus.py`)

De los 651 quipus KFG, solo **72 tienen ≥5 registros** (112 con ≥3) con la definición
operativa; 400 no tienen ninguno (fragmentos o escalas de valor distintas). La búsqueda
con nulo de permutación (2000 réplicas, BH sobre 62 quipus) encuentra **9 quipus con
q < 0,05, todos del archivo de Incahuasi**:

| quipu | n | cuota | apoyo | nulo medio/máx | p | q |
|---|---|---|---|---|---|---|
| UR267B | 25 | 10 | 13 | 1,07 / 3 | 0,0005 | 0,005 |
| UR267A | 18 | 15 | 12 | 1,39 / 6 | 0,0005 | 0,005 |
| UR269 | 58 | 46 | 10 | 0,89 / 3 | 0,0005 | 0,005 |
| UR256 | 21 | 10 | 8 | 1,06 / 3 | 0,0005 | 0,005 |
| UR275 | 25 | 47 | 7 | 0,59 / 3 | 0,0005 | 0,005 |
| UR255 | 16 | 15 | 6 | 1,18 / 4 | 0,0005 | 0,005 |
| UR268 | 29 | 208 | 4 | 0,14 / 2 | 0,0005 | 0,005 |
| UR266 | 26 | 47 | 3 | 0,90 / 3 | 0,001 | 0,008 |
| UR274B | 19 | 17 | 3 | 0,47 / 3 | 0,001 | 0,008 |

Ningún quipu de fuera de UR255–UR280 supera el nulo. Los mejores fuera del grupo de
cuotas fuertes son UR274A con 44 (apoyo 2; p = 0,018; q = 0,13) y, ya fuera de
Incahuasi, UR201 con 35 (apoyo 2; p = 0,027; q = 0,18). **El inventario de cuotas detectadas es {10, 15, 17, 46, 47, 208}**, más las
cuotas explícitas 25 (UR267B/UR269) y 30 (UR273A/UR274A), que no salen como constantes
por neto porque en esos quipus la cuota aparece como cuerda suelta.

**Parejas con cuotas que sumen 46 o 44: cero.** Las sumas de dos cuotas del inventario
son 20, 25, 27, 30, 32, 34, 40, 45, 47, 50, 54, 55, 56, 57, 59, 61, 62, 63, 64, 69, …
**44 y 46 no son alcanzables** salvo como 44+0 (UR274A, artefacto aritmético) o 46+0
(UR269, que es el propio libro maestro, no un componente). Por tanto la **familia
dirigida de parejas candidatas tiene tamaño 0**: la predicción, tal como está formulada,
no tiene ningún candidato que cumpla su precondición estructural en el corpus codificado.

### 2.3 Barrido exhaustivo de parejas (`02_parejas_46_44.py`, `02b`, `02c`)

Para no depender de la detección de cuotas se probaron **todas** las parejas de quipus
con ≥3 registros (definición laxa): **143 quipus, 10 153 parejas**. Para cada pareja,
S_i = A_i + B_i (alineación por índice) y se cuenta cuántos de los 24 objetivos explica
el multiconjunto de sumas (emparejamiento uno a uno, exacto y ±1).

| Conjunto | máx. exactas | parejas ≥2 | nulo global (máx / parejas ≥2) | p |
|---|---|---|---|---|
| A (posición) | **2** | 4 | 2,13 (máx 3) / 5,68 | 1,00 / 0,80 |
| B (cuota) | **2** | 2 | 2,13 (máx 4) / 3,82 | 0,95 / 0,88 |

- **Ninguna pareja alcanza 3 coincidencias exactas.** El máximo observado (2) es
  exactamente lo que produce el azar (media 2,13).
- El desfase entre registros de A y B no cambia nada: con d = −3…+3 el máximo es 2
  (una vez 3, p = 0,16) y el nulo da 2,1 de media (`parejas_desfases.csv`).
- La mejor pareja por p bruto es **AS007+UR234**: 2 exactas y 3 con ±1 de 24
  (p₁ = 0,001). Corrigiendo por la familia completa de 10 153 parejas, **q = 1**
  (q mínimo posible 5,07); un BH sobre las 249 parejas preseleccionadas daría 0,25,
  pero esa corrección no es válida porque la preselección usó los datos. El nulo de
  magnitud da **p = 0,36** (media 1,29): las 3 coincidencias ±1 son números redondos
  (2399, 2700, 2250).
- Potencia: con 10 153 parejas y B = 2000, el q mínimo posible es **5,07**; BH no puede
  certificar nada aunque el efecto sea perfecto. Por eso la prueba válida es el máximo
  global: el nulo nunca superó **3** coincidencias exactas en 100 réplicas, de modo que
  una pareja con **≥4** habría dado p ≤ 0,01. No hay ninguna con 3.

### 2.4 Control positivo: la maquinaria detecta las parejas conocidas (`05`)

Con las sumas ya calculadas por el equipo 13 (`componentes_filas.csv`, emparejando por
número de grupo) y los objetivos definidos por cuota:

| pareja | objetivos | exactas | LCS | nulo medio/máx | p |
|---|---|---|---|---|---|
| UR273A+UR273B | cuota 47 (n=8) | **3** | 3/8 | 0,35 / 3 | **0,001** |
| UR274A+UR273B | cuota 47 (n=8) | **2** | 2/8 | 0,32 / 2 | **0,013** |
| UR267A+UR267B | cuota 25 (n=4) | **2** | 2/4 | 0,16 / 2 | **0,007** |
| UR273A+UR273B | cuota 46 (n=14) | 0 | 0 | 0,00 | 1,00 |
| UR267A+UR267B | cuota 44 (n=10) | 0 | 0 | 0,00 | 1,00 |

El conjunto de cuota 25 solo recoge 4 filas con la cuota **explícita** (g28=200,
g47=662, g65=522, g77=486); las otras filas del flujo 25 (g21=828, g41=742, g53=712,
g81=392) tienen la cuota implícita (no hay cuerda 25 en el grupo) y no entran en este
control, que por eso es conservador.

El estadístico **sí detecta** un flujo real cuando la alineación es la correcta y los
objetivos son los de su cuota: 3/8 exactas con orden perfecto para el flujo 47 y 2/4
para el 25. Las mismas parejas dan **0** contra las filas 46/44. Esto valida el método
y descarta que el negativo de 2.3 sea un fallo de la prueba.

### 2.5 UR268 frente a la suma de bloques de UR269 (`03_ur268_bloques.py`)

UR268 tiene 29 registros y cabeceras entre 7135 y 15 039. Se probaron 3 definiciones de
bloque (separadores PK; patrón de cuotas 47…25; ventanas deslizantes de 5), con
cabeceras y con netos (cabecera − cuota), exacto y ±1: **12 pruebas, 0 coincidencias
exactas**. La única ±1 es una ventana deslizante (p = 0,55). Todos los q = 1.

Las sumas de bloque (PK) y su cabecera más cercana de UR268:

| bloque | suma | UR268 más cercana | diferencia |
|---|---|---|---|
| 0 | 9335 | 9332 | +3 |
| 1 | 7384 | 7553 | −169 |
| 2 | 10379 | 10385 | −6 |
| 3 | 9503 | 9443 | +60 |
| 4 | 9810 | 9793 | +17 |
| 5 | 14944 | 15039 | −95 |
| 6 | 8515 | 8527 | −12 |
| 7 | 8853 | 8966 | −113 |
| 8 | 10244 | 10385 | −141 |
| 9 | 7922 | 8000 | −78 |
| 10 | 8553 | 8527 | +26 |
| 11 | 2392 | 2200 | +192 |
| 12 | 7444 | 7553 | −109 |
| 13 | 4100 | 2200 | +1900 |
| 14 | 6084 | 7135 | −1051 |

**Potencia:** si UR268 fuese exactamente la suma de los 15 bloques, se observarían
15/15 coincidencias; en la definición PK el nulo nunca supera 2, así que el test
detectaría **≥3** bloques exactos. Observado: **0**. La hipótesis "UR268 = suma de bloques de UR269" queda
rechazada para estas definiciones, no por falta de potencia.

### 2.6 Los casi-aciertos son puro espaciado (`06_proximidad_ur268.py`)

Las dos casi-coincidencias que señaló el equipo 13 (9335 vs 9332; 10379 vs 10385) no
son especiales. Con 29 cabeceras de UR268 repartidas en ~8000 unidades, la distancia al
valor más cercano es ~140 por puro espaciado. Contando cuántas de las 15 sumas de bloque
tienen una cabecera a menos de δ:

| δ | observado | nulo (media) | p |
|---|---|---|---|
| 1 | 0/15 | 0,00 | 1,00 |
| 10 | 2/15 | 2,00 | 1,00 |
| 25 | 4/15 | 4,00 | 1,00 |
| 50 | 5/15 | 5,00 | 1,00 |
| 100 | 8/15 | 8,00 | 1,00 |
| 200 | 13/15 | **13,00** | 1,00 |

El nulo reproduce **exactamente** el observado en todos los umbrales: la proximidad no
aporta nada. Los "casi" son la línea base de densidad, no una relación con error de
lectura.

### 2.7 ¿Filas 2–4 = suma de 2 o 3 registros? (`04_sumas_2_3_registros.py`)

Con la definición estricta, 21 quipus del archivo tienen ≥2 registros. Se cuentan las
representaciones de cada objetivo como suma de 2 o 3 registros distintos del mismo
quipu, y se compara con un **nulo de densidad local** (enteros sorteados en [0,9t, 1,1t],
que preserva la magnitud del objetivo):

| objetivos | suma de | observado | nulo local | p | q mínimo por objetivo |
|---|---|---|---|---|---|
| A (24) | 2 registros | 22 en 14/24 | 11,7 | 0,022 | 0,28 |
| A (24) | 3 registros | 63 en 22/24 | 58,1 | 0,29 | 0,62 |
| B (24) | 2 registros | 19 en 13/24 | 13,0 | 0,12 | 0,32 |
| B (24) | 3 registros | 68 en 21/24 | 63,1 | 0,30 | 0,61 |

El único p < 0,05 (0,022) no sobrevive a corregir por las 8 celdas de la tabla
(BH q = 0,18) y **desaparece al quitar UR269 del pool**: 5 representaciones frente a
5,5 esperadas (p = 0,62). El exceso está dentro del propio libro maestro y es
la identidad trivial **cabecera = neto + cuota** de cada registro (305 de las 443
representaciones con todos los valores de nivel 0 son de UR269). Controlando por
densidad y excluyendo esa identidad:

| variante | observado | nulo local | p |
|---|---|---|---|
| A, 2 registros, sin UR269 | 5 | 5,5 | 0,62 |
| A, 3 registros, sin UR269 | 50 | 47,6 | 0,39 |
| A, todos los valores nivel 0, sin UR269 | 138 | 108,8 | 0,17 |
| B, 2 registros, sin UR269 | 4 | 6,0 | 0,80 |
| B, 3 registros, sin UR269 | 58 | 51,4 | 0,21 |

**Ninguna fila 2–4 es una suma de 2 o 3 registros de otro quipu más de lo que explica la
densidad.** Con ~0,5 representaciones esperadas por fila (pares) y ~2,4 (tríos), el test
solo tendría potencia para una relación sistemática que afectara a la mitad de las
filas; no para certificar una fila aislada. Ese es el límite honesto de este negativo.

## 3. Resumen de controles

| Prueba | observado | nulo | p | corrección |
|---|---|---|---|---|
| Cuotas en el corpus (62 quipus) | 9 quipus q<0,05 | 1,0–1,4 apoyos | 0,0005–0,001 | BH q = 0,005–0,008 |
| Parejas con cuota 44/46 | **0** | — | — | familia vacía |
| Barrido de 10 153 parejas (máximo) | 2 exactas | 2,13 (máx 3) | 1,00 | estadístico máximo |
| Mejor pareja (AS007+UR234) | 3 con ±1 | 1,29 | 0,001 bruto / **0,36 magnitud** | BH familia completa q = 1 |
| Control positivo UR273A+B (flujo 47) | 3/8 exactas | 0,35 | 0,001 | — |
| UR268 = Σ bloques (12 pruebas) | 0 exactas | 0,04–0,26 | 1,00 | BH q = 1 |
| UR268 proximidad (13/15 a ±200) | 13 | **13,00** | 1,00 | — |
| Filas 2–4 = 2 registros (sin UR269) | 5 | 5,5 | 0,62 | BH q por objetivo ≥ 0,28 |
| Filas 2–4 = 3 registros (sin UR269) | 50 | 47,6 | 0,39 | BH q por objetivo ≥ 0,61 |

## 4. Resultados negativos (explícitos)

1. **No hay ninguna pareja de quipus con cuotas que sumen 46 o 44** en el corpus KFG
   codificado. La familia dirigida tiene tamaño 0.
2. **Ninguna pareja de los 143 quipus con ≥3 registros reproduce las filas 2–4**:
   máximo 2 coincidencias exactas de 24 (nulo 2,13), 0 parejas con ≥3, y el máximo
   global no es significativo (p = 1,00). El desfase −3…+3 no cambia el resultado.
3. **UR268 no es la suma de los bloques de UR269** en ninguna de las 12 definiciones
   probadas (0 exactas; el test detectaría ≥3). Los "casi" son exactamente lo que
   predice el espaciado de 29 cabeceras (13/15 a ±200 frente a 13,00 esperadas).
4. **Ninguna fila 2–4 es una suma de 2–3 registros de otro quipu** más de lo esperado
   por densidad (p = 0,39–0,80 al excluir UR269). El único p < 0,05 era la identidad
   interna cabecera = neto + cuota del propio UR269.
5. **Ningún quipu JC participa**: los 23 quipus del Sector B no tienen cuotas y solo
   JC005 llega a 3 registros; no aportan candidatos.

## 5. Niveles de evidencia

- **Apoyado con datos (negativo principal).** La predicción no se cumple en el corpus
  codificado: no hay parejas candidatas y el barrido exhaustivo, con potencia para
  detectar ≥4 coincidencias exactas, encuentra como máximo 2. El control positivo
  demuestra que la misma maquinaria detecta los flujos 47 y 25 ya conocidos.
- **Apoyado con datos (inventario de cuotas).** Las únicas cuotas constantes del corpus
  son las 9 del archivo de Incahuasi; fuera de UR255–UR280 no hay ninguna que supere el
  nulo (mejor q = 0,13).
- **Demostrado con las definiciones probadas (UR268).** UR268 no es la suma de los
  bloques de UR269; el negativo tiene potencia para detectar ≥3 bloques exactos.
- **Propuesto.** Los flujos 46, 46 y 44 no se conservan en el corpus codificado. Es la
  explicación más simple, pero no está demostrada: 400 quipus no tienen registros
  utilizables y podrían esconder los componentes.
- **Especulativo.** Que las cuotas de los componentes perdidos sigan el mismo esquema
  (p. ej. 29+17 = 46, 30+16 = 46, 15+29 = 44, 17+27 = 44, 21+25 = 46): no hay ningún
  dato que lo sostenga; solo es la forma que exigiría la regla "cuota suma".

## 6. Limitaciones y potencia

- **Cobertura.** 400 de los 651 quipus no tienen ningún registro con la definición
  operativa (fragmentos, valores < 100 o grupos de una sola cuerda). El barrido cubre
  143 quipus; si un componente perdido es un fragmento como UR273A (que la definición
  estricta dejaba en 1 registro), la definición laxa lo recupera, pero no todos los
  fragmentos tienen cabeceras ≥ 100.
- **Detección de cuotas.** Una cuota expresada en solo 1–2 registros no se detecta
  (p. ej. UR274A, 44, apoyo 2). El barrido de parejas no depende de eso, pero el
  inventario de 2.2 sí es un límite inferior.
- **Alineación.** El barrido usa A_i + B_i por índice; el equipo 13 empareja por número
  de grupo, lo que puede introducir desfases. Se probaron desfases −3…+3 sin cambio.
- **Potencia del barrido.** Con 10 153 parejas, BH no puede certificar nada (q mínimo
  5,07); la prueba válida es el máximo global, que detectaría ≥4 exactas (p ≤ 0,01).
  El resultado observado (máx 2) está en el centro del nulo.
- **UR268.** El negativo vale para las 3 definiciones de bloque probadas. No se probaron
  bloques definidos por el color de los separadores ni sumas ponderadas; el equipo 13
  ya documentó que el orden no se conserva (τ bajo), lo que va en la misma dirección.
- **Sumas de 2–3 registros.** El test de 2.7 solo tiene potencia para relaciones
  sistemáticas (≥10 filas); no puede descartar que una fila aislada sea una suma casual.

## 7. Para el coordinador

- **La familia dirigida está vacía; por eso la predicción se probó como búsqueda
  exhaustiva.** En los 651 quipus KFG solo 9 tienen cuota constante (todos UR255–UR280,
  con cuotas 10, 15, 17, 46, 47 y 208) y **ninguna pareja de cuotas suma 46 ni 44** (las
  sumas posibles son 20, 25, 27, 30, 32, 34, 40, 45, 47, 50…). Los flujos 46/44
  exigirían cuotas nuevas (29+17, 30+16, 15+29, 17+27, 21+25…), no conservadas.
- **Barrido exhaustivo: 10 153 parejas, máximo 2 coincidencias exactas de 24 (nulo
  2,13), ninguna con 3.** El estadístico máximo da p = 1,00; la mejor pareja
  (AS007+UR234) tiene p bruto 0,001 pero q = 1 (familia completa) y su nulo de
  magnitud p = 0,36.
- **Control positivo decisivo:** con las sumas del equipo 13, UR273A+UR273B reproduce
  3/8 filas de cuota 47 (p = 0,001, orden perfecto) y UR267A+UR267B 2/4 de cuota 25
  (p = 0,007). La misma maquinaria, aplicada a las filas 46/44, da 0. El negativo no es
  un fallo del test.
- **UR268 no es la suma de los bloques de UR269:** 0 coincidencias exactas en 12 pruebas
  (3 definiciones de bloque × cabecera/neto × exacto/±1), con potencia para detectar ≥3.
  Los dos "casi" (9335/9332 y 10 379/10 385) son puro espaciado: 13/15 sumas tienen una
  cabecera a ±200, y el nulo da exactamente 13,00.
- **Ninguna fila 2–4 es suma de 2–3 registros de otro quipu** más de lo esperado por
  densidad (p = 0,39–0,80 sin UR269). El único p < 0,05 (0,022) era la identidad
  interna cabecera = neto + cuota del propio UR269.
- **Nivel de evidencia:** negativo **apoyado con datos** para las filas 2–4 y el barrido
  de parejas; **demostrado con las definiciones probadas** para UR268; **propuesto** que
  los componentes 46/44 no se conservan; **especulativo** cualquier reconstrucción de sus
  cuotas.
- **Recomendación 1:** no gastar más tiempo en buscar parejas 46/44 en el KFG. Si se
  busca, hacerlo en los registros de campo/fotos de Chu y en los 5 quipus de Inkawasi
  que Urton no estudió, con la predicción refinada: cuotas nuevas en
  {14, 16, 19, 21, 27, 29, 31} (complementos de 30, 30, 25, 25, 17, 17 y 15) o pares
  nuevos como 22+22 = 44 y 18+28 = 46.
- **Recomendación 2:** el siguiente test con más poder no es otra pareja, sino el
  **orden dentro del bloque**: las filas 2–4 tienen cuotas 46, 46 y 44, pero no se sabe
  cuál es cuál; si apareciera un candidato, la prueba debe exigir que sus sumas caigan
  en las filas 2, 3 y 4 en orden (LCS), no solo que coincidan los valores.
- **Recomendación 3:** revisar en el objeto las diferencias de UR268 que no sean
  atribuibles a error de lectura (60, 95, 113, 141…): no forman un offset constante y
  no acercan UR268 a los bloques; probablemente son cuerdas no registradas o bloques
  incompletos.

## 8. Reproducibilidad

| script | qué hace | salida |
|---|---|---|
| `00_objetivos.py` | bloques y filas de UR269; objetivos A y B | `ur269_filas.csv`, `ur269_objetivos.csv` |
| `01a_explorar_cuotas.py` | apoyo observado de cuotas en 62 quipus | `cuotas_observadas.csv` |
| `01_cuotas_corpus.py` | cuotas con nulo de permutación y BH en todo el corpus | `cuotas_corpus.csv` |
| `02_parejas_46_44.py` | barrido de 10 153 parejas, nulo barajando B, BH | `parejas_screen.csv` |
| `02b_nulo_global.py` | nulo del estadístico máximo del barrido | — |
| `02c_desfases.py` | robustez a desfases −3…+3 | `parejas_desfases.csv` |
| `03_ur268_bloques.py` | UR268 vs sumas de bloque (3 definiciones) | `ur268_bloques.csv` |
| `04_sumas_2_3_registros.py` | filas 2–4 como suma de 2–3 registros | `sumas_23_registros.csv` |
| `05_control_positivo.py` | parejas conocidas vs sus filas | `control_positivo.csv` |
| `06_proximidad_ur268.py` | casi-coincidencias de UR268 vs nulo de espaciado | — |

Semillas: 4644 (01), 4602 (02), 4605 (02b), 4607 (02c), 4603 (03), 4604 (04),
4606 (05), 4608 (06).

## 9. Literatura (contexto mínimo)

- **Urton 2015 (Inkawasi)**: los "pares atados" contienen registros cuantitativos muy
  similares y hay posibles unidades contables estandarizadas; es el punto de partida
  del equipo 13, pero el resumen no ofrece controles estadísticos ni cuotas.
- **Clindaniel 2019**: confirma en UR267A/UR255 el uso W/AB/MB como suma/resta/resultado
  (proof of concept) y advierte que no ha encontrado otros quipus del mismo género; esto
  apoya que UR267A+B sea un caso local, no una regla general que permita predecir las
  cuotas 46/44.
- En las fichas consultadas (Urton 2015, Clindaniel 2019) no aparece ninguna propuesta
  de que las cuotas de un libro maestro se descompongan en sumas de cuotas de
  componentes; la regla 30+17=47 y 15+10=25 es un hallazgo del equipo 13, no de la
  literatura.
