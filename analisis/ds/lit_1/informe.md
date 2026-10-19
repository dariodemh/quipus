# Informe `lit_1` — Extracción y verificación de afirmaciones de la literatura sobre quipus

**Fecha:** 17 de octubre de 2026 · **Carpeta:** `analisis/ds/lit_1/`
**Insumos:** 12 fichas de `docs/fichas/` + `analisis/datos/{cuerdas,quipus,grupos}.csv`
**Scripts:** `01_afirmaciones.py` (tabla de afirmaciones), `02_test_sumas.py`, `03_test_urton2005.py`, `04_test_ur6.py`, `05_test_uniformidad.py`, `06_test_categoricas.py`, `07_decimal.py`.

---

## 1. Pregunta

¿Qué afirmaciones concretas y comprobables sobre el significado o la estructura de los quipus hacen las 12 fichas asignadas, y cuáles de ellas se sostienen al contrastarlas con los 651 quipus del corpus KFG?

La tarea tiene dos partes: (a) convertir la prosa de las fichas en afirmaciones con quipus, cifras y prueba explícita (`afirmaciones.csv`); (b) verificar con datos las 3–5 más importantes, con modelo nulo y p-valor.

---

## 2. Método

### 2.1 Extracción

`01_afirmaciones.py` genera `afirmaciones.csv` (46 filas) con las columnas pedidas: `fuente`, `afirmacion`, `quipus_implicados`, `cifras`, `como_comprobarla`, `comprobable_con_datos_del_repo`.

| Comprobabilidad | Filas |
|---|---|
| sí | 14 |
| parcial | 15 |
| no | 17 |

Las 17 "no" son, sobre todo, afirmaciones que dependen de documentos coloniales (Urton 1998, 2001), de quipus etnográficos ausentes del corpus (Salomon 2002, 2004), de libros sin texto disponible (Conklin 2002) o de identificaciones que el KFG no permite (números B-87xx de Locke 1928, AS114/AS123, AS116/AS150).

### 2.2 Datos y unidad de análisis

- 651 quipus, 57.818 cuerdas, 41.714 cuerdas de nivel 0 (colgantes), 64.464 racimos de nudos.
- La unidad de análisis es el **quipu**, no la cuerda. Los contrastes a nivel de cuerda se acompañan de un nulo que permuta **dentro de cada quipu**.
- `valor` es el valor decimal decodificado por KFG. Los ceros sin nudos se tratan como ausentes, no como cero (se conservan como 0 sólo para sumar grupos, y se advierte).
- Para la dirección de nudo se parseó la cadena `nudos` (`nTIPO(posición,dirección),aporte`): 64.464 racimos, 34.547 cuerdas con al menos un nudo S/Z.

### 2.3 Controles

Cada contraste lleva su nulo explícito: permutación de valores dentro de cada quipu (sumas), permutación de una secuencia (cuentas duplicadas), o comparación con la esperanza bajo Independencia dada la frecuencia global (uniformidad). Semilla fija `20261017`; B = 5.000–20.000. Los p-valores principales se corrigen con Holm.

---

## 3. Resultados

### 3.1 Codificación decimal posicional — Locke 1912, Ascher & Ascher 1981

**Afirmación:** los nudos se leen en base 10 posicional; el nudo largo expresa unidades; los grupos de nudos simples van de 1 a 9.

Con los 64.464 racimos:

| Tipo | Racimos | Máx. nudos | Máx. aporte | `aporte == n` |
|---|---|---|---|---|
| S (simple) | 26.776 | 800 | 300.000 | 0,008 |
| L (largo) | 28.297 | 4.000 | 4.000 | 0,999 |
| E (figura de ocho) | 8.710 | 700 | 700 | 1,000 |
| EE / LL / BL / SP / TF | 445 | ≤6 / ≤800 | ≤800 | 1,000 |

