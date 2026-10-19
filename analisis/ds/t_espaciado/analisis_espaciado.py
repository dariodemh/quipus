"""¿El espaciado entre grupos marca secciones con aritmética distinta?

Tests (unidad = quipu; nulo = permutación dentro de quipu):
  A. ¿Los gaps grandes separan grupos más distintos en valor/tamaño/color?
  B. ¿Los grupos con estructura aritmética KFG (sumas, bandas, series decrecientes)
     están más aislados por gaps?
  C. ¿Las relaciones de suma cruzan menos gaps grandes que ventanas aleatorias del
     mismo quipu y longitud?
"""
import os
import re
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'derived')
R = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
REL = os.path.join(R, 'data', 'external', 'data-science-khipu-article', 'data', 'ascher_sum_relations')
SEED = 20261017
NPERM = 4000

g = pd.read_pickle(os.path.join(D, 'grupos.pkl'))
g = g.sort_values(['kfg', 'grupo']).reset_index(drop=True)
pd.set_option('display.width', 180)

# ------------------ A. pares de grupos consecutivos ------------------
pairs = []
for k, d in g.groupby('kfg'):
    d = d.reset_index(drop=True)
    for i in range(len(d) - 1):
        a, b = d.iloc[i], d.iloc[i + 1]
        if pd.isna(a.gap) or a.n_con_nudos == 0 or b.n_con_nudos == 0:
            continue
        pairs.append(dict(kfg=k, gi=a.grupo, gap=a.gap, gap_dpos=a.gap_dpos,
                          n_a=a.n_cuerdas, n_b=b.n_cuerdas,
                          dv=abs(a.logv_mean - b.logv_mean),
                          dnd=abs(a.ndig_max - b.ndig_max),
                          dcl=abs(a.ncl_mean - b.ncl_mean),
                          dl=abs(a.largo_mean - b.largo_mean),
                          dn=abs(a.n_cuerdas - b.n_cuerdas),
                          dent=abs(a.color_ent - b.color_ent)))
P = pd.DataFrame(pairs)
print('=== A. pares consecutivos ===')
print('pares utilizables:', len(P), 'quipus:', P.kfg.nunique())
print('quipus con >=4 pares:', int((P.groupby('kfg').size() >= 4).sum()))


def corr_gap_delta(P, col, min_pairs=4, nperm=NPERM, seed=SEED):
    unidades = []
    for k, d in P.groupby('kfg'):
        d = d.dropna(subset=['gap', col])
        if len(d) < min_pairs or d.gap.nunique() < 2:
            continue
        x = stats.rankdata(d.gap); x -= x.mean()
        y = stats.rankdata(d[col]); y -= y.mean()
        unidades.append((x, y))
    if not unidades:
        return None

    def rho(x, y):
        return float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))
    obs = np.mean([rho(x, y) for x, y in unidades])
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for b in range(nperm):
        s = 0.0
        for x, y in unidades:
            s += rho(rng.permutation(x), y)
        null[b] = s / len(unidades)
    return dict(n_quipus=len(unidades), obs=obs, null_sd=null.std(),
                p_pos=(1 + np.sum(null >= obs)) / (nperm + 1),
                p_dos=(1 + np.sum(np.abs(null) >= abs(obs))) / (nperm + 1),
                frac_pos=float(np.mean([rho(x, y) > 0 for x, y in unidades])))


print('\n--- A1. Spearman(gap, |delta feature|) dentro de quipu ---')
resA = {}
for col in ['dv', 'dnd', 'dcl', 'dl', 'dn', 'dent']:
    r = corr_gap_delta(P, col, nperm=2000)
    resA[col] = r
    if r:
        print(f'{col}: rho={r["obs"]:.3f} (sd null {r["null_sd"]:.3f}), '
              f'p_pos={r["p_pos"]:.4f}, p_dos={r["p_dos"]:.4f}, frac+={r["frac_pos"]:.2f}, n={r["n_quipus"]}')

