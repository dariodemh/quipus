import pandas as pd, numpy as np
pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 60)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg == 'AS069'].copy().sort_values('orden').reset_index(drop=True)
# first 60: orden, group, color short, valor, nudos
sub = d.head(60).copy()
sub['col'] = sub.color.str.slice(0,18)
print(sub[['orden','grupo','nivel','col','valor','nudos','largo']].to_string())
