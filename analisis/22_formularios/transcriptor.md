# 22_formularios: control por transcriptor

**Motivo.** 24_color_formato mostró que el vocabulario de color depende de quién transcribe:
- en 40 cuerdas, Ascher distingue unos 6 colores, Urton 9,7 y Clindaniel 14,9;
- UR1107 (Ascher) y UR237 (Urton) son el mismo quipu y coinciden en 0 de 23 etiquetas.

Por eso el contraste «mismo reparto dentro del archivo frente a entre archivos» y la prueba de refutación de `informe.md` §4 podían estar confundidos con el transcriptor.

**Script:** `transcriptor.py`. Lee `refutacion_pares.csv` y usa OKR en solo lectura.

**Salidas:**
- `transcriptor_quipus.csv`
- `transcriptor_pares_inv.csv`
- `transcriptor_pares_dig.csv`
- `transcriptor_resumen.csv`
- `salida_transcriptor.txt`

## Dos definiciones de transcriptor

| definición | qué mide | regla |
|---|---|---|
| **inv** (investigador) | quién **observó y nombró los colores** | prefijo del registro, la misma regla de `24_color_formato/comun24.py`: AS y UR ≥ 1000 = Ascher; UR = Urton; JC = Clindaniel; HP; KH |
| **dig** (digitalizador) | quién **cargó las cuerdas** en la base de datos | moda de `cord.CREATED_BY` en OKR, como pidió el coordinador |

- **`CREATED_BY` no es el observador.** Los registros de Ascher los cargaron sobre todo katie (129) y leah (60). Los de Urton, al menos 10 personas: gurton 84, cbrezine 59, eric 39, tania 34, julia 32, …
- La definición relevante para el vocabulario de color es **inv**. La **dig** se informa como control secundario.

## Confusión en el análisis original

| pares (mismo motivo de color fino) | mismo investigador | mismo digitalizador |
|---|---|---|
| dentro de archivo (n = 168) | 90 % | 92 % |
| entre archivos sin relación (n = 224) | 48 % | 23 % |

La confusión era real: la comparación original enfrentaba sobre todo «mismo transcriptor» con «transcriptores mezclados».

## Resultado con el investigador fijo

La métrica es la fracción de pares con el mismo motivo cuyo reparto está dentro de d\* = 0,434. El nulo permuta las posiciones de un perfil.

| investigador | k | dentro: cerca / n (nulo) | entre: cerca / n (nulo) | Fisher OR, p | potencia «entre» para detectar 25 % |
|---|---|---|---|---|---|
| todos (pares del mismo investigador) | ≥ 3 | **25/96 = 26 %** (6,7) | **0/35 = 0 %** (0,2) | ∞, **0,0002** | 1,00 |
| todos | 2 | 27/56 = 48 % (14,6) | 13/73 = 18 % (10,1; p = 0,14) | 4,3, **0,0003** | 0,77 |
| **Urton** | ≥ 3 | 25/95 (6,4) | 0/14 (0,2) | ∞, **0,037** | 0,90 |
| **Urton** | 2 | 26/52 (14,0) | 13/67 (9,5; p = 0,084) | 4,15, **0,0007** | 0,73 |
| **Ascher** | ≥ 3 | 0/1 | 0/21 (0,0) | — | 1,00 |
| **Ascher** | 2 | 1/2 | 0/5 | — | 0,10 |
| Clindaniel | — | 0 pares | 0 pares | — | — |
| HP / KH | — | 2 / 0 | 0 / 1 | — | — |

- **Mantel-Haenszel**, estratificado por investigador y k: **OR = 5,5**. Es casi el mismo valor que el original sin estratificar (5,75).
- **Sensibilidad (UR053A–E domina).** Aporta 72 de los 95 pares de Urton con k ≥ 3 dentro de archivo y 20 de los 25 cercanos. Sin los pares UR053~UR053:
  - Urton, k ≥ 3: dentro 5/23 = 22 % (nulo 1,3; p = 0,002) frente a entre 0/14. Fisher p = 0,135.
  - Urton, k = 2: dentro 11/35 = 31 % (nulo 6,5; p = 0,013) frente a entre 13/67 = 19 % (nulo 9,5; p = 0,085). Fisher p = 0,22.

  La dirección se mantiene y los pares de dentro siguen superando su nulo. La diferencia con los de entre deja de ser significativa: hay pocos pares.

## Resultado con el digitalizador fijo (secundario)

- **OR de Mantel-Haenszel = 2,3.**
- cbrezine (Incahuasi y Leymebamba) tiene 99 pares dentro de archivo y **0 entre archivos**: no se puede comparar.
- **katie** (Ascher), k ≥ 3: dentro 3/11 frente a entre 0/21 (p = 0,033).
- **julia**, k ≥ 3: entre 4/14 cercanos (p = 0,0065 frente al nulo).
  - Son los mismos pares HP033~KH0049 (3 motivos) y HP033~UR272 que ya aparecían en `informe.md` §4.
  - **HP033 y KH0049 tienen investigadores distintos (HP frente a KH)** y comparten digitalizadora, museo (MNAAHP) y costa sur. Con el investigador fijo no forman par.

## ¿Aparece una clave compartida que la diferencia de vocabulario ocultaba?

**No.**

- Con el investigador fijo, los pares sin relación con k ≥ 3 cercanos son **0 de 35**:
  - Urton: 0 de 14, con procedencias Santa, Nazca, Incahuasi y Pachacamac;
  - Ascher: 0 de 21.
- La potencia para detectar una tasa del 25 %, la de dentro de archivo, es de 0,90–1,00.
- **El criterio congelado de refutación sigue en 0 pares** con las dos definiciones.
- **Lo único que queda son pares con k = 2.** En Urton hay 13 de 67 cercanos frente a 9,5 esperados (p = 0,084): motivos W\|MB, MB\|AB y W\|AB entre Leymebamba, Huaquerones y Pachacamac.
  - Es el resto débil de «el blanco o el claro va con lo mayor» que ya se había visto.
  - Con el investigador fijo deja de ser significativo (antes: 25 frente a 18,7, p = 0,02).
  - Por diseño, k = 2 no refuta.

## Potencia (pares por transcriptor)

| investigador | dentro, k = 2 / k ≥ 3 | entre sin relación, k = 2 / k ≥ 3 | entre estrictos, k ≥ 3 |
|---|---|---|---|
| Urton | 52 / 95 (sin UR053: 35 / 23) | 67 / 14 | 13 |
| Ascher | 2 / 1 | 5 / 21 | 1 |
| Clindaniel | 0 / 0 | 0 / 0 | 0 |

- **Solo hay n para Urton.**
- **Ascher no tiene pares dentro de archivo.** Casi todos sus quipus son de procedencia desconocida, así que caen en la clase «otro».
- Clindaniel no tiene ningún par.

## Veredicto

| afirmación | nivel |
|---|---|
| No hay clave de color compartida entre archivos sin relación, con el transcriptor fijo | **se mantiene** (negativo con potencia ≥ 0,9 en Urton y Ascher para k ≥ 3) |
| «Mismo reparto dentro del archivo ≫ entre archivos» con el investigador fijo | **se mantiene** (MH OR 5,5; Urton p = 0,0007 y 0,037) |
| … sin UR053A–E | **se debilita** a dirección no significativa (22 % frente a 0 %, p = 0,135). La firma de clave local la sostiene sobre todo un archivo |
| Ascher y Clindaniel | **sin potencia** dentro de archivo |
