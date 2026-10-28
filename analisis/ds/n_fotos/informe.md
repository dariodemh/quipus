# Auditoría visual de las fotos AS del *Code of the Quipu Databook*

**Equipo:** `ds/n_fotos` · **Fecha:** 18 de octubre de 2026
**Fuente visual:** fotografías publicadas del Databook de Ascher (88 imágenes), consultadas solo para verificar valores; no se reproducen en este repositorio.
**Fuentes de contraste:** `analisis/datos/cuerdas.csv` (KFG), `analisis/ds/n_databook/databook_rows.csv` y el OCR `analisis/fuentes_txt/databook/as*.txt`.
**Entregables:** este informe, `auditoria_fotos.csv` (88 filas), `tabla_comparacion.csv`, `controles_fotos.py`, `controles_fotos.json`, `generar_auditoria.py`, `estructura_esperada.py`, `notas_vision.md`.

> **Restricción respetada:** las fotos no se copian, incrustan ni redistribuyen. Todo lo que sigue son descripciones textuales y cifras derivadas. Las imágenes solo se leyeron desde su carpeta original.

---

## 1. Pregunta

¿Qué muestran realmente las 88 fotos AS del *Databook*? ¿Permiten verificar la estructura gruesa (número de colgantes, grupos, colores dominantes, subsidiarias, cuerdas superiores, conservación) que transcriben el KFG y el OCR? ¿Qué objetos acompañan a los quipus prioritarios (AS069, los de mayores discrepancias y los asociados AS69–71, AS48&49, AS36&37)? ¿Aportan algo que la transcripción omita, o al revés?

No se audita el significado de los quipus: se audita la **cadena de transmisión visual → texto → base de datos**, un paso previo a cualquier análisis semántico.

---

## 2. Método

### 2.1 Corpus y unidad

- 88 archivos, pero **27 etiquetas de quipu**: 23 quipus efectivamente fotografiados y 4 conjuntos que solo aparecen por sus objetos asociados (AS036/AS037, AS048/AS049, AS059–AS067, AS069–AS071 assoc).
- Las 23 etiquetas representan **al menos 30 objetos físicos**: AS026A y AS026B son dos quipus; AS033A–G son siete piezas (aunque en las fotos se ven ~4). Unidad de análisis: **el quipu**, no la foto.
- Solo **~25 fotos son vistas generales**; ≥28 son macros de nudos o uniones, ≥12 son detalles parciales y ≥10 son duplicados o reexposiciones de la misma toma.

### 2.2 Protocolo de lectura visual

Para cada vista general anoté: número aproximado de cuerdas que cuelgan, número de grupos separados por espacio o color, colores dominantes, presencia de subsidiarias, cuerdas superiores, objetos asociados y conservación. Para los conteos usé como referencia la regla local (una regla métrica aparece en AS10, AS11, AS12, AS15, AS17, AS18, AS20, AS25, AS31, AS32, AS33, AS34, AS38, AS213, AS214, AS215). Las cifras son **aproximadas** y en los quipus grandes son **cotas inferiores**.

**Advertencia de no ceguera (crítica):** yo había leído antes los conteos del KFG y del Databook. Por tanto, mis conteos **no son independientes** y no pueden validar el archivo. Los trato como una descripción de lo visible y como un contraste de *consistencia*, no como una prueba. El único control realmente independiente es el aritmético (sección 4.2).

### 2.3 Contraste

Para cada quipu: (i) cuerdas totales y colgantes de nivel 0 en KFG; (ii) colgantes descritos en el OCR; (iii) grupos KFG vs grupos por espaciado del Databook; (iv) colores dominantes KFG vs OCR; (v) lo visible en la foto. Los grupos del Databook se extrajeron de la prosa previa a la tabla (`group of N pendant cords`, `pendant cord (n)`), no del parser de filas.

---

## 3. Resultados

### 3.1 Qué hay en las 88 fotos (y qué no)

