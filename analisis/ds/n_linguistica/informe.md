# Lingüística de la contabilidad andina: léxico, clasificadores y sílabas para un desciframiento por plantillas

**Equipo:** n_linguistica · **Fecha:** 18/10/2026 · **Semilla:** 20261018

---

## 1. Pregunta

¿Qué categorías lingüísticas y contables pueden nombrarse con seguridad en los quipus, y qué predicciones medibles se siguen de dos hipótesis rivales: (a) el quipu usa **etiquetas de categoría** (clase de lo contado, oficio, unidad) y (b) el quipu codifica **sílabas** (logosilabismo, Hyland 2017)? El objetivo operativo es preparar un desciframiento por plantillas: un léxico de unidades y operaciones, un inventario de clasificadores numerales, la fonología silábica de las lenguas relevantes y listas de nombres propios que un quipu tendría que registrar.

## 2. Método y datos

### 2.1 Fuentes lingüísticas

- Diccionarios coloniales: Santo Tomás 1560 (quechua), González Holguín 1608 (quechua), Bertonio 1612 (aimara), Carrera 1644 (mochica/yunga). Para Carrera usé la edición de Villarreal (1921), que reproduce el *Arte* y cuya sección VIII ("Numeración") está disponible en texto completo; las páginas citadas son de esa edición.
- Manuscrito de Huarochirí (ca. 1608), edición bilingüe de Arguedas (texto djvu de archive.org). Extraje el bloque quechua con un clasificador Naive Bayes de n-gramas de caracteres entrenado con líneas de alta confianza (2.302 líneas castellanas y 2.315 quechuas). Resultado: **2.829 líneas quechuas, 151.915 caracteres, 19.225 tokens (19.145 palabras usables)**; el texto castellano de la misma edición (2.805 líneas, 56.958 sílabas) se usó como control negativo.
- Corpus aimara moderno ya presente en el repo (`analisis/ds/n_descifrado_lm/corpus/aymara.txt`, 300.000 caracteres) sólo como control tipológico, no como fuente colonial.
- Etnohistoria: Rostworowski, *Costa peruana* (pachacas, ayllus, curacas), Murra 2024 (pesos y medidas), Barraza et al. 2022 (tablas 1 y 2 de términos contables), Hyland 2017 (Collata), Urton 2003/2017.

### 2.2 Datos de quipus

`analisis/datos/cuerdas.csv` (57.818 cuerdas, 651 quipus). Unidad de análisis: **el quipu**. Se excluyeron las cuerdas con `nudos` vacío (valor 0 no es un cero real). El color se redujo al primer código base (`W:AB` → `W`); esto preserva la categoría dominante pero pierde el barber pole, lo que se declara como limitación. La torsión se restringió a S/Z y la unión a R/V/T; "U", "Unknown" y "?" se trataron como ausentes.

### 2.3 Controles

Para cada prueba de estructura de grupos usé un nulo que **permuta la etiqueta dentro de cada quipu**, preservando la composición de colores/torsiones/uniones de cada quipu y los tamaños de grupo. Estadístico: segregación por grupo `(O−E)/(P−E)`, donde 1 = grupos puramente monocromáticos y 0 = reparto aleatorio. P-valor empírico con 400 permutaciones; corrección de Holm sobre cuatro pruebas. Para sílabas, el nulo de bigramas baraja el segundo miembro de cada bigrama (preserva frecuencias y número de bigramas), 300 permutaciones. Todos los scripts están en esta carpeta; se ejecutan con `python <script>.py`.

## 3. Resultados

### 3.1 Léxico contable (`lexico_contable.csv`)

**89 entradas** con término, lengua, fuente, glosa, categoría, equivalencia y nota. Distribución: 34 números, 13 unidades de medida, 11 operaciones, 10 colores, 8 registros, 6 partes del quipu, 4 nudos, 3 oficios. Lenguas: 39 quechua, 21 mochica/yunga, 10 aimara, 1 aimara/quechua, 18 español (9 común + 9 técnico).

