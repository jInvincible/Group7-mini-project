# %% Import libraries
from graphlib import TopologicalSorter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %% Import Data
df = pd.read_csv('raw_watson_healthcare.csv')


# %% Explore Data
df.info()


# %%
df.columns


# %% Correct column title
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

# uppercase first charracter using title
# list out all object columns
obj_cols_list = df.select_dtypes(include=['object']).columns.to_list()
for col in obj_cols_list:
    df[col] = df[col].str.title()
    

# %%
# generate data groupby
data = {}
for column in df.columns:
    data[column] = df.groupby([column, 'Attrition']).agg({'Attrition': 'count'})


# %%
main = 'Age'
# prepare data for Attrition count by Age
a_age = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (16,10)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Age'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
# prepare data for Attrition count by BusinessTravel
main = 'BusinessTravel'
a_biztravel = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Business Travel'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
# prepare data for Attrition count by DailyRate
main = 'DailyRate'
a_drate = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (16,10)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 90
top_display = int(top/2)
chart_xlabel = 'Daily Rate'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))      

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'Department'
# prepare data for Attrition count by Department
a_dep = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Department'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))    

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'DistanceFromHome'
# prepare data for Attrition count by DistanceFromHome
a_distfromhome = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (8,6)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Distance From Home'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))    

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()

# %%
main = 'Education'
# prepare data for Attrition count by Education
a_edu = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,6)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Education'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'EducationField'
# prepare data for Attrition count by EducationField
a_edufild = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Education Field'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'EnvironmentSatisfaction'
# prepare data for Attrition count by EnvironmentSatisfaction
a_envsat = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Environment Satisfaction'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()

# %%
main = 'Gender'
# prepare data for Attrition count by Gender
a_gender = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (4,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Gender'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'HourlyRate'
# prepare data for Attrition count by HourlyRate
a_hrate = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (15,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 90
top_display = int(top/2)
chart_xlabel = 'Hourly Rate'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()



# %%
main = 'JobInvolvement'
# prepare data for Attrition count by JobInvolvement
a_jevol = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Job Involvement'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'JobLevel'
# prepare data for Attrition count by JobLevel
a_jlevel = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Job Level'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()



# %%
main = 'JobRole'
# prepare data for Attrition count by JobRole
a_jrole = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'JobRole'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()



# %%
main = 'JobSatisfaction'
# prepare data for Attrition count by JobSatisfaction
a_jsat = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Job Satisfaction'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()



# %%
main = 'MaritalStatus'
# prepare data for Attrition count by MaritalStatus
a_mstat = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (4,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Marital Status'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()



# %%
main = 'MonthlyIncome'
# prepare data for Attrition count by MonthlyIncome
a_income = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (16,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 90
top_display = int(top/2)
chart_xlabel = 'Monthly Income'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()



# %%
main = 'MonthlyRate'
# prepare data for Attrition count by MonthlyRate
a_mrate = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (16,4)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 90
top_display = int(top/2)
chart_xlabel = 'Monthly Rate'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()



# %%
main = 'NumCompaniesWorked'
# prepare data for Attrition count by NumCompaniesWorked
a_nocomp = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Num Companies Worked'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'Over18'
# prepare data for Attrition count by Over18
a_over18 = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (2,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Over 18'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'OverTime'
# prepare data for Attrition count by OverTime
a_ot = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (3,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'OverTime'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'PercentSalaryHike'
# prepare data for Attrition count by 
a_pctsalhike = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (6,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Percent Salary Hike'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'PerformanceRating'
# prepare data for Attrition count by PerformanceRating
a_perfrate = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (3,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Performance Rating'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'RelationshipSatisfaction'
# prepare data for Attrition count by 
a_relsat = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,6)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Relationship Satisfaction'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'StandardHours'
# prepare data for Attrition count by StandardHours
a_stdhours = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (3,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Standard Hours'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'Shift'
# prepare data for Attrition count by Shift
a_shift = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Shift'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'TotalWorkingYears'
# prepare data for Attrition count by TotalWorkingYears
a_totalworkyear = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (13,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Total Working Years'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'TrainingTimesLastYear'
# prepare data for Attrition count by TrainingTimesLastYear
a_traintimelastyear = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Training Times Last Year'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'WorkLifeBalance'
# prepare data for Attrition count by WorkLifeBalance
a_worklifebalance = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (5,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Work Life Balance'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'YearsAtCompany'
# prepare data for Attrition count by YearsAtCompany
a_yearsatcomp = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (12,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Years At Company'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'YearsInCurrentRole'
# prepare data for Attrition count by 
a_yearsincurrole = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,5)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Years In Current Role'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'YearsSinceLastPromotion'
# prepare data for Attrition count by 
a_yearslastpromote = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,10)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Years Since Last Promotion'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
main = 'YearsWithCurrManager'
# prepare data for Attrition count by YearsWithCurrManager
a_yearswithcurboss = data[main]
a_chart_data = data[main]
a_y_n = a_chart_data.rename(columns={'Attrition':'Count'}).reset_index()
a_no = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])
a_yes = pd.DataFrame({main: None, 'Attrition': None,
                                        'Count': None}, index=[])

for a in set(a_y_n[main]):
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]).empty:
        a_no = pd.concat([a_no, pd.DataFrame({main: a, 'Attrition': 'No','Count': 0}, index=[1])])
    else:
        a_no = pd.concat([a_no, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'No')]])
    if (a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]).empty:
        a_yes = pd.concat([a_yes, pd.DataFrame({main: a, 'Attrition': 'Yes','Count': 0}, index=[2])])
    else:
        a_yes = pd.concat([a_yes, a_y_n[(a_y_n[main] == a) & (a_y_n['Attrition']== 'Yes')]])

a_yes1 = a_yes.copy()

# add Sort column as Yes Count
a_yes1 = a_yes1.sort_values(by=main, ignore_index=True)
a_yes = a_yes.sort_values(by=main, ignore_index=True)
a_no = a_no.sort_values(by=main, ignore_index=True)
a_yes['Sort'] = a_yes1.loc[:, 'Count']
a_no['Sort'] = a_yes1.loc[:, 'Count']

a_y_n1 = pd.concat([a_yes, a_no])

# create chart settings
if len(set(a_y_n1[main])) > 100:
    top = 100
else:
    top = len(set(a_y_n1[main]))*2
fgsize = (7,7)
bar_thick = 0.5
df_chart = a_y_n1.copy()
df_chart = df_chart.sort_values(by=['Sort', main], ascending=False, ignore_index=True).head(top)
chart_y_mean = round(df_chart['Sort'].mean(),2)
chart_y_max = df_chart['Sort'].max()
chart_max = df_chart['Count'].max()
names_rotation = 0
top_display = int(top/2)
chart_xlabel = 'Years With Current Manager'
chart_ylabel = 'Attrition counts'
if top_display > 5:
    chart_title = f'Top {top_display} {chart_ylabel} by {chart_xlabel}'
else:
    chart_title = f'{top_display} {chart_ylabel} by {chart_xlabel}'

# create yes_bar, no_bar and names list
yes_bar = df_chart.loc[df_chart['Attrition'] == 'Yes', 'Count'].to_list()
no_bar = df_chart.loc[df_chart['Attrition'] == 'No', 'Count'].to_list()
names = []
for a in df_chart[main]:
    if str(a) not in names:
        names.append(str(a))
names = [name.replace(' ', '\n') if ' ' in name else name for name in names]
names = [name.replace('_', '\n') if '_' in name else name for name in names]
names = [name.replace('-', '\n') if '-' in name else name for name in names]
r = np.arange(len(set(df_chart[main])))   

# start drawing chart
fig, ax = plt.subplots(figsize=fgsize)

ax.bar(r, yes_bar, color='#af0b1e', edgecolor='white',width= bar_thick, label = 'Yes')
ax.bar(r, no_bar, bottom = yes_bar, color='#18384e', edgecolor='white', width= bar_thick, label = 'No')

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1))

