# -*- coding: utf-8 -*-
"""UR093: tests aritmeticos con nulo de permutacion (1000x, seed 0) y Holm.
Unidad: el quipu (un solo quipu -> los tests son internos; el nulo preserva
estructura, nivel y tasa de ceros)."""
import pandas as pd, numpy as np
from itertools import product
rng_seed = 0
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
name = u.cuerda.values; val = u.valor.values
V = dict(zip(name, val)); padre = dict(zip(name, u.padre)); nivel = dict(zip(name, u.nivel))
l0 = u[u.nivel == 0].cuerda.tolist()
l1 = u[u.nivel == 1].copy(); l1['pos'] = l1.groupby('padre').cumcount() + 1
l2 = u[u.nivel == 2]
kids1 = l1.groupby('padre').cuerda.apply(list).to_dict()
kids2 = l2.groupby('padre').cuerda.apply(list).to_dict()

def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p); adj = np.empty(m); prev = 0
    for k, i in enumerate(o):
        v = min(1, p[i] * (m - k)); v = max(v, prev); adj[i] = v; prev = v
    return adj

# ---------- valores de referencia ----------
tot_desc = {}
def desc_sum(c):
    return V[c] + sum(desc_sum(k) for k in kids2.get(c, []))
for p in l0:
    tot_desc[p] = V[p] + sum(desc_sum(k) for k in kids1.get(p, [])) + \
                  sum(V[k] for k in kids1.get(p, []))
# ojo: desc_sum ya incluye V[k]; redefinimos limpio
def all_desc_sum(c):
    s = V[c]
    for k in kids1.get(c, []) + kids2.get(c, []):
        pass
    return s + sum(all_desc_sum(k) for k in kids1.get(c, []))
# jerarquia real: nivel1 cuelga de nivel0; nivel2 cuelga de nivel1
child = {}
for c in u.cuerda:
    if pd.notna(padre[c]): child.setdefault(padre[c], []).append(c)
def subtree(c):
    return V[c] + sum(subtree(k) for k in child.get(c, []))
def children_sum(c, skip=()):
    return sum(subtree(k) for k in child.get(c, []) if k not in skip)

def info_pairs():
    """(target, ref) informativos: excluye el caso trivial 0=0."""
    out = []
    for p in l0:
        if p in child:
            s = children_sum(p)
            if V[p] > 0 or s > 0:
                out.append((p, s))
    return out
inf = info_pairs()
print('colgantes con subs:', sum(1 for p in l0 if p in child), '| informativos (no 0=0):', len(inf))
triv = [(p, children_sum(p)) for p in l0 if p in child and V[p] == 0 and children_sum(p) == 0]
print('pares triviales 0=0:', len(triv))

# ---------- estadisticos ----------
def stats(vals):
    VV = dict(zip(name, vals))
    res = {}
    # H1 suma de subsidiarias directas (subarbol)
    res['H1_suma_subs'] = sum(1 for p, s in [(p, sum(subtree(k) for k in child.get(p, []))) for p in l0]
                              if p in child and (VV[p] > 0 or s > 0) and VV[p] == s)
    # H2 suma solo nivel1 (sin nietos)
    res['H2_suma_subs_directas'] = sum(1 for p in l0 if p in child and
        (VV[p] > 0 or sum(VV[k] for k in child[p]) > 0) and
        VV[p] == sum(VV[k] for k in child[p]))
    # H3 excluye pos 6,7
    def s67(p):
        return sum(VV[k] for k in child.get(p, []) if int(k.split('s')[-1]) not in (6, 7))
    res['H3_suma_sin_pos67'] = sum(1 for p in l0 if p in child and (VV[p] > 0 or s67(p) > 0) and VV[p] == s67(p))
    # H4 cuenta de subs con nudo
    res['H4_n_subs_con_nudo'] = sum(1 for p in l0 if p in child and
        VV[p] > 0 and VV[p] == sum(1 for k in child[p] if VV[k] > 0))
    # H5 max subsidiaria
    res['H5_max_subs'] = sum(1 for p in l0 if p in child and
        (VV[p] > 0 or max(VV[k] for k in child[p]) > 0) and
        VV[p] == max(VV[k] for k in child[p]))
    # H6 suma de nivel2 bajo cada nivel1 = nivel1 (6 casos)
    res['H6_sub1_suma_nietos'] = sum(1 for c in kids2 if (VV[c] > 0 or
        sum(VV[k] for k in kids2[c]) > 0) and VV[c] == sum(VV[k] for k in kids2[c]))
    # H7 PPS: colgante = suma de ventana contigua de 2..6 vecinos (mismo grupo)
    hits = 0
    for g, grp in u[u.nivel == 0].groupby('grupo'):
        cs = grp.cuerda.tolist(); vs = [VV[c] for c in cs]; n = len(vs)
        for i in range(n):
            if vs[i] == 0: continue
            for L in range(2, 7):
                for j in range(max(0, i - L + 1), min(i + 1, n - L + 1)):
                    if j == i or (j <= i < j + L): continue
                    if sum(vs[j:j + L]) == vs[i]: hits += 1
    res['H7_PPS_ventana'] = hits
    # H8 primero del grupo = suma del resto
    res['H8_primero_suma_resto'] = sum(1 for g, grp in u[u.nivel == 0].groupby('grupo')
        if VV[grp.cuerda.iloc[0]] == grp.cuerda.iloc[1:].map(VV).sum() and VV[grp.cuerda.iloc[0]] > 0)
    return res, VV

obs, _ = stats(val)
print('observado:', obs)

# ---------- nulo 1: permutar TODOS los valores (global) ----------
# ---------- nulo 2: permutar valores DENTRO de cada nivel (preserva ceros/estructura) ----------
rng = np.random.default_rng(rng_seed)
nperm = 1000
nulls = []
for it in range(nperm):
    v2 = val.copy()
    if it % 2 == 0:  # nulo global
        rng.shuffle(v2)
    else:            # nulo estratificado por nivel
        for lv in (0, 1, 2):
            idx = np.where(u.nivel.values == lv)[0]
            v2[idx] = rng.permutation(v2[idx])
    r, _ = stats(v2)
    nulls.append(r)
N = pd.DataFrame(nulls)
print('\n== nulo (1000 permutaciones, seed 0) ==')
rows = []
for k in obs:
    nl = N[k].values
    p = (1 + (nl >= obs[k]).sum()) / (nperm + 1)
    rows.append((k, obs[k], round(nl.mean(), 2), int((nl >= obs[k]).sum()), p))
res = pd.DataFrame(rows, columns=['test', 'obs', 'null_medio', 'n_ge', 'p'])
res['p_holm'] = holm(res.p.values)
print(res.to_string(index=False, float_format=lambda x: f'{x:.4f}'))
res.to_csv('analisis/ds/k_UR093/resultados_aritmetica.csv', index=False)

# detalle de los matches informativos
print('\n== detalle H1 (colgante = suma subarbol) ==')
for p, s in inf:
    if V[p] == s:
        print(' ', p, V[p], '=', '+'.join(f'{k}:{V[k]}' for k in child[p]))
print('\n== detalle H6 (nivel1 = suma de sus 8 nietos) ==')
for c in kids2:
    if V[c] == sum(V[k] for k in kids2[c]):
        print(' ', c, V[c], '=', [V[k] for k in kids2[c]])
