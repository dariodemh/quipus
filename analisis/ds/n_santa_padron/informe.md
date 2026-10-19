# ¿Sigue el orden de los nombres del padrón del Santa (1670) el orden de los grupos de los quipus?

**Dictamen en una línea:** no. Ninguna prueba de orden sobrevive a la corrección múltiple; el único exceso nominal (precisión color→nombre *in-sample*, p = 0,021) desaparece al validar fuera de muestra (0,117 frente a 0,092 esperado, p = 0,32) y se explica porque en los dos quipus grandes el color de la primera cuerda es una **seriación posicional** (ciclos de 4 y 5 colores), no una etiqueta individual. La coincidencia de tamaños entre pachacas y quipus que usa Urton (2017, tabla 12.3) es la asignación por rangos elegida *post hoc*, no un hallazgo.

Etiqueta de evidencia: **apoyado con datos (resultado negativo)**. La estructura del archivo y la seriación de color están **demostradas**; la hipótesis de orden queda **no apoyada**; cualquier lectura nombre↔grupo concreta es **especulativa**.

---

## 1. Pregunta

Los equipos 11 y 12 propusieron que el orden de los nombres en el padrón de la revisita de 1670 (seis pachacas de Recuayes, San Pedro de Corongo, valle del Santa) sigue el orden de los grupos de seis cuerdas en los quipus del Santa. Se prueba:

- **H-macro:** el orden de las pachacas en el documento sigue el orden/tamaño de los seis quipus.
- **H-micro:** dentro de cada pachaca, el nombre *i* corresponde al grupo *i* del quipu emparejado. Es decir, algún rasgo observable del grupo (color de la primera cuerda, valor de la posición 1, tipo de unión, etc.) debe alinearse con algún rasgo del nombre (nombre de pila, apellido, condición de dependiente, etc.) **en la misma posición**.

La segunda es la única hipótesis propiamente de orden y la única falsable con estos datos.

---

## 2. Datos y fuentes

- **Quipus:** `analisis/datos/cuerdas.csv` (KFG). UR087–UR092 = KH0323–KH0328, Museo Temple Radicati, procedencia «Santa». Se reconstruyeron los 133 grupos de seis cuerdas con los mismos criterios de exclusión de cuerdas sueltas que `05_etnohistoria/santa_grupos.py` (UR087 sin grupos de tamaño 1; UR089 sin p73 y p140; UR090 sin p31, p38 y p63–p66). Resultado: **48 / 9 / 34 / 17 / 15 / 10 = 133**, idéntico a Urton (2017: 229, tabla 12.3) y a Medrano y Urton (2018).
- **Padrón:** Urton 2017, Apéndice A (pp. 239–240), transcrito en orden; contrastado con la tabla 4 de Medrano y Urton 2018 y con la tabla 2 (conteos por pachaca). Segmentación de nombres propia (el texto va corrido); los totales por pachaca coinciden con los publicados.
- **Literatura:** Urton 2017, cap. 12 y Apéndices A–B; Medrano y Urton 2018 (texto completo, 302 líneas).
- **Aviso de identificadores:** `KH0227` es «Huaura Valley, near Lima, on Santa Rosalía Hacienda» y `UR198` es «Santa Clara, Nazca». **No son quipus del valle del Santa**: son homónimos de «Santa» en el campo `procedencia`. Incluirlos en el archivo sería un error de datos; no tienen padrón asociado y no se usan aquí (véase §5).

Semilla fija 1670. Scripts: `s0_datos.py` (construcción de datos), `s1_test.py` (descriptivos y test principal), `s2_orden.py` (variantes de alineación y periodicidad), `s3_rasgos.py` (max-estadístico sobre 72 pares de rasgos), `s4_controles.py` (por quipu, controles y Holm). Salidas en `s1.out`–`s4.out`, `santos_grupos133.csv`, `padron_orden.csv`.

---

## 3. Método

