# 10_tablas: ¿qué hay en las columnas de los quipus-tabla?

**Respuesta corta.** En los quipus-tabla la columna no suele ser un "total" del resto de la fila. Esa columna-total solo existe en Incahuasi. Lo que sí se repite es otra cosa:

- **Las columnas son categorías de tamaño desigual.** Hay una columna grande, a menudo la primera y a menudo blanca, y columnas menores.
- **Las filas son unidades de tamaño distinto.** Todas sus columnas crecen y decrecen juntas.
- **Los totales de fila, cuando existen, van fuera de la fila**, en una cuerda suelta (grupo de una cuerda) pegada a ella o en una cuerda superior.
- **Hay columnas gemelas** (dos registros casi iguales de la misma cantidad) **y filas duplicadas** (copias).
- **El número de filas no muestra ningún valor "típico"** (4, 6, 10, 12) que sobreviva al control.

## Datos y método

- **Selección.** Se tomaron 177 quipus con columnas: q<0,05 en la prueba de grupos explícitos de `03_gramatica` (color o magnitud), o "columna fuerte" en `02_color`. Los CSV de 02 y 03 se leen sin modificarlos.
- **Matriz.** Las filas son los grupos de colgantes del tamaño modal (al menos 2 cuerdas, al menos 3 grupos). Las columnas son las posiciones dentro del grupo.
  - Las cuerdas superiores (unión T) se excluyen de la matriz y se tratan como candidatas a resumen.
  - Una celda sin nudos se trata como ausente, no como cero.
  - Mediana R = 8 filas (RIC 4–13), mediana K = 6 columnas (RIC 4–8). El 81 % de las celdas tiene nudos.
- **Nulos.** Todos son por permutación, con semilla fija 20261017 y p empírico. La corrección es BH entre quipus para cada prueba y Holm entre los indicadores de corpus.
  - **N_fila**: baraja las celdas dentro de cada fila. Destruye la identidad de la columna y conserva cada fila.
  - **N_col**: baraja cada columna entre filas. Conserva cada columna y destruye la coherencia de la fila.
  - **N_ambos** (el nulo del encargo): baraja las filas entre sí y las celdas dentro de cada fila.
  - **Orden de filas**: permuta las filas completas.
- **Scripts** (en orden; unos 20 min en total): `comun.py` (incluye autocomprobación), `t1_columnas.py`, `t2_arquetipos.py`, `t3_filas.py`, `t3b_detalle_resumen.py`, `t4_lecturas.py`. Cada uno deja sus resultados en `t*_resumen.txt` y `t*.csv`.

## T1. Descripción de las columnas, quipu a quipu (`t1_por_quipu.csv`, `t1_resumen.txt`)

| prueba (nulo) | evaluables | p<0,05 | q<0,05 |
|---|---|---|---|
| columna sistemáticamente mayor/menor (N_fila) | 177 | 124 | **119** |
| vacías concentradas en columnas (N_fila) | 177 | 69 | 52 |
| columna casi constante (N_fila) | 170 | 51 | 36 |
| la celda = suma del resto de la fila cae siempre en la misma columna (N_fila) | 29 | 7 | 7 |
| exceso de filas con total interno (N_col) | 177 | 11 | 6 |
| columna k = i + j, o i = k − j ("saldo") (N_col) | 167 | 18 | 8 |
| correlación entre columnas a lo largo de las filas (N_col) | 135 | 67 | **60** |
| proporción fija entre dos columnas (N_col) | 137 | 53 | 26 |
| tendencia del total de fila a lo largo de las filas (orden de filas) | 147 | 29 | 6 |

- **Columna mayor/menor.** Es la regla: 119 de 177 quipus. Cautela: la selección se hizo en parte por columnas de magnitud, así que esta cifra es casi circular.
  - Lo que no es circular es *qué* columna es la mayor: la primera en 49 quipus (22 esperados si la posición fuera uniforme), la última en 14 (22 esperados) y una interior en 56 (75 esperados).
- **Columna total.** Es **solo Incahuasi**: UR255, UR256, UR267A, UR267B, UR269 y UR275, más UR045 con 4 de 23 filas. En todos ellos la terna es `col0 = col1 + col2`, lo que replica 01.
  - **Resultado negativo:** fuera de Incahuasi no hay ningún quipu con una columna que sea el total de su fila, ni con exceso de filas con total interno.
