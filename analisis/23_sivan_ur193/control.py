# Control de la "traducción" silábica de UR193 (Sivan/ALBA 2026, encontrado/UR193.xlsx):
# misma regla de lectura aplicada a secuencias reales frente a secuencias al azar con la misma distribución.
import pandas as pd, numpy as np, re
rng=np.random.default_rng(20261018)
t=pd.read_excel('encontrado/UR193.xlsx',sheet_name='Traduction')
r=pd.read_excel('encontrado/UR193.xlsx',sheet_name='Resume',header=None)
# tabla nudo->sílaba implícita en la hoja (L2..L12)
SYL={2:'ki',3:'ma',4:'ka',5:'ta',6:'pa',7:'wa',8:'cha',9:'pi',10:'si',11:'ti',12:'ku'}
# diccionario = su propio vocabulario (filas 28-75 de 'Resume') + todas las sílabas sueltas, que la hoja acepta como partículas
vocab={str(w).strip() for w in r.iloc[28:76,0].dropna()}
DICT=vocab|set(SYL.values())
def lee(seq):  # seq = lista de vueltas L; S10 se ignora (prefijo numérico)
    return [SYL[x] for x in seq if x in SYL]
def acierto(sil):
    if not sil: return False
    for i in range(0,min(2,len(sil))):           # quita hasta 1 afijo al inicio
        for j in range(len(sil),max(i,len(sil)-2),-1):   # y hasta 1 al final
            if j>i and ''.join(sil[i:j]) in DICT: return True
    return False
txt=t[t.Type=='TEXTE'].Noeuds.dropna().map(lambda s:[int(m) for m in re.findall(r'L(\d+)',s)])
txt=[s for s in txt if s]
obs=np.mean([acierto(lee(s)) for s in txt])
pool=[x for s in txt for x in s]; L=[len(s) for s in txt]
nul=[np.mean([acierto(lee(list(rng.choice(pool,l)))) for l in L]) for _ in range(2000)]
uni=[np.mean([acierto(lee(list(rng.integers(2,13,l)))) for l in L]) for _ in range(2000)]
print(f'cuerdas TEXTE con nudos L: {len(txt)}  longitudes: {pd.Series(L).value_counts().sort_index().to_dict()}')
print(f'tasa de acierto real: {obs:.3f}')
print(f'azar (misma distribución de vueltas): media {np.mean(nul):.3f}  p(azar>=real)={np.mean(np.array(nul)>=obs):.3f}')
print(f'azar (vueltas uniformes 2-12): media {np.mean(uni):.3f}')
# sin sílabas sueltas como 'palabra' (solo palabras de >=2 sílabas del vocabulario)
DICT2={w for w in vocab if len(w)>=4}
def acierto2(sil):
    return any(''.join(sil[i:j]) in DICT2 for i in range(len(sil)) for j in range(i+2,len(sil)+1))
o2=np.mean([acierto2(lee(s)) for s in txt]); n2=[np.mean([acierto2(lee(list(rng.choice(pool,l)))) for l in L]) for _ in range(2000)]
print(f'solo palabras de >=2 sílabas: real {o2:.3f}  azar {np.mean(n2):.3f}  p={np.mean(np.array(n2)>=o2):.3f}')

# --- diccionario INDEPENDIENTE: raíces de 2-3 sílabas al inicio de palabras del manuscrito de Huarochirí (~1608)
txtq=open('analisis/ds/n_linguistica/corpus/huarochiri_quechua.txt',encoding='utf-8').read().lower()
def norm(w):
    w=re.sub(r'hu([aeiou])',r'w\1',w); w=w.replace('qu','k').replace('ch','§').replace('c','k').replace('§','ch')
    w=w.replace('e','i').replace('o','u'); return w
SY=re.compile(r'(ch|[kpmtwsnlr]|)([aiu])')
stems=set()
for w in re.findall(r'[a-zñ]+',txtq):
    s=SY.findall(norm(w))
    sy=[a+b for a,b in s]
    for k in (2,3):
        if len(sy)>=k: stems.add(''.join(sy[:k]))
print('raíces de Huarochirí:',len(stems))
def acierto3(sil):
    return any(''.join(sil[i:j]) in stems for i in range(len(sil)) for j in range(i+2,len(sil)+1))
o3=np.mean([acierto3(lee(s)) for s in txt]); n3=np.array([np.mean([acierto3(lee(list(rng.choice(pool,l)))) for l in L]) for _ in range(2000)])
print(f'diccionario independiente (Huarochirí): real {o3:.3f}  azar {n3.mean():.3f}  p={np.mean(n3>=o3):.3f}')
