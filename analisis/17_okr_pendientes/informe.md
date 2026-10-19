# 17 · OKR pendientes: tabla puente y datos sin integrar

Tarea de datos (no de interpretación). Todo lo de aquí es conteo o comparación de registros; no hay inferencia estadística ni resultados sobre significado.

Archivos de esta carpeta:

| archivo | contenido |
|---|---|
| `puente.py` | construye `puente.csv` y `puente_conteos.txt` (solo stdlib) |
| `puente.csv` | una fila por KH (702 filas) |
| `puente_conteos.txt` | conteos completos, listas de alias duplicados e inventarios compartidos |
| `comparar_as1_as9.py` | comparación de AS1-AS9.db con KFG (solo lectura) |
| `parte_b_xlsx.py` | conversión de los xlsx de KH0631-KH0702 que no están en KFG |
| `cuerdas_extra.csv` | 776 cuerdas de 19 quipus nuevos, mismo esquema que `analisis/datos/cuerdas.csv` |
| `inventario_manual.py` / `inventario_manual.csv` | inventario de jpg, pdf, docx y xlsx no convertidos |

No se ha modificado nada fuera de esta carpeta, ni `analisis/datos/`, ni `scripts/construir_tabla.py`.

---

## 1. Parte A. Tabla puente KH ↔ AS/UR ↔ KFG ↔ khipu.db

### 1.1 Fuentes y correcciones a la brief

- `okr-kh-numbers.csv` tiene **702 filas** (no 760). La cifra de 760 coincide con el número de líneas del fichero (761 con cabecera), porque hay celdas con saltos de línea dentro de comillas.
- `khipu.db` (`khipu_main`): 619 filas, `OKR_NUM` único por fila, y todos los `OKR_NUM` están en la lista de 702.
- `analisis/datos/quipus.csv`: 651 filas (una por xlsx). La columna `okr` trae un KH en 593 filas y un nombre (AS/UR/QU/MM…) en las restantes.
- Se usó también `data/external/data-science-khipu-article/data/khipu_summary.csv` (650 filas, con `khipu_id` = `KHIPU_ID` de khipu.db) y `KFG_DB.SQL` (685 filas en `khipu_main`) para explicar las cifras.

### 1.2 Reglas de normalización de alias

- **R1.** Los tokens de "Other Names" se separan por `,` y `/`.
- **R2.** Prefijo de dos letras más número: el número se rellena a 3 cifras (`QU14` → `QU014`, `LL01` → `LL001`, `UR44` → `UR044`). Los números de 4 cifras (`UR1031`, `UR1107`) se conservan. En khipu.db son etiquetas distintas: `UR1031` y `UR044` aparecen juntas en KH0033 y el OKR dice que son registros diferentes.
- **R3.** Sufijo entre paréntesis o pegado: `AS063(A)` → `AS063A`.
- **R4.** Calificadores (` - Part 1`, ` Detail 1`) se quitan del alias de salida. Para emparejar con KFG se usa la clave completa (`AS101 - Part 1` = `AS101_Part_1`).
- **R5.** Emparejamiento con KFG por clave alfanumérica en mayúsculas (`AS061_MA036` = `AS061/MA036`). Un nombre compuesto de KFG (`MM006_AN001`) se empareja con el KH que contiene todas sus partes (KH0672).
- **R6.** `INVESTIGATOR_NUM` de khipu.db se añade a los alias del KH, marcado como "solo en khipu.db" si el OKR no lo tiene.

### 1.3 Enlace KFG → KH (prioridad)

1. `khipu_id` del resumen KFG → `KHIPU_ID` de khipu.db → `OKR_NUM`: 558 xlsx.
2. Columna `okr` del xlsx (`KH####`): 39 xlsx (no solapan con el criterio 1 en 4 casos).
3. Nombre del xlsx en los alias del OKR: 52 xlsx.
4. Nombre compuesto (R5): 2 (KH0672, KH0673).

Algunos xlsx cumplen varios criterios; el método completo queda en `kfg_enlace` de cada fila.
Resultado: **los 651 xlsx reciben un KH, sin conflictos** (0 conflictos).

### 1.4 Conteos

