# Cuerdas superiores (`union = T`) y cordón principal

**Equipo:** t_cuerdas_superiores · **Fecha:** 18/10/2026
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `quipus.csv`, `grupos.csv`; validación externa con `data/external/data-science-khipu-article/data/ascher_sum_relations/sum_top_cords_relation.csv`.

---

## 1. Pregunta

¿Qué son las cuerdas superiores (`union = T`) y qué registran? Para cada quipu con cuerdas superiores: ¿la superior es la suma de qué cuerdas exactamente? ¿De un grupo contiguo, de las cuerdas de un color, de cuerdas alternas? ¿Qué implica esto sobre cómo se organizaban las categorías en el quipu?

## 2. Definiciones y datos

- **Cuerda superior (unidad):** cuerda de nivel 0 que (a) tiene `union = T`, o (b) tiene al menos un hijo de nivel 1 con `union = T`. El segundo caso existe porque en 9 quipus la marca T está en los colgantes que cuelgan de la superior, no en la superior misma (p. ej. `UR006 p24`, `AS215 p11`).
- **Grupo adyacente:** el grupo inmediatamente anterior o siguiente según `grupo`/`grupos.csv` (KFG agrupa por espaciado sobre el cordón principal). La superior suele estar sola en su propio grupo.
- **Suma de referencia:** suma de los valores de las cuerdas de **nivel 0** del grupo adyacente. Los valores 0 sin nudos se tratan como ausentes (`NaN`); los 0 con nudos cuentan como 0.
- **Cifras de base:** 154 cuerdas con `union = T` en 26 quipus (4,0 % de los 651). Esas 154 cuerdas producen **93 unidades superiores**: 82 son cuerdas T de nivel 0 y 11 son padres de colgantes T. **17 quipus** tienen al menos una T de nivel 0; en los otros 9 la marca T está solo en los colgantes de una superior no marcada (AS010, AS044, AS061, AS212, AS215, UR006, UR1051, UR186, UR201). De las 93, **73 tienen valor** y **20 están en blanco** (sin nudos).
- **Denominador estadístico:** 72 unidades con valor y al menos un grupo adyacente con ≥2 cuerdas de nivel 0.

## 3. Método

### 3.1 Familias de suma evaluadas

Para cada unidad superior y cada lado (anterior/siguiente):

| Familia | Definición |
|---|---|
| `full_l0` | todas las cuerdas nivel 0 del grupo adyacente |
| `full_all` | todas las cuerdas del grupo (todos los niveles) |
| `contig_l0` | cualquier sub-bloque contiguo (≥2 cuerdas) nivel 0 |
| `contig_all` | cualquier sub-bloque contiguo (≥2) en orden físico |
| `color_l0` | cualquier clase de color del grupo (≥2 cuerdas; en el control estricto, subconjunto propio) |
| `color_all` | idem, todos los niveles |
| `alt_l0` | posiciones pares o impares (subconjunto propio, ≥2 cuerdas) |
| `alt3_l0` | cada tercera posición (subconjunto propio, ≥2 cuerdas) |

Una unidad cuenta como acierto si **algún** lado adyacente cumple la regla. Se probaron ambos lados porque la literatura y los datos muestran superiores antes y después de su grupo (KFG: 50 relaciones exactas con el grupo anterior y 14 con el siguiente).

### 3.2 Modelo nulo

Permutación de valores **dentro de cada quipu**, con semilla fija:

- **N1:** se permutan los valores de las cuerdas de nivel 0 que no pertenecen a ninguna unidad superior. Se preservan: multiconjunto de valores del quipu, tamaños de grupo, posiciones, colores y valores de las superiores.
- **N2:** se permutan los valores de todas las cuerdas no superiores (todos los niveles), para las familias `*_all`.

Se usaron 2 000–3 000 permutaciones. El p-valor empírico es `(1 + #{nulo ≥ observado}) / (N + 1)`. Estadísticos: (a) total de aciertos; (b) número de quipus con ≥1 acierto; (c) media por quipu de la tasa de aciertos (cada quipu pesa igual, regla 1 del brief).

El nulo mantiene **fijos los valores de las superiores** y baraja solo los de las colgantes: pregunta si el valor observado de la superior se alinea con *su* grupo más de lo esperado, no si existen valores sumables en cualquier parte del quipu. Barajar dentro del quipu (y no en todo el corpus) preserva la escala de valores de cada quipu, que varía mucho entre quipus; un barajado global mezclaría escalas y haría el test menos interpretable.

