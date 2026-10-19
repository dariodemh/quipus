"""UR1032 — modulos (5 azul + 3 blanco), vectores, repeticiones, sumas por seccion."""
import pandas as pd, numpy as np
C=pd.read_csv('analisis/datos/cuerdas.csv')
s=C[C.kfg=='UR1032'].copy().sort_values('orden').reset_index(drop=True)
col=s[s.nivel==0].copy()
col['size']=col.groupby('grupo')['grupo'].transform('size')
col['pos']=col.groupby('grupo').cumcount()
col['rn']=np.arange(1,len(col)+1)

# construir modulos: emparejar grupo 5 seguido de grupo 3 (o 3 seguido de 5)
mods=[]
for gid in range(107):
    a=col[col.grupo==gid]; b=col[col.grupo==gid+1]
    sa,sb=len(a),len(b)
    if {sa,sb}=={5,3}:
        blue=a if sa==5 else b
        white=b if sa==5 else a
        mods.append((gid, gid+1, tuple(sorted(blue.sort_values('pos').valor.astype(int))),
                     tuple(sorted(white.sort_values('pos').valor.astype(int)))))
print('modulos (5azul+3blanco):', len(mods))
# repetidos
from collections import Counter
bv=Counter(m[2] for m in mods); wv=Counter(m[3] for m in mods)
print('vectores azules repetidos (top):', bv.most_common(6))
print('vectores blancos repetidos (top):', wv.most_common(6))
modall=Counter((m[2],m[3]) for m in mods)
print('modulos completos repetidos:', [k for k,v in modall.items() if v>1])

print('\n== suma por modulo (azul+blanco) ==')
ms=[sum(m[2])+sum(m[3]) for m in mods]
print('describe:', pd.Series(ms).describe().round(2).to_dict())
print('sumas:', ms)

# secciones
idx=[1,58,131,204,277,342,416]
print('\n== modulos por seccion y su suma ==')
for i in range(6):
    a,b=idx[i],idx[i+1]
    sub=col[(col.rn>=a)&(col.rn<b)]
    gids=sorted(sub.grupo.unique())
    # contar modulos dentro
    gset=set(gids)
    sz=col.groupby('grupo').size().to_dict()
    nm=0
    for gid in gids:
        if gid+1 in gset and {sz[gid],sz[gid+1]}=={5,3}:
            nm+=1
    print(f'sec{i+1}: n={b-a} grupos={len(gids)} modulos~{nm} suma_total={int(sub.valor.sum())}')
