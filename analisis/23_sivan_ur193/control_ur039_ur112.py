# Mismo control en los quipus de calibración (UR039) y réplica ciega (UR112) de Sivan, con datos KFG.
# Lectura: cada nudo L de valor 2-12 en la cuerda -> sílaba (tabla de la hoja UR193); acierto = alguna raíz de 2-3 sílabas de Huarochirí.
import pandas as pd, numpy as np, re, importlib.util, sys
rng=np.random.default_rng(20261018)
SYL={2:'ki',3:'ma',4:'ka',5:'ta',6:'pa',7:'wa',8:'cha',9:'pi',10:'si',11:'ti',12:'ku'}
txtq=open('analisis/ds/n_linguistica/corpus/huarochiri_quechua.txt',encoding='utf-8').read().lower()
def norm(w):
    w=re.sub(r'hu([aeiou])',r'w\1',w); w=w.replace('qu','k').replace('ch','§').replace('c','k').replace('§','ch')
    return w.replace('e','i').replace('o','u')
SY=re.compile(r'(ch|[kpmtwsnlr]|)([aiu])'); stems=set()
for w in re.findall(r'[a-zñ]+',txtq):
    sy=[a+b for a,b in SY.findall(norm(w))]
    for k in (2,3):
        if len(sy)>=k: stems.add(''.join(sy[:k]))
hit=lambda sil:any(''.join(sil[i:j]) in stems for i in range(len(sil)) for j in range(i+2,len(sil)+1))
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
R=re.compile(r'(\d+)L\(')
for q in ['UR039','UR112','UR193','UR050','UR055']:
    seqs=[[int(x) for x in R.findall(s) if 2<=int(x)<=12] for s in c[(c.kfg==q)&c.nudos.notna()].nudos]
    seqs=[s for s in seqs if len(s)>=2]
    if not seqs: print(q,'sin cuerdas con >=2 nudos L'); continue
    lee=lambda s:[SYL[x] for x in s]
    o=np.mean([hit(lee(s)) for s in seqs]); pool=[x for s in seqs for x in s]
    n=np.array([np.mean([hit(lee(list(rng.choice(pool,len(s))))) for s in seqs]) for _ in range(1000)])
    print(f'{q}: cuerdas={len(seqs)} real={o:.3f} azar={n.mean():.3f} p={np.mean(n>=o):.3f}')
