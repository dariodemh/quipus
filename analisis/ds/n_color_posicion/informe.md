# Color y posición en los quipus: ¿lleva el color información sobre el valor independiente de la posición?

**Carpeta:** `analisis/ds/n_color_posicion/`
**Semilla:** 20261018
**Fecha:** 18-10-2026
**Datos:** `analisis/datos/cuerdas.csv`, `quipus.csv`, `grupos.csv`; copias de `analisis/14_copias/filas_alineadas.csv`. La base OKR se usó solo para lectura (no se creó ni modificó ningún `khipu.db`).

---

## 0. Resumen

El equipo rojo mostró que el «167/403» cae a 19/317 (p = 0,24) al controlar posición, racimos, largo, totales y copias, y que el blanco concentra las cuerdas grandes. Esta tarea separa color de posición con un diseño que compara **cuerdas en la misma posición dentro de grupos del mismo tamaño**.

Resultado central: **no hay un código de color→valor general e independiente de la posición**. El color está fuertemente atado a la posición (28 % de las posiciones tienen el mismo color en todos los grupos; NMI color~posición 0,505 frente a 0,200 del nulo). Al fijar la posición, el color se asocia al valor en **32/221 quipus (14,5 %)**, pero al añadir efectos fijos de grupo —es decir, al comparar dentro del mismo grupo— quedan **10/205 (4,9 %, exactamente lo esperado por azar)** y la mediana de varianza explicada cae a **1,2 %** (por debajo del nulo). El test agregado sí detecta una cola positiva (p = 0,002), pero es una **minoría de quipus con códigos locales fuertes** (r² absoluto mediano 13–31 %, rango de color 1,4–1,8 log), no un efecto difuso. Al excluir la **cuerda mayor de cada grupo**, el efecto dentro de grupo desaparece (0/157, p = 0,214).

En el diseño limpio de «swap» (dos grupos con los mismos colores en distinto orden), **gana la posición**: el color solo gana en 42 % de los 172 pares, y la aparente ventaja del color (p = 0,010) se debe íntegramente a **UR1140**, un quipu de colores compuestos `B` vs `B:BB`; sin él, p = 0,575.

**Veredicto:** el color no es una categoría semántica panandina que codifique magnitud. Es, sobre todo, **sintaxis de posición y de grupo**, con **códigos locales fuertes en una minoría de quipus** (≈5–15 %), muchos de ellos ligados a la cuerda mayor/total del grupo. La interpretación semántica de esos códigos locales sigue siendo **especulativa**.

---

## 1. Pregunta

1. ¿El color de una posición dentro del grupo cambia entre grupos? Si nunca cambia, color = posición y no hay nada que separar.
2. Cuando cambia, ¿el valor sigue al color o a la posición?
3. ¿El color aporta información sobre el valor después de controlar posición (y grupo), en cuántos quipus y con qué tamaño?
4. ¿Qué efecto mínimo era detectable con este corpus?

---

## 2. Método

### 2.1 Universo y unidad

- Unidad de inferencia: **el quipu**. Todos los conteos y p-valores se agregan por quipu; los tests por quipu usan permutaciones dentro del quipu.
- Cuerdas de **nivel 0** (colgantes) con color y valor no nulos.
- **Grupos de tamaño fijo:** dentro de cada quipu se toma cada tamaño `k` con **≥4 grupos completos** de ese tamaño (todas sus cuerdas con color y valor). Así `pos = 0..k-1` es comparable entre grupos.
- `k = 1` se excluye: no hay posición que controlar (98 estratos; es el diseño antiguo, confundido).
- Universo: **276 quipus** con ≥4 grupos iguales; **234 quipus con k ≥ 2**, **343 estratos (quipu,k)**, **18 151 cuerdas**, **1 901 posiciones**. La muestra primaria (sin ausentes ni totales) tiene **11 606 cuerdas**.
- Esto es el **43 % del corpus** (276/649): los quipus con estructura de grupos repetidos, que son justamente los más «tabulares» y donde el color tiene más probabilidad de ser columna. La conclusión no se extrapola sin más al 57 % restante.

