import pandas as pd, numpy as np
pd.set_option('display.width', 240)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)

# marker cords = color not exactly 'W'
d['is_marker'] = d.color != 'W'
print("markers (color!=W):", d.is_marker.sum(), "/", len(d))
# how many markers are singletons vs in blocks
gs = d.groupby('grupo').size()
sing_groups = set(gs[gs==1].index)
d['in_singleton'] = d.grupo.isin(sing_groups)
print("markers in singleton groups:", (d.is_marker & d.in_singleton).sum())
print("non-markers in singleton groups:", (~d.is_marker & d.in_singleton).sum())
# do markers always start a 'record'? sequence of marker flag
d['runs'] = (d.is_marker != d.is_marker.shift()).cumsum()
# lengths of marker-runs
runlens = d.groupby('runs').is_marker.agg(['first','size'])
print("marker-run lengths:", runlens[runlens['first']]['size'].value_counts().to_dict())
# color band position: markers with top-band pattern "(0.0-"
band = d[d.color.str.contains(r'\(0\.0-', na=False)]
print("cords with a colored top-band (0.0-x):", len(band))
# base color of band markers
print("base color of band markers (first token):", band.color.str.split(r'[\\(/]').str[0].value_counts().head(12).to_dict())
