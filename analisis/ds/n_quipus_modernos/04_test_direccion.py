# -*- coding: utf-8 -*-
"""Convencion 'direccion del nudo = mitad / categoria' (Urton 2003;
Hyland, Ware & Clark 2014; Clindaniel 2019; tablero de Mangas 2021).

D1 pureza por cuerda: las cuerdas multi-nudo son S o Z, no mezclas.
   Nulo: barajar la direccion de TODOS los nudos DENTRO del quipu,
   preservando el numero de nudos por cuerda y la razon S:Z del quipu.
D2 valor: cuerdas S vs Z, con y sin estratificar por numero de nudos
   (la direccion puede estar mecánicamente ligada al tipo de nudo).
D3 MI(direccion; color) dentro del quipu y D3b controlando el grupo.
D4 MI(direccion; torsion).
D5 MI(direccion; grupo).
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
d = c[(c.nivel == 0) & c.dir.isin(["S", "Z"])].copy()
g = d.groupby("kfg").dir.agg(n="size", z=lambda s: (s == "Z").sum())
keep = g[(g.n >= 8) & (g.z >= 2) & (g.n - g.z >= 2)].index
d = d[d.kfg.isin(keep)].sort_values(["kfg", "orden"]).reset_index(drop=True)

blocks = []
for k, dd in d.groupby("kfg"):
    dd = dd.reset_index(drop=True)
    blocks.append(dict(kfg=k, dir=dd.dir.values.copy(),
                       ns=dd.dir_s.values.astype(int), nz=dd.dir_z.values.astype(int),
                       val=dd.valor.fillna(0).values.astype(float),
                       col=pd.Categorical(dd.colfam.fillna("NA")).codes.astype(np.int64),
                       grp=pd.Categorical(dd.grupo.fillna(-1).astype(str)).codes.astype(np.int64),
                       tw=pd.Categorical(dd.twist.fillna("NA")).codes.astype(np.int64),
                       grpraw=dd.grupo.fillna(-1).astype(int).values))


def expand(b):
    return np.array(["S"] * int(b["ns"].sum()) + ["Z"] * int(b["nz"].sum()))


def purity_from_flat(b, flat):
    ns = b["ns"]
    nz = b["nz"]
    n = ns + nz
    ok = n >= 2
    if ok.sum() == 0:
        return np.nan
    pos = 0
    pure = 0
    for i in range(len(ns)):
        k = n[i]
        seg = flat[pos:pos + k]
        pos += k
        if k >= 2:
            if len(np.unique(seg)) == 1:
                pure += 1
    return pure / ok.sum()


def stats_for(dirs):
    num = den = mic = mit = mig = micg = 0.0
    numg = deng = 0.0
    numk = denk = 0.0
    for b, dv in zip(blocks, dirs):
        z = dv == "Z"
        s = dv == "S"
        vz = np.log1p(b["val"][z & (b["val"] > 0)])
        vs = np.log1p(b["val"][s & (b["val"] > 0)])
        if len(vz) and len(vs):
            w = len(vz) * len(vs) / (len(vz) + len(vs))
            num += w * (vz.mean() - vs.mean())
            den += w
        # D2b: diferencia de valor DENTRO de cada grupo
        for gid in np.unique(b["grp"]):
            m = b["grp"] == gid
            zz = m & z & (b["val"] > 0)
            ss = m & s & (b["val"] > 0)
            if zz.sum() and ss.sum():
                w = zz.sum() * ss.sum() / (zz.sum() + ss.sum())
                numg += w * (np.log1p(b["val"][zz]).mean() - np.log1p(b["val"][ss]).mean())
                deng += w
        # D2c: diferencia de valor DENTRO de estratos de numero de nudos
        nk = np.minimum(b["ns"] + b["nz"], 6)
        for kk in np.unique(nk):
            m = nk == kk
            zz = m & z & (b["val"] > 0)
            ss = m & s & (b["val"] > 0)
            if zz.sum() and ss.sum():
                w = zz.sum() * ss.sum() / (zz.sum() + ss.sum())
                numk += w * (np.log1p(b["val"][zz]).mean() - np.log1p(b["val"][ss]).mean())
                denk += w
        dc = np.where(dv == "S", 0, 1).astype(np.int64)
        mic += fast_mi(dc, b["col"])
        mig += fast_mi(dc, b["grp"])
        mit += fast_mi(dc, b["tw"])
        # MI condicional al grupo
        for gid in np.unique(b["grp"]):
            m = b["grp"] == gid
            if m.sum() >= 3 and len(np.unique(dc[m])) > 1 and len(np.unique(b["col"][m])) > 1:
                micg += m.sum() / len(dc) * fast_mi(dc[m], b["col"][m])
    return dict(D2=(num / den if den else np.nan), D2b=(numg / deng if deng else np.nan),
                D2c=(numk / denk if denk else np.nan),
                D3=mic, D3b=micg, D4=mit, D5=mig)


obs = stats_for([b["dir"] for b in blocks])

# D1: pureza observada y nula (barajando nudos dentro del quipu)
pur_obs = np.array([purity_from_flat(b, expand(b)) for b in blocks])
pur_null_quipu = {b["kfg"]: [] for b in blocks}
for it in range(B):
    for b in blocks:
        flat = expand(b).copy()
        rng.shuffle(flat)
        pur_null_quipu[b["kfg"]].append(purity_from_flat(b, flat))
pur_null_global = [np.nanmean([pur_null_quipu[b["kfg"]][it] for b in blocks])
                   for it in range(B)]
pur_obs_global = np.nanmean(pur_obs)

null = {k: [] for k in ["D2", "D2b", "D2c", "D3", "D3b", "D4", "D5"]}
for it in range(B):
    dirs = []
    for b in blocks:
        dv = b["dir"].copy()
        rng.shuffle(dv)
        dirs.append(dv)
    st = stats_for(dirs)
    for k in null:
        null[k].append(st[k])

rows = []
rows.append(dict(test="D1", descripcion="pureza de direccion por cuerda (fraccion)",
                 obs=pur_obs_global, null_mean=float(np.mean(pur_null_global)),
                 null_sd=float(np.std(pur_null_global, ddof=1)),
                 efecto_z=(pur_obs_global - np.mean(pur_null_global)) / np.std(pur_null_global, ddof=1),
                 p=(1 + np.sum(np.array(pur_null_global) >= pur_obs_global)) / (1 + B),
                 n_quipus=len(blocks), lado="greater"))
labels = {"D2": "log(valor Z) - log(valor S)", "D2b": "log(valor Z) - log(valor S) | grupo",
          "D2c": "log(valor Z) - log(valor S) | nudos", "D3": "MI(direccion; color)",
          "D3b": "MI(direccion; color | grupo)", "D4": "MI(direccion; torsion)",
          "D5": "MI(direccion; grupo)"}
for k in ["D2", "D2b", "D2c", "D3", "D3b", "D4", "D5"]:
    dd = describe(obs[k], null[k], "two" if k.startswith("D2") else "greater")
    dd.update(test=k, descripcion=labels[k], n_quipus=len(blocks),
              lado="two" if k.startswith("D2") else "greater")
    rows.append(dd)

res = pd.DataFrame(rows)
res.to_csv("res_direccion.csv", index=False, encoding="utf-8-sig")
print(res.round(4).to_string())
print("quipus:", len(blocks), "cuerdas multi-nudo:", int((d.dir_s + d.dir_z >= 2).sum()))
print("pureza obs", round(pur_obs_global, 3), "nula", round(float(np.mean(pur_null_global)), 3))
