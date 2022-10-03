import bs4
import numpy as np
import pandas as pd


REPLACEMENTS = [
    ('img', {'alt': 'downward-facing red arrow'}, 'b', {}, 'O'),
    ('img', {'alt': 'upward-facing green arrow'}, 'b', {}, 'I'),
    ('img', {'alt': 'Yellow card'}, 'b', {}, 'Y'),
    ('img', {'alt': 'Yellow-red card'}, 'b', {}, 'RSY'),
    ('img', {'alt': 'Red card'}, 'b', {}, 'R'),
    ('img', {'title': 'Goal'}, 'b', {}, 'G'),
    # ('style', {}, 'b', {}, '')
]

def replace_tags_with_labels(html, replacements=REPLACEMENTS):
    if type(html) in ['bs4.element.Tag']:
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
    else:
        soup = bs4.BeautifulSoup(html, 'html.parser')

    for tag, search_attr, new_tag, new_attr, new_string in \
            replacements:
        for node in soup.find_all(tag, search_attr):
            replacement = soup.new_tag(new_tag, **new_attr)
            replacement.string = new_string
            node.replace_with(replacement)
    return str(soup)

with open('raw data/html_string.txt') as f:
    match_info = f.read()

match_info = bs4.BeautifulSoup(replace_tags_with_labels(match_info).replace('\n',''), 'html.parser')

fgoals = match_info.find(attrs={'class': ['fgoals']})
fhgoal = fgoals.find(attrs={'class':'fhgoal'})
fagoal = fgoals.find(attrs={'class':'fagoal'})
fhgoal_collect = [i.attrs['title'].strip() if i.name == 'a' else i.text.strip() for i in fhgoal.select('a[title],span')]
fagoal_collect = [i.attrs['title'].strip() if i.name == 'a' else i.text.strip() for i in fagoal.select('a[title],span')]
# def cleanup_fgoals(fgoals_collect):
#     for _ in range(4):
#         index_to_remove = []
#         for i, word in enumerate(fgoals_collect):
#             if word == 'Penalty kick (association football)' or word == 'Own goal':
#                 index_to_remove.append(i)
#             elif len(word) <= 3:
#                 index_to_remove.append(i)
#             elif word in fgoals_collect[i-1] and i != 0:
#                 index_to_remove.append(i)
#
#         index_to_remove.sort(reverse=True)
#         for i in index_to_remove:
#             fgoals_collect.pop(i)
#
#     hstar = [fgoals_collect[i] for i in range(0, len(fgoals_collect), 2)]
#     hevent = [fgoals_collect[i].replace('\xa0','') for i in range(1, len(fgoals_collect), 2)]
#     return hstar, hevent

def cleanup_fgoals(fgoals_collect):
    for _ in range(4):
        index_to_remove = []
        for i, word in enumerate(fgoals_collect):
            if word == 'Penalty kick (association football)' or word == 'Own goal':
                index_to_remove.append(i)
            elif len(word) <= 3:
                index_to_remove.append(i)
            elif word in fgoals_collect[i - 1] and i != 0:
                index_to_remove.append(i)

        index_to_remove.sort(reverse=True)
        for i in index_to_remove:
            fgoals_collect.pop(i)

    star = [fgoals_collect[i].split('(')[0] if len(fgoals_collect[i].split('(')) > 0 else fgoals_collect[i] for i in range(0, len(fgoals_collect), 2)]
    event = [fgoals_collect[i].replace('\xa0', '') for i in
              range(1, len(fgoals_collect), 2)]
    return star, event

hgoal_event = cleanup_fgoals(fhgoal_collect)
agoal_event = cleanup_fgoals(fagoal_collect)
df_agoal = pd.DataFrame(
                {'Starname_a': agoal_event[0], 'Goal_eventa': agoal_event[1]})

(df_starting,'Starname_h', 'Starname_a', 'HT Fullname', 'AT Fullname', 'Goal_eventh', 'Goal_eventa')

import re
list_check = ['Romário', "G 26'", "G 52'\xa0(pen.)"]
star_event_dict = {}
key = ''
for name in list_check:
    try:
        re.search('\\bG\s\d+', name).group(0)
        name.replace('\xa0', '')
        star_event_dict[key] += [name]

    except AttributeError:
        if len(name.split('(')) > 0:
            name = name.split('(')[0]
        star_event_dict[name] = []
        key = name



