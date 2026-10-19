# Verificación independiente de las afirmaciones sobre Incahuasi (equipo 16)

Recálculo desde cero con scripts propios sobre `analisis/datos/cuerdas.csv` (y `quipus.csv` solo para metadatos). No se leyó ni ejecutó nada de `analisis/09_incahuasi/` ni de `analisis/13_sistema_incahuasi/`.

Scripts: `lib.py` (carga, registros, cabeceras), `01_suma_cabeceras.py`, `02_cuotas.py`, `03_ur270_ur278.py`, `04_totales_ur278.py`. Salidas: `salida_0*.txt`. Semilla 16, 10 000 réplicas por nulo; p = (k+1)/(N+1).

## Tabla resumen

| # | Afirmación | Reproduce | Cifras propias | p nulo |
|---|---|---|---|---|
| 1 | cab(273A_i) + cab(273B_i) = cab de UR266/UR275/UR269 | **sí** (cifra exacta) | 8 exactas de 18 pares válidos; 10/18 con ±1. Nulo (barajar orden de 273B): media 0,73 exactas | <0,0001 (0 de 10 000 réplicas con ≥8) |
| 2 | cab(267A_i) + cab(267B_i) = cab de UR269 | **parcial** | 5 exactas de 26 pares (no 3/6); 8/26 con ±1 (no 5/6). Los 3 ejemplos citados sí son exactos. Nulo media 0,70 | 0,0005 |
| 3 | Valor "cuota" en casi todos los registros | **parcial** | UR274A 30: 17/26 (65 %); UR274B 17: 12/33 (36 %); UR273B 17: 3/27 (11 %); UR266 47: 23/32 (22 tras cabecera); UR275 47: 24/26 (92 %); UR267A 15: 25/26; UR255 15: 24/28; UR267B 10: 26/26; UR256 10: 21/24 | ≤0,0001 en 7 quipus; 274B 0,06; 273B 0,88 |
| 4 | UR270 vs UR278, 9 columnas (colgante + s1) | **sí** | 5 de 12 grupos con 6–9/9 (g0→g21: 9/9; g4→g25: 9/9; g5→g26: 7/9; g8→g27: 8/9; g9→g28: 6/9). Control solo colgantes: 0 de 12 con ≥6 | por grupo 0,0001 (los 5); global P(≥5 grupos) 0,0001 |
| 5 | Totales de fila UR278 = cabeceras UR266 (15 pares, τ=1) | **parcial** | 11 pares exactos únicos, τ=1,00. Con ±1: 14 pares únicos, τ=0,74. El "15" sale de contar cabeceras con alguna suma ±1, no únicas. Emparejamiento greedy en orden fuerza τ=1 por construcción | P(n≥11)<0,0001; P(n≥11 y τ=1)<0,0001 |

## Método y definiciones

- **Registro**: grupo de colgantes no separador. Probé tres variantes de separador: A (todas las cuerdas PK), B (primera cuerda empieza por PK), C (alguna cuerda empieza por PK). A y B dan lo mismo en todos los quipus. C solo cambia UR266 (32 a 31 registros; el grupo 26, colores W-YB-PK, deja de contar) y UR274A (26 a 25). Con C, la afirmación 1 da 8/18 igual, y la 3 da UR274A 16/25 en vez de 17/26 y UR266 47 sin cambio (23/31). Ninguna conclusión cambia.
- **Cabecera**: valor del primer colgante del grupo con nudos.
- **Afirmación 1 y 2**: emparejo por índice de registro (ya que los ejemplos alinean por índice). Nulo: barajo la lista completa de registros de B (incluidos ausentes). Estadístico: exactos, y ±1 como control.
- **Afirmación 3**: k = número de registros con ≥1 cuerda de valor exacto X (colgante o subsidiaria del grupo). Nulo 1: permuto valores no ausentes dentro del quipu. Nulo 2 (look-elsewhere): máximo de k sobre todos los valores del quipu. Resultado: X es el valor más frecuente en registros en los 9 casos, y el nulo de máximo da el mismo p que el nulo fijo.
- **Afirmación 4**: S_j = colgante_j + s1(colgante_j), j=1..9 (orden). Compara por posición con los 30 grupos de UR278 (±1). Nulo: permuto las 9 sumas dentro del grupo de UR270. Control: solo colgantes.
- **Afirmación 5**: solo cabeceras con una única suma igual (exacta o ±1) para evitar el greedy. τ de Kendall sobre esos pares. Nulo: cada grupo de UR278 se sustituye por la suma de su mismo número de cuerdas tomadas al azar del conjunto de cuerdas de UR278. (Permutar las sumas entre grupos no sirve: deja invariante el número de coincidencias.)

