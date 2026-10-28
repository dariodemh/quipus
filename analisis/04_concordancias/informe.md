# 04 · Concordancias entre quipus: copias, versiones y resúmenes

Equipo: archivística y patrones a gran escala. Fecha: 2026-10-17.
Scripts (reproducibles, semillas fijas): `concordancias.py` (tareas 1, 1b y 2; ~13 min con numba, 20 núcleos), `archivos.py` (tareas 3 y 4), `verificacion.py` (pruebas dirigidas). `python concordancias.py --demo` corre la autocomprobación (copia sembrada con un error de ±1 dígito y una cuerda omitida; resumen sembrado; par independiente no significativo).
Resultados en `resultados/`. Los más útiles: `pares_significativos.csv`, `alineamientos.txt` (las cuerdas alineadas, una por línea, con color, largo y nudos), `archivo_<nombre>_aristas.csv`, `verificacion_salida.txt`.

## 1. Método

**Secuencia de un quipu.** Valores de todas las cuerdas con nudos (colgantes y subsidiarias), en `orden`. Las cuerdas sin nudos se tratan como ausentes y se quitan. Entran 636 quipus con 3 o más cuerdas anudadas, es decir 201 930 pares.

**Puntuación de copia (tarea 1).** Uso alineamiento local Smith-Waterman con huecos (5 bits por hueco) y puntuación log-odds en bits:
- coincidencia exacta: log2(0,85/f(v));
- tolerante, cuando |a−b| = 10^k (un dígito ±1): log2(0,05/t(v));
- discordancia: log2(0,10/(1−f−t)).

f y t se calculan sobre la composición conjunta **del par**. Así, «1-1-1» entre dos quipus llenos de unos vale cerca de 0 bits y «57-30-56» vale mucho. Se alinea B en los dos sentidos.

**Nulo (tarea 1).** Se barajan los dos quipus, lo que conserva la distribución de valores de cada uno.
- Todos los pares reciben 50 permutaciones.
- Los pares con p<0,01 (1169) reciben 1000 permutaciones más.
- Si la observación supera todas las permutaciones, la cola se extrapola con una Gumbel ajustada por momentos (Karlin-Altschul), con escala mínima 1/ln 2 para evitar colas degeneradas. En los demás casos se usa el p empírico.
- La corrección es BH-FDR sobre los 201 930 pares; los pares no refinados conservan su p de 50 permutaciones.
- Calibración: el 0,58 % de los pares tiene p<0,01, así que el nulo es conservador.

**Nulo secundario por bloques.** Se permutan bloques de 5 cuerdas para conservar la autocorrelación local. Lo reporto, pero es **demasiado conservador para copias verdaderas**: conserva los bloques compartidos y por eso el duplicado documentado KH0033/UR044 queda con q_bloque = 1. No lo uso como criterio.

**Tarea 1b.** El mismo análisis se repite solo con la subsecuencia de valores ≥100 (las «cabeceras»). Así resiste versiones que intercalan cuerdas pequeñas. Abarca 265 quipus y 34 980 pares.

**Preselección por n-gramas (recomendada en el encargo).** Usé 3-gramas exactos con todos los valores ≥10, en ambos sentidos. Seleccionan 2392 pares, pero **5 de los 25 pares significativos no tienen ninguna semilla**, entre ellos KH0049/UR122 y UR064/UR068: los errores de ±1 dígito y las subsidiarias intercaladas rompen los 3-gramas exactos. Como el barrido exhaustivo con numba dura unos 2 minutos, lo usé como método principal. Las semillas quedan solo como columna de control.

