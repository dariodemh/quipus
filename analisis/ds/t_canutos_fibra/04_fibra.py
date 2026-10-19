"""
Fibra (algodon CN vs camelido CL) y su asociacion con valor, color,
posicion y procedencia.  Unidad = QUIPU.

Todo contraste lleva nulo por permutacion (semilla fija 20241018) y
p-valor empirico; correccion de multiplicidad BH al final.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

BASE = r"."
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20241018)
NPERM = 20000

q = pd.read_csv(os.path.join(OUT, "quipus.csv"))
cord = pd.read_csv(os.path.join(OUT, "cuerdas_okr.csv"), low_memory=False)
cord["fib"] = cord.FIBER.replace({"": np.nan}).fillna("NA")

# poblacion: quipus con fibra codificada (CN/CL) en al menos una cuerda
P = q[(q.n_CN + q.n_CL) > 0].copy()
P["camelido"] = (P.n_CL > 0).astype(int)
P["n_cod"] = P.n_CN + P.n_CL
P["pCL"] = P.n_CL / P.n_cod
P["colores_por_cuerda"] = P.num_ascher_colors / P.num_cords.replace(0, np.nan)
P["log_n"] = np.log10(P.num_cords.clip(lower=1))
P["canuto"] = (P.num_canuto_cords > 0).astype(int)

print("=" * 72)
print("POBLACION: %d quipus con fibra codificada; %d con >=1 cuerda camelido (%.1f%%)"
      % (len(P), P.camelido.sum(), 100 * P.camelido.mean()))
print("de los %d con camelido: %d son 100%% camelido, %d mixtos"
      % (P.camelido.sum(), (P.pCL == 1).sum(), ((P.pCL > 0) & (P.pCL < 1)).sum()))

print("\n--- fibra del cordon principal vs cuerdas colgantes ---")
ct = pd.crosstab(q.pc_fibra.fillna("NA"), q.n_CL > 0)
print(ct.to_string())
sub = q[q.pc_fibra.isin(["CN", "CL"])]
phi = stats.chi2_contingency(pd.crosstab(sub.pc_fibra, sub.n_CL > 0))[0]
print("chi2=%.1f  (n=%d)  -> la fibra es un atributo de quipu completo" % (phi, len(sub)))

print("\n--- fibra vs MUSEO/COLECCION (posible confusor de registro) ---")
mus = q[q.n_CN + q.n_CL > 0].copy()
mus["cam"] = (mus.n_CL > 0).astype(int)
t = mus.groupby("MUSEUM_NAME").agg(n=("cam", "size"), cam=("cam", "sum"))
print(t[t.cam > 0].sort_values("cam", ascending=False).to_string())
print("museos con >=1 camelido: %d de %d con fibra codificada" % ((t.cam > 0).sum(), len(t)))

print("\n" + "=" * 72)
print("A. FIBRA vs PROCEDENCIA (zona)")
tab = pd.crosstab(P.zona, P.camelido)
print(tab.to_string())
# Monte Carlo de chi2 (las celdas son chicas)
tabv = tab.values
chi_obs = stats.chi2_contingency(tabv)[0]
row = tabv.sum(1, keepdims=True)
tot = tabv.sum()


def chi2_perm(rng, labels, groups, reps=5000):
    """permuta las etiquetas camelido entre quipus y recalcula chi2."""
    out = []
    y = np.asarray(labels)
    g = pd.Series(groups).astype(str).values
    for _ in range(reps):
        yp = rng.permutation(y)
        t = pd.crosstab(pd.Series(g), pd.Series(yp)).values
        t = t[t.sum(1) > 0][:, t.sum(0) > 0]
        if t.shape[0] < 2 or t.shape[1] < 2:
            out.append(0.0)
        else:
            out.append(stats.chi2_contingency(t)[0])
    return np.array(out)


null = chi2_perm(rng, P.camelido.values, P.zona.values)
p_zona = (null >= chi_obs).mean()
print("chi2=%.1f  p_perm=%.4f" % (chi_obs, p_zona))

print("\n" + "=" * 72)
print("B. FIBRA vs TAMANO, COLOR, VALOR (continuas) -- permutacion simple")
cont = ["num_cords", "num_ascher_colors", "colores_por_cuerda", "mean_cord_value",
        "percent_s_knots", "knot_cluster_count"]


def perm_diff(df, col, y="camelido", reps=NPERM):
    d = df[[col, y]].dropna()
    a = d.loc[d[y] == 1, col].values
    b = d.loc[d[y] == 0, col].values
    if len(a) < 3 or len(b) < 3:
        return np.nan, np.nan, np.nan
    obs = np.median(a) - np.median(b)
    pool = np.concatenate([a, b])
    k = len(a)
    cnt = 0
    for _ in range(reps):
        rng.shuffle(pool)
        if abs(np.median(pool[:k]) - np.median(pool[k:])) >= abs(obs):
            cnt += 1
    return obs, (cnt + 1) / (reps + 1), len(a)


res = []
for c in cont:
    obs, p, na = perm_diff(P, c)
    res.append(dict(variable=c, dif_mediana=obs, p_perm=p, n_cl=na,
                    med_cl=P.loc[P.camelido == 1, c].median(),
                    med_cn=P.loc[P.camelido == 0, c].median()))
R = pd.DataFrame(res)
print(R.round(3).to_string(index=False))

print("\n" + "=" * 72)
print("C. CONTROL DE LA EXPLICACION ABURRIDA: tamano")
P["q_n"] = pd.qcut(P.num_cords, 4, labels=False, duplicates="drop")
tab2 = pd.crosstab(P.q_n, P.camelido)
print(tab2.to_string())
# permutacion ESTRATIFICADA por cuartil de tamano
obs = P.groupby("q_n").camelido.mean()
obs_stat = ((obs * P.groupby("q_n").size()).sum() / len(P))  # = tasa global, no informa
# estadistico: exceso de camelidos en los dos cuartiles grandes
big = P.q_n.isin([2, 3])
obs_frac = P.loc[big, "camelido"].mean() - P.loc[~big, "camelido"].mean()
cnt = 0
y = P.camelido.values.copy()
for _ in range(NPERM):
    yp = y.copy()
    for g in P.q_n.unique():
        idx = np.where(P.q_n.values == g)[0]
        yp[idx] = rng.permutation(yp[idx])
    d = yp[big.values].mean() - yp[~big.values].mean()
    if abs(d) >= abs(obs_frac):
        cnt += 1
print("diferencia de tasa camelido (2 cuartiles grandes - 2 chicos) = %.3f, p=%.4f"
      % (obs_frac, (cnt + 1) / (NPERM + 1)))
print("pCL medio por cuartil de tamano:")
print(P.groupby("q_n").agg(n=("camelido", "size"), tasa=("camelido", "mean"),
                           med_cords=("num_cords", "median")).round(3).to_string())

print("\n" + "=" * 72)
print("D. DENTRO DE LOS QUIPUS MIXTOS (unica via no confundida)")
mix = P[(P.pCL > 0) & (P.pCL < 1)]
print(mix[["okr", "kfg_name", "n_cod", "n_CL", "n_CN"]].to_string(index=False))
x = cord[(cord.fib.isin(["CN", "CL"])) & (cord.KHIPU_ID.isin(mix.KHIPU_ID))].copy()
x["blanco"] = x.color.fillna("").astype(str).str.startswith("W").astype(int)
x["con_nudos"] = (x.valor.fillna(0) > 0).astype(int)
x["logv"] = np.log10(x.valor.clip(lower=1))
rows = []
for kid, g in x.groupby("KHIPU_ID"):
    for var in ["logv", "blanco", "CORD_LEVEL", "CORD_LENGTH"]:
        a = g.loc[g.fib == "CL", var].dropna()
        b = g.loc[g.fib == "CN", var].dropna()
        if len(a) < 4 or len(b) < 4:
            continue
        obs = a.median() - b.median()
        pool = np.concatenate([a.values, b.values])
        k = len(a)
        cnt = 0
        for _ in range(5000):
            rng.shuffle(pool)
            if abs(np.median(pool[:k]) - np.median(pool[k:])) >= abs(obs):
                cnt += 1
        rows.append(dict(quipu=kid, variable=var, n_cl=len(a), n_cn=len(b),
                         dif=obs, p=(cnt + 1) / 5001))
D = pd.DataFrame(rows)
print(D.round(3).to_string(index=False))

print("\n" + "=" * 72)
print("E. RESUMEN DE p-VALORES Y BH")
allp = []
for _, r in R.iterrows():
    allp.append(("quipu:" + r.variable, r.p_perm))
for _, r in D.iterrows():
    allp.append(("cuerda:%s:%s" % (r.quipu, r.variable), r.p))
allp.append(("quipu:zona", p_zona))
allp.append(("quipu:tamano_estratificado", (cnt + 1) / (NPERM + 1)))
A = pd.DataFrame(allp, columns=["prueba", "p"])
A["p_BH"] = stats.false_discovery_control(A.p.values)
print(A.sort_values("p").round(4).to_string(index=False))
A.to_csv(os.path.join(OUT, "fibra_pvalores.csv"), index=False)
R.to_csv(os.path.join(OUT, "fibra_quipu.csv"), index=False)
D.to_csv(os.path.join(OUT, "fibra_cuerda_mixtos.csv"), index=False)
