# 26_clave_local: diseño congelado

Escrito antes de calcular cualquier acuerdo entre quipus. Lo que se añada después de correr va en «Desviaciones» de `informe.md`. La única salida que se mira antes de congelar es la de `estructura.py` (§6): cuenta pares y simula potencia, sin calcular distancias entre quipus.

## 0. Pregunta

¿La clave de formulario es propia del archivo (más acuerdo dentro del archivo que entre archivos) **sin UR053A–E** y sin comparar etiquetas de color?

## 1. Representaciones invariantes al vocabulario

Solo colgantes de nivel 0, en el orden de KFG, con los grupos de KFG. Color fino normalizado con `re.sub(r'\([^)]*\)','',s)`. Se reutiliza `22_formularios/detector.py` (`cargar`, `candidatos`, `anova`, `perfil`).

- **R1, partición de color.** Los candidatos cromáticos finos (`Cf`) de detector.py: motivo contiguo dentro del grupo, k = 2–12, ≥ 3 bloques válidos, ≥ 2 colores, sin color ausente. Cada motivo se **recodifica por orden de aparición** (W|R|W|A → «ABAC»). El patrón es la cadena recodificada; el nombre del color se pierde. Si varios motivos de un quipu dan el mismo patrón, se queda el de menor p_col. Entra solo si p_col < 0,05 (ANOVA de posición tras quitar la escala del bloque): es un formulario en ese quipu.
- **R2, posición.** Los candidatos `P` de detector.py (grupos de exactamente k colgantes, ≥ 3 bloques). No usan color. Entra si p_col < 0,05.
- **R3, descriptores de forma (secundario).**
  - *bandas*: fracción de cambios de color entre colgantes adyacentes que caen en una frontera de grupo;
  - *cabecera*: fracción de grupos de ≥ 3 colgantes cuya primera cuerda tiene un color distinto al color modal del grupo.

  Los dos se calculan por quipu, sin nombres de color.
- **Reparto.** Para R1 y R2, el perfil de detector.py: la media por posición del log1p centrado por bloque (clr). Distancia euclídea entre perfiles del mismo patrón.

## 2. Validación de la invariancia (antes de la prueba)

- **Pares de validación.** Pares de `14_copias/filas_alineadas.csv` con investigadores distintos (copias y «mismo objeto»): el mismo contenido transcrito por dos personas. Se informa aparte UR1107~UR237, que es el mismo objeto en sentido inverso. Para R1 y R2 en ese par, UR237 se invierte (orden de colgantes y de grupos).
- **Medidas sobre colgantes alineados (nivel 0 en los dos):**
  1. coincidencia exacta de etiqueta;
  2. ARI (índice de Rand ajustado) entre las dos particiones de color;
  3. kappa del indicador «cambia el color respecto al colgante anterior alineado».

  Nulo: desplazamiento circular de las etiquetas de B (conserva las rachas), con 999 réplicas.
- **Medidas de quipu:**
  - si comparten un patrón R1 o R2 con d ≤ d\* (concordancia, §3);
  - la diferencia en *bandas* y *cabecera*, frente a la de pares al azar.
- **Criterio (congelado).**
  - Una representación se declara **validada** si, en los pares de validación, la concordancia de quipu es mayor que en pares al azar de los mismos investigadores (proporción, Fisher unilateral p < 0,05), o si el ARI mediano supera al nulo (Wilcoxon de signo frente al nulo por par, p < 0,05).
  - Para R3, la validación exige que |diferencia| en los pares de validación sea menor que en pares al azar (Mann-Whitney unilateral p < 0,05).
  - Una representación que no valide se informa igual, pero su prueba principal se marca «no invariante».

## 3. Concordancia de un par de quipus

- d\* = 0,434, heredado de 22_formularios: la distancia máxima entre UR053A, C y D en W|R|A. No se recalibra.
- s_R(a, b) = 1 si a y b comparten al menos un patrón de R con d ≤ d\*; si no, 0.
- **Primaria, incondicional.** Sobre todos los pares de quipus elegibles, es decir, con ≥ 1 patrón en R.
- **Secundaria, condicional.** Solo los pares que comparten ≥ 1 patrón.
- Variante solo con k ≥ 3.

## 4. Archivos (partición principal, con una etiqueta por quipu)

Se asigna por prioridad; la primera regla que se cumple gana.

1. **Nazca/Berlín:** UR1140, UR1136, UR223, HP056, UR234, UR1131.
2. **Santa:** procedencia exactamente «Santa» (UR087–UR092).
3. **Puruchuco–Huaquerones:** museo «Puruchuco Museum» o procedencia «Huaquerones».
4. **Leymebamba.**
5. **Armatambo:** cualquier grafía.
6. **Pachacamac × museo.** Berlín une las dos grafías, «Ethnologisches Museum» y «Museum für Völkerkunde».
7. **Ica × museo.** Procedencias con Ica, Ocucaje, Callango o Pisco; no Arica.
8. **Nazca × museo.**
9. **Inventario consecutivo** (la regla de 22_formularios/archivos.py: mismo museo, mismo prefijo, número ±1, componentes conexas) para los quipus que aún no tienen archivo.
10. Los demás quipus son singletons: solo forman pares «entre».

**Excluidos de la prueba principal:**
- **UR053A–E:** control positivo, que se corre aparte con la misma prueba.
- **Incahuasi:** análisis aparte (§7).

**Pares excluidos** (no son registros independientes):
- copias y mismo objeto de `14_copias/pares_resumen.csv`;
- quipus del mismo juego con letra (la misma base, como UR131A/B/C).

