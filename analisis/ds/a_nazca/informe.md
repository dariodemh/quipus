# Monografía del archivo de Nazca y Atarco

Autor: investigador del equipo (carpeta `analisis/ds/a_nazca/`). Fecha: 2026-10-17.

Scripts reproducibles en esta carpeta: `01_descriptivo.py`, `02_relaciones.py`,
`03_relaciones2.py`, `04_candidatos.py`, `05_totales.py`, `06_color_estructura.py`,
`07_nulo_intragrupo.py`. Salidas: `tabla_quipus.csv`, `relaciones_dump.json`.

## 1. Pregunta

¿Qué contiene y qué registraba el conjunto de quipus con procedencia **Nazca** y
**Atarco** del Khipu Field Guide (KFG)?

1. Describir el conjunto (tamaños, estructuras, colores, valores, sumas, cuerdas
   superiores, unión R/V, torsión, direcciones de nudo).
2. Buscar **relaciones entre** estos quipus (secuencias de valores compartidas,
   totales de uno que aparecen en otro, estructuras de grupos idénticas,
   patrones de color), con modelo nulo.
3. Reconstruir la jerarquía del archivo (quipus de detalle vs. de resumen).
4. Contrastar con la literatura del sitio y proponer qué se registraba.

## 2. Datos y método

- Fuente: `analisis/datos/{cuerdas,quipus,grupos}.csv` (KFG, ya preparados).
- Unidad de análisis: el **quipu** (regla 1 del BRIEF). Los tests de secuencias
  usan permutaciones **dentro de cada quipu**.
- Universo: los 19 quipus KFG con `procedencia ∈ {Nazca, Atarco}`:
  13 Nazca + 6 Atarco. Total **3 353 cuerdas**.
- Valores 0 sin nudos = ausentes (regla 6). Los trato como "huecos" que cortan
  las secuencias, no como ceros.
- Nulos: (i) barajar valores dentro de cada quipu; (ii) barajar valores dentro
  de cada **grupo** (control más fuerte, preserva tamaño de grupo y perfil de
  ausencias). 500 réplicas, semilla 0. p-valor empírico `(1+#{nulo≥obs})/(1+500)`.
- Verificación de identidad de objetos con
  `data/external/open-khipu-repository/data/okr-kh-numbers.csv`.

### 2.1 Identidad y procedencia de los objetos (control previo, ¡crítico!)

Del fichero OKR "Other Names":

- **KH0034 = AS032 = UR1032**: el **mismo objeto físico** con dos nombres KFG
  (el KFG solo lo lista como UR1032). Cualquier "coincidencia" AS032↔UR1032
  sería trivial. En `cuerdas.csv` solo existe como UR1032 (verificado: 0 filas
  AS032, 0 AS127).
- **KH0142 = AS127 = UR1127** y **KH0143 = AS128**: las **dos mitades** de la
  accesión de Berlín VA63042 **(A)** y **(B)**. UR1127 es un fragmento de 6
  cuerdas; AS128 el quipu grande (289). Comparten historia de colección.
- **KH0235 = AS215** y **KH0236 = AS215F**: AS215F es un **fragmento** (2
  colgantes con subsidiarias) asociado, registrado por los Ascher como F1/F2.
- **UR023, UR024, UR027, UR028, UR029, UR057** (los seis Atarco): según OKR están
  **atados juntos** ("six khipus tied together", accesiones "s/n" A–G). Es el
  vínculo físico más fuerte del conjunto y condiciona cómo leer las relaciones
  entre ellos (no son "objetos independientes que coinciden").
- **UR113, UR114, UR121, UR122** (Gotemburgo) y **UR1032, UR040** (Peabody):
  objetos independientes. (UR121 y UR122 comparten lote de museo 1938.45.)
- **Regla 6**: uso la procedencia declarada, no el museo; "Atarco" figura como
  procedencia y como región (Cuntisuyu, valle de Nazca).

## 3. Resultado 1 — Descripción del conjunto

Tabla por quipu (`01_descriptivo.py` → `tabla_quipus.csv`). `suma_grupo` = nº de
colgantes = suma de sus subsidiarias directas; `dir` = direcciones de nudo
presentes (la Z de los nudos en figura de ocho es artefacto del tipo de nudo).

