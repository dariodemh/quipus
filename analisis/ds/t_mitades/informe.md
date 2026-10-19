# Dualidad andina y mitades en los quipus: ¿simetría especular?

**Equipo:** t_mitades · **Fecha:** 18-10-2026 · **Datos:** KFG (`analisis/datos/`, 651 quipus, 57 818 cuerdas, 41 714 pendientes) · **Semilla:** 20261018

---

## 1. Pregunta

La hipótesis de la dualidad andina (hanan/hurín, mitades, moieties) predice que un quipu puede dividirse en dos conjuntos espejo: mismo número de cuerdas, misma secuencia de colores, sumas iguales o en razón fija, o dos códigos binarios complementarios (R/V, S/Z). Se testea en todo el corpus KFG con modelos nulos explícitos.

Predicciones operacionalizadas:

1. **H1 (sumas):** la suma de la primera mitad de los pendientes se parece a la de la segunda más de lo que predice una asignación aleatoria de los mismos valores.
2. **H2 (estructura):** las posiciones espejo (i-ésima desde la izquierda vs i-ésima desde la derecha) repiten valores y colores más de lo esperado; los grupos emparejados en espejo tienen sumas y tamaños iguales.
3. **H3 (código):** R vs V, S vs Z y AB vs MB definen dos mitades equilibradas en número de cuerdas y en suma de valores.
4. **H4 (mitades locales):** dentro de cada grupo de colgantes, la primera mitad repite la segunda.
5. **H5 (Hyland 2014 / Medrano-Urton 2018):** S se concentra en la mitad superior y Z en la inferior; R/V separa mitades; ambos códigos están alineados entre sí.

La explicación aburrida que hay que descartar primero es que los valores y colores estén **agrupados en bloques** (grupos, secciones de color) y que cualquier corte contiguo herede ese agrupamiento sin que exista una regla de dualidad.

### 1.1 Antecedentes y qué predice cada uno

- **Urton (2003, *Signs of the Inka Khipu*):** los rasgos de manufactura (torsión, ply, dirección de nudo, orientación del amarre) formarían un código binario. La ficha advierte que es una tesis teórica, sin resultados cuantitativos ni controles en el resumen: “que un rasgo sea binario no implica que codifique información significativa”.
- **Ascher (2005):** en 59 quipus bien descritos, spin y ply son uniformes; la dirección de nudo es uniforme en ~81 % y mixta en ~19 %. Spin, ply y dirección **no** distinguen datos cuantitativos de no cuantitativos. Es el control obligado de cualquier lectura binaria.
- **Hyland, Ware & Clark (2014):** en **un** quipu/texto híbrido, nudos S ↔ Hanan (superior) y Z ↔ Urin (inferior). El dato es “apoyado con datos” para ese objeto; la extrapolación al corpus es una propuesta con n = 1.
- **Clindaniel (2019):** la dirección S/Z no es aleatoria (Z dominante salvo Armatambo), pero la interpretación Z = no marcado / S = marcado es propuesta.
- **Medrano y Urton (2018):** en seis quipus del Santa, los amarres R/V de las primeras cuerdas de grupos de seis dividirían a los tributarios en moieties. Coincidencia numérica apoyada; la partición social es propuesta.
- **Urton (2019):** UR28 tendría tres agrupaciones que suman 102 y seis ayllus en dos mitades (AB = hanan, MB = hurín). Las igualdades aritméticas son verificables; la semántica de color/mitad es especulativa y circular.

Estas fuentes permiten una predicción corpus-wide clara: si la dualidad fuera un principio general, los cortes por mitad, por R/V, por S/Z o por AB/MB deberían mostrar exceso de simetría (sumas iguales, conteos equilibrados, secuencias espejo) frente a un nulo que preserve la composición local.

---

## 2. Datos y unidad

