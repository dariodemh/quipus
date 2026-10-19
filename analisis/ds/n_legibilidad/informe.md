# ds/n_legibilidad · Mapa de legibilidad de los 651 quipus

**Equipo:** n_legibilidad · **Fecha:** 18/10/2026 · **Semilla:** 20261018
**Datos (solo lectura):** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `quipus.csv`, `grupos.csv`.
**Scripts (en orden):** `motor.py` → `05_inter.py` → `06_mapa.py` → `09_analisis.py` → `10_placebo.py` → `11_fuera_muestra.py` → `12_cifras.py`. Los `00`–`04` son exploratorios.
**Salidas:** `quipus_legibles.csv` (el mapa, una fila por quipu), `cuerdas_legibles.csv` (una fila por cuerda), `reglas_resumen.csv`, `por_procedencia.csv`, `pares_copia.csv`, `inter_pred.csv`, `top20_fuera_incahuasi.csv`, `modelo_ols.csv`, `nulo_resumen.npz`.

---

## 1. Pregunta

El motor de `19_prediccion` reconstruyó a ciegas el 50,8 % de las cuerdas de 13 quipus de Incahuasi. ¿Qué fracción de **cada** quipu del corpus es reconstruible a partir del resto con reglas estructurales declaradas de antemano, y qué explica esa legibilidad? ¿Hay «géneros» legibles (contables) frente a ilegibles? ¿Qué quipus fuera de Incahuasi son candidatos a sistemas nuevos?

## 2. Definiciones

- **Cuerda con valor:** 40 162 de las 57 818 (69,5 %). Los `0` con `nudos` vacío son ausentes y quedan fuera (regla 6 del brief). 10 quipus no tienen ninguna cuerda con valor.
- **Legible (LOO):** se oculta una cuerda, se aplican todas las reglas usando solo las demás, y la cuerda cuenta como legible si **alguna** predicción es exacta. Una cuerda puede tener 0, 1 o varias «vías» (reglas que disparan sobre ella).
- **Índice de legibilidad de un quipu:** `tasa = aciertos / cuerdas con valor`. **Tasa neta** = `tasa − nulo`, donde el nulo es la media de la misma maquinaria con los valores barajados dentro del quipu.
- **Cobertura** = fracción de cuerdas con al menos una vía. **Acierto si vía** = aciertos / cuerdas con vía.

## 3. Método

### 3.1 Reglas declaradas a priori

Ninguna regla usa el valor de la cuerda objetivo ni para formularse ni para elegir la pareja. Las puertas («este quipu cierra», «esta pareja es copia») se calculan **excluyendo** la cuerda/posición objetivo.

| # | Regla | Predicción | Condición |
|---|---|---|---|
| 1 | `subs` | padre = Σ hijas inmediatas presentes | ≥2 hijas |
| 2 | `subs_res` | hija = padre − Σ otras hijas | ≥2 hermanas presentes |
| 3 | `hija_unica` | padre = su única hija / hija = padre | 1 hija presente |
| 4 | `superior` | unidad T = Σ colgantes del grupo adyacente anterior (si no, siguiente) | unidad con `union=T` o padre de colgantes T; ≥2 sumandos |
| 5 | `grupo_total` | colgante solo en su grupo = Σ colgantes del grupo anterior | no es unidad T; ≥2 sumandos |
| 6 | `cierre` | 1.ª colgante = Σ resto; y cada partida = cabecera − Σ otras | grupo con ≥3 colgantes; ≥50 % de los **otros** grupos cierran y ≥4 evaluables |
| 7 | `copia_quipu` | X[i] = Y[i+d] | misma procedencia (≠ Unknown), tamaños 0,5–2,5; `d` y su recuento estimados **sin** la cuerda i; ≥K aciertos (K = 40 % del menor) y offset único |
| 8 | `copia_grupo` | X[g,k] = Y[h,k+e] | offset local `e` estimado sin la cuerda; ≥3 posiciones y ≥60 % de acuerdo |
| 9 | `suma_dos` | X[i] = A[i+dₐ] + B[i+d_b] | A,B par de copia; ≥2 posiciones vecinas ya suman (≥60 %) |

Se **excluyó deliberadamente la «cuota»** de 19: su propio informe demuestra que equivale a la moda del quipu y no discrimina frente a la línea base.

### 3.2 Corrección de una fuga (importante para el equipo)

La primera implementación de `copia` usaba las anclas del alineamiento LCS completo y comprobaba que el hueco entre anclas vecinas fuera equilibrado. Se auditó enmascarando el valor objetivo y repitiendo el alineamiento (`contra` de `comun19.py`): **en 238 de 300 predicciones la pareja desaparece al ocultar el valor**, es decir, el ancla se había elegido mirando el valor oculto. Aquella versión daba 47 % de acierto en 2 052 predicciones; era en buena parte un artefacto de condicionar el alineamiento a que los valores ya casaran. Se sustituyó por el modelo de **offset** (§3.1, reglas 7–9), que no mira el valor objetivo. Todos los números de este informe son de la versión corregida.

