# UR262 — Lectura profunda de un quipu de Inkawasi (Incahuasi)

**Quipu:** UR262 = KH0498 = Museo del Proyecto Incahuasi, nº 12009-13. Procedencia: Incahuasi (valle de Cañete), recuperado en la **kallanka U.A. 02** (Urton 2017, cap. 9). 490 cuerdas.
**Scripts:** `01_prep.py` … `09_nudos_partidos.py` en esta carpeta. Tabla de resultados: `ur262_tabla_pruebas.csv`.
**Datos:** `analisis/datos/cuerdas.csv` y `grupos.csv` (KFG). Contraste con OKR (KH0498) en §7.

---

## 0. Resumen ejecutivo

UR262 es el quipu **más grande del archivo de Incahuasi** (490 cuerdas; mediana del archivo = 76) y el más "arbustivo" (352 subsidiarias, hasta 5 niveles). Su estructura es la de un **registro de lista anidada**: una cabecera de 3 cuerdas, seis grupos de 18–27 colgantes y dos cuerdas sueltas que no son datos (una de ellas, `p138`, es una **cuerda de amarre** anotada como "tie cord").

La aritmética interna es **negativa**: no hay cuerdas superiores (`union` T = 0), ningún total de grupo reaparece como valor de otra cuerda (0 casos; 6,7 esperados por azar), y "colgante = suma de subsidiarias" se cumple en 2 de 105 casos (p = 0,07; no significativo). Los dos patrones que **sí** sobreviven a los controles son débiles y locales: (a) el primer colgante del grupo tiende a ser el mayor (3/6 grupos; p = 0,003) y a ser de color AB (3/6; p = 0,007, no sobrevive Holm); (b) hay 8 casos de **duplicación madre-hija** (mismo valor o ±1 %; p = 0,004), que encajan con la idea de "checks-and-balances" de Urton y Chu (2015).

Lectura más probable (**propuesta**, con partes **apoyadas con datos**): **registro de depósito/almacén, no censo ni calendario ni tributo sumatorio**. Filas = grupos (clases de producto o sectores del depósito); columnas = niveles de subdivisión de cada entrada. No es un árbol de sumas: los niveles **repiten o subdividen** una entrada, no la agregan.

---

## 1. Pregunta

¿Qué es UR262? ¿Qué registra, cómo está organizado, y qué parte de su contenido es aritmética verificable frente a pura lista? ¿Qué información —si alguna— es no numérica?

---

## 2. Método

1. Reconstrucción del árbol completo (madre → hijas → nietas) desde `padre`/`nivel`/`orden`; 490/490 cuerdas clasificadas.
2. Parseo de los 725 racimos de nudos (`tipo`, posición, dirección, aporte) y verificación de que la suma de aportes = `valor` en las 490 cuerdas (0 discrepancias).
3. Batería de detectores aritméticos y estructurales, cada uno con **nulo de permutación explícito** (1.000 remuestreos, semilla 0):
   - nulo global: se barajan los 490 valores entre todas las cuerdas, árbol fijo;
   - nulo por nivel: se barajan los valores dentro de cada nivel (conserva la distribución de magnitudes por nivel);
   - nulo de dígitos (para valores repetidos): se permutan los dígitos de cada posición decimal entre cuerdas, conservando la estructura decimal;
   - nulo de color: se permutan las etiquetas de color entre colgantes.
4. p empírico = (1 + nº de nulos ≥ observado)/(1 + 1.000). **Holm** sobre la familia de 15 pruebas (tabla §6).
5. Unidad de análisis: el quipu. Las pruebas internas son condicionales a este quipu; no se generaliza a otros sin replicación.

---

## 3. Estructura reconstruida

### 3.1 Cifras globales

