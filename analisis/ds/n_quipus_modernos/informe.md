# Quipus modernos y coloniales tardíos con clave conocida: ¿piedra de Rosetta de las convenciones no numéricas?

**Equipo:** `n_quipus_modernos` · **Fecha:** 18 de octubre de 2026 · **Semilla:** 20261018
**Datos:** KFG `analisis/datos/cuerdas.csv` (57 809 cuerdas, 651 quipus), `quipus.csv`, `grupos.csv`; OKR `data/external/open-khipu-repository/data/khipu.db` (619 quipus, solo lectura). Corpus documental/etnográfico externo (véase §2.2).
**Scripts (en esta carpeta, en orden):** `01_merged.py`, `02_claves.py`, `03_test_torsion.py`, `04_test_direccion.py`, `05_test_subsidiarias.py`, `06_test_color.py`, `07_test_canutos.py`, `08_consolidar.py`, `09_subconjuntos.py`, `11_okr_control.py`, `12_convenciones.py`.
**Salidas:** `claves.csv` (34 claves), `cuerdas_con_clave.csv` (11 cuerdas), `convenciones.csv` (12 convenciones), `resultados_globales.csv` (26 pruebas), `res_*.csv`, `cuerdas_merged.csv`.

---

## 1. Pregunta

Los quipus se siguieron usando hasta el siglo XX en pastoreo, comunidades, cofradías y ritos. En varios casos el usuario o el etnógrafo explicó qué significaba cada cuerda. ¿Qué convenciones **no numéricas** (color, torsión, unión, posición, subsidiaria, nudo, objeto atado, fibra, borla) están documentadas con clave conocida? ¿Cuáles se repiten entre fuentes independientes? ¿Se pueden **probar en el corpus antiguo** (KFG/OKR) con un nulo explícito? ¿Qué es continuidad inca y qué es innovación colonial? ¿Qué plantilla dejan para los quipus no numéricos?

---

## 2. Método

### 2.1 Lo que hay —y lo que no hay— en nuestras bases

- KFG: **651 quipus, 57 809 cuerdas**. OKR: **619 quipus**. Ninguno es un quipu moderno de pastor: OKR solo fecha 20 quipus en 1600 y uno en 1630; **502/619 no tienen fecha** y **ninguno está fechado después de 1630**. KFG no tiene campo de fecha y su corpus es arqueológico/colonial temprano. Las bases, por tanto, no contienen el corpus moderno.
- El corpus moderno hay que reconstruirlo desde la literatura. Inventario aproximado: **43 khipus de pastoreo/cosecha** en la encuesta de Mackey (24 estudiados por ella; 19 hombres y 1 mujer entrevistados), 1 Cutusuma, 3 Laramarca, 3 Anchucaya (121 colgantes), ~20 quipocamayos de Tupicocha (2 por ayllu), 263 objetos de Rapaz, 2 Collata (487 colgantes), 1 tablero de Mangas (87 cuerdas), 4 réplicas de Pimentel. Son ~340 objetos, pero **solo Cutusuma publica una tabla completa cuerda-por-cuerda con valores y significado**; Laramarca publica la estructura (4 cuerdas) sin valores.
- Consecuencia: la “piedra de Rosetta” moderna es **más estrecha de lo que sugiere la bibliografía**. `cuerdas_con_clave.csv` tiene 11 filas: 7 de Cutusuma y 4 de Laramarca. No hay ninguna tabla comparable para Tupicocha, Rapaz, Anchucaya ni Collata en las fuentes abiertas consultadas.

### 2.2 Corpus documental (fuentes con clave)

