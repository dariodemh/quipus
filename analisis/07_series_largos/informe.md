# 07_series_largos: cuerdas con series de nudos largos (UR050–UR055, UR039, UR110, UR112, UR144)

Pregunta: las cuerdas con 2–6 racimos de nudos largos (L) de 4–9 vueltas, sin patrón decimal (`4L;5L;5L`), ¿son reales en el registro original?, ¿qué estructura tienen las "palabras" (secuencias de vueltas)?, ¿qué interpretación sobrevive a nulos explícitos?, ¿es un estilo local o general?

Scripts (en orden; semilla 20261017; reutilizan `06_nudos/racimos.csv` y `06_nudos/util.py` sin modificarlos):
`01_okr.py` (verificación contra OKR) → `02_prep.py` (tabla de cuerdas foco y referencia decimal) → `03_pruebas.py` (palabras, nulos, interpretaciones; B = 2 000, 1 000 en similitud) → `04_corpus.py` (corpus completo, estilo, repetición entre quipus, sensibilidad de UR144). Salidas: `0N_salida.txt`, `01_quipus.csv`, `okr_racimos.csv`, `okr_cuerdas.csv`, `cuerdas_foco.csv`, `cuerdas_decimal.csv`, `tabla_descriptiva.csv`, `tabla_pruebas.csv` (351 pruebas con p, BH y Holm), `tabla_vs_decimal.csv`, `tabla_corpus_series.csv`.

Definición: **serie_L** = cuerda con ≥2 racimos y todos los racimos son un nudo L (sin S/E). "Palabra" = tupla de vueltas de arriba abajo.

## 1. ¿Existen en el registro original? (`01_okr.py`)

- **El OKR las registra igual que el KFG.** En el OKR cada racimo es un `knot_cluster` propio con su `START_POS`, y contiene **un solo nudo L** (2 577 de 2 578 racimos L en los 9 quipus) con `NUM_TURNS` explícito; dirección S 94 % (2 417 S, 143 Z, 18 U); `AXIS_ORIENTATION` = AXU en 80 %. Si emparejamos racimo a racimo (número de colgante + posición en cm), la coincidencia KFG–OKR en tipo es del 99,1–100 %, en vueltas del 99,4–100 % y en dirección del 100 % en 8 de los 9 quipus. Recuento global: serie_L 1 247 cuerdas en KFG frente a 1 211 en OKR.
- **Excepción, UR144:** el 39 % de los racimos L no coincide, y siempre es el **racimo superior** (58 de 60): KFG da +2 a +4 vueltas respecto del OKR (p. ej. KFG `7-3` frente a OKR `4-3`). Con las vueltas del OKR, UR144 se parece a los demás (media 3,5 frente a 5,1; descenso último−primero −0,9 frente a −4,3; sd dentro de la cuerda 0,56 frente a 2,12). **La lectura de las vueltas depende de la fuente** en un quipu de nueve, y no puedo decidir cuál de las dos es correcta.
- **Ascher frente a Urton (tipo asignado por posición o por tipo):** no aplica. Los 9 quipus son solo UR; el `khipu_summary` del KFG no les da equivalente AS. El Databook de Ascher (`encontrado/Databook/Quipus/as*.pdf`, 206 PDF) son escaneos sin capa de texto: `pdftotext`/`pypdf` devuelven texto vacío, no hay OCR instalado y ningún AS corresponde a estos quipus. Como Urton asigna el tipo por la morfología del nudo, un L de n vueltas a 15–60 cm queda registrado como L de n vueltas, de modo que la serie no es un artefacto de asignación por posición. **Ojo:** KFG y OKR **no son independientes**, porque proceden del mismo registro del equipo de Urton y Brezine. La verificación descarta errores de transcripción entre bases, pero no errores de lectura en el museo.
- **Notas de campo relevantes:** UR050: "*Knots are extremely difficult to read (Urton)*", torsión floja (~70°) y "*knot placement indicates canutos were wrapped after knots were tied?*". UR055: "*Khipu of human hair*" (descripción de museo) y "*last small knot may be unintentional*". UR052: grupos de cuerdas dobladas y envueltas con hilo de color ("canuto"), tipos de fibra A–D. UR051: "*cord wrapped with rest of group*" (42 cuerdas). UR112: "*Camelid khipu with canutos*", grupos 19–20 reconstruidos "best guesses". UR110: "needlework bundle". Hay numerosos nudos de reparación en UR050 y UR055. No encontré ninguna nota que describa las series como error.
- **Hallazgo estructural clave:** los **únicos 8 quipus del OKR con tabla `canuto`** (cuerdas atadas en fajos envueltos con hilo) son exactamente UR039, UR050, UR052, UR054, UR055, UR110, UR112 y UR144. El noveno, UR051, tiene cuerdas "wrapped with rest of group" sin codificar como canuto. Los fajos son de 4 o 6 cuerdas (UR050: 24×6 + 5×4; UR055: 31×4 + 9×6; UR144: 24×4); UR039 tiene fajos de 2. La literatura del repo (Curatola 2013, que cita a Urton 2011; Milillo 2024) trata los quipus "canuto" como **post-inka y probablemente coloniales**. UR039 figura con procedencia "Huari", sin fecha.