# A2. big gap vs small gap: diferencia de |delta| (más robusto a empates)
print('\n--- A2. gap grande (> percentil 75 del quipu) vs pequeño ---')


def big_small(P, col, q=0.75, nperm=2000, seed=SEED, min_pairs=4):
    unidades = []
    for k, d in P.groupby('kfg'):
        d = d.dropna(subset=['gap', col])
        if len(d) < min_pairs or d.gap.nunique() < 2:
            continue
        thr = d.gap.quantile(q)
        big = d.gap > thr
        if big.sum() < 1 or (~big).sum() < 1:
            continue
        unidades.append((d[col].values, big.values))
    if not unidades:
        return None

    def stat(us):
        vals = []
        for y, b in us:
            vals.append(y[b].mean() - y[~b].mean())
        return float(np.mean(vals))
    obs = stat(unidades)
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for i in range(nperm):
        null[i] = stat([(y, rng.permutation(b)) for y, b in unidades])
    return dict(n_quipus=len(unidades), obs=obs, null_sd=null.std(),
                p=(1 + np.sum(null >= obs)) / (nperm + 1),
                frac_pos=float(np.mean([y[b].mean() - y[~b].mean() > 0 for y, b in unidades])))


resA2 = {}
for col in ['dv', 'dnd', 'dcl', 'dl', 'dent']:
    r = big_small(P, col, nperm=2000)
    resA2[col] = r
    if r:
        print(f'{col}: dif={r["obs"]:.3f} (sd {r["null_sd"]:.3f}), p={r["p"]:.4f}, frac+={r["frac_pos"]:.2f}, n={r["n_quipus"]}')

# ------------------ B. grupos con estructura aritmética ------------------
print('\n=== B. estructura aritmética y aislamiento ===')
flags = g[['kfg', 'grupo', 'gap', 'gap_dpos', 'n_pend', 'n_cuerdas']].copy()
flags['dec'] = 0; flags['band'] = 0; flags['csum'] = 0

dec = pd.read_csv(os.path.join(REL, 'ascher_decreasing_cluster_relation.csv'))
for r in dec.itertuples():
    flags.loc[(flags.kfg == r.name) & (flags.grupo == r.cluster_position), 'dec'] = 1
band = pd.read_csv(os.path.join(REL, 'cluster_sum_bands_relation.csv'))
for r in band.itertuples():
    flags.loc[(flags.kfg == r.name) & (flags.grupo == r.cluster_position), 'band'] = 1
cs = pd.read_csv(os.path.join(REL, 'cluster_cluster_sum_relation.csv'))
for r in cs.itertuples():
    flags.loc[(flags.kfg == r.name) & (flags.grupo == r.left_cluster_position), 'csum'] = 1
    flags.loc[(flags.kfg == r.name) & (flags.grupo == r.right_cluster_position), 'csum'] = 1
flags['arit'] = flags[['dec', 'band', 'csum']].max(axis=1)
print('grupos con flag:', {c: int(flags[c].sum()) for c in ['dec', 'band', 'csum', 'arit']},
      '| quipus con algún flag:', flags[flags.arit == 1].kfg.nunique())

# gap antes y después
flags['gap_before'] = flags.groupby('kfg').gap.shift(1)
flags['gap_after'] = flags.gap
flags['gap_max'] = flags[['gap_before', 'gap_after']].max(axis=1)
flags['gap_sum'] = flags[['gap_before', 'gap_after']].sum(axis=1, min_count=1)

