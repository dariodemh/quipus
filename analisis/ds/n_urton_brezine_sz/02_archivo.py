# -*- coding: utf-8 -*-
"""
02_archivo.py
Test de asociacion entre direccion de nudo (S/Z) y archivo/procedencia.
Unidad = quipu. Nulo = permutacion de etiquetas de archivo entre quipus.
Controles: tamano, torsion de cordel, fibra; BH para comparaciones multiples.
Salida: salida_02.txt (compacta) + CSVs.
"""
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


def arch12(p):
    """Mapea la procedencia a los 12 archivos de la Tabla 2 de U&B 2009."""
    p0 = p.lower()
    if p0 == "sin":
        return "SIN"
    if "leymebamba" in p0:
        return "Laguna de los Condores"
    if "pachac" in p0:
        return "Pachacamac"
    if "puruchuco" in p0:
        return "Puruchuco"
    if "tambo colorado" in p0:
        return "Tambo Colorado"
    if "paracas" in p0 or "puntilla" in p0:
        return "Paracas"
    if "ocucaje" in p0 or "ullujaya" in p0 or "ullujalla" in p0:
        return "Ocucaje"
    if "atarco" in p0:
        return "Atarco"
    if "nazca" in p0 or "nasca" in p0 or "copara" in p0 or "cacatilla" in p0 or "santa clara" in p0:
        return "Nazca"
    if "arica" in p0 or "lluta" in p0 or "miller" in p0:
        return "Arica"
    if "chancay" in p0 or "huando" in p0:
        return "Chancay"
    if p0 == "santa" or "santa rosalia" in p0:
        return "Santa"
    if p0 == "ica" or "ica/" in p0 or "between ica" in p0 or "ica valley" in p0 or "callango" in p0:
        return "Ica"
    return "Otros/vago"


quipus["arch"] = quipus.prov.map(arch12)
quipus.loc[quipus.region.fillna("").str.strip() == "Puruchuco", "arch"] = "Puruchuco"
ARCHS = ["Pachacamac", "Ica", "Laguna de los Condores", "Nazca", "Arica",
         "Paracas", "Chancay", "Santa", "Ocucaje", "Atarco",
         "Tambo Colorado", "Puruchuco"]

# ------------------------------------------------------------------ datos
kfg = pd.read_csv(OUT + r"\perquipu_kfg.csv").merge(
    quipus.set_index("kfg")[["arch", "prov"]], left_on="kfg", right_index=True, how="left")
kfgS = pd.read_csv(OUT + r"\perquipu_kfg_S.csv").merge(
    quipus.set_index("kfg")[["arch"]], left_on="kfg", right_index=True, how="left")

con = sqlite3.connect(DB)
okm = pd.read_csv(OUT + r"\perquipu_okr.csv")
ok = okm.merge(quipus.set_index("okr")[["arch"]], left_on="OKR_NUM", right_index=True, how="left")
# si no hay match por okr, usar la agrupacion de provenance OKR
ok["arch"] = ok["arch"].fillna(ok["archivo"])


def _stats(y, codes, k):
    n = np.bincount(codes, minlength=k).astype(float)
    s = np.bincount(codes, weights=y, minlength=k)
    return n, s


def eta2(y, codes, k):
    y = np.asarray(y, float)
    n, s = _stats(y, codes, k)
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


def perm_pair(y, g, B=B):
    """p bilateral para cada grupo vs resto, matriz comun de permutaciones."""
    y = np.asarray(y, float)
    codes, uniq = pd.factorize(g)
    k = len(uniq)
    N = len(y)
    n, s = _stats(y, codes, k)
    tot = s.sum()
    obs = s / n - (tot - s) / (N - n)
    hits = np.zeros(k)
    for _ in range(B):
        cp = RNG.permutation(codes)
        n2 = np.bincount(cp, minlength=k).astype(float)
        s2 = np.bincount(cp, weights=y, minlength=k)
        d = s2 / n2 - (tot - s2) / (N - n2)
        hits += (np.abs(d) >= np.abs(obs) - 1e-12)
    return dict(zip(uniq, obs)), dict(zip(uniq, (1 + hits) / (B + 1)))


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        j = o[i]
        prev = min(prev, p[j] * n / (i + 1))
        q[j] = prev
    return q


