# -*- coding: utf-8 -*-
"""Totales y subtotales CORRECTOS (sin deduplicar) y nulo por permutacion.
Estadistico X = nº de coincidencias cruzadas entre:
   - gran total (suma de toda cuerda con nudos) de A  ==  un valor de cuerda de B
   - suma de un grupo de A                           ==  un valor de cuerda de B
Nulo: barajar los valores dentro de cada quipu (mismas posiciones/niveles), 500.
"""
import pandas as pd, numpy as np, os
from collections import Counter
ROOT = r'.'
D = os.path.join(ROOT, 'analisis', 'datos')
RNG = np.random.default_rng(0); NREP = 500
c = pd.read_csv(os.path.join(D, 'cuerdas.csv'))
q = pd.read_csv(os.path.join(D, 'quipus.csv'))
KFG = q.loc[q['procedencia'].isin(['Nazca', 'Atarco']), 'kfg'].tolist()
s = c[c['kfg'].isin(KFG)].copy().sort_values(['kfg', 'orden'])
real = s['nudos'].notna() & (s['nudos'].astype(str).str.strip() != '')
s = s.assign(val=np.where(real, s['valor'], np.nan))

def build(df):
    """devuelve por quipu: total, valores de cuerda (reales), sumas de grupo."""
    tot={}; vals={}; gsum={}
    for k,d in df.groupby('kfg'):
        v = d['val'].dropna()
        tot[k]=float(v.sum()); vals[k]=sorted(v.astype(int).tolist())
        gsum[k]=[]
        for gid,dd in d.groupby('grupo'):
            gsum[k].append(float(dd['val'].dropna().sum()))
    return tot, vals, gsum

def cruces(tot, vals, gsum, thr=15):
    """pares (A,B) donde un subtotal de A (total o suma de grupo) == valor de B."""
    hits=[]
    for a in KFG:
        subs=[tot[a]]+[g for g in gsum[a] if g>0]
        for b in KFG:
            if a==b: continue
            vb=set(vals[b])
            for x in subs:
                if x>=thr and x in vb:
                    hits.append((a,int(x),b))
    return hits

tot, vals, gsum = build(s)
hits = cruces(tot, vals, gsum)
print('=== CRUCES subtotal(A) == valor de cuerda(B), umbral 15 ===')
for h in hits: print('   ', h)
print('obs =', len(hits))

# nulo: barajar valores dentro de cada quipu (permuta los 'val' no nulos)
null=[]
for r in range(NREP):
    df = s.copy()
    newv=[]
    for k,d in s.groupby('kfg'):
        idx=d.index
        vv=d['val'].values.copy()
        mask=~np.isnan(vv)
        vv[mask]=RNG.permutation(vv[mask])
        newv.append(pd.Series(vv,index=idx))
    df['val']=pd.concat(newv).sort_index()
    t2,v2,g2=build(df)
    null.append(len(cruces(t2,v2,g2)))
null=np.array(null)
print(f'nulo media={null.mean():.2f} max={null.max()} p={(1+(null>=len(hits)).sum())/(1+NREP):.4f}')

print('\n=== gran total por quipu (correcto) ===')
for k in KFG: print(f'   {k}: total={int(tot[k])}  n_cuerdas_reales={len(vals[k])}  sumas_grupo={[int(x) for x in gsum[k] if x>0]}')

# --- jerarquia interna: cord = suma de grupo? y cord = suma de hermanas? ---
print('\n=== cord cuya suma = grupo (candidato a "total" interno) ===')
for k,d in s.groupby('kfg'):
    npend=(d['nivel']==0).sum()
    for gid,dd in d.groupby('grupo'):
        gs=dd['val'].dropna().sum()
        for _,r in dd.iterrows():
            if pd.notna(r['val']) and r['val']>0 and abs(r['val']-gs)<1e-9 and (dd['val'].dropna()>0).sum()>1:
                print(f'   {k} grupo {gid}: cuerda {r["cuerda"]} = {int(r["val"])} = suma del grupo')
