"""UR1032 — buscar suma posicion-a-posicion estilo AS215 (grupo = suma de grupos)."""
import pandas as pd, numpy as np, re
C=pd.read_csv('analisis/datos/cuerdas.csv')
s=C[C.kfg=='UR1032'].copy().sort_values('orden').reset_index(drop=True)
col=s[s.nivel==0].copy()
col['size']=col.groupby('grupo')['grupo'].transform('size')
col['pos']=col.groupby('grupo').cumcount()

# matrices por color (tamano)
def mat(size, npos):
    ids=[g for g,sb in col.groupby('grupo') if len(sb)==size]
    M=np.zeros((len(ids),npos))
    for i,g in enumerate(ids):
        M[i,:len(col[col.grupo==g])]=col[col.grupo==g].sort_values('pos').valor.values
    return ids, M

bid,B=mat(5,5); wid,W=mat(3,3)
print('grupos azules:',len(bid),'| blancos:',len(wid))
print('suma total azul:',B.sum(),'| blanca:',W.sum(),'| quipu:',B.sum()+W.sum())
print('B sums:',dict(zip(bid,B.sum(1).astype(int))))
print('W sums:',dict(zip(wid,W.sum(1).astype(int))))

def test_shift(M, k, step, name):
    rng=np.random.default_rng(0)
    n=len(M)
    def stat(Mx):
        hit=0; tot=0
        for i in range(n):
            idx=[i+step*(j+1) for j in range(k)]
            if max(idx)<n:
                tot+=1
                if np.array_equal(Mx[i], Mx[idx].sum(0)): hit+=1
        return hit, tot
    h,t=stat(M)
    # nulo: permutar valores de todas las celdas dentro de cada columna? mejor: permutar filas de valores
    cnt=0; N=1000
    flat=M.copy()
    for _ in range(N):
        Mp=M.copy()
        for c in range(M.shape[1]):
            Mp[:,c]=rng.permutation(Mp[:,c])
        hh,_=stat(Mp)
        if hh>=h: cnt+=1
    print(f'{name}: {h}/{t} exactos, p_emp={cnt/N:.3f}')

print('\n== sumas de k grupos del mismo color (paso 2), posicion a posicion ==')
test_shift(B,5,2,'B: g = suma de 5 azules siguientes')
test_shift(B,3,2,'B: g = suma de 3 azules siguientes')
test_shift(W,5,2,'W: g = suma de 5 blancos siguientes')
test_shift(W,3,2,'W: g = suma de 3 blancos siguientes')

# suma escalar: algun grupo = suma de k grupos del mismo color
print('\n== igualdad escalar: grupo = suma de k grupos mismo color (ventana/aleatorio) ==')
def scalar_test(M, k, name, trials=5000):
    rng=np.random.default_rng(0); n=len(M); sums=M.sum(1)
    # ventana consecutiva de k grupos del mismo color hacia atras
    win=0; tot=0
    for i in range(k,n):
        tot+=1
        if abs(sums[i]-sums[i-k:i].sum())<1e-9: win+=1
    # base rate por azar
    cnt=0
    for _ in range(trials):
        idx=rng.choice([j for j in range(n)],k,replace=False)
        pass
    from itertools import combinations
    # base rate teorica: prob de que suma de k al azar == sums[i]
    hit=0; N=2000
    for _ in range(N):
        i=rng.integers(n)
        comb=rng.choice([j for j in range(n) if j!=i], k, replace=False)
        if abs(sums[i]-sums[list(comb)].sum())<1e-9: hit+=1
    print(f'{name}: ventana exacta {win}/{tot}; azar {hit}/{N} ({hit/N:.3f})')
scalar_test(B,5,'azules k=5'); scalar_test(B,3,'azules k=3')
scalar_test(W,5,'blancos k=5'); scalar_test(W,3,'blancos k=3')
