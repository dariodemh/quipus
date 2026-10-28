# 11_rosetta: las transcripciones coloniales como "piedra de Rosetta" de la estructura de los quipus

**Respuesta corta.**

- **La tesis de Medrano (2019) no trae listas de números.** Es un estudio lingüístico (lemas y categorías gramaticales) de 72 transcripciones de *Textos Andinos* (Pärssinen y Kiviharju). El autor dice expresamente que no estudia el contenido numérico. Solo hay cifras en los fragmentos que cita.
  - De ahí, del padrón del Santa (1670) y de la tabla 11.3 de Urton (2017) se extrajeron **10 secuencias con 63 cifras** (`transcripciones_numeros.csv`). También se extrajeron los metadatos de las 72 memorias (`medrano_metadatos_72.csv`).
- **Búsqueda Rosetta: negativa y con potencia.** No hay ningún alineamiento con q<0,05 entre 10 208 pruebas. Hay 4 con p<0,001, frente a 10,2 esperadas por azar.
  - El método sí encuentra lo que debe encontrar. Recupera la relación conocida UR278→UR266 (q = 7·10⁻⁴). Detecta listas insertadas con 2 errores de ±1 dígito: las listas de las memorias 40 y 4, en el 89–100 % de 100 ensayos.
  - Límite: no detecta copias cortas de valores 1–20. La copia AS159/AS173 sale con p = 5·10⁻⁴, pero no pasa la FDR.
  - Las listas cortas o de valores comunes (memorias 5, 16, 17 y 22) no tienen potencia suficiente: su información máxima es demasiado baja.
- **Las transcripciones sí dan significado a rasgos estructurales.** Tres firmas derivadas de los géneros coloniales separan el corpus de forma no trivial:
  1. **Asignación (cifras redondas) frente a recuento.**
     - En la memoria 4 (servicios al Inca) son redondas 9 de 9 cifras. En los recuentos de pueblos (memoria 40) y en el padrón del Santa, 0.
     - En el corpus, el 29 % de las cuerdas intactas ≥10 son múltiplos de 10, frente al 10 % esperable en un recuento. La heterogeneidad entre quipus es fortísima (χ² = 3690, 329 gl).
     - 26 quipus son "de asignación" (≥80 % redondos) y 159 son compatibles con recuento.
     - **Las tablas con "filas con tamaño" de 10_tablas son de recuento** (mediana 0,15 frente a 0,25; p = 0,01).
  2. **Cuotas repetidas.** En la memoria 4 aparecen 150, 150 y 200, 200. En el corpus hay más valores adyacentes idénticos de lo esperado (929 frente a 552, p = 0,0005; 20 quipus con q<0,05). Esos quipus son justamente los redondeados (mediana 0,55 frente a 0,20; p = 1,7·10⁻⁴).
  3. **Total antes de la lista.** En la memoria 40 hay un total de 823, un subtotal de 260 y luego los 11 pueblos, que **suman exactamente 260**.
     - En el corpus **no es una regla**: 86 casos frente a 75,5 esperados (p = 0,12). Solo aparece en UR118, UR119 (Paracas) y UR275 (Incahuasi).
     - El total al final tampoco es una regla (91 frente a 75; p = 0,04; Holm n.s.): solo AS044 y AS199.
- **Negativos**:
  - cantidad × precio, la firma de las cuentas con pesos (46 frente a 58,5);
  - tamaños de los 6 quipus del Santa frente a las 6 pachacas (p = 0,24–0,40);
  - cualquier coincidencia con los tributarios de Chachapoyas, incluido UR011.

## 1. Qué contiene la tesis (tarea 1)

### 1.1 Corpus y géneros (`r0_metadatos_medrano.py` → `medrano_metadatos_72.csv`)

- **Extracción del apéndice B.** Se sacó del PDF con PyMuPDF (expresión regular sobre el texto de las páginas 178–189) y salieron las 72 filas completas. Los recuentos por tipo coinciden con la tabla 3.1 de la tesis.

