import scrapy
import pymongo
import string
from scrapy.spiders import CrawlSpider, Rule
from ..items import document
from scrapy.linkextractors import LinkExtractor
import datefinder
items = document()


class ExtractorSpider(scrapy.Spider):
    name = 'extractor'
    allowed_domains = ['indiankanoon.org']
    start_urls = ['https://indiankanoon.org/doc/1732220/']

    def __init__(self, start_line=0):
        # define init fuction to start scrolling from database
        pass
    
    # def start_requests(self):
    #     pass

    def parse(self, response):
        source = response.css('.docsource_main ::text').extract_first()
        try:
            author = response.css('.doc_author ::text').extract_first().split(':')[-1].translate(str.maketrans('', '', string.punctuation)).strip()
        except: 
            author = ''
        try:
            petitioner = response.css('.doc_title::text').extract_first().split(' vs ')[0].translate(str.maketrans('', '', string.punctuation)).strip()
        except:
            petitioner = ''
        try:
            respondent = response.css('.doc_title::text').extract_first().split(' vs ')[1].split(' on ')[0]
        except:
            respondent = ''
        matches = list(datefinder.find_dates(response.css('.doc_title ::text').extract_first()))
        date = matches[-1].day
        month = matches[-1].month
        year = matches[-1].year
        bench = response.css('.doc_bench ::text').extract_first().split(':')[-1] 
        items['url'] = 'https://indiankanoon.org/doc/1732220/'
        items['source'] = source
        items['petitioner'] = petitioner
        items['respondent'] = respondent
        items['date'] = date
        items['month'] = month
        items['year'] = year
        items['doc_author'] = author
        items['bench'] = bench
        yield items
        

