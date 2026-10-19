# -*- coding: utf-8 -*-
"""V2: cuentas duplicadas (Urton 2005).
- AS159 vs AS173: ¿hay un tramo de 7 valores consecutivos?
- AS194 vs AS195: ¿120 = 120 es excepcional?
Controles: permutación de una secuencia y distribución de tramos comunes en todo el corpus.
"""
import pandas as pd, numpy as np, os
RNG = np.random.default_rng(20261017)
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str)
for c in ["valor", "nivel", "orden"]:
    D[c] = pd.to_numeric(D[c], errors="coerce")
l0 = D[D.nivel == 0].sort_values(["kfg", "orden"])

def seq(k, maxlen=None):
    v = l0[l0.kfg == k].valor.fillna(0).to_numpy(float)
    return v if maxlen is None else v[:maxlen]

def lccs(a, b):
    """longitud del tramo común contiguo más largo (substring)."""
    if len(a) == 0 or len(b) == 0:
        return 0, None
    prev = np.zeros(len(b) + 1, dtype=int)
    best = 0; end = None
    for i in range(len(a)):
        cur = np.zeros(len(b) + 1, dtype=int)
        cur[1:] = np.where(b == a[i], prev[:-1] + 1, 0)
        j = int(cur.argmax())
        if cur[j] > best:
            best = int(cur[j]); end = (i, j - 1)
        prev = cur
    return best, end

print("=== V2a. AS159 vs AS173 ===")
a, b = seq("AS159"), seq("AS173")
print("AS159:", a.astype(int).tolist())
print("AS173:", b.astype(int).tolist())
L, end = lccs(a, b)
print("LCCS observado:", L, "termina en", end)
if end:
    i, j = end
    print("tramo AS159[%d:%d] = %s" % (i - L + 1, i + 1, a[i - L + 1:i + 1].astype(int).tolist()))
    print("tramo AS173[%d:%d] = %s" % (j - L + 1, j + 1, b[j - L + 1:j + 1].astype(int).tolist()))
B = 20000
null = np.zeros(B, dtype=int)
for t in range(B):
    bp = b.copy(); RNG.shuffle(bp)
    null[t], _ = lccs(a, bp)
p = (1 + (null >= L).sum()) / (B + 1)
print(f"Permutación de AS173 (B={B}): media={null.mean():.2f}, p95={np.percentile(null,95):.0f}, p={p:.4g}")

print("\n=== V2b. AS194 vs AS195 ===")
print("AS194:", seq("AS194").astype(int).tolist(), " AS195:", seq("AS195").astype(int).tolist())
allv = l0.valor.fillna(0)
print("pendientes con valor 120 en el corpus:", int((allv == 120).sum()), "de", len(allv))
print("quipus con algún pendiente 120:", l0[l0.valor == 120].kfg.nunique(), "de", l0.kfg.nunique())
# probabilidad empírica de que dos quipus al azar compartan el mismo valor en su primer pendiente
first = l0.groupby("kfg").first().valor.fillna(0)
print("quipus cuyo primer pendiente vale 120:", int((first == 120).sum()))

print("\n=== V2c. Control corpus: ¿cuán excepcional es un tramo de 7? ===")
# Se excluyen secuencias degeneradas (casi todo ceros o un solo valor), que inflan el LCCS.
ids = []
for k, g in l0.groupby("kfg"):
    v = g.valor.fillna(0).to_numpy(float)
    if 10 <= len(v) <= 60 and len(set(v)) >= 5 and (v > 0).mean() >= 0.5:
        ids.append(k)
print("quipus 10-60 pendientes, >=5 valores distintos y >=50% no-cero:", len(ids))
seqs = {k: seq(k) for k in ids}
maxlen = 0
hits = []
for ii in range(len(ids)):
    for jj in range(ii + 1, len(ids)):
        Lp, _ = lccs(seqs[ids[ii]], seqs[ids[jj]])
        maxlen = max(maxlen, Lp)
        if Lp >= 7:
            hits.append((ids[ii], ids[jj], Lp))
print("pares:", len(ids) * (len(ids) - 1) // 2, "LCCS máximo:", maxlen)
print("pares con tramo >=7:", len(hits), f"({100*len(hits)/(len(ids)*(len(ids)-1)/2):.2f}%)")
print("ejemplos:", sorted(hits, key=lambda x: -x[2])[:6])

print("\n--- duplicados exactos detectados en el propio corpus ---")
# misma secuencia de valores nivel 0 => posible registro duplicado del mismo quipu
from collections import defaultdict
sig = defaultdict(list)
for k, g in l0.groupby("kfg"):
    v = tuple(g.valor.fillna(0).astype(int).tolist())
    if len(v) >= 8:
        sig[v].append(k)
dups = [v for v in sig.values() if len(v) > 1]
print("grupos de quipus con secuencia nivel-0 idéntica (>=8 cuerdas):", len(dups))
print(dups[:6])

print("\nresumen:", dict(AS159_AS173_L=L, p_perm=float(p), pares_AS=hits and len(hits)))
