# 08 · Auditoría adversarial de las sumas: ¿es el 74 % de Medrano y Khosla un artefacto?

**Afirmación auditada** (equipo 01): «La prevalencia de sumas tipo Ascher (74 %) no se distingue del azar: con un detector laxo, 75,3 % de quipus tienen ≥1 relación y el nulo dentro de nivel predice 73,5 %. Tras control, solo 2–3 % de quipus tienen contabilidad interna significativa (estimación por potencia: 5–10 %).»

**Dictamen corto.** La afirmación **se sostiene en lo esencial**, pero por una razón distinta de la que da el equipo 01, y conviene corregir dos cosas de la formulación:
1. El 01 comparó su propio detector (`Fany`) con el 74 %. Son definiciones distintas: la coincidencia 75,3 ≈ 74 es casual. Con la **definición exacta del KFG** (reimplementada y validada aquí) el resultado se repite: 69,0 % observado frente a 66,1–67,8 % esperado por azar, y el **93–100 % de las relaciones KFG son esperables por azar**.
2. «No se distingue del azar» no equivale a «no hay contabilidad». La métrica del 74 % (≥1 relación, a cualquier distancia) **no tiene potencia**. Aunque se plantara una suma real en *cada* grupo de *cada* quipu, el recuento KFG solo detectaría el 24 % de los quipus (q<0,05). El 74 % no mide contabilidad. Mide sobre todo el tamaño del quipu y lo pequeños que son sus valores.
3. Las relaciones **locales y caras** (suma de los colgantes inmediatamente vecinos, valores ≥100) sí muestran un exceso claro: 200 frente a 83–87 esperadas (2,4×). Ese exceso se concentra en unos 14–20 quipus (**≈3 % del corpus**). Corregida por potencia, la prevalencia plausible de contabilidad local verificable queda en **≈2–11 % (central 4–7 %)**, en línea con el 5–10 % del 01.

Los propios Medrano y Khosla (pp. 18–19) **reconocen** que el recuento de sumas en sus pseudoquipus es «a veces mayor (bin-sampling y bin-sampling con jitter) y a veces menor (uniforme) que el observado». Su argumento contra el azar no es la prevalencia del 74 %, sino la **lateralidad 54/46** y la **cercanía de los sumandos**. El hallazgo del 01 no contradice, por tanto, el artículo. Contradice la *lectura* habitual del 74 % (incluida la de nuestro `docs/estado_del_arte.md`, que lo etiqueta como «apoyado con datos + simulación»).

Unidad: el quipu. Semillas fijas. Huecos (0 sin nudos) fijos en su sitio en todas las permutaciones. Corrección BH-FDR dentro de cada estadístico × nulo.

---

## 1. Qué es exactamente el 74 %

Fuentes: `source/02_ascher_sum_relationships.html` (código) y el artículo (Tabla 1, p. 4–5).

- 74 % = 482 de 650 quipus aparecen en `ascher_sum_relationships.csv`, es decir, tienen **≥1 caso de cualquiera de los tipos** (el artículo: «76 % de los quipus con nudos»). Los tipos son: suma colgante-colgante (PPS, 427 quipus), por color (261), indexada (228), subsidiaria = suma de colgantes (117), grupo-grupo, «bandas de suma» (mitad izquierda = mitad derecha del grupo) y **«grupo decreciente»** (valores que bajan aproximadamente en línea recta; **no es una suma**).
- De los 482, 447 entran por los cuatro tipos de suma de cuerdas. Los otros 35 entran solo por grupo-grupo (5), bandas (15) o decreciente (17). **15 quipus cuentan en el 74 % únicamente por tener un grupo «decreciente»**.
- **Regla PPS** (código `PendantSummer`):
  - la cuerda-suma vale >10 e iguala, de forma exacta, la suma de un tramo contiguo de colgantes situado a su izquierda o derecha **a cualquier distancia** y de **cualquier longitud**;
  - el tramo tiene ≥2 cuerdas (los huecos 0 cuentan como cuerdas) y la suma debe ser mayor que el número de cuerdas del tramo;
  - se queda con el primer inicio que alcanza el valor y, si ese tramo tiene una sola cuerda (un duplicado), abandona la búsqueda.
