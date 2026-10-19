"""
UR1140 (Berlin, Nazca): ficha de 7 campos.
Reproduccion independiente + aplicacion de la ficha congelada a Nazca, Berlin y Santa.
Semilla 20261018. Solo lectura de analisis/datos/*.csv y del khipu.db (modo ro).
"""
import re, json, sqlite3
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from pathlib import Path

OUT = Path(__file__).resolve().parent
DAT = OUT.parents[1] / 'datos'
RNG = np.random.default_rng(20261018)
B = 9999

# ---------------------------------------------------------------- datos
c = pd.read_csv(DAT / 'cuerdas.csv', low_memory=False)
c = c.drop_duplicates(subset=['kfg', 'cuerda'], keep='first')
q = pd.read_csv(DAT / 'quipus.csv')
c['anud'] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != '')
c['v'] = np.where(c.anud, c.valor, np.nan)
c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())


def get(k):
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    return d.v.to_numpy(float), d.col.to_numpy(str), d.grupo.to_numpy(int), d


def runs(col):
    cut = np.flatnonzero(col[1:] != col[:-1]) + 1
    st = np.concatenate([[0], cut])
    ln = np.diff(np.concatenate([st, [len(col)]]))
    return st, ln


def bands(k, lo=4, hi=12):
    """Bandas = rachas maximas de color identico (color ya sin rangos cm).
    L = largo modal de racha en [lo,hi]; devuelve las rachas de largo L."""
    v, col, grp, d = get(k)
    if len(col) < lo:
        return None
    st, ln = runs(col)
    r = ln[(ln >= lo) & (ln <= hi)]
    if not len(r):
        return None
    u, n = np.unique(r, return_counts=True)
    L = int(u[np.lexsort((u, n))[-1]])
    bidx = [np.arange(s, s + l) for s, l in zip(st, ln) if l == L]
    return dict(k=k, v=v, col=col, grp=grp, L=L, bands=bidx,
                starts=[int(b[0]) for b in bidx], n_all=len(col), d=d)


def rank_z(M):
    """Matriz de z-scores de rangos por fila (Spearman listo para producto)."""
    Z = np.empty_like(M, dtype=float)
    for i, row in enumerate(M):
        ok = ~np.isnan(row)
        r = np.full(len(row), np.nan)
        if ok.sum() >= 2:
            rr = pd.Series(row[ok]).rank().to_numpy()
            z = (rr - rr.mean()) / (rr.std(ddof=0) if rr.std(ddof=0) > 0 else 1)
            r[ok] = z
        Z[i] = r
    return Z


def rho_mean(M):
    """Spearman medio por pares de bandas (solo filas completas)."""
    M = M[~np.isnan(M).any(axis=1)]
    if len(M) < 2:
        return np.nan
    Z = rank_z(M)
    C = Z @ Z.T / M.shape[1]
    n = len(M)
    return (C.sum() - np.trace(C)) / (n * (n - 1))


def eta2(M):
    L = np.log10(M + 1)
    grand = np.nanmean(L)
    ssb = sum(np.sum(~np.isnan(L[:, j])) * (np.nanmean(L[:, j]) - grand) ** 2 for j in range(L.shape[1]))
    sst = np.nansum((L - grand) ** 2)
    return ssb / sst if sst > 0 else np.nan


def perm_p_rho(M, B=B, rng=RNG):
    M = M[~np.isnan(M).any(axis=1)]
    obs = rho_mean(M)
    if np.isnan(obs) or len(M) < 2:
        return obs, np.nan
    Z = rank_z(M)
    n, L = Z.shape
    cnt = 0
    for _ in range(B):
        Zp = np.array([rng.permutation(row) for row in Z])
        C = Zp @ Zp.T / L
        s = (C.sum() - np.trace(C)) / (n * (n - 1))
        cnt += s >= obs - 1e-12
    return obs, (1 + cnt) / (1 + B)


def profile(M):
    """Perfil medio: z-score de log10(v+1) dentro de cada banda, promedio por posicion."""
    P = []
    for row in M:
        ok = ~np.isnan(row)
        if ok.sum() < 3:
            continue
        x = np.log10(row[ok] + 1)
        if np.ptp(x) == 0:
            continue
        z = (x - x.mean()) / x.std(ddof=0)
        p = np.full(len(row), np.nan)
        p[ok] = z
        P.append(p)
    return np.nanmean(np.array(P), axis=0) if P else None


def corr_frozen(g, f):
    ok = ~np.isnan(g) & ~np.isnan(f)
    if ok.sum() < 4 or np.ptp(g[ok]) == 0 or np.ptp(f[ok]) == 0:
        return np.nan
    return float(np.corrcoef(g[ok], f[ok])[0, 1])


