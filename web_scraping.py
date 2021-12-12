from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import urllib
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
# from app import *

#create a webdriver object and set options for headless browsing
# options = Options()
# options.headless = True
# driver = webdriver.Chrome('./chromedriver',options=options)

def get_js_soup(url,driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

def process_news(news):
    news = news.encode('ascii',errors='ignore').decode('utf-8') #removes non-ascii characters
    news = re.sub('\s+',' ',news) #repalces repeated whitespace characters with single space
    return news

def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup

def scrape_news_page(news_url,driver):
    soup = get_js_soup(news_url,driver)
    news_sec = soup.find('div',id='content_inner')
    news = process_news(news_sec.get_text(separator=' '))
    return news

def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)

# news = scrape_news_page(url,driver)
# driver.close()
#
# news_file = 'news.txt'
# write_lst(news,news_file)
#
# news = sent_tokenize(news)
# result_news = []
# for x in news:
#     result_news.append(word_tokenize(x))
#
# print(result_news)