### 3.3 Corrección múltiple

- **Primarias:** 7 familias (tabla anterior) → Holm.
- **Secundarias (color/alternos estrictos):** 5 familias → Holm.
- Los tests de subgrupos (tamaño 6, monocromía) son **exploratorios** y se reportan sin corrección, marcados como tales.

## 4. Resultados

### 4.1 Inventario: 26 quipus con cuerdas superiores

| Quipu | Grupos | T total | Unidades | Con valor | Blancas | Exactas (grupo previo) | Cuerdas exactas |
|---|---:|---:|---:|---:|---:|---:|---|
| AS006 | 12 | 28 | 6 | 6 | 0 | 4 | p7=105, p14=120, p28=138, p35=140 |
| AS007 | 37 | 16 | 10 | 10 | 0 | 4 | p20=131, p81=147, p96=80, p103=124 |
| QU009 | 16 | 6 | 6 | 6 | 0 | 4 | p70=83, p77=83, p116=50, p123=98 |
| AS001 | 4 | 3 | 2 | 2 | 0 | 1 | p7=101 |
| AS002 | 2 | 5 | 1 | 1 | 0 | 1 | p7=117 |
| AS003 | 2 | 2 | 1 | 1 | 0 | 1 | p7=76 |
| AS004 | 7 | 1 | 1 | 1 | 0 | 1 | p7=312 |
| AS072 | 14 | 8 | 8 | 5 | 3 | 1 | p23=40 |
| AS215 | 11 | 3 | 1 | 1 | 0 | 1 | p11=76 |
| QU014 | 46 | 16 | 16 | 6 | 10 | 1 | p7=541 |
| QU015 | 29 | 10 | 5 | 5 | 0 | 1 | p40=512 |
| QU016 | 17 | 5 | 5 | 4 | 1 | 1 | p24=129 |
| QU019 | 29 | 11 | 5 | 5 | 0 | 1 | p86=173 |
| UR186 | 17 | 2 | 1 | 1 | 0 | 1 | p24=75 |
| AS010 | 13 | 1 | 1 | 1 | 0 | 0 | — |
| AS044 | 28 | 1 | 1 | 1 | 0 | 0 | — |
| AS061_MA036 | 3 | 1 | 1 | 1 | 0 | 0 | — |
| AS212 | 13 | 2 | 2 | 2 | 0 | 0 | — |
| HP047 | 9 | 4 | 3 | 2 | 1 | 0 | — |
| KH0080 | 16 | 6 | 3 | 3 | 0 | 0 | — |
| QU003 | 10 | 4 | 4 | 2 | 2 | 0 | — |
| QU012 | 13 | 4 | 4 | 3 | 1 | 0 | — |
| UR006 | 63 | 9 | 1 | 0 | 1 | 0 | — |
| UR1051 | 10 | 2 | 1 | 1 | 0 | 0 | — |
| UR155 | 4 | 2 | 2 | 1 | 1 | 0 | — |
| UR201 | 18 | 2 | 2 | 2 | 0 | 0 | — |

**Totales:** 26 quipus, 154 cuerdas T, 93 unidades, 73 con valor, 20 blancas, 23 exactas en 14 quipus. Tres quipus (AS006, AS007, QU009) aportan 12 de las 23 exactas; los otros 11 quipus aportan 1 cada uno.

**Cordón principal:** no tiene valor numérico en estos datos (solo cuerdas colgantes tienen `tipo = p`). Es el soporte físico del árbol. La tabla completa con longitud, color y estructura del cordón principal está en `tabla_quipus.csv`. No se usa procedencia de museo como lugar de origen.

### 4.2 Resultado principal: cuando suma, la superior suma el grupo contiguo anterior

De 72 unidades evaluables, **23 (31,9 %; IC95 % 22,3–43,4 %) son exactamente iguales a la suma de las cuerdas de nivel 0 del grupo inmediatamente anterior**. Las 23 exactas son, en todos los casos, el grupo **anterior**; solo una (QU009 p70) también coincide con el siguiente, porque ambos grupos suman 83. Como el nulo permite acertar por cualquiera de los dos lados, el test es **conservador** respecto de la orientación: la señal real está aún más concentrada en el grupo anterior.

Ejemplos canónicos:

