import re
import bs4
import requests
import pandas as pd

## MAIN
url = 'https://web.archive.org/web/20200224034607/https://www.fifa.com/worldcup/archive/russia2018/matches/#groupphase'
url1 = 'https://web.archive.org/web/20200224034607/https://www.fifa.com/worldcup/archive/russia2018/matches/#knockoutphase'

# content of URL
r = requests.get(url)
r1 = requests.get(url1)

# Parse HTML Code
soup = bs4.BeautifulSoup(r.text, 'html.parser')
soup1 = bs4.BeautifulSoup(r1.text, 'html.parser')

# date_time_list fi-mu__info__datetime
r_date_time = soup.find_all(attrs='fi-mu__info__datetime')
f_date_time = [r.next for r in r_date_time]
date_time_list = []
for text in f_date_time:
    text = text.replace('\n', '')
    text = text.strip()
    date_time_list.append(text)

# group_list fi-groupPhase fi__info__group fi-ltr--force
r_group = soup.find_all(attrs='fi-groupPhase fi__info__group fi-ltr--force')
group_list = [r.text for r in r_group]
r1_group = soup1.find_all(attrs='fi-knockout fi__info__group fi-ltr--force')
group_list1 = [r1.text for r1 in r1_group]
total_group_list = group_list + group_list1

# stadium fi__info__stadium
r_stadium = soup.find_all(attrs='fi__info__stadium')
stadium_list = [r.text for r in r_stadium]

# home team fi-t fi-i--4 home >fi-t__nText
r_home = soup.find_all(attrs='fi-t fi-i--4 home')
f_home = [str(txt) for txt in r_home]
home_team_list = []
for home in f_home:
    home = home.replace('\n', '')
    home = home.replace('\"', '')
    home1 = re.search(r't>([\w+\s\w+]+)', string=home)[0].replace('t>', '')
    home_team_list.append(home1)

# score fi-s__scoreText
r_score = soup.find_all(attrs='fi-s__scoreText')
total_score_list = [r.next.replace('\n', '').strip() for r in r_score]
home_team_goals = []
away_team_goals = []
for score in total_score_list:
    score = score.split('-')
    score_home = score[0]
    score_away = score[1]
    home_team_goals.append(score_home)
    away_team_goals.append(score_away)


# away team fi-t fi-i--4 away >fi-t__nText
r_away = soup.find_all(attrs='fi-t fi-i--4 away')
f_away = [str(txt) for txt in r_away]
away_team_list = []
for away in f_away:
    away = away.replace('\n', '')
    away = away.replace('\"', '')
    away1 = re.search(r't>([\w+\s\w+]+)', string=away)[0].replace('t>', '')
    away_team_list.append(away1)

# matchid fi-mu__link a href="/tournaments/mens/worldcup/2018russia/match
# -center/300331537"
# match detail, navigate url:
# https://web.archive.org/web/20200224042316/https://www.fifa.com/worldcup/archive/russia2018/matches/match/300331503/
r_matchid = soup.find_all('a', attrs='fi-mu__link')
matchid_list = [r.contents[1].attrs['data-id'] for r in r_matchid]

url_match = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup#Group_stage'
r_match = requests.get(url_match)
soup_match = bs4.BeautifulSoup(r_match.text, 'html.parser')
r_match = soup_match.find_all('script')

# create dataframe Year, Datetime, Stage, Stadium, Home Team Name,
# Home Team Goals, Away Team Goals, Away Team Name, Attendance, RoundID,
# MatchID
s_date_time = pd.Series(date_time_list)
s_stage = pd.Series(total_group_list)
s_stadium = pd.Series(stadium_list)
s_home_team_name = pd.Series(home_team_list)
s_home_team_goals = pd.Series(home_team_goals)
s_away_team_goals = pd.Series(away_team_goals)
s_away_team_name = pd.Series(away_team_list)
s_matchid = pd.Series(matchid_list)
df = pd.DataFrame({'Datetime': s_date_time, 'Stage': s_stage,
                   'Stadium': s_stadium, 'Home Team Name': s_home_team_name,
                   'Home Team Goals': s_home_team_goals, 'Away Team Goals':
                       s_away_team_goals, 'Away Team Name': s_away_team_name,
                   'MatchID': s_matchid})
# save all collecting data to an excel file
df.to_excel('Russia2018.xlsx', sheet_name='All matchs')