
# coding: utf-8

# In[9]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import urllib.request
from bs4 import BeautifulSoup
import re
import nltk
from collections import Counter
import datetime
from tqdm import tqdm

url = "https://opportunities.digitalnovascotia.com/resumes/"
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(100)


# In[15]:


#<a class='load_more_jobs'></a>
load_more_jobs_a = driver.find_elements_by_class_name("load_more_resumes")
load_more_jobs_a[0].click()


# In[16]:


# create a list of unique tech jobs.
# opportunities.digitalnovascotia.com uses windowed pagination so we will analyze
# the 20 most recent jobs only. 
links = []
soup = BeautifulSoup(driver.page_source, 'html.parser')
for a in soup.find_all('a',{'href':re.compile('https://opportunities.digitalnovascotia.com/resume/')}):
    links.append(a['href'])

# number of job postings 
print(f'number of resumes: {len(links)}')

holding = []
count = 1
for line in tqdm(links):
    pages = urllib.request.urlopen(line).read()
    souper = BeautifulSoup(pages, 'lxml')

    for script in souper(["script", "style"]):
        script.replace_with(" ")
        script.decompose()

    text = souper.get_text(" ")

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "  ".join(chunk for chunk in chunks if chunk)
    
    holding.append(text)
    
words = [s.lower().split() for s in holding if s]
words = [sublist for l in words for sublist in l]
words = [''.join(c for c in w if c.isalpha()) for w in words]

check = {
    '0':'java',
    '1':'javascript',
    '2':'react',
    '3':'ruby',
    '4':'rails',
    '5':'swift',
    '6':'node',
    '7':'php',
    '8':'python',
    '9':'angular',
    '10':'django',
    '11':'sql',
    '12':'perl',
    '13':'xml',
    '14':'c#',
    '15':'c++',
    '16':'html',
    '17':'css',
    '18':'.net',
    '19':'go',
    '20':'matlab'
}

frequency = {}
for c in check:
    count = 1
    for w in words:
        if check[c] in w:
            frequency[check[c]] = count
            count += 1
frequency_sum = sum([i[1] for i in frequency.items()])

for i in frequency.items():
    print(f'{i[0]}... {round(i[1]/frequency_sum*100, 2)}%')


# In[35]:


check = {
    '0':'java',
    '1':'javascript',
    '2':'react',
    '3':'ruby',
    '4':'rails',
    '5':'swift',
    '6':'node',
    '7':'php',
    '8':'python',
    '9':'angular',
    '10':'django',
    '11':'sql',
    '12':'perl',
    '13':'xml',
    '14':'c#',
    '15':'c++',
    '16':'html',
    '17':'css',
    '18':'.net',
    '20':'matlab'
}

frequency = {}
for c in check:
    count = 1
    for w in words:
        if check[c] in w:
            frequency[check[c]] = count
            count += 1
frequency_sum = sum([i[1] for i in frequency.items()])

for i in frequency.items():
    print(f'{i[0]}... {round(i[1]/frequency_sum*100, 2)}%')

