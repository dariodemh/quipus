# -*- coding: utf-8 -*-
"""UR093: perfil de colgantes y subsidiarias; posiciones y valores."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
l1 = u[u.nivel == 1].copy(); l0 = u[u.nivel == 0].copy()
l1['pos'] = l1.groupby('padre').cumcount() + 1

print('== VALORES nivel0 ==')
print(l0.valor.value_counts().sort_index().to_dict())
print('\n== VALORES nivel1 (subs) ==')
print(l1.valor.value_counts().sort_index().to_dict())
print('\n== valor de la sub por posicion (media, n, %>0) ==')
print(l1.groupby('pos').valor.agg(['count','mean','max']).round(2).to_string())
print('\n== % de nivel1 sin nudos por posicion ==')
tmp = l1.assign(sn=l1.nudos.isna())
print(tmp.groupby('pos').sn.mean().round(2).to_dict())
print('\n== colores mas frecuentes por posicion (top1/2) ==')
for p in range(1, 11):
    s = l1[l1.pos == p].color.value_counts().head(3)
    if len(s): print(p, s.to_dict())
print('\n== pendantes con 8 subs: ejemplo primeras 3 (cuerda,valor,color + subs v/c) ==')
for p in l0.cuerda[l0.cuerda.isin(l1.padre)][:4]:
    row = l0[l0.cuerda == p].iloc[0]
    print(p, row.valor, row.color, row.nudos, '|',
          [(r.valor, r.color, r.nudos) for r in l1[l1.padre == p].itertuples()])
print('\n== nivel2: madres y valores ==')
l2 = u[u.nivel == 2]
print(l2.groupby('padre').agg(n=('cuerda','size'), suma=('valor','sum')).to_string())
print('\n== pendantes sin subs: valores ==')
sin = l0[~l0.cuerda.isin(l1.padre)]
print(sin.valor.value_counts().sort_index().to_dict())
print('\n== cords con nudos: distribucion del numero de clusters ==')
nk = u.nudos.fillna('').apply(lambda s: len([x for x in s.split(';') if x]))
print(nk.value_counts().sort_index().to_dict())
