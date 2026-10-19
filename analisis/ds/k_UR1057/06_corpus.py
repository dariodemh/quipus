import pandas as pd, numpy as np
c=pd.read_csv('analisis/datos/cuerdas.csv')
c['blank']=c.nudos.isna()
g=c.groupby('kfg').agg(n=('cuerda','size'),blank=('blank','mean'),meanv=('valor','mean'),
                       nz=('valor',lambda s:(s>0).mean()),mx=('valor','max'))
g=g[g.n>=30]
u=g.loc['UR1057']
for k in ['n','blank','meanv','nz','mx']:
    pct=(g[k]<=u[k]).mean()*100
    print(f'{k:6s} UR1057={u[k]:8.3f}  percentil={pct:5.1f}  mediana={g[k].median():8.3f}  n_quipus={len(g)}')
# repeticion de la firma de color: ventanas de 12 colores repetidas
def rep_score(s):
    cols=s.fillna('?').astype(str).str.split('(').str[0].tolist()
    if len(cols)<24: return np.nan
    w=['|'.join(cols[i:i+12]) for i in range(len(cols)-11)]
    from collections import Counter
    cnt=Counter(w)
    return sum(v for v in cnt.values() if v>1)/len(w)
sc=c.groupby('kfg').apply(lambda s: rep_score(s.sort_values('orden').color), include_groups=False)
sc=sc.dropna()
print(f'\nrepeticion color(12) UR1057={sc.get("UR1057"):.3f} percentil={(sc<=sc.get("UR1057")).mean()*100:.1f} mediana={sc.median():.3f} n={len(sc)}')
