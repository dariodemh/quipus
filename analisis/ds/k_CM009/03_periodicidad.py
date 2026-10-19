# -*- coding: utf-8 -*-
"""CM009: controles finos de periodicidad (nulo que preserva color y nulo global)."""
import pandas as pd, numpy as np

q = pd.read_csv("analisis/ds/k_CM009/cm009_cuerdas.csv").sort_values("cord_id").reset_index(drop=True)
v = q.numeric_value.to_numpy(int)
col = q.color.to_numpy()
n = len(v)
rng = np.random.default_rng(0)

def pval(obs, null):
    null = np.asarray(null)
    return (1 + np.sum(null >= obs)) / (1 + len(null))

# 1) acuerdo lag-20: nulo global vs nulo que preserva color
for L in [4, 20]:
    idx = np.arange(n - L)
    obs = float(np.mean(v[idx] == v[idx + L]))
    ng = [float(np.mean((s := rng.permutation(v))[idx] == s[idx + L])) for _ in range(1000)]
    # nulo preservando color: barajar valores dentro de cada clase de color
    ncol = []
    for _ in range(1000):
        s = v.copy()
        for c in np.unique(col):
            m = np.where(col == c)[0]
            s[m] = rng.permutation(s[m])
        ncol.append(float(np.mean(s[idx] == s[idx + L])))
    print(f"lag {L:2d}: obs={obs:.3f} | p_global={pval(obs,ng):.4f} (nulo {np.mean(ng):.3f}) "
          f"| p_color-preservado={pval(obs,ncol):.4f} (nulo {np.mean(ncol):.3f})")

# 2) secuencias binarias/categóricas periódicas
def lagscore(seq):
    seq = np.asarray(seq)
    return {L: float(np.mean(seq[:-L] == seq[L:])) for L in [4, 20]}
has = (v > 0).astype(int)
# categoría de patrón = cadena de tipos de nudo por posición
import re
def pat(s):
    if not isinstance(s, str): return "-"
    return "".join(m.group(2) for m in re.finditer(r"(\d+)([A-Z]+)\(([\d.]+),(\w)\),(\d+)", s))
patseq = np.array([pat(s) for s in q.knots_string], dtype=object)
valseq = v.astype(str)
print("\nbinaria (tiene nudo) lag20 obs=%.3f" % np.mean(has[:-20] == has[20:]))
print("patrón de tipos de nudo lag20 obs=%.3f" % np.mean(patseq[:-20] == patseq[20:]))
ng = [float(np.mean((s := rng.permutation(patseq))[:-20] == s[20:])) for _ in range(1000)]
print("  patrón lag20 p_global=%.4f (nulo %.3f)" % (pval(np.mean(patseq[:-20] == patseq[20:]), ng), np.mean(ng)))

# 3) estructura por progresiones de 20
print("\n== Subsecuencias en progresión (diferencia 20) ==")
for r in range(20):
    idx = list(range(r, n, 20))
    print(f"  fase {r+1:2d}: pos={[i+1 for i in idx]} vals={[int(v[i]) for i in idx]}")

# 4) los tres valores grandes y sus vecinos
print("\n== Valores grandes y vecindario (dif. 20) ==")
for p in [22, 42, 62]:
    i = p - 1
    print(f"  p{p}={v[i]};  p{p-2}={v[i-2]} p{p-1}={v[i-1]} p{p+1}={v[i+1]} p{p+2}={v[i+2]} p{p+3}={v[i+3]}")
print("  sum big =", int(v[21] + v[41] + v[61]), " total =", int(v.sum()), " resto =", int(v.sum() - v[21] - v[41] - v[61]) )
