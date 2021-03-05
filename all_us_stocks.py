import yfinance as yf
import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 
import sklearn as sk 
import requests

#List of 7000 NASDAQ Stocks
stock_list = pd.read_csv(r"F:\investment_ds_project\all_us_stocks.csv")

stock_list.set_index = stock_list['Symbol']
stock_list = stock_list.drop(['Name', 'Last Sale','Net Change','% Change', 'Volume', 'IPO Year'], axis = 1)
stock_list.shape

#import mutual fund information from vanguard 
vanguard_url = 'https://investor.vanguard.com/mutual-funds/list#/mutual-funds/asset-class/month-end-returns'
source = requests.get(vanguard_url)

soup = BeautifulSoup(source.content, 'lxml')
dataTable = soup.find('table', class_ = 'long-list dataTable scrollingTableLeft ng-isolate-scope')
print(dataTable)