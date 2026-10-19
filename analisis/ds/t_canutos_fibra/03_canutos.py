"""
Descriptivo de canutos y canutitos + alineamiento con la estructura de grupos.

Preguntas:
 1. cuantos quipus tienen canutos y en que regimen (envoltura total vs puntual)
 2. que envuelve un canuto (n de cuerdas, largo, nivel)
 3. los limites de canuto/cluster coinciden con limites de grupo, de color
    o de valor?  (nulo: permutacion de los limites dentro del mismo quipu)
 4. los canutitos marcan cuerdas selectivamente?

Salida: resultados en pantalla + canutos_resumen.csv
"""
import os, sqlite3
import numpy as np
import pandas as pd

BASE = r"."
OUT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "data", "external", "open-khipu-repository", "data", "khipu.db")
rng = np.random.default_rng(20241018)
con = sqlite3.connect(DB)

q = pd.read_csv(os.path.join(OUT, "quipus.csv"))
cord = pd.read_csv(os.path.join(OUT, "cuerdas_okr.csv"), low_memory=False)
can = pd.read_sql("select * from canuto", con)
clu = pd.read_sql("select * from canuto_cluster", con)
canit = pd.read_sql("select * from canutito", con).merge(
    pd.read_sql("select CORD_ID,KHIPU_ID from cord", con), on="CORD_ID")

print("=" * 70)
print("1. PREVALENCIA")
n = len(q)
con_can = (q.num_canuto_cords > 0).sum()
print("quipus KFG: %d; con >=1 canuto: %d (%.1f%%)" % (n, con_can, 100 * con_can / n))
print("quipus OKR con registros canuto: %d de %d" % ((q.n_canuto > 0).sum(), q.KHIPU_ID.notna().sum()))
sub = q[q.num_canuto_cords > 0].copy()
sub["frac"] = sub.num_canuto_cords / sub.num_cords
print("\nregimen (fraccion de cuerdas envueltas por canuto):")
print(pd.cut(sub.frac, [0, .05, .25, .5, .75, .999, 1.0]).value_counts().sort_index().to_string())
print("\nquipus con >=50%% envuelto: %d ; con <=5%%: %d" % ((sub.frac >= .5).sum(), (sub.frac <= .05).sum()))
print("\ntop 12 por fraccion:")
print(sub.sort_values("frac", ascending=False)
      .head(12)[["kfg_name", "okr", "zona", "num_cords", "num_canuto_cords", "frac"]]
      .round(3).to_string(index=False))

print("\n" + "=" * 70)
print("2. QUE ENVUELVE UN CANUTO (8 quipus OKR, 236 canutos)")
print("cuerdas por canuto:", can.NUM_CORDS.describe()[["mean", "50%", "min", "max"]].round(2).to_dict())
print("largo canuto (cm):", can.CANUTO_LENGTH.describe()[["mean", "50%", "min", "max"]].round(2).to_dict())
print("nivel:", can.CTO_LEVEL.unique(), " loops:", can.NUM_LOOPS.unique())
print("\ncobertura = cuerdas en canuto / cuerdas totales, por quipu:")
z = q[q.n_canuto > 0][["okr", "kfg_name", "num_cords", "n_canuto", "n_canuto_cluster",
                        "n_cord_en_canuto", "n_canutito", "n_cord_con_canutito", "zona"]].copy()
z["cob"] = (z.n_cord_en_canuto / z.num_cords).round(3)
z["cob_canitito"] = (z.n_cord_con_canutito / z.num_cords).round(3)
print(z.to_string(index=False))

print("\n" + "=" * 70)
print("3. ALINEAMIENTO DE LIMITES")
# para cada quipu con canutos: limites de canuto (CTO_END_CORD) en el orden de
# las cuerdas; comparar con limites de grupo, de color y de valor.
def boundaries(seq):
    return {i for i in range(1, len(seq)) if seq[i] != seq[i - 1]}

rows = []
for kid, g in cord[cord.KHIPU_ID.isin(q[q.n_canuto > 0].KHIPU_ID)].groupby("KHIPU_ID"):
    g = g.sort_values(["CORD_LEVEL", "CORD_ORDINAL"])
    # solo nivel 1 (colgantes del cordon principal), en orden de ordinal
    g1 = g[g.CORD_LEVEL == 1].sort_values("CORD_ORDINAL").reset_index(drop=True)
    if len(g1) < 10:
        continue
    okr = q.loc[q.KHIPU_ID == kid].iloc[0]
    # limite de canuto segun OKR CTO_END_CORD (nivel 1)
    o = can[can.KHIPU_ID == kid].set_index("CTO_BEG_CORD")
    lim = sorted(set(int(x) for x in can.loc[can.KHIPU_ID == kid, "CTO_END_CORD"]
                     if x < len(g1)))
    # limites alternativos
    lim_grupo = sorted(boundaries(g1.grupo.fillna(-9).tolist()))
    lim_color = sorted(boundaries(g1.color.fillna("NA").astype(str).tolist()))
    lim_valor = sorted(boundaries((g1.valor.fillna(-1) > 0).astype(int).tolist()))
    def jac(a, b):
        a, b = set(a), set(b)
        return len(a & b) / len(a | b) if (a | b) else np.nan
    rows.append(dict(kfg=okr.kfg_name, n1=len(g1), n_lim_canuto=len(lim),
                     n_grupo=len(lim_grupo), n_color=len(lim_color), n_val=len(lim_valor),
                     j_grupo=jac(lim, lim_grupo), j_color=jac(lim, lim_color),
                     j_val=jac(lim, lim_valor)))
al = pd.DataFrame(rows)
print(al.round(3).to_string(index=False))
print("\nJaccard medio: grupo %.3f  color %.3f  valor %.3f" %
      (al.j_grupo.mean(), al.j_color.mean(), al.j_val.mean()))

print("\n" + "=" * 70)
print("4. CANUTITOS: selectivos o de quipu completo?")
c8 = cord[cord.KHIPU_ID.isin(q[q.n_canutito > 0].KHIPU_ID)].copy()
c8["tiene_canutito"] = c8.CORD_ID.isin(canit.CORD_ID)
print(c8.groupby("KHIPU_ID").agg(n=("CORD_ID", "size"),
                                 con=("tiene_canutito", "sum"),
                                 frac=("tiene_canutito", "mean")).round(3).to_string())
c8["v0"] = (c8.valor.fillna(-1) == 0) | c8.valor.isna()
print("\ncanutito vs valor 0/ausente (solo quipus con canutito):")
print(pd.crosstab(c8.tiene_canutito, c8.v0, normalize="index").round(3).to_string())
print("\ncanutito vs nivel de cuerda:")
print(pd.crosstab(c8.CORD_LEVEL, c8.tiene_canutito, normalize="index").round(3).to_string())
