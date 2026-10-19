# -*- coding: utf-8 -*-
"""UR003: tendencia izquierda->derecha (attachment R/V, color, valor, nudos) y
estructura de cuerdas sin nudos. Salida -> tendencia_out.txt"""
import pandas as pd, numpy as np
from scipy import stats
rng = np.random.default_rng(0)
d = pd.read_csv('analisis/datos/cuerdas.csv', dtype={'nudos': str})
u = d[d.kfg == 'UR003'].copy().sort_values('orden').reset_index(drop=True)
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); out.append(s); print(s)
u['cbase'] = u.color.fillna('NA').str.split(r'[:\-/]').str[0]
colg = u[u.nivel==0].copy().sort_values('orden').reset_index(drop=True)

# indices 0..n-1
colg['pos']=np.arange(len(colg))
colg['isR']=(colg.union=='R').astype(int)
colg['isW']=colg.cbase.eq('W').astype(int)
colg['hasKnot']=colg.nudos.notna().astype(int)

P('=== correlaciones (Spearman) con la posicion izquierda->derecha ===')
for var in ['isR','isW','valor','hasKnot']:
    rho,p=stats.spearmanr(colg.pos, colg[var])
    P('  pos vs %-8s rho=%.3f p=%.4f'%(var,rho,p))

# --- changepoint simple: para cada k, |R-frac izquierda - R-frac derecha|
def best_split(seq):
    n=len(seq); best=(0,0)
    for k in range(3,n-3):
        d_=abs(np.mean(seq[:k])-np.mean(seq[k:]))
        if d_>best[0]: best=(d_,k)
    return best
for var in ['isR','isW']:
    seq=colg[var].values
    d_,k=best_split(seq)
    P('mejor split %s: k=%d dif=%.3f (izq=%.2f der=%.2f)'%(var,k,d_,seq[:k].mean(),seq[k:].mean()))

# nulo para el split de isR
seq=colg['isR'].values; obs_d,k=best_split(seq)
N=1000; nl=np.zeros(N)
for it in range(N):
    s=rng.permutation(seq); nl[it]=best_split(s)[0]
P('split isR obs=%.3f  nulo media=%.3f sd=%.3f  p(sup)=%.4f'%(obs_d,nl.mean(),nl.std(),(1+(nl>=obs_d).sum())/(N+1)))

# --- no-nudos: color y attachment ---
P('\n=== colgantes SIN nudos (valor=0) ===')
nk = colg[colg.hasKnot==0]
P('n sin nudos = %d / %d'%(len(nk),len(colg)))
P('sin nudos por color base:\n', nk.cbase.value_counts().head(8).to_string())
P('sin nudos por union:\n', nk.union.value_counts().to_string())
P('sin nudos NO blancos = %d (llevan color pero sin nudos)'%((nk.cbase!='W').sum()))

P('\n=== colgantes CON nudos ===')
k_=colg[colg.hasKnot==1]
P('n con nudos = %d ; por color base:\n'%len(k_), k_.cbase.value_counts().head(8).to_string())
P('con nudos por union:\n', k_.union.value_counts().to_string())

# --- attachment R/V y presencia de subsidiarias ---
P('\n=== R/V vs tiene subsidiarias ===')
nch=u[u.padre.notna()].groupby('padre').size().to_dict()
colg['nhijas']=colg.cuerda.map(nch).fillna(0).astype(int)
P(pd.crosstab(colg.union, colg.nhijas>0).to_string())

# --- nivel de profundidad: cuerdas de nivel>=2 ---
P('\n=== profundidad: cuerdas nivel>=2 ===')
deep=u[u.nivel>=2]
P('n =',len(deep),' por nivel:\n',deep.nivel.value_counts().sort_index().to_string())
P(deep[['cuerda','nivel','padre','grupo','valor','color','union']].head(25).to_string())

with open('analisis/ds/k_UR003/tendencia_out.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('\n[ok] tendencia_out.txt')
