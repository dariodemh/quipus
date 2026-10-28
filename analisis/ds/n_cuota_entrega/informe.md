# Cuota frente a entrega en Incahuasi: ¿P es la cuota y S1 la entrega?

**Carpeta:** `analisis/ds/n_cuota_entrega/`
**Fecha:** 18 de octubre de 2026
**Semilla:** 20261018 (todas las permutaciones)
**Datos:** `analisis/datos/cuerdas.csv`, `analisis/datos/quipus.csv`; OKR en solo lectura
(`data/external/open-khipu-repository/data/khipu.db`, `mode=ro`); scripts y salidas de
`analisis/13_sistema_incahuasi/` y `analisis/16_verificacion_incahuasi/`.
**Scripts:** `lib_cuota.py`, `01_p_vs_s1_incahuasi.py`, `02_ur270_perfil.py`,
`03_relaciones.py`, `04_control_externo.py`, `05_okr_cotejo.py`, `06_controles.py`,
`07_tabla_pruebas.py`.
**Salidas principales:** `p_vs_s1.csv` (entrega pedida), `p_vs_s1_incahuasi.csv`,
`pruebas_primarias.csv`, `pruebas_globales.csv`, `pruebas_quipu.csv`,
`control_magnitud.csv`, `ur270_ratios.csv`, `relaciones.csv`, `okr_cotejo.csv`,
`salida_01.txt` … `salida_07.txt`.

---

## 1. Pregunta

El equipo `n_espinoza1963` propuso que, en UR270, el colgante **P** registra la **cuota**
(un valor normativo y redondo: 22 igualdades exactas, 16 en el grupo 6, con valores
100/200) y la primera subsidiaria **S1** registra la **entrega** real (irregular); UR278,
al sumar P+S1 celda a celda, mezclaría ambas. La propuesta se apoyaba en un solo quipu
(n = 6 grupos) y no se había probado fuera de él.

Esta ronda la convierte en cuatro predicciones falsables:

1. Si P = cuota, P debe ser **más redondo**, **más repetido** y **más plano** que S1 en
   **todos** los quipus del sistema, no solo en UR270.
2. Si S1 = entrega, **S1/P** (cumplimiento) debe tener un **perfil estable por columna**
   en UR270.
3. Las relaciones bien apoyadas **UR270→UR278** y **UR278→UR275→UR266** deben pasar mejor
   con P, con S1 o con P+S1.
4. Si el patrón es propio del **sistema Incahuasi**, no debe aparecer en 20 quipus de
   otros sitios.

**Regla de alineación:** por número de grupo, sin saltar grupos vacíos; grupos PK =
separadores; celda = P+S1; la columna `j` es la posición del colgante dentro de su grupo,
contando colgantes presentes y ausentes.

---

## 2. Método

### 2.1 Datos, unidad y cobertura

- **Unidad de análisis: el quipu.** Los contrastes son pareados dentro de la celda
  (P y S1 del mismo colgante); luego se agregan por quipu. No se trata cada cuerda como
  observación independiente.
- **Celda analizada:** colgante con S1 existente y **ambos presentes y > 0**. El valor 0
  con `nudos` vacío es cuerda ausente (brief), no un cero.
- **Incahuasi = UR255–UR279** (28 quipus), como pide la tarea y como en 13/16. El metadato
  `procedencia` marca además JC001–JC023 (Sector B) y UR280; se analizan aparte como
  sensibilidad, no se mezclan.
- **Cobertura:** 663 colgantes con S1; **387 celdas** con ambos valores > 0 en **18
  quipus**. UR255, UR256, UR263, UR264, UR265, UR267A, UR273A, UR273B, UR274A y UR274B no
  tienen ninguna celda P/S1 con ambos valores > 0. UR270 aporta 94 celdas (24,3 %).
- **Control externo:** 396 quipus del corpus tienen celdas P/S1 (5 164 celdas). Se
  excluyeron Incahuasi/JC y se exigió ≥10 celdas por quipu: quedaron 146 elegibles; se
  muestrearon 20 al azar con semilla 20261018, de 13 procedencias distintas (AS, QU, UR de
  Leymebamba, Pachacamac, Ica, Paracas, Chuquitanta, Ocucaje, etc.).