| kfg | okr | proc | N_cuerdas | colg | subs | top | grupos | vmin | vmax | sumas | torsS | R | V | U | dir | colores dominantes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UR023 | KH0259 | Atarco | 20 | 10 | 10 | 0 | 2 | 0 | 4 | 1 | 20 | 10 | 0 | 10 | S,Z | AB:10;MB:10 |
| UR024 | KH0260 | Atarco | 19 | 10 | 9 | 0 | 2 | 0 | 3 | 1 | 19 | 0 | 10 | 9 | S | AB:10;MB:9 |
| UR027 | KH0262 | Atarco | 17 | 14 | 3 | 0 | 4 | 0 | 2 | 2 | 17 | 0 | 14 | 3 | S,U,Z | W:13;MB:4 |
| UR028 | KH0263 | Atarco | 91 | 76 | 15 | 0 | 8 | 0 | 102 | 1 | 89 | 75 | 0 | 16 | S,Z | AB:39;MB:38;KB:12 |
| UR029 | KH0264 | Atarco | 75 | 35 | 40 | 0 | 7 | 0 | 7 | 3 | 75 | 35 | 0 | 40 | S,U,Z | MB:36;AB:35 |
| UR057 | KH0293 | Atarco | 42 | 21 | 21 | 0 | 4 | 2 | 20 | 7 | 42 | 21 | 0 | 21 | S,Z | AB:21;MB:21 |
| AS128 | KH0143 | Nazca | 289 | 269 | 20 | 0 | 23 | 0 | 2968 | 0 | 0 | 0 | 0 | 289 | U | W:55;BS:42;DB:24 |
| AS215 | KH0235 | Nazca | 37 | 28 | 9 | 3 | 11 | 1 | 76 | 0 | 0 | 0 | 0 | 34 | U | W:DB:18;W:10 |
| AS215F | KH0236 | Nazca | 5 | 2 | 3 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 5 | U | W:3;DB:FB:2 |
| UR040 | KH0272 | Nazca | 49 | 33 | 16 | 0 | 4 | 0 | 21 | 0 | 49 | 0 | 0 | 49 | S | W:21;AB:14;DB:8 |
| UR1032 | KH0034 | Nazca | 541 | 415 | 126 | 0 | 108 | 0 | 11 | 15 | 540 | 8 | 403 | 130 | S,U,Z | LB:330;W:155;DB:35 |
| UR1127 | KH0142 | Nazca | 6 | 6 | 0 | 0 | 2 | 0 | 175 | 0 | 0 | 0 | 0 | 6 | Z | DB:5;W:1 |
| UR113 | KH0349 | Nazca | 866 | 332 | 534 | 0 | 31 | 0 | 620 | 20 | 858 | 330 | 3 | 533 | S,Z | W:203;AB:119;RB:107 |
| UR1136 | KH0152 | Nazca | 285 | 181 | 104 | 0 | 21 | 0 | 180 | 0 | 284 | 0 | 0 | 285 | S,U,Z | B:117;W:70;BB:42 |
| UR114 | KH0350 | Nazca | 260 | 219 | 41 | 0 | 16 | 0 | 20 | 2 | 248 | 18 | 197 | 45 | S,U,Z | W:63;AB:28;MB:22 |
| UR1140 | KH0156 | Nazca | 190 | 180 | 10 | 0 | 20 | 2 | 114 | 0 | 190 | 0 | 0 | 190 | S,U,Z | B:143;B:BB:20 |
| UR1176 | KH0193 | Nazca | 303 | 219 | 84 | 0 | 26 | 0 | 554 | 1 | 302 | 0 | 0 | 303 | S,Z | W:98;DB:96;B:41 |
| UR121 | KH0361 | Nazca | 40 | 23 | 17 | 0 | 5 | 0 | 856 | 1 | 39 | 12 | 11 | 17 | S | W:16;AB:7;RL:5 |
| UR122 | KH0362 | Nazca | 218 | 72 | 146 | 0 | 4 | 0 | 15652 | 0 | 218 | 0 | 65 | 153 | S,U,Z | AB:109;KB:37;MB:36 |

Totales: **3 353 cuerdas** = 2 145 colgantes + 1 164 subsidiarias nivel 1 + 43
nivel 2 + 1 nivel 3. Unión global: U 2 138, V 703, R 509, T 3. Torsión: S 2 990,
U 361, Z 1. **Gran total por quipu** (suma de cuerdas con nudos):

