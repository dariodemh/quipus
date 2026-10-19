# Ambigüedades de lectura: `valor` vs `alt`, nudos con dirección U y racimos rotos

**Equipo:** `t_alt` · **Fecha:** 2026-10-18
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `analisis/datos/quipus.csv`, `analisis/datos/grupos.csv`, `data/external/open-khipu-repository/data/khipu.db` (OKR, 619 quipus).
**Scripts (en esta carpeta, ejecutables en orden):** `e1_panorama.py`, `e2_consistencia.py`, `e3b_kfg_vs_okr_dfs.py`, `e4_marcadores.py`, `e5b_difflib.py`, `e6_direccion.py`, `e7_sumas.py`, `e8_tolerancia.py`, `e9_intervalos.py`, `e10_propagacion.py`, `e11_tolerancia_restringida.py`, `e12_cierre.py`, `e13_propagacion_final.py` (esta última es la que produce la tabla de §3.7). Semilla fija `20261018`.

---

## 1. Pregunta

1. ¿Cuánta **incertidumbre de transcripción** hay en el corpus y **dónde** está?
2. ¿Cuánto puede cambiar una **suma típica** por esa incertidumbre?
3. ¿Qué **tolerancia** deberían usar los equipos que buscan relaciones de suma?

---

## 2. Método

Unidad de análisis: el **quipu** (regla 1 del brief). Todo contraste entre cuerdas usa nulo por **permutación dentro de quipu**.

La columna `alt` resultó estar vacía (§3.1), así que la incertidumbre se estima por tres vías independientes y complementarias:

| Vía | Qué mide | Fuente |
|---|---|---|
| **A. Marcadores internos** | Autodeclaración de duda en la propia transcripción KFG | `nudos` de `cuerdas.csv` |
| **B. Doble transcripción** | Desacuerdo *empírico* entre dos bases independientes del mismo objeto | KFG vs OKR (`khipu.db`) |
| **C. Intervalos de convención** | Cota superior si cambia el criterio Ascher (tipo por posición) ↔ Urton (tipo por nudo) | reglas explícitas §3.6 |

Emparejamiento KFG↔OKR: 651 quipus KFG contra `khipu_main.OKR_NUM` → 593 pares; se conservan los **566 con el mismo número de cuerdas** (48 461 cuerdas emparejadas). El orden de cuerdas se reconstruye en OKR con un DFS sobre `PENDANT_FROM` (los hijos ordenados por `CORD_ID`, que sigue el orden de transcripción) y se alinea con `orden` de KFG. Alineación final con `difflib` sobre la secuencia de valores (48 565 posiciones), que separa **sustitución de valor** de **inserción/borrado estructural**.

---

## 3. Resultados

### 3.1 `alt` está vacía en el 100 % de los registros — DEMOSTRADO

**57 818 / 57 818** cuerdas tienen `alt` vacía. Comprobado con `dtype=str` y `keep_default_na=False` (`e1_panorama.py`), para descartar que fuese un problema de lectura del CSV.

> Consecuencia: la incertidumbre de transcripción **no se puede medir con `alt`**. Cualquier equipo que haya previsto usar `alt` como cota de error no tiene de dónde sacarla. Hay que reconstruirla (§3.2–3.6).

### 3.2 `valor` es una reducción mecánica de `nudos` — DEMOSTRADO

En las 40 121 cuerdas con nudos, aportes completos y valor numérico, `valor` coincide **exactamente** con la suma de los aportes de sus racimos: **40 121 / 40 121 (100,00 %)**; discrepancia máxima 0 (`e2_consistencia.py`).

`valor` no es una lectura independiente: es `Σ aporte`. Por tanto **toda** la ambigüedad posible vive en la cadena `nudos` (tipo de nudo, número de vueltas, lugar decimal, racimo ausente), no en una segunda codificación.

### 3.3 Marcadores internos de duda (vía A) — APOYADO CON DATOS

Sobre 64 490 racimos en 40 162 cuerdas con nudos (`e4_marcadores.py`):

