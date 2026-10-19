# UR1057 (KH0068 / AS057) — lectura profunda de un quipu

**Carpeta:** `analisis/ds/k_UR1057/` · **Fecha:** 2026-10-18 · **Semilla:** 0 (1000 permutaciones)

---

## 0. Ficha del objeto

| campo | valor |
|---|---|
| KFG | UR1057 |
| OKR | KH0068 |
| N.º original | AS057 (Ascher) |
| Museo | Museo de Ica, Ica, Perú (n.º 7) |
| Procedencia | **desconocida** (el museo no es procedencia) |
| Cordón principal | 195,5 cm; color YB:FB |
| Cuerdas | 589 (percentil 98,5 de tamaño en el corpus) |
| Datos | KFG (`cuerdas.csv`, `grupos.csv`) + OKR (`khipu.db`) + notas de Ascher (pp. 340–342) transcritas en OKR |

Las notas de Ascher que acompañan al registro OKR son la única documentación primaria localizada sobre este objeto y describen su construcción con precisión (marcadores, banderas, etiquetas, patrón de color). Las uso como fuente, no como interpretación.

---

## 1. Pregunta

¿Qué estructura tiene UR1057, qué aritmética contiene y qué tipo de registro es? En concreto: ¿censo, tributo, depósito, calendario u otro? ¿Qué serían las filas y las columnas? ¿Qué no encaja?

---

## 2. Método

### 2.1 Reconstrucción de la estructura

`grupos.csv` da **94 grupos** para este quipu, pero esa segmentación es un artefacto: KFG corta cada vez que hay un espacio, y los **marcadores** (cordones cortos y gruesos enrollados al principal) y las **banderas** (cordones largos/cortos sin nudos) se registran como "colgantes" con valor 0. La descripción de Ascher (nota 6) es explícita: *"By spacing, the quipu is separated into 24 groups. Each group has the same basic pattern: BB, (YB, W, YB, YB), BB, (YB, W, YB, YB), (YB, W, YB, YB), BB, Marker, (YB, W, YB, YB), (FB:W with a subsidiary of YB/0G, YB, 0G)"*.

Reconstruí los 24 grupos con tres anclas independientes:

1. **Terminadores**: aparecen 24 cordones de color `0G` (el último cordón de cada grupo en el patrón). Dos de ellos pertenecen a cuerdas bicolor y dos pares de grupos quedaron unidos en una primera pasada, de modo que la segmentación final se ancló en los 24 marcadores internos y se validó con los terminadores.
2. **Marcador interno**: cada grupo tiene exactamente un marcador entre el 3.er y el 4.º subgrupo; hay 40 marcadores en total (24 internos + 16 separadores entre grupos) y 9 banderas.
3. **Alineación de color**: subgrupos 1–4 = `Y,W,Y,Y`; subgrupo 5 = `W:FB` (con subsidiaria `YB/0G`), `YB`, `0G`.

Una vez corregidos esos dos casos, las tres anclas coinciden en los 24 grupos. Resultado: **24 grupos**, con 20–23 cordones cada uno, separados físicamente cada **7,2 cm** en promedio sobre 170 cm de cordón principal (rango 5–11 cm; el último grupo deja 23 cm de cordón vacío).

Composición exacta del objeto (cuadra con 589):

```
589 cuerdas
 = 559 de nivel 0 (KFG)
     = 510 colgantes reales  (456 de la retícula + 53 cabeceras BB + 1 cuerda superior mal clasificada)
     + 40 marcadores (M)
     +  9 banderas (F)
 +  30 subsidiarias (29 de nivel 1 + 1 de nivel 2)
```

De las 30 subsidiarias, **24 son estructurales**: la 4.ª celda del subgrupo 5 es la subsidiaria `YB/0G` de la madre `W:FB`. Por tanto la retícula de datos es

> **24 grupos × 5 subgrupos × 4 cordones = 480 celdas, y las 480 existen físicamente** (ninguna celda falta; lo que falta en muchas es el nudo). Verificado: la matriz 24×20 no tiene ni un `NaN` (`matriz_24x5x4.csv`), y hay exactamente una subsidiaria estructural por grupo (24/24).

Esto es el hallazgo estructural central: el objeto es una **retícula completa 24×20**, no una colección de cuerdas.

### 2.2 Nulos y corrección

