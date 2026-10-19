# 24_color_formato: ¿qué HACE el color en los quipus?

**Carpeta:** `analisis/24_color_formato/` · **Semilla:** 20261018 · **Fecha:** 18-10-2026
**Diseño congelado:** `diseno.md`, escrito antes de los resultados. Las desviaciones están en §7.
**Datos:**
- KFG: `analisis/datos/cuerdas.csv`, con el color normalizado mediante `re.sub(r'\([^)]*\)','',s)`.
- OKR en solo lectura (`mode=ro`): `cord`, `ascher_cord_color`, `khipu_main`.
- Enlaces ya verificados: `13_sistema_incahuasi/grafo_cuerdas.csv`, `ur270_ur278.csv`, `14_copias/filas_alineadas.csv` y las sumas de Puruchuco de `ds/n_puruchuco_pacha`.

---

## 0. Respuesta corta

El color de un quipu funciona como el **formato de una hoja de cálculo**, no como un diccionario. No marca qué cosa se cuenta. Marca **qué papel cumple la cuerda dentro del documento**: a qué columna o rubro pertenece, si separa secciones (marcadoras) o si abre el grupo (la primera cuerda, a menudo blanca).

La prueba nueva y más clara es el seguimiento de un mismo número de un quipu a otro:

- **Si el número conserva su papel, conserva el color.**
  - Copias: coincide la etiqueta en el 47 % de los casos, frente a un 25 % por azar.
  - Puruchuco, columna → misma columna en el nivel siguiente: 61 % frente a 18 % por azar (p = 0,0001).
- **Si cambia de papel, adopta el color del nuevo papel.**
  - En Incahuasi, las partes y las filas (AB, NB o W) pasan a ser cabeceras de registro en otro quipu.
  - Allí el destino es **W en el 75 % de los casos, sea cual sea el color de la fuente**.
  - El color de la fuente no predice el del destino: M = 0,50 frente a 0,475 del nulo (p = 0,33); NMI = 0,05 frente a 0,09 (p = 0,97).

El color, por tanto, **viaja con el rubro, no con el número**. Esto es compatible con lo que dicen los cronistas, siempre que se lea así: «el color identifica el rubro *dentro* del documento o del archivo». Es incompatible con un léxico universal («amarillo = oro» en todos los quipus). Las fuentes etnográficas (Mackey, Núñez del Prado, Salomon) y Ascher ya lo decían.

---

## 1. P1: ¿el color viaja con el dato?

`p1_viaja.py` → `p1_enlaces.csv`, `p1_resumen.csv`, `p1_tablas.txt`.

**Medidas:**
- M: proporción de enlaces en los que el color del destino es igual al de alguna fuente.
- N1: nulo que permuta los colores de destino entre los enlaces del mismo quipu de destino (rompe el emparejamiento) y conserva la composición; 9 999 réplicas.
- N2: nulo que toma un color al azar de la paleta del quipu de destino, en el mismo nivel.

| Familia de enlaces | n | M | M nulo N1 | p (N1) | NMI | NMI nulo | p (NMI) | M nulo N2 | % destinos W |
|---|---|---|---|---|---|---|---|---|---|
| Copias, mismo registrador (réplica de 14) | 273 | **0,469** | 0,249 | **0,0001** | 0,596 | 0,354 | 0,0001 | 0,257 | 24 % |
| Copias, otro registrador | 520 | 0,252 | 0,199 | 0,0001 | 0,561 | 0,310 | 0,0001 | 0,157 | 17 % |
| **Incahuasi, sumas entre quipus (todas)** | 60 | 0,500 | 0,475 | **0,33** | 0,047 | 0,088 | **0,97** | 0,218 | **75 %** |
| – partes A+B → cabecera (UR266/269/275) | 19 | 0,684 | 0,642 | 0,20 | 0,147 | 0,093 | 0,31 | 0,276 | 63 % |
| – fila de UR278 → cabecera de UR266/275/269 | 30 | 0,300 | 0,267 | 0,39 | 0,132 | 0,129 | 0,49 | 0,136 | **80 %** |
| – UR270 P+S → cabecera | 5 | 0,80 | 0,80 | 1,0 | 0 | 0 | 1,0 | 0,381 | 80 % |
| Incahuasi, UR270 (W + subsidiaria NB) → celda de UR278 | 39 | 0,718 | 0,771 | 1,0 | 0,022 | 0,044 | 1,0 | 0,601 | 74 % |
| **Puruchuco, UR068 → UR067/UR066 (columna → columna)** | 31 | **0,613** | 0,181 | **0,0001** | 0,742 | 0,310 | 0,0001 | 0,173 | 32 % |
| – UR068 → UR067 | 17 | 0,706 | 0,202 | 0,0001 | 0,763 | 0,427 | 0,0001 | 0,206 | 29 % |
| – UR068 → UR066 | 14 | 0,500 | 0,160 | 0,0001 | 0,900 | 0,423 | 0,0001 | 0,140 | 36 % |