Términos centrales:

| término | lengua | glosa | categoría | equivalencia |
|---|---|---|---|---|
| `yupay` | quechua | contar, numerar | operación | — |
| `yupana` | quechua | tabla/ábaco de contar | registro | — |
| `chuncachani` | quechua | contar por decenas | operación | — |
| `yayanchani` | quechua | sumar y consolidar cuentas | operación | — |
| `taripani` | quechua | verificar/ajustar cuentas | operación | — |
| `quipuni` | quechua | contar por nudos | operación | — |
| `quipucamayoc` | quechua | contador por nudos | oficio | — |
| `chunka` | quechua | diez | número | 10 |
| `pachak` | quechua | cien; unidad de 100 tributarios | número | 100 |
| `waranqa` | quechua | mil; unidad sociopolítica | número | 1.000 |
| `hunu` | quechua | diez mil | número | 10.000 |
| `tupu` | quechua | medida de tierra/tela | unidad de medida | ≈0,27 ha (88×44 varas) |
| `raki` | quechua | partición, porción, turno | unidad de medida | sin métrica fija |
| `poqcha` | quechua local | porción/turno de agua | unidad de medida | sin métrica; **propuesto, verificar** |
| `costal` | español | saco de transporte | unidad de medida | 1–2 fanegas, variable |
| `carga` | español | carga de hombre/animal | unidad de medida | ≈2 arrobas ≈23 kg, variable |
| `fanega` | español | medida de áridos | unidad de medida | ≈55,5 L |
| `nassop` | mochica | diez monedas/reales | número | 10 |
| `napong` | mochica | diez personas/animales/cosas | número | 10 |
| `nacqoquixll` | mochica | diez frutas/mazorcas | número | 10 |
| `naceess` | mochica | diez días | número | 10 |
| `cala` | aimara | piedra de contar | registro | — |
| `chino` | aimara | piedrecita de cuenta | registro | — |
| `chinoquipatha` | aimara | cuenta señalada por nudos | registro | — |

Dos observaciones de método: (i) `pachak`/`waranqa`/`hunu` son a la vez **numerales** y **unidades sociopolíticas** (pachaca, guaranga), de modo que un quipu puede estar contando personas por unidades de 100/1.000 y no sólo objetos; (ii) las equivalencias de `tupu`, `raki` y `poqcha` son las más frágiles. `tupu` tiene una equivalencia agraria aproximada (≈2.700 m²), pero `raki` y `poqcha` designan porciones de agua sin patrón métrico documentado; `poqcha` ni siquiera aparece en los diccionarios coloniales consultados, por lo que va marcado como propuesto.

### 3.2 Clasificadores numerales mochica/yunga: series distintas según lo contado

Carrera (1644, ed. Villarreal 1921:112–113) es explícito. Su texto, modernizado:

> «si se cuenta moneda, diez es *nassop*; si se cuentan hombres, caballos, cabras, casas y todo lo que no sea moneda, frutas ni días, entonces diez es *napong*; si son frutas, mazorcas, diez es *nacqoquixll*; si se cuentan días, diez es *naceess*.»

Y más adelante:

> «para las centenas es *paleec* y para los millares es *cunö* en los dos primeros sistemas; en el tercer sistema las centenas es *chieeng*.»

> «cuando hay unidades, decenas, centenas y millares se pone entre ellas la partícula *alio*.»

Series documentadas:

| clase de lo contado | 10 | 20 | 30 | 100 | 1.000 |
|---|---|---|---|---|---|
| monedas / reales | na.ssop | pac.ssop | coc.ssop | na.paleec | na.cunö |
| personas, animales, casas, cosas | na.pong | pac.pong | coc.pong | na.paleec | na.cunö |
| frutas / mazorcas | na.cqoquixll | pac.cqoquixll | coc.cqoquixll | na.chieeng | (no documentado) |
| días | na.ceess | pac.ceess | coc.ceess | (no documentado) | (no documentado) |

