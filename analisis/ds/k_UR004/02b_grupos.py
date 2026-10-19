"""UR004 - pruebas a nivel de grupo CON la definicion correcta de grupos.
desde/hasta de grupos.csv = posicion 1-based entre las cuerdas nivel 0 (pendientes)."""
import pandas as pd, numpy as np, io
from collections import Counter
rng=np.random.default_rng(0); NP=1000
D='analisis/datos'
u=pd.read_csv(f'{D}/cuerdas.csv'); g=pd.read_csv(f'{D}/grupos.csv')
u=u[u.kfg=='UR004'].copy()
g=g[g.kfg=='UR004'].copy()
lvl0=u[u.nivel==0].sort_values('orden').reset_index(drop=True)
name2i={c:i for i,c in enumerate(u['cuerda'])}
num=u[u.nudos.notna()]; vals=num['valor'].to_numpy(float)
kpos=np.array([name2i[c] for c in num['cuerda']])
valmap=dict(zip(u['cuerda'],u['valor']))
def perm():
    pv=np.zeros(len(u)); pv[kpos]=rng.permutation(vals); return pv
base=np.array([valmap[c] for c in u['cuerda']],float)
out=io.StringIO()
def P(*a): print(*a); print(*a,file=out)
def emp(o,n): n=np.asarray(n); return (1+(n>=o).sum())/(1+len(n))

# indice (posicion en u) de las cuerdas de cada grupo
groups=[]
for _,r in g.iterrows():
    cs=lvl0.iloc[int(r.desde)-1:int(r.hasta)]['cuerda']
    groups.append((int(r['grupo']), [name2i[c] for c in cs]))
P('=== TAMANO DE GRUPO (correcto) ===')
sizes={gp:len(ix) for gp,ix in groups}
P('n grupos', len(groups), '| tam min/max/med', min(sizes.values()), max(sizes.values()), int(np.median(list(sizes.values()))))
P('grupos de 1 cuerda:', sum(1 for v in sizes.values() if v==1), 'de multi:', sum(1 for v in sizes.values() if v>1))
P('suma de cuerdas:', sum(sizes.values()))

# suma por grupo
sums={gp: base[ix].sum() for gp,ix in groups}
P('=== SUMA POR GRUPO (correcta) ===')
P({gp:round(sums[gp],1) for gp,_ in groups})

# ---------- T3: alguna cuerda del grupo = suma de las demas ----------
multi=[ix for gp,ix in groups if len(ix)>=2]
def c3(pv):
    return sum(1 for ix in multi if any(abs(2*pv[i]-pv[ix].sum())<1e-6 for i in ix))
o3=c3(base); n3=[c3(perm()) for _ in range(NP)]
P('=== T3 grupo: cuerda = suma de las demas ===')
P(f'obs {o3}/{len(multi)} | nulo {np.mean(n3):.2f} | p={emp(o3,n3):.3f}')

# ---------- T4: suma de grupo multi = valor de cuerda AJENA ----------
def c4(pv):
    vs=set(np.round(pv[pv!=0],3)); c=0
    for gp,ix in groups:
        if len(ix)<2: continue
        s=pv[ix].sum()
        if s>0 and round(s,3) in vs and all(abs(pv[i]-s)>1e-6 for i in ix): c+=1
    return c
o4=c4(base); n4=[c4(perm()) for _ in range(NP)]
P('=== T4 suma de grupo = cuerda ajena ===')
P(f'obs {o4} | nulo {np.mean(n4):.2f} | p={emp(o4,n4):.3f}')

# ---------- A: sumas de grupo repetidas ----------
def cA(pv):
    s=[round(pv[ix].sum(),3) for gp,ix in groups if pv[ix].sum()>0]
    c=Counter(s); return sum(v-1 for v in c.values() if v>1)
oA=cA(base); nA=[cA(perm()) for _ in range(NP)]
P('=== A sumas de grupo repetidas ===')
P(f'obs {oA} | nulo {np.mean(nA):.2f} | p={emp(oA,nA):.3f}')
cc=Counter(round(v,3) for v in sums.values() if v>0)
P('sumas repetidas:', {k:v for k,v in cc.items() if v>1})

# ---------- T9: entropia color por grupo ----------
def ent(pv):
    hs=[]
    for gp,ix in groups:
        if len(ix)<2: continue
        _,cnt=np.unique(pv[ix],return_counts=True); p=cnt/cnt.sum()
        hs.append(-(p*np.log2(p)).sum())
    return float(np.mean(hs))
colbase=np.array([u.set_index('cuerda').loc[c,'color'] for c in u['cuerda']])
o9=ent(colbase); n9=[ent(rng.permutation(colbase)) for _ in range(NP)]
P('=== T9 entropia color por grupo ===')
P(f'obs {o9:.3f} | nulo {np.mean(n9):.3f} sd {np.std(n9):.3f} | p(menor)={emp(-o9,[-x for x in n9]):.3f}')

with open('analisis/ds/k_UR004/02b_grupos.txt','w',encoding='utf-8') as f: f.write(out.getvalue())
print('WROTE 02b_grupos.txt')
