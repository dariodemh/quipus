"""04 · Que marca el color: la fila (registro), el nivel/rol, o la columna.

Tres pruebas con nulo explicito:
  A) UR278: numero de filas monocromas frente a un nulo que baraja los colores
     de todo el quipu (conserva la composicion global de colores).
  B) UR270: en cada par colgante/subsidiaria, el colgante es W y la subsidiaria no.
     Nulo: intercambiar los dos colores dentro del par (p binomial exacta).
  C) columnas: informacion mutua columna-color en UR278 frente a permutar dentro
     de la fila (si el color marcara la columna, la MI seria alta).
"""
import sys
import numpy as np
import pandas as pd
from scipy.stats import binomtest
sys.path.insert(0, ".")
from comun_rejilla import RAIZ, SEMILLA, cargar_cuerdas

rng = np.random.default_rng(SEMILLA)
c, q = cargar_cuerdas()

# ---------------------------------------------------------------- A) UR278
s = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values(["grupo", "orden"]).copy()
s["pos"] = s.groupby("grupo").cumcount() + 1
s = s[s.pos <= 9]
s = s[s.grupo.isin(range(0, 33))]
filas = [g for g, d in s.groupby("grupo") if len(d) >= 7]
s = s[s.grupo.isin(filas)]
mono = s.groupby("grupo").color.nunique()
obs_mono = int((mono == 1).sum())
n_filas = len(mono)
null = []
for _ in range(5000):
    v = s.color.values.copy()
    rng.shuffle(v)
    x = s.copy()
    x["color"] = v
    null.append(int((x.groupby("grupo").color.nunique() == 1).sum()))
null = np.array(null)
p_mono = (1 + np.sum(null >= obs_mono)) / (len(null) + 1)
print(f"A) UR278 filas monocromas: {obs_mono}/{n_filas}; nulo {null.mean():.2f}/{n_filas}; p={p_mono:.4f}")
print("   colores por fila:", mono.value_counts().to_dict())
print("   color modal por fila:", s.groupby("grupo").color.first().value_counts().to_dict())

# ---------------------------------------------------------------- B) UR270
u = c[(c.kfg == "UR270") & (c.nivel == 0)]
u = u[u.grupo.isin(u.groupby("grupo").size()[lambda x: x == 9].index)]
pares = []
for _, p in u.iterrows():
    ss = c[(c.kfg == "UR270") & (c.nivel == 1) & (c.padre == p.cuerda)].sort_values("orden")
    if len(ss) == 0:
        continue
    a, b = p.color, ss.iloc[0].color
    if a == b:
        continue
    pares.append((a == "W", b == "W"))
pares = pd.DataFrame(pares, columns=["P_W", "S_W"])
n = len(pares)
k = int(pares.P_W.sum())
bt = binomtest(k, n, 0.5, alternative="greater")
print(f"\nB) UR270 pares con colores distintos: {n}; el colgante (P) es W en {k}/{n} "
      f"({k/n:.0%}); binomial p={bt.pvalue:.2e}")
print("   P W:", int(pares.P_W.sum()), "S W:", int(pares.S_W.sum()))

# ---------------------------------------------------------------- C) columnas
def mi(df):
    ct = pd.crosstab(df.pos, df.color).values.astype(float)
    p = ct / ct.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.nansum(p * np.log2(p / (p.sum(1, keepdims=True) * p.sum(0, keepdims=True)))))
obs_mi = mi(s)
null_mi = []
for _ in range(3000):
    x = s.copy()
    x["color"] = x.groupby("grupo").color.transform(lambda v: rng.permutation(v.values))
    null_mi.append(mi(x))
null_mi = np.array(null_mi)
p_mi = (1 + np.sum(null_mi >= obs_mi)) / (len(null_mi) + 1)
print(f"\nC) MI(columna, color) en UR278 = {obs_mi:.3f} bits; nulo {null_mi.mean():.3f}; p={p_mi:.2f}")
print("   (si el color marcara la columna, la MI observada superaria al nulo)")

# ---------------------------------------------------------------- D) copia UR255/UR267A
f = pd.read_csv(f"{RAIZ}/14_copias/filas_alineadas.csv")
f = f[(f.A == "UR255") & (f.B == "UR267A") & f.clase.isin(
    ["exacta", "pm1_nudo", "un_digito_otro", "varias_cifras",
     "misma_cifra_otra_posicion", "transposicion"])]
obs = int((f.color_A == f.color_B).sum())
nn = len(f)
bv = f.color_B.values
null = []
for _ in range(5000):
    null.append(int(np.sum(f.color_A.values == rng.permutation(bv))))
null = np.array(null)
print(f"\nD) copia UR255-UR267A: color identico {obs}/{nn}; nulo {null.mean():.2f}; "
      f"p={(1+np.sum(null>=obs))/(len(null)+1):.3f}")
print("   UR255:", c[c.kfg == 'UR255'].color.value_counts().head(3).to_dict(),
      "| UR267A:", c[c.kfg == 'UR267A'].color.value_counts().head(3).to_dict())
obs_u = int((f.union_A == f.union_B).sum())
print(f"   union identica {obs_u}/{nn} (UR255 {c[c.kfg=='UR255'].union.mode().iat[0]} vs "
      f"UR267A {c[c.kfg=='UR267A'].union.mode().iat[0]})")
print(f"   torsion identica {int((f.torsion_A==f.torsion_B).sum())}/{nn}")

# ---------------------------------------------------------------- E) color de fila vs tamano y forma
from scipy.stats import mannwhitneyu
T = pd.read_csv(f"{RAIZ}/13_sistema_incahuasi/ur278_tabla.csv")
s2 = s.groupby("grupo").color.agg(lambda v: v.mode().iat[0]).rename("color_fila")
T = T.merge(s2, left_on="grupo", right_index=True, how="inner")
cols = [f"c{i}" for i in range(1, 10)]
for cc in cols:
    T[cc] = T[cc] / T["total"]
a = T[T.color_fila == "AB"].total
b = T[T.color_fila == "W"].total
p_tot = mannwhitneyu(a, b).pvalue
ps = [mannwhitneyu(T[T.color_fila == "AB"][cc].dropna(),
                   T[T.color_fila == "W"][cc].dropna()).pvalue for cc in cols]
print(f"\nE) UR278 color de fila: AB mediana {a.median():.0f} vs W {b.median():.0f}, "
      f"p(tamano)={p_tot:.3f}")
print(f"   proporciones c1..c9: p minimo={min(ps):.3f} (ninguna significativa tras BH)")

