"""Tareas 1-2: cuantificacion de violaciones de la convencion decimal y explicacion aburrida
(investigador = prefijo de id, conservacion = terminacion B/R/C y notas, concentracion en pocos quipus).
"""
import numpy as np, pandas as pd
from scipy import stats
from util import *

rng = np.random.default_rng(SEED)
cf = pd.read_csv(AQUI / "cuerdas_flags.csv", keep_default_na=False, low_memory=False)
c = pd.read_csv(AQUI / "racimos.csv")
for x in cf.columns:
    if x.startswith("v_") or x in ("nether", "dir_mixta", "con_nudos"): cf[x] = cf[x].astype(bool)
# serie no decimal: >=2 racimos, todos del mismo tipo L o E (p.ej. 4L;5L;5L, 1E;1E;1E)
g = c.groupby("i").agg(ncl=("tipo", "size"), tipos=("tipo", lambda s: set(s)))
serie = g[(g.ncl >= 2) & g.tipos.apply(lambda s: len(s) == 1 and (s <= {"L"} or s <= {"E"}))].index
cf["v_serie_LE"] = False; cf.loc[serie, "v_serie_LE"] = True
cf["pref"] = cf.kfg.str.extract(r"^([A-Z]+)")[0]
cf["roto"] = cf.terminacion.isin(["B", "R", "C"])
cf["nota_dano"] = cf.notas.str.lower().str.contains("broken|missing|fragment|repair|detached|lost|damag", regex=True)
cf.to_csv(AQUI / "cuerdas_flags2.csv", index=False)

CL = {"nether": "L/E con racimo debajo (nudo inferior)", "v_serie_LE": "serie L/E >=2 racimos (no decimal)", "v_orden": "niveles no decrecientes",
      "v_banda": "racimo fuera de banda del quipu", "v_L10": "L con >=10 vueltas", "v_Emulti": "E con n>1", "v_tiporaro": "tipo raro (EE,LL,BL,SP,TF,U)",
      "v_over9": ">9 simples", "v_L1": "L de 1 vuelta", "v_Spot": "S con aporte no n*10^k", "v_valor_dist": "valor != suma de aportes", "v_alt": "alt != valor"}
k = cf[cf.con_nudos]
Q = k.groupby("kfg").agg(n=("orden", "size"), pref=("pref", "first"), roto=("roto", "mean"), dano=("nota_dano", "mean"))
Q["roto_all"] = cf.groupby("kfg").roto.mean()
Q["n_all"] = cf.groupby("kfg").size()
for x in CL: Q["f_" + x] = k.groupby("kfg")[x].mean(); Q["n_" + x] = k.groupby("kfg")[x].sum()
est = ["nether", "v_serie_LE", "v_banda", "v_L10", "v_Emulti", "v_tiporaro", "v_over9", "v_L1", "v_Spot"]
k = k.assign(v_cualq=k[est].any(axis=1)); Q["f_v_cualq"] = k.groupby("kfg").v_cualq.mean(); Q["n_v_cualq"] = k.groupby("kfg").v_cualq.sum()
CL["v_cualq"] = "cualquiera de las estructurales"
Q.to_csv(AQUI / "tabla_quipus.csv")
nq = len(Q); print("quipus con nudos:", nq, " cuerdas con nudos:", len(k))

# ---------- Tarea 1: prevalencia
rows = []
for x, lab in CL.items():
    nc = int(k[x].sum()) if x != "v_cualq" else int(k.v_cualq.sum())
    q1 = int((Q["n_" + x] >= 1).sum()); q3 = int((Q["n_" + x] >= 3).sum()); q10 = int((Q["f_" + x] >= .10).sum()); q50 = int((Q["f_" + x] >= .5).sum())
    lo, hi = wilson(q1, nq)
    rows.append(dict(clase=x, descripcion=lab, cuerdas=nc, pct_cuerdas=100 * nc / len(k), quipus_ge1=q1, pct_quipus_ge1=100 * q1 / nq,
                     ic95=f"{100*lo:.1f}-{100*hi:.1f}", quipus_ge3=q3, quipus_ge10pct=q10, quipus_ge50pct=q50))
P = pd.DataFrame(rows); P.to_csv(AQUI / "tabla_prevalencia.csv", index=False)
print(P.round(2).to_string())

# concentracion: fraccion de cuerdas anomalas que caen en los 10 quipus top; sobredispersion vs binomial
print("\nConcentracion (cualquiera estructural / nether)")
for x in ["v_cualq", "nether", "v_banda", "v_L10"]:
    s = Q["n_" + x].sort_values(ascending=False); tot = s.sum()
    p0 = tot / Q.n.sum()
    # varianza observada de tasas vs binomial esperada (indice de dispersion ponderado)
    disp = ((Q["n_" + x] - Q.n * p0) ** 2 / (Q.n * p0 * (1 - p0))).sum() / (nq - 1)
    print(f"{x}: top10 quipus={100*s.head(10).sum()/tot:.1f}% de las cuerdas anomalas; top1={100*s.iloc[0]/tot:.1f}%; indice de dispersion={disp:.1f} (1=binomial)")

