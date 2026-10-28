# Ficha de 9 cuerdas de Nazca/Berlín: marcadoras, alineamiento, sumas y género

**Autor:** equipo `n_ficha_nazca` · **Semilla:** 20261018 · **Fecha:** 2026-10-18
**Base:** `analisis/ds/n_ur1140_nazca/informe.md` (ficha congelada de 7 campos) y sus scripts.
**Datos:** `analisis/datos/cuerdas.csv`, `quipus.csv`, `grupos.csv`; OKR `khipu.db` solo lectura (no se usó para crear nada).
**Scripts:** `lib.py`, `p1_marcadoras.py`, `p2_alineamiento.py`, `p3_sumas.py`, `p4_barrido.py`, `p5_genero.py`, `p6_control.py`, `p7_controles.py`, `ficha_final.py`.
**Salidas:** `ficha_nazca.csv`, `resumen_quipus.csv`, `marcadoras.csv`, `alineamiento_120.csv`, `sumas.csv`, `barrido_corpus.csv`, `genero.csv`, `comparacion_formatos.csv`.

---

## 1. Pregunta

1. **Las 2 marcadoras.** ¿Qué son (color, valor, torsión, unión, dirección de nudo)? ¿Qué distingue a la primera de la segunda? ¿Su posición (inicio, final, medio) se asocia al total del registro, al orden de los campos o al color dominante?
2. **Campos 3–7.** Alinear los perfiles de los 4 quipus del formato probando las 120 permutaciones, con corrección por el máximo. ¿Hay una permutación que haga coincidir los 4?
3. **Relaciones numéricas.** ¿Algún campo es suma de otros? ¿Campo 1 = suma de 2..7? ¿Sumas entre registros o entre quipus (UR1140/UR1136, museo consecutivo VA16635/6)?
4. **Búsqueda de la ficha** (congelada: 9 cuerdas, 2 marcadoras, campo 1 máximo) en todo el corpus, y en grupos de 8 y 10 (variantes).
5. **Género.** Comparar con el Santa (6 campos, máximo en 4) y con Incahuasi (9 columnas ordenadas de mayor a menor): ¿existe un género «ficha de n campos con encabezado mayor»?

La hipótesis aburrida a batir: que «campo 1 máximo» sea un rasgo genérico de cualquier grupo de cuerdas (la primera cuerda suele ser grande), y que el parecido de los campos 3–7 sea un artefacto de probar 120 permutaciones.

---

## 2. Método

### 2.1 Registros

- Una fila por cuerda; se eliminan duplicados `(kfg, cuerda)`; `valor` solo si `nudos` no está vacío (regla del BRIEF).
- **Registro de n campos** = grupo de espaciado (`grupo`) con exactamente **n cuerdas de nivel 0**: n−2 cuerdas del color modal + **2 cuerdas marcadoras** de otro color. Para la ficha principal n = 9 (7 + 2). Variantes: n = 8 (6 + 2) y n = 10 (8 + 2).
- **Canonicalización congelada** (la del informe previo, sin reajustar): se invierte el orden de las n−2 cuerdas si la **segunda** marcadora (la de más a la derecha) cae en la mitad derecha (posición ≥ 5 para n = 9; ≥ 6 para n = 10; ≥ 5 para n = 8). Así el par queda como separador después de un encabezado de 2 campos.
- Color sin rangos en cm (`re.sub(r'\([^)]*\)','',s)`); en `nudos`, el número antes del tipo es el valor.
- Todos los tests de perfil usan `log10(valor+1)` estandarizado por registro.

### 2.2 Nulos y corrección

| Prueba | Nulo | B |
|---|---|---|
| 1.ª vs 2.ª marcadora (valor, largo) | test de signo pareado exacto | exacto |
| 1.ª vs 2.ª marcadora (color) | McNemar exacto | exacto |
| Posición del par (¿2 campos de un extremo?) | 2 posiciones uniformes al azar entre n | exacto |
| Lado del par en bloques | permutación de etiquetas de lado entre registros del quipu | 9 999 |
| Perfil vs ficha (UR1140) | permutación de valores **dentro de cada registro** | 999–9 999 |
| Alineamiento 3–7 | permutación dentro de registro + **máximo sobre las 120 permutaciones** | 4 000 |
| Identidades aditivas | remuestreo de valores del mismo quipu | 2 000 |
| Diferencia constante entre campos | permutación dentro de registro | 2 000 |
| Barrido del corpus | binomial vs tasa base de grupos con 2 marcadoras del mismo tamaño, **excluidos los focos** | exacto |

