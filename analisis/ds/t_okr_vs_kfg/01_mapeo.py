# -*- coding: utf-8 -*-
"""Mapeo KFG <-> OKR a nivel de cuerda y reconstruccion de valores OKR.
Solo lectura de datos. Guarda resultados en salidas/.
"""
import os, sqlite3
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg")
os.makedirs(os.path.join(OUT, "salidas"), exist_ok=True)
DB = os.path.join(ROOT, "data", "external", "open-khipu-repository", "data", "khipu.db")
CUERDAS = os.path.join(ROOT, "analisis", "datos", "cuerdas.csv")
QUIPUS = os.path.join(ROOT, "analisis", "datos", "quipus.csv")


def cargar():
    con = sqlite3.connect(DB)
    km = pd.read_sql("select KHIPU_ID,OKR_NUM,INVESTIGATOR_NUM from khipu_main", con)
    cord = pd.read_sql("select KHIPU_ID,CORD_ID,PENDANT_FROM,CORD_ORDINAL,CORD_LEVEL,"
                       "ATTACH_POS,CORD_LENGTH,INVESTIGATOR_CORD_NUM from cord", con)
    knot = pd.read_sql("select CORD_ID,TYPE_CODE,DIRECTION,knot_value_type,NUM_TURNS,"
                       "KNOT_ORDINAL,CLUSTER_ORDINAL,CLUSTER_ID from knot", con)
    kc = pd.read_sql("select CORD_ID,CLUSTER_ID,ORDINAL,TOTAL_VALUE,NUM_KNOTS from knot_cluster", con)
    con.close()
    return km, cord, knot, kc


def mapear_quipus(km, qu):
    """Devuelve tabla kfg -> KHIPU_ID. Usa okr (KH...) o INVESTIGATOR_NUM."""
    km = km.copy()
    # normalizar investigador: puede ser 'AS031/UR1031/UR044'
    km["inv_list"] = km.INVESTIGATOR_NUM.fillna("").str.upper().str.split("/")
    inv_map = {}
    for _, r in km.iterrows():
        for inv in r.inv_list:
            inv = inv.strip()
            if inv:
                inv_map.setdefault(inv, []).append(r.KHIPU_ID)
    out = []
    for _, q in qu.iterrows():
        kfg = q.kfg.upper().strip()
        okr = str(q.okr).strip().upper()
        kid = None
        via = ""
        if okr.startswith("KH"):
            hit = km[km.OKR_NUM == okr]
            if len(hit) >= 1:
                kid = int(hit.KHIPU_ID.iloc[0]); via = "KH"
        if kid is None and kfg in inv_map:
            # si hay varias, elegir la de investigador exacto
            cands = inv_map[kfg]
            kid = int(cands[0]); via = "INV"
        out.append((q.kfg, q.okr, kid, via))
    return pd.DataFrame(out, columns=["kfg", "okr", "KHIPU_ID", "via"])


def nombres_cuerdas(cords):
    """Genera nombres jerarquicos p1, p1s1... recorriendo hijos por CORD_ORDINAL.
    En OKR los niveles -1 y -2 son colgantes/cuerdas superiores (nivel 0/1).
    Devuelve DataFrame CORD_ID, cuerda, nivel, padre, orden_global."""
    ids = set(cords.CORD_ID)
    lvl = dict(zip(cords.CORD_ID, [int(x) for x in cords.CORD_LEVEL.fillna(0)]))
    children = {}
    for _, r in cords.iterrows():
        p = r.PENDANT_FROM
        children.setdefault(p, []).append((int(r.CORD_ORDINAL) if pd.notna(r.CORD_ORDINAL) else 10**9,
                                           int(r.CORD_ID)))
    for p in children:
        children[p].sort()
    roots = [p for p in children if p not in ids]
    # raiz principal = la que tiene mas hijos; las demas se agregan al final
    if len(roots) > 1:
        roots.sort(key=lambda p: -len(children[p]))
    res = []
    orden = 0

    def walk(parent, prefix, nivel, padre_nombre, start=1):
        nonlocal orden
        for i, (_, cid) in enumerate(children.get(parent, []), start=start):
            name = f"p{i}" if nivel == 0 else f"{prefix}s{i - start + 1}"
            res.append((cid, name, nivel, padre_nombre, orden))
            orden += 1
            walk(cid, name, nivel + 1, name)

    # recorrido normal desde la raiz principal
    if roots:
        walk(roots[0], "", 0, None)
        ntop = len(children[roots[0]])
        # raices huerfanas/adicionales: continuar la numeracion de colgantes
        for r in roots[1:]:
            walk(r, "", 0, None, start=ntop + 1)
            ntop += len(children[r])
    return pd.DataFrame(res, columns=["CORD_ID", "cuerda", "nivel", "padre", "orden"])


if __name__ == "__main__":
    km, cord, knot, kc = cargar()
    qu = pd.read_csv(QUIPUS)
    mp = mapear_quipus(km, qu)
    print("quipus KFG:", len(mp), "mapeados:", mp.KHIPU_ID.notna().sum())
    print(mp.via.value_counts(dropna=False).to_string())
    print(mp[mp.KHIPU_ID.isna()].head(20).to_string())
    mp.to_csv(os.path.join(OUT, "salidas", "mapa_quipus.csv"), index=False)