**Lectura de las tablas cruzadas** (`p1_tablas.txt`):
- **Incahuasi, total de fila → cabecera.** Las filas de UR278 son AB (15), NB (8) o W (7). Sus totales aparecen en UR266, UR275 o UR269 como **W 24 veces de 30**: AB → W en 11 de 15 y NB → W en 7 de 8. Es un recoloreado sistemático hacia el color de cabecera del documento de destino, que es justo la predicción «formato». Lo mismo pasa con las celdas de UR278: suman un colgante W y una subsidiaria NB de UR270, pero toman el color de **fila** de UR278 (W o AB), no el de la parte.
- **Puruchuco, columnas.** Las columnas W de las tres secciones de UR068 dan W en UR067 y UR066 en 10 de 10 casos. AB da AB/MB en 7 de 7, GG da GG/KB y W:KB da W:KB/W:AB. El ritmo de columnas de cuatro colores se conserva de un nivel a otro.
  - Circularidad: las columnas de UR068 se definieron por color, pero el color del destino no intervino.
  - Las etiquetas no son idénticas (GG en UR067 frente a KB en UR066, el mismo dato en copias del mismo nivel). La **partición** se conserva mejor que la **etiqueta**: NMI de 0,90 con M de solo 0,50.
- **Copias** (réplica de 14_copias): misma conclusión. La partición se conserva (NMI 0,56–0,60 frente a 0,31–0,35) y la etiqueta coincide solo a medias.

**Veredicto P1:**
- El color **no** es una propiedad del número que lo acompañe cuando pasa a otro papel (Incahuasi, Holm 0,99). Sí es una propiedad del **rubro o columna**, que se conserva cuando el documento de destino tiene el mismo formato (Puruchuco, Holm 0,0012).
- Coincide con la expectativa escrita en `diseno.md`. **Nivel: apoyado con datos.**
- Limitaciones:
  - solo hay dos archivos con sumas entre quipus verificadas;
  - los enlaces de Incahuasi no son independientes (60 enlaces, 5 quipus de destino);
  - en Puruchuco hay 31 enlaces en 2 destinos que son copias entre sí.

---

## 2. P2: ¿el color marca la función de la cuerda?

`p2_funcion.py`, `p2b_sin_incahuasi.py` → `p2_global.csv`, `p2_quipu.csv`, `p2_preferido.csv`, `p2b_*.csv`.

**Medidas:**
- D es la distinción de una cuerda frente a las demás de su grupo: 1 menos la fracción de esas cuerdas que tienen su mismo color.
- NG: nulo que toma una cuerda no tipo del mismo grupo.
- NP: nulo que toma una cuerda no tipo de otro grupo en la misma posición relativa (primera, interior o última).

