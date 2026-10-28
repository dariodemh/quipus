# ¿Qué son las 9 columnas de UR278 (y los grupos de 9 de UR270)?

**Equipo:** DeepSeek · carpeta `analisis/ds/n_nueve_unidades/`
**Fecha:** 18 de octubre de 2026
**Semilla:** 20261018 (todo reproducible)
**Datos:** `analisis/13_sistema_incahuasi/ur278_tabla.csv`, `ur270_ur278.csv`, `analisis/datos/cuerdas.csv`, `analisis/ds/n_rejilla/firma_9_partes.csv`, `analisis/ds/n_saya_proporcional/informe.md`, `analisis/fuentes_txt/Rostworowski_CostaPeruana.txt`.
**Scripts:** `01_datos.py`, `02_pruebas.py`, `03_diagnosticos.py`, `04_potencia.py`.
**Salidas:** `pruebas.csv` (15 pruebas), `pares_36.csv`, `bootstrap_pares.csv`, `fases.csv`, `ur270_ratio.csv`, `potencia.csv`, `salida_0*.txt`.

---

## 1. Pregunta

Las 9 columnas de UR278 son las 9 cuerdas colgantes de cada grupo (una por registro), y cada celda es la suma de dos partes, B (colgante) y A (primera subsidiaria), que en UR270 se conservan separadas. Las filas son registros sucesivos de un mismo flujo (cuota 47). La pregunta es **qué representan las 9 posiciones**. Tres hipótesis rivales:

- **(A) Tiempo.** 9 meses de 40 días de un año costeño de 9 meses, con semana de 10 días (Rostworowski, cap. Changuco: «un año especial de nueve meses… una semana de 10 días… un mes de cuarenta días y un año de nueve meses», líneas 914–916 del txt). Predice orden cronológico con sentido, tendencias suaves, estacionalidad (cosecha de maní), autocorrelación entre columnas vecinas e igualdades exactas entre vecinas (un saldo que no cambió).
- **(B) Pachacas de una guaranga.** Collique tenía 10 pachacas cuyos nombres «pueden hermanarse de dos en dos» (Rostworowski, líneas 229–241). Predice estructura en pares, orden sin sentido temporal, proporciones estables ligadas a población; 9 = 10 menos una.
- **(C) Mitades de guarangas de Lunahuaná.** El señorío comprendía 4 guarangas gobernadas por 8 curacas, dos por guaranga (¿urin/anan?), más el principal; 740 tributarios en 1577 (Rostworowski, líneas 706–762). Predice 8 columnas en 4 pares + 1 distinta (el principal), o 4+4+1.

Inkahuasi está en Lunahuaná, así que (C) es la hipótesis geográficamente pertinente; (B) es una analogía estructural desde otro valle (Chillón). Ambas predicen lo mismo a grandes rasgos —un emparejamiento— y se distinguen sobre todo por la forma (4 pares + 1 frente a 4+4+1) y por el papel de la columna «principal».

---

## 2. Datos y unidad de análisis

- **UR278:** 28 grupos con ≥7 colgantes anudados; **24 grupos tienen exactamente 9 colgantes de nivel 0, todos anudados** (54 601 unidades). Son la matriz principal 24×9. Se excluyen los grupos 10 (7 anudados), 18 (10 cuerdas), 26 (8 anudados) y 32 (12 cuerdas), porque una columna no está definida. Como control de robustez se repite todo con 26 filas (las que tienen c1–c9 llenas, incluidos 18 y 32): los resultados no cambian.
- **UR270:** 6 grupos de 9 colgantes con sus 9 primeras subsidiarias completas; cada celda es P+S1. **No es una muestra independiente**: sus grupos corresponden a filas de UR278 (21, 25, 26, 27, 28 y 30; tres con 8–9 aciertos de 9 columnas, el resto con 6–7), y UR278 es el resumen de UR270. Se usa como **control de la alineación de columnas**, no como prueba independiente.
- **Otros grupos de 9 en Incahuasi:** solo hay **3** (JC009 ×2 y UR265 ×1), y son de otra escala (valores 1–60 frente a 100–500). No permiten replicación externa. En todo el KFG hay 238 grupos de 9 completos, pero su estructura es distinta: en el 42 % la posición 0 es el máximo y el CV dentro de grupo tiene mediana 0,79, frente a 0,275 en UR278. Los grupos de 9 de UR278 no son el «total + 8 partes» habitual: son 9 unidades comparables.
- Unidad de análisis: el registro (fila) y el quipu. No se hacen pruebas a nivel de cuerda suelta.

