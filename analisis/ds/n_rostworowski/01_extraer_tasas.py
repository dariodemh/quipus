# -*- coding: utf-8 -*-
"""
Extrae las cifras de tributo y las unidades sociopolíticas de
Rostworowski, Costa peruana prehispánica (Obras completas III),
texto local analisis/fuentes_txt/Rostworowski_CostaPeruana.txt.

Las citas son por NÚMERO DE LÍNEA del txt (la edición digital no trae
paginación impresa). Se indica también la sección.

Salidas: tasas.csv, parcialidades.csv, resultados_tasas.txt
"""
import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1. TASAS Y CIFRAS DE TRIBUTO
#    valor_pesos = valor monetario según el documento (pesos ensayados)
# ---------------------------------------------------------------------------
TASAS = [
    # año, grupo, especie, cantidad, unidad, valor_pesos, linea, nota
    (1577, "Lunahuaná", "tributarios (total)", 740, "personas", None, 831,
     "Visita de Juan de Vera Olguín; 740 indios tributarios casados, viudos y solteros, 18-50 años"),
    (1577, "Lunahuaná", "tributarios (payantes)", 732, "personas", None, 836,
     "740 menos 8 reservados para caciques"),
    (1577, "Lunahuaná", "viejos", 89, "personas", None, 832, "más de 50 años, no pagan"),
    (1577, "Lunahuaná", "muchachos", 601, "personas", None, 833, "17 años para abajo, no pagan"),
    (1577, "Lunahuaná", "mujeres", 1846, "personas", None, 834, "todas las edades y estados"),
    (1577, "Lunahuaná", "personas (total)", 3276, "personas", None, 835,
     "740+89+601+1846 = 3276"),
    (1577, "Lunahuaná", "plata ensayada", 2196, "pesos", 2196.0, 837,
     "3 pesos por tributario payante"),
    (1577, "Lunahuaná", "ropa de algodón", 366, "piezas", 869.25, 838,
     "2 pesos 3 tomines por pieza; 869 pesos 2 tomines"),
    (1577, "Lunahuaná", "maíz", 500, "fanegas", 250.0, 839,
     "medio peso por fanega; puestas en los pueblos"),
    (1577, "Lunahuaná", "aves de Castilla", 758, "aves", 94.75, 840,
     "1 tomín por ave; 94 pesos 6 tomines"),
    (1577, "Lunahuaná", "total tasa", None, "pesos", 3660.0, 844,
     "5 pesos por tributario payante; el documento suma 3660"),
    (1577, "Lunahuaná", "doctrina", None, "pesos", 800.0, 846, "dos sacerdotes"),
    (1577, "Lunahuaná", "fábrica de iglesias", None, "pesos", 50.0, 847, ""),
    (1577, "Lunahuaná", "justicias y defensores", None, "pesos", 400.0, 848, ""),
    (1577, "Lunahuaná", "caciques", None, "pesos", 98.0, 849, "salario de los caciques"),
    (1577, "Lunahuaná", "hospital", 1, "tomín/tributario/año", None, 845,
     "un tomín de plata ensayada por tributario"),
    (1577, "Lunahuaná", "costas (total)", None, "pesos", 1348.0, 850,
     "doctrina 800 + fábrica 50 + justicias 400 + caciques 98"),

    (1590, "Lunahuaná", "tributarios (total)", 474, "personas", None, 802,
     "revisita de Francisco de Soto; 18-50 años"),
    (1590, "Lunahuaná", "tributarios (payantes)", 469, "personas", None, 802,
     "474 menos 5 reservados para caciques"),
    (1590, "Lunahuaná", "viejos", 96, "personas", None, 803, "más de 50 años, no pagan"),
    (1590, "Lunahuaná", "muchachos", 372, "personas", None, 804, "17 años para abajo, no pagan"),
    (1590, "Lunahuaná", "mujeres", 973, "personas", None, 805, "todas las edades y estados"),
    (1590, "Lunahuaná", "personas (total)", 1915, "personas", None, 805,
     "474+96+372+973 = 1915"),
    (1590, "Lunahuaná", "plata ensayada", 1392.34375, "pesos", 1392.34375, 806,
     "1392 pesos 2 tomines 9 granos; 2 pesos 7 tomines 9 granos por payante"),
    (1590, "Lunahuaná", "ropa de algodón", 234.5, "piezas", 556.9375, 807,
     "2 pesos 3 tomines por pieza; 556 pesos 7 tomines 6 granos"),
    (1590, "Lunahuaná", "trigo y maíz", 641.25, "fanegas", 320.625, 807,
     "641 fanegas 3 almudes; 4 tomines por fanega (320 pesos 5 tomines)"),
    (1590, "Lunahuaná", "ropa sustituta del trigo/maíz", 135, "piezas", 320.625, 807,
     "desde San Juan de 1591, 135 piezas de ropa en lugar del trigo/maíz"),
    (1590, "Lunahuaná", "aves de Castilla", 483.5, "aves", 60.4375, 809,
     "1 tomín por ave; 60 pesos 3 tomines 6 granos"),
    (1590, "Lunahuaná", "total tasa", None, "pesos", 2330.28125, 809,
     "2330 pesos 2 tomines 9 granos; 4 pesos 7 tomines 9 granos por payante"),
    (1590, "Lunahuaná", "neto del encomendero", None, "pesos", 1294.28125, 813,
     "tras descontar 1036 pesos de costas"),
    (1590, "Lunahuaná", "doctrina", None, "pesos", 700.0, 811, ""),
    (1590, "Lunahuaná", "fábrica de iglesias", None, "pesos", 33.0, 811, ""),
    (1590, "Lunahuaná", "justicias y defensores", None, "pesos", 240.0, 811, ""),
    (1590, "Lunahuaná", "costas (total)", None, "pesos", 1036.0, 811,
     "total de lo que se saca de los 2330 pesos"),
    (1557, "Cañete (villa)", "merced para acequias", 100, "pesos/año", 100.0, 660,
     "sacados de los tributos de repartimientos vacos"),

    (1571, "Collique", "tributarios", 15, "personas", None, 230,
     "Visita de Martínez Rengifo; población menguada"),
    (1571, "Collique", "muchachos", 7, "personas", None, 230, ""),
    (1571, "Collique", "niños", 2, "personas", None, 230, ""),

    (1571, "Guancayos", "coca al Inca", 45, "cestos", None, 2601,
     "5 cestos por pachaca; 45 = 9 x 5 (el texto también dice 'cinco pachaca' en 369)"),
    (1571, "Guancayos", "coca al Sol", None, "huerta especial", None, 2601,
     "coca verde de una huerta especial, sin cifra"),
    (1571, "Guancayos", "ropa de algodón", 26, "piezas", None, 340,
     "mitad hombre, mitad mujer"),
    (1571, "Guancayos", "cumbi galano", 2, "piezas", None, 340, ""),
    (1571, "Guancayos", "ollas", 10, "ollas", None, 340, "grandes y chicas"),
    (1571, "Guancayos", "rodelas de madera", 10, "rodelas", None, 340, "para las orejas"),
    (1571, "Guancayos", "sandalias/ojotas", 20, "pares", None, 340, ""),
    (1571, "Guancayos", "ganado del Inca", 300, "cabezas", None, 340,
     "cuidado en tierras del Inca; carne llevada al Cusco"),
    (1571, "Guancayos", "indios para el Inca", 3, "personas", None, 342,
     "hijos de caciques"),
    (1571, "Guancayos", "indios para las mamaconas", 3, "personas", None, 342, ""),
    (1571, "Guancayos", "muchachas para mamaconas", 10, "personas", None, 342,
     "diez muchachas hermosas elegidas"),
    (1571, "Guancayos", "coca de mitmaq estatales", "150-160", "costales/año", None, 2601,
     "estimación del quipucamayoc Juan Chauca"),
    (1571, "Guancayos", "coca del curaca principal", 40, "cestos", None, 2603,
     "20 cestos por cada una de dos mitas"),
    (1571, "Guancayos", "coca del jefe de Guarauni", 20, "cestos", None, 2605,
     "20 cestos en ambas mitas"),
    (1571, "Guancayos", "coca por runa de Guarauni", 2, "cestos", None, 2607,
     "dos cestos en las dos mitas"),

    (1534, "Chincha", "tributarios", 30000, "personas", None, 2431,
     "30 caciques de 1000 indios cada uno"),
    (1570, "Chincha", "tributarios", 600, "personas", None, 2436,
     "supervivientes según el 'Aviso'"),
    (1534, "Chincha", "labradores", 12000, "personas", None, 2432,
     "de los 30 000"),
    (1534, "Chincha", "pescadores", 10000, "personas", None, 2432,
     "de los 30 000"),
    (1534, "Chincha", "mercaderes", 6000, "personas", None, 2915,
     "de los 30 000"),
    (1570, "Chincha", "tierras vacas", 2000, "fanegadas", None, 2436,
     "tierras perdidas, convertidas en monte"),

    (1500, "Cerro Azul (Guarco)", "vasijas de almacenamiento", 9, "vasijas", None, 595,
     "capacidad 700-2000 litros cada una; Estructura D"),
    (1500, "Ungará (Guarco)", "vasijas enterradas", None, "vasijas", None, 606,
     "capacidad 300-500 galones cada una"),
]

