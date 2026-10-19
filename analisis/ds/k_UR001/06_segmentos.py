# -*- coding: utf-8 -*-
"""UR001. Segmentacion por cuerdas PK (separadores?). Bloques, tamanos, dobles bloques."""
import pandas as pd, numpy as np, json
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
pend=r[r.nivel==0].sort_values('orden').reset_index(drop=True)
rng=np.random.default_rng(0)

print('=== cuerdas PK ===')
pk=pend[pend.color=='PK']
print('total PK:',len(pk),'| sin nudos:',pk.nudos.isna().sum(),'| union:',pk.union.value_counts().to_dict())
print('posiciones (orden) PK:', list(pk.orden.astype(int)))
# PK tambien fuera de nivel 0?
print('PK en todo el quipu:', (r.color=='PK').sum())

# segmentos entre PK
pos=list(pk.orden.astype(int)); seq=list(pend.orden.astype(int))
segs=[]; cur=[]
for o in seq:
    if o in pos:
        if cur: segs.append(cur); cur=[]
        cur=[o]
    else:
        cur.append(o)
if cur: segs.append(cur)
print('\n=== segmentos delimitados por PK ===')
print('n segmentos:',len(segs))
lens=[len(s) for s in segs]
print('tamanos:',lens)
big=[l for l in lens if l>1]
print('tamanos>1:',len(big),'| media',np.mean(big).round(1),'| mediana',np.median(big),'| rango',min(big),max(big))
print('suma:',sum(lens))

# tamano sin contar el PK inicial
print('\ntamano del bloque SIN el PK:',[l-1 for l in lens if l>1])

# cada segmento empieza por PK?
print('\n=== el PK encabeza bloque? cuantos segmentos empiezan con PK:', sum(1 for s in segs if pend.set_index("orden").color[s[0]]=='PK'))
