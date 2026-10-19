import sqlite3, pandas as pd, numpy as np, re
pd.set_option('display.width',200)
con = sqlite3.connect('data/external/open-khipu-repository/data/khipu.db')
cc = pd.read_sql("SELECT ORDINAL,BEG_CORD,END_CORD,NUM_CORDS,GROUPING_CLASS FROM cord_cluster WHERE KHIPU_ID=1000096", con)
con.close()
cc = cc.sort_values('ORDINAL').reset_index(drop=True)
# map cluster ordinal -> start ordinal (1-based cord ordinal)
cl2beg = dict(zip(cc.ORDINAL, cc.BEG_CORD))
# verify target p1332 = cluster162 pos4 -> cord ordinal?
print("cluster 162:", cc[cc.ORDINAL==162].to_dict('records'))
print("cluster 94:", cc[cc.ORDINAL==94].to_dict('records'))
print("cluster 96:", cc[cc.ORDINAL==96].to_dict('records'))

c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
# build cord ordinal (1-based = orden+1)
d['cordinal'] = d.orden+1
def get_val(cordinal): return d.loc[d.cordinal==cordinal,'valor'].iloc[0]
def sk(c, p): return int(cl2beg[c]) + int(p)
# case p1332: [162,4] target; summands 94:3,94:4,94:5,96:1
print("\nTarget via [162,4] -> cordinal", sk(162,4), "valor", get_val(sk(162,4)))
for (c_,p_) in [(94,3),(94,4),(94,5),(96,1)]:
    ci = sk(c_,p_); print(f"  summand [{c_},{p_}] -> cordinal {ci} valor {get_val(ci)}")
print("  sum =", sum(get_val(sk(c_,p_)) for (c_,p_) in [(94,3),(94,4),(94,5),(96,1)]))
