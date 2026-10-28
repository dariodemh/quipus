# Tanteo disciplinado: lecturas concretas del archivo de maní de Incahuasi

**Equipo:** tanteo (n_tanteo) · **Fecha:** 2026-10-18 · **Datos:** `analisis/ds/n_okr_incahuasi/cuerdas_okr.csv` (2 584 cuerdas de los 14 quipus del montón de maní).

## 1. Pregunta

¿Podemos adivinar **lecturas contables concretas** de los 14 quipus que estaban juntos, cubiertos de maní, en la kallanka U.A.4 de Inkawasi (UR266, 268, 269, 270, 272, 273A/B, 274A/B, 275, 276, 277, 278, 279), y **sobreviven** esas lecturas cuando se prueban una sola vez en registros que no se usaron para inventarlas?

## 2. Partición (fijada antes de mirar valores)

`particion.csv`. Unidad = **registro** (grupo de colgantes). División por **bloques contiguos**: la mitad inicial de los grupos de cada quipu explora, la final confirma. Se eligió por bloques, y no pares/impares, porque las hipótesis de libro (H-a, H-d) dependen del orden. UR276 y UR279 tienen un solo grupo: allí la unidad es el colgante y se parte por `orden`.

| Quipu | registros | cuerdas | Quipu | registros | cuerdas |
|---|---:|---:|---|---:|---:|
| UR266 | 36 | 174 | UR274A | 31 | 94 |
| UR268 | 33 | 169 | UR274B | 33 | 133 |
| UR269 | 107 | 330 | UR275 | 26 | 125 |
| UR270 | 25 | 381 | UR276 | 1 | 15 |
| UR272 | 26 | 362 | UR277 | 19 | 247 |
| UR273A | 34 | 87 | UR278 | 37 | 322 |
| UR273B | 32 | 124 | UR279 | 1 | 21 |

La partición se escribió **antes** de imprimir cualquier valor; solo se usaron ids de grupo, orden y número de cuerdas.

## 3. Método

- **Registro:** grupo de colgantes (`nivel=0`). Cabecera = primer colgante; resto = componentes. En UR273A/B y UR274A/B la cabecera suele estar en blanco y el valor principal es el máximo del grupo.
- **Nulo:** permutación dentro de la mitad correspondiente y del mismo quipu, preservando tamaños y totales. 4 000 permutaciones en exploración (200 en el nulo aproximado de H13) y 8 000 en confirmación; semillas fijas (20261018 y 771013).
- **Corrección:** Holm sobre **m = 16** hipótesis registradas (no sobre las 5 pruebas que llegaron a confirmación). Los p de permutación tienen un mínimo de 1/8 001 ≈ 0,000125; se reporta como p < 0,0002.
- **Registro previo:** `hipotesis.csv` (16 hipótesis, 53 variantes, con regla exacta y predicción). Las reglas que pasaron exploración se congelaron en `congeladas.csv` antes de tocar confirmación. `exploracion_resultados.csv` y `confirmacion.csv` guardan las salidas.

## 4. Resultados

### 4.1 El registro es un depósito repartido: cabecera = cuota fija + destinos (H06, H16) — **sobrevive**

La identidad `cabecera = suma(cuerdas no cabecera)` se cumple mucho más de lo esperado por azar en las dos mitades:

| Prueba | Mitad | Registros | Aciertos | Esperado nulo | p |
|---|---|---:|---:|---:|---:|
| H06 exacto, UR275 | explorar | 13 | 2 | 0,23 | 0,0175 |
| H06 exacto, UR269 | explorar | 32 | 6 | 0,23 | 0,0002 |
| **H06 exacto, UR275** | **confirmar** | **12** | **8** | **0,66** | **<0,0002** |
| **H06 exacto, UR269** | **confirmar** | **30** | **10** | **0,47** | **<0,0002** |
| **H16 error <5 %, UR275** | **confirmar** | **12** | **12** | **0,094** | **<0,0002** |
| **H16 error <5 %, UR269** | **confirmar** | **30** | **20** | **0,066** | **<0,0002** |

Holm (m=16): **0,002** para las cinco pruebas. Todas siguen siendo significativas.

**Confusor importante (post hoc, `estratos.csv`).** La mitad de confirmación de UR275 está dominada por registros de 3 cordones (cabecera + 47 + un destino: 9 de 12). En ésos la identidad es casi tautológica. Al estratificar por número de destinos:

| Registros con ≥3 destinos | Registros | Exactos | Dentro del 5 % |
|---|---:|---:|---:|
| UR275 (ambas mitades) | 16 | 3 | **15/16** |
| UR269 (ambas mitades) | 13 | 0 | **1/13** |

