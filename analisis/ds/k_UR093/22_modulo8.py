# -*- coding: utf-8 -*-
"""UR093: modulo de 8 subsidiarias -- colores y valores por posicion."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
l0 = u[u.nivel == 0]; l1 = u[u.nivel == 1].copy()
l1['pos'] = l1.groupby('padre').cumcount() + 1

# normalizar color: parte antes de '(' y antes de ':'? dejamos tal cual
def norm(c):
    if pd.isna(c): return 'NA'
    c = str(c)
    return c.split('(')[0]
l1['col'] = l1.color.map(norm)

sub8 = l1[l1.padre.isin(l0.cuerda)]
print('== color por posicion, solo madres con >=8 subs ==')
madres8 = [p for p, s in l1.groupby('padre') if len(s) >= 8]
t = l1[l1.padre.isin(madres8)]
for p in range(1, 9):
    vc = t[t.pos == p].col.value_counts()
    print(p, 'n=', vc.sum(), '| W=', vc.get('W', 0), '| top:', vc.head(5).to_dict())

print('\n== secuencias de color completas (8 subs, colapsando W) ==')
seqs = {}
for p, grp in l1[l1.padre.isin(madres8)].groupby('padre'):
    grp = grp.sort_values('pos')
    s = '|'.join(grp.col.tolist()[:8])
    seqs[s] = seqs.get(s, 0) + 1
for s, n in sorted(seqs.items(), key=lambda x: -x[1])[:12]:
    print(n, s)

print('\n== valor>0 por posicion, solo 8-modulo ==')
for p in range(1, 9):
    v = t[t.pos == p].valor
    print(p, 'n>0', int((v > 0).sum()), '/', len(v), 'suma', int(v.sum()))

print('\n== madres por grupo: cuantas con 8 subs, cuantas sin ==')
l0 = l0.assign(con=l0.cuerda.isin(l1.padre), nsub=l0.cuerda.map(l1.groupby('padre').size()).fillna(0).astype(int))
print(l0.groupby('grupo').agg(pend=('cuerda','size'), con_sub=('con','sum'), nsub=('nsub','sum'),
                              v0=('valor','sum')).to_string())
print('\n== valores de colgantes por grupo (conteo 0/1/2/>=3) ==')
l0['cat'] = pd.cut(l0.valor, [-1,0,1,2,100], labels=['0','1','2','3+'])
print(pd.crosstab(l0.grupo, l0.cat).to_string())
print('\n== largo/terminacion/torsion de nivel0 por grupo (media largo) ==')
print(l0.groupby('grupo').largo.mean().round(1).to_dict())
print('terminaciones nivel0:', l0.terminacion.value_counts().to_dict())
print('colores nivel0 por grupo (top2):')
for g in sorted(l0.grupo.unique()):
    print(g, l0[l0.grupo == g].color.value_counts().head(2).to_dict())
