"""Perfiles por quipu (valores, estructura, contexto) -> perfiles.csv"""
import re, numpy as np, pandas as pd
from sklearn.metrics import normalized_mutual_info_score as nmi
A='..'
c=pd.read_csv(f'{A}/datos/cuerdas.csv'); q=pd.read_csv(f'{A}/datos/quipus.csv')
atl=pd.read_csv(f'{A}/28_atlas_generos/atlas.csv')
BEN=np.log10(1+1/np.arange(1,10))
def fd(v):
    return np.array([int(str(int(x))[0]) for x in v])
rows=[]
for k,g in c.groupby('kfg'):
    p=g[g.nivel==0]; v=p.valor.fillna(0).values; pos=v[v>0]
    r=dict(kfg=k,n_cuerdas=len(p))
    r['frac_cero']=(v==0).mean(); r['frac_vacio']=p.nudos.isna().mean()
    if len(pos)>=3:
        r['log_med']=np.log10(np.median(pos)); r['log_rango']=np.log10(np.percentile(pos,95)/np.percentile(pos,5)) if len(pos)>=5 else np.nan
        r['var_media']=pos.var()/pos.mean()
        big=pos[pos>=10]; r['n_ge10']=len(big)
        r['red10']=(big%10==0).mean() if len(big)>=3 else np.nan
        b5=pos[pos>=5]; r['red5']=(b5%5==0).mean() if len(b5)>=3 else np.nan
        d=fd(pos); f=np.bincount(d,minlength=10)[1:]/len(d)
        r['ben_dist']=np.abs(f-BEN).sum(); r['frac_d1']=f[0]
    else: r.update(log_med=np.nan,log_rango=np.nan,var_media=np.nan,n_ge10=0,red10=np.nan,red5=np.nan,ben_dist=np.nan,frac_d1=np.nan)
    ncl=p.nudos.fillna('').apply(lambda s:len([x for x in s.split(';') if x]))
    r['ndig_medio']=ncl[ncl>0].mean() if (ncl>0).any() else np.nan
    gs=p.groupby('grupo').size(); r['n_grupos']=len(gs); r['tam_grupo']=gs.mean(); r['cv_grupo']=gs.std()/gs.mean() if len(gs)>1 else 0
    r['subs_por_colg']=(g.nivel>0).sum()/len(p)
    col=g.color.fillna('NA').apply(lambda s:re.sub(r'\([^)]*\)','',s))
    r['n_colores']=col.nunique()
    pc=col[g.nivel==0]
    r['bandas_grupo']=pc.groupby(p.grupo).nunique().mean()
    r['nmi_color_grupo']=nmi(p.grupo,pc) if len(gs)>1 and pc.nunique()>1 else 0
    t=g.torsion[g.torsion.isin(['S','Z'])]; r['frac_Z']=(t=='Z').mean() if len(t) else np.nan
    lg=p.largo.dropna(); r['largo_med']=lg.median() if len(lg) else np.nan
    rows.append(r)
P=pd.DataFrame(rows).merge(atl[['kfg','procedencia','museo','genero','confianza','evidencia']],on='kfg')
P['frontera']=(P.evidencia.str.startswith('decimal sin estructura')).astype(int)
P.to_csv('perfiles.csv',index=False)
print(P.frontera.sum(),P.shape)
print(P.groupby(['frontera']).median(numeric_only=True).T)
