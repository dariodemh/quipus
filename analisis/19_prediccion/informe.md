# 19 · Prueba de lectura: ¿predice el modelo de 13 una cuerda que no ha visto?

Carpeta `analisis/19_prediccion/`. Semilla 19 (el método es determinista; no hay azar salvo en los controles, que también lo son). Datos: los 13 quipus del sistema (UR270, UR273A/B, UR274A/B, UR278, UR266, UR275, UR269, UR267A/B, UR255, UR256) con 1558 cuerdas con valor. Se reutiliza `analisis/13_sistema_incahuasi/comun13.py` sin modificarlo; no se usa ninguna arista de `grafo_cuerdas.csv` para predecir (solo para marcar qué cuerdas se usaron en el descubrimiento).

## Para el coordinador

1. **Cuántas cuerdas se pueden predecir.** 791 de 1558 (50,8 %) tienen al menos una vía ciega; 168 tienen ≥2 vías con entradas disjuntas y 19 tienen ≥3. Las 767 restantes no participan en ninguna relación que se pueda aplicar sin mirar su valor (UR273A/B: solo 20 de 56).
2. **Acierto del modelo (LOO, una cuerda oculta por vez, una predicción por cuerda).** Exacta 58,8 %, ±1 en un dígito 70,3 %, error relativo ≤5 % 74,7 %. Mejor línea base: 20,5 % exacta (valor más frecuente del quipu); media de columna 3 %, registro anterior 17 %, regresión por magnitud de fila 6 %. Unión de las 4 bases (cuenta si cualquiera acierta): 27 %.
3. **Dónde "leemos" de verdad** (regla; exacta del modelo frente a la mejor base en esas mismas cuerdas): UR270 ↔ UR278 (celda = colgante + subsidiaria) 74 % frente a 2 %; fila de UR278 ↔ cabeceras de UR266/UR275 55 % (79 % ±1) frente a ≤4 %; A+B → cabecera del libro 41 % frente a 9 %; copias 48 % frente a 17 %; cierre del registro (cabecera = suma del resto) 62 % frente a 27 %. **La cuota constante (70 %) no cuenta**: la moda del quipu la iguala (70,5 %); predecir "47" en UR275 no demuestra nada.
4. **Honestidad.** (a) Todas las reglas se formularon mirando estos mismos valores. Las cuerdas ajenas al descubrimiento (no aparecen en ninguna arista del grafo ni en los grupos emparejados UR270/UR278) son 126 con predicción: acierto 17,5 % exacta, **sin ventaja clara sobre las bases** (11,9–15,1 %). Las usadas en el descubrimiento: 66,6 %. La cifra honesta está más cerca de lo primero para "cualquier cuerda" y de lo segundo para "cuerdas dentro de un registro bien alineado". (b) Validación por bloques de registros (se ocultan los demás registros del bloque): la exacta global por predicción es 58,4 % en LOO, 61,3 % con 4 bloques y 57,7 % con 2, pero con menos cobertura (752 y 659 predicciones frente a 1098): lo que se pierde es cobertura, no acierto, salvo la copia (49 % → 18 % con 4 bloques), que depende de anclas vecinas. (c) Control nulo: la misma maquinaria de alineación sobre pares sin relación da 0 % de acierto exacto (51 predicciones). (d) No se puede medir cuánto infla la elección de las reglas (qué pares, qué mapeos): eso exigiría quipus nuevos.
5. **Predicciones para el museo:** `predicciones_museo.csv`, 252 filas: 149 discrepancias cercanas (cuerda registrada con otro valor predicho), 7 discrepancias de fila de UR278 y 96 reconstrucciones de cuerdas sin nudos. 122 tienen confianza media o alta (43 alta). Las más útiles se listan en §6.
6. **¿Podemos decir que "leemos" este archivo?** **Solo parcialmente y con matices.** Sí: *leemos la aritmética* de la cadena UR270 → UR278 → UR266/UR275 y de los componentes con cuota (UR255/UR267A/UR267B), con aciertos exactos de 55–83 % sobre cuerdas ocultas frente a 0–27 % de las bases, y con un control nulo en 0 %. No: no leemos el archivo entero (49 % de las cuerdas sin vía), UR269 (19 % exacta), UR274B, UR273A/B; las alineaciones entre quipus con estructuras distintas fallan al ciegas; y no leemos el *contenido* (qué es cada columna, qué cuenta cada cuota). Redacción prudente: "el sistema aritmético permite reconstruir ciegamente algo más de la mitad de las cuerdas de seis quipus del flujo 47/25; la lectura completa sigue sin demostrarse".