| concepto | cifra |
|---|---:|
| KH en la lista OKR | 702 |
| KH con fila en khipu.db | 619 |
| KH fuera de khipu.db | 83 (44 con carpeta de datos, 39 sin carpeta) |
| xlsx KFG (`quipus.csv`) | 651 |
| xlsx KFG con KH | 651 (646 KH distintos) |
| KH con al menos un quipu KFG | 646 |
| KH sin ningún quipu KFG | 56 |
| KH en khipu.db **y** en KFG | 612 |
| KH en khipu.db, sin KFG | 7 (KH0146, KH0198, KH0208, KH0228, KH0268, KH0351, KH0419) |
| KH en KFG, sin khipu.db | 34 (AS001-AS009 = KH0002-KH0010; KH0600; KH0664-KH0694 salvo algunos) |
| KH sin khipu.db y sin KFG | 49 (sin nombre en ninguna de las dos bases) |

Comprobación: 612 + 7 = 619; 612 + 34 = 646; 646 + 56 = 702; 83 = 34 + 49.

Quipus KFG sin KH: **0**. KH con dos xlsx KFG: **5**, que explican que 651 xlsx den 646 KH:

| KH | xlsx KFG | nota |
|---|---|---|
| KH0033 | `KH0033`, `UR044` | UR044 es el registro incompleto que el OKR marca como duplicado de AS031 (66 cuerdas) |
| KH0197 | `KH0197`, `UR1180` | |
| KH0227 | `KH0227` (221 cuerdas), `AS207C` (14) | AS207A-C comparten inventario C14459 en el OKR |
| KH0267 | `KH0267` (22), `UR034` (188) | |
| KH0350 | `KH0350` (55), `UR114` (260) | |

### 1.5 Explicación de 650 / 651 / 685 / 702 / 709

- **702**: números KH asignados por el OKR (`okr-kh-numbers.csv`). Incluye los 83 sin fila en khipu.db.
- **619**: filas de `khipu_main` (OKR). Son los KH con registro estructurado en khipu.db.
- **651**: xlsx en `KFG_DB_Excel/` (y `quipus.csv`). Son los quipus que sí tenemos en el KFG local.
- **650**: filas de `khipu_summary.csv`. La única diferencia con los 651 xlsx es **UR044** (el registro duplicado y sin terminar de AS031). Verificado: los 650 `khipu_id` del resumen están en el volcado SQL, y el resumen no contiene UR044.
- **685**: filas de `khipu_main` en `KFG_DB.SQL`. Los 650 del resumen están dentro. Las otras 35 son: 16 con KH que tiene xlsx pero cuyo registro SQL no es el que emparejó el resumen (registros alternativos o duplicados del mismo número KH; no verificado uno a uno), 5 de khipu.db sin xlsx (KH0198, KH0228, KH0268, KH0351, KH0419), 13 sin khipu.db y sin xlsx (incluye duplicados como `AS067/MA29`) y UR044 (que tiene xlsx pero no está en el resumen). 16 + 5 + 13 + 1 = 35.
- **709**: no es reproducible con los datos de este repo. K-CAT (`data/external/khipu-computational-toolkit/data/processed/phase3_feature_matrix.csv`) tiene 709 identificadores: 682 `KH####`, 12 `KH####A-D` y 15 con otros prefijos (RA×10, HM×2, CM×1, KT×1, RS×1). Frente al KFG local, K-CAT contiene **38 KH que no están en nuestros 651** (todos sin KFG local, p. ej. KH0023, KH0631-KH0635, KH0653-KH0702) y **no contiene** KH0099 ni KH0140. Es decir: K-CAT usa una versión posterior del KFG que incluye los KH de las carpetas pendientes. El README de K-CAT dice que compila desde "KFG source XLS" (`data/kfg/KFG/KFG/`), carpeta que no está en este repo.
- Cifras de la documentación que **no** pude reproducir exactamente:
  - "650 quipus KFG declaran un número KH (647 distintos)": en `khipu_summary.csv` hay 596 filas con `okr_name` KH (593 distintos); en `quipus.csv`, 593 filas.
  - "647 de 650 quipus KFG tienen equivalente en el OKR": con las reglas de arriba hay 651 de 651 con KH y 646 KH distintos.
  - "593 de esos números están en khipu.db": el conjunto de 593 KH de `okr` no coincide con el de los 612 que sí están en khipu.db.

