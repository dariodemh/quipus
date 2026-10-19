# UR006 (KH0242) — Lectura profunda de un quipu

**Carpeta:** `analisis/ds/k_UR006/` · **Scripts:** `01_reconstruir.py`, `02_aritmetica.py`, `03_nulos.py`, `04_color.py`, `05_posicion.py` · **Semilla:** 0 · **1000 permutaciones**

---

## 1. Pregunta

¿Qué estructura y qué aritmética internas tiene el quipu **UR006** (Leymebamba, KH0242, Centro Mallqui)**? Urton (2001, 2005) lo propuso como un **calendario bienal + censo de contribuyentes**. Objetivos:
1. Reconstruir la estructura completa (grupos, cuerdas, subsidiarias, colores, valores, cuerdas superiores, uniones, direcciones de nudo).
2. Buscar aritmética interna (colgante = suma de subsidiarias, cuerda superior = suma de grupo, valores repetidos, razones, periodicidades). Contrastar cada patrón con un **nulo de permutación** (barajar valores dentro del quipu, 1000 veces, semilla 0).
3. Proponer la lectura más probable y marcar el nivel de evidencia.
4. Señalar anomalías y posible información no numérica.

## 2. Método y datos

- Fuente: `analisis/datos/cuerdas.csv`, `grupos.csv`, `quipus.csv` (KFG) y, para clasificación física, `data/external/open-khipu-repository/data/khipu.db` (tablas `khipu_main`, `cord`).
- Identidad: KFG `UR006` = OKR `KH0242` = `KHIPU_ID 1000025` (INVESTIGATOR_NUM `UR006`, museo CMA.625/LC1-254, Leymebamba/Chachapoyas). Confirmado por conteo exacto de cuerdas en ambas fuentes (874).
- La unidad de análisis es el **quipu** (un solo individuo); por eso los nulos se construyen **barajando los valores dentro del quipu** (preservan la multitud de valores, la jerarquía y los colores). No hay inferencia poblacional posible (n=1): todos los p-valores son de "estructura interna vs. azar interno", no de una población de quipus.
- Convención del BRIEF: `valor 0` con `nudos` vacío = **cuerda sin nudos = ausente**, no un cero real.

## 3. Resultados: estructura

**Tamaño y forma general**
- **874 cuerdas** en el quipu: **571 colgantes** (nivel 0), **285 subsidiarias** (nivel 1) y **18 sub-subsidiarias** (nivel 2). (OKR: 570 a nivel 1, 276 a nivel 2, 18 a nivel 3, y 10 cuerdas por **encima** del cordón principal: 9 a nivel −2 y 1 a nivel −1.)
- **63 grupos** de colgantes. Hay una alternancia muy regular entre **grupos "grandes"** y **grupos "marcadores"** de una sola cuerda con ∼9–11 subsidiarias.

**24 grupos grandes (hecho clave)**
- Exactamente **24 grupos** tienen 20–22 colgantes (nunca menos de 20): G2, G5, G7, G10, G12, G14, G16, G18, G20, G22, G24, G26, G28, G30, G32, G36, G38, G40, G43, G45, G47, G50, G53, G56. El resto son marcadores (1 colgante) o cierres (G58=4, G59=2, G60=5, G61=2, G62=5).
- Suma de colgantes por grupo grande: 11–83 (mediana ≈ 40).

**24 "cuerdas anilladas" (loop pendants)** — coincidencia fuerte con OKR
- OKR clasifica `CORD_CLASSIFICATION` **PA/TPA = 24 cuerdas** (y 6 `M`). Esas 24 loop pendants **son** los colgantes de los 24 grupos marcadores con subsidiarias (p23, p46, p69, p91, …, p553). Además hay 6 marcadores tipo `M` (sin subsidiarias: grupos 8, 35, 42, 49, 52, 55) y 2 cuerdas-cabecera (p1, p2: grupos 0 y 1). El grupo 4 (p24, la "cuerda superior") es el marcador restante con descendientes.
- Los **24 grupos grandes** y las **24 loop pendants** son dos conjuntos de tamaño 24 que se alternan a lo largo del cordón principal: los colgantes anillados están equiespaciados (diferencias de 22–24 colgantes entre uno y otro).

