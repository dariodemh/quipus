# Canutos, canutitos y fibra: qué marcan y con qué se asocian

**Equipo:** `t_canutos_fibra` · **Fecha:** 2026-10-18 · **Unidad de análisis:** el quipu
**Semilla:** 20241018 · **Scripts:** `01_construir.py` … `10_multiplicidad.py` (esta carpeta)

---

## 1. Pregunta

1. ¿Qué quipus tienen **canutos** (envolturas del cordón principal) y **qué marcan**?
2. ¿La **fibra** (algodón vs camélido) se asocia a **valor, color, posición o procedencia**?

Subproducto necesario: los **canutitos** (envolturas de hilo en el extremo de una cuerda,
terminación `TT`) son un fenómeno distinto del canuto y se analizan aparte, porque la base
los mezcla.

## 2. Datos y método

**Fuentes.** OKR `khipu.db` (619 quipus): tablas `canuto` (236 filas), `canutito` (493),
`canuto_cluster` (70), `ascher_canuto_color` (994), `ascher_canutito_color` (465),
`cord.FIBER` (57 818 cuerdas), `primary_cord.FIBER`. KFG `khipu_summary.csv` (650 quipus,
campo `num_canuto_cords`) y `analisis/datos/cuerdas.csv`. La tabla `fiber_dc` del OKR
documenta los códigos: **CN = algodón, CL = camélido** (no al revés), W = lana de oveja,
H = cabello humano, CC = mezcla, V = vegetal, AH = pelo animal.

**Unión cuerda↔valor.** El OKR no trae el nombre jerárquico de la cuerda. Se reconstruyó
caminando `PENDANT_FROM` + `CORD_ORDINAL` (`02_cuerdas.py`) y se unió con `cuerdas.csv`:
**51 910 de 54 403 cuerdas (95,3 %)** quedan con valor/color/grupo; el largo OKR y el KFG
correlacionan **r = 0,985** (n = 50 445), lo que valida la unión.

**Reglas aplicadas.** Unidad = quipu en todas las pruebas entre quipus. Cuando se baja a
cuerda, el nulo **permuta dentro de cada quipu** (nunca entre quipus), de modo que ningún
efecto pueda deberse a diferencias entre objetos. Todos los p-valores son empíricos
(20 000 permutaciones, salvo los indicados). Corrección **Benjamini-Hochberg** por familia
(`10_multiplicidad.py`). `valor = 0` con `nudos` vacío se trata como ausente, no como cero.

**Advertencia de calidad de datos.** Los campos geométricos del canuto son internos y
parcialmente incoherentes: `ATTACH_POS = 0` en los 236 canutos, `NUM_LOOPS = 0` en todos,
`CTO_LEVEL = 1` en todos, y en KH0280 los 29 canutos de 9–10,5 cm cabrían en 28 cm de
cordón principal. **No se usan longitudes ni posiciones de canuto** para nada inferencial.
`canutito.KHIPU_ID` está en 0 en las 493 filas: el quipu se recuperó por `CORD_ID`.

---

## 3. Resultados: canutos

### 3.1 ¿Cuántos quipus y en qué régimen?

- En el corpus KFG, **179/650 quipus (27,5 %)** tienen al menos un canuto.
- La distribución es **bimodal**: 86 quipus (13,2 %) tienen ≤5 % de sus cuerdas envueltas
  (marcas puntuales) y solo **27 (4,2 %) tienen ≥50 %** envuelto; 4 llegan al 100 %, pero son quipus de 3–10 cuerdas (Incahuasi), no objetos grandes.
- En el OKR solo **8 quipus** tienen registro detallado (236 canutos, 70 clusters,
  887 cuerdas con `CANUTO_ID`):

| OKR | KFG | cuerdas | canutos | clusters | cuerdas en canuto | zona | fibra |
|---|---|---|---|---|---|---|---|
| KH0289 | UR055 | 180 | 42 | 10 | 180 | desc. | s/d |
| KH0280 | UR050 | 164 | 29 | 5 | 164 | desc. | CL |
| KH0288 | UR054 | 115 | 29 | 7 | 115 | desc. | CL |
| KH0282 | UR052 | 98 | 25 | 9 | 98 | desc. | CL |
| KH0384 | UR144 | 96 | 24 | 2 | 96 | Paracas/Pisco | CL |
| KH0271 | UR039 | 91 | 45 | 1 | 91 | Huari | CN |
| KH0346 | UR110 | 89 | 22 | 5 | 89 | desc. | CL |
| KH0348 | UR112 | 76 | 20 | 5 | 76 | desc. | CL |

