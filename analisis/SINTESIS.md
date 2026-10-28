> Bitácora de trabajo del proyecto: es el diario de trabajo, en orden cronológico, y se publica para trazabilidad. Ante cualquier diferencia prevalecen los informes de cada carpeta y `paquete_revision/`. Las entradas que una sección posterior corrigió o retiró llevan al final la nota *(corregido después: ver «…»)*.

# Bitácora del coordinador

Resumen de cada informe a medida que llega. Detalle en `analisis/<carpeta>/informe.md`.

## Datos

- `analisis/datos/` (KFG aplanado): valor = suma de aportes de los nudos en 57 789/57 818 cuerdas. 30,5 % de cuerdas sin nudos. La columna `alt` está vacía en todo el corpus.

## Ronda 1

### 06 Nudos (Sonnet)
- Violaciones decimales estructuradas existen pero se concentran en pocos quipus (93/641 con estructura relevante). "Nudo inferior" (L/E con racimo debajo) en 7,5 % de cuerdas y 43,7 % de quipus; no depende de la fuente ni de la rotura (cuerdas con nudo inferior están *menos* rotas, p=0,0005).
- Etiquetas de Saez-Rodríguez: **negativo** (exceso del primer colgante = orden decreciente del grupo; desaparece con control).
- Dirección S/Z: la mezcla en una cuerda es diferencia entre tipos de nudo (96 %); sin asociación con posición, R/V ni color. **Positivo**: bloques contiguos de dirección en 23 quipus (p. ej. UR1084: 5 Z y luego 88 S) → cambio de registrador o quipu compuesto (aburrido) vs. mitades (propuesto).
- Candidatos no decimales: UR050–UR055 (+UR039, UR110, UR112, UR144): series de largos de 4–9 vueltas sin patrón decimal. UR178/179 (Cajamarquilla): conteo unario. Incahuasi (UR278, UR272, UR267A, UR255, UR270): patrón S..L;E.
- Artefactos a excluir: UR211, AS090_N2, AS019, AS004. L con ≥10 vueltas = artefacto de transcripción (n codifica el valor).
- Seguimiento lanzado: `07_series_largos` (Opus).
- Pendiente: asignación de tipo por posición (Ascher) vs por tipo (Urton) puede crear/ocultar nudos inferiores → contrastar con OKR `knot`.

### 02 Color (Sonnet)
- Tres usos del color en subconjuntos distintos (bloque y columna tienden a excluirse):
  - **Columna** (color fijo por posición en el grupo = encabezado de columna): 12 % estricto – 47 % laxo de 376 quipus (bien apoyado en quipus concretos: AS170, UR1144, UR1113, UR267A).
  - **Bloque** (grupos monocromos = categoría por grupo): 41 %. Bandas ~48 %, periodicidad ~29 %.
- Color ↔ valor dentro del quipu: 24–40 % de quipus, efecto pequeño (ε² 0,07), dirección NO común entre quipus → códigos locales, no un vocabulario de color panandino.
- Único "vocabulario" compartido: blanco/claro ↔ valores algo mayores, primera cuerda del grupo y cuerdas-suma de borde (54 % vs 36–40 % esperado, p=0,001). KB ↔ cuerda sin nudos (dominado por UR, ¿artefacto?).
- Negativos: mezclas ≠ totales; color raro no marca nada; teñidos (≤10 % de cuerdas) sin vocabulario. RL es marrón natural, no rojo.
- Sumas: 118 bordes de grupo = suma del resto (azar ~37); 72 colgante = suma de subsidiarias (azar ~45).

### 01 Aritmética (Sonnet)
- **El 74 % de Medrano y Khosla no se distingue del azar**: detector laxo 75,3 % observado vs 73,5 % esperado bajo nulo que baraja dentro de nivel. Adyacentes: 55,9 vs 52,5 %. Tras control, solo 13–21 quipus (2–3 %) con contabilidad interna significativa; estimación corregida por potencia 5–10 % con sumas exactas locales. Afirmación fuerte → auditar.
- **Bien apoyado**: cuerda superior = suma de grupos adyacentes (22/63 vs 0,6 esperado; AS006, AS007, QU009, QU016, AS001, QU015).
- **Bien apoyado (regularidad)**: Incahuasi, grupos de 3 cuerdas `[x, c, x−c]` con c constante por quipu (15 en UR255/UR267A, 10 en UR256/UR267B); 8 de 9 quipus significativos son de Incahuasi. Cuota/tara/deducción (propuesto) — conecta con el "15" de Urton y Chu 2015.
- Negativos: relaciones grupo-grupo, proporciones 1/10 (tributo) y demás razones; Benford no diagnostica. Exceso de razón 1/1 (duplicados de cantidades).
- Dígito de unidades 0 ×2,65 pero 5 no → no hay redondeo; valores-cuota (10, 20, 100). 71/434 quipus repiten valores más de lo esperable (22 esperados): 1, 10, 20, 2, 4, 100.
- Tipología débil (continuo): «códigos» (200, valores pequeños repetidos, ninguno con aritmética verificada; Huaquerones 10/12), «jerárquicos» (139), «cuerda superior» (16), «conteo/medida» (181).

### 05 Etnohistoria (Sonnet)
- **Calendario: negativo** (111 pruebas, 5 con p<0,05 vs 5,6 esperadas, nada sobrevive a Holm/BH). Ningún quipu con 328/354/360/365/730 colgantes ni 41 grupos. UR006: 24 grupos regulares pero de 20–22 colgantes, 571 colgantes (Urton: 762); la lectura calendárica no se reproduce con KFG/OKR → sigue «propuesta» como mucho. *(corregido después: ver «12 Urton 2017 (Sonnet) — lecturas frente a KFG»)*
- **Santa: el ajuste publicado no es excepcional.** Reconstruidos 133 grupos de seis (48/9/34/17/15/10, = publicado). Error mínimo 3 se alcanza por azar con p 0,36–0,94 según nulo; los p publicados suponen independencia de 133 grupos y no corrigen «el mejor de 20». Hanan/hurin = especulativo. Suma de primeras cuerdas 367–369 (objetivo de la revisita 367): p 0,005–0,018 pero post hoc → apoyo débil. Fuente: preprint OSF sr8kw de FitzPatrick (CC-BY).
- Fuentes coloniales (11 categorías, 55 pruebas): sobrevive **segregación espacial R/V** (74/100 quipus vs 5,6) — probablemente manufactura por secciones; S/Z segregada en 6/9; series crecientes en HP021 y MM006_AN001. Negativos: totales decimales, grupos de 10, clases de edad decrecientes, razones.
- Pares con 6 colgantes idénticos de misma procedencia (exploratorio): AS159/AS173, JC009/JC013, UR066/UR067, AS125/UR247, KH0033/UR044.

### 03 Gramática (Opus)
- **Registros de datos, no texto.** Ningún subconjunto pasa una prueba de "texto" que no se explique por números, bandeado o artefactos.
- Distintivo: autorrepetición (bandeado) y vocabulario saturado (Heaps β 0,44–0,73 vs ~0,9 en texto quechua/español). Zipf no diagnostica lengua (la tupla física da 0,86, lo mismo que Sivan presenta como "lingüístico").
- **Columnas bien apoyadas**: posición en grupo predice color en 51 % (texto 5 %, Markov 11 %) y magnitud en 46 % (4 %). 175/299 quipus con grupos repetidos (58,5 %) tabulares con BH; ancho típico ~6. Coincide con 02.
- **Frases compartidas: negativo.** El exceso de n-gramas desaparece al fijar la secuencia de colores: no hay léxico de nudos compartido entre quipus. Sí "formularios" de archivo (Santa, Leymebamba; Incahuasi: cuerda rosada vacía + blanca con valor grande en 4 quipus).
- S/Z: simples Z, largos tienden a S (replica Clindaniel por quipu, p=2,5e-8); homogénea por grupo y en bloques (26 quipus) → "una mano/sesión por grupo" no descartable; marcador de inicio de grupo: negativo.
- **Canal silábico de Sivan refutado en sus predicciones**: en 2700 cuerdas con ≥2 largos, efecto de orden 4,5× menor que en quechua, repetición mucho mayor, 69 % vueltas no crecientes hacia abajo (orden numérico, no fonotáctico).
- 26 quipus con mayoría de cuerdas no decimales casi nunca tienen columnas (2/25 vs 213/493, p=2,6e-4): ¿otro género de registro? (UR050–055, UR039, AS090_N2, UR203, AS014, UR1087, HP051_A, KH0001, UR193).

### 04 Concordancias (Opus) — hallazgo principal
- **Jerarquía de totales bien apoyada en Incahuasi**: los totales de los 33 grupos de UR278 (~9 colgantes, p. ej. 415+415+353+415+415+415+414+413+363 = 3618) aparecen **en orden** como primera cuerda de los grupos de UR266 (3618, 1506, 1384, 2919, 2089, …): 16/33 en orden vs media 2,8 (máx. 7) en 2000 permutaciones; q = 1e-8 / 1e-8 / 7e-4 con FDR sobre 311 150 pares ordenados. UR275 (copia de UR266) repite 11. Es la única relación de resumen entre quipus que sobrevive en todo el corpus. Tras cada cabecera de UR266, cuerda constante 47. *(corregido después: ver «paquete_revision (Opus) listo y correcciones»)*
- Cuasi-duplicados (201 930 pares, ±1 dígito, FDR): 25 pares. Replica los controles de Urton 2005 (AS159/AS173, UR1114/UR1123, UR006/UR009/UR021, Puruchuco UR064/UR068). **Copias entre museos no publicadas en nuestras fichas**: HP055 (Lima) ≈ AS084/UR1084 (París) 121/142 exactas; AS038/KH0049 (Lima) ≈ UR122 (Göteborg); Basilea MM008/015/016 copian tramos de UR212 (Berlín); UR1175 ≈ UR233+UR232; UR1118 ≈ UR218; QU002 ≈ UR137. Largos no correlacionan → objetos distintos.
- **Duplicado de base no documentado**: UR1107/UR237 = mismo objeto (largos r=0,99), registrado invertido → avisar al OKR.
- Puruchuco: UR063 consolida bloques de UR073 y UR078 (5/5 cabeceras, p=1e-4, propuesto). No reproduce las sumas de Urton y Brezine. Santa: ningún par copia/resumen. *(corregido después: ver «Ronda 8-9: resultados»)*
- Negativos: sumas cuerda a cuerda B=A1+A2 entre quipus; totales completos de un quipu como cuerda de otro; relaciones aparentes con valores pequeños caen.

### 09 Incahuasi (Sonnet)
- `[x, c, x−c]` **bien apoyado y exclusivo** de 8 quipus del Sector A (UR255, 256, 266, 267A, 267B, 269, 274B, 275); los 23 JC no lo tienen; fuera de Incahuasi no hay tríos no triviales.
- c por pareja: 15 (UR255/UR267A), 10 (UR256/UR267B), 47 (UR266/UR275; = la constante 47 de 04). En UR269 c varía por fila en bloques de 5.
- Tres parejas de quipus comparten x (24, 21, 25 valores idénticos vs ~5; p≈0,003); orden de c y neto invertido en cada pareja; R/V opuesta (p≈0,13).
- Bruto x = cuerda blanca (UR267A 15/15, UR269 14/15, UR275 6/7; Holm 0,002–0,016). Jaspeadas al final del registro.
- Hipótesis: proporcional (diezmo/merma), saldo encadenado y salida variable **descartadas**; **sobrevive deducción fija por registro** (tara/tributo/ración del depósito, indistinguibles). Fuente de la interpretación: Clindaniel 2019 citando Urton y Chu 2015:522. Traducción registro a registro de UR267A en el informe.

### 07 Series de largos (Opus)
- Reales en el registro (KFG≈OKR 99–100 %, salvo UR144) y **exclusivas de los 8 quipus con canutos** (UR039, 050, 052, 054, 055, 110, 112, 144; P=2,5e-11), probablemente coloniales.
- Vueltas en campana centrada en 5, cuerdas homogéneas (5-5-5), sin bandas posicionales, sin vocabulario compartido; parecido por fajo/vecindad/color.
- Rechazadas: otra base/suma, calendario, códigos posicionales; unidades mixtas no apoyada. Sobrevive: hábito de anudador/lote ("tamaño de nudo", no valor). **Los 4 quipus clave de Sivan son de esta familia → su silabario no se sostiene.**

### 08 Auditoría de sumas (Opus)
- El 74 % de KFG = 482/650 quipus con ≥1 de 7 tipos de relación (PPS a cualquier distancia, valor >10). Reimplementada (98,6 % de concordancia): **93–100 % de las relaciones KFG son esperables por azar** (PPS 8076 obs vs 7913–8094 esp.); mediana de "coste" 0,95. Pero la métrica tiene potencia ~24 % aun con sumas en todos los grupos → **el 74 % no es informativo** (ni prueba ni refuta contabilidad). Medrano y Khosla ya lo admitían; su argumento era la lateralidad. `estado_del_arte.md` lo etiqueta mal.
- Lo que el azar no produce: sumas adyacentes ≥100 (200 vs 83–87, ×2,4); relaciones de coste <0,001 (13 vs 0,3).
- **Quipus con contabilidad interna verificable: 20 (3,1 %)**; robustos a dos nulos: AS006, AS199, UR118, UR119, UR166 + 9 de Incahuasi. Prevalencia corregida por potencia ≈1,5–11 % (central 4–7 %).
- Lateralidad 54/46 sobrevive (p=0,002) pero la mitad se explica por la posición de valores grandes.

### 10 Tablas (Opus)
- 177 quipus tabulares (mediana 8 filas × 6 columnas). **Filas con "tamaño"** (ρ medio 0,30 entre columnas en 60/135; una fila grande lo es en todas sus columnas) → filas = unidades (personas/hogares/ayllus/depósitos) y columnas = categorías: apoyado con datos.
- Arquetipo único entre quipus: **1.ª columna mayor (68 vs 38,6) y a menudo blanca** = categoría principal, no total (Holm 0,018–0,048); última columna más vacía.
- **Columna-total solo en Incahuasi**. Columnas casi constantes (36 quipus): valor 1 (marcadores) o cuotas (15, 10, 47, 100, 20). *(corregido después: ver «30_frontera_estructura (Opus), cerrado»)*
- **Formato nuevo bien apoyado: "fila + cuerda-total suelta"** en AS044, UR1096, UR118, UR119 (Paracas), UR166, UR149. *(corregido después: ver «14 Copias y totales sueltos (Sonnet)»)*
- Negativos: filas-resumen dentro de la tabla, gran total, número de filas típico (4/6/10/12), seriación de filas.
- UR011 (Leymebamba): dos columnas gemelas (razón 1,01, p=0,0001). Significado concreto de cada columna: especulativo; nada en los datos lo fija.

## 15 Quipu y Tocapu (Haiku) — actas del simposio de Lima 2009

Entregables: `analisis/15_quipu_tocapu/` (capitulos.csv 16 contribuciones, afirmaciones.csv 166 afirmaciones comprobables, informe.md).
- Urton y Brezine: 222/451 quipus con procedencia (12 archivos, Pachacamac 68). Nudos simples 35 % S / 65 % Z; ocho 30/70; 72/272 quipus todo-Z. Retorcido final S en 96 %. Comprobable contra KFG/OKR (tarea pendiente, ligera).
- Pereyra 2006 vía Pozzi-Escot: Casa de los Quipus, 27/32 numéricos. Armatambo Contexto 24: 8 quipus, el 1423 con marca que divide el cordón en dos sectores (cf. mitades).
- Zuidema: aritmética de uncu (274 = 10 meses siderales) cuadra, pero su «quipu del Cuzco» es hipotético; no cambia nuestro negativo de calendario (05).
- Inkawasi no aparece (0 menciones); sin cuotas tributarias cuantificadas. Censos coloniales en Ulloa y Cantos de Andrade.
- Erratas del volumen: 38 381 vs 38 831 cordeles; «Pereira»; resumen de Arellano inexacto.
Evidencia: extracción documental; nada nuevo sobre significado. Útil como lista de verificaciones.

## 12 Urton 2017 (Sonnet) — lecturas frente a KFG

Entregables: `analisis/12_urton2017/` (informe.md, lecturas.csv con 23 lecturas, scripts a–j). Límite: KFG y Urton comparten la base KDB; coincidir prueba transcripción, no verificación independiente.
- **CORRIGE a 05: UR006 sí reproduce la estructura.** KFG codifica las cuerdas-lazo como subsidiarias de 25 lazos; contándolas: 24 pares, 729 cuerdas (Urton 730), años 361/368 (362/368), 45/48 sumas de la Tabla 4.3 exactas (nulo 0,56). Estructura única en el corpus: **bien apoyado**. Lectura calendario bienal: **propuesto** (un total ±1 de 730 sale en 40 % de remuestreos). «3 000 tributarios»: débil.
- Confirmadas con nulo: UR028 (cuerda 1 = 102 = Σ 2–4; 5/6 sumas de conjuntos); UR021 fuente de meses 13–16 de UR006 (0/300 perm.); UR011 15/15 pares gemelos (p<1e-4); Puruchuco UR068→UR067/UR066 con las mismas dos divergencias; firma «3 cuerdas de valor 1 en las 12 primeras» solo en esos 4 quipus; UR053B/C 35/51 valores con desfase 10 (p=2e-4) y uniones opuestas; UR268 valor fijo 208.
- No reproducidas: 6 pares de Pachacamac (correlación posicional ≈0); emblema 1-7-9 (solo UR066); «posición 1 determina las demás» en Santa (|ρ|≤0,16 dentro); «solo UR266/275 tienen 47» (UR269 tiene 8); UR273B «miles similares» (0).
- Compatibles sin discriminar: UR011 como colapso demográfico (escalón −75 %, no curva); criterio censo-like (35/482 quipus); emparejamiento pachaca/quipu en Santa (25 % por azar).
- Urton no ve la jerarquía UR278→UR266 (hallazgo de 04).
Próximo: Apéndice A (padrón) vs orden de grupos del Santa; secciones reales UR063/UR073; cuerdas bajas previas a cada par de UR011; columnas en los 35 censo-like.

## 14 Copias y totales sueltos (Sonnet)

