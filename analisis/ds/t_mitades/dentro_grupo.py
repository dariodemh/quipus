# -*- coding: utf-8 -*-
"""
Mitades DENTRO de cada grupo de colgantes (unidad natural de ~6-20 cuerdas):
sumas, colores y dicotomias R/V y S/Z.  Nulo: permutacion dentro del grupo.

Unidad de inferencia: el quipu (promedio de sus grupos).  B=2000.
Salida: dentro_grupo.json
"""
import json, re, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
RUTA = 'analisis/datos/'
SEMILLA = 20261018
B = 2000
rng = np.random.default_rng(SEMILLA)

C = pd.read_csv(RUTA + 'cuerdas.csv', dtype=str)
C['nivel'] = pd.to_numeric(C['nivel'], errors='coerce')
C['orden'] = pd.to_numeric(C['orden'], errors='coerce')
C['v'] = pd.to_numeric(C['valor'], errors='coerce')
C['tiene'] = C['nudos'].notna() & (C['nudos'].fillna('').str.strip() != '')
C['vk'] = np.where(C['tiene'], C['v'], np.nan)
C['gr'] = pd.to_numeric(C['grupo'], errors='coerce')

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

sum_obs, sum_null, eq_obs, eq_null = [], [], [], []
col_obs, col_null = [], []
kd_obs, kd_null, uni_obs, uni_null = [], [], [], []
n_grupos_tot = 0

for k, q in P.groupby('kfg', sort=False):
    sg, sg_null, eg, eg_null = [], [], [], []
    cg, cg_null, dg, dg_null, ug, ug_null = [], [], [], [], [], []
    for g, qq in q.groupby('gr', sort=False):
        n = len(qq)
        if n < 4:
            continue
        m = n // 2
        # --- sumas
        v = qq['vk'].values
        if np.sum(~np.isnan(v[:m])) >= 1 and np.sum(~np.isnan(v[n - m:])) >= 1:
            s1, s2 = np.nansum(v[:m]), np.nansum(v[n - m:])
            if s1 > 0 and s2 > 0:
                sg.append(abs(np.log(s1 / s2)))
                eg.append(float(s1 == s2))
                idx = perms(n, B, rng); vp = v[idx]
                a = np.nansum(vp[:, :m], axis=1); b = np.nansum(vp[:, m:], axis=1)
                with np.errstate(divide='ignore', invalid='ignore'):
                    dd = np.abs(np.log(a / b)); dd[~np.isfinite(dd)] = np.nan
                sg_null.append(dd)
                eg_null.append(((a == b) & (a > 0)).astype(float))
                n_grupos_tot += 1
        # --- color espejo dentro del grupo
        col = qq['col_c'].values
        pres = np.array([isinstance(x, str) for x in col])
        pares = [(i, n - 1 - i) for i in range(m)]
        idx = perms(n, B, rng)
        def mc(order):
            x = col[order]
            ok = np.array([isinstance(y, str) for y in x])
            good = [ok[i] and ok[j] for i, j in pares]
            if sum(good) < 2:
                return np.nan
            return np.mean([x[i] == x[j] for (i, j), gd in zip(pares, good) if gd])
        o = mc(np.arange(n))
        if not np.isnan(o):
            cg.append(o)
            cg_null.append(np.array([mc(idx[t]) for t in range(B)]))
        # --- dicotomias dentro del grupo
        for colname, etiq, so, sn in [('kd', ('S', 'Z'), dg, dg_null),
                                      ('uni', ('R', 'V'), ug, ug_null)]:
            x0 = qq[colname].values
            ok = np.array([z in etiq for z in x0])
            if ok.sum() < 4:
                continue
            xx = x0[ok]
            # posiciones dentro del grupo recalculadas sobre las presentes
            pos = np.arange(n)[ok]
            prim = pos < m
            if prim.sum() < 1 or (~prim).sum() < 1:
                continue
            p1 = np.mean(xx[prim] == etiq[0]); p2 = np.mean(xx[~prim] == etiq[0])
            dd = p1 - p2
            idx2 = perms(len(xx), B, rng); xp = xx[idx2]
            m1 = int(prim.sum())
            dn = np.mean(xp[:, :m1] == etiq[0], axis=1) - np.mean(xp[:, m1:] == etiq[0], axis=1)
            so.append(dd); sn.append(dn)
    if sg:
        sum_obs.append(np.mean(sg)); sum_null.append(np.nanmean(np.array(sg_null), axis=0))
        eq_obs.append(np.mean(eg)); eq_null.append(np.nanmean(np.array(eg_null), axis=0))
    if cg:
        col_obs.append(np.mean(cg)); col_null.append(np.nanmean(np.array(cg_null), axis=0))
    if dg:
        kd_obs.append(np.mean(dg)); kd_null.append(np.nanmean(np.array(dg_null), axis=0))
    if ug:
        uni_obs.append(np.mean(ug)); uni_null.append(np.nanmean(np.array(ug_null), axis=0))

out = {}
out['suma_dentro_grupo'] = res(sum_obs, sum_null, 'lower', 'suma_dentro_grupo', len(sum_obs),
                               {'n_grupos': n_grupos_tot})
out['suma_dentro_grupo_igualdad'] = res(eq_obs, eq_null, 'upper', 'suma_dentro_grupo_igualdad', len(eq_obs))
out['color_espejo_dentro_grupo'] = res(col_obs, col_null, 'upper', 'color_espejo_dentro_grupo', len(col_obs))
out['dir_dentro_grupo'] = res(kd_obs, kd_null, 'two', 'dir_dentro_grupo', len(kd_obs))
out['union_dentro_grupo'] = res(uni_obs, uni_null, 'two', 'union_dentro_grupo', len(uni_obs))

with open('analisis/ds/t_mitades/dentro_grupo.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

for k, v in out.items():
    print('%-32s obs=%8.4f nulo=%8.4f z=%7.2f p=%.4f n=%d' %
          (v['test'], v['obs'], v['null_mean'], v['z'], v['p'], v['n_quipus']))
