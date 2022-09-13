import pandas as pd
from glob import glob
source_path =  'raw data from kaggle'
filename = 'social media influencers - instagram.csv'
file_path = source_path + '/' + filename

filename_list = glob(source_path +'/*.csv')

df = pd.read_csv(file_path, engine='python')
df_columns = df.columns.split()
df.columns.replace(to_replace=r'\s+$', value=r'', regex=True)

