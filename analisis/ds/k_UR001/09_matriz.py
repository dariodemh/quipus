# -*- coding: utf-8 -*-
"""UR001. Matriz alineada de bloques PK (filas x columnas relativas)."""
import pandas as pd, numpy as np
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
pend=r[r.nivel==0].sort_values('orden').reset_index(drop=True)
pkpos=set(pend[pend.color=='PK'].orden.values)
segs=[]; cur=[]
for _,row in pend.iterrows():
    if row.orden in pkpos:
        if cur: segs.append(cur)
        cur=[]
    cur.append(dict(orden=int(row.orden),color=row.color,val=int(row.valor),union=row.union))
if cur: segs.append(cur)
blocks=[s for s in segs if len(s)>=15]
print('n bloques >=15:',len(blocks),'tamanos:',[len(b) for b in blocks])

W=18
print('\n=== MATRIZ DE VALORES (filas=bloques, col=posicion relativa 0..17; . = sin nudo) ===')
for i,b in enumerate(blocks):
    vals=['.' if c['val']==0 else str(c['val']) for c in b]
    vals+=['']*(W-len(vals))
    print('B%02d '%i+' '.join(f'{v:>5}' for v in vals[:W]))

print('\n=== MATRIZ DE COLOR (2 letras; PK=cuerda separadora) ===')
for i,b in enumerate(blocks):
    cs=[c['color'] for c in b]; cs+=['']*(W-len(cs))
    print('B%02d '%i+' '.join(f'{c:>5}' for c in cs[:W]))

# por columna: cuantas celdas con valor / color modal
print('\n=== por columna: prop. celdas con valor, valor moda ===')
for j in range(W):
    colvals=[b[j]['val'] for b in blocks if j<len(b) and b[j]['color']!='PK']
    if not colvals: continue
    rich=np.mean([v>0 for v in colvals])
    print(f'  col {j:2d}: n={len(colvals):2d} ricas={rich:.2f} val>0={sorted([v for v in colvals if v>0])[:8]}')
