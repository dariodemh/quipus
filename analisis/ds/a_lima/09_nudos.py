# -*- coding: utf-8 -*-
"""Replica de Clindaniel (2019): direccion de NUDO por sitio.
Armatambo seria el outlier (S predomina). Test binomial."""
import pandas as pd, numpy as np, re
from scipy.stats import binomtest
BASE = r"."
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
c = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
cc = c[c["kfg"].isin(sel["kfg"])].copy()
site = dict(zip(sel["kfg"], sel["sitio"]))
cc["sitio"] = cc["kfg"].map(site)

PAT = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU?])\)")
rows = []
for _, r in cc.iterrows():
    s = r["nudos"]
    if not isinstance(s, str):
        continue
    for m in PAT.finditer(s):
        nk = int(m.group(1)); typ = m.group(2); dr = m.group(4)
        rows.append((r["kfg"], r["sitio"], nk, typ, dr))
K = pd.DataFrame(rows, columns=["kfg", "sitio", "n", "tipo", "dir"])
print("Nudos parseados:", len(K), "| nudos totales:", K["n"].sum())
print("Tipos:", K["tipo"].value_counts().head(8).to_dict())
print("\nPor sitio (nudos individuales, todas las direcciones):")
t = K[K["dir"].isin(["S", "Z"])].groupby(["sitio", "dir"])["n"].sum().unstack(fill_value=0)
t["fracS"] = (t["S"] / (t["S"] + t["Z"])).round(3)
t["p_binom_S0.5"] = [binomtest(int(r["S"]), int(r["S"] + r["Z"]), 0.5).pvalue if (r["S"]+r["Z"]) else np.nan for _, r in t.iterrows()]
print(t.to_string())

# solo nudos simples S/L (los de valor)
print("\nSolo nudos simples+largos (tipos con letras S,L,E):")
t2 = K[K["dir"].isin(["S", "Z"])].groupby(["sitio", "dir"])["n"].sum().unstack(fill_value=0)
# Armatambo inversion: agrupar Armatambo vs resto
arm = K[(K["sitio"] == "Armatambo") & K["dir"].isin(["S", "Z"])]
res = K[(K["sitio"] != "Armatambo") & K["dir"].isin(["S", "Z"])]
for name, d in [("Armatambo", arm), ("Resto Lima", res)]:
    S, Z = d[d["dir"] == "S"]["n"].sum(), d[d["dir"] == "Z"]["n"].sum()
    print(f"  {name:14s} S={S} Z={Z} fracS={S/(S+Z):.3f} p(binom vs0.5)={binomtest(int(S),int(S+Z),0.5).pvalue:.2e}")

# por quipu Armatambo
print("\nArmatambo por quipu (S vs Z):")
for k in sorted(set(K[K["sitio"] == "Armatambo"]["kfg"])):
    d = K[(K["kfg"] == k) & K["dir"].isin(["S", "Z"])]
    S, Z = d[d["dir"] == "S"]["n"].sum(), d[d["dir"] == "Z"]["n"].sum()
    print(f"  {k:8s} S={S:4d} Z={Z:4d} fracS={S/(S+Z) if S+Z else 0:.3f}")

# control: cord torsion (hiio) por sitio
print("\nTorsion del CORDON por sitio:")
tt = cc[cc["torsion"].isin(["S", "Z"])].groupby(["sitio", "torsion"]).size().unstack(fill_value=0)
print(tt.to_string())
K.to_csv(BASE + r"\analisis\ds\a_lima\nudos_por_sitio.csv", index=False)