- De 26.721 racimos simples con `n ≤ 9` y aporte > 0, **99,86% cumplen `aporte = n × 10^k`** con k entero. Distribución de k: 196 unidades, 19.253 decenas, 5.789 centenas, 1.341 millares, 139 diezmiles, 3 cienmiles.
- **Ningún** nudo largo con `n ≤ 9` aporta ≥ 10 (0 de 27.934): el nudo largo es siempre unidades.
- Los 665 racimos (1,03%) con `n > 9` no son violaciones de la regla decimal: en ellos el prefijo es el **valor**, no el número de nudos (p. ej. `20L(…),20`, `800S(…),800`), una convención de registro de KFG.

**Nivel de evidencia: demostrado (consistencia interna), no prueba independiente.** El `valor` de KFG se decodificó con la misma regla decimal, así que el test verifica que la base de datos es internamente coherente y que el 1% restante son convenciones, no que la lectura sea la única posible. Aun así, descarta errores gruesos y fija el marco para los tests siguientes.

### 3.2 La cuerda superior suma el grupo — Locke 1912, 1927, 1928

**Afirmación:** la *top cord* que enlaza un grupo suma los valores de las cuerdas pendientes de ese grupo.

Diseño: se tomaron los grupos con **exactamente una** cuerda de nivel 0 (el candidato a top cord) y un grupo previo con ≥3 cuerdas de nivel 0. Se comparó el valor del candidato con la suma del grupo previo (sólo nivel 0).

| | N | Aciertos exactos | Tasa |
|---|---|---|---|
| candidato con `union=T` | 70 (16 quipus) | 23 | **32,9%** |
| candidato sin `T` | 890 | 152 | 17,1% |

- Fisher one-sided (T > no T): OR = 2,38, **p = 0,0016**.
- **Nulo de permutación** (B = 5.000; se permutan los valores de nivel 0 dentro de cada quipu, preservando tamaños de grupo y la posición de la marca T): observado 23, media nula **0,98**, p95 = 3, **p = 0,0002**.
- Dentro de los 16 quipus que tienen candidatos T, los candidatos **no-T** aciertan **0/6**. Es decir, en esos mismos quipus la marca T discrimina.
- El desglose por quipu muestra que los aciertos no vienen de un solo objeto: AS001–AS004, AS006 (4/6), AS007 (4/10), QU009 (4/6), QU012, QU014, QU015, QU016 y QU019 aportan al menos uno.
- **Variante que incluye subsidiarias en la suma:** 6/70 (8,6%), peor que la suma sólo de nivel 0. La top cord suma **pendientes**, no pendientes+subsidiarias, lo que concuerda con que Locke (1927) reporte las subsidiarias por separado (71).

**Nivel de evidencia: apoyado con datos.** No es universal: sólo un tercio de las top cords suma, y la cobertura es de 16 quipus (la marca `T` sólo aparece en 26 quipus del corpus). Pero el efecto supera ampliamente al azar y es específico de la marca T.

**Caveat de circularidad:** si el digitador hubiera marcado `T` *porque* la cuerda suma, el test sería circular. No parece el caso: 47 de 70 top cords **no** suman su grupo. La marca T es una categoría de fijación física, no una etiqueta inferida de la aritmética.

### 3.3 Cuentas duplicadas — Urton 2005

#### AS159 / AS173

Secuencias de valores de nivel 0:

```
AS159: 1 17 16 16 18 12 16 2 49 25 18 4 1 24 79 ...
AS173: 1  1 17 16 16 18 12 16 66 20 38 21 7
```

El tramo `[1, 17, 16, 16, 18, 12, 16]` aparece en **AS159[0:7]** y en **AS173[1:8]**. Es exactamente el solapamiento descrito por Urton (los 7 primeros de AS159 = P2–P8 de AS173).

