# 22_formularios — diseño congelado del detector de «formulario con clave de reparto»

Congelado el 2026-10-18, **antes** de correr el detector sobre el corpus.

Antes de congelarlo solo se miraron estas cosas, todas de casos ya publicados en SINTESIS:
- las secuencias de colgantes de los controles UR053A/C/D;
- los tamaños de grupo de UR270/UR278;
- el Friedman ya publicado de UR278.

Lo que se cambie después de correrlo se anotará en `informe.md` como desviación.

## 0. Datos y normalización

- **Fuente:** `analisis/datos/cuerdas.csv`, `quipus.csv` y `grupos.csv`. Para los números de inventario se lee `MUSEUM_NUM` de `khipu.db` en modo solo lectura, con el cruce `OKR_NUM = quipus.okr`.
- **Unidad:** colgantes de nivel 0, ordenados por `orden`, con su `grupo`. Si el valor falta, se toma 0. Las subsidiarias no entran: un formulario que cambia de formato (AB subsidiaria en UR053B) queda fuera por diseño.
- **Color fino:** `re.sub(r'\([^)]*\)','',s).strip()` (el código completo, también los mezclados como `W/W:MB`).
- **Color grueso:** la primera letra del color fino. Así RL, RB y RD pasan a R, y AB, MB y KB quedan distintos.

## 1. Bloques candidatos dentro de un quipu

Hay dos familias, y k va de 2 a 12 en las dos.

- **P_k (posicional).** Los bloques son los grupos con exactamente k colgantes. La clave es la posición dentro del grupo y el color no se usa.
- **C_m (cromática), con resolución fina y gruesa.**
  - m es una secuencia contigua de k colores **dentro de un grupo** (no cruza fronteras de grupo) y tiene al menos 2 colores distintos.
  - Las ocurrencias se toman sin solaparse, de izquierda a derecha.
  - Los bloques son esas ocurrencias. La clave es la posición dentro del motivo, que equivale al color.

**Condiciones de un candidato válido:**
- al menos 3 bloques con suma > 0;
- como máximo el 50 % de las celdas en 0;
- (n−1)(k−1) ≥ 2.

Si dos candidatos tienen exactamente el mismo conjunto de cuerdas, se cuentan una sola vez (p. ej., fino y grueso idénticos).

## 2. Estadísticos por candidato (matriz V, n bloques × k posiciones)

Se trabaja con Y = log(1+V) y un ANOVA de dos vías sin interacción: bloque + posición.

- **(i) Clave.** Efecto de posición: F_col = MS_pos / MS_res, con p paramétrico. Pregunta: ¿las posiciones guardan cuotas estables de bloque a bloque una vez quitada la escala del bloque?
- **(ii) Registro.** Coescala de bloques: F_fila = MS_bloque / MS_res. Pregunta: ¿los valores de un mismo bloque suben y bajan juntos, de modo que el bloque es una unidad o registro?
  - Su p se calcula con el **nulo 2**: barajar valores **entre bloques**, columna por columna. Es una permutación independiente de cada columna, que conserva la distribución de cada posición y rompe el bloque. Se hacen 999 réplicas.
- **Perfil (clave de reparto).** Media de las filas centradas de Y (clr de log1p). Para el informe también se da la cuota media V/Σ por posición.
- **Banderas descriptivas** (no cambian la decisión):
  - «total+partes»: una posición es igual a la suma de las demás (±1) en ≥ 50 % de los bloques;
  - «lista ordenada»: ≥ 80 % de los bloques son monótonos en el mismo sentido que el perfil;
  - «filas casi idénticas»: ≥ 50 % de los pares de bloques son iguales.

## 3. Decisión por quipu

- **p_q = min(1, m · min p_col)**, donde m es el número de candidatos válidos del quipu (Bonferroni dentro del quipu, que corrige la búsqueda).
- **BH y Holm** sobre p_q de **todos** los quipus con m ≥ 1.
- **Q, formulario detectable:** q_BH < 0,05.
  - Su tipo es el de la familia del mejor candidato.
  - Si es cromático, además debe pasar el **nulo 1**. Se barajan los colores entre los colgantes de nivel 0 del quipu, con valores y grupos fijos, y se repite la búsqueda C completa; el estadístico es el mínimo p_col entre los candidatos C. Se hacen 199 réplicas y se exige p_n1 < 0,05. Si no lo pasa, el quipu baja a «Q posicional» si su mejor P también cumple con q_BH, y si no, a «no».
- **Q+, formulario de registros:** Q, y además el mejor candidato tiene coescala con p del nulo 2 < 0,05.
- **Control negativo (quipus barajados).** Se corre el pipeline completo, con BH incluido, sobre 3 corpus barajados de cada tipo:
  - (N1) colores barajados dentro de cada quipu, contando solo las detecciones cromáticas;
  - (N3) valores barajados entre todos los colgantes de nivel 0 del quipu, con colores y grupos fijos.

  Se espera ≈ 0 detecciones en N3 y ≈ 0 detecciones cromáticas en N1. Si no es así, el p paramétrico está mal calibrado y se pasa a p por permutación.
