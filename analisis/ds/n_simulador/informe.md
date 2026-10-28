# n_simulador · Un quipucamayoc generativo para el archivo de Incahuasi

**Pregunta:** ¿qué modelo generativo produce el archivo de Incahuasi y, en particular, qué tasa de error explica que solo 8 de 18 sumas A+B sean exactas? ¿Es compatible con un sistema en el que **todas** las sumas fueran exactas en origen?

**Respuesta corta.** No con la tasa de error de transcripción medida en el corpus (0,22 % por cuerda): haría falta un 19–25 % por cuerda, 86–115 veces más, y aun así el modelo de transcripción predice que solo el 19 % de los fallos serían diferencias de un lugar decimal, cuando los 8 fallos observados lo son. El patrón —**un solo nudo, en un solo lugar decimal, ±1**— es la firma de un error de conteo al atar/leer el registro, no de ruido difuso. El generador que reproduce a la vez 8/18, el perfil de tolerancias, la bimodalidad de UR270→UR278 y el CV de las 9 columnas requiere **q ≈ 6–7 % por racimo** (≈ 20 % por cuerda, ≈ 50 % por registro). Nivel: **bien apoyado** que el ruido moderno medido no basta; **apoyado** que el error es de un nudo en el registro; **propuesto** que sea del quipucamayoc y no del transcriptor (la tasa local de transcripción no está medida de forma independiente: KFG y OKR de Incahuasi los firmó la misma persona, «julia»).

---

## 1. Datos y definiciones

- Unidad de análisis: el **quipu**; las pruebas entre cuerdas usan emparejamiento estructural (registro i con registro i), no búsqueda global.
- **Registro**: grupo de colgantes que no es separador rosa (PK); cabecera = primer colgante anudado. En UR273A/UR273B los separadores caen en los mismos grupos, lo que permite alinear registro a registro (13 §1).
- **A** = suma de las primeras subsidiarias de UR270 (parte pequeña, ~24 %); **B** = suma de los colgantes blancos (parte grande, ~76 %); **C** = cabecera del libro del flujo (UR266/UR275/UR269); **cuota** = cuerda fija (30 para A, 17 para B, 47 para A+B).
- Valores 0 sin nudos = cuerdas ausentes, nunca ceros reales.
- Fuente de los 18 registros: `analisis/13_sistema_incahuasi/componentes_filas.csv` (UR273A+UR273B), con destinos de 13 y recálculo propio contra las cabeceras de UR266/UR269/UR275.
- Fuente de UR270→UR278: `13_sistema_incahuasi/ur270_ur278.csv` y recálculo propio columna a columna.
- Tasa de transcripción moderna: **0,22 %** de cuerdas con valor distinto entre KFG y OKR (109/48 465), y **0,047 %** fuera de los 2 quipus estructurales (`ds/t_alt` §3.4). Es la única medida empírica disponible y se usa como cota.

## 2. Método

### 2.1 Generador

`02_simulador.py`. Un flujo tiene R registros. Cada registro se reparte en J = 9 unidades con pesos estables **w** (las medias reales de las 9 columnas de UR278: 290, 299, 209, 239, 255, 284, 246, 184, 195; CV = 0,163). Cada unidad se parte en B (~76 %) y A (~24 %). Niveles:

```
UR270 (detalle: 9 colgantes B + 9 subsidiarias A)
  ├─ UR278 (tabla DERIVADA: celda = B_j + A_j; solo error de transcripción)
  ├─ UR273A/274A (componente A, atado aparte)  ─┐
  └─ UR273B/274B (componente B, atado aparte)  ─┴─ A+B → UR266/275/269 (INDEPENDIENTE)
```

Dos tipos de enlace, con presupuestos de error distintos:

| tipo | qué es | error que admite |
|---|---|---|
| **derivado** | el destino se ata como suma de cuerdas que ya existen (UR278) | solo transcripción moderna |
| **independiente** | el destino se ata aparte desde el mismo hecho (libro del flujo) | error de **racimo** al contar/atar |

