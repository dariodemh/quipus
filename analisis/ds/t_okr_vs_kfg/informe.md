# KFG vs OKR: auditoría cuerda a cuerda de los valores

**Carpeta:** `analisis/ds/t_okr_vs_kfg/` · **Fecha:** 2026-10-18 · **Semilla:** 20261018

---

## 1. Pregunta

¿Coinciden el Khipu Field Guide (KFG) y el Open Khipu Repository (OKR) en el valor de cada cuerda? ¿Dónde discrepan, cuánto, y las discrepancias se explican por el investigador (prefijos AS/UR/HP/JC), por el quipu, o por errores de metadatos? ¿Qué quipus no deberían usarse sin corrección?

---

## 2. Método

### 2.1 Datos y enlace

- **KFG:** `analisis/datos/cuerdas.csv`, 651 quipus y 57 818 cuerdas.
- **OKR:** `khipu.db`, 619 quipus en `khipu_main`; 612 con cuerdas y 54 403 cuerdas.
- **Enlace de quipus:** columna `okr` de `quipus.csv` cuando empieza por `KH`; si no, `khipu_main.INVESTIGATOR_NUM` (normalizando alias separados por `/`).
  - 595 de 651 quipus KFG quedan enlazados (91,4 %). Quedan fuera 56: 22 `QU`, 22 `MM`, 11 `AS` (AS001–AS009 y AS101 Part 1/2) y `UR1124_Detail_1`.
  - De los 595, 590 tienen cuerdas en OKR y son analizables; cubren 52 795 cuerdas OKR (97,0 % de las 54 403).
  - En los quipus enlazados, 52 178 de 52 985 cuerdas KFG encuentran pareja por nombre (98,5 %); las 807 restantes son cuerdas KFG sin nombre equivalente en OKR.

### 2.2 Reconstrucción del valor OKR

`knot_cluster.TOTAL_VALUE` **está a 0 en las 60 169 filas** de la tabla, así que no sirve. El valor se reconstruye desde `knot`:

> valor(cuerda) = Σ `knot_value_type`

`knot_value_type` ya codifica el aporte decimal de cada nudo (p. ej. 10 = nudo simple en decenas, 100 = en centenas; en nudos largos coincide con el número de vueltas). Cuando `knot_value_type = 0` y el nudo es largo (`L`/`LL`) con `NUM_TURNS > 0`, se usan las vueltas (11 nudos recuperados así). Los nudos con tipo vacío y valor 0 aportan 0.

**Verificación:** esta reconstrucción reproduce el `valor` de KFG en 98,3 % de las 52 178 cuerdas emparejadas (98,0 % si se excluyen las que no tienen nudos en KFG). Es una comprobación de consistencia, no una validación independiente: ambos podrían compartir el mismo error.

### 2.3 Correspondencia cuerda a cuerda

Se reconstruye la jerarquía OKR con `PENDANT_FROM` y se ordenan los hijos por `CORD_ORDINAL`, generando nombres `p1`, `p1s1`, `p1s1s1`… Los niveles OKR −1 y −2 se tratan como colgante (0) y subsidiaria (1). Luego se une con `cuerdas.csv` por `(kfg, cuerda)`.

Dos comprobaciones independientes del mapeo:

- **Largo:** 51 085 de 52 140 cuerdas (98,0 %) tienen el mismo largo exacto en ambas fuentes. Entre las 1 055 que difieren, 944 difieren más de 0,5 cm (no es redondeo).
- **Multiset:** en 554 de 573 quipus con ≥5 cuerdas comparables, el conjunto de valores (sin importar el orden) es idéntico. Es decir, la mayoría de los desajustes cuerda a cuerda son de **etiquetado/orden**, no de valor.

Se distingue:

- **Discrepancia de valor:** KFG tiene nudos, OKR tiene valor > 0 y **el largo coincide** (±0,5 cm). Es la comparación defendible.
- **Desalineación estructural:** KFG tiene nudos pero el largo no coincide. La cuerda con ese nombre no es la misma cuerda física, o el largo está mal registrado.

### 2.4 Unidad de análisis y controles

