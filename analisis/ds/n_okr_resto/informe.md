# Pendientes del Open Khipu Repository (ronda 18): KH0674, KH0675, KH0676, discrepancias y KH0632

## 1. Pregunta

Cerrar los pendientes que dejó el equipo 17 en `analisis/17_okr_pendientes/`:

1. Transcribir las tablas de cuerdas de **KH0674 (UR-297)** y **KH0675 (UR-298)**, dos PDF escaneados sin capa de texto, y validar valor = suma de nudos.
2. Convertir **KH0676 (JS01)** desde el xlsx de la tesis de Strauss, sin columna de valor, y decidir la regla decimal. Resolver si el inventario `80.1012 aka 2708` del OKR corresponde al `36.718` del JS01.
3. Clasificar las **21 discrepancias** valor ≠ suma de nudos de `cuerdas_extra.csv` y las **6 discrepancias por quipu** entre `AS1-AS9.db` y KFG.
4. Confirmar que **KH0632** no tiene datos.

## 2. Método

### 2.1 Escaneos y OCR

- Renderizado con PyMuPDF a 300 dpi (`render_paginas.py`): 47 páginas KH0674, 18 KH0675, 10 KH0676. Miniaturas y hojas de contacto para orientación.
- OCR con Tesseract 5 (`ocr_paginas.py`) sobre las 75 páginas. **El OCR no sirve para las tablas**: son manuscritas, con lápiz y correcciones. Se usó solo para detectar orientación y estructura de página.
- Orientación automática probando 0/90/180/270° y puntuando palabras clave (`orientar.py`); las páginas de tabla quedaron todas a 270° (giro horario de 90°). Dos páginas (KH0674 p016 y p025) exigieron corrección manual.
- **Transcripción visual** de cada página a `transcripcion_KH0674*.txt` y `transcripcion_KH0675.txt`, con el formato `pagina|cuerda|spin/ply/attach|nudos|nota`. Se marca `?` lo ilegible y se anotan las dudas en la última columna.
- La transcripción cubre **cuerda, spin/ply/attach, nudos, valor y subsidiarias**. No se transcribieron color, largo, grosor ni terminación de KH0674/675 (están en la mitad derecha de las mismas páginas); quedan vacíos en los CSV y se listan como pendientes de una segunda pasada.

### 2.2 Regla decimal

La regla usada en `convertir_transcripcion.py` es la de Ascher / KFG:

- Los racimos se leen de arriba abajo. El último racimo ocupa las **unidades** si es largo (L) o figura de ocho (E). Si el último es simple (S), los simples ocupan las **decenas** (un nudo simple nunca es unidad).
- Cada racimo anterior sube una decena. Valor del racimo = nº de nudos × 10^lugar.
- Se verificó contra los valores escritos a mano en la ficha: KH0675 183 = 1.380; 185 = 1.758; 188 = 18.067; 189 = 2.755; 201 = 1.486; 197 = 15.980. KH0674 337 = 12; 210 = 111.

Para **KH0676** se usa otra regla, la que declara la propia hoja (`Pendant Detail!K3`): *"all single knots = 10, long knots = their value in parentheses, e-knot = 1"*. Es aditiva: cada nudo simple vale 10, cada largo sus vueltas, cada ocho 1, sin jerarquía entre racimos. La variante jerárquica (la de KH0674/675) se guarda en la columna `alt`. Justificación en 3.3.

### 2.3 Control de calidad

No hay prueba de hipótesis: es una tarea de transcripción, no de inferencia. El "modelo nulo" no aplica y por eso no se reporta p-valor. Los controles son deterministas:

- **Valor = suma de nudos**: 100% de las 1.047 filas nuevas (se calcula, no se copia).
- **Conteo independiente de cuerdas**: las portadas de las fichas permiten comprobar la transcripción (3.1–3.3).
- **Recálculo desde la fuente** de las 21 discrepancias (no se confió en la suma que dejó el equipo 17).
- **Calibración empírica** de la regla de KH0676 contra la distribución de 57.818 cuerdas de `cuerdas.csv` (3.3).
- Las 27 clasificaciones son un **censo**, no una muestra: no procede corrección de comparaciones múltiples (Holm/BH). Si se quisiera tratar como tests, habría que corregir 27 contrastes; no se hace porque no hay hipótesis.

