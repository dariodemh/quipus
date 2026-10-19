# Familia aditiva/tally con torsión Z: fuentes, réplica en OKR, perfil y lectura aditiva

**Carpeta:** `analisis/27_familia_z/` · **Semilla:** 20261018 · **Fecha:** 2026-10-18
**Datos:** OKR en solo lectura (`khipu.db`, 619 quipus; 612 se unen a cuerdas). Todo sale de OKR para tener `knot`, `FIBER` y `TWIST`. No se creó ningún `khipu.db`.
**Scripts (en orden):** `01_okr_tabla.py`, `02_replica.py`, `03_perfil.py`, `04_aditiva.py`, `05_sensibilidad.py`, `06_torsion_region.py`. CSV: `okr_cuerdas.csv`, `okr_quipus.csv`, `replica_resultados.csv`, `replica_base.csv`, `sensibilidad.csv`, `perfil_resultados.csv`, `perfil_hist_valores.csv`, `perfil_base.csv`, `aditiva_resumen.csv`, `aditiva_igualdad.csv`, `torsion_por_fibra_cuerda.csv`, `torsion_region_*.csv`. Salida de texto: `replica_salida.txt`.

---

## 1. Fuentes sobre hilado y torsión por región

**Convención.** `cord.TWIST` de OKR es la torsión final del cordel. S = «left lay», Z = «right lay» (Day 1967, `analisis/fuentes_txt/Day1967_QuipusWitchesKnots.txt`, línea 147).

**Lo que sí está documentado**

