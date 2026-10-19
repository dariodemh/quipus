# -*- coding: utf-8 -*-
"""UR093: parseo de nudos (tipos, direcciones) y patrones."""
import pandas as pd, numpy as np, re
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg=='UR093'].copy()

rows=[]
for _,r in u.iterrows():
    if pd.isna(r.nudos): continue
    for cl in str(r.nudos).split(';'):
        m=re.match(r'\s*(\d+)([A-Z]+)\(([\d.]+),([SZU])\)(?:,([\d.]+))?', cl)
        if m:
            n,tipo,pos,dirn,val=m.groups()
            rows.append((r.cuerda,int(r.nivel),tipo,int(n),float(pos),dirn,float(val) if val else None))
K=pd.DataFrame(rows,columns=['cuerda','nivel','tipo','n','pos','dir','val'])
print('total racimos:',len(K))
print('tipos:',K.tipo.value_counts().to_dict())
print('direcciones:',K.dir.value_counts().to_dict())
print('n por nivel:',K.nivel.value_counts().to_dict())
# direccion por tipo
print('\ndir x tipo:'); print(pd.crosstab(K.tipo,K.dir).to_string())
# direccion de nudos largos (unidades)
print('\n--- L/E largos: donde estan las decenas vs unidades ---')
print('pos<  promedio por tipo:'); print(K.groupby('tipo').pos.describe()[['count','min','max']].to_string())

# cuerdas sin nudos y con nudos
u['tiene']=u.nudos.notna()
print('\n== estructura de cuerdas con/sin nudos por nivel ==')
print(pd.crosstab(u.nivel,u.tiene).to_string())
# direccion de la torsion vs union
print('\ntorsion x union:'); print(pd.crosstab(u.torsion,u.union,dropna=False).to_string())
# notar que 2 torsion nan
nan_t = u[u.torsion.isna()]
print('cuerdas sin torsion:', nan_t[['cuerda','valor','color','union','nudos']].to_string())