Corrección múltiple: **Holm** y **BH-FDR** sobre **todas** las pruebas de cada familia; se indica la familia. En el barrido se corrige por los 10 formatos probados y, para las correlaciones, además por los 651 quipus del corpus (p = 1 para los no testables), que es la versión conservadora.

### 2.3 Universo

651 quipus en `cuerdas.csv`; 169 en Nazca/Berlín/Santa. El formato de n campos + 2 marcadoras es raro: **71 grupos de 9** con 2 marcadoras (56 con los 7 campos completos) en 13 quipus, **30 grupos de 8** (16 completos) en 13 quipus y **29 grupos de 10** (19 completos) en 7 quipus. Solo 6 quipus tienen ≥3 registros completos (4 de 9 cuerdas, 1 de 8 y 1 de 10).

---

## 3. Resultados

### 3.1 Las dos marcadoras son gemelas, no dos atributos

En los 47 registros de los 4 quipus de 9 cuerdas:

| Atributo | 1.ª marcadora | 2.ª marcadora | Coinciden |
|---|---|---|---|
| Torsión | S 47/47 | S 47/47 | **47/47** |
| Unión | U 34, V 8, R 5 | U 34, V 8, R 5 | **47/47** |
| Color | B:BB 10, B:BB/B 4, B:G 4, W:BB 7, W:G 3, B 5, … | idénticos salvo 3 casos | **44/47** |
| Dirección del 1.er nudo | Z 33, S 12, — 2 | Z 33, S 6, — 8 | 41/47 |
| Valor (mediana) | 10–26,5 | 8–18 | 1.ª>2.ª en 15/38 (p = 0,26) |
| Largo (mediana) | 31–51,5 | 12,8–50,5 | 1.ª>2.ª en 24/45 (p = 0,77) |

Ninguna prueba pareada sobrevive Holm (15 pruebas; p mínima bruta 0,0309 en el valor de UR1140, Holm 0,46). **No hay un atributo intrínseco que distinga a la primera marcadora de la segunda**: son un par duplicado (misma torsión, misma unión, casi siempre mismo color y misma dirección). La única diferencia sistemática es **relacional**: cuál de las dos queda más cerca del encabezado.

Esto corrige una lectura tentadora del informe previo («las marcadoras codifican un atributo binario»): el par no son dos atributos, es **una sola marca repetida** que funciona como separador. Lo binario es el **lado** en que se coloca el par, no la diferencia entre sus dos cuerdas.

### 3.2 La posición del par: 2 campos desde un extremo, y el lado marca secciones

En los 71 grupos de 9 con 2 marcadoras del corpus, las posiciones del par son:

| Posición | n | Comentario |
|---|---:|---|
| (3,4) | 36 | 2 campos antes del par, 5 después |
| (6,7) | 19 | espejo de (3,4) |
| (1,9) | 6 | el par abarca todo el registro (UR1176) |
| (8,9) | 4 | par al final, sin cuerpo detrás |
| otras | 6 | — |
| **2 campos de un extremo** | **55/71 (77 %)** | (3,4) o (6,7) |

Bajo el nulo de 2 posiciones uniformes entre 9 (P = 2/36 = 0,056), 55/71 da p = 1,2·10⁻⁵⁴. Los tres tamaños por separado: p = 4,7·10⁻⁸ (n = 8), 1,2·10⁻⁵⁴ (n = 9) y 6,1·10⁻²¹ (n = 10); Holm ≤ 3,6·10⁻²⁰. **Bien apoyado: el par no está al azar; está a exactamente 2 campos de un extremo.** Ese es el «encabezado de 2 campos».

El **lado** (izquierda = (3,4), derecha = (6,7)) no es aleatorio a lo largo del quipu:

- UR1140: secuencia de lados `LLLLLLLL RRRRR O RRR LL` (O = par en (2,6); 5 rachas en 19 grupos), p = 0,0011.
- UR1136: `L RRRR LLLLLLLLL R` (4 rachas en 15), p = 0,028.
- UR223 y HP056 tienen un solo lado (no testeable).

Es decir, **el par separa secciones contiguas del quipu**, no registros sueltos.

Asociación del lado con propiedades del registro:

