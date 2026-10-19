# -*- coding: utf-8 -*-
"""ATAQUE 4: UR050 '3 zonas a alturas fijas' frente a cuerdas decimales normales
con 3 racimos de nudos.

Si cualquier cuerda decimal de 3 digitos coloca sus 3 racimos a alturas
relativas fijas, la prueba de zonas de UR050 no distingue nada. Se compara:
  - centros de banda y separacion (GMM k=3)
  - dBIC = BIC(1) - BIC(3), crudo y por observacion
  - tipos de nudo (S/L) de los 3 racimos
  - proporcion de cuerdas con 3 racimos y los 3 digitos != 0
"""
import re
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

rng = np.random.default_rng(20261018)
RAIZ = r"."
c = pd.read_csv(RAIZ + "/analisis/datos/cuerdas.csv", low_memory=False)
R = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([A-Z])\)")
c["L"] = pd.to_numeric(c.largo, errors="coerce")
c["val"] = pd.to_numeric(c.valor, errors="coerce")



def clusters(s):
    if not isinstance(s, str) or s == "":
        return []
    return [(t, float(pos), int(n)) for n, t, pos, d in R.findall(s)]


c["cl"] = c.nudos.map(clusters)
c["ncl"] = c.cl.map(len)
base = c[(c.ncl > 0) & (c.L > 0)].copy()
base["rels"] = [[pos / L for t, pos, n in cl] for cl, L in zip(base.cl, base.L)]


def analiza(g, k=3, minf=20):
    rows = [r for r in g.rels if len(r) == 3 and max(r) <= 1.05]
    if len(rows) < minf:
        return None
    X = np.array(rows).ravel().reshape(-1, 1)
    bic = {kk: GaussianMixture(kk, random_state=0, n_init=3).fit(X).bic(X) for kk in (1, k)}
    gm = GaussianMixture(k, random_state=0, n_init=3).fit(X)
    cen = np.sort(gm.means_.ravel())
    # separacion: hueco minimo entre centros / sd media intra
    sd = np.sqrt(np.mean([np.var(X[gm.predict(X) == j]) for j in range(k)]))
    gap = np.min(np.diff(cen)) / sd if sd > 0 else np.nan
    return dict(n=len(rows), dBIC=bic[1] - bic[k], dBIC_n=(bic[1] - bic[k]) / len(X),
                c1=cen[0], c2=cen[1], c3=cen[2], gap=gap)


# ---- UR050 ----
g50 = base[base.kfg == "UR050"]
r50 = analiza(g50)
print("UR050:", r50)
print("UR050 cuerdas con 3 racimos: %d de %d con nudos; tipos por racimo:"
      % (len(g50[g50.ncl == 3]), len(g50)))
tt = [tuple(t for t, _, _ in cl) for cl in g50.cl if len(cl) == 3]
from collections import Counter
print("  ", Counter(tt).most_common(5))
print("  digitos por racimo:", Counter(tuple(n for _, _, n in cl) for cl in g50.cl if len(cl) == 3).most_common(4))
print("  alguna vez hay un 0 como racimo:", any(n == 0 for cl in g50.cl for _, _, n in cl))

# ---- otros quipus con >=20 cuerdas de 3 racimos ----
res = []
for k, g in base.groupby("kfg"):
    if k == "UR050":
        continue
    r = analiza(g)
    if r:
        r["kfg"] = k
        # tipos de nudo
        tt = [tuple(t for t, _, _ in cl) for cl in g.cl if len(cl) == 3]
        r["pct_SLL"] = np.mean([t == ("S", "L", "L") or t == ("S", "S", "L") or t == ("L", "L", "L")
                                for t in tt])
        r["pct_allL"] = np.mean([t == ("L", "L", "L") for t in tt])
        res.append(r)
D = pd.DataFrame(res)
print("\nquipus control con >=20 cuerdas de 3 racimos:", len(D))
cols = ["n", "dBIC_n", "c1", "c2", "c3", "gap"]
print(D[cols].describe().round(2).to_string())
print("\npercentil de UR050 dentro de los controles:")
for col in ["dBIC_n", "gap"]:
    print(f"  {col}: UR050={r50[col]:.2f} percentil={100*np.mean(D[col] < r50[col]):.1f}")
print(f"  centros UR050=({r50['c1']:.2f},{r50['c2']:.2f},{r50['c3']:.2f}) "
      f"| controles mediana=({D.c1.median():.2f},{D.c2.median():.2f},{D.c3.median():.2f})")
print("\nTop 8 controles por dBIC_n:")
print(D.sort_values('dBIC_n', ascending=False)[['kfg'] + cols][:8].round(2).to_string(index=False))
D.to_csv(RAIZ + "/analisis/ds/n_rojo_formulario/zonas_control.csv", index=False)

# ---- cuantas cuerdas de 3 racimos tienen los 3 digitos != 0, en todo el corpus ----
tot = tres = allnz = 0
for k, g in c.groupby("kfg"):
    for cl in g.cl:
        if len(cl) == 3:
            tot += 1
            if all(n > 0 for _, _, n in cl):
                allnz += 1
print(f"\ncuerdas de 3 racimos en el corpus: {tot}; con 3 digitos >0: {allnz} ({allnz/tot:.3f})")
print(f"UR050: {int(np.sum([all(n>0 for _,_,n in cl) for cl in g50.cl if len(cl)==3]))}"
      f"/{int(np.sum([len(cl)==3 for cl in g50.cl]))}")