| tipo (Medrano) | n | líneas (mediana) | con moneda | pre/post | interrumpida |
|---|---|---|---|---|---|
| pnar, primaria narrativa (Capac Ayllu, ceques de Cobo) | 3 | 98 | 0 | 3/0 | 0 |
| pnum, primaria numérica (tributo, servicios, bienes entregados) | 29 | 68 | 16 | 3/26 | 0 |
| summ, resumen (títulos de encomienda, visitas) | 32 | 33 | 0 | 32/0 | 2 |
| elicit, respuesta a preguntas (juicios: Sacaca, Chayanta, Huaraz) | 8 | 285 | 4 | 3/5 | 5 |

- **Géneros por contenido** (de los títulos):
  - tributo o tasa (Chucuito, Charcas, Machaca, Sacaca);
  - censo de "indios" por pueblo (encomiendas, Chucuito memoria 23);
  - bienes entregados a encomenderos o capitanes (Jauja, Mantaro, memorias 7–11);
  - servicios al Inca (memoria 4);
  - ganado (memorias 13 y 27);
  - historia y ceques (memorias 1–3).
- **Resultado estadístico de la tesis.** El ACP y el agrupamiento jerárquico solo separan antes/después de la conquista y con/sin moneda. La tipología exegética solo "acierta" en el 25 % (solo los *summary* forman grupo).
  - Las transcripciones posteriores a la conquista son "sustantivo + número" con un único verbo, *dar*. Esto confirma estadísticamente a Urton (1998).

### 1.2 La "insistence": cómo se lee un quipu en voz alta

La tesis propone cuatro principios:

1. **Repetición simétrica.** Pares clave-valor encadenados ("Más para guarda de Quito doscientos indios. Más..."). A cada descriptor le corresponde una cantidad y ningún descriptor queda sin ella.
2. **Elaboración.** Detalles añadidos oralmente sobre una base formulaica; es típica de lo narrativo.
3. **Acomodación.** Precios y pesos incorporados después de 1532 (en Sacaca, cantidad + precio por partida).
4. **Escala variable.** Se mezclan niveles administrativos: totales de pueblo, de cacique y de provincia. Hay "quipus resumen" de Jauja que condensan otros quipus. Los totales que se dan en el juicio se calculaban con piedras o *yupana* en el momento, "the bottom line", según Platt.

**Errores de lectura documentados.** Las correcciones más frecuentes difieren en las unidades, a menudo en 1 (una vuelta de nudo largo). Hay casos de 1479 → 1514, de 1233 → 1033 y de "diez/cinco".

- Esto justifica la tolerancia de ±1 nudo en una posición decimal que se usa en la búsqueda.

### 1.3 Secuencias numéricas extraídas (`r1_secuencias.py` → `transcripciones_numeros.csv`, `r1_resumen.txt`)

| secuencia | género | cifras | magnitud | redondas (≥10) | estructura |
|---|---|---|---|---|---|
| m4 Chupaychos → Inca (PK I:141) | pnum, pre, servicios | 400, 150, 150, 10, 200, 200, 20, 120, 60 | 10–400 | **9/9** | categoría → número; **la primera es la mayor**; pares repetidos; sin total en el fragmento |
| m5 Chupaychos → Gómez Arias | pnum, post | 100 (cada 15 días), 200 (al mes), 80, 29 | 29–200 | 2/3 | cuota por período; total derivado (2×100) |
| m16 Sacaca, aves | pnum, post, precios | 15 gallinas a 1 peso; 4 patos a 1; 540 huevos a 5 por 100 | 4–540 | 1/2 | cantidad + precio |
| m17 Sacaca–Montemayor | elicit | 500 cargas de chuño (6 pesos), 605 carneros, 20 arrobas (4 pesos) | 20–605 | 2/3 | orden de las preguntas, no del quipu; totales hechos con *yupana* |
| m22 Hinojosa (Pilco) | summ | 13, 10, 5 (o 10) | 5–13 | — | un número por pueblo |
| **m40 Aldana (Aullagas, 1540)** | summ | **823 total; 260 "con el cacique Acho" = 38+18+53+9+29+17+37+21+3+21+14** | 3–823 | **0/9** | **jerarquía de totales, total al inicio**; un número por pueblo; sin orden de tamaño |
| Santa, padrón 1670 | padrón | 18, 23, 9, 7, 41, 32 (130; 132 declarados); tributo de 367 pesos | 7–41 | 0/4 | 6 pachacas; según Medrano y Urton, 1 grupo de 6 cuerdas por tributario, 1.ª cuerda = tributo de 0–13 |
| Chachapoyas, tributarios (Urton 2017, t. 11.3) | serie temporal | 17 550 … 2 200 (8 años) | 10³–10⁴ | 3/8 | serie decreciente |

