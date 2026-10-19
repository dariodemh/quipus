# -*- coding: utf-8 -*-
"""Contrastes cuantitativos de afirmaciones de la literatura (lit_2), v2.
A) descriptivos del corpus vs cifras publicadas (Curatola/Urton 2013; Cherkinsky 2014)
B) UR019 y el 'pi' de Saez-Rodriguez (2014)
C) UR1104 (=VA42527) y Saez-Rodriguez (2013)
D) direccion de nudo S/Z (Hyland et al. 2014)
E) pares 'similares' de Incahuasi (Urton & Chu 2015)
Semilla fija; se guarda resultados.json
"""
import pandas as pd, numpy as np, re, json, itertools
from scipy import stats

D = r"./analisis/datos"
rng = np.random.default_rng(20261017)
c = pd.read_csv(D + r"\cuerdas.csv", low_memory=False)
q = pd.read_csv(D + r"\quipus.csv", low_memory=False)
c["tiene_nudos"] = c["nudos"].notna() & (c["nudos"].astype(str).str.strip() != "")
c["val"] = np.where(c["tiene_nudos"], c["valor"], np.nan)
out = {}

# ============ A. Descriptivos ============
per = c.groupby("kfg").agg(n_cuerdas=("cuerda", "size"))
per["n_pend"] = c[c.nivel == 0].groupby("kfg").size()
subs = c[c.nivel > 0]
padres_con_sub = subs.groupby("kfg")["padre"].nunique()
per["pend_con_sub"] = padres_con_sub.reindex(per.index).fillna(0)
maxniv = c.groupby("kfg").nivel.max()
prom_pend = per.n_pend.mean()

out["A"] = dict(
    n_quipus=int(c.kfg.nunique()),
    media_cuerdas=round(per.n_cuerdas.mean(), 1), mediana_cuerdas=float(per.n_cuerdas.median()),
    media_pend=round(per.n_pend.mean(), 1), mediana_pend=float(per.n_pend.median()),
    pct_cuerdas_subs=round(100 * (c.nivel > 0).mean(), 1),
    pct_pend_con_sub=round(100 * per.pend_con_sub.sum() / per.n_pend.sum(), 1),
    pct_quipus_con_sub=round(100 * (per.pend_con_sub > 0).mean(), 1),
    max_nivel=int(maxniv.max()), n_nivel_ge6=int((maxniv >= 6).sum()),
    n_nivel_ge5=int((maxniv >= 5).sum()), max_pend=int(per.n_pend.max()),
)
codes = set()
for s in c.color.dropna().astype(str):
    for pp in re.split(r"[:/\-]", s):
        pp = pp.strip()
        if pp and re.fullmatch(r"[A-Z]{1,3}\d?", pp):
            codes.add(pp)
out["A"]["n_codigos_color"] = len(codes)
print("=== A. Descriptivos (n=%d quipus) ===" % out["A"]["n_quipus"])
for k, v in out["A"].items():
    print(f"  {k}: {v}")

# ============ B. UR019 ============
u = c[c.kfg == "UR019"].sort_values("orden")
tot = u.val.sum(); pend = u[u.nivel == 0]; sub = u[u.nivel > 0]
print("\n=== B. UR019 (Saez-Rodriguez 2014) ===")
print(f"  pendientes={len(pend)} subsidiarias={len(sub)} | pc_largo={q.loc[q.kfg=='UR019','pc_largo'].iloc[0]} cm")
print(f"  suma valores={tot} | suma pendientes={pend.val.sum()} | total/13={tot/13:.3f} | pend/13={pend.val.sum()/13:.2f}")
dirs = [d for s in u.nudos for _, d in re.findall(r"\(([\d.]+),([SZU])\)", str(s))]
sumS = sum(v for s, v in zip(u.nudos, u.val) if isinstance(s, str) and ",S)" in s and ",Z)" not in s)
sumZ = sum(v for s, v in zip(u.nudos, u.val) if isinstance(s, str) and ",Z)" in s and ",S)" not in s)
print("  nudos por direccion:", {x: dirs.count(x) for x in set(dirs)}, f"| suma solo-S={sumS} solo-Z={sumZ}")
ratio = (c.groupby("kfg").val.sum() / per.n_pend).dropna()
print("  control: quipus con total/n_pend dentro de +-0.01 de constantes:")
for const in [np.pi, 2 * np.pi, np.e, (1 + 5 ** .5) / 2, 3.0, 6.0, 9.0, 12.0]:
    print(f"    {const:.4f}: {int((abs(ratio - const) < .01).sum())}")
