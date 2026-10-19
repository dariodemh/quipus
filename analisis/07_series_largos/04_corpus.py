"""Paso 4: busqueda en todo el corpus de cuerdas con series de largos (serie_L: >=2 racimos, todos L de un nudo)
y comparacion de estilo con los 9 quipus foco. Ademas: sensibilidad de UR144 a la fuente (KFG vs OKR).
Salidas: 04_salida.txt, tabla_corpus_series.csv
"""
import sys
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import hypergeom

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(AQUI.parent / "06_nudos"))
from util import pemp, SEED

f = open(AQUI / "04_salida.txt", "w", encoding="utf-8")
def P(*a):
    print(*a); print(*a, file=f)

F = ["UR039", "UR050", "UR051", "UR052", "UR054", "UR055", "UR110", "UR112", "UR144"]
ARTEF = {"AS090_N2", "AS019", "AS004", "UR211", "UR1095", "UR193", "KH0001"}  # n = valor (06_nudos)
Q = pd.read_csv(AQUI / "01_quipus.csv")
qu = pd.read_csv(RAIZ / "analisis/datos/quipus.csv")
r = pd.read_csv(RAIZ / "analisis/06_nudos/racimos.csv", low_memory=False)

# --- estilo de las cuerdas serie_L por quipu (KFG)
g = r.sort_values(["i", "j"]).groupby("i")
c = g.agg(kfg=("kfg", "first"), k=("j", "size"), allL=("tipo", lambda s: (s == "L").all()),
          w=("n", list), p=("pos", list), d=("dir", "".join))
c = c[c.allL & (c.k >= 2) & c.w.map(lambda w: not any(x != x for x in w))]
filas = []
for q, h in c.groupby("kfg"):
    if len(h) < 5: continue
    w = np.concatenate(h.w.values); gaps = [x for p in h.p for x in np.diff(p)]
    dd = "".join(h.d)
    filas.append(dict(quipu=q, serie=len(h), frac_quipu=Q.set_index("kfg").frac_kfg.get(q, np.nan), foco=q in F,
                      artefacto_n_valor=q in ARTEF, procedencia=qu.set_index("kfg").procedencia.get(q),
                      vueltas_media=w.mean(), frac_4a6=np.mean((w >= 4) & (w <= 6)), frac_le3=np.mean(w <= 3),
                      L10=np.mean(w >= 10), dirS=dd.count("S") / max(1, dd.count("S") + dd.count("Z")),
                      hueco_med=np.median(gaps), k_medio=h.k.mean(),
                      sd_dentro=np.mean([np.std(x) for x in h.w]),
                      top=", ".join(f"{'-'.join(str(int(v)) for v in k)}x{n}" for k, n in Counter(map(tuple, h.w)).most_common(3))))
C = pd.DataFrame(filas).sort_values("frac_quipu", ascending=False)
C.to_csv(AQUI / "tabla_corpus_series.csv", index=False)
P("=== Quipus con >=5 cuerdas serie_L (KFG)")
P(C.round(2).to_string(index=False))

# --- concentracion: cuantos quipus tienen >=30 % de cuerdas serie_L y cuantos de ellos son de canuto
nq = Q.kfg_cuerdas_nudo.gt(0).sum()
alto = Q[(Q.frac_kfg >= 0.3) & (Q.kfg_cuerdas_nudo >= 10)]
P(f"\nQuipus con >=30 % serie_L y >=10 cuerdas con nudos: {len(alto)} de {nq}: {list(alto.kfg)}")
cnt = Q[Q.okr_canutos > 0]
P("Quipus con canutos en OKR:", list(cnt.kfg), "| rango de frac_kfg entre", nq, "quipus:",
  dict(zip(cnt.kfg, Q.frac_kfg.rank(ascending=False)[cnt.index].astype(int))))
k_top = int((Q.frac_kfg.rank(ascending=False, method="min")[cnt.index] <= 9).sum())
P(f"P(hipergeometrica) de que >= {k_top} de {len(cnt)} quipus de canuto caigan en el top 9 de {nq} por azar:",
  f"{hypergeom.sf(k_top - 1, nq, len(cnt), 9):.2e}")