| Métrica | Valor |
|---|---|
| Cuerdas totales | **490** |
| Colgantes (nivel 0) | **138** |
| Subsidiarias (nivel ≥ 1) | **352** (185 / 113 / 38 / 12 / 4 por nivel 1–5) |
| Profundidad máxima | **5** |
| Cuerdas con nudos | 375 (76,5 %) |
| Cuerdas **sin nudos** (`valor` 0 = ausente, no cero) | **115 (23,5 %)**: 40 colgantes y 75 subsidiarias |
| Racimos de nudos | 725 (S 436, L 245, E 44) |
| Torsión | **S en las 490 cuerdas (100 %)** |
| Dirección de nudo | **724 Z, 1 S** (`p11s1s1`, un racimo de 3 nudos simples que aporta 30) |
| `union` | R 137, V 1 (`p138`), U 352 → **cero cuerdas superiores (T)** |
| Colores distintos | 27 códigos; NB 223, AB 165, AB:KB 29, MB 21, MB:KB 6, AB:MB 6… |
| Valor suma de colgantes | 25.282 |
| Valor suma de todas las cuerdas | 86.625 (máx. 8.071 en `p9s1`) |

### 3.2 Grupos (`grupos.csv` + datos)

`grupos.csv` da 9 grupos, pero **G2 y G8 son cuerdas sueltas sin nudos**, no grupos de datos: `p22` (AB, 23 cm, en 11,5 cm del cordón) y `p138` (la cuerda de amarre, 80 cm, `union` V, nota "tie cord"). Quedan **7 grupos utilizables**: una cabecera (G0) y seis grupos de 18–27 colgantes.

| Grupo | pos (cm) | colgantes | subsidiarias | cuerdas | sin nudos | suma colgantes | mediana | máx. |
|---|---|---|---|---|---|---|---|---|
| 0 | 2,0 | 3 (todas AB) | 1 | 4 | 0 | 6.025 | 2.310 | 3.088 |
| 1 | 4,0 | 18 (todas NB) | 53 | 71 | 2 | 10.112 | 495 | 1.278 |
| 2 | 11,5 | 1 (AB) | 0 | 1 | 1 | 0 | 0 | 0 |
| 3 | 17,5 | 20 | 53 | 73 | 23 | 1.028 | 45 | 194 |
| 4 | 25,0 | 27 | 27 | 54 | 28 | 1.121 | 0 | 277 |
| 5 | 32,5 | 22 | 74 | 96 | 22 | 3.530 | 81 | 1.180 |
| 6 | 40,0 | 24 | 81 | 105 | 18 | 2.871 | 50 | 1.146 |
| 7 | 46,5 | 22 | 63 | 85 | 20 | 595 | 23 | 181 |
| 8 | 94,0 | 1 (amarre) | 0 | 1 | 1 | 0 | 0 | 0 |

Los grupos arrancan a intervalos regulares de ~6,5–7,5 cm sobre el cordón principal (2,0; 4,0; 11,5; 17,5; 25,0; 32,5; 40,0; 46,5). G0 abre el quipu (tres cuerdas AB, valores 3.088 / 627 / 2.310) y es la única sección monocroma AB.

### 3.3 Jerarquía

- 33 colgantes no tienen hijas; 54 tienen 1; 35 tienen 2; 7 tienen 3; 7 tienen 4; 2 tienen 6.
- Las cadenas pueden llegar a 5 niveles (p. ej. `p80s1` → `p80s1s2` → `p80s1s2s1` → `p80s1s2s1s1` → `p80s1s2s1s1s2`).
- **Las subsidiarias de nivel 1 son, de media, más grandes que los colgantes** (media 279 vs 183; máx. 8.071 vs 3.088). Los números grandes viven *un nivel por debajo* de los colgantes, no arriba: eso descarta leer el colgante como "total" del que cuelga un desglose.

### 3.4 Color y nivel

El color no es un código de columna: es un **gradiente de profundidad**.

| Nivel | AB | NB | otros | % AB |
|---|---|---|---|---|
| 0 (colgante) | 15 | 120 | 3 | 10,9 % |
| 1 | 55 | 78 | 52 | 29,7 % |
| 2 | 68 | 16 | 29 | 60,2 % |
| 3 | 18 | 5 | 15 | 47,4 % |
| 4 | 6 | 3 | 3 | 50 % |
| 5 | 3 | 1 | 0 | 75 % |

χ² (NB/AB × nivel) = 121,2; gl = 5; p ≈ 2·10⁻²⁴. Es un hecho descriptivo robusto, pero **no demuestra significado**: puede ser una convención de manufactura (cuerdas claras para lo que cuelga de otra cuerda).

