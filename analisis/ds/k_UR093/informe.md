# UR093 (KH0329) — lectura profunda de un quipu

**Autor:** equipo k_UR093 · **Fecha:** 18-oct-2026 · **Carpeta:** `analisis/ds/k_UR093/`

---

## 1. Pregunta

¿Qué estructura tiene UR093 (1227 cuerdas, procedencia desconocida), qué aritmética interna contiene y cuál es la lectura más probable de su contenido? La tarea incluye reconstruir grupos, subsidiarias, colores, valores, cuerdas superiores y uniones; buscar toda la aritmética interna contra un nulo explícito; proponer el tipo de registro; y señalar lo que no encaja.

## 2. Datos y método

- **Fuente primaria:** `analisis/datos/cuerdas.csv`, `grupos.csv` y `quipus.csv` (KFG). **Contraste independiente:** `data/external/open-khipu-repository/data/khipu.db` (OKR, `khipu_main`, `cord`, `knot_cluster`). Los conteos de cuerdas (1227), niveles (223/956/48) y cuerdas con nudos (338) coinciden exactamente entre KFG y OKR.
- **Metadatos:** UR093 = KH0329, Museo Temple Radicati, nº s/n, apodo «Calliope», procedencia y región *Unknown*, cordón principal de 72,0 cm, color AB:MB:KB, torsión S. **No se usa el museo como lugar de origen** (regla 6 del brief). El museo alberga 28 quipus (KH0321–KH0348); los seis del valle del Santa son KH0323–KH0328 = UR087–UR092, **no** UR093.
- **Unidad de análisis:** el quipu (n=1). Por tanto **no hay replicación entre quipus**: todos los tests son internos y sus p-valores describen estructura dentro de este objeto, no generalización poblacional. Se dice explícitamente en cada caso.
- **Nulo:** 1000 permutaciones de los valores, semilla 0. Se usan dos variantes: (a) permutación global de los 1227 valores; (b) permutación estratificada por nivel (0/1/2), que preserva la tasa de ceros y la estructura jerárquica. Para la correlación colgante–subsidiarias se usa además un nulo que permuta los valores **dentro de cada grupo** (control de confusión ecológica). Para color y morfología se permutan colores/etiquetas preservando sus frecuencias marginales.
- **p empírico:** `(1 + #{nulo ≥ obs}) / (B+1)`, unilateral salvo donde se indica bilateral.
- **Corrección múltiple:** Holm por familia de tests; se reporta `p_holm`. Con 1000 permutaciones el p mínimo posible es 0,001.
- **Ceros:** `valor = 0` con `nudos` vacío se trata como **ausente**, no como cero real (regla 6). En UR093 no hay ninguna cuerda con valor 0 y nudos no vacíos, así que la distinción no afecta a las sumas, pero sí a la interpretación de las 889 cuerdas en blanco.

**Scripts reproducibles** (todos en esta carpeta, ejecutar desde la raíz del repo):

| Script | Contenido |
|---|---|
| `20_estructura.py` | conteos básicos, grupos, niveles, colores, largos |
| `21_perfil.py` | perfiles de colgantes/subsidiarias, posiciones, valores |
| `22_modulo8.py` | módulo de 8 subsidiarias: colores y valores por posición |
| `23_corpus.py` | comparación morfológica con los 619 quipus del OKR |
| `24_aritmetica_nulo.py` | batería aritmética + nulo + Holm (`resultados_aritmetica.csv`) |
| `25_color_nudos.py` | pares de color 6/7, dirección y posición de nudos |
| `26_refinados.py` | suma informativa, correlación, posición del máximo, alturas |
| `27_controles_estructurales.py` | nulos del módulo 8 y del par de color |
| `28_dentro_grupo.py` | control dentro de grupo, chi², anomalías |
| `29_extra.py` | seriación, patrones, razones, bloque R/V, punto de unión |

---

## 3. Estructura reconstruida

### 3.1 Esqueleto

| Nivel | Cuerdas | Denominación KFG | Unión dominante |
|---|---:|---|---|
| 0 | 223 | colgantes | R (217), U (5), V (1) |
| 1 | 956 | subsidiarias | V (759), R (189), U (8) |
| 2 | 48 | sub-subsidiarias | V (47), U (1) |
| **Total** | **1227** | | |