# custom x axis
plt.xticks(r, names, rotation = names_rotation) # set the name for each Bar
ax.set_xlim(-0.5,len(r)-0.5)
ax.set_xlabel(chart_xlabel)
ax.set_ylabel(chart_ylabel)
plt.tick_params(bottom=0, left=0) # disable the tick from bottom side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add a line
ax.axline(xy1=(0,chart_y_max), xy2=(15,chart_y_max) , ls=':', color = 'orange')
ax.axline(xy1=(0,chart_y_mean), xy2=(15,chart_y_mean) , ls=':', color = 'white')

# add chart title
ax.set_title(label=chart_title)
ax.text(x=len(r), y=chart_y_max+chart_max*0.02, s=f'max = {chart_y_max}')
ax.text(x=len(r), y=chart_y_mean-chart_max*0.02, s=f'mean = {chart_y_mean}')

plt.show()


# %%
tmp_biztravel = a_biztravel.copy()

# %%
tmp_biztravel = tmp_biztravel.rename(columns={'Attrition': 'Count'}).reset_index()

# %%
tmp = pd.DataFrame({'BusinessTravel': None, 'No': None, 'Yes': None}, index=[])
for biz in set(tmp_biztravel['BusinessTravel']):
    yes = tmp_biztravel[((tmp_biztravel['BusinessTravel']==biz) & (tmp_biztravel['Attrition']=='Yes')), 'Count']
    no = tmp_biztravel[((tmp_biztravel['BusinessTravel']==biz) & (tmp_biztravel['Attrition']=='No')), 'Count']
    biz = pd.DataFrame({'BusinessTravel': biz, 'No': no, 'Yes': yes}, index=[])
    tmp = pd.concat([tmp,biz])

# %%



# %%





