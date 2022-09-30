# %%
from base64 import encode
from dataclasses import asdict
from datetime import datetime
import encodings
from re import T
from stat import SF_APPEND
from turtle import end_fill
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
# %% count number of value 'missing'
ff_matches.value_counts()

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
# %%
match_table = ff_matches.pivot_table(index='Stadium', columns='Year').agg({'Match Attendance': 'sum'})
# %%