| Afirmación | Fuente | Nivel |
|---|---|---|
| La mayoría de los cordeles de quipus son de algodón con torsión final S; «a few have Z-twist» | Day 1967, línea 147 | Documentado (descriptivo) |
| Entre quipus incaicos y coloniales tempranos: cordeles de **camélido 59 % S / 41 % Z**; de **algodón 97 % S / 3 % Z** (Urton y Brezine 2011, citado por Hyland) | Hyland 2017, *Writing with twisted cords*, Curr. Anthropol. 58(3), `fuentes_txt/Hyland2017_WritingTwistedCords.txt`, línea 47 | Documentado (cifra de segunda mano). Apoya Z ~ camélido; no apoya «camélido = siempre Z» |
| Quipus de pastores de Collata (sierra; alpaca y vicuña): S 58 % / Z 42 % | Hyland 2017, línea 47 | Documentado. La sierra con camélido es **mayoritariamente S**, no Z |
| La dirección del retorcido es un rasgo semiótico (oposición binaria; S «no marcado», Z «marcado») | Hyland 2014, *Ply, markedness and redundancy*, Am. Anthropol. 116(3):643–648 ([repositorio St Andrews](https://research-repository.st-andrews.ac.uk/handle/10023/6639); solo se leyó el resumen); Urton 2003 citado en `InterpretacionLinguisticaQuipus.txt`, línea 9731 | Documentado (Cutusuma, Bolivia; Collata) |
| En los quipus patrimoniales de Tupicocha (sierra de Lima) el del segmento menor es casi todo Z y el del mayor casi todo S. Los comuneros dicen que es idiosincrasia personal, pero parece convención | Salomon, en *Narrative Threads* 2002, `fuentes_txt/NarrativeThreads2002.txt`, líneas 3475–3482 | Documentado (un caso) |
| Quipu B/8705 (Urton): 151 de 153 cuerdas «S-spun, Z-plied» | `NarrativeThreads2002.txt`, línea 2155 (nota 14) | Documentado: la torsión final Z puede ser el estándar de un quipu entero |
| Textiles de Huaca Prieta: algodón S-hilado / Z-torcido; Z-hilado/S-torcido como patrón dominante de textiles incaicos | Solo resumen de WebSearch; no se leyó la fuente primaria (no se pudo recuperar a Splitstoser, Conklin, Desrosiers, Rodman ni Frame) | **No verificado** |

**Lo que no está documentado.** Ninguna fuente leída dice que la torsión final Z sea propia de la **sierra** ni que S sea propia de la **costa**. Tampoco que el camélido se hile S y se tuerza Z como regla regional. Lo que hay es una asociación entre fibra y torsión final (Z ~ camélido, S ~ algodón) y el uso de la dirección como signo. La hipótesis «otra tradición de hilado serrana» queda **sin apoyo directo de fuentes**; es una conjetura compatible.

**Datos OKR sobre la hipótesis (`06_torsion_region.py`).**

- Cuerdas: P(Z) = **38,2 %** en camélido (n = 1 297) y **9,0 %** en algodón (27 778); 3,2 % en lana de oveja; 0 % en pelo y vegetal. La asociación fibra–torsión final se replica (Urton y Brezine: 41 % frente a 3 %).
- Las cuerdas de algodón con Z casi no existen en quipus con procedencia costera registrada: media por quipu 0,2 % (Norte, 31 quipus), 0,7 % (Centro), 0 % (Sur), 2,5 % (Sur-Centro). Se concentran en quipus **sin procedencia registrada**: 25 % (152 quipus). `regions_dc` de OKR no tiene región «sierra» (solo Norte, Norte-Centro, Centro, Sur-Centro, Sur), así que **la hipótesis serrana no se puede contrastar con OKR**. Lo único que muestra es que Z es raro donde se sabe de dónde vienen los quipus.
- Solo 2 quipus tienen ambas fibras con ambas torsiones, así que la comparación intra-quipu camélido–algodón no informa.

---

## 2. Réplica en OKR (`02_replica.py`, `05_sensibilidad.py`)

**Corrección de la premisa.** OKR (619 quipus) no tiene más quipus que KFG (651); tiene menos. Igual permite reconstruir el criterio con la tabla `knot`, que es lo pedido.

**Criterio por cuerda** (tabla `knot`; tipos L, E, SP, LL, BL, EE; valor = `knot_value_type`; vueltas = `NUM_TURNS`):

- **A (multi):** ≥ 2 nudos de unidades con valor < 10, o algún L con ≥ 10 vueltas reales.
- **B (valor):** suma de valores de unidades > 9, o algún L con ≥ 10 vueltas reales.

Tally = quipu con ≥ 50 % de cuerdas no decimales. Universo = 263 quipus con ≥ 30 cuerdas con nudos y ≥ 10 con torsión S/Z. Z = más de la mitad de las cuerdas con torsión conocida en Z.

El criterio A reproduce la lista del coordinador: **11 quipus** (UR050, 051, 052, 054, 055, UR039, UR110, UR144, LL01/UR176 = KH0001, UR193, UR203). Quedan fuera por poco UR112 (49 %) y UR1095 (46 %), y por más UR1087 y UR177 (36–37 %). El criterio B es más estricto: solo 5 (UR050, 052, 054, 055, UR193). El criterio exacto del coordinador no está en un script, así que la lista de 10 no se pudo reconstruir al pie de la letra.

**Resultados (criterio A).** Detalle en `replica_resultados.csv`.

| Prueba | Resultado |
|---|---|
| Z en tally frente a decimales | 7/11 frente a 16/252; Fisher OR 25,8, p = 4,1e-6 |
| Controlando fibra (CMH, 3 estratos) | OR_MH 24,1 (IC 3,6–159,8), p = 2e-4; permutación intra-estrato p = 0,0006 |
| Controlando región de procedencia (4 estratos usables) | OR_MH 11,7 (3,4–40,2), p = 5e-6; perm. p = 0,0008 |
| Fibra × región (5 estratos) | OR_MH 12,9 (2,3–71,6), p = 0,007; perm. p = 0,005 |
| Solo algodón | Z en 2/3 tally frente a 13/158 decimales; OR 22,3, p = 0,023 |
| Solo camélido | Z en 4/5 tally frente a 1/5 decimales; OR 16, p = 0,21 (n pequeño) |
| Logit tally ~ Z + fracción camélido (n = 183) | Z 2,22 (p = 0,006); camélido 2,98 (p = 0,001) |
| Correlación continua `frac_nd_multi` con `frac_Z` | Spearman 0,15, p = 0,014 (n = 263): débil |

Con el criterio B, más estricto, la señal baja pero se mantiene en Fisher (Z en 3/5 frente a 20/258; OR 17,9, p = 0,005). Con controles queda en p_perm 0,03–0,20, con solo 5 quipus: no concluyente.

**Sensibilidad (`sensibilidad.csv`).** El resultado se mantiene con umbrales de 30–70 % (OR 14–26; p ≤ 0,0013).

**Tres cautelas que cambian la lectura**

1. **No son 11 observaciones independientes.** UR050–055 son una serie. De ellos solo UR050 y UR054 son Z; UR051, 052 y 055 son S. Si la serie se colapsa en una unidad (que cuenta S), queda 5/7 Z en tally frente a 16/252; OR 36,9, p = 4e-5. Sin la serie: 5/6, OR 73,8, p = 1e-5. La señal sobrevive, pero con 6–7 unidades.
2. **La asociación es entre quipus, no entre cuerdas.** Dentro de quipus con cuerdas S y Z (6 quipus con el criterio B, 12 con A), una cuerda Z no tiene más probabilidad de ser no decimal que una S (CMH OR 1,02 y 1,07; p = 0,99 y 0,86). Z es una convención de **todo el quipu** que acompaña al género, no un rasgo de las cuentas largas. Es coherente con Z como signo de taller o de tradición.
3. **La familia no es toda Z.** De los 11 miembros, 4 son mayoritariamente S (UR051 29 % Z, UR052 22 %, UR055 0 %, UR203 0 %). Fibras: UR050, 054, 110, 144 son camélido; UR039, UR193, UR203 son algodón; UR055 es pelo (código `H`, pelo humano); UR051 y UR052 son mixtos; KH0001 no tiene dato de fibra. De los 7 miembros Z, 4 son camélido, 2 algodón (UR039, UR193) y 1 sin dato.

**Procedencia.** En el perfil de 12 quipus (§3), 7 no tienen procedencia en OKR (58 % frente al 22 % de los decimales; Fisher p = 0,008, BH 0,017). Por eso el control por región usa solo 4 estratos y no puede descartar que Z sea una marca de procedencia (p. ej. serrana) no registrada. Los miembros con procedencia: Huari (UR039), Valle de Pisco (UR144), Chuquitanta (KH0001), Pachacamac (UR193); UR203 figura como «unknown».

---

## 3. Perfil de la familia (`03_perfil.py`)

**Diseño.** Familia = criterio A con ≥ 30 cuerdas con nudos: 12 quipus (los 11 anteriores más AS014 del British Museum, sin dato de torsión). Control = los 297 quipus decimales restantes de ≥ 30 cuerdas. Además, 500 controles de 12 quipus pareados por tamaño (vecino más cercano entre 5 en log de cuerdas, sin reemplazo). Pruebas: Mann-Whitney (continuos) y Fisher (binarios y categorías). BH sobre las 33 comparaciones, por separado para «todos» y «pareado» (mediana de p sobre los 500 controles). Tabla completa en `perfil_resultados.csv`.

**Rasgos definicionales (no cuentan como hallazgo):** `u_x_cuerda`, `sumu_med`, `sh_L`, `sh_S`, `sh_E`, `vacias`, porque se deducen de la definición de tally.

**Rasgos que sobreviven a BH ≤ 0,05 con control pareado (no definicionales)**

| Rasgo | Familia (mediana) | Decimales | p pareado (BH) |
|---|---|---|---|
| Largo mediano de cuerda (cm) | **48,8** | 32,5 | 0,005 |
| Fracción de cuerdas multicolor | **1 %** | 21 % | 0,04 |
| Nudos largos de 2–3 vueltas (fracción de las cuentas L) | **8 %** | 40 % | 0,005 |
| Nudos largos de 4–6 vueltas | **64 %** | 38 % | 0,005 |
| Nudos largos de ≥ 10 vueltas reales | **1,3 %** | 0 % | 0,02 |
| Fracción de cuerdas Z | 100 % (mediana de 11) | 0 % | 0,005 |

**Con diferencia frente a todos los decimales pero no robustos al pareado (BH pareado > 0,05):** pocas terminaciones con nudo (K: 11 % frente a 75 %; BH pareado 0,08, BH «todos» 0,014), un color dominante (77 % de las cuerdas frente a 41 %; BH 0,07), menos colores distintos (3 frente a 6; BH 0,09), grupos más grandes (16,5 frente a 6,1 cuerdas; solo 5 quipus con grupos; BH 0,09), menos subsidiarias (42 % de quipus con subsidiarias frente a 82 %; BH 0,13), sin procedencia (58 % frente a 22 %; BH 0,13). **Sin diferencia:** número de cuerdas (mediana 106 frente a 92), largo del cordón principal (75 frente a 64 cm; p ≈ 0,6), estructura del cordón principal (50 % frente a 58 % `P`; p = 0,77), canutos (BH pareado 0,08).

**Distribución de valores por cuenta** (nudos L en unidades; `perfil_hist_valores.csv`):

| Valor | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | ≥ 10 vueltas |
|---|---|---|---|---|---|---|---|---|---|
| Familia | 2,4 % | 6,6 % | 17,2 % | **25,3 %** | 21,2 % | 16,9 % | 7,3 % | 3,0 % | 3,1 % |
| Decimales | **25,1 %** | 16,9 % | 14,8 % | 12,8 % | 10,0 % | 8,0 % | 7,1 % | 5,3 % | 0,2 % |

Los decimales tienen muchos valores bajos; la familia centra sus cuentas en 4–7 y casi no usa 2–3.

**Museo.** Solo la colección Soldi (UR050, UR054) está enriquecida frente a los decimales (2/12 frente a 0/297; p = 0,0014, BH 0,0037), pero son dos quipus de una misma serie. Los demás miembros se reparten entre Banco Central, Museo del Oro, Berlín (UR193, UR203), British Museum, Univ. San Martín de Porres, Ica y AMNH. No hay un museo común.

**Síntesis.** La familia se caracteriza por cuerdas largas, casi siempre de un solo color, con 3 a 5 cuentas de nudo largo de 4–7 vueltas por cuerda, y torsión Z en la mayoría de los quipus. El tamaño, el cordón principal y los canutos no la distinguen. Largo, color y valores son robustos al pareado por tamaño.

---

## 4. Lectura aditiva (`04_aditiva.py`; descriptivo)

Cuentas = nudos L por cuerda, ordenados por posición. UR050: 164 cuerdas y 501 cuentas (146 cuerdas con 3). UR054: 114 cuerdas y 312 cuentas. UR055: 175 cuerdas y 698 cuentas (3–5 por cuerda).

| Quipu | Media de cuenta | Índice de dispersión (var/media) | CV de la suma por cuerda | Valores |
|---|---|---|---|---|
| UR050 | 5,5 | **0,14** | 0,14 | 3–8; 5 y 6 = 79 % |
| UR054 | 5,6 | **0,23** | 0,22 | 3–9; 5 y 6 = 63 % |
| UR055 | 6,7 | **0,31** | 0,27 | 3–12; 6, 7 y 8 = 72 % |
| UR052 (referencia) | 5,6 | 0,38 | 0,37 | 3–12 |

- **Subdispersión extrema.** Un conteo de Poisson daría un índice cercano a 1; aquí es 0,14–0,38. En el quipu de ovejas de Mackey (`NarrativeThreads2002.txt`, hacia las líneas 3870–3885) las categorías van de 30 a 440 animales (crías machos 208, castrados 214, merinos 118, reproductores 30, hembras sin cría 440). Aquí cada cuenta es un solo nudo de 3–9 vueltas con muy poca variación.
- **Las cuentas dentro de una cuerda se parecen entre sí.** En UR050 (3 cuentas), 21,9 % de las cuerdas tienen las tres iguales frente a 12,4 % esperado por permutación (p = 0,001); cuentas adyacentes iguales 44 % frente a 33 % (p = 0,0005); correlación media entre cuentas 0,27. En UR054 el efecto es más débil (3 cuentas: 15 % frente a 8,5 %; p = 0,04; con 2 cuentas, rho 0,73). En UR055 no hay repetición exacta (en cuerdas de 4 y 5 cuentas, 0 % iguales), aunque con 3 cuentas rho = 0,50.
- **Sin categorías distintas por posición.** Las medias por posición son casi iguales (UR050: 5,4 / 5,5 / 5,8; UR054: 5,3 / 5,5 / 5,3). Si las tres cuentas fueran categorías de un rebaño (machos, hembras, crías) se esperarían niveles distintos por posición. No ocurre en UR050 ni en UR054.
- **Orden de cuerdas.** Sin autocorrelación entre cuerdas vecinas en UR050, UR054 y UR055 (p perm 0,08–0,18); UR052 sí (rho 0,47). En UR050 las cuerdas más largas suman menos (rho −0,31, p = 4e-5).
- **Lectura.** Los datos se parecen más a **la repetición de un valor casi fijo** que a conteos de rebaño por categoría. Es solo descriptivo: la distribución estrecha en 4–7 vueltas también puede deberse a cuántas vueltas se hacen de forma natural en un nudo largo. No se probó ninguna lectura numérica.

---

## 5. Para el coordinador

- **Fuentes (T1):** ninguna fuente leída dice «Z = sierra» o «S = costa». Hay cifras de Urton y Brezine 2011 citadas por Hyland 2017 (línea 47): camélido 41 % Z, algodón 3 % Z. Collata (alpaca, sierra) es 58 % S / 42 % Z. Splitstoser, Conklin, Desrosiers, Rodman y Frame no se pudieron leer. «Tradición serrana» queda **sin apoyo de fuentes** (propuesta). Sí está documentado que la dirección del retorcido es un signo (Hyland 2014; Tupicocha en Salomon, `NarrativeThreads2002.txt` 3475–3482).
- **OKR confirma Z ~ camélido en cuerdas (T1):** P(Z) = 38 % en camélido (n = 1 297) frente a 9 % en algodón (27 778). En algodón con procedencia costera registrada Z es ≤ 2,5 %; el Z de algodón está en quipus sin procedencia (25 %). OKR no tiene región serrana, así que no contrasta la hipótesis regional. Nivel: apoyado para fibra–torsión; sin datos para región.
- **Réplica (T2):** criterio A de OKR (tabla `knot`): 11 quipus tally en 263; Z en 7/11 frente a 16/252 decimales; OR 25,8, p = 4e-6. Se mantiene controlando fibra (OR_MH 24, p_perm 0,0006), región (OR_MH 12, p_perm 0,0008) y ambas (OR_MH 13, p_perm 0,005), y con umbrales de 30–70 %. Nivel: **apoyado**. Con el criterio B (suma > 9) solo hay 5 quipus y la señal es más débil (OR 18, p = 0,005; con controles p_perm 0,03–0,20).
- **Tres límites (T2):** (a) UR050–055 son una serie, no 6 observaciones; colapsada queda 5/7 Z, OR 37, p = 4e-5. (b) La familia no es toda Z: UR051, 052, 055 y UR203 son S. (c) Dentro de un mismo quipu, las cuerdas Z no son más no decimales que las S (OR 1,0–1,1): Z es convención de quipu o de taller, no rasgo de las cuentas. 7 de 12 miembros no tienen procedencia en OKR, así que no se descarta que Z sea una marca de procedencia no registrada.
- **Perfil (T3):** frente a decimales pareados por tamaño (BH ≤ 0,05): cuerdas más largas (mediana 48,8 frente a 32,5 cm), casi sin multicolor (1 % frente a 21 %), cuentas de 4–6 vueltas (64 % frente a 38 %) y casi sin 2–3 vueltas (8 % frente a 40 %). No robustos al pareado: pocas terminaciones con nudo, menos subsidiarias, color dominante, procedencia vacía. Sin diferencia: tamaño, cordón principal. Nivel: apoyado, n = 12; los rasgos de nudos son parcialmente definicionales. Colección Soldi enriquecida (UR050, UR054), pero es una serie.
- **Lectura aditiva (T4):** las cuentas de UR050, UR054 y UR055 están muy poco dispersas (var/media 0,14, 0,23 y 0,31 frente a ≈ 1 de un conteo Poisson) y en UR050 se repiten dentro de la cuerda (21,9 % con tres iguales frente a 12,4 % del nulo; p = 0,001). Las medias por posición son iguales. **No se parece a conteos de rebaño por categoría** (Mackey: 30 a 440 por categoría); se parece a un valor casi fijo repetido. Nivel: descriptivo, sin lectura numérica.
- **Pendiente:** obtener en texto a Splitstoser, Conklin, Frame y Urton y Brezine 2011, y una fuente que ligue procedencia serrana con torsión final, antes de usar «tradición serrana». Reformulación sugerida: «género aditivo con torsión final Z de quipu entero, asociado a camélido y a procedencia desconocida».
