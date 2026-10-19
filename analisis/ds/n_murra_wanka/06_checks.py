"""06_checks.py — Controles internos de la tabla: categorías, flujos, riqueza vs magnitud.
Salida: categorias_wanka.csv, salida_06.txt
"""
import os
import numpy as np, pandas as pd
from scipy import stats
os.chdir(os.path.dirname(os.path.abspath(__file__)))

cats = [
 (1,"I","Varones","personas","entregado"),
 (2,"I","Mujeres","personas","entregado"),
 (3,"II","Ovejas de la tierra (llamas)","cabezas","entregado"),
 (4,"II","Carneros para su comida","cabezas","entregado"),
 (5,"II","Ovejas, carneros, pacos","cabezas","rancheado"),
 (6,"III","Vestidos, lana, cumbi","piezas","entregado"),
 (7,"III","Frazadas","piezas","entregado"),
 (8,"III","Vestidos","piezas","rancheado"),
 (9,"IV","Maíz","hanegas","entregado"),
 (10,"IV","Quinua","hanegas","entregado"),
 (11,"IV","Papas","hanegas","entregado"),
 (12,"IV","Maíz","hanegas","rancheado"),
 (13,"IV","Quinua","hanegas","rancheado"),
 (14,"IV","Papas","hanegas","rancheado"),
 (15,"V","Sandalias de cuerda","pares","entregado"),
 (16,"V","Sandalias de agave","pares","entregado"),
 (17,"V","Sandalias de cuerda","pares","rancheado"),
 (18,"V","Sandalias de agave","pares","rancheado"),
 (19,"V","Soga gruesa","unidad","entregado"),
 (20,"V","Aderezos de caballo","juegos","entregado"),
 (21,"VI","Cántaros, ollas, tinajas","piezas","entregado"),
 (22,"VI","Vasijas pequeñas, mates, escudillas","piezas","entregado"),
 (23,"VI","Cántaros","piezas","rancheado"),
 (24,"VI","Mates","piezas","rancheado"),
 (25,"VII","Gallinas de Castilla","aves","entregado"),
 (26,"VII","Huevos","unidades","entregado"),
 (27,"VII","Perdices","aves","entregado"),
 (28,"VIII","Leña partida","cargas","entregado"),
 (29,"VIII","Astillas","cargas","entregado"),
 (30,"VIII","Carbón","cargas","entregado"),
 (31,"VIII","Hierba","cargas","entregado"),
 (32,"VIII","Paja","cargas","entregado"),
 (33,"IX","Chicha","cántaros","entregado"),
 (34,"IX","Toda fruta","cestas","entregado"),
 (35,"IX","Sal blanca","libras","entregado"),
 (36,"IX","Pescado","cestas de 1 libra","entregado"),
 (37,"X","Cargadores","personas","a la salida"),
 (38,"X","Yanaconas/sirvientes","personas","a la salida"),
 (39,"XI","Ovejas","cabezas","a la salida"),
 (40,"XI","Carneros","cabezas","a la salida"),
 (41,"XII","Maíz para el camino","hanegas","a la salida"),
 (42,"XII","Quinua para el camino","hanegas","a la salida"),
 (43,"XII","Papas para el camino","hanegas","a la salida"),
]
C = pd.DataFrame(cats, columns=["cuerda","categoria","etiqueta","unidad","flujo"])
C.to_csv("categorias_wanka.csv", index=False)

print("Categorías (clústeres):", C.categoria.nunique(), "| cuerdas:", len(C))
print(C.groupby("flujo").size().to_string())
print("\nCuerdas por categoría:")
print(C.groupby("categoria").size().to_string())

# riqueza vs magnitud por macro-grupo
d = pd.read_csv("wanka_celdas.csv")
orden = ["a","b","c","ch","d","e","f","g","h","i","j","k","l","ll","m","n","o","p","q"]
d["nv"] = d.valores.fillna("").apply(lambda s: len([x for x in str(s).split(";") if x]))
d["suma"] = d.valores.fillna("").apply(lambda s: sum(float(x) for x in str(s).split(";") if x))
print("\nRiqueza (n.º de cuerdas con dato) vs magnitud (log10 suma), por macro-grupo:")
for par, s in d.groupby("clusteres"):
    rho, pv = stats.spearmanr(s.nv, np.log10(s.suma.replace(0, np.nan).fillna(1)))
    print(f"  {par:10s} rho={rho:+.2f} p={pv:.3f} (n={len(s)})")

print("\nTendencia temporal de la riqueza:")
d["i"] = d.evento.map({e: i for i, e in enumerate(orden)})
rho, pv = stats.spearmanr(d.i, d.nv)
print(f"  Spearman(i_evento, n.º cuerdas con dato) = {rho:+.2f}, p={pv:.3f}, n={len(d)}")