- **Controles positivos obligatorios.** Deben salir Q:
  - UR278 y UR270 (Incahuasi), con el P_9 como candidato válido;
  - UR053A, UR053C y UR053D, con un C de W–R–AB (fino o grueso) como candidato válido.

  Si fallan, el detector se declara insensible y se informa así; no se reajusta.

## 4. Archivos

Un quipu puede pertenecer a varios archivos.

- **conjunto:** el mismo prefijo `^[A-Z]+\d+` en kfg (UR053A–E → UR053), con ≥ 2 quipus.
- **procedencia:** la misma `procedencia`, excluidas Unknown, unknown, Peru y los vacíos, con ≥ 2 quipus.
- **museo_consecutivo:** el mismo museo y el mismo prefijo alfabético del número de inventario, con el entero principal a distancia ≤ 1. Se toman las componentes conexas de ≥ 2 quipus.

## 5. Mitades y confirmación por archivo

- **Partición.** Se ordena la lista de kfg y se aplica `np.random.default_rng(20261018).permutation`. La primera mitad (redondeo hacia arriba) es la de **exploración (E)** y el resto la de **confirmación (C)**. Una sola etiqueta por quipu.
- **Exploración.**
  - Para cada archivo A y cada tipo τ (P_k, C fino o C grueso) que aparezca con ≥ 3 bloques en ≥ 1 quipu E de A, se juntan los bloques E.
  - Perfil π_E: la media por quipu del perfil clr, promediada entre quipus con el mismo peso.
  - p_E: F_col del ANOVA conjunto.
  - Pasan a confirmación los τ con p_E < 0,001, como máximo 3 por archivo y familia (los de menor p_E).
- **Confirmación.**
  - Se toman los bloques de τ en los quipus C de A, con ≥ 2 bloques por quipu y ≥ 3 en total.
  - Estadístico: T = Σ_bloques ⟨clr(bloque), π_E⟩.
  - Nulo: permutar las posiciones dentro de cada bloque de forma independiente, con 20 000 réplicas, para obtener p_C.
  - Si τ no aparece en C, el resultado es «no confirmable».
  - Se aplican Holm y BH sobre todos los τ llevados a confirmación. **Formulario de archivo confirmado:** q_BH < 0,05 («apoyado») o Holm < 0,05 («bien apoyado» si además es local).
- **Especificidad: local frente a genérico.**
  - Se calcula la concordancia media por bloque ⟨clr, π_E⟩ en los quipus de fuera, que comparten τ pero no comparten ningún archivo con A.
  - Se comparan con Mann-Whitney unilateral las concordancias medias por quipu de C(A) y de fuera.
  - Es **local** si p < 0,05, y **genérico** si fuera también concuerda (media > 0 y p de signo < 0,05) y la diferencia no es significativa.
- **Escala:** razón máx/mín del total medio de bloque entre los quipus del archivo que tienen τ.
- **Copias y sumas:** pares del archivo listados en `analisis/14_copias/pares_resumen.csv`, con su tipo.

## 6. Predicción que refutaría el modelo

- **Universo:** motivos C finos con k ≥ 2 que, en un quipu, son candidatos válidos con p_col < 0,05 nominal.
- **Pares no relacionados.** Los dos quipus deben cumplir todo esto:
  - procedencias conocidas y distintas;
  - prefijos de conjunto distintos;
  - no son museo_consecutivo;
  - no son un par de 14_copias.
- Para cada par no relacionado que comparte motivo fino idéntico se calcula la distancia de Aitchison d entre los perfiles clr.
- **Umbral d\*:** la distancia máxima entre los perfiles de UR053A, C y D sobre su motivo W–R–A grueso. Es el «reparto parecido» que el coordinador aceptó como mismo formulario.
- **Estadístico S:** el número de pares no relacionados con d ≤ d\*.
  - Nulo: permutar al azar las posiciones de uno de los perfiles de cada par, con 2 000 réplicas.
  - Además se compara con los pares del mismo motivo dentro de un mismo archivo.
- **Criterio de refutación (congelado).**
  - Basta un par no relacionado con k ≥ 3, ambos quipus Q y ambos con p_col < 0,01 en ese motivo, y d ≤ d\*, **y además** S en exceso sobre el nulo (p < 0,05) entre los pares con k ≥ 3.
  - Las coincidencias con k = 2 (una sola razón) se informan, pero no refutan.

## 7. Tasa

- Fracción de quipus con ≥ 30 cuerdas (todas, de cualquier nivel) que son Q, Q+, Q cromático y que pertenecen a un formulario de archivo confirmado.
- Se compara con los géneros coloniales de `11_rosetta` (Medrano, 72 transcripciones): ¿qué fracción son listas «categoría + número» con rubros repetidos por unidad, que es lo que generaría un formulario?

## 8. Niveles

- **Bien apoyado:** Holm < 0,05, con los nulos pasados y replicado en confirmación.
- **Apoyado:** BH < 0,05 y confirmado.
- **Propuesto:** solo en exploración, o solo nominal.
- **Especulativo:** interpretación sin prueba.
