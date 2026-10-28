# La tasa de Guancayo (1571) y las 9 columnas de UR278

**Equipo:** investigación de la fuente primaria para las 9 columnas.
**Carpeta:** `analisis/ds/n_espinoza1963/`.
**Fecha:** 18 de octubre de 2026.
**Semilla:** 20261018 (todas las permutaciones y remuestreos).
**Datos:** `analisis/fuentes_txt/RMN_XXXII.txt` (Espinoza Soriano 1963, *La guaranga y la reducción de Huancayo*, Revista del Museo Nacional XXXII), `analisis/fuentes_txt/Rostworowski_CostaPeruana.txt`, `analisis/datos/cuerdas.csv`, `analisis/datos/quipus.csv`, `analisis/13_sistema_incahuasi/ur278_tabla.csv`, `analisis/ds/n_nueve_unidades/ur270_*.csv`.
**Scripts:** `01_visita.py`, `02_grupos9.py`, `03_ur278.py`, `04_ur270.py`, `05_busqueda_tasa.py`, `06_perfiles.py`.
**Salidas:** `visita1571.csv`, `grupos9.csv`, `pruebas_grupos9.csv`, `ur278_filas.csv`, `ur278_pruebas.csv`, `ur278_pruebas_parametrico.csv`, `ur270_filas.csv`, `ur270_pruebas.csv`, `busqueda_tasa.csv`, `busqueda_tasa_ventanas.csv`, `perfiles.csv`, `perfiles_pruebas.csv`, `salida_0*.txt`.

---

## 1. Pregunta

La pregunta del equipo es si las 9 columnas de UR278 (y los grupos de 9 cuerdas de otros quipus) pueden ser las 9 pachacas de una guaranga, y si el quipu de la tasa de Guancayo que describe la Visita de Juan Martínez Rengifo (1571) permite identificar qué registran esas columnas.

La tarea tiene cinco partes: (1) extraer de la Visita todo lo cuantitativo; (2) ver si algo varía entre las 9 pachacas y comparar su perfil con la firma de UR278; (3) probar la predicción “tasa = filas de 9 valores iguales” frente a “entrega = filas desiguales” en UR278; (4) repetir el diagnóstico en UR270 y en todos los grupos de 9 del corpus; (5) describir cómo se vería en cuerdas el quipu de la tasa y buscarlo en el corpus.

**Advertencia de método:** el documento no es una descripción neutral. Es una visita administrativa española de 1571, copiada en 1584, con OCR sucio y con una interpretación previa (Espinoza) que ha contaminado la literatura. El texto que publica Espinoza es un traslado de 1584 de un capítulo de la Visita, presentado en la Audiencia de Los Reyes por Pedro Atao (`RMN_XXXII.txt:2771-2795`). Separé siempre lo que dice el manuscrito de lo que dice el comentario de Espinoza. Las líneas que cito son las del `.txt`, no las del manuscrito.

---

## 2. La fuente: qué dice la Visita y dónde está

### 2.1 El documento es del valle del Chillón, no de Huancayo

Este es el resultado más importante de la primera parte, y condiciona todo lo demás. La Visita no se hizo en Huancayo (Jauja), sino en el valle del Chillón, en los pueblos de Guancayo, Maca y Guarauni, cerca de Yangas. La prueba está en el propio texto:

- “hay de aquí a la dicha ciudad [Los Reyes] siete leguas” (`RMN_XXXII.txt:3216`). Huancayo está a unos 250 km de Lima, unas 40-50 leguas; siete leguas sitúan el lugar en el Chillón.
- “este río de Collique” (`:3385`), el río del valle del Chillón.
- La chacra de Francisco de Talavera y las haciendas de Gonzalo de Cáceres, Juan Pizarro y Antonio de Rivera (`:3481`), todos del valle de Lima/Chillón.
- El encomendero es el contador Juan de Cáceres (`:3482`), y los caciques se declaran sujetos a Gonzalo de Cáceres (`:3301`).
- Los productos de las chacras son coca, algodón, ají y mates (`:3251-3255`), propios de la franja yunga, no del valle del Mantaro.
- La cédula de encomienda de 1542 dice que el contador no tenía “yndios yungas en este valle de Lima” y le encomienda al cacique Chuquyn parco “en el valle de Guancallo” (Rostworowski, `Rostworowski_CostaPeruana.txt:333-334`).

Rostworowski ya lo había mostrado con archivo y toponimia: “los guancayos… vivían en el Chillón y no tenían nada que ver con la moderna ciudad del mismo nombre situada cerca de Jauja” (`Rostworowski:318`), y “se trata de un grupo yunga cuyo nombre es similar a otra toponimia en la región de Jauja” (`Rostworowski:338`). Espinoza, en cambio, tituló el artículo “La guaranga y la reducción de Huancayo” y situó el documento en la región wanka. **La atribución wanka es un error de Espinoza; la lectura yunga del Chillón es la correcta.** Nivel: **bien apoyado** por la distancia, el río, los encomenderos y los productos.

Consecuencia: la “guaranga de Huancayo” de 900 tributarios y 9 pachacas no es una guaranga wanka. Es un señorío yunga del Chillón, organizado por el Estado inca (o por el visitador) en 9 pachacas de 100 tributarios. Sigue siendo un caso válido de organización decimal, pero no es el caso wanka que la literatura cita.

### 2.2 Errores y tensiones del artículo de Espinoza

El artículo es útil, pero contiene errores que hay que corregir antes de usarlo como fuente de datos:

| dato | artículo de Espinoza | Visita (texto) | comentario |
|---|---|---|---|
| pachacas de Guancayo | 9 | “cinco pachacas” (`:2820`), pero lista 5 curacas con 2+1+2+2+2 = 9 (`:2832-2833`) | el “cinco” parece error de copia/OCR; la lista suma 9 |
| Maca en 1571 | 170 tributarios (línea 845) | 190: 90 en Maca + 100 en Misayo (`:3057-3059`) | 90+100=190; el artículo se contradice con su propia cuenta |
| chacras de Guarauni | 4, y “en ninguna sembraron maíz” (línea 844) | 5, y la primera (Atum) “hace cinco hanegas de sembradura de maíz” (`:3255`) | error del artículo |
| mita de Los Reyes | 8 indios | 8, pero reparte 2 Maca + 3 Guarauni + 2 Guancayo = 7 (`:3214-3216`) | falta uno, o el total está mal |
| “9 productos” | 9 rubros (líneas 1184-1188) | 12 rubros en la lista de la Visita (`:3151`), porque agrega 5 petaquillas de coca, 2 de camarones y 10 pares de rodejones | el “9” es una selección editorial de Espinoza, no una lista nativa de 9 |
| fanegas de las chacras | “nueve fanegadas de maíz” (línea 777) | 3 chacras × 3 fanegas “de sembradura” (`:3251-3255`) | el total 9 coincide, pero la Visita dice fanegas de semilla, no una medida de área literal |

