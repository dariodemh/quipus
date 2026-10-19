# -*- coding: utf-8 -*-
"""UR003: controles nulos para los patrones aritmeticos detectables (estilo KFG).
Nulo: barajar el vector de valores entre las 758 cuerdas (preservando la estructura
de arbol), 1000 iteraciones, semilla 0. Salida -> nulos_out.txt"""
import pandas as pd, numpy as np
rng = np.random.default_rng(0)
d = pd.read_csv('analisis/datos/cuerdas.csv', dtype={'nudos': str})
u = d[d.kfg == 'UR003'].copy().sort_values('orden').reset_index(drop=True)
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); out.append(s); print(s)

# --- estructura ---
child = {k: list(v['cuerda']) for k,v in u[u.padre.notna()].groupby('padre')}
def descendants(name):
    res=[]; st=[name]
    while st:
        n=st.pop()
        for c in child.get(n,[]): res.append(c); st.append(c)
    return res

# subarbol completo (yo + todos los descendientes)
def subtree(name):
    return [name]+descendants(name)

# grupos -> lista de colgantes (orden) y todas las cuerdas por grupo (por subarbol de cada colgante)
grupos = sorted(u.grupo.unique())
pend_by_grupo = {g: u[(u.grupo==g)&(u.nivel==0)].sort_values('orden').cuerda.tolist() for g in grupos}
tree_by_grupo = {g: [subtree(p) for p in pend_by_grupo[g]] for g in grupos}
allcords_by_grupo = {g: u[u.grupo==g].cuerda.tolist() for g in grupos}

V0 = u.set_index('cuerda').valor.to_dict()

def analyze(vals):
    """devuelve dict de conteos de relaciones dada una asignacion de valores {cuerda:valor}"""
    res={}
    # A) madre (colgante con hijas) == suma de sus hijas directas
    a=0; an=0
    for _,r in u.iterrows():
        ch=child.get(r['cuerda'],[])
        if ch:
            an+=1
            if abs(sum(vals[c] for c in ch)-vals[r['cuerda']])<1e-9: a+=1
    res['A_madre_suma_hijas']=(a,an)
    # A2) colgante == suma de todos sus descendientes
    a2=0
    for _,r in u[u.nivel==0].iterrows():
        de=descendants(r['cuerda'])
        if de and abs(sum(vals[c] for c in de)-vals[r['cuerda']])<1e-9: a2+=1
    res['A2_colg_suma_descend']=a2
    # B) cluster con split equilibrado: prefijo == sufijo (sobre valores de colgantes)
    b=0; bdet=[]
    for g in grupos:
        seq=[vals[c] for c in pend_by_grupo[g]]
        tot=sum(seq)
        if tot==0: continue
        for k in range(1,len(seq)):
            if abs(sum(seq[:k])-sum(seq[k:]))<1e-9 and sum(seq[:k])>0:
                b+=1; bdet.append((g,k)); break
    res['B_split_equilibrado']=(b,tuple(bdet))
    # C) pares de clusters con suma total (subarboles) igual y >0
    sums={g: sum(vals[c] for c in allcords_by_grupo[g]) for g in grupos}
    nz=[g for g in grupos if sums[g]>0]
    c=0
    for i in range(len(nz)):
        for j in range(i+1,len(nz)):
            if abs(sums[nz[i]]-sums[nz[j]])<1e-9: c+=1
    res['C_pares_clusters_iguales']=c
    # E) clusters seriados (secuencia de colgantes monotona no-dec o no-inc)
    e=0
    for g in grupos:
        seq=[vals[c] for c in pend_by_grupo[g]]
        if len(seq)<2: continue
        nd=all(seq[i]<=seq[i+1] for i in range(len(seq)-1))
        ni=all(seq[i]>=seq[i+1] for i in range(len(seq)-1))
        if nd or ni: e+=1
    res['E_clusters_seriados']=e
    # D) indexed: un colgante cuyo valor == suma de colgantes en la MISMA posicion de >=2 otros clusters
    # (posicion = ordinal entre colgantes del cluster)
    pos_vals={}  # (g,pos)->valor
    for g in grupos:
        for i,c in enumerate(pend_by_grupo[g]): pos_vals[(g,i)]=vals[c]
    d_=0; ddet=[]
    for g in grupos:
        for i,c in enumerate(pend_by_grupo[g]):
            v=vals[c]
            if v<=0: continue
            others=[pos_vals[(h,i)] for h in grupos if h!=g and i<len(pend_by_grupo[h])]
            runners=[x for x in others if x>0]
            # buscar >=2 sumandos positivos que sumen v
            found=False
            for a in range(len(runners)):
                for b2 in range(a+1,len(runners)):
                    if abs(runners[a]+runners[b2]-v)<1e-9: found=True;break
                if found:break
            if found: d_+=1; ddet.append((g,i,v))
    res['D_indexed_2sumandos']=(d_,tuple(ddet[:6]))
    return res

obs = analyze(V0)
P('=== VALORES OBSERVADOS ===')
for k,v in obs.items(): P(' ',k,'=',v)

# --- nulo ---
Varr = u.valor.values.copy()
names = u.cuerda.values
N=1000
null = {k:[] for k in ['A_madre_suma_hijas','A2_colg_suma_descend','B_split_equilibrado','C_pares_clusters_iguales','E_clusters_seriados','D_indexed_2sumandos']}
for it in range(N):
    perm = rng.permutation(Varr)
    vals = dict(zip(names, perm))
    r = analyze(vals)
    for k in null: null[k].append(r[k] if not isinstance(r[k],tuple) else r[k][0])
P('\n=== NULO (N=1000, semilla 0): media / max / p(sup) ===')
def psup(o,arr):
    arr=np.array(arr); return (1+(arr>=o).sum())/(N+1)
obsc={'A_madre_suma_hijas':obs['A_madre_suma_hijas'][0],'A2_colg_suma_descend':obs['A2_colg_suma_descend'],
      'B_split_equilibrado':obs['B_split_equilibrado'][0],'C_pares_clusters_iguales':obs['C_pares_clusters_iguales'],
      'E_clusters_seriados':obs['E_clusters_seriados'],'D_indexed_2sumandos':obs['D_indexed_2sumandos'][0]}
rows=[]
for k in obsc:
    arr=np.array(null[k]); o=obsc[k]
    p=psup(o,arr); rows.append((k,o,arr.mean(),arr.max(),p))
for k,o,m,mx,p in rows:
    P(' %-26s obs=%-4d nulo_media=%.2f nulo_max=%.0f p=%.4f'%(k,o,m,mx,p))
# Holm
ps=sorted([(p,k) for k,o,m,mx,p in rows])
m_=len(ps); holm={}
prev=0
for i,(p,k) in enumerate(ps):
    adj=min(1,(m_-i)*p); adj=max(adj,prev); prev=adj; holm[k]=adj
P('\nHolm:')
for k in obsc: P('  %-26s p=%.4f  Holm=%.4f'%(k,[p for kk,o,m,mx,p in rows if kk==k][0],holm[k]))

with open('analisis/ds/k_UR003/nulos_out.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('\n[ok] nulos_out.txt')
