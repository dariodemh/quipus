# -*- coding: utf-8 -*-
"""
02 · ¿Es el 9 un rasgo administrativo universal o local?
Anchos de grupo (numero de colgantes por grupo) en el corpus KFG; comparacion
de la tabla de 9 columnas de UR278 con el resto y con los quipus tabulares.
Unidad de prueba: el quipu (permutacion de etiquetas entre quipus).
Salidas: resultados_02.txt, anchos_grupo.csv
"""
import numpy as np, pandas as pd, os
from scipy import stats
rng = np.random.default_rng(20261018)
BASE = os.path.dirname(os.path.abspath(__file__))
DAT = os.path.join(BASE, "..", "..", "datos")

cu = pd.read_csv(os.path.join(DAT, "cuerdas.csv"), usecols=["kfg", "grupo", "nivel"])
cu = cu[(cu.nivel == 0) & cu.grupo.notna()].copy()
cu["grupo"] = cu.grupo.astype(int)
anchos = cu.groupby(["kfg", "grupo"]).size().rename("ancho").reset_index()
anchos.to_csv(os.path.join(BASE, "anchos_grupo.csv"), index=False)
print("Grupos:", len(anchos), "| quipus:", anchos.kfg.nunique(), "| ancho medio:", round(anchos.ancho.mean(), 2))

# Distribucion de anchos 1-16
d = anchos.ancho.value_counts().sort_index()
print("\nAncho : grupos")
for w in range(1, 17):
    print(f"{w:5d} : {int(d.get(w,0)):5d}")
tot = len(anchos)
p9 = (anchos.ancho == 9).mean()
print(f"\nProporcion de grupos con ancho 9: {p9:.4f} ({int((anchos.ancho==9).sum())}/{tot})")
vec = (d.get(8, 0) + d.get(10, 0)) / 2
print(f"Ratio 9 / media(8,10): {(d.get(9,0)/vec):.2f}" if vec else "sin vecinos")

# Anchos por quipu
per = anchos.groupby("kfg").agg(n_grupos=("grupo", "size"), ancho_med=("ancho", "median"),
                                ancho_min=("ancho", "min"), ancho_max=("ancho", "max"))
per["p9"] = anchos.assign(is9=anchos.ancho.eq(9)).groupby("kfg").is9.mean()
print("\nQuipus con >=1 grupo de ancho 9:", int((per.ancho_max >= 9).sum()),
      "| con TODOS sus grupos de ancho 9:", int(((per.ancho_min == 9) & (per.ancho_max == 9)).sum()),
      "| con >=80% de grupos de 9:", int((per.p9 >= 0.8).sum()))

# UR278 / UR270
for k in ["UR278", "UR270", "UR269", "UR273A", "UR266"]:
    a = anchos[anchos.kfg == k]
    if len(a):
        print(f"{k}: {len(a)} grupos, anchos {sorted(a.ancho.tolist())[:12]}{'...' if len(a)>12 else ''}")
u = anchos[anchos.kfg == "UR278"]
print("UR278 grupos con >=7 colgantes:", sorted(u[u.ancho >= 7].ancho.tolist()))
print("UR278 anchos:", u.ancho.value_counts().sort_index().to_dict())

# P(33 grupos de 9 | distribucion del corpus)
p_all9 = p9 ** 33
print(f"\nP(33/33 grupos de ancho 9 bajo la distribucion del corpus) = {p_all9:.2e}")

# Tabulares (177) frente al resto, prueba por quipu
tab = pd.read_csv(os.path.join(BASE, "..", "..", "10_tablas", "t1_por_quipu.csv"))
col = tab.columns[0]
tabq = set(tab[col].astype(str))
per = per.reset_index()
per["tabular"] = per.kfg.astype(str).isin(tabq)
obs = per.loc[per.tabular, "p9"].mean() - per.loc[~per.tabular, "p9"].mean()
perm = []
lab = per.tabular.to_numpy(); y = per.p9.to_numpy()
for _ in range(20000):
    sh = rng.permutation(lab)
    perm.append(y[sh].mean() - y[~sh].mean())
p = (1 + np.sum(np.abs(perm) >= abs(obs))) / 20001
print(f"Tabulares n={per.tabular.sum()} vs resto n={(~per.tabular).sum()}: "
      f"proporcion media de grupos de 9 {per.loc[per.tabular,'p9'].mean():.3f} vs {per.loc[~per.tabular,'p9'].mean():.3f}; "
      f"dif {obs:+.3f}, p={p:.4f}")

# Incahuasi dentro/fuera de tabulares
print("UR278 en tabulares:", "UR278" in tabq, "| UR270:", "UR270" in tabq)

# Ancho de tabla (K) en los 177 tabulares: ¿es 9 el ancho tipico?
print("\nAnchos de tabla K en tabulares (177):")
print(tab.K.value_counts().sort_index().head(15).to_dict())
print("K mediana:", tab.K.median(), "| K=9:", int((tab.K == 9).sum()), "de", len(tab))
