# Monografía del archivo de Ica y alrededores (Ica, Ocucaje, Callango, Ullujalla, Pisco)

Investigador: equipo ds/a_ica. Fecha: 2026-10-17.

## 0. Pregunta

¿Qué es y qué registraba el archivo de quipus de la zona de Ica (valle de Ica, Ocucaje,
Callango, Ullujalla y Pisco)? Cuatro sub-preguntas:
1. Descripción del conjunto (tamaños, estructuras, colores, valores, sumas, cuerdas
   superiores, unión R/V, torsión, dirección de nudos), con tabla por quipu.
2. Relaciones ENTRE los quipus del conjunto (secuencias/totales compartidos, estructuras
   de grupos y patrones de color), con nulo por permutación dentro de cada quipu.
3. ¿Existe jerarquía de archivo (quipus de detalle y de resumen)?
4. Contraste con la literatura sobre el sitio y propuesta de qué se registraba.

## 1. Método y selección

- Unidad de análisis: **el quipu** (regla 1 del BRIEF).
- Selección por `procedencia` (normalizada sin tildes, tokens exactos):
  `ica, ocucaje, callango, callengo, ullujalla, ullujaya, pisco`. El token exacto
  excluye falsos positivos como *Arica* (Chile) y otros.
- Resultado: **91 filas / 90 objetos únicos**. `KH0033` (=`UR044`) aparece con dos
  nombres para el mismo objeto (Peabody, "La puntilla, between Paracas and Pisco"):
  NO es un hallazgo, se deduplica. Ver `open-khipu-repository/data/okr-kh-numbers.csv`.
- Script: `01_seleccion.py`, salida `sel_ica.csv`.

### Procedencias del conjunto (tras selección)

| procedencia | n |
|---|---|
| Ica | 47 |
| Between Ica and Pisco | 8 |
| Valle de Ica Hacienda Callango Ocucaje | 8 |
| Hacienda Ullujalla y Callengo | 7 |
| Ocucaje | 4 |
| Pisco | 3 |
| Ica/Pisco | 3 |
| La puntilla, between Paracas and Pisco | 3 |
| Rancho San Juan, Ica Valley | 2 |
| Ullujaya, Ocucaje, Ica | 2 |
| Ica Valley, near Callango | 2 |
| Valle de Pisco | 1 |
| Ica or Cajamarquilla | 1 |

## 2. Descripción del conjunto

Script: `02_descripcion.py` → tabla completa en `tabla_quipus.csv` (una fila por quipu).
Uso de `khipu_summary.csv` (KFG, columnas precalculadas de sumas/R-V/nudos) + `cuerdas.csv`/`grupos.csv`.

### 2.1 Cifras globales

- 91 filas / **90 objetos** únicos; **6 820 cuerdas** = **5 353 colgantes** + **1 467 subsidiarias**; **923 grupos**.
- Colgantes por quipu: mediana **27**, mínimo **1** (`AS195`), máximo **864** (`UR231`). Distribución muy asimétrica.
- Colores distintos por quipu: mediana 4 (máx. 63 en `UR231`, 53 en `UR219`).
- Color dominante de colgante (todo el conjunto): **W blanco 810**, **B marrón 572**, MB 394, AB 358, LB 176, YB 168 (y combinaciones AB:MB, W:AB…). Predominan los **blancos y marrones**.
- Unión al cordón principal: **U/desconocida 3 811, V/verso 1 898, R/recto 1 018, T/cuerda superior 12**. U domina pero con R y V sustanciales.
- Torsión: **S 6 004 (88 %), U 556, Z 217**. Fuerte dominancia S (la torsión andina estándar en quipus de la costa).
- **Cuerdas superiores (top cords, `union=T` / `num_top_cords>0`): solo 5 quipus**. Suma de top cords: 2 quipus; doble suma de top cords: 1 quipu.
- R>V: 30 quipus; V>R: 31 quipus (reparto casi mitad y mitad).

### 2.2 Estructura

- El conjunto es bimodal en complejidad: muchos quipus pequeños (1–30 colgantes) con pocos grupos, y unos pocos **"monstruos" documentales** de cientos de cuerdas (`UR231` 864, `UR1114` 339, `UR1109` 287, `UR229` 189, `UR1166` 222, `UR242` 206). La mayoría parecen registros locales pequeños; unos pocos parecen grandes libros-índice.
- Colores: los quipus pequeños suelen ser casi monocromos (blanco o marrón; p. ej. `AS191`, `AS193`, `UR1141` = blanco 100 %; `AS195`, `UR1161` = marrón 100 %). Los grandes usan paletas amplias.
- Benford (primer dígito de valores): mediana ~0.78; unos pocos con Benford muy bajo (`UR231` 0.14, `UR219` 0.34, `UR139` 0.08) — coherente con listas largas no aleatorias o con dominancia de valores pequeños.

