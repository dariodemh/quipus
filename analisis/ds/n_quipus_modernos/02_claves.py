# -*- coding: utf-8 -*-
"""Transcribe las claves etnograficas/coloniales a dos CSV:
  claves.csv              -> una fila por fuente x rasgo x significado
  cuerdas_con_clave.csv   -> las unicas tablas cuerda-por-cuerda publicadas
                             (Cutusuma, Uhle 1897 + Hyland 2014; Laramarca,
                             Soto Flores 1950-51, estructura descrita por Hyland 2020)
No se inventan valores: los campos no publicados quedan vacios.
"""
import pandas as pd

cols = ["id", "fuente", "año", "lugar", "siglo", "uso", "rasgo",
        "significado_documentado", "evidencia", "n_cuerdas_datos", "cita", "nivel"]

R = []
def add(**kw):
    R.append(kw)

# --- Cutusuma, Bolivia: el unico caso con tabla cuerda por cuerda y valores ---
add(id="UHLE1897_1", fuente="Uhle 1897; reanalisis de Hyland 2014", año="1894-1895",
    lugar="Hacienda Cutusuma, Lago Titicaca, Bolivia", siglo="XIX", uso="rebaño",
    rasgo="torsión (ply final S/Z)",
    significado_documentado="S = hembra / categoría no marcada y más valorada; Z = macho castrado / categoría marcada. En las vacas: S = ordeñada a diario; Z = seca o no ordeñada todos los días.",
    evidencia="testimonio directo del pastor aimara (notas de campo de Uhle) + análisis del objeto",
    n_cuerdas_datos="7", cita="Uhle 1897: 51-63; Hyland 2014: 644-647", nivel="bien apoyado")
add(id="UHLE1897_2", fuente="Uhle 1897; Hyland 2014", año="1894-1895",
    lugar="Cutusuma, Bolivia", siglo="XIX", uso="rebaño", rasgo="posición / unión",
    significado_documentado="El cordón superior se dobla en un asa; a un lado las ovejas (387) y al otro los machos capados (285). Los machos van siempre en medio, entre las hembras y los corderos.",
    evidencia="testimonio directo", n_cuerdas_datos="2", cita="Hyland 2014: 645-646", nivel="bien apoyado")
add(id="UHLE1897_3", fuente="Uhle 1897; Hyland 2014", año="1894-1895",
    lugar="Cutusuma, Bolivia", siglo="XIX", uso="rebaño", rasgo="subsidiaria",
    significado_documentado="Dos cuerdas atadas con hilo marrón a la cuerda de los machos = corderos destetados, separados por corral (121 y 99).",
    evidencia="testimonio directo", n_cuerdas_datos="2", cita="Hyland 2014: 646", nivel="bien apoyado")
add(id="UHLE1897_4", fuente="Uhle 1897; Hyland 2014", año="1894-1895",
    lugar="Cutusuma, Bolivia", siglo="XIX", uso="rebaño", rasgo="objeto atado (hilo)",
    significado_documentado="El color del hilo con que se ata el grupo (marrón vs blanco) separa el grupo de corderos del grupo de vacas lecheras.",
    evidencia="testimonio directo", n_cuerdas_datos="5", cita="Hyland 2014: 646", nivel="apoyado")
add(id="UHLE1897_5", fuente="Uhle 1897; Hyland 2014", año="1894-1895",
    lugar="Cutusuma, Bolivia", siglo="XIX", uso="rebaño", rasgo="nudo (tamaño)",
    significado_documentado="Nudos grandes = centenas, medianos = decenas, pequeños = unidades; el cordón superior registra el total de cada clase.",
    evidencia="testimonio directo + lectura decimal", n_cuerdas_datos="7", cita="Uhle 1897: 51-63; Hyland 2014: 644", nivel="bien apoyado")

