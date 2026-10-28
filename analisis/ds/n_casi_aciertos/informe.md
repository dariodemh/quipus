# Modelo de error para los casi-aciertos de Incahuasi

**Carpeta:** `analisis/ds/n_casi_aciertos/` · **Fecha:** 2026-10-18 · **Semilla:** 20261018
**Datos:** `analisis/datos/cuerdas.csv`, `khipu.db` (OKR), los 13 quipus del sistema (`UR270, UR273A/B, UR274A/B, UR278, UR266, UR275, UR269, UR267A/B, UR255, UR256`), `13_sistema_incahuasi/` y `19_prediccion/`.
**Scripts (en este orden):** `01_catalogo.py` → `02_relaciones.py` → `04_nulo.py` → `03_reparaciones.py` → `06_clasificacion.py` → `07_stats.py`.
**Entregables:** `informe.md`, `reparaciones.csv` (282 candidatas; 31 recomendadas, una por relación reparable), `resumen_relaciones.csv` (44 casi-aciertos clasificados), `catalogo_tipos.csv`, `nulo_ediciones.csv`.

---

## 1. Pregunta

Los quipus del sistema de Incahuasi tienen decenas de relaciones aritméticas que fallan **por poco** (+1, +6, +10, +24, +100…). ¿Son errores de lectura/transcripción reparables con **una** operación sobre la cadena `nudos`, o son discrepancias reales del sistema? ¿Cuáles se pueden señalar para revisar en el museo, y cuáles no?

---

## 2. Método

### 2.1 Catálogo empírico de errores (01)

Se comparó KFG con OKR racimo a racimo, en las **35 223** cuerdas con nudos, valor > 0 y largo coincidente (±0,5 cm). Cada discrepancia de valor se alineó con `difflib` sobre la secuencia de aportes de los racimos y se clasificó en: factor 10 de posición, ±vueltas de nudo largo, figura de ocho ↔ largo, S ↔ L, racimo omitido/duplicado, conteo simple ±1, u "otro/compuesto" si hacía falta más de una operación. Como fuente secundaria se usó la auditoría KFG vs *Databook* (`ds/n_databook/`, 311 discrepancias en 210 quipus AS).

### 2.2 Motor de ediciones de una operación (03)

Para cada casi-acierto se enumeraron **todas** las ediciones de un solo racimo/nudo que convierten la relación en exacta:
eliminar el racimo (−v), duplicarlo (+v), moverlo un lugar decimal (±9v), cambiar las vueltas de un largo (±1), cambiar el conteo de un simple (±1), leer un S como L o al revés, leer un E como L(k) o al revés, o insertar un racimo ausente (m simples en 10^p, un L de k vueltas, un E).
Se impusieron límites físicos: vueltas y conteos entre 1 y 9; el factor 10 hacia abajo solo si el valor es divisible por 10. Cada edición se aplicó de verdad a la cadena y se verificó que la suma de la cadena propuesta fuera exactamente la observada + δ. La cadena propuesta se entrega en `nudos_propuesto`.

Se exploraron **los dos lados** de cada relación: las cuerdas del detalle y la(s) cuerda(s) del libro (cuando existe una copia identificable). El signo de la edición se invierte si se edita el objetivo.

Cada candidata lleva:
- `probabilidad`: tasa empírica del tipo de error por cuerda en el catálogo (modelo "resto", sin los 5 quipus que concentran el 86 % de las discrepancias).
- `p_nulo`: fracción de cuerdas de quipus **no relacionados**, con el mismo número de racimos, que admiten una edición del mismo tipo con el mismo δ (nulo geométrico, 04).

### 2.3 Relaciones incluidas (02)

44 relaciones con residual ≠ 0:
- **R1** 7 filas de UR278 (total de 9 celdas) frente a la cabecera del libro.
- **R2** 8 celdas de UR278 frente a colgante + subsidiaria 1 de UR270.
- **R3** 10 registros de UR273A + UR273B (de 18; 8 exactos).
- **R4** 10 registros de UR274A + UR273B (de 17; 7 exactos).
- **R5** 9 cuerdas únicas (cuotas 47/17 y copias).

