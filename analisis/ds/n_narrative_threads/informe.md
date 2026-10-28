# *Narrative Threads* (Quilter y Urton, eds., 2002): balance y prueba de sus hipótesis con el corpus KFG

**Autor:** equipo `n_narrative_threads`
**Fecha:** 18 de octubre de 2026
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `quipus.csv`, `grupos.csv`; OKR `khipu.db` en modo lectura (619 quipus, 54 403 cuerdas).
**Texto leído:** `analisis/fuentes_txt/NarrativeThreads2002.txt` (4 324 líneas), por capítulos y con `grep`; no se imprimieron archivos completos.

---

## 1. Pregunta

¿Qué hipótesis de *Narrative Threads: Accounting and Recounting in Andean Khipu* (2002) siguen vivas veinticuatro años después, cuáles caen con los datos de cuerdas disponibles hoy y cuáles nadie ha probado?

Dos preguntas específicas del encargo:

1. Las oposiciones binarias que Urton formalizaría después (torsión S/Z, unión R/V, dirección de nudo S/Z, color marcado/no marcado): ¿co-varían como un código de 7 bits o son independientes?
2. El patrón de Incahuasi (UR273A con unión V / UR273B con unión R; UR267A V / UR267B R): ¿aparece en todo el corpus en pares emparejados por contenido o por sitio, y es más frecuente que un nulo?

---

## 2. Método

### 2.1 Unidad y nulo

- **Unidad de análisis: el quipu.** Todas las pruebas a nivel de cuerda usan estratificación por quipu; los nulos permutan **dentro de cada quipu**, de modo que se conservan los marginales de cada quipu y no se convierte la pseudorreplicación en significación.
- **Estadístico CMH** (Cochran–Mantel–Haenszel) para pares de rasgos binarios, con nulo hipergeométrico por estrato (equivalente exacto a permutar la etiqueta dentro del quipu). 5 000 permutaciones; con ese número, **p=0,0002 es el mínimo resoluble** y debe leerse como p<0,0005.
- **Permutaciones** para proporciones, correlaciones, bandas de color, primera cuerda, etiquetas, totales y emparejamiento. Semilla fija `20261018`.
- **Corrección múltiple:** Holm y Benjamini–Hochberg sobre las 24 pruebas con p-valor (32 filas en `hipotesis.csv`, 8 sin prueba posible). Dos filas (Howard y Urton cap. 8) comparten la misma prueba tripartita, así que el número efectivo de pruebas independientes es 23; la corrección con m=24 es ligeramente conservadora. Se reportan ambos q.
- **Réplica:** los resultados estructurales principales se replicaron en OKR (tabla 6).

### 2.2 Limpieza

- Color: se eliminaron los rangos en cm con `re.sub(r'\([^)]*\)', '', s)` antes de contar; se trabajó con la **familia cromática** (primer código antes de `:`, `-`, `/`).
- Torsión y unión: se excluyeron `U`, `Unknown`, `?` y `T` cuando el test era S/Z o R/V.
- Dirección de nudo: se parseó de `nudos` (`...(... ,S/Z),valor`); una cuerda es `S` o `Z` si todos sus nudos van en esa dirección; las mixtas se excluyeron.
- **Nudo largo “narrativo”:** se definió como 10–20 vueltas de un nudo `L`. KFG codifica a veces centenas/millares como `100E`, `600L`, etc.; esos valores no son vueltas físicas y se excluyeron. Defino `L10` así en todo el informe.
- **No se usaron fibra ni grosor** (dependen del transcriptor), ni la procedencia de museo como lugar de origen.
- **Validez decimal:** una cuerda es válida si sus racimos, leídos de arriba abajo, tienen valores de la forma *d*·10^p (d=1..9) y lugares estrictamente decrecientes. Es una medida conservadora: penaliza tanto errores de transcripción como usos no decimales.

### 2.3 Advertencia sobre el volumen

El volumen tiene **13 capítulos**, no los autores que a veces se le atribuyen. **Brokaw, Niles, Rappaport, Julien y Cummins no están en *Narrative Threads* 2002** (pertenecen a *Their Way of Writing*, 2011, y a otras obras). Se reseñan los 13 que sí están.

---

## 3. Los capítulos: tesis, evidencia e hipótesis

### 3.1 Urton, “An Overview of Spanish Colonial Commentary…” (cap. 1)

**Tesis:** las fuentes coloniales sobre el quipu no son un bloque: hay que leerlas cronológicamente. Los testimonios de la primera generación (Cieza, Polo, Acosta) describen un quipu prehispánico vivo; los tardíos (Calancha, Cobo) hablan de una tradición ya transformada y sospechosa. Urton sostiene que el quipu registraba información numérica **y** narrativa, y que la mezcla ahistórica de citas ha distorsionado la discusión.

**Evidencia:** crónicas, visitas y juicios; no hay cuerdas en el capítulo.

