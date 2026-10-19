# Tanteo de géneros con plantillas coloniales: ¿qué clase de contenido llevan los quipus desconocidos?

**Equipo:** `n_plantillas` · **Fecha:** 18-10-2026 · **Semilla:** 20261018 · **Unidad de análisis:** el quipu.

**Datos:**

- `analisis/datos/cuerdas.csv` (KFG, 651 quipus, 57 809 cuerdas tras deduplicar);
- `quipus.csv`;
- `khipu.db` (OKR), solo para los canutos de UR050/UR055;
- `ds/n_no_numericos/quipus_clase.csv`, para canutos y fibra.

**Archivos de esta carpeta:**

- **Plantillas:** `plantillas.md` (congeladas, con las revisiones documentadas en §3) y `predicciones_preregistradas.md` (secciones A–F, escritas antes de cada prueba).
- **Scripts, en orden:**
  - `01_datos.py`: estructura y mitades;
  - `plantillas.py`: estadísticos, con autocomprobación en `__main__`;
  - `02_puntuar.py`: barrido;
  - `03_p6b.py`: consolidación entre quipus;
  - `04_consolidar.py`: p_corpus, BH/Holm, controles, exceso y agrupamiento;
  - `05_predicciones.py`: paso 5;
  - `06_ur053.py`: C5 y C6;
  - `07_holm_predicciones.py`.
- **Salidas:**
  - `puntuaciones.csv`: todas las pruebas, con khipu, plantilla, estadístico, p, q, mitad, q_holm, p_perm, p_corpus y coincide;
  - `controles.csv`, `coincidencias.csv`, `exceso_replicacion.csv`, `agrupamiento.txt`, `no_numericos.csv`;
  - `pred_C1/C2/C3/C5.csv` y `predicciones.csv`;
  - `controles_antes_revision.csv`, `obs_perm_prueba.csv` y `p6b_prueba.csv`: corridas de control previas al barrido.

---

## 1. Pregunta y diseño

¿Se puede reconocer el **género** de un quipu desconocido comparándolo con la *forma* que los documentos coloniales dictados de quipus atribuyen a cada género? Si una forma es lo bastante específica, los quipus de ese género deberían ajustarse a ella mucho más que por azar.

El diseño tiene tres piezas:

1. **Biblioteca de plantillas** con firma estructural medible (`plantillas.md`). Las plantillas se congelaron antes de puntuar el corpus.
2. **Controles positivos:**
   - Incahuasi: UR266, UR275 y UR278;
   - Puruchuco: UR063–UR068 y UR073;
   - Santa: UR087–UR092;
   - UR006 (calendario de Urton);
   - UR053B/C (los «ceques» de Urton);
   - los análogos censales de Urton: UR029, UR091, AS026A, AS157 y UR023.
3. **Barrido en dos mitades**, separadas al azar antes de puntuar (325 y 326 quipus):
   - **p de permutación** dentro del quipu, secuencial hasta 99 999 réplicas;
   - **p_corpus:** el percentil del quipu entre los de tamaño parecido;
   - **BH y Holm** sobre *todas* las pruebas quipu × variante de cada mitad: 5717 en exploración y 5758 en confirmación;
   - **coincidencia** = q_BH < 0,05 **y** p_corpus ≤ 0,05.

### 1.1 Biblioteca de plantillas (detalle y citas en `plantillas.md`)

