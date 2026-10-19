# Predicciones verificables

Este documento recoge predicciones concretas que no podemos comprobar desde los datos digitales. Hace falta ver el objeto, una fotografía con escala o el documento de archivo. **No hemos visto ninguno de esos objetos ni documentos.**

Cada predicción indica:

- qué se predice;
- en qué objeto o documento;
- qué resultado la confirmaría y cuál la refutaría;
- de dónde sale y desde cuándo está fijada.

Salvo que se diga otra cosa, las predicciones se fijaron el 18-10-2026 en los archivos citados, antes de cualquier contacto externo.

**Advertencia general.** En Inkawasi, KFG y OKR proceden de la **misma lectura** (la misma transcriptora). Una relectura física independiente es, por sí sola, la prueba que más falta nos hace.

Nomenclatura: `p180` es el colgante n.º 180 en la numeración de KFG/OKR; `s1` es su primera subsidiaria. En los nudos, `7L` es un nudo largo de 7 vueltas, `5S` un racimo de 5 nudos simples y `E` una figura de ocho (valor 1).

---

## A. Inkawasi: cuerdas concretas (depositario actual de los quipus de las excavaciones de A. Chu)

Prioridad, de mayor a menor: 1, 2, 3, 4, 5, 6, 7. Los cuatro primeros son los más baratos y los más informativos.

**1. UR278 p180 (grupo g21, columna 1).**

- **Predicción:** el último nudo largo tiene **6 vueltas**, no 7. El valor sería 237, no 238.
- **Por qué:**
  - la celda debe ser igual a colgante + subsidiaria de UR270 g0: 178 + 59 = 237;
  - la fila g21 suma 1654, y el libro (UR266/UR275) dice 1653.

  Un solo cambio arregla las dos comprobaciones a la vez.
- **Confirma:** 6L. **Refuta:** 7L claro e intacto. En ese caso, las dos discrepancias de +1 son reales, es decir, el registro original ya difería.
- *Fuente:* `ds/n_casi_aciertos/informe.md` §3.3c; `19_prediccion/predicciones_museo.csv`.

**2. UR275 p51 (cuota del registro g10).**

- **Predicción:** la cuerda vale 47 (`4S,40; 7L,7`) y el 7L terminal se perdió o no se transcribió. Hoy está registrada como 40.
- **Por qué:** las otras 24 cuotas del quipu valen 47, y p51 mide 26,5 cm, frente a una mediana de 41,8 cm.
- **Confirma:** un 7L, o una punta rota justo después del racimo de decenas. **Refuta:** punta intacta y sin nudo de unidades.
- *Fuente:* `ds/n_casi_aciertos` §3.3e; `19_prediccion` §6.

**3. UR274B p9, p13, p19 y p64 (cuotas registradas como 10).**

- **Predicción:** son cuotas de **17** (`1S,10; 7L,7`) a las que les falta el 7L terminal.
- **Por qué:**
  - las otras 12 cuotas del quipu valen 17;
  - las cuatro «10» están entre las cinco cuerdas más cortas de las 16 que valen 10 o 17 (20,5–25,0 cm);
  - 1332 = 1315 + 17.
- **Confirma:** el 7L o restos de él, o puntas rotas. **Refuta:** cuatro puntas intactas sin nudo de unidades. Entonces la cuota 10 es una variante real del registro y el 17 de UR274B se debilita.
- *Fuente:* `ds/n_casi_aciertos` §3.3f; verificado en `paquete_revision/verificar.py` (corrige «exactamente las 4 más cortas»).

**4. UR278 p77 (grupo g8, celda 5).**

- **Predicción:** falta un **6L** terminal; el valor sería 346 y no 340.
- **Por qué:** la fila g8 suma 3243 y el libro dice 3249 (+6), y p77 es la única de las 9 celdas sin nudo de unidades.
- **Confirma:** 6L, o una punta rota tras las decenas. **Refuta:** punta intacta.
- *Fuente:* `ds/n_casi_aciertos` §3.4.

**5. Racimo de centenas de un mismo total en cuatro objetos.**

