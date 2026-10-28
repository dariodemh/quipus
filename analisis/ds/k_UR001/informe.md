# UR001 / KH0237 — Lectura profunda de un solo quipu

**Equipo `k_UR001`** · 2026-10-17 · scripts en `analisis/ds/k_UR001/`

---

## 0. Pregunta

¿Qué tipo de registro es UR001 (Leymebamba, 572 cuerdas)? ¿Qué representan sus filas y columnas?
Objetivos: (1) reconstruir su estructura completa; (2) buscar toda la aritmética interna frente a un
modelo nulo; (3) proponer la lectura más probable con literatura y nivel de evidencia; (4) señalar
las anomalías y si hay información no numérica.

## 1. Método

- **Datos:** `analisis/datos/{cuerdas,grupos,quipus}.csv` (KFG), consultados con pandas (nunca impresos enteros).
- **Unidad de análisis:** el quipu. UR001 es un único quipu, así que los contrastes a nivel de cuerda
  usan **permutaciones dentro del quipu** (evita pseudorreplicación, regla 1 del BRIEF).
- **Modelo nulo explícito:** barajar los **valores** (o los **colores** / la variable bajo prueba) entre las
  cuerdas del propio quipu, **1000 veces, semilla fija 0**; se conserva el multiconjunto de valores.
  Para el color se añadió un **nulo por bloques de 5** (baraja bloques contiguos, preservando los
  runs locales) para no confundir autocorrelación de corto alcance con periodicidad.
- **p-valor empírico** = (n.º de permutaciones ≥ observado + 1)/(N+1). Se usa el extremo relevante.
- **Comparaciones múltiples:** se probaron ~12 contrastes; con **Holm–Bonferroni** a α=0.05 sobreviven
  los positivos con p≤0.002 (color/runs) y no cambian los negativos (p≥0.69).
- **Advertencias del BRIEF aplicadas:** `valor==0` con `nudos` vacío = cuerda **sin nudos** (no un cero real);
  el museo (Centro Mallqui) **no** se usa como procedencia de origen (la ficha declara procedencia *Leymebamba*, región *Chachapoyas*).
- **Etiquetas:** bien apoyado / apoyado con datos / propuesto / especulativo.

## 2. Estructura (script `01_estructura.py`)

Metadatos: museo Centro Mallqui; procedencia declarada **Leymebamba**, región **Chachapoyas**;
cordón principal 147 cm, color `W-B`, estructura `P`. Es uno de los ~32 quipus de la Laguna de los Cóndores (Urton 2005).

| Rasgo | Valor |
|---|---|
| Cuerdas totales | **572** |
| Colgantes (nivel 0) / sub. nivel 1 / nivel 2 | 407 / 146 / 19 (profundidad máx. **2**) |
| Grupos KFG de colgantes | 48 (mediana **1**, máx. 34) |
| Cuerdas con nudos | 318 (55.6 %) |
| Cuerdas **sin nudos** | **254 (44.4 %)** → 228 colgantes + 26 subsidiarias |
| Unión **T (cuerda superior)** | **0** |
| Unión R / V / U / Unknown | 255 / 206 / 95 / 16 |
| Torsión S / U | 550 / 22 |
| Colores distintos | 21; AB 150, W 126, MB 106, KB 38, GG 31, HB 26, PK 20; 57 cuerdas moteadas (`:`) |
| Dirección de nudo S / **Z** / U | 9 / **454** / 4 |
| Valor máximo | 8 308 (suma de colgantes 76 187) |

**Estructura periódica de bloques.** Los 48 grupos KFG son engañosos: 25 son **grupos de una sola cuerda**.
`05_periodicidad.py` y `06_segmentos.py`: **20 cuerdas son de color `PK`** (rosa), de las cuales 19 **no tienen
nudos** y su unión es mayoritariamente `Unknown`/`U`. Excluyendo tramos donde faltan separadores,
los `PK` dividen la secuencia de colgantes en **bloques de ~16–18 cuerdas** (tamaños observados: 17,17,17,17,17,17,16,16,15,15…).
Es decir, la unidad real no es el "grupo" KFG sino el **bloque entre dos cuerdas `PK`**.

## 3. Aritmética interna (scripts `02`, `04`, `11`) — casi todo NEGATIVO