- `AS006 p7 = 105 = 5+24+9+47+10+10` (grupo de 6).
- `AS006 p14 = 120 = 6+28+12+51+8+15` (grupo de 6, tres colores).
- `AS006 p28 = 138 = 7+38+14+57+8+14`.
- `QU009 p123 = 98 = 7+21+6+38+15+11`.
- `QU014 p7 = 541 = 19+88+44+301+40+49`.
- `AS072 p23 = 40 = 30+10+0+0` (grupo de 4).

De las 23, **21 son cuerdas T de nivel 0** y **2 son padres de colgantes T** (AS215 p11 y UR186 p24). La tabla completa, con nombres y valores de cada cuerda, está en `tabla_exactas.csv` y se reproduce en el anexo A.

> **Advertencia de selección (importante).** Las 23 exactas coinciden con las 23 relaciones que KFG ya había curado en posiciones T. La muestra **no es un conjunto independiente** de superiores: está enriquecida por la curaduría. Por tanto, **23/72 no estima la prevalencia** de superiores sumatorias en el corpus; estima la fracción de unidades T que reproducen una relación ya conocida. El nulo sigue siendo válido para preguntar si la alineación con el grupo *anterior* es sorprendente dada la distribución de valores, pero **no elimina el sesgo de selección**. La evidencia independiente de esta tarea son, sobre todo, los controles negativos de color/alternancia y el hallazgo de cobertura de `union = T`.

### 4.3 Controles: nulo, p-valor y unidad de análisis

| Estadístico | Observado | Nulo (media) | Nulo p95 | p empírico |
|---|---:|---:|---:|---:|
| Aciertos totales (`full_l0`) | **23** | 2,41 | 4 | **0,0003–0,0005** |
| Quipus con ≥1 acierto | **14 / 25** | 2,40 | 4 | **0,0003–0,0005** |
| Tasa media por quipu | **0,309** | 0,082 | 0,103 | **0,0003–0,0005** |
| Subgrupo con algún grupo de 6 | **21 / 45** | 2,36 | 4 | **0,0005** |
| Subgrupo sin ningún grupo de 6 | **2 / 28** | 0,061 | 1 | **0,002** (exploratorio) |

- El enriquecimiento es ~9,5× sobre el nulo (23 vs 2,41).
- El efecto no depende de un solo quipu: 14 de 25 quipus evaluables tienen al menos una exacta; el nulo espera 2,4.
- **Corrección Holm (7 familias):** `full_l0` p=0,0005 → **p_Holm = 0,0035**; `contig_l0` p=0,0005 → 0,0035; `full_all` p=0,0005 → 0,0035; `contig_all` p=0,0025 → 0,005; `alt_l0` p=1,0 → 1,0. La regla principal sobrevive a la corrección. Las dos familias de color iniciales (`color_l0`, `color_all`) también dieron p=0,0005, pero están **contaminadas**: en un grupo monocromo el “subconjunto por color” es el grupo entero, así que miden lo mismo que `full_l0`. El control estricto de 4.5 (subconjunto propio de color) da **0/73**; por eso no se interpretan como evidencia de color.
- **`full_all` (todos los niveles) no es robusto a nivel de quipu:** 5/72 vs nulo 0,46, pero p de la media por quipu = 0,071. El nivel correcto es **nivel 0**, no el grupo completo con subsidiarias.
- **`contig_l0`:** 28/72 vs nulo 8,25 (p=0,0005). El exceso sobre `full_l0` son 5 sub-bloques post hoc (AS007 p57, QU012 p18/p67/p113, UR155 p24); ninguno es el grupo completo. Son coincidencias de búsqueda, no una regla distinta.

### 4.4 ¿Qué cuerdas exactamente? Tamaño y color de los grupos sumados

De las 23 exactas:

| Tamaño del grupo | n exactas | Comentario |
|---|---:|---|
| 4 cuerdas | 2 | AS072 p23, QU015 p40 (ambos con cuerdas en 0) |
| 6 cuerdas | 20 | 87 % de las exactas; el patrón canónico |
| 7 cuerdas | 1 | AS007 p96 |

- **Monocromía:** 7/23 exactas son grupos de un solo color; **16/23 son policromas** (2–4 colores). En los no-aciertos, 30/49 son monocromos. Es decir, los grupos que suman son **más policromos**, no menos (Fisher exacto 7/23 vs 30/49, OR=0,28, p=0,022, exploratorio). La coloración no es el criterio de la suma; si algo, el grupo sumado admite mezcla de colores.
- **Color de la superior:** coincide con el color del grupo en solo 6/23 exactas (y en varios casos porque el grupo es monocromo). No hay evidencia de que la superior “seleccione” las cuerdas de su propio color.
- **Niños T de la superior:** 10/23 exactas tienen hijos T, pero **ninguna** superior con ≥2 hijos T tiene como valor la suma de sus hijos (0/13). Entre las de un solo hijo T, solo AS044 p7=30 coincide con su único hijo: un caso trivial, no una suma de categoría. Los hijos T no son los sumandos; la suma está en el grupo hermano anterior. Esto es consistente con la idea de que la superior es una cuerda **sumaria** colocada tras el grupo, y sus hijos son un detalle de segundo nivel, no el grupo sumado.

