"""
Dos sub-fichas de 7 campos segun la posicion del par de cuerdas marcadoras
(en un grupo de 9: 7 cuerdas del color modal + 2 marcadoras de otro color).
UR1140 tiene tipo (3,4) y (6,7); UR1136 tambien. Se comparan por tipo.
Nulo: permutacion dentro de cada registro. Semilla 20261018.
"""
import re, numpy as np, pandas as pd
from pathlib import Path
from collections import Counter

OUT = Path(__file__).resolve().parent
DAT = OUT.parents[1] / 'datos'
RNG = np.random.default_rng(20261018)
B = 9999

c = pd.read_csv(DAT / 'cuerdas.csv', low_memory=False).drop_duplicates(['kfg', 'cuerda'])
q = pd.read_csv(DAT / 'quipus.csv')
c['v'] = np.where(c.nudos.notna() & (c.nudos.astype(str).str.strip() != ''), c.valor, np.nan)
c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())

naz = set(q[q.procedencia.fillna('').str.contains('Nazca', case=False)].kfg)
ber = set(q[q.museo.fillna('').str.contains('Berlin', case=False)].kfg)
san = set(q[q.procedencia.fillna('').str.match(r'^Santa$')].kfg)
univ = naz | ber | san


def recs(k):
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    out = []
    for g, dd in d.groupby('grupo', sort=False):
        if len(dd) != 9:
            continue
        cols = list(dd.col)
        cnt = Counter(cols)
        maj, nmaj = cnt.most_common(1)[0]
        mix = tuple(i + 1 for i, x in enumerate(cols) if x != maj)
        if nmaj != 7:
            continue
        out.append(dict(g=int(g), mix=mix, v=dd.v.to_numpy(float)[np.array(cols) == maj],
                        v9=dd.v.to_numpy(float), cols=cols))
    return out


def prof(M):
    P = []
    for row in M:
        if np.isnan(row).any() or np.ptp(row) == 0:
            continue
        x = np.log10(row + 1)
        P.append((x - x.mean()) / x.std(ddof=0))
    return np.mean(P, axis=0) if P else None


def corr(a, b):
    if a is None or b is None:
        return np.nan
    ok = ~np.isnan(a) & ~np.isnan(b)
    if ok.sum() < 4 or np.ptp(a[ok]) == 0 or np.ptp(b[ok]) == 0:
        return np.nan
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def perm_p_frozen(M, f, B=B):
    obs = corr(prof(M), f)
    if np.isnan(obs):
        return obs, np.nan
    cnt = 0
    for _ in range(B):
        Mp = np.array([RNG.permutation(row) for row in M])
        s = corr(prof(Mp), f)
        if not np.isnan(s) and s >= obs - 1e-12:
            cnt += 1
    return obs, (1 + cnt) / (1 + B)


def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p); out = np.empty(m); prev = 0
    for r, i in enumerate(o):
        prev = max(prev, min(1.0, (m - r) * p[i])); out[i] = prev
    return out


def bh(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p); out = np.empty(m); prev = 1
    for r in range(m - 1, -1, -1):
        i = o[r]; prev = min(prev, p[i] * m / (r + 1)); out[i] = prev
    return out


# inventario de tipos en los 169
inv = []
for k in sorted(univ):
    R = recs(k)
    types = Counter(x['mix'] for x in R)
    if types:
        inv.append((k, len(R), dict(types)))
print('quipus con algun grupo 9 y 7 del color modal:', len(inv))
for x in inv:
    if x[1] >= 3:
        print(x)

# perfiles de referencia por tipo en UR1140
ref = {}
for typ in [(3, 4), (6, 7)]:
    M = np.array([x['v'] for x in recs('UR1140') if x['mix'] == typ])
    M = M[~np.isnan(M).any(1)]
    ref[typ] = prof(M)
    print('UR1140 tipo', typ, 'n', len(M), 'perfil', np.round(ref[typ], 3))

# tests por tipo
rows = []
for k in sorted(univ):
    R = recs(k)
    for typ in [(3, 4), (6, 7)]:
        M = np.array([x['v'] for x in R if x['mix'] == typ])
        if len(M) == 0:
            continue
        ncomp = int((~np.isnan(M).any(1)).sum())
        row = dict(khipu=k, tipo=str(typ), n=len(M), n_completos=ncomp,
                   en_nazca=k in naz, en_berlin=k in ber, en_santa=k in san)
        if ncomp >= 3 and k != 'UR1140':
            row['rho'] = corr(prof(M), ref[typ])
            row['p'] = perm_p_frozen(M, ref[typ])[1]
        else:
            row['rho'] = np.nan; row['p'] = np.nan
        rows.append(row)
T = pd.DataFrame(rows)
test = T.p.notna()
T['p_holm'] = np.nan; T['p_bh'] = np.nan
T.loc[test, 'p_holm'] = holm(T.loc[test, 'p'].values)
T.loc[test, 'p_bh'] = bh(T.loc[test, 'p'].values)
T.to_csv(OUT / 'resultados_tipos.csv', index=False)
print('\n== tests por tipo (>=3 registros completos, excluye UR1140) ==')
print(T[test][['khipu', 'tipo', 'n', 'n_completos', 'rho', 'p', 'p_holm', 'p_bh']].to_string(index=False))
print('\nHolm<0.05:', T[test & (T.p_holm < .05)][['khipu', 'tipo']].values.tolist())
print('BH<0.05:', T[test & (T.p_bh < .05)][['khipu', 'tipo']].values.tolist())

# cuantos quipus comparten exactamente los dos tipos
print('\n== pares de tipos ==')
for k in ['UR1140', 'UR1136', 'UR223']:
    print(k, Counter(x['mix'] for x in recs(k)))
