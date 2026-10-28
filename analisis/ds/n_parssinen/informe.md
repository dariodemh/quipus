# Las 9 columnas de UR278 frente a las listas coloniales de Pärssinen

**Equipo:** DeepSeek · carpeta `analisis/ds/n_parssinen/`
**Fecha:** 18 de octubre de 2026
**Semilla:** 20261018 (todo reproducible)
**Datos:** `analisis/fuentes_txt/Parssinen1992_Tawantinsuyu.txt`, `Parssinen2004_TextosAndinos_parcial.txt`, `Curatola2013_ContarConcertando.txt`, `Rostworowski_CostaPeruana.txt`; `analisis/13_sistema_incahuasi/ur278_tabla.csv`; `analisis/ds/n_nueve_unidades/` (firma y emparejamientos previos).
**Scripts:** `01_listas.py` (extracción y codificación), `02_analisis.py` (estadísticos y controles).
**Salidas:** `listas.csv` (165 filas, 20 listas), `resultados.csv`, `controles.csv`, `salida_02.txt`.

---

## 1. Pregunta

¿A qué tipo de lista colonial de unidades se parecen las 9 columnas de UR278? La firma que se quiere explicar es:

- 9 columnas con un perfil estable de tamaño desigual, ordenadas aproximadamente de mayor a menor (Spearman del perfil con la posición = **−0,73**, p = 0,025);
- proporciones c1..c9 ≈ 0,135 0,140 0,097 0,107 0,116 0,129 0,107 0,080 0,089;
- un par fuerte (c1,c2) y un mejor emparejamiento (1-2)(3-6)(4-9)(5-7) + c8 suelta (p = 0,002 frente a los 945 emparejamientos de 8+1).

La pregunta concreta es si alguna lista colonial transcrita de un quipu —censos decimales, sayas, guarangas, pachacas, ayllus, tributarios por parcialidad— reproduce (a) el número 9, (b) la planitud del perfil y (c) el orden de mayor a menor, o si por el contrario las listas coloniales se ordenan por jerarquía/geografía y son mucho más desiguales.

---

## 2. Método

### 2.1 Corpus de listas

Se transcribieron **20 listas** de las tablas y pasajes de Pärssinen 1992, Pärssinen & Kiviharju 2004 y Rostworowski. Cada lista se codificó en el **orden en que aparece en la fuente** (no se reordenó por tamaño), con una fila por unidad en `listas.csv`. Se marcaron como incompletas las listas con cifras faltantes.

| lista | fuente y línea | región | nivel | n | estructura |
|---|---|---|---|---|---|
| `caj_bambamarca_1567` | Pärssinen 1992, Table 2, 6316-6343 | Cajamarca | pachaca de la guaranga Bambamarca | 9 | 9 pachacas; cacique principal primero |
| `caj_chondal_1567` | ídem, 6325-6330 | Cajamarca | pachaca de Chondal (Hanansaya) | 4 | 4 pachacas |
| `caj_pomamarca_1567` | ídem, 6344-6365 | Cajamarca | pachaca de Pomamarca (Hurinsaya) | 8 (6 con cifra) | 8 pachacas, incompleta |
| `cusco_coco_1535` | Table 4, 6483-6505 | Cuzco/Limatambo | aldea/llacta del curacazgo Coco | 9 | 9 aldeas, 7 principales |
| `aullaga_acho_1540` | Table 7, 6859-6875 | Aullaga/Quillaca | aldea/llacta de la parcialidad Aullaga | 11 | 11 aldeas |
| `lupaca_sayas_1567` | cuadro de Julien, 6058-6070 | Lupaca/Chucuito | saya (mitad de cabecera) | 12 | 7 cabeceras × 2 sayas (Ilave y Yunguyo combinadas); Alasaya antes que Maasaya |
| `lupaca_cabeceras_1567` | derivado de la anterior, 5835-5837 | Lupaca/Chucuito | cabecera | 7 | 7 cabeceras; Chucuito capital primero |
| `chayanta_1540` | Pärssinen & Kiviharju 2004, 505-520 | Chayanta (Charcas) | pueblo/estancia | 12 | título a Gonzalo Pizarro; orden de quipu |
| `chayanta_1548` | ídem, 505-520 | Chayanta | pueblo/estancia | 12 | segunda transcripción del mismo quipu |
| `yanque_collagua_1540` | Table 9, 7125-7145 | Collaguas | aldea/llacta de Yanque | 16 | Hanansaya + Hurinsaya |
| `cavana_conde_1540` | Table 8, 7020-7055 | Collaguas | aldea/llacta de Cavana | 18 | Hanansaya + Hurinsaya |
| `guancayo_lords_1571` | Rostworowski 2601; Pärssinen 6285 | Chillón | señor (pachacas por señor) | 5 | 9 pachacas = 1+4×2 |
| `guancayo_pachacas_ideal` | reconstrucción decimal | Chillón | pachaca | 9 | 9 × 100 = 900 (modelo, no lista observada) |
| `caj_7guarangas` | Pärssinen 4752 | Cajamarca | guaranga | 7 | 4 Hanansaya + 3 Hurinsaya; sin cifras completas |
| `huayla_12guarangas` | Pärssinen 4696, 5523 | Huayla | guaranga | 12 | 6 Hanan + 6 Hurin; sin cifras completas |
| `pacajes_cabeceras_1543` | Pärssinen 2559 | Pacajes | cabecera | 3 | 3 cabeceras |
| `collaguas_subprovinces_1540` | Pärssinen, nota 234, 4699 | Collaguas | subprovincia | 3 | 3 subprovincias (Lari estimado) |
| `huanca_hunus` | Pärssinen 5523 | Huanca/Jauja | hunu | 3 | 3 hunus |
| `chincha_hunus` | Pärssinen 2522, 4584 | Chincha | hunu | 3 | 3 hunus |
| `chachapoya_hunus` | Pärssinen 5232 | Chachapoya | hunu | 2 | 2 hunus |