- **Predicción:** UR269 p181 tiene 4 nudos de centena (2433), UR266 p64 y UR275 p41 tienen 6 (2633), y una celda de la fila g12 de UR278 (p109–p117) tiene un nudo de centena más de lo transcrito.
- **Por qué:** la fila g12 suma 2533 y los libros dicen 2633. Las copias difieren en 4, 5 y 6 nudos de centena.
- **Confirma:** una celda de g12 con un nudo de centena más; entonces la fila suma 2633 y la discrepancia era de transcripción. **Refuta:** los cuatro objetos tal como están transcritos; la diferencia entre copias es real y nos enseña cómo se copiaba.
- *Advertencia:* 2633 aparece también en UR269 p89, así que la «escalera» no es necesariamente lineal.
- *Fuente:* `ds/n_casi_aciertos` §3.3a; `ds/n_tanteo` §8.

**6. UR266 p104.**

- **Predicción:** vale **1737** (`1S,1000; 7S,700; 3S,30; 7L,7`). Es lo que da la suma 448 + 1289 de UR273A y UR273B en el registro g11.
- **Por qué hay que mirarlo:** Urton (2017) cita 1,732. El OKR se reimportó en 2020 y hoy dice 1737.
- **Confirma:** 7L. **Refuta:** 2L, es decir, 1732. Entonces una de las 8 sumas exactas de H1 desaparece.
- *Fuente:* `18_equipo_rojo/informe.md` (bandera de datos).

**7. Relectura independiente de UR273A, UR273B y UR274A completos.**

- **Predicción:** una lectura nueva, hecha sin conocer nuestras cifras, reproduce las 8 sumas exactas A+B: 2950, 1653, 1737, 1827, 1780, 2247, 1765 y 1506. También reproduce los 3 rellenos de UR274A (1278, 2020 y 2106).
- **Confirma:** que se mantengan 7 de las 8 o más. **Refuta:** que se rompan 3 o más. En ese caso H1, que hoy está apoyada y no demostrada, cae.
- *Detalle técnico:* conviene registrar también los separadores rosados. Nuestra alineación depende de que caigan en los mismos grupos (10, 14, 16, 23 y 27) en las dos mitades.

**8. Tres discrepancias que NO son errores de un solo nudo.**

- **Predicción:** no se resolverán encontrando un nudo mal leído. Hará falta una cuerda ausente, dos errores a la vez, o aceptar una diferencia real del registro.
- **Los casos:**
  - UR278 g27 p217: 246, frente a 290 por UR270;
  - UR278 g28 p228: 300, frente a 394;
  - UR266 p86: 2114, frente a 2020.

  Ninguna edición de un racimo produce diferencias de 44 o 94. Añadimos el g4 de UR278: la fila difiere en +24.
- **Refuta:** un solo nudo que, releído, cierre la relación.
- *Fuente:* `ds/n_casi_aciertos` §4–5.

**9. Cuerdas registradas «sin nudos».**

- **Predicción:** si conservan rastros de nudos, sus valores serán los que predecimos:
  - UR255: p2 = 91, p10 = 45, p22 = 70, p25 = 145, p28 = 99, p31 = 126, p34 = 172, p38 = 80 y p41 = 200 (neto = cabecera − 15);
  - UR255 p8 y p83 = 15; UR256 p40, p81 y p112 = 10; UR274A p13, p51, p59, p72 y p75 = 30; UR275 p110 = 47.
- **Confirma:** nudos perdidos con esos valores. **Refuta:** valores distintos. Si son cuerdas intactas sin nudos, la predicción no se puede evaluar.
- *Fuente:* `19_prediccion/predicciones_museo.csv`, confianza alta (43 filas).

## B. Inkawasi: objetos no estudiados

**10. Los cinco quipus de Inkawasi que Urton no analizó.**

