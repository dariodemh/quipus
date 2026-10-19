# Agronomía del archivo de Incahuasi: calendario, rendimientos y escala de las 9 partes de UR278

**Autor:** equipo de agronomía (n_agronomia) · **Fecha:** 18 de octubre de 2026 · **Semilla:** 20261018

**Pregunta.** ¿Qué puede decir la agronomía del maní, el ají y el frijol de la costa sur central sobre (1) el calendario implícito en un año de 9 meses de 40 días, (2) la escala de 61 790 unidades de UR278, (3) el tamaño de chacra o de grupo de cultivadores que implica cada una de las 9 columnas y (4) si el volumen cabe en el valle de Cañete y en las 4 guarangas de Lunahuaná?

**Respuesta corta.** La agronomía **no respalda** que las 9 columnas sean 9 periodos de cosecha: la firma observada es demasiado plana (CV 0,173; máximo/mínimo 1,64) para cualquier calendario de picos, y ningún modelo de calendario supera el azar tras corrección de Holm (mejor p = 0,028; p Holm = 0,22). En cambio, la escala física es coherente: 61 790 unidades de 82 L son **1 449 t de maní en vaina**, equivalentes a **1 449 ha** a 1 t/ha y a **~116 000 jornadas**, y ocupan **5 067 m³**, el **39–61 %** de la capacidad corregida de Inkawasi (el 82 L se estimó de esa misma capacidad, así que esto es una comprobación de coherencia, no una validación independiente; lo independiente es que 82 L × 0,286 kg/L = 23,5 kg ≈ 1 carga). Ese volumen cabe en el valle de Cañete (3,7 % de la superficie agrícola provincial) pero **no con holgura en el estrecho valle de Lunahuaná** (ocuparía 48–97 % de su superficie cultivable); la mano de obra, en cambio, cabe en las 4 guarangas (~24–36 % de 4 000 hogares nominales) si el registro es la cosecha completa; con una extracción de 1/2 o 1/3, el margen se agota (73–109 %). El archivo es, pues, un registro de escala **valle/provincia**, no de aldea.

---

## 1. Datos y método

### 1.1 Datos del quipu

- **UR278**: tabla canónica de `analisis/13_sistema_incahuasi/ur278_tabla.csv`, 28 filas (grupos de colgantes) × 9 columnas posicionales. Las columnas son la **posición física** del colgante en el grupo (no un orden por valor), según `05_ur278_tabla.py`. 24 filas tienen exactamente 9 colgantes y suman **54 601 unidades**; las 28 filas suman **61 790**. Para composiciones uso las 24 filas completas; para el total, las 28.
- **UR270**: perfil de 9 partes de `analisis/ds/n_rejilla/firma_9_partes.csv` (6 grupos completos, 11 392 unidades). **No es una muestra independiente**: es el detalle de los mismos registros (n_saya_proporcional). Se usa solo como replicación de la firma.
- **Contexto material**: 14 quipus del sistema cubiertos de maní; UR267A/B con ají y UR271 con frijol negro (Urton 2015, ficha `docs/fichas/2015-Urton_inkawasi.md`).
- **Unidad**: bulto de ~82 L, mediana de la capacidad estimada por el volumen de Inkawasi; IC90 51–127 L (`analisis/ds/n_saya_proporcional/informe.md`). Capacidad corregida del sitio: 8 300–13 000 m³ (`analisis/ds/n_hyslop/informe.md`; los escenarios S3–S5 van de 7 944 a 16 200 m³).
- **Población**: Lunahuaná, visita de 1577: **3 276 almas, 740 tributarios, 4 guarangas, 8 curacas** (Rostworowski, *Costa peruana prehispánica*, «Las tasas virreinales»). La cifra es posterior a la epidemia; la población prehispánica fue mayor.

### 1.2 Parámetros agronómicos y su calidad

| Parámetro | Central | Rango | Base | Nivel |
|---|---|---|---|---|
| Volumen del bulto | 82 L | 51–127 (IC90); 30–130 (extremos) | n_saya_proporcional | propuesto |
| Densidad del maní en vaina | **0,286 kg/L** | 0,285–0,289 | medición de vaina GG-20, IJCMAS 2019 (DOI 10.20546/ijcmas.2019.802.354) | demostrado (medición) |
| Peso del bulto de maní | **23,5 kg** | 8,6–37,2 kg | cálculo (30–130 L × 0,286) | apoyado |
| Rendimiento del maní tradicional | 1 000 kg/ha | 700–1 300 | serie 1 200 kg/ha (1920) → 800 (1950), LEISA; ensayo de Cañete 3 437 kg/ha con insumos modernos (UNJFSC 2023) | apoyado |
| Rendimiento del ají seco | 1,5 t/ha | 1,0–2,0 | literatura agronómica; **no verificado en este informe** | especulativo |
| Rendimiento del frijol | 1,0 t/ha | 0,8–1,5 | literatura agronómica; **no verificado** | especulativo |
| Densidad del ají seco | 0,20 kg/L | 0,15–0,25 | supuesto de ingeniería de alimentos | especulativo |
| Densidad del frijol | 0,78 kg/L | 0,75–0,80 | supuesto estándar | especulativo |
| Jornadas de maní | 80/ha | 60–120 | supuesto de agricultura manual | propuesto |
| Hogares por guaranga | 1 000 | nominal | guaranga = 1 000 tributarios; 4 guarangas = 4 000 | propuesto |
| Superficie agrícola provincial | 38 900 ha | — | 8,5 % de 457 716 ha (provincia de Cañete) | apoyado (orden de magnitud) |
| Valle bajo riego | 15 000 ha | 10 000–20 000 | supuesto | especulativo |
| Lunahuaná cultivado | 1 500 ha | — | supuesto | especulativo |
| Capacidad de Inkawasi | 8 300–13 000 m³ | 7 944–16 200 | n_hyslop | propuesto |

