# Monografía del archivo de Incahuasi (Inkawasi)

Autor: equipo `a_incahuasi` (DeepSeek). Fecha: 2026-10-17.
Scripts reproducibles en esta misma carpeta (`paso1_*.py` … `paso10_*.py`,
`tabla_por_quipu.csv`). Nulo con semilla 0.

## 1. Pregunta

¿Qué contiene y qué estructura tiene el conjunto de quipus de **Incahuasi/Inkawasi**
(Inca, valle de Cañete): los 23 quipus **JC001–JC023** y **UR255–UR280**
(29 fichas: UR255–UR280 con las parejas A/B 267, 273, 274)? En concreto:
(a) cómo es el conjunto; (b) si los quipus se relacionan entre sí
(secuencias/totales/estructuras/colores compartidos); (c) si hay una jerarquía
detalle/resumen; (d) qué registraba este archivo según la literatura.

## 2. Datos y método

- Fuente: `analisis/datos/{quipus,cuerdas,grupos}.csv` (Khipu Field Guide, KFG).
- Filtro: `procedencia == "Incahuasi"` en `quipus.csv` → **52 quipus, 5624 cuerdas**.
- Unidad de análisis = **quipu** (evita pseudorreplicación; BRIEF regla 1).
- `valor` 0 con `nudos` vacío = cuerda ausente (no cero real), se excluye de los valores.
- **Nulo** para relaciones entre quipus: **barajar los valores dentro de cada quipu**
  (500 permutaciones, semilla 0) y recalcular el estadístico; p empírico =
  `(1+#nulo≥obs)/(1+500)`. Para pruebas por par se aplica **BH-FDR (0.05)**; para las
  familias de pocas pruebas, se reporta el mínimo alcanzable con 500 permutaciones (p≤0.002).
- Identidad de objetos: cada nombre KFG mapea 1-a-1 a un KH distinto en
  `data/external/open-khipu-repository/data/okr-kh-numbers.csv` (no hay dos nombres
  para el mismo objeto). Las parejas `267A/B`, `273A/B`, `274A/B` son fichas
  separadas (fragmentos) y se tratan como quipus distintos.

## 3. Resultados

### 3.1 Descripción del conjunto

- **52 quipus, 5624 cuerdas, 772 grupos.** Tamaños muy dispares: de **4 cuerdas**
  (JC002, JC020) a **490** (UR262); mediana 76.
- **29 % de cuerdas sin nudos** (vastago sin valor): cifra alta, en buena parte fragmentos.
- Valores: de 1 a **98 718** (UR257); mediana global 30. Máximos anómalamente altos en
  UR257 (98 718), UR268 (15 039), JC007 (8 153), UR266 y UR275 (4 273).
- **Unión al cordón principal**: R 2337, V 1425, U 1394, Unknown 468.
  **No hay cuerdas superiores** (ningún valor `union = T`); `pc_estructura = "P"` para los 52.
- **Torsión del cordel**: S 4408, Z 1214, U 2. **Dirección de nudo** (racimos):
  Z 6137, S 1671, U 7 → los nudos van en **Z** (zurdo), replicando a Clindaniel (2019).
- **Profundidad**: colgantes 3762; subsidiarias nivel 1 = 1367, n2 = 376, n3 = 98,
  n4 = 17, n5 = 4 (árboles someros; sólo UR262 llega a nivel 5).
- **Colores dominantes**: AB (marrón claro) 1380, W (blanco) 1096, NB (marrón muy
  oscuro) 943, MB (marrón medio) 521; mezclas frecuentes W:MB, AB:MB, W:AB.

Tabla por quipu: `tabla_por_quipu.csv`.

### 3.2 El archivo se divide en DOS subconjuntos coherentes: serie JC vs serie UR

Hallazgo fuerte (determinista, no estadístico):
- **Torsión del cordel**: **todos** los quipus JC son **Z** (1214/1217 cuerdas);
  **todos** los quipus UR son **S** (4407/4407). Separación perfecta.
- **Unión**: JC → R 712, V 38 (mayoría recta); UR → R 1625, V 1387, U 1394 (verso
  y unknown abundantes).
- **Valores**: JC media 56.7, máx 8153; UR media 535.2, máx 98 718.
- **Metadatos históricos** (Clindaniel 2019): UR255–UR280 los registró Urton; JC001–JC023
  los **excavó Clindaniel**. La dicotomía Z/S refleja dos lotes/registros distintos.

