# Nombrar las 9 partes: ¿qué unidades suman cada registro de UR278?

**Equipo:** DeepSeek · carpeta `analisis/ds/n_nueve_partes/`
**Fecha:** 18 de octubre de 2026
**Datos:** `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus), `analisis/13_sistema_incahuasi/ur270_ur278.csv`, `analisis/13_sistema_incahuasi/ur278_tabla.csv`, `analisis/ds/n_que_se_contaba/` (informe previo), literatura local (`docs/fichas/`, `analisis/fuentes_txt/`) y fuentes web (OpenAlex, Khipu Field Guide Blog, artículos de acceso abierto).
**Semilla:** 20261018. Scripts: `01_estructura.py`, `02_columnas.py`, `03_cribado9.py`; salidas en `salida_01.txt`, `salida_02.txt`, `salida_03.txt`.

---

## Pregunta

El informe `n_que_se_contaba` dejó una conclusión fuerte y una pregunta abierta. La conclusión: las 9 columnas de UR278 (Incahuasi, valle de Cañete) son **casi iguales** (CV entre medias de columna 0,18), lo que descarta edades, sexos, productos, meses y zonas ecológicas, y apunta a **9 partes administrativas**. La pregunta: **¿qué son esas 9 partes?** Y, alrededor de ella, tres preguntas auxiliares:

1. ¿Hay en la etnohistoria andina —y en particular en la costa central y sur (Cañete/Huarco, Lunahuaná, Chincha, Huarochirí, Yauyos)— divisiones en 9: ayllus, pachacas, parcialidades, guarangas?
2. ¿Qué estructura tienen las transcripciones coloniales de quipus contables (Jauja 1558–61, Sapallanga, Chucuito, *Textos Andinos* de Pärssinen y Kiviharju) y se parecen a UR278/UR266/UR275?
3. ¿Hay algún otro quipu o documento con 9 partes casi iguales, o con las cuotas 47, 17 y 208?

El objetivo no es adivinar: es **acotar** las identificaciones posibles, decir cuál es más compatible con los datos y qué observación las refutaría.

---

## Resumen de veredictos

| # | Hipótesis | Veredicto | Cifra clave | Nivel |
|---|---|---|---|---|
| 1 | Las 9 columnas son una **partición estable en 9 unidades** (no una taxonomía natural) | **compatible y reforzada** | CV entre columnas 0,193; las mismas 9 unidades en UR270 y UR278 (5 registros con 6–9/9 celdas y rho 0,95–1,00) | **demostrado** (estructura) |
| 2 | Las 9 partes son **9 pachacas/subunidades de una sola guaranga o flujo** | **la identificación más compatible** | 9 unidades de tamaño similar; pachacas/guarangas documentadas como similares entre sí; 9 pachacas en una guaranga está documentado | **propuesto** |
| 3 | Las 9 partes son **9 comunidades mitma/ayllu** de Cañete, o los 8 curacas de Lunahuaná + el principal | **posible pero no apoyada** | Lunahuaná: 4 guarangas × 2 curacas = 8 (+1 principal, si se cuenta aparte = 9); pero no hay lista de 9 mitmas | **especulativo** |
| 4 | Las 9 partes son **9 cuadrillas/turnos de mitayos o 9 chacras** que entregaban maní | **posible, no decidible** | 9 unidades casi iguales; cuota 47 compatible con ración/días; contexto de maní | **especulativo** |
| 5 | Las 9 partes son 9 productos, 9 meses, 9 zonas ecológicas o un 3×3 por posición | **descartada / no apoyada** | 3+3+3 por posición: R²=0,50, p=0,13; 4+5: p=0,22; ya descartadas por planitud | **demostrado (negativo)** para productos/meses; **no apoyado** para 3×3 |
| 6 | Las cuotas 10/15/17/46/47/208 son constantes panandinas | **descartada** | 17 solo en UR274B (2 tríos); 208 solo en UR268 (1 trío); 47 solo en UR275/269/266; fuera de Incahuasi, solo 10 en AS172 | **demostrado (negativo)** |
| 7 | Las cuotas son una **jerarquía de agregación** (componente → flujo → periodo) | **compatible** | 30+17=47; 15+10=25; 47+46+46+44+25=208 | **apoyado con datos** (heredado de 13_sistema) |

---

## 1. Método

- **Unidad de análisis = quipu.** Los contrastes de estructura se hacen por quipu; cuando se comparan grupos de 9 cuerdas se agrega por quipu o se permuta entre quipus.
- **Valores 0 sin nudos = ausentes** (NaN), nunca ceros.
- **Nulo explícito** en cada prueba; p empírico unilateral `(k+1)/(B+1)`; semilla fija 20261018.
- **Corrección múltiple** BH-FDR cuando se prueban muchas hipótesis; en los contrastes exploratorios se indica el número de pruebas y se lee el p con cautela. En concreto: las **4 particiones físicas** de §2.4 se corrigen con BH (q = 0,22–0,32; ninguna significativa); las **36 correlaciones entre columnas** de §2.3 son descriptivas y los pares positivos no sobreviven BH (los negativos son un artefacto de suma constante); el **contraste principal** (UR278 frente a 238 grupos de 9) es una sola prueba y no requiere corrección; Friedman y los nulos de §2.1 son pruebas únicas de estructura y se reportan sin corregir.
- **Reconstrucción de UR278:** 37 grupos de colgantes; 26 grupos de 9 cuerdas (24 con las 9 con valor), 4 de 10–12 y el resto de 1–6. La tabla principal usa las **24 filas estrictas** (54 601 unidades). Las columnas se numeran c1…c9 en el orden físico del quipu.
- **Dos medidas distintas de “variabilidad”** que el informe previo usa y conviene no confundir:
  - **CV entre medias de columna** (el 0,18 del informe previo): cuánto difieren las 9 medias. Es la medida de “¿son las 9 partes iguales?”.
  - **CV dentro de fila** (0,29): cuánto se dispersan las 9 cuerdas de un registro concreto. Es la medida de “¿cuánto varía un registro?”.
- **Fuentes:** fichas locales y grep de Urton (2017) y Medrano (2019); web para literatura no disponible en el repo. No leí el original de Pärssinen y Kiviharju (2004/2010): lo cito a través de Medrano (2019) y de sus fragmentos. Rostworowski, Dávila Brizeño y Espinoza Soriano se citan a través de resúmenes académicos o de la síntesis local; lo indico donde corresponde.

---

## 2. La estructura de las 9 partes

### 2.1 UR278: 24 registros completos, 9 columnas, 54 601 unidades

UR278 tiene 37 grupos con colgantes: **26 grupos de exactamente 9 cuerdas** (24 con las 9 cuerdas con valor y 2 con cuerdas vacías), 1 de 10, 3 de 12, 1 de 6, 3 de 2, 1 de 4 y 2 de 1; además hay 4 grupos sin colgantes de nivel 0. Los **24 registros completos** suman **54 601** unidades; el total de todos los grupos (incluidas las cuerdas 10–12 de los grupos rotos) es **68 403**. La diferencia con las 61 790 del informe previo es de **reconstrucción** (qué grupos y cuántas cuerdas se incluyen): con 26 filas de la tabla modal el CV es 0,187; con las 28 filas de ≥7 del informe previo, 0,184; con las 24 estrictas, **0,193**. Las tres cifras son la misma conclusión.

Perfil de las 9 columnas (porcentaje del registro, media de las 24 filas estrictas, IC95 bootstrap de filas):

| col | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
|---|---|---|---|---|---|---|---|---|---|
| % | 13,7 | 14,4 | 9,6 | 10,8 | 11,4 | 12,6 | 10,6 | 8,0 | 9,0 |
| IC95 | 12,8–14,6 | 13,1–15,5 | 8,7–10,5 | 10,1–11,5 | 10,5–12,5 | 11,7–13,6 | 9,4–11,9 | 7,0–9,0 | 8,2–9,6 |

- **CV entre medias de columna: 0,193, IC95 [0,152; 0,241]** (0,184 con las 28 filas del informe previo).
- **max/min de las medias: 1,80** (c2/c8).
- **CV dentro de fila: 0,275, IC95 [0,228; 0,322]** (0,290 con 28 filas).
- **Friedman:** χ² = 94,6, **p = 5,4·10⁻¹⁷** (24 filas; con 26 filas, χ² = 90,6). Hay efecto de columna real: las columnas no son intercambiables.
- **Concordancia de rango (Kendall W): 0,484** (χ² = 92,9). El orden de tamaño de las columnas se conserva moderadamente entre registros: c1/c2 arriba, c8/c9 abajo.
- **Nulo “columnas intercambiables”** (permutar las 9 celdas dentro de cada fila, 4 000 réplicas): CV entre medias **0,059 [0,033; 0,090]**, **p = 0,0002**. El efecto de columna no es ruido.
- **Nulo Dirichlet con el perfil observado** (α = 40, 2 000 réplicas): CV esperado **0,213 [0,150; 0,277]**, **p = 0,27** para “observado más plano”. La dispersión observada es exactamente la que produce un reparto aleatorio con esas medias; no hay nada “extra” que explicar.

**Lectura.** Las 9 partes son **similares pero no iguales**: las medias van de 8,0 % a 14,4 % (razón 1,80), no de 1 a 10. Es una partición de escala parecida, no una igualdad exacta. La diferencia entre columnas es real (Friedman, nulo de intercambio), pero pequeña frente a la variación dentro de cada columna.

### 2.2 Las 9 unidades son las mismas en UR270 y UR278

El hallazgo más importante de esta ronda no es el CV: es que **las 9 columnas tienen identidad estable**. UR270 es el quipu de detalle: cada grupo tiene 9 colgantes blancos (parte B) y 9 subsidiarias marrón (parte A). UR278 es el resumen: cada celda es colgante + subsidiaria de UR270, **columna a columna**. El emparejamiento ya establecido en `13_sistema_incahuasi` se confirma con correlaciones de perfil:

| UR270 grupo → UR278 grupo | celdas ±1 | rho de perfil |
|---|---|---|
| g0 → g21 | 9/9 | **+1,00** |
| g4 → g25 | 9/9 | **+1,00** |
| g5 → g26 | 7/9 | **+0,98** |
| g6 → g30 | 1/9 | +0,70 |
| g8 → g27 | 8/9 | **+0,95** |
| g9 → g28 | 6/9 | **+0,97** |
| g10 → g29 | 5/9 | +0,75 |
| g12 → g30 | 2/9 | +0,71 |
| g19, g22, g23, g24 (emparejamientos espurios) | 1/9 | +0,10 a +0,21 |

Los **cinco pares con correspondencia fuerte** (6–9 de 9 celdas ±1) tienen **rho 0,95–1,00**; los pares con solo 1–5 celdas coincidentes tienen rho 0,70–0,75 (débiles); los emparejamientos sin correspondencia tienen rho ≈ 0,1–0,2. Es decir: **la columna 1 de UR270 es la columna 1 de UR278, la 2 es la 2, etc., en el mismo orden**, al menos en los cinco registros que se pueden alinear con seguridad. Esto convierte “9 columnas” en “9 unidades contables con identidad fija”, no en 9 posiciones intercambiables.

**Control de estabilidad interna:** al partir las 24 filas en dos mitades (12 + 12), la correlación de rangos entre los perfiles de columna es **rho = 0,65, p = 0,058**. La identidad se conserva de forma sugerente, pero no alcanza el 5 % con esta muestra; los emparejamientos exactos con UR270 son la evidencia más fuerte.

**Control negativo:** el color no distingue las 9 unidades. En UR278 casi todos los registros son monocromos (AB, NB o W); en UR270 los 9 colgantes son W y las 9 subsidiarias NB. El color distingue **parte A de parte B**, no las 9 columnas. La identidad de las 9 unidades es **posicional**, no cromática.

**La estructura A/B.** Cada una de las 9 unidades tiene una **parte B** (colgante W) y una **parte A** (subsidiaria NB); A+B = celda de UR278. Las cuotas de los **dos quipus de componente** que consolidan A y B son **30 y 17** (suman 47), lo que sugiere **dos componentes o dos tasas por unidad**. Si A/B fueran mitades **hanan/hurin**, las 9 columnas serían 9 unidades cada una con dos mitades; los datos no lo demuestran, pero la aritmética 30+17=47 es compatible con ambas lecturas. Lo que sí es seguro: las 9 columnas son la **suma de dos partes**, no una sola cuerda.

### 2.3 Las cuotas de las 9 partes no son fijas

Si las 9 columnas fueran cuotas administrativas fijas (por ejemplo, “cada pachaca debe entregar el 11,1 %”), las proporciones serían constantes entre registros. No lo son:

- **CV intra-columna medio: 0,221.**
- **Ruido multinomial esperado** con las medias observadas y los totales de fila: **0,064**.
- **Razón Observado/Ruido = 3,5.**

Es decir, la proporción de cada unidad **varía casi cuatro veces más de lo que explicaría el muestreo**. Las 9 partes tienen un tamaño medio distinto y estable, pero **su aporte concreto cambia en cada registro**. Eso es compatible con unidades reales que producen/entregan cantidades variables (ayllus, chacras, cuadrillas), no con cuotas fijas.

Además, la proporción de algunas columnas depende del tamaño del registro: `log(c1/c7)` vs total, rho = −0,68 (p < 0,001); `log(c2/c7)` vs total, rho = −0,68 (p < 0,001). c7 pesa relativamente más en los registros pequeños; c1/c2 pesan más en los grandes. La explicación aburrida es que c7 tiene un **piso** (no baja de cierto valor) mientras las demás escalan. No es evidencia de nada semántico, pero sí de que las 9 partes no son un reparto proporcional rígido.

### 2.4 No hay un 4+5 ni un 3+3+3 por posición

El perfil ordenado por tamaño (14,0 · 13,5 · 12,9 · 11,6 · 10,7 · 10,7 · 9,7 · 8,9 · 8,0) parece dividirse en tres tercios. Es un artefacto de ordenar. Si se respeta el **orden físico** de las columnas (c1…c9) y se prueba la mejor partición contigua:

| partición física | R² | nulo (medias permutadas) | p |
|---|---|---|---|
| 2+3+4 | 0,613 | 0,251 (p95 0,655) | 0,079 |
| 3+3+3 | 0,495 | 0,251 (p95 0,651) | 0,132 |
| 4+5 | 0,199 | 0,125 (p95 0,456) | 0,222 |
| 5+4 | 0,230 | 0,125 (p95 0,456) | 0,183 |

**Ninguna partición por posición es significativa.** No hay evidencia de que las 9 columnas se agrupen en dos mitades (4+5), en tres tercios (3+3+3) o en dos bloques de 4 y 5. El “3×3” que sugiere el perfil ordenado no está en el orden del quipu. Esto es un **resultado negativo** importante: si las 9 partes fueran, por ejemplo, 3 sayas × 3 ayllus, esperaríamos que las columnas contiguas se parecieran más entre sí; no ocurre.

### 2.5 Control decisivo: UR278 es excepcionalmente plano frente a otros grupos de 9 cuerdas

*(Aquí uso el **CV dentro de grupo** —la dispersión de las 9 cuerdas de un registro—, no el CV entre medias de columna de 0,193 de §2.1.)*

El corpus tiene **238 grupos de exactamente 9 cuerdas en 97 quipus**. La media de CV dentro de grupo de UR278 es **0,275**; la mediana de los 238 grupos es **0,865**. Controlando por magnitud:

| conjunto | n | CV mediano | CV de UR278 | percentil de UR278 |
|---|---|---|---|---|
| todos los grupos de 9 | 238 | 0,865 | 0,275 | 9 % |
| total > 100 | 177 | 0,851 | 0,275 | 9 % |
| total > 500 | 89 | 0,863 | 0,275 | 16 % |
| total > 1 000 | 77 | 0,751 | 0,275 | 17 % |

- Solo **8 de 238** grupos de 9 tienen CV < 0,20; **7 son de UR278** y el otro es AS018 (un quipu de valores pequeños).
- **Nulo a nivel de quipu** (24 grupos de UR278 frente a 24 grupos al azar de los 238): CV medio del nulo **0,865 [0,677; 1,071]**, observado **0,275**, **p < 0,00005** (0/20 000).
- **Nulo emparejado por magnitud** (grupos con total 1 000–5 000, n = 62): CV medio **0,804**, observado **0,275** (n = 24), **p < 0,00005**.

**Lectura.** La planitud de UR278 no es un artefacto de valores pequeños ni de un grupo afortunado: es una propiedad del **quipu entero**. Entre los grupos de 9 cuerdas de magnitud comparable, UR278 es 3 veces más plano que la mediana. Eso es lo que se espera de una **partición administrativa deliberada**, no de una lista de categorías naturales.

**Matiz importante.** Entre las 11 tablas K=9 reconstruidas por el método modal, UR278 es la más plana (CVcol 0,193; la siguiente es UR270, su detalle, 0,313; luego 0,52, 0,57…). Pero con solo 11 tablas, ser el mínimo da p ≈ 1/11 = 0,09: **no es significativo por sí solo**. La significación viene del contraste con los 238 grupos de 9 (p < 0,00005), no del ranking de tablas.

### 2.6 UR266 y UR275: qué pasa con las 9 partes al consolidar

UR266 y UR275 no son tablas de 9 columnas. Son los quipus consolidados del mismo flujo:

| quipu | colgantes | grupos | tamaños de grupo | total | cuota |
|---|---|---|---|---|---|
| UR266 | 132 | 36 | 1–8 (moda 4) | 93 841 | 47 (2 tríos exactos; 17/26 registros según 13_sistema) |
| UR275 | 112 | 26 | 3–7 (moda 3–4) | 110 776 | 47 (9 tríos; 24/25 registros) |

- Los **totales de fila de UR278** son las **cabeceras de UR266/UR275**: 15 de 30 cabeceras de UR266 y 11 de 25 de UR275 coinciden (±1) con algún total de grupo de UR278; la alineación en orden da τ = 1 para 15 y 9 pares (13_sistema).
- UR266/UR275 añaden la **cuota 47** y las partidas de deducción; no repiten las 9 columnas. Es decir: **las 9 partes existen en el nivel de detalle (UR270/UR278) y desaparecen en el nivel consolidado**, donde solo queda el total del registro y su cuota.
- Eso es exactamente la estructura de una **cuenta jerárquica**: 9 unidades → 1 registro → 1 flujo. Las 9 partes no son 9 cuentas independientes; son la **descomposición de cada registro de una sola cuenta**.

---

## 3. Las cuotas 10, 15, 17, 46, 47 y 208: qué son y qué no son

### 3.1 Lo que muestra el archivo

Barrido de tríos exactos `x = c + n` en grupos de 3–4 cuerdas de todo el corpus (144 tríos en 61 quipus):

| cuota | quipus (tríos exactos) | lectura |
|---|---|---|
| 10 | UR267B (12), UR256 (7), AS172 (1) | componente de la pareja 15+10=25 |
| 15 | UR267A (15), UR255 (9) | componente de la pareja 15+10=25 |
| 17 | **UR274B (2)** | componente de la pareja 30+17=47 |
| 46 | UR269 (7) | flujo del bloque de 5 |
| 47 | UR275 (8), UR269 (4), UR266 (2) | flujo consolidado |
| 208 | **UR268 (1)** | periodo (suma de 5 flujos) |

- **17 no es una cuota “recurrente del archivo”**: aparece solo en UR274B (y una vez suelta en UR267B/UR273B, según 13_sistema). **208 aparece solo en UR268** (1 trío exacto; 19 de 29 registros según 13_sistema). **47 aparece solo en tres quipus del mismo flujo** (UR266, UR269, UR275). Fuera de Incahuasi, el único trío exacto con estas cuotas es **c = 10 en AS172**; no hay 15, 17, 46, 47 ni 208 fuera del archivo.
- Los valores 17, 47 y 208 **sí existen como cuerdas sueltas** en muchos quipus (351 cuerdas con 17 en 143 quipus; 135 con 47 en 55; 23 con 208 en 5), pero eso es otra cosa: son valores, no cuotas fijas de una cuenta.

### 3.2 La jerarquía de cuotas (heredada y confirmada)

`13_sistema_incahuasi` demostró que las cuotas se suman con la agregación:

- **30 (UR274A) + 17 (UR274B/UR273B) = 47** (UR266/UR275/UR269).
- **15 (UR267A/UR255) + 10 (UR267B/UR256) = 25** (UR269).
- **47 + 46 + 46 + 44 + 25 = 208** (UR268), con P ≈ 0,03 por azar (especulativo).

Es decir: **10/15/17/30 son cuotas de componente; 25/46/47 son cuotas de flujo; 208 es una cuota de periodo**. La recurrencia no es “panandina”: es **interna al archivo de Incahuasi** y sigue la jerarquía de consolidación. Esto encaja con la estructura de UR278: cada registro del flujo 47 se descompone en 9 unidades, y el flujo se consolida en 47.

### 3.3 ¿47, 17 o 208 en documentos coloniales?

No encontré ningún documento colonial con una cuota fija de 47, 17 o 208. Lo que sí aparecen son:

- **Cifras redondas** en las tasas y servicios: 400, 200, 150, 100, 50, 20, 10 (Chupachos, 1562; Chucuito, 1567).
- **Conteos de aldeas** pequeños y no redondos en los títulos de encomienda: 3, 9, 14, 17, 18, 21, 29, 37, 38, 53, 260 (Medrano 2019, cap. 2, citando Pärssinen y Kiviharju 2004, t. 2, 149). Allí **17 es la población de Callapa y 9 la de Pisquero**, no una cuota.
- **Precios y medidas**: 6 pesos por carga de chuño, 4 pesos por arroba de sebo, 500 cargas de chuño, 605 cameros (Medrano 2019, memoria 17).

**Conclusión negativa:** 47, 17 y 208 no son constantes coloniales conocidas; son **convenciones locales de Incahuasi**. La coincidencia con cifras coloniales es fácil y engañosa: 17 y 9 aparecen como poblaciones de aldeas en un título de encomienda, no como cuotas.

### 3.4 La unidad física: bultos, no productos individuales

El informe previo fijó la escala en **bultos de 10–50 kg** por la capacidad de Qolqawasi (6 400 m³; UR278 = 18–80 % de la capacidad con unidades de 25–50 kg; 0,0005–0,4 % con unidades individuales). La literatura de caravanas lo respalda:

- **Carga de llama:** 25–30 kg en viajes largos; 30–35 kg (3 arrobas) es el promedio citado; 50–60 kg en trayectos cortos (Lecoq 1987; Flores Ochoa 1995; Murra 1965; Museo Chileno de Arte Precolombino).
- **Carga humana:** 2 arrobas ≈ 23 kg como máximo legal (cédula de 1533, citada en el estudio sobre cargadores de Cuzco, 1538).

Si UR278 cuenta bultos de ~25 kg, sus 54 601 unidades son ~1 365 t; si cuenta cargas de 30 kg, ~1 638 t. Ambas caben en el depósito. Si contara personas, serían ~55 000 personas, una cifra difícil de sostener para un solo valle y un solo archivo; si contara días-persona, serían ~55 000 jornales, plausibles para una campaña de construcción. **La escala física no distingue bultos de jornales**; solo descarta unidades individuales de producto.

**Una coincidencia que no uso.** 9 × 208 = 1 872 y la mediana de fila es 2 097; 47 × 40 = 1 880. Son proximidades numéricas, no evidencia: hay muchas combinaciones posibles y la mediana no coincide exactamente. Lo anoto para que no se reintroduzca como “prueba”.

---

## 4. La literatura: ¿dónde aparece el 9 en el mundo andino?

### 4.1 Cañete, Huarco y Lunahuaná: la organización documentada no es de 9

La etnohistoria del valle de Cañete es bastante clara en los niveles altos y **no contiene un 9**:

- **Dos señoríos**: los **guarcos** en la parte baja (El Huarco–Cerro Azul) y los **lunahuanás** en la chaupiyunga (Zúñiga, Pacarán). La conquista inca fue violenta con los guarcos y pacífica con los lunahuanás; Incahuasi fue el "Nuevo Cusco" de la campaña (Rostworowski 1978–1980; 2025, *Boletín de Arqueología PUCP*).
- **Lunahuaná = 4 guarangas**, cada una gobernada por **dos curacas**: **8 curacas** en total; Rostworowski sugiere que cada guaranga se dividía en **urin/anán** (dos mitades), lo que explica los dos señores (Rostworowski 1978–1980: 190; síntesis en el artículo de 2024 sobre las poblaciones de Lunahuaná). Es la estructura más cercana a un 9: **8 curacas**, a los que las fuentes añaden un **cacique principal** (si se cuenta aparte, 9). Pero no es una división en 9 unidades coiguales; es 8 + 1 cabeza, y no está claro que el principal sea una unidad distinta.
- **Guarco**: un señorío; Garcilaso lo presenta como parte de una confederación multi-vallé con Chilca y Mala bajo Chuquimancu. No hay un número documentado de guarangas para Guarco.
- **Mitmas**: tras la conquista, Cañete recibió **mitmas de Coayllo, Chincha, la costa norte y Yauyos**. No hay una lista de 9 comunidades mitma; la cifra es abierta.
- **Los quipus de Incahuasi** aparecieron en el depósito Qolqawasi, asociados a **ají, maní y frijol negro** (Urton y Chu 2015). Es un archivo de depósito, no un archivo de poblados.

**Conclusión local:** en Cañete no hay una división en 9 ayllus, 9 pachacas o 9 guarangas documentada. Lo que hay es **2 señoríos, 4 guarangas y 8 curacas (+1 principal)**. Si las 9 columnas fueran unidades étnicas locales, tendrían que ser un nivel inferior (pachacas/ayllus) que las fuentes no detallan, o una creación administrativa inca.

### 4.2 Chincha, Huarochirí, Yauyos, Chucuito y Huánuco: el 9 tampoco está en los niveles altos

- **Chincha**: la relación de Castro–Ortega Morejón (1558) dice **30 000 tributarios y 30 caciques, cada uno con 1 000 indios** (es decir, 30 unidades tipo guaranga en el sentido decimal); 12 000 labradores, 10 000 pescadores, 6 000 mercaderes (Rostworowski 1970). No hay 9. La fama de Chincha es de **caravanas de llamas** y mercaderes, no de una partición en 9.
- **Huarochirí**: formaba parte de **Lorin Yauyos**; se documenta un **"Señor de las 7 Guarangas de Huarochirí"** (Rostworowski, citada en *La estratificación social y el hatun curaca en el mundo andino*). No hay 9.
- **Yauyos**: Dávila Brizeño (1586) describe la provincia partida en **Anan Yauyos y Lorin Yauyos**; reduce más de 200 pueblos a **39 reducciones**. No hay una división en 9.
- **Manuscrito de Huarochirí** (Ávila, ca. 1608): organiza las narrativas por **parcialidades (anan/hurin)** y por ayllus; no contiene una lista de 9 ayllus ni una partición en 9. Es una fuente de la organización dual, no de un 9.
- **Chucuito (1567)**: **7 pueblos/cabeceras** (Chucuito, Juli, Ilave, Acora, Pomata, Yunguyo, Zepita), cada uno con **hanansaya/hurinsaya**; dos quipocamayos generales y 14 marcamayos (2 por pueblo); clases tributarias **aymara** y **uru** con tasas distintas (Diez de San Miguel 1567/1964; Lucht 2004; Urton 2017). No hay 9: hay 7 × 2.
- **Huánuco (1562)**: los **chupachos** tienen **4 guarangas**, cada una con 2 caciques; las pachacas rondan los **50 aucacamayos**; el total es **1 203 tributarios** (Ortiz de Zúñiga 1567/1967; Chirinos 2024). No hay 9 guarangas ni 9 pachacas. **Pero** la declaración de los servicios al Inca (memoria 4 de *Textos Andinos*) enumera **9 partidas**: 400 indios para sembrar Cuzco, 150 yanaconas de Guayna Cápac, 150 para la guarda del cuerpo de Topa Inga, 10 para las armas, 200 para Chachapoyas, 200 para Quito, 20 para la guarda de Guayna Cápac, 120 para plumas, 60 para miel (Pärssinen y Kiviharju 2004, t. 1, 141; Medrano 2019, cap. 2). Son **9 categorías, pero muy desiguales (10–400)**, y son servicios, no una partición de la población. Es el único "9" en las visitas nombradas, y no se parece a UR278.

**Conclusión:** en la costa central y en las visitas de Chucuito, Huánuco y Yauyos **no hay una división en 9** de la población o del tributo. El 9 aparece una vez en Huánuco, como lista de 9 servicios desiguales.

### 4.3 Dónde sí hay 9: Cajamarca, Acos, Collaguas y los ceques

El 9 sí está documentado, pero en otros contextos:

- **Cajamarca**: la **waranka de Caxamarca** tenía **9 pachacas**; las siete warankas del reino de Cuismanco tenían 12, 10, 5, 8, **9**, 8 y los mitmas (Espinoza Soriano 1972, *El reino de Cuismanco*). Es el caso más claro de una **guaranga de 9 pachacas**.
- **Acos (Cusco)**: **3 ayllus y 9 sub-ayllus**; el sistema "ideal" de **9 pachacas** se repite en **Collaguas** (Zuidema, en *Quipu Y Tocapu*, fuente local, líneas 10170–10242). Es un **3 × 3**.
- **Cusco**: el sistema de **ceques** tiene **3 suyus con 9 ceques cada uno**, organizados en **3 grupos de 3**; el cuarto suyu, de rango inferior, tiene 14 (Zuidema, en *Quipu Y Tocapu*, línea 9552). Otra vez **3 × 3**.
- **Los ceques y los ayllus del Cusco**: cada mitad tiene **5 ayllus/panacas** (5 + 5 = 10), no 9. El 9 no es el patrón dual ordinario; es una **cuenta local** o un **3 × 3**.

**Regla estructural clave (Chirinos 2024; 2026):** los **ayllus** tienen tamaños muy variables (a menudo < 50 aucacamayos); las **pachacas, pisca-pachacas y guarangas**, aunque también variables, **se caracterizan por tener cantidades similares entre sí**. Los Chupachos de 1549 tenían pachacas de ~50, agrupaciones intermedias de 100–200, y dos pares de guarangas de 580 y 553; total 1 203. Las unidades mayores se componen de **2 a 7 entidades**; no se conocen 20 pachacas o 14 guarangas sin partes intermedias. **El 9 es un número posible de pachacas de una guaranga, no un número canónico del sistema decimal.**

### 4.4 El sistema decimal inca y la carga de llama

- **Unidades canónicas**: chunka (10), pachaka (100), pisca-pachaka (500), waranqa/guaranga (1 000), hunu (10 000). El **9 no es una unidad decimal**; es un **conteo local** dentro de una guaranga (Cajamarca) o un **3 × 3** (Acos, ceques).
- **En la práctica, las guarangas no tienen 10 pachacas**: las de Cajamarca tienen 5–12; las de los Chupachos, 4 guarangas con pachacas de ~50 y 1 203 tributarios, muy por debajo de los 4 000 teóricos. La terminología decimal es **jerárquica y aproximada**, no aritmética (Murra 2002: 216–217; Zuloaga 2012: 45; Chirinos 2024).
- **Carga de llama**: 25–30 kg en viajes largos; 30–35 kg (3 arrobas) como promedio; 50–60 kg en trayectos cortos (Lecoq 1987; Flores Ochoa 1995; Murra 1965; Museo Chileno de Arte Precolombino). La **carga humana** legal era de 2 arrobas ≈ 23 kg (cédula de 1533). Es la escala que el informe previo fijó para UR278: **bultos de 10–50 kg**, no productos individuales.

**Conclusión de la sección 4:** el 9 no es un número panandino ni una unidad decimal. Es un **conteo local documentado** en guarangas del norte (Cajamarca) y en estructuras 3 × 3 del Cusco (Acos, Collaguas, ceques). En la costa central no hay un 9 étnico documentado. Por tanto, si las 9 columnas son unidades sociales, lo más probable es que sean **pachacas/subunidades de una guaranga**, no ayllus ni guarangas completas: las pachacas son las que se parecen entre sí, y 9 pachacas por guaranga está documentado.

---

## 5. Las transcripciones coloniales de quipus: ¿qué estructura tienen?

### 5.1 El corpus

El corpus de referencia es **Pärssinen y Kiviharju, *Textos andinos* (2004, 2010)**: 880 páginas, 43 agrupaciones documentales, **72 memorias** (transcripciones de quipus) entre 1535 y 1653; la mayoría anteriores a la visita toledana de 1569. Medrano (2019) las clasifica en **29 primarias numéricas, 32 *summary*, 3 narrativas y 8 *elicited***; 69/72 contienen información numérica. Limitaciones: miden la **traducción al español**, no la narración andina; los datos XML no estaban públicos al depositarse; y las cifras pueden tener errores de conversión de unidades andinas a castellanas (Medrano 2019, cap. 2; Urton 2017, cap. 10).

### 5.2 Estructuras que aparecen

| documento | categorías | ¿columnas iguales? | ¿cuotas fijas? | ¿totales encadenados? |
|---|---|---|---|---|
| **Chupachos, servicios al Inca (1549/1562)** | **9 servicios** (400, 150, 150, 10, 200, 200, 20, 120, 60) | no; 10–400 | no | no (lista de servicios) |
| **Chucuito (1567)** | 7 pueblos × 2 parcialidades; clases aymara/uru | no | tasas por clase | recuentos por quipu, no un total único |
| **Jauja (crónicas, 1558–61)** | niveles: quipus descriptivos → **quipus "executive summary"** | — | — | **sí**: resumen que condensa los descriptivos |
| **Charka / Montemayor (1548–51)** | bienes (chuño, cameros, sebo), cantidades y precios | no | precios (6 pesos/carga; 4 pesos/arroba) | **sí**: distinciones finas sumadas para la presentación |
| **Título de encomienda (1540)** | ~12 aldeas (3, 9, 14, 17, 18, 21, 29, 37, 38, 53, 260…) | no; 3–260 | no | **sí**: suma a 823 |
| **Catarata (quipus arqueológicos)** | grupos de 3 cuerdas (W, RL, AB); 14–18 grupos; partes y subpartes | no; las 3 cuerdas son bienes/servicios distintos | no | **sí**: sumas entre quipus y proporciones |

**Lo que muestran:**

1. **Los totales encadenados son normales.** Jauja tiene quipus "executive summary" que condensan quipus descriptivos; Charka suma distinciones finas; el título de encomienda suma aldeas a un total. Esto es exactamente el patrón UR278 (detalle) → UR266/UR275 (resumen), y apoya la lectura jerárquica del archivo de Incahuasi (Medrano 2019, cap. 2; 13_sistema).
2. **Las categorías de una cuenta no son iguales.** En Chupachos van de 10 a 400; en el título de encomienda, de 3 a 260. La igualdad de las 9 columnas de UR278 es **rara** en el corpus transcrito.
3. **No hay una transcripción con 9 partes iguales.** El único 9 es la lista de servicios de Chupachos, y es desigual. **No encontré** una cuenta colonial con 9 columnas de magnitud similar, ni con cuotas 47/17/208.
4. **Las proporciones se usan para identificar partes.** En los quipus Catarata, Chirinos (2026) identifica partes y subpartes por **proporciones aproximadas** entre grupos, y las interpreta como pachacas/guarangas/hunus. Es el mejor análogo arqueológico de "unidades similares que se agregan en niveles": las pachacas/guarangas se parecen entre sí y se suman en entidades mayores. Pero los grupos de Catarata son de **3 cuerdas** (tres bienes/servicios), no de 9 columnas iguales.
5. **Sapallanga y Jauja (1558–61)**: no encontré en el repo una transcripción primaria de las cuentas de Jauja/Hatun Xauxa ni de Sapallanga. La referencia de **Murra (1975)** se cita en la literatura como el análisis de las visitas y de la organización decimal, pero no tengo el texto; lo dejo como **no verificado**. Lo que sí está documentado (Medrano 2019, cap. 2) es que las crónicas de Jauja describen **quipus "executive summary"** que condensan quipus descriptivos: es el paralelo estructural de UR278→UR266/275, no una cuenta de 9 partes iguales.

### 5.3 Comparación cuantitativa

| | UR278 | UR266 | UR275 | Chupachos 1562 | Título 1540 |
|---|---|---|---|---|---|
| columnas por registro | **9** | 1–8 (moda 4) | 3–7 (moda 3–4) | 9 servicios | ~12 aldeas |
| CV entre columnas | **0,19** | — | — | alto (10–400) | alto (3–260) |
| cuota fija | **47** | 47 | 47 | no | no |
| total | 54 601 (24 filas) | 93 841 | 110 776 | 4 guarangas, 1 203 tributarios | 823 |
| totales encadenados | **sí** (UR278→266/275) | sí (cabeceras) | sí (cabeceras) | no | sí |

**Conclusión:** las transcripciones coloniales **no dan el nombre** de las 9 partes, pero sí dan el **marco**: cuentas jerárquicas, con totales encadenados y categorías desiguales. La igualdad de las 9 columnas de UR278 no tiene paralelo en el corpus transcrito; es una **decisión local de formato**, no una convención panandina.

---

## 6. Tres identificaciones concretas (y una descartada)

### H1. Las 9 partes son 9 pachacas (o subunidades equivalentes) de una sola guaranga/flujo — **propuesto**

**Qué predice.** Una guaranga se descompone en pachacas de tamaño similar; cada pachaca aporta una cantidad al registro; el total del registro es la suma de las 9; la cuota 47 es la deducción del flujo. Las 9 pachacas se repiten en cada registro y en el quipu de detalle (UR270), en el mismo orden.

**Qué la apoya.**
- Las 9 columnas son **similares pero no iguales** (CV 0,19; max/min 1,80): exactamente el patrón de pachacas/guarangas "de cantidades similares", no el de ayllus (muy variables) ni el de una taxonomía natural (productos, edades, meses).
- Las 9 unidades son **las mismas** en UR270 y UR278 (5 registros con 6–9/9 celdas y rho 0,95–1,00; 2 más con rho 0,70–0,75), y su orden de tamaño se conserva (Kendall W 0,43). Es una partición administrativa estable.
- **9 pachacas por guaranga está documentado** en Cajamarca (Espinoza Soriano 1972); el 9 no es canónico, pero está dentro del rango real (5–12).
- La estructura **detalle → resumen** (UR278 → UR266/275) es la de una cuenta jerárquica, con el flujo 47 como nivel superior.
- El contexto de depósito (maní) y la escala de bultos (10–50 kg) son compatibles con un tributo de pachacas.

**Qué la debilita.**
- **No hay un documento de Cañete que liste 9 pachacas.** Lunahuaná tiene 4 guarangas × 2 curacas = 8 (+1 principal); Guarco no tiene un número documentado; Huarochirí tiene 7 guarangas; Chincha, 30.
- Las 9 columnas podrían ser **8 + 1** (los 8 curacas + el principal) más que 9 pachacas.
- Los valores podrían ser **bultos** (no tributarios), en cuyo caso "pachaca" es una analogía estructural, no una identidad demográfica.

**Qué la refutaría.** Una lista colonial de las pachacas de Lunahuaná/Guarco con un número distinto de 9; o que las 9 columnas no correspondan a las pachacas conocidas; o que el mismo formato de 9 columnas aparezca en cuentas de **productos distintos** con identidades distintas (señal de que son campos/cuadrillas, no pachacas). **Nivel: propuesto** (la estructura está apoyada; el nombre, no).

### H2. Las 9 partes son 9 comunidades mitma/ayllu de Cañete, o los 8 curacas de Lunahuaná + el principal — **especulativo**

**Qué predice.** Cada columna es una comunidad o un curaca; las 9 se repiten porque son las unidades políticas del valle; sus tamaños son parecidos porque el Inca las niveló; el registro es el tributo de cada una.

**Qué la apoya.**
- Cañete recibió **mitmas de Coayllo, Chincha, la costa norte y Yauyos**; es un valle multiétnico, y el Inca pudo crear 9 unidades.
- Lunahuaná tenía **8 curacas** (4 guarangas × 2) y las fuentes mencionan un **cacique principal**; si se cuenta aparte, **9**. Es la coincidencia local más sugerente, pero el principal puede ser uno de los 8.
- Las 9 unidades son estables y de escala similar, como comunidades niveladas.

**Qué la debilita.**
- **No hay lista de 9 mitmas**; el número es abierto.
- Si fueran 8 curacas + principal, esperaríamos que la unidad del principal fuera **mayor**; las 9 columnas son casi iguales (c2/c8 = 1,80), sin una cabeza dominante.
- Las comunidades mitma de orígenes distintos tenderían a tamaños más dispares que 0,19 de CV.
- El orden de las columnas no coincide con un orden geográfico conocido.

**Qué la refutaría.** Una lista de mitmas de Cañete con un número distinto de 9; o evidencia isotópica/estilística de más/menos grupos; o que las 9 columnas no correspondan a unidades territoriales. **Nivel: especulativo.**

### H3. Las 9 partes son 9 cuadrillas/turnos de mitayos o 9 chacras que entregaban maní — **especulativo**

**Qué predice.** Cada columna es un grupo de trabajo o una parcela; el valor es lo que entregó en el turno; la cuota 47 es la ración/días reservados; el registro es un turno de entrega.

**Qué la apoya.**
- El contexto es un **depósito de maní**; los quipus estaban bajo maní (Urton y Chu 2015).
- Las 9 unidades son casi iguales y sus aportes varían registro a registro (CV intra-columna 0,25), como cuadrillas o parcelas.
- La cuota 47 y la cuota 208 podrían leerse como **días** (47 ≈ mes y medio; 208 ≈ 7 meses), y 30+17=47, 15+10=25 encajan con medios meses; pero es numerología sin prueba.
- 9 cuadrillas/parcelas es una organización operativa plausible en un depósito.

**Qué la debilita.**
- **No hay documento de 9 cuadrillas ni 9 chacras** en Incahuasi/Cañete.
- Los valores son grandes (~2 000 por registro) y la escala física favorece **bultos**, no jornales; si fueran jornales, 54 601 jornales son plausibles, pero no hay evidencia independiente.
- Las 9 unidades se repiten **en el mismo orden** en todos los registros; unas cuadrillas/parcelas podrían hacerlo, pero es más propio de una lista administrativa fija.
- La cuota 47 no tiene por qué ser temporal: 13_sistema la explica como **suma de componentes** (30+17), no como días.

**Qué la refutaría.** Valores que sean claramente bultos (no persona-días); ausencia de 9 cuadrillas/chacras en la etnohistoria; o que las 9 columnas correspondan a unidades geográficas conocidas. **Nivel: especulativo.**

### H4. Las 9 partes son 9 productos, 9 meses, 9 zonas ecológicas o un 3×3 por posición — **descartada / no apoyada**

- **9 productos, 9 meses, 9 zonas**: la planitud (CV 0,19) las descarta; las categorías naturales tendrían dominantes. Ya estaba en `n_que_se_contaba`.
- **3×3 por posición**: la partición física 3+3+3 tiene R²=0,50 y **p=0,13**; la 4+5, p=0,22. No hay evidencia de que las columnas contiguas formen tercios o mitades. El "3×3" del perfil ordenado es un artefacto de ordenar por tamaño.
- **9 colores**: no; los registros son monocromos y el color distingue A/B, no las 9 columnas.
- **9 cuerdas de un mismo grupo**: es un formato que aparece en 238 grupos de 97 quipus, pero solo UR278/UR270 lo usan como **ancho regular de registro**; no es una convención panandina.

**Nivel: demostrado (negativo) para productos/meses/zonas; no apoyado para 3×3.**

---

## 7. Resultados negativos (los que también cuentan)

1. **No hay un documento colonial con 9 partes iguales.** El único 9 en las visitas nombradas es la lista de 9 servicios de los Chupachos, con valores 10–400.
2. **No hay un documento colonial con cuotas 47, 17 o 208.** Son convenciones locales de Incahuasi; 17 y 9 aparecen en un título de encomienda como **poblaciones de aldeas** (Callapa 17, Pisquero 9), no como cuotas.
3. **Las cuotas no son panandinas.** Fuera de Incahuasi, el único trío exacto con estas constantes es c = 10 en AS172. 47 solo en UR266/269/275; 17 solo en UR274B; 208 solo en UR268.
4. **No hay un 4+5 ni un 3+3+3 por posición.** Las particiones físicas no son significativas (p = 0,08–0,22; q BH = 0,22–0,32).
5. **Las 9 partes no son cuotas fijas.** La proporción de cada columna varía 3,5 veces más de lo que explica el muestreo; solo el tamaño medio y el orden son estables.
6. **No hay otras tablas K=9 comparables.** Solo 11 tablas K=9 en el corpus; UR278 es la más plana, pero con 11 tablas el ranking da p ≈ 0,09. La significación viene del contraste con 238 grupos de 9 (p < 0,00005), no del ranking.
7. **No se puede distinguir bultos de jornales con la escala física.** La arqueología de depósitos descarta productos individuales, pero no separa 25 kg de 1 jornada.
8. **No se puede decidir si A/B son mitades hanan/hurin o dos componentes/tasas.** La aritmética 30+17=47 es compatible con ambas; haría falta una fuente externa.

---

## 8. Límites y supuestos

1. **La reconstrucción de UR278** usa 24 filas estrictas de 9 columnas (26 en la tabla modal, que incluye 2 filas parciales); las filas rotas (7–8 cuerdas) y los grupos de 10–12 se excluyen de la tabla principal. Los totales pueden variar ±10 % según el criterio; el CV entre columnas es robusto (0,184–0,193).
2. **El corpus KFG tiene errores de lectura** y valores 0 sin nudos; usé la regla del brief (0 sin nudos = ausente). No corregí cuerdas rotas.
3. **La comparación con 238 grupos de 9** incluye grupos de valores pequeños y de otras procedencias; el nulo emparejado por magnitud (1 000–5 000) controla lo principal, pero no la procedencia ni el tipo de quipu.
4. **La etnohistoria de Cañete es fragmentaria**: Rostworowski reconstruye dos señoríos y 4 guarangas, pero no hay una lista de pachacas. La ausencia de un 9 documentado no prueba que no existiera; solo prueba que no lo tenemos.
5. **Las fuentes web y las síntesis** (Chirinos 2026, artículos de 2024–2025, resúmenes de Rostworowski/Espinoza) no sustituyen a los originales; las cito como contexto, no como prueba documental.
6. **No leí Pärssinen y Kiviharju (2004/2010)**; las citas de memorias provienen de Medrano (2019), que transcribe y traduce los fragmentos.
7. **La interpretación “pachaca”** es estructural: las pachacas/guarangas se parecen entre sí y 9 está documentado, pero no tengo los nombres de las 9 unidades.

---

## 9. Para el coordinador

- **La estructura de las 9 partes está demostrada, el nombre no.** UR278 tiene 24 registros completos de 9 columnas; las 9 son casi iguales (CV entre medias 0,193, IC95 [0,152; 0,241]; max/min 1,80) y **las mismas 9 unidades, en el mismo orden, aparecen en UR270 y UR278** (5 registros con 6–9/9 celdas ±1 y rho 0,95–1,00). No son 9 posiciones intercambiables: son 9 unidades contables con identidad fija.
- **La planitud es excepcional, no un artefacto.** Frente a 238 grupos de 9 cuerdas del corpus, la media de CV de UR278 es 0,275 vs 0,865 del nulo (p < 0,00005); el nulo emparejado por magnitud (total 1 000–5 000) da 0,804 vs 0,275 (p < 0,00005). Solo 8 de 238 grupos de 9 tienen CV < 0,20, y 7 son de UR278.
- **Las 9 partes no son cuotas fijas.** La proporción de cada columna varía 3,5 veces más de lo que explica el muestreo; el tamaño medio y el orden son estables, pero el aporte de cada unidad cambia en cada registro. Eso es propio de unidades reales (pachacas, chacras, cuadrillas), no de un reparto porcentual rígido.
- **No hay un 9 local documentado en Cañete.** Lunahuaná = 4 guarangas × 2 curacas = 8 (+1 principal); Guarco = 1 señorío; Huarochirí = 7 guarangas; Chincha = 30 caciques de 1 000; Yauyos = 2 mitades; Chucuito = 7 pueblos × 2; Huánuco = 4 guarangas. El 9 aparece en **Cajamarca (9 pachacas)**, **Acos (3 ayllus × 3)**, **Collaguas (9 pachacas)** y los **ceques (3 × 3)**. La regla útil: las **pachacas/guarangas se parecen entre sí**; los ayllus, no.
- **La identificación más compatible es “9 pachacas/subunidades de una sola guaranga o flujo”** (propuesto, no demostrado). Encaja con la escala similar, la identidad estable, la jerarquía detalle→resumen y el 9 documentado en guarangas del norte. La debilidad es que no hay una lista de 9 pachacas para Cañete.
- **Las alternativas son especulativas:** 9 comunidades mitma/ayllu, o los 8 curacas de Lunahuaná + el principal; 9 cuadrillas/turnos o 9 chacras de maní. Ninguna tiene documento local que la sostenga, y la segunda choca con que las 9 columnas son casi iguales (una cabeza debería ser mayor).
- **Las cuotas 47/17/208 no son panandinas.** 17 solo en UR274B (2 tríos); 208 solo en UR268 (1 trío); 47 solo en UR266/269/275. Fuera de Incahuasi, solo c=10 en AS172. Son una **jerarquía de agregación** (30+17=47; 15+10=25; 47+46+46+44+25=208), no constantes coloniales. En los documentos, 17 y 9 aparecen como **poblaciones de aldeas**, no como cuotas.
- **No hay transcripción colonial con 9 partes iguales.** El único 9 es la lista de 9 servicios de los Chupachos (400, 150, 150, 10, 200, 200, 20, 120, 60), desigual. Lo que sí hay es **jerarquía de totales** (Jauja: quipus "executive summary"; Charka: sumas de distinciones finas; encomienda: 823), que es el mejor paralelo de UR278→UR266/275.
- **Prueba decisiva para la próxima ronda:** buscar una lista colonial de las **pachacas de Lunahuaná/Guarco** (o de las mitmas de Cañete) y comparar nombres/número con las 9 columnas; y buscar otro quipu de Incahuasi de **ají o frijol** con 9 columnas para ver si las 9 unidades son genéricas (pachacas) o específicas del flujo 47. Si aparecen las mismas 9, H1 gana; si no, H3/H2.
- **No gastar más tiempo en:** 9 productos/meses/zonas, 3×3 por posición, o cuotas panandinas. Están descartados o no apoyados con los datos actuales.

---

## Fuentes

**Locales (repo):**
- `analisis/ds/n_que_se_contaba/informe.md` y scripts (demografía, unidades, depósitos, dígitos).
- `analisis/13_sistema_incahuasi/informe.md`, `ur270_ur278.csv`, `salida_07_ur270_ur278.txt` (cuotas, parejas, UR270↔UR278).
- `analisis/09_incahuasi/informe.md`, `analisis/01_aritmetica/informe.md`, `analisis/04_concordancias/informe.md`.
- `docs/fichas/2015-Urton_inkawasi.md`, `2017-Urton-inka-history-knots.md`, `2019-Medrano_khipu-transcription-insistence.md`, `2019-Clindaniel_grammar-inka-khipu.md`.
- `analisis/fuentes_txt/InkaHistoryinKnotsReadingKhipusas.txt` (Urton 2017), `MEDRANO-SENIORTHESIS-2019.txt`, `QuipuYTocapu.txt` (Zuidema sobre Acos/Collaguas/ceques).

**Citadas (vía local o web):**
- Chirinos Rivera, A. (2024). *Organización político-territorial en el Perú central del siglo XVI…* Tesis doctoral, UNED. Resumen y blog: “El conjunto de quipus ‘Catarata’…”, Khipu Field Guide Blog, 5 feb. 2026.
- Diez de San Miguel, G. (1567/1964). *Visita hecha a la provincia de Chucuito*. Lima: Casa de la Cultura del Perú.
- Dávila Brizeño, D. (1586). *Descripción de la provincia de Yauyos* (en Jiménez de la Espada, *Relaciones geográficas de Indias*).
- Espinoza Soriano, W. (1972). “El reino de Cuismanco”. *Revista de Arqueología y Sociedad* 7–8. (Lista de warankas y pachacas de Cajamarca.)
- Lecoq, P. (1987); Flores Ochoa, J. (1995); Murra, J. (1965). Cargas de llama (citados en la síntesis de Lecoq y en el Museo Chileno de Arte Precolombino).
- Lucht, R. (2004). “Una nueva lectura de la Visita a Chucuito (1567)”. *Indiana* 21: 175–194.
- Medrano, M. (2019). *Toward a Khipu Transcription “Insistence”…* Tesis, Harvard College.
- Murra, J. (1975/2002). *Formaciones económicas y políticas del mundo andino*; *El mundo andino*.
- Ortiz de Zúñiga, I. (1562/1967). *Visita de la provincia de León de Huánuco*. Ed. J. V. Murra. Huánuco: UNHEVAL.
- Pärssinen, M. y Kiviharju, J. (2004, 2010). *Textos andinos: Corpus de textos khipu incaicos y coloniales*, ts. 1–2. Madrid: Instituto Iberoamericano de Finlandia / UCM.
- Rostworowski, M. (1970). “Mercaderes del valle de Chincha…”. *Revista Española de Antropología Americana* 5.
- Rostworowski, M. (1978–1980). “Guarco y Lunahuaná: dos señoríos prehispánicos de la costa surcentral del Perú”. *Revista del Museo Nacional* 44.
- Rostworowski, M. (1988/1999). *Historia del Tahuantinsuyu*; *Costa peruana prehispánica*.
- Urton, G. (2017). *Inka History in Knots*. Austin: University of Texas Press.
- Urton, G. y Chu, A. (2015). “Accounting in the King’s Storehouse: the Inkawasi Khipu Archive”. *Latin American Antiquity* 26(4): 512–529.
- Zuidema, R. T. (1964/1995). *The Ceque System of Cusco*; capítulos en *Quipu Y Tocapu* (Acos, Collaguas, ceques).
- Artículos de 2024–2025 sobre Lunahuaná: “El estudio de las poblaciones indígenas de Lunahuaná en la doctrina de Cañete, siglos XVI–XVIII”, DOI 10.70748/nm.13.2024.330; “Construyendo un imperio: la ocupación inca en Lunahuaná…”, DOI 10.18800/boletindearqueologiapucp.202501.006.

**Nota:** las citas de Pärssinen y Kiviharju provienen de Medrano (2019); las de Rostworowski, Dávila Brizeño y Espinoza Soriano, de resúmenes académicos y de la síntesis local, no de los originales. Las cifras de quipus son de `analisis/datos/cuerdas.csv` (KFG) y de los scripts de esta carpeta.