L = []
A = L.append
A("=== MAPEO A LOS 12 ARCHIVOS DE LA TABLA 2 (U&B 2009) ===")
A(quipus.arch.value_counts().to_string())
A("")
A("Nuestros 12 archivos suman %d de %d quipus (%.1f%%); U&B: 222/451 (49.2%%)"
  % (quipus.arch.isin(ARCHS).sum(), len(quipus), 100 * quipus.arch.isin(ARCHS).mean()))
A("Pachacamac: %d en KFG (U&B 2009: 68); OKR: %d"
  % ((quipus.arch == "Pachacamac").sum(), (ok.arch == "Pachacamac").sum()))

# ------------------------------------------------------------------ descriptivos
def descriptivos(df, col, ncol, name, minn=10):
    d = df[(df[ncol] >= minn) & df[col].notna()].copy()
    rows = []
    for a in ARCHS:
        x = d[d.arch == a]
        if len(x) == 0:
            continue
        rows.append({"archivo": a, "n_quipus": len(x), "nudos_orient": int(x[ncol].sum()),
                     "pZ_ponderado": round((x[col] * x[ncol]).sum() / x[ncol].sum(), 3),
                     "pZ_medio_quipu": round(x[col].mean(), 3),
                     "pZ_mediana": round(x[col].median(), 3),
                     "pct_todoZ": round(100 * (x[col] == 1).mean(), 1)})
    r = pd.DataFrame(rows).sort_values("pZ_ponderado", ascending=False)
    A("")
    A(f"--- {name} (quipus con >={minn} nudos orientados) ---")
    A(r.to_string(index=False))
    return r, d


t_all, d_all = descriptivos(kfg, "pZ", "n_dir", "KFG, todos los tipos")
t_S, d_S = descriptivos(kfgS, "pZ_S", "n_dir_S", "KFG, solo nudos simples (tipo S)")
t_ok, d_ok = descriptivos(ok, "pZ", "n_dir", "OKR, todos los tipos")

# ------------------------------------------------------------------ test global
A("")
A("=== TEST GLOBAL (unidad=quipu, permutacion de etiquetas de archivo) ===")
for raw, col, ncol, name, minn in [(kfg, "pZ", "n_dir", "KFG todos", 10),
                                   (kfgS, "pZ_S", "n_dir_S", "KFG simples", 10),
                                   (ok, "pZ", "n_dir", "OKR todos", 10),
                                   (kfg, "pZ", "n_dir", "KFG todos (>=50)", 50),
                                   (kfgS, "pZ_S", "n_dir_S", "KFG simples (>=20)", 20)]:
    x = raw[(raw[ncol] >= minn) & raw[col].notna()]
    e, p = perm_global(x[col].values, x.arch.values)
    A(f"{name}: n={len(x)} quipus, eta2={e:.3f}, p_perm={p:.4f}")

# control de tamano: permutacion estratificada por terciles de nudos
for raw, col, ncol, name, minn in [(kfg, "pZ", "n_dir", "KFG todos", 10),
                                   (kfgS, "pZ_S", "n_dir_S", "KFG simples", 10),
                                   (ok, "pZ", "n_dir", "OKR todos", 10)]:
    x = raw[(raw[ncol] >= minn) & raw[col].notna()].copy()
    # residualizar por media del estrato de tamano
    x["ter"] = pd.qcut(x[ncol], 3, labels=False, duplicates="drop")
    x["res"] = x[col] - x.groupby("ter")[col].transform("mean")
    e, p = perm_global(x["res"].values, x.arch.values, strata=x["ter"].values)
    A(f"{name}: control tamano (resid. por terciles, permutacion estratificada): eta2={e:.3f}, p={p:.4f}")