### 3.3 Nulo y comparaciones múltiples

- **Nulo:** 1 000 permutaciones de los valores **dentro de cada quipu** (posiciones, grupos, estructura, colores y multiconjunto de valores fijos). En cada permutación se rehacen también las puertas (`cierre`, evidencia de `suma_dos`). Para las reglas entre quipus, el conjunto de parejas candidatas queda fijo y se barajan los valores: el nulo mide cuánto de lo observado se explica por la repetición de valores del propio quipu.
- **p por quipu:** `(1 + #{nulo ≥ observado}) / 1001`; mínimo 0,001.
- **Corrección:** Benjamini–Hochberg sobre los 641 quipus con valor.
- **Agregados:** suma de aciertos por procedencia frente a la distribución nula agregada (mismas 1 000 permutaciones), con BH sobre las 21 procedencias con ≥5 quipus.

---

## 4. Resultados

### 4.1 Global

| Métrica | Valor |
|---|---|
| Cuerdas con valor | 40 162 |
| Con ≥1 vía | 16 266 (40,5 %) |
| Con acierto exacto | **1 565 (3,90 %)** |
| Esperado por azar (nulo) | 1 029 (2,56 %) |
| Exceso | **+536 cuerdas (+1,34 puntos)** |
| Acierto si hay vía | 9,6 % |
| Sin ninguna vía | 59,5 % |

El agregado es significativo (p = 0,001, el mínimo con 1 000 permutaciones), pero el tamaño del efecto es pequeño: **solo 1,3 puntos por encima del azar**. La media engaña: la distribución está muy concentrada.

| Distribución por quipu | n |
|---|---|
| Quipus con **cero** aciertos | 448 / 641 (69,9 %) |
| Quipus con q < 0,05 (BH) | **17** (2,6 %) |
| Quipus con tasa neta > 10 % | 24 |
| Quipus con tasa neta > 25 % | 10 |
| Cuerdas que viven en quipus significativos | 2 259 (5,6 % del total) |

Percentiles de la tasa neta: p50 = 0,000; p75 = 0,000; p90 = 0,049; p95 = 0,090; p99 = 0,404.

**Lectura:** la legibilidad no es una propiedad gradual del corpus. Es un fenómeno de **minoría**: dos tercios de los quipus no tienen ni una sola cuerda reconstruible por estas vías, y el efecto agregado lo producen unas pocas decenas de quipus.

### 4.2 Por regla

Cuerdas cubiertas (con vía), aciertos exactos y tasa nula con la misma maquinaria:

| Regla | Quipus | Cuerdas | Aciertos | Tasa | Nulo | Exceso |
|---|---:|---:|---:|---:|---:|---:|
| `cierre` | 6 | 260 | 108 | **0,415** | 0,005 | **+0,410** |
| `superior` | 25 | 72 | 23 | **0,319** | 0,004 | **+0,316** |
| `grupo_total` | 264 | 679 | 47 | 0,069 | 0,014 | +0,055 |
| `subs_res` | 234 | 5 056 | 212 | 0,042 | 0,014 | +0,028 |
| `subs` | 234 | 1 800 | 72 | 0,040 | 0,017 | +0,023 |
| `hija_unica` | 377 | 8 864 | 998 | 0,113 | 0,098 | +0,015 |
| `copia_quipu` | 8 parejas (4 con aciertos) | 153 | 107 | 0,699 | 0,333 | +0,366 |

- **`cierre` es la regla fuerte**: 41,5 % exacta y cubre 260 cuerdas. Se concentra en tres quipus de Incahuasi (UR267A 45/69, UR255 27/41, UR267B 36/92) y aporta algo en UR074 (6/32), UR029 (1/17) y nada en KH0057 (0/9). Es el patrón «cabecera = cuota + partidas que suman la cabecera» que 13 ya había visto en UR267A/UR255/UR267B.
- **`superior`**: 23/72 = 31,9 % frente a 0,4 % del nulo, en 25 quipus. Confirma y generaliza `t_cuerdas_superiores`: cuando hay cuerda T, su valor suele ser la suma del grupo adyacente, pero solo hay 72 cuerdas así en todo el corpus. **Potencia:** los tres quipus que sostienen `cierre` son significativos por sí solos (q < 0,05); ninguno de los 25 con T lo es, porque 1–3 aciertos por quipu no bastan para superar BH. La regla `superior` está apoyada cuerda a cuerda, no a nivel de quipu.
- **`hija_unica` engaña**: 11,3 % de acierto parece alto, pero el nulo es 9,8 %. Una subsidiaria única **no** repite el valor del padre en general (9,1 % de igualdad bruta). El exceso es de 1,5 puntos y procede de ~20 quipus con un patrón propio (p. ej. UR017: 30 aciertos frente a 3,8 esperados; UR1130: 14 frente a 3,9). En el resto es ruido.
- **`subs` y `subs_res` son casi nada**: 4 % de acierto frente a 1,4–1,7 % del nulo. La hipótesis habitual «el colgante es la suma de sus subsidiarias» **no se sostiene** en el corpus: solo 72 de 1 800 padres con ≥2 hijas cumplen la igualdad, y 212 de 5 056 hijas se reconstruyen como residual. En UR270 (297 cuerdas, 219 subsidiarias) hay **241 vías y 0 aciertos**: sus subsidiarias no suman a sus padres ni una vez.

