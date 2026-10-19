# -*- coding: utf-8 -*-
"""UR113: pruebas aritmeticas internas con nulo de permutacion (1000, semilla 0)."""
import pandas as pd, numpy as np, json, os
from collections import defaultdict

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
rng = np.random.default_rng(0)
u = pd.read_csv(os.path.join(OUT, 'cuerdas_ur113.csv'))
u['valor'] = u.valor.fillna(0)
p = u[u.nivel == 0].copy().reset_index(drop=True)
sub = u[u.nivel > 0].copy()

# ---------- A. madre = suma de hijas inmediatas ----------
hijas = sub.groupby('padre').agg(sumh=('valor', 'sum'), nh=('valor', 'size'))
madres = p.merge(hijas, left_on='cuerda', right_index=True, how='left').fillna({'sumh': 0, 'nh': 0})
madres = madres[madres.nh > 0]
def hits(df):
    return dict(exact=int((df.valor == df.sumh).sum()),
                tol1=int((abs(df.valor - df.sumh) <= 1).sum()),
                tol2=int((abs(df.valor - df.sumh) <= 2).sum()))
obsA = hits(madres)
# nulo: barajar valores de TODAS las hijas entre si (mantiene estructura)
subv = sub.valor.values.copy()
NUL = 1000
nullA = []
for _ in range(NUL):
    perm = rng.permutation(subv)
    s = pd.Series(perm, index=sub.index).groupby(sub.padre.values).sum()
    d = madres.copy()
    d['sumh_n'] = d.cuerda.map(s).fillna(0)
    nullA.append((int((d.valor == d.sumh_n).sum()), int((abs(d.valor - d.sumh_n) <= 1).sum()),
                  int((abs(d.valor - d.sumh_n) <= 2).sum())))
nullA = np.array(nullA)
pA = [(np.sum(nullA[:, i] >= obsA[k]) + 1) / (NUL + 1) for i, k in enumerate(['exact', 'tol1', 'tol2'])]
print('A. madre=suma hijas: n madres', len(madres), 'obs', obsA,
      'nulo medio', nullA.mean(0).round(1).tolist(), 'p', [round(x, 4) for x in pA])

# ---------- B/C. colgante = suma de una corrida de colgantes previos ----------
# corridas contiguas de 2..10 dentro del mismo grupo, terminando en el colgante.
def run_sums(vals, maxlen=10):
    """devuelve set de valores alcanzables como suma de corridas contiguas previas (2..maxlen)"""
    out = set()
    for k in range(2, maxlen + 1):
        for i in range(len(vals) - k, len(vals) - 1):
            pass
    return out

def scan_runs(df, groupcol='grupo', valcol='valor', colorcol=None, maxlen=10):
    """para cada fila i, ¿su valor = suma de una corrida contigua previa dentro del grupo?"""
    res = []
    for gi, gg in df.groupby(groupcol, sort=False):
        gg = gg.reset_index(drop=True)
        for i in range(len(gg)):
            if i < 2:
                continue
            target = gg.loc[i, valcol]
            if target == 0:
                continue
            found = None
            for k in range(2, min(maxlen, i) + 1):
                seg = gg.loc[i - k:i - 1]
                if colorcol is not None and seg[colorcol].nunique() > 1:
                    continue
                if abs(seg[valcol].sum() - target) < 0.5:
                    found = k
                    break
            res.append((gi, gg.loc[i, 'cuerda'], target, found))
    return pd.DataFrame(res, columns=['grupo', 'cuerda', 'valor', 'k'])

runs = scan_runs(p)
obsB = int(runs.k.notna().sum())
runsC = scan_runs(p, colorcol='color')
obsC = int(runsC.k.notna().sum())
print('B. colgante=corrida previa (2-10):', obsB, 'de', len(runs), 'cuerdas testables')
print('C. corrida monocroma previa:', obsC, 'de', len(runsC))

def null_runs(pend, colorcol, n=1000):
    vals = pend.valor.values
    cols = pend.color.values
    out = []
    for _ in range(n):
        perm = rng.permutation(vals)
        d = pend.copy(); d['valor'] = perm
        if colorcol:
            d['color'] = cols  # color fijo por posicion
        out.append(int(scan_runs(d, colorcol=colorcol).k.notna().sum()))
    return np.array(out)
np.random.seed(0)
nB = null_runs(p, None, 300)
nC = null_runs(p, 'color', 300)
pB = (np.sum(nB >= obsB) + 1) / (len(nB) + 1)
pC = (np.sum(nC >= obsC) + 1) / (len(nC) + 1)
print('   nulo B: media', round(nB.mean(), 1), 'max', nB.max(), 'p', round(pB, 4))
print('   nulo C: media', round(nC.mean(), 1), 'max', nC.max(), 'p', round(pC, 4))
runs.to_csv(os.path.join(OUT, 'corridas.csv'), index=False)

# ---------- D. sumas de grupo ----------
gtot = p.groupby('grupo').valor.sum()
print('\nD. totales de grupo:', gtot.astype(int).to_dict())
allvals = set(p.valor.astype(int)) | set(sub.valor.astype(int))
print('   totales de grupo que coinciden con algun valor de cuerda:',
      {g: int(v) for g, v in gtot.items() if int(v) in allvals})
print('   suma total colgantes', int(p.valor.sum()), 'suma total todas', int(u.valor.sum()))
print('   grupos que suman lo mismo que otro grupo:',
      {int(v): list(gtot[gtot == v].index) for v in gtot if (gtot == v).sum() > 1})
print('   suma de grupos consecutivos que iguala a otro:')
gl = gtot.tolist()
for i in range(len(gl)):
    for j in range(i + 2, len(gl) + 1):
        s = sum(gl[i:j])
        for k, v in gtot.items():
            if abs(s - v) < 0.5 and not (i <= list(gtot.index).index(k) < j):
                print('     ', list(gtot.index)[i], '-', list(gtot.index)[j - 1], '=', int(s), '= grupo', k)

# ---------- E. repeticion de valores ----------
vc = p.valor.value_counts()
print('\nE. valores de colgante repetidos (>=4):')
print(vc[vc >= 4].head(12).to_string())
# nulo: mismo multiconjunto -> la repeticion es trivial; comparar con quipus del corpus
c = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'), dtype={'kfg': str})
c['valor'] = pd.to_numeric(c.valor, errors='coerce').fillna(0)
c['nivel'] = pd.to_numeric(c.nivel, errors='coerce')
pend_all = c[c.nivel == 0]
per = pend_all.groupby('kfg').agg(n=('valor', 'size'), s=('valor', 'sum'),
                                  vc=('valor', lambda x: x.value_counts().iloc[0] if len(x) else 0))
per['ratio_rep'] = per.vc / per.n
per['mean'] = per.s / per.n
print('\n   UR113: n=332, valor modal repetido=', int(vc.iloc[0]), 'ratio=', round(vc.iloc[0] / 332, 3),
      'media=', round(p.valor.mean(), 1))
big = per[per.n >= 100].sort_values('ratio_rep', ascending=False)
print('   quipus >=100 colgantes por ratio de repeticion del valor modal:')
print(big.head(8).round(3).to_string())
print('   percentil de UR113 en ratio_rep (n>=100):',
      round((big.ratio_rep < per.loc['UR113', 'ratio_rep']).mean(), 3))
