# -*- coding: utf-8 -*-
"""
05_dentro.py -- ¿cambia la firma DENTRO de un quipu (anadidos, reparaciones)?
  A) quipus mixtos: ¿el rasgo minoritario esta agrupado en bloques o disperso?
     estadistico = numero de rachas del valor minoritario en el orden de cuerdas;
     nulo = reubicacion aleatoria de las minorias (2000 por quipu).
  B) cambio de regimen por punto de corte (max TV) en colgantes.
  C) notas de reparacion/empalme: ¿se asocian a heterogeneidad?
"""
import os, json
import numpy as np, pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(20261018)
c = pd.read_csv(os.path.join(AQUI, 'cuerdas_rasgos.csv'))
c = c.sort_values(['kfg', 'orden'])
res = {}

def runs_stat(pos, n):
    """numero de rachas de unos en una secuencia binaria de largo n con unos en pos."""
    if len(pos) == 0: return np.nan
    s = np.zeros(n, int); s[pos] = 1
    return 1 + int((np.diff(s) == 1).sum())

def test_bloques(col, vals, minfrac=3, nperm=2000):
    out = []
    for kfg, d in c.groupby('kfg'):
        s = d[col].dropna()
        s = s[s.isin(vals)]
        n = len(s)
        if n < 10: continue
        vc = s.value_counts()
        if len(vc) < 2: continue
        minor = vc.idxmin(); k = int(vc.min())
        if k < minfrac or k > n/2: continue
        idx = np.where(s.values == minor)[0]
        obs = runs_stat(idx, n)
        null = np.empty(nperm)
        for i in range(nperm):
            null[i] = runs_stat(np.sort(RNG.choice(n, k, replace=False)), n)
        p = (1 + (null <= obs).sum())/(1+nperm)
        out.append(dict(kfg=kfg, rasgo=col, n=n, k_min=k, obs=obs,
                        esperado=null.mean(), p=p))
    return pd.DataFrame(out)

tab = []
tab.append(test_bloques('torsion', ['S', 'Z']))
tab.append(test_bloques('union', ['R', 'V']))
tab.append(test_bloques('terminacion', ['K', 'B', 'U']))
b = pd.concat(tab, ignore_index=True)
# BH por familia (rasgo)
b['q'] = np.nan
for r, g in b.groupby('rasgo'):
    p = g.p.values; o = np.argsort(p); m = len(p)
    q = np.empty(m); q[o] = np.minimum.accumulate((p[o]*m/np.arange(1, m+1))[::-1])[::-1]
    b.loc[g.index, 'q'] = np.clip(q, 0, 1)
print('A) quipus mixtos evaluables por rasgo:')
print(b.groupby('rasgo').agg(n=('kfg','size'), p05=('p', lambda s: (s < .05).sum()),
      q05=('q', lambda s: (s < .05).sum()), obs=('obs','mean'), esp=('esperado','mean')).round(3).to_string())
print('\nquipus con bloques significativos (q<0.05):')
print(b[b.q < .05][['kfg','rasgo','n','k_min','obs','esperado','p','q']].to_string(index=False))
b.to_csv(os.path.join(AQUI, 'bloques.csv'), index=False)
res['bloques'] = dict(n=int(len(b)), q05=int((b.q < .05).sum()),
                      por_rasgo=b.groupby('rasgo').size().to_dict())

# ---------- B) cambio de regimen (max TV) en colgantes ----------
def max_tv_change(labels, minseg=5):
    n = len(labels)
    cats = pd.unique(labels); best = 0
    for cut in range(minseg, n-minseg+1):
        a, bb = labels[:cut], labels[cut:]
        tv = 0.5*sum(abs((a == x).mean() - (bb == x).mean()) for x in cats)
        best = max(best, tv)
    return best

def test_cambio(col, nperm=500):
    rows = []
    for kfg, d in c.groupby('kfg'):
        d = d[(d.nivel == 0) & d[col].notna()]
        if len(d) < 20: continue
        lab = d[col].values
        if len(set(lab)) < 2: continue
        obs = max_tv_change(lab)
        null = np.array([max_tv_change(RNG.permutation(lab)) for _ in range(nperm)])
        rows.append(dict(kfg=kfg, rasgo=col, n=len(lab), obs=obs,
                         null=null.mean(), p=(1+(null >= obs).sum())/(1+nperm)))
    return pd.DataFrame(rows)

t2 = pd.concat([test_cambio('torsion'), test_cambio('union'), test_cambio('terminacion')],
               ignore_index=True)
t2['q'] = np.nan
for r, g in t2.groupby('rasgo'):
    p = g.p.values; o = np.argsort(p); m = len(p)
    q = np.empty(m); q[o] = np.minimum.accumulate((p[o]*m/np.arange(1, m+1))[::-1])[::-1]
    t2.loc[g.index, 'q'] = np.clip(q, 0, 1)
print('\nB) cambio de regimen (max TV) por quipu:')
print(t2.groupby('rasgo').agg(n=('kfg','size'), p05=('p', lambda s: (s < .05).sum()),
      q05=('q', lambda s: (s < .05).sum()), obs=('obs','mean'), nul=('null','mean')).round(3).to_string())
t2.to_csv(os.path.join(AQUI, 'cambio_regimen.csv'), index=False)
res['cambio'] = dict(n=int(len(t2)), q05=int((t2.q < .05).sum()),
                     por_rasgo=t2.groupby('rasgo').size().to_dict())

# ---------- C) notas de reparacion ----------
c['nota_rep'] = c.notas.fillna('').str.lower().str.contains(
    'repair|splice|mend|replac|insert|add(?:ed)?|join|fragment|restor', regex=True)
qrep = c.groupby('kfg').nota_rep.sum()
print('\nC) cuerdas con nota de reparacion/empalme/anadido:', int(c.nota_rep.sum()),
      'en', int((qrep > 0).sum()), 'quipus')
# comparar heterogeneidad (mezcla de torsion) entre quipus con y sin nota
f = pd.read_csv(os.path.join(AQUI, 'firma_quipu.csv'))
f['mezcla_tors'] = 1 - f.pur_tors
f['nota_rep'] = f.kfg.map(qrep).fillna(0) > 0
sub = f[f.pur_tors.notna()]
print(sub.groupby('nota_rep').mezcla_tors.agg(['size','mean','median']).round(3).to_string())
mw = stats.mannwhitneyu(sub[sub.nota_rep].mezcla_tors, sub[~sub.nota_rep].mezcla_tors,
                        alternative='greater')
print('Mann-Whitney (mas mezcla en quipus con nota):', mw)
res['notas'] = dict(n_cuerdas=int(c.nota_rep.sum()), n_quipus=int((qrep > 0).sum()),
                    p=float(mw.pvalue))
json.dump(res, open(os.path.join(AQUI, 'res_05.json'), 'w'), indent=1, default=str)
