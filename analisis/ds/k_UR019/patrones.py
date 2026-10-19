# -*- coding: utf-8 -*-
"""Patrones de posicion: indicador tiene-nudo, color. Nulos estructurales + correccion multiple."""
import numpy as np, pandas as pd, os
from itertools import combinations
rng = np.random.default_rng(0); NPERM = 1000
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
C = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
d = C[C['kfg'] == 'UR019'].sort_values('orden').reset_index(drop=True)
p = d[d['nivel'] == 0].reset_index(drop=True)
kn = p['nudos'].notna().to_numpy().astype(int)   # 1 = tiene nudo
val = p['valor'].to_numpy(float)
print('colgantes p1..p13, indicador tiene-nudo =', list(kn))
print('patron 1/0:', ''.join(map(str, kn)), '(bloques (1,1,0) desde p3 a p11)')

def autocorr_matches(s, lag):
    return int(np.sum(s[:-lag] == s[lag:]))
print('\n=== indicador tiene-nudo: autocorrelaciones ===')
for lag in (1,2,3,4,5):
    obs = autocorr_matches(kn, lag)
    null = np.array([autocorr_matches(rng.permutation(kn), lag) for _ in range(NPERM)])
    pv = (np.sum(null >= obs)+1)/(NPERM+1)
    print(f'  lag {lag}: matches obs={obs}/{len(kn)-lag}  media_nulo={null.mean():.2f}  max_nulo={null.max()}  p={pv:.3f}')

# valor solo en posiciones con nudo -> patron de valores
print('\n=== valores colgantes como serie ===')
print('valores =', [int(x) for x in val])
for lag in (2,3,4):
    a = val[:-lag]; b = val[lag:]
    print(f'  lag {lag}: correlacion Pearson =', round(np.corrcoef(a,b)[0,1],3) if a.std()>0 and b.std()>0 else 'NA')

# --- color: adyacencia con nulo GLOBAL vs nulo PRESERVANDO GRUPO
def fam(c):
    c=c.upper()
    if ':' in c or '-' in c or '/' in c: return 'mixed'
    import re; b=re.sub(r'[^A-Z]','',c)
    if b=='W': return 'white'
    if b in ('BL','B','LB','NB'): return 'blue'
    if b in ('AB','MB','KB','YB'): return 'brown'
    return 'other'
famv = np.array([fam(c) for c in p['color']])
grp = p['grupo'].to_numpy()
def adj(s): return int(np.sum(s[:-1]==s[1:]))
obs_adj = adj(famv)
null_global = np.array([adj(rng.permutation(famv)) for _ in range(NPERM)])
# nulo preservando grupo: permutar colores solo DENTRO de cada grupo
null_grp = []
for _ in range(NPERM):
    f = famv.copy()
    for g in sorted(set(grp)):
        idx = np.where(grp==g)[0]; f[idx] = rng.permutation(f[idx])
    null_grp.append(adj(f))
null_grp = np.array(null_grp)
p_glob = (np.sum(null_global>=obs_adj)+1)/(NPERM+1)
p_grp  = (np.sum(null_grp>=obs_adj)+1)/(NPERM+1)
print('\n=== color: adyacencias (misma familia) entre colgantes consecutivos ===')
print(f'  obs={obs_adj}  nulo_global media={null_global.mean():.2f} p={p_glob:.3f}  nulo_intragrupo media={null_grp.mean():.2f} p={p_grp:.3f}')

# --- indicador tiene-nudo: adyacencia de "1" consecutivos (pares)
def adj1(s): return int(np.sum((s[:-1]==1)&(s[1:]==1)))
obs_p = adj1(kn)
null_p = np.array([adj1(rng.permutation(kn)) for _ in range(NPERM)])
pp = (np.sum(null_p>=obs_p)+1)/(NPERM+1)
print(f'\n=== tiene-nudo: pares adyacentes de 1 ===\n  obs={obs_p}  nulo media={null_p.mean():.2f} max={null_p.max()} p={pp:.3f}')
print('  (los 6 colgantes anudados son p3p4 | p6p7 | p9p10 = 3 pares contiguos)')

# --- correccion multiple (Holm y BH-FDR) sobre todos los p del estudio
tests = {
 'madre=suma_hijas': 1.000, 'ternas_a+b=c': 0.508, 'razones_grupo': 0.414,
 'saez_pi_mult': 0.020, 'color_adyac_global': p_glob, 'color_adyac_intragrupo': p_grp,
 'tiene-nudo_lag1': 0.0, 'tiene-nudo_lag2': 0.0, 'tiene-nudo_lag3': 0.0,
 'tiene-nudo_pares': pp,
}
# recalcular los tres lags de tiene-nudo para tener valores reales
lags = {}
for lag in (1,2,3,4,5):
    obs = autocorr_matches(kn, lag)
    null = np.array([autocorr_matches(rng.permutation(kn), lag) for _ in range(NPERM)])
    lags[lag]= (obs, (np.sum(null>=obs)+1)/(NPERM+1))
tests['tiene-nudo_lag1']=lags[1][1]; tests['tiene-nudo_lag2']=lags[2][1]; tests['tiene-nudo_lag3']=lags[3][1]
ps = np.array(list(tests.values())); names = list(tests.keys())
order = np.argsort(ps)
m = len(ps)
# Holm
holm = np.empty(m); prev=0
for rank,i in enumerate(order):
    hv = min(1.0, (m-rank)*ps[i]); prev=max(prev,hv); holm[i]=prev
# BH-FDR
bh = np.empty(m); prev=1.0
for rank,i in enumerate(order[::-1]):
    bv = min(prev, ps[i]*m/(m-rank)); prev=bv; bh[i]=bv
print('\n=== correccion por comparaciones multiples (%d tests) ===' % m)
for i in order:
    print(f'  {names[i]:24s} p={ps[i]:.4f}  Holm={holm[i]:.4f}  BH={bh[i]:.4f}')
