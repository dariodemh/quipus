"""UR231: estructura basica. Salidas en esta carpeta."""
import pandas as pd, numpy as np, sqlite3, json, re

KFG = 'UR231'
ROOT = './'
OUT = ROOT + 'analisis/ds/k_UR231/'

c = pd.read_csv(ROOT + 'analisis/datos/cuerdas.csv')
u = c[c.kfg == KFG].copy()
u['num'] = u.cuerda.str.extract(r'p(\d+)').astype(int)
u['v'] = np.where(u.nudos.isna(), np.nan, u.valor)

# OKR: fibra y posicion
con = sqlite3.connect(ROOT + 'data/external/open-khipu-repository/data/khipu.db')
ok = pd.read_sql('select * from cord where khipu_id=1000541', con)
ok = ok[ok.CORD_LEVEL == 1]  # solo colgantes: OKR repite inv_num=1 en subsidiarias
ok = ok[['INVESTIGATOR_CORD_NUM', 'FIBER', 'CORD_ORDINAL', 'CLUSTER_ID']]
ok.columns = ['num', 'fiber', 'cord_ordinal', 'cluster_id']
# OKR solo numera colgantes (1..864); las subsidiarias comparten el num. del padre
u = u.merge(ok, on='num', how='left', suffixes=('', '_okr'))
u.loc[u.nivel > 0, ['fiber', 'cord_ordinal', 'cluster_id']] = np.nan

# posicion de la cuerda dentro del grupo (0-based)
u['idx'] = u.groupby('grupo').cumcount()

g = u[u.nivel == 0].groupby('grupo').agg(
    n=('cuerda', 'size'), nval=('v', 'count'), suma=('v', 'sum'),
    color=('color', 'first'), fiber=('fiber', 'first'),
    orden0=('orden', 'min'), orden1=('orden', 'max'))
g['nsub'] = u[u.nivel > 0].groupby('grupo').size().reindex(g.index).fillna(0).astype(int)
g = g.reset_index()

# cuerdas acumuladas (solo colgantes) antes de cada grupo
g['pend_ini'] = g.n.cumsum().shift(1).fillna(0).astype(int)
g['pend_fin'] = g.pend_ini + g.n

# valores por posicion: matriz 80 x 12
M = np.full((len(g), 12), np.nan)
for _, r in u[u.nivel == 0].iterrows():
    if r.idx < 12:
        M[int(r.grupo), int(r.idx)] = r.v

g.to_csv(OUT + 'grupos_resumen.csv', index=False)
np.save(OUT + 'matriz_valores.npy', M)
u.to_csv(OUT + 'cuerdas_enriquecidas.csv', index=False)

print(g.to_string(index=False))
print('\nTOTAL cuerdas', len(u), 'colgantes', (u.nivel == 0).sum(), 'subs', (u.nivel > 0).sum())
print('grupos', len(g), 'colores distintos', u.color.nunique())
print('cuerdas con nudos', u.nudos.notna().sum(), 'sin nudos', u.nudos.isna().sum())
print('valor total', u.v.sum(), 'grupos con valores', (g.nval > 0).sum())
print('\nInicio (cord) de los grupos 0D:', g[g.color == '0D'][['grupo', 'pend_ini', 'n']].to_string(index=False))
print('Inicio de los grupos de 12:', g[g.n == 12][['grupo', 'pend_ini', 'n', 'color']].to_string(index=False))
print('\nDiferencias de pend_ini entre grupos 0D:', np.diff(g[g.color == '0D'].pend_ini.values))
