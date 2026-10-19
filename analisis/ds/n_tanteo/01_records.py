# -*- coding: utf-8 -*-
"""Resumen estructural de los quipus del monton de mani (solo consola, nada de valores masivos)."""
import pandas as pd
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
Q = ['UR266','UR268','UR269','UR270','UR272','UR273A','UR273B','UR274A','UR274B',
     'UR275','UR276','UR277','UR278','UR279']
c = pd.read_csv('ds/n_okr_incahuasi/cuerdas_okr.csv')
d = c[c.kfg.isin(Q)].copy()

def rec(k):
    g = d[d.kfg == k]
    out = []
    for gr, gg in g.groupby('grupo'):
        col = gg[gg.nivel == 0].sort_values('orden')
        out.append((gr, col.valor.tolist(), col.color.tolist(), int((gg.nivel > 0).sum())))
    return out

if __name__ == '__main__':
    import sys
    k = sys.argv[1]
    for gr, vals, cols, ns in rec(k):
        print(f'g{gr}\tn={len(vals)}\tsub={ns}\t{vals}')
