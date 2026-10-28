# 06_nudos: nudos que no siguen la regla decimal, etiquetas y direccion de nudo

Pregunta: ¿hay cuerdas cuyos nudos NO siguen la convencion decimal y que podrian codificar informacion no numerica (etiquetas, nombres, signos)?

Datos: `analisis/datos/cuerdas.csv` (57 818 cuerdas, 651 quipus KFG; 40 162 cuerdas con nudos en 641 quipus; 64 490 racimos). Todo con semilla fija `20261017`. Scripts en esta carpeta, en orden: `01_parse.py`, `02_aburrida.py`, `03_etiquetas.py`, `04_direccion.py`, `05_catalogo.py` (+ `util.py`: Holm, BH, p empirico, Wilson). Salidas intermedias: `racimos.csv`, `cuerdas_flags*.csv`, `tabla_*.csv`, `catalogo_*.csv`, `0N_salida.txt`.

## 0. Hechos del dato que condicionan todo

- **`alt` esta vacio en las 57 818 cuerdas** (tambien en una muestra de los xlsx originales: 0 valores no vacios). El criterio "alt distinto de valor" no se puede evaluar: **resultado nulo por ausencia de dato**.
- En KFG el aporte de un racimo es siempre `n` para L y E (n = vueltas o cuenta), y `n*10^k` para S. Por tanto `valor` = suma de aportes (solo 41 cuerdas, 0,10 %, difieren). **El "valor" de una cuerda con varios racimos L/E es una simple suma sin pesos decimales**: en esas cuerdas el valor decimal no esta realmente definido (importante para quien use `valor`).
- Los nudos de dirección: 'Z' 33 866, 'S' 22 015, 'U' (desconocida) 8 541; la fuente AS casi no registra direccion (7 452 de 8 060 racimos son U).
- Tipos fuera de S/L/E: U (226), SP (210), TF (110), EE (108), LL (16), BL (11). 23 racimos sin valor aportado (UR044, etc.).

## 1. Violaciones de la convencion decimal (cuantificacion)

Definiciones (a nivel de cuerda con nudos, racimos ordenados de arriba abajo; nivel decimal de un S = log10(aporte/n); L/E/otros = unidades):

| Clase | Definicion |
|---|---|
| `nether` | L o E con otro racimo debajo; o S de unidades con algo debajo (definicion amplia de "nudo inferior") |
| `serie_LE` | >=2 racimos, todos L (o todos E): p. ej. `4L;5L;5L` |
| `orden` | niveles no estrictamente decrecientes de arriba abajo |
| `banda` | racimo fuera de la valla de Tukey (1,5 IQR, holgura min. 1,5 cm) de su nivel en su quipu (colgantes y subsidiarias por separado; >=8 racimos por nivel) |
| `L10` | L con >=10 vueltas |
| `Emulti` | E con n>1 |
| `tiporaro` | EE, LL, BL, SP, TF, U |
| `over9`, `L1`, `Spot` | >9 simples en un racimo; L de 1 vuelta; S con aporte distinto de n*10^k |
| `valor_dist`, `alt` | valor != suma de aportes; alt != valor |

Resultados (`tabla_prevalencia.csv`; 641 quipus con nudos):

| Clase | cuerdas (% de 40 162) | quipus >=1 (IC95 Wilson) | quipus >=3 cuerdas | quipus >=10 % | quipus >=50 % |
|---|---|---|---|---|---|
| nether | 3 026 (7,5 %) | 280 (43,7 %; 39,9-47,5) | 168 | 122 | 33 |
| serie_LE | 1 357 (3,4 %) | 157 (24,5 %) | 67 | 51 | 13 |
| orden | 3 329 (8,3 %) | 299 (46,7 %) | 173 | 137 | 34 |
| banda | 2 073 (5,2 %) | 391 (61,0 %) | 224 | 103 | 0 |
| L10 | 320 (0,8 %) | 55 (8,6 %) | 21 | 17 | 4 |
| Emulti | 97 (0,24 %) | 29 (4,5 %) | 9 | 7 | 1 |
| tiporaro | 567 (1,4 %) | 100 (15,6 %) | 29 | 16 | 3 |
| over9 | 23 (0,06 %) | 18 (2,8 %) | 2 | 3 | 1 |
| L1 | 23 (0,06 %) | 10 (1,6 %) | 2 | 0 | 0 |
| Spot | 47 (0,12 %) | 30 (4,7 %) | 1 | 1 | 0 |
| valor != suma | 41 (0,10 %) | 10 (1,6 %) | 2 | 2 | 1 |
| alt != valor | 0 | 0 | 0 | 0 | 0 |
| **cualquiera estructural** | 5 234 (13,0 %) | 474 (74,0 %) | 331 | 244 | 42 |

