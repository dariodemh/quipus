# Otros sistemas de registro sin escritura: qué hay de universal y qué de inca

Carpeta: `analisis/ds/n_otros_sistemas/`. Scripts: `01_tasas_comparables.py`, `02_nueve_columnas.py`, `03_copias_contabilidad.py`, `04_monte_sierpe.py`. Semilla fija 20261018. Salidas: `tasas_regimenes.csv`, `anchos_grupo.csv`, `resultados_*.txt`. No se modificó nada fuera de esta carpeta.

## 0. Pregunta

¿Qué rasgos del quipu son universales de la contabilidad con soporte material y cuáles son específicamente andinos? ¿La cadena de Incahuasi (detalle → componentes → libro del flujo → libro maestro) tiene paralelos? ¿La tasa de 8/18 sumas exactas es comparable con las cuentas proto-cuneiformes o del Exchequer? ¿Monte Sierpe ofrece un paralelo estructural con las cuotas y las 9 partes de Incahuasi?

## 1. Método

**Sistema comparado.** Siete casos, elegidos por tener literatura abierta y por cubrir un gradiente de complejidad: (1) quipu inca de Incahuasi; (2) quipus coloniales/modernos (Tupicocha, tablas de khipu, Collata); (3) *warazan* de Okinawa/Ryukyu; (4) Monte Sierpe / banda de hoyos de Pisco; (5) *tally sticks* del Exchequer inglés; (6) *bullae*, tokens y textos proto-cuneiformes de Uruk; (7) palos de mensaje australianos (AMSD).

**Rasgos codificados.** Base numérica; jerarquía de registros (parcial → consolidado); copias y doble registro; cuotas fijas; separadores; codificación de categorías; tasa de error conocida.

**Datos propios.** `analisis/datos/cuerdas.csv` y `quipus.csv` (651 quipus, 8116 grupos de colgantes); los CSV de `13_sistema_incahuasi` y `14_copias` se usaron como datos, no se re-derivó su alineación. Para Monte Sierpe se usó el PDF y el material suplementario del artículo (OSM: `sup001.docx`, `sup002.xlsx`, `sup003.xlsx`), descargados en `pdf/`.

**Reglas.** Unidad de prueba = quipu (o archivo, cuando el efecto es de sitio). Cada inferencia lleva nulo explícito y p empírico; se indica Holm cuando hay más de una prueba en la misma familia. Los valores 0 sin nudos se tratan como ausentes. La literatura comparada se usa para rasgos estructurales, no para tasas que no publica.

**Límites.** Solo leí cuatro fichas (`2002-Salomon_tupicocha`, `2004-Salomon_cord-keepers`, `2017-Hyland_twisted-cords`, `2021-Hyland-khipu-boards`) y fragmentos de `estado_del_arte.md`. No tuve acceso al texto completo de Salomon 2002/2004 ni al capítulo de Skambraks 2023 (bloqueo del servidor); de este último usé el resumen y los fragmentos indexados. El *warazan* se documenta con fuentes japonesas y con la descripción de Edmund (1924) reproducida por KASS; no hay un corpus cuantitativo publicado. Los datos de Monte Sierpe no incluyen un censo de hoyos por sección (ver §3.3).

## 2. Tabla comparativa

