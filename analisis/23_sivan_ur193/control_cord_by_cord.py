# Réplica sobre las cuerdas STRING del propio ALBA (reproducibility/cord_by_cord.csv, CC-BY 4.0):
# palabra = racha contigua de nudos L entre nudos S; mapeo ALBA v3 fijo; barajado de vueltas L dentro de cada quipu.
import sys, pandas as pd, numpy as np, re
rng=np.random.default_rng(20261018)
cbc=pd.read_csv(sys.argv[1])
BASE={2:'ki',3:'ma',4:'ka',5:'ta',6:'pa',7:'y',8:'na',9:'pi',10:'si',11:'ti',12:'ku'}; ONSET={2:'chi',7:'wa',8:'cha'}
words={w.strip().lower() for w in open('analisis/23_sivan_ur193/quechua_kaikki_2060.txt',encoding='utf-8') if w.strip()}
ext=set(words)|{w+s for w in words for s in ['ta','pa','ka','ma','na','qa','ki','si','y'] if len(w+s)>=4}
DIC=ext|{w[:i] for w in ext for i in range(4,len(w))}
def runs(ks):
    out=[];cur=[]
    for k in ks.split():
        m=re.fullmatch(r'L(\d+)',k)
        if m and 2<=int(m.group(1))<=12: cur.append(int(m.group(1)))
        else:
            if cur: out.append(cur); cur=[]
    if cur: out.append(cur)
    return out
lee=lambda r:''.join((ONSET.get(x,BASE[x]) if i==0 else BASE[x]) for i,x in enumerate(r))
s=cbc[(cbc.cord_type=='STRING')&cbc.knot_sequence.notna()]
print('cuerdas STRING:',len(s),'quipus:',s.khipu.nunique())
filas=[]; tot_o=[];tot_n=[]
for q,g in s.groupby('khipu'):
    W=[r for ks in g.knot_sequence for r in runs(ks) if len(r)>=2]
    if len(W)<10: continue
    o=np.mean([lee(r) in DIC for r in W]); pool=np.array([x for r in W for x in r]); n=[]
    for _ in range(500):
        p=rng.permutation(pool);i=0;h=[]
        for r in W: h.append(lee(list(p[i:i+len(r)])) in DIC); i+=len(r)
        n.append(np.mean(h))
    n=np.array(n); filas.append((q,len(W),o,n.mean(),(n>=o).mean()))
r=pd.DataFrame(filas,columns=['quipu','palabras','real','barajado','p'])
from statsmodels.stats.multitest import multipletests
r['q_bh']=multipletests(r.p+1/501,method='fdr_bh')[1]
print(r.round(3).to_string(index=False))
print('quipus probados',len(r),'| real>barajado:',(r.real>r.barajado).sum(),'| p<0.05:',(r.p<0.05).sum(),'| q<0.05:',(r.q_bh<0.05).sum())
print('media real',r.real.mean().round(3),'media barajado',r.barajado.mean().round(3))
r.to_csv('analisis/23_sivan_ur193/control_cord_by_cord.csv',index=False)