Todos los contrastes usan **permutación dentro del quipu**, 1000 iteraciones, semilla 0. El estadístico y lo que preserva cada nulo se detallan en la tabla de la §4. La familia confirmatoria tiene 8 pruebas con p; se corrige con **Holm**. Las pruebas descriptivas (sin nulo posible) se marcan como tales. Nada se infiere de un p-valor aislado sin mirar el tamaño del efecto.

Advertencia metodológica previa: **el 68,2 % de los colgantes (347/509) no tiene ningún nudo**. Un valor `0` con `nudos` vacío es *ausencia*, no un cero contable (regla del BRIEF). Por tanto la "media de valores" de este quipu no debe interpretarse como una media de cantidades.

---

## 3. Resultados

### 3.1 La retícula y los colores

- **24 grupos**, 480 celdas, 20 celdas por grupo.
- **Plantilla de color casi invariable.** En 456 celdas con color legible, **90,8 %** coincide con la firma canónica `(YB,W,YB,YB)×4 + (W:FB, YB, 0G)`. **11 de 24 grupos** tienen las 19 celdas colgantes exactamente en su color canónico (la 20.ª, la subsidiaria, también); el resto tiene 1–2 desviaciones o colores perdidos.
- Nulo (barajar colores entre cuerdas del quipu): p = 0,001 (mínimo alcanzable con 1000 permutaciones). El color **no es un canal de datos variable**: es la *cabecera* de la tabla, fija por posición.
- El color se repite con la posición, no con el valor: dentro de cada celda (grupo, subgrupo, posición) el color es prácticamente constante. Un test color×valor no tiene nada que medir aquí (control negativo, §5).

### 3.2 Los valores: dos registros en un objeto

La bandera **F1** (ordinal 156, justo tras el 7.º grupo) parte el quipu en dos mitades desiguales, y las dos tienen estadística distinta:

| | P1 (grupos 1–7) | P2 (grupos 8–24) |
|---|---|---|
| cordones | 146 | 363 |
| sin nudo | 62 (42,5 %) | 285 (78,5 %) |
| con valor > 0 | 84 | 76 |
| suma (sin subsidiarias) | **776** | **90** |
| máximo (colgante) | 104 | 0–4 (un solo 5) |
| valores distintos | 0–104 (24 valores) | 0,1,2,3,4,5 |
| etiquetas en nudos | sí (sg1 = YB:0G, sg2 = W) | no |

En P2, además, los valores se concentran por subgrupo de forma extrema:

- sg1 y sg2: **97 % de cuerdas sin nudo** (2 valores > 0 en 68 cuerdas cada uno).
- sg3: 93 % sin nudo (5 valores > 0).
- **sg4: 78 % con nudo, y los 53 nudos son exactamente `1E`** (nudo en ocho, valor 1). En 9 de 17 grupos, sg4 = `1,1,1,1`; en 3 más, `1,1,0,1`.
- sg5: 78 % sin nudo; aquí están todos los 2 y 4 (y un 5 aislado).

Es decir: en P2 el subgrupo 4 es una **plantilla repetida de cuatro "1"** (cuatro nudos en ocho idénticos), no una medición. El contenido real de P2 son ~20 nudos dispersos.

Los patrones de sg4 en P2: `1111`×9, `1101`×3, `1001`, `1100`, `1110`, `0000`, `0001`. El grupo 22 es el único **completamente vacío** (0 nudos en 22 cuerdas).

En P1 los sg4 sí llevan cantidades: [23,38,13,24], [6,9,2,31], [2,5,7,10], [6,23,35,53] en los cuatro grupos poblados; los otros tres (g2, g3, g6) son plantilla `1,1,1,1` con casi todo lo demás vacío.

### 3.3 Aritmética: no hay aritmética

Probé las relaciones de Ascher una por una, con nulo:

| relación | observado | esperado bajo nulo | p |
|---|---|---|---|
| madre = Σ subsidiarias | 1/20 no trivial (p384: 1 = 1); el caso con subsidiaria grande falla (p385: 1 vs 145) | — | — |
| cuerda superior = Σ grupo | T1=5 coincide con la suma del grupo 19 (pero 3 grupos suman 5); T2=2 coincide con el grupo 15 (no adyacente); ninguna es la suma de su propio grupo | — | coincidencia trivial (post hoc: P≈0,13 y 0,04) |
| sg4 = sg1+sg2+sg3 (por grupo) | 1/24 | 2,19 | 0,91 |
| sg5 = Σ sg1…sg4 | 1/24 | 1,00 | 0,66 |
| sg5 = sg1 | 1/24 | 3,58 | 0,98 |
| Σ sg1–4 = Σ sg5 (no trivial) | 6/24 | > 6 (cola baja) | 0,98 |

