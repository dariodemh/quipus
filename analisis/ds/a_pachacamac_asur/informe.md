# Monografía del archivo de Pachacamac, series AS y UR

*Investigador del equipo de análisis. Datos: `analisis/datos/{cuerdas,quipus,grupos}.csv` (KFG). Scripts en esta carpeta (`01`–`07`), salidas en `salida/`. Sin commits.*

## 0. Pregunta

¿Qué es el archivo de quipus de Pachacamac conservado bajo los nombres de catálogo **AS** y **UR**? Se describe el conjunto, se buscan relaciones entre sus quipus (con modelo nulo explícito), se intenta reconstruir una eventual jerarquía detalle/resumen y se contrasta con la literatura del sitio.

**Conjunto operativo.** `procedencia` de `quipus.csv` contiene "Pachacamac" **y** el `kfg` empieza por `AS` o `UR` → **59 quipus** (16 AS y 43 UR; 4 680 cuerdas; 672 grupos). Quedan fuera, por diseño de la tarea, los 32 HP y KH0350 (serie hermana `a_pachacamac_hp`). Con los 32 HP, este es exactamente el "Pachacamac n = 91" que analizó Clindaniel (2019).

## 1. Método

1. Unidad de análisis = **quipu**. Las pruebas a nivel de cuerda usan permutación *dentro* de cada quipu.
2. Valor "real" de una cuerda: `valor` de KFG, salvo ausente (`NaN`) si `valor == 0` **y** no hay `nudos` (regla 6 del BRIEF). Sólo **1** cuerda del conjunto tiene valor 0 con nudos presentes.
3. **Nulo prescrito:** barajar los valores reales **dentro de cada quipu** (se conserva el multiséptico de valores, por tanto el total; se destruye el orden), 500 repeticiones, `seed(0)`. Es el nulo correcto para estadísticos dependientes del orden (secuencias compartidas, bloques). Se advierte cuándo un estadístico es invariante a este nulo y se usa entonces otro nulo.
4. **Corrección de comparaciones múltiples:** Holm–Bonferroni, dentro de familia y global (familia de 15 pruebas). Se reporta.
5. Se reportan los resultados negativos.

## 1b. Control previo: duplicados de objeto

Con `data/external/open-khipu-repository/data/okr-kh-numbers.csv` (`OKR Number` ↔ `Other Names`) se verificó que **ninguna** pareja de los 59 comparte número KH ni ficha con ≥2 de nuestros nombres → no hay dos nombres del mismo objeto, **salvo**:

- **AS101** viene partido en `AS101_Part_1` y `AS101_Part_2` (mismo objeto físico, dos filas). Se descarta ese par como hallazgo.

Y, crucialmente, el fichaje de OKR **declara** (campo `Comments`):
- **KH0140 (AS125)**: *"This khipus is a duplicate of KH0483."*
- **KH0483 (UR247)**: *"This khipu is a duplicate of KH0140."*

Es decir, **AS125 y UR247 son el mismo objeto (duplicado catalogado)**. Esto importa porque el análisis de secuencias (abajo) los señalaba como el hallazgo más fuerte del archivo. Se controla excluyéndolos.

## 2. Descripción del conjunto

**Tamaño.** Cuerdas por quipu: mediana 48, media 79, rango 3–338. Mayores: UR1175 (338), UR1131 (287), UR1121 (281), UR197 (236), UR1095 (212), UR212 (196), UR208 (190), AS075 (186). La mitad tiene ≤48 cuerdas y ~1/3 tiene <20: archivo de quipus **medianos y pequeños**, no de grandes quipus administrativos.