**Nivel:** las series existen en el registro original como racimos L separados: **bien apoyado** (para el registro). Que la física sea esa, sobre todo el número exacto de vueltas, solo está **apoyado con datos**: hay una sola lectura de campo, la nota de UR050 dice "extremely difficult to read" y UR144 tiene discrepancia sistemática entre fuentes.

## 2. Las "palabras" (`03_pruebas.py`)

Corpus foco: 774 cuerdas serie_L (982 con nudos) en 9 quipus.

| quipu | serie | k moda | vueltas media (moda) | % 4–6 | % S | palabras distintas | más frecuentes |
|---|---|---|---|---|---|---|---|
| UR039 | 41 | 2 | 4,5 (5) | 94 | 100 | 16 | 5-4×10, 4-4×7 |
| UR050 | 162 | 3 | 5,5 (5) | 87 | 80 | 57 | 5-5-5×19, 5-6-6×14 |
| UR051 | 75 | 2 | 4,5 (4) | 62 | 99 | 39 | 4-3×10, 5-4×9 |
| UR052 | 89 | 4 | 5,6 (5) | 69 | 100 | 76 | 5-4×3 |
| UR054 | 111 | 3 | 5,5 (5) | 79 | 100 | 59 | 5-5-5×9, 7-6-5×6 |
| UR055 | 156 | 4 | 6,7 (7) | 40 | 99 | 135 | 7-7-7-7-6×4 |
| UR110 | 50 | 2 | 4,4 (4) | 81 | 68 | 15 | 4-4×11 |
| UR112 | 36 | 2 | 4,8 (5) | 96 | 97 | 12 | 5-5×11, 5-4×10 |
| UR144 | 54 | 2 | 4,9 (4) | 44 | 99 | 14 | 7-3×15 (OKR: 4-3) |

**Distribución de vueltas.** En los quipus foco las vueltas forman una campana centrada en 5: el 28 % de los nudos tiene 5 vueltas, el 68 % tiene 4–6 y solo el 6 % tiene 2–3. En los L de **unidades** de cuerdas decimales del resto del corpus la frecuencia **decrece de 2 a 9** (17 % → 7 %), y la moda por quipu es 2 o 3 en 71 de 144 quipus. Si las vueltas fueran cuentas de cosas, como un dígito, se esperaría la forma decreciente. La forma observada parece más bien un "nudo largo de tamaño típico" con dispersión alrededor de 5.

**Estructura dentro de la cuerda** (efecto combinado = media de z sobre 9 quipus; p empírico, BH sobre 351 pruebas):

| estadístico | nulo (a) barajar racimos entre cuerdas | nulo (b) iid de la marginal | nulo (d) permutar el orden dentro de la cuerda |
|---|---|---|---|
| sd dentro de la cuerda | z −2,6, q = 0,003 (más homogéneas) | z −1,4, q = 0,003 | z 0,2, q = 1 |
| información mutua entre vueltas sucesivas | z +2,8, q = 0,003 | z +2,8, q = 0,003 | z −0,5, q = 0,28 |
| pares contiguos iguales | z +1,1, q = 0,004 | q = 0,03 | q = 0,30 |
| tendencia (último − primero) | z −1,2, q = 0,003 | q = 0,005 | q = 0,04 |
| palabras distintas / ocurrencias | z −3,1, q = 0,003 | z −2,2, q = 0,003 | z −2,0, q = 0,003 |
| pendiente de Zipf | z −3,4, q = 0,003 | q = 0,003 | q = 0,003 |

