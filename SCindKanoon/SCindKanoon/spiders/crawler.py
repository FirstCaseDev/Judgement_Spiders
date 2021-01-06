import scrapy
from ..items import CaseDocURL
import datefinder
items = CaseDocURL()


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    # allowed_domains = ['indiankanoon.org']
    start_urls = ['http://indiankanoon.org/browse/supremecourt/']
    items['source'] = 'Supreme Court of India'

    def concatURL(self, url_str):
        url_str_split = url_str.split('/')
        new_url = 'https://indiankanoon.org/' + url_str_split[1] + '/' + url_str_split[2]
        return new_url

    def parse(self, response):
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
        for result_page in response.css('.result_title'):
            url_title = result_page.css('a ::text').extract_first()
            url_fragment = result_page.css('a ::attr(href)').extract_first()
            url = self.concatURL(url_fragment)
            matches = list(datefinder.find_dates(url_title))
            items['year'] = matches[0].year
            items['month'] = matches[0].month
            items['date'] = matches[0].day
            items['url'] = url
            items['title'] = url_title
            yield items

        NEXT_PAGE_SELECTOR = '.bottom a ::attr(href)'
        next_page = response.css('.bottom a ::attr(href)').extract()[-1]
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parseListedCases)