Todos los tests de suma **fallan** o caen por debajo del azar:

| Test | Observado | Nulo (media / máx) | p | Lectura |
|---|---|---|---|---|
| Colgante = Σ subsidiarias directas | **8 / 63** (12.7 %) | 13.8 | **0.977** | **negativo** (peor que azar) |
| Colgante = Σ de **todas** sus descendientes | 8 / 63 | — | — | igual |
| Valor 0 con nudos | 0 | — | — | consistente (0 = ausencia) |
| Alguna cuerda = Σ del resto de su grupo | 0 / 22 | 0.1 | 1.000 | **negativo** |
| 1.er colgante del grupo = Σ del resto | 0 / 6 | — | — | **negativo** |
| Suma **categórica por color** = valor existente (relación de Ascher) | 3 / 15 | 3.2 | 0.906 | **negativo** |
| Razones hija₁/hija_k constantes (==1) | 19 % (mediana 0.5) | — | — | sin proporción constante |
| Valores repetidos | 228 cuerdas en 20 valores | — | — | trivial (enteros pequeños 1–8, 22) |

**Los 8 "aciertos" de la primera fila son triviales:** todos son casos de una cuerda con valor 1 y una única
hija con valor 1. **No hay ninguna igualdad aritmética no trivial en todo el quipu.**

Esto es coherente con el estado del arte: K-CAT mide que la suma jerárquica "grupo padre = Σ hijos" solo
se cumple en ~6.6 % del corpus (Medrano y Khosla 2024 generalizan las *relaciones de Ascher*, que son sumas
**entre colgantes o por color**, no la suma jerárquica). UR001 **no es un quipu "sumatorio"** estilo Puruchuco
(Urton y Brezine 2005), y **no tiene cuerdas superiores** (`union T = 0`) pese a que Locke las considerara
la clave del carácter numérico.

## 4. Color y periodicidad (scripts `05`, `07`, `08`, `09`) — POSITIVO

- **Runs de color** en colgantes: obs 178 vs nulo 334, **p=0.001** → los colores están agrupados.
- **Homogeneidad de color dentro de grupo** (pares adyacentes iguales): obs 223/406 vs nulo 88, **p=0.001**.
- **Coherencia de color por lag** (matriz `09`): lags 1–4 altos (runs locales de ~5); y un **pico claro en lags 12–22**.
  Con el **nulo por bloques de 5** (que preserva los runs locales) los lags 12–20 siguen siendo significativos, **p=0.002**.
  → **Periodicidad real de ~16–17 cuerdas**, no explicable por el agrupamiento local de color.
- **Riqueza (tiene nudo) por lag:** máximo en **lag 17** (obs 0.628 vs nulo 0.505, p=0.005) y 34–35 → refuerza el período.
- **Contra-prueba (negativa):** la **separación entre cuerdas `PK`** NO es más regular que el azar
  (CV obs 0.969 vs nulo 0.902, p=0.694); hay huecos de 74 y 82 cuerdas donde faltan separadores.

**Matriz alineada** (`09_matriz.py`, 16 bloques de ≥15 cuerdas, alineados por posición relativa): cada bloque
se divide en **3 unidades de color de ~5 cuerdas** (p. ej. `W·W·W·W·W | AB·AB·AB·AB·AB | KB·KB·KB·KB·KB`).
Los **valores se concentran al final de cada unidad de color**:
prop. de celdas con valor por columna = col4 **0.88**, col5 **0.94**, col10 **0.69**, col15 **0.79**, col16 **0.83**;
mientras que col1, col2, col8, col12 son casi siempre vacías (0.00–0.19).

Ejemplo (dos bloques, valores alineados por columna):
```
B01  .  1  .  1  105 3101  .  .  .   1  .  1  .  .   6 4005  1  .
B04  .  1  .  .   27 4501  .  .  .   . 605 .  .  .   1 4104  1
```
El patrón "celdas vacías + valor al cierre de cada unidad de color" se repite en los 16 bloques.

## 5. Lectura propuesta