### 2.2 Estadísticos

- **Redondez:** fracción de valores múltiplos de 10, 50 y 100.
- **Igualdades exactas:** pares de celdas del mismo grupo con el mismo valor, contados por
  separado para P y S1 y normalizados por el número de pares.
- **Plano:** CV (desviación típica / media) dentro de cada grupo con ≥3 celdas; media de
  los CV por rol. `dcv = CV(S1) − CV(P) > 0` significa P más plano.
- **Cumplimiento:** cociente S1/P por celda y su perfil por columna.

### 2.3 Nulos y corrección múltiple

- **Nulo principal: intercambio P↔S1 dentro de la celda**, con probabilidad 0,5. Preserva
  el par, el grupo, el tamaño de celda y la distribución conjunta de valores; solo destruye
  la **etiqueta de rol**. Es el nulo correcto para "¿importa ser colgante o subsidiaria?".
  5 000 réplicas por quipu; 20 000 en los agregados.
- **Nulos específicos:** permutación del vector de columnas dentro de cada grupo
  (UR270→UR278); permutación de cabeceras entre filas (UR270→UR273); permutación de
  cocientes dentro de cada fila (perfil S1/P); *sign-flip* por quipu.
- **Control de magnitud (la explicación aburrida):** P suele ser mayor que S1 y los valores
  grandes son más propensos a terminar en 0. Se repite el contraste (i) solo en celdas con
  P y S1 en la **misma década** y (ii) con un logit `redondez10 ~ rol + log10(valor) +
  efectos fijos de quipu`, errores agrupados por celda.
- **Corrección múltiple:** Holm y BH sobre una familia única de **35 pruebas primarias**
  (`pruebas_primarias.csv`), además de las correcciones internas de cada bloque. Se
  reportan ambos niveles. **Sobreviven Holm 9 de 36**; BH, 11 de 36.

### 2.4 Cotejo de fuente con OKR (solo lectura)

Se reconstruyó el valor de cada cuerda en OKR sumando sus nudos (`knot`: S/E por valor de
posición; L/LL por nº de vueltas × valor de posición) y se comparó con `cuerdas.csv`.
**Incahuasi nivel 0: 2 156/2 161 valores exactos (99,8 %; 27 de 28 quipus al 100 %).**
**Nivel 1 (conjunto de subsidiarias por colgante): 428/473 exactos (90,5 %; 21 de 28
quipus al 100 %).** UR255 es el único con discrepancias apreciables (91,9 % en nivel 0).
Los 20 controles tienen mediana de coincidencia 100 %, pero varias colecciones bajan al
20–40 % (diferencias de decodificación entre KFG y OKR, no del análisis). Conclusión: los
valores P/S1 de Incahuasi son sólidos y están verificados por una fuente independiente.

---

## 3. Resultados

### 3.1 Paso 1: P frente a S1 en los 28 quipus de Incahuasi

#### 3.1.1 Agregado de 387 celdas (18 quipus)

| prueba | observado | media nula | p perm | p Holm (5) | p Holm (36) |
|---|---:|---:|---:|---:|---:|
| redondez múltiplo de 10 | +0,0879 | 0,0000 | 0,0019 | 0,0037 | 0,048 |
| redondez múltiplo de 50 | +0,0775 | 0,0000 | 0,00005 | 0,00025 | 0,0017 |
| redondez múltiplo de 100 | +0,0749 | 0,0000 | 0,00005 | 0,00025 | 0,0017 |
| igualdades exactas (pares) | +0,0439 | 0,0002 | 0,0007 | 0,0021 | 0,0189 |
| CV (P más plano) | +0,1248 | 0,0000 | 0,0410 | 0,0410 | 0,86 |

A primera vista, la hipótesis acierta. Pero el agregado es engañoso por dos razones que se
ven en los apartados siguientes.

#### 3.1.2 A nivel de quipu la dirección no es general

