# -*- coding: utf-8 -*-
"""Modelo nulo por permutacion de valores DENTRO de cada quipu (version rapida).

N1: permuta valores de cuerdas nivel 0 no-superiores dentro del quipu.
N2: permuta valores de todas las cuerdas no-superiores dentro del quipu.

Familias: full (grupo completo), contig (sub-bloque contiguo >=2),
color (subconjunto por color >=2), alt (posiciones pares/impares >=2).
"""
import pandas as pd, numpy as np, os, json, time

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
rng = np.random.default_rng(20261017)
NPERM = 2000

c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
c['sin_nudos'] = c['nudos'].isna() | (c['nudos'].astype(str).str.strip().isin(['', 'nan']))
c['val'] = c['valor'].astype(float)
c.loc[c['sin_nudos'] & (c['val'] == 0), 'val'] = np.nan
c = c.sort_values(['kfg', 'orden']).reset_index(drop=True)
c['idx'] = np.arange(len(c))
V = c['val'].values.astype(float)

# --- unidades de cuerda superior ---
units = []
top_names = {}
for kfg, d in c.groupby('kfg'):
    T = d[d['union'] == 'T']
    if len(T) == 0:
        continue
    l0 = d[d['nivel'] == 0]
    cand = set(l0[l0['union'] == 'T']['cuerda']) | set(T[T['nivel'] == 1]['padre'].dropna())
    top_names[kfg] = set()
    for nm in cand:
        t = d[d['cuerda'] == nm].iloc[0]
        kids = d[d['padre'] == nm]
        desc = set(); stack = [nm]
        while stack:
            p = stack.pop()
            for ch in d[d['padre'] == p]['cuerda']:
                desc.add(ch); stack.append(ch)
        top_names[kfg] |= {nm} | desc
        units.append(dict(kfg=kfg, top=nm, val=float(t['val']) if pd.notna(t['val']) else np.nan,
                          grupo=int(t['grupo']), n_kids=len(kids),
                          kids_sum=float(np.nansum(kids['val'].values)) if len(kids) else np.nan))
U = pd.DataFrame(units)

# --- precomputar estructuras por unidad y lado ---
def group_struct(kfg, gr, level_zero):
    d = c[(c['kfg'] == kfg) & (c['grupo'] == gr)].sort_values('orden')
    if level_zero:
        d = d[d['nivel'] == 0]
    idx = d['idx'].values
    vals = V[idx]
    mask = ~np.isnan(vals)
    cols = d['color'].astype(str).values
    struct = dict(idx=idx, mask=mask, cols=cols, n=len(idx))
    # sub-bloques contiguos (i,j) con >=2 valores no nulos
    spans = []
    for i in range(len(idx)):
        for j in range(i + 2, len(idx) + 1):
            if mask[i:j].sum() >= 2:
                spans.append((i, j))
    struct['spans'] = spans
    # colores
    cdict = {}
    for k, col in enumerate(cols):
        if mask[k]:
            cdict.setdefault(col, []).append(k)
    struct['colors'] = {col: np.array(ix) for col, ix in cdict.items() if len(ix) >= 2}
    # alternos
    alts = []
    for step in (2, 3):
        for start in range(step):
            ix = np.arange(start, len(idx), step)
            if 2 <= len(ix) < len(idx) and mask[ix].sum() >= 2:
                alts.append(ix)
    struct['alts'] = alts
    return struct

pre = {}
for i, u in U.iterrows():
    pre[(i, 'prev_l0')] = group_struct(u.kfg, u.grupo - 1, True)
    pre[(i, 'next_l0')] = group_struct(u.kfg, u.grupo + 1, True)
    pre[(i, 'prev_all')] = group_struct(u.kfg, u.grupo - 1, False)
    pre[(i, 'next_all')] = group_struct(u.kfg, u.grupo + 1, False)

# denominadores
DEN = {}
for fam in ['full_l0','contig_l0','color_l0','alt_l0','full_all','contig_all','color_all']:
    DEN[fam] = []
    for i, u in U.iterrows():
        if pd.isna(u.val):
            continue
        suf = '_all' if fam.endswith('_all') else '_l0'
        if pre[(i,'prev'+suf)]['n'] >= 2 or pre[(i,'next'+suf)]['n'] >= 2:
            DEN[fam].append(i)

def sum_idx(vals, mask, ix):
    v = vals[ix]
    return np.nansum(v), int((~np.isnan(v)).sum())