- **Las cuerdas son internamente homogéneas** (palabras tipo 5-5-5 o 4-4): 6 de 9 quipus con q < 0,03 frente al nulo (a). UR144 va en sentido contrario, pero solo con las cifras del KFG.
- **La "secuencialidad" (información mutua) se explica entera por la composición de cada cuerda.** Desaparece con el nulo (d). El orden dentro de la cuerda solo aporta una **tendencia monótona** propia de cada quipu: ascendente en UR050 (+0,38) y UR052 (+0,58), descendente en UR039 (−0,59) y UR144. Esa tendencia hace que las palabras se repitan algo más en su orden real que barajadas (palabras distintas y Zipf frente a (d)). No hay indicio de un orden con estructura más allá de "el tamaño crece o decrece a lo largo de la cuerda".
- **Zipf:** las pendientes observadas (−0,24 a −1,17) son de la misma magnitud que las del nulo iid (−0,15 a −0,95). Una curva "tipo Zipf" sale de vueltas al azar, así que **no es evidencia lingüística**. Esto afecta directamente a Sivan (2026), cuyos quipus de calibración y validación (UR039, UR050, UR055, UR112) pertenecen todos a esta familia. Su "información mutua" y su Zipf no distinguen un lenguaje de un generador iid con homogeneidad por cuerda.
- **Comparación con números decimales (nulo c; percentil entre 177 quipus decimales con ≥20 cuerdas de k ≥ 2):** las series son extremas. Diferencia contigua media en percentil 1–7 (0,7–1,9 frente a 2,8 de mediana decimal), sd dentro de la cuerda en percentil 1–5, pares iguales en percentil 93–97. Los dígitos de números reales varían mucho más dentro de la cuerda.
- **Repetición entre quipus:** las palabras distintas compartidas por pares de quipus foco son **menos** que con el nulo (a) (226 frente a 277; p = 0,001; con k ≥ 3: 85 frente a 102, p = 0,06). **No hay vocabulario compartido.**

**Posiciones (cm).** Separación mediana entre racimos de 11,5–19 cm (decimal: 7 cm). La sd de la posición del j-ésimo racimo entre cuerdas del mismo k es de 4,3–12 cm (decimal, sd por nivel: mediana 2,2, p90 4,4): los 9 quipus están en el percentil 89–100. El coeficiente de variación de los huecos es de 0,16–0,33 (decimal 0,12). **No hay bandas alineadas entre cuerdas**, como sí ocurre con los dígitos. El espaciado dentro de cada cuerda es semirregular (CV ~0,2), pero cada cuerda tiene su propia escala. Las vueltas no dependen de la altura de forma consistente: rho(vueltas, cm) va de −0,37 a +0,36 según el quipu, y −0,81 en UR144-KFG.

**Relación con canuto, vecinas y color** (similitud de la media de vueltas entre pares; nulos por permutación dentro del quipu):
- Las cuerdas del **mismo canuto** se parecen más entre sí (z combinado 2,2; q = 0,0035; individualmente UR052, UR055, UR110 y UR144 con q < 0,01), igual que las **vecinas** a ≤2 posiciones (z 3,1; q = 0,0035; 7 de 9 quipus) y las del **mismo color** (z 3,0; q = 0,0035; 5 quipus con más de un color). Lo mismo vale para el número de racimos k (z 2,6; 2,6 y 7,4).
- La **posición homóloga dentro del canuto** (la 1.ª cuerda de cada fajo frente a la 2.ª...) **no** produce similitud (z 0,09; q = 0,91): **negativo**.

## 3. Interpretaciones y su predicción falsable

