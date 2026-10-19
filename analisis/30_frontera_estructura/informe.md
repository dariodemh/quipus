# 30. La frontera: ¿hay estructura que los detectores existentes no ven?

**Pregunta.** El atlas (28) deja 180 quipus como «listas decimales sin estructura detectada». ¿Muestran estructura que los detectores ya usados (sumas internas, copias, formularios, tablas, asignación, tally, plantillas) no buscan? Si la muestran, ¿qué estructura es, a qué género se acercan y cuántos dejan de ser frontera?

**Respuesta corta.**

- Con el diseño congelado salen 22 quipus.
- Con un nulo más estricto, añadido después de ver los datos (Enmienda 3; solo puede quitar hallazgos), salen **3**: UR040, UR167 y UR1033F. Los tres tienen la misma estructura: **pares de cuerdas de dos colores intercalados** (A/B/A/B).
- Un cuarto, **UR122**, tiene totales por columna; queda «propuesto» por las reglas, pero queda **apoyado post hoc** porque su copia completa, KH0049, contiene la misma tabla jerárquica.
- Casi todas las relaciones entre quipus que parecían nuevas se explican por la autocorrelación local de cada lista; no muestran un vínculo con un compañero concreto.

## 1. Muestra y diseño

- **Frontera:** filas de `atlas.csv` con `genero == SIN` y evidencia «decimal sin estructura detectada» (180). Se excluyen los 113 de datos insuficientes.
- **División:** estratificada por transcriptor (UR, AS, resto), con semilla 20261018. Quedan 89 quipus en A (exploración) y 91 en B (confirmación).
- `diseno.md` se escribió antes de correr nada. Tiene tres enmiendas, cada una fechada y motivada:
  1. T1 y T6: se añadieron subestadísticos, porque los controles sintéticos fallaban. Fue antes de ver datos reales.
  2. I1–I4: se cambió el estadístico a la cobertura por tramos, que tolera huecos, porque el control HP055/UR1084 fallaba. También fue antes de ver datos reales.
  3. Nulos por tramos y por bloques de subsidiarias. Fue **después** de ver los resultados; es conservadora.
- **16 pruebas por quipu:** 7 internas (T1–T7) y 9 entre quipus (I1–I9). Son 2509 pruebas con datos y 371 NA.
- **Compañeros:**
  - para I1–I7: los otros 179 de la frontera, más el mismo museo (normalizado) y el mismo sitio;
  - para I8 e I9: el mismo sitio o, si no se conoce, el mismo museo.
  - Se excluyen los pares que son el mismo objeto (UR1107/UR237, AS125/UR247 y KH0033/UR044).
- **Valores p:**
  - por permutación con escalada Besag–Clifford: hasta 99 999 réplicas en las internas, y hasta 19 999 o 99 999 entre quipus, con un presupuesto de 300 s;
  - BH y Holm sobre **todas** las pruebas a la vez (las 2509);
  - en A, una familia se promueve si tiene algún BH(A) < 0,10 o exceso binomial;
  - en B se replica si el exceso binomial pasa Holm o hay algún BH confirmatorio < 0,05.
- **Niveles** (detalle en `diseno.md`):
  - *demostrado:* Holm global y la familia se replica;
  - *apoyado:* q global < 0,05 y la familia se replica;
  - *propuesto:* q < 0,05 sin réplica de la familia;
  - *especulativo:* p < 0,01.

## 2. Controles positivos

| Control | Resultado |
|---|---|
| Sintéticos internos, uno por prueba (periodo 5, colores con periodo 4, tramo repetido, grupos ordenados, subsidiaria = colgante/10, totales por posición, pares espejo que suman 50) | 7 de 7 con p ≤ 0,005 (`controles_internos.csv`) |
| I2: UR1107 invertido frente a UR237 | p = 5e-4, 15 posiciones cubiertas |
| I1: UR1084 frente a HP055 | p = 5e-4, 125 posiciones cubiertas |
| I8: totales de UR278 en Incahuasi | p = 1e-5 (UR266, 12 grupos) |
| Las dos copias bajo el nulo estricto de la Enmienda 3 | p = 5e-4 y 5e-4 (`controles_bloque.csv`): el nulo estricto **no** mata las copias reales |

## 3. Resultados globales

| | p < 0,05 | p < 0,01 |
|---|---|---|
| Frontera real, diseño congelado (2509 pruebas) | 242 | 114 |
| Esperado por azar | 125 | 25 |
| Frontera nula 0 (cada F permutado; compañeros reales) | 57 | 11 |
| Frontera nula 1 | 78 | 17 |
| Internas solas, 5 réplicas nulas (de 1014) | 30–49 | 4–8 |
| Frontera real tras la Enmienda 3 | 133 | 50 |