35 tienen destino identificable; **9 no lo tienen** (no son verificables con el archivo conservado).

### 2.4 Nulo y comparaciones múltiples

- **Nulo por edición:** para cada δ, se calculó q(δ) = fracción de cuerdas aleatorias no relacionadas que admiten *alguna* edición con ese δ exacto (`nulo_ediciones.csv`). La probabilidad de que una relación de k cuerdas sea reparable por azar es 1−(1−q)^k.
- **Nulo agregado:** 31 de 35 relaciones son reparables; el nulo geométrico predice 28,3 (p binomial aproximado = 0,177; **no corrige la dependencia** entre relaciones que comparten cuerdas). Es decir: **la mera reparabilidad no es evidencia**.
- **Comparaciones múltiples:** hay 35 contrastes de "¿es error de lectura?". Con Holm, el umbral para el más pequeño sería 0,05/35 = 0,0014. Ningún caso individual llega a ese umbral por sí solo; los argumentos son estructurales (especificidad, repetición, plantilla), no p-valores aislados.
- Los patrones repetidos (columna 1; cuotas 10) se contrastaron con binomial/hipergeométrico y se declaran como **sugerentes**, no significativos tras corrección.

### 2.5 Límites

KFG y OKR **no son lecturas independientes** para los UR: ambas proceden del archivo de Urton. El catálogo mide, sobre todo, **fidelidad de transcripción entre dos codificaciones de la misma lectura**, no error de lectura física. Además, los errores que no cambian el valor (E ↔ L1, S1 ↔ L1 en unidades) son invisibles en este catálogo. Por tanto, las tasas son una **cota inferior**.

---

## 3. Resultados

### 3.1 Catálogo: qué tipos de error existen y a qué tasa

**225 discrepancias / 35 223 cuerdas comparables = 0,64 %** (IC95 % aprox. 0,56–0,72). El 86 % se concentra en 5 quipus (UR090, UR144, UR235, UR193, UR190).

| Tipo | n | % de discrepancias | por 1000 cuerdas (global) | n en el "resto" | por 1000 cuerdas (resto) |
|---|---:|---:|---:|---:|---:|
| factor 10 de posición | 106 | 47,1 | 3,01 | 3 | 0,086 |
| ±vueltas de nudo largo | 58 | 25,8 | 1,65 | 9 | 0,259 |
| compuesto (≥2 operaciones) | 21 | 9,3 | 0,60 | 0 | 0,000 |
| bloque (estructura de racimos distinta) | 21 | 9,3 | 0,60 | 7 | 0,202 |
| racimo omitido (OKR tiene más) | 10 | 4,4 | 0,28 | 9 | 0,259 |
| E ↔ L | 4 | 1,8 | 0,11 | 2 | 0,058 |
| racimo omitido (KFG tiene más) | 2 | 0,9 | 0,06 | 2 | 0,058 |
| S ↔ L | 1 | 0,4 | 0,03 | 1 | 0,029 |
| otro | 1 | 0,4 | 0,03 | 1 | 0,029 |

Lectura:
- **El error dominante es de un dígito de posición** (factor 10), pero es un fenómeno de 3 quipus (UR090, UR235, UR144): en el resto del corpus casi no aparece (0,086/1000).
- **El segundo es la cuenta de vueltas de un nudo largo** (0,26/1000 cuerdas; 0,41/1000 cuerdas con L).
- **La omisión de un racimo entero es rara** (0,26/1000) pero existe y está atestiguada (Δ = +80, +90 en KH0058/UR044).
- **E ↔ L y S ↔ L son raros** (0,06 y 0,03/1000) y casi siempre mueven el valor en 1–3, no en 10.
- En el *Databook*: 31 convenciones ×10, 45 valores impresos que no cuadran con sus propios nudos (erratas de 1–8), 14 OCR evidentes, 128 cuerdas que KFG dejó sin nudos y 70 valores marcados `?`. Confirma que **las erratas pequeñas de transcripción existen**, pero son de valor, no de racimo.

