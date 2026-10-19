# -*- coding: utf-8 -*-
"""
08_resumen.py -- pruebas de cabecera con p exactos, BH y controles finales.
"""
import os, json, itertools
import numpy as np, pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(20261018)
f = pd.read_csv(os.path.join(AQUI, 'firma_quipu.csv'))
CAT = ['eje_tors','eje_ndS','eje_union','eje_term']
out = {}

def bh(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p)
    q = np.empty(m); q[o] = np.minimum.accumulate((p[o]*m/np.arange(1,m+1))[::-1])[::-1]
    return np.clip(q,0,1)

# T2 independencia de ejes
d = f.dropna(subset=CAT)
ps = []
for a,b in itertools.combinations(CAT,2):
    ct = pd.crosstab(d[a],d[b])
    ps.append(stats.chi2_contingency(ct)[1])
q = bh(ps)
print('T2 independencia de los 4 ejes (chi2, 6 pruebas):')
for (a,b),p,qq in zip(itertools.combinations(CAT,2), ps, q):
    print('  %-10s x %-10s p=%.3f q=%.3f' % (a,b,p,qq))
out['T2'] = dict(p=list(map(float,ps)), q=list(map(float,q)))

# T3 firma identica vs nulo de ejes independientes
p_id = np.prod([(d[c].value_counts(normalize=True).values**2).sum() for c in CAT])
obs = (d.groupby(CAT).size().pow(2).sum()-len(d))/(len(d)*(len(d)-1))
null = np.empty(5000)
for i in range(5000):
    dd = {c: RNG.permutation(d[c].values) for c in CAT}
    g = pd.DataFrame(dd).groupby(CAT).size()
    null[i] = (g.pow(2).sum()-len(d))/(len(d)*(len(d)-1))
p = (1+(null>=obs).sum())/5001
print('\nT3 P(par con firma identica): obs %.4f | nulo %.4f (sd %.4f) p=%.3f' % (obs,null.mean(),null.std(),p))
out['T3'] = dict(obs=float(obs), null=float(null.mean()), p=float(p), n=int(len(d)))

# T4 Incahuasi: torsion por sector
inc = f[f.museo=='Proyecto Incahuasi'].copy()
inc['sector'] = np.where(inc.kfg.str.startswith('JC'),'JC','UR')
ct = pd.crosstab(inc.sector, inc.eje_tors)
print('\nT4 Incahuasi torsion x sector:'); print(ct.to_string())
print('  Fisher p = %.3g' % stats.fisher_exact(ct.values)[1])
out['T4'] = dict(tabla=ct.values.tolist(), p=float(stats.fisher_exact(ct.values)[1]))

# T5 union en las parejas A/B del sistema
print('\nT5 union R/V en parejas A/B (misma "obra", dos partes):')
for A,B in [('UR273A','UR273B'),('UR267A','UR267B')]:
    a = f[f.kfg==A].iloc[0]; b = f[f.kfg==B].iloc[0]
    print('  %s pR=%.3f (n=%d) | %s pR=%.3f (n=%d)' % (A,a.pR,a.n_union,B,b.pR,b.n_union))
out['T5'] = {k: float(f[f.kfg==k].pR.iloc[0]) for k in ['UR273A','UR273B','UR267A','UR267B']}

# T6/T8 sistema: distancia con y sin union
inc = inc.reset_index(drop=True)
TG = ['UR266','UR269','UR270','UR273A','UR273B','UR275','UR278']
idx = inc.index[inc.kfg.isin(TG)].tolist()

def dist(df, cols):
    n=len(df); D=np.full((n,n),np.nan)
    for i in range(n):
        for j in range(i+1,n):
            a,b=df.iloc[i],df.iloc[j]
            v=[a[c]!=b[c] for c in cols if pd.notna(a[c]) and pd.notna(b[c])]
            if v: D[i,j]=D[j,i]=np.mean(v)
    return D

for cols, et in [(CAT,'4 ejes'), ([c for c in CAT if c!='eje_union'],'sin union'),
                 (['eje_tors'],'solo torsion')]:
    D = dist(inc, cols)
    def mp(ii):
        v=[D[i,j] for i,j in itertools.combinations(ii,2) if not np.isnan(D[i,j])]
        return np.mean(v) if v else np.nan
    o = mp(idx)
    nl = np.array([mp(list(RNG.choice(len(inc), len(idx), replace=False))) for _ in range(10000)])
    nl = nl[~np.isnan(nl)]
    print('T6 Incahuasi %-12s obs %.3f  nulo %.3f  p(<=)=%.4f' % (et,o,nl.mean(),(1+(nl<=o).sum())/(1+len(nl))))
    out['T6_'+et] = dict(obs=float(o), null=float(nl.mean()), p=float((1+(nl<=o).sum())/(1+len(nl))))

# T6b control: nulo restringido al sector UR (deposito), no a todo Incahuasi
ur = inc[inc.sector=='UR'].reset_index(drop=True)
idxu = ur.index[ur.kfg.isin(TG)].tolist()
print(); print('T6b mismo test con nulo SOLO dentro del sector UR (n=%d):' % len(ur))
for cols, et in [(CAT,'4 ejes'), ([c for c in CAT if c!='eje_union'],'sin union'),
                 (['eje_tors'],'solo torsion')]:
    D = dist(ur, cols)
    def mp(ii):
        v=[D[i,j] for i,j in itertools.combinations(ii,2) if not np.isnan(D[i,j])]
        return np.mean(v) if v else np.nan
    o = mp(idxu)
    nl = np.array([mp(list(RNG.choice(len(ur), len(idxu), replace=False))) for _ in range(10000)])
    nl = nl[~np.isnan(nl)]
    print('  %-12s obs %.3f nulo %.3f p(<=)=%.4f' % (et,o,nl.mean(),(1+(nl<=o).sum())/(1+len(nl))))
    out['T6b_'+et] = dict(obs=float(o), null=float(nl.mean()),
                          p=float((1+(nl<=o).sum())/(1+len(nl))))

# T7 copias: deficit de union
pares = pd.read_csv(os.path.join(os.path.abspath(os.path.join(AQUI,'..','..','..')),
                                 'analisis','14_copias','pares_resumen.csv'))
cop = pares[pares.tipo=='copia']; fx=f.set_index('kfg')
vistos=set(); rows=[]
for _,r in cop.iterrows():
    if r.A in vistos or r.B in vistos: continue
    vistos |= {r.A, r.B}; rows.append(r)
cop = pd.DataFrame(rows)
print('  parejas de copia no redundantes:', len(cop))
k=0; n=0
for _,r in cop.iterrows():
    if r.A in fx.index and r.B in fx.index:
        a,b=fx.loc[r.A],fx.loc[r.B]
        if pd.notna(a.eje_union) and pd.notna(b.eje_union):
            n+=1; k+=int(a.eje_union==b.eje_union)
print('\nT7 copias: union coincide %d/%d; P(X<=%d | Bin(%d,0.5)) = %.4f' % (
    k,n,k,n,stats.binom.cdf(k,n,0.5)))
out['T7'] = dict(k=k,n=n,p=float(stats.binom.cdf(k,n,.5)))
json.dump(out, open(os.path.join(AQUI,'res_08.json'),'w'), indent=1)
