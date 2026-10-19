# Verificación de las cifras de Urton & Brezine (2009) sobre nudos y torsión, y test de asociación dirección S/Z ↔ archivo

**Carpeta:** `analisis/ds/n_urton_brezine_sz/`
**Fecha:** 2026-10-17
**Fuentes:** `analisis/datos/cuerdas.csv` (KFG, 651 quipus), `analisis/datos/quipus.csv`, `data/external/open-khipu-repository/data/khipu.db` (OKR, 619 quipus), `analisis/fuentes_txt/QuipuYTocapu.txt` (texto del capítulo) y `analisis/15_quipu_tocapu/afirmaciones.csv`.

---

## 1. Pregunta

1. ¿Se reproducen, con nuestros datos, las cifras que Urton y Brezine (2009) dan en las actas *Quipu y Tocapu* sobre procedencia, número de cordeles, nudos y torsión?
2. ¿La dirección S/Z del nudo se asocia con el archivo/procedencia del quipu, a nivel de quipu, con un nulo por permutación y corrección múltiple?

---

## 2. Datos y método

### 2.1 Corpus y definiciones

- **KFG:** `cuerdas.csv`, 57.818 cuerdas de 651 quipus. El campo `nudos` se parseó con la gramática `nTIPO(posición,dirección),valor`; una corrida `3S(...)` son **3 nudos simples** (aporta 30 en las decenas), mientras que `L`, `E`, `EE`, `LL` cuentan como **1 nudo**. Se excluyen del denominador los nudos con dirección `U` (desconocida). Los valores 0 sin nudos no se cuentan como nudos.
- **OKR:** tabla `knot` (110.677 filas; 110.151 unidas a `cord`), `TYPE_CODE` S/L/E/... y `DIRECTION` S/Z/U. `cord.TWIST` = torsión final del cordel; `cord.FIBER` = fibra.
- **Archivo:** no es cualquier etiqueta de procedencia. La Tabla 2 del capítulo usa **12 archivos arqueológicos**: Laguna de los Cóndores (Leymebamba), Santa, Chancay, Pachacamac, Puruchuco, Tambo Colorado, Paracas, Ica, Ocucaje, Atarco, Nazca y Arica. Nuestro `quipus.csv` no tiene "Puruchuco" en `procedencia`, pero sí `region = Puruchuco` para 24 quipus (19 con procedencia "Huaquerones"); los reasignamos a Puruchuco. Sin esa corrección, el archivo Puruchuco desaparece y el total de 12 archivos en KFG baja de 279 a 255.
- Los quipus sin etiqueta específica ("Unknown", "Peru", "Eduard Gaffron", "Huaquerones" sin región, etc.) se agrupan como **sin archivo / Otros-vago**. Esto es una reconstrucción, no la clasificación original de la KDB.

### 2.2 Contraste estadístico

- **Unidad:** el quipu. Respuesta principal: `pZ` = proporción de nudos en Z entre los nudos con dirección conocida (todos los tipos). Respuesta secundaria: `pZ_S` = solo nudos simples; también se probó por tipo (L, E).
- **Estadístico:** eta² = SS_entre / SS_total de las medias por quipu, **sin ponderar por número de nudos** (evita pseudorreplicación). Se reporta también el chi² del patrón todo-Z/todo-S/mixto y V de Cramer.
- **Nulo:** 10.000 permutaciones de las etiquetas de archivo entre quipus, semilla 20261017. p empírico = (1 + n.º permutaciones ≥ observado)/(B+1).
- **Controles:** (i) tamaño, residualizando por terciles de nudos orientados y permutando dentro de cada tercil; (ii) tasa de dirección desconocida `%U`, residualizando por quintiles; (iii) torsión del cordel, restringiendo a cuerdas de torsión S; (iv) fibra, restringiendo a nudos en cuerdas de algodón (OKR); (v) exclusión de khipus canuto; (vi) subconjunto de 12 archivos y quipus con ≥50 nudos; (vii) replicación en OKR.
- **Comparaciones múltiples:** BH-FDR dentro de la familia de comparaciones pareadas (cada archivo vs el resto) y dentro de la familia de los tres tipos de nudo. Los tests globales son pruebas primarias preespecificadas; el resto son robusteces y se reportan todas.

### 2.3 Scripts

