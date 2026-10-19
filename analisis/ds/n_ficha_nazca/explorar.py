"""Exploracion inicial: grupos de 9, marcadoras y atributos. Solo imprime resumenes cortos."""
import re, numpy as np, pandas as pd
from pathlib import Path
from collections import Counter

OUT = Path(__file__).resolve().parent
DAT = OUT.parents[1] / 'datos'
c = pd.read_csv(DAT / 'cuerdas.csv', low_memory=False).drop_duplicates(['kfg', 'cuerda'])
c['v'] = np.where(c.nudos.notna() & (c.nudos.astype(str).str.strip() != ''), c.valor, np.nan)
c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())
c['nudos'] = c.nudos.fillna('').astype(str)

def dirs(s):
    d = Counter(re.findall(r'\d+[SLE]+\([^,]*,\s*([SZU])\)', s))
    return ''.join(sorted(d)) or ''

for k in ['UR1140', 'UR1136', 'UR223', 'HP056', 'UR1176']:
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    print('\n===', k, 'nivel0:', len(d), 'grupos:', d.grupo.nunique())
    for g, dd in d.groupby('grupo', sort=False):
        if len(dd) != 9:
            continue
        cols = list(dd.col); cnt = Counter(cols); maj, nm = cnt.most_common(1)[0]
        if nm != 7:
            continue
        mk = dd[dd.col != maj]
        print(f"g{int(g):>2} maj={maj:<6} mix={tuple(i+1 for i,x in enumerate(cols) if x!=maj)!s:<8}",
              'v=', list(mk.v.round(1)), 'col=', list(mk.col), 'tor=', list(mk.torsion.fillna('?')),
              'uni=', list(mk.union.fillna('?')), 'dir=', [dirs(s) for s in mk.nudos],
              '| vals7=', list(dd[dd.col == maj].v.round(0)))
