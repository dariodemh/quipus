# -*- coding: utf-8 -*-
"""
01_descriptivo.py  --  Cuerdas sin nudos: taxonomía, distribución y control cruzado OKR.
Lee analisis/datos/{cuerdas,quipus}.csv (KFG) y data/external/open-khipu-repository/data/khipu.db.
Salidas: tablas_01.csv (varias secciones), resumen impreso <= 40 líneas.
"""
import os, re, sqlite3
import numpy as np
import pandas as pd

BASE = r"."
OUT = os.path.join(BASE, "analisis", "ds", "t_cuerdas_vacias")
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(os.path.join(BASE, "analisis", "datos", "cuerdas.csv"), dtype=str, keep_default_na=False)
q = pd.read_csv(os.path.join(BASE, "analisis", "datos", "quipus.csv"), dtype=str, keep_default_na=False)

df["sin"] = df.nudos.str.strip() == ""
df["nivel"] = df.nivel.astype(int)
df["orden"] = df.orden.astype(int)
df["grupo"] = df.grupo.astype(int)
df["L"] = pd.to_numeric(df.largo, errors="coerce")

# --- taxonomía de terminación (OKR termination_dc)
TERM = {"K": "K knotted (completa, nudo terminal)",
        "B": "B broken (rota)", "C": "C cut (cortada)",
        "U": "U unfinished (sin nudo terminal)", "R": "R ravelled (deshilachada)",
        "D": "D doubled (doblada)", "": "sin dato", "0": "código 0"}
df["term_lab"] = df.terminacion.map(lambda x: TERM.get(x, x))
df["rota"] = df.terminacion.isin(["B", "C"])
df["completa"] = df.terminacion.isin(["K", "U", "R", "D"])

rows = []
def add(sec, k, v):
    rows.append({"seccion": sec, "clave": k, "valor": v})

add("global", "cuerdas", len(df))
add("global", "quipus", df.kfg.nunique())
add("global", "sin_nudos", int(df.sin.sum()))
add("global", "pct_sin_nudos", round(100 * df.sin.mean(), 2))
add("global", "rotas_cortadas", int((df.sin & df.rota).sum()))
add("global", "completas_sin_nudos", int((df.sin & df.completa).sum()))
add("global", "terminacion_desconocida", int((df.sin & ~df.rota & ~df.completa).sum()))

# por terminación
tab = df.groupby("term_lab").agg(n=("sin", "size"), sin=("sin", "sum"))
tab["pct_sin"] = (100 * tab.sin / tab.n).round(1)
tab["pct_del_total_sin"] = (100 * tab.sin / df.sin.sum()).round(1)
tab.to_csv(os.path.join(OUT, "tab_terminacion.csv"), encoding="utf-8-sig")
for k, r in tab.iterrows():
    add("terminacion", k, f"n={int(r.n)}; sin={int(r.sin)}; pct_sin={r.pct_sin}; pct_del_total={r.pct_del_total_sin}")

# por nivel
tab = df.groupby("nivel").agg(n=("sin", "size"), sin=("sin", "sum"))
tab["pct_sin"] = (100 * tab.sin / tab.n).round(1)
tab.to_csv(os.path.join(OUT, "tab_nivel.csv"), encoding="utf-8-sig")
for k, r in tab.iterrows():
    add("nivel", int(k), f"n={int(r.n)}; sin={int(r.sin)}; pct_sin={r.pct_sin}")