La formulación de la tarea («`nassop` sólo para días, monedas y fruta») debe precisarse: en Carrera `nassop` es la serie de **monedas**; los días usan `naceess` y las frutas `nacqoquixll`. Lo que hay es una **serie distinta por clase**, no un sufijo único para tres clases.

Carrera añade ejemplos de unidades con sustantivos específicos: `na col mang` "un caballo de maíz", `pac öseen lü` "dos estados de agua", `coc pong cqelä` "treinta gavilanes", `noc ssop xllaxll` "cuarenta reales o patacones". Es decir, el **clasificador está fusionado con el numeral** y la serie se elige por la clase del referente, no por el número.

**¿Pudo un quipu marcar la clase con color, torsión o unión?** Tipológicamente sí: un sistema de clasificadores puede realizarse por un morfema (mochica) o por un rasgo separado (color de la cuerda). Pero la analogía es **tipológica, no histórica**: el mochica es de la costa norte y la mayoría de los quipus del KFG son incaicos/coloniales de otras regiones. La pregunta empírica es si en los quipus las dimensiones no numéricas se comportan como etiquetas de clase.

Pruebas con `cuerdas.csv`:

1. **Homogeneidad de color dentro de grupos.** Si el color marcara la clase de un grupo, los grupos deberían ser monocromáticos. El estadístico de segregación es **0,061** (n=575 quipus; Q1=−0,046, Q3=0,123; 56,8% de quipus con valor positivo; p permutación=0,0025; Holm=0,010). Es positivo pero **débil**: muy lejos de 1.
2. **Unión.** La unión (R/V/T) sí forma bloques: **0,428** (n=164; Q1=0,009, Q3=0,715; 79,4% positivo; p=0,0025; Holm=0,010). Es el único rasgo con comportamiento de marcador de grupo.
3. **Torsión.** Sólo **28 de 651 quipus** tienen S y Z dentro del mismo quipu y grupos con ≥2 cuerdas; el efecto es 0,080 pero la prueba de signos por quipu **no es significativa** (48% positivo, p=0,655). La torsión no puede ser un clasificador general: en la gran mayoría de quipus es uniforme.
4. **Color y magnitud numérica.** El color explica η²=0,171 de la varianza del orden de magnitud, frente a 0,085 del nulo (p=0,0033); controlando por nivel, η²=0,137 en el nivel 0 (28.522 cuerdas, 638 quipus) y 0,137 en el nivel 1. El exceso es de unos **5 puntos porcentuales**: real pero pequeño, y confundido con posición estructural.
5. **¿Inventario de símbolos fusionado?** Si color×torsión×unión formara un alfabeto de signos, las combinaciones observadas serían menos que las esperadas por independencia. Ocurre lo contrario: la razón mediana observado/esperado es **1,07** (n=415 quipus; Q1=1,00, Q3=1,15; sólo 12,5% <1). Las tres dimensiones se combinan casi libremente. Además, la mediana de combinaciones distintas por quipu es **5** (media 5,8; máximo 40) y **sólo 1 de 415 quipus llega a 20 combinaciones**. Un silabario que necesite 20–50 signos no cabe en un quipu contable típico.

Conclusión de esta parte: **apoyado con datos** que la unión marca grupos; **propuesto** que eso corresponda a una clase semántica (la explicación aburrida es que la unión refleja cómo se ató físicamente el grupo); **no apoyado** que el color sea un clasificador de grupo fuerte; **refutado** que la torsión sea un clasificador general.

### 3.3 Fonología y sílabas

#### Quechua central/costeño (Huarochirí, ca. 1608)

