# -*- coding: utf-8 -*-
"""
05_color_union_pareado.py -- efecto de cada color / tipo de unión sobre "sin nudos",
comparando dentro de cada quipu (cuerdas K, nivel 0, L>0).
Evita z estratificados inestables en categorías raras.
"""
import os, importlib.util
import pandas as pd
import numpy as np

BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "t_cuerdas_vacias")
spec = importlib.util.spec_from_file_location("p02", os.path.join(OUT, "02_permutaciones.py"))
p02 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p02)

df = p02.load()
d0 = p02.add_position(df)
k = d0[(d0.terminacion == "K") & (d0.nivel == 0) & (d0.L > 0)].copy()

rows = []
print("== COLOR: cada categoría vs el resto, dentro de quipu ==", flush=True)
for col in ["AB", "W", "MB", "YB", "B", "KB", "DB", "RB", "GG", "LG", "LB", "PK", "BB", "HB", "CB", "NA"]:
    k["flag"] = k.pc == col
    if k.flag.sum() < 30:
        continue
    r = p02.perm_diff(k, "kfg", "sin", "flag", label=f"color:{col}")
    if r is None:
        continue
    s = k[k.flag]
    print(f"{col:3s} n={len(s):5d} vacías={100*s.sin.mean():5.1f}% | "
          f"w={100*r['obs_w']:+.2f}pp (p={r['p_w']:.4f}) eq={100*r['obs']:+.2f}pp (p={r['p']:.4f}) "
          f"pooled={100*r['obs_pool']:+.2f}pp (p={r['p_pool']:.4f}) | quipus={r['n_groups']}", flush=True)
    rows.append(dict(tipo="color", categoria=col, n=len(s), pct_vacias=100*s.sin.mean(),
                     efecto_w_pp=100*r['obs_w'], p_w=r['p_w'], efecto_eq_pp=100*r['obs'],
                     p_eq=r['p'], efecto_pool_pp=100*r['obs_pool'], p_pool=r['p_pool'],
                     n_quipus_contraste=r['n_groups']))

print("\n== UNIÓN: cada categoría vs el resto, dentro de quipu ==", flush=True)
for col in ["R", "V", "DESCONOCIDA"]:
    k["flag"] = k.un == col
    r = p02.perm_diff(k, "kfg", "sin", "flag", label=f"union:{col}")
    s = k[k.flag]
    print(f"{col:12s} n={len(s):5d} vacías={100*s.sin.mean():5.1f}% | "
          f"w={100*r['obs_w']:+.2f}pp (p={r['p_w']:.4f}) eq={100*r['obs']:+.2f}pp (p={r['p']:.4f}) "
          f"pooled={100*r['obs_pool']:+.2f}pp (p={r['p_pool']:.4f}) | quipus={r['n_groups']}", flush=True)
    rows.append(dict(tipo="union", categoria=col, n=len(s), pct_vacias=100*s.sin.mean(),
                     efecto_w_pp=100*r['obs_w'], p_w=r['p_w'], efecto_eq_pp=100*r['obs'],
                     p_eq=r['p'], efecto_pool_pp=100*r['obs_pool'], p_pool=r['p_pool'],
                     n_quipus_contraste=r['n_groups']))

pd.DataFrame(rows).to_csv(os.path.join(OUT, "color_union_pareado.csv"), index=False, encoding="utf-8-sig")
print("\nguardado color_union_pareado.csv", flush=True)