La lista de **Bambamarca** es la única lista de 9 pachacas con cifras completas que encontramos en las tablas revisadas de Pärssinen. La de **Coco** es la única lista de 9 aldeas con cifras completas. La de **Aullaga** es la única de 11. Las de Yanque (16) y Cavana (18) son listas de aldeas, no de unidades decimales; se usan como control de "lista de asentamientos".

**Vacíos del corpus:** no encontramos listas de **ayllus** con cifras individuales. Los ayllus/hathas de Lupaca aparecen solo como conteos ideales (17 hathas) frente a los reales (13 en Maasaya, 11 en Alasaya), sin cifras por unidad (Pärssinen 6088). Tampoco hay una lista completa de pachacas de **Chupaychu/Huánuco** con cifras en este libro: Pärssinen cita el quipu de 1549 y la mita decimal, pero no tabula las pachacas una por una (1992: 784-802, 6222). Esos vacíos limitan la comparación y explican por qué el corpus se concentra en Cajamarca, Cuzco, Collasuyu y Lupaca.

### 2.2 Estadísticos

Para cada lista completa se calculó:

- **CV** = desviación estándar / media de las cifras (desigualdad de tamaños).
- **máx/mín** = cociente entre la unidad mayor y la menor.
- **n efectivo** = 1 / Σp², donde p son las proporciones; dividido por n da una **equidad** entre 0 y 1 (1 = todas las unidades iguales). Es comparable entre listas de distinto n.
- **ρ de Spearman** entre la cifra y la posición en la lista (1 = primera). La firma de UR278 tiene ρ = −0,73; se prueba la cola negativa (lista de mayor a menor).
- **pendiente log(proporción) ~ rango**: mide el gradiente de tamaño cuando la lista se ordena de mayor a menor. La firma tiene pendiente −0,071; las filas individuales de UR278 tienen mediana −0,108 (rango −0,235 a −0,018).

### 2.3 Nulos, p-valores y corrección múltiple

- **Nulo de orden (ρ):** se permutan las posiciones de la lista. Para Bambamarca (n=9) se enumeraron las **9! = 362.880** permutaciones (p exacto, con empates); para el resto, 200.000 permutaciones de Monte Carlo con semilla 20261018. El p es a una cola (descenso).
- **Nulo de perfil (solo listas de 9):** se comparó el perfil ordenado de la lista con cada una de las **24 filas de UR278** (L2 sobre proporciones ordenadas). El nulo es la distribución de las **276 distancias entre pares de filas de UR278**: si la lista cae dentro de esa nube, su forma es indistinguible de la variabilidad interna del quipu; si cae fuera, es un desajuste. El p es la fracción de pares de filas más cercanos que la lista.
- **Nulo de orden documental (solo listas de 9):** L1 entre el perfil de la lista (en su orden) y el perfil medio de UR278; el nulo son las 24 filas de UR278 medidas contra su propia media.
- **Tríadas (3×3):** media de las correlaciones dentro de (1-2-3)(4-5-6)(7-8-9), frente a 20.000 particiones aleatorias en tres tríadas.
- **Corrección múltiple:** Holm sobre las **3 listas primarias independientes** (Bambamarca, Coco, Aullaga) y, como sensibilidad, sobre las 9 listas completas de n ≥ 7. Se reportan ambos.

### 2.4 Límites del método

1. **La muestra de listas no es aleatoria.** Son las listas que Pärssinen decidió imprimir. No representan el universo de censos coloniales; son casos disponibles.
2. **El orden de la tabla de Bambamarca no está verificado en el documento original.** Pärssinen pudo haber ordenado la tabla al publicarla. La presencia de inversiones (75 antes que 78; 49 antes que 75) sugiere que no es un simple ordenamiento por tamaño, pero no lo prueba. El resultado de Bambamarca debe leerse como "la lista tal como la publica Pärssinen", no como "el orden del quipu original".
3. **Son censos de 1567-1571, unos 35 años después de la conquista.** Pärssinen argumenta que el número de pachacas cambió poco, pero los hogares sí cambiaron. La estructura puede ser colonial, no incaica. Además, no todas las listas son transcripciones directas de un quipu: la de Bambamarca es una **visita** (Pärssinen discute que las visitas se basaban en khipus locales, pero el orden pudo fijarlo el escribano); las de Coco y Aullaga son **títulos de encomienda** que copian censos leídos de khipus. La distinción importa: una lista de visita puede estar ordenada por el escribano, no por el quipu.
4. **La firma de UR278 es un perfil medio de 24 filas.** Es más suave que cualquier fila individual: su CV (0,193) no debe compararse directamente con el CV de una lista única, sino con la distribución de CV de las 24 filas (mediana 0,290; IQR 0,190-0,359; máximo 0,480). Por eso se reporta el percentil de cada lista dentro de esa distribución.
5. **No se sabe qué son las cifras de UR278.** La comparación es de *forma* (n, planitud, orden), no de contenido semántico. Si las columnas no son personas/hogares, la analogía con censos es estructural, no sustantiva.
6. **Potencia limitada con n pequeño.** Con 9 unidades, el test de ρ solo detecta descensos fuertes; un ρ verdadero de −0,5 a menudo no alcanzará p < 0,05. La falta de significación en Coco o Aullaga no prueba que su orden sea aleatorio, solo que no se distingue de una permutación. Por eso el resultado positivo de Bambamarca (ρ −0,87) es más informativo que los negativos.

---

## 3. Resultados

### 3.1 La firma de 9 partes, recalculada

Con las 24 filas de 9 cuerdas de `ur278_tabla.csv` (54.601 unidades en total):

