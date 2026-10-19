"""
Ficha fisica de 7 campos: grupos de 9 cuerdas con 7 cuerdas del color modal
(2 cuerdas marcadoras). UR1140, UR1136, UR223.
Nulo: permutacion dentro de cada grupo (registro). Semilla 20261018.
Correccion sobre los quipus probados (21 con grupos de 9) y, conservador, 169.
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
c['anud'] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != '')
c['v'] = np.where(c.anud, c.valor, np.nan)
c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())

naz = set(q[q.procedencia.fillna('').str.contains('Nazca', case=False)].kfg)
ber = set(q[q.museo.fillna('').str.contains('Berlin', case=False)].kfg)
san = set(q[q.procedencia.fillna('').str.match(r'^Santa$')].kfg)
univ = naz | ber | san


def groups9(k):
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    out = []
    for g, dd in d.groupby('grupo', sort=False):
        if len(dd) != 9:
            continue
        cnt = Counter(dd.col)
        maj, n = cnt.most_common(1)[0]
        sel = np.array(dd.col) == maj
        out.append(dict(g=int(g), maj=maj, n7=int(sel.sum()),
                        v7=dd.v.to_numpy(float)[sel], v9=dd.v.to_numpy(float),
                        cols=list(dd.col)))
    return out


def rank_z(M):
    Z = np.empty_like(M, float)
    for i, row in enumerate(M):
        ok = ~np.isnan(row)
        z = np.full(len(row), np.nan)
        if ok.sum() >= 2:
            r = pd.Series(row[ok]).rank().to_numpy()
            sd = r.std(ddof=0)
            z[ok] = (r - r.mean()) / sd if sd > 0 else 0.0
        Z[i] = z
    return Z


def rho_mean(M):
    M = M[~np.isnan(M).any(axis=1)]
    if len(M) < 2:
        return np.nan
    Z = rank_z(M)
    C = Z @ Z.T / M.shape[1]
    n = len(M)
    return (C.sum() - np.trace(C)) / (n * (n - 1))


def perm_p_rho(M, B=B):
    M = M[~np.isnan(M).any(axis=1)]
    obs = rho_mean(M)
    if np.isnan(obs) or len(M) < 2:
        return obs, np.nan
    Z = rank_z(M)
    n, L = Z.shape
    cnt = 0
    for _ in range(B):
        Zp = np.array([RNG.permutation(row) for row in Z])
        C = Zp @ Zp.T / L
        s = (C.sum() - np.trace(C)) / (n * (n - 1))
        cnt += s >= obs - 1e-12
    return obs, (1 + cnt) / (1 + B)


def eta2(M):
    L = np.log10(M + 1)
    grand = np.nanmean(L)
    ssb = sum(np.sum(~np.isnan(L[:, j])) * (np.nanmean(L[:, j]) - grand) ** 2 for j in range(L.shape[1]))
    sst = np.nansum((L - grand) ** 2)
    return ssb / sst if sst > 0 else np.nan


def profile(M):
    P = []
    for row in M:
        if np.isnan(row).any():
            continue
        x = np.log10(row + 1)
        if np.ptp(x) == 0:
            continue
        P.append((x - x.mean()) / x.std(ddof=0))
    return np.nanmean(P, axis=0) if P else None


def corr(a, b):
    ok = ~np.isnan(a) & ~np.isnan(b)
    if ok.sum() < 4 or np.ptp(a[ok]) == 0 or np.ptp(b[ok]) == 0:
        return np.nan
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def perm_p_frozen(M, f, B=B):
    g = profile(M)
    obs = corr(g, f)
    if np.isnan(obs):
        return obs, np.nan
    cnt = 0
    for _ in range(B):
        Mp = np.array([RNG.permutation(row) for row in M])
        gp = profile(Mp)
        s = corr(gp, f)
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


# ficha de referencia: UR1140, 7 cuerdas del color modal dentro de grupos de 9
G0 = [x for x in groups9('UR1140') if x['n7'] == 7]
M0 = np.array([x['v7'] for x in G0])
f0 = profile(M0)
print('UR1140 grupos 9:', len(groups9('UR1140')), 'con 7 del color modal:', len(M0))
print('perfil ficha7 (cluster):', np.round(f0, 3))
print('eta2', round(eta2(M0), 3), 'rho', round(rho_mean(M0), 3), 'p', perm_p_rho(M0)[1])

rows = []
for k in sorted(univ):
    gg = groups9(k)
    M7 = np.array([x['v7'] for x in gg if x['n7'] == 7]) if any(x['n7'] == 7 for x in gg) else np.empty((0, 7))
    ncomp = int((~np.isnan(M7).any(axis=1)).sum()) if len(M7) else 0
    row = dict(khipu=k, n_grupos9=len(gg), n_con7=len(M7), n_completos=ncomp,
               en_nazca=k in naz, en_berlin=k in ber, en_santa=k in san)
    if ncomp >= 3:
        r = rho_mean(M7); row['eta2'] = eta2(M7); row['rho'] = r
        row['p_rho'] = perm_p_rho(M7)[1]
        row['rho_ficha'] = corr(profile(M7), f0)
        row['p_ficha'] = perm_p_frozen(M7, f0)[1]
    else:
        row.update(eta2=np.nan, rho=np.nan, p_rho=np.nan, rho_ficha=np.nan, p_ficha=np.nan)
    rows.append(row)
R = pd.DataFrame(rows)
test = R.n_completos >= 3
R['p_holm_21'] = np.nan; R['p_bh_21'] = np.nan; R['p_holm_169'] = np.nan; R['p_bh_169'] = np.nan
# correccion primaria: 21 quipus con al menos un grupo de 9
idx21 = R.n_grupos9 >= 1
R.loc[idx21, 'p_holm_21'] = holm(R.loc[idx21, 'p_ficha'].fillna(1).values)
R.loc[idx21, 'p_bh_21'] = bh(R.loc[idx21, 'p_ficha'].fillna(1).values)
# correccion conservadora: los 169 quipus probados (los no testables p=1)
R['p_holm_169'] = holm(R.p_ficha.fillna(1).values)
R['p_bh_169'] = bh(R.p_ficha.fillna(1).values)
R.to_csv(OUT / 'resultados_ficha9.csv', index=False)

print('\n-- quipus con >=3 grupos de 9 y 7 campos --')
print(R[test][['khipu', 'n_grupos9', 'n_con7', 'n_completos', 'eta2', 'rho', 'p_rho',
               'rho_ficha', 'p_ficha', 'p_holm_21', 'p_bh_21', 'p_holm_169', 'p_bh_169']]
      .to_string(index=False))
print('\n-- 21 quipus con grupos de 9 (aunque no testables) --')
print(R[idx21][['khipu', 'n_grupos9', 'n_con7', 'n_completos', 'rho_ficha', 'p_holm_21']].to_string(index=False))

# correlaciones entre las tres fichas
print('\n== correlacion entre perfiles ==')
for a in ['UR1140', 'UR1136', 'UR223']:
    for b in ['UR1140', 'UR1136', 'UR223']:
        if a < b:
            Ma = np.array([x['v7'] for x in groups9(a) if x['n7'] == 7])
            Mb = np.array([x['v7'] for x in groups9(b) if x['n7'] == 7])
            print(a, b, 'rho_perfil', round(corr(profile(Ma), profile(Mb)), 3),
                  'n', len(Ma), len(Mb))

# copias / sumas
print('\n== copias / sumas ==')
def allvals(k):
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    return d.v.to_numpy(float)
for a, b in [('UR1140', 'UR1136'), ('UR1140', 'UR223'), ('UR1136', 'UR223')]:
    va, vb = allvals(a), allvals(b)
    sa, sb = np.sort(va[~np.isnan(va)]), np.sort(vb[~np.isnan(vb)])
    n = min(len(sa), len(sb))
    overlap = len(set(sa) & set(sb)) / len(set(sa) | set(sb))
    print(a, b, 'n', len(va), len(vb), 'suma', np.nansum(va), np.nansum(vb),
          'corr_ordenados', round(float(np.corrcoef(sa[:n], sb[:n])[0, 1]), 3),
          'solape_multiset', round(overlap, 3))
    # sumas por grupo emparejadas por orden
    ga = [x['v9'].sum() for x in groups9(a)]
    gb = [x['v9'].sum() for x in groups9(b)]
    m = min(len(ga), len(gb))
    print('   sumas por grupo (primeros', m, ')', np.round(ga[:m], 1), np.round(gb[:m], 1),
          'corr', round(float(np.corrcoef(ga[:m], gb[:m])[0, 1]), 3))

# guardar ficha
pd.DataFrame({'posicion': np.arange(1, 8), 'perfil_z_7campos': np.round(f0, 4)}).to_csv(OUT / 'ficha7.csv', index=False)
print('\nescrito ficha7.csv')
