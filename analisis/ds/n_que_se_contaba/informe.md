# ¿Qué se contaba? Demografía, unidades decimales, capacidad de depósito y dígitos

**Equipo:** DeepSeek (carpeta `analisis/ds/n_que_se_contaba/`)
**Fecha:** 18 de octubre de 2026
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `analisis/13_sistema_incahuasi/ur278_tabla.csv`, `analisis/10_tablas/` (177 tablas reconstruidas), `analisis/11_rosetta/fA_redondeo_por_quipu.csv`, literatura en `analisis/fuentes_txt/` y `docs/fichas/`.
**Semilla:** 20261017. Todo el código está en esta carpeta (`comun.py`, `01_demografia.py`, `02_unidades.py`, `03_depositos.py`, `04_digitos.py`).

## Pregunta

El proyecto ya sabe **cómo** funcionaba la contabilidad inca: cuerdas superiores = sumas de grupos, tríos `[x, c, x−c]` con cuota fija, parejas A/B que se consolidan, una jerarquía de quipus en Incahuasi. No sabe **qué** se contaba: ni la identidad de las columnas, ni la de las partes A/B, ni la unidad (personas, costales, granos, cargas), ni el producto.

Esta ronda ataca esa pregunta con cuatro disciplinas que el proyecto no había usado de forma sistemática: demografía (¿son grados de edad?), metrología decimal inca (¿son unidades de 10/100/500/1000/10 000?), arqueología de depósitos (¿qué magnitudes físicas caben en las colcas de Inkawasi?) y análisis de dígitos (Benford y dígito final: ¿recuento natural o asignación administrativa?). El objetivo no es adivinar sino **descartar**: cada hipótesis recibe veredicto con cifras.

## Método general

1. **Unidad de análisis = quipu.** Los contrastes de demografía y dígitos se hacen por quipu; las pruebas a nivel de cuerda se agregan por quipu o usan permutaciones dentro de quipu. En las tablas la fila es el grupo de colgantes y la columna la posición dentro del grupo (misma reconstrucción que `10_tablas/comun.py`).
2. **Nulo explícito en cada prueba**, con p empírico unilateral `(k+1)/(B+1)` y semilla fija.
3. **Corrección múltiple BH-FDR** cuando se prueban muchos quipus o muchas hipótesis; se indica el número de pruebas.
4. **Valores 0 sin nudos = ausentes** (NaN), nunca ceros.
5. Cada conclusión se etiqueta: **demostrado / apoyado con datos / propuesto / especulativo**.

---

## 1. Demografía: ¿eran las columnas categorías de edad y sexo?

### 1.1 Qué predice el modelo

Los censos incas usaban del orden de 10–12 grados de edad (Guaman Poma; visitas coloniales). Si las K columnas de una tabla fueran esos grados, el perfil de medias por columna debería tener la forma de una población preindustrial de alta mortalidad. Modelé una población estable con mortalidad Siler calibrada a **e0 ≈ 28 años** (esperanza de vida al nacer típica de sociedades preindustriales; tabla de vida estable, crecimiento r = 0). Probé dos esquemas de bandas:

| esquema | bandas | perfil esperado (%) | CV entre columnas | max/min |
|---|---|---|---|---|
| S1 (5 años + abierta) | 0-4, 5-9, …, 35-39, 40+ | 27,7 · 8,6 · 7,5 · 6,7 · 5,9 · 5,2 · 4,7 · 4,2 · 29,6 | **0,90** | **7,1** |
| S3 (tipo Guaman Poma) | 0-2, 2-5, 5-10, 10-15, 15-20, 20-40, 40-60, 60-70, 70+ | 20,0 · 7,7 · 8,6 · 7,5 · 6,7 · 19,9 · 13,2 · 5,5 · 10,8 | **0,50** | **3,6** |

El esquema más **generoso** (S3, anchos desiguales que imitan los grados sociales andinos) exige ya un CV de 0,50 y un cociente max/min de 3,6. Cualquier censo real es mucho más desigual que eso: el grupo más numeroso (niños o adultos jóvenes) tiene varias veces el tamaño del más pequeño (ancianos).

### 1.2 UR278: el caso mejor documentado

UR278 son 33 registros sucesivos del flujo 47 en 9 columnas de tamaño relativo estable (la tabla conservada tiene 28 filas completas o casi). Perfil observado (media de las proporciones por fila):