**Estructura.** Mayoritariamente **planos**: mediana de `max_nivel` = 1 (sólo colgantes + 1 nivel de subsidiarias); sólo 4 quipus llegan a nivel 3 (UR1175, UR1095, UR216, UR253). De las cuerdas madre con hijas, **512 tienen exactamente 1 hija** con valor, 46 tienen 2 y sólo 8 tienen ≥5: el árbol es casi siempre una **cadena lineal**, no un abanico. Grupos por quipu: mediana 7; máximo 80 (UR1121: 280 colgantes en 80 grupos ≈ 3,5 cuerdas/grupo).

**Colores.** Dominan **W (blanco; 1 116 cuerdas, 24 %)**, MB (387), B (383), AB (341), YB (206), LB (198); abundan combinaciones `W:AB`, `W:MB`, `NB:R`, `AB:MB`, `AB:GG` (hilos mezclados). Color dominante por quipu: **W en 26**, AB en 5, B en 4, LB en 3. El color está casi completo (30/4 680 nulos). Cordón principal `pc_color`: W en 14, B en 6, AB en 5, PK en 4.

**Valores.** 3 309 valores reales. Mediana 20, p75 63, p90 336, p99 5 983, máx 49 676. Distribución fuertemente asimétrica; valores más frecuentes 1 (243), 10 (178), 2 (171), 3 (163), 4 (151), 20 (150), 5 (123): **vocabulario numérico pequeño dominante** con cola de totales grandes.

**Presentes/ausentes.** 1 371 de 4 680 cuerdas (29 %) sin nudos = ausentes (igual que el 30 % del corpus). 4 quipus tienen >50 % de cuerdas sin nudos (UR1121, UR216 y otros).

**Torsión (hilado de la cuerda) y unión al cordón principal.** Torsión **S en 4 068** cuerdas, Z sólo 40, U 569 → hilado mayoritariamente **S**. Unión: **R** (recto) 1 391, **V** (verso) 808 (≈1,7:1); 40 quipus son *puramente R* y 36 *puramente V* (es decir, la dirección de fijación está fuertemente estandarizada dentro de cada quipu).

**Dirección del nudo (dentro de los racimos) — no confundir con la torsión.** Sólo se registran direcciones **S y Z**: **Z = 3 052, S = 1 623, U = 852** (ratio Z/S ≈ 1,88). 15 quipus marcan la dirección como U en la mayoría de cuerdas: **limitación de datos**, no hallazgo.

**Cuerdas superiores y sumas.** Sólo **2 cuerdas superiores** (unión T), ambas en **UR201**, y sus valores (6 y 3) **no** son los totales de su grupo (6 279 y 5 790): no funcionan como resumen. Sumas internas **genuinas** (madre = suma de ≥2 hijas): sólo **2** en todo el archivo (UR1151 p9 = 5; UR254 p7 = 30). Otras 28 "sumas" son coincidencias triviales de 1 sola hija. Sumas de grupo genuinas (1.ª cuerda = suma del resto): sólo **3** (AS172 g7 = 10+10; UR196 g1 = 1+4+4+3 = 12; UR230 g5 = 7+6 = 13). Ningún quipu tiene una cuerda = total general salvo AS112 (total 10, trivial).

⇒ **El archivo es aritméticamente plano: casi no hay agregación jerárquica.** (Tabla completa por quipu: `salida/tabla_quipus.csv`, 59 filas.)

## 3. Relaciones ENTRE los quipus (con control nulo)

Se buscaron cuatro tipos de relación. Todas las pruebas de secuencia usan el nulo prescrito (barajar valores/colores dentro de cada quipu, 500×, `seed(0)`).

**(a) Secuencias de valores compartidas.** Nº de "k-mers" de valores consecutivos presentes en ≥2 quipus.

| k | obs (todos) | nulo | p | obs sin AS125/UR247 | nulo | p |
|---|---|---|---|---|---|---|
| 3 | 92 tipos / 81 pares | 50,3 / 47,6 | 0,002 | 82 / 80 | 50,6 / 47,8 | 0,002 |
| 4 | 19 / 11 | 6,7 / 5,9 | 0,002 | 10 / 10 | 6,6 / 5,8 | 0,136 |
| 5 | 8 / 1 | 0,9 / 0,8 | 0,002 | **0 / 0** | 0,9 / 0,8 | 1,000 |