1. **Unidad de análisis:** el quipu, no la cuerda (regla 1 del BRIEF). Los grupos se comparan dentro de su quipu; el estadístico agregado se calcula sobre los pares alineados y el nulo permuta **dentro de cada pachaca**, de modo que se conservan tamaños, márgenes de nombres y composición por pachaca.
2. **Nulo explícito:** para H-micro, permutación del orden de los nombres dentro de cada pachaca (destruye exactamente el orden, conserva todo lo demás). Para H-macro, dos nulos: (a) las 720 asignaciones de quipus a pachacas; (b) composiciones aleatorias de 133 grupos en 6 partes (el nulo correcto para «¿son los tamaños más parecidos de lo esperable?»).
3. **Alineación:** emparejamiento por prefijo (nombre *i* ↔ grupo *i*), que es lo que implica «el orden sigue el orden». Como los conteos no coinciden (133 grupos frente a 130 nombres), se probaron además orden invertido y desplazamientos de −5 a +5 como análisis de sensibilidad.
4. **Estadísticos:** V de Cramér (asociación categórica), precisión de la mejor asignación color→nombre (in-sample y *held-out*: ajuste en posiciones pares, prueba en impares), AMI (información mutua ajustada, robusta a cardinalidad) y Spearman para tendencias.
5. **Corrección múltiple:** Holm sobre la batería de pruebas de orden; en el test exploratorio de 72 pares de rasgos, **max-estadístico** (se recalcula el máximo en cada permutación), que controla la búsqueda sobre rasgos sin necesidad de Holm.

---

## 4. Resultados

### 4.1 Lo que sí se reproduce (validación de los datos)

| Comprobación | KFG / padrón | Publicado |
|---|---|---|
| Grupos de 6 por quipu | 48 / 9 / 34 / 17 / 15 / 10 = **133** | 133 (Urton 2017: 229) |
| Colores distintos en la 1.ª cuerda | **33** | 32 (Medrano y Urton 2018) |
| Colores que aparecen una sola vez | **17** | 17 |
| Grupos con las 6 cuerdas del mismo color (sin rangos de longitud) | 122/133 | «color-banded» |
| Tributarios por pachaca | 18 / 23 / 9 / 7 / 41 / 32 = **130** | 130 (Medrano y Urton 2018, tabla 2) |
| Total del documento | 130 listados + 2 ausentes = 132 | 132 |
| Suma de la posición 1 | **369** | 359 + 2 cuerdas rotas ≈ 367/8 |
| Unión R / V de la 1.ª cuerda | 63 / 69 (+1 U) | 63 / 70 |

Notas: (i) Urton (2017: 218) dice «Namús (19)» y total 131; la lista del Apéndice A tiene **18** nombres y Medrano y Urton (2018) usan 18. Uso 18. (ii) La suma de posición 1 da 369 en KFG; el libro da 359 más dos cuerdas rotas. Al menos 9 de los 10 puntos de diferencia están en **una sola celda**: UR087 grupo 3, posición 1 = 10 en KFG y 1 en el Apéndice B. Es una discrepancia de transcripción, no de estructura. (iii) El Apéndice B coincide grupo por grupo con KFG en los 15 grupos de UR091 (valores y colores), lo que valida la reconstrucción. (iv) El número de grupos con las seis cuerdas del mismo color es 115/133 si se comparan las cadenas crudas; sube a 122/133 al eliminar los rangos de longitud del código (que varían de una cuerda a otra dentro del mismo grupo).

El padrón, además, tiene **una sola agrupación deliberada visible**: los cinco «hijo de» están todos al final de Namus (posiciones 14–18). No hay agrupación por apellidos: la fracción de apellidos iguales en posiciones contiguas es 0,09 en Corongo (p = 0,06) y 0,00 en las otras cinco pachacas. Es decir, **el orden de los nombres es casi arbitrario** salvo ese bloque final; no hay una estructura familiar que el quipu pudiera estar replicando.

### 4.1b Todo lo cuantitativo del padrón (respuesta al punto 1 de la tarea)

