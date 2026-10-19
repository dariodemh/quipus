# -*- coding: utf-8 -*-
"""UR093 en el corpus OKR: morfologia comparada (adjuncion media, modulo 8)."""
import sqlite3, pandas as pd, numpy as np
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
c = pd.read_sql("select KHIPU_ID, CORD_ID, CORD_LEVEL, ATTACH_POS, CORD_LENGTH, PENDANT_FROM, ATTACHMENT_TYPE, TERMINATION from cord", con)
k = pd.read_sql("select KHIPU_ID, OKR_NUM, MUSEUM_NAME, PROVENANCE from khipu_main", con)
print('quipus', len(k), 'cords', len(c))

# nivel 1 = colgante; nivel 2 = subsidiaria (OKR)
c['lvl'] = c.CORD_LEVEL
# metricas por quipu
g = c.groupby('KHIPU_ID')
m = pd.DataFrame({
    'n': g.size(),
    'n_l1': c[c.lvl==1].groupby('KHIPU_ID').size(),
    'med_attach2': c[c.lvl==2].groupby('KHIPU_ID').ATTACH_POS.median(),
    'frac_mid': c[c.lvl==2].assign(mid=lambda d: d.ATTACH_POS>2).groupby('KHIPU_ID').mid.mean(),
})
m['n_l2'] = c[c.lvl==2].groupby('KHIPU_ID').size()
m = m.fillna({'n_l1':0,'n_l2':0,'frac_mid':0})
m = m.merge(k.set_index('KHIPU_ID'), left_index=True, right_index=True)
m['prop_sub'] = m.n_l2 / m.n_l1.replace(0, np.nan)
big = m[m.n_l1 >= 20]
print('\n== quipus con >=20 colgantes: mediana attach de subsidiarias ==')
print('n quipus', len(big), '| med_attach2 cuantiles', big.med_attach2.quantile([.25,.5,.75]).round(1).to_dict())
print('UR093 (KH0329):', m.loc[m.OKR_NUM=='KH0329', ['n','n_l1','n_l2','med_attach2','frac_mid','prop_sub']].round(2).to_dict('records'))
print('\n== top 12 por med_attach2 (>=20 colgantes) ==')
print(big.sort_values('med_attach2', ascending=False).head(12)[['OKR_NUM','MUSEUM_NAME','n','n_l1','n_l2','med_attach2','frac_mid']].to_string(max_colwidth=28))
print('\n== Temple Radicati (KH0321-KH0348) ==')
tr = m[m.MUSEUM_NAME.fillna('').str.contains('Radicati')]
print(tr[['OKR_NUM','n','n_l1','n_l2','med_attach2','prop_sub']].sort_values('OKR_NUM').to_string())
print('\n== quipus con proporcion de subsidiarias >2 (como UR093) ==')
print(big[big.prop_sub > 2][['OKR_NUM','MUSEUM_NAME','n','n_l1','n_l2','med_attach2','prop_sub']].round(2).to_string(max_colwidth=25))