- **Nulo:** 20.000 permutaciones de la secuencia de AS173; el tramo común contiguo más largo (LCCS) observado es 7, la media nula 1,98, p95 = 3, **p = 0,00005**.
- **Control de corpus:** en 276 quipus con 10–60 pendientes, ≥5 valores distintos y ≥50% no-cero (37.950 pares), sólo **68 pares (0,18%)** alcanzan un tramo ≥7. El máximo del corpus es 14 (`UR066`/`UR067`). Un tramo de 7 no es único, pero sí raro.

#### AS194 / AS195

AS194 = `[120, 0]`, AS195 = `[120]`: el valor 120 coincide y AS194 tiene un pendiente extra sin nudos, tal como dice la ficha. Pero el control es contundente: **46 quipus** tienen algún pendiente de 120 y **4 quipus** tienen el primer pendiente de 120. Con una sola cuerda, la coincidencia no es evidencia por sí sola; sólo un análisis de color y estructura (que aquí no se hizo) podría sostenerla.

#### Control inesperado: duplicados dentro del propio corpus

Buscando secuencias de nivel 0 idénticas (≥8 cuerdas) aparecieron dos pares de registros con **la misma secuencia exacta**: `KH0033 = UR044` (54 valores idénticos) y `UR070 = UR071`. Son probablemente el mismo objeto catalogado dos veces. Cualquier análisis de "cuentas duplicadas" debe deduplicar antes; aquí no afecta a AS159/AS173, pero es un aviso para el resto del equipo.

**Nivel de evidencia: apoyado con datos** (AS159/AS173); **propuesto** (AS194/AS195).

### 3.4 UR6: calendario y censo — Urton 2001, 2005

**Afirmación:** UR6 tiene 762 pendientes, 730 organizados en 24 conjuntos de 29–31 cuerdas (dos años de 365 días) y 2.962 nudos; UR9 y UR21 replican un segmento de cuatro meses.

Lo que hay en KFG para `UR006` (KH0242, Leymebamba):

| Métrica | Urton | KFG | Δ |
|---|---|---|---|
| pendientes (nivel 0) | 762 | **571** | −191 |
| conjuntos de 29–31 | 24 | **0** | — |
| tamaño máximo de grupo | 29–31 | **22** | — |
| nudos totales | 2.962 | **1.480** | ≈ mitad |
| cuerdas totales | — | 874 (285 nivel 1, 18 nivel 2) | — |

- Tamaños de grupo: {1: 33, 2: 2, 4: 2, 5: 2, 20: 1, 21: 10, 22: 13}. Los 571 pendientes / 24 = 23,8, no 29–31.
- El total de nudos es casi exactamente la mitad (1.480 ≈ 2.962/2), lo que sugiere una diferencia de convención de conteo (¿nudos vs. vueltas? ¿mitad del objeto?) más que un error aleatorio.
- **UR9/UR21:** el tramo común contiguo más largo con UR6 es 10 para UR009 (nulo medio 7,9; **p = 0,09**) y 7 para UR021 (nulo medio 6,6; **p = 0,51**). No hay evidencia de replicación en las secuencias de KFG.

**Nivel de evidencia: no comprobable con este corpus / discrepancia de datos.** No refuta a Urton: la versión KFG de UR006 parece incompleta o digitalizada con otro criterio (los 762 pendientes y los 24 conjuntos no están). Pero **cualquier análisis que use UR006 de KFG no puede asumir la estructura publicada**, y el equipo debería consultar el KDB/OKR o el registro original antes de construir sobre ella.

### 3.5 Uniformidad de torsión y dirección de nudo — Ascher 2005

**Afirmación (a):** spin y ply son uniformes en todos los cordeles salvo 3 quipus.