| Propiedad | Resultado | Nivel |
|---|---|---|
| Total del registro | UR1140: (3,4) 158,4 vs (6,7) 207,6; MWU p = 0,056 (no significativo) | negativo |
| Orden de los campos | Los perfiles crudos de (3,4) y (6,7) están **espejados**: r = −0,926; al canonicalizar, r = +0,926 | **bien apoyado** |
| Color dominante | UR1136: (3,4) = 10 W, (6,7) = 5 G (confusión perfecta). UR1140: ambos lados B. Corpus: Fisher W/no-W × L/R p = 0,134 | confundido en UR1136, no general |

**Lectura:** el par de marcadoras es un **separador de 2 campos de encabezado**; su lado indica el sentido de lectura y, en algunos quipus, coincide con un cambio de color/sección. En UR1136 el lado y el color están perfectamente confundidos, así que allí no se puede separar «sección» de «color».

### 3.3 Alineamiento de los campos 3–7: 120 permutaciones, resultado negativo

Perfil z de los 5 campos (canónico):

| Quipu | n | Perfil campos 3–7 |
|---|---:|---|
| UR1140 | 19 | [−0,05; 0,43; −0,55; 0,38; −0,22] |
| UR1136 | 14 | [−0,14; −0,05; 0,53; 0,09; −0,42] |
| UR223 | 7 | [−0,39; 1,27; 0,12; 0,46; −1,46] |
| HP056 | 5 | [−0,03; 0,80; 0,32; 0,30; −1,38] |

Mejor de las 120 permutaciones contra UR1140, con p corregido por el máximo (nulo: permutación dentro de registro, 4 000 réplicas):

| Quipu | r sin permutar | Mejor permutación | r máx | p(max) | Holm (4 pruebas) |
|---|---:|---|---:|---:|---:|
| UR1136 | −0,311 | (2,3,5,4,1) | 0,915 | 0,662 | 1,0 |
| UR223 | +0,590 | (3,2,5,4,1) | 0,956 | 0,335 | 1,0 |
| HP056 | +0,425 | (4,2,5,3,1) | 0,890 | 0,812 | 1,0 |
| **Conjunta (3 quipus)** | — | **(4,2,5,3,1)** | media 0,838 | **0,0197** | **0,079** |

- Las correlaciones altas (0,89–0,97) **no son evidencia**: con 5 campos, el máximo de 120 permutaciones alcanza rutinariamente valores ≈0,9 (los p(max) por par son 0,33–0,81). Un r = 0,96 puede salir por azar (UR223–HP056: r = 0,958 sin permutar, p(max) = 0,41).
- En la prueba **conjunta** el estadístico es la media de las 3 correlaciones; su nulo tiene media 0,51 y p95 ≈ 0,78, y el observado (0,838) deja p = 0,0197. Es el único resultado que se acerca, y no sobrevive Holm (0,079).
- La mejor permutación **no es la misma** para los tres quipus. La única regularidad compartida es que el último campo del otro quipu (nuestro campo 7) se alinea con su primer campo del cuerpo; es un efecto de los extremos, no un orden común.
- La prueba conjunta da p = 0,0197 bruto, pero **no sobrevive Holm** (0,079) y el óptimo conjunto es el mejor solo para HP056, no para UR1136 ni UR223.

**Nivel: negativo.** No hay una permutación que haga coincidir los perfiles de los 4 quipus. Lo compartido es el encabezado (campos 1–2), no el cuerpo.

### 3.4 Relaciones numéricas: tampoco hay sumas

| Prueba | UR1140 | UR1136 | UR223 | HP056 | p bruto mín. | Holm (16) |
|---|---:|---:|---:|---:|---:|---:|
| Campo 1 = suma de 2..7 | 0/19 | 1/14 | 0/7 | 1/5 | 0,0035 (HP056) | 0,056 |
| Campo 1 = suma de algún subconjunto de 2..7 | 11/19 | 5/14 | 1/7 | 4/5 | 0,0235 (UR1140) | 0,329 |
| Mejor diferencia constante entre dos campos | 16 % | 14 % | 43 % | 40 % | 0,276 | 1,0 |
| Total de un registro = suma de otros dos | 2 | 0 | 0 | 1 | 0,0795 | 1,0 |