- **12 grupos** sobre un cordón principal de 72 cm; posición de grupo entre 0,5 y 58,0 cm. Tamaños: 21, 3, 14, 18, 20, 39, 16, 18, 24, 16, 15, 19 colgantes (suma 223).
- **No hay cuerdas superiores:** `union = T` aparece **0 veces**. Tampoco hay uniones «doble» ni cordón superior sumatorio. Por tanto **no existe una cuerda padre de grupo** contra la cual contrastar la suma del grupo; la hipótesis «grupo = suma de grupos» no es contrastable en este objeto.
- **Torsión:** 1224 cuerdas en S, 1 en U, 2 sin dato. La torsión **no discrimina nada** aquí (99,8 % S).
- **Terminaciones:** K 994, R 120, B 96, U 11, C 6. Predominio de nudo terminal K.
- **Largos:** colgantes 40,1 cm de media (mediana 41,5; rango 0–77,5); subsidiarias 26,0; sub-subsidiarias 24,6.

### 3.2 Grupos

`grupos_resumen.csv` contiene la tabla completa. Resumen:

| Grupo | Colgantes | Σ valor colgantes | Colgantes en blanco | Subsidiarias | Unión de subsidiarias |
|---:|---:|---:|---:|---:|---|
| 0 | 21 | 52 | 12 | 24 | V |
| 1 | 3 | 2 | 1 | 0 | — |
| 2 | 14 | 31 | 0 | 66 | V (1 U) |
| 3 | 18 | 44 | 12 | 41 | V |
| 4 | 20 | 29 | 3 | 101 | V (1 U) |
| 5 | 39 | 47 | 18 | 146 | V (2 U) |
| 6 | 16 | 55 | 1 | 88 | **R (88/88)** |
| 7 | 18 | 27 | 3 | 93 | **R (91/93)** |
| 8 | 24 | 139 | 0 | 86 | V (2 R) |
| 9 | 16 | 49 | 2 | 106 | V |
| 10 | 15 | 48 | 1 | 109 | V (2 U) |
| 11 | 19 | 80 | 6 | 96 | V (8 R, 1 U) |

Los grupos **no** son homogéneos: la tasa de colgantes en blanco va de 0/24 (grupo 8) a 18/39 (grupo 5); χ² grupo × (valor>0) p < 0,001. La suma por grupo va de 2 (grupo 1) a 139 (grupo 8), sin relación con el número de colgantes (grupo 5 tiene 39 colgantes y suma 47; grupo 8 tiene 24 y suma 139).

### 3.3 Jerarquía y módulo de 8

- **121 de 223 colgantes (54,3 %) tienen subsidiarias.** Distribución del número de hijas: 1 → 5 casos, 7 → 2, **8 → 90**, 9 → 23, 10 → 1. Entre los colgantes *con* hijas, el 74,4 % tiene exactamente 8.
- **6 subsidiarias (todas en la posición s1) tienen a su vez 8 sub-subsidiarias** (48 cuerdas de nivel 2). Son `p32s1, p70s1, p108s1, p141s1, p182s1, p214s1`. Es decir, hay un módulo 8×8 completo en 6 columnas.
- **El módulo de 8 es un rasgo raro en el corpus:** de 512 quipus del OKR con ≥10 colgantes, solo 18 tienen algún colgante con 8 hijas y solo 3 tienen ≥5 (`KH0329`, 90/223; `KH0568`, 24/30; `KH0349`, 7/332). UR093 es, además, el **2.º quipu más grande del OKR** (1227 cuerdas; mediana del corpus 42,5; el mayor es KH0082 con 1831).
- **Nulo A (reparto aleatorio de 956 subsidiarias entre 121 colgantes):** esperados 5,9 colgantes con 8 (máx. 15 en 1000 simulaciones); observados 90. p = 0,001 (mínimo alcanzable). La regularidad de 8 no es un artefacto del tamaño.
- **Las hijas de un módulo se unen casi siempre en un solo punto:** 118 de 121 colgantes con hijas tienen **una sola altura de unión** para todas ellas; solo 3 tienen dos alturas. La mediana global de la altura de unión es **15,5 cm** (rango 0–19,5). En el corpus OKR la mediana de la altura de unión de subsidiarias es **2,0 cm** (cuartiles 0,5–6,1): UR093 es un extremo de **ramificación a media cuerda**. Esto, más las puntas y nudos alineados (3.7), indica que cada colgante + sus 8 hijas se construyó como un **ramillete unitario**, no como cuerdas independientes.

