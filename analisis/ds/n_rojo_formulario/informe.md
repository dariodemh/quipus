# Equipo ROJO — Ataque al «formulario local» y a los hallazgos del 18-10-2026

**Autor:** equipo rojo (modelo `formulario local`)
**Fecha:** 18-10-2026
**Semilla:** 20261018
**Carpeta:** `analisis/ds/n_rojo_formulario/`

---

## 1. Pregunta

¿Sobreviven a controles aburridos las cinco piezas que sostienen el modelo «formulario local»?

1. El color predice el valor dentro del quipu (167/403; «demostrado»).
2. No hay léxico de color compartido.
3. UR053A–E reparte W/R/AB en 4:1:1.
4. UR050 tiene 3 zonas a alturas fijas.
5. El emparejamiento 2+1+2+2+2 de UR278 explica 11 igualdades exactas.

La hipótesis roja de partida es que las cinco se explican, total o parcialmente, por (a) posición/orden dentro del grupo, (b) tamaño de la cuerda, (c) adyacencia física, (d) el propio formato decimal y (e) duplicación de datos (copias). Se buscó la explicación aburrida antes que la interesante (regla 7 del BRIEF).

## 2. Método

- **Datos:** `analisis/datos/cuerdas.csv` y `quipus.csv`; `analisis/13_sistema_incahuasi/ur278_tabla.csv`; `analisis/14_copias/filas_alineadas.csv`. No se regeneró ningún dato ni se tocó la base OKR.
- **Unidad:** el quipu. Todos los conteos de aciertos son por quipu (p. ej. «44 de 403 quipus»). Las pruebas dentro del quipu usan permutaciones *dentro* de cada quipu o residualización con efectos fijos de grupo, nunca permutaciones globales de cuerdas.
- **Color:** se quitaron los rangos en cm con `re.sub(r'\([^)]*\)','',s)`; no se normalizaron las combinaciones (`W:AB`, etc.), igual que en `20_categorias`.
- **Nulos:** permutación dentro de grupo/quipu para el color; para las zonas, comparación contra cuerdas decimales reales (no contra alturas uniformes); para los pares, comparación contra otros recortes contiguos.
- **Corrección múltiple:** BH-FDR dentro de cada familia (403 quipus × condición en el ataque 1; 2 pruebas en el ataque 4; 5 patrones en el ataque 5). Al final se aplica **Holm global sobre las 5 p-valores principales** (una por afirmación), que es la corrección exigida por el BRIEF.
- **Copias:** 43 quipus aparecen en familias de copia en `14_copias/filas_alineadas.csv`. Se analizó su efecto por separado.
- **Niveles:** demostrado / apoyado con datos / propuesto / especulativo.

## 3. Ataque 1 — «El color predice el valor en 167/403»

### Reproducción
Se replicó el pipeline de `categorias3.py` (colgantes nivel 0, ≥20 cuerdas, colores con ≥3 casos, η² sobre `log1p(valor)`):

| Condición | Quipus con q<0,05 | η² mediano |
|---|---|---|
| Barajado global (el «167») | 176/403 | 0,163 |
| Barajado dentro del grupo (el «103») | 108/403 | 0,163 |
| Residualizado sobre grupo + posición + posición² + nº de racimos + log(largo) | **44/403** | **0,052** |

El «167» es la prueba débil: barajar el color en todo el quipu deja intacto el efecto de grupo y de posición, que es precisamente lo que hay que controlar. El número defendible de partida es 103–108, no 167.

### Controles acumulados

| Filtro | Quipus | q<0,05 | Esperado al 5 % | p binomial |
|---|---|---|---|---|
| Residual + todas las cuerdas | 403 | 44 | 20,2 | 1,4e-6 |
| Residual + sin quipus con copias | 367 | 28 | 18,4 | 0,019 |
| Residual + sin cuerdas de total/máxima + sin copias | **317** | **19** | **15,9** | **0,24** |

