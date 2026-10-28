# Informe — Catálogo de rasgos no numéricos en las notas de los quipus

**Equipo:** t_notas · **Fecha:** 2026-10-18 · **Carpeta:** `analisis/ds/t_notas/`
**Scripts:** `extract.py` (taxonomía y extracción), `analyze.py` (catálogo, tests, nulos), `validate.py` (controles), `audit_precision.py` (muestra para auditoría manual).
**Salidas:** `rasgos.csv`, `rasgos_okr.csv`, `tabla_catalogo.csv`, `tabla_por_quipu.csv`, `tabla_procedencia.csv`, `tabla_coocurrencia.csv`.

---

## 1. Pregunta

¿Qué observaciones cualitativas registraron los investigadores en las cuerdas y en los cordones principales (cuerdas cortadas, reparaciones, objetos atados, nudos raros, plumas, pelo, colores especiales, cuerdas superiores), con qué frecuencia aparecen por quipu y por procedencia, y qué parte de esa señal es un rasgo del quipu y qué parte es un artefacto de cómo se documentó?

## 2. Datos

- `analisis/datos/cuerdas.csv`: 57 818 cuerdas de 651 quipus; **2 493 cuerdas (4,3 %) tienen nota** y pertenecen a **278 quipus (42,7 %)**. Son 1 539 cadenas distintas.
- `khipu.db` (OKR): 2 278 notas no vacías en 501 quipus: 420 en `khipu_main`, 319 en `primary_cord`, 1 539 en `cord.CORD_NOTES` (la columna `plainnotes` de `primary_cord` está vacía).
- `analisis/datos/quipus.csv`: `procedencia`, `region`, `museo`, `okr` (mapeo kfg → KH).

## 3. Método

1. **Taxonomía léxica explícita** (17 categorías, expresiones regulares en inglés y español sobre las notas). Cada categoría es multiclase y no excluyente: una nota puede marcar `rota` y `reparacion`. Definiciones en `extract.py`.
2. **Auditoría de precisión**: 12 notas distintas por categoría revisadas a mano (`audit_precision.py`, semilla 11). Precisión aparente: `rota` 12/12, `reparacion` 11/12 (un caso "could have been spliced"), `envoltura` 12/12, `nudo_extra` 9/12 (2 casos son ambigüedad de conteo, no nudo anómalo), `objeto` 2/3 (el resto son montajes de museo). Los falsos positivos por negación son mínimos (1/294 en `rota`, por "unbroken").
3. **Unidad de análisis = quipu** (BRIEF, regla 1). Los tests de procedencia usan presencia/ausencia por quipu; los de co-ocurrencia permutan **dentro de cada quipu**.
4. **Nulos explícitos**: 10 000 permutaciones con semilla `20261018`; p empírico `(1+#≥obs)/(B+1)`. Corrección **Benjamini-Hochberg** sobre las 14 categorías testeadas.
5. Se separan tres categorías que **no son rasgos del quipu** sino metadatos de la ficha (`fibra`, `etiqueta`, `clasif_tipo`) y se reportan aparte.

## 4. Resultados

### 4.1 Cobertura y concentración

- 2 493/57 818 cuerdas anotadas (**4,3 %**); 844 cuerdas con al menos un rasgo del catálogo (**33,9 % de las anotadas, 1,5 % del total**).
- 186/278 quipus anotados (**66,9 %**) tienen al menos un rasgo; **92 quipus anotados no tienen ninguno** (sus notas son códigos de fibra, "value 1", "Type A", remisiones a observaciones).
- 554 notas son **solo metadatos** de ficha (fibra/etiqueta/tipo), no rasgos físicos.
- La documentación está **extremadamente concentrada**: los 5 quipus más anotados reúnen el **23,7 %** de las cuerdas anotadas y los 10 primeros el **34,0 %** de las cuerdas con rasgo. Mediana: 3 cuerdas anotadas por quipu (máx. 281, QU012).
- Por colección: **QU 31,9 %** de sus cuerdas anotadas, MM 10,2 %, UR 3,4 %, AS 1,6 %, KH 0,9 %, JC 0,2 %. La densidad de notas es una propiedad de la colección/transcripción, no del quipu.