**Resumen (tarea 2).**
- Para cada quipu A calculo la secuencia de totales de sus grupos, sumando los colgantes anudados de los grupos que tienen 2 o más. Esa secuencia se alinea contra la secuencia de cuerdas de B. Hay 311 150 pares ordenados.
- Saltar un total de A cuesta 5 bits. Saltar una cuerda de B cuesta solo 0,1 bit, porque los totales pueden estar dispersos en B (por ejemplo, la 1.ª cuerda de cada grupo).
- La probabilidad de azar es la composición de B. Un total grande y raro puntúa mucho; uno pequeño y común, casi nada.
- Hay tres nulos:
  - **(a)** se barajan los colgantes de A entre posiciones, conservando el tamaño de los grupos (totales nulos de magnitud realista), y también B;
  - **(b)** el mismo, por bloques;
  - **(c) nulo de orden:** los mismos totales de A en orden aleatorio y B intacto. Mide solo si las coincidencias siguen el orden.
- Control interno: el método detecta las cuerdas superiores que suman grupos dentro de un mismo quipu (AS006 p=0,001; AS007 p=0,006).

**Archivos (tarea 3).**
- Incahuasi: 52 quipus (JC001–023, UR255–280).
- Puruchuco: UR060–UR082, la vasija de Mackey; el OKR los da como «Huaquerones» y 20 tienen datos.
- Santa: UR087–092.
- Leymebamba: UR001–022.
- Pachacamac: 90 quipus, 86 con datos, según la procedencia declarada.

Dentro de cada archivo aplico BH sobre los pares del archivo. Además pruebo:
- **sumas cuerda a cuerda** B = A1 + A2: ventanas exactas de 3 cuerdas con B ≥10, extendidas; p FWER contra 100 barajados del archivo;
- **totales globales**: si el total de A aparece como cuerda de B; el nulo usa totales de quipus ajenos al archivo.

**Artefactos (tarea 4).**
- Comparo cada par con `okr-kh-numbers.csv`: mismo número KH, o duplicado declarado en los comentarios.
- Uso la geometría como prueba de «mismo objeto». Si se midió dos veces el mismo objeto, los largos de cuerda casi coinciden; la regla se calibró con los dos duplicados documentados (KH0033/UR044: r = 1,00, diferencia mediana 0 cm; AS125/UR247: r = 0,92, 2 cm). Criterio: r_largo ≥ 0,9 y diferencia mediana ≤ 2,5 cm.
- Los tramos con 4 valores distintos o menos se marcan como débiles, porque pueden ser artefactos de rachas.

## 2. Resultados

### 2.1 Tarea 1: cuasi-duplicados (FDR global, 25 pares con q<0,05)