### 2.2 Variables

- `y = log1p(valor)`.
- **Color:** se quitan los rangos en cm con `re.sub(r'\([^)]*\)','',s)`. Dentro de cada quipu, colores con <3 cuerdas se colapsan a `OTRO` (evita dummies de una sola cuerda).
- **Ausentes:** valor 0 con `nudos` vacío se excluye en la variante primaria (regla 6 del BRIEF); se reporta la variante que los incluye (`todo`).
- **Totales:** se excluye la cuerda cuyo valor es exactamente la suma del resto de su grupo.
- **Copias:** se construyen familias con las 25 parejas de `filas_alineadas.csv` (componentes conexas) y se deja **un representante por familia** (el de más cuerdas). La variante `sin_copias` las excluye; da los mismos resultados que la muestra completa (A 31/216, B global p = 0,004), así que se reporta como control y no como muestra primaria. Las copias no se cuentan como evidencia independiente.
- **Máxima del grupo:** en la variante `sin_copias_max` se excluye, además, la cuerda de mayor valor de cada grupo (una por grupo).

### 2.3 Modelos

Para cada quipu:

- **Modelo A (posición):** `y ~ posición(k,pos) + color`. Compara grupos en la misma posición; no controla diferencias globales entre grupos.
- **Modelo B (grupo + posición):** `y ~ grupo + posición(k,pos) + color`. Controla el nivel medio del grupo; identifica el color por variación dentro del grupo entre posiciones.
- **Modelo C (tamaño):** B + nº de racimos + log(largo). Controla que el color sea un proxy del tamaño de la cuerda (la explicación aburrida del equipo rojo).

Estadístico: **R² parcial del color** (incremento sobre los controles) y F del término color. Tamaño de efecto: **ΔSS/TSS** (proporción de varianza total explicada por color tras los controles) y rango de los efectos de color ajustados en log1p. Solo se aceptan quipus con **df2 = n − q − df1 ≥ 2**; sin eso el diseño grupo+posición satura la tabla y el R² no es interpretable (se excluyen 7–23 quipus según variante; se reporta `n_valid`).

### 2.4 Nulo

Se permutan los **colores dentro de cada `(quipu, k, pos)`**: se mantiene fija la posición y la composición de colores de cada posición, y solo se cambia qué grupo recibe cada color. Es el nulo que pide la tarea. 499 permutaciones por quipu; **999** para los conteos definitivos de A/B/C (con 299–499 el p mínimo es 0,002–0,003 y el umbral de BH para 200 tests es ~0,00025: el conteo queda artificialmente en 0). 499–999 para el test agregado `T = Σ ΔSS/TSS` (una estadística por quipu, no ponderada).

### 2.5 Corrección múltiple

- **BH-FDR** dentro de cada familia de tests por quipu (variante × modelo).
- **Holm** sobre las 11 pruebas principales (tabla en §5.3). La columna `holm` de `agregados_final.csv` es Holm solo dentro de los 4 agregados; la tabla del informe usa la familia completa de 11 pruebas, que es la que manda.
- Los conteos de quipus significativos se comparan con el 5 % esperado mediante binomial.

### 2.6 Potencia

Se destruye la asociación real permutando colores dentro de posición, se planta un efecto `+δ` en log1p sobre el color modal (y sobre W como robustez), y se mide la tasa de detección contra el percentil 95 del nulo (499 permutaciones, 200 simulaciones). δ ∈ {0; 0,2; 0,35; 0,5; 0,7}.

---

## 3. Descriptivo: color y posición están fuertemente confundidos

| Indicador | Valor |
|---|---|
| Posiciones con color **constante** entre grupos | **28,4 %** (540/1 901) |
| Posiciones con color modal ≥80 % de los grupos | **38,3 %** |
| Posiciones con ≥2 colores | 71,6 % |
| Por quipu: mediana de la fracción de posiciones constantes | **0,111** (P25 0,000; P75 0,556) |
| NMI color~posición (mediana por quipu) | **0,505** |
| NMI bajo barajado global de colores (mediana) | **0,200** |
| Diferencia NMI observada − nula | **+0,268** |
| Quipus con NMI observada > nula | **165/222 (74,3 %)**, binomial p = 1,1 × 10⁻¹³ |
| Colores por quipu (mediana) | 4 |