| Tipo de contenido | Etiquetas | Fotos | Comentario |
|---|---|---:|---|
| Quipu completo o casi completo | AS010, 011, 012, 015, 017, 018, 020, 025, 026, 031, 032, 033, 034, 038, 069, 070, 213, 214, 215 | ~55 | 19 etiquetas |
| Quipu en detalle/macro | AS012, 020, 025, 026, 031, 032, 033, 038, 069, 070, 212, 124, 136, 140 | ~25 | Nudos, uniones, remates |
| Solo objeto asociado | AS036/037 (bolsa), AS048/049 (cerámica), AS059–067 (bolsa), AS069–071 (cordones) | 8 | **No hay foto de esos quipus** |
| Quipu sobre soporte de madera | AS124, AS136, AS140 | 5 | Barra tallada, no cordón principal textil |
| Montaje museográfico | AS038 (radial), AS213 (tabla negra) | 10 | La disposición no es la original |

**Resultado negativo mayor:** las fotos **no** son 88 quipus ni 88 vistas. Faltan por completo los quipus AS036, AS037, AS048, AS049 y AS059–AS067; de ellos solo se fotografiaron la bolsa P688, la cerámica de La Centinela y la bolsa de Chala.

### 3.2 Conteos: cuerdas visibles vs archivo

`n0` = colgantes de nivel 0 en KFG. En AS010 y AS212 el `n0` incluye cuerdas superiores (ver 3.4). "Visual" = cuerdas que cuelgan, no necesariamente colgantes de nivel 0.

| Quipu | KFG total / n0 | Databook colgantes | Visual (aprox.) | Grupos KFG/DB | Veredicto |
|---|---:|---:|---:|---:|---|
| AS010 | 28 / 27 | 23 | **23 + 2 top** | 13 / 9 | parcial: KFG suma 2 top + 2 fantasmas |
| AS011 | 24 / 15 | 15 | 15 | 2 / 2 | **sí** |
| AS012 | 105 / 85 | 85 | 35 | 7 / 6 | parcial: no verificable |
| AS015 | 12 / 12 | 12 | 13 | 3 / 3 | **sí** |
| AS017 | 39 / 20 | 20 | 22 | 2 / 2 | **sí** |
| AS018 | 10 / 9 | 9 | **9** | 1 / 1 | **sí, exacto** |
| AS020 | 10 / 10 | 10 | **10** | 2 / 2 | **sí, exacto** |
| AS025 | 2 / 2 | 2 | **2** | 2 / 2 | **sí, exacto** |
| AS026A | 77 / 54 | 63 | ~70 cuerdas | 6 / ? | parcial |
| AS026B | 260 / 105 | 135 | ~250 cuerdas | 13 / ? | parcial: visual = cuerdas totales |
| AS031 | — | 54 | 52 | — / 9 | n/a (sin KFG); cuadra |
| AS032 | — | 405 | 175 | — / 102 | parcial: subconteo por maraña |
| AS033 | — | 100 (7 piezas) | 30 (1 pieza) | — / ? | parcial |
| AS034 | — | 108 | 95 | — / 18 | parcial (ilustración) |
| AS038 | — | 108 (6×18; parser 115) | 110 | — / 6 | **sí** |
| AS048 | 80 / 52 | 52 | — | 12 / 12 | n/a: no hay foto |
| AS059 | 8 / 8 | 8 | — | 2 / 2 | n/a: no hay foto |
| AS069 | 1831 / 1650 | 1404 | >500 | **432 / 204** | parcial: plegado gigante |
| AS070 | — | 99 (prosa 88) | 95 | — / 15 | n/a (sin KFG); cuadra |
| AS124 | — | 56 | — | — / — | n/a: barra de madera |
| AS136 | — | 180 (2×90) | ~100 | — / 20 | parcial: se ve **una mitad de 90** |
| AS140 | — | 180 (2×90) | ~110 | — / 20 | parcial: se ve **una mitad de 90** |
| AS212 | 100 / 68 | 65 | — | 13 / 13 | parcial: n0 incluye 3 top |
| AS213 | 36 / 18 | 18 | **19** | 1 / 1 | **sí** |
| AS214 | 20 / 20 | 20 | **20** | 6 / 6 | **sí, exacto** |
| AS215 | 37 / 28 | 27 | **28** | 11 / 10 | **sí** (1 top) |

