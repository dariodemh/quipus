# Rehacer el núcleo de Incahuasi con la base OKR (`khipu.db`)

Carpeta: `analisis/ds/n_okr_incahuasi/`. Scripts: `01_tabla_okr.py`, `02_inventario.py`, `03_pruebas.py`, `04_nuevas.py`, `lib_okr.py`. Salidas: `cuerdas_okr.csv`, `inventario_incahuasi.csv`, `detalle_nuevas.csv`, `pruebas_kfg.csv`, `pruebas_okr.csv`, `detalle_t1_*.csv`, `detalle_t3_*.csv`, `nuevas_pruebas.csv`, `salida_03_*.txt`. Semilla 4218/4219. No se modificó nada fuera de esta carpeta.

## 0. Resumen

1. **La tabla OKR se puede construir y reproduce KFG.** 52/52 quipus de Incahuasi cruzados por `puente.csv`; 5 732 cuerdas OKR frente a 5 624 de KFG. Los recuentos de colgantes coinciden en 51/52 quipus y las sumas por grupo son idénticas en 733/772 grupos (95 %); los 39 grupos con diferencia están en 5 quipus y se explican por cuerdas nuevas o por una reasignación de nivel en UR255, no por errores de construcción.
2. **KFG pierde 111 cuerdas en Incahuasi**, no solo 32: 58 subsidiarias en UR256, 32 en UR274B, 11 en UR265, 4 en UR255, 2 en UR264 y 4 en UR280. Además KFG no ve 7 marcadoras (6 en UR274B, 1 en UR264) y 3 cuerdas que marca como rosas son datos en OKR. En Incahuasi hay **1 sola cuerda superior T** (UR255 p36), no 95: el dato de 92/95 es del corpus, no de este archivo.
3. **Las cinco pruebas centrales se mantienen**, con las mismas cifras y prácticamente los mismos p: 8/18 sumas A+B, 5 grupos de UR270 con ≥6 columnas en UR278, 12/33 totales de UR278 en UR266 (τ = 1), 6/26 sumas UR267A+B en UR269, y cuota 17 en UR274B (3/20 neto; 10/20 explícito). De las relaciones aritméticas centrales, ninguna se refuerza de forma material; una (UR274A+UR274B) mejora pero sigue sin significación. La cuota 17 se trata aparte en el punto 5.
4. **Las cuerdas recuperadas no crean relaciones aritméticas nuevas.** Una búsqueda dirigida de 8 pruebas (valores nuevos contra el consolidado, UR270, UR278, cuotas, UR267B y UR255) no deja ninguna con q < 0,05; la mejor es «valores nuevos de UR274B en el conjunto de cuotas» (6/21 frente a 3,5; p = 0,031; q = 0,25).
5. **Lo único que cambia de forma útil es el nulo de la cuota 17 explícita en UR274B**: el recuento observado no cambia (10), pero al incorporar las 32 subsidiarias el nulo baja de 7,9 a 5,9 y el p pasa de 0,086 (KFG) a 0,004 (OKR; q = 0,012). Es una mejora real de poder estadístico, no evidencia nueva: las 12 cuerdas «17» ya estaban en KFG.

## 1. Pregunta

¿Se sostienen las relaciones centrales del sistema contable de Incahuasi si se reconstruyen con la base OKR, que conserva cuerdas que KFG pierde (subsidiarias de UR274B/UR256, marcadoras y superiores), y aparecen relaciones nuevas gracias a esas cuerdas?

## 2. Método

### 2.1 Esquema de `khipu.db` y correspondencia con KFG

Tablas usadas: `cord` (jerarquía y unión), `knot` (nudos), `ascher_cord_color` (color), `khipu_main` (identidad). Campos clave:

| KFG | OKR | Regla |
|---|---|---|
| `kfg` | `puente.csv → khipu_id` | 52/52 con id; `khipu_main.INVESTIGATOR_NUM` lo confirma |
| `nivel` | `CORD_LEVEL − 1` | nivel 0 = colgante; −1/−2/−3 son cordón principal y anexos (excluidos) |
| `padre` | `PENDANT_FROM` | para nivel 1 el padre es el cordón principal (id fuera de `cord`) |
| `grupo` | `CLUSTER_ID` | índice del clúster del colgante ordenado por `CORD_ORDINAL`; las subsidiarias heredan el grupo de su colgante |
| `orden` | DFS por `CORD_ORDINAL` | madre seguida de sus hijas, como KFG |
| `cuerda` | `p{CORD_ORDINAL}`, `p…s1`, `p…s1s1` | numeración propia; validada contra el nombre KFG |
| `valor` | `Σ knot.knot_value_type` | en OKR el tipo de nudo ya trae el valor de posición (1000, 100, 10, 1) y el nº de vueltas del nudo largo |
| `pres` | `≥1 nudo` | 0 sin nudos = ausente, igual que el brief |
| `color` | `FULL_COLOR` | si hay varias filas por cuerda se toma la primera (`color_id`) |
| `union` | `ATTACHMENT_TYPE` | R/V/T/U |
| separador (PK) | `CORD_CLASSIFICATION = 'M'` | marcadora; se fuerza color `PK` para que `lib18.registros` la trate igual que KFG |

Decisiones que afectan a las pruebas:

- **Separador = marcadora M**, no color rosa. En OKR solo hay 52 M en Incahuasi y 48 cuerdas nivel 0 con color PK en KFG; 7 marcadoras (UR264, UR274B) son nuevas y 3 PK de KFG son datos en OKR (UR266 p106/p108, UR274A p69). Usar el color habría dejado fuera las 6 marcadoras de UR274B, que es justo la parte recuperada.
- **Jerarquía aplanada.** OKR cuelga directamente del colgante cuerdas que KFG pone dos o tres niveles más abajo (p. ej. KFG `p101s1s3` = OKR `p101s3`). El grupo y el valor no cambian; sí cambian `nivel` y `padre`. Para «primera subsidiaria» se usa la primera hija por `CORD_ORDINAL`, que coincide con la `s1` de KFG (validado porque la prueba UR270→UR278 da exactamente el mismo resultado).
- **Alineación.** Registro = grupo no separador; cabecera = primer colgante anudado (definición congelada de 13/18). Se alinea por número de grupo, sin saltar grupos vacíos, y se exige que ambos registros tengan cabecera. Los grupos de registro son **idénticos** KFG vs OKR en todos los quipus de las pruebas (UR273A 29, UR273B 27, UR274A 26, UR267A/B 26, UR270 21, UR278 36, UR266 33, UR269 91), de modo que la alineación es la misma que en 13. La única excepción es UR274B: OKR tiene 27 registros (33 grupos − 6 marcadoras) frente a 33 grupos de KFG, pero en ambos casos solo 24 tienen cabecera, y los pares efectivos son los mismos.

### 2.2 Validación de la tabla

- Nivel 0: 3 759 en OKR vs 3 762 en KFG. La diferencia está solo en UR255, y no es pérdida: las 3 cuerdas que KFG cuenta como colgantes (p81=25, p82=10, p86=26) son en OKR subsidiarias de p36, p64 y p73 (valores 25, 10 y 26). UR255 pasa de 89 a 90 cuerdas (+4 subsidiarias, −3 colgantes reasignados).
- Sumas por grupo: idénticas en 733 de 772 grupos. Las diferencias están en 5 quipus y son exactamente el valor de las cuerdas nuevas: UR256 (+3 357), UR274B (+3 700), UR265 (+40), UR255 (+16, neto de la reasignación) y JC005 (+5, una cuerda con valor distinto).
- Valores: idénticos cuerda a cuerda salvo JC005 (0→5) y los desplazamientos de UR255 por la reasignación anterior. No hay ningún caso de valor perdido.
- La tabla completa tiene 54 171 cuerdas en 605 quipus con `kfg`; sirve también de pool para los nulos.

