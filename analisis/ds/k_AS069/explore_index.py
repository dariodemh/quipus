import pandas as pd
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',120)
base='data/external/data-science-khipu-article/data/ascher_sum_relations/'
x=pd.read_csv(base+'indexed_pendant_sum_relation.csv'); x.columns=[c.strip().lstrip('\ufeff') for c in x.columns]
x=x[x.name=='AS069']
print(x[['cord_name','cord_position','cord_position_index','cord_value','num_summands','sum_string']].head(6).to_string())
print()
y=pd.read_csv(base+'pendant_pendant_sum_relation.csv'); y.columns=[c.strip().lstrip('\ufeff') for c in y.columns]
y=y[y.name=='AS069']
print(y[['cord_name','cord_position','cord_position_index','cord_value','num_summands']].head(6).to_string())
