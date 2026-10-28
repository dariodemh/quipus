# Los quipus patrimoniales de Tupicocha (Salomon 2004): convenciones, límites y qué sobrevive para lo prehispánico

**Investigador:** n_salomon · **Fecha:** 2026-10-18
**Fuente primaria:** Frank Salomon, *The Cord Keepers: Khipus and Cultural Life in a Peruvian Village* (Duke UP, 2004), texto en `analisis/fuentes_txt/Salomon2004_CordKeepers.txt`. Todas las citas son **número de línea** de ese archivo (una línea = un párrafo).
**Datos:** KFG (`analisis/datos/cuerdas.csv`, 57 818 cuerdas, 651 quipus), OKR en modo lectura (no se usó para escribir), `quipus.csv`, `grupos.csv`.
**Scripts:** `tests_salomon.py` (pruebas principales), `robustez_torsion.py` (control de torsión). Salidas: `resultados_tests.csv`, `claves_salomon.csv`, `tupicocha_cuerdas.csv`.

---

## 1. Pregunta

¿Qué convenciones de lectura documenta o infiere Salomon para los quipocamayos de Tupicocha, con qué base probatoria, y **cuáles de esas convenciones dejan una huella medible en el corpus antiguo** (KFG/OKR) que sobreviva a un nulo por permutación y a corrección de comparaciones múltiples?

La pregunta no es "¿qué dicen los quipus de Tupicocha?" —Salomon no los descifra— sino "¿qué regularidades formales de los quipus antiguos son compatibles con el sistema que Salomon reconstruye, y cuáles no?".

---

## 2. Método

1. **Lectura selectiva con cita de línea.** Se leyeron íntegras las secciones descriptivas del cap. 6 (L1737–1930), el cap. 9 (L2529–2880) y las secciones de correspondencia del cap. 7 (L2026–2275), más los pasajes de datación (L1608–1622), de interpretación aldeana (L2304–2460) y del episodio de 1750 (L1566–1592). No se leyó el libro entero.
2. **Extracción de convenciones** a `claves_salomon.csv`, cada una con: fuente (línea), base (testimonio / correlación con libros / inferencia), predicción medible y nivel de evidencia.
3. **Pruebas en el corpus antiguo.** Unidad = **quipu**. Cuando el estadístico es a nivel de cuerda, el nulo **permuta dentro de cada quipu** y los z se agregan por `Z = Σz/√k` (evita pseudorreplicación). Cuando el estadístico es un conteo por quipu, el nulo permuta dentro de cada grupo y se agrega igual. 2000 permutaciones (500 en los barridos de rachas), semilla 20261018. Holm sobre 12 pruebas con p calculable.
4. **Color**: se eliminan los rangos en cm con `re.sub(r'\([^)]*\)','',s)` y se agrupa en familias "émicas" a la Salomon (W; BR = chumpi/marrones; GY = grises; RD; BL; YL; OT). Se probó también un nulo **dentro del grupo físico** (espacios del cordón principal), que es el más conservador.
5. **Blancos**: `nudos` vacío = cuerda sin nudos (no es un cero real). 31,6 % de los colgantes del corpus (13 192/41 714).

---

## 3. Convenciones que Salomon documenta o infiere

### 3.1 Arquitectura y fabricación

