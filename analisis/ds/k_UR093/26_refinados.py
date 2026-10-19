# -*- coding: utf-8 -*-
"""UR093: tests refinados (suma informativa, correlacion, posicion del maximo,
alineacion de nudos). Nulo: 1000 permutaciones, seed 0, dentro del quipu."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
val = u.valor.values; name = u.cuerda.values; nivel = u.nivel.values
V = dict(zip(name, val)); padre = dict(zip(name, u.padre))
l0 = u[u.nivel == 0].copy(); l1 = u[u.nivel == 1].copy()
l1['pos'] = l1.groupby('padre').cumcount() + 1
l2 = u[u.nivel == 2]
child = {}
for c in u.cuerda:
    if pd.notna(padre[c]): child.setdefault(padre[c], []).append(c)
def subtree(c, VV):
    return VV[c] + sum(subtree(k, VV) for k in child.get(c, []))
groups = {g: grp.cuerda.tolist() for g, grp in l0.groupby('grupo')}
subs_p = {p: child.get(p, []) for p in l0.cuerda}

def stats(vals):
    VV = dict(zip(name, vals)); r = {}
    # suma informativa: solo pendantes con >=2 hijas no nulas o suma>=2, excluye 1=1
    hits = tot = 0
    for p in l0.cuerda:
        if p not in child: continue
        s = sum(subtree(k, VV) for k in child[p])
        if s >= 2 or VV[p] >= 2:
            tot += 1
            if VV[p] == s: hits += 1
    r['suma_informativa'] = hits
    # correlacion de Spearman entre valor del colgante y suma de subsidiarias (solo con suma>0)
    a, b = [], []
    for p in l0.cuerda:
        if p in child:
            s = sum(subtree(k, VV) for k in child[p])
            if s > 0:
                a.append(VV[p]); b.append(s)
    r['spearman'] = pd.Series(a).corr(pd.Series(b), method='spearman')
    # posicion del maximo dentro del grupo (1..n); estadistico: cuantos grupos lo tienen en las 3 primeras
    r['max_top3'] = sum(1 for g, cs in groups.items() if cs and int(np.argmax([VV[c] for c in cs])) < 3)
    # cuantos grupos tienen el maximo en la posicion 1 o 2
    r['max_top2'] = sum(1 for g, cs in groups.items() if cs and int(np.argmax([VV[c] for c in cs])) < 2)
    # "pendiente": correlacion entre posicion y valor dentro de grupos
    rhos = []
    for g, cs in groups.items():
        if len(cs) >= 5:
            rhos.append(pd.Series(range(len(cs))).corr(pd.Series([VV[c] for c in cs]), method='spearman'))
    r['rho_pos_medio'] = np.nanmean(rhos)
    return r

obs = stats(val)
print('observado:', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in obs.items()})
rng = np.random.default_rng(0); nperm = 1000; rows = []
for it in range(nperm):
    v2 = val.copy()
    if it % 2 == 0:
        rng.shuffle(v2)
    else:
        for lv in (0, 1, 2):
            idx = np.where(nivel == lv)[0]; v2[idx] = rng.permutation(v2[idx])
    rows.append(stats(v2))
N = pd.DataFrame(rows)
print('\n== nulo ==')
from scipy.stats import rankdata
for k in obs:
    nl = N[k].dropna().values
    o = obs[k]
    if k == 'rho_pos_medio':
        p = (1 + (np.abs(nl) >= abs(o)).sum()) / (len(nl) + 1)
    else:
        p = (1 + (nl >= o).sum()) / (len(nl) + 1)
    print(f'{k:18s} obs={o:.3f} nulo={nl.mean():.3f} p={p:.4f}')

# ---------- alineacion de nudos (directo desde OKR: attach + start) ----------
import sqlite3
print('\n== altura absoluta de los nudos (desde el cordon principal) ==')
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
cord = pd.read_sql("select CORD_ID, CORD_LEVEL, ATTACH_POS, CORD_LENGTH from cord where KHIPU_ID=1000321", con)
cord['tip'] = cord.ATTACH_POS + cord.CORD_LENGTH
kc = pd.read_sql("""select kc.CORD_ID, kc.START_POS from knot_cluster kc
                    join cord c on kc.CORD_ID=c.CORD_ID where c.KHIPU_ID=1000321""", con)
ah = kc.merge(cord, on='CORD_ID')
ah['h'] = ah.ATTACH_POS + ah.START_POS
print(ah.groupby('CORD_LEVEL').h.describe()[['count', 'mean', '50%', 'std', 'min', 'max']].round(1).to_string())
print('\n== altura de las puntas (attach + largo) ==')
print(cord.groupby('CORD_LEVEL').tip.describe()[['count', 'mean', '50%', 'std']].round(1).to_string())