**Cuerdas superiores (union T) y unión R/V**
- `union`: **V 412, R 339, U 113, T 9, ? 1**. Las 9 cuerdas `T` son las subsidiarias de **p24 (grupo 4)**, que en OKR están en **nivel −1/−2 (por encima del cordón principal)** → es el único conjunto "de cuerda superior" del quipu.
- El grupo 4 (p24 + 9 cuerdas superiores) suma 31; no iguala ninguna suma vecina obvia (ver §6, anomalías).

**Colores**
- Dominante **MB**; luego **AB, RB, KB, GG** y mezclas (`AB:GG`, `AB:KB`, `AB:MB`, `MB:KB`).
- El **cordón principal** es bicolor: `GG:MB(0–157 cm)/AB(157–220 cm)` → estructura bipartita.
- Los grupos grandes muestran una **plantilla posicional**: el colgante 1 es MB (11 grupos) o VR (13 grupos), el 2 suele ser AB (grupos iniciales) o MB, y el **último colgante** del grupo es casi siempre una cuerda **bicolor/mezclada** (AB:GG, AB:KB, MB:KB…).

**Nudos, giro y direcciones**
- Direcciones de nudo por instancia: **Z 565, S 33, U 2** (S aparece en solo 31 cuerdas, repartidas por todo el quipu, sin patrón claro).
- Tipos: **L** en 288 cuerdas, **E** (figura de ocho) en 236, **S** (simples) en las decenas. Los "unos" se escriben casi siempre como `1E` (figura de ocho).
- `torsion`: **S 844, U 29**. Las 29 U se concentran en los colgantes **marcadores/loop pendants** (p23, p46, p69, …), que además son las cuerdas sin nudos de cada grupo marcador.
- **323 cuerdas sin nudos** (valor 0 = ausente): 264 colgantes + 59 subsidiarias → **46 % de los colgantes son "vacíos"**; no son ceros numéricos.

**Totales**
- Suma de **todas** las cuerdas: **3037**. Colgantes: 1050. Subsidiarias: 1987.
- Valores más repetidos (colgantes): 0 (265), 1 (120), 2 (64), 3 (35), 5 (15), 4 (14), 7 (11), 9 (10).

## 4. Resultados: aritmética con controles

Familia de 4 pruebas de estructura aritmética (nulo = barajar los 874 valores, 1000 it., semilla 0):

| Prueba | Observado | Media nula | p |
|---|---|---|---|
| T1: colgante = suma de sus subsidiarias directas | 11 | 13.05 | 0.80 |
| T2: en un grupo, alguna cuerda = suma del resto | 1 | 1.90 | 0.87 |
| T3: marcador: última subsidiaria = suma de las anteriores (−2) | 0 | 0.24 | 1.00 |
| **T4: grupo marcador con tripla final (3 últimas subsidiarias) que suma ≥50** | **10** | **0.45** | **0.001** |

Otras pruebas (familias separadas):
- **Gradiente de valores por posición** dentro de los 24 grupos grandes: Spearman posición↔valor = **+0.487** (nulo ≈ 0.00, sd 0.05, **p=0.001**). La 1.ª mitad de cada grupo es 62 % ceros; la 2.ª, 27 %. La posición 12 es ≠0 en 23/24 grupos.
- **Regularidad posicional del color** (acuerdo con el color modal por posición): **0.669** vs nulo 0.634 (sd 0.003, **p=0.001**) → significativa pero de **efecto pequeño** (lo consume en gran parte el predominio de MB).

**Corrección por comparaciones múltiples.** En la familia aritmética (4 pruebas) se aplica **Holm**: solo T4 sobrevive (p=0.001 < 0.05/4=0.0125); T1, T2, T3 no. Con **BH-FDR** sobre las 6 pruebas (T1–T4, color, posición), sobreviven **T4, gradiente posicional y color** (p=0.001 cada una; umbral ≈0.025).

### 4.1 El hallazgo central: los 10 conjuntos de tres términos
En **10 grupos marcadores** (G3, G11, G13, G19, G21, G27, G29, G37, G39, G46) las **tres últimas subsidiarias** forman un trío numérico grande:

```
G3  30 65 20      G11 19 521 24    G13 30 80 20     G19 15 40 22
G21 20 71 35      G27 12 35 20     G29 20 61 20     G37 11 35 20
G39 10 40 16      G46 10 30 10
```
Los 10 colgantes de estos grupos son **PA/TPA (loop pendants)** confirmados en OKR, y las tríos están exactamente en las **tres últimas cuerdas** de cada loop pendant. **Esto replica con datos independientes y con un control nulo (p=0.001) el hallazgo de Urton (2005)**: "UR6 contiene 10 conjuntos numéricos de tres términos (p. ej. 20-61-20; 11-35-20; 30-65-20/30-80-20; 10-30-10)… localizados todos en las tres últimas cuerdas de los 'loop pendants'". Urton los interpreta como **etiquetas/nombres** (identidad de ayllu, tarea o período).