## 1. Método

| Script | Qué hace |
|---|---|
| `comun19.py` | Motor de predicción ciega. `predecir(cuerda, hide)` aplica 6 reglas sin leer los valores ocultos. Las correspondencias entre quipus se buscan con LCS de las demás cifras (exacto o ±1) y se emparejan por orden dentro del hueco entre dos anclas si ambos huecos tienen igual longitud (`contra`); nunca se usa el valor oculto ni las aristas del grafo. |
| `01_loo_inventario.py` | Tareas 1 y 2: inventario de redundancia y LOO. |
| `02_baselines.py` | Tarea 3. |
| `03_validacion_cruzada.py` | Tarea 5: CV por bloques de registros y control nulo. |
| `04_museo.py` | Tarea 4. |

Reglas: **copia** (cabecera copia en el quipu pareja; dentro del registro, cuerda por posición); **suma_AB** (cabecera del libro = A_i + B_i; A_i = cabecera − B_i; B_i = cabecera − A_i; registros de A y B por orden, ver 13); **fila278** (cabecera de UR266/UR275/UR269 = suma de una fila de UR278; celda = cabecera − otras celdas); **celda270** (celda de UR278 = colgante + subsidiaria s1 de UR270 en la misma columna; fila de UR270 elegida por las otras columnas, ≥4 coincidencias y única); **cierre** (cabecera = suma del resto de cuerdas del registro; solo en quipus donde el resto de registros cierra ≥50 %); **cuota** (la cuerda en la posición modal de la cuota = constante del quipu, estimada sin la cuerda oculta). Métricas: exacta, ±1 en un dígito (`tol`: diferencia 0, 1, 10, 100…), error relativo ≤5 % (`r5`) y error relativo mediano. Una cuerda oculta sin predicción cuenta como "no predecible", no como fallo, en las tablas del modelo; en las bases una cuerda sin predicción cuenta como fallo.

## 2. Inventario de redundancia (`inventario_redundancia.csv`)

Cuerdas con valor y con vía ciega, por quipu: UR255 54/65, UR256 52/99, UR266 50/120, UR267A 67/76, UR267B 62/106, UR269 52/218, UR270 100/297, UR273A 9/23, UR273B 11/33, UR274A 25/50, UR274B 21/65, UR275 93/114, UR278 195/292. Número de vías (independientes = con entradas disjuntas): 1 vía, 528 cuerdas; 2 vías, 231 (142 con entradas disjuntas); ≥3 vías, 32. El fichero da por cuerda las vías, cuántas aciertan (exacta y ±1) y si estaba en el grafo de 13 (`en_grafo_13`, 665 de las 791).

Las vías de UR266/UR275 no son del todo independientes entre sí: una es copia de la otra, aunque sean cuerdas distintas. Las parejas UR278 → libro y A+B → libro sí son independientes (entradas disjuntas): es la "doble entrada" de 13.

## 3. Leave-one-out (`loo_resultados.csv`, `loo_consenso.csv`, `salida_01_loo.txt`)

Por regla (todas las vías, 1098 predicciones):

| Regla | n | exacta | ±1 dígito | ≤5 % |
|---|---|---|---|---|
| celda270 | 150 | 0,740 | 0,880 | 0,913 |
| cierre | 245 | 0,616 | 0,706 | 0,771 |
| cuota | 217 | 0,705 | 0,742 | 0,774 |
| fila278 | 252 | 0,476 | 0,714 | 0,730 |
| copia | 150 | 0,487 | 0,513 | 0,573 |
| suma_AB | 84 | 0,393 | 0,393 | 0,512 |