Inventario aproximado: vocales /a i u/ (con [e o] como alófonos), consonantes /p t k q/, /tʃ/, /s ʃ x h/, /m n ɲ/, /l ʎ r/, /w j/. No hay series aspiradas/eyectivas en el quechua central; el manuscrito escribe `c/qu` para /k/, `hu` para /w/ y `ñ` para /ɲ/. La correspondencia **l ~ r ~ ll** es un rasgo dialectal del quechua central/costeño (Torero 1970; Cerrón-Palomino 2008). El corpus muestra vacilación directa: escribe `quirca` 29 veces y `quillca` 15 (más `quellca` 3) para *qillqa*, y alterna `llacta` (133) con `racta` (22, probable error de OCR). Es un **indicio ortográfico**, no una prueba fonológica.

Resultados sobre 48.673 sílabas:

| medida | valor |
|---|---|
| palabras usables | 19.145 |
| sílabas | 48.673 |
| tipos silábicos | 1.212 |
| entropía | 6,98 bits |
| CV | 48,33% |
| CVC | 40,24% |
| V | 2,63% |
| VC | 2,40% |
| CVV | 2,08% |
| CCV | 1,41% |
| CVCC | 0,25% |

Las sílabas más frecuentes son `ka` (3.132), `ta` (2.258), `pa` (1.968), `kan` (1.770), `chay` (1.606), `ku` (1.389), `na` (1.369), `pas` (1.096), `man` (981), `cha` (977). Los bigramas más frecuentes son `ku-na` (512), `man-ta` (350), `chay-si` (333), `kar-kan` (325), `ñis-pa` (312), `ru-na` (310), `ka-nan` (257), `ta-pas` (243), `an-cha` (230), `chay-man` (230): son precisamente las cadenas de sufijos y enclíticos del quechua.

El inventario **CV** es de 86 tipos; **26 signos cubren el 90%** de las sílabas CV, **33 cubren el 95%** y 50 el 99%. Es decir, un silabario CV de unas 30–50 unidades sería suficiente para escribir quechua; no es un imposible tipológico.

Control fonotáctico: la información mutua entre sílabas contiguas es **2,90 bits**, frente a **0,99 bits** del nulo que baraja el segundo miembro (p=0,0033, 300 permutaciones). Hay estructura secuencial fuerte. Pero el **control castellano de la misma edición da 4,09 bits** (nulo 1,53): las métricas "lingüísticas" no distinguen quechua de castellano por sí solas; de hecho el castellano tiene más entropía (7,76 vs 6,98) y más MI. Cualquier afirmación del tipo "el quipu tiene propiedades lingüísticas porque su entropía/Zipf se parece al lenguaje" es, por tanto, **no diagnóstica**.

Curva de rarefacción (tipos de sílaba): 500→132; 1.000→194; 2.000→246; 5.000→379; 10.000→501; 20.000→757; 40.000→1.116. El inventario sigue creciendo: el texto es heterogéneo (nombres propios, préstamos, topónimos).

#### Aimara

Inventario: /a i u/ con longitud distintiva; consonantes /p pʰ pʼ, t tʰ tʼ, k kʰ kʼ, q qʰ qʼ, tʃ tʃʰ tʃʼ, s x, m n ɲ, l ʎ, r, w j/. Estructura silábica (C)V(C), sin grupos consonánticos nativos; acento predecible (penúltima). En el control moderno de 68.987 sílabas: CV 49,8%, CVC 24,5%, V 4,8%, CCV 2,7% (préstamos), entropía 8,39 bits. La diferencia con el quechua (CVC 40%) refleja sobre todo la morfología sufijal y la ortografía, no una diferencia radical de estructura.

### 3.4 Nombres propios que un quipu tendría que registrar (`nombres_propios.csv`)

**102 entradas** con nombre, tipo, entidad, fuente, orden documental, segmentación silábica y número de sílabas. Total: 338 sílabas, 119 sílabas distintas, media 3,31 sílabas por nombre (mediana 3). Es decir, un nombre típico ocupa **3–4 posiciones silábicas**: si un quipu escribiera nombres con un signo por sílaba, un nombre ocuparía una secuencia corta de 3–4 cuerdas/nudos, no una sola cuerda.

