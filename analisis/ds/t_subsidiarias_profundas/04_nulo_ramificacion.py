# -*- coding: utf-8 -*-
"""Forma de los arboles frente a nulos de ramificacion aleatoria.

Nulo A (conservador): conserva exactamente la secuencia de grados de salida
  (numero de hijos por nodo) y aleatoriza el emparejamiento.
Nulo B: arbol recursivo aleatorio (cada nodo se cuelga de uno previo uniforme),
  conserva solo n.

Salidas: forma_arboles.csv, forma_quipus.csv, forma_stats.json
"""
import pandas as pd, numpy as np, os, json
from collections import defaultdict

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
rng = np.random.default_rng(7)
REPS = 400

d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
T = pd.read_csv(os.path.join(OUT, 'arboles.csv'))
KFG_DEEP = set(T.kfg)


def sim_depth_deg(degs, reps, rng):
    n = len(degs); out = np.zeros(reps, dtype=int)
    if n <= 1: return out
    base = list(range(1, n))
    for r in range(reps):
        pool = base.copy(); rng.shuffle(pool)
        depth = np.zeros(n, dtype=int); q = [0]; head = 0; ptr = 0; md = 0
        while head < len(q):
            u = q[head]; head += 1
            for _ in range(degs[u]):
                v = pool[ptr]; ptr += 1
                depth[v] = depth[u] + 1
                if depth[v] > md: md = depth[v]
                q.append(v)
        out[r] = md
    return out


def sim_depth_rrt(n, reps, rng):
    out = np.zeros(reps, dtype=int)
    for r in range(reps):
        depth = np.zeros(n, dtype=int); md = 0
        for i in range(1, n):
            p = rng.integers(0, i)
            depth[i] = depth[p] + 1
            if depth[i] > md: md = depth[i]
        out[r] = md
    return out


rows = []
for kfg, g in d[d.kfg.isin(KFG_DEEP)].groupby('kfg', sort=False):
    ch = defaultdict(list)
    for c, p in zip(g['cuerda'], g['padre']):
        if isinstance(p, str): ch[p].append(c)
    def hh(x):
        return 0 if not ch.get(x) else 1 + max(hh(k) for k in ch[x])
    for r in g.loc[g['nivel'] == 0, 'cuerda']:
        nodes = [r]; q = [r]
        while q:
            x = q.pop()
            for k in ch.get(x, []):
                nodes.append(k); q.append(k)
        rows.append(dict(kfg=kfg, raiz=r, n=len(nodes), altura_obs=hh(r),
                         degs=[len(ch.get(x, [])) for x in nodes]))
F = pd.DataFrame(rows)
print('arboles en quipus con estructura profunda:', len(F), '| con n>=4:', int((F.n >= 4).sum()))

res = []
for _, r in F[F.n >= 4].iterrows():
    degs = r.degs
    sd = sim_depth_deg(degs, REPS, rng)
    sr = sim_depth_rrt(len(degs), REPS, rng)
    res.append(dict(kfg=r.kfg, raiz=r.raiz, n=r.n, altura_obs=int(r.altura_obs),
                    mA=float(sd.mean()), q95A=float(np.percentile(sd, 95)),
                    pA=float((1 + (sd >= r.altura_obs).sum()) / (1 + REPS)),
                    mB=float(sr.mean()), q95B=float(np.percentile(sr, 95)),
                    pB=float((1 + (sr >= r.altura_obs).sum()) / (1 + REPS))))
R = pd.DataFrame(res)
R.to_csv(os.path.join(OUT, 'forma_arboles.csv'), index=False)

deep = R[R.altura_obs >= 3]
print('\nArboles altura>=3:', len(deep))
print('  obs media %.2f | nulo A media %.2f | nulo B media %.2f' %
      (deep.altura_obs.mean(), deep.mA.mean(), deep.mB.mean()))
print('  P(nuloA>=obs): media %.3f mediana %.3f frac<0.05 %.2f' %
      (deep.pA.mean(), deep.pA.median(), (deep.pA < 0.05).mean()))
print('  P(nuloB>=obs): media %.3f mediana %.3f frac<0.05 %.2f' %
      (deep.pB.mean(), deep.pB.median(), (deep.pB < 0.05).mean()))

# test valido por quipu: numero de arboles con altura>=3 vs Poisson-binomial (nulo A)
per = []
for kfg, g in R.groupby('kfg'):
    ps = [float((sim_depth_deg(F.loc[(F.kfg == kfg) & (F.raiz == raiz), 'degs'].iloc[0], 200, rng) >= 3).mean())
          for raiz in g.raiz]
    K = int((g.altura_obs >= 3).sum())
    dist = np.array([1.0])
    for p in ps:
        dist = np.convolve(dist, [1 - p, p])
    per.append(dict(kfg=kfg, pendants_n4=len(g), obs_prof=K, esp_prof=float(sum(ps)),
                    p=float(dist[K:].sum()), altura_max=int(g.altura_obs.max()),
                    altura_media_nula=float(g.mA.mean())))
Q = pd.DataFrame(per).sort_values('p').reset_index(drop=True)
m = len(Q)
Q['bh'] = (Q['p'] * m / np.arange(1, m + 1)).iloc[::-1].cummin().iloc[::-1]
Q.to_csv(os.path.join(OUT, 'forma_quipus.csv'), index=False)
print('\nTest por quipu (n=%d): obs=%d esperado=%.1f | BH<0.05: %d' %
      (len(Q), Q.obs_prof.sum(), Q.esp_prof.sum(), int((Q.bh < 0.05).sum())))
print(Q.head(10).to_string(index=False))

json.dump(dict(n_arboles=int(len(F)), n_deep=int(len(deep)),
               altura_obs=float(deep.altura_obs.mean()),
               nulaA=float(deep.mA.mean()), nulaB=float(deep.mB.mean()),
               pA_media=float(deep.pA.mean()), pA_mediana=float(deep.pA.median()),
               pB_media=float(deep.pB.mean()), pB_mediana=float(deep.pB.median()),
               fracA05=float((deep.pA < 0.05).mean()), fracB05=float((deep.pB < 0.05).mean()),
               quipus_bh=int((Q.bh < 0.05).sum())),
          open(os.path.join(OUT, 'forma_stats.json'), 'w'), indent=2)

print('\nMas extremos por pA:')
print(deep.sort_values('pA').head(10)[['kfg', 'raiz', 'n', 'altura_obs', 'mA', 'q95A', 'mB', 'q95B', 'pA', 'pB']].to_string(index=False))
