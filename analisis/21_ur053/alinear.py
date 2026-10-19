# UR053A–E: extrae tríos (W, R, AB) en cualquier formato y alinea pares de quipus por LCS con nulo de barajado
import pandas as pd, re, numpy as np, itertools
rng=np.random.default_rng(20261018)
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
def norm(s): s=re.sub(r'\([^)]*\)','',str(s)); return 'R' if s.startswith('R') else s
def trios(q):
    g=c[c.kfg==q].copy(); g['col']=g.color.map(norm)
    sub={r.padre:r.valor for r in g[g.nivel==1].itertuples() if r.col=='AB'}
    p=g[g.nivel==0]; out=[]; L=list(zip(p.cuerda,p.col,p.valor))
    for i in range(len(L)-1):
        if L[i][1]=='W' and L[i+1][1]=='R':
            ab=sub.get(L[i+1][0])
            if ab is None and i+2<len(L) and L[i+2][1]=='AB': ab=L[i+2][2]
            out.append((L[i][2],L[i+1][2],ab))
    return out
T={q:trios(q) for q in ['UR053A','UR053B','UR053C','UR053D','UR053E']}
for q,t in T.items(): print(q,len(t),t[:4])
def lcs(a,b,eq):
    n,m=len(a),len(b); D=np.zeros((n+1,m+1),int)
    for i in range(n):
        for j in range(m):
            D[i+1,j+1]=D[i,j]+1 if eq(a[i],b[j]) else max(D[i,j+1],D[i+1,j])
    # reconstruir
    i,j,pares=n,m,[]
    while i and j:
        if eq(a[i-1],b[j-1]) and D[i,j]==D[i-1,j-1]+1: pares.append((a[i-1],b[j-1])); i-=1; j-=1
        elif D[i-1,j]>=D[i,j-1]: i-=1
        else: j-=1
    return D[n,m], pares[::-1]
eq=lambda x,y: x[0]==y[0] and abs(x[1]-y[1])<=1   # W exacto, R ±1
rows=[]
for a,b in itertools.combinations(T,2):
    o,pares=lcs(T[a],T[b],eq)
    nul=np.array([lcs(list(rng.permutation(np.array(T[a],dtype=object))),T[b],eq)[0] for _ in range(1000)])
    abeq=sum(1 for x,y in pares if x[2] is not None and y[2] is not None and abs(x[2]-y[2])<=1)
    rows.append((a,b,len(T[a]),len(T[b]),o,nul.mean(),(nul>=o).mean(),abeq))
    print(f'{a}-{b}: LCS={o} nulo={nul.mean():.1f} p={(nul>=o).mean()+1/1001:.4f}  AB coincide(±1) en {abeq}/{o}')
pd.DataFrame(rows,columns=['a','b','na','nb','lcs','nulo','p','ab_coincide']).to_csv('analisis/21_ur053/alineamientos.csv',index=False)
o,pares=lcs(T['UR053B'],T['UR053C'],eq)
for x,y in pares: print('  B',x,'  C',y)
