"""P3: relaciones numericas dentro del registro y entre registros/quipus."""
import itertools, numpy as np, pandas as pd
from lib import load, records, canon, OUT, RNG

c = load()
KS = ['UR1140', 'UR1136', 'UR223', 'HP056']
def mat(k):
    return np.array([canon(r['vals'], r['pos']) for r in records(c, k) if not np.isnan(r['vals']).any()])
Ms = {k: mat(k) for k in KS}

print('== identidades aditivas por registro ==')
rows = []
for k in KS:
    M = Ms[k]
    s26 = M[:, 1:].sum(1)
    eq1 = int((M[:, 0] == s26).sum())
    diff = M[:, 0] - s26
    # campo 1 = suma de algun subconjunto de 2..7
    hit = 0
    for r in M:
        S = r[1:]
        for m in range(1, 64):
            if abs(sum(S[i] for i in range(6) if m >> i & 1) - r[0]) < 1e-9:
                hit += 1; break
    rows.append(dict(khipu=k, n=len(M), f1_eq_suma2_7=eq1, f1_eq_suma_subconj=hit,
                     dif_mediana=float(np.median(diff)), dif_min=float(diff.min()), dif_max=float(diff.max())))
    print(f'{k:<7} n={len(M):>2}  f1==sum(f2..f7): {eq1}/{len(M)}  f1==sum(subconj 2..7): {hit}/{len(M)}  '
          f'f1-sum rango [{diff.min():.0f},{diff.max():.0f}] mediana {np.median(diff):.0f}')
R1 = pd.DataFrame(rows)

# nulo para identidades: remuestreo de valores del quipu (preserva distribucion marginal)
print('\n== nulo (remuestreo de valores del quipu, B=2000): identidades aditivas ==')
B = 2000
for k in KS:
    M = Ms[k]; obs = int((M[:, 0] == M[:, 1:].sum(1)).sum())
    pool = M.ravel()
    cnt = 0
    for _ in range(B):
        Mp = RNG.choice(pool, size=M.shape)
        if int((Mp[:, 0] == Mp[:, 1:].sum(1)).sum()) >= obs:
            cnt += 1
    print(f'{k}: f1==sum(f2..7) obs={obs}  p={(1+cnt)/(1+B):.4f}')

# diferencias constantes entre pares de campos
print('\n== diferencias constantes entre pares de campos (7x6=42 por quipu) ==')
def const_pairs(M):
    out = {}
    for i, j in itertools.permutations(range(7), 2):
        d = M[:, i] - M[:, j]
        v, n = np.unique(d, return_counts=True)
        out[(i, j)] = (v[np.argmax(n)], n.max() / len(M))
    return out
for k in KS:
    M = Ms[k]; o = const_pairs(M); top = sorted(o.items(), key=lambda x: -x[1][1])[:4]
    print(k, ' | '.join(f'f{i+1}-f{j+1}={v:.0f} en {fr:.0%}' for (i, j), (v, fr) in top))

# el mejor par de diferencias constantes: nulo por permutacion dentro de registro
print('\n== control: mejor diferencia constante vs nulo (permutacion dentro de registro) ==')
for k in KS:
    M = Ms[k]
    def best(MM):
        bb = 0
        for i, j in itertools.permutations(range(7), 2):
            d = MM[:, i] - MM[:, j]
            v, n = np.unique(d, return_counts=True); bb = max(bb, n.max() / len(MM))
        return bb
    obs = best(M); cnt = 0
    for _ in range(2000):
        Mp = np.array([RNG.permutation(r) for r in M])
        if best(Mp) >= obs - 1e-12: cnt += 1
    print(f'{k}: mejor dif constante cubre {obs:.0%} de registros, p={(1+cnt)/2001:.4f}')

# sumas entre registros y entre quipus
print('\n== sumas entre registros / entre quipus ==')
T = {k: Ms[k].sum(1) for k in KS}
for k in KS:
    t = T[k]; hit = sum(1 for i in range(len(t)) for j in range(len(t)) for l in range(j + 1, len(t))
                        if i not in (j, l) and abs(t[i] - (t[j] + t[l])) < 1e-9)
    print(f'{k}: totales de registro que son suma exacta de otros dos: {hit} casos (n={len(t)})')
for a, b in [('UR1140', 'UR1136'), ('UR1140', 'UR223'), ('UR1140', 'HP056')]:
    A, Bv = T[a], T[b]
    hit = sum(1 for x in A for y in Bv if abs(x - y) < 1e-9)
    r = np.corrcoef(A, Bv)[0, 1] if len(A) == len(Bv) else np.nan
    print(f'{a} vs {b}: totales iguales {hit}; r de totales por indice de grupo={r if not np.isnan(r) else float("nan"):.2f}')

# --- nulos mas cuidadosos ---
def any_subset_sum(r):
    S = r[1:]
    for m in range(1, 64):
        if abs(sum(S[i] for i in range(6) if m >> i & 1) - r[0]) < 1e-9:
            return True
    return False

print('\n== f1 = suma de ALGUN subconjunto de f2..f7: nulo por remuestreo ==')
for k in KS:
    M = Ms[k]; obs = sum(any_subset_sum(r) for r in M); pool = M.ravel()
    cnt = 0
    for _ in range(2000):
        Mp = RNG.choice(pool, size=M.shape)
        if sum(any_subset_sum(r) for r in Mp) >= obs:
            cnt += 1
    print(f'{k}: obs={obs}/{len(M)}  p={(1+cnt)/2001:.4f}')

print('\n== sumas de totales de registros: nulo por remuestreo ==')
for k in KS:
    M = Ms[k]; t = M.sum(1)
    def count(tv):
        return sum(1 for i in range(len(tv)) for j in range(len(tv)) for l in range(j + 1, len(tv))
                   if i not in (j, l) and abs(tv[i] - (tv[j] + tv[l])) < 1e-9)
    obs = count(t); pool = M.ravel(); cnt = 0
    for _ in range(2000):
        Mp = RNG.choice(pool, size=M.shape)
        if count(Mp.sum(1)) >= obs:
            cnt += 1
    print(f'{k}: obs={obs}  p={(1+cnt)/2001:.4f}')

R1.to_csv(OUT / 'sumas.csv', index=False)
print('\nescrito sumas.csv')