| kfg | total | kfg | total | kfg | total |
|---|---:|---|---:|---|---:|
| UR122 | 89 290 | UR1176 | 6 672 | UR028 | 308 |
| UR113 | 13 113 | UR1136 | 5 710 | AS215 | 266 |
| AS128 | 11 859 | UR1140 | 4 245 | UR057 | 185 |
| — | — | UR121 | 1 153 | UR029 | 125 |
| — | — | UR114 | 547 | UR040 | 113 |
| — | — | UR1032 | 357 | UR024 | 44 |
| — | — | UR1127 | 350 | UR023 | 43 |
| — | — | — | — | UR027 | 19 |
| — | — | — | — | AS215F | 9 |

Lecturas inmediatas:

- **Tamaños muy dispares**: de 5 cuerdas (AS215F, fragmento) a 866 (UR113).
  Los seis Atarco son pequeños (17–91 cuerdas); Nazca incluye los gigantes
  UR113 (866), UR1032 (541) y AS128 (289).
- **Torsión casi siempre S** (2 990/3 353 = 89 %); la única torsión Z pura es el
  fragmento UR1127. Ningún quipu con torsión dominante Z.
- **Unión**: dos "firmas". (a) Quipus casi todo en **U (desconocido)**: AS128,
  AS215, AS215F, UR1136, UR1140, UR1176 (bloque Berlín/Múnich + Hood).
  (b) Quipus con **R/V explícito**: UR1032 (403 V), UR114 (197 V), UR113
  (330 R), UR023/UR028/UR057 (R). **Solo AS215 tiene cuerdas superiores**
  (3; unión T).
- **Colores dominantes**: Atarco = alternancia marrón claro/medio (AB/MB); UR027
  blanco (W). Nazca: W y marrón claro (AB) dominan; UR1032 tiene un marrón claro
  (LB) muy marcado (330/541); UR1136 y UR1140 son marrones oscuros (B); UR122
  casi todo AB.
- **Presencia de sumas** (relaciones de Ascher ya calculadas por el KFG,
  `ascher_sum_relationships.csv`, 14/19 quipus):

| kfg | PPS | color | indexada | subsidiaria | cluster-cluster |
|---|---:|---:|---:|---:|---:|
| UR113 | 135 | 99 | 38 | 126 | 1 |
| UR1140 | 125 | 63 | 45 | 0 | 0 |
| UR1136 | 96 | 26 | 24 | 2 | 1 |
| UR1176 | 56 | 19 | 5 | 14 | 1 |
| AS128 | 45 | 8 | 5 | 0 | 0 |
| UR114 | 8 | 2 | 8 | 6 | 1 |
| AS215 | 7 | 3 | 0 | 2 | 0 |
| UR028 | 3 | 3 | 0 | 4 | 1 |
| UR121 | 3 | 0 | 0 | 0 | 0 |
| UR057 | 2 | 3 | 0 | 0 | 0 |
| UR1127 | 2 | 0 | 0 | 0 | 1 |
| UR122 | 1 | 0 | 3 | 0 | 0 |
| UR1032 | 1 | 2 | 0 | 0 | 0 |
| UR029 | 0 | 0 | 1 | 0 | 0 |

  Patrón claro: **UR113, UR1136, UR1140, UR1176 están saturados de relaciones de
  suma** (agregación), mientras **UR1032 (541 cuerdas) y UR122 (el de números
  gigantes) casi no tienen sumas** → no son "quipus de totales"; son secuencias
  largas o repetitivas. AS215F, UR023, UR024, UR027, UR040 no figuran (sin sumas
  detectadas).

## 4. Resultado 2 — Relaciones ENTRE quipus

### A) Secuencias de valores compartidas → **NEGATIVO (artefacto)**

Corridas contiguas de valores reales dentro de un grupo (los ausentes cortan la
corrida). Estadístico = nº de pares de quipus con ≥1 corrida común.

| L | obs pares | nulo intra-quipu (media) | p | nulo intra-**grupo** (media) | p |
|---:|---:|---:|---:|---:|---:|
| 3 | 32 | 22,8 | 0,020 | 36,3 | 0,90 |
| 4 | 13 | 3,8 | **0,002** | 10,1 | 0,13 |
| 5 | 2 | 0,3 | 0,042 | 1,7 | 0,55 |