Entregables: `analisis/14_copias/` (informe.md, scripts, verificacion_*.csv).
- **Crítica textual** (25 pares, 13 familias; duplicados de base como ruido): valores conservados al nivel del ruido de lectura (86,6 % exacto vs 93,0 % en el mismo objeto leído dos veces, p=0,21). Errores: 54 % de un nudo, sin dirección común. Ediciones sistemáticas solo en dos pares: UR233 omite las subsidiarias de UR1175 y repite 100→110; UR1084 omite 8/14 cuerdas 222 de HP055 (Holm 3e-4). Sin «actualización de censo». Orden de fidelidad (propuesto): valor ≳ presencia > color > largo > dirección ≈ R/V. **El contenido que se copiaba era el número; el color se conserva solo parcialmente y la dirección/fijación no.** Sesgo: copias detectadas por valor.
- **Fila + total suelto:** 51 aciertos exactos vs 14,9 nulo (p=0,0005). 7 quipus con q<0,05: AS044, AS066, AS199 (nuevos los dos últimos), UR1096, UR118, UR119, UR166; UR149 no se reproduce. Sin concentración por procedencia/museo. UR118/UR119 = registros paralelos del mismo formato, no copias.
- **Museo:** UR232 y UR233 comparten inventario VA63038 (comentario OKR de KH0469); UR212 = VA42513 o VA42508(A); Basilea MM008/015/016 = IVc.366.03; UR1107/UR237 = mismo objeto (discordancias de lectura decimal). Tablas de cuerdas a medir en `verificacion_*.csv`.

## 11 Rosetta (Opus) — transcripciones coloniales

Entregables: `analisis/11_rosetta/` (informe.md, scripts r0–r3b, medrano_metadatos_72.csv, transcripciones_numeros.csv). Medrano 2019 es lingüística, sin listas de cifras: solo 10 secuencias / 63 cifras recuperables (fragmentos, padrón del Santa 1670, tabla 11.3 de Urton).
- Dato nuevo: encomienda de Aldana (memoria 40), 11 pueblos suman exactamente 260, total declarado *antes* de la lista.
- Lectura oral (Medrano): pares categoría→número, detalles orales, totales calculados con piedras/yupana al leer, «quipus resumen» aparte; errores corregidos de ±1.
- **Firma asignación vs recuento** (apoyado; «asignación» propuesto): cuerdas intactas ≥10 múltiplos de 10 en 28,9 % (recuento esperado 10 %); heterogeneidad χ²=3690/329 gl; 26 quipus «de asignación» (≥80 % redondos), 159 compatibles con recuento. Cuerdas rotas: 58 % redondas (pierden unidades) → excluir. Tablas de 10 con filas co-crecientes = recuento (p=0,01, Holm 0,03).
- **Cuotas repetidas** (apoyado): 929 adyacentes idénticos vs 552 (p=0,0005; 20 quipus q<0,05), concentrados en los redondeados (p=1,7e-4). Ambas firmas: AS172, UR197, UR219, UR271.
- Total antes de la lista: no es regla (solo UR118, UR119, UR275). Negativos: cantidad×precio=valor; tamaños quipus del Santa vs pachacas.
- **Rosetta: negativa con potencia bien apoyada.** 10 208 pruebas, 0 con q<0,05; control positivo UR278→UR266 recuperado (q=7e-4); listas insertadas con 2 errores se detectan 89–100 %. Esperable: documentos de sierra/Charcas, corpus costero.
- Lectura propuesta: filas = pueblos/ayllus; 1.ª columna = partida principal; columnas constantes = tasa fija; listas redondas repetidas = asignaciones; totales calculados fuera del quipu (explica la escasez de sumas internas de 08).
Próximo: listas completas de *Textos Andinos* (Pärssinen y Kiviharju) o XML de Medrano; Chucuito 1567.

## 13 Sistema contable de Incahuasi (Opus) — hallazgo principal (pendiente de verificación independiente: 16)

Entregables: `analisis/13_sistema_incahuasi/` (informe.md con diagrama y traducción, 12 scripts, grafo_cuerdas.csv, libro_consolidado.csv).
- **Bien apoyado:** las parejas atadas son dos partes de un registro que se suman. UR273A_i + UR273B_i = cabecera en UR266/UR275/UR269: 8/18 exactas vs 1,3 (Holm 0,002); UR274A rellena huecos de UR273A. UR267A + UR267B = filas de UR269 con cuota 25: 3/6 vs 0,19 (Holm 0,005). Orden conservado (τ=1). *(corregido después: ver «Resultados ronda 7-8» y «Pruebas dirigidas sobre datos completos anonimizados»)*
- **Bien apoyado:** cuota consolidada = suma de cuotas: 30 + 17 = 47; 15 + 10 = 25 (nuevo; ni Urton ni 04/09). *(corregido después: ver «16 Verificación independiente de 13»)*
- **Bien apoyado:** UR270 = detalle: colgantes blancos = parte B, subsidiarias = parte A (Holm 0,006). Cada celda de UR278 = colgante + subsidiaria de UR270, columna a columna (5 grupos con 6–9/9 vs 0,003; p=0,0002).
- **Doble vía:** total por 9 columnas (UR270→UR278→UR266) y por 2 partes (UR270→UR273A/B→UR266) coinciden. Cabecera blanca en 73 % de 222 registros (31 % esperado). Copias nuevas UR273A–UR274A, UR273B–UR274B.
- **Apoyado:** UR269 = libro maestro en bloques de 5 (periodos); fila 1 = flujo 47, fila 5 = flujo 25; cuotas 47, 46, 46, 44, 25 → 3 flujos perdidos. UR278 = 33 registros sucesivos del flujo 47 en 9 columnas de tamaño relativo estable. *(corregido después: ver «Cierre DeepSeek + equipo rojo»)*
- **Negativos:** ningún nivel por encima de UR266 (13 260 pruebas); UR257 y JC (Sector B) aislados; neto jaspeado solo en UR275.
- **Especulativo:** UR268 (cuota 208 = 47+46+46+44+25) como nivel de periodo; identidad de columnas y partes; maní/ají.
- **Predicción comprobable:** en los 5 quipus de Inkawasi no estudiados por Urton, parejas cuyas cuotas sumen 46 o 44 y cuyas sumas den las filas 2–4 de UR269.

## Ronda 4 (en curso)
- 16_verificacion_incahuasi (Haiku): recálculo independiente de 13 sin sus scripts.
- 17_okr_pendientes (Haiku): tabla puente KH↔UR↔AS↔KFG, conteos 650/651/685/702/709, xlsx y AS1-AS9.db del OKR, inventario de lo que requiere transcripción manual.

## 16 Verificación independiente de 13 (Haiku, scripts propios, semilla 16)
| Afirmación de 13 | Replica | Cifras |
|---|---|---|
| UR273A_i + UR273B_i = cabeceras UR266/275/269 | **sí** | 8/18 exactas, nulo 0,73, p<1e-4 |
| UR270 colgante+s1 = celdas UR278 | **sí** | mismos 5/12 grupos (dos 9/9), control solo colgantes 0, p=1e-4 |
| Totales UR278 = cabeceras UR266 en orden | sí, cifra menor | 11 pares exactos τ=1 (14 con ±1); 13 decía 15 |
| UR267A+B → UR269 | parcial | 5/26 exactas en barrido completo (p=5e-4); 13 probó solo las 6 filas con cuota 25 |
| Cuotas explícitas | parcial | 30 en 274A 17/26; 47 en 266 23/32 y 275 24/26; 15 y 10 en 21–26 de ~26; **17 explícito débil: 274B 12/33 (p=0,06), 273B 3/27** |
Consecuencia: las dos relaciones centrales (A+B y UR270→UR278) quedan **bien apoyadas y replicadas**. «47 = 30 + 17» baja a **apoyado**: el 17 se infiere sobre todo por aritmética (x − n = c), no por cuerda explícita. UR267→UR269 apoyado. *(corregido después: ver «Pruebas dirigidas sobre datos completos anonimizados»)*

## 17 OKR pendientes y tabla puente (Haiku)
Entregables: `analisis/17_okr_pendientes/` (puente.csv, cuerdas_extra.csv, inventario_manual.csv, informe.md).
- **19 quipus nuevos, 776 cuerdas** en `cuerdas_extra.csv` (KH0631, KH0633–0635, KH0638–0651, KH0702); 743/776 valor = suma de nudos, 21 discrepancias marcadas. AS1-AS9.db = AS001–AS009, ya en KFG (sumas difieren en 6; sin alinear cuerda a cuerda).
- **Conteos explicados:** OKR 702 KH; khipu.db 619; KFG 651 xlsx = 646 KH (5 con dos xlsx); 612 en ambos, 34 solo KFG, 7 solo khipu.db. 650 = 651 − UR044 (duplicado de AS031). 685 = volcado SQL. 709 = KFG posterior (K-CAT), 38 KH ausentes aquí.
- **Alias conflictivos:** AS101 en KH0114/0115; AS124/UR1124 en KH0138/0139; KH0033 = UR1031 y UR044; VA63038 = UR232/UR233; **VA24370 = UR1106/UR1107** (UR1107/UR237 NO comparten inventario; su identidad la sostienen solo los largos, 14); 80.1012 aka 2708 en KH0676/KH0700.
- Manual: KH0632 sin datos; KH0652 hoja de hilos envueltos; KH0676 sin columna de valor; KH0674/0675 PDF escaneados; KH0653–0663 jpg (borrador DeepSeek en curso: n_fichas_jpg); croquis KH0638–0652; 21 discrepancias.

## DeepSeek, primera tanda (19 informes, 19:12–20:15; leídas solo las secciones «Para el coordinador»)
Archivos (`analisis/ds/a_*`):
- **Ninguna relación entre quipus sobrevive al nulo** en Lima (63), Leymebamba (22), Nazca, Chile (10), Pachacamac AS/UR (59) y HP (30), Santa. Excepciones = copias: Ica replica AS114/AS123 y AS159/AS173 de Urton (p=0,002).
- **a_incahuasi tampoco encontró nada con nulos genéricos**, cuando 04/13/16 sí, con pruebas dirigidas (orden, cabeceras, A+B). Lección: las relaciones entre quipus solo aparecen con hipótesis estructurales; los barridos genéricos no tienen potencia. Útil: lote JC = torsión Z y valores pequeños; lote UR = S y grandes.
- Santa = 6 quipus (UR087–092); **KH0227 (Huaura) y UR198 (Nazca) mal incluidos por el nombre**. R/V por quipu reproduce a Contreras (5 puros + UR090 mixto). Nudos Z dominantes.
- Pachacamac: AS125 = UR247 (duplicado OKR); HP = 30 objetos (HP001/002 y HP029/030 comparten registro). Z > S en nudos (p=0,007, replica Clindaniel). Armatambo: único con torsión Z.
- Chile (Playa Miller/Arica): subsidiarias masivas (p≈1e-6); trío UR131A/B/C coherente.
Quipus (`analisis/ds/k_*`):
- **Patrón recurrente: cuerdas marcadoras + bloques de tamaño fijo.** KH0083: 7 cuerdas rojas sin nudos cada 11 (8×11). UR001: bloques de ~16 separados por 20 cuerdas PK sin nudos. UR1032: 5 marcadores M → 6 secciones de módulos 5 azules + 3. CM009: 15 registros de 4 colores. AS069: cada grupo empieza con una marcadora de color (p=0,001). UR004: 31 PK = marcadores. Converge con los marcadores blancos de Medrano y Khosla y con los separadores rosas de Incahuasi (13).
- **Problema de datos: UR087 tiene 13 cuerdas superiores que KFG registra como union=U, no T** → los análisis de cuerdas superiores (01, 08) pueden infraestimarlas. Cruzar con CORD_CLASSIFICATION del OKR.
- UR006 (k_): sin contar las cuerdas-lazo; superado por 12. Las lecturas astronómicas de Sáez-Rodríguez (UR019, UR1104) no resisten.

## Ronda 5 — ambición (altitud, profundidad, amplitud), lanzada 2026-10-17
Meta: pasar de «hay sumas» a «leemos un archivo», con juez externo y adversario.
- 18_equipo_rojo (Opus): intentar destruir Incahuasi (senderos bifurcados, nulos duros, transcriptor que corrige, fuera de muestra).
- 19_prediccion (Sonnet): leave-one-out de cuerdas de Incahuasi vs líneas base; predicciones a ciegas para museo.
- ds/n_detectores (DeepSeek): detectores dirigidos de 13 en todo el corpus; ¿otros sistemas tipo Incahuasi?; cuerdas superiores que KFG pierde (union=U).
- ds/n_que_se_contaba (DeepSeek): demografía (pirámide), unidades decimales incas, capacidad de depósitos, Benford.
Después: búsqueda de antecedentes (OpenAlex + DeepSeek + Sonnet para dudosos).

## Revisión directa del coordinador (código propio, sin scripts de 13/16)
- UR273A + UR273B alineados por número de grupo (los separadores PK caen en los mismos grupos 10, 14, 16, 23, 27): 8/18 sumas exactas en cabeceras de UR266/UR275/UR269; nulo 0,94; 0/10 000 permutaciones lo igualan. Alinear por «registros con nudos» (saltando grupos vacíos) desfasa y da 1/21: la alineación por grupo es la correcta.
- UR270 colgante + s1 → UR278: g0→g21 9/9, g4→g25 9/9, g5→g26 7/9, g8→g27 8/9, g9→g28 6/9 (±1); solo colgantes: ninguno ≥6. Nueve números de tres cifras en orden: no es azar. Curiosidad: en las dos filas 9/9 la 1.ª columna de UR278 es +1 (237→238, 301→302).
Veredicto: las dos relaciones centrales quedan confirmadas por tercera vía independiente.

## Parciales 2026-10-18 00:40 (equipo rojo, predicción, DeepSeek tanda 2)
- 18 equipo rojo (parcial): A+B UR273 sobrevive corrección por jardín de senderos (p corr 0,015). UR267A+B→cabeceras UR269 NO (p corr 0,32) → "no bien apoyada". Búsqueda completa de pares-suma en otros archivos (~46k pruebas): nada comparable; el sistema encadenado es exclusivo de Incahuasi. Sumas no son números "fáciles".
- 19 predicción (parcial): LOO en Incahuasi, cuerda con redundancia: exacta 67 % (sin redundancia 18 %); dos vías concordantes 77 %, discordantes 7 %.
- n_que_se_contaba: demografía descartada (CV 9 columnas UR278 = 0,18; pirámides exigen 0,5-0,9; p<2,5e-4). Positivo: 9 partes administrativas equilibradas. Sin llenado de unidades decimales. Unidad = bulto (10-50 kg), no ítem. Benford inútil.
- n_okr_resto: KH0674/0675 transcritos (cierran con portadas), KH0676 convertido (regla aditiva, apoyado). Errata OKR: KH0676 = Brooklyn 36.718, no 80.1012. 11/21 discrepancias del equipo 17 eran errores de su parser → desconfiar de VALIDACION de 17. AS008: cuerda de 17.612 ausente en KFG. KH0632 sin datos.
- n_databook: KFG vs Databook valor 94,7 %, color 92,2 %, largo 99,9 %. KFG a veces inventa: AS081 (Databook "no numerical interpretation possible") recibe valores; AS129 concatenados. 80 quipus del Databook (38 %) no están en KFG. 812 notas de Ascher en notas_ascher.csv.
- k_UR1057: retícula 24×5×4 casi vacía (68 % sin nudo), sin aritmética; tabla administrativa (apoyado). Sumas "ascher_sum_relations" de KFG = sobreajuste en quipus con ceros.
- k_UR113: 10/23 grupos ordenados decrecientes (percentil 99,4 del corpus), 17 subtotales exactos (p=0,002). Los "135 sumas" de KFG son artefacto.
- k_UR262: no sumatorio; gramática limpia (una mano); AB = gradiente de profundidad; primera cuerda = cabecera, no total.
- t_notas: rotas Leymebamba 1,3 % vs costa sur 15,5 % (conservación). KFG=OKR en notas. Sin plumas/cuentas.
- t_cuerdas_vacias: 30,5 % sin nudos = 3 fenómenos; vacías al final de grupo (38,5 vs 26,2 %, p=3e-14); 462 grupos en blanco (vs 227 esperados).

## Parciales 2026-10-18 01:00
- n_santa_padron: orden del padrón 1670 vs quipus Santa NO se sostiene (p=0,18; p=0,0056 previo era circular → 0,24). Nuevo: en UR087 color de primera cuerda = seriación de período 4; UR092 ciclo de 5 colores. 44 % de grupos: color = posición, no identidad.
- t_cuerdas_superiores: 23/72 superiores = suma exacta del grupo contiguo anterior (nulo 2,4; Holm 0,0035), grupos de tamaño 6 casi siempre; color no es criterio. Bien apoyado.
- t_ceros: 726 cuerdas con cero posicional interno; el hueco mide ~1 banda (ratio 0,96); alineación decimal local por grupos.
- t_espaciado: espacios entre grupos no delimitan secciones aritméticas; posición de nudos ordinal y redundante.
- t_valores_frecuentes: 10/15/20/40 no son especiales; solo 100 (2,05×) sobrevive limpio → pachaca o redondeo. "Estándar 15" y "47" de Incahuasi = artefacto de copias en el nulo de vocabulario (no contradice cuotas en flujos, sí su lectura como vocabulario del sitio).
- t_canutos_fibra: canutos = sistema de fijación (~4 colgantes c/u, siempre camélido); en UR052 23/24 fronteras de grupo = fronteras de canuto (p=5e-5, apoyado); color de canuto es capa independiente de información.

## Cierre DeepSeek + equipo rojo (2026-10-18 03:40)
- Todas las tareas DeepSeek terminadas.
- 18 equipo rojo (informe.md): SOBREVIVEN UR270→UR278 (P+S1), UR278→UR266, UR273A+B (p corr 0,015; 0/59 pares ajenos). SE DEBILITAN 267A+B→UR269 (p corr 0,32) y 30+17=47 (el 17 casi ausente; KFG omite 32 subsidiarias de UR274B presentes en OKR). CAE la "posición en bloque" de UR269 (separación por magnitud). Bandera: UR266 reimportado 2020, 1,732→1737. Prueba fuera de muestra propuesta: buscar en 5 quipus inéditos de Inkawasi una pareja A/B que dé filas 2–4 de UR269; 04_fuera_muestra.py no ejecutado.
- n_detectores: Incahuasi único (11/12 cuotas significativas). Los 5 controles se recuperan. Huacho UR1088+UR195 = artefacto de densidad. D5: KFG pierde 92/95 cuerdas superiores nivel 1 de OKR y 502/502 marcadoras; KFG union=T ≠ OKR T (54 casos). No usar KFG para superiores/marcadoras.
- t_mitades: no hay mitades especulares (al contrario: gradiente decreciente izq→der, 61 % vs 49 %, p=0,0005). R/V y S/Z forman bloques, no mitades, e independientes. Dualidad, si existe, en secciones contiguas.
- t_alt: columna alt vacía al 100 %. KFG vs OKR valor 99,33 % idéntico; errores = factor 10 o nada. Tolerancia recomendada 0 o ±1, nunca ±5 %; el enemigo es la multiplicidad.
- t_okr_vs_kfg: 0,63 % discrepancias, 86 % en 5 quipus (UR090, UR144, UR235, UR193, UR190). ERRATA: KFG KH0197/0227/0267/0350 contienen en realidad KH0198/0228/0268/0351 (desplazados en uno). 49,8 % de discrepancias = factor 10 de decodificación de posición. knot_cluster.TOTAL_VALUE = 0 en todas las filas de OKR.
- Pendiente: 19 predicción.

