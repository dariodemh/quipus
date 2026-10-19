import pandas as pd, numpy as np
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
top=['UR179','UR180','UR178','UR050','UR054','UR052','AS076','JC012','UR203','UR215']
d=Q[Q.kfg.isin(top)].copy()
d['orden']=d.kfg.map({k:i+1 for i,k in enumerate(top)})
cols=['orden','kfg','ncuerdas','ncuerdas_nudo','n_multi','D','I','Q','frac_units','Z','num_canuto_cords','f_CL','frac_rico','fracS','procedencia','museo','flag_tx','ND','NC','NU','subtipo']
d[cols].sort_values('orden').round(3).to_csv('analisis/ds/n_no_numericos/top10.csv',index=False)
print(d[cols].sort_values('orden').round(3).to_string(index=False))
mp=pd.read_csv('analisis/ds/t_okr_vs_kfg/salidas/mapa_quipus.csv')
print('\nOKR:')
print(d[['kfg']].merge(mp,on='kfg',how='left')[['kfg','okr','KHIPU_ID','via']].to_string(index=False))