### 2.2 Parámetros explícitos

| parámetro | significado | valor | cómo se fijó |
|---|---|---|---|
| `med`, `sig_row` | mediana y dispersión del total bruto de un registro | 2015; 0,36 | mediana y CV reales de los totales de fila de UR278 (CV 0,364) |
| `sig_idio` | ruido de cada unidad | 0,24 | reproduce CV intra-fila 0,287 y correlación entre columnas 0,70 |
| `w_j` | cuotas relativas de las 9 partes | medias UR278 | dato (CV 0,163) |
| `a_mean`, `a_conc` | fracción de la parte A | 0,24; 30 | mediana real A/(A+B) (0,26) |
| `q_rac` | **error de un racimo** (nudo) en un componente, por racimo | **0,061** (IC ABC 0,056–0,067) | ajustado a 8/18 |
| `q_trans` | error de transcripción moderna por cuerda | 0,0022 | medido KFG↔OKR |
| `p_factor10` | fracción de erratas modernas que son ×10 | 0,20 | 22/109 de `t_alt` |
| `s_blank` | componente en blanco/perdido | 0,0–0,05 | grilla |
| `f_dest` | el libro destino se conserva | 15/18 | dato |
| `p_link` | grupos UR270 que son el mismo registro que UR278 | 5/12 | dato |
| `p_miss_cell` | celda de la tabla no copiada | 0,05 | ajuste |
| `b_rota` | cuerda rota/perdida | 0,006 | notas de rotura del corpus (0,56 %) |
| vacías por rol | componente / libro / detalle / tabla | 0,74 / 0,31 / 0,22 / 0,09 | dato por quipu |

### 2.3 Ajuste

- **Rejilla** 7 × 4 × 6 = 168 celdas (`rejilla_ajuste.csv`), 1 500 simulaciones por celda; distancia = suma de |sim − obs| en exactas, ≤1, ≤10, ≤1000, fracción 10^k y aciertos UR278.
- **ABC** con 2 000 simulaciones y 2 % de aceptación (`03_controles.py` §5) para la posterior de `q_rac`.
- **Controles:** nulo de emparejamiento por permutación de B entre registros (20 000 réplicas); p-valor empírico; 6 pruebas de ajuste global con **Holm**; análisis de sensibilidad a 8/18 vs 7/18 vs 8/15.

## 3. Resultados

### 3.1 Los 18 registros, uno por uno

| reg | A | B | A+B | destino (13) | Δ | clase |
|---|---|---|---|---|---|---|
| 0 | 272 | 3991 | 4263 | UR266 g15 = 4273 | −10 | **un nudo** |
| 1 | 297 | 2300 | 2597 | — | (36 al más cercano) | sin destino |
| 3 | 808 | 2142 | 2950 | UR266 g19 / UR275 g10 | 0 | exacta |
| 4 | 126 | 1249 | 1375 | UR269 g59 = 2375 | −1000 | **un nudo** |
| 6 | 30 | 1129 | 1159 | — | — | A en blanco (30 = cuota) |
| 9 | 453 | 1200 | 1653 | UR266 g25 / UR269 g5 / UR275 g16 | 0 | exacta |
| 10 | 448 | 1289 | 1737 | UR266 g26 / UR269 g11 / UR275 g17 | 0 | exacta |
| 11 | 502 | 1325 | 1827 | UR269 g17 | 0 | exacta |
| 12 | 448 | 1332 | 1780 | UR269 g23 / UR275 g19 | 0 | exacta |
| 13 | 579 | 1370 | 1949 | UR266 g29 = 1939 | +10 | **un nudo** |
| 14 | 672 | 1575 | 2247 | UR275 g21 | 0 | exacta |
| 15 | 509 | 1256 | 1765 | UR266 g33 | 0 | exacta |
| 16 | 325 | 1181 | 1506 | UR269 g49 / UR275 g23 = 1505 | +1 | **un nudo** (1506 = UR266 g2 es coincidencia) |
| 17 | 503 | 1193 | 1696 | — | (41 al más cercano) | sin destino |
| 18 | 526 | 1361 | 1887 | UR269 g61 = 1886 | +1 | **un nudo** |
| 19 | 517 | 1370 | 1887 | UR269 g61 = 1886 | +1 | **un nudo** |
| 20 | 368 | 1662 | 2030 | UR269 g69 / UR275 g13 = 2020 | +10 | **un nudo** |
| 21 | 263 | 1096 | 1359 | UR269 g45 = 2359 | −1000 | **un nudo** |