**Lo que cuadra.** En 11 quipus pequeños y extendidos el conteo visual coincide con los colgantes de nivel 0 con desviación ≤2 (AS010 tras corregir, AS011, AS015, AS017, AS018, AS020, AS025, AS031, AS213, AS214, AS215). AS018, AS020, AS025 y AS214 coinciden **exactamente**. Las fotos, por tanto, sirven para verificar estructura gruesa de quipus de ≤30 colgantes.

**Lo que no cuadra y por qué.**
- **AS012 (35 vs 85).** La foto muestra dos racimos densos, ~30–35 cuerdas gruesas; 85 exigiría ~3 cuerdas/cm. No puedo refutar el archivo: puede haber una segunda capa o cordones finos superpuestos. Queda **no verificable**, no "falso".
- **AS032 (175 vs 405).** La foto en U muestra 150–200 cuerdas; el resto puede estar en la segunda capa o en la maraña inferior. Subconteo esperable.
- **AS069 (>500 vs 1650).** Quipu plegado en 5–6 tramos; cada tramo muestra 150–250 cuerdas. Es geométricamente compatible con 1650, pero **no contable**.
- **AS026.** El conteo visual (~330 cuerdas) coincide con las **337 cuerdas totales** de KFG (77 + 260), no con los 159 colgantes de nivel 0. Es la demostración más limpia de que **contar cuerdas colgando no es contar colgantes**: las subsidiarias cuelgan al lado y se confunden con los colgantes.
- **AS136/AS140 (180 vs ~100).** El Databook dice que la unión a la barra separa cada quipu en **2 partes de 10 grupos de 9 = 90 por parte**. La foto muestra exactamente una de las dos mitades. No hay contradicción: 180 es el total, ~90–110 es lo visible.

### 3.3 Grupos: 13/17 exactos, con dos explicaciones mecánicas

Comparé los grupos KFG (`grupo`) con los grupos por espaciado del OCR en 17 quipus comparables:

- **13/17 exactos** (76.5 %), **15/17 dentro de ±1** (88.2 %), mediana de la diferencia = **0**.
- Nulo de permutación (emparejar los grupos KFG con los del Databook de **otro** quipu, 5 000 permutaciones, semilla 42): p = **0.0002** para el número de aciertos exactos y p = **0.0002** para el error absoluto medio. Holm para dos pruebas: **0.0004**.
- El error absoluto medio (13.8) está dominado por **AS069** (432 vs 204). Sin AS069 y AS010, los 15 restantes coinciden todos dentro de ±1 y 13 exactamente.

Las dos discrepancias no son errores aleatorios:

1. **AS069: 432 grupos KFG vs 204 del Databook.** KFG tiene **205 grupos de una sola cuerda**, de largo 36–43 cm, casi todos sin nudos (199 de 205) y muchos con una banda de color en el extremo superior (0–2 cm). Son los **"markers"** que el Databook describe aparte ("markers 1 & 2, group of 7 pendants..."). Los otros 227 grupos de KFG tienen ≥2 cuerdas, frente a los 204 del Databook. Es decir: **432 = 227 grupos múltiples + 205 marcadores**. Los 205 marcadores explican el 89 % del exceso; los 23 grupos múltiples restantes (11 % del exceso) no están explicados y podrían ser subdivisiones por cuerdas superiores o por espaciado. **En lo esencial es un artefacto de definición, no un error de conteo.**
2. **AS010: 13 grupos KFG vs 9 del Databook.** KFG separa como grupo cada colgante aislado y cada cuerda superior; el Databook los agrupa por espaciado. Ejemplo: los 7 grupos de 1 cuerda de KFG incluyen los dos top cords (T1, T2) y dos cuerdas de largo 0.

### 3.4 Cuerdas superiores, marcadores y desplazamiento posicional (hallazgo principal)

La foto de AS010 permitió alinear la imagen con el texto y descubrir un problema que afecta a todo el KFG:

