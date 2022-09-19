import re
import bs4
import requests
import pandas as pd
import numpy as np

# variables
# group_list sample
default_group_list = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5',
                      'Group 6', 'Group 7', 'Group 8', 'Group A', 'Group B',
                      'Group C', 'Group D', 'Group E', 'Group F', 'Group G',
                      'Group H'
                      ]

# knockout_list sample
default_knockout_list = ['Semi-finals', 'Final', 'Preliminary round',
                         'Quarter-finals', 'Semi-finals', 'Match for third place',
                         'First round', 'Round of 16', 'Third place',
                         'Play-off for third place']

# url summary page
url = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'

# request content
r = requests.get(url)

# parse HTML code
soup = bs4.BeautifulSoup(r.text, 'html.parser')

# create group_list
headline_group = soup.find_all(attrs='mw-headline', text=default_group_list)
group_list = [group.text for group in headline_group]

headline_knockout = soup.find_all(attrs='mw-headline', text=default_knockout_list)
knockout_list = [rounds.text for rounds in headline_knockout]

# check number of matches each group
url_group = [f'{url}/{group}'.replace(' ', '_') for group in group_list]
dic = dict.fromkeys(group_list, [])

url_groupA ='https://en.wikipedia.org/wiki/2018_FIFA_World_Cup/Group_A'
r_A = requests.get(url_groupA)
soup_A = bs4.BeautifulSoup(r_A.text, 'html.parser')
match_count_A = soup_A.find_all(name='table', attrs='wikitable')



# create dictionary with key = group and value = list of matches


# date and time
date_f = soup.find_all(attrs='bday dtstart published updated')
date_list = [date.text for date in date_f]
time_f = soup.find_all(attrs='ftime')
time_list = [time.text[0:5] for time in time_f]

# stage

