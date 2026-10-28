# Etnohistoria andina y astronomía cultural: qué dicen las fuentes coloniales sobre los quipus y qué se puede verificar en el corpus

Equipo 05. Datos: `analisis/datos/cuerdas.csv` (651 quipus KFG; 640 con algún valor > 0), `quipus.csv`, `grupos.csv`. Todo es reproducible desde esta carpeta con semillas fijas. Unidad de análisis: el quipu. Cada resultado lleva su nulo, su p empírico y su corrección por multiplicidad (Holm y BH sobre el número total de pruebas de cada familia). Los resultados negativos están incluidos.

Para la parte del valle del Santa se leyó además, íntegro, el preprint abierto de FitzPatrick (2024) (OSF `sr8kw`, CC-BY). Es la primera vez que el proyecto tiene las cifras de la revisita de 1670 que las fichas no traían: tributarios por pachaca, la tabla de las 20 alineaciones, los conteos de grupos por quipu y la fórmula del p publicado.

Archivos: `calendario.py` (+ `calendario_parcial_*.csv`, `calendario_resultados.csv`, `calendario_holm_total.py/.csv`, `control_secuencia30.py/.csv`), `ur006.py`, `santa_grupos.py`, `santa_analisis.py` (+ `santa_*.csv`), `firmas_coloniales.py`, `firmas_post.py`, `firmas_resultados_final.csv`, `pares_mismo_contexto.py`, `extras.py`.

---

## 0. Resumen ejecutivo

| Tema | Resultado | Nivel |
|---|---|---|
| **Calendario (365/360/354-355/328/29-30/27-28/12-24)** en totales de quipu, de grupo, secuencias y conteos de cuerdas | 111 pruebas (96 + 15 conteos estructurales): 5 con p < 0,05 sin corregir (se esperan 5,6 por azar); **0 sobreviven a Holm y a BH**. Ningún quipu tiene 328, 354, 355, 360, 365 o 730 colgantes. | **Apoyado con datos (negativo)**: no hay exceso de números calendáricos |
| UR006 como calendario | El registro KFG/OKR reproduce **24 grupos grandes muy regulares** (20-22 colgantes cada uno), pero **no** reproduce "730 cuerdas en 24 grupos de 29-31" (578 cuerdas, solo 2 grupos con 29-31; 571 colgantes frente a 762 de Urton). Los totales por grupo (12-83) no son números calendáricos. | La regularidad: **bien apoyado** (estructura). Su lectura como calendario: **propuesto**, sin apoyo numérico en estos datos |
| **Santa: "alineación óptima" de mitades** | Es **trivial**: con el error definido por FitzPatrick, el mínimo posible es 3 y se alcanza en 62-77 % de los repartos de tamaños de pachaca al azar (94 % si el recuento de verso es aleatorio). Los p publicados son `(error+1)/134`: suponen un recuento de verso uniforme en 0..133 y no corrigen el "mejor de 20". | Ajuste publicado: **no excepcional**; interpretación de mitades (hanan/hurin): **especulativo** |
| Santa: suma de la primera cuerda = tributo | La suma de las primeras cuerdas de los 133 grupos da **369** (367 si se excluye el grupo con unión desconocida). De las 6 columnas posibles solo esa queda cerca de 367. Con un nulo sobre "objetivo arbitrario", p ≈ 0,005-0,018. Las cifras por mitad que cita FitzPatrick (381 + 86 = 467) **no suman 367 y no se reproducen** (KFG: 267-273 verso, 94-102 recto). | Coincidencia total: **apoyado débilmente** (post hoc); desglose por mitades: **no reproducible** |
| Firmas de las categorías coloniales | 55 pruebas. Sobreviven a Holm: segregación espacial de R/V (74 de 100 quipus evaluables frente a 5,6 esperados), segregación S/Z (6 de 9) y dos quipus con grupos de 8-12 colgantes **crecientes**. Ninguna firma decimal, de censo por edad decreciente, de archivo/depósito, de ganado o de calendario aparece por encima del azar tras corregir. | ver sección 4 |

---

## 1. Qué dicen las fuentes coloniales (compilado desde las fichas y el preprint de FitzPatrick)

