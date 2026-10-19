# 24_color_formato — diseño congelado (antes de mirar resultados)

Fecha: 2026-10-18. Semilla: **20261018** (todas las permutaciones). Escritura solo en esta carpeta.
OKR solo lectura (`file:...khipu.db?mode=ro`). KFG: `analisis/datos/cuerdas.csv`.

## 0. Conocimiento previo declarado (no es ciego)

Antes de congelar este diseño ya había leído:
- `14_copias`: en las copias el color se conserva **como partición** (NMI) más que como etiqueta; con nulo estratificado por valor, 4 de 6 familias del mismo registrador conservan color. UR1107/UR237 (mismo objeto, dos registradores) 0/21 códigos iguales.
- `13_sistema_incahuasi` §2.7: cabecera blanca en el 73 % de 222 registros (nulo 31 %); en UR270 la parte A (subsidiarias) es NB/W:NB y la B (colgantes) es W; vi las 3 primeras filas de `ur278_tabla.csv` (colores de fila AB, NB, NB).
- `ds/n_color_posicion`: NMI color~posición 0,505 vs 0,200; el efecto dentro de grupo desaparece sin la cuerda mayor.
- Puruchuco: las secciones de UR063/UR068 se **definieron por el ritmo de color** W / AB-MB / GG / W:KB (circularidad: ver P1c).

Por eso la parte de copias de P1 es **réplica**, no prueba nueva. Lo nuevo: color a través de **sumas** (Incahuasi y Puruchuco), función de cuerda en todo el corpus, transcriptor, códigos locales.

## 1. Normalización

- `color = re.sub(r'\([^)]*\)','',s).strip()`; vacío → NA.
- `base` = primer componente antes de `:`, `-`, `/`, `*`, `%` (p. ej. `W:MB`→`W`, `B:BB`→`B`).
- `compuesto` = el código normalizado contiene `:`, `-`, `/`.
- Cuerda **ausente** = valor 0 y `nudos` vacío (regla 6 del BRIEF). Cuerda **en blanco** = ausente y terminación ≠ `B` (no rota).
- Registrador (investigador) por prefijo KFG: `AS`, `UR`<1000 → `UR`, `UR`≥1000 → `AS` (series Ascher volcadas en UR, según 14_copias), `HP`, `QU`, `JC`, `MM`, `KH`. Captura de datos: `khipu_main.CREATED_BY` y `cord.CREATED_BY` de OKR (minúsculas).

## 2. Pregunta 1 — ¿el color viaja con el dato?

**Enlaces** (fuente → destino, nivel cuerda):
- **F1 copias**: las 25 parejas de `14_copias/filas_alineadas.csv` (color_A, color_B). Réplica.
- **F2 Incahuasi** (`13_sistema_incahuasi/grafo_cuerdas.csv`, solo enlaces entre quipus distintos y no-copia):
  - `suma_AB(parte A|B)`: componente (UR267A/B, UR273A/B, UR274A) → cabecera (UR266/269/275). Fuente = color de la cuerda componente.
  - `total_grupo`: fila de UR278 → cabecera de UR266/UR275/UR269. Fuente = color modal de la fila de UR278.
  - `suma_PS`, `parte_P`, `parte_S`: UR270 → UR273A/B, UR266, UR269, UR275.
  - **UR270 → UR278 celdas** (de `ur270_ur278.csv`, filas con ≥6/9 aciertos): fuente = colgante (W) y subsidiaria (NB) de UR270 en la columna j; destino = cuerda j de la fila de UR278.
- **F3 Puruchuco**: UR068 secciones (cuerdas 14–33, 34–53, 54–73) columna j → UR067 datos columna j (sin la cuerda 30) y → UR066 (13–32); UR063 (cortes 0,20,41,56,76,96,111; alineado por el final, grupos de 4) → UR068 central. Solo columnas cuya suma coincide (exacta o ±1 dígito).
  - **P1c (circularidad)**: como las columnas de UR068 se definieron por color, el color de la FUENTE es columna por construcción; el DESTINO (UR067/UR066) no intervino en la definición, así que su color sí es prueba.

