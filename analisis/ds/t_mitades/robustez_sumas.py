# -*- coding: utf-8 -*-
"""Robustez del test de simetria de sumas: mediana, signo y proporciones."""
import numpy as np, pandas as pd, json, warnings
warnings.filterwarnings('ignore')
B = 4000
rng = np.random.default_rng(20261018)

C = pd.read_csv('analisis/datos/cuerdas.csv', dtype=str)
C['nivel'] = pd.to_numeric(C['nivel'], errors='coerce')
C['orden'] = pd.to_numeric(C['orden'], errors='coerce')
C['v'] = pd.to_numeric(C['valor'], errors='coerce')
C['tiene'] = C['nudos'].notna() & (C['nudos'].fillna('').str.strip() != '')
C['vk'] = np.where(C['tiene'], C['v'], np.nan)
P = C[C['nivel'] == 0].sort_values(['kfg', 'orden'])

datos = []
for k, q in P.groupby('kfg', sort=False):
    n = len(q)
    if n < 6:
        continue
    m = n // 2
    v = q['vk'].values
    a, b = v[:m], v[n - m:]
    if np.sum(~np.isnan(a)) < 1 or np.sum(~np.isnan(b)) < 1:
        continue
    s1, s2 = np.nansum(a), np.nansum(b)
    if s1 <= 0 or s2 <= 0:
        continue
    datos.append((k, n, m, v))

print('quipus:', len(datos))
obs = np.array([np.log(s1 := np.nansum(v[:m]) / np.nansum(v[n - m:])) for (_, n, m, v) in datos])
obs_abs = np.abs(obs)
def stats(x):
    return dict(media_abs=float(np.mean(np.abs(x))), mediana_abs=float(np.median(np.abs(x))),
                frac_pos=float(np.mean(x > 0)), frac_igual=float(np.mean(x == 0)),
                frac_abs_005=float(np.mean(np.abs(x) < 0.05)))

# nulo: permutaciones dentro de cada quipu
medias, medianas, pos, eq, c05 = [], [], [], [], []
for b in range(B):
    x = []
    for (_, n, m, v) in datos:
        vp = rng.permutation(v)
        a, c = np.nansum(vp[:m]), np.nansum(vp[n - m:])
        x.append(np.log(a / c) if a > 0 and c > 0 else np.nan)
    x = np.array(x)
    medias.append(np.nanmean(np.abs(x)))
    medianas.append(np.nanmedian(np.abs(x)))
    pos.append(np.nanmean(x > 0))
    eq.append(np.nanmean(x == 0))
    c05.append(np.nanmean(np.abs(x) < 0.05))
res = {}
for nom, o, nl, lado in [('media_abs', stats(obs)['media_abs'], np.array(medias), 'lower'),
                         ('mediana_abs', stats(obs)['mediana_abs'], np.array(medianas), 'lower'),
                         ('frac_pos', stats(obs)['frac_pos'], np.array(pos), 'two'),
                         ('frac_igual', stats(obs)['frac_igual'], np.array(eq), 'upper'),
                         ('frac_abs_005', stats(obs)['frac_abs_005'], np.array(c05), 'upper')]:
    if lado == 'lower':
        p = (1 + np.sum(nl <= o)) / (B + 1)
    elif lado == 'upper':
        p = (1 + np.sum(nl >= o)) / (B + 1)
    else:
        p = min(1, 2 * min((1 + np.sum(nl <= o)) / (B + 1), (1 + np.sum(nl >= o)) / (B + 1)))
    res[nom] = dict(obs=float(o), null_mean=float(np.nanmean(nl)), null_sd=float(np.nanstd(nl)),
                    z=float((o - np.nanmean(nl)) / np.nanstd(nl)), p=float(p), lado=lado,
                    p_lower=float((1 + np.sum(nl <= o)) / (B + 1)),
                    p_upper=float((1 + np.sum(nl >= o)) / (B + 1)))
    print('%-14s obs=%8.4f nulo=%8.4f z=%7.2f p=%.5f' % (nom, o, np.nanmean(nl), res[nom]['z'], p))
print('descriptivo:', {k: round(v, 4) for k, v in stats(obs).items()})
print('percentiles |log|:', np.percentile(obs_abs, [10, 25, 50, 75, 90]).round(3).tolist())
json.dump(res, open('analisis/ds/t_mitades/robustez_sumas.json', 'w'), indent=1)