- **Reglas COL, IDX y SUB:**
  - COL: tramos de ≥3 cuerdas no nulas del mismo color «más largo»;
  - IDX: tramos de ≥2 cuerdas con el mismo índice en grupos contiguos, valor >5 y excluidos los múltiplos de 10 y de 100;
  - SUB: subsidiaria >10 = tramo de ≥3 colgantes, sin múltiplos de 10 <100.
  - En los tres tipos se toma el tramo más corto. Cada lado cuenta como una relación.

**Validación de la reimplementación** (`kfg.py`, `01_validar.py`):

| Tipo | Relaciones (nuestras / KFG) | Quipus ≥1 | Quipus con recuento idéntico |
|---|---|---|---|
| PPS | 8076 / 8088 | 428 / 427 | 98,6 % |
| COL | 3055 / 3023 | 262 / 261 | 98,3 % |
| IDX | 2358 / 2340 | 233 / 228 | 95,2 % |
| SUB | 886 / 767 | 133 / 117 | 94,6 % (desajuste menor, sin efecto en conclusiones) |

Con los cuatro tipos: 449 quipus en nuestra reimplementación y 447 en el KFG.

## 2. Revisión del código del equipo 01

**Correcto:**
- `stats_L0` resuelve bien los tramos adyacentes con sumas prefijas y `searchsorted` (lado izquierdo `S[j]=S[i]−a[i]`, derecho `S[k]=S[i+1]+a[i]`) y las fronteras de grupo con huecos.
- `Fany` no puede emparejar una cuerda consigo misma: un tramo que la contiene, con ≥2 sumandos no nulos, suma más que ella.
- Los nulos conservan el multiconjunto, dejan fijos los huecos y estratifican por nivel. El autotest pasa.
- Los p-valores empíricos llevan el +1, y el BH se aplica solo a los quipus testables.

**Problemas:**
1. **Comparación desigual.** `Fany` acepta cuerdas-suma de 1 a 10 (p. ej. 3 = 1+2 en cualquier parte), corta en 10 sumandos y no tiene el filtro «valor > nº de sumandos». No es el detector KFG, así que el 75,3 % no es una réplica del 74 %. La conclusión sobrevive con la definición exacta (§3), pero la cifra citada no prueba nada por sí misma.
2. **La métrica «≥1 relación» está saturada por construcción.** La prevalencia depende del tamaño del quipu, tanto en los datos como en el nulo (M2):

   | colgantes | n | observado | nulo M1 | nulo M2 |
   |---|---|---|---|---|
   | ≤10 | 122 | 17 % | 13 % | 16 % |
   | 21–40 | 149 | 81 % | 78 % | 80 % |
   | 81–160 | 92 | 99 % | 97 % | 97 % |
   | >160 | 63 | 100 % | 99 % | 99 % |

   «No se distingue del azar» es cierto, pero el estadístico tampoco podría distinguir un corpus 100 % contable (§5). El 01 debió decir «el 74 % no es evidencia», no «el 74 % es azar».
3. **Estadístico compuesto de baja potencia.** Suma recuentos de relaciones baratas (valores de 1 dígito) y caras con el mismo peso. Un estadístico ponderado por improbabilidad (§4) rinde más: 53 % frente a 34 % de potencia con φ=0,5. Aun así, detecta casi los mismos quipus (9 de mis 14 están en sus 13).
4. **Resolución del p-valor.** Con B=2000 y ~550 tests, BH exige ≥6 quipus en el p mínimo. Lo comprobé recalculando con B=20 000 (`06_refinar.py`): **no cambia** el número de significativos (13–15). No es un problema real, pero hay que comprobarlo.
5. **Estructura que el nulo destruye.** Barajar dentro del nivel destruye la autocorrelación local (bloques de valores iguales o parecidos) y el orden de magnitudes. Añadí un nulo M2 que **conserva el número de dígitos de cada posición**. Es el más duro para los recuentos KFG: elimina todo el exceso global, pero no el local (§3–4). Los nulos N3 y N4 del 01 no pueden detectar sumas dentro de un grupo pequeño. Con [x, c, x−c], 4 de los 6 órdenes conservan la relación. El 01 lo reconoce.
6. **Lo que el 01 hizo bien:**
   - pidió una tasa base, que el campo no tenía;
   - estimó la potencia con sumas plantadas;
   - distinguió la detección (2–3 %) de la prevalencia (5–10 %);
   - aisló las dos señales reales (cuerdas superiores; cierres de Incahuasi).