Tabla por quipu: `tabla_quipus.csv` (columnas: n_colg, n_subs, n_grupos, max_subs, color1, color2, frac_color1, n_colores, val_min, val_max, val_total, n_top_cords, n_top_sum, n_top_dsum, r_ratio, v_ratio, pct_s_knots, pct_z_knots, benford).

## 3. Relaciones ENTRE los quipus

Scripts: `03_relaciones.py`, `04_candidatos.py`, `05_tramos.py`, `06_robustez_sumas.py`,
`07_jerarquia.py`. Unidad: objeto único (90). Semilla 0; 500 permutaciones.

### 3.1 Secuencias de valores compartidas — **apoyado con datos**

Estadístico: nº de n-gramas de valores consecutivos (colgantes con valor, en orden de
lectura) compartidos entre todos los pares de quipus.

| test | obs | nulo medio | p |
|---|---|---|---|
| L=3 | 413 | 230.3 | 0.0020 |
| L=4 | 111 | 35.7 | 0.0020 |
| L=4 distintivo (max>2) | 52 | 16.3 | 0.0020 |
| L=4 distintivo y sin repetidos | 10 | 2.3 | 0.0020 |

Nulo: barajar los valores **dentro de cada quipu** (conserva el multiset, rompe el orden).
El exceso **sobrevive** a exigir valores distintivos y sin repetición → no es artefacto de
valores triviales (1,2,3).

**Hallazgo principal — par KH0128 (UR1114, "Between Ica and Pisco") ~ KH0137 (UR1123, "Ica"):**
comparten un **bloque verbatim de 10 valores consecutivos** `[40, 9, 57, 30, 56, 80, 21, 8, 22, 12]`,
flangeado por valores distintos:

```
KH0128  ... 3, 4, 3, 3, 2, 2, | 40,9,57,30,56,80,21,8,22,12 | 110,10,88,76,231,240 ...
KH0137  ...389,1350,63,500,54,560,| 40,9,57,30,56,80,21,8,22,12 | 600,15,10,50,1575,353 ...
```

Test del tramo contiguo máximo (distintivo): obs=10 vs nulo medio 5.1 (p95=6), **p=0.0020**.
Otros pares con tramos ≥5: KH0175~KH0190 (7), KH0379~KH0566 (6), KH0113~KH0162 (5),
KH0122~KH0474 / KH0122~KH0478 (5), KH0175~KH0384 (5).

Grafo de pares con ≥2 n-gramas L=4 distintivos: 8 aristas; el **hub** es KH0478 (UR250, Ica)
conectado a KH0122, KH0380, KH0447, KH0474.

### 3.2 Totales de un quipu que aparecen en otro — **apoyado con reserva**

Nº de pares (A,B) con `total(A)` igual a algún valor de cuerda de B.

| umbral de total | obs | nulo medio | p |
|---|---|---|---|
| >0 | 148 | 76.6 | 0.022 |
| >20 | 80 | 29.5 | 0.018 |
| >100 | 48 | 12.3 | 0.004 |
| >500 | 3 | 3.2 | **0.53** |

Nulo: barajar valores **entre** quipus globalmente (conserva el nº de valores por quipu).
Señal real para totales medianos, **nula para totales grandes** (no hay "gran total").
**Reserva (explicación aburrida):** los datos humanos son ricos en números redondos; totales y
valores colisionan más de lo que captura un nulo que destruye la "redondez". Los recuentos por
quipu además están confundidos por tamaño (`KH0222` total=6 "aparece en 26 quipus" es trivial).

### 3.3 Estructuras de grupos idénticas — **resultado negativo**

5 estructuras repetidas (p. ej. `(6,6)`: KH0158~KH0119; `(2,2,2,2,2,2,2,2,2,2)`: KH0157~KH0164).
Nº de pares idénticos obs=5 vs nulo=5.0, **p=1.000**. Control directo: KH0157 (UR1141) y
KH0164 (UR1148) comparten estructura (10 grupos de 2) pero sus valores son
`[20,20,24,...,22]` vs `[1327,2060,941,...,599]` — **sin relación de contenido**. La coincidencia
estructural es genérica (layout administrativo), no un vínculo.