### 1.6 Alias duplicados y conflictos

- **Un alias en dos KH:** `AS101` en KH0114 (AS101 - Part 1) y KH0115 (AS101 - Part 2); `AS124` y `UR1124` en KH0138 y KH0139 (`UR1124 Detail 1`). En los cuatro casos el enlace KFG se resuelve por `khipu_id` y los nombres completos son distintos.
- **Un KH con dos UR:** KH0033 (`UR1031`, `UR044`), KH0118 (`UR1104`, `UR224`), KH0268 (`UR036`, `UR133`), KH0351 (`UR115`, `UR126`).
- **Un KH con dos AS:** KH0074 (`AS063A`, `AS063`), KH0077 (`AS065A`, `AS065`), KH0199 (`AS182A`, `AS182`). Coinciden con las notas del OKR sobre khipus divididos.
- **Inventario compartido (mismo museo, sin sufijo A/B):** 38 grupos, 122 KH. Ejemplos:
  - `VA63038`: KH0469 (UR232) y KH0470 (UR233). El OKR dice que son el mismo número de inventario.
  - `VA24370`: KH0120 (UR1106, A) y KH0121 (UR1107, B).
  - `VA42528`: KH0114/KH0115. `VA24371`: KH0138/KH0139. `C14459`: KH0225-KH0227.
  - Hay además grupos grandes, como `RT-16905` (KH0638-KH0652) o `IVc.366.03` (KH0682-KH0691).
- **Mismo número en museos distintos:** `80.1012 aka 2708` aparece en KH0676 (Brooklyn, JS001) y KH0700 (Stanford, SB001). Posible duplicado a revisar.
- **Corrección a la brief:** UR1107 (KH0121, `VA24370(B)`) y UR237 (KH0473, `VA66834`) **no** comparten inventario. Los pares reales son UR232/UR233 (`VA63038`) y UR1106/UR1107 (`VA24370`).
- **Duplicados marcados en el OKR:** KH0033 (UR044), KH0080 (AS067/MA029 y AS067/MA29), KH0140 ↔ KH0483, KH0198 (UR236).

### 1.7 Lo que no se resuelve

- Los 14 KH sin datos (sin khipu.db, sin KFG y sin carpeta) son solo nombres en el OKR. Los otros 35 de los 49 sin KFG ni khipu.db tienen carpeta y son los pendientes de la parte B.
- `puente.csv` no decide qué entrada es "la" canónica cuando hay duplicados. Eso sigue los comentarios del OKR, sin reinterpretarlos.

---

## 2. Parte B. Datos del OKR fuera de khipu.db

### 2.1 B1. `KH0002_0010/AS1-AS9.db`

- **Esquema:** igual que khipu.db (`khipu_main`, `cord`, `knot`, `knot_cluster`, `cord_cluster`, `primary_cord`, `ascher_cord_color`). Contiene 9 quipus (`KHIPU_ID` 1000662-1000670) con 681 cuerdas y 1.872 nudos.
- **Están ya en KFG** (AS001-AS009, `quipus.csv`) y **no** en khipu.db (ningún `KHIPU_ID` ni `INVESTIGATOR_NUM` de estos nueve aparece allí). Por eso **no hay nada que añadir a `cuerdas_extra.csv`** para ellos.
- **Comparación** (valor de cuerda = suma de `TOTAL_VALUE` de sus clusters, la misma regla que el KFG):

| quipu | cuerdas DB / KFG | con nudos DB / KFG | suma valores DB / KFG | multiconjunto igual |
|---|---|---|---|---|
| AS001 | 31 / 31 | 31 / 31 | 462 / 462 | sí |
| AS002 | 15 / 15 | 13 / 13 | 247 / 247 | sí |
| AS003 | 9 / 9 | 9 / 9 | 164 / 164 | sí |
| AS004 | 22 / 22 | 22 / 22 | 4637 / 4736 | no |
| AS005 | 59 / 59 | 50 / 50 | 193 / 179 | no |
| AS006 | 92 / 92 | 87 / 88 | 1468 / 1604 | no |
| AS007 | 171 / 171 | 156 / 156 | 2875 / 2512 | no |
| AS008 | 249 / 248 | 197 / 196 | 88084 / 70026 | no |
| AS009 | 33 / 33 | 14 / 14 | 476 / 467 | no |

