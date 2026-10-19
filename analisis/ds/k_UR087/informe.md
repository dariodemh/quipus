# Lectura profunda de un quipu: UR087 (Valle del Santa)

**Autor:** equipo `k_UR087`. **Fecha:** 2026-10-17. **Datos:** `analisis/datos/` (KFG) + `data/external/open-khipu-repository/data/khipu.db` (OKR).
**Scripts reproducibles:** `analisis_UR087.py`, `controles_UR087.py`. **Volcado de estructura:** `estructura_UR087.txt`.

---

## 1. Pregunta

Reconstruir la estructura completa de **UR087** (= KH0323, Museo Temple Radicati, procedencia registrada "Santa", 370 cuerdas según KFG) y decidir, con controles nulos:
1. ¿Qué estructura tiene (grupos, subsidiarias, colores, cuerdas superiores, uniones, direcciones de nudo)?
2. ¿Qué aritmética interna contiene, y resiste un modelo nulo?
3. ¿Cuál es la lectura más probable (censo, tributo, depósito, calendario, otro) y con qué nivel de evidencia?
4. ¿Qué no encaja y podría ser información no numérica?

Contexto: los seis quipus UR087–UR092 (KH0323–KH0328) son el "caso Rosetta" del valle del Santa, asociado a la **revisita de 1670 de San Pedro de Corongo** (Medrano y Urton 2018; FitzPatrick 2024; Contreras 2026).

## 2. Método

- **Unidad de análisis = el quipu.** Los contrastes a nivel de cuerda usan **permutaciones dentro de UR087** (barajar valores/cuerdas, 1000 veces, semilla 0) y **p-valor empírico** `(1+Σ[null≥real])/(1+1000)`.
- Para el corpus: comparación **controlando por tamaño** (regresión `conteo ~ nº colgantes`, z de residuo) y **corrección de Holm**, porque los conteos brutos de relaciones de suma crecen con el tamaño del quipu.
- Se distingue el campo `union` de KFG del campo `ATTACHMENT_TYPE`/`CORD_CLASSIFICATION` de OKR (no coinciden; ver §4).
- Los 0 sin nudos se tratan como **ausentes**, no como ceros.

## 3. Resultados

### 3.1 Estructura reconstruida

| Rasgo | Valor |
|---|---|
| Cuerdas totales | 370 (KFG) / 371 (OKR) |
| Colgantes (nivel 0) | 306 |
| Subsidiarias (nivel >0) | 64 |
| Cuerdas superiores (OKR `CORD_CLASSIFICATION='T'`) | **13** |
| Marcadores (OKR `='M'`, 1,5–2,5 cm) | **5** |
| Cuerdas sin nudos (valor 0) | 49 |
| Torsión | S 366, Z 4 |
| Terminación | K 307, R 33, B 29, D 1 |
| Direcciones de nudo (en el campo `nudos`) | Z 323, S 40, U 1 |
| Suma de valores de colgantes | 1234 |

**La unidad estructural real no es el "grupo" de `grupos.csv`** (56 grupos definidos por espacios en el cordón principal; alternan tamaños 6–9 y 1) **sino el *run* de color**: una racha de colgantes del mismo color. UR087 tiene **65 runs de color, de los cuales 41 son de exactamente 6 cordeles** (246 de los 306 colgantes = **80,4 %**). Los "grupos de 1" de `grupos.csv` son casi siempre (a) **cuerdas superiores** (ver 3.3) o (b) **separadores sin nudos** de color LG/G0.

### 3.2 Estructura interna de los runs de 6 (la "fila")

Tratando los 41 runs de 6 como una matriz 41×6 (medias por columna):

```
col:        0     1     2     3     4     5
media:    1,22  2,73  1,20 13,05  1,37  1,37
% ≤ 2:    0,98  0,54  0,95  0,02  0,93  0,95
```

- La **columna 3** es el valor grande en **40/41 filas** (media 13, máx 26) y correlaciona 0,876 con la suma de la fila.
- La **columna 1** es intermedia; las columnas 0, 2, 4, 5 casi siempre valen 1 (a veces 0–3).
- Es decir: cada run de 6 parece una **fila de 6 casillas**, con una cantidad dominante en la casilla 3 y cinco casillas de conteos pequeños.

### 3.3 Cuerdas superiores y relaciones de suma

OKR clasifica **13 cordeles como cuerdas superiores (T)**: `p7, p14, p21, p40, p47, p54, p61, p68, p75, p88, p95, p102, p109` (valores 15, 21, 13, 20, 16, 22, 20, 20, 10 y cuatro 0). **KFG las registra como `union=U` (desconocida), no como T**, de modo que un análisis basado solo en KFG las "pierde". Las cuatro últimas (p88, p95, p102, p109) son además de color LG y **sin nudos**.