### 4.2 Catálogo de rasgos (base: 278 quipus y 2 493 cuerdas anotadas)

| rasgo | qué captura | cuerdas | quipus | % quipus anotados | % de los 651 |
|---|---|---:|---:|---:|---:|
| `rota` | rota, cortada, fragmento, deshilachada, "almost broken" | 294 | 104 | 37,4 | 16,0 |
| `cordon_principal` | observación sobre el cordón/cuerda principal | 186 | 88 | 31,7 | 13,5 |
| `reparacion` | reparación, empalme, re-atar, re-anudar, "mend" | 90 | 40 | 14,4 | 6,1 |
| `envoltura` | hilo enrollado/envuelto (marcadores, fijaciones) | 73 | 26 | 9,4 | 4,0 |
| `perdida` | ausente, perdida, desaparecida | 49 | 21 | 7,6 | 3,2 |
| `marcador` | "marker" (cuerda corta marcadora en el cordón) | 31 | 17 | 6,1 | 2,6 |
| `deterioro` | manchas, podredumbre, desgaste, insectos | 50 | 16 | 5,8 | 2,5 |
| `cuerda_superior` | "top cord" / cuerda superior | 50 | 14 | 5,0 | 2,2 |
| `sin_nudo_final` | "no end knot" | 114 | 11 | 4,0 | 1,7 |
| `nudo_extra` | nudo en el cordón principal, nudo doble/extraño, sobre la barra | 18 | 7 | 2,5 | 1,1 |
| `color_anomalo` | color incierto, desteñido, manchado, teñido | 7 | 7 | 2,5 | 1,1 |
| `desprendida` | desprendida/desatada | 12 | 6 | 2,2 | 0,9 |
| `pelo` | pelo animal/humano en la cuerda | 9 | 6 | 2,2 | 0,9 |
| `objeto` | objeto/material añadido: barra, metal, alambre, concha, calabaza | 6 | 3 | 1,1 | 0,5 |
| `pluma` | pluma | **0** | **0** | 0 | 0 |
| `fibra` (meta) | código de fibra ("Fiber: A/CL…") | 411 | 14 | 5,0 | 2,2 |
| `etiqueta` (meta) | remisión a observación/esquema/etiqueta de museo | 85 | 16 | 5,8 | 2,5 |
| `clasif_tipo` (meta) | "Type A-D", "value N", "Alt.Value" | 149 | 16 | 5,8 | 2,5 |

Rasgos raros inspeccionables uno por uno (ids completos en `tabla_por_quipu.csv`):
`objeto` = MM018, UR113, UR213; `pelo` = KH0033, MM020, QU020, UR004, UR044, UR055; `color_anomalo` = QU009, QU013, QU014, QU015, QU017, UR089, UR266; `nudo_extra` = QU009, QU014, QU016, UR001, UR004, UR006, UR213; `desprendida` = AS074, AS128, MM004, UR089, UR092, UR1176.

### 4.3 Distribución por quipu

Nº de rasgos distintos por quipu anotado: 0 → 92 quipus; 1 → 96; 2 → 45; 3 → 24; 4 → 10; 5 → 3; 6 → 3; 7 → 5. Mediana 1. La correlación entre nº de cuerdas anotadas y nº de rasgos distintos es Spearman **ρ = 0,446**: buena parte de la "riqueza" de un quipu es profundidad de documentación.

### 4.4 Frecuencias por procedencia (105 quipus con ≥5 cuerdas anotadas)

Porcentaje de quipus con el rasgo (test χ² con nulo de permutación de etiquetas de procedencia, 10 000 réplicas, BH-FDR sobre 14 rasgos):

