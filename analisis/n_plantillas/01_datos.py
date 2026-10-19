"""Prepara, por quipu, la estructura de colgantes (nivel 0) y la partición en mitades.
Salida: datos.pkl, mitades.csv. Semilla 20261018."""
import pickle, numpy as np, pandas as pd
from pathlib import Path

D = Path(__file__).resolve().parents[1] / 'datos'
OUT = Path(__file__).resolve().parent
c = pd.read_csv(D / 'cuerdas.csv', low_memory=False)
c = c.drop_duplicates(subset=['kfg', 'cuerda'], keep='first')  # UR196 / MM007_AN002 duplicados
q = pd.read_csv(D / 'quipus.csv')
c['anud'] = c.nudos.notna() & (c.nudos.astype(str).str.strip() != '')
c['v'] = np.where(c.anud, c.valor, np.nan)
c['raiz'] = c.cuerda.astype(str).str.split('s').str[0]

K = {}
for k, d in c.groupby('kfg', sort=False):
    d = d.sort_values('orden')
    p = d[d.nivel == 0]
    sub = d.groupby('raiz').size()
    s1 = d[d.nivel == 1].drop_duplicates('raiz').set_index('raiz').v
    K[k] = dict(
        vals=p.v.to_numpy(float), grp=p.grupo.to_numpy(int), col=p.color.fillna('?').astype(str).to_numpy(),
        att=p.union.fillna('?').astype(str).to_numpy(),
        sub=np.array([sub.get(r, 1) for r in p.cuerda.astype(str)]),
        s1=np.array([s1.get(r, np.nan) for r in p.cuerda.astype(str)], float),
        ntot=len(d))
meta = q.set_index('kfg')[['museo', 'procedencia', 'region']]
ks = sorted(K)
rng = np.random.default_rng(20261018)
perm = rng.permutation(ks)
mit = {k: ('exploracion' if i < len(ks) // 2 else 'confirmacion') for i, k in enumerate(perm)}
pd.DataFrame({'kfg': ks, 'mitad': [mit[k] for k in ks]}).to_csv(OUT / 'mitades.csv', index=False)
pickle.dump(dict(K=K, meta=meta, mit=mit), open(OUT / 'datos.pkl', 'wb'))
print(len(K), 'quipus;', sum(v == 'exploracion' for v in mit.values()), 'en exploración')
