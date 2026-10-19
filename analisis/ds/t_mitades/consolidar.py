# -*- coding: utf-8 -*-
"""Consolida resultados, calcula BH-FDR exploratorio y descriptivos."""
import json
import numpy as np
import pandas as pd

base = 'analisis/ds/t_mitades/'
R = json.load(open(base + 'resultados.json'))
Bl = json.load(open(base + 'bloques.json'))
To = json.load(open(base + 'totales.json'))
Dg = json.load(open(base + 'dentro_grupo.json'))
Rb = json.load(open(base + 'robustez_sumas.json'))

print('=== FAMILIA PRIMARIA (12, Holm) ===')
for r in R['familia']:
    print('%-30s obs=%8.4f nulo=%8.4f z=%7.2f p=%.4f p_holm=%.4f' %
          (r['test'], r['obs'], r['null_mean'], r['z'], r['p'], r['p_holm']))

explor = []
for src, d in [('B', Bl), ('T', To), ('D', Dg)]:
    for k, v in d.items():
        if isinstance(v, dict) and 'p' in v and 'test' in v:
            explor.append(dict(test=v['test'], obs=v['obs'], null=v['null_mean'], z=v['z'],
                               p=v.get('p_doscolas', v['p']), p_dir=v['p'],
                               pl=v.get('p_lower'), pu=v.get('p_upper'), n=v['n_quipus'], fuente=src))
for k, v in Rb.items():
    explor.append(dict(test='robustez_' + k, obs=v['obs'], null=v['null_mean'], z=v['z'],
                       p=v['p'], p_dir=v['p'], pl=v.get('p_lower'), pu=v.get('p_upper'),
                       n=570, fuente='R'))
# BH-FDR
ps = np.array([e['p'] for e in explor])
m = len(ps)
o = np.argsort(ps)
q = np.empty(m)
prev = 1.0
for rank in range(m - 1, -1, -1):
    i = o[rank]
    val = min(prev, ps[i] * m / (rank + 1))
    q[i] = val
    prev = val
for e, qq in zip(explor, q):
    e['q_bh'] = float(qq)
print('\n=== EXPLORATORIOS (BH-FDR, m=%d) ===' % m)
for e in sorted(explor, key=lambda z: z['p']):
    print('%-38s obs=%8.4f nulo=%8.4f z=%7.2f p=%.5f q=%.4f n=%d [%s]' %
          (e['test'], e['obs'], e['null'], e['z'], e['p'], e['q_bh'], e['n'], e['fuente']))

# ---------------------------------------------------------- descriptivos
C = pd.read_csv('analisis/datos/cuerdas.csv', dtype=str)
C['nivel'] = pd.to_numeric(C['nivel'], errors='coerce')
C['orden'] = pd.to_numeric(C['orden'], errors='coerce')
C['v'] = pd.to_numeric(C['valor'], errors='coerce')
C['tiene'] = C['nudos'].notna() & (C['nudos'].fillna('').str.strip() != '')
C['vk'] = np.where(C['tiene'], C['v'], np.nan)
import re
def dm(s):
    if not isinstance(s, str): return None
    d = [x for x in re.findall(r',([SZU])\)', s) if x in 'SZ']
    if not d: return None
    return 'S' if d.count('S') > d.count('Z') else ('Z' if d.count('Z') > d.count('S') else d[0])
C['kd'] = C['nudos'].apply(dm)
C['uni'] = C['union'].where(C['union'].isin(['R', 'V']))
C['tor'] = C['torsion'].where(C['torsion'].isin(['S', 'Z']))
P = C[C['nivel'] == 0].copy()

def uniformidad(col, vals):
    g = P.groupby('kfg')[col].apply(lambda s: set(x for x in s if x in vals))
    n = g.apply(len)
    return dict(con_datos=int((n > 0).sum()), mixtos=int((n > 1).sum()),
                pct_mixtos=round(float((n > 1).sum() / (n > 0).sum() * 100), 1))
desc = {}
desc['union'] = uniformidad('uni', ('R', 'V'))
desc['direccion'] = uniformidad('kd', ('S', 'Z'))
desc['torsion'] = uniformidad('tor', ('S', 'Z'))

# distribucion de rachas y splits de 2 bloques
def runs_list(col, vals, minn=6):
    out = []
    for k, q in P.groupby('kfg'):
        s = [x for x in q[col].values if x in vals]
        if len(s) < minn or len(set(s)) < 2: continue
        ch = [i for i in range(1, len(s)) if s[i] != s[i - 1]]
        out.append((len(s), len(ch) + 1, ch[0] / len(s) if len(ch) == 1 else np.nan))
    return pd.DataFrame(out, columns=['n', 'rachas', 'split'])
for col, vals in [('uni', ('R', 'V')), ('kd', ('S', 'Z'))]:
    d = runs_list(col, vals)
    desc[col + '_rachas'] = {'n': int(len(d)), 'rachas_2': int((d.rachas == 2).sum()),
                             'frac_2': round(float((d.rachas == 2).mean()), 3)}
    d2 = d[d.rachas == 2]
    desc[col + '_2bloques'] = {'n': int(len(d2)),
                               'split_mediana': round(float(d2.split.median()), 3),
                               'IQR': [round(float(d2.split.quantile(.25)), 3), round(float(d2.split.quantile(.75)), 3)],
                               'frac_split_0.4_0.6': round(float(((d2.split >= .4) & (d2.split <= .6)).mean()), 3)}

# suma de mitades descriptiva
t = pd.read_csv(base + 'por_quipu.csv')
t['signed'] = np.log(t.s1 / t.s2)
desc['sumas'] = {'n': int(len(t)), 'mediana_ratio': round(float((t.s1 / t.s2).median()), 3),
                 'IQR_ratio': [round(float((t.s1 / t.s2).quantile(.25)), 3), round(float((t.s1 / t.s2).quantile(.75)), 3)],
                 'pct_s1_mayor': round(float((t.s1 > t.s2).mean() * 100), 1),
                 'pct_exactamente_igual': round(float((t.s1 == t.s2).mean() * 100), 2)}

desc['n_quipus'] = int(P.kfg.nunique())
desc['n_pendientes'] = int(len(P))
desc['quipus_n6'] = int((P.groupby('kfg').size() >= 6).sum())
json.dump(desc, open(base + 'descriptivos.json', 'w'), indent=1)
print('\n=== DESCRIPTIVOS ===')
for k, v in desc.items():
    print(k, v)
