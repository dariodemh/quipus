# -*- coding: utf-8 -*-
"""Robustez de los hallazgos principales: pares, color, límites, Santa."""
import json
import numpy as np
import pandas as pd
from scipy import stats
from comun import cargar, bh_holm

RNG = np.random.default_rng(777)
RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_salas2025"
c, q = cargar()
val = c[c.valida].sort_values(["kfg", "orden"]).reset_index(drop=True)
lvl0 = val[val.nivel == 0].sort_values(["kfg", "orden"]).reset_index(drop=True)
v0 = lvl0.v.values
gid0 = pd.factorize(lvl0.kfg)[0]
n0 = len(lvl0)
same0 = gid0[:-1] == gid0[1:]

# ------------------------------------------------ 1. pares: longitud de rachas
rachas = []
for kfg, d in lvl0.groupby("kfg"):
    v = d.v.values
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]:
            j += 1
        if j > i and v[i] > 1:
            rachas.append((v[i], j - i + 1))
        i = j + 1
rdf = pd.DataFrame(rachas, columns=["valor", "largo"])
dist = rdf.largo.value_counts().sort_index()
# nulo: misma cuenta de rachas por permutación
def cuenta_rachas(v):
    out = {}
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[i]:
            j += 1
        if j > i and v[i] > 1:
            out[j - i + 1] = out.get(j - i + 1, 0) + 1
        i = j + 1
    return out
null_r = []
B = 2000
# versión vectorizada sencilla: reutilizar bloques
bloques = [d.v.values for _, d in lvl0.groupby("kfg")]
null_counts = {2: [], 3: [], 4: []}
for _ in range(B):
    cc = {2: 0, 3: 0, 4: 0}
    for v in bloques:
        vv = RNG.permutation(v)
        d = cuenta_rachas(vv)
        for k in cc:
            cc[k] += d.get(k, 0)
    for k in cc:
        null_counts[k].append(cc[k])
res_rachas = {"dist_obs": {int(k): int(v) for k, v in dist.items()},
              "pares_obs": int((rdf.largo == 2).sum()),
              "trios_obs": int((rdf.largo == 3).sum()),
              "nulos_pares_media": float(np.mean(null_counts[2])),
              "nulos_trios_media": float(np.mean(null_counts[3])),
              "ratio_pares": float((rdf.largo == 2).sum() / np.mean(null_counts[2])),
              "ratio_trios": float((rdf.largo == 3).sum() / np.mean(null_counts[3])),
              "p_pares": float((1 + np.sum(np.array(null_counts[2]) >= (rdf.largo == 2).sum())) / (B + 1)),
              "p_trios": float((1 + np.sum(np.array(null_counts[3]) >= (rdf.largo == 3).sum())) / (B + 1)),
              "valores_mas_repetidos": rdf[rdf.largo == 2].valor.value_counts().head(8).to_dict()}
print("rachas:", res_rachas)

# ------------------------------------------------ 2. color: concentración por quipu
def aportes(color, flagcol, Btarget=20000):
    d = val.copy()
    d["flag"] = d[flagcol].values
    filas = []
    for kfg, g in d.groupby("kfg"):
        n = len(g)
        if n == 0:
            continue
        nc = int((g.color_base == color).sum())
        if nc == 0:
            continue
        obs = g.loc[g.color_base == color, "flag"].sum()
        esp = nc * g.flag.mean()
        filas.append((kfg, n, nc, int(obs), float(esp), float(obs - esp)))
    f = pd.DataFrame(filas, columns=["kfg", "n", "nc", "obs", "esp", "aporte"])
    f = f.sort_values("aporte", ascending=False)
    total = f.aporte.sum()
    top = f.head(8).to_dict("records")
    return {"n_quipus_color": int(len(f)), "total_aporte": float(total),
            "top": top, "top3_share": float(f.head(3).aporte.sum() / total) if total else None}

res_col = {
    "KB_u0": aportes("KB", "u0"),
    "DB_c100": aportes("DB", "c100"),
}
print("aportes KB u0:", json.dumps(res_col["KB_u0"], ensure_ascii=False)[:500])

# test dirigido con 20k permutaciones para KB/u0 y DB/c100
codes, uniques = pd.factorize(val.color_base.astype(str).values)
K = len(uniques)

def perm_dir(color, flagcol, B=20000):
    flag = val[flagcol].values.astype(float)
    k = list(uniques).index(color)
    obs = flag[codes == k].sum()
    gidv = pd.factorize(val.kfg)[0]
    nv = len(val)
    cnt = 0
    for _ in range(B):
        fp = flag[np.lexsort((RNG.random(nv), gidv))]
        if fp[codes == k].sum() >= obs:
            cnt += 1
    return {"obs": float(obs), "p": float((1 + cnt) / (B + 1))}
