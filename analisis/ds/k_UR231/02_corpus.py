"""UR231 en el contexto del corpus KFG: tamano, grupos, cuerdas vacias, color."""
import pandas as pd, numpy as np

ROOT = './'
c = pd.read_csv(ROOT + 'analisis/datos/cuerdas.csv')
c['blank'] = c.nudos.isna()
c['v'] = np.where(c.blank, np.nan, c.valor)

agg = c.groupby('kfg').agg(ncuerdas=('cuerda', 'size'),
                           ncolg=('nivel', lambda s: (s == 0).sum()),
                           nsub=('nivel', lambda s: (s > 0).sum()),
                           blanks=('blank', 'sum'),
                           ngrupos=('grupo', 'nunique'),
                           ncolores=('color', 'nunique'),
                           nval=('v', 'count'))
agg['fblank'] = agg.blanks / agg.ncuerdas
agg['fval'] = agg.nval / agg.ncuerdas
agg['ratio_sub'] = agg.nsub / agg.ncolg

ur = agg.loc['UR231']
print('UR231:', ur.to_dict())
print('percentil de ncuerdas:', round((agg.ncuerdas < ur.ncuerdas).mean() * 100, 1))
print('percentil de ngrupos:', round((agg.ngrupos < ur.ngrupos).mean() * 100, 1))
print('percentil de fblank:', round((agg.fblank < ur.fblank).mean() * 100, 1))
print('percentil de ncolores:', round((agg.ncolores < ur.ncolores).mean() * 100, 1))
print('percentil de ratio_sub:', round((agg.ratio_sub < ur.ratio_sub).mean() * 100, 1))
print('\nCorpus: medianas')
print(agg[['ncuerdas', 'ncolg', 'ngrupos', 'fblank', 'ncolores', 'ratio_sub']].median().round(3).to_dict())
print('\nTop 8 quipus por cuerdas:')
print(agg.sort_values('ncuerdas', ascending=False).head(8)[['ncuerdas', 'ncolg', 'ngrupos', 'fblank', 'ncolores']].to_string())
print('\nQuintil de fblank:')
print(pd.cut(agg.fblank, 5).value_counts().sort_index().to_string())
print('\nCuantos quipus tienen >=80 grupos:', (agg.ngrupos >= 80).sum(), 'de', len(agg))
print('Quipus con fblank>0.7:', (agg.fblank > 0.7).sum())
print('Quipus con fval>0.2 y fblank>0.7:', ((agg.fval > 0.2) & (agg.fblank > 0.7)).sum())