## 3. Relaciones KFG frente a tres nulos (`02_nulos.py`, `04_resumen.py`; B=1000)

Nulos (huecos fijos en los tres):
- **M0**: barajar todo el quipu.
- **M1**: barajar dentro de nivel.
- **M2**: barajar dentro de nivel × nº de dígitos.

| Estadístico (corpus) | Observado | E M0 | E M1 | E M2 | Fracción esperable por azar |
|---|---|---|---|---|---|
| PPS | 8076 | 8031 | 7913 | 8094 | **0,98–1,00** |
| COL (color) | 3055 | 2980 | 2831 | 2997 | 0,93–0,98 |
| IDX (indexadas) | 2358 | 2290 | 2226 | 2385 | 0,94–1,01 |
| IDX, nulo por columnas* | 2358 | — | — | 2118 | 0,90 |
| SUB | 886 | (2077) | 822 | 907 | 0,93–1,02 |
| PPS en cadena (un sumando es a su vez suma) | 4093 | 4255 | 4067 | 4104 | **1,00** |
| PPS con valor ≥100 | 1962 | 1668 | 1758 | 1882 | 0,85–0,96 |
| PPS adyacente (salvo huecos) | 873 | 756 | 721 | 711 | 0,81–0,87 |
| **PPS adyacente y ≥100** | **200** | 84 | 87 | 83 | **0,42–0,44** (p<0,001) |
| **PPS adyacente con coste local <0,01** | **64** | 10,5 | 12,4 | 13,0 | **0,16–0,20** (p<0,001) |
| **PPS adyacente con coste local <0,001** | **13** | 0,2 | 0,3 | 0,4 | **0,02–0,03** |

\* Nulo por columnas: baraja cada columna (mismo índice en el grupo) entre grupos (`05_idx_columnas.py`).

Quipus con ≥1 relación de los 4 tipos: **449 (69,0 %)**. Esperados: M0 440 (67,6 %), M1 430 (66,1 %), M2 441 (67,8 %). Solo PPS: 428 frente a 414–422.

**Lectura.**
- Cuando se buscan tramos a cualquier distancia y longitud, las sumas KFG son **casi exactamente** lo que dan los mismos valores en cualquier orden.
- Las **cadenas de sumas anidadas** tampoco superan el azar: 1,00.
- Lo que el azar no reproduce son las sumas **de los vecinos inmediatos con valores grandes**. Solo el **10,8 %** de las relaciones PPS del KFG son adyacentes. La distancia mediana entre cuerda-suma y sumandos es de 11 cuerdas (p90: 61). El 15,7 % tiene ≥10 sumandos y el 60 % tiene valor ≤50.

## 4. Coste por relación: caras frente a baratas (`03_relaciones.py`, `relaciones_pps.csv`)

**Definición del coste de una relación:** P(V ∈ W).
- V es un valor aleatorio del mismo quipu con el mismo número de dígitos, generado con un modelo de dígitos independientes por posición (estimado en el quipu, con suavizado de Laplace).
- W es el conjunto de sumas de tramos disponibles: **global** = cualquier tramo que permita la regla KFG; **local** = tramos que empiezan junto a la cuerda.

**Resultados:**
- **Coste global mediano: 0,95.** Para la relación KFG típica, un valor al azar de la misma magnitud tendría un 95 % de probabilidad de encontrar también algún tramo que lo iguale. Solo 33 de 8076 relaciones tienen coste global <0,05, frente a 15–31 esperadas: nada bajo M2.
- **Coste local** (solo las 873 adyacentes): mediana 0,146. Hay 64 relaciones <0,01 en 21 quipus y 13 <0,001 en 5 quipus.
- Las relaciones más caras son casi todas de Incahuasi y siguen el patrón x = (x−c) + c con c ≈ 46 o 47:
  - UR269: 9 relaciones, p. ej. 2214 = 2168 + 46 y 2675 = 2629 + 46;
  - UR275: 3096 = 47 + 107 + 46 + 2896;
  - UR266: 3618 = 47 + 1364 + 2207.

  A ellas se suman UR188 (24072 = 868 + 23204) y UR268 (9793 = 208 + 9585).
