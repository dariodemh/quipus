"""Tests principales de n_narrative_threads (Quilter & Urton 2002).
Todos los nulos son permutaciones; semilla fija. Unidad = quipu.
"""
import json
import numpy as np
import pandas as pd
import prep

SEED = 20261018
rng_global = np.random.default_rng(SEED)
d, q = prep.load()
d0 = d[d.nivel == 0].copy()
d0["grupo"] = pd.to_numeric(d0["grupo"], errors="coerce")
d0["valor_n"] = pd.to_numeric(d0["valor_n"], errors="coerce")
q = q.set_index("kfg")

results = []


def add(test, hipotesis, obs, null=None, p=None, n=None, extra=""):
    results.append(dict(test=test, hipotesis=hipotesis, observado=obs,
                        nulo=float(np.mean(null)) if null is not None else np.nan,
                        p=float(p) if p is not None else np.nan, n=n, extra=extra))
    print(f"{test:38s} obs={obs!s:>12.12} null={'' if null is None else round(float(np.mean(null)),3)} p={p if p is None else round(p,5)} n={n}")


# ---------------------------------------------------------------- A. pureza
print("\n=== A. Pureza de rasgos dentro de cada quipu ===")
pur = []
for trait in ["torsion2", "union2", "kdir", "cromatico"]:
    vals = d0[["kfg", trait]].dropna()
    vals = vals[vals[trait].astype(str).isin(["S", "Z", "R", "V", "0", "1", "0.0", "1.0"])]
    for k, x in vals.groupby("kfg"):
        if len(x) < 3:
            continue
        vc = x[trait].value_counts(normalize=True)
        pur.append(dict(trait=trait, kfg=k, purity=vc.iloc[0], both=len(vc) > 1, n=len(x)))
pur = pd.DataFrame(pur)
desc = pur.groupby("trait").agg(median_purity=("purity", "median"), quipus=("kfg", "size"),
                                con_dos_categorias=("both", "sum"))
print(desc.round(3).to_string())
desc.to_csv("pureza_rasgos.csv")

# ---------------------------------------------------------------- B. CMH
print("\n=== B. Co-variación de rasgos binarios (CMH, permutación intra-quipu) ===")


def cmh_table(df, a, b, min_n=6):
    sub = df.dropna(subset=[a, b])
    rows = []
    for k, x in sub.groupby("kfg"):
        n = len(x)
        if n < min_n or x[a].nunique() < 2 or x[b].nunique() < 2:
            continue
        o11 = int(((x[a] == 1) & (x[b] == 1)).sum())
        rows.append((k, n, o11, int((x[a] == 1).sum()), int((x[b] == 1).sum())))
    t = pd.DataFrame(rows, columns=["kfg", "n", "o11", "r1", "c1"])
    t["e11"] = t.r1 * t.c1 / t.n
    t["v"] = t.r1 * (t.n - t.r1) * t.c1 * (t.n - t.c1) / (t.n ** 2 * (t.n - 1))
    return t


def cmh_perm(t, n_perm=5000, seed=SEED):
    rng = np.random.default_rng(seed)
    n = t.n.values.astype(int); r1 = t.r1.values.astype(int); c1 = t.c1.values.astype(int)
    obs = ((t.o11 - t.e11).sum()) ** 2 / t["v"].sum()
    null = np.empty(n_perm)
    for i in range(n_perm):
        o = rng.hypergeometric(c1, n - c1, r1)
        e = r1 * c1 / n
        v = r1 * (n - r1) * c1 * (n - c1) / (n ** 2 * (n - 1))
        null[i] = ((o - e).sum()) ** 2 / v.sum()
    p = (1 + (null >= obs).sum()) / (n_perm + 1)
    return obs, null, p


