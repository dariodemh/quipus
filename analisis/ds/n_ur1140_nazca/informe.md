# UR1140 (Berlín, Nazca): ficha de 7 campos

**Autor:** equipo `n_ur1140_nazca` · **Semilla:** 20261018 · **Fecha:** 2026-10-18
**Datos:** `analisis/datos/cuerdas.csv`, `analisis/datos/quipus.csv`; OKR `khipu.db` en modo lectura.
**Scripts:** `analisis.py`, `analisis_ficha9.py`, `analisis_tipos.py`, `analisis_canonico.py`, `comparar_candidatos.py`, `ficha_final.py`.
**Salidas:** `ficha7.csv`, `ficha7_canonica.csv`, `resumen_pruebas.csv`, `resultados_*.csv`.

---

## 1. Pregunta

1. ¿Se reproduce de forma independiente el hallazgo de `n_plantillas` en UR1140: 15 bandas de color × 7 cuerdas, con la posición dentro de la banda ordenando los valores (η² ≈ 0,42; Holm 0,005)?
2. Congelada la ficha de 7 campos de UR1140, ¿qué quipus de Nazca, Berlín y del Santa tienen el mismo número de campos y el mismo perfil?
3. Si hay ≥2, ¿son copias o sumas entre sí?
4. En el Santa cada banda es una persona y cada posición un rubro. ¿Qué serían los 7 campos de UR1140?

La hipótesis a batir es la más aburrida: que el «7» sea un artefacto de cómo se cortan las bandas de color, y que el parecido entre quipus se reduzca a un rasgo genérico (por ejemplo, «la primera cuerda es grande»).

---

## 2. Método

### 2.1 Datos y definiciones

- Una fila por cuerda; se eliminan duplicados `(kfg, cuerda)` como en `n_plantillas`.
- `valor` solo si `nudos` no está vacío; un 0 con `nudos` vacío es cuerda ausente, no cero (regla del BRIEF).
- Se trabaja con cuerdas de nivel 0 (colgantes), ordenadas por `orden`.
- Color: se quitan los rangos en cm con `re.sub(r'\([^)]*\)', '', s)`.
- **Definición A (la de `n_plantillas`):** bandas = rachas maximales de color idéntico; largo modal de racha en [4,12] = 7; se conservan las rachas de largo 7. En UR1140 salen 15.
- **Definición B (unidad física):** grupos de espaciado (`grupo`) de 9 cuerdas, confirmados en OKR como 20 clusters de exactamente 9 cuerdas. Dentro de cada grupo, 7 cuerdas del color modal + 2 cuerdas marcadoras de otro color (B:BB, B:G, etc.). En UR1140 hay 20 grupos; 19 con 7 cuerdas B utilizables.
- **Canonicalización:** si la segunda cuerda marcadora está en posición ≥5, se invierte el orden de las 7 cuerdas. Así el campo 1 queda siempre en el borde del registro adyacente al par marcador. Esta regla usa solo la posición de las marcadoras, no los valores.

### 2.2 Estadísticos

