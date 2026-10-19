# 26_clave_local: ¿clave de formulario propia del archivo, sin UR053 y sin etiquetas de color?

**Pregunta.** En 22_formularios, la parte positiva del modelo de formulario local («más acuerdo dentro del archivo que entre archivos») solo era significativa gracias a UR053A–E (sin ese juego, p = 0,135). Además, se comparaban etiquetas de color, que dependen del transcriptor. Aquí se repite la prueba con representaciones que no usan nombres de color, se excluye UR053 y se estratifica por investigador.

**Respuesta corta.**
- **Sin UR053, la clave local no se demuestra.**
  - Con la partición de color (R1), el acuerdo dentro del archivo es igual al de entre archivos: T = +0,015, p = 0,24. La potencia para detectar el efecto de 22 (22 % frente a 5 %) era ≈ 1,0.
  - El control positivo UR053 sí se detecta con la misma representación: 7 de 9 pares concuerdan, frente a una tasa base del 14 % (p = 0,0008). La prueba funciona; no hay otro archivo así.
- **Tampoco hay clave compartida entre archivos sin relación**, ahora que la representación permite comparar transcriptores distintos.
  - La concordancia en pares estrictamente no relacionados está en el nivel del azar (3,1 %, nulo 3,0 %).
  - Pero **la de dentro de archivo también** (3,7 %, nulo 3,1 %).
- **La partición de color es solo en parte invariante:**
  - entre transcriptores, ARI mediano 0,24 (0 sería el azar);
  - UR1107~UR237: ARI 0,26.

  Ascher separa LB/YB donde Urton escribe AB, y los dos agrupan las cuerdas de forma distinta.

## Archivos

| archivo | qué es |
|---|---|
| `diseno.md` | diseño congelado y potencia (§9), escritos antes de calcular acuerdos |
| `comun26.py` | representaciones R1, R2 y R3; partición de archivos; investigador; prueba por permutación. Autocomprobación: `python analisis/26_clave_local/comun26.py` |
| `estructura.py` | construye `patrones.csv` (patrones por quipu), `quipus26.csv` (R3) y `archivos26.csv` (archivo asignado); cuenta pares y calcula la potencia (`estructura.csv`, `salida_estructura.txt`) |
| `validacion.py` | validación de invariancia con pares de doble transcripción (`validacion.csv`, `salida_validacion.txt`) |
| `clave_local.py` | prueba principal, secundarias, control UR053, Incahuasi, detalle por archivo y refutación. Salidas: `pruebas.csv`, `archivos_detalle.csv`, `pares_concordancia.csv`, `refutacion26.csv`, `refutacion26_resumen.csv`, `salida_clave_local.txt` |

**Orden de ejecución**, desde la raíz:
1. `python analisis/26_clave_local/estructura.py`
2. `validacion.py`
3. `clave_local.py`

En Windows, `PYTHONIOENCODING=utf-8`.

## Desviaciones del diseño (declaradas)

1. **El control positivo excluía sus propios pares.** La regla «juegos con letra = no independientes» (§4) también quitaba los pares UR053A~E, así que en la primera corrida el control salió vacío (NaN). Para UR053 se levantó la exclusión; el par UR053B~C sigue fuera por ser copia. Esto no cambia la prueba principal, de la que UR053 está excluido.
2. **Análisis post hoc:**
   - sensibilidad de R2 quitando un par;
   - revisión de los pares concordantes uno por uno.
3. **Codificación de la consola** (UTF-8). Sin efecto.

## 1. Representación invariante y su validación

**Las tres representaciones:**
- **R1 (partición):** cada motivo de color contiguo se recodifica por orden de aparición (W|R|W → «ABA»). Por cada patrón y quipu se queda el motivo con menor p_col, y solo si p_col < 0,05.
- **R2 (posición):** grupos de exactamente k cuerdas. No usa color.
- **R3:** *bandas* (fracción de cambios de color que caen en frontera de grupo) y *cabecera* (fracción de grupos cuya 1.ª cuerda no tiene el color modal).