**El hallazgo aparente lo produce el duplicado.** AS125 y UR247 comparten 12 colgantes idénticos y **consecutivos**: 1517, 2373, 6291, 3495, 4213, 6323, 4122, 2220, 4377, 1292, 1162, 2393, … (luego 3130 vs 31111, probable error de transcripción, y de nuevo 3332, 2122). Es **el mismo objeto** (duplicado declarado en OKR, §1b), no una relación entre quipus distintos. Al excluirlo, **toda** la señal de k≥4 desaparece (k=5 → 0; k=4 → p = 0,136). Sólo queda un exceso débil de k=3 (p = 0,002), pero los k=3 compartidos son **motivos de números pequeños redondos** (4,4,4; 20,20,20; 1,1,1; 50,20,10…), esperables con el vocabulario de §2. Conclusión: **la similitud de secuencias entre quipus distintos es la que predice el azar, salvo ruido de vocabulario pequeño.**

**(b) Totales de un quipu que aparecen en otro.** 
- Como **bloque contiguo** (≥2 cuerdas) de B: obs **250** pares ordenados, nulo **246,1 ± 10,5**, **p = 0,373** → azar. 
- Como **valor suelto** de B: obs 54. El nulo prescrito es **invariante** (el conjunto de valores de B no cambia al barajar dentro de B), así que se usó un nulo **cross-quipu** (reasignar valores entre quipus): esperado 68,1 ± 2,9, **p = 1,000** → los totales reaparecen **menos** de lo esperado por azar. 
- Como **suma de grupo** de B: 13 pares, todos de valores triviales (10, 36, 149…).

**(c) Estructuras de grupos idénticas.** Ningún par de quipus comparte la **secuencia exacta** de tamaños de grupo: **0** coincidencias (nulo 0), p = 1,000.

**(d) Patrones de color.** Ningún par comparte la **secuencia completa** de colores de colgantes (0). A nivel de fragmentos, los 4-mers de color se comparten entre más pares de lo esperado (obs 381 pares vs nulo 243, p = 0,002, también sin duplicado), **pero** está dominado por **tramos monocromos** ((W,W,W,W) en 28 quipus) y transiciones a blanco (LB,W,W,W; AB,W,W,W…): motivos genéricos por el pequeño repertorio de colores, no mensajes compartidos. El número de 4-mers **distintos** es *menor* que el nulo (p = 1,000): los colores forman tramos regulares (estructura intra-quipu), no vinculación entre quipus.

**Balance (§3):** no hay evidencia de vinculación numérica entre los quipus AS/UR distintos. El único caso llamativo es un duplicado de museo.

## 4. Jerarquía del archivo (detalle vs resumen)

Resultado **negativo**:
- **Entre quipus:** no hay totales que reaparezcan como valores, bloques o sumas de grupo de otro (§3b). No hay un quipu "de resumen" que agregue a otros.
- **Dentro de cada quipu:** sólo 2 sumas madre = Σhijas genuinas, 3 sumas de grupo, 2 cuerdas superiores (de valor minúsculo), ningún total general. El archivo **no** contiene la jerarquía clásica de agregación decimal piramidal.

El conjunto se comporta como un **ensamble de registros independientes y planos** (listas de cuentas por grupos de colgantes), no como un sistema de detalle→resumen. Nivel de evidencia: **apoyado con datos**.

## 5. Contraste con la literatura de Pachacamac

**Clindaniel (2019), cap. 3 — dirección de nudo.** Analiza Pachacamac **n = 91** (exactamente nuestras 16 AS + 43 UR + 32 HP) y halla que **Z domina sobre S** (patrón global, replicado en Pachacamac). Nuestros datos lo **replican**: Z = 3 052 vs S = 1 623 (Z/S = 1,88); a nivel de quipu, **30 quipus con Z>S vs 13 con S>Z** (sign test p = 0,0069; Holm global p = 0,055, borderline). → **apoyado con datos.**

