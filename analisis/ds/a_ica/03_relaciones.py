# -*- coding: utf-8 -*-
"""Relaciones ENTRE los quipus de Ica: secuencias de valores compartidas,
totales de un quipu en otro, estructuras de grupos idénticas, patrones de color.
Nulo por permutación (semilla 0)."""
import pandas as pd, numpy as np, os, re
from collections import Counter

rng_seed = 0
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DAT = os.path.join(RAIZ, 'analisis', 'datos')
HERE = os.path.dirname(__file__)

sel = pd.read_csv(os.path.join(HERE, 'sel_ica.csv'))
sel['kfg'] = sel['kfg'].astype(str)
OBJ = dict(zip(sel['kfg'], sel['objeto']))  # dedup: mismo objeto = mismo valor
c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv'))
c['kfg'] = c['kfg'].astype(str)
g = pd.read_csv(os.path.join(DAT, 'grupos.csv'))
g['kfg'] = g['kfg'].astype(str)
cc = c[c['kfg'].isin(sel['kfg'])].copy()

def nclusters(s):
    if pd.isna(s) or str(s).strip() in ('', 'nan'):
        return 0
    return len([x for x in str(s).split(';') if x.strip()])

cc['ncl'] = cc['nudos'].map(nclusters)
cc = cc.sort_values(['kfg', 'orden'])

# Un quipu-dato por OBJETO (para no contar KH0033 y UR044 dos veces)
quipus = []
for kfg, sub in cc.groupby('kfg'):
    quipus.append((OBJ[kfg], kfg, sub))
# quedarnos con una sola fila por objeto: el primer kfg
seen = {}
for ob, kfg, sub in quipus:
    if ob not in seen:
        seen[ob] = (kfg, sub)
OBJ_IDS = list(seen.keys())
print('Objetos únicos analizados:', len(OBJ_IDS))

# --- Series de valores (colgantes nivel 0, valor presente, en orden) ---
series = {}
for ob in OBJ_IDS:
    kfg, sub = seen[ob]
    p = sub[(sub['nivel'] == 0) & (sub['ncl'] > 0)]['valor'].astype(int).tolist()
    series[ob] = p

# --- Estructura de grupos (tamaño de cada grupo) ---
gstruct = {}
for ob in OBJ_IDS:
    kfg, sub = seen[ob]
    gg = g[g['kfg'] == kfg].sort_values('grupo')
    sizes = (gg['hasta'] - gg['desde'] + 1).astype(int).tolist()
    gstruct[ob] = tuple(sizes)

# --- Totales ---
total = {ob: int(sum(series[ob])) for ob in OBJ_IDS}


def seqset(vals, L):
    return set(tuple(vals[i:i + L]) for i in range(len(vals) - L + 1))


def shared_ngrams(series, L, ids):
    ss = {ob: seqset(series[ob], L) for ob in ids}
    total_shared = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            inter = ss[ids[i]] & ss[ids[j]]
            total_shared += len(inter)
    return total_shared


# ---------- (A) Secuencias de valores compartidas (n-gramas consecutivos) ----------
print('\n=== (A) N-gramas de valores compartidos entre pares ===')
for L in (3, 4):
    obs = shared_ngrams(series, L, OBJ_IDS)
    # nulo: barajar valores DENTRO de cada quipu (rompe contigüidad, conserva multiset)
    null = []
    for t in range(500):
        rng = np.random.default_rng(rng_seed * 1000 + t)
        perm = {}
        for ob in OBJ_IDS:
            v = series[ob][:]
            rng.shuffle(v)
            perm[ob] = v
        null.append(shared_ngrams(perm, L, OBJ_IDS))
    null = np.array(null)
    p = (np.sum(null >= obs) + 1) / (len(null) + 1)
    print('L=%d  obs=%d  nulo medio=%.1f  p=%.4f  (IC95 nulo %.1f-%.1f)'
          % (L, obs, null.mean(), p, np.percentile(null, 2.5), np.percentile(null, 97.5)))

# Detalle de los pares con más n-gramas de longitud 4 compartidos
ss4 = {ob: seqset(series[ob], 4) for ob in OBJ_IDS}
pairs = []
for i in range(len(OBJ_IDS)):
    for j in range(i + 1, len(OBJ_IDS)):
        a, b = OBJ_IDS[i], OBJ_IDS[j]
        inter = ss4[a] & ss4[b]
        if inter:
            pairs.append((len(inter), a, b, sorted(inter)[:3]))
pairs.sort(reverse=True)
print('Pares con >=1 n-grama L=4 compartido:', len(pairs))
for n, a, b, ex in pairs[:12]:
    print('  %2d  %s ~ %s  ej %s' % (n, a, b, ex))

