# -*- coding: utf-8 -*-
"""Control de calidad: contraste KFG vs OKR para los quipus con arboles profundos.
OKR numera los niveles +1 respecto de KFG (nivel 1 = cordon principal / cuerdas
de nivel 0 en KFG). Se comparan conteos por nivel y se marca discrepancia."""
import pandas as pd, numpy as np, sqlite3, os, json

BASE = r'.'
OUT = os.path.join(BASE, 'analisis', 'ds', 't_subsidiarias_profundas')
d = pd.read_csv(os.path.join(BASE, 'analisis', 'datos', 'cuerdas.csv'))
T = pd.read_csv(os.path.join(OUT, 'arboles.csv'))
c = sqlite3.connect(os.path.join(BASE, 'data', 'external', 'open-khipu-repository', 'data', 'khipu.db'))

rows = []
for kfg in sorted(T.kfg.unique()):
    r = c.execute('select KHIPU_ID from khipu_main where OKR_NUM=?', (kfg,)).fetchone()
    if not r:
        rows.append(dict(kfg=kfg, okr='no', kfg_n=len(d[d.kfg == kfg]),
                         kfg_max=int(d[d.kfg == kfg].nivel.max()), okr_n=np.nan, okr_max=np.nan,
                         estado='sin OKR'))
        continue
    kid = r[0]
    df = pd.read_sql('select CORD_LEVEL, count(*) n from cord where KHIPU_ID=? group by CORD_LEVEL', c, params=(kid,))
    okr_max = int(df.CORD_LEVEL.max()) - 1 if len(df) else np.nan   # normalizar a escala KFG
    okr_n = int(df.n.sum())
    kn = len(d[d.kfg == kfg]); kmax = int(d[d.kfg == kfg].nivel.max())
    # tolerancia: 15% de diferencia en total y mismo maximo +-1
    estado = 'ok'
    if abs(okr_n - kn) > max(5, 0.15 * kn) or (pd.notna(okr_max) and abs(okr_max - kmax) > 1):
        estado = 'DISCREPA'
    rows.append(dict(kfg=kfg, okr='si', kfg_n=kn, kfg_max=kmax, okr_n=okr_n, okr_max=okr_max, estado=estado))

C = pd.DataFrame(rows)
C.to_csv(os.path.join(OUT, 'control_okr.csv'), index=False)
print(C.estado.value_counts().to_string())
print('\nQuipus con discrepancia:')
print(C[C.estado == 'DISCREPA'].to_string(index=False))
print('\nQuipus corroborados (mismo max nivel +-1 y conteo similar):')
print(C[C.estado == 'ok'].to_string(index=False))
json.dump(C.estado.value_counts().to_dict(), open(os.path.join(OUT, 'control_okr.json'), 'w'), indent=2)
