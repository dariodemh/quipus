"""C5: P6b dentro del conjunto atado UR053A-E (variante 33, prerregistrada en §E)."""
import importlib.util, numpy as np, pandas as pd
from pathlib import Path
OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('p6b', OUT / '03_p6b.py'); P6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P6)
SET = ['UR053A', 'UR053B', 'UR053C', 'UR053D', 'UR053E']
P6.socios = lambda k: [j for j in SET if j != k]
rows = [P6.run(k) for k in SET]
d = pd.DataFrame([r for r in rows if r]); d.to_csv(OUT / 'pred_C5.csv', index=False); print(d.to_string())

# ---- C6: MM001 como lista de ceques (prerregistrada en §F) ----
import pickle, plantillas as T
K = pickle.load(open(OUT / 'datos.pkl', 'rb'))['K']; k = K['MM001']
G = T.groups(k); sz = np.array([len(x) for x in G])
for i in range(len(sz) - 3):
    s = np.sort(sz[i:i + 4])
    if np.all(np.abs(s - np.array([9, 9, 9, 14])) <= 1): break
idx = np.concatenate(G[i:i + 4]); v = k['vals'][idx]
print('MM001 grupos', i, '..', i + 3, 'tamaños', sz[i:i + 4].tolist(), '| suma valores', np.nansum(v), '| anudadas', int((~np.isnan(v)).sum()))
print('valores por grupo', [np.nan_to_num(k['vals'][x]).astype(int).tolist() for x in G[i:i + 4]])
c = pd.factorize(k['col'][idx])[0]
rng = np.random.default_rng(20261018)
o = T.P9a(c[None, :])[0]; null = T.P9a(rng.permuted(np.tile(c, (9999, 1)), axis=1))
print(f'P9a en los 41: {o:.3f}, p={(1 + np.sum(null >= o)) / 10000:.4f}; colores', k['col'][idx].tolist())