**Ninguna relación aditiva supera al azar; varias están por debajo.** El quipu no es un libro de cuentas que cuadre: no hay totales, ni cuerdas superiores sumatorias, ni jerarquía madre/subsidiaria aritmética.

Las "relaciones de suma" que el buscador automático del KFG reporta para UR1057 (21 `pendant_pendant_sum`) son **artefactos de sobreajuste**: por ejemplo, p154 = 104 aparece como "suma" de **54 cuerdas** dispersas entre los grupos 11 y 22, y p16 = 38 como suma de **37 cuerdas**. Con 68 % de ceros, cualquier número se deja expresar como suma de un subconjunto grande. Lo reporto como resultado negativo y como advertencia de método.

### 3.4 Periodicidad y serie

- La autocorrelación máxima de la secuencia de valores (lags 1–20) es |ρ| = 0,585 (lag 1), p = 0,001 incluso con nulo intra-grupo. **Pero no es información serial**: la produce el bloque de cuatro `1` consecutivos del sg4. Es la plantilla, no un mensaje.
- Tendencia de la suma de grupo con el índice: ρ = −0,458 (p = 0,017) en los 24; **desaparece dentro de P2** (ρ = −0,076, p = 0,77). Es un efecto de la partición P1/P2, no una tendencia.
- No hay seriación ni progresión: los vectores de 4 valores de P1 son monótonos 34/35 veces sólo porque hay muchos empates y valores pequeños (no lo cuento como hallazgo).

### 3.5 Anclaje en el corpus

| métrica | UR1057 | percentil | mediana del corpus |
|---|---|---|---|
| n.º de cuerdas | 589 | 98,5 | 81,5 |
| fracción sin nudo (todas las cuerdas) | 0,688 | 94,6 | 0,219 |
| valor medio | 1,76 | 6,3 | 17,8 |
| fracción con valor > 0 | 0,309 | 5,6 | 0,779 |
| repetición de color (ventanas de 12) | 0,479 | 83,7 | 0,000 |

UR1057 es un objeto **grande, casi vacío y de valores muy bajos**. No es un quipu "típico" y no debe usarse para estimar tasas del corpus.

---

## 4. Controles

Familia de 8 pruebas con nulo, Holm (m = 8):

| # | prueba | estadístico | observado | p | p Holm | nulo |
|---|---|---|---|---|---|---|
| A | plantilla de color | proporción de acierto | 0,908 (n=456) | 0,001 | **0,008** | baraja colores entre cuerdas del quipu |
| B | subgrupo × clase de valor | χ² | 196,2 | 0,001 | **0,008** | baraja valores entre cuerdas |
| C | blancura por subgrupo | sd de las 5 proporciones | 0,303 | 0,001 | **0,008** | baraja el indicador "sin nudo" |
| D | sg4 = (1,1,1,1) | n.º de grupos | 12/24 | 0,001 | **0,008** | permuta valores dentro de cada grupo |
| E | filas duplicadas | n.º de filas en duplicados | 2 | 0,005 | 0,015 | permuta valores dentro de (sg,pos) |
| F | autocorrelación máx. | \|ρ\| | 0,585 | 0,001 | 0,008 | permuta dentro de grupo |
| G | tendencia (solo P2) | ρ | −0,076 | 0,768 | 1,000 | permuta sumas |
| H | Σ sg1–4 = Σ sg5 | coincidencias | 6 | 0,984 | 1,000 | permuta dentro de grupo |

Notas de interpretación:

- **A, B, C y D no son cuatro hallazgos independientes**: son cuatro caras del mismo hecho (la plantilla 24×5×4 con el sg4 "1,1,1,1"). Con Holm quedan significativos, pero deben leerse como **un** resultado estructural.
- **E** (filas duplicadas) también es consecuencia de la plantilla: el duplicado es la fila "todo cero salvo `1,1,1,1`", que aparece dos veces porque es la fila base. No es una "cuenta duplicada" de Urton.
- **F** está contaminado por el bloque de cuatro `1` consecutivos; no lo interpreto como codificación serial.
- **H** es el control más informativo: la aritmética observada está *por debajo* del azar.

