import pandas as pd, numpy as np, re, sys
pd.set_option('display.width', 200)
C = pd.read_csv('analisis/datos/cuerdas.csv', dtype={'nudos': str, 'color': str, 'notas': str})
Q = pd.read_csv('analisis/datos/quipus.csv')
print('quipus', Q.kfg.nunique(), 'cuerdas', len(C))

pat = re.compile(r'^(\d+)([A-Z?]+)\(([\d.]+),([SZU?])\)(?:,([\d.]+))?$')
rows = []
bad = 0
for r in C.itertuples():
    s = r.nudos
    if not isinstance(s, str) or s.strip() == '' or s == 'nan':
        continue
    for seg in s.split(';'):
        seg = seg.strip()
        if not seg:
            continue
        m = pat.match(seg)
        if not m:
            bad += 1
            continue
        n, t, pos, d, v = m.groups()
        rows.append((r.kfg, r.cuerda, r.nivel, int(n), t, float(pos), d,
                     float(v) if v is not None else np.nan))
K = pd.DataFrame(rows, columns=['kfg','cuerda','nivel','n','tipo','pos','dir','val'])
print('clusters', len(K), 'bad segs', bad)
print(K.tipo.value_counts().to_string())
print('\nL val distribution')
print(K[K.tipo=='L'].val.value_counts().head(15).to_string())
print('\nE val'); print(K[K.tipo=='E'].val.value_counts().head(10).to_string())
print('\nS val counts'); print(K[K.tipo=='S'].val.value_counts().head(15).to_string())
print('\nS val multiples check: % divisible by10', (K[K.tipo=='S'].val % 10 == 0).mean())
print('\nL val multiples check: % divisible by10', (K[K.tipo=='L'].val % 10 == 0).mean())
print('\nvalue 0 clusters', (K.val==0).sum(), 'NaN', K.val.isna().sum())
# per-cord cluster count
print('\ncuerdas no nudos:', C.nudos.isna().sum(), 'vacios str:', (C.nudos.fillna('').str.strip()=='').sum())
print('cuerdas valor 0:', (C.valor==0).sum(), 'sin nudos y valor0:', ((C.valor==0)&(C.nudos.fillna('').str.strip()=='')).sum())
print('\nunion counts'); print(C.union.value_counts(dropna=False).to_string())
print('\nterminacion top'); print(C.terminacion.value_counts(dropna=False).head(15).to_string())
print('\ncolor top'); print(C.color.value_counts(dropna=False).head(20).to_string())
