import scrapy


class IndkanoonSpiderSpider(scrapy.Spider):
    name = 'indKanoon_spider'
    allowed_domains = ['indiankanoon.org']
    start_urls = ['https://indiankanoon.org/browse']

    def parse(self, response):
        pass