### 4.3 Mapa por procedencia

Solo las 21 procedencias con ≥5 quipus. `neta` = (aciertos − nulo)/cuerdas; `q` es BH sobre el agregado por procedencia.

| Procedencia | Quipus | Cuerdas | Cobertura | Tasa | **Neta** | q |
|---|---:|---:|---:|---:|---:|---:|
| near Lima | 5 | 80 | 0,40 | 0,175 | **0,122** | 0,013 |
| Huaquerones | 16 | 472 | 0,37 | 0,193 | **0,097** | 0,005 |
| Nazca | 13 | 2 095 | 0,58 | 0,068 | 0,038 | 0,005 |
| Incahuasi | 52 | 3 980 | 0,48 | 0,057 | 0,038 | 0,005 |
| Chancay, Central Coast | 5 | 81 | 0,24 | 0,049 | 0,028 | 0,35 |
| Huacho | 5 | 443 | 0,20 | 0,050 | 0,026 | 0,024 |
| Peru | 5 | 254 | 0,21 | 0,039 | 0,016 | 0,25 |
| Unknown | 233 | 12 900 | 0,38 | 0,040 | 0,015 | 0,005 |
| Valle de Ica…Ocucaje | 8 | 351 | 0,68 | 0,023 | 0,012 | 0,24 |
| Leymebamba | 22 | 3 602 | 0,44 | 0,054 | 0,009 | 0,063 |
| Paracas | 7 | 596 | 0,64 | 0,015 | 0,008 | 0,16 |
| Pachacamac | 87 | 4 183 | 0,34 | 0,026 | 0,007 | 0,024 |
| Armatambo, Huaca San Pedro | 11 | 269 | 0,02 | 0,007 | 0,006 | 0,35 |
| Ica | 47 | 2 169 | 0,32 | 0,018 | 0,003 | 0,36 |
| Hacienda Ullujalla y Callengo | 7 | 318 | 0,60 | 0,031 | −0,000 | 0,74 |
| Between Ica and Pisco | 8 | 486 | 0,31 | 0,016 | −0,002 | 0,81 |
| Marquez | 6 | 174 | 0,18 | 0,000 | −0,002 | 1,00 |
| Playa Miller #6, Arica | 5 | 384 | 0,76 | 0,016 | −0,003 | 0,81 |
| Eduard Gaffron | 10 | 139 | 0,42 | 0,000 | −0,005 | 1,00 |
| Santa | 6 | 901 | 0,40 | 0,017 | −0,029 | 1,00 |
| Atarco | 6 | 218 | 0,67 | 0,138 | −0,045 | 1,00 |

- «near Lima» y «Huaquerones» encabezan la tabla, pero por motivos distintos: near Lima por un solo quipu (UR1130, repetición padre-hija) y Huaquerones por las parejas de copia y por el candidato de suma (§4.9).
- **Incahuasi no es especial**: 3,8 % neto, en la media de las procedencias grandes.
- **Santa y Atarco tienen tasas brutas altas (0,017 y 0,138) y netas negativas**: sus valores son tan repetitivos que el azar explica todo. Es el mejor ejemplo de por qué hace falta el nulo.
- Pachacamac (87 quipus, la mayor colección) es prácticamente ilegible: 0,7 % neto.

### 4.4 Tamaño y rasgos estructurales

| Cuerdas con valor | Quipus | Cobertura | Tasa | Neta | Significativos |
|---|---:|---:|---:|---:|---:|
| <10 | 113 | 0,21 | 0,000 | −0,000 | 0 |
| 10–19 | 104 | 0,30 | 0,008 | 0,004 | 2 |
| 20–49 | 194 | 0,31 | 0,022 | 0,013 | 4 |
| 50–99 | 114 | 0,36 | 0,022 | 0,013 | 4 |
| 100–199 | 83 | 0,41 | 0,029 | 0,020 | 4 |
| ≥200 | 43 | 0,49 | 0,014 | 0,007 | 3 |

La cobertura **sí** crece con el tamaño (21 % → 49 %), pero el acierto no: los quipus grandes tienen más vías y más oportunidades de fallar. La tasa neta tiene un máximo suave en 100–199 cuerdas y cae en los gigantes.

