# 04 · Fuera de muestra: ataque final al sistema de Incahuasi

Carpeta: `analisis/ds/n_fuera_muestra/`. Script: `04_fuera_muestra.py`; salida completa: `salida_04_fuera_muestra.txt`. Semilla 1804. No se modificó nada fuera de esta carpeta.

## Pregunta

¿Sobrevive fuera de muestra la afirmación **1a** del sistema de Incahuasi —`cab(UR273A_i) + cab(UR273B_i)` cae en la unión de cabeceras de UR266/UR275/UR269— y, de paso, la estructura de UR269 (afirmación 4b) que se apoya en ella? Se ejecutan las cinco pruebas (i)–(v) del diseño §4 de `18_equipo_rojo/informe.md`, incluida la repetición de (ii), y se da un veredicto por prueba.

## Método

- **Datos y definiciones congeladas.** Se reutilizan `lib18.py` (registro = grupo de colgantes no separador; cabecera = primer colgante anudado; 0 sin nudos = ausente) y `comun13.py` (BH) sin modificarlos. R1 queda congelada como `A_i + B_i ∈ S`, con `S` = 94 valores únicos de las **cabeceras** de UR266/UR275/UR269. Como sensibilidad se usa también `S_all` = las 260 cuerdas anudadas de esos tres quipus, que es la definición original de 13.
- **Alineación.** Registro a registro por posición ordinal, sin comprimir huecos (los grupos PK sin nudos separan y no cuentan). En UR273A/UR273B la posición ordinal coincide con el número de grupo (ambos tienen la misma lista de grupos). En UR274A **no** coincide: sus separadores están en otra posición, y el alineamiento ordinal es el único que reproduce los tres cuadres 1278, 2020 y 2106; por eso se usa ese.
- **Nulos.** (i) y (iii): barajar B entre los registros de la misma mitad (rompe solo el emparejamiento). (ii): asignar a las 4 posiciones candidatas 4 valores de B distintos, extraídos de las 21 posiciones con B presente. (iv): nulo **condicionado a la magnitud**: para cada acierto se elige al azar una fila del bloque cuya cabecera esté dentro de ±15 % (sensibilidad ±10 % y ±20 %). (v): barajar las cuotas entre las filas de cada bloque.
- **Réplicas.** 10 000 permutaciones Monte Carlo por prueba; donde el espacio es pequeño se enumera exacto (9! = 362 880 para las mitades de 273; 21P4 = 143 640 para (ii)).
- **Corrección múltiple.** Holm sobre los cinco p primarios; se reporta también BH-FDR. Se etiqueta cada conclusión como bien apoyado / apoyado con datos / propuesto / especulativo.

## Resultados

### Resumen

| Prueba | Observado | Esperanza nula | p | Holm | Veredicto para 1a / 4b |
|---|---|---|---|---|---|
| (i) 273 por mitades | 5/9 y 3/9 | 1,000 y 0,444 | 0,00013 y 0,00397 (exactos); IUT **0,0040** | **0,0159** | **Sobrevive** (estable en ambas mitades) |
| (ii) 274A rellena 273A | **3/4** | 0,143 | **0,00013** (exacto) | **0,0007** | **Sobrevive**, pero no es 3/3 |
| (iii) 267 por mitades | 1/13 y 4/13 | 0,308 y 0,538 | 0,288 y 0,0012; IUT 0,288 | 0,503 | **Cae fuera de muestra** (1b) |
| (iv) posición en UR269 | 4/4 (y 6/6 ±1) | — | **0,251** (y 0,247) | 0,503 | **Cae como evidencia independiente** (4b) |
| (v) cuota par/impar | 4/15 | 1,98 | 0,101 | 0,303 | **No confirma**; ver matiz temporal |

Solo (i) y (ii) sobreviven a Holm. La afirmación 1a **sobrevive al ataque fuera de muestra**; 1b y la prueba de posición de 4b no. Las pruebas (iii)–(v) no prueban 1a en sentido estricto: (iii) prueba 1b y (iv)–(v) prueban 4b; el veredicto sobre 1a se basa en (i) y (ii).

### (i) R1 por mitades de registros (273A+B)

