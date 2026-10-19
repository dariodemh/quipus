"""Firmas numericas de las categorias que las fuentes coloniales dicen que registraban los quipus. Unidad: quipu. Semilla fija.
uso: python firmas_coloniales.py [N_SIM]"""
import numpy as np, pandas as pd, sys, time, itertools
from collections import defaultdict
from scipy import stats
NS=int(sys.argv[1]) if len(sys.argv)>1 else 2000
rng=np.random.default_rng(20261018)
D='./analisis/datos/'
c=pd.read_csv(D+'cuerdas.csv',low_memory=False); c['valor']=c.valor.fillna(0)
meta=pd.read_csv(D+'quipus.csv').set_index('kfg')
Q={}
for k,x in c.groupby('kfg',sort=False):
    x=x.sort_values('orden')
    if (x.valor>0).sum()<1: continue
    pm=(x.nivel==0).values
    Q[k]=dict(v=x.valor.values.astype(float),niv=x.nivel.values,g=pd.factorize(x.grupo)[0],pm=pm,
              tors=x.torsion.values,uni=x.union.values,col=x.color.fillna('NA').values,nud=x.nudos.isna().values,prov=str(meta.loc[k,'procedencia']))
    Q[k]['ng']=Q[k]['g'].max()+1
rows=[]
def add(cat,firma,obs,nm,p,nota=''): rows.append(dict(categoria=cat,firma=firma,quipus_obs=obs,nulo_media=nm,p=p,nota=nota))
def pemp(obs,null): return (1+(np.asarray(null)>=obs).sum())/(1+len(null))
def run(shuf,stat,ns):
    obs=sum(np.asarray(stat(q,q['v']),int) for q in Q.values()); null=[]
    for s in range(ns): null.append(sum(np.asarray(stat(q,shuf(q)),int) for q in Q.values()))
    return obs,np.array(null)
def boot(q):   # bootstrap dentro del estrato (colgantes / subsidiarias): conserva la distribucion de valores del quipu, cambia totales
    v=q['v'].copy()
    for m in (q['niv']==0,q['niv']>0):
        idx=np.flatnonzero(m)
        if len(idx): v[idx]=q['v'][rng.choice(idx,len(idx))]
    return v
def perm(q):   # permutacion dentro del estrato: conserva valores y estructura, rompe posicion/agrupacion
    v=q['v'].copy()
    for m in (q['niv']==0,q['niv']>0):
        idx=np.flatnonzero(m); v[idx]=q['v'][rng.permutation(idx)]
    return v
t0=time.time()
CAT1='decimal admin (chunka/pachaka/waranqa/hunu)'
# ---------- 1. Decimal administrativo
TT=[10,100,1000,10000]; NM1=[f'={t}' for t in TT]+[f'~{t}(+-2%)' for t in TT[1:]]+['%100==0 y >=100','%1000==0 y >=1000']
def hit_tot(x):
    h=[x==t for t in TT]+[abs(x-t)<=0.02*t for t in TT[1:]]+[(x%100==0)&(x>=100),(x%1000==0)&(x>=1000)]; return np.array(h,int)
def st_tot_all(q,v): return hit_tot(v.sum())
def st_tot_pen(q,v): return hit_tot(v[q['pm']].sum())
def st_grp(q,v):
    gs=np.bincount(q['g'],weights=v,minlength=q['ng']); return np.array([(gs==t).any() for t in TT]+[(np.abs(gs-t)<=0.02*t).any() for t in TT[1:]]+[False,False],int)
for nom,st,sh in (('total de quipu (todas las cuerdas)',st_tot_all,boot),('total de quipu (solo colgantes)',st_tot_pen,boot),('total de grupo',st_grp,perm)):
    o,n=run(sh,st,NS)
    for j,nm in enumerate(NM1):
        if nom=='total de grupo' and j>=len(NM1)-2: continue
        add(CAT1,f'{nom} {nm}',o[j],n[:,j].mean(),pemp(o[j],n[:,j]))
print('decimal listo',round(time.time()-t0),flush=True)
def vec(cnt,T,nbs):
    lam=np.mean([cnt[s] for s in nbs]); return cnt[T],lam,stats.poisson.sf(cnt[T]-1,lam)