| Rasgo | n | Neta | Cobertura | Significativos |
|---|---:|---:|---:|---:|
| Tiene cuerdas T | 26 | 0,021 | 0,47 | 0 / 26 |
| No tiene T | 625 | 0,009 | 0,32 | 17 / 625 |
| Tiene subsidiarias | 435 | 0,009 | 0,46 | 13 / 435 |
| No tiene subsidiarias | 216 | 0,011 | 0,05 | 4 / 216 |
| Tiene predicciones de copia | 10 | **0,273** | 0,71 | 4 / 10 |
| No tiene | 641 | 0,006 | 0,33 | 13 / 641 |

- Las cuerdas T **suben la cobertura** (0,47 frente a 0,32) pero no la tasa neta (0,021 frente a 0,009; ningún quipu con T es significativo tras BH). La regla funciona cuando dispara, pero hay muy pocas T.
- Las subsidiarias tampoco marcan diferencia: `subs`/`subs_res` disparan mucho y aciertan poco.
- Lo único que separa de verdad es **tener una copia**: 10 quipus con 27,3 % neto frente a 0,6 % del resto.

### 4.5 ¿Qué explica la legibilidad? (OLS con bootstrap)

Unidad = quipu; n = 532 (≥10 cuerdas con valor, sin los 6 quipus de copias literales). Variable dependiente: tasa neta. IC del 95 % por bootstrap de quipus (2 000 réplicas). **R² = 0,064.**

| Variable | Coef. | IC 95 % | ¿Significativo? |
|---|---:|---|---|
| log(cuerdas con valor) | +0,0127 | [0,0059; 0,0197] | sí |
| diversidad de valores (distintos/total) | +0,0193 | [−0,0023; 0,0416] | no |
| cuerdas por grupo | −0,0005 | [−0,0011; −0,0000] | apenas |
| fracción de subsidiarias | +0,0096 | [−0,0154; 0,0346] | no |
| n.º de cuerdas T | +0,0000 | [−0,0017; 0,0037] | no |
| dummies de procedencia (ref. Incahuasi) | — | todas cruzan 0 | no |

**Ningún rasgo estructural explica gran cosa.** El tamaño aporta +1,3 puntos por cada e-fold, y el resto es idiosincrático. Dicho de otro modo: la legibilidad es una propiedad de **quipus concretos**, no de clases de quipus.

### 4.6 «Géneros» de quipu

Clasificación por la regla que aporta la mayoría de los aciertos de cada quipu:

| Género | Quipus | Cobertura | Acierto si vía | **Neta** | Significativos |
|---|---:|---:|---:|---:|---:|
| aditivo interno (`cierre`/`superior`/`grupo_total`/`subs`) | 40 | 0,56 | 0,21 | **0,081** | 8 |
| copia entre quipus | 11 | 0,61 | 0,56 | **0,282** | 4 |
| mixto | 15 | 0,28 | 0,21 | 0,035 | 0 |
| repetición jerárquica (`hija_unica`) | 145 | 0,52 | 0,21 | 0,033 | 5 |
| **sin redundancia** (0 aciertos) | 430 | 0,23 | 0,00 | −0,012 | 0 |

Sí hay géneros, pero no los que se esperaban:

1. **Aditivo interno** (40 quipus): grupos que cierran, totales de grupo, cuerdas T. Es el género «contable» de verdad; su neto es 8,1 %. Los tres quipus fuertes son UR267A/UR255/UR267B (Incahuasi); fuera de ahí, AS080, AS001, UR113, UR166.
2. **Copia** (11 quipus): el más legible (28,2 %) pero **no es contabilidad**: son el mismo objeto o una copia literal (§5.3).
3. **Repetición jerárquica** (145 quipus): el padre se repite en su única hija. Es redundancia trivial, no aritmética; neto 3,3 % y solo 5 significativos.
4. **Sin redundancia** (430 quipus, 67 %): ninguna vía acierta. Aquí están las «listas» y los quipus no numéricos: el 30 % de las cuerdas del corpus no tienen valor y las que lo tienen no se relacionan por suma con nada.

**No aparece un género «no numérico» distinto**: los quipus con muchas cuerdas sin nudos simplemente caen en «sin redundancia» o tienen coberturas altas con acierto nulo (la vía existe pero el valor no suma).

### 4.7 Incahuasi: el 51 % no generaliza

Los 13 quipus del sistema de 19, con las reglas generales de este trabajo:

| Quipu | Cuerdas | Vías | Aciertos | Tasa neta |
|---|---:|---:|---:|---:|
| UR267A | 76 | 69 | 45 | **0,588** |
| UR255 | 65 | 43 | 27 | **0,413** |
| UR267B | 106 | 106 | 38 | **0,352** |
| UR266 | 120 | 36 | 4 | 0,020 |
| UR269 | 218 | 56 | 3 | 0,012 |
| UR278 | 292 | 36 | 2 | 0,006 |
| UR256 | 99 | 0 | 0 | 0,000 |
| UR273B | 33 | 2 | 0 | 0,000 |
| UR273A | 23 | 0 | 0 | 0,000 |
| UR274A/B | 115 | 7 | 0 | ≈0 |
| UR275 | 114 | 14 | 0 | −0,005 |
| UR270 | 297 | 241 | **0** | −0,007 |
| **Total** | **1 558** | 610 (39,1 %) | **119 (7,6 %)** | **0,073** |

