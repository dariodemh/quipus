# -*- coding: utf-8 -*-
"""Control del 'descubrimiento' de Saez-Rodriguez (2014) sobre UR019:
pi = 40.9/13, distancia Tierra-Luna = 24.6, S/Z-knots. Nulo y multiplicidad.
"""
import numpy as np, pandas as pd, os
rng = np.random.default_rng(0)
NPERM = 1000
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
C = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
d = C[C['kfg'] == 'UR019'].sort_values('orden').reset_index(drop=True)
val = d['valor'].to_numpy(float); lvl = d['nivel'].to_numpy(int)
name = d['cuerda'].astype(str).to_numpy(); n = len(val)

# pares madre->subsidiaria
pairs = []
for i in range(n):
    if lvl[i] != 0: continue
    ks = [j for j in range(n) if name[j].startswith(name[i]+'s')]
    for j in ks: pairs.append((i, j))
print('pares madre-subsidiaria:', [(name[i], int(val[i]), name[j], int(val[j])) for i,j in pairs])

def stat_SZ(v):
    """Suma de (colgante x subsidiaria). Saez reporta '40,9' (=408/10)."""
    s = sum(v[i]*v[j] for i,j in pairs)
    return s
S = stat_SZ(val)
print('\nSuma (colgante*subsidiaria) =', int(S), ' -> /10 =', S/10, ' -> (/10)/13 =', S/10/13)
print('Saez reporta 40,9 ; pi = 3,14159 ; nuestro valor /10/13 = %.4f' % (S/10/13))

# --- nulo: barajar valores, recomputar
perms = np.array([stat_SZ(rng.permutation(val)) for _ in range(NPERM)])
T = S/10/13; pi = np.pi
p_pi = (np.sum(np.abs(perms/10/13 - pi) < np.abs(T-pi)) + 1)/(NPERM+1)
print('Nulo suma: media=%.1f  P25=%.1f  P75=%.1f  max=%.1f' % (perms.mean(), np.percentile(perms,25), np.percentile(perms,75), perms.max()))
print('p(|T-pi| <= |obs-pi|) =', round(p_pi,3), ' (nulo, 1000 perm, semilla 0)')

# --- multiplicidad: cuantos divisores producen 'constantes famosas'
FAMOSAS = {'pi':3.14159,'2pi':6.28318,'e':2.71828,'phi':1.61803,'raiz2':1.41421,
           'sinodico29.5':29.5,'sidero27.32':27.25,'327':327,'328':328,'110':110,
           '2.5':2.5,'365':365,'360':360,'12':12,'24':24}
DIV = sorted(set([d for k in list(range(1,31))+[13,26,100,1000,10000] for d in (k,10*k,100*k)]))
def score(v):
    s = stat_SZ(v); hits = 0; det=[]
    for dv in DIV:
        x = s/dv
        for k,c in FAMOSAS.items():
            if abs(x-c)/c < 0.005:
                hits += 1; det.append((int(s),dv,k,round(x,3)))
    return hits, det
h_obs, det = score(val)
print('\nMultiplicidad (divisores 1..30,13,26,100,1000,10000 x 15 constantes, tol 0,5%%):')
print('  aciertos observados =', h_obs, '->', det)
perm_scores = np.array([score(rng.permutation(val))[0] for _ in range(NPERM)])
p_mult = (np.sum(perm_scores >= h_obs)+1)/(NPERM+1)
print('  nulo: media=%.2f  max=%d  p(>=obs)=%.3f' % (perm_scores.mean(), perm_scores.max(), p_mult))

# --- S/Z knots: reproducibilidad
import re
dirs = []
for s in d['nudos'].dropna():
    dirs += re.findall(r'\([0-9.]+,([SZU])\)', str(s))
print('\nDirecciones de nudo reales (KFG=OKR):', {k:dirs.count(k) for k in set(dirs)})
print('Saez afirma Z-knots=16,3 y S-knots=24,6 . En los datos solo hay 1 nudo S (p4).')
print('NO reproducible: la particion S/Z que sostiene su tesis no existe en UR019.')

# --- totales y su 'redondez'
print('\nSuma colgantes=%d  subsidiarias=%d  total=%d  (total=100)' % (val[lvl==0].sum(), val[lvl==1].sum(), val.sum()))
# nulo de redondez: dado el MISMO multiset, el total es invariante -> no testeable por permutacion.
# complementario: valores reales vs enteros aleatorios 0..30 (mismo n), prob total multiplo de 10
rr = np.random.default_rng(0)
tot = np.array([rr.integers(0,31,size=n).sum() for _ in range(20000)])
print('  P(total multiplo de 10 | 18 enteros U[0,30]) =', round(np.mean(tot%10==0),3), '(referencia)')
