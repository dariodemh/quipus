# -*- coding: utf-8 -*-
"""Tabla por cuerda y por quipu desde OKR (solo lectura). Salidas: okr_cuerdas.csv, okr_quipus.csv"""
import sqlite3, pandas as pd, numpy as np
B=r"."
c=sqlite3.connect('file:'+B+'/data/external/open-khipu-repository/data/khipu.db?mode=ro',uri=True)
cord=pd.read_sql("select KHIPU_ID,CORD_ID,CORD_LEVEL,TWIST,FIBER,TERMINATION,CORD_LENGTH,CLUSTER_ID,CANUTO_ID,PENDANT_FROM from cord",c)
kn=pd.read_sql("select CORD_ID,TYPE_CODE t,knot_value_type v,NUM_TURNS nt from knot",c)
LT={'L','E','SP','LL','BL','EE'}
kn['long']=kn.t.isin(LT)
kn['v']=pd.to_numeric(kn.v,errors='coerce')
# unidades: nudos largos/E con valor <10 ; vueltas reales: L con NUM_TURNS>=10
kn['u']=kn.long&(kn.v<10)
kn['uv']=np.where(kn.u,kn.v,0)
kn['t10']=(kn.t=='L')&(kn.nt>=10)
g=kn.groupby('CORD_ID').agg(n_knots=('t','size'),n_u=('u','sum'),sum_u=('uv','sum'),t10=('t10','any'),max_u=('uv','max'))
cord=cord.merge(g,left_on='CORD_ID',right_index=True,how='left')
cord['n_knots']=cord.n_knots.fillna(0)
cord['nd_valor']=(cord.sum_u>9)|cord.t10          # criterio principal: suma de unidades >9 o >=10 vueltas
cord['nd_multi']=(cord.n_u>=2)|cord.t10            # criterio amplio: >=2 nudos de unidades
cord.to_csv('okr_cuerdas.csv',index=False)
km=pd.read_sql("select KHIPU_ID,INVESTIGATOR_NUM inv,OKR_NUM okr,PROVENANCE prov,REGION reg,MUSEUM_NAME museo,NOTES from khipu_main",c)
rg=pd.read_sql("select provenance prov,north_south ns,region rg from regions_dc",c)
km=km.merge(rg,on='prov',how='left')
pc=pd.read_sql("select KHIPU_ID,STRUCTURE pc_estr,TWIST pc_twist,FIBER pc_fiber,PCORD_LENGTH pc_len from primary_cord",c).drop_duplicates('KHIPU_ID')
km=km.merge(pc,on='KHIPU_ID',how='left')
rows=[]
for k,d in cord.groupby('KHIPU_ID'):
    dk=d[d.n_knots>0]
    zs=d.TWIST.isin(['S','Z']).sum()
    fb=d.FIBER.replace('',np.nan).dropna()
    r=dict(KHIPU_ID=k,n_cords=len(d),n_knotted=len(dk),
      frac_nd=dk.nd_valor.mean() if len(dk) else np.nan, frac_nd_multi=dk.nd_multi.mean() if len(dk) else np.nan,
      n_tw=zs,frac_Z=(d.TWIST=='Z').sum()/zs if zs else np.nan,
      n_fb=len(fb),frac_cam=fb.isin(['CL','A','L','CC']).mean() if len(fb) else np.nan,frac_cn=(fb=='CN').mean() if len(fb) else np.nan,
      largo_med=d.CORD_LENGTH[d.CORD_LENGTH>0].median(),
      frac_canuto=(d.TERMINATION=='TT').mean(), frac_K=(d.TERMINATION=='K').mean(), frac_U=(d.TERMINATION=='U').mean(),frac_B=d.TERMINATION.isin(['B','C','R']).mean(),
      frac_sub=(d.CORD_LEVEL>1).mean(), max_lvl=d.CORD_LEVEL.max(),
      mean_sumu=dk.sum_u.mean() if len(dk) else np.nan)
    rows.append(r)
q=km.merge(pd.DataFrame(rows),on='KHIPU_ID')
q.to_csv('okr_quipus.csv',index=False)
print(len(q),q.n_cords.describe())
mem="UR050 UR051 UR052 UR053 UR054 UR055 UR039 UR110 UR112 UR144 UR193 KH0001 UR1095 UR1087 UR177".split()
print(q[q.inv.isin(mem)|q.okr.isin(mem)][['inv','okr','prov','n_cords','n_knotted','frac_nd','frac_nd_multi','frac_Z','frac_cam','frac_cn']].round(2).to_string())