Por quipu (consenso por cuerda; exacta): UR255 0,83; UR267A 0,79; UR274A 0,76; UR270 0,74; UR267B 0,63; UR278 0,61; UR256 0,54; UR275 0,47; UR273B 0,45; UR273A 0,44; UR266 0,40; UR274B 0,29; **UR269 0,19**. (La tabla completa regla × quipu está en `loo_resumen_regla_quipu.csv`: p. ej. la cuota en UR269 solo acierta 20 %, porque allí varía por fila de bloque 47/46/46/44/25 y la regla ciega usa la moda; la suma hacia UR269 acierta 0 de 6.)

Hallazgos de detalle:
- **Acuerdo entre vías.** De 263 cuerdas con ≥2 vías, en 158 coinciden (acierto exacto 76,6 %); donde no coinciden, 6,7 %. El acuerdo es una buena señal de fiabilidad. Las cuerdas con una sola vía aciertan 63,8 %.
- **Hueco entre anclas.** En la copia, cuando las dos anclas son contiguas (hueco 1) la exacta es 80,6 % frente a 26,1 % con huecos largos. En fila278 y suma_AB no hay tal gradiente (el fallo no es de alineación sino de que la relación no cierra; ver siguiente punto).
- **Cuando la regla no cierra, falla toda la fila.** UR278 g4 suma 3293 y el libro dice 3317 (+24); g8 3243 frente a 3249 (+6); g12 2533 frente a 2633 (+100). En esas filas las 9 predicciones de celda salen desplazadas en la misma cantidad y cuentan como fallos: parte de los fallos de fila278 son discrepancias reales entre libros, no errores del método. Son también candidatas para el museo (§6).

## 4. Líneas base (`baselines_tabla.csv`, `salida_02_baselines.txt`)

Mismas cuerdas ocultas. Exacta del modelo frente a cada base (una cuerda sin predicción de la base cuenta como fallo):

| Subconjunto | n | modelo | mediana col. | media col. | registro previo | moda quipu | magnitud fila |
|---|---|---|---|---|---|---|---|
| todas (consenso) | 791 | **0,588** | 0,183 | 0,030 | 0,174 | 0,205 | 0,063 |
| celda270 | 150 | **0,740** | 0,007 | 0 | 0 | 0,020 | 0,027 |
| fila278 | 170 | **0,547** | 0 | 0 | 0,012 | 0 | 0,041 |
| suma_AB | 46 | **0,413** | 0 | 0 | 0 | 0 | 0,087 |
| copia | 149 | **0,483** | 0,101 | 0,020 | 0,087 | 0,128 | 0,174 |
| cierre | 245 | **0,616** | 0,257 | 0,065 | 0,249 | 0,269 | 0,163 |
| cuota | 217 | 0,705 | 0,664 | 0,111 | 0,622 | **0,705** | 0,009 |
| no usadas en descubrimiento | 126 | 0,175 | 0,119 | 0 | 0,151 | 0,135 | 0,008 |
| usadas en descubrimiento | 665 | 0,666 | 0,195 | 0,036 | 0,179 | 0,218 | 0,074 |

Lectura: el modelo gana por mucho (≥2,5 veces, y en celda270/fila278/suma_AB por 8–100 veces) en las reglas que codifican aritmética entre cuerdas. Empata con la moda en la cuota (esperable: es una constante). **En las cuerdas ajenas al descubrimiento la ventaja casi desaparece** (0,175 frente a 0,151). "Por mucho" solo vale para las relaciones ya identificadas.

## 5. Honestidad: descubrimiento frente al resto, CV y control nulo