---

## 5. Resultados negativos (explícitos)

1. **No hay suma de subsidiarias**: de 20 madres con subsidiaria > 0, sólo una coincide (p384: 1 = 1, trivial); el caso con una subsidiaria grande la rompe (p385: madre 1, subsidiaria 145). Las 24 subsidiarias estructurales valen 0 o 1 y son una *posición* del subgrupo 5, no un desglose.
2. **No hay cuerdas superiores sumatorias**: las dos T (T1 = 5, T2 = 2) están atadas a marcadores, no cierran grupos, y ninguna coincide con la suma del grupo al que están asociadas (T1 coincide con el grupo 19, pero 3 grupos suman 5; T2 coincide con el grupo 15, que no es adyacente). Ambas son compatibles con azar.
3. **No hay relación grupo = Σ subgrupos, ni subgrupo = Σ posiciones, ni patrón de totales.** Con nulos, todas las relaciones están al nivel del azar o por debajo.
4. **No hay código binario R/V**: 517 cuerdas recto, **0 verso**, 55 desconocidas. La hipótesis R/V del valle del Santa es inaplicable aquí (aunque el 55 % del corpus también tiene 0 verso: no es anomalía, es ausencia).
5. **La dirección de nudo no es un canal independiente**: 102 de 103 nudos en ocho son Z y los nudos largos son S. La dirección está determinada por el tipo de nudo, no codifica nada aparte. (Coincide con la conclusión negativa de Ascher 2005.)
6. **La torsión no aporta**: 542 S, 28 U, 2 Z en las 589 cuerdas. Uniforme.
7. **No hay lectura calendárica**: total de la retícula 866 (P1 776 + P2 90; sin subsidiarias), no aparecen 365, 584, 354, 328, 260 ni 145 como agregados; los grupos tienen 20–23 cuerdas, no 29–31; no hay 12, 18 ni 20 unidades. El único 145 está en una subsidiaria aislada (§6.3) y no es un total.
8. **El "número de cuerdas = 559" de KFG sobrecuenta**: incluye 40 marcadores y 9 banderas. Los colgantes reales son 510. Cualquier estadístico de corpus basado en `num_pendant_cords` está inflado en quipus con marcadores.

---

## 6. Interpretación

### 6.1 Qué está demostrado

- UR1057 es una **retícula completa de 24 filas × 20 columnas** (5 subgrupos × 4 cordones), con cabeceras de color fijas y separadores físicos (marcadores/banderas).
- Está **partida en dos registros** por la bandera F1: 7 filas cuantitativas (P1) y 17 filas casi vacías (P2).
- El 68 % de las cuerdas no tiene nudo; el contenido numérico es escaso y se concentra en 4 filas de P1.
- No contiene aritmética verificable.

### 6.2 Qué tipo de registro es (lectura más probable)

**Filas y columnas.** La lectura que mejor ajusta es: **cada fila = una unidad registrada** (un ayllu, una casa, un almacén, un ítem) y **cada columna = una categoría de 4 posiciones**, repetida 5 veces. Es decir, una **lista/tabla administrativa**, no un libro de sumas.

Ordeno las hipótesis por ajuste a los datos:

1. **Registro tabular administrativo (censo/lista de unidades)** — *apoyado con datos* en la forma (24 filas, 20 campos, celdas completas, sin totales), *propuesto* en el contenido. Encaja con: 24 unidades espaciadas regularmente, valores 0–104 en 4 filas (¿personas?, ¿tributarios?), filas "base" de 4 en el resto.
2. **Depósito/inventario por ítem y período** — *propuesto*. Encaja con: muchas celdas vacías (sin stock), valores por celda, ausencia de totales, 5 subgrupos que podrían ser 5 períodos o 5 productos y 4 cordones que podrían ser 4 medidas o 4 parcialidades. No hay evidencia interna que lo distinga del censo.
3. **Tributo** — *propuesto, más débil*: un registro de tributo suele cerrar con totales o cuotas; aquí no hay ni totales ni cuotas reconocibles.
4. **Calendario** — **no apoyado**: los tests numéricos son negativos (§5.7). No descarto que la cuadrícula 24×20 tenga una lectura temporal (24 × 20 = 480 días ≈ 16 meses), pero es numerología sin control y no la sostengo.

