"""UR1032 — secciones entre marcadores M1-M5; modulos de 8."""
import pandas as pd, numpy as np
C=pd.read_csv('analisis/datos/cuerdas.csv')
s=C[C.kfg=='UR1032'].copy().sort_values('orden').reset_index(drop=True)
col=s[s.nivel==0].reset_index(drop=True)
col['size']=col.groupby('grupo')['grupo'].transform('size')
col['rn']=np.arange(1,len(col)+1)  # ordinal de colgante 1..415

markers={'M1':'p58','M2':'p131','M3':'p204','M4':'p277','M5':'p342'}
print('grupos de los marcadores:')
for m,cr in markers.items():
    r=col[col.cuerda==cr]
    print(f'  {m} {cr}: grupo={int(r.grupo.iloc[0])}, size_grupo={int(r["size"].iloc[0])}, valor={r.valor.iloc[0]}')

# secciones por indice de colgante (1..415)
idx=[1]+[int(col[col.cuerda==c].rn.iloc[0]) for c in markers.values()]+[416]
print('\n== pendientes por seccion (entre marcadores) ==')
for i in range(len(idx)-1):
    a,b=idx[i],idx[i+1]
    n=b-a
    print(f'  seccion {i+1}: colgantes #{a}..#{b-1}  n={n}  ({n/8:.1f} modulos de 8)')

# composicion de cada seccion: cuantos grupos de 5 / 3 / singletons
print('\n== composicion por seccion ==')
secs=list(zip(idx[:-1],idx[1:]))
for i,(a,b) in enumerate(secs):
    sub=col[(col.rn>=a)&(col.rn<b)]
    vc=sub['size'].value_counts().to_dict()
    print(f'  sec{i+1}: {vc}, suma_valores={int(sub.valor.sum())}')
