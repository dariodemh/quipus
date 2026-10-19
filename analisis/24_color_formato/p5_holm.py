"""Holm sobre la familia congelada de 12 pruebas principales (diseno.md §7). Salida: holm.csv"""
import pandas as pd

import comun24 as C

r1 = pd.read_csv(C.AQUI / "p1_resumen.csv").fillna({"sub": "todo"})
g2 = pd.read_csv(C.AQUI / "p2_global.csv")
p2 = pd.read_csv(C.AQUI / "p2_preferido.csv")
t3 = pd.read_csv(C.AQUI / "p3_pruebas.csv")


def f1(fam, col, sub="todo"):
    return float(r1[(r1.familia == fam) & (r1["sub"] == sub)][col].iloc[0])


def f2(t, col):
    return float(g2[(g2.tipo == t) & (g2.reg == "todos")][col].iloc[0])


P = [
    ("P1 Incahuasi sumas: M vs N1", f1("F2_incahuasi_suma", "p_M_N1")),
    ("P1 Incahuasi sumas: NMI vs N1", f1("F2_incahuasi_suma", "p_NMI_N1")),
    ("P1 Puruchuco: M vs N1", f1("F3_puruchuco", "p_M_N1")),
    ("P1 copias mismo registrador: M vs N1", f1("F1_copia_mismo_reg", "p_M_N1")),
    ("P2 T1 total: D vs NG", f2("T1", "p_NG")),
    ("P2 T1 total: D vs NP", f2("T1", "p_NP")),
    ("P2 T3 cabecera-máximo: D vs NG", f2("T3", "p_NG")),
    ("P2 T4 en blanco: D vs NG", f2("T4", "p_NG")),
    ("P2 T5 marcadora: D vs NG", f2("T5", "p_NG")),
    ("P2 T7 subsidiaria = padre (más que el nulo)", f2("T7", "p_igual_mayor")),
    ("P2 preferencia W de T1 entre quipus", float(p2[p2.tipo == "T1"].p_W.iloc[0])),
    ("P3 alfabeto rarefactado ~ registrador", float(t3[t3.prueba == "alf_rare ~ registrador"].p.iloc[0])),
]
H = pd.DataFrame(P, columns=["prueba", "p"])
H["holm"] = C.holm(H.p.values)
H.to_csv(C.AQUI / "holm.csv", index=False)
print(H.to_string())
