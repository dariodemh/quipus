# Transcripción borrador de fichas de registro (JC024–JC034) — Open Khipu Repository

**Carpeta de trabajo:** `analisis/ds/n_fichas_jpg/`
**Autor:** equipo DS. **Fecha:** 2026-10-17. **Estado:** BORRADOR para revisión humana.

---

## 1. Pregunta

¿Qué contienen las fichas de registro escaneadas que acompañan a los quipus
`KH0653–KH0663` (aliases `JC024–JC034`) del Open Khipu Repository, y se pueden
convertir en una transcripción de cuerdas (nudos, valor, color, largo) fiable y
comparable con `analisis/datos/cuerdas.csv`?

Objetivos concretos:

1. Identificar qué es cada imagen (ficha de cuerdas, dibujo, foto), su número KH/UR/AS
   y su museo/procedencia.
2. Transcribir las tablas de cuerdas a CSV por ficha.
3. Comprobar la coherencia interna: **valor escrito = suma de nudos transcritos**.
4. Ver si esos KH tienen alias y si ya están en `quipus.csv` / `cuerdas.csv`, y
   comparar cuando exista dato previo.
5. Dejar explícita toda la incertidumbre (celdas con `?`).

## 2. Método

- **Fuente:** `data/external/open-khipu-repository/data/`. Inspección visual directa de
  los JPG con recortes a resolución completa (script `recortar.py`; recortes en
  `recortes/`). No se usó OCR automático: la escritura es manuscrita y el OCR no es
  fiable; todo se leyó a ojo y se marca con `?` lo dudoso.
- **Transcripción:** una fila por cuerda, con la jerarquía de la ficha (`1`, `1s1`,
  `3s2`…). La notación de nudos se copia tal cual: `nTIPO(posición_cm,dirección)`,
  con `S` simple, `L` largo, `E` en ocho; la dirección se escribe `Z` aunque en la
  ficha aparezca como `2` (la grafía del 2 y de la Z es la misma en esta letra).
- **Verificación aritmética** (`verificar.py`): se parsean los racimos y se comprueba
  que su suma, con los valores posicionales implícitos, iguala el `valor` escrito.
  Para cuerdas con un solo racimo la comprobación es **vacua** (1, 10 o 100 dan lo
  mismo): se marca como "posición inferida del valor" y no cuenta como evidencia.
- **Control nulo:** el acuerdo valor↔nudos no es trivial; para cuantificarlo se
  permutan los valores escritos dentro de cada ficha y se cuenta cuántas cuerdas
  coinciden por azar (10 000 permutaciones, semilla 20261017).
- **Corrección múltiple:** Holm sobre las fichas con cuerdas verificables (9) y sobre
  los quipus con relaciones jerárquicas (7).
- **Comparación externa:** búsqueda de alias en `okr-kh-numbers.csv`, presencia en
  `analisis/datos/quipus.csv`, en `khipu.db` y en `cuerdas.csv`.
- **Codificación de cuerdas vacías:** las cuerdas sin nudos se guardan con `nudos`
  vacío y `valor = 0`, siguiendo el brief (0 sin nudos = cuerda ausente, **no** un cero
  real). En la ficha original esas celdas llevan un guion.
- **Archivos:** scripts `recortar.py` (recortes), `verificar.py` (coherencia + JSON),
  `resumen.py` (tabla resumen), `controles.py` (permutaciones, Holm), `comparar_kfg.py`
  (Mann-Whitney vs KFG). Salidas: `transcripcion_*.csv`, `verificacion.json`,
  `resumen.csv`, `comparacion_kfg_fichas.csv`, `recortes/`.

### 2.1 Aviso importante sobre el encargo

El encargo pedía transcribir «los jpg de `KH0631_0632/` y `KH0638_0652/`». **Esas dos
carpetas no contienen fichas de registro en JPG**:

| Carpeta | Contenido real | ¿Ficha de cuerdas? |
|---|---|---|
| `KH0653_0663/` | 11 `JC0xx_record.jpg` (4032×3024) | **Sí**: cada foto muestra una hoja manuscrita de campo + una hoja de tabla mecanografiada/ manuscrita |
| `KH0631_0632/` | `SH 001 upper half with ruler & greyscale.jpeg`, `C14 date for SH001.jpg`, `SH001.xlsx`, `SH001 Description 2023.docx` | **No**: son fotos del quipu y de la fecha C14; los datos están en XLSX/DOCX, no en imagen |
| `KH0638_0652/` | `Croquis KhipusEnlazadosEnglish.jpg` (dibujo), 15 × `KHIPU ENLAZADO-MNAAHP.01–15.xlsx`, 1 DOCX | **No**: es un croquis del conjunto; los datos están en XLSX |

Por tanto la transcripción de tablas se hace sobre las **11 fichas de KH0653_0663**.
De las otras dos carpetas se describe la imagen y se documenta qué falta (§4).

## 3. Inventario y transcripción, ficha por ficha

