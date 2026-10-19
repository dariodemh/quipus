# Santa (cap. 12): UR087-UR092, grupos de seis (reconstruccion de 05), sumas por posicion, pachacas, posicion 1 vs resto
from util import *
from scipy import stats
rng=np.random.default_rng(12017)
g6=pd.read_csv('./analisis/05_etnohistoria/santa_grupos6.csv')
rows=[]
for k,x in g6.groupby('kfg',sort=False):
    p=pend(k); names=p.cuerda.tolist()
    for r in x.itertuples():
        i=names.index(r.first); v=p.valor.values[i:i+6].astype(int); 
        if len(v)==6: rows.append([k,r.g]+v.tolist())
A=pd.DataFrame(rows,columns=['kfg','g','p1','p2','p3','p4','p5','p6'])
print('grupos',len(A),A.groupby('kfg').size().to_dict(),' (Urton 48/9/34/17/15/10 =133)')
s=A[['p1','p2','p3','p4','p5','p6']].sum().tolist(); print('sumas por posicion KFG:',s,' | Urton: 359(+broken ->367/8),1512,434,4876,611,616')
print('p1 por quipu:',A.groupby('kfg').p1.sum().to_dict(),' rango p1',A.p1.min(),A.p1.max())
print('posicion 4 es el maximo del grupo en',np.mean(A.p4>=A[['p1','p2','p3','p5','p6']].max(axis=1)),' (excluyendo grupos todo cero:',np.mean((A.p4>=A[['p1','p2','p3','p5','p6']].max(axis=1))[A[['p1','p2','p3','p4','p5','p6']].sum(axis=1)>0]),')')
print('grupos con todo 0:',int((A[['p1','p2','p3','p4','p5','p6']].sum(axis=1)==0).sum()))
# p1 vs resto
nz=A[A[['p2','p3','p4','p5','p6']].sum(axis=1)>0]
rs=[]
for k,x in nz.groupby('kfg'):
    if len(x)<8 or x.p1.nunique()<2: continue
    r,p=stats.spearmanr(x.p1,x[['p2','p3','p4','p5','p6']].sum(axis=1))
    nul=[stats.spearmanr(rng.permutation(x.p1.values),x[['p2','p3','p4','p5','p6']].sum(axis=1))[0] for _ in range(2000)]
    rs.append((k,len(x),round(r,3),(np.sum(np.abs(nul)>=abs(r))+1)/2001))
print(pd.DataFrame(rs,columns=['kfg','n','rho_p1_vs_resto','p_perm']).to_string())
# pairing pachacas ~ khipus por rango (tabla 12.3)
trib=np.array([19,23,9,7,41,32]); gr=np.array([15,17,10,9,48,34])
print('Spearman tributarios vs grupos (emparejamiento de Urton):',stats.spearmanr(trib,gr)[0],' suma |dif|',np.abs(trib-gr).sum())
# nulo: composiciones aleatorias uniformes de 133 en 6 partes; distancia tras emparejar por rango
def comp(n,k):
    cuts=np.sort(rng.choice(np.arange(1,n),k-1,replace=False)); return np.diff(np.concatenate([[0],cuts,[n]]))
d0=np.abs(np.sort(trib)-np.sort(gr)).sum()
nul=[np.abs(np.sort(trib)-np.sort(comp(133,6))).sum() for _ in range(20000)]
print('suma|dif| tras ordenar: observada',d0,' P(nulo<=obs) composiciones uniformes:',np.mean(np.array(nul)<=d0),' mediana nulo',np.median(nul))
# nulo con tamanos tipo "seisenas" de quipus reales: remuestreo de los 6 conteos con reposicion de {48,9,34,17,15,10}? no aplica.
print('nombres tributarios en Apendice A (a mano del texto): ver informe')
A.to_csv('santa_grupos_posiciones.csv',index=False)
# pos 5/6 ~ poblacion 5 x 132 = 660: probabilidad de que alguna de las 6 columnas quede tan cerca de un objetivo arbitrario
cols=np.array(s,float); obsd=min(abs(np.log(c/660)) for c in cols[[4,5]]); anyd=min(abs(np.log(c/660)) for c in cols)
T=np.exp(rng.uniform(np.log(100),np.log(5000),100000)); dmin=np.min(np.abs(np.log(cols[None,:]/T[:,None])),axis=1)
print('columna 5/6 a %.1f%% de 660; P(alguna de las 6 columnas a <= esa distancia de un objetivo log-uniforme 100-5000) = %.3f'%(100*(np.exp(obsd)-1),np.mean(dmin<=obsd)))
print('empates de 4 estaciones: columnas',cols.tolist())