**Hipótesis comprobables:** (i) una subclase de quipus viola las reglas decimales (probada en 4.3); (ii) los rasgos estructurales varían por región (probada en 4.6; la variación temporal no es testeable con KFG); (iii) el vocabulario colonial cambia con el tiempo (no testeable con cuerdas).

### 3.2 Howard, “Spinning a Yarn…” (cap. 2)

**Tesis:** las narraciones quechuas de Huamalíes se organizan por repetición, encadenamiento y anclaje en el paisaje; la memoria no es un texto almacenado sino una performance. Si el quipu servía para recitar, su estructura debería parecerse más a un guion repetitivo que a una prosa lineal.

**Evidencia:** corpus oral recogido por la autora en San Pedro de Pariarca (Huánuco), analizado con teorías de la memoria (Bartlett, Yates) y de la oralidad.

**Hipótesis comprobable:** sobrerrepresentación de estructuras tripartitas/repetitivas en las cuerdas. **Prueba:** 8,6% de las cuerdas tienen exactamente 3 racimos; 3 quipus combinan ≥50% de cuerdas con 3 racimos y nudos largos 10–20 (UR193, KH0001, AS090_N2); rho=0,13, p=0,003. Es un apoyo débil, no una confirmación de la estructura narrativa.

### 3.3 Conklin, “A Khipu Information String Theory” (cap. 3)

**Tesis:** el orden de construcción es el orden de la información: cordón principal → cuerdas secundarias → terciarias → nudos. El cordón principal “anuncia” el quipu por material, color y plying; las cuerdas superiores resumen grupos; la torsión, el plying y el color son información de primer nivel, anterior a los nudos. El quipu sería una “carta”, no solo un mnemónico privado.

**Evidencia:** análisis técnico de piezas (AMNH B/8705, 7604/P.C.), fotografías, comparación con telares y puentes colgantes; cálculo de capacidad informativa (~23 bits por cuerda secundaria).

**Hipótesis comprobables:** (i) la cuerda superior es la suma del grupo (probada, 4.3); (ii) el color del cordón principal predice la paleta (probada, 4.2); (iii) torsión/plying codifican información por cuerda (negativa, 4.1); (iv) grupos de 5, 6 o 10 (negativa, 4.5).

### 3.4 Marcia Ascher, “Reading Khipu: Labels, Structure, and Format” (cap. 4)

**Tesis:** los números pueden ser magnitudes o **etiquetas** (DNI, teléfono, código postal); el quipu usa ambos. La estructura —espaciado, color, niveles, dirección— es un “formato” que hay que reconocer antes de leer los datos. Dos quipus pueden contar la misma historia con datos distintos (AS69/AS70).

**Evidencia:** 215 quipus estudiados en 34 museos; análisis lógico-matemático; ejemplos AS69, AS70, AS101.

**Hipótesis comprobables:** (i) los valores iniciales de grupo se repiten más que los valores aleatorios (probada, 4.5); (ii) los quipus emparentados comparten formato/paleta (probada con pares A/B, 4.4); (iii) color y espaciado codifican estructura (probada, 4.2).

### 3.5 Robert Ascher, “Inka Writing” (cap. 5)

**Tesis:** los incas sí tenían escritura; el quipu es un sistema semasiográfico, no glotográfico. La oposición oral/letrado es etnocentrista; la escritura no exige representar sonidos.

**Evidencia:** comparación con sistemas de escritura, el episodio de Cajamarca, la imprenta de Gutenberg; argumentación teórica.

**Hipótesis comprobable:** la estructura produce significado independiente de los valores. No es falsable con KFG sin un experimento de formato; queda como propuesta interpretativa.

### 3.6 Assadourian, “String Registries…” (cap. 6)

**Tesis:** el quipu es un registro contable y de memoria; los cronistas describen registros de tributos, censos y bienes, con colores que significan categorías. La memoria histórica se transmitía oralmente alrededor del quipu, no solo en él.

**Evidencia:** Zárate (1555), Cieza, Polo, Garcilaso, Calancha; reconstrucción de la tradición de Blas Valera.

**Hipótesis comprobable:** predominio del sistema decimal. **Prueba:** 62,5% de 28 457 cuerdas evaluables son decimalmente válidas; la mediana por quipu es 1,0 y 391 de 636 quipus (61,5%) tienen todas sus cuerdas evaluables válidas. Las violaciones se concentran en 26 quipus (ver 4.3).

### 3.7 Hyland, “Woven Words: The Royal Khipu of Blas Valera” (cap. 7)

**Tesis:** los documentos de Nápoles (*Historia et Rudimenta Linguae Piruanorum*) describen un quipu “real” silábico, con símbolos tejidos que representan sílabas quechuas, atribuido a Blas Valera. Hyland defiende la autenticidad de la tradición y su valor para repensar el quipu como escritura.

**Evidencia:** manuscritos de Nápoles, Montesinos, archivos jesuitas; debate con Estenssoro y los Domenici.