# ---------------------------------------------------------------------------
# 2. UNIDADES SOCIOPOLÍTICAS
# ---------------------------------------------------------------------------
PARCIALIDADES = [
    # valle, unidad, nombre, nivel, tributarios, linea, nota
    ("Guarco", "encomienda norte", "Antonio Navarro / Juan Navarro", "encomienda", None, 680,
     "mitad norte del valle, con Asia, Oquilla y Calango"),
    ("Guarco", "encomienda sur", "Alonso Martín de Don Benito", "encomienda", None, 683,
     "segunda encomienda del valle"),
    ("Guarco", "minoría étnica", "coayllos (don Pedro Coayllo)", "mitmaq", 30, 630,
     "hasta treinta indígenas con tierras dadas por los incas en Huanca y Lalna"),
    ("Guarco", "minoría étnica", "chinchas (Tambo de Locos)", "mitmaq", None, 634,
     "tierras en Herbay Bajo/Alto y Palo"),
    ("Guarco", "minoría étnica", "mochicas (Hualcará)", "mitmaq", None, 638,
     "sin lugar preciso en el documento"),
    ("Guarco", "tierras de dios", "Pachacamac (Cuyba/Siuba)", "enclave religioso", None, 644,
     "chacras al sur del valle, junto a la acequia Pachacamilla"),
    ("Guarco", "tierras del Sol", "Vilcahuasi/Huacones", "enclave religioso", None, 649,
     "tierras del Sol al norte de Vilcahuasi"),

    ("Lunahuaná", "señorío", "Lunaguanay (curaca principal)", "señorío", 740, 695,
     "cédula de depósito de 1534; 740 tributarios en la visita de 1577"),
    ("Lunahuaná", "guaranga 1", "Lunaguanay", "guaranga", 183, 706,
     "183 = 732 tributarios payantes / 4 guarangas (derivado)"),
    ("Lunahuaná", "guaranga 2", "Llaquipa (residente en las minas)", "guaranga", 183, 706,
     "183 derivado"),
    ("Lunahuaná", "guaranga 3", "Allauca (mitmaq), pueblo Mullibamba", "guaranga", 183, 712,
     "183 derivado"),
    ("Lunahuaná", "guaranga 4", "Jucxu / Pedro Camaluana", "guaranga", 183, 712,
     "183 derivado; la identificación Jucxu-Camaluana es dudosa en el texto"),
    ("Lunahuaná", "curacas", "8 curacas, 2 por guaranga", "curaca", None, 762,
     "posible división urin/anan de cada guaranga"),
    ("Lunahuaná", "ayllus/barrios", "16 nombres actuales (Caltopilla, Caltopa, Casalla, Catapaya, Con-Con y Ramadilla, Paullu, Langla, Lunahuaná, Patapampa, Condoray, Uchupampa, Paraíso, Lúcumo, San Pedro, Socsi, San Jerónimo)", "ayllu/barrio", None, 716,
     "lista de informantes; posible rezago de antiguos ayllus"),

    ("Collique", "guaranga", "Collique", "guaranga", 1000, 229,
     "guaranga = mil tributarios (cifra ideal/incaica)"),
    ("Collique", "pachaca", "Chuquiruro", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Caxa Chumbi", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Vilca Tanta", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Vilca Chumbi", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Chumbi Guarco", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Chumbi Tanta", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Carua Guanco", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Carua Chumbi", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Chinqui Yanga", "pachaca", None, 236, ""),
    ("Collique", "pachaca", "Chuquitanta", "pachaca", None, 236, ""),
    ("Collique", "pueblo", "Collique (visita 1571)", "pueblo", 15, 230,
     "15 tributarios, 7 muchachos y 2 niños"),

    ("Guancayos", "pachaca", "9 pachacas (no se listan los nombres)", "pachaca", 900, 369,
     "900 hatun runa; el texto dice 'cinco pachaca' y luego 'nueve pachaca' entre cinco jefes; 1+4x2=9 y 5x9=45 apoyan nueve; 100 por pachaca derivado"),
    ("Guancayos", "jefes", "5 jefes: uno gobierna 1 pachaca, cuatro gobiernan 2", "curaca", None, 369,
     "1 + 4x2 = 9 pachacas"),

    ("Chincha", "pachaca", "30 caciques de 1000 indios", "pachaca", 30000, 2431,
     "30 pachacas de 1000 tributarios; un señor mayor"),
    ("Chincha", "grupo laboral", "labradores", "grupo funcional", 12000, 2915, ""),
    ("Chincha", "grupo laboral", "pescadores", "grupo funcional", 10000, 2915, ""),
    ("Chincha", "grupo laboral", "mercaderes", "grupo funcional", 6000, 2915, ""),
]

