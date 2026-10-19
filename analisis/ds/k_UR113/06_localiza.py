# -*- coding: utf-8 -*-
"""UR113: localizacion por grupo de las sumas madre=hijas y de las corridas, con nulo
dentro de cada grupo y correccion de Holm."""
import pandas as pd, numpy as np, os
BASE = r'.'; OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
rng = np.random.default_rng(0)
u = pd.read_csv(os.path.join(OUT, 'cuerdas_ur113.csv')); u['valor'] = u.valor.fillna(0)
p = u[u.nivel == 0].copy(); s = u[u.nivel > 0].copy()
h = s.groupby('padre').agg(sumh=('valor', 'sum'), nh=('valor', 'size'))
m = p.merge(h, left_on='cuerda', right_index=True)
m = m[m.nh > 0].copy(); m['dif'] = m.valor - m.sumh
m['exact'] = (m.dif == 0).astype(int)

# --- nulo dentro de cada grupo: barajar valores de las hijas dentro del grupo
N = 2000
res = []
for gi, G in m.groupby('grupo'):
    if len(G) < 3: continue
    obs = int(G.exact.sum())
    subs_g = s[s.grupo == gi]
    vals = subs_g.valor.values
    cnt = []
    for _ in range(N):
        perm = rng.permutation(vals)
        sg = pd.Series(perm, index=subs_g.index).groupby(subs_g.padre.values).sum()
        cnt.append(int((G.valor.values == G.cuerda.map(sg).fillna(-1).values).sum()))
    cnt = np.array(cnt)
    pv = (np.sum(cnt >= obs) + 1) / (N + 1)
    res.append(dict(grupo=gi, madres=len(G), exactas=obs, exp=cnt.mean(), p=pv,
                    frac=round(obs / len(G), 2), mae=round(G.dif.abs().mean(), 1)))
R = pd.DataFrame(res)
# Holm
from scipy.stats import false_discovery_control
R['q_bh'] = false_discovery_control(R.p.values, method='bh')
R = R.sort_values('p')
print(R.round(4).to_string(index=False))
R.to_csv(os.path.join(OUT, 'sumas_por_grupo.csv'), index=False)

# --- corridas: detalle
runs = pd.read_csv(os.path.join(OUT, 'corridas.csv'))
p2 = p.copy(); p2['color'] = p2.color.fillna('NA')
for gi, G in p2.groupby('grupo'):
    G = G.reset_index(drop=True)
    for i in range(2, len(G)):
        t = G.loc[i, 'valor']
        if t == 0: continue
        for klen in range(2, min(10, i) + 1):
            seg = G.loc[i - klen:i - 1]
            if abs(seg.valor.sum() - t) < 0.5:
                print(f"  {G.loc[i,'cuerda']:>5} g{gi:>2} v={int(t):>4} = suma de {klen} previos "
                      f"{list(seg.valor.astype(int))} colores {list(seg.color)} -> propio {G.loc[i,'color']}")
                break

# --- madre = hija unica (casos triviales)
print('\nmadres con una sola hija y suma exacta:', int(((m.nh == 1) & (m.exact == 1)).sum()))
print(m[(m.nh == 1) & (m.exact == 1)][['cuerda', 'grupo', 'valor']].to_string(index=False))
