# -*- coding: utf-8 -*-
"""
02_pureza.py -- coherencia interna de cada rasgo y estructura de la firma.
  A) pureza observada vs nulo que baraja cuerdas entre quipus (conserva tamanos y marginal)
  B) distribucion de la firma: ejes binarios y su asociacion cruzada (chi2 / permutacion)
  C) firma por coleccion/sitio y control de transcriptor (CREATED_BY) en OKR
"""
import os, json
import numpy as np, pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(20261018)
f = pd.read_csv(os.path.join(AQUI, 'firma_quipu.csv'))
c = pd.read_csv(os.path.join(AQUI, 'cuerdas_rasgos.csv'))
res = {}

# ---------- A) pureza vs nulo (vectorizado con bincount) ----------
def test_pureza(lab, gid, minn=5, nperm=4000):
    d = pd.DataFrame({'lab': lab, 'g': gid}).dropna()
    g = pd.factorize(d.g)[0]
    codes, uni = pd.factorize(d.lab)
    K = len(uni)
    sizes = np.bincount(g)
    keep = sizes >= minn
    # pureza observada por quipu = max_c count / n
    M = np.zeros((len(g), K))
    M[np.arange(len(g)), codes] = 1
    cnt = np.zeros((len(sizes), K))
    np.add.at(cnt, g, M)
    obs = (cnt.max(1) / sizes)[keep]
    v = M.copy()
    null = np.empty(nperm)
    for i in range(nperm):
        # barajar etiquetas entre cuerdas (global), preservando tamanos de quipu
        idx = RNG.permutation(len(g))
        cnt2 = np.zeros((len(sizes), K))
        np.add.at(cnt2, g, M[idx])
        null[i] = np.mean((cnt2.max(1) / sizes)[keep])
    p = (1 + (null >= obs.mean()).sum()) / (1 + nperm)
    return dict(quipus=int(keep.sum()), obs=float(obs.mean()), null=float(null.mean()),
                p=float(p), pct_puros=float((obs == 1).mean()),
                n_cuerdas=int(len(d)))

tab = []
# SOLO valores conocidos: U/Unknown/? no son categoria de manufactura
tors_lab = c['torsion'].where(c['torsion'].isin(['S','Z']))
union_lab = c['union'].where(c['union'].isin(['R','V','T']))
items = [(tors_lab,'torsion',5), (union_lab,'union',5),
         (c['terminacion'],'terminacion',5), (c['color_fam'],'color',5)]
for col in ['nd_simple_S','nd_largo_S','nd_ocho_S']:
    base = col.replace('_S','')
    lab = np.where(c[base+'_S']+c[base+'_Z']==0, None,
                   np.where(c[base+'_S']>c[base+'_Z'], 'S',
                            np.where(c[base+'_S']<c[base+'_Z'], 'Z', None))).astype(object)
    items.append((lab, base+'_dir', 10))
for lab, nombre, minn in items:
    r = test_pureza(np.asarray(lab), c.kfg.values, minn)
    r['rasgo'] = nombre
    tab.append(r); print(r)
res['pureza'] = tab

# ---------- B) ejes de la firma ----------
f['eje_tors'] = np.select([f.pS_tors>.5, f.pS_tors<.5], ['S','Z'], None).astype(object)
f['eje_ndS'] = np.select([f.pS_nd_simple>.5, f.pS_nd_simple<.5], ['S','Z'], None).astype(object)
f['eje_union'] = np.select([f.pR>.5, f.pR<.5], ['R','V'], None).astype(object)
f['eje_term'] = f[['pK','pB_term','pU_term']].idxmax(axis=1).map(
    {'pK':'K','pB_term':'B','pU_term':'U'})
for col in ['eje_tors','eje_ndS','eje_union','eje_term']:
    print('\n', col, f[col].value_counts(dropna=False).to_dict())

def chi2_fast(a, b):
    ct = pd.crosstab(a, b).values
    r = ct.sum(1, keepdims=True); s = ct.sum(0, keepdims=True); n = ct.sum()
    E = r @ s / n
    return float(((ct-E)**2 / E).sum())

def chi2_perm(a, b, nperm=10000):
    d = f[[a, b]].dropna()
    chi2 = chi2_fast(d[a].values, d[b].values)
    bb = d[b].values.copy(); aa = d[a].values
    null = np.empty(nperm)
    for i in range(nperm):
        null[i] = chi2_fast(aa, RNG.permutation(bb))
    return chi2, (1+(null>=chi2).sum())/(1+nperm), len(d), pd.crosstab(d[a], d[b])

pairs = [('eje_tors','eje_ndS'), ('eje_tors','eje_union'), ('eje_tors','eje_term'),
         ('eje_ndS','eje_union'), ('eje_ndS','eje_term'), ('eje_union','eje_term')]
print('\nasociacion cruzada de ejes (chi2, p perm, n):')
res['ejes'] = []
for a, b in pairs:
    chi2, p, n, ct = chi2_perm(a, b)
    res['ejes'].append(dict(a=a, b=b, chi2=round(chi2,2), p=float(p), n=int(n)))
    print(f'{a:10s} x {b:10s} chi2={chi2:7.2f} p={p:.4f} n={n}')
    if a=='eje_tors' and b=='eje_ndS': print(ct.to_string())
f.to_csv(os.path.join(AQUI, 'firma_quipu.csv'), index=False)

# ---------- C) firma por coleccion / transcriptor ----------
print('\n--- firma por coleccion (top) ---')
f['col'] = f.museo.fillna('s/d').str.slice(0,28)
for col in ['eje_tors','eje_ndS','eje_union']:
    t = pd.crosstab(f['col'], f[col])
    t['n'] = t.sum(axis=1)
    print(col); print(t.sort_values('n', ascending=False).head(8).to_string())

print('\n--- control transcriptor OKR (CREATED_BY) ---')
sub = f[f.created_by.notna() & f.pS_tors.notna()]
print(sub.groupby('created_by').agg(n=('kfg','size'), pS=('pS_tors','mean'),
      thick=('thick_mean','mean'), fibrec=('fib_frac_cod','mean')).round(3).to_string())
groups = [d.pS_tors.dropna().values for _, d in sub.groupby('created_by') if len(d) >= 5]
print('Kruskal pS_tors ~ created_by:', stats.kruskal(*groups))
groups = [d.thick_mean.dropna().values for _, d in sub.groupby('created_by') if len(d) >= 5]
print('Kruskal grosor ~ created_by:', stats.kruskal(*groups))
print(pd.crosstab(sub.created_by, sub.fib_frac_cod > 0.5).to_string())

json.dump(res, open(os.path.join(AQUI, 'res_02.json'), 'w'), indent=1, default=str)