print("  rango ratio p5-p95:", round(float(np.percentile(ratio, 5)), 2), "-", round(float(np.percentile(ratio, 95)), 2))
out["B"] = dict(n_pend=int(len(pend)), n_sub=int(len(sub)), suma=float(tot),
                suma_pend=float(pend.val.sum()), ratio=round(tot / 13, 3),
                dirs={x: dirs.count(x) for x in set(dirs)}, sumS=float(sumS), sumZ=float(sumZ),
                n_pi=int((abs(ratio - np.pi) < .01).sum()), n_validos=int(len(ratio)),
                p5=float(np.percentile(ratio, 5)), p95=float(np.percentile(ratio, 95)))

# ============ C. UR1104 = VA42527 ============
v = c[c.kfg == "UR1104"].sort_values("orden")
print("\n=== C. UR1104 (=VA42527) (Saez-Rodriguez 2013) ===")
print(f"  cuerdas={len(v)} pendientes={(v.nivel==0).sum()} subsidiarias={(v.nivel>0).sum()} (afirma 21, 0)")
s4 = v.val.iloc[14:18] / 10
print(f"  cuerdas 15-18 (/10)={[round(x,1) for x in s4.tolist()]} suma={s4.sum():.1f}")
print(f"  315+140+217+209={881}; 881/29.5={881/29.5:.3f} -> no es multiplo entero")
out["C"] = dict(n=int(len(v)), suma_15_18=round(float(s4.sum()), 1), div29_5=round(881 / 29.5, 3))

# ============ D. Direccion de nudo ============
def cord_dir(s):
    ds = [d for _, d in re.findall(r"\(([\d.]+),([SZU])\)", str(s)) if d in ("S", "Z")]
    if not ds: return None
    return ds[0] if len(set(ds)) == 1 else "M"

c["cdir"] = c.nudos.apply(cord_dir)
pend = c[(c.nivel == 0) & c.cdir.isin(["S", "Z"])]
ok = pend.groupby("kfg").filter(lambda d: len(d) >= 6 and d.cdir.nunique() == 2)
print(f"\n=== D. Direccion S/Z (Hyland 2014): {ok.kfg.nunique()} quipus con >=6 pendientes y ambas clases ===")
data = []
for k, d in ok.groupby("kfg"):
    d = d.sort_values("orden")
    x = (d.cdir.values == "S").astype(float)
    _, gi = np.unique(d.grupo.values, return_inverse=True)
    data.append((x, gi, gi.max() + 1, np.arange(1, len(x) + 1)))

def st(x, gi, ng, r):
    runs_ = 1 + int(np.sum(x[1:] != x[:-1]))
    rk = abs(r[x == 1].mean() - (len(x) + 1) / 2) if x.sum() else 0.0
    s_g = np.bincount(gi, weights=x, minlength=ng); n_g = np.bincount(gi, minlength=ng)
    pbar = x.mean()
    return runs_, rk, float(np.sum(n_g * (s_g / n_g - pbar) ** 2))

obs = np.array([st(*d) for d in data]).sum(axis=0)
B = 4000
null = np.zeros((B, 3))
for b in range(B):
    acc = np.zeros(3)
    for x, gi, ng, r in data:
        acc += st(rng.permutation(x), gi, ng, r)
    null[b] = acc
p = [(np.sum(null[:, 0] <= obs[0]) + 1) / (B + 1),      # runs: menos runs = agrupamiento
     (np.sum(null[:, 1] >= obs[1]) + 1) / (B + 1),
     (np.sum(null[:, 2] >= obs[2]) + 1) / (B + 1)]
print(f"  runs obs={obs[0]:.0f} nulo={null[:,0].mean():.0f} p={p[0]:.4f}")
print(f"  |rango S - centro| obs={obs[1]:.0f} p={p[1]:.4f}")
print(f"  heterogeneidad entre grupos obs={obs[2]:.1f} p={p[2]:.4f}")
mixed = lastZ = 0
for s in c.nudos.dropna():
    ds = [d for _, d in re.findall(r"\(([\d.]+),([SZU])\)", str(s)) if d in ("S", "Z")]
    if len(ds) >= 2:
        mixed += 1; lastZ += ds[-1] == "Z"