| rasgo | Costa sur | Desconocida | Leymebamba | Otras | Pachacamac | p perm | q BH |
|---|---:|---:|---:|---:|---:|---:|---:|
| `rota` | 62 % (10/16) | 62 % (28/45) | **6 % (1/16)** | 29 % (6/21) | 43 % (3/7) | 0,0006 | **0,007** |
| `deterioro` | 0 % | 33 % (15/45) | 0 % | 5 % | 0 % | 0,0010 | **0,007** |
| `sin_nudo_final` | 0 % | 24 % (11/45) | 0 % | 0 % | 0 % | 0,0038 | **0,018** |
| `desprendida` | 19 % (3/16) | 0 % | 0 % | 0 % | 0 % | 0,0149 | 0,052 |
| `envoltura` | 6 % | 29 % (13/45) | 0 % | 10 % | 14 % | 0,0368 | 0,103 |
| `perdida` | 6 % | 22 % | 6 % | 0 % | 29 % | 0,058 | 0,135 |
| `reparacion` | 38 % | 24 % | 6 % | 19 % | 29 % | 0,31 | 0,43 |
| `color_anomalo`, `objeto`, `cuerda_superior`, `pelo`, `marcador`, `cordon_principal` | — | — | — | — | — | >0,23 | >0,41 |

Tasas por 100 cuerdas anotadas (independientes del tamaño del quipu): `rota` 18,3 Costa sur / 12,7 Desconocida / **1,3 Leymebamba** / 13,1 Pachacamac; `reparacion` 11,3 / 2,3 / 0,9 / 9,1; `sin_nudo_final` 0 / 8,0 / 0 / 0; `deterioro` 0 / 3,4 / 0 / 0.

### 4.5 El confundido obvio: la colección, no la procedencia

Los rasgos que "dependen de la procedencia" son en realidad **convenciones de una colección**:

| rasgo | AS | MM | QU | UR | otros |
|---|---:|---:|---:|---:|---:|
| `rota` | 38 | 26 | 116 | 113 | 4 |
| `deterioro` | 0 | 4 | **44** | 2 | 0 |
| `sin_nudo_final` | 0 | 0 | **114** | 0 | 0 |
| `reparacion` | 16 | 8 | 3 | 63 | 0 |
| `perdida` | 4 | 0 | 8 | 37 | 0 |
| `cuerda_superior` | 15 | 4 | 28 | 3 | 0 |
| `cordon_principal` | 32 | 15 | 17 | 121 | 1 |

`sin_nudo_final` aparece **114/114 veces en quipus QU** (11 quipus) y `deterioro` en 44/50 notas QU: son estilos de anotación de esa colección, no distribución geográfica. Tasa de `rota` por prefijo: AS 27,1 %, MM 17,4 %, QU 13,9 %, UR 8,5 %. Cualquier conclusión "por procedencia" que no se controle por colección/transcriptor es insegura.

### 4.6 Control dentro de una sola colección: conservación, no cultura

Restringiendo a la colección **UR** (1 328 cuerdas anotadas en 82 quipus; mismo equipo de transcripción, mismas planillas), la diferencia de `rota` sobrevive:

- Por cuerdas: Costa sur **39/252 (15,5 %)** vs Leymebamba **4/318 (1,3 %)**, Fisher p = 4,6 × 10⁻¹¹.
- Por quipu: 14/30 vs 2/20, Fisher p = 0,012.
- `reparacion`: 18/252 (7,1 %) vs 3/318 (0,9 %).

La explicación aburrida —y suficiente— es **conservación**: los quipus de Leymebamba provienen de la chullpa seca de Laguna de los Cóndores (1996), nunca estuvieron en exhibición; los de la costa sur pasaron por museos, vitrinas y manipulación. La nota registra **historia de conservación**, no significado.

### 4.7 Co-ocurrencia dentro del quipu (permutación intra-quipu, B = 10 000)

Solo quipus con ≥3 cuerdas anotadas; se permuta el rasgo A dentro de cada quipu conservando el nº de cuerdas anotadas y el nº de casos de A.