# por quipu
g = df.groupby("kfg").agg(n=("sin", "size"), sin=("sin", "sum"), rotas=("rota", "sum"), completas=("completa", "sum"))
g["p"] = g.sin / g.n
g["p_rotas"] = g.rotas / g.n
g["p_completas"] = g.completas / g.n
g.to_csv(os.path.join(OUT, "tab_por_quipu.csv"), encoding="utf-8-sig")
add("quipu", "con_al_menos_1_sin", int((g.sin > 0).sum()))
add("quipu", "todos_sin", int((g.p == 1).sum()))
add("quipu", "p_sin_mediana", round(g.p.median(), 3))
add("quipu", "p_sin_p25_p75", f"{g.p.quantile(.25):.3f}-{g.p.quantile(.75):.3f}")
add("quipu", "p_sin_max", round(g.p.max(), 3))
add("quipu", "spearman_p_vs_n", round(g[["p", "n"]].corr(method="spearman").iloc[0, 1], 3))
add("quipu", "top5_quipus_por_n_sin", ", ".join(g.sort_values("sin", ascending=False).head(5).index.tolist()))

# largos
for lab, sub in [("todas_sin", df[df.sin]),
                 ("rotas", df[df.sin & df.rota]),
                 ("completas", df[df.sin & df.completa]),
                 ("K", df[(df.terminacion == "K") & df.sin]),
                 ("U", df[(df.terminacion == "U") & df.sin]),
                 ("con_nudos", df[~df.sin])]:
    s = sub.L.dropna()
    add("largo", lab, f"n={len(s)}; media={s.mean():.1f}; mediana={s.median():.1f}; p25={s.quantile(.25):.1f}; p75={s.quantile(.75):.1f}")

# --- control cruzado con OKR (conteo por quipu de cuerdas sin ningún knot_cluster)
con = sqlite3.connect(os.path.join(BASE, "data", "external", "open-khipu-repository", "data", "khipu.db"))
km = pd.read_sql("select KHIPU_ID, OKR_NUM, INVESTIGATOR_NUM, COMPLETE from khipu_main", con)
bykh = dict(zip(km.OKR_NUM, km.KHIPU_ID))
byinv = dict(zip(km.INVESTIGATOR_NUM, km.KHIPU_ID))
q["kid"] = [bykh.get(o) or byinv.get(o) or byinv.get(k) for o, k in zip(q.okr, q.kfg)]

cord_okr = pd.read_sql("""
select c.KHIPU_ID, c.CORD_ID, c.CORD_LEVEL, c.TERMINATION,
       (select count(*) from knot_cluster kc where kc.CORD_ID=c.CORD_ID) as nclusters
from cord c where c.CORD_LEVEL >= 1
""", con)
ok = cord_okr.groupby("KHIPU_ID").agg(okr_cords=("CORD_ID", "size"),
                                      okr_sin=("nclusters", lambda s: int((s == 0).sum())))
q = q.merge(ok, left_on="kid", right_index=True, how="left")
q = q.merge(g.reset_index(), on="kfg", how="left")
qq = q[q.okr_cords.notna()].copy()
qq["dif"] = qq.sin - qq.okr_sin
qq["dif_rel"] = qq.sin / qq.n - qq.okr_sin / qq.okr_cords
add("okr_cruce", "quipus_emparejados", len(qq))
add("okr_cruce", "spearman_n_sin_kfg_vs_okr", round(qq[["sin", "okr_sin"]].corr(method="spearman").iloc[0, 1], 3))
add("okr_cruce", "pearson_n_sin_kfg_vs_okr", round(qq[["sin", "okr_sin"]].corr().iloc[0, 1], 3))
add("okr_cruce", "mediana_dif_abs_n", round((qq.sin - qq.okr_sin).abs().median(), 1))
add("okr_cruce", "mediana_dif_rel", round(qq.dif_rel.median(), 4))
add("okr_cruce", "pct_quipus_dif_rel_menor_0.05", round(100 * (qq.dif_rel.abs() < 0.05).mean(), 1))
qq[["kfg", "okr", "n", "sin", "okr_cords", "okr_sin", "dif", "dif_rel"]].to_csv(
    os.path.join(OUT, "tab_cruce_okr.csv"), index=False, encoding="utf-8-sig")

pd.DataFrame(rows).to_csv(os.path.join(OUT, "tablas_01.csv"), index=False, encoding="utf-8-sig")
print(pd.DataFrame(rows).to_string(max_colwidth=90))