| Tipo | Instancias (quipus) | D obs. | D nulo NG | p NG | D nulo NP | p NP | Quipus con q < 0,05 | Color modal entre quipus |
|---|---|---|---|---|---|---|---|---|
| T1 total de grupo (valor = suma del resto) | 168 (79) | 0,543 | 0,475 | **0,0001** | 0,504 | 0,037 (Holm 0,15) | 2 de 9 (UR269, UR275) | W en 4 de 9 (nulo 2,4; p = 0,029, Holm 0,14) |
| T2 total de subsidiarias | 62 (31) | 0,516 | 0,531 | 0,77 | – | – | 0 de 4 | – |
| T3 cabecera = máximo del grupo | 1 454 (334) | 0,574 | 0,558 | **0,0001** | 0,540 | 0,0001 | 28 de 133 (10 de Incahuasi) | W en 64 de 133 (nulo 43,8; p = 0,0005) |
| T4 cuerda en blanco | 4 071 (336) | 0,580 | 0,584 | **0,97** | – | – | 22 de 198 | W en 45 de 198 (nulo 52; p = 0,97) |
| T5 marcadora (OKR «M») | 331 (22) | **0,756** | 0,162 | **0,0001** | – | – | 4 de 7 | sin color común (W, MB, AB:MB:GG…) |
| T6 cuerda superior (OKR «T») | 87 (10) | 0,640 | 0,481 | 0,0001 | – | – | 8 de 9 | AB en 5 de 9 (p_top = 0,12) |
| T7 subsidiaria del mismo color que su padre | 13 737 (434) | 19,7 % iguales | 16,7 % | **0,0001** (más iguales) | – | – | – | – |

**Lectura:**

1. **Marcadoras (T5): el uso más claro.** Son de un color distinto al de sus vecinas en el 76 % de los casos, frente al 16 % esperado. Pero **no hay un color de marcadora común** entre quipus: 7 quipus dan 7 colores modales distintos. Es formato puro, con clave local. Casi todo viene de AS069 (244 marcadoras).
2. **Cuerdas superiores (T6): también se distinguen** (0,64 frente a 0,48; 8 de 9 quipus). Hay una tendencia a AB que no es significativa.
3. **Totales y cabeceras (T1, T3): se distinguen de su grupo, pero poco.** El efecto medio es de +0,02 a +0,07 en D. Controlando la posición (NP), el total ya no pasa Holm (0,15). Además:
   - El W de la cabecera es en realidad **W de la primera cuerda**, no del máximo. Las 64 cabeceras modales W de 133 quipus superan el nulo, también sin Incahuasi (51 de 110; p = 0,0005). Pero dentro del mismo quipu, la primera cuerda que no es el máximo es igual de blanca: 19 quipus a favor y 24 en contra, Wilcoxon p = 0,75 (`p2b_control_posicion.csv`).
   - El color blanco marca **la primera posición del grupo**, no la cuerda grande. Es lo mismo que dijeron a Mackey los quipucamayos modernos: el color señala la cuerda «primera» o «izquierda» (cita en §5).
   - En Incahuasi el total sí es W de forma muy marcada (UR269: W en el 93 % de 15; UR275: 80 % de 10), pero es una convención de archivo.
4. **Cuerdas en blanco (T4): no tienen color propio** (0,580 frente a 0,584). Hay 22 quipus locales con q < 0,05. Lo «vacío» se marca por posición o ausencia, no con un color.
5. **Subsidiarias (T7): repiten el color del padre algo más que el azar** (19,7 % frente a 16,7 %). El efecto es pequeño: el 80 % de las subsidiarias tienen otro color. La subsidiaria **no hereda** el color; casi siempre se distingue de su padre, lo que encaja con una sub-rúbrica.
6. **Totales de subsidiarias (T2): sin señal.**

**Veredicto P2:**
- El color marca de forma robusta los **separadores** (marcadoras, superiores) y, débilmente, el **inicio del grupo**.
- No marca el total como tal una vez controlada la posición, ni las cuerdas en blanco.
- Entre quipus solo se comparte una tendencia: **primera cuerda blanca**, que es posicional.
- **Nivel:** marcadoras, demostrado (Holm 0,0012); primera cuerda W, apoyado con datos; total con color propio, no se sostiene fuera de Incahuasi.

---

## 3. P3: efecto del transcriptor

`p3_transcriptor.py` → `p3_quipu.csv`, `p3_pruebas.csv`, `p3_vocabulario.csv`, `p3_mismo_objeto.csv`, `p3_nmi_grupo.csv`.

### Tamaño del alfabeto

Nº de colores distintos en 40 cuerdas tomadas al azar (rarefacción), por registrador:

| Registrador | Quipus | Alfabeto rarefactado (mediana) | Bases (mediana) | Códigos totales | Códigos exclusivos |
|---|---|---|---|---|---|
| AS (Ascher, incl. UR1xxx) | 86 | **5,99** | 3,96 | 406 | 259 |
| UR (Urton y equipo) | 182 | 9,72 | 5,33 | 735 | 517 |
| HP | 22 | 8,92 | 4,65 | 136 | 58 |
| QU | 18 | 9,54 | 5,94 | 108 | 59 |
| KH | 11 | 10,02 | 6,15 | 130 | 46 |
| MM | 14 | 12,13 | 6,27 | 126 | 47 |
| JC (Clindaniel) | 7 | 14,90 | 7,28 | 154 | 86 |