**Decisión con el diseño congelado** (`frontera_estructura_sin_enmienda3.csv`, `salida_03_decision_sin_enmienda3.txt`):

- Salen **22 quipus**, con Σq = 0,70 en las filas que los sacan.
- Familias replicadas: T2, T3, T5, I1, I2, I3, I4 e I6.
- En las dos fronteras nulas no sale **ninguno** (0 y 0).

**Por qué no basta con eso.**

- La frontera nula permuta F entero, así que destruye a la vez la señal y cualquier estructura local. Por eso no puede medir si la estructura local de F imita una relación.
- Al mirar las filas aparecieron dos confusiones:
  1. **Rachas y escalones dentro de F.** Valores iguales seguidos, o 1-2-3 (que `tol` empareja), producen «copias», «diferencias constantes» y «razones» con cualquier compañero que también tenga rachas.
  2. **Subsidiarias hermanas y magnitud por grupo.** Inflan T5.
- **Enmienda 3.** Las filas de T3, T5, I1–I4 e I6 con p < 0,05 se recalculan con nulos que conservan esa estructura:
  - en T3 e I1–I4 e I6, los tramos de valores consecutivos tol-iguales se permutan como bloques;
  - en T5, el conjunto de subsidiarias de un colgante se mueve entero a otro colgante del mismo grupo.
  - Se toma p = max(p, p_bloque); como p solo sube, BH y Holm siguen siendo válidos.
- **Filas con p < 0,05 antes y después:**

  | Familia | Antes | Después | Esperado |
  |---|---|---|---|
  | I1 | 22 | 11 | 8,9 |
  | I2 | 31 | 16 | 8,9 |
  | I3 | 30 | 7 | 8,9 |
  | I4 | 24 | 6 | 8,9 |
  | I6 | 18 | 9 | 8,9 |
  | T3 | 28 | 7 | 8,5 |
  | T5 | 23 | 11 | 4 |

- **Decisión final** (`frontera_estructura.csv`, `familias.csv`):
  - Solo se replica T2: q confirmatorio mínimo en B = 0,0027.
  - **Salen 3 quipus** (Σq = 0,027).
  - Otros 6 quedan como propuestos y 41 filas como especulativas.
  - Fronteras nulas con la misma regla: 0 y 0.

## 4. Lo que se buscó y lo que se encontró

### 4.1 Relaciones entre quipus (I1–I7): negativo casi total

**Copia con tolerancia (I1).**

- Sobrevive UR1118 ≈ UR218, ya conocida por 04: p_bloque = 5e-4; queda en «propuesto» porque la familia no se replica.
- AS207B ~ UR016 (p_bloque = 2e-4) no pasa BH.

**Invertida (I2).**

- Ningún quipu individual llega a q < 0,05.
- Hay un exceso agregado débil tras la Enmienda 3: 16 de 177, frente a 8,9 esperados (binomial p = 0,017). La familia no se promovió en A (8 de 88).
- El único caso real de inversión que conocemos (UR1107/UR237) es el mismo objeto leído dos veces.

**Diferencia constante (I3) y razón (I4).**

- Caen al azar: 7 y 6 de 177.
- La mejor, QU017 ~ UR016 (diferencia; p_bloque = 5e-4), **no es específica**. QU017 puntúa casi igual con UR016 (36,8), AS093 (29,1), QU002 (28,2) y UR056A (27,5). Es una propiedad de QU017, no un vínculo.
- AS207B ~ MM004 (razón 2) eran rachas 10,10,10 ↔ 20,20,20: cae con p_bloque.

**Grupos permutados (I5).** 1 caso en 141 (UR057 ~ UR076, p = 0,0015): no se replica.

**Sumas de bloque (I6 e I7).**

- I6 en UR1049 (77 aciertos) se alcanza igual con UR034 y QU011: no es específico.
- I7: 0 de 157 con p < 0,05.

### 4.2 Relaciones jerárquicas débiles (I8 e I9): negativo

- Ninguna familia se promovió: I8 tuvo 2 de 79 en A e I9 0 de 67.
- El mejor I9 (AS093 ← UR1088, p = 2,5e-4) es un artefacto del estadístico. UR1088 tiene 10 grupos que suman 15, y AS093 contiene un 15.
- **No hay totales de grupo de la frontera que reaparezcan en otro quipu del mismo sitio** más de lo que da el azar.

### 4.3 Estructura interna

**T1, periodicidad de valores: negativo.** 3 de 78 en A.

