# -*- coding: utf-8 -*-
"""Render compacto del quipu a un txt (para grep) y resumen de patrones."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].sort_values('orden').copy()
u['valor'] = u.valor.fillna(0)

lines=[]
for grp, sub in u.groupby('grupo'):
    lines.append(f'### GRUPO {grp}')
    for _, r in sub.iterrows():
        col = str(r.color)
        ind = '  '*int(r.nivel)
        v = int(r.valor)
        un = r.union
        lines.append(f'{ind}{r.cuerda:<8} v={v:<4} {col:<14} u={un}')
open('analisis/ds/k_UR093/render.txt','w',encoding='utf-8').write('\n'.join(lines))

# patron: subsidiarias por grupo
n0=u[u.nivel==0]
subs=u[u.nivel==1]
cnt=subs.groupby('padre').size()
n0=n0.assign(nsub=n0.cuerda.map(lambda p: cnt.get(p,0)))
print('== n subsidiarias por colgante, segun grupo ==')
print(pd.crosstab(n0.grupo, n0.nsub).to_string())
print('\n== valor colgante vs color (top) ==')
# color dominante por grupo
for grp,s in n0.groupby('grupo'):
    print(grp, 'n=',len(s),'valores:', s.valor.tolist())
