"""Exploracion de UR234 (grupos de 8), UR1131 (grupos de 10), UR278 (Incahuasi),
Santa (UR087-092) y tasa base de 'primera cuerda = maximo'."""
import numpy as np, pandas as pd
from collections import Counter
from lib import load, records, canon, prof, OUT, DAT

c = load()
print('== UR234 (8) / UR1131 (10) / UR278 ==')
for k, size in [('UR234', 8), ('UR1131', 10), ('UR278', 9)]:
    d = c[(c.kfg == k) & (c.nivel == 0)]
    print(f'\n{k}: nivel0={len(d)}, grupos={d.grupo.nunique()}, tamanos={dict(Counter(d.groupby("grupo").size()))}')
    qq = pd.read_csv(DAT / 'quipus.csv')
    q = qq[qq.kfg == k]
    print('  museo/procedencia:', q.museo.iloc[0], '|', q.procedencia.iloc[0], '| region:', q.region.iloc[0])

print('\n== detalle UR234 (grupos de 8) ==')
for r in records(c, 'UR234', size=8):
    print(f"g{r['g']:>2} maj={r['maj']:<4} pos={r['pos']} v={np.round(r['vals'],0)} "
          f"marc={r['mcol']} v={np.round(r['mval'],0)}")

print('\n== detalle UR1131 (grupos de 10) ==')
for r in records(c, 'UR1131', size=10):
    print(f"g{r['g']:>2} maj={r['maj']:<4} pos={r['pos']} v={np.round(r['vals'],0)} "
          f"marc={r['mcol']} v={np.round(r['mval'],0)}")

print('\n== UR278: primeras 6 filas de grupos ==')
d = c[(c.kfg == 'UR278') & (c.nivel == 0)].sort_values('orden')
for g, dd in list(d.groupby('grupo', sort=False))[:4]:
    print('g', g, 'n', len(dd), 'colores', list(dd.col), 'v', list(dd.v.fillna(-1).round(0)))

print('\n== Santa: estructura de UR087 ==')
d = c[(c.kfg == 'UR087') & (c.nivel == 0)].sort_values('orden')
print('nivel0', len(d), 'grupos', d.grupo.nunique(), 'tamanos', dict(Counter(d.groupby('grupo').size())))
print('colores por grupo (primeros 5):')
for g, dd in list(d.groupby('grupo', sort=False))[:5]:
    print('g', g, 'n', len(dd), list(dd.col), list(dd.v.fillna(-1).round(0)))

print('\n== TASA BASE: primera cuerda = maximo, en grupos de 8/9/10 de todo el corpus ==')
for size in [8, 9, 10]:
    tot = 0; hit = 0; quipus = 0
    for k, dd in c[(c.nivel == 0)].groupby('kfg'):
        for g, gg in dd.groupby('grupo', sort=False):
            if len(gg) != size:
                continue
            v = gg.sort_values('orden').v.to_numpy(float)
            if np.isnan(v).any() or np.ptp(v) == 0:
                continue
            tot += 1; hit += int(np.argmax(v) == 0)
    print(f'size {size}: {hit}/{tot} = {hit/tot:.3f} de los grupos tienen maximo en la posicion 1')