- **Columnas casi constantes (36).**
  - Casi siempre valen **1** y están en la primera o la cuarta posición: UR087 (Santa), UR198, UR244, AS048, QU021 y otros. Una cuerda con valor 1 constante funciona como marcador o contador de unidad, no como cantidad.
  - Otras son constantes de **cuota**: 15 y 10 (Incahuasi), 47 (UR275), 208 (UR268), 30 (UR274A), 100 (HP055, HP003) y 20 (AS156).
- **Correlación positiva entre columnas.** Aparece en 60 de 135 quipus (mediana de ρ medio 0,30; esperado 0 en N_col). **Las filas tienen un "tamaño"**: una fila grande lo es en todas sus columnas.
  - Explicación aburrida posible: secciones del quipu escritas en otra escala.
- **Proporción fija entre columnas (26).** La mitad (13 de 26) tiene una razón cercana a 1, es decir, columnas casi iguales; esto se trata en T4 como "gemelas". Solo hay razones distintas de 1 aisladas: 2 en HP017, 0,5 en UR119 y 0,4 en AS156.
- **Seriación de filas.** Es rara: 6 quipus (5 decrecientes: HP017, KH0197, UR011, UR1057, UR268; 1 creciente: AS008). **Resultado negativo** como rasgo general: las filas no están ordenadas por tamaño (no forman un *ranking*).

## T2. Arquetipos de columna entre quipus (`t2_resumen.txt`, `t2_indicadores.csv`, `t2_arquetipos.csv`)

Se definieron de antemano unos indicadores por quipu (unidad = quipu) y se comparó su recuento con un nulo conjunto de 999 iteraciones, en las que se barajan todas las matrices a la vez.

| indicador | quipus | obs. | esperado | p (Holm) |
|---|---|---|---|---|
| A1 la 1.ª columna es la mayor | 169 | **68** | 38,6 | 0,001 (0,018) |
| A5 la columna mayor es la más blanca (colores fijos, valores barajados) | 122 | **25** | 15,5 | 0,004 (0,048) |
| A6 la 1.ª columna es la más blanca (colores barajados) | 128 | **29** | 16,8 | 0,002 (0,032) |
| A7u la última columna es la más vacía | 141 | **31** | 18,5 | 0,003 (0,042) |
| A7p la 1.ª columna es la más vacía | 141 | 11 | 18,3 | inf. 0,034 (0,34) |
| A2 la última es la menor / A3 la última es la mayor / A4 la 1.ª es la menor | 169 | 34 / 25 / 49 | 31,6 / 32,1 / 40,1 | n.s. |
| A0 ρ(posición, rango) medio (¿decrecen las columnas de izquierda a derecha?) | 155 | −0,07 | 0,00 | 0,08 bilateral (n.s.) |

**Agrupamiento k-medias** de 1.129 columnas. Se usaron rasgos normalizados sin la posición: rango, magnitud relativa, % de vacías, cuota de la moda, papel de total, % de blanco y consistencia del color.

- **La estructura es débil.** La silueta con k=8 es 0,24, frente a 0,21 en el nulo (máximo del nulo 0,24). No hay "tipos" nítidos sino un continuo.
- **Los grupos sí se asocian con la posición** de forma no aleatoria: χ² = 13,7 frente a 2,6 en el nulo, p = 0,005.
  - **Columna grande** (arq. 3: rango 0,90, magnitud ×5; 164 columnas en 121 quipus): sobrerrepresentada en la 1.ª posición (×1,58) y la mitad blanca.
  - **Columna-total** (arq. 4: 6 columnas, todas de Incahuasi): siempre en la 1.ª posición.
  - **Columna blanca de tamaño medio** (arq. 2): ×1,31 en la 1.ª posición.
  - **Columna casi constante y pequeña** (arq. 5, cuota de la moda 0,78): en los bordes (×1,22 en la 1.ª, ×1,24 en la última).
  - **Columnas vacías** (arq. 1 y 6) y **columnas de color variable** (arq. 7): infrarrepresentadas en la 1.ª posición (×0,5–0,7).

**Lectura.** El único arquetipo de columna recurrente entre quipus es **"columna grande al inicio, a menudo blanca"**, más una tendencia a la **última columna vacía o pequeña**. Nivel: *apoyado con datos*.