---

## 3. Método: dos nulos, porque hay dos preguntas distintas

El error fácil aquí es usar un solo nulo. Los estadísticos de orden y los de asociación no se calibran igual.

**Nulo L (etiquetas de columna).** Se permuta la asignación de las 9 etiquetas a las 9 posiciones, con la **misma permutación en todas las filas**. Conserva el perfil de medias por columna, el efecto de fila y la distribución conjunta; solo rompe el orden físico. Es el nulo correcto para (A): ¿el orden observado es especial frente a otros órdenes? Se enumera **9! = 362 880 exacto**.

**Nulo C (columnas independientes).** Se permuta cada columna entre filas por separado, se recentra por fila (para conservar la restricción composicional) y se recalcula el estadístico. Destruye la covariación entre columnas y conserva la marginal de cada una. Es el nulo correcto para (B/C): ¿hay asociación entre columnas más allá de sus marginales? 20 000 réplicas. Los estadísticos de «mejor de 945 emparejamientos» son **invariantes** a permutar etiquetas (darían p = 1 por construcción), y por eso se calibran con el nulo C; además se verificó con un **nulo paramétrico** (columnas independientes + efecto de fila común, con las SD observadas), que da el mismo resultado.

**Estadísticos predefinidos** (15; detalle en `pruebas.csv`):

| código | hipótesis | estadístico | cola |
|---|---|---|---|
| L1 | A | Σ\|p_j − p_{j+1}\| del perfil (rugosidad) | baja |
| L2 | A | correlación media entre columnas adyacentes | alta |
| L3 | A | \|Spearman(perfil, posición)\| | alta |
| L4 | A | nº de extremos locales del perfil | baja |
| L5 | A | R² de perfil ~ cos+sin(2πj/9) | alta |
| L9 | A | nº de celdas con \|x_ij − x_i,j+1\| ≤ 1 | alta |
| L6 | B/C | r media del emparejamiento a priori (1-2)(3-4)(5-6)(7-8) | alta |
| L7 | B/C | suma \|p_i − p_j\| de ese emparejamiento | baja |
| C0 | B/C | Friedman sobre rangos dentro de fila (¿hay efecto de columna?) | alta |
| C1 | B/C | máximo sobre los **945** emparejamientos de 8+1 de la r media intra-par | alta |
| C1b | B/C | ídem con \|r\| (relación de cualquier signo) | alta |
| C2 | C | máximo sobre las **126** biparticiones 4+4(+1) de (r intra − r entre) | alta |
| L8 | C | \|media(p1..p4) − media(p5..p8)\| | alta |
| C3 | B/C | máximo sobre 945 de igualdades intra-par (nulo: permutar **dentro de cada fila**, que conserva la planitud de la fila) | alta |
| C5 | C | mayor hueco del perfil ordenado / rango (¿una columna aparte?) | alta |

Corrección múltiple: **BH-FDR y Holm sobre las 15 pruebas**. Los estadísticos están correlacionados, así que BH es aproximado; se reportan ambos y se llama «significativo» solo lo que sobrevive a BH. Potencia calculada por simulación (`04_potencia.py`).

**Nota sobre el sondeo previo del coordinador.** Se verificó y se corrige en parte:
- La suma de \|dif log\| entre adyacentes: mis valores en log-razón (quitando solo el efecto de fila) son **1,447 observado frente a 2,035 de media nula, p = 0,046** (su 62,1 vs 74,7, p = 0,022, es la misma señal sobre valores brutos). Coincide en dirección y orden de magnitud.
- Su control de «quitar efectos de fila y columna» (p = 0,16) **no es válido para esta pregunta**: el efecto de columna *es* la señal de adyacencia (columnas vecinas con medias parecidas). Al eliminarlo se elimina lo que se quiere medir. El control correcto es el nulo de etiquetas, que ya conserva el perfil y solo rompe el orden.
- Las igualdades exactas: **15 adyacentes frente a 21 no adyacentes**, los mismos conteos que él obtuvo; con las 24 filas de 9 cuerdas las oportunidades son 192/672 en vez de 208/728. Con nulo de etiquetas, **p = 0,0095**. Su recuento es correcto; lo que falta es el contraste y la explicación.