**Recuento.** 8/18 exactas según 13; **7/18** si se descarta la coincidencia 1506 = UR266 g2 (que 13 misma identifica como el total de UR278 g1) y se usa el destino estructural 1505 (±1). En los 15 registros comparables: **7 exactas y 8 discrepancias**, todas de un nudo. Tres registros no son comparables (2 sin destino + 1 con A en blanco).

**La firma.** Los 8 fallos con destino tienen |Δ| = 10^k **exactamente**: 1, 1, 1, 10, 10, 10, 1000, 1000. En los 8, **cambia una sola posición decimal y el dígito cambia en ±1**. Nulo con destinos aleatorios del pool (128 cabeceras): P(|Δ| = 10^k) = 0,011 → 8/8 dan p = 2·10⁻¹⁶ (7/7, con el recuento de 13: 1,6·10⁻¹⁴); P(cambia una sola posición) = 0,023 → p = 8·10⁻¹⁴. No hay ningún fallo difuso.

### 3.2 ¿Qué tasa de error explica 8/18?

Si todas las sumas fueran exactas en origen, un registro solo falla por error de transcripción moderna:

| supuesto | P(fallo por registro) | P(≥7 fallos en 15) |
|---|---|---|
| q = 0,22 % por cuerda (todo el corpus) | 0,0066 | **3,3·10⁻¹²** |
| q = 0,047 % por cuerda (fuera de quipus estructurales) | 0,0014 | **7,0·10⁻¹⁷** |
| contar 10 fallos en 18 (los 3 no comparables como fallos) | — | 6,4·10⁻¹⁸ |

Tasas necesarias para igualar 7–8 exactas de 15:

- **q = 0,189 por cuerda** (8/15, recuento de 13) → **86×** la tasa medida.
- **q = 0,216 por cuerda** (7/15, recuento estructural) → **98×**.
- **q = 0,237 por cuerda** (8/18) → **108×** la medida; **0,253** (7/18) → **115×**.
- Con q = 0,237–0,253, el corpus debería tener **≈ 11 500–12 300 cuerdas discrepantes** entre KFG y OKR; hay **109**. Es una contradicción directa, no un problema de potencia.

**Pero** (limitación importante): para Incahuasi la comparación KFG↔OKR **no es independiente**. Las 1 856 cuerdas de UR266/267/269/270/273/274/275/278 dan **0 discrepancias**, y eso no mide la calidad de la transcripción: `khipu_main.CREATED_BY` y `cord.CREATED_BY` son **«julia»** en las dos bases (KH0502, KH0506, KH0507, KH0510, KH0511, KH0512, KH0514, KH0517). La tasa local de transcripción, por tanto, **no está medida**. Lo que sí está medido es la tasa del corpus (0,22 %) y la coherencia interna de los valores (100 % `valor = Σ aportes`).

### 3.3 La firma distingue los dos mecanismos

Se simuló el modelo de «todo exacto en origen + transcripción» con la tasa que **sí** iguala 8/18 (q = 0,19):

| modelo | exactas/18 | fallos que son 10^k |
|---|---|---|
| observado | 0,444 | **1,000** (8/8) |
| transcripción q = 0,19 | 0,447 | **0,188** |
| transcripción q = 0,24 | 0,371 | 0,185 |
| racimo q = 0,061 + transcripción 0,22 % | 0,462 | 0,816 |

