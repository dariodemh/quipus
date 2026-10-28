# Lit_2 — Afirmaciones comprobables de la literatura sobre quipus y su contraste con el corpus

**Autor:** equipo lit_2 · **Fecha:** 2026-10-17 · **Semilla:** 20261017
**Scripts:** `tests.py` (contrastes), `control_D.py` (dirección del efecto en D), `explorar.py` (descriptivos), `crear_afirmaciones.py` (tabla).
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `quipus.csv`, `grupos.csv`; OKR (`khipu.db`) solo para verificar tres identificaciones. No se regeneró nada.

---

## 1. Pregunta

¿Qué afirmaciones concretas y cuantitativas sobre el significado o la estructura de los quipus hacen las fichas asignadas, cuáles son contrastables con los datos del repo, y cuáles se sostienen al contrastarlas?

## 2. Método

1. **Lectura de 12 fichas** y extracción de toda afirmación con un referente verificable (ids de quipu, cifras, colores, sumas, alineaciones documentales). Resultado: **19 filas** en `afirmaciones.csv` (3 marcadas `si`, 10 `parcial`, 6 `no`).
2. **Selección de las 5 familias más importantes y efectivamente contrastables** (A–E abajo). No se eligieron por conveniencia: son las que admiten una operación explícita y limpia sobre `cuerdas.csv`.
3. **Unidad de análisis = quipu** (regla 1 del brief). Las permutaciones se hacen **dentro de cada quipu**, nunca entre quipus, salvo el nulo de reasignación de vectores de E, que respeta el estrato de tamaño.
4. **Nulo explícito y p-valor empírico** en cada test (4 000 permutaciones en D; 2 000 en E). Se informa el mínimo p alcanzable (1/(B+1) ≈ 0,00025).
5. **Corrección múltiple:** BH-FDR sobre los 4 p-valores calculados (3 de D + 1 de E). Los contrastes A–C son descriptivos/aritméticos y no generan p.
6. Los valores `0` con `nudos` vacío se tratan como ausentes (`NaN`), no como ceros.

## 3. Resultados

### A. Estadísticos descriptivos del corpus vs. cifras publicadas

| Afirmación (fuente) | Publicado | Repo (651 quipus) | Veredicto |
|---|---|---|---|
| Media de cordeles por quipu (Urton apud Curatola 2013, ~450 ejemplares KDB) | 84 | **88,8** (mediana 43) | consistente |
| Media de colgantes (Cherkinsky 2014, ~480 entradas KDB) | 60 (mediana 27) | **64,1** (mediana 32) | consistente |
| Colgantes con al menos una subsidiaria (Curatola 2013) | ~25 % | **22,6 %** | consistente |
| Profundidad jerárquica máxima (Curatola 2013) | 6 niveles | **15 niveles** (HP038); 3 quipus ≥5 | la cifra publicada no es un techo |
| Rango de colgantes (Curatola 2013) | 1–1500 | **1–1650** | 1 quipu excede 1500 |
| Matices de color (Cherkinsky 2014) | 52 | **61 códigos Ascher simples** | mismo orden de magnitud |

Reparto de profundidad: 216 quipus con 0 niveles, 285 con 1, 104 con 2, 36 con 3, 7 con 4, 2 con 5, 1 con 15 (el 15 es una cadena real de subsidiarias de una sola hija en HP038, no un error de parseo).

**Lectura:** las cifras “de la literatura” se replican casi exactamente. Pero **no es una confirmación independiente**: KFG y el Harvard KDB describen en gran parte los mismos objetos. Sirve para validar la tubería, no la teoría.

### B. UR19 y el “π” de Saez-Rodriguez (2014)

UR19 = KH0255 (Centro Mallqui, Leymebamba). En el repo:

- 13 colgantes + 5 subsidiarias = 18 cuerdas → **coincide** con la ficha.
- `pc_largo` = **26,0 cm** → **coincide**.
- Suma de todos los valores = **100,0**; suma de colgantes = **78,0**.
- `100 / 13 = 7,69`; `78 / 13 = 6,00`. **No** se reproduce el “total 40,9” ni `40,9/13 = 3,14`.
- Direcciones de nudo: **1 racimo S y 11 Z**; suma de valores de cuerdas solo-S = **1,0**, solo-Z = **99,0**. La partición “S = 24,6 / Z = 16,3” no existe en estos datos (y 24,6 + 16,3 = 40,9, el total que tampoco aparece).