- **Campo 1 no es la suma de los otros seis.** Ocurre en 2 de 45 registros (4,4 %), esperable por azar con enteros pequeños (p bruto 0,0035–0,007; Holm 0,056). La hipótesis «campo 1 = total aditivo del registro» **no se sostiene**.
- El mejor resultado aparente es UR1140: 11/19 registros tienen campo 1 = suma de *algún* subconjunto de los otros seis (p = 0,024 bruto), pero (a) el subconjunto cambia en cada registro, (b) con 63 subconjuntos posibles el hallazgo es débil y (c) Holm lo deja en 0,33. No hay una fórmula.
- No hay diferencias constantes entre pares de campos (nada análogo al «c = 15/10» de Incahuasi).
- UR1140 y UR1136 **no comparten totales de registro** (0 coincidencias) y la razón de totales no es constante (1,24). Se confirma el resultado previo: no son copias ni sumas.

**Nivel: negativo** para sumas internas y entre quipus.

### 3.5 Barrido del corpus: 5 quipus de 9 cuerdas, 1 de 8 y 1 de 10

Criterio: ≥3 registros completos con el formato (n−2 campos + 2 marcadoras). Tasa base = grupos con 2 marcadoras del mismo tamaño en el resto del corpus (excluidos los focos).

| Quipu | Tam. | Campos | Grupos | Completos | Máx. campo 1 | Base | p | Holm (10) | Museo / procedencia |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **UR1140** | 9 | 7 | 19 | 19 | **19/19 (100 %)** | 0,636 | 0,0002 | **0,0017** | Berlín / Nazca |
| **UR1136** | 9 | 7 | 15 | 14 | **13/14 (93 %)** | 0,636 | 0,0161 | 0,113 | Berlín / Nazca |
| UR223 | 9 | 7 | 8 | 7 | **7/7 (100 %)** | 0,636 | 0,0423 | 0,254 | Berlín / Ica |
| HP056 | 9 | 7 | 5 | 5 | **5/5 (100 %)** | 0,636 | 0,104 | 0,522 | Lima / desconocida |
| UR1176 | 9 | 7 | 6 | 0 | — | — | — | — | Berlín / Nazca |
| **UR234** | **8** | **6** | 10 | 4 | **4/4 (100 %)** | 0,200 | 0,0016 | **0,0128** | Berlín / desconocida |
| **UR1131** | **10** | **8** | 13 | 12 | **11/12 (92 %)** | 0,286 | 9,2·10⁻⁶ | **0,0001** | Berlín / Pachacamac |

- **UR234** (grupos de 8: 6 campos + par en (3,4), 10 grupos) y **UR1131** (grupos de 10: 8 campos + par en (7,8), 13 grupos) son **variantes nuevas** del mismo formato, no conocidas en el informe previo. UR234 tiene valores en miles (2007–3419 en el campo 1) y UR1131 en decenas; la escala cambia, la estructura no.
- **UR1131 valida la regla de orientación fuera de muestra**: sin invertir, el máximo está en el campo 1 en **0/12** registros; con la regla congelada (invertir porque el par está en la mitad derecha), en **11/12** (p = 0,0032 contra orientación al azar). La regla no se reajustó.
- UR1176 tiene 6 grupos con el par en (1,9), pero **0 registros completos** (el primer campo DB está vacío en todos): no confirma ni refuta.
- La tasa base de «campo 1 máximo» en grupos de 9 con 2 marcadoras es **63,6 %** (7/11), no el 1/7 uniforme: la primera cuerda tiende a ser grande aun sin ficha. Aun así, UR1140 (19/19) y UR1131 (11/12) quedan muy por encima; UR1136, UR223 y HP056 no sobreviven la corrección conservadora.

**Nivel:** *apoyado con datos* que el formato 2 campos + par + cuerpo existe en 6, 7 y 8 campos y que el campo 1 es el máximo; *bien apoyado* que el formato es raro (7 quipus de 651).

### 3.6 ¿Género «ficha de n campos con encabezado mayor»? Santa e Incahuasi