Además: m11, 1 033 cántaros de chicha; m13, 1 514 alpacas (cifras sueltas, no buscadas).

**Lo que la tesis no trae.**

- Las listas completas de las 29 memorias pnum y las 32 summ.
- Su XML de corpus no está en el repo.

Sin ellas, la Rosetta solo puede usar los fragmentos citados.

## 2. Firmas estructurales por género, medidas en el corpus (tarea 2; `r2_firmas.py` → `r2_resumen.txt`, `fA_redondeo_por_quipu.csv`, `fBCF_por_quipu.csv`)

**Método común.**

- Unidad: el quipu.
- Nulo: permutación de los valores no vacíos dentro del quipu, con las posiciones vacías fijas (2000 permutaciones). Para eventos raros se usó la cola de Poisson de la media nula cuando el p empírico tocaba el piso.
- Corrección: BH entre quipus.
- Se excluyen los artefactos de 06 (UR211, AS090_N2, AS019, AS004).
- Para las firmas de secuencia se usaron colgantes de nivel 0 sin cuerdas superiores.

| género (fuente) | firma comprobable | resultado en el corpus | nivel |
|---|---|---|---|
| **Asignación o tasa de servicios** (m4: 9/9 redondas) frente a **recuento de personas** (m40, Santa: 0 redondas) | fracción de cuerdas **intactas** (terminación K) ≥10 que son múltiplo de 10; nulo binomial p0 = 0,1 | tasa conjunta 0,289 (×2,9). Sobredispersión χ² = 3690/329 gl (p ≈ 0): **los quipus se reparten entre "redondos" y "de recuento"**. 143 con exceso (q<0,05), **26 "de asignación"** (≥80 %): UR197, UR058A/B (Arica), AS156, UR202, UR219, AS172, UR228, AS200, AS041, UR103, AS072, JC001, AS101, UR1102, UR227, … **159 compatibles con recuento** (≤20 %). Histograma: 60/92/90/43/19/15/11 en 0–.1–.2–.4–.6–.8–.95–1 | **apoyado con datos** (la heterogeneidad); "asignación" = **propuesto** |
| ídem, cruce con 10_tablas | ¿las tablas son de recuento? | tablas con filas con tamaño (ρ entre columnas, q<0,05): fracción redonda 0,15 frente a 0,25 en las demás tablas (Mann-Whitney p = 0,01; Holm sobre 3 cruces, 0,03). Columnas casi constantes: 0,23 frente a 0,20 (p = 0,98) | **apoyado (exploratorio)**: las tablas con filas que crecen juntas son recuentos (personas u hogares por unidad), no asignaciones |
| **Cuota repetida** (m4 150/150, 200/200; m5 "100 cada 15 días") | colgantes adyacentes idénticos ≥10 | 929 frente a 552 (máximo del nulo 620), p = 0,0005. 20 quipus q<0,05: UR190, UR219, MM001, AS066, UR113, UR283, AS207A, UR278, UR197, UR1114, … Son los redondeados: mediana 0,55 frente a 0,20, p = 1,7·10⁻⁴. En ambas listas: **AS172, UR197, UR219, UR271** | **apoyado con datos**; "lista de asignaciones tipo m4" = **propuesto** |
| **Resumen de encomienda** (m40: total → subtotal → lista que lo suma) | colgante = suma exacta de los 3–12 siguientes (total antes) o de los anteriores (total después) | antes: 86 frente a 75,5 (p = 0,12); después: 91 frente a 75,3 (p = 0,04). Quipus con q<0,05: antes **UR118, UR119, UR275**; después **AS044, AS199**. Direcciones 3 frente a 2 | **negativo** como regla general; **bien apoyado** en esos 5 (replica a 10_tablas) |
| **Cuenta monetizada** (m16, m17: cantidad, precio, valor) | terna consecutiva a·b = c (factor 2–12, c ≥ 20) | 46 frente a 58,5 (p = 0,96); ningún quipu | **negativo** |
| **Padrón individual** (Santa) | (a) tamaños de quipu = tamaños de pachaca; (b) 1.ª cuerda pequeña | (a) L1 entre tamaños ordenados = 21 (9/7, 10/9, 15/18, 17/23, 34/32, 48/41); nulo: composiciones uniformes de 133, mediana 33, p = 0,24; Dirichlet(2), mediana 24, p = 0,40. (b) En el Santa la 1.ª columna es la **menor** (suma 369 frente a 439–4871, 05). En el corpus, "1.ª columna menor" = 49 frente a 40,1 esperado (A4 de 10_tablas, n.s.) | (a) **negativo**; (b) **el formato Santa no es el arquetipo general** (lo general es la 1.ª columna mayor) |
| Censo por edades decrecientes; totales decimales; calendario (05) | — | negativos en 05 | negativo |