Lectura honesta: el reparto **se sostiene en UR275** (15 de 16 registros complejos dentro del 5 %; los residuos van de 0 a 62 unidades, ≤4,7 %, compatibles con redondeo/transcripción), pero **no en los registros complejos de UR269** (1 de 13). El único fallo de UR275 es g8 (2633): le falta un destino de 2 002 y sólo suma 631. UR269 usa otro formato, como ya sabíamos por los bloques de 5; no se puede leer con la misma regla. Aviso de potencia: en la mitad de confirmación de UR275 sólo hay **3 registros complejos** (los tres dentro del 5 %), así que la confirmación fuerte del reparto complejo es limitada; la evidencia principal es la suma de ambas mitades.

### 4.2 La cuota es fija por quipu, no proporcional al depósito (H05) — **apoyado, hipótesis proporcional falsada**

- UR275: en los 24 registros que llevan el cordón 47, la tasa 47/cabecera va de **1,10 % a 3,68 %** (media 2,29 %).
- UR268: en los 19 registros con 208, la tasa va de **1,38 % a 2,92 %** (media 2,19 %).
- El 2 % de Urton & Chu 2018 es, por tanto, **el promedio de una cuota fija**, no una regla de cálculo: con cabeceras de 1 278 a 4 273, una cuota proporcional al 2 % habría oscilado entre 26 y 85; la cuerda dice 47 (o 40 en un registro) en casi todos.
- En UR269 la tasa aparente es mucho más dispersa (media 8,4 %, máx. 209 %), otra señal de que su formato no es el mismo libro.

### 4.3 Las 9 partes son proporciones fijas, no novenos iguales (H07, H15) — **sobrevive**

Perfil medio de las 9 columnas de UR278, ajustado **sólo con las 17 filas de exploración** (es el que se congeló y se usó para predecir):

| c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 13,5 % | 13,6 % | 8,7 % | 10,7 % | 11,6 % | 12,5 % | 12,4 % | 8,7 % | 8,3 % |
| ±2,7 | ±2,9 | ±1,7 | ±1,8 | ±3,6 | ±2,2 | ±2,4 | ±3,4 | ±2,6 |

(Con las 26 filas completas el perfil es casi idéntico: 13,8; 14,4; 9,5; 10,8; 11,0; 12,9; 11,0; 8,0; 8,7 %. La tabla usa las 17 de exploración para no contaminar la confirmación.)

- Ajustado en 17 filas de exploración y probado en 9 filas de confirmación: **MAE = 40,4** por celda, frente a **50,1** de los novenos iguales y **58,3** del nulo que baraja las columnas de cada fila (p < 0,0002; Holm 0,002).
- El perfil no es un artefacto del tamaño: las filas grandes y pequeñas dan perfiles casi iguales (ρ = 0,817). El CV dentro de fila es 0,278.
- UR270 y UR278 comparten el mismo perfil (ρ = 0,833; p = 0,0045), y la celda de UR278 = colgante + subsidiaria de UR270 en **5 de 7** grupos de exploración (control positivo H14).
- **Negativo útil:** ninguna fila tiene las 9 columnas ordenadas de mayor a menor (0/26), así que no son valores ordenados por tamaño: son **categorías fijas**.
- UR270 no tiene ninguna fila de 9 cordones en la mitad de confirmación (todas caen en la primera mitad), así que H07 sólo pudo confirmarse en UR278; UR270 queda como replicación exploratoria.

### 4.4 No hay dinámica de saldo (H01–H04) — **negativo claro**

Cero transiciones exactas en las 63 transiciones probadas:

| Hipótesis | Transiciones | Exactas | p |
|---|---:|---:|---:|
| H01 UR273B = saldo que se mueve con UR273A | 9 | 0 | 1,0 |
| H02 UR274B = saldo que se mueve con UR274A | 8 | 0 | 1,0 |
| H03 cabeceras de UR275 acumuladas | 12 | 0 | 1,0 |
| H04 cabeceras de UR269 acumuladas | 34 | 0 | 1,0 |

UR273A/B y UR274A/B **no son stock y flujo**: son dos componentes aditivas del mismo depósito (la suma A+B da la cabecera del libro, ya bien apoyado en `13_sistema_incahuasi`). Nuestro test añade que **tampoco** son un saldo que se actualiza paso a paso, ni en el libro.

### 4.5 La escalera de copias (H09) — **especulativo, y más débil de lo que parecía**