---

## 4. Resultados

### 4.1 El hecho básico: hay un perfil de columnas fuerte y estable

Las 9 posiciones **no son equivalentes**. Participación media de cada columna en el total del registro:

| | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
|---|---|---|---|---|---|---|---|---|---|
| cuota | 0,137 | 0,144 | 0,096 | 0,108 | 0,114 | 0,126 | 0,106 | **0,080** | 0,090 |
| log-razón (clr) | 0,24 | 0,28 | −0,13 | 0,01 | 0,05 | 0,16 | −0,05 | **−0,38** | −0,19 |

- **Efecto de columna: Friedman = 94,6 frente a 8,0 del nulo (permutar dentro de fila), p = 0,0002, q = 0,003. Bien apoyado.**
- La razón máximo/mínimo es **1,80** y el CV entre columnas 0,193, muy por encima del ruido de conteo (~0,06): las columnas difieren de forma sistemática, no por muestreo.
- En **UR270** (6 grupos, todos correspondientes a filas de UR278) el perfil es casi idéntico: r = **0,937** (nulo de etiquetas p = 0,00055). No es replicación independiente —las celdas de UR278 son P+S1 de UR270 y la alineación se estableció por contenido—, pero sí muestra que **el orden físico de las 9 unidades es el mismo en los dos quipus**: si UR270 las hubiera ordenado de otro modo, P+S1 no coincidiría columna a columna (9/9, 9/9 y 8/9 aciertos en los tres grupos mejor alineados de `13_sistema_incahuasi`).
- El **orden no es arbitrario pero tampoco cronológico**: el perfil **decrece** con la posición (Spearman = **−0,73**, p = 0,025, q = 0,076; índice de monotonía 0,75 frente a 0,50, p = 0,038). Las dos primeras columnas son las mayores (28,1 % del total frente a 22,2 % si fueran iguales) y las dos últimas las menores. Hay repuntes locales (c3 baja, c6 sube), así que no es una simple escalera.

**Lectura:** las 9 posiciones son una **lista fija y ordenada de 9 subunidades de tamaño desigual**, con las mayores al principio y las menores al final. Eso es compatible con A, B y C en abstracto, pero descarta dos lecturas simples: «9 unidades iguales» (B en su forma decimal estricta) y «orden arbitrario».

### 4.2 Hipótesis A (tiempo): las predicciones específicas fallan

| prueba | observado | nulo | p | q (BH) |
|---|---|---|---|---|
| L5 estacionalidad (R² cos+sin) | 0,192 | 0,250 | 0,517 | 0,55 |
| L4 extremos del perfil (curva suave) | 4 | 4,67 | 0,435 | 0,50 |
| L2 correlación entre vecinas | 0,028 | −0,098 | 0,090 | 0,135 |
| L1 rugosidad del perfil | 1,447 | 2,035 | 0,046 | 0,098 |
| L3 tendencia monótona | 0,733 | 0,289 | 0,025 | 0,076 |
| L9 igualdades entre vecinas (±1) | 29 | 15,8 | 0,0044 | **0,022** |