## 19 Predicción (Sonnet, cerrado 2026-10-18 ~04:00) — analisis/19_prediccion/informe.md
- 791/1558 cuerdas del archivo (50,8 %) tienen al menos una vía ciega de predicción. LOO: exacta 58,8 % vs mejor línea base 20,5 % (moda del quipu).
- Por regla: celda UR278 = UR270 74 % (base 2 %); fila UR278 vs libro 55 % (≤4 %); A+B 41 % (9 %); copia 48 % (17 %); cierre 62 % (27 %); cuota 70,5 % = empate con la moda (no prueba nada).
- Honestidad: cuerdas del grafo de 13 aciertan 66,6 %; las no usadas en el descubrimiento 17,5 % ≈ base 15,1 %. Validación cruzada por bloques: cuota y cierre se sostienen; copia cae 49→18 %; fila278 y A+B pierden cobertura con 2 mitades. Control nulo de copia: 0/51.
- Veredicto: leemos la aritmética de la cadena UR270→UR278→UR266/UR275 y de los componentes con cuota; no el archivo entero ni el contenido. Prueba sin sesgo: los 5 quipus inéditos de Inkawasi.
- predicciones_museo.csv: 252 filas (43 de confianza alta). Ej.: UR278 g12 suma 2533 vs libro 2633 (una celda +100); UR278 g21 celda 1 238→237; UR274B cuotas "10" serían 17; UR275 p51 40→47.

## Ronda 8: altitude / depth / range (2026-10-18 ~04:00). Tareas con DeepSeek-V4.1-Flash
- ALTITUD: prueba ciega "sobre sellado": 52 quipus de Incahuasi anonimizados (Q01..Q52, a/b = partes atadas), 597/3980 cuerdas anudadas ocultas (15 %, semilla 20261018), sin notas. Dos corridas Flash independientes en directorios aislados fuera del repo (quipu_ciego y quipu_ciego2), sin acceso a la web ni a otros directorios. Respuestas y mapa de ids guardados aparte (sellado/). Script: analisis/ds/ciego.sh. Tras puntuar: paquete de predicciones congeladas para museo.
  n_legibilidad (mapa de legibilidad del corpus), n_simulador (modelo generativo del archivo).
- PROFUNDIDAD: n_okr_incahuasi, n_fuera_muestra, n_casi_aciertos (modelo de error), n_fotos (auditoría visual AS con fotografías publicadas del Databook, consultadas para verificar valores).
- AMPLITUD: n_no_numericos, n_nueve_partes (etnohistoria), n_materiales (manos/talleres), n_otros_sistemas (Uruk, Exchequer, warazan, Monte Sierpe), n_almacenes (economía/unidad). Lingüística: después de n_no_numericos.
- Antecedentes: ant_incahuasi, ant_resto.

## Ronda 9 (2026-10-18 ~04:15): de sistema a desciframiento (método Kober/Ventris)
- n_rejilla: diccionario interno de categorías a partir de las relaciones verificadas; firma de las 9 partes.
- n_puruchuco_pacha: el método de Incahuasi (todas las cuerdas, OKR, alineación por grupo, P+S1) en Puruchuco (jerarquía de Urton & Brezine 2005) y Pachacamac.
- Después (Opus): traducción completa del archivo de Incahuasi + cruce de la firma de 9 partes con listas coloniales (ancla de Ventris).

## Resultados ronda 7-8 (2026-10-18 ~04:15)
- ant_incahuasi: H1 (A+B), H2 (UR270→UR278), H3 (UR278→UR266) NO publicados como relaciones concretas: 0/16 sumandos de H1 en Urton 2017 ni en suplemento 2018; 6/8 cabeceras sí. Antecedente cualitativo en Urton 2017 cap. 9 → "nuevos con antecedente cualitativo"; citar a Urton generosamente. H4 "exclusivo de Incahuasi" FALSO como formulación: Puruchuco (Urton & Brezine 2005) y UR9/UR21→UR6 (Urton 2017 cap. 4) son cadenas publicadas; lo nuevo es la arquitectura concreta. H6: 10/15/47/208 ya son los valores fijos de Urton & Chu 2018; 17 y 30 los consideraron y rechazaron; 46 nuevo. H5: 9 columnas ya descritas; nuevo CV 0,18 + rechazo demográfico. H7 (LOO) nuevo como cuantificación.
- ant_resto: R2 (seriación de color Santa) YA PUBLICADO por FitzPatrick 2024 → citar o retirar. R3: el p=0,0056 era nuestro; el p=0,02985 de FitzPatrick es el mejor de 20 alineaciones (sin corregir ~0,60): crítica nueva. Contreras 2026 no valida numéricamente el match de Santa. R8 (erratas) claramente nuevo (0 en literatura e issues). R4 canutos: aporte real, contradice Milillo 2024 (un solo quipu: 23/24). R6 ceros posicionales: evidencia directa contra Florio & Overmann 2025 (niegan posicional/cero) → alto valor teórico. R5: no es hombre de paja de Urton, formular como "la dualidad no se manifiesta como simetría especular". R1, R9 incrementales (Locke 1927; Medrano 2019).
- n_fuera_muestra: 1a (UR273A+B) SOBREVIVE fuera de muestra: mitades 5/9 (p 1,3e-4) y 3/9 (p 0,004), Holm 0,016. Predicción UR274A por UR273A en blanco: 3/4 (no 3/3). 1b (267A+B) CAE (Holm 0,50). Posición en UR269 CAE. Cuota por paridad no confirma.
- n_okr_incahuasi: OKR confirma el núcleo con las mismas cifras (Holm ≤ 0,0021). KFG pierde 111 cuerdas en Incahuasi (UR256 +58, UR274B +32…). Cuota 17 en UR274B se refuerza (p 0,086→0,004); UR273B sigue sin 17. Ninguna relación nueva. Usar OKR como base de Incahuasi (cuerdas_okr.csv).
- n_simulador: ATENCIÓN, corregido por el coordinador. Afirmaba que los 8 fallos A+B difieren exactamente 10^k (p=2e-16), pero los destinos venían del campo en_resumen de 13 (elegidos con tolerancia) y el nulo usaba destinos al azar: circular. Nulo correcto (¿hay alguna cabecera del pool a ±10^k?): 7/10 fallos vs 2,18 esperados, p ≈ 0,0015 (18 y 19 suman igual: no independientes). Firma "error de un racimo" = apoyado, no bien apoyado. Válido: el 8/18 no es ruido de transcripción (tasa 0,22 %); UR270→UR278 es mezcla (filas derivadas vs independientes); KFG y OKR de Incahuasi los firmó la MISMA transcriptora → no son lecturas independientes. Cuerdas vacías estructurales por rol.
- n_nueve_partes: mismas 9 unidades en el mismo orden en UR270 y UR278 (identidad fija). Planitud excepcional (7/8 grupos de 9 con CV<0,2 del corpus son de UR278). Proporciones varían por registro (unidades reales, no reparto fijo). No hay 9 documentado en Cañete (Lunahuaná 4 guarangas × 2 = 8 +1). 9 pachacas en Cajamarca y Collaguas. Propuesto: 9 pachacas de una guaranga. *(corregido después: ver «paquete_revision (Opus) listo y correcciones»)*
- n_almacenes: la unidad no puede pesar < 3,4-10,4 kg (capacidad Qolqawasi). La unidad es un VOLUMEN (saco 30-55 L), no masa. Cada columna ≈ 1,2-2 cámaras grandes. El test de capacidad solo excluye, no confirma. *(corregido después: ver «Corrección de escala»)*
- n_otros_sistemas: Uruk (2 niveles) y Exchequer (2-3) consolidan; nadie tiene 4 niveles con doble vía. Warazan de Okinawa: decimal anudado con cuotas → el decimal anudado no es exclusivamente andino. Monte Sierpe sin censo por bloque publicado. Copias = efecto de archivo.
- n_fotos: 88 fotos = 23 etiquetas (~30 objetos). KFG mete superiores y marcadores en nivel 0 (AS010, AS212, AS215). AS069: 205 marcadores contados como grupos, numeración desplazada hasta +169. AS124/136/140 atados a barras de madera talladas (nuevo).

## Antecedentes verificados por el coordinador con los textos completos (2026-10-18 ~05:30)
Se incorporaron Urton & Chu 2015, Urton & Chu 2018 y Urton & Brezine 2005 (texto completo cotejado; texto en analisis/fuentes_txt/).
- 2015 menciona UR255, UR256, UR261, UR266, UR267A/B, UR268, UR269, UR270, UR271, UR272, UR276B. NO menciona UR273, UR274, UR275 ni UR278. UR270 aparece solo como "sin valor repetido". Publica los pares cercanos UR267A/UR255 (fijo 15, secuencias x/15/y) y UR267B/UR256 (fijo 10, "solo un quinto de cuerdas") → nuestras copias 255/267A y 256/267B YA ESTÁN PUBLICADAS. Contexto: 14 quipus en la kallanka U.A.4 cubiertos de maní.
- 2018 menciona solo UR267A/B, UR268 y UR275. Interpreta los valores fijos como IMPUESTO: ~2 % del depósito promedio (UR275 47/2257,8 = 2,1 %; UR268 208 = 2,0 %; UR267B 10 = 1,9 %; UR267A 15 = 11,2 %). UR275 = maní, 56 446 unidades, depósitos de 1278 a 4272. UR267A/B = ají.
- Ninguna de las 8 sumas A+B, ni UR270→UR278, ni UR278→UR266 aparece en ninguno de los dos. Ninguno de los 16 sumandos aparece. CONFIRMADO: H1, H2 y H3 son nuevos. *(corregido después: ver «Inventario de Inkawasi»)*
- Consecuencia interpretativa: nuestras "cuotas" = el "impuesto" de Urton & Chu (no reclamarlo). Nuestro aporte: dónde van esos depósitos (A+B → libro, tabla de 9 → libro) y qué son las partes.

## LeVine (ed.) 1992, Inka Storage Systems (notas en analisis/fuentes_txt/LeVine1992_notas.md)
- Inkawasi (Hyslop vía Snead): 202 cuartos de almacén documentados (~250 estimados), de 3,5–4 m de lado, sin puertas, alrededor de un patio. Base militar ocupada poco tiempo, luego abandonada en favor de Cerro Azul. Es la excepción del almacenaje costero (la costa tiene 3 % de las unidades del imperio).
- Capacidad: 5000–14 000 m³ según altura (2–3,5 m). Cota superior de la unidad si todo lo registrado se almacenó a la vez y al 100 %: UR278 sola 80–227 L; libro de 122 609 unidades 40–114 L; de 300 378 unidades 16–47 L. La fanega (~56 L, glosario) cae dentro del rango, compatible con "unidad ≈ 1/6–1 fanega" de n_almacenes.
- Ancla documental clave: en 1533–37 las dos saya wanka entregaban bienes "en proporción directa a sus poblaciones relativas", y los quipus wanka listaban los bienes en orden constante (Murra). Cieza: un color de cuerda por producto. → Lanzado n_saya_proporcional (¿las 9 columnas aportan en proporción fija, como una leva por población, o varían como producción?).

## Ronda 8-9: resultados (2026-10-18 ~06:00)
- PRUEBA CIEGA (sobre sellado, puntuada por el coordinador; puntuaciones guardadas aparte en sellado/): las dos corridas Flash predijeron solo el 8 % de las 597 cuerdas ocultas (45 y 46), con 73 % y 76 % de exactas; las de confianza alta, 100 % (10/10) y 95 % (19/20). La base acierta 5 % y 14 %. Redescubrieron a ciegas: cuotas fijas (10, 15, 47, 208; ya publicadas por Urton & Chu), copias UR255≈UR267A y UR256≈UR267B (publicadas en 2015) y UR275≈UR266 (mismo libro reordenado). NO redescubrieron A+B ni UR270→UR278. La corrida 2 probó A+B=C solo con alineación por el mismo índice de grupo (nuestra relación cae en cualquier cabecera del libro, reordenada) y no sumó colgante + subsidiaria entre quipus. Lectura honesta: nuestras relaciones nuevas requieren elecciones no obvias. Esas elecciones las corrigió el equipo rojo (jardín de senderos, p 0,015) y la mitad fuera de muestra, pero un buscador genérico ciego no las encuentra. Coincide con n_puruchuco_pacha y n_legibilidad: los detectores genéricos no reproducen ni Incahuasi.
- n_puruchuco_pacha: el método reproduce LITERALMENTE la jerarquía publicada de Puruchuco (UR068→UR067 15/20; UR063→UR068 14/20; Holm ≤ 0,0006), incluidas las discrepancias 2904/2908 y 161/162 de Urton & Brezine. Copias UR066≈UR067 y UR064≈UR068. Las marcadoras OKR de UR073 dividen en 6 bloques = 6 secciones de UR063. Pachacamac, Ica y Huaquerones: nada. La unidad de alineación depende del género (registros en Incahuasi, columnas dentro de secciones en Puruchuco).
- n_rejilla: UR270 y UR278 tienen las mismas 9 partes en el mismo orden (39/45 celdas ±1; la identidad es la mejor de las 9! permutaciones en 5/5 registros). Firma: c2≈c1 (27,6 %) > c6 > c5 > c7 > c4 > c3 > c9 > c8 (17,2 %). El color marca la fila o el nivel, no la columna. La posición y la cuota sí marcan. Hay dos formatos de libro (UR275/UR266 frente a UR269).
- n_legibilidad: el corpus NO es legible con reglas a priori: 3,9 % de exactas frente a 2,56 % del nulo; 70 % de los quipus sin ninguna cuerda reconstruible. Solo cierre de grupo (41,5 %) y superior = suma del grupo adyacente (31,9 %). El 51 % de Incahuasi no generaliza (7,6 % con reglas generales).
- n_no_numericos: 56 quipus rompen la gramática decimal: tallies puros, decimales con unidades extra y sin nudos con color rico. Sin lenguaje de color (Collata no se replica). Se asocian a canutos (OR 7,3) y fibra animal. Prioridad: Cajamarquilla UR178, UR179 y UR180 (AMNH; nudos "no-axis").
- n_casi_aciertos: que un casi-acierto se repare con una sola edición NO es evidencia (31/35 frente a 28,3 esperados). Cuatro casos son discrepancias reales (+24, −44, −94, −94). g12 es una ESCALERA DE COPIAS: UR269 2433 → UR278 2533 → UR266/UR275 2633 (4, 5 y 6 nudos de centena). Lo más limpio para el museo: UR278 p180, 7L→6L (arregla la celda y la fila g21); UR275 p51 (falta 7L); UR274B p9, p13, p19 y p64 (las 4 cuotas más cortas: mirar la punta). *(corregido después: ver «Prueba dirigida A+B (Opus ciego, 05:35) y tareas terminadas» y «paquete_revision (Opus) listo y correcciones»)*
- n_simulador (corregido antes): KFG y OKR de Incahuasi son de la misma transcriptora → falta una relectura física independiente.

## Inventario de Inkawasi (Urton & Chu 2015, suplemento: Appendix I; texto en analisis/fuentes_txt/UrtonChu2015_suplemento.txt)
- TODO el sistema (UR266, 268, 269, 270, 272, 273A/B, 274A/B, 275, 276, 277, 278, 279) es UN SOLO montón de 14 quipus cubiertos de MANÍ en la esquina SO de la kallanka U.A.4 (sector A, unidad 20N, U.E. 11–22 consecutivas). UR271 estaba cubierto de frijoles en el centro de la misma sala. → Las 9 partes y los "bultos" son de MANÍ (encaja con n_almacenes: maní con cáscara, unidad por volumen).
- Orden de U.E.: 11 UR269, 12 UR266, 13 UR270, 14 UR273A/B, 15 UR274A/B, 16 UR278, 17 UR277, 18 UR268, 19 UR275, 20 UR276, 21 UR279, 22 UR272. (¿Orden de excavación = orden del montón? Por ahora sin relación evidente con la cadena; n pequeño.)
- Antecedentes en el suplemento que hay que CITAR: UR273B "#s similar to 1000s numbers on matching pair UR266 & UR275" (vieron el parecido cualitativo, no la suma A+B); UR274A valor fijo "30" y UR274B "17" (componentes de 30+17=47 ya anotados); UR278 "organized in sets of 9 cords"; UR266 "matches UR275". → H1 queda como "nuevo con antecedente cualitativo explícito (suplemento 2015)".
- Las copias UR255/UR256 (pila del corredor, sector C) reproducen a UR267A/B (canasta con ají, sector A, U.A.7): copias guardadas en otro edificio, como respaldo de archivo.
- De Espinoza Soriano 1971 solo se cotejaron las 19 páginas iniciales (introducción), sin las cuentas wanka. Los datos wanka están en Murra 2024 (n_murra_wanka).
- Hyslop 1985 y LeVine 1992: texto completo cotejado (analisis/fuentes_txt/).

## Rostworowski, *Costa peruana prehispánica* (coordinador, 05:00)
Texto en `analisis/fuentes_txt/Rostworowski_CostaPeruana.txt`.
- Lunahuaná (valle de Incahuasi): **4 guarangas, 8 curacas (2 por guaranga, ¿hanan/hurin?)** más el principal Lunaguanay (1534, AGI Patronato 119). Visita de 1577: 3276 almas, 740 tributarios; tasa de 1196 pesos de plata, 366 piezas de ropa, **500 fanegas de maíz** y 758 aves. Revisita de 1590: 474 tributarios. *(corregido después: ver «paquete_revision (Opus) listo y correcciones»)*
- Ningún curaca vivía en Incahuasi. Cieza dice que se abandonó tras la conquista de Guarco; Rostworowski propone que siguió como centro administrativo y tambo, y que lo construyó gente de mita de diversos lugares.
- Collique: una guaranga de **10 pachacas** con nombres que "pueden hermanarse de dos en dos".
- Changuco (costa norte): un testigo declaró un **año de 9 meses**; Rostworowski propone 9 meses × 40 días = 360 días, con semana de 10 días. Esto abre una hipótesis rival: las 9 columnas serían periodos, no pachacas.
- Sondeo propio sobre el orden de las columnas de UR278: adyacencia p = 0,022 en bruto, pero p = 0,16 con residuos fila × columna; igualdades exactas entre adyacentes 15/208 frente a 21/728 entre no adyacentes. Nivel: **especulativo**. Lo pongo a prueba en n_nueve_unidades (tiempo vs pachacas en pares vs 4×2+1), junto con n_rostworowski (lectura completa).
- n_saya_proporcional (terminado): no hay proporcionalidad rígida tipo wanka (sobredispersión 3,7×); no hay sayas 4+5 ni fracciones 2/9-3/9-4/9. La composición depende del tamaño del registro (elasticidades de 0,58 a 1,6). La capacidad de Inkawasi excluye unidades ≤ 30–40 L; la central es 82 L (IC90 51–127). *(corregido después: ver «Corrección de escala»)*