# ---------- Tarea 2a: investigador (prefijo)
print("\nPor prefijo (investigador/fuente proxy)")
rows = []
pref = Q.pref.values; mask_ok = Q.n >= 5
pt = []
for x in [z for z in CL if z != "v_alt"]:  # v_alt: sin varianza (todo vacio)
    f = Q["f_" + x]
    gr = [f[(Q.pref == p) & mask_ok].values for p in sorted(Q.pref.unique())]
    gr = [a for a in gr if len(a) >= 3]
    H = stats.kruskal(*gr).statistic
    sub = Q[mask_ok]; fv = sub["f_" + x].values; pv = sub.pref.values
    null = []
    for _ in range(4000):
        pp = rng.permutation(pv)
        null.append(stats.kruskal(*[fv[pp == u] for u in np.unique(pp) if (pp == u).sum() >= 3]).statistic)
    row = dict(clase=x, H=H, p=pemp(H, null))
    for u in sorted(Q.pref.unique()):
        s = Q[(Q.pref == u) & mask_ok]; row[f"{u}_pct_quipus>=1"] = 100 * (s["n_" + x] >= 1).mean(); row[f"{u}_tasa_media%"] = 100 * s["f_" + x].mean()
    rows.append(row)
T = pd.DataFrame(rows); T["p_holm"] = holm(T.p); T.to_csv(AQUI / "tabla_prefijo.csv", index=False)
print("n quipus por prefijo (n>=5 cuerdas con nudos):", Q[mask_ok].pref.value_counts().to_dict())
print(T.round(3).to_string())

# ---------- Tarea 2b: conservacion
print("\nConservacion: Spearman estratificado por prefijo (permutacion de roto_all dentro de prefijo)")
res = []
for x in ["v_cualq", "nether", "v_serie_LE", "v_banda", "v_L10", "v_tiporaro"]:
    sub = Q[mask_ok];
    def stat(r):
        tot = 0; w = 0
        for u in sub.pref.unique():
            m = (sub.pref == u).values
            if m.sum() < 8: continue
            rr = stats.spearmanr(r[m], sub["f_" + x].values[m]).statistic
            if np.isfinite(rr): tot += rr * m.sum(); w += m.sum()
        return tot / w
    r0 = sub.roto_all.values; obs = stat(r0); null = []
    for _ in range(2000):
        r = r0.copy()
        for u in sub.pref.unique():
            m = np.where((sub.pref == u).values)[0]; r[m] = rng.permutation(r0[m])
        null.append(stat(r))
    res.append(dict(clase=x, rho_estrat=obs, p=pemp(obs, null, "dos")))
R_ = pd.DataFrame(res); R_["p_holm"] = holm(R_.p); print(R_.round(4).to_string()); R_.to_csv(AQUI / "tabla_conservacion_quipu.csv", index=False)

print("\nConservacion nivel cuerda: permutando el flag anomalo DENTRO de cada quipu (cuerdas con nudos)")
res = []
kk = k.reset_index(drop=True); grp = kk.groupby("kfg").indices
for x in ["v_cualq", "nether", "v_serie_LE", "v_banda", "v_L10"]:
    a = kk[x].values.astype(int); b = kk.roto.values.astype(int)
    obs = (a * b).sum(); null = np.zeros(2000)
    idx = [v for v in grp.values() if a[v].sum() > 0 and a[v].sum() < len(v)]
    for t in range(2000):
        s = 0
        for v in idx: s += (rng.permutation(a[v]) * b[v]).sum()
        null[t] = s
    fixed = sum((a[v] * b[v]).sum() for v in idx)
    res.append(dict(clase=x, anom_rotas_obs=fixed, esperado=null.mean(), p=pemp(fixed, null, "dos"),
                    pct_rotas_en_anom=100 * (a * b).sum() / a.sum(), pct_rotas_en_resto=100 * ((1 - a) * b).sum() / (1 - a).sum()))
R2 = pd.DataFrame(res); R2["p_holm"] = holm(R2.p); print(R2.round(4).to_string()); R2.to_csv(AQUI / "tabla_conservacion_cuerda.csv", index=False)

# notas que mencionan "knot" en cuerdas anomalas vs no
print("\nNotas libres: % con alguna nota en anomalas vs resto")
for x in ["nether", "v_banda"]:
    print(x, f"{100*(k[k[x]].notas!='').mean():.1f}% vs {100*(k[~k[x]].notas!='').mean():.1f}%")
