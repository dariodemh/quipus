"""Diagnóstico del efecto color~largo: ¿posición en el grupo, nivel, o componente físico?"""
import os
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'derived')
c = pd.read_pickle(os.path.join(D, 'cuerdas.pkl')).drop_duplicates(['kfg', 'cuerda'])
c = c[c.tiene_nudos & (c.largo > 0) & c.valor.notna()].copy()
c['loglargo'] = np.log(c.largo)
c['logcola'] = np.log(c.cola.clip(lower=0.05))
c['loglead'] = np.log(c.lead.clip(lower=0.05))
c['span'] = (c.pos_max - c.pos_min).clip(lower=0)
c['logspan'] = np.log(c.span.clip(lower=0.05))
c = c[c.color_simple.notna() & (c.color_simple != 'MIX')].copy()
c['pos_in_group'] = c.groupby(['kfg', 'grupo']).orden.rank(method='first')
c['frac_pos'] = c.groupby(['kfg', 'grupo']).pos_in_group.transform(lambda x: (x - 1) / max(len(x) - 1, 1))
c['pos_cat'] = pd.cut(c.frac_pos, [-0.01, 0.01, 0.34, 0.67, 0.99, 1.01],
                      labels=['primera', 'tercio1', 'medio', 'tercio3', 'ultima'])

SEED = 20261017
NPERM = 1500


def rank(x):
    return stats.rankdata(x)


def eps2(y, lab, min_n=6, min_col=2):
    n = len(y)
    if n < min_n:
        return np.nan
    cats, inv, cnt = np.unique(lab, return_inverse=True, return_counts=True)
    if len(cats) < 2 or cnt.min() < min_col:
        return np.nan
    r = rank(y)
    mr = np.bincount(inv, weights=r) / cnt
    H = 12.0 / (n * (n + 1)) * np.sum(cnt * (mr - (n + 1) / 2.0) ** 2)
    k = len(cats)
    return (H - k + 1) / (n - k)


def perm_eps(df, ycol, unit=('kfg', 'grupo'), nperm=NPERM, seed=SEED, min_n=6):
    us = []
    for k, d in df.groupby(list(unit)):
        d = d.dropna(subset=[ycol, 'color_simple'])
        e = eps2(d[ycol].values, d.color_simple.values, min_n)
        if np.isfinite(e):
            us.append((d[ycol].values, d.color_simple.values))
    if not us:
        return None
    obs = np.mean([eps2(y, l, min_n) for y, l in us])
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for i in range(nperm):
        null[i] = np.mean([eps2(y, rng.permutation(l), min_n) for y, l in us])
    return dict(n=len(us), obs=obs, null=null.mean(), sd=null.std(),
                p=(1 + np.sum(null >= obs)) / (nperm + 1))


print('=== 1. ¿el largo depende de la posición en el grupo? ===')
cat = c.groupby(['kfg', 'grupo', 'pos_cat'], observed=True).loglargo.mean().reset_index()
cat['dev'] = cat.loglargo - cat.groupby(['kfg', 'grupo']).loglargo.transform('mean')
print(cat.groupby('pos_cat', observed=True).dev.agg(['count', 'mean']).round(3).to_string())

print('\n=== 2. ¿el color se asocia a la posición en el grupo? ===')
p_pos = perm_eps(c, 'frac_pos', unit=('kfg', 'grupo'), nperm=1000)
print('epsilon2 frac_pos ~ color:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in p_pos.items()})

print('\n=== 3. color ~ componentes físicas ===')
for col in ['loglargo', 'loglead', 'logspan', 'logcola']:
    r = perm_eps(c, col, nperm=1500)
    print(f'{col}: eps2={r["obs"]:.4f} (nulo {r["null"]:.4f}, sd {r["sd"]:.4f}), p={r["p"]:.4f}, n={r["n"]}')

print('\n=== 4. color ~ largo controlando posición (residuo de posición dentro de grupo) ===')
# residual de loglargo tras posición (dummies de pos_cat) y media del grupo
X = pd.get_dummies(c.pos_cat, drop_first=True).astype(float)
X['grupo'] = c.kfg.astype(str) + '|' + c.grupo.astype(str)
y = c.loglargo.values
y_dm = y - pd.Series(y).groupby(X.grupo.values).transform('mean').values
Xd = X.drop(columns='grupo')
Xd = Xd - Xd.groupby(X.grupo.values).transform('mean').values
beta, *_ = np.linalg.lstsq(Xd.values, y_dm, rcond=None)
c['largo_pos_resid'] = y_dm - Xd.values @ beta
r = perm_eps(c, 'largo_pos_resid', nperm=1500)
print('eps2 largo_pos_resid ~ color:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})

print('\n=== 5. diferencia de cada color vs resto, dentro de grupo ===')
rows = []
for col in c.color_simple.unique():
    sub = c[c.color_simple.isin([col]) | c.color_simple.notna()]
    # comparar dentro de grupos que tienen el color y al menos otro color
    def dif(d):
        if (d.color_simple == col).sum() < 2 or (d.color_simple != col).sum() < 2:
            return np.nan
        return np.log(d[d.color_simple == col].largo).mean() - np.log(d[d.color_simple != col].largo).mean()
    v = c.groupby(['kfg', 'grupo']).apply(dif, include_groups=False).dropna()
    if len(v) >= 15:
        rows.append((col, len(v), v.mean(), stats.wilcoxon(v).pvalue))
print(pd.DataFrame(rows, columns=['color', 'n_grupos', 'dif_log', 'p']).round(3).sort_values('dif_log').to_string(index=False))