**Sáez-Rodríguez (2013) — el khipu VA 42527.** Su objeto estrella (= KH0118) es **UR1104, que está en nuestro conjunto**. Lo describimos: **21 cuerdas colgantes, sin subsidiarias, todas blancas, todas unión V y torsión S, pc `W-MB-MB`, valores 1 385–37 076** (coincide con la ficha: "21 cuerdas, sin subsidiarias, colgantes blancas"). Su lectura calendárica (ciclos lunares/agrícolas, partida doble) es **n = 1, sin controles**; el propio `docs/estado_del_arte.md` la usa como **contraejemplo metodológico** (§ líneas 301, 245). En nuestro conjunto UR1104 es **1 de 59**, atípico (todo V, sin sumas): sirve para una anécdota, no para inferir el significado del archivo.

**Urton (2017), *Inka History in Knots*.** Dedica un capítulo a Pachacamac (valle de Lurín) dentro de una obra que trata los quipus como registros de **censo y tributo**. La ficha no da cifras comparables. Nuestro resultado (archivo plano, sin agregación ni vínculos) **no confirma** un uso administrativo agregado en esta muestra: si son registros de cuentas, no vienen articulados como libros de tributo jerárquicos.

**Composición museística (contexto crítico).** 51 de los 59 quipus están en **Berlín** (`Museum für Völkerkunde` = `Ethnologisches Museum`, dos nombres del mismo museo); Munich 2, Göteborg 2, Leipzig 2, Smithsonian 1, París 1. Es decir, el "archivo" es **una colección de museo colonial**, no un contexto arqueológico excavado: los números AS (Ascher) y UR (Urton) son **dos sistemas de numeración sobre las mismas vitrinas**, razón por la que existe el duplicado AS125=UR247. Cualquier inferencia de "archivo administrativo" del sitio debe ser escéptica.

**Propuesta (qué se registraba aquí).** Con la evidencia disponible, lo más defendible es que los AS/UR de Pachacamac son **un conjunto de quipus de cuentas/listas pequeñas e independientes** (nº de cuerdas mediano, grupos de pocas cuerdas, vocabulario numérico pequeño, dirección de nudo Z-dominante), **sin** agregación decimal y **sin** relación numérica entre piezas. La hipótesis de "archivo jerárquico de tributo/censo" **no** se sostiene para esta muestra. Nivel: **propuesto** para "registros de cuentas"; **especulativo** para cualquier contenido temático concreto.

## 6. Resultados negativos (explicitados)

1. **Sin secuencias de valores compartidas reales** entre quipus distintos (k≥4, p ≥ 0,136 sin el duplicado).
2. **Sin reapartición de totales** entre quipus (bloques: p = 0,373; valores: p = 1,000, por debajo del azar).
3. **Sin estructuras de grupo idénticas** (0; p = 1,000).
4. **Sin secuencias de color completas idénticas** (0); el exceso de fragmentos es monótono y genérico.
5. **Sin jerarquía detalle/resumen** ni dentro ni entre quipus (sólo 2 sumas madre genuinas en 4 680 cuerdas).
6. La "dirección de nudo desconocida" (U) cubre 852/5 527 nudos con dirección: limita cualquier análisis direccional.

## 7. Nivel de evidencia por conclusión

| Conclusión | Nivel |
|---|---|
| AS125 y UR247 son el mismo objeto (duplicado de museo) | **bien apoyado** (ficha OKR + 12 valores idénticos) |
| Archivo plano, sin agregación numérica interna | **apoyado con datos** |
| Sin vinculación numérica entre quipus (nulo 500, Holm) | **apoyado con datos** |
| Z domina la dirección de nudo (replica a Clindaniel) | **apoyado con datos** (p = 0,007; borderline tras Holm global) |
| Conjunto = registros de cuentas pequeños e independientes | **propuesto** |
| Colección de museo colonial, no archivo excavado del sitio | **apoyado con datos** (composición museística) |
| Cualquier contenido temático (calendario, tributo…) | **especulativo** |

