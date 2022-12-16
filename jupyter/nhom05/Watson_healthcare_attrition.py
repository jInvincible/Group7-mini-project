# %% 
# Import libraries
from re import A
from tokenize import group
from unicodedata import category
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
import seaborn as sns


# %% 
# Import Data
df = pd.read_csv('raw_watson_healthcare.csv')


# %% 
# Explore Data
df.info()


# %%
# Explore Data
df.columns


# %% 
# Correct column title
correction = {'BUSINESSTravel': 'BusinessTravel', ' department': 'Department',
              'gender': 'Gender', 'Job role': 'JobRole',
              'monthly rate': 'MonthlyRate', 'Total Working Years': 'TotalWorkingYears'}
df = df.rename(columns=correction)
df.columns


# %%
df.isna().sum()

# EmployeeID                   3
# Department                   1
# EducationField               2
# HourlyRate                  11
# JobRole                      1
# MaritalStatus                1
# StandardHours                7
# dtype: int64


# %%
df.head(5)


# %%
df.duplicated().sum()


# %%
# clean up
# remove duplicate row
df = df.drop_duplicates()

# clean_up leading and ending spaces
df = df.replace(to_replace=r'^\s+', value='', regex= True)
df = df.replace(to_replace=r'\s+$', value='', regex= True)

# correct value: BusinessTravel 
# (Rarely -> Travel_Rarely)
df['BusinessTravel'] = df['BusinessTravel'].replace(to_replace='Rarely', value='Travel_Rarely', regex= False)

# drop unused columns:
df = df.drop(columns=['EmployeeCount','StandardHours','EmployeeID'])

# uppercase first charracter using title
# list out all object columns
obj_cols_list = df.select_dtypes(include=['object']).columns.to_list()
for col in obj_cols_list:
    df[col] = df[col].str.title()
    
    
# %%
df_yes = df.loc[df['Attrition'] == 'Yes']
df_yes = df_yes.dropna()
sum_yes = len(df_yes)

# %%
df_yes


# %%
# display columns values
column_values = {}
for col in obj_cols_list:
    values = df_yes[col].unique().tolist()
    for value in values:
        if col not in column_values:
            column_values[col] = [value]
        else:
            column_values[col] += [value]
column_values


# %%
# generate data groupby each column and column 'Attrition'
data1 = {}
data = {}
for column in df.columns:
    data1[column] = df.groupby([column, 'Attrition']).agg({'Attrition': 'count'})

for column in df.columns:
    if column != 'Attrition':
        tmp_b = data1[column]
        tmp_b = tmp_b.rename(columns={'Attrition': 'Count'}).reset_index()
        tmp = pd.DataFrame({column: None, 'No': None, 'Yes': None, 'Yes pct': None}, index=[])
        for biz in set(tmp_b[column]):
            if (tmp_b[((tmp_b[column]==biz) & (tmp_b['Attrition']=='Yes'))]['Count']).empty: # 'Yes' = 0 if no 'Attrition' == 'Yes' matches
                yes = 0
            else:
                yes = int(tmp_b[((tmp_b[column]==biz) & (tmp_b['Attrition']=='Yes'))]['Count'])
            if (tmp_b[((tmp_b[column]==biz) & (tmp_b['Attrition']=='No'))]['Count']).empty: # 'No' = 0 if no 'Attrition' == 'No' matches
                no = 0
            else:
                no = int(tmp_b[((tmp_b[column]==biz) & (tmp_b['Attrition']=='No'))]['Count'])
            btemp = pd.DataFrame({column: biz, 'No': no, 'Yes': yes, 'Yes pct': yes/sum_yes}, index=[1])
            tmp = pd.concat([tmp,btemp])
        data[column] = tmp.copy()
        