**Lectura:** en casi un tercio de las posiciones el color es literalmente la posición: todos los grupos repiten el mismo color. En el resto el color cambia, pero sigue muy acoplado a la posición (NMI 0,505 vs 0,200; 74 % de los quipus por encima del nulo). Hay variación suficiente para separar los ejes, pero el acoplamiento de origen es la primera explicación aburrida de cualquier asociación color–valor.

### 3.1 El diseño «swap»

Se identificaron **172 pares de posiciones** en **22 quipus** donde dos grupos del mismo tamaño tienen exactamente los mismos dos colores intercambiados entre dos posiciones. Si el valor sigue al color, las cuerdas del mismo color deben parecerse; si sigue a la posición, deben parecerse las de la misma posición.

| | Observado | Nulo (colores barajados dentro de posición) |
|---|---|---|
| Pares | 172 (22 quipus) | — |
| Gana el color | 72 (41,9 %) | — |
| Δ medio = d_pos − d_col | **−0,613** | **−1,659** (sd 0,494) |
| p (color mejor que posición) | **0,010** | — |

El Δ observado es **menos negativo** que el nulo: el color mejora algo el ajuste respecto de la posición pura, pero **la posición sigue ganando en promedio** (Δ < 0). Además, el resultado **no es robusto**: 96 de los 172 pares son de **UR1140**, un quipu casi monocromo (`B`) cuyos «colores» son variantes compuestas `B:BB`, `B:G`, `B:BB/B`. Sin UR1140: 76 pares, 21 quipus, gana el color 24/76 (31,6 %), Δ medio −1,828 frente a nulo −1,740 (sd 0,577), **p = 0,575**. La evidencia limpia de «el valor sigue al color» es, pues, **un solo quipu y con colores compuestos**, no un fenómeno de colores Ascher distintos.

---

## 4. Resultados principales

### 4.1 Modelo A: a posición fija, el color se asocia al valor en una minoría

Variante primaria (sin ausentes ni totales), 999 permutaciones por quipu:

| | Valor |
|---|---|
| Quipus válidos | 221 |
| Quipus con q < 0,05 | **32 (14,5 %)** |
| Esperado al 5 % | 11,05 |
| Binomial | **p = 7,7 × 10⁻⁸** |
| Quipus con q < 0,10 | 39 |
| R² parcial mediano (todos) | 0,085 |
| Varianza absoluta mediana (todos) | **3,65 %** |
| Varianza absoluta mediana (hits) | **30,6 %** |
| Rango de color mediano (hits) | **1,76 log** (≈ 5,8×) |
| Test agregado T_abs | 24,76 vs nulo 12,10; **p = 0,002** |
| Quipus con z > 0 | 56,6 % |

Hay un **exceso claro de quipus** (32 vs 11) y el agregado es significativo. Pero la distribución es **bimodal**: la mediana de todos (3,65 %) está prácticamente en el nulo (3,48 %), y son unos pocos quipus con efectos enormes (30 % de varianza, colores que difieren 5–6×) los que producen el exceso. Los 32 hits incluyen casos como UR123 (r² = 0,98; rango 3,31 log), AS128 (0,94), HP017 (0,85), UR231 (0,79), UR052 (0,69). No es un efecto pequeño y difuso: es «la mayoría no tiene nada, una minoría tiene un código fuerte».

### 4.2 Modelo B: al comparar dentro del grupo, el exceso desaparece

