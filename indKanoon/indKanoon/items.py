# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CaseCounts(scrapy.Item):
    source = scrapy.Field()
    year = scrapy.Field()
    count = scrapy.Field()


class CaseDocURL(scrapy.Item):
    url = scrapy.Field()