# ---------- (B) Totales de un quipu que aparecen en otro ----------
print('\n=== (B) Totales de un quipu presentes en otro (valor de cuerda o de grupo) ===')
# valores presentes de cada objeto (cuerdas con nudo)
cc['objeto'] = cc['kfg'].map(OBJ)
vals_by = {}
for ob in OBJ_IDS:
    vals_by[ob] = set(cc[(cc['objeto'] == ob) & (cc['ncl'] > 0)]['valor'].astype(int))
# número de objetos cuyo total aparece como valor en otro objeto
def count_total_in_other(total, vals_by, ids):
    hits = 0
    for a in ids:
        ta = total[a]
        if ta <= 0:
            continue
        for b in ids:
            if a != b and ta in vals_by[b]:
                hits += 1
    return hits


def count_total_in_other_vals(total, vals_by, ids):
    hits = 0
    for a in ids:
        ta = total[a]
        if ta <= 0:
            continue
        for b in ids:
            if a != b and ta in vals_by[b]:
                hits += 1
    return hits


obs = count_total_in_other(total, vals_by, OBJ_IDS)
print('Coincidencias total(A) == valor de cuerda en B:', obs)
# Nulo: permutar valores entre quipus globalmente (reconstruir series y totales)
allvals = [v for ob in OBJ_IDS for v in series[ob]]
null = []
for t in range(500):
    rng = np.random.default_rng(rng_seed * 777 + t)
    shuffled = allvals[:]
    rng.shuffle(shuffled)
    # reasignar conservando el tamaño de cada serie
    k = 0
    pser, ptot, pvals = {}, {}, {}
    for ob in OBJ_IDS:
        n = len(series[ob])
        pser[ob] = shuffled[k:k + n]
        k += n
        ptot[ob] = int(sum(pser[ob]))
        pvals[ob] = set(pser[ob])
    null.append(count_total_in_other_vals(ptot, pvals, OBJ_IDS))
null = np.array(null)
p = (np.sum(null >= obs) + 1) / (len(null) + 1)
print('nulo medio=%.1f  p=%.4f' % (null.mean(), p))

# ---------- (C) Estructuras de grupos idénticas ----------
print('\n=== (C) Estructuras de grupos idénticas (misma secuencia de tamaños) ===')
cnt = Counter(gstruct[ob] for ob in OBJ_IDS)
dup = {k: v for k, v in cnt.items() if v > 1}
print('Estructuras repetidas:', len(dup))
for k, v in sorted(dup.items(), key=lambda x: -x[1])[:10]:
    obs_ = [ob for ob in OBJ_IDS if gstruct[ob] == k]
    print('  x%d  %s -> %s' % (v, k, obs_))
pairsid = sum(v * (v - 1) // 2 for v in cnt.values())
# Nulo: barajar la asignación de estructuras entre quipus (conserva multiset)
null = []
for t in range(500):
    rng = np.random.default_rng(rng_seed * 55 + t)
    arr = [gstruct[ob] for ob in OBJ_IDS]
    rng.shuffle(arr)
    c2 = Counter(arr)
    null.append(sum(v * (v - 1) // 2 for v in c2.values()))
null = np.array(null)
p = (np.sum(null >= pairsid) + 1) / (len(null) + 1)
print('pares idénticos obs=%d  nulo=%.1f  p=%.4f' % (pairsid, null.mean(), p))

# ---------- (D) Patrones de color compartidos ----------
print('\n=== (D) Patrones de color compartidos (n-gramas de color de colgante) ===')
colser = {}
for ob in OBJ_IDS:
    kfg, sub = seen[ob]
    colser[ob] = sub[(sub['nivel'] == 0)]['color'].fillna('?').astype(str).tolist()
for L in (3, 4):
    obs = 0
    ss = {ob: seqset(colser[ob], L) for ob in OBJ_IDS}
    for i in range(len(OBJ_IDS)):
        for j in range(i + 1, len(OBJ_IDS)):
            obs += len(ss[OBJ_IDS[i]] & ss[OBJ_IDS[j]])
    null = []
    for t in range(500):
        rng = np.random.default_rng(rng_seed * 999 + t)
        perm = {}
        for ob in OBJ_IDS:
            v = colser[ob][:]
            rng.shuffle(v)
            perm[ob] = v
        sp = {ob: seqset(perm[ob], L) for ob in OBJ_IDS}
        tot = 0
        for i in range(len(OBJ_IDS)):
            for j in range(i + 1, len(OBJ_IDS)):
                tot += len(sp[OBJ_IDS[i]] & sp[OBJ_IDS[j]])
        null.append(tot)
    null = np.array(null)
    p = (np.sum(null >= obs) + 1) / (len(null) + 1)
    print('L=%d  obs=%d  nulo=%.1f  p=%.4f' % (L, obs, null.mean(), p))