```
c1 13,5 %  c2 14,0 %  c3 9,6 %  c4 10,7 %  c5 11,6 %
c6 13,2 %  c7 11,1 %  c8 8,3 %  c9 9,0 %
CV = 0,184  IC95 bootstrap [0,152; 0,230]
max/min = 1,70  IC95 [1,51; 2,04]
```

- **CV observado 0,184 vs 0,50–0,90 del modelo.** El perfil es 2,7–4,9 veces más plano de lo que cualquier pirámide de edad permite.
- **max/min 1,70 vs 3,6–7,1.** El 95 % de las filas tiene un cociente max/min dentro de fila de 1,24–6,35 (mediana 2,56); solo **4 de 28** filas alcanzan el mínimo que exige el modelo más generoso (3,6). En un censo, la mayoría de las filas-unidad debería acercarse a ese perfil.
- **Nulo demográfico (bootstrap Dirichlet-multinomial con la dispersión observada, B = 4000):** bajo H0 “las columnas son bandas de edad”, el CV esperado es 0,90 [0,87; 0,94] para S1 y 0,50 [0,47; 0,53] para S3. La probabilidad de observar un CV tan plano o más plano es **p < 0,00025** en ambos casos (0/4000). La distancia de Aitchison al modelo también es máxima: D = 1,63 (S1) y 0,83 (S3) frente a 0,14 y 0,13 esperados bajo H0; **p < 0,00025**.
- **Control de estructura (las columnas no son intercambiables):** Friedman con 26 filas completas, χ² = 90,6, **p = 3,5·10⁻¹⁶**; permutando celdas dentro de fila el CV cae a 0,059 [0,032; 0,088] (p < 0,00025). Es decir: **hay estructura de columnas real, pero es una estructura plana**, incompatible con edades.
- **Control de dispersión (Dirichlet por momentos, columnas con las medias observadas):** CV esperado 0,195; p = 0,72. La dispersión observada es exactamente la que produce un reparto administrativo con esas medias; no hay nada “demográfico” que explicar.

**Firma de sexos.** Si las 9 columnas fueran pares varón/mujer por grado de edad, los pares deberían estar cerca de 1:1. El mejor emparejamiento (minimizando Σ|log(a/b)|) empareja (c1,c2), (c3,c9), (c4,c5), (c6,c7) y deja fuera c8; el coste (24,0) es menor que el de columnas independientes (49,3; p < 0,001), pero la **razón max/min dentro de cada par tiene mediana 1,12 y cola hasta 2,23**: covarían porque comparten el tamaño del registro, no porque sean mitades sexuales de una misma clase. Al dividir cada fila por su media (quitar el tamaño del registro), las correlaciones de los pares caen a 0,36 (c1–c2), 0,18 (c4–c5), −0,02 (c6–c7) y −0,04 (c3–c9). Un par varón/mujer real estaría en 1,00–1,05 y mantendría la correlación. **No hay firma de sexos.**

**Qué más descarta la planitud.** El mismo cálculo no es específico de la edad: cualquier hipótesis en la que las 9 columnas tengan tasas base muy desiguales queda descartada por el CV de 0,18 y el max/min de 1,70. Eso incluye **9 productos** (maíz, papa y ají no tienen la misma importancia), **9 meses o estaciones** (la cosecha andina es fuertemente estacional) y **9 zonas ecológicas** (la costa, la puna y la selva no producen lo mismo). Lo que sí es compatible con la planitud es un **reparto administrativo diseñado para partes casi iguales**: 9 ayllus, 9 parcialidades, 9 cuadrillas, 9 depósitos o 9 columnas de un mismo flujo. Esa es la lectura positiva que queda: **las columnas son una partición, no una taxonomía natural** [apoyado con datos para la planitud; propuesto para “partición administrativa”].

**Veredicto UR278: demografía DESCARTADA.** No es “indecidible”: el perfil es demasiado plano por un factor 2,7–4,9 y la probabilidad bajo el modelo de edad es < 2,5·10⁻⁴. Lo que sí queda **apoyado con datos** es que las 9 columnas son **subunidades administrativas de tamaño deliberadamente parecido** (probablemente un reparto en 9 partes, no una estructura de población).

### 1.3 Cribado de las 177 tablas

