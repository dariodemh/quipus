# lit_3 — Extracción y comprobación de afirmaciones sobre el significado y la estructura de los quipus

**Autor:** equipo lit_3 · **Fecha:** 17 de octubre de 2026 · **Semilla:** 20261017
**Datos:** `analisis/datos/{cuerdas,quipus,grupos}.csv` (651 quipus, 57 818 cuerdas) y, solo para un control, `data/external/open-khipu-repository/data/khipu.db`.
**Scripts:** `comun.py`, `t1_ur028.py`, `t2_ur267a.py`, `t3_santa.py`, `t4_direccion_nudos.py`, `t5_torsion.py`, `t6_metadatos.py`, `t7_color_okr.py`.
**Entregable de datos:** `afirmaciones.csv` (34 afirmaciones de 12 fichas).

---

## 1. Pregunta

¿Qué afirmaciones concretas sobre el **significado** o la **estructura** de los quipus hacen las fichas de literatura, y cuáles se sostienen al contrastarlas con los datos del repo?

No intento descifrar quipus. Intento separar tres cosas que la literatura suele mezclar:

1. **Regularidades estructurales** (cuántos cordeles, qué colores, qué dirección de nudo, qué sumas).
2. **Interpretaciones semánticas** (qué *significa* un color, una mitad, un 102).
3. **Predicciones falsables** que se derivan de esas interpretaciones.

La unidad de análisis es el **quipu**, no la cuerda (regla 1 del brief). Cuando he analizado cuerdas, he usado permutaciones o bootstrap **dentro de / entre quipus** y he reportado el efecto de diseño.

---

## 2. Método

### 2.1 Extracción

Leí las 12 fichas asignadas y extraje 34 afirmaciones con un criterio explícito: que mencionen **quipus identificables, cifras, patrones de color, sumas o alineaciones con documentos**. Cada fila de `afirmaciones.csv` lleva fuente, afirmación, quipus implicados, cifras, cómo comprobarla y si es comprobable con los datos del repo.

Resultado de la criba:

| Comprobable | n | Ejemplos |
|---|---:|---|
| **sí** | 10 | 133 grupos del Santa; dirección S/Z en Inkawasi; UR28; UR267A; KH#### |
| **parcial** | 11 | torsión 97% S; 95 combinaciones de Collata; tributo del Santa; “un tercio no decimal” |
| **no** | 13 | Collata (no está en el corpus); tablas de Mangas/Casta; transcripciones coloniales; tintes |

Más de un tercio de las afirmaciones (13/34) **no es contrastable con este repo** por una razón trivial pero importante: los objetos estudiados (Collata, Mangas, Ayacucho, Casta, los *paper khipus*) **no están** en KFG/OKR. Lo comprobé buscando “Collata”, “Mangas”, “Casta”, “Corongo”, “Ayacucho” y “1932” en `quipus.csv`: cero coincidencias.

### 2.2 Identificación de los casos

- **Seis quipus del valle del Santa:** `UR087`–`UR092`, museo Temple Radicati, procedencia “Santa”, OKR `KH0323`–`KH0328`. Son los únicos seis quipus con procedencia Santa en el corpus y reproducen exactamente los 133 grupos de seis cordeles que reporta Medrano & Urton (2018). La identificación es, por tanto, muy probable, pero es una **suposición** (la ficha no da los IDs).
- **UR28** y **UR267A/UR255** están presentes y completos.
- **Inkawasi:** `JC001`–`JC023` + `UR255`–`UR280` = 52 quipus en la literatura; en KFG hay 48 con datos (23 JC + 25 UR), suficiente para replicar.

### 2.3 Controles

- **Nulo explícito** en cada prueba que lo admite: permutación del tercer valor (UR267A), permutación de etiquetas respetando el número de bloques por quipu (Santa), binomial y bootstrap por quipu (dirección y torsión).
- **Corrección múltiple:** BH-FDR sobre la familia de 7 pruebas confirmatorias (tabla en §5).
- **Valores 0 sin nudos = ausentes** (regla 6), nunca ceros reales.
- **Escepticismo:** antes de aceptar una interpretación, busqué la explicación aburrida (confusión por quipu, tamaño, selección post hoc, diferencia de codificación).

---

## 3. Resultados

### T1. UR28: la aritmética de las tres sumas = 102 (Urton 2019)

