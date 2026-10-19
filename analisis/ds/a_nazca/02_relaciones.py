# -*- coding: utf-8 -*-
"""Relaciones ENTRE los quipus Nazca/Atarco.
- secuencias de valores compartidas (corridas contiguas de colgantes)
- totales de un quipu que aparecen como valor en otro
- estructuras de grupos identicas (n pendientes por grupo)
- patrones de color
Nulo: barajar valores dentro de cada quipu, 500 reps, semilla 0.
"""
import pandas as pd, numpy as np, os, json
from collections import Counter

ROOT = r'.'
D = os.path.join(ROOT, 'analisis', 'datos')
OUT = os.path.join(ROOT, 'analisis', 'ds', 'a_nazca')
RNG = np.random.default_rng(0)
NREP = 500

c = pd.read_csv(os.path.join(D, 'cuerdas.csv'))
q = pd.read_csv(os.path.join(D, 'quipus.csv'))
g = pd.read_csv(os.path.join(D, 'grupos.csv'))
KFG = q.loc[q['procedencia'].isin(['Nazca', 'Atarco']), 'kfg'].tolist()
s = c[c['kfg'].isin(KFG)].copy().sort_values(['kfg', 'orden'])

# valores de colgantes (nivel 0) en orden
pend = {k: d.loc[d['nivel'] == 0, 'valor'].astype(int).tolist()
        for k, d in s.groupby('kfg')}
# todas las cuerdas con valor>0 (pendientes y subsidiarias) para 'totales'
allv = {k: d.loc[d['valor'] > 0, 'valor'].astype(int).tolist() for k, d in s.groupby('kfg')}
# estructura de grupos: n colgantes por grupo, en orden
estr = {}
colseq = {}
for k, d in s.groupby('kfg'):
    counts = []
    for gid, dd in d.groupby('grupo'):
        counts.append(int((dd['nivel'] == 0).sum()))
    estr[k] = counts
    colseq[k] = d.loc[d['nivel'] == 0, 'color'].tolist()

def corridas(seq, L):
    """conjunto de corridas contiguas de longitud >= L"""
    out = set()
    for i in range(len(seq) - L + 1):
        out.add(tuple(seq[i:i + L]))
    return out

def n_pares_corridas(dict_seq, L):
    ks = list(dict_seq)
    sets = {k: corridas(dict_seq[k], L) for k in ks}
    pares = 0; total = 0; detalle = []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            inter = sets[ks[i]] & sets[ks[j]]
            if inter:
                pares += 1; total += len(inter)
                detalle.append((ks[i], ks[j], sorted(inter)[:3]))
    return pares, total, detalle

print('=== A) CORRIDAS CONTIGUAS DE VALORES (colgantes) ===')
res = {}
for L in (2, 3, 4):
    pares, total, det = n_pares_corridas(pend, L)
    res[L] = pares
    print(f'L={L}: pares={pares} corridas={total}')
    if L == 3:
        for d in det:
            print('   ', d)

# nulo: barajar dentro de cada quipu
print('\n--- nulo (barajar valores dentro de cada quipu, 500 reps) ---')
for L in (2, 3, 4):
    obs_pares, obs_tot, _ = n_pares_corridas(pend, L)
    null_pares = []
    base = {k: list(v) for k, v in pend.items()}
    for r in range(NREP):
        perm = {k: list(RNG.permutation(v)) for k, v in base.items()}
        p, t, _ = n_pares_corridas(perm, L)
        null_pares.append(p)
    null_pares = np.array(null_pares)
    pval = (1 + (null_pares >= obs_pares).sum()) / (1 + NREP)
    print(f'L={L}: obs_pares={obs_pares} media_nulo={null_pares.mean():.2f} '
          f'max_nulo={null_pares.max()} p={pval:.4f}')

print('\n=== B) TOTALES DE UN QUIPU QUE APARECEN EN OTRO ===')
# total del quipu = suma de todas las cuerdas con valor>0
tot = {k: sum(v) for k, v in allv.items()}
# subtotales: grupos (suma de colgantes valor>0 por grupo) y por madre+subs
subtot = {k: set() for k in KFG}
for k, d in s.groupby('kfg'):
    for gid, dd in d.groupby('grupo'):
        subtot[k].add(int(dd.loc[dd['valor'] > 0, 'valor'].sum()))
    for padre, dd in d.groupby('padre'):
        if pd.notna(padre):
            subtot[k].add(int(dd.loc[dd['valor'] > 0, 'valor'].sum()))
    for _, row in d.iterrows():
        if row['valor'] > 0:
            subtot[k].add(int(row['valor']))

def n_matches(tot, sets):
    ks = list(tot)
    vals = {k: set(sets[k]) for k in ks}
    hits = []
    for a in ks:
        for b in ks:
            if a == b:
                continue
            if tot[a] in vals[b] and tot[a] > 0:
                hits.append((a, tot[a], b))
    return hits

hits = n_matches(tot, subtot)
print('total de A presente como valor/subtotal en B:')
for h in hits:
    print('   ', h)
obs_h = len(hits)

# nulo
null_h = []
for r in range(NREP):
    perm = {k: list(RNG.permutation(v)) for k, v in allv.items()}
    pt = {k: sum(v) for k, v in perm.items()}
    ps = {k: set(v) for k, v in perm.items()}
    null_h.append(len(n_matches(pt, ps)))
null_h = np.array(null_h)
pval_h = (1 + (null_h >= obs_h).sum()) / (1 + NREP)
print(f'obs={obs_h} media_nulo={null_h.mean():.2f} max={null_h.max()} p={pval_h:.4f}')

print('\n=== C) ESTRUCTURAS DE GRUPOS ===')
for k in KFG:
    print(f'   {k}: {estr[k]}')
# pares con estructura identica o contenida
print('--- pares identicos o uno contenido en otro ---')
ks = list(estr)
def contenida(a, b):
    # a contenido contiguo en b o viceversa
    if len(a) > len(b):
        a, b = b, a
    if len(a) == 0:
        return False
    for i in range(len(b) - len(a) + 1):
        if b[i:i + len(a)] == a:
            return True
    return False
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        if estr[ks[i]] == estr[ks[j]]:
            print(f'   IDENTICA {ks[i]} == {ks[j]}: {estr[ks[i]]}')
        elif contenida(estr[ks[i]], estr[ks[j]]):
            print(f'   contenida {ks[i]} ({estr[ks[i]]}) en {ks[j]} ({estr[ks[j]]})')

print('\n=== D) PATRONES DE COLOR (colgantes) ===')
for k in KFG:
    print(f'   {k}: {colseq[k]}')
json.dump({'pend': pend, 'estr': estr, 'colseq': colseq, 'tot': tot},
          open(os.path.join(OUT, 'relaciones_dump.json'), 'w'))
