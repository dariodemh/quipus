# ¿Bultos, raciones o ítems? Prueba independiente de la unidad de medida de Incahuasi

**Equipo:** DeepSeek — carpeta `analisis/ds/n_almacenes/`
**Fecha:** 18 de octubre de 2026
**Semilla:** 20261018 (todo el código es reproducible: `comun.py`, `01_estructura.py`, `02_capacidad.py`, `03_mita.py`, `04_controles.py`, `05_sitios.py`)
**Datos:** reconstrucción de UR278 en `analisis/13_sistema_incahuasi/ur278_tabla.csv` (28 filas × 9 columnas), libro consolidado `13_sistema_incahuasi/libro_consolidado.csv`, `datos/cuerdas.csv` (solo para UR268), Urton (2017) cap. 9 y apéndice, resumen de Urton & Chu (2015) en OpenAlex, y metrología colonial/andina.

---

## 1. Pregunta

`analisis/ds/n_que_se_contaba/informe.md` concluyó que UR278 (61 790 unidades) no cuenta ítems sueltos sino **bultos de 10–50 kg**, y que la unidad exacta es indecidible. Esa conclusión se apoyó en una sola cuenta: el porcentaje de los 6 400 m³ de Qolqawasi que ocuparía el archivo según la masa unitaria.

Esta ronda la pone a prueba **por una vía independiente**, sin reutilizar el argumento del porcentaje de capacidad como si fuera una prueba:

1. ¿Qué dicen la arqueología de Incahuasi y la comparación con otros depósitos incas sobre cuánto cabe y dónde estaban los quipus?
2. ¿Qué masa/volumen implican las unidades de carga andinas (carga de llama, costal, fanega, arroba) y las raciones?
3. ¿Cuántos "periodos" de 61 790 unidades caben en el depósito, y qué extensión temporal implica cada unidad?
4. Si las 9 columnas fueran grupos de trabajo (mit'a) o depósitos, ¿qué fuerza laboral o qué volumen implicaría cada unidad?

La novedad de método: en vez de preguntar "¿qué fracción de capacidad ocupa X?", calculo la **cota inferior de masa unitaria** que hace coherente el archivo con el depósito, y comparo esa cota con las unidades etnohistóricas. También separo la restricción **másica** de la **volumétrica**, que resulta decisiva.

---

## 2. Método

- **Unidad de análisis = el libro (ledger) del quipu, no la cuerda.** Todos los cálculos usan totales de registros o de quipus. No hay tests a nivel de cuerda.
- **Cuatro niveles de ledger** (para no confundir "periodo" con "registro"):
  | nivel | quipu | unidades | registros |
  |---|---|---|---|
  | L1 registro (una entrega) | media de UR278 | 2 207 | 1 |
  | L2 libro de flujo | UR278 (9 columnas) | **61 790** | 28 |
  | L3 libro maestro | UR269 | 122 609 | 67 (~12 bloques de 5–9) |
  | L4 nivel de periodo | UR268 (máximo por grupo) | 300 378 | 30 |
- **Nulos explícitos** en cada prueba (detalle en §5): permutación dentro de fila para la estructura de columnas; uniformidad de dígitos para la granularidad; **prior log-uniforme sobre el tamaño de la unidad** para la coincidencia capacidad–ledger; Monte Carlo sobre rendimientos agrícolas para la mano de obra.
- **Corrección múltiple** BH-FDR en las 5 pruebas de granularidad y Holm en los 6 modelos de unidad.
- **Valores 0 sin nudos = ausentes** (no se usan como ceros).
- Cada conclusión va etiquetada: **bien apoyado / apoyado con datos / propuesto / especulativo**.

---

## 3. La arqueología: qué hay, dónde y cuánto cabe

### 3.1 Qolqawasi (Incahuasi, valle de Cañete, 28 km tierra adentro)

De Urton (2017, cap. 9, que cita a Hyslop 1985) y del resumen de Urton & Chu (2015):

| elemento | cifra | fuente |
|---|---|---|
| estructuras norte | 4 kallankas (U.A. 01, 02, 04, 05) + 2 "espacios de clasificación" sin techo (U.A. 07, 08) | Urton 2017: 158 |
| cámaras grandes rectangulares | **36** (centro, a lo largo del corredor N-S) | ídem |
| colcas pequeñas cuadradas | **209** (oeste, sur, este) | ídem |
| unidades de almacenamiento | **245** | 36 + 209 |
| volumen estimado en uso | **6 400 m³** | Urton 2017: 157, con cita 8 |
| quipus recuperados | **34** (7 en el corredor + 27 en kallankas y espacios de clasificación) | Urton 2017: 159 |
| cuadrícula del piso de U.A. 07 | cuadros de **23 × 23 cm**; paneles de 3 × 39 = 117; ~30 paneles = **3 510 cuadros** | Urton 2017: 158–159 |
| contexto de los quipus | UR267A/B bajo **ají**, en U.A. 07; UR271 bajo **frijol negro**, en U.A. 05; **14 quipus** (entre ellos UR270, UR275, UR278, UR268, UR266) bajo **maní**, en la esquina SO de una kallanka; UR255/256 en el corredor | Urton 2017: 159–161, apéndice |
| productos del sitio | maíz, frijol, maní, ají y otros | Urton 2017: 159 |

**Control de coherencia del volumen.** Los 6 400 m³ se descomponen de forma verosímil: si cada colca pequeña es de 2 × 2 m con 1,3–1,8 m de carga útil (5,2–7,2 m³), las 209 colcas ocupan 1 087–1 505 m³ y quedan **112–148 m³ por cada una de las 36 cámaras grandes** (p. ej. 15 × 6 m con 1,3–1,6 m de carga). Es una planta plausible para salas de recepción y almacenamiento. `05_sitios.py`.

**Comparación con otros conjuntos** (solo número de unidades, porque los volúmenes por qolqa publicados son incompatibles entre sí; ver negativo N5):

| sitio | unidades | referencia |
|---|---|---|
| Qolqawasi | 245 | Urton 2017 |
| Huánuco Pampa | 497 | Morris & Thompson 1970 |
| Mantaro | 2 573 | LeVine 1992; D'Altroy 2003 |
| Cotapachi (Cochabamba) | 2 400 | D'Altroy 2003 |
| Paria | 1 000 | Faldin et al. 2010 |

Incahuasi tiene la mitad de unidades que Huánuco Pampa y una décima parte que el Mantaro, pero sus unidades son mucho mayores (26,1 m³ de media frente a 4–16 m³ de una qolqa redonda). El 6 400 m³ no es una cifra desaforada: cae entre Huánuco Pampa y el Mantaro.

**Lo que la arqueología NO da.** No hay cantidades de producto recuperadas: el maní eran "montones", el frijol "dos puñados". Son depósitos **simbólicos/marcadores**, no el stock. Por tanto **no se puede calibrar la masa unitaria dividiendo kilos excavados entre unidades anotadas** (negativo N3). Es un límite duro y conviene decirlo: la arqueología fija el continente (un depósito de 6 400 m³), no el contenido.

### 3.2 Unidades de carga y medida

| unidad | equivalencia | masa de maíz | volumen |
|---|---|---|---|
| arroba | 25 libras = **11,5 kg** | 11,5 kg | ~15,5 L |
| carga de llama | **2 arrobas = 23–25 kg** (hasta 30) | 23–30 kg | 30–40 L |
| costal (de porte) | saco de 1 arroba a 2 fanegas | 25–50 kg | 33–69 L |
| fanega | 55,5 L (fanega de áridos castellana; en el Perú colonial ~55 L) | 41–45 kg | **55,5 L** |

Fuentes: arroba = 25 libras (metrología castellana; 11,5 kg); carga de llama = "dos ladrillos, o sea, dos arrobas (25 kilogramos)" (capítulo del IHEAL sobre transporte andino); fanega = 55,5 L y 42–45 kg de maíz/trigo (tablas de equivalencias coloniales); costal = saco de transporte, 25–50 kg.

**El dato clave que la ronda anterior no explotó:** estas unidades son **volumétricas** antes que másicas. Una fanega de maíz pesa 43 kg; una fanega de maní con cáscara pesa ~14 kg; una fanega de ají seco, ~17 kg. Si el depósito se llena por volumen (como cualquier almacén), el "bulto" es un **saco de ~30–55 L**, y su masa depende del producto. Esto importa porque los quipus de Incahuasi estaban bajo **maní** y **ají**, los dos productos más ligeros por litro.

**Acceso a las fuentes (transparencia).** El texto de Urton (2017), en el repo (`analisis/fuentes_txt/`), es la fuente primaria para todo lo de Qolqawasi (cap. 9 y apéndice). De **Urton & Chu (2015)** solo hay resumen (OpenAlex; Unpaywall: cerrado). **Hyslop (1985)** no está accesible en línea ni en el repo. **LeVine (1992)** tampoco: uso las cifras de número de qolqas que cita D'Altroy (2003) y las tablas secundarias de metrología. **D'Altroy & Earle (1985)** se consultó solo por resumen (OpenAlex), para el marco general, no para cifras. Por eso el número de unidades por sitio es sólido, pero **los volúmenes por qolqa no lo son** (N5), y no construyo ninguna conclusión sobre ellos.

---

## 4. Resultados

### 4.1 UR278 por dentro: qué se está sumando

`01_estructura.py`:

- 28 filas × 9 columnas, 249 celdas con valor (3 ausentes). Suma de las 9 columnas = **61 790**.
- Celda media **248,2**; mediana 228; rango **11–537**. Fila media 2 015 (rango 875–4 273).
- Por columna: c1 8 218, c2 8 466, c3 5 814, c4 6 722, c5 6 846, c6 8 151, c7 7 104, c8 5 211, c9 5 258.
- **Control de reconstrucción:** sumar la columna `total` da 62 179 (+0,6 %, incluye las cuerdas 10 y 12 de los grupos 18 y 32). Las dos copias del mismo flujo dan 56 986 (UR266) y 56 446 (UR275). La dispersión entre las tres versiones es **9,1 %**, < 0,1 décadas: no cambia ninguna conclusión física.

La tabla de UR278 es, por tanto, un libro de 28 registros × 9 subunidades, con celdas de 11 a 537 unidades. La pregunta es qué pesa/ocupa una unidad.

### 4.2 La prueba de capacidad, bien hecha

Capacidad másica: 6 400 m³ × densidad aparente **0,40–0,70 t/m³** = **2 560–4 480 t**. (La densidad depende del producto: maíz en grano 0,60–0,80; frijol 0,65–0,80; chuño 0,40–0,55; ají seco 0,25–0,40; maní con cáscara 0,20–0,30 t/m³. `02_capacidad.py`.)

Masa y volumen del **libro maestro L3** (122 609 unidades) según la unidad:

| unidad | masa (t) | % del volumen del sitio | llenados del depósito | veredicto |
|---|---|---|---|---|
| ración-persona-día (0,7 kg) | 86–98 | **1,5–2,1 %** | 0,02–0,04 | incompatible |
| arroba (11,5 kg / 15,5 L) | 1 410 | 29–31 % | 0,32–0,55 | posible |
| carga de llama (26,5 kg / 35 L) | 2 820–3 678 | 57–77 % | 0,63–1,44 | posible |
| **costal 25 kg / 34,5 L** | **3 065** | **63–69 %** | **0,68–1,20** | **el mejor ajuste** |
| fanega (43 kg / 55,5 L) | 5 027–5 517 | 106 % | 1,12–2,16 | posible |
| costal 50 kg / 69 L | 6 130 | 126–138 % | 1,37–2,39 | posible (2 turnos) |

Para el nivel superior **L4** (UR268, 300 378 unidades): a 25 kg son 7 509 t = 1,68–2,93 llenados (archivo de 2–3 años); con ración de 0,7 kg son 180–240 t = **3,8–5,2 % del volumen (4–9 % de la masa)** del depósito. Es decir: **ni siquiera el libro de más alto nivel del archivo, interpretado como raciones, llega al 10 % de lo que cabía en Qolqawasi.**

### 4.3 La cota inferior de masa unitaria (el resultado central)

En vez de elegir una unidad y ver si encaja, invierto la pregunta: **¿cuál es la masa unitaria mínima que hace que el archivo quepa en el depósito en T años?** Supuesto: el ledger recoge todo lo que pasó por el depósito en T años y el depósito estaba razonablemente lleno (2 560–4 480 t; uso la densidad mínima, 0,40 t/m³, que es la cota conservadora).

| T (años que cubre el archivo) | cota con L3 (UR269, 122 609) | cota con L4 (UR268, 300 378) |
|---|---|---|
| 1 | 20,9 kg | 8,5 kg |
| 2 | 10,4 kg | 4,3 kg |
| 2,5 | 8,4 kg | **3,4 kg** |
| 5 | 4,2 kg | 1,7 kg |
| 10 | 2,1 kg | 0,85 kg |
| 20 | 1,0 kg | 0,43 kg |

La cota depende de **qué ledger se tome como el registro completo del depósito**:

- Si el archivo completo es el libro maestro L3 (122 609 unidades) y cubre 1–2 años, la unidad no puede bajar de **10,4–20,9 kg**. Es la versión fuerte del argumento y la que reproduce el "10–50 kg" anterior.
- Si el archivo completo es el nivel de periodo L4 (UR268, 300 378 unidades) y cubre ~2,5 años (30 periodos ≈ 30 meses), la cota baja a **3,4 kg**. Es la versión conservadora.
- En **ambas** versiones, los **ítems sueltos (0,3 g) quedan excluidos por 4–5 órdenes de magnitud**. Las **raciones (0,7 kg)** quedan excluidas por un factor 5–15 salvo que el archivo cubriera ≥10 años o representara <10 % del movimiento del depósito.

La cota superior la pone el transporte: una llama carga 23–30 kg y un costal de porte rara vez supera 50 kg. El rango físicamente coherente es, por tanto, **~4–45 kg**, con **10–30 kg** como zona preferente (la única que funciona con los dos ledgers y un archivo de 1–2,5 años).

### 4.4 La restricción volumétrica cambia la conclusión (aporte nuevo)

La ronda anterior trató la unidad como una **masa fija**. Pero el depósito es un volumen y los productos tienen densidades muy distintas. Si la unidad es un **saco de volumen estándar** (costal/fanega, 30–55 L), todo encaja para *todos* los productos:

| producto | densidad (t/m³) | masa de un saco de 35 L | masa de un saco de 55 L |
|---|---|---|---|
| maíz en grano | 0,60–0,80 | 21–28 kg | 33–44 kg |
| frijol | 0,65–0,80 | 23–28 kg | 36–44 kg |
| chuño | 0,40–0,55 | 14–19 kg | 22–30 kg |
| ají seco | 0,25–0,40 | 9–14 kg | 14–22 kg |
| **maní con cáscara** | 0,20–0,30 | **7–11 kg** | **11–17 kg** |

Con una masa fija de 25 kg, el maní con cáscara ocuparía **0,10 m³ por unidad** y el libro maestro L3 (122 609 u.) pediría **12 260 m³**, casi el doble del sitio. Con un saco de 35 L, el mismo ledger pide 4 291 m³ = 67 % del sitio, **cualquiera que sea el producto**. Y los quipus estaban precisamente bajo maní y ají.

**Conclusión:** la unidad es un **bulto de volumen estándar (~30–55 L; ~1/6 a 1 fanega)**, no una masa fija. Su masa va de ~7 kg (maní con cáscara) a ~44 kg (maíz), lo que explica por qué la ronda anterior necesitó el rango "10–50 kg" y por qué ningún valor único encajaba en todos los productos.

**La cuadrícula de 23 × 23 cm: una calibración baja, y una advertencia.** Es la única "regla física" del sitio (3 510 cuadros en U.A. 07). Si un cuadro fuera una unidad de cuenta, su volumen sería el de una capa de 3–10 cm sobre 529 cm²: **1,6–5,3 L**, es decir 1,2–4 kg de maíz o 0,4–1,3 kg de maní. Con esa unidad, el ledger superior L4 (300 378) ocuparía **480–1 590 m³ = 7–25 %** del depósito. No es absurdo, pero deja el depósito tres cuartos vacío y obliga a que el archivo cubra solo una parte del movimiento. No sé la profundidad de llenado ni si un cuadro equivalía a una unidad (Urton y Chu lo describen como plantilla de clasificación, no como contenedor), así que esto es [especulativo] y no lo uso para el veredicto; pero impide afirmar que la unidad *tenía que* ser de 25 kg. El rango honesto sigue siendo 4–45 kg, con 10–30 kg como zona preferente.

### 4.5 ¿Y las 9 partes? Grupos de trabajo frente a depósitos

UR278 tiene 9 columnas con estructura real: CV entre columnas **0,184** frente a **0,059** del nulo de permutación dentro de fila (p = 0,0002, `04_controles.py`). Las columnas no son intercambiables: son 9 subunidades estables.

**(a) Si son 9 cuadrillas de mit'a.** Con 61 790 unidades repartidas en 9 grupos, cada grupo produce 61 790/9 × masa. Trabajadores necesarios por grupo (Monte Carlo sobre rendimiento por jornal 30–600 kg/día según cultivo y temporada de 20–60 días; `03_mita.py`):

| unidad | total (t) | t por grupo | maíz: trab./grupo | maní: trab./grupo | ají: trab./grupo |
|---|---|---|---|---|---|
| ración 0,7 kg | 43 | 4,8 | **0,6** (0,3–1,4) | 2,3 (1,2–4,9) | 7,9 (4,0–17,6) |
| arroba 11,5 kg | 711 | 79 | 11 | 39 | 129 |
| **costal 25 kg** | **1 545** | **172** | **23** (12–50) | **84** (44–175) | **281** (144–621) |
| fanega 43 kg | 2 657 | 295 | 40 (21–87) | 145 (77–303) | 480 (247–1 064) |

Con bultos, las 9 cuadrillas suman **54–450 trabajadores** si el producto es chuño o maíz, **400–1 600** si es maní y **1 300–5 600** si es ají. Son cifras de contingente mit'a perfectamente normales para una instalación estatal de esta escala. Con raciones, cada "cuadrilla" tendría **menos de un trabajador**: el absurdo es aritmético, no retórico.

**(b) Si son 9 depósitos.** Cada columna totaliza 5 211–8 466 unidades. Con sacos de 35 L: 182–296 m³ = **1,2–2,0 cámaras grandes** (151 m³ útiles cada una) por ledger. Con arrobas de 15,5 L: 0,5–0,9 cámaras. Es decir, cada columna equivale a **una o dos cámaras** por periodo: exactamente lo que se espera de un libro que reparte un flujo entre los 9 sectores de un depósito.

Ambas lecturas (cuadrillas y depósitos) son compatibles con bultos; ninguna lo es con raciones.

### 4.6 La cuota 47 (y 17, 10): qué magnitud tiene

La cuota es constante en unidades por registro (47 en el flujo "47"; 30 + 17 en sus componentes; 15 + 10 en el flujo "25"). Su interpretación física:

| lectura de 47 | masa por registro | % del registro medio (2 207 u.) |
|---|---|---|
| 47 ítems (grano) | 14 g | 2,1 % |
| 47 raciones | 33 kg | 2,1 % |
| **47 bultos de 25 kg** | **1 175 kg** | **2,1 %** |
| 47 fanegas | 2 021 kg | 2,1 % |

El **porcentaje es idéntico por construcción** (47/2 207), así que la cuota no discrimina por sí sola. Lo que sí es informativo:

- La cuota es un **número fijo absoluto** (47) mientras el bruto del registro varía 3,8× (875–4 273). No es un impuesto proporcional: es un **número fijo de unidades por entrega**, como un "47 sacos por partida". Eso encaja con un **contenedor contado**, no con una masa variable.
- Las cuotas de los cinco flujos del libro maestro son **47, 46, 46, 44 y 25**: casi iguales entre flujos. Si cada flujo fuera un producto distinto y la cuota fuera una masa fija, las cuotas en *unidades* tendrían que diferir según el producto (un saco de maní pesa la mitad que uno de maíz). Que sean casi idénticas favorece un **mismo número de sacos**, no una misma masa. [especulativo, pero coherente con §4.4]

### 4.7 Logística de caravana (prueba de plausibilidad independiente)

Registro medio del flujo = 2 207 unidades = 55 t a 25 kg. Una llama carga 25 kg:

- **2 207 cargas de llama por registro.** Si un registro fuera una sola entrega, sería una caravana imposible (las mayores documentadas son de cientos a ~1 000 animales).
- Si un registro es un **periodo mensual**, son 74 cargas/día: una caravana mediana, perfectamente normal.
- A 0,7 kg el registro serían 62 cargas: una caravana pequeña, pero entonces el depósito estaría al 2 % (absurdo).

Es decir, la logística de caravana **obliga a que el registro sea un periodo agregado (semanas o un mes), no una entrega única**. Con 28–33 registros, el libro del flujo cubriría **~2–3 años**, que es justo el horizonte en el que la cota de §4.3 exige ≥4–10 kg según el ledger. [propuesto: la coherencia es real, pero depende de que el registro sea mensual, cosa no bien apoyada]

---

## 5. Controles

### 5.1 Nulos y p-valores

| prueba | estadístico | nulo | resultado | p / q |
|---|---|---|---|---|
| Estructura de columnas UR278 | CV entre columnas 0,184 | permutar celdas dentro de fila (5 000 réplicas) | nulo 0,059 [p95 0,084] | **p = 0,0002** |
| Granularidad: múltiplos de 2 | 0,494 | dígitos uniformes 0/1 (20 000) | esperado 0,500 | p = 0,60; q = 0,92 |
| múltiplos de 5 | 0,217 | ídem | 0,200 | p = 0,27; q = 0,92 |
| múltiplos de 10 | 0,076 | ídem | 0,100 | p = 0,92; q = 0,92 |
| múltiplos de 25 | 0,040 | ídem | 0,040 | p = 0,54; q = 0,92 |
| múltiplos de 50 | 0,016 | ídem | 0,020 | p = 0,73; q = 0,92 |
| Coincidencia capacidad–ledger (6 modelos) | \|log₁₀(volumen/capacidad)\| | prior log-uniforme de volumen unitario 5·10⁻⁵–0,5 m³ | ver §5.2 | Holm mínimo **0,080** |

- **BH-FDR (5 pruebas de granularidad): ninguna significativa** (q = 0,915). Las celdas de UR278 **no** se agrupan en lotes redondos: no hay exceso de pares (0,494), ni de múltiplos de 5 (0,217), ni de 10 (0,076, *por debajo* de lo esperado). Si los quipucamayoc contaran "sacos por pares de llama" o "decenas de costales", se vería un exceso; no está.
- **Dígito final de las celdas:** χ² = 17,7 (9 gl), p = 0,039 sin corregir — pero el exceso está en los dígitos 1, 4 y 5, y el **déficit en 0 y 9**, que es lo contrario de lo que produciría un recuento de lotes redondos. No lo interpreto (es una prueba única entre muchas y el patrón no tiene sentido teórico).
- **Holm (6 modelos de unidad):** el mejor ajuste (fanega, p = 0,013) queda en **q = 0,080**. Ningún modelo se distingue.

### 5.2 El test de coincidencia, explicado (y por qué no es una prueba)

Un lector podría objetar: "si el ledger cabe justo en el depósito, eso confirma la unidad". No. Bajo ignorancia total del volumen unitario (log-uniforme entre 5·10⁻⁵ y 0,5 m³, cuatro décadas), la probabilidad de que un ledger de ~10⁵ unidades caiga **dentro de un factor 2** de la capacidad es **0,15**; dentro de un factor 1,25, **0,048**. Es decir: la coincidencia que la ronda anterior presentó como apoyo es **estadísticamente barata**. Su valor real es otro: **excluye** unidades que se alejan 2–4 órdenes de magnitud (ítems, raciones), no **confirma** 25 kg frente a 11 o 43 kg.

Formulación correcta del resultado: *"la capacidad física pone una cota inferior a la masa unitaria; no identifica la unidad"*.

### 5.3 Robustez

- **Total del ledger:** 56 446 / 56 986 / 61 790 / 62 179 según la versión (dispersión 9,1 %). Todos los cálculos se mueven < 0,1 décadas.
- **Volumen del sitio:** si 6 400 m³ fuera 3× demasiado (2 112 m³), el ledger maestro a 25 kg serían 2,1–3,6 llenados en vez de 0,7–1,2: sigue siendo un archivo de depósito. **La exclusión de raciones e ítems es robusta a un error de 3× en la capacidad** (con raciones, aun con 1/3 del volumen, el archivo sería el 5–6 % del depósito).
- **Reconstrucción de UR278:** la suma de las 9 columnas coincide con la tabla de `13_sistema_incahuasi` y con las copias UR266/UR275 en orden (τ = 1). No hay dependencia de una reconstrucción mía.

---

## 6. Resultados negativos (los que también cuentan)

- **N1. La capacidad no distingue entre bultos.** Arroba (0,32–0,55 llenados), costal de 25 kg (0,68–1,20), carga de llama (0,63–1,44) y fanega (1,12–2,16) son todos compatibles con un archivo de depósito. Tras Holm, **ninguno** se distingue (q ≥ 0,080). Decir "25 kg" en vez de "11,5 kg" o "43 kg" **no está justificado por la arqueología**.
- **N2. No hay granularidad de lotes.** Ninguna prueba de múltiplos sobrevive BH (q = 0,92). Las cifras se comportan como recuentos continuos, no como "N sacos de 50" o "N pares de cargas".
- **N3. No hay calibración directa por el producto excavado.** Urton (2017) describe "montones" de maní y "dos puñados" de frijol: son depósitos marcadores, no el stock. **No se puede dividir masa excavada entre unidades anotadas.** La arqueología de Incahuasi no publica ni un kilo.
- **N4. Inconsistencia de fuente sobre el edificio.** El texto de Urton (2017: 159 y 1822) sitúa los 14 quipus del maní en la **U.A. 05**, pero el apéndice y el pasaje de la p. 1836 dicen **U.A. 04**. La esquina suroeste de una kallanka, sí; el número de unidad de análisis, no está claro. Afecta a cualquier intento de asociar un quipu a un espacio concreto.
- **N5. Los volúmenes por qolqa publicados son incoherentes.** D'Altroy (1992: 175), vía Wikipedia, da 3,7–5,5 m³ para una qolqa de 3,23 m de diámetro interior; un cilindro de 3,23 m × 2 m son 16 m³. No usé esa cifra para extrapolar (solo comparé números de unidades). Cualquier cálculo de capacidad agregada a partir de "nº de qolqas × 5 m³" es dudoso.
- **N6. El lapso temporal del archivo no está determinado.** Es el eslabón más débil de todo el argumento: si el archivo cubriera 20 años, la cota inferior de masa unitaria baja a 0,4–1 kg y las raciones volverían a ser (apenas) posibles. La arqueología no fecha los quipus con precisión suficiente (Cherkinsky & Urton 2014 no distingue inca tardío de colonial temprano en esta muestra).
- **N7. La lectura "registro = mes" no está bien apoyada.** Es la hipótesis que hace coherentes la logística de caravana (74 cargas/día) y la cota de masa (≥4–10 kg para 2–3 años), pero no hay evidencia independiente de que cada fila de UR278 sea un mes.
- **N8. Las 9 columnas como "depósitos" siguen siendo especulativas.** La estructura de columna es bien apoyada; su referente (depósitos, cuadrillas, días, ayllus) no.

---

## 7. Tabla de escenarios y veredicto

Supuestos explícitos: capacidad 6 400 m³; densidad 0,40–0,70 t/m³; ledger de referencia L2 = 61 790 (flujo) y L3 = 122 609 (maestro); archivo de 1–3 años.

| # | Hipótesis de unidad | Masa del ledger L3 | % capacidad (vol.) | Cuadrilla (9 grupos, maíz) | Caravana por registro | Veredicto | Nivel |
|---|---|---|---|---|---|---|---|
| 1 | **Ítem suelto** (grano, ají, papa, mazorca) | 0,04–31 t | 0,001–1,6 % | < 0,3 trab. | ~0,03–22 cargas | **descartada** | bien apoyado (cota física) |
| 2 | **Ración-persona-día** (0,7 kg) | 86–98 t | 1,5–2,1 % | 0,3–1,4 trab. | 62 cargas | **descartada** | apoyado con datos |
| 2b | **Cuadro de 23 × 23 cm** (1,6–5,3 L) | 0,15–0,5 t | 3–10 % | 1–4 trab. | 180–530 cargas | posible pero deja el depósito al 7–25 % | especulativo |
| 3 | **Arroba** (11,5 kg) | 1 410 t | 29–31 % | 11 trab. | 1 015 cargas | posible; no preferida | propuesto |
| 4 | **Carga de llama** (23–30 kg) | 2 820–3 678 t | 57–77 % | 20–27 trab. | 2 200 cargas | **compatible** | apoyado con datos |
| 5 | **Costal de volumen 30–40 L** (7–28 kg según producto) | 860–3 430 t | 55–69 % | 7–27 trab. | ~2 000 cargas | **el más coherente** | propuesto |
| 6 | **Fanega / costal 50–55 L** (11–44 kg) | 1 350–5 517 t | 106 % | 25–45 trab. | ~3 800 cargas | compatible (2 turnos/año) | propuesto |
| 7 | Producto individual + 9 depósitos | — | — | — | — | descartada | bien apoyado |

**Respuesta a la pregunta del encargo:**

- **¿Cuántos bultos caben en Incahuasi?** Entre **~51 000 y ~179 000** bultos de 25–50 kg (2 560–4 480 t), o **~130 000–210 000** sacos de 30–50 L. UR278 (61 790) es **el 32–35 % del volumen del sitio**; el libro maestro L3 (122 609) es **el 63–69 %**, y el nivel de periodo L4 (300 378) pide **1,7–2,9 llenados**.
- **¿Es compatible 61 790 por periodo?** Sí, si "periodo" = libro de un flujo (28 registros, ~1–3 años). **No** si "periodo" = un registro (2 207 unidades = 1,2 % del volumen, una entrega normal). La cifra de 61 790 **no es un periodo administrativo**: es un libro de 28 registros.
- **¿Con cuotas 47/17/10 por unidad?** Sí en el sentido débil (todas las lecturas dan 2,1 % del registro, trivial), y **sí en el sentido fuerte de "47 sacos"**: la cuota es un número fijo de contenedores por partida, casi idéntico entre flujos (47, 46, 46, 44, 25), lo que favorece un **contenedor contado** sobre una masa. Nivel: propuesto.
- **¿Cuánto produce un grupo por temporada?** Con bultos, **172 t por grupo** (costal 25 kg) en una temporada, lo que exige **23–84 trabajadores por grupo** (54–450 en total para chuño/maíz; 400–1 600 para maní; 1 300–5 600 para ají). Con raciones, **4,8 t por grupo**: menos de un trabajador. La hipótesis de las 9 cuadrillas **solo funciona con bultos**.

---

## 8. Nivel de evidencia (resumen)

| afirmación | nivel |
|---|---|
| UR278 = 28 registros × 9 subunidades; 61 790 unidades; estructura de columna real (p = 0,0002) | **bien apoyado** |
| La unidad no es un ítem suelto (grano, ají, papa, mazorca) | **bien apoyado** (cota física: 4–5 órdenes de magnitud) |
| La unidad no es una ración-persona-día | **apoyado con datos** (1,5–5 % del depósito aun en el ledger superior; excluida salvo archivo ≥10 años o <10 % del movimiento) |
| La unidad es un bulto de **~4–45 kg** (zona preferente 10–30 kg) | **apoyado con datos** (cota inferior 3,4–10,4 kg según ledger y plazo; superior por la llama) |
| La unidad es un **volumen estándar de ~30–55 L**, con masa variable por producto (7–44 kg) | **propuesto** (resuelve el caso del maní, que la masa fija de 25 kg no resuelve) |
| La unidad exacta (arroba vs costal vs fanega) | **indecidible** con estos datos (Holm q ≥ 0,08) |
| Las 9 columnas son cuadrillas de mit'a de 20–90 trabajadores | **propuesto** (compatible, no bien apoyado) |
| Las 9 columnas son 9 depósitos/cámaras (1–2 cámaras por columna) | **propuesto** |
| La cuota 47 son 47 sacos por partida | **propuesto** |
| Cada fila de UR278 es un mes y el archivo cubre 2–3 años | **especulativo** |

---

## 9. Para el coordinador

- **La conclusión de `n_que_se_contaba` se sostiene, pero por una razón distinta y más fuerte.** No es que "61 790 unidades ocupen el 48 % del depósito si son de 30 kg": es que, para que el archivo quepa en Qolqawasi en un plazo corto (1–2,5 años), **la unidad no puede pesar menos de 3,4–10,4 kg**. La cota sale de dividir la capacidad (6 400 m³ × 0,40–0,70 t/m³ = 2 560–4 480 t) entre el ledger completo (122 609 o 300 378 unidades) y el plazo. Los ítems sueltos quedan excluidos por 4–5 órdenes de magnitud; las raciones, al 1,5–5 % del depósito.
- **Aporte nuevo: la unidad es un volumen, no una masa.** Con 25 kg fijos, el maní con cáscara —el producto bajo el que estaban 14 de los 34 quipus— pediría 12 260 m³, el doble del sitio. Con un **saco de 30–55 L**, el mismo ledger pide 55–69 % del volumen **para cualquier producto**. La masa del bulto va de ~7 kg (maní) a ~44 kg (maíz). Eso reinterpreta el "10–50 kg" anterior como "**1/6 a 1 fanega**".
- **La arqueología no puede elegir la unidad exacta, y lo dice con números.** Arroba (0,32–0,55 llenados), costal (0,68–1,20), carga de llama (0,63–1,44) y fanega (1,12–2,16) son todos compatibles; tras Holm, q ≥ 0,080. Cualquier afirmación del tipo "contaban costales de 25 kg" es **propuesta**, no resultado.
- **El test de coincidencia es barato y hay que dejar de usarlo como prueba.** Con ignorancia log-uniforme del volumen unitario, la probabilidad de que un ledger de 10⁵ unidades caiga dentro de un factor 2 de la capacidad es **0,15**. La capacidad sirve para **excluir** unidades, no para **confirmar** una.
- **Las 9 partes funcionan como cuadrillas solo con bultos.** Con costal de 25 kg, cada grupo produce 172 t/temporada y necesita **23 trabajadores (maíz), 84 (maní) o 281 (ají)**; en total, **54–450 mitayos** si el producto es chuño/maíz, **400–1 600** si es maní y **1 300–5 600** si es ají. Con raciones, cada cuadrilla tendría **0,6 trabajadores**: la hipótesis se autodestruye.
- **Como depósitos, las 9 columnas también cierran:** cada columna (5 211–8 466 unidades) equivale a **1,2–2,0 cámaras grandes** de 151 m³ por ledger, con sacos de 35 L. Es la primera vez que el sistema de 9 partes tiene una contrapartida física verosímil, aunque sea [propuesto].
- **La cuota 47 es un número fijo de contenedores, no un porcentaje.** Las cuotas de los cinco flujos del libro maestro son 47, 46, 46, 44 y 25: casi idénticas. Si fueran masas fijas y los flujos fueran productos distintos, las cuotas en unidades tendrían que diferir (un saco de maní pesa la mitad que uno de maíz). Favorece "47 sacos por partida" [propuesto].
- **Negativos que conviene registrar:** (i) no hay granularidad de lotes en las cifras (q = 0,92: ni pares, ni decenas, ni múltiplos de 25); (ii) no hay ni un kilo de producto publicado en Incahuasi, así que no hay calibración directa; (iii) Urton (2017) se contradice entre U.A. 04 y U.A. 05 para los 14 quipus del maní; (iv) los volúmenes por qolqa de la literatura son geométricamente incoherentes (3,7–5,5 m³ para un cilindro de 3,23 m de diámetro) y no deben usarse para extrapolar capacidades.
- **El eslabón débil es el tiempo.** Si el archivo cubriera 20 años, la cota de masa bajaría a 0,4–1 kg. La logística de caravana (2 207 cargas de 25 kg por registro) obliga a que cada fila sea un **periodo agregado** (74 cargas/día si es un mes), lo que con 28–33 filas da 2–3 años y cierra el círculo. Pero es [especulativo]: **la prioridad de la próxima ronda debería ser datar el archivo y decidir si las filas de UR278 son meses, semanas o entregas.**
- **Recomendación concreta:** buscar en el archivo de Chu/Hyslop las **dimensiones de las 36 cámaras** (no solo el total de 6 400 m³) y el **volumen de relleno** de las colcas; con una sola cámara medida se podría convertir "1,2–2,0 cámaras por columna" en una prueba de volumen con denominador observado. Y no volver a usar el porcentaje de capacidad como confirmación: usarlo solo como cota.

---

## Anexo: archivos

| archivo | contenido |
|---|---|
| `comun.py` | constantes, densidades, unidades, semilla |
| `01_estructura.py` | totales de UR278, granularidad, estructura de columnas, libro consolidado → `ur278_filas.csv`, `resumen_ur278.json` |
| `02_capacidad.py` | capacidad, escenarios de unidad, cota de masa, coincidencia, cuadrícula, caravanas, raciones → `capacidad_escenarios.csv` |
| `03_mita.py` | cuadrillas de mit'a, 9 depósitos, ritmo diario → `mita_escenarios.csv` |
| `04_controles.py` | BH/Holm, permutación de columnas, robustez del total |
| `05_sitios.py` | descomposición del volumen, comparación con otros sitios, sensibilidad |
| `06_verificacion.py` | assert de las 24 cifras citadas en este informe (todas OK) |