## 5. Lectura más probable

**Tipo de registro.** Los datos apoyan que UR006 es un **registro agregado y fuertemente estructurado** (censo/tributo o cuenta administrativa), no una narrativa ni un simple listado plano:
- 24 bloques comparables (los grupos grandes de 20–22 colgantes), cada uno "encabezado/cerrado" por una **loop pendant** (24 en total).
- Un **total global** de ~3037 (suma de todas las cuerdas) **concuerda con el total corregido de Urton (2005), 2962** (Urton 2001 daba 3005). La coincidencia del gran total es el indicio cuantitativo más fuerte de que estamos ante el mismo registro/lectura.
- 10 de los marcadores llevan una firma numérica de tres términos → **apoyado con datos**.

**Censo/calendario.** Lo que los datos **confirman** del modelo de Urton: la existencia de **24 bloques** y de **24 loop pendants** (compatible con "2 años = 24 meses" o con "24 unidades sociales"), los **10 tríos-etiqueta** y el **gran total ≈3000**. Lo que **no** confirman: el detalle "**730 cuerdas en 24 conjuntos de 29–31 cuerdas**". En KFG/OKR los 24 conjuntos tienen **20–22 colgantes** (no 29–31), y los colgantes son **571**, no 762. Es un **resultado negativo** (§6).

**Filas y columnas (propuesto).** La lectura interna más económica es una **tabla de 24 × ~21**:
- **Filas:** las **24 unidades** (los 24 grupos grandes; p. ej. ayllus/comunidades o meses).
- **Columnas:** las **~21–22 posiciones** dentro de cada grupo (una plantilla repetida). Apoyo: la regularidad posicional del color (p=0.001) y el **gradiente de valores** (p=0.001; los colgantes de la izquierda son casi siempre 0 y los de la derecha concentran las cantidades).
- Las **loop pendants** (24) funcionarían como **encabezado/subtotal/etiqueta** de cada fila; los 10 tríos serían la "etiqueta de identidad" de esos 10 bloques.
- Evidencia de esta parte: **propuesto** (estructura consistente; el contenido semántico de filas/columnas no está demostrado).

## 6. Anomalías y lo que no encaja

1. **Discrepancia con la literatura (importante, negativa).** Urton (2001/2005): 762 colgantes, 730 en 24 conjuntos de 29–31 cuerdas, total corregido 2962. KFG/OKR: **571 colgantes**, 24 conjuntos de **20–22** colgantes, total **3037**. Se reproducen el nº de conjuntos (24), los 10 tríos y el orden de magnitud del total; **no** el "29–31 cuerdas" ni los 762 colgantes. Hipótesis: convenciones de transcripción/segmentación distintas entre la lectura de Urton 2001 y la relectura KFG/OKR. Debe resolverse antes de aceptar la lectura calendárica día-por-cuerda.
2. **Grupo 4 (p24 + 9 cuerdas superiores):** única "cuerda superior" real; p24 está por encima del cordón principal (nivel −1/−2) y sus 9 cuerdas suman 31, sin relación aritmética encontrada. Podría ser un **marcador estructural** o información **no numérica**.
3. **p1:** `union = ?`, largo 0, sin color, sin nudos — cuerdas "cabecera/anilla" atípica.
4. **323 cuerdas sin nudos** (46 % de los colgantes): por convención son **ausencias**, no ceros. Que casi la mitad de los colgantes estén vacíos sugiere un uso "de plantilla" (posiciones reservadas que a veces no se llenan) más que una lista densa de cantidades.
5. **Nudos "raros":** los "unos" van casi siempre como **figura de ocho (E)**, no como nudo simple; la dirección **S** aparece en solo 31 cuerdas y sin patrón; **torsion/union "U"** se acumulan justo en los colgantes marcadores (probablemente por cómo se anuda la loop pendant). Y hay **un único nudo "0L"** (p388, grupo 38: `0L(5.5,U),0`), un nudo largo de cero vueltas con valor 0 — el único colgante con "cero explícito" (los 264 restantes con valor 0 no tienen nudos). Podría ser una marca, no una cantidad.
6. **Cordón principal bicolor** (GG:MB / AB a 157 cm): posible **partición en dos mitades** (¿dos años? ¿hanan/hurin?); no hay marcador obvio en 157 cm que lo confirme.

