"""UR004 - pruebas finales limpias + detalles estructurales para el informe."""
import pandas as pd, numpy as np, io
from collections import Counter
rng=np.random.default_rng(0); NP=1000
D='analisis/datos'
u=pd.read_csv(f'{D}/cuerdas.csv'); g=pd.read_csv(f'{D}/grupos.csv')
u=u[u.kfg=='UR004'].copy(); g=g[g.kfg=='UR004'].copy()
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

groups=[]
for _,r in g.iterrows():
    cs=list(lvl0.iloc[int(r.desde)-1:int(r.hasta)].cuerda)
    groups.append((int(r['grupo']), cs))

# T3 limpio: solo sumas NO triviales (cuenda = suma de >=2 ajenas con valor>0)
multi=[(gp,cs) for gp,cs in groups if len(cs)>=2]
def c3clean(pvmap):
    hits=0
    for gp,cs in multi:
        vs=[pvmap[c] for c in cs]; s=sum(vs)
        for i,c in enumerate(cs):
            others=[v for j,v in enumerate(vs) if j!=i]
            nz=[v for v in others if v>0]
            if len(nz)>=2 and abs(2*vs[i]-s)<1e-6: hits+=1; break
    return hits
o3=c3clean(valmap); n3=[c3clean(dict(zip(u['cuerda'],perm()))) for _ in range(NP)]
P('=== T3 LIMPIO (suma no trivial, >=2 sumandos con valor>0) ===')
P(f'obs {o3}/{len(multi)} | nulo {np.mean(n3):.2f} | p={emp(o3,n3):.3f}')

# max value
mx=u.loc[u.valor.idxmax()]
P('=== VALOR MAXIMO ===')
P(f'{mx.cuerda} valor={mx.valor} color={mx.color} grupo={mx.grupo} union={mx.union} nudos={mx.nudos}')

# total y reparto
P('=== TOTALES ===')
P(f'suma total (424 cuerdas con nudo): {num.valor.sum():.0f}')
P(f'mayor suma de grupo: {max(base[ix].sum() for gp,ix in [(gp,[name2i[c] for c in cs]) for gp,cs in groups]):.0f}')

# homogeneidad de color por grupo
homog=0; tot=0
for gp,cs in groups:
    if len(cs)<2: continue
    tot+=1; cols=[u.set_index('cuerda').loc[c,'color'] for c in cs]
    if len(set(cols))==1: homog+=1
P('=== COLOR POR GRUPO ===')
P(f'grupos multi monocromaticos: {homog}/{tot} = {homog/tot:.2f}')
# colores dominantes
P('colores grupo-0dominantes:', Counter([Counter([u.set_index("cuerda").loc[c,"color"] for c in cs]).most_common(1)[0][0] for gp,cs in groups if len(cs)>=2]).most_common())

# cuerdas sin nudo por nivel
P('=== SIN NUDOS ===')
P('sin nudo por nivel:', u[u.nudos.isna()].nivel.value_counts().to_dict())
P('sin nudo por color:', u[u.nudos.isna()].color.value_counts().head(8).to_dict())

# autocorrelacion de color por lag (tramo)
seqc=np.array(u.sort_values('orden')['color'])
def lag_same(seq,k):
    return int((seq[:-k]==seq[k:]).sum())
P('=== AUTOCORRELACION DE COLOR (lag 1-4) ===')
for k in [1,2,3,4]:
    o=lag_same(seqc,k); nn=[lag_same(rng.permutation(seqc),k) for _ in range(NP)]
    P(f'lag{k}: obs {o} | nulo {np.mean(nn):.1f} sd {np.std(nn):.1f} | z={(o-np.mean(nn))/np.std(nn):.1f} p={emp(o,nn):.3f}')

# direccion de nudo por nivel
P('=== DIRECCION NUDO POR NIVEL ===')
import re
for lv in [0,1,2]:
    dd=[]
    for s in u[(u.nivel==lv)&u.nudos.notna()].nudos:
        dd+= [m[1] for m in re.findall(r'\(([\d.]+),([SZU])\)', s)]
    P(f'nivel {lv}:', Counter(dd).most_common(4))

# cuerdas PK (marcadores en cordon principal)
P('=== CUERDAS PK (marcador en cordon principal) ===')
P(f'n={int((u.color=="PK").sum())}, todas valor 0: {bool((u[u.color=="PK"].valor==0).all())}')
P(u[u.color=='PK'][['orden','cuerda','grupo','notas']].head(6).to_string())

with open('analisis/ds/k_UR004/06_final.txt','w',encoding='utf-8') as f: f.write(out.getvalue())
print('WROTE 06_final.txt')
