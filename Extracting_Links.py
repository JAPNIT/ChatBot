
import urllib.request
import sys
from bs4 import BeautifulSoup

if __name__ == "__main__":

    ### Create opener with Google-friendly user agent
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'GoogleChrome')]

    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages.
    for start in range(0,10):
        url = "http://www.google.com/search?q=hello" + str(start*10)
        page = opener.open(url)
        soup = BeautifulSoup(page, "html.parser")

        ### Parse and find
        ### Looks like google contains URLs in <cite> tags.
        ### So for each cite tag on each page (10), print its contents (url)
        for cite in soup.findAll('cite'):
            print (cite.text)
