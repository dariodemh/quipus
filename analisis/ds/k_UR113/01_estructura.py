# -*- coding: utf-8 -*-
"""UR113 (KH0349, Nazca, Goteborg): reconstruccion estructural."""
import pandas as pd, numpy as np, json, os

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
c = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'), dtype={'kfg': str})
g = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'grupos.csv'), dtype={'kfg': str})
u = c[c.kfg == 'UR113'].copy()
for col in ['valor', 'orden', 'nivel', 'grupo', 'largo']:
    u[col] = pd.to_numeric(u[col], errors='coerce')
u = u.sort_values('orden').reset_index(drop=True)
u['sin_nudo'] = u.nudos.isna()
u.to_csv(os.path.join(OUT, 'cuerdas_ur113.csv'), index=False)

gu = g[g.kfg == 'UR113'].copy()
print('grupos.csv cols:', list(g.columns))
print(gu.to_string())
gu.to_csv(os.path.join(OUT, 'grupos_ur113.csv'), index=False)

# --- por grupo ---
rows = []
for gi, sub in u.groupby('grupo'):
    p = sub[sub.nivel == 0]
    s = sub[sub.nivel > 0]
    rows.append(dict(grupo=gi, n=len(sub), pend=len(p), subs=len(s), nivel2=(sub.nivel == 2).sum(),
                     nivel3=(sub.nivel == 3).sum(),
                     suma_pend=p.valor.sum(), suma_todo=sub.valor.sum(),
                     pend_sin_nudo=p.sin_nudo.sum(), subs_sin_nudo=s.sin_nudo.sum(),
                     pend_val0=(p.valor == 0).sum(),
                     color_pend='|'.join(p.color.fillna('NA')),
                     union_pend='|'.join(p.union.fillna('NA')),
                     largo_pend=round(p.largo.sum(), 1),
                     subs_por_pend=round(len(s)/max(len(p), 1), 2)))
res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUT, 'por_grupo.csv'), index=False)
print(res[['grupo', 'n', 'pend', 'subs', 'nivel2', 'suma_pend', 'pend_sin_nudo', 'subs_por_pend']].to_string(index=False))
print('\nTOTAL pend', len(u[u.nivel == 0]), 'subs', len(u[u.nivel > 0]), 'suma pend', u[u.nivel == 0].valor.sum())

# --- estructura jerarquica: cuantas subsidiarias por madre ---
pend = u[u.nivel == 0]
hijos = u[u.nivel > 0].groupby('padre').size()
print('\nmadres con hijas:', len(hijos), 'max hijas:', hijos.max())
print('distribucion hijas:', hijos.value_counts().sort_index().to_dict())
print('\nsubs por nivel de madre:', u[u.nivel > 0].groupby('nivel').size().to_dict())
# profundidad
def name2ord(n):
    return n
print('\ncuerdas nivel>=2:')
print(u[u.nivel >= 2][['orden', 'cuerda', 'nivel', 'padre', 'valor', 'nudos', 'color', 'union', 'largo']].to_string(index=False))

# --- colores: transiciones y repeticion ---
print('\ncolores distintos nivel0:', pend.color.nunique(), 'nivel1:', u[u.nivel == 1].color.nunique())
print(pend.color.value_counts().head(20).to_string())
print('\ntorsion por nivel:', u.groupby('nivel').torsion.value_counts().to_dict())
print('union por nivel:', u.groupby('nivel').union.value_counts().to_dict())
print('\nnotas no nulas:', u.notas.notna().sum())
print(u[u.notas.notna()][['orden', 'cuerda', 'notas']].head(20).to_string(index=False))