Reconstruí las 177 tablas de `10_tablas` (fila = grupo modal, columna = posición) y apliqué el mismo contraste con K bandas (K = número de columnas; se excluyen K > 12, que no puede ser un censo de 10–12 grados → 171 tablas, 159 con perfil válido).

| resultado | cifra |
|---|---|
| CV observado (mediana) | 0,68 (p5–p95: 0,14–1,32) |
| CV del modelo con la misma K (mediana) | 0,91 |
| razón CVobs/CVmodelo (mediana) | 0,73 (p5–p95: 0,15–1,45) |
| tablas con razón ≥ 0,6 (forma piramidal *posible*) | **96/159 (60 %)** |
| tablas con razón ≥ 0,8 | 74/159 |
| tablas que **no rechazan** el modelo por dispersión (q BH ≥ 0,05) | 63/159 (40 %) |
| tablas que no rechazan por **forma** (distancia de Aitchison, q ≥ 0,05) | 56/159 (35 %) |
| tablas que pasan **ambos** filtros (dispersión y forma) | **23/159 (14 %)** |
| tablas que rechazan el modelo en al menos un filtro | 136/159 (86 %) |

Lectura: **el 86 % de las tablas queda descartado demográficamente**. El 14 % restante (23 tablas) no se distingue de un censo, pero tampoco de un perfil categórico cualquiera: el modelo de edad, con K! asignaciones posibles y K bandas, es lo bastante flexible para ajustar formas variadas. Control de esas 23: **ninguna tiene perfil monótono decreciente** y solo 5 tienen el máximo en la primera columna; sus perfiles son variados (p. ej. AS005 [23, 17, 64, 8], HP010 [45, 4, 7, 4, 7, 7, 11, 15, 5]), lo que confirma que pasan por la libertad de permutación, no por una forma piramidal reconocible. Además, la tabla emblemática (UR278) cae del lado rechazado. **Veredicto global: la demografía no explica el corpus; como máximo es compatible con una minoría de tablas, y no hay ninguna tabla en la que la forma piramidal sea la explicación preferida frente a “lista ordenada”.**

Negativo que conviene retener: la mayoría de las tablas **no** son censos. Eso reduce el espacio: las columnas no son, en general, edades ni sexos.

---

## 2. Unidades decimales incas: ¿se “llenaban” chunka, pachaka, pichqa-pachaka, waranqa, hunu?

### 2.1 Qué se probó

La administración inca contaba en unidades de 10, 100, 500, 1000 y 10 000 (chunka, pachaka, pichqa-pachaka, waranqa, hunu). Si los quipus se llevaran “llenando” esas unidades, los totales deberían acumularse en ventanas alrededor de 10, 50, 100, 500, 1000, 5000 y 10 000 (p. ej. 90–110, 450–550, 900–1100), no solo ser múltiplos exactos.

- **Totales de grupo** (suma de cuerdas de nivel 0 del grupo; n = 6 459 con total > 0) y **totales de quipu** (suma de nivel 0; n = 637).
- **Estadístico:** número de totales en cada ventana ±10 % alrededor de la unidad, comparado con lo esperado integrando una **KDE gaussiana de log10(total)** (ancho 0,05 décadas; sensibilidad 0,03 y 0,08). Es el nulo que pide el encargo: la propia distribución de totales, suavizada.
- **Nulo estructural adicional:** barajar los valores de las cuerdas entre grupos del mismo quipu (conserva tamaño de grupo, total del quipu y distribución de valores), 1000 réplicas.
- **BH-FDR** sobre las 14 pruebas (7 unidades × 2 conjuntos).
- No se evalúa la ventana de 10: los totales < 30 se excluyen porque la KDE logarítmica no es fiable en el extremo discreto (mediana de los totales de grupo = 50). El test relevante para el sistema decimal son 100, 500, 1000 y 10 000.

### 2.2 Resultados

| unidad | grupos: obs/esp (ratio) | quipus: obs/esp (ratio) | q BH |
|---|---|---|---|
| 50 | 197 / 193,4 (1,02) | 8 / 9,3 (0,86) | 0,95 |
| 100 | 188 / 177,9 (1,06) | 11 / 13,5 (0,82) | 0,95 |
| 500 | 142 / 137,1 (1,04) | 18 / 21,9 (0,82) | 0,95 |
| 1000 | 99 / 90,5 (1,09) | 17 / 20,0 (0,85) | 0,95 |
| 5000 | 61 / 54,5 (1,12) | 12 / 13,5 (0,89) | 0,95 |
| 10000 | 11 / 14,8 (0,75) | 14 / 11,9 (1,18) | 1,00 |

