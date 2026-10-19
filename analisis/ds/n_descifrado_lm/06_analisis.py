# -*- coding: utf-8 -*-
"""Consolida resultados, corrige por comparaciones multiples (BH-FDR) y arma
las tablas del informe."""
import os, sys, numpy as np, pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.minimum(q, 1.0)

r = pd.read_csv(os.path.join(BASE, "resultados.csv"))
l = pd.read_csv(os.path.join(BASE, "langstats.csv"))
t = r.merge(l[["quipu", "alfabeto", "H_cond", "H_cond_pc", "z_H_shuffle", "pct_H_pc", "zipf", "rep"]],
            on=["quipu", "alfabeto"], how="left")

# secuencias unicas (A1/A2/A3 suelen ser la misma particion)
t["clave"] = (t.quipu.astype(str) + "|" + t.n.astype(str) + "|" + t.n_signos.astype(str)
              + "|" + t.logL_obs.round(4).astype(str))
t["unica"] = ~t.clave.duplicated()

t["q_barajado"] = bh(t.p_vs_barajado)
t["q_calibrado"] = bh(t.p_calibrado)
t["q_barajado_uniq"] = np.nan
t.loc[t.unica, "q_barajado_uniq"] = bh(t.loc[t.unica, "p_vs_barajado"])

# dos lados de la calibracion
t["lado"] = np.where(t.p_calibrado < 0.05, "arriba (mas rigido que lengua)",
            np.where(t.p_calibrado > 0.95, "abajo (menos estructura que lengua)", "dentro"))
t["alcanza_silabario"] = t.n_signos >= 40

t.to_csv(os.path.join(BASE, "resultados_consolidados.csv"), index=False)

print("== por alfabeto (medias) ==")
print(t.groupby("alfabeto").agg(n=("n", "count"), V_med=("n_signos", "median"),
      V_max=("n_signos", "max"), logL=("logL_obs", "mean"),
      null=("logL_null_mean", "mean"), pc=("logL_pc_mean", "mean"),
      H=("H_cond", "mean"), Hpc=("H_cond_pc", "mean")).round(2).to_string())

print("\n== calibracion ==")
print(t.groupby(["lado"]).size().to_string())
print("\nV>=40:", int(t.alcanza_silabario.sum()), "de", len(t))
print("p_barajado<0.05:", int((t.p_vs_barajado < 0.05).sum()),
      " q<0.05:", int((t.q_barajado < 0.05).sum()),
      " unicas q<0.05:", int((t.q_barajado_uniq < 0.05).sum()), "de", int(t.unica.sum()))

print("\n== mejores por calibracion (V>=10, dentro) ==")
sub = t[(t.n_signos >= 10)].sort_values("p_calibrado", ascending=False)
print(sub[["quipu", "alfabeto", "n", "n_signos", "logL_obs", "logL_pc_mean",
           "p_vs_barajado", "p_calibrado", "H_cond", "H_cond_pc", "pct_H_pc"]].head(12).round(2).to_string(index=False))

print("\n== candidatos: resumen ==")
cand = ["UR179", "UR180", "UR178", "UR050", "UR054", "UR052", "AS076", "JC012", "UR203", "UR215"]
print(t[t.quipu.isin(cand)].groupby("quipu").agg(
    V_med=("n_signos", "median"), V_max=("n_signos", "max"),
    pmin=("p_vs_barajado", "min"), pcal_min=("p_calibrado", "min"),
    pcal_max=("p_calibrado", "max"), H=("H_cond", "mean"),
    Hpc=("H_cond_pc", "mean"), pctH=("pct_H_pc", "mean")).round(2).to_string())