**Explicaciones aburridas comprobadas.**

1. **Rotura.** Las cuerdas rotas (terminación B) son redondas en el 58 %, frente al 29 % de las intactas (K): la rotura se lleva los nudos de unidades, que van abajo. Por eso F-A usa solo cuerdas intactas. La rotura sigue pudiendo inflar el redondeo si una cuerda "K" perdió su extremo, pero no explica la sobredispersión entre quipus.
2. **Registrador.** Los quipus AS (Ascher) son más redondos (mediana 0,33) que los UR (0,20). Pero los "de asignación" se reparten (11 AS y 12 UR), así que no es solo el registrador.
3. **Magnitud.** El redondeo no crece con la magnitud: 0,30 en 10–99, 0,28 en 100–999 y 0,20 en ≥1000. No es una "estimación a ojo" de cantidades grandes.

## 3. Búsqueda Rosetta (tarea 3; `r3_rosetta.py` → `rosetta_resultados.csv`, `r3_resumen.txt`)

### 3.1 Diseño

- **Secuencias buscadas.** Las 8 secuencias de ≥3 cifras (sin precios), en sentido directo e inverso (por los quipus registrados invertidos, como UR1107/UR237).
- **Contra qué.** La secuencia completa de cuerdas con nudos de cada quipu, en el orden de KFG (colgantes y subsidiarias).
- **Alineamiento local** (Smith-Waterman):
  - acierto si |v − q| ∈ {0, 10ᵏ ≤ q}, es decir, ±1 nudo en una posición;
  - el acierto vale w = −log₁₀ f, con f la frecuencia en el corpus de valores que aciertan q. Así se **penalizan los valores comunes**: 10 vale 0,97, 3 vale 0,70, 823 vale 3,90 y 17 550 vale 5,0;
  - saltar una cuerda del quipu cuesta −0,25, porque la lectura puede omitir cuerdas de detalle;
  - saltar una cifra de la transcripción cuesta −1.
- **Nulo y p.** Se permutan los valores dentro de cada quipu. El p es adaptativo: 10³ permutaciones; si p ≤ 0,005, 10⁵; y si sigue en el piso, cola Gumbel. Corrección BH sobre las 10 208 pruebas.

### 3.2 Controles

- **(a) Positivo real.** Los 12 primeros totales de grupo de UR278 se buscaron en todo el corpus, salvo UR278. **El mejor es UR266**, con 9 cabeceras alineadas en orden y separadas por cuerdas de detalle: p = 2,7·10⁻⁷, q = 7·10⁻⁴. Replica a 04.
- **(b) Copia contigua de valores pequeños: es el límite del método.** Se buscaron las cuerdas 0–11 de AS159, que contienen el tramo de 8 compartido con AS173 (Urton 2005).
  - AS173 sale con 8 aciertos exactos en orden, pero solo con p = 5·10⁻⁴ (q = 0,32 dentro de los controles).
  - El motivo es que AS173 tiene 15 cuerdas con valores 1–20 que ya son los de la consulta. El nulo de permutación dentro del quipu solo premia el orden, y con 15 valores repetitivos el orden es poco informativo.
  - Conclusión: **copias cortas de valores pequeños no son detectables con FDR sobre todo el corpus**. El negativo de la Rosetta vale para listas con cifras distintivas, no para listas de 1–20.
