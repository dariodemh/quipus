# -*- coding: utf-8 -*-
"""Genera afirmaciones.csv: extracción de afirmaciones comprobables de 12 fichas.
Solo escribe dentro de analisis/ds/lit_1/."""
import csv, os

COLS = ["fuente", "afirmacion", "quipus_implicados", "cifras",
        "como_comprobarla", "comprobable_con_datos_del_repo"]

R = []
def add(f, a, q, c, m, comp):
    R.append(dict(zip(COLS, [f, a, q, c, m, comp])))

# ---------------- 1912 Locke ----------------
L12 = "Locke 1912, The Ancient Quipu"
add(L12, "Los nudos se usan puramente como registros numéricos; no hay indicio de otro uso en los especímenes conservados.",
    "B8713 (AMNH, Huando) + especímenes AMNH", "1 espécimen central; 10 variantes de nudo",
    "Verificar que todo quipu del corpus tenga valores decimales reconstruibles y que ninguna cuerda escape al sistema posicional (clusters <=9, largos en unidades).",
    "parcial")
add(L12, "La cuerda superior que enlaza un grupo suma los valores de las cuerdas pendientes de ese grupo (top cord = sumatoria).",
    "B8713; grupos con top cord en general", "1 grupo verificado en el artículo (suma exacta)",
    "Para cada cuerda con union=T y nivel 0, comparar su valor con la suma de las cuerdas nivel 0 del grupo inmediatamente a la izquierda; comparar con cuerdas no-T; permutación dentro de quipu.",
    "si")
add(L12, "Las distancias desde el cordón principal ubican las órdenes decimales: grupos de nudos simples de 1-9, nudo largo para unidades.",
    "Todos", "<=9 nudos simples por racimo; 8 tipos de nudo largo",
    "Contar nudos por racimo en la cadena `nudos`: ¿algún racimo simple >9? ¿algún largo con valor >=10?",
    "si")
add(L12, "El color de la cuerda no tiene significado especial: se elige según el gusto del fabricante.",
    "B8713", "1 espécimen",
    "Test de asociación color-valor (por quipu y agregado) y de recurrencia de secuencias de color; nulo por permutación de colores dentro de quipu.",
    "parcial")
add(L12, "B8713 podría ser un registro de seis periodos o años de cuatro clases de objetos.",
    "B8713", "6 periodos x 4 clases",
    "Identificar B8713 en KFG (no hay números B en los metadatos) y comprobar 6 grupos x 4 cuerdas.",
    "no")
add(L12, "Solo existen diez variaciones de nudo: dos formas de nudo simple y ocho nudos largos que difieren en el número de vueltas.",
    "Especímenes AMNH", "10 variantes",
    "Tabular tipos de nudo (S, L, E, EE, SP, TF...) y rango de vueltas en el corpus.",
    "parcial")
add(L12, "La tesis fuerte (quipus = registros numéricos, no narrativos) se apoya en inspección de especímenes, no en estadística.",
    "Corpus AMNH", "sin N ni controles",
    "No falsable directamente; sirve de hipótesis nula frente a hipótesis narrativas (Urton 1998/2003).",
    "no")

# ---------------- 1927 Locke ----------------
L27 = "Locke 1927, A Peruvian Quipu"
add(L27, "El espécimen tiene 15 grupos de 6 cuerdas pendientes, cada grupo con una cuerda superior sumatoria, y 3 cuerdas sueltas P, Q, R al final.",
    "Espécimen del Museum of the American Indian (Heye)", "15 grupos x 6 = 90 pendientes + 3 sueltas",
    "Buscar en KFG un quipu con 15 grupos de exactamente 6 pendientes nivel 0 y 3 cuerdas finales no agrupadas.",
    "parcial")
add(L27, "La suma de las cuerdas superiores de los grupos es 839, con 71 en las cuerdas subsidiarias.",
    "Espécimen Heye", "839 y 71",
    "Buscar quipu cuya suma de valores de cuerdas union=T (nivel 0) sea 839 y cuyas subsidiarias de esas T sumen 71.",
    "parcial")
add(L27, "Hay una discrepancia en el grupo J: la cuerda superior suma 43 y las pendientes 45.",
    "Espécimen Heye", "43 vs 45",
    "Localizar el quipu y comparar suma de pendientes vs top cord; no hay id en KFG.",
    "no")
