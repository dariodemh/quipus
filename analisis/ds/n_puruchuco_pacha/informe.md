# ¿Sirve el método de Incahuasi en otros archivos? Puruchuco y Pachacamac

**Equipo:** `n_puruchuco_pacha`. **Fecha:** 2026-10-18.
**Datos:** `analisis/datos/cuerdas.csv` (KFG, 651 quipus), `quipus.csv`, `grupos.csv`,
`khipu.db` (OKR) enlazado por `analisis/17_okr_pendientes/puente.csv`.
**Scripts:** `comun_np.py`, `00_explorar.py`, `01_puruchuco_jerarquia.py`,
`02_general.py`, `03_candidatos.py`, `04_marcadores.py`, `05_controles.py`,
`06_celdas.py`, `07_copias_cuerda.py`. Semilla fija 20261018 (+ detector).
Todo se ha escrito solo en `analisis/ds/n_puruchuco_pacha/`. Sin commits.

---

## 0. Resumen de una línea

**Sí, el método sirve, pero no como detector genérico: en Puruchuco reproduce la
jerarquía de Urton & Brezine (2005) con 16/20 y 14/20 columnas exactas
(p = 0,0002), y en Pachacamac no aparece nada (0/65 quipus con cuota,
0/8 con tabla de celdas, ningún enlace tras corrección).** El resultado importante
de la ronda es que **Puruchuco es un segundo sistema encadenado real**, distinto
del sistema de parejas de Incahuasi; y que el detector a nivel de "registro"
—incluso con todas las cuerdas— **no lo ve**.

---

## 1. Pregunta

¿El método que resolvió Incahuasi (UR255–UR280) sirve en otros archivos?

Las cuatro reglas que, según el equipo 13, hicieron visibles las relaciones de
Incahuasi son:

- **(a)** usar **todas** las cuerdas, no solo las cabeceras;
- **(b)** alinear registros por **número de grupo sin saltar grupos vacíos**;
- **(c)** incluir la **primera subsidiaria** (colgante + s1);
- **(d)** tratar los **grupos de color marcador (PK)** como separadores.

`n_detectores` había dado negativo fuera de Incahuasi, pero solo con cabeceras y
con los detectores D1–D4. Aquí se repiten las pruebas con (a)–(d) y contra OKR,
en Puruchuco (24 quipus; jerarquía UR063/064/065/066/067/068/073), Pachacamac
(90 quipus) y los mejores candidatos del mapa de legibilidad.

---

## 2. Método

### 2.1 Unidad, registros y definiciones

- **Unidad de análisis: el quipu.** Las permutaciones son siempre dentro de un
  quipu (barajar cuerdas o registros de B), nunca entre quipus.
- **Registro** = grupo de colgantes. Se conservan los **grupos vacíos** entre el
  mínimo y el máximo (regla b). Un grupo vacío tiene valor 0 y no rompe la
  alineación.
- **Tres definiciones de valor de registro**, todas con todas las cuerdas
  (regla a):
  - **X**: cabecera = primer colgante anudado (línea base de `n_detectores`);
  - **P**: suma de todos los colgantes nivel 0 del grupo;
  - **PS**: P + suma de las primeras subsidiarias (regla c).
- **Celdas** (regla c, prueba de tabla): vector de colgante + su primera
  subsidiaria, por grupo; se compara posición a posición con el vector de
  colgantes de otro quipu (D4 de `n_detectores`, reimplementado).
- **Marcadoras** (regla d): en OKR, `CORD_CLASSIFICATION='M'`; en KFG, los
  grupos PK sin nudos. Los bloques entre marcadoras son registros/secciones.
- **0 sin nudos = cuerda ausente**, no cero contable.
- **Tolerancia**: diferencia en {0, 1, 10, 100, 1000} (un dígito), la misma de
  `13_sistema_incahuasi`.

### 2.2 OKR además de KFG

- Enlace `kfg → KHIPU_ID` por `puente.csv` (752 filas; 6/6 de la jerarquía de
  Puruchuco enlazados).
