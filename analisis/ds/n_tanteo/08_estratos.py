# -*- coding: utf-8 -*-
"""Post hoc: la identidad cabecera=suma(resto) por numero de destinos.
Control del confusor: la mitad de confirmacion tiene registros mas simples."""
import pandas as pd, numpy as np
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
Q = ['UR266','UR268','UR269','UR270','UR272','UR273A','UR273B','UR274A','UR274B',
     'UR275','UR276','UR277','UR278','UR279']
c = pd.read_csv('ds/n_okr_incahuasi/cuerdas_okr.csv'); c['valor'] = c.valor.fillna(0)
c = c[c.kfg.isin(Q)]
part = pd.read_csv('ds/n_tanteo/particion.csv')
TAG = {(r.kfg, int(r.id)): r.mitad for _, r in part[part.unidad == 'grupo'].iterrows()}

rows = []
for k in ['UR275', 'UR269']:
    g = c[(c.kfg == k) & (c.nivel == 0)]
    for gr, gg in g.groupby('grupo'):
        v = gg.sort_values('orden').valor.astype(int).tolist()
        if len(v) < 2 or v[0] <= 0:
            continue
        nd = len(v) - 1
        resto = sum(v[1:])
        rows.append(dict(quipu=k, grupo=int(gr), mitad=TAG.get((k, int(gr))),
                         n_destinos=nd, cabecera=v[0], resto=resto,
                         exacto=int(v[0] == resto),
                         rel=abs(v[0] - resto) / v[0]))
t = pd.DataFrame(rows)
t.to_csv('ds/n_tanteo/estratos.csv', index=False)
print(t.groupby(['quipu', 'mitad', 'n_destinos']).agg(
    registros=('exacto', 'size'), exactos=('exacto', 'sum'),
    dentro5=('rel', lambda s: int((s < 0.05).sum()))).to_string())
print('\nSolo registros con >=3 destinos (los informativos):')
print(t[t.n_destinos >= 3].groupby(['quipu', 'mitad']).agg(
    registros=('exacto', 'size'), exactos=('exacto', 'sum'),
    dentro5=('rel', lambda s: int((s < 0.05).sum()))).to_string())
