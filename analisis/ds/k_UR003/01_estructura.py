# -*- coding: utf-8 -*-
"""UR003 (Leymebamba, KH0239): reconstruccion estructural. Salida -> estructura_out.txt"""
import pandas as pd, re, io, sys

d = pd.read_csv('analisis/datos/cuerdas.csv', dtype={'nudos': str})
u = d[d.kfg == 'UR003'].copy().sort_values('orden').reset_index(drop=True)
g = pd.read_csv('analisis/datos/grupos.csv')
gu = g[g.kfg == 'UR003'].copy()

out = []
def P(*a):
    s = ' '.join(str(x) for x in a)
    out.append(s); print(s)

# --- jerarquia ---
P('=== UR003: resumen ===')
P('total cuerdas', len(u))
P('por nivel:\n', u.nivel.value_counts().sort_index().to_string())
P('por grupo (cuerdas totales):\n', u.grupo.value_counts().sort_index().to_string())

# colgantes por grupo
colg = u[u.nivel == 0]
P('\ncolgantes por grupo:\n', colg.grupo.value_counts().sort_index().to_string())

# --- por grupo: colgantes, subs, suma de valores de colgantes, valor total grupo ---
P('\n=== por grupo: n_colg, n_subs, suma_valor_colgantes, suma_valor_total, min/max valor colg ===')
for gi in sorted(u.grupo.unique()):
    sub = u[u.grupo == gi]
    cg = sub[sub.nivel == 0]
    P(f'g{gi:>2}: colg={len(cg):>3} subs={len(sub)-len(cg):>3} '
      f'sum_colg={cg.valor.sum():>6.0f} sum_tot={sub.valor.sum():>6.0f} '
      f'val_colg[min,max]=[{cg.valor.min():.0f},{cg.valor.max():.0f}]')

P('\nsuma colgantes total =', colg.valor.sum())
P('suma todas las cuerdas =', u.valor.sum())

# --- union ---
P('\n=== union por nivel ===')
P(u.groupby(['nivel', 'union']).size().unstack(fill_value=0).to_string())
P('\ncolgantes (nivel0) union counts:\n', colg.union.value_counts(dropna=False).to_string())
P('\ncuerdas union R (posicion en grupo):')
for _, r in u[u.union == 'R'].iterrows():
    P(f"  orden={r.orden} {r.cuerda} nivel={r.nivel} grupo={r.grupo} valor={r.valor:.0f} color={r.color}")

# --- colores ---
P('\n=== color base (sin combinaciones ":","-","/") top ===')
base = u.color.fillna('NA').str.split(r'[:\-/]').str[0]
P(base.value_counts().head(20).to_string())

# --- valores ---
P('\n=== distribucion de valores (todas) ===')
P(u.valor.value_counts().sort_index().to_string())
P('\nvalores colgantes:\n', colg.valor.value_counts().sort_index().to_string())

# --- torsion, terminacion ---
P('\ntorsion:\n', u.torsion.value_counts(dropna=False).to_string())
P('\nterminacion:\n', u.terminacion.value_counts(dropna=False).to_string())

# --- cuerdas sin nudos ---
P('\nsin nudos (nudos vacio):', u.nudos.isna().sum())
syn = u[u.nudos.isna()]
P('sin nudos por nivel:\n', syn.nivel.value_counts().sort_index().to_string())
P('sin nudos con valor>0:', (syn.valor > 0).sum())
P('con nudos pero valor=0:', ((u.nudos.notna()) & (u.valor == 0)).sum())

# --- guardar tabla completa ordenada a texto ---
with open('analisis/ds/k_UR003/estructura_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

# volcar tabla por cordon para inspeccion manual
cols = ['orden', 'cuerda', 'nivel', 'padre', 'grupo', 'valor', 'nudos', 'color', 'torsion', 'union', 'largo', 'terminacion']
u[cols].to_csv('analisis/ds/k_UR003/ur003_cuerdas_orden.csv', index=False)
print('\n[ok] escritos estructura_out.txt y ur003_cuerdas_orden.csv')
