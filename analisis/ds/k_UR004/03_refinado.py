"""UR004 - pruebas refinadas + correccion de multiplicidad."""
import pandas as pd, numpy as np, io
from collections import defaultdict, Counter
rng = np.random.default_rng(0); NP = 1000
D='analisis/datos'
u = pd.read_csv(f'{D}/cuerdas.csv'); g = pd.read_csv(f'{D}/grupos.csv')
u = u[u.kfg=='UR004'].copy().reset_index(drop=True)
g = g[g.kfg=='UR004'].copy().reset_index(drop=True)
ALLN=len(u); name2i={c:i for i,c in enumerate(u['cuerda'])}
num=u[u.nudos.notna()]; vals=num['valor'].to_numpy(float)
kpos=np.array([name2i[c] for c in num['cuerda']])
valmap=dict(zip(u['cuerda'],u['valor']))
def perm():
    pv=np.zeros(ALLN); pv[kpos]=rng.permutation(vals); return pv
base=np.array([valmap[c] for c in u['cuerda']],float)
out=io.StringIO()
def P(*a): print(*a); print(*a,file=out)
def emp(obs,nulls): n=np.asarray(nulls); return (1+(n>=obs).sum())/(1+len(n))

# grupos multi
mg=[]
for _,r in g.iterrows():
    idx=[name2i[c] for c in u[(u.orden>=r['desde'])&(u.orden<=r['hasta'])]['cuerda']]
    mg.append((int(r['grupo']),int(r['desde']),int(r['hasta']),idx))
sums={grp: base[idx].sum() for grp,_,_,idx in mg}
P('=== SUMA POR GRUPO ===')
for grp,_,_,idx in mg:
    P(f'g{grp:2d} n={len(idx):2d} suma={sums[grp]:7.1f}')

# A) sumas de grupo repetidas
cnt=Counter(round(v,3) for v in sums.values() if v>0)
rep={k:v for k,v in cnt.items() if v>1}
P('=== A: sumas de grupo repetidas ===')
P('valores de suma con >1 grupo:', rep)
def count_rep(pv):
    s={grp: pv[idx].sum() for grp,_,_,idx in mg}
    c=Counter(round(v,3) for v in s.values() if v>0)
    return sum(v-1 for v in c.values() if v>1)
obsA=count_rep(base); nullA=[count_rep(perm()) for _ in range(NP)]
P(f'obs pares-duplicados {obsA} | nulo media {np.mean(nullA):.2f} | p={emp(obsA,nullA):.3f}')

# B) "cuerda resumen": grupo multi seguido/precedido por grupo de 1 cuerda cuyo valor = suma
gorder=[(int(r['grupo']),int(r['desde']),int(r['hasta'])) for _,r in g.iterrows()]
sz={grp:h-d+1 for grp,d,h in gorder}
def val_of_group(grp):
    d,h=[(d,h) for gg,d,h in gorder if gg==grp][0]
    idx=[name2i[c] for c in u[(u.orden>=d)&(u.orden<=h)]['cuerda']]
    return base[idx].sum()
def summary_hits(pv):
    # reconstruir valores por grupo
    gv={grp:(pv[[name2i[c] for c in u[(u.orden>=d)&(u.orden<=h)]['cuerda']]].sum()) for grp,d,h in gorder}
    c=0
    for grp,d,h in gorder:
        if sz[grp]<2: continue
        s=gv[grp]
        for nb in (grp-1,grp+1):
            if nb in sz and sz[nb]==1 and abs(gv[nb]-s)<1e-6: c+=1
    return c
obsB=summary_hits(base); nullB=[summary_hits(perm()) for _ in range(NP)]
P('=== B: grupo de 1 cuerda adyacente = suma del grupo vecino multi ===')
P(f'obs {obsB} | nulo media {np.mean(nullB):.2f} | p={emp(obsB,nullB):.3f}')

# C) runs de color (maximo tramo consecutivo mismo color)
def max_run(seq):
    best=cur=1
    for i in range(1,len(seq)):
        cur = cur+1 if seq[i]==seq[i-1] else 1
        best=max(best,cur)
    return best
colarr=np.array(u.sort_values('orden')['color'])
obsC=max_run(colarr); nullC=[max_run(rng.permutation(colarr)) for _ in range(NP)]
P('=== C: tramo maximo de color igual ===')
P(f'obs {obsC} | nulo media {np.mean(nullC):.2f} | p={emp(obsC,nullC):.3f}')

# D) subsidiarias comparten color con la madre?
subs=u[u.nivel>0]
same=sum(1 for _,r in subs.iterrows() if r['color']==valmap.get(r['padre'],None) or r['color']==u.set_index('cuerda').loc[r['padre'],'color'])
P('=== D: subsidiaria mismo color que madre ===')
P(f'{same}/{len(subs)} = {same/len(subs):.2f}')

# E) estructura de digitos
P('=== E: digitos de los valores con nudo ===')
d1=(num['valor']%10).astype(int); d10=((num['valor']//10)%10).astype(int); d100=((num['valor']//100)%10).astype(int)
P('unidades  :', d1.value_counts().sort_index().to_dict())
P('decenas   :', d10.value_counts().sort_index().to_dict())
P('centenas  :', d100.value_counts().sort_index().to_dict())

# F) deltas entre cuerdas consecutivas iguales (configuraciones repetidas)
vseq=u.sort_values('orden')['valor'].to_numpy(float)
P('=== F: valores mas frecuentes entre las 424 con nudo ===')
P(num['valor'].value_counts().head(12).to_dict())

with open('analisis/ds/k_UR004/03_refinado.txt','w',encoding='utf-8') as f: f.write(out.getvalue())
print('WROTE 03_refinado.txt')