# --- Laramarca, Peru ---
add(id="SOTO1950_1", fuente="Soto Flores 1950-51; descripcion en Hyland 2020", año="1948-1950",
    lugar="Comunidad de Laramarca, Huancavelica, Peru", siglo="XX", uso="rebaño",
    rasgo="color",
    significado_documentado="Colgante negro = ovejas machos; colgante blanco = ovejas hembras.",
    evidencia="etnografía con informantes", n_cuerdas_datos="4", cita="Soto Flores 1950-51: 299-306; Hyland 2020: 137-158", nivel="apoyado")
add(id="SOTO1950_2", fuente="Soto Flores 1950-51; Hyland 2020", año="1948-1950",
    lugar="Laramarca, Peru", siglo="XX", uso="rebaño", rasgo="subsidiaria + color",
    significado_documentado="Subsidiaria negra = corderos machos; subsidiaria blanca = corderas hembras. La subsidiaria hereda el color de la madre y añade la edad/cría.",
    evidencia="etnografía", n_cuerdas_datos="2", cita="Soto Flores 1950-51: 299-306; Hyland 2020: 137-158", nivel="apoyado")
add(id="SOTO1950_3", fuente="Soto Flores 1950-51; Hyland 2020", año="1948-1950",
    lugar="Laramarca, Peru", siglo="XX", uso="rebaño", rasgo="posición (cordón principal)",
    significado_documentado="Los nudos en el propio cordón principal registran totales; los colgantes, clases de animales.",
    evidencia="etnografía", n_cuerdas_datos="2", cita="Hyland 2020: 137-158, comentario a Soto Flores", nivel="propuesto")

add(id="URTON2003_1", fuente="Urton 2003", año="2003",
    lugar="Andes", siglo="XVI", uso="administrativo / teorico",
    rasgo="torsión (ply), unión, dirección de nudo",
    significado_documentado="Propone que el ply y la direccion del nudo codifican oposiciones binarias por marcadez (S no marcado, Z marcado); no da una clave semantica verificada.",
    evidencia="teoria / sintesis", n_cuerdas_datos="0", cita="Urton 2003: 143-154", nivel="propuesto")

# --- Mackey, tipologia y practicas ---
add(id="MACKEY2002_1", fuente="Mackey 1970, 2002", año="1965-1967",
    lugar="Cusco, Puno y La Libertad, Peru", siglo="XX", uso="rebaño / productos",
    rasgo="estructura (tipo A/B/C)",
    significado_documentado="Tipo A = khipu incaico estandar; tipo B = un solo hilo de dos cabos doblado, con nudos en la parte gruesa (centenas/millares) y dos colas (decenas/unidades); tipo C = cordón único con zonas decimales. 43 khipus de pastores/cosecha, 24 estudiados por ella, 20 informantes.",
    evidencia="encuesta etnográfica + colecciones", n_cuerdas_datos="0 (tipologia, no tabla)", cita="Mackey 2002: 321-347, esp. 327-335", nivel="apoyado")
add(id="MACKEY2002_2", fuente="Mackey 2002", año="1965-1967",
    lugar="Paucartambo, Cusco", siglo="XX", uso="rebaño", rasgo="posición / color / número inicial",
    significado_documentado="El pastor marcaba el inicio del khipu con tres rasgos redundantes: número inicial, color de la cuerda y posición relativa.",
    evidencia="observación directa", n_cuerdas_datos="0", cita="Mackey 2002: 335", nivel="apoyado")
add(id="MACKEY2002_3", fuente="Mackey 2002", año="1965-1967",
    lugar="Cusco", siglo="XX", uso="rebaño", rasgo="nudo / posición",
    significado_documentado="En los khipus tipo B, un nudo en la parte doble y gruesa vale 100 o 1000; en las colas, 10 o 1. La posición en la estructura fija el valor.",
    evidencia="etnografía", n_cuerdas_datos="0", cita="Mackey 2002: 330-333", nivel="apoyado")