| # | Convención | Base | Nivel |
|---|---|---|---|
| C1 | 9 de 10 quipocamayos son **"bandados"**: colgantes agrupados por color, sin espacios de cordón principal entre grupos (L1883–1885). | Observación directa de los 10 especímenes. | Bien apoyado (para Tupicocha) |
| C2 | Cuerdas de 2 plies, cada ply de 2 hilos; torsión alterna S–Z–S o Z–S–Z; **mayor incidencia de Z que en los especímenes antiguos** (L1786–1787). | Observación; comparación con colecciones. | Apoyado |
| C3 | El nudo largo Inka ("con argolla") y el nudo Tupicocha (T) **no son alomorfos**: el primero "ata" (guardado), el segundo "libera" (L1839–1857, L2326–2331). | Testimonio de Nery Javier (recuerdo de su bisabuelo Tobías) + morfología. | Propuesto |
| C4 | Hay un tercer nudo largo, el **Mújica** (múltiple ocho), sólo 2 veces y sólo en m-01 (L1864). | Observación. | Bien apoyado |
| C5 | La torsión no es signo para los artesanos: "cuestión de costumbre personal" (L1800–1801, L2333). **Pero** el par 1sf-01/2sf-01, escindido en los años 20, se opone S vs Z (L1802–1806). | Contradicción explícita entre testimonio y un caso. | Propuesto (el caso único) |
| C6 | El **pachacamanta** (nudo terminal ornamentado) marca el extremo inicial; su nombre se glosa "acerca del ciento" y sugiere que el ayllu era una *pachaka* (L1769). | Testimonio de un anciano + etimología. | Especulativo |
| C7 | **Hitos/motas** en el cordón principal y **cantitos** (hilo brillante pasado) forman un "metacódigo" de comentario, con paleta distinta a la de las cuerdas de datos (L1772–1785). | Observación + testimonio (fiestas, jurisdicción). | Propuesto |
| C8 | No hay espacios que separen grupos; las **subsidiarias** ("compañías") se fijan en cm 0 y son el 10,6 % de los colgantes (L1753, L1883–1884). | Observación. | Bien apoyado |

### 3.2 Colores

| # | Convención | Base | Nivel |
|---|---|---|---|
| C9 | El color agrupa **funciones**, no cantidades: "como capítulos de un libro" (faenas, alimentos, reservorio) (L2341–2342). | Testimonio de Nery Javier; coherente con los libros de actas. | Apoyado (émico) |
| C10 | El orden de las bandas **no se repite** entre quipus, ni siquiera dentro del mismo ayllu: "ninguno se parece obviamente a otro en el array de colores" (L2539). | Observación de los 10 especímenes. | Bien apoyado (para Tupicocha) |
| C11 | El color se percibe en dos familias (chumpi/marrón y oque/gris) que se tocan en negro y blanco, más colores "vivos" de acento (L1829–1831). | Tres artesanas clasificando cuerdas por separado; acuerdo parcial. | Apoyado |

### 3.3 Nudos y valores

| # | Convención | Base | Nivel |
|---|---|---|---|
| C12 | Los nudos son sobre todo **identificadores** (número de orden, nombre, estatus), no cantidades; la posición del nudo **no está estandarizada** (L2679–2685). | Irregularidad observada + ausencia de sumas. | Propuesto |
| C13 | La **cuerda sin nudos = cuenta saldada** ("cumplió todo… se va"), no casilla vacía (L2326–2328, L2674–2678). | Testimonio de Nery Javier + lógica de "registro negativo". | Apoyado (émico) |
| C14 | La ausencia se marca **con un nudo en una cuerda existente**, no creando cuerda nueva; por eso un registro negativo tiene menos nudos, no menos cuerdas (L2197–2199). | Fuente quechua de 1608 + libros de actas. | Apoyado |
| C15 | Tupicocha **no tiene cuerdas superiores ni cuerdas de suma**: no se computa a través de cuerdas (L2680–2682). | Observación directa. | Bien apoyado (para Tupicocha) |
| C16 | La primera cuerda junto al pachacamanta es anómala, "portada" o etiqueta del conjunto (L2784–2786). | Observación (m-01, colgante 1 sin nudo). | Propuesto |

### 3.4 Unidades sociales y calendario