Estos errores no invalidan la Visita, pero sí invalidan varias cifras que circulan en la literatura. El `visita1571.csv` usa el texto de la Visita y marca con `epoca` las filas derivadas o calculadas.

### 2.3 La Visita en números

El archivo `visita1571.csv` tiene 119 filas con la estructura pedida (`unidad, nivel, nombre, cantidad, unidad_medida, epoca, linea`). Las líneas 700-1200 son comentario de Espinoza (incluida la lista de 9 productos y los totales ×9); las líneas 2780-3483 son la Visita. Las cifras centrales:

| qué | cantidad | unidad | época | línea |
|---|---:|---|---|---|
| tributarios de Guancayo | 900 | tributarios | Inca | 2820 |
| pachacas de Guancayo | 9 | pachacas | Inca | 731, 2832-2833 |
| tributarios por pachaca | 100 | tributarios | Inca (derivado 900/9) | 747 |
| curacas | 5 (1 de guaranga + 4 de pachaca) | curacas | Inca | 747 |
| Mongoy/Moncoy | 2 pachacas | pachacas | Inca | 2832 |
| Cancay/Caycay | 1 pachaca | pachacas | Inca | 2832 |
| Chuquitanga/Chuquitunca | 2 pachacas | pachacas | Inca | 2832 |
| Chumbillán | 2 pachacas | pachacas | Inca | 2832 |
| Antachumbi/Aritachumbi | 2 pachacas | pachacas | Inca | 2833 |
| Guarauni | 200 | tributarios | Inca | 2975 |
| Guarauni | 2 | pachacas | Inca | 835 |
| Maca en 1571 | 190 (90 Maca + 100 Misayo) | tributarios | 1571 | 3057-3059 |
| Misayo: tributarios residentes en Maca | 10 | tributarios | 1571 | 3080-3090 |
| Misayo: los 10 con mujeres e hijos | 32 | personas | 1571 | 845 |
| Guancayo en 1571: pachacas extinguidas | 7 | pachacas | 1571 | 2949-2957 |
| Guancayo en 1571: pachacas con descendencia | 2 (las de Mongoy) | pachacas | 1571 | 2949-2957 |

La Visita **no da los nombres de las 9 pachacas**; solo los de los 5 curacas. Espinoza reconoce que no se sabe con exactitud el nombre de los nueve ayllos o pachacas (artículo, línea 749). Los nombres que sí aparecen son los de los curacas: Mongoy/Moncoy, Cancay/Caycay, Chuquitanga/Chuquitunca, Chumbillán y Antachumbi/Aritachumbi (`:2832-2833`).

La tasa anual de **cada pachaca** al Inca, según la lista de la Visita (`:3149-3151`):

| producto | cantidad | unidad |
|---|---:|---|
| coca | 5 | cestos grandes |
| ropa de algodón (mitad hombre, mitad mujer) | 26 | piezas |
| cumbi galano | 2 | piezas/trajes |
| maíz | 3 | fanegas |
| ají | 4 | cestos grandes |
| ojotas | 20 | pares |
| charqui de pájaros secos | 10 | petacas |
| guabas secas | 3 | petaquillas |
| manta de algodón para hamaca | 1 | manta |
| **para el Inca** |  |  |
| coca de zuara | 5 | petaquillas |
| camarones secos | 2 | petaquillas |
| **para los orejones** |  |  |
| rodejones de palo | 10 | pares |

Además, para las mamaconas, cada pachaca daba al año: 10 pocchas de maíz = 5 fanegas, 10 pocchas de frijoles = 5 fanegas, 10 ollas grandes y chicas, y 5 cargas de algodón por hilar (`:3151`). El repartimiento entero cuidaba 300 cabezas de ganado de la tierra (`:3151`), daba 3 hijos de caciques para servicio del Inca, 3 indios para guardar a las mamaconas y 10 indias escogidas (`:3153`).

El curaca principal recibía, por año: 5 sementeras de maíz de 4 pocchas cada una (2 fanegas cada una, 10 fanegas en total), una chacra de ají, una de frijoles de fanega y media, una de calabaza, una de yuca, una chacra grande de coca que daba 20 cestos por mita, una de algodón, 10 indios hamaqueros, 5 muchachos pajes y 2 viejos porqueros (`:3162-3170`). Cada indio le daba además un carnero de la tierra al año (`:3183`).

La mita colonial a Los Reyes era de 8 indios, repartidos 2 en Maca, 3 en Guarauni y 2 en Guancayo (`:3214-3216`). Los caciques tenían 4, 4 y 3 muchachos de servicio, respectivamente (`:3220`); a cada muchacho casado se le daba una pieza de ropa para él y otra para su mujer al año (`:3230`). La tasa del encomendero era de 60 piezas de ropa, y cada tributario pagaba 4 pesos al año para esa ropa (`:3238`); había una derrama de 2 tomines por indio, mujer e hijo para un ornamento, cobrada cuatro años antes (`:3240`).

Las chacras comunales de Guancayo eran 9 (`:3251-3255`): Atuncama (3 fanegas de maíz de sembradura), Pircay (tinta colorada), Curpa (algodón), Llamavilla (mates), Pampavilla (coca), Camasca (3 fanegas de maíz), Vitoc (3 fanegas de maíz), Cancavilla (coca) y Achuan (ají). Las tres de maíz suman 9 fanegas de sembradura, no 9 fanegas de cosecha. Guarauni tenía 5 chacras (Atum, 5 fanegas de maíz; Corupa, coca; Vitrito, ají; Pequepe, ají; Camac, mates). Maca tenía 6 (Capa, 5 fanegas de maíz; Cudcuy, 5 fanegas de maíz; Guaynacapa, coca, que antiguamente daba 50 cestos; Guacllav; Guadccy, algodón; Quillaque).