El 50,8 % de 19 **no se reproduce** con reglas declaradas a priori y sin alineamientos hechos a mano: se queda en 7,6 %. La diferencia tiene tres causas identificables:
1. 19 incluía la **cuota** (≈1/3 de sus predicciones), que es la moda del quipu.
2. 19 usaba correspondencias **específicas** (`celda270`, `fila278`, A+B) descubiertas mirando esos mismos 13 quipus; aquí solo se aplica el offset genérico.
3. Las reglas que sí generalizan (`cierre`) solo funcionan en los tres quipus de grupos que cierran.

UR270 es el caso más claro: 241 cuerdas tienen vía (casi todas por `subs`) y **ninguna** acierta. UR278, UR266 y UR269, que en 19 se «leían» por tablas, aquí son ilegibles.

### 4.8 Top 20 fuera de Incahuasi: no hay sistemas nuevos, hay cuatro explicaciones aburridas

Criterio: ≥20 cuerdas con valor, sin los quipus de copia literal, ordenado por tasa neta. La columna «por qué» da las reglas que aportan los aciertos.

| # | Quipu | Procedencia | Cuerdas | Aciertos | Nulo | Neta | Por qué | q |
|---|---|---|---:|---:|---:|---:|---|---:|
| 1 | UR1130 | near Lima | 26 | 14 | 3,9 | 0,39 | `hija_unica` (14) | 0,038 |
| 2 | UR017 | Leymebamba | 103 | 30 | 3,8 | 0,25 | `hija_unica` (30) | 0,038 |
| 3 | AS080 | Unknown | 38 | 10 | 1,2 | 0,23 | `subs_res` (6), `subs` (2) | 0,061 |
| 4 | UR204 | Unknown | 65 | 15 | 1,6 | 0,21 | `hija_unica` (12) | 0,038 |
| 5 | AS001 | Unknown | 31 | 6 | 1,2 | 0,15 | `hija_unica` (2), `subs_res` (2), `superior` (1) | 0,366 |
| 6 | UR113 | Nazca | 723 | 101 | 12,2 | 0,12 | `subs_res` (74), `subs` (17) | 0,038 |
| 7 | UR048 | Pueblo Libre | 51 | 7 | 1,2 | 0,11 | `subs_res` (6), `subs` (1) | 0,119 |
| 8 | UR074 | Huaquerones | 71 | 24 | 16,3 | 0,11 | `hija_unica` (24) | 0,155 |
| 9 | UR166 | Huando, Chancay | 28 | 3 | 0,0 | 0,11 | `grupo_total` (3) | 0,038 |
| 10 | UR093 | Unknown | 338 | 58 | 23,2 | 0,10 | `hija_unica` (32), `subs_res` (21) | 0,038 |
| 11 | UR254 | Pachacamac | 28 | 5 | 2,1 | 0,10 | `hija_unica`, `subs_res` | 0,787 |
| 12 | UR053E | Unknown | 105 | 14 | 3,7 | 0,10 | `hija_unica` (14) | 0,061 |
| 13 | AS153 | Unknown | 39 | 6 | 2,2 | 0,10 | `subs_res` (4), `subs` (2) | 0,787 |
| 14 | UR057 | Atarco | 42 | 14 | 9,9 | 0,10 | `hija_unica` (14) | 1,000 |
| 15 | UR103 | Unknown | 34 | 8 | 4,8 | 0,09 | `hija_unica` (8) | 0,965 |
| 16 | UR1135 | Ica | 21 | 2 | 0,0 | 0,09 | `hija_unica` (2) | 0,246 |
| 17 | MM019 | Unknown | 218 | 34 | 13,9 | 0,09 | `hija_unica` (34) | 0,038 |
| 18 | UR202 | Pachacamac | 77 | 10 | 3,1 | 0,09 | `hija_unica` (10) | 0,207 |
| 19 | HP046_A | Unknown | 36 | 4 | 0,8 | 0,09 | `hija_unica` (4) | 0,562 |
| 20 | UR021 | Leymebamba | 137 | 24 | 12,6 | 0,08 | `hija_unica` (24) | 0,119 |

