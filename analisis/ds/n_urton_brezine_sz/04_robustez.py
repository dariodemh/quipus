# -*- coding: utf-8 -*-
"""
04_robustez.py
Robustez del efecto archivo->direccion de nudo:
  - por tipo de nudo (S, L, E)
  - excluyendo canutos, Arica (42% U) y quipus mal documentados
  - leave-one-archive-out
  - bootstrap de eta2 e intervalos por archivo
  - agrupacion alternativa por region
  - prueba binaria todo-Z
"""
import re
import sqlite3
import numpy as np
import pandas as pd

BASE = r"."
OUT = BASE + r"\analisis\ds\n_urton_brezine_sz"
DB = BASE + r"\data\external\open-khipu-repository\data\khipu.db"
RNG = np.random.default_rng(20261017)
B = 10000

quipus = pd.read_csv(BASE + r"\analisis\datos\quipus.csv")
quipus["prov"] = quipus.procedencia.fillna("").str.strip()
quipus.loc[quipus.prov.str.lower().isin(["unknown", ""]), "prov"] = "SIN"
exec(open(OUT + r"\arch12.py", encoding="utf-8").read())
quipus["arch"] = quipus.prov.map(arch12)
quipus.loc[quipus.region.fillna("").str.strip() == "Puruchuco", "arch"] = "Puruchuco"

cuerdas = pd.read_csv(BASE + r"\analisis\datos\cuerdas.csv")
PAT = re.compile(r"(\d+)([A-Z]+)\(([-\d.]+),([SZUszu]?)\)")
rows = []
for r in cuerdas.itertuples():
    if not isinstance(r.nudos, str):
        continue
    for m in PAT.finditer(r.nudos):
        t = m.group(2)
        d = (m.group(4) or "U").upper()
        n = int(m.group(1)) if t in ("S", "SP") else 1
        if d not in ("S", "Z"):
            d = "U"
        rows.append((r.kfg, t, d, n))
kk = pd.DataFrame(rows, columns=["kfg", "t", "d", "n"])
kk = kk.merge(quipus.set_index("kfg")[["arch", "region"]], left_on="kfg", right_index=True, how="left")


def perquipu(df):
    o = df[df.d.isin(["S", "Z"])]
    g = o.groupby("kfg").d.agg(n_dir="size", pZ=lambda s: (s == "Z").mean())
    u = df.groupby("kfg").n.sum()
    g["n_total"] = u.reindex(g.index)
    g["pct_U"] = 100 * (1 - g.n_dir / g.n_total)
    g = g.join(quipus.set_index("kfg")[["arch", "region"]], how="left")
    return g.reset_index()


def eta2(y, codes, k):
    y = np.asarray(y, float)
    n = np.bincount(codes, minlength=k).astype(float)
    s = np.bincount(codes, weights=y, minlength=k)
    ok = n > 0
    gm = y.mean()
    ssb = (n[ok] * (s[ok] / n[ok] - gm) ** 2).sum()
    sst = ((y - gm) ** 2).sum()
    return ssb / sst if sst > 0 else np.nan


def perm_global(y, g, B=B, strata=None):
    y = np.asarray(y, float)
    codes, uniq = pd.factorize(g)
    k = len(uniq)
    obs = eta2(y, codes, k)
    cnt = 0
    if strata is None:
        for _ in range(B):
            if eta2(y, RNG.permutation(codes), k) >= obs:
                cnt += 1
    else:
        sc, _ = pd.factorize(strata)
        for _ in range(B):
            cp = codes.copy()
            for sv in np.unique(sc):
                idx = np.where(sc == sv)[0]
                cp[idx] = RNG.permutation(cp[idx])
            if eta2(y, cp, k) >= obs:
                cnt += 1
    return obs, (1 + cnt) / (B + 1)


L = []
A = L.append

