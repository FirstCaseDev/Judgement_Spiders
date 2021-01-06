import scrapy
import re
import regex
import pymongo
import string
from scrapy.spiders import CrawlSpider, Rule
from ..items import document
from scrapy.linkextractors import LinkExtractor
import datefinder
items = document()

client = pymongo.MongoClient("mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["SCcaseurls"]
col = db["SCurls00"]


class ExtractorSpider(scrapy.Spider):
    name = 'extractor'
    allowed_domains = ['indiankanoon.org']
    # start_urls = ['https://indiankanoon.org/doc/1732220/']

    def __init__(self, start_line=0):
        # define init fuction to start scrolling from database
        pass
    
    def start_requests(self):
        # y = col.distinct('url')
        x = col.find({},{'url': 1})
        if x is not None: 
            for a in x:   
                url = a['url']
                # print (url)
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
        TEXT_SELECTOR = '.judgments'
        all_text = response.css(TEXT_SELECTOR)
        INTRO_SELECTOR = 'p ::text'
        end_texts = response.css(INTRO_SELECTOR)[-3:].extract()
        for segment in end_texts:
            try:
                segment = segment.strip().lower()
            except:
                segment = ''
            print(segment)
            if 'allow' in segment:
                judgement = 'allowed'
                if 'partly' in segment:
                    judgement = 'partly allowed'
                break
            elif 'dismiss' in segment:
                judgement = 'dismissed'
                if 'partly' in segment:
                    judgement = 'partly dismissed'
                break    
            else:
                judgement = 'tied / unclear'
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
        title = response.css('.doc_title ::text').extract_first() 
        date = matches[-1].day
        month = matches[-1].month
        year = matches[-1].year
        bench = response.css('.doc_bench ::text').extract_first().split(':')[-1]
        PARA_SELECTOR = '* ::text'
        para_text = all_text.css(PARA_SELECTOR).extract()
        para_text = " ".join(para_text)
        para_text = para_text.replace('\n', ' ')
        para_text = para_text.replace('\t', ' ')
        para_text = re.sub(' +', ' ', para_text) 
        para_text = para_text.replace("Try out our Premium Member services: Virtual Legal Assistant , Query Alert Service and an ad-free experience. Free for one month and pay only if you like it.",' ')
        items['url'] = response.request.url
        items['source'] = source
        items['petitioner'] = petitioner
        items['respondent'] = respondent
        items['date'] = date
        items['month'] = month
        items['year'] = year
        items['doc_author'] = author
        items['bench'] = bench
        items['judgement'] = judgement
        items['judgement_text'] = para_text
        items['title'] = title
        yield items
        

