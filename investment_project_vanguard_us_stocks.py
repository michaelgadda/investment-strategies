import yfinance as yf
import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
import sklearn as sk 
import time 
import json

#List of 7000 NASDAQ Stocks
stock_list = pd.read_csv(r"F:\investment_ds_project\all_us_stocks.csv")

stock_list.set_index = stock_list['Symbol']
stock_list = stock_list.drop(['Name', 'Last Sale','Net Change','% Change', 'Volume', 'IPO Year'], axis = 1)
stock_list.shape


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
print(inside_table8)
rows = inside_table8.find_all('tbody', class_ = 'original ng-scope')[0]
print(rows)