### 4.5 Color y alternancia: resultados negativos

| Familia | Observado | Nulo | p | Holm (5) |
|---|---:|---:|---:|---:|
| `color_proper` (subconjunto propio de un color en el grupo) | **0 / 73** | 0,267 | 1,0 | 1,0 |
| `color_top` (cuerdas del color de la superior) | **0 / 73** | 0,075 | 1,0 | 1,0 |
| `color_quipu` (todas las nivel 0 de un color en el quipu) | 4 / 73 | 1,073 | 0,023 | 0,113 |
| `color_quipu_top` (todas las del color de la superior en el quipu) | **0 / 73** | 0,171 | 1,0 | 1,0 |
| `alt_l0` (pares/impares del grupo) | **0 / 73** | 0,585 | 1,0 | 1,0 |

*Nota:* el denominador de esta tabla es 73 unidades con valor; una de ellas no tiene grupo adyacente con ≥2 cuerdas y nunca puede acertar. El denominador principal de 4.3 es 72. La diferencia no cambia ninguna conclusión (todos los observados son 0).

- **No hay un solo caso** en que la superior sea la suma de un subconjunto propio definido por color dentro del grupo, ni de las cuerdas de su propio color, ni de posiciones alternas.
- Los 4 aciertos de `color_quipu` son: AS007 p57=17 (5 cuerdas W:LB), QU009 p7=33 (13 cuerdas B), QU012 p67=137 (27 cuerdas W), UR186 p24=75 (6 cuerdas W:BG). Tres son independientes de la regla de grupo; el de UR186 es el mismo grupo monocromo. Con corrección por 5 familias, p_Holm=0,113: **no significativo**. Se reportan como exploratorios, no como hallazgo.
- **Alternancia:** 0/73. El nulo esperaba 0,59; no hay ninguna señal. La organización no es “cuerdas alternas”.

### 4.6 Las que no suman: blancas, discrepancias y funciones heterogéneas

- **20/93 unidades están en blanco** (sin nudos): AS072 (3), HP047 (1), QU003 (2), QU012 (1), QU014 (10), QU016 (1), UR006 (1), UR155 (1). 16 de ellas tienen un grupo siguiente ≥2 y 15 un grupo anterior ≥2; 19/20 no tienen hijos T. Son compatibles con **marcadores de grupo o superiores sin total registrado**, no con sumas.
- **44 unidades con valor y grupo anterior ≥2 no son exactas.** De ellas, 8 están a ±10 del total del grupo y 1 a ±1. Ejemplos: AS007 p88=152 vs 153; AS006 p21=127 vs 118 (+9); AS006 p42=93 vs 102 (−9); AS001 p14=93 vs 83 (+10); QU014 p43=935 vs 925 (+10). Los desfases de ±9/±10 sugieren **errores de un nudo** (una decena) o valores mal decodificados, no una regla alternativa.
- **QU014** es el caso extremo: 16 unidades, 10 blancas, solo 1 exacta (p7=541). Es un quipu con muchas superiores que no funcionan como totales; probablemente marcadores o datos incompletos.
- **AS007** tiene 10 unidades, 4 exactas y varias near-miss; es el quipu con más superiores “parciales”.
- **Auditoría completa:** las 93 unidades, con grupo anterior y siguiente, suma, diferencia, número de hijos, banderas de contiguo/color/alterno y valor, están en `tabla_todas_unidades.csv`. Las 50 no exactas con valor se pueden revisar allí una por una; las 20 blancas están marcadas con `valor = NaN`.

### 4.7 Contraste con la curaduría de KFG: 86 relaciones

El archivo `sum_top_cords_relation.csv` de KFG (Medrano & Khosla 2024) contiene **86 relaciones candidatas en 29 quipus**, de las cuales **64 son exactas**. Su `summand_value` es exactamente la suma de las cuerdas nivel 0 del grupo sumando, lo que confirma que nuestra definición de “suma” coincide con la suya.