Todas las fotos de `KH0653_0663` tienen la misma estructura: **una hoja rayada
manuscrita a la izquierda (ficha de campo)** y **una hoja con la tabla de cuerdas a la
derecha** (encabezado impreso `Khipu Number:` rellenado a mano, columnas
`cord | spin/ply/attach. | knots (no., type, pos, direction) | length cm | thickness mm |
color | value | subsidiaries (no., position)`). Las dos hojas están sobre una superficie
clara, en la misma foto; la hoja de la tabla está algo girada. Todas son del
**sitio arqueológico Huacones-Vilcahuasi (PIA El Huarco, Cañete, Lima)**; el museo en
`okr-kh-numbers.csv` figura como «Sitio arqueológico Huacones-Vilcahuasi» con número de
colección (no es un museo: es el proyecto arqueológico).

Convenciones de la ficha: la dirección de los nudos se escribe `2` = **Z**; `S` = nudo
simple, `L` = nudo largo, `E` = nudo en ocho; `d` al final de la línea de nudos queda
**sin interpretar** (¿«down»? ¿marca de «doble»? aparece en la mayoría de cuerdas con
nudo largo final, nunca en cuerdas sin nudos). En la columna `length` casi todas las
cifras llevan una letra pegada (`k`, `b`, `r`, `c`) que tampoco sé interpretar; la
transcribo en `notas` y **no** la uso como unidad (la unidad declarada es cm).

#### Inventario de las 14 imágenes

| # | archivo | qué es | KH / alias | institución |
|---|---|---|---|---|
| 1 | `KH0653_0663/JC024_record.jpg` | ficha de cuerdas (hoja de campo + tabla) | KH0653 / JC024 | Huacones-Vilcahuasi |
| 2 | `JC025_record.jpg` | ficha de cuerdas | KH0654 / JC025 | Huacones-Vilcahuasi |
| 3 | `JC026_record.jpg` | ficha de cuerdas (2 cuerdas, sin nudos) | KH0655 / JC026 | Huacones-Vilcahuasi |
| 4 | `JC027_record.jpg` | ficha de cuerdas | KH0656 / JC027 | Huacones-Vilcahuasi |
| 5 | `JC028_record.jpg` | ficha de cuerdas | KH0657 / JC028 | Huacones-Vilcahuasi |
| 6 | `JC029_record.jpg` | ficha de cuerdas | KH0658 / JC029 | Huacones-Vilcahuasi |
| 7 | `JC030_record.jpg` | ficha de cuerdas | KH0659 / JC030 | Huacones-Vilcahuasi |
| 8 | `JC031_record.jpg` | ficha de cuerdas | KH0660 / JC031 | Huacones-Vilcahuasi |
| 9 | `JC032_record.jpg` | ficha de cuerdas | KH0661 / JC032 | Huacones-Vilcahuasi |
| 10 | `JC033_record.jpg` | ficha de cuerdas | KH0662 / JC033 | Huacones-Vilcahuasi |
| 11 | `JC034_record.jpg` | ficha de cuerdas | KH0663 / JC034 | Huacones-Vilcahuasi |
| 12 | `KH0631_0632/SH 001 upper half with ruler & greyscale.jpeg` | **foto** del quipu con regla (17 cm) y carta de grises | KH0631 / SH001 | Univ. St Andrews |
| 13 | `KH0631_0632/C14 date for SH001.jpg` | **captura** de informe de radiocarbono | KH0631 / SH001 | Univ. St Andrews |
| 14 | `KH0638_0652/Croquis KhipusEnlazadosEnglish.jpg` | **dibujo/esquema** del conjunto enlazado | KH0638–KH0652 / RT-16905 | MNAAHP Lima |

Ninguna de las 11 fichas de Huacones es un dibujo ni una foto del quipu: son **hojas de
registro manuscritas fotografadas**, con la tabla de cuerdas en una hoja aparte dentro de
la misma foto. Todas las fotos son de 4032×3024 px.

### 3.1 JC024 (KH0653) — 16 cuerdas

- **Qué es:** ficha de campo + tabla de cuerdas. **KH0653 / JC024**, Huacones-Vilcahuasi,
  Inv. 789, lote 97, sector F, unidad de excavación 8, capa A-1, elemento 11,
  «Quipu 8», registrado el 1/12/2017 (RAE).
- **Tabla:** 8 colgantes (1–8), cada uno con **1 subsidiaria** (1s1…8s1). Valores
  escritos: 119, 34, 29, 5, 29, –, 19, –, 10, –, 19, –, 5, –, 4, –.
- **Comprobación:** 6 cuerdas verificables, **6/6 coinciden**; 4 con un solo racimo
  (5, 10, 5, 4) no verificables. Modelo posicional: decimal estándar.
- **Dudas:** (a) cord 1 tiene posiciones 3.5/9/7 cm, no monótonas (posible 5.5 en vez
  de 9); (b) el largo de cord 1 sólo aparece escrito a mano sobre el encabezado como
  «16.S 6»; (c) los tramos de color con rangos en cm están emborronados (cord 4 tiene
  cuatro líneas de texto); (d) la anotación de subsidiarias `(1, 6.0)` está en la fila
  de 8s1, pero por posición corresponde al colgante 8.
