"""UR1032 — aritmetica interna + nulso (permutacion dentro del quipu, semilla 0)."""
import pandas as pd, numpy as np
rng = np.random.default_rng(0)
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden').reset_index(drop=True)

# --- 1. colgante = suma de subsidiarias ---
madres = s[(s.nivel == 0) & s.cuerda.isin(s[s.nivel == 1].padre)]
filas = []
for _, m in madres.iterrows():
    subs = s[s.padre == m.cuerda]
    filas.append((m.cuerda, m.valor, subs.valor.sum(), len(subs), m.color))
df = pd.DataFrame(filas, columns=['cuerda', 'valor', 'suma_sub', 'n_sub', 'color'])
igual = (df.valor == df.suma_sub)
print('== colgante vs suma de subsidiarias ==')
print('madres con subsidiarias:', len(df), '| coincidencias exactas:', int(igual.sum()),
      f'({100*igual.mean():.1f}%)')
print(df[~igual].head(20).to_string())

# colgante == subsidiaria mas grande? colgante >= suma?
print('valor madre cuando coincide:', df.loc[igual, 'valor'].value_counts().to_dict())
print('cuando NO coincide, suma_sub:', df.loc[~igual, 'suma_sub'].value_counts().to_dict())

# --- 2. sumas de grupo ---
s['grupo'] = s.grupo.astype(int)
grp = s[s.nivel == 0].groupby('grupo').valor.agg(['sum', 'count', 'max', 'mean'])
print('\n== sumas de grupo (colgantes) ==')
print('suma por grupo describe:'); print(grp['sum'].describe())
print('grupos con suma 0:', int((grp['sum'] == 0).sum()), 'de', len(grp))
print('sumas top:'); print(grp['sum'].sort_values(ascending=False).head(15).to_dict())

# --- 3. razones / valores repetidos entre grupos adyacentes ---
sumas = grp['sum'].values
print('\ngrupo suma total quipu:', sumas.sum())

# --- 4. color: alternancia dentro de grupo ---
print('\n== color por posicion dentro del grupo (colgantes) ==')
col = s[s.nivel == 0].copy()
col['pos'] = col.groupby('grupo').cumcount()
print(col.groupby('pos').color.value_counts().head(20).to_dict())