| Plantilla | Fuente (línea en `fuentes_txt/`) | Firma medida | Control positivo |
|---|---|---|---|
| P1 Censo por «calles» de edad (a–d) | Murúa en U17 l. 2438–2439; Guaman Poma de memoria | Ventana de 10 (o 9, o 2 × 10) cuerdas con el perfil de una población estacionaria; también 10 sumas de grupo | ninguno |
| P2 Censo toledano en 4 categorías | Lunahuaná 1577/1590, R l. 762 | Proporciones 740 : 89 : 601 : 1846 | ninguno |
| P3 Unidades domésticas | U17 l. 2485–2492 | Distribución de 1–7 | Análogos de Urton |
| P4 → P4r Padrón nombrado | MU18 l. 38, 48 | Bandas de color de igual largo, valores bajos | Santa |
| P5a–c Libro de almacén | U17 cap. 9; SINTESIS | Partes estables; cabecera = cuota + destinos; tríos `[x, c, x−c]` | Incahuasi |
| P6a/b Consolidación | U17 l. 6231; `n_puruchuco_pacha` | Sumas internas; secciones que suman una ventana de otro quipu del hallazgo | Puruchuco |
| P7a–c Tributo en orden fijo | M24 (wanka); R l. 762, 806–809 | Perfil por posición; 12 categorías; tasa de 4 especies | ninguno |
| P8 → P8ar, b, c Calendario | U17 l. 711–750; R 914–916 | Unidades de ~30 cuerdas; valores ≈ 30 (×12); valores ≈ 40 (×9) | UR006 |
| P9a/b Ceques | U17 l. 1258, 1263, 1266–1280, 1518–1524 | Ciclo de color de periodo 3; conteos 41 / 328–350 / ½ / {9,9,9,14} | UR053B/C |
| P10 Lista dinástica | Cronistas (débil) | Bloque de 5 + resto con color distinto | ninguno |
| P11a/b Registro segmentado por eventos | P04 l. 318, 373–380 (Guacrapaucar, Chupaychu, Xauxa) | Bloques que repiten la secuencia de colores, con o sin marcador | ninguno (el quipu wanka no está en el corpus) |
| P11c Lista de conquistas | P04 l. 570–578; Calancha en l. 318 | Cifras de cabecera únicas | ninguno |
| P12 Cuenta monetaria colonial | C13 l. 18–124; MU18 l. 38 | Subsidiaria 1–7 (reales) | ninguno |

**Senderos bifurcados.** Se probaron 30 variantes congeladas, más 2 revisiones (P4r y P8ar), más un cambio de clave de datos (P6b) y 1 variante nueva en el paso 5 (C5). Las pruebas del paso 5 suman 56, todas con Holm conjunto. Antes de congelar ya había visto los conteos de UR050 (164), UR055 (180) y UR052 (24 × 4); por eso todo acierto de conteo en ellos se trató como post hoc (`plantillas.md` §0).

---

## 2. Controles positivos (validación del método)

| Plantilla | Reconocidos (p < 0,05 y p_corpus ≤ 0,10) | Detalle | Veredicto |
|---|---|---|---|
| **P4r padrón (Santa 1670)** | **5/6** | Los 6 dan p_perm = 5·10⁻⁵; UR087 tiene p_corpus 0,12. El P4 original, por grupos KFG, solo veía UR087: los grupos KFG no recogen las bandas de 6 (UR088 y UR092 son *un* grupo KFG). | **Validada tras una revisión** |
| **P5 almacén (Incahuasi)** | UR275 (P5b p = 0,0012; P5c p = 5·10⁻⁵); UR278 (P5a p = 10⁻⁵, pero p_corpus no es interpretable: solo 8 quipus pasan la puerta, casi todos de Incahuasi); UR266 solo nominal (P5c p = 0,0125, p_corpus 0,25) | 1/3 estricto, 2/3 laxo | **Parcial** |
| **P6b consolidación (Puruchuco)** | **4/6** | UR068 → UR066/UR067 con 15/20 columnas exactas, incluidas las discrepancias 2908/2904 y 162/161 de Urton y Brezine; UR064, UR066 y UR067, p = 5·10⁻⁴. UR063 (secciones irregulares 20/21/15) y UR073 (roto) no. | **Validada** |
| **P8ar calendario (UR006)** | 1/3 | UR006: 19 unidades de 26–36 cuerdas, p = 5·10⁻⁵, p_corpus 0,002. El P8a original (racha en [27, 33] con «grupo + siguientes») daba p = 0,24. UR009 y UR021, fragmentos fuente de UR006, no. | **Validada solo en UR006** |
| **P9a ceques (UR053B/C)** | 1/2 | UR053C sí (p = 10⁻⁵); UR053B no, porque lleva el tercer color en subsidiarias. | **Validada** |
| **P3 unidades domésticas** | 1/4 (UR029); UR023 no pasa la puerta | Los análogos censales de Urton (χ² de Brezine) **no se distinguen** de quipus de su tamaño | **Descartada** |

Lectura: el método **reconoce los archivos ya leídos** (Santa, Puruchuco, Incahuasi, UR006 y UR053C) cuando la firma es estructural. No reconoce los «censos» de Urton, que se definían solo por la distribución de valores. Las plantillas P1, P2, P7, P8b/c, P10, P11 y P12 **no tienen control** en el corpus, y sus coincidencias no pueden pasar de *propuesto*.