- Torsión S/Z por quipu: **481/515 uniformes (93,4%)**; 34 mixtos. Restringiendo a quipus con ≥5 cuerdas con torsión: 468/501 (93,4%).
- El dato de Ascher (56/59 = 94,9%) coincide casi exactamente.
- Nulo: si las etiquetas se asignaran independientemente con la p global (Z = 7,0%), se esperarían **63,7** quipus uniformes entre los 501 con ≥5 cuerdas; se observan **468**. La uniformidad es una propiedad del objeto, no del azar.
- Los quipus mixtos son sistemáticamente más grandes (media 152,9 cuerdas vs. 89,7): parte de la "mixtura" es un efecto de tamaño.
- No se puede testear el *ply* ni la torsión del cordón principal: `quipus.csv` no trae esos campos.

**Afirmación (b):** ~81% de los quipus tienen dirección de nudo uniforme; 19% mixta.

- Con criterio estricto (100% de los nudos en una sola dirección): **182/512 = 35,5%** uniformes, 330 mixtos. **No replica el 81%.**
- Pero el criterio estricto no es el único posible: 72,9% de los quipus tienen ≥80% de sus nudos en una dirección, 58,6% ≥90%, y la fracción mayoritaria mediana es 95,1%. Por cuerda, 90,1% tienen una sola dirección.
- Los quipus con dirección mixta son otra vez más grandes (79,6 vs. 47,0 pendientes).

**Nivel de evidencia:** (a) **apoyado con datos**; (b) **no replicado con criterio estricto; discrepancia probablemente definicional** (Ascher pudo contar "predominante" o una submuestra de 59 quipus más pequeños). No se puede afirmar que Ascher se equivoque sin su definición operacional exacta.

### 3.6 "Sumas categóricas": madre = suma de subsidiarias — Ascher & Ascher 1981

**Afirmación:** el valor de una cuerda madre es la suma de sus subsidiarias.

- 9.426 madres con ≥1 subsidiaria en 435 quipus: **1.189 coincidencias exactas (12,6%)**.
- Madres con valor > 0 y ≥2 hijas: **117/2.340 = 5,0%**.
- **Nulo de permutación** (B = 2.000; se permutan los valores de todas las cuerdas dentro de cada quipu, preservando la jerarquía): observado 1.189, media nula **1.205**, p95 = 1.250, **p = 0,73**.

**Nivel de evidencia: resultado negativo.** La tasa observada es *igual o menor* que la esperada por azar dadas las distribuciones de valores. La relación "madre = suma de hijas" **no es una regla del corpus**. El único bolsón con exceso aparente son las madres con 8 hijas (23,2%), y está concentrado en dos quipus (UR093: 23/96; HP038: 10/24), no es general. Ascher describió relaciones válidas para especímenes concretos; extrapolarlas al corpus es incorrecto.

---

## 4. Controles, p-valores y corrección múltiple

| Test | Estadístico | Nulo | p |
|---|---|---|---|
| Top cord = suma del grupo | 23/70 vs 0,98 esperados | permutación intra-quipu, B=5.000 | **0,0002** |
| Top cord vs no-T (mismo estadístico) | OR 2,38 | Fisher one-sided | 0,0016 |
| AS159/AS173 tramo de 7 | LCCS 7 vs media 1,98 | permutación de AS173, B=20.000 | **0,00005** |
| UR9 vs UR6 | LCCS 10 | permutación de UR9, B=5.000 | 0,09 |
| UR21 vs UR6 | LCCS 7 | permutación de UR21, B=5.000 | 0,51 |
| Madre = suma de hijas | 1.189 vs 1.205 | permutación intra-quipu, B=2.000 | 0,73 |

**Holm** sobre los tres tests primarios (top cord, AS159/AS173, sumas categóricas): 0,00005×3 = 0,00015; 0,0002×2 = 0,0004; 0,73. Los dos positivos sobreviven; el negativo se mantiene negativo.

Controles adicionales: (i) en los quipus con top cords, los candidatos no-T aciertan 0/6; (ii) la variante que incluye subsidiarias empeora el ajuste (6/70); (iii) el control de corpus para tramos de 7 da 0,18% de pares; (iv) se detectaron duplicados de registro (KH0033=UR044, UR070=UR071) que hay que excluir en análisis de duplicados.