Lectura:
- Las violaciones de **posicion** (nudo inferior / series L/E / orden) son la clase grande; las violaciones de **cuenta** (>9 simples, L1, valor != suma) son residuales (<0,1 % de cuerdas) y suelen ser errores/convencion de registro: `over9` incluye casos con n = valor (`800S,800`, `59S`) y pares como `10S,100` (diez simples en decenas, que viola la regla de <=9).
- `L10`: en el 77 % n es multiplo de 10 y los racimos son del tipo `500L,500` / `100E,100`: **n codifica el valor, no las vueltas** (artefacto de transcripcion; AS090_N2 aporta 51 de 320, UR1095 37, UR193 30, KH0001 29). El 70,6 % de las cuerdas L10 esta en 10 quipus.
- `nether` en >=1 cuerda: 43,7 % de los quipus (26,2 % con >=3 cuerdas). Hyland (2024) da ">20 % del OKR" sin definicion operativa: es **compatible**, no una replicacion (definicion mia, mas amplia: incluye `L;L`, `L;E`, `L;S`).
- `banda`: 1 019 racimos (929 cuerdas) caen dentro de la valla de **otro** nivel (posible nivel mal asignado); el resto cae fuera de todas. Con valla de Tukey el 5 % es un umbral facil de cruzar: es la clase menos informativa (bandas que derivan a lo largo del quipu, ver 5).
- Concentracion: los 10 quipus con mas cuerdas `nether` contienen el 38,5 % de ellas; indice de dispersion frente a binomial 27,7 (nether), 19,5 (cualquiera), 18,2 (L10), 2,7 (banda). Las anomalias **no son ruido homogeneo: son propiedades de quipus concretos**.
- Top por clase (cuerdas): nether UR055 173, UR193 167, UR050 164, KH0001 115, UR054 113; serie_LE UR050 162, UR055 156, UR054 111, UR052 89, UR051 75; tiporaro UR193 106, UR211 82, UR203 50; L1 QU013 9, HP039 5.

Nivel de evidencia: la existencia y magnitud de las violaciones en los datos KFG es **bien apoyado (descriptivo)**; que reflejen la fisica del quipu y no el criterio de codificacion no esta resuelto (ver 2).

## 2. Explicacion aburrida (`02_aburrida.py`, `02_salida.txt`)

**2a. Investigador/fuente (prefijo de id).** Prueba Kruskal-Wallis con permutacion de etiquetas de prefijo entre quipus (4 000 permutaciones; quipus con >=5 cuerdas con nudos: UR 354, AS 130, HP 50, QU 21, JC 20, MM 17, KH 14), Holm sobre 11 clases:

| Clase | p perm. | p Holm | % quipus >=1 cuerda por prefijo |
|---|---|---|---|
| nether | 0,084 | 0,59 | AS 39, HP 28, JC 40, KH 64, MM 41, QU 38, UR 50 |
| serie_LE | 0,73 | 1 | AS 26, HP 16, UR 27 |
| orden | 0,136 | 0,81 | - |
| banda | 0,064 | 0,51 | AS 54, HP 64, UR 69, QU 81 |
| **L10** | 0,001 | **0,009** | AS 11, KH 21, QU 33, UR 8, HP 0, JC 0 |
| tiporaro | 0,005 | **0,047** | QU 29, KH 21, UR 20, AS 15, HP 0 |
| Spot | 0,004 | **0,047** | MM 12, QU 24, UR 5, AS 2 |
| valor != suma | 0,025 | 0,22 | KH 14, UR 2 |
| cualquiera | 0,26 | 1 | 60-86 en todos |

