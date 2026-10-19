"""Caracterizacion de la clase no numerica + R_diff (color en cuerdas sin nudo)."""
import pandas as pd, numpy as np
from scipy import stats
RNG=np.random.default_rng(20261018)
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_indice.csv')
N=pd.read_csv('analisis/ds/n_no_numericos/nulo_resumen.csv')
C=pd.read_csv('analisis/ds/n_no_numericos/cuerdas_anom.csv')
S=pd.read_csv('data/external/data-science-khipu-article/data/khipu_summary.csv')

# R_diff por quipu + p permutacion
rows=[]
for q,d in C.groupby('kfg'):
    kn=d.knotless.values.astype(bool); rich=d.rich_color.values.astype(bool)
    nk=kn.sum(); nkn=(~kn).sum()
    if nk==0 or nkn==0:
        rows.append((q,np.nan,np.nan,nk,nkn)); continue
    obs=rich[kn].mean()-rich[~kn].mean()
    B=2000; cnt=0
    for b in range(B):
        rp=RNG.permutation(rich)
        v=rp[kn].mean()-rp[~kn].mean()
        if v>=obs: cnt+=1
    rows.append((q,obs,(1+cnt)/(B+1),nk,nkn))
RD=pd.DataFrame(rows,columns=['kfg','Rdiff','Rdiff_p','n_knotless','n_knotted'])
Q=Q.merge(RD,on='kfg',how='left').merge(N[['kfg','p_hi','z','score_obs','D_null','I_null','Q_null']],on='kfg',how='left')

# metadatos externos
S=S.rename(columns={'kfg_name':'kfg'})
cols=['kfg','num_ascher_colors','num_canuto_cords','num_top_cords','num_subsidiary_cords','num_banded_clusters','num_seriated_clusters','num_decreasing_clusters','benford_match','mean_cord_value','percent_s_knots']
Q=Q.merge(S[cols].drop_duplicates('kfg'),on='kfg',how='left')
# fibra OKR
import sqlite3
con=sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
km=pd.read_sql('select KHIPU_ID,OKR_NUM,INVESTIGATOR_NUM from khipu_main',con)
fib=pd.read_sql('select KHIPU_ID,FIBER,count(*) n from cord group by 1,2',con)
fibp=fib.pivot_table(index='KHIPU_ID',columns='FIBER',values='n',fill_value=0)
fibp['tot']=fibp.sum(axis=1)
for c in ['CL','CN','AH','W','H','V','CC']:
    if c in fibp: fibp['f_'+c]=fibp[c]/fibp.tot
km=km.merge(fibp[[c for c in fibp.columns if c.startswith('f_')]],left_on='KHIPU_ID',right_index=True,how='left')
mp={}
for r in km.itertuples():
    for key in [r.OKR_NUM,r.INVESTIGATOR_NUM]:
        if isinstance(key,str): mp[key]=r
def getf(q):
    r=mp.get(q)
    if r is None: return pd.Series(dtype=float)
    return pd.Series({'f_CL':getattr(r,'f_CL',np.nan),'f_CN':getattr(r,'f_CN',np.nan),'f_AH':getattr(r,'f_AH',np.nan)})
Q=Q.merge(pd.DataFrame([dict(kfg=q,**getf(q).to_dict()) for q in Q.kfg]),on='kfg',how='left')

# clase
Q['ND']=(Q.n_multi>=5)&((Q.Q>=0.5)|(Q.I>=0.10)|(Q.D>=0.80))
Q['NC']=(Q.n_knotless>=5)&(Q.n_knotted>=5)&(Q.Rdiff>=0.3)&(Q.Rdiff_p<0.05)
Q['NU']=(Q.Z>=0.10)&(Q.ncuerdas>=8)
Q['clase']=Q.ND|Q.NC|Q.NU
Q['pref']=Q.kfg.str.extract(r'^([A-Z]+)')
Q.to_csv('analisis/ds/n_no_numericos/quipus_clase.csv',index=False)
print('clase ND',Q.ND.sum(),'NC',Q.NC.sum(),'NU',Q.NU.sum(),'union',Q.clase.sum(),'de',len(Q))
print('\nND por prefijo'); print(pd.crosstab(Q.pref,Q.ND).T.to_string())
print('\nNC (Rdiff>=.3,p<.05):'); print(Q[Q.NC].sort_values('Rdiff',ascending=False)[['kfg','ncuerdas','n_knotless','n_knotted','Rdiff','Rdiff_p','frac_rico','procedencia']].head(25).round(3).to_string(index=False))
print('\nNU:'); print(Q[Q.NU].sort_values('Z',ascending=False)[['kfg','ncuerdas','n_imposible','Z','n_knotless','procedencia']].head(15).round(3).to_string(index=False))
print('\nND top:'); print(Q[Q.ND].sort_values('Q',ascending=False)[['kfg','ncuerdas_nudo','n_multi','D','I','Q','Rdiff','NC','procedencia']].head(30).round(2).to_string(index=False))