| | Valor |
|---|---|
| Quipus válidos | 205 |
| Quipus con q < 0,05 | **10 (4,9 %)** |
| Esperado al 5 % | 10,25 |
| Binomial | **p = 0,577** |
| Quipus con q < 0,10 | 14 |
| R² parcial mediano | 0,075 |
| Varianza absoluta mediana (todos) | **1,20 %** |
| Varianza absoluta mediana (hits) | **13,1 %** |
| Rango de color mediano (hits) | **1,43 log** (≈ 4,2×) |
| Test agregado T_abs | 8,36 vs nulo 6,40; **p = 0,002** |
| Quipus con z > 0 | 47,8 % (¡menos de la mitad!) |

El **número** de quipus significativos es exactamente el esperado por azar (10/205), pero el **test agregado** sigue detectando una cola positiva (p = 0,002): los 10 hits tienen efectos grandes (13 % de varianza mediana, hasta 28 %), mientras la mediana de los 195 restantes es 1,0 % y solo el 47,8 % de los z son positivos (52,2 % negativos). Es decir: **no hay un efecto general; hay un puñado de códigos locales fuertes**.

Intersección A ∩ B: **7 quipus**. Otros **25** son significativos solo en A (asociación a nivel de grupo, no dentro del grupo) y **3** solo en B. La descomposición es informativa:

- **25 quipus:** el color marca **grupos** con valores distintos (A sí, B no).
- **7 quipus:** color asociado al valor tanto entre grupos como dentro del grupo.
- **3 quipus:** código local dentro del grupo que A no ve (AS008, KH0081, UR195).

### 4.3 Modelo C: el control de tamaño no cambia el patrón

Añadiendo nº de racimos y log(largo) (la receta del equipo rojo):

| | Valor |
|---|---|
| Quipus válidos | 186 |
| q < 0,05 (999 permutaciones) | **9 (4,8 %)** |
| Esperado | 9,3 (p = 0,587) |
| Varianza absoluta mediana | **0,97 %** |
| Test agregado | **p = 0,002** |
| Hits | AS008, HP017, KH0081, QU013, UR195, UR208, UR1140, MM019, UR1152 |

El tamaño de la cuerda no explica los códigos locales (HP017 sube de r² 0,826 a 0,859 al añadir tamaño; QU013 de 0,469 a 0,494), pero tampoco crea un efecto general: 9/186 es azar y la mediana es 1 %.

### 4.4 El efecto dentro de grupo se concentra en la cuerda mayor

Al excluir la cuerda de mayor valor de cada grupo (variante `sin_copias_max`):

| | A | B |
|---|---|---|
| Quipus válidos | 195 | 157 |
| q < 0,05 | **18 (9,2 %)** | **0** |
| Esperado | 9,75 | 7,85 |
| Binomial | **p = 0,0095** | p = 1,0 |
| Varianza absoluta mediana | 6,04 % | 1,11 % |
| Test agregado | **p = 0,002** | **p = 0,214** |
| z medio | +1,20 | **−0,05** |
| Quipus con z > 0 | 61 % | 42 % |

Quitar una sola cuerda por grupo **mata la señal dentro de grupo**: B pasa de p = 0,002 a p = 0,214 y de 10 hits a 0; A se reduce de 32 a 18 hits (aunque conserva un exceso modesto, binomial p = 0,0095). Los efectos de los quipus estrella se atenúan mucho: UR195 baja de r² 0,565 a 0,171; UR1152 de 0,746 a 0,197; AS008 de 0,414 a 0,218. No todos (HP017 0,826→0,706; UR197 0,434→0,492; UR229 0,309→0,398), pero el agregado desaparece.

**Interpretación aburrida:** el color de la cuerda mayor/total del grupo es distinto del resto, y esa es la principal fuente de «color→valor» dentro de grupo. Es una **convención de formato** (marcar el total, el encabezado o la cuerda principal), no un código semántico de contenido. La pérdida de potencia por quitar 1/k cuerdas también contribuye; no se puede separar del todo con este diseño, pero la atenuación de los efectos individuales apunta a algo más que potencia.

### 4.5 Copias, ausentes y totales