- Kruskal-Wallis con permutación: H = 41,1, **p = 0,0001** (Holm 0,0012). Con bases: H = 45,0, p = 0,0001.
- **Ascher distingue unos 6 colores por cada 40 cuerdas; Urton, casi 10; Clindaniel, 15.**
- Los códigos exclusivos de un registrador cubren el 5–13 % de sus cuerdas.
- Dentro del registrador UR, la persona que introdujo los datos (`CREATED_BY`) también se asocia con el alfabeto (H = 27,9, p = 0,0002; cbrezine 6,0 frente a gurton 10,7 y chandra 14,7). Pero en la única región con dos personas comparables (Chachapoyas, cbrezine frente a katie) la diferencia desaparece (p = 0,60).
- **Confusión no separable:** registrador, colección, sitio y época de transcripción van juntos. No hubo ninguna región con ≥ 2 registradores de ≥ 4 quipus para el control previsto (desviación 5).

### Mismo objeto leído dos veces

| Par | Registradores | n | Etiqueta igual | NMI (nulo) |
|---|---|---|---|---|
| KH0033 / UR044 | KH / UR | 23 | 91 % | 1,00 (0,12) |
| **UR1107 / UR237** | **AS / UR** | 23 | **0 %** | 0,49 (0,31), p = 0,003 |
| AS125 / UR247 | AS / UR | 15 | 100 % (todo W) | – |

En UR1107/UR237 lo que Ascher llama YB o LB, Urton lo llama AB; lo que Ascher llama BS o LB, Urton lo llama MB. **La etiqueta depende de quién mira; la partición se conserva en parte.**

### ¿Cambian las conclusiones dentro de un solo registrador?

- **Color ~ grupo** (NMI sobre el p95 del nulo): AS 49 de 108, UR 85 de 194, QU 12 de 15, HP 12 de 32. El color como marca de grupo se sostiene dentro de cada registrador.
- **Marcadoras:** se sostienen en AS (0,75 frente a 0,14) y en UR (0,92 frente a 0,64).
- **Totales y cabeceras:** el resultado **cambia** según el registrador.
  - En UR, T1 (0,55 frente a 0,47; p = 0,0001) y T3 (0,63 frente a 0,57; p = 0,0001) se distinguen.
  - En AS, T1 no se distingue (p = 0,24) y T3 se distingue *menos* que una cuerda al azar del grupo (0,43 frente a 0,47).
  - Parte de la «marca de total» depende de Incahuasi y del modo de transcribir de UR.
- **Subsidiaria igual al padre:** se repite igual en AS y en UR.

**Veredicto P3:**
- Las **etiquetas** (y con ellas cualquier «léxico») dependen mucho del transcriptor. Las **particiones** (color = grupo, marcadora distinta) no dependen de él.
- Cualquier comparación de etiquetas entre quipus de distintos registradores (p. ej. «W = principal» en todo el corpus) está contaminada por este efecto.
- **Nivel:** demostrado para el tamaño del alfabeto y para el par UR1107/UR237; no se puede separar de la colección.

---

## 4. P4: los códigos locales fuertes

`p4_locales.py` → `p4_medidas.csv`, `p4_colores.csv`.

Medida: η² del color sobre log1p(valor) en las cuerdas presentes de nivel 0, con colores de ≥ 3 cuerdas y 4 999 permutaciones. Variantes: (a) crudo; (b) colapsado a la base; (c) residual de grupo (permutación dentro del grupo); (d) residual de posición; (e) sin totales ni máximos.