Aviso: casi todo viene de resúmenes o de síntesis modernas; las citas de cronistas pasan por intermediarios. Los documentos coloniales mismos (revisita de 1670, Textos Andinos) no están en el repo.

| Categoría | Qué dicen las fuentes (y por quién) | Firma numérica que se deriva | Estado de evidencia en la fuente |
|---|---|---|---|
| Tributarios / censo | Revisita de 1670 de San Pedro de Corongo: 132 tributarios (130 nombrados) en 6 pachacas, "lo ponga por quipo" (Medrano y Urton 2018; FitzPatrick 2024). UR6: censo de contribuyentes y fuente del censo colonial de 1535 (Urton 2001, 2005). Primeras cuentas "menudas" invisibles para los jueces (Curatola y de la Puente 2013). | Grupos de seis cuerdas = individuos; la 1.ª cuerda = tributo; suma ≈ total de la revisita | apoyado con datos (coincidencia) / propuesto |
| Edad y sexo | Garcilaso: los objetos sin color "se ordenaban empezando por el más importante" (via FitzPatrick). Petición de Chuschi: cuenta subdividida "casados/viudas" (Durston y Urioste, hipótesis explícita). Hyland 2014: en un quipu pastoril de Uhle torsión S = hembra, Z = macho, separados espacialmente. | Grupos de 8-12 colgantes con clases ordenadas decrecientes; segregación espacial de categorías binarias | propuesto / n = 1 |
| Decimal administrativo | chunka/pachaka/waranqa/hunu; "pachaca" = ayllu en Corongo; UR6: ideal ≈ 3000 mit'ayuq (tresguarangas); UR28: 102 = pachaca de mita (Urton). | Totales de grupo/quipu = 10, 100, 1000, 10 000 o múltiplos; grupos de 10 colgantes | bien apoyado el sistema posicional; propuesto el uso administrativo |
| Depósitos / qollqa y cuentas duplicadas | Inkawasi: 34 quipus, ají/maní/frijol, pares atados con cuentas muy similares (Urton y Chu 2015). Garcilaso: ≥ 4 khipukamayuq por comunidad con las mismas cuentas; pares/tríos concordantes (Urton 2005; AS159/AS173, AS194/AS195, etc.). Quipus "resumen" (Medelius). | Dos quipus comparten secuencias largas de valores; un total = suma de otros del mismo archivo | apoyado (existencia), sin modelo nulo en la fuente |
| Mitas | Potosí: capitanes de mita con cordeles de colores por ayllu/pueblo/ganado/plata (Salazar-Soler; ~9000 mitayos 1573, > 14 000 1578). Mita de plaza y tambos del Cuzco: pueblo de origen, faltantes, tiempo (Amado Gonzales). Tripartición de la tasa y fracciones 2/9, 3/9, 4/9 (Medelius; Chirinos). | Razones exactas entre totales (1/3, 1/7); magnitudes de 10³-10⁴ | propuesto / exploratorio |
| Ganado | Tulpo (Huamachuco, s. XVII): ovejas madres/vacías/preñadas/paridas, carneros, corderos por edad; totales de 10 000-15 000 cabezas (Castro de Trelles). | Categorías binarias segregadas; totales 10⁴ | bien apoyado documentalmente |
| Tributo monetizado | Parinacocha: 240 pesos por semana en oro, 52 semanas = 12 480 pesos al año, 5 años = 62 400 (Glave). Pesos ensayados, fracciones monetizadas (Medelius). | Grupos de 52 colgantes; totales 12 480 / 62 400 | bien apoyado documentalmente |
| Genealogías, historias, nombres | Urton 1998 (alto contenido sintáctico/semántico en lecturas del s. XVI); Collata: 487 colgantes, 95 combinaciones de color/fibra/torsión, 75 % sin nudo terminal; ALLUKA, YAKAPAR (Hyland 2017, especulativo); Santa: 32 combinaciones de color frente a 30 nombres (Medrano y Urton). | Quipus casi sin nudos con alta diversidad de color/atributos | especulativo |
| Calendario | Nordenskiöld (especulativo, según Locke); UR6: 730 cuerdas en 24 conjuntos de 29-31 = 2 años de 365 días (Urton 2001, 2005). | Totales o conteos = 365, 360, 354-355, 328, 29-30, 27-28, 12/24 | propuesto |
| Ceques / mitades | 41 ceques y 328 huacas (Zuidema, citado por FitzPatrick); mitades hanan/hurin, Collana-Payan-Cayao; Tupicocha: mitades Yacapar/Yañac (Salomon, Hyland et al. 2021). | 328 colgantes/totales; 41 grupos; binario R/V segregado | propuesto |
| Judicial / confesión / hucha | Spalding: normas y dictámenes en quipus; quipus confesionales (Harrison, Charles); partida doble ligada al registro de deudas morales (Urton). | Sin firma numérica directa (el pareado de cuentas se prueba en 4.3) | propuesto / especulativo |