- Con el nulo *intra-quipu* hay un exceso aparente (L=4: 13 vs 3,8; Holm sobre 3
  tests deja los tres por debajo de 0,05).
- Pero el **nulo intra-grupo** (que preserva el tamaño de grupo y la mezcla de
  valores dentro de cada grupo) **absorbe todo el exceso**: L=3 p=0,90; L=4
  p=0,13; L=5 p=0,55.
- La corrida común más larga del archivo es de **6 valores** entre UR028 y UR113:
  `[1,2,1,1,1,1]`; la siguiente, AS128–UR057 = `[3,3,2,3,3]`. **Todas las
  corridas largas son de valores 1–3**: regiones de baja entropía.
- Conclusión: **no hay evidencia de secuencias de valores compartidas entre
  quipus** más allá de lo esperado por la homogeneidad interna de los grupos
  (los grupos tienden a contener valores parecidos). Nivel: **bien apoyado
  (negativo)**.

### B) Totales de un quipu que aparecen en otro → **débil / negativo**

- Gran total de A como valor de cuerda de B: 16 coincidencias, **todas de
  totales pequeños** (AS215F=9 → 7 quipus; UR027=19 → 5 quipus; UR023=43;
  UR024=44; UR057=185 en UR1176). Los **grandes totales (UR113=13 113,
  UR122=89 290, AS128=11 859, UR1176=6 672) no aparecen como valor/subtotal en
  ningún otro quipu**.
- Estadístico global (subtotal de A = valor de B, umbral 15): obs 209 vs nulo
  (barajado intra-quipu, que solo afecta a las sumas de grupo) media 175,6,
  max 229, **p=0,016** sin corregir; dominado por subtotales pequeños (15–26).
  Con umbral alto (p. ej. ≥50) el efecto desaparece.
- Conclusión: **no hay jerarquía aritmética entre quipus**. Las coincidencias son
  de números pequeños que aparecen en cualquier quipu de muchos valores. Nivel:
  **apoyado con datos (negativo)**.

### C) Estructuras de grupos idénticas → **apoyado (por vínculo físico/documental)**

Vectores de "nº de colgantes por grupo", en orden:

| kfg | nº grupos | tamaños |
|---|---:|---|
| UR023 | 2 | [5, 5] |
| UR024 | 2 | [5, 5] |
| UR029 | 7 | [5, 5, 5, 5, 5, 5, 5] |
| UR057 | 4 | [3, 6, 6, 6] |
| UR027 | 4 | [5, 2, 3, 4] |
| UR028 | 8 | [1, 3, 20, 10, 1, 20, 1, 20] |
| UR1136 | 21 | [9 × 20, 1] (uno de 1) |
| UR1140 | 20 | [9 × 20] |
| UR122 | 4 | [18, 18, 18, 18] |
| UR1176 | 26 | dominante 8 (14 grupos) |
| UR1032 | 108 | patrón alternante 5,3 (51 grupos de 3) |
| UR113 | 31 | heterogéneo (dominante 5) |
| AS128 | 23 | dominante 10 (15 grupos) |
| AS215 | 11 | [1×6, 6, 4, 4, 4, 4] |
| UR114 | 16 | dominante 18 (4) |

- **UR023 ≡ UR024** ([5,5], idéntico) y ambos en el lote atado de Múnich.
- **UR1136 ≈ UR1140** ([9 ×20]): idéntica estructura de grupos (9 colgantes por
  grupo), y sus accesiones berlinesas son **consecutivas** (VA16635 y VA16636).
  En `quipus.csv` los metadatos ya operacionalizan esto: las columnas `pc_*` y
  `estructura` de ambos son casi calcadas y ambos están en Berlín. Es el
  candidato más fuerte a "dos quipus del mismo archivo/registro".
- El lote de Múnich comparte la convención de **grupos de 5** (UR023, UR024,
  UR029) y la paleta AB/MB; UR027 y UR057 se apartan.
- Conclusión: las estructuras idénticas **coinciden con vínculos físicos o de
  accesión**, no aparecen entre quipus de museos/procedencias no relacionadas.
  Nivel: **apoyado con datos** (UR1136/UR1140) y **propuesto** (Múnich).

### D) Patrones de color → **apoyado (modularidad robusta)**

- Periodicidad (mejor periodo T que maximiza la coincidencia `color[i]==color[i+T]`):
  media observada 0,747 vs nulo intra-quipu 0,579 (**p=0,005**). Restringiendo a
  los 10 quipus **multicolor** (≥3 colores): obs 0,672 vs nulo 0,411 (**p=0,003**).