| prueba | quipus | con diferencia > 0 | p signos | p Wilcoxon | p Holm (5 signos) |
|---|---:|---:|---:|---:|---:|
| redondez10 | 18 | 10 | 0,815 | 0,099 | 1,000 |
| redondez50 | 18 | 8 | 0,815 | 0,014 | 1,000 |
| redondez100 | 18 | 8 | 0,815 | 0,025 | 1,000 |
| igualdades | 18 | 3 | 0,0075 | 0,368 | 0,0377 |
| CV (plano) | 9 | 8 | 0,039 | 0,049 | 0,156 |

La redondez de P **no** es sistemática: 10/18, 8/18 y 8/18 quipus en la dirección
predicha; el test de signos no se acerca a la significación. Las igualdades sí tienen un
exceso agregado, pero **solo 3 de 18 quipus** van en la dirección predicha: el efecto está
concentrado en UR270 (19 pares de exceso) y UR271 (55 pares), mientras el resto suma –22
pares. No es "en todos los quipus"; es "en dos quipus, uno de ellos con muchos pares".

La heterogeneidad se ve directamente en los quipus con más celdas (la tabla completa está en
`p_vs_s1_incahuasi.csv`):

| quipu | celdas | dr10 (P–S1) | deq (P–S1) | dcv (S1–P) |
|---|---:|---:|---:|---:|
| UR270 | 94 | **+0,266** | +0,068 | +0,028 |
| UR262 | 70 | +0,071 | 0,000 | **+0,599** |
| UR272 | 51 | +0,020 | –0,109 | +0,037 |
| UR277 | 36 | +0,056 | –0,062 | +0,175 |
| UR271 | 32 | +0,094 | **+0,423** | +0,120 |
| UR269 | 20 | +0,050 | +0,167 | — |
| UR268 | 16 | 0,000 | 0,000 | — |
| UR266 | 13 | **–0,154** | 0,000 | — |
| UR278 | 13 | –0,077 | –0,081 | +0,135 |
| UR260 | 12 | 0,000 | –0,051 | **–0,251** |
| UR279 | 7 | **–0,429** | 0,000 | +0,024 |

Hay quipus con el signo contrario y quipus sin diferencia; la media agregada no representa
a la mayoría.

#### 3.1.3 El control decisivo: P es más redondo porque es más grande

P > S1 en 274/387 celdas (70,8 %); la mediana de S1/P es 0,41. En las **170 celdas con P y
S1 en la misma década**:

| prueba | n | dif. observada | discordancias P | discordancias S1 | p McNemar |
|---|---:|---:|---:|---:|---:|
| múltiplo de 10 | 170 | **0,0000** | 21 | 21 | **1,000** |
| múltiplo de 50 | 170 | +0,0118 | 7 | 5 | 0,774 |
| múltiplo de 100 | 170 | +0,0294 | 6 | 1 | 0,125 |

Y el logit con efectos fijos de quipu:

| término | coef | EE | p |
|---|---:|---:|---:|
| rol (P=1) | +0,283 | 0,238 | **0,235** |
| log10(valor) | +0,746 | 0,257 | **0,0037** |

**La explicación aburrida gana.** Al comparar valores de la misma magnitud, la ventaja de P
desaparece por completo para los múltiplos de 10 (21 vs 21) y no es significativa para 50
y 100. Lo que predice la redondez es el **tamaño**, no el rol. La "cuota redonda" no se
distingue de "P es el número grande".

#### 3.1.4 Dos controles que rematan el resultado

- **Quitando UR270:** el efecto agregado de redondez10 cae de +0,0879 a **+0,0307
  (p = 0,18)**. UR270 aporta el **73,5 %** del efecto agregado. Al quitar cualquier otro
  quipu, el efecto sigue entre +0,086 y +0,098 (p ≤ 0,003). **Todo el hallazgo agregado
  depende de un quipu.**
- **Mismo color:** en las **103 celdas donde P y S1 tienen el mismo color limpio**, las
  discordancias de redondez10 son **18 vs 17 (p = 1,000)** y P > S1 solo en 58 %. El
  contraste P/S1 está confundido con el color (en UR270, P es blanco y S1 es NB/W:NB). No
  se puede atribuir al rol.