**Validación** con los pares transcritos dos veces de `14_copias` (copias y mismo objeto), sobre colgantes alineados.

| medida (13 pares con investigadores distintos) | resultado | nulo | p |
|---|---|---|---|
| etiqueta exacta | mediana 0,24 | — | — |
| **ARI de la partición** | **mediana 0,24**; supera al nulo en 8 de 9 | 0,00 | Wilcoxon **0,004** |
| kappa de «cambia el color» | mediana 0,00 | 0,00 | 0,16 |
| R1: el par concuerda (patrón + reparto) | 2 de 4 | 0,14 en pares al azar | 0,099 |
| R2: el par concuerda | 0 de 3 | 0,002 | 1 |
| R3 bandas, \|dif\| | 0,07 | 0,18 | 0,072 |
| R3 cabecera, \|dif\| | 0,28 | 0,33 | 0,20 |
| referencia: copias del **mismo** investigador | ARI 0,45; etiqueta 0,44 | | |

**UR1107 (Ascher) frente a UR237 (Urton), alineados en sentido inverso, 23 colgantes:**
- 0 de 23 etiquetas iguales.
- **ARI 0,26** (p = 0,043): la partición se recupera más que por azar, pero lejos de 1.
  - Ascher alterna LB/YB en cuerdas que Urton anota todas AB.
  - La de 800 es YB para uno y W para el otro.
- **Los grupos tampoco coinciden.** El grupo de 9 cuerdas de UR1107 (207, 131, 100, 30, 65, 18, 10, 10, 10) son 4 grupos en UR237. El de 7 (0, 34, 6, 101, 105, 215, 210) son 2.
- Ninguno de los dos tiene un formulario R1 ni R2 con p < 0,05, así que no se pueden comparar a nivel de quipu.

**Lectura.**
- R1 queda **validada solo por la cláusula de la partición** (ARI > nulo). A nivel de quipu (patrón + reparto) la evidencia es de 2 de 4, p = 0,099.
- **R2 y R3 no validan.** R2 no depende del vocabulario de color, pero sí de cómo cada transcriptor marca los grupos.
- **El transcriptor no solo nombra distinto: también discrimina y agrupa distinto.** La partición reduce el problema, pero no lo elimina.

## 2. Archivos y potencia

**Partición** (`archivos26.csv`), con una etiqueta por quipu y por prioridad:
1. Nazca/Berlín (UR1140, UR1136, UR223, HP056, UR234, UR1131);
2. Santa (UR087–092);
3. Puruchuco–Huaquerones;
4. Leymebamba;
5. Armatambo;
6. Pachacamac × museo;
7. Ica × museo;
8. Nazca × museo;
9. inventario consecutivo.

UR053 e Incahuasi quedan aparte. Se excluyen los pares de copias o del mismo objeto y los juegos con letra.

**Elegibles** (≥ 1 formulario con p < 0,05):
- R1: 149 quipus. Pares del mismo investigador dentro de archivo: AS 192, UR 122, HP 28.
- R2: 136 quipus.

**Potencia declarada** antes de correr (simulación con la estructura real de pares):

| R | p1 = 0,22 / p0 = 0,05 | p1 = 0,15 / p0 = 0,05 |
|---|---|---|
| R1 | 1,00 | 1,00 |
| R2 | 0,93 | 0,77 |

## 3. Prueba principal (mismo investigador, permutación de archivos dentro de investigador, B = 9 999)