KFG ya tiene calculadas relaciones de suma exactas para UR087:

| Tipo (KFG) | UR087 | percentil bruto del corpus |
|---|---|---|
| pendant–pendant sum | 65 | 95,8 % |
| pendant–pendants by color | 55 | 98,2 % |
| indexed pendant sum | 13 | 93,5 % |
| cluster–cluster sum | 6 | 98,9 % |
| sum top cords | 2 | 98,0 % |

Ejemplos verificados a mano:
- **p7 = 15 = 1+1+10+1+1+1** = suma exacta del run de 6 anterior (`p1..p6`). ✔
- `p47 = 16` = suma del **cordel en la posición 0** de los clusters 0, 2, 4, 6, 7, 8, 10 (suma "por columna"). 
- `p167 = p192 = p217 = 22` = `11 (YB, cluster 10, pos 3) + 11 (AB, cluster 12, pos 3)` (suma de una misma columna en dos filas).

Es decir, la aritmética existe pero es **indexada/columnar** (suma de la misma posición a través de varias filas de 6), no "grupo = suma del grupo".

### 3.4 Color y unión

- **No hay periodicidad de color** ni a nivel de cuerda (p=1,0 para período 6) ni a nivel de run (períodos 1–6, todos p>0,06). El orden de colores de los 41 runs es `AB, W, AB, W, AB, YB, AB, …` (irregular). La única señal de color fuerte es la **agrupación en runs** (períodos 1–3 a nivel de cuerda: p=0,001), trivial.
- **UR087 no tiene ni una sola cuerda "verso"**: OKR da `ATTACHMENT_TYPE` = **R 310 / U 61 / V 0**. Es un espécimen **puramente recto** (uno de dos; ver §4).

## 4. Controles (nulo, p-valor, multiplicidad)

### 4.1 Nulos internos (permutación dentro de UR087, 1000×, semilla 0)

| Hipótesis | Real | Nulo (media) | p |
|---|---|---|---|
| Colgante = suma de sus subsidiarias | 7/58 | 9,5 | 0,90 (negativo) |
| Cordel = suma de los 6 colgantes previos | 4 | 1,58 | 0,070 (n.s.) |
| Cordel = suma de cualquier bloque contiguo (2–8) | 43 | 47,2 ± 5,8 | 0,78 (negativo) |
| Valores iguales a distancia 1 / 2 / 3 | 70 / 79 / 70 | 76,9 / 76,5 / 76,3 | 0,93 / 0,36 / 0,91 (negativo) |
| Tripleta con diferencias iguales (progresión) | 67 | 68,9 ± 5,1 | 0,68 (negativo) |
| Periodicidad de color período 6 | 33 | 71,6 | 1,00 (negativo) |

### 4.2 Control de tamaño para las relaciones de suma (el control clave)

El aparente "top 2–6 % del corpus" **desaparece al controlar por tamaño**, porque UR087 es un quipu grande (306 colgantes, top-14 del corpus) y **los conteos de sumas crecen con el tamaño**. Regresión `conteo ~ nº colgantes` (z de residuo):

| Tipo | UR087 | predicho | z | p |
|---|---|---|---|---|
| pendant–pendant | 65 | 57,0 | 0,47 | 0,64 |
| por color | 55 | 33,2 | 1,84 | 0,065 |
| indexed | 13 | 20,4 | −0,85 | 0,40 |
| cluster–cluster | 6 | 2,3 | 1,29 | 0,20 |
| top cords | 2 | 0,3 | 2,19 | 0,029 |

**Holm (5 contrastes):** p ajustados = 0,143 / 0,262 / 0,595 / 0,795 / 0,639. **Ninguna relación de suma es significativamente más frecuente en UR087 que en quipus de su tamaño.** La explicación aburrida (tamaño) gana.

### 4.3 La firma que SÍ es distintiva: los runs de 6

Frente a la pregunta de Medrano–Urton ("grupos de seis cordeles codificados por color"), el rasgo que separa a UR087 es estructural:

- Fracción de colgantes en runs de **exactamente 6**: UR087 = **0,804**; percentil 99,1 % del corpus y **percentil 100 % entre los 118 quipus grandes (≥100 colgantes)**, con **p(≥) = 0,008**.
- Los otros quipus de esta "familia" con fracciones altas incluyen a **sus hermanos del Santa**: UR092 (1,00) y UR091 (0,73). Esto **apoya con datos** que los seis quipus del Santa comparten la convención de "grupos de 6 colores".