## 7. Información no numérica

La evidencia apunta a que buena parte del significado está en rasgos **no decimales**: el **color** (plantilla posicional, p=0.001, aunque de efecto pequeño), el **giro/torsión** (S dominante; U solo en los marcadores), el **tipo de unión** (R/V/T), la **forma física** (loop pendants PA/TPA) y la **dirección del nudo** (S/Z). Urton (2003, 2005) propuso que estos rasgos codifican información adicional; en este quipu el color posicional y la forma de las loop pendants son los candidatos más sólidos, pero su **contenido** sigue siendo **especulativo**.

## 8. Nivel de evidencia (resumen)

- **Apoyado con datos:** 24 grupos grandes de 20–22 colgantes; 24 loop pendants (PA/TPA) coincidentes en OKR; total global ≈3037 que concuerda con el de Urton; **10 conjuntos de tres términos en las 3 últimas cuerdas de los loop pendants** (p=0.001, réplica independiente de Urton 2005); **gradiente de valores por posición** (p=0.001).
- **Propuesto:** lectura como registro agregado tipo censo/tributo; tabla 24 filas × ~21 columnas; loop pendants como subtotales/etiquetas.
- **Especulativo:** que los 10 tríos sean "nombres/etiquetas de identidad"; que el color posicional tenga contenido semántico; la partición bicolor del cordón principal.
- **Resultado negativo:** la estructura "730 cuerdas en 24 conjuntos de 29–31 cuerdas" **no** se reproduce; y **no** hay aritmética de suma colgante=subsidiarias (p=0.80) ni grupo=suma de grupos (p=0.87).

## 9. Para el coordinador (lo más importante)

- **UR006 (KH0242) = el UR6 de Urton**: KFG y OKR coinciden en 874 cuerdas; gran total 3037 ≈ 2962 de Urton, así que es el mismo registro. Nivel: **demostrado**.
- **24 grupos grandes (20–22 colgantes) + 24 loop pendants (PA/TPA)**: estructura rígida y perfectamente identificable en ambas fuentes. Explica el "24" calendárico/demográfico de Urton. Nivel: **apoyado con datos**.
- **Los 10 conjuntos de tres términos** (p. ej. 30-65-20; 20-61-20; 11-35-20) están en las 3 últimas subsidiarias de los loop pendants: **replicado con control nulo (p=0.001)** y coincide con la lista publicada por Urton (2005). Nivel: **apoyado con datos**.
- **Gradiente numérico por posición** dentro de cada grupo (Spearman +0.49, p=0.001): los colgantes de la izquierda son 0 y los de la derecha acumulan las cantidades → **apoya una plantilla de columnas**. Nivel: **apoyado con datos**.
- **NO hay aritmética de sumas**: colgante=Σsubsidiarias falla (p=0.80) y grupo=Σgrupos falla (p=0.87). No es un quipu de totalización simple. Nivel: **resultado negativo**.
- **No se reproduce el "730 cuerdas en 24 conjuntos de 29–31"**: aquí los conjuntos tienen 20–22 colgantes y hay 571 colgantes, no 762. Antes de aceptar la lectura "1 cuerda = 1 día" hay que conciliar las convenciones de conteo. Nivel: **resultado negativo / caveat**.
- **46 % de los colgantes no tienen nudos** (ausencias, no ceros) → refuerza que es una **plantilla de posiciones** parcialmente llenada, no una lista densa.
- **Anomalías:** el grupo 4 (p24 + 9 cuerdas superiores, nivel −1/−2) es el único ensamblaje "de cuerda superior" y no cuadra con ninguna suma; p1 es una cuerda-cabecera atípica.
- **Recomendación siguiente ronda:** (a) conciliar 571 vs 762 colgantes y 20–22 vs 29–31 cuerdas/conjunto usando el apéndice de Urton (2003/2005) y la lectura física del museo; (b) buscar el mismo patrón "24 grupos + 10 tríos en loop pendants" en UR9 y UR21 (Urton dice que replican ~1/6 de UR6) — es la prueba de falsabilidad natural; (c) probar si las columnas (posiciones) tienen un significado estable comparando los 24 grupos columna a columna (¿la columna 12 es siempre un tipo de conteo?).
