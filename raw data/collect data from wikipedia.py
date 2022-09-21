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
a_check = soup_main.find(attrs='mw-headline', text='Group A')
a_check_parent = a_check.parent
b_check = a_check_parent.findNext(attrs='mw-headline', text='Group B')

cdata_all = cdata_group_list + cdata_knockout_list

# # create url_list
# url_group = [f'{url_main}_{group}' for group in group_list]
# url_knockout = [f'{url_main}_knockout_stage']
# url_list = url_group + url_knockout

    # for testing only
    # matches_info = soup.find(attrs={'class': 'footballbox'})

    # loops to get all information from each matches
    for matches_info in number_of_match:
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
        # -> AWAY_TEAM_SCORE_LIST

        # # use matches_info as anchor to find starting tag, the second table after
        # # matches_info will be correct starting tag
        # starting = matches_info.find_next_siblings('table', limit=2)[1]
        # # -> STARTING
        #
        # # creating the df of home team and away team to recognize data of starting
        # # easier
        # # get tag of home_team and away_team
        # for i, tag in enumerate(starting.tbody.tr):
        #     if i == 1:
        #         home_team_table_rows_tag = tag
        #     if i == 5:
        #         away_team_table_rows_tag = tag
        #
        # # make df home_team
        # data = []
        # table_rows = home_team_table_rows_tag.find_all('tr')
        # for tr in table_rows:
        #     td = tr.find_all('td')
        #     row = [tr.text for tr in td]
        #     data.append(row)
        #
        # df_home_team = pd.DataFrame(data, columns=['HT Role', 'HT Shirt Number',
        #                                            'HT Full Name',
        #                                            'HT Events',
        #                                            'HT Discipline'])
        #
        # # get the manager name + index from HT Role, copy to HT Full Name,
        # # drop the latest row in df_home_team
        # ht_m_index = int(df_home_team[df_home_team['HT Role'].str.contains(
        #     'Manager.*')==True].index.values)
        # ht_manager = df_home_team['HT Role'].iloc[-1]
        # df_home_team.loc[ht_m_index, 'HT Full Name'] = ht_manager
        # df_home_team = df_home_team.drop(index=len(df_home_team)-1)
        #
        # # make df away_team
        # data = []
        # table_rows = away_team_table_rows_tag.find_all('tr')
        # for tr in table_rows:
        #     td = tr.find_all('td')
        #     row = [tr.text for tr in td]
        #     data.append(row)
        #
        # df_away_team = pd.DataFrame(data, columns=['AT Role', 'AT Shirt Number',
        #                                            'AT Full Name',
        #                                            'AT Events',
        #                                            'AT Discipline'])
        # # get the manager name + index from AT Role, copy to AT Full Name,
        # # drop the latest row in df_away_team
        # at_m_index = int(df_away_team[df_away_team['AT Role'].str.contains(
        #     'Manager.*') == True].index.values)
        # at_manager = df_away_team['AT Role'].iloc[-1]
        # df_away_team.loc[at_m_index, 'AT Full Name'] = at_manager
        # df_away_team = df_away_team.drop(index=len(df_away_team) - 1)
        #
        # # make df starting of the match
        # df_starting = pd.concat([df_home_team, df_away_team], axis=1)
        # series_matchid = pd.Series([matchid] * len(df_starting))
        # series_matchid = series_matchid.rename('MatchID')
        # df_starting = pd.concat([series_matchid, df_starting], axis=1)

        # assign all collected data to corresponding list
        columns_year.append(match_date[0:4])
        columns_stage.append(match_stage)
        columns_date.append(match_date)
        columns_time.append(match_time)
        columns_stadium.append(match_stadium)
        columns_home_team.append(home_team_name.replace('\xa0',''))
        columns_home_team_goal.append(home_team_f_score)
        columns_away_team_goal.append(away_team_f_score)
        columns_away_team.append(away_team_name.replace('\xa0',''))
        columns_attendance.append(match_attendance)

df_all_matches = pd.DataFrame({'Year': columns_year,'Stage': columns_stage,
                                   'Time': columns_time, 'Date': columns_date,
                                   'Stadium': columns_stadium, 'Home Team':
                                       columns_home_team, 'HT Goals':
                                       columns_home_team_goal, 'AT Goals':
                                       columns_away_team_goal, 'Away Team':
                                       columns_away_team, 'Match '
                                                               'Attendance':
                                       columns_attendance})