### 2.4 Mitas, turnos y cestos por mita

La cosecha de coca se hacía en **dos mitas** al año (`:3341`). El curaca principal sacaba **20 cestos por mita** de su chacra grande de coca (`:3170`), es decir, 40 cestos al año. El curaca de Guarauni, de rango inferior, sacaba **20 cestillos al año** en las dos mitas (`:3351`), es decir, 10 por mita, la mitad que el principal. Los indios comunes de Guarauni sacaban **2 cestillos al año** en las dos mitas (`:3341`), es decir, 1 por mita. La diferencia cesto/cestillo es de escala: el cesto es la unidad grande (probablemente el *runcu*), el cestillo la unidad pequeña.

### 2.5 Unidades de medida: lo que está y lo que no está

La Visita usa: **cesto** (coca, ají), **cestillo** (coca), **petaca** (charqui), **petaquilla** (coca, camarones, guabas), **fanega/hanega** (maíz, frijoles; también “fanegas de sembradura” como medida de la chacra), **pocha/poccha** (10 pocchas = 5 fanegas, luego 1 pocha = 1/2 fanega), **carga** (algodón), **manta** (ropa), **par** (ojotas, rodejones), **olla**, **peso**, **tomín**, **legua**, **carnero de la tierra**.

**“Runcu” no aparece en la Visita.** Lo que aparece es “cesto” y “cestillo”. Rostworowski define *runcu* en otro capítulo como el cesto grande usado para medir coca y ají, con subdivisiones *checta runcu* (media canasta), *cutmu* (cuarta parte) y *sillcu* (octava) (`Rostworowski:5154`). Es un término lexicográfico/etnográfico, no una palabra del documento de 1571. Por eso, si se quiere decir que las 9 pachacas daban “5 runcus de coca”, hay que aclarar que es una equivalencia interpretativa, no una cita.

### 2.6 Lo que la Visita no dice

- No da el número de tributarios de Guancayo en 1571; solo dice que 7 de las 9 pachacas se extinguieron y que sobreviven las 2 de Mongoy (`:2949-2957`).
- No dice que las 9 pachacas tuvieran 100 tributarios cada una en 1571; los 100 son el ideal/derivado de 900/9 en tiempo del Inca.
- No da el número de mitayos por pachaca; la mita a Lima se reparte por pueblo (2/3/2), no por pachaca.
- No da fanegas de cosecha de las chacras; da fanegas de sembradura.
- No da colores ni posición de las cuerdas de un quipu. La Visita es un documento escrito; no hay un quipu descrito en ella.
- No dice que los 9 rubros de la lista sean 9; la lista tiene 12 categorías y Espinoza selecciona 9.

---

## 3. Tarea 2: ¿qué varía entre las 9 pachacas?

### 3.1 Lo que la Visita dice que es igual

La Visita es explícita: cada una de las 9 pachacas de Guancayo daba **la misma lista** de productos al Inca (`:3121`: “de las pachacas de Guancayo que eran nueve cada una de las cosas siguientes”), y el reparto entre pachacas era igual (“el repartimiento entre las pachacas tanto al uno como al otro”, `:3194`). En tiempo del Inca, las 9 pachacas tenían 100 tributarios cada una (900/9). Es decir, el perfil de tasa por pachaca es **plano**: 9 valores iguales.

### 3.2 Lo que varía: solo la supervivencia en 1571

El único dato que varía entre las 9 pachacas es la extinción: en 1571 sobreviven 2 pachacas (las de Mongoy) y 7 están extinguidas (`:2949-2957`). Eso da un perfil binario `[100, 100, 0, 0, 0, 0, 0, 0, 0]`, no un perfil gradual. Los demás datos no son por pachaca:

- **Chacras:** las 9 chacras comunales son de la guaranga, no de cada pachaca; las 9 pachacas las poseen en común (artículo, línea 775). Lo que varía es el cultivo de cada chacra (3 de maíz, 1 de tinta, 1 de algodón, 1 de mates, 2 de coca, 1 de ají), no la pachaca.
- **Mitas:** la mita de Lima se reparte por pueblo (2 Maca, 3 Guarauni, 2 Guancayo), no por pachaca.
- **Tasa:** idéntica en las 9 pachacas.
- **Curacas:** lo que varía es el número de pachacas por curaca (2,1,2,2,2), no un valor económico por pachaca.

### 3.3 Comparación con la firma de UR278

La firma de UR278 (24 filas de 9 cuerdas) es un perfil gradual, no plano:

| perfil | CV | max/min | forma |
|---|---:|---:|---|
| tasa por pachaca (9 iguales) | 0,000 | 1,00 | plano |
| productos (5,26,2,3,4,20,10,3,1) | 1,019 | 26,00 | muy sesgado |
| productos ×9 (45,234,18,27,36,180,90,27,9) | 1,019 | 26,00 | muy sesgado |
| supervivencia 1571 (2 vivas / 7 extintas) | 1,871 | ∞ | 7 ceros |
| chacras de maíz (3 chacras × 3 fanegas) | 1,414 | ∞ | 6 ceros |
| **UR278 (columnas)** | **0,1765** | **1,75** | gradual |

La conclusión es negativa en las tres comparaciones posibles:

1. **Si las columnas son pachacas**, la tasa predice 9 columnas iguales; UR278 tiene un gradiente de 1,75× (c1 0,135, c8 0,080) y un efecto de columna fuerte (Friedman p = 0,0002, ya bien apoyado en `n_nueve_unidades`). **No coinciden.**
2. **Si las columnas son productos**, el perfil de productos es 26 veces máximo/mínimo, mucho más sesgado que UR278 (1,75×). La correlación en el orden documentado es r = 0,712 (p = 0,015), pero es exploratoria: el orden de la lista no está justificado independientemente, y la mejor asignación post hoc de los 9 productos a las 9 columnas llega a r = 0,867. Con 9! órdenes posibles, encontrar r ≥ 0,712 es fácil; no es evidencia.
3. **Si el perfil es la supervivencia de 1571**, hay 7 ceros; UR278 no tiene ningún cero. La correlación con las dos pachacas vivas en c1-c2 es r = 0,713 (p = 0,015), pero es el máximo posible sobre las 36 colocaciones de dos valores no nulos: no es un contraste válido. La forma (7 ceros) es incompatible con UR278.