---

## 2. Tarea 1: la hipótesis calendárica

### 2.1 Diseño

- **Objetivos exactos (14)**: 27, 28, 29, 30 (meses sidéreo y sinódico), 328 (Zuidema), 354, 355 (12 lunas), 360, 365, y sus dobles 656, 708, 710, 720, 730. **Ventanas ±2 (4)**: 365, 360, 354-355 (355 ± 2), 328.
- **Medidas (5 familias)**: (1) total del quipu con todas las cuerdas; (2) total de colgantes; (3) total de cada grupo (con subsidiarias); (4) total de cada grupo (solo colgantes); (5) sumas de 3 a 30 colgantes consecutivos. Más: nº de grupos = 12 o 24 y nº de cuerdas por grupo = 27-30 (comparación con vecinos, cola de Poisson), y conteos estructurales (nº de colgantes o cuerdas = 328, 360, 365, 354, 355, 730; nº de grupos = 41, 12, 24; vecinos ± 5).
- **Estadístico**: nº de quipus con al menos un acierto.
- **Nulos**: totales de quipu: *bootstrap* de valores dentro del quipu y del estrato (colgantes/subsidiarias), que conserva la distribución de valores y la estructura pero cambia la suma (barajar sin reemplazo dejaría el total invariante). Grupos y secuencias: permutación de valores dentro del quipu y del estrato (conserva valores y tamaños de grupo, rompe posición). 4000 simulaciones por familia, semilla fija.
- **Multiplicidad**: 90 pruebas de las 5 familias (18 objetivos × 5) + 6 (grupos 12/24, cuerdas por grupo 27-30) + 15 conteos = **111 pruebas**, todas contadas.

### 2.2 Resultados

- Con 4000 simulaciones: **5 de 111 pruebas con p < 0,05 sin corregir (esperado 5,6); Holm < 0,05: 0; BH < 0,05: 0.** (`calendario_holm_total.csv`).
- La mejor, "suma de colgantes consecutivos = 30" (308 quipus frente a 285 esperados, p = 0,001, Holm 0,11), **no es calendárica**: el control `control_secuencia30.py` calcula el mismo exceso para T = 15 a 45. T = 36 tiene mayor exceso (28,7) que T = 30 (22,4); el exceso medio de los múltiplos de 10 (15,8) es el doble que el del resto (7,9). Es redondez decimal más correlación local entre colgantes vecinos, no un calendario.
- Totales de quipu: 354 → UR170 (cuatro cuerdas de valor 70 más valores pequeños); 708 → UR239; 365 solo en colgantes → UR048. Cada uno es 1 quipu frente a 0,1-0,4 esperados (p entre 0,13 y 0,27 sin corregir). No hay ningún total de 328, 355, 360, 656, 710, 720 ni 730.
- Totales de grupo: 328 (AS199 g0, UR197 g6, UR062 g1...), 354 (UR069 g1, UR149 g7), 355 (AS122, UR212, UR258), 360 (MM001 g1, QU018 g3), 365 (QU014 g41, solo colgantes), 730 (UR1109 g32, UR274A g3). Todos dentro de lo esperado por azar (el menor p sin corregir es 0,026: ventana 328 ± 2 en grupos de colgantes, 19 quipus frente a 12,1; el resto, p ≥ 0,12).
- Nº de grupos: 12 en 17 quipus (vecinos: 15,8; p = 0,42); 24 en 7 (vecinos: 5,0; p = 0,24). Nº de cuerdas por grupo 27-30: sin exceso. **Ningún quipu** tiene exactamente 328, 354, 355, 360, 365 o 730 colgantes, ni 41 grupos.