| Marcador | Racimos | % racimos | Cuerdas | % cuerdas | Quipus |
|---|---|---|---|---|---|
| Dirección **U** (desconocida) | 8 541 | 13,24 % | 5 820 | 14,49 % | — |
| … cuerdas **100 % U** | — | — | 5 611 | 13,97 % | — |
| Tipo de nudo **raro** (U, SP, TF, EE, LL, BL, `?`) | 704 | 1,09 % | 567 | 0,98 % | 100 |
| Aporte **ausente** (no se sabe cuánto vale el racimo) | 65 | 0,10 % | — | — | — |
| Racimo **no parseable** (cadena mal formada) | 23 | 0,04 % | 23 | 0,06 % | 3 |
| **Defecto duro** (aporte ausente/no parseable, S con n>9, S con aporte no decimal) | 150 | 0,23 % | **111** | **0,19 %** | 54 |
| **Niveles decimales no decrecientes** (arriba→abajo) | — | — | 3 362 | 8,37 % | — |
| … nivel decimal **duplicado** | — | — | 3 193 | 7,95 % | — |
| **L de 1 vuelta** (indistinguible de un S) | 23 | 0,04 % | — | — | — |
| L de ≥10 vueltas / S con n>9 | 363 / 23 | — | — | — | — |
| Nota de **rotura** (`broken`, `missing`, `fragment`…) | — | — | 322 | 0,56 % | 110 |

**Dos hallazgos negativos importantes dentro de esta tabla:**

- Las **irregularidades de nivel decimal no cambian el valor**. Como `valor = Σ aporte` es una suma, el orden de los racimos es irrelevante: un nivel "fuera de orden" o duplicado da exactamente el mismo total. Comprobado: las 3 362 cuerdas con niveles no decrecientes tienen el mismo `valor` bajo cualquier reordenación. **No son incertidumbre de valor.**
- Una **L de 1 vuelta vale 1 igual que un S de unidades**: tampoco cambia el valor (23 casos, 0,04 %).

La dirección **U** es un marcador **sistemático de fuente**, no de duda individual: el 92,5 % de los racimos del prefijo **AS** son U, frente al 10,6 % de KH, 1,5 % de UR, 1,4 % de HP, 0,5 % de QU, 0,1 % de MM y 0,0 % de JC. La colección AS simplemente **no registró la dirección**.

### 3.4 Contraste KFG ↔ OKR: la única medida empírica de desacuerdo — APOYADO CON DATOS

566 quipus, 48 565 cuerdas alineadas (`e3b`, `e5b`):

| Clase | Cuerdas | % |
|---|---|---|
| Alineadas con **valor idéntico** | 48 240 | **99,33 %** |
| Alineadas con **valor distinto** | 109 | **0,22 %** |
| **Inserción/borrado** (estructura: una cuerda que una base tiene y la otra no, o en otro sitio) | 208 | 0,43 % |

- **548 / 566 quipus (96,8 %)** son idénticos cuerda a cuerda: **sólo 10 quipus tienen algún desacuerdo de valor** y en ellos están los 109.
- **79 % de los desacuerdos de valor (86/109) están en sólo dos quipus: UR090 (50) y UR235 (36)**, con desplazamientos sistemáticos de 90/180/270 unidades (múltiplos de 90): es un problema **estructural de una de las dos transcripciones**, no ruido repartido.
- Fuera de esos dos quipus quedan **23 desacuerdos en 48 465 cuerdas = 0,047 %**; de ellos 12 son de **≤4 unidades** (mediana 3) y 4 son >100. Es la clase "errata ordinaria".
- **22 de los 109 desacuerdos son factor 10 exacto** (y 2 son factor 1/10): el error dominante es de **lugar decimal**, no de número de vueltas.

**Dónde está la incertidumbre, en una frase:** no está repartida; está en **2–10 quipus con problemas sistemáticos** (UR090, UR235, UR144, HP004, UR193, AS072…) y, fuera de ellos, en ~0,05 % de las cuerdas con erratas de 1–4 unidades o de un lugar decimal.

