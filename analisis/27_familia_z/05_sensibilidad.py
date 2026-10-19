# -*- coding: utf-8 -*-
"""Sensibilidad: umbral del criterio y colapso de series no independientes (UR050-055; BCR UR051/052; Berlin)."""
import pandas as pd,numpy as np
from scipy.stats import fisher_exact
b=pd.read_csv('replica_base.csv'); out=[]
for thr in (.3,.4,.5,.6,.7):
    b['T']=(b.frac_nd_multi>=thr).astype(int); t=pd.crosstab(b['T'],b.Z).reindex(index=[0,1],columns=[0,1],fill_value=0).values
    o,p=fisher_exact(t); out.append(dict(variante=f'umbral {thr:.0%}',n_tally=int(b['T'].sum()),Z_en_tally=int(t[1,1]),Z_en_decim=int(t[0,1]),n_decim=int(t[0].sum()),OR=o,p=p))
# colapsar serie UR050-055 en una unidad (Z si mayoria de miembros Z)
b['T']=(b.frac_nd_multi>=.5).astype(int)
serie=b.inv.isin(['UR050','UR051','UR052','UR053','UR054','UR055'])
s=b[serie&(b['T']==1)]; zs=int(s.Z.mean()>.5)
c=b[~serie]
t=pd.crosstab(c['T'],c.Z).reindex(index=[0,1],columns=[0,1],fill_value=0).values
t2=t.copy(); t2[1,zs]+=1
o,p=fisher_exact(t2); out.append(dict(variante='serie UR050-055 colapsada en 1 unidad',n_tally=int(t2[1].sum()),Z_en_tally=int(t2[1,1]),Z_en_decim=int(t2[0,1]),n_decim=int(t2[0].sum()),OR=o,p=p))
o,p=fisher_exact(t); out.append(dict(variante='sin la serie UR050-055',n_tally=int(t[1].sum()),Z_en_tally=int(t[1,1]),Z_en_decim=int(t[0,1]),n_decim=int(t[0].sum()),OR=o,p=p))
# ademas sin quipus Berlin (UR193, UR203 mismo museo)
c2=c[~c.inv.isin(['UR203'])]
t=pd.crosstab(c2['T'],c2.Z).reindex(index=[0,1],columns=[0,1],fill_value=0).values; t[1,zs]+=1
o,p=fisher_exact(t); out.append(dict(variante='serie colapsada y sin UR203',n_tally=int(t[1].sum()),Z_en_tally=int(t[1,1]),Z_en_decim=int(t[0,1]),n_decim=int(t[0].sum()),OR=o,p=p))
r=pd.DataFrame(out); r.round(5).to_csv('sensibilidad.csv',index=False); print(r.round(5).to_string(index=False))
print(b[b['T']==1][['inv','okr','frac_Z','frac_cam','frac_cn','n_cords']].round(2).to_string())
