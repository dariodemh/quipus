# -*- coding: utf-8 -*-
"""UR093: seriacion, patrones repetidos, razones, bloque R/V y punto unico de union."""
import pandas as pd, numpy as np, sqlite3, re
from scipy.stats import spearmanr, hypergeom
from collections import Counter
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
l0 = u[u.nivel == 0]; l1 = u[u.nivel == 1].copy()
l1['pos'] = l1.groupby('padre').cumcount() + 1

# --- seriacion dentro del modulo de 8 ---
mods = [g.sort_values('pos').valor.tolist() for p, g in l1.groupby('padre') if len(g) >= 7]
rhos = [spearmanr(range(len(m)), m).statistic for m in mods if len(set(m)) > 1]
obs = np.nanmean(rhos)
rng = np.random.default_rng(0); null = []
for _ in range(1000):
    rr = []
    for m in mods:
        mm = rng.permutation(m)
        if len(set(mm)) > 1:
            rr.append(spearmanr(range(len(mm)), mm).statistic)
    null.append(np.nanmean(rr))
null = np.array(null)
print('seriacion: rho medio =', round(obs, 3), '| modulos con rho<0:', sum(1 for r in rhos if r < 0), '/', len(rhos),
      '| p =', round((1 + (null <= obs).sum()) / 1001, 4))
print('decrecientes exactos:', sum(all(a >= b for a, b in zip(m, m[1:])) for m in mods),
      '| crecientes exactos:', sum(all(a <= b for a, b in zip(m, m[1:])) for m in mods))

# --- patrones repetidos ---
mods8 = {p: tuple(g.sort_values('pos').valor.tolist()) for p, g in l1.groupby('padre') if len(g) == 8}
cnt = Counter(mods8.values())
print('\nmodulos de 8:', len(mods8), '| patrones distintos:', len(cnt),
      '| todo-cero:', sum(1 for v in mods8.values() if sum(v) == 0))
print('top patrones:', cnt.most_common(6))

# --- razones por grupo ---
print('\nrazon suma colgantes / suma subsidiarias por grupo:')
for g, grp in u.groupby('grupo'):
    pc = grp[grp.nivel == 0].valor.sum(); ps = grp[grp.nivel == 1].valor.sum()
    print(' ', g, round(pc / ps, 2) if ps else 'NA', f'({pc}/{ps})')
print('global:', round(l0.valor.sum() / l1.valor.sum(), 2))

# --- R/V: bloque 6-7 ---
print('\nR/V en nivel 1 por grupo:')
t = pd.crosstab(l1.grupo, l1.union)
print(t.to_string())
for g, k, n in [(6, 88, 88), (7, 91, 93)]:
    print('grupo', g, 'p hipergeometrico =', hypergeom.sf(k - 1, 956, 189, n))

# --- punto unico de union ---
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
cord = pd.read_sql("select CORD_ID, CORD_LEVEL, ATTACH_POS, PENDANT_FROM from cord where KHIPU_ID=1000321", con)
l2 = cord[cord.CORD_LEVEL == 2]
print('\ncolgantes con >=8 subsidiarias:', l2.PENDANT_FROM.value_counts().ge(8).sum(),
      '| alturas de union distintas por colgante:', l2.groupby('PENDANT_FROM').ATTACH_POS.nunique().value_counts().to_dict())
print('mediana de ATTACH_POS de subsidiarias:', l2.ATTACH_POS.median(),
      '| rango:', (l2.ATTACH_POS.min(), l2.ATTACH_POS.max()))

# --- "algun colgante = suma del resto de su grupo" (control de posicion) ---
groups = {g: grp.valor.tolist() for g, grp in l0.groupby('grupo')}
def anypos(gs):
    n = 0
    for vs in gs:
        for i, v in enumerate(vs):
            if v > 0 and v == sum(vs[:i] + vs[i+1:]):
                n += 1; break
    return n
obs = anypos(groups.values())
rng = np.random.default_rng(0); sim = []
for _ in range(1000):
    sim.append(anypos([list(rng.permutation(vs)) for vs in groups.values()]))
sim = np.array(sim)
print('\ngrupo con algun colgante = suma del resto: obs', obs, '/12 | nulo', round(sim.mean(), 2),
      '| p', round((1 + (sim >= obs).sum()) / 1001, 4))