| # | Convención | Base | Nivel |
|---|---|---|---|
| C17 | La unidad de cuenta es el **hogar**, no el individuo; no hay censo (L2071–2073). | Libros de actas + etnografía. | Apoyado |
| C18 | **Una banda = una faena y su anfitrión** (*gastador*), no un miembro por cuerda: el modelo "un miembro por colgante" es refutado por el tamaño de banda (L2669–2672). | Conteo: 5,6 colgantes/banda vs. ~15 hogares. | Apoyado |
| C19 | **15–16 bandas por quipu, ~31 por par, ~100 colgantes, ~6 por banda**; el 15 se corresponde con los hogares del ayllu (1919: 14 miembros → "ronda en 14 partes") y con la estructura 15/30 de las *huacsa* de 1608 (L2587–2593, L2595–2597, L2610–2619, L2648–2656). | Conteo + libros + manuscrito quechua. | Apoyado (para Tupicocha); el salto al 15/30 colonial es **especulativo** |
| C20 | Los quipus van **en pares**, uno por cada oficial dual (camachico/mayor) o uno por semestre; los pares de Allauca y Satafasca difieren en ≤2 bandas (L2140–2144, L2595–2596). | Testimonio oral + conteo. | Apoyado |
| C21 | El orden de los colgantes es **cronológico** y los hitos marcan términos fijos (semestre/año) (L2346–2349). | Testimonio de Nery Javier. | Propuesto |
| C22 | El sentido de lectura (izquierda→derecha o inverso) **sigue sin determinarse** (L2403). | — | No resuelto |

---

## 4. Quipus concretos y reconstrucción en formato de cuerdas

Salomon **no publica una tabla cuerda-por-cuerda** de ningún quipocamayo: la "Key Figure 26" es un dibujo, no un listado, y la tabla 10 (conteos por espécimen) está **ilegible en el texto OCR** (los números se perdieron). Por eso `tupicocha_cuerdas.csv` contiene:

- **64 filas** con el **esquema posicional completo de m-01** (16 cuartetos × 4 posiciones Ch–v1–O–v2), con las reglas de color, torsión, nudos y valores que Salomon enuncia para cada posición (L2711–2748, L2819–2840). Es una reconstrucción **gramatical**, no observacional: los valores concretos de cada cuerda no se conocen.
- Las **pocas cuerdas con atributos explícitos**: colgante 1 de m-01 (sin nudo), 11 (nudo M), 39 (marcador central tricolor), 1sf-01 p1–6 (S) y p7–12 (Z), p30–32 (cantito), p66 (mechón atado), 2a-01 p77 (deshilachado), c-01 (dos grises con pelo de vaca), 1g-01 (88+10 cuerdas, sólo 6+4 anudadas).

Datos agregados recuperables (verificables en el texto):

| Quipu | Colgantes | Subsidiarias | Bandas | Nudos |
|---|---|---|---|---|
| 1g-01 (Primer Huangre) | 88 | 10 | 15 (10 sin ningún nudo) | 6 colgantes + 4 subsidiarias |
| m-01 (Mújica) | ~64 (16 cuartetos) | 0 | 16 "cuartetos" | mayoría anudada; tipo A siempre |
| 9 bandados | 70–125 (media 101) | 10,6 % de colgantes | media 15,4; mediana 15; moda 15 | variable |
| Total 10 | media 98 (con m-01) | — | media 15,5 (DE 2,1) | — |

**Limitación honesta:** sin la tabla 10 original no puedo reconstruir los conteos por espécimen ni verificar el "±2 bandas" de los pares. Lo que sí se reconstruye es la *gramática* de m-01, que es el único quipu con estructura posicional explícita.

---

## 5. Quipus y libros de actas: cómo buscó, qué encontró, qué falló

**Cómo buscó.** Tupicocha tiene 128+ volúmenes de actas de ayllu desde 1870, escritos espontáneamente, sin supervisión estatal (L2063). Salomon no busca una traducción; busca **isomorfismos estructurales**. Formula ocho proposiciones (L2035–2037) y las contrasta con atributos de las cuerdas.