- **Seis pachacas**, en este orden en el documento: Namus, Corongo, Cuyuchin, Cusca, Guauyan, Ucore.
- **Tributarios:** 18, 23, 9, 7, 41, 32 = **130 con nombre**; el documento declara **132** «ausentes y presentes» (2 sin nombre). Urton (2017: 218) cuenta 19 en Namus y 131; la lista tiene 18 (Medrano y Urton 2018 también usan 18).
- **Tributo:** 2 pesos, 7 reales y 3 quartillos por tributario; total 367 pesos, ¼ real y 1 quartillo (2,75 × 132 = 363, de ahí la discusión de Urton sobre el redondeo).
- **Categorías:** el padrón es una lista de **tributarios varones**; **no hay casados / viudos / solteros** ni edades. Las únicas marcas internas son **5 «hijo de»** (todos en Namus, al final) y **4 honoríficos** (3 «don» + 1 «d.»). No hay otra jerarquía registrada.
- **Orden interno:** por pachaca, sin orden alfabético, sin orden por tamaño y sin agrupación familiar detectable (§ arriba). El orden de las pachacas tampoco es alfabético ni por tamaño (18, 23, 9, 7, 41, 32).
- **Nombres de pila:** 40 distintos y 24 que aparecen una sola vez con mi normalización directa; 34/17 con normalización agresiva; Medrano y Urton publican 30/14. Los más frecuentes: «juo» (32), «franco» (11), «po» (8), «domingo» (7), «agn»/«joseph»/«diego» (6 cada uno).

### 4.2 H-macro: el emparejamiento pachaca↔quipu no es evidencia

| Pachaca (orden del documento) | Tributarios | Quipu (tabla 12.3) | Grupos |
|---|---|---|---|
| Namus | 18 | UR091 | 15 |
| Corongo | 23 | UR090 | 17 |
| Cuyuchin | 9 | UR092 | 10 |
| Cusca | 7 | UR088 | 9 |
| Guauyan | 41 | UR087 | 48 |
| Ucore | 32 | UR089 | 34 |

- Σ|diferencia| = **21**; Spearman = **1,00**.
- Nulo (a), 720 permutaciones de quipus: p = 0,0056. **Pero solo 4 de las 720 asignaciones alcanzan el mínimo 21**: la asignación propuesta es, por construcción, la que ordena los tamaños. Urton eligió el emparejamiento que hace coincidir los rangos; el p = 0,0056 solo dice que eligió bien, no que el orden signifique algo.
- Nulo (b), composiciones aleatorias de 133 en 6 partes: **p = 0,24**. Los tamaños no son más parecidos de lo esperable por azar (coincide con 12_urton2017).

Además, no existe un «orden de los quipus» independiente: el orden físico del archivo (UR087…UR092) no coincide con el orden del documento (Spearman −0,66, n = 6, p = 0,16), y la única ordenación que coincide es la que se construyó para que coincidiera. **H-macro no es contrastable y no aporta evidencia.**

### 4.3 H-micro: color de la primera cuerda frente a nombre de pila, en orden

Alineación por prefijo, n = 121 pares (se pierden 12 grupos y 9 nombres por los conteos desiguales).

| Pachaca | Quipu | n | V | p(V) | precisión | p | held-out | p |
|---|---|---|---|---|---|---|---|---|
| Namus | UR091 | 15 | 0,746 | 0,17 | 0,667 | 0,27 | 0,000 | 1,00 |
| Corongo | UR090 | 17 | 0,832 | 0,45 | 0,706 | 1,00 | 0,000 | 1,00 |
| Cuyuchin | UR092 | 9 | 0,913 | 0,038 | 0,778 | 0,048 | 0,500 | 0,048 |
| Cusca | UR088 | 7 | 0,750 | 1,00 | 0,714 | 1,00 | 0,000 | 1,00 |
| Guauyan | UR087 | 41 | 0,644 | 0,98 | 0,268 | 0,95 | 0,100 | 0,23 |
| Ucore | UR089 | 32 | 0,788 | 0,20 | 0,719 | 0,046 | 0,125 | 0,10 |
| **Agregado** | | **121** | **0,583** | **0,18** | **0,438** | **0,021** | **0,117** | **0,32** |

- **V agregada = 0,583**; nulo 0,554 (p95 0,608); **p = 0,18**. Sin señal.
- **Precisión in-sample = 0,438** frente a 0,397 esperado por el nulo (p95 0,430); p = 0,021 sin corregir. Es el único resultado nominalmente «positivo» de toda la batería. Pero:
  - al excluir el nombre más frecuente («juo», 32/130) baja a 0,413 (p = 0,098);
  - **fuera de muestra cae a 0,117** frente a 0,092 esperado (p95 0,150; p = 0,32): el exceso era sobreajuste del mapeo color→nombre;
  - tras Holm, p = 0,125. No sobrevive.
