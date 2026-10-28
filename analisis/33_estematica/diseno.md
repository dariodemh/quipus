# 33 · Estemática del corpus: diseño congelado

Escrito el 2026-10-18 **antes de correr ninguna prueba de este análisis**. Lo único que miré antes de escribirlo: tamaños (cuerdas por quipu: mediana 43, máximo 1831), los códigos de `terminacion` (K, B, U, R, D) y los informes previos 04 y 14 (que ya contienen resultados de copias por un detector distinto: Smith-Waterman de un solo bloque). Semilla única: **20261033**.

## 0. Qué añade esto a 04/14

04 buscó UN bloque colineal por par (directo o inverso), sin escala ni reordenamiento. 14 hizo crítica textual por par. Aquí: (i) una medida que suma varios bloques disjuntos en cualquier orden y sentido (robusta a reordenar grupos e invertir), (ii) escala ×k, (iii) familias con ≥3 testigos tratadas con el método de Lachmann (errores conjuntivos/separativos, compatibilidad de particiones), (iv) dirección de copia con criterios explícitos.

## 1. Unidades

- **Secuencia de un quipu**: valores enteros de las cuerdas con nudos (todos los niveles) en `orden` (misma definición que 04, `cuerdas.csv`). Entran los quipus con ≥ 3 cuerdas anudadas. N pares = C(n,2) sobre esos quipus; ese N es el denominador de Holm y BH.
- **Nivel** de cada cuerda (`nivel`) se guarda para el nulo y para la crítica (capa de subsidiarias).
- Color normalizado con `re.sub(r'\([^)]*\)','',s)`. El color NO entra en la detección (solo en la crítica, como en 14).

## 2. Medida de similitud (congelada)

Puntuación log-odds en bits, idéntica a 04 (reutilizo sus funciones `_ft`/`matriz`): exacta log2(0,85/f(v)); tolerante (|a−b| = 10^d, un nudo de más o de menos) log2(0,05/t(v)); discordancia log2(0,10/(1−f−t)); f y t sobre la composición conjunta del par (los valores comunes del par pesan casi nada: robustez a «1-1-1» y a listas de ceros). Hueco lineal 5 bits.

Robustez pedida:
- **(e) pequeñas diferencias de valor**: la coincidencia tolerante (±1 nudo en una posición).
- **(d) omisión/inserción**: huecos del alineamiento local.
- **(b) inversión**: cada bloque se busca en los dos sentidos de B.
- **(a) reordenamiento de grupos**: **suma de bloques disjuntos**. Se toma el mejor bloque local (Smith-Waterman, directo o inverso), se retiran sus filas y columnas (cada cuerda se usa una sola vez) y se repite; se suman hasta **K = 5** bloques, contando el 2.º y siguientes solo si valen **≥ τ = 10 bits**. Un par es «reordenado» si tiene ≥ 2 bloques aceptados cuyo orden en A y en B no coincide o cuyos sentidos difieren.
- **(c) escala ×k**: B se transforma por k ∈ {1, 10, 1/10, 2, 1/2} (para 1/k solo los valores divisibles; los demás quedan como centinela que nunca coincide). Puntuación del par = máximo sobre k. El nulo hace el mismo máximo, así que la búsqueda sobre k queda pagada dentro del p.

Estadístico: `S = max_k Σ bloques`. Se guardan k, bloques, sentidos, cuerdas alineadas, exactas, tolerantes y discordantes.

## 3. Prefiltro (huella barata)

Para cada par y cada k: H_k = Σ idf(v) sobre los valores distintos v ≥ 10 presentes en A y en k·B; idf(v) = log2(N_quipus/df(v)). Invariante a orden, inversión y reordenamiento. **Candidatos = los 15 000 pares con mayor max_k H_k** (≈ 7 % de los pares). Los pares no candidatos reciben p = 1 (conservador) pero cuentan en el denominador de Holm/BH. Diagnóstico obligatorio: recuperación de los controles y de los 25 pares de 04 por el prefiltro.

## 4. Nulos

1. **Principal (por par)**: barajar los valores dentro de cada quipu **dentro de su nivel** (colgantes entre colgantes, subsidiarias entre subsidiarias; las posiciones anudadas y los niveles quedan fijos), en A y en B, y recalcular `S` (con el máximo sobre k). Etapas: 99 permutaciones a todos los candidatos; si b ≤ 1, 999 más. p empírico = (b+1)/(N+1). Si la observación supera todas las réplicas, cola extrapolada por Gumbel ajustada por momentos (como 04, con escala mínima 1/ln 2). Se informan p_emp y p.
2. **Por bloques** (solo para pares con q < 0,05): permutación de bloques de 5 cuerdas (conserva autocorrelación local); se informa, no decide (04 mostró que es demasiado conservador para copias verdaderas).
3. **Pares de sitios distintos**: tasa de pares con q < 0,05 entre pares de dos procedencias conocidas distintas. Si la copia es fenómeno de archivo, esa tasa debe ser ≈ 0; cada caso que aparezca se examina a mano.

