# ¿Qué son las cuerdas sin nudos del corpus KFG?

**Equipo:** `t_cuerdas_vacias` · **Fecha:** 18/10/2026 · **Datos:** KFG (`analisis/datos/cuerdas.csv`, 57 818 cuerdas, 651 quipus) y control OKR (`khipu.db`).

---

## 1. Pregunta

El 30,5 % de las cuerdas del KFG no tiene ningún nudo. ¿Son cuerdas rotas/cortadas, marcadores de posición, ceros, separadores de grupo o etiquetas codificadas por color? La tarea pide, además, distinguir las cuerdas cortadas de las cuerdas completas sin nudos y comparar posición en el grupo (primera/última), color, unión y largo frente a las cuerdas con nudos, con un nulo explícito por permutación dentro de quipu.

## 2. Datos y definiciones

- **Unidad de inferencia:** el quipu (651). Los tests a nivel de cuerda se hacen permutando dentro de cada quipu; nunca se tratan 57 818 cuerdas como independientes.
- **Sin nudos:** `nudos` vacío. En el KFG, `valor = 0` con `nudos` vacío significa **ausente**, no un cero real (regla del BRIEF). No se usa `valor` como evidencia de cero.
- **Terminación** (diccionario OKR `termination_dc`): `K` = knotted (extremo con nudo terminal; cuerda completa), `B` = broken (rota), `C` = cut (cortada), `U` = unfinished (sin nudo terminal, no rota ni cortada), `R` = ravelled (deshilachada), `D` = doubled (doblada).
- **Subconjunto limpio principal:** cuerdas de nivel 0 (colgantes), terminación `K` y largo > 0. Así se comparan cuerdas completas con cuerdas completas, sin contaminar con fragmentos ni con marcadores de largo 0. n = 27 464; 7 022 sin nudos (25,6 %).
- **Marcadores de largo 0:** 1 480 cuerdas sin nudos con `largo = 0` (8,4 % de las vacías). Se analizan aparte; no se usan en las comparaciones de largo. Algunas notas las describen explícitamente como “marker”, “attachment point” o “nudo en el cordón principal”; otras son simplemente cuerdas sin largo medible.
- **Rotas/cortadas:** `B` o `C`. **Completas sin nudos:** `K`, `U`, `R` o `D` con largo > 0.

## 3. Método estadístico

1. **Nulo por permutación dentro de quipu.** Para una variable binaria (sin nudos sí/no) o continua (largo), se reasigna dentro de cada quipu, preservando el número de cuerdas vacías por quipu y el tamaño de cada quipu. 5 000 permutaciones, semilla 20261017. El p mínimo resoluble es 1/5 001 ≈ 0,0002; se reporta como `p < 0,0002`.
2. **Estimador de efectos fijos por quipu.** Para cada quipu con cuerdas vacías y no vacías: `d_i = media(y | vacía) − media(y | no vacía)`, peso `w_i = n1·n0/n`. El efecto principal es `Σ w_i d_i / Σ w_i`; se reportan también el promedio simple por quipu y el pooling de cuerdas. Esta tripleta es importante porque hay **paradojas de Simpson** (véase §5.4).
3. **Test exacto para grupos con una sola cuerda vacía.** Si la vacía se colocara al azar dentro de un grupo de tamaño `n`, `P(última) = 1/n`. Se compara el número observado con la suma de Bernoulli (Poisson-binomial) y se calcula z y p normal. Este test no depende de 5 000 permutaciones y es el más limpio para la hipótesis “marcador final”.
4. **Test estratificado de color/unión.** Para cada categoría `c`: `O_c` observado vs `E_c` esperado con los márgenes de cada quipu; estadístico global `Σ (O−E)²/V`; p por permutación dentro de quipu; p y q BH-FDR por categoría. Se repitió con estratos `quipu × unión`, `quipu × color` y `quipu × posición final` para separar efectos.
5. **Corrección múltiple.** Holm sobre 14 pruebas principales; BH-FDR sobre las categorías de color (16) y unión (3). Se indica en las tablas.
6. **Control cruzado OKR.** Para 596 quipus emparejados por KH/nombre, se contó en OKR las cuerdas con cero `knot_cluster` y se comparó con el conteo KFG de cuerdas sin nudos.

## 4. Resultados

### 4.1 Taxonomía: no es un fenómeno único

