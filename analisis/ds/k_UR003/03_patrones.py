# -*- coding: utf-8 -*-
"""UR003: patrones (color, valor, attachment R/V) y controles nulos. Salida -> patrones_out.txt"""
import pandas as pd, numpy as np
rng = np.random.default_rng(0)
d = pd.read_csv('analisis/datos/cuerdas.csv', dtype={'nudos': str})
u = d[d.kfg == 'UR003'].copy().sort_values('orden').reset_index(drop=True)
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); out.append(s); print(s)

u['cbase'] = u.color.fillna('NA').str.split(r'[:\-/]').str[0]
u.loc[u.cbase.str.match(r'^[A-Z]{1,3}\('), 'cbase'] = 'MIX'
colg = u[u.nivel==0].copy()
# numero de hijas directas
nch = u[u.padre.notna()].groupby('padre').size().to_dict()
colg['nhijas'] = colg.cuerda.map(nch).fillna(0).astype(int)

P('=== secuencia de COLGANTES por grupo (valor|colorBase|attachment) ===')
for gi in sorted(colg.grupo.unique()):
    cg = colg[colg.grupo==gi].sort_values('orden')
    toks = ['%d%s%s' % (r.valor, r.cbase[0], r.union) for _, r in cg.iterrows()]
    P('g%-2d (n=%d): %s' % (gi, len(cg), ' '.join(toks)))

P('\n=== attachment R/V de colgantes por grupo ===')
for gi in sorted(colg.grupo.unique()):
    cg = colg[colg.grupo==gi].sort_values('orden')
    seq = ''.join(str(x) for x in cg.union.fillna('?').tolist())
    P('g%-2d: %s' % (gi, seq))

# --- test estructura R/V: numero de cambios (switches) vs nulo ---
def switches(seq):
    return sum(1 for i in range(1,len(seq)) if seq[i]!=seq[i-1])
P('\n=== TEST R/V: switches observados vs nulo (barajar etiquetas dentro de cada grupo) ===')
rv = colg[colg.union.isin(['R','V'])].copy()
obs_sw=0; obs_n=0
for gi in sorted(rv.grupo.unique()):
    seq = rv[rv.grupo==gi].sort_values('orden').union.tolist()
    if len(seq)>=2:
        obs_sw += switches(seq); obs_n += len(seq)
P('switches totales obs = %d sobre %d cuerdas R/V' % (obs_sw, obs_n))
N=1000; null=np.zeros(N)
for it in range(N):
    s=0
    for gi in sorted(rv.grupo.unique()):
        seq = rv[rv.grupo==gi].sort_values('orden').union.tolist()
        if len(seq)>=2:
            perm = list(rng.permutation(seq)); s+=switches(perm)
    null[it]=s
P('nulo switches media=%.1f sd=%.1f min=%d max=%d' % (null.mean(), null.std(), null.min(), null.max()))
p_less = (1+(null<=obs_sw).sum())/(N+1)
p_greater = (1+(null>=obs_sw).sum())/(N+1)
P('p(obs<=nulo)=%.4f  p(obs>=nulo)=%.4f  (una cola)' % (p_less, p_greater))

# --- color vs valor: blancos vs no-blancos ---
P('\n=== color (W vs no-W) vs valor ===')
gh = colg[colg.union.isin(['R','V','U'])]
w = gh[gh.cbase=='W'].valor; nw = gh[gh.cbase!='W'].valor
P('W  n=%d media=%.3f  frac>0=%.3f' % (len(w), w.mean(), (w>0).mean()))
P('noW n=%d media=%.3f frac>0=%.3f' % (len(nw), nw.mean(), (nw>0).mean()))
# permutacion: diferencia de medias
def dm(colv, valv):
    return colv.groupby(colv).apply(lambda x:0)  # placeholder
obs_diff = nw.mean()-w.mean()
lab = gh.cbase.eq('W').values; vv = gh.valor.values
nd=np.zeros(N)
for it in range(N):
    pp=rng.permutation(lab)
    nd[it]=vv[~pp].mean()-vv[pp].mean()
P('obs diff(noW-W)=%.3f  nulo media=%.3f sd=%.3f  p(>=obs)=%.4f' % (obs_diff, nd.mean(), nd.std(), (1+(nd>=obs_diff).sum())/(N+1)))

# --- nivel/attachment de subsidiarias vs color de la madre ---
P('\n=== subsidiarias: color base por nivel ===')
P(u[u.nivel==1].cbase.value_counts().head(8).to_string())
P('colgantes color base count:\n', colg.cbase.value_counts().head(8).to_string())

# --- valor vs numero de hijas (correlacion) ---
P('\n=== valor vs n_hijas (colgantes) ===')
c = np.corrcoef(colg.nhijas, colg.valor)[0,1]
P('corr(nhijas,valor)=%.3f' % c)
P('media valor por nhijas:')
P(colg.groupby('nhijas').valor.agg(['mean','count']).head(10).to_string())

# --- values: are they bernoulli-ish? ---
P('\n=== distribucion valor colgantes vs Binomial/rr ===')
vc = colg.valor.value_counts().sort_index()
P(vc.to_string())

with open('analisis/ds/k_UR003/patrones_out.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('\n[ok] patrones_out.txt')
