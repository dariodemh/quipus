"""14_copias · Tarea 2: formato "fila + cuerda-total suelta" en todo el corpus.
Definición. Grupo-fila = grupo de colgantes (nivel 0, sin unión T) con >=2 cuerdas con nudos y suma S>=10.
Cuerda suelta = grupo de 1 colgante (con nudos) cuyo índice de grupo es adyacente (±1) al de una fila.
Acierto = valor de la suelta == S (tol 0) o |valor-S|<=1 (tol 1). "antes"/"después" según el índice de grupo.
Nulo 1 (por quipu): se barajan los valores de todas las cuerdas sueltas del quipu entre sus posiciones (conserva multiconjunto);
  2000 permutaciones, semilla fija; p empírico unilateral; BH sobre los quipus evaluables (>=3 candidatos).
Nulo 2 (global, descriptivo): tasa de acierto de la suelta contra filas a distancia d=1 (adyacente) frente a d=2..5.
Salidas: fila_total_por_quipu.csv, fila_total_hits.csv, fila_total_concentracion.csv, fila_total_salida.txt
`python fila_total.py --demo` autocomprueba con un quipu sintético.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

OUT = Path(__file__).resolve().parent
RAIZ = OUT.parents[1]
SEED = 20261017
NPERM = 2000
MINCAND = 3
TOLS = {"0": (0, 0.0), "1": (1, 0.0), "2pc": (0, 0.02)}  # (absoluta, relativa): acierto si |v-S| <= max(abs, rel*S)


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / (np.arange(n) + 1))[::-1])[::-1]
    return np.minimum(q, 1)


def candidatos(cq, todas=None, dmax=1):
    """devuelve DataFrame de candidatos (suelta, fila, lado, distancia) de un quipu. cq: colgantes nivel 0 sin T."""
    sz = cq.groupby("grupo").size()
    nk = cq[cq.valor > 0].groupby("grupo").size()
    suma = cq.groupby("grupo").valor.sum()
    if todas is not None:
        suma_all = todas.groupby("grupo").valor.sum()
    filas = {g: suma[g] for g in sz.index if nk.get(g, 0) >= 2 and suma[g] >= 10}
    omin = cq.groupby("grupo").orden.min()
    out = []
    for g in sz.index[sz == 1]:
        x = cq[cq.grupo == g].iloc[0]
        if not x.valor > 0:
            continue
        for d in range(1, dmax + 1):
            for gg in (g + d, g - d):
                if gg in filas:
                    # lado por numeración de cuerda (orden), no por índice de grupo (KFG ordena grupos por posición en cm y a veces los invierte)
                    lado = "antes" if x.orden < omin[gg] else "despues"
                    out.append((x.cuerda, g, x.valor, gg, filas[gg], lado, d, suma_all[gg] if todas is not None else np.nan))
    return pd.DataFrame(out, columns=["suelta", "g_suelta", "v", "g_fila", "S", "lado", "d", "S_all"])


def prueba(cq, rng, tol):
    """p empírico de nº de aciertos a distancia 1; devuelve (n_cand, hits, esperado, p, lista de aciertos)."""
    cand = candidatos(cq)
    n = len(cand)
    if n == 0:
        prueba.ultimo_nulo = np.zeros(NPERM)
        return 0, 0, np.nan, 1.0, cand.iloc[0:0]
    hit = (cand.v - cand.S).abs() <= np.maximum(tol[0], tol[1] * cand.S)
    obs = int(hit.sum())
    sing = cq[(cq.groupby("grupo").valor.transform("size") == 1) & (cq.valor > 0)]
    pool = sing.valor.to_numpy(float)
    slot = {c: i for i, c in enumerate(sing.cuerda)}
    idx = np.array([slot[c] for c in cand.suelta]); S = cand.S.to_numpy(float)
    nul = np.empty(NPERM)
    for b in range(NPERM):
        v = rng.permutation(pool)
        nul[b] = (np.abs(v[idx] - S) <= np.maximum(tol[0], tol[1] * S)).sum()
    prueba.ultimo_nulo = nul
    return n, obs, nul.mean(), (1 + (nul >= obs).sum()) / (NPERM + 1), cand[hit]


def _demo():
    rng = np.random.default_rng(1)
    filas = []
    for r in range(8):  # 8 filas, con la suelta delante = suma
        vals = rng.integers(10, 300, 5)
        filas += [(int(vals.sum()),)] + [(int(v),) for v in vals]
    d2, k, gcount = [], 0, 0
    for r in range(8):
        d2.append({"kfg": "X", "cuerda": f"s{r}", "grupo": gcount, "valor": filas[r * 6][0], "nivel": 0, "union": "U"}); gcount += 1
        for j in range(5):
            d2.append({"kfg": "X", "cuerda": f"s{r}_{j}", "grupo": gcount, "valor": filas[r * 6 + 1 + j][0], "nivel": 0, "union": "V"})
        gcount += 1
    d2 = pd.DataFrame(d2)
    n, obs, esp, p, h = prueba(d2, np.random.default_rng(2), TOLS["0"])
    assert obs == 8 and p < 0.01, (n, obs, esp, p)
    # control negativo: valores independientes
    d3 = d2.copy(); d3.loc[d3.cuerda.str.startswith("s") & ~d3.cuerda.str.contains("_"), "valor"] = rng.integers(500, 900, 8)
    n, obs, esp, p, h = prueba(d3, np.random.default_rng(3), TOLS["0"])
    assert obs == 0
    print("demo ok")


if "--demo" in sys.argv:
    _demo()
    sys.exit()

C = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv")
Q = pd.read_csv(RAIZ / "analisis/datos/quipus.csv").set_index("kfg")
rows = []
NULOS = {t: {} for t in TOLS}
hits = []
dist_rows = []
for i, (k, g) in enumerate(C.groupby("kfg")):
    cq = g[(g.nivel == 0) & (g.union != "T")]
    if cq.grupo.nunique() < 3:
        continue
    rng = np.random.default_rng([SEED, i])
    o = {"kfg": k}
    for tol in TOLS:
        n, obs, esp, p, h = prueba(cq, rng, TOLS[tol])
        NULOS[tol][k] = prueba.ultimo_nulo
        o[f"n_cand"] = n
        o[f"hits_tol{tol}"], o[f"esp_tol{tol}"], o[f"p_tol{tol}"] = obs, esp, p
        if len(h):
            hh = h.copy(); hh["kfg"] = k; hh["tol"] = tol; hh["diff"] = hh.v - hh.S
            hits.append(hh)
    rows.append(o)
    # nulo 2: distancia
    cd = candidatos(cq, dmax=5)
    if len(cd):
        for (d, lado), x in cd.groupby(["d", "lado"]):
            dist_rows.append({"kfg": k, "d": d, "lado": lado, "n": len(x), "h0": int((x.v == x.S).sum()), "h1": int(((x.v - x.S).abs() <= 1).sum())})
R = pd.DataFrame(rows)
H = pd.concat(hits) if hits else pd.DataFrame()
D = pd.DataFrame(dist_rows)
ev = R[R.n_cand >= MINCAND].copy()
for tol in TOLS:
    ev[f"q_tol{tol}"] = bh(ev[f"p_tol{tol}"])
R = R.merge(ev[["kfg"] + [f"q_tol{t}" for t in TOLS]], on="kfg", how="left")
R["evaluable"] = R.n_cand >= MINCAND
for c_ in ("procedencia", "museo", "region"):
    R[c_] = R.kfg.map(Q[c_])
R["serie"] = R.kfg.str.extract(r"^([A-Z]+)")[0]
R["registrador"] = np.where((R.serie == "AS") | ((R.serie == "UR") & (R.kfg.str[2:].str.extract(r"(\d+)")[0].astype(int) >= 1000)), "AS", R.serie)
R.to_csv(OUT / "fila_total_por_quipu.csv", index=False)
H.to_csv(OUT / "fila_total_hits.csv", index=False)
D.to_csv(OUT / "fila_total_distancias.csv", index=False)

pr = print
pr(f"quipus con >=3 grupos: {len(R)}; con candidatos (suelta adyacente a fila): {(R.n_cand>0).sum()}; evaluables (>= {MINCAND} candidatos): {R.evaluable.sum()}")
pr(f"candidatos totales {int(R.n_cand.sum())}; aciertos tol0 {int(R.hits_tol0.sum())}, tol1 {int(R.hits_tol1.sum())}; esperado por quipu (suma) tol0 {R.esp_tol0.sum():.1f}, tol1 {R.esp_tol1.sum():.1f}")
# p global: suma de aciertos vs suma de los nulos -> aproximación por simulación conjunta ya implícita; test de exceso por quipu con p<.05
for tol in TOLS:
    e = R[R.evaluable]
    nsig_p = int((e[f"p_tol{tol}"] < .05).sum()); nsig_q = int((e[f"q_tol{tol}"] < .05).sum())
    pr(f"tol {tol}: evaluables {len(e)}; p<0,05: {nsig_p} (esperado por azar ~{0.05*len(e):.1f}); q<0,05 (BH): {nsig_q}")
    pr("   quipus con q<0,05:", ", ".join(e[e[f"q_tol{tol}"] < .05].kfg))

# exceso global: suma de aciertos vs suma de nulos independientes por quipu
for tol in TOLS:
    tot = int(R[f"hits_tol{tol}"].sum())
    sn = np.sum([NULOS[tol][k] for k in R.kfg], axis=0)
    flagged = set(R[(R.q_tol0 < .05) | (R.q_tol1 < .05)].kfg)
    sn2 = np.sum([NULOS[tol][k] for k in R.kfg if k not in flagged], axis=0)
    tot2 = int(R[~R.kfg.isin(flagged)][f"hits_tol{tol}"].sum())
    pr(f"tol {tol}: aciertos {tot} vs nulo {sn.mean():.1f} (max {sn.max():.0f}), p={(1+(sn>=tot).sum())/(NPERM+1):.4f}; "
       f"sin los {len(flagged)} quipus marcados: {tot2} vs {sn2.mean():.1f}, p={(1+(sn2>=tot2).sum())/(NPERM+1):.4f}")
    r2 = R[~R.kfg.isin(flagged) & (R[f"hits_tol{tol}"] > 0)][["kfg", "n_cand", f"hits_tol{tol}", f"esp_tol{tol}", f"p_tol{tol}"]]
    pr(f"   quipus no marcados con aciertos (tol {tol}): {len(r2)}"); pr(r2.round(3).to_string(index=False))

# distancia
pr("\nAciertos por distancia de la fila (d=1 adyacente; d=2..5), sumado en el corpus (tol0 | tol1):")
tt = D.groupby("d")[["n", "h0", "h1"]].sum()
tt["tasa0"] = tt.h0 / tt.n; tt["tasa1"] = tt.h1 / tt.n
pr(tt.round(4).to_string())
# idem sin los quipus significativos (¿queda exceso?)
sig = set(R[(R.q_tol1 < .05) | (R.q_tol0 < .05)].kfg)
tt2 = D[~D.kfg.isin(sig)].groupby("d")[["n", "h0", "h1"]].sum()
tt2["tasa0"] = tt2.h0 / tt2.n; tt2["tasa1"] = tt2.h1 / tt2.n
pr("\nSin los quipus con q<0,05:")
pr(tt2.round(4).to_string())
pr("\nlado de los aciertos por quipu significativo (tol1):")
if len(H):
    hs = H[(H.tol == "1") & H.kfg.isin(sig)]
    pr(hs.groupby(["kfg", "lado"]).size().unstack(fill_value=0).to_string())
    pr("aciertos exactos por quipu significativo (diff):")
    pr(hs.groupby("kfg")["diff"].apply(lambda s: dict(s.value_counts())).to_string())

# concentración
pr("\n=== Concentración (quipu = unidad; marca = q<0,05 en tol0 o tol1; universo = quipus evaluables)")
E = R[R.evaluable].copy()
E["marca"] = (E.q_tol0 < .05) | (E.q_tol1 < .05)
tot_m, tot_n = int(E.marca.sum()), len(E)
pr(f"marcados {tot_m} de {tot_n} evaluables ({tot_m/tot_n:.3f})")
res = []
for col in ("registrador", "serie", "museo", "procedencia", "region"):
    for v, g in E.groupby(col):
        if len(g) < 2:
            continue
        a, n = int(g.marca.sum()), len(g)
        p = stats.hypergeom.sf(a - 1, tot_n, tot_m, n) if a > 0 else 1.0
        res.append({"categoria": col, "valor": v, "evaluables": n, "marcados": a, "esperado": n * tot_m / tot_n, "p_hiper": p})
res = pd.DataFrame(res)
res["q_BH"] = bh(res.p_hiper)
res.sort_values("p_hiper").to_csv(OUT / "fila_total_concentracion.csv", index=False)
pr(res.sort_values("p_hiper").head(12).round(4).to_string(index=False))
pr(f"(BH sobre {len(res)} categorías)")
# marcados: tabla
pr("\nQuipus marcados:")
mm = E[E.marca][["kfg", "registrador", "museo", "procedencia", "n_cand", "hits_tol0", "esp_tol0", "q_tol0", "hits_tol1", "esp_tol1", "q_tol1"]]
pr(mm.round(4).to_string(index=False))