d0["torZ"] = (d0.torsion2 == "Z").astype(float).where(d0.torsion2.notna())
d0["uniV"] = (d0.union2 == "V").astype(float).where(d0.union2.notna())
d0["kdS"] = (d0.kdir == "S").astype(float).where(d0.kdir.isin(["S", "Z"]))
d0["crom"] = d0.cromatico
for a, b, lab in [("torZ", "uniV", "torsión Z × unión V"), ("torZ", "crom", "torsión Z × color marcado"),
                  ("uniV", "crom", "unión V × color marcado"), ("kdS", "torZ", "nudo S × torsión Z"),
                  ("kdS", "uniV", "nudo S × unión V"), ("kdS", "crom", "nudo S × color marcado")]:
    t = cmh_table(d0, a, b)
    if len(t) == 0:
        continue
    obs, null, p = cmh_perm(t)
    signs = np.sign(t.o11 - t.e11)
    add(f"CMH {lab}", "independencia de rasgos binarios", obs, null, p,
        n=len(t), extra=f"quipus +{int((signs>0).sum())}/-{int((signs<0).sum())}")

# co-variación a nivel de quipu (proporciones)
print("\n--- B2. Co-variación entre quipus (proporciones) ---")
prof = d0.groupby("kfg").agg(n=("cuerda", "size"),
                             pV=("uniV", "mean"), pTorZ=("torZ", "mean"),
                             pCrom=("crom", "mean"), pKdS=("kdS", "mean"))
prof = prof[prof.n >= 10]
for a, b, lab in [("pV", "pTorZ", "unión V × torsión Z"), ("pV", "pCrom", "unión V × color"),
                  ("pV", "pKdS", "unión V × nudo S"), ("pCrom", "pTorZ", "color × torsión"),
                  ("pCrom", "pKdS", "color × nudo S")]:
    x = prof[[a, b]].dropna()
    if x[a].nunique() < 3 or x[b].nunique() < 3:
        continue
    obs = x[a].corr(x[b], method="spearman")
    null = np.empty(2000)
    ya = x[a].values
    for i in range(2000):
        null[i] = pd.Series(ya).corr(pd.Series(rng_global.permutation(x[b].values)), method="spearman")
    p = (1 + (np.abs(null) >= abs(obs)).sum()) / 2001
    add(f"Spearman quipu {lab}", "co-variación ecológica entre quipus", obs, null, p, n=len(x))

# ---------------------------------------------------------------- C. bandas de color
print("\n=== C. Bandas de color dentro del quipu ===")
seq = d0.sort_values(["kfg", "orden"])
same_null = np.zeros(1000); pairs_null = np.zeros(1000)
per_q = []
for k, x in seq.groupby("kfg"):
    c = x.color_f.fillna("").values
    c = c[c != ""]
    if len(c) < 4:
        continue
    s = np.sum(c[1:] == c[:-1]); n = len(c) - 1
    per_q.append((k, s, n, c))
for i in range(1000):
    ss = 0; nn = 0
    for k, s, n, c in per_q:
        z = rng_global.permutation(c)
        ss += np.sum(z[1:] == z[:-1])
        nn += n
    same_null[i] = ss; pairs_null[i] = nn
obs_rate = sum(s for _, s, _, _ in per_q) / sum(n for _, _, n, _ in per_q)
null_rate = same_null / pairs_null
p = (1 + (null_rate >= obs_rate).sum()) / 1001
add("Bandas de color (adyacencia)", "Salomon: color en bloques", obs_rate, null_rate, p, n=len(per_q))

# ---------------------------------------------------------------- D. color de la primera cuerda
print("\n=== D. ¿La primera cuerda del grupo se distingue por color? ===")
groups = []
for (k, g), x in d0.groupby(["kfg", "grupo"]):
    x = x.sort_values("orden")
    if len(x) < 3:
        continue
    c = x.color_f.fillna("").values
    if len(set(c)) < 2:
        continue
    groups.append((k, g, c))
def mode_excl(c, j):
    vals, counts = np.unique(np.delete(c, j), return_counts=True)
    return vals[np.argmax(counts)]