**Estadísticos** (por familia de enlaces):
- `M` = proporción de enlaces con color destino == color fuente (para sumas con varias fuentes: == color de alguna fuente; se reporta también ==base).
- `NMI(fuente, destino)`.
- `H_dest` = entropía del color de destino y `W_dest` = proporción de destinos W.

**Nulos**:
- **N1 (emparejamiento)**: permutar los colores de destino entre enlaces de la misma familia y el mismo quipu destino (9 999 réplicas). Contesta: ¿el color concreto de la fuente predice el color concreto del destino?
- **N2 (paleta)**: sustituir el color de destino por el de una cuerda al azar del mismo quipu destino y mismo nivel. Contesta: ¿coinciden más que la paleta del destino?

**Predicción congelada / interpretación**:
- SEMÁNTICO (el color es identidad del dato) si M o NMI superan N1 en las familias de **suma** (no solo en copias).
- FORMATO si en las sumas M no supera N1 y el destino toma un color de rol del documento destino (W_dest alto o un único color dominante en el destino, independiente de la fuente).
- PARTICIÓN LOCAL si NMI > N1 pero M ≈ 0 (se conserva la agrupación con otra etiqueta).
- Mi expectativa previa (escrita antes): **formato** en Incahuasi (las cabeceras serán W sea cual sea el color de las partes), **conservación** en Puruchuco (el destino UR067 repetirá el ritmo de color).

## 3. Pregunta 2 — ¿el color marca la función de la cuerda?

Tipos (KFG salvo indicación):
- **T1 total de grupo**: colgante nivel 0 cuyo valor > 0 es exactamente la suma de los demás colgantes nivel 0 del grupo (≥2 otros con valor > 0).
- **T2 total de subsidiarias**: colgante con ≥2 subsidiarias de nivel 1 con valor, cuyo valor = suma de ellas.
- **T3 cabecera-máximo**: primera cuerda presente del grupo cuando es el máximo estricto del grupo y no es T1 (cabecera de registro tipo Incahuasi).
- **T4 en blanco**: colgante nivel 0 en blanco (def. §1) en grupo con ≥2 cuerdas anudadas.
- **T5 marcadora** (OKR `CORD_CLASSIFICATION='M'`) y **T6 cuerda superior** (OKR `'T'`), con color OKR `ascher_cord_color.FULL_COLOR` (PCORD_FLAG=0), comparadas con las demás cuerdas del mismo `CLUSTER_ID`/khipu.
- **T7 subsidiaria**: color de la subsidiaria nivel 1 frente al de su padre.

**Estadístico de distinción (D)** por instancia: 1 si su color ≠ color modal de las demás cuerdas de su grupo (T1–T4) o de su vecindad (T5–T6: las 6 cuerdas no-tipo más cercanas por ordinal en el mismo khipu); T7: 1 si color subsidiaria ≠ color padre.
**Nulo NG (grupo)**: la instancia se sustituye por una cuerda no-tipo al azar del mismo grupo (T1–T4) / vecindad (T5–T6); T7: subsidiaria sustituida por otra subsidiaria nivel 1 del mismo quipu → ¿coincide con el padre?
**Nulo NP (posición)** para T1 y T3: cuerda no-tipo de otro grupo del mismo quipu en la misma posición relativa (primera / última / interior). Controla «el color marca posición».
Por quipu (≥3 instancias): p de permutación (1-cola, D_obs ≥ D_nulo, 1 999 réplicas), BH por tipo; conteo de quipus q < 0,05 contra 5 % (binomial). Global: suma de D sobre quipus contra el nulo (9 999 réplicas).
**Color preferido entre quipus**: para cada quipu con ≥3 instancias, color modal del tipo. Estadístico: nº de quipus cuyo modal del tipo es W (y el color modal más frecuente); nulo: permutar la etiqueta de tipo dentro de grupo (T1, T3, T4) o dentro de khipu (T5, T6), 1 999 réplicas. «Mismo color entre quipus» se acepta solo si ese conteo supera el nulo con p < 0,05 tras Holm.
Predicción congelada: T1 y T3 distintos de su grupo por encima de NG (sí) pero no por encima de NP (el total ya está en una posición marcada); T5 marcadoras muy distintas; preferencia W de T1/T3 entre quipus débil (como el «resto compartido débil» de 22_formularios).

