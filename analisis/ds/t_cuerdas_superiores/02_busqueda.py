# -*- coding: utf-8 -*-
"""Busqueda exhaustiva de la relacion aritmetica de cada cuerda superior (union T, nivel 0).

Familias de candidatos, sobre las cuerdas que preceden a la superior:
  - grupo precedente completo (nivel 0 / todos los niveles)
  - cualquier sub-bloque contiguo (nivel 0 / orden fisico completo)
  - cualquier suma por color (nivel 0 / todos)
  - subconjuntos alternos (posiciones pares / impares)
  - grupo siguiente completo (por si la superior precede a su grupo)
"""
import pandas as pd, numpy as np, os, itertools, json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
c = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
c['sin_nudos'] = c['nudos'].isna() | (c['nudos'].astype(str).str.strip().isin(['', 'nan']))
c['val'] = c['valor'].astype(float)
c.loc[c['sin_nudos'] & (c['val'] == 0), 'val'] = np.nan
c = c.sort_values(['kfg', 'orden']).reset_index(drop=True)

def sumv(vals):
    v = np.array([x for x in vals if pd.notna(x)], dtype=float)
    return v.sum() if len(v) else np.nan

def contiguous_sums(vals, minlen=1):
    """Devuelve dict suma->lista de (i,j) para sub-bloques contiguos."""
    out = {}
    n = len(vals)
    for i in range(n):
        for j in range(i + minlen, n + 1):
            s = sumv(vals[i:j])
            if pd.notna(s):
                out.setdefault(round(s, 6), []).append((i, j))
    return out

def color_sums(df):
    out = {}
    for col, d in df.groupby('color'):
        s = sumv(d['val'])
        if pd.notna(s):
            out.setdefault(round(s, 6), []).append(col)
    return out

