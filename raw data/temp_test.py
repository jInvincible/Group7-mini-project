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

y_ff =[
    # '1930',
    # '1934',
    # '1938',
    # '1950',
    # '1954',
    # '1958',
    # '1962',
    # '1966',
    # '1970',
    # '1974',
    # '1978',
    # '1982',
    # '1986',
    # '1990',
    # '1994',
    # '1998',
    # '2002',
    # '2006',
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

    # for testing-only
    # group_list = []
    df_total_starting = pd.DataFrame(None, columns=['MatchID', 'HT Role', 'HT Shirt Number', 'HTFull Name', 'HT Discipline', 'HT In/Out', 'AT Role', 'AT Shirt Number', 'AT Full Name', 'AT Discipline', 'AT In/Out'])

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
            # get match_id
            match_id = re.search('[\d]+(?=\/$)|[\d]+$|[\d]+(?=\/i)|[\d]+(?=\/r)|[\d]+(?=/\#)',
                match_info.find('a', text='Report')['href']).group(0)

            # get starting tag
            # tag_starting_table = match_info.findNextSiblings('table', limit=2)[1]
            tag_starting_table = match_info.nextSibling.nextSibling

            # get tag of home team starting
            tag_h = tag_starting_table.tr.findChildren("td", recursive=False)[0]

            # get tag of away team starting
            tag_a = tag_starting_table.tr.findChildren("td", recursive=False)[-1]
            row = []
            hdata = []
            for tr in tag_h.find_all('tr'):
                td = [i.text for i in tr.find_all('td')]
                row = [i for i in td]
                hdata.append(row)
            df_hdata = pd.DataFrame(hdata)
            df_hdata = df_hdata.replace(to_replace='', value='None')
            # # get the manager name + index from HT Role, copy to HT Full Name,
            # # drop the latest row in df_hdata
            ht_m_index = int(df_hdata[df_hdata[0].str.contains(
                'Manager.*')==True].index.values)
            ht_manager = df_hdata[0].iloc[-1]
            df_hdata.loc[ht_m_index, 2] = ht_manager
            df_hdata = df_hdata.drop(index=len(df_hdata)-1)


            row = []
            adata = []
            adata_dic = {'at role':'', 'at shirt number': '', 'at fullname':'', 'at discipline': '', 'at in_out': ''}
            for tr in tag_a.table.find_all('tr'):
                td = [i.text for i in tr.find_all('td')]
                row = [i for i in td]
                adata.append(row)
            df_adata = pd.DataFrame(adata)
            df_adata = df_adata.replace(to_replace='', value='None')
            # # get the manager name + index from AT Role, copy to AT Full Name,
            # # drop the latest row in df_adata
            at_m_index = int(df_adata[df_adata[0].str.contains(
                'Manager.*') == True].index.values)
            at_manager = df_adata[0].iloc[-1]
            df_adata.loc[at_m_index, 2] = at_manager
            df_adata = df_adata.drop(index=len(df_adata) - 1)


            df_starting = pd.concat([pd.Series(match_id), df_hdata, df_adata], axis=1)
            df_starting.columns = ['MatchID', 'HT Role', 'HT Shirt Number', 'HT FullName', 'HT Discipline', 'HT In/Out', 'AT Role', 'AT Shirt Number', 'AT Full Name', 'AT Discipline', 'AT In/Out']
            df_starting['MatchID'] = match_id

            # append collecting data to corresponding columns
            df_total_starting = pd.concat([df_total_starting, df_starting])

            # reset url_main to reuse in loops
        url_main = url_temp1