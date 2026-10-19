"""
Pruebas de las convenciones que Salomon (2004) documenta en Tupicocha
sobre el corpus antiguo (KFG, analisis/datos/cuerdas.csv).

Unidad de analisis = quipu. Los contrastes a nivel de cuerda usan
permutaciones DENTRO de cada quipu y se agregan por z-sum (o por
permutacion a nivel de quipu cuando el estadistico es un conteo).
Semilla fija. Salida: resultados_tests.csv.
"""
import re
import numpy as np
import pandas as pd
from scipy.stats import norm, binom

RNG = np.random.default_rng(20261018)
B = 2000
BASE = "analisis/datos/"

d = pd.read_csv(BASE + "cuerdas.csv", low_memory=False)
q = pd.read_csv(BASE + "quipus.csv", low_memory=False)
d["kfg"] = d["kfg"].astype(str)

def clean_color(s):
    if not isinstance(s, str):
        return "?"
    s = re.sub(r"\([^)]*\)", "", s).strip().upper()
    return s if s else "?"

BROWN = {"AB", "MB", "KB", "YB", "B", "LB", "NB", "DB", "HB", "RB",
         "CB", "FB", "BB", "OB", "TB"}
def family(s):
    if s == "?":
        return "OT"
    first = re.split(r"[:/\-]", s)[0].strip()
    if first.startswith("W"):
        return "W"
    if first in BROWN or (first.endswith("B") and first not in {"BL"}):
        return "BR"
    if first in {"R", "RL", "PR", "PK", "LR", "RM"}:
        return "RD"
    if first in {"BL", "PB", "BS"}:
        return "BL"
    if first in {"Y", "SY", "YG"}:
        return "YL"
    if first.endswith("G"):
        return "GY"
    if first in {"G", "GN"}:
        return "GN"
    return "OT"

d["c0"] = d["color"].map(clean_color)
d["fam"] = d["c0"].map(family)
d["blanco"] = d["nudos"].fillna("").astype(str).str.strip().eq("")
d["tors"] = d["torsion"].where(d["torsion"].isin(["S", "Z"]))
lv0 = d[d.nivel == 0].sort_values(["kfg", "orden"])

def runs(x):
    x = np.asarray(x)
    if len(x) == 0:
        return 0
    return 1 + int(np.sum(x[1:] != x[:-1]))

def z_runs(vals, nperm=B):
    vals = np.asarray(vals)
    obs = runs(vals)
    if len(vals) < 3 or len(set(vals)) < 2:
        return None
    perm = np.empty(nperm)
    v = vals.copy()
    for i in range(nperm):
        RNG.shuffle(v)
        perm[i] = runs(v)
    sd = perm.std()
    if sd == 0:
        return None
    return (obs - perm.mean()) / sd, obs / perm.mean()

def summarize(name, zs, ratios):
    zs = np.array(zs, float)
    Z = zs.sum() / np.sqrt(len(zs))
    return dict(test=name, n_quipus=len(zs), Z=Z,
                # p de una cola en la direccion observada (efecto = agrupamiento
                # si Z<0 para rachas; se informa el signo)
                p=float(2 * min(norm.cdf(Z), 1 - norm.cdf(Z))),
                efecto=float(np.median(ratios)),
                frac_z_2=float((np.abs(zs) > 2).mean()))

# ---------------------------------------------------------------- T1 color
def test_color_runs():
    out = []
    for within in (False, True):
        zs, ratios = [], []
        for kfg, g in lv0.groupby("kfg"):
            if len(g) < 8:
                continue
            if within:
                pieces = [h.fam.values for _, h in g.groupby("grupo", sort=False)
                          if len(set(h.fam.values)) > 1]
                if sum(len(p) for p in pieces) < 8:
                    continue
                obs = sum(runs(p) for p in pieces)
                perm = np.empty(500)
                for i in range(500):
                    s = 0
                    for p in pieces:
                        v = p.copy(); RNG.shuffle(v); s += runs(v)
                    perm[i] = s
            else:
                f = g.fam.values
                if len(set(f)) < 2:
                    continue
                obs = runs(f)
                perm = np.empty(500)
                v = f.copy()
                for i in range(500):
                    RNG.shuffle(v); perm[i] = runs(v)
            if perm.std() == 0:
                continue
            zs.append((obs - perm.mean()) / perm.std())
            ratios.append(obs / perm.mean())
        out.append(summarize("T1_color_bandas" + ("_dentro_grupo" if within else ""),
                             zs, ratios))
    return out