- Los quipus multicolor con patrón casi periódico: **UR1032** (T=8, 0,96),
  **UR1136** (T=9, 0,90), **UR1140** (T=9, 0,88), **UR1176** (T=17, 0,84),
  UR028 (AB×5/MB×5). UR114 (0,28) y UR113 (0,51) **no** son periódicos: usan
  muchos colores sin módulo.
- Estructura de módulos (leída de las secuencias): UR1032 = `W` + `LB×5`;
  UR1176 = `RB` + `W×8` + `DB×7`; UR1136 = `W×8` + `W:BB×2`; UR1140 = `B…B` +
  `B:BB×2`; UR028 = `AB×5` + `MB×5`; AS128 = bloques de 10 (`BS×10`, `LD×10`,
  `W-KB×10`).
- Colores compartidos entre quipus (bigramas) no aportan: el bigrama `AB-AB`
  domina en cualquier quipu AB-cargado (UR113–UR114 comparten 16 bigramas, ambos
  de Gotemburgo, pero es trivial).
- Conclusión: el **color está organizado en módulos repetidos** (estructura
  bien apoyada con control). Compartir *exactamente* el mismo patrón de color entre
  quipus solo ocurre entre objetos del mismo lote/accesión. Nivel: **apoyado**.

## 5. Resultado 3 — Jerarquía del archivo

**Dentro de cada quipu (detalle → total interno): sí hay jerarquía.**

- **UR028 (=UR28, Atarco)**: el valor **102** aparece como un colgante y como la
  suma de **dos** grupos → **102 = 102 = 102**. Verificado por nosotros (grupos
  [1,3,20,10,1,20,1,20] con sumas [102,102,32,8,24,40]) y **coincide exactamente**
  con Urton (2019), que lo publica para UR28.
- **AS128**: p170 (70) + p170s1 (5) = 75, frente a la suma p177–p198 = 72
  (verificado en `cuerdas.csv`). Coincide con la corrección publicada de
  Thompson (2025). Es decir, AS128 tiene cuerdas de control de suma que no
  cuadran (error de transcripción o de registro).
- Los quipus con estructura de suma densa (UR113, UR1136, UR1140, UR1176) tienen
  decenas o centenares de relaciones de Ascher → registros de **agregación**.

**Entre quipus (detalle → resumen a escala de archivo): no se sostiene.**

- Ningún gran total de un quipu aparece como valor o suma de grupo en otro
  (§4B). No hay "quipu resumen" definido aritméticamente.
- Lo que sí hay es **agrupación física**: (i) los seis Atarco atados (Múnich);
  (ii) AS128+UR1127 (misma accesión, A/B); (iii) UR1136+UR1140 (accesiones
  consecutivas, misma estructura); (iv) AS215+AS215F (accesión con fragmento).
  La jerarquía, si existe, es **de conjunto físico**, no de aritmética entre
  objetos.

**Propuesta de lectura**: el archivo es heterogéneo; conviven (a) pequeños
quipus Atarco del lote de Múnich, probablemente **unidades contables** de pocas
decenas de cuerdas con grupos fijos de 5 y paleta AB/MB; (b) dos "quipus de
totales" berlineses hermanos (UR1136/UR1140) de 9 cuerdas por grupo; (c) grandes
quipus Nazca con decenas de grupos, parte de ellos saturados de sumas internas
(UR113, UR1176) y parte no (UR1032, UR122). Nivel: **propuesto**.

## 6. Resultado 4 — Contraste con la literatura del sitio

Búsqueda con `grep` en `docs/` (no leí PDFs ni ficheros grandes):

- **Urton (2019)** (ficha `2019-Urton-reflexiones-tahuantinsuyo.md`; y
  `docs/estado_del_arte.md` §4.6): describe **UR28 del Museum für Völkerkunde de
  Múnich, procedente de Atarco (valle de Nazca, Cuntisuyu), 74 cordeles**,
  demuestra **102 = 102 = 102** y la organización por color (AB/MB), y propone
  que 102 sea una ***pachaca* de mita** y que el quipu registre **seis ayllus en
  dos mitades**; "AB = hanan" queda **especulativo/circular**. → Nuestro UR028
  **es exactamente ese objeto**; nuestra verificación independiente reproduce su
  igualdad numérica. La semántica (pachaca, ayllus) es **propuesta**, no
  bien apoyada (el propio estado del arte la etiqueta así).