def eval_family(vals, fam):
    hits = {}
    suf = '_all' if fam.endswith('_all') else '_l0'
    for i in DEN[fam]:
        u = U.iloc[i]
        tv = u.val
        h = False
        for side in ['prev', 'next']:
            s = pre[(i, side + suf)]
            if s['n'] < 2:
                continue
            if fam.startswith('full'):
                v, k = sum_idx(vals, s['mask'], s['idx'])
                h = (k >= 2 and np.isclose(v, tv))
            elif fam.startswith('contig'):
                v = np.nan_to_num(vals[s['idx']], nan=0.0)
                cs = np.concatenate([[0.0], np.cumsum(v)])
                mk = np.concatenate([[0], np.cumsum(s['mask'])])
                for (a, b) in s['spans']:
                    if (mk[b] - mk[a]) >= 2 and np.isclose(cs[b] - cs[a], tv):
                        h = True; break
            elif fam.startswith('color'):
                for col, ix in s['colors'].items():
                    v, k = sum_idx(vals, s['mask'], s['idx'][ix])
                    if k >= 2 and np.isclose(v, tv):
                        h = True; break
            elif fam.startswith('alt'):
                for ix in s['alts']:
                    v, k = sum_idx(vals, s['mask'], s['idx'][ix])
                    if k >= 2 and np.isclose(v, tv):
                        h = True; break
            if h:
                break
        hits[i] = h
    return hits

def stats(hits):
    total = int(sum(hits.values()))
    byq = {}
    for i, h in hits.items():
        byq.setdefault(U.iloc[i].kfg, []).append(h)
    means = [np.mean(v) for v in byq.values()]
    return total, float(np.mean(means)), len(means)

# observado
obs = {}
for fam in DEN:
    h = eval_family(V, fam)
    obs[fam] = stats(h)
    print(fam, 'obs', obs[fam], 'den', len(DEN[fam]), flush=True)

# --- permutaciones ---
res = {fam: {'total': [], 'mean': []} for fam in DEN}
groups = {k: d for k, d in c.groupby('kfg')}
# indices por quipu para cada esquema
idxN1 = {k: d[(d['nivel'] == 0) & (~d['cuerda'].isin(top_names.get(k, set())))]['idx'].values
         for k, d in groups.items()}
idxN2 = {k: d[~d['cuerda'].isin(top_names.get(k, set()))]['idx'].values
         for k, d in groups.items()}

def shuffle_copy(idxmap):
    vals = V.copy()
    for k, idx in idxmap.items():
        v = vals[idx]
        m = ~np.isnan(v)
        vv = v[m].copy(); rng.shuffle(vv)
        vals[idx[m]] = vv
    return vals

t0 = time.time()
for perm in range(NPERM):
    v1 = shuffle_copy(idxN1)
    for fam in ['full_l0', 'contig_l0', 'color_l0', 'alt_l0']:
        st = stats(eval_family(v1, fam))
        res[fam]['total'].append(st[0]); res[fam]['mean'].append(st[1])
    v2 = shuffle_copy(idxN2)
    for fam in ['full_all', 'contig_all', 'color_all']:
        st = stats(eval_family(v2, fam))
        res[fam]['total'].append(st[0]); res[fam]['mean'].append(st[1])
    if (perm + 1) % 250 == 0:
        print('perm', perm + 1, 't=%.1fs' % (time.time() - t0), flush=True)

# --- resumen y Holm ---
summary = []
for fam in DEN:
    ot, om, nq = obs[fam]
    tt = np.array(res[fam]['total']); mm = np.array(res[fam]['mean'])
    p_total = (1 + np.sum(tt >= ot)) / (NPERM + 1)
    p_mean = (1 + np.sum(mm >= om)) / (NPERM + 1)
    summary.append(dict(familia=fam, n_unidades=len(DEN[fam]), n_quipus=nq,
                        obs_total=ot, obs_tasa=ot / len(DEN[fam]),
                        nulo_total_medio=float(tt.mean()),
                        nulo_total_p95=float(np.quantile(tt, .95)),
                        p_total=p_total, obs_media_quipu=om,
                        nulo_media_quipu=float(mm.mean()), p_media_quipu=p_mean))
S = pd.DataFrame(summary)
order = np.argsort(S['p_total'].values); prev = 0
for rank, j in enumerate(order):
    adj = min(1.0, (len(S) - rank) * S.loc[j, 'p_total'])
    prev = max(prev, adj)
    S.loc[j, 'p_holm'] = prev
S = S.sort_values('p_total')
S.to_csv(os.path.join(BASE, 'nulo_resumen.csv'), index=False)
np.save(os.path.join(BASE, 'nulo_totales.npy'),
        np.array([res[f]['total'] for f in DEN]))
print('\n', S.to_string(index=False), flush=True)