**Conclusión (apoyado con datos, resultado negativo):** en el corpus de 640 quipus no hay más números "calendáricos" de los que produce el azar con la misma distribución de valores y estructura. Esto no refuta que UR006 sea un calendario (n = 1), pero muestra que la hipótesis no generaliza como regla del corpus y que, al contar todos los números mágicos probados, los hallazgos aislados son los esperados.

### 2.3 UR006 (`ur006.py`)

- KFG/OKR (KH0242): 874 cuerdas, **571 colgantes** (Urton 2005: 762), 303 subsidiarias, suma de valores 3037 (Urton: 3005 en 2001 y 2962 corregido). Discrepancia de versión no resuelta.
- Hay **24 grupos grandes** de 20-22 colgantes (20, 21, 21, 21, 21, 21, 21, 21, 22, 22, 21, 22, ...) intercalados con colgantes-lazo de 10 subsidiarias. Esto coincide con "24 conjuntos". Pero con subsidiarias esos grupos tienen 21-31 cuerdas (media 24,1; total 578); solo 2 caen en 29-31. Con los lazos el total es 549 colgantes; ninguna combinación da 730.
- Los totales por grupo grande son 12-83 (media 48), sin relación visible con 29-31 o con meses.
- **Regularidad**: racha de grupos consecutivos con nº de colgantes en rango ≤ 2: UR006 = 24, la 2.ª del corpus tras UR231 (76 grupos de colgantes regulares) y por delante de UR1057 (21), UR1166 (20), UR229 (18), AS050 (17); 2 quipus de 651 alcanzan ≥ 24. La regularidad de UR006 es atípica pero no única: es una propiedad de quipus de banda de color, no una prueba de calendario.

**Nivel**: estructura (24 grupos regulares): bien apoyado. Lectura calendárica de UR006: propuesto. "730 cuerdas en grupos de 29-31": **no reproducible con KFG/OKR**.

---

## 3. Tarea 2: valle del Santa

### 3.1 Los seis quipus y su reconstrucción (`santa_grupos.py`)

UR087-UR092 = KH0323-KH0328 (Museo Temple Radicati). Grupos de seis cuerdas (bloques de 6 colgantes consecutivos del mismo color; se excluyen las cuerdas sueltas, siguiendo el criterio de Medrano y Urton descrito por FitzPatrick: p7, p14 ... de UR087; p73 y p140 de UR089; p31, p38 y p63-p66 de UR090):

| Quipu | grupos (KFG) | publicado | uniones de la 1.ª cuerda |
|---|---|---|---|
| KH0323 | 48 | 48 | R × 48 |
| KH0324 | 9 | 9 | V × 9 |
| KH0325 | 34 | 34 | V × 34 |
| KH0326 | 17 | 17 | V × 11, R × 6 (publicado: V × 12, R × 5) |
| KH0327 | 15 | 15 | V × 15 |
| KH0328 | 10 | 10 | R × 9, U × 1 (publicado: R × 10) |
| **Total** | **133** | **133** | **R 63, V 69, U 1** (publicado R 63, V 70) |

Los conteos de grupos coinciden exactamente. La reconstrucción difiere en dos casos de la lectura publicada de la unión de la 1.ª cuerda: un grupo de KH0326 (p91, R en KFG; V en la lectura publicada) y un grupo de KH0328 (p7, unión desconocida en KFG). Sobre todas las cuerdas: 406 R y 423 V (49,0 % / 51,0 %), idéntico a Contreras (2026); y como allí, esto relee el mismo campo de la misma tradición de registro (no es verificación independiente).

### 3.2 Suma de la primera cuerda frente al tributo de 367 pesos