**Hipótesis comprobable:** presencia de signos no numéricos con valor fonético. **No hay datos en KFG**; los quipus con iconografía tejida no están en el corpus. Queda como especulativa, no como refutada.

### 3.8 Urton, “Recording Signs in Narrative-Accounting Khipu” (cap. 8)

**Tesis:** existe una clase de quipus “narrativo-contables” que usan el repertorio decimal pero lo reorganizan: cuerdas con **tres subunidades** (racimos), nudos largos de más de 9 vueltas (hasta 16), nudos largos en posición alta y unidades tripartitas que podrían ser logogramas o unidades semasiográficas. Es el antecedente directo de *Signs of the Inka Khipu* (2003), donde Urton formaliza las oposiciones binarias.

**Evidencia:** cuatro quipus (AMNH B/8705, British Museum, Múnich), transcripción de 153 cuerdas de B/8705: 87% con tres subunidades; largos de hasta 16 vueltas.

**Hipótesis comprobables:** (i) 3 racimos por cuerda en una subclase (probada, débil); (ii) nudos largos 10–20 (probada); (iii) nudo largo arriba de nudos simples (probada); (iv) código binario combinatorio (negativa, 4.2); (v) modelado contra un texto quechua (nunca hecho).

### 3.9 Quilter, “Yncap Cimin Quipococ’s Knots” (cap. 9)

**Tesis:** no hubo un solo sistema imperial: hubo diversidad y estandarización parcial. La lectura estaba restringida a los khipukamayuq, pero Garcilaso aprendió a leer cuentas; ambos testimonios pueden ser ciertos si coexistían tradiciones locales. Compara el quipu con el telégrafo, la estenografía y los tokens del Cercano Oriente.

**Evidencia:** crónicas, etnografía, arqueología; estudio previo de Urton (1994) en 99 quipus de Berlín, sin patrones regionales claros en tipos de nudo.

**Hipótesis comprobable:** los rasgos estructurales varían por procedencia. **Prueba:** eta² por sitio: unión 0,021; torsión 0,041; nudo S 0,027 (p=0,001); color 0,002 (p=0,13). La diversidad estructural existe; la composición de color no varía por sitio.

### 3.10 Platt, “Without Deceit or Lies” (cap. 10)

**Tesis:** en el juicio de restitución de tributos del siglo XVI, los chinu (quipus aimaras) se leen de forma variable: el color que en una provincia significa plata en otra significa otra cosa. El quipu no es fonográfico, pero puede contener rebus y elementos semasiográficos.

**Evidencia:** expediente judicial, visitas, lexicografía aimara; comparación con los quipus de pastores.

**Hipótesis comprobable:** la asociación color–valor difiere entre sitios. **Prueba:** interacción color×sitio 0,010 vs 0,0042 nulo, 201 celdas, p=0,0005. Apoyo con datos, con la cautela de que “significado” y “distribución de valores” no son lo mismo.

### 3.11 Harrison, “Pérez Bocanegra’s *Ritual formulario*” (cap. 11)

**Tesis:** el quipu se usó en la confesión cristiana para enumerar pecados; Pérez Bocanegra (1631) lo describe y lo combate. Hay una continuidad técnica entre el quipu andino y el rosario, y una transformación colonial del uso.

**Evidencia:** *Ritual formulario*, sermones de Acosta, dibujo de Guaman Poma, catecismos.

**Hipótesis comprobable:** cuerdas con categorías de pecado y valores repetidos. **No hay quipus de confesión identificados en KFG.** Especulativa.

### 3.12 Salomon, “Patrimonial Khipu in a Modern Peruvian Village” (cap. 12)

**Tesis:** los *quipocamayos* de Tupicocha (Huarochirí) son documentos patrimoniales vivos, no fósiles incas. Se exhiben por pares, uno por cada autoridad de la parcialidad; el par 1SF-01/2SF-01 tiene plying opuesto (S vs Z). El color se organiza en bandas; hay nudos no canónicos y cuerdas móviles, lo que sugiere un dispositivo **operativo**, no solo un archivo. Los quipus no serían “textos” acumulativos sino esquemas de un ciclo político.

**Evidencia:** trabajo de campo 1995–2000; 10 especímenes; radiocarbono 1650–1950; microscopía de fibras; entrevistas.

**Hipótesis comprobables:** (i) pares con unión/torsión opuesta (probada, negativa frente al nulo); (ii) color en bandas (probada, positiva); (iii) nudos no decimales (probada, positiva); (iv) pares A/B son mitades de la misma obra (probada, positiva por contenido).

### 3.13 Mackey, “The Continuing Khipu Traditions” (cap. 13)

**Tesis:** los quipus de pastores modernos usan seis principios: posición del nudo, grosor, racimos de diez, vueltas, primera cuerda y “zonas contables”. El principio que sobrevive del quipu inca es la posición; el color rara vez codifica la categoría del objeto y más bien marca el inicio o el grupo.

