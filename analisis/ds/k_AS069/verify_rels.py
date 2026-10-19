import pandas as pd, numpy as np, re
base = 'data/external/data-science-khipu-article/data/ascher_sum_relations/'
def load(f):
    x = pd.read_csv(base+f); x.columns=[c.strip().lstrip('\ufeff') for c in x.columns]
    return x[x.name=='AS069'] if 'name' in x.columns else x

def sumval(s):
    return sum(int(n) for n in re.findall(r'\]:(-?\d+)', str(s)))

for f,lab in [('pendant_pendant_sum_relation.csv','PENDANT-PENDANT'),
              ('pendant_pendants_color_sum_relation.csv','PENDANT-COLOR'),
              ('indexed_pendant_sum_relation.csv','INDEXED-PENDANT'),
              ('subsidiary_pendant_sum_relation.csv','SUBSIDIARY-PENDANT'),
              ('indexed_subsidiary_sum_relation.csv','INDEXED-SUBSIDIARY')]:
    x = load(f)
    x = x[x.sum_string.notna()].copy()
    x['s'] = x.sum_string.map(sumval)
    x['exact'] = x.s == x.cord_value
    print(f"{lab}: n={len(x)}  exact={x.exact.sum()} ({100*x.exact.mean():.0f}%)  "
          f"val_nozero={(x.cord_value!=0).sum()}")
    if len(x):
        print("   cord_value range:", x.cord_value.min(), x.cord_value.max(),
              "| n_summands range:", x.num_summands.min(), x.num_summands.max())
    print()

# clusters
cc = load('cluster_cluster_sum_relation.csv')
print("CLUSTER-CLUSTER SUM:", len(cc))
cc2 = cc.copy()
cc2['ls'] = cc2.left_cluster_sum_string.map(sumval); cc2['rs']=cc2.right_cluster_sum_string.map(sumval)
print(cc2[['cluster_sum','left_cluster_sum_string','right_cluster_sum_string','cord_count_distance']].head(8).to_string())