- **Thompson (2025), correcciones a Ascher** (`2025-Thompson-ascher-corrections.md`):
  documenta que **AS128 p170+p170s1 = 75 frente a p177–p198 = 72** (lo
  reproducimos) y errores de identificación de museo (varios AS reasignados entre
  VA-numberos de Berlín; pares intercambiados AS132/AS133 = VA24369A/B). Esto
  **avala** tratar con cautela los códigos de accesión berlineses.
- **Thompson (2026), Peabody** (`2026-Thompson-peabody-khipus.md`): confirma que
  **KH0034 = AS032/UR1032** (nuestro UR1032) y lista el conjunto **KH0035-41 =
  AS033A-G, "siete khipus atados en configuración circular"** (no es Nazca en
  nuestros datos, pero es otro ejemplo de "archivo" = objetos atados) y
  **KH0272 = UR040**. También **KH0033 = AS031/UR044 incompleto/UR1031**.
- **Milillo (2023)** (`2023-Milillo-khipu-colours.md`): dos khipus **wari**
  (1932.08.0001/0002) de **Gotemburgo**, procedencia declarada "Nasca". **No son
  los nuestros** (nuestros Gotemburgo son 1924.18.0001 = UR113, 1931.37.0001 =
  UR114, 1938.45.231/0228 = UR121/UR122). Matiz importante: en Gotemburgo se
  mezclan objetos Wari y "Nazca"; la procedencia "Nasca" del catálogo no es
  necesariamente inca.
- **Sivan (2026)** (`2026-Sivan_inca-spreadsheet.md`) usa **UR198 (Nazca)** entre
  sus muestras; **Clindaniel (2019)** y el estado del arte (§3.3, §4.6) dan el
  marco de "relaciones de Ascher" y de la dificultad de significación con valores
  pequeños (cita explícitamente el riesgo de coincidencia por azar que aquí
  cuantificamos).
- **FitzPatrick (2026)** (`2026-FitzPatrick_largest-khipu.md`): ficha mínima
  "relación entre el quipu más grande conocido y un quipu resumen", **sin texto
  ni datos verificables**; posible solapamiento con el quipu de Arica de Thompson
  (2024). **No la uso como evidencia.**

**Síntesis semántica (propuesta)**: lo que se registraba en Atarco (valle de
Nazca) es, con la mejor evidencia disponible (Urton 2019), un **conteo de
unidades/contribuyentes agrupados** (posiblemente *pachaca* de 100 + 2, seis
grupos/ayllus en dos mitades). Nuestros datos **no pueden confirmar ni refutar**
la semántica, pero **sí confirman** la aritmética interna (102=102=102) y la
organización modular por color. Para el resto del conjunto (Nazca grande) la
evidencia es aún más débil: hay agregación interna (muchas sumas de Ascher) pero
**ningún** vínculo aritmético entre quipus.

## 7. Controles y niveles de evidencia

| Afirmación | Control | Nivel |
|---|---|---|
| Composición del conjunto (tamaños, colores, unión, torsión) | recuento directo | **bien apoyado** |
| Color organizado en módulos periódicos | nulo intra-quipu, p=0,003 (multicolor) | **bien apoyado** |
| No hay secuencias de valores compartidas entre quipus | nulo intra-grupo, p=0,13–0,90 | **bien apoyado (negativo)** |
| UR028: 102=102=102 | verificación + coincide con Urton 2019 | **bien apoyado** |
| AS128: 75 vs 72 | verificación + coincide con Thompson 2025 | **bien apoyado** |
| UR1136 y UR1140 son dos quipus del mismo archivo | estructura idéntica (9×20) + accesiones consecutivas | **apoyado con datos** |
| Lote de Múnich = conjunto Atarco coherente | OKR "tied together" + grupos de 5 + paleta AB/MB | **apoyado** |
| No hay jerarquía aritmética entre quipus | nulo (p=0,016 sin corregir, dominado por valores pequeños) | **apoyado (negativo)** |
| Qué se registraba (pachaca/ayllus; tributo, censo) | literatura, sin test propio | **propuesto / especulativo** |