- 651 quipus, 41 714 pendientes (`nivel == 0`), 57 818 cuerdas en total.
- 604 quipus con ≥6 pendientes; 567 entran en el test de sumas (algún valor > 0 en cada mitad).
- `valor` solo se usa si la cuerda tiene nudos (`nudos` no vacío). Las **13 192** cuerdas sin nudos (31,6 % de los pendientes) se tratan como **ausentes**, no como cero.
- Los grupos se toman de la columna `grupo` de `cuerdas.csv`; las sumas de grupo **incluyen subsidiarias** (una subsidiaria se asigna al grupo de su madre). Esto reproduce exactamente el caso UR028 de Urton (2019), como se ve en §4.7.
- Unidad de inferencia: **el quipu**. Los estadísticos se calculan por quipu y luego se promedian con peso igual; los nulos permutan dentro de cada quipu.

---

## 3. Método

### 3.1 Estadísticos

| Bloque | Estadístico por quipu |
|---|---|
| Sumas de mitades | \|log(s₁/s₂)\|, con s₁ = suma de la 1.ª mitad y s₂ = 2.ª mitad (se descarta el cordel central si n es impar) |
| Igualdad exacta | indicador s₁ = s₂ |
| Razón fija | indicador de razón ≈ 2:1 o 3:1 (tolerancia 2–6 %) |
| Espejo de valores/colores | tasa de coincidencia en pares (i, n−1−i); control: pares paralelos (i, m+i) |
| Mitades de código | \|log(suma_R/suma_V)\|, \|log(suma_S/suma_Z)\|, \|log(suma_AB/suma_MB)\|; \|n_a−n_b\|/N |
| Grupos espejo | media de \|log(s_i/s_j)\| y de \|n_i−n_j\|/(n_i+n_j) para pares i, G−1−i |
| Bloques | n.º de rachas, pureza de grupo, cambios en frontera de grupo, estadístico de punto de cambio máx.\|p_izq−p_der\| |
| Asociaciones | diferencia de tasas (R entre S y Z; R o S entre AB y MB) y diferencia de log-valor entre categorías |

La predicción “mismo número de cuerdas” aplicada a las dos mitades posicionales es trivial por construcción (difieren como máximo en 1). Por eso se testea en los **grupos emparejados en espejo** (§4.1) y en los **conteos por categoría** R/V, S/Z y AB/MB (§4.3).

### 3.2 Modelos nulos

- **N1 — permutación de cuerdas dentro del quipu:** preserva la distribución marginal de valores/etiquetas y el tamaño de las mitades, rompe el orden. Es el nulo primario de H1–H2.
- **N2 — permutación de grupos completos:** preserva la composición interna y el tamaño de cada grupo, solo reordena bloques. Es el nulo correcto para separar “mitades” de “bloques contiguos” (H1 y H2). Sin este nulo, cualquier agrupación por grupos produce falsos positivos.
- **N3 — binomial(N, 0,5):** para el equilibrio de conteos entre dos categorías (H3).
- **N4 — scan de punto de cambio:** se evalúa el mejor corte en el 20–80 % central y se compara su posición con la permutación; si las mitades fueran reales, el corte debería concentrarse en 0,5.
- B = 2 000 permutaciones (4 000–5 000 en los tests de robustez), p empírico = (1 + nº nulos ≥/≤ observado)/(B+1). Semilla fija.
- **Corrección múltiple:** familia confirmatoria de 12 tests → Holm. Los tests estructurales y de asociación posteriores se declaran exploratorios y se corrigen con BH-FDR sobre 42 pruebas.

---

## 4. Resultados

### 4.1 Sumas de la primera vs segunda mitad: no son espejo, hay un gradiente

