"""Construye los grupos de seis cuerdas de los 6 quipus del Santa (UR087-092 = KH0323-28) desde cuerdas.csv."""
import pandas as pd, numpy as np
D='./analisis/datos/'
IDS=['UR087','UR088','UR089','UR090','UR091','UR092']
KH=dict(zip(IDS,['KH0323','KH0324','KH0325','KH0326','KH0327','KH0328']))
PUB_N=dict(zip(IDS,[48,9,34,17,15,10]))  # FitzPatrick 2024 p.4

def grupos_seis():
    c=pd.read_csv(D+'cuerdas.csv',low_memory=False)
    out=[]
    for k in IDS:
        x=c[(c.kfg==k)&(c.nivel==0)].copy()
        x['n']=x.cuerda.str[1:].astype(int)
        x=x.sort_values('n')
        # cuerdas "sueltas" (no pertenecen a un grupo de seis): singletons de espaciado en UR087 (grupo de tamaño 1),
        # p73,p140 de UR089 (union U, sin color/valor), p31,p38 de UR090 y las 4 pardas sobrantes p63-p66 (criterio de Medrano y Urton 2018, via FitzPatrick p.12)
        if k=='UR087':
            sz=x.groupby('grupo').cuerda.transform('size'); x=x[sz>1]
        if k=='UR089': x=x[~x.n.isin([73,140])]
        if k=='UR090': x=x[~x.n.isin([31,38,63,64,65,66])]
        x=x.reset_index(drop=True)
        assert len(x)%6==0,(k,len(x))
        for g in range(len(x)//6):
            b=x.iloc[6*g:6*g+6]
            out.append(dict(kfg=k,kh=KH[k],g=g,vals=b.valor.tolist(),unions=b.union.tolist(),colors=b.color.tolist(),first=b.cuerda.iloc[0]))
    return pd.DataFrame(out)
if __name__=='__main__':
    G=grupos_seis()
    print(G.groupby('kfg').size().to_dict(), len(G))
    G['u1']=G.unions.str[0]; G['v1']=G.vals.str[0]
    print(G.groupby(['kfg','u1']).size().unstack(fill_value=0))
    print('suma primera cuerda',G.v1.sum()); print(G.groupby('u1').v1.agg(['size','sum','mean']))
    print(G.groupby('kfg').v1.sum())
    for p in range(6): print('pos',p+1,'suma',sum(v[p] for v in G.vals))