# Para el test: rank del gap dentro de quipu; comparar flagged vs no flagged
def perm_flag(flags, col, flagcol='arit', nperm=4000, seed=SEED, match_npend=False):
    unidades = []
    for k, d in flags.groupby('kfg'):
        d = d.dropna(subset=[col])
        if d[flagcol].nunique() < 2 or len(d) < 3:
            continue
        if match_npend:
            # comparar solo dentro de estratos de n_pend
            for npend, e in d.groupby('n_pend'):
                if e[flagcol].nunique() < 2 or len(e) < 2:
                    continue
                unidades.append((e[col].values, e[flagcol].values.astype(bool)))
        else:
            unidades.append((d[col].values, d[flagcol].values.astype(bool)))
    if not unidades:
        return None

    def stat(us):
        dif = [y[b].mean() - y[~b].mean() for y, b in us if b.sum() > 0 and (~b).sum() > 0]
        return float(np.mean(dif)) if dif else np.nan
    obs = stat(unidades)
    rng = np.random.default_rng(seed)
    null = np.empty(nperm)
    for i in range(nperm):
        null[i] = stat([(y, rng.permutation(b)) for y, b in unidades])
    return dict(n_unidades=len(unidades), obs=obs, null_sd=np.nanstd(null),
                p=(1 + np.nansum(null >= obs)) / (nperm + 1),
                frac_pos=float(np.nanmean([y[b].mean() - y[~b].mean() > 0 for y, b in unidades])))


print('\n--- B1. gap (cm) en grupos con estructura aritmética ---')
resB = {}
for col in ['gap_after', 'gap_before', 'gap_max', 'gap_sum']:
    r = perm_flag(flags, col, nperm=3000)
    resB[col] = r
    if r:
        print(f'{col}: dif={r["obs"]:.3f} (sd {r["null_sd"]:.3f}), p={r["p"]:.4f}, frac+={r["frac_pos"]:.2f}, n={r["n_unidades"]}')
print('--- B2. controlando tamaño del grupo (estratos n_pend) ---')
resB2 = {}
for col in ['gap_after', 'gap_max']:
    r = perm_flag(flags, col, nperm=3000, match_npend=True)
    resB2[col] = r
    if r:
        print(f'{col}: dif={r["obs"]:.3f} (sd {r["null_sd"]:.3f}), p={r["p"]:.4f}, frac+={r["frac_pos"]:.2f}, n={r["n_unidades"]}')

# ------------------ C. relaciones de suma y fronteras ------------------
print('\n=== C. ¿las sumas cruzan gaps grandes? ===')
contig = g.groupby('kfg').grupo.apply(lambda x: np.array_equal(x.values, np.arange(len(x))))
contig_k = set(contig[contig].index)
print('quipus con índices de grupo contiguos:', len(contig_k), '/', len(contig))
# C1. cluster-cluster sums: left/right son índices de grupo
cs = cs[cs.name.isin(g.kfg.unique())].copy()
cs['lo'] = cs[['left_cluster_position', 'right_cluster_position']].min(axis=1)
cs['hi'] = cs[['left_cluster_position', 'right_cluster_position']].max(axis=1)
cs['span'] = cs.hi - cs.lo
cs = cs[(cs.span > 0) & cs.name.isin(contig_k)]
print('cluster-cluster sums con span>0:', len(cs), 'quipus', cs.name.nunique())


def cruces(df, kfgcol, locol, hicol, span, gapserie, thr=2.0, nperm=3000, seed=SEED):
    """Nº de gaps >=thr entre lo y hi; nulo = ventana aleatoria del mismo span en el quipu.

    Test global: media observada vs distribución nula de la media (misma permutación
    para todas las relaciones), lo que preserva la composición de spans y quipus.
    """
    rng = np.random.default_rng(seed)
    obs = []
    draws = []
    for r in df.itertuples():
        k = getattr(r, kfgcol)
        lo = int(getattr(r, locol)); hi = int(getattr(r, hicol)); sp = int(getattr(r, span))
        gs = gapserie.get(k)
        if gs is None:
            continue
        n = len(gs)
        if lo < 0 or hi >= n or sp < 1:
            continue
        obs.append(int(np.sum(gs[lo:hi] >= thr)))
        starts = np.arange(0, n - sp)
        if len(starts) == 0:
            continue
        pick = rng.choice(starts, size=nperm, replace=True)
        draws.append(np.array([np.sum(gs[s:s + sp] >= thr) for s in pick]))
    if not obs or not draws:
        return None
    obs = np.array(obs); D = np.vstack(draws)
    obs_mean = obs.mean(); null_dist = D.mean(axis=0)
    p = (1 + np.sum(null_dist <= obs_mean)) / (nperm + 1)  # una cola: menos cruces
    return dict(n=len(obs), obs_mean=obs_mean, null_mean=null_dist.mean(),
                dif=obs_mean - null_dist.mean(), p=p,
                frac_cero=float(np.mean(obs == 0)))


