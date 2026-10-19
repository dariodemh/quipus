"""Tablas del mapa: por regla, procedencia, tamano, rasgos estructurales, generos y modelo.

Unidad = quipu. La tasa neta resta el nulo (valores barajados dentro del quipu).
"""
import numpy as np, pandas as pd
from pathlib import Path
A = Path(__file__).resolve().parent
B = pd.read_csv(A / "cuerdas_legibles.csv")
R = pd.read_csv(A / "quipus_legibles.csv")
O = pd.read_csv(A / "inter_pred.csv")
RR = pd.read_csv(A / "reglas_resumen.csv")
rng = np.random.default_rng(20261018)
B["reglas_hit"] = B["reglas_hit"].fillna("")
# atribuir tambien las reglas entre quipus
M0 = pd.read_csv(A / "mapa_l0.csv")
mm = {(k, s): v for k, s, v in M0.itertuples(index=False)}
for r in O.itertuples():
    if r.hit:
        j = B.index[(B.kfg == r.kfg) & (B.i == mm[(r.kfg, r.i)])][0]
        prev = B.at[j, "reglas_hit"]
        B.at[j, "reglas_hit"] = (prev + ";" if prev else "") + r.regla

# ---------------------------------------------------------------- duplicados / copias
pares = []
for (a, b), d in O[O.regla == "copia_quipu"].groupby(["kfg", "otro"]):
    if a < b:
        pares.append(dict(a=a, b=b, n=len(d), hit=int(d.hit.sum()), fr=d.hit.mean()))
P = pd.DataFrame(pares)
P["duplicado"] = (P.n >= 8) & (P.fr >= 0.75) if len(P) else pd.Series(dtype=bool)
dup_quipus = set(P[P.duplicado].a) | set(P[P.duplicado].b)
print("=== parejas con >=8 predicciones de copia y >=75%% identicas (mismo objeto o copia literal) ===")
print(P[P.duplicado].sort_values("fr", ascending=False).round(3).to_string(index=False))
P.to_csv(A / "pares_copia.csv", index=False)
print("quipus implicados:", len(dup_quipus))

# ---------------------------------------------------------------- tabla global
nv = R.nval.sum(); h = R.hit.sum()
print("\n=== GLOBAL ===")
print("quipus %d (con valor %d); cuerdas con valor %d" % (len(R), int(R.nval.gt(0).sum()), nv))
print("cuerdas con >=1 via: %d (%.1f%%); con acierto exacto: %d (%.2f%%); nulo esperado %.2f%% (exceso %.2f puntos)"
      % (R.via.sum(), 100 * R.via.sum() / nv, h, 100 * h / nv, 100 * R.hit_null.sum() / nv,
         100 * (h - R.hit_null.sum()) / nv))
print("quipus con q<0.05 (BH sobre 641): %d (%.1f%%)" % (R.sig.sum(), 100 * R.sig.mean()))
print("quipus con tasa_neta>0.10: %d ; >0.25: %d ; =0 (sin exceso): %d"
      % ((R.tasa_neta > 0.10).sum(), (R.tasa_neta > 0.25).sum(), (R.tasa_neta <= 0).sum()))

print("\n=== POR REGLA (cuerdas cubiertas; nulo = misma maquinaria con valores barajados) ===")
print(RR.round(3).to_string(index=False))

print("\n=== POR PROCEDENCIA (>=5 quipus) ===")
g = B.groupby("procedencia").agg(nq=("kfg", "nunique"), nc=("hit", "size"), via=("via", "sum"),
                                 hit=("hit", "sum"), pn=("p_null", "sum"))
g["tasa"] = g.hit / g.nc; g["neta"] = (g.hit - g.pn) / g.nc; g["cob"] = g.via / g.nc
G = g[g.nq >= 5].sort_values("neta", ascending=False)
print(G.round(3).to_string())
G.to_csv(A / "por_procedencia.csv")

# test por procedencia: suma de los aciertos frente a la distribucion nula agregada (mismas permutaciones)
NZ = np.load(A / "nulo_resumen.npz")
orden = sorted(R.kfg)
pos = {k: i for i, k in enumerate(orden)}
NQ = NZ["por_quipu"]
def p_agregado(ks):
    idx = [pos[k] for k in ks]
    nul = NQ[idx].sum(0)
    obs = int(R.set_index("kfg").loc[ks, "hit"].sum())
    return (1 + int((nul >= obs).sum())) / (len(nul) + 1), obs, float(nul.mean())
res = [p_agregado(list(B[B.procedencia == p].kfg.unique())) for p in G.index]
G["p_perm"] = [x[0] for x in res]; G["obs"] = [x[1] for x in res]; G["nul_agr"] = [x[2] for x in res]
m = len(G); pv = G.p_perm.to_numpy(); o = np.argsort(pv); q = np.empty(m); prev = 1
for t in range(m - 1, -1, -1):
    prev = min(prev, pv[o][t] * m / (t + 1)); q[t] = prev
G["q_perm"] = np.nan; G.iloc[o, G.columns.get_loc("q_perm")] = q
print("\ncon q_perm<0.05:", list(G[G.q_perm < 0.05].index))
G.to_csv(A / "por_procedencia.csv")

print("\n=== TAMANO Y RASGOS ===")
R["cubo"] = pd.cut(R.nval, [0, 10, 20, 50, 100, 200, 10000], right=False)
print(R.groupby("cubo", observed=True).agg(nq=("kfg", "size"), nval=("nval", "median"),
      neta=("tasa_neta", "mean"), cob=("cobertura", "mean"), ac=("acierto_si_via", "mean"),
      sig=("sig", "sum")).round(3).to_string())
