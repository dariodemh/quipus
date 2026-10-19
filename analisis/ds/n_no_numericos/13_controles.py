"""Caracterizacion final + controles (tamano, prefijo, region)."""
import pandas as pd, numpy as np
from scipy import stats
import statsmodels.formula.api as smf
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
Q['clase3']=np.select([Q.ND,Q.NC,Q.NU],['ND','NC','NU'],'resto')
# primario: clase limpia vs resto limpio
Q['prim']=np.where(Q.flag_tx,np.nan,Q.clase.astype(float))
Q['logN']=np.log1p(Q.ncuerdas)
Q['tiene_canuto']=Q.num_canuto_cords.fillna(0)>0
Q['tiene_CL']=Q.f_CL.fillna(0)>0.001
Q['n_top_any']=Q.n_top.fillna(0)>0
Q['banded']=Q.num_banded_clusters.fillna(0)>0
Q['seriated']=Q.num_seriated_clusters.fillna(0)>0
Q['proc']=Q.procedencia.fillna('Unknown').replace({'unknown':'Unknown'})
def cat(s):
    s=str(s).lower()
    if 'unknown' in s: return 'Unknown'
    if 'pachacamac' in s: return 'Pachacamac'
    if 'incahuasi' in s: return 'Incahuasi'
    if 'armatambo' in s: return 'Armatambo'
    if 'leymebamba' in s or 'chachapoyas' in s: return 'Leymebamba'
    if 'ica' in s or 'pisco' in s or 'ocucaje' in s or 'callango' in s: return 'Ica/Pisco'
    if 'nazca' in s or 'paracas' in s: return 'Nazca/Paracas'
    if 'lima' in s or 'huacho' in s or 'chancay' in s or 'huaquerones' in s: return 'Lima/Huacho'
    if 'arica' in s or 'lluta' in s or 'chile' in s: return 'N Chile'
    return 'Other'
Q['procc']=Q.proc.map(cat)

num=['ncuerdas','ncuerdas_nudo','nclusters','frac_rico','n_color','frac_subs','frac_topd','f_CL','num_canuto_cords','num_ascher_colors','num_banded_clusters','num_seriated_clusters','frac_sin_nudo','n_multi','benford_match','n_pend','V1_c','Hn_c','mi_pat','mi_val']
rows=[]
for v in num:
    if v not in Q: continue
    a=Q[Q.clase_limpia][v].dropna(); b=Q[(~Q.clase)&~Q.flag_tx][v].dropna()
    if len(a)<3 or len(b)<3: continue
    u,p=stats.mannwhitneyu(a,b,alternative='two-sided')
    rows.append(dict(var=v,n_clase=len(a),med_clase=a.median(),n_resto=len(b),med_resto=b.median(),p=p,
                     delta=(a.median()-b.median())))
R=pd.DataFrame(rows); ok=R.p.notna(); R['q']=np.nan
R.loc[ok,'q']=stats.false_discovery_control(R.loc[ok,'p'],method='bh')
R['sig']=np.where(R.q<0.05,'*','')
print('== Numericas (clase limpia vs resto limpio) ==')
print(R.sort_values('p').round(4).to_string(index=False))

rows=[]
for v in ['tiene_canuto','tiene_CL','n_top_any','banded','seriated']:
    a=Q[Q.clase_limpia][v].dropna(); b=Q[(~Q.clase)&~Q.flag_tx][v].dropna()
    t=[[a.sum(),len(a)-a.sum()],[b.sum(),len(b)-b.sum()]]
    orr,p=stats.fisher_exact(t)
    rows.append(dict(var=v,prop_clase=a.mean(),n_clase=len(a),prop_resto=b.mean(),n_resto=len(b),OR=orr,p=p))
R2=pd.DataFrame(rows); R2['q']=stats.false_discovery_control(R2.p,method='bh')
print('\n== Binarias ==')
print(R2.round(4).to_string(index=False))

print('\n== Logit canuto ~ clase + logN + prefijo ==')
d=Q.dropna(subset=['prim']).copy().rename(columns={'C':'Cconv'})
d['tiene_canuto']=d['tiene_canuto'].astype(int); d['tiene_CL']=d['tiene_CL'].astype(int)
m=smf.logit('tiene_canuto ~ prim + logN + C(pref)',data=d).fit(disp=0)
print(m.summary2().tables[1].round(4).to_string())
print('\n== Logit CL ~ clase + logN (solo UR) ==')
d2=d[d.pref=='UR'].copy()
try:
    m2=smf.logit('tiene_CL ~ prim + logN',data=d2).fit(disp=0)
    print(m2.summary2().tables[1].round(4).to_string())
except Exception as e: print(e)
print('\n== OLS frac_rico ~ clase + logN + prefijo ==')
m3=smf.ols('frac_rico ~ prim + logN + C(pref)',data=d).fit()
print(m3.summary2().tables[1].round(4).to_string())

print('\n== Procedencia ==')
known=Q[(Q.procc!='Unknown')&(~Q.flag_tx)]
print((known.groupby('procc').clase.agg(['size','sum','mean']).sort_values('mean',ascending=False)).round(3).to_string())
ct=pd.crosstab(known.procc,known.clase)
chi2,p,dof,exp=stats.chi2_contingency(ct); print('chi2',round(chi2,2),'dof',dof,'p',round(p,4))
# ND vs resto known
print('\nND rate known:'); print((known.groupby('procc').ND.agg(['size','sum','mean']).sort_values('mean',ascending=False)).round(3).to_string())
chi2,p,dof,exp=stats.chi2_contingency(pd.crosstab(known.procc,known.ND)); print('ND chi2',round(chi2,2),'p',round(p,4))
Q.to_csv('analisis/ds/n_no_numericos/quipus_clase.csv',index=False)
R.to_csv('analisis/ds/n_no_numericos/tests_caracterizacion.csv',index=False)
R2.to_csv('analisis/ds/n_no_numericos/tests_binarias.csv',index=False)
