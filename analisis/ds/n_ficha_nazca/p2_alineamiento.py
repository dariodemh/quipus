"""P2: alineamiento de los campos 3-7 entre quipus. 120 permutaciones, con
correccion por el maximo (estadistico max sobre las 120) y nulo por permutacion
dentro de cada registro."""
import itertools, numpy as np, pandas as pd
from lib import load, records, canon, prof, corr, holm, bh, OUT, RNG

c = load()
KS = ['UR1140', 'UR1136', 'UR223', 'HP056']
PERMS = list(itertools.permutations(range(5)))
P5 = np.array(PERMS)  # 120 x 5

def mat(k):
    V = [canon(r['vals'], r['pos']) for r in records(c, k) if not np.isnan(r['vals']).any()]
    return np.array(V)

def prof5(M):
    """Perfil z de las columnas 3-7."""
    X = np.log10(M[:, 2:] + 1)
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True, ddof=0)
    return Z.mean(0)

def allr(f, p):
    """r de f con p[perm] para las 120 permutaciones."""
    Q = p[P5]                      # 120 x 5
    fc = f - f.mean(); pc = Q - Q.mean(1, keepdims=True)
    return (pc @ fc) / (np.linalg.norm(pc, axis=1) * np.linalg.norm(fc))

def maxr_null(Mt, f, B=4000):
    obs = allr(f, prof5(Mt)); imax = int(np.argmax(obs)); mx = obs[imax]
    cnt = 0; vals = np.empty(B)
    for b in range(B):
        Mp = np.array([RNG.permutation(row) for row in Mt[:, 2:]])
        # el nulo permuta los 5 campos dentro de cada registro
        X = np.log10(Mp + 1)
        Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True, ddof=0)
        rr = allr(f, Z.mean(0)); vals[b] = rr.max()
        if vals[b] >= mx - 1e-12:
            cnt += 1
    return mx, PERMS[imax], (1 + cnt) / (1 + B)

Ms = {k: mat(k) for k in KS}
for k in KS:
    print(k, 'registros completos', len(Ms[k]), 'media cruda 7 campos', np.round(Ms[k].mean(0), 1))
f0 = prof5(Ms['UR1140'])

print('\n== perfil z de los campos 3-7 ==')
for k in KS:
    print(f'{k:<7}', np.round(prof5(Ms[k]), 2))

print('\n== 120 permutaciones: mejor alineamiento con UR1140 (campos 3-7) ==')
rows = []
for k in KS[1:]:
    mx, pm, p = maxr_null(Ms[k], f0)
    # r sin permutar
    r0 = float(np.corrcoef(prof5(Ms[k]), f0)[0, 1])
    rows.append(dict(khipu=k, n=len(Ms[k]), r_sin_perm=r0, r_max=mx,
                     permutacion=str(tuple(i + 1 for i in pm)), p_max=p))
    print(f'{k}: r sin permutar={r0:+.3f} | mejor perm={tuple(i+1 for i in pm)} r={mx:+.3f} | p(max)={p:.4f}')
R = pd.DataFrame(rows)

# --- test conjunto: una sola permutacion para los 3 quipus ---
print('\n== test conjunto: una permutacion para los 3 quipus ==')
F = [prof5(Ms[k]) for k in KS[1:]]
def joint_stat(Plist):
    # media de r para cada permutacion
    Rs = np.array([allr(f0, p) for p in Plist])   # 3 x 120
    return Rs.mean(0)
obs = joint_stat(F); j = int(np.argmax(obs))
print('mejor permutacion conjunta', tuple(i + 1 for i in PERMS[j]), 'media r=', round(obs[j], 3),
      '| r por quipu', [round(float(allr(f0, F[i])[j]), 3) for i in range(3)])
B = 3000; cnt = 0; nullmax = np.empty(B)
for b in range(B):
    Fp = []
    for M in [Ms[k] for k in KS[1:]]:
        Mp = np.array([RNG.permutation(row) for row in M[:, 2:]])
        X = np.log10(Mp + 1)
        Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True, ddof=0)
        Fp.append(Z.mean(0))
    s = joint_stat(Fp).max(); nullmax[b] = s
    if s >= obs[j] - 1e-12:
        cnt += 1
print(f'p(max conjunto)={(1+cnt)/(1+B):.4f}  nulo: media={nullmax.mean():.3f} p95={np.quantile(nullmax,.95):.3f}')

# permutaciones por par (matriz completa, para ver consistencia)
print('\n== mejor permutacion por par de quipus (r max) ==')
for a in range(4):
    for b in range(a + 1, 4):
        rr = allr(prof5(Ms[KS[a]]), prof5(Ms[KS[b]]))
        i = int(np.argmax(rr))
        print(f'{KS[a]} vs {KS[b]}: perm={tuple(x+1 for x in PERMS[i])} r={rr[i]:+.3f} (r sin perm={allr(prof5(Ms[KS[a]]), prof5(Ms[KS[b]]))[0]:+.3f})')

R.to_csv(OUT / 'alineamiento_120.csv', index=False)
np.save(OUT / 'perfil_campos37.npy', np.array([prof5(Ms[k]) for k in KS]))
print('\nescrito alineamiento_120.csv')