**Decisión metodológica.** El maní es el único cultivo con densidad medida y con una serie histórica de rendimiento; por eso la conversión principal se hace sobre maní y los valores de ají y frijol se usan solo como contraste de orden de magnitud. Todos los parámetros discutibles se someten a análisis de sensibilidad (§4.5) y cada escenario del CSV lleva su nivel de evidencia.

### 1.3 Modelos y nulos

1. **Nulo posicional** (UR278): se permutan las 9 etiquetas de columna **dentro de cada fila** (20 000 réplicas). Preserva el total y la composición de cada registro; pregunta si la posición de la columna aporta información sobre la cuota. Es el nulo correcto frente a la pseudorreplicación de cuerdas.
2. **Nulo de calendario**: para cada modelo con un conjunto fijo de *k* periodos de actividad, el estadístico es la cuota media dentro menos la cuota media fuera; el p-valor se obtiene **enumerando exactamente los C(9,k) subconjuntos** de periodos. Es exacto y no depende de supuestos distribucionales.
3. **Corrección múltiple**: Holm sobre los 8 modelos de calendario (familia preespecificada).
4. **Estabilidad**: bootstrap de filas (10 000), split-half (5 000), leave-one-row-out y descomposición de varianza en log(valor).
5. **Escala**: tres niveles de agregación —libro completo (61 790), registro medio (2 207) y columna media (6 866)— para no confundir el archivo con una sola cosecha.

---

## 2. Calendario agronómico y predicción temporal

### 2.1 Ciclos en la costa sur central (Cañete, Chincha, Pisco)

| Cultivo | Ciclo | Siembra en la costa | Cosecha | Campañas/año | Periodos de 40 d ocupados |
|---|---|---|---|---|---|
| **Maní** (*Arachis hypogaea*) | 120–160 d; el ensayo de Cañete se instala de agosto a febrero (ventana de ~6 meses) | agosto–octubre; Guaman Poma: «si es yunga, tarde» | diciembre–marzo | **1 principal**; 2 solo con variedades cortas y riego (2 × 150–160 = 300–320 d) | 3–4 por cosecha; 7–8 para dos |
| **Ají** (*Capsicum* spp.) | 150–210 d al primer corte; planta perenne 2–3 años en la costa sin heladas | agosto–noviembre (almácigo) | febrero–junio y luego corte continuo | 1 establecimiento; cosecha **escalonada** | 5–9 |
| **Frijol** (*Phaseolus vulgaris*) | 90–110 d | septiembre–noviembre; febrero–abril | diciembre–enero; mayo–junio | **2–3** | 2,5–3 por cosecha |

**Calendario inca.** Guaman Poma (cap. 11) pone la preparación de tierras y el inicio de la siembra en julio–agosto («Chacra Yapuy», «Chacra Conacuy»), la cosecha y el llenado de depósitos en mayo («Aymoray Quilla»), y advierte expresamente que en la yunga se siembra **más tarde** que en la sierra. Ese desfase costeño (agosto–octubre) es el que usan los modelos M1–M4. El año de 9 meses × 40 días = 360 + 5 está documentado por un testigo indígena y desarrollado por Rostworowski (n_rostworowski, pp. 914–916); es **uno** de varios calendarios costeños (Cieza habla de 10 meses; las Pléyades regulan el año). Guaman Poma, en cambio, describe 12 meses: no hay un mapeo único de 9 columnas a 12 meses.

### 2.2 ¿Cuántas cosechas caben en 9 periodos de 40 días?

- **Maní:** 360/160 ≈ 2,25 → **2 cosechas teóricas** (300–320 d), con 40–60 d de holgura; en la práctica, la campaña principal (agosto–febrero) deja poco espacio para una segunda de maní, que exigiría siembra en febrero–marzo y cosecha en julio–agosto. **1 cosecha principal, 2 en el límite.**
- **Ají:** una planta perenne entra en producción a los 5–7 meses y se cosecha durante meses; en 9 periodos cabe **1 establecimiento y una cosecha continua**, no 2 ciclos.
- **Frijol:** 360/100 ≈ 3,6 → **3 cosechas** (300 d).

Si las 9 columnas fueran periodos, el patrón esperado no es plano: una cosecha de maní ocupa 2–3 periodos (pico del 50 % en 2 periodos), dos cosechas 4 periodos (25 % cada uno), el frijol 3 picos (33 %), y el ají una meseta de 5–6 periodos (17–20 %). El **CV** de esas cuotas sería 1,98 (2 periodos), 1,19 (4), 1,50 (3) y 0,75–0,95 (5–6), respectivamente.