**Afirmación:** el cordel #1 suma 102; el grupo 2 (p2–p4 + subsidiarios) suma 102; las seis agrupaciones del grupo 3 (p5–p74) también suman 102, con un error de registro de 2 unidades; mitad AB / mitad MB.

**Resultado (determinista, sin test):**

| Unidad | Suma | Composición |
|---|---:|---|
| p1 | **102** | AB 102 |
| p2–p4 + subsidiarias | **102** | AB 54 + MB 48 |
| p5–p76 + subsidiarias (grupos 2,3,5,7) | **104** | AB 52 + MB 48 + KB 4 |
| Desvío | **+2** | exactamente el error que reporta Urton |

- El KFG registra **76 colgantes + 15 subsidiarias = 91 filas**, no 74 cordeles: dos colgantes (`p35`, `p56`) no tienen color ni nudos (valor 0 = ausente). Ajustando por esos dos ausentes, los “74 cordeles” del artículo son consistentes.
- **Control:** busqué todas las combinaciones de grupos del KFG que suman 102. Salen 8, pero **todas incluyen los grupos vacíos 4 y/o 6**; entre grupos no vacíos solo `{0}` y `{1}` dan 102, y `{2,3,5,7}` da 104. La coincidencia no es trivial.
- **Negativo/limitación:** el 102 aparece tres veces, pero eso **no demuestra** que sea una *pachaca* ni que AB sea *hanan*. La parte aritmética se sostiene; la semántica es interpretación.

**Nivel:** aritmética interna **demostrada** (reproducible); lectura como pachaca/mitades **propuesta**.

---

### T2. UR267A: ¿“blanco = suma, marrón = resta, moteado = resultado”? (Clindaniel 2019, cap. 4)

**Afirmación:** en UR267A, W = suma/acreditación, AB = resta/débito, AB:MB = resultado; el ejemplo es 106 − 15 = 91. En UR255 los roles se invierten.

**Resultado:** el quipu está organizado en **25 tríos completos** (más 4 grupos de 1–4 cordeles). La relación `primer − segundo = tercero` se cumple exactamente en **15 de 25** tríos (60%; 15 de 23 si se excluyen los terceros ausentes, 65%). Una permutación que rompe el emparejamiento del tercer valor da **p = 0,00005** (B = 20 000). El trío citado se reproduce exactamente: **106 (W) − 15 (AB) = 91 (AB:MB)**.

Pero el **color** no predice el acierto, y de hecho lo contradice:

| Color del tercer cordel | n | tríos exactos |
|---|---:|---:|
| AB (marrón claro sólido) | 11 | **9 (82%)** |
| W (blanco) | 5 | 4 (80%) |
| **AB:MB (moteado)** | 7 | **2 (29%)** |

El color que la hipótesis designa como “resultado” (moteado) es el **peor** predictor. Los tríos que fallan no son aleatorios: varios tienen terceros ausentes (0) o valores desplazados (p. ej. 161−15=146 vs 140; 114−15=99 vs 84).

**UR255:** su estructura no son tríos (alterna grupos de 1–4 cordeles con cuerdas vacías). Al aplicar la misma regla, solo 7/15 coinciden y la permutación da p = 1,0: **no hay evidencia de la “inversión” de roles** con este diseño.

**Nivel:** la **aritmética** de UR267A está **apoyada con datos** (p < 10⁻⁴), pero es un caso elegido a posteriori por el propio autor; la **semántica del color** queda **no apoyada** y en parte contradicha.

---

### T3. Los seis quipus del Santa: 133 grupos, mitades y verso/recto (Medrano & Urton 2018; FitzPatrick 2024)

**A) 133 grupos de seis cordeles.** Reconstruí bloques de **6 colgantes consecutivos** dentro de cada grupo del KFG:

- **133 bloques exactos**, que cubren 798 de los 824 colgantes (quedan 26 colgantes en restos de 1–4).
- Bloques por quipu: UR087 48, UR088 9, UR089 34, UR090 17, UR091 15, UR092 10.
- Que un procedimiento definido *sin mirar la cifra* produzca exactamente 133 es un **ajuste estructural fuerte**: la afirmación de M&U se sostiene.

**B) La suma de los primeros cordeles = tributo.** La suma es **398** (por quipu: 57, 80, 101, 113, 36, 11). Probé los seis *offsets* posibles dentro del bloque: 398, 1 858, 501, 4 438, 615 y 690. **Ninguno da 132 ni 133**, los números de tributarios/bloques del artículo. Sin la *revisita* de 1670 (no está en el repo) no se puede decidir si 398 es el tributo evaluado en otra unidad; la afirmación queda **parcial**. Lo que sí se puede decir: **no es un simple conteo de tributarios**.