- **Copias:** `sin_copias` da A 31/216 (global p = 0,002) y B 0/200 con 299 permutaciones (global p = 0,004; mediana de varianza 1,1 %). Las copias no crean el fenómeno: 2 de los 32 hits de A y 1 de los 10 de B son copias. El patrón es el mismo que en el corpus completo.
- **Ausentes:** incluirlos (`todo`) sube los conteos (A 48/234, B 11/234) pero no cambia la conclusión; la mediana de varianza absoluta de B es 2,0 %. Los ausentes añaden una asociación color–presencia, no color–magnitud.
- **Totales:** excluirlos baja A de 48 a 32 y B de 11 a 10 (comparando `todo` con `primario`); confirma que parte del «color = clase» era «color = total».

### 4.6 Colores simples vs compuestos

| Variante | A: varianza abs. mediana | A: T_abs (p) | B: varianza abs. mediana | B: T_abs (p) |
|---|---|---|---|---|
| Todos | 3,65 % | 24,76 (0,002) | 1,20 % | 8,36 (0,002) |
| Solo simples (sin `: / -`) | 2,70 % | 19,29 (0,003) | **0,50 %** | 5,82 (0,003) |
| Compuestos → `MIX` | 2,62 % | 20,85 (0,003) | 0,73 % | 7,23 (0,003) |

Los colores compuestos (22,9 % de las cuerdas) aportan **cerca de la mitad** de la señal de B: la varianza absoluta mediana cae de 1,20 % a 0,50 % al quitarlos. Para A, la señal baja ~25 %. Los códigos locales de B se apoyan en parte en variantes de mezcla (`B:BB`, `W:MB`…), que pueden codificar torsión/ply más que una categoría de color. Es un argumento más para no leerlos como semántica de color sin imágenes.

### 4.7 Escala de rangos

Repitiendo A/B sobre el rango normalizado dentro de cada quipu (probit), A da **29/222** q < 0,05 (frente a 32/221 con log1p): el resultado de A es robusto a la escala. B da 0/207 con 199 permutaciones (sin resolución para BH); la mediana de r² es 0,080, del mismo orden que con log1p. No hay evidencia de que el patrón sea un artefacto de valores extremos.

### 4.8 Dirección y sitio

- **W no es «grande».** Después de controlar posición (A) o grupo+posición (B), W > resto en solo **31–32 %** de los quipus; la mediana del contraste es 0. La observación del equipo rojo («W concentra las cuerdas grandes») es marginal: se explica por posición/grupo, no por un código W = total.
- **No hay enriquecimiento por región.** De los 32 hits de A, 25 son de región «Unknown»; ninguna región con n ≥ 8 supera el 25 % de hits y todos los q de Fisher son 1,0. No se puede atribuir el fenómeno a un sitio/colección con esta muestra. (La procedencia de museo no se usa como lugar de origen, regla 6.)

---

## 5. Controles

### 5.1 Nulo y calibración

- El nulo permuta colores **dentro de (quipu,k,pos)**: mantiene la posición y la composición de colores de cada posición. Es el nulo correcto para «¿el color aporta algo a posición fija?».
- Calibración empírica del test agregado con 200 simulaciones bajo el nulo: **4,5 % (modelo B)** y **6,5 % (modelo A)** de rechazo al 5 %. Aceptable; A algo anticonservador, dentro del error Monte Carlo (±2 %).
- El nulo por quipu es discreto; por eso se usan 999 permutaciones para los conteos BH.

### 5.2 Grados de libertad y resolución de p

- Se excluyen quipus con **df2 < 2**: sin eso, grupo+posición satura la tabla (df2 negativo) y el R² es 1 por construcción. Es un filtro necesario; afecta a 7–23 quipus según variante.
- **Resolución:** con 299 permutaciones el p mínimo es 0,0033; el umbral de BH para 200 tests es ~0,00025. Por eso el conteo de B con 299 es 0 (artefacto) y con 999 es 10. Todos los conteos que se reportan como definitivos usan 999.
- **df2 pequeño:** 26 quipus de B (13 %) tienen df2 = 2–4 y aportan 22 % del T_abs; sus R² son inestables. El filtro mínimo df2 ≥ 2 es permisivo. Con df2 ≥ 5 el T_abs de B baja de 8,36 a 6,54 (no se recalculó el nulo); la conclusión cualitativa (cola de pocos quipus, no efecto general) no depende de ellos, pero los tamaños de efecto de esos 26 quipus deben tomarse con cautela.
- Sensibilidad paramétrica (F, sin permutar): A 45/216, B 16/208, C 16/186. Es más anticonservadora que la permutación; se reporta solo como cota superior. La correlación entre p permutado y pF es 0,85–0,89 en log.