- **Cero excesos significativos** tras BH (0/12 pruebas evaluables con q < 0,05 y ratio > 1; la ventana de 10 no es evaluable). Las ratios van de 0,75 a 1,18; ninguna se aparta de lo que predice la distribución suavizada.
- **Nulo estructural:** las fracciones observadas coinciden con el nulo en todas las unidades (p = 0,22–0,74); solo 5000 da p = 0,028 sin corregir (q ≈ 0,19, no significativo) y 10000 va en dirección contraria (p = 0,995). Es decir: **no hay “llenado” de unidades**.
- **La cola alta no está en las potencias de 10.** El histograma de la mantisa (log10 total mod 1) tiene su máximo en 0,5–0,7 (grupos: 495 y 561 de 3 870 en los bins 0,5–0,6 y 0,6–0,7) y su mínimo en 0,9–1,0 (297; 7,7 % frente al 10,1 % del bin 0,0–0,1). Es el patrón de una convolución de 2–5 cuerdas de tamaño medio, no el de “redondear hacia arriba” al siguiente pachaka.
- **Los totales de quipu no tienen escala preferida:** KS de log10(total) mod 1 contra U(0,1), D = 0,039, **p = 0,31** (n = 596). En grupos el KS rechaza (D = 0,082, p = 4·10⁻²³), pero por la forma global de la distribución, no por picos en las unidades (los ratios de la tabla lo muestran).

### 2.3 El único efecto decimal real (y su control)

Sí hay **redondeo exacto**: 15,7 % de los totales de grupo son múltiplos de 10 (esperado continuo 10 %), 2,0 % múltiplos de 100 (esperado 1 %), 0,3 % múltiplos de 1000 (esperado 0,1 %); el residuo 0 de `total mod 100` aparece 129 veces frente a 26,2 esperadas (χ² p = 1,2·10⁻⁸³). Pero esto **no es independiente de las cuerdas**: el 29 % de las cuerdas intactas ya son múltiplos de 10 (11_rosetta).

Control: se conservó la parte de las decenas de cada cuerda y se barajaron los dígitos de unidades entre cuerdas. El nulo da 12,6 % de totales múltiplos de 10 [11,8; 13,4]; el observado es 15,7 %, **3,1 puntos por encima** (p < 0,002). Queda un pequeño redondeo *del total a las decenas*, pero no a las centenas ni a las unidades administrativas: no hay preferencia por 100, 500, 1000 o 10 000 frente a 200, 300, 700, etc.

**Veredicto: “llenado de unidades decimales incas” DESCARTADO.** Los totales son suaves alrededor de las unidades canónicas (0/12 pruebas evaluables). Lo que existe es (a) una herencia de cuerdas redondeadas a decenas y (b) un pequeño redondeo adicional del total a las decenas, no a las unidades de 100/500/1000/10 000.

---

## 3. Arqueología de depósitos: ¿qué magnitudes físicas admiten las cifras?

### 3.1 Anclas arqueológicas

Urton (2017, cap. 9) y Urton y Chu (2015), sobre Qolqawasi (Inkawasi, valle de Cañete):

- **6 estructuras al norte:** 4 kallankas (U.A. 01, 02, 04, 05) y 2 “espacios de clasificación” sin techo (U.A. 07, 08).
- **36 cámaras grandes** de almacenamiento en el centro y **209 colcas pequeñas** cuadradas alrededor (oeste, sur, este).
- **~6 400 m³** de capacidad total estimada cuando estaba en uso.
- **34 quipus** recuperados; 14 bajo maní en la kallanka U.A. 05 (UR266, 268, 269, 270, 272, 273A/B, 274A/B, 275, 276–279), UR267A/B bajo ají en U.A. 07, UR271 bajo frijol negro, UR255/256 en el corredor.
- **Cuadrículas de 23 × 23 cm** en el piso de U.A. 07, en paneles de 3 × 39 (~30 paneles ≈ 3 510 cuadros), interpretadas como unidades estándar de clasificación.