# --- Nunez del Prado y Holm: fuentes citadas pero sin clave por cuerda ---
add(id="NUNEZ1950_1", fuente="Núñez del Prado 1950", año="1950",
    lugar="Cusco, Peru", siglo="XX", uso="rebaño / ritual",
    rasgo="nudo, color, grosor",
    significado_documentado="Registra que los khipus modernos siguen en uso y combinan nudos, grosores y colores; no publica una tabla cuerda-por-cuerda ni glosas verificables.",
    evidencia="etnografía descriptiva", n_cuerdas_datos="0", cita="Núñez del Prado 1950: 7-24", nivel="especulativo")
add(id="HOLM1953_1", fuente="Holm 1953/1968", año="1953",
    lugar="Costa ecuatoriana", siglo="XX", uso="mnemónico / calendario",
    rasgo="nudo",
    significado_documentado="El 'sapán' ecuatoriano se describe como cordón de nudos usado como recurso mnemónico; no hay clave publicada de colores ni de cuerdas.",
    evidencia="etnografía descriptiva", n_cuerdas_datos="0", cita="Holm 1953; Holm 1968: 85-90", nivel="especulativo")

# --- Tupicocha ---
add(id="SALOMON2004_1", fuente="Salomon 2004 (y 2006 en espanol)", año="1994-2004",
    lugar="San Andres de Tupicocha, Huarochiri, Peru", siglo="XX", uso="cívico / ritual / trabajo comunal",
    rasgo="posición / jerarquía de colgantes y subsidiarias",
    significado_documentado="Cada ayllu/parcialidad conserva dos quipocamayos como insignia; los cordeles representan cargos, miembros y obligaciones, ordenados jerárquicamente. Los marcadores (motas, pachacamanta) identifican el objeto y su rango. Ya no se leen, pero se exhiben cada 2-3 de enero en la huayrona.",
    evidencia="etnografía + documentos de ayllu", n_cuerdas_datos="0 (no hay tabla publica)", cita="Salomon 2004: caps. 6-7; Salomon 2006 (IFEA)", nivel="apoyado")
add(id="SALOMON2004_2", fuente="Salomon 2004", año="1994-2004",
    lugar="Tupicocha, Peru", siglo="XX", uso="cívico", rasgo="objeto atado / borla",
    significado_documentado="Los marcadores de colores vivos (motas, puños, 'pachacamanta') marcan extremos, secciones e identidad del quipocamayo; se leen a distancia en la ceremonia.",
    evidencia="etnografía", n_cuerdas_datos="0", cita="Salomon 2006, cap. 6 (OpenEdition, pp. 171-224)", nivel="propuesto")

# --- Rapaz ---
add(id="PETERS2006_1", fuente="Peters y Salomon 2006; Salomon 2017", año="2002-2006",
    lugar="San Cristobal de Rapaz, Oyon, Lima, Peru", siglo="XIX-XX", uso="ritual / agrícola / rebaño",
    rasgo="objeto atado (figurinas, mechones, cuero, pompones) y color/torsion",
    significado_documentado="263 objetos unilineales, sin colgantes; los nudos importan poco y los objetos atados son signos informativos. Los comuneros dicen que registran el trabajo y la relacion con los cerros; no hay clave cordel por cordel.",
    evidencia="etnografía + conservacion", n_cuerdas_datos="0", cita="Peters y Salomon 2006: 40-43", nivel="propuesto")

# --- Anchucaya ---
add(id="HYLAND2016_1", fuente="Hyland 2016", año="1935-1940s",
    lugar="Santiago de Anchucaya, Huarochiri, Peru", siglo="XX", uso="trabajo comunal",
    rasgo="color / posición del grupo",
    significado_documentado="Cada ayllu tiene un color fijo; la secuencia de 6 colores se repite 10 veces (seriacion); cada grupo de 6 colgantes = una de las 10 tareas comunales, en orden memorizado (Runa Wacho, Mula Wacho, ..., Papel).",
    evidencia="testimonio del ultimo khipukamayuq (Tello 1935) + nieto", n_cuerdas_datos="60 en el khipu descrito; RT21287 = 71", cita="Hyland 2016: 490-509, secciones 'Watancha'", nivel="bien apoyado")