| Quipu | n | Colores | % compuesto | (a) | (b) base | (c) grupo | (d) posición | (e) sin total/máx. | V color~grupo | V color~torsión | Lectura |
|---|---|---|---|---|---|---|---|---|---|---|---|
| UR123 | 44 | 5 | 70 % | 0,90 | 0,10 | 0,16 | 0,86 | 0,92 | **0,90** | 0 | Cada color ocupa su propio grupo (1–2 grupos por color). Es **marca de grupo**, con variantes moteadas (W:AB, W:GG, AB:GG) como distintivo. |
| HP017 | 73 | 7 | 19 % | 0,55 | 0,19 | 0,49 | 0,36 | 0,47 | 0,43 | 0,43 | **Columna:** W siempre al final (posición relativa 1,00; máximo del grupo en el 50 %), W:MB al principio (máximo en el 100 %), W:GG cerca del principio con valores bajos. El código está en las variantes de W. |
| QU013 | 134 | 7 | 14 % | 0,42 | 0,26 | 0,38 | 0,52 | 0,61 | 0,51 | 0 | **Es el mejor candidato a categoría local.** YB (mediana 12) frente a BS (3), GG y PG (2), repartidos en 24 grupos. Resiste el control de grupo, de posición y de totales. |
| UR208 | 95 | 12 | 38 % | 0,37 | 0,11 (p = 0,19) | 0,46 | 0,30 | 0,36 | 0,50 | 0 | W es siempre la primera cuerda (15 de 15 grupos); AB es el máximo del grupo en el 80 %. Hay columnas con variantes AB/AB:GG. **Formato con variantes moteadas.** |
| AS128 | 130 | 10 | 27 % | 0,73 | 0,28 | 0,28 | 0,69 | 0,84 | **0,86** | 0 | Cada color ocupa 1–3 grupos; DB es un grupo de valores grandes (mediana 613). Es **marca de grupo**. |
| UR231 | 223 | 12 | 13 % | 0,71 | 0,54 | **0,00** (p = 1) | 0,68 | 0,69 | **1,00** | 0,24 | **Grupo puro:** cada grupo es de un solo color y los grupos difieren en magnitud. Dentro del grupo el color no informa nada. |
| UR1152 | 63 | 12 | 62 % | 0,65 | 0,42 | 0,53 | 0,55 | 0,69 | 0,73 | 0 | La familia B (B, B-BB, B-YG, mediana 197–385) frente a MB y W (5–10). **Posible categoría local**, pero el 62 % de las cuerdas son compuestas. |
| UR1140 | 178 | 4 | 22 % | 0,03 (p = 0,22) | 0 | 0,03 | 0,02 | 0,01 | 0,38 | 0 | **No hay código:** B, B:BB y B:G tienen el mismo valor. La señal del «swap» de n_color_posicion no se reproduce como asociación con la magnitud. |

Holm sobre los 8 p de (e): todos < 0,03 salvo UR1140 (0,62).

**Clasificación con la regla congelada y su corrección:**
- La regla de `diseno.md` etiqueta «ARTEFACTO compuesto/ply» a UR123, HP017, UR208, AS128 y UR1140, porque al colapsar los compuestos a su base se pierde más de la mitad de η². Pero la torsión es constante en todos (V color~torsión = 0; todo S, o U en AS128).
- Por tanto **no es un artefacto de torsión ni de ply.** Es que **el código distingue el color liso del moteado o jaspeado** (W frente a W:AB, B frente a B-BB).
- Si esa distinción la hizo el quipucamayoc o el transcriptor no se puede decidir sin imágenes. P3 muestra que los transcriptores difieren mucho precisamente en cuánto detallan los compuestos.

**Resumen P4:**
- De los 8 quipus, **3 son marca de grupo** (UR123, AS128, UR231), **2 son columna o posición con variantes moteadas** (HP017, UR208) y **1 no tiene código** (UR1140).
- **Solo 2 son candidatos a categoría local** que no se reduce a grupo, posición ni total (QU013 y UR1152), y UR1152 depende de compuestos.
- **Nivel:** apoyado con datos para la descripción; especulativo para cualquier significado.

---

## 5. P5: lo que dicen las fuentes

Búsqueda en `analisis/fuentes_txt/`, con las citas verificadas línea a línea.

### Las afirmaciones de léxico universal (tipo B) solo están en los cronistas, y como ejemplos

