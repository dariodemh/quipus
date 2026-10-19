# -*- coding: utf-8 -*-
"""Perfil de la familia tally (A_multi50) vs decimales (todos y pareados por tamano). BH."""
import sqlite3, pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
from scipy.stats import mannwhitneyu, fisher_exact, chi2_contingency
from statsmodels.stats.multitest import multipletests
rng=np.random.default_rng(20261018)
B=r"."
c=sqlite3.connect('file:'+B+'/data/external/open-khipu-repository/data/khipu.db?mode=ro',uri=True)
q=pd.read_csv('okr_quipus.csv'); cd=pd.read_csv('okr_cuerdas.csv')
# extras: grupos, colores, nudos
cl=pd.read_sql("select KHIPU_ID,count(*) n_grp,avg(NUM_CORDS) grp_media,count(distinct NUM_CORDS)*1.0/count(*) grp_var from cord_cluster where CLUSTER_LEVEL=1 group by 1",c)
col=pd.read_sql("select KHIPU_ID,COLOR_CD_1 c1,COLOR_CD_2 c2,FULL_COLOR fc from ascher_cord_color where PCORD_FLAG=0",c)
cc=col.groupby('KHIPU_ID').agg(n_colores=('c1','nunique'),multic=('c2',lambda s:(s.notna()&(s!='')).mean()),dom=('c1',lambda s:s.value_counts(normalize=True).iloc[0]))
kn=pd.read_sql("select k.CORD_ID,c.KHIPU_ID,k.TYPE_CODE t,k.knot_value_type v,k.NUM_TURNS nt from knot k join cord c using(CORD_ID)",c)
kn['v']=pd.to_numeric(kn.v,errors='coerce')
L=kn[(kn.t=='L')&(kn.v<10)]
vd=L.groupby('KHIPU_ID').v.agg(L_media='mean',L_n='size')
for lo,hi,n in [(2,3,'L23'),(4,6,'L46'),(7,9,'L79')]:
    vd[n]=L.assign(x=L.v.between(lo,hi)).groupby('KHIPU_ID').x.mean()
vd['L_ge10']=kn[kn.t=='L'].assign(x=lambda d:d.nt>=10).groupby('KHIPU_ID').x.mean()
tk=kn.groupby('KHIPU_ID').t.value_counts(normalize=True).unstack().fillna(0)[['S','L','E']].add_prefix('sh_')
kpc=cd[cd.n_knots>0].groupby('KHIPU_ID').agg(knots_x_cuerda=('n_knots','mean'),u_x_cuerda=('n_u','mean'),sumu_med=('sum_u','median'),frac_vacias=('n_knots',lambda s:0))
q=q.merge(cl,on='KHIPU_ID',how='left').merge(cc,on='KHIPU_ID',how='left').merge(vd,on='KHIPU_ID',how='left').merge(tk,on='KHIPU_ID',how='left').merge(kpc,on='KHIPU_ID',how='left')
q['vacias']=cd.groupby('KHIPU_ID').n_knots.apply(lambda s:(s==0).mean()).reindex(q.KHIPU_ID).values
q['con_sub']=(q.frac_sub>0).astype(int); q['pc_tw_Z']=(q.pc_twist=='Z').astype(int); q['pc_estr_P']=(q.pc_estr=='P').astype(int)
q['Zmay']=(q.frac_Z>.5).astype(int); q['sin_prov']=((q.prov.fillna('')=='')).astype(int)
q['museo_s']=q.museo.fillna('').str.replace('"','').str.slice(0,30)
base=q[(q.n_knotted>=30)].copy(); base['fam']=(base.frac_nd_multi>=.5).astype(int)
fam=base[base.fam==1]; ctl=base[base.fam==0]
print('familia',len(fam),'control total',len(ctl)); print(fam[['inv','prov','museo_s','n_cords','frac_Z','frac_cam']].to_string())
cont=['n_cords','largo_med','frac_canuto','frac_K','frac_U','frac_B','frac_sub','max_lvl','n_grp','grp_media','n_colores','multic','dom','L_media','L23','L46','L79','L_ge10','sh_S','sh_L','sh_E','knots_x_cuerda','u_x_cuerda','sumu_med','vacias','pc_len','frac_Z']
binar=['con_sub','pc_tw_Z','pc_estr_P','Zmay','sin_prov']
def matched():
    pool=ctl.copy(); sel=[]
    for _,r in fam.sample(frac=1,random_state=int(rng.integers(1e9))).iterrows():
        d=(np.log(pool.n_cords)-np.log(r.n_cords)).abs().sort_values().head(5)
        i=rng.choice(d.index); sel.append(i); pool=pool.drop(i)
    return ctl.loc[sel]