**C) Verso/recto como binario.** El primer cordel de los 133 bloques es **V en 69, R en 63, U en 1**: equilibrio casi perfecto (binomial p = 0,66). A primera vista, FitzPatrick tiene razón: hay un signo binario.

Pero el control por quipu cambia la lectura:

| khipu | R | V | U |
|---|---:|---:|---:|
| UR087 | 48 | 0 | 0 |
| UR088 | 0 | 9 | 0 |
| UR089 | 0 | 34 | 0 |
| UR090 | 6 | 11 | 0 |
| UR091 | 0 | 15 | 0 |
| UR092 | 9 | 0 | 1 |

**Solo 1 de 6 quipus tiene ambos signos.** Un nulo que preserva el número de bloques por quipu y asigna V/R con probabilidad global 0,52 da **p = 0,00005** para tanta concentración (B = 20 000); χ² quipu×unión = 128,7, gl = 10, p = 8,5 × 10⁻²³, V de Cramér = 0,70. Es decir: **el “signo binario” es un atributo de quipu (o de ayllu), no un marcador por tributario dentro de cada quipu**. La lectura de FitzPatrick de V/R como marcado/no marcado *dentro* de la población no se sigue de estos datos; la de M&U de “mitades” tampoco, porque los seis quipus no se parten 3/3 (2 R, 3 V, 1 mixto).

**D) Magnitud y confusión.** A nivel de bloque, los bloques V tienen valores mucho mayores que los R (total mediano 90 vs 18; Mann-Whitney p = 6,6 × 10⁻⁹). La explicación aburrida es que **V/R está confundido con el quipu**: UR088 y UR089 son V y tienen valores grandes; UR087 y UR092 son R y tienen valores pequeños. En el único quipu mixto, UR090, la diferencia desaparece (total mediano 111 vs 100; p = 0,88) y en el primer cordel incluso se invierte (V 5 vs R 7,5; p = 0,044). **No hay evidencia de que V implique mayor magnitud dentro de un mismo quipu.**

**E) Alineación óptima de mitades (FitzPatrick).** No replicable: requiere los valores del censo de 1670, que no están en el repo. Enumerar 6! = 720 alineaciones sin la función objetivo del documento no tiene sentido. Queda **parcial**.

**Nivel:** 133 grupos, **apoyado con datos**; binario V/R, **apoyado** como rasgo de quipu; interpretación como mitades/marcado, **propuesta**; coincidencia con el tributo, **no verificable**.

---

### T4. Dirección de los nudos S/Z (Clindaniel 2019, cap. 3)

**Afirmación:** en Inkawasi dominan los Z (6 209 Z vs 1 704 S); los simples son 1 619 Z vs 19 S (p < 0,0001); los largos/en ocho son más S (402 S vs 835 Z); si un cordel tiene largo-S, sus simples son todos Z (1 212 vs 0); el patrón se replica en Pachacamac y Puruchuco, salvo Armatambo.

**Resultado (nudos individuales, no racimos):**

| Muestra | Simples S | Simples Z | %Z |
|---|---:|---:|---:|
| Inkawasi, 52 quipus de la literatura (48 en KFG) | 37 | 12 561 | **99,7%** |
| Solo JC001–JC023 | 12 | 794 | 98,5% |
| Pachacamac (museo) | 0 | 3 599 | 100% |
| Puruchuco (región) | 34 | 1 518 | 97,8% |
| Armatambo UR281–UR294 | 5 | 326 | **98,5%** |
| Armatambo, todos (incluye HP047) | 101 | 396 | 79,7% |
| Chachapoyas | 2 167 | 2 330 | **51,8%** |
| Resto | 17 389 | 44 137 | 71,7% |