Sumas por posición dentro del grupo (cuerdas 1 a 6): **369**, 1507, 439, 4871, 615, 616. Con el grupo de unión desconocida excluido, la columna 1 da **367**, el total de la revisita (367 pesos 1/4 real 1 cuartillo). La coincidencia es real pero hay que descontar la elección post hoc de la columna y del objetivo: si el tributo total fuera un número arbitrario entre 100 y 5000 (uniforme o log-uniforme), la probabilidad de que alguna de las 6 columnas quede a ≤ 2 de él es 0,5-1,8 %. Con una prior más ancha en torno a magnitudes de cientos, ≈ 1,8 %. Además, la 1.ª cuerda es la columna de menor suma del grupo (las otras cinco suman 1,2 a 13 veces más), de modo que "la columna que más se acerca a 367" tiene una ventaja estructural.

Las cifras por mitad de FitzPatrick (verso 381, recto 86) **no suman 367** (suman 467) y su nota 14 reconoce incertidumbre. KFG da, con la lectura propia, verso 267 y recto 100 (+ 2 de unión desconocida) = 369, o 273/94 si se asigna el grupo discrepante de KH0326 como verso. El contraste de 5,45 contra 1,4 pesos por tributario que construye sobre esas cifras **no es reproducible** con este corpus; además la diferencia de promedio se explica entre quipus (KH0323 y KH0328 tienen valores de 1.ª cuerda de 1,2 y 1,1 de media; KH0324 de 8,9), no dentro de una mitad.

El número de grupos (133) y de tributarios nombrados (130) o declarados (132) es un acuerdo de ±1 a ±3 en un recuento sin objetivo independiente: no hay modo de asignarle una probabilidad sin una prior sobre cuántos tributarios habría en una comunidad con 6 quipus.

### 3.3 Enumeración de alineaciones y ajuste (`santa_analisis.py`)

Tamaños de pachaca de la revisita (FitzPatrick, de Zevallos 1991): Namus 18, Corongo 23, Cuyuchin 9, Cusca 7, Guauyan 41, Ucore 32 (130 nombres). Hay 20 formas de elegir las tres pachacas del verso; error = |S − 70| + |(130 − S) − 63|. Se reproduce exactamente la tabla 3 de FitzPatrick.

- **Enumeración completa**: errores 3 (Namus-Cuyuchin-Guauyan, la propuesta de FitzPatrick), 5 (dos alineaciones, una es la de Medrano y Urton), 9 (tres), 13, 19, 23 (tres), 27 (dos), ... hasta 69. **Alineaciones con un ajuste igual o mejor que el de Medrano y Urton (error 5): 3 de 20 (15 %). Igual o mejor que el de FitzPatrick (error 3): 1 de 20 (5 %).** Como mera enumeración eso es lo que hay, pero no es un p-valor del "descubrimiento":
- **Los p publicados** son exactamente `(error + 1)/134` (verificado en las 20 filas): equivalen a suponer que el recuento de grupos verso es uniforme en 0..133, no corrige por haber elegido el mejor de 20 y trata 133 grupos como 133 decisiones independientes, cuando los atributos R/V se asignan por quipus enteros (5 de 6 quipus son puros): hay ≈ 6-7 decisiones independientes.
- **Nulo a (recuento verso aleatorio)**: el mejor error entre las 20 alineaciones es ≤ 3 con probabilidad 0,94 si V ~ Binomial(133, 0,5) y 0,36 si V es uniforme en 0..133 (0,70 si se restringe a V entre 45 y 90).
- **Nulo b (quipus enteros)**: asignando cada quipu entero a R o V (KH0326 con 12V/5R fijo), de 32 combinaciones 15 alcanzan error ≤ 3 y 17 alcanzan ≤ 5.
- **Nulo c (tamaños de pachaca al azar, V = 70 fijo)**: composiciones uniformes de 130 en 6 partes: P(mejor error ≤ 3) = 0,62; ≤ 5: 0,71. Con Dirichlet(2): 0,77 y 0,85. Combinado con V binomial: 0,60.
- Como 3 es el piso del error (cualquier S entre 67 y 70 daría 3), el "óptimo" de FitzPatrick es esencialmente el mejor valor alcanzable con 20 sumas de triples, y solo hay un triple (S = 68) en [67, 70].