| Categoría | n | % de las 17 656 vacías | Largo mediano |
|---|---:|---:|---:|
| Rotas/cortadas (`B`/`C`, largo > 0) | 4 549 | 25,8 % | 6,0 cm |
| Completas sin nudos (`K`/`U`/`R`/`D`, largo > 0) | 11 487 | 65,1 % | 35,0 cm |
| Largo 0 (marcador/indeterminada) | 1 480 | 8,4 % | 0 cm |
| Otras / largo ausente | 140 | 0,8 % | — |
| **Total** | **17 656** | **100 %** | |

Desglose por terminación: `K` 9 422 (53,4 % de las vacías), `B` 5 174 (29,3 %), `U` 2 101 (11,9 %), `R` 512 (2,9 %), `C` 6, `D` 7, sin dato 405. La tasa de vacuidad no es uniforme: **25,2 % de las `K`** están vacías, **25,8 % de las `U`**, **23,2 % de las `R`**, pero **55,3 % de las `B`** y **85,7 % de las `C`**. Es decir, las cuerdas rotas tienen más del doble de probabilidad de no tener nudos que las completas; eso es lo esperable si la rotura se lleva parte de la cuerda y/o de los nudos.

**Largo.** Las rotas vacías son fragmentos: mediana 6,0 cm (IQR 1,5–13,5) frente a 21,5 cm de las `B` con nudos y 32,5 cm de todas las cuerdas con nudos. Dentro de quipu, una cuerda rota vacía es **−11,5 cm** más corta que una rota con nudos (w; p < 0,0002; pooling −13,6 cm). En cambio, una `K` vacía con largo > 0 mide **+3,9 cm** más que una `K` con nudos dentro del mismo quipu (IC95 % +3,2 a +4,6; p < 0,0002). El pooling de cuerdas da +1,1 cm y p ≈ 1,0 (no significativo), otra vez por mezcla de tamaños de quipu; el efecto dentro de quipu es pequeño pero consistente.

**Prevalencia por quipu.** 544/651 quipus (83,6 %) tienen al menos una cuerda vacía; **10 quipus (1,5 %) están completamente vacíos**. La fracción vacía por quipu tiene mediana 17,9 % (IQR 6,7–33,3 %). Los 10 quipus 100 % vacíos son AS025, HP025, HP026, HP028, HP048, QU001, UR070, UR071, UR082 y UR158; tienen largos y diversidad de color normales (p. ej. UR071: 26 cuerdas, 21 colores), no son simples “cuerdas sueltas”. El KFG ya reportaba 14/650 quipus sin nudos (2 %), cifra compatible.

### 4.2 Control cruzado: las vacías son reales, no un artefacto del KFG

En los 596 quipus emparejados con OKR, el número de cuerdas sin nudos del KFG correlaciona **Spearman 0,991** (Pearson 0,998) con el número de cuerdas OKR sin ningún `knot_cluster`; la diferencia absoluta mediana es **0** y el 98,7 % de los quipus está a menos de 5 puntos porcentuales. Los 10 quipus 100 % vacíos coinciden exactamente con OKR (salvo QU001, sin equivalente OKR). Esto **demuestra** que el fenómeno no es un fallo de codificación del KFG, aunque ambas bases comparten parte de la herencia KDB y no son plenamente independientes.

### 4.3 Posición: la vacía aislada tiende a ser la última del grupo

Proporciones brutas (K, nivel 0, largo > 0): primera 24,9 %, intermedia 25,6 %, última 26,2 %. La diferencia bruta es pequeña porque muchos grupos tienen varias vacías. El patrón se ve mucho mejor restringiendo a **grupos con exactamente una cuerda vacía**:

| Posición de la única vacía | Observado | Esperado al azar | z | p |
|---|---:|---:|---:|---:|
| Última (n ≥ 2; 663 grupos) | **255 (38,5 %)** | 173,9 (26,2 %) | **7,58** | **3,4×10⁻¹⁴** |
| Primera (n ≥ 2; 663 grupos) | 163 (24,6 %) | 173,9 (26,2 %) | −1,02 | 0,31 |
| Última, sólo n ≥ 3 (522 grupos) | **179 (34,3 %)** | 103,4 (19,8 %) | **8,50** | <10⁻¹⁵ |
| Última, sólo n ≥ 4 (421 grupos) | **138 (32,8 %)** | 69,8 (16,6 %) | **9,07** | <10⁻¹⁵ |