**Resultado negativo principal:** no hay evidencia de que P sea más redondo que S1 por ser
"cuota"; el efecto bruto es un efecto de magnitud, confundido además con el color, y concentrado en UR270.

#### 3.1.5 La excepción UR270 y su grupo 6

UR270 sigue siendo atípico y merece registrarse:

- P: 39 % múltiplos de 10, 22 % de 50, 21 % de 100. S1: 13 %, 1 %, 0 %.
- Igualdades exactas: **23 en P frente a 4 en S1** (281 pares). Nuestro filtro de presencia
  da 23/4; el informe previo decía 22/3, la diferencia es solo el tratamiento de celdas
  ausentes. El fenómeno es el mismo.
- Grupo 6: P = `[200,200,100,100,100,200,200,100,100]`; S1 =
  `[70,97,58,61,61,92,41,54,59]`.
- **El grupo 6 es único en todo Incahuasi:** de **142 grupos con ≥5 colgantes**, es el
  único con todos los P en {100,200} y el único con ≤2 valores distintos y mínimo ≥50
  (1/142; p = 0,0070 sin corregir, Holm 0,176 y BH 0,025 en la familia de 36 pruebas;
  además fue seleccionado *post hoc* por el informe previo, así que el p real es mayor). Es una estructura deliberada,
  no ruido.

Nivel: **apoyado con datos** que el grupo 6 de UR270 es una estructura binaria deliberada;
**no apoyado** que esa estructura sea una "cuota" en el sentido de la hipótesis.

### 3.2 Paso 2: el cociente S1/P en UR270

UR270 tiene 7 grupos de 9 colgantes; 6 están completos (g0, g4, g5, g6, g8, g9). Matriz
S1/P (filas = grupos, columnas = j):

| g | j1 | j2 | j3 | j4 | j5 | j6 | j7 | j8 | j9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0,331 | 0,475 | 0,380 | 0,215 | 0,314 | 0,530 | 0,060 | 1,091 | 0,336 |
| 4 | 0,400 | 0,629 | 0,387 | 0,328 | 0,358 | 0,562 | 0,517 | 0,638 | 0,424 |
| 5 | 0,287 | 0,364 | 0,258 | 0,276 | 0,428 | 0,325 | 0,179 | 1,067 | 0,387 |
| 6 | 0,350 | 0,485 | 0,580 | 0,610 | 0,610 | 0,460 | 0,205 | 0,540 | 0,590 |
| 8 | 0,251 | 0,626 | 0,391 | 0,218 | 0,804 | 0,336 | 0,944 | 0,940 | 0,301 |
| 9 | 0,360 | 0,627 | 0,278 | 0,323 | 0,426 | 0,180 | 0,633 | 1,879 | 0,478 |
| **media** | 0,330 | 0,534 | 0,379 | 0,328 | 0,490 | 0,399 | 0,423 | **1,026** | 0,419 |

Pruebas (nulo: permutar los cocientes dentro de cada fila, 20 000 réplicas):

| estadístico | observado | nulo | p |
|---|---:|---:|---:|
| SS_col/SS_tot (varianza explicada por columna) | 0,495 | 0,159 | 0,0001 |
| RMSE de predicción *leave-one-out* por columna | 0,246 | 0,317 | 0,0001 |
| split-half Pearson (filas pares vs impares) | 0,952 | — | 0,0005 |
| split-half Spearman | 0,600 | — | 0,062 |
| Friedman de rangos por fila | χ² = 8,94 | — | 0,112 |

**Pero el perfil no es robusto:** está dominado por la **columna 8**, la única con media
> 1 (1,026; las demás 0,33–0,53). Al quitar la columna 8, SS_col cae de **0,495 a 0,160** y
el split-half de **0,952 a 0,603**; el Friedman de rangos no es significativo (p = 0,11).
No hay un "perfil de cumplimiento" de 9 columnas; hay **una columna anómala** (j8) que
entrega tanto o más que su cuota en 5 de 6 filas.