- **Cuerdas:** coinciden en 8 de 9 quipus. En AS008, la DB tiene una cuerda extra: `CORD_LEVEL = -1`, `CORD_CLASSIFICATION = 'T'`, sin nudos ni longitud, colgada del cordón principal (`PENDANT_FROM` = 1000669). El KFG no la incluye. No la añadí a `cuerdas_extra.csv` porque no es un quipu nuevo y no tiene nombre en el KFG.
- **Valores:** las sumas coinciden solo en AS001-AS003. En AS008 la diferencia (18.058) viene en buena parte de una cuerda de la DB con valor 17.612 (clusters de 10.000 y 7.000); el KFG no tiene ninguna cuerda por encima de 12.138. La DB no tiene nombres de cuerda (`p#`), así que no se puede alinear cuerda a cuerda sin una tabla de correspondencias. Lo registro como discrepancia a revisar. No corregí el KFG.

### 2.2 B2. Los xlsx de KH0631-KH0702

**Formatos.**
- **Formato KFG** (hojas Khipu/PrimaryCord/Clusters/Cords, con `Value` y `Alt_Value`): `SH001.xlsx` (KH0631) y `R4303.xlsx` (KH0702). Lectura con la lógica de `construir_tabla.py`, copiada en `parte_b_xlsx.py` (el original no se toca).
- **Formato "recording sheet"** (hojas `primary_cord`, `pendant_cords`, `code_descriptions`): KH0633-KH0635 (3 xlsx) y KH0638-KH0651 (14 xlsx). Las cuerdas vienen una por fila, con subsidiarias como filas propias (`1s1`). Los nudos están como `4L(19.0,S,4)d` y se reescriben a notación KFG (`4L(19.0,S),4`). La columna `value` se compara con la suma.
- **Formato KDB** (hojas `Heading`, `Pendant Detail`): `JS01_Strauss_Harvard_Senior_Thesis.xlsx` (KH0676). No tiene columna de valor y la regla de la hoja ("long knots = their value in parentheses") es ambigua. **No convertido.**
- **Sin hoja de cuerdas:** `KHIPU ENLAZADO-MNAAHP.15.xlsx` (KH0652) tiene `wrapped threads`. **No convertido.**
- **Sin datos:** KH0632 (SH002) no tiene ningún archivo en su carpeta.

**Nuevos frente al KFG local.** Ninguno de los 19 quipus convertidos está en `quipus.csv`, en khipu.db ni en el resumen. Comprobado por inventario (`Museum Number`, OKR, nombres):
- KH0631 (SA004/SH001, St. Andrews), KH0702 (Museo Amano R4303; el resto de Amano en OKR son R2699, R2700 y R4248), KH0633-KH0635 (British Museum, Am1937,0213.84; el AS014 del BM es Am1907,0319.286), KH0638-KH0651 (MNAAHP, RT-16905).

| KH | archivo | cuerdas | valor = suma de nudos | discrepancias | sin comprobar |
|---|---|---:|---:|---:|---:|
| KH0631 | SH001.xlsx | 22 | 18 | 3 | 1 |
| KH0702 | R4303.xlsx | 147 | 147 | 0 | 0 |
| KH0633 | Am_1937_0213_84_khipu_1 | 67 | 67 | 0 | 0 |
| KH0634 | Am_1937_0213_84_khipu_2 | 42 | 40 | 2 | 0 |
| KH0635 | Am_1937_0213_84_khipu_3 | 166 | 163 | 2 | 1 |
| KH0638-KH0651 | KHIPU ENLAZADO-MNAAHP.01 a .14 | 332 | 308 | 14 | 10 |
| **Total** | **19 quipus** | **776** | **743** | **21** | **12** |