- Las cuerdas «de total» (valor = suma del resto del grupo) y las máximas de cada grupo son 3 600 y 5 599 de las 41 357 cuerdas nivel 0 con color y valor. Al excluirlas, con el nulo dentro de grupo los aciertos bajan de 108 a 75 y el η² mediano de 0,163 a 0,159; con la residualización completa quedan 27/349 y η² 0,096. Es decir, buena parte del «color marca clase» es «las cuerdas grandes van en otro color».
- **11 de los 44 quipus que sobreviven a los controles son copias** (25 %, frente a 10,7 % de copias en el corpus). Las copias no son evidencia independiente: replican el mismo dato. Sin ellas quedan 28.
- La posición dentro del grupo no explica mucho *del color* (R² mediano color ~ posición + posición² = 0,065), pero sí explica el valor: por eso residualizar sobre posición elimina ~60 % de los aciertos. La lectura correcta es que **color y posición están confundidos**: el color marca bandas que coinciden con la deriva del valor a lo largo del grupo.
- El color que más pesa es W (mediana de valor 22 en los quipus con efecto, frente a 0–2 de KB/MB/B). Es consistente con «W = cuerda principal/total», no necesariamente con una categoría semántica.
- **Robustez (regla 6 del BRIEF):** 12 887 de las 41 357 cuerdas nivel 0 (31 %) tienen valor 0 y `nudos` vacío, es decir, son ausentes y no ceros reales. Excluyéndolas: 53/350 tras residual, 30/319 sin copias (p = 0,0008) y **19/268 sin totales ni copias (p = 0,082)**. La conclusión no cambia (el efecto se desvanece con todos los controles), aunque en esta variante queda más cerca del umbral.

**Veredicto:** el «demostrado» **no sobrevive**. Queda: (i) apoyado con datos que en un subconjunto de quipus el color se asocia al valor; (ii) **propuesto** que el color funcione como categoría semántica con clave local; (iii) demostrado que el «167» estaba inflado por el nulo global y que las copias inflan el apoyo aparente.

## 4. Ataque 2 — Potencia del negativo «no hay léxico compartido»

Se plantó un léxico de 4 colores (el mismo orden: W, MB, AB, B) en el 30 % y el 10 % de los quipus de **Pachacámac** (80 quipus, el sitio más favorable: cualquier otro sitio tiene menos potencia). Se midió la potencia de las dos pruebas del coordinador con 60 simulaciones y 100–150 permutaciones cada una.

| Prevalencia | Forma del plantado | Potencia P1 (orden de categorías) | Potencia P2 (secuencias de grupo) |
|---|---|---|---|
| 30 % | 4 bloques en orden fijo | **0,92** | 0,00 |
| 30 % | reordenar colores dentro de cada grupo | 0,017 | 0,00 |
| 30 % | idem + 30 % de ruido | 0,00 | 0,00 |
| 10 % | 4 bloques en orden fijo | 0,00 | 0,00 |
| 10 % | reordenar dentro de grupo | 0,00 | 0,00 |

- En el corpus real: P1 Δτ = 0,0068, p = 0,373 (replica el 0,007/0,34); P2 = 84 patrones compartidos, p = 1,0 (el coordinador reportó 48 frente a 50, p = 0,79; la diferencia es de definición de grupo, no de conclusión).
- **P1 tiene potencia aceptable solo contra un léxico fuerte y masivo** (30 % de los quipus del sitio con el mismo orden de 4 colores): 92 %. No tiene potencia contra un léxico que afecte al 10 % de los quipus (0 %) ni contra un léxico que solo ordene los colores dentro de cada grupo (1,7 %).
- **P2 tiene potencia cero incluso contra el plantado más fuerte.** El motivo es estructural: su nulo baraja los colores *dentro del grupo*, preservando la composición. Un léxico que se manifieste como «estos 4 colores van juntos en este grupo» produce exactamente la misma composición y el nulo lo reproduce. P2 solo puede detectar secuencias ordenadas repetidas cuando la composición no basta para explicarlas; no es una prueba de léxico compartido en general.

**Veredicto:** el negativo es **parcial**. «No hay un léxico fuerte, site-wide, que afecte a ≥30 % de los quipus del sitio» está **apoyado con datos**. «No hay léxico compartido» a secas es **especulativo**: las pruebas no tenían potencia para léxicos débiles, y P2 no podía detectar el caso más natural (composición compartida).