**Ninguno es un sistema nuevo comparable a Incahuasi.** Se reparten en tres clases:
- **Repetición padre-hija** (13 de 20): el valor del colgante se repite en su única subsidiaria. Redundancia real en esos quipus (el nulo es bajo), pero no aritmética: no hay nada que «leer» salvo la duplicación. Candidatos a estudiar como formato de registro, no como sistema contable.
- **Aritmética de subsidiarias** (AS080, UR113, UR048, AS153, UR093): el padre se reconstruye como residual de sus hijas en el 10–20 % de los casos. **UR113** (Nazca, 723 cuerdas) es el mejor candidato del corpus fuera de Incahuasi: 74 residuales exactos, consistente con la lectura profunda de `k_UR113`. Merece una pasada con las reglas de 19 adaptadas a su estructura.
- **Total de grupo** (UR166): 3 aciertos de `grupo_total`, nulo 0. Es el único quipu del top con una vía aditiva de grupo fuera de Incahuasi, pero n = 3.
- Los quipus con q > 0,10 (UR254, AS153, UR057, UR103, UR1135, UR202, HP046_A, UR021, UR074) **no sobreviven a la corrección múltiple**: su exceso es compatible con el azar.

### 4.9 El candidato Huaquerones (suma de dos registros)

La única estructura nueva que aparece es un grupo de quipus de **Huaquerones**: UR060 y UR074 actúan como registros A y B, y UR064, UR072, UR075, UR076, UR079 como registros X con X ≈ A + B en posiciones alineadas. La regla `suma_dos`, estimando el offset **solo con posiciones pares** y evaluando en las impares, da **20/36 = 55,6 %** de aciertos en 7 quipus, frente a **37,1 %** con offsets aleatorios (200 offsets por triple). El exceso es de +18 puntos, con n = 36 posiciones y 7 quipus.

Es **sugerente pero no demostrado**: los valores son enteros pequeños (1–6), donde las sumas aparecen por azar con facilidad, y el null de offsets aleatorios no corrige la elección del par (A,B). Se propone como candidato a verificar en los objetos y a replicar con un null que baraje los pares (A,B), no solo el offset.

---

## 5. Controles

### 5.1 Nulo dentro del quipu

Es el control central. Para cada quipu se barajan los valores entre sus propias cuerdas (1 000 veces), preservando multiconjunto, posiciones, grupos, colores y estructura. Se rehacen las puertas. El nulo esperado es 2,56 % de aciertos; el observado, 3,90 %. **El exceso es de 1,34 puntos, no de 3,90.** Todos los porcentajes de este informe son netos salvo que se diga «bruto».

Además, el nulo reproduce dos efectos esperados y sirve de autocomprobación:
- `hija_unica` cae del 11,3 % al 9,8 % (casi todo el «acierto» era la repetición de valores pequeños).
- Santa y Atarco pasan de tasas brutas altas a netas negativas.

### 5.2 Multiplicidad

- **Por quipu:** p < 0,05 sin corregir: 52 de 641; tras BH quedan **17** (2,6 %). La corrección elimina dos tercios de los «significativos».
- **Por procedencia:** BH sobre 21 → 7 significativas (near Lima, Huaquerones, Nazca, Incahuasi, Huacho, Unknown, Pachacamac). De ellas, Pachacamac es significativa solo porque tiene 87 quipus y un efecto minúsculo (0,7 %); el tamaño del efecto no es relevante.
- **Por regla:** las reglas se declaran antes de mirar los datos y se reportan todas, incluidas las que fallan. No se hace búsqueda de subconjuntos (el brief lo prohíbe y `k_UR113`/`t_alt` muestran que aparecen por azar).

### 5.3 Copias: placebo y fuera de muestra

- **Placebo entre procedencias distintas:** la misma maquinaria de offset sobre parejas de procedencia distinta y tamaño similar dispara solo **25 predicciones** (frente a 323 reales con las dos reglas de copia, 8 %) con 56 % de acierto. Las 16 de `copia_quipu` que disparan tienen 87,5 % de acierto: probablemente son **copias con etiqueta de museo distinta** (el brief advierte que la procedencia no es el origen). La especificidad de la regla está en **cuántas veces dispara**, no en el acierto.
- **Fuera de muestra (offset con posiciones pares, evaluación en impares):** `copia_quipu` dispara en 8 parejas (153 predicciones); 4 concentran 135. De esas cuatro, dos pasan la prueba con el mismo offset en ambas mitades (**AS125/UR247**: 7/7 y 7/8; **UR066/UR067**: 6/6 y 10/11), y ambas son **duplicados de base de datos / copias literales ya conocidas** por `14_copias`. UR179/UR180 cambia de offset (−6 vs −4; 3/5 y 4/5): copia parcial. UR060/UR074 cambia de −19 a −44 (16/23 y 10/22): **no es una copia global**, el ajuste in-sample era un artefacto de barrer offsets. Las otras 4 parejas (18 predicciones, p. ej. UR1097/HP031) tienen 0 aciertos.
- **`copia_grupo` no se sostiene:** baja del 61,8 % in-sample al **34,8 %** out-of-sample en 1 904 predicciones. Se excluyó del índice principal.
- **`suma_dos`:** ver §4.9 (el único que sobrevive, y con reservas).
- **Duplicados:** 3 parejas con ≥8 predicciones y ≥75 % de valores idénticos: UR066/UR067 (17, 94 %), AS125/UR247 (15, 93 %), UR179/UR180 (11, 82 %). Las dos primeras están documentadas en `14_copias` como familia de copia y duplicado de base; la tercera es nueva. En total, 6 quipus implicados. Se excluyen de los análisis de rasgos y del top 20.