Además, **S1 > P en 93/387 celdas (24,0 %) en Incahuasi**, en 11/18 quipus, y en 10/94
celdas de UR270 (10,6 %). Si S1 fuera "entrega" y P "cuota", una entrega mayor que la cuota
en una de cada cuatro celdas exige una explicación adicional (atrasos, penalidades,
redondeos) que la hipótesis no da.

**Contraste directo con la idea de cuota fija:** si P fuera la cuota, debería ser más
estable por columna entre filas que S1. No lo es: el CV entre filas por columna es
**P = 0,299** y **S1 = 0,254**; ambos tienen perfiles de columna significativos (SS_col
P = 0,510, p = 0,00015; S1 = 0,591, p = 0,00005), y S1 es incluso algo más estable.
UR270 no muestra "P fijo / S1 irregular", sino **dos componentes con estructura de columna
parecida**.

Nivel: **apoyado con datos** que existe una anomalía estable en la columna 8 de UR270;
**no apoyado** que exista un perfil de cumplimiento de 9 columnas.

### 3.3 Paso 3: ¿las relaciones pasan con P, con S1 o con P+S1?

#### A) UR270 → UR278 (celda a celda, columna a columna)

Se replicó el diseño de `13.../07_ur270_ur278.py` para tres candidatos. Estadístico: nº de
grupos de UR270 cuya mejor fila de UR278 acierta ≥6 de 9 columnas (±1), y suma de
aciertos; nulo = permutar el vector candidato dentro de cada grupo (5 000 réplicas).

| candidato | grupos con ≥6/9 | aciertos totales | p (≥6) | p (total) |
|---|---:|---:|---:|---:|
| P | 0 | 11 | 1,000 | 0,509 |
| S1 | 0 | 4 | 1,000 | 0,653 |
| **P+S1** | **5** | **51** | **0,0002** | **0,0002** |

P+S1 reproduce UR278 (g0→g21 9/9, g4→g25 9/9, g5→g26 7/9, g8→g27 8/9, g9→g28 6/9);
P solo y S1 solo no reproducen nada. **La celda de UR278 es la suma de los dos
componentes**, no la cuota ni la entrega por separado.

#### B) UR278 → UR275 → UR266

Se reconstruye el total de cada fila de UR278 a partir de UR270 con cada candidato y se
compara con las cabeceras de UR275/UR266 (dentro de ±1):

| reconstrucción | filas que coinciden con una cabecera (de 6) |
|---|---:|
| P | 0 |
| S1 | 0 |
| **P+S1** | **4** (1653 exacta; 1940→1939, 2248→2247, 1766→1765) |

Solo P+S1 cae en el rango y en los valores de las cabeceras. Las dos filas restantes
(g5→g26 7/9 y g10→g29 5/9) tienen columnas en blanco y su suma queda corta; no cambian la
conclusión.

#### C) UR270 → UR273B / UR273A

Alineación g → g+9, consistente con los tres pares documentados en 13 (g0→fila 9, g8→17, g9→18); la regla se aplica a las 9 filas con cabecera disponible, no solo a esos tres pares. Comparando la suma de
P de cada grupo con la cabecera de **UR273B** (parte B) y la suma de S1 con la de
**UR273A** (parte A):

| contraste | exactas | ±1 | p (nulo de cabeceras) |
|---|---:|---:|---:|
| P = cabecera B | **4/9** | 4/9 | **0,0004** |
| S1 = cabecera A | 1/9 | 3/9 | 0,114 |

P suma exactamente la parte B (1200, 1332, 1575, 1256); S1 aproxima la parte A (453
exacta; 672 y 509 a ±1). Y lo decisivo: **la cuota explícita de los registros consolidados
es otra cuerda**. En UR275 g16: `1653 (W), 47 (NB), 1606 (NB)`; en UR266 g25:
`100, 1653 (W), 1153, 47`. El 47 (o 30/17 en los componentes) es la cuota; **P no es esa
cuerda, es el subtotal del componente B**. Llamar "cuota" a P confunde el subtotal con la
cuota.