| Sistema | Base numérica | Jerarquía parcial → consolidado | Copias / doble registro | Cuotas fijas | Separadores | Categorías | Error conocido |
|---|---|---|---|---|---|---|---|
| **Quipu inca (Incahuasi)** | Decimal (10), dígitos por tipo/número de nudos; hasta 5 cifras | **4 niveles**: 9 subunidades por registro (UR270) → 2 componentes A/B (UR273/274, cuotas 30 y 17) → libro del flujo (UR266/275, cuota 47) → libro maestro (UR269, bloques de 5); UR268 = nivel de periodo (especulativo) | 5 parejas de copia (255/267A, 256/267B, 266/275, 273A/274A, 273B/274B); doble vía de verificación (9 columnas vs 2 componentes) | 10, 15, 17, 25, 30, 47, 208; **30+17=47, 15+10=25** | Cuerdas rosas PK, cuerdas en blanco, espacios de grupo, cabecera blanca (73 %) | Color (blanco = bruto), posición, nivel, torsión, fibra; vocabulario local | Copias: 86,6 % de valores exactos (13,4 % divergencia); relectura del mismo objeto: 93 % (7 % ruido); KFG–OKR: 0,63 % |
| **Quipu colonial/moderno** | No necesariamente decimal; el valor puede ser numérico o semasiográfico | Tabla de khipu: nombre (tabla) + cordón (obligación); Collata: 2 khipus narrativos de la misma comunidad | Collata: dos khipus narrativos, no un duplicado numérico; tablas: un cordón por nombre | Obligaciones por persona (diezmos, trabajo), no constantes registradas | Cintas de tela (Collata A: 8 cintas → 9 grupos); agujeros de la tabla | Color, fibra, torsión, grosor; nombre alfabético en la tabla | Desconocido |
| **Warazan (Ryukyu)** | Escala decimal de unidades (*koku–to–sho–go–shaku–sai*), pero **no un place-value puro**: el tipo de nudo/hebra y el grosor codifican la unidad; lazo = 50 *koku*, hebras laterales = 10 *koku* | Registro por hogar → cuota de aldea/distrito; no se documenta consolidación aritmética | No se documentan copias; el grosor distinto evita errores; se describe su uso para **verificar** cálculos de los glifos *Kaidā* (fuente secundaria) | Cuota fiscal por hogar (telas, arroz), variable | Lazo = cruce de camino en el cordel de asamblea; hebras que salen del cordón principal | Hebra/hogar/calle; grosor; posición | Sin tasa publicada; “suficientemente exacto para corregir anuncios oficiales” (Ikema 1959, secundario) |
| **Monte Sierpe (Pisco)** | Unaria: un hoyo = una unidad; filas de 7–8 hoyos | ≥60 secciones; **sin totales ni consolidación documentados** | Ninguna | Ninguna documentada | Espacios vacíos entre secciones; filas | Pertenencia a sección; estilo constructivo (con/sin muro) | No aplica (no hay lectura) |
| **Tally sticks (Exchequer)** | £sd no decimal (1£=20s, 1s=12d); muescas de distinto grosor (£1000, £100, £20, £1, 1s, 1d) | Tally (recibo) → *pipe roll* (cuenta anual) → *Chancellor's roll* (duplicado) | **Tally partido**: *stock* y *foil* con las mismas muescas; *pipe rolls* duplicados (E 352) | *Corpus comitatus*: suma anual fija del condado; impuestos | Muescas, posición en el palo, grano de la madera | Tipo de muesca = denominación; nombre/fecha grabados | Sin tasa publicada; el diseño hace evidente la manipulación; auditoría por ajuste de mitades |
| **Uruk proto-cuneiforme** | Varios sistemas **específicos del objeto** (sexagesimal, bisexagesimal, decimal S, capacidad); no un decimal abstracto | Entradas → subtotales/totales al reverso; documento primario → cuenta consolidada (MSVO 1, 212–214); “journals” y “ledgers” | *Bulla*: tokens dentro + impresiones fuera; tablillas selladas; no hay tally partido | Normas/raciones; números redondos; no una cuota fija por registro | Columnas, casos, líneas; reverso para totales | Ideogramas de mercancía, persona, lugar, tiempo; disposición | Errores y correcciones de escriba documentados; sin tasa de corpus |
| **Palos de mensaje australianos** | Ninguna (no numérico); muescas, pintura, objetos adjuntos | Ninguna; un objeto por mensaje | Ninguna; objeto único llevado por el mensajero | Ninguna | Agrupación espacial de marcas; sin estándar | Motivos convencionales, comunitarios; dependen del enunciado oral | Indefinida; la transmisión es memoria + recitación |

Fuentes: Incahuasi, `13_sistema_incahuasi/informe.md` y `16`/coordinador; khipu colonial, Salomon 2004, Hyland 2017 (doi 10.1086/691682), Hyland et al. 2021 (doi 10.25222/larr.1032); warazan, Universidad de las Ryukyus (columna en inglés), Otani 2024 (doi 10.15070/0002000636), KASS/Edmund 1924; Monte Sierpe, Bongers et al. 2026, *Antiquity* 100(409):145–163, doi 10.15184/aqy.2025.10237; Exchequer, Skambraks 2023 (doi 10.36253/979-12-215-0092-9.09), London Museum, The National Archives E 372/E 352; Uruk, Englund 2012 (doi 10.1093/oxfordhb/9780199557301.013.0002), Englund 2004, Overmann 2021 (doi 10.1086/715767), Schmandt-Besserat 1992 (*Before Writing*); palos, Kelly et al. 2024, *PLoS ONE* 19(4):e0299712.

### 2.1 Lo que la tabla ya separa

