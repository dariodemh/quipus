# 14 · Crítica de copias, formato "fila + cuerda-total" y lista para museo

Equipo: archivística y crítica textual de copias. Fecha: 2026-10-17. Semilla fija 20261017 en todo.
Entradas (solo lectura): `04_concordancias/resultados/alineamientos.txt` y `pares_significativos.csv`, `datos/cuerdas.csv`, `quipus.csv`, `okr-kh-numbers.csv` y `khipu.db` (OKR).

Scripts (se ejecutan en este orden; ~3 min en total):
`copias.py` (alinea y clasifica los 25 pares; `--demo` autocomprueba la clasificación) → `copias_agregado.py` (pruebas entre pares) → `fila_total.py` (`--demo` incluido) → `ur118_ur119.py` → `verificacion_museo.py`.
Resultados: `filas_alineadas.csv` (cada cuerda de cada par, con su clase), `pares_resumen.csv`, `tests_sistematicos.csv`, `fila_total_*.csv`, `ur118_ur119_filas.csv`, `verificacion_*.csv` y las salidas `*_salida.txt`.

## 0. Resumen

1. **Los valores de los colgantes se conservan en las copias al nivel del ruido de lectura; lo que cambia de forma no aleatoria es la estructura y, parcialmente, el color.** En 13 familias de copias, el 86,6 % de los colgantes alineados tiene el mismo valor (395/456). En los tres duplicados de base de datos (el mismo objeto leído dos veces) es el 93,0 % (53/57); la diferencia no es significativa (Fisher p = 0,21). Las diferencias de valor entre copias son sobre todo de un nudo (54 %), sin dirección común, repartidas por posición decimal como las cifras no nulas (χ² p = 0,29) y, en parte, daño físico.
2. **Cuatro ediciones sistemáticas en dos pares, el resto es ruido.** UR233 no copia la capa de subsidiarias de UR1175 (42 de 51 subsidiarias sin pareja, frente a 1 de 178 colgantes); HP055→UR1084 omite 8 de 14 cuerdas "222" (Holm p = 3e-4); UR1175→UR233 repite 100→110 cuatro veces (p = 0,0035; Holm entre pares 0,063); HP055/UR1084 tiene un salto +10 repetido 5 veces (p = 0,008).
3. **Color: se conserva por encima del azar pero solo en parte; dirección de nudo y R/V no se conservan más que por azar.** Mismo registrador (6 familias): color exacto 14–83 % frente a 16–35 % del nulo simple; con el nulo estratificado por valor, Fisher combinado p = 7e-5. Dirección: 8 de 11 familias coinciden (esperado 5,6; p = 0,13); R/V: 3 de 7 (esperado 3,5).
4. **Formato "fila + cuerda-total suelta" en todo el corpus: 7 quipus con q<0,05 de 49 evaluables** (AS044, AS066, AS199, UR1096, UR118, UR119, UR166). AS066 y AS199 son nuevos; UR149 no se reproduce con la definición de grupos. No hay concentración significativa por procedencia, museo ni registrador tras BH.
5. **UR118 y UR119 no se emparejan fila a fila**: son dos registros paralelos del mismo formato, no copias.
6. **Para museo:** UR1107/UR237 (las 3 discordancias son lecturas de posición decimal sobre el mismo nudo), HP055/AS084, KH0049/UR122, Basilea/UR212. Hallazgo nuevo del OKR: el comentario de KH0469 dice que UR232 y UR233 tienen el mismo número de inventario.

## 1. Método

**Alineamiento.** Se reutilizan los alineamientos de 04 (Smith-Waterman con huecos sobre la secuencia de cuerdas con nudos). Para cada fila alineada se recuperan los atributos de `cuerdas.csv` (valor, nudos, color, largo, unión, torsión, terminación, nivel). Las cuerdas sin nudos entre vecinas no están en el alineamiento; se cuentan aparte como "vacía en el otro lado".

**Clases de diferencia de valor** (`clase_valor`, con autocomprobación):
- `exacta`.
- `pm1_nudo`: |a−b| ∈ {1, 10, 100, 1000}, es decir, un nudo de más o de menos en alguna posición (incluye acarreos como 99/100).
- `misma_cifra_otra_posicion`: mismas cifras no nulas con un cero insertado (187/1087).
- `transposicion`.
- `un_digito_otro`: una sola cifra distinta con salto ≥ 2.
- `varias_cifras`.
- `solo_A` / `solo_B`: cuerda sin pareja en el otro quipu, separada en colgante o subsidiaria.

**Atributos de forma** (por par, sobre las filas alineadas): color exacto y color compartido (algún código común), información mutua normalizada del color (NMI, invariante a la convención de etiquetas), dirección dominante de nudos simples y largos, torsión, unión R/V, correlación de largos (Spearman) y coincidencia del número de subsidiarias por colgante.

