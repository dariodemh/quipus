"""UR231: patrones no aritmeticos (color, repeticiones, perfiles, totales)."""
import pandas as pd, numpy as np, json
from scipy import stats
from itertools import combinations

ROOT = './'
OUT = ROOT + 'analisis/ds/k_UR231/'
RNG = np.random.default_rng(0)
NPERM = 1000

g = pd.read_csv(OUT + 'grupos_resumen.csv')
u = pd.read_csv(OUT + 'cuerdas_enriquecidas.csv')
pend = u[u.nivel == 0].sort_values(['grupo', 'idx']).reset_index(drop=True)
M = np.load(OUT + 'matriz_valores.npy')  # 80 x 12, NaN donde no hay cuerda

col = g.color.to_numpy()
res = {}

# ---------- 1. periodicidad de color: coincidencias a cada lag ----------
def lag_matches(seq, lag):
    return int(sum(seq[i] == seq[i + lag] for i in range(len(seq) - lag)))

lags = {L: lag_matches(col, L) for L in range(1, 80)}
obs14 = lags[14]
# nulo: permutar el orden de los colores de los grupos
null14 = np.array([lag_matches(RNG.permutation(col), 14) for _ in range(NPERM)])
res['color_lag14'] = dict(obs=obs14, n=66, null_mean=round(float(null14.mean()), 2),
                          null_sd=round(float(null14.std()), 2),
                          p=float((1 + (null14 >= obs14).sum()) / (1 + NPERM)),
                          ranking=int(sorted(lags.values(), reverse=True).index(obs14) + 1))
print('matches color lag14 =', obs14, '/66; nulo', round(null14.mean(), 2), 'p=', res['color_lag14']['p'])
print('top lags:', sorted(lags.items(), key=lambda x: -x[1])[:8])

# ---------- 2. grupos separadores (fibra vegetal) en progresion aritmetica ----------
veg = g[g.fiber == 'V'].grupo.tolist()
print('grupos fibra vegetal:', veg, 'difs', np.diff(veg))
# p exacta de que 4 posiciones al azar entre 80 formen una PA de razon 14
valid = 80 - 3 * 14
p_ap = valid / len(list(combinations(range(80), 4)))
res['separadores_AP'] = dict(obs=veg, diffs=np.diff(veg).tolist(), p_ap=float(p_ap))
print('p exacta PA(4, d=14) =', p_ap)

# ---------- 3. totales de grupo = suma de tramos contiguos de grupos ----------
tot = g.suma.to_numpy()
def group_runs(v, minlen=2):
    hits = []
    n = len(v)
    for i in range(n):
        s = 0.0
        for j in range(i, n):
            s += v[j]
            if j - i + 1 < minlen: continue
            for k in range(n):
                if (k < i or k > j) and v[k] == s and v[k] > 0:
                    hits.append((k, i, j, float(s)))
    return hits
obs_runs = group_runs(tot)
print('total de grupo = suma de tramo contiguo de otros grupos:', len(obs_runs))
for h in obs_runs[:10]: print('   g%d = suma g%d..g%d (%.0f)' % h)
null_runs = []
for _ in range(200):
    null_runs.append(len(group_runs(RNG.permutation(tot))))
null_runs = np.array(null_runs)
res['totales_tramos'] = dict(obs=len(obs_runs), null_mean=round(float(null_runs.mean()), 2),
                             null_sd=round(float(null_runs.std()), 2),
                             p=float((1 + (null_runs >= len(obs_runs)).sum()) / 201))
print('  nulo(200):', res['totales_tramos'])

# ---------- 4. valores repetidos entre grupos ----------
vals = pend.v.fillna(0).to_numpy(float)
grp = pend.grupo.to_numpy()
from collections import defaultdict
byval = defaultdict(set)
for x, gg in zip(vals, grp):
    if x > 0: byval[x].add(gg)
rep = {x: s for x, s in byval.items() if len(s) > 1}
print('valores que aparecen en >1 grupo:', len(rep), 'de', len(byval))
print('  top:', sorted(rep.items(), key=lambda kv: -len(kv[1]))[:8])
def n_rep(v):
    d = defaultdict(set)
    for x, gg in zip(v, grp):
        if x > 0: d[x].add(gg)
    return sum(1 for s in d.values() if len(s) > 1)
null_rep = np.array([n_rep(RNG.permutation(vals)) for _ in range(NPERM)])
res['valores_repetidos'] = dict(obs=n_rep(vals), null_mean=round(float(null_rep.mean()), 2),
                                p=float((1 + (null_rep >= n_rep(vals)).sum()) / (1 + NPERM)))
print('  nulo:', res['valores_repetidos'])

# ---------- 5. perfiles de los seis grupos de 12 ----------
idx12 = g[g.n == 12].grupo.tolist()
idx12 = [i for i in idx12 if g.loc[g.grupo == i, 'nval'].iloc[0] >= 10]
P = np.array([M[i, :11] for i in idx12], float)
print('grupos de 12 con datos:', idx12, 'matriz', P.shape)
C = np.corrcoef(P)
print('correlaciones entre perfiles (11 columnas):')
print(np.round(C, 2))
off = C[np.triu_indices(len(idx12), 1)]
obs_r = float(off.mean())
null_r = []
for _ in range(NPERM):
    Q = np.array([RNG.permutation(r) for r in P])
    Cq = np.corrcoef(Q)
    null_r.append(Cq[np.triu_indices(len(idx12), 1)].mean())
null_r = np.array(null_r)
res['perfiles_r'] = dict(obs=round(obs_r, 3), null_mean=round(float(null_r.mean()), 3),
                         null_sd=round(float(null_r.std()), 3),
                         p=float((1 + (null_r >= obs_r).sum()) / (1 + NPERM)))
print('r media', round(obs_r, 3), 'nulo', round(null_r.mean(), 3), 'p=', res['perfiles_r']['p'])

# ---------- 6. ultima posicion de los grupos de 12 ----------
last = P[:, -1] if False else np.array([M[i, 11] for i in idx12], float)
first11 = np.array([M[i, :11] for i in idx12], float)
rank_last = [int((row < last[k]).sum()) for k, row in enumerate(first11)]
print('valor de la posicion 12 en cada grupo de 12:', last, 'puestos (0=el menor):', rank_last)
res['ultima_posicion'] = dict(valores=last.tolist(), puestos=rank_last)

# ---------- 7. homogeneidad de color dentro de grupos ----------
hom = u[u.nivel == 0].groupby('grupo').color.nunique()
print('colores distintos por grupo: media %.2f, max %d, grupos monocromos %d/80'
      % (hom.mean(), hom.max(), (hom == 1).sum()))
res['color_intragrupo'] = dict(media=round(float(hom.mean()), 2), max=int(hom.max()),
                               mono=int((hom == 1).sum()))

json.dump(res, open(OUT + 'patrones.json', 'w'), indent=1, ensure_ascii=False, default=str)