### 2.3 La firma real no se parece a un calendario de picos

Firma de UR278 (24 filas completas; cuotas sobre 54 601):

| | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 |
|---|---|---|---|---|---|---|---|---|---|
| Cuota | 0,1338 | **0,1373** | 0,0938 | 0,1092 | 0,1155 | 0,1255 | 0,1117 | 0,0836 | 0,0895 |
| Rango | 2 | **1** | 7 | 6 | 4 | 3 | 5 | 9 | 8 |

- Orden: **c2 > c1 > c6 > c5 > c7 > c4 > c3 > c9 > c8**. La firma del encargo (c1 ≈ c2 > c6 > c5 > c7 > c4 > c3 > c9 > c8) se reproduce **en los extremos y en c6**; el centro es frágil: con las 28 filas (incluidas las incompletas) **c7 y c5 se intercambian**. Los extremos (c1–c2 arriba, c8–c9 abajo) sí son robustos (§4.3).
- **CV = 0,173**; máximo/mínimo = **1,64**; las 9 cuotas están entre 8,4 % y 13,7 %. El error de muestreo de cada cuota es ~0,0013 (N = 54 601), muy por debajo de las diferencias entre columnas (0,04–0,06): la firma no es ruido de conteo. No hay periodos «vacíos» ni picos: la columna mayor es 1,64 veces la menor.
- Un calendario de 2 cosechas de maní predice CV ≈ 1,19 y picos de 25 %; uno de 1 cosecha, CV ≈ 1,98 y picos de 50 %. La firma observada es **7–11 veces más plana**. Para reproducirla con picos discretos harían falta **≥ 8 periodos activos** (1/0,137 = 7,3). El argumento es más fuerte de lo que parece: para *k* periodos activos, el CV mínimo se alcanza con pesos iguales, y CV(7) = 0,57 > 0,173; por tanto, **cualquier calendario con la actividad concentrada en 7 periodos o menos queda descartado por la dispersión observada**, aunque los pesos sean desiguales. La firma es **casi un gradiente continuo**, no una secuencia de picos. Eso es lo contrario de un ciclo de 150 días con dos cosechas.

**Pruebas exactas de calendario** (`calendario_modelos.csv`):

| Modelo | Periodos | Cuota dentro | Cuota fuera | p exacta | p Holm |
|---|---|---|---|---|---|
| M7 siembra/preparación en p1–p2 | 2 | 0,1356 | 0,1041 | **0,0278** | 0,222 |
| M2 maní 1 cosecha, año desde junio | 2 | 0,1205 | 0,1084 | 0,278 | 1,00 |
| M1 maní 1 cosecha, año desde enero | 2 | 0,1123 | 0,1108 | 0,472 | 1,00 |
| M4 maní 2 cosechas, año desde junio | 3 | 0,1102 | 0,1116 | 0,560 | 1,00 |
| M6 frijol 3 cosechas | 3 | 0,1030 | 0,1152 | 0,821 | 1,00 |
| M5 ají continuo | 6 | 0,1065 | 0,1202 | 0,833 | 1,00 |
| M3 maní 2 cosechas, año desde enero | 4 | 0,0994 | 0,1204 | 0,960 | 1,00 |
| M8 sin estacionalidad | 9 | 0,1111 | 0,1111 | 1,00 | 1,00 |

**Un control adicional contra la tentación post hoc.** El mejor trío posible de columnas es {c1, c2, c6} (cuota media 0,1322 frente a 0,1005 fuera), con p = 1/84 = 0,012; pero es el máximo de 84 tríos y fue elegido después de ver los datos. Corregido por Holm sobre los 8 modelos quedaría en 0,095 y no es interpretable como confirmación. Lo mismo vale para cualquier subconjunto «que se vea bien»: con 9 columnas, siempre hay un subconjunto que se ajusta por azar.

**Lectura.** Ningún modelo de cosecha se acerca a la significación. El único que se acerca es **M7**, que no es una cosecha sino la **mano de obra de siembra/preparación** en los dos primeros periodos; su p = 0,028 es post hoc (los dos periodos más grandes son c1 y c2) y desaparece tras Holm (0,22). Es un resultado negativo claro: **la agronomía no predice el perfil de columnas como periodos de cosecha**.

**Matiz importante.** Si las columnas registraran **actividad agrícola total** (siembra + deshierbe + cosecha), un perfil plano sí sería posible, porque la mano de obra se reparte. Pero entonces las columnas no son «periodos de cosecha» y el modelo deja de ser falsable con estos datos. La hipótesis «9 columnas = 9 periodos» queda, como mucho, **no refutada pero tampoco apoyada**: especulativa.

**Comparación con UR270.** El perfil de UR270 correlaciona con el de UR278 (Spearman ρ = 0,850; p = 0,0037), pero UR270 es el detalle de los mismos registros: **no es una replicación independiente**. Lo que sí muestra es que la firma no es un artefacto de la tabla de UR278.

