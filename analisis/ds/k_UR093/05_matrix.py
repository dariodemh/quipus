# -*- coding: utf-8 -*-
"""UR093: matriz de subsidiarias por posicion."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg=='UR093'].copy()
u['valor']=u.valor.fillna(0)
lvl1=u[u.nivel==1].copy()
# posicion dentro de la madre
lvl1['pos']=lvl1.groupby('padre').cumcount()+1
cnt=lvl1.groupby('padre').size()
padres=lvl1.groupby('padre').size()
# pendantes con set (>=7 subs)
sets=cnt[cnt>=7].index
print('pendantes con set (>=7 subs):',len(sets),'tam:',cnt[cnt>=7].value_counts().to_dict())
S=lvl1[lvl1.padre.isin(sets)].copy()

# matriz de valores: fila=padre, col=pos
V=S.pivot_table(index='padre',columns='pos',values='valor',aggfunc='sum',fill_value=np.nan)
print('\n== valores por posicion: no-cero y suma ==')
for p in sorted(V.columns):
    col=V[p]
    print(f'pos{p}: n={col.notna().sum()} noCero={int((col>0).sum())} suma={int(col.sum(skipna=True))} vals={sorted(col.dropna().unique().astype(int).tolist())}')

# colores por posicion: cuantos NO blancos (no empieza por W ni es W)
def esblanco(c):
    if pd.isna(c): return True
    return str(c).startswith('W') or str(c)=='W'
print('\n== color no-blanco por posicion ==')
for p in sorted(S.pos.unique()):
    s=S[S.pos==p]
    nb=(~s.color.map(esblanco)).sum()
    print(f'pos{p}: n={len(s)} noBlanco={nb} ejemplos={s[~s.color.map(esblanco)].color.head(4).tolist()}')