| prueba | T | p | Holm (familia) | BH (todas) | dentro frente a entre, por investigador |
|---|---|---|---|---|---|
| **R1 incondicional** (primaria) | +0,015 | **0,24** | 0,24 | 0,36 | AS 0,135 frente a 0,135 · UR 0,148 frente a 0,117 · HP 0,107 frente a 0,053 |
| **R2 incondicional** (primaria) | +0,007 | **0,020** | **0,040** | 0,056 | AS 0,018 frente a 0,003 · UR 0 frente a 0,003 · HP 0 frente a 0 |
| R1 condicional (comparten patrón) | +0,011 | 0,33 | | 0,48 | |
| R1, k ≥ 3 (incondicional / condicional) | +0,006 / +0,013 | 0,20 / 0,26 | | 0,40 / 0,43 | UR, k ≥ 3, condicional: 0,075 (40) frente a 0,030 |
| R1 con estratos de investigadores cruzados | +0,012 | 0,27 | | | AS–UR 0,134 frente a 0,127 |
| R1, partición por sitio | +0,019 | 0,20 | | | |
| R1 **con** UR053 (referencia) | +0,025 | 0,14 | | | UR 0,191 frente a 0,135 |
| R2, k ≥ 3 / condicional / por sitio | | 0,009 / 0,049 / 0,031 | | 0,056–0,13 | |
| R2 con estratos cruzados | +0,003 | 0,090 | | | |
| R3 bandas | +0,060 | **0,0002** | 0,0024 (secundaria) | 0,005 | HP −0,11 frente a −0,29 · UR −0,21 frente a −0,27 · AS −0,245 frente a −0,258 |
| R3 cabecera | −0,004 | 0,59 | | | |

**Control positivo, UR053A–E como archivo:**
- R1: **7 de 9 pares concuerdan, frente a 0,136** (p = 0,0008; condicional p = 0,004);
- en el detalle por archivo es el **único** archivo que pasa BH (q = 0,024 entre 17).
- R2 no aplica: ningún quipu de UR053 tiene formulario posicional.

**Lectura.**
- **R1, sin UR053, no muestra clave local.**
  - Ascher está exactamente en el nulo (0,135 frente a 0,135, con 192 pares dentro).
  - Urton va en la dirección esperada, pero sin significación.
  - Con potencia ≈ 1 para el tamaño de efecto que sugerían las etiquetas, el negativo es informativo: no existe en otros archivos una clave «tipo UR053» que la partición pueda ver.
  - Límite: la partición es solo en parte invariante (ARI 0,24), y eso diluye un efecto real más débil.
- **R2 pasa Holm (0,040), pero se apoya en 2–3 pares:**
  - UR1109~UR1179 (P3) y UR1143~UR1149 (P4), los dos de Ascher, de Ica-Berlín;
  - UR268~UR275 (P5, Incahuasi; no entra en la principal).
  - Quitando un solo par, p ≈ 0,10 (post hoc).
  - Además, R2 no validó en los pares de doble transcripción.
  - Por la regla congelada no cuenta como «demostrada». Se califica **débil**.
- **R3 bandas:** los quipus del mismo archivo se parecen en dónde caen los cambios de color respecto a los grupos (Holm 0,0024).
  - Es un **estilo de archivo, no una clave de reparto**.
  - Lo empuja sobre todo HP (Pachacamac, museo de sitio).
  - No validó (p = 0,072), así que puede ser en parte un hábito del transcriptor por sesión.

## 4. Detalle por archivo (`archivos_detalle.csv`; cada archivo frente al resto de su investigador, B = 1 999)

| archivo | R | quipus | pares dentro | concuerdan | p | BH |
|---|---|---|---|---|---|---|
| UR053 (control) | R1 | 5 | 9 | 7 | 0,0015 | **0,024** |
| Leymebamba | R1 | 9 | 33 | 7 (AB × 6) | 0,09 | 0,65 |
| Puruchuco–Huaquerones | R1 | 10 | 43 | 6 | 0,29 | 0,84 |
| Ica-Berlín | R1 | 21 | 156 | 21 | 0,50 | 0,94 |
| Pachacamac-Berlín | R1 | 17 | 64 | 6 | 0,79 | 1 |
| Pachacamac, museo de sitio | R1 | 8 | 28 | 3 | 0,39 | 0,84 |
| Nazca/Berlín | R1 | 6 | 4 | 0 (mismo investigador) | 1 | 1 |
| Incahuasi | R2 | 19 | 108 | 1 | 0,022 | 0,28 |
| Ica-Berlín | R2 | 20 | 106 | 2 | 0,033 | 0,28 |