- Muestra completa: **8/18** aciertos, esperanza exacta **0,944** con `S` de cabeceras (1,278 con `S_all`, la cifra de 13). Grupos acertados: 3, 9, 11, 12, 13, 17, 18, 19.
- Primera mitad (9 registros válidos): **5/9**, E = 1,000, p exacto = **0,00013** (solo 48 de 362 880 permutaciones alcanzan ≥5).
- Segunda mitad: **3/9**, E = 0,444, p exacto = **0,00397**.
- Heterogeneidad entre mitades: Fisher bilateral p = 0,637. Prueba de conjunción (la regla funciona en *ambas* mitades): p_IUT = max(0,00013; 0,00397) = **0,0040**.
- Sensibilidad con `S_all`: 5/9 p = 0,0029; 3/9 p = 0,0396. El resultado no depende de la definición de la diana.

**Corrección a 18 §4.** El informe del equipo rojo dice que los aciertos están "casi todos en la segunda mitad". Es falso: están **5 en la primera y 3 en la segunda** (también 5/3 si se corta por número de grupo o por posición bruta). La nota pesimista de §4 no se sostiene; leída bien, la prueba (i) apoya a 1a en vez de debilitarla.

Matiz metodológico: R1 no tiene parámetros libres, así que "derivar la regla en una mitad" solo puede significar comprobar que su tasa de acierto se mantiene en la otra. Es una prueba de estabilidad, no de predicción de una regla nueva.

### (ii) UR274A rellena los huecos de UR273A

Seis registros de UR273A no tienen cabecera (ningún colgante anudado ≥100). Cuatro tienen a la vez 273B y 274A presentes:

| Pos. | UR274A | UR273B | Suma | ¿En S? |
|---|---|---|---|---|
| 2 (grupo 2) | 862 | 2222 | **3084** | **No** |
| 5 (grupo 5) | 391 | 887 | 1278 | Sí |
| 6 (grupo 6) | 891 | 1129 | 2020 | Sí |
| 8 (grupo 8) | 772 | 1334 | 2106 | Sí |

- Resultado: **3/4**, no 3/3. Con el criterio estricto (todas las cuerdas de 273A sin nudos) son **2/3**: cuadran 1278 y 2106, falla 3084. El 3/3 de 18 §4 exige mezclar criterios: incluir el grupo 6 (que solo lleva la cuota 30, no una cabecera) y excluir el grupo 2. El valor 3084 no está en `S` ni en `S_all`.
- Esperanza exacta = **0,143**; nulo exacto (21P4 = 143 640): p = **0,00013** (18 permutaciones con ≥3). Poisson: p = 0,0004.
- **Control de familia:** de los 17 quipus del archivo con ≥3 posiciones utilizables en el mismo alineamiento, **ninguno llega a 2/4**; el mejor es UR263 con 1/4. UR255 y UR256 dan 0/4; UR274B, 0/3 (no se alinean). Bonferroni por 17 quipus: 17 × 0,00013 ≈ **0,0022**.
- La predicción es real y fuerte, pero no es ciega: 274A se eligió después de conocer que es la copia/complemento de 273A. Por eso 1a queda como **apoyado con datos**, no como bien apoyado.

### (iii) R1 por mitades (267A+B → cabeceras de UR269)

- Muestra: 5/26, E = 0,692. Grupos acertados: 13, 16, 17, 20, 24.
- Primera mitad (13 registros): **1/13**, E = 0,308, p = **0,288**.
- Segunda mitad: **4/13**, E = 0,538, p = **0,0012**.
- Fisher bilateral p = 0,322 (no hay heterogeneidad detectable), pero la conjunción da p_IUT = **0,288**.

La regla **no se habría podido derivar de la primera mitad** y no se replica en ella. El efecto está concentrado en la segunda mitad (compatible con una ventana temporal, pero esa explicación es post hoc). 1b **cae fuera de muestra**: Holm 0,503.

### (iv) Posición en el bloque de UR269, con nulo condicionado a la magnitud

Los cuatro aciertos exactos de 273A+B en UR269 caen todos en la **fila 1** de su bloque: g5 (bloque 0, 1653), g11 (bloque 1, 1737), g17 (bloque 2, 1827) y g23 (bloque 3, 1780). Contando ±1 se añaden g49 (1505) y g61 (1886): **6/6**.

El nulo uniforme que usó 13 daría 1/(5·5·5·6) = **0,0013** para 4/4 y 0,0001 para 6/6. Pero ese nulo ignora que **las filas se separan por magnitud**: la fila 1 ronda 1000–2000, las filas 2–4 casi todas 2100–2850 y la fila 5 casi todas 392–828 (con excepciones: 2375 en el bloque 7, 34 en el 12).

Con el nulo condicionado (±15 %):

