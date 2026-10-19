"""UR1032 — periodicidad de valores, subsidiarias por tipo de grupo, autocorrelacion + nulo."""
import pandas as pd, numpy as np
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden').reset_index(drop=True)
col = s[s.nivel == 0].copy()
col['size'] = col.groupby('grupo')['grupo'].transform('size')
col['pos'] = col.groupby('grupo').cumcount()

print('== subsidiarias: en que tipo de grupo caen ==')
sub = s[s.nivel == 1].copy()
gtype = col.groupby('grupo')['size'].first().to_dict()
sub['gsize'] = sub.grupo.map(gtype)
print(sub.gsize.value_counts().to_dict())
# subsidiarias por colgante: cuantas colgantes tienen subs, por tipo
col['nsub'] = col.cuerda.map(sub.padre.value_counts()).fillna(0)
print('\ncolgantes con >=1 subsidiaria por tamano de grupo:')
print(col.groupby('size').nsub.agg(['mean','sum','count']))
print('fraccion de colgantes con sub por posicion (grupos de 5):')
print(col[col['size']==5].groupby('pos').nsub.agg(['mean',lambda x:(x>0).mean()]).rename(columns={'<lambda_0>':'frac'}))

# --- autocorrelacion de la serie de valores de colgantes (en orden) ---
v = col.sort_values('orden').valor.values.astype(float)
v = v - v.mean()
n = len(v)
ac = [np.sum(v[:n-l]*v[l:])/np.sum(v*v) for l in range(1, 25)]
print('\n== autocorrelacion lag 1..24 ==')
print(np.round(ac, 3))
# nulo: permutar valores dentro del quipu
rng = np.random.default_rng(0)
mx = np.zeros(24)
for _ in range(1000):
    vp = rng.permutation(v)
    for l in range(24):
        mx[l] += np.sum(vp[:n-l]*vp[l:])/np.sum(vp*vp)
mx/=1000
print('media nula:', np.round(mx,3))
obs_ac1 = ac[0]
# p-valor para lag 1 por permutacion
cnt=0
for _ in range(2000):
    vp=rng.permutation(v); a1=np.sum(vp[:n-1]*vp[1:])/np.sum(vp*vp)
    if abs(a1)>=abs(obs_ac1): cnt+=1
print(f'lag1 obs={obs_ac1:.3f} p_emp(2col)={cnt/2000:.3f}')