add(L27, "Las tres cuerdas finales P, Q, R parecen una hoja de balance o suma final; sus totales son al menos 2795.",
    "Espécimen Heye", ">=2795",
    "Comprobar si P+Q+R = suma de los totales de grupo; requiere identificar el quipu.",
    "no")
add(L27, "El quipu se usó primariamente para registrar números, probablemente como memoria technica, no para cálculo ni como escritura.",
    "Todos", "sin N",
    "No falsable con el corpus; contrastable sólo indirectamente (¿hay operaciones aritméticas o sólo registros?).",
    "no")

# ---------------- 1928 Locke ----------------
L28 = "Locke 1928, Supplementary Notes"
add(L28, "Los ~16 quipus del AMNH examinados son todos de carácter numérico y no ejemplifican un sistema de escritura.",
    "B-8707, B-8705, B-8704, B-8703, B-8716, B-8711 (9A-9I), B-8709, B-8714, 40.1-1550, 40.1-1551, D-N65-11, B-8717, B-8710, B-8712, B-8708",
    "~16 quipus",
    "No hay números B-87xx en quipus.csv; sólo se puede comprobar el correlato numérico-decimal en los AS equivalents.",
    "parcial")
add(L28, "Varias cuerdas sumatorias existen y suman los valores de las pendientes (p. ej. 9A 'Brown, sums the pendent strand knots'; B-8712).",
    "9A (B-8711), B-8712", "2 casos citados",
    "Mismo test de top cord (union=T) que Locke 1912.",
    "si")
add(L28, "Se usan tres tipos de nudo: flamenco (F), simple (S) y largo (L), y se registran cuerdas subsidiarias con asterisco.",
    "Colección AMNH", "F/S/L",
    "Ver distribución de tipos de nudo (S, L, E, SP, TF, BL, LL) y de niveles jerárquicos en cuerdas.csv.",
    "si")
add(L28, "El color se registra por cuerda pero no se le atribuye significado especial.",
    "Colección AMNH", "columna de color por cuerda",
    "Test color-valor y color-grupo; nulo por permutación.",
    "parcial")

# ---------------- 1981 Ascher & Ascher ----------------
A81 = "Ascher & Ascher 1981, Code of the Quipu"
add(A81, "El quipu usa notación posicional decimal en base 10 (unidades, decenas, centenas, millares).",
    "Todos", "base 10",
    "Verificar que los valores decodificados sean combinaciones de 1-9 en cada orden y que ningún racimo simple exceda 9.",
    "si")
add(A81, "Existen 'sumas categóricas': el valor de una cuerda madre es la suma de los valores de sus cuerdas subsidiarias (desagregación por categorías).",
    "Todos los quipus con subsidiarias", "sin cifra en la ficha",
    "Para cada madre con >=1 subsidiaria, comparar valor de la madre con la suma de sus hijas; nulo por permutación de valores de hijas dentro del quipu.",
    "si")
add(A81, "Las 'top cords' y la estructura de árbol ('data tree') son componentes del código, no adornos.",
    "Todos", "top cords, data tree",
    "Test de top cord + análisis de jerarquía (niveles 0-5) y de grupos.",
    "si")
add(A81, "Las relaciones de Ascher quedaron especificadas a nivel de especímenes individuales, no de corpus (según Medrano y Khosla 2024).",
    "Corpus Ascher", "sin N",
    "Es una afirmación meta sobre la literatura; no se comprueba con cuerdas.csv.",
    "no")

# ---------------- 1998 Urton ----------------
U98 = "Urton 1998, From Knots to Narratives"
add(U98, "Los significantes del quipu contenían un alto nivel de información sintáctica y semántica, no sólo números.",
    "Quipus incas + transcripciones coloniales", "sin N",
    "Requiere corpus de transcripciones lectura-quipu (no incluido en el repo); con cuerdas.csv no es falsable.",
    "no")
add(U98, "El sistema de registro del quipu pudo aproximarse más a una forma de escritura de lo que se suponía.",
    "Quipus incas", "sin N",
    "Necesita correspondencias documento-quipu; no hay tabla en el repo.",
    "no")

# ---------------- 2001 Urton ----------------
U01 = "Urton 2001, Calendrical and Demographic Tomb Text"
add(U01, "UR6 es un calendario bienal combinado con un censo de contribuyentes chachapoyas.",
    "UR6 (KH0242, Laguna de los Cóndores)", "calendario de 2 años + censo",
    "Comprobar en UR006 la estructura de 24 conjuntos de 29-31 cuerdas (730 pendientes) y la periodicidad de valores.",
    "parcial")
