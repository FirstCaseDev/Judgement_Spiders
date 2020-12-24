import scrapy
from ..items import CaseDocURL


class BrowseAllDocsListSpider(scrapy.Spider):
    name = 'all_list'
    allowed_domains = ['indiankanoon.org']
    start_urls = ['https://indiankanoon.org/browse/']

    def concatURL(self, url_str):
        url_str_split = url_str.split('/')
        new_url = 'indiankanoon.org/doc/' + url_str_split[2]
        return new_url

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
        yearBrowseList = response.css('.browselist')
        for yearPage in yearBrowseList:
            yearURL = yearPage.css('a ::attr(href)').extract_first()
            if yearURL:
                yield scrapy.Request(
                    response.urljoin(yearURL),
                    callback=self.parseMonthURL
                )

    def parseMonthURL(self, response):
        monthBrowseList = response.css('.browselist')
        for monthPage in monthBrowseList:
            monthURL = monthPage.css('a ::attr(href)').extract_first()
            if monthURL:
                yield scrapy.Request(
                    response.urljoin(monthURL),
                    callback=self.parseListedCases
                )

    def parseListedCases(self, response):
        items = CaseDocURL()
        for result_page in response.css('   e'):
            url_fragment = result_page.css('a ::attr(href)').extract_first()
            url = self.concatURL(url_fragment)
            if url:
                items['url'] = url
                yield items

        NEXT_PAGE_SELECTOR = '.bottom a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parseListedCases)