### 3.4 Cuerdas en blanco

**889 de 1227 cuerdas (72,5 %) no tienen ningún nudo:** 59/223 colgantes (26,5 %), 800/956 subsidiarias (83,7 %), 30/48 sub-subsidiarias (62,5 %). Es el rasgo más llamativo del objeto y no es un problema de la base: OKR registra exactamente las mismas 338 cuerdas anudadas. La tasa de llenado es 27,5 %.

La lectura «la mayoría de las subsidiarias son campos vacíos» es la explicación aburrida y compatible con los datos; la alternativa «se perdieron los nudos» no lo es, porque las terminaciones son K/B/R (cordones acabados), no fibras rotas, y las longitudes son completas (26 cm de media).

### 3.5 Colores

- 147 cadenas de color distintas (el campo mezcla códigos, rangos `0.0-9.0` y combinaciones `:` `-` `/`), lo que obliga a normalizar. Entre las subsidiarias, **825/956 son blancas**; los colores saturados se concentran en posiciones concretas (abajo).
- En los colgantes, el color primario se reparte: blanco 83, marrón 69, rojo 24, amarillo 14, verde 8, azul 2, otros 23. **No hay asociación color primario × tener valor** (χ² p = 0,27): el color no marca qué cuerdas llevan número.
- **Par de color en las posiciones 6 y 7 del módulo de 8:** la posición 6 es verde en **103/116** módulos (tasa base de verde en subsidiarias: 11,4 %); la posición 7 es «barber pole» (contiene `:`) en **109/116** (tasa base 12,7 %). Nulo de permutación de colores: p = 0,001 en ambos casos. En ~50 % de los módulos el verde de la posición 6 coincide con el componente secundario del `W:verde` de la 7 (p. ej. `BG` + `W:BG`). Las notas de campo lo confirman cualitativamente: «122s6 darker than 122s7», «s6 much more solid than s7… same components».
- Las posiciones 1–5 y 8 son casi siempre blancas. Es decir, el módulo no es «8 campos equivalentes»: **5 blancos + 1 verde sólido + 1 verde rayado + 1 blanco**.

### 3.6 Unión R/V: un bloque estructural, no ruido

La unión no separa solo colgantes de subsidiarias (217 R / 1 V entre colgantes; 759 V / 189 R entre subsidiarias). **Las 189 subsidiarias R se concentran en los grupos 6 y 7:** 179 de 181 subsidiarias de esos dos grupos son R, frente a 10 de 775 en el resto. Hipergeométrico: p ≈ 2×10⁻⁷¹ para el grupo 6 y 9×10⁻⁷¹ para el 7 (descriptivo, no corrige dependencia interna). Es un **bloque contiguo** (grupos 6–7, posiciones 34,5–38,5 cm sobre el cordón) atado por el reverso, mientras el resto lo está por el anverso.

Esto coincide con la línea de FitzPatrick (2024), que propone leer recto/verso como *marcado/no marcado*, y con la de Hyland y Ware (2014) sobre dirección de nudo. Aquí, sin embargo, el patrón es de **bloque de construcción** (dos grupos completos), no de cuerdas individuales marcadas; la explicación aburrida —el artesano ató esa sección desde el otro lado— no puede descartarse.

### 3.7 Nudos y direcciones

- 347 racimos de nudos en 338 cuerdas: 329 cuerdas con 1 racimo, 9 con 2 (las 9 son los valores altos: p27, p40, p136, p151, p151s3, p151s7, p178, p190, p221).
- Tipos: **E 184, L 139, S 24**. La dirección está **casi determinada por el tipo**: E → Z en 172/184; L → S en 135/139; S (simple) → S en 22/24. Solo hay **18 excepciones** (12 E en S, 4 L en Z, 2 S en Z). Por tanto la dirección **no es un canal binario libre** en este quipu; las excepciones son anomalías, no una codificación paralela.
- **Alturas alineadas:** si se mide la altura absoluta desde el cordón principal (posición de unión + posición del nudo), los nudos de colgantes, subsidiarias y sub-subsidiarias caen a **24,8 / 25,2 / 25,1 cm** (DE 3,7 / 2,5 / 2,3). Las puntas de las cuerdas caen a **40,1 / 41,1 / 40,8 cm**. Es decir, el objeto está construido como un «cepillo»: todas las puntas a la misma altura y todos los nudos a la misma altura. Eso hace que el quipu se lea visualmente **como una fila/matriz**, no como cuerdas de longitud libre.