| Test | n quipus | Observado | Nulo | z | p (dirección predicha) | Holm |
|---|---:|---:|---:|---:|---:|---:|
| Simetría de sumas, media \|log(s₁/s₂)\| | 567 | **0,861** | 0,592 | **+15,6** | 1,000 (la predicha era menor) | 1,000 |
| Igualdad exacta de sumas | 567 | **1,23 %** | 1,40 % | −0,4 | 0,738 | 1,000 |
| Razón fija 2:1 o 3:1 | 567 | 9,5 % | 8,9 % | +0,6 | 0,306 | — |
| Grupos espejo: sumas | 415 | **1,330** | 1,233 | **+5,3** | 1,000 | 1,000 |
| Grupos espejo: tamaños | 415 | **0,279** | 0,264 | **+3,8** | 1,000 | 1,000 |

El signo del efecto va **en contra** de la hipótesis: las mitades son *menos* parecidas que una asignación aleatoria de los mismos valores (p de la cola opuesta = 0,0005). Controles robustos:

- **Mediana** de \|log(s₁/s₂)\|: 0,559 observada vs 0,331 nula (z = +13,1; p cola opuesta < 0,0003). No lo conducen valores extremos. (El test de robustez usa 570 quipus y permuta también la posición de los faltantes; el primario fija el patrón observado y exige ≥4 valores.)
- **Signo:** en **61,0 %** de los quipus s₁ > s₂ (nulo 49,2 %; p = 0,0005). Mediana de la razón s₁/s₂ = **1,22** (IQR 0,78–2,16); solo 6,3 % de los quipus tiene mitades dentro del ±5 % (nulo 10,2 %).
- **Nulo de grupos completos:** 0,861 vs 0,710 (z = +8,9; p cola opuesta = 0,0005). El gradiente no se explica solo por la composición de los grupos.
- **Faltantes:** en la submuestra con ≤10 puntos porcentuales de diferencia de faltantes entre mitades (n = 305), s₁ > s₂ en **61,3 %**. La primera mitad tiene algo más de cuerdas con nudos (81,0 % vs 77,6 % de media), un confundente que empujaría a favor de s₁ > s₂; pero el efecto persiste al equilibrar faltantes, así que no se explica por ellos.
- **Quitar el primer cordel de cada grupo** (posible “total” de sección; exploratorio) *aumenta* la asimetría: 80,2 % con s₁ > s₂ (n = 429). No es un artefacto de los totales iniciales.
- Tendencia monótona valor~posición: ρ de Spearman medio = **−0,073** (nulo 0,000; z = −7,4). Hay un descenso leve de izquierda a derecha.

**Lectura:** no hay mitades de suma igual; hay un orden decreciente sistemático. La igualdad exacta (1,23 %) es incluso menos frecuente que la esperada por azar (1,40 %).

### 4.2 Espejo de valores y colores en posiciones

| Test | n | Observado | Nulo | z | p |
|---|---:|---:|---:|---:|---:|
| Valores, posiciones espejo | 528 | 10,6 % | 11,1 % | −1,3 | 0,894 |
| Valores, posiciones paralelas (control) | 528 | 10,1 % | 11,1 % | −2,5 | 0,996 |
| Color primario, espejo | 601 | **46,3 %** | 48,8 % | −6,0 | 1,000 (cola opuesta 0,0005) |
| Color primario, paralelo (control) | 601 | 45,7 % | 48,8 % | −7,6 | 1,000 |
| Color exacto, espejo | 601 | 35,0 % | 38,1 % | −8,4 | 1,000 |
| Color primario, espejo vs **nulo de grupos** | 601 | **46,34 %** | **46,32 %** | **+0,04** | 0,530 |

Tres resultados importantes:

1. El espejo **no supera de forma apreciable al paralelo** (10,6 % vs 10,1 % en valores; 46,3 % vs 45,7 % en color) y ambos quedan **por debajo del nulo**: no hay una orientación especular privilegiada.
2. La aparente “anti-simetría” del color desaparece por completo al permutar **grupos completos** (46,34 % vs 46,32 %). Es decir, el color está organizado en bloques contiguos; el desajuste entre mitades es el valor esperado bajo esa estructura de bloques, no una regla de dualidad.
3. La composición de color de las dos mitades es **más distinta** de lo esperado: distancia de variación total 0,308 vs 0,200 (z = +23,3; p cola opuesta = 0,0005). Las mitades no comparten la misma paleta; el quipu cambia de sección de color.

