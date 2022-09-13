import pandas as pd
source_path =  'raw data from kaggle'
filename = 'social media influencers - instagram.csv'
file_path = source_path + '/' + filename

df = pd.read_csv(file_path, engine='python')
df.info()

df.head()
df.tail()