- El Databook describe **T1** a 3.0 cm y **T2** a 10.0 cm. En KFG, **T1 es `p1`** (con su subsidiaria `p1s1`) y **T2 es `p18`**. Es decir, las cuerdas superiores **ocupan números de colgante** y desplazan la numeración.
- KFG tiene **27 "colgantes"** en AS010; el Databook describe **23**. La aritmética es exacta: **23 colgantes + 2 cuerdas superiores + 2 cuerdas de largo 0 (`p15`, `p26`) = 27**. Las dos de largo 0 no existen físicamente: son filas fantasma.
- **AS212:** el Databook describe "group of 3 top cords (T1–T3)" entre los grupos 45–50 y 51–55. En KFG esas tres cuerdas son **`p51`, `p52`, `p53`**, y los colgantes 51–55 del Databook pasan a ser `p54`–`p58`. KFG tiene 68 nivel 0; el Databook, 65 colgantes: **68 − 3 top = 65**. Exacto.
- **AS215:** KFG tiene 28 nivel 0; el Databook, 27 colgantes + 1 cuerda superior que une 6 colgantes. **28 − 1 = 27**.
- **AS069:** no solo hay marcadores: como los marcadores también se numeran como `p`, la **numeración de KFG se desplaza** respecto del Databook. En los pares alineados del equipo `n_databook`: DB `p137` → KFG `p159` (+22); DB `p209` → KFG `p243` (+34); DB `p394` → KFG `p461` (+67); DB `p545` → KFG `p639` (+94); DB `p968` → KFG `p1137` (+169). El desplazamiento crece ~1 posición cada 6–7 colgantes, como corresponde a un marcador por grupo. **Cualquier unión posicional KFG↔Databook en AS069 sin mapa explícito está desfasada en decenas o cientos de posiciones.**
- 18 archivos del OCR mencionan cuerdas superiores (AS10, 13, 21, 44, 51, 57, 59, 61, 66, 67, 72, 96, 115, 199, 204, 207, 212, 215), es decir ~9 % de los 210 quipus. El problema no es anecdótico.

**Nivel de evidencia: bien apoyado** para AS010, AS212 y AS215 (la aritmética cierra exactamente y la posición coincide con el texto). **Apoyado con datos** para la extensión a AS069 (205 grupos de 1 cuerda con morfología de marcador y desplazamiento monótono en 5 pares alineados).

### 3.5 Colores

- **KFG vs Databook:** 92.2 % de coincidencia exacta de color (6 215 pares; nulo intra-quipu 42.9 %; p = 0.001; Holm = 0.003), ya medido por `n_databook`. Las diferencias son sobre todo `B→AB`, `WW→W`, `BY→YB` y adiciones de `W`/`PK`; no son bandas omitidas.
- **Fotos vs archivo:** en los 23 quipus la **familia** de color (claro/medio/oscuro) coincide, pero esta codificación no es ciega y solo distingue 2–3 categorías; no la presento como prueba.
- **Confirmaciones específicas útiles:**
  - **AS018:** KFG y OCR dicen `W` con una banda **`RM` a 2.5–3.0 cm**. La foto muestra exactamente eso: 9 colgantes blancos con **nudos largos teñidos de rojo** en ese tramo. Es la mejor confirmación visual de un color transcito.
  - **AS020:** la vista general parece uniforme, pero el macro `AS20(-)` muestra tres cordones distintos: **MB, KB y W**. La foto revela heterogeneidad que la vista general oculta.
  - **AS026:** el macro muestra cordones **azul-gris** junto a marrón y blanco.
  - **AS070:** el patrón **barber pole** (marrón oscuro/blanco) es visible en la vista general y en los macros.
- **Control de iluminación:** AS032 aparece **tan claro** en `AS32.jpg` y **casi negro** en `AS32(2).jpg`. Son la misma pieza con exposición distinta. **El color aparente de una foto no es dato**: solo sirve para confirmar/negar familias, no códigos Ascher.
- **Color a nivel de nudo:** AS018 y AS20 muestran que el color puede estar **localizado en el nudo** (RM) y no en toda la cuerda. El campo `color` de `cuerdas.csv` es de cuerda; una banda de 0.5 cm puede quedar resumida como `W(0-2.5)/RM(2.5-3)/W(...)`, lo que es correcto pero difícil de usar. No encontré un caso en que la foto muestre una banda ausente del archivo.