cnt={s:0 for s in range(3,21)}
for k,q in Q.items():
    sz=np.bincount(q['g'][q['pm']],minlength=q['ng']); sz=sz[sz>0]; cc=pd.Series(sz).value_counts()
    for s in cnt:
        if cc.get(s,0)>=3: cnt[s]+=1
for T,nbs in ((10,[7,8,9,11,12,13]),):
    k,lam,p=vec(cnt,T,nbs); add(CAT1,f'quipus con >=3 grupos de exactamente {T} colgantes (vs vecinos)',k,lam,p,'Poisson sobre vecinos')
print('quipus con >=3 grupos de s colgantes:',cnt)
# ---------- 2. Censo por edad/sexo: clases ordenadas (decrecientes) en grupos de 8-12 colgantes
CAT2='censo por edad/sexo (clases ordenadas)'
def st_edad(q,v):
    out=np.zeros(4,int)
    for gi in range(q['ng']):
        m=(q['g']==gi)&q['pm']; x=v[m]; n=len(x)
        if n<5 or len(set(x))<4 or (x>0).sum()<5: continue
        dec=bool(np.all(np.diff(x)<=0)); inc=bool(np.all(np.diff(x)>=0))
        if 8<=n<=12 and (x>0).sum()>=6: out[0]|=dec; out[1]|=inc
        out[2]|=dec; out[3]|=inc
    return out
o,n=run(perm,st_edad,NS)
for j,nm in enumerate(['decreciente en grupos de 8-12 colgantes','creciente en grupos de 8-12 colgantes','decreciente en grupos >=5 colgantes','creciente en grupos >=5 colgantes']):
    add(CAT2,f'quipus con >=1 grupo {nm}',o[j],n[:,j].mean(),pemp(o[j],n[:,j]))
dd=ii=0; ldec=[]; linc=[]
for k,q in Q.items():
    r=st_edad(q,q['v'])
    if r[2] and not r[3]: dd+=1; ldec.append(k)
    if r[3] and not r[2]: ii+=1; linc.append(k)
add(CAT2,'quipus con solo-decreciente vs solo-creciente (grupos>=5): prueba de signos',dd,(dd+ii)/2,stats.binomtest(dd,dd+ii,0.5,alternative='greater').pvalue,f'dec={dd}, inc={ii}')
print('edad: ejemplos dec',ldec[:15],'inc',linc[:10]); print('edad listo',round(time.time()-t0),flush=True)
# ---------- 3. Depositos/qollqa y cuentas duplicadas
CAT3='depositos/cuentas duplicadas (archivos)'
K=6
def kgrams(seq):
    s=set()
    for i in range(len(seq)-K+1):
        t=tuple(seq[i:i+K])
        if len(set(t))>=3 and sum(t)>=20: s.add(t)
    return s
def pairs_shared(order_fn):
    d=defaultdict(set)
    for k,q in Q.items():
        seq=order_fn(q['v'][q['pm']].astype(int).tolist())
        for t in kgrams(seq): d[t].add(k)
    pr=set()
    for t,ks in d.items():
        if len(ks)>1:
            for a,b in itertools.combinations(sorted(ks),2): pr.add((a,b))
    return pr
obs_pr=pairs_shared(lambda s:s)
nulls=[len(pairs_shared(lambda s:list(rng.permutation(s)))) for _ in range(min(NS,300))]
add(CAT3,f'pares de quipus que comparten {K} colgantes consecutivos con valores no triviales',len(obs_pr),np.mean(nulls),pemp(len(obs_pr),nulls),'unidad: par de quipus; nulo = barajar el orden de los colgantes de cada quipu')
pd.DataFrame(sorted(obs_pr),columns=['quipu_a','quipu_b']).to_csv('pares_secuencia_compartida.csv',index=False)
print('pares compartiendo 6-grama:',len(obs_pr),'nulo',np.mean(nulls),'max nulo',max(nulls))
print('control positivo (Urton 2005; AS114/AS123 no estan en el corpus KFG): AS159-AS173 en lista:',('AS159','AS173') in obs_pr,'| AS194-AS195:',('AS194','AS195') in obs_pr)
prov=defaultdict(list)
for k,q in Q.items():
    if q['prov'] not in ('Unknown','Peru','nan'): prov[q['prov']].append(k)