- Por quipu, solo Cuyuchin/UR092 da p ≈ 0,04, y con n = 9 y 5 colores. Ese quipu tiene un **ciclo estricto de 5 colores** (coincidencia a distancia 5 = **1,00**): los colores se repiten dos veces en 10 grupos. Con una secuencia periódica y 9 nombres, un mapeo aprende de memoria. Con 6 pruebas por quipu, Holm lo elimina (0,038 × 6 ≈ 0,23).

### 4.4 La explicación aburrida: en los quipus grandes el color es posición, no identidad

- **UR087 (48 grupos, 36 % del archivo):** 8 colores, coincidencia a distancia 1 = 0,02 y **a distancia 4 = 0,66** (azar ≈ 0,18). El khipu se ordena como una **seriación de 4 columnas**: dispuestos los 48 grupos en 12 filas × 4 columnas, **5 de las últimas 6 filas son exactamente W | RB | AB | YB** (solo la fila 7 desvía la primera celda):

  ```
  fila  0: AB/YB | AB    | W  | AB
  fila  1: AB/YB | W/AB  | YB | AB
  fila  2: AB/YB | YB/AB | RB | YB
  fila  3: AB/YB | AB    | RB | YB
  fila  4: AB/YB | YB/AB | RB | YB
  fila  5: W     | RB    | YB | MB
  fila  6: W     | RB    | AB | YB
  fila  7: YB    | RB    | AB | YB
  fila  8: W     | RB    | AB | YB
  fila  9: W     | RB    | AB | YB
  fila 10: W     | RB    | AB | YB
  fila 11: W     | RB    | AB | YB
  ```

- **UR092 (10 grupos):** 5 colores en ciclo estricto (W-LG, RL, AB, W, RB), dos vueltas completas.
- Entre ambos suman **58 de 133 grupos (44 %)** en los que el color de la primera cuerda está determinado, total o mayoritariamente, por la posición módulo *k* (estrictamente en UR092, con lag-4 = 0,66 en UR087). En esos grupos el color **no puede** estar firmando el nombre de un individuo en el orden lineal.
- En UR090 (17 grupos, mezcla R/V) y UR091 (15 grupos) no hay ciclo, pero tampoco alineación con los nombres (§4.3).

### 4.5 El único bloque que se parece (y por qué no basta)

- Namus: 13 independientes + **5 «hijo de» al final** (posiciones 14–18).
- UR091: 9 grupos con posición 1 = 4 + **6 grupos con posición 1 = 0 al final**, separados por un hueco físico en el cordón principal (confirma Medrano y Urton 2018).
- La coincidencia cualitativa es real y llamativa: las dos listas terminan en un bloque marcado. Pero (i) los tamaños no coinciden (5 frente a 6); (ii) los límites están en el 72 % de la lista de nombres y en el 60 % de la de grupos, con ~2–4 posiciones de desfase; (iii) la probabilidad conjunta 1/(C(18,5)·C(15,6)) = 2,3 × 10⁻⁸ **no es válida**, porque el par de rasgos se eligió después de ver los datos. El control correcto es el max-estadístico: **p = 0,14**.

---

## 5. Controles, resultados negativos y corrección múltiple

**Batería de pruebas de orden (Holm, m = 6):**

| Prueba | p | Holm |
|---|---|---|
| T1 macro: emparejamiento por rangos vs composiciones | 0,239 | 0,569 |
| T2 micro: V color~nombre, orden del documento | 0,182 | 0,569 |
| T3 micro: precisión color→nombre in-sample | 0,021 | **0,125** |
| T4 micro: precisión held-out | 0,322 | 0,569 |
| T5 max-AMI sobre 72 pares nombre × grupo | 0,142 | 0,569 |
| T6 orden invertido (V) | 0,073 | 0,365 |

Ninguna sobrevive Holm al 5 %.

**Controles negativos:**

