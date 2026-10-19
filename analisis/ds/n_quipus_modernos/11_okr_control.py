# -*- coding: utf-8 -*-
"""Control independiente en OKR: ?la direccion del nudo es una propiedad de la
cuerda (pureza) o un artefacto de la transcripcion KFG?
OKR registra DIRECTION por nudo, no por cuerda. Se calcula la pureza de las
cuerdas con >=2 nudos S/Z y se compara con un nulo que baraja las direcciones
entre todos los nudos del quipu (preservando el numero de nudos por cuerda)."""
import sqlite3
import numpy as np
import pandas as pd

DB = r"./data/external/open-khipu-repository/data/khipu.db"
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
k = pd.read_sql("select CORD_ID, DIRECTION from knot", con)
co = pd.read_sql("select CORD_ID, KHIPU_ID from cord", con)
con.close()
k = k[k.DIRECTION.isin(["S", "Z"])].merge(co, on="CORD_ID", how="left")
k["isZ"] = (k.DIRECTION == "Z").astype(np.int8)

blocks = []
for kid, d in k.groupby("KHIPU_ID"):
    codes, uniq = pd.factorize(d.CORD_ID)
    z = d.isZ.values
    blocks.append((codes.astype(np.int64), z, len(uniq)))


def purity(z_list):
    nums = []
    dens = []
    for (codes, _, n) in blocks_data:
        pass
    tot = 0.0
    n = 0
    for (codes, z0, nc), z in zip(blocks_data, z_list):
        s = np.bincount(codes, weights=z, minlength=nc)
        c = np.bincount(codes, minlength=nc)
        ok = c >= 2
        if ok.sum():
            tot += np.sum((s[ok] == 0) | (s[ok] == c[ok]))
            n += ok.sum()
    return tot / n if n else np.nan


blocks_data = [(c, z, n) for (c, z, n) in blocks]
obs = purity([z for _, z, _ in blocks_data])

rng = np.random.default_rng(20261018)
B = 1000
null = []
for it in range(B):
    zs = []
    for _, z, _ in blocks_data:
        zz = z.copy()
        rng.shuffle(zz)
        zs.append(zz)
    null.append(purity(zs))
null = np.array(null)
p = (1 + np.sum(null >= obs)) / (1 + B)
print("cuerdas OKR con >=2 nudos S/Z:", int(sum((np.bincount(c, minlength=n) >= 2).sum()
                                               for c, _, n in blocks_data)))
print("quipus:", len(blocks_data), "| pureza obs:", round(obs, 4),
      "| nula:", round(np.nanmean(null), 4),
      "| z:", round((obs - np.nanmean(null)) / np.nanstd(null, ddof=1), 2),
      "| p:", round(p, 4))
pd.DataFrame([dict(test="D1_OKR", obs=obs, null_mean=np.nanmean(null),
                   null_sd=np.nanstd(null, ddof=1),
                   efecto_z=(obs - np.nanmean(null)) / np.nanstd(null, ddof=1),
                   p=p, n_quipus=len(blocks_data))]).to_csv(
    "res_direccion_okr.csv", index=False, encoding="utf-8-sig")