**Control de multiplicidad numérica.** Para los 651 quipus calculé `suma total / nº de colgantes` y conté cuántos caen a ±0,01 de varias constantes: π → **1**; 2π → 0; e → 0; φ → 0; 3 → 0; **6 → 1**; 9 → 0; 12 → 0. Es decir, la tasa base de “encontrar π” es la misma que la de encontrar un 6 redondo: **1/651**. El hallazgo de π es indistinguible del azar por este procedimiento.

**Veredicto: bien apoyado que la lectura de UR19 no se reproduce con los datos del repo.** No se puede descartar que Saez usara otra tabla de Urton (2003), pero entonces el resultado depende de una transcripción no verificable, no del objeto.

### C. VA 42527 (= UR1104) y Saez-Rodriguez (2013)

- UR1104 = KH0118 = **VA42527** (Ethnologisches Museum, Berlín; Pachacamac). 21 cuerdas, **21 colgantes, 0 subsidiarias** → **coincide** con la ficha.
- Cuerdas 15–18 (valores/10): 315,9 · 140,7 · 217,8 · 208,5 → suma **882,9**; la ficha redondea a 881 (315+140+217+209).
- Pero **881 / 29,5 = 29,86**, no un entero. La afirmación “881 es múltiplo de 29,5” es **aritméticamente falsa**; la coincidencia lunar se obtiene por redondeo selectivo (315,9→315; 140,7→140; 217,8→217; 208,5→209).
- Los totales por cuerda del repo (÷10) difieren de los publicados en varios casos (p. ej., el cuarto total publicado, 2.241, frente a 2.541,9 en el repo), de modo que el “ajuste a las Pléyades” descansa sobre valores que no se reproducen.

**Veredicto: estructura (21/0) bien apoyada; inferencia astronómica no apoyada.**

### D. Dirección de nudo S/Z y moieties (Hyland, Ware & Clark 2014)

Selección: 199 quipus con ≥6 colgantes de dirección inequívoca (todos los racimos S o todos Z) y **ambas** clases presentes; 11 717 colgantes (Z = 7 196; S = 4 521). Tres estadísticos, nulo = permutar la etiqueta S/Z **dentro de cada quipu** (4 000 permutaciones):

| Estadístico | Observado | Media nula | p empírico |
|---|---|---|---|
| Nº de “runs” (cambio de dirección a lo largo del orden) | **2 317** | 3 048 | **0,0003** |
| Suma de \|rango medio de S − centro\| | **1 477** | 907 | **0,0003** |
| Heterogeneidad de la fracción S entre grupos de colgantes | **552,5** | 327 | **0,0003** |

Los tres sobreviven a BH-FDR (p = 0,0003, el mínimo alcanzable; con B = 4 000 da 0,00025). **La dirección del nudo no es aleatoria:** se agrupa en bloques a lo largo del orden y por grupo de colgantes. Pero **no tiene una orientación consistente**: S aparece después de Z en 97/199 quipus (prácticamente mitad y mitad) y la desviación firmada media es de solo +1,73 rangos por quipu.

**Pero el patrón no es una partición limpia de mitades:** la diferencia media entre la fracción de S en la 1.ª y la 2.ª mitad es solo **0,176** (mediana 0,104); **17/199** quipus superan 0,5 y **solo 1** tiene separación perfecta.

**Explicación aburrida (control):** la dirección está confundida con la composición de nudos. Las cuerdas “solo S” contienen nudo largo (unidades) en **77,6 %** de los casos; las “solo Z”, en **56,4 %**. En cambio, unión (R ≈ 42 % en ambas), torsión (S ≈ 87 % vs. 91 %) y largo mediano (36,5 vs. 35,0 cm) son casi idénticos. Además, de 14 884 cuerdas con ≥2 racimos, 3 406 tienen dirección mixta y solo 26,5 % de ellas terminan en Z: no hay una regla universal “unidades = Z”. La dirección transporta estructura, pero **no se puede afirmar que esa estructura sea la moiety**.

**Veredicto: “la dirección está estructurada y no es azar” = apoyado con datos. “S = Hanan, Z = Urin” = no comprobable con el repo (requiere el texto alfabético híbrido, n = 1).**

### E. Pares “muy similares” de Inkawasi (Urton & Chu 2015)