## 5. Multiplicidad y niveles

- **Holm** y **BH** sobre los N pares (no candidatos con p = 1).
- **Mismo objeto** (duplicado de base): largos de cuerda alineados r ≥ 0,9 y diferencia mediana ≤ 2,5 cm (regla de 04), o mismo número de inventario. No es copia: se fusiona como un solo testigo con dos lecturas.
- Niveles por par:
  - **bien apoyado**: Holm < 0,05 y pasa el equipo rojo (sección 7).
  - **apoyado**: BH q < 0,05 y pasa el equipo rojo.
  - **propuesto**: q < 0,05 pero falla algún punto del equipo rojo; o q < 0,20.
  - **especulativo**: p < 1e-3 sin lo anterior.

## 6. Exploración / confirmación

- Los quipus se dividen en dos mitades **E** y **C**, estratificadas por procedencia (orden por kfg, `default_rng(20261033)`).
- Primero se corre SOLO sobre pares E–E. En E está permitido cambiar τ, K, el conjunto de k o el tamaño del prefiltro; cualquier cambio se anota en la adenda de abajo con su motivo. Luego se congela y se corre sobre todo.
- **Detección de pares**: no depende de la división (parámetros fijos y Holm). Se compara la tasa de descubrimiento E–E frente a C–C como control de calibración.
- **Preguntas de sistema** (qué géneros del atlas y qué sitios se copian; si las copias se quedan dentro del archivo): las hipótesis se formulan con los quipus de E (implicación de cada quipu en ≥ 1 copia, Fisher por género/sitio) y se prueban en los quipus de C, con Holm sobre las hipótesis llevadas a C.

## 7. Equipo rojo (por par nuevo; se fija ahora)

Un par cae a «propuesto» si falla cualquiera:
1. **Diversidad**: las coincidencias exactas alineadas incluyen ≥ 4 valores distintos y ≥ 3 valores ≥ 10.
2. **Sin valores comunes**: quitando de ambos quipus los 10 valores más frecuentes del corpus (y los ceros), el par sigue con p_emp < 0,01 (199 permutaciones).
3. **Longitud**: ≥ 8 cuerdas alineadas.
4. **Bloques**: p del nulo por bloques < 0,05.

## 8. Crítica de familias (Lachmann)

- **Familia** = componente conexa del grafo de pares apoyados o bien apoyados (los duplicados de base fusionados).
- **Alineamiento múltiple en estrella** sobre el testigo con mayor solapamiento total; columnas = cuerdas del centro; cada testigo se proyecta por sus bloques con el centro.
- **Variantes**: columnas con ≥ 2 lecturas distintas (la omisión «—» cuenta como lectura).
  - **Conjuntivo** (≥ 3 testigos): lectura compartida por un subconjunto propio de ≥ 2 testigos frente al resto, que no sea un error trivial plausible por azar (se informa por separado si es ±1 nudo).
  - **Separativo**: lectura singular de un testigo, contra el acuerdo de los demás (o, en pares, cualquier diferencia).
  - **Árbol**: particiones compatibles dos a dos (prueba de los cuatro gametos) → árbol; particiones incompatibles = **contaminación** o coincidencia; se informa cuántas.
- **Dirección de copia** (por par dentro de la familia), criterios fijados ahora, en este orden:
  1. **Aritmética interna**: en cada variante de valor, ¿qué lectura cierra una suma interna de su propio quipu (colgante = Σ de sus subsidiarias directas; cuerda = Σ de 2–12 colgantes contiguos inmediatamente antes o después; o es sumando de una cuerda que cierra así)? La lectura que cierra es la correcta; la que no cierra, error del testigo que la porta.
  2. **Omisión de capa o de cuerdas** (lectio brevior frente a contenido completo): el testigo que omite una capa entera (subsidiarias) o un valor sistemático es candidato a derivado *si* además tiene más errores separativos; la omisión sola no decide.
  3. **Daño**: lectura menor en cuerda rota (terminación B) = pérdida física, no error de copia; se excluye de 1–2.
  4. **Corrección**: si un testigo tiene la lectura que cierra y el otro no, y el primero es el más tardío según otro criterio, es corrección.
  Veredicto: «A → B» solo si ≥ 2 criterios independientes coinciden; si no, «sin dirección».
