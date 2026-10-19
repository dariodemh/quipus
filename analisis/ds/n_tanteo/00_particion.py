# -*- coding: utf-8 -*-
"""Fija la particion explorar/confirmar ANTES de mirar valores.
Unidad = registro (grupo de colgantes). Para quipus con un solo grupo,
la unidad es el colgante (por 'orden'). Division por BLOQUES contiguos
(la mitad inicial explora, la final confirma) porque el orden importa en
las hipotesis de libro/inventario (H-a, H-d).
"""
import pandas as pd
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

Q = ['UR266','UR268','UR269','UR270','UR272','UR273A','UR273B',
     'UR274A','UR274B','UR275','UR276','UR277','UR278','UR279']
c = pd.read_csv('ds/n_okr_incahuasi/cuerdas_okr.csv')
d = c[c.kfg.isin(Q)].copy()

rows = []
for k, g in d.groupby('kfg'):
    gs = (g.groupby('grupo')
            .agg(n=('cuerda','size'), omin=('orden','min'), omax=('orden','max'))
            .sort_index())
    if len(gs) >= 2:
        half = (len(gs) + 1) // 2
        for i, (gr, r) in enumerate(gs.iterrows()):
            rows.append([k, 'grupo', int(gr), int(r.n), float(r.omin), float(r.omax),
                         'explorar' if i < half else 'confirmar'])
    else:
        # un solo grupo: dividir colgantes por orden
        col = g[g.nivel == 0].sort_values('orden').reset_index(drop=True)
        half = (len(col) + 1) // 2
        for i, r in col.iterrows():
            rows.append([k, 'colgante', int(r.orden), 1, float(r.orden), float(r.orden),
                         'explorar' if i < half else 'confirmar'])

p = pd.DataFrame(rows, columns=['kfg','unidad','id','n_cuerdas','orden_min','orden_max','mitad'])
p.to_csv('ds/n_tanteo/particion.csv', index=False)
print(p.groupby(['kfg','mitad']).agg(uds=('id','size'), cuerdas=('n_cuerdas','sum')).to_string())
