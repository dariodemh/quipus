# Control que ALBA nombra pero no corre: mapeo FIJO (silabario ALBA v3), secuencias de nudos barajadas dentro del quipu.
# Diccionario y regla de acierto de ALBA: palabra completa en Kaikki (2 060) + sufijos + prefijos de >=4 letras
# (negative_controls.load_quechua_dictionary, reimplementado sin ejecutar su código).
import pandas as pd, numpy as np, re
rng=np.random.default_rng(20261018)
BASE={2:'ki',3:'ma',4:'ka',5:'ta',6:'pa',7:'y',8:'na',9:'pi',10:'si',11:'ti',12:'ku'}
ONSET={2:'chi',7:'wa',8:'cha'}
words={w.strip().lower() for w in open('analisis/23_sivan_ur193/quechua_kaikki_2060.txt',encoding='utf-8') if w.strip()}
ext=set(words)
for w in words:
    for s in ['ta','pa','ka','ma','na','qa','ki','si','y']:
        if len(w+s)>=4: ext.add(w+s)
DIC=ext|{w[:i] for w in ext for i in range(4,len(w))}
def lee(seq): return ''.join((ONSET.get(x,BASE[x]) if i==0 else BASE[x]) for i,x in enumerate(seq))
c=pd.read_csv('analisis/datos/cuerdas.csv',low_memory=False)
R=re.compile(r'(\d+)L\(')
filas=[]
for q in ['UR039','UR112','UR193','UR144','UR050','UR055','UR1095','KH0001']:
    seqs=[[int(x) for x in R.findall(s) if 2<=int(x)<=12] for s in c[(c.kfg==q)&c.nudos.notna()].nudos]
    seqs=[s for s in seqs if len(s)>=2]
    if len(seqs)<10: continue
    o=np.mean([lee(s) in DIC for s in seqs]); pool=np.array([x for s in seqs for x in s])
    n=[]
    for _ in range(2000):
        p=rng.permutation(pool); i=0; sh=[]
        for s in seqs: sh.append(list(p[i:i+len(s)])); i+=len(s)
        n.append(np.mean([lee(s) in DIC for s in sh]))
    n=np.array(n); filas.append((q,len(seqs),o,n.mean(),np.mean(n>=o)))
    print(f'{q}: cuerdas={len(seqs)} aciertos reales={o:.3f}  barajado={n.mean():.3f}  p(barajado>=real)={np.mean(n>=o):.3f}')
pd.DataFrame(filas,columns=['quipu','cuerdas','real','barajado','p']).to_csv('analisis/23_sivan_ur193/control_exacto.csv',index=False)
