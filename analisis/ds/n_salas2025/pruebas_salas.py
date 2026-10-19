# -*- coding: utf-8 -*-
"""
Pruebas cuantitativas de las predicciones de Salas García (2025),
La interpretación lingüística de los quipus.

Unidad de análisis: el quipu. Las pruebas a nivel de cuerda usan
permutaciones DENTRO de cada quipu. Semilla fija.
Salidas: resultados.csv (todas las pruebas con p BH/Holm), resumen.json
"""
import json
import numpy as np
import pandas as pd
from scipy import stats
from comun import cargar, bh_holm

RNG = np.random.default_rng(20251018)
B = 4000          # permutaciones para pruebas principales
B_COLOR = 2000    # permutaciones para asociación de color
RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_salas2025"

c, q = cargar()
val = c[c.valida].sort_values(["kfg", "orden"]).reset_index(drop=True)
print("cuerdas válidas:", len(val), "quipus:", val.kfg.nunique())
gid = pd.factorize(val.kfg)[0]
nval = len(val)
grupos_idx = [np.where(gid == k)[0] for k in range(gid.max() + 1)]

# ---------------------------------------------------------------- descriptivos
desc = {}
units = val.u.astype(int)
desc["n_validas"] = int(len(val))
desc["p_par_empirica"] = float(val.par.mean())
desc["p_u0"] = float(val.u0.mean())
desc["p_c100"] = float(val.c100.mean())
desc["unidades"] = units.value_counts().sort_index().to_dict()
chi_u = stats.chisquare(units.value_counts().sort_index().values)
desc["chi2_unidades_uniforme"] = {"chi2": float(chi_u.statistic),
                                  "p": float(chi_u.pvalue), "gl": 9}
tens = val.t.astype(int)
chi_t = stats.chisquare(tens.value_counts().sort_index().values)
desc["chi2_decenas_uniforme"] = {"chi2": float(chi_t.statistic),
                                 "p": float(chi_t.pvalue), "gl": 9}
# ¿los ceros de decenas y unidades son independientes? (valores "redondos")
obs100 = int(val.c100.sum())
B_ind = 2000
cnt100 = np.empty(B_ind)
u = val.u.values.astype(int)
t = val.t.values.astype(int)
v = val.vi.values
for b in range(B_ind):
    uu = u[np.lexsort((RNG.random(nval), gid))]
    tt = t[np.lexsort((RNG.random(nval), gid))]
    cnt100[b] = int(((uu == 0) & (tt == 0) & (v >= 100)).sum())
p_ind = (1 + int((cnt100 >= obs100).sum())) / (B_ind + 1)
desc["mult100"] = {"obs": obs100, "esperado_independiente": float(cnt100.mean()),
                   "ratio": float(obs100 / max(cnt100.mean(), 1e-9)),
                   "p_exceso": float(p_ind)}
print("descriptivos:", json.dumps(desc, ensure_ascii=False)[:500])

# ------------------------------------------------ asociación con color (cuerda)
color = val.color_base.astype(str).values
codes, uniques = pd.factorize(color)
K = len(uniques)
mask_counts = np.bincount(codes, minlength=K)
colores = [uniques[k] for k in range(K) if mask_counts[k] >= 200]
print("colores probados:", colores)

flags = {"par": val.par.values.astype(float),
         "u0": val.u0.values.astype(float),
         "c100": val.c100.values.astype(float)}

def perm_color(flag, B=B_COLOR):
    obs = np.bincount(codes, weights=flag, minlength=K)
    perm = np.empty((B, K))
    for b in range(B):
        order = np.lexsort((RNG.random(nval), gid))
        fp = flag[order]
        perm[b] = np.bincount(codes, weights=fp, minlength=K)
    return obs, perm

res_color = {}
for nombre, flag in flags.items():
    obs, perm = perm_color(flag)
    for color in colores:
        k = list(uniques).index(color)
        n = mask_counts[k]
        o = obs[k]
        p_exc = (1 + int((perm[:, k] >= o).sum())) / (B_COLOR + 1)
        media = float(perm[:, k].mean())
        sd = float(perm[:, k].std(ddof=1)) or 1e-9
        res_color[f"{nombre}|{color}"] = {
            "n": int(n), "obs": int(o), "tasa": float(o / n),
            "nulo_media": media, "nulo_sd": sd,
            "z": float((o - media) / sd), "p_exceso": float(p_exc),
            "p_bilateral": float(min(1, 2 * min(p_exc, 1 - p_exc + 1 / (B_COLOR + 1))))
        }
    print(nombre, "terminado")