**T2, periodicidad de la partición de color: positivo, la única familia replicada.**

- Las tres filas que sacan quipus son alternancias de desfase 2:

  | Quipu | Colores | Posiciones en alternancia | q global | Holm |
  |---|---|---|---|---|
  | UR040 | W/AB | 26 de 33 | 0,008 | 0,025 |
  | UR167 | AB/MB | 30 de 37 | 0,008 | 0,025 |
  | UR1033F | W/AB | 17 de 21 | 0,010 | 0,050 |

- Seguimiento en todo el corpus (`06_alternancia.py`, 515 quipus con ≥ 2 colores): 19 alternan con desfase 2 (q < 0,05):
  - 6 TAB, 5 FOR, 1 ASG, 1 SEG y 6 SIN;
  - se concentran en el Peabody: 5 de 12, frente a 14 de 503 en el resto (Fisher p = 2,6e-5, descriptivo). Están entre ellos UR1033C y UR1033D, del mismo lote que UR1033F.
- En los que tienen valores, **un color domina al otro dentro del par**:
  - UR1033F: AB > W en 14 de 16 pares (p = 0,004);
  - HP022: W > MB en 14 de 14;
  - AS174: W > LB en 12 de 12;
  - AS062: KB > W en 13 de 15.
- Es una tabla de dos columnas escrita intercalando (unidad = par, columna = color). Se acerca a TAB/FOR, aunque el detector de tablas, que busca grupos R × K, no la ve.
- En UR040 y UR167 los valores son casi todos 0 o 1: el formato es seguro, el contenido no.

**T3, subsecuencias repetidas: la señal cae con el nulo por tramos.** Quedan 3 especulativos: UR005 (p_bloque = 5e-4), UR1116 (0,0019) y AS090_N2 (0,005).

**T4, tendencias monótonas por grupo.**

- Hay exceso agregado: 23 de 154 con p < 0,05 frente a 7,7 esperados (p = 3e-6).
- La familia **no se replica** en B: 9 de 77, Holm 0,12.
- **Es frágil al transcriptor:** UR1107 da p = 3e-5, pero su doble UR237 (el mismo objeto con otra segmentación en grupos) da p = 0,096. Propuesto: UR1107 y JC011.

**T5, subsidiaria como ajuste de su colgante.**

- Con el nulo de bloques dentro del grupo sigue habiendo exceso agregado: 11 de 81 frente a 4 esperados (p = 0,002). La familia **no se replica** en B (Holm 0,066).
- Por quipu:

  | Quipu | p_bloque | Nivel |
  |---|---|---|
  | UR016 (Leymebamba) | 1e-5 | propuesto |
  | UR093 (Santa) | 5e-4 | especulativo |
  | HP011 (Pachacamac) | 7e-4 | especulativo |
  | UR122 | 8e-4 | especulativo |
  | UR1130 | 0,004 | especulativo |

- La forma es una **escala, no una fracción fija**: el subestadístico ganador es siempre ρ de Spearman (0,38–0,87), nunca la razón modal. En UR016, la subsidiaria es menor que el colgante en el 90 % de los pares, con una razón mediana de 0,20.
- Esto es compatible con el negativo de `ds/n_quipus_modernos`: no hay una «cría proporcional» con razón fija en el corpus.

**T6, cuerda = suma de bloque no contiguo: UR122 (Holm 0,025).**

- En UR122, p2 = 457 + 951 + 875 y p9 = 447 + 855 + 972: la misma posición en los grupos 2–4. p1 = 15652 frente a 15649 de la suma.
- La familia no se replica (es rara), así que por reglas queda «propuesto».
- **Seguimiento post hoc** (`07_ur122_kh0049.py`) en KH0049, su copia completa (04 y 14):
  - KH0049 es una **tabla jerárquica de tres niveles**: B0 = B1 + B2 en 14 de 18 posiciones exactas, y B1 = B3 + B4 + B5 en 7 de 18 (8 con tolerancia). En los dos casos, la media nula es menor que 1 y p = 5e-5.
  - UR122 es la sección del subtotal (B1, B3, B4, B5) de esa tabla, con el 58 % de las cuerdas rotas.
  - La discrepancia 15652/15649 está **en las dos copias**, y B0 − B2 = 15649. Es un error o un ajuste del original, como el 2904/2908 de Puruchuco, no un error de transcripción.
  - 10_tablas decía «columna-total solo en Incahuasi». Esto es un segundo caso, de la costa sur (Nazca, Göteborg/Lima). 08 ya tenía KH0049 como candidato IDX (q = 0,07).