Existe un solo triplete con paso +100: 2433 (UR269, p181) → 2533 (suma de la fila g12 de UR278) → 2633 (UR266 p64 y UR275 p41). Pero **2633 también está en UR269 (p89, grupo 27)**, así que no es una cadena lineal de tres eslabones: pueden ser tres registros distintos separados por 100. No hay herencia de errores que permita fijar la dirección. Se queda en especulativo.

### 4.6 UR277, UR272, UR276, UR279 — **negativos y descripción**

Ninguna de las reglas de suma se cumple:

| Prueba | Resultado |
|---|---|
| H10 UR277: cordón grande = suma de los pequeños | 0/8 grupos (p = 1,0) |
| H11 UR272: primer cordón = suma del resto | 2/11 (p = 0,34) |
| H12 UR276: colgante = s1+s2 | 1/5 |
| H13 UR279: valores = totales de otro quipu | 5/12, pero el nulo da 12/12 (los valores son redondos y comunes) |

Descripción cuantitativa:

- **UR277:** 150 cordones; 93 % ≤ 60; mediana 18; p10–p90 = 0–30; 9 cordones > 100 (máx. 1 167). Es una **lista de conteos pequeños** (¿jornales, personas, días?) con algunos subtotales grandes, no un libro de depósitos.
- **UR272:** 173 cordones; **100 % ≤ 60**; mediana 2; p90 = 10; máx. 54. Es una **lista de conteos unitarios** (¿unidades, sacos, personas?) sin totales.
- **UR276:** 5 colgantes con valores 8, 24, 17, 15, 5, cada uno con dos subsidiarias (4+4, 7+1, 8+3, 5+3, 1+1). La suma padre = hijas sólo en el primero. Parece una **etiqueta/registro corto**, no un libro.
- **UR279:** 12 colgantes (69, 46, 157, 65, 160, 100, 106, 63, 65, 11, 12, 39) con subsidiarias; todos los hilos NB. Es una **lista corta de totales**, sin relación exacta con los totales del resto del montón.

## 5. Controles, corrección y límites

1. **Nulo explícito** en todas las pruebas (permutación dentro de quipu y mitad). Los p de confirmación están en el mínimo alcanzable; se reportan como < 0,0002, no como 0.
2. **Holm m = 16** (todas las hipótesis registradas, incluidas las que fallaron). Las cinco pruebas confirmadas quedan en 0,002.
3. **Confusor de complejidad** (sección 4.1): la confirmación de UR275 es más fácil que su exploración. Al estratificar, la lectura se sostiene en registros complejos de UR275 (15/16) y **falla** en los de UR269 (1/13). Esto se detectó después de confirmar y se reporta como límite, no como nuevo hallazgo.
4. **H08 se excluyó**: su formulación habría usado la mitad de confirmación para explorar. No cuenta como confirmación; se menciona sólo como consistencia descriptiva (ρ = 0,683; p = 0,029).
5. **UR270 no confirmó** H07 (sin filas de 9 en la segunda mitad). Es una replicación exploratoria, no confirmatoria.
6. **N = 14 quipus**, pero las pruebas son a nivel de registro dentro de cada quipu; no se mezclan cuerdas de quipus distintos salvo en los controles H14/H15.
7. **H12 y H13** se evaluaron sobre el quipu completo (UR276 y UR279 tienen un solo grupo, sin división posible). Ambos fallaron, así que no afectan a la corrección; H13 además tiene un nulo poco informativo (los valores son redondos y el nulo esperaba 12/12 coincidencias).
8. **H01/H02** se probaron con el emparejamiento A_i–B_i por índice de grupo. Un segundo alineamiento por orden de grupos no vacíos da también **0 aciertos**; el negativo no depende de esa elección.

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| En UR275 el registro es un depósito: cabecera = cuota fija + destinos (15/16 registros complejos dentro del 5 %) | **Apoyado con datos** |
| La cuota es fija por quipu (47; 208), no proporcional; el 2 % es un promedio | **Apoyado con datos** |
| Las 9 partes de UR278 son proporciones fijas y predicen filas no vistas (MAE 40,4 vs 50,1) | **Apoyado con datos** |
| Las 9 columnas son categorías estables, no valores ordenados por tamaño | **Apoyado con datos** |
| UR270 y UR278 comparten el mismo perfil y la celda = colgante + subsidiaria | **Apoyado con datos** (control) |
| UR273A/B y UR274A/B no son saldo/movimiento, sino componentes aditivas | **Apoyado con datos (negativo fuerte)**: 0/17 transiciones para las reglas probadas |
| El mismo reparto vale para los registros complejos de UR269 | **Falsado** (1/13) |
| Las 9 partes son poblaciones o unidades concretas (no sólo proporciones) | **Propuesto** |
| UR277 = jornales/leva; UR272 = conteo de unidades | **Propuesto** |
| La escalera 2433→2533→2633 fija la dirección de copia | **Especulativo** |
| UR279 = lista de totales de otros quipus | **Especulativo** |