rows=[]
def mw(a,b):
    a=a.dropna();b=b.dropna()
    if len(a)<3 or len(b)<3: return np.nan
    return mannwhitneyu(a,b).pvalue
M=[matched() for _ in range(500)]
for v in cont:
    pm=[mw(fam[v],m[v]) for m in M]
    rows.append(dict(rasgo=v,tipo='cont',fam_med=fam[v].median(),ctl_med=ctl[v].median(),ctlpar_med=np.median([m[v].median() for m in M]),n_fam=fam[v].notna().sum(),p_todos=mw(fam[v],ctl[v]),p_pareado_med=np.nanmedian(pm),frac_pareados_p05=np.nanmean(np.array(pm)<.05)))
for v in binar:
    t=[[fam[v].sum(),(1-fam[v]).sum()],[ctl[v].sum(),(1-ctl[v]).sum()]]
    pm=[fisher_exact([[fam[v].sum(),(1-fam[v]).sum()],[m[v].sum(),(1-m[v]).sum()]])[1] for m in M]
    rows.append(dict(rasgo=v,tipo='bin',fam_med=fam[v].mean(),ctl_med=ctl[v].mean(),ctlpar_med=np.mean([m[v].mean() for m in M]),n_fam=len(fam),p_todos=fisher_exact(t)[1],p_pareado_med=np.median(pm),frac_pareados_p05=np.mean(np.array(pm)<.05)))
# categoricas: museo, procedencia (Fisher de "estar en la categoria" para las mas frecuentes en la familia)
for v in ['museo_s','prov']:
    for k in fam[v].fillna('').value_counts().index[:4]:
        a=(fam[v].fillna('')==k).sum(); b_=(ctl[v].fillna('')==k).sum()
        p=fisher_exact([[a,len(fam)-a],[b_,len(ctl)-b_]])[1]
        rows.append(dict(rasgo=f'{v}={k or "(vacio)"}',tipo='cat',fam_med=a/len(fam),ctl_med=b_/len(ctl),n_fam=len(fam),p_todos=p,p_pareado_med=np.nan))
r=pd.DataFrame(rows)
for col in ['p_todos','p_pareado_med']:
    m=r[col].notna(); r.loc[m,'BH_'+col]=multipletests(r.loc[m,col],method='fdr_bh')[1]
r.round(4).to_csv('perfil_resultados.csv',index=False)
print(r.round(4).to_string(index=False))
# histograma de valores por cuenta (cuerdas L unidades, 1-9, >=10 vueltas)
def hist(ids):
    x=L[L.KHIPU_ID.isin(ids)].v.value_counts(normalize=True).reindex(range(2,10)).fillna(0)
    t10=kn[(kn.KHIPU_ID.isin(ids))&(kn.t=='L')]; return x.round(3).tolist(),round((t10.nt>=10).mean(),4)
h=pd.DataFrame({'familia':hist(fam.KHIPU_ID)[0],'decimales':hist(ctl.KHIPU_ID)[0]},index=range(2,10)); h.loc['>=10 vueltas']=[hist(fam.KHIPU_ID)[1],hist(ctl.KHIPU_ID)[1]]
h.to_csv('perfil_hist_valores.csv'); print(h)
base.to_csv('perfil_base.csv',index=False)