### 3.4 Patrones de color compartidos — **resultado negativo (confundido por runs)**

L=4 aparentemente significativo (obs=909, nulo=453, p=0.002), **pero desaparece** al exigir
≥2 colores distintos en la ventana:

| filtro | obs | nulo | p |
|---|---|---|---|
| sin filtro | 909 | 453.5 | 0.0020 |
| ≥2 colores distintos | 214 | 212.9 | **0.4770** |
| ≥3 colores distintos | 1 | 6.6 | **1.0000** |

Es decir: el "patrón de color compartido" es **solo runs de color repetido** (bandeado), no
secuencias de color complejas. Control superado → no es hallazgo.

### 3.5 Corrección por comparaciones múltiples

7 tests principales (valor L3, L4, L4 distintivo, tramo máximo, totales, estructuras, color L4):
p ordenados = 0.002, 0.002, 0.002, 0.002, 0.002, 0.022, 1.0.
**Holm (α=0.05): 6 de 7 sobreviven** (todo menos estructuras de grupos, p=1.0).
**BH-FDR (q=0.05): 6 de 7 sobreviven.** El test de color queda anulado por su propio control (3.4).

## 4. Jerarquía del archivo (detalle vs resumen)

Script: `07_jerarquia.py`. Candidatos a **resumen** = quipus que contienen el total de otros:

- KH0127 y KH0128 (ambos "Between Ica and Pisco") contienen los totales de 7 quipus;
  KH0455 (Ocucaje) de 6; KH0468 (Ica/Pisco) de 5.
- "Detalle" (total más reutilizado): KH0222 (total 6, en 26 quipus), KH0211/KH0063 (18, en 11),
  KH0064 (33, en 11), KH0380 (38, en 9), KH0212/KH0213 (120, en 9), KH0177 (200, en 7).

**Nivel de evidencia: propuesto/especulativo.** Los "resúmenes" candidatos son también los
quipus más grandes (más valores → más oportunidades de contener un total ajeno); y los "detalles"
más citados tienen totales pequeños y triviales. No hay evidencia de un "gran total" (thr>500 = nulo).
Señal interna independiente: **cuerdas superiores** con suma: UR149 y AS072 (suma de top cords),
AS072 única con **doble suma de top cords**; 5 quipus con top cords (UR149, AS115, AS072, UR1051,
UR155). Sumas internas (KFG) muy comunes: pendant_pendant_sum en 1 026 casos, banded_clusters 428,
seriated_clusters 440.

## 5. Contraste con la literatura de este sitio

- **Urton (2005), "Khipu Archives: Duplicate Accounts and Identity Labels"**
  (`docs/fichas/2005-Urton-khipu-archives.md`) es LA fuente del archivo de Ica. Analiza como
  "archivo" un conjunto que se solapa con el nuestro y documenta pares concordantes:
  - **AS194/AS195** (AMNH, "cerda/lana cerca de Callango, valle de Ica", algodón): valores casi
    idénticos. En KFG = **KH0212/KH0213**, ambos con un único colgante con valor **120** (total 120).
  - **AS159/AS173** (Berlín, "entre Ica y Pisco"): los 7 primeros colgantes idénticos. KFG =
    **KH0175/KH0190**; nuestro método halla el tramo `[1,17,16,16,18,12,16]` (L=7). **Coincide.**
  - **AS114/AS123** (Berlín, Ica): segmento de **10 cuerdas** `40-9-57-30-56-80-21-8-22-12`
    (AS114 pendientes 40–49; AS123 pendientes 41–50). KFG = **KH0128/KH0137**; nuestro tramo
    máximo es exactamente ese bloque. **Coincide.**
  - **AS116/AS150** (Ica): diferencias *regulares* (AS116 siempre menor) → **KFG = KH0130/KH0166**.
    Nuestro método de coincidencia exacta **no lo detecta** (solo `[37]`): es un falso negativo
    instructivo, porque los valores difieren sistemáticamente (dos conteos sucesivos, no copia).
  - Urton **propone** (sin estadística, y él mismo lo advierte) que estas coincidencias son
    "cuentas duplicadas" en un sistema de *checks and balances* con varios khipukamayuq.
    Lo que aportamos es el **control que Urton no hizo**: el exceso de secuencias compartidas es
    significativo frente a un nulo de permutación dentro de cada quipu (p=0.002, sobrevive Holm/BH).