obs = sum(1 for _, _, c in groups if c[0] != mode_excl(c, 0)) / len(groups)
null = np.empty(2000)
for i in range(2000):
    cnt = 0
    for _, _, c in groups:
        j = rng_global.integers(len(c))
        if c[j] != mode_excl(c, j):
            cnt += 1
    null[i] = cnt / len(groups)
p = (1 + (null >= obs).sum()) / 2001
add("Color de primera cuerda", "Mackey: color marca el inicio", obs, null, p, n=len(groups))

# ---------------------------------------------------------------- E. valores-etiqueta
print("\n=== E. ¿Los valores de la primera cuerda son etiquetas repetidas? ===")
glist = []
for (k, g), x in d0.groupby(["kfg", "grupo"]):
    x = x.sort_values("orden")
    if len(x) < 2:
        continue
    glist.append((k, x.valor_n.values))


# construir matriz por quipu: grupos x posiciones (solo valores válidos)
byq = {}
for (k, g), x in d0.groupby(["kfg", "grupo"]):
    x = x.sort_values("orden")
    v = x.valor_n.dropna().values
    if len(v) >= 2:
        byq.setdefault(k, []).append(v)
byq = {k: v for k, v in byq.items() if len(v) >= 4}
obs_list = [np.mean([pd.Series(v).value_counts().iloc[0] / len(v) for v in vs]) for vs in byq.values()]
obs = float(np.mean(obs_list))
null = np.empty(1000)
for i in range(1000):
    vals = []
    for k, vs in byq.items():
        rr = []
        for v in vs:
            rr.append(v[rng_global.integers(len(v))])
        vals.append(pd.Series(rr).value_counts().iloc[0] / len(rr))
    null[i] = np.mean(vals)
p = (1 + (null >= obs).sum()) / 1001
add("Repetición de valores (1.ª cuerda)", "Ascher: números como etiquetas", obs, null, p, n=len(byq))

# ---------------------------------------------------------------- F. cuerdas superiores
print("\n=== F. Cuerda superior = suma del grupo anterior ===")
matches = []; total = 0
for k, x in d0.groupby("kfg"):
    gs = {g: y for g, y in x.groupby("grupo")}
    for g, y in gs.items():
        t = y[y.union == "T"]
        if len(t) != 1:
            continue
        tv = float(t.valor_n.iloc[0])
        prev = gs.get(g - 1)
        if prev is None:
            continue
        total += 1
        matches.append((k, g, tv, float(prev.valor_n.sum()), np.isclose(tv, prev.valor_n.sum())))
md = pd.DataFrame(matches, columns=["kfg", "g", "T", "prev", "match"])
obs = md.match.mean()
vals_por_k = {k: x.valor_n.values for k, x in d0.groupby("kfg")}
null = np.empty(3000)
for i in range(3000):
    cnt = 0
    for k, g, tv, pv, m in matches:
        cand = rng_global.choice(vals_por_k[k])
        cnt += bool(np.isclose(cand, pv))
    null[i] = cnt / len(matches)
p = (1 + (null >= obs).sum()) / 3001
add("Cuerda superior = suma previa", "Conklin/Ascher: totales", obs, null, p, n=total,
    extra=f"{int(md.match.sum())}/{total} exactos")

# ---------------------------------------------------------------- G. quipus narrativos
print("\n=== G. Quipus 'narrativo-contables' (Urton cap. 8) ===")
st = d.groupby("kfg").agg(ncuerdas=("cuerda", "size"), share3=("ncl", lambda x: np.mean(x == 3)),
                          share4=("ncl", lambda x: np.mean(x == 4)), maxL=("maxL", "max"),
                          anyL10=("maxL", lambda x: (x >= 10).any()))
cand = st[(st.share3 >= 0.5) & (st.anyL10)]
print(f"khipus con >=50% de cuerdas de 3 racimos y algún nudo largo >=10: {len(cand)}")
print(cand.sort_values("share3", ascending=False).head(10).round(3).to_string())
# asociación share3 vs L>=10 a nivel de quipu
x = st[st.ncuerdas >= 10]
obs = x.share3.corr(x.anyL10.astype(int), method="spearman")
null = np.empty(2000)
for i in range(2000):
    null[i] = pd.Series(x.share3.values).corr(pd.Series(rng_global.permutation(x.anyL10.values)), method="spearman")
