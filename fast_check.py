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
    # '2010',
    # '2014',
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
# url_wiki = 'https://en.wikipedia.org/wiki/'
# urls = [f'{url_wiki}{y}_FIFA_World_Cup' for y in y_ff]

url_main = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_Group_A'

match_year = re.search('\d+', url_main).group(0)

# request content
r_main = requests.get(url_main)

# replace all img tags to corresponding labels
soup_main = bs4.BeautifulSoup(replace_tags_with_labels(r_main,replacements=
            REPLACEMENTS).replace('\n', '').replace('\r', ''),'html.parser')
soup_main = bs4.BeautifulSoup(soup_main.encode('UTF-8'), 'html.parser')

match_info = soup_main.find(attrs='footballbox').find(attrs='fhgoal')

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
# df_hdata = pd.DataFrame(hdata)
# df_hdata = df_hdata.replace(to_replace='', value='None')
# # # get the manager name + index from HT Role, copy to HT Full Name,
# # # drop the latest row in df_hdata
# ht_m_index = int(df_hdata[df_hdata[0].str.contains(
#     'Manager.*')==True].index.values)
# ht_manager = df_hdata[0].iloc[-1]
# df_hdata.loc[ht_m_index, 2] = ht_manager
# df_hdata = df_hdata.drop(index=len(df_hdata)-1)


row = []
adata = []
for tr in tag_a.table.find_all('tr'):
    td = [i.text for i in tr.find_all('td')]
    row = [i for i in td]
    adata.append(row)
# df_adata = pd.DataFrame(adata)
# df_adata = df_adata.replace(to_replace='', value='None')
# # # get the manager name + index from AT Role, copy to AT Full Name,
# # # drop the latest row in df_adata
# at_m_index = int(df_adata[df_adata[0].str.contains(
#     'Manager.*') == True].index.values)
# at_manager = df_adata[0].iloc[-1]
# df_adata.loc[at_m_index, 2] = at_manager
# df_adata = df_adata.drop(index=len(df_adata) - 1)


role_pattern = re.compile('\\b[A-Z]{2}\\b|Manager.')
snumber_pattern = re.compile('\\b[\d]{1,2}\\b')
name_pattern = re.compile('[\sa-zA-Z\-]{3,}[\sa-zA-Z\-]{3,}(\(c\))?')
card_pattern = re.compile('\\b(Y\\xa0[\d]{1,2})|\\bR(\\xa0[\d]{1,2})|\\b(RSY)\\xa0[\d]{1,2}')
in_out_pattern = re.compile('\\b[O|I](\\xa0)[\d]{1,2}')

# define pattern for each column of the sample dataframe to check
pattern_list = ['\\b[A-Z]{2}\\b|Manager.',
                '\\b[\d]{1,2}\\b',
                '[\sa-zA-Z\-]{3,}[\sa-zA-Z\-]{3,}(\(c\))?',
                '\\b(Y\\xa0[\d]{1,2})|\\bR(\\xa0[\d]{1,2})|\\b(RSY)\\xa0[\d]{1,2}',
                '\\b[O|I](\\xa0)[\d]{1,2}'
                ]
# data_to_check = ['GK', '1', 'Aleksandr Samedov']

a_dic = {0:[], 1:[], 2:[], 3:[], 4:[]}

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

a_df = pd.DataFrame(a_dic)

# ############
#
# import pandas as pd
# df_sheet1 = pd.DataFrame({'CustomerKey': [1, 2, 3, 4, 5, 5, 6, 6],
#                           'Category': ['Cate_A', 'Cate_B', 'Cate_C', 'Cate_D', 'Cate_E', 'Cate_F',
#                                        'Cate_G', 'Cate_H']
#                           })
# df_sheet2 = pd.DataFrame({'CustomerKey': [1, 2, 3, 4, 5, 6],
#                           'Country/Region': ['USA', 'Vietnam', 'ApTech', 'France', 'Germany', 'Italy']
#                           })
# print(df_sheet1)
# print(df_sheet2)
#
# df_mix = pd.merge(df_sheet1, df_sheet2, how='left', left_on='CustomerKey', right_on='CustomerKey')
# print(df_mix)

import pandas as pd
sales = pd.read_excel('Office Sales.xlsx', sheet_name=0)
sales.head()
sales["Net Revenue"] = sales["UnitPrice"] * sales["OrderQuantity"] * (100-sales["Discount %"])/100
sales["OrderMonth"]=sales.OrderDate.dt.month
sales["OrderQuarter"]=sales.OrderDate.dt.quarter
sales["OrderYear"]=sales.OrderDate.dt.year
sales.head()

pvsales = sales.groupby(['OrderYear', 'OrderMonth']).agg({'Net Revenue': sum}).reset_index()


pvsale1 = sales.groupby(["OrderYear","OrderMonth"]).sum()["Net Revenue"].reset_index()

table = sales.pivot_table(values='Net Revenue',index='OrderMonth',columns='OrderYear', aggfunc='sum')

