- **Se replica lo principal:** el dominio Z en Inkawasi (99,7% vs 98,8% reportado) y en Pachacamac/Puruchuco.
- **Cordeles cuyo único nudo es largo/E en Inkawasi:** 1 084 S vs 2 134 Z = **66,3% Z**, frente al 67,5% reportado. Replica.
- **Pero Armatambo no es la excepción que dice:** en la muestra UR281–UR294 (la suya) el 98,5% de los simples son Z. Solo `HP047`, un quipu de Armatambo con 96 nudos S y 0 Z, produce la impresión de inversión; no está en su lista UR. La afirmación “S predomina en Armatambo” **no se sostiene** con KFG.
- **Chachapoyas** (Laguna de los Cóndores) es el verdadero caso atípico: 51,8% Z, prácticamente monedas al aire. Clindaniel no lo menciona.
- **La afirmación “1212 Z vs 0 S”** se acerca en Inkawasi (77 Z vs 6 S en 103 cordeles con largo-S) pero **falla en el corpus**: 13 682 simples S vs 11 837 Z en 13 446 cordeles con largo-S. La razón es que hay quipus con “dialecto S” (ver abajo).

**El problema de pseudorreplicación.** A nivel de nudo, el corpus da 72,8% Z, con un IC binomial del 95% de [72,5%, 73,1%]. Pero al remuestrear **quipus** el IC es [65,4%, 79,4%], y el efecto de diseño es **deff ≈ 469**. La dirección no es un rasgo de cada nudo: es un rasgo del quipu. De 465 quipus con al menos un nudo simple, **247 son 100% Z, 87 son 100% S y 131 mixtos**; el 18,7% de los quipus usa S de forma exclusiva. Un binomial sobre 70 000 nudos da un p astronómico que **no significa nada** porque los nudos no son independientes. Este es el control más importante de todo el informe: **cualquier conclusión pooled sobre dirección de nudos está inflada por un factor ~470**.

**Nivel:** la existencia de un uso sistemático S/Z y su dirección en Inkawasi, **apoyada con datos**; la interpretación Z = no marcado / S = marcado, **propuesta**; la excepción de Armatambo, **refutada** con KFG; la universalidad del patrón, **no apoyada** (hay “dialectos” de quipu).

---

### T5. Torsión S/Z y diversidad de combinaciones (Hyland 2017)

**Afirmación:** los khipus contables de algodón son ~97% S; los de Collata, 58% S / 42% Z; Collata tiene 95 combinaciones de color/fibra/torsión para 487 colgantes, “mucho más” que los contables.

**Resultado:**

- **92,97% S** en 48 363 cuerdas con torsión S/Z (44 965 S, 3 398 Z). IC por bootstrap de quipus: **[89,9%, 95,5%]**. El 97% de Hyland cae en el borde superior pero es compatible; el orden de magnitud se sostiene.
- La torsión también es un rasgo de quipu: **435 quipus 100% S, 46 100% Z, 34 mixtos** (515 con datos). El 93% global es un promedio de dos poblaciones, no una propiedad de cada cuerda.
- **¿Los quipus con Z son “narrativos” o no contables?** Usé como proxies el número de colores, la fracción de colgantes sin nudos y el valor máximo. Resultados (Spearman, n = 463; BH-FDR sobre 3 pruebas):

| Variable | ρ | p | q |
|---|---:|---:|---:|
| n.º de colores | +0,055 | 0,241 | 0,282 |
| fracción de colgantes sin nudos | −0,045 | 0,336 | 0,336 |
| valor máximo del quipu | −0,143 | **0,0021** | **0,0029** |

  Los quipus con más torsión Z **no** son más coloridos ni tienen más cuerdas vacías; si algo, tienen valores máximos **menores**. La hipótesis de que Z marca “narrativo/no contable” no se sostiene con estos proxies. (Los Collata no están en el corpus, así que el 58/42 no se puede comprobar directamente.)
- **95 combinaciones en 487 colgantes:** sin fibra, solo puedo contar color+torsión. En khipus de 300–700 colgantes, la mediana es **7,5 combinaciones** y el máximo **16**; 95 está muy por encima. El ratio de Collata (0,195) está en el percentil 88 de todo el corpus, pero entre quipus grandes (≥100 colgantes) **ningún** quipu alcanza ese ratio (máximo 0,109). **La parte comparativa de la afirmación se sostiene**, con la cautela de que falta la fibra y de que los Collata no están en la base.**Nivel:** 93% S, **apoyado con datos**; 95 combinaciones excepcionales, **apoyado con datos** (parcial, sin fibra); “Z = narrativo”, **no apoyado**.

---

### T6. Metadatos: KH#### y “un tercio no decimal” (Brezine 2024; Urton 2019)