- **No hay estacionalidad**: el R² del ajuste coseno de periodo 9 es 0,19, *por debajo* de la media nula (0,25). La potencia para detectar una curva estacional suave es **1,00 para amplitud 0,2** (rango 0,4 en log ≈ 1,5× entre pico y valle). El perfil observado tiene un rango de 0,66 en log (1,9×): si fuera una curva estacional de esa amplitud, se habría detectado con probabilidad ~1. **Resultado negativo fuerte.**
- **No hay suavidad**: 4 extremos locales frente a 4,67 esperados al azar. Una curva con una cosecha tendría 2. La tendencia que sí hay es **monótona decreciente**, no estacional, y es lo que predice un orden por tamaño, no un calendario.
- **No hay autocorrelación entre vecinas** (r = 0,03, p = 0,09): si los meses contiguos compartieran choques, las vecinas covarían. No lo hacen.
- **Sí hay un exceso de igualdades entre vecinas**: 15 exactas (7,8 %) frente a 8,0 esperadas (p = 0,0095), y 29 con ±1 frente a 15,8 (p = 0,0044). Es la única predicción de A que se cumple. Pero (i) está concentrada en **6 filas planas de 24** (las filas con CV interno 0,06–0,16; 12 filas no tienen ninguna igualdad), (ii) **28 de las 29 igualdades están en la fase 1** (antes del grupo 15) y en la fase 2 hay **1**, y (iii) una regresión de igualdades por par sobre \|Δperfil\| + adyacente atribuye solo 0,5 de las 2,1 igualdades por par de exceso al tamaño parecido de las vecinas; la adyacencia aporta +1,6 (SE 0,58). El exceso no es un simple efecto de magnitud, pero sigue siendo frágil por su concentración. **Nivel: apoyado con datos pero frágil; no bien apoyado.**
- Además, A exige que cada fila sea un **año** (9 meses) para que el perfil se repita en todos los registros. La estructura documentada en `13_sistema_incahuasi` es la de **registros sucesivos de un flujo** (cuota 47, bloques de 5 en el libro maestro UR269), no de años. Si las filas son registros/periodos de duración variable, un perfil estacional fijo en las 9 columnas no tiene sentido mecánico.

**Veredicto A: no apoyada; sus predicciones distintivas (estacionalidad, suavidad, autocorrelación) fallan, y la única que se cumple (igualdades vecinas) es frágil y tiene explicación alternativa. No se puede decir que sea falsa —un calendario podría subyacer sin dejar estas huellas—, pero los datos no lo sostienen.**

### 4.3 Hipótesis B y C (pares y mitades): hay algo de emparejamiento, pero no la estructura predicha

| prueba | observado | nulo | p | q (BH) |
|---|---|---|---|---|
| C1 mejor de 945 emparejamientos (r con signo) | **0,377** | 0,198 | **0,0020** | **0,015** |
| C1b mejor de 945 con \|r\| | 0,508 | 0,417 | 0,032 | 0,081 |
| C2 mejor bipartición 4+4(+1) | 0,263 | 0,220 | 0,187 | 0,255 |
| L8 perfil 4+4 (columnas 1-4 vs 5-8) | 0,154 | 0,123 | 0,327 | 0,409 |
| L6 emparejamiento a priori (1-2)(3-4)(5-6)(7-8) | 0,102 | −0,098 | 0,079 | 0,132 |
| L7 perfil de ese emparejamiento | 0,602 | 1,018 | 0,067 | 0,125 |
| C5 hueco máximo (¿una columna aparte?) | 0,287 | 0,340 | 0,684 | 0,684 |

- **El mejor emparejamiento posible es mejor de lo que produce el azar** (0,377 vs 0,198, p = 0,002; el nulo paramétrico da p = 0,002). El ganador es **(1-2), (3-6), (4-9), (5-7)**, con c8 suelta, y **coincide exactamente en UR270** (0,442); como UR270 son las mismas filas, esto no es replicación, pero confirma que la alineación de columnas no está forzada. En el bootstrap de filas (3 000 réplicas) (1,2) aparece en el 91 % de los mejores emparejamientos; el conjunto completo se repite 765/3 000 veces y la fase 2 reproduce el mismo conjunto.
- **Pero el emparejamiento no es el predicho por B ni por C.** El a priori (1-2)(3-4)(5-6)(7-8) no es especial (p = 0,079). El 4+4+1 no existe (C2 p = 0,187; L8 p = 0,327). No hay una bipartición de mitades.
- **Las relaciones por par, a dos colas y con BH sobre los 36 pares**, son solo tres: **(1,2) r = +0,675 (q = 0,018)**, **(3,5) r = −0,658 (q = 0,025)** y **(5,7) r = +0,447 (q = 0,048)**. Las dos primeras son fuertes; la tercera moderada. No forman un emparejamiento: (5,7) y (3,5) comparten c5, y c4, c6, c8, c9 quedan sueltas.
- El «mejor de 945 con \|r\|» elige (1-2)(3-5)(4-7)(8-9) (p = 0,032): es decir, lo que hay es **un eje de compensación** (c3/c5, c2/c7, c8/c9 negativas) **más un par positivo** (c1/c2), no cuatro pares discretos.
- **Igualdades intra-par**: el mejor emparejamiento acumula 19 igualdades frente a 14,8 del nulo que conserva la planitud de cada fila (p = 0,009, q = 0,034). Es señal de que las igualdades se concentran en pares fijos, pero los pares con más igualdades son (1,2)=8, **(2,6)=6**, (6,7)=5, (7,8)=4: de nuevo, no un emparejamiento limpio.

