ur = r"https://www.etf.com/channels/sectors"

import pandas as pd

# from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup
from collections import namedtuple
import re

def get_etf_holdings(etf_symbol):
    '''
    etf_symbol: str
    
    return: pd.DataFrame
    '''
    url = 'https://www.barchart.com/stocks/quotes/{}/constituents?page=all'.format(
        etf_symbol)

    # Loads the ETF constituents page and reads the holdings table
    browser = WebDriver(r"C:\Users\emax4\Desktop\chromedriver.exe") # webdriver.PhantomJS()
    #browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    #table = get_table(soup)
    table = soup.select('table')
    return soup, table

def clean_data(txt):
    txt = str(txt)
    txt = re.sub('\s{2}', '_', txt)
    txt = re.split('_+', txt)
    li = [i.lstrip() for i in txt]
    '    Symbol     Name     % Holding     Shares'
    return li[1:5]


def get_holdings(etf_ticker):
    
    url = 'https://www.barchart.com/stocks/quotes/{}/constituents?page=all'.format(
        etf_ticker)

    # Loads the ETF constituents page and reads the holdings table
    browser = WebDriver(r"C:\Users\emax4\Desktop\chromedriver.exe") 
    #browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    #table = get_table(soup)
    table = soup.select('table')
    browser.quit()
    
    # Data is in first table
    #tables =  get_etf_holdings(etf_ticker)

    # Find all tr in table 0
    data_table = table[0].findAll('tr')

    # loop through the list exlcuding first and last
    holdings = []
    Row = namedtuple(etf_ticker, ['Symbol', 'Name', 'Holding_percent', 'Shares'])
    for index in range(len(data_table)):
        if index not in [0, len(data_table)-1]:
            hold = clean_data(data_table[index].get_text())
            holdings.append(Row(*hold))

    return pd.DataFrame(holdings)#pd.DataFrame.from_records(holdings)#pd.DataFrame(holdings)



# Loads the ETF constituents page and reads the holdings table
browser = WebDriver(r"C:\Users\emax4\Desktop\chromedriver.exe") # webdriver.PhantomJS()
#browser = webdriver.Chrome()
browser.get(ur)
html = browser.page_source
soup = BeautifulSoup(html, "html.parser")
#table = get_table(soup)
table = soup.select('table')

browser.quit()