---

## 4. Aritmética interna

### 4.1 Batería principal (nulo de 1000 permutaciones, seed 0, Holm)

| Test | Observado | Nulo (media) | p | p Holm | Veredicto |
|---|---:|---:|---:|---:|---|
| H1. Colgante = Σ subárbol de subsidiarias (115 casos informativos) | 21 | 9,0 | 0,005 | 0,030 | **Artefacto 1=1** (ver 4.2) |
| H2. Colgante = Σ subsidiarias directas | 21 | 7,7 | 0,002 | 0,016 | ídem |
| H3. Colgante = Σ subsidiarias excluyendo posiciones 6–7 | 18 | 8,5 | 0,032 | 0,160 | no significativo tras Holm |
| H4. Colgante = nº de subsidiarias con nudo | 23 | 14,7 | 0,256 | 0,767 | no |
| H5. Colgante = máx(subsidiarias) | 18 | 11,0 | 0,153 | 0,611 | no |
| H6. Subsidiaria s1 = Σ de sus 8 nietas (6 casos) | 0 | 0,14 | 1,000 | 1,000 | **negativo** |
| H7. PPS: colgante = Σ ventana contigua de 2–6 vecinos | 0 | 0,0 | 1,000 | 1,000 | **negativo** |
| H8. Primer colgante del grupo = Σ del resto | 2/12 | 0,13 | 0,003 | 0,021 | no resiste control (4.3) |

### 4.2 El «éxito» de H1/H2 es casi todo trivial

De los 21 matches de H1, **16 son del tipo `1 = 1`**: el colgante vale 1 y exactamente una subsidiaria vale 1 (las demás 0). Otros 2 son `2 = 1+1`, uno es `3 = 2+1` y solo **2 implican valores de dos cifras**: `p40 = 36 = 3+8+1+5+10+2+1+6` y `p221 = 16 = 8+3+1+1+1+0+1+1`. Como el 42 % de los colgantes vale 1 y el 8 % de las subsidiarias vale 1, el `1=1` aparece por azar con altísima frecuencia.

**Test restringido a casos informativos** (Σ subsidiarias ≥2 o colgante ≥2): **5/60** matches observados frente a **2,1** esperados; p = 0,098. **No se apoya la adición exacta.**

### 4.3 La suma de grupo de p190 no sobrevive

El grupo 10 tiene `p190 = 24` y la suma de los otros 14 colgantes del grupo = 24 (coincidencia exacta y no trivial). Pero al permitir que la relación se busque en **cualquier** posición del grupo (no solo la primera), se observan 2/12 grupos (el otro es el grupo 1, trivial `1 = 1+0`) frente a **2,0 esperados**; p = 1,0. El hallazgo inicial era un efecto de haber pre-especificado la primera posición. **No hay evidencia de totales de grupo.**

### 4.4 Lo que sí resiste: correlación colgante–subsidiarias

- Spearman global entre valor del colgante y suma de su subárbol (60 colgantes con suma >0): **ρ = 0,625**; nulo 0,007; p = 0,001.
- **Control dentro de grupo** (permutando el valor del colgante dentro de su grupo): ρ medio dentro de grupo = **0,43** en 6 grupos con n≥4 (0,33; 0,00; 0,45; 0,36; 0,75; 0,70); p = 0,001; nulo 0,065. Es decir, **no es un artefacto ecológico** de que los grupos grandes tengan valores grandes.
- Esto apoya que colgante y subsidiarias miden **cantidades del mismo dominio** (escalan juntas), pero **no** que el colgante sea la suma exacta de las subsidiarias.

### 4.5 Seriación y posición del máximo