**Lectura B/C:** hay **una** relación de par robusta, (c1,c2); hay además **dos relaciones de compensación** fuertes, (c3,c5) y (c2,c7), que no encajan en el mismo reparto. El patrón global es un **gradiente composicional de 2 dimensiones** (PC1 43 %, PC2 26 %: 69 % de la varianza), no un sistema de 4 pares. B y C predicen 4 pares + 1; los datos dan 1 par positivo, 2 ejes de compensación y 4 columnas sueltas (c4, c6, c8, c9).

**B y C no son distinguibles entre sí** con estos datos: ambas predicen lo mismo (un emparejamiento de 8 + 1) y ninguna de sus variantes —4 pares contiguos, 4+4+1, un principal distinto— aparece. El único dato que favorece levemente a C es externo: 4 guarangas × 2 curacas + principal = 9, y Lunahuaná es el valle de Inkahuasi. Es una coincidencia numérica y geográfica sugerente, no una estructura detectada en el quipu.

### 4.4 ¿Hay una columna «distinta» (el principal de C)?

No. El mayor hueco del perfil ordenado dividido por el rango es 0,287, **menor** que el 0,340 esperado por azar (p = 0,68): el perfil es un gradiente continuo, sin una columna despegada. El mayor salto está entre c2 y c3 (0,41 en log), lo que sugiere un bloque **2 + 7**, no 8 + 1.

Sí apareció un candidato: **c8** es la columna más pequeña, la más variable y la que queda suelta en el mejor emparejamiento. En UR270, su cociente A/(A+B) es **0,486** frente a ~0,28 de las demás (máximo sobre columnas, nulo permutando columnas dentro de grupo: p = 0,00025). Pero **la explicación aburrida gana**: el cociente A/(A+B) disminuye con el tamaño de la unidad (Spearman = −0,41, p = 0,002), y tras controlar log(total) el residuo de c8 (+0,107) es casi el de c2 (+0,093). c8 no es cualitativamente distinta: es la unidad más pequeña, y la parte A tiene un piso. **Hallazgo disuelto; se reporta como negativo.**

### 4.5 Residuos: PCA de log-razones

- PC1 (43 %) es un contraste de **c8 (−0,89)** contra todo lo demás: cuando c8 sube, el resto baja. Es la columna «de ajuste».
- PC2 (26 %) es **c7 (−0,73) contra c3 (+0,44) y c5 (−0,39)**: el eje de compensación c3/c5/c7.
- PC3–PC9 explican 12 %, 9 %, 5 %, 3 %, 2 %, 1 %, 0 %.
- Los dos primeros componentes bastan para describir la estructura. No hay un bloque discreto de 4 pares: un modelo de pares predeciría una matriz de correlación en bloque, y lo que se ve es un gradiente de rango 2.
- Las columnas c7 y c8 son las que se mueven (CV de cuota 0,30 y 0,32; razones de sobredispersión 5,0 y 4,6), y son también las de mayor elasticidad al tamaño (1,52 y 1,67, según `n_saya_proporcional`). Es un gradiente de variabilidad, no una clase aparte.

### 4.6 Fases (antes y después del grupo 15)

| conjunto | n | Spearman perfil-posición | igualdades adyacentes | mejor par | p |
|---|---|---|---|---|---|
| fase 1 (grupos <15) | 14 | −0,58 | **28** | (1-2)(3-8)(4-5)(6-7) | 0,0003 |
| fase 2 (grupos >15) | 10 | −0,82 | **1** | (1-2)(3-6)(4-9)(5-7) | 0,35 |
| todas | 24 | −0,73 | 29 | (1-2)(3-6)(4-9)(5-7) | 0,0013 |
| robustez 26 filas | 26 | −0,73 | 29 | (1-2)(3-6)(4-9)(5-7) | — |

