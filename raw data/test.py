import pandas as pd
import re
uni = pd.DataFrame({'World Rank': [1, 2, 3, 4, 5, '200-250', '200-250'],    'anycolumn': [1, 2, 3, 4, 5, 6, 7]})


dict = {'VN': {'win': 10,
               'draw': 0,
               'lose': 1
                }, 
        'USA': {'win': 0, 
                'draw': 9, 
                'lose': 2
                }
        }
print(dict['VN']['win'])