| Fuente | Lugar | Siglo | Uso | Qué explica | ¿Tabla por cuerda? |
|---|---|---|---|---|---|
| Uhle 1897; Hyland 2014 | Cutusuma, Bolivia | XIX | rebaño | ply S/Z = sexo/estado; posición = especie; subsidiaria = corderos; superior = total | **Sí, 7 cuerdas** |
| Soto Flores 1950-51; Hyland 2020 | Laramarca, Perú | XX | rebaño | negro = macho, blanco = hembra; subsidiaria = cría del mismo sexo | Estructura, 4 cuerdas, sin valores |
| Urton 2003 | Andes | XVI | administrativo/teórico | ply y dirección de nudo como bits por marcadez; sin clave semántica | No |
| Mackey 1970, 2002 | Cusco/Puno/La Libertad | XX | rebaño/productos | tipos A/B/C; nudos en parte doble = centenas/millares; inicio por número+color+posición | No (tipología) |
| Núñez del Prado 1950 | Cusco | XX | rebaño/ritual | nudos, grosores y colores; sin glosa verificable | No |
| Holm 1953/1968 | Ecuador | XX | mnemónico | “sapán” de nudos; sin clave de color/cuerda | No |
| Salomon 2004, 2006 | Tupicocha, Huarochirí | XX | cívico/ritual | 2 quipocamayos por ayllu; cordeles = cargos/miembros; marcadores = identidad | No |
| Peters y Salomon 2006; Salomon 2017 | Rapaz, Oyón | XIX-XX | ritual/agrícola | 263 objetos unilineales; objetos atados = signos; nudos menores | No |
| Hyland 2016 | Anchucaya, Huarochirí | XX (1935-1940s) | trabajo comunal | color = ayllu; grupo = tarea; banda = individuo; seriación = agregado; ply Z = mujer/mitad; mitad superior/inferior = hecho/debido; tela blanca = “Papel”; cayte = inicio/tema | Parcial (RT 21287, 71 cuerdas) |
| Hyland 2017 | Collata, Huarochirí | XVIII (1783) | carta/narrativa | 95 símbolos en 487 colgantes; color+fibra+ply = posibles nombres de ayllu | No (solo 3 cordones finales) |
| Hyland, Bennison y Hyland 2021 | Casta/Mangas, Huarochirí | XIX-XX | tablero/padrón | agujero = nombre; color/ply/dirección/grosor = persona, moiety, textura | 87 cuerdas, sin glosa individual |
| Pérez Bocanegra 1631; Harrison 2013; Charles 2013 | Cusco/Andahuaylillas | XVII | confesión | color = división de pecados; nudos = número; se presta y reutiliza | No; clave perdida |
| Platt 2002 | Sacaca, Charcas | XVI (juicio 1581) | tributo | chinu con productos/años; lecturas variables | No |
| Amado Gonzales 2013; Curatola y de la Puente 2013 | Cusco | XVI-XVIII | cofradía/iglesia/hacienda | quipucamayos registraban ganado y bienes de cofradías; sin clave cordel-por-cordel | No |
| Arnold y Yapita 2006 | Qaqachaka, Oruro | XX-XXI | rebaño/k'illpha | colgante = persona; color = dueño/animal; hilo insertado = color del animal; nudo masculino = cantidad de un grupo | No |
| Pimentel 2005 (vía Hyland 2020) | Suroeste de Bolivia | XIX-XX | memoria | colgante atado alrededor de otro = lo anula; grosor/largo/color = signos | 4 réplicas |

### 2.3 Cómo se construyeron las claves

`claves.csv` tiene una fila por fuente × rasgo × significado, con evidencia (testimonio directo, etnografía, documento, análisis de objeto), número de cuerdas con datos publicados y cita de página. `cuerdas_con_clave.csv` transcribe **solo** lo publicado: los 7 cordones de Cutusuma (valores 387, 285, 121, 99, 85, 60, 170; ply S/Z; posición; significado) y las 4 cuerdas de Laramarca (sin valores). No se rellenaron celdas ausentes.

### 2.4 Pruebas en el corpus antiguo

Unidad de inferencia: **el quipu**. Cada prueba compara un estadístico observado con un nulo que **permuta la etiqueta dentro de cada quipu** (torsión, dirección, canuto, color o valores de madre), preservando composición, tamaños y valores. 1 000 réplicas por prueba; p empírico `(1+#extremos)/(1+B)`; semilla 20261018. Se aplicó **Holm global a las 26 pruebas primarias** (y Holm por familia como control). Los detalles están en cada script; los resultados consolidados en `resultados_globales.csv`.

Pruebas:
- **Torsión:** T1 transiciones S/Z (bloques contiguos); T2 grupos partidos en mitades S|Z; T3 valor Z vs S; T4 MI(torsión; color); T5 MI(torsión; grupo).
- **Dirección del nudo:** D1 pureza por cuerda; D2/D2b/D2c valor Z vs S (global, dentro de grupo, dentro de número de nudos); D3/D3b MI(dirección; color) global y condicional al grupo; D4 MI(dirección; torsión); D5 MI(dirección; grupo).
- **Subsidiarias:** S1 fracción hijo<madre; S2 mediana log(hijo/madre); S3 hijo=madre/k; S4 madre=suma(hijos); S5 rho(valor madre, n hijos).
- **Color:** C1 Jaccard de bigramas entre quipus de la misma procedencia; C2 concordancia de orden entre pares de colores; C3c trigramas de bandas repetidos (seriación).
- **Objetos atados:** K1 valor; K2 sin nudos; K3 borde de grupo; K4 MI(canuto; color); K5 MI(canuto; fibra).

---

## 3. Resultados

### 3.1 El inventario de convenciones

`convenciones.csv` resume 12 convenciones. Las cinco que pedía el encargo se evalúan así:

| Convención | ¿Recurrente entre fuentes independientes? | Prueba en el corpus antiguo | Veredicto |
|---|---|---|---|
| **Color = clase de animal, bien, ayllu o persona** | **Sí, 7 fuentes** (Cutusuma, Laramarca, Qaqachaka, Anchucaya, Collata, confesión, Tupicocha) | C1 0,411 vs 0,414 (NS); C2 0,755 vs 0,745 (NS); C3c 4 438 vs 3 223 (p=0,001) | Documentado en etnografía; **no hay un léxico de color compartido** entre quipus antiguos. La repetición es local (bandas/seriación), no un código común. |
| **Subsidiaria = cría o subcategoría** | **Sí, 4 fuentes** (Cutusuma, Laramarca, Mackey, contabilidad inca) | S1 61,95% vs 60,27% (+1,7 pp); S2 NS; S3 1,48% vs 1,35% (+0,13 pp); S4 12,62% vs 9,63%; S5 rho 0,071 | **Solo la jerarquía aditiva débil** (12,6%) tiene apoyo. **No hay cría proporcional**: la mediana de hijo/madre no difiere del azar. |
| **Torsión = mitad / categoría** | **Parcial, 4 fuentes** (Cutusuma, Anchucaya, Mangas, Urton 2003) | T1 125 vs 231,8 transiciones (z=-13,5); T4/T5 z=19,3/18,1; **T2 1 vs 1,59 (p=0,82)**; **T3 +0,149 (p=0,93 en la dirección “Z menor”)** | **Apoyado como marcador de sección/bloque**, no como mitad ni como “Z = menos valorado”. |
| **Objeto atado = pérdida o muerte** | **No hay ninguna fuente que lo diga** | Canutos: 904 cuerdas en 26 quipus; casi todos los quipus son “todo canuto”; K1 NS, K2 NS, K3 p=0,087 | **Hipótesis sin fuente y sin apoyo.** Las fuentes documentan identidad/firma/tarea/anulación, no muerte. |
| **Cuerda superior = total** | **Sí, 4 fuentes** (Cutusuma, Laramarca, Mackey, contabilidad inca) | KFG: 376 cuerdas superiores en 47 quipus; 86 son sumas (22,9%); 29/47 quipus (62%) tienen al menos una; `union=T` 0/17 sumas; S4 12,6% | **Apoyado como convención minoritaria**, no universal. |

### 3.2 Torsión: bloques contiguos, no mitades

En los 13 quipus con ≥5 colgantes y ≥2 S y ≥2 Z:

- **T1:** 125 transiciones S/Z observadas frente a **231,8** esperadas por azar (z = **-13,5**; p = 0,001). Ocho de 13 quipus tienen p<0,05. Excluyendo la clase tally de `n_no_numericos`: 29 vs 58 transiciones (z = -10,0; p = 0,001), así que **no es un artefacto de los quipus tally**.
- **Caveat decisivo:** **99,4% de los grupos con ≥2 cuerdas tienen una sola torsión** (4 547 grupos). La torsión es, en la práctica, un **atributo de grupo** en KFG. T1 confirma esa arquitectura, no una partición independiente. Lo sustantivo es que los grupos Z son una minoría (202 de 1 674 cuerdas) y que **no son mitades**.
- **T4/T5:** MI(torsión; color) = 1,442 vs 0,199 (z = 19,3); MI(torsión; grupo) = 3,429 vs 1,412 (z = 18,1). La torsión se concentra en **grupos y colores específicos**.
- **T2 (mitades):** solo **1** grupo partido limpiamente en S|Z, frente a 1,59 esperados (p = 0,82). **No hay partición en mitades.**
- **T3 (valor):** los colgantes Z tienen un valor **ligeramente mayor**, no menor (+0,149 en log; p = 0,93 para la predicción “Z menor”). Sin la clase tally, la diferencia es +0,438 (Z > S). **La torsión no marca “menos valor” ni “mitad”.**

Ejemplos legibles:
- **UR1123:** 70 colgantes, 10 Z, **todos en el grupo 5 y todos blancos** (posiciones 54-72, cada 2). Es un bloque de sección, no una mitad.
- **HP045:** 48 colgantes, 6 Z; **5 en el grupo 8**, todos marrones.
- **UR087:** 306 colgantes, 4 Z; 3 en el grupo 0 y 1 suelto en el 54.
- **UR1057:** 559 colgantes, 2 Z, ambos en el grupo 79.

**Lectura:** la torsión es un **marcador de sección/categoría** (un bloque, a veces monócromo, dentro de un grupo). No es una partición binaria de mitades ni un código de valor. Esto es coherente con Cutusuma (S/Z separa sexo/estado) pero **no** con la generalización “torsión = mitad” de Anchucaya.

### 3.3 Dirección del nudo: propiedad de la cuerda y marcador de sección

En 198 quipus con ≥8 colgantes con dirección y ≥2 de cada una (14 236 colgantes; 6 244 cuerdas multi-nudo):

- **D1 pureza:** **96,5%** de las cuerdas multi-nudo son S o Z puras, frente a **61,9%** bajo el nulo intra-quipu (z = **28,5**; p = 0,001). Control independiente en OKR (16 344 cuerdas multi-nudo, 473 quipus): **80,0% vs 75,7%** (z = **23,6**; p = 0,001). El efecto es real, pero **KFG infla la pureza** (probablemente transcribe una dirección por cuerda); el número conservador es 80%.
- **D5:** MI(dirección; grupo) = 48,31 vs 34,66 (z = **14,5**). La dirección se concentra por grupos.
- **D2:** las cuerdas con dirección Z valen **más** que las S: diferencia de log(valor) = **+0,395** (z = **15,4**; ≈1,48×). Sobrevive dentro de grupo (+0,399; z = 15,9) y dentro de estratos de número de nudos (+0,318; z = 17,3). **No es un artefacto de que las Z estén en grupos con valores altos ni de que tengan más nudos.**
- **D3/D3b:** MI(dirección; color) = 9,44 vs 5,62 (z = 6,8), pero **al controlar por grupo desaparece** (13,71 vs 14,66; z = **-1,5**; p = 0,94). La asociación con color es un subproducto del banding por grupo.
- **D4:** MI(dirección; torsión) = 0,191 vs 0,178 (z = 0,26; NS). **Dirección y torsión son ejes independientes.**
- **Estructura de grupos:** en 29 quipus con ≥3 grupos de dirección pura, la secuencia de grupos tiene 1,97 transiciones para 9,07 grupos (35,5% de alternancia). **No alternan como moieties**: son 1-2 bloques grandes (p. ej. UR087: 33 grupos, 2 transiciones; QU011: 13 grupos, 1 transición).