- El perfil se mantiene en ambas fases, pero **no es idéntico**: r(perfil fase 1, fase 2) = 0,533, frente a 0,892 ± 0,059 de particiones aleatorias de las 24 filas. La diferencia es real y coherente con el efecto de tamaño ya documentado (los registros de la fase 2 son 33 % más pequeños y las elasticidades difieren por columna). No es una inestabilidad del orden, sino de las cuotas.
- **La señal de igualdades es de la fase 1**: 28 de 29. En la fase 2 hay una sola. Eso la debilita como propiedad estructural y la acerca a una peculiaridad de un tramo de registros.
- El emparejamiento (1,2) es lo único que aparece en las dos fases y en UR270.

### 4.7 Potencia: ¿no vemos estructura porque no hay, o porque no alcanza?

- **4 pares** con r intra-par 0,5: potencia 0,14; con 0,6: 0,50; con 0,7: 0,87. Es decir, **no podemos descartar un emparejamiento débil (r ≤ 0,5)**, pero sí habríamos detectado uno fuerte (r ≥ 0,7) en el 87 % de los casos. La ausencia del patrón 4+4+1 es informativa solo para estructuras fuertes.
- **Estacionalidad**: potencia 1,00 para amplitud 0,2 (rango 1,5×); 0,82 para el test de extremos. La ausencia de estacionalidad **sí es informativa**.
- El n de 24 filas es la limitación principal para los emparejamientos; no lo es para el perfil (que se estima con 24×9 valores y es muy estable).

---

## 5. Controles y explicaciones aburridas

1. **Largo de cuerda.** El largo no explica los valores: r(largo, valor) = −0,106; r(largo medio por columna, perfil) = −0,099. El perfil no es un artefacto de cuerdas más cortas o más largas.
2. **Color.** El color es de la fila (AB o W), no de la columna; solo el grupo 1 tiene un corte 4 AB + 5 NB, y no se repite. No hay mapeo color↔mitad. (El informe `n_rejilla` ya había mostrado que el color de UR278 va con la fila y en UR270 con el nivel.)
3. **Filas planas.** Las igualdades se concentran en 6 filas con CV interno bajo. Por eso el test C3 usa un nulo que permuta **dentro de cada fila** y conserva la planitud; aun así queda p = 0,009. Y por eso L9 se interpreta con la regresión sobre \|Δperfil\|.
4. **Efecto de tamaño.** Ya documentado en `n_saya_proporcional`: cuotas no fijas, elasticidades 0,58–1,67, M1 rechazado. Aquí se confirma que (1,2) sobrevive al control de log N (r parcial 0,553), pero (5,7) también (0,462), y las negativas (3,5) y (2,7) no son un artefacto de tamaño.
5. **Un estadístico que engaña.** El «CV de las sumas de par» da p = 0,0002 con el nulo de columnas independientes, pero ese nulo **destruye el efecto de fila común**; con el nulo paramétrico correcto (efecto de fila + SD observadas) el p sube a **0,0037** y la señal se reduce a las correlaciones negativas ya conocidas. Se descartó de la tabla principal para no contar dos veces lo mismo.
6. **Selección de la mejor de 945.** Todos los p de C1/C2/C3 incorporan la selección porque el nulo recalcula el máximo sobre las 945 (o 126) opciones. No hay p «nominal» de un par elegido a posteriori.
7. **Comparaciones múltiples.** 15 pruebas, BH y Holm. Los dos p más pequeños (Friedman y C1) sobreviven a Holm; L9 queda en el límite (Holm 0,057) y C3 no sobrevive a Holm.

---

## 6. Resultados negativos (explícitos)

- No hay estacionalidad de 9 partes (R² = 0,19 < nulo 0,25; potencia 1,0 para una curva de amplitud 0,2).
- No hay perfil suave (4 extremos vs 4,67 esperados).
- No hay autocorrelación entre columnas vecinas (r = 0,03, p = 0,09).
- No hay 4+4+1 (C2 p = 0,19; L8 p = 0,33).
- No hay 4 pares contiguos (L6 p = 0,079; el emparejamiento a priori no es especial).
- No hay una columna claramente distinta (hueco p = 0,68).
- No hay color por columna ni efecto del largo.
- c8 no es cualitativamente distinta: su cociente A/B se explica por su tamaño.
- No hay otros grupos de 9 comparables en Incahuasi (solo 3, de otra escala), así que no hay replicación externa posible hoy.
- El «cambio de régimen» en el grupo 15 no es un cambio de orden de columnas: el perfil se mantiene, cambian las cuotas, y eso ya estaba explicado por el tamaño.

