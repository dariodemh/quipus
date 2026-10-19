"""Caracterizacion de la clase frente al resto. Tests por quipu + BH."""
import pandas as pd, numpy as np
from scipy import stats
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
Q['grupo']=np.where(Q.ND,'ND',np.where(Q.NC,'NC',np.where(Q.NU,'NU','resto')))
Q['clase3']=np.select([Q.ND,Q.NC,Q.NU],['ND','NC','NU'],'resto')

def mw(a,b):
    a=pd.Series(a).dropna(); b=pd.Series(b).dropna()
    if len(a)<3 or len(b)<3: return np.nan,np.nan,len(a),len(b),np.nan
    u,p=stats.mannwhitneyu(a,b,alternative='two-sided')
    # r effect size
    r=1-2*u/(len(a)*len(b))
    return a.median(),b.median(),len(a),len(b),p
def fish(a,b):
    a=pd.Series(a).dropna().astype(bool); b=pd.Series(b).dropna().astype(bool)
    if len(a)<2 or len(b)<2: return np.nan,np.nan,np.nan
    t=[[a.sum(),len(a)-a.sum()],[b.sum(),len(b)-b.sum()]]
    orr,p=stats.fisher_exact(t)
    return a.mean(),b.mean(),p
rows=[]
num=['ncuerdas','ncuerdas_nudo','nclusters','frac_rico','n_color','frac_subs','frac_topd','f_CL','num_canuto_cords','num_ascher_colors','num_banded_clusters','num_seriated_clusters','num_decreasing_clusters','frac_sin_nudo','n_multi','benford_match']
for v in num:
    if v not in Q: continue
    for g in ['ND','NC','NU']:
        a=Q[Q.clase3==g][v]; b=Q[Q.clase3=='resto'][v]
        ma,mb,na,nb,p=mw(a,b)
        rows.append(dict(var=v,grupo=g,n=na,med_clase=ma,med_resto=mb,p=p))
R=pd.DataFrame(rows)
# BH por familia (todos los tests)
R['q']=np.nan
ok=R.p.notna()
R.loc[ok,'q']=stats.false_discovery_control(R.loc[ok,'p'],method='bh')
print('== Numericas (medianas) ==')
print(R[R.p<0.1].sort_values(['var','grupo']).round(4).to_string(index=False))

# binarias
rows=[]
for v in ['ND','NC','NU']:
    pass
for v in ['n_top_any','tiene_canuto','tiene_CL','alguna_serie']:
    pass
Q['tiene_canuto']=Q.num_canuto_cords.fillna(0)>0
Q['tiene_CL']=Q.f_CL.fillna(0)>0
Q['n_top_any']=Q.n_top.fillna(0)>0
Q['banded']=Q.num_banded_clusters.fillna(0)>0
Q['seriated']=Q.num_seriated_clusters.fillna(0)>0
for v in ['n_top_any','tiene_canuto','tiene_CL','banded','seriated']:
    for g in ['ND','NC','NU']:
        a=Q[Q.clase3==g][v]; b=Q[Q.clase3=='resto'][v]
        pa,pb,p=fish(a,b)
        rows.append(dict(var=v,grupo=g,prop_clase=pa,prop_resto=pb,p=p))
R2=pd.DataFrame(rows); ok=R2.p.notna(); R2['q']=np.nan
R2.loc[ok,'q']=stats.false_discovery_control(R2.loc[ok,'p'],method='bh')
print('\n== Binarias ==')
print(R2.sort_values(['var','grupo']).round(4).to_string(index=False))

# procedencia
print('\n== Procedencia (clase vs resto) ==')
Q['proc']=Q.procedencia.fillna('Unknown').replace({'unknown':'Unknown'})
def cat(s):
    s=str(s).lower()
    if 'unknown' in s or s=='nan': return 'Unknown'
    if 'pachacamac' in s: return 'Pachacamac'
    if 'incahuasi' in s or 'incawasi' in s: return 'Incahuasi'
    if 'armatambo' in s or 'huaca san pedro' in s: return 'Armatambo'
    if 'puruchuco' in s: return 'Puruchuco'
    if 'leymebamba' in s or 'chachapoyas' in s: return 'Leymebamba'
    if 'ica' in s or 'pisco' in s or 'ocucaje' in s or 'callango' in s: return 'Ica/Pisco'
    if 'nazca' in s or 'paracas' in s or 'palpa' in s: return 'Nazca/Paracas'
    if 'lima' in s or 'huacho' in s or 'chancay' in s or 'huaquerones' in s: return 'Lima/Huacho'
    if 'arica' in s or 'lluta' in s or 'tarapaca' in s or 'loa' in s or 'chile' in s: return 'N Chile'
    if 'santa' in s or 'trujillo' in s or 'moche' in s or 'chicama' in s: return 'North coast'
    return 'Other'
Q['procc']=Q.proc.map(cat)
ct=pd.crosstab(Q.procc,Q.clase3)
print(ct.to_string())
print('\nchi2 known-only')
known=Q[Q.procc!='Unknown']
print(pd.crosstab(known.procc,known.ND))
chi2,p,dof,exp=stats.chi2_contingency(pd.crosstab(known.procc,known.ND))
print('chi2',round(chi2,2),'dof',dof,'p',round(p,4))
print('\nND rate por procedencia (known):')
print((known.groupby('procc').ND.agg(['size','sum','mean']).sort_values('mean',ascending=False)).round(3).to_string())
Q.to_csv('analisis/ds/n_no_numericos/quipus_clase.csv',index=False)
R.to_csv('analisis/ds/n_no_numericos/tests_caracterizacion.csv',index=False)
R2.to_csv('analisis/ds/n_no_numericos/tests_binarias.csv',index=False)
