"""UR004 - reconstruccion estructural. Escribe resumen a 01_estructura.txt"""
import pandas as pd, numpy as np, io, re, sys

D = 'analisis/datos'
cords = pd.read_csv(f'{D}/cuerdas.csv')
gr = pd.read_csv(f'{D}/grupos.csv')
q = pd.read_csv(f'{D}/quipus.csv')

u = cords[cords.kfg == 'UR004'].copy()
g = gr[gr.kfg == 'UR004'].copy()
meta = q[q.kfg == 'UR004'].iloc[0]

out = io.StringIO()
def P(*a):
    print(*a); print(*a, file=out)

P('=== UR004 METADATOS ===')
P(meta.to_dict())
P()
P('=== CUERDAS ===')
P('total', len(u), '| nivel:', u.nivel.value_counts().to_dict())
P('union:', u.union.value_counts().to_dict())
P('torsion:', u.torsion.value_counts().to_dict())
P('terminacion:', u.terminacion.value_counts().to_dict())
u['has'] = u.nudos.notna()
P('sin nudos', int((~u.has).sum()), 'con nudos', int(u.has.sum()))
P('largo: min %.1f max %.1f mediana %.1f' % (u.largo.min(), u.largo.max(), u.largo.median()))
P()
P('=== GRUPOS ===')
P('n grupos', len(g))
g2 = g.copy()
g2['n'] = g2.hasta - g2.desde + 1
P('grupos de 1 cuerda:', int((g2.n == 1).sum()), '| de >1:', int((g2.n > 1).sum()))
P('tamano grupo: min', g2.n.min(), 'max', g2.n.max(), 'mediana', g2.n.median())
P('suma cuerdas en grupos:', int(g2.n.sum()))
# clasificar grupos de 1 cuerda
u_idx = u.set_index('orden')
singles = g2[g2.n == 1]
sing_colors = [u_idx.loc[r.desde, 'color'] for _, r in singles.iterrows()]
sing_union = [u_idx.loc[r.desde, 'union'] for _, r in singles.iterrows()]
P('grupos de 1 cuerda por color:', pd.Series(sing_colors).value_counts().to_dict())
P('grupos de 1 cuerda por union:', pd.Series(sing_union).value_counts().to_dict())
P()
# marcar PK como "marcador"
u['marcador'] = (u.color == 'PK') | (u.terminacion == 'K')
P('cuerdas color PK:', int((u.color == 'PK').sum()))
P('PK con valor!=0:', int(((u.color == 'PK') & (u.valor != 0)).sum()))
P()
P('=== SUBSIDIARIAS ===')
sub = u[u.nivel > 0]
P('n subsidiarias', len(sub), '| por nivel', sub.nivel.value_counts().to_dict())
madres = sub.padre.value_counts()
P('madres con subsidiarias:', len(madres), '| max subs de una madre', int(madres.max()))
# profundidad 2
P('subs nivel2:', sub[sub.nivel == 2].cuerda.tolist())
P()
P('=== COLORES (todos) ===')
P(u.color.value_counts().to_dict())
P()
P('=== VALORES (con nudos) ===')
vv = u[u.has]['valor']
P('n', len(vv), 'min', vv.min(), 'max', vv.max(), 'media %.1f' % vv.mean(), 'mediana %.1f' % vv.median())
P('cuantiles', {k: float(vv.quantile(k)) for k in [.25, .5, .75, .9, .99]})
P('valores repetidos top:', u[u.has]['valor'].value_counts().head(15).to_dict())
P('valor 0 sin nudos:', int(((u.valor == 0) & (~u.has)).sum()))
P()
P('=== DIRECCIONES DE NUDO (de cadena nudos) ===')
dirs = u[u.has].nudos.str.findall(r'\(([\d.]+),([SZU])\)')
allt = []
for lst in dirs:
    for _, d in lst:
        allt.append(d)
P('direcciones:', pd.Series(allt).value_counts().to_dict())
P('nudos por cuerda: max', int(u[u.has].nudos.str.count(';').add(1).max()))
P()
P('=== union x nivel ===')
P(pd.crosstab(u.nivel, u.union).to_string())
P('=== color x union ===')
P(pd.crosstab(u.color, u.union).to_string())

with open('analisis/ds/k_UR004/01_estructura.txt', 'w', encoding='utf-8') as f:
    f.write(out.getvalue())
print('WROTE 01_estructura.txt')