| estadístico | valor |
|---|---|
| perfil medio c1..c9 | 0,137 0,144 0,096 0,108 0,114 0,126 0,106 0,080 0,090 |
| CV del perfil | **0,193** |
| máx/mín | **1,80** |
| n efectivo / 9 | **8,71 / 9 = 0,968** |
| ρ(perfil, posición) | **−0,733** (p = 0,0246) |
| CV dentro de cada fila | mediana **0,290**; IQR 0,190-0,359; máximo 0,480 |
| ρ por fila | mediana **−0,59**; 62 % ≤ −0,5; 38 % ≤ −0,7 |
| pendiente log(proporción) ~ rango (perfil ordenado) | **−0,071** |
| pendiente por fila (ordenada) | mediana −0,108; rango −0,235 a −0,018 |

**Lectura:** el perfil es plano pero no igualitario (CV 0,19; máx/mín 1,8), y desciende con la posición. El descenso es una tendencia central: en cada fila individual el ρ mediano es −0,59, y solo el 38 % de las filas llega a −0,7. La firma es, por tanto, un **gradiente ordenado y estable**, no una escalera rígida que se repita exactamente en cada registro.

### 3.2 Las listas coloniales: cifras básicas

| lista | n | total | CV | máx/mín | equidad | ρ | p(ρ, una cola) | Holm primarias | percentil CV vs UR278 | pendiente ordenada |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Bambamarca, 9 pachacas** | 9 | 573 | **0,385** | 3,85 | 0,883 | **−0,870** | **0,0016** | **0,005** | 75 | −0,154 |
| **Coco, 9 aldeas** | 9 | 720 [730] | **1,079** | 25,0 | 0,491 | −0,268 | 0,240 | 0,240 | 100 | −0,432 |
| **Aullaga, 11 aldeas** | 11 | 260 | **0,613** | 17,7 | 0,745 | −0,446 | 0,082 | 0,164 | 100 | −0,221 |
| Lupaca, 12 sayas | 12 | 15.778 | **0,199** | 2,08 | 0,965 | −0,350 | 0,130 | — | 29 | −0,055 |
| Lupaca, 7 cabeceras | 7 | 15.778 | 0,356 | 3,12 | 0,902 | −0,286 | 0,251 | — | 75 | −0,183 |
| Chayanta 1540 | 12 | 346 | 0,647 | 7,50 | 0,723 | +0,172 | 0,708 | — | 100 | −0,182 |
| Chayanta 1548 | 12 | 376 | 0,620 | 7,75 | 0,739 | +0,154 | 0,688 | — | 100 | −0,190 |
| Yanque Collagua | 16 | 2.163 | 0,581 | 28,0 | 0,760 | +0,015 | 0,523 | — | 100 | −0,161 |
| Cavana Conde | 18 | 1.431 | 1,709 | 35,9 | 0,266 | −0,320 | 0,098 | — | 100 | −0,151 |
| Guancayo, 5 señores | 5 | 9 | 0,248 | 2,00 | 0,953 | +0,354 | 0,801 | — | 42 | −0,139 |
| Guancayo, 9 pachacas ideales | 9 | 900 | 0,000 | 1,00 | 1,000 | — | — | — | 0 | 0,000 |
| Chondal, 4 pachacas | 4 | 953 | 0,462 | 2,37 | 0,862 | −0,200 | 0,460 | — | 96 | −0,342 |
| Pacajes, 3 cabeceras | 3 | 3.610 | 0,245 | 1,65 | 0,961 | −0,500 | 0,499 | — | 42 | −0,138 |
| Huanca, 3 hunus | 3 | 27.000 | 0,333 | 2,00 | 0,931 | +1,000 | 1,000 | — | 67 | +0,347 |
| Chincha, 3 hunus | 3 | 28.000 | 0,327 | 2,00 | 0,933 | −1,000 | 0,168 | — | 62 | −0,347 |

El p de Bambamarca es 0,0016 (Monte Carlo; exacto 0,0018); el de las demás, Monte Carlo 200.000. La columna "percentil CV vs UR278" indica qué porcentaje de las 24 filas de UR278 tiene un CV menor o igual: 100 = la lista es más desigual que todas las filas; 29 = es más plana que el 71 % de las filas. La "pendiente ordenada" se calcula sobre las proporciones ordenadas de mayor a menor; la firma tiene −0,071.

Nota: la tabla de Cavana suma 1.431, pero el texto de Pärssinen da 1.461 [1.500]; probablemente falta una cifra en la transcripción. No afecta a las conclusiones (Cavana es un control de lista de aldeas, no una candidata).

### 3.3 ¿Las listas coloniales van de mayor a menor?

**No, en general.** De las 9 listas completas con n ≥ 7:

- solo **1 de 9** tiene ρ < −0,5 (Bambamarca);
- solo **1 de 9** tiene p < 0,05 (Bambamarca);
- solo **1 de 9** sobrevive a Holm (Bambamarca: 0,005 en las tres primarias; 0,014 en las nueve);
- la mediana de ρ es **−0,286**, y hay dos listas con ρ positivo (Chayanta 1540 y 1548).

El descenso de Bambamarca no se debe solo a la primera pachaca (la del cacique principal): si se excluye, las 8 pachacas restantes siguen bajando, ρ = **−0,814**, p exacto = **0,0092** (8! = 40.320). Es un gradiente de rango, no un simple "el principal es el mayor".

Las demás listas se ordenan por **jerarquía administrativa, capitalidad o geografía**, no por tamaño:

- **Lupaca:** Chucuito (capital) primero, luego Acora, Ilave, Juli, Pomata, Yunguyo, Zepita; dentro de cada cabecera, Alasaya (hanan) antes que Maasaya (hurin). El orden es el de la ruta/capital, y por eso el ρ es solo −0,35.
- **Cajamarca:** las tres primeras guarangas de Hanansaya (Guzmango, Chuquimango, Chondal) se listan antes que las tres de Hurinsaya (Bambamarca, Cajamarca, Pomamarca); la cuarta de Hanansaya, **Mitimaes**, va al final de la lista, probablemente por su carácter de guaranga de mitimaes (Pärssinen 4752, 4786). Chondal, la mayor de las tres, va antes que Bambamarca y Pomamarca, pero tiene solo 4 pachacas frente a 9 y 8: el número de pachacas no sigue el tamaño de la guaranga.
- **Chayanta:** la secuencia de 12 pueblos es casi idéntica en las dos transcripciones (1540 y 1548), pero las cifras no descienden (ρ +0,17 y +0,15).