# ---------------------------------------------------------------- T2 torsion
def test_torsion():
    out = []
    for halves in (False, True):
        zs, ratios = [], []
        for kfg, g in lv0.groupby("kfg"):
            t = g.tors.dropna().values
            if len(t) < 8 or len(set(t)) < 2:
                continue
            if halves:
                h = len(t) // 2
                obs = abs((t[:h] == "S").mean() - (t[h:] == "S").mean())
                perm = np.empty(B)
                v = t.copy()
                for i in range(B):
                    RNG.shuffle(v)
                    perm[i] = abs((v[:h] == "S").mean() - (v[h:] == "S").mean())
                ratios.append(obs)
            else:
                obs = runs(t)
                perm = np.empty(500)
                v = t.copy()
                for i in range(500):
                    RNG.shuffle(v); perm[i] = runs(v)
                ratios.append(obs / perm.mean())
            if perm.std() == 0:
                continue
            zs.append((obs - perm.mean()) / perm.std())
        out.append(summarize("T2_torsion" + ("_mitades" if halves else "_rachas"),
                             zs, ratios))
    return out

# ---------------------------------------------------------------- T3 blancos
def test_blanks():
    zs, ratios, fr = [], [], []
    for kfg, g in lv0.groupby("kfg"):
        b = g.blanco.values.astype(int)
        if len(b) < 8 or b.sum() < 2 or b.sum() > len(b) - 2:
            continue
        obs = runs(b)
        perm = np.empty(500)
        v = b.copy()
        for i in range(500):
            RNG.shuffle(v); perm[i] = runs(v)
        if perm.std() == 0:
            continue
        zs.append((obs - perm.mean()) / perm.std())
        ratios.append(obs / perm.mean())
        fr.append(b.mean())
    r = summarize("T3_blancos_rachas", zs, ratios)
    r["frac_medio_blancos"] = float(np.mean(fr))
    return r

# ---------------------------------------------------------------- T4 primera cuerda
def test_first_cord(field):
    obs_list, all_list = [], []
    for kfg, g in lv0.groupby("kfg"):
        if len(g) < 5:
            continue
        if field == "distinto_vecino":
            f = g.fam.values
            v = np.empty(len(f), bool)
            v[0] = f[0] != f[1] if len(f) > 1 else True
            v[1:] = f[1:] != f[:-1]
        else:
            v = g[field].values.astype(float)
        obs_list.append(float(v[0]))
        all_list.append(v)
    obs = np.mean([a - b.mean() for a, b in zip(obs_list, all_list)])
    perm = np.empty(B)
    for i in range(B):
        perm[i] = np.mean([b[RNG.integers(len(b))] - b.mean() for b in all_list])
    p = (1 + np.sum(perm >= obs)) / (B + 1)
    return dict(test=f"T4_primera_cuerda_{field}", n_quipus=len(obs_list),
                Z=np.nan, p=float(p), efecto=float(obs),
                frac_z_2=float(np.mean(obs_list)))

# ---------------------------------------------------------------- T5 orden de color
def color_order(fams):
    seen, order = set(), []
    for f in fams:
        if f not in seen:
            seen.add(f); order.append(f)
    return order