# ------------------------------------------- grupo de procedencia (nivel quipu)
qu = val.groupby("kfg").agg(
    n=("v", "size"), par=("par", "mean"), u0=("u0", "mean"),
    c100=("c100", "mean"), media=("v", "mean"), maxv=("v", "max"),
    nivel1=("nivel", lambda s: float((s > 0).mean()))).reset_index()
qu = qu.merge(q[["kfg", "procedencia", "region"]], on="kfg", how="left")
qu["macro"] = qu.procedencia.map(__import__("comun").macro_region)
print(qu.macro.value_counts().to_string())

def perm_grupo(col, grupo, B=10000):
    d = qu[["kfg", col, "macro"]].dropna()
    dentro = d.macro.isin(grupo).values
    if dentro.sum() < 3 or (~dentro).sum() < 3:
        return None
    a = d.loc[dentro, col].values
    b = d.loc[~dentro, col].values
    obs = a.mean() - b.mean()
    lab = dentro.copy()
    vals = d[col].values
    cnt = 0
    for _ in range(B):
        RNG.shuffle(lab)
        if vals[lab].mean() - vals[~lab].mean() >= obs:
            cnt += 1
    return {"grupo": "+".join(grupo), "n_grupo": len(a), "n_resto": len(b),
            "obs": float(obs), "p_exceso": float((1 + cnt) / (B + 1))}

res_proc = {}
for grupo in [["costa_norte_yunga"], ["costa_norcentral"],
              ["costa_norte_yunga", "costa_norcentral"]]:
    for col in ["par", "u0", "c100", "media", "maxv", "n", "nivel1"]:
        r = perm_grupo(col, grupo)
        if r:
            res_proc[f"{col}|{'+'.join(grupo)}"] = r
for k, v in res_proc.items():
    print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})

# ------------------------------------------------ pares: valores iguales seguidos
lvl0 = val[val.nivel == 0].sort_values(["kfg", "orden"]).reset_index(drop=True)
v0 = lvl0.v.values
gid0 = pd.factorize(lvl0.kfg)[0]
n0 = len(lvl0)
same0 = gid0[:-1] == gid0[1:]
obs_pares = int((same0 & (v0[:-1] > 1) & (v0[:-1] == v0[1:])).sum())
B_pair = 3000
cnt = 0
nulls = []
for _ in range(B_pair):
    vp = v0[np.lexsort((RNG.random(n0), gid0))]
    s = int((same0 & (vp[:-1] > 1) & (vp[:-1] == vp[1:])).sum())
    nulls.append(s)
    if s >= obs_pares:
        cnt += 1
nulls = np.array(nulls)
p_pares = (1 + cnt) / (B_pair + 1)
res_pares = {"obs": obs_pares, "nulo_media": float(nulls.mean()),
             "nulo_sd": float(nulls.std(ddof=1)),
             "z": float((obs_pares - nulls.mean()) / nulls.std(ddof=1)),
             "p_exceso": float(p_pares),
             "cuerdas_nivel0": int(n0),
             "tasa": float(obs_pares / max(n0 - len(grupos_idx), 1))}
print("pares adyacentes:", res_pares)

# --------------------------------------------------- grupos de tamaño 10
g = pd.read_csv(RAIZ + r"\analisis\datos\grupos.csv")
g["size"] = g.hasta - g.desde + 1
obs10 = int((g["size"] == 10).sum())
exp10 = 0.0; var10 = 0.0
from math import comb
for kfg, d in g.groupby("kfg"):
    n = int(d["size"].sum()); k = len(d)
    if k < 2 or n < 10 + k - 1:
        continue
    p = comb(n - 11, k - 2) / comb(n - 1, k - 1)
    exp10 += p * k
    var10 += p * (1 - p) * k
z10 = (obs10 - exp10) / (var10 ** 0.5)
p10 = float(2 * (1 - stats.norm.cdf(abs(z10))))
# controles negativos: tamaños vecinos
vecinos = {s: int((g["size"] == s).sum()) for s in range(5, 16)}
res_grupo10 = {"obs10": obs10, "esperado": float(exp10), "z": float(z10),
               "p": p10, "tamanos_5_15": vecinos, "n_grupos": int(len(g))}
