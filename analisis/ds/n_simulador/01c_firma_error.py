# -*- coding: utf-8 -*-
"""Firma del error: ¿un solo nudo en un solo lugar decimal?

- digitos que cambian entre A+B y el destino
- nulo: destinos aleatorios del pool
- nº de racimos de las cuerdas implicadas -> tasa por racimo
- estabilidad de las 9 columnas (mitades de UR278)
- Fisher: fidelidad del enlace derivado (UR270->UR278) vs independiente (A+B->libro)
"""
import json
import re
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_simulador"
rng = np.random.default_rng(20261018)
P = pd.read_csv(OUT + r"\perfil_ab.csv")
D = json.load(open(OUT + r"\datos_reales.json", encoding="utf-8"))

# ---------- 1. digitos que cambian ----------
def digitos(n, k=5):
    return [int(x) for x in str(int(n)).zfill(k)[-k:]]

def n_pos_diff(a, b):
    return sum(x != y for x, y in zip(digitos(a), digitos(b)))

mal = P[(P.absdif > 0) & P.destino.notna()].copy()
mal["pos_diff"] = [n_pos_diff(a, b) for a, b in zip(mal.suma, mal.val)]
mal["dif_digito"] = [abs(int(str(int(a)).zfill(5)[-1 - int(np.log10(abs(a - b)))]) -
                          int(str(int(b)).zfill(5)[-1 - int(np.log10(abs(a - b)))]) if a != b else 0)
                     for a, b in zip(mal.suma, mal.val)]
print("== fallos con destino ==")
print(mal[["reg", "suma", "val", "absdif", "pos_diff"]].to_string(index=False))
print("posiciones decimales que cambian:", mal.pos_diff.tolist())

# nulo: mismo suma, destino aleatorio del pool de cabeceras
pool = np.array([x["valor"] for q in D["cabeceras"] for x in D["cabeceras"][q]])
sim_pos, sim_pot = [], []
for _ in range(20000):
    a = int(rng.choice(mal.suma.values))
    b = int(rng.choice(pool))
    sim_pos.append(n_pos_diff(a, b))
    sim_pot.append(a != b and abs(a - b) > 0 and int(round(np.log10(abs(a - b)))) == np.log10(abs(a - b)))
sim_pos = np.array(sim_pos); sim_pot = np.array(sim_pot)
print("nulo posiciones que cambian: media", round(sim_pos.mean(), 2),
      "P(<=1 pos)", round((sim_pos <= 1).mean(), 3))
print("obs: 7/7 con 1 posicion -> p =", round((sim_pos <= 1).mean() ** 7, 6))
print("nulo P(dif = 10^k exacto):", round(sim_pot.mean(), 3),
      "obs 7/7 -> p =", sim_pot.mean() ** 7)

# ---------- 2. racimos por cuerda ----------
c = pd.read_csv(RAIZ + r"\analisis\datos\cuerdas.csv",
                usecols=["kfg", "orden", "nivel", "grupo", "valor", "nudos"], dtype={"nudos": str})
c["tiene"] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != "")
c["nrac"] = c.nudos.fillna("").apply(lambda s: len([x for x in str(s).split(";") if x.strip()]))
c["v"] = pd.to_numeric(c.valor, errors="coerce")

def buscar(kfg, val, tol=0):
    d = c[(c.kfg == kfg) & c.tiene & (np.abs(c.v - val) <= tol)]
    return d

rac = []
for _, r in P.iterrows():
    for col, kfg in [("A", "UR273A"), ("B", "UR273B")]:
        d = buscar(kfg, r[col])
        if len(d):
            d = d.iloc[0]
            rac.append((int(r.reg), col, kfg, float(d.v), int(d.nrac)))
rac = pd.DataFrame(rac, columns=["reg", "parte", "quipu", "valor", "nrac"])
print("\n== racimos en las cuerdas A/B localizadas ==", len(rac), "de 36")
print("racimos por cuerda: media", round(rac.nrac.mean(), 2), "mediana", int(rac.nrac.median()),
      "min", int(rac.nrac.min()), "max", int(rac.nrac.max()))
print("distribucion:", rac.nrac.value_counts().sort_index().to_dict())

# tasa por racimo que explica 8/18 (3 cuerdas por registro)
N = 3 * rac.nrac.mean()
q_rac = 1 - (8 / 15) ** (1 / N)
print(f"si el fallo es 1 racimo mal en A, B o C: N={N:.1f} racimos/registro, "
      f"q_racimo = {q_rac:.4f}")
q_cord = 1 - (8 / 15) ** (1 / 3)
print(f"si el fallo es de cuerda entera (modelo transcripcion): q_cuerda = {q_cord:.4f}")

# ---------- 3. Fisher: enlace derivado vs independiente ----------
print("\n== fidelidad por tipo de enlace ==")
print("A+B -> libro: 7/15 exactas (estructural) =", round(7 / 15, 3),
      "; 8/15 con el recuento de 13 =", round(8 / 15, 3))
print("UR270 -> UR278: 39/45 celdas +-1 =", round(39 / 45, 3))
tab = [[7, 8], [39, 6]]
odds, p = stats.fisher_exact(tab)
print("Fisher 2x2", tab, "p =", round(p, 5))

# ---------- 4. estabilidad de columnas de UR278 ----------
def matriz(kfg, j=9):
    d = c[(c.kfg == kfg) & (c.nivel == 0)].sort_values("orden")
    rows = []
    for gr, gg in d.groupby("grupo", sort=True):
        vv = list(gg.v)
        if len(vv) >= j and np.sum(~np.isnan(vv)) >= j:
            rows.append(vv[:j])
    return np.array(rows, float)

M = matriz("UR278")
h = len(M) // 2
m1, m2 = np.nanmean(M[:h], 0), np.nanmean(M[h:], 0)
print("\n== UR278 mitades ==", h, "y", len(M) - h, "filas")
print("medias 1ª mitad", m1.round(0).astype(int))
print("medias 2ª mitad", m2.round(0).astype(int))
print("Spearman de las 9 medias entre mitades:", round(stats.spearmanr(m1, m2).statistic, 3))
print("Pearson de las 9 medias:", round(np.corrcoef(m1, m2)[0, 1], 3))

res = dict(pos_diff=mal.pos_diff.tolist(), nrac_media=float(rac.nrac.mean()),
           q_racimo=float(q_rac), q_cuerda=float(q_cord),
           fisher_p=float(p), spearman_mitades=float(stats.spearmanr(m1, m2).statistic),
           p_pos1=float((sim_pos <= 1).mean() ** 7), p_pot=float(sim_pot.mean() ** 7))
json.dump(res, open(OUT + r"\firma_error.json", "w"), indent=1)