Santa: solo 2 quipus elegibles en R2 y 1 par.

**Pares concretos dentro de archivo que concuerdan con k ≥ 3** (`refutacion26.csv`, tipo = dentro, d ≤ d\*). Son candidatos, no demostraciones:
- **UR1143~UR1149** (Ica-Berlín): ABC con d = 0,36 y P4 con d = 0,43; p_col de 10⁻¹⁵ y 10⁻⁵. Es el mejor caso nuevo.
- **UR1136~UR223** (Nazca/Berlín, Ascher frente a Urton): AAB con d = 0,39. Es la «ficha» de Nazca, ahora comparable entre transcriptores.
- **UR063~UR068** (Puruchuco): ABCD con d = 0,41.
- UR004~UR006 (Leymebamba): ABA con d = 0,16.
- AS074~AS079 (inventario consecutivo): ABBC.
- AS160~UR1098 (Ica-Berlín): ABC.

## 5. Incahuasi (aparte)

- **R1:** dentro de Incahuasi concuerdan 6 de 102 pares Urton–Urton, frente a 10,4 % fuera (p = 0,87). Entre Urton y Clindaniel, dentro de Incahuasi, 4 de 45 (8,9 %) frente a 11,5 %. **No hay clave cromática compartida en Incahuasi a nivel de pares.**
- **R2:** p = 0,021, pero con 1 solo par (UR268~UR275, P5).
- Los P3/P9 de 22_formularios se confirmaron con una prueba de perfil medio del archivo, no con concordancia par a par con d ≤ 0,434. **Este resultado no los contradice**, pero indica que el formato de Incahuasi es una tendencia del archivo con mucha dispersión entre quipus, no una clave fija como la de UR053.

## 6. Refutación con la representación invariante (cualquier investigador)

Pares que comparten un patrón con k ≥ 3; concordancia = d ≤ d\* = 0,434; nulo = posiciones permutadas (2 000 réplicas).

| pares | R1: concuerdan / n (nulo, p) | R2 | criterio individual R1+R2 (nulo, p95) |
|---|---|---|---|
| dentro de archivo, sin UR053 | 8/216 = 3,7 % (6,7; 0,36) | 3/127 (0,9; 0,043) | 3 (3,1; 6) |
| **estrictamente no relacionados** | **44/1 418 = 3,1 % (42,0; 0,37)** | 5/764 (4,5; 0,47) | **22 (20,3; 27)** |
| … mismo investigador | 12/380 (10,5; 0,34) | 0/255 | 5 (5,4) |
| … **investigadores distintos** | 32/1 038 (31,6; 0,50) | 5/509 (2,3; 0,061) | 17 (14,8; 20) |

- **Regla (a)** (los estrictos superan su nulo y no son menos que los de dentro): no se cumple. R1: 3,1 % con p = 0,37.
- **Regla (b)** (≥ 3 pares con el criterio individual por encima del p95 del nulo): no se cumple. R1+R2: 22 frente a un p95 de 27.
- **La predicción de refutación no se cumple**, ahora también comparando entre transcriptores, que era la prueba justa.
- Los 22 pares estrictos que cumplen el criterio individual (ABC, ABB, AAB, ABA…) son los que se esperan por azar (20,3).
  - Incluyen AS075~MM001, AS178~UR1088, HP039~UR1121/UR1149, KH0049~UR1140 y UR208~UR269.
  - Ninguno se repite como sistema.
- **Lo nuevo:** con la partición, **el acuerdo dentro de archivo tampoco supera al azar**. Pasa a ser simétrico: no hay clave compartida y, salvo UR053 y algunos pares sueltos, tampoco una clave local detectable a nivel de pares.

## Para el coordinador