- **(c) Potencia.** Se insertaron listas en 100 quipus al azar, con 2 cifras alteradas en ±1 dígito. Se cuenta como detección un p por debajo del umbral BH de un hallazgo único (p ≤ 4,9·10⁻⁶). Archivos: `r3_resumen.txt` y `r3b_potencia.py` → `r3b_resumen.txt`.
  - m40 completa (13 cifras): detectada en el **100 %**.
  - m40 sin los totales 823 y 260 (los 11 pueblos): **95 %**.
  - m4 (9 servicios redondos): **89 %**.
  - Una sola lista de 9–13 partidas como estas saldría si estuviera en el corpus.

### 3.3 Resultado: **negativo**

- **Global.** Ningún alineamiento con q<0,05 ni con q<0,25. p<0,001 en 4 pruebas (10,2 esperadas) y p<0,01 en 27 (102 esperadas). El p adaptativo es conservador.
- **Mejor caso de la memoria 40.** Es UR1105 (p = 1,4·10⁻⁴, q = 0,77), pero sus 6 aciertos son casi todos con error: 9→8, 29→28, 17→7, 3→4, 21, 14. Es ruido de valores pequeños.
- **Otros "mejores" casos**: Santa→UR1126 (130→30, 32→22…), m5→UR146 (29→30, 80→70, 200→199, 100→110) y m4→UR1091 (150→50, 150→50). Todos se apoyan en la tolerancia y en valores frecuentes.
- **Chachapoyas.** Mejor p = 0,03. Ninguna serie de miles coincide, tampoco UR011. Urton mismo solo proponía un **ritmo** de caída parecido, no las cifras.
- **Secuencias sin potencia.** m22 (información máxima 2,9), m16 (5,1), m17 (7,1) y m5 (7,1) no pueden alcanzar el umbral FDR **aunque coincidieran**. Para ellas el negativo no informa.
- **Las que sí pueden.** El negativo es informativo para m4 (15,1), m40 (21,6) y Chachapoyas (35,0). En el caso del Santa (9,9), está en el límite.
- **Replicación.** Esto replica con nulo y FDR la observación de Urton (2017: 187) de que buscó en la KDB secuencias de censos agregados tempranos "sin encontrar ninguna".

**Lectura.** Ninguno de los quipus conservados es el registro de esos documentos concretos. Esto era lo esperable: las transcripciones son de la sierra y de Charcas, y los quipus del corpus son casi todos de la costa (05).

## 4. Contraste con Medrano y Urton (2018, Santa) y con 05_etnohistoria (tarea 4)

**Coincidencias:**

- **Formato de padrón individual: no es el arquetipo general.** Según Medrano y Urton, el Santa es un padrón individual: un grupo de 6 cuerdas por tributario, la 1.ª cuerda con el tributo (0–13 pesos) y la unión R/V como mitad. Eso hace del Santa un formato **distinto del arquetipo general**:
  - allí la 1.ª columna es la menor; en el corpus, la 1.ª columna mayor (68 frente a 39 esperados, 10_tablas);
  - los tamaños de los quipus no reflejan los de las pachacas mejor que el azar (p = 0,24–0,40; nuevo);
  - las alineaciones de mitades no son excepcionales (05).
  - En consecuencia, el Santa sigue siendo "Rosetta" **propuesta**, no bien apoyada. La única coincidencia fuerte (Σ 1.ª cuerda = 367) es post hoc (05).
- **El total "en voz alta" no tiene por qué estar en el quipu.** Las transcripciones muestran que los totales a menudo **se calculaban al leer**: piedras y *yupana* en Sacaca, "bottom line". Los quipus "resumen" eran objetos aparte (Jauja, según Chirinos).
  - Esto ofrece una explicación aburrida y documental de dos hechos del corpus:
    - solo el 3–7 % de los quipus tiene contabilidad interna verificable (08);
    - las relaciones resumen viven entre quipus (UR266 resume UR278, 04) o en cuerdas sueltas (10_tablas).
  - Nivel: **propuesto**, coherente con los datos.
- **"Empezando por el más importante."** La cita de Garcilaso (05) y la memoria 4, donde la primera partida (400, sembrar en el Cuzco) es la mayor, encajan con el arquetipo de 10_tablas: "1.ª columna mayor, a menudo blanca". Es un caso (n = 1 en las transcripciones): **propuesto**.

