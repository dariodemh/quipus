# -*- coding: utf-8 -*-
"""V3: estructura de UR6 y su relación con UR9/UR21 (Urton 2001, 2005).
Comprueba: 762 pendientes, 730 en 24 conjuntos de 29-31, total 2.962 nudos,
y replicación de un segmento por UR9/UR21.
"""
import pandas as pd, numpy as np, re, os
RNG = np.random.default_rng(20261017)
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str)
for c in ["valor", "nivel", "orden", "grupo"]:
    D[c] = pd.to_numeric(D[c], errors="coerce")

def nknots(s):
    if not isinstance(s, str):
        return 0
    return sum(int(m.group(1)) for m in re.finditer(r"(?:^|;)(\d+)[A-Z]", s))

print("=== V3a. UR6: conteos ===")
for k in ["UR006", "UR009", "UR021"]:
    x = D[D.kfg == k]
    p = x[x.nivel == 0]
    print(f"{k}: cuerdas={len(x)} pendientes={len(p)} nivel1={int((x.nivel==1).sum())} "
          f"grupos={p.grupo.nunique()} nudos={int(x.nudos.apply(nknots).sum())} "
          f"suma_valores={p.valor.fillna(0).sum():.0f}")
x = D[D.kfg == "UR006"]; p = x[x.nivel == 0]
gs = p.groupby("grupo").size()
print("UR006 tamaños de grupo:", gs.value_counts().sort_index().to_dict())
print("UR006 grupos de 29-31:", int(((gs >= 29) & (gs <= 31)).sum()))
print("UR006 pendientes en grupos de 29-31:", int(gs[(gs >= 29) & (gs <= 31)].sum()))
print("UR006 pendientes / 24 =", round(len(p) / 24, 1))
print("UR006 nudos / 2 =", nknots_sum := int(x.nudos.apply(nknots).sum()) / 2)
# distribución de valores: ¿periodicidad de 29-31?
print("UR006 nudos por grupo (primeros 12):", [int(p[p.grupo==g].nudos.apply(nknots).sum()) for g in sorted(gs.index)[:12]])

def lccs(a, b):
    if len(a) == 0 or len(b) == 0:
        return 0
    prev = np.zeros(len(b) + 1, dtype=int); best = 0
    for i in range(len(a)):
        cur = np.zeros(len(b) + 1, dtype=int)
        cur[1:] = np.where(b == a[i], prev[:-1] + 1, 0)
        best = max(best, int(cur.max()))
        prev = cur
    return best

def seq(k):
    return D[(D.kfg == k) & (D.nivel == 0)].sort_values("orden").valor.fillna(0).to_numpy(float)

print("\n=== V3b. ¿UR9/UR21 replican un segmento de UR6? ===")
a = seq("UR006")
for k in ["UR009", "UR021"]:
    b = seq(k)
    L = lccs(a, b)
    null = np.zeros(5000, dtype=int)
    for t in range(5000):
        bp = b.copy(); RNG.shuffle(bp)
        null[t] = lccs(a, bp)
    p = (1 + (null >= L).sum()) / 5001
    print(f"UR006 vs {k}: LCCS={L} (de {len(b)} cuerdas), nulo medio={null.mean():.1f} "
          f"p95={np.percentile(null,95):.0f} p={p:.4g}")

print("\nresumen:", dict(ur6_pend=int(len(D[(D.kfg=='UR006')&(D.nivel==0)])),
                         ur6_nudos=int(D[D.kfg=='UR006'].nudos.apply(nknots).sum())))