gaps = {k: d.sort_values('grupo').gap.values for k, d in g.groupby('kfg')}
rc = cruces(cs, 'name', 'lo', 'hi', 'span', gaps, thr=2.0, nperm=3000)
print('C1 cluster-cluster (gap>=2cm):', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rc.items()})
rc5 = cruces(cs, 'name', 'lo', 'hi', 'span', gaps, thr=5.0, nperm=3000)
print('C1 cluster-cluster (gap>=5cm):', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rc5.items()})

# C2. pendant-pendant sums: parsear sum_string [g,c]:valor
pp = pd.read_csv(os.path.join(REL, 'pendant_pendant_sum_relation.csv'))
pp = pp[pp.name.isin(g.kfg.unique())].copy()
PATSUM = re.compile(r'\[(\d+),\s*(\d+)\]:')


def grupos_suma(s):
    return sorted(set(int(m.group(1)) for m in PATSUM.finditer(str(s))))


pp['grupos_suma'] = pp.sum_string.map(grupos_suma)
pp['lo'] = pp.grupos_suma.map(lambda x: min(x) if x else np.nan)
pp['hi'] = pp.grupos_suma.map(lambda x: max(x) if x else np.nan)
pp['span'] = pp.hi - pp.lo
pp2 = pp[(pp.span > 0)].dropna(subset=['lo', 'hi'])
pp2 = pp2[pp2.name.isin(contig_k)]
print('\npendant-pendant sums con span>0:', len(pp2), 'quipus', pp2.name.nunique(),
      '| mediana span:', pp2.span.median())
rp = cruces(pp2, 'name', 'lo', 'hi', 'span', gaps, thr=2.0, nperm=3000)
print('C2 pendant-pendant (gap>=2cm):', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rp.items()})
rp5 = cruces(pp2, 'name', 'lo', 'hi', 'span', gaps, thr=5.0, nperm=3000)
print('C2 pendant-pendant (gap>=5cm):', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rp5.items()})

# Distribución de spans y de gaps cruzados (descriptivo)
print('\nspan de relaciones pendant-pendant:', pp2.span.describe(percentiles=[.5, .9]).round(2).to_dict())
print('fracción de relaciones que cruzan al menos un gap>=2cm:',
      round(float(np.mean([np.any(gaps[k][int(l):int(h)] >= 2.0)
                           for k, l, h in zip(pp2.name, pp2.lo, pp2.hi) if k in gaps])), 3))

# Guardar p-values
pv = {}
for col, r in resA.items():
    if r: pv[f'A_rho_{col}'] = r['p_dos']
for col, r in resA2.items():
    if r: pv[f'A_bigsmall_{col}'] = r['p']
for col, r in resB.items():
    if r: pv[f'B_{col}'] = r['p']
for col, r in resB2.items():
    if r: pv[f'B_match_{col}'] = r['p']
if rc: pv['C_cluster_2cm'] = rc['p']
if rp: pv['C_pp_2cm'] = rp['p']
pd.Series(pv, name='p').to_csv(os.path.join(BASE, 'pvalues_espaciado.csv'))
print('\np-values:', {k: f'{v:.2g}' for k, v in pv.items()})
