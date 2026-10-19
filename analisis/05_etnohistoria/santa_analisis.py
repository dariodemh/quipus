"""Valle del Santa: replica y control de Medrano & Urton 2018 / FitzPatrick 2024. Semilla fija."""
import numpy as np, pandas as pd, itertools, re
from santa_grupos import grupos_seis, IDS
rng=np.random.default_rng(20261017)
G=grupos_seis(); G['u1']=G.unions.str[0]; G['v1']=G.vals.str[0]
print('== 1. Replica de conteos'); print(G.groupby('kh').size().to_dict(),len(G))
print(G.groupby('u1').size().to_dict(),'(publicado 63 R / 70 V; KFG: 1 grupo de UR090 y 1 U en UR092 difieren)')
c=pd.read_csv('./analisis/datos/cuerdas.csv',low_memory=False)
s=c[c.kfg.isin(IDS)&c.union.isin(['R','V'])]; print('cuerdas R/V (todas):',s.union.value_counts().to_dict(),'-> %.1f%% R'%(100*(s.union=='R').mean()))
# ---- 2. tributo: suma de la cuerda 1 vs 367
cols=[sum(v[p] for v in G.vals) for p in range(6)]
print('\n== 2. Sumas por posicion dentro del grupo',cols)
print('suma 1.a cuerda =',G.v1.sum(),'; sin el grupo U =',G[G.u1!='U'].v1.sum(),'; R:',G[G.u1=='R'].v1.sum(),'V:',G[G.u1=='V'].v1.sum(),'U:',G[G.u1=='U'].v1.sum())
obs=min(abs(cols[0]-367),0); d_obs=abs(G.v1.sum()-367)
def p_target(lo,hi,logscale,n=200000,tol=d_obs):
    T=np.exp(rng.uniform(np.log(lo),np.log(hi),n)) if logscale else rng.uniform(lo,hi,n)
    T=np.round(T)
    best=np.min(np.abs(np.array(cols)[None,:]-T[:,None]),axis=1)
    return (best<=tol).mean()
print('Prob. de que un objetivo ARBITRARIO (tributo total) caiga a <=%d de alguna de las 6 sumas-columna:'%d_obs)
for lo,hi in [(100,1000),(100,5000)]:
    print('  objetivo U(%d,%d): %.4f ; log-uniforme: %.4f'%(lo,hi,p_target(lo,hi,False),p_target(lo,hi,True)))
# ---- 3. alineaciones de moieties
P={'Namus':18,'Corongo':23,'Cuyuchin':9,'Cusca':7,'Guauyan':41,'Ucore':32}; names=list(P); tot=sum(P.values()); NV,NR=70,63
def err(S,V=NV,N=133): return abs(S-V)+abs((tot-S)-(N-V))
rows=[]
for T in itertools.combinations(names,3):
    S=sum(P[t] for t in T); rows.append((' '.join(T),S,tot-S,err(S)))
A=pd.DataFrame(rows,columns=['verso','S_verso','S_recto','error']).sort_values('error').reset_index(drop=True)
A['p_publicado']=(A.error+1)/134
print('\n== 3. 20 alineaciones (verso = triple)'); print(A.to_string())
pub=[0.02985,0.04478,0.04478,0.07463,0.07463,0.07463,0.10448,0.14925,0.17910,0.17910,0.17910,0.20896,0.20896,0.28358,0.31343,0.31343,0.34328,0.41791,0.44776,0.52239]
print('p publicado (Tabla 3 de FitzPatrick) = (error+1)/134 en las 20 filas:',np.allclose(A.p_publicado,pub,atol=6e-6))
print('  -> equivale a asumir que el recuento de verso es UNIFORME en 0..133 (134 valores): null no realista.')
def best(V,N=133,sums=A.S_verso.values): return min(err(S,V,N) for S in sums)
# nulo a) V binomial / uniforme
Vb=rng.binomial(133,0.5,200000); bb=np.array([best(v) for v in range(134)])
pb=np.mean(bb[Vb]<=3); pu=np.mean(bb<=3)
print('\nNulo a) mejor error sobre las 20 alineaciones, V ~ Binomial(133,.5): P(<=3)=%.3f  P(<=5)=%.3f ; V uniforme 0..133: P(<=3)=%.3f'%(pb,np.mean(bb[Vb]<=5),pu))
print('  rango V 45..90: P(mejor error<=3)=%.3f, <=5: %.3f'%(np.mean(bb[45:91]<=3),np.mean(bb[45:91]<=5)))
# nulo b) bloques: cada quipu entero R o V (UR090 fijo 5R/12V)
atoms={'UR087':48,'UR088':9,'UR089':34,'UR091':15,'UR092':10}
res=[]
for m in itertools.product([0,1],repeat=5):  # 1=verso
    V=12+sum(a for a,b in zip(atoms.values(),m) if b); res.append((V,best(V)))