---

## 3. Barrido del corpus: el número de coincidencias no es evidencia

Hay **92 coincidencias** en 8871 pruebas (sin P9b): 44 en exploración y 48 en confirmación. Como la coincidencia exige p_corpus ≤ 0,05, a lo sumo ~5 % de los quipus probados puede coincidir **por construcción**. En `exceso_replicacion.csv` se compara lo observado con esa cota.

| Plantilla | Pruebas | Coincidencias (IC95 de Poisson) | Cota 5 % | Razón |
|---|---:|---:|---:|---:|
| P11a bloques repetidos | 396 | 16 [9, 24] | 19,8 | 0,81 |
| P9a ciclo de 3 colores | 559 | 16 [9, 24] | 28,0 | 0,57 |
| P4r padrón | 275 | 9 [4, 15] | 13,8 | 0,65 |
| P11c cifras de lugar | 184 | 7 [2, 13] | 9,2 | 0,76 |
| P6a / P6b consolidación | 401 / 302 | 6 / 6 | 20,1 / 15,1 | 0,30 / 0,40 |
| P11b bloques con marcador | 396 | 6 | 19,8 | 0,30 |
| P5c / P5b almacén | 494 / 290 | 5 / 3 | 24,7 / 14,5 | 0,20 / 0,21 |
| P7a / P7b / P7c tributo | 193 / 23 / 603 | 4 / 1 / 2 | — | ≤ 0,87 |
| P1a–d calles de edad | 195–515 | 1 / 2 / 2 / 1 | 10–26 | ≤ 0,11 |
| P8ar / P8b / P8c calendario | 455–515 | 1 / 2 / 2 | 23–26 | ≤ 0,08 |
| P2, P3, P10, P12 | 135–603 | **0** | — | 0 |

- **Ninguna plantilla supera la tasa base.** Todas las razones son ≤ 0,87. Como población, ningún género colonial aparece «en exceso» en el corpus.
- **Replicación del agrupamiento** (categoría elegida en exploración y probada en confirmación; Holm sobre las 17 pruebas de confirmación de este paso):
  - **Ninguna sobrevive.** La mejor es P6a → Incahuasi: 2/4 en exploración, 2/2 en confirmación frente a una base de 13/201 (p = 0,0039; Holm 0,062).
  - Siguen P11a → Museum für Völkerkunde de Berlín (3/6 → 4/10; p = 0,046; Holm 0,65) y P4r → Santa (4/6 → 1/3; p = 0,043; Holm 0,64).
- **Agrupamientos con todo el corpus** (descriptivos, `agrupamiento.txt`):
  - P4r se concentra en Santa (5/9; Fisher p = 6·10⁻⁸), es decir, el control.
  - P5c, P6a y P7a se concentran en Incahuasi (p = 0,005; 3·10⁻⁴; 0,003); son quipus del mismo sistema ya leído (UR255, UR256, UR267A/B, UR268, UR269, UR274A).
  - P11a se concentra en Berlín (7/16; p = 0,0014). Ese 0,0014 no sobrevive a Holm sobre plantillas × variables (≈ 54 pruebas).
  - Ninguna plantilla se asocia a canutos ni a fibra de camélido.
- **Plantillas ausentes:** P2 (censo toledano), P3, P10 (dinastía) y P12 (moneda colonial) dan 0 coincidencias. P1 (calles de edad) y P8b/c (días como valores) dan aciertos sueltos de exploración que no se replican. Coincide con `n_que_se_contaba`: no hay pirámides de edad en el corpus.
- **Artefacto detectado:** la «consolidación» KH0033 ↔ UR044 (P6b, p = 5·10⁻⁴) es una identidad del 100 % (54/54). Es el mismo quipu con dos números: SINTESIS ya registraba «KH0033 = UR1031 y UR044». Las demás P6b fuera de Puruchuco (QU013 → QU004) son coincidencias de valores pequeños (3, 3, 3…) que fallan las predicciones C4.

**Nivel:** que el corpus no contenga poblaciones de géneros coloniales reconocibles más allá de los archivos ya leídos está **apoyado con datos (negativo)**.

---

## 4. La clase no numérica

Los quipus examinados son UR178, UR179, UR180, UR050, UR052, UR054, UR055, AS076, JC012, UR203 y UR215 (`no_numericos.csv`).

