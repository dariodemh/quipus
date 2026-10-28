# Fichas de género del atlas

Cada ficha resume un género del atlas (`atlas.csv`, 651 quipus de KFG). Los géneros salen de reglas explícitas (`reglas.py`). Un quipu recibe el género de mayor confianza; si hay empate, gana el más específico, en este orden: CAL > NAZ > ARC > PAD > FOR > NON > TAL > SUM > ASG > TAB > SEG. Los demás géneros que también encienden se anotan en la columna `secundarios`.

Escala de confianza:

- **Alta:** el detector pasa Holm, o el quipu es un control positivo publicado y verificado. En los géneros con varias líneas de evidencia, además deben coincidir 3 o más.
- **Media:** el detector es significativo con BH, o hay 2 líneas de evidencia.
- **Baja:** solo hay un umbral descriptivo o una sola línea débil.

Si los datos son pobres (menos de 10 cuerdas anudadas, o más del 50 % rotas con menos de 30 anudadas), los géneros «suaves» bajan un nivel.

Referencias de línea: archivos de `analisis/fuentes_txt/`. U17 = Urton 2017; R = Rostworowski, *Costa peruana prehispánica*; MU18 = Medrano y Urton 2018; P04 = Pärssinen y Kiviharju 2004; NT = *Narrative Threads* 2002.

---

## CAL. Calendario (tipo UR006)

- **Tamaño:** n = 3: UR006 (alta), y UR009 y UR021 (media).
- **Procedencia:** Leymebamba, los tres. Los guarda el Centro Mallqui. Transcriptor: Urton.
- **Rasgos diagnósticos:**
  - 24 conjuntos pareados de [20–22 colgantes] + [8–10 de lazo], unos 30 por par.
  - Total cercano a 730 = 362 + 368.
  - La plantilla P8ar (n_plantillas) lo reconoce en UR006 (q = 0,002; p frente al corpus = 0,002).
  - UR009 y UR021 son copias de UR006 (04, 14_copias). P8ar no los reconoce por sí solos, así que entran por la relación de copia.
- **Analogía documental:**
  - Urton 2017, cap. 4, lee UR6 como calendario de dos años (U17 l. 711–717 y 750).
  - Hipótesis rival documentada: el año de 9 meses × 40 días que declara un testigo de Changuco (R l. 914–916).
- **Predicción comprobable (UR006):** en el objeto, contando los colgantes por conjunto, los pares suman unos 30 y el total unos 730. Ninguna otra unidad debería agrupar mejor, por ejemplo 9 × 40. UR009 y UR021 deben reproducir la secuencia de pares en orden, con errores de copia del orden de una cuerda.

## NAZ. Ficha con encabezado y par marcador (Nazca/Berlín)

- **Tamaño:** n = 6. Alta: UR1140, UR1131 y UR234. Media: UR1136, UR223 y HP056.
- **Procedencia:**
  - 5 están en Berlín (Museum für Völkerkunde y Ethnologisches Museum) y 1 en Lima (HP056).
  - Sitios: Nazca 2, Ica 1, Pachacamac 1, desconocida 2.
  - Transcriptores: Ascher 3, Urton 2, Pereyra 1.
- **Rasgos diagnósticos:**
  - La unidad es un registro de 9 cuerdas: 7 campos + 2 marcadoras. Hay variantes de 8 (UR234) y de 10 (UR1131).
  - El campo 1 es el máximo en 44 de 45 registros.
  - El par marcador está a 2 campos de un extremo en 55 de 71 grupos (p ≈ 1e-54). Su lado indica el sentido de lectura.
  - Las marcadoras tienen color propio: difieren de sus vecinas en el 76 % de los casos (24_color_formato).
  - No hay sumas entre campos.
  - UR1176 fue candidato del barrido, pero no pasa. Queda en FOR, con NAZ como secundario de confianza baja.