El modelo de transcripción puede copiar el **recuento** pero no la **forma**: solo el 19 % de sus fallos caen en un lugar decimal exacto, porque el error típico es ×10 de toda la cuerda o una errata de ±1–4. P(8/8 potencias de 10 | transcripción) = **1,5·10⁻⁶** (P(7/7) = 8,4·10⁻⁶). La razón de verosimilitud racimo/transcripción sobre (exactas = 8 y todas las discrepancias en 10^k) es **≥ 10⁴** (con 8 000 simulaciones el denominador no produjo ningún 8/8; se usa el valor analítico). Es decir: **no es que el sistema no pudiera ser exacto en origen; es que, si lo fuera, el error tendría que ser de un nudo en un lugar decimal, no una errata de transcripción.**

### 3.4 El generador reproduce el conjunto

Con `q_rac = 0,061`, `q_trans = 0,0022`, `s_blank = 0`:

| estadístico | observado | simulado | p posterior | Holm |
|---|---|---|---|---|
| fracción exactas /18 | 0,444 | 0,462 | 0,71 | 1,00 |
| ≤1 /18 | 0,556 | 0,539 | 1,00 | 1,00 |
| ≤10 /18 | 0,722 | 0,623 | 0,53 | 1,00 |
| fracción de fallos 10^k | 1,000 | 0,821 | 0,29 | 1,00 |
| aciertos medios UR278 (de 9) | 7,80 | 8,50 | 0,075 | 0,45 |
| filas UR278 con ≥6 aciertos | 5 | 5,06 | 1,00 | 1,00 |

Ningún estadístico rechaza el modelo tras Holm (mínimo 0,45). El único tenso es `≤10`: el modelo produce un 25 % de fallos en la posición de las centenas y en la muestra no hay ninguno; con 8 fallos, P(0 de 8 en centenas) = 0,10, no significativo.

### 3.5 UR270→UR278: no es ruido, es una mezcla

Aciertos por fila (de 9): **9, 9, 7, 8, 6, 5, 2, 1, 1, 1, 1, 1**.

- 5 filas con ≥6 aciertos y 6 filas con ≤2. Bimodal.
- Un **único** modelo binomial con p = 0,472 (la media) predice 2,4 filas ≥6 y 1,4 filas ≤2. La probabilidad de observar simultáneamente ≥5 y ≥6 es **< 5·10⁻⁶** (200 000 réplicas).
- El generador con `p_link = 5/12` (el grupo es el mismo registro) + cola no enlazada reproduce 5,06 filas ≥6 y una media de 8,5 aciertos en las enlazadas. La cola de 1–2 aciertos no es «error grande»: es **otro registro**, y coincide en 1–2 columnas porque los valores son redondos (100, 150, 200) y coincidir exacto es barato (`t_alt` §3.8).
- **Contraste de fidelidad:** el enlace derivado UR270→UR278 acierta **39/45 = 86,7 %** de las celdas (±1); el enlace independiente A+B→libro, **7/15 = 46,7 %**. Fisher 2×2: **p = 0,0034** (con el recuento de 13, 8/15, p = 0,012). No son el mismo tipo de enlace: uno se copia/suma, el otro se ata de nuevo.

### 3.6 Las otras salidas

| objetivo | real | simulado | veredicto |
|---|---|---|---|
| CV de las 9 medias de columna (UR278) | 0,163 (0,18 con las 28 filas de 13) | 0,163 | por construcción (w del dato) |
| CV dentro de fila | 0,287 | 0,29 | reproducido |
| correlación media entre columnas | 0,70 | 0,70 | reproducido |
| CV de los totales de fila | 0,364 | 0,36 | reproducido |
| mediana de la celda UR278 | 227 | 215 | KS D = 0,081, p = 0,055 |
| mediana de la parte A (UR273A) | 448 | 480 | KS p = 0,137 |
| mediana de la parte B (UR273B) | 1193 | 1527 | KS p < 0,001 (**no reproducido**) |
| mediana de cabeceras de libro | 1949 | 2015 | KS p < 0,001 (**forma no reproducida**) |
| vacías del corpus | 0,305 | 0,284 | reproducido con tasas por rol |
| tamaño de grupo (mediana / media) | 3 / 4,06 | 4 / 4,05 | media sí, forma no (KS p < 0,001) |

