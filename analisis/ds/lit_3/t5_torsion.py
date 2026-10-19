"""T5. Hyland (2017) y Clindaniel (2019): torsion S/Z y diversidad de
combinaciones color+torsion.

Afirmaciones:
  A) En khipus contables de algodon la torsion es ~97% S; en los khipus
     de Collata es 58% S / 42% Z (Hyland 2017).
  B) Los khipus de Collata tienen 95 combinaciones de color/fibra/torsion
     para 487 colgantes, "notablemente mas" que los khipus contables.
     Los Collata no estan en KFG/OKR: solo se puede evaluar la parte
     comparativa (¿es 95/487 exceptional en el corpus?).
  C) La torsion Z marcaria khipus no contables / narrativos.

Se trabaja a nivel de quipu: IC por bootstrap de quipus, correlaciones
de Spearman con permutacion y BH-FDR.
"""
import numpy as np
import pandas as pd
from scipy import stats
from comun import cargar, RNG, bh_fdr

c, q, _ = cargar()

t = c[c.torsion.isin(["S", "Z"])]
print("cuerdas con torsion S/Z:", len(t), "de", len(c))
print("S:", (t.torsion == "S").sum(), "Z:", (t.torsion == "Z").sum(),
      "| %S =", round((t.torsion == "S").mean() * 100, 2))

# IC por bootstrap de quipus
filas = []
for k, g in t.groupby("kfg"):
    filas.append((k, (g.torsion == "S").sum(), (g.torsion == "Z").sum()))
d = pd.DataFrame(filas, columns=["kfg", "S", "Z"])
d["n"] = d.S + d.Z
B = 5000
vals = []
n = len(d)
S = d.S.to_numpy(float)
N = d.n.to_numpy(float)
for _ in range(B):
    idx = RNG.integers(0, n, n)
    vals.append(S[idx].sum() / N[idx].sum())
lo, hi = np.percentile(vals, [2.5, 97.5])
print(f"IC 95% bootstrap por quipu del %S: [{lo*100:.2f}, {hi*100:.2f}]")
print("khipus con torsion S/Z:", len(d))
print("todos S:", (d.Z == 0).sum(), "| todos Z:", (d.S == 0).sum(),
      "| mixtos:", ((d.S > 0) & (d.Z > 0)).sum())

print("\n=== C. ¿La torsion Z se asocia a khipus no contables? ===")
# Variables por quipu: n colores, fraccion de colgantes sin nudos, valor maximo
m = []
for k, g in c.groupby("kfg"):
    tt = g[g.torsion.isin(["S", "Z"])]
    if len(tt) < 10:
        continue
    p = g[g.nivel == 0]
    m.append({
        "kfg": k,
        "fZ": (tt.torsion == "Z").mean(),
        "ncol": g.color.nunique(),
        "frac_sin": (p.nudos.isna()).mean() if len(p) else np.nan,
        "maxv": p.valor.max() if len(p) else np.nan,
        "npend": len(p),
    })
m = pd.DataFrame(m).dropna()
print("khipus analizados (>=10 cuerdas con torsion):", len(m))
ps = []
for var in ["ncol", "frac_sin", "maxv"]:
    rho, p = stats.spearmanr(m.fZ, m[var])
    ps.append(p)
    print(f"  Spearman fZ ~ {var:8s}: rho={rho:+.3f} p={p:.4f}")
qvals = bh_fdr(ps)
print("  q BH-FDR:", [round(v, 4) for v in qvals])

# Comparacion de grupos extremos
print("\nMedias por cuartil de fZ:")
m["q"] = pd.cut(m.fZ, [-0.01, 0.001, 0.25, 0.75, 1.01],
                labels=["0", "(0,.25]", "(.25,.75]", "(.75,1]"])
print(m.groupby("q", observed=True).agg(n=("kfg", "size"), ncol=("ncol", "mean"),
                                        frac_sin=("frac_sin", "mean"),
                                        maxv=("maxv", "median")).round(2).to_string())

# Bootstrap de la diferencia de ncol entre khipus con fZ>0 y fZ=0
a = m[m.fZ > 0].ncol.to_numpy()
b = m[m.fZ == 0].ncol.to_numpy()
print(f"\nncol medio: con Z={a.mean():.1f} (n={len(a)}), sin Z={b.mean():.1f} (n={len(b)})")
difs = []
for _ in range(5000):
    difs.append(RNG.choice(a, len(a)).mean() - RNG.choice(b, len(b)).mean())
print("  IC 95% de la diferencia:", [round(v, 2) for v in np.percentile(difs, [2.5, 97.5])])

print("\n=== B. Combinaciones color+torsion por quipu ===")
def color_base(x):
    if not isinstance(x, str):
        return "NA"
    return x.split("(")[0].split(":")[0].split("-")[0].split("/")[0].strip()

filas = []
for k, g in c.groupby("kfg"):
    p = g[g.nivel == 0]
    if len(p) < 10:
        continue
    combos = {(color_base(col), tor) for col, tor in zip(p.color, p.torsion)
              if isinstance(col, str) and tor in ("S", "Z")}
    filas.append((k, len(p), len(combos), len(combos) / len(p)))
com = pd.DataFrame(filas, columns=["kfg", "npend", "combos", "ratio"])
print("khipus con >=10 colgantes:", len(com))
print(com.ratio.describe().round(3).to_string())
print("percentil del ratio de Collata (95/487 = 0.195):",
      round((com.ratio <= 95 / 487).mean() * 100, 1), "%")
print("khipus con ratio >= 0.195:", (com.ratio >= 95 / 487).sum())
print("\nSolo khipus con >=100 colgantes:")
print(com[com.npend >= 100].ratio.describe().round(3).to_string())
print("percentil 0.195 en ese subconjunto:",
      round((com[com.npend >= 100].ratio <= 95 / 487).mean() * 100, 1), "%")
