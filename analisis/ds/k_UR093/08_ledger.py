# -*- coding: utf-8 -*-
"""UR093: ledger compacto + color posicional."""
import pandas as pd, numpy as np, re
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg=='UR093'].copy(); u['valor']=u.valor.fillna(0).astype(int)
l1=u[u.nivel==1].copy(); l1['pos']=l1.groupby('padre').cumcount()+1
sets=l1.groupby('padre').size(); sets=sets[sets>=7].index.tolist()
S=l1[l1.padre.isin(sets)]
lines=[]
for p in u[u.nivel==0].cuerda:
    r=u[u.cuerda==p].iloc[0]
    sub=l1[l1.padre==p]
    sv=' '.join(f'{int(x)}' for x in sub.valor)
    col6=S[(S.padre==p)&(S.pos==6)].color
    col7=S[(S.padre==p)&(S.pos==7)].color
    c6=col6.iloc[0] if len(col6) else '-'
    c7=col7.iloc[0] if len(col7) else '-'
    lines.append(f'g{int(r.grupo):>2} {p:<5} v={int(r.valor):<3} u={r.union} {str(r.color):<10} p6={str(c6):<10} p7={str(c7):<10} subs[{sv}]')
open('analisis/ds/k_UR093/ledger.txt','w',encoding='utf-8').write('\n'.join(lines))

# pos6 color por grupo
S2=S.copy()
S2['base6']=S2.color
c6tab=S2[S2.pos==6].groupby([u.set_index('cuerda').grupo.rename('g'),'color']).size()
# crosstab simple
tmp=S2[S2.pos==6].copy(); tmp['g']=tmp.padre.map(u.set_index('cuerda').grupo)
print('== pos6 color (top) global ==')
print(tmp.color.value_counts().head(12).to_dict())
print('\n== pos6 color por grupo (primeros) ==')
for g in sorted(tmp.g.unique()):
    print(g, tmp[tmp.g==g].color.value_counts().head(6).to_dict())
print('\n== union por grupo (R/V) ==')
n0=u[u.nivel==0].copy()
print(pd.crosstab(n0.grupo,n0.union).to_string())
print('\nunion total nivel0:',n0.union.value_counts().to_dict())
print('union nivel1:',u[u.nivel==1].union.value_counts().to_dict())
print('\nvalor por union (nivel0):')
print(n0.groupby('union').valor.agg(['count','mean','median','max']).to_string())