La parte B y las cabeceras no se reproducen bien porque el modelo fija A/(A+B) = 0,24 y las cabeceras reales incluyen cuota, partidas y grupos que no son registros. Es una limitación del generador, no un hallazgo. Las **vacías** sí: 30,5 % de cuerdas vacías frente a 0,56 % de notas de rotura (**56×**). No son roturas; son estructurales, y su tasa depende del rol del libro (74 % en los componentes, 9 % en la tabla).

## 4. Controles

1. **Nulo de emparejamiento** (permutar B entre los 18 registros, 20 000 réplicas): 8/15 exactas frente a media 0,44 y máximo 5; **p < 5·10⁻⁵** (0/20 000 réplicas ≥ 8). Coincide en orden de magnitud con el nulo de 13/16 (1,3 de 18) y con el de 18_equipo_rojo.
2. **Nulo de firma** (destino aleatorio del pool): P(|Δ| = 10^k) = 0,011; P(una sola posición decimal) = 0,023; los 8/8 dan p = 2·10⁻¹⁶ y 8·10⁻¹⁴ (7/7: 1,6·10⁻¹⁴ y 3,2·10⁻¹²).
3. **Corrección múltiple:** 6 pruebas de ajuste global, Holm → mínimo 0,45; nada se rechaza. La prueba central (tasa vs 8/18) es una sola prueba, no requiere corrección; se reporta el p exacto.
4. **Sensibilidad al recuento:** con 8/18, 7/18 (estructural) o 8/15 las conclusiones no cambian: q_rac pasa de 0,061 a ≈ 0,072, y el p de la prueba de tasa sigue < 10⁻¹¹.
5. **Semilla fija** 20261018; 1 500 simulaciones por celda de rejilla, 8 000 en la prueba central, 20 000 en los nulos.
6. **Control negativo del modelo derivado:** con solo transcripción (sin error de racimo) el enlace derivado acierta 8,5/9 y el independiente 15/15 exactas; el modelo **no** puede producir 8/18 sin el canal de racimo. Es decir, el mal ajuste de un modelo sin `q_rac` es el que identifica el parámetro.
7. **Duplicados físicos:** la parte A de UR274A coincide con la de UR273A en **13/13** registros solapados. La parte A no es un artefacto de lectura. La parte B no se pudo comprobar: los grupos de UR274B están desplazados (13 ya lo advierte) y las comparaciones directas dan diferencias grandes que son de alineación, no de nudo.

## 5. Resultados negativos

- **La copia no arregla los fallos.** UR273A+UR273B: 8/18 (7/18 estructural). UR274A+UR273B: 6/17. UR274A+UR274B: 0/15 (no alinean). Si el fallo fuera una errata moderna en una sola lectura, la segunda lectura de otra cuerda física debería corregir algunos; no lo hace.
- **El modelo de error difuso se rechaza.** Cualquier mecanismo que produzca diferencias arbitrarias (omisión de una unidad, ajuste, partida) no puede explicar 8/8 diferencias de exactamente 10^k (p ≈ 10⁻¹⁴).
- **El número de racimos no predice el fallo** en esta muestra: 17 % de fallo con ≤6 racimos vs 50 % con >6, Spearman 0,24, p = 0,335 (n = 18, sin potencia). La dirección es la esperada, pero no es evidencia.
- **La distribución de valores de la parte B y de las cabeceras no se reproduce** (KS p < 0,001). El generador sirve para el mecanismo de error, no como modelo completo de magnitudes.
- **El tamaño de grupo solo se reproduce en la media**, no en la forma (KS p < 0,001); se calibró por remuestreo, no se predijo.
- **UR270→UR278 no es un enlace ruidoso uno-a-uno**: 7 de 12 grupos no son el mismo registro (1–2 aciertos). Leerlos como «error de copia» sería un error de interpretación.
- **La tasa local de transcripción de Incahuasi no es medible con KFG↔OKR** (mismo transcriptor). Es la principal laguna del informe.