**Nulos** (todos por permutación, semilla fija, p empírico unilateral):
- color, torsión, unión, dirección y subsidiarias: se baraja el atributo de B entre las filas alineadas (2000 permutaciones; NMI 500);
- **color condicionado al valor:** el color de B se baraja solo dentro de las filas con el mismo valor. Si el color fuera una función del valor (columna), el nulo reproduce el dato y p = 1;
- largos: se baraja B (1000);
- sustitución repetida a→b: se baraja B entre las filas discordantes y se toma el máximo de multiplicidad;
- δ modal y cociente modal (¿actualización?): igual;
- omisión concentrada: hipergeométrica por valor (con ≥3 apariciones), Holm entre valores y entre pares;
- signo de las diferencias: binomial 0,5 (la orientación A/B es arbitraria, así que solo se interpreta dentro de un par);
- daño físico: McNemar entre las discordancias colgante-colgante (¿está rota, `terminacion` = B, la cuerda de menor valor más a menudo que la de mayor valor?);
- dirección/unión: la línea base es la composición del corpus por serie de registro; el esperado de cada familia es Σ P_A(c)·P_B(c) y el nulo, una simulación de Bernoulli (20 000).

**Registrador.** Las series UR1xxx son registros de Ascher volcados en la serie UR (04: UR1084 = AS084, UR1175 = AS175, UR1107 = AS107); se tratan como "AS". La comparación de color entre registradores distintos solo se hace con NMI, porque el vocabulario de color difiere: en el mismo objeto UR1107 (Ascher) y UR237 (Urton), 0 de 21 cuerdas coinciden en el código de color.

**Unidad.** Hay 25 pares, pero solo 13 familias de copia independientes (UR212 aparece en 4 pares; UR006/009/021, en 3; UR1175, en 2). Para las pruebas conjuntas se usa un representante por familia: HP055~UR1084, UR1175~UR233, KH0049~UR122, UR053B~C, UR006~UR009, UR064~UR068, UR1114~UR1123, UR066~UR067, UR1118~UR218, QU002~UR137, AS159~AS173, UR255~UR267A, MM016~UR212. Los 3 duplicados de base (KH0033/UR044, AS125/UR247, UR1107/UR237) son el control de "ruido de lectura de un mismo objeto". Los 3 pares débiles de 04 (AS128/QU013, UR113/UR271, MM019/UR131C) se excluyen de las pruebas conjuntas.

**Sesgo de selección que hay que tener presente.** Los pares se detectaron por coincidencia de valores y el alineamiento premia las coincidencias. Por eso "los valores se conservan" es en parte una consecuencia de cómo se encontraron las copias: no vemos copias que reescriban los valores. El color, la dirección y la unión no intervinieron en la búsqueda, así que sus resultados no tienen ese sesgo.

## 2. Tarea 1: crítica de copias

### 2.1 Panorama de los 25 pares (`pares_resumen.csv`)

| par | tipo | registrad. | alin. | exactas | ±1 nudo | otra posic./transp. | 1 cifra otra | varias | solo A/B | subs. sin pareja | color exacto (obs/nulo) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HP055~UR1084 | copia | HP/AS | 142 | 121 (85 %) | 8 | 2 | 5 | 6 | 18/9 | 0 | 0,14/0,11 |
| UR1175~UR233 | copia | AS/UR | 93 | 77 (83 %) | 11 | 1 | 1 | 3 | 43/0 | 42 | 0,10/0,03 |
| KH0049~UR122 | copia | KH/UR | 80 | 60 (75 %) | 2 | 0 | 5 | 13 | 11/8 | 17 | 0,30/0,32 |
| UR053B~UR053C | copia | UR/UR | 48 | 35 (73 %) | 3 | 0 | 8 | 2 | 0/0 | 0 | 0,83/0,28 |
| UR006~UR009 | copia | UR/UR | 61 | 55 (90 %) | 4 | 0 | 2 | 0 | 3/5 | 0 | 0,41/0,35 |
| UR064~UR068 | copia | UR/UR | 47 | 41 (87 %) | 4 | 0 | 2 | 0 | 2/3 | 2 | 0,60/0,18 |
| UR1175~UR232 | copia | AS/UR | 50 | 38 (76 %) | 6 | 1 | 2 | 3 | 18/0 | 11 | 0,22/0,06 |
| UR1114~UR1123 | copia | AS/AS | 10 | 10 (100 %) | 0 | 0 | 0 | 0 | 0/0 | 0 | sin color |
| UR009~UR021 | copia | UR/UR | 21 | 18 (86 %) | 1 | 0 | 2 | 0 | 0/0 | 0 | 0,24/0,17 |
| UR066~UR067 | copia | UR/UR | 21 | 20 (95 %) | 0 | 0 | 1 | 0 | 1/1 | 0 | 0,52/0,22 |
| UR006~UR021 | copia | UR/UR | 19 | 18 (95 %) | 1 | 0 | 0 | 0 | 1/1 | 0 | 0,58/0,53 |
| MM015~UR212 | copia | MM/UR | 13 | 13 (100 %) | 0 | 0 | 0 | 0 | 0/0 | 0 | 0,00/0,00 |
| MM016~UR212 | copia | MM/UR | 13 | 11 (85 %) | 1 | 1 | 0 | 0 | 0/1 | 0 | 0,00/0,03 |
| MM008~UR212 | copia | MM/UR | 8 | 8 (100 %) | 0 | 0 | 0 | 0 | 0/1 | 0 | 0,88/0,88 |
| MM016~UR1131 | copia | MM/AS | 5 | 5 (100 %) | 0 | 0 | 0 | 0 | 0/0 | 0 | 1,00/1,00 |
| UR1118~UR218 | copia | AS/UR | 8 | 7 (88 %) | 0 | 0 | 1 | 0 | 0/0 | 0 | 1,00/1,00 |
| QU002~UR137 | copia | QU/UR | 11 | 10 (91 %) | 1 | 0 | 0 | 0 | 1/0 | 1 | 1,00/0,61 |
| AS159~AS173 | copia | AS/AS | 8 | 8 (100 %) | 0 | 0 | 0 | 0 | 0/0 | 0 | 0,38/0,16 |
| UR255~UR267A | copia | UR/UR | 28 | 27 (96 %) | 1 | 0 | 0 | 0 | 2/12 | 1 | 0,14/0,17 |
| KH0033~UR044 | mismo objeto | KH/UR | 23 | 23 (100 %) | 0 | 0 | 0 | 0 | 0/0 | 0 | 0,91/0,69 |
| UR1107~UR237 | mismo objeto | AS/UR | 26 | 23 (88 %) | 0 | 2 | 1 | 0 | 0/0 | 0 | 0,00/0,00 |
| AS125~UR247 | mismo objeto | AS/UR | 15 | 14 (93 %) | 0 | 0 | 0 | 1 | 0/0 | 0 | 1,00/1,00 |
| AS128~QU013, UR113~UR271, MM019~UR131C | débiles | — | 28, 10, 8 | 100, 90, 88 % | — | — | — | — | — | — | — |

