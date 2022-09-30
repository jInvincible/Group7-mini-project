# %%
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %%
# Variables
file_path = 'C:\\Users\\Nam Invincible\\PycharmProjects\\Group7-mini-project\\Fifa_world_cup_raw2.xlsx'


# %%
ff_matches = pd.read_excel(file_path, sheet_name='All Matches')
ff_defails = pd.read_excel(file_path, sheet_name='Match Details')

# %%
ff_matches.info()
# %%
ff_defails.info()

# %%
ff_matches = ff_matches.drop(columns=ff_matches.columns[0])
ff_defails = ff_defails.drop(columns=ff_defails.columns[0])

# %% change value 'missing' to '' from column [Time]
ff_matches['Time'][ff_matches['Time'] == 'missing'] = ff_matches['Time'].replace(to_replace='missing', value='')

# %%
ff_matches['Time'][ff_matches['Time'] == 'w/o detail in /wiki/Walkover'] = ff_matches['Time'].replace(to_replace='w/o detail in /wiki/Walkover', value='')

# %%
ff_matches['Time'][ff_matches['Time'] == 'missing']

# %%
ff_matches['Time'][ff_matches['Time'] == 'w/o detail in /wiki/Walkover']

# %% convert Date to datetime type
ff_matches['Date'] = pd.to_datetime(ff_matches['Date'])

# %%
ff_matches['Time'] = pd.to_datetime(ff_matches['Time'])

# # %%
# match_count_stadium_in_location = ff_matches.pivot_table(index='Location', columns='Year', values = 'Stadium', aggfunc='nunique', fill_value=0)


# # %%
# stadium_in_year = ff_matches.pivot_table(index='Year',values='Stadium',aggfunc='nunique', fill_value=0)
# # %%
# func = lambda x: round(x/x.sum()*100,2)
# stadium_in_year['Stadium(pct)'] = func(stadium_in_year['Stadium'])
# # %%
# fig, ax = plt.subplots(figsize=(11,6))
# graphs1 = ax.bar(np.arange(len(stadium_in_year)),stadium_in_year['Stadium(pct)'], tick_label=stadium_in_year.index, width=0.8, color='#af0b1e', align='center')
# plt.xticks(rotation=45)
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.set_ylabel('Numbers of Stadium')

# ax.tick_params(bottom=False)

# year = list(stadium_in_year.index)


# for i, p in enumerate(graphs1):
#     x, y = p.get_xy()
#     width_p = p.get_width()
#     height_p = p.get_height()
#     plt.text(x=x+width_p/2, y=height_p/2.7, s=str(stadium_in_year['Stadium(pct)'][year[i]])+'%', ha = 'center', rotation=90)

# %% create column Winstats, New HT Goals, New AT Goals
ff_matches['Winstats'] = 0
ff_matches['New HT Goals'] = ff_matches['HT Goals'].copy()
ff_matches['New AT Goals'] = ff_matches['AT Goals'].copy()

# %% drop row w/o
mask = ff_matches['New AT Goals']=='w/o detail in /wiki/Walkover'

# %%
ff_matches.loc[mask,'New AT Goals'] = '0'
ff_matches.loc[mask,'New HT Goals'] = '1'
ff_matches.loc[mask,'Winstats'] = 1

# %% replace unnumeric chatacters from New HT Goals, New AT Goals
ff_matches[['New AT Goals','New HT Goals']] = ff_matches[['New AT Goals','New HT Goals']].replace('\D+','', regex=True)

# %% astype to int the 2 columns above
ff_matches[['New HT Goals', 'New AT Goals']] = ff_matches[['New HT Goals', 'New AT Goals']].astype('int64')
# %% set Winstats = 1 if values in New HT Goals larger than New AT Goals
ff_matches['Winstats'][ff_matches['New HT Goals']-ff_matches['New AT Goals']>0] = 1
# %% set Winstats = -1 if values in New HT Goals smaller than New AT Goals
ff_matches['Winstats'][ff_matches['New HT Goals']-ff_matches['New AT Goals']< 0] = -1