| Formato | Campos | Marcadores | Perfil por posición | Máx. en pos. 1 |
|---|---:|---:|---|---:|
| UR1140 (Nazca) | 7 | 2 | [**1,81**; −1,46; −0,13; 0,17; −0,43; 0,21; −0,18] | 100 % |
| UR1136 | 7 | 2 | [**1,73**; −1,49; −0,10; −0,01; 0,14; −0,06; −0,20] | 93 % |
| UR223 | 7 | 2 | [**2,23**; −0,73; −0,48; 0,25; −0,27; −0,10; −0,91] | 100 % |
| HP056 | 7 | 2 | [**1,87**; −0,39; −0,32; −0,02; −0,06; −0,02; −1,06] | 100 % |
| UR234 | 6 | 2 | [**1,86**; −0,56; −0,46; −0,14; 0,01; −0,72] | 100 % |
| UR1131 | 8 | 2 | [**2,03**; −0,09; −0,56; −0,34; −0,39; −0,31; −0,54; 0,20] | 92 % |
| **Santa** (6 quipus) | 6 | 0 | [−0,66; 0,33; −0,60; **1,66**; −0,41; −0,32] | **5,6 %** (61/72 bandas con máx. en pos. 4) |
| **Incahuasi UR278** | 9 | 0 | [0,89; **0,97**; −0,60; 0,05; 0,17; 0,51; −0,10; −1,05; −0,84] | **33 %** (8/24; 9/24 con máx. en pos. 2) |

- **Santa:** 6 campos sin marcadores, máximo en la **posición 4** (61/72 bandas, 85 %), mínimo en la 1. Es un formulario real (control positivo del método), pero **no es el mismo género**: no tiene encabezado mayor ni par separador. No se puede transferir el significado de sus campos.
- **Incahuasi UR278:** 9 columnas sin marcadores; el orden es **descendente solo en tendencia** (Spearman medio valor–posición −0,54; 0/24 grupos estrictamente decrecientes) y el máximo físico está en la columna 1 solo en 8/24 (la columna 2 suele ser mayor). Su perfil no correlaciona con la ficha Nazca (r = 0,20 en las 7 primeras posiciones).
- El **género compartido** no es «n campos con la primera grande» a secas: es **«encabezado de 2 campos + par de marcadoras + cuerpo plano»**. Bajo esa definición, los 6 quipus de 6–8 campos son el mismo género; el Santa y el Incahuasi son **otros** géneros (campos sin separador, perfiles en 4 o descendentes).

**Nivel:** *apoyado con datos* para el género de 6–8 campos con par; *negativo* para la asimilación al Santa o al Incahuasi.

---

## 4. Controles

1. **Nulo explícito en todas las pruebas** (tabla §2.2); ningún p es analítico salvo los exactos (signo, McNemar, binomial).
2. **Corrección múltiple** Holm y BH sobre todas las pruebas de cada familia; se reportan ambas. La conclusión del cuerpo (campos 3–7) es negativa con cualquier familia; la del encabezado solo sobrevive en UR1140, UR234 y UR1131.
3. **Unidad = quipu**, no cuerda: los tests de «campo 1 máximo» son binomiales por quipu; el 44/45 conjunto es descriptivo (4 quipus, no 45 unidades independientes).
4. **Tasa base honesta:** no 1/7, sino la frecuencia observada en grupos con 2 marcadoras del mismo tamaño y sin los focos (63,6 % para 9; 20 % para 8; 28,6 % para 10). La base de 9 cuerdas se estima con solo 11 grupos de 9 quipus, así que es una referencia ruidosa, no un parámetro preciso; aun así UR1140 y UR1131 sobreviven.
5. **Control de orientación fuera de muestra:** la regla congelada se aplicó sin cambios a UR1131 (0 % → 92 %) y UR234. Es la prueba de que el campo 1 máximo no es circular en los quipus que no se usaron para fijar la regla.
6. **Control de las 120 permutaciones:** el máximo sobre 120 se compara con su propia distribución nula. En la prueba conjunta (media de 3 correlaciones) el nulo tiene media 0,51 y p95 ≈ 0,78. Sin esta corrección, UR223–HP056 (r = 0,958) parecería un hallazgo; con ella, p = 0,41.
7. **Control de confusión color/lado:** en UR1136 el lado y el color dominante están perfectamente confundidos; en UR1140 no (ambos lados B). El corpus no muestra asociación general (Fisher p = 0,134). Por eso no se atribuye el efecto al color.
8. **Control de la explicación aburrida:** la primera cuerda es máxima en el 63,6 % de los grupos de 9 con 2 marcadoras; la ficha eleva eso a 93–100 % en 4 quipus y añade el par separador a 2 campos del extremo (77 %, p ≈ 10⁻⁵⁴). La estructura del par no se explica por «la primera es grande».
9. **Control de copias:** 0 totales de registro compartidos entre UR1140 y UR1136; ninguna identidad aditiva; UR234 tiene otra escala. Son formularios, no copias.
10. **Chequeo de la partición en grupos:** el grupo es el de espaciado (KFG), no una racha de color; en UR1140 OKR confirma 20 clusters de 9 cuerdas. Las rachas de color de 7 del informe previo cruzaban grupos y mezclaban dos órdenes.