### 3.6 Subsidiarias y cuerdas superiores visibles

- **Subsidiarias:** visibles en AS012, AS017, AS020, AS031, AS212 (abanico de ~10 subsidiarias de un colgante), AS026 (macros) y AS215. En los quipus pequeños se distinguen; en los grandes se confunden con colgantes. AS212 es el caso más claro de un **colgante con un abanico de subsidiarias** (nivel 1); no veo evidencia visual de nivel 2.
- **Cuerdas superiores:** visibles en AS010 (dos), AS215 (una, a la izquierda) y AS034 (ilustración con 100/10/10/10/10 y "GRAND TOTAL 161"). En AS212 el Databook describe tres cuerdas superiores (T1–T3) que por posición corresponden a `p51`–`p53`; la foto muestra un grupo de tres cuerdas cerca del centro, pero no puedo asegurar que sean esas. En AS069 los marcadores **no** son cuerdas superiores: cuelgan como colgantes vacíos.

### 3.7 Objetos asociados y contexto arqueológico

| Conjunto | Qué se ve | Contexto documentado | Comentario |
|---|---|---|---|
| **AS069–AS071** | 5 colgantes sueltos (uno con etiqueta); ~12 cordones sueltos, algunos anudados; un **quipu asociado** con ~50–60 colgantes oscuros visibles y un grupo separado | Arica/Lluta, excavados en 1965 por Percy Dauelsberg; "el otro quipu (owner's #2)" tiene 102 colgantes, ~400 subsidiarias y 2 haces de 15+2 blanks; el conjunto incluye **34 blanks + 3 con nudos** | Las fotos documentan solo una parte de los 37 cordones descritos (5 + 12): el resto no está o está fuera de cuadro. El quipu asociado es compatible con el "owner's #2" (102 colgantes), pero la foto muestra ~55: **no verificable** |
| **AS036 & AS037** | **Bolsa tejida P688** con asa, listas marrón/crema/rojo y bandas geométricas; borde superior dañado | Maranga, Huaca 1; excavados en 1925; **4 entierros**; misma tumba con vasijas, calabazas y conchas; mismo número de museo P501A/P501B | La bolsa es el único objeto fotografiado; **los quipus no aparecen**. Contexto funerario múltiple, no una tumba individual |
| **AS048 & AS049** | **6 fragmentos de cerámica** (negro sobre rojo, crema con bandas, incisa) + **una vasija restaurada** con listas crema y asa | La Centinela, Tambo de Mora (Chincha), expedición Universidad de Tokio 1958; "fragmentos de cerámica asociados" | No hay foto de los quipus. La vasija está restaurada: no sirve para datación directa sin ficha |
| **AS059–AS067** | **Bolsa de tela oscura** rectangular, tejido liso, cordón de cierre, muy desgastada | Chala; bolsa depositada por Dorothy Menzel con Oscar Núñez del Prado, Cusco; contiene 8 quipus | No hay foto de los quipus; la bolsa es la asociación de los 8. El Databook dice que AS66/AS67 tienen cuerdas superiores, pero no se ven |
| **AS124, AS136, AS140** | **Barra de madera tallada**: AS124 con cabeza de animal; AS136 con tres figuras humanas (central y dos laterales); AS140 con figura humana que sostiene una copa/vaso | AS136/140: Museo de Berlín, ingreso 1904, procedencia declarada Nasca; AS124: Museo de Colonia | **Asociación no listada en el encargo.** ¿Soporte original o montaje museográfico? Las cuerdas de suspensión y la barra sugieren montaje, pero las tallas son elaboradas. **Propuesto**, no bien apoyado |
| **AS038, AS213** | Montaje radial sobre azul (AS038) y tabla negra con alfileres (AS213) | Museos | La disposición es **museográfica**; no usar el orden radial como orden original |

### 3.8 Conservación