## 3. Resultados

### 3.1 KH0674 / UR-297 (Dumbarton Oaks, PC.WBC.2016.072)

Ficha manuscrita de 47 páginas: portada, dos páginas de grupos y 36 páginas de tabla (cuerdas 1–438). Dos tramos de cordón principal unidos a 27 cm (cordón A: 1–93; cordón B: 94–438).

| concepto | cifra |
|---|---:|
| filas transcritas | 624 (1 sin valor: 188s1, ilegible) |
| colgantes | 438 (1–438, sin huecos) |
| subsidiarias | 186 |
| cuerdas sin nudos | 164 (134 colgantes, 30,6%) |
| suma de valores | 11.688 |
| valor máximo | 810 (cuerda 29: 8S + 1S) |
| grupos | 41; la suma de los rangos de la portada da exactamente 438 |

- La estructura de grupos de las páginas 1–3 (posición en cm, rango, espacio) se usó para la columna `grupo`. Los 41 rangos cubren 1–438 sin solapamientos.
- La nota de la página 3 dice: *"In each of the 41 groups, one cord has been pulled up to a position resembling a top cord. These may actually be summary cords. These top cords are circled"*. Se marcaron dos círculos visibles (cuerdas 170 y 181), pero **no se hizo un inventario sistemático de los 41 círculos**; queda como pendiente.
- Orden: la ficha escribe 45 y 45s1 antes de 44 (que va insertada con una flecha); el CSV ordena 44 antes de 45. La cuerda 337 está escrita antes que 336 y con un asterisco; se conserva 336→337 y se anota.
- **Validación contra totales de la ficha (negativa)**: las páginas de resumen (p040–p043) dan "total on 10 cord group" para los grupos 1–11, 12–22, … 94–104. No reconcilian con la suma de las cuerdas principales: 1–11: 55 vs 28; 12–22: 70 vs 26; 23–33: 905 vs 54; 34–38: 56 vs 50; 39–49: 126 vs 150; 50–60: 182 vs 169; 61–71: 189 vs 258; 72–82: 152 vs 566; 83–93: 119 vs 217; 94–104: 145 vs 380. No se usaron como validación. La explicación más probable es que "total on 10 cord group" cuente otra cosa (nº de nudos, o cuerdas sin las subsidiarias y sin la cuerda resumen) o que los resúmenes se refieran a otra pasada de medición. **Propuesto, no bien apoyado.**

### 3.2 KH0675 / UR-298 (Dumbarton Oaks, PC.WBC.2016.071)

Ficha manuscrita de 18 páginas: portada y 17 páginas de tabla (cuerdas 1–203).

| concepto | cifra |
|---|---:|
| filas transcritas | 285 |
| colgantes | 203 (1–203, sin huecos) |
| subsidiarias | 82 |
| cuerdas sin nudos | 81 (75 colgantes, 36,9%) |
| suma de valores | 53.235 |
| valor máximo | 15.980 (cuerda 197: 1S+5S+9S+8S) |
| grupos | 10; el conteo de la portada coincide con 203 colgantes |

- La portada da los grupos por posición: 7,0 cm (1–6), 8,0 (7–30), 12,0 (31–48), 15,0 (49–66), 18,5 (68–93), 23,0 (94–99), 24,5 (100–111), 26,5 (112–123), 28,5 (124–180), 41,0 (181–203). Hay dos inconsistencias: la cuerda 67 no aparece en ningún rango (se asignó al grupo 49–67) y el grupo 124–180 dice 52 cuerdas pero el rango tiene 57. El total 203 sí cierra.
- La ficha repite el nombre `49s1s2` en dos cuerdas consecutivas; la segunda se renumeró `49s1s1` y se anotó. También hay dos filas rotuladas 136 (una de ellas es 135); se conservaron como 135 y 136.
- La cuerda 10 tiene tres racimos (`1S 1E 6L`) y un valor escrito de 17; la regla estándar da 17 (10+1+6), así que valor y ficha coinciden. La duda es el trazo del último racimo: si fuera `10L`, el valor sería 21. Se marcó dudosa la lectura, no el valor.

