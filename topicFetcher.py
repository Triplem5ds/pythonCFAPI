import time
from typing import List
from CFReqeuster import cf_request
import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

CF_PASS = 'M3YKHA69'
CF_USER = 'KNB.'
CF_PREFIX = 'https://codeforces.com/gym/'

def get_problem_submissions(browser, gym: str, problem: str):
    browser.get(f'{CF_PREFIX}{gym}/status/{problem}') #go to first status page
    submissions_table = browser.find_element(by='class name', value='status-frame-datatable').get_attribute('innerHTML')
    soup = BeautifulSoup(submissions_table, 'lxml')
    table = soup.find_all('table')[0]
    new_table = pd.DataFrame(columns=range(0,8), index=0)
    row_maker = 0
    for row in table.find_all('tr'):
        column_maker = 0
        columns = row.find_all('th')
        for column in columns:
            new_table.iat[row_maker, column_maker] = column.get_text()
            column_maker += 1
        row_maker += 1
    print(new_table)
 
if __name__ == '__main__':
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    browser.get('https://codeforces.com/enter?back=%2F')
    handle = browser.find_element(value='handleOrEmail')
    password = browser.find_element(value='password')
    handle.send_keys(CF_USER)
    password.send_keys(CF_PASS)
    browser.find_element(by='class name', value="submit").click() #login
    time.sleep(5)
    get_problem_submissions(browser, gym='103938', problem='C')
    time.sleep(5)
    
    