Magnitudes registradas: cabeceras del flujo 47 (UR266/UR269/UR275) con mediana **2 000**, p5–p95 **482–3 317**, máximo **4 273**; 43 valores > 1 000 en las dos copias UR266/UR275. UR278 conserva 28 filas × 9 columnas = **61 790 unidades** (media por celda 248). Cuota fija **47** por registro.

### 3.2 Cálculo

Capacidad media por unidad de almacenamiento: 6 400 / 245 = **26,1 m³**. Densidad aparente central 0,6 t/m³ (rango 0,3–0,8; maíz 0,7, papa 0,65, maní con cáscara 0,3, ají seco 0,4). Masa almacenable ≈ **3 840 t**.

| unidad | masa/unidad | cabecera 2 000 | UR278 (61 790) | % de 6 400 m³ | colcas equivalentes |
|---|---|---|---|---|---|
| grano de maíz | 0,3 g | 0,001 t | 0,02 t | 0,0005 % | 0,001 |
| ají seco | 5 g | 0,01 t | 0,31 t | 0,008 % | 0,02 |
| papa | 100 g | 0,2 t | 6,2 t | 0,16 % | 0,4 |
| mazorca de maíz | 250 g | 0,5 t | 15,4 t | 0,40 % | 1,0 |
| **kilogramo** | 1 kg | 2 t | 61,8 t | **1,6 %** | 3,9 |
| arroba | 11,5 kg | 23 t | 711 t | 18,5 % | 45 |
| **carga de llama** | 30 kg | 60 t | 1 854 t | **48,3 %** | 118 |
| **costal 25 kg** | 25 kg | 50 t | 1 545 t | **40,2 %** | 99 |
| costal 50 kg | 50 kg | 100 t | 3 090 t | 80,5 % | 197 |
| fanega de maíz | 45 kg | 90 t | 2 781 t | 72,4 % | 177 |

Sensibilidad a la densidad (UR278): mazorca 0,3–0,8 % de la capacidad; kilogramo 1,2–3,2 %; costal 25 kg 30–81 %; costal 50 kg 60–161 %; carga de llama 36–97 %.

### 3.3 Qué descarta y qué no

- **Descartadas: las unidades de producto individual.** Granos, maní, ají, papa o mazorca dejan el archivo de UR278 en 0,0005–0,4 % de la capacidad de Qolqawasi. Para llenar el depósito harían falta entre 250 y 200 000 veces más unidades de las registradas. Aunque los quipus cubrieran solo una fracción del flujo, un archivo de 34 quipus que registra 0,02–0,05 t de maní (unidades individuales) no es un archivo de depósito estatal.
- **Marginal: el kilogramo.** 61,8 t para UR278 = 1,6 % de la capacidad (3,9 colcas). Posible si el archivo cubre un episodio corto, pero no explica por qué se necesitan 34 quipus y 9 columnas para 62 t.
- **Físicamente plausibles: unidades de bulto, entre ~10 y ~50 kg.** Arroba, carga de llama, costal y fanega dejan UR278 entre 18 % y 80 % de la capacidad, y una cabecera mediana entre 0,6 % y 2,6 % (1,5–6 colcas). Es el rango que hace del archivo un archivo de depósito.
- **La cuota 47** solo tiene sentido físico como bulto: 47 costales = 1,2 t (2 m³, ~1/5 de una celda); 47 kg = 0,08 m³, demasiado poco para sostener un turno de personal; 47 ajíes = 0,2 kg, absurdo. La cuota es consistente con “47 bultos”, no con “47 unidades de producto”.
- **Coincidencia estructural (especulativa):** una celda media de UR278 (248 unidades) equivale a 6,2 t = 10 m³ con costal de 25 kg, es decir, **~0,4 de una colca media**; y 28 filas × 9 columnas = 252 celdas frente a 245 colcas+cámaras. Son coincidencias numéricas, no evidencia: hay muchas maneras de contar colcas y de elegir la celda. No las uso para el veredicto.

**Veredicto: la arqueología de depósitos DESCARTA las unidades de producto individual y fija la escala en bultos de ~10–50 kg (carga, costal, arroba, fanega). No distingue entre ellas.** La unidad exacta queda como [propuesto], pero el orden de magnitud queda apoyado con datos por la capacidad física: el quipu cuenta **bultos/cargas**, no granos, ajíes ni mazorcas.

---

## 4. Benford y dígitos: ¿recuento natural o asignación administrativa?

### 4.1 Diseño