### 3.3 KH0676 / JS01 (Brooklyn Museum)

El xlsx `JS01_Strauss_Harvard_Senior_Thesis.xlsx` (exportación KDB del 2/1/2019) tiene **138 filas**: 65 colgantes y 73 subsidiarias. La portada del PDF dice "group of 65 cords (1–65)": **coincide exactamente**, lo que valida que no falta ninguna cuerda.

- **Regla**: la hoja declara en `Pendant Detail!K3`: *"all single knots = 10, long knots = their value in parentheses, e-knot = 1, keep in order of knot group on cord"*. Es una regla aditiva (simples = decenas, largos = unidades, ochos = unidades), no jerárquica.
- Con esa regla: suma 4.769, mediana 21,5, máximo 121.
- Con la regla jerárquica (la de KH0674/675), el 99% de las cuerdas tiene 3+ racimos y los valores se disparan: suma 670.004, mediana 681,5, máximo 314.120. Solo 3 cuerdas superan el percentil 99,9 del corpus KFG (18.727) y ninguna con la regla aditiva.
- **Decisión**: `valor` = regla de la hoja; `alt` = variante jerárquica. Nivel de evidencia: **apoyado con datos** (la nota de la fuente + la calibración + el conteo de 65 cuerdas), no bien apoyado, porque no hay columna de valor independiente contra la que contrastar.
- Seis cuerdas usan el tipo `SP` (13, 23, 41s2s1, 61, 65s3s1, 65s4s1); se trató como `S` y se anotó. Es una decisión que necesita revisión humana.

**El número de inventario.** El PDF (página 1, escrita por Julia Strauss el 12/17/18) dice, con la misma letra y en la misma hoja que el resto de la ficha:

> Museum Name: Brooklyn Museum
> Museum Number: 36.718

El xlsx (`Heading!A4`) repite `Museum Number: 36.718`. El OKR, en cambio, asigna a KH0676 `80.1012 aka 2708`, el mismo número que a KH0700 (Stanford, SB001). **Conclusión: el número `80.1012 aka 2708` de KH0676 es un error del OKR**; el JS01 es Brooklyn 36.718. Nivel: **apoyado con datos** (dos fuentes primarias independientes: la nota manuscrita y el xlsx). No se pudo consultar el catálogo del Brooklyn Museum para confirmar que 36.718 sea el número definitivo, así que no se eleva a bien apoyado. No existe en el OKR ningún KH con el número 36.718.

### 3.4 Discrepancias valor ≠ suma de nudos

#### 3.4.1 Las 21 de `cuerdas_extra.csv`

Al recalcular desde la fuente apareció el hallazgo principal: **11 de las 21 no son discrepancias de la fuente, sino errores de parseo del equipo 17**. Su regex exigía `nTIPO(pos,dirección,valor)` y descartó racimos escritos como `8L,15.0,S,8`, `1S(5.0S,10)`, `3S(25,0,U,1)` (coma decimal), `2S(8.5,Z.20)` o `1E(16.5,Z)` sin valor. Al leer el xlsx original, la suma coincide exactamente con el valor de la hoja. Se añadió la clase **(e) error de parseo**, que no estaba en el encargo pero es la causa dominante.

| clase | n | significado |
|---|---:|---|
| (e) error de parseo del equipo 17 | 11 | la fuente es coherente; no hay nada que corregir |
| (a) error de transcripción del valor/aportación | 5 | el valor de la hoja es correcto; el aporte escrito del racimo no |
| (b) nudo mal registrado (tipo o posición incoherente) | 5 | el valor de la hoja es plausible; el nudo está mal anotado |
| (c) cuerda rota/incompleta | 0 | — |
| (d) indecidible | 0 | — |

Casos que sí son de la fuente (no parseo):