- **Todas las cuerdas se usaron, en sentido amplio.** 13 hizo búsquedas exhaustivas sobre todos los valores del archivo; ninguna cuerda es "virgen". Separo las que aparecen en una arista del grafo o en un grupo emparejado UR270/UR278 (`descubrimiento = True`, 665 de las 791 predecibles) del resto (126). Esto cuantifica el efecto selección: 66,6 % frente a 17,5 % de acierto exacto (consenso). La diferencia mezcla dos cosas: inflación por haber elegido relaciones que cerraban, y que las cuerdas fuera del grafo son precisamente donde las relaciones no cierran o la regla no aplica. La verdad está entre ambos números.
- **Validación cruzada por bloques de registros** (`cv_resumen.csv`; se ocultan los demás registros del mismo bloque, de modo que cuotas, anclas y tasas de cierre se formulan solo con el resto del quipu):

| Regla | LOO exacta (n) | CV 4 bloques | CV 2 mitades |
|---|---|---|---|
| celda270 | 0,740 (150) | 0,740 (150) | 0,740 (150) |
| cierre | 0,616 (245) | 0,642 (201) | 0,544 (204) |
| cuota | 0,705 (217) | 0,693 (212) | 0,639 (191) |
| copia | 0,487 (150) | 0,183 (82) | 0,316 (114) |
| fila278 | 0,476 (252) | 0,574 (68) | sin predicciones |
| suma_AB | 0,393 (84) | 0,513 (39) | sin predicciones |

  Las cuotas y el cierre se mantienen (la cuota estimada con una mitad predice la otra: 64–69 %). celda270 no cambia porque su emparejamiento usa las demás columnas de la propia fila, no los vecinos. La copia sí cae con 4 bloques (49 → 18 %): depende de anclas vecinas. fila278 y suma_AB pierden casi toda la cobertura con mitades: el alineamiento ciego no puede extrapolar a un tramo entero sin anclas. Los números con menor n son poco estables.
- **Control nulo.** Copia con 6 pares de quipus sin relación: 51 predicciones, 0 exactas y 1 dentro de la tolerancia (2 %). Contra esto, el 48 % de la copia real no es azar de la alineación.
- **Lo que no se mide:** la elección de las reglas y de los pares (qué quipus son pareja, que UR267A+B va a UR269 y UR273/274 a los tres libros, el umbral de cierre del 50 % y MINC = 4) se hizo mirando estos datos. La prueba definitiva sería predecir quipus nuevos del mismo depósito, por ejemplo los cinco que Urton no estudió.

## 6. Predicciones para el museo (`predicciones_museo.csv`)

Columnas: quipu, cuerda, tipo, valor_registrado ("sin nudos" para ausentes), valor_predicho, vía, reglas_independientes, confianza_num, confianza, alternativas. La confianza es la tasa de acierto exacto de la regla en ese quipu en el LOO; si ≥2 reglas distintas coinciden se usa 0,77. Solo se conservan las discrepancias cercanas (≤10 % o ≤10 unidades en valores <100), porque un error de lectura da valores próximos; las diferencias grandes indican más bien que la regla no aplica. "alta" ≥0,75, "media" 0,5–0,75.

Las más verificables (comprobar en el objeto):

