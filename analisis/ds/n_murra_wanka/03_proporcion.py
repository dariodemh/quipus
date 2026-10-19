"""03_proporcion.py — ¿Se mueve todo junto y en proporción? Pruebas sin alineación de columnas.
Unidad de análisis: el evento (19 eventos), no la cantidad. Los totales por par de clústeres
son invariantes a la asignación valor->columna que el OCR destruyó.
Salida: resultados_03.json, salida_03.txt
"""
import os, json
import numpy as np, pandas as pd
from scipy import stats
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(20261018)
B = 20000

d = pd.read_csv("wanka_celdas.csv")
orden = ["a","b","c","ch","d","e","f","g","h","i","j","k","l","ll","m","n","o","p","q"]
pares = ["I+II","III+IV","V+VI","VII+VIII","IX+X","XI+XII"]

def matriz(campo):
    M = pd.DataFrame(index=orden, columns=pares, dtype=float)
    for _, r in d.iterrows():
        if campo == "suma":
            v = 0.0 if pd.isna(r.valores) else sum(float(x) for x in str(r.valores).split(";") if x)
        else:
            v = 0.0 if pd.isna(r.valores) else len(str(r.valores).split(";"))
        M.loc[r.evento, r.clusteres] = v
    return M.astype(float)

S = matriz("suma")      # magnitud por macro-grupo y evento
N = matriz("n")         # n.º de cuerdas con dato por macro-grupo y evento

out = {}
def p(*a):
    print(*a)

def corr_media(M, log=False):
    X = np.log10(M.replace(0, np.nan)) if log else M
    C = X.corr(method="spearman").values
    iu = np.triu_indices_from(C, 1)
    return np.nanmean(C[iu]), C

def nulo_corr(M, log=False, B=B):
    X = M.copy()
    obs, _ = corr_media(X, log)
    vals = []
    for _ in range(B):
        Y = X.apply(lambda col: rng.permutation(col.values))
        vals.append(corr_media(Y, log)[0])
    vals = np.array(vals)
    return obs, float((np.sum(vals >= obs) + 1) / (B + 1)), np.nanpercentile(vals, [2.5, 97.5]), vals.std()

p("=== T1. Co-movimiento entre macro-grupos (Spearman entre perfiles de evento) ===")
for nombre, M, lg in [("magnitud (log10 total)", S, True), ("n.º de cuerdas con dato", N, False)]:
    obs, pval, ci, sd = nulo_corr(M, lg)
    out[f"corr_{nombre}"] = dict(obs=float(obs), p=pval, ic=[float(ci[0]), float(ci[1])], sd=float(sd))
    p(f"{nombre:28s} rho medio={obs:+.3f}  nulo 95% [{ci[0]:+.3f},{ci[1]:+.3f}]  p={pval:.4f}")

p("\nMatriz de correlaciones (n.º de cuerdas con dato):")
C = N.corr(method="spearman")
p(C.round(2).to_string())

p("\n=== T2. Estructura de rango 1 (¿mezcla fija escalada?) ===")
X = np.log10(S.replace(0, np.nan))
X = X.dropna(axis=1, how="all")
Z = (X - X.mean()) / X.std(ddof=0)
Z = Z.fillna(0)
u, s, vt = np.linalg.svd(Z.values, full_matrices=False)
var1 = s[0]**2 / (s**2).sum()
vals = []
for _ in range(B):
    Y = Z.apply(lambda col: rng.permutation(col.values)).values
    ss = np.linalg.svd(Y, compute_uv=False)
    vals.append(ss[0]**2 / (ss**2).sum())
vals = np.array(vals)
pval = (np.sum(vals >= var1) + 1) / (B + 1)
p(f"varianza explicada por PC1 = {var1:.3f}; nulo 95% máx = {np.percentile(vals,95):.3f}; p={pval:.4f}")
out["pc1"] = dict(var1=float(var1), p=float(pval), nulo95=float(np.percentile(vals, 95)))

p("\n=== T3. Tendencia temporal por macro-grupo (Spearman evento vs magnitud) ===")
res = []
for c in S.columns:
    rho, pv = stats.spearmanr(np.arange(19), S[c].values)
    res.append((c, rho, pv))