- **KH0631 p1** (valor 404, suma 428): los dos últimos racimos (`2S` a 12,8 y `4S` a 15,8) caen junto al nudo largo de 12,7 o por debajo de las unidades. Se propone 404, clase (b), confianza media-alta.
- **KH0631 p4** (1375 vs 1376): un `1S(28.0)` final aporta 1 por debajo de las unidades; se propone 1375, clase (b), confianza alta.
- **KH0631 p6** (259 vs 282): `2S(21.5)` y `3L(30.5)` están bajo el `9L(18.0)`; se propone 259, clase (b), alta.
- **KH0634 p17s3** (9 vs 29): `2S(4.5)=20` + `9L=9`; la hoja solo anota 9. Se propone 29, clase (a), confianza media.
- **KH0635 p37s2** (15 vs 19): el `5L` tiene 5 vueltas pero la hoja escribe 9; 10+5=15, que es el valor de la hoja. Clase (a), alta.
- **KH0640 p5** (222 vs 22): tres racimos con aportes 200/20/2 anotados como `2L`; las posiciones (3,0/8,0/13,5) y el valor 222 son coherentes. Clase (b), media-alta.
- **KH0644 p1** (30 vs 3): un único `3S` vale 30 (decenas), no 3. Clase (a), alta.
- **KH0644 p2** (16 vs 7): `1S=10` + `6L=6`; la hoja da 16. Clase (a), alta.
- **KH0648 p6** (23 vs 29): el `2L(3.5)` con aporte 20 debería ser `2S`; `3L=3`. Valor 23. Clase (b), media-alta.
- **KH0651 p6** (33 vs 35): el `3L` tiene 3 vueltas, pero la hoja escribe 5; 30+3=33. Clase (a), alta.

**Resultado negativo:** ninguna de las 21 requiere cambiar el valor de la hoja por una cuerda rota; todas las diferencias reales se explican por (a) o (b), y 11 desaparecen al releer la fuente. La regla "valor = suma de nudos" del equipo 17 estaba mal implementada en el parser, no en la fuente.

#### 3.4.2 Las 6 de `AS1-AS9.db` frente a KFG

Comparación por multiconjunto de valores por quipu (la DB no tiene nombres de cuerda, así que no se puede alinear cuerda a cuerda):

| quipu | cuerdas DB/KFG | suma DB | suma KFG | diferencia | clase | lectura |
|---|---|---:|---:|---:|---|---|
| AS004 | 22/22 | 4.637 | 4.736 | −99 | (b) | una sola diferencia: DB 2 vs KFG 101 (p14). El nudo E de la DB tiene `knot_value_type=100`, pero `TOTAL_VALUE=1`; la DB suma 2 y debería sumar 101. La notación KFG `100E` (100 nudos) es un error de conteo; el valor 101 es correcto. |
| AS005 | 59/59 | 193 | 179 | +14 | (d) | 4 cuerdas: DB 5,6,7,20 vs KFG 3,4,8,9. Sin nombres no se puede alinear; diferencias pequeñas, compatibles con uno o dos nudos mal registrados. Se mantiene KFG. |
| AS006 | 92/92 | 1.468 | 1.604 | −136 | (b) | 3 cuerdas: DB 2,14,46 vs KFG 6,52,140. La DB parte un nudo largo de 9 vueltas en dos racimos (40+3+3 donde KFG tiene 40+9+3). Se mantiene KFG; confianza baja. |
| AS007 | 171/171 | 2.875 | 2.512 | +363 | (d) | 13 cuerdas con un solo nudo simple: DB 10, KFG 1. Sin la posición física no se sabe si el nudo está en decenas o unidades. Quedan además 6 cuerdas sin explicar (246). Se mantiene KFG. |
| AS008 | 249/248 | 88.084 | 70.026 | +18.058 | (c) | Una cuerda de la DB (ordinal 225) vale **17.612** (10.000+7.000+600+10+2) y no existe en KFG: explica el 97,5% de la diferencia. Es una cuerda omitida, no un error de valor. Añadirla lleva KFG a 87.638; quedan 446 (6 cuerdas con corrimiento de decena: 10→1, 50→5, 380→38, 114→117, 14→12, 50→5). |
| AS009 | 33/33 | 476 | 467 | +9 | (d) | Una sola diferencia: DB 10 vs KFG 1 (p25, `1S(18.0)`). Ambigua por la posición; se mantiene KFG. |

**Resultado negativo:** de las 6, solo AS008 tiene una causa clara y cuantificable (cuerda ausente). Las otras cinco son diferencias pequeñas y, sin nombres de cuerda en la DB, **no se pueden resolver de forma fiable**; no se propone corregir KFG.