---

## 5. Resultados negativos (explícitos)

1. **UR6 no reproduce la estructura publicada** en KFG: 571 vs 762 pendientes; 0 grupos de 29–31 (máx. 22); 1.480 vs 2.962 nudos. UR9/UR21 no muestran el segmento de cuatro meses (p = 0,09 y 0,51).
2. **"Madre = suma de subsidiarias" no es una regla del corpus**: 12,6% de coincidencias, p = 0,73; con ≥2 hijas y madre > 0, sólo 5,0%.
3. **La uniformidad estricta de dirección de nudo no llega al 81%** de Ascher: 35,5% con criterio 100%; 72,9% si se admite ≥80%.
4. **AS194/AS195 no es evidencia fuerte por sí solo**: 46 quipus tienen un pendiente de 120; con una sola cuerda la coincidencia es barata.
5. **17 de 46 afirmaciones no son comprobables con este corpus** (documentos coloniales, quipus etnográficos, libros sin texto, ids ausentes).
6. **Dos pares de registros duplicados** en KFG (KH0033=UR044; UR070=UR071): riesgo de pseudorreplicación a nivel de quipu si no se deduplican.
7. **No se pudo identificar el espécimen de Locke 1927** (15 grupos de 6 + 3 cuerdas sueltas; top cords = 839; subsidiarias = 71). El único quipu del corpus con 15 grupos de exactamente 6 pendientes es `QU014`, pero tiene 192 pendientes, 16 top cords con suma 2.497 y 0 subsidiarias de esas top cords; no coincide. El más parecido en estructura es `AS006` (6 grupos de 6, top cords = 723, subsidiarias de top cords = 76), pero tampoco. El espécimen Heye probablemente no está digitalizado en KFG o lo está con otra segmentación.

---

## 6. Nivel de evidencia por conclusión

| Conclusión | Nivel |
|---|---|
| Codificación decimal posicional y nudo largo = unidades | **Demostrado** (consistencia interna; no independiente) |
| La top cord suma el grupo de pendientes (no subsidiarias) | **Apoyado con datos** (23 casos, 16 quipus, p=0,0002) |
| AS159/AS173 son cuentas duplicadas | **Apoyado con datos** (p=0,00005; 0,18% de pares comparables) |
| AS194/AS195 son cuentas duplicadas | **Propuesto** (coincidencia de una sola cuerda) |
| Torsión uniforme dentro del quipu | **Apoyado con datos** (93,4% vs 12,7% esperado) |
| ~81% de quipus con dirección de nudo uniforme | **No replicado**; discrepancia probablemente definicional |
| UR6 = calendario bienal + censo con 24 conjuntos de 29–31 | **No comprobable con KFG**; los conteos discrepan |
| "Sumas categóricas" como regla general | **Refutado como regla de corpus** (negativo) |
| Quipu como escritura / código binario semántico (Urton 1998, 2003) | **No comprobable** con estos datos; sin control externo |
| Tupicocha como continuidad etnográfica (Salomon 2002, 2004) | **No comprobable** (no hay quipus etnográficos en el corpus) |

---

## 7. Limitaciones

- El corpus KFG es una digitalización secundaria: `valor`, `union` y los tipos de nudo ya son interpretaciones. Los tests de suma y de duplicados son más independientes que el decimal, pero no completamente.
- `union=T` sólo aparece en 26 quipus y 154 cuerdas; la cobertura de top cords es sesgada hacia la colección AS (AMNH/Heye), justo donde Locke y Ascher trabajaron. No se puede generalizar a los 651.
- No hay torsión del cordón principal ni *ply* en `quipus.csv`, así que la afirmación completa de Ascher 2005 sólo se testea a medias.
- Los ids de Urton 2005 (AS114/AS123, AS116/AS150) y los números B-87xx de Locke no están en KFG; varias afirmaciones centrales quedan fuera de alcance.
- El test de tramos comunes está dominado por secuencias de baja entropía (muchos ceros); por eso se filtró a ≥5 valores distintos y ≥50% no-cero, y aun así el LCCS nulo medio es alto (1,98 para AS173, 7,9 para UR9).
- No se corrigió por el número de pares que Urton pudo haber mirado antes de reportar AS159/AS173; el p=0,00005 es válido para un par preespecificado, no para una búsqueda exhaustiva.

