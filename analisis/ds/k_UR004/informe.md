# UR004 — Lectura profunda de un quipu (Leymebamba / Laguna de los Cóndores)

**Autor:** equipo `k_UR004` · **Fecha:** 2026-10-17 · **Datos:** `analisis/datos/{cuerdas,grupos,quipus}.csv` (KFG) + `khipu.db` (OKR) como contraste.
**Scripts (misma carpeta):** `01_estructura.py`, `02_aritmetica.py`, `02b_grupos.py`, `03_refinado.py`, `04_detalle.py`, `05_multiple.py`, `06_final.py`. Salidas en `0*.txt`.

---

## 1. Pregunta

¿Qué es UR004 y qué registra? Objetivo: (1) reconstruir su estructura completa; (2) buscar toda la aritmética interna y contrastarla con un nulo de permutación; (3) proponer la lectura más probable (censo, tributo, depósito, calendario, otro) con evidencia literaria; (4) señalar anomalías y posibles contenidos no numéricos.

**Identidad del objeto.** UR004 = **KH0240** (OKR), museo **Centro Mallqui, Leymebamba (Amazonas)**, nº de museo `CMA 847-LC1.476 TEQ`, procedencia **Leymebamba**, región **Chachapoyas** (el estado del arte lo liga a la Laguna de los Cóndores; no se usa el museo como lugar de origen). **573 cuerdas**, cordón principal MB, estructura "P". OKR confirma 573 cuerdas y **ningún** tipo de fijación "T".

---

## 2. Método