p = (1 + (np.abs(null) >= abs(obs)).sum()) / 2001
add("3 racimos ~ nudo largo >=10", "Urton: unidad significante tripartita", obs, null, p, n=len(x),
    extra=f"{int(cand.shape[0])} candidatos")

# ---------------------------------------------------------------- H. variación por sitio
print("\n=== H. Variación de rasgos por procedencia ===")
prof2 = d0.groupby("kfg").agg(n=("cuerda", "size"), pV=("uniV", "mean"), pTorZ=("torZ", "mean"),
                              pCrom=("crom", "mean"), pKdS=("kdS", "mean"))
prof2 = prof2.join(q[["procedencia"]])
for trait in ["pV", "pTorZ", "pCrom", "pKdS"]:
    x = prof2.dropna(subset=[trait, "procedencia"])
    x = x[x.procedencia.isin(x.procedencia.value_counts()[lambda s: s >= 5].index)]
    if x.procedencia.nunique() < 3:
        continue
    grand = x[trait].mean()
    obs = x.groupby("procedencia")[trait].apply(lambda s: len(s) * (s.mean() - grand) ** 2).sum() / len(x)
    null = np.empty(1000)
    for i in range(1000):
        lab = rng_global.permutation(x.procedencia.values)
        s = pd.Series(x[trait].values).groupby(lab).agg(["mean", "size"])
        null[i] = ((s["size"] * (s["mean"] - grand) ** 2).sum()) / len(x)
    p = (1 + (null >= obs).sum()) / 1001
    add(f"eta2 sitio {trait}", "Quilter: diversidad regional", obs, null, p, n=len(x),
        extra=f"{x.procedencia.nunique()} sitios")

# ---------------------------------------------------------------- I. semántica del color por sitio
print("\n=== I. ¿El significado del color cambia por sitio? ===")
c = d0.dropna(subset=["color_f", "valor_n"]).copy()
c["procedencia"] = c.kfg.map(q.procedencia)
c = c[(c.valor_n > 0) & c.procedencia.notna()]
top_sites = c.procedencia.value_counts()[lambda s: s >= 100].index
c = c[c.procedencia.isin(top_sites)]
top_colors = c.color_f.value_counts()[lambda s: s >= 100].index
c = c[c.color_f.isin(top_colors)]
c["rank"] = c.groupby("procedencia").valor_n.rank(pct=True)
# interacción sitio x color, centrada por sitio
cell = c.groupby(["procedencia", "color_f"]).agg(m=("rank", "mean"), n=("rank", "size"))
cell = cell[cell.n >= 5].reset_index()
cell["dev"] = cell.m - cell.groupby("procedencia").m.transform("mean")
obs = (cell.n * cell.dev ** 2).sum() / cell.n.sum()
null = np.empty(500)
for i in range(500):
    cc = c.copy()
    cc["procedencia"] = rng_global.permutation(cc.procedencia.values)
    cc["rank"] = cc.groupby("procedencia").valor_n.rank(pct=True)
    ce = cc.groupby(["procedencia", "color_f"]).agg(m=("rank", "mean"), n=("rank", "size"))
    ce = ce[ce.n >= 5].reset_index()
    ce["dev"] = ce.m - ce.groupby("procedencia").m.transform("mean")
    null[i] = (ce.n * ce.dev ** 2).sum() / ce.n.sum()
p = (1 + (null >= obs).sum()) / 2001
add("Interacción color×sitio", "Platt: lecturas variables del color", obs, null, p, n=len(c),
    extra=f"{c.procedencia.nunique()} sitios, {c.color_f.nunique()} colores")

pd.DataFrame(results).to_csv("resultados_principales.csv", index=False)
print("\nGuardado resultados_principales.csv")
