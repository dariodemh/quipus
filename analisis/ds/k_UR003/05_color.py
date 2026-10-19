# -*- coding: utf-8 -*-
"""UR003: estructura de COLOR y su relacion con attachment R/V. Nulos por permutacion.
Salida -> color_out.txt"""
import pandas as pd, numpy as np
rng = np.random.default_rng(0)
d = pd.read_csv('analisis/datos/cuerdas.csv', dtype={'nudos': str})
u = d[d.kfg == 'UR003'].copy().sort_values('orden').reset_index(drop=True)
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); out.append(s); print(s)

u['cbase'] = u.color.fillna('NA').str.split(r'[:\-/]').str[0]
u.loc[u.cbase.str.match(r'^[A-Z]{1,3}\('), 'cbase'] = 'MIX'
colg = u[u.nivel==0].copy().sort_values('orden')
grupos=sorted(colg.grupo.unique())

# --- runs de color dentro de cada cluster (colgantes) ---
def runs(seq):
    return 1+sum(1 for i in range(1,len(seq)) if seq[i]!=seq[i-1])
P('=== runs de color base por cluster (colgantes) ===')
total_runs=0; total_n=0
obs_seq={}
for g in grupos:
    s=colg[colg.grupo==g].cbase.tolist()
    obs_seq[g]=s
    if len(s)>=1:
        r=runs(s); total_runs+=r; total_n+=len(s)
        P('g%-2d n=%2d runs=%2d  %s'%(g,len(s),r,''.join(x[0] for x in s)))
P('TOTAL runs=%d sobre %d colgantes'%(total_runs,total_n))

# nulo: permutar colores dentro de cada cluster, contar runs totales
N=1000; null=np.zeros(N)
for it in range(N):
    tr=0
    for g in grupos:
        s=obs_seq[g]
        if len(s)>=1: tr+=runs(list(rng.permutation(s)))
    null[it]=tr
p_less=(1+(null<=total_runs).sum())/(N+1)
P('NULO runs: media=%.1f sd=%.1f  p(obs<=nulo)=%.4f'%(null.mean(),null.std(),p_less))

# --- attachment vs color (W vs no-W) en colgantes R/V ---
rv=colg[colg.union.isin(['R','V'])].copy()
rv['isW']=rv.cbase.eq('W')
ct=pd.crosstab(rv.union,rv.isW)
P('\n=== tabla union(R/V) x color(W/noW) colgantes ===')
P(ct.to_string())
# permutacion: V asociado a W?
obs_wV = ((rv.union=='V')&(rv.isW)).sum()
N2=1000; nl=np.zeros(N2); lab=rv.isW.values
for it in range(N2):
    pp=rng.permutation(lab)
    nl[it]=((rv.union.values=='V')&pp).sum()
P('obs (V y W)=%d  nulo media=%.1f sd=%.1f  p(sup)=%.4f'%(obs_wV,nl.mean(),nl.std(),(1+(nl>=obs_wV).sum())/(N2+1)))

# --- segmentos: primeros 8 clusters vs ultimos 6 ---
P('\n=== por cluster: fraccion W y fraccion R (colgantes >=3) ===')
for g in grupos:
    s=colg[colg.grupo==g]
    if len(s)<3: continue
    P('g%-2d fracW=%.2f fracR=%.2f'%(g,(s.cbase=='W').mean(),(s.union=='R').mean()))

# --- color de hijos vs color de la madre (nivel0 vs nivel1) ---
P('\n=== color base: nivel0 vs nivel1 ===')
P('nivel0:\n', colg.cbase.value_counts().head(10).to_string())
P('nivel1:\n', u[u.nivel==1].cbase.value_counts().head(10).to_string())

# --- banding: fraccion de clusters con un solo color dominante ---
P('\n=== banding: cluster con >=50%% de un color ===')
band=0
for g in grupos:
    s=colg[colg.grupo==g].cbase
    if len(s)>=2 and s.value_counts().iloc[0]/len(s)>=0.5: band+=1
P('clusters "banded" (>=50%% dominante) = %d / %d'%(band,len(grupos)))

with open('analisis/ds/k_UR003/color_out.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('\n[ok] color_out.txt')