add(U01, "UR6 tiene 762 cuerdas pendientes, 730 organizadas en 24 conjuntos de 29-31 (= 2 años de 365 días).",
    "UR6", "762 pendientes; 730 en 24 conjuntos",
    "Contar pendientes nivel 0 y tamaños de grupo en UR006.",
    "si")
add(U01, "UR6 fue la fuente del primer censo colonial de la región, levantado por administradores españoles en 1535.",
    "UR6", "1535",
    "Requiere el documento colonial; no hay control documental en el repo.",
    "no")
add(U01, "Los 32 quipus de la Laguna de los Cóndores (1996) acompañaban ~220 fardos funerarios en media docena de chullpas.",
    "32 quipus de Leymebamba", "32 quipus, ~220 fardos",
    "Contar los quipus UR de procedencia Leymebamba/Chachapoyas en quipus.csv.",
    "parcial")

# ---------------- 2002 Conklin ----------------
add("Conklin 2002, A Khipu Information String Theory", "Capítulo sin resumen ni texto: no contiene afirmaciones verificables en la ficha.",
    "ninguno", "sin datos", "No evaluable; requiere conseguir el texto.", "no")

# ---------------- 2002 Salomon Tupicocha ----------------
add("Salomon 2002, Patrimonial Khipu in Tupicocha", "Los quipocamayos de Tupicocha codifican la organización social (ayllus) y son un quipu patrimonial vivo.",
    "Quipocamayos de Tupicocha (no arqueológicos)", "sin N en la ficha",
    "No hay quipus de Tupicocha en quipus.csv (0 registros); no comprobable con este corpus.",
    "no")

# ---------------- 2003 Urton ----------------
U03 = "Urton 2003, Signs of the Inka Khipu"
add(U03, "Los rasgos constructivos (torsión/spin, ply, dirección de nudo) forman secuencias binarias que codifican información.",
    "Todos; apéndice UR19", "sistema binario",
    "Comprobar si torsión y dirección de nudo varían de forma estructurada dentro del quipu (no uniformes) y si predicen algo; UR019 está en KFG.",
    "parcial")
add(U03, "El apéndice tabula UR19 (Chachapoyas) como caso de codificación binaria.",
    "UR19 (UR019 en KFG)", "1 quipu",
    "Comparar la tabla publicada con UR019 de cuerdas.csv (requiere el libro).",
    "parcial")
add(U03, "La capacidad informativa del sistema binario permitiría almacenar información semántica compleja.",
    "Todos", "sin N",
    "No falsable sin desciframiento; sólo se puede testear la premisa de variabilidad de rasgos.",
    "no")

# ---------------- 2004 Salomon ----------------
add("Salomon 2004, The Cord Keepers", "Tupicocha no es una piedra Rosetta, pero muestra continuidad del sistema de cordeles articulado con los ayllus.",
    "Quipocamayos de Tupicocha", "caso único",
    "No hay quipus etnográficos de Tupicocha en el corpus.",
    "no")
add("Salomon 2004, The Cord Keepers", "El quipu es un 'data graphic' más que un texto.",
    "Todos", "sin N",
    "Afirmación interpretativa; no falsable con cuerdas.csv.",
    "no")

# ---------------- 2005 Ascher ----------------
A05 = "Ascher 2005, Spin, Ply and Knot Direction"
add(A05, "Spin y ply son uniformes en todos los cordeles de un quipu, salvo 3 quipus en que difiere el cordón principal.",
    "59 quipus bien descritos", "3 excepciones / 59",
    "Calcular por quipu la uniformidad de `torsion` (S/Z) y comparar con un nulo que preserve la frecuencia global.",
    "si")
add(A05, "En ~81% de los quipus la dirección de nudo es uniforme en todo el quipu; el 19% restante es mixta.",
    "59 quipus", "81% / 19%",
    "Por quipu, contar direcciones S/Z de todos los racimos en `nudos`; calcular % de quipus con una sola dirección.",
    "si")
add(A05, "Spin, ply y dirección de nudo no sirven para distinguir datos cuantitativos de no cuantitativos.",
    "59 quipus", "conclusión negativa",
    "Test: ¿la uniformidad/mixtura de dirección predice presencia de valores o de jerarquía?",
    "parcial")

