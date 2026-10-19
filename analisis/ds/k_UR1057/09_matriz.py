import pandas as pd, numpy as np, sqlite3
n=pd.read_csv('analisis/ds/k_UR1057/pendientes_estructurado.csv')
c=pd.read_csv('analisis/datos/cuerdas.csv'); u=c[c.kfg=='UR1057']
sub=u[u.cuerda.str.match(r'p\d+s1$') & (u.color.astype(str).str.contains('0G'))].copy()
sub['madre']=sub.padre
M=pd.DataFrame(index=range(1,25),columns=pd.MultiIndex.from_product([range(1,6),range(1,5)]),dtype=float)
for r in n[n.sg>0].itertuples(): M.loc[r.grupo_a,(r.sg,r.pos)]=r.valor
# 4a celda de sg5 = subsidiaria estructural
n0=u[u.nivel==0].sort_values('orden').reset_index(drop=True)
name2grp={}
for g in range(1,25):
    pass
# mapear madre -> grupo via nombre de madre en pendientes
for r in sub.itertuples():
    row=n[n.cuerda==r.madre]
    if len(row)==1: M.loc[int(row.grupo_a.iloc[0]),(5,4)]=r.valor
print('NaN en la retícula:',int(M.isna().sum().sum()))
print('celdas:',M.shape)
M.to_csv('analisis/ds/k_UR1057/matriz_24x5x4.csv')
print('escrita')
print(M.iloc[:, :8].head(4).to_string())
