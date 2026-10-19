# Predicciones prerregistradas (escritas ANTES de mirar los datos que las ponen a prueba)

## A. Hipótesis post hoc «UR050 + UR055 = par de quipus de ceques»

Escrita el 18-10-2026, mientras corría el barrido y **sin haber mirado** colores, canutos ni valores de UR050/UR055 más allá de su número de colgantes.

**Origen (post hoc).** UR050 tiene 164 colgantes y UR055, 180. La suma es 344, dentro de las «328–350 wakas» de U17 l. 1258. Urton (l. 1518–1524) propone que los ceques se registraban en **un par** de quipus, uno por mitad. Hay que tratarla como hipótesis nueva; el conteo **no** es evidencia.

**Predicciones con datos no usados:**

- **A1.** Si cada colgante es una waka y los ceques se marcan por cambios de color (o de canuto), las rachas de color de los colgantes deberían ser:
  - unas 18 en el quipu de Hanan (9 + 9 ceques);
  - unas 23 en el de Hurin (9 + 14) (U17 l. 1263).

  Se acepta si el número de rachas de un quipu cae en [15, 21] y el del otro en [20, 26]. Antes, el nulo: ¿qué fracción de quipus de 150–200 colgantes cumple el par por azar?
- **A2.** Los ceques van en tríos collana/payan/cayao. En la secuencia de colores **modales de las rachas**, P9a(rachas) > 0 con p < 0,05 (permutación de las rachas).
- **A3.** Si el par fuera real, UR050 y UR055 deberían compartir procedencia, colección o fibra.

  Se registra si comparten material (camélido, canutos), museo o procedencia. Dato conocido de antemano (`n_no_numericos`): UR050 está en la colección Soldi y UR055 en el Museo Oro. Por tanto, A3 ya es **débil** antes de probar.

Bastan dos fallos de tres para descartar la hipótesis.

## B. Regla general para el paso 5

Para cada quipu que no es de Incahuasi y que coincide con una plantilla validada en la mitad de confirmación (o, si no hay ninguno, el mejor de exploración), se elige UNA predicción con datos que no entraron en el estadístico. Puede ser:

- otro quipu del mismo hallazgo;
- una relación de suma;
- subsidiarias o colores, si el estadístico usaba valores, o viceversa.

La predicción se escribe en `informe.md` §5 antes de ejecutar el script que la prueba (`05_predicciones.py`).

## Resultado de A (ejecutado con `05_predicciones.py`)

Las tres predicciones fallan:

- **A1:** UR050 tiene 3 rachas de color y UR055 tiene 15. Los canutos (OKR) forman 5 y 10 cúmulos. No aparecen ni las 18 ni las 23.
- **A2:** UR055 da P9a(rachas) = −0,85 (p ≈ 1). UR050 no es evaluable.
- **A3:** UR050 es de camélido y está en la colección Soldi; UR055 es de algodón y está en el Museo Oro.

La hipótesis de ceques para UR050 + UR055 queda **descartada**.

## C. Predicciones del paso 5 (escritas tras ver la lista de coincidencias, ANTES de mirar valores o subsidiarias de esos quipus)

- **C1. P4r, padrón: UR028, UR1114, UR1140 y HP033** (y los 6 del Santa como control).
  - **Predicción:** si cada banda de color es la ficha de una persona (como en el Santa), los **valores** de las cuerdas, que P4r no usa, siguen un perfil por posición dentro de la banda.
  - **Medida:** η² de la posición sobre log10(v+1) en las bandas del largo modal. Debe ser > nulo (permutación de valores entre esas celdas), con p < 0,05.
  - **C1b:** UR1123, copia publicada de UR1114 (Urton 2005), debe dar P4r con el mismo largo de banda.
- **C2. P9a, tríos de color (lectura de ceques): UR053A y UR053D** (los valores de UR053C ya los vi en la tabla 8.1 de Urton) y los demás P9a que no son de Incahuasi (QU001, UR1033B, UR1099, UR210, UR218, AS089, HP051_B, UR1121, UR073).
  - **Predicción:** si cada trío es collana/payan/cayao, la **posición en el trío** (fase del ciclo de color) ordena los valores.
  - **Medida:** η² de la fase sobre log10(v+1) > nulo, con p < 0,05.
  - **Predicción específica para UR053A/D:** la cuerda de la misma fase cromática que la «W» de UR053C es la mayor del trío en la mayoría de tríos.
- **C3. P11a/P11b, registro segmentado por eventos:** UR1057, UR1131, HP055, AS202, UR1176, AS074, AS089, AS203, UR1099, UR1149, UR1175, UR172, UR1088, AS048, AS178, HP051_B, UR1121, UR1144 (y UR068 y UR006 como referencia).
  - **Predicción:** si los bloques son eventos con la misma lista de categorías, los **valores** de los bloques repetidos comparten perfil de categoría. Esa es la forma del registro wanka: un factor de escala por evento.
  - **Medida:** correlación de Spearman media entre pares de bloques (vectores de valores alineados por posición) > nulo (permutación de valores entre las celdas de los bloques), con p < 0,05.
  - **Además:** < 50 % de celdas idénticas, para que no sea una copia.

## D. Predicciones adicionales (escritas tras ver la lista P6b y ANTES de mirar la alineación concreta)

- **C4. P6b fuera de Puruchuco: KH0033 y UR044** (La Puntilla, entre Paracas y Pisco) **y QU013.** Si la relación es una consolidación real (secciones que se suman en otro quipu):
  - **(i)** las **primeras subsidiarias** (no usadas) de las mismas secciones también suman la subsidiaria de la ventana destino en más posiciones que con el nulo (permutación de las subsidiarias de k). El conteo se hace en las posiciones con subsidiaria en ambos lados;
  - **(ii)** en la mejor alineación, las posiciones que no coinciden difieren del destino en un solo racimo, es decir, en ±10^j, en más casos que con el nulo de valores permutados.
- **C2b.** Antes de leer UR053A/C/D como tres registros independientes, hay que comprobar que **no son copias**: la fracción de valores idénticos en la mejor alineación entre pares debe ser < 50 %.

## E. Conjunto atado UR053A–E (escrita tras ver que los cinco comparten el vocabulario W / R(B|L) / AB, con W siempre como valor mayor, y ANTES de cruzar valores entre ellos)

- **C5.** Las magnitudes van por órdenes: A está en miles; D, en cientos; B, C y E, en decenas. Si el conjunto es una jerarquía de consolidación al estilo de Puruchuco, P6b, con «hallazgo» = conjunto atado (los socios son los otros 4), debe dar p < 0,05 en al menos un quipu. El nulo es el de P6b.
  - Es una variante nueva (la n.º 33 del recuento), porque la procedencia `Unknown` dejaba al conjunto fuera de P6b.

## F. MM001 (P9b_iv: cuatro grupos consecutivos de tamaños {9, 9, 9, 14}, tasa base 1/651). Escrita ANTES de mirar valores ni colores de esos grupos

- **C6.** Si esos 41 colgantes son los 41 ceques (3 suyus de 9 y Cuntisuyu de 14; U17 l. 1263) y cada valor cuenta las wakas de un ceque:
  - **(i)** la suma de sus valores cae en [300, 360] (328–350 wakas, U17 l. 1258, con margen de pérdida);
  - **(ii)** los colores muestran ciclo de 3 (collana/payan/cayao) dentro de esos 41 colgantes: P9a > 0 con p < 0,05.