- En las **posiciones marcadas T**, nuestra regla reproduce **23/23 exactas** y **0 falsos positivos** (no detecta ninguna de las 22 no exactas). En los quipus que tienen T hay 30 exactas de KFG; las otras 7 están en grupos no marcados (AS044 6, UR186 1) y quedan fuera de nuestro conjunto T.
- Pero `union = T` solo cubre **16/29 quipus** y **23/64 exactas (36 %)** de la lista curada. Las otras 41 exactas quedan fuera de las posiciones marcadas T: 34 están en quipus sin ninguna T (UR118, UR119, UR087, UR1096, UR166, etc.) y 7 en quipus que tienen T en otro lugar (AS044 6, UR186 1).
- **Conclusión de cobertura:** `union = T` es un marcador **incompleto** de cuerda superior. Sirve para estudiar el fenómeno, pero no para listar todas las superiores del corpus. La regla aritmética (grupo contiguo nivel 0) sí se replica donde hay datos.
- **Posible semántica de T (propuesto):** las 23 exactas T son todas del grupo **anterior**; 13 de las 14 exactas “siguiente” de KFG están en quipus sin T; la restante es QU009 p70, que también coincide con el grupo anterior. Esto sugiere que `union = T` no marca simplemente “cuerda superior”, sino una variante de fijación/orientación (superior colocada después de su grupo). Es una hipótesis coherente con los datos, no una prueba.
- En la muestra curada de 64 exactas: 48/64 (75 %) son grupos de 6; 34 monocromos y 30 policromos. Es el mismo patrón que en nuestra muestra T (20/23 de 6; 16/23 policromos).

### 4.8 Cordón principal

- El cordón principal no tiene valor ni nudos en `cuerdas.csv`; es el eje físico. Longitudes y colores están en `tabla_quipus.csv`.
- **Color de la superior vs color del cordón principal:** 51/93 = 54,8 % coinciden (primer código de color). Parece alto, pero el valor esperado por la composición de colores de cada quipu es 49,2/93 = 52,9 %; p=0,36. **No hay evidencia de que la superior se coloree especialmente como el cordón principal.** Es un efecto de composición, no de diseño.
- No se puede asignar significado a la longitud del cordón principal con esta muestra (n=26, longitudes muy dispares, sin control de procedencia).

## 5. Controles y explicaciones alternativas

1. **Nulo explícito:** dentro de cada quipu, se preservan valores, tamaños de grupo, colores y posiciones; solo se rompe la alineación entre la superior y su grupo. El nulo reproduce 2,4 exactas donde se observan 23.
2. **Pseudorreplicación:** el test principal se agregó por quipu (14/25 quipus vs 2,4 esperados; media de tasas 0,309 vs 0,082). El efecto no es solo de AS006/AS007/QU009, aunque estos aporten 12/23.
3. **Comparaciones múltiples:** Holm sobre 7 familias primarias; la regla `full_l0` sobrevive (p_Holm=0,0035). Las familias secundarias se corrigen aparte; `color_quipu` no sobrevive (p_Holm=0,113).
4. **Sesgo de curaduría (la explicación aburrida):** las 23 exactas son **exactamente** las 23 relaciones exactas que KFG ya había curado en **posiciones T**. No son descubrimientos nuevos: son una **replicación** de la curaduría de KFG, ahora con nulo y con búsqueda exhaustiva de color/alternancia. La muestra no es aleatoria y KFG priorizó quipus legibles.
5. **Errores de datos:** Thompson (2025) documenta errores de valor, nudo y color en las bases heredadas. Los near-miss ±1/±9/±10 son compatibles con un nudo mal contado. Si se corrigieran, la tasa exacta subiría; no cambiaría la conclusión estructural.
6. **Agrupamiento:** `grupo` es una agrupación por espaciado del KFG, no una medida independiente. Pero la identidad aritmética no depende del algoritmo: la superior coincide con la suma de las cuerdas que KFG coloca en el grupo anterior. El riesgo es que KFG haya agrupado *post hoc* para que la suma cuadre; no hay evidencia de eso, pero no se puede descartar con estos datos.
7. **Tamaño muestral:** 26 quipus, 17 con T de nivel 0, 14 con exactas. Los subgrupos (sin grupo de 6: 2/28) son pequeños y exploratorios.

## 6. Resultados negativos (resumen)