| # | interpretación | predicción | resultado | veredicto |
|---|---|---|---|---|
| i | número aditivo o en otra base | el valor (Σ vueltas, lectura posicional base 10, o k) cumple relaciones de suma: una cuerda = suma del resto de su canuto, o = suma de 2–6 vecinas, por encima del nulo | Σ: 1 frente a 1,8 (p = 0,84) y 19 frente a 23,9 (p = 0,89); posicional: 0 frente a 0,7 y 3 frente a 3,9; k: 6 frente a 5,4 (p = 0,46) y 62 frente a 83 | **rechazada** (ningún exceso; apoyado con datos, negativo). Casi no hay subsidiarias (solo 5, en UR051): la prueba colgante-subsidiaria no es posible. |
| ii | unidades no decimales / radix mixto (medidas, fracciones) | racimos inferiores con techo < base y valores bajos (1–3) frecuentes; posiciones alineadas para poder marcar ceros | sin techo: la media y el máximo en j ≥ 1 son iguales o mayores que en j = 0 (UR055 j2: máx. 12); valores ≤3 raros (0–10 % salvo UR051); sin bandas | **no apoyada**. Solo UR144-KFG (j0 7,4; j1 3,1; j2 2,2) tiene esa forma, y desaparece con las cifras del OKR. |
| iii | calendario / conteo de días | sumas 29/30 por cuerda o por canuto por encima del azar; totales con valor calendárico | cuerdas: 12 frente a 17,5 (p = 0,95); canutos: 9 frente a 6,3 (p = 0,15); totales por quipu 475–4 249 vueltas sin valor notable | **rechazada / sin apoyo** |
| iv | códigos o etiquetas categóricas | palabras repetidas en posiciones homólogas (mismo ordinal en distintos canutos) y vocabulario compartido entre quipus | homólogas: z 0,09 (q = 0,91); entre quipus: menos palabras compartidas que el azar | **rechazada** con estos diseños |
| v | convención o hábito del anudador o registrador (las vueltas son un "tamaño de nudo", no un valor) | vueltas en campana alrededor de un valor típico; homogeneidad por cuerda y por lote (canuto, vecinas); sin aritmética; sin bandas; dependencia de la lectura | se cumplen todas: campana en 4–6; homogeneidad por cuerda (z −2,6) y por canuto/vecinas (z 2–3); ninguna suma; sin bandas; UR144 cambia +3 según la fuente | **sobrevive** (apoyado con datos como descripción; como explicación, propuesto) |

Lo que sobrevive es una lectura doble: (a) el número de vueltas parece un rasgo de **factura por lote y por cuerda**, en el que cada cuerda o fajo se anuda con un "tamaño" de nudo largo parecido y con tendencia monótona, más que un valor contado; (b) la información, si la hay, estaría en lo que sí varía de forma estructurada: **k** (número de largos por cuerda), el fajo (canuto), el color y la cuerda. No he encontrado ninguna prueba de que las secuencias de vueltas sean "palabras" con orden significativo. La similitud por canuto y vecinas puede deberse tanto a contenido agrupado como a producción en tandas, y estos datos no permiten separar ambas cosas.

## 4. Todo el corpus (`04_corpus.py`)

- Hay 13 de 641 quipus con ≥30 % de cuerdas serie_L (y ≥10 cuerdas con nudos): los 9 quipus foco más AS090_N2 (artefacto n = valor), AS076 (8 cuerdas `2-2`), UR171 y AS132 (≤5 cuerdas serie cada uno). **Los 8 quipus con canuto del OKR ocupan los puestos 2–14** de 641 por fracción serie_L. Que ≥6 de ellos caigan en el top 9 por azar tiene P hipergeométrica = 2,5 × 10⁻¹¹. Los 9 quipus foco concentran el **62 %** (774 de 1 247) de todas las cuerdas serie_L del corpus.
- Las series de **otros** quipus (25 quipus con ≥5 cuerdas serie_L, sin los artefactos n = valor) son de **otro estilo**. La unidad de comparación es el quipu, con permutación de la etiqueta foco (10 000):

| rasgo | foco | otros | p |
|---|---|---|---|
| vueltas medias | 5,2 | 3,5 | 0,0001 |
| % de racimos con 4–6 vueltas | 71 % | 32 % | 0,0004 |
| % de racimos con ≤3 vueltas | 11 % | 59 % | 0,0001 |
| dirección S | 95 % | 29 % | 0,0003 |
| hueco mediano entre racimos | 14,9 cm | 5,7 cm | 0,0001 |
| homogeneidad dentro de la cuerda | — | — | sin diferencia (p = 0,75) |

  Los "otros" son sobre todo pares cortos `2-2`, `4-2` o `3-2` a 1–10 cm de distancia (UR177, UR037, UR123, AS026B, MM019, UR1145), compatibles con L "inferiores" o con convenciones de registro de quipus decimales (ver 06_nudos), no con este sistema.
