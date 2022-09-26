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
    # ('style', {}, 'b', {}, '')
]

## define corresponding pattern for each column of the sample dataframe to check
# role_pattern = re.compile('\\b[A-Z]{2}\\b|Manager.')
# snumber_pattern = re.compile('\\b[\d]{1,2}\\b')
# name_pattern = re.compile('[\sa-zA-Z\-]{3,}[\sa-zA-Z\-]{3,}(\(c\))?')
# card_pattern = re.compile(
#     '\\b(Y\\xa0[\d]{1,2})|\\bR(\\xa0[\d]{1,2})|\\b(RSY)\\xa0[\d]{1,2}')
# in_out_pattern = re.compile('\\b[O|I](\\xa0)[\d]{1,2}')
pattern_list = ['\\b[A-Z]{2}\\b|Manager.',
                '\\b[\d]{1,2}\\b',
                '[\sa-zA-Z\-]{3,}[\sa-zA-Z\-]{3,}(\(c\))?',
                '\\b(Y\\xa0[\d]{1,2})|\\bR(\\xa0[\d]{1,2})|\\b(RSY)\\xa0[\d]{1,2}',
                '\\b[O|I](\\xa0)[\d]{1,2}'
                ]

df_total_starting = pd.DataFrame(None, columns=['MatchID',
                                                'HT Role', 'HT Shirt Number',
                                                'HT Fullname',
                                                'HT Discipline', 'HT In_Out',
                                                'AT Role', 'AT Shirt Number',
                                                'AT Fullname',
                                                'AT Discipline', 'AT In_Out'])

df_group_starting = pd.DataFrame(None, columns=['MatchID',
                                                      'HT Role',
                                                      'HT Shirt Number',
                                                      'HT Fullname',
                                                      'HT Discipline',
                                                      'HT In_Out',
                                                      'AT Role',
                                                      'AT Shirt Number',
                                                      'AT Fullname',
                                                      'AT Discipline',
                                                      'AT In_Out'])

df_total_matches = pd.DataFrame(None, columns=['Year', 'Stage', 'Date', 'Time',
                                             'Stadium',	'Location',	'Home Team',
                                             'HT Goals', 'AT Goals', 'Away Team',
                                             'Match Attendance', 'MatchID'
                                             ])

df_group_matches = pd.DataFrame(None, columns=['Year', 'Stage', 'Date', 'Time',
                                             'Stadium',	'Location',	'Home Team',
                                             'HT Goals', 'AT Goals', 'Away Team',
                                             'Match Attendance', 'MatchID'
                                             ])

