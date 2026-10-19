"""UR1032 — test posicional dentro del grupo (borde vs centro) + presencia de nudo."""
import pandas as pd, numpy as np
rng=np.random.default_rng(0)
C=pd.read_csv('analisis/datos/cuerdas.csv')
s=C[C.kfg=='UR1032'].copy().sort_values('orden').reset_index(drop=True)
col=s[s.nivel==0].copy()
col['size']=col.groupby('grupo')['grupo'].transform('size')
col['pos']=col.groupby('grupo').cumcount()

# Test: en grupos de 5, valor medio en posiciones 1-3 vs 0,4
g5=col[col['size']==5]
v=g5.sort_values(['grupo','pos']).valor.values.reshape(-1,5)
obs = v[:,1:4].sum() - v[:,[0,4]].sum()
N=5000; cnt=0
for _ in range(N):
    # permutar dentro de cada fila
    vp=np.array([rng.permutation(r) for r in v])
    d=vp[:,1:4].sum()-vp[:,[0,4]].sum()
    if d>=obs: cnt+=1
print(f'g5 centro(1-3) > bordes(0,4): obs={obs}  p_emp(1col)={cnt/N:.4f}')

g3=col[col['size']==3]
w=g3.sort_values(['grupo','pos']).valor.values.reshape(-1,3)
obs3 = w[:,1].sum() - (w[:,0].sum()+w[:,2].sum())
cnt=0
for _ in range(N):
    wp=np.array([rng.permutation(r) for r in w])
    d=wp[:,1].sum()-(wp[:,0].sum()+wp[:,2].sum())
    if d>=obs3: cnt+=1
print(f'g3 centro(1) > bordes(0,2): obs={obs3}  p_emp(1col)={cnt/N:.4f}')

# presencia de nudo (binaria) por posicion en grupos de 5
print('\nfrac con nudo por posicion (g5):', (v>0).mean(0).round(3))
print('frac con nudo por posicion (g3):', (w>0).mean(0).round(3))