- **Dato de interés:** JC024 es uno de los tres quipus con **centenas** (119; los otros
  son JC027 = 259 y JC032 = 139) y el único, junto con JC028, con cuerdas de 3 racimos.

### 3.2 JC025 (KH0654) — 10 cuerdas

- **Qué es:** ficha + tabla. **KH0654 / JC025**, Inv. 788, lote 97, sector F, UE 8,
  A-1, elemento 1, «Quipu 7», 1/12/2017.
- **Tabla:** 4 colgantes; el 3 con **3 subsidiarias** (3s1–3s3) y el 4 con 3
  (4s1–4s3). Valores: 17, 26, 39, 1, 14, 15, 37, 1, 13, 29.
- **Comprobación:** 8 verificables, **8/8**; 2 vacuas (3s1 = 1E, 4s1 = 1E).
- **Dudas:** 3s1 es un **nudo en ocho** en la posición 15.0 cm (podría leerse 5.0);
  los largos llevan sufijos b/r/k.
- **Dato de interés:** dos cuerdas valen 1 y son **un solo nudo en ocho** (4s1 y 3s1),
  es decir el «1» se escribe con E, no con S. Todos los colgantes principales son NB
  salvo 3s2/3s3/4s1/4s2/4s3 (W).

### 3.3 JC026 (KH0655) — 2 cuerdas, SIN nudos

- **Qué es:** ficha + tabla. **KH0655 / JC026**, Inv. 792, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 11», 1/12/2017.
- **Tabla:** sólo 2 colgantes, **ambos sin ningún nudo**; en `knots` y en `value` hay un
  guion. Largos 26.0 y 27.0 cm; cord 1 W, cord 2 W(0-24.5)/RD(24.5-27.0).
- **Comprobación:** no aplica (0 nudos). **Es el caso límite del brief: valor 0 sin
  nudos = cuerda ausente, no un cero real.**
- **Dudas:** el largo de cord 1 lleva la anotación «(twisted)» y el de cord 2 «(k)».
- **Dato de interés:** el propio registro lo llama «quipu» aunque no tiene ni un nudo.

### 3.4 JC027 (KH0656) — 12 cuerdas

- **Qué es:** ficha + tabla. **KH0656 / JC027**, Inv. 785, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 4», 1/12/2017.
- **Tabla:** 12 colgantes simples (sin subsidiarias), **todos W**. Valores: 259, 56,
  24, 24, 60, 12, 14, 21, 23, 27, 56, 17.
- **Comprobación:** 11 verificables, **11/11**; 1 vacua (cord 5 = 6S → 60).
- **Dudas:** en cord 1 el 2.º racimo está tapado por una mancha (`?S1(6.0,Z)`); el
  valor escrito 259 exige que sean 5 simples (200+50+9). En cord 8 la posición del
  nudo en ocho es ilegible («30»?).
- **Dato de interés:** es el quipu más «aritmético» del lote: 12 cuerdas, valores
  entre 12 y 259, y un 259 que necesita tres posiciones.

### 3.5 JC028 (KH0657) — 12 cuerdas (8 + 4 subsidiarias)

- **Qué es:** ficha + tabla. **KH0657 / JC028**, Inv. 787, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 6», 1/12/2017.
- **Tabla:** colgantes 1–8; el 7 con 2 subsidiarias (7s1, 7s2) y el 8 con 2
  (8s1, 8s2). Valores: 22, 45, 54, 60, **12**, 41, 48, 9, 2, 46, 17, 3.
- **Comprobación:** 9 verificables, **8/9**; 3 vacuas. **1 descuadre real: cord 5**
  (nudos 4L+2L+3L+5L = 14; el valor escrito parece 12). Es el descuadre más claro del
  lote (el otro es JC032 c1, §3.9).
- **Dato de interés (importante):** en este quipu el registrador **suma varios racimos
  como unidades** en una misma cuerda. Cord 1 = 1S(3.5) + 1E(5.5) + 4L(8.5) +
  3L(12.5) + 4L(15.5) = 10+1+4+3+4 = **22**; cord 4 = 50+6+4 = 60; cord 6 = 30+2+4+5
  = 41. La regla del registrador es «primer racimo = decenas, todo lo demás se suma
  como unidades», no la notación decimal canónica. Afecta a la comparación con KFG.
- **Dudas:** colores con 2–3 tramos y muchísimas manchas de tinta; cord 4 color «LC»
  (no es código Ascher); largo de cord 1 anotado sobre el encabezado.

### 3.6 JC029 (KH0658) — 10 cuerdas

- **Qué es:** ficha + tabla. **KH0658 / JC029**, Inv. 791, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 10», 1/12/2017.
- **Tabla:** colgantes 1–6; subsidiarias 1s1, 2s1, 3s1, 4s1. Valores: 46, 30, 50, 30,
  41, 20, 34, 40, –, –.
- **Comprobación:** 3 verificables, **3/3**; 5 vacuas (cuerdas de un solo racimo). Cord 1 se lee `4S(1.5)+6L(9.5)`
  = 46 (el «6» es clave: con 5 daría 45).
- **Dato de interés:** las cuerdas **5 y 6 no tienen nudos** (cord 5 etiquetada «5(+)»,
  largo 34.0 cm; cord 6, 7.5 cm). Otra vez «quipu» con cuerdas vacías.