- 4/4 exactos: filas elegibles por acierto = [(1), (1,2,3,4), (1), (1)]. En tres de los cuatro bloques **solo la propia fila 1 está dentro del ±15 %**; en el bloque 1 compiten las filas 2–4 (1600, 1800, 1847). p = **0,251** (MC 0,2514); el producto exacto es 0,25.
- 6/6 con ±1: p = **0,247**. Sensibilidad ±10 % y ±20 %: p = 0,255 y 0,254.
- 267A+B en la **última** fila: 4/5 (g21, g41, g47, g65, g81), elegibles [(5), (4,9), (4,9), (5), (2)], p(≥4/5) = **0,754**; P(5/5) = 0,25. Si el bloque 5 (9 filas) se parte en 4+5, los cinco quedan en la última fila pero p = **1,000** (todas las filas elegibles son únicas).
- Por mitades de bloques: 273 exactos, pares 2/2 con p = 1,000; impares 2/2 con p = 0,250.

**La posición no añade evidencia independiente.** La concentración en la fila 1 es casi forzada por la magnitud de las sumas. El p de 13 (1·10⁻³ / 5·10⁻⁵) cae a ~0,25, tres órdenes de magnitud. La prueba de posición de 4b **cae**.

### (v) Cuota por fila: bloques pares frente a impares

Solo hay 10 bloques canónicos de 5 filas (50 registros); los demás tienen 2, 4, 6 o 9 filas. La cuota se extrae como en 09: primer valor explícito entre 15 y 50, o `cabecera − neto` en ese rango.

- Patrón canónico de 13: **[47, 46, 46, 44, 25]**.
- Ajuste global (in-sample, el patrón se deriva de estos mismos datos): **27/50** frente a 10,12 esperados; p ≤ 1·10⁻⁴. Es una descripción, no una prueba.
- **Pares** (7 bloques, 35 registros): patrón modal exactamente [47, 46, 46, 44, 25]. **Impares** (3 bloques, 15 registros): [47, 40, —, 46, 44].
- Fuera de muestra pares → impares: **4/15** frente a 1,98; p = **0,101**. Impares → pares: **4/35** frente a 4,38; p = **0,674**.

La prueba de paridad **no confirma** el patrón, pero tampoco lo refuta limpiamente: la mitad impar solo tiene 3 bloques canónicos y en ellos las filas 3–5 casi no tienen cuotas detectables (fila 3: cero registros; fila 5: solo 44 y 50). Es un problema de potencia y de datos faltantes, no una prueba en contra. Además, con solo cuotas explícitas (32/50 registros) el patrón es [47, 46, 46, 44, 20]: las filas 1–4 aguantan, pero la fila 5 depende de cómo se extraiga la cuota.

Como sensibilidad **post hoc** (elegida después de ver el resultado de paridad), un corte temporal 5+5 bloques sí replica: patrones [47, 46, 40, 44, 25] y [47, 46, 46, 44, 25]; 0–6 → 7–14: **11/25** frente a 4,12 (p = 0,0005); 7–14 → 0–6: **13/25** frente a 4,93 (p = 0,0004). Por tanto, la estructura de cuotas por fila parece real, pero **la formulación por paridad no debe citarse como evidencia** (y el corte temporal, por ser post hoc, es exploratorio).

## Controles y corrección múltiple

- **Nulo explícito en todas las pruebas**, con la estructura que podría explicar el efecto por sí sola: emparejamiento (i, iii), valores de B (ii), magnitud de la fila (iv), cuotas dentro del bloque (v).
- **Semilla fija** (1804) y ≥10 000 réplicas; enumeración exacta donde era posible.
- **Holm** sobre los cinco p primarios: (ii) 0,0007; (i) 0,0159; (v) 0,303; (iii) 0,503; (iv) 0,503. **BH-FDR**: 0,0007; 0,0099; 0,168; 0,288; 0,288. Solo (i) y (ii) sobreviven.
- **Control de familia de (ii)**: ningún otro quipu del archivo alcanza 2/4; Bonferroni ≈ 0,002.
- **Sensibilidades**: `S` de cabeceras vs todas las cuerdas; ventana ±10/±15/±20 % en (iv); bloque 5 partido o no; cuota explícita vs implícita. Con solo cuotas explícitas (32/50 registros) el patrón modal es [47, 46, 46, 44, 20]: las filas 1–4 aguantan y la fila 5 es frágil (20/25 según el criterio).

## Resultados negativos

