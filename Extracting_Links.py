'''import urllib.request
import sys
from bs4 import BeautifulSoup

if __name__ == "__main__":

    ### Create opener with Google-friendly user agent
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Google Chrome')]

    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages.
    for start in range(1):
        url = "http://www.google.com/search?q=shrimp" + str(start)
        page=opener.open(url)
        soup = BeautifulSoup(page, "html.parser")

        ### Parse and find
        ### Looks like google contains URLs in <cite> tags.
        ### So for each cite tag on each page (10), print its contents (url)
        for cite in soup.findAll('cite'):
            print (cite.text)'''

import re
import os
import sys
import json
 
from scrapy.spider import Spider
from scrapy.selector import Selector
 
class GoogleSearch(Spider):
 
 #set the search result here
    name = 'Google search'
    allowed_domains = ['www.google.com']
    start_urls = ['Insert the google url here']
 
    def parse(self, response):
 
        sel = Selector(response)
        google_search_links_list = sel.xpath('//h3/a/@href').extract()
        google_search_links_list = [re.search('q=(.*)&sa',n).group(1) for n in google_search_links_list]
 
## Dump the output to json file
        with open(output_j_fname, "w") as outfile:
            json.dump({'output_url':google_search_links_list}, outfile, indent=4)