**Conclusión (apoyado con datos):** el ajuste publicado **no es excepcional**: se alcanza o se mejora por azar con probabilidad 36-94 % según el nulo (0,36 con V uniforme, 0,47 con quipus enteros, 0,60-0,77 con tamaños aleatorios, 0,94 con V binomial). Que Medrano y Urton y FitzPatrick propongan alineaciones distintas con ajustes casi idénticos es la consecuencia esperada. Los datos no distinguen entre ellas ni respaldan una asignación hanan/hurin; el patrón R/V por sí mismo (quipus puros, Contreras) es real pero está confundido con la estructura por quipu. **La lectura de mitades (verso = hanan, recto = hurin; jerarquía Collana-Payan-Cayao) es especulativa.**

### 3.4 Otros controles

- **Colores distintos** en la 1.ª cuerda de los 133 grupos: 33 con nuestra normalización (Medrano y Urton: 32), frente a 30 nombres propios distintos. Es un número fijado por la seriación (KH0323 solo tiene 8 colores por repetición cuatro veces del mismo patrón, KH0328 repite 5 colores): el acuerdo 32 ≈ 30 no tiene nulo y FitzPatrick mismo ve que se rompe por mitades (27 colores/23 nombres en verso; 14/25 en recto).
- **Quipus tipo Santa en el corpus** (`santa_bloques6_corpus.csv`): bloques de 6 colgantes del mismo color: AS069 (92 bloques, todas con unión desconocida), UR087 (36), UR089 (31), UR091 (15), UR090 (13), UR1146 (13), UR003 (10), UR092 (10), HP034 (9), UR234 (9). Hay candidatos fuera del Santa con estructura de seisenas (UR1146, UR003, HP034, UR234, AS069) para una réplica ciega. La tendencia general "rachas de color de 6" es marginal en el corpus (33 quipus con ≥ 3 rachas de 6 frente a 24,5 en vecinos; p = 0,058 sin corregir).
- **Procedencia**: los seis son de la misma tumba, según la literatura citada por FitzPatrick; los fechados por radiocarbono sugieren (no establecen) que son anteriores a 1670 (Ghezzi et al. 2023, citado por FitzPatrick). Hyland sostiene que no corresponden a la revisita. Esto afecta cualquier "emparejamiento".

---

## 4. Tarea 3: firmas numéricas de las categorías coloniales contra el corpus (`firmas_coloniales.py`, `firmas_post.py`)

55 pruebas (unidad: quipu; los nulos son los mismos de la sección 2: bootstrap para totales, permutación dentro de grupo para estructuras de orden, vecinos con Poisson para conteos, permutación de etiquetas para segregación). Holm y BH sobre las 55. Donde el p empírico estaba en su piso (1/501) se reemplazó por la cola exacta (Poisson o binomial con tasa nula ≤ 5 %) para que Holm sea decidible.

