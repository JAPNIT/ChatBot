import re
import os
import sys
import json
 
from scrapy.spiders import Spider
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
 