y_ff = [
    '1930'
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

# custom functions
def replace_tags_with_labels(html, replacements=REPLACEMENTS):
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    for tag, search_attr, new_tag, new_attr, new_string in \
            replacements:
        for node in soup.find_all(tag, search_attr):
            replacement = soup.new_tag(new_tag, **new_attr)
            replacement.string = new_string
            node.replace_with(replacement)
    return str(soup)


def allocate_corresponding_data_columns(adata, pattern_list=pattern_list):
    # create a_dic to receive value
    a_dic = {0: [], 1: [], 2: [], 3: [], 4: []}

    for i, pattern in enumerate(pattern_list):
        for text in adata:
            try:
                if re.search(pattern, text[i]):
                    a_dic[i] += [text[i]]
                else:
                    a_dic[i] += ['None']
            except IndexError:
                # if check latest row after Manager role, keep Manager name
                if text == adata[-2] and i == 2:
                    a_dic[i] += [adata[-1][0]]
                else:
                    a_dic[i] += ['None']
    return a_dic


# end custom functions

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
    soup_main = bs4.BeautifulSoup(replace_tags_with_labels(r_main, replacements=
    REPLACEMENTS).replace('\n', '').replace('\r', ''), 'html.parser')
    soup_main = bs4.BeautifulSoup(soup_main.encode('UTF-8'), 'html.parser')

    # create group_list and knockout_list to get list of navigating url
    headline_group = soup_main.find_all(attrs='mw-headline',
                                        text=cdata_group_list)
    group_list = list(set([group.text for group in headline_group]))
    group_list.sort()


    # # for testing-only
    # group_list = ['Group 1']
    # df_total_starting = pd.DataFrame(None, columns=['MatchID',
    #                             'HT Role', 'HT Shirt Number', 'HT Fullname',
    #                             'HT Discipline', 'HT In_Out',
    #                             'AT Role', 'AT Shirt Number', 'AT Fullname',
    #                             'AT Discipline', 'AT In_Out'])
    # 1950 World cup Final stage = final round
    if '1950' in url_main:
        all_round_list = group_list + ['final round']
    elif '1934' in url_main or '1938' in url_main:
        all_round_list = group_list + ['final_tournament']
    else:
        all_round_list = group_list + ['knockout stage']


    for rounds in all_round_list:
        # make a backtup url
        url_temp1 = url_main
        rounds_temp1 = rounds.replace(' ', '_')
        url_main = f'{url_main}_{rounds_temp1}'
        # request each group detail content
        # ex: https://en.wikipedia.org/wiki/2010_FIFA_World_Cup_Group_A
        r_main = requests.get(url_main)

        # soup r_main and reformat/encode(UTF-8) ++
        soup_main = bs4.BeautifulSoup(replace_tags_with_labels(r_main,
                                                               replacements=REPLACEMENTS).replace(
            '\n', ''), 'html.parser')
        soup_main = bs4.BeautifulSoup(soup_main.encode('UTF-8'),
                                      'html.parser')
        # get tags of all matches
        all_matches_info = soup_main.findAll(attrs='footballbox')

        for match_info in all_matches_info:
            match_stage = rounds

            # get match_id, for missing matchid, receive 'missing'
            if match_info.find('a', text='Report') == None:
                match_id = 'missing'
            else:
                match_id = re.search(
                    '[\d]+(?=\/$)|[\d]+$|[\d]+(?=\/i)|[\d]+(?=\/r)|[\d]+(?=/\#)',
                    match_info.find('a', text='Report')['href']).group(0)

            # name : home team + away team
            home_team_name = match_info.find(attrs='fhome').text.replace('\xa0','')
            away_team_name = match_info.find(attrs='faway').text.replace('\xa0','')

            # check tag_fscore_a and receive HT F Score + AT F Score + time
            tag_fscore_a = match_info.find(attrs='fscore').find('a')
            slash_text = re.search('[\D]+', match_info.find(attrs='fscore').text).group(0)
            if tag_fscore_a != None:
                a_href = tag_fscore_a['href']
                # handle 2018, 2014, 2010, 2006, 1970, 1954 note, extra time note, overtime
                if '2018' not in a_href and '2014' not in a_href and '2010' not in a_href and '2006' not in a_href and '1970' not in a_href and '1954' not in a_href and 'Extra_time' not in a_href and 'Overtime' not in a_href:
                    match_id = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
                    home_team_f_score = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
                    away_team_f_score = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
                    match_time = f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
                else:
                    home_team_f_score = \
                        match_info.find(attrs='fscore').text.split(slash_text)[0]
                    away_team_f_score = \
                        match_info.find(attrs='fscore').text.split(slash_text)[1]
                    match_time = re.search('[\d]{1,2}:[\d]{1,2}', match_info.find(
                        'div', attrs='ftime').text).group(0)

            else:
                home_team_f_score = \
                match_info.find(attrs='fscore').text.split(slash_text)[0]
                away_team_f_score = \
                match_info.find(attrs='fscore').text.split(slash_text)[1]
                match_time = re.search('[\d]{1,2}:[\d]{1,2}', match_info.find(
                    'div', attrs='ftime').text).group(0)
                check_time = match_info.find('div', attrs='ftime').text

            # date
            # cut redundant of date
            cut_date = re.search('.+(?=\()', match_info.find(attrs='fdate').text)
            if cut_date != None:
                match_date = cut_date.group(0)
            else:
                match_date = match_info.find(attrs='fdate').text



            # stadium
            soup_stadium = match_info.find(attrs='fright')
            match_stadium = \
            soup_stadium.find('div', attrs={'itemprop': 'location'}
                              ).text.split(',')[0]

            # location
            match_location = \
            soup_stadium.find('div', attrs={'itemprop': 'location'}
                              ).text.split(',')[1]

            # attendance
            if match_id == 'w/o detail in /wiki/Walkover':
                match_attendance == f"{tag_fscore_a.text} detail in {tag_fscore_a['href']}"
            else:
                match_attendance = re.search('[\d,]+', re.search('Attendance[^<>]+',
                                                             str(soup_stadium.findAll(
                                                                 'div'))).group(
                0)).group(0)

            # get h_goal event
            # fhgoal = match_info.find(attrs='fhgoal')
            # if fhgoal != '':
            #     g_hcheck = [i.attrs['title'].strip() if i.name == 'a' else i.text.strip() for i in fhgoal.select('a[title],span')]
            #     for item in g_hcheck:
            #         if item == "\'":
            #             list.remove(g_hcheck, item)
            #         if len(item) == 3:
            #             list.remove(g_hcheck, item)
            #
            # if fhgoal != '':
            #     g_hcheck = fhgoal.text.replace(',', 'mergeupG ').split('\'')
            #     for i, item in enumerate(g_hcheck):
            #         if 'mergeupG' in item:
            #             g_hcheck[i-1] += f",{item.replace('mergeup', ' ')}"
            #             list.pop(g_hcheck, i)
            #         if item == '':
            #             list.pop(g_hcheck, i)
            #         if item == re.compile('\[[\d]+\]'):
            #             list.pop(g_hcheck, i)
            #
            #     star_hname = []
            #     star_hevent = []
            #     for i in g_hcheck:
            #         s_hname = i.split('G', maxsplit=1)[0]
            #         s_hevent = i.replace(s_hname, '')
            #         star_hname.append(s_hname)
            #         star_hevent.append(s_hevent)
            # else:
            #     star_hname = []
            #     star_hevent = []
            #
            # # get a_goal event
            # fagoal = match_info.find(attrs='fagoal')

            # if fagoal != '':
            # g_acheck = fagoal.text.replace(',', 'mergeupG ').split('\'')
            # for i, item in enumerate(g_acheck):
            #     if 'mergeupG' in item:
            #         g_acheck[i - 1] += f",{item.replace('mergeup', ' ')}"
            #         list.pop(g_acheck, i)
            #     if item == '':
            #         list.pop(g_acheck, i)
            #     if item == re.compile('\[[\d]+\]'):
            #         list.pop(g_acheck, i)
            #
            #     star_aname = []
            #     star_aevent = []
            #     for i in g_acheck:
            #         s_aname = i.split('G', maxsplit=1)[0]
            #         s_aevent = i.replace(s_aname, '')
            #         star_aname.append(s_aname)
            #         star_aevent.append(s_aevent)
            # else:
            #     star_aname = []
            #     star_aevent = []

            # get starting tag
            # tag_starting_table = match_info.findNextSiblings('table', limit=2)[1]
            # change tag_starting location in some match by matchid
            if match_id in ['1689', '2350', '2454', '2352', '2431', '2220',
                            '2196', '2252']:
                tag_starting_table = match_info.nextSibling.nextSibling.nextSibling
            elif match_id == 'w/o detail in /wiki/Walkover':
                # tiep theo
            else:
                tag_starting_table = match_info.nextSibling.nextSibling
            # for some match with no starting info
            if tag_starting_table.name not in ['h3', 'h2', 'link', 'style']:
                # get tag of home team starting
                # change tag_h and tag_a in some match by matchid
                if match_id in ['2350', '2352']:
                    tag_h = tag_starting_table.tr.tr.findChildren("td",
                                                                  recursive=False)[
                        0]
                else:
                    tag_h = \
                        tag_starting_table.tr.findChildren("td",
                                                           recursive=False)[0]

                # get tag of away team starting
                if match_id in ['2350', '2352']:
                    tag_a = tag_starting_table.tr.tr.findChildren("td",
                                                                  recursive=False)[
                        -1]
                else:
                    tag_a = \
                        tag_starting_table.tr.findChildren("td",
                                                           recursive=False)[
                            -1]
                row = []
                hdata1 = []
                for tr in tag_h.find_all('tr'):
                    td = [i.text for i in tr.find_all('td')]
                    row = [i for i in td]
                    hdata1.append(row)
                hdata = allocate_corresponding_data_columns(hdata1)
                df_hdata = pd.DataFrame(hdata)
                if len(df_hdata) >= 1:
                    df_hdata = df_hdata.drop(index=len(df_hdata) - 1)

                row = []
                adata1 = []
                for tr in tag_a.table.find_all('tr'):
                    td = [i.text for i in tr.find_all('td')]
                    row = [i for i in td]
                    adata1.append(row)
                adata = allocate_corresponding_data_columns(adata1)
                df_adata = pd.DataFrame(adata)
                if len(df_adata) >= 1:
                    df_adata = df_adata.drop(index=len(df_adata) - 1)

                df_starting = pd.concat(
                    [pd.Series(match_id), df_hdata, df_adata], axis=1)
                df_starting.columns = ['MatchID', 'HT Role', 'HT Shirt Number',
                                       'HT Fullname', 'HT Discipline',
                                       'HT In_Out',
                                       'AT Role',
                                       'AT Shirt Number', 'AT Fullname',
                                       'AT Discipline', 'AT In_Out'

                                       ]
                df_starting['MatchID'] = match_id

                # # append collecting data of the current match to corresponding columns of sheet Match Details
                # print(
                #     f'WorldCup {match_year} : {rounds} :: MatchID = {match_id}')
                # df_total_group_starting = pd.concat(
                #     [df_total_group_starting, df_starting])

            # if no starting information
            else:
                df_starting = pd.DataFrame(None, columns=[
                    'MatchID', 'HT Role', 'HT Shirt Number',
                     'HT Fullname', 'HT Discipline', 'HT In_Out',
                     'AT Role',
                     'AT Shirt Number', 'AT Fullname',
                     'AT Discipline', 'AT In_Out'])
                for column in list(df_starting.columns):
                    df_starting.at[0, column] = 'missing'
                df_starting['MatchID'] = match_id

            # make df_matches for all collected data
            df_matches = pd.DataFrame(
                {'Year': [match_year], 'Stage': [match_stage],
                 'Date': [match_date], 'Time': [match_time],
                 'Stadium': [match_stadium], 'Location': [match_location],
                 'Home Team': [home_team_name],
                 'HT Goals': [home_team_f_score],
                 'AT Goals': [away_team_f_score],
                 'Away Team': [away_team_name],
                 'Match Attendance': [match_attendance],
                 'MatchID': [match_id]
                 })
            print(f'WorldCup {match_year} : {rounds} :: MatchID = {match_id}')

            # append collecting data of the current match to corresponding columns of sheet Match Details
            df_group_starting = pd.concat(
                    [df_group_starting, df_starting])

                # append collecting data of current match to corresponding columns of sheet All Matches
            df_group_matches = pd.concat([df_group_matches, df_matches])
        url_main = url_temp1
    # # append to total
    # df_total_matches = pd.concat([df_total_matches, df_group_matches])
    # df_total_starting = pd.concat([df_total_starting, df_group_starting])

    # # clear df_total_group_starting for next round
    # df_group_starting = pd.DataFrame(None, columns=['MatchID',
    #                                                       'HT Role',
    #                                                       'HT Shirt Number',
    #                                                       'HT Fullname',
    #                                                       'HT Discipline',
    #                                                       'HT In_Out',
    #                                                       'AT Role',
    #                                                       'AT Shirt Number',
    #                                                       'AT Fullname',
    #                                                       'AT Discipline',
    #                                                       'AT In_Out'])
    #
    # # clear df_total_group_all_matches for next round
    # df_group_all_matches = pd.DataFrame(None,
    #                                           columns=['Year', 'Stage',
    #                                                    'Date', 'Time',
    #                                                    'Stadium',
    #                                                    'Location',
    #                                                    'Home Team',
    #                                                    'HT Goals',
    #                                                    'AT Goals',
    #                                                    'Away Team',
    #                                                    'Match Attendance',
    #                                                    'MatchID'
    #                                                    ])



df_group_matches.to_excel('Fifa_world_cup_allMatches.xlsx', sheet_name='All Matches')
df_group_starting.to_excel('Fifa_world_cup_matchDetails.xlsx', sheet_name='Match Details')