add(id="HYLAND2016_2", fuente="Hyland 2016", año="1935-1940s",
    lugar="Anchucaya, Peru", siglo="XX", uso="trabajo comunal", rasgo="color (bandas)",
    significado_documentado="En los khipus de ayllu, cada banda de color = un miembro individual, en orden de ingreso (de mayor a menor); cada colgante dentro de la banda = una tarea (5 o 6).",
    evidencia="testimonio + analisis de RT21287", n_cuerdas_datos="71", cita="Hyland 2016", nivel="apoyado")
add(id="HYLAND2016_3", fuente="Hyland 2016; Hyland 2014", año="1935-1940s",
    lugar="Anchucaya, Peru", siglo="XX", uso="trabajo comunal", rasgo="torsión (ply)",
    significado_documentado="Una banda entera de colgantes de color marron claro es Z mientras el resto es S; se interpreta como el trabajo de una mujer, valorado a la mitad que el del hombre.",
    evidencia="analogia con Cutusuma + testimonio de que la mujer vale la mitad", n_cuerdas_datos="~6", cita="Hyland 2016 (nota 16); Hyland 2014", nivel="propuesto")
add(id="HYLAND2016_4", fuente="Hyland 2016", año="1935-1940s",
    lugar="Anchucaya, Peru", siglo="XX", uso="trabajo comunal", rasgo="posición sobre el colgante (mitad superior/inferior)",
    significado_documentado="La mitad superior del colgante, junto al cordon principal, registra lo hecho; la mitad inferior, lo que se debe.",
    evidencia="testimonio directo", n_cuerdas_datos="71", cita="Hyland 2016", nivel="bien apoyado")
add(id="HYLAND2016_5", fuente="Hyland 2016", año="1935-1940s",
    lugar="Anchucaya, Peru", siglo="XX", uso="trabajo comunal", rasgo="objeto atado (tela blanca)",
    significado_documentado="Rectangulos de tela blanca atados a los colgantes = la tarea 'Papel' (comprar papel sellado oficial).",
    evidencia="testimonio + objeto", n_cuerdas_datos="varios", cita="Hyland 2016", nivel="apoyado")
add(id="HYLAND2016_6", fuente="Hyland 2016", año="1935-1940s",
    lugar="Anchucaya, Peru", siglo="XX", uso="trabajo comunal", rasgo="borla (cayte)",
    significado_documentado="El cayte grande marca el inicio del khipu y anuncia el genero/tema; el cayte pequeno marca el final.",
    evidencia="testimonio directo", n_cuerdas_datos="1", cita="Hyland 2016", nivel="apoyado")

# --- Collata ---
add(id="HYLAND2017_1", fuente="Hyland 2017", año="1783 (atribuido)", siglo="XVIII",
    lugar="San Juan de Collata, Huarochiri, Peru", uso="carta / narrativa de guerra",
    rasgo="color + fibra animal + torsión",
    significado_documentado="95 combinaciones distintas en 487 colgantes; los ultimos cordones de cada khipu combinarian color, especie animal y ply para deletrear nombres de ayllu (ALLUKA, YAKAPAR). Es una hipotesis de desciframiento, no una clave verificada.",
    evidencia="testimonio de comuneros + analisis de objetos", n_cuerdas_datos="487", cita="Hyland 2017: 412-419", nivel="especulativo")
add(id="HYLAND2017_2", fuente="Hyland 2017; Hyland 2025", año="1783", siglo="XVIII",
    lugar="Collata, Peru", uso="carta / narrativa", rasgo="objeto atado (tiras de insignia, pelo)",
    significado_documentado="Tiras de la bufanda de un lider cosidas al khipu = insignia/identidad; el pelo humano en el cordon principal = firma del autor.",
    evidencia="analisis de objeto + etnografia", n_cuerdas_datos="2 khipus", cita="Hyland 2025 (Science Advances); Hyland 2017", nivel="apoyado")

