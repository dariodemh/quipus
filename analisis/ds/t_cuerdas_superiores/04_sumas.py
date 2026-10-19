# -*- coding: utf-8 -*-
"""Familias de suma para cada unidad de cuerda superior (union T / padres de T).

Familias evaluadas sobre el grupo adyacente (anterior y siguiente):
  full_l0      : todas las cuerdas nivel 0 del grupo
  full_all     : todas las cuerdas del grupo (todos los niveles)
  contig_l0    : cualquier sub-bloque contiguo (>=2 cuerdas) nivel 0
  contig_all   : cualquier sub-bloque contiguo (>=2) en orden fisico
  color_l0     : cualquier subconjunto definido por un color (>=2 cuerdas)
  color_all    : idem, todos los niveles
  alt_l0       : posiciones pares o impares (>=2 cuerdas), subconjunto propio
  alt3_l0      : cada 3.a posicion (>=2 cuerdas), subconjunto propio
"""
import pandas as pd, numpy as np, os, json

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

def contig_hit(vals, target, minlen=2):
    n = len(vals)
    for i in range(n):
        s = 0.0; k = 0
        for j in range(i, n):
            if pd.notna(vals[j]):
                s += vals[j]; k += 1
            if k >= minlen and np.isclose(s, target):
                return True, (i, j + 1)
    return False, None

def color_hit(df, target, minlen=2):
    for col, d in df.groupby('color'):
        if len(d) < minlen:
            continue
        s = sumv(d['val'])
        if pd.notna(s) and np.isclose(s, target):
            return True, str(col), len(d)
    return False, None, 0

def alt_hit(vals, target, step=2):
    n = len(vals)
    for start in range(step):
        idx = list(range(start, n, step))
        if len(idx) < 2 or len(idx) == n:
            continue
        s = sumv([vals[i] for i in idx])
        if pd.notna(s) and np.isclose(s, target):
            return True, start, len(idx)
    return False, None, 0

# ---- construir unidades ----
units = []
for kfg, d in c.groupby('kfg'):
    T = d[d['union'] == 'T']
    if len(T) == 0:
        continue
    l0 = d[d['nivel'] == 0]
    cand = set(l0[l0['union'] == 'T']['cuerda']) | set(T[T['nivel'] == 1]['padre'].dropna())
    for nm in cand:
        t = d[d['cuerda'] == nm].iloc[0]
        kids = d[d['padre'] == nm]
        units.append(dict(kfg=kfg, top=nm, top_val=t['val'], top_color=t['color'],
                          grupo=int(t['grupo']), orden=int(t['orden']),
                          n_kids=len(kids), n_kids_T=int((kids['union'] == 'T').sum()),
                          kids_sum=sumv(kids['val'])))
U = pd.DataFrame(units)

# ---- evaluar ----
rows = []
for _, u in U.iterrows():
    d = c[c['kfg'] == u.kfg]
    kids = d[d['padre'] == u.top]
    rec = u.to_dict()
    rec['top_val'] = u.top_val
    for side, gr in [('prev', u.grupo - 1), ('next', u.grupo + 1)]:
        g = d[d['grupo'] == gr]
        l0 = g[g['nivel'] == 0].sort_values('orden')
        vals = list(l0['val'])
        rec[f'{side}_n'] = len(l0)
        rec[f'{side}_sum'] = sumv(vals)
        rec[f'{side}_sum_all'] = sumv(g['val'])
        tv = u.top_val
        rec[f'{side}_full_l0'] = bool(pd.notna(tv) and len(l0) >= 2 and np.isclose(tv, rec[f'{side}_sum']))
        rec[f'{side}_full_all'] = bool(pd.notna(tv) and len(g) >= 2 and np.isclose(tv, rec[f'{side}_sum_all']))
        ok, span = contig_hit(vals, tv) if pd.notna(tv) else (False, None)
        rec[f'{side}_contig_l0'] = ok
        rec[f'{side}_contig_l0_span'] = span
        gv = list(g.sort_values('orden')['val'])
        ok2, span2 = contig_hit(gv, tv) if pd.notna(tv) else (False, None)
        rec[f'{side}_contig_all'] = ok2
        rec[f'{side}_contig_all_span'] = span2
        ok3, col3, n3 = color_hit(l0, tv) if pd.notna(tv) else (False, None, 0)
        rec[f'{side}_color_l0'] = ok3; rec[f'{side}_color_l0_name'] = col3; rec[f'{side}_color_l0_n'] = n3
        ok4, col4, n4 = color_hit(g, tv) if pd.notna(tv) else (False, None, 0)
        rec[f'{side}_color_all'] = ok4; rec[f'{side}_color_all_name'] = col4; rec[f'{side}_color_all_n'] = n4
        ok5, st5, n5 = alt_hit(vals, tv, 2) if pd.notna(tv) else (False, None, 0)
        rec[f'{side}_alt_l0'] = ok5; rec[f'{side}_alt_l0_start'] = st5
        ok6, st6, n6 = alt_hit(vals, tv, 3) if pd.notna(tv) else (False, None, 0)
        rec[f'{side}_alt3_l0'] = ok6; rec[f'{side}_alt3_l0_start'] = st6
    # cualquier lado
    for fam in ['full_l0','full_all','contig_l0','contig_all','color_l0','color_all','alt_l0','alt3_l0']:
        rec['any_' + fam] = bool(rec.get('prev_' + fam, False) or rec.get('next_' + fam, False))
    # hijos (solo si tiene >=2 hijos)
    rec['kids_full'] = bool(pd.notna(u.top_val) and u.n_kids >= 2 and np.isclose(u.top_val, u.kids_sum))
    rows.append(rec)

R = pd.DataFrame(rows)
R.to_csv(os.path.join(BASE, 'unidades_resultados.csv'), index=False)

ev = R[R.top_val.notna()].copy()
print('unidades con valor:', len(ev), 'quipus:', ev.kfg.nunique())
print('\n== tasas crudas por unidad (denominador: unidades con valor y >=2 cuerdas en el grupo) ==')
for fam in ['full_l0','full_all','contig_l0','contig_all','color_l0','color_all','alt_l0','alt3_l0']:
    den = 0; num = 0
    for _, r in ev.iterrows():
        okden = False
        for side in ['prev','next']:
            n = r.get(f'{side}_n', 0)
            if pd.notna(n) and n >= 2:
                okden = True
        if okden:
            den += 1; num += int(r['any_' + fam])
    print(f'{fam:12s} {num:3d}/{den:3d} = {100*num/den:5.1f}%')
print('\n== por lado, solo full_l0 (grupo >=2) ==')
for side in ['prev','next']:
    sub = ev[ev[f'{side}_n'] >= 2]
    print(f'{side}: {sub[f"{side}_full_l0"].sum()}/{len(sub)} = {100*sub[f"{side}_full_l0"].mean():.1f}%')
print('\n== coincidencias any_full_l0 o any_contig_l0 ==')
cols = ['kfg','top','top_val','grupo','prev_n','prev_sum','prev_full_l0','prev_contig_l0',
        'next_n','next_sum','next_full_l0','next_contig_l0','any_full_l0','any_contig_l0',
        'any_color_l0','any_alt_l0','kids_full']
print(R[R.any_full_l0 | R.any_contig_l0 | R.any_color_l0 | R.any_alt_l0 | R.kids_full][cols].to_string(max_colwidth=30))