- **Buena:** AS018, AS020 y AS213 (montado); AS059 (bolsa) estable; AS069 tiene las cuerdas completas pero muy enmarañadas.
- **Regular:** AS010, AS011, AS015, AS017, AS025 (lazos y extremos sueltos).
- **Mala:** AS031, AS032, AS033 y AS069 (marañas, extremos deshilachados, cordones rotos); AS012 y AS026 (tensión y superposición); AS136/140 solo se conservan en **fotografía B/N de archivo**, no en color.
- **Intervención:** AS033(1)-(2) muestra **hilo blanco de reparación** en el cordón principal; AS048/49 vasija restaurada; AS213 montada con alfileres. Son objetos intervenidos: la foto no es evidencia de estado original.

### 3.9 Los quipus prioritarios por discrepancias

- **AS069 (12 discrepancias):** 9 son `d_kfg_sin_nudos` (KFG perdió racimos), 1 `c_error_databook`, 1 `d_otras`, 1 `d_valor_dudoso`. La foto no permite leer nudos, así que **no adjudica ninguna**. Lo que sí aporta es la explicación de los grupos/marcadores y el desfase posicional.
- **AS012 (7 discrepancias):** todas `d_kfg_sin_nudos` (KFG valor 0 donde el Databook ve nudos). La foto muestra cuerdas con nudos oscuros, pero sin resolución para contar; **no adjudica**.
- **AS026B (7):** 4 `d_kfg_sin_nudos`, 1 `a_ocr`, 1 `c_error_databook`, 1 `d_convencion_x10`. La foto es un plano general; **no adjudica**.
- **AS050, AS101, AS013, AS207, AS073** (los siguientes en la lista) **no tienen foto** en esta carpeta. La auditoría visual no puede priorizarlos.

---

## 4. Controles

### 4.1 Control de conteo (fallido, y se reporta como tal)

Emparejé mis conteos visuales con el archivo en 17 quipus: Spearman **ρ = 0.994** (p permutacional = 5×10⁻⁵), pendiente log–log **1.08**; en los 11 quipus contables, ρ = 0.998 y pendiente 1.01. **Este resultado es circular**: yo conocía los conteos del archivo al contar. No demuestra que las fotos validen el KFG; solo que mis descripciones son internamente coherentes con lo que había leído. Lo consigno como **control fallido** y no lo uso en las conclusiones.

El control que sí es independiente es el **aritmético**: AS010 (23 + 2 top + 2 fantasmas = 27), AS212 (65 + 3 top = 68), AS215 (27 + 1 top = 28). Cierra al entero y no depende de mi percepción.

### 4.2 Grupos: nulo y corrección múltiple

- Nulo: permutar los grupos del Databook entre quipus (destruye el emparejamiento, preserva la distribución de tamaños). 5 000 permutaciones, semilla 42.
- Resultado: 13/17 exactos, p = **0.0002**; MAE 13.8, p = **0.0002**; Holm para 2 pruebas = **0.0004**.
- **Cautela:** el nulo es débil (los grupos son enteros pequeños y el azar acierta a menudo) y el MAE está dominado por AS069. La mediana de la diferencia es 0 y, sin AS069/AS010, 15/15 coinciden dentro de ±1. El test mide **acuerdo de definición**, no verdad.

### 4.3 Color: control de exposición

AS032, misma pieza, dos fotos: `AS32.jpg` la muestra **tan claro** y `AS32(2).jpg` **casi negra**. Es el control natural de que el tono fotográfico no es un dato de color. Cualquier codificación automática de color sobre estas fotos tendría un error de familia inaceptable. Por eso no hice un test de color: solo verifiqué familias y casos específicos (AS018 RM, AS020 MB/KB/W).

### 4.4 Repetibilidad intra-observador

Las fotos duplicadas permiten repetir el conteo sin nueva información: AS017 22/22, AS031 50/52, AS012 30/35. En quipus pequeños la repetibilidad es ±2; en los enmarañados, ±5. Es una medida de ruido, no de validez.

### 4.5 Corrección múltiple

