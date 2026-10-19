# -*- coding: utf-8 -*-
"""Nulo enfocado en la regla principal (grupo adyacente completo, nivel 0),
con estadisticos a nivel de QUIPU y desagregado por tamano de grupo (6 vs otros).
"""
import pandas as pd, numpy as np, os, json, time

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
rng = np.random.default_rng(20261019)
NPERM = 2000

c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
c['sin_nudos'] = c['nudos'].isna() | (c['nudos'].astype(str).str.strip().isin(['', 'nan']))
c['val'] = c['valor'].astype(float)
c.loc[c['sin_nudos'] & (c['val'] == 0), 'val'] = np.nan
c = c.sort_values(['kfg', 'orden']).reset_index(drop=True)
c['idx'] = np.arange(len(c))
V = c['val'].values

units = []; top_names = {}
for kfg, d in c.groupby('kfg'):
    T = d[d['union'] == 'T']
    if len(T) == 0: continue
    l0 = d[d['nivel'] == 0]
    cand = set(l0[l0['union'] == 'T']['cuerda']) | set(T[T['nivel'] == 1]['padre'].dropna())
    top_names[kfg] = set()
    for nm in cand:
        t = d[d['cuerda'] == nm].iloc[0]
        desc = set(); st = [nm]
        while st:
            p = st.pop()
            for ch in d[d['padre'] == p]['cuerda']:
                desc.add(ch); st.append(ch)
        top_names[kfg] |= {nm} | desc
        units.append(dict(kfg=kfg, top=nm, val=float(t['val']) if pd.notna(t['val']) else np.nan,
                          grupo=int(t['grupo'])))
U = pd.DataFrame(units)

# estructuras adyacentes nivel 0
struct = []
for i, u in U.iterrows():
    sides = []
    for gr in (u.grupo - 1, u.grupo + 1):
        d = c[(c['kfg'] == u.kfg) & (c['grupo'] == gr) & (c['nivel'] == 0)].sort_values('orden')
        if len(d) >= 2:
            sides.append(d['idx'].values)
    struct.append(dict(i=i, kfg=u.kfg, val=u.val, sides=sides,
                       sizes=[len(s) for s in sides]))

def hit_one(vals, rec):
    if pd.isna(rec['val']): return False
    for idx in rec['sides']:
        v = vals[idx]; vv = v[~np.isnan(v)]
        if len(vv) >= 2 and np.isclose(vv.sum(), rec['val']):
            return True
    return False

def evaluate(vals):
    return {r['i']: hit_one(vals, r) for r in struct if r['sides']}

def stats(h):
    byq = {}
    for i, v in h.items():
        byq.setdefault(struct[i]['kfg'], []).append(v)
    tot = int(sum(h.values()))
    nq = sum(1 for v in byq.values() if any(v))
    meanrate = float(np.mean([np.mean(v) for v in byq.values()]))
    return tot, nq, meanrate

obs_h = evaluate(V)
OBS = stats(obs_h)
print('obs total=%d quipus_con_hit=%d media_tasa=%.4f' % OBS, flush=True)
print('denominador unidades:', len(obs_h), 'quipus:', len({struct[i]["kfg"] for i in obs_h}))

# subgrupos por tamano
def subgroup(rec, n):
    return rec['sizes'] and all(s == n for s in rec['sizes'])
sub6 = {i for i in obs_h if subgroup(struct[i], 6)}
subother = {i for i in obs_h if not subgroup(struct[i], 6)}
sub_has6 = {i for i in obs_h if 6 in struct[i]['sizes']}
sub_no6 = {i for i in obs_h if 6 not in struct[i]['sizes']}
print('all6: %d/%d   otros: %d/%d   has6: %d/%d   no6: %d/%d' % (
    sum(obs_h[i] for i in sub6), len(sub6),
    sum(obs_h[i] for i in subother), len(subother),
    sum(obs_h[i] for i in sub_has6), len(sub_has6),
    sum(obs_h[i] for i in sub_no6), len(sub_no6)))

# nulo
groups = {k: d for k, d in c.groupby('kfg')}
idxN1 = {k: d[(d['nivel'] == 0) & (~d['cuerda'].isin(top_names.get(k, set())))]['idx'].values
         for k, d in groups.items()}
res = dict(total=[], nq=[], mean=[], t6=[], toth=[], th6=[], tno6=[])
t0 = time.time()
for perm in range(NPERM):
    vals = V.copy()
    for k, idx in idxN1.items():
        v = vals[idx]; m = ~np.isnan(v)
        vv = v[m].copy(); rng.shuffle(vv); vals[idx[m]] = vv
    h = evaluate(vals)
    t, nq, mr = stats(h)
    res['total'].append(t); res['nq'].append(nq); res['mean'].append(mr)
    res['t6'].append(sum(h[i] for i in sub6))
    res['toth'].append(sum(h[i] for i in subother))
    res['th6'].append(sum(h[i] for i in sub_has6))
    res['tno6'].append(sum(h[i] for i in sub_no6))
    if (perm + 1) % 500 == 0:
        print('perm', perm + 1, '%.0fs' % (time.time() - t0), flush=True)

def pval(arr, obs):
    arr = np.array(arr)
    return (1 + np.sum(arr >= obs)) / (len(arr) + 1), float(arr.mean()), float(np.quantile(arr, .95))

out = {}
for key, obsval in [('total', OBS[0]), ('nq', OBS[1]), ('mean', OBS[2]),
                    ('t6', sum(obs_h[i] for i in sub6)),
                    ('toth', sum(obs_h[i] for i in subother)),
                    ('th6', sum(obs_h[i] for i in sub_has6)),
                    ('tno6', sum(obs_h[i] for i in sub_no6))]:
    p, mu, q95 = pval(res[key], obsval)
    out[key] = dict(obs=float(obsval), nulo_medio=mu, nulo_p95=q95, p=p)
print(json.dumps(out, indent=2, ensure_ascii=False))
json.dump(out, open(os.path.join(BASE, 'nulo_quipu.json'), 'w'), ensure_ascii=False, indent=2)
np.save(os.path.join(BASE, 'nulo_quipu_totales.npy'), np.array(res['total']))
np.save(os.path.join(BASE, 'nulo_quipu_nq.npy'), np.array(res['nq']))