- **Unidad de análisis:** el quipu. Las pruebas a nivel de cuerda/grupo usan **permutaciones dentro de UR004** (barajar la multiset de valores sobre las cuerdas con nudo), 1000 réplicas, semilla 0. p empírico = (1 + #{nulo ≥ obs}) / (1 + 1000).
- **Corrección de multiplicidad:** Holm y Benjamini–Hochberg sobre el conjunto de pruebas (`05_multiple.py`). Se advierte que varias pruebas de color miden el *mismo* fenómeno (no son independientes).
- **Clave de datos aprendida (crítica):** en `grupos.csv`, `desde/hasta` son posiciones **1-based entre las cuerdas de nivel 0** (pendientes), no el `orden` global. Los grupos **particionan exactamente** los 482 pendientes (verificado). Las subsidiarias no están en `grupos.csv`; heredan el `grupo` de su madre.
- **Valores 0 sin nudos = ausentes** (no ceros reales): se tratan como 0 sólo al sumar, y se marcan como no informativos al contar coincidencias "no triviales".

---

## 3. Resultados — estructura (con cifras)

| Dimensión | Resultado |
|---|---|
| Cuerdas totales | **573** (482 nivel 0 = pendientes; 87 nivel 1; 4 nivel 2) |
| Grupos | **73** (28 de 1 cuerda; 45 de ≥2). Tamaños: mediana 5, máx **30**. Suman 482 |
| Cuerdas superiores (union **T**) | **0** — no hay top cords (KFG y OKR coinciden) |
| Unión R / V / U | **R 213 · V 246 · U 114** (U concentra 79 de 91 subsidiarias) |
| Torsión | **S 540 · U 33** |
| Terminación | K 445 · U 121 · B 7 |
| Dirección de nudo | **Z dominante** (KFG 524 Z / 61 S / 1 U; OKR 857 Z / 71 S) |
| Con / sin nudos | 424 con nudo · **149 sin nudo (26.0 %)** |
| Valores (424 con nudo) | 1→2230; mediana 5; p90 ≈ 60; p99 ≈ 342; **valor 1 = 114 cuerdas (26.9 %)** |
| Colores | **MB 346 (60.4 %)**, KB 47, GG 32, GG:MB 31, **PK 31**, AB 19, MB:KB 15, + colas |
| Suma total | **12 304** |
| Valor máximo | **p444 = 2230** (grupo 65; `2S(3.5)=2000 + 2S(6.5)=200 + 3S(14)=30`, MB, union R) |

**Patrón de agrupamiento:** los `pos_cm` de los grupos vienen por **parejas** (misma posición sobre el cordón principal): 0; 3‑3; 9‑9; 17‑17; 20‑20; 22‑22; … (73 grupos en 44 posiciones; una posición con 4). Típicamente una **cuerda-marcador** (a menudo PK) acompaña a un grupo mult-cuerda. Los grupos **no son monocromáticos** (solo 4/45 lo son): el color **varía dentro del grupo**.

**Subsidiarias:** 91 (máx 6 por madre). Las 4 de nivel 2 cuelgan de p164s1…s4. **Color de la subsidiaria = color de la madre en 67/91 = 74 %** (herencia de color hacia abajo).

---

## 4. Resultados — aritmética interna y controles

Nulo: barajar los 424 valores dentro de UR004 (1000×, semilla 0). La columna "Holm/BH" usa la familia de 10 pruebas.

| Prueba | obs | nulo (media) | p | Holm | BH |
|---|---|---|---|---|---|
| T1 colgante = Σ subsidiarias directas | 6/84 | 4.69 | 0.302 | 1.00 | 0.40 |
| T1b idem, madres con ≥2 subsidiarias | 0/3 | 0.01 | 1.000 | 1.00 | 1.00 |
| T2 colgante = Σ todos los descendientes | 6/84 | 4.75 | 0.319 | 1.00 | 0.40 |
| T3 grupo: una cuerda = Σ de las demás (**crudo, diagnóstico fuera de la familia**) | 12/45 | 6.20 | 0.001 | — | — |
| **T3 limpio** (≥2 sumandos con valor>0) | **2/45** | 0.70 | **0.152** | 0.76 | 0.25 |
| T4 Σ de grupo = valor de una cuerda **ajena** | 21 | 13.83 | 0.003 | 0.024 | 0.010 |
| A sumas de grupo **repetidas** | 9 | 3.46 | 0.002 | 0.018 | 0.010 |
| B grupo de 1 cuerda adyacente = Σ del vecino | 0 | 0.10 | 1.000 | 1.00 | 1.00 |
| **T8 color adyacente igual (lag 1)** | 290/572 | 218.7 (sd 6.9) | **0.001** | 0.010 | 0.010 |
| **T9 entropía de color dentro de grupo** | 1.318 | 1.431 (sd 0.051) | 0.014 | 0.084 | 0.028 |
| T5 total del quipu = valor de una cuerda | 12304 no aparece | — | — | — | — |

**Testigo del intento interesante (la explicación aburrida ganó).** Los 12 "aciertos" de T3 con la definición cruda resultaron **todos triviales**: 5 grupos donde **todas** las cuerdas valen 0 (0=0), y 7 casos donde el "sumando" es una **única** cuerda no nula igual al supuesto total. Al exigir **dos o más sumandos con valor > 0**, los casos caen a **2/45 (p = 0.152, n.s.)**: **no hay aritmética interna genuina**. Análogamente, las coincidencias de T4 y A están dominadas por los valores pequeños hiperfrecuentes (1, 2, 3, 4, 6) — p. ej., el "grupo suma = 1" coincide con ~100 cuerdas del quipu. **T4 y A se retiran como evidencia de mecanismo.** T5 (total) tampoco aparece.

**Lo que sí sobrevive (una sola familia de hechos):** el **color tiene estructura local real y fuerte**:
- lag‑1: 290 pares de color igual vs 218.7 esperados (z ≈ **10.4**, p = 0.001).
- lag‑2: z ≈ 4.3 (p = 0.001); lag‑3: z ≈ 2.5 (p = 0.005); lag‑4: **no** (p = 0.49).
- Tramo máximo de color igual = **22** vs 11.5 esperado (p = 0.006).
- Entropía de color por grupo por debajo del azar (p = 0.002–0.014).
Los colores se agrupan en **rachas de 2–3 cuerdas** y se heredan madre→subsidiaria (74 %). Esto es **un único fenómeno medido con 3–4 pruebas correlacionadas**, no cuatro hallazgos independientes.

**Corrección global (familia de 10 pruebas, `05_multiple.py`):** con **Holm** (α=0.05) sobreviven **T8 (0.010), A (0.018), T4 (0.024) y C (0.042)**; **T9** solo pasa **BH** (0.028). Con **BH** sobreviven T8, A, T4, C y T9. Pero **T4 y A son artefactos de valores pequeños** (¶ anterior), de modo que el **balance neto es: estructura de color = significativa; aritmética interna = negativa.** (Las pruebas de color T8/C/T9 miden un mismo fenómeno y están correlacionadas.)

---

## 5. Resultados negativos (importantes)

1. **Sin cuerdas superiores** (0 union T en KFG y OKR): no puede existir "cuerda superior = Σ de grupo".
2. **Sin sumas internas** (T1, T1b, T2, T3 limpio, B): UR004 **no** pertenece al subconjunto de quipus con "fórmulas de Ascher" que Medrano y Khosla (2024) cifran en ~74 %. Está, con alta probabilidad, en la minoría sin sumas.
3. **Sin total global** ni total/2 como cuerda.
4. **Sin periodicidad calendárica:** solo 2 grupos de 29–31 cuerdas (no la estructura 24×29‑31 que Urton 2001 describe para UR6, del mismo sitio).
5. **Sin relación "resumen":** el valor del grupo no aparece en una cuerda adyacente designada (B = 0; T4 = artefacto).

---

## 6. Anomalías y posible información no numérica

- **31 cuerdas PK**, todas con valor 0: sus notas las describen como **"nudo en el cordón principal con borla"**, "un nudo del cordón principal", "hilos envolviendo el cordón principal". **No son cuerdas colgantes reales**: son **anotaciones del propio cordón principal** que KFG registra como pseudo-cuerdas. Funcionan como **marcadores de posición/límite** (cfr. Medrano y Khosla 2024 sobre marcadores de límite), no como números.
- **149 cuerdas sin nudos (26 %)**: 138 pendientes "vacías" (¿categorías sin dato, o columnas con cero real?), más 10 subsidiarias y 1 de nivel 2. No es un cero (BRIEF).
- **p164** es el único caso con estructura de 3 niveles (4 hijas, cada una con 1 nieta) — un "subárbol" atípico dentro de un quipu mayormente plano.
- **Torsión U (33) y terminación U (121)** concentradas en cuerdas sin nudo / PK (información perdida o no registrada).
- **Dirección de nudo casi siempre Z (89 %)**: la variación S (61 nudos) es escasa; no se detectó un uso sistemático de la dirección como marcador binario (no se probó en esta ronda).
- Posiciones del cordón principal con **grupos pareados** (misma posición, a veces 3–4 grupos): sugiere una **jerarquía implícita posición→grupos**, posible residuo de cómo KFG segmentó el espacio.

---

## 7. Lectura propuesta

**Qué es (nivel de evidencia: propuesto → especulativo en la función).** UR004 no es un quipu "aritmético": carece de sumas internas, de top cords y de totales. Es un registro **categórico/tabular con conteos**, organizado en ~73 unidades (=grupos de pendientes, ancladas a posiciones del cordón principal) con estructura interna de 1 a 30 cuerdas.

**Filas y columnas (propuesto).**
- **Filas = grupos** (73), separadas por posición sobre el cordón principal y frecuentemente precedidas por una cuerda-marcador (PK); los grupos suelen venir en parejas por posición (posible par *marcador / contenido*).
- **Columnas/dimensiones = (a) las cuerdas dentro del grupo**, **(b) el color** de cada cuerda y **(c) las subsidiarias** del mismo color que la madre.
- **Celdas = el valor decimal** decodificado (conteos pequeños, 1 dominante) + presencia/ausencia de nudo.

**Tipo de registro.** Descarto **calendario** (sin periodicidad 29–31) y **depósito puro de un solo ítem**. El perfil (muchas filas, columnas de conteo pequeño, categorías por color, marcadores de límite) es compatible con un **registro administrativo de tipo censo/tributo** de la zona Chachapoya, en la línea de lo que Urton (2001) propone para **UR6 del mismo sitio** (calendario+censo) — pero **sin** la componente calendárica. Con un 27 % de cuerdas que valen 1 y 26 % sin nudo, la lectura más prudente es **lista de cuentas/atributos por unidad (censo, contribuyentes, bienes o servicios) con columnas de color-categoría**.

**Justificación literaria.**
- Urton (2001, `docs/fichas/2001-Urton-calendrical-tomb-text.md`): UR6, del **mismo contexto funerario de Leymebamba/Laguna de los Cóndores**, se interpreta como **censo de contribuyentes** y calendario. Establece que en este sitio se registraron cuentas **demográficas/tributarias** — marco para UR004, que sin embargo **no** comparte la estructura calendárica de UR6.
- Medrano y Khosla (2024, `2024-Medrano_data-science-khipu.md`): **~74 %** de los quipus tienen fórmulas de Ascher; los **top cords registran una minoría** de las sumas y los **cordeles blancos marcan límites**. UR004 cae en la minoría **sin** sumas y usa cuerdas-marcador **PK** en vez de blancas → apoya que UR004 sea un quipu "de trabajo"/lista, no un documento de cómputo.
- Clindaniel (2025, `2025-Clindaniel_colorful-insights.md`): el color forma un **sistema semiótico** con dominios opuestos y polisemia → respalda tratar el color de UR004 (estructurado localmente, heredado) como **dimensión de categoría**, no decorativa.
- Contexto del archivo: el estado del arte (`docs/estado_del_arte.md` §4.6) sitúa a Leymebamba (UR6/UR9/UR21) entre los casos de cuentas duplicadas y de "etiquetas" de 3 términos. UR004 no muestra pares duplicados creíbles.

**Niveles de evidencia.**
- *Apoyado con datos:* color estructurado (rachas lag 1–3, homogenidad de grupo, herencia 74 %); ausencia de top cords; ausencia de sumas internas; valores sesgados a 1.
- *Propuesto:* grupos = filas/unidades de registro; color = categoría; cuerdas PK = marcadores de posición/límite.
- *Especulativo:* identificación con censo/tributo concreto; correspondencia con unidades administrativas Chachapoya.

---

## 8. Limitaciones

- **n = 1 quipu**; sin réplica externa; los p-valores son internos al objeto.
- Los valores son los **decodificados por KFG** (dependen de su transcripción de nudos); no se re-transcribieron.
- Varias pruebas de color son **dependientes**; la corrección de multiplicidad sobreestima la independencia (y aun así sobrevive).
- La partición en 73 grupos y las cuerdas PK dependen de cómo KFG registró el cordón principal; interpretarlas como "filas" es una hipótesis, no un hecho.
- No se probó la dirección S/Z como marcador binario (queda para otra ronda).

---

## 9. Para el coordinador

- **UR004 = KH0240**, Leymebamba (Chachapoyas), 573 cuerdas reales (482 pendientes / 91 subsidiarias / 73 grupos); confirmado en KFG y OKR, **sin cuerdas superiores (0 union T)**.
- **No hay aritmética interna.** Colgante=Σsubsidiarias (p=0.30), Σdescendientes (p=0.32) y Σ de grupo (p=0.15 tras quitar los casos triviales) son **negativos**. UR004 cae en la minoría de quipus **sin** las "fórmulas de Ascher" (~74 % de Medrano/Khosla 2024).
- **El hallazgo positivo es el color:** rachas locales de 2–3 cuerdas (lag‑1 z≈10.4, p=0.001; lag‑2/3 también), entropía de color por grupo por debajo del azar (p≈0.002) y **74 % de subsidiarias con el color de su madre**. El color se comporta como **categoría/columna**, no como adorno. *Nivel: apoyado con datos.*
- Los tests "bonitos" (Σ de grupo = cuerda ajena; sumas repetidas) son **artefactos** de los valores pequeños hiperfrecuentes (1 aparece 114 veces = 27 %): **no** los reporto como mecanismo de resumen.
- **Anomalía estructural clave:** 31 cuerdas **PK**, todas valor 0, con notas tipo "nudo/borla en el cordón principal" → **no son pendientes**, son **marcadores de posición/límite** (análogo a los marcadores blancos de Medrano y Khosla 2024). Los grupos vienen **pareados por `pos_cm`** (marcador + contenido).
- **Sin periodicidad calendárica** (solo 2 grupos de 29–31 cuerdas): UR004 **no** replica la estructura de UR6 del mismo sitio (Urton 2001, calendario+censo).
- **Lectura más probable (propuesto/especulativo):** registro **categórico-tabular de cuentas pequeñas** (tipo censo/tributo bienes-servicios): filas = grupos/unidades, columnas = cuerdas + color-categoría + subsidiarias; celdas = conteos (1 dominante). No es depósito de un solo ítem ni calendario.
- **Recomendaciones siguientes:** (1) replicar el test de color lag en los demás quipus de Leymebamba para ver si las rachas de color son de sitio; (2) probar la dirección de nudo S/Z como marcador binario (no hecho aquí); (3) usar las cuerdas-marcador PK como **anclas de segmentación** para redefinir "filas" y volver a probar sumas; (4) contrastar UR004 con el archivo Leymebamba (UR001–UR022) buscando secuencias de valores/colores compartidas.