# ------------------------------------------------------------------ pairwise + BH
A("")
A("=== COMPARACIONES PAREADAS vs RESTO (solo archivos con >=8 quipus; BH dentro de la familia) ===")
for raw, col, ncol, name, minn in [(kfg, "pZ", "n_dir", "KFG todos", 10),
                                   (kfgS, "pZ_S", "n_dir_S", "KFG simples", 10)]:
    x0 = raw[(raw[ncol] >= minn) & raw[col].notna()]
    keep = [a for a in ARCHS if (x0.arch == a).sum() >= 8]
    x = x0[x0.arch.isin(keep)]
    obs, ps = perm_pair(x[col].values, x.arch.values)
    archs = list(obs)
    q = bh([ps[a] for a in archs])
    rows = pd.DataFrame({"archivo": archs,
                         "n": [int((x.arch == a).sum()) for a in archs],
                         "pZ_medio": [round(x.loc[x.arch == a, col].mean(), 3) for a in archs],
                         "dif_vs_resto": [round(obs[a], 3) for a in archs],
                         "p_perm": [round(ps[a], 4) for a in archs],
                         "q_BH": [round(v, 4) for v in q]}).sort_values("p_perm")
    A(f"--- {name} ---")
    A(rows.to_string(index=False))

# ------------------------------------------------------------------ Pachacamac
A("")
A("=== Pachacamac: mayor %Z? ===")
for t, col, name in [(t_all, "pZ_ponderado", "KFG todos"),
                     (t_S, "pZ_ponderado", "KFG simples"),
                     (t_ok, "pZ_ponderado", "OKR todos")]:
    r = t.sort_values(col, ascending=False)
    pos = list(r.archivo).index("Pachacamac") + 1 if "Pachacamac" in list(r.archivo) else None
    A(f"{name}: Pachacamac puesto {pos} de {len(r)}; top3={list(r.archivo.head(3))}; "
      f"pZ={r.loc[r.archivo=='Pachacamac',col].values}")

# ------------------------------------------------------------------ patron todo-Z
A("")
A("=== PATRON TODO-Z vs ARCHIVO (quipu; permutacion) ===")
for raw, col, name, minn in [(kfg, "pZ", "KFG todos", 10), (ok, "pZ", "OKR todos", 10)]:
    x = raw[(raw["n_dir"] >= minn) & raw[col].notna()].copy()
    x["todoZ"] = (x[col] == 1).astype(float)
    e, p = perm_global(x.todoZ.values, x.arch.values)
    A(f"{name}: n={len(x)}, todoZ={int(x.todoZ.sum())}, eta2={e:.3f}, p={p:.4f}")

# ------------------------------------------------------------------ torsion de cordel
A("")
A("=== CONTROL: TORSION DEL CORDEL ===")
cord = pd.read_sql("select KHIPU_ID, CORD_ID, TWIST from cord", con)
knot = pd.read_sql("select CORD_ID, DIRECTION from knot", con)
kk = knot.merge(cord, on="CORD_ID")
kk["dir"] = kk.DIRECTION.fillna("U")
kk.loc[~kk.dir.isin(["S", "Z"]), "dir"] = "U"
# asociacion nudo-torsion a nivel cuerda, nulo dentro de quipu
cg = kk[kk.dir.isin(["S", "Z"])].groupby(["KHIPU_ID", "CORD_ID", "TWIST"]).dir.apply(
    lambda s: (s == "Z").mean()).reset_index(name="pZ")
cg = cg[cg.TWIST.isin(["S", "Z"])]
# medias por quipu y torsion (solo quipus con ambas)
pv = cg.pivot_table(index="KHIPU_ID", columns="TWIST", values="pZ", aggfunc="mean")
pv = pv.dropna()
dif = (pv["Z"] - pv["S"])
# nulo: signo de la diferencia (permutar torsion dentro de quipu no cambia la media global;
# usamos test de signos, equivalente a permutacion dentro de quipu)
from scipy import stats
A(f"cuerdas con torsion S/Z y >=1 nudo orientado: {len(cg)}; quipus con ambas: {len(pv)}")
A(f"pZ medio en cuerdas S: {pv['S'].mean():.3f}; en cuerdas Z: {pv['Z'].mean():.3f}; "
  f"dif media={dif.mean():.3f}; Wilcoxon p={stats.wilcoxon(dif).pvalue:.4f}")
