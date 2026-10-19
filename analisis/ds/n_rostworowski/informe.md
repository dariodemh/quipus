# Rostworowski, *Costa peruana prehispánica* (Obras completas III): Guarco, Lunahuaná e Incahuasi

**Equipo:** n_rostworowski · **Fecha:** 18 oct 2026
**Fuente primaria:** `analisis/fuentes_txt/Rostworowski_CostaPeruana.txt` (edición digital IEP, 2016; 5208 líneas).
**Citas:** por número de línea del txt, porque la edición digital no conserva la paginación impresa. Se indica la sección.

---

## 1. Pregunta

¿Qué aporta la lectura detenida de Rostworowski sobre el valle de Cañete (Guarco y Lunahuaná, con Incahuasi/Inkawasi) para nuestras tres hipótesis de trabajo?

1. **Unidad = bulto:** ¿los quipus de depósito cuentan bultos/volúmenes, no ítems?
2. **9 partes = pachacas o periodos:** ¿la estructura de 9 columnas de UR278/UR270 corresponde a unidades sociales (pachacas, ayllus) o a periodos (meses)?
3. **Cuotas = impuesto:** ¿los valores fijos 10, 15, 17, 47, 208 son tasas tributarias, y de qué tipo?

Preguntas secundarias: ¿hay una unidad de 9 en Guarco/Lunahuaná, o un esquema 4 guarangas × 2 = 8 + 1? ¿Qué dicen Cieza y Rostworowski sobre la función, duración, guarnición, depósitos y abandono de Incahuasi? ¿Qué productos y tierras del valle se documentan? ¿Hay menciones de quipus, cuentas, calendario o medidas?

---

## 2. Método y límites

- Lectura por tramos con `grep` y `read`, sin volcar archivos grandes. Se leyeron completos el capítulo 2 («Guarco y Lunahuaná», líneas 517–856, incluidos los dos apéndices documentales) y las secciones sobre Collique (1571), Guancayos (1571), Chincha (mercaderes) y pescadores.
- Extracción sistemática de cifras a `tasas.csv` (61 filas) y de unidades sociopolíticas a `parcialidades.csv` (32 filas), con línea de fuente y nota.
- Cálculo de ratios por tributario y control de aritmética documental (`01_extraer_tasas.py`).
- Dos pruebas de permutación sobre la tabla de 9 columnas de UR278, con semilla fija 20261018 y corrección de Holm (`02_control_9partes.py`).
- **Límite importante:** Rostworowski es etnohistoria, no arqueología de quipus. No describe los quipus de Incahuasi ni sus valores. El puente con UR278/UR270 es analógico y se marca como tal.

---

## 3. Resultados

### 3.1 Guarco: señorío poco documentado, fortalezas y minorías

Guarco ocupaba la parte baja del valle de Cañete, desde Cerro Azul hasta la toma de Palo; Lunahuaná comenzaba en Palo y seguía valle arriba, en el chaupi yunga (líneas 526, 529, 687–688). La frontera ecológica es también política: costa = Guarco; costa media = Lunahuaná; quebradas altas = yauyos mancos y laraos (526).

La organización social de Guarco es, en este libro, **casi un vacío documental**. Rostworowski lo dice expresamente: «se ignora lo relativo a las tierras de curacas y ayllus» para Guarco antes de la conquista inca (617). No hay lista de guarangas, pachacas ni ayllus guarcos. Lo que hay es:

- **Dos encomiendas** tras la conquista: la mitad norte para Antonio Navarro (luego Juan Navarro), con Asia, Oquilla y Calango; la segunda para Alonso Martín de Don Benito, tras pasar por Alonso Díaz y Francisco de Aguirre (680–683).
- **Tres fortalezas**: Guarco/Cerro Azul al norte, Cancharí en el centro, Ungará al sur, más una muralla que cerraba el valle (557–559, 600–608).
- **Minorías étnicas mitmaq**: coayllos del valle de Asia, hasta treinta indígenas con tierras dadas por los incas en Huanca y Lalna (621–632); chinchas cerca del Tambo de Locos, en Herbay Bajo/Alto y Palo (634–636); mochicas en Hualcará, probablemente desterrados por su origen norteño (638–642).
- **Tierras de dioses**: chacras de Pachacamac en Cuyba/Siuba, junto a la acequia Pachacamilla (644–648), y tierras del Sol al norte de Vilcahuasi/Huacones (649–650).

Cerro Azul aporta un dato material relevante para «unidad = bulto»: en la Estructura D, Marcus documentó **al menos nueve vasijas enormes de 700 a 2000 litros** para almacenar líquidos, dos grandes fogones y arena limpia para conservar pescado seco (anchovetas y sardinas) (595–597). No es Incahuasi, pero muestra que el almacenamiento costeño se organizaba por **volumen y contenedor**, no por ítem.