`01_cifras.py` (conteos), `02_archivo.py` (test principal), `03_secundarias.py` (cifras U08-U14), `04_robustez.py` (controles), `05_tabla.py` (tabla final), `arch12.py` (mapeo). Salidas: `salida_01.txt` … `salida_04.txt`, `perquipu_kfg*.csv`, `perquipu_okr.csv`, `tabla_afirmaciones.csv`.

---

## 3. Resultados: las cifras del capítulo

### 3.1 Tabla de contraste

| Afirmación | Su cifra (U&B 2009) | KFG (nuestro parseo) | OKR | Comentario |
|---|---|---|---|---|
| Khipus con procedencia en 12 archivos | 222 de 451 (49,2%) | **279 de 651 (42,9%)** | **255 de 619 (41,2%)** | La proporción baja de 49,2% a 41-43%; el absoluto no se reproduce porque el corpus creció y los quipus nuevos tienen menos archivo. |
| Pachacamac es el mayor archivo | 68 | **91 (14,0%)** | **91 (14,7%)** | La **proporción** se mantiene (15,1% → 14,0-14,7%); el absoluto creció con el corpus. |
| Khipus sin procedencia | 229 de 451 (50,8%) | 372 de 651 (57,1%) | 364 de 619 (58,8%) | Más khipus nuevos sin archivo. |
| Media de cordeles por khipu | 218 (Nazca) – 10 (Chancay); máx. 323; mín. 12 | 231 (Nazca) – 26 (Chancay); máx. 1.831 (Arica); mín. 5 | no calculado por archivo | Orden de magnitud similar; los extremos dependen de AS069. |
| Khipus mayores | 870 (Laguna), 1.585 (Arica); 338 (Pachacamac), 114 (Puruchuco) | **874** (UR006), **1.831** (AS069), **338 exacto**; Puruchuco 225 | no calculado | Coincidencias casi exactas en Laguna y Pachacamac; Arica y Puruchuco no. |
| Khipus con subsidiarias | 291 de 451 (64,5%) | **435 de 651 (66,8%)** | no calculado | Casi idéntico. |
| Cordeles con dato de material | 15.616 (40%); 85% algodón, 9% camélido, 6% otros | sin campo de fibra | **31.402 (57,7%); 92% algodón, 4,4% camélido** | Más cordeles documentados y más algodón que en 2009. |
| Cordeles con retorcido final S / Z | **96% S / 4% Z** (1.012 Z de 26.279) | **92,97% S / 7,03% Z** (3.398 Z de 48.363) | **92,44% S / 7,56% Z** (3.402 Z de 44.971) | La proporción Z se duplica; el absoluto Z se triplica. |
| De los cordeles Z, 54% camélido / 33% algodón | 54% / 33% | sin fibra | **16% camélido / 83% algodón** (entre los que tienen fibra) | No se reproduce: hay ~7× más cordeles Z de algodón; el absoluto de camélido Z es parecido (495 vs ~546). |
| Total de nudos | 70.660 | **121.449** | **110.151** | 1,6-1,7× más nudos. |
| Nudos con orientación | 51.178 (72,4%) | **106.591 (87,8%)** | **97.585 (88,6%)** | La cobertura de orientación subió 15 puntos. |
| **Nudos simples: S / Z** | **35% / 65%** | **27,2% / 72,8%** (n=72.477) | **26,1% / 73,9%** (n=66.590) | **No se reproduce.** El 35/65 coincide con el agregado de *todos* los tipos (34,8% S en `khipu_summary`), no con los simples. |
| Nudos largos: S / Z | 53% / 47% | **54,1% / 45,9%** | **52,4% / 47,6%** | Reproducción casi exacta. |
| Figura de ocho: S / Z | 30% / 70% | **27,1% / 72,9%** | **27,2% / 72,8%** | Reproducción cercana. |
| Patrón todo-Z | **72 de 272 (26,5%)** | **102 de 379 (26,9%)** | **94 de 333 (28,2%)** | Proporción casi idéntica; el denominador crece 1,39× (el corpus, 1,44×). |
| Patrón todo-S | **27 de 272 (9,9%)** | **39 de 379 (10,3%)** | **32 de 333 (9,6%)** | Proporción casi idéntica. |
| Pachacamac tiene el mayor % de nudos Z | cualitativo | Pachacamac 76,0% (todos) / 92,4% (simples); **Puruchuco 80,6/97,5; Santa 81,3/83,4** | Pachacamac 84,8%; Santa 96,2% | Pachacamac está en el grupo alto, pero **no es el máximo**; las diferencias con Puruchuco/Santa no son significativas. |
| Cordeles totales (texto vs figura) | 38.381 vs 38.831 | **57.818** | **54.403** | No se reproduce ninguno; el corpus actual es 1,42× mayor. La diferencia de 450 es interna al capítulo (probable errata). |

