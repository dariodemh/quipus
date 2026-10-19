# -*- coding: utf-8 -*-
"""UR113: sistema decimal (posiciones/direcciones), calidad de lectura y anomalias."""
import pandas as pd, numpy as np, re, os
BASE = r'.'; OUT = os.path.join(BASE, 'analisis', 'ds', 'k_UR113')
u = pd.read_csv(os.path.join(OUT, 'cuerdas_ur113.csv')); u['valor'] = u.valor.fillna(0)

# --- parsear nudos: 1S(4.5,Z),10 -> tipo, pos, dir, valor
pat = re.compile(r'(\d+)([A-Z]+)\(([\d.]+),([SZUR?])\)(?:,(-?\d+))?')
rows = []
for _, r in u[u.nudos.notna()].iterrows():
    for m in pat.finditer(str(r.nudos)):
        rows.append(dict(cuerda=r.cuerda, nivel=r.nivel, grupo=r.grupo, nk=int(m.group(1)),
                         tipo=m.group(2), pos=float(m.group(3)), direc=m.group(4),
                         aport=float(m.group(5) or 0), valor=r.valor))
k = pd.DataFrame(rows)
k['lugar'] = k.aport.apply(lambda a: 1 if a >= 1000 else 10 if a >= 100 else 1)
print('clusters parseados:', len(k), 'cuerdas con nudos:', k.cuerda.nunique())
print('\ndireccion por lugar decimal (1=unidades,10=decenas,100=centenas):')
print(pd.crosstab(k.lugar, k.direc).to_string())
print('\ntipo de nudo por lugar:')
print(pd.crosstab(k.lugar, k.tipo).to_string())
print('\ntipo x direccion:')
print(pd.crosstab(k.tipo, k.direc).to_string())
# consistencia: cuerdas con un solo lugar -> que direccion
print('\ncuerdas con un solo lugar decimal y su direccion:')
g = k.groupby('cuerda').agg(nlug=('lugar','nunique'), lugar=('lugar','first'), direc=('direc','first'))
print(g[g.nlug==1].groupby(['lugar','direc']).size().to_string())
# excepciones: decenas en S o unidades en Z
bad = k[((k.lugar>=10)&(k.direc=='S')) | ((k.lugar==1)&(k.direc=='Z'))]
print('\nexcepciones (decenas S o unidades Z):', len(bad), 'de', len(k), '=', round(len(bad)/len(k),4))
print(bad.groupby(['lugar','direc']).size().to_string())
print(bad.groupby('grupo').size().sort_values(ascending=False).head(8).to_string())
# valores: digitos
def dig(v):
    return [int(c) for c in str(int(v))][::-1]  # unidades primero
u['ndig'] = u.valor.apply(lambda v: len(str(int(v))) if v>0 else 0)
print('\nnumero de digitos (colgantes):', u[u.nivel==0].ndig.value_counts().sort_index().to_dict())
print('numero de digitos (subs):', u[u.nivel>0].ndig.value_counts().sort_index().to_dict())
print('\nultimo digito de los colgantes:', u[u.nivel==0].valor[u[u.nivel==0].valor>0].apply(lambda v:int(v)%10).value_counts().sort_index().to_dict())
print('ultimo digito de las subsidiarias:', u[u.nivel>0].valor[u[u.nivel>0].valor>0].apply(lambda v:int(v)%10).value_counts().sort_index().to_dict())
print('\nmultiplos de 10: colgantes', int(((u.nivel==0)&(u.valor>0)&(u.valor%10==0)).sum()), '/', int(((u.nivel==0)&(u.valor>0)).sum()),
      '; subs', int(((u.nivel>0)&(u.valor>0)&(u.valor%10==0)).sum()), '/', int(((u.nivel>0)&(u.valor>0)).sum()))
# anomalias
print('\nunion V / torsion U / terminacion rara:')
print(u[(u.union=='V')|(u.torsion!='S')][['cuerda','nivel','grupo','valor','color','torsion','union','largo','terminacion','nudos']].to_string(index=False))
print('\nvalores alt distintos de valor:', u.alt.notna().sum())