**Evidencia:** 43 quipus etnográficos de Paucartambo, Sicuani y Taquile; entrevistas con pastores.

**Hipótesis comprobables:** (i) el color marca la primera cuerda (probada, efecto pequeño); (ii) el color no codifica la categoría (apoyada indirectamente); (iii) la posición determina el valor (apoyada por la validez decimal).

---

## 4. Resultados

### 4.1 El “código binario”: poca capacidad, no un alfabeto de 7 bits

La propuesta de Urton (2003) es que el quipu combina oposiciones binarias (material, torsión, dirección de nudo, fijación, color, etc.). En KFG solo cuatro están disponibles de forma sistemática: torsión S/Z, unión R/V, dirección de nudo S/Z y color marcado/no marcado. Resultados:

**a) Casi todos los rasgos son constantes dentro de cada quipu.** Pureza mediana (proporción de la categoría mayoritaria entre las cuerdas del quipu):

| rasgo | pureza mediana | quipus con las dos categorías |
|---|---:|---:|
| torsión S/Z | 1,00 | 28 / 511 |
| unión R/V | 1,00 | 159 / 445 |
| dirección de nudo S/Z | 1,00 | 208 / 484 |
| color marcado/no marcado | 0,968 | 364 / 642 |

La torsión es el caso extremo: 44 965 cuerdas S frente a 3 398 Z (93% / 7% de las conocidas); solo 28 quipus tienen variación interna. **La torsión no es un signo por cuerda: es una marca de quipu/archivo.** Se concentra en Armatambo (100% Z), Nazca (100%), Chuquitanta (61%), Ocucaje (47%) e Incahuasi (20%); en la mayoría de los sitios es S.

**b) Las combinaciones realizadas son pocas.** En 386 quipus con ≥5 cuerdas y los cuatro rasgos conocidos, la mediana es **2 combinaciones de 16 posibles**; 78 quipus tienen **una sola** combinación y solo 21 llegan a ≥6. La información mutua mediana entre los cuatro rasgos es **0,00 bits**.

**c) Pero no hay redundancia fuerte: en conjunto, la combinatoria es compatible con independencia.** Al permutar cada rasgo por separado dentro de cada quipu (nulo de independencia; 351 quipus con ≥8 cuerdas), el número medio de combinaciones es 2,83; el observado es 2,80 (p=0,99 unilateral). Es decir: **los rasgos no co-varían como un código redundante, pero tampoco exploran el espacio combinatorio**, porque cada uno está casi fijo. La entropía mediana de la combinación realizada es **0,86 bits**; la capacidad efectiva es de ~1–2 bits por cuerda, no de 7.

**d) Asociaciones pairwise.** Solo dos sobreviven:

- **Torsión Z × color marcado:** OR=0,12; 18 de 22 quipus en dirección negativa; p=0,0002. Es robusto al excluir Arica y Chachapoyas, pero se apoya en solo 22 quipus (los únicos donde ambos rasgos varían) y la torsión Z está concentrada en pocos sitios. Interpretación aburrida: las cuerdas Z son un lote de fibra/color distinto, no un bit semántico.
- **Nudo S × unión V:** OR=1,39 en KFG (nivel de cuerda agregada); 65/58 quipus; p=0,0002. Al nivel de nudo y estratificando por quipu×tipo, OR=2,03 (124 estratos) y sobrevive a añadir la posición decimal. En OKR se replica con OR=2,17 (por quipu) y 3,35 (por quipu×tipo). **Pero la asociación es heterogénea por sitio:** Incahuasi OR=3,1 (5 estratos), Santa 6,2 (1), Ica 0,82 (3) y **Pachacamac 0,17 (9 estratos, dirección opuesta)**. Es una tendencia local/archivo, no una regla universal, y su significado es desconocido.

**e) Independencias (resultados negativos).** Unión V × color: OR=0,95, p=0,54. Nudo S × color: p=0,10. Torsión Z × unión V: p=0,017 pero solo 9 quipus (2/7), frágil y no sobrevive a Holm. Torsión Z × dirección de nudo: p=0,27.

**Conclusión:** no hay un “código de 7 bits” por cuerda en el sentido fuerte (un alfabeto combinatorio). Hay **unas pocas convenciones locales** (unión, color, dirección de nudo) y una enorme cantidad de rasgo constante por quipu. La capacidad semántica, si existe, no está en la combinatoria de bits, sino en el color multivaluado (mediana de 4 familias por quipu; 56% de cuerdas en el color dominante) y en la estructura de grupos.

### 4.2 El color es sintaxis, no un léxico simple

