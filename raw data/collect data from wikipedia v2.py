import re
import bs4
import requests
import pandas as pd

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
                       'Play-off for third place', 'Third place play-off']

REPLACEMENTS = [
    ('img', {'alt': 'downward-facing red arrow'}, 'b', {}, 'O'),
    ('img', {'alt': 'upward-facing green arrow'}, 'b', {}, 'I'),
    ('img', {'alt': 'Yellow card'}, 'b', {}, 'Y'),
    ('img', {'alt': 'Yellow-red card'}, 'b', {}, 'RSY'),
    ('img', {'alt': 'Red card'}, 'b', {}, 'R'),
    ('img', {'title': 'Goal'}, 'b', {}, 'G'),
    ('style', {}, 'b', {}, '')
]

# all columns in sheet 'All matches'
columns_year = []
columns_date = []
columns_time = []
columns_stage = []
columns_stadium = []
columns_location = []
columns_home_team = []
columns_away_team = []
columns_home_team_goal = []
columns_away_team_goal = []
columns_attendance = []
columns_matchid = []

y_ff =[
    '1930',
    '1934',
    '1938',
    '1950',
    '1954',
    '1958',
    '1962',
    '1966',
    '1970',
    '1974',
    '1978',
    '1982',
    '1986',
    '1990',
    '1994',
    '1998',
    '2002',
    '2006',
    '2010',
    '2014',
    '2018'
]
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
url_wiki = 'https://en.wikipedia.org/wiki/'
urls = [f'{url_wiki}{y}_FIFA_World_Cup' for y in y_ff]
for url_main in urls:
    # url_main = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'
    # year base on url link
    match_year = re.search('\d+', url_main).group(0)
    url_temp = url_main

    # request content
    r_main = requests.get(url_main)

    # replace all img tags to corresponding labels
    soup_main = bs4.BeautifulSoup(replace_tags_with_labels(r_main,replacements=
                REPLACEMENTS).replace('\n', '').replace('\r', ''),'html.parser')
    soup_main = bs4.BeautifulSoup(soup_main.encode('UTF-8'),'html.parser')

    # create group_list and knockout_list to get list of navigating url
    headline_group = soup_main.find_all(attrs='mw-headline', text=cdata_group_list)
    group_list = [group.text for group in headline_group]

    headline_knockout = soup_main.find_all(attrs='mw-headline',
                                       text=cdata_knockout_list)
    knockout_list = [rounds.text for rounds in headline_knockout]
    all_round_list = group_list + knockout_list
    # for only WC 2010 change, group stage
    if '2010' in url_main:
        all_round_list = knockout_list

    # get all matches information
    # get tags of all stages
    s = soup_main.findAll(attrs='mw-headline', text=all_round_list)

    # correct above tags and append to a list
    s_list = [i for i in s if i.parent.name == 'h3']

    # get tags of all matches
    all_matches_info = soup_main.findAll(attrs='footballbox')

    # allocate matches to corresponding stages
    tags_ = {'group': [], 'fleft': [], 'fevent':[], 'fright': []}
    for match_ in all_matches_info:
        for stage in s_list:
            search_belong = match_.findPrevious('h3')
            if stage in search_belong:
                tags_['group'] += [stage.text]
                tags_['fleft'] += [match_.contents[0]]
                tags_['fevent'] += [match_.contents[1]]
                tags_['fright'] += [match_.contents[2]]

    for i, group in enumerate(tags_['group']):
        match_stage = group
        event_string = tags_['fevent'][i]
        soup_fevent = bs4.BeautifulSoup(str(event_string), 'html.parser')
        home_team_name = soup_fevent.find(attrs='fhome').text
        away_team_name = soup_fevent.find(attrs='faway').text
        tag_fscore_a = soup_fevent.find(attrs='fscore').find('a')
        if tag_fscore_a != None:
            a_href = tag_fscore_a['href']
            # handle 2018, 2014, 2010, 2006, 1970, 1954 note, extra time note, overtime
            if '2018' not in a_href and '2014' not in a_href and '2010' not in a_href and '2006' not in a_href and '1970' not in a_href and '1954' not in a_href and 'Extra_time' not in a_href and 'Overtime' not in a_href:
                home_team_f_score = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
                away_team_f_score = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
                match_id = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
            else:
                home_team_f_score = \
                soup_fevent.find(attrs='fscore').text.split('–')[0]
                away_team_f_score = \
                soup_fevent.find(attrs='fscore').text.split('–')[1]
                match_id = re.search('[\d]+(?=\/$)|[\d]+$|[\d]+(?=\/i)|[\d]+(?=\/r)|[\d]+(?=/\#)',
                         soup_fevent.find('a',text='Report')['href']).group(0)
                #soup_fevent.find(attrs='fgoals').contents[1].find('a', text='Report')['href']
        else:
            home_team_f_score = soup_fevent.find(attrs='fscore').text.split('–')[0]
            away_team_f_score = soup_fevent.find(attrs='fscore').text.split('–')[1]
            match_id = re.search('[\d]+(?=\/$)|[\d]+$|[\d]+(?=\/i)|[\d]+(?=\/r)|[\d]+(?=/\#)',
                         soup_fevent.find('a',text='Report')['href']).group(0)
        datetime_string = tags_['fleft'][i]
        soup_fdate = bs4.BeautifulSoup(str(datetime_string), 'html.parser')
        # cut redundant of date
        cut_date = re.search('.+(?=\()', soup_fdate.find(attrs='fdate').text)
        if cut_date != None:
            match_date = cut_date.group(0)
        else:
            match_date = soup_fdate.find(attrs='fdate').text

        if tag_fscore_a != None:
            a_href = tag_fscore_a['href']
            # handle 2018, 2014, 2010, 2006, 1970, 1954 note, extra time note, overtime
            if '2018' not in a_href and '2014' not in a_href and '2010' not in a_href and '2006' not in a_href and '1970' not in a_href and '1954' not in a_href and 'Extra_time' not in a_href and 'Overtime' not in a_href:
                match_time = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
            else:
                match_time = re.search('^[\d]*:[\d]*', soup_fdate.find(
                    'div', attrs='ftime').text).group(0)
        else:
            match_time = re.search('^[\d]*:[\d]*', soup_fdate.find(
            'div', attrs='ftime').text).group(0)
        stadium_string = tags_['fright'][i]
        soup_stadium = bs4.BeautifulSoup(str(stadium_string), 'html.parser')
        match_stadium = soup_stadium.find('div', attrs={'itemprop':'location'}
                                          ).text.split(',')[0]
        match_location = soup_stadium.find('div', attrs={'itemprop':'location'}
                                          ).text.split(',')[1]
        if tag_fscore_a != None:
            a_href = tag_fscore_a['href']
            # handle 2018, 2014, 2010, 2006, 1970, 1954 note, extra time note, overtime
            if '2018' not in a_href and '2014' not in a_href and '2010' not in a_href and '2006' not in a_href and '1970' not in a_href and '1954' not in a_href and 'Extra_time' not in a_href and 'Overtime' not in a_href:
                match_attendance = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
            else:
                match_attendance = re.search('[\d,]+',re.search('Attendance[^<>]+',
                              str(soup_stadium.find('div'))).group(0)).group(0)
        else:
            match_attendance = re.search('[\d,]+', re.search('Attendance[^<>]+', str(soup_stadium.find('div'))).group(0)).group(0)
        #re.search('Attendance[^<>]+', str(soup_stadium.find('div'))).group(0)


        # append collecting data to corresponding columns
        columns_year.append(match_year)
        columns_stage.append(match_stage)
        columns_date.append(match_date)
        columns_time.append(match_time)
        columns_stadium.append(match_stadium)
        columns_location.append(match_location)
        columns_home_team.append(home_team_name.replace('\xa0', ''))
        columns_home_team_goal.append(home_team_f_score)
        columns_away_team_goal.append(away_team_f_score)
        columns_away_team.append(away_team_name.replace('\xa0', ''))
        columns_attendance.append(match_attendance)
        columns_matchid.append(match_id)

    # for only WC 2010 change, group stage
    if '2010' in url_main:
        all_round_list = group_list
        for rounds in all_round_list:
            # make a backtup url
            url_temp1 = url_main
            rounds_temp1 = rounds.replace(' ', '_')
            url_main = f'{url_main}_{rounds_temp1}'
            # request each group detail content
            # ex: https://en.wikipedia.org/wiki/2010_FIFA_World_Cup_Group_A
            r_main = requests.get(url_main)

            # get match_year from url
            match_year = re.search('[\d]+', url_main).group(0)

            # soup r_main and reformat/encode(UTF-8) ++
            soup_main = bs4.BeautifulSoup(replace_tags_with_labels(r_main,
                 replacements=REPLACEMENTS).replace('\n', ''), 'html.parser')
            soup_main = bs4.BeautifulSoup(soup_main.encode('UTF-8'),
                                          'html.parser')
            # get tags of all matches
            all_matches_info = soup_main.findAll(attrs='footballbox')
            for match_info in all_matches_info:

                match_stage = rounds
                cut_date = re.search('.+(?=\()',
                                     match_info.find(attrs='fdate').text)
                # cut redundant of date
                if cut_date != None:
                    match_date = cut_date.group(0)
                else:
                    match_date = match_info.find(attrs='fdate').text
                match_time = re.search('^[\d]*:[\d]*',
                                       match_info.find(attrs='ftime').text).group(0)
                match_stadium = match_info.find('div', attrs={'itemprop': 'location'}
                                  ).text.split(',')[0]
                match_location = \
                match_info.find('div', attrs={'itemprop': 'location'}
                                  ).text.split(',')[1]
                match_attendance = re.search('[\d,]+', match_info.find('div',
                            text=re.compile('Attendance[^<>]+')).text).group(0)
                home_team_name = match_info.find(attrs='fhome').text
                away_team_name = match_info.find(attrs='faway').text
                home_team_f_score = \
                match_info.find(attrs='fscore').text.split('–')[0]
                away_team_f_score = \
                match_info.find(attrs='fscore').text.split('–')[1]
                match_id = re.search('[\d]+(?=\/$)|[\d]+$|[\d]+(?=\/i)|[\d]+(?=\/r)|[\d]+(?=/\#)',
                         soup_fevent.find('a',text='Report')['href']).group(0)


                # append collecting data to corresponding columns
                columns_year.append(match_year)
                columns_stage.append(match_stage)
                columns_date.append(match_date)
                columns_time.append(match_time)
                columns_stadium.append(match_stadium)
                columns_location.append(match_location)
                columns_home_team.append(home_team_name.replace('\xa0', ''))
                columns_home_team_goal.append(home_team_f_score)
                columns_away_team_goal.append(away_team_f_score)
                columns_away_team.append(away_team_name.replace('\xa0', ''))
                columns_attendance.append(match_attendance)
                columns_matchid.append(match_id)

                # reset url_main to reuse in loops
                url_main = url_temp1

df_all_matches = pd.DataFrame({'Year': columns_year, 'Stage': columns_stage,
                               'Date': columns_date, 'Time': columns_time,
                              'Stadium': columns_stadium,
                               'Location': columns_location,
                               'Home Team': columns_home_team,
                               'HT Goals': columns_home_team_goal,
                               'AT Goals': columns_away_team_goal,
                                'Away Team': columns_away_team,
                               'Match Attendance': columns_attendance,
                               'MatchID': columns_matchid
                               })

df_all_matches.to_excel('Fifa_world_cup.xlsx', sheet_name='All Matches')