### 4.3 Mitades definidas por el código: R/V, S/Z, AB/MB

Primero, la condición de posibilidad: los códigos binarios están **casi siempre ausentes o son muy desbalanceados**.

- Solo **159/448** quipus con datos de unión tienen R y V (35,5 %); **237/507** tienen S y Z (46,7 %); solo **28/515** tienen torsión S y Z (5,4 %).
- Entre los quipus mixtos, la categoría minoritaria es de mediana **21,7 %** (R/V), **17,8 %** (S/Z) y **10,0 %** (AB/MB). No son mitades 50/50: son una categoría dominante con una minoría marcada (consistente con Ascher 2005 y Clindaniel 2019).
- \|n_a−n_b\|/N observado: **0,547** (R/V), **0,609** (S/Z), **0,476** (AB/MB); binomial(0,5) esperaría 0,118, 0,136 y 0,169 (z = +54, +63, +32; q_BH < 0,002). El desequilibrio es masivo.

| Mitad de código | n | \|log(suma_a/suma_b)\| obs. | Nulo | z | p (igualdad) | q_BH |
|---|---:|---:|---:|---:|---:|---:|
| R vs V | 141 | 1,922 | 1,878 | +0,6 | 0,712 | 1,000 |
| S vs Z | 226 | **3,210** | 2,292 | **+16,4** | 1,000 (cola opuesta 0,0002) | 0,0017 |
| AB vs MB | 188 | **1,764** | 1,553 | **+3,4** | 1,000 (cola opuesta 0,001) | 0,0034 |

Las sumas exactamente iguales son prácticamente inexistentes: 0/153 (R/V), 2/226 = 0,9 % (S/Z), 0/214 (AB/MB). **Ningún código binario define dos mitades de igual total.** S/Z y AB/MB van además en dirección contraria: sus dos categorías suman *menos* parecido que el azar.

### 4.4 Mitades dentro de cada grupo

Si la dualidad fuera local (cada grupo partido en dos), debería verse aquí.

| Test | n quipus | Observado | Nulo | z | p |
|---|---:|---:|---:|---:|---:|
| Suma, 1.ª vs 2.ª mitad del grupo | 543 | **0,999** | 0,856 | **+10,0** | 1,000 (cola opuesta 0,0005) |
| Igualdad exacta de sumas | 543 | 4,30 % | 3,86 % | +1,1 | 0,132 |
| Color primario, espejo dentro del grupo | 566 | **55,1 %** | 58,2 % | −7,5 | 1,000 (cola opuesta 0,0005) |
| S/Z, 1.ª vs 2.ª mitad del grupo | 421 | **+0,0158** | 0,000 | +2,5 | 0,018 (dos colas); q_BH = 0,028 |
| R/V, 1.ª vs 2.ª mitad del grupo | 397 | +0,0042 | 0,000 | +1,0 | 0,340 |

La única señal positiva es minúscula: **+1,6 puntos porcentuales** más S en la primera mitad del grupo (0,0158 en proporción; p = 0,018; q_BH = 0,028, en el límite), sin efecto en R/V. No sostiene una lectura de moieties.

### 4.5 Lo que sí hay: segmentación en bloques, pero no en mitades

