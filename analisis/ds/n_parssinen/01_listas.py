# -*- coding: utf-8 -*-
"""
01_listas.py — Extrae y codifica las listas ordenadas de unidades con cifras
que aparecen en Pärssinen 1992 (Tawantinsuyu), Pärssinen & Kiviharju 2004
(Textos Andinos) y Rostworowski (Costa peruana), para compararlas con la
firma de 9 partes de UR278.

Salida: listas.csv (formato largo: una fila por unidad de cada lista).
No lee archivos grandes: solo transcribe tablas ya identificadas por línea.
"""
import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "listas.csv")

rows = []


def add(list_id, fuente, linea, region, nivel, orden, nombre, cifra,
        completa=True, estructura="", nota=""):
    rows.append(dict(list_id=list_id, fuente=fuente, linea=linea, region=region,
                     nivel=nivel, orden=orden, nombre=nombre,
                     cifra=("" if cifra is None else cifra),
                     completa=("si" if completa else "no"),
                     estructura=estructura, nota=nota))


# ---------------------------------------------------------------- Cajamarca
# Pärssinen 1992, Table 2 (visita de González de Cuenca, 1567), pp. 386-387.
estruct = "guaranga > 9 pachacas; cacique principal primero; sin mitades internas documentadas"
for i, (nom, val) in enumerate([
        ("Ychican", 104), ("Bambamarca", 75), ("Tacabamba", 78),
        ("Tingomayo", 68), ("Quiden", 49), ("Guangamarca", 75),
        ("Curocchuc", 67), ("Anbagay", 30), ("Pisso", 27)], 1):
    add("caj_bambamarca_1567", "Pärssinen 1992, Table 2", "6316-6343",
        "Cajamarca", "pachaca (guaranga Bambamarca)", i, nom, val,
        estructura=estruct, nota="suma 573; visita González de Cuenca 1567")

# Chondal, misma tabla (n=4; fuera del rango 7-11, se conserva como contexto).
for i, (nom, val) in enumerate([
        ("Pingomarca", 336), ("Nepus", 142), ("Polloques", 144),
        ("Payac", 331)], 1):
    add("caj_chondal_1567", "Pärssinen 1992, Table 2", "6325-6330",
        "Cajamarca", "pachaca (guaranga Chondal, Hanansaya)", i, nom, val,
        estructura="guaranga Hanansaya > 4 pachacas; principal primero",
        nota="suma 953; Chondal es la guaranga mayor pero tiene menos pachacas")

# Pomamarca, misma tabla: 8 pachacas, solo 6 con cifra.
for i, (nom, val) in enumerate([
        ("Pomamarca", 72), ("Collana", 61), ("Chuquiral", 31),
        ("Callad", 102), ("Guambo", 80), ("Yanamango", 49),
        ("Ascape", None), ("Yayros", None)], 1):
    add("caj_pomamarca_1567", "Pärssinen 1992, Table 2", "6344-6365",
        "Cajamarca", "pachaca (guaranga Pomamarca, Hurinsaya)", i, nom, val,
        completa=(val is not None),
        estructura="guaranga Hurinsaya > 8 pachacas; 6 con cifra",
        nota="incompleta; no se usa en las pruebas")

# Las 7 guarangas (sin cifras completas): solo estructura.
for i, nom in enumerate(["Guzmango", "Chuquimango", "Chondal", "Bambamarca",
                         "Cajamarca", "Pomamarca", "Mitimaes"], 1):
    add("caj_7guarangas", "Pärssinen 1992", "4752",
        "Cajamarca", "guaranga", i, nom, None, completa=False,
        estructura="4 Hanansaya (Guzmango, Chuquimango, Chondal, Mitimaes) + 3 Hurinsaya (Bambamarca, Cajamarca, Pomamarca)",
        nota="Pärssinen solo da cifras para Chondal, Bambamarca y Pomamarca")