Las clases "de cuenta" (L10, tipo raro, Spot) **si dependen de la fuente**: son convenciones de transcripcion. La clase principal (nudo inferior, series L/E) **no** difiere significativamente entre fuentes (negativo; con 14-21 quipus en KH/QU/JC/MM la potencia para detectar diferencias moderadas es baja). Limite no resoluble con estos datos: Thompson (2026) documenta que Ascher asigna el tipo "por posicion" y Urton "por tipo de nudo"; eso podria fabricar o ocultar `nether` segun la fuente, y el prefijo solo lo captura de forma gruesa.

**2b. Conservacion.**
- A nivel de quipu (Spearman estratificado por prefijo entre la fraccion de cuerdas B/R/C [rotas, deshilachadas, cortadas, definiciones del OKR] y la tasa de anomalia): rho = 0,05 (nether, p = 0,23), 0,08 (cualquiera, p = 0,047, Holm 0,28), resto ~0. **Negativo.**
- A nivel de cuerda, permutando la etiqueta anomala dentro de cada quipu: las cuerdas `nether` estan **menos** rotas que lo esperado (366 vs 452,0 esperadas; p = 0,0005; Holm 0,0025), igual `serie_LE` (284 vs 321,6; p = 0,0005). La explicacion "anomalia = deterioro" predice lo contrario (cuerdas rotas pierden nudos del extremo, no ganan racimos extra). **Se descarta esa explicacion para estas clases.** `banda` y `L10`: sin efecto.
- Notas libres: el 10,0 % de las cuerdas nether lleva nota del investigador frente al 3,9 % del resto (7,8 % vs 4,1 % en banda): los registradores las vieron como peculiares, no como accidente conocido.

**Conclusion de la seccion**: parte de las anomalias (L10, tipos raros, S no n*10^k, >9 simples) se explica por **convencion de registro por fuente**. La clase grande (L/E con algo debajo, series de largos) **no** se explica por fuente ni por rotura segun estos proxies, y se concentra en pocos quipus (seccion 5). Es el residuo que merece estudio, con la advertencia de la asignacion por posicion vs por tipo.

## 3. Etiquetas (`03_etiquetas.py`)

**3a. ¿La primera cuerda del grupo/quipu es distinta?** Unidad = quipu; nulo: elegir la "primera" cuerda al azar dentro de cada grupo (grupos con >=3 colgantes; 596 quipus, 4 942 grupos) o del quipu (>=5 colgantes; 617 quipus); estadistico = desviacion respecto de la media de la unidad, promediada por quipu; 5 000 permutaciones; Holm sobre 32 pruebas.

Primer colgante del grupo (efecto; sd del nulo; p):
- rango (percentil) del valor **+0,039** (0,007; p = 2e-4), n.o de racimos **+0,085** (0,017; p = 2e-4), firma de tipos unica en el grupo **+0,029** (p = 6e-4): significativos tras Holm.
- Sin nudos, figura de ocho, largo, nudo inferior, subsidiarias: n.s. (p 0,02-0,45; ninguno sobrevive a Holm).
- **Ultimo** colgante del grupo: efectos de signo opuesto (sin nudos +0,030, rango -0,032, racimos -0,090; todos p = 2e-4).

Es el perfil de **orden decreciente dentro del grupo** (el primero es el mayor, el ultimo el mas vacio). **Control de tendencia** (residuo leave-one-out de la recta rasgo~posicion dentro del grupo, grupos >=5, 521 quipus; nulo por signo aleatorio entre quipus): rango del valor en pos. 1 residuo +0,012 +/- 0,013 (p = 0,37); n.o de racimos +0,021 +/- 0,033 (p = 0,50). **El exceso del primero desaparece al descontar la tendencia: no hay evidencia de que la primera cuerda sea un tipo distinto de cuerda ("etiqueta").** Un unico residuo sobrevive (cuerda sin nudos en pos. 1: +0,047, p = 4e-4, Holm 0,006) pero la tasa cruda de vacias por posicion es plana (0,316; 0,289; 0,326; ... 0,34) y la extrapolacion lineal de una variable binaria es poco fiable: lo clasifico como **no concluyente / probable artefacto**. Para el primer colgante del *quipu* el efecto "sin nudos" (+0,050, Holm 0,012) cambia de signo segun se pondere (pool: 0,283 vs 0,316 base) y tiene signos distintos por fuente (AS 0,17 vs base 0,43; QU 0,45 vs 0,31): **no robusto**.