| par | museos / procedencia | tramo | alineadas (exactas/±1/discord.) | q | clase |
|---|---|---|---|---|---|
| **HP055 ≈ UR1084 (=AS084)** | MNAAHP Lima, procedencia desconocida / Quai Branly, París | p1–185 / p1–180 | 142 (121/8/13), 27 huecos | 2e-86 | candidata a copia: casi todo el quipu; cabeceras 1080, 1091, 1078, 1069, 1077 idénticas en orden; largos r = 0,31 |
| **UR1175 (=AS175) ≈ UR233** y **≈ UR232** | Berlín VA42518, «Pachacamac» / Berlín VA63038(A)/(B), «Huacho» | UR1175 p1–104 ↔ UR233 entero; UR1175 p160–223 ↔ UR232 p49–124 | 93 (77/11/5) y 50 (38/6/6) | 4e-41; 1e-18 | candidata a copia; correspondencia de color sistemática (LB↔RB, YG↔GG, YB↔AB, W↔W); 100↔110 sistemático; largos muy distintos (24 cm), luego objetos distintos |
| **KH0049 (=AS038/HP036) ≈ UR122** | MNAAHP Lima, «Costa Sur» / Göteborg, «Nazca» | p77–99 / p41–63 | 80 (60/2/18) | 1e-38 | **versión**: los colgantes son idénticos (1146, 1590, 960, 855, 1856, 2578, 974, 1095, 849, 790, 6485, 875) y las subsidiarias difieren |
| UR053B ≈ UR053C | BCR, mismo inventario ATE 3517 | p1–32 / p11–58 | 48 (35/3/10) | 3e-26 | copia dentro de un conjunto atado |
| UR006 ≈ UR009 ≈ UR021 | Leymebamba | UR006 p276–338 | 61, 21, 19 | 1e-20 a 2e-8 | réplica de Urton (2005); UR009 está registrado en sentido inverso |
| UR064 ≈ UR068 | Puruchuco núm. 3 / núm. 2 | entero | 47 (41/4/2) | 1e-20 | réplica de Urton (2005): 1212/1213, 1236, 459, 56, 57 |
| UR066 ≈ UR067 | Puruchuco | entero | 21 (20/0/1) | 6e-9 | copia: 2904, 156, 133 |
| MM015, MM016, MM008 ≈ UR212 | Basilea IVc.366.03 (los tres «Eduard Gaffron») / Berlín VA42513, «Pachacamac» | tres tramos disjuntos de UR212: p182–194, p140–153 y p6–14 | 13, 13, 8 | 8e-12, 7e-9, 5e-3 | **copia fragmentada** en otro museo; MM016 copia además UR1131 (52, 87, 65, 45, 192; q = 0,018) |
| UR1114 ≈ UR1123 | Berlín | p40–49 / p41–50 | 10 exactas | 3e-10 | réplica de Urton (2005), con el segmento 40-9-57-30-56-80-21-8-22-12 |
| UR1118 ≈ UR218 | Berlín VA42601 / VA42559, Pachacamac | p2–9 / p7–14 | 8 (620, 470, 528, 935/932, 474, 319, 453, 492) | 2e-4 | candidata a copia |
| QU002 ≈ UR137 | Dallas / Lowe (Miami), «Chancay» | p10–17 / p11–18 | 11 | 5e-4 | candidata a copia |
| AS159 ≈ AS173 | Berlín | p1–7 / p2–8 | 8 exactas | 3e-3 | réplica de Urton (2005) |
| UR255 ≈ UR267A | Incahuasi | p13–57 / p11–52 | 28 (27 exactas), 14 huecos | 5e-3 | versión: UR267A intercala cuerdas AB:MB que faltan en UR255 |
| AS128 ≈ QU013; UR113 ≈ UR271 | Berlín / Dallas; Göteborg / Incahuasi | — | 28; 10 | 4e-13; 1e-5 | **débiles**: 4 y 3 valores distintos (rachas de 3-4 y de 220/200) |
| MM019 ≈ UR131C | Stuttgart / Chile | — | 8 | 0,047 | marginal |

**Duplicados de base de datos.** No son hallazgos; se listan aparte:
- **KH0033/UR044**: mismo KH; el OKR declara que UR044 es un duplicado inacabado de AS031.
- **AS125/UR247**: el OKR declara que KH0140 y KH0483 son el mismo quipu.
- **UR1107 (=AS107, VA24370(B)) / UR237 (VA66834): duplicado NO documentado.** Los largos dan r = 0,99 y la diferencia mediana es 1,25 cm; está registrado en sentido inverso y con números de inventario distintos. Conviene notificarlo al OKR. Encaja con el caso KH0198 (AS181 = UR236, VA66832), que sugiere que la serie VA66xxx de Berlín re-inventarió objetos que los Ascher ya habían registrado.
- Las colisiones de número KH dentro del KFG (KH0197/UR1180, AS207C/KH0227, KH0267/UR034, KH0350/UR114) **no comparten contenido** (p entre 0,06 y 0,94). Son errores de etiqueta, no datos duplicados.
- Entre JC (Clindaniel) y UR (Urton) de Incahuasi no hay ningún par significativo, así que no hay doble registro.

**Controles positivos (Urton 2005).**
- Detectados: AS159/AS173, UR1114/UR1123, el trío UR006/UR009/UR021 y Puruchuco núm. 3/núm. 2 (UR064/UR068).
- No detectado AS194/AS195: tienen 5–6 cuerdas anudadas, demasiado poco para sobrevivir a un FDR sobre 200 000 pares.
- No detectado UR1116/UR1150: Urton describe diferencias sistemáticas, no una copia.

### 2.2 Tarea 2: relaciones de resumen