La tabla completa, con nivel de evidencia por fila, está en `tabla_afirmaciones.csv`.

### 3.2 Lo que sí se reproduce

Tres bloques resisten bien:

1. **Los nudos largos y la figura de ocho.** 54,1/45,9 y 27,1/72,9 en KFG; 52,4/47,6 y 27,2/72,8 en OKR, frente a 53/47 y 30/70. Son diferencias de 1-3 puntos, con decenas de miles de nudos. **Demostrado.**
2. **La estructura de los patrones por quipu.** 26,9% todo-Z y 10,3% todo-S (KFG) frente a 26,5% y 9,9% (U&B); en OKR, 28,2% y 9,6%. Los cocientes todo-Z/todo-S son 2,6-2,9. El denominador crece 1,39×, casi exactamente lo que creció el corpus (1,44×). **Demostrado** (la estructura; no los absolutos).
3. **Los khipus mayores y Pachacamac.** El máximo de Laguna (874 vs 870), el de Pachacamac (338 vs 338) y la proporción de Pachacamac en el corpus (15,1% vs 14,0-14,7%) coinciden. **Apoyado con datos.**

### 3.3 Lo que no se reproduce

1. **Nudos simples 35% S / 65% Z.** Nuestros datos dan 26-27% S, no 35%, tanto en KFG como en OKR, con y sin ponderar, y en todos los subconjuntos razonables que probamos. La cifra 35/65 **sí** coincide con el agregado de todos los tipos: 35.363 S / 66.169 Z = **34,8% S** en `khipu_summary.csv` (33,0% S en nuestro parseo directo; la diferencia es de notación/cobertura, no de dirección). La explicación más parsimoniosa es que la etiqueta "simples" esté mal puesta y que 35/65 sea el agregado de todos los nudos. No podemos descartar que el subcorpus de 2009 tuviera otra composición, pero el hecho de que largos y figura de ocho sí coincidan hace menos probable un simple cambio de corpus.
2. **54% de camélido entre los cordeles Z.** En OKR, entre los cordeles Z con fibra conocida, solo 16% es camélido (495 CL + 21 W) y 83% algodón. El absoluto de camélido Z (495) es parecido al implícito en 2009 (54% de 1.012 = 546); lo que creció fue el algodón Z (2.497 vs ~334). **Refutado para el corpus actual.**
3. **Pachacamac como máximo absoluto de Z.** Es uno de los archivos altos, pero Puruchuco (97,5% Z en simples) y Santa (83,4%) lo superan; las diferencias no son significativas. Solo frente a Ica hay una diferencia marginal (p=0,055 en simples). **La refutación en simples depende de la reasignación de Puruchuco:** sin esos 24 quipus, Pachacamac es el máximo en simples (92,4% vs Santa 83,4%), aunque en todos los tipos Santa sigue por delante (81,3% vs 76,0%). En ningún caso las diferencias son significativas. **Parcialmente apoyado, no demostrado.**
4. **Los absolutos 222/451, 68, 38.381/38.831, 70.660, 51.178, 26.279 y 1.012.** No son reproducibles porque el corpus cambió de tamaño. Lo que se conserva son las **proporciones**, no los conteos.

### 3.4 Por qué difieren: corpus, U desconocidas y criterios