# --- Khipu boards / Casta / Mangas ---
add(id="HYLAND2021_1", fuente="Hyland, Bennison y Hyland 2021", año="XIX-1950s",
    lugar="San Pedro de Casta y San Francisco de Mangas, Huarochiri, Peru", siglo="XIX-XX", uso="trabajo comunal / confession / padron",
    rasgo="color, ply, direccion de nudo, grosor",
    significado_documentado="En el tablero de Mangas (181 agujeros, 87 cuerdas conservadas): 17 colores y >37 patrones; la direccion del nudo indica la mitad/moiety del individuo; el ply varia; tres grosores (jerga/trama/hilasa) distinguen textura. Cada agujero = un nombre escrito en el padron.",
    evidencia="etnografia + documento (Entablo) + objeto", n_cuerdas_datos="87", cita="Hyland, Bennison y Hyland 2021: 400-403", nivel="apoyado")

# --- Confesion ---
add(id="BOCANEGRA1631_1", fuente="Pérez Bocanegra 1631; Harrison 2013; Charles 2013", año="1622-1631",
    lugar="Cusco / Andahuaylillas, Peru", siglo="XVII", uso="confesión",
    rasgo="color / nudo",
    significado_documentado="Los quipus de confesion usan colores para dividir las categorias de pecados y nudos para el numero; se prestan y reutilizan. El confesor podia 'saber por los colores' que pecados habia, pero no se conserva la clave color->pecado.",
    evidencia="documento colonial (Ritual formulario)", n_cuerdas_datos="0", cita="Pérez Bocanegra 1631: 111-112, 341; Harrison 2013: 145-166", nivel="apoyado")
add(id="BOCANEGRA1631_2", fuente="Pérez Bocanegra 1631", año="1631", lugar="Cusco, Peru",
    siglo="XVII", uso="confesión", rasgo="posición / número de cuerdas",
    significado_documentado="No hay tabla cordel-por-cordel ni lista de colores; solo se afirma que hay 'muchos colores' para hacer division de los pecados.",
    evidencia="documento", n_cuerdas_datos="0", cita="Pérez Bocanegra 1631: 111", nivel="especulativo")

# --- Chinu / Qaqachaka ---
add(id="ARNOLD2006_1", fuente="Arnold y Yapita 2006", año="1990-2005",
    lugar="Qaqachaka, Oruro, Bolivia", siglo="XX-XXI", uso="rebaño / ritual k'illpha",
    rasgo="color / nudo / posición",
    significado_documentado="Cada colgante del chinu es 'de una persona' (su camino); el color del hilo corresponde al color/dueno del animal; un hilo insertado en el nudo (chimpu) marca el color del animal (rojo, blanco, negro); el nudo masculino (urqu chinu) marca la cantidad de un grupo de cierto color. El cordon principal es la 'via lactea'.",
    evidencia="etnografia de largo plazo", n_cuerdas_datos="0 (sin tabla)", cita="Arnold y Yapita 2006: 185-208, esp. 192-193", nivel="apoyado")
add(id="ARNOLD2006_2", fuente="Arnold y Yapita 2006", año="1990-2005",
    lugar="Qaqachaka, Bolivia", siglo="XX-XXI", uso="rebaño", rasgo="color insertado (chimpu)",
    significado_documentado="El hilo de color insertado en el nudo no es adorno: especifica el color del animal contado; sin el, el numero no se refiere a una clase de animal.",
    evidencia="etnografia", n_cuerdas_datos="0", cita="Arnold y Yapita 2006: 192-193", nivel="apoyado")