### 4.4 Los seis del Santa en OKR (attachment / superiores / marcadores)

| KH | Quipu | Colgantes | T | M | Attachment |
|---|---|---|---|---|---|
| KH0323 | **UR087** | 306 | **13** | **5** | **R 310 / U 61 (puro recto)** |
| KH0324 | UR088 | 54 | 0 | 0 | V 54 / U 48 (puro verso) |
| KH0325 | UR089 | 206 | 0 | 2 | V 207 / U 81 (puro verso) |
| KH0326 | UR090 | 108 | 0 | 0 | **R 40 / V 69 (mixto)** |
| KH0327 | UR091 | 90 | 0 | 0 | V 93 / U 32 (puro verso) |
| KH0328 | UR092 | 60 | 0 | 0 | R 56 / U 5 (puro recto) |

Esto **reproduce** el hallazgo de Contreras (2026: 5 puros + KH0326 mixto). UR087 y UR092 son los dos puros-**recto**; UR087 es **el único de los seis con cuerdas superiores (13) y marcadores (5)**.

## 5. Resultados negativos (importantes)

1. **No se reproduce la aritmética simple**: "colgante = suma de subsidiarias" (p=0,90) y "cuerda superior = suma del grupo de 6" (solo p7=15 de 13; p=0,07 global) **NO se sostienen**. La aritmética es indexada/columnar, no jerárquica simple.
2. **UR087 no es inusualmente aritmético** para su tamaño: ninguna de las 5 familias de relación de suma sobrevive Holm (§4.2).
3. **No hay patrón periódico de color** (cuerda ni run): descarta un uso calendario por ciclos de color.
4. **No hay valores repetidos en posiciones cercanas** ni progresiones locales (p>0,36).
5. **No hay variación recto/verso DENTRO de UR087** (0 cuerdas V). La lectura de Medrano–Urton/FitzPatrick de un **marcador binario recto/verso que divide a los tributarios en moieties** no se puede verificar dentro de este quipu: aquí el binario opera **entre quipus** (UR087 recto vs. hermanos verso), no dentro.
6. `pendant_pendants_color_sum` (p=0,065) y `sum_top_cords` (p=0,029) son sugerentes pero **no sobreviven la corrección múltiple**.

## 6. Anomalías y posible información no numérica

- **49 cuerdas sin nudos** (13 % del total), incluidas las **4 cuerdas superiores LG** (p88, p95, p102, p109) y separadores LG/G0. Un "0 con nudos vacíos" no es un cero numérico → candidatos a **separadores o marcas cualitativas**.
- **5 marcadores** (cordeles de 1,5–2,5 cm atados al cordón principal, apuntando hacia "arriba", según nota OKR): señalización **no numérica**.
- Torsión Z en solo 4 cuerdas (p3, p4, p5, p282); **p282** es además de terminación **D** y sin nudos (doble anomalía).
- **p85** no tiene color registrado (`nan`).
- Notas de campo OKR: **nudo roto e ilegible** a 13 cm en el colgante 129; **fragmento de 7 cm atado con hilo** a la cuerda 112 ("los pesos y colores coinciden"); "cambia de color entre nudos" (cuerda 4) — posibles **daños de conservación**, no estructura.
- Las **subsidiarias** son casi todas `union=U` (desconocida) → su modo de fijación no está registrado y **no se puede usar** la distinción R/V en ellas.
- La dirección de nudo es abrumadoramente **Z** (323) con 40 S: un posible uso marcado/no marcado (Clindaniel 2019), pero **no lo cuantifiqué con nulo** en esta ronda.

## 7. Lectura más probable (con nivel de evidencia)

**Lectura propuesta: registro administrativo/censal con totales — consistente con la hipótesis de tributo/censo de la revisita de 1670.** Filas = los ~41 runs de 6 cordeles (unidades: personas/familias/ayllus), columnas = 6 categorías de una misma variable (la columna 3 sería la cantidad principal, p. ej. tributarios o tasas; las demás, conteos auxiliares); las **13 cuerdas superiores** llevarían sumas/comprobantes (indexadas por columna), y los separadores LG/G0 y los marcadores delimitan secciones.

Niveles de evidencia:

| Afirmación | Nivel |
|---|---|
| UR087 está organizado en grupos de 6 cordeles codificados por color (80,4 %; p=0,008 vs grandes) | **Demostrado** (en UR087) / **apoyado con datos** (familia Santa) |
| UR087 es puramente recto y posee 13 cuerdas superiores y 5 marcadores | **Demostrado** (campos directos OKR) |
| Existe aritmética interna exacta (sumas) en UR087 | **Demostrado** (KFG + verificación de p7) |
| Esa aritmética es **más** que lo esperado por su tamaño | **No apoyado** (Holm n.s.) |
| El quipu es un registro censal/de tributo (tipo revisita de 1670) | **Propuesto** |
| El emparejamiento numérico con el tributo (Medrano–Urton) | **No verificable** (documento de 1670 no abierto; Contreras 2026 tampoco lo reproduce) |
| Moieties por recto/verso **dentro** de UR087 | **No apoyado / negado** para este quipu |
| "Firma" de nombres por color | **Especulativo** |

## 8. Limitaciones

- El **documento de la revisita de 1670 no está abierto** (estado del arte §4.3): no puedo contrastar ningún total con la fuente, así que la lectura de "tributo" queda como propuesta.
- Los campos de unión de KFG (`union`) y OKR (`ATTACHMENT_TYPE`/`CORD_CLASSIFICATION`) **no coinciden**; usar solo KFG habría ocultado las 13 cuerdas superiores. Cualquier lectura de "recto/verso" debe decir de qué base sale.
- Los conteos de relaciones de suma de KFG son un rasgo **derivado** y sensible al tamaño; usarlos como prueba de "significado" es circular sin el control de tamaño de §4.2.
- No cuantifiqué con nulo (a) la dirección de nudo Z/S ni (b) la estructura "columnar" (suma de la misma posición entre filas), que es donde KFG sí ve señal (`indexed_pendant_sum`). **Recomendado para la siguiente ronda.**

---

## Para el coordinador

- **UR087 está organizado en ~41 "filas" de 6 cordeles del mismo color** (246 de 306 colgantes = 80,4 %), rasgo que es el **percentil 100 de los quipus grandes** (p=0,008) y que **comparten sus hermanos del Santa** (UR092 100 %, UR091 73 %). Esto **apoya con datos** la estructura que Medrano–Urton describen ("grupos de seis cordeles codificados por color"). Nivel: **demostrado en UR087**.
- **Descubrimiento operativo:** UR087 tiene **13 cuerdas superiores y 5 marcadores** que **KFG registra como `union=U` (no T)**. Cualquier pipeline basado solo en KFG pierde estos cordeles de resumen. Hay que cruzar con `CORD_CLASSIFICATION` de OKR. Nivel: **demostrado**.
- **La aritmética existe pero es indexada/columnar, no jerárquica.** Verificado a mano: `p7=15=1+1+10+1+1+1` (suma exacta del run anterior); `p47=16` = suma de la columna 0 de 7 runs; `p167=p192=p217=22` = suma de la columna 3 de dos runs. **"colgante = suma de subsidiarias" es FALSO aquí** (p=0,90). Nivel: **demostrado** (existencia) / la lectura semántica, **propuesta**.
- **El "muchas sumas" es en gran parte un artefacto de tamaño.** Tras controlar por nº de colgantes, ninguna de 5 familias de relación de suma es significativa (Holm: p ajustados ≥0,14). Es un **resultado negativo** que conviene comunicar para no sobreafirmar el "quipu aritmético".
- **UR087 es puramente recto (R=310, U=61, V=0).** Reproduzco a Contreras (2026): 5 quipus puros + UR090 mixto; UR087 y UR092 son los puros-recto. **Corolario importante:** la hipótesis de moiety por recto/verso **no se manifiesta dentro de UR087**; el binario actúa **entre quipus**. Nivel: **demostrado** (campos) / interpretación **propuesta**.
- **No hay periodicidad de color** (cuerda ni run; p≈1,0) → se descarta por ahora una lectura calendárica basada en ciclos de color. Tampoco hay valores repetidos ni progresiones locales (p>0,36). Nivel: **resultado negativo**.
- **Anomalías / no numérico:** 49 cuerdas sin nudos (incl. 4 cuerdas superiores LG vacías), 5 marcadores, 4 cuerdas Z (una, p282, con terminación D), p85 sin color, y notas OKR de **nudo roto ilegible** y **fragmento atado con hilo** (daño de conservación). Candidatos a información cualitativa o a pérdida de datos, no a cifras.
- **Lo que falta para cerrar el caso:** (1) el **documento de la revisita de 1670** (no abierto) para validar el emparejamiento; (2) un **nulo propio para la estructura columnar/indexada** y para la dirección de nudo Z/S, que es donde podría haber la señal "no numérica"; (3) repetir el pipeline en **UR088–UR092** para ver si los seis forman una serie (p. ej. totales por quipu = pachacas).