### 5.3 Corrección múltiple (Holm sobre 11 pruebas principales)

| Prueba | p | Holm |
|---|---|---|
| NMI color~posición (165/222) | 1,1 × 10⁻¹³ | **1,3 × 10⁻¹²** |
| A: exceso de quipus (32/221) | 7,7 × 10⁻⁸ | **7,7 × 10⁻⁷** |
| A: T_abs global | 0,002 | **0,018** |
| B: T_abs global | 0,002 | **0,018** |
| C (tamaño): T_abs global | 0,002 | **0,018** |
| A sin máxima: exceso (18/195) | 0,0095 | **0,047** |
| A sin máxima: T_abs | 0,002 | **0,018** |
| B sin máxima: T_abs | 0,214 | 0,642 |
| Swap (172 pares) | 0,010 | **0,047** |
| Swap sin UR1140 | 0,575 | 1,0 |
| B: conteo (10/205) | 0,577 | 1,0 |

Sobreviven a Holm: el acoplamiento color–posición, el exceso de A, los agregados de A/B/C y A sin máxima, y el swap completo. **No** sobreviven: el conteo de B, el swap sin UR1140 y el B sin máxima. El swap completo pasa Holm por poco (0,047) y depende de un quipu; no debe presentarse como evidencia fuerte.

### 5.4 Potencia declarada

| Modelo | Objetivo | Potencia δ=0,2 | δ=0,35 | δ=0,5 | MDE 80 % (log) | ≈ % de valor |
|---|---|---|---|---|---|---|
| A | color modal | 0,64 | 1,00 | 1,00 | **0,267** | +31 % |
| A | W | 0,30 | 0,82 | 1,00 | **0,344** | +41 % |
| B | color modal | **0,965** | 1,00 | 1,00 | **0,164** | +18 % |
| B | W | — | — | 1,00 | **0,238** | +27 % |

El diseño **sí tenía potencia**: un efecto corpus-wide de +0,16 log (≈18 % más valor) en el color modal se detecta con 80 % en el modelo B, y +0,5 log con 100 %. El efecto general observado es mucho menor (mediana de varianza 1,2 %, equivalente a ~0,1 log), y el efecto de los códigos locales es mucho mayor (1,4–1,8 log). La conclusión negativa para un código general no es «falta de potencia»: es un negativo informativo.

---

## 6. Resultados negativos (explícitos)