- **Dudas:** las posiciones de 3s1 y 1s1 están tapadas por tinta.

### 3.7 JC030 (KH0659) — 5 cuerdas, todas con un solo racimo

- **Qué es:** ficha + tabla. **KH0659 / JC030**, Inv. 793, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 2», 1/12/2017.
- **Tabla:** 5 colgantes, **una sola agrupación de nudos cada uno**: 5L, 6L, 1S, 4L,
  2L → valores 5, 6, 10, 4, 2.
- **Comprobación:** **0 verificables** (todos un solo racimo; 4 son vacuas y el 1S=10
  sólo fija que está en decenas). Este quipu **no aporta evidencia aritmética**.
- **Dato de interés:** la ficha incluye una nota del registrador: «Red (RD) pigment on
  khipu cords could have been wider bands when it was made; there are flecks of red
  w/in some of the YB portions». Es una advertencia metodológica sobre los tramos de
  color, escrita por el propio equipo de Huacones.
- **Dato de interés 2:** la cuerda 3 tiene **un solo nudo simple y valor 10**: el mismo
  nudo que en otras cuerdas vale 1. La posición (12.2 cm) es lo único que lo distingue;
  sin la posición, el valor es ambiguo.

### 3.8 JC031 (KH0660) — 11 filas, 9 colgantes

- **Qué es:** ficha + tabla. **KH0660 / JC031**, Inv. 790, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 9», 1/12/2017. La ficha anota **«Read R-L»** (lectura de
  derecha a izquierda) y **cordón principal roto**.
- **Tabla:** colgantes 1–9; filas de subsidiarias 2s1 y 4s1 (11 filas). Valores:
  11, 1, 1, 4, 8, 3, –, –, –, –, 9.
- **Comprobación:** 4 verificables, **4/4**; 3 vacuas. Todas encajan con el modelo
  «sólo unidades» (`u`), es decir **ninguna cuerda usa decenas**: los valores son
  1, 3, 4, 8, 9, 11 y se obtienen sumando vueltas de nudos largos (2L+9L = 11,
  4L+5L = 9, 2L+6L = 8, 2L+1E = 3).
- **Inconsistencias de la ficha:** (a) la **cuerda 3 declara (1 subsidiaria, 6.0 cm)
  pero no hay fila 3s1** (las de 2 y 4 sí están); (b) las cuerdas **5, 6, 7 y 8 no
  tienen nudos** (4 de 9).
- **Dato de interés:** es el quipu con la **proporción más alta de cuerdas sin nudos**
  (4/9 = 44%) y el que usa exclusivamente la posición de unidades.

### 3.9 JC032 (KH0661) — 8 cuerdas, con una cadena de 3 niveles

- **Qué es:** ficha + tabla. **KH0661 / JC032**, Inv. 786, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 5», 1/12/2017. También «Read R-L»; cordón principal
  29.5 cm, YB, extremo retorcido.
- **Tabla:** colgantes 1–6; **1 tiene subsidiaria 1s1 y ésta a su vez 1s1s1** (única
  cadena de tres niveles del lote). Valores: **139, 78, 61**, 59, 69, 18, 97, 38.
- **Comprobación:** 8 verificables, **7/8**. **Descuadre en cord 1**: los nudos dan
  138 (1S+3S+8L) y el valor escrito «13●9» = 139 (descuadre de 1; el trazo del nudo
  largo es 8, no 9).
- **Hallazgo llamativo:** **78 + 61 = 139**. La madre vale exactamente la suma de su
  hija y su nieta. Es la única relación de este tipo en todo el lote (ver §6.2:
  p nominal 0.011, Holm 0.079, y el propio valor 139 no cuadra con sus nudos → no se
  puede afirmar que sea intencional).
- **Inconsistencia:** cord 2 declara **(1 subsidiaria, 1.0 cm)** pero no hay fila 2s1.
- **Dato de interés:** **6 de 8 cuerdas son YB con una banda roja (RD)**; la ficha usa
  YB/RD en tramos con límites en cm (p. ej. cord 1: YB 0-9.5 / RD 9.5-12 / YB 12-22).

### 3.10 JC033 (KH0662) — 8 cuerdas, la mitad vacías

- **Qué es:** ficha + tabla. **KH0662 / JC033**, Inv. 784, lote 97, sector F, UE 8,
  A-1, elemento 11, «Quipu 3», 1/12/2017. «Read L-R»; cordón principal 13 cm, YB,
  extremos rotos.
- **Tabla:** 8 colgantes. **Cuerdas 1–4 sin nudos** (largos 5.0, 7.5, 4.5, 5.0 cm, todas
  YB). Cuerdas 5–8 con **un solo racimo**: 1E → 1; 4L → 4; 4L → 4; 1S+4L → 14.
- **Comprobación:** sólo **1 verificable** (cord 8), coincide; 3 vacuas.
- **Dato de interés:** 4 de 8 cuerdas sin nudos y largos cortos (4.5–7.5 cm): son
  cuerdas «vacías» que no son ceros. El patrón (4 vacías + 4 con un racimo) sugiere
  pares/estructura, pero con n=8 no se puede concluir nada.