El efecto no es un artefacto de los grupos de tamaño 2: crece al exigir n ≥ 3 y n ≥ 4. Con el estimador de efectos fijos, la probabilidad de estar vacía es **+5,31 pp** mayor en la última posición que en el resto (IC95 % +2,86 a +7,88; p < 0,0002); el promedio simple por quipu da +5,15 pp (p < 0,0002) y el pooling +2,63 pp (p = 0,069). La primera posición **no** muestra un efecto robusto: +1,27 pp ponderado (p = 0,019), pero promedio simple no significativo y pooling negativo; el test exacto da 24,6 % vs 26,2 % (p = 0,31). **Resultado negativo: no hay “marcador de inicio”.**

Otras posiciones: las cuerdas vacías están sobrerrepresentadas en **grupos de una sola cuerda** (+9,5 pp; 32,3 % vs 25,6 % bruto; p < 0,0002) y, dentro de quipu, en grupos algo más pequeños (**−0,75 cuerdas** de tamaño; p < 0,0002). El pooling de cuerdas da +1,06 cuerdas y no significativo; la relación no es monótona (grupos de 2–4: ~20 %; 5–9: 27,6 %; 10–19: 31,0 %; ≥20: 18,0 %). No se debe hablar de una relación limpia con el tamaño.

**Primer/último grupo del quipu.** El primer grupo tiene menos vacías que el resto (w −2,9 pp; pooling −11,7 pp; p < 0,0002). El último grupo es ambiguo: w +5,3 pp (p < 0,0002), promedio simple +9,4 pp, pero pooling −5,8 pp (p = 1,0). Es un caso de Simpson; **no concluyente**.

### 4.4 Agrupamiento: hay “grupos en blanco”, no solo cuerdas sueltas

Con K, nivel 0, largo > 0:

| Contraste | Observado | Nulo (permutación dentro de quipu) | p |
|---|---:|---:|---:|
| Grupos sin ningún colgante K anudado (n ≥ 2) | **462** (8,1 % de 5 673 grupos) | 227,0 ± 8,5 | <0,0002 |
| Concentración de vacías por grupo (Σ residual², n ≥ 3) | **9 323,8** | 2 620,4 ± 109,6 | <0,0002 |
| Pares adyacentes vacíos dentro de grupo | **3 807** | 2 926,4 ± 25,1 | <0,0002 |

El exceso de grupos sin ningún colgante K anudado es casi el doble del esperado. De esos 462 grupos, **378 no tienen nudos en ningún nivel** (ni colgantes ni subsidiarias); 84 conservan nudos en alguna subsidiaria y 38 en algún colgante no-K (categorías solapadas). No lo explican los 10 quipus 100 % vacíos (sin ellos: 418 vs 182,8; p < 0,0002) ni los 5 quipus con más vacías (sin ellos: 295 vs 137,8; p < 0,0002). Distribución de las 7 022 vacías `K`: **43,2 % en grupos sin ningún colgante K anudado** (31,2 % del total en grupos sin ningún nudo en ningún nivel), 9,4 % como única vacía del grupo, 47,4 % en grupos mixtos con varias vacías. Los grupos sin ningún colgante K anudado tienen mediana de 5 cuerdas (vs 3 en los demás), 50,0 % de cuerdas blancas (vs 43,9 %), y el 36 % tiene otro grupo sin ningún colgante K anudado adyacente (294 rachas; longitud media 1,57; máxima 12). No están más cerca del inicio del quipu (5,2 % son el primer grupo vs 11,3 % de los demás) ni del final (11,5 % vs 10,7 %).

**¿Separadores?** El agrupamiento es real, pero no encontré evidencia de que el espaciado los marque como separadores: los grupos que terminan en vacía no tienen mayor espacio asociado (mediana 0,5 cm vs 1,0 cm tanto en su propio `espacio_cm` como en el del grupo siguiente; la diferencia media por quipu es +4,5 cm pero la mediana es 0 y hay 112 quipus positivos vs 119 negativos, dominada por outliers). La hipótesis de “separador entre grupos” queda **no apoyada** como mecanismo general; la de “bloques en blanco” sí está apoyada.

### 4.5 Color: asociación real pero modesta; el gran efecto de PK era un artefacto

