# Informe lit_4 — De afirmaciones de la literatura a pruebas con datos

## 1. Pregunta

¿Qué afirmaciones concretas sobre el significado o la estructura de los quipus, publicadas en las 12 fichas asignadas, son lo bastante específicas para contrastarlas con `analisis/datos/*.csv`, y cuáles se sostienen al comprobarlas?

## 2. Método

**Corpus.** 651 quipus y 57.818 cuerdas del Khipu Field Guide (KFG), más metadatos por quipu (651 filas) y 8.117 grupos de colgantes. El OKR se usó solo para verificar recuentos (619 quipus / 54.403 cuerdas / 110.677 nudos) y la cobertura del campo de fibra.

**Unidad de análisis.** El quipu. Todos los estadísticos se agregan por quipu; no se cuenta cada cuerda como observación independiente.

**Inventario.** Se extrajeron 28 afirmaciones comprobables de las 12 fichas y se clasificaron como `si` (9), `parcial` (9) o `no` (10) según si el repo contiene las variables necesarias. Están en `afirmaciones.csv`; la generación es reproducible con `hacer_afirmaciones.py`.

**Controles.** Cada prueba con incertidumbre lleva modelo nulo explícito de permutación, semilla fija `20261017` y 2.000 réplicas. Se corrigió por comparaciones múltiples con Holm sobre las tres pruebas de permutación (V1, V2, V5); incluyendo las cuatro subpruebas de V2, el mayor p ajustado es 0,003. Los recuentos exactos (V3, V4, OKR) no requieren p-valor: son aritmética verificable.

**Definiciones operativas.**

- *Nudo inferior (nether knot)*: en la cadena `nudos` (arriba→abajo), el último cluster y el penúltimo tienen valor aportado entre 1 y 9, de modo que el último cae por debajo de la posición de las unidades. Sensibilidad morfológica estricta: último cluster de tipo `E` precedido de un `L`/`LL` de unidades.
- *Relación de suma de Ascher*: (B) en un grupo de ≥3 colgantes, el primero vale la suma de los demás; (B2) algún colgante del grupo vale la suma de los demás; (C) un grupo de un solo colgante vale la suma del grupo anterior. Solo colgantes de nivel 0 con nudos y valor no ausente.
- *Frontera de grupo*: primer y último colgante (por número `p`) de cada grupo con ≥2 colgantes; *interior*: los demás.
- *Blanco*: código de color exacto `W`; sensibilidad con cualquier color que contenga `W`.

**Scripts.** Desde la raíz del repo: `python analisis/ds/lit_4/hacer_afirmaciones.py` genera `afirmaciones.csv`; `python analisis/ds/lit_4/chequeos.py` ejecuta V1–V6 y escribe `resultados.json` (≈4 min, dominado por las 2.000 permutaciones de V2 y V5). No se modificó nada fuera de `analisis/ds/lit_4/`.

## 3. Resultados

### 3.1 Inventario de afirmaciones

| Fuente | Filas | Sí | Parcial | No |
|---|---:|---:|---:|---:|
| Hyland 2024 | 2 | 1 | 0 | 1 |
| Medrano & Khosla 2024 | 4 | 1 | 2 | 1 |
| Milillo 2024 | 2 | 0 | 1 | 1 |
| Setlak 2024 | 2 | 0 | 0 | 2 |
| Thompson 2024 | 2 | 0 | 1 | 1 |
| Clindaniel 2025 | 1 | 0 | 1 | 0 |
| Hyland et al. 2025 | 2 | 1 | 0 | 1 |
| Thompson 2025 (correcciones) | 5 | 4 | 1 | 0 |
| Thompson 2025 (KBCR) | 2 | 0 | 2 | 0 |
| Contreras 2026 | 4 | 2 | 1 | 1 |
| Dosselmann et al. 2026 | 1 | 0 | 0 | 1 |
| FitzPatrick 2026 | 1 | 0 | 0 | 1 |
| **Total** | **28** | **9** | **9** | **10** |