**3b. Etiquetas repetidas en la misma posicion entre quipus de una misma procedencia.** Para cada posicion (colgante 1-5, ultimo, penultimo, primero del grupo 2 y 3) se mide el exceso de igualdad (valor, o firma tipo+n) entre pares de quipus de la misma procedencia frente a pares de procedencia distinta (excluidas Unknown; 234-323 quipus por posicion, 2 300-4 900 pares misma procedencia). Nulo: barajar la procedencia entre quipus dentro de prefijo (1 000); control adicional: la misma estadistica en 20 posiciones control (colgantes 11-30).
- **Resultado: nulo.** Exceso de igualdad entre -0,007 y +0,001 en las 18 pruebas, p de permutacion 0,44-0,998, Holm = 1 en todas; ninguna posicion supera a las posiciones control (p vs control >=0,19).
- Interpretacion: no hay indicio de valores o firmas "etiqueta" fijos en una posicion dentro de una procedencia. Salvedad: la procedencia de museo es mala etiqueta de origen, y solo ~300 quipus tienen procedencia conocida; pudo haber etiquetas por sitio concreto o por conjunto de quipus enlazados que este diseno no ve. La hipotesis de Saez-Rodriguez (n = 1, divisores elegidos a posteriori) **no recibe apoyo** en el corpus.

Nivel: ausencia de efecto de etiqueta tras control de tendencia = **apoyado con datos (negativo)**; el perfil decreciente del primero/ultimo = **bien apoyado (descriptivo)** y esperado por las relaciones de suma de Ascher.

## 4. Direccion de nudo dentro de la cuerda (`04_direccion.py`)

**4.1 Mezcla S/Z.** De 14 884 cuerdas con >=2 racimos de direccion conocida, 3 406 (22,9 %) mezclan S y Z, en 262 quipus (el 19 % de Ascher 2005 era por quipus, con otro criterio). **El 96,2 % de las mixtas es uniforme dentro de cada tipo de nudo**: la mezcla es la diferencia de direccion *entre tipos* (Z domina en simples, 72 %; 73 % en figuras de ocho; los largos 46 % Z, de modo que "S simple + L opuesto" es la norma de un quipu). Solo **131 cuerdas en 60 quipus** (0,9 % de las de >=2 racimos) tienen direcciones distintas dentro de un mismo tipo. Los racimos que difieren de la direccion modal de su quipu x tipo son el 4,3 % (mediana por quipu 0,5 %). Consistente con Clindaniel (2019) en que Z domina en simples; la tasa de Z por tipo y fuente es muy heterogenea (p. ej. JC 99 % Z en S; QU 17 % Z en L).

**4.2 Direccion vs posicion en cuerdas mixtas dentro del mismo tipo** (nulo: permutar direcciones dentro de la cuerda):
- S (62 cuerdas, 34 quipus): racimo superior Z, efecto -0,092, p = 0,21; correlacion direccion~nivel decimal (decenas vs centenas...) rho = -0,25, p = 0,048 (sin corregir; Holm sobre 4 = 0,19).
- L (42/19): -0,034, p = 0,75. E (22/9): -0,236, p = 0,081.
- **Negativo**: sin asociacion robusta con decenas/unidades. Muestras pequenas.

**4.3 Direccion de cuerda vs union R/V y color** (direccion modal de la cuerda; estadistico = media sobre quipus informativos de la diferencia de P(Z); nulo: permutar direcciones dentro de quipu x conjunto de tipos de nudo, 3 000 perm.; Holm sobre 11 pruebas):
- R vs V: efecto +0,009 (51 quipus, 4 944 cuerdas; p = 0,033; Holm 0,26). Cuerda blanca (W): +0,018 (164 quipus; p = 0,014; Holm 0,13). Hilo mixto (`:`): -0,004 (p = 0,77). Por fuente: efectos de signo inconsistente.
- **Negativo**: los efectos son <2 puntos porcentuales y no sobreviven a Holm; no hay asociacion de la direccion con la union ni con el color.