---

## 5. Resultados negativos

- **Las dos marcadoras no son dos atributos:** misma torsión (47/47), misma unión (47/47), mismo color (44/47), misma dirección (41/47). Ningún test pareado sobrevive Holm. Son una marca duplicada, no un par de codificadores.
- **El lado del par no se asocia al total del registro** (UR1140 p = 0,056) ni, en general, al color dominante (Fisher p = 0,134). La confusión perfecta de UR1136 es local.
- **No hay permutación común para los campos 3–7:** los mejores r (0,89–0,97) no superan el máximo esperado por azar; la prueba conjunta no sobrevive Holm (0,079); la mejor permutación difiere entre quipus.
- **No hay sumas:** campo 1 ≠ suma de 2..7 (2/45); no hay diferencia constante entre campos; no hay totales de registro compartidos entre quipus. El «campo 1 = total» es una lectura, no una identidad aritmética.
- **UR1136, UR223 y HP056 no sobreviven la corrección conservadora** del «campo 1 máximo» (Holm 0,11; 0,25; 0,52). El efecto fuerte está en UR1140 y en las variantes UR234/UR1131.
- **UR1176 no confirma:** 6 grupos con el par en (1,9) pero 0 registros completos.
- **El Santa no es la misma ficha:** máximo en la posición 4 (85 %), mínimo en la 1, sin marcadores; perfil distinto.
- **Incahuasi no es la misma ficha:** 9 columnas sin marcadores, orden descendente solo en tendencia (−0,54), máximo físico en la columna 1 solo en 1/3 de los grupos, r = 0,20 con la ficha Nazca.
- **UR234 es una variante estructural, no una réplica:** comparte el formato (6 campos + par) y el encabezado, pero su escala es 20–40 veces mayor y su procedencia es desconocida.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| El par de marcadoras está a exactamente 2 campos de un extremo (77 %; p ≈ 10⁻⁵⁴) | **Bien apoyado** |
| Las dos marcadoras son gemelas (torsión, unión, color, dirección); no codifican dos atributos | **Bien apoyado** |
| El par separa secciones contiguas del quipu (rachas de lado; p = 0,001 / 0,028) | **Apoyado con datos** |
| El lado del par determina el orden de los campos (perfiles espejados, r = −0,926) | **Bien apoyado** (en UR1140) |
| El campo 1 canónico es el máximo en 44/45 registros de 4 quipus | **Apoyado con datos** (fuerte en UR1140; Holm solo en UR1140) |
| El formato 2 campos + par + cuerpo existe también con 6 y 8 campos (UR234, UR1131) | **Apoyado con datos** (UR1131 sobrevive Holm 0,0001; UR234 0,013) |
| La regla de orientación predice UR1131 (0 % → 92 %) sin reajuste | **Apoyado con datos** |
| Los campos 3–7 comparten un orden entre quipus | **No apoyado / negativo** (Holm 0,079; mejor permutación distinta por quipu) |
| Algún campo es suma de otros; campo 1 = total aditivo | **No apoyado / negativo** |
| «Encabezado de 2 campos + par + cuerpo» es un género de 6–8 campos | **Propuesto** (6 quipus; falta un séptimo independiente) |
| Campo 1 = total, campo 2 = residual, cuerpo = categorías | **Propuesto / especulativo** |
| El lado del par codifica moiety o tipo de registro | **Especulativo** |
| El Santa o el Incahuasi son el mismo formulario | **No apoyado** |

---

## 7. Para el coordinador

