"""Cobertura potencial de cada regla estructural (sin mirar valores ocultos)."""
import pandas as pd, numpy as np
from pathlib import Path
D = Path(__file__).resolve().parents[2] / "datos"
c = pd.read_csv(D / "cuerdas.csv", dtype={"kfg": str, "cuerda": str, "padre": str, "nudos": str})
q = pd.read_csv(D / "quipus.csv", dtype={"kfg": str})
c["nudos"] = c["nudos"].fillna("")
c["pres"] = ~((c["valor"] == 0) & (c["nudos"].str.strip() == ""))

# hijos
kids = c[c.nivel > 0].groupby(["kfg", "padre"]).agg(n=("cuerda", "size"), npres=("pres", "sum")).reset_index()
print("padres con hijas:", len(kids), " con >=2 hijas presentes:", (kids.npres >= 2).sum(),
      " con 1 hija presente:", (kids.npres == 1).sum())
print("cuerdas hijo con >=1 hermana:", int(kids[kids.npres >= 2].npres.sum()))

# grupos: nivel 0 por grupo
l0 = c[c.nivel == 0]
gg = l0.groupby(["kfg", "grupo"]).agg(n0=("cuerda", "size"), n0pres=("pres", "sum")).reset_index()
print("\ngrupos:", len(gg), " tamano 0 pres distribution:", gg.n0pres.value_counts().sort_index().head(8).to_dict())
print("grupos con 1 colgante solo:", (gg.n0 == 1).sum(), " quipus:", gg[gg.n0 == 1].kfg.nunique())

# T
print("\nT cords:", (c.union == "T").sum(), "quipus:", c[c.union == "T"].kfg.nunique())

# pares misma procedencia con estructura de grupos identica
qmap = q.set_index("kfg").procedencia.fillna("Unknown").to_dict()
sig = gg.groupby("kfg").n0.apply(lambda s: tuple(sorted(s.tolist()))).to_dict()
# grupos ordenados por indice
sig2 = {k: tuple(v.sort_values("grupo").n0.tolist()) for k, v in gg.groupby("kfg")}
from collections import defaultdict
byp = defaultdict(list)
for k, s in sig2.items():
    byp[qmap.get(k, "Unknown")].append((k, s))
print("\nprocedencias no Unknown:", sum(1 for p in byp if p != "Unknown"))
npair = nident = 0
for p, L in byp.items():
    if p == "Unknown": continue
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            npair += 1
            if L[i][1] == L[j][1] and len(L[i][1]) >= 3:
                nident += 1
print("pares misma proc:", npair, " con firma de grupos identica (>=3 grupos):", nident)

# cuantos quipus tienen gemelo estructural
from collections import Counter
cnt = Counter()
for p, L in byp.items():
    if p == "Unknown": continue
    cc = Counter(s for _, s in L if len(s) >= 3)
    for k, s in L:
        if cc[s] > 1: cnt[k] += 1
print("quipus con >=1 gemelo estructural:", len(cnt))
print("pares con >=20 colgantes:", sum(1 for k in cnt if sig2[k] and sum(sig2[k]) >= 20))
