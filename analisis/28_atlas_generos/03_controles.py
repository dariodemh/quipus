# -*- coding: utf-8 -*-
"""Paso 2 (contraste) y paso 5 (controles).
 A. Agrupamiento no supervisado (Ward, rasgos estandarizados) frente a las reglas: ARI, NMI, tabla cruzada.
 B. Barajado de rasgos entre quipus (cada columna por separado, 200 veces): se repite la clasificacion
    y se mide cobertura, convergencia de evidencias y validez externa (NMI genero~procedencia/museo).
 C. Estabilidad: bootstrap de cuerdas dentro de cada quipu (rasgos recalculables) + umbrales movidos +-25 %.
Salidas: contraste_cluster.csv, control_barajado.csv, estabilidad.csv, salida_03_controles.txt
"""
import numpy as np, pandas as pd
from scipy.stats import binom
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score as ari, normalized_mutual_info_score as nmi, silhouette_score
from statsmodels.stats.multitest import multipletests
import reglas as RG

A_ = r"./analisis"
OUT = A_ + r"\28_atlas_generos"
rng = np.random.default_rng(28)
M = pd.read_csv(OUT + r"\matriz.csv", index_col=0)
BASE = RG.clasificar(M)
L = []
say = lambda s: (print(s), L.append(s))

# ------------------------------------------------------------------ A. agrupamiento
def nlog(x, cap=6):
    return np.clip(-np.log10(x.astype(float).fillna(1).clip(lower=1e-12)), 0, cap)

def rasgos(M):
    X = pd.DataFrame(index=M.index)
    X["log_n"] = np.log10(M.n_cuerdas)
    X["anud"] = M.frac_anudada
    X["rota"] = M.frac_rota
    X["nodec"] = M.frac_nodec.fillna(0)
    X["Z"] = M.frac_Z.fillna(M.frac_Z.median())
    X["val"] = M.log_val_med
    X["ncol"] = np.log1p(M.n_colores)
    X["nmi"] = M.nmi_color_grupo.fillna(0)
    X["camel"] = M.okr_frac_camelido.fillna(M.okr_frac_camelido.median())
    X["marc"] = np.log1p(M.okr_marcadoras.fillna(0))
    X["v10"] = (M.vueltas10 > 0).astype(float)
    X["sum"] = np.maximum(nlog(M.sumas_q), nlog(M.filatotal_q))
    X["form"] = nlog(M.form_qbh)
    X["naz"] = nlog(M.nazca_p)
    X["santa"] = nlog(M.santa_q) * (M.santa_pcorpus < .05)
    X["cal"] = nlog(M.calend_q)
    X["tab"] = M.tabla_R.notna().astype(float)
    X["rho"] = M.tabla_rho.fillna(0)
    X["red"] = M.red_frac.fillna(M.red_frac.median())
    X["cuo"] = nlog(M.cuotas_rep_q)
    X["arc"] = M.rel_archivo.map({"bien apoyada": 1, "propuesta": .5}).fillna(0)
    X["trio"] = M.trio_xcx.astype(float)
    X["nonum"] = M.nonum_subtipo.fillna("").str.contains("NC|NU").astype(float)
    X["tally"] = M.pure_tally.astype(float)
    X["segm"] = nlog(M.segm_q)
    return ((X - X.mean()) / X.std().replace(0, 1)).fillna(0)

X = rasgos(M)
K = BASE.genero.nunique()
cl = AgglomerativeClustering(n_clusters=K, linkage="ward").fit_predict(X)
asig = BASE.genero != "SIN"
say(f"A. Ward k={K} sobre {X.shape[1]} rasgos estandarizados")
say(f"   ARI reglas~cluster (todos) = {ari(BASE.genero, cl):.3f}; NMI = {nmi(BASE.genero, cl):.3f}")
say(f"   ARI (solo asignados) = {ari(BASE.genero[asig], cl[asig]):.3f}; NMI = {nmi(BASE.genero[asig], cl[asig]):.3f}")
ct = pd.crosstab(BASE.genero, cl)
ct.to_csv(OUT + r"\contraste_cluster.csv")
say("   tabla cruzada genero x cluster:\n" + ct.to_string())
for g in RG.ORDEN + ["SIN"]:
    row = ct.loc[g]
    c = row.idxmax()
    say(f"   {g}: {row.max()}/{row.sum()} en el cluster {c} (pureza del cluster {row.max()/ct[c].sum():.2f})")
# concordancia con k pequeno (solo la estructura gruesa)
for k in (4, 6, 8, 16):
    c2 = AgglomerativeClustering(n_clusters=k, linkage="ward").fit_predict(X)
    say(f"   k={k}: ARI {ari(BASE.genero, c2):.3f}, NMI {nmi(BASE.genero, c2):.3f}")