### 3.11 JC034 (KH0663) — 7 cuerdas

- **Qué es:** ficha + tabla. **KH0663 / JC034**, Inv. 782, lote 97, sector F, UE 8,
  A-1, elemento 11, **«Quipu 1»**, 1/12/2017. «Read L-R».
- **Tabla:** colgantes 1–4; cord 1 con **2 subsidiarias** (1s1 sin nudos, 1s2 = 7L) y
  cord 2 con 1 (2s1 = 7L). Valores: 1, –, 7, 2, 7, 17, 17.
- **Comprobación:** 3 verificables, **3/3**; 3 vacuas. Cord 2 = **dos nudos en ocho**
  = 2 (no un 2S).
- **Dato de interés 1:** las cuerdas **3 y 4 son duplicados exactos** (1S(10.0)+7L(20.0)
  = 17, largo 37.5 y 37.0 cm). Duplicados de este tipo son candidatos naturales a
  «repetir una cantidad» y merecen revisión humana.
- **Dato de interés 2 (color):** la ficha lleva una nota metodológica explícita:
  «Red (RO) pigment on YB is coming off but seems to have been present throughout
  these cords, so has been recorded as RO. The primary cord also has some red pigment
  in the YB portions, suggesting it also could have been fully RO-dyed in the past».
  Es decir: **el color RO de este quipu es una reconstrucción, no el color observado**.
  Cualquier análisis de color con estas fichas hereda ese sesgo.

## 4. Las otras dos carpetas: qué hay realmente

### 4.1 `KH0631_0632/` — no hay ficha; hay foto + C14

| archivo | qué es | contenido |
|---|---|---|
| `SH 001 upper half with ruler & greyscale.jpeg` (5184×3456) | **foto** de la mitad superior del quipu SH001, con regla de 17 cm y carta de grises | cordón principal oscuro, grupos de colgantes marrón/blanco/negro; **no hay tabla** |
| `C14 date for SH001.jpg` (2050×1486) | captura de un informe de **radiocarbono** | muestra «KHIPU FIBRE SAMPLE»: **452 ± 27 BP**, calibración 68.3% **1430–1455 calAD**, 95.4% **1420–1475 calAD** (OxCal 4.4.4; laboratorio FTMC-AR85-1) |
| `SH001.xlsx` | libro con hojas `Khipu`, `PrimaryCord`, `Clusters`, `Cords`, `Notes` | **22 cuerdas** en formato KFG (`Cord_Name, Twist, Attachment, Knots, Length, Termination, Thickness, Color, Value, Alt_Value, Position, Notes`) |
| `SH001 Description 2023.docx` | descripción | no leído (fuera del alcance de la tarea de visión) |

- **KH0631 = SH001** (University of St Andrews, SA004); **KH0632 = SH002** (SA005) **no
  tiene ningún archivo en la carpeta**.
- Consecuencia: de esta carpeta **no se puede transcribir ninguna tabla a partir de la
  imagen**; lo que hay es una foto parcial y una fecha C14. La transcripción ya existe
  en `SH001.xlsx` (22 cuerdas) y **no está en `cuerdas.csv`** (ver §7).

### 4.2 `KH0638_0652/` — no hay ficha; hay un croquis y 15 libros

- `Croquis KhipusEnlazadosEnglish.jpg` (3598×2280): **dibujo/esquema**, no tabla.
  Rótulos transcritos: «DIAGRAM 1: “KHIPUS ENLAZADOS”. Khipu RT 16905 MNAAHP Lima.
  Numbers are representing each of the fifteen khipus set. “inicio” and “fin” refers
  to the primary cords that are crossing hubs C, A, B, D and E. Letters are for hubs
  A, B, C, D, E, G, Zone F and Bundle H». Los números 1–15 aparecen cada uno con
  «inicio»/«fin» sobre el mismo dibujo: **los 15 quipus están físicamente enlazados
  (sus cordones principales se cruzan en nudos/haces A, B, C, D, E, G, Zona F y el
  manojo H)**.
- Los 15 `KHIPU ENLAZADO-MNAAHP.01–15.xlsx` contienen, cada uno, la nota «KhipuNN
  MNAAHP is part of a set of “Khipus Enlazados” (15 Khipus)… **Proviene de un
  decomiso, no hay más datos**» y una hoja `pendant_cords` con 5–86 cuerdas
  (≈330 cuerdas en total; el `.15` usa una hoja `wrapped threads` con 20 hilos
  enrollados). **La procedencia es desconocida (decomiso)**, no un museo.
- Consecuencia: **KH0638–KH0652 no son 15 quipus independientes**: son un conjunto
  enlazado. Tratarlos como 15 unidades en cualquier estadística es una decisión
  analítica que hay que justificar (y que puede inflar n). El croquis es la única
  fuente visual de esa estructura, y no se puede convertir en tabla de cuerdas.

## 5. Resultados agregados de las 11 fichas

