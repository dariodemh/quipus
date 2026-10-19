# -*- coding: utf-8 -*-
"""ATAQUE 2 (v2): potencia de las pruebas de 'no hay lexico de color compartido'.

Planta un lexico de 4 colores en el 30 % / 10 % de los quipus de Pachacamac
(el sitio mas grande, 80 quipus: escenario favorable) y mide la potencia de
  P1: orden de categorias (Kendall tau mismo sitio vs distinto)
  P2: secuencias de color de grupo repetidas entre quipus

Plantas:
  fuerte     : 4 bloques en orden fijo (sobreescribe el color)
  orden      : reordena dentro de cada grupo los colores existentes segun el lexico
  orden_ruido: idem con 30 % de posiciones barajadas
"""
import re
import itertools
from collections import defaultdict
import numpy as np
import pandas as pd

rng = np.random.default_rng(20261018)
RAIZ = r"."
c = pd.read_csv(RAIZ + "/analisis/datos/cuerdas.csv", low_memory=False)
q = pd.read_csv(RAIZ + "/analisis/datos/quipus.csv")
prov = q.set_index("kfg").procedencia.astype(str).to_dict()
p = c[(c.nivel == 0) & c.color.notna()].copy()
p["col"] = p.color.astype(str).map(lambda s: re.sub(r"\([^)]*\)", "", s))
p = p.sort_values(["kfg", "orden"]).reset_index(drop=True)

n = p.groupby("kfg").size()
ks = [k for k in n[n >= 10].index if prov.get(k, "Unknown") not in ("Unknown", "nan")]
base = p[p.kfg.isin(ks)].copy().reset_index(drop=True)
SITIO = "Pachacamac"
qsitio = [k for k in ks if prov[k] == SITIO]
LEX = list(base[base.kfg.isin(qsitio)].col.value_counts().index[:4])
print("quipus:", len(ks), "| Pachacamac:", len(qsitio), "| lexico:", LEX)

lab = np.array([prov[k] for k in ks])
idx = {k: i for i, k in enumerate(ks)}