- **Predicción:** Urton y Chu 2015 hablan de 34 quipus, pero el apéndice solo lista 29. UR269 está organizado en bloques de 5 filas con cuotas 47, 46, 46, 44 y 25. Si esos bloques consolidan cinco flujos, en los quipus que faltan (o en registros de campo inéditos) habrá **parejas A/B cuyas cuotas sumen 46 o 44**, y sus sumas A_i + B_i darán las cabeceras de las filas 2–4 de los bloques de UR269.
- **Regla congelada:** alinear por número de grupo; un registro en blanco en A se rellena con su copia.
- **Confirma:** 3 o más sumas exactas sobre cabeceras de las filas 2–4 de UR269. **Refuta:** ninguna pareja, o ninguna suma exacta.
- *Fuente:* `13_sistema_incahuasi/informe.md` §predicción; `18_equipo_rojo` §4; `ds/n_fuera_muestra`.

**11. Otra tabla de 9 columnas en Inkawasi (ají o frijol).**

- **Predicción:** si las 9 columnas son unidades sociales genéricas (pachacas de una guaranga), una tabla de 9 de otro producto mostrará **el mismo perfil ordenado**: c1 ≈ c2 son las mayores (unos 28 % del total entre las dos), la c8 es la menor y la correlación con la posición está entre −0,6 y −0,8.
- **Confirma:** el mismo perfil. **Refuta:** un perfil distinto. En ese caso las 9 unidades son específicas del flujo del maní.
- *Fuente:* `ds/n_nueve_partes` §9; `ds/n_nueve_unidades`.

**12. Quipus del sector B (PAI-2016-1 a 4 y 1464; Jiménez 2021) y lote JC.**

- **Predicción:** **no** se conectan aritméticamente con la cadena del sector A. Es lo que ocurre con los 23 quipus JC del sector B: torsión Z y valores pequeños.
- **Refuta:** sumas o copias exactas hacia UR266, UR275 o UR269.
- *Fuente:* `13_sistema_incahuasi` (negativos); SINTESIS, primera ronda de agentes.

**13. Huacones-Vilcahuasi, bajo Cañete (Barraza, Areche y Marcone 2022).**

- **Predicción (especulativa, de prioridad baja):** si los quipus 8 y 9, con 9 colgantes cada uno, registran las mismas 9 unidades, sus valores descenderán con la posición (ρ < −0,5) y tendrán un CV cercano a 0,2.
- **Refuta:** valores sin orden o muy desiguales (CV > 0,5).
- *Fuente:* SINTESIS, «Búsqueda de Chu y del valle de Cañete».

## C. Documentos coloniales

**14. Bambamarca, visita de González de Cuenca (1567).**

- **Predicción:** en el manuscrito, o en la edición de Espinoza Soriano de 1976–77, las 9 pachacas de la guaranga de Bambamarca aparecen **en el mismo orden** que en la tabla 2 de Pärssinen 1992, con el cacique principal primero y los tributarios 104, 75, 78, 68, 49, 75, 67, 30 y 27.
- **Confirma:** el mismo orden. **Refuta:** otro orden en el documento. Entonces el descenso (ρ = −0,87) es un artefacto editorial y el parecido con UR278 cae.
- *Fuente:* `ds/n_parssinen` §7.

**15. Lista de pachacas de Lunahuaná o de Guarco.**

- **Dónde buscar:** AGI Justicia 432 y 482; Escribanía de Cámara 498-B.
- **Predicción:** si las columnas de UR278 son pachacas de una guaranga local, alguna guaranga del valle tendrá **9 pachacas**, o una estructura de 4 pares más 1 bajo 5 señores. Sus tamaños relativos serán moderadamente desiguales (máximo/mínimo entre 1,5 y 2,5; CV entre 0,15 y 0,4), y los nombres irán por orden de rango.
- **Confirma:** una guaranga de 9 pachacas con esos tamaños. **Refuta:** guarangas documentadas de 8 o 10 pachacas sin ninguna de 9. Rostworowski da para Lunahuaná 4 guarangas y 8 curacas.
- *Fuente:* `ds/n_rostworowski` §8; `ds/n_nueve_partes` §9.

**16. Visita de Guancayo (Chillón, 1571; AGI Justicia 413).**

