# Tabla 4.4 de Urton (valores de UR006) vs KFG
from util import *
import re
T='./analisis/fuentes_txt/InkaHistoryinKnotsReadingKhipusas.txt'
L=open(T,encoding='utf-8').read().split('\n')[905:922]
txt=' '.join(l for l in L if l.strip() and not l.startswith('Table 4.4') and not l.startswith('Note'))
txt=re.sub(r'\([a-d]\)','',txt)
toks=[t.strip() for t in txt.split(',') if t.strip()]
U=[]
for t in toks:
    for part in t.split('+'):
        part=part.strip()
        if re.fullmatch(r'\d+',part): U.append(int(part))
print('valores en Tabla 4.4 (todos, tras separar +):',len(U),'suma',sum(U))
d=q('UR006')
K=[int(v) for v in d.valor if v>0]
print('KFG nonzero:',len(K),'suma',sum(K))
from collections import Counter
cu,ck=Counter(U),Counter(K); print('multiconjunto compartido',sum((cu&ck).values()),'de',len(U),len(K))
def lcs(a,b):
    import numpy as np
    m=np.zeros((len(a)+1,len(b)+1),int)
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            m[i,j]=m[i-1,j-1]+1 if a[i-1]==b[j-1] else max(m[i-1,j],m[i,j-1])
    return m[-1,-1]
# orden de cuerdas en KFG: pendiente, luego subs (como en los pares +) ; Urton: pendiente + sub unidas con '+'
print('LCS secuencia (orden KFG) =',lcs(U,K),' ; ratio',lcs(U,K)/max(len(U),len(K)))
# nulo: permutar K
import numpy as np
rng=np.random.default_rng(12017)
print('nulo LCS con K permutado: ',np.mean([lcs(U,list(rng.permutation(K))) for _ in range(20)]))
print('mayores valores Urton',sorted(U)[-8:],' KFG',sorted(K)[-8:])