Nivel: **apoyado con datos** (es un hecho de los datos; la interpretación histórica del
porqué es **propuesta**).

### 3.3 Relaciones ENTRE quipus (con nulos)

| Prueba | Observado | Nulo (semilla 0) | p | Veredicto |
|---|---|---|---|---|
| (A) k-gramas de valores compartidos, k=3 | 679 | 465 | 0.002 | señal aparente |
| (A) k=4 | 206 | 107 | 0.002 | señal aparente |
| (A) k=5 | 60 | 31 | 0.004 | señal aparente |
| (A) k=3 con **runs colapsados** | 369 | 298 | 0.012 | débil |
| (A) k=4 colapsado | 67 | 49 | 0.078 | **no** |
| (A) k=5 colapsado | 12 | 10.6 | 0.373 | **no** |
| (B) suma de grupo de *i* = valor de cuerda de *j* | 2645 | 1827 | 0.002 | exceso difuso |
| (B) sólo sumas ≥100 | 404 | 284 | 0.002 | exceso |
| (C) firmas de estructura de grupos idénticas | 0 | 0 | 1.0 | **no** |
| (C') multiconjunto de tamaños de grupo | 0 (de 1326) | — | — | **no** |
| (D) k-gramas de COLOR compartidos, k=3 | 2651 | 3011 | 1.0 | **no** |
| (E) k-gramas de SUMAS DE GRUPO compartidas, k=3 | 8 | 171 | 1.0 | **no** (opuesto) |
| (F) Jaccard de vocabulario de valores | 0.091 | 0.099 (nulo global) | 0.985 | **no** |

**Interpretación de las señales aparentes (la explicación aburrida primero):**
- **(A) se desvanece al colapsar los runs de valores repetidos consecutivos.** Los runs
  comunes son casi siempre de 1s (`[1,1,1,2]`, `[1,1,1,1,1,7,20]`, `[4,1,1,1,1]`). Con el
  control, k=4 y k=5 dejan de ser significativos. Los pocos runs "no triviales" son de
  longitud 4–5 entre 1326 pares (`JC009–UR262 [1,10,3,4]`, `JC013–UR272 [5,4,1,2,4]`,
  `UR263–UR271 [6,1,2,3,2]`): compatibles con azar. → **resultado negativo**.
- **(B) es un exceso difuso** (744/2652 pares, mediana 1, máx 55) que sobrevive incluso al
  nulo global (valores redibujados entre quipus) y a exigir sumas ≥100. Consistente con que
  los grupos reales son internamente homogéneos y el vocabulario de enteros pequeños es
  común, no con relaciones de archivo. **No se puede convertir en un hallazgo de
  contabilidad cruzada.** Lo reporto como positivo difícil de interpretar, con explicación
  trivial probable.

**Nada de lo anterior es un hallazgo entre dos nombres del mismo objeto**: los pares
`A/B` (267, 273, 274) tienen sólo 5, 1 y 3 valores compartidos y sumas muy distintas
(UR267A suma 6462 vs UR267B 24269) → **NO son "pares atados con registros similares"**.

### 3.4 Jerarquía detalle/resumen

- No hay cuerdas superiores ni estructura repetida (ninguna firma de grupos coincide).
- **Padre = suma de sus ≥2 hijas no vacías**: sólo **4 casos** de 228 nodos con ≥2 hijas
  (`JC022 p8s1=4`, `UR269 p36=110`, `UR276 p1=8`, `UR277 p114s1=5`); el nulo produce
  ~17 → los quipus registran **menos** sumas jerárquicas que el azar. → **sin jerarquía
  de suma padre=hijas**.
- Las **sumas de grupo** no se repiten de un quipu a otro (obs 8 << nulo 171). → **no hay
  "columnas de totales" compartidas** entre quipus.
- Conclusión: **no existe** en estos datos la jerarquía detalle/resumen que la hipótesis de
  "archivo" requeriría. Nivel: **resultado negativo robusto**.

### 3.5 Replicación del claim de Clindaniel (color = suma/resta/resultado)

La ficha `docs/fichas/2019-Clindaniel_grammar-inka-khipu.md` propone (proof of concept)
que en **UR267A**: **blanco W = suma, ámbar-marrón AB = resta, moteado AB:MB = resultado**,
con el ejemplo **"+106 − 15 = 91"**, y que **UR255 lo invierte** (AB = suma).

**Se reproduce EXACTAMENTE en los datos KFG:**
- UR267A: `p1 = 106 [W]`, `p2 = 15 [AB]`, `p3 = 91 [AB:MB]` → **106 − 15 = 91** ✔
- UR255: `p1 = 106 [AB]`, con la serie de cordones `= 15` también en **AB** (no en W) → la
  inversión W↔AB se confirma a nivel de color.
- Regularidad adicional: el valor constante **15** reaparece en **23 cordones** de UR267A
  (todos W) y en **23 cordones** de UR255 (todos AB), a intervalos regulares; es el mejor
  candidato a **unidad contable estandarizada** como las que postula Urton y Chu (2015).

Nivel: **apoyado con datos** (la aritmética y los colores cuadran); **propuesto** el
significado suma/resta/resultado; la unidad 15 es **propuesta**. Advertencia: es la misma
data que usó Clindaniel → **confirmación, no validación independiente**.

## 4. Controles

- Modelo nulo explícito en todas las pruebas entre quipus (barajado dentro de cada quipu,
  500 réplicas, semilla 0); para (B) y (F) se añadió un nulo **global** (valores
  redibujados entre quipus) y para (A) un control de **runs colapsados** que elimina el
  artefacto de repeticiones.
- **Corrección múltiple**: BH-FDR (0.05) en las pruebas por par de (A); en el resto, familias
  de ≤6 pruebas → umbral de Holm 0.05/6 = 0.0083; los p=0.002 sobreviven, los p≈0.01 (A
  colapsado k=3) no.
- **Resultados negativos reportados** explícitamente (secciones 3.3–3.4): no hay
  secuencias, totales, estructuras ni patrones de color compartidos entre quipus; no hay
  jerarquía de sumas; no hay vocabulario restringido.

## 5. Qué se registraba aquí (contraste con la literatura)

- **Urton y Chu (2015)**, `docs/fichas/2015-Urton_inkawasi.md`: archivo de **34 quipus** del
  **depósito estatal** de Inkawasi (Cañete), varios asociados a **ají, maní y frijol negro**;
  dos conjuntos de muestras **emparejadas y atadas** con "registros cuantitativos muy
  similares"; evidencia de **unidades contables estandarizadas** (cuadrículas). Función
  contable = apoyada; productos y unidades = propuestos; **sin controles** para la similitud.
- **Clindaniel (2019)**: Inkawasi **n=52**, 5708 cuerdas; **Z domina** (6209 Z vs 1704 S,
  p<0.0001) — lo replicamos (Z 6137 / S 1671); 83.7 % de cuerdas multicolor reproducen
  combinaciones de los *wrapped sticks*; color suma/resta/resultado en UR267A/UR255.
- **`docs/estado_del_arte.md`** (líneas 35, 83, 253, 293): confirma 52 quipus de Inkawasi;
  advierte que Urton 2005 no usó umbral estadístico y que "matches" entre valores decimales
  pequeños **pueden deberse al azar**.

**Contraste con nuestros datos:** la hipótesis "archivo con pares atados de registros
similares" **no se sostiene** en la transcripción KFG: los pares A/B no son similares ni hay
quipus con secuencias/sumas de grupo compartidas. El "registro similar" de Urton y Chu
podría estar en el **contexto físico** (quipus atados, hallados juntos) o en rasgos no
transcritos, no en una similitud numérica detectable aquí.

**Propuesta de lectura (nivel propuesto):** Inkawasi es un **almacén estatal inca**; estos
52 quipus serían **registros contables de productos almacenados/repartidos**, con
**checks-and-balances** (constante 15; un posible libro de suma/resta por color). El archivo
no es una jerarquía de detalle/resumen sino una colección heterogénea de registros
independientes, con dos lotes físicamente distintos (**JC** Z-twist, valores pequeños,
excavados por Clindaniel; **UR** S-twist, valores grandes, registrados por Urton).
La identificación de **ají/maní/frijol** es **especulativa** desde estos datos (no hay
etiquetas).

## 6. Resultados negativos (resumen)

1. No hay secuencias de valores compartidas entre quipus (señal aparente = artefacto de 1s).
2. No hay firma ni multiconjunto de estructura de grupos idéntico en 1326 pares.
3. No hay patrones de color compartidos en orden (obs < nulo).
4. No hay sumas de grupo compartidas entre quipus (obs << nulo).
5. No hay jerarquía padre=suma(hijas) (4 casos vs 17 esperados).
6. No hay vocabulario de valores más restringido de lo esperado (Jaccard ≤ nulo global).
7. Los pares A/B no son "pares atados con registros similares".

## 7. Nivel de evidencia global

- **Bien apoyado** (hechos de los datos): conteos, rangos, ausencia de cuerdas superiores,
  ausencia de firmas de grupo repetidas.
- **Apoyado con datos**: división JC(Z)/UR(S); dominancia de nudo Z; reproducción exacta de
  UR267A "+106−15=91" y de la inversión de color en UR255; constante 15 recurrente.
- **Propuesto**: color = suma/resta/resultado; unidad estandarizada 15; lectura del archivo
  como contabilidad de depósito.
- **Especulativo**: qué productos (ají/maní/frijol); significado semántico de los números.

## 8. Para el coordinador

- **El hallazgo más sólido es estructural, no semántico:** el archivo se parte en dos lotes
  —**JC** con torsión **Z** (1214/1217), valores pequeños (máx 8153) y **UR** con torsión
  **S** (4407/4407), valores grandes (máx 98 718)—; coincide con la historia de registro
  (JC excavado por Clindaniel, UR registrado por Urton). Es un hecho de los datos
  (**apoyado**); conviene tratarlos como subconjuntos separados en cualquier análisis futuro.
- **No encontramos NINGUNA relación numérica entre quipus que sobreviva a un nulo bien
  hecho:** ni secuencias, ni sumas de grupo, ni estructuras de grupo, ni patrones de color
  compartidos; y **no hay jerarquía detalle/resumen** (padre=suma(hijas) aparece 4 veces vs
  17 esperadas por azar). Recomiendo **abandonar** para este archivo la hipótesis de
  "quipus de resumen que totalizan quipus de detalle".
- **La señal de "secuencias compartidas" que aparece sin control es un artefacto de los
  runs de 1s:** al colapsar valores repetidos consecutivos, k=4 pasa de p=0.002 a p=0.078 y
  k=5 a p=0.373. Cualquier equipo que busque k-gramas de valores debe colapsar runs.
- **Confirmamos (no validamos) el proof-of-concept de Clindaniel:** UR267A = `106[W] −
  15[AB] = 91[AB:MB]` reproduce exactamente; UR255 invierte W↔AB. Es la única aritmética
  semántica (suma/resta/resultado por color) que cuadra, y está en **la misma data** que él
  usó. **Nivel: apoyado pero no independiente.**
- **Candidato a unidad contable estandarizada:** el valor constante **15** aparece en 23
  cordones de UR267A (blancos) y 23 de UR255 (AB), a intervalos regulares — apoya la
  "unidad estandarizada" de Urton y Chu (2015). **Propuesto**; merece verificación con las
  cuadrículas del piso del sitio y con JK/otros archivos.
- **Los "pares atados con registros similares" de Urton y Chu NO se ven en los datos:**
  los pares A/B (267, 273, 274) apenas comparten 1–5 valores y tienen sumas muy dispares.
  Si existen, la similitud es **contextual/física**, no numérica transcripcional.
- **Lectura propuesta del sitio:** depósito estatal inca de productos, con registros
  contables con checks-and-balances (constante + suma/resta por color). Los productos
  (ají/maní/frijol) son **especulativos** desde estos datos.
- **Siguiente ronda recomendada:** (1) conseguir el contexto de excavación y la asociación
  quipu–contexto (ausente en el OKR, `docs/fuentes_sin_datos_abiertos.md`); (2) probar el
  sistema de color suma/resta/resultado en **más** quipus de depósito (buscar el "género" que
  Clindaniel no encontró); (3) cruzar JC/UR con `khipu.db` (OKR) para ver si la dicotomía
  Z/S se mantiene en la transcripción OKR; (4) buscar la constante 15 y otras constantes
  repetidas en todo el corpus como posible vocabulario de unidades.