- **η² de posición:** proporción de varianza de `log10(valor+1)` explicada por la posición dentro de la banda/grupo. Es el estadístico de `n_plantillas` (0,42).
- **ρ̄ (concordancia de orden):** Spearman medio por pares de bandas, sobre los perfiles de valores por posición. Mide si las bandas comparten el *orden* de los valores, no solo el nivel.
- **Perfil congelado:** media por posición de los z-scores de `log10(valor+1)` dentro de cada banda. Es la «ficha» que se aplica a otros quipus.
- **Nulo:** permutación de los valores *dentro de cada banda* (preserva el multiconjunto de valores de cada registro y destruye la asignación posición-valor). B = 9 999; p empírico = (1 + #{nulo ≥ observado}) / (1 + B).
- **Corrección múltiple:** Holm y BH-FDR. Se reportan dos familias: (a) los quipus con 7 campos testables; (b) todos los quipus probados (169 en Nazca/Berlín/Santa; 651 en el corpus para la validación externa), asignando p = 1 a los no testables. La segunda es la conservadora.
- **Niveles:** demostrado / apoyado con datos / propuesto / especulativo.

### 2.3 Universo

- **Nazca:** 16 quipus (`procedencia` contiene «Nazca»).
- **Berlín:** 153 quipus (`museo` contiene «Berlin»).
- **Santa:** 6 quipus (UR087–UR092, `procedencia` = «Santa»).
- Unión: **169 quipus** (hay solapamientos Nazca/Berlín).
- Corpus completo para validación externa: 651 quipus.

---

## 3. Resultados

### 3.1 Reproducción de `n_plantillas`: el número sale, pero la banda no es el registro

UR1140 tiene **190 cuerdas** (180 de nivel 0, 10 subsidiarias). Con la definición A salen exactamente **15 rachas de 7 cuerdas**. El estadístico reproduce el publicado:

| Prueba (UR1140, 15 rachas de 7) | Valor | p (permutación) |
|---|---:|---:|
| η² de posición | **0,4236** | — |
| ρ̄ Spearman medio por pares | **0,412** | **0,0001** |

El η² coincide con el 0,42 de `n_plantillas`. La reproducción es exacta. (`n_plantillas` reporta Holm 0,005 dentro de su propia familia de pruebas; aquí el p bruto por permutación es 0,0001.)

**Pero las 15 rachas no están alineadas como registros.** Una racha de color es una unidad legítima (así se definen los grupos de 6 del Santa). El problema es que en UR1140 las 15 rachas cruzan un grupo de espaciado: cada racha está formada por las 2 cuerdas B del final de un grupo de 9 y las 5 cuerdas B del principio del grupo siguiente (o al revés). Unas son 2+5 y otras 5+2, de modo que las posiciones 1–7 no son los mismos campos en todas las bandas. OKR confirma que UR1140 tiene **20 clusters de exactamente 9 cuerdas**; el grupo de 9 es la unidad que alinea los 7 campos.

Consecuencia: la racha de 7 tiene dos fases, y cada fase tiene un perfil distinto:

| Fase | n | Perfil medio (valores crudos por posición) | ρ̄ interno |
|---|---:|---|---:|
| t = 2 (2 cuerdas del grupo anterior + 5 del siguiente) | 6 | [5,2; 91,5; 21,3; 21,7; 18,8; 29,3; 18,7] | 0,630 |
| t = 5 (5 cuerdas del grupo anterior + 2 del siguiente) | 9 | [18,6; 20,7; 10,7; 31,2; 15,8; 53,0; 6,1] | 0,667 |

La correlación media **entre** fases es solo **0,181**. El perfil agregado de 15 rachas es una mezcla de dos perfiles; el η² = 0,42 no es la magnitud limpia del formulario. Con la unidad física sin orientar baja a **η² = 0,274** (ρ̄ = 0,255; p = 0,0001); con la orientación canónica (§3.2) sube a **0,646**. Es decir: hay un efecto posicional real, pero el «0,42» es el resultado de una segmentación que mezcla dos órdenes.

**Nivel:** *demostrado* que las 15 rachas cruzan los grupos de 9 y que el perfil depende de la fase; *demostrado* que η² baja de 0,424 a 0,274 al usar el registro físico sin orientar (y sube a 0,646 al orientarlo).

### 3.2 La ficha física: 20 registros de 9 cuerdas, 7 campos + 2 marcadoras

Cada grupo de 9 de UR1140 tiene la forma (salvo el grupo 0, que tiene 6 B + 2 marcadoras + 1 BB):

```
[7 cuerdas B] + [2 cuerdas marcadoras]   (las marcadoras en posiciones 3-4, 6-7 o, una vez, 2-6)
```

Las 2 marcadoras no son ruido: su posición divide los registros en dos tipos y cambia el perfil. En UR1140:

| Tipo (posiciones de las marcadoras) | n | Perfil de las 7 cuerdas (z) | η² |
|---|---:|---|---:|
| (3,4) | 10 | [1,77; −1,37; 0,03; 0,27; −0,73; 0,42; −0,38] | **0,638** |
| (6,7) | 8 | [−0,02; −0,03; −0,11; 0,18; −0,31; −1,56; **1,85**] | **0,742** |
| (2,6) | 1 | [0,54; 0,03; 0,03; −0,80; −0,29; −1,46; 1,96] | — |

Los dos perfiles son **el mismo leído al revés**: al invertir el tipo (3,4), su correlación con el tipo (6,7) es **r = 0,926**. Por eso la canonicalización (invertir si la segunda marcadora está en posición ≥5) es la operación correcta.

Con los 19 registros canónicos de UR1140:

| Prueba (UR1140, 7 campos canónicos) | Valor |
|---|---:|
| η² de posición | **0,646** |
| ρ̄ Spearman | **0,666** (p = 0,0001) |
| Perfil canónico (z) | [**1,81**; −1,46; −0,13; 0,17; −0,43; 0,21; −0,18] |
| Media cruda por campo | [**74,9**; 6,7; 18,0; 22,4; 15,1; 26,1; 18,9] |
| Máximo en el campo 1 | **19/19** |

El campo 1 es, con mucho, el mayor (media 75; rango 28–114); el campo 2 es el menor (media 6,7; rango 2–22); los campos 3–7 son intermedios (15–26). El η² canónico (0,646) es **mayor** que el de la racha de 7 (0,424): al quitar las 2 marcadoras y orientar el registro, el efecto posicional se vuelve más nítido.

La misma estructura aparece en los otros quipus del formato. Por tipo de marcadora, contra el perfil del tipo correspondiente de UR1140: UR1136 (3,4) r = 0,905 (p = 0,0024); UR1136 (6,7) r = 0,975 (p = 0,0002); UR223 (3,4) r = 0,871 (p = 0,0073). Holm sobre las 3 pruebas de tipo da 0,0048, 0,0006 y 0,0073. Es la evidencia mecanística de que la canonicalización no es un ajuste ad hoc: el mismo par de sub-fichas aparece en otro quipu. La corrección más dura (338 pruebas quipu × tipo) deja solo el tipo (6,7) al borde (Holm ≈ 0,068).

**Nivel:** *apoyado con datos* que el registro físico es el grupo de 9 y que hay un campo 1 tipo «total» y un campo 2 tipo «residual»; *propuesto* que las 2 marcadoras indiquen la orientación/el tipo de registro.

### 3.3 Aplicación a Nazca, Berlín y Santa

#### (a) Definición A (15 rachas de 7), ficha congelada de UR1140

De los 169 quipus, **13 tienen rachas modales de 7** y **7 tienen ≥2 bandas completas** para testear. Resultados con la ficha congelada (perfil de las 15 rachas):

| Quipu | n bandas | η² | ρ̄ | r con ficha | p | Holm (12 testables) | Holm (169 probados) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **UR1136** | 13 | 0,371 | 0,369 | **0,871** | **0,0055** | **0,0385** | 0,924 |
| UR223 | 8 | 0,896 | 0,831 | 0,813 | 0,0162 | 0,0972 | 1,000 |
| UR1166 | 16 | 0,389 | — | 0,631 | 0,0609 | 0,305 | 1,000 |
| UR238 | 2 | 0,565 | — | 0,598 | 0,0701 | 0,305 | 1,000 |
| UR1121 | 2 | 1,000 | — | 0,475 | 0,129 | 0,387 | 1,000 |
| UR211 | 8 | 0,304 | 0,446 | −0,244 | 0,702 | 1,000 | 1,000 |
| UR1145 | 4 | 0,061 | −0,117 | −0,251 | 0,707 | 1,000 | 1,000 |

Solo **UR1136** sobrevive Holm si se corrige por los 12 quipus con 7 campos; **ninguno** sobrevive si se corrige por los 169 quipus probados. UR223 es marginal (p = 0,016) y no sobrevive Holm en ninguna de las dos familias.

#### (b) Definición B (grupos de 9, 7 campos), ficha congelada de UR1140

En los 169 quipus, solo **3** tienen ≥3 grupos de 9 con 7 cuerdas del color modal y registros completos: UR1140 (19), UR1136 (14) y UR223 (7). Las correlaciones con el perfil de UR1140 son:

| Quipu | n | r con ficha (7 campos) | p | Holm (21 con grupos de 9) | Holm (169) |
|---|---:|---:|---:|---:|---:|
| **UR1136** | 14 | **0,888** | **0,0041** | 0,082 (Holm 21) / BH 0,043 | 0,689 |
| UR223 | 7 | 0,562 | 0,096 | 1,000 | 1,000 |

#### (c) Validación externa: todo el corpus

Al barrer los 651 quipus aparecen **5** con ≥3 grupos de 9 y 7 cuerdas del color modal:

| Quipu | Grupos con 7 campos | Registros completos | Tipos de marcadoras | Museo / procedencia |
|---|---:|---:|---|---|
| **UR1140** | 19 | 19 | (3,4) 10, (6,7) 8, (2,6) 1 | Berlín / Nazca |
| **UR1136** | 15 | 14 | (3,4) 10, (6,7) 5 | Berlín / Nazca (VA16635) |
| **UR223** | 8 | 7 | (3,4) 8 | Berlín / Ica (VA47077) |
| **HP056** | 5 | 5 | (6,7) 5 | Museo Nacional / desconocida |
| **UR1176** | 6 | 0 | (1,9) 6 | Berlín / Nazca |

UR1140 y UR1136 tienen **números de museo consecutivos** (VA16636 y VA16635), la misma procedencia (Nazca) y el mismo formato de 20 grupos de 9. UR1176 tiene 7 ranuras DB entre dos cuerdas RB, pero la primera DB está vacía en todos los registros: **0 registros completos de 7 campos** (en la práctica son 6 campos numéricos).

Con la ficha canónica de UR1140:

| Quipu | n | r (7 campos) | p | Holm (5) | Holm (651) | r campos 3–7 | p campos 3–7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **UR1136** | 14 | **0,960** | **0,0003** | **0,0009** | 0,195 | **−0,319** | 0,697 |
| UR223 | 7 | 0,883 | 0,0057 | 0,0114 | 1,000 | 0,561 | 0,164 |
| HP056 | 5 | 0,796 | 0,0186 | 0,0186 | 1,000 | 0,302 | 0,309 |
| UR1176 | 0 | — | — | — | — | — | — |

**La correlación alta es engañosa si se mira el perfil completo.** Entre UR1140 y UR1136, r = 0,960 para los 7 campos, pero **r = −0,319 para los campos 3–7**. La correlación total está dominada por los campos 1–2 (el «encabezado»): campo 1 grande, campo 2 pequeño. Los cinco campos restantes **no comparten perfil** entre UR1140 y UR1136. En UR223 y HP056 los campos 3–7 sí se parecen entre sí (r = 0,887), pero no a los de UR1140; podría ser un subtipo, no una ficha común.

#### (d) La regla robusta: el máximo está en el campo 1 canónico

En los 45 registros completos de los 4 quipus con registros utilizables:

| Quipu | n | Máximo en campo 1 | Perfil canónico (z) | η² canónico |
|---|---:|---:|---|---:|
| UR1140 | 19 | **19/19** | [1,81; −1,46; −0,13; 0,17; −0,43; 0,21; −0,18] | 0,646 |
| UR1136 | 14 | **13/14** | [1,73; −1,49; −0,10; −0,01; 0,14; −0,06; −0,20] | 0,532 |
| UR223 | 7 | **7/7** | [2,23; −0,73; −0,48; 0,25; −0,27; −0,10; −0,91] | 0,931 |
| HP056 | 5 | **5/5** | [1,87; −0,39; −0,32; −0,02; −0,06; −0,02; −1,06] | 0,443 |
| **Total** | **45** | **44/45 (97,8 %)** | — | — |

- Nulo de permutación dentro de cada registro: p < 0,0001 (mínimo alcanzable con B = 9 999).
- Binomial ingenuo (máximo uniforme entre 7 campos): p = 2,5·10⁻³⁶; **no es válido** por clustering (45 registros en 4 quipus).
- Prueba cluster-robust: los 4 quipus tienen su máximo modal en el campo 1; bajo la nula, (1/7)⁴ ≈ 4,2·10⁻⁴.
- La única excepción es un registro de UR1136 (tipo 6,7) con el máximo en el campo 2.

**Nivel:** *apoyado con datos* (rayano en demostrado) que el campo 1 canónico es el valor principal del registro, y que el par de marcadoras define la orientación. *No* está apoyado que los 7 campos tengan un perfil completo compartido.

### 3.4 ¿Copias o sumas?

UR1140 y UR1136 son los dos candidatos con el mismo formato y el mismo encabezado. No son copias ni sumas:

| Comparación | UR1140 | UR1136 |
|---|---:|---:|
| Cuerdas de nivel 0 | 180 | 181 |
| Grupos de 9 | 20 | 20 (+1 cuerda suelta) |
| Cuerdas numéricas | 180 | 162 |
| Suma de valores | 4 238 | 5 258 |
| Media | 23,5 | 32,5 |
| Máximo | 114 | 180 |
| Celdas idénticas (7 campos alineados) | — | **1–2 %** |
| Correlación de sumas por grupo | — | **−0,546** |
| Grupos exactamente iguales | — | **0/18** |
| Grupos de B = suma exacta de dos grupos de A | — | 5/18 (esperable por azar con enteros pequeños) |
| Razón de totales B/A | — | 1,241 (no constante) |

Además, los números de museo son **consecutivos** (VA16635/VA16636), la procedencia es la misma (Nazca) y el formato es idéntico: lo más económico es que sean **dos registros independientes del mismo formulario/archivo**, no una copia ni una suma.

UR223 (Ica, VA47077; 80 cuerdas, 71 numéricas, suma 1.667, 8 registros) es una versión más corta y de otra procedencia; no es copia ni suma de UR1140/UR1136. UR1176 es un formato de 7 ranuras DB entre dos RB, pero sin 7 campos numéricos completos; no es comparable.

**Nivel:** *demostrado* que no son copias (celdas idénticas 1–2 %, sumas por grupo no correlacionadas); *propuesto* que sean dos registros del mismo archivo, con el apoyo externo de los números de museo consecutivos.

### 3.5 Control positivo: el Santa

El test detecta formularios reales. En los 6 quipus del Santa, con bandas de 6 (no de 7):

| Quipu | L | n bandas | η² | ρ̄ | p |
|---|---:|---:|---:|---:|---:|
| UR087 | 6 | 43 | 0,686 | 0,553 | 0,0005 |
| UR088 | 6 | 6 | 0,983 | 0,860 | 0,0005 |
| UR089 | 6 | 31 | 0,821 | 0,593 | 0,0005 |
| UR090 | 6 | 13 | 0,711 | 0,783 | 0,0005 |
| UR091 | 6 | 15 | 0,635 | 0,488 | 0,0005 |
| UR092 | 6 | 10 | 0,483 | — | — |

5/6 son significativos con p ≤ 0,0005. El perfil del Santa es muy estable en 5/6: **posición 4 máxima, posición 1 mínima** (p. ej. UR087: [1,2; 3,1; 1,9; 12,5; 1,5; 1,5]); UR092 es la excepción (máximo en la posición 2). Es un formulario real, y el test lo ve.

Pero el Santa tiene **6 campos, no 7**, y su perfil es **distinto**: en el Santa el máximo está en la posición 4 y el mínimo en la 1; en UR1140 el máximo está en la 1 canónica y el mínimo en la 2. La analogía «cada banda = persona, cada posición = rubro» es formalmente plausible, pero **no se puede transferir el significado de los campos del Santa a UR1140**.

**Nivel:** *demostrado* que el test tiene potencia (Santa); *demostrado* que el Santa no es la misma ficha que UR1140 (6 vs 7 campos y perfiles distintos).

---

## 4. Controles

1. **Nulo explícito:** permutación dentro de cada banda/registro, que preserva el multiconjunto de valores de cada registro. Todos los p son empíricos con B = 9 999 (B = 1 999 en el control Santa por costo).
2. **Corrección múltiple:** Holm y BH sobre (a) los quipus testables y (b) los 169 quipus probados; para la validación externa, Holm sobre los 651 del corpus. Se reportan ambas; la conclusión principal no depende de la familia menos conservadora.
3. **Control de unidad física:** OKR confirma 20 clusters de 9 cuerdas en UR1140; las 15 rachas de 7 cruzan clusters. El η² baja de 0,424 a 0,274 al usar el cluster.
4. **Control de fase:** los perfiles de las fases t = 2 y t = 5 son distintos (r entre fases = 0,181); el perfil agregado es una mezcla.
5. **Control de las marcadoras:** al excluir las 2 cuerdas marcadoras, el η² sube de 0,104 (9 posiciones) a 0,274 (7 campos) y a 0,646 (7 campos canónicos). Las marcadoras no son ruido: codifican orientación/tipo.
6. **Control de los campos 3–7:** la correlación total UR1140–UR1136 (0,960) se descompone en campos 1–2 (idénticos por construcción) y campos 3–7 (r = −0,319, p = 0,697). El «perfil de 7 campos» no está soportado más allá del encabezado.
7. **Control positivo Santa:** 5/6 significativos; el test no es ciego.
8. **Control de copias:** celdas idénticas 1–2 %, sumas por grupo no correlacionadas, ningún grupo exactamente igual.
9. **Chequeo de la explicación aburrida:** la primera explicación (rachas de color) explica el 0,42 pero no la estructura física; la segunda (grupos de 9 + marcadoras) explica el 0,646 y el 44/45. La segunda es más simple y más predictiva.
10. **Confusión color-tipo en UR1136 y UR223:** en UR1136 el tipo (3,4) son cuerdas W y el (6,7) son cuerdas G; en UR223 el tipo (3,4) es MB. Color y tipo están confundidos. En UR1140 ambos tipos son B, así que allí la comparación de tipos es limpia. La coincidencia UR1140–UR1136 se da entre B (3,4) y W (3,4), y entre B (6,7) y G (6,7): el perfil posicional parece invariante al color, pero el color no se puede descartar como explicación alternativa.

---

## 5. Resultados negativos

- **No hay un quipu fuera de UR1140 con el perfil completo de 7 campos que sobreviva a la corrección por los 169 (o 651) quipus probados.** UR1136 es el único candidato cercano: r = 0,960 y p = 0,0003, pero Holm 651 = 0,195; y sus campos 3–7 no correlacionan con los de UR1140 (r = −0,319).
- **La ficha de 15 rachas × 7 no está alineada con la unidad física.** Las 15 rachas cruzan grupos de 9; el η² = 0,42 es una mezcla de dos fases. El efecto con la unidad física es η² = 0,274 (sin orientar) o 0,646 (canónico).
- **El Santa no tiene la misma ficha:** 6 campos, no 7; máximo en la posición 4, no en la 1; perfil distinto. La analogía con el padrón del Santa es estructural, no semántica.
- **No hay copias ni sumas** entre UR1140 y UR1136 (1–2 % de celdas idénticas; sumas por grupo con r = −0,546; 0/18 grupos iguales; razón de totales 1,241 no constante).
- **UR223 y HP056** se parecen a UR1140 en el encabezado (campo 1 máximo) pero no en los campos 3–7; sus perfiles completos no sobreviven la corrección por 651 (Holm = 1,0).
- **UR1176** tiene 7 ranuras DB entre dos RB, pero la primera DB está vacía en todos los registros: 0 registros completos de 7 campos; no se puede usar como confirmación.
- **La posición 2 como mínimo no es universal:** 17/19 en UR1140, 11/14 en UR1136, pero solo 3/7 en UR223 y 2/5 en HP056. El «campo 2 pequeño» es un rasgo de los dos quipus grandes, no de toda la familia.

---

## 6. Interpretación: ¿qué serían los 7 campos?

### 6.1 Lo que los datos sostienen

1. **Campo 1 = valor principal / total.** Es el máximo en 44/45 registros (97,8 %), con media 75 en UR1140 (rango 28–114) y valores mucho mayores que los demás. La canonicalización por el par marcador lo pone siempre en primer lugar. Es el mejor candidato a «total del registro».
2. **Campo 2 = residual / cantidad pequeña.** Media 6,7 en UR1140; es el mínimo en 17/19 registros de UR1140 y 11/14 de UR1136. Podría ser un resto, una tasa o una cantidad menor, pero no se puede identificar.
3. **Campos 3–7 = categorías variables.** Medias 15–26, sin perfil compartido entre quipus. Podrían ser rubros (personas, animales, productos, edades), pero **no hay evidencia** para asignarles nombres.
4. **Las 2 marcadoras = atributo binario / orientación.** Su posición (3,4) vs (6,7) divide los registros en dos tipos con perfiles invertidos (r = 0,926 al invertir uno). La función es análoga a la unión R/V del Santa (atributo binario, probablemente moiety o tipo), pero **el significado es especulativo**. No hay variación de `union` en UR1140: las 180 cuerdas son U; el atributo binario está en el color/posición de las marcadoras, no en la unión.

### 6.2 Lo que no se sostiene

- **No es un padrón del Santa de 6 campos.** El Santa tiene 6 cuerdas por tributario, con la posición 1 = tributo (0–13), la posición 4 = máximo, unión R/V = mitad y color = nombre. UR1140 tiene 7 campos, máximo en la posición 1 canónica, sin variación de unión y sin variación de color en las 7 cuerdas (todas B). La analogía «15 personas × 7 rubros» es una posibilidad, pero no está demostrada y el perfil no coincide.
- **No hay un «formulario de 7 campos» completo compartido.** Lo compartido es el formato (9 cuerdas: 7 + 2 marcadoras), la orientación y el encabezado (campo 1 máximo). Los campos 3–7 no se replican.

### 6.3 Lectura propuesta (especulativa)

UR1140 y UR1136 serían **dos registros independientes del mismo tipo de formulario administrativo**, procedentes de la misma adquisición (Nazca, Berlín, VA16635/VA16636). Cada registro tendría:
- un **total** (campo 1),
- un **residual/tasa** (campo 2),
- **5 categorías** variables (campos 3–7),
- y **2 marcadoras de color** que indican la orientación o una dicotomía (¿mitad hanan/hurin? ¿tipo de registro? ¿sentido de lectura?).

UR223 (Ica) y HP056 (procedencia desconocida) comparten el formato y el encabezado, lo que sugiere una convención más amplia que un solo archivo local. UR1176 sería una variante con las marcadoras en los extremos (RB … RB) y un campo vacío.

Una lectura alternativa que los datos no descartan: el grupo de 9 podría contener **dos sub-registros** separados por las 2 marcadoras (5+2 o 2+5), y no un solo registro de 7 campos. La regla del máximo en el campo 1 canónico favorece la lectura de un registro único orientado, pero no la demuestra.

**Nivel:** *apoyado con datos* para el formato y el encabezado; *propuesto* para «total + residual + 5 categorías»; *especulativo* para la identidad de las categorías y para la dicotomía de las marcadoras.

---

## 7. Nivel de evidencia (resumen)

| Afirmación | Nivel |
|---|---|
| UR1140 tiene 20 grupos de 9 cuerdas; las 15 rachas de 7 cruzan grupos | **Demostrado** |
| El η² = 0,42 de `n_plantillas` se reproduce, pero baja a 0,274 con la unidad física | **Demostrado** |
| Hay dos perfiles de fase (t=2 y t=5); el agregado es una mezcla | **Demostrado** |
| El registro físico es 9 cuerdas = 7 campos + 2 marcadoras | **Apoyado con datos** |
| El campo 1 canónico es el máximo en 44/45 registros de 4 quipus | **Apoyado con datos** (cluster-robust p ≈ 4·10⁻⁴) |
| El par marcador define la orientación (invertir alinea los perfiles, r = 0,926) | **Apoyado con datos** |
| UR1140 y UR1136 comparten formato y encabezado; no son copias ni sumas | **Apoyado con datos** |
| UR1140 y UR1136 son dos registros del mismo archivo (museo consecutivo) | **Propuesto** |
| Los 7 campos tienen un perfil completo compartido | **No apoyado / negativo** (campos 3–7: r = −0,319) |
| Campo 1 = total, campo 2 = residual, campos 3–7 = categorías | **Propuesto / especulativo** |
| Las marcadoras codifican moiety o tipo | **Especulativo** |
| UR1140 es un padrón de personas como el Santa | **No apoyado** (6 vs 7 campos; perfiles distintos) |

---

## 8. Para el coordinador

- **El hallazgo de `n_plantillas` se reproduce exactamente** (η² = 0,424; ρ̄ = 0,412; p = 10⁻⁴), pero **las 15 «bandas» de 7 no están alineadas como registros**: las 15 cruzan los 20 grupos de 9 cuerdas que confirma OKR y mezclan dos órdenes internos. El 0,42 es una mezcla de dos fases; con la unidad física el η² es 0,274.
- **La unidad real es 9 cuerdas = 7 campos + 2 marcadoras.** Al excluir las marcadoras y orientar el registro, el η² sube a **0,646**. El «7» es real, pero no como racha de color.
- **La regla robusta:** en **44/45 registros (97,8 %) de 4 quipus** (UR1140, UR1136, UR223, HP056), el **campo 1 canónico es el máximo**. La orientación la define la posición del par de marcadoras: si la segunda marcadora está en posición ≥5, se invierte el orden. Nulo por permutación p < 10⁻⁴; cluster-robust (4/4 quipus) p ≈ 4·10⁻⁴.
- **Solo 5 quipus del corpus de 651 tienen ≥3 grupos de 9 con 7 campos:** UR1140, UR1136, UR223, HP056 y UR1176 (este último sin 7 campos numéricos completos). El formato es raro, no genérico.
- **UR1136 es el mejor candidato a «misma ficha»:** 20 grupos de 9, 14 registros completos, r = 0,960 con UR1140, y **números de museo consecutivos** (VA16635/VA16636, ambos Nazca/Berlín). No es copia ni suma (1–2 % de celdas idénticas; sumas por grupo r = −0,546; 0/18 grupos iguales).
- **Pero el perfil completo de 7 campos no se sostiene:** la correlación 0,960 está dominada por los campos 1–2; los campos 3–7 tienen r = −0,319 (p = 0,697). Lo compartido es el **formato + encabezado**, no una plantilla semántica de 7 rubros.
- **Corrección múltiple:** UR1136 sobrevive Holm si se corrige por los 12 quipus con 7 campos (0,039, ficha de 15 rachas) o por los 5 del formato (0,0009, ficha canónica), pero **no** si se corrige por los 169 (0,924) o los 651 (0,195). UR223 y HP056 no sobreviven la corrección conservadora. Por eso: *apoyado con datos* para el formato/encabezado, *propuesto* para la ficha completa.
- **El Santa es control positivo, no la clave:** 5/6 quipus dan p ≤ 0,0005 con 6 campos (máximo en posición 4, mínimo en 1). UR1140 tiene 7 campos y máximo en 1; **no es el mismo formulario**. La analogía «persona × rubro» es sugerente pero no transferible.
- **Próxima ronda:** (1) probar la regla «campo 1 = máximo» en los 5 quipus del formato y en nuevos quipus de 9 cuerdas; (2) buscar el significado de las 2 marcadoras (¿moiety? ¿dirección? ¿tipo?) con un documento colonial o con el archivo de Berlín; (3) ver si los campos 3–7 se permutan entre quipus (un alineamiento de 5! = 120 permutaciones, con corrección); (4) revisar UR1176 como variante de marcadoras en los extremos; (5) no usar la ficha de 15 rachas como unidad de análisis en futuros tests.

---

## 9. Archivos

- `ficha7.csv` — ficha canónica de UR1140: perfil z, media, mediana, sub-fichas (3,4) y (6,7), y qué posiciones se comparten con UR1136.
- `ficha7_canonica.csv` — perfil canónico y perfil de campos 3–7.
- `resumen_pruebas.csv` — tabla corta de las pruebas clave.
- `resultados_quipus.csv` — los 169 quipus con L, η², ρ̄, r con la ficha de 15 rachas, p y correcciones.
- `resultados_ficha9.csv` — los 169 con grupos de 9, 7 campos y perfil.
- `resultados_tipos.csv` — tests por tipo de marcadora.
- `resultados_canonico.csv` — los 5 quipus del formato, perfil canónico, campos 3–7 y correcciones.
- `resultados_santa.csv` — control positivo del Santa.
- Scripts: `analisis.py`, `analisis_ficha9.py`, `analisis_tipos.py`, `analisis_canonico.py`, `comparar_candidatos.py`, `ficha_final.py`.