| par | observado | media nula | p |
|---|---:|---:|---:|
| `rota` & `reparacion` | 19 | 22,7 | 0,938 (sin enriquecimiento) |
| `rota` & `perdida` | 1 | 4,0 | 0,994 (depleción) |
| `rota` & `desprendida` | 3 | 4,6 | 0,934 |
| `rota` & `deterioro` | 9 | 9,2 | 0,618 |
| **`reparacion` & `desprendida`** | **8** | **4,5** | **0,008** |

Lectura: las reparaciones se asocian a cuerdas **desprendidas del cordón principal**, no a cuerdas rotas a media altura. Es un control positivo de que la extracción recupera relaciones físicas reales; y un resultado negativo contra la intuición de que "reparación" marca principalmente roturas de fibra. Nótese que a nivel de quipu `reparacion` y `rota` sí co-aparecen (ambas se concentran en los mismos quipus muy anotados); el test intra-quipu demuestra que eso es clustering documental, no asociación física.

### 4.8 ¿Las notas marcan datos ausentes? (nulo: permutar anotación dentro del quipu)

| variable | P(x \| cuerda anotada) | P(x \| no anotada) | dif | p |
|---|---:|---:|---:|---:|
| `nudos` vacío | 0,302 | 0,306 | −0,003 | 0,0005 (significativo pero nulo en magnitud) |
| `union = U` | 0,323 | 0,411 | −0,088 | 0,0005 |
| `nivel > 0` (subsidiaria) | 0,227 | 0,281 | −0,054 | 0,999 (depleción) |

Las notas **no** se limitan a marcar cuerdas sin datos: se anotan algo más las cuerdas de nivel 0 y con unión conocida. Es decir, el sesgo documental va hacia las cuerdas "legibles", no hacia las problemáticas. Esto refuerza que el catálogo describe rasgos observados y no un cajón de datos faltantes.

### 4.9 Validación cruzada: KFG y OKR no son fuentes independientes

Mapeando `kfg → okr (KH)`, hay **237 quipus** con notas de cuerda en ambas fuentes. De 1 572 pares (quipu, nota) de KFG, **1 004 aparecen literalmente en OKR**; la concordancia por quipu es κ = 1,000 para `rota`, `deterioro`, `perdida`, `envoltura`, `objeto`, `cuerda_superior`, `cordon_principal`; κ = 0,983 para `reparacion` y 0,965 para `marcador`. **KFG es una copia curada de OKR**: coincidencias perfectas no son validación independiente, solo consistencia de transcripción.

### 4.10 Casos concretos

- **`sin_nudo_final`** (114 cuerdas, 11 quipus, todos QU): 112/114 tienen `terminacion = U` (el campo estructurado). Es una verbalización de un código, no un rasgo nuevo; dentro de las cuerdas con terminación U solo el 12,8 % lleva la nota.
- **Cuerdas superiores**: 154 cuerdas con `union = T` en **26 quipus** (18 de procedencia desconocida). Solo **14 quipus** tienen nota "top cord"; de 12 quipus con T y con notas, la nota aparece en **7 (58 %)**; 7 quipus tienen nota de cuerda superior sin ninguna T registrada. La nota añade información de construcción ("looped through Grp. 9", "Sum of Grp 9 Ps equal TOP CORD value"), pero es **incompleta**: no sirve como detector.
- **Objetos**: en KFG solo 3 quipus (barra, pin de metal de exhibición, alambre de reparación). En OKR hay 21 quipus, pero 15 de las 40 notas (8 quipus) son "wooden bar" (montaje de museo), 9 notas (8 quipus) mencionan tassels y 11 (9 quipus) "needlework bundles". **Ninguna pluma** en ninguna de las dos fuentes; ningún objeto atado (concha, calabaza, cuenta) descrito sobre el quipu: la única mención de conchas y calabazas (AS036/AS037) es el ajuar de la tumba, no un aditamento del quipu.
- **Pelo**: 6 quipus (9 cuerdas). Ejemplos: "strand of animal hair interlaced at top of pendant", "single black hair running down cord (tied within knot)", "sheep hair". Es el único rasgo "etnográfico" con presencia repetida, y está **dentro de nudos**, lo que sugiere contenido/relleno más que adorno.
- **Color**: 98 notas mencionan "color", pero casi todas repiten el código Ascher ("Color: W", "color KB"); solo 7 quipus (11 notas) registran anomalías (desteñido, manchado, incierto). La columna `color` ya estructura esa información: las notas **no aportan** una dimensión de color nueva.