- **0/11 coinciden con alguna plantilla.** Los mejores nominales son estos:
  - UR052 P6a (q = 0,027, pero p_corpus 0,20);
  - UR180 P1a (p_corpus 0,029, q = 0,053);
  - UR215 P10 (q = 0,037, p_corpus 0,29);
  - UR179 P3 (p_corpus 0,007), pero P3 quedó descartada.
- **Ceques para UR050 + UR055** (prerregistro A): la hipótesis venía de que 164 + 180 = 344 cae en «328–350 wakas» y de la propuesta de Urton de un par de quipus por mitad. Falla en las tres predicciones:
  - Rachas de color: 3 y 15, no las 18 y 23 esperadas. Cúmulos de canutos (OKR): 5 y 10.
  - No hay ciclo de 3 en las rachas de UR055 (p ≈ 1).
  - Fibra y colección distintas (camélido Soldi frente a algodón Museo Oro).
  - **Descartada.**
- **Padrón de nombres, calendario de tallas y lista de ceques:** ninguna plantilla explica la clase mejor que el azar.

**Nivel:** **apoyado (negativo)**. La lectura «tally/etiqueta» de `n_no_numericos` sigue siendo la más parsimoniosa.

---

## 5. Lecturas concretas y predicciones con datos no usados

Todas las predicciones se escribieron en `predicciones_preregistradas.md` antes de ejecutarlas. Son 56 pruebas con Holm conjunto (`predicciones.csv`).

### 5.1 Conjunto atado UR053A–E (Banco Central): registro tripartito jerarquizado — **apoyado**

- **Coincidencia:** P9a coincide en **UR053A (confirmación), UR053C (confirmación) y UR053D (exploración)**: tres de los cinco quipus del conjunto atado. UR053B y UR053E son pares W/R y llevan el AB en subsidiarias.
- **Lectura:** cada trío AB / W / R(B|L) es un registro de tres categorías jerarquizadas (la triada collana/payan/cayao de Urton), y **W lleva el valor principal**.
- **Predicción** (valores, que P9a no usa; los de UR053C ya los había visto en la tabla 8.1 de Urton): en UR053A y UR053D, la cuerda de la fase W es la mayor del trío.
- **Resultado:** W es la mayor en **12/15 (UR053A; p = 2,9·10⁻⁴; Holm 0,012)** y **22/23 (UR053D; p = 5·10⁻¹⁰; Holm 3·10⁻⁸)**. UR053C, ya visto, da 15/20. **No son copias**: la mejor fracción de valores idénticos entre pares es 0,02–0,12. Además, B y E también tienen W > R en sus pares.
- **Lo que no se sostiene:**
  - **No son ceques.** Hay 15, 20 y 23 tríos por quipu, no ~14 (41/3). Las magnitudes de W (40–2700) no son conteos de wakas.
  - **No hay jerarquía de sumas** dentro del conjunto (C5: P6b con el conjunto como hallazgo, p ≥ 0,06), pese a que A está en miles, D en cientos y B, C y E en decenas.
- **Conclusión:** el *formato* tripartito con categoría principal fija es un rasgo compartido por un archivo de 5 quipus, y **la categoría blanca es la cantidad principal en todos**. El contenido «ceque» no está apoyado.

### 5.2 Padrón por bandas de color fuera del Santa: UR1140 — **propuesto/apoyado**

- **Coincidencia:** P4r coincide en UR028 (Atarco), UR1114, UR1140 y HP033, además del Santa.
- **Predicción C1** (valores, que P4r no usa): si cada banda es una ficha de persona, la posición dentro de la banda ordena los valores.
- **Resultado:**
  - Los **6/6 del Santa** cumplen (η² 0,48–0,98; p ≤ 2·10⁻⁴), lo que confirma que la prueba ve el formulario del Santa.
  - Fuera del Santa solo cumple **UR1140** (Berlín, Nazca): 15 bandas de 7 cuerdas, η² = 0,42, p = 10⁻⁴, Holm 0,005.
  - UR028, UR1114 y HP033 **fallan** (η² ≤ 0,10).
  - **C1b:** UR1123, copia publicada de UR1114, tiene el mismo largo de banda (10) pero solo 6 bandas, y queda fuera de la puerta de P4r. Es parcial.
