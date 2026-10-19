# -*- coding: utf-8 -*-
"""KH0083: bateria de relaciones aritmeticas internas con nulo de permutacion.
Semilla 0, 1000 permutaciones. Salida acotada."""
import pandas as pd, numpy as np

rng = np.random.default_rng(0)
NPERM = 1000

C = pd.read_csv('analisis/datos/cuerdas.csv')
K = C[C['kfg'] == 'KH0083'].copy().sort_values('orden').reset_index(drop=True)
K['real'] = K['nudos'].notna()
VAL = K['valor'].to_numpy(float)
name2idx = {n: i for i, n in enumerate(K['cuerda'])}

# hijos directos (indices)
children = {}
for i, p in enumerate(K['padre']):
    if pd.notna(p):
        children.setdefault(p, []).append(i)
parent_idxs = [name2idx[n] for n in children if n in name2idx]

def stat_parent_sum(vals, real_mask, require_child_real=True):
    """n parents con >=1 hijo, valor>0, pv==sum(hijos). Requiere hijos con valor real."""
    hits = 0
    for pname, cidx in children.items():
        pi = name2idx.get(pname)
        if pi is None: continue
        pv = vals[pi]
        if pv <= 0: continue
        if require_child_real and not any(real_mask[j] for j in cidx): continue
        s = sum(vals[j] for j in cidx)
        if abs(pv - s) < 1e-9: hits += 1
    return hits

def stat_parent_sum_multichild(vals, real_mask):
    hits = 0
    for pname, cidx in children.items():
        pi = name2idx.get(pname)
        if pi is None or len(cidx) < 2: continue
        pv = vals[pi]
        if pv <= 0: continue
        s = sum(vals[j] for j in cidx)
        if abs(pv - s) < 1e-9: hits += 1
    return hits

def stat_repeat(vals):
    v = vals[vals > 0]
    if len(v) == 0: return 0
    _, cnt = np.unique(v, return_counts=True)
    return int((cnt > 1).sum())   # valores que se repiten

def stat_repeat_max(vals):
    v = vals[vals > 0]
    if len(v) == 0: return 0
    _, cnt = np.unique(v, return_counts=True)
    return int(cnt.max())

def stat_int_ratio(vals, real_mask):
    """pares (padre,hijo) ambos reales con razon entera >=2 (padre=k*hijo)"""
    hits = 0
    for pname, cidx in children.items():
        pi = name2idx.get(pname)
        if pi is None or not real_mask[pi]: continue
        pv = vals[pi]
        for j in cidx:
            if real_mask[j] and vals[j] > 0:
                r = pv / vals[j]
                if r >= 2 and abs(r - round(r)) < 1e-9:
                    hits += 1
    return hits

def perm_test(stat_fn, *masks):
    obs = stat_fn(VAL, *masks)
    null = np.empty(NPERM)
    for b in range(NPERM):
        vals = rng.permutation(VAL)
        null[b] = stat_fn(vals, *masks)
    p = (1 + (null >= obs).sum()) / (1 + NPERM)
    return obs, null.mean(), p

print('== R1: padre.valor==suma(hijos), padre>0, >=1 hijo ==')
print('obs, media_null, p:', perm_test(stat_parent_sum, K['real'].to_numpy()))
print('== R1b: igual pero >=2 hijos ==')
print('obs, media_null, p:', perm_test(stat_parent_sum_multichild, K['real'].to_numpy()))
print('== R2: valores repetidos (n de valores que se repiten) ==')
print('obs, media_null, p:', perm_test(stat_repeat))
print('== R2b: multiplicidad maxima ==')
print('obs, media_null, p:', perm_test(stat_repeat_max))
print('== R3: razon entera padre>=2*hijo (pares) ==')
print('obs, media_null, p:', perm_test(stat_int_ratio, K['real'].to_numpy()))

# detalles R1
print('\n== detalles de coincidencias padre=suma(hijos) ==')
for pname, cidx in children.items():
    pi = name2idx.get(pname)
    if pi is None: continue
    pv = VAL[pi]
    s = sum(VAL[j] for j in cidx)
    if pv > 0 and abs(pv - s) < 1e-9:
        print(f'  {pname}: pv={pv:g} hijos={[ (K.cuerda[j], VAL[j]) for j in cidx]}')