**A) Cobertura KH.** 593 de 651 quipus (91,1%) tienen id `KH####`. Quedan 58 con nombres antiguos: 22 MM, 22 QU, 11 AS, 3 UR; y **1 quipu sin ningún `okr`** (`UR044`). Además hay **3 IDs OKR duplicados** que afectan a 6 filas: `KH0227` = `AS207C`, `KH0267` = `UR034`, `KH0350` = `UR114`. Es decir, **KH#### no es una clave única en el archivo tal como se entrega**: hay que resolver 3 colisiones antes de usarlo como clave de unión. La recomendación de Brezine es correcta en principio, pero la implementación local está incompleta.

**B) “Casi un tercio no decimal”.** Sin una definición operativa, usé la fracción de colgantes sin nudos (valor 0 = ausente):

| Umbral | Quipus | % |
|---|---:|---:|
| sin ningún nudo | 13 | 2,0% |
| >50% de colgantes sin nudos | 81 | 12,4% |
| >33% | 177 | **27,2%** |
| >25% | 245 | 37,6% |
| >10% | 413 | 63,4% |

El único proxy que se acerca a “casi un tercio” es **>33% de colgantes sin nudos (27,2%)**, pero es una definición *ex post* y “sin nudos” no equivale a “no decimal”. La afirmación es **parcial y muy sensible al umbral**; no la usaría como hecho.

---

### T7. Control de calidad del color (Milillo 2023)

Milillo et al. demuestran que el color registrado a ojo puede ser erróneo (cuerdas bicolor/moteadas mal clasificadas) y que eso limita su uso estadístico. Comprobé si KFG y OKR permiten un control independiente.

- **Trampa de identificadores:** `CORD_ORDINAL` del OKR es el ordinal **dentro del padre** (las subsidiarias vuelven a 1); el 28,3% de las filas de `cord` tienen `(KHIPU_ID, CORD_ORDINAL)` duplicado. Un join naive KFG↔OKR por `(quipu, orden)` da solo **38% de concordancia de color**: es un artefacto, no un desacuerdo real.
- **Comparación a nivel de quipu** (447 quipus con ≥10 cuerdas en ambas bases), proporción de cada color: correlaciones de Pearson entre 0,64 (KB, GG) y 0,97 (B, YB); diferencia media absoluta global 0,039. La fracción de blanco difiere ~6 puntos porcentuales entre bases.
- **Conclusión:** KFG y OKR son **casi la misma observación**, no dos observaciones independientes. No permiten validar ni refutar a Milillo. El color sigue siendo un dato **visual, no validado**, y cualquier análisis que lo use debe declararlo.

---

## 4. Controles, nulos y corrección múltiple

Familia confirmatoria (7 pruebas), BH-FDR:

| Prueba | p | q |
|---|---:|---:|
| T2 aritmética UR267A (permutación) | 5,0 × 10⁻⁵ | 8,8 × 10⁻⁵ |
| T3 conglomerados V/R Santa (permutación) | 5,0 × 10⁻⁵ | 8,8 × 10⁻⁵ |
| T3 magnitud V > R (Mann-Whitney) | 6,6 × 10⁻⁹ | 2,3 × 10⁻⁸ |
| T4 %Z Armatambo UR (binomial) | 1,5 × 10⁻⁸⁹ | 1,1 × 10⁻⁸⁸ |
| T5 torsión ~ valor máximo (Spearman) | 2,1 × 10⁻³ | 2,9 × 10⁻³ |
| T5 torsión ~ n.º colores (Spearman) | 0,241 | 0,281 |
| T3 balance V/R (binomial) | 0,664 | 0,664 |

Todas las conclusiones “apoyadas” sobreviven a BH. Las dos que no sobreviven (o no son significativas) se reportan como negativas: **la torsión Z no se asocia a más colores** y **el binario V/R está balanceado pero no es independiente del quipu**.

Controles adicionales:

- **Unidad de análisis:** todos los tests con cuerdas usan bootstrap/permutación por quipu. El deff de 469 en dirección de nudos muestra que un test pooled habría multiplicado por ~470 la falsa precisión.
- **Nulo que preserva la estructura:** en Santa, el nulo conserva el número de bloques por quipu; si se ignorara, la concentración V/R parecería un hallazgo “de población” cuando es un rasgo de quipu.
- **Selección post hoc:** UR28 y UR267A fueron elegidos por la literatura precisamente porque muestran la regularidad. Mis tests son de **consistencia interna**, no de generalidad. Lo digo explícitamente en la etiqueta de evidencia.

---

