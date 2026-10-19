"""UR004 - aritmetica interna con nulo de permutacion (1000, seed 0)."""
import pandas as pd, numpy as np, io
from collections import defaultdict

rng = np.random.default_rng(0)
NP = 1000
D = 'analisis/datos'
cords = pd.read_csv(f'{D}/cuerdas.csv')
gr = pd.read_csv(f'{D}/grupos.csv')

u = cords[cords.kfg == 'UR004'].copy().reset_index(drop=True)
ALLN = len(u)
name2i = {c: i for i, c in enumerate(u['cuerda'])}
num = u[u.nudos.notna()].copy()
vals = num['valor'].to_numpy(float)
knot_pos = np.array([name2i[c] for c in num['cuerda']])
valmap = dict(zip(u['cuerda'], u['valor']))

def perm_vec():
    pv = np.zeros(ALLN); pv[knot_pos] = rng.permutation(vals); return pv

children = defaultdict(list)
for _, r in u.iterrows():
    if isinstance(r['padre'], str) and r['padre']:
        children[r['padre']].append(r['cuerda'])

out = io.StringIO()
def P(*a):
    print(*a); print(*a, file=out)
def emp_p(obs, nulls):
    nulls = np.asarray(nulls)
    return (1 + (nulls >= obs).sum()) / (1 + len(nulls))

# ---------- T1: colgante = suma de subsidiarias directas ----------
pend_subs = list(children.items())
midx = [name2i[m] for m, _ in pend_subs]
childidx = [[name2i[c] for c in ch] for _, ch in pend_subs]
def count_t1(pv):
    return sum(1 for mi, ci in zip(midx, childidx) if abs(pv[mi] - pv[ci].sum()) < 1e-6)
obs1 = count_t1(np.array([valmap[c] for c in u['cuerda']], float))
null1 = [count_t1(perm_vec()) for _ in range(NP)]
P('=== T1: colgante = suma de subsidiarias directas ===')
P(f'colgantes con subsidiarias: {len(pend_subs)} | coincidencias obs: {obs1} | nulo media {np.mean(null1):.2f} | p={emp_p(obs1,null1):.3f}')
det = [(m, valmap[m], [valmap[c] for c in ch]) for m, ch in pend_subs if abs(valmap[m]-sum(valmap[c] for c in ch))<1e-6]
P('coincidencias:', det[:15])

# ---------- T2: colgante = suma de TODOS los descendientes ----------
def descendants(name):
    r = []
    for c in children.get(name, []):
        r.append(c); r += descendants(c)
    return r
desidx = [[name2i[c] for c in descendants(m)] for m, _ in pend_subs]
def count_t2(pv):
    return sum(1 for mi, di in zip(midx, desidx) if di and abs(pv[mi]-pv[di].sum()) < 1e-6)
obs2 = count_t2(np.array([valmap[c] for c in u['cuerda']], float))
null2 = [count_t2(perm_vec()) for _ in range(NP)]
P('=== T2: colgante = suma de todos los descendientes ===')
P(f'obs {obs2} | nulo media {np.mean(null2):.2f} | p={emp_p(obs2,null2):.3f}')
# T1b: solo colgantes con >=2 subsidiarias
pend_multi = [(m, ch) for m, ch in pend_subs if len(ch) >= 2]
midx_m = [name2i[m] for m, _ in pend_multi]
cidx_m = [[name2i[c] for c in ch] for _, ch in pend_multi]
def count_t1b(pv):
    return sum(1 for mi, ci in zip(midx_m, cidx_m) if abs(pv[mi] - pv[ci].sum()) < 1e-6)
obs1b = count_t1b(np.array([valmap[c] for c in u['cuerda']], float))
null1b = [count_t1b(perm_vec()) for _ in range(NP)]
P(f'T1b colgantes con >=2 subsid: {len(pend_multi)} | obs {obs1b} | nulo media {np.mean(null1b):.2f} | p={emp_p(obs1b,null1b):.3f}')
P(f'distrib. n subsidiarias:', pd.Series([len(ch) for _,ch in pend_subs]).value_counts().sort_index().to_dict())

# grupos
g = gr[gr.kfg == 'UR004']
groups = []
for _, r in g.iterrows():
    idx = [name2i[c] for c in u[(u.orden >= r['desde']) & (u.orden <= r['hasta'])]['cuerda']]
    groups.append(idx)
multi = [gi for gi in groups if len(gi) >= 2]

# ---------- T3: en un grupo, alguna cuerda = suma de las demas ----------
def count_internal(pv):
    c = 0
    for gi in multi:
        s = pv[gi].sum()
        if any(abs(pv[i]*2 - s) < 1e-6 for i in gi): c += 1
    return c