## Búsqueda de Chu y del valle de Cañete (coordinador, 05:10)
Texto completo cotejado de las fuentes siguientes.
- **Chu 2015 y 2017 (ushnu del sector E)**: el ushnu tiene **3 fases constructivas**, y Chu afirma que la ocupación fue "mucho mayor al que los documentos coloniales mencionan". Hubo además una ocupación post-inca. En el ushnu aparece más cerámica Guarco que inca. Esto debilita el supuesto de la "base militar breve" (LeVine/Snead) y da margen a un archivo de varios periodos. Nivel: apoyado (arqueología publicada).
- **Christie 2017 (Cuadernos Qhapaq Ñan 5)**: al norte de los depósitos del sector A hay rejillas en el piso de cuadrados de 23×23 cm, unos 3510 por lado del pasadizo (Urton y Chu 2015, fig. 3). Serían las unidades estandarizadas de conteo.
- **Barraza, Areche y Marcone 2022 (Andean Past 13: 221–264)**, Huacones-Vilcahuasi: el centro administrativo de Guarco en el bajo Cañete, con depósito de ají, 11 quipus de algodón y una yupana en el piso (4 bloques de 5 filas × 8 hoyos). Los quipus son pequeños, de 2 a 9 colgantes, y no hay transcripción de valores. **Los quipus 8 y 9 tienen exactamente 9 colgantes.** Es un segundo archivo en el mismo valle; las cuerdas no están en OKR ni en KFG.
- Pendiente: conseguir Urton y Chu, "El archivo khipu de Incawasi: un almacén y centro contable del Estado Inka en la costa sur del Perú", y Rivas 2011 (sectorización).

## Urton 2017 (cap. 9), Urton y Chu 2018 (es) y Jiménez 2021: verificación de novedad (coordinador, 05:20)
Textos en `analisis/fuentes_txt/Urton2017_InkaHistoryInKnots.txt` (cap. 9 = líneas 1537–2433), `UrtonChu_ArchivoKhipuIncawasi_es.txt` (*Perú Prehispánico: un estado de la cuestión*, 2018) e `IdentificandoElites.txt` (tesis UNMSM, asesor Chu).
- **Novedad confirmada.** El capítulo 9 analiza la suma interna (UR268 con 208, UR275 con 47), las copias UR266≈UR275 (18/43 exactas y 8 cercanas), los pares atados UR255/256 y UR267A/B, y los paradigmas X/fijo/Y frente a X/Y/fijo. A UR270, UR273A/B, UR274A/B y UR278 solo los menciona en el apéndice, con las mismas notas del suplemento de 2015. El artículo en español no añade relaciones nuevas. **H1 (UR273A+B → libro), H2 (UR270 → UR278) y H3 (UR278 → UR266) siguen sin publicar.**
- **Antecedentes que hay que citar.**
  - Urton observa dos sumas sueltas entre UR266 y UR275: 1070 + 1217 = 2287, y 2106 + 1153 = 1653 + 1606 = 3259.
  - Corrección de error entre copias: UR267B tiene 152 − 10 = 143, y UR256 lo corrige a 153. Hay que contrastarlo con n_casi_aciertos.
  - Interpreta UR266/UR275 como posible doble entrada (débito y crédito).
  - Propone una ocupación de "probablemente medio siglo".
- **Errata de la fuente.** El montón del maní está en U.A. 05 en el texto del capítulo y en el artículo en español, pero en U.A. 04 en el apéndice y el suplemento. Las U.E. 11–22 y la unidad 20N son coherentes con U.A. 04.
- **Rejillas del piso.** En U.A. 07 hay paneles de 3 × 39 = 117 cuadrados de 23 cm; unos 30 paneles dan alrededor de 3510 cuadrados.
- **Fases (Chu 2018, citado en Jiménez 2021).** (1) Base militar contra Guarco; (2) "transformación radical": **centro provincial inca administrativo** con complejos nuevos; (3) reocupación post-inca. Los basurales indican ocupación continua. Esto apoya un archivo de fase 2 con varios periodos y unidades administrativas locales. Nivel: apoyado.
- **Cinco quipus más del sector B** (PAI-2016-1 a 4 y 1464), en una residencia de élite local, posiblemente guarco. Son más pequeños, varios están sin terminar y no hay valores publicados.
- Pendiente: conseguir Chu 2016 ("Resultados preliminares de la temporada 2013", Actas del I Congreso Nacional de Arqueología); Chu 2018 (dos artículos en *Boletín Yungas*); Carhuanina 2018; Casaverde y López 2011.

## Prueba ciega con Opus (quipu_ciego3, puntuada por el coordinador, 05:30)
Mismos datos anonimizados y las mismas 597 cuerdas ocultas que las corridas de DeepSeek Flash. Puntuación guardada aparte (sellado/puntuacion_quipu_ciego3.csv).
- **Predicciones: 68 cuerdas (11,4 %), 56 exactas (82,4 %).** Confianza alta: 21/23 (91 %; el modelo esperaba 92 %). Media: 35/45 (78 %; esperaba 71 %). Base de la moda: 14,4 %. Flash dio 33/45 (73 %) y 35/46 (76 %). Opus está **bien calibrado** y cubre algo más.
- **Redescubrió H2 a ciegas.** Q21↔Q29 = **UR270 ↔ UR278**, celda a celda, con **colgante + subsidiaria**, separadores alineados y p ≈ 3e-10. Es la primera confirmación independiente de H2: el agente no conocía nuestro resultado, ni la regla P+S1, ni la identidad de los quipus. Nivel de H2: sube de apoyado a **bien apoyado** (replicación ciega).
- También encontró: UR275 → UR266 (los totales de grupo de UR275 reaparecen como colgantes de UR266, en orden; p ≈ 1.6e-7), UR256↔UR267B reordenada, UR255↔UR267A con 15, y las cuotas 47/15/10/208/30/17.
- **No encontró H1** (A+B → libro: "No sums of two quipus appearing in a third") **ni H3** (UR278 → UR266). Ninguna de las tres corridas ciegas halló H1. Su evidencia depende de la regla de alineación (por número de grupo sin saltar vacíos), elegida con conocimiento previo, y en el equipo rojo quedó en p = 0,015. **H1 baja a apoyado, frágil.** Conviene una prueba ciega dirigida: darle la regla de alineación a un agente nuevo y pedirle solo sumas de dos quipus en un tercero.
- ¿Las fallas se deben al modelo (DeepSeek Flash)? **En parte**: Opus halló H2 y Flash no. Pero H1 no aparece con ningún modelo.

## Prueba dirigida A+B (Opus ciego, 05:35) y tareas terminadas
- **Prueba dirigida A+B.** Regla fija: alineación por grupo, P+S1, separadores PK; 132 600 triples ordenadas; 60 nulos por triple. **Ninguna triple sobrevive a Holm** (la menor p corregida es 0,93). Pero las triples **UR273A+UR273B → UR275** y **→ UR266** quedan **8.ª y 9.ª de 132 600** (4 frente a 0,40 esperados, y 5 frente a 0,70; p crudas 8e-4). Son el par físico mejor clasificado. Post hoc: 6 sumas ≥ 1000 caen en totales de grupo de UR275/UR266 (808+2142 = 2950, 453+1200 = 1653, 448+1332 = 1780, 672+1575 = 2247, 509+1256 = 1765, 325+1181 = 1506) frente a 0,49 esperadas (p ≈ 5e-4). **Veredicto sobre H1: apoyado, no bien apoyado.** El agente ciego llega al mismo par y a los mismos libros, pero solo como pista; con una búsqueda genérica sobre todo el corpus no resiste la corrección. Para demostrarla haría falta un dato nuevo: un quipu con otro par A/B, o la verificación de las cuerdas en museo.
- **n_tanteo.**
  - Sobreviven en la mitad de confirmación: (1) UR275 como depósito repartido, cabecera = cuota + destinos (15/16); (2) **las 9 partes de UR278 son proporciones estables que predicen filas no vistas** (Holm 0,002); (3) una cuota fija, no un 2 % (la tasa va de 1,1 a 3,7 %).
  - Negativo: no hay dinámica de saldo en UR273/274 (0/63).
  - La escalera de copias se debilita, porque 2633 aparece también en UR269.
  - UR277 y UR272 son listas de conteos pequeños.
- **n_hyslop.** Inkawasi no tiene plantilla de 9: se divide en mitades y 4 suyus, y ningún conteo arquitectónico cuadra con el 9. Capacidad corregida: 6400 m³ es el piso del sector A, y el total plausible es 8300–13 000 m³. U.A. 4 confirmado. Entre 1000 y 2000 residentes.
- **n_murra_wanka.** La regla "proporcional a la población de cada saya" no está en Murra 2024 (es de LeVine) y no se puede contrastar. El registro wanka (12 categorías × 19 eventos) es lo opuesto de Incahuasi. El "quipu de 43 cuerdas" de Murra no puede ser literal, porque el cuadro tiene 361 números. Ningún quipu del corpus corresponde al Mantaro.

## Ronda 12 (05:45): quipus no numéricos por tanteo controlado, agronomía, lingüística
- **n_plantillas** (Opus): tantear el GÉNERO de los quipus con una biblioteca de plantillas sacadas de documentos coloniales dictados de quipus (censo por "calles" de edad, consolidación jerárquica, libro de almacén, tributo en orden fijo, calendario 12×30 y 9×40, ceques 41/328, genealogía, padrón). Las plantillas se congelan antes de mirar el corpus. Controles positivos: Incahuasi, Puruchuco, Santa. Mitades de exploración y confirmación, con corrección por todas las variantes.
- **n_descifrado_lm** (Flash): desciframiento silábico al estilo ugarítico (modelo de lengua quechua o aymara a partir del manuscrito de Huarochirí) sobre los quipus no numéricos. Controles obligatorios: quipus numéricos, versiones barajadas, secuencias aleatorias y un control positivo (quechua real con cifrado aleatorio).
- **n_linguistica** (Flash, con web): léxico contable, unidades de carga, clasificadores numerales mochica (nassop), sílabas y listas de nombres.
- **n_agronomia** (Flash, con web): calendario del maní, el ají y el frijol en la costa sur; rendimientos; conversión de 61 790 unidades a hectáreas y tributarios; ¿9 periodos o 9 chacras?
- **Prueba dirigida de H3** (Opus ciego): ¿las filas de 9 de algún registro suman a valores de otro?

## Pruebas dirigidas sobre datos completos anonimizados (Opus ciego, 05:55): H3 BIEN APOYADA
Las reglas, los nulos y las correcciones Holm se congelaron antes de mirar. El agente no conoce la identidad de los quipus.
- **H3 sobrevive con fuerza.** Las filas de 9 de Q29 (UR278) suman a valores de Q44 (UR266): 11 aciertos frente a 0,4–0,5 esperados, **Holm p = 1,6e-9**. También a los totales de grupo de Q35 (UR275): 7 frente a 0,5, Holm 2,8e-4. Los aciertos están **en el mismo orden** (rho = 1,0; post hoc 1/11! ≈ 2,5e-8). Ejemplos: 3618, 1506, 1384, 2919, 2089, 1842, 1876, 2229, 4273, 2950, 1278.
- Es una **consolidación de tres niveles**: UR278 → totales de UR275 → colgantes blancos de UR266. Las cuerdas destino reveladas son ≤ 15 %, es decir, al nivel del azar, así que los aciertos no dependen de los valores antes ocultos.
- **Nivel de H3: bien apoyado.** El agente la encontró a ciegas, con una regla preespecificada y corrigiendo por todos los pares T × C. Salvedad: elegí la familia "tablas de 9" sabiendo que existía UR278, aunque solo 2 registros la cumplen, así que la multiplicidad es baja.
- **H1 (UR273A+B) sigue sin sobrevivir a Holm sobre las 132 600 triples** (la mejor p cruda es 7,4e-5 y el umbral es ~3,8e-7). Pero Q12a/Q12b ocupan **4 de los 5 primeros puestos** de 132 600, con destino UR275 y UR266. Post hoc: 7 sumas ≥ 1000 caen en los mismos totales que las filas de UR278 (p empírica ≈ 5e-4).
  - Con la familia natural "pares atados físicamente → registros" (3 pares × 2 órdenes × 51 = 306 pruebas), 7,4e-5 × 306 ≈ 0,02. Pero esa familia también se define después de los datos.
  - **Nivel de H1: apoyado (fuerte); no bien apoyado.** Converge con H3: A+B y las filas de UR278 caen en los MISMOS totales (2950, 1506…), es decir, son dos vías al mismo libro.
- Resumen del sistema: **UR270 → UR278** (bien apoyado, ciego) → **UR275/UR266** (bien apoyado, ciego dirigido); **UR273A+B → UR275/UR266** (apoyado); copias y cuotas (publicadas).