- **Cruces**: museo, procedencia, número de inventario, prefijo de transcriptor (AS/UR/HP/KH/MM/JC…), OKR `khipu_main.INVESTIGATOR_NUM`, `CREATED_BY` de `khipu_main` y de `cord`.
- **KFG frente a OKR**: para los miembros de las familias, comparar los valores de KFG con los reconstruidos de OKR (`knot_cluster.TOTAL_VALUE` sumado por cuerda). Igualdad ≈ 100 % ⇒ misma lectura, no lecturas independientes.

## 9. Publicación previa

Para cada par: grep de los dos identificadores (y sus alias AS/UR) en `analisis/fuentes_txt/` y `docs/fichas/`, y en los informes del propio proyecto (04, 14, 21, SINTESIS). «Nueva» solo si no aparece en ninguna fuente publicada (Urton, Urton & Chu, Urton & Brezine, Clindaniel, Ascher); si aparece solo en el proyecto, «nueva respecto a la literatura, ya en el proyecto».

## 10. Potencia

Simulación sobre quipus reales: se siembra en un quipu A una copia de un tramo de L cuerdas de otro quipu B (L = 5, 8, 12, 20), con 10 % de errores ±1 nudo, 10 % de omisiones, un reordenamiento de dos bloques y, aparte, inversión o escala ×10; se mide la proporción que alcanza Holm < 0,05 con la misma maquinaria → efecto mínimo detectable (L al 80 %).

## Adenda (cambios hechos en E, con motivo)

1. **Prefiltro sustituido (antes de mirar ninguna puntuación de pares).** La huella de §3 se evaluó solo contra los controles positivos y los 25 pares de 04: con valores ≥ 10 deja fuera 7 de 25 (UR006/009/021 de Leymebamba, AS159/AS173, QU002/UR137 y 2 débiles), porque esas copias son de valores pequeños; con todos los valores y coseno, aún pierde 5. Un prefiltro que pierde controles sesga el estema. Se sustituye por **Monte Carlo secuencial sobre todos los pares** (Besag–Clifford): etapa 0 con 9 permutaciones por nivel a los ≈ 200 000 pares; siguen a 99 solo los que superan las 9; a 999 los que tienen b ≤ 1 en 108. El p de los que se detienen es el empírico de su etapa (≥ 0,1), válido y no 1. La huella queda como columna de diagnóstico. Coste medido: ~8 ms por par mediano grande (HP055/UR1084, 5 escalas).
2. **Nulo y τ cambiados tras la fase E (corrida v1: `barrido_E_v1.csv.gz`, `salida_01_E_v1.txt`).** En E–E salían 84 pares con q < 0,05, dominados por «quipus eje» (HP034 con 9 compañeros, UR1114 con 12) cuyos bloques eran rachas de valores pequeños (2-2-2-2-2, 1-1-1) sumadas en 3–4 bloques de ~10 bits. Diagnóstico: el nulo por nivel destruye las rachas y la cola de la suma de bloques cortos es pesada. Cambios, probados solo con pares eje de E y los controles positivos (scratchpad `t_null.py`): (a) **nulo principal = permutación de rachas** (cada racha de valores iguales se mueve como unidad; conserva la composición y las rachas, destruye el orden entre valores distintos); el nulo por nivel deja de usarse; (b) **τ = 20 bits** para el 2.º bloque y siguientes. Efecto: HP034/UR006 pasa de p = 1e-12 a 0,19; JC016/UR1114 de 1e-5 a 1,0; los 11 controles siguen entre 1e-7 y 1e-91. Desde aquí, congelado; se corre todo.
3. **Añadidos post hoc, después de ver el barrido completo (no cambian el barrido; se marcan «post hoc» en todas las salidas).** (a) `05_orden_libre.py`: prueba sin orden (valores ≥ 100 compartidos frente a reemplazo por quipus de otra procedencia, y orden de esos valores), porque los controles UR256/UR267B y UR266/UR275 no se recuperaban (cada tramo compartido tiene 2 cuerdas, por debajo de τ). (b) `06_candidatas_lector.py`: dos candidatas que pasó el coordinador. (c) En `03_familias.py`, el equipo rojo (§7) se aplica solo a pares NUEVOS, como dice §7; en los publicados como copia, el nivel lo dan Holm/BH. La lista de publicados se verificó leyendo cada pasaje.
