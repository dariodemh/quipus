# UR006 (Urton cap. 4): estructura 24 pares [20-22]+[8-9 loop pendants], sumas por par (Tabla 4.3), segmento c vs UR009/UR021
from util import *
rng=np.random.default_rng(12017)
d=q('UR006'); d['pn']=d.cuerda.str.extract(r'^p(\d+)')[0].astype(int)
ch=d[d.nivel==1].groupby('padre').size(); loops=ch[ch>=5]
regs=[2,5,7,10,12,14,16,18,20,22,24,26,28,30,32,36,38,40,43,45,47,50,53,56]
g=d[d.nivel==0].groupby('grupo').pn.agg(['min','max'])
loop_pn=sorted(int(c[1:]) for c in loops.index if c!='p24')
sets=[]
for gr in regs:
    a,b=g.loc[gr]; nl=[p for p in loop_pn if p>b][0]
    reg=d[(d.pn>=a)&(d.pn<=b)]
    lp=d[d.pn==nl]
    sets.append(dict(a=a,b=b,loop=nl,n_reg=int((reg.nivel==0).sum()),n_loop=int((lp.nivel==1).sum()),
        suma_reg=reg.valor.sum(),suma_loop=lp.valor.sum()))
S=pd.DataFrame(sets); S['n']=S.n_reg+S.n_loop
print(S.to_string())
print('tot cuerdas en pares',S.n.sum(),'año1',S.n[:12].sum(),'año2',S.n[12:].sum(),'semestres',[int(S.n[i:i+6].sum()) for i in (0,6,12,18)])
print('suma valores total',d.valor.sum(),'año1(hasta par12)',d[d.pn<=S.loop[11]].valor.sum())
inset=set()
for r in S.itertuples(): inset|=set(range(r.a,r.b+1)); inset.add(r.loop)
print('fuera de pares',d[~d.pn.isin(inset)].valor.sum(),'dentro',d[d.pn.isin(inset)].valor.sum())
# Urton Tabla 4.3 (transcrita del PDF; ambigua en año 2)
U1=[(75,135),(58,19),(60,12),(52,595),(58,150),(44,10),(45,11),(49,103),(83,148),(67,13),(71,12),(71,87)]
U2=[(59,121),(52,12),(55,13),(57,86),(30,76),(26,7),(28,7),(33,64),(19,7),(22,5),(39,66),(12,37)]
K=list(zip(S.suma_reg.astype(int),S.suma_loop.astype(int)))
ex=[(k[0]==u[0])+(k[1]==u[1]) for k,u in zip(K,U1+U2)]
print('cifras Tabla4.3 coincidentes: año1',sum(ex[:12]),'/24  año2',sum(ex[12:]),'/24')
# nulo: ¿cuántas coincidencias exactas de 48 cifras se esperan si permutamos los valores entre cuerdas de UR006 y recalculamos sumas?
def sums_for(vals):
    dd=d.copy(); dd['valor']=vals
    out=[]
    for r in sets:
        reg=dd[(dd.pn>=r['a'])&(dd.pn<=r['b'])].valor.sum(); lp=dd[dd.pn==r['loop']].valor.sum()
        out.append((int(reg),int(lp)))
    return out
cnt=[]
U=U1+U2
for _ in range(1000):
    v=rng.permutation(d.valor.values)
    k=sums_for(v); cnt.append(sum((a[0]==b[0])+(a[1]==b[1]) for a,b in zip(k,U)))
print('nulo permutacion valores: coincidencias exactas media',np.mean(cnt),'max',max(cnt),' observado',sum(ex))
# calendario: remuestreo de tamaños de pares
sz=S.n.values
tot=[rng.choice(sz,24).sum() for _ in range(20000)]
print('P(|total-730|<=1) remuestreando tamaños:',np.mean(np.abs(np.array(tot)-730)<=1), ' media',np.mean(tot))
# pares que se desvian 1 de 30 etc
# 3000: total de cualquier quipu cerca de múltiplo de 1000 (±1.5%)
tt=C.groupby('kfg').valor.sum()
tt=tt[(tt>=1500)&(tt<=6000)]
near=lambda T: min(abs(T-round(T/1000)*1000)/T,1)
fr=np.mean([near(T)<=abs(3037-3000)/3037 for T in tt]); print('quipus 1500-6000: frac con total a <=%.2f%% de un múltiplo de 1000:'%(100*abs(3037-3000)/3037),fr,len(tt))
S.to_csv('ur006_pares.csv',index=False)
# LCS segmento c vs UR009/UR021
def lcs(a,b):
    m=[[0]*(len(b)+1) for _ in a+[0]]
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            m[i][j]=m[i-1][j-1]+1 if a[i-1]==b[j-1] else max(m[i-1][j],m[i][j-1])
    return m[-1][-1]
def seq_sets(i0,i1,thr=3):
    a=S.a[i0]; b=S.loop[i1]
    x=d[(d.pn>=a)&(d.pn<=b)&(d.valor>=thr)]; return [int(v) for v in x.valor]
for other in ['UR009','UR021']:
    o=q(other); o=o[o.nivel==0]
    # incluye subsidiarias y orden
    oseq=[int(v) for v in q(other).valor if v>=3]
    res=[]
    for i0 in range(0,21):
        res.append(lcs(seq_sets(i0,i0+3),oseq))
    print(other,'LCS(valores>=3) bloque meses13-16 =',res[12],' otros bloques de 4 pares: media',np.mean([r for i,r in enumerate(res) if abs(i-12)>3]),'max',max([r for i,r in enumerate(res) if abs(i-12)>3]),' len bloque',len(seq_sets(12,15)),' len',len(oseq))
    allr=[lcs(seq_sets(i0,i0+3),oseq) for i0 in range(21)]
    print('  por bloque:',allr)
print('--- LCS umbral>=5, nulo permutando orden de valores de la otra quipu')
for other in ['UR009','UR021']:
    oseq=[int(v) for v in q(other).valor if v>=5]
    obs=[lcs(seq_sets(i0,i0+3,5),oseq) for i0 in range(21)]
    best=int(np.argmax(obs))
    nul=[]
    for _ in range(300):
        p=list(rng.permutation(oseq)); nul.append(max(lcs(seq_sets(i0,i0+3,5),p) for i0 in range(21)))
    print(other,'obs por bloque',obs,'mejor bloque',best,'(meses',best+1,'-',best+4,')',' nulo max-sobre-bloques: media',np.mean(nul),'p95',np.percentile(nul,95),'p(null>=obs max)',np.mean(np.array(nul)>=max(obs)))
print('--- UR009 vs UR021 y vs UR006 completo')
a9=[int(v) for v in q('UR009').valor if v>=5]; a21=[int(v) for v in q('UR021').valor if v>=5]; a6=[int(v) for v in d.valor if v>=5]
for nm,x,y in [('UR009-UR021',a9,a21),('UR009-UR006 completo',a9,a6),('UR021-UR006 completo',a21,a6)]:
    o=lcs(x,y); nul=[lcs(list(rng.permutation(x)),y) for _ in range(200)]
    print(nm,'LCS',o,'nulo media',np.mean(nul),'max',max(nul),'p',(np.sum(np.array(nul)>=o)+1)/201,'len',len(x),len(y))
# valores compartidos exactos (multiconjunto) UR009 con segmento
from collections import Counter