## Pärssinen y Kiviharju 2004 (introducción) y Curatola y de la Puente 2013 (05:58)
Textos en `analisis/fuentes_txt/Parssinen2004_TextosAndinos_parcial.txt` y `Curatola2013_ContarConcertando.txt`. Pasados al agente de plantillas.
- **Plantilla nueva, el "libro segmentado por eventos".** La Memoria de Guacrapaucar (1558) son series de la misma lista de categorías, cada una abierta por una frase de evento ("cuando el marqués fue a Bombón"). Las categorías van por color ("plantas cultivadas", "provincias") y hay cuerdas suplementarias. Es un esqueleto narrativo dentro de una contabilidad, y lo que predice en las cuerdas es medible.
- **Plantilla de lista de conquistas e itinerario:** una "Memoria" que sale de un quipu coincide con Sarmiento en el orden de fortalezas y provincias.
- Pärssinen sugiere que el cordón principal podría marcar el género del quipu (mit'a, censo, historia).
- Falta el tomo de documentos. Los prioritarios son el doc. 1 (conquistas), el doc. 5 (Guacrapaucar), el doc. 8 (ganado de Chucuito) y el doc. 12 (Chayanta 1568).

## Quipus modernos como piedra de Rosetta (06:05)
- OKR y KFG casi no tienen quipus modernos o etnográficos; solo hay notas que remiten a Mackey 1970.
- Lancé **n_quipus_modernos** (Flash, con web). Reúne quipus de los siglos XVII al XX con clave conocida: los pastores de Mackey y Núñez del Prado, Tupicocha y Rapaz (Salomon), Anchucaya y Collata (Hyland), el chinu boliviano. Extrae sus convenciones (color = clase de bien, subsidiaria = cría o subcategoría, torsión = mitad, objeto atado = pérdida…) y las prueba en el corpus antiguo con nulos.
- La base OKR es `data/external/open-khipu-repository/data/khipu.db`.

## Ronda 13: materiales, nueve unidades, Rostworowski, agronomía; Hyland 2017 (05:50)

Verificado por el coordinador sobre los datos: unión R/V, Friedman, Spearman, texto de los guancayos.

- **La unión R/V es un código, no manufactura (bien apoyado en Incahuasi).** UR273A: 83 V / 0 R; UR273B: 113 R / 1 V; UR267A: 82 V; UR267B: 103 R. Las dos mitades de cada obra llevan unión opuesta. Por eso la unión no sirve como firma de mano. Resto de n_materiales: la manufactura identifica lotes o depósitos, no artesanos; la firma de 4 ejes no identifica (15,4 % de pares idénticos, igual al azar); las copias reproducen contenido, no gesto técnico. *(corregido después: ver «Quipus modernos, Narrative Threads y lingüística»)*
- **9 columnas de UR278 = lista fija de 9 subunidades desiguales, ordenadas de mayor a menor (n_nueve_unidades).** Friedman p < 1e-15; Spearman con la posición −0,73 (p = 0,025). Se descarta el tiempo: no hay estacionalidad ni autocorrelación, y n_agronomia tampoco encuentra calendario de cosecha que encaje (CV 0,17 frente a 1,2–2,0 predicho). Hay emparejamiento: el mejor de 945, (1-2)(3-6)(4-9)(5-7) + c8, tiene p = 0,002, aunque solo el par (1,2) es robusto.
- **Ancla textual (Rostworowski, líneas 369–371 y 2601).** Los guancayos del Chillón tenían **9 pachacas bajo 5 señores: uno con una pachaca y cuatro con dos (1 + 4×2)**, y tributaban 5 cestos de coca por pachaca (45 en total). Es exactamente la estructura de «4 pares + 1 suelta» que el test de emparejamiento favorece. **Propuesto:** las 9 columnas son pachacas, y los pares, pachacas bajo un mismo señor. En Lunahuaná no hay un 9 documentado (4 guarangas, 8 curacas). *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
- **Tributo colonial = cuota fija por cabeza (Rostworowski 1577/1590):** 0,5 piezas de ropa y ~1 ave por tributario, estables aunque la población cae 36 %. Es coherente con la cuota 47 absoluta (1,1–4,2 % del registro, no un 2 %).
- **Escala agronómica (bulto de 82 L = 23,5 kg de maní en vaina).** UR278 equivale a ~1 450 t, ~1 450 ha y 966–1 932 tributarios-año. Cabe en la mano de obra de 4 guarangas, pero no en las tierras del tramo de Lunahuaná: el maní venía del valle bajo o de varios valles. Cada columna equivale a ~160 ha y 100–160 hogares, tamaño de pachaca. Las cuotas 47 y 208 son demasiado pequeñas para ser maní provincial. *(corregido después: ver «Corrección de escala»)*
- **Prueba de Hyland (Collata, 2017: 95 símbolos de color × fibra × torsión en 487 colgantes, frente a 12 en un quipu contable moderno).** Corpus antiguo, solo color normalizado × torsión, rarefacción:
  - mediana de 13,8 tipos por cada 100 cuerdas;
  - ningún quipu antiguo llega a 95 tipos con 487 cuerdas (máximo UR093 = 75; KH0083 = 71);
  - por cada 100 cuerdas, los más ricos son UR207 (44), UR114 (34), **UR215 (34, candidato no numérico)**, QU011 y JC011.

  **Apoyado (negativo):** ningún quipu antiguo tiene el inventario de una epístola de Collata sin contar la fibra, que es la variable que el corpus antiguo no registra de forma fiable. **Trampa de datos:** los colores segmentados llevan rangos en cm («AB(0.0-14.0)/W(…)»). Sin normalizarlos, MM021 parece tener 119 símbolos. Esto se avisa en todas las tareas nuevas.
- **Nuevas fuentes extraídas:** Salomon 2004 *Cord Keepers*, *Narrative Threads* 2002, Pärssinen 1992 *Tawantinsuyu* y Hyland 2017. Tareas lanzadas: n_salomon (claves de Tupicocha probadas en el corpus antiguo), n_narrative_threads (todas las hipótesis de 2002 contra los datos de hoy, más la búsqueda de pares con unión opuesta en todo el corpus) y n_parssinen (firma de 9 partes frente a listas coloniales ordenadas).

## Fuente primaria de los guancayos y desciframiento por tanteo (05:58)

- **Espinoza 1963** (Revista del Museo Nacional XXXII, en `fuentes_txt/RMN_XXXII.txt`) transcribe la visita de Martínez Rengifo de 1571, la misma fuente que usa Rostworowski. Lo comprobé en el texto (líneas 729–761 y 1180–1194):
  - 900 tributarios en **9 pachacas de 100**;
  - curacas en estructura **1 + 4×2**: el curaca de la guaranga rige 2 pachacas, otros tres rigen 2 cada uno y uno rige 1;
  - **cada pachaca entrega la MISMA lista de 9 productos** (5 cestos de coca, 26 piezas de ropa, 2 trajes de cumbi, 3 fanegas de maíz, 4 cestos de ají, 20 pares de ojotas, 10 petacas de charqui, 3 de guabas y 1 manta).

  **Consecuencia:** una TASA por pachaca daría filas de 9 valores iguales. UR278 tiene columnas desiguales (CV 0,17–0,28), así que registraría ENTREGAS u otra magnitud, no la tasa. La excepción son las filas planas de la fase 1: hipótesis «tasa frente a entrega». Las columnas no pueden ser los 9 productos, porque las proporciones de la lista (5:26:2:…) son mucho menos parejas que las de UR278. Tarea n_espinoza1963 lanzada.
- **n_descifrado_lm terminó: ninguna lectura** (0 de 84 combinaciones de quipu y alfabeto pasan el criterio conjunto).
  - **Hallazgo sólido a priori:** los quipus no numéricos tienen alfabetos de color de mediana 5 y máximo 19, muy lejos de los 60–120 de un silabario.
  - **Trampa evitada:** «mejor que barajado» premia al quipu numérico UR278 (z = 14,4); mide rigidez, no lengua.
  - **Control positivo:** el método no recupera un cifrado de quechua real con n ≤ 100, así que el negativo significa «no detectable», no «no hay lengua».
  - **Siguiente paso:** concatenar quipus del mismo género o usar la jerarquía madre–subsidiaria como gramática. Auditar si los 46–80 signos de UR203/UR215 son reales.
- **Mackey 1970:** solo se cotejaron la introducción y parte del cap. I (unas 20 páginas). Pendiente: los capítulos sobre los quipus modernos.
- **Resumen de Mackey en *Narrative Threads*.** Su capítulo 13 (2002, pp. 320–347; `NarrativeThreads2002.txt`, líneas 3616–4130), «The Continuing Khipu Traditions», resume la tesis de 1970 con su muestra de 19 informantes:
  - **tres tipos:** A, parecido al inca, 21 %; B, hilo doblado, 70 %; C, cuerda única, 9 %;
  - **seis principios numéricos:** el central es «la posición del nudo da el valor»; son innovaciones el grosor del nudo y los racimos de 10 para el 100;
  - **subsidiarias de crin de caballo que suman o restan al total**; en el quipu de ovejas de la figura 13.3 son los MUERTOS de cada categoría;
  - **hilos de colores como separadores;**
  - **orden fijo de categorías de rebaño:** machos, hembras con cría, hembras sin cría, machos jóvenes, castrados;
  - **orden jerárquico de productos** (chuño, maíz blanco, maíz amarillo…), estable para cada usuario pero no entre quipus del mismo usuario.

  Conviene probar en el corpus antiguo si las subsidiarias forman una fracción pequeña y estable de su colgante (tasa de pérdida) en quipus de rebaño. También hay un artículo sobre un quipu etnográfico aymara en `QuipuYTocapu.txt` (cerca de la línea 4736).

## Salomon y Pärssinen (06:05)

- **n_parssinen: la lista colonial más parecida a las 9 columnas es la de las 9 pachacas de la guaranga de Bambamarca** (Cajamarca, visita de González de Cuenca de 1567; Pärssinen 1992, tabla 2). Tributarios por pachaca: 104, 75, 78, 68, 49, 75, 67, 30 y 27, con el cacique principal primero. Verificado en el texto, ρ con la posición = −0,87 (p = 0,002). Es la única de 9 listas coloniales que desciende; las demás ordenan por prestigio y no por tamaño (mediana ρ = −0,29). Bambamarca es más desigual que UR278 (CV 0,39 frente a 0,19). El censo lupaca de 12 sayas muestra que un censo leído de un quipu puede ser tan plano como UR278 (CV 0,20). Se descarta la estructura 3×3 (p = 0,19). **Apoyado:** la firma de 9 partes se parece a una lista de pachacas reales ordenada por rango. **Especulativo:** el mapeo a los 5 señores de Guancayo, aunque c8, la suelta del mejor emparejamiento, es la columna más pequeña, como la pachaca única.
- **n_salomon:** Salomon no descifra ningún quipu. Transportado al corpus antiguo:
  - **Cuerdas sin nudos:** aparecen en bandas (0,81 de las rachas esperadas; q < 1e-50). Encaja la lectura «blanco = cuenta saldada»; la de «casilla vacía» no.
  - **Torsión:** no es un código general (90 % S; solo 4 quipus mezclan de verdad, y en bloques).
  - **Color de las subsidiarias:** coincide con el de la madre más de lo esperado, al revés que en Tupicocha.
  - **Cuerda de cabeza que suma su grupo:** 2,96 % de los grupos frente a 1,77 % esperado, z = 5. Tupicocha no tiene esta convención; es una diferencia, no una continuidad.
  - **15–16 bandas:** el número de Tupicocha es demografía local, no una firma andina.

## 20_categorias: ¿categorías en vez de lengua? (coordinador, 06:30)

Pruebas hechas por el coordinador; scripts en `analisis/20_categorias/`. Colores normalizados, sin rangos en cm.

- **No hay un léxico de color compartido.**
  - El orden de los colores (posición media relativa) no se parece más entre quipus del mismo sitio que entre sitios: 6 906 pares, Δτ = 0,007, p = 0,34; sin copias, p = 0,43.
  - Las secuencias de color de grupo repetidas entre quipus no superan el nulo de orden barajado dentro del grupo: 48 frente a 50, p = 0,79.

  Esto confirma la línea 47: sin frases compartidas.
- **Dentro de cada quipu, el color sí marca clase.** El color predice la magnitud del valor en 167 de 403 quipus (q < 0,05, frente a ~20 esperados; η² mediano 0,16). En 103 se sostiene aun barajando el color dentro de cada grupo, lo que descarta un simple efecto de grupo o posición. **Bien apoyado:** el color funciona como categoría con clave local, propia de cada quipu o archivo. *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
- **Modelo «formulario local» (apoyado).** Números universales, con la gramática decimal. Categorías marcadas por color y posición dentro de un formulario cuya clave es local. Lo apoyan:
  - alfabetos de 5–19 colores;
  - la ausencia de léxico compartido;
  - formularios propios de cada archivo (Santa, Leymebamba, Incahuasi);
  - el R/V como código de archivo; *(corregido después: ver «Quipus modernos, Narrative Threads y lingüística»)*
  - la etnografía (Mackey: orden propio de cada usuario; Tupicocha);
  - la forma «categoría + número» de las transcripciones (Medrano).

  **Se refutaría** si una misma secuencia de color con el mismo significado apareciera en dos archivos sin relación.
- **Nudos como signos: negativo.** 3 000 de 40 162 cuerdas rompen la regla decimal (2 681 con varias unidades, 319 con la unidad que no va al final). *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
  - Sus formas de nudo no forman un vocabulario compartido entre quipus (300 frente a 321, p = 0,97).
  - Color y forma de nudo se asocian en solo 3 de 55 quipus, y uno es UR278, que es numérico.
  - El nudo fuera de lugar no tiene una dirección distinta (21 % frente a 22 %).
  - Sobre color + nudo como signo: n_descifrado_lm ya mostró que su inventario (hasta 80) no separa lo no numérico de lo numérico (UR266 = 46).
- **Familia UR050–UR055 (camélido, canutos, nudos largos de 2–9 vueltas): tabla dentro de la cuerda.**
  - 87–99 % de sus cuerdas rompen la regla decimal; la mediana del corpus es 5 %.
  - **UR050:** 146 de 163 cuerdas tienen exactamente 3 cuentas, a alturas fijas (14,8, 30,2 y 55,4 cm), con efecto de zona (Friedman p = 3e-6). *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
  - **UR054 y UR055:** 2 zonas que se compensan, con la suma por cuerda más constante que al barajar (p = 0,0002 y 0,002; Holm sobre 5 = 0,001 y 0,011). Es el reparto de un total entre dos categorías. *(corregido después: ver «UR053A–E como archivo y réplica de zonas»)*

  Es el subtipo B1-b de Mackey: varias cuentas separadas en una misma cuerda, en quipus de pastores. **Apoyado (exploratorio):** las zonas se eligieron por BIC sobre las alturas. **Propuesto:** registro de rebaño o de reparto en dos o tres categorías por unidad (machos/hembras, con/sin cría). Prueba siguiente: alturas relativas al largo de la cuerda y réplica en UR052/UR051 y en los tally puros de Leymebamba y Armatambo. *(corregido después: ver «27_familia_z (Sonnet)»)*

## Quipus modernos, Narrative Threads y lingüística (06:25)

- **CORRECCIÓN del R/V (n_narrative_threads).** Las tres parejas A/B de Incahuasi tienen unión opuesta, pero en el corpus solo 6 de 14 pares A/B la tienen opuesta, frente a 28 % por azar (p = 0,16; Fisher contra pares del mismo sitio p = 0,58). Bajo de «bien apoyado» a **«convención de archivo propuesta»**. Sigue apoyado que los pares A/B son mitades de una misma obra (Jaccard de valores 0,53 frente a 0,27). n_linguistica: la unión es el marcador de GRUPO más fuerte del corpus (segregación 0,43; Holm 0,010).
- **n_quipus_modernos:**
  - Solo Cutusuma publica una tabla cuerda por cuerda (7 cuerdas): la Rosetta moderna es mínima.
  - Las convenciones modernas «torsión = mitad», «subsidiaria = cría proporcional» y «Z vale menos» NO están en el corpus antiguo: son innovaciones coloniales o modernas. La torsión marca secciones (bloques, z = −13,5) y no mitades.
  - **La dirección del nudo es la señal no numérica más fuerte:** 96,5 % de las cuerdas con varios nudos son puras S o Z (nulo 61,9 %), concentradas por grupo, y las Z valen más (+0,40 en log). Es un eje de sección o categoría independiente del color y de la torsión. Pendiente: control de transcripción con imágenes.
  - Ninguna fuente dice que un objeto atado signifique pérdida: no hay que repetirlo.
- **n_narrative_threads:**
  - El «código de 7 bits» de Urton no existe como alfabeto: unos 1–2 bits efectivos por cuerda.
  - El color es sintaxis local (bandas, cordón principal que anuncia la paleta) y su relación con el valor cambia por sitio (p = 0,0005).
  - Grupos de 5/6/10 no son regla.
  - Cuerda superior = total: 26 de 76 frente a 15,5 % (p = 0,0002).
  - **Subclase con nudos largos de 10–20 vueltas, imposibles en decimal:** 198 cuerdas en 39 quipus; candidatos UR193, KH0001 y AS090_N2. Coincide con el ranking de cuerdas fuera de regla de 20_categorias, donde los tres tienen 72–75 % de cuerdas no decimales. *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
- **n_linguistica:**
  - Hay 4 series de clasificadores mochica (Carrera 1644: monedas, personas/animales/cosas, frutos, días).
  - Combinaciones por quipu de color, torsión y unión: mediana 5, y solo 1 de 415 llega a 20.
  - En Huarochirí, 26 sílabas CV cubren el 90 % del texto: un silabario es viable en principio, pero no está en el KFG.
  - Control importante: el castellano da más información mutua que el quechua, así que entropía e información mutua no prueban lengua.
  - Su advertencia (η² del color confundido con el nivel de la cuerda) no afecta a 20_categorias, que usó solo colgantes de nivel 0 y barajó dentro de cada grupo.

## n_plantillas (Opus) terminó (06:35)

- **El método funciona: reconoce los archivos ya leídos.**

  | Control positivo | Reconocidos | Detalle |
  |---|---|---|
  | Padrón del Santa 1670 | 5 de 6 | |
  | Consolidación de Puruchuco | 4 de 6 | Incluye la discrepancia 2908/2904 |
  | Calendario UR006 | 1 de 3 | |
  | Ceques UR053C | 1 de 2 | |
  | Almacén UR275 | 1 de 3 | |

  Se fijaron 30 plantillas antes de ver los datos y se corrieron 11 475 pruebas en mitades de exploración y confirmación.
- **Géneros coloniales en el resto del corpus: ninguno supera la tasa base.**
  - No aparecen: calles de edad, censo toledano, lista dinástica, cuenta en pesos, calendario de días.
  - Clase no numérica: 0 de 11.
  - El par de ceques UR050 + UR055 = 344, prerregistrado, falla sus 3 predicciones.
  - Ningún agrupamiento por museo se replica en la mitad de confirmación tras Holm. Berlín en P11a: Holm 0,65.
- **UR053A–E (conjunto atado, Banco Central): formulario tripartito W–R–AB. Apoyado; verificado por el coordinador.**
  - En los tríos W–R–AB (R = cualquier rojo), la W es la mayor en 13 de 14 (UR053A) y en 23 de 23 (UR053D).
  - El reparto es **el mismo en tres quipus de escalas muy distintas**:

    | Quipu | Reparto W / R / AB | Total medio del trío |
    |---|---|---|
    | UR053A | 0,65 / 0,19 / 0,16 | 2 421 |
    | UR053C | 0,59 / 0,25 / 0,16 | 71 |
    | UR053D | 0,66 / 0,16 / 0,18 | 178 |

  - No es una suma: ningún caso cumple W = R + AB.
  - Es el mismo fenómeno que las 9 partes de Incahuasi: un formulario de archivo con proporciones estables entre registros. Es la segunda instancia independiente del modelo «formulario local».
- **Propuestos:**
  - UR1140 (Berlín, Nazca): ficha de 7 campos ordenada por posición en la banda (Holm 0,005).
  - 8 quipus con bloques de perfil repetido (UR1131, UR1175, UR1144, UR1149, UR1099, AS178, AS048, UR172): 6 de 8 en Berlín y 4 de Pachacamac. Sin control positivo; no distingue eventos de unidades.
- **Siguiente:** leer UR053A–E como archivo, es decir, ver si C y D son partes de A; probar la ficha de UR1140 en los demás quipus de Nazca de Berlín.

## UR053A–E como archivo y réplica de zonas (coordinador, 06:50)

Scripts: `analisis/21_ur053/alinear.py` y `analisis/20_categorias/zonas_relativas.py`.

- **UR053B ↔ UR053C es una copia YA CONOCIDA**, registrada en `14_copias` como familia replicada. n_plantillas se equivocó al decir «no son copias»: comparó por posición, y C desplaza la alineación.
  - Alineando tríos (W, R ±1): 12 tríos comunes frente a 5,5 por azar (p < 0,001). AB coincide (±1) en 10 de 12.
  - **Cambio de formato:** en B, AB es SUBSIDIARIA de la cuerda roja; en C es un colgante propio. El mismo dato se escribe en dos formatos.
  - A y D no se alinean con nada: son otros registros del mismo formulario.
- **Los 5 quipus del juego reparten W / R / AB en proporciones parecidas:**

  | Quipu | W / R / AB | Total |
  |---|---|---|
  | UR053A | 0,70 / 0,17 / 0,13 | 36 800 |
  | UR053D | 0,66 / 0,16 / 0,18 | 4 160 |
  | UR053C | 0,61 / 0,23 / 0,16 | 1 415 |
  | UR053E | 0,64 / 0,18 / 0,18 | 1 260 |
  | UR053B | 0,57 / 0,26 / 0,17 | 1 200 |

  El reparto es cercano a 4:1:1 en cinco registros cuyo total varía 30 veces. Fila a fila no es exacto (CV de la parte W de 0,11 a 0,31). **Apoyado:** formulario de archivo con clave de reparto estable, como las 9 partes de Incahuasi. Curiosidad sin valor de prueba: en UR053B, W + R = 1000 exactos. *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES» y «26_clave_local (Opus)»)*
- **CORRECCIÓN de la familia UR050–055 (altura relativa al largo de la cuerda).**
  - **Solo UR050 se sostiene:** 3 zonas en 0,20, 0,41 y 0,75 del largo, con ΔBIC 306 frente a un máximo de 120 en el nulo de alturas uniformes. Coincide con las zonas en cm. *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
  - En UR051, 052, 054, 055 y 110 las zonas no superan el nulo uniforme. La «compensación» de UR054/UR055 (p = 0,0002 y 0,002 con zonas en cm) desaparece con zonas relativas (p = 0,76 y 0,44). **Queda retirada.**

  Lo que se mantiene: UR050 es una tabla de 163 filas × 3 columnas de un dígito (1–9), compatible con el subtipo B1-b de Mackey. *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*

## Espinoza 1963 y Salas 2025 (06:55)

- **n_espinoza1963.**
  - **La visita es del Chillón y no de Huancayo:** «río de Collique», línea 3385, verificada. Rostworowski tiene razón.
  - **Errores de Espinoza:** Maca tenía 190, no 170; la visita lista 12 rubros, y el «9 productos» es una selección editorial que no es plantilla nativa. Se mantiene: 900 tributarios, 9 pachacas de 100, curacas en orden **2+1+2+2+2** (Mongoy 2, Cancay 1, Chuquitanga 2, Chumbillán 2, Antachumbi 2).
  - **Predicción con orden documental, externa a los datos:** pares (1-2)(4-5)(6-7)(8-9) + c3 suelta. En UR278 esos pares suman **11 igualdades exactas**, frente a 4 en los otros cuatro pares adyacentes; verificado por el coordinador sobre 26 filas. p = 0,0003 frente a emparejamientos al azar; sin filas planas, 7 y p = 0,006. **Pero** no hay covariación (r = 0,09), y como máximo sobre 945 emparejamientos da p = 0,086. **Apoyado, frágil.** Nota: se superpone con el exceso de igualdades entre columnas vecinas ya conocido. *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
  - **«Tasa frente a entrega»:** solo 2–3 filas planas reales; la mezcla queda **propuesta**. Pista nueva: en UR270, el colgante P tiene 22 igualdades (100/200 en el grupo 6) y S1 es irregular. Hipótesis: **P = cuota, S1 = entrega**, y UR278 suma las dos. *(corregido después: ver «Ronda 14: resultados y DEGRADACIONES»)*
  - **Grupos de 9 valores iguales:** 5 en el corpus frente a 1,2 esperados (p = 0,0001), pero son constantes simples. Ningún quipu tiene la forma de la tasa de Guancayo.
