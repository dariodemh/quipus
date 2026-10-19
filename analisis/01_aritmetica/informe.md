# 01 · Aritmética contable: ¿cuánto del corpus es contabilidad con verificación interna?

Datos: 651 quipus del KFG (`analisis/datos`). Unidad de análisis: el quipu. Cuerda ausente (valor 0 sin nudos) = hueco: se queda fija al permutar y no cuenta como sumando. Semillas fijas; B = 2000 permutaciones por quipu y nulo (B = 1000 en proporciones y potencia). Reproducible con `python 0X_*.py` (orden 01→07; `python nucleo.py` ejecuta un autotest de los detectores). Salidas de consola en `salida_*.txt`; tablas en CSV.

## 1. Relaciones de suma (detectadas por mí, igualdad exacta)

| Código | Relación |
|---|---|
| R1 | colgante/subsidiaria = suma de sus subsidiarias directas (≥2 no nulas) |
| F | colgante = suma de un tramo contiguo de colgantes pegado a su izquierda o derecha (2–10 sumandos) |
| A | como F, pero el tramo son grupos enteros (empieza/acaba en frontera de grupo) |
| TA | A restringida a cuerdas con unión T (cuerda superior) |
| R4 | grupo = suma cuerda a cuerda de 2–4 grupos contiguos del mismo tamaño |
| R5a | grupo de resumen: cada cuerda = total de un grupo contiguo (n cuerdas = n grupos) |
| R5b | total de un grupo = suma de los totales de 2–6 grupos contiguos |
| Fany | colgante = suma de **cualquier** tramo contiguo de colgantes, a cualquier distancia (definición laxa, comparable a la del KFG) |
| Fsub | subsidiaria = suma de un tramo de colgantes |
| R7 | cierre intragrupo: una cuerda = suma del resto del grupo (≥3 no nulas), sin posición (`04_cierre_intragrupo.py`) |

Nulos (todos conservan el multiconjunto de valores del quipu):
- **N1**: barajar todo el quipu.
- **N2** (principal): barajar dentro de cada nivel (colgante, subsidiaria…).
- **N3**: barajar dentro de nivel y grupo (conserva la composición y los totales de cada grupo).
- **N4**: permutar el orden de los grupos como bloques (conserva toda relación interna a un grupo y destruye la contigüidad entre grupos).