# y a nivel de nudo, diferencia ponderada
nn = kk[kk.dir.isin(["S", "Z"])]
A("pZ global en cuerdas S: %.3f (n=%d); en cuerdas Z: %.3f (n=%d)" % (
    (nn[nn.TWIST == "S"].dir == "Z").mean(), (nn.TWIST == "S").sum(),
    (nn[nn.TWIST == "Z"].dir == "Z").mean(), (nn.TWIST == "Z").sum()))

# test de archivo restringido a cuerdas de torsion S
ks = kk[(kk.TWIST == "S") & kk.dir.isin(["S", "Z"])]
pp = ks.groupby("KHIPU_ID").dir.apply(lambda s: (s == "Z").mean()).reset_index(name="pZ_S_twist")
nnn = ks.groupby("KHIPU_ID").size().reset_index(name="n")
pp = pp.merge(nnn, on="KHIPU_ID")
pp = pp.merge(ok[["KHIPU_ID", "arch", "OKR_NUM"]], on="KHIPU_ID", how="left")
pp["arch"] = pp.arch.fillna("Otros/vago")
pp = pp[pp.n >= 10]
e, p = perm_global(pp.pZ_S_twist.values, pp.arch.values)
A(f"ARCHIVO con solo cuerdas de torsion S (OKR, n>={len(pp)} quipus): eta2={e:.3f}, p={p:.4f}")

# ------------------------------------------------------------------ fibra
A("")
A("=== CONTROL: FIBRA (OKR) ===")
cord2 = pd.read_sql("select KHIPU_ID, CORD_ID, FIBER from cord", con)
kf = knot.merge(cord2, on="CORD_ID")
kf["dir"] = kf.DIRECTION.fillna("U")
kf.loc[~kf.dir.isin(["S", "Z"]), "dir"] = "U"
kf = kf[kf.dir.isin(["S", "Z"])]
fib = kf.groupby("FIBER").dir.apply(lambda s: (s == "Z").mean())
fibn = kf.groupby("FIBER").size()
A("pZ por fibra (nudos): " + ", ".join(f"{i}: {fib[i]:.3f} (n={fibn[i]})"
                                        for i in ["CN", "CL", "W", "H"] if i in fib.index))
# test de fibra a nivel cuerda, nulo dentro de quipu
cf = kf.groupby(["KHIPU_ID", "CORD_ID", "FIBER"]).dir.apply(lambda s: (s == "Z").mean()).reset_index(name="pZ")
cf = cf[cf.FIBER.isin(["CN", "CL"])]
pvf = cf.pivot_table(index="KHIPU_ID", columns="FIBER", values="pZ", aggfunc="mean").dropna()
A(f"quipus con cuerdas CN y CL: {len(pvf)}; pZ medio CN={pvf['CN'].mean():.3f}, "
  f"CL={pvf['CL'].mean():.3f}; dif={ (pvf['CL']-pvf['CN']).mean():.3f}; "
  f"Wilcoxon p={stats.wilcoxon(pvf['CL']-pvf['CN']).pvalue:.4f}")
# archivo restringido a algodon
kc = kf[kf.FIBER == "CN"]
pc = kc.groupby("KHIPU_ID").dir.apply(lambda s: (s == "Z").mean()).reset_index(name="pZ_CN")
nc = kc.groupby("KHIPU_ID").size().reset_index(name="n")
pc = pc.merge(nc, on="KHIPU_ID").merge(ok[["KHIPU_ID", "arch"]], on="KHIPU_ID", how="left")
pc["arch"] = pc.arch.fillna("Otros/vago")
pc = pc[pc.n >= 10]
e, p = perm_global(pc.pZ_CN.values, pc.arch.values)
A(f"ARCHIVO con solo nudos en cuerdas de algodon (n={len(pc)} quipus): eta2={e:.3f}, p={p:.4f}")

with open(OUT + r"\salida_02.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
