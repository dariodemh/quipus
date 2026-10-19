# -*- coding: utf-8 -*-
"""
03_clustering.py -- ¿forman los quipus grupos discretos (talleres/manos)?
Representacion: 4 ejes categoricos one-hot + 6 rasgos continuos estandarizados -> PCA.
Clustering: KMeans (k=2..8) + jerarquico promedio sobre Gower (se informa el encadenamiento).
Validacion:
  (a) nulo que baraja cada rasgo independientemente entre quipus (preserva marginales,
      destruye la coherencia multivariada) -> distribucion nula de la mejor silueta;
  (b) bootstrap de cuerdas dentro de cada quipu (recalcula rasgos, error de muestreo);
  (c) bootstrap de quipus (80%).
"""
import os, json
import numpy as np, pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score

AQUI = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(20261018)
f = pd.read_csv(os.path.join(AQUI, 'firma_quipu.csv'))
res = {}

CAT = ['eje_tors', 'eje_ndS', 'eje_union', 'eje_term']
NUM = ['H_color_norm', 'p_mixto', 'colores_por_cuerda', 'pW', 'pAB', 'pMB']
d = f.dropna(subset=CAT + NUM).copy()
d = d[d.n_pend >= 6]
d = d.reset_index(drop=True)
print('n quipus para clustering:', len(d), '| sitios:', d.museo.nunique())

def matriz(df):
    cat = pd.get_dummies(df[CAT].astype(str), dtype=float)
    num = pd.DataFrame(StandardScaler().fit_transform(df[NUM].astype(float)),
                       columns=NUM, index=df.index)
    X = pd.concat([cat, num], axis=1).values
    return X

def embed(X, var=0.85):
    p = PCA(n_components=var, random_state=0).fit_transform(X)
    return p

def best_kmeans(X, ks=range(2, 9)):
    P = embed(X)
    sil = {}
    for k in ks:
        lab = KMeans(k, n_init=10, random_state=0).fit_predict(P)
        if len(set(lab)) < k: continue
        sil[k] = silhouette_score(P, lab)
    kbest = max(sil, key=sil.get)
    lab = KMeans(kbest, n_init=20, random_state=0).fit_predict(P)
    return kbest, sil[kbest], lab, sil, P

X = matriz(d)
kbest, sbest, lab, sils, P = best_kmeans(X)
print('KMeans k* =', kbest, 'silhouette =', round(sbest, 3), {k: round(v,3) for k,v in sils.items()})
res['obs'] = dict(k=int(kbest), sil=float(sbest), sil_por_k={int(k): float(v) for k, v in sils.items()})

# jerarquico sobre Gower: se informa el mejor corte con clusters >= 3%
def gower_cat(df):
    n = len(df); D = np.zeros((n, n)); m = 0
    for c in CAT:
        x = df[c].astype(str).values
        D += (x[:, None] != x[None, :]).astype(float); m += 1
    for c in NUM:
        x = df[c].astype(float).values
        rng = x.max() - x.min()
        if rng == 0: continue
        D += np.abs(x[:, None] - x[None, :]) / rng; m += 1
    return D / m

D = gower_cat(d)
cond = squareform(D, checks=False)
Zh = linkage(cond, method='average')
tam_por_k = {}
for k in range(2, 9):
    l = fcluster(Zh, k, criterion='maxclust')
    tam_por_k[k] = sorted(np.bincount(l)[1:].tolist())
print('jerarquico: tamano de clusters por k ->', tam_por_k)
res['jerarquico_tamanos'] = {int(k): v for k, v in tam_por_k.items()}