- **Universal en los siete**: acumular y contar sobre un soporte material, agrupar y separar, y codificar categorías. Eso no distingue al quipu.
- **Propio de los sistemas estatales (khipu, warazan, Exchequer, Uruk), no de Monte Sierpe ni de los palos**: cuotas fijas; y, en khipu, Exchequer y Uruk (no documentado en warazan), consolidación de lo parcial en un total. La cuota y el total son rasgos de **administración**, no de “registro sin escritura” en general.
- **Raro**: la copia física como control. Aparece en el Exchequer (tally partido), en Uruk (*bulla* con impresiones) y en el quipu (copias y parejas A/B), pero **no** en warazan, Monte Sierpe ni palos.
- **Específico del quipu (y, en su forma completa, de Incahuasi)**: el árbol de cuerdas (colgantes → subsidiarias → …), el doble canal número/categoría (color, torsión, fibra) y la cadena de cuatro niveles con verificación cruzada. El decimal anudado, en cambio, **no** es exclusivo: el warazan también es decimal posicional.

## 3. Resultados

### 3.1 Incahuasi en el espacio comparativo

La cadena está descrita en `13_sistema_incahuasi/informe.md` y replicada en `16`. Para esta comparación la reduzco a lo relevante:

1. **UR270** (detalle): cada grupo = un registro; 9 colgantes blancos = parte B; 9 subsidiarias NB = parte A. La celda de **UR278** = colgante + subsidiaria de la misma unidad (5 grupos con 6–9/9 columnas; p = 0,0002).
2. **UR273A/UR274A** (parte A, cuota 30) y **UR273B/UR274B** (parte B, cuota 17): A + B = cabecera del consolidado. **8/18 sumas exactas** frente a 0,95 esperadas por permutación (p = 5·10⁻⁵; los nulos publicados van de 0,73 a 1,27, luego el lift es 6,3–11×).
3. **UR266/UR275** (libro del flujo, cuota 47): reciben las mismas cifras por dos vías, columnas (UR278) y componentes (A+B). Es un control cruzado de tipo “doble entrada”.
4. **UR269** (libro maestro): bloques de 5 filas; fila 1 = flujo 47 y fila 5 = flujo 25 (**apoyado**: 4/4 y 4/5 exactas); las cuotas 46, 46 y 44 de las filas 2–4 corresponden a flujos cuyos quipus no se conservan (**propuesto**).
5. **UR268** (cuota 208 = 47+46+46+44+25) sería el nivel de periodo, pero no hay ninguna suma exacta que lo confirme: **especulativo**.

**¿Hay paralelos a esta cadena?** Parciales, y de menor profundidad:

- **Uruk**: el corpus es de ~5 000–6 000 tablillas, ~85 % administrativas (Englund 2012). Hay consolidación de documento primario en cuenta secundaria, documentada explícitamente (MSVO 1, 212–214; “account consolidation was a regularly used technique by the time of the Uruk III period”, Englund 2004: 40–41), y totales al reverso. En lo publicado, la cadena documentada es de **2 niveles** (primario → secundario); no se describe una cadena de cuatro niveles con una cuota propia en cada uno, ni una verificación por dos vías independientes.
- **Exchequer**: tally (recibo) → *pipe roll* (cuenta anual) → duplicado del canciller. **2–3 niveles** de soporte, con auditoría por ajuste de las dos mitades. El *pipe roll* consolida la cuenta del sheriff, pero el tally es un **recibo**, no un registro de detalle que se sume fila a fila; la verificación es física, no por dos vías aritméticas.
- **Warazan**: registro por hogar → cuota de aldea; **1–2 niveles**, sin aritmética de consolidación documentada.
- **Monte Sierpe**: secciones y filas; **1 nivel**, sin totales.
- **Palos de mensaje**: **0 niveles**.

Conclusión: la **profundidad** de 4 niveles y la **doble vía de verificación** de Incahuasi no tienen paralelo en la muestra. Lo que sí es universal es la idea de que un total consolida parciales; lo específico es que el consolidado se pueda reconstruir por dos caminos independientes y que cada nivel tenga su propia cuota.

### 3.1b Quipus coloniales y modernos: la tabla de nombres

Las **tablas de khipu** son el paralelo andino más claro del nivel “tabla”, pero con otra lógica: la tabla de Mangas tenía 181 agujeros y conserva 87 cordones; la de Ayacucho, 103 cordones; la de Chile, 109 (Hyland et al. 2021). Cada cordón cuelga junto a un **nombre escrito**: la fila es una persona, no una categoría, y el cordón registra asistencia, diezmo u obligación. Es un híbrido alfabético-anudado, no un libro aritmético. **Collata** lleva la otra dirección: 288 y 199 colgantes en 9 y 4 grupos, 95 combinaciones de color/fibra/torsión y casi ningún nudo numérico; se propone como texto narrativo, no como cuenta (Hyland 2017; nivel **propuesto/especulativo**).