def perm_p_frozen(M, f, B=B, rng=RNG):
    """p de que el perfil medio se parezca a f por azar, permutando dentro de banda."""
    g = profile(M)
    obs = corr_frozen(g, f)
    if np.isnan(obs):
        return obs, np.nan
    cnt = 0
    for _ in range(B):
        Mp = np.array([rng.permutation(row) for row in M])
        gp = profile(Mp)
        s = corr_frozen(gp, f)
        if not np.isnan(s) and s >= obs - 1e-12:
            cnt += 1
    return obs, (1 + cnt) / (1 + B)


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    prev = 0
    for rank, i in enumerate(o):
        val = min(1.0, (m - rank) * p[i])
        prev = max(prev, val)
        adj[i] = prev
    return adj


def bh(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        i = o[rank]
        val = min(prev, p[i] * m / (rank + 1))
        prev = val
        adj[i] = val
    return adj


# ---------------------------------------------------------------- 1. reproduccion UR1140
print('== 1. UR1140 ==')
u = bands('UR1140')
M = np.array([u['v'][b] for b in u['bands']])
print('cuerdas nivel0', u['n_all'], 'L modal', u['L'], 'bandas', len(u['bands']), 'matriz', M.shape)
print('eta2 posicion', round(eta2(M), 4))
rho, p_rho = perm_p_rho(M)
print('rho medio por pares', round(rho, 4), 'p', p_rho)
# fases: cuantas cuerdas iniciales de la banda caen en el grupo de espaciado anterior
ph = []
for b in u['bands']:
    t = 1
    while t < len(b) and u['grp'][b[t]] == u['grp'][b[0]]:
        t += 1
    ph.append(t)
print('fase (cuerdas en el grupo inicial) por banda', ph)
for tval in sorted(set(ph)):
    Mt = M[np.array(ph) == tval]
    print(f'fase t={tval}: n={len(Mt)} rho={rho_mean(Mt):.3f} perfil={np.round(np.nanmean(Mt, 0), 1)}')
# cruce con grupos de espaciado (unidad fisica)
cross = sum(len(set(u['grp'][b])) > 1 for b in u['bands'])
print('bandas que cruzan un grupo de espaciado:', cross, '/', len(u['bands']))

# control: unidad fisica = grupo de espaciado (cluster), 7 cuerdas B dentro de el
Mg = []
for g in sorted(set(u['grp']), key=lambda z: -z if z != 0 else 999):
    ix = np.flatnonzero(u['grp'] == g)
    sel = ix[u['col'][ix] == 'B']
    if len(sel) == 7:
        Mg.append(u['v'][sel])
Mg = np.array(Mg)
print('control cluster: 7 cuerdas B dentro del grupo, n', len(Mg), 'eta2', round(eta2(Mg), 3),
      'rho', round(rho_mean(Mg), 3))
rho_g, p_g = perm_p_rho(Mg)
print('  p(rho cluster)', p_g)
print('perfil cluster', np.round(np.nanmean(Mg, 0), 1))

# ficha congelada = perfil de las 15 rachas (definicion previa)
f_frozen = profile(M)
print('ficha congelada (15 rachas, z):', np.round(f_frozen, 3))
f_cluster = profile(Mg)
print('ficha alternativa (cluster, z):', np.round(f_cluster, 3))

# ---------------------------------------------------------------- 2. todos los quipus
print('\n== 2. aplicacion a Nazca / Berlin / Santa ==')
def setk(col, pat):
    return set(q[q[col].fillna('').str.contains(pat, case=False)].kfg)
naz = setk('procedencia', 'Nazca')
ber = setk('museo', 'Berlin')
san = setk('procedencia', r'^Santa$')
print('Nazca', len(naz), 'Berlin', len(ber), 'Santa', len(san), 'union', len(naz | ber | san))

rows = []
for k in sorted(naz | ber | san):
    b = bands(k)
    if b is None:
        rows.append(dict(khipu=k, L=np.nan, n_bandas=0, n_cuerdas=0, eta2=np.nan,
                         rho=np.nan, p=np.nan, rho_ficha=np.nan, p_ficha=np.nan,
                         en_nazca=k in naz, en_berlin=k in ber, en_santa=k in san))
        continue
    Mb = np.array([b['v'][x] for x in b['bands']])
    r = rho_mean(Mb)
    e = eta2(Mb)
    rf = corr_frozen(profile(Mb), f_frozen) if b['L'] == 7 else np.nan
    pf = np.nan
    if b['L'] == 7 and r is not None and len(Mb) >= 2:
        rf, pf = perm_p_frozen(Mb, f_frozen)
    rows.append(dict(khipu=k, L=b['L'], n_bandas=len(b['bands']), n_cuerdas=b['n_all'],
                     eta2=e, rho=r, p=(perm_p_rho(Mb)[1] if b['L'] == 7 else np.nan),
                     rho_ficha=rf, p_ficha=pf,
                     en_nazca=k in naz, en_berlin=k in ber, en_santa=k in san))
R = pd.DataFrame(rows)
R['p_ficha_adj_holm'] = np.nan
R['p_ficha_adj_bh'] = np.nan
R['p_holm_169'] = np.nan
R['p_bh_169'] = np.nan
test = R.p_ficha.notna() & (R.khipu != 'UR1140')
R.loc[test, 'p_ficha_adj_holm'] = holm(R.loc[test, 'p_ficha'].values)
R.loc[test, 'p_ficha_adj_bh'] = bh(R.loc[test, 'p_ficha'].values)
# correccion conservadora sobre los 169 quipus del universo (no testables = p 1)
R['p_holm_169'] = holm(R.p_ficha.fillna(1).values)
R['p_bh_169'] = bh(R.p_ficha.fillna(1).values)
R.to_csv(OUT / 'resultados_quipus.csv', index=False)

print('\n-- quipus con L=7 (mismos 7 campos) --')
print(R[R.L == 7][['khipu', 'n_bandas', 'eta2', 'rho', 'rho_ficha', 'p_ficha',
                   'p_ficha_adj_holm', 'p_ficha_adj_bh', 'p_holm_169', 'p_bh_169',
                   'en_nazca', 'en_berlin']]
      .to_string(index=False))
print('\n-- resumen por L --')
print(R.groupby('L').agg(n=('khipu', 'size'), rho_medio=('rho', 'mean')).to_string())
print('\nHolm<0.05 (12 testables):', R[(R.p_ficha_adj_holm < .05)].khipu.tolist())
print('BH<0.05 (12 testables):', R[(R.p_ficha_adj_bh < .05)].khipu.tolist())
print('Holm<0.05 (169 probados):', R[(R.p_holm_169 < .05)].khipu.tolist())
print('BH<0.05 (169 probados):', R[(R.p_bh_169 < .05)].khipu.tolist())

# cuantos quipus tienen >=2 bandas completas de 7
print('probados con ficha (L=7, >=2 bandas):', int(test.sum()), 'de', len(R))

# ---------------------------------------------------------------- control positivo Santa
print('\n== control positivo Santa (bandas de 6) ==')
srows = []
for k in sorted(san):
    b = bands(k)
    if b is None:
        srows.append(dict(khipu=k, L=np.nan, n_bandas=0, eta2=np.nan, rho=np.nan, p=np.nan))
        continue
    Mb = np.array([b['v'][x] for x in b['bands']])
    rr, pp = perm_p_rho(Mb, B=1999)
    srows.append(dict(khipu=k, L=b['L'], n_bandas=len(b['bands']), eta2=eta2(Mb), rho=rr, p=pp))
S = pd.DataFrame(srows)
S.to_csv(OUT / 'resultados_santa.csv', index=False)
print(S.to_string(index=False))

# ---------------------------------------------------------------- 3. copias / sumas entre fichas
cand = R[(R.p_ficha_adj_holm < .05) & (R.khipu != 'UR1140')].khipu.tolist()
print('\n== 3. copias/sumas entre candidatos ==', cand)
if len(cand) >= 2:
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            a, b = bands(cand[i]), bands(cand[j])
            Ma = np.array([a['v'][x] for x in a['bands']])
            Mb = np.array([b['v'][x] for x in b['bands']])
            if len(Ma) == len(Mb):
                ident = np.mean(Ma == Mb)
                print(cand[i], cand[j], 'celdas identicas', round(float(ident), 3))
            else:
                print(cand[i], cand[j], 'n bandas', len(Ma), len(Mb), 'no comparables 1:1')

# ---------------------------------------------------------------- OKR: estructura fisica UR1140
print('\n== OKR UR1140 ==')
con = sqlite3.connect(f'file:{(OUT.parents[2] / "data/external/open-khipu-repository/data/khipu.db").as_posix()}?mode=ro', uri=True)
cur = con.cursor()
kid = cur.execute("select KHIPU_ID from khipu_main where OKR_NUM='KH0156'").fetchone()[0]
cl = cur.execute("""select CLUSTER_ID, count(*) from cord where KHIPU_ID=? and CORD_LEVEL=1
                    group by CLUSTER_ID""", (kid,)).fetchall()
print('clusters nivel 1:', len(cl), 'tamanos:', sorted(set(x[1] for x in cl)))
print('attachment:', cur.execute("select ATTACHMENT_TYPE,count(*) from cord where KHIPU_ID=? and CORD_LEVEL=1 group by 1", (kid,)).fetchall())
print('terminacion:', cur.execute("select TERMINATION,count(*) from cord where KHIPU_ID=? and CORD_LEVEL=1 group by 1", (kid,)).fetchall())
con.close()

# guardar la ficha
pd.DataFrame({'posicion': np.arange(1, 8), 'perfil_z_15rachas': np.round(f_frozen, 4),
              'perfil_z_cluster': np.round(f_cluster, 4)}).to_csv(OUT / 'ficha7.csv', index=False)
print('\nescrito ficha7.csv')
