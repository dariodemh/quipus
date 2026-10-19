# -*- coding: utf-8 -*-
"""
Dos mitades definidas por el CODIGO (no por la posicion): R/V, S/Z, AB/MB.
Se prueba si los dos conjuntos tienen el mismo numero de cuerdas y la misma suma
de valores, con permutacion de etiquetas dentro de cada quipu.

Unidad: el quipu.  B=5000, semilla fija.
Salida: totales.json
"""
import json, re, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
RUTA = 'analisis/datos/'
SEMILLA = 20261018
B = 5000
rng = np.random.default_rng(SEMILLA)

C = pd.read_csv(RUTA + 'cuerdas.csv', dtype=str)
C['nivel'] = pd.to_numeric(C['nivel'], errors='coerce')
C['orden'] = pd.to_numeric(C['orden'], errors='coerce')
C['v'] = pd.to_numeric(C['valor'], errors='coerce')
C['tiene'] = C['nudos'].notna() & (C['nudos'].fillna('').str.strip() != '')
C['vk'] = np.where(C['tiene'], C['v'], np.nan)

def dir_mayor(s):
    if not isinstance(s, str):
        return None
    d = [x for x in re.findall(r',([SZU])\)', s) if x in 'SZ']
    if not d:
        return None
    return 'S' if d.count('S') > d.count('Z') else ('Z' if d.count('Z') > d.count('S') else d[0])

def color_coarse(s):
    if not isinstance(s, str) or not s.strip():
        return None
    s = s.strip().upper().replace(' ', '').split('(')[0]
    for sep in (':', '/', '-', '_'):
        if sep in s:
            s = s.split(sep)[0]
            break
    return s if s else None

C['kd'] = C['nudos'].apply(dir_mayor)
C['col_c'] = C['color'].apply(color_coarse)
C['uni'] = C['union'].where(C['union'].isin(['R', 'V']))
P = C[C['nivel'] == 0].copy()

def perms(N, B, rng):
    return np.argsort(rng.random((B, N)), axis=1)

def pval(obs, agg, lado):
    if lado == 'lower':
        return (1 + np.sum(agg <= obs)) / (B + 1)
    if lado == 'upper':
        return (1 + np.sum(agg >= obs)) / (B + 1)
    pl = (1 + np.sum(agg <= obs)) / (B + 1)
    pu = (1 + np.sum(agg >= obs)) / (B + 1)
    return min(1.0, 2 * min(pl, pu))

def res(obs, null, lado, nombre, nq, extra=None):
    obs = np.asarray(obs, float); null = np.asarray(null, float)
    with np.errstate(invalid='ignore'):
        agg = np.nanmean(null, axis=0)
        o, mu, sd = np.nanmean(obs), np.nanmean(agg), np.nanstd(agg)
        pl = (1 + np.sum(agg <= o)) / (B + 1)
        pu = (1 + np.sum(agg >= o)) / (B + 1)
        p = pl if lado == 'lower' else (pu if lado == 'upper' else min(1.0, 2 * min(pl, pu)))
    d = dict(test=nombre, n_quipus=int(nq), obs=float(o), null_mean=float(mu),
             null_sd=float(sd), z=float((o - mu) / sd) if sd > 0 else np.nan,
             p=float(p), p_lower=float(pl), p_upper=float(pu),
             p_doscolas=float(min(1.0, 2 * min(pl, pu))), lado=lado)
    if extra:
        d.update(extra)
    return d

def test_par(col, a, b, nombre):
    """Suma y conteo de dos categorias; estadisticos |log(sa/sb)| y |na-nb|."""
    sobs, snull, cobs, cnull = [], [], [], []
    eobs, enull = [], []
    nq = 0
    for k, q in P.groupby('kfg', sort=False):
        x = q[col].values
        ok = np.array([z in (a, b) for z in x])
        if ok.sum() < 6 or len(set(x[ok])) < 2:
            continue
        xx = x[ok]; vv = q['vk'].values[ok]
        idx = perms(len(xx), B, rng); xp = xx[idx]
        sa = np.nansum(vv[xx == a]); sb = np.nansum(vv[xx == b])
        # sumas por categoria en cada permutacion
        s_a = np.array([np.nansum(vv[xp[t] == a]) for t in range(B)])
        s_b = np.array([np.nansum(vv[xp[t] == b]) for t in range(B)])
        if sa > 0 and sb > 0:
            sobs.append(abs(np.log(sa / sb)))
            with np.errstate(divide='ignore', invalid='ignore'):
                lr = np.abs(np.log(s_a / s_b))
            lr[~np.isfinite(lr)] = np.nan
            snull.append(lr)
        na, nb = int((xx == a).sum()), int((xx == b).sum())
        # equilibrio de conteos frente a Binomial(N, 0.5)
        N = na + nb
        cobs.append(abs(na - nb) / N)
        cn = np.array([abs(2 * rng.binomial(N, 0.5) - N) / N for _ in range(B)])
        cnull.append(cn)
        eobs.append(float(sa == sb and sa > 0))
        enull.append(((s_a == s_b) & (s_a > 0)).astype(float))
        nq += 1
    out = {}
    out[nombre + '_sumas'] = res(sobs, snull, 'lower', nombre + '_sumas', len(sobs),
                                 {'descripcion': 'media |log(suma_a/suma_b)|; menor = mas iguales'})
    out[nombre + '_conteos'] = res(cobs, cnull, 'lower', nombre + '_conteos', len(cobs),
                                   {'descripcion': 'media |n_a-n_b|/N; menor = mas equilibrado (nulo Binomial(N,0.5))'})
    out[nombre + '_sumas_igualdad'] = res(eobs, enull, 'upper', nombre + '_sumas_igualdad', len(eobs),
                                         {'descripcion': 'proporcion con sumas exactamente iguales'})
    return out

out = {}
for col, a, b, nom in [('uni', 'R', 'V', 'RV'),
                       ('kd', 'S', 'Z', 'SZ'),
                       ('col_c', 'AB', 'MB', 'ABMB')]:
    out.update(test_par(col, a, b, nom))

# pares adyacentes de grupos: igualdad exacta de sumas
C['gr'] = pd.to_numeric(C['grupo'], errors='coerce')
eq_obs, eq_null = [], []
for k, q in C.groupby('kfg', sort=False):
    gs = q.groupby('gr')['vk'].sum()
    gs = gs[gs > 0]
    G = len(gs)
    if G < 3:
        continue
    a = gs.values.astype(float)
    idx = perms(G, B, rng); ap = a[idx]
    eq_obs.append(float(np.mean(a[1:] == a[:-1])))
    eq_null.append(np.mean(ap[:, 1:] == ap[:, :-1], axis=1))
out['grupos_adyacentes_igualdad'] = res(eq_obs, eq_null, 'upper', 'grupos_adyacentes_igualdad',
                                        len(eq_obs), {'descripcion': 'proporcion de pares adyacentes con suma identica'})

with open('analisis/ds/t_mitades/totales.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

for k, v in out.items():
    print('%-28s obs=%9.4f nulo=%9.4f z=%7.2f p=%.5f n=%d' %
          (v['test'], v['obs'], v['null_mean'], v['z'], v['p'], v['n_quipus']))