- **Color:** 0/73 subconjuntos propios por color; 0/73 cuerdas del color de la superior; 0/73 en todo el quipu para el color de la superior. La hipótesis “la superior suma las cuerdas de un color” **no se sostiene**.
- **Alternancia:** 0/73; el nulo esperaba 0,59. **No se sostiene**.
- **Suma de los hijos T:** 0/13 superiores con ≥2 hijos T suman sus hijos; el único caso con un solo hijo (AS044 p7=30) es trivial. **No se sostiene** la lectura ingenua “superior = suma de los colgantes que cuelgan de ella”.
- **Grupo completo con subsidiarias (`full_all`):** 5/72 vs nulo 0,46, pero p de la media por quipu = 0,071; no robusto. **El nivel 0 es el nivel correcto.**
- **Color del cordón principal:** 54,8 % vs 52,9 % esperado, p=0,36. **Sin señal.**
- **Cobertura de `union = T`:** solo 36 % de las exactas curadas por KFG. **El campo T no es un inventario completo.**

## 7. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| En 23 unidades de 14 quipus, la superior es exactamente la suma de las cuerdas nivel 0 del grupo contiguo anterior | **Bien apoyado en este corpus** (identidad aritmética verificable) |
| En la muestra T, la alineación exacta es mucho más frecuente que la esperada por azar (23 vs 2,4; p<0,001; 14/25 quipus) | **Apoyado con datos, condicional a la muestra curada** (nulo explícito, agregación por quipu, Holm; no corrige el sesgo de selección) |
| Prevalencia de superiores sumatorias en el corpus | **No estimable con este diseño** (muestra seleccionada por KFG) |
| La regla reproduce las 23 exactas en posiciones T de KFG y 0 FP (no es replicación independiente: es la misma curaduría) | **Apoyado con datos**, con ese límite explícito |
| El grupo contiguo, y no el color ni la alternancia, define la categoría sumada | **Apoyado con datos** (0/73 en color propio y alternancia; 16/23 grupos policromos) |
| La superior funciona como total de categoría / suma de control | **Propuesto** (la aritmética lo apoya; la función administrativa no se deduce de la suma) |
| Las superiores blancas son marcadores de grupo | **Propuesto** (20/93 blancas, 19/20 sin hijos T; no hay prueba directa) |
| El color codifica una dimensión distinta de la categoría (tipo de bien, moiety, etc.) | **Especulativo** (no testeado aquí; solo se descarta como criterio de suma) |
| Generalización a todos los quipus andinos | **Especulativo** (muestra curada, 26 quipus, sesgo de conservación) |

## 8. Interpretación: ¿cómo se organizaban las categorías?

La imagen que emerge es la de un **sistema de categorías espaciales y jerárquicas**, no de categorías definidas por color:

1. **La categoría es un bloque contiguo de colgantes.** El grupo físico (espaciado sobre el cordón principal) es la unidad; la superior lo totaliza. Esto es consistente con un registro administrativo decimal: cada categoría ocupa un tramo del cordón, y su total se anota en una cuerda superior.
2. **El tamaño canónico es 6 colgantes.** 20/23 exactas y 48/64 exactas de KFG son grupos de 6. Los grupos de 4/7/8 existen, pero la señal fuerte está en los de 6. Esto encaja con los “grupos de seis” descritos por Locke (1927) y con la idea de un formato estándar de categoría.
3. **El color no define la suma.** Los grupos sumados son frecuentemente policromos (16/23), y no hay un solo caso de suma por subconjunto propio de color. El color probablemente codifica **otra dimensión** (tipo de bien, procedencia, estatus, moiety), no el límite de la categoría. Esta es una corrección importante a lecturas que ven el color como clave taxonómica principal.
4. **La alternancia no organiza la suma.** No hay evidencia de cuerdas pares/impares como subcategorías sumables.
5. **No todas las superiores son totales.** 20/93 están blancas y 50 con valor no cuadran (44 de ellas con grupo anterior ≥2); algunas parecen marcadores, otras tienen errores de un nudo (±9/±10). La categoría “cuerda superior” es **heterogénea**: total, marcador, o registro incompleto. Esto apoya la lectura de Medrano & Khosla (2024) de que las superiores son minoritarias y marcan quipus “de trabajo”, más que una solución universal.
6. **Los hijos T no son el grupo sumado.** La superior puede tener sus propios colgantes, pero no son los sumandos. La suma está en el grupo hermano anterior. Esto sugiere una jerarquía de dos niveles: el grupo de colgantes (categoría) y la superior (total), con los hijos de la superior como detalle adicional, no como base de la suma.

