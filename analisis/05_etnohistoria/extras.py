"""Extras Glave (Parinacocha: 240 pesos/semana, 52 sem = 12 480; 5 anos = 62 400) y 6 quipus del Santa: verificaciones descriptivas."""
import pandas as pd, numpy as np
from scipy import stats
c=pd.read_csv('./analisis/datos/cuerdas.csv',low_memory=False); c['valor']=c.valor.fillna(0)
tot=c.groupby('kfg').valor.sum(); pen=c[c.nivel==0].groupby('kfg').valor.sum()
print('quipus con total 12480 / 62400 / 240:',[ (t,list(tot[tot==t].index),list(pen[pen==t].index)) for t in (12480,62400,240)])
print('cuerdas con valor 240:',c[c.valor==240].kfg.value_counts().head(5).to_dict(), '| cuerdas con valor 12480:',(c.valor==12480).sum())
gs=c[c.nivel==0].groupby(['kfg','grupo']).size().reset_index(name='n')
cnt={s:gs[gs.n==s].kfg.nunique() for s in range(40,65)}
print('quipus con algun grupo de exactamente s colgantes (s=47..57):',{s:cnt[s] for s in range(47,58)})
lam=np.mean([cnt[s] for s in range(47,58) if s!=52]); print('52 -> obs',cnt[52],'vecinos media %.2f'%lam,'Poisson p=%.3f'%stats.poisson.sf(cnt[52]-1,lam),'|',list(gs[gs.n==52].kfg.unique()))