**4.4 Estructura en bloques a lo largo del quipu.** En 77 estratos quipu x conjunto de tipos (>=12 cuerdas, minoria >=10 %), contando cambios de direccion entre cuerdas vecinas frente a permutacion: **33 estratos en 23 quipus con q (BH) < 0,05**, frente a ~4 esperados por azar sin corregir (36 con p<0,05). Quipus: AS199, HP037, HP046_B, MM001, QU011, QU015, QU019, UR004, UR050, UR053C, UR085, UR087, UR103, UR1084, UR110, UR1104, UR1113, UR113, UR195, UR230, UR242, UR283, UR292A. Patrones extremos: UR1084 (L+S, 107 cuerdas): 1 cambio (5 Z y luego 88 S, esperados 31); UR1113: 11 Z y luego 62 S; QU011 y HP037: un solo cambio hacia la mitad del quipu (en el limite entre grupos 5 y 6 en ambos, aunque otros estratos de esos quipus cambian dentro de un grupo). No se asocian a cambio de union (UR1084 es 92/93 V). **Explicaciones aburridas pendientes**: cambio de mano/sesion del registrador en la transcripcion, o quipus compuestos; no se pueden separar con estos datos. Si la direccion codificara una division en mitades (analogo a Hanan/Urin de Hyland, Ware y Clark 2014) este es el patron que se vería; es **propuesto** como candidato, no probado. Los p estan limitados por 2 000 permutaciones.

## 5. Catalogo: 30 quipus con mas anomalias "estructuradas" (`05_catalogo.py`, `catalogo_top30.csv`, `catalogo_completo.csv`)

Definicion de "estructurada": para cada (quipu, familia) con >=5 cuerdas anomalas y >=10 con nudos, se pone a prueba si las anomalias estan **contiguas** en el orden del quipu, **concentradas en pocos grupos** o **concentradas en un color** frente a la permutacion de la etiqueta entre las cuerdas con nudos del mismo quipu (999 perm.; combinacion min-p de Westfall-Young; BH sobre 286 pruebas; q minimo alcanzable 0,0047). Si >80 % de las cuerdas con nudos son anomalas la familia es **sistematica** (convencion de todo el quipu; no permutable). Resultado: 98 de 286 pruebas con q<0,05 (esperadas ~14 por azar) + 11 sistematicas. Por familia: nether 43 (+6 sist), banda 52, tiporaro 6 (+3), raras 4 (+1), L10 4 (+1). La **firma** (secuencia de tipos) se reporta solo descriptivamente: usarla como estadistico seria circular, porque nether/tipo raro se definen por esa secuencia. Ranking = cuerdas anomalas en familias estructuradas, excluidas `banda` (ruido de valla: bandas que derivan a lo largo del quipu) y `L10` (artefacto n=valor). Solo 93 de 641 quipus tienen alguna familia estructurada de este tipo.

