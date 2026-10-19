# -*- coding: utf-8 -*-
"""Paso 3: descubrir la regla con que KFG asigna el valor de cada racimo.
Para cada racimo S, place = contribucion / n. Tabular por numero de racimos S,
posicion entre los S, y tipos debajo.
"""
import pandas as pd, numpy as np
from collections import Counter
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_lecturas.pkl")

rows=[]
for _,r in df[df.n_rac>0].iterrows():
    ks=r.knots
    tipos=[k['tipo'] for k in ks]
    m=sum(t=='S' for t in tipos)
    js=0
    for i,k in enumerate(ks):
        contrib = k['val']
        if contrib is None: continue
        if k['tipo']=='S':
            js+=1
            rows.append((r.kfg,r.cuerda,len(ks),m,js,tipos[-1],contrib/k['n'] if k['n'] else np.nan, r.imposible))
t=pd.DataFrame(rows,columns=['kfg','cuerda','K','m','j','ultimo','place','imposible'])
print("racimos S:",len(t))
print("\nplace mas comun por (m,j), solo no imposibles:")
print(t[~t.imposible].groupby(['m','j']).place.agg(lambda s:s.value_counts().index[0]).head(20).to_string())
print("\nplace por (m,j) y ultimo tipo (no imp):")
print(t[~t.imposible].groupby(['m','j','ultimo']).place.agg(['median','count']).head(30).to_string())
print("\ncasos m=1, j=1, place=100 (no imp):")
print(t[(~t.imposible)&(t.m==1)&(t.j==1)&(t.place==100)][['kfg','cuerda','K','ultimo']].head(10).to_string())
print("\ncasos m=1, j=1, place=10 (no imp):")
print(t[(~t.imposible)&(t.m==1)&(t.j==1)&(t.place==10)][['kfg','cuerda','K','ultimo']].head(10).to_string())
# cuantas cords normales tienen S y L
print("\nCombinaciones de tipos (no imp), top:")
print(Counter(''.join(sorted(set(''.join(k['tipo'] for k in ks)))) for ks in df[~df.imposible].knots if ks).most_common(10))
t.to_csv(BASE + r"\analisis\ds\n_nudos_imposibles\places_S.csv",index=False)