**Conclusión:** la idea de que "las listas coloniales también van de mayor a menor" es falsa como regla general. Bambamarca es la excepción, no el patrón.

**Pares y mitades documentados.** Las listas coloniales sí tienen estructura dual, pero no la de la firma:

- **Lupaca:** cada cabecera se divide en Alasaya (hanan) y Maasaya (hurin); el cuadro de 12 sayas es 7 cabeceras × 2, con Ilave y Yunguyo combinadas.
- **Cajamarca:** 4 guarangas de Hanansaya + 3 de Hurinsaya (mitades desiguales, no pares).
- **Yanque y Cavana:** Hanansaya + Hurinsaya.
- **Coco:** 7 principales subordinados; 1 pachaca calculativa en Guamanrroro y 2 en Matara. No hay mitades.
- **Bambamarca y Aullaga:** no hay mitades internas documentadas.
- **Guancayo:** 1+4×2 (5 señores; uno con una pachaca, cuatro con dos).

La firma, en cambio, **no muestra una bipartición 4+4+1**: en n_nueve_unidades, la mejor bipartición 4+4(+1) da p = 0,187 (C2) y el contraste de medias 1-4 vs 5-8 da p = 0,327 (L8). El mejor emparejamiento es 4 pares + 1 suelta, no dos mitades de cuatro. Por tanto, las mitades coloniales (Alasaya/Maasaya, Hanansaya/Hurinsaya) **no se reproducen** como una bipartición de las 9 columnas; lo que se reproduce, si algo, es la forma 1+4×2.

### 3.4 ¿Son tan planas como la firma?

Tampoco en general. La firma tiene CV de perfil 0,193, pero la comparación correcta es con las filas individuales de UR278 (mediana 0,290; IQR 0,190-0,359; máximo 0,480).

- **Bambamarca:** CV 0,385, percentil 75 de las filas. Está dentro de la distribución, en el cuartil alto: es más desigual que la mediana, pero no es un caso extremo.
- **Coco:** CV 1,079, percentil 100. Es **más desigual que todas** las filas de UR278 (máximo 0,480). No es compatible.
- **Aullaga:** CV 0,613, percentil 100. También fuera por arriba.
- **Lupaca 12 sayas:** CV 0,199, percentil 29. Es la única lista colonial **tan plana o más** que la mediana de las filas de UR278. Su pendiente ordenada (−0,055) es casi idéntica a la de la firma (−0,071).
- Yanque (0,581), Cavana (1,709), Chayanta (0,65/0,62): mucho más desiguales.

**Lectura:** la firma no se parece a una lista de aldeas (Coco, Aullaga, Yanque, Cavana), que son mucho más desiguales. Se parece, en cambio, a un **censo decimal de unidades administrativas** (Lupaca) o a una **guaranga de pachacas reales** (Bambamarca), no a un conjunto de asentamientos.

### 3.5 Comparación directa de perfil (listas de 9)

Solo dos listas independientes tienen 9 unidades completas: Bambamarca (pachacas) y Coco (aldeas). Los valores, en el orden de la fuente, son:

- **Bambamarca:** Ychican 104, Bambamarca 75, Tacabamba 78, Tingomayo 68, Quiden 49, Guangamarca 75, Curocchuc 67, Anbagay 30, Pisso 27 (total 573).
- **Coco:** Chonda 250, Guamanrroro 100, Tocoyoco 20, Tocayaco 10, Vxaca 70, Tarapa 10, Matara 200, Chupaico 40, Yachibamba 30 (total 720; el texto da 720-730).

Se compara su perfil ordenado con las 24 filas de UR278; el nulo son los 276 pares de filas.

| lista | L2 medio a las 24 filas | percentil vs 276 pares | L1 en el orden documental | percentil vs 24 filas | pendiente ordenada | percentil de pendiente |
|---|---:|---:|---:|---:|---:|---:|
| **Bambamarca** | **0,067** | **60,5** | 0,222 | 87,5 | −0,154 | 12,5 |
| **Coco** | **0,268** | **100** | 0,746 | 100 | −0,432 | 0 |
| Guancayo ideal (9×100) | 0,086 | 81,9 | 0,086 | 50 | 0,000 | 100 |

- **Bambamarca cae dentro de la nube de UR278**: su distancia media (0,067) es casi la mediana de las distancias entre filas (0,061); su fila más cercana está a 0,025. El percentil 60,5 significa que el 60 % de los pares de filas de UR278 son *más* cercanos entre sí que Bambamarca a la nube; no es una coincidencia excepcional, pero tampoco un desajuste. Su pendiente es más pronunciada que la de la firma (percentil 12,5: más empinada que el 87,5 % de las filas).
- **Coco cae fuera**: su distancia media (0,268) es mayor que *todas* las distancias entre filas de UR278 (máximo 0,138); su fila más cercana está a 0,210. Es un desajuste claro.
- **El ideal 9×100 de Guancayo** tiene un L2 al perfil medio de 0,061, ligeramente menor que el de Bambamarca (0,067), pero su CV = 0 está fuera de la distribución de filas (percentil 0) y su gradiente es nulo (0 vs −0,071). No reproduce la desigualdad ni el descenso: es un reparto perfectamente igual, no la firma.

**Nulo de listas aleatorias con la misma n y CV.** Para separar "se parece porque tiene ese CV" de "se parece por su forma", se generaron 20.000 listas lognormales de 9 valores con el mismo CV que cada lista y se comparó su L2 al perfil medio:

- **Bambamarca:** L2 observado 0,067; mediana nula 0,056; p = **0,646**. Su parecido es *típico* para una lista de su CV, no excepcional. La señal de Bambamarca está en el **orden** (ρ −0,87), no en una forma imposible.
- **Coco:** L2 observado 0,284; mediana nula 0,196; p = **0,812**. Es más extrema de lo que su CV predice: su desajuste no es solo "muy desigual", sino "muy sesgada" (dos unidades gigantes y una cola de unidades minúsculas).

**Conclusión:** la lista de **9 pachacas de Bambamarca** es el mejor análogo textual de 9 unidades: reproduce el descenso (ρ −0,87) y su perfil ordenado es compatible con la nube de UR278. No es una coincidencia perfecta: es más desigual y más empinada que la firma. La lista de **9 aldeas de Coco** es un desajuste claro, lo que favorece "unidades administrativas/pachacas" sobre "asentamientos".

### 3.6 Las unidades de 9 y la estructura 1+4×2

Se buscaron unidades de 9 y estructuras 1+4×2 en todo el material:

| caso | n | estructura | cifras | comentario |
|---|---:|---|---|---|
| **Bambamarca** | 9 | 9 pachacas de una guaranga | 104, 75, 78, 68, 49, 75, 67, 30, 27 | la única lista de 9 pachacas con cifras completas en Pärssinen |
| **Coco** | 9 | 9 aldeas de un curacazgo | 250, 100, 20, 10, 70, 10, 200, 40, 30 | 7 principales; 1 pachaca calculativa en Guamanrroro, 2 en Matara |
| **Guancayo** | 9 | 9 pachacas bajo 5 señores | 2, 1, 2, 2, 2 (pachacas por señor) | **1+4×2**: un señor con 1, cuatro con 2; 900 hatun runa; 5 cestos de coca por pachaca = 45 |
| **Collaguas** | 9 | 9 patacas por mitad (3×3) | 100 cada una | 100+100+100 + 100+100+100 + 100+100+100 = 900 (Pärssinen 6401) |
| **Ceque** | 9 | 9 líneas por suyu (3×3) | sin cifras | Chinchaysuyu, Antisuyu y Collasuyu tienen 9 ceques en 3 grupos (Pärssinen 3040) |

**Guancayo es el único caso documentado de 1+4×2 con cifras:** 900 hatun runa repartidos en 9 pachacas, bajo 5 señores; uno gobierna una pachaca y cuatro gobiernan dos (Rostworowski 2601; Pärssinen 6285). Además, cada pachaca da **5 cestos grandes de coca** al Inca, es decir, 45 para el señorío (Rostworowski 2601). Es un ancla textual fuerte para "9 unidades decimales bajo 5 señores", pero **no** para un perfil desigual: si las 9 pachacas son iguales (100 cada una), el CV es 0, y la firma tiene CV 0,19.

Si las 9 columnas registraran los **cestos de coca**, serían 9 × 5 = 45, todos iguales (CV 0); no es el caso. Si registraran el **número de pachacas** de cada señor (2,1,2,2,2), serían 5 columnas, no 9. La lectura más económica es que las columnas registran el **tamaño o la cuota real de 9 pachacas**, no el número de cestos ni el de pachacas por señor. Eso es coherente con el CV 0,19: pachacas reales, no ideales.

La firma, por su parte, tiene un **mejor emparejamiento de 4 pares + 1 suelta** (p = 0,002 frente a 945), y la suelta es **c8, la columna más pequeña**. Eso es exactamente la forma 1+4×2: cuatro pares y un singlete. La analogía con Guancayo es tentadora: los cuatro pares serían los cuatro señores con dos pachacas, y c8 sería el señor con una sola pachaca (la más pequeña). Pero hay que ser escéptico:

- Los pares del mejor emparejamiento son **(1-2), (3-6), (4-9), (5-7)**, no contiguos. En Guancayo las pachacas de cada señor son contiguas (2,1,2,2,2), así que un quipu que agrupara por señor debería dar pares contiguos, no saltados.
- De los cuatro pares, solo **(1-2)** (r = 0,675, q = 0,018) y **(5-7)** (r = 0,447, q = 0,048) sobreviven a BH; **(3-6)** (r = 0,090) y **(4-9)** (r = 0,293) son débiles. El p = 0,002 es del *máximo* sobre 945 emparejamientos, no de cuatro pares independientes; parte de la señal es selección.
- La columna suelta es la más pequeña, lo que encaja con el señor de una sola pachaca, pero también con la explicación aburrida de que c8 es la unidad de ajuste (n_nueve_unidades, 4.4).

**Nivel:** la forma 1+4×2 está **apoyada con datos** en la firma (el mejor emparejamiento es mejor que el azar) y **documentada** en Guancayo. La identificación concreta de los cuatro pares con cuatro señores es **especulativa**.

Un caso paralelo de "número ideal vs número real" refuerza la cautela: en Lupaca se decía que cada saya de Chucuito tenía **17 hathas** (17 × 100 ≈ 1.700), pero la visita de 1574 encontró **13** en Maasaya y **11** en Alasaya (Pärssinen 6088; también 6080-6088). El número de unidades de una lista puede ser un ideal decimal, no un conteo real. Si las 9 columnas son un ideal (9 × 100 = 900, como Guancayo o Collaguas), el número 9 no necesita corresponder a 9 unidades sociales reales; pero la desigualdad del perfil (CV 0,19) indica que, si es un ideal, no es un reparto igualitario.

### 3.7 La alternativa 3×3 (Collaguas, ceque) falla

Collaguas organiza cada mitad en **3 grupos de 3 patacas** (9 por mitad; Pärssinen 6401), y el ceque tiene **9 líneas por suyu en 3 grupos de 3** (Pärssinen 3040). Si las 9 columnas fueran una estructura 3×3, las tríadas consecutivas (1-2-3)(4-5-6)(7-8-9) deberían estar más correlacionadas entre sí que una partición al azar.