### 3.2 Lunahuaná: 4 guarangas, 8 curacas, ~16 barrios

El señorío de Lunahuaná «comprendía cuatro guaranga» (706). La Visita de 1577 dice que esas cuatro guarangas eran gobernadas por **ocho curacas, dos por cada una**, y Rostworowski sugiere que cada guaranga se dividía en **urin y anan** (dos mitades), de ahí los dos señores (762). Es la única traza explícita de mitades en el valle.

Curacas y unidades nombrados:

- **Lunaguanay**, curaca principal (1534), con residencia en Limas, no en Incahuasi (695–701).
- **Tula**, «principal» en el mismo depósito de 1534 (695).
- **Llaquipa**, señor «residente en las minas» (706).
- **Allauca**, mitmaq, señor de Mullibamba, supeditado a Lunaguanay y gobernando una guaranga (712).
- **Jucxu**, guaranga cuyo curaca en 1580 era **Pedro Camaluana**; la identificación con las guarangas anteriores no es segura (712).
- En 1580 aparece **don Francisco Llacsaguana**, cacique principal y gobernador del valle, y **don Diego Allaucan**, cacique de Pacarán (712).

La lista de barrios actuales que recogió Rostworowski tiene **16 nombres** (Caltopilla, Caltopa, Casalla, Catapaya, Con-Con y Ramadilla, Paullu, Langla, Lunahuaná, Patapampa, Condoray, Uchupampa, Paraíso, Lúcumo, San Pedro, Socsi, San Jerónimo), posiblemente rezagos de antiguos ayllus (716–723). Es una lista de informantes modernos, no un padrón inca.

**No hay una unidad de 9 en Lunahuaná.** Hay 4 guarangas, 8 curacas y ~16 barrios. El esquema «4 × 2 = 8 + 1» no está documentado: el curaca principal está **dentro** de los ocho, no es un noveno; la primera guaranga «correspondía al curaca principal» (706). Añadir un noveno es una inferencia, no un dato.

### 3.3 Tasas de 1577 y 1590: una plantilla por tributario

La Visita de Juan de Vera Olguín (1577) y la revisita de Francisco de Soto (1590) permiten reconstruir la lógica de la tasa. Cifras principales:

| Concepto | 1577 | 1590 |
|---|---:|---:|
| Tributarios totales | 740 | 474 |
| Reservados para caciques | 8 | 5 |
| **Tributarios payantes** | **732** | **469** |
| Viejos | 89 | 96 |
| Muchachos | 601 | 372 |
| Mujeres | 1846 | 973 |
| **Personas totales** | **3276** | **1915** |
| Plata ensayada | 2196 pesos | 1392,34 pesos |
| Ropa de algodón | 366 piezas | 234,5 piezas |
| Maíz / trigo+maíz | 500 fanegas | 641,25 fanegas |
| Aves de Castilla | 758 | 483,5 |
| **Total** | **3660 pesos** | **2330,28 pesos** |

Fuentes: 1577 en 830–851; 1590 en 797–816; síntesis en 762–765.

El hallazgo cuantitativo claro es la **estabilidad de la cuota por tributario payante**:

| Cuota por payante | 1577 | 1590 | Cambio |
|---|---:|---:|---:|
| Ropa (piezas) | 0,5000 | 0,5000 | 0,00 % |
| Aves | 1,0355 | 1,0309 | −0,44 % |
| Plata (pesos) | 3,0000 | 2,9688 | −1,04 % |
| Total (pesos) | 5,0000 | 4,9686 | −0,63 % |

Es decir: **la tasa colonial es una plantilla por cabeza**, no un porcentaje de la cosecha. Entre 1577 y 1590 los tributarios caen 35,9 % (740 → 474) y la población total 41,5 % (3276 → 1915), pero la cuota unitaria casi no cambia; el total baja porque hay menos gente. El propio documento de 1590 compara con una cuenta anterior de **590 tributarios**: 590 → 469 = −20,5 %, «faltan 121» (805). Hay, pues, tres cifras demográficas (740, 590, 469) y no deben fundirse en una sola serie.

**Control de aritmética documental (resultado negativo).** La tasa de 1577 tiene inconsistencias internas:

- Componentes valorados a los precios del documento: ropa 366 × 2,375 = 869,25; maíz 500 × 0,5 = 250; aves 758 × 0,125 = 94,75; **suma = 1214 pesos**.
- El documento dice que las especies valen **1474 pesos** (843), 260 pesos más.
- 2196 + 1474 = **3670**, no 3660; 2196 + 1214 = **3410**, tampoco.
- El total 3660 sí es exactamente **732 × 5 pesos**.
- Rostworowski (762) escribe «1474 + 2196 = 3760»; la suma correcta es 3670. Es un desliz aritmético.