Los pares con <15 filas alineadas son demasiado cortos para estimar tasas; solo cuentan en los totales.

### 2.2 Línea base: cuánto difiere el mismo objeto leído dos veces

Los tres duplicados de base dan el ruido de lectura sin copista:
- **KH0033/UR044:** 23/23 exactas.
- **AS125/UR247:** 14/15; la discordancia es 3130 frente a 31111.
- **UR1107/UR237 (Ascher frente a Urton, el duplicado no documentado):** 23/26. Las tres discordancias son lecturas, no nudos distintos:
  - p20/p10, 100 frente a 10: el mismo nudo simple a 11,0 y 11,5 cm, leído como centenas por uno y como decenas por otro.
  - p27/p3, 50 frente a 500: cuerda superior sin largo registrado.
  - p7/p24, 60 frente a 66: Ascher anota un largo de 0 vueltas, `0L(44.5,U)`, donde Urton anota 6L.

Frente a esto, las copias dan 13,4 % de colgantes discordantes (61/456) y el mismo objeto 7,0 % (4/57). La diferencia no es significativa (p = 0,21), aunque la potencia es baja. Conclusión sobre los valores: **las copias no difieren en valor más de lo que difieren dos lecturas del mismo objeto**, salvo en los pares de la sección 2.4. *Apoyado con datos* (n pequeño, con el sesgo de selección ya dicho).

### 2.3 Qué tipo de diferencia de valor (colgante con colgante, 61 discordancias en las 13 familias)

| clase | n | % |
|---|---|---|
| un nudo (±1, 10, 100, 1000) | 33 | 54 % |
| una cifra, salto ≥ 2 | 14 | 23 % |
| varias cifras | 10 | 16 % |
| misma cifra, otra posición decimal | 3 | 5 % |
| transposición | 1 | 2 % |

- **Posición del error de un nudo:** 18 en unidades, 13 en decenas y 2 en centenas o millares. Esperado si el error cayera al azar sobre las cifras no nulas (47 %, 41 %, 11 %): χ² p = 0,29. Es decir, **errores de un nudo repartidos como las cifras**; no se concentran en una posición.
- **Dirección:** por par, B>A en HP055~UR1084 15/21 (p = 0,078), UR1175~UR233 11/15 (0,118) y UR064~UR068 5/6 (0,22). Ningún par es significativo; el conjunto en bruto (40/61) depende de qué quipu se llame A, así que no se interpreta.
- **Daño físico:** entre las 61 discordancias, la cuerda de menor valor está rota (terminación B) y la de mayor no en 8, y al revés en 1 (McNemar unilateral p = 0,020). Todo viene de HP055/UR1084 (7 frente a 0, p = 0,008). Allí cuerdas de color PG (y una MB) de 12–25 cm, con terminación B, leen 30, 20 o 10 donde UR1084 lee 32 (p36, p61, p73, p98) o 42 (p125): nudos de unidades perdidos por rotura. *Apoyado con datos* para HP055/UR1084; no hay efecto en el resto.
- **Cambios grandes coherentes ("valores actualizados"):** no se encuentran, salvo los casos de 2.4. Los discordantes de UR053B~C (33→53, 12→16, 20→25, 29→27, 17→14…) tienen signo mixto (B>A 5/8, p = 0,73), sin δ ni cociente común (p = 0,47 y 0,76). UR053B y UR053C comparten el inventario ATE 3517 y forman parte de un conjunto de cinco quipus atados (nota OKR): son hermanos, no un censo actualizado.

