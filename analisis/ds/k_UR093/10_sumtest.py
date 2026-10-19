# -*- coding: utf-8 -*-
"""UR093: test propio de 'suma por columna' (mismo indice entre grupos) y
'sumando pendantes cualesquiera', con nulo por permutacion (1000x, seed 0)."""
import pandas as pd, numpy as np
from itertools import combinations
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg=='UR093'].copy(); u['valor']=u.valor.fillna(0).astype(int)
n0=u[u.nivel==0].copy().sort_values('orden')
# indice dentro del grupo
n0['idx']=n0.groupby('grupo').cumcount()
vals=n0.valor.values.copy()
grp=n0.grupo.values; idx=n0.idx.values
G=12
# matriz de columnas: para cada idx, lista de valores por grupo
cols={}
for i in range(idx.max()+1):
    cols[i]=[(g,vals[k]) for k in range(len(vals)) if idx[k]==i]

def subset_sum_exists(target, items):
    # items: lista de valores (>0 considerados); busca subconjunto (>=1) que sume target
    if target<=0: return False
    it=[x for x in items if 0<x<=target]
    it.sort()
    # DP
    reach={0}
    for x in it:
        reach |= {s+x for s in list(reach) if s+x<=target}
    return target in reach and target>0 and any(x>0 for x in it)

def t_indexed(vals_):
    # reconstruir n0 con nuevos valores
    n0b=n0.copy(); n0b['valor']=vals_
    cnt=0; used=set()
    for i,rows in cols.items():
        gs=[g for g,_ in rows]
        for g,oldv in rows:
            tgt=vals_[ (grp==g)&(idx==i) ][0]
            others=[vals_[(grp==g2)&(idx==i)][0] for g2 in gs if g2!=g]
            if tgt>0 and subset_sum_exists(tgt, others):
                cnt+=1
    return cnt

def t_any(vals_):
    # un pendante = suma de subconjunto de OTROS pendantes (cualquier posicion)
    cnt=0
    pos=sorted(set(vals_[vals_>0]))
    for k in range(len(vals_)):
        tgt=vals_[k]
        if tgt<=0 or tgt>100: continue
        others=[vals_[j] for j in range(len(vals_)) if j!=k]
        # heuristica: solo considerar si hay >=2 valores; subset-sum
        if subset_sum_exists(tgt, others): cnt+=1
    return cnt

obs1=t_indexed(vals); obs2=t_any(vals)
rng=np.random.default_rng(0)
N=1000
n1=[];n2=[]
for _ in range(N):
    p=rng.permutation(vals)
    n1.append(t_indexed(p))
    n2.append(t_any(p))
n1=np.array(n1);n2=np.array(n2)
print(f'Indexed (mismo idx entre grupos): obs={obs1}  nulo medio={n1.mean():.1f}  p(obs>=nulo)={(np.sum(n1>=obs1)+1)/(N+1):.4f}')
print(f'Cualquier pendante = suma otros:  obs={obs2}  nulo medio={n2.mean():.1f}  p={(np.sum(n2>=obs2)+1)/(N+1):.4f}')
print('percentiles nulo indexed:',np.percentile(n1,[50,90,95,99]).round(1).tolist())
print('percentiles nulo any    :',np.percentile(n2,[50,90,95,99]).round(1).tolist())