# --- por tipo de nudo
A("=== EFECTO ARCHIVO POR TIPO DE NUDO (KFG; quipus con >=10 nudos del tipo) ===")
for t, nm in [("S", "simples"), ("L", "largos"), ("E", "figura de ocho")]:
    g = perquipu(kk[kk.t == t])
    g = g[g.n_dir >= 10]
    e, p = perm_global(g.pZ.values, g.arch.values)
    A(f"{nm}: n={len(g)} quipus, nudos={int(g.n_dir.sum())}, eta2={e:.3f}, p={p:.4f}, "
      f"pZ global={g.pZ.mul(g.n_dir).sum()/g.n_dir.sum():.3f}")
    # control tamano
    g2 = g.copy()
    g2["ter"] = pd.qcut(g2.n_dir, 3, labels=False, duplicates="drop")
    g2["res"] = g2.pZ - g2.groupby("ter").pZ.transform("mean")
    e2, p2 = perm_global(g2.res.values, g2.arch.values, strata=g2.ter.values)
    A(f"   control tamano: eta2={e2:.3f}, p={p2:.4f}")

# --- subconjuntos
g_all = perquipu(kk)
g_S = perquipu(kk[kk.t == "S"])
A("")
A("=== ROBUSTEZ: SUBCONJUNTOS (todos los tipos; >=10 nudos orientados) ===")
tests = []
# canutos
d = pd.read_csv(BASE + r"\data\external\data-science-khipu-article\data\khipu_summary.csv")
can = set(d.loc[d.num_canuto_cords > 0, "kfg_name"])
tests.append(("sin khipus canuto", g_all[~g_all.kfg.isin(can)]))
tests.append(("sin Arica", g_all[g_all.arch != "Arica"]))
tests.append(("solo U<=10%", g_all[g_all.pct_U <= 10]))
tests.append(("solo U<=20%", g_all[g_all.pct_U <= 20]))
tests.append(("solo 12 archivos", g_all[g_all.arch.isin(
    ["Pachacamac", "Ica", "Laguna de los Condores", "Nazca", "Arica", "Paracas",
     "Chancay", "Santa", "Ocucaje", "Atarco", "Tambo Colorado", "Puruchuco"])]))
tests.append(("solo >=50 nudos", g_all[g_all.n_dir >= 50]))
for nm, g in tests:
    g = g[g.n_dir >= 10]
    e, p = perm_global(g.pZ.values, g.arch.values)
    A(f"{nm}: n={len(g)}, eta2={e:.3f}, p={p:.4f}")

# --- leave-one-archive-out
A("")
A("=== LEAVE-ONE-ARCHIVE-OUT (eta2 global) ===")
base = g_all[g_all.n_dir >= 10]
e0, _ = perm_global(base.pZ.values, base.arch.values)
A(f"todos: eta2={e0:.3f}, n={len(base)}")
for a in ["Pachacamac", "Ica", "Laguna de los Condores", "Nazca", "Arica", "Paracas", "Ocucaje", "Santa"]:
    x = base[base.arch != a]
    e, _ = perm_global(x.pZ.values, x.arch.values, B=0)
    A(f"sin {a}: eta2={e:.3f}, n={len(x)}")

# --- bootstrap de eta2 y de medias por archivo
A("")
A("=== BOOTSTRAP (quipu, 2000 remuestras) ===")
base = g_all[g_all.n_dir >= 10].reset_index(drop=True)
codes, uniq = pd.factorize(base.arch)
k = len(uniq)
boot = []
for _ in range(2000):
    idx = RNG.integers(0, len(base), len(base))
    boot.append(eta2(base.pZ.values[idx], codes[idx], k))
boot = np.array(boot)
A(f"eta2={eta2(base.pZ.values, codes, k):.3f}; IC95% bootstrap=[{np.percentile(boot,2.5):.3f}, {np.percentile(boot,97.5):.3f}]")
for a in ["Pachacamac", "Ica", "Laguna de los Condores", "Nazca", "Arica", "Paracas", "Santa", "Ocucaje"]:
    x = base[base.arch == a]
    bs = [x.pZ.values[RNG.integers(0, len(x), len(x))].mean() for _ in range(2000)]
    A(f"{a}: pZ medio={x.pZ.mean():.3f} IC95=[{np.percentile(bs,2.5):.3f}, {np.percentile(bs,97.5):.3f}] n={len(x)}")