- **Analogía documental (propuesta):** la «Memoria» de Guacrapaucar (1558) organiza series de categorías, y cada serie va abierta por un encabezado estereotipado: «Cuando el marqués fue a Bombón» (P04 l. 318). La ficha de Nazca tiene la misma arquitectura: encabezado de 2 campos + separador + cuerpo. No hay documento de Nazca que la confirme.
- **Predicción comprobable (UR1140):**
  - En una foto, las 2 cuerdas marcadoras de cada registro de 9 se distinguen por su color de las 7 de campo.
  - Si aparece otro quipu de Berlín con número de museo consecutivo (como VA16635/6 para UR1136/UR1140), su campo 1 será el máximo en al menos el 90 % de sus registros.

## ARC. Archivo jerárquico con relaciones entre quipus (Incahuasi, Puruchuco)

- **Tamaño:** n = 21.
  - Alta (18): 13 de Incahuasi, sector A (UR255, 256, 266, 267A, 267B, 269, 270, 273A, 273B, 274A, 274B, 275, 278) y 5 de Puruchuco (UR063, 064, 066, 067, 068).
  - Media (3): UR268, UR073 y UR078 (relación propuesta).
- **Procedencia:**
  - Incahuasi 14: Proyecto Incahuasi, valle de Cañete.
  - Puruchuco/Huaquerones 7: Museo de Puruchuco.
  - Transcriptor: Urton en los 21.
- **Rasgos diagnósticos:**
  - Totales de un quipu que reaparecen en orden en otro: UR278 → UR266, 11 exactos; UR068 → UR067, 16 de 20 columnas.
  - Tríos [x, c, x − c] con cuota fija (47, 25, 15, 10), solo en 8 quipus del sector A.
  - Parejas atadas cuyas partes se suman.
  - Copias del mismo nivel.
  - El color cambia con la función de la cuerda (un número que pasa a cabecera pasa a W en el 75 % de los casos).
  - Sumas internas robustas a dos nulos en 9 de los 13 de Incahuasi.
- **Analogía documental:**
  - Urton y Chu 2015 / 2018 (`UrtonChu_ArchivoKhipuIncawasi_es.txt`): contabilidad de un almacén estatal de productos agrícolas.
  - Urton y Brezine 2005 (U17 cap. 5): jerarquía contable de Puruchuco.
  - La visita de Huánuco de 1562 describe quipucamayos de pueblo cuyos datos «pasaban a quipus centrales» (NT l. 1388, Pärssinen).
  - LeVine 1992 trata el almacenaje inca.
- **Predicción comprobable (UR278 / Incahuasi):** en los 5 quipus de Inkawasi que Urton no estudió habrá parejas cuyas cuotas sumen 46 o 44, y cuyas sumas den las filas 2–4 de UR269 (13_sistema_incahuasi). Para Puruchuco: una nueva lectura del objeto debe conservar las discrepancias 2904/2908 y 161/162 que ya predijeron Urton y Brezine.

## PAD. Padrón por persona (tipo Santa 1670)

- **Tamaño:** n = 9. Alta: UR087–UR092 (6). Baja: HP033, UR028 y UR1114.
- **Procedencia:**
  - Santa 6: Museo Temple Radicati.
  - Los 3 de confianza baja vienen de Ica, Atarco y Ullujaya: ningún padrón asociado.
- **Rasgos diagnósticos:**
  - Plantilla P4r: grupos de igual tamaño k (4–12), monocromos, cada uno de color distinto al anterior, con valores pequeños.
  - En los quipus del Santa: q ≈ 0,002 y p frente al corpus entre 0,02 y 0,12.
  - Torsión Z dominante. La unión R/V separa quipus (5 puros y UR090 mixto).
  - En UR087 el color de la primera cuerda forma una seriación de período 4. En el 44 % de los grupos, el color marca la posición y no la identidad.
- **Analogía documental:**
  - Revisita del Santa (Recuay/Corongo) de 1670: 130 tributarios con nombre y tributo idéntico (MU18 l. 38).
  - «one group of six cords of one color is followed by another six cords of a different color» (MU18 l. 48).
  - U17, cap. 12.
