# -*- coding: utf-8 -*-
"""Convencion 'objeto atado = perdida / muerte / anulacion' y marcadores
materiales. En el corpus antiguo el unico objeto atado registrado de forma
sistematica en OKR es el canuto (CANUTO_ORDINAL>0).

K1 los colgantes con canuto valen menos que los que no lo tienen
K2 los colgantes con canuto se quedan sin nudos / valor 0 mas a menudo
K3 los canutos se concentran en los bordes de grupo
K4 MI(canuto; color)
K5 MI(canuto; fibra camelido)
Nulo: permutar la marca de canuto entre colgantes DENTRO de cada quipu.
"""
import numpy as np
import pandas as pd
from utils import load, describe, SEMILLA

rng = np.random.default_rng(SEMILLA)
B = 1000


def fast_mi(x, y):
    k = int(max(x.max(), y.max()) + 1)
    ct = np.bincount(x * k + y, minlength=k * k).reshape(k, k).astype(float)
    n = ct.sum()
    if n == 0:
        return 0.0
    px = ct.sum(1) / n
    py = ct.sum(0) / n
    pxy = ct / n
    nz = pxy > 0
    return float(np.sum(pxy[nz] * np.log2(pxy[nz] / np.outer(px, py)[nz])))


c = load()
p = c[(c.nivel == 0)].copy()
g = p.groupby("kfg").canuto.agg(n="size", k="sum")
keep = g[(g.k >= 2) & (g.n - g.k >= 5)].index
p = p[p.kfg.isin(keep)].sort_values(["kfg", "orden"]).reset_index(drop=True)

blocks = []
for k, dd in p.groupby("kfg"):
    dd = dd.sort_values("orden").reset_index(drop=True)
    # borde de grupo: primero o ultimo colgante del grupo
    edge = np.zeros(len(dd), dtype=int)
    for gid, gg in dd.groupby("grupo"):
        idx = gg.index.values
        edge[idx[0]] = 1
        edge[idx[-1]] = 1
    blocks.append(dict(kfg=k, can=dd.canuto.values.astype(int),
                       val=dd.valor.fillna(0).values.astype(float),
                       nudos=(dd.nudos.fillna("") == "").values.astype(int),
                       edge=edge,
                       col=pd.Categorical(dd.colfam.fillna("NA")).codes.astype(np.int64),
                       fib=pd.Categorical(dd.fibra.fillna("NA")).codes.astype(np.int64)))


def stats_for(can_list):
    dnum = dden = zero = 0.0
    edge = 0.0
    en = 0.0
    mic = mif = 0.0
    for b, can in zip(blocks, can_list):
        z = can == 1
        nz = can == 0
        vz = b["val"][z & (b["val"] > 0)]
        vn = b["val"][nz & (b["val"] > 0)]
        if len(vz) and len(vn):
            w = len(vz) * len(vn) / (len(vz) + len(vn))
            dnum += w * (np.log1p(vz).mean() - np.log1p(vn).mean())
            dden += w
        zero += b["nudos"][z].sum()
        en += z.sum()
        if z.sum():
            edge += b["edge"][z].mean()
        mic += fast_mi(can.astype(np.int64), b["col"])
        mif += fast_mi(can.astype(np.int64), b["fib"])
    return dict(K1=(dnum / dden if dden else np.nan),
                K2=(zero / en if en else np.nan),
                K3=edge / len(blocks), K4=mic, K5=mif)


obs = stats_for([b["can"] for b in blocks])
null = {k: [] for k in ["K1", "K2", "K3", "K4", "K5"]}
for it in range(B):
    cans = []
    for b in blocks:
        x = b["can"].copy()
        rng.shuffle(x)
        cans.append(x)
    st = stats_for(cans)
    for k in null:
        null[k].append(st[k])

labels = {"K1": "log(valor con canuto) - log(valor sin canuto)",
          "K2": "fraccion de cuerdas con canuto y sin nudos",
          "K3": "fraccion de canutos en borde de grupo",
          "K4": "MI(canuto; color)", "K5": "MI(canuto; fibra)"}
sides = {"K1": "less", "K2": "greater", "K3": "greater", "K4": "greater", "K5": "greater"}
rows = []
for k in ["K1", "K2", "K3", "K4", "K5"]:
    d = describe(obs[k], null[k], sides[k])
    d.update(test=k, descripcion=labels[k], n_quipus=len(blocks), lado=sides[k])
    rows.append(d)
res = pd.DataFrame(rows)
res.to_csv("res_canutos.csv", index=False, encoding="utf-8-sig")
print(res.round(4).to_string())
print("quipus", len(blocks), "cuerdas", len(p), "canutos", p.canuto.sum())
print("top quipus", p[p.canuto == 1].kfg.value_counts().head(8).to_dict())