## 3. Inventario de diferencias KFG vs OKR en Incahuasi

| Concepto | KFG | OKR | Diferencia |
|---|---|---|---|
| Cuerdas totales | 5 624 | 5 732 | **+108** |
| Colgantes (nivel 0) | 3 762 | 3 759 | −3 (reasignadas, no perdidas) |
| Subsidiarias | 1 862 | 1 973 | +111 |
| Marcadoras visibles | 48 PK nivel 0 | 52 M | +7 nuevas, −3 PK que son datos |
| Cuerdas superiores T | 0 | 1 | UR255 p36 (valor 0, unión R) |
| Suma de todos los valores | 1 726 633 | 1 733 751 | +7 118 |

Cuerdas nuevas por quipu (las 111 subsidiarias que KFG no tiene):

| Quipu | Nuevas | Valores (anudadas) |
|---|---|---|
| UR256 | 58 | 171, 35, 200, 41, 10, 220, 60, 100, 130, 6, 65, 5, 47, 111, 16, 23, 1, 14, 10, 5, 17, 42, 18, 29, 13, 22, 5, 29, 17, 32, 5, 9, 69, 47, 7, 30, 305, 50, 297, 155, 623, 201… |
| UR274B | 32 | 121, 2, 167, 1080, 46, 10, 40, 867, 122, 10, 10, 173, 3, 23, 47, 111, 15, 5, 235, 130, 483 |
| UR265 | 11 | 7, 3, 3, 2, 3, 4, 4, 6, 5, 3 |
| UR255 | 4 | 25, 26, 10, 16 (las 3 primeras, reasignadas desde colgantes) |
| UR264 | 2 | 0, 0 |
| UR280 | 4 | todas en blanco (la suma del quipu no cambia: 6 880 en ambas bases); el resto de la diferencia de UR280 es renombrado jerárquico |

Ninguna cuerda física de KFG falta en OKR: las 3 de UR255 que aparecen como «solo KFG» son las que OKR reasigna a subsidiarias, y el resto de las diferencias de nombre (UR262, UR270, JC010…) es el aplanamiento jerárquico. **UR255 es el único quipu donde OKR tiene menos colgantes que KFG**; no es una pérdida de datos.

## 4. Pruebas centrales con OKR

Mismo código y mismas definiciones para KFG y OKR (`03_pruebas.py kfg` / `03_pruebas.py okr`), de modo que la comparación es exacta. Nulo de permutación con semilla fija; 10 000 réplicas (5 000 en UR278 y cuota 17).

| Prueba | KFG | OKR | Nulo OKR (media/máx) | p OKR | Holm |
|---|---|---|---|---|---|
| UR273A+UR273B → UR266+UR275+UR269 | 8/18 | **8/18** | 1,26 / 6 | 1·10⁻⁴ | 0,0007 |
| UR273A+UR273B → UR266+UR275 | 7/18 | **7/18** | 0,95 / 5 | 1·10⁻⁴ | — |
| UR274A+UR273B → UR266+UR275 | 6/17 | **6/17** | 1,00 / 6 | 2·10⁻⁴ | — |
| UR274A+UR274B → UR266+UR275 | 1/15 | **3/19** | 1,47 / 7 | 0,17 | — |
| UR270 P+S1 → UR278: grupos con ≥6 columnas | 5/12 | **5/12** | 0,001 / 1 | 2·10⁻⁴ | 0,0008 |
| UR270 P+S1 → UR278: aciertos totales | 51 | **51** | 12,9 / 21 | 2·10⁻⁴ | — |
| UR270 solo P → UR278 (control) | 0 grupos | **0 grupos** | — | — | — |
| UR278 totales de grupo → UR266 | 12/33 | **12/33** | 0,73 / 6 | 1·10⁻⁴ | 0,0007 |
| UR278 totales de grupo → UR275 | 7/33 | **7/33** | 0,85 / 6 | 1·10⁻⁴ | 0,0007 |
| UR267A+B → UR269 (todas las cuerdas) | 6/26 | **6/26** | 1,37 / 7 | 0,0013 | 0,0021 |
| UR267A+B → cabeceras de UR269 | 5/26 | **5/26** | 0,71 / 5 | 0,0009 | 0,0021 |
| UR269 cuota 25: cabecera = UR267A+B | 3/6 | **3/6** | 0,19 / 3 | 0,0007 | 0,0021 |
| UR274B: registros con neto x−17 | 3/19 | **3/20** | 0,17 / 3 | 4·10⁻⁴ | q = 0,0024 |
| UR274B: 17 explícito tras la cabecera | 10/19 | **10/20** | 5,92 / 11 | 0,004 | q = 0,012 |
| UR273B: 17 explícito tras la cabecera | 3/6 | **3/6** | 2,11 / 3 | 0,28 | q = 0,56 |
| UR273B: registros con neto x−17 | 0/6 | **0/6** | 0,00 | 1 | 1 |

