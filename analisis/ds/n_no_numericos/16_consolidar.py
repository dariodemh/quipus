"""Consolida el maestro final: agrega tasa de discrepancia KFG-OKR y flag de transcripcion."""
import pandas as pd, numpy as np
Q=pd.read_csv('analisis/ds/n_no_numericos/quipus_clase.csv')
P=pd.read_csv('analisis/ds/t_okr_vs_kfg/salidas/por_quipu_final.csv')
Q=Q.drop(columns=[c for c in ['tasa_valor','disc_valor','n_valor','n_estruct'] if c in Q])
Q=Q.merge(P[['kfg','tasa_valor','disc_valor','n_valor','n_estruct']],on='kfg',how='left')
bad=['UR090','UR235','UR144','UR193','UR190','KH0058','HP054','HP038','HP004','AS072','AS050','AS101_Part_1','AS101_Part_2','AS069','AS013','AS014','AS036','AS037','AS081','AS129']
Q['flag_tx']=Q.kfg.isin(bad)|(Q.tasa_valor.fillna(0)>0.05)
Q['clase_limpia']=Q.clase&~Q.flag_tx
def subtipo(r):
    s=[]
    if r.ND_seq: s.append('seq')
    if r.ND_dup: s.append('dup')
    if r.ND_inv: s.append('inv')
    if r.NC: s.append('NC')
    if r.NU: s.append('NU')
    return '+'.join(s) if s else ''
Q['subtipo']=Q.apply(subtipo,axis=1)
Q.to_csv('analisis/ds/n_no_numericos/quipus_clase.csv',index=False)
print('clase',Q.clase.sum(),'limpia',Q.clase_limpia.sum())
print(Q[Q.clase&Q.flag_tx][['kfg','subtipo','tasa_valor','disc_valor','n_valor']].to_string(index=False))
print('\nsubtipos clase limpia:'); print(Q[Q.clase_limpia].subtipo.value_counts().to_string())
print('\nlista limpia:'); print(', '.join(sorted(Q[Q.clase_limpia].kfg)))