- **Lectura propuesta de UR1140:** 15 registros (personas o unidades) × 7 campos fijos, como las fichas de 6 campos del Santa.
- **Predicción pendiente:** otros quipus de Nazca de la colección de Berlín con la misma ficha de 7 deberían mostrar el mismo perfil de campos (campo k con la misma magnitud relativa).

### 5.3 Registro segmentado por eventos o unidades (P11, Guacrapaucar/wanka) — **propuesto**

- **Predicción C3** (valores, que P11 solo vio como colores): los bloques repetidos comparten perfil de categoría (un factor de escala por bloque, como en el registro wanka).
- **Resultado:**
  - Cumplen sin ser copias (< 50 % de celdas idénticas), todos con p = 0,001 y Holm 0,042:
    - **UR1131** (13 bloques de 10, ρ̄ = 0,37);
    - **UR1175** (42 × 5, ρ̄ = 0,47);
    - **UR1144** (15 × 4, ρ̄ = 0,77);
    - **UR1149** (12 × 4);
    - **UR1099** (11 × 3);
    - **AS178** (7 × 4);
    - **AS048** (11 × 4);
    - **UR172** (7 × 4).
  - Las referencias UR068 y UR006 también cumplen.
  - Fallan AS074, AS089, AS203, HP051_B, AS202 y UR1121. HP055, UR1057 y UR1088 cumplen, pero son copias internas (53–92 % de celdas idénticas).
- **Agrupamiento:** 6 de los 8 están en el **Museum für Völkerkunde de Berlín**, 4 de ellos de **Pachacamac**.
- **Lectura propuesta:** son libros con una lista fija de categorías repetida por evento o por unidad. La plantilla no distingue «evento» de «unidad».
- **Predicción pendiente:** si son eventos, la escala de los bloques debería tener tendencia monótona con el orden (el registro wanka decae en el tiempo); si son unidades, no. Hay que probarla con un nulo de orden de bloques en la siguiente ronda.

### 5.4 Otras predicciones (negativas)

- **MM001** (P9b_iv: grupos {9, 9, 9, 14} ±1; tasa base 1/651) como lista de 41 ceques: la suma de valores da 983 (se esperaba 300–360) y no hay ciclo de 3 (p = 0,10). **Descartada.**
- **C4:** las relaciones P6b nuevas son un duplicado (KH0033 = UR044) o ruido (QU013). **Nada fuera de Puruchuco.**

---

## 6. Amenazas y límites

1. **p_corpus ≤ 0,05 fija una cota** de ~5 % de coincidencias. Por eso los recuentos no son evidencia; solo lo son la replicación entre mitades, el agrupamiento corregido y las predicciones con datos no usados.
2. **Plantillas no validadas** (P1, P2, P7, P8b/c, P10, P11 y P12): sus aciertos solo son *propuestos*. Guaman Poma y las listas dinásticas se citaron de memoria (no están en el repo).
3. **KFG:** pierde cuerdas superiores y marcadoras (`n_detectores`), y la agrupación por espaciado no coincide con las bandas de color (Santa). Las revisiones P4r y P8ar se hicieron por eso. Cuentan como variantes y están documentadas.
4. **Resolución:** en los estadísticos con bucle el p mínimo es 5·10⁻⁵, y en P6b, 5·10⁻⁴. Con ~5700 pruebas por mitad, algunos aciertos reales pueden quedar por debajo de la potencia.
5. **Lo visto antes:** los conteos de UR050/UR052/UR054/UR055 y los valores de UR053C se vieron antes de las pruebas. Se declararon y se excluyeron como evidencia.

## 7. Niveles de evidencia

| Afirmación | Nivel |
|---|---|
| El método de plantillas reconoce Santa (P4r 5/6), Puruchuco (P6b 4/6), UR006 (P8ar) y UR053C (P9a) | **demostrado** (controles a priori) |
| Ningún género colonial aparece en exceso sobre la tasa base; ningún agrupamiento se replica en confirmación tras Holm | **apoyado (negativo)** |
| Los «censos» de Urton por distribución de valores no se distinguen de quipus de su tamaño | **apoyado (negativo)** |
| Ninguna plantilla explica la clase no numérica; los ceques para UR050 + UR055 y MM001 están descartados | **apoyado (negativo)** |
| UR053A/C/D comparten un formato tripartito con W como valor principal (predicción a ciegas en A y D) | **apoyado** |
| UR053 = quipus de ceques | **no apoyado** |
| UR1140 es un padrón de 15 fichas × 7 campos | **propuesto** (una predicción cumplida) |
| Libros de bloques repetidos con perfil común en Berlín/Pachacamac (UR1131, UR1175, UR1144…) | **propuesto** |
| Lectura «eventos» frente a «unidades» de esos bloques | **especulativo** |