- Tipo de quipu según `11_rosetta/fA_redondeo_por_quipu.csv`: **asignación** = ≥80 % de cuerdas intactas ≥10 múltiplos de 10 (26 quipus); **recuento** = ≤20 % (159); intermedio (145).
- Cuerdas intactas (terminación K) con valor ≥ 10: 190 quipus con n ≥ 20.
- **Primer dígito:** χ² contra Benford, con p simulado bajo Benford (B = 1000) por quipu; BH sobre los 190.
- **Último dígito:** uniformidad 0–9, por quipu; exceso de 0.
- **Control de circularidad:** la etiqueta “asignación” se define con el dígito final, así que repetí todo excluyendo los valores múltiplos de 10 (y de 5).

### 4.2 Resultados

| conjunto | n valores | MAD vs Benford | χ² (8 gl) | p | % de 1 como primer dígito |
|---|---|---|---|---|---|
| recuento | 7 026 | 0,0269 | 574,5 | 7·10⁻¹¹⁹ | 39,4 |
| intermedio | 5 813 | 0,0390 | 917,0 | 1·10⁻¹⁹² | 45,5 |
| asignación | 807 | 0,0220 | 58,7 | 8·10⁻¹⁰ | 32,2 |
| Benford teórico | — | 0 | — | — | 30,1 |

- **Por quipu: 99/190 (52 %) rechazan Benford (q < 0,05).** Incluso entre los 61 quipus con rango >100 (los únicos donde Benford es exigible), rechazan 39 %.
- **La predicción “asignación viola Benford, recuento lo sigue” NO se cumple.** El grupo de asignación tiene un MAD *menor* (0,022) que el de recuento (0,027), y por quipu la comparación de MAD da mediana 0,068 (asignación, n=14) frente a 0,055 (recuento, n=93), Mann-Whitney **p = 0,072 en la dirección contraria** a la predicha. El χ² de asignación está dominado por un exceso en los dígitos 5 y 6 (9,3 % y 10,7 %), que es exactamente lo que producen los números redondos 50, 60, 500…, no un déficit genérico de Benford.
- **Control de circularidad:** al excluir múltiplos de 10, el grupo de asignación se queda con solo 86 valores; su MAD es 0,0347 y no rechaza Benford (p = 0,10), mientras el recuento sigue rechazando (n = 6 201, p = 4·10⁻⁹⁸). La diferencia entre grupos desaparece cuando se quita el dígito que define la etiqueta.
- **Último dígito:** 116/190 quipus (61 %) rechazan la uniformidad; la fracción mediana de 0 es 0,207 (uniforme = 0,10). Por tipo: recuento 0,120 (34 % rechaza), intermedio 0,355 (84 %), asignación 0,857 (100 %). El exceso de 0 es real pero **es la definición de “asignación”**: no es un hallazgo independiente.

### 4.3 Por qué falla Benford (explicación aburrida)

La distribución de valores individuales no es de escala libre: **46,7 % de las 40 097 cuerdas con valor están entre 1 y 9**, 15,8 % entre 10 y 19, y solo 15,7 % supera 100 (mediana = 10; moda = 1, con 5 880 cuerdas). Benford exige varios órdenes de magnitud y una mezcla logarítmica; aquí hay una concentración masiva en cuentas pequeñas. El primer dígito observado (42,2 % de 1) es aún más extremo que el que predice un modelo de rango uniforme por quipu (29,4 % de 1), porque los valores se amontonan en 10–30, no porque haya una “anomalía administrativa”.

**Veredicto: Benford DESCARTADO como diagnóstico de recuento vs asignación en este corpus.** No separa los tipos (la diferencia va en dirección contraria y no es significativa tras quitar la circularidad) y la mayoría de los quipus lo viola por la concentración de valores pequeños. El dígito final 0 sí separa los grupos, pero por construcción. **Resultado negativo útil:** el corpus no es “benfordiano”; sus cuerdas son, sobre todo, cuentas pequeñas (1–50), y los totales de miles son agregados de unas pocas cuerdas grandes.

---

## 5. Resumen de veredictos