| Test | n | Observado | Nulo cuerdas | Nulo grupos | z |
|---|---:|---:|---:|---:|---:|
| R/V: n.º de rachas | 153 | **9,91** | 24,84 | 11,41 | **−15,3** |
| R/V: pureza de grupo | 148 | **66,9 %** | 39,8 % | — | +31,8 |
| R/V: cambios en frontera de grupo | 153 | **38,0 %** | 18,2 % | — | +18,5 |
| R/V: max\|p_izq−p_der\| | 153 | **0,418** | 0,198 | 0,321 | +12,4 |
| S/Z: n.º de rachas | 226 | **12,61** | 16,75 | 13,23 | **−9,0** |
| S/Z: pureza de grupo | 204 | **54,8 %** | 45,0 % | — | +12,9 |
| S/Z: cambios en frontera de grupo | 226 | **28,1 %** | 22,0 % | — | +5,8 |
| S/Z: max\|p_izq−p_der\| | 226 | **0,308** | 0,217 | 0,267 | +7,5 |

Todos con p ≤ 0,001 y q_BH ≤ 0,002. R/V y S/Z forman **bloques contiguos** que respetan las fronteras de grupo más de lo esperado, pero también hay estructura dentro de los grupos (el nulo de grupos no lo elimina). Las rachas y maxD se contrastan además contra el nulo de grupos (columna “Nulo grupos”); pureza y frontera se contrastan contra el nulo de cuerdas. La impresión cualitativa de “dos mitades” viene de estos bloques.

Pero **los bloques no son mitades**:

- Quipus con exactamente 2 rachas: 24/153 (R/V) y 16/226 (S/Z).
- En esos casos, el corte cae en [0,4; 0,6] solo en **16,7 %** (R/V) y **6,2 %** (S/Z); la mediana del corte es 0,46 (IQR 0,07–0,84) y 0,58 (IQR 0,27–0,88). Los cortes están repartidos por todo el quipu, no en el centro.
- Scan de punto de cambio: la posición óptima tiene \|argmax−0,5\| medio 0,189 (R/V) y 0,192 (S/Z), frente a 0,194 y 0,188 en el nulo. La diferencia es de 0,005 en una escala de 0 a 0,5: no hay concentración relevante en el centro (test de “más central que el nulo”: p = 0,02 y 0,055, con un efecto despreciable).

### 4.6 Asociaciones entre códigos y con el color

- **R/V × S/Z:** independientes. Diferencia de tasa R entre S y Z = 0,0016 (nulo −0,0006; p = 0,94; n = 84). No hay un “código binario único” que se exprese a la vez por unión y por dirección de nudo.
- **R/V × AB/MB:** −0,037 (p = 0,12; n = 74). **S/Z × AB/MB:** +0,013 (p = 0,63; n = 88). El color AB no marca ni R ni S.
- **AB vs MB y valor:** AB tiene valores mayores en bruto (+0,267 en log; p = 0,0005; n = 161), pero el efecto dentro de grupo es frágil: +0,205 en el test estratificado por quipu (27 quipus; q_BH = 0,021), mientras que el análisis por grupo da +0,14 (grupos con ≥1 cuerda de cada color), +0,08 (≥2) y **−0,12 (≥4)**. El signo cambia con el umbral: no es robusto. La hipótesis “AB = hanan (mitad superior con más valor)” no se sostiene.
- **S/Z y valor:** en bruto, las cuerdas S tienen valores menores que las Z (−0,404 en log dentro de grupo; p = 0,0005). Pero al estratificar por **(grupo, tipo del primer nudo, n.º de nudos)** el efecto cae a **−0,054** y solo el 36,8 % de los 152 estratos es negativo (test de signos p = 0,0015 en la dirección *contraria*). La asociación bruta se explica por la composición de tipos de nudo, no por un significado de moiety.
- **AB/MB en mitades:** diferencia de proporción AB (1.ª − 2.ª) = −0,015 (p = 0,17; n = 268). No hay más AB en la primera mitad.
- **Grupos adyacentes:** sus sumas son **más parecidas** que las de grupos aleatorios: 1,077 vs 1,257 (z = −13,0; p = 0,0005), y la igualdad exacta de sumas ocurre en **3,66 %** de los pares adyacentes vs 2,40 % nulo (p = 0,0002). La relación aritmética es **local y secuencial**, no especular.
- Orden de grupos vs suma: ρ medio = −0,118 (solo 39,9 % positivo); vs tamaño: −0,037. Hay una leve tendencia a que los grupos mayores/valiosos estén al principio, coherente con el gradiente de §4.1.