### 5.4 Acuerdo entre vías

Solo **2 cuerdas** de 40 162 tienen dos reglas distintas que aciertan. La «doble entrada» que en 19 daba una señal de fiabilidad (77 % de acierto cuando dos vías coincidían) **no existe** en el corpus general: las vías son casi siempre una sola y no se cruzan. Es un resultado negativo importante: no hay redundancia suficiente para validar internamente las lecturas.

---

## 6. Resultados negativos

1. **La suma de subsidiarias no existe como regla general.** 72/1 800 padres (4,0 %) frente a 1,7 % del nulo. El ratio mediano Σhijas/padre es 0,73, no 1. UR270: 241 vías, 0 aciertos.
2. **Una subsidiaria única no copia al padre.** 9,1 % de igualdad bruta; el nulo es 9,8 % para la regla. El «género» de repetición jerárquica es real en ~20 quipus, pero no es la norma.
3. **La legibilidad no es gradual ni ubicua.** 448/641 quipus con cero aciertos; 430 en «sin redundancia».
4. **El 51 % de Incahuasi no generaliza.** 7,6 % con reglas a priori; UR270, UR278, UR266, UR269, UR275 y UR273/274 son ilegibles.
5. **La cuota no se usa** (es la moda) y, sin ella, la legibilidad de Incahuasi cae en picado.
6. **Las copias de grupo no sobreviven fuera de muestra** (61,8 % → 34,8 %).
7. **La suma de dos registros** solo aparece como candidato en Huaquerones y con n pequeño (36 posiciones).
8. **Ningún rasgo estructural explica la legibilidad** (R² = 0,064): ni T, ni subsidiarias, ni tamaño, ni procedencia. Es idiosincrática.
9. **No hay acuerdo entre vías** (2 cuerdas con dos aciertos): no se puede validar una lectura con otra.
10. **Los quipus grandes no son más legibles**: cobertura alta (49 %), tasa neta baja (0,7 % en ≥200 cuerdas).

---

## 7. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| El corpus es mayoritariamente **no legible** por reglas estructurales: 3,90 % exacto frente a 2,56 % del nulo; 70 % de quipus con cero aciertos | **Demostrado** (nulo explícito, 1 000 permutaciones, BH) |
| `cierre` (cabecera = cuota + partidas) es real y fuerte (41,5 % vs 0,5 %) en UR267A/UR255/UR267B y poco más | **Apoyado con datos** (n = 260, 6 quipus; coincide con 13) |
| `superior` = suma del grupo adyacente (31,9 % vs 0,4 %) | **Apoyado con datos** (n = 72, 25 quipus; coincide con `t_cuerdas_superiores`) |
| La suma de subsidiarias **no** es una regla general del corpus (4,0 % vs 1,7 %) | **Apoyado con datos** |
| Las copias entre quipus son **literales** (duplicados), no un sistema de registros relacionados | **Apoyado con datos** (placebo + fuera de muestra) |
| El 51 % de Incahuasi no generaliza (7,6 % con reglas a priori) | **Apoyado con datos** |
| Hay «géneros»: aditivo interno (40 quipus), repetición jerárquica (145), sin redundancia (430) | **Apoyado con datos** (descriptivo; el OLS muestra que los rasgos no predicen) |
| UR113 es el mejor candidato fuera de Incahuasi para aritmética de subsidiarias | **Propuesto** (74 residuales, un solo quipu) |
| El grupo Huaquerones UR060/UR074 → UR064/072/075/076/079 es un sistema de sumas de dos registros | **Propuesto** (55,6 % vs 37,1 % con offsets aleatorios; n = 36) |
| Que existan más sistemas ocultos que estas reglas no ven | **Especulativo** (no hay evidencia; el 60 % de cuerdas sin vía es compatible con cualquier cosa) |

---

## 8. Limitaciones

- **30,5 % de las cuerdas no tienen valor** (sin nudos o no decodificadas): el mapa solo cubre el 69,5 % numérico. Un quipu «ilegible» puede ser perfectamente legible en su parte no numérica (colores, torsiones, largos), que aquí no se usa.
- **Los valores son una sola lectura** (KFG): no se puede separar aritmética real de error sistemático de transcripción.
- **La procedencia es de museo**, no de origen (regla 6 del brief). El «género» por procedencia mezcla objetos de un mismo depósito con etiquetas distintas.
- **Las reglas entre quipus son de offset global**; las copias con inserciones/deleciones fuertes (UR255/UR267A, UR256/UR267B, UR266/UR275) no se detectan con el umbral actual, aunque `14_copias` las conoce. El resultado «solo duplicados literales» es cierto **para esta implementación**, no para toda copia posible.
- **El nulo baraja dentro del quipu**, lo que destruye también la estructura de valores correlacionados (p. ej. cuotas repetidas). Es conservador para la legibilidad aritmética, pero puede infravalorar reglas que dependen de la distribución de valores.
- **No se corrige la selección de las reglas** (se declaran antes, pero se probaron varias variantes de umbral). La prueba definitiva sería aplicarlas a quipus nuevos.

