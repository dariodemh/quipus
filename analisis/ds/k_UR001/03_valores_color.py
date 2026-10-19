# -*- coding: utf-8 -*-
"""UR001. Distribucion de valores, cuerdas grandes, color vs grupo, estructura del arbol."""
import pandas as pd, numpy as np, json
D='analisis/datos/'
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
rng=np.random.default_rng(0); NPERM=1000

print('=== valores >0: cuantiles ===')
v=r[r.valor>0].valor
for q in [0.5,0.75,0.9,0.95,0.99]: print(f'  q{int(q*100)}: {v.quantile(q):.0f}')
print('  max 10 valores:', sorted(r.valor.unique())[-10:])

print('\n=== 12 cuerdas de mayor valor ===')
print(r.sort_values('valor',ascending=False)[['cuerda','nivel','grupo','valor','nudos','color','union']].head(12).to_string(index=False))

print('\n=== valor por nivel ===')
print(r.groupby('nivel').valor.agg(['count','sum','median','max']).to_string())

# % de cuerdas por nivel sin nudos
print('\n=== sin nudos por nivel ===')
print(r.assign(sn=r.nudos.isna()).groupby('nivel').sn.agg(['sum','count','mean']).to_string())

# ===== color vs grupo: homogeneidad de color dentro de grupo =====
pend=r[r.nivel==0].sort_values('orden')
def homog(df, key):
    tot=0; same=0
    for g,sub in df.groupby(key):
        c=sub.color.tolist(); tot+=len(c)
        same+=sum(1 for i in range(1,len(c)) if c[i]==c[i-1])
    return same
obs=homog(pend,'grupo')
# nulo: barajar asignacion de grupo
null=[]
arr=pend.grupo.values.copy()
for _ in range(NPERM):
    p2=pend.copy(); p2['grupo']=rng.permutation(arr)
    null.append(homog(p2,'grupo'))
null=np.array(null)
p=(np.sum(null>=obs)+1)/(NPERM+1)
print(f'\n=== color constante dentro de grupo ===')
print(f'pares adyacentes mismo color: obs={obs}/{len(pend)-1}; nulo media={null.mean():.0f}; p={p:.3f}')

# tambien: moda de color por grupo
top_color=pend.groupby('grupo').color.agg(lambda s:s.mode().iloc[0])
print('grupos cuyo color modal domina (>80%):', sum(pend.groupby("grupo").color.apply(lambda s:(s==s.mode().iloc[0]).mean()>0.8)))

# ===== tamanos de los grupos grandes =====
print('\n=== grupos grandes (n colgantes) ===')
for g,n in pend.groupby('grupo').size().sort_values(ascending=False).head(8).items():
    sub=pend[pend.grupo==g]
    print(f'  grupo {g}: {n} colgantes, colores={sub.color.value_counts().head(4).to_dict()}, sub={r[r.padre.isin(sub.cuerda)].shape[0]}')

# ===== estructura: cuerdas sin nudos (posibles "etiquetas"/separadores) =====
sn=r[r.nudos.isna()]
print(f'\n=== {len(sn)} cuerdas sin nudos: por nivel {sn.nivel.value_counts().to_dict()}')
print('  union:', sn.union.value_counts().to_dict())
# son madres?
subs_of_sn = r[r.padre.isin(sn.cuerda)].shape[0]
print(f'  {sn.cuerda.isin(r.padre.dropna()).sum()} de ellas son madres de {subs_of_sn} cuerdas')

json.dump(dict(color_grupo=dict(obs=int(obs),null=float(null.mean()),p=float(p)),
               grandes={int(k):int(v) for k,v in pend.grupo.value_counts().items()}),
          open('analisis/ds/k_UR001/resultados_estructura.json','w'),indent=1)
print('\n[ok]')
