from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import requests, re

"""

links = []
page = requests.get("https://www.google.dz/search?q=hello")
soup = BeautifulSoup(page.content)
links = soup.findAll("a")
for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
    print (re.split(":(?=http)",link["href"].replace("/url?q=","")))
"""
new_search = ""
search = input("Search: ")
search = word_tokenize(search)
for i in search:
    new_search += i + "+"
print(new_search[:-1])
#https://www.straitstimes.com/politics/stepping-up-the-war-on-diabetes
def textfromurl(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

import urllib.request
import sys
from bs4 import BeautifulSoup

### Create opener with Google-friendly user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'GoogleChrome')]

### Open page & generate soup
### the "start" variable will be used to iterate through 10 pages.
for start in range(0,10):
    url = "http://www.google.com/search?q=" + new_search[:-1] + str(start*10)
    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")
    links = []
    ### Parse and find
    ### Looks like google contains URLs in <cite> tags.
    ### So for each cite tag on each page (10), print its contents (url)
    for cite in soup.findAll('cite'):
        links.append(cite.text)
        
print(links)
x = 0
summary = ""
while len(summary) < 50:

    if links[x][:7] != "http://":
        links[x] = "http://" + links[x]

    text = textfromurl(links[x])

  
    print(links[0])
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        try:
            freqTable[word] += 1
        except:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()


    for sentence in sentences:
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freqTable[wordValue]
                else:
                    sentenceValue[sentence] = freqTable[wordValue]


    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    average = int(sumValues/ len(sentenceValue))

    summary = ''
    for sentence in sentences:
            if sentence in sentenceValue and sentenceValue[sentence] > (1.5*average):
                summary +=  " " + sentence
    print(summary)
    x += 1
print(summary)