---

## 3. Rendimientos, densidad y conversión

### 3.1 Rendimientos sin abono químico y efecto del guano

- **Maní en vaina:** la serie histórica citada por LEISA (no específica del Perú) da **1 200 kg/ha en 1920** y **800 kg/ha en 1950** para agricultura tradicional; el ensayo de Cañete (2017–2018, 5 variedades) alcanza **3 437 kg/ha en vaina** con manejo agronómico convencional. Para el escenario central uso **1 000 kg/ha** y un rango 700–1 300. Nivel: **apoyado con datos** para el rango histórico; el valor prehispánico exacto es una extrapolación.
- **Guano:** hay evidencia isotópica de fertilización con guano de aves marinas en el valle de Chincha **desde ~1250 d.C.**, asociada a aumentos de productividad del maíz (PLOS ONE 2026, DOI 10.1371/journal.pone.0341263; Santana-Sagredo et al. 2021 para Atacama). Para el maní, que es leguminosa y fija nitrógeno, el efecto del guano es sobre todo de **P, K y calcio**, y debe ser **moderado (+10–30 %)**, no el +50–100 % que cabría en maíz. Nivel: **propuesto**; no he encontrado ensayos de guano en maní prehispánico.
- **Ají seco y frijol:** los valores 1,0–2,0 t/ha y 0,8–1,5 t/ha son de la literatura agronómica general y **no los he verificado con un ensayo peruano concreto**. Se usan solo para comparar órdenes de magnitud. Nivel: **especulativo**.

### 3.2 Densidad y peso del bulto

La densidad aparente medida de vaina de maní es **0,286 kg/L** (0,285–0,289; IJCMAS 2019, variedad GG-20, probeta de 1 000 cc). Entonces:

| Volumen | 30 L | 51 L | **82 L** | 127 L | 130 L |
|---|---|---|---|---|---|
| kg de maní en vaina | 8,6 | 14,6 | **23,5** | 36,3 | 37,2 |

**Supuesto crítico.** El 82 L no es una medida directa: se estimó a partir de la capacidad de Inkawasi y de las 61 790 unidades (mediana de una distribución de volúmenes compatibles con esa capacidad), es decir, **suponiendo que todo el libro se almacenó a la vez**. Si el libro cubre varios años o varias comunidades, la capacidad no identifica el volumen unitario y la conversión queda indeterminada (solo la acota por arriba).

El bulto central de 82 L pesa **23,5 kg**, casi exactamente **una carga de 23 kg (50 libras) = 2 arrobas**. Es una convergencia útil: la unidad de capacidad estimada por la arquitectura coincide con una unidad de transporte humana estándar. Nivel: **apoyado con datos** (densidad medida + aritmética), aunque la coincidencia con la carga es **propuesta**.

Para ají seco uso 0,20 kg/L (un bulto de 82 L = 16,4 kg) y para frijol 0,78 kg/L (82 L = 64 kg). El frijol es mucho más denso: **el mismo bulto no transporta el mismo peso de los tres productos**, lo que es relevante si el quipu cuenta *bultos* y no *pesos*.

### 3.3 Conversión de 61 790 unidades (tabla resumida)

Escenario central: 82 L, 0,286 kg/L, 1 000 kg/ha, 80 jornadas/ha, 1 campaña.

| Escenario | Unidades | t | ha (campaña; E4/E7 ha/año) | m³ | % capac. Inkawasi | Jornadas | % de 4 000 hogares |
|---|---|---|---|---|---|---|---|
| E1 mínimo (30 L, 1 200 kg/ha) | 61 790 | 530 | 442 | 1 854 | 14–22 | 26 508 | 8 |
| E2 bajo (51 L, 1 000 kg/ha) | 61 790 | 901 | 901 | 3 151 | 24–38 | 72 102 | 23 |
| **E3 central (82 L, 1 000 kg/ha)** | **61 790** | **1 449** | **1 449** | **5 067** | **39–61** | **115 928** | **36** |
| E4 central, 2 campañas | 61 790 | 1 449 | 1 449 (725/año) | 5 067 | 39–61 | 115 928 | 36 |
| E5 alto (127 L, 800 kg/ha) | 61 790 | 2 244 | 2 805 | 7 847 | 60–95 | 280 542 | 88 |
| E6 máximo (130 L, 700 kg/ha) | 61 790 | 2 297 | 3 282 | 8 033 | 62–97 | 393 832 | 123 |
| E7 central con rinde moderno (2 000 kg/ha) | 61 790 | 1 449 | 725 | 5 067 | 39–61 | 57 964 | 18 |
| **E8 columna media** | **6 866** | **161** | **161** | **563** | **4–7** | **12 881** | **4 (×9 = 36)** |
| E13 registro medio | 2 207 | 51,8 | 52 | 181 | 1–2 | 4 140 | 1,3 |
| E9 cuota 47 | 47 | 1,1 | 1,0 | 4 | 0,0 | 88 | 0,03 |
| E10 cuota 208 | 208 | 4,9 | 4,9 | 17 | 0,1–0,2 | 390 | 0,1 |
| E14 E3 si solo registra 1/3 | 61 790 | 1 449 | 4 347 | 5 067 | 39–61 | 347 784 | 109 |
| E15 E3 si solo registra 1/2 | 61 790 | 1 449 | 2 898 | 5 067 | 39–61 | 231 856 | 73 |

