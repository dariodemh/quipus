# Análisis computacional del corpus de quipus: resumen para revisión especializada

*Abierto a revisión especializada, 18-10-2026. Todavía sin revisión de pares; las correcciones son bienvenidas como [issues](https://github.com/dariodemh/quipus/issues).*

## 0. En una página

Pasamos todo el corpus digital de quipus (unos 650 objetos, 57 818 cuerdas) por pruebas estadísticas con nulos por permutación y corrección por comparaciones múltiples. El resultado principal está en el archivo de Inkawasi (Incahuasi, Cañete):

- **Bien apoyado.** En el montón de catorce quipus cubiertos de maní de la kallanka del sector A hay una **consolidación de tres niveles**:
  - el colgante más la primera subsidiaria de UR270 dan, columna a columna, las celdas de la tabla de 9 columnas de UR278;
  - los totales de fila de UR278 reaparecen, en el mismo orden, como cabeceras de los libros UR275 y UR266.

  Ninguna de estas dos relaciones está publicada. Las dos se recuperaron en una prueba ciega sobre datos anonimizados.
- **Apoyado, sin demostrar.** La pareja atada UR273A/UR273B, sumada registro a registro, llega a las mismas cabeceras por una segunda vía.
- **Ya estaba publicado** y aquí solo se replica: las cuotas fijas 10, 15, 47 y 208, y las copias UR255≈UR267A, UR256≈UR267B y UR266≈UR275 (Urton y Chu 2015, 2018; Urton 2017).

Fuera de Inkawasi, los resultados son sobre todo negativos o metodológicos:

- el 74 % de quipus con sumas no es informativo;
- no hay léxico de color compartido;
- no hay rastro de texto silábico;
- las plantillas de géneros coloniales no superan el azar.

Aparecen además algunos formatos de archivo, como el conjunto atado UR053A–E con un reparto W/R/AB estable, y una lista de erratas de las bases de datos.

**Para qué le escribimos.** Lo que no podemos hacer desde los datos es mirar los objetos y los documentos. KFG y OKR, en Inkawasi, son dos codificaciones de **la misma lectura**, hecha por la misma transcriptora. Adjuntamos predicciones congeladas que solo puede comprobar alguien con acceso a museos, fotografías o archivos (`predicciones_verificables.md`).

## 1. Datos

- **KFG** (Khipu Field Guide, datos del artículo de Medrano y Khosla 2024; Zenodo v2.1.0): 651 quipus y 57 818 cuerdas. Usamos 650, porque UR044 es un duplicado de AS031/KH0033. Cada cuerda trae su cadena de nudos, valor, color, torsión, unión (R/V), largo y terminación. En 57 789 cuerdas, el valor es exactamente la suma de los aportes de los nudos.
- **OKR** (Open Khipu Repository, Zenodo v2.1.0; `khipu.db` con 619 quipus, 702 números KH). Lo usamos para contrastar KFG y, en Inkawasi, como base preferente: KFG pierde 111 cuerdas de ese archivo, entre ellas 58 de UR256 y 32 subsidiarias de UR274B. Recuperamos además 19 quipus de hojas xlsx/PDF que no están en las bases (776 cuerdas).
- **Concordancia KFG–OKR:** 99,33 % de valores idénticos. El 86 % de las discrepancias se concentra en cinco quipus (UR090, UR144, UR235, UR193 y UR190), y la mitad son errores de factor 10.
- **Fuentes textuales cotejadas** (texto completo salvo indicación):
  - Urton y Chu 2015 con su suplemento, Urton y Chu 2018 (inglés y español), Urton 2017 (cap. 9 y apéndice) y Urton y Brezine 2005;
  - Medrano 2019 (tesis) y Medrano y Khosla 2024;
  - Pärssinen 1992 y la introducción de Pärssinen y Kiviharju 2004;
  - Rostworowski, *Costa peruana prehispánica*, y Espinoza Soriano 1963 (visita de Martínez Rengifo, 1571);
  - Hyslop 1985, LeVine (ed.) 1992, Salomon 2004, *Narrative Threads* 2002, Hyland 2017 y Curatola y de la Puente 2013;
  - FitzPatrick 2024 y Chu 2015–2018.
- **Límite de los datos.** La columna `alt` está vacía. KFG pierde casi todas las cuerdas superiores de nivel 1 (92 de 95) y todas las marcadoras (502 de 502), así que los análisis de superiores y marcadoras se hicieron con OKR. No hemos visto ningún objeto.

## 2. Métodos

1. **Nulos por permutación adaptados a cada pregunta.** Se barajan valores dentro del nivel, del grupo o de la magnitud, según lo que se ponga a prueba. Lo aprendimos con un error propio: un nulo «sustituye por un valor del corpus» infla cualquier suma, y uno que baraja entre quipus deja intactas las copias.
2. **Corrección múltiple.** Holm o Benjamini-Hochberg sobre la familia completa de pruebas. Cuando una regla se eligió mirando los datos (cómo alinear, qué pareja probar), contamos todas las variantes posibles («jardín de senderos»). El equipo rojo recalculó así la relación A+B sobre 58 782 pruebas.
3. **Mitades de exploración y confirmación,** y validación cruzada por bloques de registros.
4. **Prueba ciega.**
   - Se anonimizaron 52 quipus de Inkawasi (Q01–Q52), se ocultó el 15 % de las cuerdas anudadas (597) y se pidió a modelos de lenguaje sin acceso a la literatura que predijeran valores y buscaran relaciones.
   - Después, en pruebas dirigidas, se fijaron por escrito la regla, el nulo y la corrección antes de abrir los datos.
   - Las respuestas se puntuaron sin dar retroalimentación al modelo.
5. **Controles positivos.** Todo detector se probó primero con relaciones conocidas, para medir su potencia:
   - la jerarquía de Puruchuco de Urton y Brezine (2005), que el método reproduce literalmente, incluidas las discrepancias 2904/2908 y 161/162;
   - las copias publicadas por Urton (2005);
   - UR006/UR009/UR021;
   - el padrón del Santa;
   - listas insertadas artificialmente.

   Varios negativos se interpretan como «no detectable con esta potencia» y no como «no existe».
6. **Predicciones prerregistradas** antes de mirar los datos que las ponen a prueba. Por ejemplo, la hipótesis de ceques para UR050 + UR055 se registró antes y falló sus tres predicciones.
7. **Escala de evidencia.**
   - **Bien apoyado:** sobrevive al nulo y a la corrección, y se replicó por una vía independiente (otro script, otro agente o prueba ciega).
   - **Apoyado:** significativo con corrección, pero sin réplica independiente, o frágil ante la elección de la regla.
   - **Propuesto:** compatible con los datos, sin prueba que lo distinga de alternativas.
   - **Especulativo:** sin prueba.

## 3. Hallazgos por nivel de evidencia

Los identificadores entre corchetes remiten a `tabla_hallazgos.csv`.

### 3.1 Bien apoyado

**Inkawasi, sector A, montón del maní (U.A. 4, U.E. 11–22).**

- **[I01] UR270 → UR278, celda a celda.** El colgante más la primera subsidiaria de UR270 coincide con las celdas de una fila de UR278, en el mismo orden de columnas.
  - Cinco de doce grupos tienen 6–9/9 coincidencias, y dos coinciden 9/9: el g0 de UR270 con el g21 de UR278 (237, 295, 138, 198, 201, 153, 106, 138, 187) y el g4 con el g25.
  - Con solo los colgantes, ningún grupo llega a 6/9 (p = 0,0002).
  - Lo replicaron un script independiente y una revisión manual. Un modelo ciego, sin conocer la identidad de los quipus ni nuestra regla, encontró la misma relación con la misma regla (p ≈ 3·10⁻¹⁰).
- **[I02] UR278 → UR275 → UR266.** Los totales de las filas de 9 de UR278 reaparecen en el mismo orden como cabeceras.
  - En los colgantes blancos de UR266: 11 coincidencias exactas frente a 0,4–0,5 esperadas (Holm 1,6·10⁻⁹; ρ = 1).
  - En los totales de grupo de UR275: 7 frente a 0,5 (Holm 2,8·10⁻⁴).
  - Ejemplos: 3618 (= 415 + 415 + 353 + 415 + 415 + 415 + 414 + 413 + 363), 1506, 1384, 2919, 2089, 2950, 1278.
  - La relación se confirmó en prueba ciega dirigida, con la regla congelada de antemano.
- **[I09–I10] Las 9 columnas son 9 unidades con identidad fija.**
  - Son las mismas 9, en el mismo orden, en UR270 y UR278: la identidad es la mejor de las 9! permutaciones en los 5 registros comparables.
  - Su planitud es excepcional en el corpus. El CV entre medias de columna es 0,17–0,19 según la definición, y 7 de los 8 grupos de 9 cuerdas con CV < 0,2 de todo el corpus son de UR278.
- **[I06, I18] Replicamos lo publicado:**
  - las cuotas fijas 10, 15, 47 y 208, con la fórmula «total = fijo + resto»;
  - las copias UR255≈UR267A, UR256≈UR267B y UR266≈UR275.

**Resto del corpus.**

- **[C03] Cuerda superior = suma del grupo inmediatamente anterior:** 23 de 72 frente a 2,4 esperadas (Holm 0,0035). El fenómeno es conocido desde Locke. Lo nuevo es que la suma corresponde al grupo anterior y no a uno cualquiera.
- **[C04] Formato «fila + cuerda-total suelta»:** 51 aciertos frente a 14,9 (p = 0,0005), con siete quipus significativos (AS044, AS066, AS199, UR1096, UR118, UR119 y UR166).
- **[C06] El color funciona como categoría con clave local.**
  - Predice la magnitud dentro del quipu en 167 de 403 (unos 20 esperados), y en 103 aun barajando el color dentro de cada grupo.
  - No hay léxico compartido entre quipus ni entre sitios (p = 0,34 y 0,79).
- **[C24, C26] Datos.**
  - Copias entre museos no señaladas en la literatura que revisamos; por ejemplo, HP055 (Lima) ≈ UR1084/AS084 (París), con 121 de 142 cuerdas exactas.
  - Erratas concretas de las bases. Cuatro archivos de KFG (KH0197, KH0227, KH0267 y KH0350) contienen en realidad el quipu siguiente. KH0676 es Brooklyn 36.718, no 80.1012. UR1107 y UR237 son el mismo objeto registrado al revés.

### 3.2 Apoyado

- **[I03] Pareja atada UR273A + UR273B.** Alineadas por número de grupo (los separadores rosados caen en los mismos grupos), sus sumas dan 8 de 18 cabeceras exactas de UR266, UR275 y UR269 (2950, 1653, 1737, 1827, 1780, 2247, 1765 y 1506; 1,27 esperadas).
  - Sobrevive a la corrección por elección de regla (p = 0,015) y a la división en mitades (5/9 y 3/9; Holm 0,016).
  - En la prueba ciega dirigida sobre 132 600 tríos, la pareja queda entre los cinco primeros puestos, pero no supera la corrección de Holm (0,93).
  - **Nivel: apoyado, no bien apoyado.** Converge con [I02]: las sumas A+B y las filas de UR278 caen en los mismos totales.
  - **[I04]** Cuando UR273A está en blanco, UR274A ocupa su lugar en 3 de 4 registros (p = 0,00013).
- **[I11–I14] Perfil de las 9 columnas.**
  - Es desigual y ordenado de mayor a menor (Spearman −0,73; p = 0,025).
  - No se comporta como demografía ni como tiempo: el CV es demasiado bajo para una pirámide y no hay estacionalidad.
  - Sus proporciones predicen filas no vistas (Holm 0,002).
  - De las nueve listas coloniales de 9 unidades que cotejamos, la única que desciende como UR278 es la de las **9 pachacas de la guaranga de Bambamarca** (visita de González de Cuenca, 1567, según la tabla 2 de Pärssinen 1992): ρ = −0,87 (Holm 0,005). Bambamarca es más desigual: CV 0,39 frente a 0,19.
- **[I15] Emparejamiento según los curacas de Guancayo (Chillón, 1571).** El orden de los curacas (2+1+2+2+2 pachacas) predice pares de columnas con 11 igualdades exactas frente a 4 (p = 0,0003). No hay covariación (r = 0,09), y si se cuentan los 945 emparejamientos posibles la p sube a 0,086. **Apoyado, frágil.**
- **[I08] La cuota es absoluta, no proporcional.** 47 representa entre el 1,1 % y el 4,2 % del registro; el «~2 %» de Urton y Chu 2018 es un promedio.
- **[I16–I17] Predicción ciega.**
  - Dejando una cuerda fuera cada vez, el modelo acierta exactamente el 58,8 % de las cuerdas predecibles, frente al 20,5 % de la mejor línea base.
  - En las cuerdas que no intervinieron en el descubrimiento, la ventaja casi desaparece: 17,5 % frente a 15,1 %.
  - En la prueba ciega, un modelo predijo 68 cuerdas ocultas con 82 % de exactas y estaba bien calibrado.
  - Lectura honesta: **leemos la aritmética de la cadena, no el archivo entero ni su contenido.**
- **[C07] Conjunto atado UR053A–E** (Banco Central de Reserva). Los cinco quipus reparten las tres cuerdas W / R / AB en proporciones parecidas, cercanas a 4:1:1 (W entre 0,57 y 0,70), aunque sus totales van de 1 200 a 36 800. W es la mayor del trío en 13 de 14 tríos (UR053A) y en 23 de 23 (UR053D). No es una suma. Es un segundo caso, independiente de Inkawasi, de «formulario de archivo con clave de reparto estable».
- **[C09] Ceros posicionales.** En 726 cuerdas con un cero interno, el hueco mide una banda decimal (mediana 0,96; 1,89 veces el ancho de banda dentro de la misma cuerda; p = 6·10⁻³³). Es evidencia contra la tesis no posicional de Florio y Overmann (2025), con una salvedad: la asignación de valor a los nudos es en parte circular.
- **[C10] Los canutos son el sistema de fijación.** El 97,6 % de las cuerdas está dentro de un canuto, con unos 4 colgantes por canuto. En UR052, 23 de 24 fronteras de grupo coinciden con fronteras de canuto (p = 5·10⁻⁵), pero es un solo objeto.
- **[C01–C02] El 74 % de quipus con sumas (Medrano y Khosla) no es informativo.**
  - Entre el 93 % y el 100 % de las relaciones de KFG son esperables por azar.
  - La métrica solo tiene un 24 % de potencia.
  - Solo unos 20 quipus (3 %) tienen contabilidad interna verificable.
- **[C12, C13, C14, C18, C19, C23] Negativos bien sostenidos.**
  - No hay mitades especulares.
  - Solo el 100 está sobrerrepresentado como valor.
  - El emparejamiento del padrón del Santa de 1670 no sobrevive a un nulo correcto (p = 0,24). Además, la p = 0,03 de FitzPatrick es la mejor de 20 alineaciones.
  - Las cuerdas no se comportan como texto, y el silabario de Sivan falla sus propias predicciones.
  - Los quipus no numéricos tienen alfabetos de 5 a 19 colores, muy lejos de los 60–120 signos de un silabario.
  - Ningún quipu antiguo alcanza el inventario de signos de Collata.

### 3.3 Propuesto o especulativo

- **[I07] Cuotas que se suman en la consolidación:** 30 + 17 = 47, y 15 + 10 = 25. El 17 es explícito en UR274B (con OKR, p = 0,004) pero casi no aparece en UR273B. La relación UR267A + UR267B → UR269, que sostenía el 25, **no** superó las pruebas fuera de muestra.
- **[I20] Unión R/V opuesta en las dos mitades de cada pareja atada.** Se cumple en las tres parejas de Inkawasi, pero en el corpus solo en 6 de 14 pares A/B (p = 0,16). Es una convención de archivo propuesta.
- **Qué son las 9 columnas.** Proponemos 9 pachacas o subunidades de una guaranga, ordenadas por rango o tamaño. No hay ningún 9 documentado en Lunahuaná ni en Guarco. «P = cuota, S1 = entrega» en UR270 está en prueba.
- **Unidad.** Abierta, con dos hipótesis que los datos no separan: **carga** (~80 L, ~23 kg; unidad andina; preferida levemente, propuesta) y **fanega** (~56 L, ~16 kg; medida castellana). La capacidad de los depósitos solo excluye unidades muy pequeñas. El total sería de **~900–1 400 t**, solo orden de magnitud (10²–10³ t). No damos una cifra firme: depende de la unidad.
- **UR050** sería una tabla de 163 filas × 3 zonas a alturas relativas fijas, compatible con el subtipo B1-b de Mackey.
- **UR1140** (Berlín, Nazca) sería una ficha de 7 campos.

### 3.4 Hallazgos de las rondas 17–18 (fuera de Inkawasi, salvo los desajustes)

**Una tabla jerárquica en la costa sur: KH0049.** *Apoyado (post hoc).*

- KH0049 (AS038/HP036, Museo Nacional, Lima, MNAAHP3550, costa sur) es una **tabla de tres niveles en bloques de 18 cuerdas**: B0 = B1 + B2 en 14 de 18 posiciones exactas y B1 = B3 + B4 + B5 en 7 de 18 (el nulo da como máximo 6 y 4; p = 5·10⁻⁵).
- UR122 (Göteborg, 1938.45.0228) es una copia parcial: la sección de subtotales, con el 58 % de las cuerdas rotas o en 0.
- La discrepancia **15652 frente a 15649** está en las dos copias; viene del original.
- **Publicación.** Parcial: el Khipu Field Guide lista 15 sumas indexadas de KH0049 como salida automática, sin describir la jerarquía ni UR122 (`analisis/30_frontera_estructura/novedad_kh0049.md`). No hemos podido leer Ascher y Ascher 1978 ni Pereyra Sánchez 2011.
- Es un segundo caso de «total por columna» fuera de Inkawasi.

**Alternancia de dos colores.** *Bien apoyado en UR040 y UR167 (Holm 0,025); apoyado en UR1033F (q 0,010).*

- Pares de cuerdas de dos colores intercalados (A/B/A/B), la única estructura de la frontera de 180 quipus que se replicó en la mitad de confirmación (q 0,003). Se lee como una tabla de dos columnas escrita intercalada.
- Hay 19 quipus así en el corpus; 15 ya eran TAB/FOR. En UR040 y UR167 los valores son casi todos 0 o 1: el formato es seguro, el contenido no.
- De los 180 quipus de la frontera solo 3 dejan de serlo (4 con KH0049). **El resto son listas decimales sin estructura recuperable con estos datos.**

**Copia nueva: UR1104 → UR234, un «extracto de un campo».** *Apoyado (post hoc); la fuerza es la de bien apoyado.*

- UR1104 (AS104, Berlín, Pachacamac) reproduce en orden las cabeceras de nueve registros de UR234: 7 exactas, una variante (3102 frente a 3012) y la cabecera rota de UR234 (2016). Es un resumen que sube de nivel, tomando el campo mayor del formato Nazca/Berlín.
- UR108 → UR231 es parecido (5 de 6; propuesto).

**La copia como rasgo de archivo.** *Apoyado.* Dentro de un sitio hay 10 pares en 6 820; entre sitios, 6 en 72 980 (OR 17,9; p = 10⁻⁷). En los archivos casi completos, el 14–20 % de los quipus tiene copia (5,5 % en el corpus; cota inferior). Tipos: duplicado, copia por tramos, otro desglose y extracto de un campo. La dirección es indecidible en casi todos los pares.

**Un libro perdido α entre UR278 y UR266/UR275.** *Propuesto.* Los ±1 compartidos por las dos copias del libro indican un paso intermedio, no conservado, entre el detalle y el libro (error conjuntivo). Es, junto con KH0049/UR122, uno de los dos nudos firmes de dirección de copia.

**Los desajustes de UR278 son error de conteo de vueltas.** *Apoyado (n chico).* De 18 filas con destino, 11 son exactas y 7 no (39 %). Los desajustes (libro − detalle) son +6, +100, +1, −1, +1, −1, −1: sin dirección (4+/3−). 6 de 7 caen en las unidades (p = 0,007; nulo aproximado), la firma de un nudo largo mal contado, no de una convención (que daría signo o magnitud constantes). Las dos copias del libro coinciden en todos: la diferencia nace en el paso detalle → libro.

**«La cuerda mayor abre el grupo» (P5c).** *Apoyado, nuevo.* Fuera de Inkawasi, el valor mayor va primero en el 25,9 % de los grupos frente al 15,2 % esperado (Holm 0,002). En UR278 las columnas son decrecientes (tau −0,41; bien apoyado).

**Cuadre por dos caminos.** *Propuesto, con analogía débil.* No está documentado en Uruk ni en Pilos (Nissen, Damerow y Englund 1993). Lo tratamos como rasgo propio de Inkawasi. Sí hay paralelo documentado en la jerarquía de documentos, el formato fijo por tipo y las copias.

**KFG y OKR son la misma lectura** (99,9 % de coincidencia en los UR). Las únicas lecturas independientes son tres duplicados de un mismo objeto, y dan un ruido de lectura del 3–12 %. Es una estimación con pocos datos.

## 4. Qué es nuevo y qué ya estaba publicado

| Nuevo, sin publicar (según nuestra revisión) | Ya publicado y solo replicado |
|---|---|
| UR270 → UR278 celda a celda; totales de UR278 → UR275/UR266; UR273A+B → libros; UR274A sustituye a UR273A | Pares atados con valores parecidos; UR255/UR267A y UR256/UR267B; UR266≈UR275 (Urton y Chu 2015; Urton 2017) |
| Identidad, planitud y perfil ordenado de las 9 columnas; parecido con Bambamarca; pares de Guancayo | UR278 «organized in sets of 9 cords» (suplemento de 2015) |
| La cuota como valor absoluto; cuota 46; 30 + 17 = 47 como suma | Cuotas fijas 10, 15, 47 y 208; 17 y 30 considerados y rechazados (Urton y Chu 2018) |
| Formato «fila + total suelto»; orientación de la cuerda superior al grupo anterior | Cuerdas superiores sumatorias (Locke 1927; Ascher y Ascher) |
| Reparto estable W/R/AB en los cinco quipus de UR053 | Patrón W/RL/AB en los cinco y pareja UR53B/C con formato distinto y R/V opuesta (Urton 2017, cap. 8) |
| KH0049 como tabla jerárquica y UR122 como su copia; alternancia A/B/A/B; UR1104 → UR234 (extracto de un campo); la copia como rasgo de archivo; «la cuerda mayor abre el grupo» | Cuerdas superiores sumatorias y sumas de Ascher (Locke 1927; Ascher y Ascher 1981); en KFG, la lista automática de 15 sumas de KH0049 |
| Cero = banda vacía; canuto = fijación; nulo correcto para el Santa; erratas de las bases; copias entre museos | Seriación de color en el Santa (FitzPatrick 2024); estructura de UR006 (Urton 2017, cap. 4); jerarquía de Puruchuco (Urton y Brezine 2005) |

**Lo que no reclamamos:**

- que haya cadenas contables entre quipus, publicadas en Puruchuco y en UR006;
- que el sistema de Inkawasi sea «exclusivo»: lo nuevo es su **arquitectura concreta**;
- la interpretación fiscal de las cuotas, que es de Urton y Chu.

Las fuentes más próximas a cada hallazgo, y por qué no lo contienen, están en `antecedentes.md`.

## 5. Correcciones que hicimos sobre la marcha

1. **«El 74 % no se distingue del azar» pasó a «no es informativo».** Con potencia de ~24 %, la métrica no prueba ni refuta la contabilidad.
2. **UR006.** Primero dijimos que no reproducía la estructura de Urton. Contando las cuerdas-lazo sí la reproduce: 24 pares, 729 cuerdas y 45 de 48 sumas. La lectura calendárica sigue siendo propuesta.
3. **UR278 → UR266.** «16 de 33 en orden» bajó a 15 y después a 11, la cifra que replicaron el script independiente y la prueba ciega. Tampoco es cierto que fuera «la única relación entre quipus del corpus»: el método reproduce Puruchuco.
4. **UR273A+B (H1)** bajó de bien apoyado a apoyado. **UR267A+B → UR269** bajó a no bien apoyado. **30 + 17 = 47** bajó a propuesto. La «posición en el bloque de UR269» se retiró: se explicaba por la magnitud.
5. **UR270 → UR278 (H2)** subió de apoyado a bien apoyado tras la prueba ciega.
6. **Unión R/V.** Pasó de «código bien apoyado» a **convención de archivo propuesta** (6 de 14 en el corpus).
7. **Compensación UR054/UR055, retirada.** Las zonas en centímetros daban p = 0,0002, pero con alturas relativas al largo de la cuerda la p sube a 0,76 y 0,44. De esa familia solo se sostiene UR050.
8. **UR053B ≈ UR053C** es una copia ya conocida, publicada por Urton (2017, cap. 8) y registrada en nuestra crítica de copias. Una tarea intermedia dijo «no son copias» porque comparó por posición.
9. **Santa.**
   - Nuestra p = 0,0056 era circular; con el nulo correcto es 0,24.
   - La seriación de color de los quipus del Santa ya la publicó FitzPatrick 2024, así que la retiramos como novedad.
   - KH0227 (Huaura) y UR198 (Nazca) estaban mal asignados al Santa por el nombre.
10. **Copias y cuotas ya publicadas.** Las copias de Inkawasi y las cuotas 10, 15, 47 y 208 las tratábamos como nuestras hasta leer Urton y Chu 2015 y 2018.
11. **Modelo de error de transcripción.**
    - Que una discrepancia se pueda reparar con un solo cambio de nudo no prueba que sea un error de transcripción: ocurre 31 veces de 35, frente a 28,3 esperadas.
    - La «escalera de copias» 2433 → 2533 → 2633 pierde fuerza, porque 2633 también aparece en UR269.
    - **Corrección de este paquete:** las cuatro cuotas «10» de UR274B no son exactamente las cuatro cuerdas más cortas. Están entre las cinco más cortas: una mide 25,0 cm y la cuota de 17 más corta mide 24,5 cm. La probabilidad por azar pasa de 5,5·10⁻⁴ a unos 3·10⁻³.
12. **Unidad y tonelaje de Incahuasi.** Habíamos escrito «~1 390 t» y «82 L» con demasiada precisión. La cifra salía de un bulto de 82 L que era solo propuesto (despejado de la capacidad del depósito, que da 5 090 o 8 300–13 000 m³ según el cálculo). La unidad es indecidible entre carga (~23 kg) y fanega (~56 L); el total es ~900–1 400 t, solo orden de magnitud.
13. **«54 % de fallos» de UR278 → libro.** Eran 13 de 24. Son 26 filas, 8 sin destino; de las 18 con destino, 11 exactas y 7 desajustes (39 %).
14. **KH0049 y la novedad.** La pregunta «¿está publicado?» da «parcialmente»: KFG lista sus sumas, pero no la jerarquía ni la copia. Mantenemos «apoyado» por ser post hoc.
15. **Guancayo.** La visita de 1571 es del valle del Chillón, no de los wanka de Huancayo. Espinoza 1963 tiene errores de cifras, y su lista de «9 productos» es una selección editorial, no una plantilla nativa.
16. **Barras de madera (corrección de este paquete).** Una tarea presentaba como nuevo que AS124, AS136 y AS140 estuvieran atados a barras de madera talladas. Urton (2017, cap. 7) ya describe entre 12 y 15 quipus en barras así, así que no lo reclamamos.

## 6. Qué le pediríamos

1. **Juicio arqueológico.** ¿Es verosímil que un montón de catorce quipus cubiertos de maní contenga tres niveles de un mismo flujo, más un libro (UR269) organizado por periodos?
2. **Juicio etnohistórico.** ¿Es razonable leer las 9 columnas como pachacas de una guaranga ordenadas por rango? ¿Conoce listas de pachacas de Lunahuaná o de Guarco?
3. **Comprobaciones físicas o documentales** de `predicciones_verificables.md`. Las más baratas:
   - UR278 p180: ¿el último nudo largo tiene 6 vueltas o 7?
   - UR275 p51 y las cuatro puntas de UR274B: ¿falta el 7L terminal?
   - El orden de las pachacas de Bambamarca en el manuscrito de 1567.

## 7. Cifras verificadas para este paquete

Recalculé desde `analisis/datos/cuerdas.csv` (KFG), sin usar los scripts de las tareas, las cifras siguientes. El script es `analisis/paquete_revision/verificar.py` (15/15 correctas).

| # | Cifra | Resultado |
|---|---|---|
| 1 | Unión R/V | UR273A 83 V / 0 R; UR273B 113 R / 1 V; UR267A 82 V; UR267B 103 R |
| 2 | UR273A + UR273B por número de grupo | 18 registros comparables; 8 sumas exactas en cabeceras de UR266/UR275/UR269: 2950, 1653, 1737, 1827, 1780, 2247, 1765, 1506 |
| 3 | UR270 g0 (P+S1) frente a UR278 g21 | 8 exactas; la primera celda difiere en +1 (238 frente a 237) |
| 4 | Totales de fila de UR278 en colgantes de UR266 | 11 exactos en el mismo orden (LCS); fila g0 = 3618 |
| 5 | Cuotas de UR274B | 12 cuerdas de 17 y 4 de 10. Las de 10 miden 20,5, 22,5, 24,0 y 25,0 cm; la de 17 más corta, 24,5 cm. Corrige el «exactamente las 4 más cortas» de `n_casi_aciertos`. |
| 6 | UR275 p51 | Vale 40; hay 24 cuerdas de valor 47 |
| 7 | CV entre medias de columna de UR278 | 0,173 (24 filas completas; máx./mín. 1,64). Los informes dan 0,17–0,19 según la definición. |
| 8 | Bambamarca (104, 75, 78, 68, 49, 75, 67, 30, 27) | ρ = −0,870; CV = 0,385 |
| 9 | Reparto W/R/AB en UR053A–E | A 0,67/0,18/0,15; B 0,57/0,26/0,17; C 0,61/0,23/0,16; D 0,66/0,16/0,18; E 0,64/0,18/0,18. La SINTESIS da dos valores para A: 0,65/0,19/0,16 y 0,70/0,17/0,13. |
| 10 | KH0049, bloques de 18 | B0 = B1 + B2: 14/18; B1 = B3 + B4 + B5: 7/18 |
| 11 | 15652/15649 | KH0049 B1[1] = UR122 B0[1] = 15652; B3 + B4 + B5 = 15649 = B0 − B2 |
| 12 | UR122 en 0 donde KH0049 tiene valor (p19–p36) | 12 posiciones; p21–p23 = 487, 281, 661 |
| 13 | UR1104 frente a UR234 g0–g8 | 7 exactas, 3102/3012, cabecera rota 2016 |
| 14 | Desajustes UR278 → libro | 18 con destino, 11 exactas, 7 desajustes (+6, +100, +1, −1, +1, −1, −1); 6/7 en unidades, p = 0,0069 |
| 15 | UR278 g29 | desajuste −1 (1507 frente a 1506) |

**Comprobado en el texto fuente** (Urton 2017, `fuentes_txt/Urton2017_InkaHistoryInKnots.txt`, líneas 1266–1491): Urton ya describe la pareja UR53B/C, el cambio de formato y la unión R/V opuesta. Lo tratamos como publicado.