### 2.4 Ediciones sistemáticas

**UR1175 frente a UR233 y UR232 (versión con desglose).**
- Capa de colgantes: copiada (177 con pareja, 1 sin ella en UR233).
- Capa de subsidiarias: 42 de 51 sin pareja con UR233 y 11 de 16 con UR232. UR1175 tiene 35 subsidiarias en el tramo alineado (cuerdas LB, es decir marrón claro, bajo cada YB o W); UR233 solo 14.
- Sustitución repetida: 100 (YB) en UR1175 frente a 110 (AB) en UR233 cuatro veces (p. 5, 11, 23 y 29 de UR233), más un 120. En UR233 aparece un nudo de decena a 17,5–18,0 cm que UR1175 no tiene. Repetición de la misma sustitución: p = 0,0035 (Holm sobre 18 pares: 0,063). δ modal +10 ×4 (p = 0,002) y cociente modal 1,0 ×5 (p = 0,005); Holm sobre 6 pruebas: 0,012 y 0,030. La dirección de los nudos largos cambia (Z en UR1175, S en UR233).
- Lectura: UR233 reproduce el nivel de colgantes de UR1175 con un cambio regular de +10 en las cuerdas "100", y deja fuera las subsidiarias. *Apoyado con datos*; que sea una "actualización" o una convención de cuenta es *especulativo*. Es la mayor desviación coherente del corpus de copias.

**HP055 frente a UR1084 (Lima / París).**
- Omisión por valor: 18 cuerdas de HP055 sin pareja en 160 del tramo; ocho son las cuerdas 222 (W:AB), de 14 en total (hipergeométrica p = 1e-5; Holm 3e-4). Las ocho omitidas son p6, p19, p32, p45, p57, p94, p131 y p143; las otras seis sí se copiaron (p69 como 220, rota). La secuencia se repite por bloques (1080, 12, 22, 100, 40, 222, 23, 33…) y el 222 es el elemento del bloque que UR1084 salta. *Apoyado con datos*.
- Salto +10: 5 de 21 discordancias (nulo 2,45; p = 0,008; Holm sobre 6 pruebas 0,048): 55→65, 32→42 y tres veces 22→32.
- Lectura de posición decimal: p114, 187 en HP frente a 1087 en UR1084, con el mismo nudo a 3,0 cm leído como centenas y como millares.
- Dirección: los nudos largos son Z en HP055 y S en UR1084.

**KH0049 frente a UR122.** Los 12 colgantes largos coinciden (19 de 20 colgantes alineados). La diferencia está en las subsidiarias (41 de 60 exactas; 17 de KH0049 y 8 de UR122 sin pareja), aunque el número de subsidiarias por colgante coincide más que el azar (0,45 frente a 0,15; p = 0,001). UR122 tiene el 57,8 % de sus cuerdas rotas y KH0049 el 1,4 %, por lo que parte de las diferencias de subsidiarias es daño. *Versión con subsidiarias distintas*: apoyado; la causa, por verificar.

**UR255 frente a UR267A.** 27 de 28 exactas; UR267A intercala 12 cuerdas de color AB:MB (valores 191, 239, 84, 120, 80, 200, 142…) que UR255 no tiene (OKR: "UR255 'Match'", Incahuasi). Es una adición, no una edición de valores.

**Contra el patrón.** En los pares UR1114~UR1123, AS159~AS173, MM015/MM008~UR212, MM016~UR1131 y UR1118~UR218 los valores alineados son idénticos o con un solo error (de 8 a 13 filas): son tramos copiados literalmente.

### 2.5 Qué se conserva y qué cambia (13 familias, un representante por familia)

| atributo | resultado | nulo | nivel |
|---|---|---|---|
| valor del colgante | 86,6 % exacto (mismo objeto: 93,0 %) | selección (ver método) | demostrado que se conserva; ¡sesgado por selección! |
| presencia de la cuerda colgante | 5,6 % sin pareja (57/1011) | — | apoyado |
| presencia de subsidiarias | 25 % sin pareja (63/249); sin UR1175~UR233, 10,6 % (21/198), CMH p = 0,076 | CMH entre pares | solo UR1175~UR233 (y tendencia en KH0049~UR122) |
| número de subsidiarias por colgante | coincide más que el azar en 4 de 10 pares con subsidiarias | permutación | apoyado |
| color (mismo registrador) | exacto 0,14–0,83 frente a 0,16–0,35 del nulo simple (NMI estratificado por valor: 4 de 6 familias con p ≤ 0,05; Fisher 1e-5) | permutación estratificada por valor | apoyado con datos, pero con muchos cambios |
| color (distinto registrador) | NMI 0,40–0,69 frente a 0,19–0,46 (3 familias; Fisher 1,7e-6) | idem | apoyado: se conserva la partición, no la etiqueta |
| largo de cuerda | ρ mediana 0,31 (13 familias; 9 con p<0,05); mismo objeto 0,76–1,00 | permutación | apoyado: relación débil |
| dirección de nudos largos | coinciden 8/11 (esperado 5,6; p = 0,13) | composición del corpus | no demostrado |
| dirección de nudos simples | 9/11 (esperado 6,5; p = 0,10) | idem | no demostrado |
| unión R/V | 3/7 (esperado 3,5) | idem | no se conserva |