## 9. Siguiente ronda

1. **UR113**: adaptar las reglas de 19 a su estructura (31 grupos, 505 subsidiarias) y medir cuánto se lee. Es el mejor candidato individual.
2. **Huaquerones**: replicar `suma_dos` con un nulo que baraje los pares (A,B) y no solo el offset; si sobrevive, es un sistema nuevo.
3. **UR267A/UR255/UR267B**: extraer el patrón exacto de `cierre` (¿cuota + 2 partidas?) y contrastarlo con la hipótesis de cuota de 13.
4. **Subsidiarias**: en lugar de Σhijas = padre, probar padre = max(hijas), padre = Σhijas + cuota, o jerarquía de 3 niveles. El 0,73 mediano sugiere una parte, no un todo.
5. **Cuerdas sin valor**: repetir el mapa usando color/torsión/largo como «valor» simbólico, para las 17 656 cuerdas sin nudos.

---

## 10. Para el coordinador

1. **La respuesta corta: el corpus no es legible.** Con reglas estructurales declaradas a priori, solo el **3,90 %** de las 40 162 cuerdas con valor se reconstruye exactamente, frente al **2,56 %** que da el azar (valores barajados dentro de cada quipu). El exceso real es de **1,34 puntos**, no de 3,90.
2. **La legibilidad es de minorías, no gradual.** **448 de 641 quipus (70 %)** no tienen ni una sola cuerda reconstruible; solo **17** sobreviven a BH (q < 0,05) y concentran 2 259 cuerdas (5,6 % del corpus).
3. **Lo que sí se lee es aditivo y escaso:** `cierre` de grupo (108/260 = **41,5 %** frente a 0,5 % del nulo), sobre todo en UR267A, UR255 y UR267B, y `superior` = suma del grupo adyacente (23/72 = **31,9 %** frente a 0,4 %). Son 332 cuerdas en total.
4. **La hipótesis de la subsidiaria-suma es falsa como regla general:** 4,0 % de acierto frente a 1,7 % del azar. En UR270, 241 vías y **cero** aciertos. Una subsidiaria única tampoco copia al padre (9,1 % bruto, 9,8 % nulo).
5. **El 51 % de Incahuasi no generaliza:** con reglas generales y sin alineamientos hechos a mano, los 13 quipus dan **7,6 %** (119/1 558). La diferencia son la cuota (que es la moda) y las correspondencias específicas de 19 (`celda270`, `fila278`). UR270, UR278, UR266 y UR269 son ilegibles aquí.
6. **Las «copias» son duplicados literales, no un sistema.** Solo 8 parejas disparan la regla de offset (4 con aciertos); dos pasan la prueba fuera de muestra y ya estaban documentadas (UR066/UR067, AS125/UR247). `copia_grupo` cae del 62 % al **35 %** cuando el offset se estima sin las posiciones que se evalúan. **No hay una red de registros relacionados.**
7. **No hay «doble entrada»:** solo **2 cuerdas** de 40 162 tienen dos reglas distintas que aciertan. No se puede validar una lectura con otra; la señal de fiabilidad de 19 no existe en el corpus.
8. **Ningún rasgo estructural explica la legibilidad** (OLS, R² = 0,064): ni tamaño, ni cuerdas T, ni subsidiarias, ni procedencia. La única excepción es «tener una copia» (10 quipus, 27 % neto). La legibilidad es idiosincrática del objeto.
9. **Top 20 fuera de Incahuasi: no hay sistemas nuevos.** 13 de 20 son repetición padre-hija (UR1130, UR017, UR204, UR093…); 5 son aritmética parcial de subsidiarias, con **UR113** (Nazca, 74 residuales) como mejor candidato; UR166 tiene 3 totales de grupo. El único candidato a sistema es el grupo **Huaquerones** (UR060/UR074 como registros A/B y UR064/072/075/076/079 como A+B), con 55,6 % fuera de muestra frente a 37,1 % de offsets aleatorios: **propuesto, no demostrado**.
10. **Recomendación:** dejar de buscar un «sistema general» en los 651 y (a) exprimir UR113 y los tres quipus de cierre de Incahuasi, (b) verificar el candidato Huaquerones con un nulo que baraje pares, (c) atacar las 17 656 cuerdas sin valor con atributos no numéricos. El mapa completo está en `quipus_legibles.csv`.