- **Urton y Brezine (2005, Puruchuco)** y **Urton y Chu (2015, Inkawasi)**: describen la
  síntesis de datos de censo/tributo "entre niveles contables". Es el modelo de jerarquía
  (detalle→resumen) que buscamos en el punto 3, pero en el valle del Rímac/Cañete, no en Ica.
- **2026-Thompson-peabody-khipus** y **2025-Thompson-ascher-corrections**: usan KH0032/KH0033
  (los "La puntilla, between Paracas and Pisco" de nuestro set) y muestran que KH0033 (=AS031=UR044)
  tiene **9 grupos (Ascher) vs 10 (UR)**: nuestra tabla usa la lectura KFG/UR (10 grupos), y
  confirma que KH0033 y UR044 son el **mismo objeto** (no un par).
- **1928-Locke-supplementary-notes**: los quipus AMNH de Ica (40.1-1550, 40.1-1551, D-N65-11)
  ya traían lecturas por cuerda y color; son parte de nuestro conjunto (AS191–AS197, etc.).
- **Medrano y Khosla (2024)** (`repo-kfg`, `2024-Medrano_data-science-khipu`): las fórmulas de
  Ascher cubren ≥74 % de los quipus; los **top cords son minoría** y marcan quipus "de trabajo"
  de bajo nivel; proponen cordeles **blancos como marcadores de límite** de grupos de suma. Nuestro
  set lo respeta: blancos y marrones dominan; top cords solo en 5 quipus.
- **Advertencias del `estado_del_arte.md`** que respetamos: museo ≠ procedencia (por eso usamos
  `procedencia`, y 74/91 quipus del set tienen `region` desconocida); el OKR/KFG **no es muestra
  aleatoria**; `value=0` sin nudos = ausente (regla 6 del BRIEF).

### ¿Qué se registraba aquí? (propuesta)

El patrón es el de un **archivo administrativo del valle de Ica**: muchos quipus pequeños
(mediana 27 colgantes) con estructura de grupos, sin top cord, dominados por el par blanco/marrón,
muchos con grupos seriados y bandeados (fórmulas de Ascher). Sobre ese fondo, un puñado de
**cuentas paralelas/duplicadas** de gran tamaño (KH0128, KH0137) que repiten tramos verbatim,
exactamente como predice el modelo de "cuentas concordantes" de Urton (2005). Es decir: este
archivo registraba **conteos (censos, tributo o producción) replicados por más de un
khipukamayuq**, no un texto. **Nivel: propuesto**, apoyado en la convergencia entre nuestro
resultado estadístico y los pares publicados.

## 6. Controles, resultados negativos y límites

**Controles aplicados**
- Unidad = quipu (objeto), no cuerda. Deduplicación de nombres (KH0033=UR044).
- Nulo explícito por permutación (semilla 0, 500 iteraciones): dentro de cada quipu (rompe orden,
  conserva multiset) para secuencias y color; entre quipus (conserva nº de valores por quipu)
  para totales.
- Filtro de "información": exigir valores distintivos (max>2) y sin repetición. El efecto de
  secuencias **sobrevive** (p=0.002 en todos los casos).
- Corrección por comparaciones múltiples: 7 tests; **Holm y BH-FDR dejan 6/7 significativos**.
- **Control positivo externo**: el método redescubre 2 de los 4 pares publicados de Urton (2005).

**Resultados negativos (importantes)**
1. **Patrones de color: NO son hallazgo.** El exceso aparente (p=0.002) desaparece al exigir
   ≥2 colores distintos en la ventana (p=0.477). Es solo **runs de color repetido** (bandeado).
2. **Estructuras de grupos idénticas: NO.** 5 pares coincidentes vs 5.0 esperados por azar (p=1.0).
   KH0157~KH0164 comparten `(2,2,2,2,2,2,2,2,2,2)` pero sus valores no tienen nada que ver.
3. **No hay "gran total" del archivo**: la contención de totales grandes (>500) es nula (p=0.53).
4. **La "componente de 8 quipus" no es significativa** (componente mayor obs=8 vs nulo medio 6.96,
   p=0.40): parece un grupo natural de quipus pequeños y seriados, no un sub-archivo.
5. **Sensibilidad del método**: coincidencia exacta falla en cuentas con diferencias regulares
   (AS116/AS150). Un solo tramo compartido no prueba copia (puede ser valor redondo recurrente).

**Límites**
- `procedencia` a nivel de sitio es gruesa; muchas fichas dicen solo "Ica" o "entre Ica y Pisco";
  la región está vacía en 74/91. No hay coordenadas ni contexto arqueológico.