# --- Pimentel, memoria ---
add(id="PIMENTEL2005_1", fuente="Pimentel, via Hyland 2020/2023", año="siglos XIX-XX",
    lugar="Suroeste de Bolivia", siglo="XIX-XX", uso="memoria / sacrificios / genealogia / cosecha / rebaño",
    rasgo="unión (colgante inca atado alrededor de otro)",
    significado_documentado="Un colgante inca atado alrededor de un colgante adyacente indica que el primero 'anula' al segundo. Otros rasgos: grosor, largo y variaciones menores de color.",
    evidencia="testimonio de ancianos que replicaron los khipus", n_cuerdas_datos="4 khipus replicados", cita="Pimentel 2005, via Hyland 2020: 137-158", nivel="propuesto")

# --- Colonial: tributo / hacienda ---
add(id="PLATT2002_1", fuente="Platt 2002", año="1581 (juicio)",
    lugar="Sacaca, Charcas (hoy Potosi, Bolivia)", siglo="XVI", uso="tributo",
    rasgo="cuerda / nudo / año",
    significado_documentado="Los chinu del juicio Montemayor registran productos y anos; dos khipukamayuq leen el mismo chinu con cifras distintas. No se publica una tabla de colores ni de cuerdas.",
    evidencia="documento judicial", n_cuerdas_datos="0", cita="Platt 2002: 223-265", nivel="apoyado")
add(id="COFRADIA2013_1", fuente="Amado Gonzales 2013; Curatola y de la Puente 2013", año="siglos XVI-XVIII",
    lugar="Cusco, Peru", siglo="XVI-XVIII", uso="cofradía / iglesia / hacienda",
    rasgo="cuerda / nudo (conteo)",
    significado_documentado="Los quipucamayos registraban ganado y bienes de cofradias, iglesias y haciendas; no se publica una clave cordel-por-cordel.",
    evidencia="documento de archivo", n_cuerdas_datos="0", cita="Amado Gonzales 2013: 307-324", nivel="apoyado")
add(id="CASTRO2013_1", fuente="Castro de Trelles 2013", año="siglo XVII",
    lugar="Hacienda Tulpo, Huamachuco, Peru", siglo="XVII", uso="rebaño / hacienda",
    rasgo="cuerda / nudo (conteo)",
    significado_documentado="Quipus coloniales de hacienda registran ganado vacuno, ovejas y caballos; se conservan referencias documentales, no los cordeles con su clave.",
    evidencia="documento de archivo", n_cuerdas_datos="0", cita="Castro de Trelles 2013: 349-377", nivel="apoyado")

claves = pd.DataFrame(R, columns=cols)
claves.to_csv("claves.csv", index=False, encoding="utf-8-sig")
print("claves.csv", claves.shape)

# ---------------------------------------------------------------------------
# Tabla cuerda por cuerda: Cutusuma (7 cuerdas) y Laramarca (4 cuerdas)
# ---------------------------------------------------------------------------
C = []
def cadd(**kw):
    C.append(kw)

ccols = ["fuente", "lugar", "siglo", "quipu", "cuerda", "nivel", "valor",
         "torsion_ply", "color_fibra", "posicion", "significado", "cita"]

# Cutusuma: nivel 0 = cordon superior doblado; nivel 1 = cuerdas colgantes
cadd(fuente="Uhle 1897; Hyland 2014", lugar="Cutusuma, Bolivia", siglo="XIX",
     quipu="Cutusuma 36392", cuerda="A1", nivel="0 (lado izquierdo del asa)",
     valor="387", torsion_ply="S (dos cordones separados, S)", color_fibra="lana de oveja, blanco/monocromo",
     posicion="izquierda del asa", significado="ovejas hembras adultas ('ovejas')", cita="Hyland 2014: 644-645")
cadd(fuente="Uhle 1897; Hyland 2014", lugar="Cutusuma, Bolivia", siglo="XIX",
     quipu="Cutusuma 36392", cuerda="A2", nivel="0 (lado derecho del asa)",
     valor="285", torsion_ply="Z (dos cordones unidos con torsion final Z)", color_fibra="lana de oveja",
     posicion="derecha del asa, en medio entre hembras y corderos", significado="machos ovinos castrados ('machos capados')", cita="Hyland 2014: 645")
