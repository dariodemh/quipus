# -*- coding: utf-8 -*-
"""Validacion de las otras salidas del generador y predicciones ya comprobables.

- distribucion de valores (KS) por tipo de libro
- fraccion de cuerdas vacias (estructural vs rotura)
- tamanos de grupo
- estabilidad de las 9 cuotas relativas entre mitades de UR278
- la copia UR274A no arregla los fallos (negativo)
- nº de racimos y probabilidad de fallo (prediccion 4, potencia limitada)
"""
import json
import numpy as np
import pandas as pd
from scipy import stats
import importlib.util

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_simulador"
spec = importlib.util.spec_from_file_location("sim", OUT + r"\02_simulador.py")
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)
rng = np.random.default_rng(4242)

c = pd.read_csv(RAIZ + r"\analisis\datos\cuerdas.csv",
                usecols=["kfg", "orden", "nivel", "grupo", "valor", "nudos", "notas"],
                dtype={"nudos": str, "notas": str})
c["tiene"] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != "")
c["v"] = np.where(c.tiene, pd.to_numeric(c.valor, errors="coerce"), np.nan)
c["nrac"] = c.nudos.fillna("").apply(lambda s: len([x for x in str(s).split(";") if x.strip()]))

mejor = dict(sim.PARAMS, q_rac=0.061, s_blank=0.0, q_trans=0.0022)
U, C, A, B = sim.simular_valores(20000, mejor)

print("== 1. distribucion de valores (KS) ==")
def ks(real, simv, nombre):
    real = np.asarray(real, float); real = real[np.isfinite(real) & (real > 0)]
    simv = np.asarray(simv, float); simv = simv[np.isfinite(simv) & (simv > 0)]
    d, p = stats.ks_2samp(real, simv)
    print(f"  {nombre:28s} real med {np.median(real):7.0f}  sim med {np.median(simv):7.0f}"
          f"  D={d:.3f} p={p:.3f}")
    return d, p
det = c[(c.kfg == "UR278") & (c.nivel == 0)].v.dropna()
ks(det, U, "UR278 celda (detalle)")
ks(c[(c.kfg == "UR273A")].v.dropna(), A, "UR273A parte A")
ks(c[(c.kfg == "UR273B")].v.dropna(), B, "UR273B parte B")
cab = []
for q in ["UR266", "UR269", "UR275"]:
    d = c[(c.kfg == q) & (c.nivel == 0) & c.v.notna()].sort_values("orden")
    cab += [gg.sort_values("orden").iloc[0].v for _, gg in d.groupby("grupo")]
ks(cab, C, "cabeceras de libro")

print("\n== 2. cuerdas vacias ==")
frac = 1 - c.tiene.mean()
rotas = c.notas.fillna("").str.contains("broken|missing|fragment|roto|falta", case=False).mean()
print(f"  corpus: {frac:.3f} vacias; notas de rotura {rotas:.3f}; razon {frac/rotas:.0f}x")
for q in ["UR266", "UR269", "UR270", "UR273A", "UR273B", "UR275", "UR278"]:
    d = c[c.kfg == q]
    print(f"  {q:7s} vacias {1-d.tiene.mean():.2f}  (n={len(d)})")
# el generador: tasa de vacias por rol, mezcla de libros observada
pesos = {"componente": len(c[c.kfg.isin(["UR273A","UR273B"])]),
         "libro": len(c[c.kfg.isin(["UR266","UR269","UR275"])]),
         "detalle": len(c[c.kfg == "UR270"]), "tabla": len(c[c.kfg == "UR278"])}
tasas = {"componente": 0.735, "libro": 0.27, "detalle": 0.22, "tabla": 0.09}
tot = sum(pesos.values())
pred = sum(pesos[k] * tasas[k] for k in pesos) / tot
print(f"  generador (pesos reales {pesos}): vacias {pred:.3f}; corpus {frac:.3f}")
print("  => las vacias NO son roturas: 30,5 % vs 0,56 % (54x). Son estructurales.")