- Los nombres KH cambian (Thompson 2025/2026 corrige valores y nº de grupos): parte de los
  tramos compartidos podría deberse a errores de transcripción heredados, no al objeto.
- 500 permutaciones dan una resolución de p≈0.002; no distinguimos p mucho menores.
- Nuestra lista de 33 "pares nuevos" está dominada por tramos de baja información
  (repeticiones, múltiplos de 10, seriaciones) y debe tratarse como **exploratoria**.

## 7. Nivel de evidencia (resumen)

| Afirmación | Nivel |
|---|---|
| El conjunto es un archivo administrativo costeño (blancos/marrones, sumas, sin top cords) | **apoyado con datos** |
| Existe exceso de secuencias numéricas compartidas entre quipus (p=0.002; Holm/BH OK) | **apoyado con datos** |
| KH0128~KH0137 (=AS114/AS123) y KH0175~KH0190 (=AS159/AS173) son cuentas paralelas | **bien apoyado** (se replican tramos verbatim) |
| KH0212/KH0213 (=AS194/AS195, Callango) son cuentas paralelas | **apoyado con datos** (total 120; KFG decodifica 1 cordón) |
| Contención de totales medianos entre quipus | **apoyado con reserva** (posible artefacto de "números redondos") |
| Jerarquía detalle→resumen con un "gran total" | **no apoyado / especulativo** |
| Tríada KH0141/KH0464/KH0465 (Pisco) comparte el patrón [30,40,30,50] | **especulativo** |
| Qué se registraba: conteos replicados por varios khipukamayuq | **propuesto** |

## Para el coordinador

- **El archivo de Ica son ~90 objetos** (91 filas; KH0033=UR044 es un duplicado de nombre):
  6 820 cuerdas, mediana 27 colgantes/quipu, dominado por blanco (810) y marrón (572); torsión S 88 %;
  unión U 3 811 / V 1 898 / R 1 018; solo 5 quipus con top cord. Nivel: apoyado con datos.
- **Sí hay estructura compartida ENTRE quipus**: el número de secuencias de valores consecutivos
  compartidas supera al azar (L=3: 413 vs 230; L=4 distintivo: 52 vs 16; **p=0.002**), y sobrevive
  a Holm/BH-FDR y a exigir valores distintivos sin repetición. Nivel: apoyado con datos.
- **El hallazgo es una REDISCOBERTURA, y eso valida el método**: nuestro par nº1 (KH0128~KH0137)
  comparte el bloque verbatim `40-9-57-30-56-80-21-8-22-12`, que es exactamente el par
  **AS114/AS123 de Urton (2005)**; y KH0175~KH0190 = AS159/AS173 (7 valores). 2 de 4 pares
  publicados de Urton quedan replicados. Nivel: bien apoyado.
- **Dos resultados negativos que ahorran trabajo**: (a) los "patrones de color compartidos" son
  solo runs monocromos (pasa de p=0.002 a p=0.477 al exigir ≥2 colores); (b) las "estructuras de
  grupos idénticas" son azar puro (p=1.0). Nivel: negativo.
- **No encontramos un archivo jerárquico con gran total**: la contención de totales grandes es nula
  (p=0.53) y la "componente de 8 quipus" no supera al nulo (p=0.40). Los "resúmenes" candidatos
  (KH0127, KH0128) son simplemente los quipus más grandes. Nivel: no apoyado.
- **La interpretación más sólida** coincide con Urton: cuentas administrativas **replicadas** por
  varios khipukamayuq (checks and balances), no un texto. Nivel: propuesto.
- **Candidatos nuevos para la siguiente ronda (exploratorios):** tríada Pisco **KH0141/KH0464/KH0465**
  (patrón `30,40,30,50`) y el enlace **KH0408** (Ica Valley, near Callango) con el par de Urton
  KH0128/KH0137. Deben probarse con nulos específicos y contra datos de museo.
- **Limitación a tener en cuenta:** el método de coincidencia exacta **falla** en cuentas con
  diferencias regulares (KH0130~KH0166 = AS116/AS150): hace falta un test de "paralelismo
  proporcional/desplazado" para no perder esos pares.
- **Recomendación:** ampliar el análisis de "archivo" a todo el corpus por pares (no solo Ica),
  con el nulo de dentro-de-quipu ya implementado (`05_tramos.py`), para ver si los pares de
  cuentas duplicadas se concentran en Ica o son un patrón de todo el sistema administrativo inca.
