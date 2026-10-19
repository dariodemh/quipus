import pandas as pd, numpy as np, re
D='./analisis/datos/'
C=pd.read_csv(D+'cuerdas.csv'); Q=pd.read_csv(D+'quipus.csv').set_index('kfg'); G=pd.read_csv(D+'grupos.csv')
def q(k): return C[C.kfg==k].reset_index(drop=True)
def pend(k):
    d=q(k); return d[d.nivel==0].reset_index(drop=True)
