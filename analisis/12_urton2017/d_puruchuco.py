# Puruchuco (cap. 5): jerarquia de tres niveles, copias, segmento introductorio
from util import *
rng=np.random.default_rng(12017)
P={k:pend(k) for k in ['UR063','UR064','UR066','UR067','UR068','UR073']}
V={k:P[k].valor.values.astype(int) for k in P}
print({k:len(v) for k,v in V.items()})
# D1 copias nivel II y III
def match(a,b,off=0):
    n=min(len(a),len(b)-off); return int(np.sum(a[:n]==b[off:off+n])),n
for a,b in [('UR066','UR067'),('UR064','UR068')]:
    m,n=match(V[a],V[b]); 
    # valores mayores (>=5) exactos
    sa=[(i,v) for i,v in enumerate(V[a]) if v>=5]; same=sum(1 for i,v in sa if i<len(V[b]) and V[b][i]==v)
    nul=[]
    for _ in range(2000):
        x=rng.permutation(V[a][:n]); nul.append(np.sum(x==V[b][:n]))
    print(a,b,'posiciones iguales',m,'de',n,' valores>=5 iguales',same,'de',len(sa),' nulo media',np.mean(nul),'max',max(nul))
print('UR066',V['UR066'].tolist()); print('UR067',V['UR067'].tolist()); print('UR064',V['UR064'].tolist()); print('UR068',V['UR068'].tolist())
# D2 segmento introductorio: posiciones de cuerdas con nudos en las primeras 16
for k in ['UR064','UR066','UR067','UR068','UR063','UR073']:
    p=P[k]; pos=[i+1 for i in range(min(16,len(p))) if p.valor[i]>0]
    typ=[str(p.nudos[i])[:2]+str(p.nudos[i])[2] for i in range(min(16,len(p))) if p.valor[i]>0]
    print(k,'cuerdas con valor en las 16 primeras:',pos,[str(p.nudos[i-1])[:8] for i in pos])
# frecuencia del patron en el corpus: exactamente 3 cuerdas con nudos entre las primeras 12 (posiciones 1,7,9) todas figura de ocho valor 1
hits=[]
for k,dd in C.groupby('kfg'):
    p=dd[dd.nivel==0].reset_index(drop=True)
    if len(p)<12: continue
    f=p.valor[:12].values
    if list(np.nonzero(f)[0]+1)==[1,7,9] and all(f[[0,6,8]]==1): hits.append(k)
print('quipus con 3 nudos(valor1) exactamente en cuerdas 1,7,9 de las 12 primeras:',hits)
hits2=[]
for k,dd in C.groupby('kfg'):
    p=dd[dd.nivel==0].reset_index(drop=True)
    if len(p)<12: continue
    f=p.valor[:14].values
    nz=list(np.nonzero(f)[0]+1)
    if len(nz)==3 and all(f[np.array(nz)-1]==1) and nz[1]-nz[0]==6 and nz[2]-nz[1]==2: hits2.append((k,nz))
print('patron 1,+6,+2 (cualquier inicio) entre las 14 primeras:',hits2)
# D3 UR068 -> UR067 sumas
b=V['UR068']; a=V['UR067']; a66=V['UR066']
S1=b[13:33];S2=b[33:53];S3=b[53:73]
tot=S1+S2+S3
print('UR068 S1+S2+S3 vs UR067 cuerdas 13-32')
print(list(zip(tot.tolist(),a[12:32].tolist(),a66[12:32].tolist())))
ex=np.sum(tot==a[12:32]); ex66=np.sum(tot==a66[12:32]); print('exactas UR067',ex,'/20  UR066',ex66,'/20; discrepancias UR067:',[(int(t),int(x)) for t,x in zip(tot,a[12:32]) if t!=x])
big=[i for i in range(20) if tot[i]>=5]
print('de las',len(big),'columnas con suma>=5 coinciden con UR067:',int(np.sum(tot[big]==a[12:32][big])))
nul=[]
for _ in range(5000):
    s=[rng.permutation(S) for S in (S1,S2,S3)]; t=s[0]+s[1]+s[2]; nul.append(np.sum(t[big]==a[12:32][big]) if True else 0)
print('nulo (permutar cada seccion de UR068): media',np.mean(nul),'max',max(nul))
# D4 UR063 -> UR068 S2
v63=V['UR063']; bigs=[i for i,v in enumerate(v63) if v>=100]; print('cuerdas>=100 en UR063 (indice 1-based):',[i+1 for i in bigs],[int(v63[i]) for i in bigs],'suma',v63[bigs].sum(),' UR068 cuerda 50=',b[49])
cols=[]
for o in range(-16,4):
    idx=[i+o for i in bigs if 0<=i+o<len(v63)]
    cols.append(int(v63[idx].sum()))
tgt=S2.tolist()
print('sumas columna UR063 (alineado por cuerda grande)',cols); print('UR068 S2 (cuerdas 34-53)           ',tgt)
ex=[(c,t) for c,t in zip(cols,tgt)]
print('exactas',sum(c==t for c,t in ex),'/20; con |dif|<=1:',sum(abs(c-t)<=1 for c,t in ex),' (valores>=5 exactas:',sum(c==t for c,t in ex if t>=5),'de',sum(t>=5 for c,t in ex),')')
# nulo: permutar valores de UR063 conservando cuerdas-grandes? aqui permutar todo
nul=[];nul2=[]
for _ in range(5000):
    x=rng.permutation(v63)
    idxs=[i for i,v in enumerate(v63) if v>=100]  # misma alineacion fija
    c=[int(x[[i+o for i in idxs if 0<=i+o<len(x)]].sum()) for o in range(-16,4)]
    nul.append(sum(cc==t for cc,t in zip(c,tgt) if t>=5))
print('nulo (permutar UR063, alineacion fija): media exactas(>=5)',np.mean(nul),'P(>=obs)',np.mean(np.array(nul)>=sum(c==t for c,t in ex if t>=5)))
# totales
print({k:int(V[k].sum()) for k in V}, 'UR063+UR073',V['UR063'].sum()+V['UR073'].sum())
print('--- extra')
def lcs(a,b):
    m=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            m[i][j]=m[i-1][j-1]+1 if a[i-1]==b[j-1] else max(m[i-1][j],m[i][j-1])
    return m[-1][-1]
for a,b in [('UR063','UR073'),('UR064','UR068'),('UR066','UR067')]:
    x=[int(v) for v in V[a] if v>=5]; y=[int(v) for v in V[b] if v>=5]
    o=lcs(x,y); nul=[lcs(list(rng.permutation(x)),y) for _ in range(300)]
    print(a,b,'LCS valores>=5:',o,'de',len(x),len(y),' nulo media',np.mean(nul),'max',max(nul))
print('UR063 y UR073: valores>=100 compartidos',sorted(set(int(v) for v in V['UR063'] if v>=100)&set(int(v) for v in V['UR073'] if v>=100)))
# patron: exactamente 3 cuerdas con valor 1 y nada mas en las 12 primeras
c=0;tot=0;ex=[]
for k,dd in C.groupby('kfg'):
    p=dd[dd.nivel==0].reset_index(drop=True)
    if len(p)<20: continue
    tot+=1; f=p.valor[:12].values
    if np.count_nonzero(f)==3 and set(f[f>0])=={1}: c+=1; ex.append(k)
print('quipus con >=20 pendientes:',tot,' con exactamente 3 cuerdas de valor 1 y ninguna otra en las 12 primeras:',c, ex[:30])