**Resultado:** no hay ningún dato que varíe entre las 9 pachacas y que reproduzca la firma de UR278. La única estructura que coincide es el **número** de bloques: 4 curacas con 2 pachacas + 1 con 1 = 4 pares + 1 suelto, que es también la forma del mejor emparejamiento de UR278 (aunque los pares concretos difieren). Eso se prueba en la sección 7.

---

## 4. Tarea 3: ¿UR278 mezcla filas de tasa y de entrega?

### 4.1 Las filas planas

UR278 tiene 24 filas de exactamente 9 cuerdas (26 si se recortan los grupos 18 y 32 a c1-c9). La distribución de planitud (CV dentro de fila, es decir, desviación típica / media de los 9 valores) es:

| grupo | fase | total | CV | rango | distintos | igualdades exactas |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 3618 | **0,059** | 62 | 5 | 10 |
| 1 | 1 | 1506 | **0,064** | 32 | 8 | 1 |
| 11 | 1 | 4273 | **0,108** | 119 | 7 | 2 |
| 14 | 1 | 2950 | **0,116** | 106 | 9 | 0 |
| 3 | 1 | 2919 | **0,132** | 109 | 9 | 0 |
| 19 | 2 | 2105 | 0,160 | 122 | 9 | 0 |
| … |  |  |  |  |  |  |
| 18 | 2 | 1749 | 0,597 | 416 | 9 | 0 |

No hay ninguna fila con los 9 valores exactamente iguales ni con rango ≤ 1. Las filas “planas” son casi planas: la más plana (g0) tiene 5 valores iguales a 415, uno 414, uno 413, y dos valores bajos (353 y 363). La segunda (g1) tiene 8 valores entre 145 y 177. Es decir, no son filas de tasa perfecta; son filas con una fuerte compresión alrededor de un valor central.

### 4.2 Nulos

Usé tres nulos, porque cada uno controla una cosa distinta:

1. **Filas barajadas (N1):** se barajan las 216 celdas de la matriz 24×9. Rompe el efecto de fila y la asociación entre columnas; conserva la distribución global de valores.
2. **Columnas barajadas (N2):** se baraja cada columna entre filas por separado. Conserva el perfil de columnas y la marginal de cada columna; rompe la asociación entre columnas.
3. **Nulo paramétrico (N3):** se simula `x_ij = T_i · p_j · exp(z_ij)`, con `T_i` el total observado de la fila, `p_j` el perfil observado de columnas y `z_ij ~ N(0, σ_j)` con la dispersión observada de cada columna. Conserva el total de fila, el perfil de columnas y la dispersión de cada columna; rompe la covariación entre columnas. Es el nulo correcto para preguntar si una fila es más plana de lo que se esperaría dado el perfil y el tamaño.

Resultados (24 filas; 20 000 réplicas):

| estadístico | observado | N1 filas | p | N2 columnas | p | N3 paramétrico | p |
|---|---:|---:|---:|---:|---:|---:|---:|
| CV medio | 0,259 | 0,400 | 0,00005 | 0,402 | 0,00005 | 0,289 | **0,019** |
| filas CV ≤ 0,15 | 5 | 0,015 | 0,00005 | 0,012 | 0,00005 | 0,42 | **0,0002** |
| filas CV ≤ 0,10 | 2 | 0,001 | 0,00005 | 0,001 | 0,00005 | 0,023 | **0,00025** |
| igualdades exactas (36 pares) | 36 | 4,34 | 0,00005 | 4,27 | 0,00005 | 3,48 | **0,00005** |

UR278 es más plano que los tres nulos, pero el tamaño del efecto depende mucho del nulo: contra N1/N2 el CV medio baja de 0,40 a 0,26 (un 35 %), pero contra N3 baja solo de 0,289 a 0,259 (un 10 %). La mayor parte de la “planitud” se explica por el perfil de columnas y el tamaño de fila; queda un exceso de cola: 5 filas con CV ≤ 0,15 frente a 0,42 esperadas, y 2 con CV ≤ 0,10 frente a 0,023.

Por fila, contra N3 y con Holm sobre 24 filas:

| grupo | CV | p bruto | p Holm |
|---:|---:|---:|---:|
| 0 | 0,059 | 0,0001 | **0,0024** |
| 1 | 0,064 | 0,00015 | **0,0035** |
| 11 | 0,108 | 0,0017 | **0,037** |
| 14 | 0,116 | 0,0036 | 0,076 |
| 3 | 0,132 | 0,0072 | 0,143 |
| 19 | 0,160 | 0,026 | 0,503 |

Tres filas (g0, g1, g11) sobreviven a Holm al 5 %; g14 queda en el límite. Son filas genuinamente planas incluso después de controlar el perfil y el tamaño.

### 4.3 Fase y tamaño: la explicación aburrida

Las 5 filas con CV ≤ 0,15 están todas en la fase 1 (grupos < 15). La probabilidad exacta de que 5 de 5 estén en las 14 filas de la fase 1 es `C(14,5)/C(24,5) = 0,047`. Es nominalmente significativa, pero **desaparece al controlar el tamaño**:

- Las filas de la fase 1 son más grandes: total medio 2632 frente a 1775 en la fase 2.
- El CV correlaciona negativamente con el log del total: r = −0,428 (p = 0,037); a mayor total, menor CV por puro ruido de conteo.
- Después de quitar el efecto de `log(total)`, la diferencia de residuo entre fases es −0,030, y la permutación de etiquetas de fase da p = 0,757.

Es decir: **la concentración de filas planas en la fase 1 se explica porque las filas de la fase 1 son más grandes**, no porque haya un régimen de tasa distinto. La planitud sobreviviente de g0/g1/g11 es real, pero no es un fenómeno de fase.

### 4.4 ¿Hay una mezcla de dos componentes?

Ajusté mezclas gaussianas sobre `log(CV)` con 1, 2 y 3 componentes:

| k | BIC | AIC | pesos | medias |
|---:|---:|---:|---|---|
| 1 | **46,19** | 43,83 | 1,00 | −1,476 |
| 2 | 46,65 | **40,76** | 0,73 / 0,27 | −1,193 / −2,228 |
| 3 | 49,42 | 40,00 | 0,75 / 0,17 / 0,08 | −1,201 / −2,049 / −2,789 |

