# %%
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from cProfile import label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns



games_sales = pd.read_csv('Video_Games_Sales_as_at_22_Dec_2016.csv', encoding='latin')
#khái quát dữ liệu
games_sales.info()
#Nói về sự giống nhau của thể loại game
games_sales.loc[games_sales.Name == 'Grand Theft Auto V']
#tìm null
games_sales.isnull().sum()

#tổng quan về lượng 'Game' phát hành ra hàng năm và vẽ chart

count_games_sales=games_sales['Year_of_Release'].value_counts().sort_index().reset_index()
plt.bar(count_games_sales['index'],count_games_sales['Year_of_Release'])


#tìm lượng sale bán ra năm 2014 15 16 17 20 và ghép nó liền lại theo năm

sales_2014=games_sales[games_sales['Year_of_Release'] == 2014]
sales_2015=games_sales[games_sales['Year_of_Release'] == 2015]
sales_2016=games_sales[games_sales['Year_of_Release'] == 2016]
sales_2017=games_sales[games_sales['Year_of_Release'] == 2017]
sales_2020=games_sales[games_sales['Year_of_Release'] == 2020]

recent_sales = pd.concat([sales_2014, sales_2015, sales_2016,  sales_2017, sales_2020])


# tính tổng lượng sale bán ra theo khu vực và thể loại , lấy top 3
###sum_NA = recent_sales.groupby("Genre")[['NA_Sales']].sum().sort_values(['NA_Sales']).reset_index()
###top3_Genre_sale_NA=sum_NA[-3:]

def find_sum(a,b,c):
    x=a.groupby(b)[[c]].sum().sort_values([c]).reset_index()
    return x

def find_top3(d,e,f):
    x1=d.nlargest(f,e)
    return x1

sum_NA=find_sum(recent_sales,'Genre','NA_Sales')
top3_Genre_sale_NA=find_top3(sum_NA,'NA_Sales',3)
sum_NA_total=sum_NA.sum()

sum_EU =find_sum(recent_sales,'Genre','EU_Sales')
top3_Genre_sale_EU=find_top3(sum_EU,'EU_Sales',3)

sum_JP =find_sum(recent_sales,'Genre','JP_Sales')
top3_Genre_sale_JP=find_top3(sum_JP,'JP_Sales',3)

sum_Other =find_sum(recent_sales,'Genre','Other_Sales')
top3_Genre_sale_Other=find_top3(sum_Other,'Other_Sales',3) 

sum_GB =find_sum(recent_sales,'Genre','Global_Sales')
top3_Genre_sale_GB=find_top3(sum_GB,'Global_Sales',3)

#vẽ biểu đồ cột thể hiện thể loại game nào đang được ưa chuộng theo khu vực
#1
sum_2014=find_sum(sales_2014, 'Genre', 'Global_Sales')
sum_2015=find_sum(sales_2015, 'Genre', 'Global_Sales')
sum_2016=find_sum(sales_2016, 'Genre', 'Global_Sales')
sum_2017=find_sum(sales_2017, 'Genre', 'Global_Sales')

Gerne=['Action','Shooter','Sports','Role-Playing','Fighting']

#2
sum_NA_2014=find_sum(sales_2014,'Genre','NA_Sales')
top3_Genre_sale_NA_2014=find_top3(sum_NA_2014,'NA_Sales',3)

sum_EU_2014=find_sum(sales_2014,'Genre','EU_Sales')
top3_Genre_sale_EU_2014=find_top3(sum_EU_2014,'EU_Sales',3)

sum_JP_2014=find_sum(sales_2014,'Genre','JP_Sales')
top3_Genre_sale_JP_2014=find_top3(sum_JP_2014,'JP_Sales',3)

sum_Other_2014=find_sum(sales_2014,'Genre','Other_Sales')
top3_Genre_sale_Other_2014=find_top3(sum_Other_2014,'Other_Sales',3)
#
sum_GB_2014=find_sum(sales_2014,'Genre','Global_Sales')
top3_Genre_sale_GB_2014=find_top3(sum_GB_2014,'Global_Sales',3)

sum_GB_2015=find_sum(sales_2015,'Genre','Global_Sales')
top3_Genre_sale_GB_2015=find_top3(sum_GB_2015,'Global_Sales',3)

# %%
#2
#Genre_2014=sales_2014[sales_2014['Genre'] == 'Action']

Genre=['Action','Shooter','Sports','Role-Playing','Fighting']

pv_sales_by_genre = games_sales.pivot_table(index='Year_of_Release', columns='Genre', values='Global_Sales', aggfunc='sum', fill_value=0)

for title in Genre:
    plt.plot(pv_sales_by_genre.index,pv_sales_by_genre[title], label=title)

plt.legend()
plt.show()

# %%
plt.figure(figsize=(10,8))
area = [top3_Genre_sale_NA, top3_Genre_sale_EU, top3_Genre_sale_JP, top3_Genre_sale_Other]
for i, place in enumerate(area):
  plt.subplot(2,2,i+1)
  plt.bar(place['Genre'],place[place.columns[-1]])
  plt.title(place.columns[-1])


# %%

# %%
