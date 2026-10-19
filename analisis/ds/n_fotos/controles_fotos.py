# -*- coding: utf-8 -*-
"""Controles de la auditoría visual: sesgo de conteo, grupos KFG vs Databook,
cobertura de las fotos. Semilla fija; nulo de permutación."""
import numpy as np, pandas as pd
from scipy import stats
from pathlib import Path
import json

RNG = np.random.default_rng(42)
AQUI = Path(__file__).parent

# ---------- A. conteos visuales vs archivo ----------
# (quipu, visual, archivo, fuente, contable_plenamente)
C = [
 ("AS010", 23, 27, "KFG", 1), ("AS011", 15, 15, "KFG", 1), ("AS015", 13, 12, "KFG", 1),
 ("AS017", 22, 20, "KFG", 1), ("AS018", 9, 9, "KFG", 1), ("AS020", 10, 10, "KFG", 1),
 ("AS025", 2, 2, "KFG", 1), ("AS031", 52, 54, "Databook", 1), ("AS213", 19, 18, "KFG", 1),
 ("AS214", 20, 20, "KFG", 1), ("AS215", 28, 28, "KFG", 1),
 ("AS034", 95, 108, "Databook", 0), ("AS038", 110, 115, "Databook", 0),
 ("AS070", 95, 99, "Databook", 0), ("AS032", 175, 405, "Databook", 0),
 ("AS012", 35, 85, "KFG", 0), ("AS026", 330, 337, "KFG (A+B)", 0),
]
df = pd.DataFrame(C, columns=["quipu", "visual", "archivo", "fuente", "pleno"])

def rho_perm(x, y, n=20000):
    r = stats.spearmanr(x, y).statistic
    cnt = 0
    for _ in range(n):
        if abs(stats.spearmanr(x, RNG.permutation(y)).statistic) >= abs(r):
            cnt += 1
    return r, (cnt + 1) / (n + 1)

def slope_perm(x, y, n=20000):
    lx, ly = np.log10(x), np.log10(y)
    b = np.polyfit(lx, ly, 1)[0]
    cnt = 0
    for _ in range(n):
        if abs(np.polyfit(lx, RNG.permutation(ly), 1)[0]) >= abs(b):
            cnt += 1
    return b, (cnt + 1) / (n + 1)

res = {}
for nombre, sub in [("todos_n17", df), ("plenos_n11", df[df.pleno == 1])]:
    r, p = rho_perm(sub.visual.values, sub.archivo.values)
    b, pb = slope_perm(sub.visual.values, sub.archivo.values)
    ratio = sub.visual / sub.archivo
    res[nombre] = dict(n=len(sub), spearman=round(float(r), 3), p_perm=round(float(p), 5),
                       pendiente_loglog=round(float(b), 3), p_pendiente=round(float(pb), 5),
                       ratio_mediana=round(float(np.median(ratio)), 3),
                       ratio_min=round(float(ratio.min()), 3), ratio_max=round(float(ratio.max()), 3))

# sesgo por tamaño: mediana del ratio en quipus <=30 vs >30
peq = df[df.archivo <= 30]; gran = df[df.archivo > 30]
res["sesgo_tamano"] = dict(n_peq=len(peq), ratio_peq=round(float((peq.visual/peq.archivo).median()), 3),
                           n_gran=len(gran), ratio_gran=round(float((gran.visual/gran.archivo).median()), 3))

# ---------- B. grupos: KFG vs Databook ----------
G = [
 ("AS010", 13, 9), ("AS011", 2, 2), ("AS012", 7, 6), ("AS015", 3, 3), ("AS017", 2, 2),
 ("AS018", 1, 1), ("AS020", 2, 2), ("AS025", 2, 2), ("AS048", 12, 12), ("AS059", 2, 2),
 ("AS069", 432, 204), ("AS212", 13, 13), ("AS213", 1, 1), ("AS214", 6, 6),
 ("AS215", 11, 10), ("AS036", 9, 9), ("AS037", 7, 7),
]
g = pd.DataFrame(G, columns=["quipu", "kfg", "db"])
g["dif"] = g.kfg - g.db
g["absdif"] = g["dif"].abs()
obs_exact = float((g["dif"] == 0).mean())
obs_1 = float((g["absdif"] <= 1).mean())
obs_mae = float(g["absdif"].mean())
# nulo: emparejar cada KFG con el grupo DB de otro quipu (permutación)
cnt_exact = cnt_1 = 0; maes = []
for _ in range(20000):
    d = g.kfg.values - RNG.permutation(g.db.values)
    cnt_exact += (d == 0).sum()
    cnt_1 += (np.abs(d) <= 1).sum()
    maes.append(np.abs(d).mean())
p_exact = (cnt_exact / 20000 / len(g))
# p para el nº de aciertos exactos: proporción de permutaciones con >= observado
perm_exact = []
for _ in range(5000):
    d = g.kfg.values - RNG.permutation(g.db.values)
    perm_exact.append((d == 0).mean())
p_exact = (np.sum(np.array(perm_exact) >= obs_exact) + 1) / 5001
perm_mae = []
for _ in range(5000):
    perm_mae.append(np.abs(g.kfg.values - RNG.permutation(g.db.values)).mean())
p_mae = (np.sum(np.array(perm_mae) <= obs_mae) + 1) / 5001

res["grupos"] = dict(n=len(g), exactos=int((g["dif"] == 0).sum()), pct_exacto=round(obs_exact, 3),
                     pct_pm1=round(obs_1, 3), mae=round(obs_mae, 2), p_exacto=round(float(p_exact), 5),
                     p_mae=round(float(p_mae), 5),
                     mediana_dif=float(g["dif"].median()))
# Holm para 2 pruebas de grupos
ps = sorted([p_exact, p_mae]); holm = [min(1, ps[0]*2), min(1, max(ps[0]*2, ps[1]))]
res["grupos"]["holm"] = [round(float(x), 5) for x in holm]

# ---------- C. cobertura de las fotos ----------
aud = pd.read_csv(AQUI / "auditoria_fotos.csv", sep=";", encoding="utf-8-sig")
aud["n_colgantes_aprox"] = aud["n_colgantes_aprox"].fillna("").astype(str).str.strip()
res["cobertura"] = dict(fotos=len(aud), quipus_distintos=int(aud.quipu.nunique()),
                        filas_sin_conteo=int((aud.n_colgantes_aprox == "").sum()),
                        filas_con_conteo=int((aud.n_colgantes_aprox != "").sum()),
                        cuadra_si=int((aud.cuadra_con_KFG == "sí").sum()),
                        cuadra_parcial=int((aud.cuadra_con_KFG == "parcial").sum()),
                        no_aplica=int(aud.cuadra_con_KFG.str.startswith("n/a").sum()))

print(json.dumps(res, ensure_ascii=False, indent=2))
(AQUI / "controles_fotos.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
g.to_csv(AQUI / "grupos_kfg_vs_databook.csv", index=False, sep=";", encoding="utf-8-sig")
df.to_csv(AQUI / "conteos_visuales_vs_archivo.csv", index=False, sep=";", encoding="utf-8-sig")