# ---------------------------------------------------------------- Cuzco
# Pärssinen 1992, Table 4 (título de encomienda a Gómez de Mazuelas, 1535).
estruct = "curacazgo > 9 aldeas/llactas; 7 principales subordinados; orden de khipu"
for i, (nom, val) in enumerate([
        ("Chonda (mitimaes)", 250), ("Guamanrroro", 100), ("Tocoyoco", 20),
        ("Tocayaco", 10), ("Vxaca", 70), ("Tarapa (yungas)", 10),
        ("Matara", 200), ("Chupaico (pastores)", 40),
        ("Yachibamba (yungas)", 30)], 1):
    add("cusco_coco_1535", "Pärssinen 1992, Table 4", "6483-6505",
        "Cuzco/Limatambo", "aldea/llacta (curacazgo Coco)", i, nom, val,
        estructura=estruct,
        nota="suma 720 [730]; 1 pachaca calculativa en Guamanrroro y 2 en Matara")

# ---------------------------------------------------------------- Collasuyu
# Pärssinen 1992, Table 7: parcialidad de Aullaga, cacique Acho.
for i, (nom, val) in enumerate([
        ("Acalvo", 38), ("Berenguela", 18), ("Millme", 53), ("Pisquero", 9),
        ("Yana", 29), ("Callapa", 17), ("Taparo", 37), ("Yanaque", 21),
        ("Pucuro chacara", 3), ("Yanaqui chacara", 21),
        ("Sacina (mitimaes en Chuquisaca)", 14)], 1):
    add("aullaga_acho_1540", "Pärssinen 1992, Table 7", "6859-6875",
        "Aullaga/Quillaca (Collasuyu)", "aldea/llacta (parcialidad Aullaga)",
        i, nom, val,
        estructura="cacique Acho; 11 aldeas; orden de khipu",
        nota="suma 260; título de encomienda a Hernando de Aldana, 1540")

# Lupaca: censo khipu de 1567, cuadro de Julien reproducido por Pärssinen.
lup = [("Chucuito/Alasaya", 1233), ("Chucuito/Maasaya", 1384),
       ("Acora/Alasaya", 1221), ("Acora/Maasaya", 1207),
       ("Ilave/Ala&Maas", 1470), ("Juli/Alasaya-Chanbilla", 1438),
       ("Juli/Maasaya", 1804), ("Pomata/Alasaya", 1663),
       ("Pomata/Maasaya", 1341), ("Yunguyo/Ala&Maas", 1039),
       ("Zepita/Alasaya", 1112), ("Zepita/Maasaya", 866)]
for i, (nom, val) in enumerate(lup, 1):
    add("lupaca_sayas_1567", "Pärssinen 1992, cuadro de Julien", "6058-6070",
        "Lupaca/Chucuito", "saya (mitad de cabecera)", i, nom, val,
        estructura="7 cabeceras x 2 sayas (Ilave y Yunguyo combinadas = 12); Alasaya antes que Maasaya; Chucuito capital primero",
        nota="censo khipu leído a Diez de San Miguel 1567; total 15.778 aymaras")

# Cabeceras derivadas (suma de las sayas): no es una lista independiente.
cab = [("Chucuito", 2617), ("Acora", 2428), ("Ilave", 1470), ("Juli", 3242),
       ("Pomata", 3004), ("Yunguyo", 1039), ("Zepita", 1978)]
for i, (nom, val) in enumerate(cab, 1):
    add("lupaca_cabeceras_1567", "Pärssinen 1992 (derivado)", "5835-5837; 6058-6070",
        "Lupaca/Chucuito", "cabecera", i, nom, val,
        estructura="7 cabeceras; orden Chucuito, Acora, Ilave, Juli, Pomata, Yunguyo, Zepita (capital y ruta)",
        nota="suma de las sayas de lupaca_sayas_1567; no independiente")

