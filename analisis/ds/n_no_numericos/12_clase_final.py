"""Clase final: reconstruye el maestro limpio y aplica umbrales + nulos."""
import pandas as pd, numpy as np
from scipy import stats
base=pd.read_csv('analisis/ds/n_no_numericos/quipus_direccion.csv')
nc=pd.read_csv('analisis/ds/n_no_numericos/nulo_corpus.csv').drop(columns=['n_multi','D','I','Q','D_null','I_null','Q_null'])
cg=pd.read_csv('analisis/ds/n_no_numericos/quipus_colorgram.csv')
cgcols=[c for c in cg.columns if c.startswith(('rep','max','V1','V2','V3','not','H_','Hn_','p_rep','p_cond'))]+['n_pend']
tm=pd.read_csv('analisis/ds/n_no_numericos/quipus_tipomi.csv')
tmcols=['n','mi_pat','mi_val','mi_pat_null','p_mi','Hcolor','Vpat','Hpat','Vcolor']
Q=base.merge(nc,on='kfg',how='left').merge(cg[['kfg']+cgcols],on='kfg',how='left').merge(tm[['kfg']+tmcols],on='kfg',how='left')
ok=Q.Rdiff_p.notna(); Q['Rdiff_q']=np.nan
Q.loc[ok,'Rdiff_q']=stats.false_discovery_control(Q.loc[ok,'Rdiff_p'],method='bh')
Q['ND_seq']=(Q.n_multi>=5)&(Q.Q>=0.5)&(Q.qQ_hi<0.05)
Q['ND_dup']=(Q.n_multi>=5)&(Q.D>=0.5)&(Q.qD_hi<0.05)
Q['ND_inv']=(Q.n_multi>=5)&(Q.I>=0.10)&(Q.qI_hi<0.05)
Q['ND']=Q.ND_seq|Q.ND_dup|Q.ND_inv
Q['NC']=(Q.n_knotless>=5)&(Q.n_knotted>=5)&(Q.Rdiff>=0.3)&(Q.Rdiff_q<0.05)
Q['NU']=(Q.Z>=0.10)&(Q.ncuerdas>=8)
Q['clase']=Q.ND|Q.NC|Q.NU
bad=['UR090','UR235','UR144','UR193','UR190','KH0058','HP054','HP038','HP004','AS072','AS050','AS101_Part_1','AS101_Part_2','AS069','AS013','AS014','AS036','AS037','AS081','AS129']
Q['flag_tx']=Q.kfg.isin(bad)|(Q.tasa_valor.fillna(0)>0.05) if 'tasa_valor' in Q else Q.kfg.isin(bad)
Q['clase_limpia']=Q.clase&~Q.flag_tx
Q['score2']=0.45*Q.D+0.30*Q.I+0.25*Q.Q
Q.to_csv('analisis/ds/n_no_numericos/quipus_clase.csv',index=False)
print('ND_seq',Q.ND_seq.sum(),'ND_dup',Q.ND_dup.sum(),'ND_inv',Q.ND_inv.sum(),'ND',Q.ND.sum(),'NC',Q.NC.sum(),'NU',Q.NU.sum(),'union',Q.clase.sum(),'limpia',Q.clase_limpia.sum())
print('\nND por prefijo'); print(pd.crosstab(Q.pref,Q.ND).T.to_string())
print('\nNC final:'); print(Q[Q.NC][['kfg','ncuerdas','n_knotless','n_knotted','Rdiff','Rdiff_p','Rdiff_q','procedencia']].round(3).to_string(index=False))
print('\nND inv/seq/dup counts:',Q.ND_seq.sum(),Q.ND_dup.sum(),Q.ND_inv.sum())
print('\nND top score:')
print(Q[Q.ND].sort_values('score2',ascending=False)[['kfg','ncuerdas_nudo','n_multi','D','I','Q','num_canuto_cords','f_CL','procedencia']].head(20).round(2).to_string(index=False))