1. **No hay un código color→valor general.** En el modelo que compara dentro del grupo, 10/205 quipus son significativos (esperado 10,25; p = 0,577); la mediana de varianza explicada es 1,2 %, por debajo del nulo aproximado (1,6 % en la muestra sin filtrar), y solo el 47,8 % de los z son positivos (52,2 % negativos).
2. **El exceso de A es, en su mayor parte, group-level.** De 32 hits de A, 25 no sobreviven al añadir efectos fijos de grupo; solo 7 son también B. El color marca grupos con valores distintos, no cuerdas dentro del grupo.
3. **El efecto dentro de grupo desaparece sin la cuerda mayor.** B: de 10 hits y p = 0,002 a 0 hits y p = 0,214 al excluir la mayor de cada grupo. La señal está concentrada en la cuerda más grande/total.
4. **El swap no es robusto.** Gana la posición en 58 % de los pares; el p = 0,010 del agregado se debe a UR1140 (96/172 pares, colores `B` vs `B:BB`). Sin UR1140, p = 0,575.
5. **W no es «grande».** W > resto en solo 31–32 % de los quipus tras controlar posición/grupo; la mediana del contraste es 0. El «W = total» del equipo rojo es un efecto de posición/grupo, no un código.
6. **Los colores compuestos aportan una parte desproporcionada.** La varianza absoluta de B cae de 1,20 % a 0,50 % al quedarse solo con colores simples; los códigos locales se apoyan en mezclas que pueden codificar torsión/ply.
7. **No hay enriquecimiento por región/colección:** todos los q de Fisher = 1,0; 25/32 hits de A son «Unknown».
8. **La lista de quipus «con efecto» no es estable entre pipelines.** Solo 7/32 hits de A coinciden con los 27 del equipo rojo (Jaccard 0,13); con el modelo C, 3/9. El fenómeno agregado es robusto, la atribución a quipus concretos no.
9. **El negativo tiene límites de universo.** Solo se analizan quipus con ≥4 grupos del mismo tamaño (43 % del corpus) y k ≥ 2. No se puede afirmar nada sobre quipus de grupos irregulares o de una sola cuerda por grupo.
10. **La potencia no cubre códigos locales pequeños.** El MDE de 0,16 log es para un efecto en todos los quipus; un código local de +0,2 log en el 5 % de los quipus podría no detectarse en el agregado, aunque los códigos locales observados son mucho mayores (1,4–1,8 log) y sí se detectan individualmente.

---

## 7. Nivel de evidencia

| Afirmación | Nivel | Motivo |
|---|---|---|
| Color y posición están fuertemente confundidos | **Bien apoyado** | 28,4 % de posiciones constantes; NMI 0,505 vs 0,200; 165/222, p = 1,1 × 10⁻¹³ |
| No hay un código color→valor general independiente de posición y grupo | **Apoyado con datos** | B 10/205 (azar), mediana 1,2 %, 52,2 % de z negativos, C 9/186 (azar), MDE 0,16 log; límite: 43 % del corpus |
| El exceso de A es, sobre todo, asociación a nivel de grupo | **Apoyado con datos** | 25/32 hits de A desaparecen con efectos fijos de grupo; solo 7 son A∩B |
| Una minoría de quipus (≈5–15 %) tiene códigos locales fuertes | **Apoyado con datos** | A 32/221 (14,5 %), B 10/205, C 9/186; hits con 13–31 % de varianza y rango 1,4–1,8 log; robusto a rango y a colores simples (atenuado) |
| El color marca la cuerda mayor/total del grupo | **Propuesto** | B desaparece sin la mayor (0/157, p = 0,214); atenuación de los efectos individuales; no se separa del todo de la pérdida de potencia |
| Los códigos locales tienen contenido semántico | **Especulativo** | Sin imágenes, contexto ni textos; los compuestos pueden ser torsión/ply; la lista de quipus no es estable entre pipelines |

---

## 8. Para el coordinador