---

## 7. Veredicto y nivel de evidencia

| afirmación | nivel |
|---|---|
| Hay un efecto de columna fuerte: las 9 posiciones no son equivalentes (Friedman p = 0,0002) | **bien apoyado** |
| El perfil de columnas es estable entre fases y el orden físico es el mismo en UR270 y UR278 | **bien apoyado** el efecto de columna; **apoyado** que el sentido del gradiente es el mismo en ambas fases (Spearman −0,58 y −0,82; r entre perfiles 0,53, menor que particiones aleatorias por el efecto de tamaño) |
| El perfil está ordenado por magnitud decreciente (Spearman −0,73; monotonía 0,75) | **apoyado con datos** (q = 0,076 tras BH; no sobrevive a la corrección) |
| Existe un emparejamiento mejor que el azar (mejor de 945, p = 0,002) | **apoyado con datos** (robusto a nulo paramétrico y a bootstrap) |
| Ese emparejamiento es el de B o el de C (4 pares + 1, o 4+4+1) | **no apoyado / rechazado en su forma específica** |
| (c1,c2) es un par real (r = 0,675, q = 0,018; sobrevive a log N) | **apoyado con datos** |
| Las igualdades exactas se concentran entre columnas vecinas (15 vs 8, p = 0,0095) | **apoyado con datos, frágil** (fase 1 solamente; ~25 % explicado por \|Δperfil\|) |
| A (9 meses) es la organización de las columnas | **no apoyado**; predicciones distintivas fallan, y exige filas = años, contra la estructura de registros |
| B y C son distinguibles con estos datos | **no**: indistinguibles entre sí; ninguna de sus formas específicas aparece |
| Las 9 columnas son una lista fija y ordenada de 9 subunidades de tamaño desigual | **propuesto** (lo que mejor describe los datos, sin identificar qué son) |
| Qué son esas subunidades (depósitos, cuadrillas, cargas, pachacas, mitades) | **especulativo** |

**Veredicto: «otra».** Ni tiempo (A) ni pachacas emparejadas (B) ni mitades de guaranga (C) en sus formas específicas. Lo que los datos sostienen es una **lista fija y ordenada de 9 subunidades de tamaño desigual**, con un bloque inicial de dos unidades grandes y correlacionadas (c1, c2) y un gradiente de 7 unidades menores, atravesado por dos ejes de compensación (c3/c5 y c2/c7). B y C no se pueden separar entre sí; A se puede rechazar en lo estadístico, aunque no demostrar falsa.

---

## 8. Qué dato futuro las separaría

1. **Otro quipu de Incahuasi con 9 unidades y contenido conocido.** Es el dato decisivo y hoy no existe: solo hay 3 grupos de 9, de otra escala. Si apareciera un quipu con 9 columnas y una lista colonial de 9 nombres (pachacas o curacas) en el mismo orden, B o C quedaría identificada.
2. **El detalle del primer tramo (UR273A/B, UR274A/B)**, hoy perdido o incompleto. Si sus 9 subunidades tienen nombres o un orden distinto, se vería si el orden es semántico o aritmético.
3. **Un quipu con 10 unidades.** B predice 10 pachacas (9 = 10 − 1); C predice 4×2 + 1 = 9. Un grupo de 10 con la misma estructura favorecería a B; uno de 9 sistemático, a C. En UR278 solo 1 de los 37 grupos tiene 10 cuerdas, y es atípico.
4. **Un quipu del mismo flujo en dos órdenes físicos distintos.** Si el orden de las 9 se mantiene (como entre UR278 y UR270), es una lista canónica; si cambia, el orden no es semántico. UR270 ya da un punto a favor de la lista canónica.
5. **Dos años consecutivos del mismo flujo.** Si las columnas son meses, el perfil debería repetirse con un desfase estacional; si son unidades, no.
6. **Fotos y datos de atributos** (color, torsión, unión, largo) de las 9 cuerdas de cada grupo: un marcador material de mitad (por ejemplo, 4+5 en color) sería evidencia directa de C. En UR278 el color no lo es.
7. **Un producto distinto** (maíz, ají, ropa) en el mismo flujo: si las 9 columnas son unidades sociales, el perfil de tamaños debería repetirse; si son meses, también, pero con otra estacionalidad. La repetición del perfil entre productos no separa A de B/C; la separa la forma (suave vs escalonada).