- Valor OKR de una cuerda = `sum(knot_value_type)` de sus nudos
  (`TOTAL_VALUE` de `knot_cluster` está a 0 en esta base). Comprobado: los
  totales de UR063–UR068 coinciden exactamente entre KFG y OKR (p. ej. UR068
  3501 = 3501); UR073 difiere en 8 (1147 vs 1139) por **una sola cuerda**
  (ordinal 54: KFG 9 vs OKR 1), no por las marcadoras.
- OKR añade lo que KFG pierde (D5 de `n_detectores`):
  - **Pachacamac:** 18 marcadoras M en 9 quipus (AS075, AS112, AS156, AS170,
    UR1144, UR123, UR197, UR213, UR253) y **11 cuerdas superiores**, todas de
    UR1096 (valores 14, 19, 60, 15, 12, 17, 45, 26, 0, 0, 0; no son totales).
  - **Puruchuco:** 5 marcadoras, todas de **UR073**, y 0 cuerdas superiores.
  - **Incahuasi:** 52 marcadoras en 11 quipus, 0 superiores.
- Conclusión operativa: la regla (d) solo tiene materia en 9/90 quipus de
  Pachacamac y en UR073; fuera de ahí, KFG y OKR dan la misma estructura.

### 2.3 Pruebas y nulos

| Prueba | Qué mide | Nulo | Corrección |
|---|---|---|---|
| **T1 copias** | P_A(i)=P_B(i) por posición; y a nivel de cuerda | barajar el orden de B | BH sobre todos los pares |
| **T2 A+B→C** | P_A(i)+P_B(i) cae en los valores de registro de un tercer quipu | barajar el orden de B (conserva marginales, rompe la alineación); E exacta invariante a la permutación | BH + **nulo del mínimo p de toda la familia** (jardín de senderos, 100 réplicas) |
| **T3 filas→filas** | LCS ordenada de P_A y P_B | barajar B | BH sobre todos los pares ordenados |
| **T4 cuotas** | x_i − v = c constante, con v cualquier otra cuerda del grupo | barajar cuerdas no cabecera entre registros del mismo quipu | BH sobre quipus |
| **T5 celdas** (c) | colgante+s1 de A reproduce colgantes de un grupo de B | inyección aleatoria de grupos de A en grupos distintos de B | BH sobre pares |

El nulo de T2 es el del equipo 13/rojo: permuta **solo** el emparejamiento y
conserva magnitudes, tamaños y huecos. La corrección por el "jardín" repite
**toda** la búsqueda (todos los pares × todas las variantes) con B barajado y
compara el mínimo p observado con la distribución nula del mínimo; así se paga
por todas las combinaciones probadas, no solo por una.

**Familias corregidas por el jardín (T2):** Incahuasi 528 pares × 3 = 1584;
Pachacamac 2485 × 3 = **7455**; Puruchuco 231 × 3 = 693; Ica 496 × 3 = 1488;
Huaquerones 136 × 3 = 408. Además, T1/T3/T4/T5 se corrigen con **BH** sobre
todos sus pares o quipus (en Pachacamac: 1431 pares de copia a nivel de grupo y
3916 a nivel de cuerda; 4160 pares de LCS; 65 quipus de cuota; 7–18 pares de
celdas según el archivo).

---

## 3. Puruchuco: la jerarquía de Urton & Brezine (2005) se reproduce

### 3.1 Qué dice la literatura y qué hay en los datos

Urton (2017, cap. 5) describe **siete quipus en tres niveles**:

- **nivel I:** UR063 y UR073 (UR073 roto: 69 de ~111 cuerdas);
- **nivel II:** UR064, UR068 y el "nº 9" de Mackey (perdido);
- **nivel III:** UR066 y UR067.

Verificación de ids: los siete de la lista del encargo existen en `quipus.csv`
como UR063, UR064, UR065, UR066, UR067, UR068 y UR073 (región `Puruchuco`).
**UR065 no es uno de los siete**: es un fragmento de 6 cuerdas y suma 10; el
séptimo es el "nº 9" de Mackey, perdido. Lo comprobado es
**UR063 → UR068 → UR067**; **UR073** es la copia rota de UR063, y **UR064/UR066**
son las copias de UR068/UR067 (la suma se hereda, aunque UR064→UR066 no se probó
columna a columna).