Antes de separar los marcadores de largo 0, el color mostraba un efecto enorme: PK con 99 vacías vs 36,4 esperadas (z = 14,0). Pero **91 de las 99 PK vacías tenían largo 0**. Al excluir `largo = 0`, PK baja a 58 cuerdas, 13,8 % vacías, efecto w −7,5 pp (p = 0,22): **el “color PK = vacío” desaparece**. Es el mejor ejemplo de explicación aburrida antes de la interesante.

Con K, nivel 0, largo > 0, el test global de color sigue siendo significativo (p < 0,0002), pero las categorías que sobreviven a los controles y a BH-FDR son pocas y de efecto moderado:

| Color | n | % vacías | Efecto w (pp) | IC95 % bootstrap | p (w) | Quipus con contraste |
|---|---:|---:|---:|---:|---:|---:|
| B | 1 588 | 24,2 | **+7,0** | +0,8 a +13,1 | <0,0002 | 84 |
| RB | 356 | 9,6 | **−8,7** | −11,7 a −5,1 | <0,0002 | 38 |
| DB | 362 | 27,6 | **−13,6** | −29,8 a −0,3 | <0,0002 | 32 |
| LB | 478 | 30,1 | **+6,0** | −0,5 a +12,7 | 0,0058 | 50 |
| GG | 353 | 27,2 | **+6,3** | — | 0,0036 | 85 |
| LG | 144 | 25,0 | **+11,1** | — | 0,0024 | 23 |

BH-FDR sobre 16 colores deja estos seis con q < 0,05; W, AB, MB, YB, KB, PK, BB, HB y CB no son robustos. En particular, **W no es un marcador de vacío**: promedio simple −2,7 pp (p = 0,002) pero ponderado −0,8 pp (p = 0,13) y pooling +2,7 pp (p = 0,95). La idea de “cuerdas blancas = límites/vacíos” no se sostiene como efecto general. Tampoco hay evidencia de “etiqueta por color único”: la probabilidad de tener un color único en el grupo es 17,8 % en vacías vs 19,8 % en no vacías; el efecto ponderado +2,5 pp pero el pooling −2,1 pp y el promedio simple +7,2 pp, señales incompatibles. **No hay un patrón simple de etiqueta cromática.**

Los efectos de color sobreviven a controlar unión (B, RB, DB, LG, GG) y a controlar posición final (B +7,4; RB −7,8; DB −14,4; LB +6,0; GG +6,8; LG +12,0 pp; p ≤ 0,008). Son asociaciones independientes de esos dos factores, pero de tamaño pequeño y apoyadas en 23–85 quipus según el color.

### 4.6 Unión: las vacías se asocian sobre todo con unión “U” (desconocida)

| Unión | n | % vacías | Efecto w vs resto | IC95 % | p |
|---|---:|---:|---:|---:|---:|
| R (recto) | 10 236 | 21,2 | −2,8 pp | — | 0,0098 |
| V (verso) | 9 085 | 22,6 | +0,5 pp | — | 0,63 |
| U (desconocida) | 8 048 | **34,7** | **+16,6 pp** | +4,9 a +27,0 | <0,0002 |
| Unknown (distinto de U) | 88 | 1,1 | — | — | — |

El efecto está concentrado en `U` (34,7 % de vacías), no en `Unknown` (1,1 %). En 70 quipus con contraste, la asociación es fuerte y sobrevive a controlar color (+14,2 pp; p < 0,0002; promedio simple +5,9 pp, p = 0,115) y posición final (+12,7 pp; p < 0,0002). Interpretación: o las cuerdas vacías se fijan de una manera que el registro no puede clasificar como R/V (por ejemplo, sueltas o no estándar), o el registrador no anotó la dirección de unión cuando no había nudos. Ambas bases (KFG y OKR) usan `U`, así que no es solo un hueco del KFG, pero la independencia es limitada. **No se puede decidir entre explicación física y sesgo de registro con estos datos.**

### 4.7 Subsidiarias

En cuerdas `K` de nivel ≥ 1, la primera hermana tiene +2,9 pp de probabilidad de estar vacía (p = 0,0024), pero el pooling es negativo (−11,1 pp) y la última hermana no muestra efecto robusto (−1,9 pp; p = 0,062). El color de la hija coincide con el de la madre un +4,8 pp más entre las vacías (p = 0,035; marginal tras Holm). Son efectos débiles y direccionalmente inestables; **no los considero apoyados**.

## 5. Controles, corrección múltiple y resultados negativos

### 5.1 Familia principal y Holm