- **Cambio de corpus.** KFG tiene 651 quipus y 57.818 cuerdas; OKR, 619 y 54.403. U&B trabajaban con 451 quipus y 38.381 cuerdas (o 38.831 según la figura). El cociente de cuerdas es 1,42-1,50; el de nudos, 1,56-1,72. Casi todas las diferencias absolutas desaparecen al normalizar por el tamaño del corpus (p. ej., todo-Z: 72/272 vs 102/379).
- **U desconocidas.** En 2009, 72,4% de los nudos tenían orientación; ahora 87,8% (KFG) y 88,6% (OKR). La cobertura no es homogénea: Arica tiene **42,2% U**, Ica 11,7%, Pachacamac 11,5%, Nazca 6,3%, Laguna 0,3%, Puruchuco 0,1%. Las comparaciones entre archivos se hacen, por tanto, sobre fracciones distintas de cada quipu. Esto no invalida el test (ver 4.4), pero obliga a mirar el %U.
- **Criterio de "archivo".** U&B usan 12 archivos arqueológicos, no las 65 etiquetas de procedencia de `quipus.csv`. Nuestra reconstrucción es imperfecta: Puruchuco solo se recupera por `region`; "Huaquerones" es una etiqueta de saqueo, no un sitio; "Ica" y "Ocucaje" se solapan. El total de 12 archivos es 279/651 (42,9%) en KFG y 255/619 (41,2%) en OKR, frente a 222/451 (49,2%): la proporción es razonablemente cercana, pero no idéntica.
- **Criterio de conteo de nudos.** KFG escribe corridas (`3S` = 3 nudos); OKR tiene una fila por nudo. Nuestro parseo de KFG da 121.449 nudos, un 4,5% más que el `knot_count` de `khipu_summary.csv` (116.246), por diferencias de notación en corridas `SP`/`U`. Los porcentajes no cambian materialmente si se usa `khipu_summary` (34,8% S agregado; 26-27% S simple).
- **KFG vs OKR no son independientes.** KFG deriva en buena parte de la KDB; las diferencias entre columnas son de cobertura y de parseo, no dos muestras independientes. Por eso la replicación en OKR es una comprobación de robustez, no una validación externa.

---

## 4. ¿Se asocia la dirección S/Z con el archivo/procedencia?

### 4.1 Descriptivo

Medias por quipu (≥10 nudos orientados), KFG, todos los tipos:

| Archivo | n quipus | %Z (ponderado por nudos) | %Z medio por quipu | % todo-Z |
|---|---:|---:|---:|---:|
| Santa | 7 | 81,3 | 84,5 | 28,6 |
| Puruchuco | 19 | 80,6 | 76,6 | 21,1 |
| Pachacamac | 72 | 76,0 | 75,9 | 43,1 |
| Ocucaje | 19 | 71,9 | 78,2 | 47,4 |
| Ica | 42 | 71,8 | 65,2 | 42,9 |
| Laguna de los Cóndores | 21 | 66,6 | 63,2 | 4,8 |
| Nazca | 13 | 43,7 | 42,7 | 7,7 |
| Chancay | 6 | 37,5 | 40,6 | 33,3 |
| Atarco | 6 | 34,8 | 34,5 | 0,0 |
| Paracas | 9 | 21,1 | 60,1 | 22,2 |
| Arica | 8 | 14,3 | 12,6 | 0,0 |

En nudos simples la separación es más nítida: Puruchuco 97,5% Z, Pachacamac 92,4%, Santa 83,4%, Ica 80,6%, Ocucaje 77,8%, Laguna 54,5%, Nazca 48,7%, Arica 0,3%. El rango va de **0% a 97,5% Z**: no es una variación menor, es un ordenamiento casi completo de los archivos.

### 4.2 Test global (unidad = quipu, permutación)

| Respuesta | Fuente | n quipus | eta² | p permutación |
|---|---|---:|---:|---:|
| Todos los tipos | KFG | 467 | **0,100** | **0,0001** |
| Solo simples | KFG | 327 | **0,168** | **0,0001** |
| Solo largos | KFG | 380 | **0,132** | **0,0001** |
| Solo figura de ocho | KFG | 179 | **0,121** | **0,0327** |
| Todos los tipos | OKR | 450 | **0,132** | **0,0001** |
| Todos, ≥50 nudos | KFG | 264 | 0,121 | 0,0004 |
| Solo 12 archivos | KFG | 224 | **0,186** | **0,0001** |

El IC95% bootstrap de eta² para el test principal (todos los tipos, KFG) es **[0,076; 0,175]**. Con BH dentro de la familia de los tres tipos, la figura de ocho sigue significativa (q=0,033). El patrón todo-Z/todo-S/mixto también difiere por archivo: chi²=65,4, p permutación=0,0004, V de Cramer=0,265.

**Lectura:** la dirección del nudo se asocia al archivo, y el efecto no es un artefacto de un solo tipo de nudo: aparece en simples, largos y, más débilmente, en figura de ocho.