52 quipus con procedencia `Incahuasi` (JC001–JC052 + UR255–UR280), frente a los 34 excavados que reporta la ficha. Comparé pares del **mismo número de colgantes** con ≥5 posiciones con valor en ambas cuerdas (1 528 pares), correlacionando **por posición**, no por valores ordenados.

- r mediana de todos los pares = **−0,04**. (Si se ordenan los valores antes de correlacionar, la mediana sube a **0,87**: ese estadístico no discrimina nada y no debe usarse.)
- 25 pares del corpus tienen r ≥ 0,9; **ninguno** es un par Incahuasi–Incahuasi.
- Mejor par Incahuasi: **JC015–UR257, r = 0,857 (n = 10)**.
- Nulo de **estadístico máximo**: reasignar al azar los vectores de valores dentro de cada estrato de tamaño y quedarse con el máximo r entre los 45 quipus Incahuasi. Media del máximo nulo = **0,471**; **p = 0,113**.

**Veredicto: no se sostiene.** Con 45 quipus y ~40 comparaciones, un máximo de 0,857 es perfectamente esperable por azar (p = 0,11). El “registro muy similar” de los pares atados no emerge como un par identificable en el corpus; además, sin saber qué pares estaban atados, el test es solo una cota superior de la evidencia disponible.

**Control lateral importante:** el corpus contiene **duplicados de catálogo**. KH0033 y UR044 tienen 54 colgantes con **vector de valores idéntico** (r = 1,000; mismo museo, misma procedencia y mismo `pc_largo` = 215,5 cm): es el mismo objeto con dos ids. También UR070/UR071 (26 cuerdas). Cualquier estadístico de similitud entre quipus debe excluirlos; de lo contrario produce “descubrimientos” triviales.

### F. Lo que no se pudo contrastar

- **Puruchuco (Urton & Brezine 2005):** no aparece como `procedencia` en `quipus.csv` (0 de 651). Los 21 quipus no son identificables con los metadatos del repo. **No comprobable.**
- **Parinacocha, Tulpo, angaraes, Tupicocha:** no hay quipus físicos identificados; solo transcripciones/documentos. **No comprobable.**
- **Fossa 2013, Brokaw 2010, Hyland 2010, Salomon 2006/2013:** afirmaciones interpretativas sin variable operacionalizable en el corpus.
- **Fechado Wari/inca/colonial por quipu:** el repo no trae la capa radiocarbónica; solo se puede citar la tabla de Cherkinsky (27/31 en 1446–1663; Wari 777–1024; VA42593 = UR193 en 1390–1423).

## 4. Controles y corrección múltiple

- **Nulo explícito** en D (permutación dentro de quipu) y E (reasignación de vectores por estrato de tamaño + estadístico máximo). Semilla fija.
- **BH-FDR** sobre los 4 p-valores: los tres de D quedan < 0,001; el de E = 0,113 (no significativo). No hay inflación por comparaciones múltiples en las conclusiones positivas.
- **Control de duplicados** (F): dos pares de quipus son el mismo objeto o copias exactas; se reportan y se excluyen del argumento.
- **Control de “coincidencia numérica”** (B): tasa base de π ≈ tasa base de 6.
- **Control de explicación aburrida** (D): dirección vs. tipo de nudo, unión, torsión y largo.
- **Valores ausentes:** los 0 sin nudos se trataron como `NaN`; en E se exige ≥5 posiciones con valor común para no correlacionar patrones de ausencia (fue exactamente el artefacto que producía un falso r = 0,797 entre JC022 y UR261).

## 5. Resultados negativos (explícitos)

1. **UR19 no reproduce el “π”**: el total es 100, no 40,9; `100/13 = 7,69`; la partición S/Z publicada no existe (1 racimo S, 11 Z).
2. **VA42527**: 881 no es múltiplo de 29,5 (29,86).
3. **Inkawasi**: ningún par de quipus con registro cuantitativo casi idéntico supera el azar (p = 0,113); 0 pares Incahuasi con r ≥ 0,9.
4. **Hyland 2014**: la dirección S/Z se estructura, pero **no** como mitades limpias (mediana de la diferencia entre mitades = 0,10; solo 1/199 con separación perfecta) y está confundida con la presencia de nudo largo.
5. **Puruchuco** no es identificable en el corpus; la afirmación central de Urton & Brezine 2005 queda fuera de alcance.

## 6. Nivel de evidencia