| Prueba | p | Holm |
|---|---:|---:|
| Última posición (w) | 0,0002 | 0,0028 |
| Primera posición (w) | 0,0190 | 0,0380 |
| Grupo de 1 cuerda | 0,0002 | 0,0028 |
| Tamaño de grupo (w) | 0,0002 | 0,0028 |
| Grupos sin colgante K anudado | 0,0002 | 0,0028 |
| Adyacencia de vacías | 0,0002 | 0,0028 |
| Color global | 0,0002 | 0,0028 |
| Unión global | 0,0002 | 0,0028 |
| Largo K (w) | 0,0002 | 0,0028 |
| Largo rotas (w) | 0,0002 | 0,0028 |
| Primera hermana | 0,0024 | 0,0072 |
| Color hija = madre | 0,0352 | 0,0380 |
| Primer grupo del quipu | 0,0002 | 0,0028 |
| Último grupo del quipu | 0,0002 | 0,0028 |

Todo sobrevive Holm < 0,05, pero varias pruebas tienen estimadores no robustos entre ponderado/simple/pooling (primera posición, último grupo, primera hermana, color hija=madre). La significación estadística no las convierte en hallazgos sólidos.

### 5.2 Sensibilidad

- Excluyendo los 5 quipus con más vacías (AS069, UR093, UR231, UR1057, UR006): última posición +4,57 pp (p < 0,0002); color global p < 0,0002.
- Excluyendo los 11 quipus con >500 cuerdas: última posición +4,80 pp (p < 0,0002); color global p < 0,0002.
- Excluyendo los 10 quipus 100 % vacíos: grupos sin colgante K anudado 418 vs 182,8 (p < 0,0002); concentración y adyacencia siguen p < 0,0002.

### 5.3 Resultados negativos

- **No hay marcador de inicio:** primera posición no robusta; test exacto 24,6 % vs 26,2 % (p = 0,31).
- **No hay “blanco = vacío”:** W no robusto; el efecto bruto de PK era un artefacto de los marcadores de largo 0.
- **No hay etiqueta por color único:** señales incompatibles entre estimadores; 17,8 % vs 19,8 % bruto.
- **No hay separador por espaciado:** los grupos que terminan en vacía no tienen mayor espacio asociado; mediana 0,5 vs 1,0 cm en su `espacio_cm` y en el del grupo siguiente.
- **No hay diferencia de largo en el pooling:** K vacías +1,1 cm, p ≈ 1,0; sólo el estimador dentro de quipu es positivo (+3,9 cm).
- **Las rotas vacías no están al final:** el efecto “última” para `B` es −0,8 pp (p = 0,54); de hecho están menos en la primera posición (−4,0 pp, p = 0,0024). Eso apoya que son fragmentos, no marcadores.
- **El último grupo del quipu es ambiguo** (Simpson: w +5,3 pp, pooling −5,8 pp).
- **Subsidiarias:** efectos pequeños y direccionalmente inestables.
- **Ceros:** el KFG no permite distinguir “cero” de “ausente” en una cuerda entera; el patrón de posición final, grupos vacíos y unión U no es el de ceros numéricos aleatorios. No se puede descartar que una minoría sean ausencias/ceros, pero no como explicación general.

### 5.4 Paradojas de Simpson que hay que declarar

En varias variables el estimador dentro de quipu y el pooling de cuerdas discrepan:
- Largo K: +3,9 cm (w) vs +1,1 cm (pooling, p ≈ 1,0).
- Tamaño de grupo: −0,75 cuerdas (w) vs +1,06 (pooling, p ≈ 1,0).
- Último grupo: +5,3 pp (w) vs −5,8 pp (pooling).
- Color DB: −13,6 pp (w) vs +2,1 pp (pooling).
Esto ocurre porque los quipus grandes tienen composiciones y prevalencias muy distintas. Doy prioridad al estimador dentro de quipu (unidad = quipu), pero reporto las tres versiones para que el coordinador vea la fragilidad.

### 5.5 Controles cruzados color ↔ unión ↔ posición

- Color controlando unión (sólo R/V): global p < 0,0002; B, RB, DB, LG, GG siguen.
- Unión controlando color (colores frecuentes): global p < 0,0002; `U` sigue (z = 9,8; q = 0,0008).
- Color controlando posición final: B, RB, DB, LB, GG, LG siguen (p ≤ 0,008).
- Posición final controlando color: +4,5 pp (p < 0,0002); controlando unión: +4,9 pp (p < 0,0002).
Son señales parcialmente independientes, no una sola variable oculta.