**Divergencias y límites:**

- **Totales al inicio.** Las transcripciones ponen los totales al inicio (m40). El corpus no prefiere ninguna dirección (3 quipus frente a 2). El "total primero" de los títulos de encomienda puede ser retórica notarial española ("en esta manera"), no una regla del quipu.
- **Edad y sexo; tributo monetizado.** 05 descartó los censos por edad decreciente. Aquí se descarta la estructura de cuentas monetizadas (cantidad × precio). En el corpus no aparecen los géneros posteriores a la conquista que dominan *Textos Andinos* (26 de 29 pnum son post).
  - Coherente con un corpus mayoritariamente prehispánico y costero.

## 5. Qué significa la estructura bien apoyada, a la luz de la Rosetta (síntesis con niveles)

| rasgo bien apoyado (rondas 1–2) | análogo colonial | lectura | nivel |
|---|---|---|---|
| tabla filas × columnas; filas con "tamaño" | lista de pueblos o ayllus × categorías (m40, Chucuito: indios por cabecera) | fila = unidad social; columnas = categorías de personas o bienes; **de recuento** (no redondas, p = 0,01) | apoyado (exploratorio) |
| 1.ª columna mayor y blanca | primera partida = la principal (m4, 400; Garcilaso) | categoría principal, no total | propuesto |
| columnas casi constantes (10, 15, 20, 47, 100) | tasa fija por período o unidad ("100 piezas cada 15 días", m5) | cuota o tasa | propuesto |
| listas redondas con repeticiones (26 quipus; AS172, UR197, UR219, UR271) | servicios al Inca en cifras redondas repetidas (m4) | **registro de asignaciones** (mit'a, tasa), no de recuento | propuesto, con firma medible y con nulo |
| totales sueltos y jerarquía UR278 → UR266 | encomienda 823 → 260 → pueblos; "quipus resumen" de Jauja; *yupana* | niveles administrativos (escala variable); total externo al registro de detalle | propuesto |
| Incahuasi [x, c, x−c] | tasa con descuento fijo (sin análogo textual exacto en el material) | deducción fija | propuesto (09) |

## 6. Archivos

- `r0_metadatos_medrano.py` → `medrano_metadatos_72.csv` (apéndice B: 72 memorias, 19 campos).
- `r1_secuencias.py` → `transcripciones_numeros.csv` (10 secuencias, 63 cifras con fuente y líneas de PK) y `r1_resumen.txt`. La autocomprobación (assert) es que la suma de m40 da 260.
- `r2_firmas.py` → `r2_resumen.txt`, `fA_redondeo_por_quipu.csv` y `fBCF_por_quipu.csv` (semilla 20261017, unos 30 s).
- `r3_rosetta.py` → `rosetta_resultados.csv`, `r3_resumen.txt` y `r3_log.txt` (numba, unos 7 min). `r3b_potencia.py` → `r3b_resumen.txt`.

## 7. Siguiente ronda

1. **Conseguir las listas completas de *Textos Andinos*** (PK 2004, vols. 1–2), o el XML del corpus de Medrano, y buscar todo lo que tenga potencia. La prioridad son las 32 memorias *summary* (listas de pueblos de 10 o más cifras) y Chucuito 1567 (memorias 23–27: indios, ropa y plata por cabecera).
   - La prueba de potencia indica que una lista de 10–13 pueblos se detectaría aunque tuviera 2 errores.
   - Valdría la pena además una Rosetta "de forma": comparar la distribución de valores y la fracción redonda de cada memoria con cada quipu.
2. **Validar "asignación frente a recuento"** con el nudo final de las cuerdas (OKR `knot`) y con la procedencia de excavación (Pachacamac domina entre los redondos).
   - Si los quipus redondos de Pachacamac fueran de ofrendas o asignaciones del santuario, debería verse que comparten valores-cuota entre quipus.
3. **Padrón del Santa.** Con el orden de nombres del documento de 1670, probar si el orden de los grupos de seis dentro de cada quipu sigue el padrón (05, punto 1). Es la única Rosetta individual disponible.
4. **Revisar las cuerdas "K" redondas** para descartar extremos perdidos: comparar largos con los de las cuerdas no redondas del mismo grupo.
