# -*- coding: utf-8 -*-
"""UR093: tests de aritmetica interna con modelo nulo (permutacion de valores, 1000x, seed 0)."""
import pandas as pd, numpy as np, re
rng0 = 0
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg=='UR093'].copy(); u['valor']=u.valor.fillna(0)
u['valor']=u.valor.astype(int)

# --- jerarquia ---
padre = dict(zip(u.cuerda,u.padre))
nivel = dict(zip(u.cuerda,u.nivel))
n0 = u[u.nivel==0].cuerda.tolist()
l1 = u[u.nivel==1].copy(); l1['pos']=l1.groupby('padre').cumcount()+1
l2 = u[u.nivel==2].copy()

def valmap(df): return dict(zip(df.cuerda,df.valor))

# suma de nivel2 por madre (nivel1)
sum2 = l2.groupby('padre').valor.sum().to_dict()
# valor total de cada nivel1 = propio + hijos nivel2
l1['vtot']=l1.valor+l1.padre.map(lambda p:sum2.get(p,0))

def sum_subs(p, V, include_markers=True):
    sub=l1[l1.padre==p]
    if not include_markers:
        sub=sub[~sub.pos.isin([6,7])]
    return sub.cuerda.map(lambda c: V[c]+sum2.get(c,0)).sum()

V0=valmap(u)

# ---------- H1: colgante = suma subsidiarias ----------
con=[p for p in n0 if (u.padre==p).sum()>0]
def count_matches(V):
    return sum(1 for p in con if V[p]==sum_subs(p,V))
obs=count_matches(V0)
vals=u.valor.values
N=len(con)
def perm_test(fn, n=1000, seed=0):
    rng=np.random.default_rng(seed); cnt=0
    base=u.valor.values.copy()
    for _ in range(n):
        sh=rng.permutation(base)
        Vd=dict(zip(u.cuerda,sh))
        cnt+=fn(Vd)
    return cnt/n
p1=perm_test(lambda V: sum(1 for p in con if V[p]==sum_subs(p,V)))
print(f'H1 colgante=suma subs: obs={obs}/{N}={obs/N:.3f}  nulo={p1:.3f}  p={(p1>=obs/N):.4f}')

# ---------- H2: nivel1 = suma nivel2 (madres anidadas) ----------
nest=[p for p in l1.cuerda if (u.padre==p).sum()>0]
obs2=sum(1 for c in nest if V0[c]==sum2.get(c,0))
print(f'H2 nivel1=suma nivel2: obs={obs2}/{len(nest)}')
for c in nest:
    print('   ',c,'val',V0[c],'sumHijos',sum2.get(c,0))

# ---------- H3: grupo = suma de pendantes / suma de grupos ----------
g0=u[u.nivel==0]
print('\nsuma pendantes por grupo:', g0.groupby('grupo').valor.sum().to_dict())
print('suma total pendantes',int(g0.valor.sum()),'| suma total nivel1 hojas',int(l1.valor.sum()))

# ---------- H4: valores repetidos / razones ----------
print('\nmayor pendante por grupo:')
for grp,s in g0.groupby('grupo'):
    mx=s.valor.max()
    print(f'  g{grp}: max={int(mx)} suma={int(s.valor.sum())} n={len(s)} ratio_max/suma={mx/s.valor.sum() if s.valor.sum() else 0:.2f}')

# ---------- Permutacion: estructura posicional de valores (pos1-5 vs 6,7,8) ----------
print('\n== valores por posicion en sets (116) y nulo ==')
cnt=l1.groupby('padre').size(); sets=cnt[cnt>=7].index
S=l1[l1.padre.isin(sets)]
obs_pos={p:int(S[S.pos==p].valor.sum()) for p in range(1,10)}
print('obs suma por pos:',obs_pos)
rng=np.random.default_rng(0)
nulltot={p:[] for p in range(1,10)}
S2=S.copy()
for _ in range(1000):
    sh=rng.permutation(S2.valor.values)
    for p in range(1,10):
        nulltot[p].append(sh[(S2.pos==p).values].sum())
for p in range(1,10):
    na=np.array(nulltot[p]); 
    print(f'  pos{p}: obs={obs_pos[p]} nuloMedia={na.mean():.1f} p(obs>=null)={ (na>=obs_pos[p]).mean():.3f}')