## 6. Interpretación y nivel de evidencia

### Bien apoyado (descriptivo, corpus completo + control cruzado)

1. **30,5 % de las cuerdas no tiene nudos**, y el fenómeno es real: OKR coincide con KFG (Spearman 0,991; mediana de diferencia 0; 98,7 % de quipus a <5 pp).
2. **No es un solo tipo de cuerda:** 25,8 % son rotas/cortadas (fragmentos cortos, mediana 6 cm), 65,1 % son completas sin nudos (largo comparable a las anudadas) y 8,4 % son de largo 0 (marcadores/indeterminadas).
3. **Las rotas vacías son fragmentos:** −11,5 cm dentro de quipu frente a rotas con nudos; 55,3 % de las `B` están vacías vs 25,2 % de las `K`.
4. **10 quipus (1,5 %) están completamente vacíos** y coinciden con OKR; no son un artefacto de una sola base.

### Apoyado con datos (nulo explícito, corrección múltiple, sensibilidad)

1. **Las completas vacías no son aleatorias en la estructura:** la vacía aislada es la última del grupo mucho más de lo esperado (38,5 % vs 26,2 %; p = 3,4×10⁻¹⁴; n ≥ 3: 34,3 % vs 19,8 %), y están sobrerrepresentadas en grupos de 1 cuerda y en grupos sin ningún colgante K anudado (462 vs 227; p < 0,0002; 378 de esos 462 no tienen nudos en ningún nivel).
2. **El agrupamiento no lo explican los quipus extremos:** sobrevive al excluir los 10 quipus 100 % vacíos y los 5 mayores.
3. **Hay asociación de color y unión:** B +7,0 pp, RB −8,7, DB −13,6, LB +6,0, GG +6,3, LG +11,1 (BH q < 0,05); U +16,6 pp. Son efectos moderados, no un código de color simple.
4. **El largo de las completas vacías es ligeramente mayor dentro de quipu** (+3,9 cm; IC95 % +3,2 a +4,6), pero no en el pooling.

### Propuesto (interpretación razonable, no probada)

1. **Dos patrones coexistentes:** (a) una cuerda vacía aislada al final de un grupo, compatible con una cuerda de cierre/relleno/placeholder o con una posición reservada; (b) bloques de grupos sin ningún colgante K anudado, compatibles con secciones no registradas, un quipu preparado/inacabado o un registro deliberadamente “en blanco”. Locke (1927) ya describió grupos K–N “sin nudos o fragmentarios” y propuso un quipu “inacabado” o “preparado con exceso de cuerdas”; el patrón actual es compatible con esa lectura, pero no la demuestra.
2. **El color y la unión marcan estatus/categoría de la cuerda** (no simple etiqueta): ciertos colores y la unión U cambian la probabilidad de estar vacía. La dirección causal (color → vacío, vacío → registro de unión, o ambos por una tercera variable) no se puede separar.
3. **La unión U puede ser una mezcla de fijación no estándar y sesgo de registro.** Habría que verla en OKR/fotografías.

### Especulativo (sin apoyo suficiente)

1. **“Ceros”**: no hay evidencia de que las cuerdas vacías sean ceros numéricos; el KFG las trata como ausentes y el patrón estructural (final de grupo, grupos vacíos) no es el de ceros aleatorios. Una minoría podría ser ausencia/cero, pero no es la explicación general.
2. **“Separadores”**: hay agrupamiento, pero no hay evidencia de que el espaciado o la posición entre grupos los marque como separadores. “Bloques en blanco” está mejor apoyado que “separador”.
3. **“Etiquetas por color”**: no hay un patrón simple de color único ni de color modal; las asociaciones son modestas y heterogéneas.
4. **“Quipu no numérico tipo Collata”**: los 10 quipus 100 % vacíos tienen color y largo normales, pero no el sistema complejo de color/fibra/torsión de Collata; no se puede afirmar que sean del mismo género.

## 7. Limitaciones