Lectura:

- **UR273A+B**: las 8 sumas exactas son las mismas de 13 (g3: 808+2142=2950; g9: 453+1200=1653; g11: 448+1289=1737; g12: 502+1325=1827; g13: 448+1332=1780; g17: 672+1575=2247; g18: 509+1256=1765; g19: 325+1181=1506). Con OKR **no se pierde ninguna**; la única que cae al restringir el destino a UR266+UR275 es g12, que solo está en UR269.
- **UR270→UR278**: 5 grupos con ≥6 columnas (g0→fila 21, 9/9; g4→25, 9/9; g5→26, 7/9; g8→27, 8/9; g9→28, 6/9) y 51 aciertos. Idéntico a KFG. El control con solo colgantes da 0 grupos.
- **UR278→UR266**: 12 totales exactos de 33 filas, τ = 1 con 10 pares ordenados; a UR275, 7 exactos y τ = 1 con 6 pares.
- **UR267A+B→UR269**: 6/26 sumas en cualquier cuerda de UR269 y 5/26 en cabeceras; 3/6 de las cabeceras con cuota 25. Se mantiene, con p ligeramente mejor que en KFG (0,0013 frente a 0,0018), sin cambio de recuento.
- **Cuota 17**: UR274B sigue siendo el único quipu con apoyo (3 netos y 10 explícitos); UR273B no tiene ningún neto x−17 y sus 3 «17» explícitos no superan el nulo (p = 0,28). **La asimetría 274B/273B se mantiene.**
- **Cuota 47 = 30 + 17**: no cambia. El 47 aparece (como cuerda o como neto x−47) en 23/28 registros de UR266, 24/25 de UR275 y 8/67 de UR269, idéntico a KFG. El 25 aparece en 0/28, 0/25 y 6/67.

### 4.1 Veredicto por relación

| Relación | Veredicto con OKR | Cifra |
|---|---|---|
| UR273A + UR273B → UR266/UR275/UR269 | **se mantiene** | 8/18 exactas; idénticas a KFG; p = 1·10⁻⁴ |
| UR274A + UR273B → UR266/UR275 | **se mantiene** | 6/17; idénticas a KFG; p = 2·10⁻⁴ |
| UR270 P+S1 → filas de UR278 | **se mantiene** | 5 grupos con ≥6 columnas, 51 aciertos; p = 2·10⁻⁴ |
| UR278 totales → UR266 | **se mantiene** | 12/33, τ = 1; p = 1·10⁻⁴ |
| UR278 totales → UR275 | **se mantiene** | 7/33, τ = 1; p = 1·10⁻⁴ |
| UR267A + UR267B → UR269 | **se mantiene** (p algo mejor) | 6/26; p = 0,0013 (KFG 0,0018) |
| UR269 cuota 25 = UR267A+B | **se mantiene** | 3/6; p = 7·10⁻⁴ |
| Cuota 17 en UR274B (neta) | **se mantiene** | 3/20; p = 4·10⁻⁴; q = 0,0024 |
| Cuota 17 en UR274B (explícita) | **se refuerza en el control** | 10/20; p 0,086 → 0,004; q = 0,012 |
| Cuota 17 en UR273B | **se mantiene negativo** | 0/6 netos; 3/6 explícitos, p = 0,28 |
| UR274A + UR274B → consolidado | **se debilita el negativo, no llega** | 3/19; p = 0,17 |
| Nivel superior (T) | **negativo** | 1 sola T en Incahuasi, valor 0 |
| Relaciones nuevas con cuerdas recuperadas | **ninguna** | 8 pruebas, q ≥ 0,25 |

