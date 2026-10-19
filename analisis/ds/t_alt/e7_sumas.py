"""Relaciones de suma potenciales (madre = suma de sus hijas) y calibracion de
tolerancia: tasa de acierto observada frente a nulo por permutacion de la madre
dentro del quipu, para una rejilla de tolerancias.
"""
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
d["v"] = pd.to_numeric(d.valor, errors="coerce").fillna(0)
d["nivel"] = pd.to_numeric(d.nivel, errors="coerce")
hijos = {p: g for p, g in d[d.padre != ""].groupby("padre")}
by = d.set_index(["kfg", "cuerda"])

filas = []
for p, g in hijos.items():
    kfg = g.kfg.iloc[0]
    if (kfg, p) not in by.index:
        continue
    par = by.loc[(kfg, p)]
    if isinstance(par, pd.DataFrame):
        par = par.iloc[0]
    if len(g) < 2:
        continue
    s = g.v.sum()
    filas.append(dict(kfg=kfg, madre=p, valor=float(par.v), suma=float(s),
                      k=len(g), nivel=par.nivel))
S = pd.DataFrame(filas)
S = S[S.suma > 0].copy()
S["dif"] = S.valor - S.suma
S["reldif"] = S.dif.abs()/S.suma
print("relaciones madre-hijas con >=2 hijas y suma>0:", len(S), "quipus:", S.kfg.nunique())
print("k (n hijas) distribucion:", S.k.value_counts().sort_index().head(8).to_dict())

# --- nulo: permutar el valor de la madre entre cuerdas del mismo quipu
rng = np.random.default_rng(20261018)
vals = d.groupby("kfg").v.apply(list).to_dict()
def nulo(nrep=200):
    out = []
    for _ in range(nrep):
        r = S.copy()
        r["valor"] = [rng.choice(vals[k]) for k in r.kfg]
        out.append(r)
    return out

grid = [0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10]
print("\nT        obs%    nulo%   exceso  (nulo=200 permutaciones, media)")
obs = [(S.reldif <= t).mean() for t in grid]
N = nulo(200)
null = [np.mean([(r.reldif <= t).mean() for r in N]) for t in grid]
for t, o, n in zip(grid, obs, null):
    print(f"{t:<8.3f} {100*o:6.2f} {100*n:6.2f} {100*(o-n):7.2f}")
print("\nexactas (dif==0):", (S.dif == 0).sum(), f"({100*(S.dif==0).mean():.2f}%)")
print("nulo exacto:", np.mean([(r.dif == 0).mean() for r in N]).round(4))
S.to_csv(AQUI/"sumas_candidatas.csv", index=False)
