"""Verificación de las cifras de corpus y de las afirmaciones descriptivas simples.

Comprueba:
  A. Conteos OKR (619/54.403/110.677/633; 702 KH; 83 ausentes)
  B. Conteos KFG preparado y comparación con 650/55.720 de KFG y 709/62.746 de K-CAT
  C. K-CAT: 69,7% valor>0; 98,2% khipus con valor; L:S; mediana 42 cuerdas; 80,3% pendants sin subsidiarias
  D. Zenil: 532 khipus / 15.558 cuerdas elegibles y 8.959 enlaces
"""
import json
import os
import sqlite3

import numpy as np
import pandas as pd

from comun import cargar_cuerdas, cargar_quipus, okr_conectar, SALIDA

R = {}


def sec(t):
    print("\n=== " + t + " ===")


# ---------------------------------------------------------------- A. OKR
sec("A. Conteos OKR")
con = okr_conectar()
n_khipu = pd.read_sql("select count(*) n from khipu_main", con).n[0]
n_cord = pd.read_sql("select count(*) n from cord", con).n[0]
n_knot = pd.read_sql("select count(*) n from knot", con).n[0]
n_pc = pd.read_sql("select count(*) n from primary_cord", con).n[0]
n_color = pd.read_sql("select count(*) n from ascher_cord_color", con).n[0]
n_kc = pd.read_sql("select count(*) n from knot_cluster", con).n[0]
print(f"khipu_main={n_khipu} cord={n_cord} knot={n_knot} primary_cord={n_pc} "
      f"ascher_cord_color={n_color} knot_cluster={n_kc}")

kh = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))) if False else
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")),
    "data", "external", "open-khipu-repository", "data", "okr-kh-numbers.csv"),
    encoding="utf-8-sig")
en_db = set(pd.read_sql("select OKR_NUM from khipu_main", con).OKR_NUM)
kh_nums = set(kh["OKR Number"].str.strip())
print(f"KH asignados en CSV={len(kh_nums)}; en khipu.db={len(en_db)}; "
      f"asignados sin fila en DB={len(kh_nums - en_db)}; en DB sin CSV={len(en_db - kh_nums)}")
R["okr"] = dict(khipus=int(n_khipu), cuerdas=int(n_cord), nudos=int(n_knot),
                primary_cord=int(n_pc), colores=int(n_color),
                kh_asignados=len(kh_nums), kh_sin_db=len(kh_nums - en_db))

# ---------------------------------------------------------------- B. KFG preparado
sec("B. KFG preparado vs cifras publicadas")
c = cargar_cuerdas()
q = cargar_quipus()
por_khipu = c.groupby("kfg").size()
print(f"cuerdas.csv: khipus={c.kfg.nunique()} cuerdas={len(c)} "
      f"mediana cuerdas/khipu={por_khipu.median():.0f} media={por_khipu.mean():.1f}")
print(f"quipus sin nudos={c.groupby('kfg').con_nudos.sum().eq(0).sum()} "
      f"({100*c.groupby('kfg').con_nudos.sum().eq(0).mean():.1f}%)")
print(f"quipus con cuerdas de nivel 0={c[c.nivel == 0].kfg.nunique()}")
print(f"KFG declara 650 khipus/55.720 cuerdas; K-CAT declara 709/62.746; "
      f"repo preparado {c.kfg.nunique()}/{len(c)}")
R["kfg"] = dict(khipus=int(c.kfg.nunique()), cuerdas=int(len(c)),
                mediana_cuerdas=float(por_khipu.median()),
                khipus_sin_nudos=int(c.groupby("kfg").con_nudos.sum().eq(0).sum()))

# ---------------------------------------------------------------- C. K-CAT
sec("C. K-CAT descriptivos")
n_val_pos = (c.v > 0).sum()
print(f"cuerdas valor>0: {n_val_pos}/{len(c)} = {100*n_val_pos/len(c):.1f}% (K-CAT: 69,7%)")
khipus_val = c[c.v > 0].kfg.nunique()
print(f"khipus con >=1 valor: {khipus_val}/{c.kfg.nunique()} = "
      f"{100*khipus_val/c.kfg.nunique():.1f}% (K-CAT: 98,2%)")
# L:S en la cadena de nudos (racimos tipo L / S)
import re
nL = c.nudos.str.count(r"\d+(?:\.\d+)?L")
nS = c.nudos.str.count(r"\d+(?:\.\d+)?S")
print(f"racimos L={nL.sum()} S={nS.sum()} L:S={nL.sum()/max(nS.sum(),1):.3f} (K-CAT: 1,05)")
# pendants sin subsidiarias
padres = set(zip(c[c.nivel >= 1].kfg, c[c.nivel >= 1].padre))
pend = c[c.nivel == 0]
sin_sub = sum((k, cu) not in padres for k, cu in zip(pend.kfg, pend.cuerda))
print(f"pendants sin subsidiarias: {sin_sub}/{len(pend)} = {100*sin_sub/len(pend):.1f}% "
      f"(K-CAT: 80,3%)")
R["kcat_desc"] = dict(pct_val_pos=round(100*n_val_pos/len(c), 2),
                      pct_khipus_val=round(100*khipus_val/c.kfg.nunique(), 2),
                      L_S=round(float(nL.sum()/max(nS.sum(), 1)), 3),
                      pct_pendant_sin_sub=round(100*sin_sub/len(pend), 2))

# ---------------------------------------------------------------- D. Zenil elegibles
sec("D. Zenil: conjunto elegible")
kc = pd.read_sql("select CORD_ID, START_POS, ORDINAL, NUM_KNOTS from knot_cluster", con)
pos = kc[kc.START_POS > 0]
g = pos.groupby("CORD_ID").START_POS.nunique()
eleg = set(g[g >= 2].index)
cord = pd.read_sql("select CORD_ID, KHIPU_ID, CORD_LEVEL, PENDANT_FROM, ATTACHED_TO, TWIST, FIBER "
                   "from cord", con)
cord["eleg"] = cord.CORD_ID.isin(eleg)
print(f"cuerdas elegibles (>=2 posiciones positivas distintas)={len(eleg)} "
      f"en {cord[cord.eleg].KHIPU_ID.nunique()} khipus (Zenil: 15.558 / 532)")
# enlaces padre-hijo: en el OKR la subsidiaria apunta al padre en PENDANT_FROM
m = cord.merge(cord[["CORD_ID", "KHIPU_ID"]], left_on="PENDANT_FROM",
               right_on="CORD_ID", suffixes=("", "_padre"))
enl = m[(m.CORD_LEVEL >= 2) & (m.KHIPU_ID == m.KHIPU_ID_padre)]
knotted = set(kc.CORD_ID)
enl_kn = enl[enl.CORD_ID.isin(knotted) & enl.CORD_ID_padre.isin(knotted)]
print(f"enlaces hijo->padre nivel>=2: {len(enl)}; con nudos en ambos extremos: "
      f"{len(enl_kn)}; con fibra y torsion completas: "
      f"{len(enl.dropna(subset=['TWIST', 'FIBER']))}")
R["zenil"] = dict(cuerdas_elegibles=int(len(eleg)),
                  khipus_elegibles=int(cord[cord.eleg].KHIPU_ID.nunique()),
                  enlaces=int(len(enl)), enlaces_con_nudos=int(len(enl_kn)))

# ---------------------------------------------------------------- salida
with open(os.path.join(SALIDA, "res_02_corpus.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print("\nGuardado res_02_corpus.json")