- La inferencia es **por quipu**; las cifras por cuerda son descriptivas.
- Nulo por quipu: binomial con la tasa global, corregido por **BH-FDR**.
- Nulo de prefijos: permutación de la etiqueta de investigador entre quipus (20 000 permutaciones), preservando el tamaño y las discrepancias de cada quipu; comparaciones por pares con **Holm**.
- Nulo del umbral «>5 %»: simulación binomial con la tasa global (5 000 réplicas).
- Nulo de nivel: hipergeométrico estratificado por quipu (20 000 réplicas).
- Se excluyen de las tasas los quipus con metadatos erróneos bien apoyados (§3.7) y las cuerdas duplicadas dentro de KFG (`UR196`, `MM007_AN002`).

---

## 3. Resultados

### 3.1 Concordancia global

Tras excluir 4 registros KFG mal enlazados y 2 quipus con cuerdas duplicadas:

| Métrica | Cifra |
|---|---|
| Cuerdas KFG con nudos | 35 884 |
| Cuerdas comparables por valor (largo coincide) | 35 212 |
| **Discrepancias de valor** | **223 (0,633 %; IC95 % 0,554–0,720)** |
| Cuerdas con nudos y largo distinto (>0,5 cm) | 672 (1,87 %) |
| KFG registra nudos y OKR da 0 | 152 |
| OKR registra nudos y KFG está vacío | 134 |

Sin exclusiones, las cifras apenas cambian: 225/35 285 = 0,638 % de discrepancias de valor y 738/36 023 = 2,05 % de desalineación estructural.

**Lectura:** el acuerdo es muy alto (99,37 % de las cuerdas comparables), pero no perfecto, y los desacuerdos no están repartidos al azar.

### 3.2 Concentración por quipu

- Solo **18 de 580 quipus comparables (3,1 %)** tienen al menos una discrepancia de valor; 562 no tienen ninguna.
- **Cinco quipus concentran 191 de las 223 discrepancias (85,7 %):**

| Quipu | Cuerdas comparables | Discrepancias | Tasa |
|---|---:|---:|---:|
| UR090 | 123 | 67 | 54,5 % |
| UR144 | 96 | 56 | 58,3 % |
| UR235 | 160 | 36 | 22,5 % |
| UR193 | 18 | 18 | 100 % |
| UR190 | 97 | 14 | 14,4 % |

- Con el nulo binomial global y BH-FDR, **8 quipus** tienen exceso significativo (q < 0,05): UR090, UR144, UR235, UR193, KH0058, UR190, HP054 y HP038.

### 3.3 Tipos de discrepancia de valor (n = 223)

| Tipo | n | % | Ejemplo |
|---|---:|---:|---|
| Factor 10 exacto en uno o más racimos (valor de posición) | 111 | 49,8 % | KFG 10 → OKR 100 (Δ = +90) |
| Mismo número de racimos, distinto valor | 96 | 43,0 % | KFG `7L` → OKR `4L` (Δ = −3) |
| KFG tiene más racimos que OKR | 11 | 4,9 % | KFG registra un nudo que OKR no tiene |
| OKR tiene más racimos que KFG | 5 | 2,2 % | OKR registra un nudo que KFG no tiene |

- Dirección: 124 casos OKR > KFG y 99 KFG > OKR. Mediana de |Δ| = 9; media = 88 (los factores 10 inflan la media).
- **UR090:** 67/67 son factor 10; mediana Δ = +90. OKR asigna 100 a un nudo simple que KFG lee como 10.
- **UR235:** 36/36 factor 10; mediana Δ = +90. Mismo patrón.
- **UR144:** 55/56 son diferencias de vueltas en nudos largos; KFG registra unas 3 vueltas más en el primer nudo largo (p. ej., `7L` donde OKR tiene `4L`; mediana de la diferencia +3, n = 56).
- **HP038:** 4 casos en que KFG registra nudos y OKR no tiene ninguna fila de nudo en esa cuerda.

El patrón dominante (factor 10) es compatible con una diferencia de **interpretación del valor de posición cuando hay un dígito intermedio ausente**: OKR conserva la posición absoluta (100) y KFG recodifica como decena (10). No es un error de transcripción de un dígito aislado; es una diferencia sistemática de decodificación entre las dos fuentes.

### 3.4 Por investigador (prefijo)

Tasas sobre cuerdas comparables por valor (largo coincide), con exclusiones:

| Prefijo | Quipus | Cuerdas comparables | Discrepancias | Tasa |
|---|---:|---:|---:|---:|
| AS | 131 | 4 769 | 0 | **0,00 %** |
| HP | 52 | 1 749 | 8 | **0,46 %** |
| JC | 23 | 828 | 0 | **0,00 %** |
| UR | 364 | 26 576 | 200 | **0,75 %** |
| KH | 10 | 1 290 | 15 | **1,16 %** |

Desalineación estructural (cuerdas con nudos y largo distinto):

| Prefijo | Cuerdas con nudos | Largo distinto | Tasa |
|---|---:|---:|---:|
| AS | 4 779 | 10 | 0,21 % |
| HP | 1 806 | 57 | 3,16 % |
| JC | 828 | 0 | 0,00 % |
| UR | 27 060 | 484 | 1,79 % |
| KH | 1 411 | 121 | 8,58 % |

**Controles:**

- Heterogeneidad entre prefijos: χ² = 48,3; **p de permutación = 0,750** (20 000 permutaciones). No hay evidencia de un efecto de investigador.
- Todos los pares quedan no significativos tras Holm; el menor es AS–HP (diferencia 0,46 %, p crudo = 0,015, **p Holm = 0,154**).
- **Sensibilidad:** al excluir los 5 quipus con más discrepancias, UR baja a 9/26 082 = **0,034 %**, por debajo de HP (0,46 %) y KH (1,16 %). Es decir, el exceso aparente de UR es un efecto de 5 quipus, no del investigador.
- A nivel de quipu (¿tiene al menos una discrepancia?): AS 0/131, JC 0/23, UR 12/364, HP 3/52, KH 5/10. La concentración sigue siendo de quipus, no de prefijos. **KH no es un código de investigador**, sino una serie de registros KFG; su tasa está dominada por KH0058 (12 de 15 discrepancias).

### 3.5 Estructura y orden de cuerdas

- 672 cuerdas con nudos (1,87 %) tienen largo distinto; la mayoría de las diferencias son grandes (413 entre 2–10 cm y 293 >10 cm), no redondeo.
- En 7 quipus (HP004, HP024, HP045, HP006, UR096, HP047, UR253) el multiset de valores es idéntico: **son las mismas cuerdas físicas con otra etiqueta/orden**. El desajuste cuerda a cuerda es del mapeo, no del valor.
- AS072 tiene 60 cuerdas en ambas fuentes y el multiset de largos es idéntico, pero el orden es completamente distinto: KFG reordena las cuerdas.
- HP009 está **incompleto en KFG**: 13 cuerdas frente a 20 en OKR; además, largos de 0–2 cm con nudos a 15–20 cm, imposibles.
- UR193, UR190 y UR003 son quipus **multi-raíz en OKR** (cordones con `PENDANT_FROM` colgante o padres ausentes). La reconstrucción jerárquica es ambigua y el alineamiento por nombre puede fallar; sus tasas altas mezclan estructura y valor.

### 3.6 Desalineación estructural por quipu

14 quipus tienen >20 % de sus cuerdas con nudos y largo distinto (excluidos los 4 KH mal enlazados): AS072 (100 %), UR193 (88 %), HP009 (86 %), UR190 (72 %), KH0058 (66 %), KH0033 y UR044 (57 %), HP024 (50 %), HP004 (44 %), HP045 (39 %), HP023 (30 %), HP006 (30 %), UR096 (25 %) y HP047 (24 %). Los cuatro KH mal enlazados (KH0197, KH0227, KH0267, KH0350) también aparecerían al 100 % si no se corrigieran.

### 3.7 Defectos específicos encontrados

#### (a) Cuatro archivos KH de KFG están desplazados en uno — **bien apoyado**

Los archivos KFG `KH0197`, `KH0227`, `KH0267` y `KH0350` no corresponden a su número KH: contienen los datos del KH siguiente. La prueba es que coinciden al 100 % en número de cuerdas, largos y valores con el KH siguiente de OKR:

| Archivo KFG | KH que realmente contiene | Cuerdas | Largos iguales | Valores iguales |
|---|---|---|---:|---:|---:|
| KH0197 | KH0198 | 149 | 100 % | 100 % |
| KH0227 | KH0228 | 221 | 100 % | 100 % |
| KH0267 | KH0268 | 22 | 100 % | 100 % |
| KH0350 | KH0351 | 55 | 100 % | 100 % |

