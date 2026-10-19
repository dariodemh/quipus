# -*- coding: utf-8 -*-
"""UR003: busqueda de aritmetica interna + controles nulos (permutacion de valores
dentro del quipu, 1000 iters, semilla 0). Salida -> aritmetica_out.txt"""
import pandas as pd, numpy as np, re, json

rng = np.random.default_rng(0)
d = pd.read_csv('analisis/datos/cuerdas.csv', dtype={'nudos': str})
u = d[d.kfg == 'UR003'].copy().sort_values('orden').reset_index(drop=True)
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); out.append(s); print(s)

# ---- construir hijos ----
u['name'] = u.cuerda
children = {k: list(zip(v['cuerda'], v['valor'])) for k, v in u[u.padre.notna()].groupby('padre')}
vals = u.set_index('name').valor.to_dict()

def arrsum(names):
    return sum(vals[n] for n in names)

# lista de madres: cord ones que aparecen como padre/abuela
parents = set(u.padre.dropna())
def descendants(name):
    res = []
    stack = [name]
    while stack:
        n = stack.pop()
        for c, v in children.get(n, []):
            res.append(c); stack.append(c)
    return res
# mapa name->hijos directos (nombres)
child_names = {k: [c for c, v in v] for k, v in children.items()}

# ---------- TEST 1: madre = suma de hijas directas ----------
moms = u[u.name.isin(parents)]# todas las que tienen hijos
t1_obs = 0; t1_n = 0; detail = []
for _, r in moms.iterrows():
    ch = child_names.get(r['name'], [])
    if not ch: continue
    t1_n += 1
    s = arrsum(ch)
    if abs(s - r.valor) < 1e-9:
        t1_obs += 1
        detail.append((r['name'], r.valor, s, ch))
P('TEST1 madre == suma hijas directas: obs matches %d / %d (todas las madres)' % (t1_obs, t1_n))
if detail[:8]: P('  ejemplos:', detail[:8])

# ---------- TEST 2: madre = suma de TODOS los descendientes ----------
t2_obs = 0
for _, r in moms.iterrows():
    desc = descendants(r['name'])
    if not desc: continue
    if abs(arrsum(desc) - r.valor) < 1e-9:
        t2_obs += 1
P('TEST2 madre == suma todos descendientes: obs matches %d / %d' % (t2_obs, t1_n))

# ---------- TEST 3: colgante == suma de sus descendientes, solo nivel0 ----------
colg = u[u.nivel == 0]
t3_obs = 0; t3_n = 0; ex3 = []
for _, r in colg.iterrows():
    ch = child_names.get(r['name'], [])
    if not ch: continue
    t3_n += 1
    s = arrsum(ch)
    if abs(s - r.valor) < 1e-9:
        t3_obs += 1; ex3.append((r['name'], r.valor, s))
P('TEST3 colgante == suma hijas directas: obs %d / %d' % (t3_obs, t3_n))
if ex3: P('  ejemplos:', ex3[:10])

# ---------- NULL: barajar VALORES entre todas las cuerdas, preservando estructura ----------
V = u.valor.values.copy()
def count_t1(valarr):
    vm = dict(zip(u.name.values, valarr))
    m = 0
    for _, r in moms.iterrows():
        ch = child_names.get(r['name'], [])
        if not ch: continue
        if abs(sum(vm[c] for c in ch) - vm[r['name']]) < 1e-9: m += 1
    return m
def count_t3(valarr):
    vm = dict(zip(u.name.values, valarr))
    m = 0
    for _, r in colg.iterrows():
        ch = child_names.get(r['name'], [])
        if not ch: continue
        if abs(sum(vm[c] for c in ch) - vm[r['name']]) < 1e-9: m += 1
    return m

N = 1000
null1 = np.array([count_t1(rng.permutation(V)) for _ in range(N)])
null3 = np.array([count_t3(rng.permutation(V)) for _ in range(N)])

def pval(obs, null):
    return (1 + (null >= obs).sum()) / (N + 1)
P('\nNULL (barajar valores, N=%d, semilla 0):' % N)
P('TEST1 obs=%d  null media=%.2f max=%.0f  p=%.4f' % (t1_obs, null1.mean(), null1.max(), pval(t1_obs, null1)))
P('TEST3 obs=%d  null media=%.2f max=%.0f  p=%.4f' % (t3_obs, null3.mean(), null3.max(), pval(t3_obs, null3)))

# ---------- TEST 4: alguna cuerda del grupo = suma del grupo ----------
P('\nTEST4: cord cuyo valor == suma de colgantes del grupo:')
for gi in sorted(u.grupo.unique()):
    sub = u[u.grupo == gi]; cg = sub[sub.nivel == 0]
    s = cg.valor.sum()
    hits = sub[sub.valor == s]
    if len(hits): P('  g%d suma=%d match:' % (gi, s), list(zip(hits.cuerda, hits.valor)))

# ---------- TEST 5: suma de un grupo = suma de otro (igualdad/razones) ----------
sums = {gi: u[(u.grupo == gi) & (u.nivel == 0)].valor.sum() for gi in u.grupo.unique()}
P('\nTEST5 sumas de grupos:', sums)
from collections import Counter
c = Counter(sums.values())
P('  sumas repetidas:', {k: v for k, v in c.items() if v > 1})

# ---------- TEST 6: valor repetido dentro de subarbol / cordones con igual valor y color ----------
P('\nTEST6 valores repetidos: total cuerdas con valor>0 =', (u.valor > 0).sum())

# ---------- TEST 7: patron de color periodico en secuencia de colgantes ----------
P('\nTEST7 patrones de color (pendulo):')
seqs = []
for gi in sorted(u.grupo.unique()):
    cg = u[(u.grupo == gi) & (u.nivel == 0)].sort_values('orden')
    base = cg.color.fillna('NA').str.split(r'[:\-/]').str[0].tolist()
    if len(base) >= 4: seqs.append((gi, base))
# buscar periodicidad de periodo 2 y 3 dentro de cada grupo
def periodic_score(base, p):
    # fraccion de posiciones que siguen el patron base[i]==base[i-p]
    return np.mean([base[i] == base[i - p] for i in range(p, len(base))])
P(' grupo  n  p2  p3   colores')
for gi, base in seqs:
    P('  g%-2d %3d %.2f %.2f  %s' % (gi, len(base), periodic_score(base, 2), periodic_score(base, 3), ''.join(x[0] for x in base)))

with open('analisis/ds/k_UR003/aritmetica_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('\n[ok] aritmetica_out.txt')
