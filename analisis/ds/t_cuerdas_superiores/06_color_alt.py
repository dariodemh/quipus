# -*- coding: utf-8 -*-
"""Controles especificos: subconjuntos POR COLOR (propios) y ALTERNOS.

Variantes:
  color_proper : grupo adyacente nivel 0; una clase de color con 2<=n<n_grupo
  color_top    : cuerdas del grupo adyacente cuyo color == color de la superior
  color_quipu  : todas las cuerdas nivel 0 del quipu de un mismo color (2<=n<total)
  color_quipu_top : todas las nivel 0 del quipu del color de la superior
  alt_l0       : posiciones pares/impares del grupo adyacente (subconjunto propio)
Nulo: permutacion de valores nivel 0 dentro del quipu.
"""
import pandas as pd, numpy as np, os, time

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
rng = np.random.default_rng(20261018)
NPERM = 1500

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
                          grupo=int(t['grupo']), color=str(t['color'])))
U = pd.DataFrame(units)

# estructuras
def gstruct(kfg, gr):
    d = c[(c['kfg'] == kfg) & (c['grupo'] == gr) & (c['nivel'] == 0)].sort_values('orden')
    return d

unit_struct = []
for i, u in U.iterrows():
    rec = dict(i=i, kfg=u.kfg, val=u.val, color=u.color,
               prev=gstruct(u.kfg, u.grupo - 1), next=gstruct(u.kfg, u.grupo + 1))
    # colores del quipu (nivel 0, sin unidades superiores)
    dq = c[(c['kfg'] == u.kfg) & (c['nivel'] == 0) & (~c['cuerda'].isin(top_names[u.kfg]))]
    rec['quipu_colors'] = {col: dq[dq['color'].astype(str) == col]['idx'].values
                           for col in dq['color'].astype(str).unique()}
    rec['quipu_n'] = len(dq)
    unit_struct.append(rec)

def sumv(vals, idx):
    v = vals[idx]
    return np.nansum(v), int((~np.isnan(v)).sum())

def eval_all(vals):
    out = {k: {} for k in ['color_proper', 'color_top', 'color_quipu', 'color_quipu_top', 'alt_l0']}
    for rec in unit_struct:
        tv = rec['val']
        if pd.isna(tv): continue
        hit = {k: False for k in out}
        # grupos adyacentes
        for side in ['prev', 'next']:
            g = rec[side]
            if len(g) < 2: continue
            n = len(g)
            # color propio
            for col, gd in g.groupby(g['color'].astype(str)):
                if 2 <= len(gd) < n:
                    s, k = sumv(vals, gd['idx'].values)
                    if k >= 2 and np.isclose(s, tv):
                        hit['color_proper'] = True
            # color de la superior
            gd = g[g['color'].astype(str) == rec['color']]
            if 2 <= len(gd) < n:
                s, k = sumv(vals, gd['idx'].values)
                if k >= 2 and np.isclose(s, tv):
                    hit['color_top'] = True
            # alternos
            for start in (0, 1):
                ix = np.arange(start, n, 2)
                if 2 <= len(ix) < n:
                    s, k = sumv(vals, g['idx'].values[ix])
                    if k >= 2 and np.isclose(s, tv):
                        hit['alt_l0'] = True
        # color en todo el quipu
        for col, ix in rec['quipu_colors'].items():
            if 2 <= len(ix) < rec['quipu_n']:
                s, k = sumv(vals, ix)
                if k >= 2 and np.isclose(s, tv):
                    hit['color_quipu'] = True
        ix = rec['quipu_colors'].get(rec['color'], np.array([], dtype=int))
        if 2 <= len(ix) < rec['quipu_n']:
            s, k = sumv(vals, ix)
            if k >= 2 and np.isclose(s, tv):
                hit['color_quipu_top'] = True
        for k in out:
            out[k][rec['i']] = hit[k]
    return out

def stats(h):
    byq = {}
    for i, v in h.items():
        byq.setdefault(U.iloc[i].kfg, []).append(v)
    return int(sum(h.values())), float(np.mean([np.mean(v) for v in byq.values()])), len(byq)

obs = eval_all(V)
for k, h in obs.items():
    print(k, 'obs', stats(h), 'den', len(h), flush=True)

# nulo N1
res = {k: {'total': [], 'mean': []} for k in obs}
groups = {k: d for k, d in c.groupby('kfg')}
idxN1 = {k: d[(d['nivel'] == 0) & (~d['cuerda'].isin(top_names.get(k, set())))]['idx'].values
         for k, d in groups.items()}
t0 = time.time()
for perm in range(NPERM):
    vals = V.copy()
    for k, idx in idxN1.items():
        v = vals[idx]; m = ~np.isnan(v)
        vv = v[m].copy(); rng.shuffle(vv); vals[idx[m]] = vv
    e = eval_all(vals)
    for k, h in e.items():
        st = stats(h); res[k]['total'].append(st[0]); res[k]['mean'].append(st[1])
    if (perm + 1) % 250 == 0:
        print('perm', perm + 1, 't=%.1f' % (time.time() - t0), flush=True)

rows = []
for k, h in obs.items():
    ot, om, nq = stats(h)
    tt = np.array(res[k]['total']); mm = np.array(res[k]['mean'])
    rows.append(dict(familia=k, n=len(h), obs=ot, tasa=ot/len(h),
                     nulo=np.mean(tt), p=(1+np.sum(tt>=ot))/(NPERM+1),
                     media_q=om, nulo_media_q=np.mean(mm),
                     p_media_q=(1+np.sum(mm>=om))/(NPERM+1)))
S = pd.DataFrame(rows); S.to_csv(os.path.join(BASE, 'color_alt_resumen.csv'), index=False)
print('\n', S.to_string(index=False))