### 3.5 Nudos: decimalidad casi perfecta

- En las **unidades** solo hay nudos largos (L, dígitos 2–9) o figura de ocho (E, dígito 1): **289 racimos L/E en 278 cuerdas**; cero nudos simples en unidades.
- Simples (S) solo en decenas, centenas y millares (**436/436**).
- **El dígito 1 se escribe siempre con E** (44 racimos de 1 vuelta; ningún L de 1 vuelta), y el 0 de unidades simplemente no se anuda (98 cuerdas terminan en decenas).
- 277 cuerdas tienen dígito de unidades ≠ 0; su distribución (1:34, 2:38, 3:44, 4:41, 5:25, 6:28, 7:25, 8:27, 9:15) se aparta de la uniforme (χ² p = 0,005), con exceso de 3–4 y defecto de 9.
- Ningún nudo con más de 9 vueltas, ningún L con aporte ≥ 10, ninguna violación del orden decimal (posiciones crecientes hacia abajo).
- **Excepción real (11 cuerdas, 2,2 %):** el dígito de unidades está **partido en dos racimos contiguos**, casi siempre "n−1 + 1E" (`4L+1E`=5 en `p114s3s1`, `5L+1E`=6 en `p129s3`, `3L+1E`=4 en `p83s2s1`, `7L+1E`=8 en `p49s2`, `1E+1E`=2 en `p115s1`, `4L+2L`=6 en `p49`, `7L+2L`=9 en `p84`). En 10 de 11 la suma coincide con el dígito de unidades; **`p15s4s1` es la única anomalía dura**: `9L+1E` en unidades da 10 y KFG registra 110, cuando la lectura decimal estricta sería 109 (o 120 si hubiera acarreo). Es el único caso del quipu en que la suma L/E no reproduce el dígito de unidades.

Esto reproduce el patrón "S…L;E" descrito para Incahuasi en la síntesis del proyecto y es la parte **demostrada** del quipu: es un registro decimal limpio.

---

## 4. Aritmética interna (con nulos)

| Prueba | Observado | Esperado por azar | p | Holm |
|---|---|---|---|---|
| A1 colgante = suma de hijas directas | 2/105 | 0,44 | 0,073 | 0,51 |
| A2 colgante = suma de todos sus descendientes | 1/105 | 0,28 | 0,25 | — |
| A3 cuerda con una sola hija, mismo valor | 4 | 0,53 | **0,003** | **0,036** |
| A4 total de grupo repetido en otra cuerda | **0** | 6,7 | 1,00 | 1,00 |
| A5 colgante = bloque contiguo de ≥2 colgantes del grupo | 26 | 21,9 | 0,31 | 1,00 |
| A6 razón suma_hijas/valor ∈ [6,5; 7,5] | 8 | 1,45 | **0,002** | **0,028** |
| A6b misma prueba, máximo sobre ventanas (corrige elección post hoc) | 8 | 8,4 | 0,62 | 1,00 |
| A7 colgante = 2 × suma de hijas | 0 | 0,30 | 1,00 | 1,00 |

Lectura:

- **No hay jerarquía de sumas.** Los 2 casos de A1 son `p71` = 54 = `p71s1` y `p136` = 24 = `p136s1`: no son sumas, son **copias** (una hija única con el mismo valor). Con el nulo por nivel, A1 sube a p = 0,037 y tampoco sobrevive.
- **No hay totales de grupo en ninguna parte**: los totales (10.112; 1.028; 1.121; 3.530; 2.871; 595; 6.025) no aparecen como valor de ninguna cuerda (0 vs 6,7 esperados). Tampoco el primer colgante es la suma del resto (0/7 grupos). Es un **negativo fuerte**: si el quipu tuviera una cabecera sumatoria, estaría aquí y no está.
- **No hay cuerdas superiores** (`union` T = 0), así que la prueba clásica "cuerda superior = suma de grupo" **no es aplicable**, no es que salga negativa: el quipu no tiene ese nivel.
- **A6 es un artefacto probable.** El cociente "suma de hijas / valor del colgante" se agrupa en 6,7–7,4 en 8 casos (p. ej. `p7`: 5.464/788 = 6,93; `p74`: 1.476/210 = 7,03; `p98`: 2.210/320 = 6,91). Pero la ventana se eligió *después* de ver los datos; al corregir por la elección de ventana (máximo sobre todas las ventanas de ancho 1), p = 0,62. **No lo cuento como hallazgo.**
- **Razón 1/10 (chequeo secundario):** 1 caso con v/suma de hijas ≈ 0,1 frente a 2,0 esperados por azar (p = 0,85, 500 permutaciones): tampoco hay estructura de razón 1/10 (la clásica de tributo).