### 3.5 La dirección U **no** predice error de valor — RESULTADO NEGATIVO

- Entre los 109 pares alineados que discrepan, sólo **6 (5,5 %)** tienen algún nudo U, frente a una **base del 10,2 %** de cuerdas con U. Es decir, los nudos U están **ligeramente subrepresentados** entre los errores, no sobrerrepresentados.
- Contraste exploratorio previo (todas las cuerdas, sin separar los quipus estructurales): 0,91 % de desacuerdo en cuerdas con U vs 0,56 % sin U; diferencia 0,35 pp, **p permutación = 0,012** (2 colas, 2 000 permutaciones dentro de quipu); **Holm sobre 3 pruebas exploratorias (U, fuente, tamaño) = 0,036**. Pero **desaparece al quitar los quipus estructurales** (§3.4), así que lo clasifico como **artefacto de 2 quipus, no robusto**.

- **Validación cruzada de la propia marca U**: de 4 733 cuerdas que KFG marca 100 % U, OKR también las marca 100 % U en **4 721** casos; sólo **10 cuerdas (0,03 %)** tienen U en KFG y dirección conocida en OKR, y **0** al contrario. La marca U es **reproducible entre transcriptores**: es una propiedad del registro de campo, no una duda.

### 3.6 La diferencia de convención Ascher/Urton **no** explica los desacuerdos — RESULTADO NEGATIVO

La literatura advierte que Ascher asigna el tipo de nudo **por posición** y Urton **por tipo de nudo** (Thompson 2026), lo que en teoría puede mover un nudo un lugar decimal. Construí el **intervalo de valores alternativos** bajo esa convención (reglas A1–A3 en `e9_intervalos.py`): un L/E/raro que no es el último racimo se lee en el lugar que le da su posición.

- **3 210 cuerdas (7,99 %)** cambian de valor bajo esa convención alternativa; el cambio mediano es **×6** (p25 ×2,8; p75 ×32).
- **Pero sólo 5 de 267 (1,9 %) de los desacuerdos reales KFG↔OKR caen dentro de ese intervalo.** Es decir: la diferencia de convención **no es lo que está produciendo los desacuerdos observados**. Es un riesgo teórico real (y hay que fijar la convención), pero **no** la fuente del ruido medido. **Cota superior si esa convención estuviera operando:** una suma de 5 cuerdas cambiaría en el **34 %** de los casos (p90 del cambio relativo 273 %), de modo que las relaciones de suma serían inestables en un tercio del corpus (`e10_propagacion.py`).

### 3.7 Propagación a sumas: ¿cuánto cambia una suma típica? (vía B)

Modelo M1 (empírico): cada cuerda hija se corrompe con probabilidad *p* = tasa de desacuerdo KFG↔OKR y el error es multiplicativo, con razón muestreada (simetrizada) de los desacuerdos observados. Se parte de **grupos reales** de colgantes (5 614 grupos; suma mediana 60, p25 10, p75 340). 30 000 sorteos por celda.

| k hijas | val. | p = 0,22 % (todas): P(suma cambia) | cambio rel. mediano *si* cambia | p90 rel. | cambio abs. mediano | p = 0,047 % (sin UR090/UR235): P(cambia) |
|---|---|---|---|---|---|---|
| 2 | 24 066 | 0,44 % | 66,5 % | 606 % | 15 | 0,10 % |
| 3 | 22 318 | 0,70 % | 32,0 % | 402 % | 9 | 0,16 % |
| 5 | 15 827 | 0,94 % | 17,8 % | 283 % | 11 | 0,23 % |
| 8 | 7 590 | 2,06 % | 7,5 % | 105 % | 8 | 0,26 % |
| 10 | 4 887 | 2,03 % | 8,3 % | 111 % | 9 | 0,47 % |

*(`val.` = simulaciones válidas, es decir, grupos con ≥k cuerdas y suma>0.)*

