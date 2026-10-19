import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score as ari
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from scipy.optimize import linear_sum_assignment
rng=np.random.default_rng(31); out=[]
def pr(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
P=pd.read_csv('perfiles.csv')
F=['frac_cero','frac_vacio','log_med','log_rango','var_media','red10','red5','ben_dist','ndig_medio',
   'n_cuerdas','n_grupos','tam_grupo','cv_grupo','subs_por_colg','n_colores','bandas_grupo','nmi_color_grupo','frac_Z','largo_med']
LOG=['n_cuerdas','n_grupos','tam_grupo','var_media']
X=P[F].copy()
for l in LOG: X[l]=np.log1p(X[l])
X=X.fillna(X.median())          # ponytail: imputacion por mediana
Z=StandardScaler().fit_transform(X)
fr=P.frontera.values==1
Zf=Z[fr]; n=len(Zf)
pr('frontera n =',n)
# ---- 2a agrupamiento
def km(Z,k,seed=0): return KMeans(k,n_init=10,random_state=seed).fit(Z)
def nulo(Z): return rng.multivariate_normal(Z.mean(0),np.cov(Z.T),len(Z))  # nulo: una nube gaussiana con la misma covarianza (un solo genero continuo)
res=[]
for k in range(2,8):
    s=silhouette_score(Zf,km(Zf,k).labels_)
    ns=[silhouette_score(N,km(N,k).labels_) for N in (nulo(Zf) for _ in range(100))]
    res.append((k,s,np.mean(ns),np.percentile(ns,95),(np.sum(np.array(ns)>=s)+1)/101))
R=pd.DataFrame(res,columns=['k','sil','nulo_media','nulo_p95','p']); pr(R.round(3).to_string(index=False))
# estabilidad bootstrap + estabilidad por quipu
def boot(Z,k,B=100):
    ref=km(Z,k); aris=[]; agree=np.zeros(len(Z))
    for b in range(B):
        i=rng.integers(0,len(Z),len(Z)); m=KMeans(k,n_init=5,random_state=b).fit(Z[i])
        lab=m.predict(Z); aris.append(ari(ref.labels_,lab))
        C=np.array([[np.sum((ref.labels_==a)&(lab==c)) for c in range(k)] for a in range(k)])
        r,cc=linear_sum_assignment(-C); mp=dict(zip(cc,r)); agree+=np.array([mp[x] for x in lab])==ref.labels_
    return ref.labels_,np.mean(aris),np.percentile(aris,[2.5,97.5]),agree/B
for k in (2,3,4,5):
    _,a,ci,_=boot(Zf,k,60); pr(f'k={k} bootstrap ARI medio {a:.2f} IC {ci.round(2)}')
ok=R[R.p<.05]; K=int(ok.loc[ok.sil.idxmax(),'k']) if len(ok) else 2; pr('k elegido (max silueta) =',K)
lab,a,ci,stab=boot(Zf,K,200); pr(f'k={K}: ARI {a:.2f} {ci.round(2)}; estabilidad por quipu mediana {np.median(stab):.2f}; >=0.7: {(stab>=.7).sum()}')
# ---- 2b clasificador
tr=(~fr)&P.confianza.isin(['alta','media']).values&(P.genero!='SIN').values
vc=P[tr].genero.value_counts(); keep=vc[vc>=6].index; tr&=P.genero.isin(keep).values
pr('entrenamiento',dict(P[tr].genero.value_counts()),'(descartados <6: ',[g for g in vc.index if g not in keep],')')
y=P.genero[tr].values; rf=RandomForestClassifier(500,min_samples_leaf=2,class_weight='balanced',random_state=0)
cv=StratifiedKFold(5,shuffle=True,random_state=0)
pp=cross_val_predict(rf,Z[tr],y,cv=cv,method='predict_proba'); cls=np.unique(y); pred=cls[pp.argmax(1)]
from sklearn.metrics import balanced_accuracy_score
acc=(pred==y).mean(); bacc=balanced_accuracy_score(y,pred); base=vc[keep].max()/vc[keep].sum()
perm=[balanced_accuracy_score(rng.permutation(y),pred) for _ in range(500)]
pr(f'CV 5-fold: exactitud {acc:.3f}, balanceada {bacc:.3f}; base mayoritaria {base:.3f}; balanceada con etiquetas barajadas {np.mean(perm):.3f} (p95 {np.percentile(perm,95):.3f})')
pr('por clase (recall):',{c:round(float((pred[y==c]==c).mean()),2) for c in cls})
hi=pp.max(1)>=.7; pr(f'en CV, prob>=0.7: {hi.mean():.2f} de casos, precision {(pred[hi]==y[hi]).mean():.2f}')
rf.fit(Z[tr],y); pf=rf.predict_proba(Zf)
# ---- 3 firmas rosetta
T=pd.read_csv('../11_rosetta/transcripciones_numeros.csv',encoding='utf-8',encoding_errors='replace')
T=T[T.papel=='item']; T['v']=pd.to_numeric(T.valor,errors='coerce'); T=T[T.v>0]
def cat(g):
    g=str(g)
    if 'servicio' in g: return 'servicio/asignación'
    if 'padr' in g or 'summ' in g or 'elicit' in g: return 'padrón/recuento'
    if 'serie' in g: return 'tributo (serie)'
    return 'pnum otros'
T['cl']=T.genero.apply(cat)
BEN=np.log10(1+1/np.arange(1,10))
def firma(v):
    v=np.asarray(v); b=v[v>=10]; d=np.array([int(str(int(x))[0]) for x in v])
    return dict(n=len(v),red10=round((b%10==0).mean(),2) if len(b) else np.nan,log_med=round(np.log10(np.median(v)),2),
                ben_dist=round(np.abs(np.bincount(d,minlength=10)[1:]/len(d)-BEN).sum(),2))
rows=[(c,)+tuple(firma(g.v).values()) for c,g in T.groupby('cl')]
pr('\nFirmas documentales (items rosetta):'); pr(pd.DataFrame(rows,columns=['clase','n','red10','log_med','ben_dist']).to_string(index=False))
# ---- salida
P['_i']=range(len(P)); F0=P[fr].copy(); F0['cluster']=lab; F0['estab_cluster']=stab.round(3)
for j,c in enumerate(rf.classes_): F0['p_'+c]=pf[:,j].round(3)
F0['mejor_genero']=rf.classes_[pf.argmax(1)]; F0['p_mejor']=pf.max(1).round(3)
F0['asigna']=np.where(F0.p_mejor>=.7,'existente:'+F0.mejor_genero,'')
cs=F0.groupby('cluster').agg(n=('kfg','size'),n_cuerdas=('n_cuerdas','median'),red10=('red10','median'),red5=('red5','median'),log_med=('log_med','median'),
  ben=('ben_dist','median'),var_media=('var_media','median'),n_grupos=('n_grupos','median'),subs=('subs_por_colg','median'),n_colores=('n_colores','median'),
  nmi=('nmi_color_grupo','median'),estab=('estab_cluster','mean'),p_mejor=('p_mejor','mean'),top=('mejor_genero',lambda s:s.value_counts().index[0]))
pr('\nClusters de la frontera:'); pr(cs.round(2).to_string())
pr('\nProcedencia por cluster (top 3):')
for c,g in F0.groupby('cluster'): pr(c,dict(g.procedencia.value_counts().head(3)))
# nuevo genero: cluster estable (estab media>=.7) y p_mejor medio <0.5 y quipu estab>=.7
nuevo_c=[c for c,r in cs.iterrows() if r.estab>=.7 and r.p_mejor<.5 and len(ok)>0 and R.sil.max()>=.25]  # Kaufman-Rousseeuw: sil<0.25 = sin estructura sustancial
F0['asigna']=np.where(F0.asigna!='',F0.asigna,np.where(F0.cluster.isin(nuevo_c)&(F0.estab_cluster>=.7),'nuevo:cluster'+F0.cluster.astype(str),''))
pr('\nclusters candidatos a genero nuevo:',nuevo_c)
pr('asignables prob>=0.7 a existente:',(F0.asigna.str.startswith('existente')).sum(),'; a nuevo:',(F0.asigna.str.startswith('nuevo')).sum(),'; total',(F0.asigna!='').sum(),'de',n)
pr('existentes:',dict(F0.asigna[F0.asigna.str.startswith('exist')].value_counts()))
pr('mejor genero (argmax) de los 180:',dict(F0.mejor_genero.value_counts()))
F0.drop(columns=['_i','frontera','evidencia']).to_csv('asignacion_frontera.csv',index=False)
open('salida_analisis.txt','w',encoding='utf-8').write('\n'.join(out))

print('red10 NaN en frontera:',F0.red10.isna().sum(),'; p_mejor>=.5:',(F0.p_mejor>=.5).sum(),'; >=.6:',(F0.p_mejor>=.6).sum(),'; max',F0.p_mejor.max())