Globalmente, con q<0,05 en el nulo (a), salen 3 de 311 150 pares ordenados.
- **UR278 → UR266**: q = 1e-8; robusto a los tres nulos (q_bloque = 1e-8; p_orden = 2e-9, q_orden = 7e-4).
- **UR278 → UR275**: q = 0,007; q_bloque = 0,005; p_orden = 2e-6, aunque q_orden = 0,27 con m = 311 150.
- UR113 → UR264: es un **artefacto**. Lo sostienen totales pequeños (7, 14, 22, 25, 29, 30, 35) dispersos en 210 cuerdas; falla el nulo de orden (q = 1) y la prueba con totales ≥100 (LCS 3, p = 0,52).

**Verificación por lectura de cuerdas (`verificacion.py`).**
- UR278 (Incahuasi) tiene 33 grupos de unos 9 colgantes, de 124 a 537. Por ejemplo, el grupo 0 es 415+415+353+415+415+415+414+413+363 = **3618**.
- Sus totales aparecen **en orden** como la 1.ª cuerda (W/AB) de los grupos de UR266: 3618, 1506, 1384, 2919, 2089, 1842, 1876, 2229, 4273, 2533/2633, 3095/3096, 2950, 1278, 2115/2114, 2105/2106, 1654/1653.
- Subsecuencia común más larga, con ±1 dígito: **16 de 33**. En el nulo la media es 2,8 y el máximo 7 en 2000 permutaciones (p < 5e-4).
- En UR275, copia de UR266, coinciden 11.
- Casi todas esas cabeceras de UR266 van seguidas de una cuerda constante **47**.
- La cabecera no es la suma del resto del grupo de UR266 (solo 2 de 19 grupos), así que el total no se calcula dentro de UR266: viene de UR278.

**Negativos.**
- Ninguna otra relación sobrevive en el corpus.
- Las relaciones UR004 → UR006/UR011/UR021 (Leymebamba) y UR1034 → UR1145 (Pachacamac) eran significativas en el archivo con el nulo (a), pero caen con el nulo de orden y con totales ≥100. Son artefactos de valores pequeños (2–35), justo el caso que había que penalizar.

### 2.3 Tarea 3: grafos por archivo

**Incahuasi**: 52 quipus, 1326 pares; es el único archivo con jerarquía bien apoyada.
```
UR278 (detalle: 33 grupos × ~9) ──totales──▶ UR266 ══copia══ UR275
UR270 (grupos) ──4 totales──▶ UR274B   (propuesto)
UR255 ══versión══ UR267A        UR256 ══versión══ UR267B   (UR267A/B: mismo inventario, A y B)
```
- UR270 → UR274B: las cuerdas W de UR274B 1332, 1402, 1300 y 1575 son totales de grupos de UR270. Además, cada una va seguida de un desglose con la constante 17 (1402 = 1385 + 17; 1300 = 1283 + 17). La LCS da p = 0,0035, pero no sobrevive al FDR del archivo con el nulo de orden: **propuesto**.
- Las «versiones» UR267A/UR275 contienen las cuerdas de su par más cuerdas extra intercaladas, de color moteado (AB:MB, W:MB).
- Las sumas cuerda a cuerda y los totales globales son negativos (p = 0,60 y 0,063).
- Hay 41 quipus aislados.

**Puruchuco**: 20 quipus con datos, 190 pares.
```
UR064 ══ UR068 (núm. 3 / núm. 2)     UR066 ══ UR067
UR063 ◀══ UR073 (cabeceras 127/126, 229, 148, 367/368, 157/147: 5/5 en orden, p=1e-4 frente al archivo)
UR063 ◀── UR078 (último bloque 219, 6; débil)
```
Propuesta: UR063 consolida los bloques de UR073 y UR078. En el FDR del archivo dan q = 0,047 y 0,039; en el global no son significativos.