**Lectura:** la incertidumbre es **rara y de cola gruesa**. En **99,1 %** de las sumas de 5 cuerdas el valor es **exactamente el mismo** entre las dos transcripciones; cuando cambia, cambia mucho (mediana 17,8 %, p90 283 %) porque el error típico es de un **lugar decimal** o un desplazamiento sistemático. **No es un ruido difuso de ±2 %**: es "nada o un factor".

### 3.8 Calibración de tolerancia: el problema no es el ruido, es la multiplicidad

Dos espacios de búsqueda, ambos con nulo por permutación de valores **dentro del quipu** (100–200 repeticiones), `e8_tolerancia.py` y `e11_tolerancia_restringida.py`.

**(a) Espacio permisivo** (cualquier tramo contiguo de ≥2 colgantes de un grupo contra cualquier colgante del quipu): 48,3 millones de comparaciones, **74 243 candidatas por quipu**.

| Tolerancia T | Aciertos obs. | Aciertos nulo | Exceso | **Falsos positivos esperados / quipu** |
|---|---|---|---|---|
| 0 (exacto) | 0,96 % | 0,89 % | +0,07 pp | **663** |
| 0,5 % | 0,97 % | 0,90 % | +0,07 pp | 670 |
| 2 % | 1,03 % | 0,97 % | +0,07 pp | 717 |
| 5 % | 1,23 % | 1,16 % | +0,06 pp | 863 |
| 10 % | 1,66 % | 1,59 % | +0,07 pp | 1 180 |

**(b) Espacio realista** (la "cuerda suma" es un colgante del grupo y la suma un tramo de ≥2 *otros* colgantes del mismo grupo): 6,98 millones de comparaciones, **1 599 candidatas por grupo**.

| Tolerancia T | Aciertos obs. | Aciertos nulo (sd) | Exceso | FP esp. / grupo | obs/nulo |
|---|---|---|---|---|---|
| 0 (exacto) | 0,50 % | 0,43 % (0,01) | +0,06 pp | 6,9 | **1,14** |
| 0,5 % | 0,50 % | 0,44 % | +0,06 pp | 7,1 | 1,14 |
| 1 % | 0,52 % | 0,46 % | +0,07 pp | 7,3 | 1,15 |
| 2 % | 0,57 % | 0,49 % | +0,08 pp | 7,9 | 1,16 |
| 5 % | 0,72 % | 0,64 % | +0,08 pp | 10,2 | 1,13 |
| 10 % | 1,08 % | 0,96 % | +0,13 pp | 15,3 | 1,13 |

**La relación señal/ruido es plana (≈1,14) en toda la rejilla.** Ampliar la tolerancia del 0 al 10 % **multiplica por 1,7 los aciertos observados… y por 1,7 los del nulo**. En este corpus, una tolerancia relativa **no compra señal: compra falsos positivos al mismo ritmo**. Y a T=0 ya hay ~7 coincidencias exactas por grupo atribuibles al azar (los valores son enteros pequeños: coincidir exacto es barato).

### 3.9 Tolerancia recomendada

Con los datos de §3.7 y §3.8:

- **Para el ruido de transcripción: T = 0 (exacto).** El ruido deja intactas el 99,1–99,9 % de las sumas; una tolerancia no recupera relaciones verdaderas, porque las que fallan fallan por un factor, no por un margen.
- Si se quiere un margen de seguridad, **±1 unidad absoluta (o ±0,1 % relativo), nunca ±5 %**. Por encima de 1 % sólo se acumulan coincidencias por azar.
- **La multiplicidad es el verdadero enemigo**: con 1 599 candidatas por grupo y 7 FP esperadas a T=0, cualquier hallazgo debe reportar (i) el espacio de búsqueda declarado *a priori*, (ii) el número de candidatas, y (iii) un p-valor por permutación **por quipu o por grupo**, no una tolerancia global.
- **Antes de ampliar tolerancias, hay que arreglar los datos**: 111 cuerdas con defecto duro (54 quipus), 567 cuerdas con tipo raro (100 quipus) y los 2–10 quipus estructuralmente mal alineados (UR090, UR235, UR144, HP004…) son la fuente real de error, y son auditables a mano.