La tabla completa, con supuestos y nivel de evidencia por fila, está en **`escenarios_agronomia.csv`**.

**Tres escalas que no hay que confundir.**

1. **Libro completo (61 790 u.):** 1 449 t, 1 449 ha, 5 067 m³. Es el techo, no una cosecha anual necesariamente.
2. **Registro medio (2 207 u.):** 51,8 t, 52 ha, 4 140 jornadas, ~52 hogares. Es la escala de **una fila**; si cada fila es un registro de recaudación, el libro es un agregado de 28 registros y el total no representa un solo año.
3. **Columna media (6 866 u.):** 161 t, 161 ha, 12 881 jornadas, ~107–161 hogares. Es la escala de **una de las 9 partes**.

### 3.4 ¿Cabe en Cañete y en las 4 guarangas?

- **Tierra.** 1 449 ha son el **3,7 %** de las 38 900 ha agrícolas de la provincia de Cañete y ~**10 %** de un valle bajo riego supuesto de 15 000 ha. Caben en la provincia. Pero el maní no se cultiva en monocultivo: exige rotación por enfermedades del suelo. Si entra **1 de cada 3 años**, el área de rotación sube a **~4 350 ha** (11 % de la provincia, ~29 % del riego supuesto), lo que sigue cabiendo en Cañete pero refuerza que no es un cultivo de aldea. En cambio, en Lunahuaná —un tramo donde la zona irrigada rara vez supera 1,5 km de ancho (Hyslop 1985)— el máximo geométrico es de ~1 500–3 000 ha (1,5 km × 10–20 km de valle), de modo que el maní ocuparía **48–97 %** de la superficie cultivable: posible en el límite, pero **implausible como monocultivo**. El grueso de la producción tuvo que venir del valle bajo del Cañete (Guarco) o de varios valles; Incahuasi, 13 km aguas arriba de la llanura costera, es el punto de acopio, no la chacra.
- **Mano de obra.** 115 928 jornadas a 80 j/ha. Con 4 000 hogares nominales y 80 jornadas por hogar, se necesitan **1 449 hogares = 36 %** de las 4 guarangas. En términos de **tributarios** (un tributario = un hombre adulto; 90–120 jornadas al año), hacen falta **966–1 288 tributarios** (rango 1 932 si se usan 60 jornadas). Los **740 tributarios de 1577** cubren solo el **57 %** con 90 jornadas. El umbral es ~1 300 tributarios a 90 jornadas (o ~1 000 a 120): la población prehispánica tendría que haber sido **1,3–2,6 veces** la de 1577, lo que es plausible tras las epidemias, pero no está demostrado. **La mano de obra cabe en las 4 guarangas; la tierra no cabe con holgura en Lunahuaná.**
- **Si el quipu registra solo una fracción de la cosecha** (E14/E15): con 1/3, el área cultivada sube a 4 347 ha y la mano de obra a 347 784 jornadas (109 % de las 4 guarangas); con 1/2, 2 898 ha y 73 %. Es decir, el registro es compatible con una **tasa de extracción de 1/2 o más**, no con un tercio, si las 4 guarangas son el único reservorio de mano de obra.
- **Consumo per cápita.** 1 449 t para ~20 000 personas (4 000 hogares × 5) son **72,5 kg/persona/año** de maní en vaina (~54 kg de grano, ~150 g/día). Es alto para consumo directo, pero razonable si el destino es **semilla, aceite, renta y aprovisionamiento militar**, o si el libro cubre **2–3 años**. Como cosecha anual de una sola provincia, está en el límite superior.

### 3.5 Las 9 partes como 9 campos o 9 grupos de cultivadores

Cada columna implica **161 t** de maní (a 82 L y 1 000 kg/ha), es decir, **161 ha** de chacra o el equivalente producido por **~107 hogares** a 1,5 ha/hogar, o **~161 hogares** a 80 jornadas/hogar. Las dos lecturas son indistinguibles con el quipu solo:

- **9 chacras del Inca:** 161 ha por chacra es grande para una chacra individual, pero plausible como **bloque de campos estatales**; 9 bloques = 1 449 ha, una parte importante del valle (10 % del riego supuesto).
- **9 grupos de cultivadores:** ~100–160 hogares por columna, 900–1 450 en total, **24–36 % de las 4 guarangas**. Es la lectura que mejor encaja con la escala demográfica y con la organización en guarangas/pachacas; también con la **tendencia a que las columnas decrezcan de izquierda a derecha** (22/24 filas, ρ medio −0,54; §4.2), como una lista jerárquica de unidades, no como campos dispersos. Si una pachaca tiene ~100 hogares, las 4 guarangas contendrían ~40 pachacas; las 9 columnas equivalen a ~9 pachacas, es decir, a **una guaranga**, no a las cuatro. Eso es coherente con un registro de una unidad de leva, no con el censo de toda la provincia.