## 6. Nivel de evidencia

- **Bien apoyado:** (i) 8/18 es incompatible con la tasa de transcripción medida (p = 3,3·10⁻¹²), y haría falta 86–115× esa tasa; (ii) los 8 fallos con destino son diferencias de un solo nudo en un solo lugar decimal (p = 2·10⁻¹⁶); (iii) UR270→UR278 es bimodal, no ruido (p < 5·10⁻⁶); (iv) el enlace derivado es más fiel que el independiente (Fisher p = 0,0034); (v) las vacías no son roturas (56×).
- **Apoyado con datos:** q_rac ≈ 6–7 % por racimo (19–22 % por cuerda, 47–53 % por registro) como parámetro que reproduce el conjunto; el error está en el registro atado, no en ruido difuso; la parte A está confirmada por el duplicado físico (13/13).
- **Propuesto:** que el error sea del quipucamayoc al atar (y no del transcriptor). La firma y los duplicados lo favorecen, pero la tasa local de transcripción no está medida de forma independiente.
- **Especulativo:** qué flujo/registro concreto se equivocó; la identidad de las 9 columnas; que los 3 flujos perdidos (cuotas 46, 46, 44) tengan la misma tasa.

## 7. Qué predice el modelo que aún no hemos medido

1. **En una muestra nueva de ~15 registros comparables** (p. ej. los 5 quipus de Inkawasi que Urton no estudió): **7–8 exactas y 7–8 discrepancias, todas de un nudo**, con |Δ| repartido ≈ 2 en 1, 2 en 10, 2 en 100, 2 en 1000. Si aparece una diferencia de 37 o de 250, el modelo cae.
2. **En la cuerda física:** el racimo discrepante debe estar en **una sola banda decimal** y diferir en **un nudo** (±1) del valor del libro. Es comprobable con las fotos o con la cadena `nudos` de KFG: para cada fallo, el patrón de dígitos de A (o B) debe coincidir con el del libro salvo una banda. Predicción concreta: en el registro 0, B = 3991 debería ser 4001 (decenas 9→0 con acarreo); en el 4, B = 1249 debería ser 2249 (millares 1→2); en el 13, B = 1370 debería ser 1360 (decenas 7→6).
3. **La copia UR274B, bien alineada, no debe corregir a UR273B** si el error es de atado; si lo corrige, el error era de lectura. Es la prueba que separa «quipucamayoc» de «transcriptor» y aún no se ha hecho (UR274B tiene los grupos desplazados).
4. **Los flujos 46/44**, si existen, deben mostrar la misma firma de un nudo y la misma tasa (≈ 50 % de registros con una discrepancia). Es la predicción que 13 dejó abierta.
5. **Otras tablas derivadas** del corpus deben tener fidelidad alta (≥ 85 %) y otros libros independientes fidelidad baja (≈ 50 %). Si una tabla derivada muestra 50 %, el modelo de dos canales falla.
6. **Las cuerdas vacías no deben correlacionar con las notas de rotura** entre quipus (predicción: correlación ≈ 0, pendiente 0). Si las vacías fueran roturas, la correlación sería alta.
7. **El CV de 0,163 debe ser estable entre mitades** (Spearman de las cuotas relativas = 0,65; niveles = 0,47). Predice que las 9 cuotas son una propiedad del sistema, no del periodo.

## 8. Qué lo refutaría

- Que una **segunda transcripción independiente** de UR273A/B (o las fotos) diera valores distintos en ≥ 15 % de las cuerdas: entonces el error sería del transcriptor y «todas exactas en origen» volvería a ser viable.
- Que en los 8 fallos el racimo discrepante **no** esté en una sola banda decimal (p. ej. dos nudos en dos bandas, o una diferencia de 37): el mecanismo de un nudo quedaría refutado.
- Que UR274B, bien alineado, **corrija** sistemáticamente los fallos: el error estaría en la lectura, no en el atado.
- Que una tabla derivada distinta muestre la misma fidelidad baja que un libro independiente: el contraste derivado/independiente (Fisher p = 0,0034) sería un artefacto de UR278.

