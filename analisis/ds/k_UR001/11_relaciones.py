# -*- coding: utf-8 -*-
"""UR001. Relaciones de Ascher (sumas categoricas por color) y periodo robusto."""
import pandas as pd, numpy as np, json
r=pd.read_csv('analisis/ds/k_UR001/ur001_cuerdas.csv').sort_values('orden').reset_index(drop=True)
pend=r[r.nivel==0].sort_values('orden').reset_index(drop=True)
rng=np.random.default_rng(0); NPERM=1000

# ---- Ascher: suma categorica por color = alguna cuerda? ----
vals=set(int(v) for v in r.valor if v>0)
print('=== suma por color = valor de alguna cuerda? ===')
tot=0
for c,s in pend.groupby('color').valor.sum().items():
    if s>0 and int(s) in vals:
        # excluir la coincidencia trivial con su propia cuerda
        print(f'  color {c}: suma={int(s)} coincide con valor existente')
        tot+=1
print('coincidencias:',tot,'de',pend.color.nunique(),'colores')

# ---- misma prueba con nulo ----
def count_col_sum(df):
    v=set(int(x) for x in df.valor if x>0)
    n=0
    for c,s in df.groupby('color').valor.sum().items():
        if s>0 and int(s) in v: n+=1
    return n
obs=count_col_sum(pend)
null=np.array([count_col_sum(pend.assign(valor=rng.permutation(pend.valor.values))) for _ in range(NPERM)])
p=(np.sum(null>=obs)+1)/(NPERM+1)
print(f'  nulo: media={null.mean():.1f}; p={p:.3f}')

# ---- periodo robusto: nulo que preserva runs locales (bloques de 5) ----
col=pend.color.values
def match_lag(seq,P): return np.mean(seq[:-P]==seq[P:])
def block_shuffle(arr,bs=5):
    n=len(arr); idx=np.arange(n); blocks=[idx[i:i+bs] for i in range(0,n,bs)]
    order=rng.permutation(len(blocks)); out=np.concatenate([blocks[i] for i in order]); return arr[out]
print('\n=== periodo de color: nulo por bloques de 5 (preserva runs locales) ===')
for P in [12,15,16,17,18,19,20,34,35]:
    obs=match_lag(col,P)
    nulls=np.array([match_lag(block_shuffle(col),P) for _ in range(500)])
    p=(np.sum(nulls>=obs)+1)/501
    print(f'  lag {P}: obs={obs:.3f} nulo_bloque={nulls.mean():.3f} p={p:.3f}')

# ---- conjuntos de 3 valores (Urton labels): hay triples con 3er termino comun? ----
print('\n=== posible marca de "etiqueta": 3er valor en runs / repetidos exactos ===')
vv=pend[pend.valor>0]
cnt=vv.valor.value_counts()
dups=vv[vv.valor.isin(cnt[cnt>=3].index)]
print('valores con >=3 repeticiones:',sorted(set(int(v) for v in dups.valor)))

json.dump(dict(col_sum_obs=obs,col_sum_p=float(p)),open('analisis/ds/k_UR001/resultados_relaciones.json','w'),indent=1)
print('\n[ok]')
