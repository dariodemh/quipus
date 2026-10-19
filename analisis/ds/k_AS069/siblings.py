import pandas as pd, numpy as np
c = pd.read_csv('analisis/datos/cuerdas.csv')
q = pd.read_csv('analisis/datos/quipus.csv')
for k in ['AS069','AS070','AS071','AS072']:
    n = (c.kfg==k).sum()
    row = q[q.kfg==k]
    proc = row.procedencia.iloc[0] if len(row) else '?'
    print(k, "cuerdas:", n, "| proc:", proc)
# corpus size ranking
sizes = c.kfg.value_counts().head(8)
print("Top khipus por n cuerdas:", sizes.to_dict())