Nivel: **bien apoyado** que la celda de UR278 = P+S1 y que P = subtotal del componente B;
**apoyado con datos** que S1 = componente A (1 exacta, 3 a ±1, p = 0,11; la señal es
direccional pero no alcanza significación con 9 filas).

### 3.4 Paso 4: control externo (20 quipus de otros sitios)

| bloque | n quipus | n celdas | redondez10 | redondez50 | redondez100 | igualdades | CV plano |
|---|---:|---:|---:|---:|---:|---:|---:|
| Incahuasi UR255–UR279 | 28 | 387 | +0,0879 (p=0,0013) | +0,0775 (p=0,00005) | +0,0749 (p=0,00005) | +0,0439 (p=0,0006) | +0,1248 (p=0,039) |
| Control 20 quipus | 20 | 527 | +0,0285 (p=0,108) | **+0,0361 (p=0,0005)** | +0,0057 (p=0,189) | **–0,0423 (p=0,999)** | +0,0208 (p=0,38) |
| JC001–JC023 (Sector B) | 23 | 139 | –0,0144 (p=0,71) | –0,0216 (p=0,94) | +0,0072 (p=0,50) | +0,0358 (p=0,13) | +0,1755 (p=0,017) |

Lectura:

- **El exceso de redondez de P no es propio de Incahuasi:** el control muestra el mismo
  efecto para múltiplos de 50 (+0,036; p = 0,0005), con la mitad de tamaño. Es una
  propiedad del corpus (P es el número grande), no del sistema.
- **Las igualdades sí son específicas:** en el control van en dirección **contraria**
  (–0,042; p = 0,999), es decir, S1 tiene más igualdades que P. Incahuasi es la excepción.
- **Incahuasi vs control** a nivel de quipu no difiere significativamente en ninguna de las
  tres medidas (redondez10 p = 0,68; igualdades p = 0,078; CV p = 0,42). Con 18 vs 20
  quipus no hay potencia para declarar una diferencia; lo honesto es decir que **no se
  demuestra que el patrón sea específico de Incahuasi**, salvo la dirección de las
  igualdades, que es sugestiva (p = 0,078).
- **JC (Sector B, también Incahuasi según el metadato):** no muestra redondez; sí muestra P
  más plano (CV +0,175; p = 0,017, Holm 0,39). Es un resultado aislado, no concluyente.

Nivel: **bien apoyado** que el efecto de redondez aparece también fuera de Incahuasi;
**apoyado con datos** que las igualdades son la parte más específica del sistema, pero
concentrada en dos quipus.

### 3.5 Resumen de corrección múltiple

`pruebas_primarias.csv` reúne 36 pruebas. **Sobreviven Holm (α = 0,05):**

1. redondez50 agregada Incahuasi (p = 0,00005; Holm 0,0017);
2. redondez100 agregada Incahuasi (p = 0,00005; Holm 0,0017);
3. SS_col del cociente S1/P en UR270 (p = 0,0001; Holm 0,0031);
4. UR270→UR278 con P+S1 (p = 0,0002; Holm 0,0060);
5. P = cabecera B (p = 0,0004; Holm 0,0116);
6. split-half del cociente S1/P (p = 0,0005; Holm 0,0140);
7. redondez50 en el control externo (p = 0,0005; Holm 0,0140);
8. igualdades agregadas Incahuasi (p = 0,0007; Holm 0,0182);
9. redondez10 agregada Incahuasi (p = 0,0019; Holm 0,0463).

**No sobreviven:** el control de magnitud (ninguna de sus 3 pruebas), el logit de rol, el
leave-one-out sin UR270, el mismo color, el Friedman del perfil, S1 = cabecera A, la
comparación Incahuasi vs control y las tres pruebas de signos de redondez. Es decir: **lo
que sobrevive es, por un lado, el efecto bruto de redondez (que los controles explican por
magnitud y que desaparece sin UR270) y, por otro, la estructura aditiva P+S1 = UR278 y
P = componente B.** El perfil S1/P sobrevive solo en su versión dominada por la columna 8.

---

## 4. Resultados negativos (explícitos)