La hipótesis más económica es que falta en la transcripción un rubro de trigo o maíz por unos 250–260 pesos. Para nuestro trabajo, **usar las cantidades físicas y los ratios por tributario, no los totales monetarios de 1577**.

La tasa de 1590 sí cierra: 1392,34 + 556,94 + 320,63 + 60,44 = 2330,34, frente a 2330,28 del documento (diferencia de 6 granos por redondeo).

### 3.4 Incahuasi: función, duración, guarnición, depósitos, mitas, abandono

Rostworowski dedica el apartado «El problema de Incahuasi» (728–760). Lo esencial:

- **Ubicación y forma:** complejo en la quebrada de Lunahuaná, margen izquierda, a 1,5 km de Paullo; tres grupos: El Arca/Acllahuasi al oeste, conjunto principal con «palacio», plaza trapezoidal y ushnu al centro, Colccahuasi y un barrio residencial al este (728–733, 740).
- **Técnica constructiva:** piedra de recolección sin labrar, barro, enlucido; **no** se usaron piedras labradas ni grandes adobes incas; impresión de construcción apresurada (742–744).
- **Fundación:** según Cieza (cap. LIX), lo mandó edificar **Tupac Yupanqui** durante la conquista de Guarco; el inca llamó **Cusco** al lugar y dio a plazas y calles los nombres de la capital (533, 744). La guerra duró tres o cuatro años, con retiradas estivales de los serranos (535, 744).
- **Guarnición:** mientras duró la guerra contra los guarcos hubo guarniciones en Incahuasi; terminada la contienda, la tropa y la residencia real quedaron sin objeto y, según Cieza, **se abandonó** el complejo (745).
- **Continuidad:** Rostworowski matiza: es posible que siguieran en uso los edificios necesarios a la administración inca y el **tambo** para enviados cusqueños; el abandono fue «seguramente solo parcial», porque nadie más que el Inca podía habitar una réplica sagrada del Cusco (745, 760).
- **Ningún curaca vivía allí:** el curaca Lunaguanay residía en Limas; ningún cacique del valle tenía ese privilegio (699).
- **Mitas de diversos lugares:** «debió acudir gente de diversos lugares por sus mitas» (760). Es una afirmación de Rostworowski, no un dato de archivo sobre el número de mitayos.
- **Colccahuasi = colcas:** pequeñas estructuras de paredes altas, sin puertas ni ventanas, a las que se entraba desde arriba; se guardarían **pertrechos de guerra y alimentos**; tras la guerra, el edificio pudo servir de taller/obraje textil (733).
- **Réplica del Cusco:** hipótesis de trabajo; El Arca = Urin Cusco, conjunto central = Anan Cusco, Colccahuasi = Colcampata; el cerro pequeño haría de Huanacauri (754–759). El propio texto la llama «mera hipótesis de trabajo» (760).
- **Carácter:** «un magnífico capricho y un derroche de poderío de un inca», no comparable a Huánuco Pampa o Vilcashuamán (760).

La arqueología de almacenes (LeVine 1992, notas del coordinador; Hyslop 1985; Snead) añade: **202 de unas 250 unidades** del Sector A serían almacenes rectangulares sin puertas, de 3,5–4 m de lado; ocupación breve; posible función de **base militar y acopio estratégico**, abandonada luego en favor de Cerro Azul. Hay una **tensión** útil: la arqueología insiste en la brevedad; Rostworowski propone continuidad administrativa parcial. Para nuestro problema, lo relevante es que Incahuasi fue **un depósito militar de campaña**, no un centro civil permanente.

### 3.5 Productos y tierras

Productos documentados por Rostworowski para Cañete:

- **Coca:** cultivo específico del chaupi yunga, «muy importante para la economía del lugar» (525); las tierras de coca son la franja de 300–1000 msnm (355–364). No se dice que Incahuasi tuviera cocales.
- **Maíz:** base de la tasa (500 fanegas en 1577; 641,25 fanegas de trigo/maíz en 1590), sembrado en tierras del valle (839, 807).
- **Algodón:** 366 piezas de ropa en 1577 y 234,5 en 1590; 26 piezas en el tributo de los guancayos (340, 838).
- **Pescado seco:** producto principal de Cerro Azul/Guarco, conservado en arena; anchovetas y sardinas (596, 686).
- **Guano:** solo como etimología hipotética del nombre Lunaguanay («hombre guanay»), no como producto registrado (696–698).
- **Ají y frijol:** aparecen en la lista de tributos de los **guancayos del Chillón** (340), no en el capítulo de Cañete.
- **Maní:** aparece una sola vez en todo el libro, como ingrediente de la chicha (yuca, maní, etc., línea 3059), **no** como producto de Cañete ni de Incahuasi. La asociación maní–quipus viene de Urton & Chu (2015), no de Rostworowski.

Tierras:

- **Del Inca:** el Estado tomó las mejores tierras; en el Chillón se recuerda cada chacra que fue del soberano, del Sol o de las mamaconas (2597). En Cañete, el Inca tenía chacras y tierras, y los coayllos recibieron tierras «del ynga» (628–630).
- **Del Sol:** tierras en Vilcahuasi/Huacones, al norte del valle (649–650); cultivadas por la población local, con el producto remitido al culto.
- **De Pachacamac:** chacras en Cuyba/Siuba, cultivadas por la población local y remitidas al templo (644–648). Es un **enclave religioso**, no una hacienda estatal.
- **De curacas y ayllus:** para Guarco se ignoran (617); para Lunahuaná no hay padrón, solo nombres de guarangas, curacas y barrios (706–723).

### 3.6 Quipus, cuentas, calendario y medidas

Quipus y cuentas:

- **Censo por quipos:** el Inca mandó que los hombres de 20 a 40 años «estuviesen empadronados por sus quipos» para la guerra (2423). Es un quipu de **población**, no de productos.
- **Cuentas de tributo:** en un juicio de 1572 por Ilo, Arica y Tarapacá, las cuentas de tributos cobrados se declaran «según las declaraciones contenidas en los quipus», con 18 cestos de coca de Carumas y 20 de Arica (2658).
- **Quipucamayoc:** Juan Chauca, «quipucamayoc que fue de Huascar Inca», estima la producción de coca de las chacras estatales en 150–160 costales al año (2601).
- **Otras cuentas:** una instrucción real manda traer «las pinturas y tablas y otras quentas que aya» (5190, n. 22). Es un testimonio de que «quenta» podía designar soportes pictóricos y tabulares, no solo quipus.

Calendario:

- Un testigo indígena declara que el año tiene **nueve meses** (914, 1158–1160). Rostworowski propone, como hipótesis, un **mes de 40 días** (semana de 10 días × 4) y un **año de 9 meses = 360 días + 5** (916).
- Guamán Poma menciona la semana de 10 días; la gramática yunga de Carrera tiene el sufijo **nassop/ssop** para contar días, monedas y fruta (916, 2292). Es decir, el sistema decimal se usaba específicamente para **días, dinero y fruta**, no para todo.
- Cieza afirma que contaban el año «de diez en diez meses» (917); Calancha y Ávila documentan el uso de las **Pléyades/Cabrillas** para regular cosechas y solsticios (921–926).
- Conclusión: en la costa había **varios calendarios simultáneos**; el de 9 meses × 40 días es uno de ellos, no el único (915–920).

Medidas:

- **Runcu:** medida de capacidad para **coca y ají**, usada como unidad en los inventarios de depósitos o tambos; era un cesto grande, con subdivisiones **checta runcu (1/2), cutmu (1/4), sillcu (1/8)**; un cesto de coca pesaba ~20 libras (5154).
- **Fanega:** ~56 L (glosario de LeVine 1992); **almud** = 1/12 de fanega (807, 839); **azumbre** = 2,016 L (5192).
- **Vasijas:** 700–2000 L en Cerro Azul (595); 300–500 galones en Ungará (606).
- **Cestos/costales/petaquillas:** unidades de coca en el tributo y en las cuentas (2601–2606).

---

## 4. Controles cuantitativos

### 4.1 Las 9 columnas de UR278 están equilibradas (T1)

Tabla `ur278_tabla.csv` (28 filas × 9 columnas). 26 filas tienen las 9 columnas completas; la suma de las 9 columnas es **61 790** (coincide con la síntesis del equipo) y la suma de totales de fila es 62 179.

- CV dentro de fila observado: **0,278** (rango 0,059–0,597).
- Nulo: reparto aleatorio del total de cada fila en 9 partes (Dirichlet(1,…,1)), 20 000 permutaciones: CV medio **0,865** (sd 0,045).
- **p < 5 × 10⁻⁵**; Holm (2 pruebas) = 1 × 10⁻⁴.

Las 9 partes no son un reparto arbitrario: están deliberadamente equilibradas. Pero «equilibradas» no significa iguales: la columna mayor (13,6 %) es **1,63 ×** la menor (8,3 %). También es lo que se esperaría si cada celda fuera un **agregado de varias cuerdas**; la prueba no distingue esa posibilidad de la de «unidades sociales».

### 4.2 Las 9 columnas tienen identidad estable (T2)

- Correlación media entre los perfiles de las 26 filas: **r = 0,410** (325 pares).
- Nulo: permutar los 9 valores dentro de cada fila (preserva total y CV de fila): r medio **0,0001** (sd 0,020).
- **p < 5 × 10⁻⁵**; Holm = 1 × 10⁻⁴.

Las columnas no son intercambiables: tienen tamaños relativos estables y un orden reproducible. Eso es compatible con **unidades fijas** (pachacas, ayllus, depósitos, categorías), no con un simple volcado de valores. El perfil no es monótono (13,2; 13,6; 9,5; 10,9; 11,6; 12,9; 11,2; 8,3; 8,8 %), así que la correlación no es un artefacto de ordenar las columnas por tamaño.