## 8. Para el coordinador

1. **El hallazgo más fuerte era una trampa:** AS125 y UR247 comparten 12 valores consecutivos idénticos (1517, 2373, 6291…), pero el propio catálogo OKR los declara **duplicados** (KH0140 = KH0483). Es el mismo objeto bajo dos numeraciones (Ascher `AS` y Urton `UR`) del mismo museo (Berlín). **No es un hallazgo.**
2. **Excluido el duplicado, no hay relación numérica entre los quipus AS/UR:** secuencias compartidas k≥4 = azar (p = 0,136–1,0), totales cruzados = azar (bloques p = 0,373; valores p = 1,0, *por debajo* del azar), estructuras de grupo y secuencias de color idénticas = 0/59.
3. **El archivo es aritméticamente plano:** en 4 680 cuerdas sólo 2 sumas madre = Σhijas genuinas, 3 sumas de grupo, 2 cuerdas superiores (de valor minúsculo, no resumen) y ningún total general. **No hay jerarquía detalle→resumen**, ni intra ni inter-quipu.
4. **Replicamos a Clindaniel (2019):** la dirección de nudo está dominada por **Z** (3 052 Z vs 1 623 S) y, a nivel de quipu, 30 con Z>S vs 13 con S>Z (sign test p = 0,007). Evidencia **apoyada con datos**; tras Holm global queda borderline (0,055).
5. **El "Pachacamac n = 91" de Clindaniel** = nuestros 16 AS + 43 UR + 32 HP. Nuestra muestra es 2/3 de ese corpus: bueno para replicar, malo para conclusiones temáticas.
6. **El famoso khipu calendárico de Sáez-Rodríguez (VA 42527) = UR1104, está aquí:** 21 colgantes, sin subsidiarias, todos blancos, unión V, valores 1 385–37 076. Es 1 de 59 y atípico; su lectura calendárica es n = 1 (el estado del arte la llama contraejemplo metodológico). No extrapolar.
7. **Ojo con la composición colonial:** 51/59 quipus están en el mismo museo de Berlín (dos nombres). "Archivo de Pachacamac" es en realidad una **colección de museo**, y los prefijos AS/UR son dos numeraciones de las mismas vitrinas → esperar más duplicados. Recomiendo cruzar sistemáticamente los 59 con `okr-kh-numbers.csv` (colección `VA…`).
8. **Recomendación siguiente ronda:** (a) mapear TODOS los pares AS/UR por número de colección del museo para detectar más duplicados; (b) probar si el vocabulario pequeño (1,2,3,4,5,10,20) funciona como **códigos/etiquetas** más que como cantidades (consistente con Sáez-Rodríguez, pero con controles); (c) comparar AS/UR con los HP del mismo sitio para ver si el patrón plano se debe al origen de museo o al sitio.

---
### Anexos
- Scripts: `01_describir.py`, `02_duplicados.py`, `03_relaciones.py`, `04_diagnostico.py`, `05_sumas_jerarquia.py`, `06_jerarquia_interna.py`, `07_resumen_estadistico.py`.
- Salidas: `salida/tabla_quipus.csv`, `salida/lccs_pares.csv`, `salida/totales_bloques.csv`, `salida/total_como_valor.csv`, `salida/total_como_grupo.csv`, `salida/jerarquia_interna.csv`, `salida/pruebas_holm.csv`, `salida/kmer_val_k4.csv`.
- Reproducción: `python 01_describir.py` … `python 07_resumen_estadistico.py` (semilla 0 fija).