**Tasa base que usa el modelo:** 0,10 % de cuerdas con error de valor en el "resto"; por tipo, 8,6·10⁻⁵ (factor 10), 2,6·10⁻⁴ (vueltas), 2,6·10⁻⁴ (omisión), 5,8·10⁻⁵ (E/L), 2,9·10⁻⁵ (S/L).

### 3.2 Panorama de reparaciones

- **31 de 35** relaciones con destino son reparables con **una** edición (88,6 %).
- La mediana es **4 candidatas por relación** (media 8,1; máximo 43). Las filas de 9 cuerdas son las más inespecíficas (21–43 candidatas); las cuotas y las celdas, las más específicas (1–4).
- **La probabilidad del catálogo es minúscula para cualquier candidata individual** (10⁻⁵–10⁻⁴). Lo que discrimina no es que haya reparación, sino **cuántas** hay, **de qué tipo**, y si **repite un patrón**.

### 3.3 Los casos de la lista

| Caso | δ | Reparación de una edición | Veredicto |
|---|---:|---|---|
| UR278 g12 | +100 | 5S→6S (o 6S→5S en el libro) en el racimo de centenas | **Discrepancia entre copias** |
| UR278 g4 | +24 | **ninguna** | **Discrepancia real/compuesta** |
| UR278 g8 | +6 | **insertar un 6L en p77**, la única de las 9 celdas sin nudo de unidades | **Error de lectura plausible** |
| UR278 g13 | +1 | ±1 vuelta en una de 9 cuerdas (40 candidatas) | Ambiguo |
| UR278 g17 | −1 | ±1 vuelta (18 candidatas) | Ambiguo |
| UR278 g19 | +1 | ±1 vuelta (43 candidatas) | Ambiguo |
| UR278 g21 | −1 | **p180: 7L→6L** (resuelve también la celda) | **Error de lectura plausible** |
| UR278 col1 (g21, g25) | +1, +1 | p180 7L→6L; p196 tiene 2E donde el detalle tiene 1E | **Patrón sistemático (sugerente)** |
| UR273 A+B | +10, ±1, ±10, +1000 | conteo simple en decenas/centenas/millares; 7 con destino | 3 plausibles, 4 ambiguos |
| UR275 p51 | +7 | falta un **7L** al final (como en las otras 24 cuotas) | **Error de lectura plausible** |
| UR274B p9/p13/p19/p64 | +7 | falta el **7L** terminal; las 4 son las más cortas | **Estructural sistemático** |

#### (a) UR278 g12: +100 es una escalera de copias, no una errata

Las tres copias del mismo registro dan:

| Quipu | Racimo de centenas | Valor |
|---|---|---|
| UR269 p181 | `4S,400` | 2433 |
| UR278 fila g12 | `5S,500` (implícito) | 2533 |
| UR266 p64 | `6S,600` | 2633 |
| UR275 p41 | `6S,600` | 2633 |

No es un nudo mal leído en un solo sitio: es una **diferencia de 4/5/6 nudos simples entre objetos**. Los dos libros (UR266 y UR275) coinciden entre sí; UR278 y UR269 discrepan cada uno por 100. La explicación aburrida es que las copias no son idénticas (el escriba ató 4, 5 o 6 nudos) o que una de las lecturas contó mal el racimo. **No se puede resolver sin contar los nudos físicos** de UR266 p64, UR275 p41, UR269 p181 y la fila g12 de UR278 (p109–p117).

#### (b) UR278 g4: +24 no admite ninguna edición de un nudo

24 no es un valor de racimo posible (los racimos valen m·10^p o k vueltas), no es 9·v, y no hay ningún nudo de 24 en las cadenas. Se necesitan **al menos dos operaciones** (p. ej. +20 y +4) o una cuerda ausente. Es el caso más claro de **discrepancia real o error compuesto**.

#### (c) UR278 g21 y la primera columna: el caso más limpio

UR278 p180 = `2S(4.0),200; 3S(10.0),30; 7L(19.0),7; 1E(24.0),1` = 238.

- La celda de UR278 (238) excede en 1 a colgante+subsidiaria de UR270 (178+59 = 237).
- La fila g21 suma 1654, y el libro dice 1653.