## 5. ¿Relaciones nuevas gracias a las cuerdas perdidas?

Universo conservador: las **107 subsidiarias** de los 5 quipus en que KFG no registró ninguna subsidiaria (UR256 58, UR274B 32, UR265 11, UR255 4, UR264 2); 81 están anudadas. Quedan fuera las 4 de UR280, que están en blanco y no tienen efecto aritmético. Nulo: cada valor nuevo se sustituye por uno de los 40 valores más cercanos en escala log del pool de cuerdas anudadas de Incahuasi que no son nuevas (el nulo de magnitud de 13). 10 000 réplicas; BH sobre 8 pruebas.

| Prueba dirigida | Obs. | Nulo | p | q (BH) |
|---|---|---|---|---|
| UR274B nuevas → consolidado (UR266+275+269) | 13/21 | 10,75 | 0,158 | 0,42 |
| UR256 nuevas → consolidado | 25/46 | 23,56 | 0,357 | 0,70 |
| UR274B nuevas → UR270 | 9/21 | 12,26 | 0,990 | 0,99 |
| UR274B nuevas → UR278 | 10/21 | 12,10 | 0,960 | 0,99 |
| **UR274B nuevas → cuotas {10,15,17,25,30,46,47,208}** | **6/21** | **3,48** | **0,031** | **0,25** |
| UR256 nuevas → UR267B | 19/46 | 15,73 | 0,115 | 0,42 |
| UR256 nuevas → UR255 | 8/46 | 7,82 | 0,558 | 0,74 |
| UR274B cabecera + nuevas del registro → consolidado | 5/24 | 4,33 | 0,439 | 0,70 |

**Ninguna sobrevive a la corrección múltiple.** La única sugerente (6 valores nuevos de UR274B en el conjunto de cuotas) se explica por densidad: los valores nuevos incluyen 10, 10, 10, 15, 46 y 47, y ese conjunto de cuotas está formado por números pequeños y frecuentes; con el nulo de magnitud queda en q = 0,25.

Otras comprobaciones dirigidas, todas negativas:

- **UR274A + UR274B → consolidado**: mejora de 1/15 (KFG) a 3/19 (OKR), pero el nulo es 1,47 y p = 0,17. No es una relación nueva, solo deja de ser un negativo plano.
- **Cuota 17 explícita**: la observación no cambia (10), pero el nulo baja de 7,92 a 5,92 porque las 32 subsidiarias ocupan posiciones que antes quedaban vacías. p = 0,086 → 0,004. **Las 12 cuerdas «17» son todas colgantes antiguas: no hay ni una cuota 17 entre las cuerdas recuperadas.**
- **UR274B ↔ UR273B**: con las 6 marcadoras, UR274B queda en 27 registros, los mismos que UR273B. La comparación por registros muestra una racha de 3 exactos + 1 ±10 en los registros 1-5 con desfase +1, pero **KFG ya la tiene** (racha de 5 con desfase +2, porque sus registros en blanco desplazan el índice). No es una relación nueva; solo cambia el desfase.
- **Marcadoras como fronteras**: UR273A y UR273B tienen marcadoras en los mismos índices de registro [10, 13, 14, 20, 23]. UR274A [4, 5, 7, 10, 19] y UR274B [4, 5, 6, 11, 13, 22] solo comparten las dos primeras: **la partición de UR274B no coincide con la de UR274A**, a diferencia de la pareja 273. Eso explica que la alineación registro a registro 274A/274B siga siendo mala.
- **Superiores**: en Incahuasi solo hay 1 cuerda T (UR255 p36, valor 0, sin nudos). No hay ningún nivel superior que KFG hubiera perdido en este archivo. El dato 92/95 es del corpus (UR087, UR119, etc.), no de Incahuasi; **cualquier conclusión sobre superiores en Incahuasi es negativa**.
- **UR256**: sus 58 subsidiarias recuperadas no la alinean con UR267B (19/46 valores en común; p = 0,11) ni con UR255 (8/46; p = 0,56). Sigue siendo un libro de correcciones, no una copia limpia.

