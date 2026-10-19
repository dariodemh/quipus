"""Tarea 4: tipología aritmética de quipus (clustering) y cruce con procedencia (a nivel de quipu, con permutación estratificada por colección)."""
import numpy as np, pandas as pd, warnings
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score
from nucleo import cargar, bh
warnings.filterwarnings("ignore")
D = Path(__file__).parent
Qs, q = cargar(); q = q.set_index("kfg")
S = pd.read_csv(D / "resultado_por_quipu.csv").set_index("kfg")
C = pd.read_csv(D / "cierre_intragrupo.csv").set_index("kfg")
rows = []
for k, Q in Qs.items():
    v = Q["v"][Q["pres"] & (Q["v"] > 0)]
    if len(v) < 10: continue
    u, c = np.unique(v, return_counts=True)
    w = v[v >= 10]
    s = S.loc[k]
    rows.append(dict(kfg=k, n_pos=len(v), lmed=np.log10(np.median(v)), lp90=np.log10(np.percentile(v, 90)), fle9=(v <= 9).mean(),
                     top=c.max() / len(v), distintos=len(u) / len(v), m10=(w % 10 == 0).mean() if len(w) >= 10 else np.nan,
                     lnpos=np.log10(len(v)), lgs=np.log10(len(Q["L0"]) / (len(Q["gs"]) - 1)), subs=(Q["lvl"] > 0).mean(),
                     prof=Q["lvl"].max(), ausentes=1 - Q["pres"].mean(),
                     zcomp=np.arcsinh((s.obs_comp - s.E_N2_nivel_comp) / max(s.sd_N2_nivel_comp, 0.5)),
                     zcierre=np.arcsinh((C.loc[k, "obs"] - C.loc[k, "E"]) / max(C.loc[k, "sd"], 0.3)),
                     tieneT=float(s.obs_TA_elig > 0)))
F = pd.DataFrame(rows).set_index("kfg")
F["m10"] = F.m10.fillna(F.m10.median())
cols = [c for c in F.columns if c != "n_pos"]
X = StandardScaler().fit_transform(F[cols].clip(F[cols].quantile(.01), F[cols].quantile(.99), axis=1) if False else F[cols].clip(F[cols].quantile(.01), F[cols].quantile(.99), axis=1))
pca = PCA(0.9).fit(X); Z = pca.transform(X); print("quipus clusterizados", len(F), "de 651; PCs", Z.shape[1], "var", pca.explained_variance_ratio_.sum().round(2))
print("cargas PC1/PC2:\n", pd.DataFrame(pca.components_[:2].T, index=cols, columns=["PC1", "PC2"]).round(2).T.to_string())
res = []
for k in range(2, 9):
    km = KMeans(k, n_init=20, random_state=0).fit(Z)
    sil = silhouette_score(Z, km.labels_)
    rng = np.random.default_rng(k); aris = []
    for b in range(60):
        ix = rng.choice(len(Z), len(Z)); kb = KMeans(k, n_init=5, random_state=b).fit(Z[ix])
        aris.append(adjusted_rand_score(km.labels_, kb.predict(Z)))
    gm = GaussianMixture(k, random_state=0, n_init=3).fit(Z)
    res.append(dict(k=k, silueta=round(sil, 3), ARI_boot=round(np.mean(aris), 3), BIC_gmm=round(gm.bic(Z), 0), ARI_ward=round(adjusted_rand_score(km.labels_, AgglomerativeClustering(k).fit_predict(Z)), 3)))
R = pd.DataFrame(res); print(R.to_string()); R.to_csv(D / "tipologia_k.csv", index=False)
import sys
K = int(sys.argv[1]) if len(sys.argv) > 1 else 4  # k=2 (mejor silueta) y k=4 (más detalle, estable); ver informe
km = KMeans(K, n_init=50, random_state=0).fit(Z); F["cluster"] = km.labels_
# etiquetas por orden de mediana del valor
ordc = F.groupby("cluster").lmed.median().sort_values().index; F["cluster"] = F.cluster.map({c: i for i, c in enumerate(ordc)})
print("K =", K); prof = F.groupby("cluster")[cols + ["n_pos"]].median().round(2); prof["n_quipus"] = F.cluster.value_counts().sort_index(); print(prof.T.to_string())
F = F.join(q[["procedencia"]]); F["prefijo"] = F.index.str.extract(r"([A-Z]+)", expand=False)
F.to_csv(D / "tipologia_por_quipu.csv"); prof.to_csv(D / "tipologia_perfiles.csv")
print(pd.crosstab(F.prefijo, F.cluster))
# cruce con procedencia (excluye Unknown/ vagas), permutación de etiquetas DENTRO de cada prefijo de colección
G = F[~F.procedencia.isin(["Unknown", "unknown", "Peru"])].copy()
top = G.procedencia.value_counts(); top = top[top >= 8].index.tolist(); G = G[G.procedencia.isin(top)]
print("procedencias con >=8 quipus:", {p: int((G.procedencia == p).sum()) for p in top})
def tabla(g): return pd.crosstab(g.procedencia, g.cluster).reindex(index=top, columns=range(K), fill_value=0)
def chi(t): e = t.sum(1).values[:, None] * t.sum(0).values[None, :] / t.values.sum(); return (((t.values - e) ** 2) / e).sum()
t0 = tabla(G); c0 = chi(t0); rng = np.random.default_rng(11); nP = 4000
nulls = []; chin = []
lab = G.procedencia.values.copy(); grp = {p: np.where(G.prefijo.values == p)[0] for p in G.prefijo.unique()}
for _ in range(nP):
    l = lab.copy()
    for p, ix in grp.items(): l[ix] = rng.permutation(l[ix])
    g = G.assign(procedencia=l); t = tabla(g); nulls.append(t.values); chin.append(chi(t))
nulls = np.array(nulls); chin = np.array(chin)
print("chi2 observado", round(c0, 1), "p perm (estratificado por prefijo)", (1 + (chin >= c0).sum()) / (nP + 1), "V de Cramer", round(np.sqrt(c0 / (t0.values.sum() * (min(t0.shape) - 1))), 3))
# enriquecimiento por celda
cel = []
for i, p in enumerate(top):
    for j in range(K):
        o = t0.values[i, j]; e = nulls[:, i, j].mean(); pp = (1 + (nulls[:, i, j] >= o).sum()) / (nP + 1); pm = (1 + (nulls[:, i, j] <= o).sum()) / (nP + 1)
        cel.append(dict(procedencia=p, cluster=j, n=t0.values[i].sum(), obs=o, esp=round(e, 1), p_exceso=pp, p_defecto=pm))
cel = pd.DataFrame(cel); cel["q_exceso"] = bh(cel.p_exceso); cel["q_defecto"] = bh(cel.p_defecto)
cel.to_csv(D / "tipologia_x_procedencia.csv", index=False)
print(t0.to_string()); print(cel[(cel.q_exceso < .1) | (cel.q_defecto < .1)].to_string())
print("== sin estratificar (solo informativo):"); 
chi2 = []
for _ in range(2000): chi2.append(chi(tabla(G.assign(procedencia=rng.permutation(G.procedencia.values)))))
print("p perm global", (1 + (np.array(chi2) >= c0).sum()) / 2001)