# ---- nulo (a) ----
nperm = 300
null_sil = np.empty(nperm)
nn_obs = np.sort(D + np.eye(len(d))*9, axis=1)[:, 0].mean()
null_nn = np.empty(nperm)
print('dist. media al vecino mas proximo: %.4f | pares con d<0.10: %d' %
      (nn_obs, ((D < .10).sum() - len(d))//2))
res['obs']['nn_mean'] = float(nn_obs)
res['obs']['pares_d10'] = int(((D < .10).sum() - len(d))//2)
for i in range(nperm):
    dd = d.copy()
    for c in CAT + NUM:
        dd[c] = RNG.permutation(dd[c].values)
    _, sn, _, _, _ = best_kmeans(matriz(dd))
    null_sil[i] = sn
    Dn = gower_cat(dd)
    null_nn[i] = np.sort(Dn + np.eye(len(dd))*9, axis=1)[:, 0].mean()
    if i % 60 == 0: print(' nulo', i, flush=True)
p_sil = (1 + (null_sil >= sbest).sum())/(1+nperm)
p_nn = (1 + (null_nn <= nn_obs).sum())/(1+nperm)
print('NULL silueta: %.3f (sd %.3f)  p=%.4f' % (null_sil.mean(), null_sil.std(), p_sil))
print('NULL nn:      %.4f  p=%.4f' % (null_nn.mean(), p_nn))
res['null'] = dict(sil_mean=float(null_sil.mean()), sil_sd=float(null_sil.std()),
                   p_sil=float(p_sil), nn_mean=float(null_nn.mean()), p_nn=float(p_nn), nperm=nperm)

# ---- bootstrap cuerdas ----
c = pd.read_csv(os.path.join(AQUI, 'cuerdas_rasgos.csv'))
def recompute(idx):
    s = c.iloc[idx]; out = {}
    for kfg, g in s.groupby('kfg'):
        nt = g.torsion.isin(['S','Z']).sum(); nu = g.union.isin(['R','V','T']).sum()
        vc = g.color_fam.dropna().value_counts(); p = vc/vc.sum() if vc.sum() else None
        H = -(p*np.log(p)).sum() if p is not None and len(p) > 1 else 0.0
        nf = g.color_fam.nunique(); ncol = max(g.color_fam.notna().sum(), 1)
        out[kfg] = dict(pS_tors=(g.torsion.eq('S').sum()/nt) if nt else np.nan,
            pS_nd_simple=(g.nd_simple_S.sum()/g.nd_simple_n.sum()) if g.nd_simple_n.sum() else np.nan,
            pR=(g.union.eq('R').sum()/nu) if nu else np.nan,
            pK=g.terminacion.eq('K').sum()/max(g.terminacion.notna().sum(),1),
            pB_term=g.terminacion.eq('B').sum()/max(g.terminacion.notna().sum(),1),
            pU_term=g.terminacion.eq('U').sum()/max(g.terminacion.notna().sum(),1),
            H_color_norm=H/np.log(nf) if nf > 1 else 0.0,
            p_mixto=g.color_mixto.mean(), colores_por_cuerda=nf/len(g),
            pW=g.color_fam.eq('W').sum()/ncol, pAB=g.color_fam.eq('AB').sum()/ncol,
            pMB=g.color_fam.eq('MB').sum()/ncol)
    return pd.DataFrame(out).T

idx_by_q = c.groupby('kfg').indices
base_lab = pd.Series(lab, index=d.kfg.values)
aris = []
for b in range(100):
    fb = recompute(np.concatenate([RNG.choice(ii, len(ii), replace=True) for ii in idx_by_q.values()])).astype(float)
    fb['eje_tors'] = pd.Series(np.select([fb.pS_tors>.5, fb.pS_tors<.5], ['S','Z'], None), index=fb.index)
    fb['eje_ndS'] = pd.Series(np.select([fb.pS_nd_simple>.5, fb.pS_nd_simple<.5], ['S','Z'], None), index=fb.index)
    fb['eje_union'] = pd.Series(np.select([fb.pR>.5, fb.pR<.5], ['R','V'], None), index=fb.index)
    fb['eje_term'] = fb[['pK','pB_term','pU_term']].idxmax(axis=1).map({'pK':'K','pB_term':'B','pU_term':'U'})
    dd = d[['kfg'] + CAT + NUM].set_index('kfg').copy(); fbi = fb.reindex(dd.index)
    for cc in CAT + NUM: dd[cc] = fbi[cc].where(fbi[cc].notna(), dd[cc])
    dd = dd.dropna(); 
    P2 = embed(matriz(dd.reset_index(drop=True)))
    l2 = KMeans(kbest, n_init=10, random_state=0).fit_predict(P2)
    aris.append(adjusted_rand_score(base_lab.loc[dd.index].values, l2))
print('ARI bootstrap cuerdas: %.3f (sd %.3f, min %.2f max %.2f)' %
      (np.mean(aris), np.std(aris), np.min(aris), np.max(aris)))
res['boot_cuerdas'] = dict(ari=float(np.mean(aris)), sd=float(np.std(aris)), n=len(aris))

# ---- bootstrap quipus ----
aris2 = []
for b in range(200):
    ii = RNG.choice(len(d), int(.8*len(d)), replace=False)
    P2 = embed(matriz(d.iloc[ii].reset_index(drop=True)))
    l2 = KMeans(kbest, n_init=10, random_state=0).fit_predict(P2)
    aris2.append(adjusted_rand_score(base_lab.iloc[ii].values, l2))
print('ARI bootstrap quipus: %.3f (sd %.3f)' % (np.mean(aris2), np.std(aris2)))
res['boot_quipus'] = dict(ari=float(np.mean(aris2)), sd=float(np.std(aris2)))

# ---- perfil ----
d['lab'] = lab
print(); print('clusters:', d.lab.value_counts().sort_index().to_dict())
print(); print('perfil (medias) por cluster:')
print(d.groupby('lab')[NUM + ['n_pend']].mean().round(3).to_string())
print(); print('ejes por cluster:')
for cc in CAT:
    print(cc); print(pd.crosstab(d.lab, d[cc]).to_string())
print(); print('ARI cluster vs cada eje:', {cc: round(adjusted_rand_score(d.lab, d[cc].astype(str)), 3) for cc in CAT})
print(); print('museo dominante por cluster:')
for k, g in d.groupby('lab'):
    print(k, len(g), g.museo.fillna('s/d').value_counts().head(3).to_dict(),
          g.region.fillna('Unknown').value_counts().head(2).to_dict())
d[['kfg','lab','museo','region','eje_tors','eje_ndS','eje_union','eje_term']].to_csv(
    os.path.join(AQUI, 'clusters.csv'), index=False)
np.save(os.path.join(AQUI, 'gower_D.npy'), D)
d[['kfg']].to_csv(os.path.join(AQUI, 'gower_orden.csv'), index=False)
json.dump(res, open(os.path.join(AQUI, 'res_03.json'), 'w'), indent=1)