### 3.5 KH0632

Confirmado: **no hay datos**. La carpeta `KH0631_0632/` contiene solo archivos de SH001 (`SH001.xlsx`, `SH001 Description 2023.docx`, dos jpg). No hay SH002 ni xlsx, ni fila en `khipu.db` (`OKR_NUM='KH0632'` → 0 filas; `INVESTIGATOR_NUM LIKE '%SH002%'` → 0), ni registro en KFG. Solo existe el número en la lista OKR. **Bien apoyado** (ausencia verificada en las tres fuentes).

## 4. Controles y resultados negativos

- **Control de conteo (independiente)**: KH0674 438 colgantes = suma de los 41 rangos de la portada; KH0675 203 = conteo de los 10 grupos; KH0676 65 = "group of 65 cords". Los tres cierran. Es la mejor evidencia de que la transcripción no perdió cuerdas.
- **Control de regla**: en KH0674/675 los valores escritos a mano coinciden con la regla posicional en todas las cuerdas que se pudieron leer (p. ej. KH0675 183, 185, 188, 189, 197, 201; KH0674 210, 337). En KH0676 no hay valores escritos; la elección se apoya en la nota de la hoja y en la calibración contra el corpus.
- **Resultado negativo 1**: los totales de los grupos de KH0674 (p040–p043) no reconcilian con la suma de las cuerdas (10 grupos comprobados, solo uno a 6 unidades). No se usaron.
- **Resultado negativo 2**: 11 de las 21 "discrepancias" no existen; eran errores de parseo. El equipo 17 sobrestimó el problema.
- **Resultado negativo 3**: las 6 discrepancias AS1-AS9 no se resuelven cuerda a cuerda; solo AS008 tiene causa identificable.
- **Sin p-valor**: no hay hipótesis ni efecto; el análogo es el control determinista. Se declara explícitamente para no simular inferencia donde no la hay.

## 5. Nivel de evidencia

| afirmación | nivel |
|---|---|
| KH0674 tiene 438 colgantes y KH0675 203; KH0676 65 | **bien apoyado** (conteo y portadas) |
| KH0632 no tiene datos | **bien apoyado** (tres fuentes) |
| El número del OKR para KH0676 (80.1012 aka 2708) es erróneo; el JS01 es 36.718 | **apoyado con datos** (nota manuscrita + xlsx) |
| 11/21 discrepancias son errores de parseo | **bien apoyado** (lectura del xlsx original) |
| Las correcciones propuestas de las 10 restantes | **apoyado con datos** / **propuesto** según confianza |
| La regla de KH0676 es la aditiva de la hoja | **apoyado con datos** (nota + calibración), no bien apoyado |
| AS008 tiene una cuerda de 17.612 omitida en KFG | **apoyado con datos** |
| Las otras 5 discrepancias AS son indecidibles | **propuesto** (limitación de la DB) |
| Los totales de grupo de KH0674 miden otra cosa | **especulativo** |

## 6. Lo que necesita revisión humana (archivo y celda)

### KH0674

1. `analisis/ds/n_okr_resto/cuerdas_KH0674.csv`, filas de las cuerdas **208, 209s1, 247, 351**: la ficha escribe 12, 22, 100 y 100; el cálculo da 10, 20, 10 y 10. Hay que decidir si el nudo simple está en decenas o centenas. (Las cuatro están marcadas "dudoso" en `notas`.)
2. `transcripcion_KH0674.txt`, página **p025**, filas 208/209s1: el valor de la ficha no coincide con los nudos; revisar el trazo.
3. `transcripcion_KH0674.txt`, página **p033**: orden 336/337 y el asterisco de la cuerda 336; ¿la 336 está atada a la 337?
4. `transcripcion_KH0674.txt`, página **p008**: la cuerda 44 está insertada con flecha entre 45 y 45s1; confirmar que el orden correcto es 44, 44s1–44s3, 45, 45s1.
5. `transcripcion_KH0674.txt`, página **p039**, cuerda 433: `1S(5.0) 2S(11.5)` da 120; revisar si el segundo racimo es `2S` o `2L`.
- `cuerdas_KH0674.csv`, fila de la cuerda **188s1**: los nudos son ilegibles (`?`) y el valor queda vacío. Es la única fila sin valor de los tres quipus.
6. `png/KH0674/p040.png`–`p043.png`: los totales de grupo no reconcilian; decidir qué representan antes de usarlos.
7. **Faltan** color, largo, grosor y terminación en todas las filas de `cuerdas_KH0674.csv` (columnas `color`, `largo`, `terminacion`): están en la mitad derecha de cada página.