Implicación: en los Andes hay **dos tipos de tabla** —la indexada por personas (tabla de khipu) y la indexada por categorías (UR278)— y solo la segunda tiene consolidación aritmética. La tabla de nombres se parece a las listas de personas de Uruk (nombre + cantidad); el “libro consolidado” se parece a la cuenta secundaria de Uruk y al *pipe roll*. La **cadena completa** con cuotas en cada nivel sigue siendo exclusiva de Incahuasi.

### 3.2 ¿Es comparable la tasa 8/18?

**No como tasa bruta.** El 44 % (8/18) solo tiene sentido frente a su propio nulo: 5,3 % por comparación (0,95/18), lift 8,4×, p = 5·10⁻⁵. Pero una tasa bruta depende del **régimen numérico** del sistema. Con el mismo número de valores en el blanco, la probabilidad de que una suma caiga en una cifra listada es:

| Régimen | Blancos | Rango | P(acierto al azar) |
|---|---|---|---|
| Incahuasi, observado | 89 cabeceras | 100–4 273 | **0,444** |
| Incahuasi, nulo de emparejamiento | 89 | 100–4 273 | **0,053** |
| Quipus reales con valores ≤300 (131 quipus) | variable | 5–2 000 | **0,059** (mediana) |
| Enteros densos, 20 blancos | 20 | 1–1 000 | **0,010** |
| Múltiplos de 10, 20 blancos | 20 | 10–1 000 | **0,190** |
| Múltiplos de 60, 20 blancos | 20 | 60–3 600 | **0,346** |

Lectura: en un sistema sexagesimal de números redondos, **el azar solo puede dar ~35 %**; una “tasa de verificación” del 30–40 % en Uruk no sería evidencia de nada sin el nulo. En un sistema de enteros densos, en cambio, el azar da ~1 % y una tasa del 44 % sería altísima. Por eso **la única magnitud comparable es el lift** (observado ÷ azar), y para Uruk, el Exchequer o el warazan **no hay tasas publicadas con denominador** que permitan calcularlo. La literatura describe totales que “cuadran” y errores de escriba, pero no publica “n de sumas exactas / n de comparaciones”.

**Un control adicional.** De los 18 registros, 8 son exactos y 10 no. De los 10 fallos, 2 difieren en ±1 y 3 en ±10 de la cabecera más cercana; los otros 5 difieren en 9, 25, 29, 31 y 36, que es el orden del vecino más cercano esperado en un blanco de 89 valores espaciados ~47. **No hay una firma limpia de “error de dígito”**. Además, el volcado de `13` no distingue el destino alineado de **cualquier otra cabecera con el mismo valor**: 1506 coincide con UR266 g2, que `13` identifica como total de UR278 g1, y 1827 y 1780 se atribuyen ambos a UR269 g17 (no pueden ser la misma fila). Por eso **8/18 es un límite superior** de la tasa de correspondencia correcta, no una tasa de error del quipucamayoc. Para comparar con otras contabilidades habría que rehacer el test con la alineación registro a registro publicada, no con “cualquier cabecera del libro”.

### 3.3 Monte Sierpe: qué publica y qué no

Los números del artículo y de su OSM son:

- ~**5 200 hoyos** en ~1,5 km; **≥60 secciones** separadas por espacios vacíos (Bongers et al. 2026: 151).
- Sección **a**: ≥9 filas consecutivas de 8 hoyos = **72**.
- Sección **b**: 6 filas de 7 + 1 fila de 8 = **50**.
- Sección **c**: ≥12 filas alternando 7 y 8; los conteos diagonales son **1, 3, 5, 7, 9, 11, 11, 14, 12, 10, 8, 6, 4, 2, 1** (OSM, Fig. S40). La suma es 104; como cada hoyo cae en una sola diagonal, 104 sería el total de la sección **si la serie cubre toda la sección** (el OSM no lo dice explícitamente).
- No hay tabla de hoyos por sección en el OSM: los suplementos son microbotánica (`sup002`, `sup003`) y texto/figuras (`sup001`). El único dato numérico nuevo es la serie diagonal de la sección c.

**Comparación con las cuotas y las 9 partes de Incahuasi:**