for c, rho, pv in res:
    p(f"{c:12s} rho={rho:+.2f}  p={pv:.3f}")
neg = sum(1 for _, r, _ in res if r < 0)
p(f"macro-grupos con rho<0: {neg}/6; sign test p={stats.binomtest(neg,6,0.5).pvalue:.3f}")
out["tendencia"] = {c: (float(r), float(pv)) for c, r, pv in res}

p("\n=== T4. Desigualdad interna (CV) comparada con Incahuasi ===")
# perfil de cada evento: proporción de cada macro-grupo sobre el total del evento
P = S.div(S.sum(axis=1), axis=0)
cv_evento = (P.std(axis=1, ddof=1) / P.mean(axis=1)).values
p(f"CV entre los 6 macro-grupos, dentro de cada evento: mediana={np.median(cv_evento):.2f} "
  f"[{np.percentile(cv_evento,5):.2f}; {np.percentile(cv_evento,95):.2f}]")
# variabilidad temporal dentro de cada macro-grupo
cvt = (S.std(ddof=1) / S.mean()).values
p(f"CV temporal dentro de cada macro-grupo: {np.round(cvt,2).tolist()}")
out["cv"] = dict(entre_grupos_mediana=float(np.median(cv_evento)), temporal=[float(x) for x in cvt])

p("\n=== T5. Concentración temporal ===")
tot = S.sum().sum()
for e in ["a", "f", "q"]:
    p(f"evento {e}: {100*S.loc[e].sum()/tot:.1f} % de la suma bruta de todos los valores")
prim = S.iloc[:6].sum().sum()
p(f"seis primeros eventos (1533-34): {100*prim/tot:.1f} %")
out["concentracion"] = dict(a=float(S.loc['a'].sum()/tot), f=float(S.loc['f'].sum()/tot),
                            seis=float(prim/tot))

p("\n=== T6. Redondeo decimal (comparación con Incahuasi 15,7 % múltiplos de 10) ===")
W = pd.read_csv("wanka.csv")
v = W.cantidad.values
mult10 = np.mean(v % 10 == 0)
n = len(v)
lo, hi = stats.binomtest(int((v % 10 == 0).sum()), n, 0.10).proportion_ci()
p(f"múltiplos de 10: {mult10:.3f} (n={n}); IC95 binomial [{lo:.3f},{hi:.3f}] bajo p=0,10")
p(f"múltiplos de 5: {np.mean(v % 5 == 0):.3f}")
# bootstrap por evento (respeta que las cantidades se agrupan en 19 eventos)
evs = W.evento.unique()
bs = []
for _ in range(5000):
    pick = rng.choice(evs, len(evs), replace=True)
    vv = pd.concat([W[W.evento == e] for e in pick]).cantidad.values
    bs.append(np.mean(vv % 10 == 0))
p(f"bootstrap por evento: IC95 [{np.percentile(bs,2.5):.3f},{np.percentile(bs,97.5):.3f}]")
out["redondeo"] = dict(mult10=float(mult10), n=int(n), ic=[float(lo), float(hi)],
                       ic_evento=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])

# --- corrección de comparaciones múltiples ---------------------------------
from statsmodels.stats.multitest import multipletests
pruebas = {
    "T1a co-movimiento magnitud": out["corr_magnitud (log10 total)"]["p"],
    "T1b co-movimiento n.º cuerdas": out["corr_n.º de cuerdas con dato"]["p"],
    "T2 rango-1 (PC1)": out["pc1"]["p"],
    "T3 tendencia (sign test)": float(stats.binomtest(neg, 6, 0.5).pvalue),
    "T6 redondeo ×10": float(stats.binomtest(int((v % 10 == 0).sum()), n, 0.10).pvalue),
}
rej, q, _, _ = multipletests(list(pruebas.values()), method="holm")
p("\n=== Corrección de Holm (5 pruebas) ===")
for (k, pv), qq, rr in zip(pruebas.items(), q, rej):
    p(f"{k:34s} p={pv:.2e}  Holm={qq:.2e}  {'significativo' if rr else 'no'}")
out["holm"] = {k: float(qq) for k, qq in zip(pruebas, q)}

json.dump(out, open("resultados_03.json", "w"), indent=1)