- **Advertencia:** la correspondencia entre el orden de los nombres y el orden de los grupos NO se sostiene (n_santa_padron: p = 0,18; la asignación de pachacas es circular). La confianza alta corresponde al **formato** y a la procedencia documental, no a una lectura nombre por nombre.
- **Predicción comprobable:**
  - Los 6 quipus suman 133 grupos, frente a 130–132 tributarios.
  - Con el folio original de la revisita, cada grupo debe tener la misma cuota.
  - Los «hijo de» de Namus deben caer al final, como en los 6 grupos finales de UR091 con posición 1 = 0.

## FOR. Formulario con clave de reparto

- **Tamaño:** n = 101.
  - Alta (9): UR053A–E, UR131A–C y UR149.
  - Media: 61. Baja: 31.
- **Procedencia:**
  - Desconocida 34, Pachacamac 18, Ica 9, Incahuasi (sector B, JC) 5, Huacho 4.
  - Berlín guarda 37.
  - Transcriptores variados: Ascher 40, Urton 39, otros 22.
- **Rasgos diagnósticos (22_formularios):** un registro se repite en bloques y conserva las proporciones entre sus partes.
  - Clave cromática: el reparto por color de cuerda.
  - Clave posicional: el reparto por posición en el bloque.
  - En UR053A–E: W > R en 99 de 111 tríos, y W:R entre 0,66 y 0,80 en 5 quipus cuya escala varía 70 veces.
  - Es la señal más frecuente del corpus: 162 detecciones (150 de los 410 quipus con ≥ 30 cuerdas). Por la jerarquía, 64 quedan asignados a otro género: TAB 20, ARC 17, SUM 9, ASG 6, NAZ 5 y otros. A la inversa, 3 quipus entran en FOR solo por la clave de archivo bien apoyada.
  - El reparto concreto es local: no hay clave compartida entre archivos, tampoco con el transcriptor fijo.
- **Analogía documental:**
  - Los guancayos del Chillón: 9 pachacas de 100 bajo 5 señores (1 + 4 × 2), con el tributo repartido por pachaca (R l. 369–371).
  - La tasa toledana de Lunahuaná (1577) da cantidades fijas por especie: pesos, ropa, maíz y aves (R l. 762).
- **Predicción comprobable (UR053A):** cualquier registro nuevo del juego, o de un archivo del mismo número de museo, repartirá W / R / AB en torno a 0,65 / 0,19 / 0,16 (±0,05), sea cual sea su total. W nunca será igual a R + AB, porque es un reparto y no una suma. Lo comprobable es la **partición** de colores, no sus etiquetas, que dependen del transcriptor.

## NON. No numérico (sin nudos o nudos no axiales)

- **Tamaño:** n = 17. Media: 5 (MM020, UR179, UR180, UR241, UR058A). Baja: 12.
- **Procedencia:** desconocida 6, Pachacamac 3, Huaquerones 3, Cajamarquilla 2 (+ UR180), Arica 1.
- **Rasgos diagnósticos:**
  - Clase NC: cuerdas sin nudos con color rico.
  - Clase NU: nudos «no axiales», que OKR registra como nudos sin tipo (n_no_numericos).
  - Confianza baja: menos del 20 % de cuerdas anudadas aunque estén intactas.
  - No muestran léxico de color ni código binario de dirección (negativos de n_no_numericos).
- **Analogía documental/etnográfica:**
  - Hyland 2017: los quipus-epístola de Collata, con 95 signos de color × fibra × torsión, frente a 12 en un quipu contable.
  - Salomon 2004: los quipus patrimoniales de Tupicocha, donde la información está en la factura y no en el número.
- **Predicción comprobable (UR179/UR180, Cajamarquilla, AMNH):** en una foto, los nudos «no axiales» serán hilos atados o enrollados, no nudos de cuerda. Los 3 quipus de Cajamarquilla compartirán esa morfología. Si las fotos muestran nudos decimales comunes, el género cae.