**Qué encontró.**
1. **Contenido interno al ayllu**: ningún otro ente posee quipocamayos (L2039).
2. **Plan + prueba de ejecución**: las actas registran (a) compromisos y (b) su cumplimiento, con *cumplido / no vale* (L2066). Los quipus serían el mismo par plan/ejecución: m-01 (ciclo de color) = planificación; bandados = ejecución (L2868–2873).
3. **Unidad = hogar** (C17).
4. **Secuencia por número de orden / familia / grados de edad** (L2075–2096): tres modos de seriar, que dan tres hipótesis de orden para las cuerdas.
5. **Dualidad de oficiales** ↔ dualidad de quipus (C20).
6. **Las faenas son el tema dominante** de las actas y, por analogía, de las cuerdas (L2160–2164).
7. **Registro negativo** como método por defecto hasta 1930 (L2183–2189).
8. **Auditoría social**: el balance apunta a cero; de ahí la abundancia de cuerdas sin nudos (L2262).

**Las dos pruebas numéricas que sí hizo** (L2647–2666):
- **Test 1a**: Cacarima 1919 escribe que la ronda se hará "en 14 partes" y tiene 14 miembros; un ciclo rendiría "miembros + 1" sesiones ≈ 15. Compatible con 15–16 bandas.
- **Test 1b**: Segunda Allauca registra 12–13 obligaciones supra-ayllu por año en 1925–33; sumadas a las ~15 internas dan ~30, compatible con ~31 bandas por par.

**Qué falló.**
- **Ninguna entrada de acta se leyó contra ninguna cuerda.** Salomon lo dice: los libros "aluden a los quipocamayos sin decir qué información contenían las cuerdas" (L2027). La correspondencia es **de formato y de número**, nunca léxica. Es el límite central del libro.
- **La datación no fija el momento**: 10 de 13 muestras caen en la meseta 1650–1950; el método probabilístico de McJunkin/Edwards sugiere ~1870, pero es "una inferencia novedosa, no parte del canon radiocarbónico" (L1616–1619). m-01 tiene cuerdas de 1979 y 1990 (L1621).
- **El retro-quipu narrativo fracasó**: la idea inicial de mapear la estructura episódica del manuscrito quechua de 1608 sobre los quipocamayos se abandonó porque "cronología e índices funcionales apuntan a continuidades menos simples" (L363).
- **Los "nudos fantasma" no se pudieron leer**: como los nudos de Tupicocha no están estandarizados, Salomon no puede distinguir un nudo removido de una arruga (L1906–1908).
- **m-01 está contaminado**: las cuerdas tipo A (Ch y O) fueron restauradas después de 1979; el propio Salomon duda de su fiabilidad (L2744). Cualquier lectura de m-01 es, en parte, lectura de una restauración moderna.

---

## 6. Quipu → escritura alfabética, y los quipus "narrativos"

**Continuidad, no muerte.** El cap. 5 argumenta contra la tesis de la desaparición política del arte del quipu en el siglo XVI: en Huarochirí se siguió haciendo quipus junto a la "ciudad letrada" durante siglos (L371). El caso fuerte es **1750**: María Micaela Chinchano llevó 22 cartas de un oficial español a 22 pueblos, cada una con un quipu atado; los quipus eran de **colores variados** y fueron leídos como autenticación/paráfrasis (L1566–1592). Salomon maneja tres hipótesis —etiqueta de dirección, acreditación, paráfrasis del contenido— y **no elige**: "no sabemos el contenido de las cuerdas" (L1588). Lo decisivo es que el episodio prueba competencia de quipu **ordinaria y rápida en 1750**, no especializada ni masculina.