**T7, pares que suman lo mismo: no se replica.** UR076: 8 de 12 pares adyacentes suman 6 (q = 0,056); especulativo.

## 5. Quipus que dejan la frontera y sus predicciones

| Quipu | Estructura | Nivel | Género cercano | Predicción comprobable |
|---|---|---|---|---|
| UR040 (Nazca, Peabody) | alternancia W/AB, desfase 2 | demostrado (Holm 0,025) | TAB/FOR: pares intercalados | Con otra lectura, la alternancia se conserva. Si el color que domina se mantiene, es una tabla de 2 columnas; hoy los valores son casi nulos, así que la prueba es la foto. |
| UR167 (Ica o Cajamarquilla, AMNH) | alternancia AB/MB, desfase 2 | demostrado (Holm 0,025) | TAB/FOR | Mismo formato; los valores 0/1 sugieren presencia/ausencia por par, así que otro transcriptor debe leer los mismos 0 en los mismos colores. |
| UR1033F (Peabody) | alternancia W/AB; AB > W en 14 de 16 | apoyado (q 0,010) | TAB: tabla de 2 columnas intercaladas | En el lote UR1033, C y D ya alternan con desfase 2 y B repite un ciclo de 3 colores (W:R, W:GG, W:AB). A, E y G tienen 4–12 colgantes, demasiado pocos para evaluarlos. Predicción: en la foto de UR1033F, AB > W también en los pares hoy leídos como 0 o rotos; un ciclo de color en A, E o G es esperable, pero no se exige. |
| UR122 (Nazca, Göteborg) | totales por posición (columna) | propuesto por reglas; **apoyado post hoc** con KH0049 | SUM/TAB jerárquica | Las cuerdas de UR122 en 0 donde KH0049 tiene valor (p. ej. p21–p23: 487, 281, 661) están rotas o sueltas en el objeto. El bloque 1 completo cumple B0 = B1 + B2 + B3. |

**Recuento:**

- Dejan de ser frontera **3 de 180 (1,7 %)** con las reglas, o **4 (2,2 %)** contando UR122 post hoc.
- Con el diseño congelado sin Enmienda 3 serían 22. De ellos, 19 caen con el nulo estricto.

**Falsos positivos esperados:**

1. Según BH, Σq de las filas que sacan quipus = 0,027 falsos esperados entre los 3.
2. Fronteras nulas completas: 0 quipus salen en 2 de 2 réplicas, con las reglas con y sin Enmienda 3. La cota superior Poisson al 95 % es de ≈ 1,5 por corrida.
3. El dato que más importa: **el diseño congelado tenía una tasa de falsos positivos real del orden de 19/22 (≈ 86 %)** contra la confusión por estructura local. Esa confusión es invisible para un nulo de permutación total. Las copias reales (los controles) sobreviven al nulo estricto, así que la caída no es pérdida de potencia.

## 6. Limitaciones

- La Enmienda 3 es posterior a ver los datos. Solo sube los p, así que no puede crear hallazgos, pero la decisión de qué confusiones controlar se tomó viendo las filas.
- En las pruebas entre quipus con muchos compañeros, el suelo de p es 5e-4 (presupuesto de tiempo). No pueden llegar a Holm global (≈ 2e-5), así que su máximo nivel posible es «apoyado».
- Las tablas de 2 columnas intercaladas dependen del color. UR (Urton) distingue más colores que AS. La concentración en el Peabody puede ser del lote o del transcriptor; UR transcribe los 5.
- T4 y T6 dependen de la segmentación en grupos del transcriptor (UR1107 frente a UR237).
- I8 e I9 cuentan totales repetidos más de una vez (artefacto en AS093). Una versión con totales distintos solo puede dar menos.
- KH0049 no está en la frontera: su estructura jerárquica es un hallazgo colateral que el atlas no recoge; KH0049 figura como FOR.

## Para el coordinador