**Donde hay registro fino, el canuto no es puntual: cubre todas las fijaciones del quipu**
(909 cuerdas declaradas vs 887 con `CANUTO_ID`, 97,6 %). Es un rasgo de **objeto completo**,
no una marca selectiva.

### 3.2 ¿Qué envuelve un canuto?

Cada canuto envuelve la fijación de un grupo chico de colgantes al cordón principal:
**mediana 4 cuerdas** (media 3,85; rango 1–6), `CTO_LEVEL = 1` siempre, largo declarado
mediano 6,5 cm. Los canutos se agrupan en **clusters** (mediana 3 canutos por cluster,
separados por un espacio). Es decir: la envuelta es un tubo que recorre el cordón principal
en tramos, y cada tramo cubre ~4 colgantes consecutivos.

### 3.3 ¿Los límites del canuto coinciden con límites de grupo? **Sí** (el hallazgo central)

En 7 de los 8 quipus el detector de grupos del KFG es degenerado (164 grupos para 164
cuerdas en KH0280, etc.): los canutos rellenan los espacios que el algoritmo usa para
separar grupos, así que no hay contraste posible. El único quipu con grupos reales es
**UR052/KH0282: 98 cuerdas en 24 grupos y 9 clusters de canuto**.

- **23 de los 24 límites de grupo coinciden exactamente con un límite de canuto.**
- Jaccard observado = **0,885**; nulo de 24 límites aleatorios: p = **5 × 10⁻⁵**
  (20 000 permutaciones).

Esto es lo más fuerte que tenemos: **el canuto delimita grupos de colgantes**. Con la
salvedad de que el detector de grupos del KFG pudo haberse apoyado en el mismo rasgo visual,
por lo que la coincidencia no es del todo independiente.

### 3.4 ¿Los canutos llevan información de color? Sí, y es **independiente** del color de las cuerdas

- **173/236 canutos** tienen color registrado; el canuto está pintado en **1–4 bandas** de
  ~3 cm (mediana 3). En KH0280: `YB-VB-PR`, `AB-PR-VB`, `W-PR-VB`, `PR-KB-G0`,
  `KB-YB-PR`, `R-KB-YB`, `VB-G0-PR`.
- Las secuencias **se repiten en runs de canutos consecutivos** (KH0280: 29 canutos →
  8 secuencias distintas en 9 runs; 2–10 secuencias por quipu).
- El 63 % de las transiciones entre secuencias consecutivas comparten ≥2 bandas, frente a
  **42 % esperado por azar** con esta paleta: hay estructura de corrimiento, pero débil.
- **El color del canuto NO coincide con el color de las cuerdas que envuelve**: solape
  0–10 % y **ningún quipu significativo** (p = 0,63–1,00, 8 pruebas). En KH0280 las cuerdas
  usan 2 colores y los canutos 8. La envuelta **añade una capa de color propia**, ortogonal
  a la de los colgantes.

### 3.5 ¿Los segmentos de canuto son unidades contables? **No**

Para los 8 quipus se calculó la suma de valores por segmento de canuto y se comparó con
3 000 reordenamientos aleatorios de las cuerdas con la misma distribución de tamaños:
- Sumas "redondas" (múltiplos de 10): **14,1 % observado vs ~10 % esperado**; solo 1 de 8
  quipus alcanza p<0,05 (UR055, p = 0,008), que **no sobrevive a BH** (q = 0,08).
- Homogeneidad interna de las sumas: ningún quipu por debajo del azar (p = 0,27–1,00).

**El canuto no agrupa cuerdas por su aritmética.** Es un delimitador material, no una
unidad de suma.

### 3.6 Perfil de los 8 quipus envueltos

Frente al resto del corpus (medianas): **97 cuerdas vs 39**, **2,5 colores vs 6**,
**0 subsidiarias vs 2** (todos los 8 tienen cero; Mann-Whitney de la proporción de
subsidiarias p = 0,0035), y **7 de 8 con ≥69 % de nudos en dirección S**. Es un estilo
coherente: grande, plano (sin jerarquía), monocromo y S.

### 3.7 Canutitos: otra cosa, y también informativa

- **493 canutitos** en **467 cuerdas** de **8 quipus** (los mismos ocho salvo KH0288/UR054, más
  KH0281/UR051). El **100 % está en cuerdas de nivel 1**: nunca en una subsidiaria
  (0/5 subsidiarias disponibles).
- Están en el **extremo** de la cuerda: mediana al **96 %** del largo (media 89 %); largo
  mediano 3 cm. Son, literalmente, un **hilo de color atado al extremo**.
- Cobertura por quipu **muy desigual**: de 1,1 % (UR039) a 87,5 % (UR144) de las cuerdas.
  No es un marcador raro: en 4 quipus marca más de la mitad.
