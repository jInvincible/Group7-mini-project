import pandas as pd
from glob import glob
source_path = 'raw data'
content = ''
file_type = 'xlsx'
recursive = False

# get list of all csv file_path in source folder
filename_list = glob(f'{source_path}/*.{file_type}', recursive=f'{recursive}')

# for each file
# excel file
if (file_type == 'xlsx') or (file_type == 'xls'):
    for filename in filename_list:
        xl = pd.ExcelFile(filename)
        sheets = xl.sheet_names
        for sheet in sheets:
            count = 0
            df = pd.read_excel(filename, sheet_name=f'{sheet}')
            # trim column data and make a list
            df_columns = [name.strip() for name in df.columns]
            content += f'#### ({filename}) -- sheet ({sheet}) ####\n'
            # creating content to report
            for i in df_columns:
                content += f'column[{count+1}]: {i}'
                content += '\n'
                count += 1

# csv file
elif file_type == 'csv':
    for filename in filename_list:
        count = 0
        df = pd.read_csv(filename)
        # trim column data and make a list
        df_columns = [name.strip() for name in df.columns]
        content += f'#### ({filename}) ####\n'
        # creating content to report
        for i in df_columns:
            content += f'column[{count+1}]: {i}'
            content += '\n'
            count += 1

# save report to a result file
with open('data_columns_scan_result.txt', 'w+') as f:
    f.write(content)

