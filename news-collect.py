import pandas as pd
import numpy as np
import sys
import re
import requests
import csv
import string
import os
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import json
import time
import datetime
import urllib.request

top_url = 'https://www.bleepingcomputer.com/'
driver = webdriver.Chrome(executable_path='../VSCode/Chromedriver/chromedriver.exe')
driver.get(top_url)
time.sleep(3)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=driver_path)


res = requests.get(top_url)
soup = BeautifulSoup(res.text, 'html.parser')

news_list_date = []
news_list_title = []
news_list_link = []
news_list_article = []

titles = soup.find_all('div', class_='bc_latest_news_text')
webhook_url = 'https://hooks.slack.com/services/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'

now = datetime.datetime.now()
print(now)

for title in titles:
    published = title.find(class_='bc_news_date').string
    date = datetime.datetime.strptime(published, '%B %d, %Y')
    if (now.day - date.day) > 1:
        continue
    
    header = title.find('h4')
    article_url = header.a['href']
    news_list_title.append(header.text)
    news_list_link.append(article_url)
    
    article_driver = webdriver.Chrome(executable_path='../VSCode/Chromedriver/chromedriver.exe')
    article_driver.get(article_url)
    time.sleep(3)
    
    res_article = requests.get(article_url)
    soup_article = BeautifulSoup(res_article.text, 'html.parser')
    articles = soup_article.find_all('div', class_='articleBody')
    
    for article in articles:
        news_list_article.append(article.get_text().replace('\n', ''))
    article_driver.quit()
    
    data = {
    "text": "Security News:Bleepingcomputer",
    "attachments": [
        {   
            "color": "good",
            "fields": [
            {
                "title": header.text,
                "value": article_url,
                "short": "true"
            }],
        "image_url": '',
          }]
    }

    req = urllib.request.Request(webhook_url)
    req.add_header('Content-type', 'application/json')

    with urllib.request.urlopen(req, json.dumps(data).encode('utf-8')) as f:
        print(f.read().decode('utf-8'))
                
driver.quit()