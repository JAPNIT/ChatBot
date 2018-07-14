from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import requests, re
from gtts import gTTS
import os,sys
import urllib.request

def summary(search):
    
    new_search = ""
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

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'GoogleChrome')]

    for start in range(0,10):
        url = "http://www.google.com/search?q=" + new_search[:-1] + str(start*10)
        page = opener.open(url)
        soup = BeautifulSoup(page, "html.parser")
        links = []
        for cite in soup.findAll('cite'):
            links.append(cite.text)
            
    x = 0
    summary = ""
    while len(summary) < 50:
        try:
            if links[x][:4] != "http":
                links[x] = "https://" + links[x]
            print(links[x])
            text = textfromurl(links[x])
            link = links[x]
        except:
            break

        text = text[len(text)//2 :]
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
        try:
            average = int(sumValues/ len(sentenceValue))
        except:
            average = 100000

        count = 0
        summary = ''
        for sentence in sentences:
                if count == 3:
                    break
                if sentence in sentenceValue and sentenceValue[sentence] > (1.5*average):
                    summary +=  " " + sentence
                    count += 1
        x += 1

    language = 'en'
    try:
        myobj = gTTS(text=summary, lang=language, slow=False)
    except:
        return "Sorry lah, couldn't find"

    myobj.save("summary.mp3")
     
    os.system("afplay summary.mp3")
    return summary

    