---

## 5. Controles adicionales

| Prueba | Observado | Nulo | p |
|---|---|---|---|
| D1 valores repetidos (cuerdas "sobrantes" en valores duplicados) | 201 | 256 (nulo de dígitos) | 1,00 |
| D2 similitud entre colgantes adyacentes (mediana \|dif\|) | 45 | 56 | 0,18 |
| D3 primer colgante del grupo es AB | 3/6 | 11 AB/133 colgantes → 0,50 esperados | 0,0075 (exacta) |
| D3b periodicidad del color (mejor lag 2–15) | 0,854 | 0,736 | 0,080 |
| D5 largo vs valor (Spearman) | ρ = 0,453 | 0,00 | 0,001 |
| D6 primer colgante = máximo del grupo | 3/6 | 0,29 | 0,0027 |
| D7 duplicado madre-hija exacto | 7 | 1,98 | 0,005 |
| D7b duplicado madre-hija ≤ 1 % | 8 | 2,28 | 0,004 |

- **D1 (negativo):** no hay un vocabulario de valores-cuota. Los 201 duplicados son *menos* de los que produce un nulo que conserva la estructura decimal; valores como 10 (21 veces), 40 (10), 30 (10) no exceden lo esperable. **No se reproduce aquí el sistema de "fixed values" (208, 47, 15, 10) que Urton describe para otros quipus de Inkawasi**: 208 aparece 0 veces, 47 tres veces, 15 una vez.
- **D5 (artefacto):** la correlación largo–valor desaparece al controlar por número de racimos (ρ parcial = −0,11). Es mecánica: más dígitos → más nudos → más largo. **No hay código de longitud.**
- **D6 + D3:** las cuerdas iniciales de grupo son a la vez las mayores (3/6; esperado 0,29) y desproporcionadamente AB (3/6; 11 AB entre 133 colgantes). Es el patrón de **cabecera de sección**. Con Holm, D6 sobrevive (0,035) y D3 queda al borde (0,067).
- **D7 (apoyado con datos):** 8 pares madre-hija con el mismo valor (±1 %), frente a 2,3 esperados. Ejemplos: `p71` = `p71s1` = 54; `p87s1` = `p87s1s1` = 38; `p106s1` = `p106s1s1` = 40; `p136` = `p136s1` = 24; y el casi-duplicado `p92` = 1.146 frente a `p92s1` = 1.151 (diferencia 5, 0,4 %). Las cuerdas de cada par son **físicamente distintas** (largos 53 vs 33,5 cm; 17 vs 25; 8,5 vs 11; 30,5 vs 15) y llevan los nudos a alturas distintas, así que no es un copy-paste de la transcripción: son dos cuerdas anudadas con el mismo número. Entre colgantes del mismo grupo no hay exceso de duplicados exactos (8 vs 8,2). Es un efecto pequeño (2,3 % de los pares) pero con un mecanismo claro: **restatement/control**, no suma.

---

## 6. Tabla maestra y corrección múltiple

15 pruebas, Holm: sobreviven A3 (duplicado exacto, 0,036), A6 (razón 6,8 — artefacto, 0,028), D5 (largo-valor — artefacto mecánico, 0,015), D6 (primer colgante = máximo, 0,035) y D7 (duplicados madre-hija, 0,044–0,050). Quedan fuera A1, A4, A5, D1, D2, D3 (0,067), D3b, A6b, A7.