## 9. Para el coordinador

- **El 8/18 no es ruido de transcripción.** Con la tasa medida (0,22 % por cuerda) la probabilidad de 7 fallos en 15 es **3·10⁻¹²**; haría falta un **19–25 % por cuerda**, 86–115× la tasa, y el corpus tendría ~11 500 discrepancias en vez de 109.
- **La forma del fallo es la prueba fuerte:** los 8 fallos con destino son diferencias de **exactamente 10^k**, con **una sola posición decimal cambiada y ±1**. Nulo: 2·10⁻¹⁶. Un error de transcripción daría diferencias difusas o ×10 del valor entero; solo el 19 % de sus fallos caerían en 10^k.
- **Modelo generativo:** un registro se reparte en 9 unidades (CV de medias 0,163; CV intra-fila 0,287; correlación 0,70); A y B se atan por separado; el libro se ata de nuevo. El parámetro que reproduce todo es **q ≈ 6–7 % por racimo** (≈ 20 % por cuerda, ≈ 50 % por registro). El ajuste global pasa Holm (mínimo 0,45) en 6 estadísticos.
- **UR270→UR278 es una mezcla, no un enlace ruidoso:** 5 filas con 6–9/9 y 6 filas con 1–2/9; un binomial único no puede producir ambas (p < 5·10⁻⁶). La tabla es **derivada** (86,7 % de celdas) y el libro es **independiente** (46,7 %); Fisher p = 0,0034. Leer los 7 grupos no enlazados como «error» sería un error.
- **La copia no arregla nada:** UR274A+UR273B da 6/17 exactas (vs 8/18); UR274A+UR274B, 0/15. La parte A sí está confirmada por el duplicado (13/13). El error no es una errata de una sola lectura de A.
- **Laguna crítica, y hay que decirlo:** para Incahuasi, KFG y OKR los firmó la **misma transcriptora («julia»)**; 0/1 856 discrepancias no son independencia. La tasa local de transcripción **no está medida**. Por eso «el error es del quipucamayoc» queda **propuesto**, no bien apoyado.
- **Resultado negativo útil:** las cuerdas vacías (30,5 %) no son roturas (0,56 %, 56×); son estructurales y dependen del rol del libro (74 % en componentes, 9 % en la tabla). El generador las reproduce con tasas por rol (28,4 % ponderado).
- **Predicción para la próxima ronda (barata):** en los 5 quipus de Inkawasi no estudiados por Urton, buscar parejas A/B con cuotas 46/44; predecimos ~50 % de registros con **una** discrepancia de un nudo, y |Δ| ≈ 10^k. Si aparece una diferencia difusa, el modelo cae.
- **Predicción sobre el objeto:** en el registro 0, B = 3991 debería ser 4001; en el 4, 1249 → 2249; en el 13, 1370 → 1360. Es comprobable en las fotos o en `nudos` sin volver a transcribir.
- **Consecuencia para el resto del archivo:** cualquier relación entre quipus que dependa de dos registros atados por separado tiene un techo de ~50 % de coincidencia exacta. Los barridos que exigen 8/8 o 9/9 están midiendo, en realidad, enlaces **derivados** (copias o tablas), no registros independientes.

## 10. Reproducción

```
python 01_datos.py        # estadísticos reales + ab_reales.csv + datos_reales.json
python 01b_objetivos.py   # perfil A+B, nulos de cercanía, CV, copias
python 01c_firma_error.py # firma de un nudo, Fisher, mitades de UR278
python 02_simulador.py    # generador + rejilla (rejilla_ajuste.csv)
python 03_controles.py    # tasas, firma, nulo, Holm, ABC (controles.json)
python 04_validacion.py   # valores, vacías, grupos, copias, racimos
python 05_resumen.py      # bimodalidad y razón de verosimilitud (final.json)
```

Semilla 20261018. Todo se escribe en `analisis/ds/n_simulador/`; no se modificó nada fuera de esta carpeta.