**Narrativos.** Salomon es explícitamente escéptico:
- No encuentra "ningún uso sistémicamente imitador del lenguaje" (L343); los resultados son "compatibles con una lectura más que lockeana… pero no confirman" un sistema lingüístico.
- Urton (1998) ve anomalías (valores >10, nudos fuera de lugar) en ~1/3 de los quipus antiguos y las llama "narrativas"; Tupicocha "no confirma la narración como tal, pero sí confirma funciones fuera de lo numérico" (L1840).
- La estructura episódica "preformateada" de las crónicas (catálogos de campañas) haría posible un quipu narrativo, pero no hay evidencia (L356).
- La **khipumancia** (adivinación contando sílabas/pares) es, en su opinión, una **back-formation moderna** influida por la cartomancia y la alfabetización, aprendida en los años 30–40, cuando ya nadie actualizaba quipus (L2452–2456). No es una pista sobre lo prehispánico.

**Juicio de Salomon:** el quipu es un **medio operable** (se desarma, se reanuda, se corrige), no un texto fijo; su fuerza está en la simulación y el registro, no en la legibilidad *ex post facto* (L1892–1900). La metáfora correcta es "mazo de cartas" / "diagrama de circuitos", no "libro".

---

## 7. Pruebas en el corpus antiguo

### 7.1 Resultados (tabla)

`n` = quipus; `Z` = z agregado (Σz/√k); `p` de dos colas; `q` = Holm sobre 12 pruebas.

| Prueba | n | Z | p | q | Efecto |
|---|---|---|---|---|---|
| T1 Color en bandas (quipu completo) | 492 | −45,9 | <1e−15 | <1e−15 | 0,870× las rachas esperadas; 52,9 % de quipus con \|z\|>2 |
| T1b Color en bandas (dentro del grupo físico) | 387 | −19,3 | 1,1e−82 | 9,5e−82 | 0,944×; 41,9 % con \|z\|>2 |
| T2 Torsión en rachas | 27 | −13,8 | 3,3e−43 | 2,3e−42 | **artefacto**: ratio mediano 1,003 (ver 7.3) |
| T2b Torsión: mitades | 24 | +4,19 | 2,7e−5 | 1,1e−4 | diferencia media de fracción S entre mitades = 2,5 pp |
| T3 Blancos en rachas (quipu) | 422 | −43,8 | <1e−15 | <1e−15 | 0,814×; 41,9 % con \|z\|>2; 29,6 % de colgantes blancos |
| T3b Blancos en rachas (dentro del grupo) | 366 | −15,6 | 3,9e−55 | 3,1e−54 | 0,933× |
| T4a Primera cuerda blanca | 617 | — | 0,001 | 0,003 | +5,1 pp sobre la tasa del propio quipu |
| T4b Primera cuerda "distinta del vecino" | 617 | — | 0,20 | 0,20 | +1,3 pp (nulo) |
| T5 Orden de color entre quipus del mismo sitio | 302 | — | 0,088 | 0,18 | acuerdo 0,336 vs nulo 0,214 (+0,12) |
| T6 Cabeza de grupo = suma del resto | 100 | +5,01 | 2,7e−7 | 1,4e−6 | 129 grupos (2,96 % vs 1,77 % esperado); 17 % de quipus con z>2 |
| T6b Cuerda superior = suma del grupo | 1 | — | — | — | no testeable (1 grupo) |
| T7 Subsidiaria contrasta con la madre | 317 | −5,84 | 5,3e−9 | 3,2e−8 | **−2,9 pp**: coinciden MÁS que el azar |
| T8 Color explica el valor | 418 | +42,9 | <1e−15 | <1e−15 | η² = 0,062 del log-valor |

### 7.2 Lectura