- 5 200 / 60 = **86,7 hoyos por sección** (si fueran 65 secciones, 80,0; si 70, 74,3). No hay un valor único.
- 72, 50 y 104 **no coinciden con ninguna cuota** de Incahuasi {10, 15, 17, 25, 30, 44, 46, 47, 208}. 50 = 2×25 es un múltiplo trivial.
- Si los cuatro números (72, 50, 104, 86,7) se sortearan uniformemente entre 10 y 210, la probabilidad de al menos una coincidencia exacta con las nueve cuotas es **0,167**. Es decir, ni siquiera una coincidencia habría sido informativa.
- El “9” de la sección a es el **número de filas**, no una partición en 9 partes: 9 filas × 8 hoyos. La racha de 9 filas iguales no es rara: simulando 60 secciones de 8–13 filas con anchos 7/8, **p = 0,32** de encontrar al menos una racha de 9.
- La serie diagonal es un perfil aproximadamente unimodal (sube 1→14 y baja a 1), consistente con el conteo diagonal de una retícula escalonada; es un **producto de la geometría**, no una notación numérica. Los propios autores piden más análisis para saber si es intencional (OSM: 37–38).
- El quipu que el artículo usa como paralelo (VA16135a/b, Berlín: 80 grupos de 10–12 cuerdas) **no está en KFG/OKR**, así que la analogía no se puede replicar con nuestros datos. Y la “aritmética intricada” que se le atribuye (Medrano y Khosla 2024) es justamente la que `08_auditoria_sumas` mostró que **no se puede evaluar con el detector KFG**: el 74 % de los quipus con relaciones es esperable por azar y la métrica tiene poca potencia (ni prueba ni refuta la contabilidad). El artículo la cita sin control.

**Conclusión:** Monte Sierpe es compatible con un **contador unario de superficie** (hoyos = unidades, secciones = grupos sociales), pero no hay evidencia publicada de totales, cuotas, copias ni consolidación. No es un paralelo de la cadena de Incahuasi; a lo sumo, de su nivel 0 (unidades).

### 3.4 El “9” no es una firma administrativa universal

En el corpus KFG (651 quipus, 8 116 grupos):

- Ancho medio de grupo: **5,14** colgantes.
- Grupos de ancho 9: **254 (3,13 %)**. La ratio frente a la media de los vecinos 8 y 10 es **0,97**: no hay pico en 9.
- 298 quipus tienen al menos un grupo de 9; 9 tienen **todos** sus grupos de 9 (varios con un solo grupo, de modo que la cifra es un límite superior); 13 tienen ≥80 %.
- En los 177 quipus tabulares, el ancho de tabla K tiene mediana **6**; K=9 en **15/177 (8,5 %)**. Los tabulares tienen una proporción algo mayor de grupos de 9 que el resto (0,063 vs 0,038), pero **p = 0,08** y no sobrevive a Holm (0,16). **Negativo.**
- **UR278** es la excepción local: 26 grupos tienen exactamente 9 colgantes, 1 tiene 10 y 3 tienen 12; en total 30 grupos con ≥7 colgantes, compatible con las 28–33 filas que usa `13` según cómo se cuenten separadores y grupos incompletos (los de 1–6 colgantes). Es un diseño de 9 columnas, real y local, no una tendencia del corpus.
- **Collata A** (khipu narrativo, sin nudos numéricos salvo terminales) tiene **288 colgantes en 9 grupos separados por 8 cintas** (Hyland 2017). Es decir: 9 grupos también aparecen en un registro **no contable**. El 9 no distingue contabilidad de narración.

### 3.5 Copias y contabilidad: un efecto de archivo, no una ley

Cruzando los 29 pares de copia (25 de `14_copias` + 5 estructurales de `13`, con un solapamiento) con los 20 quipus de contabilidad interna verificable de `08`:

| Prueba | Con copia | Sin copia | OR | p |
|---|---|---|---|---|
| Contabilidad verificable (20) | 7 | 13 | 7,18 | **0,00042** |
| Contabilidad fuera de Incahuasi (11) | 0 | 11 | 0 | **1,00** |
| Incahuasi (14) | 10 | 4 | 36,3 | <10⁻⁵ |

El efecto existe, pero **desaparece al quitar Incahuasi**: ninguno de los 11 quipus contables de otros sitios está en un par de copia. Hay dos cautelas. Primera: copias y sumas se detectaron con la **misma señal** (los valores), de modo que el test positivo no es independiente; el resultado robusto es el negativo. Segunda: la fila de Incahuasi es **descriptiva**, no inferencial, porque ese conjunto se definió con los mismos datos que prueban su sistema. A nivel de archivo (unidad correcta para un efecto de sitio):

| Archivo | n | Copias | Contabilidad verificable |
|---|---|---|---|
| Incahuasi | 52* | 11 | 9 |
| Pachacamac | 90 | 7 | 0 |
| Paracas | 7 | 0 | 2 |
| Ica | 47 | 1 | 1 |
| Leymebamba | 22 | 3 | 0 |
| Nazca | 13 | 3 | 0 |