- **Garcilaso**, citado en Pärssinen 2004 (`Parssinen2004_TextosAndinos_parcial.txt:280`): «Por los colores sacaban lo que se contenia en aquel tal hilo, como el oro por el amarillo y la plata por el blanco, y por el colorado la gente de guerra. Las cosas que no tenfan colores iban puestas por su orden…».
- **Calancha**, en NarrativeThreads2002 (`NarrativeThreads2002.txt:1454–1455`, vía Assadourian): negro = tiempo, carmesí = el Inca, y «each province had a different mixture of colors». Assadourian advierte que Calancha «composed for his demonstration» un ejemplo; no describe un quipu concreto.
- **Acosta** (`NarrativeThreads2002.txt:1445`): habla de tantas diferencias de color que «derived innumerable significations». No da una clave fija.
- **Murúa** no aparece en los textos disponibles con nada sobre el color.

### Las fuentes que examinaron quipus reales o hablaron con sus usuarios niegan el léxico universal

- **Day 1967** (`Day1967_QuipusWitchesKnots.txt:150`): «The symbolic color schemes mentioned by the early chroniclers (white for silver, yellow for gold, red for soldiers, and so on) do not seem to have been used in any extant quipus.»
- **Mackey 2002**, quipus modernos (`NarrativeThreads2002.txt:4077`): «To the majority of modern khipu makers, color did not appear to represent the category being counted. Rather, color was more often used to signal the 'first,' or 'left,' cord… this ranking varied idiosyncratically». Y en la línea 4092: «cord color is rarely used to denote the categories that are counted».
  - Encaja **exactamente** con P2: el blanco marca la primera cuerda, no la grande.
- **Mackey 1970** (`Mackey1970_KnotRecords.txt:347`): «It would appear that color of the pendent cords was totally up to the user».
- **Núñez del Prado 1950**, citado por Salas (`InterpretacionLinguisticaQuipus.txt:6647`): «el uso del color no tiene una significación especial… en la mayor parte de los casos el uso del color depende del capricho imaginativo del operador».
  - Menciona como excepción convenciones «más o menos conocidas» (blanco = cuentas generales, negro = pérdidas).
  - Salas (línea 6643) reúne cinco significados distintos del hilo negro según la fuente: plata, tiempo, animales machos, pérdidas y asesinar.
- **Mackey 1990**, citada por Salas (`InterpretacionLinguisticaQuipus.txt:2305`): «Todos dijeron que el orden de las colgantes y no su color era lo que servía como instrumento mnemotécnico».
- **Ascher 1983**, citada por Salas (`:2299–2303`): «una de las más importantes técnicas de categorización cruzada es el uso del color y la posición redundantemente». Es la NMI color~posición de n_color_posicion, enunciada hace 40 años.

### Las fuentes que sí dicen «el color identifica el rubro» lo dicen dentro de un registro o comunidad (tipo A)

- **Salomon 2004, Tupicocha.** «the color bands… correspond to functional domains for which the ayllu had responsibility» (`Salomon2004_CordKeepers.txt:2505`). Pero también: «Consultants did not agree on what colors of band correspond to each agenda» (2514) y «no two quipocamayos obviously resemble each other in color array of bands» (2539).
- **Hyland 2016**, sobre Nery Javier (`Hyland2016_Anchucaya.txt:165`): cada banda de color de *ese* quipu de Satafasca tenía un tema, y el quipu era «for the ayllu of Satafasca only».
- **Mackey 2002**, Sr. Quispe (`NarrativeThreads2002.txt:3938`): marrón = habas y blanco = quinua en *su* quipu nº 7. En el nº 8, todo blanco, usó otro recurso.
- **Urton 2017** (`:6270`): AB = Hanan y MB = Hurin *en las cuerdas de Atarco*.

### Respuesta a la pregunta

- **Ninguna fuente basada en quipus reales dice que el mismo color signifique lo mismo en todos los quipus.** Solo lo dicen Garcilaso y Calancha, con ejemplos que parecen ilustrativos, y una preimpresión de 2026 (Sivan), cuya «traducción» de UR193 no superó el azar (`23_sivan_ur193`).
- Lo que sí dicen varias fuentes es que **dentro de un quipu o de un archivo, cada rubro tiene su color**. Es la lectura «color = formato de columna» que muestran P1 (Puruchuco), P2 (marcadoras) y n_color_posicion (NMI 0,505).
- La frase de Garcilaso tiene dos mitades:
  - «por los colores sacaban lo que se contenía en aquel hilo» es compatible con nuestros datos si el color dice *qué rubro* es esta cuerda en este documento;
  - «el oro por el amarillo» como clave fija entre quipus es lo que los datos y las fuentes etnográficas contradicen.
  - Su segunda frase, «las cosas que no tenían colores iban puestas por su orden», es literalmente la redundancia color/posición.
