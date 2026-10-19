# Pachacamac (cap. 6): totales del apendice, seis pares "closely matching" (Tabla 6.1), estadisticos del corpus
from util import *
rng=np.random.default_rng(12017)
ids=("UR1097 UR1099 AS101_Part_1 AS101_Part_2 UR1102 UR1104 AS110 AS111 AS112 UR1118 UR1119 UR1121 AS125 UR1131 AS134 AS139 UR1144 UR1145 UR1151 AS156 AS158 UR1163 UR1165 UR1167 AS170 AS172 UR1175 AS187 AS188 AS189 UR115 UR1095 UR1096 UR123 UR124 UR126 UR1034 AS075 HP001 HP002 HP003 "
 "HP004 HP005 HP006 HP007 HP008 HP009 HP010 HP011 HP012 HP013 HP014 HP017 HP018 HP019 HP020 HP021 HP022 HP023 HP024 HP025 HP026 HP027 HP028 HP029 HP030 HP031 HP032 UR196 UR197 UR199 UR200 UR201 UR202 UR208 UR212 UR213 UR214 UR216 UR218 UR226 UR230 UR243 UR245 UR244 UR246 UR247 UR248 UR249 UR253 UR254").split()
vals=[131,15505,2100,1340,665,205515,424,1085,10,56189,105947,122,48362,10449,239,4027,8148,19088,228,3846,149,274,473,1275,35108,74376,11979,302,593,290,190,9694,437,1164,754,190,2570,573,28040,29080,5023,
 1344,1177,1941,6718,2690,497,63409,14856,3496,414,1107,4386,434,31,91,3501,314,1271,1277,0,0,198386,0,16404,52916,76,149,410,23594,1627,43860,73402,4679,7138,6533,9267,73,1931,8282,12019,830,439,34,401,2281,76343,42824,47809,865,625]
assert len(ids)==91==len(vals)
tot=C.groupby('kfg').valor.sum()
rows=[]
for i,v in zip(ids,vals):
    k=tot.get(i,np.nan); rows.append((i,v,k, 'ok' if k==v else ('ausente' if np.isnan(k) else 'dif')))
T=pd.DataFrame(rows,columns=['id','total_urton','total_kfg','estado']); 
print(T.estado.value_counts().to_dict())
print(T[T.estado!='ok'].to_string())
print('exactos entre los presentes: %d de %d'%((T.estado=='ok').sum(),(T.estado!='ausente').sum()))
T.to_csv('pachacamac_totales.csv',index=False)
# estadisticos del corpus
v=np.array(vals,float); print('mediana',np.median(v),'media',v.mean(),'(Urton 1,486 y 15,610); max',v.max(),'min',v.min())
kk=[i for i in ids if i in tot.index]
sub=[(C[(C.kfg==i)&(C.nivel>=1)].shape[0]>0) for i in kk]; print('con subsidiarias',np.mean(sub),'(Urton 67%)')
sizes=[]
for i in kk:
    gg=G[G.kfg==i]; sizes+= (gg.hasta-gg.desde+1).astype(int).tolist()
from collections import Counter
print('tamano de grupo mas comunes',Counter(sizes).most_common(8),' (Urton: 5:169, 3:144, 1:116, 2:80, 4:79, 6:74)')
# Tabla 6.1 pares
pairs=[('UR1131','UR1095'),('UR1144','UR218'),('UR1151','AS189'),('UR1096','UR196'),('HP018','UR243'),('UR226','UR230')]
def lcs(a,b):
    m=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            m[i][j]=m[i-1][j-1]+1 if a[i-1]==b[j-1] else max(m[i-1][j],m[i][j-1])
    return m[-1][-1]
out=[]
for a,b in pairs:
    da,db=q(a),q(b)
    pa,pb=da[da.nivel==0],db[db.nivel==0]
    x=[int(w) for w in da.valor if w>=3]; y=[int(w) for w in db.valor if w>=3]
    o=lcs(x,y); nul=[lcs(list(rng.permutation(x)),y) for _ in range(200)]
    # multiconjunto de valores>=3 compartidos
    ca,cb=Counter(x),Counter(y); sh=sum((ca&cb).values())
    out.append(dict(a=a,b=b,pend_a=len(pa),pend_b=len(pb),subs_a=len(da)-len(pa),subs_b=len(db)-len(pb),tot_a=int(da.valor.sum()),tot_b=int(db.valor.sum()),lcs=o,n_a=len(x),n_b=len(y),nulo_media=round(np.mean(nul),1),nulo_max=max(nul),p=round((np.sum(np.array(nul)>=o)+1)/201,4),compartidos=sh))
O=pd.DataFrame(out); print(O.to_string()); O.to_csv('pachacamac_pares.csv',index=False)
print('--- correlacion posicional de pendientes (Spearman) y de colores')
from scipy import stats
rr=[]
for a,b in pairs+[('UR053B','UR053C')]:
    pa=pend(a).valor.values; pb=pend(b).valor.values
    n=min(len(pa),len(pb))
    r,p=stats.spearmanr(pa[:n],pb[:n])
    # nulo: permutar pb
    nul=[stats.spearmanr(pa[:n],rng.permutation(pb[:n]))[0] for _ in range(500)]
    ca=pend(a).color.values[:n]; cb=pend(b).color.values[:n]; col=np.mean(ca==cb)
    nulc=np.mean([np.mean(ca==rng.permutation(cb)) for _ in range(500)])
    rr.append((a,b,n,round(r,3),round((np.sum(np.abs(nul)>=abs(r))+1)/501,4),round(col,2),round(nulc,2)))
print(pd.DataFrame(rr,columns=['a','b','n','spearman_pos','p_perm','frac_color_igual','color_nulo']).to_string())
print('--- pares de Pachacamac con igual numero de pendientes y total a +-10%')
kk=[i for i in ids if i in tot.index and tot[i]>0]
npd={i:int((q(i).nivel==0).sum()) for i in kk}
cand=[]
for i in range(len(kk)):
    for j in range(i+1,len(kk)):
        a,b=kk[i],kk[j]
        if npd[a]==npd[b] and abs(np.log(tot[a]/tot[b]))<=np.log(1.1): cand.append((a,b,npd[a],int(tot[a]),int(tot[b])))
print(len(cand),'pares (de',len(kk)*(len(kk)-1)//2,')'); print(cand)
eq=sum(1 for i in range(len(kk)) for j in range(i+1,len(kk)) if npd[kk[i]]==npd[kk[j]]); print('pares con igual numero de pendientes:',eq)
