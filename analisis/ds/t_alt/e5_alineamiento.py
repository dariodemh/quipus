"""Limpia el contraste KFG vs OKR: separa desacuerdo de VALOR (lectura de nudos)
de desacuerdo ESTRUCTURAL (orden / una cuerda de mas o de menos).
Estrategia: para cada quipu discrepante, probar desplazamientos -3..+3 y
comprobar si el desacuerdo se explica por un corrimiento de la secuencia.
Salida: kfg_vs_okr_cuerdas.csv (ya generado por e3b) + resumen.
"""
import sqlite3
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
P = pd.read_csv(AQUI/"kfg_vs_okr_cuerdas.csv")
P["dif"] = P.v.fillna(0) - P.v_kfg.fillna(0)

# reconstruir secuencia por quipu en orden
P = P.sort_values(["kfg", "oidx"])
filas = []
for kfg, g in P.groupby("kfg"):
    g = g.sort_values("oidx")
    a = g.v_kfg.values
    b = g.v.fillna(0).values
    base = (a == b).mean()
    best = (base, 0)
    for s in range(-3, 4):
        if s == 0:
            continue
        if s > 0:
            aa, bb = a[s:], b[:-s]
        else:
            aa, bb = a[:s], b[-s:]
        if len(aa) < max(3, 0.5*len(a)):
            continue
        f = (aa == bb).mean()
        if f > best[0]:
            best = (f, s)
    filas.append(dict(kfg=kfg, n=len(g), acuerda=base, mejor=best[0], shift=best[1]))
S = pd.DataFrame(filas)
S["estructural"] = (S.mejor >= 0.9) & (S.acuerda < 0.9)
print("quipus:", len(S))
print("acuerdo perfecto sin desplazar:", (S.acuerda == 1).sum())
print("quipus con desplazamiento que explica el desacuerdo:", S.estructural.sum())
print(S[S.estructural][["kfg", "n", "acuerda", "mejor", "shift"]].to_string(index=False))
res = S[~S.estructural]
print("\n-- tras excluir los estructurales --")
print("quipus:", len(res), " cuerdas:", res.n.sum())
print("tasa de desacuerdo por cuerda (media ponderada):",
      round(1 - (res.acuerda*res.n).sum()/res.n.sum(), 5))
print("quipus con algun desacuerdo de valor:", (res.acuerda < 1).sum())
print(res[res.acuerda < 1][["kfg", "n", "acuerda"]].sort_values("acuerda").to_string(index=False))
S.to_csv(AQUI/"alineamiento_por_quipu.csv", index=False)