**Cuerdas decimales confirmadas (bien apoyado).** Los valores grandes están en notación decimal posicional
correcta:
`p81 = 8S(8000)+3S(300)+8L(8) = 8308`; `p70=8201`; `p389=5490`; `p153=4501`. Es decir, **la técnica de
registro numérico decimal está presente y bien aplicada**.

**Tipo de registro (propuesto).** El conjunto de rasgos —(a) sistema decimal en los valores grandes,
(b) estructura **tabular periódica** de ~16–17 cuerdas por bloque, (c) bloques **separados por cuerdas `PK`**
sin nudos, (d) cada bloque subdividido en **3 unidades de color de ~5**, (e) valores situados al cierre de
cada unidad de color, (f) **sin aritmética sumatoria**— es el de una **tabla de conteos categorizados**, no
un recuento jerárquico sumado.

Lectura más probable: **registro administrativo tabular de censo/tributo** (conteos por categoría), del tipo
que Urton (2001, 2005) propone para el archivo de la Laguna de los Cóndores: UR6 se lee como **censo de
contribuyentes + calendario**, y UR1 es parte del mismo archivo (22 khipus estudiables, sitios LC1, chullpas 3–4).

- **Filas** ≈ cada **bloque** delimitado por `PK` (≈20–25 filas): una unidad registrada
  (una parcialidad/ayllu/hogar, o un período).
- **Columnas** ≈ las **3 unidades de color de ~5 cuerdas** por bloque: **categorías** (p. ej. grupos
  demográficos o clases de bien/obligación), cuyo conteo cae en la cuerda de cierre de la unidad.
- **Cuerdas "hub"** (`p1`=17 hijas, `p230`=16, `p232`=20, `p301`=21, todas de valor 0) actúan como **índices/listas**
  de categorías (sus subsidiarias tienen conteos pequeños 1–5), no como totales: **ninguna es la suma de sus hijas**.

Nivel de evidencia: **apoyado con datos** para "registro decimal estructurado en tabla periódica con
categorías de color y separadores `PK`"; **propuesto** para la etiqueta "censo/tributo" (no hay control
documental ni coincidencia con un censo conocido, igual que en UR6).

**Alternativas consideradas y por qué son menos probables:**
- *Calendario*: UR6 se lee como calendario porque tiene **24 conjuntos de 29–31 cuerdas** (≈2 años de 365 días).
  UR001 **no** tiene 24 conjuntos de ~30; tiene bloques de ~16–17 y 44 % de cuerdas vacías. No se ajusta al molde calendárico.
- *Depósito/almacén (sumatorio)*: descartado porque **no hay cuerdas superiores ni sumas** (p≈0.98–1.0).
- *Quipu narrativo/no numérico*: improbable, porque los valores grandes están en **decimal correcto** y bien formado.

## 6. Anomalías y "lo que no encaja"

1. **44 % de cuerdas sin nudos** (254/572; 228 colgantes). No son ceros: son cuerdas **vacías/placeholder**.
   Es la anomalía más llamativa y la que más se aparta del quipu "sumatorio" clásico.
2. **No hay cuerdas superiores** (`union T = 0`), justo el rasgo que Locke y Ascher usaron como prueba del
   carácter numérico. UR001 codifica sin resúmenes.
3. **Dirección de nudo casi uniforme:** 454 Z vs 9 S (y torsión S 550/22). Contraste con la tesis binaria
   S/Z (Urton 2003): aquí el canal S/Z está prácticamente **libre/no usado** → poco probable que codifique
   información relevante. (Ascher 2005 ya mostró que spin/ply/dirección **no** distinguen datos numéricos de no numéricos.)
4. **Unión R/V mezclada** (255 R / 206 V / 95 U), sin patrón categórico limpio; coincide con el hallazgo de
   que R/V (nulos de permutación) no añade estructura clara a escala de corpus.
5. **`p394`** (color `W:KB`, unión R, valor 8, con 4 subsidiarias de valores 8/1/1/1) y `p398` son atípicas.
6. **Profundidad máxima 2** (146 sub-nivel-1 + 19 sub-nivel-2): árbol **plano**, muy por debajo de la media
   de la KDB (hasta 6 niveles; ~1/4 de quipus con subsidiarios).