sil0 = silhouette_score(X, cl)

# ------------------------------------------------------------------ B. barajado
ID = ["okr", "museo", "region"]
proc0 = M.procedencia
def metricas(Acl, M_):
    a = Acl.genero != "SIN"
    kn = a & (proc0 != "Unknown")
    return dict(alta=(Acl.nivel == 3).mean(), media=(Acl.nivel == 2).mean(), baja=(Acl.nivel == 1).mean(),
                sin=(~a).mean(), lineas2=(Acl.lineas[a] >= 2).mean(), lineas_med=Acl.lineas[a].mean(),
                nmi_proc=nmi(proc0[kn], Acl.genero[kn]), nmi_museo=nmi(M_.museo[a], Acl.genero[a]),
                ari_base=ari(BASE.genero, Acl.genero))
obs = metricas(BASE, M)
B = 200
sims = []
# cada detector se baraja como bloque (sus columnas van juntas); los bloques, de forma independiente
BLOQUES = [["n_cuerdas", "n_colg", "n_grupos", "frac_anudada", "frac_rota", "log_val_med", "transcriptor", "disc_okr"],
           ["frac_nodec"], ["frac_Z"], ["n_colores", "nmi_color_grupo", "color_grupo_p"],
           ["okr_frac_camelido", "okr_frac_lana"], ["okr_marcadoras", "okr_superiores"],
           ["sumas_q", "sumas_q_M1", "sumas_01"], ["filatotal_q"], ["rel_archivo", "trio_xcx", "copias"],
           ["form_Q", "form_holm", "form_qbh", "form_archivo"], ["nazca_p"],
           ["santa_q", "santa_pcorpus", "procedencia"], ["calend_q", "calend_pcorpus"], ["segm_q", "segm_pcorpus"],
           ["tabla_R", "tabla_K", "tabla_q_orden", "tabla_rho"], ["red_n", "red_frac", "red_q"], ["cuotas_rep_q"],
           ["nonum_clase", "nonum_subtipo", "frac_sin_nudo", "pure_tally"], ["vueltas10"]]
assert set(sum(BLOQUES, [])) == set(M.columns) - set(ID), set(M.columns) - set(ID) - set(sum(BLOQUES, []))
for b in range(B):
    S = M.copy()
    for bl in BLOQUES:
        i = rng.permutation(len(S))
        for c in bl:  # columna a columna con el mismo orden: conserva el tipo
            S[c] = S[c].values[i]
    Ab = RG.clasificar(S)
    m = metricas(Ab, M)
    if b < 50:
        try:
            m["sil"] = silhouette_score(rasgos(S), AgglomerativeClustering(n_clusters=K, linkage="ward").fit_predict(rasgos(S)))
        except ValueError:
            m["sil"] = np.nan
    sims.append(m)
sims = pd.DataFrame(sims)
sims.to_csv(OUT + r"\control_barajado.csv", index=False)
say(f"\nB. Barajado de rasgos entre quipus ({B} reps; cada detector permutado como bloque)")
for k_, v in obs.items():
    s = sims[k_]
    # p unilateral en la direccion de la degradacion esperada (observado mayor que barajado)
    p = (1 + (s >= v).sum()) / (1 + len(s))
    say(f"   {k_:10s} observado {v:.3f} | barajado media {s.mean():.3f} [{s.quantile(.025):.3f}, {s.quantile(.975):.3f}] | p(obs<=baraj) {p:.3f}")
say(f"   silueta Ward observada {sil0:.3f} | barajada media {sims.sil.mean():.3f} (max {sims.sil.max():.3f})")

# ------------------------------------------------------------------ C. estabilidad
C = pd.read_csv(A_ + r"\datos\cuerdas.csv")
C["anud"] = (C.nudos.notna() & (C.nudos.astype(str).str.strip() != "")).astype(float)
# reutiliza el parser de 01_matriz sin re-ejecutar el script
src = open(OUT + r"\01_matriz.py", encoding="utf8").read()
ns = {}
exec(src[src.index("def no_decimal"):src.index('C["anudada"]')], {"re": __import__("re"), "np": np}, ns)
nd = C.nudos.map(ns["no_decimal"])
C["nd_ok"] = nd.notna().astype(float)
C["nd"] = nd.fillna(False).astype(float)
C["z_ok"] = C.torsion.isin(["S", "Z"]).astype(float)
C["z"] = (C.torsion == "Z").astype(float)
C["rota"] = (C.terminacion == "B").astype(float)
C["red_ok"] = ((C.anud > 0) & (C.terminacion == "K") & (C.valor >= 10)).astype(float)
C["red"] = (C.red_ok > 0) & (C.valor % 10 == 0)
C["red"] = C.red.astype(float)
C = C[C.kfg.isin(M.index)].reset_index(drop=True)
codes, uniq = pd.factorize(C.kfg)
n_q = np.bincount(codes)
start = np.r_[0, np.cumsum(n_q)[:-1]]
order = np.argsort(codes, kind="stable")
Cs = C.iloc[order].reset_index(drop=True)
codes = codes[order]
VARS = ["anud", "nd_ok", "nd", "z_ok", "z", "rota", "red_ok", "red"]
V = Cs[VARS].values