- Dentro de cada módulo de 8, los valores tienden a decrecer de s1 a s8: ρ medio posición–valor = **−0,216** (40/55 módulos con ρ<0), p = 0,001 frente a permutación dentro del módulo. Efecto débil pero real: el campo 1 suele ser el mayor.
- En **8/12 grupos** el valor máximo cae en las **3 primeras posiciones** (nulo 2,75–3,11 según la variante de permutación; p = 0,002; 6/12 en las 2 primeras, nulo 2,2, p = 0,007). Sugiere que cada grupo empieza por una cifra «grande» (cabecera o total parcial), aunque no sea la suma exacta del grupo.

### 4.6 Patrones repetidos y razones

De los 90 módulos de 8, **29 patrones distintos**; 40 son todo-cero. El patrón no trivial más frecuente es `(1,0,0,0,0,0,0,0)` (11 veces), seguido de `(0,0,0,0,0,0,1,0)` (6). No hay una plantilla única; hay una **familia de plantillas dispersas**.

**Razones constantes: no.** La razón Σ colgantes / Σ subsidiarias es **1,42** en el total, pero por grupo varía entre **0,87** (grupos 7 y 10) y **2,21** (grupo 8): no hay un factor fijo entre niveles. Tampoco hay una relación fija entre el valor del colgante y el número de hijas: entre los colgantes **con** hijas, ρ de Spearman = **0,00** (el ρ global de 0,36 solo refleja que los colgantes sin hijas suelen valer 0). Los valores repetidos son los esperables en datos de conteo (94 colgantes = 1; 77 subsidiarias = 1), no una clave de repetición.

---

## 5. Interpretación propuesta

### 5.1 Qué tipo de registro parece

La estructura física es la de una **tabla**: 223 unidades (columnas) × hasta 9 cuerdas por unidad (el colgante + 8 subsidiarias), todas las puntas y todos los nudos a la misma altura, con 12 bloques sobre el cordón. Los valores son enteros pequeños (0–9 en el 93 % de las cuerdas anudadas; máximo 73), compatibles con **conteos**, no con medidas continuas. La correlación colgante–subsidiarias (ρ=0,43 dentro de grupo) indica que ambos niveles cuantifican el mismo dominio.

Hipótesis ordenadas por verosimilitud:

1. **Registro censal o de unidades domésticas (propuesto).** Cada colgante = una unidad (familia, tributario, casa); las 8 subsidiarias = 8 categorías de personas o de bienes; el valor = número de individuos/ítems. A favor: 42 % de colgantes valen 1 (unidades unipersonales), distribución de cola larga con pocos agregados grandes (73, 36, 30), 12 bloques que podrían ser ayllus/parcialidades, y el módulo 8×8 anidado (una categoría que se subdivide en las mismas 8). En contra: no hay sumas exactas, hay 83,7 % de subsidiarias vacías y no hay procedencia ni documento asociado.
2. **Inventario/registro de bienes o ganado (propuesto).** Misma lógica, pero las 8 categorías serían tipos de bien/animal y el valor cabezas o unidades. La cola larga (73) favorece esta lectura sobre un censo humano; no hay forma de discriminar ambas con estos datos.
3. **Registro tributario/almacén (especulativo).** No hay cuerdas superiores, ni valores en decenas redondas (solo 15/338 valores son múltiplos de 10), ni series de 10; un registro de depósito imperial típico tendría otra granulación. La ausencia de top cords lo hace menos probable.
4. **Calendario (descartado).** 12 grupos es tentador, pero los tamaños (3–39 colgantes) no corresponden a meses, no hay periodicidad de color ni de valores, y 223 no es 365 ni un múltiplo calendárico. **Negativo.**
5. **Registro jerárquico/clasificatorio no aritmético (especulativo).** El 8×8 anidado y las 40 plantillas todo-cero sugieren una **taxonomía** más que una contabilidad: categorías que se subdividen, con conteos escasos. Es compatible con un uso «diagramático de jerarquías» (Salomon 2013).

