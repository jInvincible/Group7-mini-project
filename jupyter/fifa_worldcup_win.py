# %% 
# import library
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
ff_matches = pd.read_excel('Fifa_world_cup_raw3.xlsx', sheet_name='All Matches')
# ff_defails = pd.read_excel(file_path, sheet_name='Match Details')

# %%
# data information
ff_matches.info()
# %%
# ff_defails.info()

# %%
# drop the first columns since no use
ff_matches = ff_matches.drop(columns=ff_matches.columns[0])
# ff_defails = ff_defails.drop(columns=ff_defails.columns[0])

# %% 
# convert Date to datetime type
ff_matches['Date'] = pd.to_datetime(ff_matches['Date'])

# %%
# convert Time to datetime type
# ff_matches['Time'] = pd.to_datetime(ff_matches['Time'])

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



# %% 
# create column Winstats, New HT Goals, New AT Goals
ff_matches['Winstats'] = 0
ff_matches['New HT Goals'] = ff_matches['HT Goals'].copy()
ff_matches['New AT Goals'] = ff_matches['AT Goals'].copy()

# %% 
# replace non-numeric chatacters from New HT Goals, New AT Goals
ff_matches[['New AT Goals','New HT Goals']] = ff_matches[['New AT Goals','New HT Goals']].replace(to_replace='\D+', value='', regex=True)

# %% 
# clean up leading and ending spaces
ff_matches = ff_matches.replace(to_replace=r'^\\s+', value='', regex=True)
ff_matches = ff_matches.replace(to_replace=r'\\s+$', value='', regex=True)

# %% 
# astype the 2 columns above to 'int64' dtype
ff_matches[['New HT Goals', 'New AT Goals']] = ff_matches[['New HT Goals', 'New AT Goals']].astype('int64')

# %% 
# set Winstats = 1 if values in New HT Goals larger than New AT Goals
ff_matches['Winstats'][ff_matches['New HT Goals']-ff_matches['New AT Goals']>0] = 1
# %% 
# set Winstats = -1 if values in New HT Goals smaller than New AT Goals
ff_matches['Winstats'][ff_matches['New HT Goals']-ff_matches['New AT Goals']< 0] = -1

# %%
# retrieve attended country
countries_list = list(set(pd.concat([ff_matches['Home Team'], ff_matches['Away Team']], axis=0)))
# %%
# Generate winrate of countries_list
win_dict = {}
for country in countries_list:    
    for i, name in enumerate(ff_matches['Home Team']):
        if country == name:
            if country not in win_dict:
                win_dict[country] = {'win':0, 'draw': 0, 'lose': 0}
            if ff_matches.loc[i, 'Winstats'] == 1:
                win_dict[country]['win'] += 1
            elif ff_matches.loc[i, 'Winstats'] == -1:
                win_dict[country]['lose'] += 1
            elif ff_matches.loc[i, 'Winstats'] == 0:
                win_dict[country]['draw'] += 1
    for i, name in enumerate(ff_matches['Away Team']):
        if country == name:
            if country not in win_dict:
                win_dict[country] = {'win':0, 'draw': 0, 'lose': 0}
            if ff_matches.loc[i, 'Winstats'] == 1:
                win_dict[country]['win'] += 1
            elif ff_matches.loc[i, 'Winstats'] == -1:
                win_dict[country]['lose'] += 1
            elif ff_matches.loc[i, 'Winstats'] == 0:
                win_dict[country]['draw'] += 1
            
# %%
# create df_winrate_by_country
df_win_of_country = pd.DataFrame(win_dict)

# %%
def percentage(col):
    num = col.value_counts()
    sum = col.sum()
    return num/sum
    
df_winrate_of_country = df_win_of_country.apply(percentage)

# %%
df_win_of_country['Yugoslavia']
# %%
df_win_of_country = df_win_of_country.sort_index(axis=1)

# %%
for country in countries_list:
    a = df_win_of_country[country]
    print(a)
# %%