**Nivel:** la *forma tabular* es **apoyada con datos**; que sea censo y no depósito es **propuesto**; cualquier atribución semántica concreta (ayllus, maíz, mitayos) es **especulativa**.

### 6.3 El detalle que más me intriga: P1 vs P2

P1 (7 filas) tiene valores hasta 104, nudos etiquetados y suma 776. P2 (17 filas) tiene, en la mayoría de las filas, **cuatro "1" idénticos** (9 de 17 exactamente `1,1,1,1`) y suma 90. Eso no es un censo homogéneo: parece **un formulario con 7 filas llenas y 17 filas sólo pautadas**, o **dos registros distintos cosidos en el mismo cordón** (uno cuantitativo, otro categórico/booleano). Las etiquetas de P1 (cordones de 2 cm atados a los nudos, YB:0G en sg1 y W en sg2) son un canal aparte que sólo existe en la mitad cuantitativa: o marcan "esto es dato", o identifican la categoría del nudo. No hay datos suficientes para decidir (25 cuerdas etiquetadas en la nota de Ascher, ninguna medición independiente).

### 6.4 Anomalías y lo que no encaja

| anomalía | dato | lectura |
|---|---|---|
| **145** en `p385s1` | la única subsidiaria con valor grande (100+40+5), en el grupo 17, sobre una madre que vale 1 | outlier real; ¿agregado posterior, “etiqueta” o error de lectura? Es el mayor valor del quipu y está fuera de la retícula |
| grupo 22 completamente vacío | 22 cuerdas, 0 nudos | fila no llenada (¿registro incompleto?) |
| 23 cm de cordón vacío al final | tras el grupo 24 | ¿un grupo 25 previsto o perdido? |
| `1E` con dirección S en `p385` | 1 de 103 nudos en ocho | la excepción a la regla E→Z; está en el mismo grupo del 145 (¿rehecho?) |
| grupo 23: un 5 en sg1 | único valor > 1 en sg1–3 de todo P2 | rompe la regla "sg1–3 sólo 0/1" |
| `p161s1` | nota KFG: "no es subsidiaria, es una cuerda adicional" | error de la base; 1 cuerda mal clasificada |
| ≈14 cuerdas no observadas / desaparecidas | notas KFG | huecos de registro que afectan la completitud de la retícula (aunque las 480 celdas existen) |
| colores perdidos | ≥3 celdas de P2 y varias de P1 sin color | no afecta la plantilla (los colores faltantes se concentran en cuerdas dañadas) |

### 6.5 ¿Información no numérica?

Sí, pero **en la forma, no en los valores**: el color, el número de subgrupos, la posición del marcador y las banderas constituyen un **esquema** (como los encabezados de una tabla). Eso es información estructural, no un texto. Las tres candidatas a información no numérica *dentro* del contenido son:

- las **etiquetas** atadas a nudos (canal aparte, sólo P1);
- el **patrón de celdas con/sin nudo** (¿una lista de presencia?);
- el **145** y los valores 2/4 restringidos al sg5 (¿marcadores categóricos?).

Ninguna se puede contrastar con los datos disponibles; las tres quedan en **especulativo**.

---

## 7. Nivel de evidencia (resumen)

| afirmación | nivel |
|---|---|
| 24 grupos × 5 subgrupos × 4 cordones; 480 celdas completas | **demostrado** (dato + notas de Ascher) |
| plantilla de color fija (90,8 %; p Holm = 0,008) | **apoyado con datos** |
| dos registros separados por F1 (P1 cuantitativo / P2 casi vacío) | **apoyado con datos** |
| ausencia de aritmética interna (todos los tests ≤ azar) | **apoyado con datos** (resultado negativo) |
| el objeto es una tabla/lista administrativa, no un libro de sumas | **apoyado con datos** (forma) |
| es un censo (y no un depósito) | **propuesto** |
| filas = ayllus/casas; columnas = categorías de 4 posiciones × 5 | **propuesto** |
| calendario | **especulativo / no apoyado** |
| etiquetas = marcas de categoría o de "dato" | **especulativo** |
| 145 y sg5 como "etiquetas de identidad" (Urton 2005) | **especulativo** |

