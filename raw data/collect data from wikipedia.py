import re
import bs4
import requests
import pandas as pd
import numpy as np

# variables
default_round_list = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5',
                      'Group 6', 'Group 7', 'Group 8', 'Group A', 'Group B',
                      'Group C', 'Group D', 'Group E', 'Group F', 'Group G',
                      'Group H', 'Semi-finals', 'Final', 'Preliminary round',
                      'Quarter-finals', 'Semi-finals', 'Match for third place',
                      'First round','Round of 16', 'Third place',
                      'Play-off for third place'
                      ]

# url
url = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'
#https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_Group_A

# request content
r = requests.get(url)

# parse HTML code
soup = bs4.BeautifulSoup(r.text, 'html.parser')

# create round_list
headline = soup.find_all(attrs='mw-headline', text=default_round_list)
round_list = [round.text for round in headline]

# date and time
date_f = soup.find_all(attrs='bday dtstart published updated')
date_list = [date.text for date in date_f]
time_f = soup.find_all(attrs='ftime')
time_list = [time.text[0:5] for time in time_f]

# stage