- La columna grande **no es un total**: no es la suma de las demás salvo en Incahuasi. Es la categoría principal, la más numerosa.
- Encaja con el vocabulario "blanco ↔ mayor, primera cuerda" de 02, aunque es un efecto pequeño: 68 quipus frente a 39 esperados.

## T3. Filas (`t3_resumen.txt`, `t3_por_quipu.csv`, `t3b_*.csv`, `t3b_log.txt`)

**Número de filas.** Se comparó el recuento de cada valor con el de su vecindad x±2 (binomial con p0 = 1/5, Holm sobre 20 pruebas).

- Ningún valor "típico" sobrevive.
  - Mejores casos: R = 4 (25 frente a 15 esperados, p = 0,005, Holm 0,09); 10 grupos en el corpus (35 frente a 24, p = 0,014, Holm 0,26); K = 6 y K = 4 (p ≈ 0,03, Holm 0,6).
  - R = 10 (chunka), R = 12 y R = 6 (pachacas): nada.
  - R es múltiplo de 10 en 18 de 177 tablas.
- **Resultado negativo**: el número de filas no codifica 4 suyus, 10 ni 12 de forma detectable. Las columnas de 6 no son más frecuentes de lo que permite una distribución suave.

**Filas y cuerdas resumen.**

- **Formato "fila + cuerda-total"** (`t3b_fila_total.csv`). Es un hallazgo nuevo.
  - En 6 quipus, un grupo de una sola cuerda pegado a cada fila contiene **la suma de esa fila**, con q<0,05 frente al nulo que reasigna los valores de las cuerdas sueltas:
    - **AS044**: 6 de 11 filas, total después de la fila; esperado 0,7.
    - **UR1096** (Pachacamac): 5 de 6 filas, después; esperado 0,7.
    - **UR166** (Chancay): 2 de 4, después y antes.
    - **UR118 y UR119** (Paracas, pareja de museo): el total va *antes* de la fila. 4–5 de 6–13 exactas o a menos del 2 %; esperado 0,8–1,2.
    - **UR149**: 3 a menos del 2 %.
  - Es la misma idea que la cuerda superior-suma de AS006 (cuatro cuerdas T = total de su fila), pero con colgantes.
  - Hay cuasi-coincidencias (333 frente a 335, 497 frente a 498, 535 frente a 531): errores, cuerdas rotas o ajustes. Nivel: *bien apoyado* en esos 6 quipus, raro en el corpus.
- **Cuerdas = total de columna** (Σ de todas las filas): 6 quipus con q<0,05.
  - En HP017, UR202 y UR198 son valores redondos y frecuentes (2, 10, 20, 30, 100). Lo más probable es una coincidencia que el nulo no recoge del todo (aburrido).
  - **UR231** (Ica/Pisco) tiene 6 cuerdas intercaladas con valores distintos de tres cifras (264–411), iguales a 6 totales de columna distintos. Candidato *propuesto*.
  - Ninguna cuerda coincide con el gran total de la tabla.
  - Totales de tramos contiguos de filas: no hay exceso (2.643 frente a 2.697): **negativo**.
- **Filas resumen dentro de la tabla** (una fila = suma de las demás o acumulada): solo UR1120 y AS008. Fila = fila_i + fila_j: 0 quipus. **Negativo**: las tablas no llevan una fila de totales.
- **Filas duplicadas.** Hay 11 quipus con más pares idénticos que el azar (198 pares frente a 108 esperados): AS156 (65 pares; filas repetidas de dos en dos), UR1088 (37), UR1057, UR1121, UR1109, UR1149 (filas consecutivas 1430/670/3410/820 ×4) y UR087 (Santa).
  - En 7 quipus las copias son contiguas (40 frente a 16).
  - Lectura: duplicado o comprobación de partidas, o unidades con asignación idéntica (*propuesto*).

**¿Qué distingue a una fila?**

- Su **tamaño global**: correlación entre columnas en 60 quipus.
- A veces una **cuerda-total propia**.
- A veces una **duplicación**.
- **No el color**: la información mutua normalizada color~columna tiene mediana 0,65, frente a 0,24 para color~fila. La fila explica más color que la columna solo en 45 de 176 quipus, que son tablas en bloque al estilo de 02.
- **No el orden**: no hay seriación (solo 6 quipus).

## T4. Lecturas concretas con predicción (`t4_resumen.txt`, `t4_gemelas.csv`)

