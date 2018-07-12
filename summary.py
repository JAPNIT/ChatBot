from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
import requests
import importlib
#https://www.straitstimes.com/politics/stepping-up-the-war-on-diabetes
def textfromurl(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text

text = textfromurl(input("Enter Url"))
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