**Nivel:** **propuesto**. La aritmética es sólida; la identificación de las columnas con grupos sociales es una inferencia, no una prueba. Además, las cuotas cambian con el tamaño del registro (§4.2), de modo que las 9 unidades no tienen tamaños fijos: la lectura de «9 grupos» es **compatible**, no demostrada.

### 3.6 Las cuotas 47 y 208

Como fracción de 61 790, 47 y 208 son **0,076 % y 0,337 %**: 1,1 t y 4,9 t, 1,0 ha y 4,9 ha, 88 y 390 jornadas, **1 y 5 hogares**. Si 47 y 208 fueran cantidades de maní en la misma unidad, serían **escala doméstica**, no provincial. Por tanto: o no son cantidades de maní, o la unidad no es el bulto de 82 L, o son cuotas de otra cosa (cargas, personas, unidades de un producto distinto). **No pueden ser el total de un periodo de una provincia.** Nivel: **demostrado (negativo)** bajo el supuesto de que sean cantidades en la misma unidad.

---

## 4. Controles

**Alcance.** Todas las pruebas de esta sección son **intra-quipu** (UR278): las filas son registros dentro del mismo quipu y no son réplicas independientes. Los p-valores describen la estructura interna de UR278, no la generalización a otros quipus; UR270 comparte los mismos registros y no sirve como réplica independiente. Por eso hablo de «apoyado con datos» y no de «demostrado» en las afirmaciones sobre el significado de las columnas.

### 4.1 Nulo posicional (¿la posición de la columna importa?)

Permutando las 9 etiquetas dentro de cada fila (20 000 réplicas): la correlación entre índice de columna y cuota es **ρ = −0,683**; el nulo tiene media 0,001; **p = 0,0245** (una cola; **0,049 a dos colas**). El R² de la cuota sobre la posición es 0,462; **p = 0,0441** (0,088 a dos colas). Es decir, **la posición aporta información**: las primeras columnas tienden a ser mayores, pero el efecto es marginal, se detectó después de ver los datos y no es confirmatorio; además, 22/24 filas tienen ρ negativo (sign test p = 2 × 10⁻⁵, descriptivo; las filas no son independientes). Lo trato como **apoyado con datos**, no como demostrado.

### 4.2 ¿Es un artefacto de la tabla?

No en el sentido mecánico: las columnas son la **posición física** del colgante, no un orden por valor (`05_ur278_tabla.py`). La tabla no se construyó ordenando valores. Pero hay dos propiedades del quipu que sí son reales:

1. **Tendencia decreciente** dentro de cada fila (22/24 filas con ρ negativo, ρ medio −0,54): sugiere una **lista con tendencia jerárquica** (de mayor a menor) o una convención de registro, no 9 campos independientes.
2. **Dependencia del tamaño del registro.** La cuota de c2 baja con el total de la fila (ρ = −0,64; p = 0,0007; **Holm 0,006**) y la de c7 sube (ρ = +0,58; p = 0,003; **Holm 0,022**); c1 también baja (ρ = −0,51; p = 0,010; Holm 0,070, marginal). c9, en cambio, es plana (ρ = −0,03). Es decir, en los registros grandes las primeras columnas pierden peso y c7 gana: **parte de la firma es un efecto de composición ligado al tamaño del registro**, no una propiedad fija de 9 unidades. Nivel: **apoyado con datos** (Holm sobre 9 correlaciones).

### 4.3 Estabilidad de la firma

Bootstrap de filas (10 000): la probabilidad de que las dos mayores sean c1 y c2 es **0,86**; de que las dos menores sean c8 y c9, **0,83**; el orden completo observado se repite solo en **15,4 %** de las réplicas. Split-half: ρ mediana **0,92** (IC90 0,78–0,98). Leave-one-row-out: el orden completo cambia al quitar **1 de 24** filas (c1/c2 y c8/c9 están casi empatadas). **Conclusión:** los extremos de la firma son robustos; el orden exacto del centro (c3–c7) no lo es.

### 4.4 Descomposición de varianza

En log(valor): **filas 52,1 %**, **columnas 17,3 %**, residuo 30,6 %. El tamaño del registro (la fila) es el factor dominante; el perfil de columnas es una modulación secundaria. Cualquier interpretación de las columnas debe explicar primero por qué todos los registros crecen juntos (efecto de fila), y luego la modulación del 17 %.

### 4.5 Sensibilidad

- **Densidad 0,25–0,32 kg/L:** el total pasa de 1 267 a 1 621 t (±12 %); las hectáreas, de 1 267 a 1 621 (a 1 000 kg/ha, 1 t = 1 ha). No cambia ninguna conclusión.
- **Rendimiento 700–1 300 kg/ha:** las hectáreas van de 1 115 a 2 071 (factor 1,9). La conclusión «cabe en Cañete, no con holgura en Lunahuaná» se mantiene en todo el rango.
- **Volumen 30–130 L:** el total va de 530 a 2 297 t (factor 4,3) y las hectáreas de 442 a 3 282. En el extremo alto, el área es el 8,4 % de la provincia y el 22 % del riego supuesto: sigue cabiendo en Cañete, pero exigiría movilizar casi toda la mano de obra de las 4 guarangas (123 %).
- **Dos campañas:** reducen el área anual a la mitad, no la mano de obra total (se reparte entre dos cosechas).