Compuesto por quipu = R1+F+R4+R5a+R5b (el nulo se calcula sobre la misma suma, así que el solapamiento entre tipos no sesga). p empírico = (1+#{nulo ≥ obs})/(B+1). BH-FDR entre quipus «testables» (nulo con varianza > 0).

### Resultados de corpus (suma sobre 651 quipus; observadas vs esperadas bajo N2)

| Tipo | Obs. | Esp. N2 | Cociente | Quipus con ≥1 (obs / esp. N2) |
|---|---|---|---|---|
| R1 | 72 | 46,4 | 1,6 | 38 / 33,9 |
| F | 1992 | 1792 | 1,11 | 364 / 342 |
| A | 561 | 425 | 1,32 | 215 / 188 |
| **TA (cuerda superior)** | **22** | **0,63** | **35** | 12 / 0,6 |
| R4 | 5 | 1,3 | 4 | 4 / 1,2 |
| R5a | 1 | 1,1 | 0,9 | 1 / 1,1 |
| R5b | 129 | 114 | 1,13 | 67 / 58 |
| Fany | 14 411 | 13 514 | 1,07 | **490 (75,3 %) / 478 (73,5 %)** |
| Fsub | 4080 | 3819 | 1,07 | 266 / 257 |
| R7 (cierre) | 168 | 84 | 2,0 | 79 / 74 |

El corpus entero tiene un exceso pequeño sobre el azar (compuesto 2199 vs 1955 en N2, p < 0,001; con N1 p = 0,10; con N3 p = 0,18; con N4 p = 0,005). Salvo tres señales (cuerdas superiores, cierres intragrupo de Incahuasi y un goteo de F/A en pocos quipus), el grueso de las coincidencias aritméticas es lo que daría el azar con esos valores.

### Por quipu (BH-FDR, compuesto)

`resultado_por_quipu.csv` trae, por quipu y tipo: obs, E, sd, p y q bajo N1–N4.

| Nulo | testables | p<0,05 (esperados por azar) | q<0,05 |
|---|---|---|---|
| N1 | 564 | 47 (28) | 10 |
| **N2 (principal)** | 548 | 55 (27) | **13 (2,0 % de 651; 2,4 % de los testables)** |
| N3 | 500 | 22 (25) | 0 |
| N4 | 403 | 15 (20) | 0 |

- Por tipo en N2 (q<0,05): F 17, A 14, **TA 6**, R1 0, R4 0, R5a 0, R5b 0, Fany 0, Fsub 0.
- Unión de tres familias (compuesto N2, TA N2, R7): **21 quipus = 3,2 % del corpus (3,8 % de los testables)**. Cada familia lleva su BH; la unión puede inflar el FDR hasta ≈3× el nominal, así que son 21 candidatos, no 21 hechos. Procedencia (museo, no origen): 8 Incahuasi, 7 sin procedencia, y uno de Nazca, Paracas, Ica, Ica-Pisco, Huacho y Huando (Gaffron).
- Los 13 de N2 son casi todos «F» (sumas de tramos de colgantes pegados): UR255, 256, 267A, 267B, 269, 275 (Incahuasi), UR113 (también 17 R1), UR119, UR166, UR1114, AS199, MM001, QU009.
- N3 y N4 no confirman nada. Es esperable por construcción, no necesariamente un negativo: N3 conserva la composición del grupo (que ya contiene la suma) y N4 conserva toda relación interna a un grupo. El test de potencia lo comprueba: una suma plantada dentro del grupo se detecta 0 % con N4, 21 % con N3 y 55 % con N2.

### Comparación con el 74 % de Medrano y Khosla

- Con un detector laxo comparable (Fany), **el 75,3 % de los quipus tiene ≥1 relación**, casi exactamente el 74 %. Pero el nulo N2 predice **73,5 %** (478 de 651): la cifra cruda es indistinguible de lo que producen valores barajados. Con el detector adyacente (F): 55,9 % observado vs 52,5 % esperado.
- Tras el control: 2,0 % (N2, compuesto) a 3,2 % (unión de familias) y 0 % con N3/N4.
- Potencia (`03_potencia.py`, planto «última cuerda del grupo = suma de las anteriores» en grupos de ≥3 cuerdas): con el 50 % de los grupos plantados se detecta (q<0,05, N2) el 34 % de los quipus plantables (47 % con p<0,05); con el 100 %, 55 %. Con 0 % plantado salen los 13 reales. Los quipus de ≤10 cuerdas (153) son casi no testables (70 testables, 0 detecciones). Lo observado (≈2–4 %) sugiere una fracción de quipus con sumas exactas locales **del orden de 5–10 %** (exceso de p<0,05 en N2: 55−27 ≈ 28 de 548, dividido por una potencia ≈ 0,47), no 74 %. Estimación gruesa.
- Cautelas: (i) mi definición exige igualdad exacta y relaciones locales; no cuenta sumas por color, indexadas ni con tolerancia; (ii) Medrano y Khosla pueden medir otra cosa («arreglos significativos» frente a pseudoquipus de tres distribuciones) y no pude reproducir su detalle; (iii) la potencia es baja en quipus pequeños o de valores pequeños, donde R1 y F aciertan por azar con valores de 1–9.

### Tipos de operación presentes

1. **Cuerda superior = suma de colgantes adyacentes (TA): demostrado.** 22 de las 63 cuerdas superiores de nivel 0 con valor > 0 (35 %) son suma exacta de un bloque adyacente de grupos (esperado 0,6 en N2; 5,5 en N4, así que también importa el orden). 6 quipus con q<0,05: AS006 (4/6), AS007 (4/10), QU009 (4/6), QU016 (2/4), AS001 (1/2), QU015 (1/5); 4 se mantienen bajo N4. Solo 17 quipus tienen cuerda superior de nivel 0: operación minoritaria y localizada, coherente con Medrano y Khosla.
2. **Cierre intragrupo (R7): una cuerda = suma del resto del grupo.** 168 vs 84 esperados (p < 0,001). 9 quipus con q<0,05, **8 de ellos Incahuasi** (UR255, 256, 266, 267A, 267B, 269, 274B, 275) más UR1152 (Ica). Patrón: grupos de 3 cuerdas `[x, c, x−c]` con una constante c por quipu: 15 en UR255 y UR267A (15 de 15 grupos), 10 en UR256 y UR267B (12 de 12), 46–47 en UR269, UR275 y UR266. Es decir x = c + resto, con c fija. **Apoyado con datos** como regularidad aritmética de Incahuasi; su lectura (parte estándar, tara, ración fija, cuota) es **propuesta/especulativa**.
3. **Sumas de colgantes vecinos (F/A) y colgante = suma de subsidiarias (R1):** exceso modesto (1,1×, 1,3×, 1,6×) repartido en pocos quipus; R1 sobre todo en UR113 (17 de las 72). **Apoyado con datos, débil.**
4. **Suma cuerda a cuerda de grupos (R4), grupo de resumen (R5a), suma de totales de grupos (R5b): resultado negativo.** 5, 1 y 129 casos frente a 1,3, 1,1 y 114 esperados; ningún quipu significativo. R4 y R5a tienen pocos casos elegibles (42 y 48 quipus testables), así que la potencia es baja.
5. **Igualdad padre-hijos o totales de grupo iguales (razón 1/1):** 575 vs 453 pares colgante–suma de subsidiarias, y 8376 vs 7615 pares de grupos con total idéntico (145 quipus con ≥1). Hay duplicación de cantidades por encima del azar a nivel de corpus (p < 0,001); ninguna individual sobrevive a BH.

## 2. Distribuciones de valores (`05_distribuciones.py`)

- **Benford.** Por quipu (n ≥ 50, 240 quipus): 148 rechazan Benford a q<0,05 (MAD mediano 0,042; solo 4 con MAD < 0,015). Pooled por magnitud (IC por remuestreo de quipus en `benford_pooled.csv`): valores de 1 dígito MAD 0,010 (0,314 de unos vs 0,301); 2 dígitos 0,419 de unos (MAD 0,031); 3 dígitos 0,439 (0,038); ≥4 dígitos 0,535 (0,062). El exceso de «1» crece con la magnitud: es la huella de un sistema posicional con pocos nudos por posición, no de Benford ni de una anomalía contable. Benford es un mal nulo aquí; **no demostrado como diagnóstico**.
- **Redondeo.** En 118 quipus con ≥40 valores ≥20, el dígito de unidades 0 es 2,65× (IC95 % 2,0–3,3, bootstrap de quipus) más frecuente que el promedio de los dígitos 2,3,4,6,7,8,9; 84 de 118 con p<0,05 (esperados ≈6), 79 con q<0,05. El 5 no sobrerrepresenta (razón mediana 1,09; 8 con q<0,05). Múltiplos de 100 en valores ≥1000: 98 vs 55 esperados por independencia de dígitos (razón 1,78; 22 quipus; 2 con q<0,05). Explicación aburrida: no es «redondeo a 5/10» sino ausencia de nudos en la posición de unidades (cuerdas que registran solo decenas o centenas) y valores usados como cuota o categoría (10, 20, 100). 22 de 118 quipus tienen > 50 % de unidades 0. **Apoyado con datos** (exceso de ceros finales), causa no determinada.
- **Valores pequeños repetidos.** Mediana de los valores del corpus = 10 (cuartiles 4 y 33); 301 quipus tienen mediana ≤ 9. Repetición (índice de Simpson) frente a lognormal discretizada ajustada al quipu: 179 de 434 con q<0,05 (esperados ≈22). Con un nulo más duro (barajar los dígitos de cada posición decimal entre cuerdas, que conserva magnitudes y ceros finales): 71 de 434 con q<0,05 y 48 en ambos nulos. Valor más repetido en los significativos: 1 (41), 10 (41), 20 (13), 2 (11), 4 (11), 100 (8). **Apoyado con datos**: en ≈11–16 % de los quipus (n ≥ 20) hay valores-categoría repetidos más allá de lo que explica la forma de los dígitos; que sean «códigos» es **propuesto**.

## 3. Proporciones fijas (`06_proporciones.py`)

Dos familias: F1 (colgante o subsidiaria vs suma de sus subsidiarias) y F2 (pares de grupos con totales ≥10). Razones exactas 1/10, 1/5, 1/4, 1/3, 1/2, 2/3, 3/4, 1 y sus inversas. Nulo N2 (B = 1000), nulo agregado de corpus y BH sobre quipu × razón.

- **Ningún quipu** tiene una proporción significativa tras BH (0 de 651 en cualquier razón y familia). El número de quipus con p<0,05 es ≤ el esperado (p. ej. 1/10: 4 vs 12 en F1; 6 vs 14 en F2).
- **1/10 (tributo): negativo.** F1 56 vs 69 esperados (p corpus = 0,96); F2 39 vs 40 (p = 0,54). Tampoco 1/2 ni 1/3 en F1 (254 vs 245; 154 vs 138).
- Excesos de corpus sin quipu individual: F2 con 1/5 (148 vs 112, p = 0,011), 1/4 (189 vs 144, p = 0,008), 1/2 (773 vs 697, p = 0,004), 3/4 (928 vs 856, p = 0,001); F1 con 2/3 (108 vs 84, p = 0,003). Son excesos del 5–30 % sobre pocas coincidencias, y N2 no conserva la sobredispersión de los totales de grupo, así que no pueden tomarse por proporciones fijas. **No demostrado.**

## 4. Tipología (`07_tipologia.py`)

536 quipus con ≥10 valores. Rasgos: log mediana y p90, fracción ≤9, cuota del valor más frecuente, razón de valores distintos, fracción de múltiplos de 10, tamaño, cuerdas por grupo, fracción de subsidiarias, profundidad, fracción de huecos, exceso de sumas (compuesto N2 y cierre R7, arcsinh del z) y presencia de cuerda superior. Estandarización, recorte en percentiles 1–99, PCA (90 % de varianza), k-means.

- **La estructura es débil**: silueta 0,15–0,19 para k = 2…8. El primer eje es un continuo «valores pequeños y repetidos ↔ valores grandes y variados». k = 2 es lo más estable (ARI bootstrap 0,91); k = 4 (ARI 0,76, silueta 0,18) da la lectura más útil. Las sumas no separan clusters: el exceso medio de sumas es ≈ 0 en todos salvo el que define la cuerda superior.
- Perfiles k = 4 (medianas):
  - **C0 «códigos/categorías»** (200 quipus, 37 %): mediana 4, 80 % de valores ≤ 9, un mismo valor ocupa el 30 % de las cuerdas, pocas subsidiarias; **0 de los 21 quipus con aritmética verificada**.
  - **C1 «registros jerárquicos»** (139): grandes (120 cuerdas), 43 % subsidiarias, profundidad 2, mediana ≈10; 5 de los 21.
  - **C2 «cuerda superior»** (16): definido por la unión T y señal de suma (z = 1,07); 6 de los 21 (AS001, AS006, AS007, QU009, QU015, QU016). Es cluster casi por construcción.
  - **C3 «conteo/medida»** (181, 34 %): mediana ≈ 44, solo 8 % de valores ≤ 9, 75 % de valores distintos, sin subsidiarias; 10 de los 21 (Incahuasi, UR113, MM001…).
  Dos géneros robustos: **códigos** (valores pequeños, repetitivos, sin sumas detectadas) y **conteo/medida** (valores grandes, variados), con una familia jerárquica intermedia y un grupo pequeño con cuerda superior. Etiquetas **propuestas**. El 0/21 de C0 puede deberse en parte a potencia baja con valores pequeños.
- **Cruce con procedencia** (8 procedencias con ≥8 quipus, sin Unknown; permutación de etiquetas dentro de cada colección AS/UR/HP/JC/…, 4000 permutaciones): χ² = 66,6, p = 0,0005, V de Cramér = 0,32 (k = 4); con k = 2, p = 0,024. Celda con q<0,1 en k = 4: **Huaquerones sobrerrepresentada en C0 (códigos), 10 de 12 vs 3,7 esperados (q = 0,008)**. Con k = 2, Nazca y Huaquerones tienden al cluster de valores pequeños e Incahuasi y Leymebamba al de valores grandes (q ≈ 0,07). Reparto (C0/C1/C3): Incahuasi 10/14/16, Pachacamac 20/19/39, Ica 11/5/21, Leymebamba 5/11/5. **Apoyado con datos** que la procedencia no es independiente del género aritmético (controlando colección); **propuesto** cualquier lectura regional. La procedencia es de museo (no origen) y está confundida con la colección: todos los JC son Incahuasi y el control por prefijo no los separa.

## Resultados negativos
- El 74 % de quipus «con aritmética» es lo esperado por azar con valores barajados; tras el control queda 2–3 %.
- R4, R5a, R5b, proporciones (1/10, 1/2, 1/3…), diagnóstico Benford y «redondeo a 5»: sin evidencia.
- N3 y N4 no confirman ningún quipu de N2 (limitación de diseño y de potencia, no refutación).
- Los clusters no se separan por sumas; la tipología es un continuo.

## Niveles de evidencia
- **Demostrado:** cuerdas superiores = suma de grupos adyacentes en un puñado de quipus (22 de 63 cuerdas; 6 quipus q<0,05, 4 también bajo N4); cierres `[x, c, x−c]` en Incahuasi con c constante por quipu.
- **Apoyado con datos:** exceso pequeño de sumas F/A/R1 en el corpus; repetición de valores-categoría (≈11–16 % de quipus); exceso de unidades 0; dependencia procedencia–género tras control por colección; gran parte del «74 %» es tasa base.
- **Propuesto:** c como cuota/tara; géneros «códigos» vs «conteo»; 10/20/100 como categorías.
- **Especulativo:** cualquier lectura calendárica o demográfica de los valores; el significado de la constante.

## Siguiente ronda
1. Estudiar los grupos Incahuasi `[x, c, x−c]`: qué cuerda es x (color, unión R/V, posición, pares atados entre quipus); si el 0 de `[112,15,0]` es un hueco de decodificación; si c coincide entre quipus pareados (UR255–UR267A).
2. Repetir R7 y TA con tolerancia ±1 y con sumas que incluyan subsidiarias (totales de colgante); añadir sumas por color e indexadas, que mi detector no cubre.
3. Nulos con dependencia de vecindad (permutación de bloques de longitud k) para quipus de valores pequeños, y potencia calibrada por tamaño.
4. Separar los ceros finales entre cuerdas «solo decenas» y unidades faltantes por deterioro (campos `notas`, `nudos`).
5. Cruzar los 21 candidatos con el análisis cromático: ¿los sumandos comparten color?