def test_color_order():
    prov = q.set_index("kfg")["procedencia"].fillna("Unknown")
    rows = []
    for kfg, g in lv0.groupby("kfg"):
        if len(g) < 10:
            continue
        o = color_order(g.fam.values)
        if len(o) >= 3:
            rows.append((kfg, prov.get(kfg, "Unknown"), o))
    df = pd.DataFrame(rows, columns=["kfg", "proc", "order"])
    obs_s, null = [], []
    ngroups = 0
    for proc, g in df.groupby("proc"):
        if len(g) < 4:
            continue
        ngroups += 1
        orders = list(g.order)
        vals = [orders[i][0] == orders[j][0]
                for i in range(len(orders)) for j in range(i + 1, len(orders))]
        obs_s.append(np.mean(vals))
        for _ in range(200):
            sh = [list(RNG.permutation(o)) for o in orders]
            v2 = [sh[i][0] == sh[j][0]
                  for i in range(len(sh)) for j in range(i + 1, len(sh))]
            null.append(np.mean(v2))
    obs = float(np.mean(obs_s))
    null = np.array(null)
    p = (1 + np.sum(null >= obs)) / (len(null) + 1)
    return dict(test="T5_orden_color_entre_quipus_mismo_sitio", n_quipus=len(df),
                Z=np.nan, p=float(p), efecto=obs - float(null.mean()),
                frac_z_2=float(obs))

# ---------------------------------------------------------------- T6 sumas
def test_group_head_sums():
    obs_tot, zs = 0, []
    for kfg, gk in lv0.groupby("kfg"):
        per_q_obs, per_q_null = 0, np.zeros(500)
        for gr, g in gk.groupby("grupo"):
            v = g.valor.values.astype(float)
            if len(v) < 3 or np.isnan(v).any() or (v == 0).all():
                continue
            s = v.sum()
            per_q_obs += int(2 * v[0] == s)
            perm = np.empty(500)
            for i in range(500):
                w = v.copy(); RNG.shuffle(w)
                perm[i] = int(2 * w[0] == s)
            per_q_null += perm
        obs_tot += per_q_obs
        sd = per_q_null.std()
        if sd > 0:
            zs.append((per_q_obs - per_q_null.mean()) / sd)
    Z = np.sum(zs) / np.sqrt(len(zs))
    return dict(test="T6_cabeza_grupo_igual_suma_resto", n_quipus=len(zs),
                Z=Z, p=float(1 - norm.cdf(Z)), efecto=float(obs_tot),
                frac_z_2=float((np.array(zs) > 2).mean()))

def test_topcord_sums():
    n, ok = 0, 0
    for (kfg, gr), g in d.groupby(["kfg", "grupo"]):
        tc = g[g.union == "T"]
        rest = g[(g.union != "T") & (g.nivel == 0)]
        if len(tc) != 1 or len(rest) < 2:
            continue
        if rest.valor.isna().any() or tc.valor.isna().any():
            continue
        n += 1
        if abs(tc.valor.iloc[0] - rest.valor.sum()) < 1e-6:
            ok += 1
    return dict(test="T6b_cuerda_superior_igual_suma", n_quipus=n, Z=np.nan,
                p=np.nan, efecto=ok, frac_z_2=np.nan)

# ---------------------------------------------------------------- T3b blancos intra-grupo
def test_blanks_within_groups():
    zs, ratios = [], []
    for kfg, g in lv0.groupby("kfg"):
        pieces, obs = [], 0
        for _, h in g.groupby("grupo", sort=False):
            b = h.blanco.values.astype(int)
            if len(b) >= 3 and 0 < b.sum() < len(b):
                pieces.append(b); obs += runs(b)
        if not pieces or sum(len(p) for p in pieces) < 8:
            continue
        perm = np.empty(500)
        for i in range(500):
            s = 0
            for p in pieces:
                v = p.copy(); RNG.shuffle(v); s += runs(v)
            perm[i] = s
        if perm.std() == 0:
            continue
        zs.append((obs - perm.mean()) / perm.std())
        ratios.append(obs / perm.mean())
    return summarize("T3b_blancos_rachas_dentro_grupo", zs, ratios)