## 5. Ataque 3 — UR053A–E: ¿4:1:1 trivial?

### Estructura
Los tríos no son «tres cuerdas cualesquiera»: en UR053A/C/D son bloques contiguos W-R-AB; en UR053B/E el AB es **subsidiaria** de la cuerda roja. Es decir, el «trío» es una unidad de formato, no una coincidencia de color.

| Quipu | Tríos W-R-AB | W mayor | share W / R / AB (mediana) |
|---|---|---|---|
| UR053A | 14 | 13 | 0,68 / 0,19 / 0,12 |
| UR053B | 18 | 12 | 0,60 / 0,21 / 0,18 |
| UR053C | 20 | 14 | 0,65 / 0,18 / 0,17 |
| UR053D | 23 | 23 | 0,66 / 0,17 / 0,16 |
| UR053E | 35 | 35 | 0,62 / 0,18 / 0,19 |
| **Total** | **110** | **97 (88 %)** | **0,64 / 0,18 / 0,18** |

### Controles
- **Contra otros quipus con el mismo patrón W-R-AB:** solo hay **3 quipus** (UR197, UR208, UR232) y 17 tríos; W es el mayor en 3/17 (17,6 %). Fisher frente a UR053: p = 0,008; Mann-Whitney de share1: p < 1e-4. Pero el control está dominado por UR232 (Huacho), cuya estructura es otra (AB enorme), y n = 3 quipus es demasiado poco para generalizar.
- **Contra la explicación «W es la principal y R/AB subsidiarias o menores»:** en el corpus, la madre supera a su subsidiaria AB en 66,8 % de 1 694 pares. En UR053 solo en 41,5 % (la madre no supera al AB en el 58,5 % restante). Así que el orden W > AB no se explica por «principal > subsidiaria»; es una propiedad del formulario.
- **Contra pares W-R de nivel 0 en otros quipus:** W > R en **99/111 (89,2 %)** en UR053 frente a **55/136 (40,4 %)** en 32 quipus (Fisher bilateral p = 4,3e-16). Barajando el color dentro de cada quipu de UR053 (conservando valores): p = 0,0002. Este es el control decisivo: **el orden W > R no es trivial**.
- **El reparto 4:1:1 sí es menos impresionante de lo que parece:** el share1 medio de UR053 (0,746 sobre pares W-R) es solo el **percentil 78** de los 32 quipus con pares W-R (mediana 0,528; máximo 1,0), y R y AB son estadísticamente iguales (0,179 vs 0,179). No es «4:1:1»: es «W grande, R y AB pequeños e indistinguibles». La mediana de share1 en tríos contiguos genéricos es 0,33; la de UR053 es 0,64, pero con CV 0,11–0,31 dentro de cada quipu.

**Veredicto:** **parcial**. El orden W > {R, AB} está **apoyado con datos** y no es trivial (p = 4,3e-16). El «reparto 4:1:1» como proporción estable es **propuesto**: la proporción no es extrema frente a otros quipus con pares W-R, y R/AB no están ordenados. La comparación con otros archivos es débil por n = 3 quipus.

## 6. Ataque 4 — UR050: ¿3 zonas o cualquier cuerda de 3 racimos?

Se comparó UR050 con **62 quipus del corpus que tienen ≥20 cuerdas decimales normales con exactamente 3 racimos de nudos**, ajustando el mismo GMM de 3 componentes sobre alturas relativas (posición / largo).

| | UR050 | Controles (mediana) | Percentil de UR050 |
|---|---|---|---|
| Centros de banda | 0,204 / 0,418 / 0,755 | 0,20 / 0,43 / 0,67 | — |
| ΔBIC(1→3) por observación | 0,635 | −0,08 | 98,4 |
| Hueco mínimo entre centros / SD | 3,55 | 2,82 | 88,7 |
| Cuerdas de 3 racimos | 146 | 20–203 | — |