- **El «167/403» está muerto y el color no es un código general de magnitud.** Con el diseño que compara cuerdas en la misma posición, el color se asocia al valor en 32/221 quipus (14,5 %), pero al añadir efectos fijos de grupo quedan 10/205 (4,9 %, exactamente el azar) y la mediana de varianza explicada cae a **1,2 %**, por debajo del nulo. El test agregado detecta una cola (p = 0,002), pero no un efecto difuso.
- **La explicación aburrida es posición + grupo.** El 28,4 % de las posiciones tiene el mismo color en todos los grupos; la NMI color~posición es 0,505 frente a 0,200 del nulo (165/222, p = 1,1 × 10⁻¹³). El color es, sobre todo, sintaxis de columna/grupo.
- **El exceso que queda en A es group-level.** De 32 hits de A, 25 no sobreviven al control de grupo: el color marca **grupos** con valores distintos, no cuerdas dentro del grupo. Solo 7 quipus tienen ambas cosas.
- **Hay una minoría de códigos locales fuertes, no un vocabulario compartido.** 10/205 quipus (B) y 9/186 (C) tienen efectos grandes: 13–31 % de la varianza, colores que difieren 4–6×. Casos de A: UR123 (r² 0,98), AS128, UR231, UR052. Casos de B/C: HP017, QU013, UR208, AS008, UR195, UR1152. Son códigos locales, no un léxico panandino.
- **La señal dentro de grupo se concentra en la cuerda mayor/total.** Al excluir la mayor de cada grupo, B pasa de 10 hits y p = 0,002 a **0 hits y p = 0,214**. Es consistente con «color = marca del total/encabezado», no con «color = categoría de contenido». Nivel: propuesto.
- **El swap limpio no salva al color.** Gana la posición en 58 % de los 172 pares; el p = 0,010 agregado se debe a **UR1140** (96/172 pares, colores `B` vs `B:BB`); sin él, p = 0,575. No usar el swap como evidencia de semántica.
- **W no es «grande».** Tras controlar posición/grupo, W > resto en solo 31–32 % de los quipus y la mediana del contraste es 0. El «W concentra las cuerdas grandes» es un efecto marginal de posición/grupo. Los compuestos (`B:BB`, `W:MB`…) aportan ~40 % de la señal de B y pueden ser torsión/ply, no color.
- **El negativo es informativo: había potencia.** El MDE a 80 % es **0,164 log (≈18 %)** para el color modal en B y 0,267 en A; un +0,5 log se detecta al 100 %. No se puede atribuir la ausencia de efecto general a falta de potencia.
- **Recomendación 1:** no buscar un léxico de color panandino; buscar **convenciones de formato** (¿el color distinto marca el total, el encabezado, la cuerda mayor o la primera columna?) y estudiar caso por caso los 10–30 quipus con código local (UR123, HP017, QU013, UR208, AS128, UR231, UR1140) con imágenes: ¿el color cambia el valor o solo la marca? ¿Coincide con torsión, ply o posición?
- **Recomendación 3:** no presentar listas de quipus «con efecto» como canónicas: solo 7/32 coinciden con el equipo rojo y 3/9 con el modelo C. El fenómeno agregado es robusto; la atribución individual es frágil. Reportar siempre el pipeline y el universo.

---

## 9. Reproducibilidad

| Script | Qué hace |
|---|---|
| `01_diseno.py` | Construye la base de grupos de tamaño fijo, posiciones y copias. |
| `02_descriptivo.py` | Posiciones constantes, NMI color~posición y pares swap. |
| `motor.py` | Motor de los modelos A/B/C y permutaciones dentro de posición. |
| `04_run.py` | Primera pasada de variantes/modelos (A/B); resultados en `log_04.txt`. |
| `05_potencia.py` | Potencia declarada y MDE. |
| `06_swaps.py` / `06b_swaps_sin_ur1140.py` | Test swap completo y sin UR1140. |
| `07_resumen.py` | Resúmenes y top quipus. |
| `08_global_abs.py` | T_abs y z por quipu (primera versión). |
| `09_robustez.py` | Colores simples/compuestos y escala de rangos. |
| `10_final.py` / `10b_final.py` | Resultados finales con filtro df2 ≥ 2; `10b` guarda `color_posicion.csv`. |
| `11_bh.py` / `11b_bh_C.py` | BH con 999 permutaciones (A/B y C). |
| `12_size.py` | Modelo C (tamaño). |
| `13_merge.py` | Integra los p/q de 999 permutaciones en el CSV final. |

**Salidas principales:** `color_posicion.csv` (una fila por quipu × variante × modelo, con r², r² absoluto, p, q, df, efectos), `agregados_final.csv`, `agregados_todas.csv`, `bh_999.csv`, `bh_999_C.csv`, `potencia.csv`, `potencia_resumen.csv`, `swaps_test.csv` (172 pares), `swaps_test_sin_ur1140.csv` (76 pares), `swaps_quipu.csv`, `robustez.csv`, `nmi_color_pos.csv`, `diseno_resumen.csv`. Los agregados de las variantes `todo`, `sin_aus` y `sin_copias` están en `log_04.txt` y `log_10.txt`; el CSV principal contiene las variantes `primario` y `sin_copias_max`, que son las que sostienen las conclusiones.