### 4.3 Comparaciones pareadas (cada archivo vs el resto) y BH

**Todos los tipos (KFG):**

| Archivo | n | %Z medio | Diferencia vs resto | p | q BH |
|---|---:|---:|---:|---:|---:|
| Arica | 8 | 12,6 | −0,570 | 0,0002 | **0,0016** |
| Nazca | 13 | 42,7 | −0,263 | 0,0127 | 0,0508 |
| Pachacamac | 72 | 75,9 | +0,133 | 0,0197 | 0,0525 |
| Ocucaje | 19 | 78,2 | +0,120 | 0,184 | 0,369 |
| Puruchuco | 19 | 76,6 | +0,102 | 0,267 | 0,428 |
| Paracas | 9 | 60,1 | −0,076 | 0,572 | 0,685 |
| Laguna | 21 | 63,2 | −0,046 | 0,614 | 0,685 |
| Ica | 42 | 65,2 | −0,027 | 0,685 | 0,685 |

**Solo nudos simples (KFG):**

| Archivo | n | %Z medio | Diferencia vs resto | p | q BH |
|---|---:|---:|---:|---:|---:|
| Arica | 8 | 1,2 | −0,767 | 0,0001 | **0,0007** |
| Pachacamac | 53 | 88,4 | +0,231 | 0,0020 | **0,0070** |
| Nazca | 8 | 37,1 | −0,387 | 0,0068 | **0,0159** |
| Puruchuco | 12 | 91,2 | +0,190 | 0,134 | 0,235 |
| Laguna | 18 | 61,3 | −0,142 | 0,195 | 0,273 |
| Ocucaje | 14 | 84,1 | +0,115 | 0,346 | 0,403 |
| Ica | 32 | 72,6 | −0,015 | 0,885 | 0,885 |

Tras BH, en el test principal solo **Arica** se separa claramente del resto; Nazca y Pachacamac quedan en el borde (q≈0,05). En simples, Arica, Pachacamac y Nazca sobreviven. Es un efecto de **dos polos** (Arica muy S; Pachacamac/Puruchuco muy Z) más que un gradiente continuo.

### 4.4 Controles

| Control | eta² | p | Lectura |
|---|---:|---:|---|
| Tamaño (resid. por terciles, permutación estratificada) | 0,102 | 0,0001 | El efecto no se debe a quipus grandes/pequeños. |
| Tasa de U (resid. por quintiles de %U) | 0,089 | 0,0001 | El efecto sobrevive al control de documentación. |
| Solo cuerdas de torsión S (OKR) | 0,130 | 0,0001 | La torsión del cordel no lo explica. |
| Solo nudos en cuerdas de algodón (OKR) | 0,158 | 0,0002 | La fibra no lo explica (dentro del algodón). |
| Sin khipus canuto | 0,096 | 0,0012 | No es un efecto de los canutos. |
| Sin Arica | 0,070 | 0,0011 | Arica es un polo importante, pero no el único. |
| ≥50 nudos | 0,121 | 0,0009 | No es un artefacto de quipus con pocos nudos. |
| Solo 12 archivos | 0,186 | 0,0001 | Más fuerte al quitar "Otros/vago". |
| Solo quipus con %U≤10% | 0,164 | 0,118 | **Pierde significación por potencia** (n=106), no porque el efecto desaparezca: eta² sube. |

**Torsión del cordel ≠ dirección del nudo.** A nivel de cuerda, el pZ es 0,676 en cuerdas de torsión S y 0,683 en cuerdas de torsión Z (diferencia 0,007; Wilcoxon de las diferencias dentro de quipu p=0,0555, ns). La dirección del nudo no está determinada por el retorcido del cordel.

**Fibra.** En OKR, los nudos en cuerdas de algodón son 70,4% Z; en camélido, 16,6% Z (es decir, 83,4% S). Es una asociación fuerte, pero **solo 7 quipus tienen cuerdas de ambas fibras**, así que el test dentro de quipu no tiene potencia (Wilcoxon p=0,5). El efecto de archivo se mantiene al restringir a algodón (eta²=0,158), de modo que la fibra no explica las diferencias entre archivos, aunque sí contribuye al nivel absoluto de S/Z.

**Tamaño.** Spearman pZ vs n.º de nudos: −0,139 (p=0,0026) en KFG, −0,047 (p=0,33) en OKR. Inconsistente y pequeño; el control por terciles no cambia eta².

