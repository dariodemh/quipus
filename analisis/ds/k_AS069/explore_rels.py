import pandas as pd, numpy as np
pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 80)
base = 'data/external/data-science-khipu-article/data/ascher_sum_relations/'
def load(f):
    x = pd.read_csv(base+f)
    x.columns = [c.strip().lstrip('\ufeff') for c in x.columns]
    return x[x.name == 'AS069'] if 'name' in x.columns else x

pps = load('pendant_pendant_sum_relation.csv')
print("PENDANT-PENDANT SUM relations:", len(pps))
print(pps.columns.tolist())
print(pps[['cord_name','cord_position','cord_value','num_summands','sum_string','handedness']].head(12).to_string())
print()
# verify: parse sum_string numbers and compare
def parse_sum(s):
    import re
    nums = re.findall(r'-?\d+', str(s))
    return [int(n) for n in nums]
pps = pps.copy()
pps['nums'] = pps.sum_string.map(parse_sum)
# sum_string format? print some
print("sum_string examples:", pps.sum_string.dropna().unique()[:8].tolist())
print()
colors = load('pendant_pendants_color_sum_relation.csv')
print("PENDANT-PENDANTS COLOR SUM relations:", len(colors))
print(colors[['cord_name','cord_position','cord_value','cord_color','num_summands','sum_string','handedness']].head(10).to_string())
sub = load('subsidiary_pendant_sum_relation.csv')
print()
print("SUBSIDIARY-PENDANT SUM relations:", len(sub))
print(sub[['cord_name','cord_position','parent_cord_position','cord_value','num_summands','sum_string','handedness']].head(10).to_string())
