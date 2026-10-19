"""Cierre: conjunto 'sospechoso' de cuerdas que hay que auditar a mano, tasas por
fuente, y contraste U <-> desacuerdo SOLO sobre los pares alineados 1-a-1.
"""
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
c = pd.read_csv(AQUI/"racimos_alt.csv")
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)

# --- cuerdas con defecto DURO (no depende de convencion)
mal = c[(c.ap.isna()) | (c.tipo == "?") | ((c.tipo == "S") & (c.n > 9))]
mal_i = set(mal.i)
# S con aporte no decimal
c2 = c[(c.tipo == "S") & c.ap.notna() & c.niv.isna()]
mal_i |= set(c2.i)
d["sospechosa"] = d.index.isin(mal_i)
print("cuerdas con defecto duro (aporte ausente/no parseable, S>9, S no decimal):",
      d.sospechosa.sum(), f"({100*d.sospechosa.mean():.2f}%)  quipus:", d[d.sospechosa].kfg.nunique())
print("  de ellas con valor>0:", (d[d.sospechosa].valor.astype(float) > 0).sum())

raras = set(c[~c.tipo.isin(["S", "L", "E"])].i)
d["rara"] = d.index.isin(raras)
print("cuerdas con algun tipo de nudo raro:", d.rara.sum(), f"({100*d.rara.mean():.2f}%)  quipus:", d[d.rara].kfg.nunique())

# --- tasas por fuente
P = pd.read_csv(AQUI/"kfg_vs_okr_cuerdas.csv")
P["dif"] = P.v.fillna(0) - P.v_kfg
P["fuente"] = P.kfg.str.extract(r"^([A-Z]+)")[0]
P["nU"] = P.nU.fillna(0); P["nk"] = P.nk.fillna(0)
t = P.groupby("fuente").agg(quipus=("kfg", "nunique"), cuerdas=("dif", "size"),
                            desacuerdo=("dif", lambda s: s.ne(0).mean()),
                            frac_U=("nU", "sum"), kn=("nk", "sum"))
t["frac_U"] = t.frac_U/t.kn
print("\n-- por fuente (todas las cuerdas comparables) --")
print(t[["quipus", "cuerdas", "desacuerdo", "frac_U"]].round(4).to_string())

# --- U vs desacuerdo sobre pares alineados 1-a-1
W = pd.read_csv(AQUI/"desacuerdos_alineados.csv")
d["nU_kfg"] = [s.count(",U)") for s in d.nudos]
d["nk_kfg"] = [s.count(")") for s in d.nudos]
W = W.merge(d[["kfg", "cuerda", "nU_kfg", "nk_kfg"]], on=["kfg", "cuerda"], how="left")
print("\npares alineados 1-a-1 con valor distinto:", len(W))
print("  de ellos con >=1 nudo U en KFG:", (W.nU_kfg.fillna(0) > 0).sum(),
      f"({100*(W.nU_kfg.fillna(0)>0).mean():.1f}%)")
base = P.assign(U=P.nU > 0)
print("  base comparable: fraccion de cuerdas con >=1 U:", round((base.nU > 0).mean(), 4))
print("  |dif| mediana de los pares:", W.dif.abs().median() if "dif" in W else
      (W.v_okr-W.v_kfg).abs().median())
print("  razon okr/kfg = 10 o 0.1:", ((W.v_okr/W.v_kfg.replace(0, np.nan)).round(2).isin([10, 0.1])).sum())