El BIC favorece **una** componente (ΔBIC = 0,46, prácticamente empate); el AIC favorece dos. La componente baja de la mezcla de 2 incluye g0, g1, g3, g11, g14 y g19, es decir, no es una clase limpia de fase 1 (incluye g19, de fase 2). **No hay evidencia sólida de una mezcla de filas de tasa y de entrega.** Lo que hay es una cola de 2-3 filas excepcionalmente planas, no una segunda población.

### 4.5 Veredicto de la tarea 3

- **Hay filas planas reales:** g0, g1 y g11 son más planas que el nulo paramétrico (Holm < 0,05); g14 queda cerca.
- **No hay una mezcla de dos poblaciones:** el BIC favorece una sola; la “clase plana” no es estable ni coincide con una fase.
- **La fase 1 no es un régimen de tasa:** su ventaja desaparece al controlar el tamaño (p = 0,757).
- **Propuesto, no bien apoyado:** UR278 podría contener 2-3 registros de tasa o de un solo ítem repetido, mezclados con 21-22 registros de entrega variable. La evidencia es de cola, no de mezcla.

Nivel: **apoyado con datos** que hay 2-3 filas excepcionalmente planas; **no apoyado** que UR278 sea una mezcla de tasa y entrega; **propuesto** que esas filas sean registros de tasa.

---

## 5. Tarea 4: UR270 y todos los grupos de 9 del corpus

### 5.1 UR270

UR270 tiene 6 grupos de 9 con colgante (P) y primera subsidiaria (S1) completos. Es la fuente de 6 filas de UR278, así que sirve de control de la suma P+S1.

| matriz | CV de las 6 filas | filas CV ≤ 0,15 | igualdades exactas | p (global) |
|---|---|---:|---:|---:|
| P+S1 | 0,235–0,494 | 0 | 2 | 0,187 |
| P (colgante) | 0,256–0,611 | 0 | **22** | **0,0000** |
| S1 (subsidiaria) | 0,257–0,464 | 0 | 3 | 0,614 |

No hay ninguna fila de 9 plana en UR270: el CV mínimo es 0,235 (P+S1) y 0,256 (P). El nulo paramétrico no muestra un exceso de planitud (CV medio P+S1 0,329 observado vs 0,326 nulo, p = 0,57). **UR270 no replica las filas planas de UR278.**

Pero hay un detalle importante: **P tiene 22 igualdades exactas, 16 de ellas en el grupo 6**, cuyos valores son `[200, 200, 100, 100, 100, 200, 200, 100, 100]`. Es un patrón binario de 100/200, no una fila plana. S1, en cambio, es irregular (`[70, 97, 58, 61, 61, 92, 41, 54, 59]`), y P+S1 queda en un término medio. Esto sugiere una hipótesis distinta: **P podría ser la cuota/tasa (redonda, binaria) y S1 la entrega real (irregular); UR278, al sumar P+S1, mezcla las dos.** Es una hipótesis propuesta, no bien apoyada, y con n = 6 no se puede cerrar. Pero es la pista más interesante de UR270 y explica por qué las filas de UR278 no son ni perfectamente planas ni perfectamente irregulares.

### 5.2 El corpus: 237 grupos de 9

Definición: grupos con exactamente 9 colgantes de nivel 0, todos anudados, valores > 0. Hay **238** grupos de 9 con 9 valores anudados; 237 con todos > 0. La distribución de planitud:

| estadístico | observado | nulo (barajar dentro de cada quipu) | p |
|---|---:|---:|---:|
| grupos con 9 valores iguales | **5** | 1,19 | **0,0001** |
| grupos con rango ≤ 1 | **6** | 1,83 | **0,0007** |
| grupos con CV ≤ 0,05 | **5** | 1,19 | **0,0001** |
| grupos con CV ≤ 0,10 | **7** | 1,26 | **0,0001** |
| igualdades exactas (suma de 36 pares) | **877** | 584 | **0,0001** |

Los 5 grupos con 9 valores iguales son:

| quipu | grupo | valor | vector |
|---|---:|---:|---|
| AS018 | 0 | 70 | 70 × 9 |
| AS207A | 7 | 10 | 10 × 9 |
| MM019 | 5 | 2 | 2 × 9 |
| MM019 | 6 | 2 | 2 × 9 |
| MM019 | 8 | 2 | 2 × 9 |

Los 7 con CV ≤ 0,10 agregan UR278 g0 y g1 (CV 0,059 y 0,064), que no son exactamente iguales. El CV medio de los 237 grupos es 0,808 y la mediana 0,742; solo el 2,9 % tiene CV ≤ 0,10. Es decir, los grupos de 9 son normalmente muy desiguales; los pocos planos son una excepción real.

El nulo baraja las cuerdas dentro de cada quipu, conservando la distribución de valores del quipu y el número/tamaño de sus grupos. Así, un quipu con muchos doses (MM019) tiene más probabilidad de producir un grupo de doses por azar; aun así, MM019 produce 3 grupos de 2 y el nulo espera 0,036, p = 0,0001. AS207A produce un grupo de 10 y el nulo espera 0,000, p = 0,0001; AS018 es trivial (solo tiene 9 cuerdas, todas 70, así que el nulo también da 1, p = 1).

Holm por prueba, sobre los 96 quipus que tienen al menos un grupo de 9 (6 pruebas: 9 iguales, rango ≤ 1, CV ≤ 0,05, CV ≤ 0,10, igualdades exactas y CV medio):

| quipu | prueba | observado | p bruto | p Holm |
|---|---|---:|---:|---:|
| AS207A | 9 iguales | 1 | 0,0001 | **0,0096** |
| MM019 | 9 iguales | 3 | 0,0001 | **0,0096** |
| MM019 | rango ≤ 1 | 3 | 0,0002 | **0,0192** |
| AS207A | rango ≤ 1 | 1 | 0,0007 | 0,0665 |
| UR265 | rango ≤ 1 | 1 | 0,0157 | 1,000 |
| AS018 | 9 iguales | 1 | 1,000 | 1,000 |

En igualdades exactas sobreviven Holm: AS207A, MM019, QU013 (28 igualdades), UR270 (22), UR278 (36) y UR113 (18); AS026B, AS128, QU002, UR265, UR283, UR120, UR001, HP030, UR123, UR199, UR277, UR1107, HP056, UR195 no sobreviven.