- **n_salas2025.**
  - Hay 0 quipus de la costa norte (yunga) con procedencia conocida, así que no se puede comparar.
  - **Paridad:** sin exceso de pares global, excluyendo unidades 0. Hay quipus «de doses» aislados (UR037, MM019, AS036, UR216) sin asociación con color ni procedencia.
  - Los múltiplos de 10 y 100 son redondez decimal, no clasificador.
  - **Robusto:** los cambios de color caen en fronteras de grupo (+9 pp, Holm 0,027; 59,5 % de quipus positivos). El color marca tramos o secciones.
  - La posición no codifica magnitud.
  - El calendario de «cuerda = día» no aparece.

## Ronda 14 lanzada (07:05)

- **DeepSeek Flash:**
  - n_cuota_entrega: en Incahuasi, ¿P = cuota y S1 = entrega?
  - n_nudos_imposibles: los 39 quipus con nudos largos de 10–20 vueltas.
  - n_ur1140_nazca: la ficha de 7 campos en Nazca, Berlín y el Santa.
  - n_rojo_formulario: equipo rojo contra 20_categorias, UR053, UR050 y los pares 2+1+2+2+2.
- **Opus:**
  - 22_formularios: detector congelado de «formulario con clave de reparto» en todo el corpus, con controles Incahuasi y UR053 y la prueba que refutaría el modelo.
  - paquete_revision: resumen para un especialista, predicciones verificables, tabla de hallazgos y antecedentes. Sin contacto externo en esta fase.

## paquete_revision (Opus) listo y correcciones (07:20)

- **Entregado en `analisis/paquete_revision/`:**
  - resumen para especialista, de unas 6 páginas;
  - 26 predicciones verificables, con las más baratas primero;
  - `tabla_hallazgos.csv` (51 filas);
  - `antecedentes.md`;
  - `verificar.py`: 9 de 9 cifras clave recalculadas desde KFG; corrido por el coordinador.
- **Correcciones que se adoptan:**
  - **UR053, antecedente.** Urton 2017, cap. 8 (líneas 1266–1490 del txt; verificado), ya publica:
    - el patrón W/RL/AB en los 5 quipus del conjunto atado;
    - la correspondencia UR53B ↔ UR53C (tabla 8.1);
    - la unión R/V de ambos.

    **Lo nuevo es solo el reparto estable (~0,6–0,67 / 0,16–0,26 / 0,15–0,18) entre 5 quipus cuyos totales varían 30 veces;** Urton no halló relación numérica entre los otros tres. Cifras canónicas, según `verificar.py`, por color sobre colgantes y subsidiarias: A 0,67/0,18/0,15; B 0,57/0,26/0,17; C 0,61/0,23/0,16; D 0,66/0,16/0,18; E 0,64/0,18/0,18. La versión anterior de A (0,70/0,17/0,13) contaba solo colgantes.
  - **UR274B:** las 4 cuotas «10» están entre las 5 cuerdas más cortas, no son «las 4 más cortas»; p ≈ 0,003 en vez de 5,5e-4.
  - **Barras de madera (AS124, AS136, AS140):** no es nuevo; Urton 2017, cap. 7, describe entre 12 y 15 quipus en barras.
  - **Lunahuaná:** vale la lectura de n_rostworowski: el curaca principal está entre los 8. No hay un «8 + 1» documentado.
  - **Cifras canónicas:**
    - UR278 → UR266: 11 totales exactos en orden;
    - CV de las medias de columna de UR278: 0,173 (24 filas);
    - Friedman: p = 0,0002 por permutación; el p < 1e-15 es el paramétrico.

## 22_formularios (Opus): el modelo de formulario local en todo el corpus (07:50)

El diseño se congeló en `analisis/22_formularios/diseno.md`, con 5 desviaciones declaradas. La principal: se pasó de p paramétrico a permutación porque el paramétrico falló el control negativo.

- **Controles:**
  - positivos: 5 de 5 (UR053A/C/D cromáticos; UR278 y UR270 posicionales con grupos de 9);
  - valores barajados: 0 detecciones;
  - colores barajados: 3–5 falsos frente a 73 reales.
- **Tasa:** 150 de 410 quipus con ≥30 cuerdas (36,6 %) tienen un formulario detectable. En 69 (16,8 %) la clave es el color y en 83 (20,2 %) los bloques coescalan. **Apoyado:** el formulario es un rasgo frecuente, no una rareza.
- **Formularios de archivo confirmados (BH): 20. Locales bien apoyados: 4** (UR053A–E, UR267A/B, UR131A–C, UR141 + UR149). Dos no son registros independientes: UR267A/B son mitades y UR131A–C es un juego. 138 de 200 tipos no se pudieron confirmar porque los archivos son pequeños.
- **UR053A–E:** W:R entre 0,66 y 0,80 en 5 quipus cuya escala varía 70 veces (Holm 0,003; específico del archivo p = 0,042). Dentro de cada quipu no coescala fila a fila. Es una **clave de archivo, no de registro**.
- **Incahuasi:** P3 y W|NB|AB confirmados (Holm 0,006 y 0,038). El grupo de 9 solo post hoc (p = 0,022). Especificidad no bien apoyada (p = 0,063).
- **PREDICCIÓN DE REFUTACIÓN: no se cumple.**
  - Ningún par de archivos sin relación comparte la clave según el criterio congelado. Con definición estricta: 1 frente a 0,4 esperados (p = 0,33).
  - Mismo motivo con el mismo reparto: 25 % de los pares dentro de un archivo frente a 5,5 % entre archivos (OR 5,75; p = 0,0007).
  - **Resto compartido débil:** en pares de dos colores de sitios distintos, la razón va en el mismo sentido el 59 % de las veces (p = 0,034), sobre todo blanco > marrón. Hay que incorporarlo al modelo: existe un marcado débil de «lo principal», a menudo blanco y en la primera posición, que no es un léxico.
- **Nivel del modelo:** apoyado. Sobrevive su prueba de refutación y la tasa es alta, pero la clave local solo se DEMUESTRA en 4 conjuntos pequeños. Pistas nuevas: el grupo de 8 de UR141/UR149 (Berlín) y el bloque de 6 cuerdas W + R del Santa (UR087/UR092), posible «grupo por tributario».

## Ronda 14: resultados y DEGRADACIONES (13:10)

- **n_rojo_formulario (equipo rojo): baja varias afirmaciones del coordinador.**
  - **«Color = categoría» (167 de 403): de BIEN APOYADO a PROPUESTO.**
    - Con el nulo correcto: 103–108.
    - Controlando posición, número de racimos y largo: 44.
    - Sin totales, máximas ni copias: 19 de 317 frente a 15,9 esperados (p = 0,24).

    El blanco concentra las cuerdas grandes, así que color y posición o tamaño están confundidos.
  - **«No hay léxico compartido»: potencia baja.**
    - P1 detecta un léxico fuerte del 30 % (92 %), pero 0 % con un léxico del 10 %.
    - P2 tiene 0 % de potencia en todos los escenarios.

    El negativo solo vale contra léxicos fuertes que abarquen todo el sitio. La prueba de refutación de 22_formularios sigue siendo el apoyo principal.
  - **UR053:** sobrevive W > R en 99 de 111 (89 % frente a 40 % en otros quipus; Fisher 4e-16; es lo único que pasa Holm global). La proporción concreta no es especial (percentil 78), y R = AB.
  - **UR050, «3 zonas»: retirado.** Es el formato decimal; cualquier cuerda con 3 racimos da 0,20, 0,43 y 0,67. Lo no trivial es que tenga 3 racimos LARGOS, y eso es rasgo de familia (UR050/052/054/055/193).
  - **UR278, 2+1+2+2+2: retirado como confirmación.** Los recortes contiguos dan 6, 11, 10, 9 y 9 (verificado por el coordinador); el del documento es el máximo por una igualdad (p = 0,20). Unas 7,5 de las 11 igualdades se esperan solo por adyacencia.
- **n_cuota_entrega:**
  - «P = cuota, S1 = entrega»: **no se sostiene**. P no es más redondo controlando magnitud (p = 1,0), y S1 > P en el 24 % de las celdas.
  - **Bien apoyado:** la celda de UR278 es P+S1 (5 grupos con ≥ 6/9 columnas; con solo P o solo S1, 0 grupos; p = 0,0002). P suma la cabecera del componente B de UR273B (4/9, p = 0,0004). Nombres nuevos: componente B / componente A.
  - UR270 g6, con todos los P en {100, 200}, es único (1 de 142) y su sentido es desconocido.
  - KFG y OKR coinciden en el 99,8 % de los valores de Incahuasi.
- **n_nudos_imposibles (corrige a n_narrative_threads):**
  - En KFG el número antes de L es el VALOR, no las vueltas.
  - Hay vueltas reales ≥ 10 en 144 cuerdas de **14** quipus, no de 39: UR1095 (32), UR193 (29), KH0001 (29), UR055 (18), UR1087 (13), UR203 (8), AS014 (5)… AS090_N2 queda descartado (valores posicionales; verificado).
  - No son errores: KFG y OKR coinciden al 92,8 % y 6 de 14 tienen notas del transcriptor.
  - Ninguna lectura alternativa cierra sumas (Holm 1,0).
  - **Clase aparte:** 915 cuerdas en 76 quipus con varias unidades que suman más de 9 (notación aditiva o tally).
  - AVISO: `20_categorias/nudos_signo.py` contó como «violación» los L posicionales (p. ej. «200L»), así que su cifra de 3 000 está inflada. Su negativo (no hay vocabulario de nudos) no cambia.
- **n_ur1140_nazca:** la unidad real es **9 cuerdas = 7 campos + 2 marcadoras**. El campo 1 es el máximo en **44 de 45 registros de 4 quipus** (UR1140, UR1136, UR223, HP056; p < 1e-4; robusto por quipu p ≈ 4e-4). UR1136 tiene número de museo consecutivo a UR1140 (VA16635/6), r = 0,96, pero dominado por los campos 1–2. **Apoyado:** formato y encabezado. **Propuesto:** la ficha completa.
- **Estado del modelo «formulario local»: apoyado, con base más estrecha.** Lo sostienen:
  - la prueba de refutación de 22_formularios;
  - los formatos de archivo: UR053 con W > R, la ficha de Nazca/Berlín, Incahuasi, la familia aditiva UR050–055.

  Ya no se apoya en «color = categoría» ni en los negativos de léxico de baja potencia.

## Ronda 15 lanzada (13:20)

- n_ficha_nazca: marcadoras, alineación de los campos 3–7, sumas, y búsqueda de la ficha de 9 en todo el corpus.
- n_color_posicion: separa color de posición con permutación de colores dentro de cada posición; potencia declarada.
- No hay fotos de los candidatos de nudos de ≥ 10 vueltas (UR1095 Múnich, UR193 Berlín, KH0001 AMNH): las fotos del Databook son solo de quipus AS. Pendiente: conseguirlas.

## Género aditivo/tally = torsión Z + camélido (coordinador, 13:45; pista de la página «Z cords» de KFG)

- Las páginas del sketchbook de KFG (p. ej. KH0108 = UR1095) son **dibujos generados desde la base**, no fotos. No sirven para verificar vueltas de nudos.
- **Prueba.** Se marca como tally/aditivo a todo quipu con ≥ 50 % de cuerdas no decimales; el criterio corregido toma el valor, no las vueltas.
  - Entre 285 quipus con ≥ 30 cuerdas: de 10 quipus tally, 7 tienen torsión mayoritariamente Z, frente a 16 de 275 decimales (Fisher OR 38, p = 9e-7).
  - Con la fibra de OKR (171 quipus), la regresión logística tally ~ Z + camélido da coeficientes de 2,76 (p = 0,003) para Z y 3,69 (p = 0,0001) para camélido: **son señales independientes**.
  - Solo en quipus de algodón: Z frente a tally, OR 22 (p = 0,024). UR039 y UR193 son de algodón y 100 % Z.
- **Interpretación (propuesta):** el género aditivo/tally (UR050–055, UR039, UR110, UR144, UR193, KH0001) viene de otra tradición de hilado. En la sierra el hilo de camélido suele hilarse S y torcerse Z; en la costa, el algodón se hila Z y se tuerce S. *Esto viene del conocimiento general de textilería andina y hay que verificarlo con una fuente.* Encaja con quipus de pastores de tradición serrana (Mackey). Las procedencias son variadas (Huari, Pisco, Pachacamac, Chuquitanta): sería un género que circulaba, no un sitio.
- **Nivel:** apoyado (asociación); propuesto (tradición serrana). Pendiente: una fuente sobre la dirección de hilado por región y la réplica con OKR completo. *(corregido después: ver «27_familia_z (Sonnet)»)*

## «Traducción» silábica de UR193 (Sivan/ALBA 2026): no supera el azar (13:55)

- **Qué es la hoja.** Lee cada nudo largo de n vueltas como una sílaba: L2 ki, L3 ma, L4 ka, L5 ta, L6 pa, L7 wa, L8 cha, L9 pi, L10 si, L11 ti, L12 ku. Los S10 se toman como prefijos numéricos y algunas sílabas se reinterpretan como afijos (PASS, ACC, GEN…). Declara un 96 % de aciertos de diccionario y concluye que UR193 es un «registro de consultas al oráculo de Pachacamac».
- **Control** (`analisis/23_sivan_ur193/control.py`, misma regla de lectura en las 116 cuerdas reales y en secuencias al azar con la misma distribución de vueltas):

  | Diccionario | Real | Azar | p |
  |---|---|---|---|
  | Sus reglas, con sílabas sueltas como partículas | 100 % | 100 % | — |
  | Diccionario INDEPENDIENTE: 3 101 raíces de 2–3 sílabas del manuscrito de Huarochirí | 97,4 % | 97,3 % | 0,62 |
  | Solo palabras de su propio vocabulario de ≥ 2 sílabas | 57,8 % | 47,2 % | 0,014 |

  El último caso es circular: el vocabulario se sacó de la misma lectura de UR193.
- **Veredicto:** con un inventario de ~11 sílabas CV, casi cualquier secuencia de 2–3 nudos forma una raíz quechua. El 96 % es propiedad del código, no de UR193. **Refutado como evidencia de lectura.** Lo que sí es real es lo físico: los nudos espirales de UR193 y su género aditivo con torsión Z.
- **Dibujos de KFG** (sketchbook, KH0001 y KH0108): son dibujos vectoriales generados desde la base, no fotos.
- Se incorporó `fuentes_txt/Day1967_QuipusWitchesKnots.txt` (Day 1967); aún sin leer.

## ALBA / Sivan 2026: «Reading the Inca Spreadsheet». Antecedente y prueba decisiva (14:20)

- **Fuentes:**
  - preprint *Reading the Inca Spreadsheet* (v1.01), texto en `fuentes_txt/Sivan2026_InkaSpreadsheet.txt`;
  - repositorio github.com/Alba-Research/KhipuReader (commit 7c2722b, 29-04-2026), consultado solo para leer sus datos, sin ejecutar su código;
  - sitio alba-project.org/khipu-reader.
- **ANTECEDENTE, a citar.** La analogía «el quipu es una hoja de cálculo» ya la publica Sivan 2026, y antes era común en la literatura contable. Nuestro modelo NO es esa analogía: es la hipótesis estadística de «clave local por archivo, sin léxico compartido», probada con un test de refutación (22_formularios). Sivan propone lo CONTRARIO: un silabario universal (L2 ki/chi, L3 ma, L4 ka, L5 ta, L6 pa, L7 y/wa, L8 na/cha, L9 pi, L10 si, L11 ti, L12 ku, E qa) que leería el corpus entero.
- **Falla de método en ALBA.**
  - Su «length-preserving shuffle» (negative_controls.py, control 3) en realidad baraja la asignación sílaba ↔ nudo; lo dice su propio comentario en la línea 210.
  - Sus pruebas de permutación también barajan el mapeo (p = 0,001 en UR039, que es el quipu sobre el que se OPTIMIZÓ; 95,7.º percentil, p = 0,043, con el diccionario combinado).
  - Nunca prueban si las SECUENCIAS reales dan más palabras que secuencias barajadas con el mismo mapeo.
- **Nuestro control** (`analisis/23_sivan_ur193/control_exacto.py`): mapeo ALBA v3 fijo, con polifonía de inicio; su diccionario Kaikki de 2 060 palabras más su extensión de sufijos y prefijos de ≥ 4 letras; su regla de palabra completa. Barajado de los valores de vuelta entre cuerdas del mismo quipu, conservando la longitud de cada cuerda.

  | Quipu | Real | Barajado | p |
  |---|---|---|---|
  | **UR039** (su calibración) | **0,891** | **0,943** | 0,99 |
  | **UR112** (su réplica ciega) | 0,973 | 0,960 | 0,52 |
  | UR193 | 0,707 | 0,728 | 0,77 |
  | UR144 | 0,891 | 0,799 | 0,035 (Holm 0,28) |
  | UR050 | 0,528 | 0,629 | 1,0 |
  | UR055 | 0,233 | 0,216 | 0,30 |
  | UR1095 | 0,850 | 0,825 | 0,52 |
  | KH0001 | 0,736 | 0,716 | 0,39 |

  Con el diccionario independiente de Huarochirí el resultado es el mismo: UR193 p = 0,62, UR039 p = 1, UR112 p = 1.