- **[demostrado, negativo con potencia]** Sin UR053, la clave local no aparece con la representación invariante (partición de color recodificada + reparto). Dentro frente a entre archivo, por investigador: T = +0,015, p = 0,24 (Holm 0,24). Ascher 0,135 frente a 0,135 (192 pares dentro), Urton 0,148 frente a 0,117, HP 0,107 frente a 0,053. La potencia declarada era 1,00 para el efecto de 22 sin UR053 (22 % frente a 5 %).
- **[demostrado]** La prueba sí detecta una clave local real: el control UR053A–E da 7 de 9 pares concordantes frente a una tasa base del 13,6 % (p = 0,0008). De 17 archivos, es el único con BH < 0,05 (q = 0,024). **La «clave de archivo» es, hoy, un rasgo de UR053, no un patrón general del corpus.**
- **[apoyado]** La invariancia es parcial.
  - Entre transcriptores, la partición de color coincide más que por azar (ARI mediano 0,24, frente a 0,45 entre copias del mismo transcriptor; Wilcoxon p = 0,004). Los cambios de color adyacentes no coinciden (kappa 0).
  - UR1107~UR237: 0 de 23 etiquetas iguales, ARI 0,26 (p = 0,043). Ascher separa LB/YB donde Urton pone AB, y los grupos también difieren (9 cuerdas = 4 grupos).
  - **El transcriptor discrimina y agrupa distinto, no solo nombra distinto.**
- **[débil]** La concordancia posicional (R2) pasa Holm (p = 0,020; Holm 0,040), pero descansa en 2 pares de Ascher de Ica-Berlín (UR1109~UR1179, UR1143~UR1149). Quitando uno, p ≈ 0,10. Además, R2 no validó en los pares de doble transcripción (0 de 3).
- **[demostrado como negativo de la refutación]** No hay clave compartida entre archivos sin relación, **ahora también entre transcriptores distintos**. En pares estrictos, R1 da 44/1 418 = 3,1 % (nulo 3,0 %; p = 0,37). Entre investigadores distintos, 32/1 038 (nulo 31,6). El criterio individual da 22 pares frente a 20,3 esperados (p95 27). Ni la regla (a) ni la (b) se cumplen.
- **[apoyado, cambio de lectura]** El acuerdo dentro de archivo, sin UR053, también está en el azar: 8/216 = 3,7 % frente a 3,1 %. La asimetría «local sí / compartida no» de 22_formularios desaparece fuera de UR053: los dos lados son nulos.
- **[apoyado: estilo, no clave]** Los quipus de un mismo archivo se parecen en *dónde* cambian de color respecto a los grupos (R3 bandas: p = 0,0002, Holm 0,0024). Lo empuja HP (Pachacamac, museo de sitio): |dif| 0,11 frente a 0,29. No validó entre transcriptores (p = 0,072). Puede ser un hábito de archivo o de transcripción.
- **[propuesto]** Candidatos concretos de clave compartida dentro de archivo:
  - UR1143~UR1149 (Ica-Berlín; ABC y P4, p_col 10⁻¹⁵);
  - UR1136~UR223 (ficha de Nazca, entre Ascher y Urton; AAB d = 0,39);
  - UR063~UR068 (Puruchuco; ABCD).

  Merecen el tratamiento de UR053 (exploración → confirmación a nivel de bloque), no un contraste de corpus.
- **[apoyado]** Incahuasi no muestra concordancia par a par de partición (6 de 102 Urton–Urton frente a 10,4 %; Urton–Clindaniel 4 de 45 frente a 11,5 %; p = 0,87). Sus formatos P3/P9 son tendencias del archivo con dispersión, no una clave fija.
- **Nivel recomendado para el modelo «formulario local»:**
  - «Sin clave compartida»: se mantiene y **se refuerza** (vale entre transcriptores).
  - «Clave propia del archivo»: **baja de apoyado a propuesto**. Solo se demuestra en UR053 (más pares sueltos). Con la partición, el resto de los archivos no se distingue del azar.
  - Límites: invariancia parcial (ARI 0,24); d\* heredado y estricto para k grande; los grupos dependen del transcriptor.