## 4. Pregunta 3 — efecto del transcriptor

- Por quipu: nº de colores distintos (normalizados), nº de bases, fracción de cuerdas con color compuesto; **rarefacción** a 40 cuerdas (media de 200 submuestras) para quitar el efecto tamaño.
- Prueba: Kruskal-Wallis del alfabeto rarefactado por registrador; nulo permutando la etiqueta de registrador entre quipus (9 999). Confusión declarada: registrador ~ colección ~ región. Control: comparar registradores dentro de la misma región/procedencia cuando haya ≥2 registradores con ≥5 quipus.
- Igual con `CREATED_BY` (captura) dentro del registrador UR.
- Mismo objeto leído dos veces (KH0033/UR044, UR1107/UR237, AS125/UR247, y pares de `pares_resumen` con tipo `mismo_objeto`): concordancia de etiqueta y NMI.
- **Robustez de conclusiones**: rehacer dentro de cada registrador con ≥15 quipus (UR, AS) (a) NMI color~grupo vs nulo y (b) D de T1 y T3 vs NG. La conclusión «color = formato» se mantiene si (a) y el patrón de (b) tienen el mismo signo y significación en cada registrador.

## 5. Pregunta 4 — códigos locales fuertes

Quipus: UR123, HP017, QU013, UR208, AS128, UR231, UR1152, UR1140 (lista fija, de n_color_posicion).
Para cada uno y para cada color (≥3 cuerdas): n, valor mediano, log1p medio, posición media en el grupo, nº de grupos, fracción de totales (T1/T2), torsión, nivel, terminación, compuesto.
Medidas (η² de color sobre log1p(valor) en cuerdas presentes nivel 0, con p de permutación 4 999):
- (a) color crudo; (b) color colapsado a base (compuestos → base); (c) residual tras efectos fijos de grupo; (d) residual tras posición en grupo; (e) sin T1/T2 ni máximos de grupo; (f) η² de torsión sobre valor; asociación color~torsión (Cramér V).
Clasificación congelada:
- **ARTEFACTO de compuesto/ply** si (b) cae a < 50 % de (a) y el contraste está entre variantes `X` vs `X:Y` de la misma base.
- **MARCA DE TOTAL/ENCABEZADO** si (e) cae a < 50 % de (a).
- **MARCA DE GRUPO/COLUMNA** si (c) o (d) cae a < 50 % de (a).
- **TORSIÓN** si Cramér V color~torsión > 0,5.
- **CATEGORÍA LOCAL** si (a)–(e) se mantienen ≥ 50 % y p < 0,05.
Holm sobre los 8 p de (e) (la prueba más exigente).

## 6. Pregunta 5 — fuentes

Grep en `analisis/fuentes_txt/` (cronistas citados, Mackey, Salomon 2004, Hyland 2016/2017, Urton, Medrano, etc.). Clasificar cada cita: (A) color identifica rubro dentro del documento; (B) mismo color = mismo significado en todos los quipus; (C) color marca estructura; (D) color propio del autor/comunidad; (E) otro. Verificar a mano las citas que se usen en el informe.

## 7. Familia Holm de pruebas principales (congelada)

1. P1 Incahuasi sumas: M vs N1.
2. P1 Incahuasi sumas: NMI vs N1.
3. P1 Puruchuco: M (destino UR067/UR066) vs N1.
4. P1 copias mismo registrador: M vs N1 (réplica).
5. P2 T1 global D vs NG.
6. P2 T1 global D vs NP.
7. P2 T3 global D vs NG.
8. P2 T4 global D vs NG.
9. P2 T5 marcadoras D vs NG.
10. P2 T7 subsidiaria = padre vs nulo.
11. P2 preferencia W de T1 entre quipus.
12. P3 alfabeto rarefactado por registrador (KW permutado).
BH dentro de cada familia de pruebas por quipu.

## 8. Desviaciones

Se anotarán en el informe con motivo, sin borrar este texto.