Contenido:

- **Collique (valle del Chillón), Visita de Martínez Rengifo 1571:** 10 pachacas en orden documental: Chuquiruro, Caxa Chumbi, Vilca Tanta, Vilca Chumbi, Chumbi Guarco, Chumbi Tanta, Carua Guanco, Carua Chumbi, Chinqui Yanga, Chuquitanta. Curacas/principales: Chuquiruro, don Francisco Yaybi, don Hernando Nacar, Francisco Nacar, Rodrigo Asmat; y don Diego Sacllachumbi (guancayos, 1605).
- **Lunahuaná:** 4 guarangas; curacas Lunaguanay, Llaquipa/Llaquixa, Allauca (mitmaq, Mullibamba), don Francisco Llacsaguana, don Diego Allaucan (Pacarán), don Pedro Camaluana (Jucxu); Chuquimancu según Garcilaso. 16 barrios/posibles ayllus (Caltopilla, Paraíso, Caltopa, Lúcumo, Casalla, San Pedro, Catapaya, Con-Con y Ramadilla, Socsi, Paullu, San Jerónimo, Langla, Lunahuaná, Patapampa, Condoray, Uchupampa).
- **Guarco:** 4 guarangas; don Alonso Guarac, don Thomas, don Juan Caruatanta, Llactamala.
- **Huarochirí:** 54 ayllus de la lista de padrones del s. XVIII, agrupados por pueblo: Casta (Yacapar, Yanac, Binquiguamo, Allauca, Guallacocha), Carapoma (Capam, Guari, Collana, Allauca, Julca, Sulca, Callan, Tres Casas, Pariac, Iapani), Collata (Ayna michuy, Huanca yanac, Paucartambo, Mango, Huchu, Vilca, Colca, Mango rraqui, Collata), Chacalla, Santa Eulalia de Apocaya, Huanza, Iris, Jicamarca, Larao, Otao. Añadí los linajes **Alluka** y **Yakapar** que Hyland 2017 propone leer en Collata, marcados como hipótesis.
- **Chincha:** la fuente local no da nombres de pachacas; sólo las tres categorías de 10.000 labradores, 10.000 pescadores y 10.000 mercaderes. Lo registro como **vacío documental**, no lo relleno con nombres de otras regiones.

### 3.5 ¿Logosilábico o etiquetas de categoría? Predicciones medibles

| Predicción | Si es logosilábico | Si son etiquetas de categoría | Resultado en KFG |
|---|---|---|---|
| Tamaño del inventario por quipu | 20–50 signos recurrentes | 3–10 etiquetas | mediana **5** combinaciones; sólo 1/415 ≥20 → **no permite silabario** |
| Frecuencia de signos | Zipf, signos muy frecuentes | pocas etiquetas, muy repetidas | no testeado con signos fonéticos; el inventario es demasiado pequeño |
| Estructura secuencial | bigramas con MI alta, morfología sufijal | dependencia de grupo, no secuencial | MI 2,90 bits (nulo 0,99), pero castellano 4,09 → **no diagnóstico** |
| Longitud de "palabra" | 2–6 signos | 1 etiqueta por grupo | los nombres tienen 3,31 sílabas de media; los grupos KFG tienen mediana de 4 cuerdas → compatible con ambas |
| Marcador de grupo | el signo inicial sería una consonante/sílaba | etiqueta inicial de clase | unión marca grupo (0,43); color apenas (0,06) |
| Coexistencia con números | cuerdas silábicas sin nudos decimales | etiquetas conviven con números | no testeado aquí; Sivan reporta 5,4% de cuerdas "STRING" en OKR |

La conclusión es asimétrica: **los datos no apoyan un silabario general en los quipus contables del KFG**, pero tampoco lo refutan para quipus narrativos postconquista como Collata (que no están en el KFG). Lo que sí refutan es que el color, la torsión y la unión formen por sí solos un alfabeto fusionado: se combinan de forma casi independiente.