## Resultados y controles

- **1 y 2**: la coincidencia es real frente al nulo de orden, pero con magnitudes pequeñas la cifra del nulo que da el equipo (≈1,3) no sale con mi nulo (0,73). Los pares que coinciden son sumas de valores de 273A/B entre 1 500 y 2 950 en los pares exactos. UR266 y UR275 tienen listas de cabeceras casi idénticas, así que el conjunto diana es menos independiente de lo que parece; el nulo ya lo contempla porque usa el mismo conjunto.
- **3**: el patrón es fuerte donde aparece (UR275, UR267A, UR267B, UR255, UR256), con X siempre como valor más frecuente del quipu. Se sitúa en una posición fija del registro: en UR275 es el segundo colgante en 24/26 registros; en UR267A y UR267B es el segundo en 23/26. Eso sugiere una celda fija (etiqueta o cuota estructural), no un valor reconstruido. No llega a "casi todos" en UR274A (65 %) ni en UR274B/UR273B (36 %, 11 %; esta última sin señal).
- **4**: es la afirmación más sólida. El control de solo colgantes da 0, y los vectores de los grupos que coinciden (g0, g4, g5, g8, g9) casi no tienen valores redondos (solo 98 y 95 cerca de 100 en g9). Además la correspondencia es monótona: UR270 g0, g4, g5, g8, g9, g10 se emparejan con UR278 g21, g25, g26, g27, g28, g29. Es un indicio de estructura compartida, pero hay que mirarlo con cuidado (ver siguientes pasos).
- **5**: los 11 pares exactos con τ=1 superan el nulo (media 0,34). La cifra de 15 pares con τ=1 no se reproduce como tal: con ±1 el τ baja a 0,74.
- **Explicaciones aburridas**: no encuentro cordones idénticos (valor+nudos+largo, ≥2 racimos) compartidos entre quipus objetivo, así que no es duplicación de datos. Sí existe una posible tautología de codificación: si s1 = UR278_j − UR270_j por construcción del registro, la afirmación 4 sería un artefacto. No lo puedo verificar con los datos.

## Nivel de evidencia

- **Apoyado con datos**: afirmación 1 (8/18, p<0,0001); afirmación 4 (5 grupos, p=0,0001, con control negativo); afirmación 5 (11 pares exactos, τ=1, p<0,0001).
- **Apoyado con datos, débil**: afirmación 2 (5/26, p=0,0005; el número citado de 3/6 no se reproduce).
- **Apoyado con datos, parcial**: afirmación 3 (7 de 9 quipus con p<0,001; 274B y 273B no).
- **Propuesto**: que la cuota (valor fijo en posición fija) es una etiqueta estructural. El significado de la cuota es especulativo.

## Siguientes pasos

1. Comprobar si s1 de UR270 es residuo respecto a UR278 (o viceversa) y si la diferencia tiene estructura propia. Esto decide si la afirmación 4 es un hallazgo o una tautología de codificación.
2. Revisar la orientación de columnas en la afirmación 4 (orden inverso) y el número de grupos comparables; el nulo actual es por grupo, no por quipu.
3. Repetir la afirmación 1 con un nulo que preserve también la estructura de cabeceras de UR266/UR275, ya que son casi idénticas.
4. Unificar la definición de "separador" con el equipo 13 antes de comparar cifras; las diferencias están en UR266 (grupo 26) y UR274A.
