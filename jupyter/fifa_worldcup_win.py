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
ff_matches['Date'] = pd.to_datetime(ff_matches['Date'])#, format='%d %B %Y', exact=False)

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
            if ff_matches.loc[i, 'Winstats'] == -1:
                win_dict[country]['win'] += 1
            elif ff_matches.loc[i, 'Winstats'] == 1:
                win_dict[country]['lose'] += 1
            elif ff_matches.loc[i, 'Winstats'] == 0:
                win_dict[country]['draw'] += 1
            
# %%
# create df_win_by_country
df_win_of_country = pd.DataFrame(win_dict).T

# %%
# create columns total in df_win_by_country
df_win_of_country['total'] = df_win_of_country.sum(axis=1)

# %%
def percent(element):
    return round(element/df_win_of_country['total'],3)
    
df_winrate_of_country = df_win_of_country.apply(percent)

# %%
# create top 10 country by winrate
top_10_winrate_country = df_winrate_of_country.sort_values(by='win', ascending=False).head(10).drop(columns='total')

# %%
# list(top_10_winrate_country['win'])
# [i for i in top_10_winrate_country['win']]
# tuple(top_10_winrate_country.index)

# %%
# create 100% stacked bar
# prepair data in percentage
df=top_10_winrate_country.copy()
r = [0,1,2,3,4,5,6,7,8,9]
winBars = list(df['win'])
drawBars = list(df['draw'])
loseBars = list(df['lose'])

# plot
barWidth = 0.85
names = tuple(df.index)

# Create green Bars
plt.bar(r, winBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="win")
# Create orange Bars
plt.bar(r, drawBars, bottom=winBars, color='#f9bc86', edgecolor='white', width=barWidth, label="draw")
# Create blue Bars
plt.bar(r, loseBars, bottom=[i+j for i,j in zip(winBars, drawBars)], color='#a3acff', edgecolor='white', width=barWidth, label="lose")
 
# Custom x axis
plt.xticks(r, names, rotation=90)
plt.ylabel("Percentage")
 
# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
 
# Show graphic
plt.show()

# %%
# create 100% stacked bar
# prepair data in percentage
df=top_10_winrate_country.sort_values(by='win', ascending=True).copy()
r = [0,1,2,3,4,5,6,7,8,9]
winBars = list(df['win']*100)
drawBars = list(df['draw']*100)
loseBars = list(df['lose']*100)

# plot info
barHeight = 0.85
names = tuple(df.index)
fig, ax = plt.subplots()
# create win Bars
ax.barh(r, winBars, color='#af0b1e', edgecolor='white', height=barHeight, label="win")
# create draw Bars
ax.barh(r, drawBars, left=winBars, color='#f9bc86', edgecolor='white', height=barHeight, label="draw")
# create lose Bars
ax.barh(r, loseBars, left=[i+j for i,j in zip(winBars, drawBars)], color='#a3acff', edgecolor='white', height=barHeight, label="lose")
 
# custom x axis
plt.yticks(r, names) # set the name of each Bar
ax.set_xticks([0,25,75,100]) # overwrite the xticks at the bottom
plt.tick_params(bottom=0, left=0) # disable the tick from bottom and left side
plt.xlabel("Percent")

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)
 
# add a legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
 
# add a line
ax.axvline(x=50, ls=':', color = 'white', ymin=0.02, ymax=0.95)
ax.text(x=50, y=-1.2, s='50', ha='center')
ax.set_title(label='Top 10 Countries of Winning Rate of WorldCup')

# show graph
plt.show()


# %%
# create columns Region
# regions_list = pd.read_excel('List of countries by regional classification.xlsx', sheet_name='Region List')

# df_winrate_of_country['Region'] = 0

# %%
# df_winrate_of_country = df_winrate_of_country.reset_index()
# %%
# def map_region(element):
#     if element == regions_list['']

# df_winrate_of_country['Region'] = df_winrate_of_country['index'].apply(map_region)
# %%
# mask = [df_winrate_of_country['index'].isin(regions_list['Country'])]

# %%
temp_merged = pd.merge(left=df_winrate_of_country, right=regions_list, left_on=df_winrate_of_country['index'], how='left',right_on=regions_list['Country'])
temp_merged = temp_merged.drop(columns=['Region_x', 'Country', 'Global South'])
# %%
# null_value = temp_merged['Region_y'].isnull().sum()
# %%
# temp_merged.to_excel('winrate.xlsx', sheet_name='sheet1')
# %%