P(f"Cuerdas serie_L en los 9 foco: {int(Q[Q.kfg.isin(F)].kfg_serieL.sum())} de {int(Q.kfg_serieL.sum())} del corpus "
  f"({Q[Q.kfg.isin(F)].kfg_serieL.sum() / Q.kfg_serieL.sum():.0%})")

# --- estilo: foco vs resto (no artefacto), por quipu; prueba de permutacion de etiqueta foco entre quipus
X = C[~C.artefacto_n_valor]
rng = np.random.default_rng(SEED)
P("\n=== Estilo foco vs otros quipus con series (no artefacto); unidad = quipu; nulo: permutar etiqueta foco (10000)")
for v in ["vueltas_media", "frac_4a6", "frac_le3", "dirS", "hueco_med", "sd_dentro"]:
    x = X[v].values; lab = X.foco.values
    obs = x[lab].mean() - x[~lab].mean()
    nul = np.array([(lambda l: x[l].mean() - x[~l].mean())(rng.permutation(lab)) for _ in range(10000)])
    P(f"  {v}: foco {x[lab].mean():.2f} vs otros {x[~lab].mean():.2f} (n={(~lab).sum()}), p = {pemp(obs, nul, 'dos'):.4f}")

# --- UR144: sensibilidad a la fuente (las vueltas del racimo superior difieren KFG vs OKR)
oc = pd.read_csv(AQUI / "okr_cuerdas.csv", low_memory=False, dtype={"palabra": str})
o = oc[(oc.inv == "UR144") & oc.serie_L].palabra.map(lambda s: [float(x) for x in s.split("-")])
k = c[c.kfg == "UR144"].w
for nm, ws in [("KFG", list(k)), ("OKR", list(o))]:
    P(f"UR144 {nm}: n={len(ws)} media vueltas {np.mean(np.concatenate(ws)):.2f}, ultimo-primero {np.mean([w[-1] - w[0] for w in ws]):.2f}, "
      f"sd dentro {np.mean([np.std(w) for w in ws]):.2f}, top {Counter(tuple(map(int, w)) for w in ws).most_common(4)}")
f.close()

# --- repeticion de palabras ENTRE quipus foco (k>=2): palabras distintas compartidas por par; nulo a dentro de cada quipu
f = open(AQUI / "04_salida.txt", "a", encoding="utf-8")
W = {q: [list(w) for w in c[c.kfg == q].w] for q in F}
def nulo_a(ws, rng):
    flat = np.concatenate(ws); rng.shuffle(flat); out, i = [], 0
    for w in ws: out.append(tuple(flat[i:i + len(w)])); i += len(w)
    return out
from itertools import combinations
def compartidas(D):
    return sum(len(set(map(tuple, D[a])) & set(map(tuple, D[b]))) for a, b in combinations(F, 2))
obs = compartidas(W)
nul = np.array([compartidas({q: nulo_a(W[q], rng) for q in F}) for _ in range(1000)])
P(f"\nPalabras distintas compartidas entre pares de quipus foco (36 pares): obs {obs}, nulo a {nul.mean():.1f} (sd {nul.std():.1f}), "
  f"p(dos) {pemp(obs, nul, 'dos'):.3f}")
# misma prueba solo con palabras de longitud >=3
W3 = {q: [w for w in W[q] if len(w) >= 3] for q in F}
obs3 = sum(len(set(map(tuple, W3[a])) & set(map(tuple, W3[b]))) for a, b in combinations(F, 2) if W3[a] and W3[b])
nul3 = []
for _ in range(1000):
    Z = {q: nulo_a(W3[q], rng) if W3[q] else [] for q in F}
    nul3.append(sum(len(set(Z[a]) & set(Z[b])) for a, b in combinations(F, 2)))
P(f"  solo k>=3: obs {obs3}, nulo {np.mean(nul3):.1f}, p(dos) {pemp(obs3, np.array(nul3), 'dos'):.3f}")
f.close()
