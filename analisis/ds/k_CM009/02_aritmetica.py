# -*- coding: utf-8 -*-
"""CM009: aritmética interna, periodicidad y controles nulos (permutación, 1000, semilla 0)."""
import pandas as pd, numpy as np

q = pd.read_csv("analisis/ds/k_CM009/cm009_cuerdas.csv").sort_values("cord_id").reset_index(drop=True)
v = q.numeric_value.to_numpy(dtype=int)
col = q.color.to_numpy()
n = len(v)
rng = np.random.default_rng(0)
prefix = np.concatenate([[0], np.cumsum(v)])
pos_by_val = {}
for i, x in enumerate(v):
    pos_by_val.setdefault(int(x), []).append(i)

def pval(obs, null):
    null = np.asarray(null)
    return (1 + np.sum(null >= obs)) / (1 + len(null))

# ---------- 1) periodicidad de COLOR ----------
print("== Periodicidad de color ==")
for L in [2, 3, 4, 5, 20]:
    obs = np.mean(col[:-L] == col[L:])
    null = [np.mean(c[:-L] == c[L:]) for c in (rng.permutation(col) for _ in range(1000))]
    print(f"  lag {L:2d}: acuerdo obs={obs:.3f}  p={pval(obs,null):.4f}  nulo_medio={np.mean(null):.3f}")

# ---------- 2) periodicidad de VALOR ----------
print("\n== Periodicidad de valor: fracción v[i]==v[i+L] ==")
for L in [4, 5, 8, 10, 20]:
    idx = np.arange(n - L)
    obs = np.mean(v[idx] == v[idx + L])
    null = []
    for _ in range(1000):
        s = rng.permutation(v)
        null.append(np.mean(s[idx] == s[idx + L]))
    print(f"  lag {L:2d}: obs={obs:.3f} p={pval(obs,null):.4f}")

# ---------- 3) valores repetidos ----------
print("\n== Valores repetidos ==")
vc = pd.Series(v).value_counts()
obs_rep = int(vc[vc > 1].sum())
null = []
for _ in range(1000):
    s = pd.Series(rng.permutation(v)).value_counts()
    null.append(int(s[s > 1].sum()))
print(f"  cuerdas con valor no único: obs={obs_rep} p={pval(obs_rep,null):.4f}")
print(f"  valor 1 aparece {vc.get(1,0)}x; 0/sin-nudo {vc.get(0,0)}x; 3 aparece {vc.get(3,0)}x")

# ---------- 4) sumas contiguas ----------
def count_contig(vals):
    c = 0
    hits = []
    pre = np.concatenate([[0], np.cumsum(vals)])
    for i in range(n):
        for j in range(i + 1, n):           # >=2 sumandos
            t = pre[j + 1] - pre[i]
            if t <= 0:
                continue
            for k in pos_by_val.get(int(t), []):
                if k < i or k > j:
                    c += 1
                    hits.append((k, i, j))
    return c, hits

print("\n== Sumas contiguas de >=2 cuerdas que igualan otra cuerda ==")
obs, hits = count_contig(v)
null = [count_contig(rng.permutation(v))[0] for _ in range(1000)]
print(f"  coincidencias obs={obs} p={pval(obs,null):.4f}")
for k, i, j in hits[:12]:
    print(f"    {q.cord_name[k]}={v[k]}  = suma pos {i+1}..{j+1}")

# ---------- 5) acumulados ----------
print("\n== Acumulado P_i que iguala una cuerda posterior ==")
run = np.cumsum(v)
hitsp = [(i + 1, int(v[k]), int(run[i])) for i in range(n) for k in range(i + 1, n) if v[k] == run[i]]
print("  total:", len(hitsp), hitsp[:8])

# ---------- 6) sumas por bloques candidatos ----------
print("\n== Sumas por bloques candidatos (¿un bloque = otra cuerda?) ==")
for start, size in [(0, 5), (4, 4), (5, 4), (0, 4)]:
    blocks = [v[s:s + size].sum() for s in range(start, n - size + 1, size)]
    print(f"  bloque start={start+1} size={size}: sums={blocks}")