---

## 4. Controles

| Control | Resultado |
|---|---|
| **Nulo explícito** | Permutación de valores **dentro de cada quipu** (preserva tamaño, distribución de valores y composición del quipu). 100–200 repeticiones por celda. |
| **p-valor empírico** | Contraste U→desacuerdo: p = 0,012 (2 colas, 2 000 permutaciones dentro de quipu). |
| **Corrección múltiple** | Holm sobre 3 pruebas exploratorias (U, fuente, tamaño del valor) → **0,036**. Se reporta, pero el efecto **no sobrevive** al quitar los quipus estructurales (§3.5). |
| **Independencia de la medición** | El desacuerdo KFG↔OKR no se mide sobre el mismo campo: son bases distintas con transcriptores distintos (`CREATED_BY`: katie, gurton, julia, cbrezine…). |
| **Alineamiento** | Sin separar inserciones/borrados, el desacuerdo bruto sería 0,60 %; con `difflib` baja a 0,22 %, y el 0,43 % restante es **estructural**. Sin este paso se sobreestima el ruido por 3. |
| **Cota superior** | El intervalo de convención (§3.6) da el peor caso: 8 % de cuerdas, factor 6 mediano. |
| **Chequeo de la marca U contra un segundo transcriptor** | 4 721/4 733 concordancias exactas (§3.5). |
| **Sesgo del corpus** | 85 de los 651 quipus KFG (13 %) no son comparables con OKR (sin KH o con distinto número de cuerdas): la tasa de desacuerdo **no está medida en ese 13 %**. |

---

## 5. Resultados negativos (explícitos)

1. **`alt` no contiene información**: vacía en el 100 % de las filas. No sirve como cota de error.
2. **La dirección U no aumenta el riesgo de error de valor** (5,5 % en errores vs 10,2 % base; y el contraste global desaparece al limpiar 2 quipus).
3. **Las irregularidades de nivel decimal (8,37 % de las cuerdas) no cambian el valor**: la suma es invariante al orden de los racimos.
4. **Una L de 1 vuelta no es una ambigüedad de valor** (vale 1 igual que un S de unidades).
5. **La diferencia de convención Ascher/Urton no explica los desacuerdos observados** (1,9 % de cobertura).
6. **No hay relación madre = suma de hijas** por encima del azar: 669 relaciones con ≥2 hijas, 10 exactas (1,49 %) y el nulo da 1,49 %. No hay señal en esa formulación.
7. **Ampliar la tolerancia no mejora la relación señal/ruido** (obs/nulo ≈ 1,14 constante de 0 a 10 %).

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| `alt` vacía en el 100 %; `valor` = Σ aportes en el 100 % | **demostrado** |
| Marcadores internos (U 13,2 %; tipos raros 1,09 %; defectos duros 0,19 %; roturas 0,56 %) | **demostrado** (conteo directo) |
| U se concentra por fuente (AS 92,5 % vs JC 0 %) y es reproducible entre transcriptores | **demostrado** |
| Desacuerdo de valor entre transcripciones = 0,22 % de las cuerdas; 99,33 % idénticas; 96,8 % de los quipus idénticos | **apoyado con datos** (2 bases, pero probablemente misma fuente de campo: es una **cota inferior** del error real de lectura) |
| El desacuerdo se concentra en 2–10 quipus | **apoyado con datos** |
| El error dominante es de lugar decimal (22 % factor 10) | **apoyado con datos** |
| Una suma de 5 cuerdas queda intacta en ~99,1 % de los casos; si cambia, cambia un factor | **apoyado con datos** (modelo calibrado, no medición directa de la misma suma en dos bases) |
| La tolerancia óptima es 0 y ampliarla sólo añade falsos positivos | **apoyado con datos** |
| El intervalo de convención (8 % de cuerdas, factor 6) es una cota superior del riesgo | **propuesto** (reglas A1–A3 son una interpretación; no validada por los datos: cubre sólo 1,9 %) |
| Que las cuerdas rotas/no codificadas expliquen parte del 0,43 % estructural | **especulativo** (no hay campo de rotura en OKR que permita comprobarlo) |