Consecuencia: si se enlazan por la columna `okr`, estos 4 quipus aparecen con 100 % de discrepancia. Es un **falso positivo de calidad de datos**, no un problema de las lecturas. Corrección en `salidas/correcciones_kfg.csv`.

#### (b) Duplicados dentro de KFG — **bien apoyado**

- `UR196`: 16 filas extra; cada nombre `p1`…`p8` aparece dos veces con largos y valores distintos (dos fragmentos mezclados en un mismo archivo).
- `MM007_AN002`: 2 filas duplicadas.
- `KH0033` y `UR044` son el mismo quipu (66 cuerdas, mismos largos y valores), pero `KH0033` codifica los largos ausentes como 0 en vez de vacío: 37 cuerdas con largo 0 donde OKR sí tiene un largo > 0 (p. ej., 44 cm). Es una inconsistencia de codificación, no dos quipus.

#### (c) Limitaciones internas de OKR — **bien apoyado**

- `knot_cluster.TOTAL_VALUE = 0` en **60 169/60 169** filas. Cualquier análisis que use esa columna obtiene ceros.
- 212 nudos con `knot_value_type = 0`: 43 largos, 22 figura de ocho, 20 simples y 123 con tipo vacío. Solo 11 largos se pudieron recuperar con `NUM_TURNS`; **32 nudos largos quedan sin valor** (vueltas y valor ambos ausentes).
- 6 quipus con referencias `PENDANT_FROM` colgantes o múltiples raíces (AS061_MA036, KH0083, UR003, UR149, UR190, UR193): cuerdas huérfanas que dificultan reconstruir la jerarquía.

#### (d) Limitaciones internas de KFG — **bien apoyado**

- 26 cuerdas tienen cadenas de nudos sin el valor explícito tras la coma (casi todas en `UR044`): `1S(5.0,Z);1E(11.0,Z)`. No se puede verificar el valor interno de esas cadenas, aunque la columna `valor` sí está.
- Codificación inconsistente de largos ausentes: `0` en unos archivos, vacío en otros (el caso KH0033/UR044).
- 56 quipus (4 833 cuerdas) no existen en OKR; no son un error, pero limitan la cobertura al 91,4 % de los quipus.

---

## 4. Controles y resultados negativos

1. **Nulo binomial por quipu + BH:** 8 quipus significativos. La tasa global es 0,633 %; los 8 tienen tasas entre 7,4 % y 100 %. Todos siguen significativos al excluir los 4 registros mal enlazados.
2. **Permutación de prefijos:** p = 0,750. **No hay efecto de investigador.** El aparente exceso UR desaparece al quitar 5 quipus.
3. **Nulo del umbral >5 %:** 11 quipus superan el 5 % (con cualquier denominador), mientras el nulo predice 14,2 (p = 0,85). Es decir, **contar quipus >5 % no es evidencia por sí solo**: con denominadores pequeños, una sola discrepancia supera el 5 %. La lista útil es la de los 8 significativos tras BH y la de los 23 con causa identificada.
4. **Multiset:** 554/573 quipus tienen el mismo conjunto de valores. La mayoría de los desajustes cuerda a cuerda son de orden/etiqueta.
5. **Largo:** 98,0 % de largos exactamente iguales; entre los que difieren, 89 % difieren >0,5 cm. El mapeo por nombre no está inventando diferencias por redondeo.
6. **Nivel de cuerda:** las discrepancias se concentran en colgantes de primer nivel (193 de 223; 0,77 %) más que en subsidiarias de nivel 1 (0,33 %; nivel 2: 0,09 %); el exceso sobre lo esperado por azar es significativo pero pequeño (193 vs 176,5 esperados; p = 0,0001, hipergeométrico estratificado por quipu).
7. **Tamaño del quipu:** correlación entre n.º de cuerdas comparables y tasa de discrepancia = −0,03. No hay confounding por tamaño.
8. **Negativos:** AS y JC tienen **cero** discrepancias de valor (0/4 769 y 0/828). 562 de 580 quipus no tienen ninguna. No hay evidencia de que un investigador sea sistemáticamente menos fiable.

---

## 5. Nivel de evidencia