Solo hay dos pruebas formales (grupos: exactos y MAE); se aplicó Holm y se reporta **0.0004** en ambas. Los conteos y el color son descriptivos y no llevan p-valor porque el diseño no es ciego.

---

## 5. Resultados negativos

1. **No encontré ninguna cuerda visible que falte en KFG y en el Databook a la vez.** No hay evidencia de "cuerdas fantasma" en el sentido inverso (foto → archivo). Las cuerdas fantasma van en la otra dirección: KFG → foto (AS010 `p15`, `p26`).
2. **Ninguna foto adjudica una discrepancia de valor.** La resolución no permite leer racimos completos; solo los macros (AS18, AS20, AS31(5), AS38, AS212) permiten contar nudos locales, y ninguno de esos quipus está en la lista de discrepancias.
3. **No hay fotos de los quipus AS036, AS037, AS048, AS049 ni AS059–AS067.** De ellos solo hay objetos asociados. Cualquier afirmación sobre su estructura física es textual, no visual.
4. **No hay evidencia de bandas de color omitidas por el KFG.** La coincidencia de familia es total, y los desacuerdos de código ya detectados (`B→AB`, `BY→YB`, adición de `W`) son de etiqueta, no de banda ausente.
5. **AS012, AS032 y AS069 no se pueden contar en foto.** Los subconteos (35/85, 175/405, >500/1650) **no son refutaciones**: son límites de visibilidad por capas, pliegues y maraña.
6. **AS034 no es una foto de museo**: es una ilustración histórica rotulada "A QUIPU FROM THE INCA CITY OF PACHACAMAC" con "GRAND TOTAL 161". Su procedencia es una afirmación de la fuente secundaria; no debe usarse como lugar de origen.
7. **El "mejor estado de conservación" de AS69–71 es relativo:** las cuerdas están completas, pero el espécimen está plegado y enmarañado; la foto no permite un conteo directo.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Las 88 fotos no son 88 quipus: 23 etiquetas fotografiadas + 4 conjuntos solo asociados; ≥30 objetos físicos | **Bien apoyado** (inventario de archivos) |
| AS010: KFG 27 = 23 colgantes + 2 cuerdas superiores + 2 cuerdas de largo 0 | **Bien apoyado** (alineación t1→p1, t2→p18 y aritmética) |
| AS212: las 3 cuerdas superiores son p51–p53 y los colgantes 51–55 pasan a p54–p58 | **Bien apoyado** (posiciones y 68−3=65) |
| AS215: KFG 28 incluye 1 cuerda superior; 28−1=27 | **Apoyado con datos** |
| AS069: 432 grupos KFG vs 204 del Databook por 205 marcadores contados como grupos | **Apoyado con datos** (morfología de los 205 grupos de 1 cuerda; 432 = 227 grupos múltiples + 205 marcadores; 23 sin explicar) |
| AS069: desplazamiento de la numeración KFG vs Databook (+22 a +169) | **Apoyado con datos** (5 pares alineados y crecimiento ~1/6–7) |
| Conteos visuales coinciden con nivel 0 en 11 quipus pequeños (±2) | **Apoyado con datos** (no ciego) |
| AS136/140: la foto muestra una de las 2 mitades de 90 | **Apoyado con datos** (texto del Databook + ~90–110 visibles) |
| Asociaciones AS36/37 (bolsa P688 + 4 entierros + cerámica/calabazas/conchas), AS48/49 (cerámica), AS59–67 (bolsa de Chala) | **Apoyado con datos** por el texto y la foto del objeto; **no verificado en los quipus**, que no se ven |
| AS69–71: el quipu asociado es el "owner's #2" de 102 colgantes | **Propuesto** (la foto muestra ~55; compatible, no verificable) |
| Las barras talladas de AS124/136/140 son soportes originales y no montajes | **Especulativo** (las fotos no lo deciden) |
| Cualquier afirmación sobre el significado de marcadores, colores o grupos | **No abordado / especulativo** |

---

## 7. Limitaciones