- **Los cronistas no se equivocaban en que el color fuera clave; se equivocaban, o simplificaban, en que la clave fuera universal.** Para leer un quipu hacía falta su clave local, es decir, el quipucamayoc.

---

## 6. Pruebas principales con Holm (familia congelada de 12; `holm.csv`)

| Prueba | p | Holm |
|---|---|---|
| P1 Puruchuco: M frente a N1 | 0,0001 | **0,0012** |
| P1 copias del mismo registrador: M frente a N1 | 0,0001 | **0,0012** |
| P2 T1 total: D frente a NG | 0,0001 | **0,0012** |
| P2 T3 cabecera-máximo: D frente a NG | 0,0001 | **0,0012** |
| P2 T5 marcadora: D frente a NG | 0,0001 | **0,0012** |
| P2 T7 subsidiaria = padre | 0,0001 | **0,0012** |
| P3 alfabeto ~ registrador | 0,0001 | **0,0012** |
| P2 preferencia W de T1 entre quipus | 0,029 | 0,14 |
| P2 T1 total: D frente a NP (posición) | 0,037 | 0,15 |
| P1 Incahuasi sumas: M frente a N1 | 0,33 | 0,99 |
| P1 Incahuasi sumas: NMI frente a N1 | 0,97 | 1,0 |
| P2 T4 en blanco: D frente a NG | 0,97 | 1,0 |

## 7. Desviaciones del diseño (declaradas)

1. **Estadístico D.** El diseño decía «≠ color modal». Por los empates de la moda usé como primario D = 1 − (fracción de las otras cuerdas con el mismo color) y guardo D_moda. Los dos dan la misma dirección (`p2_global.csv`).
2. **T1 estricto.** Valor = suma exacta del resto, con ≥ 2 sumandos. Da solo 168 instancias; el equipo rojo contó unos 3 600 «totales» con otra definición. Por eso la prueba de preferencia de T1 tiene 9 quipus y poca potencia.
3. **P4.** La etiqueta congelada «ARTEFACTO compuesto/ply» se aplicó, pero la reinterpreto porque la torsión es constante (§4).
4. **P2b es post hoc.** Incluye la exclusión de Incahuasi y el control de posición de la preferencia W. Se añadió tras ver que 10 de los 28 quipus con T3 significativo eran de Incahuasi.
5. **P3.** El control dentro de la región previsto no fue posible (ninguna región con ≥ 2 registradores de ≥ 4 quipus con ≥ 40 cuerdas). Solo se hizo para la captura en Chachapoyas.
6. **UR066.** Se alineó por el mejor desplazamiento de valores (12). Los colores no intervinieron en esa elección.
7. **Instancias de T5.** El 74 % viene de AS069; las cifras por quipu (4 de 7) son más representativas que el total.

## 8. Limitaciones

- Las sumas entre quipus verificadas existen en **dos archivos** (Incahuasi y Puruchuco). La generalización «el color viaja con el rubro, no con el número» descansa en ellos más las copias.
- Las etiquetas de color dependen del transcriptor (P3). Cualquier comparación de etiquetas entre quipus mezcla convención antigua y convención de quien transcribió. Solo las particiones (NMI) son comparables.
- La distinción liso/moteado, que sostiene la mitad de los códigos locales, no se puede validar sin imágenes. No se usaron fotografías.
- T4 (en blanco) no distingue entre cuerdas sin nudos a propósito y nudos perdidos. Excluí las terminaciones rotas, pero no los desgastes.
- El universo de P2 son los quipus con grupos. Los quipus sin estructura de grupos quedan fuera.

---

## Para el coordinador

- **El color viaja con el rubro, no con el número (apoyado con datos; dos archivos).**
  - En Puruchuco, una columna conserva su color al pasar de UR068 a UR067/UR066: 61 % frente a 18 % del nulo; NMI 0,74 frente a 0,31; Holm 0,0012.
  - En Incahuasi, cuando un número cambia de papel (partes o filas → cabecera de registro), el destino es W en el 75 % de los casos, sea cual sea la fuente. M = 0,50 frente a 0,475 (p = 0,33); NMI 0,05 frente a 0,09 (Holm 0,99). Las filas AB y NB de UR278 pasan a W en 18 de 23.
