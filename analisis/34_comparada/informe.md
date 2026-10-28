# Contabilidad comparada: protocuneiforme, Lineal B y quipus

*18-10-2026. Carpeta `analisis/34_comparada/`. Niveles: bien apoyado / apoyado / propuesto / especulativo. Literatura: la búsqueda web fue escasa; lo de Uruk y Pilos viene sobre todo de conocimiento previo de la literatura citada, sin página verificada (se marca). Solo se verificó por la web que existen: Englund 2011 («Accounting in proto-cuneiform», en Radner y Robson, *Oxford Handbook of Cuneiform Culture*), Englund 2005 (CDLJ 2005:1, «Unusual Accounting Practices in Archaic Mesopotamian Tablets») y Killen 1984 («Last year's debts on the Pylos Ma Tablets», SMEA 25: 173–188).*

## A. Pallariforme (detalle en `pallariforme.md`)
Larco Hoyle (1942–43) propuso escritura sobre pallares mochicas; los contemporáneos la rechazaron (fichas rituales o de juego); no hay datos tabulados abiertos ni relación demostrable con quipus. **Especulativo; sin relación con quipus.** No seguir.

## B1. Rasgos estructurales (literatura)
**Protocuneiforme** (versión corregida tras leer la fuente primaria; ver «Verificación con Archaic Bookkeeping»; NDE1993 = Nissen, Damerow y Englund 1993, *Archaic Bookkeeping*, Univ. of Chicago Press; páginas impresas): casi 5000 tablillas y fragmentos de Uruk (Uruk IV–III), en su gran mayoría administrativas (pp. ix, 21). Unos 60 signos numéricos entre ~1200 signos (p. 25). Cinco sistemas principales (sexagesimal S, bisexagesimal B, SE de capacidad de cereal, GAN2 de superficie, EN de función desconocida) más derivados y el sistema U4 de tiempo (pp. 27–28); el mismo signo vale distinto según el sistema (pp. 26–27). Tablillas con partidas en el anverso y suma en el reverso (p. 20), pero también tablillas sin suma y totales que no son la suma aritmética (pp. 21, 35). Formato de tablilla propio de cada tipo de transacción (p. 30). Copias solo de listas léxicas (pp. 24, 106), no de cuentas. *Tasa de error: los autores no dan tasas, solo casos (ver verificación).* Correcciones respecto de la primera versión: no hay un sistema de calendario «E» (el tiempo es U4; EN es desconocido), las razones SE son 5, 6, 10, 3, 10 (p. 37), y no hay borradores de cuentas arcaicas documentados.

**Lineal B** (Pilos; Killen 1984; Shelmerdine, capítulo de tasación en *New Documents in Mycenaean Greek*; Palaima sobre manos de escriba; sin página verificada): series con formato de fórmula (Ma, Jn, Fr), ideogramas de producto más numerales decimales, líneas de total (*to-so*), y en Ma la distinción tasado / entregado (*a-pu-do-si*) / adeudado (*o-pe-ro*), con «deudas del año pasado» (Killen 1984). Varias manos de escriba reconocibles.

## B2. Tabla comparada
Ver `rasgos_comparados.csv` (10 rasgos, con tipo de paralelo, nivel y páginas de NDE1993; actualizada en la segunda ronda).
- **Paralelos reales:** jerarquía en niveles (Incahuasi 3–4, Uruk 2–3); formato fijo por documento; copias; numerales leídos antes que los productos.
- **Analogías débiles:** cuadre por dos caminos (solo Incahuasi, propuesto); posición de totales (el protocuneiforme al final o reverso, Incahuasi primero); metrologías por producto (hay heterogeneidad de perfil, no bases distintas bien apoyadas); cuota (los quipus restan, Pilos compara tres columnas); signo de producto (los quipus no lo tienen).

## B3. Predicciones y pruebas
Diseño escrito antes de correr: `diseno_previo.md`. Código con semilla 20261018: `pruebas.py` (salida `resultados_pruebas.csv`; 5000 permutaciones; Holm sobre 7 pruebas) y `sensibilidad.py` (fuera de la familia).

| Prueba | Predicción | Resultado | p Holm | Nivel |
|---|---|---|---|---|
| P1a dígito de unidades por archivo | base 10 universal: sin diferencia | **Difiere** (chi2=1340, 11 archivos, 493 quipus); proporción de 0 entre 0,08 (Paracas) y 0,39 (Ica) en valores ≥10 | 0,003 | apoyado (heterogeneidad); causa propuesta |
| P1b ídem por género | ídem | **Difiere** (chi2=1950, 626 quipus) | 0,0014 | apoyado |
| P2a total en primera posición | exceso | 101/168 (esperado 49,8) | 0,0014 | solo Incahuasi (abajo) |
| P2b total en última | exceso (predicción cuneiforme) | 25/168 (esperado 49,8): déficit | 1 | rechazado |
| P2c primero−último, SUM vs resto | depende del género | dif −0,47 con solo 3 quipus SUM | 0,82 | sin potencia |
| P3 discrepancia UR278→UR266 | errores de un dígito | 24 filas: 11 exactas; 13 fallan (0,54; IC95 % aprox. 0,35–0,72); 7/13 de un solo dígito decimal. Nulo (celdas permutadas): 0,23 exactas y 5,6 de un dígito | 0,0014 | apoyado |
| P4 déficit tipo o-pe-ro (cuota = suma de dos entregas) | exceso | 13 grupos vs 10,8 esperado | 0,70 | negativo |

Lecturas:
- **P1.** Las posiciones son decimales casi siempre (de ~63 000 nudos S, unos 30 tienen posición que no es potencia de 10; probable error de transcripción). Lo que difiere por archivo y género es el perfil de dígitos: Leymebamba, Huaquerones y Santa tienen exceso de dígito 1 (0,28–0,33) y pocos 0 (conteo unitario o sin redondeo); Ica, Pachacamac y el género ASG tienen exceso de 0 (múltiplos de 10). Es la huella que dejarían precisiones o metrologías distintas, pero **no demuestra bases distintas**: los dígitos dependen también de la magnitud, de marcadores de valor 1 y de copias que repiten valores, y permutar quipus no lo corrige del todo. Propuesto: usar la heterogeneidad como pista de «formato».
- **P2.** El «total primero» es **un artefacto de Incahuasi**: 74 de los 101 casos vienen de 10 quipus del género ARC (UR255, UR256, UR267A/B, UR269, UR275…), cuya estructura `[x, c, x−c]` pone x primero; además ARC se definió en parte con esas relaciones (circularidad parcial). Sin ARC: 27 primero y 25 último de 94 totales, esperado 25,7 cada uno (p = 0,42 y 0,49): **no hay preferencia de posición en el resto del corpus** y no hay paralelo con el total al reverso. Límite: solo se detecta «total = suma de todos los demás del grupo»; no se probaron cuerdas superiores (KFG las pierde) ni sumas entre niveles.
- **P3.** Hay estructura de error de un dígito (omitir o añadir un nudo o racimo; apoya la firma «error de un racimo» de `n_simulador`). La tasa de fallo 0,54 es cota superior: algunas filas pueden no tener entrada en UR266 (el pool tiene 36 cabeceras). **No es comparable con la tasa de error de escribas protocuneiformes** porque no conseguí esa cifra; ver propuesta 3.
- **P4.** No hay estructura «tasado = entregado + adeudado» en Incahuasi. La cuota quipu es de resta (neto): entraron X, se apartó 47, quedaron X−47, un modelo distinto al de Pilos. No medí si hay entregas inferiores a la cuota (x<47).

## B4. Qué enseña el desciframiento protocuneiforme
Según NDE1993 (pp. 25–27), Falkenstein (1936) asumió valores por signo; Vaiman y Friberg en los años setenta mostraron más sistemas y que el «sistema decimal competidor» era un error lógico; el equipo de Berlín (desde 1983) cambió de método: en vez de fijar valores desde pocas cuentas, buscó las **reglas de uso** de cada signo (qué signos co-ocurren, cuáles nunca) y las probó contra todo el corpus (6500 notaciones, incluidos fragmentos sin contexto). Eso reveló sistemas distintos por clase de producto y que los «errores de cálculo» eran en parte sistemas no reconocidos. Los productos quedaron en parte sin leer. (Los p-valores de B3 son de la primera ronda; ver Holm en 11 pruebas en la verificación.)

Propuestas concretas (todas **propuestas**, no hechas):
1. **Búsqueda de pesos por cierre.** En grupos candidatos que no cuadran en decimal (UR050–055, UR039; Cajamarquilla UR178/179), probar si cuadran con radices mixtas (vectores de razones entre 2 y 20 por posición), con nulo por permutación de la asignación de razones y Holm. Es la técnica de Damerow y Englund aplicada a quipus no decimales.
2. **Co-ocurrencia por columna.** En UR278 (9 columnas estables) cruzar columna × perfil de dígitos × cuota; si las columnas son productos o unidades, su perfil debería distinguirse (P1 a escala de columna).
3. **Calibrar el error con CDLI.** Calcular la tasa de desajuste de sumas en textos con total (ATU 5, MSVO, Ur III) y compararla con 54 % (cota) y con la fracción de un dígito; así P3 será comparable.
4. **Ancla externa** al modo de Ventris: listas coloniales (ya planificada).
5. **Manos de escriba.** En Pilos las manos explican variación; en Incahuasi KFG y OKR son de la misma transcriptora, así que su concordancia no es verificación independiente (ya señalado en SINTESIS).

## Verificación con Archaic Bookkeeping (segunda ronda)
Fuente: `analisis/fuentes_txt/Nissen1993_ArchaicBookkeeping.txt`. Página impresa = página PDF − 11 hasta la PDF 100 y − 13 desde la PDF 101 (comprobado con los números impresos que conserva el OCR). Citas «NDE1993 p. N».

**1. Qué se confirma y qué se corrige.**

| Afirmación de memoria | Veredicto | Página |
|---|---|---|
| ~5000 textos, mayoría administrativos | Confirmado («casi 5000», «la gran mayoría») | pp. ix, 21 |
| Jerarquía individual → resumen → anual | Parcial. Hay tres categorías de tablilla (etiquetas, una entrada, varias casillas), niveles bajo, medio y alto, y un balance que recoge dos documentos individuales (Jemdet Nasr 62a–c) con subtotales (17 + 10 = 27 trabajadores). «Cuenta anual» solo propuesta (fig. 30; Kushim, 37 meses). La cadena de tablillas es regla (p. 30) pero la relación entre entradas «solo se ha probado en pocos casos» (p. 20) | pp. 19–20, 30, 34–36, 74–75 |
| Totales en el reverso | Confirmado con salvedades: hay tablillas con muchas partidas y sin suma, y totales del reverso mayores que la suma del anverso («las notaciones de resumen no son idénticas a sumas aritméticas») | pp. 20, 21, 35 |
| Sistemas por producto | Confirmado, con correcciones (arriba): 60 signos, 5 sistemas y derivados; S para discretos, B para raciones y cereal procesado; cada sistema SE para un cereal «probablemente»; 120 y 600 nunca juntos; 10 de 60 signos sin sistema | pp. 25–28, 37 |
| Formato fijo | Confirmado: la posición de los signos depende del formato de tablilla de cada transacción | p. 30 |
| Copias | Solo de listas léxicas (profesiones: al menos 165 copias); no de cuentas | pp. 24, 106 |
| Borradores | **No sostenido**: el único croquis preliminar con entradas borradas es de Ur III | p. 68 |
| Déficit tipo o-pe-ro en Uruk | No en Uruk IV–III. Cantidades teóricas y adeudos aparecen ya en textos arcaicos de forma general; el balance sistemático de debe y haber con déficits trasladados (LA+A) es sumerio antiguo y Ur III | pp. 35, 49–54 |

**Lección metodológica (p. 25).** Hasta 1983 las contradicciones entre los valores asumidos de los signos y las cuentas se atribuían a «errores de cálculo» de los escribas, y solo la reconstrucción de las reglas de uso de cada signo (probadas contra 6500 notaciones) reveló sistemas distintos. Aplicación: el 54 % de filas UR278→UR266 que no cuadran puede incluir convenciones o sistemas no reconocidos, no solo errores.

**2. Tasa de error de escribas.** NDE1993 no da tasas. Casos arcaicos: MSVO 3,35 omite 3 unidades de la última entrada (p. 39); MSVO 3,51 omite 4 unidades de malta en el subtotal (p. 43); MSVO 3,2 pone una unidad en vez de una decena (p. 43); MSVO 3,11 omite 5 jarras grandes y descuadra grano y malta (p. 46); un área de 30 000 Sar frente a 29 000 (p. 57). Los autores hablan de «numerosos errores aritméticos en muchos textos» (p. 37). De los 8 textos MSVO 3 que analizan, 4 llevan error: ~50 %, con sesgo de selección y N pequeño. Comparación: UR278→UR266, 13 de 24 filas no cuadran (54 %, IC95 % 0,35–0,72, cota superior). **El orden de magnitud coincide, pero no es una comparación válida** (muestras de 8 y 24 no aleatorias). Tipo de error: en Uruk, 3 de 4 son omisión de una partida o bloque y 1 es deslizamiento de magnitud; en UR278, 7 de 13 fallos son de un solo dígito (nulo 5,6), y la prueba nueva P6 (omisión de una celda entera) **no** se sostiene (2 vs 3,9 esperados, p = 0,92). El error de Incahuasi es de magnitud (un nudo o racimo), no de partida omitida.

**3. Cuadre por dos caminos.** NDE1993 no documenta totales por fila y por columna ni dos resúmenes independientes del mismo detalle. Lo más cercano: el balance 62a, que recoge exactamente las entradas de dos documentos individuales «en secuencia distinta», con dos subtotales y un total general (pp. 74–75); sumas en dos pasos, por producto y total general (p. 43); dos tablillas con total general idéntico (31a–b, p. 35; los autores no entienden su relación); un reverso con insumos calculados desde el anverso (fig. 32, p. 35). **Conclusión: el cuadre cruzado de Incahuasi es un rasgo propio (propuesto), con analogía débil, no un paralelo real documentado.** Sí tiene paralelo real el reordenamiento del balance (UR275 reordena UR266).

**4. Orden de mayor a menor.** La frase de la p. 49 («la lista empieza con los individuos que reciben raciones mayores») describe una cuenta **acadia antigua** (c. 2250 a. C.), no protocuneiforme, y dice «como es habitual para este tipo de texto». En el Uruk arcaico solo la lista de profesiones está ordenada por rango (pp. 19, 111). La lista de áreas decrecientes (p. 139) y las listas metrológicas por tamaño de la sección de aritmética son posteriores. El libro **no** establece una convención de orden decreciente en el protocuneiforme, solo en cuentas de raciones posteriores. Cuantificarlo exige CDLI (no hecho).

**5. Pruebas nuevas** (diseño en la adenda de `diseno_previo.md`; `pruebas2.py`; Holm sobre 11 pruebas; `resultados_pruebas_ronda2.csv`):

| Prueba | Resultado | p Holm (11) | Nivel |
|---|---|---|---|
| P5b: columnas de UR278 de mayor a menor | 24 filas, tau medio −0,41 (nulo 0,00) | 0,0022 | bien apoyado en UR278 |
| P5c: el mayor va primero (corpus sin Incahuasi, sin grupos con total) | 25,9 % de 2342 grupos vs 15,2 % esperado | 0,0022 | apoyado |
| P5a: orden monótono decreciente (mismo conjunto) | tau medio −0,017 (nulo 0,000, sd 0,007) | 0,063 | no significativo tras Holm |
| P6: omisión de una celda entera | 2 vs 3,9 esperado | 1 | negativo |

Lectura: fuera de Incahuasi no hay orden monótono general, pero sí tendencia a que el valor mayor vaya primero (posible cabecera o subtotal parcial no detectado como total). El decrecimiento de las 9 columnas de UR278 es propiedad de ese quipu, no convención bien apoyada del corpus ni de Uruk. Holm recalculado en 11: P1a 0,0048; P1b, P2a y P3 0,0022; el resto de la primera ronda no cambia de conclusión.

## Para el coordinador
- Confirmado con página: sistemas numéricos por clase de producto (NDE1993 pp. 25–28), formato fijo por transacción (p. 30), totales en el reverso (p. 20), copias solo de listas léxicas (pp. 24, 106). La cadena de documentos es real pero «probada en pocos casos» (p. 20).
- Se cayó: borradores de cuentas arcaicas (solo uno, de Ur III); mi lista de sistemas (el tiempo es U4, EN es desconocido); «mayor a menor» como convención protocuneiforme (la cita de la p. 49 es acadia antigua).
- Totales: el reverso no siempre es la suma aritmética (p. 35). Un desajuste no prueba error; puede ser convención contable. Misma cautela para Incahuasi.
- Lección del desciframiento (p. 25): los «errores de escriba» eran sistemas no reconocidos. Antes de atribuir el 54 % de UR278→UR266 a errores, buscar convenciones.
- Cuadre cruzado de Incahuasi: sin paralelo documentado en Uruk; rasgo propio (propuesto). Paralelo real: balance que reordena entradas de documentos individuales (pp. 74–75).
- Errores: el libro no da tasas; 4 de 8 textos MSVO 3 analizados tienen error (sesgo). Magnitud parecida a 54 %, comparación no válida. Uruk: omisiones de partida; UR278: errores de un dígito (7/13) y omisión de celda no apoyada (P6).
- Nuevo: P5b (columnas de UR278 decrecientes, tau −0,41, Holm 0,0022) y P5c (mayor primero 26 % vs 15 %, Holm 0,0022); sin orden monótono general (P5a, Holm 0,063).
- El déficit o-pe-ro no está en Uruk IV–III (balance de debe y haber: sumerio antiguo y Ur III, pp. 49–54); su ausencia en Incahuasi (P4) no contradice un paralelo protocuneiforme.
