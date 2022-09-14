import pandas as pd
from glob import glob
source_path = 'raw data from kaggle'
content = ''

# get list of all csv file_path in source folder
filename_list = glob(source_path +'/**/*.csv', recursive= True)

# for each csv file
for filename in filename_list:
    df = pd.read_csv(filename, engine='python')
    # trim column data and make a list
    df_columns = [name.strip() for name in df.columns]
    content += '#### ' + filename + ' ####\n'
    count = 0
    # creating content to report
    for i in df_columns:
        content += f'column[{count+1}]: {i}'
        content += '\n'
        count += 1

# save report to a result file
with open('data_columns_scan_result.txt', 'w+') as f:
    f.write(content)

