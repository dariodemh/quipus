# -*- coding: utf-8 -*-
"""
04_pares.py -- ¿los quipus relacionados comparten "mano"?
  A) Incahuasi: los 7 quipus del sistema aritmetico (UR273A/B, UR266, UR275, UR270, UR278, UR269)
     frente a todos los pares del mismo sitio (nulo = subconjuntos aleatorios de igual tamano).
  B) Copias (14_copias): acuerdo de rasgos de manufactura en los pares copia vs pares control.
  C) Cuantos pares del corpus comparten firma exacta en los 4 ejes (poder discriminante).
"""
import os, json, itertools
import numpy as np, pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
RNG = np.random.default_rng(20261018)
f = pd.read_csv(os.path.join(AQUI, 'firma_quipu.csv'))
CAT = ['eje_tors', 'eje_ndS', 'eje_union', 'eje_term']
res = {}

def acuerdo(a, b, cols):
    v = [a[c] == b[c] for c in cols if pd.notna(a[c]) and pd.notna(b[c])]
    return (sum(v)/len(v)) if v else np.nan, len(v)

def dist_firma(df, cols=CAT):
    n = len(df); D = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(i+1, n):
            a, b = df.iloc[i], df.iloc[j]
            d = [a[c] != b[c] for c in cols if pd.notna(a[c]) and pd.notna(b[c])]
            if d: D[i, j] = D[j, i] = np.mean(d)
    return D

# ---------- A) Incahuasi ----------
inc = f[f.museo == 'Proyecto Incahuasi'].copy().reset_index(drop=True)
TG = ['UR266','UR269','UR270','UR273A','UR273B','UR275','UR278']
print('Incahuasi: %d quipus; cobertura por eje:' % len(inc))
print(inc[CAT].notna().sum().to_dict())
print('\nreparto de ejes en el sitio:')
for c in CAT:
    print(' ', c, inc[c].value_counts(dropna=False).to_dict())

idx = inc.index[inc.kfg.isin(TG)].tolist()
D = dist_firma(inc)
# distancia media por pares del conjunto objetivo
def mean_pair(D, ii):
    vals = [D[i, j] for i, j in itertools.combinations(ii, 2) if not np.isnan(D[i, j])]
    return np.mean(vals), len(vals)
obs, nobs = mean_pair(D, idx)
nperm = 20000
null = np.empty(nperm)
for p in range(nperm):
    ii = RNG.choice(len(inc), len(idx), replace=False)
    null[p] = mean_pair(D, ii)[0]
p_inc = (1 + (null <= obs).sum())/(1+nperm)   # menor distancia = mas parecido
print('\nA) Incahuasi, 7 quipus del sistema: distancia media de firma = %.3f (%d pares)' % (obs, nobs))
print('   nulo (7 al azar del sitio): %.3f  p(<=) = %.4f' % (null.mean(), p_inc))
print('   pares con firma IDENTICA en los 4 ejes:',
      int(sum(1 for i, j in itertools.combinations(idx, 2) if D[i, j] == 0)), 'de', nobs)
res['incahuasi'] = dict(n_sitio=len(inc), obs=float(obs), null=float(null.mean()),
                        p=float(p_inc), n_pares=int(nobs))

# torsion dentro del sitio: ¿los 7 son todos S por azar?
from scipy.stats import hypergeom
nS = int((inc.eje_tors == 'S').sum()); nZ = int((inc.eje_tors == 'Z').sum())
k7 = int((inc.loc[idx, 'eje_tors'] == 'S').sum())
print(); print('   torsion en Incahuasi: %d S / %d Z; los 7 del sistema: %d S' % (nS, nZ, k7))
print('   P(los 7 S | 26/48) hipergeometrica = %.5f' % hypergeom.sf(k7-1, nS+nZ, nS, len(idx)))
# tamano: ¿los 7 son los mas grandes?
print('   n_pend de los 7:', inc.loc[idx, 'n_pend'].tolist())
print('   n_pend del resto: mediana %.1f, rango %d-%d' % (
    inc.drop(idx).n_pend.median(), inc.drop(idx).n_pend.min(), inc.drop(idx).n_pend.max()))
print('   torsion x tamano en el sitio (mediana n_pend):')
print(inc.groupby('eje_tors').n_pend.agg(['size','median']).to_string())
res['inc_tors'] = dict(nS=nS, nZ=nZ, k7=k7,
    p_hiper=float(hypergeom.sf(k7-1, nS+nZ, nS, len(idx))))