**Columnas gemelas en el corpus** (exploratorio: la hipótesis surgió al mirar T1; la prueba es con N_col y BH). Un par de columnas con |vi − vj| ≤ max(1, 2 %) aparece más de lo esperado en 23 de 119 quipus con p<0,05, pero solo 5 tienen q<0,05: UR011, UR1121, UR149, UR267B y UR269. Fuera de Incahuasi, la cosa es real pero rara.

| quipu | lectura propuesta | predicción | resultado | nivel |
|---|---|---|---|---|
| **UR267A/B, UR255, UR256, UR275, UR269, UR274B** (Incahuasi) | fila = lote o entrega; columnas = [bruto, cuota fija c, neto] | (a) bruto = c + neto; (b) c es fija, no proporcional; (c) bruto > c; (d) **nueva**: si falta c, bruto = neto; (e) **nueva**: la columna del bruto es blanca | (a) 52–100 % de filas completas (UR255 7/7, UR267B 12/13); (b) CV(c) = 0 en UR255, UR256 y UR275 frente a CV(c/bruto) 0,10–0,48: **cuota fija, no tasa**; (c) se cumple: ninguna fila con bruto ≤ c, salvo 1 en UR269; (d) **falla**: casi no hay filas para probar y, donde las hay, bruto ≠ neto (0/1, 1/11, 1/2), así que la cuota no es opcional; c cambia de posición en algunas filas (UR267A filas 23–24, UR274B); (e) bruto blanco en UR267A (25/25), UR269 (51/59), UR274B (12/12), UR275 (7/9), pero **no** en UR255 ni UR256 (todo AB) | estructura aritmética **bien apoyada** (01 y aquí); "deducción/tara/tributo" **propuesto** |
| **UR011** (Leymebamba) | fila = unidad social (ayllu o pachaca), con un bloque de 9 filas grandes (6 300–15 700) y otro de 5 pequeñas (720–3 100); col3 y col4 = dos recuentos del mismo universo (p. ej. dos fechas o dos mitades); col0–col2 = subcategorías | (a) col3/col4 ≈ 1; (b) col0–2 proporcionales a col3; (c) cuerdas fuera de tabla = totales de bloque | (a) razón mediana 1,014; DE(log) 0,25 frente a 0,69 en el nulo, p = 0,0001; 4 de 14 filas a menos del 2 %, pero nunca idénticas, así que no es una copia; (b) ρ = 0,65 / 0,84 / 0,94, p ≤ 0,006; (c) **falla**: solo cuasi-coincidencias (2 082 frente a 2 068, 2 000 frente a 1 988) | relaciones **apoyadas con datos**; "censo en dos fechas o dos mitades" **especulativo** |
| **KH0197** (procedencia desconocida) | fila = partida; col0 (blanca) y col1 (AB) = dos registros de la misma cantidad (asignado/recibido) | \|col0 − col1\| ≤ 2 % en exceso; si es asignado/recibido, signo constante | 4 filas casi iguales (533/532, 512/513, 304/305, 22/23) frente a 0,8 esperadas, p = 0,003; ρ = 0,93; signo **no constante** (−1, +1, +1, +1); las demás filas difieren mucho (−425, −98, +68) | casi-igualdad **apoyada** (post hoc, no pasa BH en el corpus); "verificación" **especulativo** |
| **UR1144** (Pachacamac) | fila = unidad; col0 = bien principal (centenas); col1–3 = bienes menores | (a) el tamaño de la fila arrastra a todas las columnas; (b) col0 ≈ múltiplo fijo del resto; (c) col0 no es el total | (a) ρ(col0, col1+2+3) = 0,65, p = 0,009; (b) razón ≈ 2,3, DE(log) 0,14 frente a 0,22, p = 0,009, pero con mucha dispersión (1,7–3,0); (c) col0 = suma del resto en 0 filas | "columna grande = categoría principal, no total" **apoyado con datos** |
| **AS178** (cerca de Lima) | fila = unidad; col1 (B) y col2 (LB) = dos mitades de una partida; col0 (blanca) = doble de col3 (KB) | (a) col1 ≈ col2; (b) col0 ≈ 2·col3; (c) col0 no es la suma | (a) 6 de 6 filas frente a 2,0, p = 0,003; (b) 5 frente a 2,1, p = 0,014; (c) 0 filas | **especulativo**: solo 7 filas y valores redondos (10, 20, 30, 60); predicciones post hoc |
| **AS044, UR1096, UR118/UR119** | fila = unidad con 6 categorías (6 colgantes); la cuerda suelta adyacente = total de la unidad | fila sumada = cuerda suelta adyacente | ver T3: 6/11, 5/6, 4–5/13, frente a ≈1 esperado, q<0,05 | **bien apoyado** como estructura; las categorías concretas, desconocidas |