1. **P no es más redondo que S1 por ser P.** En 170 celdas de la misma década: 21 vs 21
   múltiplos de 10 (p = 1,000); el logit da rol p = 0,235 y log10(valor) p = 0,0037.
2. **El efecto agregado desaparece sin UR270:** +0,0307, p = 0,18. UR270 aporta el 73,5 %.
3. **No es "en todos los quipus":** 10/18, 8/18 y 8/18 en redondez; 3/18 en igualdades.
   El test de signos de redondez no es significativo (p = 0,815).
4. **No es específico de Incahuasi:** el control de 20 quipus muestra redondez50 +0,036
   (p = 0,0005); Incahuasi vs control no difiere (p = 0,68 en redondez10).
5. **El color confunde el contraste:** en 103 celdas del mismo color, 18 vs 17 (p = 1,000); con la misma magnitud y el mismo color, no hay efecto.
6. **"Entrega ≤ cuota" falla:** S1 > P en 24,0 % de las celdas de Incahuasi (11 % en
   UR270) y en 11 de 18 quipus.
7. **P no es más fijo por columna que S1:** CV entre filas 0,299 (P) vs 0,254 (S1). No hay
   "cuota fija / entrega irregular".
8. **El perfil de cumplimiento no es robusto:** SS_col 0,495 → 0,160 al quitar la columna
   8; Friedman p = 0,11; Spearman split-half p = 0,062.
9. **S1 = componente A no alcanza significación:** 1/9 exactas, p = 0,11 (aunque 3/9 a
   ±1).
10. **La cuota ya está identificada y no es P:** en UR275/UR266 el 47 (o 30/17) es una
    cuerda aparte; P es el subtotal del componente B (4/9 exactas, p = 0,0004).

---

## 5. Nivel de evidencia

| afirmación | nivel |
|---|---|
| Los datos P/S1 de Incahuasi son fieles a OKR (99,8 % nivel 0; 90,5 % nivel 1) | **bien apoyado** |
| La celda de UR278 es P+S1 (5 grupos ≥6/9; p = 0,0002; P y S1 solos, 0) | **bien apoyado** |
| P es el subtotal del componente B (4/9 exactas; p = 0,0004) y la cuota explícita (47/30/17) es otra cuerda | **bien apoyado** |
| UR270 g6 es una estructura binaria 100/200 única en Incahuasi (1/142 grupos) | **apoyado con datos** |
| S1 es el componente A (1 exacta, 3 a ±1; p = 0,11) | **apoyado con datos / propuesto** |
| Existe una anomalía estable en la columna 8 de UR270 (S1/P ≈ 1,03) | **apoyado con datos** (pero es 1 columna) |
| P = cuota y S1 = entrega | **no apoyado**; la lectura de "dos componentes aditivos" la reemplaza |
| El patrón P/S1 es una propiedad del sistema Incahuasi | **no bien apoyado**; el control externo muestra el mismo efecto de magnitud |
| El significado de 100/200 en g6 (cuota por unidad, cupo, categoría) | **especulativo** |
| El significado de las 9 columnas (depósitos, días, grupos) | **especulativo** (heredado de 13) |

---

## 6. Limitaciones

- **n pequeño en los contrastes clave:** 18 quipus con celdas, 9 con grupos de ≥3, 6 filas
  completas en UR270. Los tests de signos tienen poca potencia; los de permutación
  pareada, mucha, pero no resuelven la independencia entre celdas del mismo quipu.
- **Confusión estructural:** en UR270, P es blanco y S1 es NB/W:NB; P es ~3 veces mayor.
  Rol, color y magnitud no se pueden separar dentro de ese quipu. Los controles de misma
  década y mismo color muestran que, fuera de esa combinación, el efecto desaparece.
- **Selección post hoc:** el grupo 6 y la columna 8 se eligieron después de ver los datos
  (informe previo); sus p-values no son confirmatorios.
- **La relación UR270→UR278 podría ser una tautología de codificación** si quien digitó
  UR278 calculó las celdas como P+S1. El nulo de permutación la descarta como artefacto
  estadístico, pero no como posible artefacto de registro. El cotejo OKR confirma que los
  valores existen en las cuerdas, no que se hayan codificado de forma independiente.