**Lectura:** la dirección del nudo es una **propiedad de la cuerda** y marca **secciones/grupos**, no una alternancia de mitades. El signo del valor es el contrario al predicho por “Z = marcado = menos valorado”: en este corpus **Z vale más**. Esto puede significar que Z es la categoría principal (es la dirección mayoritaria: 33 908 Z vs 22 015 S en los racimos) y S la subcategoría, o que la dirección codifica otra dimensión (p. ej. tipo de bien). No se puede decidir sin glosas.

### 3.4 Subsidiarias: no son crías proporcionales

En 435 quipus, 9 425 madres y **16 098 pares** madre-hijo:

- **S1:** 61,95% de los hijos valen menos que la madre, frente a 60,27% del nulo (**+1,7 pp**; z = 5,4; p = 0,001). El efecto es estadísticamente significativo pero **diminuto**: los hijos son pequeños porque casi todas las cuerdas son pequeñas.
- **S2:** mediana de log(hijo/madre) = **-1,946** vs **-1,988** del nulo (p = 0,998). **No hay diferencia**: la proporción hijo/madre no es más pequeña de lo que predice el azar.
- **S3:** solo **1,48%** de los pares son exactamente madre/k (k=2..10), frente a 1,35% del nulo (**+0,13 pp**). No hay un sistema de fracciones simples.
- **S4:** **12,62%** de las madres valen exactamente la suma de sus hijos, frente a 9,63% del nulo (**+3,0 pp**; z = 13,5). La jerarquía aditiva existe, pero es **minoritaria**.
- **S5:** rho(valor madre, número de hijos) = **0,071** vs 0,001 (z = 4,0). Los registros más grandes tienen apenas más subcategorías.

**Subconjuntos:**
- **Fibra de camélido** (11 quipus, 8 de ellos tally): S1 26,2% vs 32,8% (dirección **contraria**), S3 0,58% vs 0,86% (contraria), S4 9,3% vs 6,1% (p = 0,034). Ni siquiera en los quipus de fibra animal aparece el patrón de cría.
- **Clase tally** (56 quipus limpios): S1 sin efecto (44,9% vs 44,8%), S4 16,3% vs 11,8% (z = 5,5). La jerarquía aditiva es algo más fuerte, pero sigue siendo una minoría.

**Lectura:** la subsidiaria **no** es una cría proporcional en el corpus antiguo. Es, como mucho, una **parte que a veces suma al total**. La convención moderna de Cutusuma/Laramarca (subsidiaria = cordero) **no se generaliza** a los quipus incas/coloniales.

### 3.5 Color: fórmula local, no léxico compartido

En 275 quipus de 15 procedencias con ≥5 quipus y ≥8 colgantes coloreados:

- **C1:** Jaccard de bigramas de color entre quipus de la misma procedencia = **0,411** vs **0,414** del nulo (z = -0,65; p = 0,74). **No hay más similitud de orden dentro de una procedencia que entre procedencias.**
- **C2:** concordancia de orden entre pares de colores = **0,755** vs **0,745** (z = 0,42; p = 0,34). **No hay un orden fijo compartido.**
- **C3c:** dentro de cada quipu, los trigramas de bandas repetidos son **4 438** vs **3 223** del nulo (z = 73,4; p = 0,001). Hay **repetición local** (seriación/banding), y sobrevive al restringir a quipus con ≥4 colores (4 017 vs 2 932; z = 63,5). Pero los ejemplos están dominados por alternancias de dos colores (A-B-A-B), no por ciclos de 6 colores.
- **Por procedencia:** solo **Incahuasi** (C1, z = 4,1; p = 0,001) sobrevive Holm dentro de las 30 pruebas por procedencia; Huacho (p = 0,002) no. Con 15 procedencias y 2 pruebas cada una, un positivo aislado es compatible con ruido o con un uso local.

**Lectura:** el color es **formulaico dentro de cada quipu** (bandas, seriación), pero **no forma un léxico estable compartido** entre quipus de la misma procedencia. Esto no refuta que el color signifique algo en cada quipu; refuta que el mismo código de color se reutilice entre quipus, que es lo que necesitaría una “piedra de Rosetta” panandina.

### 3.6 Objetos atados: canutos como género, no como pérdida

- **904 cuerdas con canuto en 26 quipus.** La distribución es enormemente desigual: UR050 163/164, UR052 94/96, UR054 93/115, UR055 179/180, UR039 90/91, UR110 88/89, UR112 75/76. Son quipus **casi enteros con canutos**, no quipus con objetos ocasionales.
- Solo **4 quipus** permiten un contraste interno canuto vs no canuto (UR054 aporta 93 de los 103 canutos contrastados).
- **K1** (valor): -0,018 (NS). **K2** (sin nudos): 1,9% vs 2,4% (NS). **K3** (borde de grupo): 75,0% vs 57,2% (p = 0,087). **K4** (color): MI 0,434 vs 0,094 (p = 0,010), pero lo arrastra UR054. **K5** (fibra): 0,082 vs 0,041 (p = 0,036), débil.