## Resultados negativos

1. Fuera de Incahuasi no hay columna de totales de fila. Los totales, cuando existen, van en cuerdas aparte.
2. No hay filas-resumen dentro de la tabla, ni sumas de tramos de filas en cuerdas externas.
3. Ningún número "típico" de filas (4, 6, 10, 12) ni de columnas sobrevive a Holm.
4. No hay seriación ni *ranking* general de filas (6 de 147).
5. No hay un orden decreciente común de las columnas de izquierda a derecha (A0 n.s.); solo la 1.ª columna destaca.
6. Los arquetipos de columna no forman tipos nítidos (silueta casi igual al nulo); solo hay asociaciones débiles con la posición.
7. Proporciones distintas de 1 (½, 2, 1/10): aisladas, sin patrón compartido. Coincide con 01.
8. Incahuasi: la predicción "sin cuota, bruto = neto" falla.

## Cautelas

- **Circularidad**: la selección por columnas de magnitud infla la prueba de "columna mayor". Los indicadores entre quipus (A1, A5–A7) no dependen de qué columna se seleccionó.
- **Definición de fila = grupo modal**: deja fuera grupos de otros tamaños, que pueden ser filas con cuerdas rotas o perdidas. En UR231, muchos grupos modales están vacíos.
- **Coincidencias con valores redondos**: el nulo que baraja valores dentro de la tabla no captura del todo la abundancia de 10, 20 y 100 (HP017, UR202, UR198).
- **Las lecturas de T4 son post hoc**, elegidas tras ver T1. Sus p son ilustrativos y no confirmatorios. UR118/UR119 pueden ser dos registros del mismo objeto o del mismo archivo.

## Niveles de evidencia

| conclusión | nivel |
|---|---|
| Las tablas tienen una columna sistemáticamente mayor y otras menores (119/177) | bien apoyado (estructura; en parte circular) |
| Arquetipo recurrente: la 1.ª columna es la mayor (68 frente a 39) y tiende a ser blanca; la última, vacía o pequeña | apoyado con datos |
| Filas = unidades de tamaño variable (correlación entre columnas en 60/135) | apoyado con datos |
| Columna = total de fila solo en Incahuasi, con cuota constante | bien apoyado (replica 01); cuota fija y no tasa: apoyado con datos |
| Formato "fila + cuerda-total suelta" (AS044, UR1096, UR118, UR119, UR166, UR149) | bien apoyado en esos quipus |
| Filas duplicadas o copias (11 quipus) | apoyado con datos |
| Columnas gemelas (dos registros de la misma cantidad) en UR011, KH0197, AS178 y otros | apoyado (UR011) / exploratorio |
| Número típico de filas (decimal, 4 suyus, 6 pachacas) | sin evidencia (negativo) |
| Significado de cada columna (hombres/mujeres, productos, etc.) | especulativo: nada en los datos lo fija |

## Siguiente ronda

1. **Buscar el formato "fila + total suelto" en todo el corpus**, sin restringirse a las tablas seleccionadas. Ver si se concentra en ciertos sitios (Paracas, Pachacamac) y si el total va siempre antes o siempre después según el archivo.
2. **UR118 y UR119 (pareja de Paracas)**: emparejarlos fila a fila. ¿Son el mismo registro en dos fechas (como col3/col4 de UR011)?
3. **UR011 y el resto de Leymebamba (UR001–UR022)**: ¿se repite la estructura de dos conteos gemelos y dos bloques de filas? ¿Algún quipu del archivo contiene los totales de bloque (88 027 / 80 524 / 9 128 / 9 037)?
4. **UR231**: verificar a mano las 6 cuerdas que coinciden con totales de columna, y su color (AB/B, frente al resto).
5. **Duplicados** (AS156, UR1088, UR1149): ¿la copia tiene otro color o dirección de nudo (otra mano), lo que indicaría una verificación?
