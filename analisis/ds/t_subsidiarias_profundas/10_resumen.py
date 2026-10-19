# -*- coding: utf-8 -*-
"""Resumen por quipu de las estructuras profundas."""
import pandas as pd, numpy as np, os
from collections import defaultdict

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
q = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'quipus.csv'))
T = pd.read_csv(os.path.join(OUT, 'arboles_tipos.csv'))
C = pd.read_csv(os.path.join(OUT, 'control_okr.csv'))
d['sin_nudos'] = d['nudos'].isna() | d['nudos'].astype(str).str.strip().isin(['', 'nan'])
d['v'] = d['valor'].astype(float)
d.loc[d['sin_nudos'] & (d['v'] == 0), 'v'] = np.nan

rows = []
for kfg, g in T.groupby('kfg'):
    sub = d[d.kfg == kfg]
    # duplicacion en aristas internas del arbol
    deep = set()
    gg = sub
    ch = defaultdict(list)
    for c, p in zip(gg.cuerda, gg.padre):
        if isinstance(p, str): ch[p].append(c)
    for r in g.raiz:
        st = [r]
        while st:
            x = st.pop(); deep.add(x); st += ch.get(x, [])
    V = dict(zip(gg.cuerda, gg.v))
    edges = [(p, k) for p in deep for k in ch.get(p, []) if k in deep]
    ev = [(V[p], V[k]) for p, k in edges if pd.notna(V[p]) and pd.notna(V[k])]
    dup = np.mean([abs(a - b) < 1e-9 for a, b in ev]) if ev else np.nan
    rows.append(dict(kfg=kfg, arboles=len(g), cuerdas=g.n.sum(), altura=int(g.altura.max()),
                     nivel3=int(g.n_nivel3.max()), n_cuerdas=len(sub),
                     dup=round(dup, 2) if pd.notna(dup) else np.nan,
                     tipos=';'.join(f'{k}:{v}' for k, v in g.tipo.value_counts().items())))
R = pd.DataFrame(rows).merge(q[['kfg', 'procedencia']], on='kfg', how='left')
R = R.merge(C[['kfg', 'estado']], on='kfg', how='left')
R['pct_cuerdas'] = 100 * R.cuerdas / R.n_cuerdas
R = R.sort_values(['nivel3', 'cuerdas'], ascending=False)
R.to_csv(os.path.join(OUT, 'resumen_quipus.csv'), index=False)
print('quipus:', len(R), '| arboles:', R.arboles.sum(), '| cuerdas:', R.cuerdas.sum())
print(R.head(18).to_string(index=False))
print('\nOKR:', R.estado.fillna('sin').value_counts().to_dict())
print('Incahuasi:', int(R.procedencia.astype(str).str.contains('Incahuasi').sum()))