## 5. Controles

1. **Nulo de procedencia**: permutación de la etiqueta de procedencia entre quipus (conserva tasas globales y tamaños); 10 000 réplicas; BH-FDR. Solo `rota`, `deterioro` y `sin_nudo_final` sobreviven (q ≤ 0,018).
2. **Nulo intra-quipu** para co-ocurrencia y para el sesgo de anotación: conserva el nº de cuerdas anotadas y de casos por quipu; elimina el efecto de los quipus gigantes (QU012, QU013).
3. **Control de colección**: repetición del efecto `rota` solo con UR (misma planilla, mismos transcriptores): sobrevive (p = 4,6 × 10⁻¹¹ por cuerda; p = 0,012 por quipu).
4. **Auditoría de precisión** manual (12 notas/categoría) y prueba de negaciones ("unbroken": 1 falso positivo).
5. **Doble fuente** KFG/OKR: consistencia, no independencia (κ ≈ 1).
6. **Chequeo contra campos estructurados**: `terminacion`, `union`, `nudos`, `nivel`: las notas no duplican mecánicamente los campos, salvo `sin_nudo_final`.

## 6. Resultados negativos

- **No hay plumas** (0 notas) y **no hay objetos rituales atados** en las notas de cuerda del KFG: 0 tassels, 0 conchas, 0 cuentas, 0 calabazas. El catálogo no sostiene la imagen de quipus como paquetes rituales con aditamentos; al menos no en esta base.
- `color_anomalo` es marginal (7 quipus) y no se asocia a procedencia (q = 0,41). La información de color está en la columna `color`, no en las notas.
- `reparacion` no se asocia a `rota` dentro del quipu (p = 0,94): el vínculo intuitivo no existe a nivel de cuerda.
- `perdida` está **depletada** en cuerdas rotas (1 vs 4 esperadas, p = 0,99): se anota "perdida" en cuerdas que no están rotas, probablemente cuerdas que faltan del ejemplar.
- No hay diferencia por procedencia en `cordon_principal`, `marcador`, `cuerda_superior`, `pelo`, `objeto`, `color_anomalo` (todos q > 0,4).
- La nota "cuerda superior" detecta solo el 58 % de los quipus con `union = T` y produce 7 quipus con nota sin T: **no es un detector fiable**.
- 92 de 278 quipus anotados no tienen ningún rasgo del catálogo: la mayoría de las notas son metadatos de ficha.

## 7. Nivel de evidencia

| afirmación | nivel |
|---|---|
| El catálogo y sus frecuencias (294 cuerdas rotas en 104 quipus; 90 reparaciones en 40; 50 cuerdas superiores en 14; etc.) | **bien apoyado** (para esta base) |
| La documentación está concentrada en pocas colecciones y quipus (QU 31,9 % vs JC 0,2 % de cuerdas anotadas; top-10 = 34 % de los rasgos) | **bien apoyado** |
| KFG y OKR son la misma transcripción, no fuentes independientes (κ ≈ 1; 1 004/1 572 cadenas idénticas) | **bien apoyado** |
| `sin_nudo_final` es una convención de la colección QU (114/114) ligada a `terminacion = U` (112/114) | **bien apoyado** |
| Los quipus de Leymebamba registran menos roturas que los de la costa sur (1,3 % vs 15,5 % de cuerdas), consistente con mejor conservación | **apoyado con datos** (control dentro de UR; confundido con historia de museo, no con cultura) |
| Las reparaciones se asocian a cuerdas desprendidas y no a roturas (8 vs 4,5; p = 0,008) | **apoyado con datos** (n pequeño, test exploratorio) |
| Cualquier diferencia de rasgos "por procedencia" más allá de `rota`/conservación | **propuesto / no sostenido**: confundido con colección y transcriptor |
| Que el pelo dentro de nudos indique contenido ritual | **especulativo** (6 quipus, sin contexto) |
| Que la escasez de plumas/objetos refleje la ausencia real de aditamentos en los quipus | **especulativo**: puede ser un límite de la digitalización (las notas de cordón principal del OKR sí mencionan 8 tassels y 9 "needlework bundles") |