- **Clasificación:** «baratas» son las de valor ≤50, cualquier distancia o muchos sumandos (≈90 % del total KFG). «Caras» son las adyacentes con ≥3 dígitos (≈2–3 %).

## 5. Potencia (`07_potencia.py`)

Seguí el mismo plantado que el 01: en una fracción φ de los grupos de ≥3 colgantes, la última cuerda pasa a valer la suma de las anteriores del grupo. El test usa el nulo M2 con BH sobre todo el corpus.

| φ | PPS KFG (q<0,05) | PPS adyacente | Adyacente ≥100 | Σ −log₁₀ coste local (q<0,05 / p<0,05) |
|---|---|---|---|---|
| 0,10 | 0 % | 12 % | 14 % | 18 % / 36 % |
| 0,25 | 3 % | 26 % | 24 % | 34 % / 49 % |
| 0,50 | 9 % | 44 % | 38 % | 53 % / 61 % |
| 1,00 | **24 %** | 59 % | 45 % | 67 % / 70 % |

Con φ=0 no hay ninguna detección falsa.

**El recuento KFG no tiene potencia.** Con una suma real en cada grupo del corpus, solo el 24 % de los quipus da señal. Por eso el 74 % no sirve ni para afirmar ni para negar la contabilidad.

## 6. Quipus con contabilidad interna verificable (`06_refinar.py`, B=20 000 para los candidatos)

**Estadísticos locales** (adyacente, adyacente ≥100, coste <0,01, Σ −log coste), con q<0,05 tanto en M1 como en M2: **14 quipus**.
- Incahuasi: UR255, UR256, UR266, UR267A, UR267B, UR269, UR270, UR274B, UR275.
- Otros: AS006, AS199, UR118, UR119 (Paracas) y UR166 (Huando).
- Solo con M1: MM001; solo con M2: UR145.
- Coincidencias con el 01: 9 de sus 13 (N2).

**Definición KFG sin localidad**, con q<0,05 en M2: 8 quipus, casi todos por la vía IDX (KH0049, QU002, UR112, UR1120, UR1143, UR122, UR208), además de AS159 y UR269.
- Con el nulo por columnas, IDX no deja ninguno con q<0,05. Los mejores son KH0049 y UR208, ambos con p=0,0005 y q=0,07: candidatos, no hechos.
- Con M1, PPS y COL marcan 20 quipus, entre ellos UR231 (186 sumas frente a 135; es el quipu que Medrano y Khosla reconstruyen) y AS069. Ninguno sobrevive a M2: su exceso se explica por dónde están los valores grandes.

**Concentración del exceso.** El 79 % del exceso de sumas adyacentes ≥100 (92 de 117) y el 83 % del exceso de Σ −log coste están en los quipus significativos. El resto (~25 relaciones) se reparte en una cola fina.

**Unión con las señales del 01** (cuerdas superiores TA: AS001, AS007, QU009, QU015, QU016; cierre R7: UR1152): **20 quipus = 3,1 % del corpus.**

**Prevalencia estimada.**
- Exceso de p<0,05 en Σ −log coste (M2): 40 observados frente a 24 esperados de 476 testables, es decir +16 (IC aprox. 7–25).
- Dividido por la potencia con p<0,05 (0,36–0,70), da ≈10–70 quipus: **1,5–11 % del corpus, central ≈4–7 %**.
- Es compatible con el 5–10 % del 01. Vale **solo para sumas locales**. Las sumas no locales reales (totales en grupos-resumen alejados, por color, indexadas) no se pueden verificar con estos estadísticos: no es que estén ausentes, es que no se pueden comprobar.

## 7. Lateralidad (`08_lateralidad.py`)

Medrano y Khosla oponen al azar la asimetría 54/46. La repetí con nulos intra-quipu (B=500):
- observado: 53,9 % de las PPS a la derecha;
- M1: 50,0 % [49,2–50,7], p=0,002;
- M2: 52,1 % [51,5–52,7], p=0,002.

La asimetría **sobrevive**, pero **la mitad se explica por la posición de las magnitudes** (M2). El resto puede deberse al orden dentro de los grupos (valores decrecientes de izquierda a derecha, que el propio KFG cuenta como «relación»). No es una prueba de sumas intencionales. Nivel: **apoyado con datos como regularidad de orden; propuesto como «diseño contable»**.