No lo están:

- media de r dentro de las tres tríadas consecutivas = **−0,020**;
- media nula (20.000 particiones) = **−0,099**;
- p = **0,190** (la tríada observada no es especial; en la enumeración completa de las 280 particiones en tres tríadas, la partición consecutiva queda en el puesto 53/280).

**Resultado negativo:** la estructura 3×3 de Collaguas/ceque no explica las 9 columnas. La forma 1+4×2 (4 pares + 1) tiene más apoyo que la 3×3.

### 3.8 Qué dice Pärssinen sobre el orden y la transcripción

- **El orden es una de las tres variables básicas del quipu**, junto con el color y el número (Pärssinen 1992: 717). Pärssinen acepta con cautela la afirmación de Garcilaso de que las cosas "iban puestas por su orden, empezando de las de más calidad y procediendo hasta las de menos" (1992: 709).
- **El orden de un texto-quipu sigue el prestigio político, no la cronología**: en la historia de Topa Inca, primero Chinchaysuyu, después Antisuyu, Collasuyu y Cuntisuyu (1992: 1446). El orden de prestigio de los suyus es Chinchaysuyu > Antisuyu > Collasuyu > Cuntisuyu (1992: 3066).
- **El orden de las categorías es fijo pero "elástico"**: maíz antes que quinua y papas, pero las categorías pueden intercambiarse; lo nuevo se añade al final o al principio (1992: 707, 730).
- **En los censos, los nombres se memorizaban en el orden en que estaban listados**; los quipucamayos tenían métodos para marcar nombres con color y número (1992: 803).
- **Las transcripciones a papel conservan sobre todo la secuencia de unidades, no tanto las cifras exactas.** Las dos copias de Chayanta (1540 y 1548) tienen la misma secuencia de 12 pueblos (ρ entre ambas = **0,977**), aunque las cifras varían en ±1 a ±24 y Pärssinen dice que las listas estaban "ordenadas de manera muy distinta" (2004: 477). Los errores de lectura de ±1 nudo están documentados (2004: 575). Esto aconseja leer el orden como relativamente estable y las cifras como aproximadas.
- **El orden reproduce la jerarquía de las parcialidades.** Curatola (2013: 227) muestra que los caciques y quipucamayos de Lucanas-Laramati se colocaban, al leer sus quipus, en el mismo orden jerárquico de los ayllus; el quipu conserva "la huella de su propia creación colectiva". El quipu es un "evento de escritura" en el que se negocian cuotas y se reproduce la organización social (Curatola 2013: 197-227).
- **Las cuotas se expresan como fracciones del total.** Polo de Ondegardo: cada parcialidad sabía si le tocaba la séptima, quinta o décima parte (Curatola 2013: 203); en los quipus huancas las entregas se reparten en fracciones de **2/9, 3/9 y 4/9** (Chirinos, citado en Curatola 2013: 196). Es decir, el **9 como denominador** tiene un antecedente textual en la contabilidad de parcialidades, aunque no en una lista de 9 unidades.
- **El hanan va primero, con excepciones.** En la tabla lupaca, Alasaya (hanan) precede sistemáticamente a Maasaya (hurin) en cada cabecera (Pärssinen 6058-6070); en Cajamarca, las tres primeras guarangas de Hanansaya (Guzmango, Chuquimango, Chondal) preceden a las de Hurinsaya, aunque Mitimaes (Hanansaya) va al final (Pärssinen 4752, 4786). El orden de las listas es, por tanto, un orden de **prestigio/mitad**, que puede correlacionar con el tamaño (el principal suele ser el mayor) pero no es un ordenamiento por tamaño.

---

## 4. Controles

### 4.1 Nulo de orden y corrección múltiple

| lista | ρ observado | p (una cola) | Holm (3 primarias) | Holm (9 listas) |
|---|---:|---:|---:|---:|
| Bambamarca | −0,870 | **0,0016** (exacto 0,0018) | **0,0047** | **0,014** |
| Coco | −0,268 | 0,240 | 0,240 | 1,000 |
| Aullaga | −0,446 | 0,082 | 0,164 | 0,658 |
| Lupaca 12 | −0,350 | 0,130 | — | 0,779 |
| Lupaca 7 | −0,286 | 0,251 | — | 1,000 |
| Chayanta 1540 | +0,172 | 0,708 | — | 1,000 |
| Chayanta 1548 | +0,154 | 0,688 | — | 1,000 |
| Yanque | +0,015 | 0,523 | — | 1,000 |
| Cavana | −0,320 | 0,098 | — | 0,684 |

Solo Bambamarca sobrevive a Holm en ambas versiones. El resultado no depende de la corrección.

### 4.2 Nulo de perfil y de orden documental

| prueba | observado | nulo | p | lectura |
|---|---:|---|---:|---|
| Bambamarca, perfil ordenado L2 | 0,067 | 276 pares de filas UR278 (mediana 0,061; máx 0,138) | 0,607 | dentro de la nube; compatible |
| Coco, perfil ordenado L2 | 0,268 | ídem | 1,000 | fuera de la nube; desajuste |
| Bambamarca, orden documental L1 | 0,222 | 24 filas UR278 (rango 0,083-0,304) | 0,880 | dentro del rango, pero menos típico |
| Coco, orden documental L1 | 0,746 | ídem | 1,000 | muy por fuera |
| Bambamarca, nulo CV (L2 al perfil) | 0,067 | 20.000 listas lognormales de n=9 y CV=0,385 (mediana 0,056) | 0,646 | típico para su CV; la señal está en el orden |
| Coco, nulo CV (L2 al perfil) | 0,284 | 20.000 listas lognormales de n=9 y CV=1,079 (mediana 0,196) | 0,812 | más extremo de lo que su CV predice |
| Tríadas 3×3 | −0,020 | 20.000 particiones (media −0,099) | 0,190 | sin estructura de tríadas |