prov={p:ks for p,ks in prov.items() if len(ks)>=3}
def arch_stats(tot):
    eq=res=r37=0
    for p,ks in prov.items():
        t=np.array([tot[k] for k in ks]); n=len(t); sums=set()
        for i,j in itertools.combinations(range(n),2):
            if t[i]>=20 and t[i]==t[j]: eq+=1
            a,b=max(t[i],t[j]),min(t[i],t[j])
            if b>=20 and (a==3*b or a==7*b): r37+=1
            if t[i]>=20 and t[j]>=20: sums.add(t[i]+t[j])
        res+=sum(1 for x in t if x>=50 and x in sums)
    return np.array([eq,res,r37])
totobs={k:q['v'].sum() for k,q in Q.items()}
o=arch_stats(totobs); nn=np.array([arch_stats({k:boot(q).sum() for k,q in Q.items()}) for _ in range(min(NS,300))])
cats=[CAT3,CAT3,'mitas/tripartición (fracciones del tributo)']
for j,nm in enumerate(['pares con total identico (>=20) en el mismo contexto','quipus cuyo total = suma de otros dos del mismo contexto (resumen)','pares con razon de totales exacta 3 o 7']):
    add(cats[j],nm,o[j],nn[:,j].mean(),pemp(o[j],nn[:,j]),f'{len(prov)} contextos (campo procedencia) con >=3 quipus; no implica origen')
print('archivos listo',round(time.time()-t0),flush=True)
# ---------- 4. Ganado / categorias binarias
CAT4='ganado / categorias binarias (S/Z, R/V)'
def ww_p(lab):
    lab=np.asarray(lab); n1=(lab==lab[0]).sum(); n2=len(lab)-n1
    if n1<4 or n2<4: return None
    R=1+np.sum(lab[1:]!=lab[:-1]); n=n1+n2; mu=2*n1*n2/n+1; sd=np.sqrt(2*n1*n2*(2*n1*n2-n)/(n*n*(n-1)))
    return stats.norm.cdf((R-mu)/sd)
def seg(q,field,vals,lab=None):
    l=q[field] if lab is None else lab
    m=q['pm']&np.isin(l,vals)
    if m.sum()<8: return (0,0)
    p=ww_p(l[m]); return (int(p is not None and p<0.05), int(p is not None))
for field,vals,nom in (('tors',['S','Z'],'torsion S/Z (sexo del ganado en Uhle, Hyland 2014)'),('uni',['R','V'],'union R/V (mitades)')):
    o=np.sum([seg(q,field,vals) for q in Q.values()],axis=0); nl=[]
    for s in range(min(NS,500)):
        t=0
        for q in Q.values():
            l=q[field].copy(); idx=np.flatnonzero(q['pm']&np.isin(q[field],vals)); l[idx]=q[field][rng.permutation(idx)]; t+=seg(q,field,vals,l)[0]
        nl.append(t)
    add(CAT4,f'quipus con segregacion espacial de {nom} (Wald-Wolfowitz p<.05)',o[0],np.mean(nl),pemp(o[0],nl),f'{o[1]} quipus evaluables')
print('segregacion listo',round(time.time()-t0),flush=True)
# ---------- 5. Genealogias / historias / nombres
CAT5='genealogias/historias/nombres (no numericos)'
def ent(a):
    p=pd.Series(a).value_counts(normalize=True).values; return -(p*np.log2(p)).sum()
info=[]
for k,q in Q.items():
    pm=q['pm']; n=pm.sum()
    if n<20: continue
    info.append((k,n,q['nud'][pm].mean(),ent(q['col'][pm]),len(set(q['col'][pm])),q['prov']))
I=pd.DataFrame(info,columns=['kfg','npend','frac_sin_nudo','H_color','n_colores','procedencia']); I['sinnudo']=I.frac_sin_nudo>=0.6
I['bin']=pd.qcut(I.npend,5,labels=False)
obs=I[I.sinnudo].H_color.median()-I[~I.sinnudo].H_color.median(); nl=[]
for s in range(min(NS,2000)):
    lab=I.groupby('bin').sinnudo.transform(lambda x: rng.permutation(x.values)).values.astype(bool); nl.append(I[lab].H_color.median()-I[~lab].H_color.median())