**Una sola edición —7L→6L en p180— hace exactas las dos comprobaciones a la vez.** Es la candidata mejor sostenida de todo el conjunto: la misma corrección reconcilia el detalle (UR270) y el total (UR266/UR275). Recomendación: contar las vueltas del nudo largo de UR278 p180 (¿6 o 7?).

La otra fila 9/9 (g25) tiene el mismo +1 en la columna 1, pero el mecanismo es distinto: su celda UR278 p196 = `3S,300; 1E,1; 1E,1` tiene **dos figuras de ocho** donde el detalle tiene una. El patrón "columna 1 vale +1 en las dos filas 9/9" se repite (2/2), pero con mecanismos distintos; si la columna fuera aleatoria, P(las dos en la misma columna) = 1/9 = 0,11 (no significativo). Queda como **sugerente**.

#### (d) UR273 A+B: 10/18 no exactas, casi todas de un dígito

De las 18 sumas A+B, 8 son exactas y 10 no. De las 10, **7 tienen destino identificable** y sus residuales son +10, −10, −1, −1, −10, +1000, +1000; las otras 3 (2597, 1159, 1696) **no aparecen en el libro conservado** y no son verificables.

- Las de ±1 y ±10 se reparan con un conteo simple (±1 nudo en decenas) o ±1 vuelta: tipos atestiguados.
- Las de +1000 exigen añadir un nudo de mil (1S→2S en el racimo de millares): es una operación, pero un salto de 1000 en una suma de ~2000 es una edición grande; las clasifico como ambiguas.
- **Ojo con reg18/reg19:** ambas sumas dan 1887 y ambas apuntan a la **misma** cabecera UR269 p171 = 1886. No pueden ser dos registros distintos del mismo libro; lo más probable es que una sea un **duplicado de alineamiento**. Una sola edición en p171 (6L→7L) "resolvería" las dos, pero eso es un artefacto de la duplicación, no evidencia doble.

#### (e) UR275 p51 = 40 vs 47: falta el 7L terminal

p51 = `4S(18.5),40`, sin nudo de unidades. Las otras **24** cuotas de UR275 son `4S(14–17),40; 7L(18–24),7`. La p51 mide 26,5 cm (mediana de las otras: 41,8). Insertar un 7L al final la convierte en 47. La probabilidad de al menos una omisión de racimo en 25 cuerdas es 0,65 % — baja pero no despreciable. Es, junto con p77, el **mejor candidato individual a error de transcripción** después de p180. Revisar la punta de p51.

#### (f) UR274B: las cuotas "10" no son erratas aleatorias

19 cuotas: **12 valen 17** (`1S,10;7L,7`), **4 valen 10** (`1S,10`, sin 7L) y 3 tienen otro valor. Las 4 de valor 10 son **exactamente las 4 más cortas** de las 16 que valen 10 o 17 (20,5–25,0 cm frente a un mínimo de 24,5 cm en las de 17). Si la omisión fuera aleatoria:

- P(≥4 omisiones en 16 cuerdas | 2,6·10⁻⁴) ≈ 8·10⁻¹².
- P(que las 4 más cortas sean justo las 4 de 10) = 1/C(16,4) = 5,5·10⁻⁴.

Conclusión: **no es un error de lectura aleatorio**. Es un patrón ligado a la longitud: en las cuotas cortas falta el nudo largo terminal. Puede ser (i) una omisión sistemática del transcriptor en cuerdas cortas, o (ii) que el nudo no esté físicamente. En ambos casos la revisión es la misma: **mirar la punta de p9, p13, p19 y p64 de UR274B**.

### 3.4 Clasificación final

| Clase | n | Qué significa |
|---|---:|---|
| Error de lectura plausible | 8 | Reparable con pocas candidatas de tipo atestiguado (p180, p77, p51, R3 reg0/13/20, R2 g27c1) |
| Sistemático | 5 | El mismo patrón en el mismo slot/columna (columna 1 de UR278; 4 cuotas de UR274B) |
| Discrepancia entre copias | 1 | g12: los objetos/copias difieren en el número de nudos (4/5/6) |
| Discrepancia real o compuesta | 4 | Sin reparación de una edición: g4 (+24), g27c4 (−44), g28c6 (−94), UR266 p86 (−94) |
| Ambiguo | 17 | Reparable, pero con muchas candidatas o ediciones grandes (±1000, E→L7, etc.) |
| Sin destino | 9 | No verificable con el archivo conservado |