| Conclusión | Nivel |
|---|---|
| KFG y OKR coinciden en el 99,37 % de las cuerdas comparables; 0,63 % discrepa en valor | **Apoyado con datos** |
| Las discrepancias se concentran en 5 quipus (85,7 %) y en 8 quipus significativos tras BH | **Apoyado con datos** |
| Cuatro archivos KH de KFG están desplazados en uno (KH0197→KH0198, etc.) | **Bien apoyado** |
| `knot_cluster.TOTAL_VALUE` es inútil (todo 0) | **Bien apoyado** |
| El patrón dominante es una diferencia de valor de posición (factor 10), no un dígito suelto | **Apoyado con datos** |
| UR144 difiere por vueltas de nudos largos (KFG registra ~3 vueltas más) | **Apoyado con datos** |
| No hay efecto de investigador tras corregir por quipu | **Apoyado con datos** (resultado negativo) |
| KFG reordena subsidiarias respecto a `CORD_ORDINAL` de OKR | **Propuesto** (multiset idéntico; regla exacta no probada) |
| UR193/UR190/UR003 están mezclados o son multi-fragmento en OKR | **Propuesto** |
| Cuál de las dos lecturas es «correcta» en UR090/UR235/UR144 | **Especulativo** (requiere revisar imágenes/cordeles) |

---

## 6. Quipus con más del 5 % de discrepancias

Definición amplia: discrepancias (valor o largo) / cuerdas KFG con nudos. Se excluyen los 4 registros KH mal enlazados y los duplicados. **23 quipus**; se indica la causa y si el multiset de valores coincide (señal de que solo cambia el orden).

| Quipu | Pref. | C. con nudos | Disc. | Tasa | Disc. valor | Tasa valor | Multiset | Causa |
|---|---|---:|---:|---:|---:|---:|:---:|---|
| UR193 | UR | 152 | 148 | 97,4 % | 18 | 100 % | no | mixto: OKR multi-raíz |
| AS072 | AS | 10 | 9 | 90,0 % | 0 | — | — | orden (largos en otro orden) |
| HP009 | HP | 7 | 5 | 71,4 % | 0 | 0 % | — | KFG incompleto (13 vs 20 cuerdas) |
| UR144 | UR | 96 | 56 | 58,3 % | 56 | 58,3 % | no | valor: vueltas 7 vs 4 |
| UR090 | UR | 123 | 67 | 54,5 % | 67 | 54,5 % | no | valor: 100 vs 10 |
| HP024 | HP | 6 | 3 | 50,0 % | 0 | 0 % | sí | orden |
| UR190 | UR | 350 | 166 | 47,4 % | 14 | 14,4 % | no | mixto: OKR multi-raíz |
| HP004 | HP | 36 | 15 | 41,7 % | 0 | 0 % | sí | orden de subsidiarias |
| HP045 | HP | 31 | 11 | 35,5 % | 0 | 0 % | sí | orden |
| HP006 | HP | 10 | 3 | 30,0 % | 0 | 0 % | sí | orden |
| HP023 | HP | 23 | 6 | 26,1 % | 1 | 6,3 % | no | orden + 1 valor |
| UR096 | UR | 44 | 11 | 25,0 % | 0 | 0 % | sí | orden |
| HP047 | HP | 17 | 4 | 23,5 % | 0 | 0 % | sí | orden |
| KH0058 | KH | 164 | 38 | 23,2 % | 12 | 21,4 % | no | mixto; registro KH de AS047/HP035 |
| UR235 | UR | 160 | 36 | 22,5 % | 36 | 22,5 % | no | valor: 100 vs 10 |
| HP054 | HP | 18 | 3 | 16,7 % | 3 | 16,7 % | no | valor |
| UR003 | UR | 456 | 40 | 8,8 % | 3 | 0,7 % | no | estructura (multi-raíz) |
| UR044 | UR | 23 | 2 | 8,7 % | 1 | 10,0 % | no | mixto; duplicado con KH0033 |
| KH0033 | KH | 23 | 2 | 8,7 % | 1 | 10,0 % | no | mixto; largos ausentes como 0 |
| UR255 | UR | 62 | 5 | 8,1 % | 1 | 1,7 % | no | estructura |
| HP038 | HP | 54 | 4 | 7,4 % | 4 | 7,4 % | no | valor: KFG tiene nudos que OKR no |
| UR253 | UR | 61 | 4 | 6,6 % | 0 | 0 % | sí | orden |
| UR280 | UR | 134 | 8 | 6,0 % | 1 | 0,8 % | no | estructura |

