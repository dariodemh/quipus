import pandas as pd, numpy as np
pd.set_option('display.width', 220)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg == 'AS069'].copy()
g = pd.read_csv('analisis/datos/grupos.csv')
gg = g[g.kfg == 'AS069'].copy()

# --- valores de las cuerdas CON nudos ---
kn = d[d.nudos.notna()].copy()
print("cuerdas con nudos:", len(kn), "/", len(d))
print("valor stats (con nudos):")
print(kn.valor.describe())
print("valores unicos con nudos:", kn.valor.nunique())
print("top valores frecuentes:")
print(kn.valor.value_counts().head(20).to_dict())
print()
# sin nudos
nn = d[d.nudos.isna()]
print("sin nudos valor unico:", nn.valor.unique()[:5], "n=", len(nn))
print()
# --- estructura de niveles ---
print("nivel 1 (subsidiarias):", (d.nivel==1).sum(), " nivel2:", (d.nivel==2).sum())
# cuerdas madre con subsidiarias
moms = d[d.nivel>0].padre.value_counts()
print("madres con subsidiarias:", len(moms), "max hijas:", moms.max())
print("distribucion n hijas:", moms.value_counts().sort_index().to_dict())
print()
# --- grupos ---
print("grupos.csv AS069 filas:", len(gg))
print(gg.head(20).to_string())
print("grupos con espacio distinto de 0 (separaciones):")
print(gg[gg.espacio_cm.notna() & (gg.espacio_cm>0)].head(20).to_string())