**Filas y columnas probables:** si es una tabla, las **columnas** son las 223 unidades (colgante + sus 8 subsidiarias) y las **filas** son los 8 campos del módulo (posiciones 1–8), leídos de izquierda a derecha sobre el cordón. Los 12 grupos serían **secciones** (ayllus, parcialidades, lotes o depósitos), no filas. La posición 6–7 (par verde sólido/rayado) **parece** un marcador de campo más que un dato: lleva nudos solo en 14/114 y 21/114 módulos y es el único par con color sistemático; aun así, esos valores existen, así que no puede descartarse que sean **campos especiales** (p. ej., dos categorías destacadas) y no meros separadores. El campo 1 es el «campo activo»: tiene más nudos (34/114) y es el único que se subdivide en 8 (6 casos).

### 5.2 Literatura

- **No hay ninguna mención a UR093/KH0329 en `docs/fichas/` ni en `docs/estado_del_arte.md`** (grep literal: 0 resultados). Tampoco hay ficha del Museo Temple Radicati. La lectura semántica no puede apoyarse en una fuente que describa este objeto.
- **Paralelo morfológico más cercano:** Milillo (2023) describe el quipu wari 1932.08.0002 (Gothenburg, «Nasca») como «loop and branched», con **un colgante y 8 subsidiarias**, la última con 8 de segundo nivel. UR093 repite el módulo 8 y el anidamiento 8×8, pero a escala de 223 colgantes y con unión lateral a media cuerda (15,5 cm), no en el extremo. Es el único paralelo publicado que encuentro; **nivel: especulativo** para inferir filiación wari.
- **Corpus:** el módulo 8 es excepcional (18/512 quipus con ≥10 colgantes tienen alguno; solo UR093, KH0568 y KH0349 tienen ≥5). Los otros quipus con módulo 8 son KH0568 (procedencia unknown), KH0349 (Nazca) y KH0362 (Nazca, con la misma unión a media cuerda, 15,0 cm). La asociación con Nazca/sur es sugerente pero n=4: **especulativo**.
- **Color y no-numericidad:** Salomon (2013) señala que los quipus preincaicos están «menos anudados y más coloreados». UR093 (72,5 % de cuerdas sin nudos, par verde sistemático, 147 códigos de color) encaja en ese perfil, lo que abre la puerta a una confección preincaica o a un uso no predominantemente numérico. **Propuesto, no bien apoyado.**
- **R/V y dirección:** FitzPatrick (2024) propone recto/verso como marcado/no marcado; Hyland y Ware (2014) proponen S/Z ↔ Hanan/Urin. En UR093 el R/V marca un **bloque de dos grupos** (p≈10⁻⁷⁰) y la dirección S/Z está cautiva del tipo de nudo (E→Z, L→S), así que **no replican** esas hipótesis a nivel de cuerda. Es un negativo útil.
- **Los seis quipus del Santa (UR087–UR092)** son censos con estructura muy distinta (61–371 cuerdas, 0,02–0,89 subsidiarias por colgante, sin módulo 8). UR093 no se parece a ellos; no hay base para asignarle esa procedencia.

### 5.3 Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| 1227 cuerdas, 223/956/48, 12 grupos, 0 cuerdas superiores, 889 en blanco | **Bien apoyado** (conteo directo, doble fuente KFG/OKR) |
| Módulo de 8 subsidiarias y 6 casos de 8×8 | **Bien apoyado** (estructura); p=0,001 frente a reparto aleatorio |
| Par de color verde sólido/rayado en posiciones 6–7 | **Bien apoyado** (103/116 y 109/116; p=0,001) |
| Bloque R en grupos 6–7 | **Bien apoyado** (179/181 vs 10/775; p≈10⁻⁷⁰) |
| Puntas y nudos alineados a ~41 y ~25 cm | **Bien apoyado** (DE 2,3–3,7 cm) |
| Colgante y subsidiarias miden el mismo dominio (correlación) | **Apoyado con datos** (ρ=0,43 dentro de grupo; p=0,001) |
| El colgante es la suma exacta de las subsidiarias | **No apoyado** (5/60; p=0,098) |
| Totales de grupo / suma de grupos | **No apoyado** (2/12 vs 2,0 esperados; p=1,0) |
| Lectura censal o de inventario | **Propuesto** |
| Filiación wari/Nazca por el módulo 8 | **Especulativo** |
| Uso calendárico | **Descartado** |

---

## 6. Anomalías y lo que no encaja