- **Bandas:** la proporción de cuerdas adyacentes del mismo color es **0,598** frente a **0,445** del nulo que permuta colores dentro del quipu (633 quipus; p=0,001). El color se usa en bloques contiguos, como una segmentación.
- **Primera cuerda:** en 3 159 grupos con ≥3 cuerdas y ≥2 colores, la primera cuerda difiere del color modal del resto en **66,95%** de los casos, frente a **64,17%** si se elige una cuerda al azar (p=0,0005). El efecto es real pero pequeño (+2,8 puntos porcentuales): el color **ayuda** a marcar el inicio, no lo determina.
- **Significado variable:** la interacción color×sitio sobre el rango del valor es 0,010 frente a 0,0042 del nulo (30 sitios, 19 colores, 201 celdas; p=0,0005). La composición de color **no** varía por sitio (eta²=0,002; p=0,13), pero la asociación color–valor sí. Esto apoya la observación de Platt: el color no tiene un léxico universal.
- **Color del cordón principal:** los quipus con cordón principal cromático tienen 26,2% de colgantes cromáticos frente a 10,2% si el cordón es neutro (649 quipus; p=0,0005). El efecto sobrevive dentro de sitio (4/4 sitios con ambos tipos, diferencia media +0,22) y en los cinco quintiles de tamaño (positivo en 5/5, media +0,15; p=0,0005): el cordón principal “anuncia” la paleta, como quería Conklin.

### 4.3 Contabilidad: la cuerda superior y la subclase no decimal

- **Cuerda superior = suma del grupo anterior:** 26 de 76 cuerdas T (34,2%) igualan exactamente la suma del grupo previo, frente a **15,5%** del nulo que toma la suma de un grupo al azar del mismo quipu (p=0,0002). Si se admite el grupo siguiente, 30/76. Los 14 quipus con coincidencias incluyen AS001, AS002, AS003, AS004, AS006, AS007, AS072, QU003, QU009, QU012, QU014, QU015, QU016, QU019. Es el resultado más limpio del volumen: **la cuerda superior es un total**, aunque no en todos los casos (posiblemente por grupos mal segmentados o cuerdas perdidas).
- **Validez decimal:** 26 075 de 28 457 cuerdas evaluables (62,5%) son decimalmente válidas; la mediana por quipu es 1,0 y 391/636 quipus (61,5%) son 100% válidos. El sistema decimal es dominante pero no universal: 26 quipus concentran la mayor parte de las violaciones.
- **Subclase narrativo-contable:** 198 cuerdas en 39 quipus tienen nudos largos de 10–20 vueltas; en los 29 quipus con ≥5 cuerdas evaluables, la regularidad decimal es **0,659** frente a **0,941** del resto (p=0,0005). El efecto **no es circular**: al excluir las propias cuerdas con nudo largo, el resto de esas mismas cuerdas sigue siendo menos decimal (0,666 vs 0,941; p=0,0005). Además, la inversión “nudo largo arriba de nudos simples” aparece en 6,9% de las cuerdas de esos quipus frente a 0,4% en el resto (p=0,0005).
- **Candidatos a “narrativo-contables”:** UR193 (96,5% de cuerdas con 3 racimos), KH0001 (82,5%) y AS090_N2 (60,3%), todos con nudos largos 10–20. El quipu B/8705 de Urton no está en KFG, pero el patrón estructural sí se replica en estos tres.

### 4.4 Pares A/B y el patrón de Incahuasi

Se identificaron 14 pares A/B con ≥10 cuerdas (mitades de catálogo, probablemente mitades físicas de una misma obra). **Seis** tienen unión opuesta (≥70% V en una mitad y ≤30% V en la otra): HP046, UR056, UR117, UR267, UR273 y UR274. Los tres de Incahuasi son perfectos: UR267A 100% V / UR267B 0% V; UR273A 100% V / UR273B 1% V; UR274A 99% V / UR274B 0% V.

**Frente al nulo:** el 28,1% de los pares controles del mismo sitio y tamaño comparable también son opuestos (DE 0,111); 6/14 = 42,9%, p=0,162. Frente a la tasa global de pares mismo sitio (592/1 690 = 35,0%), Fisher p=0,58. **El patrón no es estadísticamente excepcional**: la unión R/V ya está fuertemente estructurada por sitio (Incahuasi tiene 14 quipus V-dominantes y 27 R-dominantes; otros sitios son casi todos V o casi todos R), de modo que dos quipus cualesquiera del mismo sitio y tamaño tienen una probabilidad alta de ser opuestos por azar.

Los tres pares perfectos de Incahuasi dan p=0,043 sin corregir (3/3 frente a 35%), pero no sobreviven a la corrección ni al nulo por sitio. **Conclusión: el patrón existe, pero no se demuestra que sea un emparejamiento deliberado.** Lo que sí es fuerte es que los pares A/B son mitades de la misma obra: comparten paleta (Jaccard 0,531 vs 0,268; p=0,0007) y sus totales son más parecidos (razón 0,463 vs 0,244; p=0,0033). Es decir, el emparejamiento por contenido es real; la oposición de unión puede ser una consecuencia de cómo se fabricaron las dos mitades, no una regla de "dualidad" independiente.

### 4.5 Etiquetas, formato y grupos

