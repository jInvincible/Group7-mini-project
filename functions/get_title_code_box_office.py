import pandas as pd
import bs4
import requests
import time
from random import randint

url = 'https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?offset='
code_list = []
i = 0 # so lan dem

while i < 5:
    # content of URL
    r = requests.get(f'{url}{i*200}')

    # Parse HTML Code
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    # Find all links as a-link-normal
    links = soup.find_all(class_='a-link-normal', href=True)

    for link in links:
        if str(link).find('/title/') != -1:
            code = str(link).split('/')[2]
            code_list.append(code)
    i = i+ 1
    rand = randint(5, 10)
    print(f'wait for {rand}')
    time.sleep(rand)


df = pd.DataFrame(code_list)
# df.to_csv('title_code.csv')