### 4.7 Caso UR028 (Urton 2019): 102 = 102, pero no es una mitad

Con las sumas de grupo que incluyen subsidiarias, la reconstrucción desde KFG da:

| Sección | Suma |
|---|---:|
| p1 (cordel único) | **102** |
| p2–p4 + subsidiarias | **102** |
| Grupos 2–7 (p5–p76 + subsidiarias) | 32 + 8 + 0 + 24 + 0 + 40 = **104** |
| p5–p74 (sin p75–p76) | 97 |

El primer 102 = 102 se reproduce exactamente y es **demostrado** dentro del artefacto. La suma de los grupos 2–7 (p5–p76 + subsidiarias) da 104 en KFG; Urton reporta 102 para las seis agrupaciones y declara un error de registro de 2 unidades, de modo que 104 = 102 + 2 es consistente con su lectura. La delimitación literal “#5–74” no coincide con los índices KFG (p5–p74 da 97), probablemente porque Urton cuenta cordeles y no pendientes. Lo que importa: las dos mitades posicionales del quipu suman **200 vs 56**, no 102 vs 102. El caso ilustra el patrón real: **totales repetidos en secciones anidadas**, no dos mitades especulares.

---

## 5. Controles, robustez y corrección múltiple

1. **Nulo explícito en todos los tests.** Para sumas y espejos se usa permutación dentro del quipu; para separar bloques de mitades se añade el nulo de grupos completos. Sin el segundo, el color “parecía” anti-simétrico (z = −6) cuando en realidad era exactamente lo esperado por bloques (z = +0,04).
2. **p-valores empíricos** con resolución 1/(B+1) (0,0005 con B = 2 000; 0,0002 con B = 5 000). Varios p están en el piso; se reporta el z y el tamaño del efecto, no solo el p.
3. **Holm** sobre 12 tests confirmatorios: solo las rachas de S/Z y R/V sobreviven (p_Holm = 0,012). Ningún test de simetría sobrevive. **BH-FDR** sobre 42 tests exploratorios: los hallazgos de bloques, desequilibrio de conteos, grupos adyacentes y gradiente tienen q ≤ 0,003.
4. **Heterogeneidad:** el efecto de sumas no es de unos pocos quipus: el signo s₁ > s₂ aparece en 61 % de 567. El de bloques aparece en la mayoría de los quipus con ambas categorías.
5. **Faltantes:** el resultado de sumas persiste en la submuestra con faltantes equilibrados (61,3 %); la falta de nudos es más frecuente en la primera mitad, lo que va en contra del efecto.
6. **Valores extremos:** mediana y test de signos confirman el resultado; no depende de los cocientes extremos.
7. **Confusión por tipo de nudo:** la asociación S/Z–valor desaparece al estratificar por tipo y número de nudos.
8. **Confusión por composición de grupo:** la asociación AB/MB–valor no es robusta dentro de grupo.
9. **Descriptivo, no causal:** el KFG es una decodificación moderna; “primera mitad” es el orden de registro, no necesariamente el orden en que el quipu se doblaba o se leía.

---

## 6. Resultados negativos (explícitos)

