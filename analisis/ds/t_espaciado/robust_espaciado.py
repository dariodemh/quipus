"""Robustez del hallazgo A: gaps grandes separan grupos de escala distinta.

- bins de gap con delta estandarizado dentro de quipu (efecto graduado)
- excluir gaps extremos (>10 cm)
- usar gap_dpos (incluye ancho del grupo)
- mediana en vez de media de valor
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'derived')
g = pd.read_pickle(os.path.join(D, 'grupos.pkl')).sort_values(['kfg', 'grupo']).reset_index(drop=True)
c = pd.read_pickle(os.path.join(D, 'cuerdas.pkl')).drop_duplicates(['kfg', 'cuerda'])
SEED = 20261017

# features por grupo con mediana
med = c[c.tiene_nudos].groupby(['kfg', 'grupo']).agg(
    logv_med=('logvalor', 'median')).reset_index()
g = g.merge(med, on=['kfg', 'grupo'], how='left')

rows = []
for k, d in g.groupby('kfg'):
    d = d.reset_index(drop=True)
    for i in range(len(d) - 1):
        a, b = d.iloc[i], d.iloc[i + 1]
        if pd.isna(a.gap) or pd.isna(a.logv_med) or pd.isna(b.logv_med):
            continue
        rows.append(dict(kfg=k, gap=a.gap, gap_dpos=a.gap_dpos,
                         dv=abs(a.logv_med - b.logv_med),
                         dv_mean=abs(a.logv_mean - b.logv_mean),
                         dnd=abs(a.ndig_max - b.ndig_max),
                         dl=abs(a.largo_mean - b.largo_mean),
                         dn=abs(a.n_cuerdas - b.n_cuerdas)))
P = pd.DataFrame(rows)
print('pares:', len(P), 'quipus:', P.kfg.nunique())

# estandarizar delta dentro de quipu
for col in ['dv', 'dv_mean', 'dnd', 'dl']:
    P[col + '_z'] = P.groupby('kfg')[col].transform(lambda x: (x - x.mean()) / (x.std(ddof=0) + 1e-9))

bins = [-0.01, 0.5, 1.0, 2.0, 5.0, 1e9]
labels = ['0-0.5', '0.5-1', '1-2', '2-5', '>5']
P['bin'] = pd.cut(P.gap, bins, labels=labels)
print('\n--- delta de valor (mediana) estandarizado por bin de gap ---')
print(P.groupby('bin', observed=True).agg(n=('dv_z', 'size'), dv_z=('dv_z', 'mean'),
                                          dnd_z=('dnd_z', 'mean'), dl_z=('dl_z', 'mean')).round(3).to_string())

print('\n--- correlación de rangos (dentro de quipu) por especificación ---')


def test(P, gapcol, dcol, min_pairs=4, nperm=1500, seed=SEED, maxgap=None):
    Q = P.dropna(subset=[gapcol, dcol]).copy()
    if maxgap is not None:
        Q = Q[Q[gapcol] <= maxgap]
    us = []
    for k, d in Q.groupby('kfg'):
        if len(d) < min_pairs or d[gapcol].nunique() < 2:
            continue
        x = stats.rankdata(d[gapcol]); x -= x.mean()
        y = stats.rankdata(d[dcol]); y -= y.mean()
        us.append((x, y))
    if not us:
        return None

    def rho(x, y):
        return float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))
    obs = np.mean([rho(x, y) for x, y in us])
    rng = np.random.default_rng(seed)
    null = np.array([np.mean([rho(rng.permutation(x), y) for x, y in us]) for _ in range(nperm)])
    return dict(n=len(us), rho=obs, p=(1 + np.sum(null >= obs)) / (nperm + 1),
                frac_pos=float(np.mean([rho(x, y) > 0 for x, y in us])))


for gapcol in ['gap', 'gap_dpos']:
    for dcol in ['dv', 'dv_mean', 'dnd', 'dl']:
        for mg in [None, 10]:
            r = test(P, gapcol, dcol, maxgap=mg)
            if r:
                print(f'{gapcol:8s} {dcol:8s} maxgap={str(mg):4s}: rho={r["rho"]:.3f} p={r["p"]:.4f} frac+={r["frac_pos"]:.2f} n={r["n"]}')

# quintiles de gap dentro de quipu
P['gap_q'] = P.groupby('kfg').gap.transform(lambda x: pd.qcut(x, 5, labels=False, duplicates='drop'))
print('\n--- delta por quintil de gap dentro de quipu ---')
print(P.groupby('gap_q').agg(n=('dv_z', 'size'), dv_z=('dv_z', 'mean'),
                              dnd_z=('dnd_z', 'mean'), dl_z=('dl_z', 'mean')).round(3).to_string())
