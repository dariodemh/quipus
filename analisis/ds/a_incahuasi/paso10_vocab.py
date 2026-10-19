# -*- coding: utf-8 -*-
"""Paso 10: vocabulario de valores compartido (Jaccard de conjuntos de valores)
observado vs nulo global (valores redibujados del pool global, mismos tamanos)."""
import pandas as pd, numpy as np, itertools
RAIZ = "./"
rng = np.random.default_rng(0); NPERM = 500
q = pd.read_csv(RAIZ + "analisis/datos/quipus.csv")
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
inc = q[q["procedencia"] == "Incahuasi"]; ids = sorted(inc["kfg"].tolist())
ci = c[c["kfg"].isin(ids)].copy()
ci["sin_nudos"] = ci["valor"].eq(0) & (ci["nudos"].isna() | ci["nudos"].astype(str).str.strip().isin(["", "nan"]))
vals = {k: ci[(ci.kfg == k) & ~ci.sin_nudos]["valor"].astype(int).tolist() for k in ids}
allv = [v for k in ids for v in vals[k]]
def jac(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A | B) if (A | B) else 0
pairs = [p for p in itertools.combinations(ids, 2)]
obs = np.array([jac(vals[a], vals[b]) for a, b in pairs])
print(f"Jaccard observado: media={obs.mean():.3f} p90={np.percentile(obs,90):.3f} max={obs.max():.3f}")
i = int(np.argmax(obs)); print("  par mas parecido:", pairs[i], round(obs[i], 3))
# nulo global
nullmean = []
for _ in range(200):
    pool = list(allv); rng.shuffle(pool); idx = 0; nv = {}
    for k in ids:
        nv[k] = pool[idx:idx + len(vals[k])]; idx += len(vals[k])
    m = np.mean([jac(nv[a], nv[b]) for a, b in pairs]); nullmean.append(m)
nullmean = np.array(nullmean)
print(f"nulo global Jaccard medio={nullmean.mean():.3f}  (obs-{nullmean.mean():+.3f}); "
      f"p(obs_medio<=nulo)={(1+(nullmean>=obs.mean()).sum())/(1+len(nullmean)):.4f}")
# pares con Jaccard alto
for thr in (0.4, 0.5, 0.6):
    print(f"  pares Jaccard>={thr}: {(obs>=thr).sum()}")