# control por tamano: probabilidad de S por estrato de n_pend
inc['tam_q'] = pd.qcut(inc.n_pend, 4, duplicates='drop')
print('   S/Z por cuartil de tamano:')
print(pd.crosstab(inc.tam_q, inc.eje_tors, normalize='index').round(2).to_string())
pr = inc.groupby('tam_q', observed=True).eje_tors.apply(lambda s: (s=='S').mean())
p7 = float(np.prod([pr.loc[inc.tam_q[i]] for i in idx]))
print('   P(los 7 S) usando la tasa S de SU estrato de tamano = %.4f' % p7)
res['inc_tors']['p_estrato'] = p7
# correlacion corpus-wide torsion ~ tamano
print(); print('   corpus: torsion ~ tamano (mediana n_pend)')
print(f.groupby('eje_tors').n_pend.agg(['size','median']).to_string())
# detalle de los 7
print('\ndetalle de los 7:')
print(inc[inc.kfg.isin(TG)][['kfg'] + CAT + ['pS_tors','pS_nd_simple','pR','pK','pB_term','pW','pAB']]
      .to_string(index=False))
# pares concretos
print('\npares del sistema (distancia 0-1):')
for i, j in itertools.combinations(idx, 2):
    if D[i, j] > 0:
        print('  %-7s %-7s d=%.2f  %s | %s' % (inc.kfg[i], inc.kfg[j], D[i, j],
              [inc[c][i] for c in CAT], [inc[c][j] for c in CAT]))

# ---------- B) copias ----------
pares = pd.read_csv(os.path.join(RAIZ, 'analisis', '14_copias', 'pares_resumen.csv'))
cop = pares[pares.tipo == 'copia'][['A','B','familia','mismo_registrador']].copy()
fx = f.set_index('kfg')
rows = []
for _, r in cop.iterrows():
    if r.A in fx.index and r.B in fx.index:
        a, b = fx.loc[r.A], fx.loc[r.B]
        ac, n = acuerdo(a, b, CAT)
        rows.append(dict(A=r.A, B=r.B, familia=r.familia, mismo_reg=r.mismo_registrador,
                         acuerdo=ac, n=n, tors=(a.eje_tors == b.eje_tors),
                         ndS=(a.eje_ndS == b.eje_ndS), union=(a.eje_union == b.eje_union),
                         term=(a.eje_term == b.eje_term), dcolor=abs(a.H_color_norm-b.H_color_norm)))
cp = pd.DataFrame(rows)
print('\nB) copias evaluables:', len(cp))
print(cp[['A','B','acuerdo','tors','ndS','union','term','dcolor']].to_string(index=False))
kk = int(cp.tors.notna().sum())
print('media acuerdo = %.3f; torsion igual %d/%d; ndS %d/%d; union %d/%d; term %d/%d' % (
    cp.acuerdo.mean(), cp.tors.sum(), kk, cp.ndS.sum(), kk, cp.union.sum(), kk, cp.term.sum(), kk))

# nulo: pares aleatorios con los mismos dos prefijos y sitio compatible -> usar todo el corpus
def null_pairs(col, n, nperm=20000):
    obs = int(cp[col].sum())
    kk = int(cp[col].notna().sum())
    colmap = {'tors':'eje_tors','ndS':'eje_ndS','union':'eje_union','term':'eje_term'}
    vals = f[colmap[col]].dropna().values
    # probabilidad marginal de coincidencia
    pv = pd.Series(vals).value_counts(normalize=True)
    p0 = (pv**2).sum()
    null = RNG.binomial(kk, p0, nperm)
    return obs, kk, p0, (1+(null >= obs).sum())/(1+nperm)
for col in ['tors','ndS','union','term']:
    o, k, p0, p = null_pairs(col, len(cp))
    print('  %-6s obs %d/%d  esperado %.1f (p0=%.3f)  p=%.4f' % (col, o, k, k*p0, p0, p))
res['copias'] = cp.to_dict(orient='records')

# ---------- C) poder discriminante ----------
cc = f.dropna(subset=CAT)
n = len(cc)
combos = cc.groupby(CAT, dropna=False).size().sort_values(ascending=False)
print('\nC) %d quipus con los 4 ejes; %d combinaciones distintas (max 16).' % (n, len(combos)))
print(combos.head(8).to_string())
pares_id = int((combos*(combos-1)//2).sum()); tot = n*(n-1)//2
print('pares con firma identica: %d de %d (%.1f%%)' % (pares_id, tot, 100*pares_id/tot))
res['combos'] = dict(n=int(n), n_combos=int(len(combos)), pares_id=pares_id, pares_tot=tot)
json.dump(res, open(os.path.join(AQUI, 'res_04.json'), 'w'), indent=1, default=str)