- **Valores como etiquetas:** en 399 quipus con ≥4 grupos, el valor más repetido de la primera cuerda de cada grupo aparece en 46,9% de los grupos, frente a 37,8% si se elige una posición al azar (p=0,001). Los primeros valores son más “etiquetarios”, como quería Ascher.
- **Tamaño de grupo:** la moda es 1 cuerda (2 504 de 8 116 grupos); 5=673, 6=670, 10=215. **No hay preferencia por 5, 6 o 10**; la afirmación de Conklin no se sostiene como regularidad del corpus.
- **Diversidad de color:** mediana de 4 familias por quipu (máximo 22); 65 de 617 quipus son monocromos; 56% de las cuerdas están en el color dominante. El color es multivaluado, no un bit.

### 4.6 Diversidad regional: los rasgos estructurales son marcas de archivo

La hipótesis de Quilter (cap. 9) se confirma, pero con una consecuencia incómoda para cualquier lectura semántica: **los rasgos estructurales son, en gran medida, marcas de procedencia.**

| rasgo | eta² por sitio | p | sitios | lectura |
|---|---:|---:|---:|---|
| proporción de unión V | 0,021 | 0,001 | 16 | sitios casi 100% V vs casi 0% V |
| proporción de torsión Z | 0,041 | 0,001 | 16 | Z concentrado en Armatambo, Nazca, Chuquitanta, Ocucaje, Incahuasi |
| proporción de nudo S | 0,027 | 0,001 | 17 | variación por archivo |
| proporción de color marcado | 0,002 | 0,13 | 21 | **no** varía por sitio |

Ejemplos: la torsión Z es 100% en Armatambo y en el valle de Nazca, 61% en Chuquitanta, 47% en Ocucaje y 20% en Incahuasi, pero ~0–1% en Santa, Pachacamac o Ica. La unión V es 0% en Monte de Cacatilla y en el sitio “unknown”, 7% en Playa Miller (Arica), y 100% en Ica/Pisco, Huacho y Huaura. Es decir: **R/V y S/Z funcionan como firmas de taller o región**, no como bits semánticos libres. Cualquier modelo que las use como variables explicativas debe incluir sitio/archivo como factor, o quedará confundido.

---

## 5. Controles

1. **Nulo explícito en todas las pruebas.** Permutación dentro de quipu para rasgos de cuerda; permutación de etiquetas de sitio para eta²; permutación de colores para bandas; permutación de posición para primera cuerda; permutación de cuerdas del mismo quipu para cuerdas superiores; pares controles del mismo sitio y tamaño para A/B. Semilla fija.
2. **CMH** en lugar de chi-cuadrado global: cada quipu aporta su propia tabla 2×2; el nulo es hipergeométrico por estrato. Así no se cuenta 40 000 veces el mismo quipu.
3. **Corrección múltiple.** 24 pruebas con p; **19 sobreviven Holm** y **20 sobreviven BH** a q<0,05. Las que no sobreviven a Holm: torsión×unión (q_Holm=0,084), unión×color (q=1,00), nudo×color (q=0,42), pares A/B opuestos (q=0,49) y el test de combinaciones (q=0,99). De ellas, las tres últimas y el test de combinaciones son resultados nulos o negativos; el único positivo que no sobrevive es torsión×unión.
4. **Control de circularidad en la validez decimal.** El contraste L10 vs resto se repitió excluyendo las cuerdas con nudo largo; el efecto persiste (0,666 vs 0,941).
5. **Control de artefacto de transcripción.** Los nudos largos de 10–20 vueltas se separaron de los valores 100+ que KFG usa para centenas/millares; sin esa separación, el test estaría inflado por 600L/700E.
6. **Control de confusión por sitio.** La torsión y la unión son marcas de sitio; por eso los tests de co-variación se hicieron dentro de quipu. El efecto del cordón principal se replicó dentro de sitio (4/4).
7. **Réplica en OKR.** Torsión: pureza mediana 1,00; solo 23/476 quipus varían. Unión: pureza 1,00; 143/409 varían. Nudo S × unión V: OR=2,17 por quipu y 3,35 por quipu×tipo (misma dirección que KFG).
8. **Límites.** KFG mezcla transcriptores; la dirección de nudo y la unión pueden tener errores; la muestra no es aleatoria (museos); la procedencia de museo no es lugar de origen. Los tamaños de efecto pequeños (primera cuerda, nudo S×unión) no deben convertirse en interpretaciones fuertes.

---

## 6. Resultados negativos (explícitos)

