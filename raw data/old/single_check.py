from bs4 import BeautifulSoup
import pandas as pd
with open('C:\Users\Nam Invincible\PycharmProjects\Group7-mini-project\raw data\old\html_string.txt', encoding='UTF-8') as f:
    match_info = f.read()

match_info = BeautifulSoup(match_info, 'html.parser')
fgoal_tag = match_info.find(attrs='fgoal')

print(fgoal_tag)