- **Predicción:** en el manuscrito, el orden de los curacas es Mongoy (2 pachacas), Cancay (1), Chuquitanga (2), Chumbillán (2) y Antachumbi (2), como en la transcripción de Espinoza 1963. Se resuelven además dos dudas: «cinco» frente a «nueve» pachacas, y Maca con 170 o 190.
- **Confirma:** ese orden y 9 pachacas. **Refuta:** otro orden. Entonces el emparejamiento de columnas (1-2)(4-5)(6-7)(8-9) + c3 pierde su ancla documental.
- *Fuente:* `ds/n_espinoza1963` §10.

**17. Cualquier lista colonial de 9 unidades dictada de un quipu.**

- **Predicción de control (riesgo de refutar el modelo):** las listas leídas de quipus que siguen un orden administrativo serán, en su mayoría, de prestigio o jerarquía y **no** de tamaño (mediana de ρ ≈ −0,3). Si aparecieran muchas listas de 9 ordenadas de mayor a menor, el parecido con Bambamarca dejaría de ser especial.
- *Fuente:* `ds/n_parssinen`.

## D. Otros quipus

**18. UR053A–E (Banco Central de Reserva del Perú, Lima): reparto W / R / AB.**

- **Predicción:**
  - en una relectura con los colores comprobados, la cuerda W es la mayor del trío en al menos el 85 % de los tríos de cada quipu;
  - el reparto medio queda en 0,55–0,72 / 0,15–0,27 / 0,12–0,20;
  - A y D **no** son copias de B, C ni E; B ≈ C es copia, con AB como subsidiaria en B y como colgante en C.
- **Confirma:** ese reparto en los cinco. **Refuta:** que en algún quipu R o AB sea la mayor en más del 30 % de los tríos, o que los rojos «R» resulten colores distintos (RL frente a otros) con repartos diferentes.
- *Fuente:* SINTESIS, «UR053A–E como archivo»; `21_ur053/alinear.py`; verificado en `verificar.py`.

**19. Otros quipus del mismo hallazgo de UR053, si existen en la colección del BCRP o en sus registros de adquisición.**

- **Predicción:** mismo vocabulario W/RL/AB y reparto cercano a 4:1:1 aunque cambie la escala.
- **Refuta:** el mismo vocabulario con un reparto distinto, por ejemplo W menor que R.

**20. UR050 (colección Soldi): tres cuentas por cuerda.**

- **Predicción:** en foto con escala, 146 de 163 cuerdas muestran 3 racimos de un dígito (1–9) a alturas relativas fijas, cerca de 0,20, 0,41 y 0,75 del largo.
- **Refuta:** racimos a alturas irregulares, o lo que se transcribió como 3 racimos es un solo nudo largo.
- *Fuente:* SINTESIS, corrección de la familia UR050–055.

**21. Quipus con canutos (UR039, UR050, UR054, UR055, UR110, UR112, UR144).**

- **Predicción:** las fronteras de grupo de colgantes coinciden con las fronteras de canuto en más del 80 % de los casos, como en UR052 (23 de 24).
- **Refuta:** coincidencia al nivel del azar. Entonces el resultado de UR052 queda como caso aislado.
- *Fuente:* `ds/t_canutos_fibra` §8.

**22. Cajamarquilla, UR178, UR179 y UR180 (AMNH).**

- **Predicción:**
  - los nudos «no-axis» de UR179 (54 nudos) y UR180 (30) son nudos simples en serie, sin posiciones decimales: una cuenta de palotes o etiqueta, no signos;
  - UR178 es una secuencia de 57 nudos simples de valor 1.
- **Refuta:** nudos de formas distintas que se repiten con un patrón (inventario de signos), o posiciones decimales claras.
- *Fuente:* `ds/n_no_numericos` §8.

**23. Ceros posicionales medidos en el objeto.**

- **Predicción:** en cuerdas con un cero interno (por ejemplo 105, con la banda de las decenas vacía), el hueco medido sobre el objeto equivale a una banda decimal: la razón hueco / ancho de banda queda entre 0,8 y 1,1, y es casi el doble que la separación entre dos bandas contiguas de la misma cuerda.
- **Refuta:** huecos sin relación con el ancho de banda. Entonces el cero se infirió mal en la transcripción.
- *Fuente:* `ds/t_ceros` §7.

