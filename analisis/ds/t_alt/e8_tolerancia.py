"""Calibracion de tolerancia para busqueda de sumas (version vectorizada).

Espacio de busqueda: para cada grupo de colgantes con >=2 cuerdas, todas las sumas
de tramos contiguos de >=2 colgantes, comparadas con el valor de cualquier colgante
del mismo quipu.
Por tolerancia T: tasa observada, tasa bajo nulo (permutar valores dentro del quipu),
exceso y falsos positivos esperados por quipu.
"""
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
d["v"] = pd.to_numeric(d.valor, errors="coerce").fillna(0)
g = pd.read_csv(RAIZ/"analisis/datos/grupos.csv", dtype=str, keep_default_na=False)
g["desde"] = pd.to_numeric(g.desde, errors="coerce"); g["hasta"] = pd.to_numeric(g.hasta, errors="coerce")
d["pnum"] = d.cuerda.str.extract(r"^p(\d+)$")[0]
raiz = d[d.pnum.notna()].copy(); raiz["pnum"] = raiz.pnum.astype(int)
Vq = {k: {int(i): float(x) for i, x in zip(grp.pnum, grp.v)} for k, grp in raiz.groupby("kfg")}
Gq = {k: grp for k, grp in g.groupby("kfg")}

def reldifs(Vq):
    """devuelve array de |target - suma|/suma para todas las comparaciones"""
    out = []
    for kfg, grp in Gq.items():
        vals = Vq.get(kfg)
        if not vals:
            continue
        tv = np.array(list(vals.values()), float)
        for _, r in grp.iterrows():
            idx = [i for i in range(int(r.desde), int(r.hasta)+1) if i in vals]
            if len(idx) < 2:
                continue
            v = np.array([vals[i] for i in idx], float)
            # sumas de tramos contiguos >=2
            cs = np.concatenate([[0], np.cumsum(v)])
            sums = [cs[b]-cs[a] for a in range(len(v)) for b in range(a+2, len(v)+1)]
            sums = np.array([s for s in sums if s > 0])
            if len(sums) == 0:
                continue
            out.append((np.abs(tv[:, None]-sums[None, :])/sums[None, :]).ravel())
    return np.concatenate(out)

rng = np.random.default_rng(20261018)
R = reldifs(Vq)
print("comparaciones candidatas:", len(R), " quipus:", len(Vq))
grid = [0, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10]
obs = [(R <= t).mean() for t in grid]
nul = []
for _ in range(100):
    Vn = {k: {i: x for i, x in zip(v.keys(), rng.permutation(list(v.values())))} for k, v in Vq.items()}
    Rn = reldifs(Vn)
    nul.append([(Rn <= t).mean() for t in grid])
nul = np.array(nul)
ncand = len(R)/len(Vq)
print("\nT           obs%    nulo%(sd)      exceso(pp)  FP_esperados/quipu  obs/exceso")
for i, t in enumerate(grid):
    o, n = obs[i], nul[:, i].mean()
    print(f"{t:<10.4g} {100*o:6.2f}   {100*n:6.2f} ({100*nul[:,i].std():.2f})  {100*(o-n):8.2f}   {n*ncand:8.3f}          {(o/n if n>0 else float('nan')):6.1f}")
print("\ncandidatas por quipu:", round(ncand, 1))
