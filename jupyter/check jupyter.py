#%%
# import libs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# add datas
excel_file = pd.ExcelFile('Fifa_world_cup_raw3.xlsx')
ff_matches = pd.read_excel(excel_file, sheet_name='All Matches')
ff_details = pd.read_excel(excel_file, sheet_name='Match Details')
regions_list = pd.read_excel('regions_list.xlsx', sheet_name='region list')

# %%
# clean up leading and ending spaces
ff_matches = ff_matches.replace(to_replace='^\\s+', value='', regex=True)
ff_matches = ff_matches.replace(to_replace='\\s+$', value='', regex=True)
ff_details = ff_details.replace(to_replace='^\\s+', value='', regex=True)
ff_details = ff_details.replace(to_replace='\\s+$', value='', regex=True)
ff_details['HT Discipline'] = ff_details['HT Discipline'].replace('None', '0')
ff_details['HT Discipline'] = ff_details['HT Discipline'].replace('missing', '0')
ff_details['HT Discipline'] = ff_details['HT Discipline'].fillna('0')
ff_details['HT Discipline'] = ff_details['HT Discipline'].replace(r'\[.\]', '', regex=True)
ff_details.loc[ff_details['HT Discipline'].str.count(r"'") == 3.0, 'HT Discipline'] = '3'
ff_details.loc[ff_details['HT Discipline'].str.count(r"'") == 2.0, 'HT Discipline'] = '2'
ff_details.loc[ff_details['HT Discipline'].str.count(r"'") == 1.0, 'HT Discipline'] = '1'
ff_details['AT Discipline'] = ff_details['AT Discipline'].replace('None', '0')
ff_details['AT Discipline'] = ff_details['AT Discipline'].replace('missing', '0')
ff_details['AT Discipline'] = ff_details['HT Discipline'].replace(r'\[.\]', '0')
ff_details['AT Discipline'] = ff_details['AT Discipline'].fillna('0')
ff_details.loc[ff_details['AT Discipline'].str.count(r"'") == 3.0, 'AT Discipline'] = '3'
ff_details.loc[ff_details['AT Discipline'].str.count(r"'") == 2.0, 'AT Discipline'] = '2'
ff_details.loc[ff_details['AT Discipline'].str.count(r"'") == 1.0, 'AT Discipline'] = '1'

# create column Winstats, New HT Goals, New AT Goals
ff_matches['Winstats'] = 0
ff_matches['New HT Goals'] = ff_matches['HT Goals'].copy()
ff_matches['New AT Goals'] = ff_matches['AT Goals'].copy()

# clear non-numeric chatacters from New HT Goals, New AT Goals
ff_matches[['New AT Goals','New HT Goals']] = ff_matches[['New AT Goals','New HT Goals']].replace(to_replace='\D+', value='', regex=True)

# change dtype of the 2 columns to 'int64'
ff_matches[['New HT Goals', 'New AT Goals']] = ff_matches[['New HT Goals', 'New AT Goals']].astype('int64')
ff_details[['AT Discipline', 'HT Discipline']] = ff_details[['AT Discipline', 'HT Discipline']].astype('int64')

# convert Date to datetime type
ff_matches['Date'] = pd.to_datetime(ff_matches['Date'])

# set Winstats = 1 if values in New HT Goals larger than New AT Goals
mask_1 = ff_matches['New HT Goals']-ff_matches['New AT Goals']> 0
ff_matches.loc[mask_1, 'Winstats'] = 1

# set Winstats = -1 if values in New HT Goals smaller than New AT Goals
mask_neg1 = ff_matches['New HT Goals']-ff_matches['New AT Goals']< 0
ff_matches.loc[mask_neg1, 'Winstats'] = -1
# %%
# retrieve set of country name
countries_list = list(set(pd.concat([ff_matches['Home Team'], ff_matches['Away Team']], axis=0)))

# Generate team_info_dict from countries_list and ff_matches
team_info_dict = {}
for country in countries_list:    
    for i, name in enumerate(ff_matches['Home Team']):
        if country == name:
            if country not in team_info_dict:
                team_info_dict[country] = {'win':0, 'draw': 0, 'lose': 0, 'goals': 0, 'matches': 0}
            if ff_matches.loc[i, 'Winstats'] == 1:
                team_info_dict[country]['win'] += 1
            elif ff_matches.loc[i, 'Winstats'] == -1:
                team_info_dict[country]['lose'] += 1
            elif ff_matches.loc[i, 'Winstats'] == 0:
                team_info_dict[country]['draw'] += 1
            team_info_dict[country]['goals'] += ff_matches.loc[i, 'New HT Goals']
            team_info_dict[country]['matches'] += 1
                
    for i, name in enumerate(ff_matches['Away Team']):
        if country == name:
            if country not in team_info_dict:
                team_info_dict[country] = {'win':0, 'draw': 0, 'lose': 0, 'goals': 0, 'matches': 0}
            if ff_matches.loc[i, 'Winstats'] == -1:
                team_info_dict[country]['win'] += 1
            elif ff_matches.loc[i, 'Winstats'] == 1:
                team_info_dict[country]['lose'] += 1
            elif ff_matches.loc[i, 'Winstats'] == 0:
                team_info_dict[country]['draw'] += 1
            team_info_dict[country]['goals'] += ff_matches.loc[i, 'New AT Goals']
            team_info_dict[country]['matches'] += 1
         
# create df_team_info
df_team_info = pd.DataFrame(team_info_dict).T

# create df_winrate
def percent(element):
    return round(element/df_team_info['matches'],3)