## E. Identidad de objetos y erratas (museo y mantenedores de las bases)

**24. UR1107 y UR237 (Ethnologisches Museum, Berlín) son el mismo objeto,** transcrito dos veces y al revés: largos con r ≈ 0,96–0,99 según el cálculo, 23 de 26 valores exactos y numeración invertida.

- **Dato:** el inventario VA 24370 corresponde a UR1106/UR1107, y Urton (2017, fig. 7.2) lo muestra atado a una barra de madera.
- **Confirma:** UR237 es VA 24370 a/b. **Refuta:** un objeto distinto con cuerdas de largos distintos.
- *Fuente:* `14_copias/verificacion_UR1107_UR237.csv`; `17_okr_pendientes`.

**25. Copias entre museos que deben ser objetos distintos.**

- **Las parejas:** HP055 (Lima, MNAAHP 29934) ≈ UR1084/AS084 (París); AS038/KH0049 (Lima, MNAAHP3550) ≈ UR122 (Göteborg, 1938.45.0228; ver la predicción 29); MM008/015/016 (Basilea, IVc.366.03) ≈ tramos de UR212 (Berlín); UR1175 ≈ UR233 + UR232 (que comparten el inventario VA63038).
- **Predicción:** son objetos físicamente distintos, con largos y torsiones diferentes. Las diferencias listadas en `14_copias/verificacion_*.csv` son nudos de más o de menos en el objeto, no errores de lectura. En concreto, HP055 tiene 8 de las 14 cuerdas de valor 222 que faltan en UR1084.
- **Refuta:** que sean el mismo objeto (duplicado de base), o que las diferencias desaparezcan al releer.

**26. Erratas de las bases.**

- **Predicciones:**
  - KH0676 es Brooklyn Museum 36.718, no 80.1012;
  - AS008 tiene una cuerda de valor 17 612 que falta en KFG;
  - los archivos KFG de KH0197, KH0227, KH0267 y KH0350 contienen los datos de KH0198, KH0228, KH0268 y KH0351;
  - AS081, que el *Databook* declara sin interpretación numérica, no debería tener valores.
- **Confirma:** el cotejo con las hojas originales o con los mantenedores (OKR/KFG).
- *Fuente:* `ds/n_okr_resto`; `ds/t_okr_vs_kfg`; `ds/n_databook`.

## F. Frontera, copias y desajustes (rondas 17–18)

Estas predicciones se fijaron el 18-10-2026, después de ver los datos (post hoc). Son más débiles que las de las secciones A–E por ese motivo.

**27. UR234 g5, cabecera rota (Ethnologisches Museum, Berlín).**

- **Predicción:** la cabecera rota del grupo 5 vale **2016** (`2S,2000; 1S,10; 6L,6`).
- **Por qué:** UR1104 (AS104, Berlín, Pachacamac) reproduce en orden las cabeceras de UR234 g0–g8 (2007, 2080, 3102, 2247, 2578, **2016**, 3419, 3159, 1407; UR234: 2007, 2080, 3012, 2247, 2578, rota, 3419, 3159, 1407). Hay 7 exactas, una variante (3102 frente a 3012: el mismo nudo en otra posición decimal) y la cabecera rota. Es el tipo «extracto de un campo».
- **Confirma:** restos de nudos o huella de 2016 en la cuerda rota. **Refuta:** otro valor legible. Adicional: releer UR234 g2 (¿3012 o 3102?) y la misma cabecera en UR1104.
- *Fuente:* `analisis/33_estematica/informe.md`; `verificar.py` (comprobación 11).

**28. UR108 (Lima, Temple Radicati) frente a la cuerda 9 de UR231 (Berlín), y la unión VA16135a/b.**

- **Predicción:** los valores de UR108 coinciden con la cuerda 9 de 5 de las 6 secciones grandes de UR231 (5/6 exactas); UR108 sería un extracto de campo, como UR1104.
- **Nivel:** propuesto (post hoc). UR108 tiene solo 7 cuerdas, así que el orden aporta poco (1/60).
- **Confirma:** que la sexta sección también coincida al releerla. Si se sostiene, apoya que los fragmentos VA16135a y VA16135b son un solo quipus (hay que comprobar la unión física en el museo). **Refuta:** que las cinco coincidencias se deban a lecturas erróneas.

