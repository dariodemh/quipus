# -*- coding: utf-8 -*-
"""Selecciona los 10 casos mas extremos (una estructura por quipu) y vuelca
el detalle cuerda por cuerda a extremos.txt. Tambien calcula rasgos de color,
longitud y valores por nivel.

Salida: extremos.txt, casos10.csv
"""
import pandas as pd, numpy as np, os
from collections import defaultdict

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')

d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
d['sin_nudos'] = d['nudos'].isna() | d['nudos'].astype(str).str.strip().isin(['', 'nan'])
d['v'] = d['valor'].astype(float)
d.loc[d['sin_nudos'] & (d['v'] == 0), 'v'] = np.nan
T = pd.read_csv(os.path.join(OUT, 'arboles.csv'))
R = pd.read_csv(os.path.join(OUT, 'forma_arboles.csv'))

# ranking: n_nivel3, luego n, una por quipu
rank = T.sort_values(['n_nivel3', 'n'], ascending=False)
sel = []; seen = set()
for _, r in rank.iterrows():
    if r.kfg in seen: continue
    seen.add(r.kfg); sel.append(r)
    if len(sel) == 10: break

lines = []
casos = []
for r in sel:
    kfg, raiz = r.kfg, r.raiz
    g = d[d.kfg == kfg]
    ch = defaultdict(list)
    for c, p in zip(g['cuerda'], g['padre']):
        if isinstance(p, str): ch[p].append(c)
    nodes = [raiz]; q = [raiz]
    while q:
        x = q.pop()
        for k in ch.get(x, []):
            nodes.append(k); q.append(k)
    sub = g[g.cuerda.isin(nodes)].copy()
    sub['rel'] = sub['nivel'] - int(sub.loc[sub.cuerda == raiz, 'nivel'].iloc[0])
    pr = R[(R.kfg == kfg) & (R.raiz == raiz)]
    pA = float(pr.pA.iloc[0]) if len(pr) else float('nan')
    casos.append(dict(kfg=kfg, raiz=raiz, n=r.n, altura=r.altura, nivel3=r.n_nivel3,
                      pA=pA, grado_max=r.grado_max, frac_cadena=round(r.frac_cadena, 2),
                      n_con_valor=r.n_con_valor, ancho=r.ancho_niveles))
    lines.append(f'\n===== {kfg} / {raiz}  n={r.n} altura={r.altura} nivel>=3={r.n_nivel3} '
                 f'pA={pA:.3f} =====')
    lines.append('cuerda | niv | valor | color | largo | union | nudos')
    for _, x in sub.sort_values('orden').iterrows():
        v = '' if pd.isna(x.v) else ('%g' % x.v)
        lines.append('  ' * int(x.rel) + f"{x.cuerda} | {int(x.rel)} | {v} | {x.color} | "
                     f"{x.largo} | {x.union} | {str(x.nudos)[:40]}")
    # rasgos por nivel
    lines.append('  -- por nivel relativo: n, con valor, largo medio, colores distintos')
    for lv, gg in sub.groupby('rel'):
        lines.append(f'     {int(lv)}: n={len(gg)}, valor={int(gg.v.notna().sum())}, '
                     f'largo={gg.largo.mean():.1f}, colores={gg.color.nunique()}')

open(os.path.join(OUT, 'extremos.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
pd.DataFrame(casos).to_csv(os.path.join(OUT, 'casos10.csv'), index=False)
print(pd.DataFrame(casos).to_string(index=False))
print('\nextremos.txt lineas:', len(lines))