def ktau(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = len(x)
    if m < 3:
        return np.nan
    iu = np.triu_indices(m, 1)
    dx = (x[:, None] - x[None, :])[iu]
    dy = (y[:, None] - y[None, :])[iu]
    conc = np.sum((dx * dy) > 0)
    disc = np.sum((dx * dy) < 0)
    n0 = m * (m - 1) / 2
    den = np.sqrt((n0 - np.sum(dx == 0)) * (n0 - np.sum(dy == 0)))
    return (conc - disc) / den if den > 0 else np.nan


def posiciones(tab):
    pos = {}
    for k, g in tab.groupby("kfg"):
        s = g.col.tolist()
        nn = len(s)
        d = {}
        for i, x in enumerate(s):
            d.setdefault(x, []).append(i / (nn - 1))
        pos[k] = {x: np.mean(v) for x, v in d.items()}
    return pos


def lista_pares(pos):
    """Pares fijos (los del corpus base, con >=4 colores comunes alli)."""
    pares = []
    for a, b in itertools.combinations(ks, 2):
        sh = [x for x in pos[a] if x in pos[b]]
        if len(sh) >= 4:
            pares.append((a, b))
    return pares


POS0 = posiciones(base)
PARES = lista_pares(POS0)
print("pares P1:", len(PARES))


def taus(pos, pares):
    out = np.empty(len(pares))
    for j, (a, b) in enumerate(pares):
        sh = [x for x in pos[a] if x in pos[b]]
        out[j] = ktau([pos[a][x] for x in sh], [pos[b][x] for x in sh]) if len(sh) >= 4 else np.nan
    return out


# cache: los pares que no tocan un quipu plantado no cambian
POS_POR_QUIPU = {k: posiciones(base[base.kfg == k])[k] for k in ks}
TAU0 = taus(POS0, PARES)
ia = np.array([idx[a] for a, b in PARES])
ib = np.array([idx[b] for a, b in PARES])
print("mismos sitio:", int((lab[ia] == lab[ib]).sum()))


def stat(l, tau):
    same = l[ia] == l[ib]
    return np.nanmean(tau[same]) - np.nanmean(tau[~same])


def pval1(l, tau, nperm=100):
    o = stat(l, tau)
    cnt = sum(stat(rng.permutation(l), tau) >= o for _ in range(nperm))
    return o, (cnt + 1) / (nperm + 1)


def grupos_de(tab):
    return [(k, g2.col.tolist()) for (k, _), g2 in tab.groupby(["kfg", "grupo"])
            if 3 <= len(g2) <= 12]


def compartidos(gr):
    d = defaultdict(set)
    for k, s in gr:
        if len(set(s)) >= 2:
            d[tuple(s)].add(k)
    return sum(len(v) for v in d.values() if len(v) >= 2)


def pval2(gr, nperm=100):
    o = compartidos(gr)
    cnt = 0
    for _ in range(nperm):
        if compartidos([(k, list(rng.permutation(s))) for k, s in gr]) >= o:
            cnt += 1
    return o, (cnt + 1) / (nperm + 1)


def planta_fuerte(quipus):
    out = base.copy()
    for k in quipus:
        m = out.kfg == k
        nk = int(m.sum())
        cc = []
        for j, col in enumerate(LEX):
            cc += [col] * (nk // 4 + (1 if j < nk % 4 else 0))
        out.loc[m, "col"] = cc[:nk]
    return out


def planta_orden(quipus, ruido=0.0):
    out = base.copy()
    rank = {x: i for i, x in enumerate(LEX)}
    for k in quipus:
        for u, g in out[out.kfg == k].groupby("grupo"):
            cols = g.col.tolist()
            orden = sorted(cols, key=lambda x: (rank.get(x, 10), x))
            if ruido > 0:
                m = rng.random(len(orden)) < ruido
                vals = orden.copy()
                rng.shuffle(vals)
                for j in np.where(m)[0]:
                    orden[j] = vals[j]
            out.loc[g.index, "col"] = orden
    return out


o1, p1 = pval1(lab, TAU0, 200)
o2, p2 = pval2(grupos_de(base), 150)
print(f"REAL: P1 dif={o1:.4f} p={p1:.4f} | P2 compartidos={o2} p={p2:.4f}")

NSIM = 60
filas = []
for frac in (0.30, 0.10):
    for modo in ("fuerte", "orden", "orden_ruido"):
        det1 = det2 = 0
        e1, e2 = [], []
        for s in range(NSIM):
            kk = list(rng.choice(qsitio, size=max(2, int(round(frac * len(qsitio)))), replace=False))
            tab = (planta_fuerte(kk) if modo == "fuerte"
                   else planta_orden(kk, 0.0 if modo == "orden" else 0.3))
            pos = dict(POS_POR_QUIPU)
            for k in kk:
                pos[k] = posiciones(tab[tab.kfg == k])[k]
            tau = TAU0.copy()
            toca = np.array([(a in kk) or (b in kk) for a, b in PARES])
            jj = np.where(toca)[0]
            tau[jj] = taus(pos, [PARES[j] for j in jj])
            a1, q1 = pval1(lab, tau, 100)
            a2, q2 = pval2(grupos_de(tab), 100)
            det1 += q1 < 0.05
            det2 += q2 < 0.05
            e1.append(a1)
            e2.append(a2)
        filas.append(dict(frac=frac, modo=modo, potencia_P1=det1 / NSIM,
                          potencia_P2=det2 / NSIM, efecto_P1=round(float(np.nanmedian(e1)), 4),
                          efecto_P2=float(np.median(e2))))
        print(filas[-1], flush=True)
        pd.DataFrame(filas).to_csv(RAIZ + "/analisis/ds/n_rojo_formulario/potencia_lexico.csv", index=False)
print(pd.DataFrame(filas).to_string(index=False))
