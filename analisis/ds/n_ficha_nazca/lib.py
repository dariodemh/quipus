"""Utilidades comunes: carga, registros de n campos + 2 marcadoras, perfiles y tests."""
import re, numpy as np, pandas as pd
from pathlib import Path
from collections import Counter

OUT = Path(__file__).resolve().parent
DAT = OUT.parents[1] / 'datos'
RNG = np.random.default_rng(20261018)

def load():
    c = pd.read_csv(DAT / 'cuerdas.csv', low_memory=False).drop_duplicates(['kfg', 'cuerda'])
    c['v'] = np.where(c.nudos.notna() & (c.nudos.astype(str).str.strip() != ''), c.valor, np.nan)
    c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())
    c['nudos'] = c.nudos.fillna('').astype(str)
    c['dirs'] = c.nudos.map(lambda s: ''.join(sorted(Counter(re.findall(r'\d+[SLE]+\([^,]*,\s*([SZU])\)', s)))) or '')
    c['dir1'] = c.nudos.map(lambda s: (re.findall(r'\d+[SLE]+\([^,]*,\s*([SZU])\)', s) or [''])[0])
    return c

def records(c, k, size=9, nmark=2):
    """Registros = grupos de `size` cuerdas nivel 0 con exactamente `nmark` cuerdas de
    color distinto al modal. Devuelve dicts con atributos de campo y marcador."""
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    out = []
    for g, dd in d.groupby('grupo', sort=False):
        if len(dd) != size:
            continue
        cols = list(dd.col); cnt = Counter(cols); maj, nm = cnt.most_common(1)[0]
        if nm != size - nmark or cnt[maj] != size - nmark:
            continue
        mark = [i for i, x in enumerate(cols) if x != maj]
        if len(mark) != nmark:
            continue
        f = dd[dd.col == maj]
        m = dd[dd.col != maj]
        out.append(dict(g=int(g), size=size, maj=maj, pos=tuple(i + 1 for i in mark),
                        vals=f.v.to_numpy(float), fields=f,
                        mcol=[x for x in m.col], mval=m.v.to_numpy(float),
                        mtor=list(m.torsion.fillna('?')), muni=list(m.union.fillna('?')),
                        mdir=list(m.dir1), mfield=[x for x in m.cuerda],
                        tot=float(np.nansum(f.v.to_numpy(float)))))
    return out

def canon(v, pos, size=9, rule='second'):
    """Orienta el vector de n campos. 'second': invierte si la 2a marcadora esta en pos >= size/2+1."""
    if rule == 'second':
        inv = pos[-1] >= (size // 2 + 1)
    elif rule == 'center':
        inv = np.mean(pos) > (size + 1) / 2
    else:  # none
        inv = False
    return v[::-1] if inv else v

def prof(M):
    P = []
    for r in M:
        if np.ptp(r) == 0 or np.isnan(r).any():
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

def perm_p(M, f, sl=slice(None), B=9999, rng=None):
    rng = rng or RNG
    obs = corr(prof(M)[sl], f[sl])
    if np.isnan(obs):
        return obs, np.nan
    cnt = 0
    for _ in range(B):
        Mp = np.array([rng.permutation(row) for row in M])
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

def maxfrac(M):
    """Fraccion de registros con maximo en el campo 1."""
    if len(M) == 0:
        return np.nan, 0
    return float(np.mean([np.nanargmax(r) == 0 for r in M])), len(M)