*52 es el número de quipus con procedencia “Incahuasi” en los metadatos (incluye material de los sectores A y B); `13` estudia 34. De 12 archivos reales con n≥5 y algún rasgo (la tabla muestra los 6 principales; excluyo “Unknown”), **solo Incahuasi tiene copias y contabilidad verificable a la vez**. Pachacamac tiene 7 copias y ninguna contabilidad verificable; Paracas tiene 2 quipus contables y ninguna copia. Con n = 1 archivo, no se puede concluir que la copia sea un rasgo de la contabilidad: es una **práctica de Incahuasi** (y, en otro sentido, de los talleres de Pachacamac, donde copian sin aritmética verificable).

### 3.6 Tasas de error: solo el quipu tiene una medición propia

- **Quipu**: entre copias, 86,6 % de valores exactos (13,4 % de divergencia); la relectura del mismo objeto da 93,0 % (7 % de ruido de transcripción). La diferencia 86,6 vs 93,0 **no es significativa** (p = 0,21, `14_copias`): el “6,4 % neto” es una estimación, no un efecto bien apoyado. KFG vs OKR: 0,63 % de discrepancias de **transcripción**, la mitad por factor 10 (`t_okr_vs_kfg`). Es la única tasa construida con denominador y control, y aun así es pequeña y ruidosa.
- **Exchequer**: no hay tasa publicada. El diseño (tally partido, ajuste de *stock* y *foil*, *pipe roll* duplicado) es un mecanismo **anti-fraude**, no una medida de error. La literatura describe fraudes y auditorías, no “n de muescas erróneas / n de tallys”.
- **Uruk**: hay errores y correcciones de escriba, y totales al reverso, pero no un denominador de corpus. La consolidación está documentada; la exactitud no está cuantificada.
- **Warazan**: sin tasa. La afirmación de que era “suficientemente exacto para corregir anuncios oficiales” es cualitativa y secundaria.
- **Monte Sierpe**: no hay lectura, luego no hay tasa de error posible.
- **Palos de mensaje**: la exactitud depende de la memoria del mensajero; no es una propiedad del objeto.

**Consecuencia metodológica:** la comparación de “tasas de error” entre sistemas es hoy **imposible**. Solo se puede comparar el *diseño* del control (copia partida, doble vía, sello, grosor) y, en el quipu, el *lift* de una prueba dirigida.

## 4. Controles, nulos y corrección múltiple

| Prueba | Nulo | p | Corrección | Veredicto |
|---|---|---|---|---|
| 8/18 sumas A+B | permutar B entre los 18 registros | 5·10⁻⁵ | no (prueba dirigida única); se reportan tres nulos (0,73–1,27 esperados) | **Bien apoyado** (replicado por 16 y el coordinador) |
| 8/18 como “tasa” | el mismo, expresado como lift | — | — | **No comparable** con tasas brutas de otros sistemas |
| Grupos de ancho 9 en tabulares | permutar la etiqueta “tabular” entre quipus | 0,080 | Holm con la ratio 9/vecinos → 0,16 | **Negativo** |
| Copias × contabilidad (20) | Fisher exacta | 0,00042 | Holm (3 pruebas) → 0,0013 | **Apoyado, pero confundido con el archivo** |
| Copias × contabilidad fuera de Incahuasi | Fisher exacta | 1,00 | — | **Negativo** |
| Racha de 9 filas en Monte Sierpe | 60 secciones, anchos 7/8 al azar | 0,319 | no | **No es señal** |
| Coincidencia de cuotas de Monte Sierpe | 4 números U(10,210) vs 9 cuotas | 0,167 | no | **No es señal** |

No hay corrección múltiple en las pruebas dirigidas de Incahuasi (una sola hipótesis estructural). Sí la hay en las pruebas exploratorias de “9” y “copias”, y en ambos casos el resultado no sobrevive o queda confundido con el sitio.

## 5. Resultados negativos

1. **No hay un “9” universal**: 3,13 % de los grupos, ratio 0,97 frente a los vecinos; K=9 en 15/177 tabulares (mediana 6); p=0,08 sin corregir.
2. **No hay copias asociadas a la contabilidad fuera de Incahuasi**: 0/11 quipus contables no-incaicos en pares de copia (p=1). Pachacamac copia sin aritmética verificable; Paracas tiene aritmética sin copias.
3. **Monte Sierpe no da cuotas ni totales**: 72, 50, 104 y 86,7 no coinciden con las cuotas de Incahuasi; la probabilidad de una coincidencia incidental es 0,17; la racha de 9 filas tiene p=0,32.
4. **No hay censo de hoyos por sección** en el artículo ni en el OSM; la comparación “bloque a bloque” que pedía la tarea no se puede hacer con los datos publicados.
5. **No hay tasas de error publicadas** para Uruk, Exchequer, warazan, Monte Sierpe ni palos de mensaje; la comparación de exactitud se reduce al quipu.
6. **El quipu-paralelo del artículo (VA16135) no está en KFG/OKR**: no se puede replicar su aritmética con nuestros datos.
7. **La alineación de los 8/18 no está libre de ambigüedad**: el volcado no distingue el destino alineado de cualquier cabecera con el mismo valor (1506 coincide con UR266 g2, total de UR278 g1; 1827 y 1780 se atribuyen ambos a UR269 g17); 8/18 es un límite superior.