| Categoría | Firma | Quipus que la muestran | Nulo | p (ajustado) | Veredicto |
|---|---|---|---|---|---|
| Decimal admin | Total de quipu = 10, 100, 1000, 10 000; ≈ ± 2 %; múltiplo de 100 o 1000 (colgantes y total) | = 10: 2; = 100: 1; = 1000 (colgantes): 1; ≈ 1000: 3-5; múltiplo de 100: 7-8 | 2,0 / 0,7 / 0,2 / 4-5 / 6,7-6,8 | todas p ≥ 0,17; Holm = 1 | **sin señal** |
| Decimal admin | Total de grupo = 1000 | 6 quipus | 3,4 | p = 0,09; Holm = 1 | sin señal |
| Decimal admin | Quipus con ≥ 3 grupos de exactamente 10 colgantes | 17 | 19,8 (vecinos 7-13) | p = 0,77 | **sin señal** (pico de tamaño en 3-6, no en 10) |
| Censo por edad/sexo | Grupos de 8-12 colgantes con clases **decrecientes** | **0** | 0,04 | p = 1 | negativo |
| Censo por edad/sexo | Grupos de ≥ 5 colgantes decrecientes / crecientes | 5 / 8 | 2,8 / 2,8 | 0,16 / 0,009 (Holm 0,47) | sin señal; prueba de signos dec/inc: 5 vs 8, p = 0,87 |
| Censo por edad/sexo | Grupos de 8-12 colgantes **crecientes** | **2**: HP021 (1, 1, 1, 6, 26, 36, 187, 3236), MM006_AN001 (0, 35, 54, 65, 109, ..., 536) | 0,04 | p = 8·10⁻⁴, Holm 0,042, BH 0,015 | señal débil y exploratoria; son series ordenadas por magnitud que terminan en un valor muy grande (¿total?), no censos decrecientes |
| Depósitos / cuentas duplicadas | Pares de quipus con 6 colgantes consecutivos idénticos (no triviales) | 41 pares | 32,1 (máx. nulo 54) | p = 0,11 | sin exceso global; control positivo: AS159-AS173 recuperado, AS194-AS195 no |
| Depósitos / cuentas duplicadas | De esos 41 pares, los que comparten procedencia | 5 (AS125-UR247, AS159-AS173, JC009-JC013, KH0033-UR044, UR066-UR067) | 1,4 | p = 0,014 (Holm 0,71) | exploratorio, a favor de duplicación dentro de un mismo archivo |
| Depósitos / cuentas duplicadas | Total idéntico (≥ 20) en el mismo contexto; total = suma de otros dos (resumen) | 3; 23 | 2,1; 24,4 | 0,34; 0,62 | sin señal (28 contextos con ≥ 3 quipus; el campo es procedencia y no origen) |
| Mitas | Razón exacta de totales 3 o 7 entre quipus del mismo contexto | 6 | 3,0 | p = 0,086 | sin señal |
| Ganado / categorías binarias | **Segregación espacial de R/V** (Wald-Wolfowitz p < 0,05 por quipu) | **74 de 100 quipus evaluables** | 5,6 | p ≈ 10⁻⁷³ (Holm 5·10⁻⁷²) | **fuerte** (ver explicación aburrida abajo) |
| Ganado / categorías binarias | Segregación de torsión S/Z (sexo, tipo Uhle) | 6 de 9: HP045, UR051, UR052, UR087, UR1123, UR1087 | 0,6 | p = 1,2·10⁻⁶ (Holm 6·10⁻⁵) | señal débil: pocos quipus, y en 3 de 6 (HP045, UR087, UR1123) la categoría minoritaria tiene solo 4-10 cuerdas |
| Genealogías / nombres | Entropía de color de quipus con ≥ 60 % de colgantes sin nudo frente al resto (40 de 435 quipus) | mediana 2,04 vs 2,31 bits (dif. −0,27) | permutación estratificada por tamaño | p = 0,24 | **negativo**: los quipus casi sin nudos no tienen más diversidad de color |
| Calendario / ceques | Nº exacto de colgantes o cuerdas = 328, 360, 365, 354, 355, 730; 41 grupos | 0 en todos | 0-1,8 | 1 | **negativo** |
| Calendario / ceques | 12 y 24 grupos | 17; 7 | 18,1; 4,8 | 0,63; 0,21 | negativo |
| Nivel individual | ≥ 3 rachas de color de exactamente 6 colgantes (vs 4, 5, 7, 8) | 33 | 24,5 | p = 0,058 | sin señal tras corregir |
| Tributo monetizado | Totales de 12 480 o 62 400 (Parinacocha); grupos de 52 colgantes (semanas) | 0; 0; 1 (UR090, accidental) | 0,5 | p = 0,39 | negativo (`extras.py`) |

**Explicación aburrida de la señal de R/V.** El 74 % de los quipus con ambas uniones presenta rachas largas de la misma unión. Lo natural es que el sentido del nudo de amarre dependa de quién y cuándo ató las cuerdas, no de una categoría codificada: la segregación aparece en cualquier quipu atado por secciones. Esto no apoya ni refuta las mitades del Santa; indica que, para tomar R/V como signo binario (Urton, FitzPatrick, Clindaniel), habría que mostrar que las rachas coinciden con otra variable independiente (color, posición, valor) y no con el ritmo de manufactura.