- **Paleta propia**: los canutitos usan colores que las cuerdas no usan (KH0289: 19 colores
  de canutito vs 4 de cuerda; KH0280: 5 vs 2); la coincidencia de color canutito↔cuerda es
  del **1,3 %** (n = 465). El hilo es deliberadamente **contrastante**.
- **Fibra del canutito: 465/465 CL (camélido).**

Selectividad dentro de cada quipu (AUC por quipu, nulo intragrupo, BH):

| variable | AUC medio | p | q (BH) |
|---|---|---|---|
| tiene valor > 0 | 0,520 | 0,0075 | **0,015** |
| log₁₀(valor) | 0,502 | 0,97 | 1,00 |
| color blanco | 0,473 | 0,0015 | **0,004** |
| nivel de cuerda | 0,496 | 0,35 | 0,45 |
| largo de cuerda | 0,650 | 5 × 10⁻⁵ | **0,0002** |

Efectos **reales pero pequeños**: las cuerdas marcadas están algo más a menudo anudadas
(AUC 0,52) y son más largas (AUC 0,65); **no** difieren en la magnitud del valor (AUC 0,502,
el negativo más limpio del informe) ni en el nivel. El efecto "blanco" se apoya en 4 quipus
con 0–4 cuerdas blancas: **no es robusto**.

---

## 4. Resultados: fibra

### 4.1 La fibra es un atributo del **objeto**, no de la cuerda

- Códigos: **CN 28 895 cuerdas (53 %)**, **CL 1 373 (2,5 %)**, **sin dato 22 995 (42 %)**,
  otros 1 134.
- De los 297 quipus con fibra codificada: **277 solo algodón**, **20 con camélido**
  (13 puros, 7 mixtos), es decir **6,7 %**.
- La fibra del **cordón principal predice la de los colgantes**: PC camélido → 14/18 quipus
  con camélido; PC algodón → 346/349 sin camélido (χ² = 212, n = 367).
- Solo **1 quipu** (KH0281/UR051: 31 CL vs 35 CN) tiene ≥10 cuerdas de cada fibra. **La fibra
  no se puede contrastar contra valor/color/posición dentro del quipu**, salvo en ese caso
  (y allí todo es nulo: log valor p = 0,32; blanco p = 1,00).

### 4.2 La fibra **falta de forma no aleatoria** (sesgo de registro)

**283/650 quipus (44 %) no tienen ni una cuerda con fibra codificada.** La falta se concentra
por colección: Museum für Völkerkunde Berlin **97,9 %** sin dato, Museo de Sitio de
Pachacamac **96,9 %**, AMNH **90,3 %**; en cambio Incahuasi, Armatambo, Museo Regional de Ica
y Puruchuco tienen **0 %** de falta (χ² por zona p = 9,6 × 10⁻²⁶). Cualquier conclusión sobre
fibra describe **el subconjunto codificado**, no el corpus.

### 4.3 Asociaciones a nivel de quipu (n = 297; 20 camélidos)

| prueba | estadístico | p | q (BH) |
|---|---|---|---|
| camélido ~ zona | χ² = 30,1 | 0,034 | 0,15 |
| camélido ~ nº de cuerdas | dif. mediana +23,5 | 0,30 | 0,54 |
| camélido ~ colores/cuerda | dif. −0,056 | 0,14 | 0,36 |
| camélido ~ colores/cuerda **controlando log n** | dif. residual +0,017 | 0,34 | 0,54 |
| camélido ~ `mean_cord_value` | 10 vs 16 | 0,39 / 0,75 | 0,56 / 0,97 |
| camélido ~ nº de clusters de nudo | −0,5 | 0,99 | 1,00 |
| camélido ~ estilo de nudo S | 16/20 vs 80/277 | 7,9 × 10⁻⁶ | **0,0001** |

**Valor: negativo.** La mediana de `mean_cord_value` es 10 en camélidos y 16 en algodón
(p = 0,75, Mann-Whitney; la permutación da 0,39). La diferencia de medianas a nivel de
cuerda (8 vs 3) es **entre quipus**, no dentro: no es evidencia.

**Color: negativo tras controlar tamaño** (q = 0,54). La impresión de que los quipus de
camélido son "menos coloridos" (0,087 vs 0,143 colores por cuerda) se explica por tamaño y
colección.

**Posición: no evaluable y por tanto negativo.** Con un solo quipu mixto con potencia no hay
contraste interno posible.