La mitad de las afirmaciones (10/28) no son contrastables con el repo por falta de ids, de texto o de variables (envoltorios, lecturas coloniales, isótopos, firmas de artesano). Eso ya es un resultado: la literatura revisada es en buena parte no falsable con los datos abiertos disponibles.

### 3.2 V1. Nudos inferiores: el «>20 %» se sostiene, pero casi todo es tasa base

Hyland (2024) afirma que los nudos inferiores aparecen en más del 20 % de los quipus del OKR.

| Definición | Cuerdas | Quipus | % de 651 |
|---|---:|---:|---:|
| Dos últimos clusters en 1–9 (amplia) | 2.384 | 242 | **37,2 %** |
| Último cluster tipo `E` | 796 | 161 | 24,7 % |
| Último `E` tras un `L`/`LL` (estricta) | 631 | 148 | **22,7 %** |

IC 95 % de la definición amplia (Wilson/Beta): 33,5–40,9 %. El «>20 %» se cumple incluso con la definición estricta (22,7 %).

**Pero** el nulo que permuta el orden de los clusters dentro de cada cuerda da 33,4 % de quipus con al menos un nudo inferior (media de 2.000 réplicas), frente al 37,2 % observado (242/651); p empírico = 0,0005. Es decir, la mayor parte de la prevalencia se explica por la frecuencia de clusters de unidades y por el número de clusters por cuerda, no por una posición anómala. El exceso atribuible a la posición «bajo las unidades» es de solo ~3,8 puntos porcentuales (≈12 % relativo).

**Nivel:** *apoyado con datos* para la prevalencia >20 %; *especulativo* para la lectura de que esos nudos obligan a revisar la tipología de Locke, porque el nulo muestra que la mayoría son esperables sin intención codificadora.

### 3.3 V2. Fórmulas de Ascher: hay sumas no aleatorias, pero no el 74 %

Medrano y Khosla (2024) afirman que las fórmulas de Ascher caracterizan al menos el 74 % de 650 quipus.

| Relación | Observado | Nulo (permutación dentro del quipu) | p empírico |
|---|---:|---:|---:|
| B: primer colgante = suma del resto (grupos ≥3) | 5,6 % | 3,48 % | 0,0015 |
| B2: algún colgante = suma del resto (grupos ≥3) | 12,7 % | 10,05 % | 0,0015 |
| C: grupo de 1 = total del grupo anterior | 4,7 % | 0,96 % | 0,0005 |
| **Cualquiera de las tres** | **16,3 %** (104/638) | **10,63 %** | **0,0005** |

Las sumas internas están enriquecidas respecto al azar (razón observado/nulo ≈ 1,5; para C ≈ 4,9), así que hay estructura aritmética real. Pero con una definición estricta y portable, la cobertura es 16,3 %, no 74 %. La diferencia no es un fallo de la afirmación necesariamente: Medrano usa una familia de fórmulas mucho más amplia (subsidiarias, top cords, grupos, fragmentos) que el resumen no detalla. Lo que sí se puede decir es que **la cifra del 74 % no es reproducible con las convenciones de suma más simples** y que el resumen no reporta tasa base. Sin el nulo, el 16,3 % parecería alto; con el nulo, el exceso es de 5,7 puntos.

**Nivel:** *apoyado con datos* que las sumas internas no son aleatorias; *no bien apoyado* (y no replicado) el 74 %.

### 3.4 V3. Valle del Santa: replicación exacta del patrón recto/verso

Contreras (2026) afirma que en UR087–UR092 (KH0323–KH0328) el 49,0 % de las cuerdas son recto y el 51,0 % verso, que cinco de seis quipus son puros y que solo KH0326 es mixto (40 recto / 69 verso).

| KFG | Cuerdas | R | V | U | % R (de R+V) |
|---|---:|---:|---:|---:|---:|
| UR087 | 370 | 310 | 0 | 60 | 100,0 |
| UR088 | 102 | 0 | 54 | 48 | 0,0 |
| UR089 | 288 | 0 | 207 | 81 | 0,0 |
| UR090 | 131 | 40 | 69 | 22 | 36,7 |
| UR091 | 125 | 0 | 93 | 32 | 0,0 |
| UR092 | 61 | 56 | 0 | 5 | 100,0 |
| **Total** | **1.077** | **406** | **423** | **248** | **49,0** |