### KH0675

8. `transcripcion_KH0675.txt`, página **p002**, cuerda **10**: el último racimo es `6L` o `10L`; el valor escrito (17) sugiere `6L`. Confirmar.
9. `transcripcion_KH0675.txt`, página **p006**: dos cuerdas rotuladas `49s1s2`; la segunda se renumeró `49s1s1`. Confirmar cuál es cuál.
10. `transcripcion_KH0675.txt`, página **p014**: dos filas rotuladas 136 (una es 135). Confirmar.
11. `transcripcion_KH0675.txt`, página **p017**, cuerda **191**: la ficha escribe 2.084; la regla posicional da 2.804. ¿Racimo de centenas omitido o error de la ficha?
12. `cuerdas_KH0675.csv`, columna `grupo`: la cuerda 67 no está en ningún rango de la portada y el grupo 124–180 dice 52 cuerdas pero tiene 57. Confirmar la asignación.
13. **Faltan** color, largo, grosor y terminación (igual que en KH0674).

### KH0676

14. `JS01_Strauss_Harvard_Senior_Thesis.xlsx`, hoja `Pendant Detail`, **celda K3**: la nota "all single knots = 10…" es la base de la regla; confirmar que se interpreta como suma aditiva y no jerárquica.
15. `cuerdas_KH0676.csv`, columna `alt`: para las cuerdas **41, 41s2, 47, 31, 14, 7, 40, 9s1** la regla jerárquica da valores de 5–6 cifras (máximo 314.120) frente a 21–121 de la regla aditiva. Revisar si esos racimos son realmente posiciones decimales distintas.
16. `JS01_Strauss_Harvard_Senior_Thesis.xlsx`, hojas `Pendant Detail` (filas de las cuerdas **13, 23, 41s2s1, 61, 65s3s1, 65s4s1**) y `cuerdas_KH0676.csv`: tipo `SP` tratado como `S`. Confirmar qué significa `SP`.
17. `data/external/open-khipu-repository/data/okr-kh-numbers.csv`, **fila de KH0676 al abrir el CSV en hoja de cálculo (fila 677), columna `Collection Number` (F)**: dice `80.1012 aka 2708`; debe decir `36.718` (Brooklyn Museum). El mismo número está mal asignado a KH0700 (fila 701 en hoja de cálculo), que sí es Stanford.
18. `JS01_Strauss_Harvard_Senior_Thesis.xlsx`, hoja `Heading`, **celda A4**: dice 36.718, coherente con el PDF; no cambiar.

### Discrepancias

19. `analisis/17_okr_pendientes/cuerdas_extra.csv`, filas **2, 5, 7, 244, 269, 330, 375, 448, 451, 453, 478, 510, 511, 563, 567, 576, 584, 598, 638, 653, 697**: las 21 discrepancias. La clasificación y el valor propuesto están en `discrepancias_clasificadas.csv`; las que hay que mirar con lupa son **KH0631 p1** (fila 2), **KH0631 p6** (fila 7), **KH0634 p17s3** (fila 269), **KH0640 p5** (fila 478) y **KH0648 p6** (fila 584).
20. `AS1-AS9.db`, tabla `knot_cluster`, **CLUSTER_ID 1065565/1065566** (AS004, p14): el nudo E tiene `knot_value_type=100` pero `TOTAL_VALUE=1`; la agregación de la DB ignora el lugar. Revisar también `knot`, `KNOT_ID` de esas dos clusters.
21. `AS1-AS9.db`, **AS008, CORD_ORDINAL 225** (CORD_ID de la cuerda con clusters 10.000/7.000/600/10/2): no está en KFG. Confirmar si es una cuerda real o un artefacto de la DB.
22. `AS1-AS9.db`, **AS005, AS006, AS007, AS009**: diferencias pequeñas sin nombres de cuerda; no se pueden resolver sin la tabla de correspondencias DB↔KFG.

