# -*- coding: utf-8 -*-
"""Tabla de registros: por grupo, suma de colgantes y cabecera (primer colgante)."""
import pandas as pd
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
Q = ['UR266','UR268','UR269','UR270','UR272','UR273A','UR273B','UR274A','UR274B',
     'UR275','UR276','UR277','UR278','UR279']
c = pd.read_csv('ds/n_okr_incahuasi/cuerdas_okr.csv')
d = c[c.kfg.isin(Q)].copy()
d['valor'] = d.valor.fillna(0)

def grupos(k, nivel0=True):
    g = d[(d.kfg == k) & (d.nivel == 0)]
    out = []
    for gr, gg in g.groupby('grupo'):
        gg = gg.sort_values('orden')
        out.append(dict(kfg=k, grupo=int(gr), n=len(gg), suma=int(gg.valor.sum()),
                        cab=int(gg.valor.iloc[0]), vals=gg.valor.astype(int).tolist(),
                        cols=gg.color.tolist()))
    return pd.DataFrame(out).sort_values('grupo')

if __name__ == '__main__':
    import sys
    k = sys.argv[1]
    t = grupos(k)
    print(t[['grupo','n','cab','suma']].to_string(index=False))