---

## 8. Para el coordinador

- **UR1057 es una retícula completa 24×5×4 = 480 celdas**, no una colección de cuerdas: 24 grupos separados cada 7,2 cm, 5 subgrupos con la misma firma de color (Y,W,Y,Y)×4 + (W:FB, YB, 0G), 4 cordones por subgrupo (el 4.º del sg5 es una subsidiaria estructural). La nota de Ascher (OKR, pp. 340–342) lo confirma; KFG lo parte en 94 "grupos" por los marcadores.
- **El 68 % de los colgantes no tiene nudo** (347/509). UR1057 está en el percentil 94,6 de blancura y 6,3 de valor medio del corpus: es un objeto grande y casi vacío.
- **Dos registros en uno**: la bandera F1 separa 7 filas cuantitativas (suma 776, máx. 104, nudos etiquetados) de 17 filas casi vacías (suma 90, valores 0/1/2/4; la cifra excluye la subsidiaria de 145). En P2 el subgrupo 4 es una plantilla de cuatro nudos `1E` idénticos (9/17 grupos = `1,1,1,1`); el grupo 22 está en blanco.
- **No hay aritmética**: madre ≠ Σ subsidiarias; ninguna cuerda superior cierra un grupo; sg4 ≠ Σ sg1–3, sg5 ≠ Σ resto. Todos los tests quedan al nivel del azar o por debajo (Holm).
- **Las 21 "sumas" que reporta KFG son sobreajuste**: p154 = 104 aparece como suma de 54 cuerdas dispersas. No usar `ascher_sum_relations` sin nulo en quipus con muchos ceros.
- **Controles**: plantilla de color 90,8 % (p Holm = 0,008), subgrupo×valor χ² = 196 (p Holm = 0,008), blancura por subgrupo (p Holm = 0,008), sg4 = 1,1,1,1 en 12/24 grupos (p Holm = 0,008). Los cuatro son caras del mismo hecho estructural.
- **Negativos fuertes**: 0 cuerdas verso (R/V inaplicable); dirección de nudo determinada por el tipo (E→Z, L→S); torsión uniforme; ningún número calendárico (365/584/354/260) ni agregado que los produzca.
- **Lectura más probable**: tabla administrativa de 24 unidades × 20 campos (censo/lista de unidades, con depósito/inventario como alternativa igual de compatible). La forma tabular es **apoyada con datos**; "censo" es **propuesto**; el calendario es **especulativo y no apoyado**.
- **Anomalías a revisar**: `p385s1` = 145 (el mayor valor, fuera de la retícula, en el grupo con el único nudo `1E` dirección S), grupo 22 vacío, 23 cm de cordón final sin usar, ≈14 cuerdas no observadas.
- **Siguiente ronda**: (i) buscar en el corpus otros quipus con retícula repetida 24×n y comparar su distribución de blancura (¿es una clase de objeto?); (ii) conseguir las notas de Ascher pp. 340–342 completas y las fotos del Museo de Ica n.º 7 para verificar las 25 etiquetas; (iii) probar si el patrón de celdas con/sin nudo de P2 correlaciona con algo externo (no con los valores, que ya probé); (iv) no usar este quipu para estimar tasas de corpus.

---

## 9. Reproducibilidad

| script | salida |
|---|---|
| `01_estructura.py` | grupos de `grupos.csv`, tamaños, posiciones |
| `02_reconstruir.py` | segmentación por terminadores 0G y marcadores |
| `03_tabla.py` | `pendientes_estructurado.csv`, `matriz_24x5x4.csv`, `out_03.txt` (límites manuales de los 24 grupos) |
| `05_stats.py` | `tests.csv` (primera batería) |
| `06_corpus.py` | percentiles frente a 410–453 quipus |
| `07_stats2.py` | `tests2.csv` (batería con nulos y Holm) |
| `08_relaciones.py` | relaciones aditivas y monotonía |
| `09_matriz.py` | matriz 24×5×4 definitiva (con la subsidiaria como celda 5.4) |

Todo con semilla 0 y 1000 permutaciones. Los CSV de trabajo están en esta carpeta. No se modificó nada fuera de `analisis/ds/k_UR1057/`.
