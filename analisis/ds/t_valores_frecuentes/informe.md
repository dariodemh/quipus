# Vocabulario numérico de los quipus: qué valores se repiten y qué es artefacto

**Carpeta:** `analisis/ds/t_valores_frecuentes/`
**Datos:** KFG aplanado, `analisis/datos/cuerdas.csv` + `quipus.csv` (651 quipus, 57 818 cuerdas).
**Unidad de análisis:** el quipu. Las cuerdas se usan para describir; toda inferencia se hace por quipu o con nulos aplicados dentro/fuera de cada quipu.
**Semilla:** 20261018.
**Scripts:** `01_explorar.py`, `02_heaping_global.py`, `03_concentracion.py`, `04_codigos.py`, `05_procedencia_color.py`, `06_inspeccion.py`, `07_robustez.py`, `08_chequeos.py`, `09_resumen.py`, `10_bootstrap.py`, `11_vecinos.py`.
**Tablas:** `tabla_heaping_global.csv`, `tabla_concentracion.csv`, `tabla_codigos.csv`, `tabla_procedencia.csv`, `tabla_color.csv`, `tabla_bootstrap.csv`, `tabla_vecinos.csv`.

---

## 1. Pregunta

¿Qué valores concretos (1, 2, 5, 10, 12, 15, 30, 40, 100…) aparecen más de lo que predice una distribución log-uniforme/Benford? ¿Cuántos quipus sobrerrepresentan cada valor (nulo por permutación entre quipus)? ¿Hay valores que funcionan como **códigos** y no como cantidades? ¿Se concentran por **procedencia** o por **color**?

## 2. Método

### 2.1 Datos y limpieza

- Se excluyen 17 650 cuerdas con `valor = 0` y `nudos` vacío (ausencia, no cero) y 65 ceros reales. Quedan **40 097 cuerdas con nudos en 640 quipus**; 11 quipus no tienen ninguna cuerda con nudos.
- Todos los valores son enteros (sin decimales); máximo 320 535.
- Se conservan las 128 cuerdas superiores con nudos (`union = T`) en el análisis principal y se repite todo sin ellas: los resultados no cambian (top de valores idéntico; p. ej. 1 pasa de 5 880 a 5 859 cuerdas).
- Se comprobó el artefacto de transcripción descrito en la literatura (nudo largo con ≥ 10 vueltas cuyo número de vueltas se confunde con el valor): afecta a **362 cuerdas (0,9 %)** y a solo 7 de las 325 cuerdas de valor 100 y 4 de las 125 de valor 200. **No explica el heaping.**

### 2.2 Nulos para el heaping global

El encargo pide comparar con log-uniforme/Benford. Se usan cuatro nulos, de más ingenuo a más exigente:

- **A. Log-uniforme:** P(v) ∝ 1/v, v = 1…320 535 (H ≈ 13,3).
- **B1. Dígitos uniformes por longitud:** dentro de cada longitud (1, 2, 3… dígitos) todos los valores igual de probables. Es el nulo de "ningún número favorito".
- **B2. Dígitos independientes con marginales ajustadas dentro de cada longitud:** P(v) = Π P(dígito en su posición | longitud). Conserva el sesgo empírico de cada dígito en cada posición (el exceso de 0 en las unidades, la caída del primer dígito) y deja como señal solo las **combinaciones** de dígitos favoritas. Es el nulo serio para "valores concretos".
- **C. Uniforme dentro de (longitud, suma de dígitos):** control grueso del **coste de nudos**. Escribir 10 cuesta 1 nudo y 47 cuesta 11; si el heaping es solo economía de nudos, valores del mismo coste deberían ser igual de frecuentes. El nulo C es ciego para 10, 100 y 1 000 (son los únicos de su estrato), lo que se indica donde importa.

p-valores de Poisson de una cola por valor y corrección de Benjamini–Hochberg (BH-FDR) sobre todos los valores. **Advertencia:** el p de Poisson trata las 40 097 cuerdas como independientes y es anticonservador; por eso la inferencia principal se hace a nivel de quipu y los q globales se reportan como descriptivos. Como control adicional se hizo un **bootstrap por quipu** (300 remuestreos de los 640 quipus, reestimando B2 en cada muestra).