- **Bandas de color: sí, pero modestas.** Las cuerdas del mismo color se agrupan mucho más de lo que permite el azar (Z≈−46). Pero el efecto es del ~13 % de rachas, y **baja al 6 % cuando se permuta dentro del grupo físico**: buena parte de la homogeneidad de color coincide con los espacios del cordón principal que ya usa el transcriptor. Es un efecto real de "banda", pero no es la estructura dominante que Salomon ve en Tupicocha.
- **Blancos: se agrupan, no se dispersan.** El resultado es inequívoco y sobrevive al nulo conservador (0,93× dentro de grupo). Esto **apoya la lectura "cuerda saldada / banda cumplida"** de Salomon y **contradice** la lectura "casilla de unidad ausente", que predeciría blancos dispersos. Pero no la refuta del todo: un registro negativo con blancos por grupo también produce agrupamiento.
- **Torsión: no es un código general.** El z enorme de T2 es un artefacto de quipus con minoría Z minúscula (2–3 cuerdas Z entre 40 S: la adyacencia de esas pocas produce z extremos). Al restringir a quipus con minoría ≥20 % quedan **4 quipus**: allí el efecto es fuerte (0,43× rachas; diferencia de mitades 29,5 pp; 3/4 con z>2). Conclusión: **donde S y Z coexisten de verdad, la torsión forma bloques y opone mitades**; en el 96 % de los quipus (casi todo S) no hay nada que testear. La torsión no puede ser un código binario general, pero sí una marca de **taller/momento/lote**, que es exactamente la explicación aburrida.
- **Sin orden fijo de colores entre quipus del mismo sitio** (p=0,088, q=0,18): negativo, y coincide con Salomon. La ligera tendencia (0,336 vs 0,214) se explica porque W y BR son los colores más frecuentes, no por un canon.
- **La primera cuerda es "portada"**: más blanca (+5,1 pp), pero **no** más atípica en color. Apoyo débil a C16; el mecanismo parece ser "empieza con blanco", no "empieza con una cuerda rara".
- **Subsidiarias: el corpus antiguo hace lo contrario de lo que dice Salomon.** Las subsidiarias tienden a **repetir** el color de su madre (45,8 % de contraste observado vs 48,7 % esperado). La afirmación de "subsidiarias de color contrastante" (L1886) no se generaliza.
- **Sumas "de cabeza": existen en el corpus antiguo.** El 2,96 % de los grupos tiene su primera cuerda igual a la suma de las demás, frente a 1,77 % esperado (Z=5,0). El efecto es pequeño pero sólido y va en la dirección de las cuerdas superiores/suma de Urton, **no** de la negación de Salomon (que es cierta sólo para Tupicocha).
- **El color sesga el valor** (η²=0,062): la tesis "color = función, no cantidad" es demasiado fuerte. Un 6 % de la varianza del log-valor se explica por familia de color; es consistente con que ciertas categorías (rebaños, tejidos) tengan escalas típicas distintas, no con un sistema numérico color-codificado.
- **15–16 bandas / 100 colgantes NO es una regularidad andina.** En 441 quipus con ≥20 colgantes: mediana 10 grupos, moda 4, sólo 4,5 % con 15–16; mediana 56 colgantes; tamaño de grupo mediano 4, moda 1. El "15" de Tupicocha es **idiosincrático y demográfico** (14–19 hogares), no un canon prehispánico. Esto es un resultado negativo importante: la lectura calendárica 15/30 se apoya en una coincidencia local.

### 7.3 Controles y explicaciones aburridas

1. **Nulo conservador dentro de grupo** para color y blancos: los efectos bajan pero sobreviven (color 0,944×; blancos 0,933×).
2. **Artefacto de minoría escasa** en torsión: detectado y corregido (ver `robustez_torsion.py`).
3. **Convención del transcriptor**: el KFG registra colores por cuerdas contiguas; es plausible que el transcriptor "suavice" transiciones. No puedo descartarlo. El hecho de que el efecto caiga a la mitad al controlar por grupo sugiere que parte del banding es la propia definición de grupo del KFG.
4. **Pseudorreplicación**: evitada agregando z por quipu; los n de T1/T3 son 400–500 quipus, no 40 000 cuerdas.
5. **Comparaciones múltiples**: Holm sobre 12 pruebas. T5 (orden de color) y T4b (primera cuerda atípica) **no sobreviven**; no deben reportarse como hallazgos.
6. **Dependencia entre pruebas**: T1, T2, T3 y T8 usan el mismo corpus; Holm es conservador pero no corrige la correlación entre estadísticos. Los q deben leerse como "sobrevive a Holm", no como probabilidad conjunta exacta.