## 6. Universal, andino y local

**Universal de la contabilidad con soporte material (7/7 casos):**
- acumular y contar unidades;
- agrupar y separar (espacios, columnas, muescas, lazos);
- codificar categorías (mercancía, persona, lugar) en un canal distinto del número.

**Propio de los sistemas estatales (khipu, warazan, Exchequer, Uruk; 4/4):**
- fijar cuotas por unidad social (hogar, condado, registro);
- consolidar parciales en un total (documentado en khipu, Exchequer y Uruk; no en warazan);
- **duplicar o verificar** (tally partido, *bulla*, copias), presente en 3 de los 4.

**Compartido con Ryukyu, no universal:**
- **nudos sobre una escala decimal de unidades**: el warazan también los tiene, en una región sin contacto, aunque no como place-value puro (allí el tipo de nudo/hebra codifica la unidad). Luego el decimal anudado no es una invención andina; lo andino es su **combinación** con el árbol de cuerdas (Uruk usa sistemas específicos del objeto y el Exchequer, £sd).
- **árbol de cuerdas** (colgante → subsidiaria → …): no aparece en warazan, tally, Uruk, Monte Sierpe ni palos.
- **doble canal número/categoría** con color, torsión y fibra; el vocabulario de color es **local**, no panandino (`02_color`, `03_gramatica`).
- **parejas A/B que se suman** y cuotas que se suman (30+17=47): no encontrado en ningún otro sistema de la muestra.
- **tabla de 9 columnas × 33 filas** con cabecera blanca: local de Incahuasi; el 9 también aparece en un khipu narrativo (Collata), luego no es diagnóstico.

**Local de Incahuasi (no extrapolar):**
- cuotas 10/15/17/25/30/47/208 y su regla de suma;
- 9 columnas, bloques de 5 en UR269, cabecera blanca al 73 %;
- copias en cada nivel y doble vía de verificación;
- UR268 = 208 (especulativo).

## 7. Hipótesis comprobables con nuestros datos

1. **Cuotas como columnas constantes.** Si la cuota fija es un rasgo administrativo general, los 36 quipus con columnas casi constantes (`10_tablas`) deberían tener más sumas internas exactas y más valores repetidos 10/15/20/25/47 que controles apareados por tamaño y procedencia. *Predicción*: enriquecimiento; *si falla*, la cuota es solo un rótulo local.
2. **Copias y aritmética dentro de cada archivo.** En archivos con ≥2 pares de copia, comparar la tasa de sumas verificables entre quipus con copia y sin copia. *Predicción anti-fraude*: mayor en los copiados. *Dato actual*: Pachacamac (7 copias, 0 contabilidad) va en contra; hace falta más n.
3. **Ancho 9 y efecto de columna.** Si 9 columnas es una plantilla administrativa, los tabulares con K=9 deberían mostrar un efecto de columna (Friedman) y un efecto de fila más fuertes que los K≠9. *Predicción*: diferencia; *dato actual*: prevalencia de 9 no significativa (p=0,08).
4. **Decimal anudado khipu vs warazan.** Comparar el mapeo dígito→tipo de nudo en quipus (KFG `nudos`) con los tipos de nudo del warazan (fotos de museo). *Predicción*: si ambos usan un código analógico de tamaño, el orden de los tipos será monótono con la magnitud; si el quipu usa tipos discretos (S/L/E), no lo será.
5. **Censo de Monte Sierpe.** Medir las ≥60 secciones en la imagen de dron y probar (a) módulo 9/10, (b) agrupamiento en números redondos, (c) forma de la distribución (Poisson = tally; constantes repetidas = cuotas). *Predicción si es tally*: sin módulo preferido; *si es cuota*: constantes repetidas.
6. **Doble vía en otros archivos.** Buscar en los 5 quipus inéditos de Inkawasi parejas A/B cuyas cuotas sumen 46 o 44 y cuyas sumas den las filas 2–4 de UR269. *Predicción*: si el sistema es real, aparecerán; si no, el archivo conservado es un fragmento único.
7. **Tasa de error común.** Publicar para cada sistema el mismo estadístico: acuerdo exacto entre dos copias o dos lecturas del mismo objeto. Solo entonces se podrá comparar 86,6 % (quipu) con lo que sea que den el Exchequer y Uruk.

