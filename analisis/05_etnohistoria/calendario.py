"""Hipotesis calendarica: busca 'numeros magicos' en totales de quipu/grupo/secuencias y contrasta con nulos. Unidad: quipu.
uso: python calendario.py N_SIM MODO   (MODO = total_all|total_pend|grupo_all|grupo_pend|secuencia -> escribe parcial) ; python calendario.py N_SIM combine (une y corrige). Semilla fija por modo."""
import numpy as np, pandas as pd, sys, time
from scipy import stats
NSIM=int(sys.argv[1]) if len(sys.argv)>1 else 1000
MODO=sys.argv[2] if len(sys.argv)>2 else 'combine'
rng=np.random.default_rng(20261017+ (abs(hash(MODO))%1000 if False else sum(map(ord,MODO))))
D='./analisis/datos/'
c=pd.read_csv(D+'cuerdas.csv',low_memory=False)
c['valor']=c.valor.fillna(0)
EXACT=[27,28,29,30,328,354,355,360,365,656,708,710,720,730]          # 14 objetivos exactos
APPROX={'365±2':365,'360±2':360,'354.5±2':355,'328±2':328}           # 4 ventanas (|x-T|<=2; 355 cubre 353-357)
TARG=np.array(EXACT)
Q={}
for k,x in c.groupby('kfg',sort=False):
    x=x.sort_values('orden')
    if (x.valor>0).sum()<1: continue
    g=pd.factorize(x.grupo)[0]
    Q[k]=dict(v=x.valor.values.astype(float),niv=x.nivel.values,g=g,pm=(x.nivel.values==0),ng=g.max()+1)
print('quipus con algun valor>0:',len(Q))
WMAX=30
def hits_from(arr):
    """arr: array de numeros; devuelve vector bool [14 exactos + 4 aprox]"""
    a=np.asarray(arr)
    if a.size==0: return np.zeros(len(EXACT)+len(APPROX),bool)
    ex=(a[:,None]==TARG[None,:]).any(0)
    ap=np.array([(np.abs(a-t)<=2).any() for t in APPROX.values()])
    return np.r_[ex,ap]
def stat_all(q,v,mode):
    pm=q['pm']
    if mode=='total_all': return hits_from([v.sum()])
    if mode=='total_pend': return hits_from([v[pm].sum()])
    gs=np.bincount(q['g'],weights=v,minlength=q['ng'])
    if mode=='grupo_all': return hits_from(gs)
    gp=np.bincount(q['g'],weights=v*pm,minlength=q['ng'])
    if mode=='grupo_pend': return hits_from(gp[gp>=0])
    if mode=='secuencia':   # sumas de pendientes consecutivos, longitud 3..WMAX
        p=v[pm]; cs=np.r_[0,np.cumsum(p)]; s=[]
        for L in range(3,min(WMAX,len(p))+1): s.append(cs[L:]-cs[:-L])
        return hits_from(np.concatenate(s) if s else [])
def shuffle(q,mode):
    v=q['v'].copy(); niv=q['niv']
    if mode in('total_all','total_pend'):   # bootstrap con reemplazo dentro del estrato (conserva la distribucion de valores de ese quipu)
        for m in (niv==0,niv>0):
            idx=np.flatnonzero(m)
            if len(idx): v[idx]=q['v'][rng.choice(idx,len(idx))]
        return v
    for m in (niv==0,niv>0):                 # permutacion dentro del estrato (conserva valores y estructura)
        idx=np.flatnonzero(m); v[idx]=q['v'][rng.permutation(idx)]
    return v
MODES=['total_all','total_pend','grupo_all','grupo_pend','secuencia']
NAMES=[str(t) for t in EXACT]+list(APPROX)
rows=[]; t0=time.time()
for mode in ([MODO] if MODO!='combine' else []):
    obs=np.zeros(len(NAMES),int); 
    for k,q in Q.items(): obs+=stat_all(q,q['v'],mode)
    null=np.zeros((NSIM,len(NAMES)),int)
    for s in range(NSIM):
        for k,q in Q.items(): null[s]+=stat_all(q,shuffle(q,mode),mode)
    for j,n in enumerate(NAMES):
        p=(1+(null[:,j]>=obs[j]).sum())/(1+NSIM)
        rows.append(dict(familia=mode,objetivo=n,quipus_obs=obs[j],nulo_media=null[:,j].mean(),nulo_sd=null[:,j].std(),exceso=obs[j]-null[:,j].mean(),p=p))
    print(mode,'listo',round(time.time()-t0),'s',flush=True)
if MODO!='combine':
    pd.DataFrame(rows).to_csv('calendario_parcial_%s.csv'%MODO,index=False); sys.exit()
import glob
R=pd.concat([pd.read_csv(f) for f in sorted(glob.glob('calendario_parcial_*.csv'))],ignore_index=True)
# Holm sobre TODAS las pruebas (familias x objetivos)
def holm(p):
    p=np.asarray(p); o=np.argsort(p); m=len(p); adj=np.empty(m); run=0
    for i,ix in enumerate(o): run=max(run,(m-i)*p[ix]); adj[ix]=min(1,run)
    return adj
def bh(p):
    p=np.asarray(p); m=len(p); o=np.argsort(p); q=np.empty(m); prev=1
    for i in range(m-1,-1,-1): prev=min(prev,p[o[i]]*m/(i+1)); q[o[i]]=prev
    return q
# ---- conteo de grupos 12/24 y tamano de grupo 27-30 (metodo de vecinos, Poisson)
ng=pd.Series({k:q['ng'] for k,q in Q.items()})
cnt=ng.value_counts().sort_index()
def vecinos(cnt,T,w=3):
    nb=[cnt.get(T+d,0) for d in range(-w,w+1) if d!=0]; lam=np.mean(nb); k=cnt.get(T,0)
    return k,lam,stats.poisson.sf(k-1,lam)
extra=[]
for T in (12,24):
    k,lam,p=vecinos(cnt,T); extra.append(dict(familia='n_grupos',objetivo=str(T),quipus_obs=k,nulo_media=lam,nulo_sd=np.sqrt(lam),exceso=k-lam,p=p))
gsz=[]
for k,q in Q.items(): gsz.append(set(np.bincount(q['g']).tolist()))
csz=pd.Series([t for s in gsz for t in s]).value_counts().sort_index()   # n de quipus con >=1 grupo de tamano t (cuerdas con subsidiarias)
for T in (27,28,29,30):
    kk,lam,p=vecinos(csz,T); extra.append(dict(familia='cuerdas_por_grupo',objetivo=str(T),quipus_obs=kk,nulo_media=lam,nulo_sd=np.sqrt(lam),exceso=kk-lam,p=p))
R=pd.concat([R,pd.DataFrame(extra)],ignore_index=True)
R['p_holm']=holm(R.p); R['q_bh']=bh(R.p); R['n_pruebas']=len(R)
R.to_csv('calendario_resultados.csv',index=False)
pd.set_option('display.width',200)
print('n pruebas =',len(R)); print(R.sort_values('p').head(25).round(4).to_string())
print('\nn_grupos distribucion cerca de 12 y 24:',{t:int(cnt.get(t,0)) for t in range(8,30)})