- **Copias (réplica de 14):** se conserva la etiqueta en el 47 % frente al 25 % y la partición con NMI 0,60 frente a 0,35. Con otro registrador, la etiqueta casi no coincide (25 % frente a 20 %), pero la partición sí (0,56 frente a 0,31).
- **Marcadoras (demostrado):** se distinguen de sus vecinas en el 76 % frente al 16 % (Holm 0,0012), pero cada quipu usa un color distinto para ellas. Formato con clave local. Las cuerdas superiores, igual (0,64 frente a 0,48; 8 de 9 quipus).
- **«Blanco = principal» es en realidad «blanco = primera cuerda» (apoyado con datos).**
  - La cabecera-máximo es modalmente W en 64 de 133 quipus (nulo 43,8; p = 0,0005; también sin Incahuasi, 51 de 110).
  - Dentro del quipu, la primera cuerda que no es máximo es igual de blanca (19 a favor, 24 en contra; p = 0,75).
  - Coincide literalmente con Mackey 2002: el color señala la cuerda «primera» o «izquierda». El total controlado por posición ya no pasa Holm (0,15).
- **Las cuerdas en blanco no tienen color propio** (0,580 frente a 0,584; p = 0,97). **Las subsidiarias casi nunca heredan el color del padre:** 19,7 % iguales frente a 16,7 % del azar, así que el 80 % se distingue.
- **El efecto del transcriptor es grande (demostrado, pero confundido con la colección).**
  - Alfabeto en 40 cuerdas: Ascher 6,0, Urton 9,7, Clindaniel 14,9 (p = 0,0001).
  - En el mismo objeto, UR1107 (Ascher) y UR237 (Urton) coinciden en 0 de 23 etiquetas: YB/LB de Ascher equivale a AB de Urton.
  - La marca de total y de cabecera se ve en UR pero no en AS. La partición color~grupo sí se mantiene en todos.
- **Los 8 códigos locales se dividen así:**
  - 3 marcas de grupo: UR231 (η² dentro del grupo = 0), UR123 y AS128 (V color~grupo 0,86–1,0);
  - 2 columnas con variantes moteadas: HP017 (W al final, W:MB al principio) y UR208 (W primera, AB máximo);
  - 1 sin código: UR1140 (η² 0,03);
  - **solo QU013 (YB grande frente a BS pequeño, en 24 grupos) y UR1152 son candidatos a categoría local real.**
  - Los compuestos no son torsión (V = 0), sino la distinción liso/moteado, que puede ser del transcriptor.
- **Fuentes:**
  - Solo Garcilaso y Calancha dan claves universales (amarillo = oro, negro = tiempo), y como ejemplos.
  - Quien examinó quipus o habló con sus usuarios lo niega: Day 1967; Mackey 1970/2002; Núñez del Prado 1950 («capricho imaginativo del operador»); Salomon 2004 («Consultants did not agree…»; «no two quipocamayos… resemble each other in color array»).
  - Ascher 1983: «color y posición redundantemente».
  - El «color = rubro» sí está documentado, pero **dentro** de un quipu o ayllu (Salomon, Hyland, Mackey/Quispe, Urton/Atarco).
- **Respuesta a la pregunta:** los cronistas tenían razón en que el color era clave, porque dice qué rubro es cada cuerda. La clave, sin embargo, era del documento o del archivo, no del imperio. Por eso hoy el color se ve como «formato». No es una decepción: es la forma de una contabilidad con plantillas locales y lector experto.
- **Limitaciones:**
  - P1 descansa en 2 archivos (91 enlaces de suma);
  - las etiquetas no son comparables entre transcriptores;
  - liso/moteado sin imágenes;
  - T1 estricto con poca potencia (9 quipus en la prueba de preferencia);
  - P2b es post hoc.
- **Siguiente paso:** buscar más pares de sumas entre quipus fuera de Incahuasi y Puruchuco (p. ej. en el Santa o en Pachacamac) y repetir P1. Es la única prueba que separa «color del rubro» de «color del número».