Para el mismo objeto la dirección coincide en las dos comparaciones evaluables (UR1107/UR237 y KH0033/UR044); R/V solo es evaluable en KH0033/UR044 y coincide. Con tan pocos casos, no se puede decir si el cambio de dirección en las copias (HP055/UR1084, UR1175/UR233, UR255/UR267A) es real; coincide con la lectura de "una mano por grupo" de 03.

**Orden de fidelidad aproximado: valor del colgante ≳ presencia de la cuerda > color (como partición) > largo > dirección ≈ R/V.** Lo que se copia es la secuencia de cantidades por cuerda (contenido); el color se reproduce en parte, como agrupación y no como etiqueta; la mecánica de anudado (dirección, R/V, largos exactos) cambia con el objeto. La lectura "el valor es el contenido y el resto es forma" es la más económica, pero con dos reservas: (i) el valor está inflado por el sesgo de selección; (ii) el color no es libre, está más cerca del contenido que la dirección o el R/V. *Propuesto*.

### 2.6 Resumen: ¿ruido o edición?

- **Ruido de copia/lectura:** la mayoría. Errores de un nudo sin dirección ni posición preferente, comparables a los del mismo objeto leído dos veces, más daño físico demostrable en HP055.
- **Edición sistemática:** en UR1175→UR233 (capa de subsidiarias y +10 en las cuerdas "100") y en HP055→UR1084 (se omiten 8 de las 14 cuerdas 222, +10 repetido). La versión con subsidiarias es un "desglose": propuesto.
- **No hay evidencia** de actualización de censos con cambios grandes coherentes en ninguna familia.

## 3. Tarea 2: formato "fila + cuerda-total suelta" en todo el corpus (`fila_total.py`)

**Definición.** Fila = grupo de colgantes (nivel 0, sin unión T) con ≥2 cuerdas con nudos y suma S ≥ 10. Suelta = grupo de 1 colgante con nudos, con índice de grupo ±1 respecto a una fila. Acierto = valor de la suelta igual a S (tolerancia 0), a ±1, o a ±2 % de S. "Antes" o "después" se decide por la numeración de las cuerdas, no por el índice de grupo: KFG ordena los grupos por posición en cm y a veces los invierte (UR118: la cuerda p38 es el total de la fila p39–44, pero su grupo viene después).

**Nulo por quipu.** Se barajan los valores de todas las cuerdas sueltas del quipu entre sus posiciones (2000 permutaciones), con BH sobre los quipus evaluables (≥3 candidatos). Nulo descriptivo adicional: la misma suelta frente a filas a distancia 2–5.

**Resultados.**
- Hay 498 quipus con ≥3 grupos, 161 con una suelta adyacente a una fila, y 49 evaluables con 576 candidatos.
- Aciertos con tolerancia 0: 51 (nulo 14,9; p = 0,0005). Con ±1: 66 (nulo 22,3; p = 0,0005).
- **Quipus con q<0,05:** tolerancia 0, siete (AS044, AS066, AS199, UR1096, UR118, UR119, UR166); ±1, seis (todos menos AS066, q = 0,063); ±2 %, los mismos siete.
- Los 7 coinciden con los de 10 (AS044, UR1096, UR118, UR119, UR166) más dos nuevos:
  - **AS066** (Cuzco): 6 aciertos de 31 candidatos; incluye 237 y 200.
  - **AS199** (Nueva York): 5 aciertos de 21; incluye 513, 489, 587 y 127.
  - **UR149** no se reproduce: 0 aciertos exactos y p = 0,022 (q = 0,12) con ±2 %. Su fila en 10 se definía con otra regla de grupos.
- **Tasa de acierto por distancia:** 8,9 % (51/576) con la fila adyacente y 1,2 % (17/1476) con las filas a distancia 2–5. Sin los 7 quipus marcados, 3,2 % (14/438) frente a 1,0 % (12/1170).
- **Exceso difuso:** sin los 7 marcados, quedan 14 aciertos frente a 7,2 esperados (p = 0,0015; con ±1, 24 frente a 11,6). Hay señal en más quipus (UR186 p = 0,022, UR047 p = 0,09, AS215 p = 0,07), pero ninguno pasa BH: muchos quipus tienen muy pocas filas para detectarlo.

**Concentración** (quipu = unidad; universo = 49 evaluables; marca = q<0,05 en tolerancia 0 o ±1; hipergeométrica, BH sobre 30 categorías):

| categoría | evaluables | marcados | esperado | p | q |
|---|---|---|---|---|---|
| procedencia Paracas | 2 | 2 | 0,29 | 0,018 | 0,27 |
| museo Göteborg | 2 | 2 | 0,29 | 0,018 | 0,27 |
| registrador AS (Ascher) | 12 | 4 | 1,7 | 0,051 | 0,38 |
| registrador UR (Urton) | 28 | 3 | 4,0 | 0,89 | 1 |