# --- control tasa de U (documentacion)
A("")
A("=== CONTROL: TASA DE DIRECCION DESCONOCIDA (U) ===")
base_u = g_all[g_all.n_dir >= 10].copy()
base_u["dec"] = pd.qcut(base_u.pct_U, 5, labels=False, duplicates="drop")
base_u["resU"] = base_u.pZ - base_u.groupby("dec").pZ.transform("mean")
e, p = perm_global(base_u.resU.values, base_u.arch.values)
A(f"pZ residualizado por quintiles de %U: eta2={e:.3f}, p={p:.4f}, n={len(base_u)}")
for qq in range(5):
    x = base_u[base_u.dec == qq]
    A(f"  quintil U {qq}: %U entre {x.pct_U.min():.0f}-{x.pct_U.max():.0f}, n={len(x)}, pZ medio={x.pZ.mean():.3f}")

# --- comparaciones concretas de Pachacamac
A("")
A("=== PACHACAMAC vs PURUCHUCO / SANTA (dos colas, permutacion) ===")
for t, nm in [(None, "todos"), ("S", "simples")]:
    gg = g_all if t is None else perquipu(kk[kk.t == t])
    gg = gg[gg.n_dir >= 10]
    for a in ["Puruchuco", "Santa", "Ica", "Ocucaje"]:
        x = gg[gg.arch.isin(["Pachacamac", a])]
        if (x.arch == a).sum() < 3:
            continue
        obs = x.loc[x.arch == "Pachacamac", "pZ"].mean() - x.loc[x.arch == a, "pZ"].mean()
        cnt = 0
        for _ in range(10000):
            lab = RNG.permutation(x.arch.values)
            d = x.pZ.values[lab == "Pachacamac"].mean() - x.pZ.values[lab == a].mean()
            if abs(d) >= abs(obs) - 1e-12:
                cnt += 1
        A(f"{nm}: Pachacamac({ (x.arch=='Pachacamac').sum() }) - {a}({(x.arch==a).sum()}) = {obs:.3f}, p={(1+cnt)/10001:.4f}")

# --- region
A("")
A("=== AGRUPACION ALTERNATIVA: REGION (KFG) ===")
g = g_all[(g_all.n_dir >= 10) & g_all.region.notna()].copy()
g["reg"] = g.region.str.strip().replace("", "NA")
big = g.reg.value_counts()
g = g[g.reg.isin(big[big >= 10].index)]
e, p = perm_global(g.pZ.values, g.reg.values)
A(f"region (grupos >=10 quipus): n={len(g)}, grupos={g.reg.nunique()}, eta2={e:.3f}, p={p:.4f}")
A(g.groupby("reg").agg(n=("pZ", "size"), pZ=("pZ", "mean")).round(3).sort_values("pZ", ascending=False).to_string())

# --- binario todo-Z
A("")
A("=== BINARIO TODO-Z vs TODO-S vs MIXTO POR ARCHIVO ===")
base = g_all[g_all.n_dir >= 10].copy()
base["pat"] = np.where(base.pZ == 1, "todoZ", np.where(base.pZ == 0, "todoS", "mixto"))
tab = base.groupby(["arch", "pat"]).size().unstack(fill_value=0)
for c in ["todoZ", "todoS", "mixto"]:
    if c not in tab:
        tab[c] = 0
tab["n"] = tab.sum(axis=1)
tab["pct_todoZ"] = (100 * tab.todoZ / tab.n).round(1)
A(tab.loc[[a for a in tab.index if a not in ("SIN", "Otros/vago")],
          ["todoZ", "todoS", "mixto", "n", "pct_todoZ"]].sort_values("pct_todoZ", ascending=False).to_string())
# chi2 con permutacion
from scipy import stats
ct = pd.crosstab(base.arch, base.pat)
chi = stats.chi2_contingency(ct)[0]
cnt = 0
for _ in range(5000):
    sh = pd.Series(RNG.permutation(base.pat.values), index=base.index)
    c2 = stats.chi2_contingency(pd.crosstab(base.arch, sh))[0]
    if c2 >= chi:
        cnt += 1
A(f"chi2={chi:.1f}, p_perm={(1+cnt)/5001:.4f}, V de Cramer={np.sqrt(chi/(len(base)*(min(ct.shape)-1))):.3f}")

with open(OUT + r"\salida_04.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