1. **18 nudos con dirección «imposible» para su tipo:** 12 E en S (valor 1), 4 L en Z, 2 S en Z. Si la dirección fuera un canal semántico, estas serían excepciones; más probablemente son errores de registro o nudos deteriorados. Lista en `25_color_nudos.py`.
2. **14 cuerdas con unión U** (5 colgantes, 8 subsidiarias, 1 sub-subsidiaria). Coinciden con cuerdas dañadas o de unión dudosa: p31 «tied with white string», p132 «broken off primary cord», p143 «not attached, very raveled», p42 con largo 0, p98 con largo 1. **5 de las 6 madres del módulo 8×8 tienen unión U** (p32s1, p70s1, p108s1, p141s1, p214s1): la unión está oculta por el ramillete de 8 cuerdas. No es información semántica, es visibilidad.
3. **Cuerdas «sueltas» y reparaciones:** p150 tiene una cuerda *suelto* de 44 cm, color AB, con un nudo E, «secured outside the sequence of pendants» (no está en `cuerdas.csv`); p132 roto y apoyado; p143 sin atar; p25, p62, p133, p174 con tramos trenzados («mend?»); p123, p164, p200 con envolturas BG («as on cord 88»). Son marcas de conservación y deben excluirse de cualquier análisis fino de color/posición.
4. **40 de los 90 módulos de 8 son todo-cero.** No es un cero numérico: son cuerdas sin nudos. Si el módulo es una plantilla de 8 campos, el 44 % de las unidades no tiene ningún dato en los campos.
5. **23 colgantes tienen 9 subsidiarias y 1 tiene 10**, no 8. La moda 8 no es universal; el exceso suele ser una subsidiaria adicional al final (posición 9), no un campo nuevo.
6. **6 módulos 8×8** aparecen en colgantes de valor 0 o 1, no en los colgantes grandes. La profundidad jerárquica no acompaña al tamaño del valor: es clasificación, no magnitud.
7. **p2 (grupo 0) vale 30 y sus 8 subsidiarias suman 34; p151 vale 73 y suman 61; p190 vale 24 y suman 47.** No hay un sesgo constante (ni el colgante siempre mayor ni siempre menor): no es un error de redondeo sistemático.
8. **147 códigos de color y 102 con `-` / 84 con `/`** (rangos y mezclas). La normalización de color es una fuente de error; los resultados de color se basan en la familia primaria y deben tomarse como aproximados (Milillo 2023 advierte que el color registrado a ojo no es comparable entre museos).
9. **El grupo 1 tiene solo 3 colgantes** (dos valen 1, uno 0) y suma 2. Es un grupo casi vacío; podría ser un separador o un grupo truncado.
10. **Procedencia desconocida y museo no verificable:** el OKR y el KFG lo atribuyen a «Museo Temple Radicati», pero la colección pasó (según nota de prensa de 2016) en custodia al MALI; la ubicación actual no está confirmada. No se puede usar el museo como origen.

---

## 7. Resultados negativos (explícitos)

- **No hay cuerdas superiores** (`union=T` = 0): no se puede testear «grupo = suma de grupos» ni «cuerda superior = suma de colgantes».
- **No hay PPS** (suma de colgantes contiguos): 0 coincidencias en 223 colgantes × ventanas de 2–6.
- **No hay suma jerárquica exacta:** 5/60 casos informativos (p=0,098); 0/6 casos de s1 = Σ nietas.
- **No hay totales de grupo:** 2/12 frente a 2,0 esperados (p=1,0).
- **No hay asociación color–valor** en colgantes (χ² p=0,27).
- **No hay codificación libre S/Z:** la dirección está determinada por el tipo de nudo (E→Z, L→S); solo 18 excepciones.
- **No hay periodicidad calendárica:** 12 grupos, pero tamaños 3–39 y ninguna periodicidad de color/valor.
- **No hay alternancia de color en la secuencia de colgantes:** el número de runs de color por grupo es ≈ n−3 (p. ej. grupo 5: 39 colgantes, 31 runs), lo que indica secuencias casi aleatorias, no bandas periódicas.
- **No hay rastro documental:** 0 menciones de UR093/KH0329 en la literatura del repo.

---

## 8. Para el coordinador