**Lectura:** el canuto es un **marcador de género/registro** (un quipu entero con canutos), no un signo por cuerda de “pérdida” o “muerte”. La hipótesis “objeto atado = pérdida o muerte” **no tiene fuente etnográfica** y **no tiene apoyo en el corpus**. Las fuentes documentan más bien identidad/firma (pelo, Collata), tarea (tela blanca, Anchucaya), anulación (Pimentel) o género (Rapaz).

### 3.7 Cuerda superior = total: real pero minoritaria

- KFG anota **376 cuerdas superiores en 47 quipus**; **86 son “sum top cords”** (22,9%) y **29/47 quipus (61,7%)** tienen al menos una. El propio KFG describe 21 “double sum” adicionales.
- Las **17 cuerdas con `union=T` y hijos** en KFG **no son sumas** (0/17). `union=T` no es un marcador de cuerda-summit; es un tipo de fijación. Esto es una advertencia metodológica: no usar `union=T` como “cuerda superior”.
- **S4** (madre = suma de hijos) = 12,6% vs 9,6%. La misma lógica, un nivel más abajo, es también minoritaria.

**Lectura:** la cuerda superior es un total **en una minoría sustancial de casos** (23% de las cuerdas, 62% de los quipus con cuerdas superiores), no una regla universal. Es una convención real, pero no la base de una gramática general.

---

## 4. Controles y amenazas

1. **Nulo explícito y p empírico:** cada prueba tiene un nulo que preserva lo que podría explicar el efecto por sí solo (composición de torsion/dirección, tamaño de grupo, número de nudos, distribución de valores de madre, paleta de color). 1 000 réplicas; p mínimo 0,001.
2. **Corrección múltiple:** **26 pruebas primarias**, Holm global. **14/26 sobreviven** (q=0,026). Pero varias son efectos diminutos: S1 (+1,7 pp) y S3 (+0,13 pp) son significativas por n grande, no por tamaño. Las pruebas con efecto sustantivo son T1, T4, T5, D1, D2, D2b, D2c, D5 y S4; C3c es real pero local. La tabla siguiente resume las pruebas clave (la tabla completa, con las 26, está en `resultados_globales.csv`).

| Prueba | Observado | Nulo | z | p | q global | Lectura |
|---|---:|---:|---:|---:|---:|---|
| T1 transiciones S/Z | 125 | 231,8 | -13,5 | 0,001 | 0,026 | torsión en bloques |
| T2 mitades S\|Z | 1 | 1,59 | -0,5 | 0,823 | 1,000 | **no hay mitades** |
| T3 valor Z-S | +0,149 | 0,0006 | 1,5 | 0,929 | 1,000 | **Z no vale menos** |
| T4 MI(torsión;color) | 1,442 | 0,199 | 19,3 | 0,001 | 0,026 | torsión↔color |
| T5 MI(torsión;grupo) | 3,429 | 1,412 | 18,1 | 0,001 | 0,026 | torsión↔grupo |
| D1 pureza dirección | 0,965 | 0,619 | 28,5 | 0,001 | 0,026 | dirección por cuerda |
| D2 valor Z-S | +0,395 | 0,001 | 15,4 | 0,001 | 0,026 | **Z vale más** |
| D2b valor Z-S \| grupo | +0,399 | 0,001 | 15,9 | 0,001 | 0,026 | no es confusión de grupo |
| D2c valor Z-S \| nudos | +0,318 | 0,001 | 17,3 | 0,001 | 0,026 | no es confusión de tipo |
| D3b MI(dirección;color\|grupo) | 13,71 | 14,66 | -1,5 | 0,940 | 1,000 | color explicado por grupo |
| D4 MI(dirección;torsión) | 0,191 | 0,178 | 0,3 | 0,282 | 1,000 | ejes independientes |
| S2 log(hijo/madre) | -1,946 | -1,988 | 1,2 | 0,998 | 1,000 | **no hay cría proporcional** |
| S4 madre=suma(hijos) | 0,126 | 0,096 | 13,5 | 0,001 | 0,026 | jerarquía aditiva débil |
| C1 Jaccard color | 0,411 | 0,414 | -0,6 | 0,741 | 1,000 | **no hay léxico compartido** |
| C2 orden de colores | 0,755 | 0,745 | 0,4 | 0,344 | 1,000 | **no hay orden fijo** |
| C3c trigramas de bandas | 4 438 | 3 223 | 73,4 | 0,001 | 0,026 | seriación local |
| K1 valor con canuto | -0,018 | -0,002 | -0,3 | 0,396 | 1,000 | canuto no = pérdida |
| K4 MI(canuto;color) | 0,434 | 0,094 | 5,6 | 0,010 | 0,120 | solo UR054 |
3. **Transcripción KFG vs OKR:** la concordancia de torsión es 96,7% en 52 473 cuerdas unidas. La pureza de dirección es 96,5% en KFG pero **80,0% en OKR**: KFG simplifica. Usamos el 80% como cota conservadora; el efecto sigue siendo significativo (z = 23,6).
4. **Confusión con la clase tally:** los 13 quipus de torsión están dominados por la clase tally de `n_no_numericos` (UR050/51/52/54/55, etc.). Al excluirla, T1 sigue (z = -10,0), pero T4/T5 bajan (z = 6,1/8,6). La torsión como sección **no** es solo tally, pero su asociación con color/grupo es más fuerte dentro de la clase.
5. **Confusión con grupo/banding:** la dirección se asocia al color (D3) pero **no** al controlar por grupo (D3b). No interpretar “dirección = color”; es “dirección = sección, y el color también”.
6. **Confusión con tipo de nudo:** la diferencia de valor Z>S sobrevive al control por número de nudos y por grupo (D2b/D2c) y se ve dentro de cuerdas uniformes de nudos simples (mediana S=30 vs Z=50). No es solo que las Z tengan nudos largos.
7. **Canutos:** solo 4 quipus con contraste interno y UR054 aporta el 90%. K4/K5 no son concluyentes; no se puede separar “canuto = color” de “UR054 = caso único”.
8. **Color y procedencia:** usamos la columna `procedencia` de KFG (lugar de hallazgo/origen), **no** la columna `museo`, conforme a la regla del BRIEF. Aun así, 235/651 quipus tienen procedencia “Unknown” y las 15 procedencias con ≥5 quipus son una muestra sesgada. Además, la paleta puede reflejar prácticas de tinte locales, no semántica.
9. **Publicación sesgada:** las fuentes modernas que publican claves son las que tienen un informante excepcional (Cutusuma, Anchucaya). No son una muestra aleatoria de quipus modernos. La ausencia de tablas para Tupicocha/Rapaz/Collata no significa que no existan; significa que no están en abierto.
10. **Circularidad:** las pruebas de torsión/dirección usan las mismas variables que definen las convenciones. El valor predictivo está en el **contraste con el nulo**, no en la mera presencia de bloques (siempre hay banding).
11. **Unidad:** todas las pruebas de asociación se hacen dentro de cada quipu y se agregan; no se mezclan cuerdas de quipus distintos. Las pruebas por procedencia (C1/C2) usan el quipu como unidad y comparan pares.
12. **Unidad de registro:** **99,4% de los grupos con ≥2 cuerdas tienen una sola torsión** y 69,1% una sola dirección. La torsión es un atributo de grupo en KFG, y la dirección lo es en menor medida. Eso infla T1 y la pureza de dirección; el control OKR reduce la pureza a 80% (frente a 96,5% en KFG), pero la torsión sigue siendo un atributo de grupo. Sin imágenes no se puede separar “señal real” de “convención de registro”.