| ficha | KH | cuerdas | con nudos | sin nudos | subsid. | suma valores | máx | verificables | coinciden |
|---|---|---|---|---|---|---|---|---|---|
| JC024 | KH0653 | 16 | 10 | 6 | 8 | 273 | 119 | 6 | 6 |
| JC025 | KH0654 | 10 | 10 | 0 | 6 | 192 | 39 | 8 | 8 |
| JC026 | KH0655 | 2 | 0 | 2 | 0 | 0 | – | 0 | – |
| JC027 | KH0656 | 12 | 12 | 0 | 0 | 593 | **259** | 11 | 11 |
| JC028 | KH0657 | 12 | 12 | 0 | 4 | 359 | 60 | 9 | 8 |
| JC029 | KH0658 | 10 | 8 | 2 | 4 | 291 | 50 | 3 | 3 |
| JC030 | KH0659 | 5 | 5 | 0 | 0 | 27 | 10 | 0 | – |
| JC031 | KH0660 | 11 | 7 | 4 | 2 | 37 | 11 | 4 | 4 |
| JC032 | KH0661 | 8 | 8 | 0 | 2 | 559 | 139 | 8 | 7 |
| JC033 | KH0662 | 8 | 4 | 4 | 0 | 23 | 14 | 1 | 1 |
| JC034 | KH0663 | 7 | 6 | 1 | 3 | 51 | 17 | 3 | 3 |
| **total** | | **101** | **82** | **19** | **29** | **2405** | 259 | **53** | **51** |

Cifras descriptivas (n = 101 cuerdas transcritas, 82 con nudos):

- **19/101 cuerdas sin nudos (18.8 %)**, en 6 de las 11 fichas. Ninguna de ellas es un
  «cero»: son cuerdas sin ningún nudo (el brief ya avisa de esto).
- Distribución de valores sesgada a lo pequeño: **25 de las 82 cuerdas con nudos valen ≤ 9
  (30.5 %)**, **6 valen 1**, y sólo **3 valen ≥ 100** (119, 139, 259). Mediana de las
  cuerdas con nudos = 18.5.
- Tipos de nudo contados: **L 77, S 58, E 13**. Los nudos en ocho se usan para el 1 y
  el 2 (JC024, JC025, JC032, JC033, JC034), nunca para valores altos.
- Largos: 4.0–53.0 cm, mediana 28.0 cm. El grosor (mm) **no está relleno en ninguna
  ficha**.
- Colores (código principal): **YB 46, W 32, NB 12, RO 6, NB+W 2, MB 2, LC 1**. La
  notación de bandas (`YB(0-9.5)/RD(9.5-12)/YB(12-22)`) es **la misma que usa
  `cuerdas.csv`** (2 143 cuerdas de KFG tienen ese formato), así que es directamente
  convertible.
- **29 filas son subsidiarias** (28.7 % de las cuerdas). La cadena más profunda es
  `1s1s1` (JC032).

## 6. Controles

### 6.1 Coherencia aritmética valor ↔ nudos (control principal)

Se parsean los racimos de cada cuerda y se comprueba si el valor escrito es igual a la
suma con valores posicionales. Para evitar circularidad se prueban **cuatro modelos**
(decimal estándar, decimal invertido, «decenas + resto unidades», «todo unidades») y se
acepta si alguno coincide; el modelo que encaja se reporta.

- **53 cuerdas verificables** (≥2 racimos). **51 coinciden (96.2 %)**; 29 cuerdas tienen
  un solo racimo y **no son verificables** (1, 10 o 100 dan lo mismo).
- **Modelo:** 41 cuerdas encajan con el decimal estándar; **5 encajan sólo con
  «decenas + resto unidades»** (3 en JC028, 2 en JC032: la ficha suma varios racimos
  como unidades).
- **Nulo de permutación** (10 000 permutaciones de los valores dentro de cada ficha,
  semilla 20261017): se esperaban **10.9 aciertos por azar** de 53; se observaron **51**.
  p por ficha y Holm (9 fichas con cuerdas de ≥2 racimos):

| ficha | obs/total | esperado azar | p | p Holm |
|---|---|---|---|---|
| JC025 | 8/8 | 0.98 | 0.0001 | 0.001 |
| JC027 | 11/11 | 1.54 | 0.0001 | 0.001 |
| JC028 | 8/9 | 1.21 | 0.0001 | 0.001 |
| JC032 | 7/8 | 0.87 | 0.0001 | 0.001 |
| JC024 | 6/6 | 1.66 | 0.0059 | 0.029 |
| JC031 | 4/4 | 0.99 | 0.0423 | 0.169 |
| JC029 | 3/3 | 0.99 | 0.1623 | 0.487 |
| JC034 | 3/3 | 1.67 | 0.3365 | 0.673 |
| JC033 | 1/1 | 1.00 | 1.0 | 1.0 |

  **Interpretación:** la coherencia es real y no se explica por azar en 5 de 9 fichas;
  en las 4 restantes el n es demasiado pequeño para detectarla (no es evidencia de
  incoherencia). Es un control de **lectura**, no una prueba sobre los quipus.