- **Cualquier cuerda con 3 racimos produce 3 bandas a alturas parecidas** (0,20/0,43/0,67). El nulo de «alturas uniformes» del análisis original es el nulo equivocado: compara contra una cuerda sin estructura decimal. Contra cuerdas reales, UR050 es el más apretado, pero no cualitativamente distinto.
- P empírica de UR050 dentro de los 62 controles: **0,032**; con **Holm sobre las 2 pruebas** (ΔBIC/n y hueco): **0,064, no significativo**.
- Lo que **sí** es no trivial es el formato: **las 146 cuerdas de UR050 con 3 racimos son todas `L,L,L`** (de 163 cuerdas del quipu), con dígitos 1–9 (mayoría 5–6). Una cuerda decimal normal solo puede tener **un** racimo de unidades; tres racimos largos en la misma cuerda no son un número decimal. Pero ese formato no es exclusivo de UR050: en el corpus hay 397 cuerdas `L,L,L` de 3 racimos en 33 quipus, y UR052/UR054/UR055/UR193 lo comparten (ΔBIC/n = −0,04 / 0,16 / −0,02 / 0,29). Es un formato de familia, no una invención de UR050.
- El dato de «los 3 dígitos son ≠ 0» no aporta: en las 4 231 cuerdas de 3 racimos del corpus, el 99,7 % tiene los 3 dígitos > 0, simplemente porque un dígito 0 no deja racimo.

**Veredicto:** **parcial**. «3 zonas a alturas fijas» como evidencia **no sobrevive**: es una propiedad genérica de las cuerdas de 3 racimos y no pasa Holm (0,064). Lo que sobrevive, **apoyado con datos**, es la descripción «tabla de 163 filas × 3 columnas de un dígito en notación de nudo largo», que ya estaba en la síntesis. La interpretación funcional (rebaño/reparto) sigue **especulativa**.

## 7. Ataque 5 — UR278: ¿cuánto del 2+1+2+2+2 es adyacencia?

Matriz de igualdades exactas de las 24 filas × 9 columnas:

- Objetivo (1-2)(4-5)(6-7)(8-9): **11**.
- Complemento adyacente (2-3)(3-4)(5-6)(7-8): **4**.
- Suma de las 8 parejas adyacentes: 15; con 4 adyacentes al azar se esperan **7,5**.
- **Los 5 recortes contiguos 2+1+2+2+2 posibles dan 6, 11, 10, 9 y 9.** El objetivo es el máximo de 5, pero por **1 igualdad** sobre el segundo (deja c5 suelta: 10) y por 2 sobre la mediana (9). Si los 5 recortes fueran equivalentes, la probabilidad de que el objetivo sea el máximo es 1/5 = **0,20**.
- En el corpus, la igualdad entre cuerdas adyacentes de un grupo es **1,40×** la de cuerdas no adyacentes (14,5 % vs 10,4 %, 139 153 pares). En UR278 es **2,3×** (7,8 % vs 3,4 %). Dos tercios del exceso de 11 ya están en la adyacencia: 4 parejas adyacentes al azar dan 7,5.
- El p = 0,003 frente a los 945 emparejamientos es correcto pero compara contra emparejamientos **no adyacentes** en su mayoría; no controla la adyacencia. El propio n_espinoza1963 ya reportó p = 0,086 como máximo sobre 945. El control correcto (5 recortes contiguos) da p = 0,20.

**Veredicto:** **no** para el patrón específico 2+1+2+2+2. **Sí** para el hecho más general, ya conocido, de que las columnas vecinas se parecen más de lo esperado (1,4× en el corpus, 2,3× en UR278). El «11» no debe presentarse como confirmación de la estructura documental de la Visita: cualquier recorte contiguo da 9–11.

## 8. Corrección múltiple global

Holm sobre las 5 p-valores principales (una por afirmación):

| Ataque | p principal | Holm ajustado | ¿Significativo? |
|---|---|---|---|
| 3. W>R UR053 | 4,3e-16 | 2,1e-15 | **sí** |
| 4. UR050 (ΔBIC/n) | 0,032 | 0,128 | no |
| 5. UR278 patrón contiguo | 0,20 | 0,60 | no |
| 1. Color con todos los controles | 0,241 | 0,60 | no |
| 2. Léxico P1 | 0,373 | 0,60 | no |