**Procedencia: confundida con colección.** 14 de los 20 quipus de camélido tienen procedencia
**desconocida** (Temple Radicati, colección Soldi, Museo Oro). La asociación con zona
(q = 0,15) está sostenida por Arica/Lluta y no es interpretable: el brief prohíbe usar el
museo como lugar de origen, y aquí no hay otra cosa.

### 4.4 El único correlato fuerte de la fibra es tecnológico, y se cae al controlar colección

`percent_s_knots` (dirección de nudo dominante) separa casi perfectamente: **16/20 quipus de
camélido son de estilo S** frente a 80/277 de algodón (p = 7,9 × 10⁻⁶; q = 0,0001).
**Pero dentro del Museo Temple Radicati —la colección que aporta 7 de los 20 camélidos— la
asociación desaparece: 6/7 vs 7/16, p = 0,089.** Es decir, el "efecto fibra" es en buena
parte un **efecto colección/estilo local**: un paquete de quipus S, grandes, poco coloridos y
de camélido, probablemente de una misma tradición regional, no una regla del sistema.

### 4.5 La fibra de la envoltura sí es una elección deliberada

**Las 994 filas de color de canuto (173 canutos) son todas CL (camélido) y las 465 de
canutito también.** Esto incluye a **KH0271/UR039, un quipu de algodón
(91 cuerdas CN) cuyos canutos son de camélido**. La envuelta no copia la fibra del objeto:
se elige camélido para envolver. Es el único caso del informe donde la fibra **no** es
redundante con la del quipu.

---

## 5. Controles y resultados negativos (resumen)

**Controles que se hicieron**
1. Nulo de permutación explícito en toda prueba (semilla 20241018).
2. Permutación **estratificada por quipu** para todo contraste a nivel de cuerda.
3. Nulo que preserva la **distribución de tamaños de segmento** en el test de sumas.
4. Nulo de **límites aleatorios** en el alineamiento canuto↔grupo.
5. **Estratificación por tamaño** (cuartiles) para la fibra: la tasa de camélido es 7,9 %,
   2,7 %, 10,8 % y 5,4 % por cuartil → sin gradiente (p = 1,00). El tamaño **no** explica
   la fibra.
6. **Estratificación por museo** para el estilo S: el efecto global se derrumba (p = 0,089).
7. BH sobre 13 pruebas por familia.
8. Validación de la unión cuerda↔valor con el largo (r = 0,985).

**Resultados negativos**
- La fibra **no** se asocia al valor (q = 0,56 / 0,97), ni al número de nudos, ni al color
  una vez controlado el tamaño, ni a la posición (no evaluable).
- El canuto **no** es una unidad aritmética (sumas no redondas, q = 0,08).
- El color del canuto **no** replica el color de las cuerdas (p ≥ 0,63 en los 8).
- El canuto **no** se asocia al estilo S (p = 1,00).
- El canutito **no** distingue la magnitud del valor (AUC 0,502, p = 0,97) ni el nivel.
- 86 de los 179 quipus con canutos los tienen en ≤5 % de sus cuerdas: la mayoría de las "presencias"
  son marcas aisladas, no el sistema de envoltura total.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| El canuto envuelve la fijación de un grupo chico de colgantes (mediana 4) al cordón principal, y cubre todas las fijaciones en los 8 quipus con registro fino | **Demostrado** (descripción estructural de la tabla, 887 cuerdas) |
| Los límites de canuto coinciden con los límites de grupo de colgantes (23/24 en UR052, p = 5 × 10⁻⁵) | **Apoyado con datos** (un solo quipu con grupos independientes; posible circularidad con el detector del KFG) |
| El canuto lleva una secuencia de color propia, en runs, independiente del color de las cuerdas | **Apoyado con datos** (173 canutos, 8 quipus, ningún solape significativo) |
| El canuto no es una unidad contable | **Apoyado con datos** (8 pruebas, ninguna sobrevive BH) |
| El canutito es un hilo de contraste atado al extremo de colgantes de nivel 1, con paleta propia | **Demostrado** (posición al 96 % del largo; 467/467 nivel 1; 1,3 % de coincidencia de color) |
| La fibra es un atributo del objeto (cordón principal ↔ colgantes) | **Apoyado con datos** (χ² = 212) |
| La fibra no codifica valor, color ni posición | **Apoyado con datos** (negativos con n = 297 y controles) |
| El "efecto fibra" sobre el estilo de nudo es en realidad un efecto de colección/tradición local | **Apoyado con datos** (se cae al estratificar por museo: p = 0,089) |
| El canuto es un *kayte* / marcador de sujeto (Milillo 2024) | **Especulativo** — no falsable con estos datos; lo observado (envoltura total del objeto, color independiente, no aritmético) es igual de compatible con "organizador material de secciones" |
| La secuencia de color del canuto etiqueta la sección ("título" de grupo) | **Propuesto** — hay runs y hay frontera, pero no hay contenido correlacionado que lo confirme |