## 8. Para el coordinador

- **8/18 no es una tasa de error ni una tasa comparable.** Es 44 % frente a 5,3 % de su nulo (lift 8,4×; p=5·10⁻⁵; los nulos publicados dan 6,3–11×). En un ledger sexagesimal redondo el azar solo da **35 %**; en enteros densos, 1 %. Sin denominador y sin nulo, las “tasas” de Uruk y del Exchequer no se pueden comparar.
- **La cadena de Incahuasi tiene paralelos parciales, no un equivalente.** Uruk consolida documento primario → cuenta secundaria (2 niveles, MSVO 1, 212–214) y el Exchequer tally → pipe roll → duplicado (2–3 niveles, con copia partida). Nadie tiene 4 niveles con doble vía independiente.
- **El “9” no es universal.** 3,13 % de los grupos del corpus, ratio 0,97 frente a los vecinos; K=9 en 15/177 tabulares (mediana 6; p=0,08, Holm 0,16). UR278 es local; Collata tiene 9 grupos en un khipu **narrativo**. El 9 de Monte Sierpe es una racha de filas (p=0,32), no una partición.
- **Monte Sierpe no publica censo por bloque.** 5 200 hoyos / ≥60 secciones = 86,7; solo hay tres secciones descritas (72, 50, 104); ninguna coincide con las cuotas, y la probabilidad de que al menos una coincidiera por azar es 0,17; el OSM solo añade la serie diagonal 1,3,5,…,14,…,1. La analogía con Inkawasi es **propuesta**, no bien apoyada.
- **Las copias son un efecto de archivo.** 7/20 quipus contables vs 44/631 (OR 7,2; p=0,0004), pero **0/11** fuera de Incahuasi (p=1). Pachacamac tiene 7 copias y 0 contabilidad verificable; Paracas 0 copias y 2 contables. Con n=1 archivo, no es una ley de la contabilidad.
- **El warazan es el paralelo más cercano y el más incómodo.** Escala decimal de unidades (*koku–to–sho–go–shaku–sai*), cuotas por hogar, lazo = 50 *koku*, separadores (lazo = cruce), grosor para evitar errores. Pero no es un place-value puro y no tiene árbol de cuerdas ni consolidación. El decimal anudado **no es exclusivamente andino**.
- **Uruk y Exchequer aportan el contraste clave.** Uruk usa **5 sistemas específicos del objeto** (no un decimal abstracto) y *bullae* como doble registro; el Exchequer usa £sd no decimal y un tally partido anti-fraude. Ambos tienen consolidación; ninguno publica tasa de error.
- **Los palos de mensaje son el outgroup necesario.** >1 500 objetos, pero no numéricos, sin totales, copias ni cuotas; el contenido va en la recitación memorizada. Recuerdan que no todo registro sin escritura es contabilidad (cf. Collata).
- **Recomendación inmediata.** (a) Pedir/medir el censo de hoyos por sección de Monte Sierpe; (b) buscar parejas A/B y cuotas 46/44 en los 5 quipus inéditos de Inkawasi; (c) rehacer el 8/18 con la alineación registro a registro publicada, no con “cualquier cabecera”; (d) no usar el 9 como firma cultural sin control de múltiples comparaciones.

## 9. Niveles de evidencia

- **Bien apoyado:** la aritmética de la cadena de Incahuasi (A+B, cuota suma, UR270→UR278, UR278→UR266/275), replicada por tres vías; el **exceso** de 8/18 sobre su nulo (no la tasa bruta); la distribución del ancho 9 en el corpus; la estructura decimal del warazan y la estructura por denominaciones del tally (documental); la consolidación proto-cuneiforme (Englund 2004).
- **Apoyado con datos:** la ausencia de un paralelo completo de la cadena (búsqueda exhaustiva de 13/18 y esta comparación); el efecto de copia confundido con Incahuasi; la no-comparabilidad de tasas brutas (simulación); la lectura de Monte Sierpe como contador unario (no como libro).
- **Propuesto:** la lista de rasgos universales (inferencia sobre 7 casos); la cuota como deducción/tasa; el warazan como tecnología emparentada por convergencia, no por contacto; el 9 de Collata como agrupación narrativa.
- **Especulativo:** cualquier transmisión histórica entre warazan y quipu; Monte Sierpe como “eslabón perdido” de la contabilidad andina; UR268 como nivel de periodo; el 9 como principio cosmológico compartido.
