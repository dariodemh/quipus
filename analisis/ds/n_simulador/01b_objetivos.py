# -*- coding: utf-8 -*-
"""Objetivos finos: perfil de diferencias, nulos de cercania, doble via y copias.

Lee datos_reales.json (producido por 01_datos.py) y componentes_filas.csv.
"""
import json
import re
import numpy as np
import pandas as pd

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_simulador"
rng = np.random.default_rng(20261018)

D = json.load(open(OUT + r"\datos_reales.json", encoding="utf-8"))
cab = D["cabeceras"]
comp = pd.read_csv(RAIZ + r"\analisis\13_sistema_incahuasi\componentes_filas.csv")
ab = comp[comp.fuente == "UR273A+UR273B"].copy().reset_index(drop=True)

# ---- destino elegido por 13 (campo en_resumen) y perfil de diferencias ----
filas = []
for _, r in ab.iterrows():
    s = r.parte_A + r.parte_B
    txt = str(r.en_resumen) if pd.notna(r.en_resumen) else ""
    pares = re.findall(r"(UR\d+):g(\d+):(\d+)(~?)", txt)
    if pares:
        # preferir coincidencia exacta; si no, la primera
        exact = [p for p in pares if p[3] == ""]
        q, gr, val, tol = (exact[0] if exact else pares[0])
        dif = s - int(val)
    else:
        q, gr, val, dif = "", -1, np.nan, np.nan
    filas.append(dict(reg=int(r.registro), A=r.parte_A, B=r.parte_B, suma=s,
                      destino=f"{q}:g{gr}" if q else "", val=int(val) if q else np.nan,
                      dif=dif, absdif=abs(dif) if q else np.nan))
P = pd.DataFrame(filas)
P.to_csv(OUT + r"\perfil_ab.csv", index=False)
print("== PERFIL A+B (destino de 13) ==")
print(P.to_string(index=False))
obs = P.absdif.dropna().values
print("exactas", (obs == 0).sum(), "<=1", (obs <= 1).sum(), "<=10", (obs <= 10).sum(),
      "<=100", (obs <= 100).sum(), "<=1000", (obs <= 1000).sum(), "sin destino", P.destino.eq("").sum())
pot = [10 ** k for k in range(0, 5)]
print("fallos que son 10^k:", sorted([int(x) for x in obs if x > 0 and int(x) in pot]))

# ---- nulo: diferencia minima contra el pool de cabeceras ----
pool = np.array([x["valor"] for q in cab for x in cab[q]])
print("\npool cabeceras n=", len(pool))
def perfil_nulo(n=20000):
    out = []
    for _ in range(n):
        s = rng.integers(200, 4500)
        out.append(np.min(np.abs(pool - s)))
    return np.array(out)
nul = perfil_nulo()
print("nulo distancia minima: mediana", np.median(nul), "p25", np.percentile(nul, 25),
      "P(<=10)", (nul <= 10).mean(), "P(<=1)", (nul <= 1).mean(),
      "P(exacto)", (nul == 0).mean(), "P(10^k exacto y >0)",
      np.mean([x > 0 and int(x) in pot for x in nul]))
print("obs: <=10", (obs <= 10).sum(), "/", len(obs), " (nulo esperado",
      round((nul <= 10).mean() * len(obs), 2), ")")
print("obs: 10^k exacto y >0", sum(1 for x in obs if x > 0 and int(x) in pot), "/", len(obs),
      " (nulo esperado", round(np.mean([x > 0 and int(x) in pot for x in nul]) * len(obs), 2), ")")

# ---- CV de las MEDIAS de columna (el 0,18 de n_que_se_contaba) ----
c = pd.read_csv(RAIZ + r"\analisis\datos\cuerdas.csv",
                usecols=["kfg", "orden", "nivel", "grupo", "valor", "nudos"], dtype={"nudos": str})
c["tiene"] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != "")
c["v"] = np.where(c.tiene, pd.to_numeric(c.valor, errors="coerce"), np.nan)

def matriz(kfg, j=9):
    d = c[(c.kfg == kfg) & (c.nivel == 0)].sort_values("orden")
    rows = []
    for gr, gg in d.groupby("grupo", sort=True):
        vv = list(gg.v)
        if len(vv) >= j and np.sum(~np.isnan(vv)) >= j:
            rows.append(vv[:j])
    return np.array(rows, float)