---

## 7.1 Reproducibilidad

Desde `analisis/ds/lit_1/`:

```
python 01_afirmaciones.py      # genera afirmaciones.csv
python 02_test_sumas.py        # top cord = suma (V1)
python 03_test_urton2005.py    # AS159/AS173, AS194/AS195, control de corpus (V2)
python 04_test_ur6.py          # UR6, UR9, UR21 (V3)
python 05_test_uniformidad.py  # torsión y dirección de nudo (V4)
python 06_test_categoricas.py  # madre = suma de hijas (V5)
python 07_decimal.py           # consistencia decimal (V0)
```

Todos leen `analisis/datos/*.csv`, no escriben fuera de la carpeta y usan semilla fija `20261017`. Los p-valores de permutación se regeneran de forma determinista.

---

## 8. Para el coordinador

- **46 afirmaciones extraídas** de las 12 fichas: 14 comprobables con el repo, 15 parciales, 17 no comprobables (documentos coloniales, quipus etnográficos, libros sin texto, ids ausentes).
- **La lectura decimal se sostiene**: 99,86% de 26.721 racimos simples cumplen `aporte = n×10^k`, y **ningún** nudo largo bien formado (n≤9) aporta ≥10. Es consistencia interna de KFG, no una prueba independiente.
- **La top cord suma de verdad**: 23/70 aciertos exactos (32,9%) frente a 152/890 (17,1%) en cuerdas no-T; permutación intra-quipu p=0,0002, Fisher p=0,0016. Suma sólo pendientes de nivel 0, no subsidiarias.
- **AS159/AS173 es un duplicado genuino**: tramo exacto de 7 valores `[1,17,16,16,18,12,16]` (AS159[0:7] = AS173[1:8]), p=0,00005; sólo 0,18% de los pares comparables del corpus alcanzan 7.
- **AS194/AS195 es evidencia débil**: coincide 120=120, pero 46 quipus tienen un pendiente de 120. No lo usaría como prueba principal de la tesis archivística.
- **UR6 no se puede usar tal como está en KFG**: 571 pendientes (no 762), 0 grupos de 29–31 (máx. 22), 1.480 nudos (no 2.962, casi la mitad). UR9/UR21 no replican el segmento (p=0,09 y 0,51). Hay que ir al KDB/OKR o al registro original.
- **Resultado negativo importante**: "madre = suma de subsidiarias" no es una regla del corpus (12,6%; p=0,73 frente al nulo). Sólo 5,0% con ≥2 hijas y madre >0. Ascher aplica a especímenes, no al corpus.
- **Ascher 2005 se replica a medias**: torsión uniforme 93,4% (vs 94,9% publicado); dirección de nudo uniforme estricta 35,5%, no 81% — pero 72,9% si se admite ≥80% en una dirección. La discrepancia es de definición, no necesariamente de datos.
- **Alerta de datos**: `KH0033 = UR044` y `UR070 = UR071` tienen secuencias de pendientes idénticas; son registros duplicados del mismo quipu. Deduplicar antes de cualquier análisis que cuente quipus.
- **Siguiente ronda recomendada**: (1) reconstruir la lista de top cords desde el KDB y no desde `union`; (2) buscar los pares de Urton en OKR/KDB (AS114/AS123, AS116/AS150) y aplicarles el mismo nulo de LCCS; (3) pedir la definición operacional de "dirección de nudo uniforme" a la tabla de Ascher 2005; (4) resolver UR6 con el registro original antes de testear el calendario.