| Conclusión | Nivel |
|---|---|
| Las cifras descriptivas del KDB (84 cordeles; 60/27 colgantes; ~25 % con subsidiarias) se replican en el corpus | **apoyado con datos** (replicación del mismo corpus, no independiente) |
| El “π” y la partición S/Z de UR19 no se reproducen | **bien apoyado** (con los datos del repo) |
| 881 no es múltiplo de 29,5 | **bien apoyado** (aritmética) |
| La dirección de nudo S/Z está estructurada en bloques (posición y grupos), no es azar | **apoyado con datos** (p = 0,0003, BH); sin orientación consistente |
| S = Hanan / Z = Urin | **propuesto** (n = 1, no contrastable aquí) |
| Los pares atados de Inkawasi tienen registros “muy similares” | **no apoyado** (p = 0,113; resultado negativo) |
| UR1104 tiene 21 colgantes sin subsidiarias | **bien apoyado** |
| Quipus “pareados” como partida doble | **propuesto**; el corpus tiene duplicados de catálogo que inflan cualquier parecido |
| Puruchuco: sumas internas y quipus-resumen | **no comprobable** con los metadatos del repo |

## 7. Limitaciones

- El corpus KFG **no es una muestra aleatoria** de quipus: está sesgado hacia colecciones de museo europeas/americanas y hacia quipus conservados.
- La `procedencia` es de museo, no lugar de origen (regla 6); no se usó como variable causal.
- La dirección de nudo se infiere de la cadena `nudos`; los racimos con dirección `U` (8 541) quedaron fuera.
- En E no se conocen los pares físicamente atados: el test es una cota superior, no una prueba del emparejamiento real.
- El “orden” de las cuerdas es el de registro del KFG; si el registro no respeta la izquierda→derecha física, el test de posición de D se atenúa (no se infla).

## 8. Para el coordinador

- Se extrajeron **19 afirmaciones** contrastables de las 12 fichas: 3 `si`, 10 `parcial`, 6 `no`. La tabla está en `afirmaciones.csv`.
- **Las cifras descriptivas de la literatura se replican casi exactamente** en el corpus: 88,8 cordeles/quipu (vs. 84), 64,1 colgantes (vs. 60; mediana 32 vs. 27), 22,6 % de colgantes con subsidiarias (vs. ~25 %), 61 códigos de color (vs. 52). Es validación de tubería, **no** confirmación independiente: KFG y KDB describen los mismos objetos.
- **UR19 desmiente el “π”**: 13+5 cuerdas y 26,0 cm coinciden, pero el total es **100**, no 40,9; `100/13 = 7,69`. La tasa base de encontrar π así es 1/651, igual que encontrar un 6 redondo.
- **VA42527**: la estructura 21/0 coincide, pero **881/29,5 = 29,86**, no un múltiplo. El “calendario lunar” es redondeo selectivo.
- **Hyland 2014 se sostiene solo a medias**: la dirección S/Z no es azar (p = 0,0003 en tres tests, sobrevive BH), pero se agrupa en bloques **sin orientación consistente** (S después de Z en 97/199), no forma mitades limpias (mediana de diferencia = 0,10; 1/199 perfecto) y está confundida con la presencia de nudo largo (77,6 % vs. 56,4 %). **S = Hanan / Z = Urin sigue siendo propuesto, no bien apoyado.**
- **Inkawasi: resultado negativo.** Mejor par JC015–UR257 r = 0,857, pero el máximo nulo es 0,47 y p = 0,113; ningún par Incahuasi llega a r ≥ 0,9 frente a 25 pares en el resto del corpus.
- **Alerta de datos:** KH0033 y UR044 son **el mismo quipu con dos ids** (54 colgantes, valores idénticos, mismo `pc_largo`); UR070/UR071 es otro duplicado. Cualquier análisis de similitud/“copias” debe deduplicar antes.
- **Puruchuco (Urton & Brezine 2005) no es identificable** en `quipus.csv`: 0 quipus con esa procedencia. Es la afirmación más importante de la lista que queda fuera de alcance; recomiendo pedir el mapeo KH→procedencia.
- **Recomendación siguiente ronda:** (1) construir el mapa KH↔procedencia para recuperar Puruchuco y los 21 quipus; (2) probar la hipótesis de Hyland con los quipus híbridos/documentos asociados, no con el corpus general; (3) testear “partida doble” solo tras deduplicar y con nulo de multiset; (4) no volver a usar correlaciones sobre valores ordenados: su mediana basal es 0,87 y produce falsos positivos.