for col, lab in [("nT", "tiene cuerdas superiores T"), ("nsub", "tiene subsidiarias")]:
    R[lab] = R[col] > 0
    print("\n%s:\n%s" % (lab, R.groupby(lab).agg(nq=("kfg", "size"), neta=("tasa_neta", "mean"),
          cob=("cobertura", "mean"), sig=("sig", "mean")).round(3).to_string()))
R["tiene_copia"] = R.via_inter > 0
print("\ncopia entre quipus:\n%s" % R.groupby("tiene_copia").agg(nq=("kfg", "size"),
      neta=("tasa_neta", "mean"), hit=("hit", "sum"), sig=("sig", "mean")).round(3).to_string())

# correlaciones (Spearman) con la tasa neta, sin duplicados
from scipy.stats import spearmanr
sub = R[(R.nval >= 10) & (~R.kfg.isin(dup_quipus))].copy()
sub["lnval"] = np.log(sub.nval); sub["subfrac"] = sub.nsub / sub.n
print("\n=== correlaciones con tasa_neta (quipus nval>=10, sin duplicados, n=%d) ===" % len(sub))
for col in ["lnval", "div", "media_grupo", "ngrupos", "subfrac", "nT", "maxv"]:
    r, p = spearmanr(sub[col], sub.tasa_neta)
    print("%-10s rho=%+.3f  p=%.2g" % (col, r, p))

# ---------------------------------------------------------------- modelo OLS con bootstrap
def ols_boot(df, y, X, nboot=2000):
    Xm = np.column_stack([np.ones(len(df))] + [df[c].to_numpy(float) for c in X])
    yv = df[y].to_numpy(float)
    b = np.linalg.lstsq(Xm, yv, rcond=None)[0]
    pred = Xm @ b; r2 = 1 - ((yv - pred) ** 2).sum() / ((yv - yv.mean()) ** 2).sum()
    bs = []
    for _ in range(nboot):
        i = rng.integers(0, len(df), len(df))
        bs.append(np.linalg.lstsq(Xm[i], yv[i], rcond=None)[0])
    bs = np.array(bs)
    return b, np.percentile(bs, [2.5, 97.5], axis=0), r2

sub["proc_g"] = sub.procedencia.where(sub.procedencia.isin(
    ["Incahuasi", "Pachacamac", "Ica", "Leymebamba", "Huaquerones", "Nazca"]), "Otra")
for p in ["Pachacamac", "Ica", "Leymebamba", "Huaquerones", "Nazca", "Otra"]:
    sub["p_" + p] = (sub.proc_g == p).astype(float)
X = ["lnval", "div", "media_grupo", "subfrac", "nT", "p_Pachacamac", "p_Ica", "p_Leymebamba",
     "p_Huaquerones", "p_Nazca", "p_Otra"]
b, ci, r2 = ols_boot(sub, "tasa_neta", X)
M = pd.DataFrame(dict(var=["const"] + X, b=b, lo=ci[0], hi=ci[1]))
M["sig"] = np.sign(M.lo) == np.sign(M.hi)
print("\n=== OLS tasa_neta ~ rasgos (n=%d, referencia=Incahuasi); R2=%.3f ===" % (len(sub), r2))
print(M.round(4).to_string(index=False))
M.to_csv(A / "modelo_ols.csv", index=False)

# ---------------------------------------------------------------- generos
def genero(d):
    rh = [x for s in d.reglas_hit for x in s.split(";") if x]
    from collections import Counter
    c = Counter(rh)
    if not rh:
        return "sin redundancia"
    adit = sum(c[r] for r in ("cierre", "superior", "grupo_total", "subs", "subs_res", "suma_dos"))
    cop = c["copia"] + c["copia_quipu"] + c["copia_grupo"]; rep = c["hija_unica"]
    tot = adit + cop + rep
    if tot == 0:
        return "sin redundancia"
    if adit >= 0.5 * tot and adit >= 2:
        return "aditivo interno"
    if cop >= 0.5 * tot and cop >= 2:
        return "copia entre quipus"
    if rep >= 0.5 * tot:
        return "repeticion jerarquica"
    return "mixto"
R["genero"] = [genero(B[B.kfg == k]) for k in R.kfg]
print("\n=== GENEROS ===")
print(R[R.nval > 0].groupby("genero").agg(nq=("kfg", "size"), nval=("nval", "median"),
      neta=("tasa_neta", "mean"), cob=("cobertura", "mean"), ac=("acierto_si_via", "mean"),
      sig=("sig", "sum")).round(3).to_string())
R.to_csv(A / "quipus_legibles.csv", index=False)

# ---------------------------------------------------------------- top 20 fuera de Incahuasi
print("\n=== TOP 20 FUERA DE INCAHUASI (nval>=20, sin duplicados, ordenado por tasa_neta) ===")
T = R[(R.procedencia != "Incahuasi") & (R.nval >= 20) & (~R.kfg.isin(dup_quipus))]
T = T.sort_values("tasa_neta", ascending=False).head(20)
for r in T.itertuples():
    d = B[B.kfg == r.kfg]
    from collections import Counter
    c = Counter(x for s in d[d.hit == 1].reglas_hit for x in s.split(";") if x)
    print("%-8s %-28s nval=%3d hit=%2d (nulo %4.1f) neta=%.2f cob=%.2f ac=%.2f q=%.3f %s"
          % (r.kfg, str(r.procedencia)[:28], r.nval, r.hit, r.hit_null, r.tasa_neta,
             r.cobertura, r.acierto_si_via if r.acierto_si_via == r.acierto_si_via else -1,
             r.q, dict(c.most_common(3))))
T.to_csv(A / "top20_fuera_incahuasi.csv", index=False)