**Límite de las pruebas:** demuestran estructura (partes equilibradas + identidad de columna), **no** qué representa cada columna. No distinguen pachaca de periodo, producto o depósito.

### 4.3 La cuota 47 no es un 2 %: es una cuota absoluta

En UR278, 47 dividido por el total de cada registro:

- Rango: **1,10 %–4,18 %**; media 2,36 %; CV **0,33**.
- Solo **3 de 28** registros caen dentro de ±10 % de un 2 % exacto.
- Totales de registro: 1125–4273 (mediana 2015).

En los grupos KFG de otros quipus (no son los valores de Urton & Chu): UR275, 47/grupo = 0,55–1,85 % (media 1,15 %); UR268, 208/grupo = 0,69–2,80 % (media 1,28 %); UR266, 47/grupo = 0,65–4,70 % (media 1,81 %).

**Lectura:** 47 es una **cuota fija absoluta** por registro; su proporción varía casi 4 veces. La frase «47 ≈ 2 % del depósito» describe un promedio, no una tasa. Si 47 fuera un impuesto proporcional, debería escalar con el total; no lo hace. Esto **refuta** la lectura de 47 como «tasa del 2 %» y **apoya** la lectura de «cuota fija por registro/periodo», del mismo modo que la tasa colonial es una cuota fija por tributario, no un porcentaje de la cosecha.

### 4.4 El 9 en las fuentes (exploratorio)

Conteos de unidades documentadas: Lunahuaná 4 guarangas, 8 curacas, 16 barrios; Collique 10 pachacas; Guancayos 9 pachacas; Chincha 30 pachacas. Si esos seis conteos fueran uniformes entre 2 y 30, P(≥1 nueve) ≈ **0,19**. Con seis conteos, un solo 9 **no es estadísticamente especial**. El 9 de Guancayos es un ancla textual valiosa, pero no una prueba de que el 9 de UR278 sea social.

### 4.5 Escalas: dónde cae una cifra de tasa frente a un quipu

- Celdas de UR278 (cuerdas nivel 0 con valor > 0): mediana **227**, rango 11–1 918. Totales de registro: 1 125–4 273, mediana 2 015.
- Cabeceras de UR266 (nivel 0): mediana **638**, p75 1 761, máximo 4 273; en efecto, «tres cifras por cuerda».
- Cantidades físicas de la tasa de Lunahuaná: 366 piezas de ropa, 500 fanegas, 758 aves; valores monetarios 2 196 y 3 660 pesos. Caen en el orden de un **registro** de UR278 o de una cabecera de UR266, no en el de una celda pequeña.
- La cuota 47 es ~1,6 órdenes de magnitud menor que un registro (47 / 2 015 ≈ 0,023). Si 47 es un impuesto, grava un **agregado** (registro/periodo), no una celda individual.
- La cuota 208 de UR268 es del orden de una celda grande de UR278 (1918) o de una cabecera mediana de UR266 (638–1 761); su escala es compatible con un **resumen de periodo**, no con una celda.

Esto no prueba nada por sí solo, pero acota las lecturas: 47 no puede ser «lo que produce una chacra» ni «lo que paga un individuo»; es una cuota de nivel agregado.

---

## 5. Evaluación de las hipótesis

### H1. Unidad = bulto

**Nivel: apoyado con datos (para depósitos costeños); propuesto (para Incahuasi).**

A favor:

- El **runcu** es la unidad de capacidad para coca y ají en inventarios de depósitos, con subdivisiones binarias (1/2, 1/4, 1/8) y un cesto de coca de ~20 libras (5154). Es exactamente el tipo de unidad que uno esperaría en un quipu de almacén.
- La fanega (~56 L, glosario de LeVine 1992) y el almud (1/12) son las unidades del maíz en las tasas (807, 839); el azumbre (2 L) se usa para líquidos (5192).
- Las vasijas de Cerro Azul (700–2000 L) y Ungará (300–500 galones) muestran almacenamiento por volumen (595, 606).
- Urton & Chu (2015) describen «grids» de cuadrados en el piso como posibles **unidades contables estandarizadas** para productos agrícolas; la ficha del paper lo marca como propuesta, no como lectura semántica.

En contra / límite:

- Ningún texto dice que un nudo o una cuerda equivalga a un bulto. La conexión es contextual.
- Los quipus de Incahuasi están asociados a maní, ají y frijol, pero la asociación es **física/contextual**; Urton & Chu usan «suggest», «may have served» (ficha 2015, línea 9). No es una decodificación.

### H2. 9 partes = pachacas

**Nivel: propuesto, con una dificultad documental.**

A favor:

- El único 9 exacto del libro: los **guancayos del Chillón** tenían **9 pachacas**, 900 hatun runa, 5 jefes (uno con 1 pachaca y cuatro con 2), y pagaban **5 cestos de coca por pachaca = 45 cestos** (369–371, 2601). Es un esquema 9 × 5 = 45, justo el tipo de estructura «9 partes + cuota fija» que buscamos. **Ojo:** el texto tiene una contradicción: primero dice «novecientos hatun runa, repartidos en cinco pachaca» y luego «las nueve pachaca estaban repartidas entre cinco jefes» (369). La aritmética 1 + 4×2 = 9 y el total de 45 cestos (5 × 9) apoyan el **nueve**; el «cinco pachaca» parece un error de transmisión o de redacción.
- Las 9 columnas de UR278 tienen identidad estable y tamaños relativos fijos (T2), como unidades administrativas recurrentes.
- Las columnas no son iguales (1,63×), lo que permite pachacas de tamaños distintos, como los 5 jefes guancayos con 1 o 2 pachacas.

Dificultad:

- **Guancayos está en el Chillón, no en Cañete.** Lunahuaná tiene 4 guarangas y 8 curacas, no 9; sus ~16 barrios tampoco dan 9. Si las columnas son pachacas, serían un nivel intermedio **no documentado** de 9 pachacas dentro de las 4 guarangas (plausible: 4 × 2–3 = 8–12), pero Rostworowski no lo dice.
- El 9 de Guancayos es un solo caso entre seis conteos; no es estadísticamente especial (§4.4).

### H3. 9 partes = periodos

**Nivel: no apoyado por la estructura del quipu; el calendario de 9 meses es real pero no mapea a las columnas.**

A favor:

- El año de **9 meses × 40 días = 360 + 5** está documentado en un testigo indígena y desarrollado por Rostworowski (914–916). Es una pieza fuerte de la cosmología costeña.
- El sufijo **ssop/nassop** se usa para contar días, monedas y fruta (916, 2292): hay un modo decimal específico para el tiempo.

En contra:

- En el archivo de Incahuasi, el eje temporal son las **filas**: UR278 son 33 registros sucesivos; UR269 se organiza en **bloques de 5** periodos con cuotas 47, 46, 46, 44, 25 (trabajo previo del equipo, `13_sistema_incahuasi`). El 9 está en las **columnas**, no en las filas.
- Si las columnas fueran meses, esperaríamos 9 columnas de tamaño similar y una sucesión temporal; las columnas tienen identidades fijas y tamaños desiguales, y las filas son las que avanzan.
- El calendario de 9 meses es uno entre varios (Cieza dice 10 meses; las Pléyades regulan el año) (915–921). No hay razón para imponerlo a la matriz.

**Síntesis:** la lectura más coherente es **filas = periodos/registros sucesivos; columnas = 9 unidades estables**. El 9 es espacial/administrativo, no temporal. Esto reconcilia H2 y H3 sin confundirlas.

### H4. 4 guarangas × 2 = 8 + 1

**Nivel: especulativo / no apoyado.**

- Las 4 guarangas y los 8 curacas (2 por guaranga) están documentados (706, 762). El 8 + 1 no.
- El curaca principal está dentro de los 8, no es un noveno (706, 762).
- En las 9 columnas no hay una columna «central» claramente dominante: la mayor es c2 (13,6 %), no c1; c1 es 13,2 %; c9 es 8,8 %. Un esquema 8 + 1 predeciría una columna especial; no se ve.
- Podría ser 8 mitades + 1 unidad central (Incahuasi o el curaca principal), pero es una conjetura sin ancla documental.

### H5. Cuotas = impuesto

**Nivel: apoyado con datos en cuanto a «cuota fija»; refutado en cuanto a «porcentaje».**

A favor:

- Las cuotas 10, 15, 17, 47, 208 son valores fijos, repetidos y no proporcionales al total del registro (§4.3). Eso es la firma de un **tributo por unidad/periodo**, no de un reparto proporcional.
- La tasa colonial es exactamente eso: una plantilla fija por tributario (0,5 ropa, ~1 ave, 3 pesos, total 5 pesos), que se mantiene aunque la población caiga 36 % (§3.3).
- Urton & Chu (2018) leen los valores fijos como «something like a tax, or levy» (recogido en la síntesis del equipo).

En contra / matices:

- 47 = 30 + 17 y 25 = 15 + 10: la cuota también codifica **niveles de agregación** (componente → flujo → periodo). No es solo un impuesto; es un marcador de nivel.
- 208 = 47 + 46 + 46 + 44 + 25 es una coincidencia sugerente (P ≈ 0,03), no una prueba.
- No hay un análogo documental exacto de 17; 47 se parece a 45 (coca guancaya) y a 50 (ropa por 100 tributarios), pero con 5 cuotas y muchos números documentales esos parecidos son baratos. **No los usemos como prueba.**

