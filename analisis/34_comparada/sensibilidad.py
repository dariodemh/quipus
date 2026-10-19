"""Sensibilidad (fuera de la familia Holm). Semilla fija."""
import csv, collections, numpy as np
rng = np.random.default_rng(20261018)
D='analisis/datos/'
C=list(csv.DictReader(open(D+'cuerdas.csv',encoding='utf-8')))
Q={r['kfg']:r['procedencia'] for r in csv.DictReader(open(D+'quipus.csv',encoding='utf-8'))}
G={r['kfg']:r['genero'] for r in csv.DictReader(open('analisis/28_atlas_generos/atlas.csv',encoding='utf-8'))}
grp=collections.defaultdict(lambda: collections.defaultdict(list))
for x in C:
    if x['nivel']=='0': grp[x['kfg']][int(x['grupo'])].append(int(float(x['valor'] or 0)))
# (a) digito de unidades solo valores >=10
dig=collections.defaultdict(lambda: np.zeros(10))
for q in grp:
    for g in grp[q].values():
        for v in g:
            if v>=10: dig[Q.get(q)][v%10]+=1
for l,t in dig.items():
    if t.sum()>=300: print('digito>=10',l,int(t.sum()),'p0=%.3f'%(t[0]/t.sum()),'p5=%.3f'%(t[5]/t.sum()))
# (b) totales: por quipu, sin ARC
res=collections.defaultdict(lambda:[0,0,0])
for q,gs in grp.items():
    for v in gs.values():
        w=[a for a in v if a>0]
        if len(w)>=3:
            for i,a in enumerate(w):
                if a==sum(w)-a:
                    r=res[q]; r[0]+=i==0; r[1]+=i==len(w)-1; r[2]+=1; break
for excl in (False,True):
    qs=[q for q in res if not(excl and G.get(q)=='ARC')]
    f=sum(res[q][0]>res[q][1] for q in qs); l=sum(res[q][1]>res[q][0] for q in qs); t=sum(res[q][0]==res[q][1] for q in qs)
    print('sin ARC' if excl else 'todos','quipus',len(qs),'mayoria primero',f,'mayoria ultimo',l,'empate',t,
          'totales primero',sum(res[q][0] for q in qs),'ultimo',sum(res[q][1] for q in qs),'total',sum(res[q][2] for q in qs))
print('ARC quipus con totales', [(q,res[q]) for q in res if G.get(q)=='ARC'][:30])
print('Incahuasi', {q:res[q] for q in res if Q.get(q)=='Incahuasi'})
# (c) esperado y p exacto (Poisson-binomial por simulacion) sin ARC
ns=[]
for q,gs in grp.items():
    if G.get(q)=='ARC': continue
    for v in gs.values():
        w=[a for a in v if a>0]
        if len(w)>=3 and any(a==sum(w)-a for a in w): ns.append(len(w))
ns=np.array(ns); sim=np.array([(rng.integers(0,ns)==0).sum() for _ in range(5000)])
print('sin ARC: totales',len(ns),'esperado primero/ultimo=%.1f'%(1/ns).sum(),'P(sim>=27)=%.3f'%((sim>=27).mean()),'P(sim<=25)=%.3f'%((sim<=25).mean()))