df_winrate = df_team_info.copy()
df_winrate[['win','draw','lose']] = df_winrate[['win','draw','lose']].apply(percent)
df_winrate[['goals']] = df_winrate[['goals']].apply(percent)
# %%
# create top 10 countries by winrate
top_10_winrate_country = df_winrate[['win','draw','lose']].sort_values(by='win', ascending=False).head(10)

# create 100% stacked bar for top 10 winrate of country
# prepair data in percentage
df=top_10_winrate_country.sort_values(by='win', ascending=True).copy()
r = range(len(df))
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
ax.barh(r, drawBars, left=winBars, color='grey', edgecolor='white', height=barHeight, label="draw")
# create lose Bars
ax.barh(r, loseBars, left=[i+j for i,j in zip(winBars, drawBars)], color='#18384e', edgecolor='white', height=barHeight, label="lose")
 
# custom x axis
plt.yticks(r, names) # set the name of each Bar
ax.set_xticks([0,25,50,75,100]) # overwrite the xticks at the bottom
plt.tick_params(bottom=0, left=0) # disable the tick from bottom and left side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)
 
# add a legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
 
# add a line
ax.axvline(x=50, ls=':', color = 'white', ymin=0.05, ymax=0.95)
ax.set_title(label='Top 10 Country of Winning rate')

# show graph
plt.show()

# %%
# apply map_region to Region column in df_winrate
def map_region(name):
    for i, country in enumerate(regions_list['Country']):
        if name == country:
            return regions_list.loc[i, 'Region']
        else:
            pass
    return 'not listed'
df_winrate = df_winrate.reset_index()
df_winrate = df_winrate.rename(columns={'index':'Country'})
df_winrate['Region'] = df_winrate['Country'].apply(map_region)
df_winrate_of_region = pd.pivot_table(data=df_winrate,index='Region', aggfunc='mean').sort_values(by='win', ascending=0)[['win','draw','lose']]

# create 100% stacked bar for winrate of region
# prepair data in percentage
df = df_winrate_of_region.sort_values(by='win', ascending=True).copy()
r = range(len(df))
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
ax.barh(r, drawBars, left=winBars, color='grey', edgecolor='white', height=barHeight, label="draw")
# create lose Bars
ax.barh(r, loseBars, left=[i+j for i,j in zip(winBars, drawBars)], color='#18384e', edgecolor='white', height=barHeight, label="lose")
 
# custom x axis
plt.yticks(r, names) # set the name of each Bar
ax.set_xticks([0,25,50,75,100]) # overwrite the xticks at the bottom
plt.tick_params(bottom=0, left=0) # disable the tick from bottom and left side

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# add legend
ax.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
 
# add a line
ax.axvline(x=50, ls=':', color = 'white', ymin=0.05, ymax=0.95)
ax.set_title(label='The Winning Rate by Region')

# show graph
plt.show()

# %%
year_list = list(set(ff_matches['Year']))
df_final_stage = pd.DataFrame(None)
for year in year_list:
    df_final = ff_matches[((ff_matches['Stage'] == 'final round')| (ff_matches['Stage'] == 'final tournament')|(ff_matches['Stage'] == 'knockout stage')) & (ff_matches['Year'] == year)].iloc[[-2, -1], :]
    df_final_stage = pd.concat([df_final_stage, df_final],axis=0)

attend_final_country = list(set(pd.concat([df_final_stage['Home Team'], df_final_stage['Away Team']], axis=0)))

attend_counter = {}
for country in attend_final_country:    
    for name in df_final_stage['Home Team']:
        if country == name:
            try: 
                if attend_counter[country] > 0:
                    attend_counter[country] += 1
            except KeyError:
                attend_counter[country] = 1
            
    for name in df_final_stage['Away Team']:
        if country == name:
            try: 
                if attend_counter[country] > 0:
                    attend_counter[country] += 1
            except KeyError:
                attend_counter[country] = 1                

df_final_stage_count = pd.DataFrame(data=attend_counter, index=['Attend']).T
df_final_stage_count = df_final_stage_count.reset_index()

def mapping_(element):
    for i, item in enumerate(df_winrate['Country']):
        if element == item:
            return df_winrate.loc[i, 'win']
        else:
            pass
    return 'not found'

df_final_stage_count['win'] = df_final_stage_count['index'].apply(mapping_)
df_final_stage_count = df_final_stage_count.sort_values(by='win', ascending=0)


# %%
# create df_avg_goal and top 10 avg goal
df_avg_goal = df_winrate[['Country', 'win', 'goals']].copy().sort_values(by='goals', ascending=0)
top_10_country_by_avg_goal = df_avg_goal.head(10)

# Create BarH chart of Top 10 Countries of Average Goal
df = top_10_country_by_avg_goal.sort_values(by='goals', ascending=True).copy()
fig, ax = plt.subplots(figsize=(8,6))
r = range(len(df))
barHeight = 0.8
names = df['Country']
ax.barh(r, df['goals'], color='#af0b1e', edgecolor='white', height=barHeight, label='attend')
plt.yticks(r, names)
plt.tick_params(bottom=0, left=0)

for pos in ['top', 'left', 'right', 'bottom']:
    ax.spines[pos].set_visible(0)

# set xticks 
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
ax.set_xlim(0,3)
ax.set_xlabel('Goals per match')

ax.axvline(x=1.5, ls=':', color = 'white', ymin=0.05, ymax=0.95)
ax.set_title(label='Top 10 Countries of Average Goal', y = -0.03)
plt.show()
# %%
