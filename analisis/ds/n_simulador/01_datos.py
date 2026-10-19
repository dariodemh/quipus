# -*- coding: utf-8 -*-
"""Extrae los estadisticos REALES del archivo de Incahuasi que el simulador debe reproducir.

No modifica nada fuera de esta carpeta. Lee solo columnas necesarias de cuerdas.csv
(57 818 filas es grande pero se lee una vez con usecols y se filtra en memoria;
nunca se imprime entero).
"""
import json
import numpy as np
import pandas as pd

RAIZ = r"."
CSV = RAIZ + r"\analisis\datos\cuerdas.csv"
OUT = RAIZ + r"\analisis\ds\n_simulador"

INC = ["UR255", "UR256", "UR266", "UR267A", "UR267B", "UR268", "UR269",
       "UR270", "UR273A", "UR273B", "UR274A", "UR274B", "UR275", "UR278"]

c = pd.read_csv(CSV, usecols=["kfg", "orden", "cuerda", "nivel", "padre",
                              "grupo", "valor", "nudos", "color"],
                dtype={"nudos": str, "color": str})
c["tiene_nudos"] = c["nudos"].notna() & (c["nudos"].astype(str).str.strip() != "")
c["valor"] = pd.to_numeric(c["valor"], errors="coerce")
# valor 0 con nudos vacio = ausente, no cero
c["v"] = np.where(c["tiene_nudos"], c["valor"], np.nan)

res = {}

# ---------- 1. distribucion de valores y vacias ----------
def stats_quipu(df):
    v = df["v"].dropna()
    v = v[v > 0]
    return dict(n_cuerdas=len(df), n_con_nudos=int(df["tiene_nudos"].sum()),
                frac_vacias=float(1 - df["tiene_nudos"].mean()),
                n_val=len(v),
                med=float(np.median(v)) if len(v) else np.nan,
                p25=float(np.percentile(v, 25)) if len(v) else np.nan,
                p75=float(np.percentile(v, 75)) if len(v) else np.nan,
                p90=float(np.percentile(v, 90)) if len(v) else np.nan,
                max=float(v.max()) if len(v) else np.nan,
                frac_menor100=float((v < 100).mean()) if len(v) else np.nan,
                frac_mayor1000=float((v >= 1000).mean()) if len(v) else np.nan)

res["por_quipu"] = {k: stats_quipu(g) for k, g in c[c.kfg.isin(INC)].groupby("kfg")}
corp = c[c.v.notna() & (c.v > 0)]
res["corpus"] = dict(n_cuerdas=len(c), frac_vacias=float(1 - c["tiene_nudos"].mean()),
                     med=float(corp.v.median()), p25=float(corp.v.quantile(.25)),
                     p75=float(corp.v.quantile(.75)), p90=float(corp.v.quantile(.90)),
                     frac_menor100=float((corp.v < 100).mean()),
                     frac_mayor1000=float((corp.v >= 1000).mean()))

# ---------- 2. tamano de grupos ----------
g = c[c.nivel == 0].groupby(["kfg", "grupo"]).size()
res["grupos"] = dict(med=float(g.median()), media=float(g.mean()),
                     p25=float(g.quantile(.25)), p75=float(g.quantile(.75)),
                     n=len(g))
res["grupos_inc"] = dict(med=float(g[g.index.get_level_values(0).isin(INC)].median()),
                         media=float(g[g.index.get_level_values(0).isin(INC)].mean()),
                         n=len(g[g.index.get_level_values(0).isin(INC)]))

# ---------- 3. cabeceras de cada quipu (primer colgante anudado de cada grupo) ----------
def cabeceras(kfg):
    d = c[(c.kfg == kfg) & (c.nivel == 0) & c.v.notna()].sort_values("orden")
    out = []
    for gr, gg in d.groupby("grupo", sort=True):
        gg = gg.sort_values("orden")
        out.append(dict(grupo=int(gr), valor=float(gg.iloc[0]["v"]),
                        color=gg.iloc[0]["color"], orden=int(gg.iloc[0]["orden"]),
                        n=len(gg)))
    return out

cab = {k: cabeceras(k) for k in ["UR266", "UR269", "UR275"]}
for k, v in cab.items():
    res.setdefault("cabeceras", {})[k] = v

# ---------- 4. sumas A+B reales (alineacion de 13, tabla componentes_filas) ----------
comp = pd.read_csv(RAIZ + r"\analisis\13_sistema_incahuasi\componentes_filas.csv")
ab = comp[comp.fuente == "UR273A+UR273B"].copy()
destinos = []
for q in cab:
    destinos += [(q, x["grupo"], x["valor"]) for x in cab[q]]