**Resultados negativos** (importantes): (1) no hay corridas de valores compartidas
entre quipus atribuibles a contenido compartido; (2) ningún total grande de un
quipu reaparece en otro; (3) no existe un "quipu resumen" detectable por
aritmética; (4) no hay dirección de nudo Z relevante (la única Z "real" es el
fragmento UR1127); (5) UR1032 y UR122 son grandes pero **no** son quipus de
sumas.

**Sesgos y límites**: bases del KFG con errores de transcripción documentados;
procedencias de museo heterogéneas y a veces contradictorias; el test de
"secuencias compartidas" es sensible al tratamiento de los ceros/ausentes; n = 19
quipus (potencia baja para vínculos entre objetos concretos).

## 8. Para el coordinador

- **No hay vínculo aritmético entre quipus de este archivo.** Al buscar "total de
  A = valor/suma de B", los grandes totales (UR113=13 113, UR122=89 290,
  AS128=11 859, UR1176=6 672) **no aparecen en ningún otro quipu**; solo coinciden
  totales pequeños (9, 19, 43, 44) por puro azar. La única pista global da
  p=0,016 sin corregir y desaparece al subir el umbral: **negativo**.
- **El hallazgo "secuencias compartidas" es un artefacto.** Hay exceso frente al
  nulo que baraja el quipu entero (p=0,002), pero **se desvanece** al barajar
  *dentro de cada grupo* (p=0,13–0,90). La causa aburrida: los grupos contienen
  valores homogéneos (sobre todo 1–3). Todas las corridas largas son de 1s y 2s.
- **Lo que sí es estructura real:** el **color está modulado** (periodicidad muy
  por encima del azar, p=0,003). UR1032 (T≈8), UR1136/UR1140 (T=9), UR1176
  (T≈17) son casi periódicos; UR113 y UR114 no. Este es el rasgo más robusto del
  conjunto y merece un análisis de módulos de color a escala de corpus.
- **Dos quipus hermanos en Berlín:** UR1136 y UR1140 tienen **estructura de
  grupos idéntica (9 colgantes × 20 grupos)** y accesiones **consecutivas**
  (VA16635/VA16636). Es el mejor candidato a "dos registros del mismo archivo"
  fuera de un lote atado. Recomiendo revisarlos con imagen de museo.
- **Cuidado con los nombres:** UR1032 = AS032 (mismo objeto), AS128/UR1127 = dos
  mitades de VA63042 (A/B), AS215/AS215F = objeto+fragmento, y los **seis Atarco
  (UR023/24/27/28/29/057) están atados juntos**. Cualquier "coincidencia" entre
  ellos no es un hallazgo.
- **Confirmamos la literatura:** UR028 (Atarco) tiene **102 = 102 = 102**
  (coincide con Urton 2019) y AS128 tiene 70+5=75 vs 72 (coincide con Thompson
  2025). Nuestro pipeline reproduce hallazgos publicados → vale como validación.
- **Atarco (Múnich) y Nazca grande se comportan distinto:** los Atarco son
  pequeños, con grupos de 5 y paleta AB/MB (convención de conteo uniforme); los
  Nazca grandes se dividen en "saturados de sumas internas" (UR113, UR1136,
  UR1140, UR1176) y "grandes sin sumas" (UR1032, UR122).
- **UR1032 y UR122 no son quipus de totales** pese a su tamaño (1 relación de
  suma cada uno). UR122 es el de números gigantes (total 89 290; 4 grupos de 18
  cuerdas ≈ 28 000 cada uno): revisar si es un registro de magnitudes grandes o
  una convención no decimal. Prioridad para la próxima ronda.
- **Nivel de evidencia:** bien apoyado (descripción, modularidad de color, 102=102,
  ausencia de secuencias compartidas); apoyado (UR1136/UR1140 mismo archivo, lote
  de Múnich); propuesto/especulativo (qué se registraba: pachaca/ayllus). La
  semántica de Urton para UR28 **no** la podemos elevar de "propuesta".
- **Recomendaciones:** (1) análisis de módulos de color con nulo de grupo en
  todo el corpus; (2) revisar UR1136/UR1140 con imágenes; (3) tratar UR122 y el
  bloque `tipo` no decimal como hipótesis aparte; (4) replicar el test
  intra-grupo delante de cualquier afirmación de "cuentas duplicadas" (Urton 2005)
  para separar vínculo real de homogeneidad interna.