1. **No hay código combinatorio de 7 bits por cuerda.** Mediana de 2 combinaciones de 16; 78/386 quipus con una sola; MI mediana 0; las combinaciones observadas igualan el nulo de independencia (2,80 vs 2,83).
2. **La torsión no es un signo por cuerda.** 93% S; solo 28/511 quipus varían; es marca de sitio/archivo.
3. **El emparejamiento con unión opuesta no supera el nulo.** 6/14 vs 28,1% (p=0,162); Fisher vs tasa global p=0,58. Los tres pares perfectos de Incahuasi no bastan tras corrección.
4. **No hay preferencia por grupos de 5, 6 o 10.** Moda=1; 5=673, 6=670, 10=215 de 8 116.
5. **Unión y color son independientes** (OR=0,95; p=0,54); **dirección de nudo y color** también (p=0,10).
6. **La composición de color no varía por sitio** (eta²=0,002; p=0,13), aunque su asociación con el valor sí.
7. **La “primera cuerda” tiene un efecto de color real pero minúsculo** (+2,8 pp). Es consistente con Mackey, pero no convierte al color en un marcador fuerte de inicio.
8. **No se puede probar la hipótesis silábica de Hyland ni la de confesión de Harrison** con KFG: no hay quipus con iconografía tejida ni contextos de confesión en el corpus.

---

## 7. Nivel de evidencia

| Afirmación | Nivel | Base |
|---|---|---|
| El sistema decimal de posición es dominante en el corpus | **Bien apoyado** | 62,5% de cuerdas válidas; mediana por quipu 1,0; literatura Locke/Ascher |
| La cuerda superior suma el grupo anterior | **Apoyado con datos (fuerte)** | 26/76 exactos vs 15,5% nulo de sumas de grupo; p=0,0002 |
| Existe una subclase “narrativo-contable” con nudos largos 10–20, orden invertido y menor regularidad decimal | **Apoyado con datos** | 198 cuerdas en 39 quipus; en los 29 con ≥5 cuerdas evaluables, 0,659 vs 0,941; control sin las cuerdas L; p=0,0005 |
| El color se organiza en bandas y marca la primera cuerda | **Apoyado con datos** | 0,598 vs 0,445; 66,95% vs 64,17% |
| El cordón principal anuncia la paleta | **Apoyado con datos** | 0,262 vs 0,102; sobrevive dentro de sitio |
| Los números se usan como etiquetas | **Apoyado con datos** | 0,469 vs 0,378 |
| Los pares A/B son mitades de la misma obra | **Apoyado con datos** | Jaccard 0,531 vs 0,268; totales 0,463 vs 0,244 |
| La asociación nudo S × unión V es una convención real | **Propuesto (asociación global, heterogénea por sitio)** | OR=1,39 KFG; 2,03 por tipo; OKR 2,17–3,35; pero Pachacamac invierte (OR=0,17) |
| El color tiene significados variables por sitio | **Propuesto** | Interacción p=0,0005, pero “valor” no es “significado” |
| La estructura tripartita refleja narrativa quechua | **Propuesto** | rho=0,13; 3 candidatos; solo analogía |
| El quipu es escritura semasiográfica | **Propuesto** | Argumento teórico, no falsable con KFG |
| El quipu fue dispositivo operativo en Tupicocha | **Propuesto** | Etnografía y radiocarbono; no hay test en corpus antiguo |
| El quipu “real” silábico de Blas Valera | **Especulativo** | Documentos disputados; sin cuerdas |
| El quipu de confesión | **Especulativo** | Solo fuentes textuales |
| Un código de 7 bits por cuerda | **No apoyado; refutado en su versión fuerte (4 de 7 rasgos disponibles)** | 2/16 combinaciones; independencia; baja entropía |

---

## 8. Qué sigue vivo, qué cae, qué nadie probó

**Siguen vivas (con datos):**
- La cuerda superior como total (Conklin/Ascher).
- El color como sintaxis: bandas, primera cuerda, paleta anunciada por el cordón principal (Ascher, Salomon, Mackey, Conklin).
- La existencia de una subclase no decimal con nudos largos anómalos (Urton cap. 8).
- La diversidad regional de los rasgos estructurales (Quilter).
- La variabilidad del color por sitio (Platt).
- Los números como etiquetas y el formato como información (Ascher).

**Caen o quedan muy debilitadas:**
- El código binario combinatorio de 7 bits por cuerda (Urton 2003): la capacidad realizada es de ~2 combinaciones, no 16; los rasgos son casi constantes por quipu.
- La torsión como signo por cuerda: es marca de archivo/sitio.
- El emparejamiento deliberado con unión opuesta: el patrón existe pero no supera la tasa base; lo bien apoyado es que los pares A/B son mitades de la misma obra.
- Los grupos de 5/6/10 como principio organizador.
- El color como codificación simple de categorías de objetos (Mackey ya lo negaba para los quipus modernos; aquí tampoco aparece un léxico universal).

**Nadie ha probado todavía (ni en 2002 ni ahora):**
- La comparación de los quipus narrativo-contables con un texto quechua (el propio Urton la propone y dice que “nunca se ha intentado”).
- La hipótesis silábica de Hyland con cuerdas arqueológicas.
- El uso confesional de Harrison con un corpus identificado.
- La tesis semasiográfica de R. Ascher con un experimento de formato.
- La hipótesis operativa de Salomon en quipus prehispánicos (solo hay etnografía moderna).
- La cronología de las fuentes de Urton cap. 1 con un análisis cuantitativo de vocabulario.