# Chayanta: dos transcripciones del mismo khipu (Pärssinen & Kiviharju 2004).
chayanta = [
    ("Calapicana / Chayanta", 40, 42), ("Challachalla / Challa", 8, 8),
    ("Calache / Lehalacha", 15, 15), ("Chamarca / Mochamrca", 22, 46),
    ("Suaraui / Suairaui", 10, 10), ("Samincho / Simichoi", 60, 60),
    ("Ticongari / Ticongari", 60, 62), ("Amarcoia / Mosaca", 20, 20),
    ("Pichivisca / Pichiuisa", 49, 49), ("Puchivusca / Piutivisa", 26, 27),
    ("Lapilomaro / Piornaca", 16, 17), ("Caranga / Caranga", 20, 20)]
for i, (nom, v40, v48) in enumerate(chayanta, 1):
    add("chayanta_1540", "Pärssinen & Kiviharju 2004", "505-520",
        "Chayanta (Charcas)", "pueblo/estancia", i, nom, v40,
        estructura="título de encomienda a Gonzalo Pizarro 1540; orden de khipu",
        nota="suma 346; lista parcial de un total de 3.263")
    add("chayanta_1548", "Pärssinen & Kiviharju 2004", "505-520",
        "Chayanta (Charcas)", "pueblo/estancia", i, nom, v48,
        estructura="segunda transcripción del mismo khipu (título a Pedro de Hinojosa 1548)",
        nota="suma 376; misma secuencia de pueblos, cifras ±1-24")

# Collaguas: Yanque Collagua, Table 9 (suma exacta 2.163).
for i, (nom, val) in enumerate([
        ("Condori", 10), ("Tuti", 172), ("Canacoto", 80), ("Capa", 60),
        ("Chivara", 170), ("Chapica", 150), ("Canqui", 280), ("Malco", 108),
        ("Yumasca", 126), ("Cuparqui", 267), ("Cupas", 143), ("Yanqui", 234),
        ("Tula", 32), ("Coymo", 138), ("Vchuma", 133), ("Soro", 60)], 1):
    add("yanque_collagua_1540", "Pärssinen 1992, Table 9", "7125-7145",
        "Collaguas (Cuntisuyu)", "aldea/llacta (Yanque Collagua)", i, nom, val,
        estructura="Hanansaya + Hurinsaya; 16 aldeas; orden de la lista",
        nota="suma exacta 2.163")

# Cavana Conde, Table 8 (18 aldeas; la tabla suma 1.431 frente a 1.461/1.500).
for i, (nom, val) in enumerate([
        ("Caguana [Cavana]", 610), ("Oyomarca", 100), ("Tapa", 23),
        ("Pacalla", 30), ("Api", 20), ("Ayamar", 30), ("Quigua", 117),
        ("Quirque", 46), ("Talla", 56), ("Mataya", 50), ("Guanca", 72),
        ("Morco", 27), ("Llocalla", 20), ("Yura", 100), ("Turco", 20),
        ("Guacar", 53), ("Pituo", 40), ("Gualliquiman", 17)], 1):
    add("cavana_conde_1540", "Pärssinen 1992, Table 8", "7020-7055",
        "Collaguas (Cavana Conde)", "aldea/llacta", i, nom, val,
        estructura="Hanansaya + Hurinsaya; 18 aldeas; Cavana 610 primero",
        nota="suma de la tabla 1.431; el texto da 1.461 [1.500]: posible cifra omitida")

# ---------------------------------------------------------------- Costa central
# Guancayo (Chillón): 9 pachacas repartidas entre 5 señores.
guancayo = [("Mongoy", 2), ("Cancay", 1), ("Chuquitunga", 2),
            ("Chumbillan", 2), ("Antachunbi", 2)]
for i, (nom, val) in enumerate(guancayo, 1):
    add("guancayo_lords_1571", "Rostworowski, Costa peruana", "2601 (y 369-371)",
        "Chillón/Guancayo", "señor (pachacas por señor)", i, nom, val,
        estructura="5 señores; 9 pachacas = 1+4x2 (Mongoy 2, Cancay 1, Chuquitunga 2, Chumbillan 2, Antachunbi 2)",
        nota="900 hatun runa; 5 cestos de coca por pachaca = 45; visita Martínez de Rengifo 1571")