Si se descuentan los dos artefactos (A6 y D5), los hallazgos que sobreviven son **tres regularidades estructurales locales**: cabecera de grupo (D6), duplicación madre-hija (D7) y —al borde— color AB en la cabecera (D3). Ninguna es una suma.

---

## 7. Contraste de fuentes (calidad de datos)

- OKR (KH0498) y KFG coinciden en **490 cuerdas y 725 racimos**, pero **no en la forma del árbol**: OKR pone 247 cuerdas en su nivel 2 (el primero de las subsidiarias) y KFG 185; KFG tiene 4 cuerdas en el quinto nivel de subsidiarias y OKR solo 1. Cualquier análisis de profundidad depende de la fuente.
- `knot_cluster.TOTAL_VALUE` de OKR está **vacío (0)** para este quipu: los valores solo existen en KFG. No hay verificación independiente de los valores.
- `alt` está vacía en todo el corpus; no hay lectura alternativa que contrastar.

---

## 8. Lectura propuesta: ¿qué registro es?

**Filas (grupos).** Siete secciones: una cabecera de 3 cuerdas AB con las cifras mayores (3.088 / 627 / 2.310) y seis grupos de 18–27 colgantes. Los grupos difieren en escala (G1: mediana 495; G7: mediana 23; G4: mediana 0 con 18 de 27 colgantes vacíos) y en densidad (G1: 53 subsidiarias en 18 colgantes; G4: 27 en 27). Esa heterogeneidad es la que se espera de **clases de producto distintas** o de **sectores/partidas distintas**, no de una lista homogénea de personas.

**Columnas (niveles).** El colgante es la entrada; las subsidiarias son su subdivisión (parciales, segundo conteo, o el mismo lote en otra unidad). No suman: **repiten o refinan**. La distribución lo respalda: las subsidiarias de nivel 1 son más grandes que los colgantes y concentran los valores de miles.

**Lo que NO es.**
- **Censo:** no hay unidades de 10/100 personas, ni estructura de edades; no se observan mitades hanan/hurin; el rango y la forma de los valores no lo sugieren.
- **Calendario:** ningún ciclo de 328/354/360/365; 7 grupos no son 12 meses ni 41 semanas; los tamaños 18–27 no son múltiplos calendáricos.
- **Tributo sumatorio:** no hay totales, ni cuotas repetidas (D1), ni razón 1/10, ni cuerdas superiores.
- **Depósito/almacén:** es lo que el contexto arqueológico indica (kallanka U.A. 02 del Qolqawasi de Inkawasi) y lo que la forma —lista anidada de lotes con cabeceras y controles— permite.

**Literatura.**
- Urton y Chu (2015, *Latin American Antiquity* 26(4)) describen el archivo de Inkawasi como contabilidad de depósito estatal, con **pares atados de registros muy similares** ("checks-and-balances") y posibles **unidades contables estandarizadas** para ají, maní y frijol. La función contable está **apoyada con datos**; la identificación de productos y unidades es **propuesta**. Nuestros D7 (duplicados madre-hija) encajan con la lógica de control, pero a escala de una sola cuerda, no de quipus emparejados.
- Urton (2017, cap. 9) sitúa **UR262–265 y UR280 en la kallanka U.A. 02** y describe "internal summing" y "fixed values" (208, 47, 15, 10) en *otros* quipus del archivo. **UR262 no muestra ni lo uno ni lo otro.**
- El informe interno `13_sistema_incahuasi` ya clasificaba a UR262 como **no enlazado** al "sistema" de totales de UR266/UR278; nuestros resultados son consistentes con eso y lo cuantifican.
- Clindaniel (2019) documenta para Inkawasi 6.209 nudos Z frente a 1.704 S (78 %/22 %) y un uso del color como marcador en casos piloto (UR267A, UR255). UR262 es **mucho más uniforme que la media del archivo** (724 Z / 1 S) y usa AB como marcador de profundidad/cabecera, no como suma/resta: no replica el sistema W/AB/MB de UR267A.