obs3 = count_internal(np.array([valmap[c] for c in u['cuerda']], float))
null3 = [count_internal(perm_vec()) for _ in range(NP)]
P('=== T3: en un grupo, alguna cuerda = suma de las demas ===')
P(f'grupos >=2 cuerdas: {len(multi)} | obs {obs3} | nulo media {np.mean(null3):.2f} | p={emp_p(obs3,null3):.3f}')

# ---------- T4 (corregido): suma de un grupo Multi-cuerda = valor de una cuerda AJENA ----------
multi_groups = []
for _, r in g.iterrows():
    idx = [name2i[c] for c in u[(u.orden>=r['desde'])&(u.orden<=r['hasta'])]['cuerda']]
    if len(idx) >= 2: multi_groups.append((int(r['grupo']), idx))
def count_sum_ajena(pv):
    vs = set(np.round(pv[pv != 0], 3)); c = 0
    for _, gi in multi_groups:
        s = pv[gi].sum()
        if s > 0 and round(s, 3) in vs and all(abs(pv[i]-s) > 1e-6 for i in gi): c += 1
    return c
obs4 = count_sum_ajena(np.array([valmap[c] for c in u['cuerda']], float))
null4 = [count_sum_ajena(perm_vec()) for _ in range(NP)]
P('=== T4: suma de un grupo (>=2 cuerdas) = valor de una cuerda AJENA ===')
P(f'obs {obs4} de {len(multi_groups)} grupos multi | nulo media {np.mean(null4):.2f} | p={emp_p(obs4,null4):.3f}')
gm = [(k, round(sum(valmap[c] for c in u[(u.orden>=r2['desde'])&(u.orden<=r2['hasta'])]['cuerda']),1)) for _,r2 in g.iterrows() for k in [int(r2['grupo'])] if len([c for c in u[(u.orden>=r2['desde'])&(u.orden<=r2['hasta'])]['cuerda']])>=2]
P('sumas multi-grupo:', gm)

# ---------- T5: total del quipu ----------
tot = float(num['valor'].sum())
allvals = set(np.round(num['valor'].to_numpy(float), 3))
P('=== T5: total del quipu ===')
P(f'suma cuerdas con nudo: {tot:.1f} | max valor {num["valor"].max()} | total aparece como cuerda? {round(tot,3) in allvals} | total/2={tot/2:.1f} aparece? {round(tot/2,3) in allvals}')

# ---------- T7: valores repetidos ----------
vc = num['valor'].value_counts()
P('=== T7: valores repetidos ===')
P(f'valores distintos {num["valor"].nunique()} de {len(num)} cuerdas | con >1 aparicion: {int((vc>1).sum())} | cuerdas en valores repetidos: {int(vc[vc>1].sum())}')

# ---------- T8: adyacencia de color ----------
seq = u.sort_values('orden'); col = seq['color'].to_numpy()
same_obs = int((col[:-1] == col[1:]).sum())
null8 = [int((lambda pc: (pc[:-1]==pc[1:]).sum())(rng.permutation(col))) for _ in range(NP)]
P('=== T8: color adyacente igual ===')
P(f'obs {same_obs} de {len(col)-1} | nulo media {np.mean(null8):.2f} sd {np.std(null8):.2f} | p(mayor)={emp_p(same_obs,null8):.3f}')

# ---------- T9: entropia de color dentro de grupos ----------
colarr = dict(zip(u['cuerda'], u['color']))
def mean_entropy(cm):
    hs = []
    for _, r in g.iterrows():
        cs = [cm[c] for c in u[(u.orden>=r['desde'])&(u.orden<=r['hasta'])]['cuerda']]
        if len(cs) < 2: continue
        _, cnt = np.unique(cs, return_counts=True); p = cnt/cnt.sum()
        hs.append(-(p*np.log2(p)).sum())
    return float(np.mean(hs))
obs9 = mean_entropy(colarr)
null9 = [mean_entropy(dict(zip(u['cuerda'], rng.permutation(col)))) for _ in range(NP)]
P('=== T9: entropia de color dentro de grupos ===')
P(f'obs {obs9:.3f} | nulo media {np.mean(null9):.3f} sd {np.std(null9):.3f} | p(menor)={emp_p(-obs9,[-x for x in null9]):.3f}')

with open('analisis/ds/k_UR004/02_aritmetica.txt','w',encoding='utf-8') as f: f.write(out.getvalue())
print('WROTE 02_aritmetica.txt')