## 9. Limitaciones y siguiente ronda

- **Cobertura:** `union = T` solo marca 26 quipus y 36 % de las exactas curadas. Para un inventario completo hay que usar la lista curada de KFG (`sum_top_cords_relation.csv`) o detectar estructuralmente las superiores (grupo de 1 cuerda adyacente a un grupo de ≥2), y luego validar con la aritmética.
- **Muestra no aleatoria:** KFG prioriza quipus legibles; los 26 quipus T están concentrados en AS/QU/UR y en museos con buena documentación. No se puede generalizar sin una muestra estratificada.
- **Errores de datos:** conviene una auditoría de los near-miss ±1/±9/±10 contra las fichas y los nudos crudos; si se confirman errores, la tasa exacta sube y la interpretación se refuerza.
- **Función semántica:** la suma no dice *qué* se suma. Para eso hay que cruzar con etnohistoria (tributo, mitas, ganado) y con los quipus de archivo (Puruchuco, Santa). La estructura “grupo contiguo + total” es compatible con muchas semánticas.
- **Siguiente prueba sugerida:** repetir el análisis en los 29 quipus curados por KFG (no solo los 26 con T) con el mismo nulo, y comparar la tasa de exactas entre quipus con T, sin T y con superiores blancas. También probar si el grupo sumado coincide con el grupo *anterior* en todos los quipus de un mismo archivo (Puruchuco/Santa), lo que indicaría una convención local.

## 10. Para el coordinador

- **26 quipus** (154 cuerdas T) tienen cuerdas superiores; producen **93 unidades** (82 T de nivel 0 + 11 padres de colgantes T). **73 tienen valor; 20 están blancas.**
- **23/72 unidades evaluables (31,9 %; IC95 22–43 %) en la muestra T/curada** son exactamente la suma de las cuerdas **nivel 0 del grupo contiguo anterior** (no es una prevalencia del corpus: la muestra está seleccionada por KFG). El nulo dentro de cada quipu espera **2,4**; p≈0,0003–0,0005; **Holm 0,0035**. **14/25 quipus** tienen al menos una exacta (nulo 2,4).
- **La regla es de grupo contiguo, no de color ni de alternancia:** 0/73 subconjuntos propios por color, 0/73 del color de la superior, 0/73 alternos. Los grupos sumados son **policromos en 16/23** casos. El color no es el criterio de la categoría.
- **Tamaño canónico 6:** 20/23 exactas y 48/64 exactas curadas por KFG son grupos de 6. La señal fuerte está ahí; en grupos sin ningún 6 solo hay 2/28 exactas (p=0,002 exploratorio, n pequeño).
- **Los hijos T de la superior no son los sumandos:** 0/13 superiores con ≥2 hijos T suman sus hijos. La suma está en el grupo hermano, no en los colgantes de la propia superior.
- **`union = T` es un marcador incompleto:** cubre 16/29 quipus y solo 23/64 exactas de la lista curada de KFG. Nuestra regla reproduce 23/23 exactas en posiciones T y 0 falsos positivos, pero **no descubre nuevas**: replica la curaduría de KFG. Hay que usar la lista curada para el universo completo.
- **20/93 superiores blancas** y 50 con valor no exactas (44 con grupo anterior ≥2); varias near-miss ±1/±9/±10 sugieren errores de un nudo. La categoría “superior” es heterogénea: total, marcador o registro incompleto.
- **Nivel de evidencia:** identidad aritmética **bien apoyada** en 23 casos; enriquecimiento estadístico **apoyado con datos**; función de total/marcador **propuesta**; generalización **especulativa**.
- **Recomendación:** repetir el mismo nulo en los 29 quipus curados (no solo los 26 con T), auditar los near-miss contra nudos crudos y probar la convención anterior/siguiente por archivo (Puruchuco, Santa). El hallazgo estructural es sólido; la semántica de las categorías sigue abierta.

---

## Anexo A. Las 23 sumas exactas