## 4. Controles, resultados negativos y límites

### 4.1 Controles

- Nulo de permutación dentro de quipu para color/torsión/unión; 400 permutaciones; p mínimo 0,0025.
- Holm sobre cuatro pruebas: todos los valores corregidos = **0,00998**. Se reportan igualmente los tamaños de efecto, porque con n grande una p pequeña no implica efecto grande.
- Nulo de bigramas: 300 permutaciones; p mínimo 0,0033.
- Control negativo castellano para entropía/MI: **más alto que el quechua**, lo que invalida esos indicadores como prueba de "lenguaje".
- Control por nivel en color-magnitud: η² baja de 0,171 a 0,137; el efecto se mantiene pero es pequeño.

### 4.2 Resultados negativos

1. **Torsión:** no es un clasificador general. Sólo 28/651 quipus tienen S y Z dentro del mismo quipu; la prueba de signos no es significativa (p=0,655). No recomiendo invertir más en torsión como marcador de clase.
2. **Color:** la segregación por grupo es positiva pero débil (0,061). Si el color fuera una etiqueta de clase a nivel de grupo, esperaríamos valores cercanos a 0,4–0,7 como los de unión.
3. **Inventario fusionado:** las combinaciones color×torsión×unión son casi independientes (razón 1,07), no un alfabeto constreñido. La mediana de 5 combinaciones por quipu es demasiado baja para un silabario.
4. **Entropía/MI:** el castellano supera al quechua en ambas; no sirven para decidir si un quipu "parece lengua".
5. **Chincha:** no hay lista de pachacas en la fuente local; no la inventé.
6. **`poqcha`:** no aparece en los diccionarios coloniales consultados; su valor como unidad de agua es local y no verificable con las fuentes de este repo.
7. **Nombre de unidades:** `raki` y `poqcha` no tienen equivalencia métrica; `tupu` sólo aproximada. Cualquier plantilla que los use debe llevar un rango, no un número.

### 4.3 Límites

- El KFG ya viene decodificado; los valores y colores no son observación primaria mía.
- Reduje el color al primer código base; se pierden barber pole y combinaciones.
- Los grupos son espacios físicos en el cordón, no categorías semánticas conocidas.
- La analogía mochica es tipológica; no hay continuidad histórica bien apoyada con los quipus incaicos.
- El corpus de Huarochirí es una edición OCR de 1966; la extracción quechua/castellana es probabilística y la silabificación depende de la normalización ortográfica.
- Las listas de nombres vienen de la compilación de Rostworowski, no de una verificación archivística propia.

## 5. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| El sistema decimal y los términos de cuenta están documentados en diccionarios y crónicas | **bien apoyado** |
| Carrera 1644 describe cuatro series de clasificadores numerales mochica (monedas, animados/cosas, frutas, días) | **bien apoyado** (texto primario, ed. Villarreal 1921) |
| El quechua de Huarochirí tiene estructura silábica CV/CVC y un inventario CV de ~86 tipos, 26 de ellos cubren el 90% de las sílabas CV | **apoyado con datos** |
| La unión marca bloques de grupo en los quipus | **apoyado con datos** (0,43; p=0,0025) |
| El color marca clases de grupo | **propuesto** (0,06; positivo pero débil) |
| La torsión marca clases | **no apoyado / refutado como clasificador general** |
| Los quipus contables del KFG codifican un silabario | **no apoyado** (inventario mediano 5; combinaciones independientes) |
| Los quipus de Collata deletrean ALLUKA/YAKAPAR | **especulativo** (Hyland 2017; sin datos replicables) |
| `poqcha` es una unidad de agua | **propuesto, sin verificar** |

## 6. Predicciones falsables para la siguiente ronda

