# -*- coding: utf-8 -*-
"""UR001. Sumas a nivel de grupo (nulo), estructura de grupos grandes, histograma."""
import pandas as pd, numpy as np, json
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
pend=r[r.nivel==0].sort_values('orden').reset_index(drop=True)
rng=np.random.default_rng(0); NPERM=1000

print('=== histograma de valores (colgantes) ===')
bins=[-1,0,10,100,1000,10000]
lab=['0(sin nudo)','1-10','11-100','101-1000','>1000']
c=pd.cut(pend.valor,bins=bins,labels=lab)
print(c.value_counts().reindex(lab).to_string())

print('\n=== TEST: en cada grupo, existe una cuerda = suma de las demas? ===')
def group_match(df):
    hits=0; ev=0
    for g,sub in df.groupby('grupo'):
        vs=sub[sub.valor>0].valor.values
        if len(vs)<2: continue
        ev+=1
        tot=vs.sum()
        # una cuerda = suma de las otras <=> su valor = tot/2
        if np.isclose(tot/2, vs).any(): hits+=1
    return hits,ev
h,e=group_match(pend)
print(f'  obs: {h}/{e} grupos')
null=[]
for _ in range(NPERM):
    p2=pend.copy(); p2['valor']=rng.permutation(p2.valor.values)
    null.append(group_match(p2)[0])
null=np.array(null)
print(f'  nulo media={null.mean():.1f} max={null.max()}; p={ (np.sum(null>=h)+1)/(NPERM+1):.3f}')

print('\n=== TEST 2: primer colgante del grupo = suma del resto? ===')
def first_is_sum(df):
    hits=0;ev=0
    for g,sub in df.groupby('grupo'):
        vs=sub.sort_values('orden').valor.values
        if vs[0]>0 and len(vs)>1 and vs[1:].sum()>0:
            ev+=1
            if vs[0]==vs[1:].sum(): hits+=1
    return hits,ev
h,e=first_is_sum(pend); print(f'  obs: {h}/{e}')

print('\n=== GRUPO 29 (34 colgantes) ===')
s=pend[pend.grupo==29]
print(f'  valores={list(s.valor.astype(int))}')
print(f'  colores={list(s.color)}')
print('  primeros 12:')
print(s[['orden','cuerda','valor','color','union']].head(12).to_string(index=False))