### H6. ¿Una cuota de 47 o 17 por unidad tiene análogo?

- **47:** dos coincidencias de orden de magnitud: 45 cestos de coca para 9 pachacas guancayas (9 × 5) y 50 piezas de ropa por 100 tributarios en Lunahuaná (0,5 × 100). Ambas dentro del 6 %. Pero la primera es de otro valle y la segunda es una tasa colonial por cabeza, no un impuesto incaico. **Coincidencia, no analogía demostrada.**
- **17:** no hay análogo. Si fuera ropa, equivaldría a 34 tributarios; si coca, a 3,4 pachacas de 5 cestos. Ninguna de las dos cosas está documentada.
- **10:** sí aparece como cantidad en la lista guancaya (10 ollas, 10 rodelas), pero es una lista de bienes, no una cuota por unidad.
- **208:** no hay análogo; 208 ≈ 0,44 × 469 tributarios (ropa de 1590), pero es numerología.

---

## 6. Resultados negativos

1. **Maní, ají y frijol no están en Rostworowski para Cañete/Incahuasi.** El maní aparece una sola vez en el libro, como ingrediente de la chicha (3059); el ají y el frijol solo en la lista de tributos de los guancayos del Chillón (340). La asociación de los quipus con maní/ají/frijol es arqueológica y contextual (Urton & Chu 2015), no textual.
2. **Guarco no tiene datos de guarangas, pachacas ni ayllus.** Rostworowski lo dice: se ignoran las tierras de curacas y ayllus (617). No se puede probar la hipótesis de 9 unidades en Guarco.
3. **Lunahuaná no tiene 9.** Tiene 4 guarangas, 8 curacas y ~16 barrios (706, 762, 716–723). El «8 + 1» no está documentado.
4. **Las 9 columnas no son «casi iguales» en sentido estricto.** CV 0,278; la mayor es 1,63× la menor. Son equilibradas frente a un reparto aleatorio, no iguales.
5. **47 no es un 2 % estable.** 1,10–4,18 %; solo 3/28 registros dentro de ±10 % de 2 %. La lectura de «tasa del 2 %» no se sostiene.
6. **El 9 no es la periodicidad del archivo.** Las filas son 33 registros sucesivos; UR269 usa bloques de 5. El año de 9 meses existe, pero no mapea a las columnas.
7. **La tasa de 1577 tiene aritmética inconsistente.** Especies 1474 vs componentes 1214; total 3660 vs 3670; Rostworowski escribe 3760. No usar los totales monetarios sin depurar.
8. **No hay mención de quipus en Incahuasi en Rostworowski.** El vínculo Incahuasi–quipus es arqueológico (Urton & Chu), no etnohistórico.
9. **El 9 de Guancayos no es estadísticamente especial** entre los conteos documentados (P ≈ 0,19 bajo un nulo uniforme exploratorio).

---

## 7. Nivel de evidencia

| Afirmación | Nivel |
|---|---|
| Guarco: 2 encomiendas, 3 fortalezas, coayllos/chinchas/mochicas, tierras de Pachacamac y del Sol | **Demostrado** (documental) |
| Lunahuaná: 4 guarangas, 8 curacas (2 por guaranga), 740→474 tributarios | **Demostrado** (documental) |
| Tasas 1577/1590: plantilla por tributario estable (ropa 0,5; aves ~1,03; plata ~3; total ~5) | **Demostrado** (aritmética de los documentos) |
| Guancayos: 9 pachacas (el texto también dice «cinco pachaca»), 900 runa, 5 jefes, 45 cestos = 9 × 5 | **Demostrado** el total de 45 y la estructura 1+4×2=9; el «cinco pachaca» es una contradicción textual |
| Incahuasi: fundación por Tupac Yupanqui, guarnición de guerra, colcas, abandono según Cieza | **Demostrado** (Cieza + Rostworowski) |
| Incahuasi: continuidad parcial como centro administrativo/tambo; mitas de diversos lugares | **Propuesto** (Rostworowski, sin archivo específico) |
| 9 columnas de UR278 equilibradas (CV 0,278 vs 0,865) e identidad estable (r 0,41 vs 0) | **Demostrado** (permutación, p_Holm < 1e-4) |
| 47 es cuota absoluta, no proporcional (1,10–4,18 %) | **Demostrado** (aritmética) |
| 9 columnas = 9 unidades/pachacas | **Propuesto** (analogía guancaya + estructura estable; falta lista de Cañete) |
| 9 columnas = 9 periodos | **No apoyado / especulativo** (el eje temporal son las filas; calendario de 9 meses no mapea) |
| 4 × 2 = 8 + 1 | **Especulativo** (sin dato) |
| Cuotas = impuesto fijo por unidad/periodo | **Apoyado con datos** (cuota absoluta + tasas por cabeza); «2 %» **refutado** |
| Unidad = bulto/runcu | **Apoyado** para depósitos costeños; **propuesto** para Incahuasi |
| 47 ≈ 45/50 y 208 ≈ 0,44 × 469 | **Especulativo / coincidencia** |