M = matriz("UR278")
medias = np.nanmean(M, axis=0)
print("\n== UR278 ==", M.shape)
print("medias por columna", medias.round(0).astype(int))
print("CV de las 9 medias de columna =", round(float(np.std(medias) / np.mean(medias)), 3))
print("CV dentro de fila (mediana) =", round(float(np.median(np.nanstd(M, axis=1) / np.nanmean(M, axis=1))), 3))
print("correlacion media entre columnas =", round(float(np.mean(np.corrcoef(M, rowvar=False)[np.triu_indices(9, 1)])), 3))
# CV por fila entre columnas: ya calculado; tambien dispersion de los totales de fila
tot = np.nansum(M, axis=1)
print("total de fila: mediana", int(np.median(tot)), "CV", round(float(np.std(tot) / np.mean(tot)), 3))

# ---- UR270 columnas P y S ----
ur = pd.read_csv(RAIZ + r"\analisis\13_sistema_incahuasi\ur270_ur278.csv")
PM = np.array([(list(map(float, str(s).split())) + [np.nan] * 9)[:9] for s in ur.P], float)
SM = np.array([(list(map(float, str(s).split())) + [np.nan] * 9)[:9] for s in ur.S1], float)
print("\n== UR270 (12 grupos) ==")
print("medias P", np.nanmean(PM, 0).round(1), "CV medias", round(float(np.nanstd(np.nanmean(PM, 0)) / np.nanmean(PM)), 3))
print("medias S", np.nanmean(SM, 0).round(1), "CV medias", round(float(np.nanstd(np.nanmean(SM, 0)) / np.nanmean(SM)), 3))
print("cuota A/(A+B) por grupo", np.round(np.nansum(PM, 1) / (np.nansum(PM, 1) + np.nansum(SM, 1)), 3))
print("CV dentro de fila P", round(float(np.nanmedian(np.nanstd(PM, 1) / np.nanmean(PM, 1))), 3))

# ---- UR270->UR278: cuantos aciertos y ajuste binomial vs mezcla ----
ac = np.array([9, 9, 7, 8, 6, 5, 1, 2, 1, 1, 1, 1])
from scipy import stats
print("\n== UR270->UR278 aciertos ==", ac.tolist())
k = ac.sum(); n = 9 * len(ac)
# MLE binomial
ph = k / n
ll = stats.binom.logpmf(ac, 9, ph).sum()
print("MLE binomial p(match)=", round(ph, 3), "logL=", round(ll, 2))
# mezcla: fraccion f de filas emparejadas de verdad (aciertos ~ Bin(9,1-e)) + resto azar (p0)
p0 = float(np.mean([np.mean([abs(PM[i, j] + SM[i, j] - t) <= 1 for j in range(9)]) for i in range(len(PM)) for t in [0]]))  # no usable
print("P(>=6 aciertos) bajo binomial:", round(stats.binom.sf(5, 9, ph) * 12, 2),
      "filas observadas >=6:", int((ac >= 6).sum()))
print("P(<=2) bajo binomial:", round(stats.binom.cdf(2, 9, ph) * 12, 2),
      "filas observadas <=2:", int((ac <= 2).sum()))

# ---- doble libro: UR266 y UR275 por separado, y si coinciden entre si ----
print("\n== registro: suma | UR266 mas cercano | UR275 mas cercano | libros coinciden? ==")
v266 = np.array([x["valor"] for x in cab["UR266"]])
v275 = np.array([x["valor"] for x in cab["UR275"]])
doble = []
for _, r in P.iterrows():
    a = v266[np.argmin(np.abs(v266 - r.suma))]
    b = v275[np.argmin(np.abs(v275 - r.suma))]
    doble.append((int(r.reg), int(r.suma), int(a), int(b), abs(a - b) == 0,
                  int(min(abs(a - r.suma), abs(b - r.suma)))))
    print(f"reg {int(r.reg):2d}  {int(r.suma):5d} | {int(a):5d} | {int(b):5d} | "
          f"{'SI' if abs(a-b)==0 else 'no':3s} | dif minima {int(min(abs(a-r.suma),abs(b-r.suma)))}")
pd.DataFrame(doble, columns=["reg", "suma", "ur266", "ur275", "libros_iguales", "dif_min"]).to_csv(
    OUT + r"\doble_libro.csv", index=False)
db = pd.DataFrame(doble, columns=["reg", "suma", "ur266", "ur275", "iguales", "dif_min"])
print("libros coinciden entre si en", int(db.iguales.sum()), "/", len(db), "registros")
print("y en esos, dif con A+B:", sorted(db[db.iguales].dif_min.tolist()))

# ---- copias: coincidencia UR266 vs UR275 en los registros con fallo decimal ----
print("\n== libro consolidado: cabeceras por grupo ==")
for q in cab:
    print(q, [(x["grupo"], int(x["valor"])) for x in cab[q]][:6], "...",
          len(cab[q]), "grupos")