cadd(fuente="Uhle 1897; Hyland 2014", lugar="Cutusuma, Bolivia", siglo="XIX",
     quipu="Cutusuma 36392", cuerda="B1", nivel="1 (atada con hilo marron a A2)",
     valor="121", torsion_ply="S", color_fibra="lana de oveja",
     posicion="colgando de la cuerda de machos", significado="corderos destetados, corral 1", cita="Hyland 2014: 646")
cadd(fuente="Uhle 1897; Hyland 2014", lugar="Cutusuma, Bolivia", siglo="XIX",
     quipu="Cutusuma 36392", cuerda="B2", nivel="1 (atada con hilo marron a A2)",
     valor="99", torsion_ply="S", color_fibra="lana de oveja",
     posicion="colgando de la cuerda de machos", significado="corderos destetados, corral 2", cita="Hyland 2014: 646")
cadd(fuente="Uhle 1897; Hyland 2014", lugar="Cutusuma, Bolivia", siglo="XIX",
     quipu="Cutusuma 36392", cuerda="C1", nivel="1 (atada con hilo blanco al asa)",
     valor="85", torsion_ply="S", color_fibra="lana de oveja",
     posicion="grupo de vacas lecheras", significado="vacas ordeñadas a diario", cita="Hyland 2014: 646-647")
cadd(fuente="Uhle 1897; Hyland 2014", lugar="Cutusuma, Bolivia", siglo="XIX",
     quipu="Cutusuma 36392", cuerda="C2", nivel="1 (atada con hilo blanco al asa)",
     valor="60", torsion_ply="Z", color_fibra="lana de oveja",
     posicion="grupo de vacas lecheras", significado="vacas secas (no ordeñadas)", cita="Hyland 2014: 646-647")
cadd(fuente="Uhle 1897; Hyland 2014", lugar="Cutusuma, Bolivia", siglo="XIX",
     quipu="Cutusuma 36392", cuerda="C3", nivel="1 (atada con hilo blanco al asa)",
     valor="170", torsion_ply="Z", color_fibra="lana de oveja",
     posicion="grupo de vacas lecheras", significado="vacas no ordeñadas todos los dias", cita="Hyland 2014: 646-647")

# Laramarca: dos colgantes y dos subsidiarias, sin valores publicados
cadd(fuente="Soto Flores 1950-51; Hyland 2020", lugar="Laramarca, Peru", siglo="XX",
     quipu="Laramarca (tipo A)", cuerda="p_negro", nivel="0", valor="",
     torsion_ply="", color_fibra="negro", posicion="colgante",
     significado="ovejas machos", cita="Hyland 2020: 137-158, comentario a Soto Flores")
cadd(fuente="Soto Flores 1950-51; Hyland 2020", lugar="Laramarca, Peru", siglo="XX",
     quipu="Laramarca (tipo A)", cuerda="p_negro_s1", nivel="1", valor="",
     torsion_ply="", color_fibra="negro", posicion="subsidiaria del colgante negro",
     significado="corderos machos", cita="Hyland 2020")
cadd(fuente="Soto Flores 1950-51; Hyland 2020", lugar="Laramarca, Peru", siglo="XX",
     quipu="Laramarca (tipo A)", cuerda="p_blanco", nivel="0", valor="",
     torsion_ply="", color_fibra="blanco", posicion="colgante",
     significado="ovejas hembras", cita="Hyland 2020")
cadd(fuente="Soto Flores 1950-51; Hyland 2020", lugar="Laramarca, Peru", siglo="XX",
     quipu="Laramarca (tipo A)", cuerda="p_blanco_s1", nivel="1", valor="",
     torsion_ply="", color_fibra="blanco", posicion="subsidiaria del colgante blanco",
     significado="corderas hembras", cita="Hyland 2020")

cuerdas = pd.DataFrame(C, columns=ccols)
cuerdas.to_csv("cuerdas_con_clave.csv", index=False, encoding="utf-8-sig")
print("cuerdas_con_clave.csv", cuerdas.shape)