| # | Hipótesis | Veredicto | Cifra clave | Nivel |
|---|---|---|---|---|
| 1 | Las columnas de UR278 son grados de edad/sexo | **descartada** | CV 0,184 [0,152; 0,230] vs 0,50–0,90 exigido; p < 2,5·10⁻⁴ | demostrado (condicionado a un modelo demográfico estándar) |
| 2 | Las columnas del corpus son edades/sexos | **descartada en 136/159 tablas (86 %); indecidible en 23 (14 %)** | las 23 pasan por la flexibilidad de la permutación; ninguna es monótona ni piramidal | apoyado con datos |
| 3 | Las columnas vienen en pares varón/mujer | **descartada** | correlación residual tras quitar tamaño: 0,36 / 0,18 / −0,02 / −0,04; razón mediana 1,12 | apoyado con datos |
| 4 | Las columnas son una partición administrativa casi igual (9 partes) | **compatible** | CV 0,18; max/min 1,70; 4/28 filas con max/min ≥ 3,6 | apoyado (planitud) / propuesto (partición) |
| 5 | Los totales se “llenan” a 10/100/500/1000/10 000 | **descartada** | 0/12 pruebas evaluables; ratios 0,75–1,18; q ≥ 0,95 | demostrado (negativo) |
| 6 | Los totales se redondean a decenas | **apoyada** | 15,7 % múltiplos de 10 vs 12,6 % [11,8; 13,4] del nulo | apoyado con datos |
| 7 | La unidad es un producto individual (grano, ají, papa, mazorca) | **descartada** | UR278 = 0,0005–0,4 % de los 6 400 m³; harían falta ×250–200 000 | demostrado con los supuestos de capacidad/densidad |
| 8 | La unidad es un bulto de ~10–50 kg (carga, costal, arroba, fanega) | **compatible; unidad exacta indecidible** | UR278 = 18–80 % de la capacidad; cabecera = 1–6 colcas | propuesto |
| 9 | Benford separa recuento de asignación | **descartado** | 99/190 quipus rechazan; asignación MAD 0,022 < recuento 0,027; MW p = 0,072 en dirección opuesta | demostrado (negativo) |
| 10 | El dígito final 0 marca asignación | **demostrado pero circular** | 0,857 (asignación) vs 0,120 (recuento); la etiqueta se define con ese dígito | definicional |

## 6. Resultados negativos (los que también cuentan)

- **No hay pirámide demográfica** en UR278 ni en el 86 % de las tablas; el 14 % restante no es evidencia positiva (el modelo es demasiado flexible y ninguno de esos perfiles es monótono ni piramidal).
- **No hay pares de sexo**: los pares de columnas covarían solo por el tamaño del registro; las razones no son 1:1.
- **No hay llenado de unidades decimales**: ni 90–110, ni 450–550, ni 900–1100, ni 4 500–5 500, ni 9 000–11 000. El único efecto es un redondeo débil a decenas.
- **No hay diferencia Benford entre recuento y asignación**; el control de circularidad elimina la diferencia aparente.
- **No hay unidades de producto individual**: el archivo de UR278 sería 0,0005–0,4 % de Qolqawasi.
- **No hay señal de 9 productos, 9 meses ni 9 zonas ecológicas**: la planitud del perfil las descarta con el mismo argumento que la edad.
- **Negativo metodológico:** el test de Benford por quipu tiene poca potencia y el de demografía tiene demasiada flexibilidad; ninguno de los dos sirve como “detector” automático.

## 7. Límites y supuestos

1. **El modelo demográfico es un supuesto**, no un dato: usé una población estable Siler con e0 ≈ 28 y dos esquemas de bandas (5 años y tipo Guaman Poma). Aun con el esquema más plano (S3), el CV exigido es 0,50; el observado es 0,18. Para refutar el veredicto habría que invocar un censo con clases de edad *diseñadas para ser iguales en tamaño*, que no es un censo demográfico sino una partición administrativa (y entonces la hipótesis 4 es la relevante).
2. **La capacidad de 6 400 m³ y las 245 unidades son estimaciones** de Urton (2017) y Urton y Chu (2015); la densidad aparente varía 0,3–0,8 t/m³. La conclusión sobre unidades individuales es robusta en todo ese rango (0,0005–0,4 %); la frontera entre “kg” y “bulto” no lo es.
3. **El espacio temporal del archivo es desconocido**: si los 34 quipus cubren un solo día, un flujo de 62 t es imposible; si cubren años, es normal. La arqueología no resuelve la unidad exacta, solo el orden de magnitud.
4. **Los valores son los decodificados por KFG**, con errores de lectura posibles; no corregí por cuerdas rotas salvo en el análisis de dígitos (terminación K), donde la selección puede sesgar.
5. **La etiqueta “asignación/recuento” de 11_rosetta es circular** para cualquier análisis de dígitos; lo digo y lo controlo, pero no hay una etiqueta independiente disponible.
6. **Las tablas se reconstruyen con el grupo modal**; quipus con grupos de tamaños mixtos pueden quedar mal representados. Se excluyeron K > 12 por no ser un censo de 10–12 grados.
7. **Corrección múltiple:** BH-FDR en las 14 pruebas de unidades, en los 190 quipus de Benford y en los 159 de demografía; los p citados sin corregir se identifican como tales.
8. **No usé procedencia de museo como lugar de origen** en ninguna conclusión.

