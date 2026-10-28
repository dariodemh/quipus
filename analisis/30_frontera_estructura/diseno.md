# 30. Frontera: diseño congelado (escrito antes de correr ninguna prueba)

Fecha de congelación: 2026-10-18. Semilla: 20261018. Ningún resultado de las pruebas se ha mirado al escribir esto; solo tamaños (cuerdas por quipu, subsidiarias) para fijar mínimos.

## Muestra

- **Frontera F** = filas de `analisis/28_atlas_generos/atlas.csv` con `genero == SIN` y `evidencia` que empieza por «decimal sin estructura detectada» (180). Los 113 de «datos insuficientes» quedan fuera.
- **División exploración / confirmación:** los 180 se ordenan por kfg, se estratifican por transcriptor (prefijo: UR, AS, resto) y dentro de cada estrato se barajan con `numpy.random.default_rng(20261018)`; la primera mitad (redondeo hacia abajo) de cada estrato va a **A (exploración)**, el resto a **B (confirmación)**.
- **Secuencia de un quipu:** colgantes (`nivel == 0`) en el orden `orden`; valor = `valor` (0 si no tiene nudos). Grupos = `grupo`. Subsidiarias = `nivel == 1` con su `padre`. Color normalizado con `re.sub(r'\([^)]*\)','',s)`; en las pruebas entre quipus no se usa el color (solo particiones dentro de un quipu).

## Compañeros (pruebas entre quipus)

