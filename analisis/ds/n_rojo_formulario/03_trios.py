# -*- coding: utf-8 -*-
"""ATAQUE 3 (v2): el 'reparto 4:1:1' W-R-AB de UR053A-E frente a trios W-R-AB
de otros quipus.

Trios definidos por PATRON DE COLOR (como alinear.py): W seguida de R (rojo) y
AB como colgante siguiente o como subsidiaria de la roja.
Controles:
  - trios W-R-* de otros quipus
  - trios W-R-AB de otros quipus
  - todos los trios contiguos de otros quipus (reparto generico)
"""
import re
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu

rng = np.random.default_rng(20261018)
RAIZ = r"."
c = pd.read_csv(RAIZ + "/analisis/datos/cuerdas.csv", low_memory=False)
q = pd.read_csv(RAIZ + "/analisis/datos/quipus.csv")
prov = q.set_index("kfg").procedencia.astype(str).to_dict()


def norm(s):
    s = re.sub(r"\([^)]*\)", "", str(s))
    return "R" if s.startswith("R") else s


c["col"] = c.color.map(norm)
c["val"] = pd.to_numeric(c.valor, errors="coerce")
c = c.sort_values(["kfg", "orden"])


def trios_patron(g):
    """W seguida de R; AB = siguiente colgante o subsidiaria de la R."""
    sub = {r.padre: r.val for r in g[g.nivel == 1].itertuples() if r.col == "AB"}
    p = g[g.nivel == 0]
    out = []
    L = list(zip(p.cuerda, p.col, p.val))
    for i in range(len(L) - 1):
        if L[i][1] == "W" and L[i + 1][1] == "R":
            ab = sub.get(L[i + 1][0])
            if ab is None and i + 2 < len(L) and L[i + 2][1] == "AB":
                ab = L[i + 2][2]
            out.append((L[i][2], L[i + 1][2], ab))
    return out


T = {}
for k, g in c.groupby("kfg"):
    t = trios_patron(g)
    if t:
        T[k] = t

UR = ["UR053A", "UR053B", "UR053C", "UR053D", "UR053E"]


def reparto(tab):
    a = np.array([[x[0], x[1], x[2] if x[2] is not None else np.nan] for x in tab], float)
    ok = ~np.isnan(a).any(1)
    a = a[ok]
    s = a.sum(1)
    sh = a / s[:, None]
    return dict(n=len(a), primero_mayor=float(np.mean(a[:, 0] >= a[:, 1:].max(1))),
                share1=float(np.median(sh[:, 0])), share2=float(np.median(sh[:, 1])),
                share3=float(np.median(sh[:, 2])),
                cv1=float(np.std(sh[:, 0]) / np.mean(sh[:, 0])),
                mean_share1=float(np.mean(sh[:, 0])))


filas = []
for k in UR:
    if k in T:
        r = reparto(T[k]); r["grupo"] = k; filas.append(r)
        a = np.array([[x[0], x[1], x[2]] for x in T[k] if x[2] is not None], float)
        print(f"{k}: trios={len(T[k])} con AB={len(a)} W mayor={int(np.sum(a[:,0]>=a[:,1:].max(1)))}"
              f" R>AB={int(np.sum(a[:,1]>a[:,2]))}")
r = reparto([x for k in UR for x in T.get(k, [])]); r["grupo"] = "UR053 todas"; filas.append(r)

otros_wr = [x for k, t in T.items() if k not in UR for x in t]
otros_wrab = [x for x in otros_wr if x[2] is not None]
filas.append(dict(reparto(otros_wr), grupo="otros W-R-*"))
filas.append(dict(reparto(otros_wrab), grupo="otros W-R-AB"))
# todos los trios contiguos de otros quipus (control generico)
gen = []
for k, g in c[c.nivel == 0].groupby("kfg"):
    if k in UR:
        continue
    v = g.val.values.astype(float)
    if len(v) < 3:
        continue
    for i in range(len(v) - 2):
        if np.isfinite(v[i:i + 3]).all() and (v[i:i + 3] > 0).all():
            gen.append((v[i], v[i + 1], v[i + 2]))
a = np.array(gen)
sh = a / a.sum(1)[:, None]
filas.append(dict(grupo="trios contiguos genericos", n=len(a),
                  primero_mayor=float(np.mean(a[:, 0] >= a[:, 1:].max(1))),
                  share1=float(np.median(sh[:, 0])), share2=float(np.median(sh[:, 1])),
                  share3=float(np.median(sh[:, 2])),
                  cv1=float(np.std(sh[:, 0]) / np.mean(sh[:, 0])),
                  mean_share1=float(np.mean(sh[:, 0]))))
R = pd.DataFrame(filas)[["grupo", "n", "primero_mayor", "share1", "share2", "share3",
                          "mean_share1", "cv1"]]
print("\n=== Reparto de trios definidos por color")
print(R.round(3).to_string(index=False))
R.to_csv(RAIZ + "/analisis/ds/n_rojo_formulario/trios_reparto.csv", index=False)

# Fisher: W mayor en UR053 vs otros W-R-*
a1 = np.array([[x[0], x[1], x[2]] for k in UR for x in T[k] if x[2] is not None])
a2 = np.array([[x[0], x[1], x[2]] for x in otros_wrab])
tab = [[int(np.sum(a1[:, 0] >= a1[:, 1:].max(1))), len(a1)],
       [int(np.sum(a2[:, 0] >= a2[:, 1:].max(1))), len(a2)]]
print("\nFisher W mayor UR053 vs otros W-R-AB:", tab, "p=%.4f" % fisher_exact(tab)[1])
s1 = a1[:, 0] / a1.sum(1)
s2 = a2[:, 0] / a2.sum(1)
print("Mann-Whitney share1 UR053 vs otros W-R-AB: p=%.4f (medianas %.2f vs %.2f)" %
      (mannwhitneyu(s1, s2, alternative="greater")[1], np.median(s1), np.median(s2)))

# cuanto se aleja UR053 de la distribucion de share1 de otros trios W-R-* genericos
s3 = np.array([x[0] / (x[0] + x[1] + (x[2] or 0)) for x in otros_wr if x[2] is not None and x[2] > 0])
print("otros W-R-AB share1: mediana %.3f P90 %.3f | UR053 %.3f" %
      (np.median(s3), np.percentile(s3, 90), np.median(s1)))
