# -*- coding: utf-8 -*-
"""Reconstruye el valor de cada cuerda OKR a partir de sus nudos y lo compara con KFG.

Metodo de valor: OKR guarda en knot.knot_value_type el valor decimal aportado por
cada nudo (p.ej. 10 = nudo simple en decenas, 100 = en centenas; en nudos largos
coincide con NUM_TURNS). Verificacion: suma de knot_value_type reproduce KFG en
~98% de las cuerdas. knot_cluster.TOTAL_VALUE esta a 0 en toda la base (no usable).
"""
import os, sqlite3
import pandas as pd
import numpy as np
from importlib import import_module

m = import_module("01_mapeo")
ROOT = m.ROOT; OUT = m.OUT


def reconstruir(knot):
    kn = knot.copy()
    kn["val"] = pd.to_numeric(kn.knot_value_type, errors="coerce").fillna(0)
    # OKR a veces deja knot_value_type=0 en nudos largos con vueltas registradas
    falta = (kn.val <= 0) & kn.TYPE_CODE.isin(["L", "LL"]) & (kn.NUM_TURNS > 0)
    kn.loc[falta, "val"] = kn.loc[falta, "NUM_TURNS"]
    val = kn.groupby("CORD_ID")["val"].sum().rename("valor_okr")
    nkn = kn.groupby("CORD_ID").size().rename("n_nudos_okr")
    nkn_pos = kn[kn.val > 0].groupby("CORD_ID").size().rename("n_nudos_pos_okr")
    return pd.concat([val, nkn, nkn_pos], axis=1).reset_index()


def main():
    km, cord, knot, kc = m.cargar()
    qu = pd.read_csv(m.QUIPUS)
    mp = pd.read_csv(os.path.join(OUT, "salidas", "mapa_quipus.csv"))
    kfg = pd.read_csv(m.CUERDAS)

    filas = []
    for kid in mp.KHIPU_ID.dropna().astype(int).unique():
        c = cord[cord.KHIPU_ID == kid].copy()
        if c.empty:
            continue
        nm = m.nombres_cuerdas(c)
        nm["KHIPU_ID"] = kid
        filas.append(nm)
    cmap = pd.concat(filas, ignore_index=True)
    cmap = cmap.merge(cord[["CORD_ID", "CORD_LENGTH", "CORD_LEVEL", "ATTACH_POS"]], on="CORD_ID", how="left")
    rec = reconstruir(knot)
    cmap = cmap.merge(rec, on="CORD_ID", how="left")
    aliases = mp.dropna(subset=["KHIPU_ID"]).copy()
    aliases["KHIPU_ID"] = aliases.KHIPU_ID.astype(int)
    cmap = cmap.merge(aliases[["KHIPU_ID", "kfg"]], on="KHIPU_ID", how="left")
    cmap.to_csv(os.path.join(OUT, "salidas", "mapa_cuerdas_okr.csv"), index=False)
    print("cuerdas OKR mapeadas:", len(cmap), "quipus:", cmap.KHIPU_ID.nunique())

    j = kfg.merge(cmap, on=["kfg", "cuerda"], how="inner", suffixes=("", "_okr"))
    print("cuerdas KFG con match:", len(j), "de", len(kfg), "; quipus:", j.kfg.nunique())
    j["dlargo"] = (j.largo - j.CORD_LENGTH).abs()
    print("largo |dif|<=0.51:", round((j.dlargo <= 0.51).mean(), 4),
          "| <=0.1:", round((j.dlargo <= 0.1).mean(), 4), "nulo:", j.largo.isna().sum())
    j["valor_okr"] = j.valor_okr.fillna(0)
    j["kfg_ausente"] = j.nudos.isna()
    j["coincide"] = np.isclose(j.valor.fillna(0), j.valor_okr)
    print("coincidencia valor global:", round(j.coincide.mean(), 4))
    print("coincidencia excl. cuerdas sin nudos KFG:", round(j[~j.kfg_ausente].coincide.mean(), 4))
    j.to_csv(os.path.join(OUT, "salidas", "join_cuerdas.csv"), index=False)

    ej = j[(~j.coincide) & (~j.kfg_ausente)][["kfg", "cuerda", "valor", "nudos", "valor_okr", "n_nudos_okr"]]
    print("desacuerdos con nudos KFG:", len(ej), "de", (~j.kfg_ausente).sum())
    print(ej.head(20).to_string())


if __name__ == "__main__":
    main()