## 7. Lectura contable concreta (la que sobrevive)

- **UR275 (y su copia UR266, peor conservada):** cada grupo es **una entrega de maní**. La cuerda 1 es el **total del depósito** (1 278–4 273 unidades). La cuerda 2 es la **retención fija** (47; 40 en un registro). Las cuerdas 3–n son los **destinos del reparto** (2–6 por registro); su suma reproduce el total (15/16 registros complejos dentro del 5 %; residuos de 0 a 62 unidades, salvo g8, al que le falta un destino de 2 002). El registro no es un saldo: es un reparto cerrado.
- **UR278:** cada fila es **ese mismo depósito desglosado en 9 unidades fijas**. Las 9 cuerdas no son novenos iguales: cada columna tiene una cuota estable (13,5; 13,6; 8,7; 10,7; 11,6; 12,5; 12,4; 8,7; 8,3 %). La fila se puede predecir desde el total y el perfil (MAE 40,4 frente a 50,1 de los novenos iguales). Cada celda es la suma de un colgante y su subsidiaria de UR270.
- **UR270:** es el **detalle** de esas 9 unidades (colgante + subsidiaria por unidad); no añade una décima parte.
- **UR273A/B y UR274A/B:** no son un libro de saldos. Son **dos mitades aditivas** del mismo depósito (A pequeña en centenas, B grande en miles; cuotas 30 + 17 = 47).
- **UR268:** el mismo formato de libro, con **cuota fija 208** (2,2 % medio; 1,4–2,9 %), sobre depósitos de 7 000–15 000.
- **UR269:** libro maestro con **bloques de 5 flujos**; sus registros simples (cabecera + cuota + un destino) siguen el reparto, pero sus registros de 4–5 cordones **no** (1/13). Es un formato distinto, no una copia de UR275.
- **UR277 y UR272:** listas de **conteos pequeños** (medianas 18 y 2), no totales de depósitos. **UR276 y UR279:** etiquetas o listas cortas; su papel en el montón sigue sin leerse.

## 8. Para el coordinador

- **Lo que sobrevive a confirmación:** (1) el registro de UR275 es un depósito repartido —cabecera = cuota fija + destinos— con 15/16 registros complejos dentro del 5 %; (2) las 9 partes de UR278 son proporciones fijas que predicen filas no vistas (MAE 40,4 vs 50,1 de novenos iguales, p < 0,0002; Holm 0,002); (3) cuota fija, no 2 % proporcional.
- **El 2 % de Urton & Chu es un promedio, no una regla:** 47/2 257,8 = 2,1 % en promedio, pero la tasa por registro va de 1,1 % a 3,7 % porque la cuota es constante. Conviene decirlo así en el museo.
- **Confusor detectado:** la mitad de confirmación de UR275 son registros de 3 cordones, donde la identidad es casi tautológica. Al estratificar, el reparto se sostiene en UR275 (15/16) pero **falla en los registros complejos de UR269 (1/13)**. No unificar los dos formatos.
- **Negativo fuerte:** no hay dinámica de saldo en 273A/B, 274A/B ni en las cabeceras de 275/269 (0/63 transiciones exactas). A/B son componentes aditivas, no stock/flujo.
- **La escalera 2433→2533→2633 es más débil de lo que parecía:** 2633 también está en UR269 (p89), así que no es una cadena lineal de tres eslabones. Sin herencia de errores no se puede fijar la dirección; queda especulativo.
- **UR277 (mediana 18, 93 % ≤ 60) y UR272 (mediana 2, 100 % ≤ 60) no son totales:** son listas de conteos. UR276 (5 registros) y UR279 (12 colgantes) siguen sin papel claro.
- **UR270 no pudo confirmar** el perfil de 9 partes (todas sus filas de 9 cayeron en exploración). Es replicación exploratoria (ρ = 0,833), no confirmatoria.
- **Siguiente ronda sugerida:** (a) separar por formatos antes de cualquier prueba conjunta; (b) buscar el ancla documental de las 9 unidades (¿9 almacenes, 9 ayllus, 9 días?); (c) atacar UR269 con la regla de bloques de 5 en vez de la regla de reparto; (d) no gastar más pruebas en UR277/272 hasta tener un ancla externa.
