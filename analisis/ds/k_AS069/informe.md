# AS069 (KH0082) — Lectura profunda de un solo quipu

**Autor:** equipo `k_AS069` · **Fecha:** 2026-10-17 · **Carpeta:** `analisis/ds/k_AS069/`

---

## 1. Pregunta

AS069 es el quipu con más cuerdas del corpus KFG (1831), procedente del valle de Lluta (Arica, Chile), excavado por Percy Dauelsberg en 1965. Preguntas:

1. ¿Cuál es su estructura completa (grupos, subsidiarias, colores, valores, cuerdas superiores, uniones, nudos)?
2. ¿Qué aritmética interna contiene (sumas, igualdades, razones, periodicidad de color), y supera esa aritmética a un nulo?
3. ¿Cuál es la lectura más probable (tipo de registro, filas y columnas)?
4. ¿Qué no encaja y qué pudo ser información no numérica?

## 2. Método y datos

- Datos: `analisis/datos/cuerdas.csv` (1831 filas para AS069), `grupos.csv`, `quipus.csv` y `data/external/open-khipu-repository/data/khipu.db` (OKR, KHIPU_ID 1000096). Relaciones de suma de Ascher precomputadas por KFG en `data/external/data-science-khipu-article/data/ascher_sum_relations/`.
- **Unidad de análisis: el quipu** (1 quipu). Todos los controles se hacen por **permutación de los valores dentro del propio quipu** (se barajan los 398 valores >0 entre las 398 posiciones con nudo, 1000 repeticiones, semilla 0), que preserva la multitud de valores, la estructura de grupos y el número de cuerdas con nudo. p-valor empírico = (1 + #{nulo ≥ obs})/(1+B).
- Corrección por comparaciones múltiples: **Holm** sobre los 7 tests.
- Valores 0 sin nudos = ausente (no cero real), según el brief. No se usa el museo como lugar de origen.
- Cumplimiento del límite de contexto: sólo lecturas por `grep`/pandas con salida ≤ 40 líneas; fichas leídas completas: FitzPatrick 2026 y Thompson 2024 (2 de 4).

## 3. Estructura reconstruida

| Rasgo | Valor |
|---|---|
| Cuerdas totales | **1831** |
| Colgantes (nivel 0) | 1650 |
| Subsidiarias (nivel 1 / nivel 2) | 171 / 10 |
| Grupos (`grupo`) | **432** |
| Cuerdas **sin nudos** | **1433 (78,3 %)** |
| Cuerdas con nudos | **398 (21,7 %)** |
| Valor máx. / suma de valores | 585 / 13057 |
| Valores distintos (>0) | 92; **350 de 398 valores están repetidos** |
| Largo medio de cuerda | 36,5 cm (máx 53) |
| Torsión | **todas U** (desconocida) |
| Unión (`union`) | **1830 U + 1 Unknown → no hay cuerdas superiores (T) ni R/V registradas** |
| Terminación | K 1610, U 217, B 3, R 1 |
| Color | 1409 W puro; 422 coloreadas; **245 colores distintos** |
| Nudos (OKR) | 1011: S 643, L 281, E 74, **LL 13** |
| Dirección de nudo | **todas U** (sin información S/Z) |

**Grupos (la unidad de registro):** la distribución de tamaños es bimodal: **189 grupos de 1 cuerda**, **87 de 7**, **83 de 6**, y colas hasta 20 cuerdas (grupo 241 = 20; varios de 17–19). La primera cuerda de cada grupo (`pos_in=0`) está **coloreada en 219 de 432 grupos (50,7 %)** frente a 422/1831 (23,0 %) del total; el resto de la cuerda es blanca. La estructura fina es: **cuerda marcadora de color + bloque de 6–7 cuerdas blancas** que llevan los valores.

**Subsidiarias:** 137 cuerdas madre con hijas (100 con 1, 32 con 2, 3 con 3, 2 con 4). Los valores >0 se concentran en las posiciones 1 y 4 dentro del bloque (para grupos de 7: posiciones {1:50, 4:58, 2:15, 3:15, 5:20}).

**Nota KFG (relaciones de Ascher), todas ellas exactas (verificado: 100 % de coincidencia valor↔suma):**

| Relación | N |
|---|---|
| pendant–pendant sum | 200 |
| pendant–pendants por color | 263 |
| indexed pendant sum | 140 |
| subsidiary–pendant sum | 47 (+10 indexed subsidiary) |
| cluster–cluster sum | 16 |
| cluster sum bands | 5 |
| clusters *banded* / *seriated* | **235 (94 %) / 15 (6 %)** |
| decreasing clusters | 0 |

## 4. Aritmética interna y controles nulos

Nulo = barajar los valores >0 dentro del quipu (1000×, semilla 0). Holm sobre 7 tests (α=0,05).

| # | Patrón probado | Observado | Nulo (media) | p | Holm |
|---|---|---|---|---|---|
| A | madre = Σ subsidiarias (jerarquía directa) | 37 | 36,7 | **0,51** | no signif. |
| B | valor = Σ de ≥2 cuerdas **consecutivas del mismo índice** (grupo) | 37 | 24,5 | **0,005** | **sobrevive** |
| B' | ídem, sólo hacia delante | 39 | 24,6 | **0,006** | **sobrevive** |
| C2 | valor = subconjunto (cualquiera, ≥2) del mismo índice | 328/398 | 318,2 | 0,038 | **no sobrevive** |
| D | pares de grupos con suma igual | 198 | 129,5 | **0,003** | **sobrevive** |
| E1 | agrupamiento global del color (nº de *runs*) | 641 | 650,4 | 0,29 | no signif. |
| E2 | 1.ª cuerda del grupo coloreada | 219/432 | 99,6 esp. | **0,001** | **sobrevive** |

**Lectura de los tests.**
- **Positivo fuerte y controlado:** (i) la primera cuerda de cada grupo es un **marcador de color** (E2, p=0,001); (ii) las **sumas "indexadas"** —una cuerda con el mismo índice dentro del bloque suma ≥2 cuerdas de ese índice en otros bloques— superan al azar (B/B′, p≈0,005); (iii) los **totales de grupo se repiten** mucho más de lo esperado (D, p=0,003), típico de partidas que se vuelven a listar o cierran.
- El test genérico de "subconjunto cualquiera" (C2) es el menos informativo (casi todo número pequeño es expresable como suma de otros dos cuando hay 400 valores repetidos); su p=0,038 no sobrevive a Holm. Es una **advertencia metodológica**: las "relaciones de Ascher" abundantes de AS069 son fáciles de obtener por azar en un quipu grande; lo informativo es la **estructura** (índice/posición), no la mera existencia de una suma.

## 5. Estructura de color

- 422 cuerdas coloreadas (23 %), 245 colores distintos; el marcador de grupo usa una paleta amplia (183 colores distintos en las 219 primeras cuerdas coloreadas): dominan blanco-mixto y bandas superiores `W:XX(0.0-2.0)/W(...)` (258 cuerdas con banda de color en los primeros 2 cm).
- La **seriación/bandeo** es la norma: 94 % de los clusters son "banded". Esto es coherente con Clindaniel (2019), que halla que los quipus de **magnitud alta tienden a estar seriados** (regresión magnitud→seriación, p<0,01).
- **Negativo:** el color **no** se agrupa globalmente más allá del azar (E1, p=0,29); su regularidad es **posicional** (marca la cabecera del grupo), no un simple bloque contiguo.

## 6. Interpretación propuesta: filas y columnas

**Tipo de registro (nivel: propuesto).** AS069 es un **registro administrativo tabular de tipo censo/tributo (contable)**, no un calendario ni un texto glotográfico. Argumentos:
- Es un patrón de **marcador + bloque de valores**: cada grupo es una **fila** (una unidad: persona, familia, ayllu, partida o ítem) y cada cuerda del bloque es una **columna/campo** (magnitud), consistente con "columnas de 1000/100/10/1" descritas por Locke (1927) en quipus de 15 grupos × 6 cuerdas.
- Las **sumas indexadas** (mismo índice entre bloques) equivalen a **totales de columna / subtotales cruzados**, la firma de un libro de cuentas (Ascher & Ascher 1981; Medrano & Khosla 2024).
- La **repetición de totales de grupo** (D) sugiere que el registro **cierra/duplica** totales por sección.
- 94 % bandado y seriado, propio de registros grandes "de trabajo".
- El valle de Lluta/Arica (norte de Chile) es un **archivo local** del Horizonte Tardío/colonial temprano; Thompson (2024) describe precisamente una **fuerte conexión numérica entre dos quipus excavados juntos cerca de Arica, uno de ellos el mayor registrado** (AS069-071 fueron excavados juntos por Dauelsberg, 1965; AS069 = 1831 cuerdas, AS071 = 404). Esto sitúa a AS069 como el "quipu mayor" del caso de Thompson y refuerza la lectura de **registro maestro/resumen** con cordeles marcadores de color (nivel **apoyado con datos** para la existencia de las relaciones; **propuesto** para "censo/tributo").

**Filas = grupos** (cada marcador de color abre una unidad). **Columnas = posiciones de cuerda dentro del bloque** (índices 0..6), con la "columna 4" y la "columna 1" cargando los valores y operando como totales indexados. **Nivel de evidencia: propuesto** (estructura apoyada con datos; contenido semántico, especulativo).

## 7. Lo que no encaja / anomalías

- **78 % de las cuerdas no tiene nudo alguno.** En un registro "numérico" esto es enorme: la mayoría del objeto **no lleva número**. O bien las cuerdas vacías son posiciones "clave/plantilla" repetidas, o el contenido principal es **no numérico** (color/estructura/posición) y sólo algunas cuerdas son contables.
- **No hay cuerdas superiores (union T)**: las sumas detectadas por KFG se anclan a **colgantes**, no a cordones superiores (contra la intuición de Locke; coincide con Medrano & Khosla 2024, que hallan top cords minoritarios).
- **Torsión y dirección de nudo uniformes (todas U)**: no hay señal R/V ni S/Z → no se puede testear el código binario ni la dirección aquí (limitación del registro OKR/KFG).
- **Nudo `LL` (doble largo, x13)**: el diccionario OKR lo marca como "found in Dahlsberg khipu"; es una peculiaridad local del (=estos) quipus de Dauelsberg y un posible marcador no decimal.
- **Grupos grandes anómalos** (241 con 20 cuerdas; 37, 101 con 18; 193 con 17) rompen la plantilla de 6–7.
- **Corrección de datos:** Thompson (2025/2026) documenta errores de valor/tipo de nudo/color en datos heredados; Milillo et al. (2023) demuestran que el color observado puede no ser el original. Ambos elevan la incertidumbre de cualquier lectura de valor **y** de color en AS069.

## 8. Resultados negativos (explícitos)

- **NO** se cumple la suma jerárquica clásica **madre = Σ subsidiarias** (p=0,51). Las relaciones de AS069 son **entre colgantes/por índice**, no padre→hijo.
- **NO** hay agrupamiento global de color (p=0,29).
- **NO** hay "decreasing clusters" (0) ni patrones de "suma consecutiva" en orden de lectura puro: al probar valor = Σ de cuerdas **consecutivas no-nulas** en el orden global, observado = 0 y nulo = 0 (las sumas **no** son sobre bloques contiguos arbitrarios, sino **indexadas por posición en el bloque**). Este fue un resultado negativo clave para descartar un modelo de "total corrido".
- El test de subconjunto genérico no supera Holm → la mera existencia de sumas no es evidencia fuerte en un quipu grande.

## 9. Nivel de evidencia (resumen)

| Afirmación | Nivel |
|---|---|
| Estructura marcador(coloreado)+bloque(blanco); 78 % sin nudos; 432 grupos | **bien apoyado** (descriptivo) |
| La 1.ª cuerda del grupo es marcador de color | **apoyado con datos** (p=0,001 con nulo) |
| Sumas indexadas y repetición de totales de grupo superan el azar | **apoyado con datos** (p≈0,003–0,006, Holm) |
| Registro administrativo tabular tipo censo/tributo; filas=grupos, columnas=índices | **propuesto** |
| Conexión con el "quipu mayor de Arica" de Thompson (2024) | **propuesto** |
| Contenido no numérico en las 1433 cuerdas vacías / nudo LL | **especulativo** |

## 10. Para el coordinador

- **AS069 = KH0082**, 1831 cuerdas, 432 grupos (valle de Lluta, Arica; marco Dauelsberg 1965). Es, con diferencia, el mayor del corpus (el siguiente, UR093, tiene 1227).
- **No hay cuerdas superiores (union T) ni uniones R/V**: todo es colgante (1830 U + 1 ?). Torsión y dirección de nudo, todas U. No se puede testear el código binario R/V aquí.
- **78 % de las cuerdas no tiene nudos** (1433/1831). El contenido numérico está sólo en 398 cuerdas (valores repetidos: 350/398; máx 585).
- **Estructura probada:** cada grupo empieza con una **cuerda marcadora de color** (219/432; p=0,001 vs nulo de barajado) seguida de un bloque de 6–7 cuerdas blancas con los valores. 94 % de clusters "banded/seriated".
- **Aritmética probada con control:** las **sumas indexadas** (mismo índice entre bloques) y la **repetición de totales de grupo** superan al azar (p≈0,003–0,006; sobreviven Holm). La relación clásica **madre=Σ subsidiarias NO se cumple** (p=0,51): es un resultado negativo importante.
- **Advertencia metodológica:** probar "valor = suma de un subconjunto cualquiera" da 82 % de aciertos **también en el nulo** (p=0,038, no sobrevive Holm). En un quipu grande, "abundan sumas por azar"; lo que discrimina es la **estructura posicional**, no la suma suelta.
- **Interpretación propuesta:** registro **administrativo tabular (censo/tributo)**: filas = grupos (unidades marcadas por color), columnas = índices de posición dentro del bloque (con totales de columna indexados). **Propuesto**, no bien apoyado.
- **Contexto:** Thompson (2024, *Ñawpa Pacha*) describe una fuerte conexión numérica entre dos quipus excavados juntos cerca de Arica, uno el mayor registrado; **AS069 (1831) y AS071 (404) fueron excavados juntos por Dauelsberg**. Apoya un rol de "registro maestro/relacionado" (propuesto).
- **Siguiente ronda recomendada:** (1) replicar el test indexado con la estructura de clusters de 570 (KFG) que incluya subsidiarias, para cuantificar formalmente las 140 relaciones "indexed" y las 200 pendant–pendant con un nulo equivalente; (2) comparar AS069 con AS071 (conexión de Thompson) cordón a cordón; (3) auditar valor y color contra el examen físico (advertencias Thompson/Milillo) antes de cualquier lectura semántica; (4) probar si las 1433 cuerdas sin nudos codifican información **por posición/color** (no numérica).

---

### Scripts (en esta carpeta)
`explore1..6.py`, `resumen.py`, `tests_B.py`, `tests_ADE.py`, `tests_C2.py`, `tests_B_okr.py`, `verify_rels.py`, `null_runs.py`, `debug_sum*.py`. Nulos guardados en `nullB.npy`, `nullC2.npy`, `null_runs.npy`.
