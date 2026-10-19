# -*- coding: utf-8 -*-
"""UR113 en el corpus: tamano, jerarquia y singularidad estructural."""
import pandas as pd, numpy as np, os
BASE = r'.'; OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
c = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'), dtype={'kfg': str})
c['valor'] = pd.to_numeric(c.valor, errors='coerce').fillna(0)
for col in ['nivel', 'grupo', 'largo']:
    c[col] = pd.to_numeric(c[col], errors='coerce')
c['sin_nudo'] = c.nudos.isna()
per = c.groupby('kfg').agg(n=('cuerda', 'size'), pend=('nivel', lambda x: (x == 0).sum()),
                           subs=('nivel', lambda x: (x > 0).sum()), maxniv=('nivel', 'max'),
                           grupos=('grupo', 'nunique'), ncol=('color', 'nunique'),
                           suma=('valor', 'sum'), sinnudo=('sin_nudo', 'sum'))
per['ratio'] = per.subs / per.pend.replace(0, np.nan)
per['sinnudo_frac'] = per.sinnudo / per.n
per = per.sort_values('n', ascending=False)
print('UR113 en el corpus:')
print('  n cuerdas', per.loc['UR113', 'n'], 'puesto', int((per.n > per.loc['UR113', 'n']).sum()) + 1, 'de', len(per))
print('  colgantes', int(per.loc['UR113', 'pend']), 'puesto', int((per.pend > per.loc['UR113', 'pend']).sum()) + 1)
print('  subsidiarias', int(per.loc['UR113', 'subs']), 'puesto', int((per.subs > per.loc['UR113', 'subs']).sum()) + 1)
print('  ratio subs/colgante', round(per.loc['UR113', 'ratio'], 2), 'puesto', int((per.ratio > per.loc['UR113', 'ratio']).sum()) + 1)
print('  grupos', int(per.loc['UR113', 'grupos']), 'puesto', int((per.grupos > per.loc['UR113', 'grupos']).sum()) + 1)
print('  colores distintos', int(per.loc['UR113', 'ncol']), 'puesto', int((per.ncol > per.loc['UR113', 'ncol']).sum()) + 1)
print('\nTop 12 por cuerdas:')
print(per.head(12)[['n', 'pend', 'subs', 'ratio', 'grupos', 'ncol', 'sinnudo_frac']].round(2).to_string())
print('\nTop 10 por ratio subs/colgante (con >=50 colgantes):')
print(per[per.pend >= 50].sort_values('ratio', ascending=False).head(10)[['pend', 'subs', 'ratio', 'n']].round(2).to_string())
print('\nDistribucion del ratio (quipus >=50 colgantes): media', round(per[per.pend >= 50].ratio.mean(), 2),
      'mediana', round(per[per.pend >= 50].ratio.median(), 2), 'p90', round(per[per.pend >= 50].ratio.quantile(.9), 2))
print('  percentil de UR113:', round((per[per.pend >= 50].ratio < per.loc['UR113', 'ratio']).mean(), 3))
# franja de la fraccion de cuerdas sin nudo
print('\nFraccion de cuerdas sin nudo: UR113', round(per.loc['UR113', 'sinnudo_frac'], 3),
      '; mediana corpus', round(per.sinnudo_frac.median(), 3), '; percentil',
      round((per.sinnudo_frac < per.loc['UR113', 'sinnudo_frac']).mean(), 3))
# cuantos quipus tienen >=300 colgantes y >=30 grupos
big = per[(per.pend >= 300)]
print('\nquipus con >=300 colgantes:', len(big), ':', big.index.tolist()[:12])
per.to_csv(os.path.join(OUT, 'corpus_por_quipu.csv'))
