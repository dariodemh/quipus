# -*- coding: utf-8 -*-
"""
06_grupos.py -- firma a nivel de GRUPO de colgantes: ¿los rasgos se organizan por grupo?
Estadistico por quipu = fraccion de cuerdas que comparten el valor modal de su grupo
(pureza ponderada). Nulo: barajar el rasgo DENTRO del quipu (conserva composicion y
tamanos de grupo). 500 permutaciones.
"""
import os, json
import numpy as np, pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(20261018)
c = pd.read_csv(os.path.join(AQUI, 'cuerdas_rasgos.csv'))
res = {}

def pureza_grupos(df, col, nperm=500, minq=3, minc=10):
    rows = []
    for kfg, d in df.groupby('kfg'):
        d = d[d[col].notna() & d.grupo.notna()]
        if len(d) < minc: continue
        sz = d.groupby('grupo').size()
        sz = sz[sz >= 2]
        if len(sz) < minq: continue
        d = d[d.grupo.isin(sz.index)]
        g = pd.factorize(d.grupo)[0]; K = g.max()+1
        lab = pd.factorize(d[col])[0]; C = lab.max()+1
        n = len(d)
        def stat(lb):
            M = np.zeros((K, C)); np.add.at(M, g, np.eye(C)[lb])
            return M.max(1).sum()/n
        obs = stat(lab)
        null = np.array([stat(RNG.permutation(lab)) for _ in range(nperm)])
        rows.append(dict(kfg=kfg, rasgo=col, n=n, n_grupos=int(len(sz)),
                         obs=obs, null=null.mean(),
                         p=(1+(null >= obs).sum())/(1+nperm)))
    return pd.DataFrame(rows)

tab = pd.concat([pureza_grupos(c, x) for x in ['torsion', 'union', 'terminacion', 'color_fam']],
                ignore_index=True)
tab['q'] = np.nan
for r, g in tab.groupby('rasgo'):
    p = g.p.values; o = np.argsort(p); m = len(p)
    q = np.empty(m); q[o] = np.minimum.accumulate((p[o]*m/np.arange(1, m+1))[::-1])[::-1]
    tab.loc[g.index, 'q'] = np.clip(q, 0, 1)
print('pureza por grupo (ponderada) vs nulo dentro del quipu:')
print(tab.groupby('rasgo').agg(n=('kfg','size'), obs=('obs','mean'), nul=('null','mean'),
      q05=('q', lambda s: (s < .05).sum())).round(3).to_string())
tab.to_csv(os.path.join(AQUI, 'grupos_pureza.csv'), index=False)
res['grupos'] = {k: {kk: float(vv) for kk, vv in v.items()}
                 for k, v in tab.groupby('rasgo').agg(obs=('obs','mean'), nul=('null','mean'),
                 q05=('q', lambda s: (s < .05).sum())).round(4).to_dict('index').items()}

c['pos1'] = c.groupby(['kfg', 'grupo']).orden.transform('min') == c.orden
sub = c[c.union.isin(['R', 'V']) & c.grupo.notna()]
print('\nunion R/V segun posicion en el grupo:')
print(sub.groupby('pos1').union.value_counts(normalize=True).unstack().round(3).to_string())
print(sub.groupby('pos1').size().to_string())
res['union_pos1'] = sub.groupby('pos1').union.value_counts(normalize=True).unstack().round(4).to_dict()
json.dump(res, open(os.path.join(AQUI, 'res_06.json'), 'w'), indent=1, default=str)
