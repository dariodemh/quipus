# -*- coding: utf-8 -*-
"""UR001. Periodicidad: tamanos de grupo, run-length de color/union, singletons."""
import pandas as pd, numpy as np
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
pend=r[r.nivel==0].sort_values('orden').reset_index(drop=True)

print('=== tamanos de grupo de colgantes (orden) ===')
sizes=pend.groupby('grupo').size().sort_index()
print(list(sizes.values))
print('n grupos:',len(sizes),'| bloques(>1):',(sizes>1).sum(),'| singletons:',(sizes==1).sum())
print('suma de bloques>1:',sizes[sizes>1].sum(),'| suma singletons:',sizes[sizes==1].sum())

print('\n=== RLE de color sobre colgantes ===')
def rle(seq):
    out=[]; 
    for x in seq:
        if out and out[-1][0]==x: out[-1][1]+=1
        else: out.append([x,1])
    return out
cr=rle(pend.color.tolist())
print('n runs color:',len(cr),'| largos:',[l for _,l in cr][:40])
print('moda de longitud de run:',pd.Series([l for _,l in cr]).mode().tolist())

print('\n=== RLE de union ===')
ur=rle(pend.union.tolist())
print('n runs:',len(ur),'|', [(c,l) for c,l in ur][:30])

print('\n=== singletons: que son? ===')
sing=sizes[sizes==1].index
sg=pend[pend.grupo.isin(sing)]
print('union:',sg.union.value_counts().to_dict())
print('color:',sg.color.value_counts().head(6).to_dict())
print('con nudos:',sg.nudos.notna().sum(),'/',len(sg))
print('ejemplos:',sg[['cuerda','valor','color','union']].head(12).to_dict('records'))

print('\n=== bloques: primeros valores de cada bloque grande ===')
for g in sizes[sizes>1].index[:8]:
    sub=pend[pend.grupo==g]
    print(f'  g{g} n={len(sub)} primeros vals={list(sub.valor.head(6).astype(int))} union={list(sub.union.head(6))} color={list(sub.color.head(6))}')
