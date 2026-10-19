# -*- coding: utf-8 -*-
"""Confirmacion UNICA de las reglas congeladas (H06, H07, H16).
Holm sobre m = 16 hipotesis registradas (todas, pasen o no).
"""
import numpy as np, pandas as pd
from scipy import stats
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

RNG = np.random.default_rng(771013)
NP = 8000
Q = ['UR266','UR268','UR269','UR270','UR272','UR273A','UR273B','UR274A','UR274B',
     'UR275','UR276','UR277','UR278','UR279']
c = pd.read_csv('ds/n_okr_incahuasi/cuerdas_okr.csv'); c['valor'] = c.valor.fillna(0)
c = c[c.kfg.isin(Q)]
part = pd.read_csv('ds/n_tanteo/particion.csv')
TAG = {(r.kfg, r.unidad, int(r.id)): r.mitad for _, r in part.iterrows()}
def tag(k, g): return TAG.get((k, 'grupo', int(g)), 'NA')

def recs(k):
    g = c[(c.kfg == k) & (c.nivel == 0)]
    out = []
    for gr, gg in g.groupby('grupo'):
        gg = gg.sort_values('orden')
        out.append(dict(grupo=int(gr), vals=gg.valor.astype(int).tolist(),
                        cab=int(gg.valor.iloc[0]), tag=tag(k, gr)))
    return sorted(out, key=lambda x: x['grupo'])

def perm_p(obs, null, side='greater'):
    null = np.asarray(null)
    return (1 + ((null >= obs) if side == 'greater' else (null <= obs)).sum()) / (1 + len(null))

res = []
def add(id_, var, stat, n, obs, exp, p):
    res.append(dict(id=id_, variante=var, estadistico=stat, n=n,
                    aciertos=obs, esperado=exp, p=p))
    print(f'{id_} {var:6s} {stat:42s} n={n:3d} obs={obs} esp={exp} p={p:.4f}')

# ---------------- H06 exacto ----------------
for k in ['UR275', 'UR269']:
    rs = [r for r in recs(k) if r['cab'] > 0 and r['tag'] == 'confirmar' and len(r['vals']) > 1]
    o = np.array([r['cab'] for r in rs]); s = np.array([sum(r['vals'][1:]) for r in rs])
    hits = int((o == s).sum())
    null = [int((RNG.permutation(o) == s).sum()) for _ in range(NP)]
    add('H06', k, 'cabecera == suma(resto), exacto', len(rs), hits,
        round(float(np.mean(null)), 2), perm_p(hits, null))

# ---------------- H16 tolerante ----------------
for k in ['UR275', 'UR269']:
    rs = [r for r in recs(k) if r['cab'] > 0 and r['tag'] == 'confirmar' and len(r['vals']) > 1]
    o = np.array([r['cab'] for r in rs], float); s = np.array([sum(r['vals'][1:]) for r in rs], float)
    obs = float((np.abs(o - s) / o < 0.05).mean())
    allv = [v for r in rs for v in r['vals'][1:]]
    sizes = [len(r['vals']) - 1 for r in rs]
    null = []
    for _ in range(NP):
        perm = RNG.permutation(allv); idx = 0; sums = []
        for z in sizes:
            sums.append(perm[idx:idx+z].sum()); idx += z
        null.append(float((np.abs(o - np.array(sums)) / o < 0.05).mean()))
    add('H16', k, 'frac. error relativo < 5 %', len(rs), round(obs, 3),
        round(float(np.mean(null)), 3), perm_p(obs, null))

# ---------------- H07 perfil de 9 columnas ----------------
def rows9(k):
    out = {}
    g = c[(c.kfg == k) & (c.nivel == 0)]
    for gr, gg in g.groupby('grupo'):
        v = gg.sort_values('orden').valor.astype(int).tolist()
        if len(v) == 9 and sum(v) > 0:
            out[int(gr)] = dict(cells=v, tag=tag(k, gr))
    return out
R = rows9('UR278')
ex = [r['cells'] for r in R.values() if r['tag'] == 'explorar']
co = [r['cells'] for r in R.values() if r['tag'] == 'confirmar']
P = np.mean([np.array(x) / sum(x) for x in ex], axis=0)
print('P congelado recalculado:', np.round(P*100, 2), 'n ex', len(ex), 'n co', len(co))
obs_mae = np.mean([np.abs(np.array(x) - sum(x)*P).mean() for x in co])
eq_mae = np.mean([np.abs(np.array(x) - sum(x)/9).mean() for x in co])
null = []
for _ in range(NP):
    vals = []
    for x in co:
        y = RNG.permutation(x)
        vals.append(np.abs(y - sum(x)*P).mean())
    null.append(float(np.mean(vals)))
add('H07', 'UR278', 'MAE por celda (predice perfil)', len(co), round(float(obs_mae), 1),
    f'{np.mean(null):.1f} (nulo), {eq_mae:.1f} (novenos)', perm_p(obs_mae, null, 'less'))

# ---------------- Holm sobre m=16 ----------------
df = pd.DataFrame(res)
m = 16
p = df.p.values.astype(float)
order = np.argsort(p)
adj = np.empty(len(p)); run = 0.0
for rank, i in enumerate(order, start=1):
    run = max(run, min(1.0, (m - rank + 1) * p[i]))
    adj[i] = run
df['p_holm_m16'] = adj
df['sig_holm_0.05'] = adj < 0.05
df.to_csv('ds/n_tanteo/confirmacion.csv', index=False)
print('\n', df[['id','variante','aciertos','esperado','p','p_holm_m16','sig_holm_0.05']].to_string(index=False))