Paracas y Göteborg son el mismo par (UR118/UR119). **No hay concentración demostrable por procedencia, museo ni investigador.** Tres de los siete marcados son de procedencia desconocida; los otros son Pachacamac (UR1096), Paracas (UR118, UR119) y Huando/Chancay (UR166). *Negativo con potencia baja*.

**Lado del total.** En los quipus de la serie Ascher el total va después de la fila (AS044 6/8, AS066 6/6, AS199 6/6, UR1096 7/7; 25 de 27 aciertos). En UR118 va antes (6 de 7) y en UR119 antes (4/4); UR166 mixto (2/2). Es una diferencia por serie de registro y puede deberse solo a la dirección de numeración de cada registrador. *No se puede interpretar sin saber cómo numeró cada uno*.

### 3.1 UR118 y UR119 fila a fila (`ur118_ur119.py`, `ur118_ur119_filas.csv`)

Ambos son una tabla de filas de 6 cuerdas (a veces 8): la 1.ª es un **marcador** de valor constante por bloque, luego 4–5 cantidades, con la mayor en 4.ª–5.ª posición (mediana 224 en UR118 y 230 en UR119). El marcador es 16 en 14 filas seguidas de UR118, y 19 (4 filas), 25 (3), 19 (10), 31 (1) y 13 (6) en UR119. UR118 tiene 23 filas y UR119 24.
- **Total = suma de la fila (con el marcador):** UR118, 6 de 17 filas con total (|dif| ≤ 1: 7); UR119, 4 de 10. No coinciden con la suma incluyendo subsidiarias (0 en ambos). Se excluye de UR118 el último bloque de 8 cuerdas grandes (p160–p167), que no es una fila.
- **Las filas que no coinciden se explican en dos casos y se quedan sin explicar en el resto:**
  - UR118 p53–58: la cuerda del marcador no tiene nudos y total − suma = 16, el valor del marcador del resto.
  - UR118 p132–137 (total 530): tiene dos cuerdas sin nudos, y total − suma = 418 = 151 + 267, que son justo los valores de la fila siguiente p139–144 (total también 530, p138 = 530). Esa fila es una **copia con dos celdas perdidas** del bloque contiguo. Es un ejemplo de fila duplicada (10).
  - El resto de diferencias (11 positivas, 4 negativas, p = 0,12) no se explican por cuerdas rotas (0,24 frente a 0,20 cuerdas rotas por fila, p = 0,54).
- **Emparejamiento UR118↔UR119:**
  - Hay 1 par de filas con ≥2 columnas idénticas en la misma posición (UR118 p18–23 y UR119 p9–14, [91, 61]); nulo 1,05, p = 0,69.
  - El mejor alineamiento monótono de los totales de fila (desfases −4..4, ambos sentidos) da ρ = 0,44 (p = 0,42).
  - Las sumas de fila no difieren entre quipus (Mann-Whitney p = 0,27).
- **Lectura:** mismo formato, mismo archivo (Paracas, Göteborg), contenido distinto fila a fila: **dos registros paralelos**, no copia ni versión. Si fueran el mismo registro en dos fechas, las filas deberían alinearse y no lo hacen. *Apoyado con datos* (negativo; potencia limitada con 23–24 filas).

## 4. Tarea 3: lista para verificación en museo

Archivos: `verificacion_objetos.csv` (27 quipus: números de inventario de las dos fuentes, procedencia, nº de cuerdas, % de cuerdas rotas, cordón principal, notas del OKR), `verificacion_pares.csv` (17 pares con la predicción bajo "mismo objeto" y bajo "copia" y las cuerdas a mirar), `verificacion_UR1107_UR237.csv` (cuerda a cuerda) y `verificacion_HP055_UR1084.csv`.

### 4.1 Discrepancias de catálogo que conviene resolver primero

| objeto(s) | qué dicen las fuentes | acción |
|---|---|---|
| **UR232 y UR233** | `okr-kh-numbers`: VA63038(A) y VA63038(B); `khipu_main`: VA63038(B) y VA 63038 b. El comentario de KH0469 dice que las letras A y B las asignó Urton y que "los objetos reales tienen el mismo número de inventario" | confirmar si son dos objetos o dos partes de uno bajo VA63038; ambos copian partes de UR1175 (Pachacamac, VA42518) |
| **UR212** | `okr-kh-numbers`: VA42513; `khipu_main`: VA42508(A) | confirmar el número; es el original de las copias de Basilea |
| **Basilea MM008, MM015, MM016** | los tres con IVc.366.03; procedencia "Eduard Gaffron" | ¿un lote de fragmentos con un mismo número? ¿Colección Gaffron (UR166 también es Gaffron, de Huando)? |
| **KH0049** | un registro lista MNAAHP3550 y otro MNAAHP3550, 3884-147 | confirmar el segundo número (AS038 = HP036) |
| **AS159** | VA16138B frente a VA16138 A | solo formato |

### 4.2 Duplicado de base no documentado: UR1107 (=AS107) y UR237

