# -*- coding: utf-8 -*-
"""Relaciones refinadas:
A) corridas de valores REALES (nudos no vacios), rotas en ausentes y en
   fronteras de grupo. Estadistico: nº de pares con corrida comun (L>=3 y L>=4)
   y longitud maxima de corrida comun por par. Nulo: barajar dentro de cada quipu.
B) estructuras de grupo identicas/contenidas + significancia por permutacion.
C) totales (>=20) de un quipu presentes como valor/subtotal en otro.
"""
import pandas as pd, numpy as np, os
ROOT = r'.'
D = os.path.join(ROOT, 'analisis', 'datos')
RNG = np.random.default_rng(0)
NREP = 500

c = pd.read_csv(os.path.join(D, 'cuerdas.csv'))
q = pd.read_csv(os.path.join(D, 'quipus.csv'))
KFG = q.loc[q['procedencia'].isin(['Nazca', 'Atarco']), 'kfg'].tolist()
s = c[c['kfg'].isin(KFG)].copy().sort_values(['kfg', 'orden'])

def real(d):
    return d['nudos'].notna() & (d['nudos'].astype(str).str.strip() != '')

# secuencia por grupo: lista de valores reales de colgantes; None = ausente (rompe)
def seq_grupos(d):
    d = d[d['nivel'] == 0]
    out = []
    for gid, dd in d.groupby('grupo'):
        seg = []
        for _, r in dd.iterrows():
            seg.append(int(r['valor']) if (pd.notna(r['nudos']) and str(r['nudos']).strip() != '') else None)
        out.append(seg)
    return out

seqs = {k: seq_grupos(d) for k, d in s.groupby('kfg')}

def runs_of(segs, L):
    out = set()
    for seg in segs:
        i = 0
        while i <= len(seg) - L:
            win = seg[i:i + L]
            if all(x is not None for x in win):
                out.add(tuple(win)); i += 1
            else:
                # salta al siguiente no-ausente
                i += 1
    return out

def maxrun(a, b):
    # longitud de la corrida contigua real mas larga comun (dentro de grupo)
    best = 0
    for seg1 in a:
        for seg2 in b:
            # programacion simple
            # solo sobre valores reales; None corta
            n1, n2 = len(seg1), len(seg2)
            dp = [0] * (n2 + 1)
            for i in range(1, n1 + 1):
                nd = [0] * (n2 + 1)
                for j in range(1, n2 + 1):
                    if seg1[i-1] is not None and seg1[i-1] == seg2[j-1]:
                        nd[j] = dp[j-1] + 1
                        best = max(best, nd[j])
                dp = nd
    return best

def stats(seqs, L):
    ks = list(seqs)
    sets = {k: runs_of(seqs[k], L) for k in ks}
    pares = 0; tot = 0; det = []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            inter = sets[ks[i]] & sets[ks[j]]
            if inter:
                pares += 1; tot += len(inter); det.append((ks[i], ks[j], len(inter), sorted(inter)[:2]))
    return pares, tot, det

def stats_maxrun(seqs):
    ks = list(seqs)
    maxlen = 0; parmax = None
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            mr = maxrun(seqs[ks[i]], seqs[ks[j]])
            if mr > maxlen:
                maxlen = mr; parmax = (ks[i], ks[j])
    return maxlen, parmax

print('=== A) CORRIDAS DE VALORES REALES (sin ausentes) ===')
maxlen_obs, parmax_obs = stats_maxrun(seqs)
print(f'longitud maxima de corrida comun (observada, todo el archivo): {maxlen_obs} en {parmax_obs}')
obs = {}
for L in (3, 4, 5):
    pares, tot, det = stats(seqs, L)
    obs[L] = pares
    print(f'L={L}: pares={pares} corridas={tot}')

# nulo
base = {k: [seg[:] for seg in v] for k, v in seqs.items()}
flat = {k: [x for seg in v for x in seg] for k, v in seqs.items()}
null = {L: [] for L in (3, 4, 5)}
for r in range(NREP):
    perm = {}
    for k, segs in base.items():
        vals = list(flat[k]); RNG.shuffle(vals)
        it = iter(vals); perm[k] = [[next(it) for _ in seg] for seg in segs]
    for L in (3, 4, 5):
        p, t, _ = stats(perm, L)
        null[L].append(p)
for L in (3, 4, 5):
    n = np.array(null[L]); po = obs[L]
    pval = (1 + (n >= po).sum()) / (1 + NREP)
    print(f'L={L}: obs_pares={po} nulo_media={n.mean():.2f} nulo_max={n.max()} p={pval:.4f}')

# detalle de las corridas mas largas (L>=4) para inspeccion
pares, tot, det = stats(seqs, 4)
print('\nPares con corridas L>=4 (top por nº):')
for d in sorted(det, key=lambda x: -x[2])[:15]:
    print('   ', d)

print('\n=== C) TOTALES (>=20) DE UN QUIPU PRESENTES EN OTRO ===')
allo = {k: sorted(set(d.loc[d['valor'] > 0, 'valor'].astype(int))) for k, d in s.groupby('kfg')}
# subtotales: suma por grupo y suma por madre+subs
sub = {k: set() for k in KFG}
for k, d in s.groupby('kfg'):
    for gid, dd in d.groupby('grupo'):
        v = int(dd.loc[dd['valor'] > 0, 'valor'].sum())
        if v: sub[k].add(v)
    for padre, dd in d.groupby('padre'):
        if pd.notna(padre):
            v = int(dd.loc[dd['valor'] > 0, 'valor'].sum())
            if v: sub[k].add(v)
tot = {k: sum(v for v in allo[k]) for k in KFG}
hits = []
for a in KFG:
    if tot[a] < 20: continue
    for b in KFG:
        if a == b: continue
        if tot[a] in sub[b] or tot[a] in allo[b]:
            hits.append((a, tot[a], b))
for h in hits: print('   ', h)
print(f'totales>=20 cruzados: {len(hits)}')
