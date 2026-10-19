# -*- coding: utf-8 -*-
"""Lectura aditiva descriptiva: UR050, UR054, UR055 (y UR052/UR051 de referencia). OKR solo lectura."""
import sqlite3,pandas as pd,numpy as np,warnings; warnings.filterwarnings('ignore')
from scipy.stats import spearmanr,kruskal
rng=np.random.default_rng(20261018)
B=r"."
c=sqlite3.connect('file:'+B+'/data/external/open-khipu-repository/data/khipu.db?mode=ro',uri=True)
rows=[];L=[]
for inv in ['UR050','UR054','UR055','UR052']:
    k=c.execute("select KHIPU_ID from khipu_main where INVESTIGATOR_NUM=?",(inv,)).fetchone()[0]
    d=pd.read_sql("select c.CORD_ID,c.CORD_ORDINAL o,c.CORD_LENGTH ln,k.TYPE_CODE t,k.knot_value_type v,kc.START_POS p from cord c join knot k on k.CORD_ID=c.CORD_ID join knot_cluster kc on kc.CLUSTER_ID=k.CLUSTER_ID where c.KHIPU_ID=? and k.TYPE_CODE='L' order by c.CORD_ORDINAL,kc.START_POS",c,params=(k,))
    d['v']=d.v.astype(float)
    g=d.groupby('o').agg(vals=('v',list),n=('v','size'),ln=('ln','first'),s=('v','sum'))
    allv=d.v[d.v>0]
    print(f"\n=== {inv}: {len(g)} cuerdas, {len(d)} cuentas L; n cuentas/cuerda {g.n.value_counts().sort_index().to_dict()}")
    print("distribucion valores 0..12:",d.v.value_counts().sort_index().astype(int).to_dict())
    print(f"media {allv.mean():.2f} var {allv.var():.2f} indice dispersion var/media {allv.var()/allv.mean():.2f}; suma por cuerda: mediana {g.s.median()} CV {g.s.std()/g.s.mean():.2f}")
    r=dict(quipu=inv,cuerdas=len(g),cuentas=len(d),media=allv.mean(),dispersion=allv.var()/allv.mean(),CV_suma=g.s.std()/g.s.mean())
    # igualdad intra-cuerda vs nulo (permutar valores entre cuerdas con el mismo n, conservando posicion)
    for nn in sorted(g.n.unique()):
        if nn<2: continue
        G=g[g.n==nn]
        if len(G)<15: continue
        M=np.array(G.vals.tolist())
        eq=lambda M:np.mean([len(set(x))==1 for x in M]); adj=lambda M:np.mean((M[:,1:]==M[:,:-1]))
        o_eq,o_adj=eq(M),adj(M); ne=[];na=[]
        for _ in range(2000):
            P=np.column_stack([rng.permutation(M[:,j]) for j in range(nn)]); ne.append(eq(P)); na.append(adj(P))
        pe=(1+np.sum(np.array(ne)>=o_eq))/2001; pa=(1+np.sum(np.array(na)>=o_adj))/2001
        rho=np.mean([spearmanr(M[:,i],M[:,j])[0] for i in range(nn) for j in range(i+1,nn)])
        zm=M.mean(0)
        print(f"  cuerdas con {nn} cuentas (n={len(G)}): todas iguales {o_eq:.1%} (nulo {np.mean(ne):.1%}, p={pe:.4f}); adyacentes iguales {o_adj:.1%} (nulo {np.mean(na):.1%}, p={pa:.4f}); rho medio entre cuentas {rho:.2f}; media por posicion {np.round(zm,2).tolist()}")
        L.append(dict(quipu=inv,cuentas_por_cuerda=nn,n=len(G),todas_iguales=o_eq,nulo_iguales=np.mean(ne),p_iguales=pe,adyacentes_iguales=o_adj,nulo_adyacentes=np.mean(na),p_adyacentes=pa,rho_medio=rho,medias_posicion=str(np.round(zm,2).tolist())))
    # autocorrelacion por orden de cuerda (suma) y relacion largo-suma
    s=g.s.values; r1=spearmanr(s[1:],s[:-1])[0]
    nul=[spearmanr(*(lambda x:(x[1:],x[:-1]))(rng.permutation(s)))[0] for _ in range(2000)]
    p1=(1+np.sum(np.abs(nul)>=abs(r1)))/2001
    rl,pl=spearmanr(g.ln,g.s,nan_policy='omit')
    print(f"  autocorrelacion lag-1 de la suma por orden de cuerda: rho={r1:.2f} (p perm={p1:.4f}); largo vs suma: rho={rl:.2f} p={pl:.2g}")
    r.update(rho_lag1=r1,p_lag1=p1,rho_largo_suma=rl,p_largo_suma=pl); rows.append(r)
pd.DataFrame(rows).to_csv('aditiva_resumen.csv',index=False); pd.DataFrame(L).to_csv('aditiva_igualdad.csv',index=False)