- **Las dos marcadoras no son dos atributos: son una marca duplicada.** Comparten torsión (47/47), unión (47/47), color (44/47) y dirección (41/47); ningún test pareado sobrevive Holm. Lo informativo no es la diferencia entre ellas sino **dónde está el par**.
- **El par está a exactamente 2 campos de un extremo** en 55/71 grupos de 9 (77 %; p ≈ 10⁻⁵⁴; Holm también para 8 y 10 cuerdas). Esa es la estructura real: **encabezado de 2 campos + par separador + cuerpo**. El «7 campos» no es una lista de 7 rubros, sino 2 + 5.
- **El lado del par marca secciones contiguas del quipu** (UR1140: 5 rachas, p = 0,0011; UR1136: 4 rachas, p = 0,028) y determina el orden de lectura (perfiles espejados, r = −0,926). En UR1136 el lado está confundido con el color (W vs G); en UR1140 no.
- **La ficha se generaliza a 6 y 8 campos:** aparecen **UR234** (10 grupos de 8 = 6 campos + par; 4/4 con campo 1 máximo; Berlín, procedencia desconocida) y **UR1131** (13 grupos de 10 = 8 campos + par; 11/12; Berlín/Pachacamac). En total, **7 quipus de 651** tienen el formato (6 utilizables; UR1176 está incompleto). Son variantes nuevas, no estaban en el informe previo.
- **UR1131 valida la regla de orientación fuera de muestra:** sin invertir, el máximo está en el campo 1 en **0/12**; con la regla congelada, en **11/12** (p = 0,0032). Es la mejor prueba de que la canonicalización no es un ajuste ad hoc.
- **Los campos 3–7 no se alinean.** Las 120 permutaciones dan r = 0,89–0,97, pero el máximo por par esperado por azar también ronda 0,9 (p corregidos 0,34–0,81); en la prueba conjunta el nulo tiene media 0,51 y p95 ≈ 0,78, el observado 0,838 deja p = 0,0197 y no sobrevive Holm (0,079); la mejor permutación cambia en cada quipu. El parecido es un artefacto de la libertad de permutar.
- **No hay sumas:** campo 1 ≠ suma de 2..7 (2/45), no hay diferencias constantes entre campos ni totales de registro compartidos entre UR1140 y UR1136. El «total» del campo 1 es semántico, no aritmético.
- **El género no es «n campos con la primera grande» a secas.** El Santa (6 campos, máximo en 4, mínimo en 1, sin marcadores) y el Incahuasi (9 columnas, descendente solo en tendencia, máximo físico en la columna 2 la mitad de las veces, r = 0,20 con Nazca) son **otros** formatos. El género Nazca es específico: 2 campos de encabezado, par separador, cuerpo plano.
- **Corrección conservadora:** del «campo 1 máximo» solo sobreviven Holm UR1140 (0,0017), UR234 (0,013) y UR1131 (0,0001); UR1136 (0,11), UR223 (0,25) y HP056 (0,52) no. La tasa base no es 1/7 sino 63,6 % en grupos de 9 con par; aun así el efecto es sólido en los tres primeros.
- **Próxima ronda:** (1) buscar un séptimo quipu independiente con el formato en 8/10 cuerdas para romper la dependencia de 6 objetos; (2) probar si el **lado** del par predice el color/sección en el corpus (no solo en UR1136); (3) leer UR234 con su escala en miles: ¿es otra unidad (bultos, población) o un total?; (4) verificar en OKR los clusters de 8/10 de UR234/UR1131; (5) no usar los campos 3–7 como plantilla semántica en futuros tests.

---

## 8. Archivos

- `ficha_nazca.csv` — ficha congelada: por posición (1–8), rol (encabezado/cuerpo), perfil z de cada quipu (UR1140, UR1136, UR223, HP056, UR234, UR1131), media de los 4 de 9 cuerdas, media cruda de UR1140 y fracción de máximos.
- `resumen_quipus.csv` — por quipu: formato, campos, n, máximo en campo 1, razón c1/c2, η², ρ̄, r con la ficha, museo y procedencia.
- `marcadoras.csv` — 47 registros con color, valor, torsión, unión, dirección y largo de las dos marcadoras.
- `alineamiento_120.csv` — mejores permutaciones y p corregidos por el máximo.
- `sumas.csv` — identidades aditivas y diferencias constantes.
- `barrido_corpus.csv` — los 7 quipus del formato en 8/9/10 cuerdas con p y correcciones.
- `genero.csv` — test de género contra la tasa base.
- `comparacion_formatos.csv` — perfiles de Nazca, Santa e Incahuasi.
- Scripts reproducibles: `lib.py`, `p1_marcadoras.py`, `p2_alineamiento.py`, `p3_sumas.py`, `p4_barrido.py`, `p5_genero.py`, `p6_control.py`, `p7_controles.py`, `ficha_final.py`, `explorar.py`, `explorar2.py`.