Tabla completa con notas en `salidas/quipus_mas_5pct.csv`.

**Los 4 quipus que no deben usarse con el enlace actual** (error de metadatos, no de datos): KH0197, KH0227, KH0267, KH0350. Si se usan, reenlazar a KH0198, KH0228, KH0268 y KH0351 respectivamente.

---

## 7. Recomendaciones para los demás equipos

1. **No mezclar KFG y OKR a nivel de cuerda sin comprobar el largo.** Si el largo difiere >0,5 cm, probablemente la cuerda con ese nombre no es la misma; usar el multiset de valores o rehacer el alineamiento.
2. **Excluir o reenlazar** KH0197, KH0227, KH0267 y KH0350. Son falsos positivos al 100 %.
3. **No usar `knot_cluster.TOTAL_VALUE`** (todo 0). Reconstruir desde `knot`, con la salvedad de los 32 nudos largos sin valor.
4. **No tratar `valor` de KFG como equivalente absoluto de OKR:** KFG recodifica el valor de posición y puede convertir un 100 de OKR en 10 (Δ = 90). Para análisis de magnitudes, usar una sola fuente o comparar rangos/órdenes.
5. **Marcar los 8 quipus BH-significativos** como casos a revisar manualmente antes de incluirlos en análisis que dependan de valores exactos: UR090, UR144, UR235, UR193, KH0058, UR190, HP054, HP038.
6. **UR196 y MM007_AN002** tienen cuerdas duplicadas; deduplicar antes de contar cuerdas.
7. Para los quipus con solo orden alterado (HP004, HP024, HP045, HP006, UR096, HP047, UR253), el valor global del quipu no cambia; solo la asignación cuerda↔valor. No sirven para análisis que crucen valor con posición/nombre.

---

## 8. Para el coordinador

- **El acuerdo global es alto pero no perfecto:** 223 discrepancias de valor en 35 212 cuerdas comparables (0,63 %; IC95 % 0,55–0,72). Otras 672 cuerdas (1,87 %) tienen el largo mal alineado.
- **No es un problema de investigadores:** AS 0/4 769, JC 0/828, HP 8/1 749 (0,46 %), UR 200/26 576 (0,75 %), KH 15/1 290 (1,16 %); permutación de prefijos p = 0,75 y ningún par significativo tras Holm. Al quitar 5 quipus, UR cae a 0,03 %.
- **Es un problema de 5 quipus:** UR090 (67), UR144 (56), UR235 (36), UR193 (18) y UR190 (14) concentran el 85,7 % de las discrepancias de valor. 562 de 580 quipus no tienen ninguna.
- **Hallazgo duro y accionable:** cuatro archivos KH de KFG están desplazados en uno. KH0197 contiene KH0198, KH0227 contiene KH0228, KH0267 contiene KH0268 y KH0350 contiene KH0351 (100 % de coincidencia en cuerdas, largos y valores con el KH siguiente). Con el enlace actual aparecen como 100 % discrepantes: son falsos positivos.
- **Patrón dominante:** 111 de 223 discrepancias (49,8 %) son un factor 10 exacto. OKR conserva la posición absoluta (100) y KFG recodifica como decena (10). No es un dígito cambiado al azar; es una diferencia de decodificación del valor de posición.
- **Segundo patrón:** UR144 (55 casos) difiere en las vueltas de nudos largos: KFG registra ~3 vueltas más que OKR (p. ej., 7L frente a 4L). Requiere revisión de imagen para decidir cuál es correcta.
- **Ocho quipus significativos tras BH-FDR:** UR090, UR144, UR235, UR193, KH0058, UR190, HP054, HP038. Son los que hay que revisar a mano; el resto de la lista >5 % son, en su mayoría, problemas de orden/etiqueta con el mismo multiset de valores.
- **Defectos de infraestructura:** `knot_cluster.TOTAL_VALUE` está a 0 en las 60 169 filas; 212 nudos tienen `knot_value_type = 0` (32 largos sin valor recuperable); KFG tiene 26 cadenas sin valor explícito y 18 filas duplicadas (UR196, MM007).
- **Recomendación inmediata:** publicar una tabla de correspondencia corregida (4 KH reenlazados) y una lista negra/ámbar de quipus para los análisis de valores exactos. Sin eso, cualquier equipo que cruce KFG y OKR heredará estos errores.
