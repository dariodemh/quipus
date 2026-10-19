# -*- coding: utf-8 -*-
"""
¿Color / torsión / unión funcionan como CLASIFICADORES (etiquetas de clase)
o como código combinatorio libre (tipo silábico)?

Unidad de análisis: el quipu. Nulo: permutar la etiqueta DENTRO de cada quipu.
Semilla fija. Versión vectorizada.
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json, re, time
import numpy as np
import pandas as pd
from scipy import stats

RNG = np.random.default_rng(20261018)
NPERM = 400

d = pd.read_csv('../../datos/cuerdas.csv')

def base_color(c):
    if not isinstance(c, str) or c.strip() == '':
        return None
    m = re.match(r'([A-Z]{1,2})', c.strip())
    return m.group(1) if m else 'OTRO'

d['col'] = d.color.map(base_color)
d['tor'] = d.torsion.where(d.torsion.isin(['S', 'Z']))
d['uni'] = d.union.where(d.union.isin(['R', 'V', 'T']))
d['gid'] = d.kfg + '|' + d.grupo.astype(str)
d['qcode'] = pd.factorize(d.kfg)[0]
d['gcode'] = pd.factorize(d.gid)[0]

# --- estadístico de segregación por grupo ------------------------------------
def setup(var):
    sub = d.loc[d[var].notna(), ['qcode', 'gcode', var]].copy()
    sub['x'] = pd.factorize(sub[var])[0]
    # grupos con >=2 cuerdas
    gs = sub.groupby('gcode').size()
    sub = sub[sub.gcode.isin(gs[gs >= 2].index)]
    return sub

def assort_fast(sub):
    """devuelve (O, E, P, n) global; O=pares mismo valor dentro de grupo."""
    n = len(sub)
    g = sub.gcode.values.astype(np.int64)
    x = sub.x.values.astype(np.int64)
    q = sub.qcode.values.astype(np.int64)
    K = int(x.max()) + 1
    # celda grupo x valor
    cell = g * K + x
    cnt = np.bincount(cell)
    O = float((cnt * (cnt - 1)).sum())
    # tamaños de grupo
    ng = np.bincount(g)
    P = float((ng * (ng - 1)).sum())
    # composición por quipu
    nq = np.bincount(q, minlength=q.max() + 1)
    cellq = q * K + x
    cq = np.bincount(cellq, minlength=len(nq) * K)
    # E = suma_q P_q * [sum_c n_qc(n_qc-1)] / [n_q(n_q-1)]
    dfg = pd.DataFrame({'g': g, 'q': q}).drop_duplicates('g')
    dfg['ng'] = ng[dfg.g.values]
    Pq = dfg.groupby('q').ng.apply(lambda s: (s * (s - 1)).sum()).reindex(range(len(nq)), fill_value=0).values
    pairs_q = (cq * (cq - 1)).reshape(len(nq), K).sum(axis=1)
    denom = nq * (nq - 1)
    E = float(np.nansum(np.where(denom > 0, Pq * pairs_q / denom, 0)))
    return O, E, P, n

def assort_perm(sub, nperm=NPERM):
    """devuelve media del estadístico ponderado bajo permutación dentro de quipu."""
    q = sub.qcode.values
    vals = []
    idx_by_q = [np.where(q == k)[0] for k in range(q.max() + 1)]
    for _ in range(nperm):
        s = sub.copy()
        x = s.x.values.copy()
        for ii in idx_by_q:
            x[ii] = x[RNG.permutation(ii)]
        s['x'] = x
        O, E, P, n = assort_fast(s)
        vals.append((O - E) / (P - E) if P > E else np.nan)
    return np.array(vals)

out = {}
per_quipu = []
t0 = time.time()
for var in ['col', 'tor', 'uni']:
    sub = setup(var)
    O, E, P, n = assort_fast(sub)
    obs = (O - E) / (P - E)
    null = assort_perm(sub)
    p = (1 + np.sum(null >= obs)) / (1 + len(null))
    # por quipu (unidad de análisis)
    rows = []
    for k, g in sub.groupby('qcode'):
        if len(g) < 3:
            continue
        Oi, Ei, Pi, ni = assort_fast(g)
        if Pi > Ei:
            rows.append((k, (Oi - Ei) / (Pi - Ei), Pi))
    r = pd.DataFrame(rows, columns=['qcode', 'assort', 'pares'])
    pos = int((r.assort > 0).sum()); neg = int((r.assort < 0).sum())
    sign_p = stats.binomtest(pos, pos + neg, 0.5, alternative='greater').pvalue
    out[var] = dict(n_quipus=int(len(r)), obs=float(obs),
                    null_mean=float(np.nanmean(null)), null_sd=float(np.nanstd(null)),
                    p_perm=float(p), median=float(r.assort.median()),
                    q25=float(r.assort.quantile(.25)), q75=float(r.assort.quantile(.75)),
                    frac_pos=float(pos / max(1, pos + neg)), sign_p=float(sign_p))
    r['var'] = var
    per_quipu.append(r)
    print(var, out[var], 'tiempo', round(time.time() - t0, 1))

pd.concat(per_quipu).to_csv('clases_por_quipu.csv', index=False)

# --- combinaciones color x torsion x union libres o constreñidas --------------
sub = d[['qcode', 'col', 'tor', 'uni']].dropna()
rows = []
for k, g in sub.groupby('qcode'):
    n = len(g)
    if n < 6:
        continue
    obs = g.groupby(['col', 'tor', 'uni'], observed=True).ngroups
    pc = g.col.value_counts(normalize=True).values
    pt = g.tor.value_counts(normalize=True).values
    pu = g.uni.value_counts(normalize=True).values
    exp = sum(1 - (1 - a * b * c) ** n for a in pc for b in pt for c in pu)
    rows.append((k, n, obs, exp, obs / exp, len(pc), len(pt), len(pu)))
cmb = pd.DataFrame(rows, columns=['qcode', 'n', 'obs', 'exp', 'ratio', 'ncol', 'ntor', 'nuni'])
out['combinaciones'] = dict(n_quipus=int(len(cmb)),
                            med_n=float(cmb.n.median()),
                            med_obs=float(cmb.obs.median()), med_exp=float(cmb.exp.median()),
                            med_ratio=float(cmb.ratio.median()),
                            q25=float(cmb.ratio.quantile(.25)), q75=float(cmb.ratio.quantile(.75)),
                            frac_ratio_lt1=float((cmb.ratio < 1).mean()))
cmb.to_csv('combinaciones_por_quipu.csv', index=False)
print('combinaciones', out['combinaciones'])

# --- color y magnitud numérica ------------------------------------------------
def mag(v):
    v = abs(v)
    return 0 if v == 0 else int(np.floor(np.log10(v))) + 1
d['valor_num'] = pd.to_numeric(d.valor, errors='coerce')
d['mag'] = d.valor_num.map(lambda v: np.nan if pd.isna(v) else mag(v))
sub = d.loc[d.nudos.notna() & d.valor_num.notna(), ['qcode', 'col', 'mag']].dropna()

def eta_global(s):
    nq = s.groupby('qcode').size()
    sy = s.groupby('qcode').mag.sum()
    sy2 = s.groupby('qcode').mag.apply(lambda x: (x ** 2).sum())
    sst = (sy2 - sy ** 2 / nq)
    cell = s.groupby(['qcode', 'col']).mag.agg(['size', 'sum'])
    cell['ssb'] = cell['sum'] ** 2 / cell['size']
    ssb = cell.groupby('qcode').ssb.sum() - sy ** 2 / nq
    eta = (ssb / sst).replace([np.inf, -np.inf], np.nan).dropna()
    return eta[eta.index.isin(nq[nq >= 10].index)].mean()

obs_eta = eta_global(sub)
null_eta = []
for _ in range(300):
    s = sub.copy()
    s['mag'] = s.groupby('qcode')['mag'].transform(lambda x: RNG.permutation(x.values))
    null_eta.append(eta_global(s))
p_eta = (1 + np.sum(np.array(null_eta) >= obs_eta)) / (1 + len(null_eta))
out['color_magnitud'] = dict(eta2=float(obs_eta), null=float(np.mean(null_eta)),
                             p_perm=float(p_eta))
print('color_magnitud', out['color_magnitud'])

# --- Holm --------------------------------------------------------------------
tests = {'color_grupo': out['col']['p_perm'], 'torsion_grupo': out['tor']['p_perm'],
         'union_grupo': out['uni']['p_perm'], 'color_magnitud': out['color_magnitud']['p_perm']}
order = sorted(tests, key=tests.get)
holm = {}; prev = 0
for i, k in enumerate(order):
    val = max(min(1, (len(order) - i) * tests[k]), prev); prev = val
    holm[k] = val
out['tests'] = tests
out['holm'] = holm

with open('resultados_clases.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