- **Sesgo de circularidad:** en **3 cuerdas** la lectura de un dígito se fijó *porque*
  el valor escrito lo exigía (JC024 c1, JC027 c1, JC029 c1; marcadas en los CSV). Si se
  excluyen, la coherencia sigue siendo **48/50 = 96 %**: el resultado no depende de
  esas 3 celdas, pero no son evidencia independiente.

### 6.2 Relaciones jerárquicas (madre = suma de descendientes)

Se comprobó en las **22 cuerdas madre** con descendientes si su valor es la suma de los
valores del subárbol. Nulo: permutación de valores dentro del quipu.

- **2/22 coincidencias exactas**, pero **una es trivial** (JC031 cord 2 = 1, su única
  hija = 1). La única no trivial es **JC032 cord 1 = 139 = 78 + 61** (p nominal 0.011;
  **Holm 0.079** sobre 7 quipus). Además el propio cord 1 tiene nudos que suman 138,
  no 139.
- **Conclusión: NO hay evidencia de suma jerárquica.** 1 caso en 22 pruebas es
  compatible con azar, y el caso está contaminado por un descuadre interno.

### 6.3 Comparación con la base KFG (¿son raros estos quipus?)

A nivel de quipu (unidad = quipu; 11 fichas vs 651 quipus de `cuerdas.csv`; 10 fichas
en las métricas de valor, porque JC026 no tiene nudos), Mann-Whitney bilateral:

| métrica | Huacones (mediana) | KFG (mediana) | p |
|---|---|---|---|
| n.º de cuerdas | **10** | 43 | **8.4 × 10⁻⁶** |
| fracción sin nudos | 0.14 | 0.18 | 0.48 |
| mediana de valor | 17.5 | 10 | 0.58 |
| fracción ≤ 9 | 0.28 | 0.46 | 0.46 |
| fracción ≥ 100 | 0.00 | 0.03 | 0.07 |

- **Único rasgo diferencial: son quipus pequeños** (mediana 10 cuerdas vs 43). En
  estructura de valores y proporción de cuerdas vacías **no se distinguen de KFG**
  (ningún p < 0.07; con Holm, ninguno significativo).
- Esto es un control de plausibilidad: si la transcripción hubiera inventado valores o
  perdido cuerdas, lo esperable sería una anomalía en esta comparación. No la hay.

### 6.4 Incertidumbre declarada

- **74 de 404 celdas (18.3 %) llevan `?`**, casi todas en `color` (bandas y límites en
  cm) y en `notas`; los nudos y valores tienen muchas menos dudas.
- No hay segundo transcriptor: **no se pudo calcular acuerdo inter-anotador**. Es la
  limitación principal de este borrador.

## 7. Comparación externa (alias, bases previas)

| KH | alias | museo/colección (okr-kh-numbers) | en quipus.csv | en cuerdas.csv | en khipu.db |
|---|---|---|---|---|---|
| KH0653–KH0663 | JC024–JC034 | Sitio arqueológico Huacones-Vilcahuasi, Cañete, Lima; núms. 782–792 | **no** | **no** | **no** |
| KH0631 | SH001 | University of St Andrews, SA004 | no | no | no |
| KH0632 | SH002 | University of St Andrews, SA005 | no | no | no |
| KH0638–KH0652 | — | MNAAHP Lima, RT-16905 (decomiso) | no | no | no |

- `quipus.csv`/`cuerdas.csv` (651 quipus KFG) **terminan en JC023 = KH0630**.
- `khipu.db` (619 quipus, 54 403 cuerdas) **termina en KH0630**: no contiene ninguno de
  los 28 quipus de estas tres carpetas.
- **No hay, por tanto, ninguna comparación posible contra `cuerdas.csv`** para las 11
  fichas: mi transcripción es (hasta donde puedo comprobar) el primer dato estructurado
  de estos quipus en el repo.
- **Hallazgo colateral:** `SH001.xlsx` (KH0631) **ya contiene una transcripción en
  formato KFG de 22 cuerdas**, pero SH001 **no está en `cuerdas.csv`** ni en
  `khipu_summary.csv` (650 filas). Es un hueco de la base, no de los datos.

## 8. Resultados negativos y límites

1. **No se puede comparar con KFG**: los 11 quipus (y SH001, y los 15 enlazados) están
   fuera de `cuerdas.csv`, `quipus.csv` y `khipu.db`. Cualquier afirmación sobre su
   significado queda sin contraste externo.
2. **No hay evidencia de suma jerárquica** (§6.2): 1 caso no trivial en 22 pruebas y
   ese caso tiene un descuadre interno de 1.
3. **Dos descuadres sin resolver** en los que la ficha no cuadra consigo misma:
   JC028 cord 5 (valor 12 vs nudos 14) y JC032 cord 1 (valor 139 vs nudos 138).
4. **Dos subsidiarias declaradas sin fila** (JC031 cord 3, JC032 cord 2). No sé si no
   existen, si no se midieron o si se olvidaron de transcribirlas.
5. **No hay fichas para KH0631_0632 ni KH0638_0652**: la tarea de visión sólo se pudo
   hacer en 11 de las 14 imágenes (las otras 3 son 1 foto, 1 captura de C14 y 1 croquis).