### 7.4 Resultados negativos (explícitos)

- No hay evidencia de un **orden fijo de categorías de color** entre quipus de un mismo sitio (T5, q=0,18).
- La **torsión no es un código binario** en el corpus: 90 % de las cuerdas son S y sólo 27/651 quipus mezclan S y Z.
- Las **subsidiarias no son de color contrastante**; al contrario (T7).
- **No se puede testear** el nudo Tupicocha vs Inka, los hitos, los cantitos, el pachacamanta ni las cuerdas superiores: el KFG no los codifica (o casi no existen: 26 quipus con alguna unión `T`, 1 grupo testeable).
- La **dirección de nudo** es `U` (desconocida) en la enorme mayoría de los registros: no testeable.

---

## 8. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Tupicocha tiene 10 quipocamayos bandados, ~15 bandas, ~100 colgantes, sin cuerdas de suma | **Bien apoyado** (observación directa de Salomon) |
| El color agrupa colgantes en bandas en el corpus antiguo | **Apoyado con datos** (Z≈−46; sobrevive al nulo dentro de grupo, aunque el efecto es del 6–13 %) |
| Las cuerdas sin nudos se agrupan en bandas saldadas | **Apoyado con datos** (0,81×; 0,93× dentro de grupo) |
| La torsión forma bloques/mitades donde S y Z coexisten | **Apoyado con datos**, pero sólo 4 quipus balanced → **propuesto** como fenómeno general |
| La primera cuerda es "portada" | **Apoyado con datos** (débil: +5,1 pp) |
| Existen sumas de cabeza de grupo en el corpus antiguo | **Apoyado con datos** (2,96 % vs 1,77 %; Z=5,0) |
| El color sesga el valor | **Apoyado con datos** (η²=0,06), interpretación **propuesta** |
| 15–16 bandas / 100 colgantes es un canon andino | **Refutado** como regularidad del corpus; es idiosincrasia de Tupicocha |
| Subsidiarias de color contrastante | **Refutado** en el corpus antiguo |
| Un quipu = plan (m-01) y otro = ejecución (bandado) | **Propuesto** (analogía con actas; no hay prueba independiente) |
| Las bandas = faenas con anfitrión (*gastador*) | **Propuesto** (compatible con conteos; no hay lectura) |
| El par de quipus = oficiales duales | **Propuesto** (testimonio oral + conteo ±2) |
| 15/30 = herencia de las *huacsa* de 1608 | **Especulativo** |
| La khipumancia es back-formation moderna | **Apoyado** (cronología del testimonio), pero no testeable en corpus |
| Los quipus "narrativos" existen | **No bien apoyado**; Salomon no encuentra imitación del lenguaje |

---

## 9. Qué conjunto de claves sobrevive como hipótesis para lo prehispánico

De las 22 convenciones, sobreviven **cinco** con algún respaldo en el corpus antiguo, y **dos** quedan refutadas:

**Sobreviven:**
1. **Banda de color = bloque funcional** (C1/C9). Efecto real aunque modesto. Es la hipótesis más transportable: el color segmenta, no numera.
2. **Cuerda sin nudos = categoría saldada/ausente**, no cero numérico (C13). El agrupamiento de blancos es el hallazgo más robusto de esta ronda.
3. **Primera cuerda = etiqueta/portada** (C16). Débil, pero consistente y barato de seguir probando con el ítem "blanco inicial" (que ya apareció en la literatura del repo).
4. **Suma en la cabeza del grupo** (contraria a C15, que es sólo de Tupicocha): hay un operador aditivo "de cabeza" en el corpus antiguo. Esto conecta con Urton y con la hipótesis de cuerdas superiores.
5. **Torsión como marca de lote/taller**, no como código (C5). Explica los bloques sin postular semántica.