---

## 5. Resultados negativos (explícitos)

1. **No hay un léxico de color compartido:** C1 y C2 no superan el nulo (0,411 vs 0,414; 0,755 vs 0,745). La repetición de bandas es local, no un código común.
2. **La torsión no es una mitad:** T2 1 vs 1,59 (p = 0,82); T3 no muestra que Z valga menos (p = 0,93). La torsión marca bloques/secciones, no mitades ni valores.
3. **La dirección del nudo no es “Z = marcado = menos valorado”:** las Z valen **más** (+0,40 en log; z = 15,4), incluso dentro de grupo y de número de nudos.
4. **La dirección no se asocia con la torsión:** D4 z = 0,26. Son ejes independientes; no forman un único código binario.
5. **La subsidiaria no es una cría proporcional:** S2 no difiere del azar (p = 0,998); S3 +0,13 pp. En fibra de camélido, S1 y S3 van en dirección contraria.
6. **No hay evidencia de “objeto atado = pérdida/muerte”:** ninguna fuente lo dice; los canutos no se asocian a valores bajos ni a cuerdas sin nudos (K1/K2 NS).
7. **La cuerda superior no es siempre un total:** 22,9% de las cuerdas superiores y 61,7% de los quipus con cuerdas superiores; `union=T` 0/17.
8. **No hay un orden fijo de colores entre quipus de la misma procedencia:** solo Incahuasi sobrevive Holm, y podría ser un efecto local.
9. **La clase tally no muestra el patrón de cría:** S1 44,9% vs 44,8%; S4 16,3% vs 11,8%. La jerarquía aditiva es débil incluso ahí.
10. **No se puede probar la confesión:** no sobrevive ningún quipu de confesión con su clave; Pérez Bocanegra no da la lista color→pecado.
11. **No se puede probar la borla/cayte en el corpus antiguo:** KFG/OKR no codifican borlas por cuerda.
12. **La fibra animal como categoría no es testeable con rigor:** OKR distingue CL/CN/W, no especie; el efecto de CL está confundido con colección (n_no_numericos).

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Los quipus modernos usan color, torsión, posición, subsidiaria, objeto y borla con significado documentado | **Bien apoyado** para los casos con informante (Cutusuma, Anchucaya); **apoyado** para el resto |
| Existe una tabla cuerda-por-cuerda publicada y completa | **Bien apoyado** que solo Cutusuma (7 cuerdas); Laramarca solo estructura |
| La torsión forma bloques contiguos y se asocia a grupo/color en el corpus antiguo | **Apoyado con datos** (T1 z=-13,5; T4/T5 z>18; robusto sin tally) |
| La torsión no es una mitad ni un código de “menos valor” | **Apoyado con datos (negativo)** (T2 p=0,82; T3 p=0,93) |
| La dirección del nudo es una propiedad de la cuerda | **Apoyado con datos** (KFG 96,5% vs 61,9%; OKR 80,0% vs 75,7%; z=23,6) |
| La dirección marca secciones/grupos, no moieties alternantes | **Apoyado con datos** (D5 z=14,5; 29 quipus, 1,97 transiciones/9 grupos) |
| Las cuerdas Z valen más que las S | **Apoyado con datos** (D2/D2b/D2c; z>15), pero **sin interpretación semántica** |
| La dirección no se asocia con la torsión | **Apoyado con datos (negativo)** (D4 z=0,26) |
| La subsidiaria no es una cría proporcional | **Apoyado con datos (negativo)** (S2 p=0,998; S3 +0,13 pp) |
| La jerarquía aditiva madre=suma(hijos) existe pero es minoritaria | **Apoyado con datos** (12,6% vs 9,6%; en tally 16,3% vs 11,8%) |
| El color no forma un léxico compartido entre quipus de la misma procedencia | **Apoyado con datos (negativo)** (C1/C2 NS) |
| La seriación/banding local es real | **Apoyado con datos** (C3c z=73; rico en colores z=63) |
| Los canutos son un marcador de género/registro, no de pérdida | **Propuesto** (distribución “todo canuto”; K1/K2 NS; solo 4 quipus de contraste) |
| La cuerda superior es un total minoritario | **Apoyado con datos** (22,9% de cuerdas; 61,7% de quipus) |
| “Objeto atado = pérdida/muerte” | **Especulativo / no apoyado**; ninguna fuente lo documenta |
| “Torsión = mitad” como regla general | **Especulativo / no apoyado** en el corpus antiguo; documentado solo en casos modernos |
| Collata como escritura logosilábica | **Especulativo** (Hyland 2017; 95 símbolos, 3 cordones finales, sin control) |
| La clase no numérica es tally/etiqueta, no narrativa | **Propuesto** (coherente con n_no_numericos y con este informe) |