### 4.6 El ají y el frijol como control de escala

Con los totales brutos de cuerdas de nivel 0 (proxy, no reconstrucción canónica): UR267A+B (ají) ≈ 30 381 unidades; UR271 (frijol) ≈ 8 736; UR278 ≈ 68 403. A 82 L y 0,20 kg/L, el ají serían ~498 t secas, es decir, **~25 kg/persona/año** para 20 000 personas: **implausible como condimento**. El frijol, a 0,78 kg/L, ~559 t, ~28 kg/persona/año: alto pero posible. El desajuste del ají es un **negativo útil**: o el bulto del ají era mucho menor, o los quipus de ají cubren varios años o cuentan otra cosa (plantas, manojos, no bultos). No se puede usar el mismo factor de conversión para los tres productos sin más evidencia.

---

## 5. Resultados negativos (explícitos)

1. **No hay calendario de cosecha que explique la firma.** Ningún modelo de picos supera el azar tras Holm; el mejor (siembra en p1–p2) es post hoc y no sobrevive (p Holm = 0,22).
2. **La firma es demasiado plana para periodos de cosecha.** CV 0,173 y máximo/mínimo 1,64, frente a CV 1,19–1,98 de un calendario de 1–2 cosechas. Harían falta ≥ 8 periodos activos.
3. **Las 9 partes no son iguales.** Van de 8,4 % a 13,7 % (factor 1,64); la hipótesis de 9 partes idénticas se rechaza.
4. **El orden exacto de la firma no es único.** c1/c2 y c8/c9 están casi empatadas; el centro c3–c7 cambia entre las 24 y las 28 filas y en leave-one-out.
5. **El total de 61 790 no es necesariamente una cosecha anual.** Es la suma de 28 registros; la escala por registro es 28 veces menor (~52 t, 52 ha, 52 hogares).
6. **Lunahuaná no tiene tierra suficiente con holgura** para 1 449 ha de maní: aun con el máximo geométrico (1 500–3 000 ha), el maní ocuparía 48–97 % de la superficie cultivable. El valle alto es un cuello de botella, no el reservorio principal.
7. **El ají no escala con el mismo bulto.** 25 kg/persona/año de ají seco es implausible; la unidad o el periodo de los quipus de ají deben ser distintos.
8. **El guano no explica por sí solo rendimientos altos en maní.** Es leguminosa; el efecto esperado es +10–30 %, no +100 %. Los 3 437 kg/ha de Cañete son con manejo agronómico convencional y probablemente fertilización.

---

## 6. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| La densidad del maní en vaina es 0,286 kg/L (variedad medida) y un bulto de 82 L pesa 23,5 kg | **demostrado** (medición + aritmética) |
| La firma de columnas de UR278 es estable en sus extremos (c1–c2 arriba, c8–c9 abajo) | **demostrado para UR278** (bootstrap 0,83–0,86) |
| La posición de la columna aporta información (ρ = −0,68; p = 0,0245) | **apoyado con datos** (post hoc, un solo quipu) |
| La cuota de c9 no depende del tamaño de la fila, pero c2 y c7 sí (ρ = −0,64 y +0,58; Holm 0,006 y 0,022) | **apoyado con datos** (Holm sobre 9) |
| 61 790 unidades a 82 L = 1 449 t = 1 449 ha = 5 067 m³ = 39–61 % de Inkawasi | **demostrado bajo los supuestos** (aritmética) |
| El volumen cabe en Cañete pero no en Lunahuaná | **propuesto** (depende del área de Lunahuaná, que no se midió) |
| La mano de obra cabe en las 4 guarangas (24–36 % de 4 000 hogares) | **propuesto** (depende de 80 j/ha y 80 j/hogar) |
| Cada columna = ~100–160 hogares o ~161 ha | **propuesto** |
| 9 columnas = 9 periodos | **especulativo / no apoyado** |
| 9 columnas = 9 grupos de cultivadores ordenados por tamaño | **propuesto** (la mejor lectura, no demostrada) |
| Guano +10–30 % en maní | **especulativo** |
| Rendimientos de ají y frijol | **especulativo** (no verificados) |

---

## 7. Qué haría falta para la siguiente ronda

1. **Medir densidades reales** de ají seco y frijol en bultos experimentales (no supuestos): cambia la comparación entre productos.
2. **Conseguir un ensayo peruano de maní sin fertilizante** en Cañete/Chincha, con rendimiento y jornadas/ha, para sustituir la extrapolación histórica.
3. **Fechar el archivo**: si las 28 filas de UR278 son 28 registros anuales, 28 comunidades o 28 periodos, la escala cambia 28 veces. Los quipus de UR269 (bloques de 5) y la secuencia de colores pueden ayudar.
4. **Probar la hipótesis de lista ordenada**: comparar el orden físico de los colgantes con el valor en otros quipus de 9 partes; si el orden por tamaño es una convención, la firma no es agronómica.
5. **Buscar el vínculo con las 4 guarangas**: si cada columna es un grupo, ¿hay 9 grupos en la organización de Lunahuaná/Guarco? Los documentos de 1577 dan 4 guarangas × 2 sayas = 8; el noveno podría ser el Inca o un grupo de mitimaes. Es una hipótesis textual, no agronómica.