## TAL. Registro aditivo/tally (torsión Z)

- **Tamaño:** n = 28. Alta: 12 (KH0001, UR039, UR050–055, UR110, UR144, UR193, JC012, UR284). Media: 7. Baja: 9.
- **Procedencia:** desconocida 13, Pachacamac 3, Incahuasi 2 (JC), Chuquitanta, Huari, Pisco, cerca de Lima. El género circula: no es propio de un sitio.
- **Rasgos diagnósticos:**
  - 50 % o más de las cuerdas violan la gramática decimal: lugar repetido o cifra mayor que 9.
  - Torsión mayoritariamente Z (OR 38 frente a los decimales).
  - Fibra de camélido (OR independiente).
  - Nudos de 10 o más vueltas en 14 quipus.
  - No hay sumas, ni con lecturas alternativas.
  - El silabario de ALBA/Sivan sobre estos mismos quipus no supera al azar (23_sivan_ur193).
- **Analogía etnográfica:**
  - Mackey 1970: quipus de pastores con cuentas separadas por categoría en una misma cuerda (subtipo B1-b; resumen en NT cap. 13, l. 3616–4130).
  - Uhle 1897: quipus de rebaño en la puna, «descendientes directos» de los contables (NT l. 1506).
- **Predicción comprobable (UR050):**
  - En el objeto, más del 90 % de las cuerdas tendrán torsión Z y fibra de camélido.
  - Las cuerdas tendrán 3 racimos de nudos largos de un dígito (tabla de 163 × 3).
  - Ninguna cuerda será suma de otras.
  - Si se analiza la fibra de UR039 y UR193 (algodón con 100 % de torsión Z), seguirán siendo la excepción costera del género.

## SUM. Contabilidad decimal con totales internos

- **Tamaño:** n = 14.
  - Alta (8): AS006, AS044, AS066, AS199, UR118, UR119, UR166 y UR1096.
  - Media (6): AS001, AS007, QU009, QU015, QU016 y UR1152.
  - Los 9 quipus de Incahuasi con sumas van a ARC.
- **Procedencia:** desconocida 9, Paracas 2 (UR118/UR119), Pachacamac, Ica y Huando.
- **Rasgos diagnósticos:**
  - Sumas de colgantes adyacentes ≥ 100 en exceso, robustas a los nulos M1 y M2 (08_auditoria_sumas).
  - Formato «fila + cuerda-total suelta» (14_copias: 51 aciertos frente a 14,9).
  - Cuerdas superiores que suman su grupo (01).
  - Es el ≈ 3 % del corpus: la contabilidad verificable es rara.
- **Analogía documental:** la encomienda de Aldana (Cuzco, 1540; Medrano 2019, l. 294) da 11 pueblos que suman exactamente 260, con el total declarado ANTES de la lista. La lectura oral de Medrano dice que los totales se calculaban con yupana al leer, lo que explica que sean escasos en los quipus.
- **Predicción comprobable (UR118/UR119, Paracas):** son registros paralelos del mismo formato. En el objeto, la cuerda-total suelta irá separada de su fila por un espacio mayor que el que hay entre filas. Un documento equivalente declarará totales que salen exactos al sumar sus partidas.

## ASG. Lista de asignación (cifras redondas, cuotas repetidas)

- **Tamaño:** n = 28.
  - Alta (4): AS172, UR197, UR219 y UR271, que tienen las dos firmas.
  - Media: 24.
- **Procedencia:** Pachacamac 10, desconocida 6, Armatambo 2, Arica 2, Ica 2, Pisco 2. Berlín guarda 14.
- **Rasgos diagnósticos (11_rosetta):**
  - El 80 % o más de las cifras intactas ≥ 10 son múltiplos de 10 (en un recuento se espera un 10 %).
  - Valores iguales adyacentes en exceso (cuotas repetidas).
  - No hay filas co-crecientes.
  - Dentro de las tablas, las de recuento co-crecen y las redondas no (p = 0,01).