Solo el orden W > R de UR053 sobrevive a la corrección global. Esto no significa que las demás sean falsas, sino que **no alcanzan el umbral que el propio BRIEF exige para sostener una afirmación fuerte**.

## 9. Resultados negativos (explícitos)

1. El «167/403» no se sostiene: 103–108 con el nulo correcto, 44 tras controles, 19/317 (p = 0,24) sin totales ni copias; excluyendo además los ausentes (valor 0 sin nudos), 19/268 (p = 0,082).
2. El color pierde ~60 % de sus aciertos al controlar posición, nº de racimos y largo (108→44): color y posición están confundidos.
3. El 25 % de los quipus con efecto son copias; contarlas como evidencia independiente infla el resultado.
4. UR050 no se distingue de cuerdas decimales de 3 racimos (Holm 0,064); los centros de banda son casi idénticos (0,20/0,43/0,67).
5. UR278: el patrón específico no se distingue de otros recortes contiguos (p = 0,20); 7,5 de las 11 igualdades se esperan solo por adyacencia.
6. UR053: R y AB no están ordenados (R > AB en 9/14, 10/18, 11/20, 11/23, 12/35); el «4:1:1» es en realidad «4:1:1 con las dos partes pequeñas iguales».
7. Solo 3 quipus fuera de UR053 tienen el patrón W-R-AB; la comparación externa tiene n = 3.
8. P2 (secuencias de grupo) tiene potencia cero incluso contra un léxico plantado fuerte; su negativo no es informativo.
9. P1 no tiene potencia contra un léxico que afecte al 10 % de los quipus (0 %) ni contra uno intra-grupo (1,7 %).

## 10. Nivel de evidencia que asignaría

| Afirmación | Nivel original | Nivel rojo | Motivo |
|---|---|---|---|
| El color predice el valor en 167/403 | demostrado | **retirado** | nulo global + copias + totales |
| El color se asocia al valor en un subconjunto de quipus | — | **apoyado con datos** | 19/317 tras todos los controles (p=0,24; 19/268 y p=0,082 sin ausentes); señal débil pero no nula |
| El color es una categoría semántica con clave local | demostrado | **propuesto** | confundido con posición/tamaño; sin prueba independiente |
| No hay léxico de color compartido | demostrado (negativo) | **apoyado solo para léxico fuerte (≥30 %)**; **especulativo** para léxico débil | simulación de potencia |
| UR053: W > R/AB y formulario local | apoyado | **apoyado con datos** | p = 4,3e-16, permutación 0,0002 |
| UR053: reparto 4:1:1 estable | apoyado | **propuesto** | proporción no extrema (percentil 78); R≈AB; n=3 controles |
| UR050: 3 zonas a alturas fijas | apoyado (exploratorio) | **retirado como evidencia**; el formato de 3 racimos L sigue **apoyado** | control con cuerdas decimales; Holm 0,064 |
| UR050: tabla de 163×3 dígitos | apoyado | **apoyado con datos** | 146/146 cuerdas L,L,L, dígitos 1–9 |
| UR278: pares 2+1+2+2+2 confirman la Visita | apoyado, frágil | **especulativo** | máximo de 5 recortes contiguos, p=0,20 |
| UR278: exceso de igualdades entre columnas vecinas | ya conocido | **apoyado con datos** | 1,4× en el corpus, 2,3× en UR278 |
| Modelo «formulario local» en conjunto | apoyado | **propuesto** | pierde dos pilares (color «demostrado» y negativo de léxico) y conserva el formato de archivo |

## 11. Para el coordinador