- **Conclusión:** las series de largos de 4–7 vueltas, en dirección S y espaciadas unos 15 cm, son **un estilo exclusivo de los quipus de canuto** (cuerdas atadas en fajos envueltos), probablemente post-inka. No es un rasgo general del corpus. La procedencia conocida es casi nula (Valle de Pisco para UR144, "Huari" para UR039; el resto son colecciones Soldi, Banco Central, Museo Oro y Temple Radicati), así que no puedo decir si se trata de un taller o una región.

## 5. Resultados negativos

1. Sin relaciones de suma (aditiva, posicional ni por k), ni dentro del canuto ni con vecinas.
2. Sin calendario (29/30) en cuerdas ni en canutos.
3. Sin etiquetas en posiciones homólogas de los fajos, ni vocabulario compartido entre quipus.
4. Sin estructura de orden en las vueltas más allá de la composición de la cuerda y una tendencia monótona. La información mutua y la curva de Zipf se reproducen con los nulos.
5. Sin techo de radix ni alineamiento en bandas: no son un sistema posicional.
6. El Databook de Ascher no se pudo usar: son PDF escaneados sin texto y no hay equivalentes AS de estos quipus.

**Corrección por comparaciones múltiples:** BH-FDR sobre las 351 pruebas de `tabla_pruebas.csv`. Con B = 2 000 el p mínimo es 0,0005, de modo que **ningún resultado alcanza Holm < 0,05 sobre 351 pruebas** (Holm mínimo 0,175). Los efectos combinados principales tienen q_BH = 0,003. Las pruebas de corpus y estilo (p ≤ 0,0004 con 10 000 permutaciones, 6 pruebas) sobreviven a Holm.

## 6. Niveles de evidencia

- Las series están en el registro (OKR = KFG, racimos separados de un único L): **bien apoyado**. Fiabilidad física de las vueltas: **apoyado**, con la salvedad de la discrepancia sistemática de UR144 entre fuentes.
- Estilo exclusivo de los quipus de canuto (8/8 + UR051) y distinto de las demás series L del corpus: **bien apoyado (descriptivo)**, con contraste por quipu p ≤ 0,0004.
- Vueltas en campana en 4–6, homogeneidad por cuerda, canuto y vecinas, sin bandas: **apoyado con datos**.
- Aditivo, otra base, radix mixto, calendario y códigos categóricos: **rechazados o sin apoyo** (apoyado con datos, negativo).
- "Las vueltas son tamaño de nudo por lote, no un valor; la información está en k, fajo y color": **propuesto**.
- Cualquier lectura silábica de las vueltas (Sivan 2026): **sin apoyo**. Sus indicadores "lingüísticos" se reproducen con nulos no lingüísticos, y sus 4 quipus clave son de esta misma familia.

## 7. Siguiente ronda

1. **Canutos como portadores de información:** la tabla `ascher_canuto_color` del OKR (994 filas) da colores de los envoltorios. Probar si el color del envoltorio, el número de cuerdas por fajo y k o la media de vueltas por fajo se asocian (nulo: permutar fajos dentro del quipu). Es lo que queda en pie.
2. **k como número:** tratar k (número de largos por cuerda) y el total de largos por fajo como los posibles valores, y repetir las pruebas de suma y de repetición con ellos a nivel de fajo.
3. **Reverificar UR144 y UR050 con fotografías** (la discrepancia +3 de UR144; "extremely difficult to read" en UR050) antes de usar vueltas exactas.
4. **Fechado:** si los canutos son coloniales, comparar con quipus coloniales documentados (Curatola y Puente 2013; Setlak 2024).
5. Preparar un nulo de "cobertura léxica" para Sivan con estas mismas cuerdas: asignaciones aleatorias de sílabas a vueltas iid con homogeneidad por cuerda, para medir la cobertura que cabe esperar por azar.
