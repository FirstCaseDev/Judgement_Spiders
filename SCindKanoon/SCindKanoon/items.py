# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScindkanoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class document(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    petitioner = scrapy.Field()
    respondent = scrapy.Field()
    date = scrapy.Field()
    month = scrapy.Field()
    year = scrapy.Field()
    doc_author = scrapy.Field()
    bench = scrapy.Field()
    judgement_result = scrapy.Field()
    judgement_text = scrapy.Field()
    # cited_by = scrapy.Field()
    # cited = scrapy.Field()

class CaseDocURL(scrapy.Item):
    url = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    date = scrapy.Field()
    
