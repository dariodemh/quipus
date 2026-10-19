# -*- coding: utf-8 -*-
"""Tests de suma jerarquica y relaciones alternativas, con nulo de permutacion
de valores observados dentro de cada quipu.

Salidas: sumas_nulo.csv, sumas_stats.json, sumas_grupos.csv
"""
import pandas as pd, numpy as np, os, itertools, json
from collections import defaultdict

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
rng = np.random.default_rng(20261017)

d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv')).reset_index(drop=True)
d['sin_nudos'] = d['nudos'].isna() | d['nudos'].astype(str).str.strip().isin(['', 'nan'])
d['v'] = d['valor'].astype(float)
d.loc[d['sin_nudos'] & (d['v'] == 0), 'v'] = np.nan
V = d['v'].to_numpy()

# --- grupos padre-hijo y arboles profundos
T = pd.read_csv(os.path.join(OUT, 'arboles.csv'))
deep_cords = set()
ch_all = defaultdict(list)
idx_map = {}
for i, (kfg, c, p) in enumerate(zip(d['kfg'], d['cuerda'], d['padre'])):
    idx_map[(kfg, c)] = i
    if isinstance(p, str):
        ch_all[(kfg, p)].append((kfg, c))
for _, r in T.iterrows():
    stack = [(r.kfg, r.raiz)]
    while stack:
        x = stack.pop()
        if x in deep_cords: continue
        deep_cords.add(x); stack.extend(ch_all.get(x, []))

groups = []   # (kfg, pi, kids, nivel, profundo)
for (kfg, p), kidnames in ch_all.items():
    pi = idx_map[(kfg, p)]
    kids = [idx_map[x] for x in kidnames]
    groups.append((kfg, pi, kids, int(d.at[pi, 'nivel']), (kfg, p) in deep_cords))
print('grupos padre-hijo:', len(groups), '| en arboles profundos:', sum(g[4] for g in groups))

# --- test 1: padre = suma de todos los hijos (corpus)
valid = []
for gi, (kfg, pi, kids, niv, prof) in enumerate(groups):
    if len(kids) >= 2 and pd.notna(V[pi]) and not np.isnan(V[kids]).any():
        valid.append((gi, kfg, pi, kids, niv, prof))
gid = np.array([g[0] for g in valid])
edge_g = np.concatenate([np.full(len(g[3]), g[0]) for g in valid]).astype(int)
edge_c = np.concatenate([np.array(g[3]) for g in valid]).astype(int)
gp = np.array([g[2] for g in valid]).astype(int)
glvl = np.array([g[4] for g in valid])
gdeep = np.array([g[5] for g in valid])
print('grupos comparables (todos los valores presentes):', len(valid))

def matches(vals):
    s = np.bincount(edge_g, weights=vals[edge_c], minlength=len(valid))
    return np.abs(s[gid] - vals[gp]) < 1e-6

obs = matches(V)
print('padre = suma(todos): %d/%d = %.2f%%' % (obs.sum(), len(valid), 100*obs.mean()),
      '| en arboles profundos: %d/%d' % (obs[gdeep].sum(), gdeep.sum()))

# --- nulo: permutar valores observados dentro de cada quipu
blocks = [(g.index.to_numpy()) for _, g in d.groupby('kfg', sort=False)]
obs_tot = int(obs.sum()); obs_deep = int(obs[gdeep].sum()); obs_lvl3 = int(obs[glvl >= 3].sum())
null_tot, null_deep, null_lvl3 = [], [], []
for rep in range(2000):
    vp = V.copy()
    for b in blocks:
        ok = b[~np.isnan(V[b])]
        vp[ok] = rng.permutation(V[ok])
    m = matches(vp)
    null_tot.append(int(m.sum())); null_deep.append(int(m[gdeep].sum())); null_lvl3.append(int(m[glvl >= 3].sum()))
null_tot = np.array(null_tot); null_deep = np.array(null_deep); null_lvl3 = np.array(null_lvl3)
p_tot = (1 + (null_tot >= obs_tot).sum()) / (1 + len(null_tot))
p_deep = (1 + (null_deep >= obs_deep).sum()) / (1 + len(null_deep))
p_lvl3 = (1 + (null_lvl3 >= obs_lvl3).sum()) / (1 + len(null_lvl3))
print('NULO total: obs=%d nulo=%.1f [%.0f,%.0f] p=%.4f' % (obs_tot, null_tot.mean(),
      np.percentile(null_tot, 2.5), np.percentile(null_tot, 97.5), p_tot))
