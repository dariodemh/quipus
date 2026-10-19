"""Corrección de Holm sobre todas las pruebas de predicción del paso 5 (A2, C1-C5)."""
import pandas as pd
from pathlib import Path
from statsmodels.stats.multitest import multipletests
OUT = Path(__file__).resolve().parent
r = []
for f, lab, pcol in [('pred_C1.csv', 'C1 perfil en bandas (P4r)', 'p'), ('pred_C2.csv', 'C2 fase del trío (P9a)', 'p'),
                     ('pred_C3.csv', 'C3 perfil entre bloques (P11)', 'p'), ('pred_C5.csv', 'C5 jerarquía UR053 (P6b)', 'p_perm')]:
    d = pd.read_csv(OUT / f)
    for x in d.itertuples(): r.append(dict(prueba=lab, khipu=x.khipu if hasattr(x, 'khipu') else x.kfg, p=getattr(x, pcol)))
# resultados impresos por 05_predicciones.py (A2, C2 binomiales, C4)
r += [dict(prueba='A2 ceques en rachas', khipu='UR055', p=0.9999), dict(prueba='C6(ii) ciclo de 3 en 41 cuerdas', khipu='MM001', p=0.1028),
      dict(prueba='C2 binomial W mayor', khipu='UR053A', p=2.9e-4), dict(prueba='C2 binomial W mayor', khipu='UR053C', p=1.7e-4),
      dict(prueba='C2 binomial W mayor', khipu='UR053D', p=5e-10)]
for k, p1, p2 in [('KH0033', .5004, 1), ('UR044', .5013, 1), ('QU013', 1, .9352), ('UR068', 1, 1)]:
    r += [dict(prueba='C4(i) subsidiarias', khipu=k, p=p1), dict(prueba='C4(ii) fallos 10^j', khipu=k, p=p2)]
d = pd.DataFrame(r).dropna(subset=['p'])
d['p_holm'] = multipletests(d.p, method='holm')[1]
d.to_csv(OUT / 'predicciones.csv', index=False)
print(len(d), 'pruebas'); print(d.sort_values('p').head(25).to_string())
