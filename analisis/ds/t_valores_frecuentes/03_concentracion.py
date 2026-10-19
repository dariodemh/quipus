# -*- coding: utf-8 -*-
"""Concentracion por quipu de cada valor + nulo por permutacion entre quipus.

Nulo: se barajan los valores entre quipus DENTRO de cada estrato (longitud, primer digito),
es decir 1-9 | 10-19 | 20-29 | ... | 100-109 | ...
Conserva (i) cuantas cuerdas tiene cada quipu en cada decada y (ii) la frecuencia global
de cada valor. Destruye solo la asociacion valor-quipu DENTRO de la decada, de modo que
un quipu que usa valores grandes no aparece artificialmente sobrerrepresentando valores
pequenos. Es el control de la explicacion aburrida "escala del quipu".
"""
import pandas as pd, numpy as np, os
from scipy import stats

RUTA = r"./analisis/datos"
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261018)
NPERM = 1000

c = pd.read_csv(RUTA + r"\cuerdas.csv", low_memory=False)
k = c[c.nudos.notna() & c.valor.notna()].copy()
k["valor"] = k.valor.astype(int)
k = k[k.valor > 0].reset_index(drop=True)

qids = sorted(k.kfg.unique())
qidx = {q: i for i, q in enumerate(qids)}
k["qi"] = k.kfg.map(qidx)
k["L"] = k.valor.map(lambda v: len(str(v)))
k["d1"] = k.valor.map(lambda v: int(str(v)[0]))
# estrato: decada (para 1 digito, todo 1-9 junto)
k["est"] = np.where(k.L == 1, 0, k.L * 10 + k.d1)
ests = sorted(k.est.unique())
eidx = {e: i for i, e in enumerate(ests)}

qi = k.qi.values; val = k.valor.values; est = k.est.values
ne = len(ests); nq = len(qids)
E = np.array([eidx[e] for e in est])

f = pd.Series(val).value_counts()
preval = k.groupby("valor").kfg.nunique()

prob = sorted(set(f[f >= 50].index) | {1, 2, 5, 10, 12, 15, 20, 30, 40, 100, 200, 110, 47, 33, 22})
print("valores probados:", len(prob), "| cuerdas cubiertas:", int(f[prob].sum()), "/", len(k))

# cuerdas por quipu y estrato
n_ie = np.zeros((nq, ne))
np.add.at(n_ie, (qi, E), 1)
tot_e = n_ie.sum(0)

exp_i = {}
for v in prob:
    e = eidx[0 if len(str(v)) == 1 else len(str(v)) * 10 + int(str(v)[0])]
    p = f.get(v, 0) / tot_e[e] if tot_e[e] > 0 else 0.0
    exp_i[v] = n_ie[:, e] * p

obs_counts = {v: np.bincount(qi[val == v], minlength=nq) for v in prob}


def stats_de(cnt, exp):
    n2 = (cnt >= 2).sum(); n3 = (cnt >= 3).sum()
    p1 = stats.poisson.sf(cnt - 1, exp)
    sobre = (p1 < 0.05).sum()
    tot = cnt.sum()
    hhi = ((cnt / tot) ** 2).sum() if tot else np.nan
    top = cnt.max() / tot if tot else np.nan
    return (cnt >= 1).sum(), int(n2), int(n3), int(sobre), hhi, top


observ = {v: stats_de(obs_counts[v], exp_i[v]) for v in prob}
perms = {v: [] for v in prob}
for it in range(NPERM):
    vp = val.copy()
    for e in range(ne):
        m = np.where(E == e)[0]
        if len(m) > 1:
            vp[m] = rng.permutation(val[m])
    for v in prob:
        perms[v].append(stats_de(np.bincount(qi[vp == v], minlength=nq), exp_i[v]))

rows = []
for v in prob:
    o = observ[v]; P = np.array(perms[v], float)
    def pemp(col, greater=True):
        if greater:
            return (1 + (P[:, col] >= o[col]).sum()) / (1 + NPERM)
        return (1 + (np.abs(P[:, col] - P[:, col].mean()) >= abs(o[col] - P[:, col].mean())).sum()) / (1 + NPERM)
    rows.append({"valor": v, "n": int(f.get(v, 0)), "quipus_obs": int(preval.get(v, 0)),
                 "n_ge2_obs": o[1], "n_ge2_null": round(P[:, 1].mean(), 1),
                 "n_sobre_obs": o[3], "n_sobre_null": round(P[:, 3].mean(), 1),
                 "hhi_obs": o[4], "hhi_null": round(P[:, 4].mean(), 6),
                 "p_sobre": pemp(3), "p_ge2": pemp(1, False), "p_hhi": pemp(4)})
R = pd.DataFrame(rows)


def bh(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); q = np.empty(m); prev = 1.0
    for i in range(m - 1, -1, -1):
        prev = min(prev, p[o[i]] * m / (i + 1)); q[o[i]] = prev
    return q


for col in ["p_sobre", "p_ge2", "p_hhi"]:
    R["q" + col[1:]] = bh(R[col].values)
R = R.sort_values("n", ascending=False)
R.to_csv(OUT + r"\tabla_concentracion.csv", index=False)

pd.set_option("display.width", 260)
print("\n=== mas quipus sobrerrepresentados de lo esperado ===")
print(R[R.n >= 50].sort_values("p_sobre")[["valor", "n", "quipus_obs", "n_sobre_obs", "n_sobre_null", "q_sobre", "hhi_obs", "hhi_null"]]
      .head(16).to_string(index=False, float_format=lambda x: f"{x:.3g}"))
print("\n=== candidatos ===")
cand = [1, 2, 3, 5, 10, 11, 12, 15, 20, 22, 30, 33, 40, 47, 50, 100, 110, 200]
print(R[R.valor.isin(cand)].sort_values("n", ascending=False)[["valor", "n", "quipus_obs", "n_sobre_obs", "n_sobre_null", "q_sobre", "n_ge2_obs", "n_ge2_null", "hhi_obs", "hhi_null"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3g}"))
print("\n=== concentracion (hhi) ===")
print(R[R.n >= 50].sort_values("p_hhi")[["valor", "n", "quipus_obs", "hhi_obs", "hhi_null", "q_hhi"]]
      .head(10).to_string(index=False, float_format=lambda x: f"{x:.3g}"))
print("\nsobreviven BH q<0.05 (n>=50):  sobre=%d/%d  hhi=%d/%d  ge2=%d/%d" %
      ((R.q_sobre < .05).sum(), len(R), (R.q_hhi < .05).sum(), len(R), (R.q_ge2 < .05).sum(), len(R)))

print("\n=== quipus que mas aportan cada candidato ===")
meta = pd.read_csv(RUTA + r"\quipus.csv", low_memory=False).set_index("kfg")
for v in [100, 200, 110, 47, 33, 22, 15, 10, 1]:
    cnt = obs_counts[v]; top = np.argsort(cnt)[::-1][:5]; tot = cnt.sum()
    parts = []
    for i in top:
        if cnt[i] == 0: break
        parts.append(f"{qids[i]}({int(cnt[i])},{str(meta.procedencia.get(qids[i],'?'))[:20]})")
    print(f"v={v:>4} total={tot:>5} top5={' '.join(parts)}")