- **Veredicto (bien apoyado con sus propios datos y reglas):** el orden de los nudos no aporta ninguna palabra quechua más allá de lo que da la distribución de vueltas. La «cobertura» del 92–97 % es propiedad del mapeo, que se ajustó a valores frecuentes con sílabas CV frecuentes, y del diccionario con prefijos. No es una lectura. Coincide con n_descifrado_lm (control positivo no recuperado; «mejor que barajado» premia la rigidez) y con n_linguistica, que ya advertía contra el argumento de entropía de Sivan.
- **Convergencia:** los quipus «de texto» de ALBA (UR039, UR112, UR193, UR144) son exactamente nuestro género aditivo/tally con torsión Z (sección anterior). Lo que ALBA lee como sílabas, nuestros datos lo explican como conteos aditivos de nudos largos de varias vueltas.
- **Salvedades:** usamos KFG y no OKR, y aproximamos su definición de cuerdas STRING con «≥ 2 nudos L de 2–12». Para replicar del todo habría que correr su extractor sobre OKR; no se ha hecho porque supone ejecutar código externo.
- **Réplica sobre las cuerdas STRING del PROPIO ALBA** (`reproducibility/cord_by_cord.csv`, MIT; 2 191 cuerdas, 69 quipus). Palabra = racha de nudos L entre nudos S; mapeo v3 fijo; diccionario Kaikki ampliado; barajado de vueltas dentro de cada quipu; 500 permutaciones (`analisis/23_sivan_ur193/control_cord_by_cord.py` y `.csv`).
  - Hay 24 quipus con ≥ 10 palabras. Media real 0,808 frente a 0,818 barajada.
  - En 11 de 24 lo real supera a lo barajado. Ninguno tiene p < 0,05 (q_BH mínimo 1,0).
  - **El silabario ALBA no lee nada que no lea también una secuencia al azar con las mismas vueltas. Bien apoyado.**
- **Qué trae el repo ALBA:** no hay datos primarios nuevos; todo deriva de OKR y KFG. Es útil por:
  - los léxicos: Kaikki quechua 2 060, quechua_strict_clean, alba_complete_dictionary e IDS aymara (licencia MIT; citar);
  - su clasificación STRING/INT por cuerda;
  - 119 lecturas interpretativas en JSON, que son interpretación y no datos.

  El script `merge_okr_kfg.py` y su «divergences.csv» (no incluido) replican lo que ya medimos: KFG y OKR coinciden al 99,8 % en Incahuasi.
- **Pendiente:** decidir si se comunica este resultado a ALBA, por ejemplo con un issue en su repo. No se ha contactado a nadie.

## Ronda 15: ficha de Nazca y color frente a posición (14:50)

- **n_color_posicion: el color NO codifica magnitud por sí mismo (negativo con potencia).**
  - Comparando la misma posición en grupos distintos, el color se asocia al valor en 32 de 221 quipus.
  - Con efectos fijos de grupo quedan 10 de 205 (4,9 %, el nivel del azar). La varianza explicada mediana es 1,2 %.
  - Efecto mínimo detectable al 80 %: 0,164 log (≈ 18 %). Un efecto de +0,5 log se detecta al 100 %.
  - **Lo que sí hace el color es marcar columna o grupo.** NMI color ~ posición de 0,505 frente a 0,200 del nulo (165 de 222). El coordinador lo verificó con otro diseño: 165 de 326 quipus sobre el p95 del nulo; NMI 0,35 frente a 0,24.
  - La poca señal dentro del grupo se concentra en la cuerda mayor o total; sin ella, 0 aciertos. Propuesto: el color marca total o encabezado.
  - «El blanco es grande» era solo efecto de posición.
  - Unos 10–30 quipus tienen códigos locales fuertes (UR123, HP017, QU013, UR208, AS128, UR231, UR1152).
  - **Lectura:** el color es FORMATO (identidad de columna, marca de total o encabezado), como el formato de celda en una hoja de cálculo, no un contenido aparte. Encaja con el modelo de formulario local y explica por qué «color = categoría» se disuelve al controlar la posición: color y posición son la misma información.
- **n_ficha_nazca: el formato es «encabezado de 2 campos + par marcador + cuerpo».**
  - Las 2 marcadoras son una marca duplicada. El par está a 2 campos de un extremo en 55 de 71 grupos (p ≈ 1e-54), y su lado marca secciones y sentido de lectura.
  - Se generaliza a 6 y 8 campos: **UR234** (grupos de 8) y **UR1131** (grupos de 10).
  - **Validación fuera de muestra en UR1131:** con la regla de orientación congelada, el campo 1 es el máximo en 11 de 12 registros, frente a 0 de 12 sin invertir (p = 0,0032).
  - En total 7 de 651 quipus tienen el formato, todos de Berlín (Nazca, Pachacamac o procedencia desconocida).
  - Los campos 3–7 no se alinean entre quipus y no hay sumas. Es un formato distinto del del Santa y del de Incahuasi.
  - Pasan Holm: UR1140 (0,0017), UR234 (0,013) y UR1131 (0,0001). **Apoyado:** un formato de archivo con encabezado y separador.

## 25_auditoria_color_fotos (Sonnet): confiabilidad del color (15:05)

- Fotografías publicadas del Databook (diapositivas de 800 px, con dominante de color); 14 quipus AS; emparejamiento por bloques.
  - **Categoría gruesa** (blanco / marrón / colorido): 21 de 24 bloques coinciden (88 %); 0 errores blanco frente a marrón.
  - **Tonos de marrón** (AB / MB / DB): solo 5 verificables, con 1 acuerdo pleno.
  - **Fronteras de cambio de color:** 6 de 6 a escala de bloque.
  - **Rasgos que la base no registra:** un hilo rojo enrollado (no es el color de la cuerda) en AS018, el cordón principal trenzado multicolor de AS011 y un hilo azul atado en AS012.

  **Consecuencia:** el color grueso es usable. Los tonos de marrón hay que tratarlos como ordinales e inciertos. Los códigos «/» de tramo corto pueden ser hilos enrollados o atados, no el color de la cuerda.
- **Glosario Ascher** (verificado en `ascher_color_dc`): W blanco, AB marrón claro, B marrón amarillento moderado, MB marrón moderado, KB marrón oscuro, DB marrón profundo, LB marrón amarillento profundo, YB marrón amarillento claro, **BG azul grisáceo**, G verde oliva grisáceo. Corrige glosas previas que tomaban B como azul.
- AS026, 031–034, 038, 070, 124, 136 y 140 tienen foto pero no tienen filas en `cuerdas.csv`.
- Los entregables no contienen imágenes.

## 24_color_formato (Opus): qué hace el color (15:30)

- **El color viaja con el RUBRO, no con el número.**
  - Puruchuco: el color de cada columna se conserva de UR068 a UR067/UR066 (61 % frente a 18 % del nulo; Holm 0,0012).
  - Incahuasi: cuando un número cambia de papel (de parte o fila a cabecera), el destino pasa a W en el 75 % de los casos, sea cual sea el color de origen. Las filas AB/NB de UR278 llegan como W en 18 de 23.

  **Apoyado:** el color identifica el rubro dentro de un documento o archivo y cambia con la función de la cuerda.
- **Otras funciones del color:**
  - Las marcadoras difieren de sus vecinas (76 % frente a 16 %; Holm 0,0012), con un color propio de cada quipu.
  - «Blanco = principal» es en realidad «blanco = primera cuerda del grupo»: 64 de 133 frente a 43,8 esperados. La cuerda del total, una vez controlada la posición, no pasa Holm.
  - Las subsidiarias se distinguen del color del padre en el 80 % de los casos.
- **Códigos locales fuertes** (8 revisados): 3 son marca de grupo, 2 son columna con variantes moteadas y UR1140 no tiene código. Solo QU013 y UR1152 son candidatos a categoría local real.
- **Fuentes.** Solo Garcilaso y Calancha dan claves de color universales, y lo hacen como ejemplos. Day 1967, Mackey, Núñez del Prado («capricho imaginativo del operador») y Salomon las niegan. Ascher 1983 ya hablaba de la redundancia entre color y posición.
- **ADVERTENCIA IMPORTANTE: el transcriptor.**
  - En 40 cuerdas, Ascher distingue ~6 colores, Urton 9,7 y Clindaniel 14,9 (p = 0,0001).
  - **El mismo quipu transcrito dos veces, UR1107 (Ascher) y UR237 (Urton): 0 de 23 etiquetas coinciden.** Verificado por el coordinador: mismos valores en orden inverso (800, 207, 210, 215, 105, 101…) y colores LB/YB/BS frente a AB/MB/HB. Incluso la cuerda de 800 aparece como YB en uno y W en el otro.
  - **Consecuencia:** cualquier comparación de color ENTRE quipus de transcriptores distintos está contaminada. Esto debilita el negativo de «léxico compartido» y la prueba de refutación de 22_formularios, porque los archivos suelen tener un solo transcriptor. **Pendiente obligatorio:** repetir la prueba de refutación solo entre quipus del MISMO transcriptor (p. ej. los de Urton de distintas procedencias).

## 22_formularios: control por transcriptor (15:50)

- La confusión era real: el 90 % de los pares dentro de un archivo comparten investigador, frente al 48 % de los pares entre archivos. `CREATED_BY` registra quién cargó los datos, no quién nombró los colores, así que el transcriptor se asigna por investigador (AS y UR ≥ 1000 = Ascher; resto de UR = Urton).
- **Con el investigador fijo, sigue sin aparecer una clave compartida oculta.**
  - 0 de 35 pares sin relación del mismo investigador tienen el mismo reparto con 3+ colores. La potencia para detectar una tasa del 25 % es ≥ 0,9.
  - Ningún par cumple el criterio de refutación.
  - El exceso débil con 2 colores (blanco–marrón) baja a p = 0,084.
- **Dentro frente a entre archivos, con el investigador fijo:** 25 de 96 frente a 0 de 35 (p = 0,0002; OR 5,5). **Pero sin UR053A–E deja de ser significativo** (p = 0,135); la dirección se mantiene.
- **Nivel del modelo «formulario local».** Se mantiene **apoyado**, con dos lecturas según la parte:
  - **«Sin clave compartida entre archivos»** es un negativo con potencia, también con el transcriptor fijo. Es la parte más sólida.
  - **«Clave local bien apoyada»** descansa casi solo en UR053A–E, más los formatos de Incahuasi y de Nazca/Berlín. Hacen falta más archivos con varios quipus del mismo investigador.

## Ronda 16 lanzada (14:05)

- 26_clave_local (Opus): probar la clave local SIN UR053, con una representación invariante al vocabulario (particiones de color) y validación UR1107 = UR237.
- 27_familia_z (Sonnet): fuentes sobre la dirección de hilado por región, réplica en OKR completo, perfil de la familia, lectura aditiva.
- 28_atlas_generos (Opus): género más probable de cada quipu según todos los detectores, con confianza y una predicción comprobable; cobertura del corpus.
- 29_lectura_incahuasi (Opus): lectura integral, una «traducción» con nivel de evidencia por elemento y la lista de lo que no sabemos.

## 27_familia_z (Sonnet) (14:30)

- **Asociación Z ~ tally: se REPLICA en OKR con la tabla knot.** 7 de 11 tally frente a 16 de 252 decimales (OR 26, p = 4e-6). Resiste los controles de fibra y región (p_perm ≤ 0,005). Colapsando la serie UR050–055 en un solo caso queda 5 de 7 (p = 4e-5). Con el criterio estricto (suma > 9) se debilita (OR 18, p = 0,005; con controles p_perm 0,03–0,20). **Apoyado.**
  - Límites: UR051, UR052, UR055 y UR203 son de torsión S.
  - Dentro de un quipu, las cuerdas Z no son más «no decimales» que las S: la Z es una convención del quipu, no de cada cuenta.
- **«Tradición serrana»: sin apoyo de fuentes.** Ninguna fuente leída asocia la Z con la sierra. Lo documentado es Z ~ camélido (Urton y Brezine 2011, citado en Hyland 2017: camélido 41 % Z frente a algodón 3 % Z), y Collata (sierra) es 58 % S. Baja a **especulativo**.
- **Perfil frente a controles del mismo tamaño (BH):** cuerdas más largas (48,8 frente a 32,5 cm), casi sin multicolor (1 % frente a 21 %), cuentas de 4–6 vueltas (64 % frente a 38 %).
- **«Registro de rebaño»: RETIRADO.**
  - Las cuentas son demasiado regulares: var/media 0,14–0,31, frente a ≈ 1 de un conteo, y las categorías del quipu de ovejas de Mackey van de 30 a 440.
  - En UR050, las tres cuentas de una cuerda son iguales el 22 % de las veces frente al 12 % del nulo (p = 0,001).
  - **Propuesto:** marcas de tamaño casi fijo (cupos o unidades repetidas, quizá turnos o entregas estándar) y no recuentos libres.

## 29_lectura_incahuasi (Opus): lectura integral (14:45)

- **Entregables** (`analisis/29_lectura_incahuasi/`):
  - `lectura.md`: los 14 quipus en orden de flujo, con diagrama; frase de lectura por tipo de cuerda; 13 preguntas abiertas priorizadas; párrafo en lenguaje llano;
  - `tabla_traducida.csv`: 1 461 cifras con papel, lectura, enlace, nivel y fuente;
  - `coherencia.py`: 12 de 12 cifras clave recalculadas; las cabeceras de UR275 suman 56 446, como en Urton y Chu 2018.
- **Lectura del sistema (propuesta; los componentes están bien apoyados o apoyados): cuadre cruzado.**
  - UR270 es una matriz de 9 unidades × 2 partes por registro.
  - UR278 suma por unidad.
  - UR273A/B suman por parte.
  - Ambos caminos llegan al mismo total en el libro UR275/UR266: «entraron X, se apartó la cuota fija 47, quedaron X − 47».
- **Nuevo, como reconstrucción propuesta:** todas las celdas donde no cuadran UR270 g10 y UR278 g29 caen en cuerdas rotas o vacías. Valores perdidos: 194, 161 y 22, y UR278 p212 = 62. Son predicciones verificables en el objeto.
- **Correcciones de cifras:**
  - 26 filas de 9 suman 59 166 bultos (≈ 1 390 t), no 61 790; *(corregido después: ver «Corrección de escala»)*
  - ρ = −0,73 con proporciones por fila (−0,68 con medias brutas);
  - la capacidad del depósito sale 5 090 m³ en n_saya frente a 8 300–13 000 m³ en n_hyslop, sin resolver;
  - el bulto de 82 L queda en propuesto.
- **Divergencia sin resolver:** UR270 g4 da 1 941 por la vía de unidades y 1 780 por A + B.
- **Prioridad 1:** una relectura física independiente. KFG y OKR son la misma lectura hecha por la misma transcriptora.

## 26_clave_local (Opus): la clave propia de cada archivo NO se demuestra sin UR053 (14:50)

- **Representación invariante (partición de color recodificada).** Solo es invariante en parte: ARI de 0,24 entre transcriptores frente a 0,45 en copias del mismo transcriptor. En UR1107 ~ UR237 el ARI es 0,26, porque los transcriptores también AGRUPAN distinto (9 cuerdas en un grupo para uno son 4 grupos para el otro).
- **Prueba principal** (sin UR053 ni Incahuasi, permutación dentro de investigador): T = +0,015, p = 0,24. La potencia declarada antes de correr era 1,00 para el efecto observado en UR053, así que **el negativo es informativo**.
- **Control positivo UR053:** 7 de 9 pares concuerdan frente a 13,6 % de base (p = 0,0008). Es el único de 17 archivos con BH < 0,05.
- **Refutación entre transcriptores:** tampoco se cumple. 3,1 % frente a 3,0 % del nulo (p = 0,37). Dentro de archivo, sin UR053, la concordancia también está en el azar.
- **Niveles revisados del modelo «formulario local»:**
  - **Apoyado (reforzado):** sin clave de color compartida entre archivos, incluso con el transcriptor fijo y con representación invariante.
  - **Apoyado:** el color es formato dentro del documento; identifica columna y rubro (24_color_formato, n_color_posicion).
  - **Propuesto (baja desde apoyado):** clave propia y compartida por los quipus de un mismo archivo. Solo UR053A–E la muestra; las bandas y la posición sugieren estilo de archivo, pero no validan.
  - **Lectura:** cada DOCUMENTO tiene su formato. Que todos los quipus de un archivo compartan una clave común queda por demostrar.
- Candidatos a revisar como UR053: UR1143 ~ UR1149 (Ica-Berlín), UR1136 ~ UR223 (ficha Nazca) y UR063 ~ UR068 (Puruchuco).

## 28_atlas_generos (Opus): atlas del corpus (15:00; verificado: 651 quipus, 8 de 8 controles positivos en su género)

- **Género por quipu** (`analisis/28_atlas_generos/atlas.csv`; fichas en `generos.md`). Cifras: n total / n con confianza alta.

  | Género | n | Alta |
  |---|---|---|
  | Formulario con clave de reparto | 101 | 9 |
  | Lista segmentada (solo formato) | 76 | 0 |
  | Tabla de recuento | 55 | 0 |
  | Aditivo/tally con torsión Z | 28 | 12 |
  | Lista de asignación (cifras redondas) | 28 | 4 |
  | Archivo jerárquico (Incahuasi, Puruchuco) | 21 | 18 |
  | No numérico | 17 | 0 |
  | Decimal con totales internos | 14 | 8 |
  | Padrón tipo Santa | 9 | 6 |
  | Ficha Nazca/Berlín | 6 | 3 |
  | Calendario UR006 | 3 | 1 |
  | Sin género | 293 | — |

- **COBERTURA, la medida del avance:**
  - con confianza alta o media entendemos estructuralmente el **31,6 % de los quipus y el 52,4 % de las cuerdas**;
  - 45 % queda sin género: 113 por datos insuficientes y **180 (28 %) son listas decimales sin estructura detectada**, que es la frontera real.
- **Controles:**
  - el agrupamiento no supervisado coincide poco en conjunto (ARI 0,24), pero separa limpio la ficha Nazca (6 de 6) y el padrón (8 de 9);
  - al barajar rasgos la asignación cae al azar; el género se asocia a la procedencia (NMI 0,355 frente a 0,220; p = 0,005);
  - estabilidad bootstrap: 90,9 % de los quipus conserva su género en ≥ 80 % de las réplicas; los géneros frágiles son asignación y tally;
  - tener dos o más líneas de evidencia NO supera al azar (p = 0,29): no usarlo como argumento.
- **Uso:** es un mapa del corpus con una predicción comprobable por quipu, para especialistas y museos. **Apoyado** en los géneros de confianza alta; propuesto el resto.

## Ronda 17 lanzada (15:10): la frontera de 180 quipus

- 30_frontera_estructura (Opus): relaciones entre quipus con tolerancia, escala o inversión; periodicidad, repeticiones, sumas no contiguas, ajustes de subsidiarias; diseño congelado y mitades de exploración y confirmación.
- 31_frontera_perfiles (Sonnet): perfiles estadísticos, agrupamiento validado, clasificador entrenado en los géneros del atlas y comparación con firmas documentales coloniales.