1. **Emparejamientos equivocados (720):** la V observada (0,583) está en el percentil 0,38 de las asignaciones alternativas (media 0,596; máximo 0,688); la precisión (0,438) en el percentil 0,30 (media 0,462). El emparejamiento propuesto es **peor que el promedio** de emparejamientos alternativos.
2. **Desplazamientos:** la V en el desplazamiento 0 es 0,583; con desplazamiento +4 es **0,652**, con −4 es 0,594, y con el orden invertido **0,602** (p = 0,073). Si el orden importara, el desplazamiento 0 debería ser el mejor; no lo es. El máximo sobre 11 alineaciones no es corregible a significación.
3. **Tests por quipu:** 6 pruebas, ninguna sobrevive Holm; la única con p < 0,05 (UR092) queda explicada por el ciclo de 5 colores.
4. **Sin el nombre más frecuente:** el exceso de precisión baja de 0,041 a 0,036 y deja de ser nominalmente significativo (p = 0,098): el «efecto» dependía de que «juo» es el 25 % de la muestra.
5. **H-macro:** el p = 0,0056 de las 720 permutaciones es un artefacto de condicionar en los tamaños observados; con el nulo correcto (composiciones) es 0,24.
6. **Tendencia de la posición 1 con la posición en la lista:** sin tendencia global (Fisher combinado Z = −1,25, p = 0,21). Los dos únicos trends nominales van en direcciones opuestas (Namus ρ = −0,85, que es el bloque de ceros; Corongo ρ = +0,53, p = 0,03), lo que es la firma de ruido, no de un orden compartido.
7. **Recuento de nombres vs colores:** la comparación marginal que usan Medrano y Urton (30 nombres de pila distintos y 14 singletons frente a 32 colores y 17 singletons) **no se reproduce con una normalización directa**: obtengo 40 distintos / 24 singletons sin normalizar, 37/21 quitando títulos y 34/17 con una normalización agresiva (quitar «don»/«d.», agrupar «leon …», «juco»≈«juo»). El 34/17 se acerca al 33/17 de los colores, así que la comparación puede ser correcta con *su* normalización; pero en cualquier caso **es una coincidencia de recuentos, no una prueba de correspondencia ni de orden**.

**Sobre KH0227 y UR198:** son «Santa» solo en el nombre del fundo o del pueblo. UR198 (Santa Clara, Nazca) tiene 257 colgantes en 40 grupos espaciales, de los cuales solo 9 son de seis cuerdas; KH0227 (Huaura) tiene 168 colgantes y 7 grupos de seis. Ninguno pertenece al archivo Radicati, ninguno tiene padrón asociado y sus patrones de color no son comparables (UR198 agrupa por 4, KH0227 mezcla 6/15/16). No se pueden usar para probar la hipótesis; usarlos sería un falso positivo de «procedencia».

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| El archivo del Santa son 6 quipus con 133 grupos de seis cuerdas, distribuidos 48/9/34/17/15/10 | **demostrado** (KFG = Apéndice B = tabla 12.3) |
| 33 colores distintos y 17 singletons en las primeras cuerdas | **demostrado** (reproduce 32/17 publicado) |
| En UR087 el color de la primera cuerda es una seriación de período 4; en UR092, de período 5 | **demostrado** (descriptivo, exacto) |
| El padrón tiene 130 nombres en 6 pachacas con los conteos publicados y un bloque de 5 «hijo de» al final de Namus | **demostrado** |
| **No hay correspondencia de orden entre nombres y grupos más allá del azar** | **apoyado con datos** (n = 121; V p = 0,18; held-out p = 0,32; max-AMI p = 0,14; Holm no significativo) |
| El emparejamiento pachaca↔quipu de la tabla 12.3 no es evidencia (es la asignación por rangos) | **apoyado con datos** |
| El color de la primera cuerda codifica el nombre de pila (Medrano y Urton 2018) | **propuesto**, no apoyado aquí: el orden no se alinea y en 44 % de los grupos el color es periódico |
| La unión R/V codifica la mitad de moiedad | **propuesto** (descriptivo consistente: 5 de 6 quipus uniformes; no probado) |
| Cualquier identificación nombre↔grupo concreta («este grupo es Juo Chauca») | **especulativo** |