## 8. Para el coordinador

- **La demografía está descartada, y no por poco.** En UR278 el perfil de las 9 columnas tiene CV 0,184 [0,152; 0,230] y max/min 1,70; cualquier pirámide preindustrial (e0 ≈ 28) exige CV 0,50–0,90 y max/min 3,6–7,1. Bajo el modelo de edad, p < 2,5·10⁻⁴ (0/4 000 simulaciones). Solo 4 de 28 filas alcanzan el max/min mínimo. En el corpus, 136/159 tablas (86 %) se rechazan; las 23 restantes no son evidencia positiva.
- **El hallazgo positivo es una partición, no una taxonomía.** Las 9 columnas son casi iguales entre sí (CV 0,18). Eso descarta edades, sexos, productos, meses y zonas ecológicas —todas tendrían categorías dominantes— y apunta a **9 partes administrativas deliberadamente equilibradas** (ayllus, parcialidades, cuadrillas, depósitos). Es la primera restricción semántica fuerte de esta ronda.
- **No hay “llenado” de las unidades decimales incas.** 0/12 pruebas evaluables en ventanas ±10 % alrededor de 50/100/500/1000/5000/10 000; las ratios van de 0,75 a 1,18. Solo sobrevive un redondeo débil del total a las decenas (15,7 % vs 12,6 % del nulo, p < 0,002), no a 100/500/1000/10 000.
- **La unidad física es de bulto, no de producto individual.** UR278 (61 790 unidades) sería 0,0005–0,4 % de los 6 400 m³ de Qolqawasi si contara granos, ajíes, papas o mazorcas; con unidades de 10–50 kg (arroba, carga de llama, costal, fanega) ocupa 18–80 % de la capacidad, que es lo que se espera de un archivo de depósito. La cuota 47 solo tiene sentido como “47 bultos”. La unidad exacta sigue abierta: **indecidible con estos datos**.
- **Benford no sirve aquí.** 99/190 quipus (52 %) lo violan; el grupo de asignación se ajusta *mejor* que el de recuento (MAD 0,022 vs 0,027) y la diferencia desaparece al excluir los múltiplos de 10. La razón es aburrida: 46,7 % de las 40 097 cuerdas valen 1–9 y la mediana es 10; no hay escala libre.
- **Dato de magnitud que conviene reutilizar:** las cuerdas son cuentas pequeñas (moda 1, mediana 10; solo 15,7 % > 100), mientras las cabeceras de Incahuasi son ~2 000 = 9 columnas × ~250. El archivo de Incahuasi es atípico: registra flujos de bultos, frente a las cuentas pequeñas que dominan el resto del corpus.
- **Recomendación 1:** contrastar la hipótesis de “9 partes” con listas coloniales de ayllus/mitades (Chucuito 1567, visitas) y con los quipus de 9 columnas de otros archivos; buscar si el orden de las 9 columnas se conserva entre quipus (ya hay estabilidad de tamaño).
- **Recomendación 2:** usar la cuadrícula de 23 × 23 cm de U.A. 07 para calibrar la unidad (un cuadro = ¿1–6 kg?) y probar si 47 es un número de bultos por registro; el archivo de Urton y Chu no publica el peso, pero la cuadrícula es la única “regla física” del sitio.
- **Recomendación 3:** no gastar más esfuerzo en Benford ni en pirámides de edad para este corpus; sí en cambiar la pregunta de “qué categoría” a “qué parte administrativa” y en buscar unidades de bulto en las fuentes coloniales (costal, carga, fanega, arroba).