def main():
    # tasas.csv
    with open(os.path.join(BASE, "tasas.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["anio", "grupo", "especie", "cantidad", "unidad",
                    "valor_pesos", "linea_fuente", "nota"])
        for row in TASAS:
            w.writerow(row)

    # parcialidades.csv
    with open(os.path.join(BASE, "parcialidades.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["valle", "unidad", "nombre", "nivel", "tributarios",
                    "linea_fuente", "nota"])
        for row in PARCIALIDADES:
            w.writerow(row)

    # ------------------------------------------------------------------
    # 3. Ratios por tributario (solo las tasas de Lunahuaná)
    # ------------------------------------------------------------------
    def ratio(cant, trib):
        return cant / trib

    lines = []
    lines.append("RATIOS POR TRIBUTARIO PAYANTE")
    lines.append("=" * 60)
    for anio, trib in [(1577, 732), (1590, 469)]:
        lines.append(f"\n{anio} (payantes = {trib})")
        if anio == 1577:
            items = [("plata (pesos)", 2196.0),
                     ("ropa (piezas)", 366.0),
                     ("maíz (fanegas)", 500.0),
                     ("aves", 758.0),
                     ("total (pesos)", 3660.0)]
        else:
            items = [("plata (pesos)", 1392.34375),
                     ("ropa (piezas)", 234.5),
                     ("trigo+maíz (fanegas)", 641.25),
                     ("aves", 483.5),
                     ("total (pesos)", 2330.28125)]
        for nombre, cant in items:
            lines.append(f"  {nombre:28s} {ratio(cant, trib):8.4f}")

    lines.append("\nCOMPARACIÓN 1577 vs 1590 (mismos conceptos)")
    lines.append("-" * 60)
    pares = [("ropa/payante", 366/732, 234.5/469),
             ("aves/payante", 758/732, 483.5/469),
             ("plata/payante", 2196/732, 1392.34375/469),
             ("total/payante", 3660/732, 2330.28125/469)]
    for nombre, a, b in pares:
        lines.append(f"  {nombre:20s} 1577={a:7.4f}  1590={b:7.4f}  "
                     f"dif={100*(b-a)/a:6.2f}%")

    lines.append("\nCONTROL DE ARITMÉTICA DE LAS TASAS")
    lines.append("-" * 60)
    lines.append("1577 componentes valorados: ropa 366x2,375=%.4f; maíz 500x0,5=%.1f; "
                 "aves 758x0,125=%.3f; suma=%.4f" %
                 (366*2.375, 500*0.5, 758*0.125, 366*2.375+250+758*0.125))
    lines.append("1577 documento: especies 1474; plata 2196; total 3660.")
    lines.append("  -> 2196+1474=3670, no 3660; componentes valorados=%.2f, no 1474." %
                 (366*2.375+250+758*0.125))
    lines.append("  -> El total 3660 sí es exactamente 732 x 5 pesos.")
    lines.append("1590 componentes: ropa 234,5x2,375=%.4f; trigo/maíz 641,25x0,5=%.4f; "
                 "aves 483,5x0,125=%.4f; suma=%.4f" %
                 (234.5*2.375, 641.25*0.5, 483.5*0.125,
                  234.5*2.375+641.25*0.5+483.5*0.125))
    lines.append("1590 documento: total 2330,28125; suma componentes=%.4f" %
                 (1392.34375+234.5*2.375+641.25*0.5+483.5*0.125))

    txt = "\n".join(lines)
    with open(os.path.join(BASE, "resultados_tasas.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print(txt)

if __name__ == "__main__":
    main()