## 6. Controles

- **Nulo explícito en todas las pruebas.** A+B: barajar B entre registros (conserva marginales y rompe solo el emparejamiento). UR270→UR278: permutar las sumas P+S dentro del grupo (nulo 1) y permutar S entre colgantes (nulo 2); control con solo P. UR278→UR266: permutar los valores de nivel 0 dentro de UR278 (conserva tamaños de grupo). UR267A+B: barajar B; dirigido a cuota 25: barajar B. Cuota 17: barajar las cuerdas no cabecera entre registros. Valores nuevos: nulo de magnitud (40 vecinos en log).
- **p empírico** con el estimador (éxitos + 1)/(B + 1); p mínimo 1·10⁻⁴ con 10 000 réplicas.
- **Corrección múltiple.** Holm sobre las 7 pruebas principales (todas q ≤ 0,0021). BH sobre las 8 de cuota 17 (q = 0,0024 y 0,012 para UR274B; q = 0,56 para UR273B). BH sobre las 8 de cuerdas nuevas (ninguna q < 0,05).
- **Control de pipeline.** El mismo script ejecutado sobre KFG reproduce exactamente las cifras y los p de 13/18 (diferencia 0 en 16 de 18 pruebas). Eso descarta que los cambios se deban al código.
- **Control de alineación.** Los números de grupo usados en cada par son idénticos KFG vs OKR; la única diferencia estructural es UR274B (marcadoras), y sus 24 cabeceras efectivas son las mismas.
- **Control de magnitud y densidad** en la búsqueda de valores nuevos (el nulo de 13), que es lo que hace caer el único candidato a q = 0,25.
- **Control negativo** UR270 solo P → UR278: 0 grupos con ≥6 columnas, como en 13.

## 7. Resultados negativos

- Ninguna relación aritmética nueva con las 107 cuerdas recuperadas (8 pruebas, q ≥ 0,25).
- UR274A+UR274B → consolidado sigue sin significación (3/19; p = 0,17).
- UR256 no se alinea con UR267B ni con UR255 gracias a sus 58 subsidiarias.
- Las marcadoras de UR274B no reproducen la partición de UR274A (solo 2 de 5 posiciones).
- No hay ninguna cuerda superior nueva en Incahuasi: 1 T en total, sin valor.
- La cuota 17 neta no aparece en UR273B (0/6) ni en UR274A (0/15); la asimetría entre copias se mantiene.
- Los valores 46 y 47 de UR274B (p15s2, p34s3) no cierran ninguna identidad aritmética del registro: no son cuotas explícitas ni netos.
- Las 3 cuerdas que OKR tiene de menos como colgantes en UR255 no son pérdidas, pero obligan a no usar UR255 como copia exacta de UR267A sin corregir el nivel.

## 8. Niveles de evidencia

- **Bien apoyado (campos directos, sin inferencia):**
  - La tabla OKR reproduce KFG: colgantes y sumas por grupo idénticos salvo las diferencias inventariadas.
  - KFG pierde 111 cuerdas en Incahuasi (107 analizadas + 4 de UR280) y 7 marcadoras; OKR no pierde ninguna cuerda salvo la reasignación de nivel de UR255.
  - En Incahuasi hay 1 sola cuerda superior T, no 95.
  - Las 8 sumas A+B, los 5 grupos de UR270, los 12 totales de UR278 y las 6 sumas de UR267A+B son exactamente las mismas en OKR que en KFG.