- KFG y OKR comparten herencia KDB; la concordancia es alta pero no es una replicación independiente.
- El color registrado a ojo puede no corresponder al original (Milillo et al. 2023); los efectos de color son los más frágiles.
- La definición de “grupo” depende del espaciado del KFG; una cuerda de cierre podría haber sido asignada al grupo anterior. Eso afecta la interpretación de “última”, no la existencia del patrón.
- `largo = 0` mezcla marcadores físicos, puntos de atadura y largos no medidos; no es una categoría homogénea.
- 651 quipus no son una muestra aleatoria (sesgos de colección y conservación).
- No se analizaron fibra, torsión, ply ni dimensiones físicas; podrían explicar parte del color/unión.
- Los p-valores de 0,0002 son el mínimo resoluble con 5 000 permutaciones; los verdaderos pueden ser menores. Los tamaños de efecto son pequeños en varios casos.

## 8. Para el coordinador

- **El 30,5 % de las cuerdas (17 656/57 818) no tiene nudos, pero no es un solo fenómeno:** 29,3 % son rotas/cortadas (fragmentos cortos), 65,1 % son completas sin nudos y 8,4 % son de largo 0 (marcadores/indeterminadas). No mezclar estas categorías en futuros análisis.
- **Las rotas vacías son fragmentos:** miden −11,5 cm dentro de quipu frente a rotas con nudos y no están al final de los grupos. No son marcadores.
- **Las completas vacías son reales (OKR r = 0,991) y están estructuradas:** la vacía aislada es la última del grupo en 38,5 % de los casos vs 26,2 % esperado (p = 3,4×10⁻¹⁴); con n ≥ 3, 34,3 % vs 19,8 %. También abundan en grupos de 1 cuerda y en grupos sin ningún colgante K anudado.
- **Hay 462 grupos sin ningún colgante K anudado (8,1 %) frente a 227 esperados (p < 0,0002),** 378 de ellos sin ningún nudo en ningún nivel; el 43 % de las vacías K está en esos grupos (31 % en los 378 totalmente vacíos). El efecto sobrevive a excluir los 10 quipus 100 % vacíos y los 5 quipus más vacíos.
- **Mejor interpretación:** dos patrones, (a) cuerdas de cierre/placeholder al final de grupos y (b) bloques/grupos en blanco compatibles con secciones no registradas o un quipu preparado/inacabado (Locke 1927 ya lo propuso). No es un cero numérico general ni un separador marcado por espaciado.
- **Color:** el enorme efecto de PK (99 vs 36 esperadas) era un artefacto: 91/99 PK vacías tenían largo 0. Tras excluirlas, quedan efectos modestos: B +7,0 pp, RB −8,7, DB −13,6, LB +6,0, GG +6,3, LG +11,1 (BH q < 0,05). W y AB no son marcadores; no hay etiqueta por color simple.
- **Unión:** las vacías tienen unión U (desconocida) en 34,7 % vs 21–23 % en R/V; +16,6 pp (IC95 % +4,9 a +27,0). Puede ser fijación no estándar o sesgo de registro; hay que verificarlo en OKR/fotos.
- **Próximos pasos recomendados:** (1) inspeccionar en OKR/fotografías las cuerdas finales vacías y su unión; (2) comparar KFG vs OKR cord a cord en una muestra; (3) analizar los 10 quipus 100 % vacíos como categoría propia; (4) añadir fibra/torsión/ply; (5) probar si las vacías finales se relacionan con sumas o con el cierre de series; (6) separar siempre `largo = 0` y `B/C` antes de cualquier modelo de color o posición.
- **Nivel de evidencia:** bien apoyado el conteo y la taxonomía; apoyado con datos el patrón de posición final, el agrupamiento, el largo de completas y las asociaciones de color/unión; propuesto el rol de cierre/placeholder y los bloques inacabados; especulativo el cero, el separador y la etiqueta por color.

---

## Anexo: scripts y tablas

- `01_descriptivo.py` → `tablas_01.csv`, `tab_terminacion.csv`, `tab_nivel.csv`, `tab_por_quipu.csv`, `tab_cruce_okr.csv`.
- `02_permutaciones.py` → `resultados_perm.csv`, `color_perm.csv`, `union_perm.csv`.
- `03_robustez.py` → `resultados_robustez.csv`, `color_perm_Lpositivo.csv`, `union_perm_Lpositivo.csv`.
- `04_controles.py` → `resultados_controles.csv`.
- `05_color_union_pareado.py` → `color_union_pareado.csv`.
- `06_bootstrap.py` → `bootstrap_ic.csv`.
- Semilla global 20261017; 5 000 permutaciones; Python 3.13, pandas/numpy.
