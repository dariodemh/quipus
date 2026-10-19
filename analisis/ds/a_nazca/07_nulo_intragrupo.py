# -*- coding: utf-8 -*-
"""Control extra: nulo que baraja valores DENTRO DE CADA GRUPO (preserva
tamano de grupo y patron de ausencias). Si el exceso de corridas compartidas
desaparece, era homogeneidad intra-grupo, no un vinculo entre quipus.
"""
import pandas as pd, numpy as np, os
ROOT=r'.'; D=os.path.join(ROOT,'analisis','datos')
RNG=np.random.default_rng(0); NREP=500
c=pd.read_csv(os.path.join(D,'cuerdas.csv')); q=pd.read_csv(os.path.join(D,'quipus.csv'))
KFG=q.loc[q['procedencia'].isin(['Nazca','Atarco']),'kfg'].tolist()
s=c[c['kfg'].isin(KFG)].copy().sort_values(['kfg','orden'])
def segs(df):
    out={}
    for k,d in df.groupby('kfg'):
        g=[]
        for gid,dd in d[d['nivel']==0].groupby('grupo'):
            seg=[]
            for _,r in dd.iterrows():
                seg.append(int(r['valor']) if (pd.notna(r['nudos']) and str(r['nudos']).strip()!='') else None)
            g.append(seg)
        out[k]=g
    return out
def runs_of(segsd,L):
    out=set()
    for seg in segsd:
        for i in range(len(seg)-L+1):
            w=seg[i:i+L]
            if all(x is not None for x in w): out.add(tuple(w))
    return out
def npairs(segsd,L):
    ks=list(segsd); ss={k:runs_of(segsd[k],L) for k in ks}
    n=0
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            if ss[ks[i]]&ss[ks[j]]: n+=1
    return n
S=segs(s)
print('obs L=3:',npairs(S,3),' L=4:',npairs(S,4),' L=5:',npairs(S,5))
# nulo: permutar valores dentro de cada grupo (solo posiciones no-None)
bases={}
for k,d in s.groupby('kfg'):
    gg=[]
    for gid,dd in d[d['nivel']==0].groupby('grupo'):
        vals=[int(r['valor']) for _,r in dd.iterrows() if pd.notna(r['nudos']) and str(r['nudos']).strip()!='']
        pos=[(i) for i in range(len(dd)) if True]
        gg.append(([None]*len(dd), vals, dd.index.tolist(),
                   [ (pd.notna(r['nudos']) and str(r['nudos']).strip()!='') for _,r in dd.iterrows()]))
    bases[k]=gg
def perm_segs(k):
    out=[]
    for seg,vals,idx,mask in bases[k]:
        seg=seg[:]; v=list(vals); RNG.shuffle(v); it=iter(v)
        for i,m in enumerate(mask):
            seg[i]=next(it) if m else None
        out.append(seg)
    return out
for L in (3,4,5):
    null=[]
    for r in range(NREP):
        perm={k:perm_segs(k) for k in KFG}
        null.append(npairs(perm,L))
    null=np.array(null)
    print(f'L={L}: nulo_intragrupo media={null.mean():.2f} max={null.max()} p={(1+(null>=npairs(S,L)).sum())/(1+NREP):.4f}')