### 2.3 Nulo por permutación entre quipus

Para cada valor v se cuenta en cuántos quipus aparece (≥ 1, ≥ 2, ≥ 3) y en cuántos quipus está sobrerrepresentado (p de Poisson de una cola < 0,05 con la composición de décadas de ese quipu). El nulo **baraja los valores entre quipus dentro de cada estrato (longitud, primer dígito)**: conserva el número de cuerdas de cada década en cada quipu y la frecuencia global de cada valor, y destruye solo la asociación valor–quipu. Esto controla la explicación aburrida "este quipu usa números grandes y aquel pequeños". 1 000 permutaciones; p empírico = (1 + #{nulo ≥ obs})/(1 + 1 000); BH sobre los 71 valores probados (n ≥ 50 más los candidatos del encargo).

### 2.4 Nulos para códigos, procedencia y color

- **Posición de etiqueta:** se marca la primera cuerda de cada grupo (6 520 grupos) y se permuta esa marca **dentro de cada quipu** entre sus colgantes de nivel 0. Un valor que funciona como etiqueta/encabezado debe sobrerrepresentarse ahí.
- **Papel aritmético:** se identifica madre (tiene hijas), suma exacta (valor = Σ hijas) y cuerda superior.
- **Procedencia:** unidad = quipu; Fisher exacto de presencia del valor en el sitio vs el resto; BH sobre 90 pruebas (18 valores × 5 sitios con ≥ 15 quipus).
- **Color:** se toma el token primario (W, AB, MB, YB, B, KB…). Test estratificado por quipu: obs vs esperado con varianza hipergeométrica, es decir, se compara el color de las cuerdas con valor v contra las demás cuerdas **del mismo quipu**; BH sobre 108 pruebas (18 valores × 6 colores). Se repite solo con colores sólidos (sin mezclas).

---

## 3. Resultados

### 3.1 La distribución no es log-uniforme ni Benford: es magnitud + redondeo decimal

- **Benford del primer dígito** (valores ≥ 10, n = 21 387): χ² = 2 655,8, gl = 8, p < 10⁻³⁰⁰. El primer dígito 1 aparece 1,43× lo que predice Benford; el 9, solo 0,37×. **Benford se rechaza.**
- **Log-uniforme** también se rechaza como modelo global: sobrerrepresenta los valores pequeños (obs/esp 1,9–2,7 para 1–5) y produce un bulto en 10–100 que una ley monótona no puede generar (obs/esp 7,1 en 10; 10,7 en 100). Log-uniforme y Benford son **malos modelos de este corpus** y no sirven como nulo único.
- La estructura real está en los dígitos: en valores de 2 dígitos (n = 15 081), el **32,7 % termina en 0** (4 926) frente a ~10 % si los dígitos fueran uniformes (**×3,3**); el dígito de las decenas cae monótonamente 1 > 2 > … > 9 (6 320 → 263).
- Conclusión: el "vocabulario" dominante no son números sueltos sino **una clase: los múltiplos de 10 y de 100**. El redondeo decimal es el hecho grueso y explica la mayor parte de lo que a primera vista parece "números favoritos".

### 3.2 Casi todos los candidatos del encargo se explican por los márgenes de dígitos

Razón observado/esperado bajo B2 (dígitos independientes), valores con n ≥ 100 (se incluye 5 como control de un dígito), con IC 95 % bootstrap por quipu:

| valor | n cuerdas | quipus | obs/esp B1 | **obs/esp B2** | IC 95 % bootstrap | q-BH B2 |
|---|---|---|---|---|---|---|
| 100 | 325 | 104 | 59,4 | **2,05** | [1,74; 2,41] | 1,7e-28 |
| 47 | 135 | 55 | 0,81 | **1,84** | [1,12; 2,62] | 2,8e-08 |
| 200 | 125 | 55 | 22,9 | **1,67** | [1,33; 1,98] | 2,0e-05 |
| 110 | 141 | 85 | 25,8 | **1,48** | [1,24; 1,82] | 0,001 |
| 33 | 220 | 84 | 1,31 | **1,37** | [1,10; 1,65] | 0,0008 |
| 22 | 389 | 148 | 2,32 | **1,23** | [1,07; 1,37] | 0,004 |
| 50 | 338 | 145 | 2,02 | 1,13 | [0,98; 1,27] | 0,12 |
| 11 | 635 | 232 | 3,79 | 1,12 | — | 0,057 |
| 15 | 567 | 206 | 3,38 | 1,06 | [0,97; 1,13] | 0,29 |
| 10 | 2 141 | 391 | 12,8 | 1,04 | [0,96; 1,12] | 0,21 |
| 12 | 675 | 235 | 4,03 | 1,01 | [0,91; 1,11] | 0,65 |
| 20 | 944 | 253 | 5,63 | 0,96 | [0,89; 1,05] | 0,96 |
| 30 | 536 | 201 | 3,20 | 0,91 | [0,82; 1,02] | 1 |
| 5 | 1 499 | 341 | 0,72 | 0,72 | [0,65; 0,80] | 1 |

**Negativo importante:** 1, 2, 5, 10, 12, 15, 20, 30, 40 y 50 **no** sobreviven al control de dígitos. Su frecuencia aparente se deriva de (i) que los valores pequeños son más comunes y (ii) que el 0 en las unidades es frecuente. En particular:

- **10 no es especial frente a otros múltiplos de 10.** Destaca frente a 11–19 (4,6× la media de sus vecinos), pero eso es la cara visible de que el 0 en las unidades es frecuente; una vez que se acepta el sesgo del dígito de las decenas hacia 1, su exceso desaparece (obs/esp 1,04; IC incluye 1). Su pico es el de la clase "múltiplo de 10", no un privilegio del 10.
- **15 no es especial** frente a 12–19 (obs/esp 1,06; IC [0,97; 1,13]).
- **1 y 2** aparecen como "exceso" solo porque el nulo B2 para números de 1 dígito es uniforme entre 1 y 9; el exceso refleja la pendiente de la distribución de magnitud, no un número favorito. No se cuentan como hallazgo.

Solo sobreviven con q < 0,05 y n ≥ 100: **100, 47, 200, 110, 33, 22**. (También salen 1, 2 y 3, pero son artefactos del nulo uniforme de 1 dígito y no se interpretan como preferencia; y **1 000**, con 44 cuerdas en 24 quipus y 5,65×, que pertenece a la clase de las centenas/millares redondos.)

**Control libre de modelo (vecinos inmediatos).** Para no depender de la independencia de dígitos de B2, se compara cada valor redondo con sus nueve vecinos de la misma decena:

| valor | n | total de su decena (v…v+9) | % de la decena | media de los 9 vecinos | veces la media |
|---|---|---|---|---|---|
| 10 | 2 141 | 6 320 | 34 % | 464 | 4,6× |
| 40 | 389 | 1 238 | 31 % | 94 | 4,1× |
| 100 | 325 | 553 | **59 %** | 25 | **12,8×** |
| 110 | 141 | 349 | 40 % | 23 | 6,1× |
| 200 | 125 | 229 | **55 %** | 12 | **10,8×** |
| 300 | 45 | 108 | 42 % | 7 | 6,4× |

Los picos son **locales**, no el resultado de una tendencia suave: 100 es el 59 % de todas las cuerdas con valor 100–109 y 12,8× la media de 101–109. Para 10 y 40 el pico es la cara visible del exceso de 0 en las unidades (10 es el único múltiplo de 10 de su decena); para 100, 200 y 110 hay un exceso **adicional** sobre los márgenes de dígitos (B2), que es el que sobrevive.

### 3.3 Test de clases: el único exceso de clase robusto son las centenas redondas

| clase | obs | esp B2 | razón | q-BH |
|---|---|---|---|---|
| múltiplos de 5 | 10 245 | 10 500 | 0,97 | 1 |
| múltiplos de 10 | 6 944 | 6 750 | 1,03 | 0,0098 |
| **múltiplos de 100** | 776 | 421 | **1,84** | 5e-54 |
| repdigitos (11, 22, …, 222) | 1 666 | 1 380 | 1,21 | 1e-13 |
| palíndromos (≥ 2 dígitos) | 2 039 | 1 730 | 1,18 | 3e-13 |
| potencias de 10 sin el 1 (10, 100, 1 000…) | 2 513 | 2 230 | 1,13 | — |
| suma de dígitos ≤ 3 (solo pendiente de magnitud) | 18 027 | 12 000 | 1,50 | <1e-300 |

Lectura: **no hay "redondeo a 5"** (0,97); el redondeo es a 10 (leve, 1,03) y sobre todo **a 100 (1,84)**. Que los múltiplos de 10 no excedan bajo B2 **no** significa que no haya redondeo: significa que el redondeo ya está incorporado en el marginal del dígito 0; el hecho bruto es el 32,7 % de unidades 0 de §3.1. Lo que B2 añade es que, *dado* ese marginal, solo las centenas redondas siguen sobrando. La clase "suma de dígitos ≤ 3" es solo la pendiente de magnitud (números pequeños más frecuentes), no un número favorito; se incluye para mostrar que un nulo ingenuo la confundiría con una preferencia. Los repdigitos tienen un exceso pequeño (1,21) pero **casi todo viene de copias**: 222 tiene 35 cuerdas en 16 quipus, 20 de ellas en HP055 + UR1084, que son el mismo registro; 33 y 22 también están inflados por ese par. (El 1 infla cualquier clase que lo contenga: las "potencias de 10" dan 1,95× con el 1 y solo 1,13× sin él; por eso no se reporta esa clase como hallazgo.)

### 3.4 ¿Cuántos quipus sobrerrepresentan cada valor?

Con el nulo de permutación entre quipus (estratos de década) y 71 valores probados:

- **Hay 1 007 excesos (valor, quipu) observados frente a 349 esperados: 2,89×.** Es decir, el fenómeno es general: los valores no se reparten al azar entre quipus, cada quipu tiene su repertorio.
- **40 de 71 valores** tienen más quipus sobrerrepresentados de lo esperado (q < 0,05).
- El HHI medio por quipu es **0,168 observado vs 0,127 nulo** (p = 0,005, 200 permutaciones): dentro de cada quipu se repiten valores más de lo que predice su composición de décadas.
- La prevalencia es **menor que la esperada por azar para todos los valores**: 1 está en 365 quipus (esperado 580), 10 en 391 (473), 100 en 104 (201), 47 en 55 (107), 200 en 55 (100). Ningún valor es "ubicuo": todos están concentrados en un subconjunto de quipus.

Casos concretos (n_sobre = quipus sobrerrepresentados; nulo entre paréntesis):

| valor | n cuerdas | quipus con el valor | n_sobre | n_sobre nulo | quipu que más aporta |
|---|---|---|---|---|---|
| 1 | 5 880 | 365 | 53 | 5,7 | UR003: 276 (Leymebamba) |
| 2 | 3 627 | 389 | 36 | 9,3 | — |
| 3 | 2 327 | 386 | 30 | 10,1 | — |
| 10 | 2 141 | 391 | 43 | 2,9 | MM001: 73 (Huacho) |
| 20 | 944 | 253 | 22 | 1,9 | — |
| 30 | 536 | 201 | 22 | 1,2 | — |
| 100 | 325 | 104 | 20 | 3,9 | UR1109: 53 (Ica) |
| 200 | 125 | 55 | 10 | 1,8 | UR1109: 20 (Ica) |
| 15 | 567 | 206 | 18 | 7,6 | UR267A: 25 / UR255: 24 (Incahuasi) |
| 47 | 135 | 55 | 3 | 3,1 | UR266: 24 / UR275: 24 (Incahuasi) |
| 110 | 141 | 85 | 11 | 3,8 | KH0001: 9 |
| 33 | 220 | 84 | 7 | 3,3 | UR1084: 18 / HP055: 17 |
| 22 | 389 | 148 | 13 | 5,0 | UR1084: 29 / HP055: 18 |

El valor **47** es el más concentrado de todos (HHI 0,076 vs 0,017 nulo): 48 de sus 135 cuerdas están en **dos quipus emparejados de Incahuasi** (UR266 y UR275, 24 cada uno). El valor **100** es el que más sobrerrepresentación produce en términos relativos, pero está repartido: los 3 quipus mayores aportan solo el 26 % de sus 325 cuerdas. UR1109 (Ica) es un registro de cantidades redondas encadenadas (100 ×53, 120 ×26, 200 ×20, 125 ×14, 150 ×9, 110 ×8), no un código.

### 3.5 ¿Hay valores que funcionan como códigos?

Se buscaron tres firmas de código: (a) aparecer en la **primera cuerda del grupo** (posición de etiqueta/encabezado), (b) **no** participar en sumas, (c) repetirse una vez por grupo en vez de muchas veces.

- **Solo el valor 1 muestra la firma (a):** 755 primeras cuerdas con 1 frente a 640 esperadas (×1,18; p = 0,0010; q = 0,019). El efecto sobrevive al excluir los quipus dominados por unos (×1,19; p = 0,002) y lo sostienen 126 quipus, no uno solo (los mayores: UR198 +15,2; UR004 +11,6; UR087 +10,8). Es un efecto **pequeño pero robusto**: 1 se usa a veces como marcador/placeholder, no solo como cantidad. Sin embargo, **no es una etiqueta única**: el 63 % de los grupos con ≥ 3 cuerdas que contienen un 1 contienen ≥ 2 unos (1 032/1 640), así que el uso es mixto. Además, de las 117 cuerdas con 1 que son madres de ≥ 2 hijas, **ninguna** suma exactamente (0/117), frente a 72/1 798 = 4 % en el corpus: el 1 no funciona como total.
- **Ningún otro valor se comporta como etiqueta.** Al contrario, 11–19, 22, 33, 47, 100 y 200 están **subrepresentados** en la primera posición: 47 aparece 7 veces donde se esperaban 26,6 (déficit p < 0,001); 15, 101 vs 130; 12, 81 vs 111. Es el patrón opuesto al de un encabezado de columna.
- **100 y 200 no son sumas:** 0 de las 43 madres con 100 suman exactamente (0/6 con ≥ 2 hijas), frente a 72/1 798 = 4 % de las madres con ≥ 2 hijas; 0,3 % de las cuerdas con 100 son cuerdas superiores y el 90,8 % son colgantes de nivel 0. Se usan como cantidades registradas, no como totales.
- **222** tiene un exceso llamativo (2,79× B2, q = 3e-05), pero 20 de sus 35 cuerdas están en HP055 + UR1084 (copias). No se sostiene como código.

**Conclusión:** no hay ningún valor con la firma completa de código. El candidato más plausible es **1 como marcador** (apoyado con datos, efecto pequeño); **100 como unidad de cuenta/atractor de redondeo** (propuesto); **47 y los repdigitos como códigos locales** (especulativo, contaminado por copias).

### 3.6 Procedencia

5 sitios con ≥ 15 quipus: Pachacamac (87), Incahuasi (52), Ica (47), Leymebamba (22), Huaquerones (16). **Ninguna asociación valor–sitio sobrevive a BH: 0 de 90 pruebas.**

Lo más cercano (descriptivo, q = 0,116): **Leymebamba** tiene alta prevalencia de valores pequeños (10 en 90,9 % de sus quipus vs 60 % del resto; 1 en 86,4 % vs 56 %; 11 en 68,2 % vs 35,1 %; OR 3,4–6,7; p 0,0026–0,013), pero son solo 22 quipus y no sobrevive a la corrección. **Ica y Pachacamac** van en dirección opuesta para 1 y 2 (menos prevalencia).

El hallazgo más fuerte en crudo es Incahuasi: **15** es el 15,7 % de los valores de su década (10–19) frente al 8,4 % del resto (OR 2,04; p = 1,7e-07), y **47** es el 33,2 % de su década (40–49) frente al 6,7 % (OR 6,89; p = 1,9e-21). Pero al quitar los dos quipus emparejados que los sostienen, el efecto **desaparece**:

- 15, sin UR267A/UR255: 7,2 % vs 8,4 % (OR 0,85; p = 0,43).
- 47, sin UR275/UR266: 11,9 % vs 6,7 % (OR 1,87; p = 0,038, ya no significativo tras multiplicidad).

Es decir, **el "estándar de 15" y el "47" de Incahuasi son el mismo registro replicado en quipus pareados**, no un vocabulario del sitio. Es el resultado negativo más importante de esta sección.

### 3.7 Color

108 pruebas valor × color; **7 sobreviven a BH**, todas con efectos pequeños:

| par | obs | esp | razón | q | consistencia por quipu |
|---|---|---|---|---|---|
| 1 – B (azul) | 281 | 240 | 1,17 | 0,005 | +38 / −36 quipus (signo p = 0,91) |
| 3 – B | 132 | 103 | 1,28 | 0,005 | +35 / −41 (p = 0,57) |
| 1 – W (blanco) | 1 837 | 1 920 | 0,96 | 0,021 | — |
| 30 – KB (marrón oscuro) | 19 | 10,3 | 1,85 | 0,044 | +14 / −56 (¡dirección consistente negativa!) |
| 47 – YB | 21 | 13,3 | 1,58 | 0,044 | 3 quipus aportan el 81 % de la desviación |

(Los otros dos pares que sobreviven son déficits: 2–W, 0,94×, q = 0,021, y 2–YB, 0,88×, q = 0,05.)

En colores sólidos los tamaños no cambian (1-B 1,22×; 3-B 1,19×; 30-KB 1,93×; 47-YB 1,53×). Pero **la dirección no es consistente entre quipus**: el z agregado sale de que unos pocos quipus grandes aportan desviaciones positivas, mientras la mayoría va en contra. No hay un código de color panandino; como mucho, asociaciones locales débiles. Esto coincide con el equipo de color de la ronda 1 (efecto pequeño, dirección no común).

---

## 4. Resultados negativos (resumen)

1. **No hay "números favoritos" universales**: 1, 2, 5, 10, 12, 15, 20, 30, 40 y 50 no superan el nulo de dígitos (B2). El aparente heaping es magnitud + 0 en las unidades.
2. **Benford y log-uniforme se rechazan** como modelos del corpus; no sirven como nulo único.
3. **No hay redondeo a 5** (múltiplos de 5: 0,97×).
4. **47 no es un código panandino**: 48/135 cuerdas están en dos quipus pareados de Incahuasi.
5. **El efecto "15 de Incahuasi" desaparece** al quitar los dos quipus pareados (OR 2,04 → 0,85; p = 0,43).
6. **Ninguna asociación valor–procedencia sobrevive a BH** (0/90).
7. **Ninguna asociación valor–color es consistente en dirección** entre quipus.
8. **222 y los repdigitos** están inflados por copias (HP055/UR1084).
9. **100 no es un código**: es una cantidad redonda repartida en 104 quipus, sin papel de suma ni de etiqueta.

## 5. Nivel de evidencia

| afirmación | nivel |
|---|---|
| El sistema numérico está dominado por una distribución de magnitud con redondeo decimal (32,7 % de los valores de 2 dígitos terminan en 0) | **demostrado** (descriptivo, n = 15 081) |
| Benford y log-uniforme no describen el corpus | **demostrado** (χ² y razones; p < 1e-300) |
| Los valores se concentran por quipu: 1 007 excesos vs 349 esperados (2,9×); HHI 0,168 vs 0,127 | **apoyado con datos** (permutación entre quipus, p = 0,005) |
| 100, 200, 110 tienen exceso global robusto (IC bootstrap > 1) | **apoyado con datos** |
| 100 funciona como unidad de cuenta / atractor de redondeo (pachaca) | **propuesto** (no distinguible de redondeo por estos datos) |
| 1 se usa a veces como marcador en la primera cuerda del grupo (×1,18; p = 0,001) | **apoyado con datos**, efecto pequeño |
| 15 y 47 como "estándares locales" de Incahuasi | **propuesto** en la literatura; aquí se muestra que es **artefacto de copia** (dos pares de quipus) |
| 47/33/22 como códigos | **especulativo** (concentración por copias) |
| Asociaciones valor–color (1-B, 3-B, 30-KB, 47-YB) | **especulativo**: significativas en agregado, inconsistentes por quipu |

## 6. Limitaciones

- Los valores KFG son una decodificación, no una lectura verificada; Thompson documenta errores de tipo de nudo y de posición. Un 100 mal posicionado (un nudo simple en el lugar equivocado) produciría el mismo efecto que un "redondeo"; la comprobación con OKR (`knot`, `knot_cluster`) queda pendiente.
- 11 quipus no tienen cuerdas con nudos y quedan fuera.
- `procedencia` no es lugar de origen arqueológico (el brief lo prohíbe expresamente); "Ica" y "Nazca" son regiones, no sitios.
- Los quipus pareados/copias (HP055–UR1084, UR255–UR267A, UR266–UR275) inflan la repetición de valores; se identificaron por sus valores, no por una auditoría de copia.
- El nulo B2 es conservador para las clases (absorbe el exceso de 0 en las unidades) y ciego para 10/100/1 000 en el nulo de coste.
- El bootstrap por quipu reestima B2 pero no corrige el sesgo de selección del corpus.

## 7. Para el coordinador

- **El "vocabulario numérico" no es una lista de números favoritos.** La distribución está dominada por la magnitud (números pequeños más frecuentes) y por el redondeo decimal: el 32,7 % de los valores de 2 dígitos termina en 0 (×3,3 sobre dígitos uniformes). Benford y log-uniforme se rechazan (p < 1e-300).
- **10, 12, 15, 20, 30, 40 y 50 no son especiales**: caen dentro de lo que predicen los márgenes de dígitos (10: 1,04×; 15: 1,06×; IC bootstrap incluye 1). Cualquier interpretación de "10 = décima", "15 = quincena", "40 = cuarenta" a partir de su frecuencia es un espejismo.
- **Solo 100, 200, 110, 47, 33 y 22 sobreviven** al nulo de dígitos, y de ellos los tres últimos están contaminados por copias. **100 es el hallazgo más sólido**: 2,05× [1,74; 2,41], presente en 104 quipus, sin papel de suma ni de etiqueta. Es compatible con una unidad de cuenta (pachaca) o con un atractor de redondeo; los datos no permiten distinguirlos.
- **La repetición es local, no global**: 1 007 excesos (valor, quipu) frente a 349 esperados (2,9×); 40/71 valores muestran clustering; el HHI por quipu es 0,168 vs 0,127 (p = 0,005). Ningún valor es ubicuo: la prevalencia observada es *menor* que la esperada por azar para todos (1: 365 vs 580; 10: 391 vs 473; 100: 104 vs 201). Cada quipu tiene su repertorio.
- **El "estándar de 15" de Incahuasi es un artefacto de copia.** El 15 es el 15,7 % de su década en Incahuasi (OR 2,04; p = 1,7e-07), pero al quitar UR267A/UR255 baja a 7,2 % (OR 0,85; p = 0,43). Lo mismo con el 47 (OR 6,89 → 1,87 al quitar UR275/UR266). No hay vocabulario del sitio.
- **Nada sobrevive por procedencia** (0/90 tras BH); Leymebamba es sugestivo (prevalencia alta de 1, 2, 3, 10, 11, 20, 22; OR 3,4–6,7) pero son 22 quipus y q = 0,12.
- **No hay código de color panandino.** 1-B y 3-B son significativos en agregado (1,17× y 1,28×) pero la dirección no es consistente entre quipus (signo +38/−36 y +35/−41); 30-KB y 47-YB dependen de pocos quipus. Como mucho, asociaciones locales débiles.
- **Único candidato a marcador: el 1** en la primera cuerda del grupo (755 vs 640; ×1,18; p = 0,001; sobrevive a excluir quipus dominados por unos). Ningún otro valor se comporta como etiqueta; 11–19, 22, 33, 47, 100 y 200 están *subrepresentados* en esa posición.
- **Recomendación next round:** (i) verificar en OKR los valores 100/200/1000 y su posición de nudo (¿un nudo simple mal situado?); (ii) auditar los pares HP055–UR1084, UR255–UR267A, UR266–UR275 antes de cualquier análisis de vocabulario; (iii) probar si 100 aparece en grupos con 10 cuerdas de 10 (pachaca) o en listas de precios/tributo como UR1109; (iv) no gastar más pruebas en 10/15/20/40/50: ya están explicados.