**Lectura:** la convención de escribir 9 cuerdas iguales existe y es más frecuente que el azar, pero es rara (5/237) y está concentrada en tres quipus (AS018, AS207A, MM019). Los valores son constantes simples (2, 10, 70), no una lista de 9 productos. La explicación aburrida —“9 cuerdas que cuentan 9 veces el mismo ítem” (por ejemplo, 9 unidades de 2, o 9 lotes de 10)— explica estos casos sin necesidad de una tabla de tasa. No hay ningún quipu con una matriz 9×9 de grupos constantes.

---

## 6. Tarea 5: cómo se vería el quipu de la tasa de Guancayo y búsqueda en el corpus

### 6.1 Diseño en cuerdas

La tasa de Guancayo es 9 productos × 9 pachacas. Hay dos disposiciones naturales:

**(A) Una pachaca por grupo, 9 productos por grupo.** La cuerda principal lleva 9 grupos; cada grupo tiene 9 colgantes, uno por producto. Cada grupo repite el mismo vector `[5, 26, 2, 3, 4, 20, 10, 3, 1]`. Son 81 colgantes; los 9 grupos son idénticos en valores (pueden cambiar de color para marcar el producto o la pachaca). Cada colgante se anuda con 1-2 racimos: 5 = 5 simples unidades; 26 = 2 simples decenas + 6 simples unidades; 2 = 2 unidades; 3 = 3 unidades; 4 = 4 unidades; 20 = 2 decenas; 10 = 1 decena; 1 = 1 unidad. Visualmente es un “damero de gemelos”: 9 grupos de 9 cuerdas con los mismos racimos en la misma posición.

**(B) Un producto por grupo, 9 pachacas por grupo.** La cuerda principal lleva 9 grupos, uno por producto; cada grupo tiene 9 colgantes iguales (las 9 pachacas). El grupo de coca son 9 cuerdas de 5; el de ropa, 9 de 26; el de cumbi, 9 de 2; etc. También son 81 colgantes, pero ahora cada grupo es constante y los valores por grupo son 5, 26, 2, 3, 4, 20, 10, 3, 1. Es la forma más fácil de reconocer: **9 bloques de 9 valores iguales, con valores distintos entre bloques**.

**(C) Si el quipu registra los totales de la guaranga**, no hay 81 cuerdas sino 9: una por producto, con los valores `45, 234, 18, 27, 36, 180, 90, 27, 9` (los ×9 de Espinoza). Es un solo grupo de 9 cuerdas desiguales, no un damero.

El corpus tiene quipus de 100-180 cuerdas (UR1140, UR1136), así que 81 cuerdas no es un tamaño imposible. La ausencia de la forma no se debe a que el corpus no tenga quipus grandes.

### 6.2 Búsqueda

Busqué las tres formas en los 651 quipus del KFG:

1. **Grupos de 9 con el multiset exacto** `[5,26,2,3,4,20,10,3,1]` o `[45,234,18,27,36,180,90,27,9]`: **0 coincidencias**.
2. **Grupos de 9 constantes** con un valor de la lista de productos: AS207A g7 = 10 × 9; MM019 g5, g6, g8 = 2 × 9. Ninguno con 5, 26, 3, 4, 20, 1, 45, 234, 18, 27, 36, 180, 90 o 9.
3. **Quipus con ≥ 9 grupos de 9:** UR278 (24 grupos, 0 constantes), UR1140 (20, 0), UR1136 (18, 0), UR1131 (11, 0). Ninguno es una matriz de grupos constantes.
4. **Grupos de 9 con el mismo vector repetido en el mismo quipu:** solo MM019 (g5 = g6 = g8 = 2 × 9). No hay 9 grupos iguales.
5. **Ventanas de 9 colgantes consecutivos proporcionales al vector de productos:** 23 752 ventanas. La más cercana es UR203, posición 23255, vector `[3, 36, 3, 4, 7, 30, 8, 2, 3]`, escala 1,36, error relativo L2 = 0,164. El nulo (barajar valores dentro de cada quipu) da un error medio de 0,146 y un mínimo de 0,057; **p = 0,755**. Es decir, la ventana más parecida no es más parecida que lo que produce el azar. Otras ventanas cercanas: UR1088 `[2,10,2,1,2,10,3,1,2]` (error 0,198), JC001 `[10,80,18,10,20,50,40,4,5]` (0,202), UR004 `[1,123,22,20,23,101,29,2,2]` (0,212). Ninguna es significativa.
6. **La búsqueda de los ×9 es redundante:** como el error es invariante a escala (se busca la mejor escala), el vector de productos y el de totales ×9 dan exactamente el mismo error y el mismo p. No son dos pruebas independientes.

### 6.3 Resultado

**No hay en el KFG ningún quipu con la forma de la tasa de Guancayo.** No hay 9 grupos de 9 constantes, ni el vector de productos, ni los totales ×9, ni una matriz 9×9 de gemelos. Lo único que existe es la convención local de un grupo de 9 cuerdas iguales (2, 10, 70), que no es la tabla de 9 productos × 9 pachacas.

Nivel: **bien apoyado** que no hay coincidencia exacta en el corpus actual; **apoyado con datos** que la ventana más cercana no es significativa (p = 0,755); **especulativo** que un quipu de este tipo exista en colecciones no incluidas en el KFG.

---

## 7. La estructura 2+1+2+2+2: el hallazgo más sugerente

La Visita describe los curacas en este orden: Mongoy (2 pachacas), Cancay (1), Chuquitanga (2), Chumbillán (2), Antachumbi (2). Si las 9 columnas de UR278 estuvieran en ese orden, el emparejamiento predicho sería:

`(1-2)(4-5)(6-7)(8-9) + c3`

Es exactamente un patrón de 4 pares + 1 suelto, el mismo que el mejor emparejamiento de UR278, pero con pares **contiguos** y en el orden de la Visita. Lo probé de dos maneras:

| estadístico | observado | nulo / referencia | p |
|---|---:|---|---:|
| r intra-par (log-razón, sin efecto de fila) | 0,090 | media de 945 emparejamientos ≈ −0,10 | 0,088 (rank 83/945) |
| igualdades exactas en los 4 pares | **11** | 4,00 esperadas dentro de fila | **0,0003** |
| igualdades, rank sobre 945 emparejamientos | 11 | media 4,0; máximo 11 | **0,0011** |
| igualdades sin las 5 filas más planas | 7 | — | 0,0063 (rank 6/945) |
| máximo sobre 945 emparejamientos, nulo dentro de fila | 11 | media del máximo 9,1 | 0,086 |