---

## 4. Controles

1. **Nulo geométrico por δ.** Para δ = ±1, el 80–100 % de las cuerdas aleatorias admiten una edición (basta añadir o quitar una vuelta). Para δ = ±10, ~85 %. Para δ = ±100, 12–72 % según el número de racimos. Para **δ = 24, 44, 46, 94, 125, la probabilidad es 0**: no existe ninguna edición de un nudo que los produzca. Esto separa limpiamente los casos.
2. **Nulo agregado.** 31/35 reparables observadas frente a 28,3 esperadas por geometría (p binomial ≈ 0,177, sin independencia). **No hay exceso atribuible a errores de lectura.** La reparabilidad es barata; por eso no la uso como evidencia.
3. **Especificidad.** La mediana de candidatas es 4; los casos que propongo como error tienen 1–4 candidatas y, además, una edición del tipo correcto (vueltas o conteo), no una inserción genérica.
4. **Repetición.** Los dos patrones que no son de un solo nudo (columna 1; cuotas 10) se evalúan con la probabilidad de que se repitan por azar: 1/9 = 0,11 y 5,5·10⁻⁴ respectivamente. El segundo sobrevive; el primero no.
5. **Comparaciones múltiples.** 35 contrastes: Holm exigiría p < 0,0014 para el más pequeño. Ningún caso individual lo alcanza; las conclusiones son **estructurales**, no inferenciales.
6. **Control negativo.** Las 3 sumas A+B sin destino y las 9 relaciones sin destino no se usaron para elegir candidatas ni para calcular tasas.

---

## 5. Resultados negativos

- **No se puede atribuir el +1 de la columna 1 a un error aleatorio**: aparece en las 2 filas 9/9, pero con mecanismos distintos (vueltas en una, figura de ocho en otra); p = 0,11, no significativo.
- **+24 (g4), −44 (g27c4), −94 (g28c6) y −94 (UR266 p86) no son reparables con una edición.** No son errores de un nudo: o son discrepancias reales, o son errores compuestos (≥2 operaciones), o hay una cuerda ausente.
- **Las cuotas 10 de UR274B no son erratas de lectura**: 4/19 en el mismo slot y todas las más cortas. La tasa de omisión del catálogo (2,6·10⁻⁴) las descarta como azar (p ≈ 8·10⁻¹²).
- **Tres de las diez sumas A+B no exactas no tienen destino**: no se puede decidir si son errores o discrepancias; el archivo conservado no alcanza.
- **La tasa de error del corpus es heterogénea**: el 86 % de las discrepancias está en 5 quipus. Usar la tasa global (0,64 %) para Incahuasi sobreestima el error; usar la del resto (0,10 %) es más honesto, pero sigue siendo una cota inferior.
- **No hay evidencia de un sesgo de investigador** (permutación p = 0,75 en `t_okr_vs_kfg`): el catálogo no se puede atribuir a un equipo.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| El catálogo de tipos de error y sus tasas (0,64 % global; 0,10 % resto) | **Bien apoyado** (conteo directo sobre 35 223 cuerdas) |
| El factor 10 es el tipo dominante (47 %) y está concentrado en 5 quipus | **Bien apoyado** |
| Las vueltas de nudos largos son el segundo tipo (26 %) | **Bien apoyado** |
| 31/35 casi-aciertos son reparables con una edición | **Bien apoyado** (por construcción) |
| La reparabilidad **no** es evidencia (80 % de las relaciones aleatorias también lo son) | **Apoyado con datos** (nulo geométrico) |
| g12 (+100) es una diferencia entre copias (4/5/6 nudos de centenas) | **Apoyado con datos** (tres copias convergentes) |
| UR278 p180 (7L→6L) es un error de lectura plausible | **Apoyado con datos** (resuelve celda y fila; 1 candidata de vueltas) |
| UR275 p51 omite el 7L terminal | **Apoyado con datos** (24/24 cuotas hermanas lo tienen; p = 0,0065) |
| UR278 p77 omite el 6L terminal (g8, +6) | **Apoyado con datos** (es la única de las 9 celdas sin nudo de unidades) |
| Las cuotas 10 de UR274B son un patrón ligado a la longitud, no azar | **Apoyado con datos** (p = 5,5·10⁻⁴; 4/4 más cortas) |
| g4 (+24) es discrepancia real o error compuesto | **Apoyado con datos** (ninguna edición de un nudo lo produce) |
| La columna 1 de UR278 tiene un sesgo sistemático de +1 | **Propuesto** (2/2, p = 0,11) |
| Las cuotas 10 son un rasgo del sistema (no del objeto) | **Especulativo** |
| Que los 4 "10" de UR274B sean nudos perdidos físicamente | **Especulativo** |

