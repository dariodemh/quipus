# -*- coding: utf-8 -*-
"""UR093: colores, pares (pos6,pos7), direccion de nudos, periodicidad."""
import pandas as pd, numpy as np, re
from collections import Counter
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
l0 = u[u.nivel == 0]; l1 = u[u.nivel == 1].copy()
l1['pos'] = l1.groupby('padre').cumcount() + 1

def base(c):
    if pd.isna(c): return 'NA'
    c = str(c).split('(')[0]
    return c
l1['col'] = l1.color.map(base)
# color primario (primer codigo antes de : - /)
def prim(c):
    return re.split(r'[:/\-]', c)[0] if c != 'NA' else 'NA'
l1['prim'] = l1.col.map(prim)
l0 = l0.assign(prim=l0.color.map(base).map(prim))

print('== pares pos6/pos7: misma familia de color? ==')
pares = []
for p, grp in l1[l1.pos.isin([6,7])].groupby('padre'):
    d = dict(zip(grp.pos, grp.col))
    if 6 in d and 7 in d:
        pares.append((p, d[6], d[7], prim(d[6]), prim(d[7])))
pp = pd.DataFrame(pares, columns=['padre','c6','c7','p6','p7'])
print('pares completos', len(pp), '| misma familia primaria', (pp.p6 == pp.p7).sum(),
      '| ambos no-W', ((pp.p6 != 'W') & (pp.p7 != 'W')).sum())
print('c6 blancos:', (pp.p6 == 'W').sum(), '| c7 blancos:', (pp.p7 == 'W').sum())
print('c7 contiene ":" (barber):', pp.c7.str.contains(':').sum())
print('\n== familias de color en pos6 ==')
print(pp.p6.value_counts().head(12).to_dict())

print('\n== fondos: color de colgantes ==')
def fam(c):
    c = str(c).split('(')[0]
    c = re.split(r'[:/\-]', c)[0]
    return {'W':'blanco','AB':'marron','MB':'marron','KB':'marron','YB':'amarillo','RB':'rojo','BG':'verde','VB':'verde','GG':'verde','PB':'azul','BL':'azul','RL':'rojo'}.get(c, 'otro')
u['fam'] = u.color.map(fam)
print(pd.crosstab(u.nivel, u.fam).to_string())

print('\n== direccion de nudos ==')
pat = re.compile(r'(\d*)([SLE]+)\(([\d.]+),([SZU])\)')
rows = []
for c, s in zip(u.cuerda, u.nudos):
    if pd.isna(s): continue
    for m in pat.finditer(str(s)):
        rows.append((c, nivel := int(u[u.cuerda == c].nivel.iloc[0]), m.group(1), m.group(2), float(m.group(3)), m.group(4), int(u[u.cuerda == c].valor.iloc[0])))
kn = pd.DataFrame(rows, columns=['cuerda','nivel','n','tipo','pos','dir','valor'])
print('clusters', len(kn))
print(pd.crosstab(kn.tipo.str[0], kn.dir).to_string())
print('\n-- direccion por nivel --')
print(pd.crosstab(kn.nivel, kn.dir).to_string())
print('\n-- direccion por valor (solo 1 nudo) --')
one = kn[kn.n == '1']
print(pd.crosstab(one.valor, one.dir).head(12).to_string())
print('\n-- posicion del nudo en la cuerda (cm) por nivel --')
print(kn.groupby('nivel').pos.describe()[['count','mean','50%','min','max']].round(1).to_string())

print('\n== periodicidad de color en colgantes: runs ==')
for g, grp in l0.groupby('grupo'):
    seq = grp.prim.tolist()
    runs = 1 + sum(1 for a, b in zip(seq, seq[1:]) if a != b)
    print(g, 'n', len(seq), 'runs', runs, '|', ''.join(x[0] for x in seq))
