"""Negativos: n-gramas de color, entropia condicional, MI tipo-color, direccion.
Aplica BH y compara proporciones clase vs resto.
"""
import pandas as pd, numpy as np
from scipy import stats
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
m=Q[Q.n_pend>=20].copy()
for c in ['p_rep2_c','p_cond_c','p_mi']:
    ok=m[c].notna(); m['q_'+c]=np.nan
    m.loc[ok,'q_'+c]=stats.false_discovery_control(m.loc[ok,c],method='bh')
print('Quipus >=20 pendientes:',len(m),' clase',m.clase.sum())
for c in ['p_rep2_c','p_cond_c','p_mi']:
    for thr in ['p','q']:
        col=(thr+'_'+c) if thr=='q' else c
        a=(m[m.clase][col]<0.05).sum(); na=m.clase.sum()
        b=(m[~m.clase][col]<0.05).sum(); nb=(~m.clase).sum()
        orr,p=stats.fisher_exact([[a,na-a],[b,nb-b]])
        print(f'{col}: clase {a}/{na} ({a/na:.1%}) vs resto {b}/{nb} ({b/nb:.1%}) OR={orr:.2f} p={p:.4f}')
print('\nMedias clase vs resto:')
for v in ['rep2_c','rep3_c','Hn_c','H_c','V1_c','V1_e','mi_pat','mi_val']:
    a=m[m.clase][v].dropna(); b=m[~m.clase][v].dropna()
    print(v,round(a.mean(),3),round(b.mean(),3),'p',round(stats.mannwhitneyu(a,b).pvalue,4))
print('\nValores: distribucion')
for v in ['mean_cord_value','benford_match']:
    a=Q[Q.clase_limpia][v].dropna(); b=Q[(~Q.clase)&~Q.flag_tx][v].dropna()
    print(v,round(a.median(),3),round(b.median(),3),'p',round(stats.mannwhitneyu(a,b).pvalue,4))
# proporcion de cuerdas con valor<10 (usando cuerdas)
C=pd.read_csv('analisis/ds/n_no_numericos/cuerdas_anom.csv')
C=C.merge(Q[['kfg','clase']],on='kfg',how='left')
g=C[C.nclust>0].groupby('kfg').apply(lambda d: pd.Series({'frac_lt10':(d.valor<10).mean(),'frac_rep':1-d.valor.nunique()/len(d)}),include_groups=False)
Q2=Q.merge(g,on='kfg',how='left')
a=Q2[Q2.clase_limpia].frac_lt10.dropna(); b=Q2[(~Q2.clase)&~Q2.flag_tx].frac_lt10.dropna()
print('frac valores<10',round(a.median(),3),round(b.median(),3),'p',round(stats.mannwhitneyu(a,b).pvalue,4))
a=Q2[Q2.clase_limpia].frac_rep.dropna(); b=Q2[(~Q2.clase)&~Q2.flag_tx].frac_rep.dropna()
print('frac valores repetidos',round(a.median(),3),round(b.median(),3),'p',round(stats.mannwhitneyu(a,b).pvalue,4))
Q2.to_csv('analisis/ds/n_no_numericos/quipus_clase.csv',index=False)