### KH0632

23. `KH0631_0632/`: no hay SH002. Confirmar con el museo (University of St Andrews, SA005) o dejarlo como "sin datos".

## 7. Archivos entregados

| archivo | contenido |
|---|---|
| `cuerdas_KH0674.csv` | 624 filas, esquema de `cuerdas.csv` |
| `cuerdas_KH0675.csv` | 285 filas |
| `cuerdas_KH0676.csv` | 138 filas (`valor` = regla de la hoja; `alt` = jerárquica) |
| `cuerdas_nuevas.csv` | las 1.047 filas de los tres quipus, con columna `fuente` |
| `discrepancias_clasificadas.csv` | 21 + 6 filas, clase, valor propuesto, confianza, evidencia |
| `transcripcion_KH0674*.txt`, `transcripcion_KH0675.txt` | transcripción cruda con dudas |
| `render_paginas.py`, `ocr_paginas.py`, `preparar_imagenes.py`, `orientar.py`, `contactos.py` | render, OCR y orientación |
| `convertir_transcripcion.py`, `convertir_kh0676.py`, `clasificar_discrepancias.py`, `unir_nuevas.py` | conversión y clasificación |
| `png/`, `ocr/` | 300 dpi, miniaturas, hojas de contacto y texto OCR |

## 8. Para el coordinador

- **KH0674 y KH0675 están transcritos**: 438 y 203 colgantes, 624 y 285 cuerdas, sumas 11.688 y 53.235. Los conteos cierran con las portadas (41 grupos = 438; 10 grupos = 203), lo que es la mejor prueba de que no se perdió ninguna cuerda. Nivel: bien apoyado.
- **KH0676 está convertido**: 65 colgantes + 73 subsidiarias = 138 cuerdas, suma 4.769. La regla que declara la propia hoja es aditiva (simples = 10, largos = vueltas, ochos = 1); la variante jerárquica daría 670.004 y un máximo de 314.120, fuera de escala. Se guardan ambas (`valor` y `alt`). Nivel: apoyado con datos, no bien apoyado.
- **El número del OKR para KH0676 está mal**: el PDF manuscrito y el xlsx dicen Brooklyn Museum **36.718**; el OKR le puso `80.1012 aka 2708`, que es el de KH0700 (Stanford). Hay que corregir la fila de KH0676 en `okr-kh-numbers.csv`. Nivel: apoyado con datos.
- **De las 21 discrepancias de `cuerdas_extra.csv`, 11 no existen**: son errores del parser del equipo 17 (coma decimal, `8L,15.0,S,8`, etc.). Al releer el xlsx, la suma coincide con el valor. Es el hallazgo más importante de esta ronda y obliga a desconfiar de la columna `VALIDACION` que dejó el equipo 17.
- Las 10 restantes sí son de la fuente: 5 son errores de aportación (el valor de la hoja es correcto) y 5 son nudos mal registrados (tipo o posición). Ninguna exige declarar la cuerda rota. Nivel: apoyado con datos / propuesto según el caso.
- **De las 6 diferencias AS1-AS9, solo AS008 tiene causa clara**: una cuerda de 17.612 ausente en KFG explica el 97,5% de la diferencia. Las otras cinco son pequeñas y, sin nombres de cuerda en la DB, **no se pueden resolver**; no conviene tocar KFG.
- **KH0632 no tiene datos**: ni archivo, ni fila en `khipu.db`, ni registro KFG. Solo existe el número en la lista OKR.
- **Limitación grande**: de KH0674/675 solo se transcribieron las columnas de estructura y valor; color, largo, grosor y terminación están en las mismas páginas y quedan para una segunda pasada. No se deben usar esos CSV para análisis de color o longitud todavía.
- **Para la siguiente ronda**: (1) revisar los 24 puntos de la lista de la sección 6; (2) decidir la regla de KH0676 con una muestra física o con la versión KFG en línea; (3) buscar la tabla de correspondencias DB↔KFG para AS1-AS9; (4) inventariar los 41 "top cords" circulados de KH0674, que la propia ficha sugiere que son cuerdas resumen.
