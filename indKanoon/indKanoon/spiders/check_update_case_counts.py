import scrapy
import re
from scrapy.spiders import CrawlSpider
from ..items import CaseCounts,CaseDocURL

class ListedCount(scrapy.Item):
    SourceName = scrapy.Field()
    Year = scrapy.Field()
    YearCount = scrapy.Field()


class CheckUpdateCaseCountsSpider(scrapy.Spider):
    name = 'case_counts'
    allowed_domains = ['indiankanoon.org']
    start_urls = ['http://indiankanoon.org/browse/']

    def processCount(self, count):
        try:
            f = re.search('\((.+?)\)', count).group(1)
        except AttributeError:
            f = '0'
        return f

    def processSource(self, sourceRaw):
        source = sourceRaw.replace("\n", "").replace("\\s+", "")
        return source

    def parse(self, response, **kwargs):
        sourceBrowseList = response.css('.browselist')
        for sourcePage in sourceBrowseList:
            sourceURL = sourcePage.css('a ::attr(href)').extract_first()
            if sourceURL:
                yield scrapy.Request(
                    response.urljoin(sourceURL),
                    callback=self.parseYearURL
                )

    def parseYearURL(self, response):
        items = CaseCounts()
        yearBrowseList = response.css('.browselist')
        sourceRaw = response.css('.static_bar ::text')[0].extract()
        source = self.processSource(sourceRaw)
        for yearPage in yearBrowseList:
            countRaw = yearPage.css(' ::text')[2].extract()
            count = int(self.processCount(countRaw))
            year = yearPage.css('a::text').extract_first()
            if year:
                items['source'] = source
                items['year'] = year
                items['count'] = count
                yield items

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# process.crawl(MySpider)
# process.start() 