- **UR093 es el 2.º quipu más grande del OKR (1227 cuerdas) y morfológicamente único:** 223 colgantes, 956 subsidiarias, 48 sub-subsidiarias, 12 grupos, **0 cuerdas superiores**, **889 cuerdas sin nudos (72,5 %)**.
- **El rasgo que lo define es un módulo de 8 subsidiarias:** 90 colgantes tienen exactamente 8 hijas (74 % de los que tienen hijas), frente a 5,9 esperadas por azar (p=0,001). En 6 casos la primera subsidiaria se subdivide a su vez en 8 (módulo 8×8). Solo otros dos quipus del corpus (KH0568 y KH0349) tienen ≥5 módulos así.
- **El módulo tiene un par de color sistemático:** posición 6 verde sólido (103/116; base 11 %; p=0,001) y posición 7 verde «barber pole» (109/116; base 13 %; p=0,001). Son **marcadores de campo**, casi nunca llevan nudos.
- **La unión R/V no es ruido:** los grupos 6–7 son recto (179/181 subsidiarias) y el resto verso (10/775). Es un bloque contiguo de construcción/marcado (p≈10⁻⁷⁰), coherente con FitzPatrick (2024), pero probablemente físico, no semántico.
- **La aritmética exacta no aparece:** colgante = Σ subsidiarias solo en 5/60 casos informativos (p=0,098); PPS = 0; s1 = Σ nietas = 0/6; el único total de grupo (p190=24=Σ resto) desaparece al permitir cualquier posición (2/12 vs 2,0; p=1,0). El «21/115, p=0,005» inicial es un **artefacto de los 1=1**.
- **Lo que sí resiste es la correlación:** colgante y suma de subsidiarias, ρ=0,625 global y **ρ=0,43 dentro de grupo** (p=0,001), lo que indica que ambos niveles cuentan cantidades del mismo dominio, sin adición exacta. También resisten la seriación débil (ρ=−0,22) y el máximo en las 3 primeras posiciones del grupo (8/12; p=0,002).
- **Lectura más probable (propuesto):** registro **tabular de conteos por unidades** — censo/unidades domésticas o inventario de bienes/ganado—, con 223 unidades, 8 campos por unidad y 12 secciones; el campo 1 es el «campo activo» y el par verde 6–7 es un marcador. No se puede distinguir censo de inventario con estos datos.
- **Descartado:** calendario (12 grupos pero tamaños 3–39 y sin periodicidad); **depósito imperial** poco probable (sin top cords, sin decenas redondas).
- **Anomalías a documentar antes de la próxima ronda:** 18 nudos con dirección anómala, 14 uniones U (daño/visibilidad), 40/90 módulos todo-cero, 23 colgantes con 9 subsidiarias, y las reparaciones/envolturas (p25, p62, p123, p132, p143, p150, p164, p200).
- **Recomendación:** (1) buscar la ficha de conservación/foto de UR093 en el Museo Temple Radicati o el MALI para confirmar si los 8 ramilletes son físicos o una convención de registro; (2) comparar UR093 con KH0568, KH0349 y KH0362 (los otros quipus con módulo 8) para ver si comparten el par verde y la unión a media cuerda; (3) no usar UR093 como evidencia de moieties ni de dirección de nudo: aquí R/V es bloque y S/Z es tipo de nudo.

---

### Reproducibilidad

Ejecutar desde la raíz del repo:

```bash
python analisis/ds/k_UR093/20_estructura.py
python analisis/ds/k_UR093/21_perfil.py
python analisis/ds/k_UR093/22_modulo8.py
python analisis/ds/k_UR093/23_corpus.py
python analisis/ds/k_UR093/24_aritmetica_nulo.py
python analisis/ds/k_UR093/25_color_nudos.py
python analisis/ds/k_UR093/26_refinados.py
python analisis/ds/k_UR093/27_controles_estructurales.py
python analisis/ds/k_UR093/28_dentro_grupo.py
python analisis/ds/k_UR093/29_extra.py
```

Salidas auxiliares: `resultados_aritmetica.csv`, `grupos_resumen.csv`, `colgantes.csv`, `render.txt`, `ledger.txt` (estas tres últimas de la exploración previa; no se usan para las cifras finales).