| # | quipu | procedencia museo | cuerdas c/nudos | anomalas estruct. | familia, n, % del quipu, firma modal (cuota entre anomalas), contraste | bloques dir. |
|---|---|---|---|---|---|---|
| 1 | UR055 | Unknown | 176 | 173 | nether 173 (98 %), L-L-L-L 31 %, SIST | |
| 2 | UR050 | Unknown | 164 | 164 | nether 164 (100 %), L-L-L 89 %, SIST | si |
| 3 | UR054 | Unknown | 114 | 113 | nether 113 (99 %), L-L-L 57 %, SIST | |
| 4 | UR052 | Unknown | 94 | 90 | nether 90 (96 %), L-L-L-L 34 %, SIST | |
| 5 | UR211 | Ica/Pisco | 83 | 82 | tipo raro 82 (99 %), TF 76 %, SIST | |
| 6 | UR051 | Unknown | 86 | 75 | nether 75 (87 %), L-L 85 %, SIST | |
| 7 | UR278 | Incahuasi | 292 | 66 | nether 66 (23 %), S-S-L-E 35 %, q = 0,005 | |
| 8 | UR144 | Valle de Pisco | 96 | 58 | nether 58 (60 %), L-L 84 %, q = 0,005 | |
| 9 | UR110 | Unknown | 85 | 51 | nether 51 (60 %), L-L 92 %, q = 0,005 | si |
| 10 | AS090_N2 | Peru | 58 | 42 | nether 42 (72 %), L-L-L 45 %, q = 0,005 | |
| 11 | AS069 | Lluta Valley | 398 | 40 | nether 40 (10 %), L-L 22 %, q = 0,005 | |
| 12 | UR112 | Unknown | 76 | 37 | nether 37 (49 %), L-L 89 %, q = 0,005 | |
| 13 | MM019 | Unknown | 218 | 30 | nether 30 (14 %), L-L 77 %, q = 0,005 | |
| 14 | UR188 | Unknown | 74 | 27 | nether 9, tipo raro 8, raras 10 (S-S-S-L-?), q = 0,005-0,022 | |
| 15 | UR113 | Nazca | 723 | 26 | tipo raro 26 (4 %), U-S, q = 0,005 (+49 banda) | si |
| 16 | UR120 | Huacho | 49 | 25 | nether 20 (E-E-E-E), raras 5, q = 0,005-0,03 | |
| 17 | UR044 | La puntilla (Paracas-Pisco) | 23 | 23 | raras 23 (100 %): valor != suma, SIST | |
| 18 | UR272 | Incahuasi | 213 | 23 | nether 23 (11 %), L-E, q = 0,017 | |
| 19 | AS026B | Unknown | 229 | 22 | nether 22 (10 %), L-L 82 %, q = 0,013 | |
| 20 | KH0083 | Mollepampa | 351 | 22 | nether 22 (6 %), L-L, q = 0,022 (+44 banda) | |
| 21 | AS207A | Unknown | 162 | 20 | nether 20 (12 %), L-E 50 %, q = 0,005 | |
| 22 | UR1145 | Pachacamac | 75 | 19 | nether 19 (25 %), L-L 79 %, q = 0,027 | |
| 23 | UR179 | Cajamarquilla | 16 | 16 | tipo raro 16 (100 %), U-U-U, SIST | |
| 24 | UR1091 | Unknown | 78 | 14 | nether 14 (18 %), L-L 86 %, q = 0,005 | |
| 25 | UR267A | Incahuasi | 76 | 14 | nether 14 (18 %), S-L-E 57 %, q = 0,020 | |
| 26 | UR178 | Cajamarquilla | 14 | 14 | nether 14 (100 %), S-S-S-S (S de 1 nudo espaciados, "conteo unario"), SIST | |
| 27 | UR006 | Leymebamba | 551 | 14 | nether 14 (3 %), L-L, q = 0,005 | |
| 28 | UR255 | Incahuasi | 65 | 13 | nether 13 (20 %), S-L-E 46 %, q = 0,024 | |
| 29 | UR005 | Leymebamba | 40 | 13 | nether 13 (32 %), L-L-L-L, q = 0,005 (+8 banda) | |
| 30 | JC012 | Incahuasi | 22 | 13 | nether 13 (59 %), E-E 92 %, q = 0,005 | |

Notas sobre los mejores candidatos (con su lectura aburrida):
- **UR050-UR055 (+UR039, UR112, UR110, UR144)**: cuerdas con 2-6 racimos de nudos largos de 4-9 vueltas, espaciados 10-30 cm entre si, direccion S dominante (UR050: 402 S, 99 Z; UR055: 689 S), colores W, DB o LK segun el quipu, sin patron decimal; KFG les asigna `valor` = suma de vueltas. Son los candidatos mas fuertes a **un sistema no decimal** (series de largos como signos). Procedencia desconocida (colecciones Soldi, Banco Central, Museo Oro): no se puede usar para contraste con documentos. Aburrida (no descartada): pueden ser un tipo de quipu no sumatorio ya descrito en la literatura (no lo he verificado) o una convencion de transcripcion de UR; en cualquier caso el valor KFG de esas cuerdas no debe usarse.
- **UR211 (TF)**: `1000TF,1000; 100TF,100; 10TF,10` con n = valor; **codificacion del valor en n con tipo propio** (TF sin glosa), no una anomalia fisica.
- **UR178 (Cajamarquilla)**: 4-5 nudos simples de 1 vuelta espaciados a lo largo de cuerdas blancas/AB: conteo unario, no decimal. Quipu de solo 14 cuerdas.
- **UR278, UR272, UR267A, UR255, UR270 (Incahuasi)**: S...L;E, esto es, E o L *debajo* del L de unidades, en 11-23 % de las cuerdas: es el patron "nudo inferior" de Hyland en un contexto de contabilidad inca. Estructurado (q <= 0,02) pero parcial: encaja con la lectura "E = marcador adicional por debajo de las unidades".
- **AS090_N2, AS019, AS004** (n = valor en L/E) son el caso de manual de **artefacto de codificacion**; excluir de cualquier lectura de contenido.