print('NULO profundo: obs=%d nulo=%.2f p=%.4f' % (obs_deep, null_deep.mean(), p_deep))
print('NULO nivel>=3: obs=%d nulo=%.2f p=%.4f' % (obs_lvl3, null_lvl3.mean(), p_lvl3))

# --- tabla por quipu (para BH se usa test binomial exacto contra tasa nula global)
q = null_tot.mean() / len(valid)
from scipy.stats import binomtest
per = []
for kfg in sorted(set(g[1] for g in valid)):
    idx = [i for i, g in enumerate(valid) if g[1] == kfg]
    k = int(obs[idx].sum()); n = len(idx)
    if n == 0: continue
    pv = binomtest(k, n, q, alternative='greater').pvalue
    per.append(dict(kfg=kfg, tests=n, obs=k, esperado=n*q, p=pv))
P = pd.DataFrame(per)
P['bh'] = np.minimum.accumulate((P.sort_values('p')['p'] * len(P) / np.arange(1, len(P)+1)).iloc[::-1].values)[::-1] if len(P) else []
P.to_csv(os.path.join(OUT, 'sumas_por_quipu.csv'), index=False)

# --- tests alternativos en arboles profundos
def subset_hit(cv, pv, kmax=10):
    k = len(cv)
    if k > kmax: return False
    for r in range(1, k):
        for c in itertools.combinations(range(k), r):
            if abs(cv[list(c)].sum() - pv) < 1e-6:
                return True
    return False

def alt_scan(vals):
    sub = her = 0; nn = 0
    for (kfg, pi, kids, niv, prof) in groups:
        if not prof: continue
        pv = vals[pi]; cv = vals[kids]
        if pd.isna(pv) or np.isnan(cv).any() or len(kids) < 2: continue
        nn += 1
        if len(kids) >= 3 and any(abs(cv[i] - (cv.sum()-cv[i])) < 1e-6 for i in range(len(kids))): her += 1
        if subset_hit(cv, pv): sub += 1
    return nn, sub, her

nn, o_sub, o_her = alt_scan(V)
print('\nArboles profundos: %d grupos comparables' % nn)
print('  padre = subconjunto propio de hijos: %d (%.1f%%)' % (o_sub, 100*o_sub/nn))
print('  un hijo = suma de los demas: %d (%.1f%%)' % (o_her, 100*o_her/nn))
ns, nh = [], []
for rep in range(1000):
    vp = V.copy()
    for b in blocks:
        ok = b[~np.isnan(V[b])]
        vp[ok] = rng.permutation(V[ok])
    _, s, h = alt_scan(vp)
    ns.append(s); nh.append(h)
ns = np.array(ns); nh = np.array(nh)
p_sub = (1 + (ns >= o_sub).sum()) / (1 + len(ns))
p_her = (1 + (nh >= o_her).sum()) / (1 + len(nh))
print('  NULO subconjunto: media %.2f p=%.4f | NULO hermano: media %.2f p=%.4f' %
      (ns.mean(), p_sub, nh.mean(), p_her))

# --- nodos que cumplen
print('\nNodos que cumplen padre=suma(todos):')
for i, ok in enumerate(obs):
    if ok:
        _, kfg, pi, kids, niv, prof = valid[i]
        print(' ', kfg, d.at[pi, 'cuerda'], 'nivel', niv, 'valor', V[pi],
              'hijos', [(d.at[k, 'cuerda'], V[k]) for k in kids])

json.dump(dict(n_grupos=len(groups), n_valid=len(valid), obs_total=obs_tot,
               null_total_mean=float(null_tot.mean()), p_total=float(p_tot),
               obs_deep=obs_deep, null_deep_mean=float(null_deep.mean()), p_deep=float(p_deep),
               obs_lvl3=obs_lvl3, p_lvl3=float(p_lvl3), q_null=float(q),
               n_alt=nn, obs_sub=o_sub, p_sub=float(p_sub), obs_her=o_her, p_her=float(p_her)),
          open(os.path.join(OUT, 'sumas_stats.json'), 'w'), indent=2)
pd.DataFrame(dict(obs=obs_tot, null=null_tot)).to_csv(os.path.join(OUT, 'sumas_nulo.csv'), index=False)
print('\nBH quipus con p<0.05:', int((P.bh < 0.05).sum()), 'de', len(P))
print(P.sort_values('p').head(8).to_string(index=False))
