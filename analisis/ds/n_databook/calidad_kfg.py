#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calidad interna de los nudos de KFG frente a su propio valor."""
import os
import pandas as pd
from decoder import decode

BASE = os.path.dirname(os.path.abspath(__file__))
D = lambda *a: os.path.join(BASE, *a)

kf = pd.read_csv(D('..', '..', 'datos', 'cuerdas.csv'))
kf = kf[kf.kfg.str.startswith('AS')].copy()
kf['val'] = pd.to_numeric(kf.valor, errors='coerce')
kf['L'] = pd.to_numeric(kf.largo, errors='coerce')
kf[['semval', 'amb', 'ncl']] = pd.DataFrame(
    kf.apply(lambda r: decode(r.nudos, r.L), axis=1).tolist(), index=kf.index)
kf['tiene_nudos'] = kf.ncl > 0

x = kf[kf.tiene_nudos]
print('cuerdas AS', len(kf), '| con nudos', len(x))
print('con nudos y decodificacion no ambigua:', int((~x.amb).sum()))
u = x[~x.amb]
print('valor == decodificacion:', round((abs(u.semval - u.val) <= 0.5).mean(), 4))
print('valor != decodificacion:', int((abs(u.semval - u.val) > 0.5).sum()))
print('\nKFG valor>0 sin nudos:', int(((~kf.tiene_nudos) & (kf.val > 0)).sum()))
print('KFG valor==0 con nudos:', int((kf.tiene_nudos & (kf.val == 0)).sum()))

bad = u[abs(u.semval - u.val) > 0.5].copy()
bad['dif'] = bad.val - bad.semval
print('\nejemplos de valor no sostenido por sus nudos:')
print(bad[['kfg', 'cuerda', 'valor', 'nudos', 'semval']].head(16).to_string(max_colwidth=48))
bad.to_csv(D('kfg_valor_no_sostenido.csv'), index=False)

# interseccion con el Databook: valor KFG == valor Databook pero nudos KFG no lo sostienen
res = pd.read_csv(D('databook_vs_kfg.csv'))
m = bad.merge(res[['quipu', 'cord_kfg', 'valor_db']], left_on=['kfg', 'cuerda'],
              right_on=['quipu', 'cord_kfg'], how='inner')
print('\nKFG no sostenido y con par en Databook:', len(m))
print('de ellos, valor KFG == valor Databook:', int((m.val == m.valor_db).sum()),
      '| KFG != Databook:', int((m.val != m.valor_db).sum()))
m.to_csv(D('kfg_valor_no_sostenido_cruce.csv'), index=False)