---

## 8. Para el coordinador

- **La agronomía no salva la hipótesis «9 columnas = 9 periodos».** Ningún calendario de cosecha se ajusta: el mejor modelo da p = 0,028 y Holm = 0,22; los demás, p ≥ 0,27.
- **La firma es demasiado plana para una cosecha.** CV 0,173 y máximo/mínimo 1,64; un calendario de 1–2 cosechas de maní predice CV 1,19–1,98. La columna mayor es apenas 1,64 veces la menor.
- **El bulto de 82 L pesa 23,5 kg, casi una carga de 50 libras.** Ese es el dato independiente: densidad medida (0,286 kg/L) × volumen. Con él, 61 790 bultos = **1 449 t de maní en vaina**, **1 449 ha** a 1 t/ha y **5 067 m³**. El **39–61 %** de la capacidad de Inkawasi es una comprobación de coherencia, no una validación, porque el 82 L se estimó de esa misma capacidad.
- **La escala es de valle, no de aldea.** 1 449 ha = 3,7 % de la superficie agrícola provincial, pero 48–97 % de las 1 500–3 000 ha cultivables del estrecho Lunahuaná: el maní tuvo que venir del valle bajo del Cañete (Guarco) o de varios valles, no solo del tramo de Lunahuaná.
- **La mano de obra sí cabe en las 4 guarangas:** 116 000 jornadas equivalen a 966–1 932 tributarios, es decir, 24–48 % de los 4 000 tributarios nominales (o 1 449 hogares a 80 jornadas). Con los 740 tributarios de 1577 solo se cubriría el 57 %, lo que es coherente con una población prehispánica mayor.
- **Cada columna equivale a ~161 t, ~161 ha y ~100–160 hogares.** Es demasiado para una chacra individual y razonable para un grupo tipo pachaca; la lectura «9 grupos de cultivadores» es la más económica, pero queda en **propuesto**.
- **Las cuotas 47 y 208 no son cantidades provinciales:** 1,1 t y 4,9 t, 1 y 5 hogares. O no son maní, o la unidad no es el bulto de 82 L. **Demostrado (negativo)** bajo ese supuesto.
- **Cuidado con el total:** 61 790 es la suma de 28 registros; por registro son ~52 t, 52 ha y ~52 hogares. Si el libro cubre varios años o varias comunidades, la escala anual se reduce hasta 28 veces.
- **El ají no escala con el mismo bulto:** ~25 kg/persona/año de ají seco es implausible; hay que revisar la unidad de los quipus de ají antes de usarlos como control.

---

### Archivos generados

- `01_datos.py` → `columnas_ur278.csv`, `filas_ur278.csv`, `columnas_dos_versiones.csv`
- `02_calendario.py` → `calendario_modelos.csv`
- `03_conversion.py` → **`escenarios_agronomia.csv`**
- `04_controles.py` → `perfil_columnas.csv`, `columnas_vs_tamano.csv`
- `oa.py`, `bing.py` (utilidades de consulta; `bing.py` se descartó por ruido)

### Fuentes citadas

- Rostworowski, *Costa peruana prehispánica*, «Las tasas virreinales» (visita de 1577: 3 276 almas, 740 tributarios, 4 guarangas) — `analisis/fuentes_txt/Rostworowski_CostaPeruana.txt`.
- Guaman Poma de Ayala, *Nueva corónica*, cap. 11 («El capítulo de los meses del año»), Wikisource: siembra en julio–agosto, «si es yunga, tarde»; cosecha en mayo (Aymoray).
- Urton 2015, ficha `docs/fichas/2015-Urton_inkawasi.md` (asociación maní/ají/frijol).
- IJCMAS 2019, DOI 10.20546/ijcmas.2019.802.354 (densidad de vaina de maní 0,286 g/cc).
- LEISA, «Una plataforma para mejorar la producción de maní» (1 200 kg/ha en 1920 → 800 en 1950).
- Herreros Llamccaya 2023, UNJFSC, ensayo de 5 variedades de maní en Cañete (3 437 kg/ha en vaina; agosto–febrero).
- PLOS ONE 2026, DOI 10.1371/journal.pone.0341263 (guano en Chincha desde ~1250 d.C.).
- `analisis/ds/n_saya_proporcional/informe.md` (bulto 82,4 L; IC90 51,4–126,9).
- `analisis/ds/n_hyslop/informe.md` y `capacidad_escenarios.csv` (capacidad 7 944–16 200 m³; rango usado 8 300–13 000).
- `analisis/ds/n_rostworowski/informe.md` (año de 9 meses × 40 días, pp. 914–916).
- `analisis/13_sistema_incahuasi/ur278_tabla.csv` y `05_ur278_tabla.py` (matriz 28 × 9; columnas = posición física).
- `analisis/ds/n_rejilla/firma_9_partes.csv` (perfil de UR270).