- **Museo normalizado** por palabras clave (berlin, incah/inahuasi, Museo Nacional de Arqueología/Pueblo Libre/Museo Nacional Lima → MNAAHP, banco central, Ica, Quai Branly/Musée de l'Homme → París, Hannover/Hanover West Germany, Hamburg, Soldi); el resto, el texto tal cual.
- **Sitio** = `procedencia`; desconocido si es Unknown, Peru, South Peru, Aankoop o vacío.
- Compañeros de I1–I7: los otros 179 de la frontera ∪ todos los quipus (de cualquier género) del mismo museo ∪ del mismo sitio.
- Compañeros de I8–I9 (jerarquía débil): los del mismo sitio; si el sitio es desconocido, los del mismo museo.
- **Se excluyen pares que son el mismo objeto** (04: «duplicado de base» o «mismo objeto»: UR1107/UR237, AS125/UR247, KH0033/UR044). UR1107/UR237 se usa como control positivo aparte.

## Coincidencia con tolerancia («±1 en un dígito»)

`tol(a,b)`: a = b, o |a − b| = 10^d y la cifra d del menor no es 9 (es decir, difieren en exactamente una cifra, por una unidad, sin acarreo).

## Batería (16 pruebas por quipu; NA si no aplica)

Peso de un valor v en un quipu: w(v) = −ln(frecuencia de v entre sus colgantes no nulos). Las rachas de valores triviales (1, 1, 1…) pesan poco.

**Internas** (nulo = permutación de los colgantes del propio quipu, con la estructura indicada):

| id | Estructura | Estadístico | Nulo |
|---|---|---|---|
| T1 | periodicidad de valores | rangos centrados; ACF(k) para k = 2…⌊n/3⌋; prominencia = ACF(k) − (ACF(k−1)+ACF(k+1))/2; máx. sobre k con ACF(k) > 0 | permutación total de valores |
| T2 | periodicidad de la partición de color | igual, con A(k) = P(color_i = color_{i+k}) | permutación total de colores (≥ 2 colores) |
| T3 | subsecuencia repetida con tolerancia | dentro del quipu, máx. sobre desfases δ ≥ 1 de la suma de pesos de una racha diagonal de coincidencias `tol` (ambos > 0), longitud ≥ 3 | permutación total |
| T4 | tendencia monótona por grupo | Σ\|S_Kendall\| / Σ máx, grupos con ≥ 4 colgantes no nulos | permutación de los no nulos dentro de cada grupo |
| T5 | subsidiaria como ajuste de su colgante | pares (colgante>0, subsidiaria directa>0), ≥ 5 pares: (a) frecuencia de la razón exacta modal, (b) de la diferencia ≠ 0 modal, (c) ρ de Spearman; min-p calibrado | barajar subsidiarias entre pares |
| T6 | cuerda = suma de bloque no contiguo | n.º de colgantes con valor ≥ 10 iguales (exacto) a la suma de L = 2…12 colgantes a paso k = 2…12 inmediatamente antes o después de ella (≥ 2 sumandos no nulos) | permutación total |
| T7 | pares que suman lo mismo | esquemas: pares adyacentes con desfase 0 y 1, espejo dentro de grupo (≥ 4), espejo de todo el quipu; por esquema (≥ 4 pares), n.º de pares con la suma modal (suma ≥ 2); min-p calibrado | permutación total |

**Entre quipus** (estadístico = máximo sobre compañeros; el nulo permuta el lado indicado y recalcula el máximo con los mismos compañeros):

| id | Estructura | Estadístico | Nulo |
|---|---|---|---|
| I1 | misma secuencia (copia) con tolerancia | máx. suma de pesos de una racha diagonal (≥ 3) de `tol` contra la concatenación de compañeros | permutar colgantes de F |
| I2 | misma secuencia invertida | igual con F invertido | idem |
| I3 | diferencia constante d ≠ 0 | racha (≥ 3) con B_j − F_i constante ≠ 0, peso | idem |
| I4 | escala (razón constante r ≠ 1) | racha (≥ 3) con B_j/F_i constante ≠ 1 (exacta), peso | idem |
| I5 | orden de grupos permutado | grupos de F (≥ 2 no nulos) que coinciden posición a posición (`tol`) con un grupo de igual tamaño del compañero; estadístico = emparejados − LIS (grupos desplazados) | permutar colgantes de F conservando tamaños de grupo |
| I6 | suma aproximada de bloque contiguo de F en un compañero | n.º máx. de cuerdas distintas (cualquier nivel, ≥ 10) de un compañero que igualan con `tol` alguna suma de L = 2…12 colgantes contiguos de F (≥ 2 no nulos) | permutar colgantes de F |
| I7 | suma aproximada de bloque de un compañero en F | n.º máx. de cuerdas distintas de F (≥ 10) que igualan con `tol` una suma de bloque de un compañero | permutar colgantes de cada compañero |
| I8 | jerarquía débil hacia arriba: total de grupo de F aparece en otro quipu del sitio | n.º máx. de grupos de F (≥ 2 no nulos, total ≥ 10) cuyo total aparece (exacto) como cualquier cuerda de un compañero del sitio | permutar colgantes de F conservando tamaños de grupo |
| I9 | jerarquía débil hacia abajo: total de grupo de un quipu del sitio aparece en F | n.º máx. de grupos de un compañero cuyo total aparece (exacto) en F | permutar colgantes de cada compañero |

## Valores p

- p = (b + 1)/(N + 1), con b = réplicas nulas ≥ observado.
- Escalada secuencial (Besag–Clifford): internas 999 → 9 999 → 99 999; entre quipus 199 → 1 999 → 19 999 → 99 999. Se pasa a la siguiente etapa solo si b ≤ 2 (internas) o b ≤ 1 (entre quipus), y si la etapa siguiente cabe en el presupuesto de tiempo (se registra N).
- min-p (T5, T7): p de cada subestadístico por rango sobre las mismas réplicas; p final = rango del min-p observado entre los min-p nulos.

## Multiplicidad y decisión

1. **q global** = BH sobre TODAS las pruebas no NA (16 × 180, ambas mitades). **Holm global** sobre el mismo conjunto.
2. **Exploración (A):** una familia (prueba) se **promueve** si en A tiene ≥ 1 descubrimiento con BH(A) q < 0,10 (BH sobre todas las pruebas de A), o si el número de quipus con p < 0,05 supera la binomial(n_A no NA, 0,05) con p unilateral < 0,05.
3. **Confirmación (B):** solo familias promovidas. Una familia **se replica** si en B (a) la binomial de p < 0,05 da p < 0,05 tras Holm sobre las familias promovidas, o (b) hay ≥ 1 quipu de B con q < 0,05 en un BH restringido a {familias promovidas × quipus de B}.
4. **Nivel por fila (quipu × prueba):**
   - **bien apoyado**: Holm global < 0,05 y la familia se replica.
   - **apoyado**: q global < 0,05 y la familia se replica.
   - **propuesto**: q global < 0,05 pero la familia no se replica (o no se promovió); o, en B, q confirmatorio < 0,05 con q global ≥ 0,05.
   - **especulativo**: p < 0,01 sin lo anterior.
   - **ninguno**: el resto.
5. **Deja la frontera** un quipu con al menos una fila bien apoyada o apoyada. Se informa aparte si la relación ya la conocía 04 (`pares_significativos.csv`): eso no es estructura «nueva», es un detector existente que el atlas no convirtió en género.

## Tasa de falsos positivos

- Analítica: BH controla FDR ≤ 5 %; Σq de las filas que hacen salir a un quipu como cota del número esperado de falsos.
- **Empírica:** se repite todo el procedimiento (mismas reglas, misma división, misma escalada) sobre una **frontera nula**: cada quipu sustituido por una permutación de sus colgantes (conservando tamaños de grupo), colores y subsidiarias barajados de forma independiente; los compañeros reales no se tocan. Cuántos quipus «dejan la frontera» en el nulo = falsos positivos esperados del procedimiento. Si el tiempo lo permite, 2 réplicas.

## Controles positivos (deben dar p < 0,01; si no, se informa la falta de potencia)

- I2 invertida: UR1107 frente a UR237 (mismo objeto, orden inverso), incluido como compañero solo aquí.
- I1 copia: UR1084 frente a HP055.
- I8 total de grupo: UR278 frente a los quipus de Incahuasi (sus totales están en UR266).
- Internas: un quipu sintético por prueba, construido con valores reales barajados de la frontera y una estructura plantada (periodo 5, repetición de 6 valores, grupos ordenados, subsidiaria = colgante/10, cuerda = suma a paso 3, pares espejo que suman 50, colores con periodo 4).

## Predicciones

Cada fila con nivel ≥ propuesto lleva una predicción comprobable generada a partir de sus cifras (compañero, desfase, constante, lag, grupo).

## No se repite

Sumas internas contiguas (01/08), copias directas exactas ya listadas (04/14, se marcan como conocidas), formularios (22), tablas R × K (10), asignación por redondeo (11), tally Z (27) y plantillas P4r/P8ar/P11a (n_plantillas). I1 se incluye solo para la frontera y separando lo ya conocido.

## Enmienda 1 (antes de correr sobre datos reales; motivada solo por los controles sintéticos)

- **T1**: con rangos, un periodo 5 perfecto repetido 6 veces daba solo p = 0,013 (el ruido de la ACF a desfases grandes es alto). Se añade un segundo subestadístico, la prominencia de la coincidencia exacta de valores no nulos (como T2), y T1 pasa a min-p calibrado de {rangos, iguales}.
- **T6**: la suma a paso k con 264 combinaciones por cuerda tiene poca potencia (control p = 0,31). Se añade un segundo subestadístico: cuerda = suma de la **misma posición** en L ≥ 2 grupos consecutivos (antes o después), y T6 pasa a min-p de {paso_k, misma_posición}. El control sintético de T6 se cambia a 3 totales por posición en el último de 4 grupos.
- Controles sintéticos tras la enmienda: los 7 con p ≤ 0,005 (`controles_internos.csv`).

## Enmienda 2 (antes de correr las pruebas entre quipus sobre la frontera; motivada solo por los controles)

- **I1–I4**: la racha diagonal más larga no tolera huecos; el control HP055/UR1084 (copia con omisiones) daba p = 0,015. El estadístico pasa a ser, para cada compañero, la **suma de pesos de las posiciones de F cubiertas por rachas de ≥ 3** con ese compañero (une tramos separados por huecos o sustituciones); máximo sobre compañeros. Nulo sin cambios.
- Controles tras la enmienda: I2 UR1107~UR237 p = 5e-4 (15 posiciones cubiertas), I1 UR1084~HP055 p = 5e-4 (125), I8 UR278→Incahuasi p = 1e-5 (UR266). Los dos primeros con N = 1 999 por presupuesto de tiempo.
- Presupuesto de escalada en las pruebas entre quipus: 300 s por prueba (se corren en 10 procesos paralelos). Consecuencia conocida: en compañeros grandes el suelo de p es 5e-4, por debajo del umbral de Holm global (~1,7e-5); esas filas pueden llegar a «apoyado», no a «bien apoyado».

## Enmienda 3 (POSTERIOR a ver los resultados; solo puede quitar descubrimientos)

Al inspeccionar las filas significativas vi dos confusiones posibles que los nulos congelados no controlan:

1. **Autocorrelación local de F** (rachas de valores iguales, escalones 1-2-3 que `tol` empareja) infla T3 e I1–I4 frente a una permutación total de F, porque la permutación rompe las rachas. Nulo alternativo: permutar como bloques los tramos máximos de valores consecutivos `tol`-iguales.
2. **Agrupamiento de subsidiarias** bajo un mismo colgante y **magnitud propia de cada grupo** inflan T5 (la permutación por pares trata como independientes subsidiarias hermanas, y un grupo de valores grandes con subsidiarias grandes da ρ > 0 sin relación colgante a colgante). Nulo alternativo: mover el conjunto de subsidiarias de un colgante entero a otro colgante **del mismo grupo** (estadístico ρ de Spearman, que fue el ganador en todas las filas T5 con p < 0,01).
3. **I6** depende de cómo se reparten ceros y valores en F (sumas de bloque más variadas), no solo de un compañero: mismo nulo por tramos que I1–I4. Además, en UR1049 el máximo lo alcanzan varios compañeros grandes por igual (UR034 y QU011, 77 aciertos cada uno), señal de que no hay compañero específico.

Se recalcula con el nulo alternativo cada fila de esas familias con p < 0,05 (en la frontera real y en la nula; con 0,05 y no 0,01 para que el test binomial de réplica también use p corregidos) y se usa **p efectivo = max(p, p_bloque)**. Como p solo puede subir, BH/Holm siguen siendo válidos (la decisión es más conservadora). Todo lo demás (promoción, réplica, niveles) se recalcula igual. Se informan ambos resultados.