rows = []
for kfg, d in c.groupby('kfg'):
    T0 = d[(d['union'] == 'T') & (d['nivel'] == 0)]
    if len(T0) == 0:
        continue
    for _, t in T0.iterrows():
        # unidad superior: la propia cuerda y sus descendientes T
        unit_names = set([t['cuerda']])
        # hijos T por prefijo jerarquico
        for nm in d['cuerda']:
            if isinstance(nm, str) and nm.startswith(t['cuerda'] + 's'):
                unit_names.add(nm)
        unit = d[d['cuerda'].isin(unit_names)]
        other = d[~d['cuerda'].isin(unit_names)]
        before = other[other['orden'] < t['orden']]
        after = other[other['orden'] > t['orden']]
        gprev = t['grupo'] - 1
        gnext = t['grupo'] + 1
        prev = other[other['grupo'] == gprev]
        nxt = other[other['grupo'] == gnext]
        rec = dict(kfg=kfg, top=t['cuerda'], top_val=t['val'], grupo=t['grupo'],
                   color=t['color'], n_before=len(before), n_prev=len(prev),
                   prev_l0=sumv(prev[prev['nivel'] == 0]['val']),
                   prev_all=sumv(prev['val']),
                   next_l0=sumv(nxt[nxt['nivel'] == 0]['val']),
                   next_all=sumv(nxt['val']))
        tv = t['val']
        rec['hit_prev_l0'] = pd.notna(tv) and pd.notna(rec['prev_l0']) and np.isclose(tv, rec['prev_l0'])
        rec['hit_prev_all'] = pd.notna(tv) and pd.notna(rec['prev_all']) and np.isclose(tv, rec['prev_all'])
        rec['hit_next_l0'] = pd.notna(tv) and pd.notna(rec['next_l0']) and np.isclose(tv, rec['next_l0'])
        rec['hit_next_all'] = pd.notna(tv) and pd.notna(rec['next_all']) and np.isclose(tv, rec['next_all'])
        # sub-bloques contiguos en el grupo previo
        pl0 = prev[prev['nivel'] == 0].sort_values('orden')
        pa = prev.sort_values('orden')
        rec['hit_contig_prev_l0'] = False; rec['contig_prev_l0'] = ''
        rec['hit_contig_prev_all'] = False; rec['contig_prev_all'] = ''
        if pd.notna(tv):
            cs = contiguous_sums(list(pl0['val']))
            if round(tv, 6) in cs:
                rec['hit_contig_prev_l0'] = True
                i, j = cs[round(tv, 6)][0]
                rec['contig_prev_l0'] = f"{i}:{j} ({j-i} cuerdas)"
            cs2 = contiguous_sums(list(pa['val']))
            if round(tv, 6) in cs2:
                rec['hit_contig_prev_all'] = True
                i, j = cs2[round(tv, 6)][0]
                rec['contig_prev_all'] = f"{i}:{j} ({j-i} cuerdas)"
        # colores
        rec['hit_color_prev_l0'] = False; rec['color_prev_l0'] = ''
        rec['hit_color_prev_all'] = False; rec['color_prev_all'] = ''
        if pd.notna(tv):
            c1 = color_sums(pl0)
            if round(tv, 6) in c1:
                rec['hit_color_prev_l0'] = True
                rec['color_prev_l0'] = '|'.join(map(str, c1[round(tv, 6)]))
            c2 = color_sums(pa)
            if round(tv, 6) in c2:
                rec['hit_color_prev_all'] = True
                rec['color_prev_all'] = '|'.join(map(str, c2[round(tv, 6)]))
        # alternos nivel 0 en grupo previo
        rec['hit_alt_prev_l0'] = False; rec['alt_prev_l0'] = ''
        if pd.notna(tv) and len(pl0) >= 2:
            for par in (0, 1):
                v = pl0.iloc[par::2]['val']
                s = sumv(v)
                if pd.notna(s) and np.isclose(tv, s):
                    rec['hit_alt_prev_l0'] = True
                    rec['alt_prev_l0'] = f"inicio {par} ({len(v)} cuerdas)"
        # misma regla pero en TODO lo anterior (bloques contiguos de nivel 0)
        rec['hit_contig_before_l0'] = False; rec['contig_before_l0'] = ''
        if pd.notna(tv):
            bl0 = before[before['nivel'] == 0].sort_values('orden')
            cs = contiguous_sums(list(bl0['val']))
            if round(tv, 6) in cs:
                rec['hit_contig_before_l0'] = True
                ii = cs[round(tv, 6)]
                rec['contig_before_l0'] = f"{len(ii)} bloques; primero {ii[0][0]}:{ii[0][1]}"
        rows.append(rec)

res = pd.DataFrame(rows)
res.to_csv(os.path.join(BASE, 'tops_candidatos.csv'), index=False)
print('tops:', len(res), 'quipus:', res.kfg.nunique())
print('top_val no nulo:', res.top_val.notna().sum())
print('\n-- tasas sobre top_val no nulo --')
n = res.top_val.notna().sum()
for col in ['hit_prev_l0','hit_prev_all','hit_next_l0','hit_next_all',
            'hit_contig_prev_l0','hit_contig_prev_all','hit_color_prev_l0',
            'hit_color_prev_all','hit_alt_prev_l0','hit_contig_before_l0']:
    print(f'{col:28s} {res[col].sum():3d}/{n}  {100*res[col].sum()/n:5.1f}%')
print('\n-- coincidencias (solo filas con algun hit) --')
cols = ['kfg','top','top_val','grupo','prev_l0','prev_all','next_l0','next_all',
        'hit_prev_l0','hit_prev_all','hit_next_l0','hit_contig_prev_l0','contig_prev_l0',
        'hit_contig_prev_all','hit_color_prev_all','color_prev_all','hit_alt_prev_l0','alt_prev_l0']
m = res[res[[x for x in cols if x.startswith('hit_')]].any(axis=1)]
print(m[cols].to_string(max_colwidth=40))