No hay relaciones de resumen: los totales de grupo, las sumas cuerda a cuerda (racha máxima 0) y los totales globales (p = 0,15) dan negativo. **No reproduzco la jerarquía de sumas de Urton y Brezine (2005) con estas definiciones**; de ese trabajo solo tenemos el resumen.

**Santa**: 6 quipus. **Ningún par es copia ni resumen** de otro (todas las p > 0,05; tarea 2 p ≥ 0,16; sumas negativas). Los seis registran contenidos distintos.

**Leymebamba**: 22 quipus. El triángulo de copias UR006–UR009–UR021 (Urton 2005) se replica; nada más. Las aristas de resumen desde UR004 son artefactos (ver 2.2). Las sumas cuerda a cuerda dan p_FWER = 0,059.

**Pachacamac**: 86 quipus, 3655 pares.
- Hay una copia interna (UR1118 ≈ UR218) y un duplicado de base (AS125/UR247).
- Fuera del archivo, varios quipus atribuidos a Pachacamac tienen copias en otros fondos: UR212 y UR1131 en los fragmentos de Basilea (MM008/015/016), y UR1175 en UR232/233.
- No hay relaciones de resumen (sumas p_FWER = 0,059; totales globales p = 1).

## 3. Nivel de evidencia

| conclusión | nivel |
|---|---|
| UR278 → UR266/UR275: los totales de los grupos de un quipu de detalle se registran en orden como cabeceras de otro quipu, que a su vez tiene una copia | **bien apoyado** (3 nulos y lectura de cuerdas) |
| Existen copias exactas o casi exactas entre quipus de un mismo archivo (Leymebamba, Puruchuco, Incahuasi, Berlín/Pachacamac); réplica de Urton (2005) | **bien apoyado** |
| Copias entre objetos de museos distintos: HP055/AS084, AS038/UR122, Basilea/UR212, UR1175/UR232-233, QU002/UR137 | **apoyado con datos** (estadística fuerte; la identidad física y la procedencia no están verificadas) |
| «Consolidación»: un quipu grande que reúne a varios menores (UR1175 = UR233 + UR232; UR063 = UR073 + UR078; MM016 = tramos de UR212 y UR1131) | **propuesto** |
| UR270 → UR274B; constantes 47 y 17 como deducciones fijas | **propuesto** |
| Archivos jerárquicos como norma general | **especulativo**: solo Incahuasi muestra resumen; Santa, Puruchuco, Leymebamba y Pachacamac dan negativo |

## 4. Negativos y limitaciones

- No hay relaciones de resumen fuera de Incahuasi. Las sumas cuerda a cuerda (B = A1 + A2) no superan el nulo en ningún archivo. Los totales globales de un quipu no aparecen en las cuerdas de otro más de lo esperado.
- Las coincidencias con valores pequeños son abundantes y falsas. El nulo de orden y la prueba con totales ≥100 las eliminan.
- Los largos distintos indican objetos distintos, pero dos equipos (HP frente a AS/UR) pueden medir de forma distinta. Las asignaciones «copia frente a mismo objeto» deben confirmarse en los museos.
- Las convenciones de color difieren entre investigadores, así que el acuerdo de color entre equipos no sirve como criterio.
- Las relaciones de resumen se probaron solo con grupos de colgantes (nivel 0). No probé subtotales por color, subsidiarias ni sumas de varios quipus de detalle.

## 5. Próxima ronda

1. Comprobar en los museos HP055 frente a AS084, UR1107 frente a UR237 (y avisar al OKR), y los fragmentos de Basilea frente a UR212: historia de la colección Gaffron.
2. Incahuasi: buscar sistemáticamente los patrones «total = x + 17» y «cabecera + 47» en todo el archivo, y comprobar si las cuerdas moteadas intercaladas de UR267A/UR275 son aritmética de sus vecinas (W/AB/AB:MB de Clindaniel).
3. Ampliar el resumen a totales por color y por subsidiarias, y a sumas de N quipus de detalle alineadas por grupo.
4. Usar la regla geométrica de duplicados para depurar el corpus antes de cualquier análisis por quipu.