La correlación no apoya el emparejamiento (r = 0,090, p = 0,088; con 26 filas r = 0,007, p = 0,236). Pero las **igualdades exactas** sí: los pares de la Visita acumulan 11 igualdades, el máximo de los 945 emparejamientos posibles, y muy por encima de las 4 esperadas si las columnas se barajaran dentro de cada fila (p = 0,0003). El resultado es robusto a dejar fuera las 5 filas más planas (7 igualdades, rank 6/945, p = 0,0063). Los pares aportan 5, 3, 2 y 1 igualdades, en el mismo orden de bloques de la Visita.

Pero hay que ser escéptico:

- El máximo sobre 945 emparejamientos tiene p = 0,086: si uno busca el mejor emparejamiento sin hipótesis previa, 11 igualdades no es raro (la media del máximo es 9,1). El resultado solo es significativo porque el emparejamiento estaba **pre-especificado** por la Visita.
- Las igualdades están concentradas en las filas planas: g0 aporta 5 de las 11 (pares 1-2 y 4-5), g9 aporta otras, etc. Sin las filas planas quedan 7, todavía significativas, pero el efecto es fundamentalmente “las filas planas tienen valores repetidos, y los pares de la Visita capturan esas repeticiones”.
- La correlación, que sería la prueba de que las columnas covarían como parejas, no da nada. Es un emparejamiento de **igualdades**, no de **covariación**.

**Interpretación propuesta:** las 9 columnas de UR278 podrían ser 9 pachacas agrupadas en 5 curacas (4 pares + 1 suelta), y las pachacas de un mismo curaca llevarían el mismo valor en algunos registros (tasa por curaca, no por pachaca). Eso explicaría por qué los pares contiguos de la Visita tienen más igualdades que otros pares, pero no por qué las columnas no covarían. Nivel: **apoyado con datos, frágil**; no bien apoyado.

---

## 8. Controles, resultados negativos y explicaciones aburridas

### 8.1 Controles que hice

- **Unidad de análisis:** las pruebas de UR278 son por fila (24 filas), no por cuerda; las del corpus son por grupo de 9 dentro de cada quipu, con nulo que conserva el quipu. No hay pseudorreplicación a nivel de cuerda suelta.
- **Nulo explícito:** tres nulos para UR278 (filas, columnas, paramétrico), uno para el corpus (barajar dentro del quipu), uno para el emparejamiento (barajar dentro de fila) y uno para las ventanas (barajar dentro del quipu).
- **Semilla fija:** 20261018; 20 000 réplicas en las pruebas de UR278/UR270; 10 000 en el corpus; 2 000 en las ventanas; 50 000 en las permutaciones de perfiles.
- **Corrección múltiple:** Holm por fila (24), Holm por prueba sobre 96 quipus (6 pruebas), Holm sobre las 5 pruebas globales del corpus, Holm por matriz y prueba en UR270 (6 pruebas × 3 matrices). Cuando un resultado no sobrevive, lo digo.
- **Tamaño:** controlé el efecto de `log(total)` sobre el CV; la fase 1 deja de ser significativa después del control (p = 0,757).
- **Selección:** la prueba del emparejamiento 2+1+2+2+2 está pre-especificada por la Visita; aun así, reporto el p del máximo sobre 945 (0,086), que es el precio de buscar el mejor emparejamiento.
- **Post hoc:** las correlaciones de los productos (r = 0,712) y de la supervivencia (r = 0,713) son exploratorias; no las uso como evidencia principal.

### 8.2 Resultados negativos

- **No hay datos que varíen por pachaca** salvo la extinción (2 vivas / 7 extintas). La tasa es idéntica en las 9; las chacras son comunales; las mitas se reparten por pueblo.
- **El perfil de UR278 no es plano** (CV 0,176; max/min 1,75), mientras que la tasa por pachaca predice CV 0. No coinciden.
- **El perfil de productos es demasiado sesgado** (max/min 26) para ser el perfil de columnas de UR278 (1,75). La correlación en el orden documentado es post hoc.
- **El perfil de supervivencia tiene 7 ceros**; UR278 no tiene ninguno. La correlación con c1-c2 es el máximo posible sobre las colocaciones, no un contraste.
- **No hay mezcla de tasa y entrega en UR278:** el BIC favorece una componente; la “clase plana” no es limpia; la fase 1 se explica por el tamaño.
- **No hay filas planas en UR270:** CV mínimo 0,235; ninguna ≤ 0,15; el nulo no muestra exceso.
- **No hay 9 grupos de 9 constantes en ningún quipu del corpus.**
- **No hay coincidencia exacta con el vector de productos ni con los totales ×9** (0/237 grupos; 0/23 752 ventanas).
- **La ventana más cercana no es significativa** (error 0,164 vs nulo 0,146; p = 0,755).
- **“Runcu” no aparece en la Visita:** el documento dice cesto/cestillo; runcu es una glosa posterior.
- **La atribución wanka de Espinoza es falsa:** el documento es del Chillón (7 leguas a Lima, río Collique, Talavera, Cáceres).

### 8.3 La explicación aburrida que gana en varios frentes

- **Filas planas de UR278:** la mayor parte se explica por el perfil de columnas y el tamaño de fila (N3 reduce el efecto de 0,43 a 0,29). Quedan 2-3 filas de cola, que pueden ser registros de un solo ítem repetido, no una tasa.
- **Grupos de 9 iguales del corpus:** son 9 cuerdas que cuentan 9 veces el mismo ítem (2, 10, 70). No hace falta una tabla de tasa.
- **Emparejamiento 2+1+2+2+2:** las igualdades se concentran en las filas planas; el emparejamiento captura esas repeticiones, no una covariación económica.
- **Fase 1:** las filas son más grandes; el CV baja con el tamaño. No es un cambio de régimen.

---

## 9. Niveles de evidencia