Se reproduce exactamente: 49,0/51,0 agregado, 5 quipus puros y UR090 (=KH0326) con 40 R / 69 V. El total de cuerdas es 1.077, una menos que las 1.078 del artículo; las 248 sin especificar son consistentes con las 249 reportadas. La discrepancia de una cuerda no afecta ninguna conclusión.

**Advertencia:** la coincidencia es exacta porque el campo `union` del KFG y el `ATTACHMENT_TYPE` del OKR probablemente comparten la misma tradición de registro (Harvard KDB). Es una verificación de aritmética y de propagación de datos, no evidencia física independiente. La ficha de Contreras ya lo advierte; nuestros números lo confirman.

**Nivel:** *bien apoyado* como replicación descriptiva; *no independiente* como validación del emparejamiento con el tributo de 367 pesos (que la propia autora deja fuera).

### 3.5 V4. Correcciones de Thompson (2025): tres de cuatro se confirman; AS010 no

| Corrección | Comprobación en KFG | Veredicto |
|---|---|---|
| AS128: p170+p170s1 = 75; suma p177–p198 = 72 | p170 = 70; p170s1 = 5; 22 cuerdas p177–p198 suman 72 | **confirmado exacto** |
| AS115: 188+205+213 = 606; 266+225+245 = 736 | los seis valores existen (p13=188, p14=205, p15=213; p19/p21=266, p22=225, p23=245) | **confirmado** |
| AS044: total de grupo 248 (no 228) | el grupo 10 suma 248 exacto | **confirmado** |
| AS010: primeros 7 colgantes = 58 (no 51) | p1 = 33 y p1s1 = 18 → 51; los primeros 7 colgantes por número suman 87; 58 no aparece | **no confirmado** |

AS010 es el caso interesante: el KFG contiene exactamente el total 51 que Thompson señala como erróneo, y no contiene el 58 corregido. O bien la corrección no se propagó al KFG, o bien «primeros 7 colgantes» se refiere a otra agrupación que la ficha no precisa. Sin el documento completo no se puede decidir; se reporta como resultado negativo/parcial, no como refutación.

**Nivel:** *bien apoyado* para AS128, AS115 y AS044 (aritmética reproducible); *indeterminado* para AS010.

### 3.6 V5. ¿Son las cuerdas blancas marcadores de frontera de grupo?

Medrano y Khosla (2024) proponen que los colgantes blancos marcan límites de grupos de suma.

| | Cuerdas | % blancas (`W`) |
|---|---:|---:|
| Frontera de grupo (primera/última) | 10.932 | **29,4 %** |
| Interior del grupo | 27.993 | 22,4 % |

Diferencia agregada: +7,0 puntos. Como los quipus difieren en tamaño y en proporción de blancos, el estadístico primario es la media de las diferencias por quipu (cada quipu pesa igual): **+2,8 puntos**, nulo −0,02, p empírico = 0,0005 (596 quipus). Con la definición amplia (`W` en cualquier combinación) la diferencia agregada es 44,2 % vs 37,9 %.

El efecto existe y va en la dirección propuesta, pero es modesto: ~3 puntos por quipu. La explicación aburrida —los quipus suelen alternar color al inicio de grupo, y el blanco es el color más frecuente (12.537 cuerdas)— no se puede descartar con estos datos. Además, la propuesta original es sobre grupos *de suma*; aquí se prueba sobre todos los grupos, lo que diluye el efecto si solo aplica a grupos con total.

**Nivel:** *apoyado con datos* como asociación modesta; *propuesto* como convención semántica de límite.

### 3.7 V6. El «quipu más grande» y el par de Arica (exploratorio)