- **No ceguera:** los conteos se hicieron después de leer KFG y Databook. El único control independiente es aritmético.
- **Resolución:** 800×546 no permite leer nudos en vistas generales; solo macros. La auditoría es de estructura gruesa, no de valores.
- **Cobertura:** 5 quipus prioritarios no tienen foto; 3 solo tienen fotos B/N de archivo; 2 están montados y su orden es museográfico.
- **Color:** la iluminación y el escaneo cambian el tono (AS32); no se puede usar para códigos Ascher.
- **Objetos asociados:** las fotos no tienen escala ni ficha de excavación; el contexto proviene del OCR, no de la imagen.
- **AS033:** las 7 piezas A–G no se pueden asignar una a una a las fotos; solo distingo ~4 piezas.

---

## 8. Para el coordinador

- **Las 88 fotos no son 88 quipus.** Son 23 etiquetas fotografiadas (≥30 objetos: AS026A/B, AS033A–G) más 4 conjuntos que solo aparecen por sus objetos asociados. Faltan por completo los quipus AS036/37, AS048/49 y AS059–67: de ellos solo hay bolsa o cerámica.
- **El KFG mete cuerdas superiores y marcadores en el nivel 0.** AS010: 27 = 23 colgantes + 2 top + 2 cuerdas de largo 0 (p15, p26). AS212: 68 = 65 + 3 top (p51–p53). AS215: 28 = 27 + 1 top. `nivel==0` **no** significa "colgante".
- **AS069 está doblemente inflado y desfasado.** 432 grupos vs 204 porque 205 marcadores se cuentan como grupos de 1; y la numeración KFG se desplaza hasta +169 posiciones (DB p968 → KFG p1137). No usar uniones posicionales KFG↔Databook en AS069 sin mapa.
- **Los conteos visuales funcionan en pequeño, no en grande.** 11 quipus de ≤30 colgantes coinciden con ±2 (AS018, AS020, AS025, AS214 exactos). AS012 (35/85), AS032 (175/405) y AS069 (>500/1650) subestiman por capas/maraña; no son refutaciones. AS136/140 son 2×90 y la foto muestra una mitad: cuadra.
- **El color solo se puede auditar por familias.** AS018 confirma la banda RM a 2.5–3.0 cm (nudos rojos); AS020 revela MB/KB/W que la vista general oculta; AS032 cambia de tan a casi negro según la exposición. No usar color de foto como código Ascher.
- **Asociaciones nuevas:** AS124, AS136 y AS140 están atados a **barras de madera talladas** (animal en AS124; tres figuras en AS136; figura con copa en AS140). No estaba en el encargo; no se puede decidir si son soportes originales o montajes.
- **AS69–71:** las fotos muestran 5 colgantes sueltos, ~12 cordones (algunos anudados) y un quipu asociado de ~55 colgantes visibles. El Databook describe 34 blanks + 3 anudados y un "owner's #2" de 102 colgantes: la foto documenta solo parte.
- **Recomendación de datos:** añadir a `cuerdas.csv` una columna `tipo` (colgante / superior / marcador / fantasma) y un `p_db` con la numeración del Databook. Sin eso, cualquier análisis de grupos o posiciones en AS010, AS069, AS212 y AS215 estará sesgado.
- **Siguiente ronda:** (i) fotografiar los quipus AS036/37, AS048/49 y AS059–67; (ii) re-fotografiar AS012, AS032 y AS069 con alta resolución y escala; (iii) repetir los conteos de forma ciega con dos anotadores para convertir la concordancia en evidencia; (iv) probar si los marcadores de AS069 tienen color/posición sistemáticos (posible función de conteo).

---

### Archivos de esta carpeta

- `auditoria_fotos.csv` — 88 filas, una por foto, con conteos, colores, observaciones y veredicto.
- `tabla_comparacion.csv` — resumen por quipu (26 filas: 23 etiquetas fotografiadas + AS026A/B desdoblados).
- `controles_fotos.py` / `controles_fotos.json` — permutation tests y cobertura.
- `generar_auditoria.py` — genera el CSV a partir de las observaciones.
- `estructura_esperada.py` / `estructura_esperada.csv` — conteos KFG/OCR por quipu fotografiado.
- `notas_vision.md` — notas crudas de la inspección.