| Quipu | Superior | Valor | Grupo (nivel 0) | Suma |
|---|---|---:|---|---:|
| AS001 | p7 | 101 | p1:4 + p2:39 + p3:4 + p4:40 + p5:8 + p6:6 | 101 |
| AS002 | p7 | 117 | p1:20 + p2:8 + p3:10 + p4:50 + p5:16 + p6:13 | 117 |
| AS003 | p7 | 76 | p1:4 + p2:10 + p3:37 + p4:7 + p5:14 + p6:4 | 76 |
| AS004 | p7 | 312 | p1:10 + p2:20 + p3:40 + p4:172 + p5:50 + p6:20 | 312 |
| AS006 | p7 | 105 | p1:5 + p2:24 + p3:9 + p4:47 + p5:10 + p6:10 | 105 |
| AS006 | p14 | 120 | p8:6 + p9:28 + p10:12 + p11:51 + p12:8 + p13:15 | 120 |
| AS006 | p28 | 138 | p22:7 + p23:38 + p24:14 + p25:57 + p26:8 + p27:14 | 138 |
| AS006 | p35 | 140 | p29:5 + p30:42 + p31:8 + p32:64 + p33:13 + p34:8 | 140 |
| AS007 | p20 | 131 | p14:4 + p15:47 + p16:17 + p17:50 + p18:3 + p19:10 | 131 |
| AS007 | p81 | 147 | p75:18 + p76:13 + p77:48 + p78:15 + p79:47 + p80:6 | 147 |
| AS007 | p96 | 80 | p89:0 + p90:6 + p91:12 + p92:26 + p93:4 + p94:28 + p95:4 | 80 |
| AS007 | p103 | 124 | p97:11 + p98:4 + p99:48 + p100:11 + p101:46 + p102:4 | 124 |
| AS072 | p23 | 40 | p19:30 + p20:10 + p21:0 + p22:0 | 40 |
| AS215 | p11 | 76 | p5:4 + p6:14 + p7:7 + p8:37 + p9:10 + p10:4 | 76 |
| QU009 | p70 | 83 | p64:3 + p65:8 + p66:18 + p67:30 + p68:12 + p69:12 | 83 |
| QU009 | p77 | 83 | p71:5 + p72:7 + p73:8 + p74:31 + p75:14 + p76:18 | 83 |
| QU009 | p116 | 50 | p110:2 + p111:14 + p112:5 + p113:18 + p114:4 + p115:7 | 50 |
| QU009 | p123 | 98 | p117:7 + p118:21 + p119:6 + p120:38 + p121:15 + p122:11 | 98 |
| QU014 | p7 | 541 | p1:19 + p2:88 + p3:44 + p4:301 + p5:40 + p6:49 | 541 |
| QU015 | p40 | 512 | p36:100 + p37:142 + p38:0 + p39:270 | 512 |
| QU016 | p24 | 129 | p18:15 + p19:16 + p20:58 + p21:16 + p22:11 + p23:13 | 129 |
| QU019 | p86 | 173 | p80:6 + p81:46 + p82:18 + p83:73 + p84:10 + p85:20 | 173 |
| UR186 | p24 | 75 | p18:12 + p19:4 + p20:38 + p21:19 + p22:0 + p23:2 | 75 |

**Notas del anexo:** AS215 p11 y UR186 p24 son unidades donde la marca T está en los hijos, no en la superior; las otras 21 son T de nivel 0. QU009 p70 también coincide con el grupo siguiente (ambos suman 83). Los grupos de AS007 p96 (7 cuerdas, 4 colores) y AS006 p14 (6 cuerdas, 3 colores) son los casos más claramente policromos.

## Anexo B. Archivos generados

| Archivo | Contenido |
|---|---|
| `01_explorar.py` | exploración inicial: T por quipu, grupo previo, sumas |
| `02_busqueda.py` | familias de búsqueda (contiguos, color, alternos) |
| `03_inventario.py` | inventario de unidades T / padres de T |
| `04_sumas.py` | evaluación por unidad y por familia |
| `05_nulo.py` | nulo de permutación, 7 familias, Holm |
| `06_color_alt.py` | controles estrictos de color y alternancia |
| `07_nulo_quipu.py` | nulo con estadísticos por quipu y subgrupos de tamaño |
| `08_tablas.py` | tablas finales |
| `tabla_quipus.csv` | 26 quipus con metadatos del cordón principal |
| `tabla_exactas.csv` | 23 exactas con cuerdas y valores |
| `tabla_todas_unidades.csv` | 93 unidades con todos los indicadores |
| `unidades_resultados.csv` | resultados completos por unidad |
| `nulo_resumen.csv`, `color_alt_resumen.csv`, `nulo_quipu.json` | resultados de los controles |

**Semillas:** 20261017 (nulo principal), 20261018 (color/alternos), 20261019 (nulo por quipu). **Permutaciones:** 2 000–3 000. Todos los scripts son reproducibles desde la raíz del repo con `python analisis/ds/t_cuerdas_superiores/<script>.py`.