print("grupos tamaño 10:", res_grupo10)

# ------------------------------------- color como marcador de límites de grupo
lvl0["cb"] = lvl0.color_base.values
cb0 = lvl0.cb.values
gr0 = lvl0.grupo.values
same0b = gid0[:-1] == gid0[1:]
bound0 = same0b & (gr0[:-1] != gr0[1:])
within0 = same0b & ~bound0
chg0 = cb0[:-1] != cb0[1:]
obs_bound = chg0[bound0]
obs_within = chg0[within0]
stat_obs = np.mean(obs_bound) - np.mean(obs_within)
B_b = 3000
cnt = 0
for _ in range(B_b):
    cbp = cb0[np.lexsort((RNG.random(n0), gid0))]
    ch = cbp[:-1] != cbp[1:]
    st = ch[bound0].mean() - ch[within0].mean()
    if st >= stat_obs:
        cnt += 1
p_bound = (1 + cnt) / (B_b + 1)
res_bound = {"tasa_cambio_en_limite": float(np.mean(obs_bound)),
             "tasa_cambio_dentro": float(np.mean(obs_within)),
             "dif": float(stat_obs), "n_pares_limite": int(bound0.sum()),
             "n_pares_dentro": int(within0.sum()), "p_exceso": float(p_bound)}
print("color y límites:", res_bound)

# --------------------------------------- prelación: grupos altos primero
grp = val[val.nivel == 0].groupby(["kfg", "grupo"], sort=True).v.sum().reset_index()
cuenta = grp.groupby("kfg").size()
grp = grp[grp.kfg.isin(cuenta[cuenta >= 4].index)].copy()
qid = pd.factorize(grp.kfg)[0]
pos = grp.groupby("kfg").cumcount().values.astype(float)
gtot = grp.v.values.astype(float)
gmean = grp.groupby("kfg").v.transform("mean").values
posmean = pd.Series(pos).groupby(qid).transform("mean").values
posc = pos - posmean
gtc = gtot - gmean
den_pre = np.sqrt(np.sum(posc ** 2) * np.sum(gtc ** 2))
obs_rho = float(np.sum(posc * gtc) / den_pre)
B_pre = 2000
cnt = 0
ng = len(grp)
for _ in range(B_pre):
    gp = gtot[np.lexsort((RNG.random(ng), qid))]
    gpc = gp - gmean
    r = np.sum(posc * gpc) / den_pre
    if r <= obs_rho:  # prelación = grupos importantes primero (correlación negativa)
        cnt += 1
p_pre = (1 + cnt) / (B_pre + 1)
res_pre = {"r_medio": obs_rho, "n_quipus": int(grp.kfg.nunique()),
           "p_cola_negativa": float(p_pre)}
print("prelación:", res_pre)

# ------------------------------------------------ ordinal: orden vs valor
x = lvl0.orden.values.astype(float)
xmean = lvl0.groupby("kfg").orden.transform("mean").values
xc = x - xmean
vmean = lvl0.groupby("kfg").v.transform("mean").values
vc = v0 - vmean
den_or = np.sqrt(np.sum(xc ** 2) * np.sum(vc ** 2))
obs_rho0 = float(np.sum(xc * vc) / den_or)
B_or = 2000
cnt = 0
for _ in range(B_or):
    vp = v0[np.lexsort((RNG.random(n0), gid0))]
    vpc = vp - vmean
    r = np.sum(xc * vpc) / den_or
    if abs(r) >= abs(obs_rho0):
        cnt += 1
p_or = (1 + cnt) / (B_or + 1)
# Spearman descriptivo por quipu (solo una vez)
sp = []
for kfg, d in lvl0.groupby("kfg"):
    if len(d) >= 8 and d.v.nunique() > 1:
        rho = stats.spearmanr(d.orden.values, d.v.values).statistic
        if np.isfinite(rho):
            sp.append((rho, len(d)))
res_ord = {"r_intragrupo": obs_rho0,
           "spearman_medio": float(np.average([a for a, _ in sp],
                                              weights=[b for _, b in sp])) if sp else np.nan,
           "n_quipus_spearman": len(sp), "p_bilateral": float(p_or)}
print("ordinal:", res_ord)

