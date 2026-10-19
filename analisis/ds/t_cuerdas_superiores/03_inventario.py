# -*- coding: utf-8 -*-
"""Inventario completo de unidades de cuerda superior.

Una unidad = cuerda de nivel 0 que (a) tiene union T, o (b) tiene al menos un
hijo de nivel 1 con union T.  Los hijos T son los colgantes que cuelgan de ella.
"""
import pandas as pd, numpy as np, os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
c['sin_nudos'] = c['nudos'].isna() | (c['nudos'].astype(str).str.strip().isin(['', 'nan']))
c['val'] = c['valor'].astype(float)
c.loc[c['sin_nudos'] & (c['val'] == 0), 'val'] = np.nan
c = c.sort_values(['kfg', 'orden']).reset_index(drop=True)

def sumv(v):
    a = np.array([x for x in v if pd.notna(x)], float)
    return a.sum() if len(a) else np.nan

rows = []
for kfg, d in c.groupby('kfg'):
    T = d[d['union'] == 'T']
    if len(T) == 0:
        continue
    l0 = d[d['nivel'] == 0]
    # candidatos: nivel0 con union T
    cand = set(l0[l0['union'] == 'T']['cuerda'])
    # o nivel0 con hijos nivel1 T
    parents = set(T[T['nivel'] == 1]['padre'].dropna())
    cand |= parents
    for nm in sorted(cand, key=lambda x: d[d['cuerda'] == x]['orden'].iloc[0]):
        t = d[d['cuerda'] == nm].iloc[0]
        kids = d[d['padre'] == nm]
        kT = kids[kids['union'] == 'T']
        # grupo propio y vecinos
        own = d[d['grupo'] == t['grupo']]
        prev = d[d['grupo'] == t['grupo'] - 1]
        nxt = d[d['grupo'] == t['grupo'] + 1]
        rows.append(dict(
            kfg=kfg, top=nm, top_val=t['val'], top_color=t['color'],
            top_union=t['union'], grupo=t['grupo'],
            n_kids=len(kids), n_kids_T=len(kT),
            kids_sum=sumv(kids['val']), kidsT_sum=sumv(kT['val']),
            own_n=len(own), own_l0n=len(own[own['nivel'] == 0]),
            own_l0_sum=sumv(own[own['nivel'] == 0]['val']),
            own_all_sum=sumv(own['val']),
            prev_l0_sum=sumv(prev[prev['nivel'] == 0]['val']),
            prev_all_sum=sumv(prev['val']),
            next_l0_sum=sumv(nxt[nxt['nivel'] == 0]['val']),
            next_all_sum=sumv(nxt['val']),
            kids_vals=';'.join(f"{r.cuerda}={r.val:g}" for r in kids.itertuples() if pd.notna(r.val)),
            prev_vals=';'.join(f"{r.cuerda}={r.val:g}" for r in prev.sort_values('orden').itertuples() if pd.notna(r.val)),
        ))
inv = pd.DataFrame(rows)
inv['hit_kids'] = np.isclose(inv.top_val, inv.kids_sum)
inv['hit_kidsT'] = np.isclose(inv.top_val, inv.kidsT_sum)
inv['hit_prev'] = np.isclose(inv.top_val, inv.prev_l0_sum)
inv['hit_prev_all'] = np.isclose(inv.top_val, inv.prev_all_sum)
inv['hit_next'] = np.isclose(inv.top_val, inv.next_l0_sum)
inv.to_csv(os.path.join(BASE, 'inventario_tops.csv'), index=False)
print('unidades:', len(inv), 'quipus:', inv.kfg.nunique())
print('con valor:', inv.top_val.notna().sum())
print(inv.groupby('kfg').size().to_string())
print('\nhits: kids %d  kidsT %d  prev %d  prev_all %d  next %d' % (
    inv.hit_kids.sum(), inv.hit_kidsT.sum(), inv.hit_prev.sum(),
    inv.hit_prev_all.sum(), inv.hit_next.sum()))
print('\nunidades sin hijos T (posibles sumarias de grupo):')
print(inv[inv.n_kids_T == 0][['kfg','top','top_val','grupo','prev_l0_sum','prev_all_sum',
                              'hit_prev','hit_prev_all','next_l0_sum','hit_next']].to_string())
