# -*- coding: utf-8 -*-
"""Inspeccion de candidatos concretos + nulos correctos.
"""
import pandas as pd, numpy as np, os
ROOT = r'.'
D = os.path.join(ROOT, 'analisis', 'datos')
RNG = np.random.default_rng(0)
c = pd.read_csv(os.path.join(D, 'cuerdas.csv'))
q = pd.read_csv(os.path.join(D, 'quipus.csv'))
KFG = q.loc[q['procedencia'].isin(['Nazca', 'Atarco']), 'kfg'].tolist()
s = c[c['kfg'].isin(KFG)].copy().sort_values(['kfg', 'orden'])
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 50)

def pend(d):
    return d[d['nivel'] == 0].sort_values('orden')

# --- corrida larga UR028 vs UR113 ---
def longrun(a, b):
    best = (0, None, None)
    for i in range(len(a) - 1):
        for j in range(len(b) - 1):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i+k] == b[j+k]:
                k += 1
                if k > best[0]:
                    best = (k, i, j)
    return best
va = pend(s[s['kfg'] == 'UR028'])['valor'].astype(int).tolist()
vb = pend(s[s['kfg'] == 'UR113'])['valor'].astype(int).tolist()
print('UR028 seq:', va[:80])
print('UR113 seq (primeros 60):', vb[:60])
print('longrun UR028-UR113:', longrun(va, vb))

# --- UR028 total 220: donde esta en UR113 y UR1140 ---
print('\n--- UR028 total =', sum(va), '---')
for kk in ['UR113', 'UR1140']:
    d = s[s['kfg'] == kk]
    # valor exacto
    ex = d[(d['valor'].abs() == sum(va))][['cuerda', 'nivel', 'valor', 'color', 'nudos']]
    print(kk, 'valores exactos 220:'); print(ex.to_string())
    # suma de grupo
    for gid, dd in d.groupby('grupo'):
        if int(dd.loc[dd['valor'] > 0, 'valor'].sum()) == sum(va):
            print(f'  {kk} grupo {gid} suma=220, cuerdas={dd["cuerda"].tolist()[:6]}...')

# --- UR114 total 147 en UR1136 ---
print('\n--- UR114 total =', sum(pend(s[s["kfg"]=="UR114"])["valor"].astype(int)), 'en UR1136 ---')
d = s[s['kfg'] == 'UR1136']
print(d[(d['valor'] == 147)][['cuerda', 'nivel', 'valor', 'color']].to_string())
for gid, dd in d.groupby('grupo'):
    if int(dd.loc[dd['valor'] > 0, 'valor'].sum()) == 147:
        print(f'  grupo {gid} suma=147: {dd["cuerda"].tolist()}')

# --- UR057 total 61 en UR1140 y UR122 ---
print('\n--- UR057 total =', sum(pend(s[s["kfg"]=="UR057"])["valor"].astype(int)), '---')
for kk in ['UR1140', 'UR122']:
    d = s[s['kfg'] == kk]
    ex = d[(d['valor'] == 61)][['cuerda', 'nivel', 'valor', 'color']]
    print(kk, 'valor 61:'); print(ex.to_string())

# --- UR040 total 76 en AS215 (que tiene cuerdas superiores) ---
print('\n--- UR040 total = 76; AS215 vmax=76 ---')
d = s[s['kfg'] == 'AS215']
print(d[d['valor'] == 76][['cuerda', 'nivel', 'valor', 'union', 'color']].to_string())

# --- UR1032 total 37 ---
print('\n--- UR1032 total =', sum(pend(s[s["kfg"]=="UR1032"])["valor"].astype(int)), '---')
for kk in ['AS215', 'UR1140']:
    d = s[s['kfg'] == kk]
    print(kk, d[d['valor'] == 37][['cuerda', 'nivel', 'valor']].to_string())

# --- nulo para "suma de grupo de A = suma de grupo de B" (invariante parcial) ---
print('\n=== NULO: coincidencias de subtotales de grupo entre quipus ===')
def grupos_sums(kk):
    d = s[s['kfg'] == kk]
    return [int(dd.loc[dd['valor'] > 0, 'valor'].sum()) for _, dd in d.groupby('grupo')]
gs = {k: grupos_sums(k) for k in KFG}
def n_cross(gs):
    hits=0
    ks=list(gs)
    for a in ks:
        for b in ks:
            if a==b: continue
            for v in gs[a]:
                if v>0 and v in gs[b]:
                    hits+=1
    return hits
obs = n_cross(gs)
print('obs coincidencias de suma-de-grupo entre quipus:', obs)

print('\n--- valores identicos de colgante compartidos entre quipus (invariante) ---')
allp = {k: set(pend(s[s['kfg']==k])['valor'].astype(int)) - {0} for k in KFG}
cnt=0
pairs=[]
ks=list(KFG)
for i in range(len(ks)):
    for j in range(i+1,len(ks)):
        inter = allp[ks[i]] & allp[ks[j]]
        if inter:
            cnt+=len(inter)
            pairs.append((ks[i],ks[j],len(inter),sorted(inter)))
print('pares con valores compartidos:',len(pairs),'total valores:',cnt)
for p in sorted(pairs,key=lambda x:-x[2])[:8]: print('  ',p)
