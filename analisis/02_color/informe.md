# Color del quipu: ¿categoría, posición (columna) o nada?

Equipo 02_color. Datos: `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus del KFG). Unidad de análisis: el quipu. Semilla base 20261017 (`comun.py`), cada quipu/prueba usa `default_rng([SEED, tarea, índice_quipu, ...])`. Todo es reproducible con los scripts de esta carpeta (orden: `t1_posicion.py`, `t1b_seriacion.py`, `t2_t3_valor.py`, `resumen_t3.py`, `t3b_controles.py`, `t4_especiales.py`, `t4b_cordon_principal.py`, `t4c_sumas_agrupado.py`; ~10 min en total). Las CSV de resultados quedan en la misma carpeta.

## Respuesta corta

El color **no es "nada"** y **tampoco es un único sistema**. Los datos apoyan tres usos distintos, cada uno en un subconjunto de quipus:

1. **Posición/columna**: en una minoría de quipus (46 de 376 evaluables, 12 %, con criterio estricto) el color de la cuerda depende de su posición en el grupo, con columnas de color fijas repetidas grupo tras grupo. Con criterio laxo (solo significación) es el 47 %.
2. **Bloque/grupo y bandas**: en el 41 % de los quipus los grupos son internamente homogéneos en color, y ~48 % tienen rachas ("banding") de color más largas que el azar.
3. **Valor**: dentro del 40 % de los quipus el color predice la magnitud del valor, pero casi siempre con dirección propia del quipu. Solo hay un vocabulario compartido pequeño: **blanco/claro ↔ valores algo mayores, primera cuerda del grupo y cuerdas que son suma del resto**; **marrón oscuro KB ↔ cuerdas sin nudos** (dominado por UR). Los colores teñidos no muestran ningún vocabulario consistente (y son pocos).

Las diferencias de efecto compartido son pequeñas (AUC ±0,04–0,06). No hay evidencia de que colores mezclados marquen totales (resultado negativo).

## Preparación de los datos

- Color: se quitan los rangos `(a-b)` y se separan tokens por `: / - % * _`. Tipo de cuerda: simple (41 800), moteado `:` (11 993), barber-pole `-` (2 364), segmentado `/` (954), otro (274); 433 sin color (excluidas). Etiqueta del color = código normalizado completo (`W:AB` ≠ `W`).
- Valor: solo cuerdas con `nudos` no vacío; 0 sin nudos = ausente (30,5 % de las cuerdas). La propia ausencia de nudos se usa como resultado ("vacía") en T3.
- Posición en grupo: orden dentro de (quipu, `grupo`) solo para colgantes (nivel 0); se usan grupos de ≥3 cuerdas; posición recortada a 8.
- **Natural vs teñido (T5)**, según el diccionario `ascher_color_dc` del OKR (familia ISCC): natural = blanco, marrones, grises, negros (49 250 cuerdas); teñido = rojo, naranja, amarillo, azul, verde (5 648 cuerdas, 9,8 %); ambiguo = oliva, `PK` ("unknown Urton color"), códigos fuera del diccionario (2 487). Variante estricta (solo descriptores vivos, sin "grayish"): 1 877 cuerdas (3,3 %).
  - **Discrepancia con el encargo**: en el diccionario OKR `RL` = "light reddish brown" (familia marrón, natural), no un rojo teñido. Los rojos verdaderos son `RM`, `SR`, `VR` y son rarísimos (solo 8 quipus evaluables para valor), de modo que "rojo" no se puede contrastar.
- Nulos (todos con p empírico "mid-p" con corrección +0,5/(B+1); calibración comprobada: con color independiente 3,5 % de quipus tienen p<0,05).
- Comparaciones múltiples: **BH-FDR**, aplicado donde se indica (por variante y nulo, sobre quipus o sobre la familia de pruebas de metaanálisis). La tasa de falsos positivos esperada es 5 % de p crudos.

## Tarea 1. Color como encabezado de columna

**Estadístico**: información mutua MI(color; posición-en-grupo) por quipu (alfabeto = 8 colores más frecuentes del quipu + "otro"). Efecto normalizado nMI = (MI − media nula)/H(color).

**Nulos**: N1 permuta colores en todo el quipu; **N2 permuta dentro de cada grupo** (conserva la composición de cada grupo: es el control principal); N3 permuta el orden de los grupos completos (conserva la secuencia de colores y los tamaños de grupo, solo mueve las fronteras). Aviso: permutar grupos enteros entre sí deja la MI(color;posición) idéntica por construcción, por eso N3 se implementó como reordenación de tamaños de grupo. B = 500/1000/300. Elegibles: 376 quipus (≥3 grupos de ≥3 cuerdas, ≥12 cuerdas con color, ≥2 colores).

| Variante | n | N2 BH<0,05 | N3 BH<0,05 | "columna fuerte" (N2 y N3 BH<0,05 y nMI≥0,25) | nMI mediana |
|---|---|---|---|---|---|
| todos los colores | 376 | 178 (47 %) | 93 (25 %) | 46 (12 %) | 0,056 |
| sin 1.ª cuerda de grupo | 364 | 158 | 62 | 29 | 0,046 |
| sin 1.ª ni última | 339 | 122 (36 %) | 47 (14 %) | 24 (7 %) | 0,040 |
| solo naturales | 355 | 158 (45 %) | 84 | 47 | 0,054 |
| solo teñidos | 75 | 23 (31 %) | 13 | 7 | 0,043 |
| binario natural/teñido | 207 | 51 (25 %) | 25 | 15 | 0,051 |
| binario estricto | 89 | 19 (21 %) | 10 | 6 | 0,026 |

Metaanálisis por quipu (Stouffer de z de permutación, N2): z ≈ 102 en "todos" (p < 1e-300), quipus con p crudo<0,05: 52 %; en quipus "regulares" (≥60 % de grupos del mismo tamaño y ≥4 grupos; n=134) el 63 % (84) son significativos y la nMI mediana sube a 0,18.

**Potencia** (simulación sobre la estructura real de grupos, `resultados_t1_potencia.csv`): si el 20 % de las cuerdas copian un color de columna, el test detecta (BH) 18 %; 30 % → 53 %; 50 % → 84 %. Un quipu con columnas "ruidosas" (<30 % de cuerdas siguen la columna) pasa desapercibido; la proporción real de quipus con columna es, por tanto, **entre 12 % (estricto) y ~47 % (laxo)** y no se puede afinar más con este diseño.

**Homogeneidad intragrupo (color = etiqueta de bloque)**: fracción de pares del mismo grupo con igual color 0,413 frente a 0,306 del nulo; 171 de 415 quipus (41 %) con BH<0,05. Cruce con columna (376 quipus): solo bloque 118, solo columna 133, ambos 45, ninguno 80. Es decir, bloque y columna tienden a **excluirse** (cuando el grupo es homogéneo no hay estructura por columna).

**Seriación y bandas** (secuencia de colgantes de cada quipu, 424 evaluables con ≥20 cuerdas; nulo = permutación global; BH):

| Variante de la secuencia | n | bandas (rachas) | periódico | ambos | ninguno |
|---|---|---|---|---|---|
| completa | 424 | 196 (46 %) | 117 (28 %) | 7 | 104 (25 %) |
| solo naturales (comprimida) | 384 | 47 % | 25 % | 2 % | 27 % |
| binaria natural/teñido | 245 | 25 % | 12 % | 0,4 % | 63 % |

Estadístico de bandas = acuerdo entre cuerdas contiguas a(1); periodicidad = max_{k=2..12} a(k) − a(1) (así las rachas largas no se confunden con periodicidad). Con p crudo<0,05: bandas 51 %, periódico 33 %. El período más frecuente es k=4 (26 quipus), luego 6, 3, 2 y 5; no hay un período dominante.

**Casos y control interno.** Ejemplos claros de encabezado de columna: AS170 (7 columnas con colores fijos `LC | W-BS | W-B | G0/BS | MB/W | 0D/W | W/…` repetidos en cada grupo), AS074, UR1144 (columna 2 siempre `W:LB`), UR1113 (columnas 5 y 6 siempre `W:FR`, `W:MB`), UR1149, HP055, KH0081, y **UR267A**, el quipu que Clindaniel (2019) usa como prueba de concepto de lectura por color. En contraste, UR087 (valle del Santa; Medrano y Urton) tiene grupos de 6 cuerdas del **mismo** color (p. ej. `AB/YB` ×6): es estructura de bloque, no de columna. Al quitar la primera y última cuerda de cada grupo el efecto baja pero persiste (36 % significativos, 7 % "fuertes"), de modo que no es solo "cabecera/pie distinto".

**Cautelas:** (i) la N3 es mucho más exigente que la N2 (25 % vs 47 %): parte del efecto N2 puede venir de rachas de color combinadas con la heterogeneidad de tamaños de grupo; por eso la etiqueta "fuerte" exige ambos. (ii) Muchas "columnas" son repeticiones de un patrón de grupo; que sean *encabezados* con significado (en vez de un patrón decorativo/de fabricación, cf. los bastones envueltos de Inkawasi) no se puede decidir con estos datos. (iii) Posible duplicidad de registros de un mismo quipu entre colecciones (no comprobada).

## Tarea 2. Color ↔ magnitud del valor dentro del quipu

**Estadístico**: Kruskal-Wallis sobre rangos del valor con el color (códigos con <3 cuerdas → "otro") y tamaño de efecto ε² = (H−k+1)/(n−k). Por separado **colgantes** y **subsidiarias**. **Nulos**: Nq (permuta color en el quipu y clase), Ng (permuta dentro del grupo; para subsidiarias, dentro de la madre), Nc (desplazamiento circular del color a lo largo del quipu: conserva rachas y autocorrelación). B = 1000.

| Clase / variante | n quipus | ε² mediana | significativos BH: Nq | Ng | Nc |
|---|---|---|---|---|---|
| colgantes, todos | 365 | 0,069 | 147 (40 %) | 89/332 (27 %) | 86 (24 %) |
| colgantes, solo naturales | 346 | 0,058 | 119 | 74/309 | 76 |
| colgantes, solo teñidos | 49 | 0,046 | 13 | 5/38 | 10 |
| subsidiarias, todos | 142 | 0,076 | 48 | 14/131 | 39 |
| subsidiarias, naturales | 129 | 0,061 | 34 | 10/115 | 31 |

Metaanálisis (Stouffer): significativo con los tres nulos y en todas las variantes (BH ≈ 0). **Es un resultado positivo robusto: dentro del quipu el color y la magnitud están asociados**, también con solo colores naturales y controlando por grupo. Pero el efecto por quipu es de tamaño modesto (mediana ε² ≈ 0,07), y el resultado de T3 muestra que la dirección casi nunca es común entre quipus.

## Tarea 3. Vocabulario entre quipus (metaanálisis por quipu)

Diseño: por quipu, AUC (color X contra el resto de las cuerdas de su clase) para dos resultados, **magnitud del valor** (cuerdas con nudos) y **cuerda sin nudos**; más ρ(luminosidad Ascher, valor). Efecto por quipu = AUC − 0,5 con p y z de permutación (Nq, Ng, Nc). Entre quipus: prueba de signo (fracción de quipus con efecto>0), Wilcoxon, Stouffer, exceso de quipus con p<0,05 y BH sobre todas las combinaciones (140 por nulo: clase × resultado × color × fondo). Colores: 12 códigos simples frecuentes, moteado/barber/segmentado/cualquier mezcla/mezcla con W, familias rojo/azul/verde/amarillo, teñido amplio/estricto, natural. Mínimo 5 cuerdas con y 5 sin el color por quipu, y ≥8 quipus. Para colores naturales se repite con "fondo natural" (el resto restringido a naturales). Criterio **robusto**: BH<0,05 en los tres nulos con el mismo signo y prueba de signo p<0,05 (`resultados_t3_robustos.csv`): **21 de 140 combinaciones**.

Resultados clave (colgantes salvo indicación; eff = mediana del AUC−0,5; "%+" = % de quipus con efecto>0):

| Color / resultado | quipus | eff | %+ | por colección (%+) | lectura |
|---|---|---|---|---|---|
| **W**, valor | 227 | +0,057 | 64 % | AS 74, HP 63, KH 80, MM 50, UR 61 | blanco → valores algo mayores |
| W, valor, solo interior de grupo | 125 | +0,037 | 63 % | sin UR: n=40, +0,059, 74 % | no es efecto de bordes ni de UR |
| W, valor, fondo natural | 210 | +0,063 | 63 % | — | no es "natural vs teñido" |
| W, vacía | 237 | −0,044 | 26 % | AS 25, HP 17, KH 0, UR 30 | blanco rara vez sin nudos |
| luminosidad ρ, valor | 360 | −0,074 | 36 % | 25–40 % en 6 de 7 colecciones (QU 56 %) | más claro → más valor |
| **KB**, vacía | 54 | +0,198 | 85 % | UR 82 (n=40) | marrón oscuro → cuerda sin nudos |
| KB, vacía, sin UR | 13 | +0,29 | 85 % | | consistente pero n pequeño |
| mezclas (cualquiera), valor | 233 | −0,037 | 40 % | AS 50, HP 25, UR 40 | mezcla → valores algo menores; **no sobrevive sin UR** en el control de interior (+0,004) |
| mezclas, subsidiarias, vacía | 139 | −0,038 | 33 % | UR 34 | mezcla → subsidiaria con nudos |
| B (marrón moderado), valor, natural | 47 | −0,081 | 32 % | AS 12, UR 45 | heterogéneo, débil |

**Lo que NO se encontró (negativos):** "W siempre con valores pequeños" es falso (es al revés, y el efecto es de ±0,06 de AUC, no una regla). "Colores mezclados W:AB marcan totales": no; las mezclas tienen valores ligeramente menores (`MIX_con_W` no robusto) y, en T4, son *menos* frecuentes en cuerdas que son sumas. **Ningún color teñido** (rojo, azul, verde, amarillo, teñido amplio o estricto) tiene efecto robusto sobre valor ni sobre vacía; MB, AB, LB, YB, NB, HB, DB, GG: efectos de signo inconsistente entre quipus o inestables entre nulos (p. ej. MB valor: significativo en los tres nulos pero 41 % de quipus con signo positivo, sign p=0,06; YB valor: +0,03, 63 %, sign p=0,08).

**Control de la explicación aburrida** (`t3b_controles.py`): excluyendo primera y última cuerda de cada grupo y quitando la colección dominante (UR), los efectos de W (valor y vacía) se mantienen; el de KB-vacía se mantiene pero solo con 9–13 quipus fuera de UR; el de las mezclas se pierde. Hay que tratar el efecto KB-vacía con cautela: puede ser un artefacto de registro o conservación (cuerdas oscuras/deterioradas con nudos perdidos o no registrados) más que un código; no hemos verificado `notas` ni `terminacion`.

## Tarea 4. ¿Marcan los colores raros, mezclas y cordones principales cuerdas especiales?

**Detección de sumas** (propia, estricta): colgante con valor >0 igual a la suma de ≥2 subsidiarias directas con nudos; y primera/última cuerda de un grupo (≥3) igual a la suma del resto. Chance por permutación de valores dentro del quipu (300 perms):

- Colgante = suma de subsidiarias: **72** casos entre 1 800 candidatos (4 %), en 38 quipus; esperado por azar 45,5 (z = 4,2). Excedente real ≈ 26 casos. Contra la relación de suma de Ascher del KFG: coinciden 22 de mis 36 quipus (el KFG es menos estricto: 108 quipus).
- Primera o última cuerda del grupo = suma del resto: **118** casos entre 9 884 cuerdas de borde (1,2 %), 49 quipus; esperado 36,8 (z = 13,9). 37 de mis 41 quipus tienen "pendant–pendant sum" en el KFG.

Hay pocas sumas por quipu (<8 quipus por prueba), así que su relación con el color se evaluó con una **prueba estratificada por quipu** (el atributo se permuta *dentro* de cada quipu; segunda variante: dentro de terciles de magnitud del valor, para que "es grande" no explique "es blanca"):

| Cuerda "suma" | atributo | observado | esperado azar (Nq / Nv) | p | BH |
|---|---|---|---|---|---|
| borde de grupo = suma del resto (49 quipus, 118) | **blanca** | 54 % | 36 % / 40 % | 0,001 / 0,001 | 0,006 |
| ídem, solo colores naturales (46, 112) | blanca | 57 % | 37 % / 42 % | 0,001 | 0,006 |
| ídem | mezcla | 9 % | 18 % / 16 % | 0,005 / 0,008 | 0,02 |
| ídem | rara global / teñida | 8 % / 3 % | 9 % / 2 % | n.s. | — |
| colgante = suma de subs (33 quipus, 67) | blanca, mezcla, rara, teñida | 16 % / 19 % / 24 % / 1 % | 18 % / 19 % / 22 % / 2 % | n.s. | 1,0 |

**Colores y cuerdas estructurales, por quipu** (metaanálisis de 273–360 quipus; BH<0,05 en Nq, Ng y Nv):

- **Primera cuerda del grupo**: más blanca (+3,5 pp mediana; 56 % de quipus positivos, sign p=0,05; media +12,6 pp porque algunos quipus tienen primeras cuerdas casi siempre blancas; 27 % de quipus p<0,05), **más clara** (ρ −0,08; 64 % de 360 quipus), **menos mezclada** (−5 pp; 36 % positivos), menos color raro global (−4 pp) y menos teñida (−3 pp). Se mantiene con solo naturales y con control por valor (Nv).
- **Última cuerda del grupo**: menos blanca (−4 pp, 36 % positivos). El efecto mixto de "última = mezcla" tiene z alto pero efecto mediano 0 y 49 % de quipus positivos: no fiable.
- **Cuerda superior (union T)**: solo 8–11 quipus evaluables (154 cuerdas T en total); tendencia a más clara/menos rara, pero sin potencia. **Sin conclusión.**
- **Color raro** (rareza dentro del quipu ≤10 % o global <0,5 %) no marca cuerdas especiales; al contrario, la primera cuerda del grupo es *menos* rara.

**Cordón principal** (616 quipus con color del cordón principal; nulo: permutar el color del cordón principal entre quipus de la misma colección; B=5000): fracción de colgantes que comparten algún hilo con el cordón principal 0,51 frente a 0,34 esperado (p = 0,0002), 69 % de los quipus por encima del azar; sin contar W 0,35 vs 0,19. **Explicación aburrida probable**: el cordón principal y los colgantes de un mismo quipu usan la misma paleta/hilado (mismo taller, mismo lote de hilo); no implica significado.

## Tarea 5. Natural vs teñido: ¿cambia el resultado?

- **Columna (T1)**: no depende de los teñidos. Solo naturales: 45 % de quipus significativos (igual que con todos: 47 %); solo teñidos: 31 % (n=75, menor potencia); la **mera posición de las cuerdas teñidas entre las naturales** (binario) es estructurada en 25 % de los quipus (21 % con la definición estricta), algo que no se explicaría solo por qué material había.
- **Valor (T2)**: solo naturales ε² mediana 0,058 y 34 % de quipus BH-significativos (Nq); no cambia.
- **Vocabulario (T3)**: los **tres efectos compartidos son de colores naturales** (blanco, luminosidad, marrón oscuro KB). Con los teñidos no hay nada robusto; la muestra es pequeña (rojo: 8 quipus, azul 51, verde 90) y el color de las cuerdas teñidas actuales puede no ser el original (Milillo et al. 2023). Que W y KB sean justamente colores sin teñir **es exactamente la cautela material**: el efecto W↔valor mayor y KB↔sin nudos podría reflejar qué hilo (algodón blanco, camélido pardo/oscuro) se usaba para qué tipo de cuerda en un taller, o conservación diferencial, no una "categoría semántica".
- **Cuerdas especiales (T4)**: primera cuerda blanca/clara y borde-suma blanco persisten con solo naturales (57 % vs 37 %).

## Niveles de evidencia

| Conclusión | Nivel |
|---|---|
| Existe estructura color-posición-en-grupo (columnas con color estable) en algunos quipus y no se explica por la composición del grupo (N2) | **demostrado** (estadístico, con nulo y FDR) para esos quipus individuales; AS170, UR1144, UR1113, UR267A, etc. |
| Porcentaje de quipus con columnas: 12 % (estricto) a 47 % (laxo) | **apoyado con datos** (rango; potencia limitada, N3 más severa que N2) |
| Esas columnas son encabezados con significado (no patrón decorativo/de fabricación) | **propuesto** |
| Color como etiqueta de bloque (grupos homogéneos, 41 %) y bandas (≈48 %) | **apoyado con datos** |
| Periodicidad/seriación en ≈29 % de los quipus | **apoyado con datos** (período no dominante) |
| Color asociado a magnitud del valor dentro del quipu (40 % de quipus; 27 % con control por grupo) | **demostrado** como asociación; su semántica, **propuesta** |
| Vocabulario compartido: blanco/claro ↔ mayor valor, primera cuerda del grupo y cuerdas "suma" (borde = suma del resto) | **apoyado con datos**, efecto pequeño (AUC≈+0,04–0,06); la suma, solo 49 quipus |
| KB (marrón oscuro) ↔ cuerda sin nudos | **apoyado con datos** como patrón; causa (artefacto/código) **especulativa**; dominado por UR |
| Mezclas marcan totales / W siempre pequeño / color raro marca cuerdas especiales | **refutado en estos datos** (resultados negativos) |
| Cordón principal comparte color con colgantes | **demostrado** como correlación; probable paleta compartida (aburrida) |
| Teñidos portan vocabulario | **sin evidencia** (poca muestra; color posiblemente alterado) |
| Cuerdas superiores (T) marcadas por color | **sin conclusión** (8–11 quipus) |

## Limitaciones

- El color registrado es cualitativo (Pantone/Ascher) y puede diferir del original; Milillo et al. (2023) hallaron cuerdas mal registradas (bicolor/moteadas) y alteraciones por tafonomía/biocidas. Este análisis hereda esa incertidumbre; el único antídoto aquí fue la comparación natural/teñido.
- La parte significativa del color son W y marrones: los *mismos* colores que aporta el material disponible. No separamos algodón de camélido (el KFG no trae fibra por cuerda en `cuerdas.csv`).
- Los z de Stouffer son enormes porque los quipus grandes pesan más; por eso se reportan también la fracción de quipus con efecto y la prueba de signo. Cuando la fracción de quipus positivos es cercana a 50 %, la significación del Stouffer es engañosa (p. ej. "última cuerda mixta").
- Los nulos asumen intercambiabilidad dentro del quipu (o dentro de grupo/valor/ciclo). Los controles Nc/Ng/Nv cubren rachas, grupos y tamaño del valor, pero no la posición en el eje cm de la cuerda ni el tipo de nudo.
- T4 sumas: pocas sumas por quipu; la prueba agrupada depende de 33–49 quipus y de unos pocos con muchas sumas.
- Procedencia museística no usada como origen. No se analizaron los colores *segmentados* por tramo (los rangos se eliminaron).

## Ideas para la siguiente ronda

1. **Decodificar las columnas**: en los 46 quipus de columna fuerte, ver si el color de columna se asocia con el tipo de nudo o con el orden decimal (unidades/decenas) del valor, o con relaciones de suma entre columnas (Santa valle, UR087–092: ¿color de bloque? ¿nombre del tributario?).
2. **Subconjunto con sumas**: construir un catálogo de las 118+72 sumas y comprobar si el color blanco marca *siempre* la suma dentro de cada quipu (por quipu, no agrupado), y si invierten roles (UR255 de Clindaniel).
3. **KB-vacía**: revisar `notas`, `terminacion`, `union` y metadatos de conservación de esas cuerdas; probar si es artefacto (cuerdas rotas, color oscuro por suciedad).
4. **Material**: cruzar con fibra del OKR (`fiber_dc`) por cuerda para separar algodón y camélido, y con el análisis de tintes de Milillo (datos XRF Zenodo).
5. **Estructura de los colores segmentados** (`MB(0–7)/W(7–35)`: color por tramo) y mezclas `:` frente a `-`: ¿son lo mismo que "pares de colores" de los bastones envueltos?
6. Repetir T1 con grupos definidos por el color (no por el espacio) para ver si las "columnas" cambian cuando se redefinen los grupos.