# ------------------------------------- estructura: Santa vs resto (nivel quipu)
feats = ["n", "par", "u0", "c100", "media", "maxv", "nivel1"]
res_estruct = {}
d = qu.dropna(subset=["macro"])
for col in feats:
    a = np.log1p(d[d.macro == "costa_norcentral"][col].values)
    b = np.log1p(d[d.macro != "costa_norcentral"][col].values)
    if len(a) < 3:
        continue
    obs = a.mean() - b.mean()
    lab = d.macro.values.copy(); vals = np.log1p(d[col].values)
    cnt = 0
    for _ in range(10000):
        RNG.shuffle(lab)
        if vals[lab == "costa_norcentral"].mean() - vals[lab != "costa_norcentral"].mean() >= obs:
            cnt += 1
    res_estruct[col] = {"n_santa": len(a), "n_resto": len(b),
                        "obs_log": float(obs), "p_exceso": float((1 + cnt) / 10001)}
print("estructura Santa:", res_estruct)

# ------------------------------------------------------ calendario / 730 cuerdas
cal = []
for kfg, d in c.groupby("kfg"):
    if 700 <= len(d) <= 800:
        gg = g[g.kfg == kfg]
        cal.append({"kfg": kfg, "cuerdas": len(d), "grupos": int(gg.grupo.nunique()),
                    "n_grupos_29_31": int(gg["size"].between(29, 31).sum())})
res_cal = {"quipus_700_800": cal,
           "quipus_con_24_grupos_29_31": int(sum(1 for x in cal if x["n_grupos_29_31"] >= 24))}

# ------------------------------------------------------------- tabla de p-valores
filas = []
for k, v in res_color.items():
    filas.append({"prueba": "color_" + k, "p": v["p_exceso"],
                  "efecto": v["tasa"] - v["nulo_media"] / v["n"],
                  "detalle": json.dumps(v, ensure_ascii=False)})
for k, v in res_proc.items():
    filas.append({"prueba": "procedencia_" + k, "p": v["p_exceso"],
                  "efecto": v["obs"], "detalle": json.dumps(v, ensure_ascii=False)})
filas += [
    {"prueba": "pares_adyacentes", "p": res_pares["p_exceso"],
     "efecto": res_pares["obs"], "detalle": json.dumps(res_pares, ensure_ascii=False)},
    {"prueba": "grupo_tamano10", "p": res_grupo10["p"],
     "efecto": res_grupo10["z"], "detalle": json.dumps(res_grupo10, ensure_ascii=False)},
    {"prueba": "color_limite_grupo", "p": res_bound["p_exceso"],
     "efecto": res_bound["dif"], "detalle": json.dumps(res_bound, ensure_ascii=False)},
    {"prueba": "prelacion_grupos", "p": res_pre["p_cola_negativa"],
     "efecto": res_pre["r_medio"], "detalle": json.dumps(res_pre, ensure_ascii=False)},
    {"prueba": "ordinal_orden_valor", "p": res_ord["p_bilateral"],
     "efecto": res_ord["r_intragrupo"], "detalle": json.dumps(res_ord, ensure_ascii=False)},
    {"prueba": "mult100_independencia", "p": desc["mult100"]["p_exceso"],
     "efecto": desc["mult100"]["ratio"], "detalle": json.dumps(desc["mult100"], ensure_ascii=False)},
]
for k, v in res_estruct.items():
    filas.append({"prueba": "estructura_santa_" + k, "p": v["p_exceso"],
                  "efecto": v["obs_log"], "detalle": json.dumps(v, ensure_ascii=False)})

res = pd.DataFrame(filas)
res["p_holm"], res["p_bh"] = bh_holm(res.p.values)
res = res.sort_values("p")
res.to_csv(OUT + r"\resultados.csv", index=False)
with open(OUT + r"\resumen.json", "w", encoding="utf-8") as f:
    json.dump({"descriptivos": desc, "color": res_color, "procedencia": res_proc,
               "pares": res_pares, "grupo10": res_grupo10, "limites": res_bound,
               "prelacion": res_pre, "ordinal": res_ord, "estructura": res_estruct,
               "calendario": res_cal}, f, ensure_ascii=False, indent=1)
print("\nRESULTADOS (p<0.10):")
print(res[res.p < 0.10][["prueba", "p", "p_holm", "p_bh", "efecto"]].to_string(index=False))
print("\nfilas totales:", len(res))