res=pd.DataFrame(res,columns=['V','best']); print('Nulo b) 32 asignaciones R/V por quipu entero (UR090 fijo): V distintos=%d, con mejor error<=3: %d/32, <=5: %d/32'%(res.V.nunique(),(res.best<=3).sum(),(res.best<=5).sum()))
print('  asignacion observada: V=70 ->',best(70)); print(res.sort_values('V').T.to_string())
# nulo c) tamanos de pachaca aleatorios (composiciones de 130 en 6 partes), V=70 fijo
def comp(n=130,k=6):
    cuts=np.sort(rng.choice(np.arange(1,n),k-1,replace=False)); return np.diff(np.r_[0,cuts,n])
def bestsizes(sz):
    return min(err(sum(t),70) for t in itertools.combinations(sz,3))
N=20000; e1=np.array([bestsizes(comp()) for _ in range(N)])
e2=np.array([bestsizes(np.maximum(1,np.round(130*rng.dirichlet(np.full(6,2.0)))).astype(int)) for _ in range(N)])  # (suma ~130)
print('Nulo c) tamanos al azar (composiciones uniformes) con V=70 fijo: P(mejor<=3)=%.3f  P(<=5)=%.3f  | Dirichlet(2): P(<=3)=%.3f P(<=5)=%.3f'%((e1<=3).mean(),(e1<=5).mean(),(e2<=3).mean(),(e2<=5).mean()))
# nulo d) ambos: composiciones al azar y V binomial
e3=np.array([min(err(sum(t),v) for t in itertools.combinations(comp(),3)) for v in rng.binomial(133,0.5,N)])
print('Nulo d) tamanos al azar + V binomial: P(<=3)=%.3f P(<=5)=%.3f'%((e3<=3).mean(),(e3<=5).mean()))
print('Errores posibles para V=70 (con sumas 68 y 71): FitzPatrick err=3 (S=68), Medrano-Urton err=5 (S=71): el unico valor que alcanza 3 es S in [67,70]; solo S=68 existe')
# ---- 4. colores unicos
col=G.colors.str[0].fillna('NA').str.replace(r'\([^)]*\)','',regex=True); print('\n== 4. colores distintos (cuerda 1) en 133 grupos:',col.nunique(),'| por quipu',G.assign(c=col).groupby('kh').c.nunique().to_dict())
# nulo: barajar colores entre grupos no cambia el recuento; el recuento esta fijado por la seriacion.
# ---- 5. quipus tipo Santa en el corpus
allc=c[c.nivel==0].copy(); allc['n']=allc.cuerda.str[1:].astype(int); out=[]
for k,x in allc.groupby('kfg'):
    x=x.sort_values('n'); cl=x.color.fillna('NA').tolist(); un=x.union.tolist(); i=0;b=0;ids=[]
    while i+6<=len(cl):
        if cl[i]!='NA' and len(set(cl[i:i+6]))==1 and (i+6>=len(cl) or cl[i+6]!=cl[i]) and (i==0 or cl[i-1]!=cl[i]):
            b+=1; ids.append(un[i]); i+=6
        else: i+=1
    out.append((k,len(cl),b,''.join(ids)))
S6=pd.DataFrame(out,columns=['kfg','npend','bloques6','ident_union']).sort_values('bloques6',ascending=False)
print('\n== 5. quipus con bloques de 6 cuerdas del mismo color (>=8 bloques):'); print(S6[S6.bloques6>=8].head(25).to_string())
S6.to_csv('santa_bloques6_corpus.csv',index=False)
G.drop(columns=['vals','unions','colors']).to_csv('santa_grupos6.csv',index=False)
A.to_csv('santa_alineaciones.csv',index=False)