**29. UR122 (Göteborg 1938.45.0228) frente a KH0049 (Lima, MNAAHP3550).**

- **Predicción 1:** las cuerdas de UR122 en 0 donde KH0049 tiene valor están **rotas o sueltas** en el objeto. En el bloque p19–p36 hay 12 posiciones así; las tres primeras son p21–p23 (KH0049: 487, 281, 661).
- **Predicción 2:** **KH0049 B1[1] (la cuerda 19 de la tabla) se lee 15652.** B3 + B4 + B5 da 15649, y B0 − B2 también. La discrepancia está en las dos copias, así que viene del original (como 2904/2908 en Puruchuco).
- **Confirma:** huellas de cuerdas rotas; 15652 en la relectura. **Refuta:** cuerdas íntegras y en 0 en UR122, o 15649 en KH0049.
- *Fuente:* `analisis/30_frontera_estructura/07_ur122_kh0049.py`, `novedad_kh0049.md`; `verificar.py` (comprobaciones 10).

**30. Relectura de UR040 (Peabody) y UR167 (AMNH).**

- **Predicción:** la alternancia de dos colores A/B/A/B (W/AB en UR040: 26 de 33 posiciones; AB/MB en UR167: 30 de 37) se conserva en otra lectura. Los valores son casi todos 0 o 1, así que lo que hay que comprobar son los mismos colores en las mismas posiciones, no el valor.
- **Refuta:** que otra lectura rompa la alternancia o lea los colores sin patrón.
- *Fuente:* `analisis/30_frontera_estructura/informe.md` §5.

**31. UR278: nudos largos de las celdas con desajuste ±1.**

- **Predicción:** en las filas g13, g17, g19, g21 y g29 de UR278 (desajuste libro − detalle de +1, −1, +1, −1, −1) el error está en el **conteo de vueltas de un nudo largo de unidades**. 6 de los 7 desajustes caen en las unidades (p ≈ 0,007, nulo aproximado). Hay que contar las vueltas de los nudos largos de esas filas. Las candidatas por fila (18–43 por fila, salvo g21) están en `analisis/ds/n_casi_aciertos/informe.md` y `reparaciones.csv`; g21 ya está en la predicción 1.
- **Confirma:** vueltas que, corregidas en una celda, cuadran la suma con el libro. **Refuta:** nudos largos claros y completos en todas las celdas; sería entonces una discrepancia real del registro.
- Los otros dos desajustes (g8, +6; g12, +100) no son de este tipo: ver la predicción 4 y la escalera 4/5/6 de `n_casi_aciertos` §3.3a.
- *Fuente:* `analisis/34_comparada/desajustes.py`; `verificar.py` (comprobación 12).

**32. UR278 g29 (1507) frente a g1 (1506): ¿registro duplicado?**

- **Predicción:** la fila g29 de UR278 suma 1507 y enlaza con UR266 g2 = 1506, que ya es el destino exacto de g1. Se prevé que g29 sea un **duplicado** de g1 (un grupo atado o copiado dos veces) o que tenga un nudo de más.
- **Confirma:** que las 9 celdas de g29 coincidan con las de g1 salvo en una, o que el grupo sea físicamente repetido. **Refuta:** que sus celdas difieran de g1 en varios sitios y que haya otro destino en el libro. Nota: no hemos comparado celda a celda g29 con g1; es una predicción por el destino compartido.

---

## Predicciones que ya fallaron (para que conste)

- **UR050 + UR055 como par de quipus de ceques** (prerregistrada): fallaron las tres predicciones (rachas de color, ciclo de 3, fibra y colección). `n_plantillas/predicciones_preregistradas.md`.
- **Orden del padrón del Santa (1670) frente a los quipus:** p = 0,24 con el nulo correcto.
- **UR267A + UR267B → UR269:** cae fuera de muestra (Holm 0,50).
- **Tasa de Guancayo:** no hay en el corpus ningún quipu con la forma «9 productos × 9 pachacas iguales».
