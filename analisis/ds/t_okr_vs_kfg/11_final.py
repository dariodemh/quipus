# -*- coding: utf-8 -*-
"""Cifras finales citables, con y sin los registros KFG mal vinculados."""
import os
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
SAL = os.path.join(OUT, "salidas")

MAL = {"KH0197", "KH0227", "KH0267", "KH0350"}   # metadatos okr erroneos (museo/nº cuerdas)
DUP = {"UR196", "MM007_AN002"}                   # cuerdas duplicadas dentro de KFG

j = pd.read_csv(os.path.join(SAL, "join_cuerdas.csv"))
j["prefijo"] = list(j.kfg.str.extract(r"^([A-Z]+)")[0])
j["tiene_kfg"] = j.nudos.notna()
j["disc"] = (~j.coincide) & j.tiene_kfg
j["largo_ok"] = j.dlargo <= 0.51

def resumen(df, etiqueta, excluir=True):
    x = df[~df.kfg.isin(MAL | DUP)] if excluir else df
    comp = x[x.tiene_kfg]
    val = comp[comp.largo_ok]
    disc_val = val[~val.coincide]
    print(f"\n### {etiqueta}")
    print(f"quipus: {x.kfg.nunique()} | cuerdas emparejadas: {len(x)}")
    print(f"cuerdas con nudos KFG: {len(comp)}")
    print(f"cuerdas comparables por valor (largo OK): {len(val)} | discrepancias: {len(disc_val)}"
          f" = {len(disc_val)/len(val)*100:.3f}%")
    print(f"cuerdas con nudos y largo distinto (>0.5 cm): {(~comp.largo_ok).sum()}"
          f" = {(~comp.largo_ok).mean()*100:.2f}%")
    print(f"KFG con nudos y OKR=0: {(comp.valor_okr==0).sum()}")
    print(f"KFG sin nudos y OKR>0: {((~x.tiene_kfg) & (x.valor_okr>0)).sum()}")
    t = x.groupby("prefijo").agg(quipus=("kfg", "nunique"),
                                 n_valor=("largo_ok", "sum"))
    vv = val.groupby("prefijo").agg(n=("coincide", "size"),
                                    d=("coincide", lambda s: (~s).sum()))
    vv["tasa%"] = (vv.d / vv.n * 100).round(3)
    print(vv.to_string())
    return x, comp, val

x, comp, val = resumen(j, "CON exclusiones")
resumen(j, "SIN exclusiones", excluir=False)

# concentracion
g = x[~x.kfg.isin(DUP)].groupby("kfg").apply(
    lambda d: pd.Series({"n": (d.tiene_kfg & d.largo_ok).sum(),
                         "d": ((~d.coincide) & d.tiene_kfg & d.largo_ok).sum()}), include_groups=False)
g = g[g.n > 0]
g["tasa"] = g.d / g.n
top = g.sort_values("d", ascending=False).head(5)
print("\ntop5 por discrepancias de valor:")
print(top.to_string())
print("top5 / total discrepancias:", int(top.d.sum()), "/", int(g.d.sum()),
      f"= {top.d.sum()/g.d.sum()*100:.1f}%")
print("quipus con >=1 discrepancia de valor:", (g.d > 0).sum(), "de", len(g))
print("quipus con tasa>5% y n>=5:", ((g.tasa > 0.05) & (g.n >= 5)).sum())

# tabla >5% (definicion pedida: discrepancias / cuerdas KFG con nudos)
h = pd.read_csv(os.path.join(SAL, "por_quipu.csv"), index_col=0)
h = h[~h.index.isin(MAL | DUP)]
lista = h[h.tasa > 0.05].copy()
lista["disc_valor"] = g.d.reindex(lista.index).fillna(0).astype(int)
lista["n_valor"] = g.n.reindex(lista.index).fillna(0).astype(int)
lista["tasa_valor"] = (lista.disc_valor / lista.n_valor.replace(0, np.nan)).round(3)
lista = lista.sort_values("tasa", ascending=False)
cols = ["prefijo", "n_con_nudos", "disc", "tasa", "disc_valor", "n_valor", "tasa_valor", "okr_solo"]
print("\n### lista >5% (definicion amplia: toda discrepancia / cuerdas con nudos)")
print(lista[cols].to_string())
lista.to_csv(os.path.join(SAL, "lista_mas_5pct.csv"))
