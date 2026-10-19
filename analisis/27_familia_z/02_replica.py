# -*- coding: utf-8 -*-
"""Replica en OKR: tally (>=50% cuerdas no decimales) vs torsion Z, controlando fibra y procedencia."""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
from scipy.stats import fisher_exact
from statsmodels.stats.contingency_tables import StratifiedTable, Table2x2
import statsmodels.api as sm
rng=np.random.default_rng(20261018)
q=pd.read_csv('okr_quipus.csv'); cd=pd.read_csv('okr_cuerdas.csv')
q['rg']=q.rg.fillna('').replace('', 'sin_region'); q['rg']=q.rg.where(q.rg!='Unknown','sin_region')
q['fibra']=np.select([q.frac_cam>=.5,q.frac_cn>=.5],['camelido','algodon'],default=np.where(q.n_fb>0,'mixta','sd'))
base=q[(q.n_knotted>=30)&(q.n_tw>=10)].copy()
base['Z']=(base.frac_Z>.5).astype(int)
out=[]; lines=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); lines.append(s)
P("quipus OKR:",len(q),"con >=30 cuerdas con nudos y >=10 con torsion S/Z:",len(base))
for nombre,col in [('A_multi50','frac_nd_multi'),('B_valor50','frac_nd')]:
  for thr in (.5,):
    b=base.copy(); b['T']=(b[col]>=thr).astype(int)
    P(f"\n== {nombre} (>= {thr:.0%} cuerdas no decimales) ==  tally n={b['T'].sum()}:",', '.join(b[b['T']==1].inv.tolist()))
    t=pd.crosstab(b['T'],b.Z).reindex(index=[0,1],columns=[0,1],fill_value=0)
    P("tabla tally x Z (filas T=0/1, cols Z=0/1):",t.values.tolist())
    orr,p=fisher_exact(t.values); P(f"Fisher: OR={orr:.1f} p={p:.2g}; Z en tally {t.loc[1,1]}/{t.loc[1].sum()}, en decimales {t.loc[0,1]}/{t.loc[0].sum()}")
    out.append(dict(criterio=nombre,prueba='Fisher global',n=len(b),n_tally=int(b['T'].sum()),OR=orr,p=p))
    # CMH por estratos
    def cmh(strat,label):
        tabs=[]
        for k,g in b.groupby(strat):
            tt=pd.crosstab(g['T'],g.Z).reindex(index=[0,1],columns=[0,1],fill_value=0).values
            if tt.sum()>0 and (tt.sum(1)>0).all() and (tt.sum(0)>0).all(): tabs.append(tt)
        st=StratifiedTable(tabs); r=st.test_null_odds(correction=True)
        # permutacion intra-estrato del estadistico MH
        def stat(zz):
            bb=b.assign(Z2=zz); s=0
            for k,g in bb.groupby(strat): s+=((g['T']==1)&(g.Z2==1)).sum()-g['T'].sum()*g.Z2.sum()/len(g)
            return s
        obs=stat(b.Z.values); null=[]
        idx={k:v.index for k,v in b.groupby(strat)}
        for _ in range(5000):
            z=b.Z.copy()
            for k,ix in idx.items(): z.loc[ix]=rng.permutation(b.Z.loc[ix].values)
            null.append(stat(z.values))
        pp=(1+np.sum(np.array(null)>=obs))/5001
        P(f"CMH controlando {label}: estratos usados={len(tabs)}, OR_MH={st.oddsratio_pooled:.1f} (IC95 {st.oddsratio_pooled_confint()[0]:.1f}-{st.oddsratio_pooled_confint()[1]:.1f}), p_cmh={r.pvalue:.2g}; p perm intra-estrato (unilateral)={pp:.4f}")
        out.append(dict(criterio=nombre,prueba='CMH '+label,n=len(b),n_tally=int(b['T'].sum()),OR=st.oddsratio_pooled,p=r.pvalue,p_perm=pp))
    cmh('fibra','fibra (camelido/algodon/mixta/sd)')
    cmh('rg','region de procedencia')
    b['fr']=b.fibra+'|'+b.rg; cmh('fr','fibra x region')
    # subconjuntos
    for f in ['algodon','camelido']:
        s=b[b.fibra==f]; t=pd.crosstab(s['T'],s.Z).reindex(index=[0,1],columns=[0,1],fill_value=0)
        o,p=fisher_exact(t.values); P(f"solo fibra {f}: tabla {t.values.tolist()} OR={o:.1f} p={p:.2g}")
        out.append(dict(criterio=nombre,prueba='Fisher solo '+f,n=len(s),n_tally=int(s['T'].sum()),OR=o,p=p))
    # logit con fibra conocida
    s=b[b.fibra.isin(['algodon','camelido','mixta'])].copy(); s['cam']=(s.frac_cam).fillna(0)
    X=sm.add_constant(s[['Z','cam']].astype(float))
    try:
        m=sm.Logit(s['T'],X).fit(disp=0,maxiter=200); P("logit T ~ Z + fraccion_camelido (n=%d): Z=%.2f p=%.3g; cam=%.2f p=%.3g"%(len(s),m.params.Z,m.pvalues.Z,m.params.cam,m.pvalues.cam))
        out.append(dict(criterio=nombre,prueba='logit Z|cam',n=len(s),n_tally=int(s['T'].sum()),OR=np.exp(m.params.Z),p=m.pvalues.Z))
    except Exception as e: P('logit fallo',e)
    # continuo: Spearman frac_nd vs frac_Z
    from scipy.stats import spearmanr
    r,p=spearmanr(base[col],base.frac_Z); P(f"Spearman {col} vs frac_Z (n={len(base)}): rho={r:.2f} p={p:.2g}")
# Nivel cuerda: dentro de quipus mixtos S/Z, cuerda Z vs no decimal (estratos = quipu)
c=cd[cd.TWIST.isin(['S','Z'])&(cd.n_knots>0)].copy(); c['Zc']=(c.TWIST=='Z').astype(int)
for col in ['nd_valor','nd_multi']:
    tabs=[]
    for k,g in c.groupby('KHIPU_ID'):
        t=pd.crosstab(g.Zc,g[col].astype(int)).reindex(index=[0,1],columns=[0,1],fill_value=0).values
        if (t.sum(1)>0).all() and (t.sum(0)>0).all(): tabs.append(t)
    st=StratifiedTable(tabs); r=st.test_null_odds(correction=True)
    P(f"\nNivel cuerda, dentro de quipus con S y Z (estratos={len(tabs)}), {col}: OR_MH(Z vs S -> no decimal)={st.oddsratio_pooled:.2f} IC {st.oddsratio_pooled_confint()[0]:.2f}-{st.oddsratio_pooled_confint()[1]:.2f} p={r.pvalue:.2g}")
    out.append(dict(criterio=col,prueba='cuerda Z vs S dentro de quipu (CMH)',n=len(c),n_tally=len(tabs),OR=st.oddsratio_pooled,p=r.pvalue))
pd.DataFrame(out).to_csv('replica_resultados.csv',index=False)
base.to_csv('replica_base.csv',index=False)
open('replica_salida.txt','w',encoding='utf-8').write('\n'.join(lines))