## 5. Resultados negativos (los que más información dan)

1. **El “resultado” moteado de UR267A no es el resultado:** 2/7 tríos exactos con tercer cordel AB:MB, frente a 9/11 con AB sólido. La aritmética existe; la semántica del color propuesta no.
2. **UR255 no invierte los roles** de forma detectable (7/15, permutación p = 1,0).
3. **No hay mitades 3/3 en el Santa:** 2 quipus R, 3 V, 1 mixto. El signo V/R está confundido con el quipu (V de Cramér 0,70; p de conglomerados 5 × 10⁻⁵), y la asociación V↔magnitud desaparece dentro del único quipu mixto (p = 0,88).
4. **La suma 398 no es 132 ni 133** en ningún *offset* del bloque de 6. La coincidencia con el tributo no se puede verificar sin la *revisita*.
5. **Armatambo no es S-dominante:** 98,5% Z en la muestra UR281–UR294. El “outlier” es un solo quipu, HP047, fuera de esa lista.
6. **La dirección de nudos no es universal:** 18,7% de los quipus son 100% S; Chachapoyas está en 51,8% Z. El “patrón Inkawasi” es un dialecto local, no una gramática panandina.
7. **“1212 Z vs 0 S” no generaliza:** en todo el corpus, los cordeles con largo-S tienen 13 682 simples S vs 11 837 Z.
8. **La torsión Z no marca “narrativo”:** no se asocia a más colores (q = 0,28) ni a más cuerdas vacías; se asocia débilmente a valores máximos *menores* (ρ = −0,14).
9. **KH#### no es clave única** en el archivo: 3 colisiones y 1 quipu sin OKR.
10. **KFG y OKR no son independientes:** un join naive por ordinal da 38% de concordancia por un artefacto de `CORD_ORDINAL`; a nivel de quipu las composiciones de color correlacionan 0,64–0,97.

---

## 6. Nivel de evidencia

| Hallazgo | Nivel |
|---|---|
| UR28: 102 = 102; bloque p5–p76 = 104 (error de 2) | **demostrado** (aritmética interna) |
| UR267A: `primero − segundo = tercero` en 15/25 tríos (p < 10⁻⁴) | **apoyado con datos** |
| Santa: 133 bloques de 6 colgantes consecutivos | **apoyado con datos** (ajuste estructural exacto) |
| Santa: V/R es un rasgo de quipu, no de tributario | **apoyado con datos** (p de conglomerados 5 × 10⁻⁵) |
| Inkawasi: 99,7% de nudos simples Z; largos 66,3% Z | **apoyado con datos** |
| Corpus: 93% de torsión S (IC 89,9–95,5%) | **apoyado con datos** |
| Collata: 95 combinaciones es excepcional para 487 colgantes | **apoyado con datos** (parcial: sin fibra) |
| UR267A: W=suma, AB=resta, moteado=resultado | **no apoyado / contradicho** |
| Santa: V/R = mitades o marcado/no marcado dentro de la población | **propuesto**, con confusión por quipu |
| UR28: 102 = pachaca; 6 ayllus; AB = hanan; ×5 = 510 | **propuesto** |
| Armatambo: S domina | **refutado** con KFG |
| Collata: ALLUKA/YAKAPAR por rebus | **especulativo** (sin datos publicados) |
| Tablas de khipu, Casta, Mangas, tintes | **no evaluable** con este repo |

---

## 7. Limitaciones

- **KFG no es independiente de OKR/KDB.** Las correlaciones de color y la coincidencia de valores sugieren una fuente común. Replicar a Clindaniel con KFG es, en parte, reanalizar los mismos datos con otra codificación; no es una replicación externa.
- **Los documentos externos no están:** *revisita* de 1670, censo de Corongo, transcripciones de Pärssinen-Kiviharju, tablas de Mangas/Casta. Sin ellos, las afirmaciones “documento ↔ quipu” quedan en parcial.
- **Color y torsión son datos visuales**, no validados químicamente (Milillo). El color compuesto del KFG (26,7% de las cuerdas) tiene convenciones de codificación que no siempre coinciden con OKR.
- **Identificación de los seis del Santa** por procedencia + 133 bloques es una inferencia, no un ID documentado.
- **n pequeño** en los casos estrella (UR28, UR267A, seis del Santa): los tests internos son sólidos, pero la generalización es otra cosa.
- **Los 0 sin nudos** se trataron como ausentes; si algún 0 es real, los totales cambian (poco, pero cambian).