### 31_frontera_perfiles (Sonnet, 15:30) — verificado contra salida_analisis.txt
- Frontera (180 quipus decimales sin género): el mejor corte es k=2 (122/58). La silueta es 0,19 frente a un nulo p95 de 0,15 (p=0,01), pero el ARI bootstrap tiene un IC de [0,03; 0,99], así que es inestable. Es un **gradiente de escala** (valores ~5 y 4 colores frente a ~100 y 12 colores), no géneros nítidos. Nivel: apoyado.
- Clasificador RF sobre el atlas (198 quipus): CV balanceada 0,46, frente a 0,125 con etiquetas barajadas. NAZ y PAD tienen recall 0. Es circular con las reglas del atlas.
- Solo 1/180 es asignable con prob ≥0,7 (ASG). No aparece ningún género nuevo. La redondez de los grupos (0,25–0,34) queda entre padrón (0,17) y asignación (1,00); con 45 ítems documentales no se separan padrón, inventario y tributo.
- Conclusión: con perfiles globales la frontera no se resuelve; hace falta estructura interna (ronda 30, Opus).

### Corrección de escala (2026-10-18 ~15:15)
- Las "≈1 390 t" de mis resúmenes daban demasiada precisión. Toda la cifra sale del supuesto bulto = 82 L, que está en **propuesto**. Ese valor no viene de la arqueología: lo despejó n_saya_proporcional de la capacidad del depósito, suponiendo todo almacenado a la vez y al 100 %. La misma capacidad sale 5 090 m³ en un cálculo y 8 300–13 000 m³ en otro, sin resolver. n_almacenes ya había mostrado que la unidad es **indecidible**: arroba, costal, carga de llama y fanega son todas compatibles, con Holm q ≥ 0,08. Su mejor ajuste nominal fue la fanega (55,5 L), pero no gana.
- Con maní en vaina a 0,286 kg/L y 59 166 bultos: 1/6 de fanega da ~157 t; un saco de 40 L, ~677 t; la fanega, ~939 t; 82 L, ~1 390 t; y 127 L, ~2 150 t.
- Que 82 L "no quepa" en las tierras de Lunahuaná es evidencia, débil, contra un bulto tan grande o contra que el libro sea una sola cosecha de un solo valle. No es un hallazgo sobre la producción.
- La fanega es una medida castellana: sirve como referencia de volumen, no como unidad inca. Nivel de la unidad: abierta (rango ~10–130 L). Tonelaje: solo orden de magnitud, 10²–10³ t.
- Seguimiento: la "fanega" (~56 L) viene del glosario de LeVine, y la llamé "confirmación independiente" del rango 30–55 L de n_almacenes; eso exageraba. Pasé a 82 L sin explicarlo, pero la fanega cae dentro de su IC90 (51–127 L) y las dos cifras salen de la capacidad del depósito. Formulación vigente: **saco de ~30–80 L, del orden de una fanega; total ~700–1 000 t (orden de 10² a 10³)**. Para cerrarlo hace falta evidencia física: contenedores de las excavaciones de Chu o una tasa colonial del valle en especie.
- Ajuste final: el argumento de la tierra no discrimina, porque la superficie de Lunahuaná fue un supuesto y a escala de Cañete cualquier unidad cabe en el 2–4 %. Quedan dos hipótesis con nombre, que los datos no separan: **fanega** (~56 L, ~16 kg, medida castellana) y **carga** (~80 L, ~23 kg = una carga de cargador o llama, unidad andina). La carga tiene leve preferencia, propuesta. Total ~900–1 400 t.

## Ronda 18 lanzada (~15:40)
- Opus `analisis/33_estematica/`: árbol de copias de todo el corpus (Lachmann: errores conjuntivos, dirección de la copia, controles positivos con copias conocidas).
- Sonnet `analisis/34_comparada/`: chequeo rápido de la escritura pallariforme (Larco Hoyle) y comparación con la contabilidad protocuneiforme y el Lineal B (cuota frente a entrega), con ≥3 pruebas sobre nuestros datos.
- Opus `lector/`: lector reproducible que empaqueta los detectores validados, con verificar.py.
- El artículo de Incahuasi queda para cuando todo esté cerrado.

### 34_comparada (Sonnet) — verificado contra resultados_pruebas.csv
- Pallariforme (Larco Hoyle): especulativo, sin relación demostrable con los quipus. No hay datos abiertos. Las críticas citadas vienen de una fuente secundaria.
- Protocuneiforme y Lineal B, rasgo por rasgo:
  - Paralelos reales: jerarquía de documentos, formato fijo por tipo y copias.
  - Analogías débiles: cuadre por dos caminos (no documentado en Uruk ni en Pilos), metrología por producto y déficit o-pe-ro.
  - El conocimiento de Uruk y Pilos es previo, sin páginas verificadas.
- Pruebas (Holm sobre 7):
  - El perfil del dígito de unidades difiere por archivo y por género (p 0,003 y 0,0014). Lo bajo a **propuesto** porque las copias y la magnitud confunden. La base 10 es universal.
  - El "total primero" se explica por los quipus ARC; fuera de ellos no hay preferencia.
  - UR278→UR266: 11/24 filas exactas y 7 fallos de un dígito. Reconfirma lo sabido, no es nuevo. *(corregido después: ver «Desajustes UR278 → libro: ¿convención o error?»)*
  - El déficit tipo o-pe-ro es negativo (p 0,70).
- Lección de método: los sistemas metrológicos protocuneiformes se descifraron por cuadre de totales y contexto, que es lo que ya hacemos. Propuesta útil pendiente: calibrar la tasa de error de los escribas con CDLI.
- Fuente nueva: Nissen, Damerow y Englund 1993, *Archaic Bookkeeping*. Texto completo cotejado (fuentes_txt/Nissen1993_ArchaicBookkeeping.txt, 182 págs.). 34_comparada se amplió para verificar con páginas: tasa de error de escribas, cuadre por dos caminos y orden de mayor a menor. La pág. ~60 muestra una cuenta de raciones ordenada de mayor a menor, como las 9 columnas de Incahuasi.

### 34_comparada, ronda 2: verificado con Archaic Bookkeeping (NDE 1993; resultados_pruebas_ronda2.csv revisado; la cita de la p. 25 cotejada con el texto)
- Confirmado con páginas: sistemas numéricos por producto (5 principales; el mismo signo vale distinto según el sistema; pp. 25–28, 37), formato fijo por transacción (p. 30), totales en el reverso (p. 20) y cadenas de documentos «probadas en pocos casos» (balance Jemdet Nasr 62a–c reordenado, pp. 74–75; paralelo de UR275 reordenando UR266).
- Corregido:
  - El orden de mayor a menor de la pág. ~60 es acadio antiguo (c. 2250 a. C.), no protocuneiforme. En el Uruk arcaico solo la lista de profesiones va ordenada por rango.
  - Los totales del reverso pueden superar la suma, así que un desajuste no prueba error.
  - El déficit tipo o-pe-ro es sumerio antiguo y Ur III, no Uruk.
- **El cuadre por dos caminos no está documentado en Uruk.** El de Incahuasi queda como rasgo propio (propuesto, con analogía débil).
- Errores de escriba: el libro no da tasas, solo casos. 4 de los 8 textos MSVO 3 que analiza tienen errores, sobre todo omisiones. En UR278 los fallos son de un dígito. P6 (omisión de una celda) es negativa: 2 frente a 3,9 esperado.
- Pruebas nuevas (Holm sobre 11):
  - P5b: las columnas de UR278 son decrecientes (tau −0,41; Holm 0,002). Bien apoyado; ya era apoyado.
  - **P5c: en el corpus sin Incahuasi, el valor mayor va primero en el 25,9 % de los grupos, frente al 15,2 % esperado (Holm 0,002). Apoyado, es nuevo:** la convención «la cuerda mayor abre el grupo» va más allá de Incahuasi y Nazca.
  - P5a: no hay orden monótono general (Holm 0,055).
- **Lección de método (NDE p. 25):** hasta 1983 los desajustes protocuneiformes se atribuían a «errores de cálculo» de los escribas, cuando eran sistemas no reconocidos. → Los 13/24 fallos de UR278→UR266 podrían ser en parte una convención no reconocida. Candidata a prueba: ¿son sistemáticos (misma columna, mismo dígito, mismo signo)? *(corregido después: ver «Desajustes UR278 → libro: ¿convención o error?»)*

### Lector reproducible `lector/` (Opus): verificado por el coordinador (verificar.py 13/13 en 137 s)
- Comando: `python lector/lector.py <KFG|OKR|archivo.csv> [--json] [--todos]`. Pasa por los 651 quipus en 167 s sin errores. Cada ficha trae 8 secciones, y cada afirmación su nivel y su ruta.
- Reproduce desde cero:
  - UR270→UR278 (celda = P+S1);
  - los totales de UR278 en UR266 y en UR275;
  - Nazca en UR1140 (19/19) y UR1131 (11/12);
  - UR053A = FOR;
  - el atlas completo (coincidencia 1,000);
  - los controles negativos.
- Matiz: la copia UR266~UR275 no sale cuerda a cuerda, solo por registro (44/46 aristas). La ficha la da como documentada.
- Relaciones en el corpus: 28 quipus, casi todos con pares conocidos. Candidatos nuevos, propuestos: **UR004→UR091** (totales en orden) y **UR1034~UR1145**.
- Dependencias: el lector IMPORTA por ruta 01_aritmetica, 04_concordancias, 22_formularios, 28_atlas_generos y ds/n_ficha_nazca. Hay que incluirlos o copiarlos dentro de lector/.
- Fuera por ahora: escalas, reordenamientos de bloques y sumas no contiguas (enganche en DETECTORES_EXTRA, para 30_frontera). Revisar KH0631 (OKR sin KFG; datos con discrepancias).

### Desajustes UR278 → libro: ¿convención o error? (coordinador; 34_comparada/desajustes.py)
- **Corrige el 54 % de 34_comparada (P3):** UR278 tiene 26 filas de 9; 8 no tienen destino conservado en el libro. De las 18 con destino, 11 son exactas y 7 son desajustes (39 %); 5 de esos 7 son ±1.
- Desajustes (libro − detalle): +6, +100, +1, −1, +1, −1, −1. **No hay dirección sistemática** (4+/3−, p = 1,0). Las dos copias del libro, UR266 y UR275, coinciden entre sí en todos: la diferencia nace en el paso detalle → libro.
- **6 de 7 están en las unidades** (p = 0,007 frente a un nulo de 1/3 por posición; nulo aproximado). Las unidades se anudan como nudos largos de varias vueltas, que son los más fáciles de contar mal. Es la firma de un error de conteo de vueltas, sea del khipukamayuq o del transcriptor, y no la de una convención. Una convención daría signo o magnitud constantes, como en Uruk, donde un mismo signo valía distinto según el sistema.
- Veredicto: **error de conteo de vueltas en nudos largos (apoyado); convención descartada para estos 7 (apoyado, n chico)**. La revisión en el museo debe mirar los nudos largos de las celdas señaladas en n_casi_aciertos.
- Aviso: la fila g29 (1507) enlaza con UR266 g2 = 1506, que ya es el destino exacto de g1. Revisar si es un registro duplicado.

### 30_frontera_estructura (Opus), cerrado; el coordinador reprodujo 07_ur122_kh0049.py
- De los 180 de la frontera solo salen 3 con las reglas congeladas y un nulo más estricto: **UR040, UR167 (bien apoyado, Holm 0,025) y UR1033F (apoyado)**. La familia común es la **alternancia de dos colores A/B/A/B**, la única que se replicó en la mitad de confirmación (q 0,003). En el corpus hay 19 quipus así: 15 ya eran TAB/FOR y 5 están en el Peabody. Se lee como una tabla de dos columnas escrita intercalada; en UR1033F, AB > W en 14/16.
- **Nuevo, fuerte y post hoc: KH0049, copia completa de UR122, es una tabla jerárquica de 3 niveles con totales por columna.** En bloques de 18 cuerdas, B0 = B1+B2 en 14/18 posiciones exactas y B1 = B3+B4+B5 en 7/18; el nulo da como máximo 6 y 4 (p 5e-5; reproducido). UR122 copia la sección de subtotales. La discrepancia 15652/15649 está en las dos copias, así que viene del original. Nivel apoyado, por ser post hoc. **Corrige a 10_tablas:** la columna-total ya no es «solo Incahuasi»; hay un segundo caso, Nazca (Gotemburgo/Lima). PENDIENTE: verificar si Ascher o Urton ya lo publicaron. *(corregido después: ver «Cabos sueltos, paquete de revisión»)*
- El diseño congelado era laxo: dejaba salir 22. La enmienda 3, un nulo que conserva rachas y que solo puede subir p, quitó 19 sin perder los controles reales (UR1107/UR237 y HP055/UR1084 siguen en p 5e-4). Las fronteras nulas dejan salir 0.
- Negativos limpios: periodicidad, repeticiones internas, pares de suma igual y relaciones entre quipus del mismo museo o sitio (solo sobrevive el ya conocido UR1118≈UR218). Propuestos: subsidiarias que escalan con su colgante por rango y tendencias monótonas, sin replicación.
- Lectura de conjunto, con los perfiles de 31: la frontera es en su mayoría **listas decimales sin estructura recuperable con estos datos**. Para seguir harían falta metadatos (contexto, fotos) o una clave externa, no más estadística.
- Revisiones baratas en el museo: foto de UR122 (las cuerdas en 0 donde KH0049 tiene valor deberían estar rotas), relectura de UR040 y UR167, y releer KH0049 B1[1] (15652 frente a 15649).

- 22:23 (Lima): 33_estematica se amplió con las candidatas del lector, el caso UR122/KH0049 y los desajustes de UR278. Los demás agentes de la ronda 17–18 ya cerraron: 30, 31, 34 y lector.

### 33_estematica (Opus), cerrado; el coordinador verificó UR1104→UR234 en cuerdas.csv
- Barrido de los 201 930 pares, con un nulo que permuta rachas. Recupera 5 de 7 controles por tramos; los otros 2, que comparten cabeceras y no tramos, con una prueba sin orden post hoc. De los 25 pares de 04 recupera 23.
- **Copia nueva (no publicada; grep y web): UR1104 (AS104, Berlín, Pachacamac; Ascher) reproduce en orden las cabeceras de 9 registros de UR234 (Berlín; Urton).** Verificado: 2007 2080 3102 2247 2578 2016 3419 3159 1407 frente a 2007 2080 3012 2247 2578 [rota] 3419 3159 1407. Hay 8 números de 4 cifras exactos y en orden, y la única variante es el mismo nudo leído en otra posición decimal. UR1104 conserva la cabecera rota de UR234 (2016), que es una **predicción verificable en el objeto**. Nivel apoyado (post hoc), aunque la fuerza es de bien apoyado. Tipo nuevo de copia, el **extracto de un campo**: un resumen que sube de nivel, tomando el campo 1 (el mayor) del formato Nazca/Berlín. Une el formato de ficha con un quipu resumen. *(corregido después: ver «Cabos sueltos, paquete de revisión» y «Lector y atlas actualizados con las rondas 17-18»)*
- Propuesta: UR108 (Lima, Temple Radicati) → cuerda 9 de las 6 secciones de UR231 (Berlín), con 5/6 exactas. Si se confirma, apoya la unión de los fragmentos VA16135a/b.
- **La copia es un rasgo de archivo:** dentro de un sitio, 10 de 6 820 pares; entre sitios, 6 de 72 980 (OR 17,9; p 1e-7). En los archivos casi completos tiene copia entre el 14 y el 20 % de los quipus; en el corpus, el 5,5 % (cota inferior). Tipos: duplicado, copia por tramos en varias piezas (UR232+UR233; Basilea→UR212, con dos invertidos), otro desglose y extracto de un campo. Contaminación propuesta: MM016 combina UR212 y UR1131. TAL, ASG y SUM no se copian.
- Dirección: indecidible en casi todos los pares. Hay dos nudos firmes por errores conjuntivos: un libro perdido α entre UR278 y UR266/UR275 (los ±1 compartidos), y KH0049/UR122 (15652/15649). Leymebamba queda en estrella sin resolver.
- Candidatas del lector: UR004→UR091 negativa (p 0,51); UR1034→UR1145 especulativa.
- KFG y OKR son la misma lectura (99,9 %). Las únicas lecturas independientes son 3 duplicados de un mismo objeto, con un ruido de lectura del 3 al 12 %. Este es el dato de error de transcripción que faltaba.

### Cabos sueltos, paquete de revisión (Sonnet): verificar.py 15/15, corrido por el coordinador
- KH0049 = AS038/HP036, MNAAHP3550, «Costa Sur» (no Nazca; Nazca viene de UR122 = KH0362, Gotemburgo). **Parcialmente publicado:** KFG lista sus sumas indexadas como salida automática. No están publicadas la jerarquía de 3 niveles, la copia UR122 ni la discrepancia 15652/15649. Sin revisar: Ascher y Ascher 1978 y Pereyra Sánchez 2011.
- **Corrección:** UR1104→UR234 son **7 exactas + 1 variante (3102/3012) + 1 rota (2016)**, no «8 exactas».
- Retirada la frase «B0 = B1+B2+B3 en UR122» de 30 (nota añadida al informe).
- Paquete: predicciones 27–32 nuevas; la unidad pasa a carga o fanega, ~900–1 400 t; el «54 %» se corrige a 7/18 = 39 %; antecedentes K01–K06 (NDE 1993).

## Lector y atlas actualizados con las rondas 17-18 (18-10, noche)
- `lector/verificar.py`: 19/19 comprobaciones (13 anteriores + 6 nuevas, con controles negativos AS006 y KH0049 barajado). `--todos`: 651 quipus, 0 errores.
- Detectores genéricos nuevos en `detectores.DETECTORES_EXTRA`: alternancia de dos colores (nulo de 06) y totales por columna (nulo de 07; reproduce KH0049 14/18 y 7/18).
- Relaciones documentadas añadidas: UR234→UR1104, UR231→UR108, KH0049→UR122, UR004→UR091 (negativa), UR1034~UR1145 (especulativa), UR278→libro con sus 7 desajustes.
- Enmiendas al atlas (`28_atlas_generos/enmiendas.csv`; `atlas.csv` no se toca): UR040 TAB baja, UR167 TAB media, UR1033F TAB media, KH0049 SUM media (FOR queda secundario), UR122 SUM baja. Cobertura media/alta: 206 → 208 quipus (31,6 → 32,0 %).
- UR1104: en los registros 1-9 de UR234 hay 7 cabeceras exactas + 3102/3012 + la rota (2016); con 1385 del 12.º registro son 8 cabeceras en orden. Las dos cifras son compatibles.
- Candidato nuevo sin verificar: QU005, B2 = B0+B1 en 12 de 19 posiciones (q 1e-4; atlas FOR media). UR1120 (B0 = B1+B2+B3 en 7/8) es la fila resumen ya vista en 10_tablas.
