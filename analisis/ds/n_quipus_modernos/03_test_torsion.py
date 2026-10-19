# -*- coding: utf-8 -*-
"""Convencion 'torsion = mitad / categoria marcada'.
Pruebas en el corpus antiguo (KFG+OKR), unidad = quipu, nulo = permutar la
torsion entre colgantes DENTRO de cada quipu.

T1 transiciones (bloques contiguos de S/Z)
T2 particion en mitades por grupo (una mitad S, la otra Z)
T3 los colgantes Z valen menos que los S (marcado = menos valorado)
T4 la torsion se asocia al color (MI)
T5 la torsion se asocia al grupo (MI)
"""
import numpy as np
import pandas as pd
from utils import load, describe, SEMILLA

rng = np.random.default_rng(SEMILLA)
B = 1000


def fast_mi(x, y):
    """MI en bits para dos arrays de enteros no negativos."""
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
p = c[(c.nivel == 0) & c.twist.isin(["S", "Z"])].copy()
g = p.groupby("kfg").twist.agg(n="size", z=lambda s: (s == "Z").sum())
keep = g[(g.n >= 5) & (g.z >= 2) & (g.n - g.z >= 2)].index
p = p[p.kfg.isin(keep)].sort_values(["kfg", "orden"]).reset_index(drop=True)

clase = pd.read_csv(r"..\n_no_numericos\quipus_clase.csv")
tally = set(clase.loc[clase["clase_limpia"] == 1, "kfg"]) if "clase_limpia" in clase else set()

blocks = []
for k, d in p.groupby("kfg"):
    d = d.sort_values("orden").reset_index(drop=True)
    colcodes = pd.Categorical(d.colfam.fillna("NA")).codes.astype(np.int64)
    grpcodes = pd.Categorical(d.grupo.fillna(-1).astype(str)).codes.astype(np.int64)
    blocks.append(dict(kfg=k, idx=d.index.values,
                       tw=d.twist.values.copy(),
                       val=d.valor.fillna(0).values.astype(float),
                       col=colcodes, grp=grpcodes,
                       tally=k in tally))


def stats_for(tw_list):
    tr = half = num = den = mic = mig = 0.0
    per_tr, per_half = {}, {}
    for b, tw in zip(blocks, tw_list):
        t = int(np.sum(tw[1:] != tw[:-1]))
        tr += t
        per_tr[b["kfg"]] = t
        h = 0
        for gid in np.unique(b["grp"]):
            m = b["grp"] == gid
            if m.sum() < 4:
                continue
            w = tw[m]
            if len(np.unique(w)) < 2:
                continue
            k = len(w) // 2
            a, z = w[:k], w[k:]
            if len(np.unique(a)) == 1 and len(np.unique(z)) == 1 and a[0] != z[0]:
                h += 1
        half += h
        per_half[b["kfg"]] = h
        z = tw == "Z"
        s = tw == "S"
        vz = np.log1p(b["val"][z & (b["val"] > 0)])
        vs = np.log1p(b["val"][s & (b["val"] > 0)])
        if len(vz) and len(vs):
            w = len(vz) * len(vs) / (len(vz) + len(vs))
            num += w * (vz.mean() - vs.mean())
            den += w
        mic += fast_mi(np.where(tw == "S", 0, 1).astype(np.int64), b["col"])
        mig += fast_mi(np.where(tw == "S", 0, 1).astype(np.int64), b["grp"])
    return dict(T1=tr, T2=half, T3=(num / den if den else np.nan),
                T4=mic, T5=mig), per_tr, per_half


def run(blocks):
    obs, ptr_obs, ph_obs = stats_for([b["tw"] for b in blocks])
    null = {k: [] for k in ["T1", "T2", "T3", "T4", "T5"]}
    ptr_null = {b["kfg"]: [] for b in blocks}
    ph_null = {b["kfg"]: [] for b in blocks}
    for it in range(B):
        tw_list = []
        for b in blocks:
            tw = b["tw"].copy()
            rng.shuffle(tw)
            tw_list.append(tw)
        st, ptr, ph = stats_for(tw_list)
        for k in null:
            null[k].append(st[k])
        for k in ptr:
            ptr_null[k].append(ptr[k])
            ph_null[k].append(ph[k])
    return obs, null, ptr_obs, ph_obs, ptr_null, ph_null


obs, null, ptr_obs, ph_obs, ptr_null, ph_null = run(blocks)
labels = {"T1": "transiciones S/Z (menos = bloques contiguos)",
          "T2": "grupos partidos en mitades S|Z",
          "T3": "log(valor Z) - log(valor S)",
          "T4": "MI(torsion; color)",
          "T5": "MI(torsion; grupo)"}
sides = {"T1": "less", "T2": "greater", "T3": "less", "T4": "greater", "T5": "greater"}
rows = []
for k in ["T1", "T2", "T3", "T4", "T5"]:
    d = describe(obs[k], null[k], sides[k])
    d.update(test=k, descripcion=labels[k], n_quipus=len(blocks), lado=sides[k])
    rows.append(d)

blocks_all = blocks
blocks = [b for b in blocks_all if not b["tally"]]
if len(blocks) >= 3:
    obs2, null2, *_ = run(blocks)
    for k in ["T1", "T2", "T3", "T4", "T5"]:
        d = describe(obs2[k], null2[k], sides[k])
        d.update(test=k + "_sin_tally", descripcion=labels[k] + " (sin clase tally)",
                 n_quipus=len(blocks), lado=sides[k])
        rows.append(d)

res = pd.DataFrame(rows)
res.to_csv("res_torsion.csv", index=False, encoding="utf-8-sig")

pq = []
for b in blocks_all:
    k = b["kfg"]
    p1 = (1 + np.sum(np.array(ptr_null[k]) <= ptr_obs[k])) / (1 + B)
    p2 = (1 + np.sum(np.array(ph_null[k]) >= ph_obs[k])) / (1 + B)
    pq.append(dict(kfg=k, n=len(b["tw"]), n_z=int(np.sum(b["tw"] == "Z")),
                   transiciones=ptr_obs[k], transiciones_nulas=float(np.mean(ptr_null[k])),
                   p_transiciones=p1, mitades=ph_obs[k], p_mitades=p2,
                   clase_tally=k in tally))
pd.DataFrame(pq).to_csv("torsion_por_quipu.csv", index=False, encoding="utf-8-sig")
print(res.round(4).to_string())
print("\nPor quipu:")
print(pd.DataFrame(pq).sort_values("p_transiciones").head(13).round(4).to_string())
