import re
import bs4
import requests
import pandas as pd
import numpy as np

# variables
# group_list cdata
cdata_group_list = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5',
                    'Group 6', 'Group 7', 'Group 8', 'Group A', 'Group B',
                    'Group C', 'Group D', 'Group E', 'Group F', 'Group G',
                    'Group H'
                    ]

# knockout_list cdata
cdata_knockout_list = ['Semi-finals', 'Final', 'Preliminary round',
                       'Quarter-finals', 'Semi-finals',
                       'Match for third place',
                       'First round', 'Round of 16', 'Third place',
                       'Play-off for third place']

REPLACEMENTS = [
    ('img', {'alt': 'downward-facing red arrow'}, 'b', {}, 'O'),
    ('img', {'alt': 'upward-facing green arrow'}, 'b', {}, 'I'),
    ('img', {'alt': 'Yellow card'}, 'b', {}, 'Y'),
    ('img', {'alt': 'Yellow-red card'}, 'b', {}, 'RSY'),
    ('img', {'alt': 'Red card'}, 'b', {}, 'R'),
    ('img', {'title': 'Goal'}, 'b', {}, 'G')
]

# all columns in sheet 'All matches'
columns_year = []
columns_date = []
columns_time = []
columns_stage = []
columns_stadium = []
columns_home_team = []
columns_away_team = []
columns_home_team_goal = []
columns_away_team_goal = []
columns_attendance = []
columns_matchid = []
match_info_attrs = '\'class\':\'footballbox\''

# all columns in sheet 'Starting'
# columns_matchid this columns persist in both 2 sheets

# end variables

# custom function
def replace_tags_with_labels(html, replacements=REPLACEMENTS):
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    for tag, search_attr, new_tag, new_attr, new_string in \
            replacements:
        for node in soup.find_all(tag, search_attr):
            replacement = soup.new_tag(new_tag, **new_attr)
            replacement.string = new_string
            node.replace_with(replacement)
    return str(soup)


# end custome function

# main
# url summary page
url_main = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'

# request content
r_main = requests.get(url_main)

# parse HTML code
soup_main = bs4.BeautifulSoup(r_main.text, 'html.parser')

# replace all img tags to corresponding labels
soup_main = bs4.BeautifulSoup(replace_tags_with_labels(r_main,
                                                        replacements=REPLACEMENTS),
                               'html.parser')

# create group_list and knockout_list to get list of navigating url
headline_group = soup_main.find_all(attrs='mw-headline', text=cdata_group_list)
group_list = [group.text for group in headline_group]

headline_knockout = soup_main.find_all(attrs='mw-headline',
                                   text=cdata_knockout_list)
knockout_list = [rounds.text for rounds in headline_knockout]
all_round_list = group_list + knockout_list
next_round = ''
for counter, round in enumerate(all_round_list):
    if counter < len(all_round_list):
        match_stage = round
        if match_stage != next_round:
            next_round = all_round_list[counter+1]
    current_round_tag = soup_main.find(attrs='mw-headline', text=round).parent
    # match_stage = 'Group A'
    while current_round_tag.find(attrs='mw-headline', text=next_round) != soup_main.find(attrs='mw-headline', text=next_round) or (match_stage == next_round):
        if current_round_tag.attrs == soup_main.find(attrs={'class': 'footballbox'}).attrs:
            matches_info = current_round_tag
            # get home_team_name
            home_team_name = matches_info.find(attrs='fhome').text
            # -> HOME_TEAM_NAME

            # get away_team_name
            away_team_name = matches_info.find(attrs='faway').text
            # - > AWAY_TEAM_NAME

            # get match final score
            f_score = matches_info.find(attrs='fscore').text
            home_team_f_score = f_score.split('–')[0]
            away_team_f_score = f_score.split('–')[1]
            # -> HOME_TEAM_F_SCORE + AWAY_TEAM_F_SCORE

            # get match date
            match_date = matches_info.find(attrs='bday dtstart published updated').text
            # -> MATCH_DATE

            # get match time
            match_time = matches_info.find(attrs='ftime').next.text

            # get stadium name
            match_stadium = matches_info.find('span',
                                              attrs={'itemprop': 'name address'}).find(
                'a').text
            # -> MATCH_STADIUM

            # get attendance
            attendance_string = str(matches_info.find(text=re.compile('Attendance.*')))
            matching = re.search(pattern='[\d,]+', string=attendance_string)
            match_attendance = matching.group(0)
            # -> MATCH_ATTENDANCE

            # get referee
            match_referee = matches_info.find(text=re.compile(
                'Referee.*')).nextSibling.text
            # -> MATCH_REFEREE

            # get matchid
            matchid_tag = matches_info.find(name='a', attrs={'class': 'external text'})
            matchid = matchid_tag.attrs['href'].split('/')[-1]
            # -> MATCHID

            # make df for home_team_score
            # get score_event_tag for home_team and away_team from matches_info
            home_team_score_tag = matches_info.find(attrs={'class': 'fhgoal'})
            home_team_score_list = home_team_score_tag.text.split('\n')[1:]
            # -> HOME_TEAM_SCORE_LIST
            away_team_score_tag = matches_info.find(attrs={'class': 'fagoal'})
            away_team_score_list = away_team_score_tag.text.split('\n')[1:]
            columns_year.append(match_date[0:4])
            columns_stage.append(match_stage)
            columns_date.append(match_date)
            columns_time.append(match_time)
            columns_stadium.append(match_stadium)
            columns_home_team.append(home_team_name.replace('\xa0', ''))
            columns_home_team_goal.append(home_team_f_score)
            columns_away_team_goal.append(away_team_f_score)
            columns_away_team.append(away_team_name.replace('\xa0', ''))
            columns_attendance.append(match_attendance)
        current_round_tag = current_round_tag.nextSibling
        while current_round_tag.string == '\n':
            current_round_tag = current_round_tag.nextSibling
df_all_matches = pd.DataFrame({'Year': columns_year,'Stage': columns_stage,
                                   'Time': columns_time, 'Date': columns_date,
                                   'Stadium': columns_stadium, 'Home Team':
                                       columns_home_team, 'HT Goals':
                                       columns_home_team_goal, 'AT Goals':
                                       columns_away_team_goal, 'Away Team':
                                       columns_away_team, 'Match '
                                                               'Attendance':
                                       columns_attendance})

