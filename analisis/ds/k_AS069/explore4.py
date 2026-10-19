import pandas as pd, numpy as np
pd.set_option('display.width', 240); pd.set_option('display.max_rows', 200)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg == 'AS069'].copy().sort_values('orden').reset_index(drop=True)

# grupo sizes
gs = d.groupby('grupo').size()
print("distribucion tamano de grupo:", gs.value_counts().sort_index().to_dict())
print("grupos con 7 cuerdas:", (gs==7).sum(), " con 1:", (gs==1).sum(), " con 6:", (gs==6).sum())
print()
# sequence of group sizes (first 40)
print("tamano por grupo (primeros 60):", gs.values[:60].tolist())
print()
# grupos grandes
print("grupos con >=12 cuerdas:", gs[gs>=12].to_dict())
print()
# colors within a 7-group (grupo 2 = orden 3..9)
for gr in [2,4,6,8]:
    sub = d[d.grupo==gr]
    print(f"grupo {gr}:", list(zip(sub.orden.tolist(), sub.color.tolist(), sub.valor.tolist())))