- **No hay mitades de suma igual:** 1,23 % de igualdad exacta (menos que el 1,40 % nulo); mediana de razón 1,22; solo 6,3 % dentro del ±5 %.
- **No hay espejo de valores:** 10,6 % de coincidencia en posiciones espejo, por debajo del nulo (11,1 %) y del control paralelo (10,1 %).
- **No hay espejo de colores:** 46,3 % vs 48,8 % nulo; y el nulo de grupos lo lleva a 46,34 % vs 46,32 %. El color forma bloques, no mitades.
- **No hay mitades R/V, S/Z ni AB/MB equilibradas:** minoría mediana 10–22 %; desequilibrio de conteos z = +32 a +63; sumas no iguales (R/V p = 0,71; S/Z y AB/MB incluso menos iguales que el azar).
- **No hay alineación R/V ↔ S/Z** (p = 0,94) ni color AB ↔ R/S (p = 0,12 y 0,63).
- **No hay más AB en la primera mitad** (p = 0,17).
- **No hay mitades locales dentro de los grupos:** sumas menos iguales que el azar; color menos repetido; R/V sin efecto; S/Z +1,6 pp (no sobrevive a Holm).
- **No hay concentración del punto de cambio en el centro:** 16,7 % y 6,2 % de los cortes en [0,4; 0,6] para los quipus de 2 bloques.
- **No hay asociación S/Z–valor** tras controlar tipo de nudo (efecto −0,05, inconsistente entre estratos).

---

## 7. Nivel de evidencia

| Conclusión | Nivel |
|---|---|
| UR028: p1 = 102 y p2–p4 + subsidiarias = 102 (aritmética interna verificable) | **Demostrado** |
| Las mitades posicionales de los quipus **no** son especulares en sumas, valores ni colores; el efecto va en dirección contraria (gradiente decreciente) | **Apoyado con datos** (n = 528–601; nulos N1 y N2; mediana y signos) |
| R/V y S/Z forman **bloques contiguos** que respetan fronteras de grupo, pero no se alinean con la mitad del quipu | **Apoyado con datos** (n = 153–226; q_BH ≤ 0,002) |
| Los códigos binarios están **desbalanceados** y ausentes en la mayoría de los quipus (minoría 10–22 %) | **Apoyado con datos** (n = 153–226; binomial) |
| Las sumas de **grupos adyacentes** se parecen más que las de grupos aleatorios (relación aritmética local/sequencial) | **Apoyado con datos** (n = 471; q_BH = 0,0017) |
| El gradiente izquierda→derecha refleja una jerarquía contable (totales al inicio, componentes después) | **Propuesto** (descriptivo; no testeado contra un modelo contable explícito) |
| Los bloques R/V y S/Z corresponden a secciones/parciales de cuenta y no a moieties globales | **Propuesto** |
| La dualidad hanan/hurín se codifica en estos rasgos a escala de quipu | **No apoyado / especulativo** (la predicción corpus-wide falla) |
| AB = hanan y S = hanan en el corpus | **Especulativo** (n = 1 en Hyland 2014; sin señal corpus-wide) |

---

## 8. Limitaciones

- El KFG decodifica valores con convenciones modernas; un error sistemático de decodificación afectaría los niveles, no la conclusión cualitativa de ausencia de espejo.
- “Primera mitad” es un corte por número de pendientes en el orden KFG. Si los quipus se leían plegados o en orden distinto, el corte no coincide con la mitad emic. Se probó también el corte por grupos y dentro de grupos; ninguno muestra espejo.
- Los grupos del KFG se definen por espaciado; la inclusión de subsidiarias cambia algunas sumas (por eso se reporta el caso UR028 con y sin p1/p75–p76).
- **La pureza de grupo de R/V y S/Z puede reflejar en parte convenciones de transcripción** (registrar un solo valor por grupo). El hallazgo de bloques se apoya también en la estructura dentro de grupos y en el nulo de grupos, pero no puede separarse del todo de la práctica de registro. La dirección de nudo, además, está ligada al tipo de nudo, así que parte de su agrupamiento puede ser mecánica.
- El gradiente izquierda→derecha podría deberse a una convención de ordenación si el KFG ordenara por valor; el orden declarado es físico (izquierda→derecha) y el efecto persiste al quitar el primer cordel de cada grupo, pero no es una prueba definitiva.
- 651 quipus de museo no son una muestra aleatoria; la ausencia de señal no prueba que ningún quipu tuviera mitades, solo que no es un principio general del corpus.
- Los tests de asociación son observacionales; “independencia” significa ausencia de asociación lineal de tasas, no independencia semántica.
- No se usó procedencia museística como origen (regla del brief).