- **Recuento:** de los 180 quipus «decimales sin estructura», dejan la frontera **3 (1,7 %)**: UR040, UR167 y UR1033F. Contando UR122 post hoc son **4 (2,2 %)**. Los falsos esperados son Σq = 0,027, y en 2 fronteras nulas salen 0 y 0. **Demostrado** para UR040 y UR167 (Holm 0,025); **apoyado** para UR1033F (q 0,010).
- **Estructura común de los 3: dos colores intercalados A/B/A/B.** Es la única familia que se replica en la mitad de confirmación (q confirmatorio = 0,003). En el corpus la tienen 19 quipus, 15 de ellos ya en TAB/FOR. Se concentra en el Peabody (5 de 12; Fisher 2,6e-5, descriptivo). Es una **tabla de dos columnas escrita intercalando**: en 4 casos con valores, un color domina en 12–14 de 12–16 pares. Nivel: **apoyado** como formato. Su lectura como «dos categorías por unidad» es **propuesta**.
- **Nuevo y fuerte (post hoc): KH0049/UR122 es una tabla jerárquica con totales por columna.** B0 = B1 + B2 en 14 de 18 posiciones y B1 = B3 + B4 + B5 en 7–8 de 18 (p = 5e-5 cada una). UR122 copia la sección del subtotal. La discrepancia 15652/15649 está en las dos copias, así que es del original. Nivel: **apoyado**, porque es posterior al diseño. Corrige a 10: la columna-total ya no es «solo Incahuasi».
- **Advertencia metodológica:** con el diseño congelado salían 22 quipus y 7 familias «replicadas». Un nulo que conserva rachas y escalones de F tumba 19 de los 22: la estructura local imita las relaciones. Los controles reales (UR1107/UR237 invertido y HP055/UR1084) **sobreviven** a ese nulo (p = 5e-4). **Demostrado** que el nulo de permutación total es insuficiente para buscar relaciones entre quipus. Toda prueba futura de copia, diferencia o razón debe usar nulos por tramos.
- **Relaciones entre quipus de la frontera o del mismo museo: negativo.** No hay copias nuevas, inversiones, versiones desplazadas, versiones escaladas ni grupos reordenados que sobrevivan. QU017 ~ UR016 (diferencia, p_bloque 5e-4) no es específico: QU017 puntúa casi igual con otros 3 compañeros. Solo queda UR1118 ≈ UR218, ya conocido. Nivel del negativo: **apoyado**, con potencia comprobada por los controles.
- **Jerarquía débil por sitio (un total de grupo que aparece en otro quipu del mismo sitio): negativo** (I8: 2 de 79; I9: 0 de 67; ninguna familia promovida). El mejor caso (AS093 ← UR1088) es un artefacto de totales repetidos (15). Nivel: **apoyado** (negativo).
- **Subsidiarias que escalan con su colgante (T5).** Hay exceso agregado: 11 de 81 frente a 4 con un nulo de bloques dentro del grupo (p = 0,002). No se replica por quipu (Holm B 0,066). UR016 (p 1e-5) es **propuesto**; UR093, HP011 y UR1130 son **especulativos**. Es una escala por rangos (ρ 0,38–0,87), no una razón fija: compatible con el negativo de n_quipus_modernos sobre la «cría proporcional».
- **Tendencias monótonas dentro de grupo (T4).** Hay exceso agregado: 23 de 154 frente a 7,7 (p = 3e-6). No se replica en B (Holm 0,12) y es frágil al transcriptor: UR1107 da p = 3e-5, y su doble UR237 da 0,096 porque segmenta otros grupos. Nivel: **propuesto** (posible «lista ordenada»). No es un género hasta tener segmentación independiente.
- **Negativos limpios:**
  - periodicidad de valores (T1: 3 de 78);
  - sumas de bloque no contiguas fuera de UR122 (T6: 3 de 150);
  - pares con suma constante (T7: UR076, 8 de 12 pares suman 6, especulativo);
  - repeticiones internas tras el nulo por tramos (T3: 7 de 170, al nivel del azar).
- **Predicciones baratas:**
  1. Foto de UR122: las cuerdas en 0 donde KH0049 tiene valor (p. ej. 487, 281, 661 en el bloque 1) deben estar rotas.
  2. Lote UR1033 (Peabody): C, D y F alternan 2 colores y B cicla 3. Ya se cumple en los datos para C y D; A, E y G son demasiado cortos. En la foto de UR1033F, AB > W debe sostenerse en los pares hoy leídos como 0.
  3. Retranscribir UR040 y UR167: la alternancia de color se conserva.
  4. Releer KH0049 B1[1]: debe dar 15652, no 15649 (error del original).
  **Especulativo** hasta comprobarlas.

> **Corrección del coordinador (2026-10-18):** en la tabla de §5, fila UR122, la frase «el bloque 1 completo cumple B0 = B1 + B2 + B3» no la sostiene `07_ur122_kh0049.py`, que da diferencias grandes en casi todas las posiciones. Queda retirada. La procedencia de KH0049 es «Costa Sur» en OKR y KFG; «Nazca» viene de UR122. Novedad: KFG ya lista las sumas indexadas de KH0049 como salida automática; la jerarquía de 3 niveles, la copia UR122 y la discrepancia compartida no aparecen publicadas (ver `novedad_kh0049.md`).
