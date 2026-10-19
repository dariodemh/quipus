# -*- coding: utf-8 -*-
"""Aritmetica interna de UR019 + controles nulos (permutacion de valores, 1000x, semilla 0).
Cuerdas fijas leidas de analisis/datos/cuerdas.csv (KFG). Salida compacta.
"""
import numpy as np, pandas as pd, re, os
from itertools import combinations
rng0 = 0
NPERM = 1000
rng = np.random.default_rng(rng0)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
C = pd.read_csv(os.path.join(ROOT, 'analisis', 'datos', 'cuerdas.csv'))
d = C[C['kfg'] == 'UR019'].sort_values('orden').reset_index(drop=True)

# nivel, grupo, valor, color, union, tiene_nudos
val   = d['valor'].to_numpy(float)
lvl   = d['nivel'].to_numpy(int)
grp   = d['grupo'].to_numpy(int)
col   = d['color'].astype(str).to_numpy()
uno   = d['union'].astype(str).to_numpy()
kn    = d['nudos'].notna().to_numpy()
name  = d['cuerda'].astype(str).to_numpy()
n = len(val)

def fam(c):
    c = c.upper()
    if ':' in c or '-' in c or '/' in c: return 'mixed'
    base = re.sub(r'[^A-Z]', '', c)
    if base in ('W',): return 'white'
    if base in ('BL', 'B', 'LB', 'NB'): return 'blue/black'
    if base in ('AB', 'MB', 'KB', 'YB'): return 'brown'
    return 'other'
familia = np.array([fam(c) for c in col])

def suma_grupo(v):
    return {g: v[(grp == g) & (lvl == 0)].sum() for g in sorted(set(grp))}

print('=== A. ESTRUCTURA NUMERICA ===')
print('valores colgantes:', list(zip(name[lvl==0], val[lvl==0])))
print('valores subsidiarias:', list(zip(name[lvl==1], val[lvl==1])))
print('suma colgantes =', int(val[lvl==0].sum()), '| suma subsidiarias =', int(val[lvl==1].sum()),
      '| suma total =', int(val.sum()))
print('suma por grupo (colgantes):', suma_grupo(val))
print('n cuerdas con nudo:', int(kn.sum()), '/', n)
print('posiciones con nudo (colgantes):', list(name[(lvl==0)&kn]))

# ---- Test 1: madre = suma de sus hijas
def matches_madre(v):
    c = 0
    for i in range(n):
        if lvl[i] != 0: continue
        kids = np.where((lvl == 1))[0]
        # hijo si su padre (via nombre) empieza por name[i]+'s'
        ks = [j for j in range(n) if name[j].startswith(name[i]+'s')]
        if ks and abs(v[i] - sum(v[j] for j in ks)) < 1e-9:
            c += 1
    return c
obs_madre = matches_madre(val)
print('\n[Test 1] madre == suma(hijas): observado =', obs_madre, '(de 5 madres)')

# ---- Test 2: pares con razon entera 2..10 entre valores != 0
def ratio_pairs(v):
    L = [x for x in v if x > 0]
    c, ex = 0, []
    for a, b in combinations(range(len(L)), 2):
        hi, lo = max(L[a],L[b]), min(L[a],L[b])
        if lo > 0:
            r = hi/lo
            if abs(r-round(r))<1e-9 and 2 <= round(r) <= 10:
                c += 1; ex.append((hi,lo,int(round(r))))
    return c, ex
obs_r, ex_r = ratio_pairs(val)
print('\n[Test 2] pares con razon entera 2..10:', obs_r, '->', ex_r)

# ---- Test 3: ternas aditivas a+b=c (cuerdas distintas)
def add_triples(v):
    L = list(v); c = 0; ex = []
    for a, b, cc in combinations(range(n), 3):
        if v[a]+v[b] == v[cc] and v[cc] > 0:
            c += 1; ex.append(tuple(sorted([int(v[a]),int(v[b]),int(v[cc])])))
    return c, ex
obs_t, ex_t = add_triples(val)
print('\n[Test 3] ternas a+b=c:', obs_t, '->', sorted(set(ex_t)))

# ---- Test 4: valores iguales (pares) entre != 0
def eq_pairs(v):
    L=[x for x in v if x>0]; c=0
    for a,b in combinations(range(len(L)),2):
        if L[a]==L[b]: c+=1
    return c
obs_eq = eq_pairs(val)
print('\n[Test 4] pares de valores iguales (!=0):', obs_eq)