- AS069/KH0082, procedencia **Lluta Valley** (Arica), es el mayor del KFG por número de cuerdas: **1.831** (siguiente: UR093 con 1.227). Es consistente con «el quipu más grande registrado» de Thompson (2024), pero por *valor total* AS069 ocupa el puesto 93 (total 13.057), así que «más grande» depende de la métrica.
- Buscando un par numérico: UR131A (6.713) + UR131C (6.345) = 13.058, a una unidad del total de AS069 (13.057). Es tentador, pero hay 22 pares de quipus entre los 651 que caen a ±1 de 13.057 sobre 211.575 pares posibles; el hallazgo es consistente con un fenómeno de comparaciones múltiples y no se sostiene como evidencia.
- No se pudo identificar el segundo quipu del par de Thompson ni el «quipu resumen» de FitzPatrick (2026): la ficha de FitzPatrick no tiene texto, DOI ni ids.

**Nivel:** *especulativo*. No se usa como evidencia.

### 3.8 Verificaciones auxiliares

- **OKR:** 619 quipus, 54.403 cuerdas, 110.677 nudos. Coincide exactamente con Contreras (2026).
- **Cobertura de fibra:** el OKR solo tiene cuerda de nivel −1 (cordón principal) en 25 quipus; de 154 cordones principales, 79 son algodón (`CN`) y 75 no tienen fibra registrada. No hay ningún cordón principal con código `H` (cabello); `H` aparece en 226 cuerdas de nivel 1 en 3 quipus. Esto **apoya con matiz** la afirmación de Hyland et al. (2025) de que el OKR no registra sistemáticamente el material del cordón principal: el campo existe, pero la cobertura es mínima.
- **KH0631** no aparece en el KFG ni en el OKR del repo, de modo que la afirmación isotópica no es comprobable aquí.
- **Milillo (2024):** los 9 quipus con envoltorios no se pueden localizar de forma fiable; el campo no existe y `notas` no lo recoge de forma sistemática.

## 4. Controles, resultados negativos y explicaciones aburridas

1. **V1:** el 37 % de prevalencia no es principalmente señal: el nulo da 33,4 %. El exceso posicional es pequeño.
2. **V2:** el 74 % no se replica con definiciones estrictas (16,3 % observado). El enriquecimiento real es 1,5× sobre el nulo, no 74 %.
3. **V4:** AS010 no se confirma; el KFG conserva el valor 51 que la corrección dice erróneo.
4. **V3:** replicación exacta pero circular en la fuente (misma tradición de registro).
5. **V5:** efecto real pero pequeño; puede reflejar alternancia de color al inicio de grupo, no semántica.
6. **V6:** el «par numérico» de Arica es compatible con azar por comparaciones múltiples.
7. **Corrección múltiple:** Holm sobre V1, V2 y V5 (con las cuatro subpruebas de V2) deja el mayor p ajustado en 0,003; ninguna conclusión cambia.
8. **Resultados no comprobables:** 10/28 afirmaciones carecen de ids o variables; no se les asigna ningún nivel de evidencia empírica.

## 5. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Nudos inferiores en >20 % de los quipus | **apoyado con datos** (37,2 %; IC 33,5–40,9) |
| Los nudos inferiores son una anomalía posicional no explicada por la tasa base | **especulativo** (exceso de solo 3,8 pp sobre el nulo) |
| Ascher formulae ≥74 % | **no sostenido** con definición estricta; **propuesto** para la familia amplia de Medrano |
| Las sumas internas no son aleatorias | **apoyado con datos** (16,3 % vs 10,6 % nulo; p=0,0005) |
| Patrón recto/verso del Santa (49/51; 5 puros; KH0326 40/69) | **bien apoyado** (replicación exacta) |
| Correcciones AS128, AS115, AS044 | **bien apoyado** (aritmética exacta) |
| Corrección AS010 | **indeterminado / no confirmado** |
| Blancos como marcadores de frontera | **apoyado con datos** (+2,8 pp por quipu; p=0,0005), magnitud modesta |
| Cordón principal de KH0631 de cabello; artesano comunero | **no comprobable** en el repo (fuera del corpus) |
| OKR sin datos sistemáticos de cordón principal | **apoyado con datos**, con matiz (campo existe, cobertura 25/619) |
| Relación numérica AS069–par de Arica / FitzPatrick | **especulativo** |

