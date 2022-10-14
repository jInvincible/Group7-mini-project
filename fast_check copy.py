import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

sales = pd.read_excel('Office Sales.xlsx', 'Sales')
customer = pd.read_excel('Office Sales.xlsx', 'Customer')
sales.info()

sales['OrderMonth'] = sales.OrderDate.dt.month
sales['OrderQuarter'] = sales.OrderDate.dt.quarter
sales['OrderYear'] = sales.OrderDate.dt.year.astype(str)

def month_convert(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months[int(month) - 1]

sales['OrderMonthString'] = sales['OrderMonth'].apply(month_convert)

sales['OrderMonth'].value_counts()

