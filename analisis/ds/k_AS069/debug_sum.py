import pandas as pd, numpy as np
pd.set_option('display.width', 200)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
print("target cords:")
for nm in ['p1332','p1329','p940','p1138','p1154']:
    row = d[d.cuerda==nm]
    if len(row): print(nm, "orden", int(row.orden.iloc[0]), "valor", row.valor.iloc[0], "grupo", row.grupo.iloc[0])
print()
# where is value 17? list cords with value 17 and their order
v17 = d[d.valor==17]
print("cords con valor 17: orden", v17.orden.tolist())
print()
# print window around p1332 (search orden)
t = d[d.cuerda=='p1332']
o = int(t.orden.iloc[0]); print("p1332 orden", o)
print(d[(d.orden>=o-8)&(d.orden<=o+3)][['orden','cuerda','color','valor','grupo']].to_string())