- **Objetos:** Museum für Völkerkunde / Ethnologisches Museum, Berlín. UR1107: VA24370(B), procedencia "Marquez"; UR237: VA66834, procedencia desconocida. Ambos con 26 cuerdas con nudos (29 y 30 en total), cordón principal de 129,5 y 129,0 cm.
- **Evidencia:** valores idénticos en 23 de 26 cuerdas; numeración invertida (p1 de UR1107 = p30 de UR237); correlación de largos ρ = 0,96 y diferencia mediana de 1,25 cm (calibración con duplicados conocidos: KH0033/UR044 0 cm, AS125/UR247 2 cm).
- **Qué necesita el conservador** (tabla completa en `verificacion_UR1107_UR237.csv`):
  1. Medir el largo de las cuerdas de un extremo; predicción si es el mismo objeto: cada cuerda mide lo mismo que su pareja (±2 cm). Ejemplos: UR1107 p1 = 95,0 cm (UR237 p30 = 94,5), p5 = 57,5 (p26 = 57,0), p14 = 54,0 (p17 = 55,5). Salto atípico: p2 84,5 frente a 74,0.
  2. Comparar los tres nudos de lectura dudosa: p20/p10 (un nudo simple a 11 cm, ¿centenas o decenas?), p7/p24 (¿hay un nudo largo en la posición 40–44 cm o solo el hueco?) y las dos cuerdas superiores p27/p3 (50 frente a 500).
  3. Confirmar que ambos números VA (24370 y 66834) remiten a la misma pieza (registro de entrada, fotografías antiguas, etiquetas). Hipótesis de trabajo: la serie VA66xxx re-inventarió objetos ya registrados por Ascher (mismo patrón que KH0198: AS181 = UR236, VA66832).
  4. Notificar al OKR: UR1107/UR237 no está marcado como duplicado (sí lo están KH0033/UR044 y AS125/UR247).

### 4.3 Copias entre museos (lo que predice cada hipótesis)

**Bajo "dos objetos distintos con la misma secuencia" se espera:** nudos físicamente distintos (cuerda por cuerda), largos y torsión no relacionados (no hay identidad física: los largos no se parecen, ρ ≤ 0,5), y las diferencias de la lista son lecturas reales, no errores de transcripción. **Bajo "mismo objeto"** se esperan largos coincidentes (|Δ| ≤ 2,5 cm).

| par (museos) | evidencia 04/14 | cuerdas a mirar | verificar |
|---|---|---|---|
| **HP055 (Lima, MNAAHP 29934) ↔ UR1084=AS084 (Quai Branly, 71.1930.19.470)** | 142 alineadas, 121 exactas (q = 2e-86); ρ largos 0,31; ambos con cordón principal de 112 y 116 cm | las **cuerdas 222 de HP055** (p6, p19, p32, p45, p57, p94, p131, p143) sin pareja en UR1084; cuerdas cortas de color PG de HP055 (p36 = 30, p61 = 20, p73 = 10, p98 = 30, p125 = 30; 12–25 cm, rotas); p59, p145, p158 (HP lee 22, UR1084 lee 32); p78 (22 frente a 12); p114 (187 frente a 1087, nudo a 3 cm) | si las cuerdas 222 existen en UR1084 y fueron omitidas o están en otra parte del cordón principal; si los nudos de las PG rotas se han perdido; tensión/dirección S/Z de los largos (Z frente a S) |
| **KH0049 (=AS038/HP036, Lima) ↔ UR122 (Göteborg, 1938.45.0228)** | 80 alineadas; 19 de 20 colgantes coinciden (12 valores largos idénticos) | las subsidiarias bajo p78–p99 de KH0049 y p42–p63 de UR122: 17 y 8 sin pareja; UR122 tiene el 57,8 % de cuerdas rotas | si las subsidiarias que faltan están rotas o perdidas en UR122, o si son distintas |
| **Basilea MM008/MM015/MM016 (IVc.366.03) ↔ UR212 (Berlín, VA42513 o VA42508(A))** | tres tramos disjuntos de UR212 (p6–14, p140–153, p182–194; 8, 13 y 13 filas); MM016 además copia 5 cuerdas de UR1131 (VA42510) | MM016 p2/p4 (23, 21) frente a UR212 p152/p149 (22, 12); la cuerda extra 11 de UR212 p151 | si los fragmentos son parte física de un quipu con UR212 o una copia; orígenes en la colección Gaffron |
| **QU002 (Dallas, B376/T41299.23) ↔ UR137 (Lowe, 57.172.002)** | 11 alineadas, q = 5e-4; ρ largos 0,75 | p11 (25 frente a 24) y la subsidiaria p11s2 | los largos se parecen más de lo esperado en una copia (ρ = 0,75): comprobar si son el mismo objeto (dos museos de EE. UU.) |
| **UR1175 (Berlín VA42518) ↔ UR233, UR232 (VA63038)** | ver 2.4; ρ largos 0,29 y 0,17 | las cuerdas YB "100" de UR1175 (p3, p8, p18, p23) frente a AB "110" de UR233 (p5, p11, p23, p29); las subsidiarias LB de UR1175 | si UR233 tiene realmente un nudo de decena extra (a 17,5–18,0 cm) y si le faltan subsidiarias |
| **UR1118 ↔ UR218; UR1114 ↔ UR1123; AS159 ↔ AS173** (Berlín) | 8, 10 y 8 filas | p5 (935 frente a 932) en UR1118/UR218 | copias dentro del mismo museo (réplica de Urton 2005) |

