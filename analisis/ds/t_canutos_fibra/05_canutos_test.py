"""
Controles para canutos:
 (a) prevalencia vs procedencia / fibra / tamano, con nulo por permutacion
 (b) en los 8 quipus con registro detallado: los segmentos de canuto son
     unidades contables? (homogeneidad interna y sumas redondas) frente a un
     nulo de segmentaciones contiguas aleatorias con la MISMA distribucion de
     tamanos, dentro del mismo quipu.
 (c) alineamiento con limites de grupo en el unico quipu con grupos reales
     (UR052), con nulo de limites aleatorios.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20241018)
NPERM = 20000

q = pd.read_csv(os.path.join(OUT, "quipus.csv"))
cord = pd.read_csv(os.path.join(OUT, "cuerdas_okr.csv"), low_memory=False)

print("=" * 72)
print("(a) PREVALENCIA DE CANUTOS")
q["can"] = (q.num_canuto_cords > 0).astype(int)
q["can_full"] = (q.prop_canuto >= 0.5).astype(int)
q["S"] = (q.percent_s_knots > 0.5).astype(int)
q["cam"] = (q.n_CL > 0).astype(int)


def perm_chi2(y, g):
    g = pd.Series(g).astype(str).values
    y = np.asarray(y)
    t = pd.crosstab(pd.Series(g), pd.Series(y)).values
    obs = stats.chi2_contingency(t)[0]
    cnt = 0
    for _ in range(5000):
        yp = rng.permutation(y)
        tt = pd.crosstab(pd.Series(g), pd.Series(yp)).values
        tt = tt[tt.sum(1) > 0][:, tt.sum(0) > 0]
        if tt.shape[0] < 2 or tt.shape[1] < 2:
            continue
        if stats.chi2_contingency(tt)[0] >= obs:
            cnt += 1
    return obs, (cnt + 1) / 5001


print("quipus con >=1 canuto: %d/%d (%.1f%%)" % (q.can.sum(), len(q), 100 * q.can.mean()))
print("envoltura >=50%%: %d (%.1f%%)" % (q.can_full.sum(), 100 * q.can_full.mean()))
print("\npor zona:")
t = q.groupby("zona").agg(n=("can", "size"), can=("can", "sum"),
                          full=("can_full", "sum"))
t["pct"] = (100 * t.can / t.n).round(1)
print(t.sort_values("can", ascending=False).to_string())
for var in ["zona"]:
    print("chi2 %s: %.1f p=%.4f" % ((var,) + perm_chi2(q.can, q[var])))
print("\ncanuto vs tamano (num_cords): mediana con=%0.0f sin=%0.0f"
      % (q.loc[q.can == 1, "num_cords"].median(), q.loc[q.can == 0, "num_cords"].median()))
print("  Mann-Whitney p=%.4f" % stats.mannwhitneyu(
    q.loc[q.can == 1, "num_cords"], q.loc[q.can == 0, "num_cords"]).pvalue)
print("\ncanuto vs fibra:")
print(pd.crosstab(q.can, q.cam, margins=True).to_string())
print("  Fisher p=%.4f" % stats.fisher_exact(pd.crosstab(q.can, q.cam))[1])
print("\ncanuto vs estilo de nudo (S dominante):")
print(pd.crosstab(q.can, q.S, margins=True).to_string())
print("  Fisher p=%.4f" % stats.fisher_exact(pd.crosstab(q.can, q.S))[1])
print("\nperfil de los 8 quipus con registro OKR completo:")
cols = ["okr", "kfg_name", "zona", "num_cords", "num_ascher_colors", "mean_cord_value",
        "percent_s_knots", "n_CL", "n_CN", "pc_estructura"]
print(q[q.n_canuto > 0][cols].round(2).to_string(index=False))
print("\n(mediana de los 8 vs resto)")
c8 = q[q.n_canuto > 0]
for c in ["num_cords", "num_ascher_colors", "mean_cord_value", "percent_s_knots"]:
    print("  %-20s %8.1f  vs %8.1f" % (c, c8[c].median(), q.loc[q.n_canuto == 0, c].median()))

# ------------------------------------------------------------------ (b)
print("\n" + "=" * 72)
print("(b) LOS SEGMENTOS DE CANUTO SON UNIDADES CONTABLES?")
res = []
for kid in q.loc[q.n_canuto > 0, "KHIPU_ID"]:
    g = cord[(cord.KHIPU_ID == kid) & (cord.CORD_LEVEL == 1)].sort_values("CORD_ORDINAL")
    if len(g) < 10:
        continue
    val = g.valor.fillna(0).values.astype(float)
    # tamano de cada segmento segun los 236 canutos
    seg = pd.read_sql("select CTO_BEG_CORD,CTO_END_CORD,NUM_CORDS from canuto where KHIPU_ID=%d" % kid,
                      __import__("sqlite3").connect(
                          os.path.join(r".",
                                       "data", "external", "open-khipu-repository",
                                       "data", "khipu.db")))
    seg = seg.sort_values("CTO_BEG_CORD")
    sizes = seg.NUM_CORDS.values
    n = len(val)
    # sumas observadas (solo si los segmentos cubren el vector)
    if sizes.sum() != n:
        print("  %s: cobertura %d de %d cuerdas (se omite)" % (kid, sizes.sum(), n))
        continue
    pos = np.concatenate([[0], np.cumsum(sizes)])
    sums = np.array([val[pos[i]:pos[i + 1]].sum() for i in range(len(sizes))])
    # nulo: mismos tamanos en orden aleatorio (barajar cuerdas)
    nb = 3000
    rnd_sums = []
    for _ in range(nb):
        v = rng.permutation(val)
        rnd_sums.append(np.array([v[pos[i]:pos[i + 1]].sum() for i in range(len(sizes))]))
    rnd_sums = np.array(rnd_sums)
    obs_round = np.mean(sums % 10 == 0)
    null_round = np.mean(rnd_sums % 10 == 0, axis=1)
    p_round = (np.sum(null_round >= obs_round) + 1) / (nb + 1)
    obs_cv = np.std(sums) / (np.mean(sums) + 1e-9)
    null_cv = np.std(rnd_sums, axis=1) / (np.mean(rnd_sums, axis=1) + 1e-9)
    p_cv = (np.sum(null_cv <= obs_cv) + 1) / (nb + 1)
    res.append(dict(quipu=kid, n=n, n_seg=len(sizes), med_cords_seg=np.median(sizes),
                    frac_sumas_redondas=obs_round, p_redondas=p_round,
                    cv_sumas=obs_cv, p_homogeneidad=p_cv))
B = pd.DataFrame(res)
print(B.round(3).to_string(index=False))
print("\nmedia de frac. de sumas redondas = %.3f (azar ~0.10)" % B.frac_sumas_redondas.mean())
print("quipus con p_redondas<0.05: %d de %d" % ((B.p_redondas < .05).sum(), len(B)))

# ------------------------------------------------------------------ (c)
print("\n" + "=" * 72)
print("(c) ALINEAMIENTO CON GRUPOS (UR052 / KH0282)")
kid = q.loc[q.kfg_name == "UR052", "KHIPU_ID"].iloc[0]
g = cord[(cord.KHIPU_ID == kid) & (cord.CORD_LEVEL == 1)].sort_values("CORD_ORDINAL")
import sqlite3
con = sqlite3.connect(os.path.join(r".",
                                   "data", "external", "open-khipu-repository",
                                   "data", "khipu.db"))
lim_can = sorted(int(x) for x in pd.read_sql(
    "select CTO_END_CORD from canuto where KHIPU_ID=%d" % kid, con).CTO_END_CORD)
seq = g.grupo.fillna(-9).astype(int).values
lim_grp = [i for i in range(1, len(seq)) if seq[i] != seq[i - 1]]


def jac(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b)


obs = jac(lim_can, lim_grp)
cnt = 0
for _ in range(NPERM):
    a = set(rng.choice(np.arange(1, len(seq)), size=len(lim_can), replace=False))
    if jac(a, lim_grp) >= obs:
        cnt += 1
print("n cuerdas=%d  n limites canuto=%d  n limites grupo=%d  Jaccard=%.3f  p_perm=%.5f"
      % (len(seq), len(lim_can), len(lim_grp), obs, (cnt + 1) / (NPERM + 1)))
print("coincidencias exactas: %d de %d limites de grupo"
      % (len(set(lim_can) & set(lim_grp)), len(lim_grp)))
print("\ngrupos y canutos de UR052 (posicion en el cordon principal):")
gg = pd.read_csv(os.path.join(r".", "analisis", "datos", "grupos.csv"))
gg = gg[gg.kfg == "UR052"]
print(gg[["grupo", "pos_cm", "desde", "hasta", "espacio_cm"]].head(12).to_string(index=False))
cc = pd.read_sql("select ORDINAL,START_POSITION,END_POSITION,NUM_CANUTOS,SPACING from canuto_cluster where KHIPU_ID=%d" % kid, con)
print(cc.to_string(index=False))
B.to_csv(os.path.join(OUT, "canutos_segmentos.csv"), index=False)
