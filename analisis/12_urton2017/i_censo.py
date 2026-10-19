# Selectividad del criterio "censo-like" de Urton (cap. 10): valores en 1-7, mas 1-4 que 5-7
from util import *
from scipy import stats
rows=[]
for k,d in C.groupby('kfg'):
    v=d[(d.valor>0)].valor.values  # todas las cuerdas con valor (pendientes+subs)
    if len(v)<15: continue
    f17=np.mean((v>=1)&(v<=7)); f14=np.mean((v>=1)&(v<=4)); f57=np.mean((v>=5)&(v<=7))
    rows.append((k,len(v),f17,f14,f57))
R=pd.DataFrame(rows,columns=['kfg','n','f1_7','f1_4','f5_7'])
crit=(R.f1_7>=0.90)&(R.f1_4>R.f5_7)
print('quipus con >=15 cuerdas con valor:',len(R),' censo-like (>=90% en 1-7 y 1-4>5-7):',crit.sum())
print(R[R.kfg.isin(['UR023','UR028','UR029','UR006','UR009','UR021'])])
print('listado:',R[crit].kfg.tolist()[:80])
# prueba chi-cuadrado vs exemplar aproximado de visitas (1..7), como Brezine
ex=np.array([.22,.28,.20,.14,.08,.05,.03]); ex/=ex.sum()
pas=[]
for k,d in C.groupby('kfg'):
    v=d[(d.valor>=1)&(d.valor<=7)].valor.values.astype(int)
    if len(v)<15: continue
    o=np.bincount(v,minlength=8)[1:8]; 
    # misma aprox que Urton: porcentajes; se usa chi2 sobre conteos esperados
    e=ex*o.sum()
    # agrupar celdas con esperado<5
    ch,p=stats.chisquare(o,e); pas.append((k,p, (d.valor>7).mean()))
P=pd.DataFrame(pas,columns=['kfg','p','frac_gt7'])
print('con chi2 vs exemplar (valores 1-7): p>0.05 en',(P.p>0.05).sum(),'de',len(P),'quipus')
print(P[P.kfg.isin(['UR023','UR028','UR029'])])
R.to_csv('censo_like_criterio.csv',index=False)