7. **Puede haber información no numérica** en: el **color** (21 códigos, fuerte estructura de bloques;
   pero Milillo et al. 2023 advierten que el color registrado a ojo puede no ser el original) y en las
   **cuerdas vacías** (posibles separadores/marcas), pero **no** en la dirección de nudo (casi uniforme).

## 7. Resultados negativos (explícitos)

- No hay suma colgante = Σ subsidiarias (p=0.977; observado **por debajo** del azar).
- No hay suma de grupo ni cuerda superior sumatoria (0/22; p=1.0).
- No hay suma categórica por color (p=0.906).
- No hay razones constantes entre hermanas.
- La separación de las cuerdas `PK` **no** es significativamente más regular que el azar (p=0.694).
- No hay estructura calendárica de 24 conjuntos tipo UR6.

## 8. Nivel de evidencia (resumen)

| Afirmación | Nivel |
|---|---|
| UR001 usa el sistema **decimal posicional** (valores grandes bien formados) | **bien apoyado** (lectura interna verificada) |
| Estructura **periódica** de ~16–17 cuerdas y bloques separados por `PK` | **apoyado con datos** (p=0.002 sobre nulo por bloques) |
| **Categorías de color** por unidades de ~5 con valores al cierre | **apoyado con datos** |
| **Ausencia** de aritmética sumatoria interna | **apoyado con datos** (varios tests, p≥0.9) |
| Es un registro de **censo/tributo tabular** | **propuesto** |
| Cuerdas "hub" = índices de categorías | **propuesto** |
| Color como canal semántico de categorías | **especulativo** (depende de color fiable) |

## 9. Para el coordinador

- **UR001 no es un quipu "sumatorio".** Ningún test de aritmética interna pasa: colgante ≠ Σ subsidiarias (8/63, y triviales; p=0.977 — por *debajo* del azar), ni suma de grupo, ni suma por color (p=0.906), ni razones constantes. **No hay cuerdas superiores** (union T=0).
- **Sí es un quipu decimal bien formado.** Los valores grandes están en notación posicional correcta (p. ej. p81=8308 = 8000+300+8). El sistema numérico está **bien apoyado**; lo que falta es la aritmética de agregación.
- **Hallazgo fuerte y nuevo: es tabular y periódico.** Hay un **período de ~16–17 cuerdas** (color y "tiene nudo" se repiten; p=0.002 frente a un nulo que preserva runs locales). Los bloques están separados por **20 cuerdas `PK` (rosa) sin nudos**.
- **Estructura interna de los bloques:** cada bloque se divide en **3 unidades de color de ~5 cuerdas** y los **valores se concentran al cierre de cada unidad** (col4-5, col10, col15-16 ricas al 79–94 %; col1-2-8-12 vacías). Esto es lo que da la lectura "filas × columnas".
- **Cuerdas "hub"** p1/p230/p232/p301 (valor 0, 16–21 subsidiarias de conteos pequeños) parecen **índices de categorías**, no totales. Ninguna es suma de sus hijas.
- **Anomalías:** 44 % de cuerdas sin nudos; dirección de nudo casi uniforme (454 Z vs 9 S) → el canal S/Z está prácticamente sin usar; árbol plano (profundidad máx. 2).
- **Lectura más probable (propuesta):** registro administrativo **tabular de censo/tributo** del archivo de la Laguna de los Cóndores, hermano de UR6 (que Urton 2001/2005 lee como censo + calendario). **Filas** = bloques (unidades registradas); **columnas** = categorías de color de ~5 cuerdas; celdas = conteos decimales.
- **La alternativa calendárica es menos probable:** UR6 se apoya en 24 conjuntos de 29–31 cuerdas; UR001 no los tiene (bloques de ~16–17).
- **Recomendación siguiente ronda:** (1) testar el mismo patrón periódico + `PK` en **todos los `UR###` de Leymebamba** para ver si el período ~17 y los separadores `PK` son firma de la colección; (2) buscar si las **3 unidades de color** tienen un orden/etiqueta estable entre quipus del archivo; (3) cruzar los conteos con UR6/UR9/UR21 (posible cuenta duplicada, como los pares de Urton 2005), con control de multiplicidad.
- **Cautela:** color y valor son datos **inciertos** (Thompson 2025; Milillo 2023). Toda lectura de color aquí es **propuesta/especulativa**, no bien apoyada.