**Límite y potencia:** incluso permitiendo ajustar el mapeo color→nombre sobre los mismos datos, la mejor concordancia es 0,438 (azar 0,397): la alineación observada no puede explicar más del **44 %** de las posiciones, y fuera de muestra explica el 11,7 % (azar 9,2 %). Se excluye una lista paralela fiel; **no** se excluye una correspondencia muy ruidosa (más de la mitad de las posiciones mal) ni un orden parcial que afecte solo a un subconjunto de grupos.

---

## 7. Qué haría falta para resucitar la hipótesis

1. **El documento original con la disposición de la lista** (columnas, folios, marcas): el OCR del Apéndice A no permite saber si el orden es lineal o columnar, y la hipótesis es sensible a ello.
2. **Un orden de quipus independiente** (orden de hallazgo, numeración de Radicati, inventario del museo): sin él, H-macro es circular.
3. **Un rasgo del nombre con estructura conocida** (p. ej., edad, estado civil, obligación tributaria) que el quipu pudiera codificar en las posiciones 2–6. La posición 1 no sirve: el documento dice que todos pagan lo mismo (2 pesos, 7 reales, 3 quartillos) y los valores 0–13 la contradicen.
4. **Leer UR087 como tabla de 4 columnas** (12 × 4) en lugar de lista lineal: si el khipu se lee por columnas, la comparación de orden tendría que rehacerse con ese orden, y el padrón tendría que tener una estructura de 4 columnas equivalente (no la tiene).

---

## 8. Para el coordinador

- **La hipótesis de orden no se sostiene.** Las 121 posiciones alineadas (de 133 grupos) dan V = 0,583 (p = 0,18); el único p nominal (precisión color→nombre, 0,021) muere con Holm (0,125) y **desaparece fuera de muestra** (0,117 frente a 0,092; p = 0,32).
- **El «p = 0,0056» del emparejamiento pachaca-quipu es circular:** solo 4 de 720 asignaciones alcanzan el mínimo, porque la tabla 12.3 es la asignación por rangos elegida *post hoc*. El nulo correcto (composiciones de 133 en 6) da **p = 0,24**.
- **Hallazgo estructural nuevo y sólido:** en UR087 (48 grupos) el color de la primera cuerda es una **seriación de período 4** —las últimas 6 filas de 4 grupos son casi idénticas (5 exactamente W | RB | AB | YB); en UR092 hay un ciclo estricto de 5 colores. En 58/133 grupos (44 %) el color es posición, no identidad. Eso explica por sí solo por qué «color = nombre de pila en orden» falla en el quipu más grande.
- **El único bloque sugerente** es Namus: 5 «hijo de» al final de la lista y 6 grupos con posición 1 = 0 al final de UR091. Es una coincidencia cualitativa real, pero los tamaños no coinciden (5 vs 6), los límites están desfasados ~2–4 posiciones y el max-estadístico corregido da **p = 0,14**. No es evidencia.
- **El orden de los nombres del padrón es casi arbitrario:** no hay agrupación por apellidos (0,09 en Corongo, p = 0,06; 0,00 en las demás). Solo hay una agrupación deliberada (los dependientes de Namus), lo que reduce mucho lo que un quipu podría estar replicando.
- **La comparación 30 nombres / 32 colores no se reproduce** con una normalización directa (40/24 sin normalizar; 34/17 con normalización agresiva). Aun reproduciéndola, es una coincidencia de recuentos, no una prueba de correspondencia.
- **UR198 y KH0227 no son del valle del Santa** (Santa Clara de Nazca y Huaura). Si los equipos 11/12 los incluyeron por el campo `procedencia`, hay que corregirlo: no tienen padrón y su estructura no es la del archivo Radicati.
- **Recomendación:** cerrar la línea «orden de nombres ↔ orden de grupos» y redirigir el esfuerzo a (a) la estructura de color por columnas de UR087/UR092 (¿es un formato de tabla?), (b) la unión R/V como marcador binario (descriptivo consistente, 63/69), y (c) conseguir el folio original del padrón antes de cualquier nueva prueba de alineación.