### 4.5 El caso Pachacamac

La afirmación "Pachacamac tiene el mayor porcentaje de nudos en Z de todos los archivos" **no se sostiene como máximo único**:

- En todos los tipos, Santa (81,3%) y Puruchuco (80,6%) superan a Pachacamac (76,0%).
- En simples, Puruchuco (97,5%) supera a Pachacamac (92,4%).
- Las diferencias Pachacamac−Puruchuco (p=0,85 en simples), Pachacamac−Santa (p=0,69) y Pachacamac−Ocucaje (p=0,67) no son significativas.
- Pachacamac **sí** está significativamente por encima del resto en simples (q=0,007) y es el archivo grande con más Z. La formulación correcta es: "Pachacamac es uno de los dos o tres archivos con más Z, no el máximo".
- **Caveat:** si no se reasigna Puruchuco por `region`, Pachacamac recupera el primer puesto en simples (92,4% vs Santa 83,4%). La conclusión "no es el máximo" es, por tanto, condicional a esa reconstrucción; lo que sí es robusto es que Pachacamac pertenece al grupo alto y que las diferencias con Puruchuco/Santa no son significativas.

---

## 5. Resultados negativos

1. **Dirección del nudo y torsión del cordel:** sin asociación (p=0,0555; diferencia de 0,7 puntos porcentuales).
2. **Dirección del nudo y tamaño del quipu:** asociación débil e inconsistente entre KFG y OKR; el efecto de archivo no cambia al controlar por tamaño.
3. **Geografía vs archivo: no separables.** La región, incluyendo "Unknown" (351 quipus), explica poco (eta²=0,027; p=0,028), pero entre los 114 quipus con región conocida explica **eta²=0,178 (p=0,008)**, comparable al archivo (0,186 en los 12 archivos). Las etiquetas de región son pocas y en parte duplican los archivos; no podemos atribuir el efecto específicamente al archivo y no a la geografía.
4. **Figura de ocho:** es el tipo con señal más débil (eta²=0,121; p=0,033; sobrevive BH por poco). No debe usarse como evidencia fuerte por sí sola.
5. **Subconjunto con %U≤10%:** pierde significación (p=0,118), aunque el tamaño de efecto es alto (eta²=0,164). Es un problema de potencia (n=106), no una refutación.
6. **La cifra 35% S en nudos simples** no se reproduce en ningún subconjunto natural; la única forma de acercarse es promediar sin ponderar quipus que contienen nudos U (35,5%), lo que no es un estadístico defendible.
7. **El 54% de camélido entre cordeles Z** no se reproduce (16% en el corpus actual).

---

## 6. Nivel de evidencia

| Conclusión | Nivel |
|---|---|
| Los nudos largos son ~53/47 S/Z y la figura de ocho ~28/72 | **Demostrado** (dos fuentes, decenas de miles de nudos) |
| Los patrones todo-Z (~27%) y todo-S (~10%) por quipu se mantienen | **Demostrado** (proporciones casi idénticas; cociente 2,6-2,9) |
| La dirección S/Z se asocia al archivo/procedencia | **Demostrado** como asociación estadística (eta²=0,10; p<0,0001; robusto a tamaño, U, torsión, fibra, canutos y fuente) |
| La asociación refleja estilos locales o tradiciones de archivo | **Propuesto** (compatible con estilo local, región o tradición de archivo; no separable de museo/collector) |
| Pachacamac es el archivo con más Z | **Parcialmente apoyado**; no es el máximo único |
| La dirección del nudo es un código binario semántico (Urton 2003) | **Especulativo**; este trabajo solo muestra estructura, no significado |
| "Nudos simples 35% S / 65% Z" | **Refutado** para el corpus actual; probable error de etiqueta (35/65 = agregado de todos los tipos) |
| "96% S / 4% Z en cordeles" | **Apoyado con datos para 2009**, pero ya no describe el corpus actual (93/7) |
| "54% de camélido entre cordeles Z" | **Refutado** en el corpus actual (16%) |

---

## 7. Limitaciones