- **Analogía documental:**
  - Tasa de Lunahuaná de 1577 y retasa de 1590: cantidades redondas por especie, como 500 fanegas de maíz (R l. 762, 806–809).
  - Medrano 2019 cita cuotas repetidas: «150, 150 / 200, 200» y «100 cada 15 días».
- **Predicción comprobable (UR271):** la cifra modal 220 aparece 15 veces. En un documento de tasa o mita del mismo valle, las cuotas por pueblo serán iguales o múltiplos de una unidad común. En el objeto no habrá nudos de unidades (largos) en las cuerdas intactas.

## TAB. Tabla de recuento (unidades × categorías)

- **Tamaño:** n = 55. Media: 34. Baja: 21. Ninguno es de confianza alta: es un formato frecuente y genérico.
- **Procedencia:** desconocida 30, Pachacamac 7, Huaquerones 3 y otros.
- **Rasgos diagnósticos (10_tablas):**
  - Filas × columnas regulares, con una mediana de 8 × 6.
  - La 1.ª columna es la mayor y a menudo blanca: es la categoría principal, no un total.
  - Las filas tienen «tamaño»: una fila grande lo es en todas las columnas (ρ ≥ 0,3).
  - Las cifras no son redondas (recuento).
  - No hay columna-total, que solo aparece en Incahuasi.
- **Analogía documental:**
  - El padrón de unidades domésticas de Urton (U17 l. 2485): valores de 1 a 7.
  - Las visitas por pueblo y rubro, como la de Huánuco de 1562.
  - Las 9 pachacas de Bambamarca (Pärssinen 1992, tabla 2), con tributarios por pachaca 104, 75, 78…
- **Predicción comprobable (AS069, 114 × 7):** la 1.ª columna será la mayor en la mayoría de las filas. Los totales de fila NO estarán en el quipu. Si aparece un documento, sus filas serán unidades (pueblos, ayllus o casas) y sus columnas, rubros en orden fijo.

## SEG. Lista segmentada (solo formato)

- **Tamaño:** n = 76, todos de confianza baja.
- **Procedencia:** desconocida 22, Pachacamac 11, Ica 8, Leymebamba 8, Incahuasi 6. Berlín guarda 21.
- **Rasgos diagnósticos:** al menos uno de estos tres:
  - el color marca el grupo (NMI color ~ grupo sobre el nulo, 24_color_formato);
  - 2 o más marcadoras OKR;
  - bloques que repiten la secuencia de categorías (P11a, sin Holm).

  Es formato sin aritmética detectada: sabemos cómo está segmentado, no qué cuenta.
- **Analogía documental:**
  - El registro wanka (Murra 2024): 12 categorías en orden constante × 19 eventos (ds/n_murra_wanka).
  - La Memoria de Guacrapaucar: series de categorías abiertas por un evento (P04 l. 318).
- **Predicción comprobable:** en una foto, los cambios de color y las marcadoras caerán en las fronteras de grupo de KFG, con al menos 6 de 6 bloques coincidentes, como en la auditoría de fotos (25). Un detector de bloques repetidos debería encender si se retranscribe.

## SIN. Sin género

- **Tamaño:** n = 293 (45 %).
  - 113 por datos insuficientes: menos de 10 cuerdas anudadas, o la mayoría rotas.
  - 180 son decimales sin estructura detectada.
- **Procedencia:** desconocida 110, Pachacamac 36, Ica 24, Incahuasi 23 (los 23 JC del sector B, sin relaciones, más UR257 y otros), Gaffron 10.
- **Lectura:**
  - Los 180 «decimales sin estructura» son el territorio que el proyecto aún no entiende. Probablemente son listas de recuento demasiado cortas para que los detectores tengan potencia: la potencia del recuento KFG es de ~24 % aun con sumas en todos los grupos.
  - **Predicción nula comprobable:** una retranscripción independiente no hará encender ningún detector congelado.