- **No se usó la procedencia de museo como origen** (brief). El "control externo" es
  diverso por procedencia declarada, con las cautelas del caso.

---

## 7. Para el coordinador

- **La hipótesis "P = cuota, S1 = entrega" no se sostiene.** P no es más redondo que S1
  cuando se controla la magnitud (21 vs 21 múltiplos de 10, p = 1,000; logit del rol
  p = 0,235), el efecto agregado desaparece al quitar UR270 (+0,031, p = 0,18) y el mismo
  exceso de redondez aparece en 20 quipus de otros sitios (redondez50 p = 0,0005).
- **Lo que sí queda bien apoyado es la estructura aditiva:** la celda de UR278 es P+S1
  (5 grupos con ≥6/9 columnas, p = 0,0002; con P solo o S1 solo, 0 grupos) y P suma
  exactamente la cabecera del componente B de UR273B (4/9, p = 0,0004).
- **La cuota ya estaba localizada y no es P:** en UR275/UR266 el 47 (y 30/17 en los
  componentes) es una cuerda aparte; P es el subtotal del componente B. Llamar "cuota" a P
  mezcla el subtotal con la cuota.
- **UR270 g6 es real y único:** de 142 grupos de ≥5 colgantes en Incahuasi, es el único
  con todos los P en {100,200} (1/142). Es una estructura deliberada, pero n = 9 y no
  permite decidir qué significa (¿cupo por unidad? ¿categoría?).
- **El "perfil de cumplimiento" S1/P no es de 9 columnas:** SS_col = 0,495 (p = 0,0001)
  pero cae a 0,160 al quitar la columna 8 y el Friedman de rangos da p = 0,11. Hay una
  anomalía en j8 (S1/P ≈ 1,03), no un perfil estable.
- **"Entrega ≤ cuota" falla en 24 % de las celdas** (S1 > P), y P no es más estable por
  columna que S1 (CV 0,299 vs 0,254): no hay "cuota fija / entrega irregular".
- **Calidad de datos verificada:** KFG y OKR coinciden en 99,8 % de los valores de nivel 0
  y 90,5 % de los conjuntos de subsidiarias de Incahuasi. Los resultados no son un artefacto
  de digitalización.
- **Recomendación 1:** abandonar la etiqueta "cuota/entrega" para P/S1 y pasar a
  "componente B / componente A"; probar si A y B corresponden a mitades, ayllus o
  categorías de tributarios (la literatura de 13/16 ya tiene la pista A+B).
- **Recomendación 2:** buscar un quipu donde P no sea sistemáticamente mayor que S1 (o
  donde P y S1 compartan color) para romper la confusión magnitud/color; y explicar la
  columna 8 de UR270 y el 100/200 de g6 con una fuente colonial o etnográfica.
- **Recomendación 3:** no usar el agregado de 387 celdas como evidencia de sistema: está
  dominado por UR270 (73,5 % del efecto). Los próximos contrastes deben ser
  leave-one-quipu-out por defecto.

---

## 8. Reproducibilidad

```
cd analisis/ds/n_cuota_entrega
python 01_p_vs_s1_incahuasi.py   # 387 celdas, 5 pruebas globales + 5 de signos + magnitud
python 02_ur270_perfil.py        # perfil S1/P, SS_col, split-half, Friedman
python 03_relaciones.py          # UR270->UR278, totales->UR275/266, UR270->UR273A/B
python 04_control_externo.py     # 20 controles + JC; escribe p_vs_s1.csv
python 05_okr_cotejo.py          # cotejo KFG vs OKR (solo lectura)
python 06_controles.py           # leave-one-out, mismo color, estabilidad, Holm/BH
python 07_tabla_pruebas.py       # 36 pruebas primarias, Holm y BH
```

Todas las permutaciones usan `numpy.random.default_rng(20261018)`. Los p empíricos son
`(k+1)/(N+1)`. `p_vs_s1.csv` contiene una fila por quipu (Incahuasi + 20 controles) con
las métricas, los p por prueba y sus versiones Holm/BH.