# Reconstrucción ideal: 9 pachacas x 100 = 900 (no observada unidad por unidad).
for i in range(1, 10):
    add("guancayo_pachacas_ideal", "Rostworowski (reconstrucción decimal)", "2601",
        "Chillón/Guancayo", "pachaca (reconstruida)", i, f"pachaca {i}", 100,
        estructura="9 pachacas x 100 = 900; reconstrucción, no lista observada",
        nota="CV=0 por construcción; sirve solo como modelo ideal")

# ---------------------------------------------------------------- Otras estructuras
# Pacajes: tres cabeceras (visita de Pérez de Esquibel, 1543).
for i, (nom, val) in enumerate([("Caquiaviri", 1200), ("Machaca", 1500),
                                ("Caquingora", 910)], 1):
    add("pacajes_cabeceras_1543", "Pärssinen 1992", "2559",
        "Pacajes", "cabecera", i, nom, val,
        estructura="3 cabeceras; Pizarro había calculado 1.200 / 1.600 / 1.700",
        nota="n=3; solo contexto")

# Collaguas: tres subprovincias (censo khipu 1540; Lari estimado).
for i, (nom, val) in enumerate([("Yanque Collaguas", 2163), ("Cavana", 1461),
                                ("Lari Collaguas", 2250)], 1):
    add("collaguas_subprovinces_1540", "Pärssinen 1992, nota 234", "4699",
        "Collaguas", "subprovincia", i, nom, val, completa=(i < 3),
        estructura="3 subprovincias, cada una con 2 mitades y 3 grupos de 3 patacas",
        nota="Lari estimado en 2.000-2.500; no usar en pruebas")

# Huayla: 12 guarangas (6 Hanan + 6 Hurin), solo tres con cifras.
for i in range(1, 13):
    add("huayla_12guarangas", "Pärssinen 1992", "4696; 5523",
        "Huayla (Chinchaysuyu)", "guaranga", i, f"guaranga {i}", None,
        completa=False,
        estructura="6 guarangas de Hanan Huayla + 6 de Hurin Huayla",
        nota="solo tres guarangas con cifras (750, 750 y 900); no usar en pruebas")

# Hunus comparativos (n=3 y n=2).
for i, (nom, val) in enumerate([("Hatun Jauja", 6000), ("Hanan Huanca", 9000),
                                ("Hurin Huanca", 12000)], 1):
    add("huanca_hunus", "Pärssinen 1992", "5523",
        "Huanca/Jauja", "hunu", i, nom, val,
        estructura="3 hunus; orden Hatun Jauja, Hanan, Hurin",
        nota="cifras aproximadas")
for i, (nom, val) in enumerate([("trabajadores", 12000), ("pescadores", 10000),
                                ("comerciantes", 6000)], 1):
    add("chincha_hunus", "Pärssinen 1992", "2522; 4584",
        "Chincha", "hunu", i, nom, val,
        estructura="3 hunus; 28.000 hogares",
        nota="cifras aproximadas")
for i, (nom, val) in enumerate([("hunu de Leimebamba y Cochabamba", 10000),
                                ("hunu restante", 10000)], 1):
    add("chachapoya_hunus", "Pärssinen 1992", "5232",
        "Chachapoya", "hunu", i, nom, val,
        estructura="2 hunus de casi 10.000 hogares cada uno",
        nota="cifras aproximadas")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["list_id", "fuente", "linea", "region",
                                      "nivel", "orden", "nombre", "cifra",
                                      "completa", "estructura", "nota"])
    w.writeheader()
    w.writerows(rows)

print("listas.csv:", len(rows), "filas;", len(set(r["list_id"] for r in rows)), "listas")
for lid in sorted(set(r["list_id"] for r in rows)):
    n = sum(1 for r in rows if r["list_id"] == lid)
    comp = all(r["completa"] == "si" for r in rows if r["list_id"] == lid)
    print(f"  {lid:28s} n={n:2d} completa={'si' if comp else 'no'}")