1. **(iii)** La primera mitad de la pareja 267 es indistinguible del nulo (1/13, p = 0,288). 1b no es estable fuera de muestra; su p corregido por Holm es 0,503.
2. **(iv)** La regla "fila 1 / fila última" se explica por la magnitud: p ≈ 0,25 en vez de 0,0013. Con el bloque 5 partido, p = 1,0. No es evidencia independiente de 4b.
3. **(v)** La prueba de paridad no confirma el patrón de cuotas (p = 0,101; la otra dirección p = 0,674). El patrón solo se sostiene con un corte temporal post hoc.
4. **(ii)** No es 3/3: el registro del grupo 2 (862 + 2222 = 3084) falla. El 3/3 de §4 corresponde a los tres registros que cuadran; el cuarto, que también cumple el criterio de "273A sin cabecera", no cuadra. Con el criterio estricto de "273A totalmente en blanco" el resultado es 2/3.
5. **(i)** La nota de §4 sobre la segunda mitad es un error factual: 5 aciertos en la primera mitad y 3 en la segunda.

## Nivel de evidencia

- **1a (UR273A+B → 266/275/269): apoyado con datos, y ahora también fuera de muestra.** (i) estable en ambas mitades (IUT p = 0,004; Holm 0,016); (ii) 3/4 con p exacto = 0,00013 y ningún otro quipu ≥2/4 (Holm 0,0007). No llega a "bien apoyado" porque (ii) depende de la elección post hoc de 274A y de la definición de "sin cabecera", y porque todo sigue siendo KFG, no una relectura independiente.
- **1b (UR267A+B → UR269): propuesto, debilitado.** Falla la mitad de los datos; Holm 0,503. No debe presentarse como resultado fuera de muestra.
- **4b, posición en el bloque: cae como evidencia independiente.** El efecto es un artefacto de magnitud (p ≈ 0,25).
- **4b, cuota por fila: apoyado con datos solo in-sample y en el corte temporal exploratorio; la prueba de paridad es no concluyente.** No citar la paridad como confirmación.
- El núcleo 2 (UR270 → UR278) y 3 (UR278 → UR266) no se tocan aquí; siguen como estaban.

## Para el coordinador

- **1a sobrevive al fuera de muestra.** Por mitades: 5/9 (p exacto 0,00013) y 3/9 (p 0,0040); conjunción p = 0,0040, Holm 0,016. La nota de 18 §4 ("casi todos en la segunda mitad") es falsa: son 5 en la primera y 3 en la segunda.
- **La predicción de 274A es real pero es 3/4, no 3/3** (y 2/3 con el criterio estricto de "273A totalmente en blanco"). 1278, 2020 y 2106 cuadran; 862 + 2222 = 3084 no. p exacto = 0,00013; ningún otro quipu del archivo llega a 2/4; Bonferroni ≈ 0,002. Sigue siendo la evidencia fuera de muestra más fuerte, pero no es ciega: 274A se eligió por ser la copia de 273A.
- **1b cae fuera de muestra.** 267A+B da 1/13 en la primera mitad (p = 0,288) y 4/13 en la segunda (p = 0,0012); Holm 0,503. El efecto está concentrado en la segunda mitad del libro.
- **La prueba de posición en UR269 (4b) cae como evidencia independiente.** El 4/4 en la fila 1 es casi forzado por la magnitud: condicionando a ±15 %, p = 0,25 (no 0,0013); con 267, p = 0,75; partiendo el bloque 5, p = 1,0.
- **La cuota por fila no se confirma por paridad** (4/15 frente a 1,98; p = 0,101), pero la mitad impar tiene solo 3 bloques y las filas 3–5 casi no tienen cuotas. Un corte temporal 5+5 sí replica (11/25 y 13/25; p ≈ 5·10⁻⁴), aunque es post hoc: no cuenta como confirmatorio.
- **Corrección múltiple:** solo (i) y (ii) pasan Holm; (iii), (iv) y (v) no. El mensaje central para el público debe ser "1a resiste; 1b y la posición en el bloque, no".
- **Lo que falta para cerrar 1a:** relectura o fotos independientes de UR273A/B y UR274A (sobre todo el grupo 2), y las subsidiarias de UR274B/UR256 que faltan en KFG. Sin eso, 1a es "apoyado con datos", no "bien apoyado".
- **Siguiente ronda:** pre-registrar la regla "273A sin cabecera → 274A" y aplicarla a los quipus de Inkawasi no publicados; buscar los tres flujos que faltan (cuotas 46, 46, 44) en esos quipus; y repetir (iii) en una mitad ciega antes de volver a citar 1b.