1. **Marcador de grupo:** si la unión es una etiqueta de clase, la primera cuerda de cada grupo debería tener una unión distintiva y el resto del grupo la misma. Medir la proporción de grupos con "cabecera" y compararla con un nulo que permute el orden dentro del grupo.
2. **Rangos de valor por clase:** si el color/unión marca clase, las cuerdas de una misma clase deberían tener distribuciones de valor más parecidas entre sí que con las de otra clase, dentro del mismo quipu. Test de Kruskal-Wallis por quipu + nulo de permutación.
3. **Plantillas de nombres:** alinear los 102 nombres (3,31 sílabas de media) con secuencias de 3–4 cuerdas en quipus de Huarochirí/Collata; si el logosilabismo es cierto, la distribución de longitudes de secuencia debería concentrarse en 3–4 y los signos finales deberían repetirse como sufijos.
4. **Coexistencia número/texto:** replicar en KFG la distinción de Sivan entre cuerdas decimales y "STRING"; si el canal silábico existe, las cuerdas de texto deberían tener nudos no decimales y una distribución de colores distinta.
5. **Clasificadores mochica:** buscar en quipus de la costa norte (si los hay en el KFG/OKR) una asociación entre color y clase de producto documentada en las visitas; la predicción es que el color sea constante dentro de grupos de un mismo producto y cambie entre productos.
6. **Control de autenticidad:** repetir todo con colores sin colapsar y con las correcciones de Thompson, y reportar si los efectos sobreviven.

## Para el coordinador

- Entregué `lexico_contable.csv` (89 términos: 39 quechua, 21 mochica, 10 aimara, 1 aimara/quechua, 18 español) y `nombres_propios.csv` (102 pachacas/ayllus/curacas/barrios, con segmentación silábica; 338 sílabas, media 3,31 por nombre).
- Carrera 1644 confirma **cuatro series de clasificadores numerales mochica**: `nassop` (monedas), `napong` (personas/animales/cosas), `nacqoquixll` (frutas/mazorcas) y `naceess` (días), con centenas distintas (`paleec` vs `chieeng`) y la partícula `alio`. La analogía con el quipu es tipológica, no histórica.
- En 651 quipus/57.818 cuerdas, la **unión** es el único marcador de grupo fuerte: segregación 0,428, 79,4% de quipus positivos, p=0,0025 (Holm 0,010). El **color** es débil (0,061; 56,8% positivo); la **torsión** no es usable (sólo 28 quipus variables; p=0,655).
- **No hay evidencia de un alfabeto fusionado**: color×torsión×unión se combinan casi independientemente (razón 1,07); la mediana es **5 combinaciones por quipu** y sólo **1 de 415** llega a 20. Un silabario de 20–50 signos no cabe en un quipu contable típico.
- El quechua de Huarochirí da 48.673 sílabas, 1.212 tipos, 48,3% CV y 40,2% CVC; **26 signos CV cubren el 90%** y 33 el 95%. El silabario es tipológicamente viable, pero no está instanciado en el KFG.
- La MI silábica es 2,90 bits (nulo 0,99; p=0,0033), pero el **castellano de la misma edición da 4,09** (nulo 1,53): entropía y MI no son pruebas de "lenguaje". No repetir el argumento de Sivan sin este control.
- El color explica η²=0,171 de la magnitud del valor (nulo 0,085); controlando por nivel baja a 0,137. Es un efecto pequeño, confundido con la posición estructural: no lo vendería como "color = clase".
- Recomiendo tres pruebas concretas: (i) cabeceras de grupo y unión; (ii) rangos de valor por color/unión dentro de cada quipu; (iii) alineación de los nombres de 3–4 sílabas con secuencias de 3–4 cuerdas en quipus de Huarochirí/Collata.
- No gastaría más esfuerzo en torsión como clasificador. Sí pediría los datos crudos de Collata (487 colgantes) para testear la hipótesis logosilábica fuera del KFG, donde la densidad de combinaciones es mayor.
- Todos los scripts y resultados están en `analisis/ds/n_linguistica/`; semilla 20261018; sin commits.