6. **KH0632 (SH002) no tiene ningún archivo** en su carpeta.
7. **El color es la columna menos fiable** (18 % de celdas con `?`, manchas de tinta en
   casi todas las fichas) y en JC034 el registrador **reconstruye** el rojo («RO») a
   partir de restos de pigmento. Un análisis de color con estos datos heredaría ese
   sesgo.
8. Los códigos `RO` (6 cuerdas) y `LC` (1) **no existen en `cuerdas.csv`** (RO: 0
   cuerdas; LC: 146, sí existe). `RO` habrá que mapearlo (¿RD? ¿RL?) antes de comparar.
9. El sufijo `d` de las líneas de nudos y las letras pegadas a los largos (`k`, `b`,
   `r`, `c`) **no se han interpretado**: no se usaron para calcular nada.

## 9. Nivel de evidencia

| afirmación | nivel |
|---|---|
| Las 11 imágenes de `KH0653_0663` son fichas de campo + tabla de cuerdas de Huacones-Vilcahuasi, y su contenido está transcrito en 11 CSV | **bien apoyado** (lectura directa; 101 filas) |
| El valor escrito coincide con la suma de los nudos transcritos en 51/53 cuerdas verificables (96 %), muy por encima del azar (10.9 esperados) | **bien apoyado** para la coherencia interna; **apoyado con datos** como indicador de calidad de lectura |
| Hay 19/101 cuerdas sin nudos y ninguna es un cero | **bien apoyado** |
| Los quipus de Huacones son pequeños (mediana 10 cuerdas) pero por lo demás indistinguibles de KFG en valores y cuerdas vacías | **apoyado con datos** (Mann-Whitney, 11 vs 651) |
| JC032 cord 1 = 78 + 61 = 139 podría ser una suma jerárquica intencional | **especulativo** (1 caso, Holm 0.079, descuadre de 1) |
| KH0638–KH0652 son un conjunto enlazado (no 15 quipus independientes) | **bien apoyado** por el croquis y los 15 libros, aunque la consecuencia estadística es una decisión abierta |
| El registro de color de las fichas es reconstruido en parte (RO por restos de pigmento) | **bien apoyado** (nota manuscrita en JC034) |

## 10. Para el coordinador

- **Hecho:** las 11 fotos de `KH0653_0663` son fichas de registro (hoja de campo + tabla
  de cuerdas) del sitio **Huacones-Vilcahuasi** (Cañete, Lima), alias **JC024–JC034**.
  Están transcritas en 11 CSV (`transcripcion_JC0xx_record.csv`), 101 cuerdas en total.
- **Los quipus NO están en ninguna base previa:** `cuerdas.csv`, `quipus.csv` y
  `khipu.db` terminan en **JC023 / KH0630**. No hay contra qué compararlos; esta
  transcripción abre datos nuevos (11 quipus, ~82 cuerdas con nudos).
- **Calidad:** el valor escrito cuadra con la suma de los nudos en **51/53 cuerdas
  verificables (96 %)** frente a **10.9 esperadas por azar** (permutación, Holm: 5 de 9
  fichas significativas). Sin las 3 lecturas guiadas por el valor: 48/50.
- **Caveat grande:** el 18.3 % de las celdas lleva `?` (sobre todo color), **no hay
  segundo transcriptor** y quedan **2 descuadres** (JC028 c5: 12 vs 14; JC032 c1: 139 vs
  138) y **2 subsidiarias declaradas sin fila** (JC031 c3, JC032 c2). Es un borrador:
  que una persona revise los 11 CSV antes de usarlos.
- **Negativo importante:** no hay evidencia de sumas jerárquicas (1 caso no trivial en
  22 pruebas, Holm 0.079). El único candidato (JC032: 78+61=139) tiene además un
  descuadre de 1 en sus propios nudos.
- **Contexto estructural:** con 10 cuerdas de mediana son **quipus pequeños**
  (KFG: 43; p = 8 × 10⁻⁶), pero su mezcla de valores y su 19 % de cuerdas vacías **no
  difieren de KFG** (todos los p > 0.07). Son quipus «normales» en composición.
- **Las otras dos carpetas no tienen fichas:** `KH0631_0632` tiene una foto de SH001 y
  un **C14 de 452±27 BP → 1430–1455 calAD**; `KH0638_0652` tiene un **croquis que
  demuestra que los 15 quipus RT-16905 están físicamente enlazados** (decomiso, sin
  procedencia). Los datos de ambas están en XLSX, no en imagen.
- **Recomendación 1:** pedir a una persona que revise los CSV y resuelva los 4 puntos
  marcados; luego importar las 11 fichas a `cuerdas.csv` (con `okr` = KH0653–0663, sin
  procedencia de museo: el «museo» aquí es el proyecto arqueológico).
- **Recomendación 2:** usar el croquis de RT-16905 para decidir si los 15 «quipus
  enlazados» se modelan como 1 unidad o 15; hoy `okr-kh-numbers.csv` los cuenta como 15
  y eso puede inflar cualquier n.
- **Recomendación 3:** añadir `SH001.xlsx` (22 cuerdas, formato KFG) a `cuerdas.csv`:
  es un quipu datado por C14 y hoy está fuera de la base.
