import csv

import numpy as np
import pandas as pd

import Constant

CSV_NAME = f'./{Constant.parse2csv_name}.csv'
df = pd.read_csv(CSV_NAME)
df['run_id'] = df['run_id'].replace({'clingo': 'nesthdb'}, regex=True)
d =df[df['solver']=='nesthdb']

for x,i in df.iterrows():
    for x1,i1 in d.iterrows():
        if i1['run_id']==i['run_id']:
            df.at[x,'tree_width'] = i1['tree_width']
            df.at[x,'projections'] = i1['projections']


#d = df[df['solver'] == 'dpdb']



# print(df['tree_width'])
#  df.at[, 'tree_width'] = row['tree_width']
# print('asdasd')

df.to_csv(f'{Constant.csv2dpdbtw_name}.csv', encoding='utf-8')

# print('asdasd')


# print(dpdb_df['tree_width'])
