# -*- coding: utf-8 -*-
"""UR093: extraer relaciones de suma del KFG (KFG_DB) sin imprimir strings gigantes."""
import pandas as pd, glob, os
D='data/external/data-science-khipu-article/data/'
cards={}
for f in glob.glob(D+'ascher_sum_relations/*.csv')+glob.glob(D+'KFG_DB_Excel/*.csv'):
    try:
        d=pd.read_csv(f,low_memory=False)
    except Exception as e:
        continue
    if 'khipu_id' not in d.columns: continue
    hit=d[d.khipu_id==1000321] if d.khipu_id.dtype!=object else d[d.khipu_id.astype(str)=='1000321']
    if len(hit):
        scal=[c for c in d.columns if 'string' not in c and d[c].dtype.name in ('int64','float64','bool','int32')]
        cards[os.path.basename(f)]=hit[scal].to_dict('records')
for k,v in cards.items():
    print('==',k)
    for r in v: print('   ',r)