nl=np.array(nl)
add(CAT5,f'diferencia de mediana de entropia de color (>=60% colgantes sin nudo vs resto; {I.sinnudo.sum()}/{len(I)} quipus)',obs,nl.mean(),(1+(np.abs(nl)>=abs(obs)).sum())/(1+len(nl)),'bilateral; permutacion estratificada por tamano; "quipus_obs" = diferencia en bits')
I[I.sinnudo].sort_values('npend',ascending=False).to_csv('quipus_sin_nudos.csv',index=False)
print('sin nudo (>=60% colgantes sin nudo):',I.sinnudo.sum(),'de',len(I),'| H mediana sin nudo %.2f vs resto %.2f'%(I[I.sinnudo].H_color.median(),I[~I.sinnudo].H_color.median()))
# ---------- 6. Calendario / ceques: conteos estructurales
CAT6='calendario/ceques (conteos estructurales)'
ncp=pd.Series({k:int(q['pm'].sum()) for k,q in Q.items()}).value_counts().sort_index()
nct=pd.Series({k:len(q['v']) for k,q in Q.items()}).value_counts().sort_index()
ngr=pd.Series({k:q['ng'] for k,q in Q.items()}).value_counts().sort_index()
for ser,nom,T in ((ncp,'colgantes',[328,360,365,354,355,730]),(nct,'cuerdas totales',[328,360,365,354,355,730]),(ngr,'grupos',[41,12,24])):
    for t in T:
        nb=[ser.get(t+d,0) for d in range(-5,6) if d!=0]; lam=np.mean(nb); k=int(ser.get(t,0))
        add(CAT6,f'quipus con exactamente {t} {nom} (vs vecinos +-5)',k,lam,stats.poisson.sf(k-1,max(lam,1e-9)),'Poisson sobre vecinos')
        if k:
            f={'colgantes':lambda q:int(q['pm'].sum()),'cuerdas totales':lambda q:len(q['v']),'grupos':lambda q:q['ng']}[nom]
            print('   ',nom,t,'->',[kk for kk,q in Q.items() if f(q)==t][:8])
# ---------- 7. Nivel individual: rachas de color de 6 (Hyland 2016 / Santa)
CAT7='nivel individual (grupos de color de 6, tipo Santa)'
cr={s:0 for s in range(3,11)}
for k,q in Q.items():
    cl=q['col'][q['pm']]; runs=[]; i=0
    while i<len(cl):
        j=i
        while j+1<len(cl) and cl[j+1]==cl[i] and cl[i]!='NA': j+=1
        runs.append(j-i+1); i=j+1
    rc=pd.Series(runs).value_counts()
    for s in cr:
        if rc.get(s,0)>=3: cr[s]+=1
k,lam,p=vec(cr,6,[4,5,7,8]); add(CAT7,'quipus con >=3 rachas de color de exactamente 6 colgantes (vs 4,5,7,8)',k,lam,p,'Poisson sobre vecinos')
print('quipus con >=3 rachas de color de longitud s:',cr)
R=pd.DataFrame(rows)
def holm(p):
    p=np.asarray(p); o=np.argsort(p); m=len(p); adj=np.empty(m); run_=0
    for i,ix in enumerate(o): run_=max(run_,(m-i)*p[ix]); adj[ix]=min(1,run_)
    return adj
def bh(p):
    p=np.asarray(p); m=len(p); o=np.argsort(p); q=np.empty(m); prev=1
    for i in range(m-1,-1,-1): prev=min(prev,p[o[i]]*m/(i+1)); q[o[i]]=prev
    return q
R['p_holm']=holm(R.p); R['q_bh']=bh(R.p); R['n_pruebas']=len(R)
R.to_csv('firmas_resultados.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',100)
print('n pruebas',len(R)); print(R.sort_values('p').head(30)[['categoria','firma','quipus_obs','nulo_media','p','p_holm','q_bh']].round(4).to_string())