filas = []
for _, r in ab.iterrows():
    s = float(r.parte_A) + float(r.parte_B)
    exactos = [(q, gr) for q, gr, v in destinos if v == s]
    # destino mas cercano
    mejor = min(destinos, key=lambda t: abs(t[2] - s))
    dif = s - mejor[2]
    filas.append(dict(registro=int(r.registro), A=float(r.parte_A), B=float(r.parte_B),
                      suma=s, exactos=str(exactos) if exactos else "",
                      mejor_destino=f"{mejor[0]}:g{mejor[1]}", mejor_valor=mejor[2],
                      dif=dif, dif_rel=dif / max(mejor[2], 1)))
ab_out = pd.DataFrame(filas)
ab_out.to_csv(OUT + r"\ab_reales.csv", index=False)
res["ab"] = dict(n=len(ab_out), exactas=int((ab_out.exactos != "").sum()),
                 frac_exactas=float((ab_out.exactos != "").mean()),
                 con_destino_cercano_1=int((ab_out.dif.abs() <= 1).sum()),
                 abs_dif=list(np.abs(ab_out.dif).round(0).astype(int)),
                 dif=list(ab_out.dif.round(0).astype(int)),
                 ratios=[round(a / (a + b), 3) for a, b in zip(ab_out.A, ab_out.B)])

# ---------- 5. UR270 -> UR278 ----------
ur = pd.read_csv(RAIZ + r"\analisis\13_sistema_incahuasi\ur270_ur278.csv")
cols = []
for _, r in ur.iterrows():
    P = [float(x) for x in str(r.P).split()]
    S = [float(x) for x in str(r.S1).split()]
    T = str(r.UR278).replace("·", " ").split()
    ok = 0
    difs = []
    for j in range(min(9, len(P), len(S), len(T))):
        t = float(T[j])
        difs.append(P[j] + S[j] - t)
        ok += abs(P[j] + S[j] - t) <= 1
    cols.append(dict(g270=int(r.grupo_UR270), f278=int(r.fila_UR278),
                     aciertos=int(r.aciertos), n_col=int(r.n_col),
                     recalc=ok, difs=difs))
res["ur270_ur278"] = cols

# CV de columnas de UR278 (solo cuerdas nivel 0, la fila es el grupo)
u278 = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values("orden")
tab = []
for gr, gg in u278.groupby("grupo", sort=True):
    vv = list(gg.sort_values("orden")["v"])
    if len(vv) >= 7 and sum(x for x in vv if not np.isnan(x)) > 0:
        tab.append(vv[:9])
arr = np.array([[np.nan if np.isnan(x) else x for x in row] +
                [np.nan] * (9 - len(row)) for row in tab], dtype=float)
cv_filas = np.nanstd(arr, axis=1) / np.nanmean(arr, axis=1)
cv_cols = np.nanstd(arr, axis=0) / np.nanmean(arr, axis=0)
res["ur278"] = dict(n_filas=len(arr), cv_filas_med=float(np.nanmedian(cv_filas)),
                    cv_columnas_med=float(np.nanmedian(cv_cols)),
                    cv_columnas=[round(float(x), 3) for x in cv_cols],
                    corr_media=float(np.nanmean(np.corrcoef(np.nan_to_num(arr, nan=np.nanmean(arr, 0)), rowvar=False)[np.triu_indices(9, 1)])))

with open(OUT + r"\datos_reales.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=float)

# ---------- salida corta ----------
print("== POR QUIPU ==")
for k in INC:
    d = res["por_quipu"][k]
    print(f"{k:7s} n={d['n_cuerdas']:4d} vacias={d['frac_vacias']:.2f} "
          f"med={d['med']:8.0f} p25={d['p25']:7.0f} p75={d['p75']:8.0f} "
          f"p90={d['p90']:8.0f} <100={d['frac_menor100']:.2f} >=1k={d['frac_mayor1000']:.2f}")
print("\n== A+B ==")
print(ab_out[["registro", "A", "B", "suma", "exactos", "mejor_destino", "mejor_valor", "dif"]].to_string(index=False))
print("exactas", res["ab"]["exactas"], "/", res["ab"]["n"], "=", res["ab"]["frac_exactas"],
      "| <=1:", res["ab"]["con_destino_cercano_1"])
print("\n== UR270->UR278 ==")
for x in cols:
    print(x["g270"], "->", x["f278"], "aciertos", x["recalc"], "/", x["n_col"], "difs", x["difs"])
print("\n== UR278 ==", res["ur278"])
print("== corpus ==", res["corpus"])
print("== grupos ==", res["grupos"], res["grupos_inc"])
