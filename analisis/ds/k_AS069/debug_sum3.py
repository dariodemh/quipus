import sqlite3, pandas as pd, numpy as np
pd.set_option('display.width',200)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
print("orden 616-624:")
print(d[(d.orden>=616)&(d.orden<=624)][['orden','cuerda','grupo','valor','color']].to_string())
print()
# grupo 344 layout
print("grupo 344:")
print(d[d.grupo==344][['orden','cuerda','valor']].to_string())
print()
# Now use GRUPO as cluster, position = orden - min(orden in grupo)
d['pos_in'] = d.orden - d.groupby('grupo').orden.transform('min')
def val_at(g,p):
    r=d[(d.grupo==g)&(d.pos_in==p)]
    return r.valor.iloc[0] if len(r) else None
# test indexed example: target [45?] we only have grupo... try: is there a group whose index-4 cord =12 from groups 18,20,22,23 index 4?
for g in [18,20,22,23]:
    print("grupo",g,"size",(d.grupo==g).sum(),"pos4 val", val_at(g,4))