def recalcula(idx, Mb):
    s = np.vstack([np.bincount(codes, weights=V[idx, j], minlength=len(uniq)) for j in range(len(VARS))]).T
    S = pd.DataFrame(s, index=uniq, columns=VARS)
    Mb.loc[S.index, "frac_anudada"] = S.anud / n_q
    Mb.loc[S.index, "frac_rota"] = S.rota / n_q
    Mb.loc[S.index, "frac_nodec"] = np.where(S.nd_ok > 0, S.nd / S.nd_ok.replace(0, 1), np.nan)
    Mb.loc[S.index, "frac_Z"] = np.where(S.z_ok > 0, S.z / S.z_ok.replace(0, 1), np.nan)
    ok = S.red_ok >= 8
    p = binom.sf(S.red - 1, S.red_ok.clip(lower=1), .1)
    q = np.full(len(S), np.nan)
    q[ok.values] = multipletests(p[ok.values], method="fdr_bh")[1]
    Mb.loc[S.index, "red_n"] = np.where(ok, S.red_ok, np.nan)
    Mb.loc[S.index, "red_frac"] = np.where(ok, S.red / S.red_ok.replace(0, 1), np.nan)
    Mb.loc[S.index, "red_q"] = q
    return Mb

# comprobacion: la version recalculada sin remuestreo reproduce la matriz
M0 = recalcula(np.arange(len(Cs)), M.copy())
A0 = RG.clasificar(M0)
say(f"\nC. Recalculo sin remuestreo: coincide con el atlas en {(A0.genero == BASE.genero).mean():.3f} de los quipus "
    f"(redondeo: corr frac {M0.red_frac.corr(M.red_frac):.3f})")
BB = 200
gen = {"cuerdas": [], "umbrales": [], "ambos": []}
for b in range(BB):
    idx = (start[codes] + np.floor(rng.random(len(Cs)) * n_q[codes]).astype(int))
    Mb = recalcula(idx, M.copy())
    u = {k: v * rng.uniform(.75, 1.25) if isinstance(v, float) else v for k, v in RG.U.items()}
    gen["cuerdas"].append(RG.clasificar(Mb).genero)
    gen["umbrales"].append(RG.clasificar(M0, u).genero)
    gen["ambos"].append(RG.clasificar(Mb, u).genero)
est = pd.DataFrame({k: pd.concat(v, axis=1).eq(A0.genero, axis=0).mean(axis=1) for k, v in gen.items()})
est["genero"] = BASE.genero
est["confianza"] = BASE.confianza
est.to_csv(OUT + r"\estabilidad.csv")
say(f"   estabilidad (fraccion de {BB} replicas con el mismo genero), mediana y fraccion >=0,8:")
for k in ("cuerdas", "umbrales", "ambos"):
    say(f"   {k:9s}: mediana {est[k].median():.2f}; >=0,8 en {(est[k] >= .8).mean():.3f} de los quipus")
say("   por genero (ambos): " + "; ".join(f"{g} {s.median():.2f}/{(s >= .8).mean():.2f}"
                                       for g, s in est.groupby("genero")["ambos"]))
say("   por confianza (ambos): " + "; ".join(f"{g} {s.median():.2f}/{(s >= .8).mean():.2f}"
                                          for g, s in est.groupby("confianza")["ambos"]))
# bootstrap de quipus para el agrupamiento
ar = []
for b in range(100):
    i = rng.choice(len(X), len(X), replace=True)
    cb = AgglomerativeClustering(n_clusters=K, linkage="ward").fit_predict(X.iloc[i])
    ar.append(ari(cl[i], cb))
say(f"   Ward: estabilidad bootstrap de quipus ARI medio {np.mean(ar):.3f} [{np.quantile(ar, .025):.3f}, {np.quantile(ar, .975):.3f}]")
open(OUT + r"\salida_03_controles.txt", "w", encoding="utf8").write("\n".join(L) + "\n")