**Nivel de evidencia.**
- *Demostrado (descriptivo, este quipu)*: 490 cuerdas, 138 colgantes, 352 subsidiarias, profundidad 5, 23,5 % sin nudos, torsión S 100 %, 724 Z/1 S, cero cuerdas superiores, decimalidad con L/E en unidades y E para el 1 (con la excepción de `p15s4s1`).
- *Apoyado con datos*: ausencia de sumas internas (A1–A5, A7); cabecera de grupo = colgante mayor (D6); duplicación madre-hija (D7); color AB asociado a profundidad y a cabeceras (D3/D4).
- *Propuesto*: que sea un registro de depósito con filas = productos/sectores y columnas = subdivisiones de cada entrada.
- *Especulativo*: que cada grupo sea un producto concreto (ají/maní/frijol) o que las posiciones 12–13 marquen una división en dos mitades del grupo.

---

## 9. Anomalías y lo que no encaja

1. **`p138` (grupo 8)**: 80 cm, sin nudos, `union` V, nota "tie cord". No es dato: es la **cuerda de amarre** del quipu. Debe excluirse de cualquier estadística de valores (yo la excluyo de los grupos de datos).
2. **`p22` (grupo 2)**: cuerda AB aislada, sin nudos, entre G1 y G3. Probablemente un **separador** físico, no una entrada vacía.
3. **G0**: tres cuerdas AB con la cifra más alta del quipu (3.088) y otras dos grandes (627, 2.310), sin relación aritmética con los demás grupos (0 casos de total repetido). Es una **cabecera**, pero no sabemos de qué: podría ser un resumen en otra unidad, un lote aparte o una etiqueta de identificación.
4. **G4**: 27 colgantes, 18 sin nudos y mediana 0. Parece una **plantilla/formedero a medio llenar** más que un grupo con datos: un tramo preparado con posiciones y sin valores.
5. **Vacío estructural**: 115 cuerdas sin nudos (23,5 %), 40 de ellas colgantes. En términos de registro, son **posiciones ausentes**, no ceros. Su concentración en G3/G4 (23 y 28) sugiere secciones incompletas o no usadas.
6. **Unidades partidas en dos racimos (11 cuerdas):** el dígito de unidades se anuda como dos racimos contiguos (`4L+1E`, `7L+1E`, `4L+2L`…), no como un único nudo largo. En 10 casos la suma da el dígito correcto; en `p15s4s1` (`9L+1E` = 10 con valor 110) la lectura es ambigua. Es el único "nudo raro" sistemático del quipu; puede ser una convención de quien anudó o de quien transcribió.
7. **Un solo nudo S** (`p11s1s1`, simple de 30) en 725 racimos: podría ser un error de transcripción o una marca deliberada; con un caso no se decide.
8. **La razón ~6,8** (8 pares) es el único patrón "tentador" que encontré y **no resiste** la corrección por selección de ventana. Lo dejo como curiosidad, no como hallazgo.
9. **AB en posiciones 12–13** en los cuatro grupos mayores (G4: 12 y 22; G5: 13; G6: 13; G7: 13) y en 20–21 en G6/G7. Es compatible con una división en bloques de ~12 o en dos mitades, pero con 4 grupos y sin sumas que la respalden es **especulativo**.
10. **Discrepancia KFG/OKR en la profundidad del árbol** (§7): afecta a cualquier conclusión sobre "subsidiarias de subsidiarias".

**¿Información no numérica?** Sí, y es poca: (a) el **color** (AB vs NB) marca profundidad y cabeceras, un eje categórico independiente del valor; (b) la **posición/espaciado** define los grupos (7 secciones a ~7 cm); (c) la **cuerda de amarre** final es un cierre físico, no un dato. La torsión (toda S), la terminación y la dirección de nudo no varían lo suficiente para portar información: son constantes de manufactura.

---

## 10. Resultados negativos (explícitos)