**Para los pares con ρ de largos alto** (QU002/UR137, ρ = 0,75; UR1114/UR1123, 0,62; AS159/AS173, 0,63) la hipótesis "mismo objeto" no se puede descartar solo con los largos; la comprobación física decide.

## 5. Negativos y limitaciones

- No hay actualización de censos con cambios grandes coherentes en ninguna familia. Solo hay dos ediciones sistemáticas (UR1175→UR233 y HP055→UR1084).
- La dirección de nudo y el R/V no se conservan más que por azar (p = 0,13 y 0,77); la potencia es baja (11 y 7 familias).
- **El sesgo de selección sobre el valor no se puede corregir.** Las copias se detectaron por valores y una copia que los reescribiera sistemáticamente no aparecería. Una búsqueda independiente por color solo (o por posición/largo) en las parejas de un mismo registrador diría si hay copias de forma con contenido distinto; no se hizo.
- El alineamiento solo es monótono (no detecta reordenación de cuerdas) y trata las subsidiarias como elementos de la secuencia, así que en zonas con subsidiarias diferentes sustituye cuerdas sin relación (las 13 "varias cifras" de KH0049~UR122 son sobre todo eso).
- El color entre registradores distintos solo se evalúa con NMI. El código de color de UR1107 y UR237 (mismo objeto) no coincide en ninguna cuerda.
- La orientación A/B es arbitraria; los signos solo se interpretan dentro de un par. Las familias comparten quipus (UR212 en 4 pares): se usa un representante por familia en las pruebas conjuntas.
- Formato fila+total: solo 49 de 498 quipus tienen ≥3 candidatos; un quipu con 2 filas no se puede evaluar. Con valores pequeños y redondos (10, 20, 50) el nulo no es perfecto: AS044, UR1096 y AS066 incluyen totales de 15–50.
- "Antes/después" depende de la numeración del registrador; no se interpreta físicamente.

## 6. Niveles de evidencia

| conclusión | nivel |
|---|---|
| Las 25 parejas de 04 son copias o versiones (la mayoría con valores casi idénticos) | demostrado (04) |
| Los valores de los colgantes se conservan al nivel del ruido de lectura del mismo objeto (86,6 % frente a 93,0 %) | apoyado con datos (con sesgo de selección y potencia baja) |
| Errores de valor: un nudo, sin dirección ni posición preferente; parte de ellos es daño (HP055) | apoyado con datos |
| UR233 no copia la capa de subsidiarias de UR1175; UR233 añade +10 en las cuerdas "100" | apoyado con datos (un solo par) |
| HP055→UR1084 omite 8 de las 14 cuerdas 222 | apoyado con datos (un solo par) |
| La capa de subsidiarias es "lo que se rehace" en una versión | propuesto (dependiente de UR1175~UR233; CMH sin él p = 0,076) |
| El color se conserva como partición por encima del azar, no como etiqueta | apoyado con datos |
| Valor = contenido, dirección/R/V = forma; el color está en medio | propuesto |
| Dirección y R/V cambian con cada objeto (una mano por copia) | especulativo |
| Formato "fila + cuerda-total suelta" en 7 quipus (AS044, AS066, AS199, UR1096, UR118, UR119, UR166) | demostrado en esos quipus |
| El formato aparece de forma difusa en más quipus | propuesto (exceso residual p = 0,0015; ninguno individual pasa BH) |
| Concentración por procedencia, museo o investigador | negativo (ninguna pasa BH) |
| UR118 y UR119 son registros paralelos, no copias | apoyado con datos |
| UR1107/UR237 son el mismo objeto | apoyado con datos (largos ρ = 0,96); falta confirmar en museo |
| UR232 y UR233 comparten número de inventario | demostrado (comentario del OKR) |

## 7. Siguiente ronda

1. **Verificación en museo** (sección 4), empezando por UR1107/UR237 y los números VA63038 y VA42513/VA42508(A).
2. **Búsqueda de copias de forma:** alinear las secuencias de color (con nulo de bloques) dentro de cada registrador y ver si hay pares que copian el color y no los valores; es la contraparte sin sesgo de selección del resultado "valor = contenido".
3. **Subsidiarias de UR1175:** probar si sus valores (LB) son sumas o desgloses de los colgantes de UR233/UR232, y si el +10 en las cuerdas "100" de UR233 corresponde a una subsidiaria de UR1175.
4. **HP055/UR1084:** completar la lista de las cuerdas 222 omitidas y comprobar si las omisiones coinciden con el cambio de bloque de dirección de nudos de UR1084 señalado en 06 (5 Z y luego 88 S).
5. **AS066 y AS199:** reanalizar como tablas con total suelto; su serie (Ascher) y la dirección de numeración. **UR149:** revisar con la definición de filas de 10.
6. **Fila + total en más quipus:** relajar el mínimo de candidatos (≥2) usando una prueba conjunta por registrador.