- **Procedencia ≠ origen.** `procedencia` es en buena parte museo/colector, no lugar de excavación (regla 6 del BRIEF). "Huaquerones" no es un sitio. La asignación de Puruchuco por `region` es una reconstrucción.
- **Los 12 archivos no son una muestra aleatoria.** Algunos son colecciones de un sitio; otros, conjuntos de museo. Los quipus de un archivo pueden compartir manos, época o materia prima, lo que produce la asociación sin que haya un "código de archivo".
- **No se puede reconstruir el snapshot de 2009.** OKR no tiene fechas de ingreso anteriores a 2011; no sabemos qué 451 quipus eran. Por eso las diferencias absolutas se explican por crecimiento del corpus, pero no se pueden verificar una a una.
- **KFG y OKR no son independientes.** KFG deriva de la KDB; la replicación en OKR controla parseo y cobertura, no sesgo de fuente.
- **pZ es extremo (0 o 1) en muchos quipus.** El test es, en la práctica, una comparación de proporciones de quipus todo-Z/todo-S; es robusto pero grueso.
- **U no es aleatoria.** Arica tiene 42% U; sus medias se basan en una fracción menor de sus nudos. El control por %U y la restricción a %U≤10% no muestran que el efecto desaparezca, pero la precisión por archivo es desigual.
- **No hay datos de fibra en KFG.** El control de fibra solo es posible en OKR y con 31.402 de 54.403 cordeles.
- **Asociación no es significado.** Que la dirección S/Z varíe por archivo es compatible con estilo local, con tecnología de manufactura o con un código; este análisis no distingue entre esas hipótesis.

---

## 8. Para el coordinador

- **Las cifras de nudos largos y figura de ocho se replican casi exactamente** (54,1/45,9 y 27,1/72,9 frente a 53/47 y 30/70). Son el núcleo sólido del capítulo.
- **La cifra estrella de "nudos simples 35% S / 65% Z" no se reproduce:** nuestros datos dan 26-27% S en KFG y OKR. El 35/65 coincide con el agregado de *todos* los tipos (34,8% S), lo que sugiere un error de etiqueta en el capítulo. Es la discrepancia más importante y conviene citarla con cuidado.
- **Los patrones todo-Z y todo-S sí se replican en proporción:** 26,9% y 10,3% (KFG) frente a 26,5% y 9,9% (U&B), con el denominador creciendo 1,39× (el corpus, 1,44×). Los absolutos 72/272 no son comparables porque el corpus pasó de 451 a 651 quipus.
- **La dirección S/Z se asocia fuertemente al archivo, a nivel de quipu:** eta²=0,100 (IC95% 0,076-0,175), p<0,0001, 10.000 permutaciones; en simples eta²=0,168; en largos 0,132; en figura de ocho 0,121 (p=0,033). Replica en OKR (0,132).
- **El efecto sobrevive a los controles aburridos:** tamaño, tasa de U, torsión del cordel, fibra (solo algodón), exclusión de canutos, ≥50 nudos y subconjunto de 12 archivos. Sin Arica baja a eta²=0,070 pero sigue significativo (p=0,001).
- **Región y archivo están confundidos:** con región conocida, la región explica eta²=0,178 (p=0,008), tanto como el archivo (0,186 en los 12 archivos). El patrón es de dos polos: Arica casi todo S (0,3% Z en simples) y Pachacamac/Puruchuco casi todo Z (92-98% Z).
- **Pachacamac no es el máximo absoluto:** Puruchuco (97,5% Z en simples) y Santa (83,4%) lo superan, sin diferencias significativas. Pachacamac sí es significativamente más Z que el resto en simples (q=0,007). La afirmación "el mayor porcentaje de Z" es parcialmente apoyada, no demostrada.
- **La torsión del cordel no explica la dirección del nudo** (p=0,055; 0,676 vs 0,683). La fibra sí se asocia (algodón 70% Z, camélido 17% Z), pero el efecto de archivo persiste dentro del algodón. No confundir torsión del cordel con dirección del nudo.
- **Las cifras de torsión de 2009 (96/4; 54% camélido entre los Z) ya no describen el corpus:** hoy es 93/7 y solo 16% de los cordeles Z con fibra conocida es camélido. El absoluto de camélido Z es similar; lo que creció fue el algodón Z.
- **Recomendación:** (i) tratar 35/65 como posible errata y no como dato; (ii) usar archivo y región como factores alternativos (no excluyentes), con modelos que controlen por fibra y por documentador; (iii) buscar el significado en los pares de archivos extremos (Arica vs Pachacamac/Puruchuco), donde el contraste S/Z es casi determinista, y no en el promedio del corpus.