print("\n== 3. tamanos de grupo ==")
g = c[c.nivel == 0].groupby(["kfg", "grupo"]).size()
gi = g[g.index.get_level_values(0).isin(
    ["UR266", "UR269", "UR270", "UR273A", "UR275", "UR278"])]
pois = 1 + rng.poisson(gi.mean() - 1, 20000)
print(f"  Incahuasi: mediana {gi.median():.0f}, media {gi.mean():.2f}, "
      f"p75 {gi.quantile(.75):.0f}, max {gi.max()}")
print(f"  generador Poisson(media-1)+1: mediana {np.median(pois):.0f}, "
      f"media {pois.mean():.2f}, p75 {np.percentile(pois,75):.0f}")
print(f"  KS p = {stats.ks_2samp(gi.values, pois).pvalue:.3f} (calibrado, no predicho)")

print("\n== 4. estabilidad de las 9 cuotas relativas (UR278) ==")
d = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values("orden")
rows = []
for gr, gg in d.groupby("grupo", sort=True):
    vv = list(gg.v)
    if len(vv) >= 9 and np.sum(~np.isnan(vv)) >= 9:
        rows.append(vv[:9])
M = np.array(rows, float)
h = len(M) // 2
sh = M / np.nansum(M, axis=1, keepdims=True)
s1, s2 = np.nanmean(sh[:h], 0), np.nanmean(sh[h:], 0)
print(f"  cuotas relativas 1ª mitad: {np.round(s1,3)}")
print(f"  cuotas relativas 2ª mitad: {np.round(s2,3)}")
print(f"  Spearman entre mitades: {stats.spearmanr(s1,s2).statistic:.3f} (niveles daban 0.467)")
print(f"  CV de las 9 medias de columna: {np.std(np.nanmean(M,0))/np.mean(np.nanmean(M,0)):.3f}")

print("\n== 5. la copia UR274A no arregla los fallos (negativo) ==")
comp = pd.read_csv(RAIZ + r"\analisis\13_sistema_incahuasi\componentes_filas.csv")
pool = np.array([x["valor"] for q in json.load(open(OUT + r"\datos_reales.json"))["cabeceras"]
                 for x in json.load(open(OUT + r"\datos_reales.json"))["cabeceras"][q]])
for fuente in ["UR273A+UR273B", "UR274A+UR273B", "UR274A+UR274B"]:
    dd = comp[comp.fuente == fuente]
    n = 0
    for _, r in dd.iterrows():
        s = r.parte_A + r.parte_B
        n += bool(np.any(pool == s))
    print(f"  {fuente:18s}: {n}/{len(dd)} sumas exactas")

print("\n== 6. fallo vs nº de racimos (prediccion 4) ==")
P = pd.read_csv(OUT + r"\perfil_ab.csv")
rac = []
for _, r in P.iterrows():
    tot = 0
    for val, q in [(r.A, "UR273A"), (r.B, "UR273B")]:
        dq = c[(c.kfg == q) & c.tiene & (np.abs(c.v - val) < 0.5)]
        tot += int(dq.nrac.iloc[0]) if len(dq) else 0
    rac.append(tot)
P["nrac_AB"] = rac
P["fallo"] = (P.absdif > 0) & P.absdif.notna()
print(f"  racimos A+B por registro: mediana {P.nrac_AB.median():.0f}, "
      f"rango {P.nrac_AB.min()}-{P.nrac_AB.max()}")
print(f"  fallo medio con <=6 racimos: {P[P.nrac_AB<=6].fallo.mean():.2f} "
      f"(n={len(P[P.nrac_AB<=6])})")
print(f"  fallo medio con >6 racimos:  {P[P.nrac_AB>6].fallo.mean():.2f} "
      f"(n={len(P[P.nrac_AB>6])})")
print(f"  Spearman nrac vs fallo: {stats.spearmanr(P.nrac_AB, P.fallo.astype(float)).statistic:.3f}"
      f" p={stats.spearmanr(P.nrac_AB, P.fallo.astype(float)).pvalue:.3f} (n=18, sin potencia)")
