# -*- coding: utf-8 -*-
"""UR001. Periodicidad: autocorrelacion de 'tiene nudo' y color por lag; regularidad de PK."""
import pandas as pd, numpy as np, json
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
pend=r[r.nivel==0].sort_values('orden').reset_index(drop=True)
rng=np.random.default_rng(0); NPERM=1000

rich=(pend.nudos.notna().values).astype(float)
col=pend.color.values

def score_lag(seq_func, P):
    # fraccion de pares (i,i+P) coherentes
    a=seq_func[:-P]; b=seq_func[P:]
    return np.mean(a==b)

# color-match at lag P
print('=== coherencia de COLOR por lag (obs vs nulo) ===')
best=[]
for P in range(1,41):
    obs=score_lag(col,P)
    nulls=np.array([score_lag(rng.permutation(col),P) for _ in range(200)])
    p=(np.sum(nulls>=obs)+1)/201
    best.append((P,round(obs,3),round(nulls.mean(),3),round(p,3)))
for row in best:
    if row[3]<=0.05 or row[0]<=20: print('  lag %2d obs=%.3f nulo=%.3f p=%.3f'%row)

print('\n=== coherencia de RIQUEZA (tiene nudo) por lag ===')
bestr=[]
for P in range(1,41):
    obs=score_lag(rich,P)
    nulls=np.array([score_lag(rng.permutation(rich),P) for _ in range(200)])
    p=(np.sum(nulls>=obs)+1)/201
    bestr.append((P,round(obs,3),round(nulls.mean(),3),round(p,3)))
for row in sorted(bestr,key=lambda x:x[3])[:8]:
    print('  lag %2d obs=%.3f nulo=%.3f p=%.3f'%row)

# ==== regularidad de PK ====
print('\n=== regularidad de posiciones PK ===')
pkpos=np.array(sorted(pend[pend.color=='PK'].orden.values))
gaps=np.diff(pkpos)
print('gaps PK:',list(gaps))
print('CV obs:',round(gaps.std()/gaps.mean(),3))
nullcv=[]
n=len(pend)
for _ in range(NPERM):
    pp=np.sort(rng.choice(n,size=len(pkpos),replace=False))
    g=np.diff(pp); nullcv.append(g.std()/g.mean())
nullcv=np.array(nullcv)
p_pk=(np.sum(nullcv<=gaps.std()/gaps.mean())+1)/(NPERM+1)
print(f'  CV nulo media={nullcv.mean():.3f}; p(<=obs)={p_pk:.3f}')

# ==== coherencia de color dentro de segmentos PK ====
print('\n=== color homogeneo dentro de bloques PK? ===')
segs=np.split(np.arange(n), np.where(np.isin(pend.orden.values,pkpos))[0])[1:]
def coh(assign,segs):
    same=0;tot=0
    for s in segs:
        if len(s)<2: continue
        c=assign[s]; same+=np.sum(c[1:]==c[:-1]); tot+=len(s)-1
    return same/tot
obs=coh(col,segs)
nulls=np.array([coh(rng.permutation(col),segs) for _ in range(NPERM)])
p_seg=(np.sum(nulls>=obs)+1)/(NPERM+1)
print(f'  obs={obs:.3f} nulo={nulls.mean():.3f} p={p_seg:.3f}')
json.dump(dict(PK_CV=float(gaps.std()/gaps.mean()),PK_p=float(p_pk),
               color_seg_obs=float(obs),color_seg_p=float(p_seg)),
          open('analisis/ds/k_UR001/resultados_periodicidad.json','w'),indent=1)
print('\n[ok]')