---

## Para el coordinador

- **El método funciona como detector de formatos ya leídos.** Reconoce el Santa (P4r 5/6, tras una revisión por bandas de color), Puruchuco (P6b 4/6, incluidas las discrepancias 2908/2904 de Urton y Brezine), UR006 (P8ar, p = 5·10⁻⁵, solo tras revisar la unidad «cuerda de lazo + grupo») y UR053C (P9a). Incahuasi solo parcialmente: UR275 sí, UR278 sin referencia de corpus, UR266 no.
- **Como buscador de géneros nuevos, es negativo.** Hay 92 coincidencias en 8871 pruebas, y ninguna plantilla supera la cota del 5 % que impone p_corpus (razones 0–0,87). Ningún agrupamiento elegido en exploración se replica en confirmación tras Holm (mejor: P6a → Incahuasi, Holm 0,062).
- **Géneros ausentes:** censo por calles de edad (P1), censo toledano (P2), lista dinástica (P10), cuenta en pesos y reales (P12) y calendario de días como valores (P8b/c). La plantilla de unidades domésticas (P3) se descarta, porque los análogos censales de Urton no se distinguen de quipus de su tamaño (1/4).
- **Clase no numérica: 0/11 coincidencias.** La hipótesis de ceques para UR050 + UR055 (164 + 180 = 344 ≈ 328–350 wakas) falló las tres predicciones prerregistradas: rachas 3/15 frente a 18/23, sin ciclo de 3, fibra y colección distintas. Sigue en pie la lectura «tally/etiqueta».
- **Mejor resultado fuera de Incahuasi: el conjunto atado UR053A–E** (Banco Central).
  - Comparte el vocabulario W / R / AB, y la **cuerda W es la mayor del trío** en 12/15 tríos (UR053A, Holm 0,012) y 22/23 (UR053D, Holm 3·10⁻⁸), prerregistrado y sin copias entre ellos.
  - Es un formato tripartito jerarquizado compartido por un archivo. **No** es un sistema de ceques (15–23 tríos, no 14; magnitudes de miles) **ni** una jerarquía de sumas (C5 negativa).
- **Padrón fuera del Santa: solo UR1140** (Berlín, Nazca, 15 × 7) cumple la predicción de perfil de campos (Holm 0,005). UR028, UR1114 y HP033 coinciden por color, pero sus valores no tienen ficha. Lectura propuesta: 15 fichas × 7 campos.
- **Registro segmentado por eventos** (fuente Pärssinen, prioridad del coordinador):
  - 8 quipus sin copia cumplen que los bloques repetidos comparten perfil de valores (Holm 0,042 cada uno): UR1131, UR1175, UR1144, UR1149, UR1099, AS178, AS048 y UR172.
  - **6/8 son de Berlín, 4 de Pachacamac.** Es *propuesto*: la plantilla no tiene control y no distingue eventos de unidades.
  - **Siguiente prueba:** tendencia de la escala de los bloques con su orden, como en el decaimiento wanka.
- **Artefactos:**
  - KH0033 ≡ UR044 (identidad 54/54) aparece como «consolidación» si no se deduplica. Ya estaba en SINTESIS como alias.
  - El P4 por grupos KFG es ciego a las bandas del Santa: **no usar grupos KFG como registros cuando el registro se marca por color**.
- **Senderos bifurcados:** 30 variantes congeladas + 2 revisiones + 1 cambio de clave + 1 variante nueva (C5), con BH/Holm por mitad sobre ~5700 pruebas. Las 56 predicciones del paso 5 tienen Holm conjunto. Los conteos de UR050/UR052/UR054/UR055 se vieron antes de congelar y no cuentan como evidencia.
- **Siguientes pasos baratos:**
  1. Leer UR053A–E como archivo: qué es W, y si A (miles) agrega a D (cientos) por otra regla que no sea la suma de secciones.
  2. Probar la ficha de 7 de UR1140 en los demás quipus Nazca de Berlín.
  3. Tendencia temporal de los bloques de UR1131 y UR1175.
  4. Auditar en imagen las bandas de color de UR028 y UR1114, que coinciden por color pero no por valores.
