import pandas as pd, numpy as np
pd.set_option('display.width', 250)
c = pd.read_csv('analisis/datos/cuerdas.csv')
g = pd.read_csv('analisis/datos/grupos.csv')
u = c[c.kfg=='UR1057'].copy()
gu = g[g.kfg=='UR1057'].copy()

print("=== GRUPOS (pos_cm, desde-hasta) ===")
print(gu.to_string(index=False))

# merge
m = gu.merge(u.groupby('grupo').agg(n=('cuerda','size'),
        n0=('nivel', lambda s:(s==0).sum()),
        nsub=('nivel', lambda s:(s>0).sum()),
        sum0=('valor','sum'), max0=('valor','max')), left_on='grupo', right_index=True)
print("\n=== group sizes ===")
print(m[['grupo','pos_cm','desde','hasta','espacio_cm','n','n0','nsub','sum0','max0']].to_string(index=False))
print("\nsize counts:", m.n0.value_counts().sort_index().to_dict())
print("pos gaps:", np.round(np.diff(gu.pos_cm.values),2)[:60])