## 6. Resultados negativos (reunidos)

1. `alt != valor`: sin dato (campo vacio).
2. Primer colgante de grupo/quipu como "etiqueta" distinta del perfil de la cuerda: **no** tras control de tendencia.
3. Valores/firmas repetidos en la misma posicion entre quipus de la misma procedencia: **no** (18 pruebas, Holm = 1).
4. Direccion de nudo vs union R/V, color blanco/hilo mixto, decenas vs unidades: **no** tras correccion (efectos <2 pp).
5. Nudo inferior / series L/E explicados por investigador o por rotura: **no** (por prefijo, Holm 0,59; las cuerdas anomalas estan *menos* rotas, p = 0,0005).
6. Violaciones de cuenta puntuales (>9 simples, L1, valor != suma): <0,1 % de cuerdas, sin estructura; consistentes con error de registro.

## 7. Niveles de evidencia

- Prevalencia de violaciones de posicion (nether 43,7 % de quipus >=1 cuerda; 26 % >=3), concentracion en quipus concretos, ausencia de `alt`: **bien apoyado (descriptivo)** con la definicion usada; sensible a la asignacion por posicion/por tipo (Thompson 2026) **no resuelta**.
- La explicacion por fuente cubre L10, tipos raros, Spot (**apoyado con datos**); no cubre nether/series L/E (**apoyado con datos, negativo**).
- No hay efecto de "etiqueta" en la primera cuerda tras descontar la tendencia decreciente: **apoyado con datos (negativo)**.
- Direccion: la mezcla S/Z intra-cuerda es casi toda efecto del tipo de nudo (**bien apoyado**, 96,2 %); sin asociacion con posicion/color/union (**apoyado, negativo**).
- Estructura en bloques de direccion (23 quipus) y quipus de series de largos (UR050-055...): estructura **apoyada con datos**; interpretacion como contenido no numerico **propuesta/especulativa**.
- Que alguno de esos quipus codifique nombres, etiquetas o signos: **especulativo**; el analisis no aporta ninguna lectura, solo prioriza candidatos.

## 8. Ideas para la siguiente ronda

1. **Resolver la asignacion por posicion vs por tipo**: comparar el mismo quipu en OKR (`knot`, con `NUM_TURNS`, `AXIS_ORIENTATION`) y KFG, y repetir `nether` con la definicion de OKR; recalcular tras aplicar las correcciones de Thompson (2025).
2. **Revisar UR050-055, UR039, UR110-112, UR144** (series de largos): estudiar las secuencias de vueltas por cuerda como "palabras" (entropia, repeticion, longitud) con nulo por barajado de vueltas entre cuerdas del mismo quipu; ver si hay reutilizacion de secuencias (equivalente a etiquetas) y si el espaciado entre racimos es constante (regla vs azar).
3. **Bloques de direccion**: comprobar si los puntos de cambio coinciden con limites de grupo, cambio de color/fibra o cuerdas de union; en HP037/QU011/UR1084 mirar fotos o notas de campo para descartar cambio de registrador.
4. Fijar una definicion de "nether" (posicion + tipo) y pre-registrar la prueba antes de mirar mas quipus (la presente clasificacion es exploratoria; 98/286 pruebas de estructura son muchas).
5. Analizar el quipu **UR178 / UR179 (Cajamarquilla)** y UR211 como casos de codificaciones no decimales documentables.
6. Control cruzado: repetir 3a con la definicion de grupos de OKR (`cord_cluster`) para ver si el efecto del primero cambia.