res_dir = {"KB_u0": perm_dir("KB", "u0"), "DB_c100": perm_dir("DB", "c100")}
print("dirigidos:", res_dir)

# ------------------------------------------------ 3. límites de grupo, robustez
cb0 = lvl0.color_base.values
gr0 = lvl0.grupo.values
bound0 = same0 & (gr0[:-1] != gr0[1:])
within0 = same0 & ~bound0
chg0 = cb0[:-1] != cb0[1:]
# solo quipus con ambos tipos de pares
qcon = []
for kfg, d in lvl0.groupby("kfg"):
    idx = d.index.values
    if len(idx) < 3:
        continue
    b = chg0[idx[:-1]][bound0[idx[:-1]]]
    w = chg0[idx[:-1]][within0[idx[:-1]]]
    if len(b) >= 2 and len(w) >= 2:
        qcon.append((kfg, b.mean() - w.mean(), len(b), len(w)))
qdf = pd.DataFrame(qcon, columns=["kfg", "dif", "nb", "nw"])
obs_dif = float(qdf.dif.mean())
# nulo vectorizado: permutar color dentro de cada quipu
gpair = gid0[:-1]
nb = np.bincount(gpair, weights=bound0.astype(float)).astype(int)
nw = np.bincount(gpair, weights=within0.astype(float)).astype(int)
keep = (nb >= 2) & (nw >= 2)
B_b = 5000
cnt = 0
for _ in range(B_b):
    cbp = cb0[np.lexsort((RNG.random(n0), gid0))]
    ch = (cbp[:-1] != cbp[1:]).astype(float)
    sb = np.bincount(gpair, weights=ch * bound0)
    sw = np.bincount(gpair, weights=ch * within0)
    difs = sb[keep] / nb[keep] - sw[keep] / nw[keep]
    if difs.mean() >= obs_dif:
        cnt += 1
res_bound2 = {"n_quipus": len(qdf), "dif_media_por_quipu": obs_dif,
              "p_exceso": float((1 + cnt) / (B_b + 1)),
              "quipus_dif_positiva": float((qdf.dif > 0).mean())}
print("límites robusto:", res_bound2)

# ------------------------------------------------ 4. Santa: composición
qu = val.groupby("kfg").agg(n=("v", "size"), media=("v", "mean"),
                            par=("par", "mean"), u0=("u0", "mean"),
                            c100=("c100", "mean")).reset_index()
qu = qu.merge(q[["kfg", "procedencia", "region", "museo"]], on="kfg", how="left")
qu["macro"] = qu.procedencia.map(__import__("comun").macro_region)
nor = qu[qu.macro == "costa_norcentral"].sort_values("n", ascending=False)
print("norcentral:")
print(nor[["kfg", "procedencia", "region", "n", "media", "par", "u0", "c100"]].to_string(index=False))
# Santa solo
santa = qu[qu.procedencia.astype(str).str.strip().str.lower() == "santa"]
res_santa = {"n_santa": len(santa), "n_mediana": float(santa.n.median()),
             "n_resto_mediana": float(qu[~qu.kfg.isin(santa.kfg)].n.median()),
             "n_max": int(santa.n.max()), "quipus": santa[["kfg", "n"]].to_dict("records")}
# Mann-Whitney y permutación de medianas
a = np.log1p(santa.n.values); b = np.log1p(qu[~qu.kfg.isin(santa.kfg)].n.values)
res_santa["mannwhitney_p"] = float(stats.mannwhitneyu(a, b, alternative="greater").pvalue)
print("Santa:", res_santa)

# ------------------------------------------------ 5. prelación / ordinal: tamaño de efecto
# distribución de Spearman por quipu para orden-valor
sp = []
for kfg, d in lvl0.groupby("kfg"):
    if len(d) >= 8 and d.v.nunique() > 1:
        rho = stats.spearmanr(d.orden.values, d.v.values).statistic
        if np.isfinite(rho):
            sp.append(rho)
sp = np.array(sp)
res_ef = {"spearman_orden_valor": {"media": float(sp.mean()), "mediana": float(np.median(sp)),
                                   "p25": float(np.percentile(sp, 25)), "p75": float(np.percentile(sp, 75)),
                                   "frac_abs_mayor_0.3": float((np.abs(sp) > 0.3).mean()),
                                   "n": int(len(sp))}}
print("efectos:", res_ef)

with open(OUT + r"\robustez.json", "w", encoding="utf-8") as f:
    json.dump({"rachas": res_rachas, "aportes_color": res_col, "dirigidos": res_dir,
               "limites": res_bound2, "santa": res_santa, "efectos": res_ef},
              f, ensure_ascii=False, indent=1)
print("OK")