---

## 7. Limitaciones

1. **n = 8** quipus con canutos detallados; **n = 20** con camélido. Todo lo demás es
   descriptivo. Los p-valores son válidos pero la inferencia externa es débil.
2. **Registro en 2006** (Brezine) con campos geométricos incoherentes; `ATTACH_POS`,
   `NUM_LOOPS` y `CTO_LEVEL` son constantes y no informativos.
3. **`canutito.KHIPU_ID` = 0** en las 493 filas (recuperado por `CORD_ID`).
4. **44 % de los quipus sin fibra**, y la falta depende de la colección → el 6,7 % de
   camélidos es una tasa del subconjunto codificado, no del corpus.
5. La coincidencia canuto↔grupo en UR052 puede ser circular si el detector del KFG usó el
   canuto como pista visual.
6. `num_canuto_cords` del KFG procede en parte del OKR y en parte de codificación propia:
   las dos fuentes no coinciden (p. ej. KH0281 tiene 75 en KFG y ningún registro en OKR).

## 8. Para el coordinador

- **Los canutos no son marcas raras ni decorativas: son el sistema de fijación.** En los 8
  quipus con registro fino el 97,6 % de las cuerdas está dentro de un canuto; cada canuto
  envuelve ~4 colgantes consecutivos (mediana 4, rango 1–6). El canuto es un atributo del
  objeto completo, no un marcador puntual. Y su fibra es siempre camélido (994/994 filas),
  incluso en UR039, un quipu de algodón: la envuelta no copia la fibra del objeto.
- **El mejor resultado positivo del informe:** en UR052/KH0282, **23 de 24 fronteras de grupo
  de colgantes coinciden con una frontera de canuto** (Jaccard 0,885; p = 5 × 10⁻⁵ frente a
  límites aleatorios). El canuto delimita grupos. Es un solo quipu y hay riesgo de
  circularidad, así que va como *apoyado con datos*, no demostrado.
- **El canuto no es una unidad de cuenta.** Las sumas por segmento no son redondas (14,1 % vs
  10 % esperado) y ningún quipu sobrevive a BH. Descartar la idea "cada canuto = un total".
- **Los canutos llevan una secuencia de color propia** (1–4 bandas de ~3 cm) que se repite en
  runs y que **no coincide con el color de las cuerdas** (0–10 % de solape, ningún quipu
  significativo). Es una capa de información independiente: la envuelta dice algo distinto
  de lo que dicen los colgantes. Qué dice, no lo sabemos.
- **Los canutitos son otra cosa y van aparte**: hilo de contraste atado al extremo del 100 %
  de las cuerdas marcadas, siempre de nivel 1, con paleta que las cuerdas no usan. Marcan
  cuerdas algo más largas (AUC 0,65) y anudadas (AUC 0,52), pero **no** distinguen la
  magnitud del valor (AUC 0,502, p = 0,97). No son "etiquetas de cifra".
- **La fibra no codifica valor, color ni posición.** Valor: mediana 10 vs 16, p = 0,75.
  Color: se explica por tamaño (p = 0,34). Posición: no evaluable. Estos son negativos con
  controles, no falta de datos.
- **La fibra es un atributo del objeto:** el cordón principal predice la fibra de los
  colgantes (χ² = 212). Con 13 quipus 100 % camélido y un solo quipu mixto con potencia
  (KH0281), cualquier análisis "fibra vs X" a nivel de cuerda es pseudorreplicación.
- **El único correlato fuerte de la fibra (estilo de nudo S, p = 8 × 10⁻⁶) se cae al
  estratificar por museo (p = 0,089).** Es un efecto de colección/tradición local (Temple
  Radicati, Arica, colección Soldi), no una regla del sistema.
- **Alerta de datos para todo el equipo:** el 44 % de los quipus no tiene ni una cuerda con
  fibra codificada, y la falta es 98 % en Berlin-Völkerkunde, 97 % en Pachacamac y 90 % en
  AMNH. Cualquier conclusión sobre fibra describe ese subconjunto.
- **Siguiente ronda:** (i) conseguir los 8 quipus con canutos en foto y verificar
  independientemente las fronteras de grupo de UR052; (ii) codificar la secuencia de color
  del canuto en los ~150 quipus con `num_canuto_cords > 0` que hoy no tienen registro
  detallado y probar si predice contenido; (iii) no gastar más esfuerzo en "fibra vs valor"
  sin nuevos datos de fibra.