- No hay suma colgante = subsidiarias (2/105, p = 0,07; y los 2 casos son copias, no sumas).
- No hay totales de grupo en ninguna cuerda (0 vs 6,7; p = 1).
- No hay cuerdas superiores: `union` T = 0. La prueba clásica no es aplicable.
- No hay cuerdas superiores = suma de grupo, ni grupo = suma de grupos.
- No hay exceso de bloques contiguos que sumen un colgante (26 vs 22; p = 0,31).
- No hay exceso de valores repetidos/cuotas (201 vs 256; p = 1): no se replican los "fixed values" de Urton.
- No hay similitud especial entre colgantes adyacentes (p = 0,18).
- No hay periodicidad de color demostrable (p = 0,08).
- No hay razón constante (el 6,8 no sobrevive la corrección post hoc).
- No hay código de longitud: la correlación largo–valor es mecánica (ρ parcial = −0,11).
- No hay estructura calendárica ni de censo.

---

## 11. Limitaciones

- Un solo quipu: nada de esto se generaliza sin replicar en UR263–265 y UR280 (misma kallanka).
- Los valores dependen de una sola transcripción (KFG); OKR no tiene valores para KH0498.
- El árbol KFG y el de OKR discrepan en profundidad.
- El contexto físico (producto asociado, posición exacta en la kallanka, agrupación de quipus atados) **no está en los datos abiertos**; es la pieza que más añadiría.
- Potencia: con 6 grupos y 8 duplicados, los efectos locales son frágiles; los p de 0,003–0,007 no deben leerse como tamaños de efecto grandes.

---

## 12. Para el coordinador

- **UR262 es el quipu más grande de Incahuasi** (490 cuerdas; mediana del archivo 76) y el más anidado (352 subsidiarias, 5 niveles). Cualquier caracterización del archivo tiene que contar con él.
- **No es un quipu de sumas.** Cero cuerdas superiores, cero totales de grupo repetidos, 2/105 "colgante = hijas" (y son copias). El "internal summing" que Urton atribuye al archivo **no aparece aquí**; confirma la clasificación previa de UR262 como no enlazado al sistema de UR266/UR278.
- **Tampoco es censo, calendario ni tributo sumatorio.** No hay cuotas repetidas (los "fixed values" 208/47/15/10 de Urton no se replican: 0, 3, 1 y 21 casos), ni ciclos, ni razón 1/10.
- **La gramática del quipu es limpísima:** 100 % torsión S, 724 nudos Z y 1 S, decimalidad casi perfecta (unidades siempre en nudo largo o figura de ocho, el 1 siempre en E), con una sola excepción de lectura (`p15s4s1`, unidades partidas 9+1 = 110). Un solo taller/mano.
- **El color AB no es un código de columna: es un gradiente de profundidad** (11 % de los colgantes, 30 % del nivel 1, 60 % del nivel 2; χ² p ≈ 10⁻²⁴) y tiende a marcar la **cabecera** de los grupos (3/6; p = 0,007 exacto, aunque no sobrevive Holm: 0,067).
- **Cabecera de sección (apoyado):** el primer colgante del grupo es el mayor en 3/6 grupos (esperado 0,29; p = 0,003). No es la suma del resto: es una entrada principal, no un total.
- **Duplicación madre-hija (apoyado, efecto pequeño):** 8 pares con el mismo valor ±1 % frente a 2,3 esperados (p = 0,004), p. ej. `p71`=`p71s1`=54, `p92`=1.146 vs `p92s1`=1.151. Encaja con los "checks-and-balances" de Urton y Chu (2015), pero a escala de cuerda, no de quipu emparejado.
- **Lectura propuesta:** registro de depósito/almacén. Filas = 7 secciones (productos o sectores; G0 es una cabecera AB de tres cifras grandes); columnas = niveles de subdivisión de cada entrada, que **repiten o refinan** pero no agregan. Nivel: *propuesto* (contexto) / *apoyado* (forma de lista anidada) / *demostrado* (estructura física y decimal).
- **Siguiente ronda:** (1) replicar estos detectores en UR263, UR264, UR265 y UR280 (misma kallanka) para ver si el "no-sumatorio" es del sitio o del lote; (2) buscar el contexto de excavación (producto asociado, quipus atados) en Chu 2013–2014 o en los cuadernos de Urton; (3) contrastar el árbol KFG vs OKR antes de cualquier análisis de profundidad; (4) probar si los bloques de ~12 colgantes (marcados por AB en 12–13) son unidades de otra partición, con más quipus.