## 8. Limitaciones

- Taxonomía de bolsa de palabras: no resuelve negación, ironía ni referencias anafóricas ("the rest", "as on cord 88"); la auditoría da ≥90 % en las categorías principales, pero `nudo_extra` y `objeto` son las más frágiles.
- 4,3 % de cuerdas anotadas y 42,7 % de quipus: el denominador real es la documentación, no el corpus. Las tasas por 100 cuerdas anotadas corrigen parcialmente, pero no eliminan el sesgo de qué se decidió anotar.
- El mapeo kfg → KH deja fuera 41 quipus anotados (QU, MM, HP, JC) que no están en OKR; la comparación entre fuentes se limita a 237.
- No se prueba significado: se caracteriza el registro cualitativo. Los rasgos con potential semántico (`nudo_extra` en el cordón principal, `marcador`, cuerdas superiores) quedan identificados pero no interpretados.

## 9. Para el coordinador

- **El filón es pequeño pero limpio**: 2 493 de 57 818 cuerdas (4,3 %) tienen nota; 278 de 651 quipus. Cualquier uso de `notas` como variable debe declarar ese denominador.
- **Catálogo listo para usar**: 14 rasgos no numéricos con frecuencias por quipu y procedencia en `tabla_catalogo.csv` / `tabla_por_quipu.csv`. Los grandes: rotas (104 quipus), observaciones de cordón principal (88), reparaciones (40), envolturas/marcadores (26/17), cuerdas superiores (14).
- **La señal "por procedencia" es casi toda estilo de colección**: `sin_nudo_final` es 114/114 QU; `deterioro` 44/50 QU. Sin controlar por prefijo/transcriptor, cualquier correlación con procedencia es espuria.
- **Único efecto geográfico que sobrevive al control**: los quipus UR de Leymebamba tienen 1,3 % de cuerdas rotas frente a 15,5 % en la costa sur (p = 4,6 × 10⁻¹¹), y el patrón se repite por quipu (p = 0,012). Es **conservación**, no cultura: útil para ponderar qué quipus están completos.
- **Control positivo del método**: reparación co-ocurre con cuerdas desprendidas (8 vs 4,5 esperadas; p = 0,008) y **no** con roturas (p = 0,94). Las notas capturan relaciones físicas reales.
- **KFG = OKR**: κ ≈ 1,0 y 1 004/1 572 cadenas idénticas. No gastar esfuerzo en "validar" una fuente con la otra; sirven para completar cobertura (OKR añade 8 quipus y notas de cordón principal ausentes en KFG).
- **Negativo importante**: no hay plumas (0), ni cuentas, ni conchas; solo 6 quipus con pelo y 3 con objetos en KFG. La hipótesis de "quipus con aditamentos rituales" no se puede sostener con esta base (aunque OKR menciona 8 tassels y 9 needlework bundles en notas de cordón principal: vale la pena revisarlos a mano).
- **Candidatos con potencial semántico para la siguiente ronda**: (a) los 4 quipus con un nudo explícito en el cordón principal (`UR001`, `UR004`, `UR006`, `UR213`; el catálogo `nudo_extra` suma 7 con los casos de ambigüedad de conteo QU009/QU014/QU016), que podrían marcar grupos o sumas; (b) los 17 quipus con `marcador`; (c) los 26 con `union = T`, donde la nota dice explícitamente "Sum of Grp 9 Ps equal TOP CORD value".
- **Recomendación**: usar `rota` como covariable de conservación en los análisis de valores (las cuerdas rotas pueden tener valores truncados), y **no** usar `notas` como proxy de procedencia ni de ritualidad.