- **El «167/403» no es el número que hay que defender.** Con el nulo correcto (barajar dentro del grupo) son 103–108; al controlar posición, nº de racimos y largo bajan a 44; al quitar totales/máximas y copias quedan **19 de 317 frente a 15,9 esperados (p = 0,24)**; excluyendo además los ausentes (31 % de las cuerdas nivel 0 son valor 0 sin nudos), **19 de 268 (p = 0,082)**. El «demostrado» del color como categoría hay que retirarlo.
- **La explicación aburrida del color es posición + tamaño.** El color W concentra las cuerdas grandes (mediana 22 frente a 0–2 de KB/MB/B), y el modelo con posición, nº de racimos y largo elimina ~60 % de los aciertos (108→44). Color y posición están confundidos; no se puede afirmar «categoría semántica» sin un diseño que los separe.
- **11 de los 44 quipus que sobreviven a los controles son copias** (25 %, frente a 10,7 % del corpus). Las copias replican el mismo dato: no son evidencia independiente. Contarlas infla el apoyo del modelo.
- **El negativo «no hay léxico compartido» tiene poca potencia.** P1 detecta un léxico fuerte (30 % de los quipus del sitio, 4 colores en orden fijo) con 92 %, pero baja a 0 % con el 10 % y a 1,7 % si el léxico solo ordena dentro del grupo. P2 tiene **0 % de potencia en todos los escenarios**, incluso el plantado fuerte, porque su nulo preserva la composición de colores. El negativo solo vale para léxicos fuertes y site-wide.
- **UR053 es el hallazgo que mejor sobrevive, pero no por el «4:1:1».** W > R en 99/111 (89 %) frente a 40 % en otros quipus (Fisher 4,3e-16; permutación 0,0002). Es el único resultado que pasa Holm global. Lo que no se sostiene es la proporción: R y AB son iguales (0,18/0,18) y el share1 de UR053 es solo el percentil 78 de otros quipus con pares W-R.
- **UR050: las «3 zonas» son el formato decimal, no un hallazgo.** Cualquier cuerda con 3 racimos tiene bandas en 0,20/0,43/0,67; UR050 da 0,20/0,42/0,75 y Holm = 0,064. Lo que sí es no trivial es que las 146 cuerdas tengan **tres racimos largos** (imposible en un número decimal), pero ese formato lo comparten UR052/054/055/193: es de familia, no de UR050.
- **UR278: el 2+1+2+2+2 no confirma la Visita.** Los cinco recortes contiguos posibles dan 6, 11, 10, 9 y 9: el objetivo es el máximo de 5 por una sola igualdad (p = 0,20). En UR278 las columnas vecinas son 2,3× más iguales que las no vecinas; 7,5 de las 11 igualdades se esperan solo por adyacencia. El exceso de igualdades vecinas es real, pero no discrimina el orden documental.
- **Recomendación 1:** rehacer el análisis de color con un diseño que separe color de posición (p. ej., cuerdas de la misma posición en grupos distintos, o modelos mixtos con pendiente de posición por quipu) y tratar las copias como estrato aparte: el efecto que reaparece en copias no debe sumarse al de quipus independientes.
- **Recomendación 2:** para el léxico, construir una prueba con potencia declarada (prevalencia mínima detectable, p. ej. 30 %) y no presentar los negativos de P1/P2 como ausencia de léxico. Un léxico intra-grupo es hoy indistinguible de la composición local.
- **Recomendación 3:** conservar del modelo «formulario local» solo lo que tiene control: el formato de archivo (bloques W-R-AB en UR053, tres racimos largos en UR050) y el orden W > R. Todo lo demás (color = clase, reparto 4:1:1, pares de la Visita) queda en **propuesto o especulativo**.

## 12. Reproducibilidad

| Script | Qué hace |
|---|---|
| `01_ataque_color.py` | Réplica de 167/103/44 con controles de posición, racimos y largo |
| `01b_copias.py` | Exclusión de quipus con copias |
| `01c_ausentes.py` | Robustez excluyendo valor 0 con `nudos` vacío (ausentes) |
| `02_potencia.py` | Simulación de léxico plantado y potencia de P1/P2 |
| `03_trios.py` | Tríos W-R-AB de UR053 frente a otros quipus |
| `03b_trios.py` | W>R, Fisher, permutación intra-quipu y percentil del share1 |
| `04_zonas.py` | UR050 frente a 62 quipus con cuerdas de 3 racimos |
| `05_ur278.py` | Matriz de igualdades, recortes contiguos y tasa de adyacencia |

Salidas: `color_controles.csv`, `color_sin_totales.csv`, `color_sin_ausentes.csv`, `potencia_lexico.csv`, `trios_reparto.csv`, `zonas_control.csv`, `ur278_control.csv`, `ataques.csv`.