# ---------------- 2005 Urton archives ----------------
U05 = "Urton 2005, Khipu Archives"
add(U05, "AS159 y AS173 son cuentas duplicadas: los 7 primeros pendientes de AS159 son idénticos en valor y estructura a los pendientes P2-P8 de AS173.",
    "AS159 (KH0175), AS173 (KH0190)", "7 valores consecutivos",
    "Extraer secuencias de valores nivel 0 y buscar el tramo común; p-valor por permutación de una de las secuencias.",
    "si")
add(U05, "AS194 y AS195 son cuentas duplicadas: valores casi idénticos (120), difieren en un tercer pendiente ausente y en los colores.",
    "AS194 (KH0212), AS195 (KH0213)", "120 = 120; 1 pendiente extra en AS194",
    "Comparar valores nivel 0 y colores de AS194/AS195.",
    "si")
add(U05, "AS114 y AS123 comparten un segmento de 10 cuerdas con valores 40-9-57-30-56-80-21-8-22-12 (AS114 pendientes 40-49; AS123 41-50).",
    "AS114, AS123", "10 valores",
    "AS114 y AS123 no están en KFG; sólo comprobable si se incorporan desde KDB/OKR.",
    "no")
add(U05, "AS116 y AS150 comparten un segmento con diferencias regulares (AS116 siempre menor), compatible con dos conteos sucesivos.",
    "AS116, AS150", "segmento con diferencias regulares",
    "AS116 y AS150 no están en KFG.",
    "no")
add(U05, "Los quipus de Puruchuco 2, 9 y 3 son tres versiones concordantes de una misma cuenta; el 9 es la versión estandarizada.",
    "Puruchuco 2, 9, 3 (posiblemente HP002, HP009, HP003)", "3 quipus; 74, 71 y 62 pendientes",
    "Comparar matrices de valores y colores entre HP002/HP009/HP003 y ver si son el triplete más parecido del archivo HP.",
    "parcial")
add(U05, "UR6 tiene 762 pendientes y 2.962 nudos en total (corregido desde 3.005 en 2001).",
    "UR6", "762 pendientes; 2.962 nudos",
    "Contar pendientes y nudos (suma de vueltas/nudos por racimo) en UR006.",
    "si")
add(U05, "UR6 contiene 10 conjuntos numéricos de tres términos (p. ej. 20-61-20; 11-35-20; 30-65-20; 10-30-10), todos en las tres últimas cuerdas de los 'loop pendants', interpretados como etiquetas de identidad.",
    "UR6", "10 conjuntos de 3 términos",
    "Buscar tripletes de valores consecutivos en el extremo de grupos/loop pendants de UR006; requiere identificar loop pendants (union/terminacion).",
    "parcial")
add(U05, "Si los tripletes de UR6 son etiquetas y no cantidades, el censo baja de ~3.000 a 1.513 (año 1) + 601 (año 2) = 2.114 contribuyentes.",
    "UR6", "2.114 vs ~3.000",
    "Depende de la interpretación de los tripletes; no verificable sin ellos.",
    "no")
add(U05, "UR9 y UR21 replican el segmento de cuatro meses de UR6 (aprox. 1/6 de los datos).",
    "UR6, UR9, UR21", "~1/6 del registro",
    "Buscar el tramo común más largo entre las secuencias de valores de UR006, UR009 y UR021; nulo por permutación.",
    "si")
add(U05, "La existencia de cuentas duplicadas refuta la tesis de Cobo (1653) de que cada quipu sólo podía ser leído por quien lo hizo.",
    "Pares AS159/AS173, AS194/AS195, AS114/AS123, AS116/AS150, Puruchuco", ">=5 pares/tríos",
    "Si los pares se confirman, la conclusión se sigue por lógica; el test es la existencia de los matches.",
    "parcial")

# ordenar por fuente (año)
import re
def year(f):
    m = re.search(r"(\d{4})", f)
    return int(m.group(1)) if m else 9999
R.sort(key=lambda r: (year(r["fuente"]), r["fuente"]))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "afirmaciones.csv")
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(R)
print("filas:", len(R), "->", out)
print("por comprobabilidad:", {k: sum(1 for r in R if r["comprobable_con_datos_del_repo"] == k) for k in ["si", "parcial", "no"]})