**Sensibilidad:** Ica y Pachacamac como un solo archivo por sitio.

## 5. Prueba principal

- **Estadístico:** T = Σ_s w_s (media de s dentro − media de s entre) / Σ_s w_s.
  - Los estratos s son los investigadores (regla de 24_color_formato: AS y UR ≥ 1000 = Ascher; resto de UR = Urton; JC, HP, KH, MM, QU).
  - Solo cuentan pares del mismo investigador.
  - w_s es el número de pares dentro de archivo del estrato.
- **Nulo:** permutar las etiquetas de archivo entre los quipus elegibles de cada investigador. Así se conservan los tamaños de archivo y la tasa base de cada investigador. B = 9 999; p unilateral (más acuerdo dentro).
- **Familia primaria:** {R1, R2} × incondicional, con Holm.
- **Secundarias, con BH sobre todas:**
  - condicional;
  - solo k ≥ 3;
  - estratos que incluyen pares de investigadores distintos (estratos = par de investigadores; el nulo sigue siendo la permutación dentro de investigador);
  - sensibilidad de la partición;
  - R3 bandas y cabecera (s = −|diferencia|).
- **Control positivo:** UR053A–E como único archivo, frente a los demás quipus de Urton, con el mismo T. Se espera p < 0,05 en R1.
- **Lectura:**
  - **clave local demostrada sin UR053** si R1 o R2 pasa Holm < 0,05 y la representación está validada (§2);
  - **apoyada** si solo pasa BH o solo nominalmente;
  - **no demostrada** si no pasa.

## 6. Potencia (declarada antes de correr)

- `estructura.py` cuenta pares dentro y entre por investigador y los pares que comparten patrón. No calcula d entre quipus.
- Luego simula S: los pares que comparten patrón concuerdan con probabilidad p1 si son de dentro de archivo y p0 si son de entre; los que no comparten, 0. Corre el mismo test por permutación (B = 999, 200 simulaciones).
- Escenarios (p1, p0): (0,22; 0,05), la tasa por etiquetas de 22_formularios sin UR053; (0,15; 0,05); (0,30; 0,10).
- La potencia queda escrita abajo, en §9, antes de la corrida principal.

## 7. Incahuasi (aparte)

- Incahuasi como archivo, frente al resto. Mismo T por investigador (UR y JC) y otro T con el par de investigadores UR–JC.
- El par UR–JC dentro de Incahuasi es justamente donde una representación invariante permite comparar entre transcriptores.

## 8. Refutación con la representación invariante

- **Universo:**
  - pares de quipus **estrictamente no relacionados**: archivos distintos, procedencia conocida, sin palabra de ≥ 4 letras común en la procedencia y museo distinto;
  - **cualquier investigador**, porque la representación lo permite;
  - UR053 e Incahuasi incluidos como miembros.
- **Medidas:**
  - para los pares que comparten un patrón R1 o R2 con k ≥ 3, la fracción con d ≤ d\*, frente al nulo de posiciones permutadas dentro del perfil (2 000 réplicas);
  - el **criterio individual**: k ≥ 3, p_col < 0,01 en los dos quipus, los dos con Q ≠ «no» en 22_formularios y d ≤ d\*.
- **El modelo se refuta** si se cumple (a) o (b):
  - (a) la fracción de pares estrictamente no relacionados con d ≤ d\* supera su nulo (p < 0,05) **y** no es menor que la fracción dentro de archivo sin UR053 (estimación puntual, misma representación);
  - (b) el número de pares que cumplen el criterio individual es ≥ 3, viene de ≥ 3 pares de sitios distintos **y** supera el percentil 95 de su nulo de posiciones permutadas.
- Si no se cumplen ni (a) ni (b), la predicción de refutación no se cumple.

## 9. Potencia calculada (pegada desde `estructura.py`, antes de la corrida principal)

Salida de `estructura.py`, corrida antes de calcular cualquier distancia entre quipus.

**Quipus elegibles (sin UR053 ni Incahuasi):**
- R1: 149 (AS 64, UR 58, HP 12, KH 6, QU 6, MM 3);
- R2: 136.

**Pares del mismo investigador:**

| R | investigador | dentro: n (comparten patrón) | entre: n (comparten patrón) |
|---|---|---|---|
| R1 | AS | 192 (155) | 1 824 (1 497) |
| R1 | UR | 122 (114) | 1 526 (1 306) |
| R1 | HP | 28 (28) | 38 (21) |
| R2 | AS | 113 (16) | 1 427 (236) |
| R2 | UR | 67 (15) | 1 417 (298) |
| R2 | HP | 21 (11) | 34 (2) |

- En R1, el 82–93 % de los pares comparte algún patrón (sobre todo «AB», que comparten casi todos). La concordancia descansa, por tanto, en el reparto.
- En R2 se comparte poco: el tamaño de grupo debe coincidir.

**Potencia** (200 simulaciones, B = 199, alfa nominal 0,05; supone pares independientes, así que es optimista):

| R | p1 = 0,22, p0 = 0,05 | p1 = 0,15, p0 = 0,05 | p1 = 0,30, p0 = 0,10 |
|---|---|---|---|
| R1 | 1,00 | 1,00 | 1,00 |
| R2 | 0,93 | 0,77 | 0,95 |

Con esta potencia, un resultado nulo en R1 es informativo frente a una clave local del tamaño que se observó por etiquetas sin UR053 (22 % frente a 5 %).
