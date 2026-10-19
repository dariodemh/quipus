import pandas as pd, numpy as np
pd.set_option('display.width', 240)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg == 'AS069'].copy().sort_values('orden').reset_index(drop=True)
gs = d.groupby('grupo').size()

# singletons
sing = d[d.grupo.isin(gs[gs==1].index)]
print("singletons n:", len(sing))
print("singleton color top:", sing.color.value_counts().head(15).to_dict())
print("singleton valor: con nudos:", sing.nudos.notna().sum(), " sin:", sing.nudos.isna().sum())
print("singleton valores !=0:", (sing.valor!=0).sum())
print("singleton valores repetidos top:", sing.valor.value_counts().head(10).to_dict())
print()
# compare singleton vs non-singleton colors
non = d[~d.grupo.isin(gs[gs==1].index)]
print("non-singleton color top:", non.color.value_counts().head(15).to_dict())
print()
# colors: how many white
print("W-only cuerdas:", (d.color=='W').sum(), "/", len(d))
# multi-color (contains / or : or -)
mc = d[d.color.str.contains(r'[/:\-]', na=False)]
print("cuerdas con color compuesto:", len(mc))
print("colores compuestos top:", mc.color.value_counts().head(10).to_dict())
print()
# values: distribution of nonzero values and their position within group of 7
print("--- valores !=0 por posicion dentro de grupo (grupos de 6-8) ---")
for sz in [6,7,8]:
    sub = d[d.grupo.isin(gs[gs==sz].index)].copy()
    sub['pos_in'] = sub.groupby('grupo').cumcount()
    posz = sub[sub.valor!=0].pos_in.value_counts().sort_index()
    print(f"grupo size {sz}: nonzero por posicion ->", posz.to_dict())