---

## 8. Ideas para la siguiente ronda

1. **Conseguir la *revisita* de 1670 y el censo de Corongo** (o la tabla de FitzPatrick) para probar de verdad la alineación de mitades y la suma 398.
2. **Pedir a los autores los datos crudos** de Collata (487 colgantes) y de Mangas (87 cordones): sin transcripción publicada, el rebus no es falsable.
3. **Modelar la dirección de nudos como variable de quipu** (modelo mixto o beta-binomial) y comprobar si los “dialectos” S/Z coinciden con archivos/regiones o con talleres.
4. **Replicar el 133 del Santa con otra definición de bloque** (p. ej. grupos de 6 separados por color) para ver si el número es robusto o una coincidencia de la segmentación.
5. **Test de la hipótesis de “marcado” de FitzPatrick** con una variable externa (rango/edad del tributario) en lugar de la magnitud interna, que está confundida con el quipu.
6. **Auditar el mapeo KH####** y publicar una tabla de equivalencias limpia (3 colisiones, UR044 sin OKR).
7. **No volver a hacer tests pooled de nudos** sin deff: el factor 469 es una advertencia para todo el equipo.

---

## 9. Para el coordinador

- **34 afirmaciones extraídas de 12 fichas: 10 comprobables, 11 parciales, 13 no comprobables** con este repo. La literatura sobre Collata, Mangas y Casta no se puede testear aquí: esos objetos no están en KFG/OKR.
- **UR28 se sostiene aritméticamente:** 102 (cordel 1) = 102 (grupo 2) y 104 en el bloque p5–p76, exactamente el “error de 2” que reporta Urton. La lectura 102 = pachaca y AB = hanan sigue siendo interpretación.
- **UR267A: la aritmética sí, el color no.** 15/25 tríos cumplen `primero − segundo = tercero` (permutación p = 5 × 10⁻⁵), pero el cordel moteado que la hipótesis llama “resultado” solo acierta 2/7, frente a 9/11 del marrón sólido. El “proof of concept” no es una regla de color.
- **Los 133 grupos de seis del Santa se reproducen exactamente** (798 de 824 colgantes; 26 en restos). Es el mejor ajuste estructural del informe.
- **El verso/recto del Santa es un rasgo de quipu, no de tributario:** 69 V / 63 R en total, pero solo 1 de 6 quipus tiene ambos signos (p de conglomerados 5 × 10⁻⁵; V de Cramér 0,70). La asociación V↔valores grandes (p = 6,6 × 10⁻⁹) desaparece dentro del único quipu mixto (p = 0,88). No hay mitades 3/3: 2 R, 3 V, 1 mixto.
- **La suma de los primeros cordeles es 398, no 132/133**, en ningún *offset* del bloque. Sin la *revisita* de 1670 no se puede decir si coincide con el tributo; lo que sí se puede decir es que no es un conteo de tributarios.
- **Inkawasi replica bien:** 99,7% de nudos simples Z y 66,3% Z en cordeles de un solo nudo largo, frente a 98,8% y 67,5% publicados. **Pero Armatambo no es la excepción que dice Clindaniel:** 98,5% Z en su propia muestra UR281–UR294; el único quipu S-dominante es HP047, fuera de esa lista. Chachapoyas, no Armatambo, es el caso atípico (51,8% Z).
- **Alerta de pseudorreplicación:** la dirección de nudos tiene deff ≈ 469; el IC por quipu es [65,4%, 79,4%] frente al binomial [72,5%, 73,1%]. Los 247 quipus 100% Z y 87 quipus 100% S muestran que S/Z es un “dialecto” de quipu. Cualquier p pooled sobre nudos está inflado.
- **Torsión:** 93,0% S (IC 89,9–95,5%), compatible con el ~97% de Hyland. Los quipus con Z no son más coloridos (q = 0,28) ni tienen más cuerdas vacías; la idea de que Z marca “narrativo” no se sostiene. Las 95 combinaciones de Collata sí son excepcionales: en khipus de 300–700 colgantes el máximo del corpus es 16.
- **Metadatos:** KH#### cubre 91,1%, pero hay 3 colisiones de ID y UR044 sin OKR. KFG y OKR no son independientes (composiciones de color r = 0,64–0,97); el join naive por `CORD_ORDINAL` da 38% por un artefacto. Recomiendo no usar color ni identifiers sin auditoría previa.