**Nota sobre el p del perfil:** no es un test de "la lista es igual a la firma"; es un test de si la lista cae dentro de la variabilidad de las filas de UR278. Un p alto (Bambamarca 0,607) significa "no se distingue de la nube"; un p = 1,000 (Coco) significa "está más lejos que todos los pares de filas". Para Bambamarca, el resultado es de **compatibilidad**, no de identidad bien apoyada.

### 4.3 Estabilidad de la transcripción (Chayanta)

Las dos transcripciones del mismo quipu (1540 y 1548) dan:

- misma secuencia de 12 pueblos (ρ entre los vectores de cifras por posición = **0,977**);
- diferencias de cifras: 40→42, 22→46, 60→62, 26→27, 16→17; el resto iguales;
- suma 346 vs 376.

**Lectura:** el orden de los pueblos es muy estable; las cifras no. Esto apoya la idea de que un quipu transcrito conserva la **secuencia de unidades** mejor que los valores exactos. También es un control para nuestra comparación: si el orden de Bambamarca se conservó al pasar al papel, su ρ −0,87 es informativo; si Pärssinen lo reordenó, no lo es. No pudimos verificar el documento original.

### 4.4 Otras comprobaciones

- **Bambamarca sin la primera pachaca:** ρ = −0,814, p exacto = 0,0092 (8!); el descenso no es solo el efecto del principal.
- **Bambamarca con la primera pachaca:** ρ = −0,870, p exacto = 0,0018; la primera es 1,39× la segunda y 1,77× la media de las otras ocho. Es un principal grande, pero no desproporcionado.
- **Guancayo ideal 9×100:** CV = 0, equidad = 1; cae en el percentil 82 de la nube de perfiles, pero no reproduce el gradiente. Un reparto decimal perfecto es *demasiado plano*.
- **Lupaca 12 sayas:** CV 0,199 (percentil 29), pendiente −0,055 (percentil 79): es la lista más plana y con el gradiente más parecido a la firma, pero tiene 12 unidades y su orden es administrativo (ρ −0,35). No es una lista de 9.

---

## 5. Resultados negativos

1. **No hay una lista colonial de 9 unidades que sea a la vez plana y ordenada como la firma.** Bambamarca es la única que desciende, pero es más desigual (CV 0,385 vs perfil 0,193) y más empinada (pendiente −0,154 vs −0,071). Lupaca 12 es tan plana como la firma, pero tiene 12 unidades y no desciende (ρ −0,35).
2. **La lista de 9 aldeas de Coco no se parece en nada:** CV 1,079, máx/mín 25, distancia de perfil fuera de la nube de UR278 (0,268 > 0,138). Esto es un argumento contra "las 9 columnas son 9 asentamientos".
3. **Aullaga (11 aldeas) y las listas de Collaguas (Yanque 16, Cavana 18) son demasiado desiguales** (CV 0,58-1,71; percentil 100). No son candidatas.
4. **Las listas coloniales no van generalmente de mayor a menor:** solo 1 de 9 (Bambamarca) tiene ρ < −0,5 y sobrevive a Holm; la mediana de ρ es −0,29; hay listas con ρ positivo.
5. **La estructura 3×3 (Collaguas, ceque) no aparece en las 9 columnas:** p = 0,190; la partición consecutiva en tríadas queda en el puesto 53/280.
6. **El ideal decimal 9×100 es demasiado plano:** CV 0; no reproduce la desigualdad real de la firma. Si las 9 columnas fueran pachacas ideales de 100, esperaríamos CV ≈ 0, no 0,19.
7. **El orden de las listas coloniales es jerárquico/geográfico, no de tamaño.** Lupaca ordena por cabecera y por hanan/hurin; Cajamarca ordena las guarangas de Hanansaya antes que las de Hurinsaya; Chayanta conserva la secuencia de pueblos pero no desciende. La correlación con el tamaño, cuando existe (Bambamarca), es un subproducto del rango del principal, no una regla de ordenamiento.
8. **No se pudo verificar el orden original de la tabla de Bambamarca.** Si Pärssinen ordenó la tabla por tamaño, el ρ −0,87 sería un artefacto editorial. Las inversiones internas (75 antes que 78; 49 antes que 75) lo hacen improbable, pero no es una prueba.

---

## 6. Nivel de evidencia

| afirmación | nivel |
|---|---|
| Las 9 columnas de UR278 tienen un perfil estable, desigual y ordenado (ρ −0,73; CV 0,193; 24 filas) | **bien apoyado** (replicado en n_nueve_unidades) |
| Las listas coloniales de unidades no se ordenan en general de mayor a menor (1/9 con ρ < −0,5; mediana −0,29) | **bien apoyado** para el corpus extraído |
| La lista de 9 pachacas de Bambamarca desciende con la posición (ρ −0,87; p exacto 0,0018; Holm 0,005; sin la primera, ρ −0,81, p 0,009) | **bien apoyado** estadísticamente, con la reserva del orden editorial de la tabla |
| El perfil ordenado de Bambamarca es compatible con la nube de filas de UR278 (percentil 60,5) | **apoyado con datos** (compatibilidad, no identidad) |
| El parecido de *forma* de Bambamarca no es excepcional para su CV (p = 0,646 frente a listas aleatorias con su mismo CV); la señal está en el **orden** (ρ −0,87), no en una forma imposible | **bien apoyado** (resultado negativo parcial) |
| La lista de 9 aldeas de Coco es incompatible con la firma (CV 1,08; perfil fuera de la nube) | **bien apoyado** (resultado negativo) |
| El censo lupaca de 12 sayas tiene la misma planitud/gradiente que la firma (CV 0,199; pendiente −0,055), pero 12 unidades y orden administrativo | **apoyado con datos** (buen análogo de forma, no de número/orden) |
| Las 9 columnas son 9 pachacas/unidades administrativas de una guaranga o provincia, ordenadas por rango | **propuesto** |
| La estructura 1+4×2 (4 pares + 1 suelta) de la firma se corresponde con los 5 señores de Guancayo (4 con dos pachacas, 1 con una) | **propuesto / especulativo**; la forma 1+4×2 está apoyada, la identificación concreta de los pares no |
| La columna c8 (la suelta) es el señor con una sola pachaca | **especulativo** |
| Las 9 columnas son un calendario o una estructura 3×3 | **no apoyado / negativo** |