---

## 7. Continuidades inca vs innovaciones coloniales

**Continuidades plausibles desde el inca:**
- **Nudo decimal** como gramática base (bien apoyado).
- **Color como categoría** (documentado en crónicas y etnografía; el corpus antiguo muestra banding, no un léxico compartido).
- **Jerarquía de cuerdas y subsidiarias** (la madre puede ser suma de hijos, 12,6%; la subsidiaria es una parte, no una cría).
- **Cuerda superior como total** en una minoría de quipus (23-62%).
- **Dirección del nudo como marcador de sección** (fuerte en el corpus; podría ser una continuidad de un uso prehispánico de “lado/mitad”, pero no alterna moieties).
- **Torsión como marcador binario** (presente, pero muy rara: 93% S; Z concentrada en pocos quipus, solo 13 con ≥2 Z y ≥2 S). Podría ser una continuidad de marcadez, pero el signo del valor es contrario al esperado.

**Innovaciones coloniales o post-incas:**
- **Quipus-tablero/padrón** (agujero = nombre; Casta/Mangas, XVI-XX). Es una fusión con la lista alfabética de nombres.
- **Quipus de confesión** (color = categoría de pecado; Cusco, XVII). Es una adaptación catequética, y la clave se perdió.
- **Seriación explícita de colores de ayllus × tareas** (Anchucaya, XX; quizá colonial). La seriación existe en el corpus antiguo, pero no con esta semántica.
- **Logosillabismo de Collata** (XVIII; posible invención colonial o tradición local de fibra animal).
- **Objetos atados como firmas/insignias/género** (Rapaz, Collata, Mangas; XIX-XX).
- **Quipus de pastor unilineales/bifurcados** (Mackey tipos B/C; post-incas).
- **Torsión como género/mitad con valor mitad** (Cutusuma, Anchucaya; XIX-XX). No se encuentra en el corpus antiguo; es la innovación más clara de las que parecían “generales”.

---

## 8. Plantilla para los quipus no numéricos

La clase de `n_no_numericos` (56 quipus limpios, 9,4% del corpus) se caracteriza por repetición unaria, canutos (68% vs 22%) y fibra de camélido (16% vs 1,7%), sin cuerdas superiores. Este informe añade tres piezas:

1. **La torsión y la dirección son marcadores de sección, no valores.** En los quipus no numéricos, esperar que torsión/dirección **corten** el quipu en bloques (grupos, bandas, secciones), no que codifiquen un número. Es una gramática de **partición**, no de magnitud.
2. **El color es local, no un léxico panandino.** En los no numéricos, el color puede distinguir categorías dentro de un quipu (bandas, seriación), pero no se debe esperar el mismo color→categoría en otro quipu. La plantilla correcta es “cada quipu tiene su propio código de color, aprendido localmente”, no “existe un diccionario de colores”.
3. **Los objetos atados marcan género/identidad/tarea, no pérdida.** Los canutos de los no numéricos (68%) son un **marcador de género material**: quipus enteros con canutos, no cuerdas sueltas con un canuto. Eso es consistente con un **registro/etiqueta** (tally, inventario, marcador de género), no con una narrativa de muertes.