- **Apoyado con datos:**
  - Que las relaciones centrales sobreviven a la sustitución de base (todas con Holm ≤ 0,0021).
  - Que la cuota 17 explícita de UR274B gana poder estadístico con las cuerdas recuperadas (p 0,086 → 0,004; q = 0,012), aunque la observación sea la misma.
  - Que las cuerdas recuperadas no aportan relaciones nuevas (8 pruebas corregidas, todas negativas).
- **Propuesto:**
  - Leer el 46 y el 47 de UR274B como «cuotas escritas en subsidiarias» y no como partidas. Encajan en el conjunto de cuotas, pero el nulo de magnitud no lo certifica (q = 0,25).
  - Que la partición de UR274B por marcadoras sea la correcta y la de KFG (33 grupos) una fusión de registros.
- **Especulativo:**
  - Que las 58 subsidiarias de UR256 sean el detalle de las correcciones de UR267B. Los valores no cuadran registro a registro.
  - Cualquier lectura de las 6 marcadoras de UR274B como «periodos» distintos de los de UR274A.

## 9. Para el coordinador

- **La base OKR no cambia el núcleo: lo confirma.** Las cinco pruebas centrales dan las mismas cifras que KFG y los mismos p (Holm ≤ 0,0021). El sistema contable de Incahuasi no era un artefacto de la codificación KFG.
- **KFG pierde más de lo que decía el brief en Incahuasi: 111 cuerdas, no 32.** UR256 (+58), UR274B (+32), UR265 (+11), UR255 (+4), UR264 (+2), UR280 (+4). Además KFG no ve 7 marcadoras (6 en UR274B) y 3 cuerdas rosas que en OKR son datos.
- **El dato de «92/95 superiores» no aplica a Incahuasi.** Aquí hay una sola cuerda T (UR255 p36, valor 0). Las superiores perdidas están en UR087, UR119, HP047, etc.; para Incahuasi el argumento de las superiores es negativo.
- **La cuota 17 se refuerza solo en el control, no en la observación.** UR274B: 3/20 netos x−17 (p = 0,0004) y 10/20 «17» explícitos; el p de estos últimos pasa de 0,086 (KFG) a 0,004 (OKR) porque las 32 subsidiarias recuperadas llenan posiciones que antes quedaban vacías. Las 12 cuerdas «17» son antiguas: no hay ninguna cuota entre las cuerdas nuevas.
- **UR273B sigue sin apoyo para la cuota 17** (0/6 netos; 3/6 explícitos, p = 0,28). La tesis 30 + 17 = 47 sigue dependiendo de UR274B, no de la pareja.
- **Ninguna relación nueva sobrevive.** Ocho pruebas dirigidas con nulo de magnitud y BH: la mejor es «valores nuevos de UR274B en el conjunto de cuotas» (6/21 frente a 3,5; p = 0,031; q = 0,25). Los valores 46 y 47 están ahí, pero el nulo de densidad los absorbe.
- **UR274A + UR274B mejora de 1/15 a 3/19, pero no llega** (p = 0,17). Las marcadoras de UR274B no reproducen la partición de UR274A (solo 2 de 5 posiciones), así que la alineación registro a registro sigue sin base estructural.
- **Recomendación 1:** usar OKR como base para Incahuasi y conservar KFG solo como control. La tabla `cuerdas_okr.csv` ya está construida y validada; no hay que rehacerla.
- **Recomendación 2:** el siguiente paso rentable no son las cuerdas nuevas, sino la relectura del objeto: UR255 (3 colgantes reasignados), UR274B (6 marcadoras y 32 subsidiarias) y UR266 p104 (valor 1737 reimportado en 2020). Con eso se decide si las diferencias son de codificación o del quipucamayoc.
- **Recomendación 3:** no corregir por «superiores» en Incahuasi; sí hacerlo en el resto del corpus, donde D5 sigue siendo el hallazgo más sólido (92/95 T y 502/502 marcadoras perdidas).