## 8. Dictamen y niveles de evidencia

**Bien apoyado:**
- el 74 % (≥1 relación de Ascher de cualquier tipo y a cualquier distancia) **no es evidencia de contabilidad**;
- con la definición exacta del KFG, el 93–100 % de las relaciones y casi toda la prevalencia (69,0 % frente a 66–68 %) son tasa base;
- el estadístico carece de potencia (24 % aun con sumas en todos los grupos);
- 15 de los 482 quipus entran en el 74 % solo por un grupo «decreciente», que no es una suma.

En ese sentido, el 74 % **es un artefacto de la métrica**: no es un error de cálculo, sino un uso sin tasa base. Los propios autores admiten que sus pseudoquipus producen recuentos parecidos.

**Bien apoyado:**
- existe un exceso real de **sumas locales caras**: adyacentes ≥100, 200 frente a ~85 (2,4×); coste <0,001, 13 frente a 0,3;
- ese exceso se concentra en 14 quipus robustos a dos nulos, la mitad de Incahuasi.

**Apoyado con datos:**
- la contabilidad interna verificable alcanza a **≈3 % del corpus** (20 quipus, unión con las cuerdas superiores y cierres del 01);
- la prevalencia corregida por potencia está en **≈2–11 %** (central 4–7 %) para sumas locales.

**No bien apoyado:** sumas indexadas, por color, en cadena y subsidiarias como fenómeno de corpus. Ninguna supera los nulos de magnitud o de columna.

**Veredicto sobre el 01:**
- **Correcto en la conclusión** y en las cifras de detección y de potencia.
- **Incorrecto en la comparación**: `Fany` no es la definición de Medrano y Khosla, y la coincidencia 75,3 ≈ 74 es casual.
- **Impreciso en la inferencia**: «no se distingue del azar» debe decir «no es informativo». Lo que limita es la potencia de la métrica, no la ausencia de sumas.
- Debe corregirse la frase del `estado_del_arte.md` que da el 74 % como «apoyado con datos + simulación». La simulación del artículo respalda la lateralidad, no la prevalencia.

## Negativos
- Cadenas de sumas anidadas: 4093 frente a 4067–4255 (nada).
- Sumas por color, indexadas (con el nulo por columnas) y subsidiarias: ningún exceso de corpus robusto.
- PPS a distancia, incluso con valores ≥100: entre el 85 y el 96 % es azar.
- Los quipus JC de Incahuasi (23, en su mayoría <40 cuerdas) no muestran señal local; JC010 tiene q=0,11.

## Siguiente ronda
1. Un nulo que conserve la autocorrelación local (permutación por bloques de longitud k o intercambios entre vecinos) para separar «sumas» de «valores parecidos juntos».
2. Las relaciones caras de Incahuasi (x = (x−c) + c con c = 15, 46 o 47) son la mejor pista: comprobar si c coincide entre quipus atados (UR255–UR267A) y si se repite en los JC.
3. Probar sumas no locales con un estadístico de coste, por ejemplo grupos-resumen enteros (R5a/TA ampliados con tolerancia ±1 en las centenas, como permite el KFG para cuerdas superiores).
4. Repetir la lateralidad con un nulo que conserve la tendencia decreciente dentro de cada grupo.

## Archivos
- `kfg.py`: detectores KFG reimplementados, coste, nulos y autotest (`python kfg.py`).
- `01_validar.py`: validación frente a los CSV del KFG → `validacion_por_quipu.csv`.
- `02_nulos.py` → `nulos_por_quipu.csv`, `nulos_corpus.npz`.
- `03_relaciones.py` → `relaciones_pps.csv` (8076 relaciones con coste).
- `04_resumen.py` → `nulos_por_quipu_q.csv`, `salida_04_resumen.txt`.
- `05_idx_columnas.py` → `idx_columnas.csv`.
- `06_refinar.py` (B=20 000) → `refinado.csv`.
- `07_potencia.py` → `potencia.csv`.
- `08_lateralidad.py` → `salida_08_lateralidad.txt`.
- Orden de ejecución: 01 → 08. Todo con semilla fija.
