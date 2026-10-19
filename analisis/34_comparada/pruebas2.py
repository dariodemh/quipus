"""Segunda ronda; ver adenda de diseno_previo.md. Semilla fija. Desde la raiz del repo."""
import csv, collections, numpy as np
rng = np.random.default_rng(20261018)
D='analisis/datos/'
C=list(csv.DictReader(open(D+'cuerdas.csv',encoding='utf-8')))
Q={r['kfg']:r['procedencia'] for r in csv.DictReader(open(D+'quipus.csv',encoding='utf-8'))}
grp=collections.defaultdict(lambda: collections.defaultdict(list))
for x in C:
    if x['nivel']=='0': grp[x['kfg']][int(x['grupo'])].append(int(float(x['valor'] or 0)))
NR=5000; P={}
def taus(M):  # M: (g,n) -> tau por fila, vectorizado
    n=M.shape[1]; iu=np.triu_indices(n,1)
    return np.sign(M[:,iu[1]]-M[:,iu[0]]).sum(1)/(n*(n-1)/2)
def by_n(gs):
    d=collections.defaultdict(list)
    for w in gs: d[len(w)].append(w)
    return {n:np.array(v) for n,v in d.items()}
def stats(B,rng=None):
    T=[];F=[]
    for n,M in B.items():
        if rng is not None: M=np.take_along_axis(M,rng.random(M.shape).argsort(1),1)
        T.append(taus(M)); mx=M.max(1); F.append((M[:,0]==mx)&((M==mx[:,None]).sum(1)==1))
    return np.concatenate(T).mean(), np.concatenate(F).mean()
def has_total(w): return any(a==sum(w)-a for a in w)
G5=[]
for q,gs in grp.items():
    if Q.get(q)=='Incahuasi': continue
    for v in gs.values():
        w=[a for a in v if a>0]
        if len(w)>=4 and len(set(w))>=3 and not has_total(w): G5.append(w)
B=by_n(G5); obs,omax=stats(B); nt=[];nm=[]
for _ in range(NR):
    t,f=stats(B,rng); nt.append(t); nm.append(f)
nt=np.array(nt);nm=np.array(nm)
P['P5a_tau_corpus_sin_Incahuasi']=(((nt<=obs).sum()+1)/(NR+1),f'grupos={len(G5)}; tau medio={obs:.3f}; nulo={nt.mean():.3f} sd {nt.std():.3f}')
P['P5c_maximo_primero']=(((nm>=omax).sum()+1)/(NR+1),f'{omax:.3f} vs nulo {nm.mean():.3f}')
rows=[[a for a in g if a>0] for g in grp['UR278'].values()]
rows=[r for r in rows if len(r)==9]
BR=by_n(rows); o=stats(BR)[0]; n=[stats(BR,rng)[0] for _ in range(NR)]
n=np.array(n); P['P5b_UR278_columnas_decrecientes']=(((n<=o).sum()+1)/(NR+1),f'filas={len(rows)}; tau medio={o:.3f}; nulo={n.mean():.3f}')
# P6
cells=np.array(rows)
H=np.array([[a for a in g if a>0][0] for g in grp['UR266'].values() if any(a>0 for a in g) and [a for a in g if a>0][0]>=100])
def st(cm):
    k=0; ex=0
    for r in cm:
        S=r.sum(); d=np.abs(H-S)
        if (d==0).any(): ex+=1; continue
        if any(np.isin(d,r)): k+=1
    return k,ex
k,ex=st(cells); nl=[]
for _ in range(NR):
    c2=np.column_stack([rng.permutation(cells[:,j]) for j in range(9)]); nl.append(st(c2)[0])
nl=np.array(nl)
P['P6_error_omision_partida']=(((nl>=k).sum()+1)/(NR+1),f'filas={len(cells)}; exactas={ex}; no exactas con cabecera a +-celda={k}; nulo={nl.mean():.2f}')
# Holm sobre 11
old=[(r['prueba'],float(r['p']),r['detalle']) for r in csv.DictReader(open('analisis/34_comparada/resultados_pruebas.csv',encoding='utf-8'))]
allp=old+[(k,v[0],v[1]) for k,v in P.items()]
it=sorted(allp,key=lambda t:t[1]); m=len(it); run=0; out=[]
for i,(k,p,d) in enumerate(it):
    run=max(run,min(1,(m-i)*p)); out.append((k,p,run,d))
with open('analisis/34_comparada/resultados_pruebas_ronda2.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['prueba','p','p_holm_11','detalle']); w.writerows(out)
for r in out: print(r[0],round(r[1],4),round(r[2],4),r[3][:120])