print(f"  cuerdas con >=2 racimos: {mixed}; ultimo racimo Z: {lastZ} ({100*lastZ/mixed:.1f}%)")
# control: direccion del primer vs ultimo racimo
print("  cuerdas por clase:", pend.cdir.value_counts().to_dict())
out["D"] = dict(n_quipus=int(ok.kfg.nunique()), runs=float(obs[0]), runs_null=float(null[:, 0].mean()),
                p_runs=float(p[0]), p_rank=float(p[1]), p_grp=float(p[2]),
                mixed=int(mixed), lastZ_pct=round(100 * lastZ / mixed, 1),
                clases={k: int(v) for k, v in pend.cdir.value_counts().items()})

# ============ E. Pares de Incahuasi ============
inc = set(q[q.procedencia == "Incahuasi"].kfg)
p0 = c[c.nivel == 0]
V = {}
for k, d in p0.groupby("kfg"):
    V[k] = d.sort_values("orden").val.values
bylen = {}
for k, vv in V.items():
    if len(vv) >= 6:
        bylen.setdefault(len(vv), []).append(k)

def pair_r(a, b):
    x, y = V[a], V[b]
    m = ~np.isnan(x) & ~np.isnan(y)
    if m.sum() < 5: return np.nan
    if x[m].std() == 0 or y[m].std() == 0: return np.nan
    return np.corrcoef(x[m], y[m])[0, 1]

obs_pairs = []
for n, ks in bylen.items():
    for a, b in itertools.combinations(ks, 2):
        r = pair_r(a, b)
        if not np.isnan(r):
            obs_pairs.append((r, a, b, n))
OP = pd.DataFrame(obs_pairs, columns=["r", "a", "b", "n"])
OP["inc"] = OP.a.isin(inc) & OP.b.isin(inc)
print("\n=== E. Pares 'similares' (Urton & Chu 2015) ===")
print(f"  pares comparables (misma n_pend, >=5 cuerdas con valor comun): {len(OP)}")
print(f"  r mediana={OP.r.median():.3f}; r>=0.9: {(OP.r>=.9).sum()} pares; de ellos Incahuasi: {OP[OP.r>=.9].inc.sum()}")
print("  top pares del corpus:")
print(OP.sort_values("r", ascending=False).head(6).to_string(index=False))
top_inc = OP[OP.inc].sort_values("r", ascending=False).head(4)
print("  top pares Incahuasi:")
print(top_inc.to_string(index=False))
obs_max = float(OP[OP.inc].r.max())
# nulo: reasignar vectores al azar dentro de cada estrato de longitud
B2 = 2000
null_max = np.empty(B2)
for b in range(B2):
    newV = {}
    for n, ks in bylen.items():
        perm = rng.permutation(ks)
        for k, src in zip(ks, perm):
            newV[k] = V[src]
    Vsave = V
    V = newV
    mx = -1
    for n, ks in bylen.items():
        incks = [k for k in ks if k in inc]
        for a, bb in itertools.combinations(incks, 2):
            r = pair_r(a, bb)
            if not np.isnan(r): mx = max(mx, r)
    V = Vsave
    null_max[b] = mx
pE = (np.sum(null_max >= obs_max) + 1) / (B2 + 1)
print(f"  max r Incahuasi={obs_max:.3f}; nulo max r media={null_max.mean():.3f}, p={pE:.4f}")
out["E"] = dict(n_pares=int(len(OP)), mediana=round(float(OP.r.median()), 3),
                n_r90=int((OP.r >= .9).sum()), n_r90_inc=int(OP[OP.r >= .9].inc.sum()),
                max_inc=obs_max, null_max_mean=round(float(null_max.mean()), 3), p=float(pE),
                top=[(round(x.r, 3), x.a, x.b, int(x.n)) for x in OP.sort_values("r", ascending=False).head(5).itertuples()])

json.dump(out, open("resultados.json", "w"), indent=1)
print("\nOK -> resultados.json")