**Predicciones falsables para la siguiente ronda:**
- En los 56 no numéricos, los bloques de torsión/dirección deben coincidir con los límites de grupo/banda más de lo esperado por azar (test de intersección de particiones).
- Los canutos deben concentrarse en quipus/grupos, no en cuerdas individuales (ya se ve: 26 quipus, casi todos “todo canuto”).
- Las subsidiarias de los no numéricos deben ser **subcategorías** (mismo color/torsión que la madre), no crías con valor proporcional.
- Si aparece un quipu no numérico con color+fibra+ply muy variables y nudos solo terminales, es candidato a Collata (logosilábico), no a tally.

---

## 9. Para el coordinador

- **La “piedra de Rosetta” moderna existe, pero es minúscula.** De ~340 quipus modernos documentados, solo **Cutusuma** publica una tabla completa cuerda-por-cuerda (7 cuerdas) y **Laramarca** publica la estructura (4 cuerdas, sin valores). `cuerdas_con_clave.csv` tiene 11 filas. Tupicocha, Rapaz, Anchucaya y Collata no publican tablas completas en abierto. Nuestras bases (KFG/OKR) tienen **0 quipus modernos**: OKR no fecha ninguno después de 1630 y 502/619 no tienen fecha; KFG no tiene campo de fecha.
- **La convención “torsión = mitad” no se sostiene en el corpus antiguo.** La torsión forma **bloques contiguos** (125 vs 232 transiciones; z=-13,5) y se asocia a grupo y color (z=19,3/18,1), pero **99,4% de los grupos con ≥2 cuerdas tienen una sola torsión**: es un **marcador de grupo/sección**, no una partición interna. Además **no** parte los grupos en mitades (1 vs 1,59; p=0,82) y **no** hace que las Z valgan menos (+0,149; p=0,93 en la dirección predicha).
- **La dirección del nudo es la señal no numérica más fuerte y más abundante.** 96,5% de las cuerdas multi-nudo son S o Z puras (nulo 61,9%; control OKR 80,0% vs 75,7%, z=23,6). Se concentra por grupos (z=14,5) y las cuerdas Z valen **más** que las S (+0,40 en log; z=15,4; sobrevive dentro de grupo y de número de nudos). **No** se asocia con la torsión (z=0,26) ni con el color al controlar grupo (z=-1,5). Es un eje independiente de **sección/categoría**, no de “marcado = menos”.
- **La subsidiaria no es una cría proporcional.** 16 098 pares: la mediana de hijo/madre no difiere del azar (p=0,998); solo 1,48% son madre/k; la jerarquía aditiva madre=suma(hijos) es 12,6% vs 9,6%. En los 11 quipus de fibra de camélido, S1 y S3 van en dirección **contraria**. La convención de Cutusuma/Laramarca (subsidiaria = cordero) **no se generaliza**.
- **El color no es un léxico compartido.** Entre quipus de la misma procedencia, la similitud de bigramas de color es 0,411 vs 0,414 (NS) y la concordancia de orden 0,755 vs 0,745 (NS). Hay **seriación local** (C3c 4 438 vs 3 223; z=73), pero dominada por alternancias de 2 colores. Solo Incahuasi sobrevive Holm en 30 pruebas por procedencia, y puede ser ruido.
- **“Objeto atado = pérdida/muerte” es una hipótesis sin fuente.** Ninguna de las fuentes lo dice; documentan identidad/firma (pelo, Collata), tarea (tela blanca, Anchucaya), anulación (Pimentel) o género (Rapaz). Los canutos son un **marcador de género/registro**: 904 cuerdas en 26 quipus, casi todos “todo canuto” (UR050 163/164, UR055 179/180); K1/K2 NS y solo 4 quipus permiten contraste interno.
- **La cuerda superior es un total real pero minoritario.** KFG: 376 cuerdas superiores en 47 quipus; 86 son sumas (22,9%); 29/47 quipus (61,7%) tienen al menos una. `union=T` no sirve como marcador de summit (0/17 sumas). S4 (madre=suma hijos) 12,6%.
- **Continuidades vs innovaciones.** Continuidades plausibles: nudo decimal, color como categoría, jerarquía de cuerdas, dirección como sección, torsión binaria rara. Innovaciones coloniales/post-incas: quipus-tablero, confesión, seriación de ayllus, Collata logosilábico, objetos-firma, quipus de pastor unilineales, y **torsión = género/mitad con valor mitad** (XIX-XX), que es justamente la que no aparece en el corpus antiguo.
- **Para los no numéricos:** la plantilla es **partición, no magnitud**. Torsión/dirección cortan en bloques; color y banda son códigos locales; canutos/objetos marcan género/identidad; subsidiarias son subcategorías, no crías. Eso favorece la lectura **tally/etiqueta** de `n_no_numericos` y **no** la narrativa/silábica. La prueba decisiva barata: intersección de las particiones de torsión/dirección con los límites de grupo/banda en los 56 no numéricos, y auditoría de imágenes de UR179/180/178 y AS076/JC012.
- **Recomendación de siguiente ronda:** (1) conseguir las tablas completas de Tupicocha (Salomon 2004, apéndices), Anchucaya (RT 21287) y Collata (487 colgantes) para ampliar `cuerdas_con_clave.csv`; (2) probar la intersección de particiones en los 56 no numéricos; (3) hacer un control de transcripción KFG→OKR de la dirección en una muestra de imágenes; (4) no usar `union=T` como cuerda superior sin verificar la definición; (5) tratar la torsión como marcador de sección en los modelos de clase, no como “mitad”.