---

## 8. Para el coordinador

- **Rostworowski no menciona maní, ají ni frijol en Cañete/Incahuasi.** El maní aparece una sola vez en el libro, como ingrediente de la chicha (3059); ají y frijol solo en la lista de tributos de los guancayos del Chillón (340). El contexto de maní es Urton & Chu 2015: 34 quipus, asociación física/contextual, y los propios autores usan «suggest»/«may have served». No es lectura semántica.
- **Lunahuaná no da un 9.** Tiene 4 guarangas, 8 curacas (2 por guaranga, posible hanan/urin) y ~16 barrios; el curaca principal está dentro de los 8, así que «4 × 2 = 8 + 1» no está documentado (706, 762, 716–723).
- **El único 9 exacto es Guancayos (Chillón):** 9 pachacas, 900 hatun runa, 5 jefes (1 + 4×2) y **45 cestos de coca = 9 × 5** (369–371, 2601). El texto oscila («cinco pachaca» / «nueve pachaca»), pero 1+4×2=9 y 5×9=45 apoyan el nueve. Es el mejor ancla textual para «9 partes + cuota fija por parte», pero de otro valle y un solo caso entre seis conteos (P ≈ 0,19 bajo un nulo exploratorio).
- **Las tasas 1577/1590 son una plantilla por cabeza:** 0,5 pieza de ropa, ~1,03 aves, ~3 pesos de plata y ~5 pesos totales por tributario, casi idénticas pese a que los tributarios caen 35,9 % (740 → 474) y la población 41,5 % (3276 → 1915). El tributo colonial es una cuota fija por persona, no un porcentaje de la cosecha. **Ojo con la aritmética de 1577:** los componentes valorados suman 1214 pesos, el documento dice 1474, y el total 3660 no cuadra con 2196 + 1474 = 3670; Rostworowski escribe 3760. Usar cantidades físicas y ratios, no totales monetarios.
- **UR278: las 9 columnas están equilibradas pero no son iguales.** CV dentro de fila 0,278 frente a 0,865 del nulo (p_Holm < 1e-4); la mayor es 1,63 × la menor. Tienen identidad estable (r = 0,41 frente a 0 del nulo; p_Holm < 1e-4), así que no son intercambiables.
- **La cuota 47 es absoluta, no un 2 %:** 1,10–4,18 % del registro, solo 3/28 dentro de ±10 % de 2 %; es ~1/43 de un registro. Eso refuta «tasa proporcional» y apoya «cuota fija por registro/periodo», igual que la tasa colonial por cabeza.
- **El eje temporal del archivo son las filas, no las columnas:** UR278 son 33 registros sucesivos y UR269 se organiza en bloques de 5 periodos (cuotas 47, 46, 46, 44, 25). El año de 9 meses × 40 días está documentado (914–916), pero no mapea a las 9 columnas: «9 = periodos» no está apoyado; «9 = unidades/pachacas» es la lectura plausible.
- **Unidad = bulto:** apoyado para depósitos costeños por el **runcu** (medida de coca/ají en inventarios, con 1/2, 1/4, 1/8 y cesto de ~20 libras), la fanega/almud y las vasijas de 700–2000 L; propuesto, no demostrado, para Incahuasi.
- **Incahuasi:** fundado por Tupac Yupanqui durante la guerra contra Guarco, construido rápido con piedra basta, con guarnición y colcas de campaña; Cieza dice que se abandonó al terminar la guerra, y Rostworowski propone continuidad parcial como centro administrativo/tambo y mitas de diversos lugares. Ningún curaca vivió allí. La arqueología (Hyslop/Snead) insiste en la ocupación breve y los ~202 almacenes de ~250 unidades.
- **Recomendación inmediata:** buscar en AGI Justicia 432/482 y Escribanía de Cámara 498-B una lista de 9 pachacas/ayllus de Lunahuaná (o de Cañete) que permita probar la firma de 9 columnas; mientras no exista, tratar «9 = pachacas» como propuesto y no usar 47 como «2 %».

---

### Archivos de este equipo

- `tasas.csv` — 61 filas de cifras de tributo, población y productos, con línea de fuente.
- `parcialidades.csv` — 32 filas de unidades sociopolíticas (Guarco, Lunahuaná, Collique, Guancayos, Chincha).
- `01_extraer_tasas.py` — extracción y cálculo de ratios; salida `resultados_tasas.txt`.
- `02_control_9partes.py` — pruebas T1/T2, cuota 47, estabilidad de tasas, 9 en las fuentes; salida `resultados_control.txt`.
- Semilla fija: 20261018. 20 000 permutaciones. Holm sobre 2 pruebas.
