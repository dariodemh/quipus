"""Calibracion de tolerancia en el espacio de busqueda REALISTA (vectorizado):
  para cada grupo de colgantes (n>=3), cada colgante del grupo como posible
  'cuerda suma' y cada tramo contiguo de >=2 OTROS colgantes del mismo grupo.
Observado vs nulo (permutar valores dentro del quipu) para una rejilla de tolerancias.
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
Vq = {k: {int(i): float(x) for i, x in zip(gr.pnum, gr.v)} for k, gr in raiz.groupby("kfg")}

def bloques(idx, Vq):
    """para cada grupo devuelve lista de arrays n x m de |target-suma|/suma"""
    out = []
    for kfg, grp in g.groupby("kfg"):
        vals = Vq.get(kfg)
        if not vals:
            continue
        for _, r in grp.iterrows():
            ii = [i for i in range(int(r.desde), int(r.hasta)+1) if i in vals]
            if len(ii) < 3:
                continue
            v = np.array([vals[i] for i in ii], float)
            n = len(v)
            cs = np.concatenate([[0.0], np.cumsum(v)])
            S, inside = [], []
            for a in range(n):
                for b in range(a+2, n+1):
                    s = cs[b]-cs[a]
                    if s > 0:
                        S.append(s); inside.append((a, b))
            if not S:
                continue
            S = np.array(S); M = np.zeros((n, len(S)), bool)
            for k2, (a, b) in enumerate(inside):
                M[a:b, k2] = True
            R = np.abs(v[:, None]-S[None, :])/S[None, :]
            out.append(R[~M])
    return out

rng = np.random.default_rng(20261018)
B = bloques(None, Vq)
R = np.concatenate(B)
print("comparaciones (espacio restringido):", len(R), " grupos:", len(B))
grid = [0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10]
obs = [(R <= t).mean() for t in grid]
nul = []
for _ in range(200):
    Vn = {k: {i: x for i, x in zip(v.keys(), rng.permutation(list(v.values())))} for k, v in Vq.items()}
    Rn = np.concatenate(bloques(None, Vn))
    nul.append([(Rn <= t).mean() for t in grid])
nul = np.array(nul)
print("candidatas por grupo:", round(len(R)/len(B), 1))
print("\nT        obs%    nulo%(sd)     exceso(pp)  FP_esp/grupo  obs/nulo")
for i, t in enumerate(grid):
    o, n = obs[i], nul[:, i].mean()
    print(f"{t:<8.3g} {100*o:6.2f}  {100*n:6.2f} ({100*nul[:,i].std():.2f})  {100*(o-n):7.2f}     {n*len(R)/len(B):8.3f}      {(o/n if n>0 else np.nan):5.2f}")