---

## 9. Para el coordinador

- **El resultado más sólido del volumen es la cuerda superior como total:** 26/76 igualdades exactas con el grupo previo frente a 15,5% del nulo de sumas de grupo (p=0,0002), en 14 quipus. Es el único caso donde el quipu “dice” una operación aritmética verificable.
- **El “código de 7 bits” no existe como alfabeto por cuerda.** La mediana es 2 combinaciones de 16; 78/386 quipus tienen una sola; la información mutua mediana es 0. En conjunto, la combinatoria no se aparta de la independencia (2,80 vs 2,83), pero casi no varían dentro del quipu: la capacidad efectiva es ~1–2 bits, no 7.
- **La torsión no es un signo por cuerda:** 93% S, solo 28/511 quipus varían, y el Z se concentra en Armatambo, Nazca, Chuquitanta, Ocucaje e Incahuasi. Sirve para discriminar archivos/regiones, no para leer cuerdas.
- **El color es sintaxis, no léxico:** bandas (0,598 vs 0,445), primera cuerda (66,95% vs 64,17%, efecto +2,8 pp) y cordón principal que anuncia la paleta (0,262 vs 0,102, replicado dentro de sitio). Su asociación con el valor cambia por sitio (p=0,0005), como decía Platt.
- **Existe una subclase narrativo-contable:** 198 cuerdas en 39 quipus con nudos largos de 10–20 vueltas; en los 29 con ≥5 cuerdas evaluables, regularidad decimal 0,659 vs 0,941, y el efecto persiste al excluir esas cuerdas (0,666 vs 0,941). Candidatos: UR193, KH0001, AS090_N2. El B/8705 de Urton no está en KFG, pero el patrón se replica.
- **El patrón de Incahuasi es real pero no excepcional:** UR267A/B, UR273A/B y UR274A/B son perfectamente opuestos (V vs R), pero 6/14 pares A/B lo son frente a 28,1% del nulo (p=0,162) y 35,0% de todos los pares mismo sitio (Fisher p=0,58). Lo que sí está apoyado con datos es que los pares A/B son mitades de la misma obra (Jaccard 0,531 vs 0,268; totales 0,463 vs 0,244).
- **Los grupos de 5/6/10 no son un principio del corpus:** moda=1; 5=673, 6=670, 10=215 de 8 116 grupos. La afirmación de Conklin cae como regularidad; puede seguir siendo una elección local en casos concretos.
- **19 de 24 pruebas sobreviven Holm; 20 sobreviven BH.** Los resultados nulos (unión×color, nudo×color) y los pares opuestos no alcanzan significación; el único positivo que no sobrevive a Holm es torsión×unión (p=0,017 con solo 9 quipus).
- **Ojo con la asociación nudo S × unión V:** es global (OR=1,39; p=0,0002) y se replica en OKR (2,17–3,35), pero **no es universal**: en Pachacamac se invierte (OR=0,17). No usarla como regla pancorporal.
- **Recomendación inmediata:** (i) atacar los tres candidatos narrativo-contables con transcripción fina y, si se puede, un texto quechua; (ii) buscar en catálogos de museo más pares A/B con metadata de mitad física, que es el diseño natural para probar el emparejamiento; (iii) dejar de tratar torsión y unión como bits por cuerda y tratarlas como marcas de archivo/sitio en cualquier modelo; (iv) probar el color como sistema multivaluado (familias + posición + banda), no como binario marcado/no marcado.

---

## 10. Reproducibilidad

Scripts en `analisis/ds/n_narrative_threads/`:

| script | contenido |
|---|---|
| `prep.py` | carga, limpieza de color, parseo de nudos, funciones de permutación/Holm/BH |
| `binarios.py` | CMH de pares de rasgos binarios |
| `tests.py` | pruebas principales (pureza, CMH, bandas, primera cuerda, etiquetas, cuerdas superiores, triadas, sitio) |
| `controles.py` | controles de torsión×color y nudo×unión por tipo/posición |
| `codigo.py` | combinaciones, validez decimal, cordón principal, tamaños de grupo |
| `combos.py` | combinaciones observadas vs nulo de independencia |
| `pares.py` | pares A/B, nulo por sitio/tamaño, similitud de contenido |
| `color_sitio.py` | interacción color×sitio |
| `okr_replica.py` | réplica en OKR (solo lectura) |
| `make_hipotesis.py` | construye `hipotesis.csv` y aplica Holm/BH |

Resultados intermedios: `resultados_principales.csv`, `resultados_cmh.csv`, `pureza_rasgos.csv`, `codigo_combinaciones.csv`, `hipotesis.csv`, `log_tests.txt`, `log_pares.txt`.

**Nota:** no se creó ni modificó ningún `khipu.db`; OKR se abrió con `mode=ro`. No se hicieron commits.
