"""
Ficha canonica de 7 campos en grupos de 9 (7 del color modal + 2 marcadoras).
Canonicalizacion: si el primer marcador esta en posicion >=5, se invierte el orden
de las 7 cuerdas (lectura en sentido contrario). Se congela UR1140 y se prueba
el perfil completo y el de los campos 3-7 por separado.
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
c['v'] = np.where(c.nudos.notna() & (c.nudos.astype(str).str.strip() != ''), c.valor, np.nan)
c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())


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
        out.append(dict(g=int(g), mix=mix, v=dd.v.to_numpy(float)[np.array(cols) == maj]))
    return out


def canon(k):
    M = []
    for x in recs(k):
        if np.isnan(x['v']).any():
            continue
        M.append(x['v'] if x['mix'][-1] < 5 else x['v'][::-1])
    return np.array(M)


def prof(M):
    P = []
    for r in M:
        if np.ptp(r) == 0:
            continue
        x = np.log10(r + 1)
        P.append((x - x.mean()) / x.std(ddof=0))
    return np.mean(P, axis=0) if P else None


def corr(a, b):
    if a is None or b is None:
        return np.nan
    ok = ~np.isnan(a) & ~np.isnan(b)
    if ok.sum() < 3 or np.ptp(a[ok]) == 0 or np.ptp(b[ok]) == 0:
        return np.nan
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def perm_p(M, f, sl=slice(None), B=B):
    obs = corr(prof(M)[sl], f[sl])
    if np.isnan(obs):
        return obs, np.nan
    cnt = 0
    for _ in range(B):
        Mp = np.array([RNG.permutation(row) for row in M])
        s = corr(prof(Mp)[sl], f[sl])
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


# inventario en todo el corpus
inv = []
for k, d in c[c.nivel == 0].groupby('kfg'):
    n = 0; types = Counter()
    for g, dd in d.groupby('grupo', sort=False):
        if len(dd) != 9:
            continue
        cols = list(dd.col); cnt = Counter(cols); maj = cnt.most_common(1)[0][0]
        if cnt[maj] != 7:
            continue
        n += 1; types[tuple(i + 1 for i, x in enumerate(cols) if x != maj)] += 1
    if n >= 3:
        inv.append((k, n, dict(types)))
print('quipus del corpus con >=3 grupos 9 y 7 del color modal:', len(inv))
for x in inv:
    print(' ', x)

f = prof(canon('UR1140'))
print('\nUR1140 canonico n', len(canon('UR1140')), 'perfil', np.round(f, 3))
print('campos 1-2', np.round(f[:2], 2), '| campos 3-7', np.round(f[2:], 2))

rows = []
for k, n, types in inv:
    M = canon(k)
    row = dict(khipu=k, n_grupos=n, n_completos=len(M), tipos=str(types))
    if len(M) >= 3 and k != 'UR1140':
        row['rho_total'], row['p_total'] = perm_p(M, f)
        row['rho_3_7'], row['p_3_7'] = perm_p(M, f, slice(2, None))
        row['rho_1_2'], row['p_1_2'] = perm_p(M, f, slice(0, 2))
    else:
        row.update(rho_total=np.nan, p_total=np.nan, rho_3_7=np.nan, p_3_7=np.nan,
                   rho_1_2=np.nan, p_1_2=np.nan)
    rows.append(row)
R = pd.DataFrame(rows)
test = R.p_total.notna()
R['p_holm_5'] = np.nan; R['p_bh_5'] = np.nan
R.loc[test, 'p_holm_5'] = holm(R.loc[test, 'p_total'].values)
R.loc[test, 'p_bh_5'] = bh(R.loc[test, 'p_total'].values)
R['p_holm_651'] = np.nan; R['p_bh_651'] = np.nan
p651 = np.ones(651)
p651[:len(R)] = np.where(test.values, R.p_total.fillna(1).values, 1.0)
R.loc[test, 'p_holm_651'] = holm(p651)[:len(R)][test.values]
R.loc[test, 'p_bh_651'] = bh(p651)[:len(R)][test.values]
R.to_csv(OUT / 'resultados_canonico.csv', index=False)
print('\n== pruebas con la ficha canonica de UR1140 ==')
print(R[['khipu', 'n_grupos', 'n_completos', 'rho_total', 'p_total', 'rho_3_7', 'p_3_7',
         'rho_1_2', 'p_holm_5', 'p_holm_651']].to_string(index=False))

# correlaciones entre perfiles canonicos
print('\n== correlaciones entre perfiles canonicos ==')
P = {k: prof(canon(k)) for k, n, t in inv}
for a in P:
    for b in P:
        if a < b and P[a] is not None and P[b] is not None:
            print(a, b, 'total', round(corr(P[a], P[b]), 3),
                  'campos3-7', round(corr(P[a][2:], P[b][2:]), 3))

# guardar ficha canonica y variantes
pd.DataFrame({'posicion': np.arange(1, 8), 'perfil_canonico_z': np.round(f, 4),
              'perfil_campos3_7_z': [np.nan, np.nan] + list(np.round(f[2:], 4))}).to_csv(OUT / 'ficha7_canonica.csv', index=False)
print('\nescrito ficha7_canonica.csv')