---

## 7. Para el coordinador

- **La firma de 9 partes sigue en pie:** 24 filas, 54.601 unidades, perfil CV 0,193, máx/mín 1,80, ρ −0,73; el descenso es una tendencia central (ρ mediano por fila −0,59), no una escalera rígida.
- **La lista colonial más parecida a las 9 columnas es la de las 9 pachacas de la guaranga de Bambamarca (Cajamarca, 1567):** ρ = −0,870 (p exacto 0,0018; Holm 0,005), y su perfil ordenado cae dentro de la nube de las 24 filas de UR278 (percentil 60,5). Es el único caso de 9 unidades que desciende en nuestro corpus; sin la pachaca del cacique principal, las 8 restantes siguen bajando (ρ −0,81, p 0,009).
- **Pero no es una coincidencia perfecta:** Bambamarca es más desigual (CV 0,385 vs 0,193) y más empinada (pendiente −0,154 vs −0,071). La lista de 9 aldeas de Coco es un desajuste claro (CV 1,08; perfil fuera de la nube), lo que favorece "pachacas/unidades administrativas" sobre "asentamientos".
- **El mejor análogo de planitud no es una lista de 9, sino el censo lupaca de 12 sayas:** CV 0,199 (percentil 29 de las filas), pendiente −0,055, casi idéntica a la firma (−0,071). Tiene 12 unidades y orden administrativo (ρ −0,35), así que no explica el 9 ni el orden, pero demuestra que un censo decimal leído de un quipu puede tener exactamente esa planitud.
- **Las listas coloniales no van en general de mayor a menor:** solo 1 de 9 (Bambamarca) tiene ρ < −0,5 y sobrevive a Holm; la mediana es −0,29; Lupaca ordena por cabecera y hanan/hurin; Cajamarca pone Guzmango, Chuquimango y Chondal (Hanansaya) primero, aunque Mitimaes va al final; Chayanta conserva la secuencia pero no desciende. El orden es de prestigio/jerarquía, no de tamaño.
- **Guancayo (Chillón) da el ancla 1+4×2:** 900 hatun runa, 9 pachacas bajo 5 señores (uno con una, cuatro con dos), 5 cestos de coca por pachaca = 45. Es el único caso documentado de 9 = 1+4×2 con cifras.
- **La forma 1+4×2 también está en la firma:** el mejor emparejamiento es 4 pares + 1 suelta (p = 0,002), y la suelta es c8, la columna más pequeña, justo como el señor con una sola pachaca. Pero los pares no son contiguos y solo (1-2) y (5-7) sobreviven a BH; la identificación con los cinco señores es **especulativa**, no bien apoyada.
- **Dos alternativas fallan:** la estructura 3×3 (Collaguas, ceque) no aparece (p = 0,190; la partición consecutiva queda 53/280), y el ideal decimal 9×100 es demasiado plano (CV 0; la firma tiene 0,19). Las 9 columnas no son ni tríadas ni pachacas ideales iguales: son unidades reales de tamaño desigual (o un censo de sayas como el lupaca).
- **Recomendación para la siguiente ronda:** (1) verificar el orden de la tabla de Bambamarca en la visita original de González de Cuenca (1567) o en la copia de Espinoza Soriano 1976-77, para descartar un orden editorial; (2) buscar una provincia con **5 cabeceras y 9 sayas/pachacas** (4×2+1) en las visitas de Chucuito, Pacajes o Collaguas; (3) probar si las 9 columnas se pueden agrupar en 4 pares + 1 con una regla *ex ante* (no el máximo sobre 945), por ejemplo pares de columnas que compartan color o longitud de cuerda; (4) contrastar la hipótesis "pachacas reales" con la escala absoluta: ~250 unidades por columna es compatible con pachacas de una guaranga grande o con sayas pequeñas, pero no con pachacas ideales de 100.
- **Nivel global:** el parecido con Bambamarca es **apoyado con datos**; la lectura "9 pachacas de una guaranga ordenadas por rango" es **propuesta**; el mapeo concreto a los cinco señores de Guancayo es **especulativo**. No hay ninguna lista colonial que reproduzca a la vez el 9, la planitud y el orden de la firma.

---

### Referencias citadas

- Pärssinen, M. 1992. *Tawantinsuyu: The Inca State and Its Political Organization*. Helsinki: SHS. Líneas del txt: 709, 717, 1446, 3040, 3066, 4752, 4786, 5835-5837, 6058-6070, 6088, 6229-6231, 6285, 6310-6316, 6401, 6551.
- Pärssinen, M. & J. Kiviharju 2004. *Textos Andinos. Corpus de textos khipu incaicos y coloniales*, I. Madrid. Líneas: 463, 477, 505-520, 575.
- Curatola Petrocchi, M. & J. C. de la Puente Luna 2013. "Contar concertando: quipus, piedritas y escritura en los Andes coloniales". En *El quipu colonial*. Lima: PUCP. Líneas: 115, 173, 196-203, 227.
- Rostworowski, M. *Costa peruana prehispánica*. Líneas: 369-371, 2601.
- `analisis/ds/n_nueve_unidades/informe.md` (firma de 9 partes, emparejamientos, c8).
- `analisis/13_sistema_incahuasi/ur278_tabla.csv` (24 filas de 9).