**Quedan refutadas o no transportables:**
6. **15–16 bandas / ~100 colgantes / ~6 por banda** (C19): es demografía de Tupicocha, no canon. No usar como firma calendárica.
7. **Subsidiarias contrastantes** (C8): el corpus antiguo hace lo contrario.

**No transportables por falta de datos**: nudo T vs I (C3), hitos/cantitos (C7), pachacamanta (C6), cuerdas superiores (C15), dirección de nudo, orden de lectura (C22).

**Lo que el libro aporta y no es testeable pero debe guiar la próxima ronda:** la distinción **plan vs ejecución** (m-01 vs bandados) y la unidad **hogar/faena**. Son las hipótesis sustantivas más ricas, y ninguna se puede probar sin un corpus con pares identificados y libros contemporáneos. Tupicocha es el único lugar donde ambas cosas existen, y aun así Salomon no logró leer una sola entrada.

---

## 10. Para el coordinador

- **Salomon no descifra ningún quipu.** Su aporte es un modelo etnográfico (banda = faena, hogar = unidad, cuerda blanca = saldado, par de quipus = oficiales duales) y una demostración de que el arte siguió vivo hasta ~1870 (radiocarbono) y por lo menos hasta 1750 (caso Chinchano).
- **Lo más sólido que se transporta al corpus antiguo:** las cuerdas sin nudos se agrupan en bandas (0,81× las rachas esperadas; 0,93× aun dentro del grupo físico; n=422 y 366; q<1e−50). La lectura "blanco = casilla de unidad ausente" no se sostiene; la lectura "blanco = cuenta saldada / banda cumplida" sí.
- **El banding de color existe pero es modesto:** 0,87× las rachas esperadas, y sólo 0,94× al permutar dentro del grupo. Buena parte de la "banda" es la definición de grupo del transcriptor. No es la estructura dominante del corpus.
- **Resultado negativo importante:** 15–16 bandas y ~100 colgantes **no** son una regularidad andina (mediana 10 grupos, moda 4, sólo 4,5 % de 441 quipus en 15–16; mediana 56 colgantes). El "15/30" de Tupicocha es demografía local (14–19 hogares) y no debe usarse como firma calendárica prehispánica.
- **La torsión no es un código general:** 90 % de las cuerdas son S y sólo 27/651 quipus mezclan S y Z. Donde mezclan de verdad (4 quipus con minoría ≥20 %), hay bloques fuertes (0,43× rachas; mitades separadas 29,5 pp). Es marca de lote/taller, no semántica.
- **Las subsidiarias contradicen a Salomon en el corpus antiguo:** coinciden con el color de su madre más que el azar (−2,9 pp; q=3e−8). La regla "subsidiaria de color contrastante" no se generaliza.
- **Hay un operador aditivo "de cabeza"** en el corpus antiguo: 2,96 % de los grupos tienen la primera cuerda igual a la suma de las demás (vs 1,77 % esperado; Z=5,0; q=1e−6). Tupicocha carece de cuerdas de suma, así que esto es una **diferencia** Tupicocha/antiguo, no una continuidad.
- **El color sesga el valor** (η²=0,06): "color = función, no cantidad" es demasiado fuerte; hay una asociación débil pero real.
- **Para la próxima ronda:** (a) probar el "blanco inicial" y las bandas saldadas en quipus con grupos bien definidos y en OKR (no sólo KFG); (b) buscar pares de quipus del mismo sitio con estructura espejada para testear C20; (c) intentar recuperar la tabla 10 desde el PDF original (el OCR la perdió) para verificar los conteos por espécimen; (d) no gastar esfuerzo en hitos/cantitos/nudo T con KFG: no están codificados.