---

## 9. Para el coordinador

- **La hipótesis de mitades especulares no se sostiene en el corpus.** En 567–570 quipus, la mediana de \|log(s₁/s₂)\| es 0,559 frente a 0,331 nula; solo 1,23 % tiene sumas exactamente iguales (nulo 1,40 %) y solo 6,3 % cae dentro del ±5 % (nulo 10,2 %).
- **El efecto va en dirección contraria:** en 61 % de los quipus la primera mitad suma más que la segunda (nulo 49 %; p = 0,0005). Hay un gradiente decreciente izquierda→derecha (ρ = −0,073), no una simetría.
- **Los colores no se reflejan:** la coincidencia en posiciones espejo es 46,3 % vs 48,8 % nula; con el nulo de grupos completos queda 46,34 % vs 46,32 %. El color está en bloques contiguos, no en mitades.
- **Los códigos R/V y S/Z forman bloques fuertes** (rachas 9,9 vs 24,8 y 12,6 vs 16,7; pureza de grupo 67 % y 55 %), pero **no son mitades**: solo 16,7 % y 6,2 % de los quipus con exactamente 2 bloques (24 y 16 quipus) tienen el corte en [0,4; 0,6].
- **R/V y S/Z son independientes entre sí** (p = 0,94) y no se alinean con AB/MB (p = 0,12 y 0,63). No hay un “código binario único” de moiety.
- **Los códigos están desbalanceados:** la categoría minoritaria mediana es 21,7 % (R/V), 17,8 % (S/Z) y 10,0 % (AB/MB); los conteos se apartan masivamente de 50/50 (z = +32 a +63). Son rasgos marcados, no mitades.
- **La única estructura aritmética robusta es local:** las sumas de grupos adyacentes se parecen más que las aleatorias (1,077 vs 1,257; igualdad exacta 3,66 % vs 2,40 %). La contabilidad se organiza en secciones consecutivas, no en espejos.
- **UR028 reproduce 102 = 102** (p1 y p2–p4 + subsidiarias), pero sus mitades posicionales suman 200 vs 56. Es un caso de totales anidados, no de dos mitades.
- **La asociación S/Z–valor es un artefacto del tipo de nudo:** cae de −0,404 a −0,054 al estratificar por tipo y número de nudos. No la usaría como evidencia semántica.
- **Recomendación:** buscar la dualidad, si existe, en **secciones contiguas y en la aritmética local** (pares/tríos de grupos, totales y parciales), no en cortes del quipu por la mitad; y testear la hipótesis hanan/hurín solo donde haya una etiqueta externa (UR028, Santa Valley, tablas de khipu), no en el corpus completo.

---

## 10. Reproducibilidad

Scripts en `analisis/ds/t_mitades/` (Python 3.13, pandas/numpy/scipy):

| Script | Qué hace | Salida |
|---|---|---|
| `explorar.py` | cobertura y forma de los datos | consola |
| `mitades.py` | 12 tests confirmatorios de mitades posicionales + Holm | `resultados.json`, `por_quipu.csv` |
| `bloques.py` | rachas, pureza, fronteras, scan de cambio, nulo de grupos, asociaciones | `bloques.json` |
| `totales.py` | mitades definidas por R/V, S/Z, AB/MB (sumas y conteos) | `totales.json` |
| `dentro_grupo.py` | mitades dentro de cada grupo | `dentro_grupo.json` |
| `robustez_sumas.py` | mediana, signo y proporciones con B = 4 000 | `robustez_sumas.json` |
| `consolidar.py` | tablas, BH-FDR y descriptivos | `descriptivos.json` |

Semilla 20261018; B = 2 000 salvo `robustez_sumas.py` (4 000) y `totales.py` (5 000). Los logs de ejecución están en `log_*.txt`.
