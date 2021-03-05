import yfinance as yf
import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup

import requests
import pandas as pd 
import numpy as np 
import sklearn as sk 
from sklearn.linear_model import LinearRegression
import time 
import json

#List of 7000 NASDAQ Stocks
stock_list = pd.read_csv(r"F:\investment_ds_project\all_us_stocks.csv")

stock_list.set_index = stock_list['Symbol']
stock_list = stock_list.drop(['Name', 'Last Sale','Net Change','% Change', 'Volume', 'IPO Year'], axis = 1)
stock_list.shape

#stock_list = stock_list.set_index(['Symbol'])
stock_list.dropna(axis = 0, inplace = True)
stock_list['% Change'].replace({'%': ''},inplace = True, regex = True)
x = stock_list[['Market Cap']]
y = stock_list[['% Change']]

x1 = stock_list['Market Cap']
y1 = stock_list['% Change']

y.dtypes

stock_actions = None
historical_data = None
dividend_list = [0]*len(stock_list.index)
split_list = [0]*len(stock_list.index)
one_year_change_list = [0]*len(stock_list.index)
one_year_date = [0] * len(stock_list.index)
one_year_price = [0] * len(stock_list.index)
for idx, symbol in enumerate(stock_list['Symbol']): 
    if(idx < len(stock_list.index)):
        ticker = yf.Ticker(symbol)
        print(ticker)
        try:
            stock_actions = ticker.actions
            dividend_avg = stock_actions['Dividends'].mean()
            splits_avg = stock_actions['Stock Splits'].mean()
            dividend_list[idx] = dividend_avg
            split_list[idx] = splits_avg
        except: 
            dividend_list[idx] = -1
            split_list[idx] = -1
            print(f"no available dividend and split data for {ticker}")
        historical_data = ticker.history(period = 'MAX', interval = '1mo')
        historical_data.dropna(axis = 0, how= 'all')
        open_price =  historical_data['Open']
        close_price = historical_data['Close']
        mlist = list(historical_data)
       
        if len(open_price) >= 17: 
            one_year_change = (close_price[len(close_price)-1]- open_price[len(open_price)-18])/open_price[len(close_price)-1]
            one_year_change_list[idx] = one_year_change
            date[idx] = historical_data.index[len(close_price)-18]
            one_year_price[idx] = open_price[len(open_price)-18]
        else:
            one_year_change = (close_price[len(close_price)-1]- open_price[0])/open_price[len(close_price)-1]
            one_year_change_list[idx] = one_year_change
            one_year_price[idx] = open_price[0]
    

stock_list['1 Year % Change'] = one_year_change_list
stock_list['Average Dividend'] = dividend_list
stock_list['Stock Splits'] = splits_avg
stock_list['1 Year Date'] = date
stock_list['1 Year Price'] = one_year_price

stock_list.to_csv('test_stock_list.csv')


#import mutual fund information from vanguard
browser = webdriver.Chrome(executable_path = r"C:\Users\Michael G\Desktop\chromedriver.exe")
vanguard_url = 'https://investor.vanguard.com/mutual-funds/list'
browser.get(vanguard_url)
time.sleep(20)
source = browser.page_source
soup = BeautifulSoup(source, 'html.parser')
dataTable = soup.find('div', class_= 'template break-A')
inside_table = dataTable.find('div', class_ = 'template-region content-region containsFloats')
inside_table1 = inside_table.find('div', class_ = 'template-region primary-region break-A')
#print(len(inside_table1.find_all('div')))
vanguardScrimProductsArea = inside_table1.find_all('div')[0]
#print(inside_table1.find_all('div')[0])

data_ng_viewer = vanguardScrimProductsArea.find_all('div')[0]

inside_table4 = data_ng_viewer.find('div', class_ = 'ng-scope _mutualFunds')

inside_table5 = inside_table4.find('div', class_= 'tableContainer')
inside_table6 = inside_table5.find('div', class_ = 'scrollingTables')
inside_table7 = inside_table6.find('div', class_ = 'scrollingTableLeftSide ng-scope')
inside_table8 = inside_table7.find('table', class_ = 'long-list dataTable scrollingTableLeft ng-isolate-scope')
#print(inside_table8)
rows = inside_table8.find_all('tbody', class_ = 'original ng-scope')[0]
#print(rows)