---

## 7. Para la siguiente ronda

1. **Auditar a mano UR090 y UR235** (86 de los 109 desacuerdos). Son 226 + 194 = 420 cuerdas; resolverlos bajaría el desacuerdo a ~0,05 %.
2. **Comparar contra una tercera transcripción** (databook de Ascher, ya en el repo vía `papers/`/`fuentes_txt`): las dos bases comparadas aquí comparten probablemente el registro de campo de Urton, y por eso 99,33 % puede ser una cota inferior.
3. **Fijar por escrito la convención S/L** (Ascher por posición vs Urton por tipo) antes de buscar sumas: es el único factor que puede mover valores un orden de magnitud, y no es detectable desde los datos.
4. **Publicar la lista de 111 cuerdas con defecto duro** como "no usar en tests de suma".

---

## 8. Para el coordinador

- **`alt` está vacía en las 57 818 cuerdas (100 %).** No hay segunda lectura en los datos; la incertidumbre hay que reconstruirla. Que ningún equipo cuente con `alt`.
- **`valor` no es una lectura: es la suma de los aportes de `nudos`, exacta en el 100 % de los casos.** Toda la ambigüedad está en la cadena `nudos`.
- **La incertidumbre real de valor es pequeña y está concentrada:** comparando KFG con la base OKR (566 quipus, 48 565 cuerdas), el **99,33 %** de las cuerdas tiene el mismo valor; 548 de 566 quipus son idénticos. Sólo **0,22 %** de las cuerdas discrepa, y **el 79 % de esos desacuerdos está en 2 quipus (UR090, UR235)**. Fuera de ellos el desacuerdo es **0,047 %**.
- **El error típico es de lugar decimal, no de vueltas:** 22 de los 109 desacuerdos son factor 10 exacto. El resto de la clase "ordinaria" es de 1–4 unidades.
- **La dirección U (13,2 % de los racimos) no es incertidumbre de valor:** es una marca sistemática de la colección AS (92,5 % de sus racimos son U) y es **perfectamente reproducible** entre transcriptores (4 721/4 733). Además **no está sobrerrepresentada entre los errores** (5,5 % vs 10,2 % base). No hay que corregirla ni preocuparse por ella en análisis de sumas.
- **Las "irregularidades" de nivel decimal (8,4 % de las cuerdas) no cambian el valor**: la suma es invariante al orden de los racimos. No son un problema de valor.
- **Cuánto cambia una suma típica:** con el error empírico, una suma de 5 cuerdas queda **exactamente igual en el 99,1 %** de los casos; cuando cambia, cambia mucho (mediana 17,8 %, p90 283 %). **Es "nada o un factor", no un ±2 %.**
- **Tolerancia recomendada: 0 (exacta) o ±1 unidad; nunca ±5 %.** En el espacio realista de búsqueda, la relación señal/nulo es plana (≈1,14) de 0 a 10 % de tolerancia: ampliarla multiplica aciertos y falsos positivos **por igual** (7 → 15 FP por grupo).
- **El enemigo no es el redondeo, es la multiplicidad:** 1 599 candidatas por grupo y ~7 coincidencias exactas por azar. Cualquier equipo que busque sumas debe declarar el espacio *a priori* y dar p-valor por permutación por grupo, no una tolerancia global.
- **Acción concreta y barata:** auditar a mano UR090 y UR235 (420 cuerdas) y marcar como "no usar" las 111 cuerdas con defecto duro (54 quipus) y las 567 con tipo de nudo raro (100 quipus). Con eso el corpus queda limpio para búsqueda de sumas a tolerancia 0.
