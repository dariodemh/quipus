import pandas as pd, numpy as np
c = pd.read_csv('analisis/datos/cuerdas.csv')
g = pd.read_csv('analisis/datos/grupos.csv')
u = c[c.kfg=='UR1057'].copy()
gu = g[g.kfg=='UR1057'].copy()

print("=== GROUP SIZES ===")
sz = u.groupby('grupo').size()
print(sz.values)
print("total", sz.sum(), "n groups", len(sz))
print("=== cords per group (count) description ===")
print(sz.describe())

print("\n=== union by nivel ===")
print(u.groupby(['nivel','union']).size())

print("\n=== union T present? ===")
print(u[u.union=='T'].shape[0])

print("\n=== VALUES (nivel0) ===")
v0 = u[u.nivel==0].valor
print("count", len(v0), "zeros", (v0==0).sum(), "nonzero", (v0>0).sum())
print(v0.describe())
print("max", v0.max(), "min", v0.min())

print("\n=== columns with no knots (nudos NaN) ===")
print((u.nudos.isna()).sum(), "de", len(u))
print("value distribution of no-knot cords:", u[u.nudos.isna()].valor.value_counts().to_dict())

print("\n=== list grupos with sizes+sum of nivel0 valores ===")
rows=[]
for gr, sub in u.groupby('grupo'):
    n0 = sub[sub.nivel==0]
    rows.append((gr, len(sub), (sub.nivel>0).sum(), n0.valor.sum(), n0.valor.max()))
df=pd.DataFrame(rows, columns=['grupo','n','nsubs','sumv0','maxv0'])
print(df.to_string())
