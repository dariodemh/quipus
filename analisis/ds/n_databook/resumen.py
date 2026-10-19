#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conteos por quipu: cobertura, cuerdas de mas/menos, colores y largos."""
import os
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
D = lambda *a: os.path.join(BASE, *a)

res = pd.read_csv(D('databook_vs_kfg.csv'))
db = pd.read_csv(D('databook_rows.csv'))
kf = pd.read_csv(D('..', '..', 'datos', 'cuerdas.csv'))
kf = kf[kf.kfg.str.startswith('AS')].copy(); kf['quipu'] = kf.kfg
est = pd.read_csv(D('databook_estructura.csv'))

db0 = db[db.cord_databook.str.match(r'^(p\d+|t\d+)$')]
kf0 = kf[kf.nivel == 0]
r0 = res[(res.nivel_db == 0) & (res.nivel_kfg == 0) & (res.score >= 3)]

rows = []
for q in sorted(set(db0.quipu) | set(kf0.quipu)):
    a = db0[db0.quipu == q]; b = kf0[kf0.quipu == q]
    e = est[est.quipu == q]
    pares = r0[r0.quipu == q]
    sin_par = b[~b.cuerda.isin(set(pares.cord_kfg))]
    rows.append(dict(quipu=q, en_kfg=q in set(kf0.quipu),
                     n_db0=len(a), n_kfg0=len(b),
                     n_desc=(e.n_pendientes_desc.iloc[0] + e.n_tops_desc.iloc[0]) if len(e) else np.nan,
                     n_pares0=len(pares), n_kfg0_sin_par=len(sin_par),
                     kfg_sin_par_largos=','.join('%.1f' % x for x in sin_par.largo.fillna(0).tolist()[:10])))
S = pd.DataFrame(rows)
S.to_csv(D('quipus_conteos.csv'), index=False)

both = S[S.en_kfg & (S.n_db0 > 0)]
print('en ambos', len(both), '| solo databook', int((~S.en_kfg).sum()),
      '| solo KFG', int((S.en_kfg & (S.n_db0 == 0)).sum()))
print('solo KFG:', S[S.en_kfg & (S.n_db0 == 0)].quipu.tolist())

S['dif_kfg_desc'] = S.n_kfg0 - S.n_desc
x = S[S.en_kfg & S.n_desc.notna()].copy()
print('\nKFG con >=3 cuerdas MAS que la descripcion del Databook:')
print(x[x.dif_kfg_desc >= 3].sort_values('dif_kfg_desc', ascending=False)[
    ['quipu', 'n_kfg0', 'n_desc', 'dif_kfg_desc']].head(10).to_string(index=False))
print('\nKFG con >=3 cuerdas MENOS que la descripcion (posible perdida/parseo):')
print(x[x.dif_kfg_desc <= -3].sort_values('dif_kfg_desc')[
    ['quipu', 'n_kfg0', 'n_desc', 'dif_kfg_desc']].head(10).to_string(index=False))

print('\nKFG cuerdas con largo=0:', int((kf.largo == 0).sum()),
      '| con valor>0 y largo=0:', int(((kf.largo == 0) & (kf.valor > 0)).sum()))
print(kf[(kf.largo == 0) & (kf.valor > 0)][['kfg', 'cuerda', 'valor', 'color']].head(8).to_string(index=False))

# color / largo
m = res[(res.nivel_db == res.nivel_kfg) & (res.score >= 3)].copy()
print('\ncolor exacto %.3f | largo <=0.5 %.3f | n %d' %
      ((m.color_db_n.fillna('') == m.color_kfg_n.fillna('')).mean(),
       ((m.largo_db - m.largo_kfg).abs() <= 0.5).mean(), len(m)))
