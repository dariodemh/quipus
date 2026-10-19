"""Dos preguntas:
 (a) ?El desacuerdo de valor depende de la direccion U, de la fuente o del tamano?
 (b) ?Cuando una transcripcion dice U, la otra sabe la direccion? -> mide el valor
     informativo real del 'U' (el otro transcriptor como oraculo).
Nulo: permutacion de la etiqueta dentro de cada quipu (regla 1 del brief).
"""
import sqlite3
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
P = pd.read_csv(AQUI/"kfg_vs_okr_cuerdas.csv").sort_values(["kfg", "oidx"])
P["v_okr"] = P.v.fillna(0)
P["dif"] = P.v_okr - P.v_kfg
P["fuente"] = P.kfg.str.extract(r"^([A-Z]+)")[0]
P["nU"] = P.nU.fillna(0); P["nk"] = P.nk.fillna(0)
P["fracU_okr"] = np.where(P.nk > 0, P.nU/P.nk, np.nan)

# direccion U en KFG por cuerda
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
import re
R = re.compile(r"\([\d.]+,([A-Z])\)")
def cu(r):
    m = R.findall(r)
    return (sum(x == "U" for x in m), len(m))
tmp = d.nudos.map(cu)
d["nU_kfg"] = [t[0] for t in tmp]; d["nk_kfg"] = [t[1] for t in tmp]
d["fracU_kfg"] = np.where(d.nk_kfg > 0, d.nU_kfg/d.nk_kfg, np.nan)
P = P.merge(d[["kfg", "cuerda", "nU_kfg", "nk_kfg", "fracU_kfg"]], on=["kfg", "cuerda"], how="left")

print("== (a) desacuerdo de valor por direccion U ==")
P["tieneU"] = P.fracU_kfg.fillna(0) > 0
for lab, g in P.groupby("tieneU"):
    print(f"  tieneU={lab}: n={len(g)} desacuerdo={g.dif.ne(0).mean():.4f} quipus={g.kfg.nunique()}")
# nulo: permutar dif!=0 dentro de quipu
rng = np.random.default_rng(20261018)
obs = P[P.tieneU].dif.ne(0).mean() - P[~P.tieneU].dif.ne(0).mean()
diffs = []
for _ in range(2000):
    Q = P.copy()
    Q["flag"] = Q.groupby("kfg").dif.transform(lambda s: rng.permutation(s.ne(0).values))
    diffs.append(Q[Q.tieneU].flag.mean() - Q[~Q.tieneU].flag.mean())
diffs = np.array(diffs)
print(f"  dif observada={obs:.4f}  p(perm 2 colas)={2*min((diffs>=obs).mean(),(diffs<=obs).mean()):.3f}")

print("\n== (a2) desacuerdo por fuente ==")
t = P.groupby("fuente").agg(n=("dif", "size"), desac=("dif", lambda s: s.ne(0).mean()),
                           quipus=("kfg", "nunique")).sort_values("n", ascending=False)
print(t.head(8).round(4).to_string())

print("\n== (a3) desacuerdo vs tamano del valor ==")
P["bin"] = pd.cut(P.v_kfg, [-1, 0, 9, 99, 999, 1e9], labels=["0", "1-9", "10-99", "100-999", ">=1000"])
print(P.groupby("bin", observed=True).agg(n=("dif", "size"), desac=("dif", lambda s: s.ne(0).mean())).round(4).to_string())

print("\n== (b) ?cuando KFG dice U, OKR sabe? ==")
amb = P[(P.nk_kfg > 0) & (P.nk > 0)].copy()
print("cuerdas comparables:", len(amb))
print("KFG todas-U:", (amb.fracU_kfg == 1).sum(), " OKR todas-U:", (amb.fracU_okr == 1).sum())
amb["kfg_U_okr_sabe"] = (amb.fracU_kfg == 1) & (amb.fracU_okr == 0)
amb["okr_U_kfg_sabe"] = (amb.fracU_okr == 1) & (amb.fracU_kfg == 0)
print("KFG 100% U pero OKR 0% U:", amb.kfg_U_okr_sabe.sum(),
      f"({100*amb.kfg_U_okr_sabe.mean():.2f}% de las comparables)")
print("OKR 100% U pero KFG 0% U:", amb.okr_U_kfg_sabe.sum(),
      f"({100*amb.okr_U_kfg_sabe.mean():.2f}%)")
print("ambas 100% U:", ((amb.fracU_kfg == 1) & (amb.fracU_okr == 1)).sum())
print("KFG 100% U por fuente:")
print(amb[amb.fracU_kfg == 1].groupby("fuente").size().to_string())