| afirmación | nivel |
|---|---|
| La Visita es del valle del Chillón, no de Huancayo | **bien apoyado** (7 leguas a Lima, río Collique, Talavera, Cáceres; Rostworowski) |
| Guancayo tenía 900 tributarios en 9 pachacas de 100 en tiempo del Inca | **bien apoyado** por la Visita y el artículo (con la tensión “cinco” vs 9) |
| La tasa anual era la misma lista en cada pachaca | **bien apoyado** por el texto (“eran nueve cada una de las cosas siguientes”; “tanto al uno como al otro”) |
| Maca tenía 190 tributarios en 1571 (90 + 100), no 170 | **bien apoyado** por la Visita; el artículo se contradice |
| Guarauni tenía 5 chacras, una de maíz, no 4 sin maíz | **bien apoyado** por la Visita; el artículo se contradice |
| La mita de Lima era de 8 indios, pero el reparto suma 7 | **bien apoyado** que el texto se contradice; no se sabe cuál es el error |
| El “9 productos” es una selección editorial; la Visita lista 12 rubros | **bien apoyado** por comparación de líneas |
| UR278 tiene 2-3 filas excepcionalmente planas (Holm) | **apoyado con datos** (g0, g1, g11; g14 borderline) |
| UR278 es una mezcla de filas de tasa y de entrega | **no apoyado**; a lo sumo **propuesto** para 2-3 filas |
| La concentración de filas planas en la fase 1 es un régimen de tasa | **no apoyado**: se explica por el tamaño (p = 0,757 tras control) |
| El emparejamiento 2+1+2+2+2 de la Visita coincide con los pares de UR278 | **apoyado con datos, frágil** (11 igualdades vs 4, p = 0,0003; pero r = 0,090 y máximo sobre 945 p = 0,086) |
| UR270 no replica las filas planas; P es más “redondo” que S1 | **apoyado con datos** (P 22 igualdades vs S1 3; CV no significativo) |
| P = cuota y S1 = entrega en UR270 | **propuesto**; n = 6, no bien apoyado |
| En el corpus hay 5 grupos de 9 con 9 valores iguales (vs 1,2 esperados) | **bien apoyado** (p = 0,0001), pero son constantes simples (2, 10, 70) |
| Hay un quipu en el corpus con la forma de la tasa de Guancayo | **no apoyado / negativo**: 0 coincidencias; la ventana más cercana p = 0,755 |
| Las 9 columnas de UR278 son las 9 pachacas de Guancayo | **especulativo**: el documento es de otro valle y el perfil no coincide; solo la estructura 4+1 es sugerente |
| UR278 es el quipu de la tasa de Guancayo | **especulativo y poco probable**: distinto valle, distinta escala, sin coincidencia de valores |

---

## 10. Para el coordinador

- **La fuente está mal atribuida en la literatura.** La Visita de Martínez Rengifo de 1571 no es de Huancayo, sino del valle del Chillón: el texto dice “siete leguas” a Los Reyes (`:3216`), habla del “río de Collique” (`:3385`) y de las haciendas de Talavera y Cáceres (`:3481`). Rostworowski tiene razón: son yungas del Chillón, no wankas. La “guaranga de Huancayo” de 900 tributarios y 9 pachacas es un señorío yunga, no una guaranga wanka. Esto invalida el uso de este caso como ejemplo wanka.
- **Las cifras centrales son sólidas:** 900 tributarios, 9 pachacas, 100 por pachaca; 5 curacas con 2+1+2+2+2 pachacas; cada pachaca daba la misma lista de productos; 9 chacras comunales en Guancayo; Guarauni 200 en 2 pachacas; Maca 190 en 1571 (90 + 100). El `visita1571.csv` tiene 119 filas con línea.
- **El artículo de Espinoza tiene errores que hay que corregir:** Maca 170 (debe ser 190), Guarauni 4 chacras sin maíz (son 5, una de maíz), mita de 8 que suma 7, y sobre todo el “9 productos” (la Visita lista 12 rubros; el 9 es una selección editorial). No usar el “9” como si fuera una plantilla nativa.
- **UR278 no es una mezcla limpia de tasa y entrega.** Hay 2-3 filas genuinamente planas (g0, g1, g11; Holm < 0,05), pero el BIC favorece una sola componente, la “clase plana” no es estable y la concentración en la fase 1 se explica porque las filas de esa fase son más grandes (p = 0,757 tras controlar el tamaño). La hipótesis de mezcla queda **propuesta**, no apoyada.
- **El hallazgo más sugerente es la estructura 2+1+2+2+2.** El orden de curacas de la Visita (Mongoy 2, Cancay 1, Chuquitanga 2, Chumbillán 2, Antachumbi 2) predice los pares (1-2)(4-5)(6-7)(8-9)+c3. Esos pares acumulan 11 igualdades exactas, el máximo de los 945 emparejamientos y muy por encima de las 4 esperadas (p = 0,0003; sin las filas planas, 7 y p = 0,006). Pero la correlación es nula (r = 0,090; p = 0,088) y el máximo sobre 945 emparejamientos da p = 0,086: es un emparejamiento de igualdades, no de covariación. Nivel: **apoyado con datos, frágil**.
- **UR270 no replica las filas planas** (CV mínimo 0,235; ninguna ≤ 0,15), pero su colgante P tiene 22 igualdades exactas, 16 en el grupo 6 con valores 100/200, mientras que S1 es irregular. Esto sugiere que **P podría ser la cuota y S1 la entrega**, y que UR278, al sumar P+S1, mezcla las dos. Es la pista más prometedora para la siguiente ronda; hoy es **propuesta**, con n = 6.
- **En el corpus hay 5 grupos de 9 con 9 valores iguales** (AS018 70×9; AS207A 10×9; MM019 2×9 ×3), frente a 1,2 esperados (p = 0,0001). La convención existe, pero es rara (2,9 % de los 237 grupos) y son constantes simples, no una tabla de 9 productos.
- **No hay ningún quipu con la forma de la tasa de Guancayo.** Busqué el multiset de 9 productos, los totales ×9, los 9 grupos de 9 constantes y las 23 752 ventanas de 9; no hay coincidencia exacta y la ventana más cercana (UR203, error 0,164) no es mejor que el azar (nulo 0,146; p = 0,755). El corpus actual no contiene ese quipu.
- **Recomendaciones para la siguiente ronda:** (1) re-editar la Visita desde el manuscrito/AGI Justicia 413 para resolver “cinco” vs 9, 170 vs 190 y 8 vs 7; (2) probar P vs S1 como cuota vs entrega en UR270/UR278, con más grupos; (3) buscar una matriz 9×9 de gemelos en colecciones fuera del KFG; (4) no usar el “9 productos” de Espinoza como plantilla nativa; (5) tratar la atribución Chillón/yunga como un hecho, no como una hipótesis.
