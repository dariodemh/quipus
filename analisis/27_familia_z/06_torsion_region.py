# -*- coding: utf-8 -*-
"""Con OKR: P(Z) por fibra y por region (quipu como unidad), para evaluar 'Z=sierra/camelido'."""
import sqlite3,pandas as pd,numpy as np
from scipy.stats import fisher_exact
B=r"."
c=sqlite3.connect('file:'+B+'/data/external/open-khipu-repository/data/khipu.db?mode=ro',uri=True)
cd=pd.read_csv('okr_cuerdas.csv'); q=pd.read_csv('okr_quipus.csv')
cd=cd[cd.TWIST.isin(['S','Z'])].copy(); cd['Z']=(cd.TWIST=='Z').astype(int)
cd['fib']=cd.FIBER.map({'CN':'algodon','CL':'camelido','CC':'mixta','W':'lana_oveja','H':'pelo','AH':'pelo','V':'vegetal'})
t=cd.groupby('fib',dropna=False).Z.agg(['size','mean']); print("Cuerdas: P(Z) por fibra\n",t.round(3)); t.to_csv('torsion_por_fibra_cuerda.csv')
# quipu-nivel: cuantos quipus tienen >=1 cuerda Z camelido etc.
rg=pd.read_sql("select provenance prov,north_south ns,region rg from regions_dc",c)
print(rg.rg.value_counts().to_dict())
q=q.drop(columns=['rg','ns'],errors='ignore').merge(rg,on='prov',how='left')
cd=cd.merge(q[['KHIPU_ID','rg','ns']],on='KHIPU_ID',how='left'); cd['rg']=cd.rg.fillna('sin_prov')
# P(Z) por region en cuerdas de algodon y de camelido, y media por quipu
for f in ['algodon','camelido']:
    s=cd[cd.fib==f]; per=s.groupby(['rg','KHIPU_ID']).Z.mean().groupby('rg').agg(['size','mean','median'])
    per['cuerdas']=s.groupby('rg').size(); print(f"\nfibra {f}: P(Z) por region (quipus = unidad)\n",per.round(3))
    per.round(4).to_csv(f'torsion_region_{f}.csv')
# camelido vs algodon dentro de quipus mixtos (CMH por quipu)
from statsmodels.stats.contingency_tables import StratifiedTable
tabs=[]
for k,g in cd[cd.fib.isin(['algodon','camelido'])].groupby('KHIPU_ID'):
    tt=pd.crosstab(g.fib=='camelido',g.Z).reindex(index=[False,True],columns=[0,1],fill_value=0).values
    if (tt.sum(1)>0).all() and (tt.sum(0)>0).all(): tabs.append(tt)
st=StratifiedTable(tabs); print(f"\nDentro de quipus con ambas fibras (n={len(tabs)}): OR_MH Z camelido vs algodon={st.oddsratio_pooled:.2f} IC {st.oddsratio_pooled_confint()[0]:.2f}-{st.oddsratio_pooled_confint()[1]:.2f} p={st.test_null_odds(correction=True).pvalue:.2g}")