# ---------------------------------------------------------------- T8 color y valor
def test_color_value():
    """Salomon: el color agrupa funciones, no cantidades. Si el color fuese
    una etiqueta funcional sin relacion con el numero, no deberia explicar
    el valor. Estadistico: eta^2 de valor por familia de color, dentro de
    cada quipu, frente a permutacion de valores."""
    zs, etas = [], []
    for kfg, g in lv0.groupby("kfg"):
        gg = g.dropna(subset=["valor"])
        gg = gg[gg.valor > 0]
        if len(gg) < 10 or gg.fam.nunique() < 2:
            continue
        y = gg.valor.values.astype(float)
        y = np.log1p(y)
        f = gg.fam.values
        def eta2(yy, ff):
            gm = yy.mean()
            sst = ((yy - gm) ** 2).sum()
            if sst == 0:
                return 0.0
            ssb = sum(len(yy[ff == c]) * (yy[ff == c].mean() - gm) ** 2
                      for c in set(ff))
            return ssb / sst
        obs = eta2(y, f)
        perm = np.array([eta2(RNG.permutation(y), f) for _ in range(300)])
        if perm.std() == 0:
            continue
        zs.append((obs - perm.mean()) / perm.std())
        etas.append(obs)
    return summarize("T8_color_explica_valor", zs, etas)

# ---------------------------------------------------------------- T7 subsidiarias
def test_subsidiary_contrast():
    sub = d[d.nivel >= 1].copy()
    par = lv0.set_index(["kfg", "cuerda"])["fam"]
    par = par[~par.index.duplicated()]
    sub["fam_padre"] = [par.get((k, p), None) for k, p in zip(sub.kfg, sub.padre)]
    sub = sub.dropna(subset=["fam_padre"])
    sub = sub[sub.fam_padre != "OT"]
    zs, obs_m, null_m = [], [], []
    for kfg, g in sub.groupby("kfg"):
        if len(g) < 3:
            continue
        padres = lv0[(lv0.kfg == kfg) & (lv0.fam != "OT")].fam.values
        if len(padres) < 2:
            continue
        obs = (g.fam.values != g.fam_padre.values).mean()
        sims = np.array([(g.fam.values != RNG.choice(padres, len(g))).mean()
                         for _ in range(200)])
        obs_m.append(obs); null_m.append(sims.mean())
        sd = sims.std()
        if sd > 0:
            zs.append((obs - sims.mean()) / sd)
    Z = np.sum(zs) / np.sqrt(len(zs))
    return dict(test="T7_subsidiaria_color_contrasta", n_quipus=len(zs), Z=Z,
                p=float(2 * min(norm.cdf(Z), 1 - norm.cdf(Z))),
                efecto=float(np.mean(obs_m) - np.mean(null_m)),
                frac_z_2=float(np.mean(obs_m)))

def descriptivo():
    n0 = lv0.groupby("kfg").size()
    ng = lv0.groupby("kfg").grupo.nunique()
    sel = n0[n0 >= 20].index
    gs = ng.loc[sel]
    tam = lv0[lv0.kfg.isin(sel)].groupby(["kfg", "grupo"]).size()
    return dict(n_quipus=int(len(sel)),
                grupos_mediana=float(gs.median()), grupos_moda=int(gs.mode().iloc[0]),
                grupos_p25=float(gs.quantile(.25)), grupos_p75=float(gs.quantile(.75)),
                frac_grupos_15_16=float(((gs >= 15) & (gs <= 16)).mean()),
                cuerdas_mediana=float(n0.loc[sel].median()),
                tam_grupo_mediana=float(tam.median()),
                tam_grupo_moda=int(tam.mode().iloc[0]))

rows = []
for f in test_color_runs():
    rows.append(f)
for f in test_torsion():
    rows.append(f)
rows += [test_blanks(), test_blanks_within_groups(), test_color_value(),
         test_first_cord("blanco"),
         test_first_cord("distinto_vecino"),
         test_color_order(),
         test_group_head_sums(),
         test_topcord_sums(),
         test_subsidiary_contrast()]

res = pd.DataFrame(rows)
pv = res["p"].astype(float).values
m = int(np.sum(~np.isnan(pv)))
order = np.argsort(pv)
q = np.full(len(pv), np.nan)
prev = 0.0
for rank, i in enumerate(order):
    if np.isnan(pv[i]):
        continue
    prev = max(prev, min(pv[i] * (m - rank), 1.0))
    q[i] = prev
res["q_holm"] = q
res.to_csv("analisis/ds/n_salomon/resultados_tests.csv", index=False)
pd.set_option("display.width", 250)
print(res.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
print()
print("DESCRIPTIVO:", descriptivo())
