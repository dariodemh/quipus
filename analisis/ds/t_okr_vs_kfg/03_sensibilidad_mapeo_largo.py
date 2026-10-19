# -*- coding: utf-8 -*-
"""EXPLORACION DESCARTADA: correspondencia fisica KFG<->OKR por largo.

Emparejar por largo dentro de cada grupo de hermanos falla cuando muchas cuerdas
comparten largos casi identicos (Hungarian elige mal y la concordancia cae de 98%
a 82%). Se conserva como evidencia de que el mapeo por nombre jerarquico (02) es
superior. NO se usa para las cifras del informe.
"""
import os, re
import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
from importlib import import_module

m = import_module("01_mapeo")
ROOT = m.ROOT; OUT = m.OUT
SAL = os.path.join(OUT, "salidas")

RE_NUDO = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\),([\d.]+)")


def parsear_nudos(s):
    if not isinstance(s, str) or not s.strip():
        return np.nan, 0, np.nan
    total = 0.0; n = 0; pos1 = np.nan
    for i, racimo in enumerate(s.split(";")):
        mm = RE_NUDO.search(racimo.strip())
        if not mm:
            continue
        if i == 0:
            pos1 = float(mm.group(3))
        total += float(mm.group(5))
        n += int(mm.group(1))
    return total, n, pos1


def reconstruir(knot):
    kn = knot.copy()
    kn["val"] = pd.to_numeric(kn.knot_value_type, errors="coerce").fillna(0)
    falta = (kn.val <= 0) & kn.TYPE_CODE.isin(["L", "LL"]) & (kn.NUM_TURNS > 0)
    kn.loc[falta, "val"] = kn.loc[falta, "NUM_TURNS"]
    val = kn.groupby("CORD_ID")["val"].sum().rename("valor_okr")
    nkn = kn.groupby("CORD_ID").size().rename("n_nudos_okr")
    return pd.concat([val, nkn], axis=1).reset_index()


def construir_okr():
    km, cord, knot, kc = m.cargar()
    mp = pd.read_csv(os.path.join(SAL, "mapa_quipus.csv")).dropna(subset=["KHIPU_ID"])
    mp["KHIPU_ID"] = mp.KHIPU_ID.astype(int)
    rec = reconstruir(knot)
    okr = cord.merge(rec, on="CORD_ID", how="left")[["KHIPU_ID", "CORD_ID", "PENDANT_FROM",
                                                      "CORD_ORDINAL", "CORD_LEVEL", "ATTACH_POS",
                                                      "CORD_LENGTH", "valor_okr", "n_nudos_okr"]]
    okr["valor_okr"] = okr.valor_okr.fillna(0)
    okr["n_nudos_okr"] = okr.n_nudos_okr.fillna(0).astype(int)
    # nivel efectivo (los niveles negativos son colgantes/cuerdas superiores)
    okr["nivel_fis"] = np.where(okr.CORD_LEVEL > 0, okr.CORD_LEVEL, okr.CORD_LEVEL + 1)
    return okr, mp


def emparejar_grupo(gk, go):
    """Hungarian por |delta largo| + 0.5*|delta nudos|; devuelve pares (filas)."""
    if len(gk) == 0 or len(go) == 0:
        return []
    A = gk.largo.fillna(-99).values[:, None]
    B = go.CORD_LENGTH.fillna(-99).values[None, :]
    dl = np.abs(A - B)
    dn = np.abs(gk.n_nudos_kfg.fillna(0).values[:, None] - go.n_nudos_okr.fillna(0).values[None, :])
    cost = 10.0 * dl + 0.5 * dn
    cost = np.where(dl > 2.0, cost + 500, cost)
    ri, ci = linear_sum_assignment(cost)
    out = []
    for i, j in zip(ri, ci):
        out.append((i, j, dl[i, j], dn[i, j]))
    return out


def main():
    okr, mp = construir_okr()
    kfg = pd.read_csv(m.CUERDAS)
    # quitar filas duplicadas exactas del propio KFG
    kfg = kfg.drop_duplicates(subset=["kfg", "orden", "cuerda", "largo", "nudos"]).copy()
    pp = kfg.nudos.apply(parsear_nudos)
    kfg["valor_parseado"] = [x[0] for x in pp]
    kfg["n_nudos_kfg"] = [x[1] for x in pp]
    kfg["pos1_kfg"] = [x[2] for x in pp]
    kfg["valor"] = kfg.valor.fillna(0)

    pares = []
    for kfg_id, gk in kfg.groupby("kfg"):
        hit = mp[mp.kfg == kfg_id]
        if hit.empty:
            continue
        kid = int(hit.KHIPU_ID.iloc[0])
        go_all = okr[okr.KHIPU_ID == kid]
        if go_all.empty:
            continue
        # nivel 0: colgantes (hijos de la raiz principal / raices)
        ids = set(go_all.CORD_ID)
        roots = go_all[~go_all.PENDANT_FROM.isin(ids)]
        # solo los colgantes del nivel efectivo 0 y nivel 1 negativo
        top = roots.copy()
        # recorrido iterativo
        cola = [(gk[gk.padre.isna()], top)]
        vistos = set()
        while cola:
            gk_g, go_g = cola.pop()
            asg = emparejar_grupo(gk_g, go_g)
            for i, j, dl, dn in asg:
                rk = gk_g.iloc[i]; ro = go_g.iloc[j]
                pares.append(dict(kfg=kfg_id, cuerda=rk.cuerda, valor=rk.valor,
                                  valor_parseado=rk.valor_parseado, nudos=rk.nudos,
                                  n_nudos_kfg=rk.n_nudos_kfg, largo=rk.largo, orden=rk.orden,
                                  nivel=rk.nivel, padre=rk.padre,
                                  CORD_ID=int(ro.CORD_ID), CORD_LENGTH=ro.CORD_LENGTH,
                                  valor_okr=ro.valor_okr, n_nudos_okr=ro.n_nudos_okr,
                                  dlargo=dl, dnudos=dn))
                hijos_k = gk[gk.padre == rk.cuerda]
                hijos_o = go_all[go_all.PENDANT_FROM == ro.CORD_ID]
                if len(hijos_k) and len(hijos_o):
                    cola.append((hijos_k, hijos_o))
    j = pd.DataFrame(pares)
    j = j.merge(kfg[["kfg", "cuerda", "valor_parseado", "n_nudos_kfg"]], on=["kfg", "cuerda"],
                how="left", suffixes=("", "_y"))
    j["kfg_ausente"] = j.nudos.isna()
    j["coincide"] = np.isclose(j.valor, j.valor_okr)
    j["coincide_parseado"] = np.isclose(j.valor_parseado_y.fillna(0), j.valor_okr)
    j.to_csv(os.path.join(SAL, "join_fisico.csv"), index=False)
    print("pares:", len(j), "quipus:", j.kfg.nunique(),
          "|dlargo|<=0.51:", round((j.dlargo <= 0.51).mean(), 4))
    print("match valor:", round(j.coincide.mean(), 4),
          "| excl sin nudos:", round(j[~j.kfg_ausente].coincide.mean(), 4))
    sub = j[(~j.coincide) & (~j.kfg_ausente)]
    print("desacuerdos:", len(sub))
    print(sub.head(20)[["kfg", "cuerda", "valor", "nudos", "valor_okr", "largo", "CORD_LENGTH", "dlargo"]].to_string())


if __name__ == "__main__":
    main()