---

## 7. Para el coordinador

- **El catálogo existe y es utilizable, pero es una cota inferior.** 225 discrepancias KFG/OKR en 35 223 cuerdas (0,64 %): 47 % factor 10 de posición, 26 % vueltas de nudo largo, 5 % racimo omitido, 2 % E/L, 0,4 % S/L. El 86 % se concentra en 5 quipus; en el resto la tasa es 0,10 % por cuerda. KFG y OKR no son lecturas independientes (misma fuente Urton), así que el error de lectura física real no está medido.
- **La reparabilidad no es evidencia.** 31 de 35 casi-aciertos se arreglan con una edición, pero el nulo geométrico predice 28,3 (p ≈ 0,18): para δ = ±1 casi cualquier cuerda admite una vuelta más o menos. Un "casi-acierto reparable" no dice nada por sí solo.
- **Solo 4 casos son imposibles como error de un nudo:** g4 (+24), g27c4 (−44), g28c6 (−94) y UR266 p86 (−94). Ninguna edición de un racimo produce 24, 44 o 94. Son discrepancias reales o errores compuestos; no gastar tiempo en buscarlos en el museo como "un nudo mal leído".
- **g12 (+100) no es una errata: es una escalera de copias.** UR269 = 2433 (4 nudos de centena), UR278 = 2533 (5), UR266/UR275 = 2633 (6). Contar los nudos de centenas en UR266 p64, UR275 p41, UR269 p181 y UR278 p109–p117. Es el caso que más enseñaría sobre cómo se copiaban los quipus.
- **El caso más limpio para el museo es UR278 p180:** su 7L debería ser 6L. Una sola edición hace exactas la celda (238→237) y la fila g21 (1654→1653). Revisar las vueltas de ese nudo largo.
- **UR275 p51:** falta el 7L terminal (40→47). Las otras 24 cuotas de UR275 lo tienen; p51 es la segunda más corta. Probabilidad de una omisión: 0,65 %. Revisar la punta.
- **UR274B (p9, p13, p19, p64):** las cuotas "10" no son erratas aleatorias. Son 4/19, exactamente las 4 más cortas, en el mismo slot; la tasa de omisión del catálogo las descarta (p ≈ 8·10⁻¹²). Es un patrón ligado a la longitud: mirar la punta de esas 4 cuerdas para decidir si el nudo falta en el objeto o solo en la transcripción.
- **UR273 A+B:** 7 de las 10 no exactas tienen destino y residuales de ±1, ±10 o ±1000; las otras 3 no son verificables. Cuidado con reg18/reg19: ambas dan 1887 y apuntan a la misma cabecera (UR269 p171 = 1886); una es un duplicado de alineamiento, no dos errores.
- **Prioridad de revisión:** (1) UR278 p180; (2) UR278 p77 (¿falta el 6L terminal?); (3) UR275 p51; (4) las 4 puntas de UR274B; (5) los racimos de centenas de g12. Todo lo demás es ambiguo o no verificable.
- **Lo que falta:** una lectura independiente (foto/escaneo) de esas 7–8 cuerdas. Sin ella, el modelo de error no puede pasar de "apoyado con datos": el catálogo dice qué tipos de error son posibles y a qué tasa, pero no puede decidir entre un nudo mal contado y un objeto distinto.
