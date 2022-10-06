from ast import keyword
import re
import time
from typing import List
from CFReqeuster import cf_request
from lxml import etree
from KeywordTopicMapping import KeyTopicMap

from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

CF_PASS = 'M3YKHA69'
CF_USER = 'KNB.'
CF_PREFIX = 'https://codeforces.com/gym/'
TOPIC_THRESHOLD = 5

def get_span_keywords(span):
    span = str(span)
    for i in range(0,len(span)):
        if span[i] == '>':
            span = span[i+1::]
            break
    span = span[0:-7]
    return ''.join(span.strip().lower().split('_'))

def get_submission_topics(browser, gym, submission):
    try:
        browser.get(f'{CF_PREFIX}{gym}/submission/{submission}')
        submission_code = browser.find_element(value='program-source-text')
        keywords = BeautifulSoup(submission_code.get_attribute("outerHTML"), 'html.parser').find_all('span')
        keywords = [get_span_keywords(k) for k in keywords]
        topics = set()
        for word in keywords:
            if word in KeyTopicMap:
                topics.add(KeyTopicMap[word])
        return list(topics)
    except Exception as e:
        return []

def get_problem_topics(browser, gym: str, problem: str):
    browser.get(f'{CF_PREFIX}{gym}/status/{problem}') #go to first status page
    pages = browser.find_elements(by='class name', value='page-index')
    max_page = 1
    if pages:
        max_page = int(pages[-1].get_attribute('pageindex'))
    topics_dict = dict()
    for page in range(2,max_page+2):
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
            for topic in topics:
                topics_dict[topic] = topics_dict.get(topic, 0) + 1
        browser.get(f'{CF_PREFIX}{gym}/status/{problem}?pageIndex={page}&order=BY_PROGRAM_LENGTH_ASC')
        time.sleep(5)
    return [k for k,v in topics_dict.items() if v >= TOPIC_THRESHOLD]

def fetch_topics(gym):
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    browser.get('https://codeforces.com/enter?back=%2F')
    handle = browser.find_element(value='handleOrEmail')
    password = browser.find_element(value='password')
    handle.send_keys(CF_USER)
    password.send_keys(CF_PASS)
    browser.find_element(by='class name', value="submit").click() #login
    time.sleep(5)
    browser.get(f'{CF_PREFIX}{gym}')
    time.sleep(5)
    problems = BeautifulSoup(browser.find_element(by='class name',value='problems').get_attribute("innerHTML"), 'html.parser')
    a_list = problems.find_all('a', href=True)
    problem_list = []
    for entry in a_list:
        arr = entry['href'].split('/')
        if len(arr) == 5 and arr[1] == 'gym' and arr[3] == 'problem':
            problem_list.append(arr[-1])
    problem_list = list(set(problem_list))
    topics = []
    for problem in problem_list:
        topics += get_problem_topics(browser, gym=gym, problem=problem)
    topics = list(set(topics))
    return topics
    
if __name__ == '__main__':
    print(fetch_topics('103921'))   