- **Validación.** `valor` = suma del último número de cada racimo de nudos (`3S(7.5,U),30;9L(9.0,U),9` → 39). Los 21 casos con discrepancia se conservan con el valor de la hoja y se marcan en `notas` con `VALIDACION: valor=… suma_nudos=…`. No se corrigieron. Los 12 sin comprobar son cuerdas cuyo racimo no tiene valor final (p. ej. `2L(25,Z)`).
- **Ejemplo de discrepancia en la fuente:** SH001 p1 tiene valor 404 con racimos que suman 428.
- **Enlace con K-CAT.** K-CAT incluye estos mismos KH (KH0631-KH0635, KH0653-KH0702) como quipus KFG. Conviene confirmar en el KFG en línea si ya existen versiones convertidas antes de usar `cuerdas_extra.csv` como fuente nueva.
- `cuerdas_extra.csv` usa como `kfg` el número KH (no hay nombre AS/UR). El origen de cada fila está en `notas`.
- Columnas `grupo` y `padre`: para el formato "recording" se toman de `Cord Clusters` y del nombre (`p1s1` → `p1`). Para el KFG se mantienen los valores del propio fichero.

### 2.3 B3. Archivos sin conversión (jpg, pdf, docx)

Lista completa en `inventario_manual.csv` (24 filas, 18 con `requiere_transcripcion_manual = sí`).

- **Docx (sí tienen texto, no requieren transcripción):**
  - `SH001 Description 2023.docx`: descripción de Sabine Hyland (2023), 22 colgantes sin subsidiarias, C14 de 1498 BP ±27, procedencia desconocida.
  - `Description RT 16905 MNAAHP.docx`: descripción del conjunto de 15 quipus enlazados (Chirinos, Ghezzi, Álvarez; sept. 2023), con diagrama y 2 tablas.
- **PDF (sin capa de texto, son escaneos de imágenes):** `PC.WBC.2016.072.pdf` (KH0674, UR297), `PC.WBC.2016.071.pdf` (KH0675, UR298), `Struass_Original_Notes.pdf` (KH0676). `pdftotext` no devuelve texto en ninguno.
- **Jpg (14):** 11 fichas `JC024_record.jpg` … `JC034_record.jpg` (KH0653-KH0663), 2 fotos de SH001 (fecha C14 y mitad superior) y el croquis de los 15 quipus enlazados. No se abrieron las imágenes; el contenido de las fichas es una suposición según el nombre.

**Requieren trabajo manual (lista exacta):**
1. KH0632: no hay archivos (SH002).
2. KH0652: `KHIPU ENLAZADO-MNAAHP.15.xlsx`, hojas `wrapped threads` (no es formato de cuerdas).
3. KH0676: `JS01_Strauss_Harvard_Senior_Thesis.xlsx` (141 filas de cuerdas sin valor; decidir regla de decodificación).
4. KH0676: `Struass_Original_Notes.pdf` (escaneo).
5. KH0674: `PC.WBC.2016.072.pdf` (escaneo).
6. KH0675: `PC.WBC.2016.071.pdf` (escaneo).
7. KH0653-KH0663: 11 fichas jpg `JC024_record.jpg` … `JC034_record.jpg` (una por quipu).
8. KH0638-KH0652: `Croquis KhipusEnlazadosEnglish.jpg` (enlaces entre los 15 quipus; no está en los xlsx).
9. Los 21 casos de discrepancia de valor de la tabla de 2.2 (revisión contra la ficha original).
10. Confirmar `80.1012 aka 2708` (KH0676 / KH0700) y el número `36.718` que aparece en el archivo JS01 (no coincide con el OKR).

---

## 3. Limitaciones

- La comparación de AS1-AS9 es por totales y multiconjuntos porque la DB no tiene nombres de cuerda. No es una reconciliación cuerda a cuerda.
- La regla de valor "suma de nudos" es la de `construir_tabla.py` y la de la documentación del KFG. Las 21 discrepancias pueden venir de la fuente (lo más probable) o de la regla de valor; no se ha decidido cuál.
- El enlace por nombre se hace solo con los nombres del OKR, khipu.db y el KFG. No se consultó ningún otro registro de museo.
