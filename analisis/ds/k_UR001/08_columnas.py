# -*- coding: utf-8 -*-
"""UR001. Alineacion de bloques PK: patron interno de color y valor (filas/columnas)."""
import pandas as pd, numpy as np
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
pend=r[r.nivel==0].sort_values('orden').reset_index(drop=True)
pkpos=set(pend[pend.color=='PK'].orden.values)
# segmentos (solo bloques grandes)
segs=[]; cur=[]
for _,row in pend.iterrows():
    if row.orden in pkpos:
        if cur: segs.append(cur)
        cur=[]
        cur.append(('PK',row.color,int(row.valor)))  # placeholder PK
    else:
        cur.append(('',row.color,int(row.valor)))
if cur: segs.append(cur)
blocks=[s for s in segs if len(s)>1]
print('bloques:',len(blocks),'tamanos:',[len(b) for b in blocks])

# imprimir color+valor de bloques de 17
print('\n=== color de bloques (secuencia) ===')
for i,b in enumerate(blocks):
    if len(b) in (16,17,18):
        print(f'B{i} n={len(b)}:',''.join(f'{c[:2]:>3}' for _,c,_ in b))
print('\n=== valor de bloques (>0) ===')
for i,b in enumerate(blocks):
    if len(b) in (16,17,18):
        vals=['.' if v==0 else str(v) for _,_,v in b]
        print(f'B{i}:','|'.join(vals))