| Quipu / cuerda | Registrado | Predicho | Vía y razón |
|---|---|---|---|
| UR278 g21, 1.ª celda (`p180`) | 238 | 237 | colgante + subsidiaria de UR270 g0 (178 + 59 = 237) y el total 1653 de UR266/UR275 |
| UR278 fila g12 (una celda de las 9) | suma 2533 | 2633 | UR266 y UR275 dicen 2633; una celda debe valer 100 más |
| UR278 fila g4 | suma 3293 | 3317 | libro UR275 g0/UR266: +24 en alguna celda (o subsidiaria olvidada) |
| UR278 fila g8 | suma 3243 | 3249 | libro: +6 |
| UR278 filas g13, g17, g19 | 3095, 2115, 2105 | 3096, 2114, 2106 | ±1 en una celda |
| UR278 g27 (`p217`), 4.ª celda | 246 | 290 | UR270 g8: 238 + 52. **No está en el CSV** (diferencia >10 %, fuera del filtro); viene de la lista de 13 |
| UR278 g28 (`p228`), 6.ª celda | 300 | 394 | UR270 g9: 334 + 60; **no está en el CSV** (fuera del filtro); confianza baja (la colgante de UR270 cambia de color a los 45 cm) |
| UR274B (`p9`, `p13`, `p19`, `p64`) | 10 | 17 | la cuota del quipu es 17 y 1332 = 1315 + 17 |
| UR275 g10, cuota (`p51`) | 40 | 47 | cuota del quipu (0,96); 13 ya lo señalaba |
| UR267A (`p27`) | 16 | 15 | cuota del quipu (0,92) |
| UR266 `p22` | 44 | 47 | cuota (0,52) |
| UR275 `p88` | 1825 | 1827 | A+B = 502 + 1325 = 1827 |
| UR270 (p1/p1s1, p47/p47s1, p63/p63s1, p67/p67s1, p71/p71s1, p72/p72s1…) | varias | −1 a −3 | UR270 no suma exactamente a la celda de UR278 en esos grupos (0,74) |

Reconstrucciones (cuerdas sin nudos): 96, 25 de confianza alta. Ejemplos: UR255 `p2` = 91, `p10` = 45, `p22` = 70, `p25` = 145, `p28` = 99, `p31` = 126, `p34` = 172, `p38` = 80, `p41` = 200 (neto = cabecera − 15; verificables además con la copia en UR267A, donde existe el valor), cuotas ausentes de UR255 (15), UR256 (10), UR274A (30) y UR275 `p110` (47). La mayoría de las predicciones de baja confianza (45 reconstrucciones, 78 discrepancias, 7 de fila) quedan en el CSV por completitud; no se recomienda gastar tiempo de museo en ellas. Ojo: muchas predicciones "media" de UR267A/UR256 provienen del cierre en registros con partidas y conviene tratarlas como hipótesis débiles; las filas de fila de UR278 y las cuotas de UR274B y UR275 son las más claras.

## 7. Resultados negativos

- La regla A+B → libro apenas funciona hacia UR269 (0/6) y es débil hacia UR266/UR275 (50 %).
- UR269 (19 % exacta): el modelo no lo lee más que puntualmente.
- UR273A/B y UR274B: pocas cuerdas y bajo acierto (29–45 %).
- El alineamiento ciego no extrapola a tramos largos sin anclas (mitades: sin predicciones para fila278 y suma_AB).
- La cuota no discrimina entre modelo y base.
- Las cuerdas ajenas al descubrimiento no son mejor predichas que por las bases (17,5 % frente a 15,1 %).

## 8. Niveles de evidencia

- **Apoyado con datos:** UR270 ↔ UR278 (celda = P + S; 74 % exacta y 88 % ±1 en LOO frente a ≤3 % de las bases); fila de UR278 ↔ cabeceras de UR266/UR275; cierre y cuota en UR255/UR256/UR267A/UR267B/UR274A/UR275; acuerdo entre vías como indicador de fiabilidad (77 % frente a 7 %).
- **Propuesto:** que A+B → libro sea predictivo al ciego (41 %; la evidencia de 13 sigue siendo de relaciones halladas, no de predicción).
- **Especulativo:** cualquier lectura del archivo completo; UR269 como libro maestro (solo 19 % predecible).
- **Demostrado:** solo el control nulo (la maquinaria de alineación no predice por azar en pares sin relación).

## 9. Siguiente ronda

1. Verificar en el objeto las discrepancias de §6 (primero UR278 g12, g21 c1, g27 c4 y las cuotas de UR274B); cada resultado afina la confianza.
2. Predecir quipus no usados en este análisis (cinco de Inkawasi no estudiados por Urton) con el motor tal cual: es la única prueba sin sesgo de selección.
3. Mejorar UR269 con la posición de fila en el bloque de 5 (cuotas 47/46/46/44/25) para la cuota y la suma, y repetir el LOO.
4. Sustituir el emparejamiento por huecos de igual longitud por un modelo de offset constante para extrapolar tramos.
