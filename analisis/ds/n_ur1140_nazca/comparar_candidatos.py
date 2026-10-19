"""Compara UR1140, UR1136 y UR223: copias, sumas o registros independientes del mismo tipo."""
import re, numpy as np, pandas as pd
from pathlib import Path
from collections import Counter

OUT = Path(__file__).resolve().parent
DAT = OUT.parents[1] / 'datos'
c = pd.read_csv(DAT / 'cuerdas.csv', low_memory=False).drop_duplicates(['kfg', 'cuerda'])
c['v'] = np.where(c.nudos.notna() & (c.nudos.astype(str).str.strip() != ''), c.valor, np.nan)
c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())


def groups(k):
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    out = []
    for g, dd in d.groupby('grupo', sort=False):
        cnt = Counter(dd.col)
        maj = cnt.most_common(1)[0][0]
        sel = np.array(dd.col) == maj
        out.append(dict(g=int(g), n=len(dd), v=dd.v.to_numpy(float),
                        v7=dd.v.to_numpy(float)[sel] if sel.sum() == 7 else None))
    return out


print('== estructura ==')
for k in ['UR1140', 'UR1136', 'UR223']:
    gg = groups(k)
    v = np.concatenate([x['v'] for x in gg])
    print(k, 'grupos', len(gg), 'tamanos', Counter(x['n'] for x in gg),
          'cuerdas', len(v), 'numericas', int((~np.isnan(v)).sum()),
          'suma', np.nansum(v), 'media', round(np.nanmean(v), 2), 'max', np.nanmax(v),
          'grupos_con_7', sum(x['v7'] is not None for x in gg))

print('\n== UR1140 vs UR1136: alineacion por orden de grupo ==')
ga, gb = groups('UR1140'), groups('UR1136')
A = np.array([x['v'] for x in ga if x['n'] == 9])
Bm = np.array([x['v'] for x in gb if x['n'] == 9])
print('formas', A.shape, Bm.shape)
# matrices de 7 campos solo donde hay 7
A7 = np.array([x['v7'] for x in ga if x['v7'] is not None])
B7 = np.array([x['v7'] for x in gb if x['v7'] is not None])
print('7 campos', A7.shape, B7.shape)
for name, X, Y in [('orden', A7, B7), ('invertido', A7, B7[::-1])]:
    n = min(len(X), len(Y))
    x, y = X[:n], Y[:n]
    ok = ~np.isnan(x) & ~np.isnan(y)
    print(name, 'n', n, 'fraccion celdas identicas', round(float(np.mean(x[ok] == y[ok])), 3),
          'corr celdas', round(float(np.corrcoef(x[ok], y[ok])[0, 1]), 3),
          'ratio mediano', round(float(np.median(y[ok] / np.where(x[ok] == 0, np.nan, x[ok]))), 3))
# sumas de grupo
sa = np.array([np.nansum(x['v']) for x in ga if x['n'] == 9])
sb = np.array([np.nansum(x['v']) for x in gb if x['n'] == 9])
ok = ~np.isnan(sa) & ~np.isnan(sb)
print('sumas por grupo corr', round(float(np.corrcoef(sa[ok], sb[ok])[0, 1]), 3),
      'ratios', np.round(sb[ok] / sa[ok], 2))

# test de sumas exactas: algun grupo de B = grupo de A, o suma de dos grupos de A
setA = set(np.round(sa[~np.isnan(sa)], 3))
pairs = set(np.round(sa[i] + sa[j], 3) for i in range(len(sa)) for j in range(i + 1, len(sa))
            if not np.isnan(sa[i]) and not np.isnan(sa[j]))
setB = set(np.round(sb[~np.isnan(sb)], 3))
print('grupos B que son un grupo A exacto:', len(setB & setA), '/', len(setB))
print('grupos B que son suma exacta de dos grupos A:', len(setB & pairs), '/', len(setB))
print('total B / total A', round(np.nansum(Bm) / np.nansum(A), 3))

print('\n== UR223 ==')
gc = groups('UR223')
C = np.array([x['v'] for x in gc if x['n'] == 9])
C7 = np.array([x['v7'] for x in gc if x['v7'] is not None])
print('formas', C.shape, C7.shape, 'suma', np.nansum(C))
# solapamiento de multiset con A
va = np.sort(A[~np.isnan(A)]); vc = np.sort(C[~np.isnan(C)])
print('multiset A/C solape', round(len(set(va) & set(vc)) / len(set(va) | set(vc)), 3))
# sumas: algun grupo C = grupo A o suma de dos A
sc = np.array([np.nansum(x['v']) for x in gc])
print('sumas C', np.round(sc, 1))
print('grupos C que son grupo A exacto:', len(set(np.round(sc, 3)) & setA), '/', len(sc))
print('grupos C que son suma de dos A:', len(set(np.round(sc, 3)) & pairs), '/', len(sc))

# perfil de las tres fichas
def prof(M):
    P = []
    for row in M:
        if np.isnan(row).any():
            continue
        x = np.log10(row + 1)
        if np.ptp(x) == 0:
            continue
        P.append((x - x.mean()) / x.std(ddof=0))
    return np.nanmean(P, 0)
print('\n== perfiles (7 campos) ==')
for k, M in [('UR1140', A7), ('UR1136', B7), ('UR223', C7)]:
    print(k, np.round(prof(M), 3))