# ---- Test 5: suma de grupos -> alguna razon entera entre sumas
gs = list(suma_grupo(val).values())
gsnz = [x for x in gs if x > 0]
def ratio_pairs_list(L):
    c=0
    for a,b in combinations(range(len(L)),2):
        hi,lo=max(L[a],L[b]),min(L[a],L[b])
        if lo>0 and abs(hi/lo-round(hi/lo))<1e-9 and 2<=round(hi/lo)<=10: c+=1
    return c
obs_gr = ratio_pairs_list(gsnz)
print('\n[Test 5] razones enteras entre sumas de grupo:', obs_gr, '(sumas no nulas', gsnz, ')')

# ---- Test 6: nudos con direccion S/Z
dirs=[]
for s in d['nudos'].dropna():
    dirs += re.findall(r'\([0-9.]+,([SZU])\)', str(s))
print('\n[Test 6] direcciones de nudo:', {k:dirs.count(k) for k in set(dirs)})

# ================= NULOS =================
def perm_stats(v):
    """recalcula los estadisticos sobre un vector de valores permutado."""
    m = matches_madre(v)
    r,_ = ratio_pairs(v)
    t,_ = add_triples(v)
    e = eq_pairs(v)
    gsnz = [x for x in {g: v[(grp==g)&(lvl==0)].sum() for g in sorted(set(grp))}.values() if x>0]
    gr = ratio_pairs_list(gsnz)
    return m, r, t, e, gr

print('\n=== B. NULOS (barajar los 18 valores dentro del quipu, 1000x, semilla 0) ===')
perm = np.array([perm_stats(rng.permutation(val)) for _ in range(NPERM)])
labels = ['madre=suma(hijas)', 'razones enteras', 'ternas a+b=c', 'valores iguales', 'razones de grupo']
obs = [obs_madre, obs_r, obs_t, obs_eq, obs_gr]
for k,lab in enumerate(labels):
    col_perm = perm[:,k]
    p = (np.sum(col_perm >= obs[k]) + 1) / (NPERM + 1)
    print(f'  {lab:22s} obs={obs[k]:3d}  media_nulo={col_perm.mean():6.2f}  max_nulo={col_perm.max():3d}  p(>=obs)={p:.3f}')

# ---- Test global combinado: cuantos de los 5 tipos dan "acierto" (obs>0)
observed_types = sum(1 for o in obs if o > 0)
perm_types = np.sum(perm > 0, axis=1)
p_comb = (np.sum(perm_types >= observed_types) + 1) / (NPERM + 1)
print(f'  TIPOS con acierto: obs={observed_types}/5  media_nulo={perm_types.mean():.2f}  p(>=obs)={p_comb:.3f}')

# ================= COLOR =================
print('\n=== C. COLOR ===')
print('color por cuerda:', list(zip(name, col)))
print('familia por cuerda:', list(zip(name, familia)))
# color vs tiene nudos (colgantes)
from scipy.stats import fisher_exact, chi2_contingency
pnd = lvl==0
tab = pd.crosstab(familia[pnd], kn[pnd])
print('tabla (colgantes) familia x tiene_nudo:\n', tab.to_string())
if tab.shape[0]>1 and tab.shape[1]>1:
    chi2,pchi,_,_ = chi2_contingency(tab)
    print('chi2=%.2f p=%.3f' % (chi2,pchi))
# adyacencia de color (misma familia colgantes consecutivos)
fam_p = familia[pnd]
obs_adj = int(np.sum(fam_p[:-1]==fam_p[1:]))
def adj_colors(f):
    return int(np.sum(f[:-1]==f[1:]))
perms_adj = np.array([adj_colors(rng.permutation(fam_p)) for _ in range(NPERM)])
p_adj = (np.sum(perms_adj>=obs_adj)+1)/(NPERM+1)
print(f'adyacencias de color (colgantes): obs={obs_adj}  media_nulo={perms_adj.mean():.2f}  p={p_adj:.3f}')
# periodos
for per in (2,3,4):
    obs_per = int(np.sum(fam_p[:-per]==fam_p[per:]))
    pp = np.array([int(np.sum(rng.permutation(fam_p)[:-per]==rng.permutation(fam_p)[per:])) for _ in range(NPERM)]) if False else None
    # hacer bien: permutar una vez por iteracion
    cnt=0
    for _ in range(200):
        f=rng.permutation(fam_p)
        if int(np.sum(f[:-per]==f[per:]))>=obs_per: cnt+=1
    print(f'periodo {per}: matches obs={obs_per}  p={ (cnt+1)/201:.3f} (200 perm)')
