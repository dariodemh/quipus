"""UR1032 — banco de pruebas con nulo por permutacion (semilla 0) + Holm."""
import pandas as pd, numpy as np, re
rng = np.random.default_rng(0)
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg=='UR1032'].copy().sort_values('orden').reset_index(drop=True)
def ab(c):
    if pd.isna(c): return '?'
    for t in re.split(r'[^A-Za-z]+', str(c)):
        if t: return t[:3]
    return '?'
s['cab']=s.color.map(ab)
col=s[s.nivel==0].copy()
col['size']=col.groupby('grupo')['grupo'].transform('size')
gsum=col.groupby('grupo').valor.sum()
gsize=col.groupby('grupo').size()
vals=col.sort_values('orden').valor.values
grupos=col.sort_values('orden').grupo.values
sizes_map=col.groupby('grupo')['size'].first()

tests=[]
def holm(pvals, names):
    order=np.argsort(pvals); m=len(pvals); out=[0]*m; prev=0
    for i,idx in enumerate(order):
        v=pvals[idx]*(m-i); v=max(v,prev); prev=v; out[idx]=min(v,1)
    return out

# --- T1: color determinado por tamano de grupo ---
# estadistico: fraccion de cuerdas en grupos de 5 que son LB + en grupos de 3 que son W
def t1(colors, sizes):
    m5 = sizes==5; m3=sizes==3
    return np.mean(colors[m5]=='LB') + np.mean(colors[m3]=='W')
obs1=t1(col.cab.values, col['size'].values)
n1=0
for _ in range(1000):
    cp=rng.permutation(col.cab.values)
    if t1(cp,col['size'].values)>=obs1: n1+=1
tests.append(('T1 color~tamano grupo (5=LB,3=W)', obs1, n1/1000))

# --- T2: densidad de valor azul(5) vs blanco(3) ---
def dens(vals, sizes):
    return np.mean(vals[sizes==5]) - np.mean(vals[sizes==3])
obs2=dens(vals, col['size'].values); n2=0
for _ in range(1000):
    vp=rng.permutation(vals)
    if dens(vp,col['size'].values)>=obs2: n2+=1
tests.append(('T2 valor medio 5-grupos > 3-grupos', obs2, n2/1000))

# --- T3: colgante = suma de subsidiarias ---
sub=s[s.nivel==1]
def frac_sum(vals_all, order):
    # reconstruye df con valores permutados
    d=pd.DataFrame({'cuerda':s.sort_values('orden').cuerda.values,
                    'padre':s.sort_values('orden').padre.values,
                    'nivel':s.sort_values('orden').nivel.values,'v':vals_all})
    madres=d[(d.nivel==0)&d.cuerda.isin(d[d.nivel==1].padre)]
    ss=d[d.nivel==1].groupby('padre').v.sum()
    mm=madres.set_index('cuerda').v
    idx=[c for c in mm.index if c in ss.index]
    return np.mean([mm[c]==ss[c] for c in idx])
allv=s.sort_values('orden').valor.values
obs3=frac_sum(allv,None); n3=0
for _ in range(1000):
    vp=rng.permutation(allv)
    if frac_sum(vp,None)>=obs3: n3+=1
tests.append(('T3 colgante=suma subsidiarias', obs3, n3/1000))

# --- T4: igualdad de suma entre pares (5,3) adyacentes ---
def pairs_eq(vals, groups, sizes_map):
    d=pd.DataFrame({'g':groups,'v':vals})
    gs=d.groupby('g').v.sum()
    gsizes=sizes_map
    eq=0; tot=0
    for g in range(107):
        if g in gsizes and g+1 in gsizes and {gsizes[g],gsizes[g+1]}=={5,3}:
            if gs[g]==gs[g+1]: eq+=1
            tot+=1
    return eq/tot
obs4=pairs_eq(vals, grupos, sizes_map); n4=0
for _ in range(1000):
    vp=rng.permutation(vals)
    if pairs_eq(vp,grupos,sizes_map)>=obs4: n4+=1
tests.append(('T4 suma 5-grupo = suma 3-grupo adyacente', obs4, n4/1000))

# --- T5: lag-8 autocorrelacion ---
v=vals-vals.mean(); n=len(v)
def lag8(x): return np.sum(x[:n-8]*x[8:])/np.sum(x*x)
obs5=lag8(v); n5=0
for _ in range(1000):
    vp=rng.permutation(v)
    if abs(lag8(vp))>=abs(obs5): n5+=1
tests.append(('T5 autocorrelacion lag-8', obs5, n5/1000))

# --- T6: colgante 5-grupo repite valor de otro 5-grupo en su misma posicion (periodicidad) ---
# prueba: diferencia de valores entre grupos adyacentes del mismo tamano
def rep(vals, groups, sizes_map):
    d=pd.DataFrame({'g':groups,'v':vals,'o':range(len(vals))})
    # suma por grupo, comparar grupos separados por 2 (mismo tamano)
    gs=d.groupby('g').v.sum()
    gids=[g for g in range(106) if g in sizes_map and g+2 in sizes_map and sizes_map[g]==sizes_map[g+2]]
    return np.mean([gs[g]==gs[g+2] for g in gids])
obs6=rep(vals,grupos,sizes_map); n6=0
for _ in range(1000):
    vp=rng.permutation(vals)
    if rep(vp,grupos,sizes_map)>=obs6: n6+=1
tests.append(('T6 suma igual a 2 grupos de distancia (mismo color)', obs6, n6/1000))

# --- T7: tasa de subsidiaria 3-grupos > 5-grupos ---
nsub=col.cuerda.map(s[s.nivel==1].padre.value_counts()).fillna(0).values
sz=col['size'].values
def subrate(nsub,sz): return np.mean(nsub[sz==3])-np.mean(nsub[sz==5])
obs7=subrate(nsub,sz); n7=0
for _ in range(1000):
    np_=rng.permutation(nsub)
    if subrate(np_,sz)>=obs7: n7+=1
tests.append(('T7 tasa subsidiaria 3-grupos > 5-grupos', obs7, n7/1000))

# Holm
pvals=[t[2] for t in tests]; names=[t[0] for t in tests]
adj=holm(pvals,names)
print(f"{'test':<50}{'obs':>9}{'p_emp':>9}{'p_Holm':>9}")
for (nm,ob,p),a in zip(tests,adj):
    print(f'{nm:<50}{ob:>9.3f}{p:>9.3f}{a:>9.3f}')
print('\nHolm: m =',len(tests))