## 6. Limitaciones

- El KFG no es el OKR: 651 vs 619 quipus y convenciones de decodificación distintas. Las replicaciones exactas (V3) muestran que comparten la tradición Harvard, lo que limita la independencia.
- Las definiciones operativas de «nudo inferior» y «fórmula de Ascher» son necesariamente más estrechas que las de los autores; un resultado negativo puede deberse a la operacionalización, no a la afirmación. Por eso se reporta como «no replicado con esta definición», no como refutación.
- No se usó la procedencia de museo como lugar de origen; AS069 se ubica por el campo `procedencia` (Lluta Valley), no por el museo.
- Los valores 0 sin nudos se trataron como ausentes en todas las sumas.
- El corpus está sesgado por el coleccionismo colonial (Contreras 2026); ninguna conclusión se generaliza al universo de quipus.

## 7. Para el coordinador

- Se inventariaron **28 afirmaciones** de las 12 fichas: **9 comprobables**, **9 parciales**, **10 no comprobables** con el repo. La literatura revisada es en gran parte no falsable con datos abiertos.
- **Hyland (2024) se sostiene en la cifra pero no en la interpretación:** 37,2 % de los quipus tienen un nudo inferior (IC 33,5–40,9; >20 % seguro), pero el nulo de permutación da 33,4 %. El exceso posicional es de solo ~3,8 puntos. No es una rareza, pero tampoco una anomalía fuerte.
- **El 74 % de Medrano y Khosla no se replica** con definiciones estrictas: 16,3 % de los quipus muestran alguna relación de suma de grupo, frente a 10,6 % del nulo (p=0,0005). Hay señal aritmética real (1,5×), pero la cifra estrella depende de una familia de fórmulas que el resumen no especifica. Pedir a los autores la definición operativa y la tasa base antes de usarla.
- **Contreras (2026) se replica exactamente** en el Santa: 49,0 % recto / 51,0 % verso, 5 quipus puros y UR090/KH0326 con 40 R / 69 V. Pero es la misma tradición de registro (KFG/OKR), así que no es validación independiente.
- **Tres de las cuatro correcciones numéricas de Thompson (2025) se confirman** en el KFG (AS128: 75 y 72; AS115: 606 y 736; AS044: 248). **AS010 no:** el KFG tiene 51 (el valor que ella corrige) y no tiene 58. Hay que resolverlo con la imagen del museo antes de propagar la corrección.
- **Los blancos como límite de grupo van en la dirección propuesta pero son un efecto pequeño:** 29,4 % en fronteras vs 22,4 % en interiores (agregado), +2,8 pp por quipu, p=0,0005. La explicación aburrida (alternancia de color al inicio de grupo) no está descartada.
- **El OKR sí tiene campo de fibra, pero casi no lo usa en cordones principales:** solo 25 quipus tienen cordón principal registrado, 75/154 sin fibra y ningún `H` (cabello) en nivel −1. La afirmación de Hyland et al. (2025) se sostiene con ese matiz; KH0631 no está en el corpus abierto.
- **Recomendación 1:** pedir a Medrano/Khosla la definición operativa de «Ascher formula» y reejecutar V2 con ella; es la única forma de saber si el 74 % es real o una definición laxa.
- **Recomendación 2:** no usar el «par numérico de Arica» (AS069 + UR131A/C, diferencia de 1) como evidencia: 22 pares de 211.575 caen a ±1 por azar. Si FitzPatrick no aparece con texto e ids, la afirmación debe quedar fuera del banco de criterios.
- **Recomendación 3:** el siguiente paso rentable es enriquecer el corpus con variables hoy ausentes (envoltorio del cordón principal, material, ids de museo corregidos) y repetir V1/V5 con la distinción entre grupos con y sin total, que es donde la hipótesis del blanco puede ser fuerte o desaparecer.