---

## 9. Para el coordinador

- **Las 9 columnas no son equivalentes.** Efecto de columna fuerte (Friedman 94,6 vs 8,0; p = 0,0002) y perfil estable: c1–c2 ~28 % del total, c8–c9 ~17 %. Cualquier hipótesis que las trate como 9 unidades iguales está descartada.
- **El perfil está ordenado por tamaño, no por el calendario**: Spearman con la posición = −0,73 (p = 0,025; q = 0,076). Las mayores primero, las menores al final, con repuntes locales. Esto es lo que predice una lista jerárquica, no un año de 9 meses.
- **A (tiempo) no se sostiene.** No hay estacionalidad (R² 0,19 < nulo 0,25; potencia 1,0 para una curva de 1,5×), ni perfil suave (4 extremos vs 4,67), ni autocorrelación entre vecinas (r = 0,03). La única predicción que se cumple —igualdades entre vecinas, 15 exactas vs 8 esperadas, p = 0,0095— está concentrada en 6 filas planas y en la fase 1 (28 de 29); el tamaño parecido de las vecinas explica solo ~25 % del exceso, pero la concentración la hace frágil.
- **Verifiqué su sondeo**: sus 15/208 y 21/728 son correctos (yo obtengo 15/192 y 21/672 con las 24 filas de 9 cuerdas; p = 0,0095 con nulo de etiquetas). Su p = 0,16 «tras quitar fila y columna» no es un control válido: el efecto de columna es justamente la señal de adyacencia.
- **B y C: hay emparejamiento, pero no el que predicen.** El mejor de los 945 emparejamientos es mejor que el azar (0,377 vs 0,198; p = 0,002; el mismo conjunto en UR270), pero el ganador es (1-2)(3-6)(4-9)(5-7) con c8 suelta, no 4 pares contiguos (p = 0,079) ni 4+4+1 (p = 0,19). B y C no son distinguibles entre sí con estos datos.
- **Solo tres pares sobreviven a BH (36 pares, dos colas)**: (1,2) +0,675 (q = 0,018), (3,5) −0,658 (q = 0,025) y (5,7) +0,447 (q = 0,048). No forman un reparto: (5,7) y (3,5) comparten c5. El patrón es un gradiente de 2 componentes (PC1+PC2 = 69 %), no cuatro pares.
- **El «principal distinto» de C no aparece**: el mayor hueco del perfil es menor que el azar (p = 0,68). El candidato c8 (cociente A/B = 0,49 vs 0,28) se disuelve: el cociente baja con el tamaño de la unidad (rho = −0,41) y, controlando log N, c8 y c2 son iguales. Es un efecto de piso, no una unidad distinta.
- **Potencia**: con 24 filas detectamos 4 pares con r ≥ 0,7 (87 %) pero no con r ≤ 0,5 (14 %). La ausencia de 4+4+1 descarta estructuras fuertes, no débiles. La ausencia de estacionalidad, en cambio, es concluyente.
- **Fases**: el sentido del gradiente se mantiene (Spearman −0,58 y −0,82), pero las cuotas cambian más de lo que permite el azar (r entre fases 0,53 vs 0,89 de particiones aleatorias), coherente con el efecto de tamaño ya conocido. Las igualdades desaparecen en la fase 2 (1 de 29): no las trataría como propiedad estructural.
- **Veredicto**: «otra» — lista fija y ordenada de 9 subunidades de tamaño desigual, con un bloque inicial de dos. No es tiempo, no es 4 pares + 1, no es 4+4+1. Nivel: efecto de columna y estabilidad, **bien apoyados**; orden por tamaño y par (1,2), **apoyados**; qué son las unidades, **especulativo**.
- **Qué pediría**: un segundo quipu de Incahuasi con 9 unidades y contenido conocido (hoy no hay ninguno comparable), el detalle perdido del primer tramo (UR273A/B–UR274A/B), y un grupo de 10 unidades. Sin eso, B y C seguirán siendo indistinguibles.
