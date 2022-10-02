from ast import keyword
import re
import time
from typing import List
from CFReqeuster import cf_request
from lxml import etree

from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

CF_PASS = 'M3YKHA69'
CF_USER = 'KNB.'
CF_PREFIX = 'https://codeforces.com/gym/'

def get_span_keywords(span):
    span = str(span)
    for i in range(0,len(span)):
        if span[i] == '>':
            span = span[i+1::]
            break
    span = span[0:-7]
    return span.strip()

def get_submission_topics(browser, gym, submission):
    browser.get(f'{CF_PREFIX}{gym}/submission/{submission}')
    submission_code = browser.find_element(value='program-source-text')
    keywords = BeautifulSoup(submission_code.get_attribute("outerHTML"), 'html.parser').find_all('span')
    keywords = [get_span_keywords(k) for k in keywords]
    return []

def get_problem_submissions(browser, gym: str, problem: str):
    browser.get(f'{CF_PREFIX}{gym}/status/{problem}') #go to first status page
    submissions_table = browser.find_element(by='class name', value='status-frame-datatable')
    soup = BeautifulSoup(submissions_table.get_attribute("innerHTML"), 'html.parser')
    submissions = soup.find_all('a', href=True)
    submission_codes = []
    for submission in submissions:
        arr = submission['href'].split('/')
        if len(arr) == 5 and arr[1] == 'gym' and arr[3] == 'submission':
            submission_codes.append(arr[-1])
    
    for submission in submission_codes:
        topics = get_submission_topics(browser, gym, submission)
    
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
    
    