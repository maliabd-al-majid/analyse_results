import csv

import numpy as np
import pandas as pd

CSV_NAME = './treewidth_output_PMC_ARG_75.csv'
df = pd.read_csv(CSV_NAME)
d =df[df['solver']=='nesthdb']
for x,i in df.iterrows():
    for x1,i1 in d.iterrows():
        if i1['instance']==i['instance']:
            df.at[x,'tree_width'] = i1['tree_width']
            df.at[x,'projections'] = i1['projections']


#d = df[df['solver'] == 'dpdb']



# print(df['tree_width'])
#  df.at[, 'tree_width'] = row['tree_width']
# print('asdasd')

df.to_csv('PMC_ARG_75_treewidth.csv', encoding='utf-8')

# print('asdasd')


# print(dpdb_df['tree_width'])