**Qué firmas aparecen y en qué quipus.** (1) Segregación R/V: 74 quipus, entre ellos los seis del Santa (puros o casi). (2) Series ordenadas crecientes de 8-12 colgantes: HP021 y MM006_AN001. (3) Pares que comparten secuencias y procedencia: AS159/AS173 (control positivo de Urton 2005), JC009/JC013 (Inkawasi), UR066/UR067 (Huaquerones), AS125/UR247 (Pachacamac), KH0033/UR044 (La Puntilla). (4) Segregación S/Z: HP045, UR051, UR052, UR087, UR1123, UR1087. Ninguna firma de censo decimal, de edad decreciente, de depósitos por totales, de mitas, de tributo monetizado o de calendario.

---

## 5. Controles, sesgos y límites

- **Datos**: varios quipus de Urton 2005 (AS114, AS123, AS116, AS150) no están en el corpus KFG de 651 quipus, por lo que los controles positivos de cuentas duplicadas solo cubren AS159/AS173 y AS194/AS195 (este último no detectado con 6-gramas; sus valores difieren por una cuerda ausente).
- KFG/OKR y las publicaciones difieren en UR006 (571 vs 762 colgantes; total 3037 vs 2962) y en 2 grupos del Santa (sección 3.1). No sabemos cuál es la lectura correcta de la cuerda; esto es un margen de error para todas las coincidencias de ± 2-3 unidades.
- **Procedencia**: el campo `procedencia` se usó solo para agrupar "contexto de archivo", sin inferir origen; los museos son de coleccionismo (Contreras 2026).
- **Potencia**: muchas pruebas de totales tienen 0-3 aciertos; un nulo con media 0,1-0,4 y 1 acierto produce p ≈ 0,1-0,3. No se puede detectar un calendario que solo tenga 1-2 quipus del corpus; lo que se descarta es una regla general.
- **El nulo de bootstrap para totales** supone cuerdas independientes dentro de cada estrato, mientras que los quipus reales tienen sumas internas (relaciones de Ascher): los totales reales son más variables o más estructurados que los simulados. Con más estructura, el nulo subestima algunos aciertos; para los 111 números calendáricos, el resultado negativo es robusto a esto.
- No se probaron aquí 'etiquetas de tres términos' de UR006 ni las sumas por color de Ascher; ver sección 6.

---

## 6. Qué investigar a continuación

1. **Conseguir el documento de 1670** (Zevallos Quiñones 1991, Etnohistoria del Área Viru-Santa) y el apéndice de Urton (2017): con los nombres y su orden, comprobar si el orden de los grupos de seis por quipu sigue el orden del padrón (hipótesis falsable que los autores no han probado) y reconstruir las sumas por pachaca, no solo por mitad.
2. **Réplica ciega fuera del Santa**: UR1146, UR003, HP034, UR234, AS069 y KH0055 (FitzPatrick) tienen estructura de seisenas; comprobar que la primera cuerda es la "pequeña" y que las otras 5 posiciones siguen reglas numéricas fijas (Urton 2017: 227) con un nulo de permutación de posiciones.
3. **R/V como firma de manufactura o de categoría**: modelar la unión (R/V) en función de color, longitud, torsión, posición en el cordón principal y número de nudos; un signo semántico debería predecirse por la variable social, uno de manufactura por el orden de atado.
4. **UR231** (76 grupos regulares) y UR1057 (21) como segundos candidatos de "calendario por conjuntos"; revisar contra OKR el recuento de colgantes y la versión Urton (762) para entender la discrepancia.
5. **Duplicados**: ampliar la búsqueda de cuentas concordantes con alineación aproximada (no solo 6-gramas exactos) y modelo nulo, dentro de procedencias de excavación (Inkawasi, Puruchuco, Laguna de los Cóndores).
6. **Corpus textual**: usar los anexos de Curatola y de la Puente (2013) y Textos Andinos como casos cuantitativos "texto-quipu" (Tulpo, Parinacocha, Lucanas) para fijar firmas de ganado/mita a priori, antes de mirarlas en el corpus.