# %%
# define function 'draw_this_column' for data
def draw_this_column(column=column, fgsize=None, chart_xlabel=None, chart_ylabel=None, chart_title=None, bar_names_dict:Optional[dict]=None, bar_names_rotation=None, sort_by='Attrition'):
    a_chart_data=data[column]
    
    # create chart settings
    if len(a_chart_data[column]) > 100:
        top = 100
    else:
        top = len(a_chart_data[column])*2

    # define figure size base on maximun of drawing bars
    if fgsize == None: # define figure size if no input
        if top >= 100:
            fgsize = (50,14)
        elif top < 100 and top >= 40:
            fgsize = (25,8)
        elif top < 40 and top >= 20:
            fgsize = (10,7)
        else:
            fgsize = (top/2+1,7) 
    bar_thick = 0.5 # define bar_thick
    df_chart = a_chart_data.copy()
    # sort by attrition = yes DESC| sort by column name ASC | no sort
    if sort_by == 'Attrition':
        df_chart = df_chart.sort_values(by=['Yes', column], ascending=False, ignore_index=True).head(top) # define top data
    elif sort_by == column:
        df_chart = df_chart.sort_values(by=column, ascending=True, ignore_index=True).head(top)
    else:
        df_chart = df_chart.head(top)
        
    chart_y_mean = round(df_chart['Yes'].mean(),2) # define chart mean of yes_bar 
    chart_y_max = df_chart['Yes'].max() # define chart max of yes_bar
    
    if bar_names_rotation == None: # define rotation of bar names at xticks
        if len(df_chart[column]) > 6: # if the number of bars is higher than 6
            if len(str(df_chart[column].to_list()[0])) > 2 and len(str(df_chart[column].to_list()[-1])) > 2: # rotate 90 if bar_name is number and length > 2
                bar_names_rotation = 90
            else:
                bar_names_rotation = 0
        else:
            bar_names_rotation = 0
            
    # define chart xlabel
    if chart_xlabel == None:
        chart_xlabel = ''
        for i in range(len(column)):
            if i != 0:
                if column[i].isupper():
                    chart_xlabel += f' {column[i]}'
                else:
                    chart_xlabel += column[i]
            else:
                chart_xlabel += column[i]
                
    if chart_ylabel == None:
        chart_ylabel = 'Attrition counts' # deine chart ylabel
        
    if chart_title == None:
        if len(df_chart[column]) > 5: # display strings at title
            chart_title = f'Top {int(len(df_chart[column]))} {chart_ylabel} by {chart_xlabel}'
        else:
            chart_title = f'{int(len(df_chart[column]))} {chart_ylabel} by {chart_xlabel}'

    # create data for yes_bar, no_bar
    yes_bar = df_chart['Yes'].to_list()
    no_bar = df_chart['No'].to_list()
    yes_pct = df_chart['Yes pct'].to_list()
    
    # create list of bar_names bar_names_dict={'1': 'mot'}, df_chart[column] = 1
    if bar_names_dict == None:
        bar_names = []
        for a in df_chart[column]:
            bar_names.append(str(a))
            
    else:
        bar_names = []
        for a in df_chart[column]:
            try:
                bar_names.append(bar_names_dict[a])
            except TypeError:
                raise TypeError("bar_names_dict must be dictionary type \nEx:\nbar_names_dict={'1': 'mot', '2': 'hai'}\nwhile names = ['1', '2']")
                return None
    # replace name with white space or '-' by '\n' to display long name in some lines
    bar_names = [name.replace(' ', '\n') if ' ' in str(name) else str(name) for name in bar_names]
    bar_names = [name.replace('_', '\n') if '_' in str(name) else str(name) for name in bar_names]
    bar_names = [name.replace('-', '\n') if '-' in str(name) else str(name) for name in bar_names]
    r = np.arange(len(df_chart[column]))   

    # start drawing chart
    fig, ax = plt.subplots(figsize=fgsize)

    ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes') # drawing yes_bar
    ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No') # drawing no_bar
    
    # get chart_ymax and chart_xmax
    chart_max = ax.get_ylim()[1]
    chart_xmax = ax.get_xlim()[1]
    
    # add yes pct
    for idx in r:
        if yes_bar[idx] > 0:
            if len(df_chart[column]) > 7:
                ax.text(x=idx, y=yes_bar[idx]+no_bar[idx]+chart_max*0.02, s=f'{round(yes_pct[idx]*100,2)}%', rotation = 90, ha='center', va = 'bottom', color = 'white')
            else:
                ax.text(x=idx, y=yes_bar[idx]+no_bar[idx]+chart_max*0.02, s=f'{round(yes_pct[idx]*100,2)}%', ha='center', va = 'bottom', color = 'white')   

    # add legend
    ax.legend(loc='upper left', bbox_to_anchor=(1,1), labels=['Yes', 'No'])

    # custom axis
    plt.xticks(r, bar_names, rotation = bar_names_rotation) # set the name for each Bar
    ax.set_xlim(-0.5,len(r)-0.5)
    ax.set_xlabel(chart_xlabel)
    ax.set_ylabel(chart_ylabel)
    plt.tick_params(bottom=0, left=0) # disable the tick from bottom and left side

    for pos in ['top', 'left', 'right', 'bottom']:
        ax.spines[pos].set_visible(0)

    # add a line
    ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
    ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')
    

    # add text for line    
    ax.text(x=chart_xmax+0.2, y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
    ax.text(x=chart_xmax+0.2, y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

    # add chart title
    ax.set_title(label=chart_title)

    plt.show()


# %%
column = 'Age'
draw_this_column(column=column,sort_by=column)


# %%
column = 'BusinessTravel'
draw_this_column(column=column, bar_names_dict={'Travel_Rarely': 'Hiếm', 'Travel_Frequently': 'Thường xuyên', 'Non-Travel': 'Không'})


# %%
column = 'DailyRate'
draw_this_column(column=column)


# %%
column = 'Department'
draw_this_column(column=column)


# %%
column = 'DistanceFromHome'
draw_this_column(column=column)


# %%
column = 'Education'
draw_this_column(column=column)


# %%
column = 'EducationField'
draw_this_column(column=column)


# %%
column = 'EnvironmentSatisfaction'
draw_this_column(column=column)


# %%
column = 'Gender'
draw_this_column(column=column)


# %%
column = 'HourlyRate'
draw_this_column(column=column)


# %%
column = 'JobInvolvement'
draw_this_column(column=column)


# %%
column = 'JobLevel'
draw_this_column(column=column)


# %%
column = 'JobRole'
draw_this_column(column=column)


# %%
column = 'JobSatisfaction'
draw_this_column(column=column)


# %%
column = 'MaritalStatus'
draw_this_column(column=column)


# %%
column = 'MonthlyIncome'
draw_this_column(column=column)


# %%
column = 'MonthlyRate'
draw_this_column(column=column)


# %%
column = 'NumCompaniesWorked'
draw_this_column(column=column)


# %%
column = 'Over18'
draw_this_column(column=column)


# %%
column = 'OverTime'
draw_this_column(column=column)


# %%
column = 'PercentSalaryHike'
draw_this_column(column=column)


# %%
column = 'PerformanceRating'
draw_this_column(column=column)


# %%
column = 'RelationshipSatisfaction'
draw_this_column(column=column)


# # %%
# column = 'StandardHours'
# draw_this_column(column=column)


# %%
column = 'Shift'
draw_this_column(column=column)


# %%
column = 'TotalWorkingYears'
draw_this_column(column=column)


# %%
column = 'TrainingTimesLastYear'
draw_this_column(column=column)


# %%
column = 'WorkLifeBalance'
draw_this_column(column=column)


# %%
column = 'YearsAtCompany'
draw_this_column(column=column)


# %%
column = 'YearsInCurrentRole'
draw_this_column(column=column)


# %%
column = 'YearsSinceLastPromotion'
draw_this_column(column=column)


# %%
column = 'YearsWithCurrManager'
draw_this_column(column=column)

# %%
ages_list = [[18, 19, 20, 21],
             [22, 23, 24, 25],
             [26, 27, 28, 29],
             [30, 31, 32, 33],
             [34, 35, 36, 37],
             [38, 39, 40, 41]]
grouped_by_ages = {}
for age in ages_list:
    df_temp = pd.DataFrame(None)
    for num in age:
        df_temp1 = df_yes.loc[df_yes['Age'] == num]
        df_temp = pd.concat([df_temp, df_temp1])
    df_temp = df_temp.drop_duplicates(ignore_index=True)
    cate_dict = {}
    for column in df_temp.columns:        
        if column != 'Age' and column != 'Attrition' and column != 'Over18':
            temp = df_temp[column].unique().tolist()          
            list.sort(temp)
            if column not in cate_dict:
                cate_dict[column] = temp
            else:
                cate_dict[column] += temp
    grouped_by_ages[str(age)] = cate_dict

category_result = pd.DataFrame(grouped_by_ages)
category_result
# %%
