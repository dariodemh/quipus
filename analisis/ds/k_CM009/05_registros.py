# -*- coding: utf-8 -*-
"""CM009: descomposición en registros (ciclos de color de 4 cuerdas) y resumen de tests."""
import pandas as pd, numpy as np
from scipy import stats

q = pd.read_csv("analisis/ds/k_CM009/cm009_cuerdas.csv").sort_values("cord_id").reset_index(drop=True)
v = q.numeric_value.to_numpy(int); col = q.color.to_numpy(); n = len(v)

# registros de 4 cuerdas desde p6 (ciclo de color W,AB,GG,W:KB)
start = 5
recs = []
for r in range((n - start) // 4):
    s = start + 4 * r
    recs.append(dict(rec=r + 1, pos_inicio=s + 1, W=v[s], AB=v[s + 1], GG=v[s + 2], W_KB=v[s + 3],
                     cols="".join(col[s:s + 4]), suma=v[s:s + 4].sum()))
R = pd.DataFrame(recs)
print("cabecera p1-p5:", list(zip(q.cord_name[:5], col[:5], v[:5])))
print("n registros de 4:", len(R), "| cuerdas usadas:", 4 * len(R), "+5 cabecera =", 4 * len(R) + 5)
print(R.to_string(index=False))
R.to_csv("analisis/ds/k_CM009/cm009_registros.csv", index=False)

# ¿W = AB+GG+W:KB ?
R["dif"] = R.W - (R.AB + R.GG + R.W_KB)
print("\n¿W = AB+GG+W:KB? coincidencias exactas:", int((R.dif == 0).sum()), "de", len(R))
print("¿W:KB = AB+GG?", int((R.W_KB == R.AB + R.GG).sum()))

# estructura de 5 registros x 3 super-grupos
print("\nsuper-grupos (5 registros c/u):")
for g in range(3):
    sub = R.iloc[5 * g:5 * g + 5]
    print(f"  SG{g+1}: W={list(sub.W)} AB={list(sub.AB)} GG={list(sub.GG)} W:KB={list(sub.W_KB)}")

# correlaciones entre columnas
print("\nSpearman entre columnas de registro:")
for a, b in [("W", "AB"), ("W", "GG"), ("W", "W_KB"), ("AB", "GG")]:
    rho, p = stats.spearmanr(R[a], R[b])
    print(f"  {a}-{b}: rho={rho:.3f} p={p:.3f}")

# ---- tabla de tests globales con Holm ----
tests = [
    ("color lag4", 0.934, 0.0010),
    ("valor lag20 (nulo color-preservado)", 0.400, 0.0010),
    ("patrón nudo lag20", 0.622, 0.0010),
    ("sumas contiguas", None, 0.3317),
    ("valores repetidos", None, 1.0000),
    ("valor lag4 (nulo color-pres.)", 0.213, 0.1249),
]
print("\ntests (p brutos ya computados en scripts previos):")
print(pd.DataFrame(tests, columns=["test", "obs", "p"]).to_string(index=False))