Los quipus del mismo nivel son **copias** (UR064≈UR068; UR066≈UR067). Las
**seis secciones** de UR063 suman, columna a columna, la **sección central** de
UR068 (20 cuerdas, #34–#53). Las **tres secciones** de UR068 suman, columna a
columna, las 20 cuerdas de datos de UR067. El libro anticipa dos discrepancias
concretas: **2904 en vez de 2908** y **161 en vez de 162**.

En KFG/OKR los tres niveles están completos y coinciden:

| quipu | cuerdas | nivel | estructura |
|---|---|---|---|
| UR063 | 111 | I | 6 secciones (20,21,15,20,20,15) |
| UR073 | 74 (69 + 5 M) | I | copia rota de UR063; 5 marcadoras → 6 bloques |
| UR064 | 74 | II | intro + 3 secciones |
| UR068 | 73 | II | intro 12 (+ cuerda 13 = 0) + 3 secciones de 20 |
| UR066 | 35 | III | intro (12) + datos |
| UR067 | 35 | III | intro (12) + datos (una cuerda rota) |

### 3.2 Nivel II → nivel III: UR068 → UR067

Se suman las tres secciones de UR068 (cuerdas 14–33, 34–53, 54–73) columna a
columna, agrupando por el ritmo de color **W / AB-MB / GG / W:KB**. Resultado de
las 20 columnas:

```
sumas UR068 : 6  0  1  0 | 19  4  3  0 | 22  3  9  1 | 156 13 12  5 | 2908 133 162 40
UR067 datos : 0  0  1  0 | 19  4  3  0 | 22  3  9  2 | 156 13 12  0 | 2904 133 161 40
```

(UR067 sin la cuerda 30, valor 1, que es la "broken string" que el propio Urton
aparta.)

- **16/20 exactas** y **17/20 con tolerancia ±1 dígito**.
- Las dos discrepancias son **exactamente** las del libro: 2904 vs 2908 y
  161 vs 162. Las otras dos (6 vs 0, 5 vs 0) son cuerdas que UR066 sí registra
  (UR066 tiene 6 y 5 en esas posiciones).
- **Nulo 1** (barajar las 20 cuerdas de UR067, 5000 réplicas): media 1,49,
  máximo 7, **p = 0,0002**.
- **Nulo 2** (permutar los 5 grupos de 4 dentro de cada sección de UR068, 2000
  réplicas): media 0,75, máximo 7, **p = 0,0005**.
- **Especificidad:** las mismas sumas dan **16/20** contra UR067 (el padre) y
  **16/20** contra UR066 (su copia de nivel III, que conserva las cuerdas 6 y 5
  que UR067 perdió); **≤3/20** contra los otros 22 quipus de Puruchuco.

### 3.3 Nivel I → nivel II: UR063 → sección central de UR068

Las seis secciones de UR063 son los grupos KFG **0 | 1+2+3 | 4 | 5 | 6 | 7**
(tamaños 20, 21, 15, 20, 20, 15). Cada sección se parte en grupos de 4 que
empiezan en una cuerda blanca; los grupos se alinean **por el final** (el último
grupo de cada sección es el que lleva el valor grande: 127, 229, 148, 367, 157,
219). Sumando por columna de color:

```
sumas UR063 : 2  0  1  0 |  9  1  1  0 |  8  2  3  1 |  57  5  4  2 | 1247 46 44  6
UR068 centro: 2  0  1  0 |  8  1  1  0 |  8  1  3  1 |  57  5  6  2 | 1236 46 59 10
```

- **14/20 exactas** y **16/20 con tolerancia**.
- Las columnas blancas **2, 8 y 57 son exactas**; la cuarta da 9 frente a 8
  (un dígito). La columna grande da 1247 vs 1236 (diferencia 11) y las dos
  últimas 44 vs 59 y 6 vs 10: es la "flexibilidad" que el propio Urton describe
  para el nivel I–II ("most of the summations are only close"), no un fallo del
  test.
- **Nulo** (permutar los grupos de 4 dentro de cada sección, 5000 réplicas):
  media 1,43, máximo 7, **p = 0,0002**.
- **Especificidad:** barriendo **todas** las ventanas contiguas de 20 cuerdas de
  los 22 quipus de Puruchuco, la mejor ventana de UR068 (la central) da 14/20;
  la de UR064 (su copia) 10/20; **ninguna otra supera 7/20**.

### 3.4 Copias y marcadoras

- **UR064 ≈ UR068:** LCS de valores = **66/73**; nulo 47,6 (máx 53),
  **p = 0,0005**. Sumas de sección: UR064 [1421, 1376, 592] vs UR068
  [1430, 1447, 621].
- **UR066 ≈ UR067:** **30/35 cuerdas idénticas** por posición, LCS 32/35; nulo
  20,9 (máx 26), **p < 0,001**. Las cinco diferencias son 0/1, 1/0, 6/0, 5/0 y
  0/161 (la cuerda que falta en UR066).
- **UR073 y la regla (d):** sus **5 marcadoras OKR** (ordinales 7, 24, 39, 57,
  72) dividen el quipu en **6 bloques** con sumas
  **[155, 251, 172, 391, 170, 0]**. Las seis secciones de UR063 suman
  **[165, 266, 172, 406, 197, 233]**. Los cinco primeros bloques coinciden con
  diferencias **−10, −15, 0, −15, −27**; el sexto se perdió porque UR073 está
  roto (69 cuerdas). Esto valida a la vez la partición en seis secciones y la
  regla "marcadora = separador".

### 3.5 Corrección múltiple y veredicto

Las tres pruebas dirigidas de la jerarquía dan p = 0,0002 / 0,0002 / 0,0005;
**Holm sobre las 3 → máximo 0,0006**. No hay ajuste post hoc: las secciones y
la dirección de las sumas vienen de la literatura; el nulo solo rompe la
alineación.

**Veredicto Puruchuco: SISTEMA ENCADENADO, confirmado.** No es el sistema de
parejas de Incahuasi (A+B→C), sino una **cadena** nivel I → II → III: cada quipu
inferior se despliega en secciones y sus columnas suman las cuerdas del padre.
La relación es real, direccional y con las dos discrepancias exactas que la
literatura anticipa. Nivel de evidencia: **demostrado (reproducción)** para las
sumas; **apoyado con datos** para la partición en seis secciones (inferida de
los grupos KFG y confirmada por las marcadoras de UR073).

---

## 4. Pachacamac: nada

90 quipus, 71 con ≥3 registros, 860 registros. Familia T2: **2485 pares × 3
variantes = 7455 pruebas**.

| Prueba | Resultado | Nulo / corrección | Veredicto |
|---|---|---|---|
| **T2 A+B→C (X)** | mejor p = 0,079 (UR1099+UR226, 2 aciertos) | corregido p = 0,91; BH q = 1 | nada |
| **T2 A+B→C (P)** | mejor p = 0,026 (UR1175+UR208, 16/32, E = 9,2) | corregido p = 0,51; q = 1 | densidad |
| **T2 A+B→C (PS)** | mejor p = 0,0054 (UR1099+UR212, 4/16, E = 0,7) | corregido p = **0,04–0,06** (dos réplicas); q = 1 | aislado/noise |
| **T1 copias (grupo)** | ningún par con q < 0,05 | BH 1431 pares | nada |
| **T1 copias (cuerda)** | dos copias conocidas: AS125=UR247 (14/15), UR1118=UR218 (8/20); AS110=UR123 (5/20) no está catalogado pero no pasa BH | BH 3916 pares, q = 1 | nada nuevo |
| **T3 filas→filas** | mejor UR199↔UR208: LCS 7, nulo 5,2, p = 0,05–0,065 | BH 4160 pares, q = 1 | nada |
| **T4 cuotas** | **0/65 quipus con q < 0,05** | BH sobre 65 | nada |
| **T5 celdas (c)** | **0/8 quipus** con tabla de celdas; ningún par con aciertos | BH | nada |

El único candidato que merece mirarse, **UR1099+UR212** (PS, 4 aciertos,
E = 0,7), se desmonta al mirar el destino: las cuatro sumas
(1593, 1679, 822, 735) caen en **cuatro quipus distintos** (HP011, UR208,
UR1175, HP005/UR226), no en un libro consolidado. Es el mismo patrón que
`n_detectores` llamó "artefacto de densidad" en Huacho.

**Veredicto Pachacamac: NADA.** No hay cuotas, no hay tabla de celdas, no hay
copias nuevas, no hay cadena ordenada. El único enlace a nivel de grupo que
roza la significación (PS, p corregido 0,04–0,06) es inestable, no tiene
destino único y no se replica en X ni en P.

**Control de potencia:** la misma prueba T4 recupera **10/30 quipus de
Incahuasi** con q = 0,002–0,012 (UR255 c=15, UR267A c=15, UR256 c=10,
UR267B c=10, UR266 c=47, UR275 c=47, UR269 c=46, UR268 c=208, UR274B c=17,
UR277 c=2). El negativo de Pachacamac no es falta de potencia de la prueba de
cuotas. Lo mismo vale para T5: el control UR270→UR278 da 6 grupos, 9/9
columnas y **p = 0,0005**; Pachacamac no tiene ni un par con aciertos.

---

## 5. Los mejores candidatos del mapa de legibilidad

No existe `analisis/ds/n_legibilidad/informe.md`. Se usó la versión disponible de
`quipus_legibles.csv` (**17 quipus con q < 0,05** en el momento de la lectura; el
archivo se regeneró durante la sesión, así que se reporta esa versión). Fuera de
Incahuasi, los primeros puestos son casi todos **reglas internas**
(`aditivo interno`, `repetición jerárquica`: AS008, AS066, AS199, MM019, UR017,
UR093, UR113, UR1130, UR166, UR204), no enlaces entre quipus. Los únicos
"copia entre quipus" verificables son:

- **UR066/UR067** (Puruchuco): la jerarquía de §3, ya identificada;
- **AS125/UR247** (Pachacamac): **el mismo objeto** en dos museos, ya catalogado
  en `14_copias` (14/15 cuerdas idénticas). No es una relación contable nueva.

Ninguno de los candidatos restantes muestra pareja de suma, cuota ni tabla.
**Veredicto: sin sistema; el mapa de legibilidad señala redundancia interna, no
archivos encadenados.**

---

## 6. Resultados negativos (explícitos)

1. **El detector genérico a nivel de registro no reproduce ni siquiera
   Incahuasi.** Con T2 (X/P/PS) y corrección por el jardín, el mínimo p de
   Incahuasi es 0,030–0,045 y el corregido 0,40–0,70. Las parejas conocidas
   UR273A+B y UR267A+B aparecen con p ≈ 0,045, pero no sobreviven a la familia
   de 528 pares. **Un negativo de este detector no es informativo**: no tiene
   potencia para sistemas dispersos.
2. **Puruchuco es invisible para ese mismo detector.** T2 sobre 231 pares:
   p corregido 0,27 (P), 0,53 (PS), 0,85 (X); T4 cuotas: 0/22; T1 grupo: 0.
   La jerarquía solo aparece al alinear **columnas dentro de secciones**, no
   registros completos. Es la limitación central del método de Incahuasi
   aplicado a otro género.
3. **Pachacamac no tiene cuotas** (0/65) ni **tabla de celdas** (0/8) ni
   **cadena ordenada** (q = 1). El mejor enlace es ruido de densidad.
4. **Ica (47) y Huaquerones (19):** T2 corregido 0,30–0,71 (Ica) y 0,64–0,90
   (Huaquerones); cuotas 0/29 y 0/17; copias: solo las conocidas AS194/AS195
   (6/7) y UR1166/UR229 (50/194, p = 0,011, q = 1). Nada nuevo.
5. **La regla (d) casi no tiene materia fuera de Incahuasi:** 9/90 quipus de
   Pachacamac y 1/24 de Puruchuco tienen marcadoras; la única aplicación
   sustantiva es UR073, y sirve para confirmar las seis secciones de UR063, no
   para descubrir un sistema nuevo.
6. **UR1096 (Pachacamac)** tiene 11 cuerdas superiores en OKR, pero sus valores
   (14, 19, 60, 15, 12, 17, 45, 26…) no son totales de nada: no hay relación
   vertical que explotar.

---

## 7. Niveles de evidencia

| Afirmación | Nivel |
|---|---|
| Puruchuco: UR068 → UR067, 16/20 columnas exactas, p = 0,0002; las dos discrepancias del libro (2904/2908, 161/162) | **Demostrado (reproducción)** |
| Puruchuco: UR063 → sección central de UR068, 14/20 exactas, p = 0,0002; columnas 2, 8 y 57 exactas (la cuarta, 9 vs 8) | **Apoyado con datos** (las secciones vienen de la literatura; el nulo solo rompe la alineación) |
| Puruchuco: sistema **encadenado** de tres niveles, no de parejas | **Apoyado con datos** |
| Puruchuco: UR064≈UR068 y UR066≈UR067 (copias del mismo nivel) | **Demostrado** (LCS 66/73 y 30/35, p ≤ 0,001) |
| UR073: las 5 marcadoras OKR delimitan las 6 secciones de UR063 (5/5 bloques a ≤27) | **Apoyado con datos** |
| Pachacamac: no hay cuotas, tabla de celdas, copias nuevas ni cadena | **Apoyado con datos** (T4 y T5 con control positivo potente) |
| Pachacamac: el enlace UR1099+UR212 es ruido | **Apoyado con datos** (4 destinos distintos; p corregido inestable 0,04–0,06) |
| El método de Incahuasi no es un detector genérico transferible | **Demostrado** (falla en su propio control positivo tras corrección) |
| Que Puruchuco sea "el segundo sistema" de la ronda | **Apoyado con datos** (dos niveles reproducidos; el nivel II tiene un quipu perdido, el nº 9, que no se puede probar) |

---

## 8. Limitaciones

- **Secciones de UR063:** la figura 5.10 del libro no está en el corpus de texto;
  la partición 0|1+2+3|4|5|6|7 se infiere de los grupos KFG y se confirma con las
  marcadoras de UR073, pero no es una lectura directa de la figura. Un cambio de
  frontera en una sección desplaza las columnas y baja el ajuste.
- **UR067:** hay que apartar una cuerda (la 30, valor 1) para alinear las 20
  columnas; el libro dice que hay una cuerda rota, pero no dice cuál. La
  identificación es consistente con las dos discrepancias publicadas.
- **Nivel II:** el "nº 9" de Mackey está perdido; no se puede probar la suma de
  los tres quipus de nivel II, solo la de UR068 (y su copia UR064) a UR067/UR066.
- **T2:** el estadístico de unión y la corrección por el mínimo p son potentes
  para detectar un sistema denso, pero no para relaciones aisladas. El negativo
  de Pachacamac en T2 es débil; el fuerte es T4/T5.
- **Cobertura:** 19/90 quipus de Pachacamac no tienen ≥3 registros y quedan
  fuera de T2; 25/90 no tienen cuota analizable. Los fragmentos podrían esconder
  un componente, como UR273A en Incahuasi.
- **Procedencia:** se usa `procedencia` arqueológica, nunca museo como lugar de
  origen. Puruchuco se selecciona por `region == 'Puruchuco'` (24 quipus), no
  por procedencia (que en KFG es "Huaquerones"/"Unknown" para muchos).

---

## 9. Para el coordinador

- **Puruchuco es un segundo sistema real, y es encadenado, no de parejas.**
  UR068 → UR067: **16/20 columnas exactas**, p = 0,0002 (nulo barajando cuerdas
  o grupos de 4); UR063 → sección central de UR068: **14/20 exactas**, p =
  0,0002. Holm sobre las 3 pruebas dirigidas: **máximo 0,0006**.
- **La reproducción es literal:** aparecen las dos discrepancias que anticipa
  Urton & Brezine 2005 —**2904 en vez de 2908** y **161 en vez de 162**— y las
  columnas blancas 2, 8 y 57 salen exactas (la cuarta, 9 frente a 8). No es una
  reconstrucción libre: es la jerarquía publicada, con los mismos números.
- **Las copias del mismo nivel también se recuperan:** UR066≈UR067 (30/35
  cuerdas idénticas, p < 0,001) y UR064≈UR068 (LCS 66/73, p = 0,0005). Eso
  cierra el control de "los quipus del mismo nivel se copian".
- **La regla (d) funciona donde debía:** las 5 marcadoras OKR de UR073 dividen
  el quipu en 6 bloques que casan con las 6 secciones de UR063 (5/5 a ≤27;
  el 6º se perdió porque UR073 está roto). Es la validación independiente de la
  partición en secciones.
- **Pachacamac: nada.** 0/65 quipus con cuota (frente a 10/30 en Incahuasi),
  0/8 con tabla de celdas (el control UR270→UR278 da 9/9 columnas, p = 0,0005),
  0 copias nuevas, 0 cadenas ordenadas. El único candidato (UR1099+UR212,
  p corregido 0,04–0,06) reparte sus 4 aciertos entre 4 quipus distintos: ruido
  de densidad.
- **Ica y Huaquerones: nada.** T2 corregido 0,30–0,90; cuotas 0/29 y 0/17;
  copias solo las conocidas (AS194/AS195, UR1166/UR229).
- **El hallazgo metodológico incómodo:** el detector genérico a nivel de
  registro **no reproduce ni Incahuasi** (p corregido 0,40–0,70) y **no ve
  Puruchuco** (p corregido 0,27–0,85). El método no es un detector transferible:
  es un conjunto de principios de alineación, y cada género exige su propia
  unidad (registros en Incahuasi, **columnas dentro de secciones** en Puruchuco).
- **Recomendación 1:** dejar de barrer archivos con T2 a nivel de registro. Para
  buscar un tercer sistema, buscar primero **estructura de secciones** (grupos de
  color/series de 4, marcadoras OKR) y probar sumas **columna a columna**; el
  negativo de Pachacamac con T2 no cierra la puerta a un sistema de ese tipo.
- **Recomendación 2:** el siguiente paso en Puruchuco es probar el nivel II
  completo: UR064+UR068+#9 → UR066/UR067. Sin el nº 9 no se puede; pero se puede
  probar si UR066 y UR067 son **dos copias del mismo consolidado** (ya lo son:
  30/35) y si sus diferencias (161 ausente, 6/5) son cuerdas perdidas o
  correcciones.
- **Recomendación 3:** aplicar el test de **columnas** (P1/P2) a todo el corpus,
  no solo a Puruchuco: detectar quipus con series de 4 cuerdas por color y
  probar si las columnas de uno suman las cuerdas de otro. Es la única prueba
  que vio Puruchuco; un barrido de columnas sobre los 651 quipus es más
  prometedor que otro barrido de registros. En Pachacamac no hay series de 4
  (grupos pequeños), así que no se espera nada allí; el único resto es la
  estructura interna de los 9 quipus con marcadoras (AS075: 5 marcadoras →
  6 bloques), que merece una ficha estructural, no otra ronda de barrido.

---

## 10. Reproducibilidad

| script | qué hace | salida |
|---|---|---|
| `00_explorar.py` | inventario KFG/OKR de Puruchuco; grupos y marcadoras | — |
| `01_puruchuco_jerarquia.py` | P1 UR068→UR067, P2 UR063→UR068, P3 copias; nulos | `salida_01_puruchuco.txt`, `puruchuco_jerarquia.json` |
| `02_general.py` | T1–T4 en Incahuasi, Pachacamac, Puruchuco; jardín | `suma_*.csv`, `copias_*.csv`, `lcs_*.csv`, `cuotas_*.csv`, `general.json` |
| `03_candidatos.py` | Ica y Huaquerones + tabla de candidatos de legibilidad | `candidatos_legibilidad.csv` |
| `04_marcadores.py` | inventario M/T; UR073 vs UR063 | `salida_04_marcadores.txt` |
| `05_controles.py` | especificidad de P1/P2 contra todos los quipus de Puruchuco | `control_p1.csv`, `control_p2.csv` |
| `06_celdas.py` | regla (c) D4 con control UR270→UR278 | `celdas_*.csv` |
| `07_copias_cuerda.py` | copias a nivel de cuerda; control AS125=UR247 | `copias_cuerda_*.csv` |

Semillas: 20261018+1 (01), +2 (02), +6 (06), +7 (07). Los nulos usan
`numpy.random.default_rng` con semilla fija; los p son empíricos
(1 + nº de réplicas ≥ observado)/(B + 1).
